# Claude Development Guidelines - Q.CELLS New Homes Solar Support Suite

## Project Structure

This project follows a clean, organized structure. **ALWAYS maintain this organization when adding new files.**

### Root Directory (Core Files Only)
```
/
├── README.md               # Main project documentation
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies (Playwright E2E tests)
├── .env.example           # Environment variable template
├── .gitignore            # Git ignore rules
├── railway.toml           # Railway deployment config (MUST be in root)
├── nixpacks.toml          # Nixpacks build config (MUST be in root)
├── server/               # Backend Python/FastAPI code
├── web/                  # Frontend HTML/CSS/JavaScript
├── assets/               # Static assets (images, fonts, etc.)
├── tests/                # All test files (unit & E2E)
├── config/               # Configuration files (see below)
└── docs/                 # All documentation (see below)
```

**IMPORTANT:** Never create files in the root directory except for the files listed above. Use the appropriate subdirectory.

**EXCEPTION:** `railway.toml` and `nixpacks.toml` MUST remain in root - Railway platform requires them there.

### `/config` - Configuration Files

**Purpose:** Configuration files for test tools and other utilities.

**Allowed files:**
- `playwright.config.js` - Playwright E2E test configuration
- `pytest.ini` - Pytest unit test configuration
- Other tool configs (eslint, prettier, etc.)

**Rules:**
- Test config files belong here
- If adding a new tool (linter, formatter, etc.), put its config here
- **EXCEPTION:** `railway.toml` and `nixpacks.toml` MUST stay in root (Railway requirement)

### `/docs` - Documentation

**Purpose:** All documentation files for developers, deployment, design standards, and guidelines.

**Allowed files:**
- `CLAUDE_GUIDELINES.md` - This file (LLM development guidelines)
- `DESIGN_STANDARDS.md` - Q.CELLS design language standards
- `DEPLOYMENT.md` - Railway deployment guide
- Any new documentation files (use UPPERCASE names with .md extension)

**Rules:**
- All `.md` files except README.md belong here
- Use descriptive UPPERCASE names (e.g., `API_REFERENCE.md`, `CONTRIBUTING.md`)
- Never create documentation files in root directory

### `/server` - Backend Code

**Purpose:** Python/FastAPI backend application code.

**Structure:**
```
server/
├── __init__.py
└── main.py              # Main FastAPI application
```

**Rules:**
- All Python backend code belongs here
- Keep modular - split into multiple files as needed (e.g., `routes.py`, `models.py`, `utils.py`)
- No test files here (tests go in `/tests`)

### `/web` - Frontend Code

**Purpose:** Frontend HTML, CSS, and JavaScript files.

**Structure:**
```
web/
├── index.html           # Main HTML file
├── styles.css           # Stylesheet
└── app.js               # JavaScript application logic
```

**Rules:**
- All frontend code belongs here
- Split CSS/JS into multiple files as needed
- No emojis in any UI-facing code
- Follow Q.CELLS design standards (see `docs/DESIGN_STANDARDS.md`)

### `/assets` - Static Assets

**Purpose:** Images, fonts, logos, and other static files served by the application.

**Structure:**
```
assets/
├── qcells-new-homes-navy-logo-scaled-1-2048x346.webp
└── [other images, icons, fonts, etc.]
```

**Rules:**
- Only static files (images, fonts, PDFs, etc.)
- No code files
- Optimize images before adding

### `/tests` - Test Files

**Purpose:** All test files (unit tests, E2E tests, integration tests).

**Structure:**
```
tests/
├── __init__.py
├── test_api.py          # Pytest unit tests
└── e2e/
    └── navigation.spec.js  # Playwright E2E tests
```

**Rules:**
- All test files belong here
- Unit tests: `test_*.py` in root of `/tests`
- E2E tests: `*.spec.js` in `/tests/e2e/`
- No production code in this directory

---

## Design Standards Reference

**IMPORTANT**: For ALL design-related work, refer to the **Q.CELLS Design Language Standards** documented in:

📄 **`docs/DESIGN_STANDARDS.md`**

This file contains comprehensive specifications for:
- Grid and Layout (Desktop & Mobile)
- Typography (Pretendard font family)
- Components (Buttons, Inputs, Navigation, etc.)
- Colors and spacing
- Common micro-experiences (Login, Sign Up, etc.)

**Before implementing any UI/UX features, LLMs MUST review the design standards file to ensure compliance.**

### 🚫 CRITICAL RULE: NO EMOJIS IN APPLICATION

**NEVER use emojis in any UI/UX-facing code:**
- ❌ No emojis in HTML
- ❌ No emojis in JavaScript strings shown to users
- ❌ No emojis in CSS content
- ❌ No emojis in user-facing text
- ❌ No emojis in buttons, labels, headings, or any visible content
- ✅ Emojis are ONLY allowed in: code comments, commit messages, and this documentation file

**If you see emojis in any UI/UX code, DELETE them immediately.**

---

## Git Workflow - Branch, Merge, and Clean Protocol

**⚠️ NO PULL REQUESTS**

This project operates with a **branch → merge to main → delete branch** workflow. There is no code review process via Pull Requests at this stage.

### 🔴 IMPORTANT: When to Trigger Git Workflow

**DO NOT** automatically run git commands. **ONLY** execute the git workflow when the user explicitly indicates we're at a good stopping point, such as:
- "OK we are at a good checkpoint"
- "OK let's merge"
- "Let's commit this"
- "Push this up"
- Any similar phrase indicating it's time to commit and merge

### 🔴 IMPORTANT: Execute Git Commands ONE AT A TIME

**NEVER** run multiple git commands in a single batch. Execute **ONE command at a time** and wait for confirmation before proceeding to the next. This allows for:
- Verification at each step
- Error handling between commands
- User visibility into the process
- Ability to stop if issues arise

### Standard Git Workflow

When working on new features or changes:

1. **Create feature branch**: `git checkout -b feature-name`
2. **Make changes and commit**: Work on your feature branch
3. **WAIT for user signal** (e.g., "OK let's merge", "good checkpoint")
4. **Pre-push checklist** (see below) - Complete ALL checks
5. **Execute git commands ONE AT A TIME:**
   - Step 1: `git add .`
   - Step 2: `git commit -m "descriptive message"`
   - Step 3: `git checkout main`
   - Step 4: `git merge feature-name`
   - Step 5: `git push origin main`
   - Step 6: `git branch -d feature-name`

**Command Reference (execute ONE at a time):**
```bash
# Step 1: Stage changes
git add .

# Step 2: Commit with message
git commit -m "descriptive message"

# Step 3: Switch to main
git checkout main

# Step 4: Merge feature branch
git merge feature-name

# Step 5: Push to main
git push origin main

# Step 6: Delete local branch
git branch -d feature-name
```

**Never create Pull Requests.** All code goes directly to main after local verification and branch cleanup.

---

## Pre-Push Checklist ✅

Before running git commands to push to origin, **ALWAYS** complete this checklist:

### 1. Kill Existing Application (if running)
```bash
# Find the process
ps aux | grep uvicorn

# Kill it
kill -9 <PID>
# OR use pkill
pkill -f uvicorn
```

### 2. Run Application Locally
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Start the application
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Verify Build Success
- ✅ Application starts without errors
- ✅ Navigate to `http://localhost:8000` in browser
- ✅ Test critical endpoints:
  - `GET /api/health` - Health check
  - `GET /api/sf/test` - Salesforce connection test
- ✅ Verify UI loads correctly
- ✅ Check browser console for JavaScript errors
- ✅ Test navigation between sections

### 4. Only After All Checks Pass - Wait for User Signal

**STOP HERE.** Do not proceed with git commands until the user explicitly says:
- "OK we are at a good checkpoint"
- "OK let's merge"
- "Let's commit this"
- Or any similar indication

### 5. Execute Git Workflow ONE COMMAND AT A TIME

Once user signals, execute each command individually:

```bash
# Command 1:
git add .

# Command 2:
git commit -m "descriptive commit message"

# Command 3:
git checkout main

# Command 4:
git merge feature-name

# Command 5:
git push origin main

# Command 6:
git branch -d feature-name
```

**If any step fails, STOP and FIX IT before continuing. Keep branches clean by always deleting after merge.**

---

## Railway Deployment Compatibility 🚂

This application is deployed on **Railway**. Ensure all code changes are Railway-compatible:

### Required Files for Railway

1. **`requirements.txt`** - Must be present and up-to-date
   ```bash
   # Update if new dependencies added
   pip freeze > requirements.txt
   ```

2. **Environment Variables** - Set in Railway dashboard:
   - `SALESFORCE_LOGIN_URL`
   - `SALESFORCE_CLIENT_ID`
   - `SALESFORCE_USERNAME`
   - `SALESFORCE_JWT_KEY_PATH`
   - `DEFAULT_TEST_SOQL`
   - `PORT` (Railway will auto-assign)
   - `CORS_ORIGINS`

3. **Port Binding** - Application MUST bind to `0.0.0.0`:
   ```python
   # server/main.py should use:
   # uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
   ```

### Railway-Specific Considerations

- **Static Files**: Ensure `web/` directory is properly served
- **No Build Step**: Python dependencies install automatically from `requirements.txt`
- **Environment Variables**: Never hardcode credentials; use Railway env vars
- **Logging**: Use `print()` or proper logging for Railway logs
- **Health Checks**: `/api/health` endpoint is critical for Railway monitoring

### Testing Railway Compatibility Locally

```bash
# Simulate Railway environment
export PORT=8000
export SALESFORCE_LOGIN_URL="your_value"
export SALESFORCE_CLIENT_ID="your_value"
# ... set other env vars

# Run application
python3 -m uvicorn server.main:app --host 0.0.0.0 --port $PORT
```

---

## Development Best Practices

### Code Organization
- Backend logic: `server/main.py`
- Frontend: `web/` directory (HTML, CSS, JS)
- Assets: `assets/` directory
- Design specs: `qcells-design-standards.md`

### Before Any Commit
1. ✅ Kill and restart local application
2. ✅ Verify build success
3. ✅ Test functionality
4. ✅ Check Railway compatibility
5. ✅ Review design standards compliance (if UI changes)
6. ✅ Commit on feature branch
7. ✅ Push feature branch → Merge to main → Delete branches

### Common Commands Reference

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

# Check running processes
ps aux | grep uvicorn

# Kill existing process
pkill -f uvicorn

# Complete git workflow (after checklist)
# On feature branch:
git add .
git commit -m "message"

# Merge and cleanup:
git checkout main
git merge feature-name
git push origin main
git branch -d feature-name
```

---

## File Organization Rules

### When Creating New Files:

1. **Backend code?** → Add to `/server/`
2. **Frontend code?** → Add to `/web/`
3. **Images/assets?** → Add to `/assets/`
4. **Tests?** → Add to `/tests/` (unit) or `/tests/e2e/` (E2E)
5. **Config files?** → Add to `/config/`
6. **Documentation?** → Add to `/docs/` with UPPERCASE name

### What NOT to Do:

❌ Never create `.md` files in root (except README.md)
❌ Never create config files in root
❌ Never mix test files with production code
❌ Never create random files in root directory

### Quick Reference:

| File Type | Location | Example |
|-----------|----------|---------|
| Python backend | `/server/` | `server/routes.py` |
| HTML/CSS/JS | `/web/` | `web/components.js` |
| Images/logos | `/assets/` | `assets/icon.svg` |
| Unit tests | `/tests/` | `tests/test_routes.py` |
| E2E tests | `/tests/e2e/` | `tests/e2e/login.spec.js` |
| Config files | `/config/` | `config/eslint.config.js` |
| Documentation | `/docs/` | `docs/API_REFERENCE.md` |

---

## Code Pattern Consistency

**CRITICAL: Always examine existing code patterns before implementing new features.**

When the user provides code examples or requests new functionality:

### ❌ DON'T:
- Implement provided code verbatim without examining the codebase
- Introduce new dependencies without checking if existing patterns solve the problem
- Assume the user's code example is the best approach for this codebase

### ✅ DO:
1. **Search for similar implementations** in the codebase first
2. **Identify existing patterns** (e.g., how other endpoints are structured)
3. **Follow established conventions** (e.g., direct SOQL queries vs. pandas DataFrames)
4. **Question unnecessary dependencies** - If Builders and Communities work without pandas, why would Homes need it?
5. **Adapt the user's request** to match the codebase's established patterns

### Example:
**User Request**: "Add Homes endpoint using this pandas code..."

**Wrong Approach**: Copy-paste the pandas code → Add pandas dependency → Create inconsistent endpoint

**Right Approach**:
1. Check how `/api/sf/builders` and `/api/sf/communities` work
2. Notice they use direct SOQL + simple record processing
3. Adapt the user's data requirements to match the existing pattern
4. Result: Consistent, dependency-free implementation

**Remember**: User-provided code examples show *what data they want*, not necessarily *how to implement it* in this specific codebase.

---

## Common Pitfalls & Debugging

### API Endpoint Pattern Consistency

**Issue**: "Unexpected token 'I', 'Internal S'... is not valid JSON" error

**Root Cause**: When a backend endpoint has a Python error (like calling an undefined function), it returns an HTML error page or plain text error message instead of JSON. The frontend tries to parse this as JSON and fails.

**Example Problem** (October 6, 2025):
```python
@app.get("/api/sf/homes")
def get_homes():
    sf = get_salesforce()  # ❌ Undefined function - causes 500 error
    # ... rest of endpoint
```

**Symptoms**:
- Frontend shows: `Error: Unexpected token 'I', "Internal S"... is not valid JSON`
- Backend returns plain text error instead of JSON
- Browser console shows the error when calling the API endpoint

**Solution**: Follow the established authentication pattern used in ALL other endpoints:
```python
@app.get("/api/sf/homes")
def get_homes():
    # ✅ Standard pattern from /api/sf/builders, /api/sf/communities, etc.
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

    sf = Salesforce(instance_url=auth["instance_url"], session_id=auth["access_token"])
    # ... rest of endpoint
```

**Lesson**: When adding new API endpoints:
1. **Copy from existing endpoints** - Don't invent new patterns
2. **Check for undefined functions** - If calling a helper function, make sure it exists
3. **Test the endpoint** - Always test API endpoints in browser/Postman before considering it complete
4. **Follow the pattern** - All `/api/sf/*` endpoints use the same auth flow

**Debugging Strategy**:
- JSON parse errors in frontend → Check backend response (could be HTML error page)
- "Internal Server Error" → Check backend logs for Python exceptions
- Undefined function errors → Search codebase to verify function exists before calling it

---

## Summary for LLMs

**When working on this project:**

1. 📁 **File organization** → Always use correct directory structure (see above)
2. 🚫 **NO EMOJIS IN UI/UX CODE** → Delete any emojis from user-facing code immediately
3. 📐 **Design changes?** → Check `docs/DESIGN_STANDARDS.md` first
4. 🔍 **New features?** → Examine existing patterns before implementing
5. 🔧 **Code changes?** → Complete pre-push checklist
6. 🛑 **Wait for user signal** → Only run git commands when user says "OK let's merge" or similar
7. 🐌 **Execute git commands ONE AT A TIME** → Never batch git commands
8. 🚂 **Deployment?** → Ensure Railway compatibility
9. 🚫 **Never create Pull Requests** → Branch → Merge to main → Delete branches
10. ✅ **Always verify locally before pushing**
11. 🧹 **Keep it clean** → Always delete branches after merging

---

## UI/UX Pattern: Accordion Layout

### Overview
The accordion layout pattern is used for master-detail views where clicking a table row expands a detail panel to the right while compressing the main table to the left.

### Implementation Pattern

**HTML Structure:**
```html
<section id="section-name" class="section visible">
  <div class="accordion-layout" id="layoutId">
    <!-- Master view (table) -->
    <div class="card master-card">
      <div id="tableContainer"></div>
    </div>
    
    <!-- Detail panel (hidden by default) -->
    <div class="card detail-card" id="detailPanel">
      <div id="detailContent"></div>
    </div>
  </div>
</section>
```

**CSS Requirements:**
```css
/* Default: Full-width master view */
.accordion-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  transition: grid-template-columns 0.3s ease;
  flex: 1;
  min-height: 0;
}

/* Split view: 50/50 layout */
.accordion-layout.split-view {
  grid-template-columns: 1fr 1fr;
}

/* Master and detail cards */
.master-card,
.detail-card {
  min-width: 0;
  min-height: 0;
  transition: opacity 0.3s ease;
  display: flex;
  flex-direction: column;
}

/* Detail card hidden by default */
.detail-card {
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease 0.2s;
}

/* Show detail card in split view */
.accordion-layout.split-view .detail-card {
  opacity: 1;
}

/* Adjust table sizing in split view */
.accordion-layout.split-view .master-table td {
  max-width: 150px;
  font-size: 13px;
}

.accordion-layout.split-view .master-table th {
  font-size: 10px;
  padding: 8px 10px;
}
```

**JavaScript Pattern:**
```javascript
// Get layout container
const layoutContainer = document.getElementById('layoutId');

// When clicking a row
async function selectItem(itemId) {
  selectedItemId = itemId;
  
  // Show split view
  layoutContainer.classList.add('split-view');
  
  // Re-render table to show selected state
  renderTable(currentData);
  
  // Load detail data
  const detailData = await fetchDetailData(itemId);
  renderDetailPanel(detailData);
}

// Close detail panel
function closeDetail() {
  selectedItemId = null;
  layoutContainer.classList.remove('split-view');
  renderTable(currentData);
}

// Make functions globally available
window.selectItem = selectItem;
window.closeDetail = closeDetail;
```

**Detail Panel Header Pattern:**
```javascript
builderInfoDiv.innerHTML = `
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
    <h3 style="margin: 0;">Detail Title</h3>
    <button onclick="closeDetail()" class="btn" style="padding: 4px 12px; font-size: 12px;">✕ Close</button>
  </div>
  <!-- Detail content here -->
`;
```

### Key Features

1. **Smooth Transitions**: CSS transitions for grid layout and opacity changes
2. **Responsive Columns**: Table columns shrink in split view
3. **Selected State**: Row highlighting persists through sorting/filtering
4. **Close Button**: Always provide a way to collapse back to full view
5. **Flexible Content**: Detail panel can contain any content structure

### Design Principles

- **Default state**: Full-width master view maximizes data visibility
- **Split view**: 50/50 split for balanced master-detail layout
- **Animations**: 300ms transitions for smooth user experience
- **Mobile**: Consider full-screen detail overlay on smaller screens

### Common Use Cases

- **Builders → Divisions**: Show builder list, expand to see divisions
- **Communities → Homes**: Show community list, expand to see homes
- **Projects → Details**: Show project list, expand to see project details

---

**Last Updated**: October 6, 2025
**Project**: Q.CELLS New Homes Solar Support Suite
**Deployment**: Railway
**Branch Strategy**: Feature branches → Merge to main → Delete branches (no PRs)
