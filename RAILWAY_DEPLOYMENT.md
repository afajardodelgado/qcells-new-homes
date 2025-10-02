# Railway Deployment Guide

This document provides instructions for deploying the Q.CELLS New Homes Solar Support Suite to Railway.

## Prerequisites

1. Railway account (https://railway.app)
2. Salesforce Connected App configured for JWT Bearer Flow
3. Private key file (server.key) for JWT authentication
4. Sentry account for error monitoring (optional but recommended)

## Environment Variables

Configure the following environment variables in Railway dashboard:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `production` |
| `SALESFORCE_LOGIN_URL` | Salesforce login URL | `https://login.salesforce.com` |
| `SALESFORCE_CLIENT_ID` | Connected App Consumer Key | `3MVG9...` |
| `SALESFORCE_USERNAME` | Salesforce username | `user@company.com` |
| `SALESFORCE_JWT_KEY_PATH` | Path to private key | `/app/server.key` |
| `PORT` | Server port (Railway auto-assigns) | `8000` |

### Optional Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEFAULT_TEST_SOQL` | Default SOQL query for testing | `SELECT Id, Name FROM Account LIMIT 5` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `https://your-app.railway.app` |
| `SENTRY_DSN` | Sentry error tracking DSN | `https://...@sentry.io/...` |

## Deployment Steps

### 1. Create New Railway Project

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init
```

Or use the Railway dashboard to create a new project from GitHub.

### 2. Connect GitHub Repository

1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python and use `requirements.txt`

### 3. Configure Environment Variables

In Railway dashboard:

1. Go to your project
2. Click on the service
3. Navigate to "Variables" tab
4. Add all required environment variables from the table above

**Important:** Set `CORS_ORIGINS` to your Railway app URL:
```
CORS_ORIGINS=https://your-app-name.railway.app
```

### 4. Add Private Key File

Railway supports secrets for sensitive files:

**Option A: Environment Variable (Base64)**
```bash
# Encode your private key
cat server.key | base64

# Add to Railway as SALESFORCE_JWT_KEY_BASE64
# Then decode in startup script
```

**Option B: Railway Volumes**
1. Create a volume in Railway
2. Upload `server.key` to the volume
3. Mount volume to `/app`
4. Set `SALESFORCE_JWT_KEY_PATH=/app/server.key`

**Recommended: Option B** for better security and easier management.

### 5. Configure Build Settings

Railway auto-detects Python projects. Ensure:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn server.main:app --host 0.0.0.0 --port $PORT`

These are usually auto-configured, but verify in "Settings" → "Deploy".

### 6. Deploy

Railway will automatically deploy on every push to your main branch.

Manual deploy:
```bash
railway up
```

### 7. Verify Deployment

After deployment:

1. Check Railway logs for errors
2. Visit your app URL: `https://your-app-name.railway.app`
3. Test health endpoint: `https://your-app-name.railway.app/api/health`
4. Test Salesforce connection: `https://your-app-name.railway.app/api/sf/test`

## Monitoring and Logs

### View Logs

In Railway dashboard:
1. Go to your service
2. Click "Deployments"
3. Select latest deployment
4. View logs in real-time

Or via CLI:
```bash
railway logs
```

### Sentry Error Monitoring

1. Create Sentry project at https://sentry.io
2. Copy DSN from project settings
3. Add `SENTRY_DSN` to Railway environment variables
4. Errors will automatically be sent to Sentry

## Custom Domain (Optional)

1. In Railway dashboard, go to "Settings"
2. Click "Generate Domain" for a Railway subdomain
3. Or add custom domain in "Domains" section
4. Update DNS records as instructed
5. Update `CORS_ORIGINS` to include your custom domain

## Troubleshooting

### Application Won't Start

**Check:**
- All required environment variables are set
- `SALESFORCE_JWT_KEY_PATH` points to correct location
- Private key file exists and is readable
- Logs for specific error messages

### Salesforce Authentication Failed

**Check:**
- `SALESFORCE_CLIENT_ID` matches Connected App Consumer Key
- `SALESFORCE_USERNAME` is authorized in Connected App
- `SALESFORCE_LOGIN_URL` is correct (prod vs sandbox)
- Private key matches the certificate uploaded to Salesforce

### CORS Errors

**Check:**
- `CORS_ORIGINS` includes your Railway app URL
- Format: `https://your-app.railway.app` (no trailing slash)
- For multiple origins: `https://app1.com,https://app2.com`

### 502 Bad Gateway

**Check:**
- Application is binding to `0.0.0.0:$PORT`
- Health check endpoint `/api/health` is responding
- Logs for application crashes

## Scaling

For 40-50 users, default Railway settings are sufficient:

- **Instances:** 1 (default)
- **Memory:** 512MB - 1GB (auto-scales)
- **CPU:** Shared (auto-scales)

If you need to scale:
1. Go to "Settings" → "Resources"
2. Adjust memory/CPU as needed
3. Railway bills based on usage

## Backup and Recovery

### Environment Variables Backup

Export variables periodically:
```bash
railway variables
```

Save output to secure location.

### Database Backup

This app uses Salesforce as the data source (no local database). Ensure Salesforce backups are configured separately.

## CI/CD Integration

Railway supports automatic deployments:

1. Push to `main` branch → Auto-deploy to production
2. Configure preview environments for feature branches (optional)

### GitHub Actions (Optional)

Add tests before deployment:

```yaml
# .github/workflows/deploy.yml
name: Test and Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest
```

## Security Best Practices

1. **Never commit:**
   - `.env` files
   - `server.key` private key
   - Any credentials

2. **Railway secrets:**
   - Use Railway's environment variables for all secrets
   - Enable "Deploy Hooks" only for trusted sources

3. **CORS:**
   - Never use `CORS_ORIGINS=*` in production
   - Whitelist only your specific domains

4. **Sentry:**
   - Enable Sentry in production for error tracking
   - Review errors regularly

## Support

For Railway-specific issues:
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

For application issues:
- Check application logs
- Review Sentry error reports
- Contact development team

---

**Last Updated:** October 2, 2025
**Deployment Platform:** Railway
**Application:** Q.CELLS New Homes Solar Support Suite
