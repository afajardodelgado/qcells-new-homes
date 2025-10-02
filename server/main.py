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

# Load .env
load_dotenv()

LOGIN_URL = os.getenv("SALESFORCE_LOGIN_URL", "https://test.salesforce.com").strip()
CLIENT_ID = (os.getenv("SALESFORCE_CLIENT_ID") or "").strip()
USERNAME = (os.getenv("SALESFORCE_USERNAME") or "").strip()
KEY_PATH = os.getenv("SALESFORCE_JWT_KEY_PATH", "").strip()
DEFAULT_TEST_SOQL = os.getenv("DEFAULT_TEST_SOQL", "SELECT Id, Name FROM Account LIMIT 5").strip()

# FastAPI app
app = FastAPI(title="SF JWT Proxy")

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


def mint_access_token(login_url: str, client_id: str, username: str, key_path: str) -> dict:
    if not login_url.startswith("https://test.salesforce.com") and not login_url.startswith("https://login.salesforce.com"):
        raise HTTPException(status_code=400, detail="LOGIN_URL must be https://test.salesforce.com (sandbox) or https://login.salesforce.com (prod)")
    if not client_id:
        raise HTTPException(status_code=400, detail="SALESFORCE_CLIENT_ID is empty")
    if not username:
        raise HTTPException(status_code=400, detail="SALESFORCE_USERNAME is empty")
    if not key_path:
        raise HTTPException(status_code=400, detail="SALESFORCE_JWT_KEY_PATH is empty")

    key_file = Path(key_path)
    if not key_file.exists():
        raise HTTPException(status_code=500, detail=f"Private key not found at: {key_file}")
    private_key = key_file.read_text()

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


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/sf/query")
def sf_query(req: QueryRequest):
    try:
        auth = mint_access_token(LOGIN_URL, CLIENT_ID, USERNAME, KEY_PATH)
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


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)
