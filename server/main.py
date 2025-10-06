import os
import json
import time
from pathlib import Path
from typing import List, Optional

import jwt
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

# Load .env
load_dotenv()

# Initialize Sentry (optional - only if SENTRY_DSN is set)
SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").strip()

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0 if ENVIRONMENT == "development" else 0.1,
        profiles_sample_rate=1.0 if ENVIRONMENT == "development" else 0.1,
    )

LOGIN_URL = os.getenv("SALESFORCE_LOGIN_URL", "https://test.salesforce.com").strip()
CLIENT_ID = (os.getenv("SALESFORCE_CLIENT_ID") or "").strip()
USERNAME = (os.getenv("SALESFORCE_USERNAME") or "").strip()
KEY_PATH = os.getenv("SALESFORCE_JWT_KEY_PATH", "").strip()
PRIVATE_KEY_CONTENT = os.getenv("SALESFORCE_PRIVATE_KEY", "").strip()  # Direct key content
DEFAULT_TEST_SOQL = os.getenv("DEFAULT_TEST_SOQL", "SELECT Id, Name FROM Account LIMIT 5").strip()

# FastAPI app
app = FastAPI(title="SF JWT Proxy")

# Startup validation
@app.on_event("startup")
async def validate_configuration():
    """Validate configuration on startup to fail fast if misconfigured"""
    import logging
    logger = logging.getLogger("uvicorn")
    
    warnings = []
    sf_warnings = []
    
    # Check Salesforce configuration (non-blocking)
    if not CLIENT_ID:
        sf_warnings.append("SALESFORCE_CLIENT_ID is not set")
    if not USERNAME:
        sf_warnings.append("SALESFORCE_USERNAME is not set")
    if not PRIVATE_KEY_CONTENT and not KEY_PATH:
        sf_warnings.append("Either SALESFORCE_PRIVATE_KEY or SALESFORCE_JWT_KEY_PATH must be set")
    
    # Check if using file path but file doesn't exist
    if KEY_PATH and not PRIVATE_KEY_CONTENT:
        key_file = Path(KEY_PATH)
        if not key_file.exists():
            sf_warnings.append(f"SALESFORCE_JWT_KEY_PATH points to non-existent file: {KEY_PATH}")
    
    # Warnings for development settings in production
    if ENVIRONMENT == "production":
        if LOGIN_URL == "https://test.salesforce.com":
            warnings.append("Using sandbox LOGIN_URL in production environment")
        if allow_all:
            warnings.append("CORS_ORIGINS is set to '*' (allow all) in production - security risk!")
    
    # Log all warnings
    for warning in warnings:
        logger.warning(f"⚠️  {warning}")
    
    # Salesforce config warnings (don't crash - API endpoints will fail gracefully)
    if sf_warnings:
        logger.warning("⚠️  Salesforce configuration incomplete - API endpoints will fail:")
        for sf_warning in sf_warnings:
            logger.warning(f"   - {sf_warning}")
        logger.warning("   Configure these variables in Railway to enable Salesforce integration")
    else:
        logger.info("✅ Salesforce configuration validated successfully")
    
    logger.info("✅ Application startup complete")

# CORS
raw_origins = os.getenv("CORS_ORIGINS", "*").split(",")
origins: List[str] = [o.strip() for o in raw_origins if o.strip()]
allow_all = len(origins) == 1 and origins[0] == "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths for static frontend and assets
ROOT_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT_DIR / "web"
ASSETS_DIR = ROOT_DIR / "assets"

# Mount static directories if present
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR), html=False), name="static")
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR), html=False), name="assets")

# Serve the SPA index
@app.get("/")
def serve_index():
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        return {"message": "Frontend not built yet"}
    return FileResponse(str(index_path))


class QueryRequest(BaseModel):
    soql: str
    tooling: Optional[bool] = False


def mint_access_token(login_url: str, client_id: str, username: str, key_path: str, key_content: str = "") -> dict:
    if not login_url.startswith("https://test.salesforce.com") and not login_url.startswith("https://login.salesforce.com"):
        raise HTTPException(status_code=400, detail="LOGIN_URL must be https://test.salesforce.com (sandbox) or https://login.salesforce.com (prod)")
    if not client_id:
        raise HTTPException(status_code=400, detail="SALESFORCE_CLIENT_ID is empty")
    if not username:
        raise HTTPException(status_code=400, detail="SALESFORCE_USERNAME is empty")
    
    # Support both file-based and environment variable key sources
    private_key = ""
    if key_content:
        # Use key from environment variable (Railway deployment)
        private_key = key_content
    elif key_path:
        # Use key from file (local development)
        key_file = Path(key_path)
        if not key_file.exists():
            raise HTTPException(status_code=500, detail=f"Private key not found at: {key_file}")
        private_key = key_file.read_text()
    else:
        raise HTTPException(status_code=400, detail="Either SALESFORCE_JWT_KEY_PATH or SALESFORCE_PRIVATE_KEY must be set")

    now = int(time.time())
    payload = {
        "iss": client_id,
        "sub": username,
        "aud": login_url,
        "exp": now + 300,
    }
    assertion = jwt.encode(payload, private_key, algorithm="RS256")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(
        f"{login_url}/services/oauth2/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        headers=headers,
        timeout=30,
    )

    try:
        data = resp.json()
    except Exception:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=data)
    return data


class ErrorLog(BaseModel):
    message: str
    filename: Optional[str] = None
    lineno: Optional[int] = None
    colno: Optional[int] = None
    stack: Optional[str] = None
    timestamp: Optional[str] = None
    userAgent: Optional[str] = None
    type: Optional[str] = "error"


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/log-error")
def log_frontend_error(error: ErrorLog):
    """Log frontend errors to Sentry and application logs"""
    import logging

    logger = logging.getLogger("frontend_errors")
    logger.error(
        f"Frontend Error: {error.message}",
        extra={
            "filename": error.filename,
            "lineno": error.lineno,
            "colno": error.colno,
            "stack": error.stack,
            "timestamp": error.timestamp,
            "userAgent": error.userAgent,
            "type": error.type
        }
    )

    # Send to Sentry if configured
    if SENTRY_DSN:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("frontend", {
                "filename": error.filename,
                "lineno": error.lineno,
                "colno": error.colno,
                "userAgent": error.userAgent
            })
            sentry_sdk.capture_message(error.message, level="error")

    return {"status": "logged"}


@app.post("/api/sf/query")
def sf_query(req: QueryRequest):
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH, PRIVATE_KEY_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Use simple-salesforce lazily to avoid import cost when not needed
    try:
        from simple_salesforce import Salesforce
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"simple-salesforce not installed: {e}")

    # Connect
    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])

    # Tooling API support if requested
    if req.tooling:
        result = sf.toolingexecute("query", method="GET", params={"q": req.soql})
        return result

    # Standard query
    result = sf.query_all(req.soql)
    return result


@app.get("/api/sf/test")
def sf_test():
    return sf_query(QueryRequest(soql=DEFAULT_TEST_SOQL))


@app.get("/api/sf/builders")
def get_builders():
    """Get National Builders with extracted City and State from compound address"""
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH, PRIVATE_KEY_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        from simple_salesforce import Salesforce
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"simple-salesforce not installed: {e}")

    # Connect to Salesforce
    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])

    # Query National Builders
    soql = """
    SELECT 
        Id,
        Name, 
        Headquarters_Address__c,
        Website__c
    FROM National_Builder__c
    """
    
    result = sf.query_all(soql)
    
    # Process records to extract City and State from compound address
    builders = []
    for record in result.get('records', []):
        hq_address = record.get('Headquarters_Address__c', {})
        
        builder = {
            "Id": record.get('Id', ''),
            "Name": record.get('Name', ''),
            "City": hq_address.get('city', '') if isinstance(hq_address, dict) else '',
            "State": hq_address.get('state', '') if isinstance(hq_address, dict) else '',
            "Website": record.get('Website__c', '')
        }
        builders.append(builder)
    
    return {
        "builders": builders,
        "totalSize": len(builders)
    }


@app.get("/api/sf/communities")
def get_communities():
    """Get all Divisions with parent (National Builder) fields"""
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH, PRIVATE_KEY_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        from simple_salesforce import Salesforce
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"simple-salesforce not installed: {e}")

    # Connect to Salesforce
    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])

    # Query all Divisions with parent (National Builder) fields
    soql = """
    SELECT
        Id,
        Name,
        Division_Address__c,
        National_Builder__c,
        National_Builder__r.Name,
        National_Builder__r.Service_Territories__c,
        National_Builder__r.Builder_ID_Code__c,
        National_Builder__r.Headquarters_Address__c,
        National_Builder__r.National_Account_Status__c,
        National_Builder__r.Account_Manager__c,
        National_Builder__r.Account_Manager__r.Name
    FROM Division__c
    """

    result = sf.query_all(soql)
    records = result.get('records', [])
    
    # Process all divisions
    communities = []
    for record in records:
        div_address = record.get('Division_Address__c', {})
        parent = record.get('National_Builder__r', {})
        hq_address = parent.get('Headquarters_Address__c', {})
        account_mgr = parent.get('Account_Manager__r', {})
        
        community = {
            "Division_Id": record.get('Id', ''),
            "Division_Name": record.get('Name', ''),
            "Division_City": div_address.get('city', '') if isinstance(div_address, dict) else '',
            "Division_State": div_address.get('state', '') if isinstance(div_address, dict) else '',
            "Builder_Name": parent.get('Name', '') if isinstance(parent, dict) else '',
            "Builder_ID_Code": parent.get('Builder_ID_Code__c', '') if isinstance(parent, dict) else '',
            "National_Account_Status": parent.get('National_Account_Status__c', '') if isinstance(parent, dict) else '',
            "Service_Territories": parent.get('Service_Territories__c', '') if isinstance(parent, dict) else '',
            "Account_Manager_Name": account_mgr.get('Name', '') if isinstance(account_mgr, dict) else '',
            "HQ_City": hq_address.get('city', '') if isinstance(hq_address, dict) else '',
            "HQ_State": hq_address.get('state', '') if isinstance(hq_address, dict) else '',
            "National_Builder__c": record.get('National_Builder__c', ''),
        }
        communities.append(community)
    
    return {
        "communities": communities,
        "totalSize": len(communities)
    }


@app.get("/api/sf/divisions/{builder_id}")
def get_divisions(builder_id: str):
    """Get Divisions for a specific National Builder with parent fields"""
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH, PRIVATE_KEY_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        from simple_salesforce import Salesforce
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"simple-salesforce not installed: {e}")

    # Connect to Salesforce
    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])

    # Query Divisions with parent (National Builder) fields
    soql = f"""
    SELECT
        Id,
        Name,
        Division_Address__c,
        National_Builder__c,
        National_Builder__r.Name,
        National_Builder__r.Service_Territories__c,
        National_Builder__r.Builder_ID_Code__c,
        National_Builder__r.Headquarters_Address__c,
        National_Builder__r.National_Account_Status__c,
        National_Builder__r.Account_Manager__c,
        National_Builder__r.Account_Manager__r.Name
    FROM Division__c
    WHERE National_Builder__c = '{builder_id}'
    """

    result = sf.query_all(soql)
    records = result.get('records', [])
    
    # Builder info (from first record's parent, if any)
    builder_info = None
    if records:
        parent = records[0].get('National_Builder__r', {})
        hq_address = parent.get('Headquarters_Address__c', {})
        account_mgr = parent.get('Account_Manager__r', {})
        
        builder_info = {
            "Name": parent.get('Name', ''),
            "Builder_ID_Code": parent.get('Builder_ID_Code__c', ''),
            "National_Account_Status": parent.get('National_Account_Status__c', ''),
            "Service_Territories": parent.get('Service_Territories__c', ''),
            "Account_Manager_Name": account_mgr.get('Name', '') if isinstance(account_mgr, dict) else '',
            "HQ_City": hq_address.get('city', '') if isinstance(hq_address, dict) else '',
            "HQ_State": hq_address.get('state', '') if isinstance(hq_address, dict) else '',
        }
    
    # Process divisions
    divisions = []
    for record in records:
        div_address = record.get('Division_Address__c', {})
        
        division = {
            "Division_Id": record.get('Id', ''),
            "Division_Name": record.get('Name', ''),
            "Division_City": div_address.get('city', '') if isinstance(div_address, dict) else '',
            "Division_State": div_address.get('state', '') if isinstance(div_address, dict) else '',
        }
        divisions.append(division)
    
    return {
        "builder_info": builder_info,
        "divisions": divisions,
        "totalSize": len(divisions)
    }


@app.get("/api/sf/homes")
def get_homes():
    """
    Fetch all New Home Projects with related lookups
    """
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH, PRIVATE_KEY_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        from simple_salesforce import Salesforce
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"simple-salesforce not installed: {e}")

    # Connect to Salesforce
    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])
    
    soql = """
    SELECT
        Id,
        Name,
        Project_Stage__c,
        New_Home_Community_Name__r.Name,
        National_Builder_Account__r.Name,
        Builder_Division__c,
        Account__r.Name,
        Authority_Having_Jurisdiction__r.Name,
        Utility__r.Name,
        Service_Voltage__c,
        Street_Address__c,
        Street_Address_2__c,
        City__c,
        State__c,
        Zip_Code__c,
        Country__c,
        Phase__c,
        Building__c,
        Lot__c,
        APN_Number__c,
        County__c,
        Application_ID__c,
        Embedded_URL__c,
        New_Home_Installer__r.Name,
        New_Home_Partner__r.Name,
        Primary_PV_Prod__r.Name,
        Electrical__r.Name,
        Plan_Type__r.Name,
        Finance_Type__c,
        Installer_Partner_PV__c,
        Installer_Partner_Battery__c,
        Model_Home__c,
        Legal_Owner__c,
        New_Home_Build__c,
        Non_Solar_Home__c,
        Estimated_COE_Date__c,
        Actual_COE_Date__c,
        Primary_Contact_Name__c,
        Primary_Phone_Number__c,
        Email__c,
        Customer_Notes__c,
        New_Home_Welcome_Email_Sent__c,
        Permission_to_Operate_Email_Sent__c
    FROM New_Home_Project__c
    """
    
    result = sf.query_all(soql)
    records = result.get('records', [])
    
    # Process homes
    homes = []
    for record in records:
        # Helper to get lookup field
        def get_lookup(obj, field):
            return obj.get(field, '') if isinstance(obj, dict) else ''
        
        home = {
            "New_Home_Project_Id": record.get('Id', ''),
            "New_Home_Project_Name": record.get('Name', ''),
            "Project_Stage": record.get('Project_Stage__c', ''),
            "Community_Name": get_lookup(record.get('New_Home_Community_Name__r'), 'Name'),
            "Builder_Name": get_lookup(record.get('National_Builder_Account__r'), 'Name'),
            "Builder_Division": record.get('Builder_Division__c', ''),
            "Account_Name": get_lookup(record.get('Account__r'), 'Name'),
            "AHJ_Name": get_lookup(record.get('Authority_Having_Jurisdiction__r'), 'Name'),
            "Utility_Name": get_lookup(record.get('Utility__r'), 'Name'),
            "Service_Voltage": record.get('Service_Voltage__c', ''),
            "Street_Address": record.get('Street_Address__c', ''),
            "Street_Address_2": record.get('Street_Address_2__c', ''),
            "City": record.get('City__c', ''),
            "State": record.get('State__c', ''),
            "Zip": record.get('Zip_Code__c', ''),
            "Country": record.get('Country__c', ''),
            "Phase": record.get('Phase__c', ''),
            "Building_Number": record.get('Building__c', ''),
            "Lot_Number": record.get('Lot__c', ''),
            "APN_Number": record.get('APN_Number__c', ''),
            "County": record.get('County__c', ''),
            "Application_ID": record.get('Application_ID__c', ''),
            "Embedded_URL": record.get('Embedded_URL__c', ''),
            "Installer_Name": get_lookup(record.get('New_Home_Installer__r'), 'Name'),
            "Partner_Name": get_lookup(record.get('New_Home_Partner__r'), 'Name'),
            "Primary_PV_Prod_Name": get_lookup(record.get('Primary_PV_Prod__r'), 'Name'),
            "Electrical_Name": get_lookup(record.get('Electrical__r'), 'Name'),
            "Plan_Type_Name": get_lookup(record.get('Plan_Type__r'), 'Name'),
            "Finance_Type": record.get('Finance_Type__c', ''),
            "Installer_Partner_PV": record.get('Installer_Partner_PV__c', ''),
            "Installer_Partner_Battery": record.get('Installer_Partner_Battery__c', ''),
            "Model_Home": record.get('Model_Home__c', ''),
            "Legal_Owner": record.get('Legal_Owner__c', ''),
            "New_Home_Build": record.get('New_Home_Build__c', ''),
            "Non_Solar_Home": record.get('Non_Solar_Home__c', ''),
            "Estimated_COE_Date": record.get('Estimated_COE_Date__c', ''),
            "Actual_COE_Date": record.get('Actual_COE_Date__c', ''),
            "Primary_Contact_Name": record.get('Primary_Contact_Name__c', ''),
            "Primary_Phone_Number": record.get('Primary_Phone_Number__c', ''),
            "Email": record.get('Email__c', ''),
            "Customer_Notes": record.get('Customer_Notes__c', ''),
            "Welcome_Email_Sent": record.get('New_Home_Welcome_Email_Sent__c', False),
            "PTO_Email_Sent": record.get('Permission_to_Operate_Email_Sent__c', False),
        }
        homes.append(home)
    
    return {
        "homes": homes,
        "totalSize": len(homes)
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)
