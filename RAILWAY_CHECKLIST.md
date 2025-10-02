# Railway Deployment Checklist

## ✅ Pre-Deployment Fixes Applied

The following issues have been fixed to ensure successful Railway deployment:

### 1. ✅ Private Key Management (CRITICAL FIX)
**Problem:** Railway doesn't persist files between deployments, so file-based private keys fail.

**Solution:** Added support for environment variable-based private keys.

**What was changed:**
- Added `SALESFORCE_PRIVATE_KEY` environment variable support
- Modified `mint_access_token()` to accept key content directly
- Supports both file-based (local dev) and env var (production) keys

**Railway Setup:**
```bash
# Copy your private key content (including BEGIN/END lines)
cat server.key

# In Railway dashboard, add environment variable:
# Variable: SALESFORCE_PRIVATE_KEY
# Value: Paste the entire key content, preserving newlines
# Railway will automatically escape the newlines as \n
```

### 2. ✅ Startup Configuration Validation
**Problem:** App would start but fail on first request if misconfigured.

**Solution:** Added startup validation that fails fast with clear error messages.

**Benefits:**
- Railway logs will show exact configuration errors immediately
- Health checks will fail if critical env vars are missing
- Clear warnings for security issues (CORS=*, sandbox in prod, etc.)

### 3. ✅ Nixpacks Build Configuration
**Problem:** Python from Nix doesn't include pip by default, and `python312Packages.pip` didn't work.

**Solution:** Create a Python virtual environment which always includes pip:
- `python3 -m venv /opt/venv` creates venv with pip bundled
- Install packages using `/opt/venv/bin/pip`
- Run app using `/opt/venv/bin/uvicorn`

## 🚀 Railway Deployment Steps

### Step 1: Set Environment Variables in Railway

Required variables:
```
ENVIRONMENT=production
SALESFORCE_LOGIN_URL=https://login.salesforce.com
SALESFORCE_CLIENT_ID=<your_connected_app_consumer_key>
SALESFORCE_USERNAME=<your_salesforce_username>
SALESFORCE_PRIVATE_KEY=<paste_entire_private_key_here>
```

Optional but recommended:
```
DEFAULT_TEST_SOQL=SELECT Id, Name FROM Account LIMIT 5
CORS_ORIGINS=https://your-app.railway.app
SENTRY_DSN=<your_sentry_dsn>
```

### Step 2: Verify Build Configuration

Railway should auto-detect:
- **Builder:** Nixpacks
- **Start Command:** `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
- **Health Check:** `/api/health`

These are configured in `railway.toml` and `nixpacks.toml`.

### Step 3: Deploy and Monitor

1. Push to main branch (auto-deploys)
2. Check Railway logs for:
   - ✅ "Configuration validated successfully"
   - ⚠️ Any warnings about security settings
   - ❌ Any configuration errors

3. Test endpoints:
   - Health: `https://your-app.railway.app/api/health`
   - SF Test: `https://your-app.railway.app/api/sf/test`

## 🐛 Remaining Potential Issues

### Issue 1: CORS Configuration
**Risk:** Medium
**Symptom:** Frontend can't connect to backend API

**Check:**
- `CORS_ORIGINS` should match your Railway app URL
- Format: `https://your-app.railway.app` (no trailing slash)
- For multiple origins: `https://app1.com,https://app2.com`

**Fix:**
```bash
# In Railway dashboard, update CORS_ORIGINS:
CORS_ORIGINS=https://your-exact-app-url.railway.app
```

### Issue 2: Salesforce Authentication
**Risk:** High
**Symptom:** 401/403 errors, "invalid_grant" errors

**Checklist:**
- [ ] Connected App Consumer Key matches `SALESFORCE_CLIENT_ID`
- [ ] User is authorized in Connected App settings
- [ ] Private key matches certificate uploaded to Salesforce
- [ ] Using correct LOGIN_URL (prod vs sandbox)
- [ ] User has API access permissions

**Debug:**
```bash
# Check Railway logs for exact error message
railway logs --tail 100

# Common errors:
# - "invalid_grant" = user not authorized or wrong key
# - "invalid_client_id" = wrong CLIENT_ID
# - "user hasn't approved this consumer" = need to authorize in SF
```

### Issue 3: Private Key Format
**Risk:** Medium
**Symptom:** JWT encoding errors, "invalid key format"

**Correct Format:**
```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA...
(multiple lines)
...
-----END RSA PRIVATE KEY-----
```

**Common Issues:**
- ❌ Missing BEGIN/END lines
- ❌ Extra spaces or characters
- ❌ Wrong key type (must be RSA, not ECDSA)
- ❌ Wrong encoding (must be PEM, not DER)

**Fix:**
```bash
# Verify your key format:
openssl rsa -in server.key -check -noout

# Should output: "RSA key ok"
```

### Issue 4: Static File Paths
**Risk:** Low
**Status:** Should work correctly

The app uses relative paths from `__file__`, which should work on Railway:
```python
ROOT_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT_DIR / "web"
ASSETS_DIR = ROOT_DIR / "assets"
```

**If frontend doesn't load:**
1. Check Railway logs for "Frontend not built yet"
2. Verify `web/` and `assets/` directories are in your repo
3. Ensure they're not in `.gitignore`

### Issue 5: Port Binding
**Risk:** Very Low
**Status:** Configured correctly

Railway auto-assigns `$PORT` environment variable, and the app uses it:
```python
port = int(os.getenv("PORT", "8000"))
```

Start command in `railway.toml` uses `$PORT` correctly:
```toml
startCommand = "uvicorn server.main:app --host 0.0.0.0 --port $PORT"
```

**Only an issue if:** You manually override the PORT variable (don't do this).

## 🔍 Debugging Commands

### View Railway Logs
```bash
# Real-time logs
railway logs

# Last 100 lines
railway logs --tail 100

# Follow logs
railway logs -f
```

### Test Locally with Railway-like Setup
```bash
# Set environment variables like Railway would
export ENVIRONMENT=production
export SALESFORCE_LOGIN_URL=https://login.salesforce.com
export SALESFORCE_CLIENT_ID=your_client_id
export SALESFORCE_USERNAME=your_username
export SALESFORCE_PRIVATE_KEY="$(cat server.key)"
export CORS_ORIGINS=http://localhost:8000
export PORT=8000

# Run the app
uvicorn server.main:app --host 0.0.0.0 --port 8000

# Test health endpoint
curl http://localhost:8000/api/health

# Test Salesforce connection
curl http://localhost:8000/api/sf/test
```

## 📊 Success Criteria

Your deployment is successful when:

1. ✅ Railway build completes without errors
2. ✅ Health check endpoint returns `{"status": "ok"}`
3. ✅ Startup logs show "✅ Configuration validated successfully"
4. ✅ `/api/sf/test` returns Salesforce data (not 401/500)
5. ✅ Frontend loads and shows the UI
6. ✅ No CORS errors in browser console

## 🆘 Still Having Issues?

1. **Check Railway logs first:**
   ```bash
   railway logs --tail 200
   ```

2. **Common error patterns:**
   - "Configuration errors:" → Missing or invalid env vars
   - "invalid_grant" → Salesforce authentication issue
   - "Private key not found" → Using KEY_PATH instead of PRIVATE_KEY
   - "502 Bad Gateway" → App crashed on startup
   - CORS errors → Wrong CORS_ORIGINS setting

3. **Verify environment variables:**
   ```bash
   railway variables
   ```

4. **Test Salesforce credentials locally first:**
   ```bash
   # Use the exact same env vars you set in Railway
   python3 -c "from server.main import mint_access_token; print('Auth successful')"
   ```

## 📝 Notes

- **Build time:** ~30-60 seconds (Nixpacks installs Python + dependencies)
- **Cold start:** ~2-3 seconds (FastAPI startup + validation)
- **Memory usage:** ~100-200 MB (sufficient for 512MB Railway plan)
- **Auto-deploy:** Enabled on push to main branch
- **Health checks:** Every 30 seconds to `/api/health`

---

**Last Updated:** 2025-10-02
**Railway Builder:** Nixpacks v1.38.0
**Python Version:** 3.12
