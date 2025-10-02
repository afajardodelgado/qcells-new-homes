# Q.CELLS New Homes - Solar Support Suite

A comprehensive Salesforce integration platform for Q.CELLS New Homes solar sales and support operations. This application provides a secure JWT-based authentication proxy to Salesforce, along with a modern web interface following Q.CELLS design standards.

## 🏗️ Project Structure

```
cp-builder-installer/
├── server/
│   ├── __init__.py
│   └── main.py              # FastAPI backend with JWT auth
├── web/
│   ├── index.html           # SPA frontend
│   ├── styles.css           # Q.CELLS design system styles
│   └── app.js               # Frontend JavaScript
├── assets/
│   └── qcells-new-homes-navy-logo-scaled-1-2048x346.webp
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── qcells-design-standards.md  # Design language documentation
```

## 🔑 Key Features

### Backend (FastAPI + Salesforce JWT)
- **Secure Authentication**: JWT Bearer Flow for Salesforce authentication
- **API Endpoints**:
  - `GET /api/health` - Health check
  - `POST /api/sf/query` - Execute SOQL queries with optional tooling API support
  - `GET /api/sf/test` - Quick test endpoint with default query
- **Static File Serving**: Serves frontend and assets
- **CORS Support**: Configurable origins for development and production

### Frontend (Vanilla JS SPA)
- **Q.CELLS Design Language**: Implements official design standards
- **Full Sidebar Navigation**: 256px sidebar with section-based routing
- **Sections**: Homes, Pricing, Marketing, Training, Support
- **Salesforce Query Interface**: Interactive SOQL query builder
- **Responsive Grid**: 12-column desktop layout (min 1384px × 768px)
- **Pretendard Font**: Multilingual typography support

### Design System
- **Colors**: Primary (#00C6C1), Text (#0A0A0A), Muted (#8B8B8B)
- **Layout**: 60px GNB, 256px Full Sidebar, 24px margins
- **Typography**: Pretendard with standardized weights and sizes
- **Components**: Buttons, inputs, cards following Q.CELLS standards

## 🚀 Setup

### Prerequisites
- Python 3.10+
- Salesforce Connected App configured for JWT Bearer flow
- Private key file (RSA 2048-bit, PEM format)
- Salesforce user authorized for the Connected App

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/afajardodelgado/qcells-new-homes.git
cd qcells-new-homes
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your Salesforce credentials
```

**Environment Variables:**
```bash
SALESFORCE_LOGIN_URL=https://test.salesforce.com     # or https://login.salesforce.com for prod
SALESFORCE_CLIENT_ID=<Connected_App_Consumer_Key>
SALESFORCE_USERNAME=<your_salesforce_username>
SALESFORCE_JWT_KEY_PATH=/absolute/path/to/server.key
DEFAULT_TEST_SOQL=SELECT Id, Name FROM Account LIMIT 5
PORT=8000
CORS_ORIGINS=*  # Restrict to specific origins in production
```

5. **Generate JWT Key Pair** (if not already done)
```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate public certificate
openssl req -new -x509 -key server.key -out server.crt -days 365

# Upload server.crt to Salesforce Connected App
# Keep server.key secure and NEVER commit it to git
```

## 🏃 Running the Application

### Development
```bash
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the application at: `http://localhost:8000`

## 🧪 Testing

### API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Test Salesforce Connection:**
```bash
curl http://localhost:8000/api/sf/test
```

**Custom SOQL Query:**
```bash
curl -X POST http://localhost:8000/api/sf/query \
  -H 'Content-Type: application/json' \
  -d '{"soql": "SELECT Id, Name FROM Account LIMIT 5"}'
```

**Tooling API Query:**
```bash
curl -X POST http://localhost:8000/api/sf/query \
  -H 'Content-Type: application/json' \
  -d '{"soql": "SELECT Id, Name FROM ApexClass LIMIT 5", "tooling": true}'
```

## 🔒 Security Best Practices

1. **Never commit sensitive files:**
   - `.env` file
   - `server.key` private key
   - Any files containing credentials

2. **Production configuration:**
   - Use `https://login.salesforce.com` for production
   - Restrict `CORS_ORIGINS` to specific domains
   - Store private key outside repository
   - Use environment variable management (e.g., AWS Secrets Manager)

3. **Salesforce Connected App:**
   - Enable OAuth scopes: `api`, `refresh_token`, `offline_access`
   - Add permitted users in Connected App settings
   - Use IP restrictions if applicable

## 📁 API Reference

### `POST /api/sf/query`

Execute SOQL queries against Salesforce.

**Request Body:**
```json
{
  "soql": "SELECT Id, Name FROM Account LIMIT 5",
  "tooling": false  // Optional: set to true for Tooling API
}
```

**Response:**
```json
{
  "records": [...],
  "totalSize": 5,
  "done": true
}
```

### JWT Token Flow

The server automatically:
1. Creates JWT assertion with client credentials
2. Exchanges JWT for Salesforce access token
3. Uses access token for API requests
4. Tokens expire after 5 minutes (configurable in code)

## 🎨 Design System

This application follows the **Q.CELLS Design Language Standards**. See `qcells-design-standards.md` for complete specifications.

**Key Standards:**
- Desktop min: 1384px × 768px
- 12-column grid system
- 60px Global Navigation Bar
- 256px Full Sidebar Navigation
- Pretendard font family
- Primary color: #00C6C1

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.118+, Python 3.12
- **Authentication**: PyJWT 2.10+, Salesforce JWT Bearer Flow
- **Salesforce Client**: simple-salesforce 1.12+
- **Server**: Uvicorn with auto-reload
- **Frontend**: Vanilla JavaScript (ES6+), CSS3
- **Typography**: Pretendard (via CDN)

## 📝 Development Notes

### Code Structure

**server/main.py (server/main.py:1-133)**
- Lines 45-87: JWT token minting logic
- Lines 95-120: Salesforce query execution
- Lines 45-48: Static file mounting for SPA

**web/app.js (web/app.js:1-47)**
- Lines 12-21: SPA navigation logic
- Lines 27-44: Salesforce query handler with error handling

## 🤝 Contributing

1. Follow Q.CELLS design standards
2. Maintain code formatting and comments
3. Test all Salesforce integrations
4. Update documentation for new features

## 📄 License

Proprietary - Q.CELLS New Homes

## 🐛 Troubleshooting

**Authentication Errors:**
- Verify Connected App consumer key matches `SALESFORCE_CLIENT_ID`
- Ensure user is authorized in Connected App
- Check private key path and permissions
- Verify login URL (test vs prod)

**CORS Issues:**
- Update `CORS_ORIGINS` in `.env`
- Check browser console for specific errors

**Import Errors:**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

## 📞 Support

For Q.CELLS New Homes internal support, contact the development team.

---

**Built with ❤️ for Q.CELLS New Homes solar operations**
