# 🍎 Mac Terminal Commands for Your Demo Setup

## Your Mac Paths
- Home: `/Users/guillaume_deramchi` (or `~`)
- Documents: `/Users/guillaume_deramchi/Documents`
- Bot repo: `/Users/guillaume_deramchi/Documents/hackathon_repo_aziz`
- Demo repo: Will be at `/Users/guillaume_deramchi/Documents/hackathonblackbox42`

---

## 🚀 Complete Setup - Copy & Paste These Commands

### Step 1: Clone Your Demo Repo

```bash
# Go to Documents folder
cd ~/Documents

# Clone your demo repo
git clone https://github.com/gderamchi/hackathonblackbox42.git

# Go into the demo repo
cd hackathonblackbox42

# Verify you're in the right place
pwd
# Should show: /Users/guillaume_deramchi/Documents/hackathonblackbox42
```

### Step 2: Copy All Bot Files from hackathon_repo_aziz

```bash
# Copy from the bot repo to your demo repo
cp -r ~/Documents/hackathon_repo_aziz/.github ~/Documents/hackathonblackbox42/
cp -r ~/Documents/hackathon_repo_aziz/src ~/Documents/hackathonblackbox42/
cp -r ~/Documents/hackathon_repo_aziz/config ~/Documents/hackathonblackbox42/
cp ~/Documents/hackathon_repo_aziz/requirements.txt ~/Documents/hackathonblackbox42/
cp ~/Documents/hackathon_repo_aziz/.pr-review-bot.json ~/Documents/hackathonblackbox42/
cp ~/Documents/hackathon_repo_aziz/README.md ~/Documents/hackathonblackbox42/
cp ~/Documents/hackathon_repo_aziz/.gitignore ~/Documents/hackathonblackbox42/

echo "✅ All bot files copied!"
```

### Step 3: Verify Files Were Copied

```bash
# Make sure you're in the demo repo
cd ~/Documents/hackathonblackbox42

# Check if files exist
ls -la .github/workflows/pr-review.yml
ls -la src/main.py
ls -la requirements.txt

# If you see the files, you're good!
echo "✅ Files verified!"
```

### Step 4: Create Demo Files with Issues

```bash
# Still in ~/Documents/hackathonblackbox42
mkdir -p examples

# Create Python demo file
cat > examples/demo_security.py << 'EOF'
"""Demo file with security issues"""

# SECURITY: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
DB_PASSWORD = "root123"

# SECURITY: SQL Injection
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)

# SECURITY: Command Injection
import os
def run_command(cmd):
    os.system(cmd)

# SECURITY: XSS Vulnerability
def render_html(user_input):
    return f"<div>{user_input}</div>"

# SECURITY: Weak Cryptography
import hashlib
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

# BUG: Division by zero
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# BUG: Null pointer
def process_user(user):
    print(user.name)
    return user.id

# BUG: Bare except
try:
    risky_operation()
except:
    pass

# BUG: Debugger left in code
import pdb
pdb.set_trace()

# BUG: Console output with sensitive data
print(f"Using password: {PASSWORD}")

# TODO: Fix all these security issues!
EOF

# Create JavaScript demo file
cat > examples/demo_quality.js << 'EOF'
/**
 * Demo file with code quality issues
 */

// SECURITY: Hardcoded credentials
const API_KEY = "sk-abcdef123456";
const SECRET = "my-secret-token";

// BUG: Using var instead of const/let
var oldStyle = "should use const or let";

// BUG: Using == instead of ===
function checkValue(value) {
    if (value == null) {
        return false;
    }
    return true;
}

// SECURITY: XSS vulnerability
function displayContent(userInput) {
    document.getElementById('content').innerHTML = userInput;
}

// SECURITY: Using eval
function executeCode(code) {
    eval(code);
}

// BUG: Console.log in production
console.log("Debug: API Key is", API_KEY);

// BUG: Debugger statement
function debugFunction() {
    debugger;
    return "debugging";
}

// BUG: Potential null access
function processUser(user) {
    console.log(user.name);
    return user.id;
}

// BUG: Array mutation
function sortArray(arr) {
    return arr.sort();
}

// TODO: Remove hardcoded credentials
// FIXME: Fix XSS vulnerability
// HACK: Temporary solution

module.exports = {
    checkValue,
    displayContent,
    executeCode
};
EOF

echo "✅ Demo files created!"
```

### Step 5: Commit Everything to Main Branch

```bash
# Make sure you're in the demo repo
cd ~/Documents/hackathonblackbox42

# Add all files
git add .

# Commit
git commit -m "Add PR Review Bot with demo files

Complete bot implementation:
- GitHub Actions workflow
- Blackbox API integration  
- Bug detection (15+ patterns)
- Security scanning (20+ patterns)
- Documentation linking
- PR summarization
- Demo files with intentional issues"

# Push to GitHub
git push origin main

echo "✅ Pushed to GitHub!"
```

### Step 6: Add API Key to GitHub (Do this in browser)

1. Open: https://github.com/gderamchi/hackathonblackbox42/settings/secrets/actions

2. Click: **"New repository secret"**

3. Enter:
   - **Name:** `BLACKBOX_API_KEY`
   - **Value:** `sk-zduYOC3n0GcsEQnyjNrnvg`

4. Click: **"Add secret"**

### Step 7: Enable GitHub Actions (Do this in browser)

1. Open: https://github.com/gderamchi/hackathonblackbox42/settings/actions

2. Under "Actions permissions":
   - Select: ✅ **"Allow all actions and reusable workflows"**

3. Under "Workflow permissions":
   - Select: ✅ **"Read and write permissions"**
   - Check: ✅ **"Allow GitHub Actions to create and approve pull requests"**

4. Click: **"Save"**

### Step 8: Create Test PR

```bash
# Make sure you're in the demo repo
cd ~/Documents/hackathonblackbox42

# Create a new branch
git checkout -b test-pr-bot

# The demo files are already there, so just commit them to this branch
git add examples/
git commit -m "Add demo files with intentional bugs and security issues

This PR tests the bot's detection capabilities:
- Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
- Common bugs (null checks, division by zero, debugger statements)
- Code quality issues (var vs const, console.log, etc.)

Expected: 20+ issues detected"

# Push the branch
git push origin test-pr-bot

# Create PR using GitHub CLI (if you have it)
gh pr create \
  --title "Test PR Review Bot" \
  --body "Testing the bot with intentional issues. Expected to detect 20+ problems."

# If you don't have gh CLI, just go to:
# https://github.com/gderamchi/hackathonblackbox42/compare
```

**Or create PR via browser:**
1. Go to: https://github.com/gderamchi/hackathonblackbox42
2. You'll see a banner "test-pr-bot had recent pushes"
3. Click "Compare & pull request"
4. Add title and description
5. Click "Create pull request"

---

## 🎉 What Happens Next

1. **Within 10 seconds:** GitHub Actions workflow starts
2. **Within 60 seconds:** Bot analyzes both demo files
3. **Bot posts:** 20+ inline comments on specific issues
4. **Bot generates:** Comprehensive PR summary

---

## 📊 Expected Results

### Python File (demo_security.py) - ~11 issues:
- Line 5: Hardcoded API key (Critical)
- Line 6: Hardcoded password (Critical)
- Line 7: Hardcoded DB password (Critical)
- Line 11: SQL injection (Critical)
- Line 17: Command injection (Critical)
- Line 22: XSS vulnerability (Critical)
- Line 27: Weak crypto MD5 (High)
- Line 31: Division by zero (Medium)
- Line 35: Null pointer (Medium)
- Line 40: Bare except (Medium)
- Line 45: Debugger statement (High)

### JavaScript File (demo_quality.js) - ~11 issues:
- Line 6: Hardcoded API key (Critical)
- Line 7: Hardcoded secret (Critical)
- Line 10: Using var (Low)
- Line 14: Using == (Medium)
- Line 22: XSS innerHTML (Critical)
- Line 27: eval() usage (Critical)
- Line 32: console.log (Info)
- Line 35: debugger statement (High)
- Line 42: Null access (Medium)
- Line 47: Array mutation (Info)
- Lines 52-54: TODO/FIXME/HACK (Info)

**Total: ~22 issues**

---

## 🔍 Verify Setup

Check if everything is in place:

```bash
cd ~/Documents/hackathonblackbox42

# Check structure
echo "Checking file structure..."
ls -la .github/workflows/pr-review.yml && echo "✅ Workflow exists"
ls -la src/main.py && echo "✅ Main bot exists"
ls -la requirements.txt && echo "✅ Requirements exists"
ls -la examples/demo_security.py && echo "✅ Python demo exists"
ls -la examples/demo_quality.js && echo "✅ JS demo exists"

echo ""
echo "✅ All files in place!"
echo ""
echo "Next steps:"
echo "1. Add API key to GitHub Secrets"
echo "2. Enable GitHub Actions"
echo "3. Create PR and watch the bot work!"
```

---

## 📞 Quick Reference

**Your Paths:**
- Bot repo: `~/Documents/hackathon_repo_aziz`
- Demo repo: `~/Documents/hackathonblackbox42`

**GitHub Links:**
- Repo: https://github.com/gderamchi/hackathonblackbox42
- Secrets: https://github.com/gderamchi/hackathonblackbox42/settings/secrets/actions
- Actions Settings: https://github.com/gderamchi/hackathonblackbox42/settings/actions
- Create PR: https://github.com/gderamchi/hackathonblackbox42/compare

**API Key:**
```
sk-zduYOC3n0GcsEQnyjNrnvg
```

---

## ✅ You're Ready!

Just copy and paste the commands above in your Mac terminal, and you'll have a working demo in 5 minutes! 🚀
