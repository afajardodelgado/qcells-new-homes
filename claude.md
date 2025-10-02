# Claude Development Guidelines - Q.CELLS New Homes Solar Support Suite

## Design Standards Reference

**IMPORTANT**: For ALL design-related work, refer to the **Q.CELLS Design Language Standards** documented in:

📄 **`qcells-design-standards.md`**

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
   - Step 3: `git push origin feature-name`
   - Step 4: `git checkout main`
   - Step 5: `git merge feature-name`
   - Step 6: `git push origin main`
   - Step 7: `git branch -d feature-name`
   - Step 8: `git push origin --delete feature-name`

**Command Reference (execute ONE at a time):**
```bash
# Step 1: Stage changes
git add .

# Step 2: Commit with message
git commit -m "descriptive message"

# Step 3: Push feature branch
git push origin feature-name

# Step 4: Switch to main
git checkout main

# Step 5: Merge feature branch
git merge feature-name

# Step 6: Push to main
git push origin main

# Step 7: Delete local branch
git branch -d feature-name

# Step 8: Delete remote branch
git push origin --delete feature-name
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
git push origin feature-name

# Command 4:
git checkout main

# Command 5:
git merge feature-name

# Command 6:
git push origin main

# Command 7:
git branch -d feature-name

# Command 8:
git push origin --delete feature-name
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
git push origin feature-name

# Merge and cleanup:
git checkout main
git merge feature-name
git push origin main
git branch -d feature-name
git push origin --delete feature-name
```

---

## Summary for LLMs

**When working on this project:**

1. 🚫 **NO EMOJIS IN UI/UX CODE** → Delete any emojis from user-facing code immediately
2. 📐 **Design changes?** → Check `qcells-design-standards.md` first
3. 🔧 **Code changes?** → Complete pre-push checklist
4. 🛑 **Wait for user signal** → Only run git commands when user says "OK let's merge" or similar
5. 🐌 **Execute git commands ONE AT A TIME** → Never batch git commands
6. 🚂 **Deployment?** → Ensure Railway compatibility
7. 🚫 **Never create Pull Requests** → Branch → Merge to main → Delete branches
8. ✅ **Always verify locally before pushing**
9. 🧹 **Keep it clean** → Always delete branches after merging

---

**Last Updated**: October 2, 2025
**Project**: Q.CELLS New Homes Solar Support Suite
**Deployment**: Railway
**Branch Strategy**: Feature branches → Merge to main → Delete branches (no PRs)
