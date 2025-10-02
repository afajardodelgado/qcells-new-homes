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


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)
