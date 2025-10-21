# 🚀 Setup Guide for https://github.com/gderamchi/hackathonblackbox42

## Step-by-Step Setup (5 Minutes)

### Step 1: Clone Your Fresh Repo

```bash
cd ~
git clone https://github.com/gderamchi/hackathonblackbox42.git
cd hackathonblackbox42
```

### Step 2: Copy Bot Files from This Repo

```bash
# Run this from the hackathon_repo_aziz directory
cd /Users/guillaume_deramchi/Documents/hackathon_repo_aziz

# Copy all essential files to your new repo
cp -r .github ~/hackathonblackbox42/
cp -r src ~/hackathonblackbox42/
cp -r config ~/hackathonblackbox42/
cp requirements.txt ~/hackathonblackbox42/
cp .pr-review-bot.json ~/hackathonblackbox42/
cp README.md ~/hackathonblackbox42/
cp .gitignore ~/hackathonblackbox42/

# Create examples directory with demo files
mkdir -p ~/hackathonblackbox42/examples

# Copy demo files
cat > ~/hackathonblackbox42/examples/demo_security.py << 'EOF'
"""
Demo file with security issues for PR bot demonstration.
"""

# SECURITY ISSUE: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
DB_PASSWORD = "root123"

# SECURITY ISSUE: SQL Injection
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)

# SECURITY ISSUE: Command Injection
import os
def run_command(cmd):
    os.system(cmd)

# SECURITY ISSUE: XSS Vulnerability
def render_html(user_input):
    return f"<div>{user_input}</div>"

# SECURITY ISSUE: Weak Cryptography
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

# BUG: Console output
print(f"Using password: {PASSWORD}")

# TODO: Fix all these issues!
EOF

cat > ~/hackathonblackbox42/examples/demo_quality.js << 'EOF'
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

echo "✅ Files copied successfully!"
```

### Step 3: Commit and Push to Main Branch

```bash
cd ~/hackathonblackbox42

git add .
git commit -m "Add PR Review Bot with demo files"
git push origin main
```

### Step 4: Add API Key to GitHub Secrets

1. Go to: https://github.com/gderamchi/hackathonblackbox42/settings/secrets/actions

2. Click **"New repository secret"**

3. Enter:
   - **Name:** `BLACKBOX_API_KEY`
   - **Value:** `sk-zduYOC3n0GcsEQnyjNrnvg`

4. Click **"Add secret"**

### Step 5: Enable GitHub Actions Permissions

1. Go to: https://github.com/gderamchi/hackathonblackbox42/settings/actions

2. Under **"Actions permissions"**:
   - Select ✅ **"Allow all actions and reusable workflows"**

3. Under **"Workflow permissions"**:
   - Select ✅ **"Read and write permissions"**
   - Check ✅ **"Allow GitHub Actions to create and approve pull requests"**

4. Click **"Save"**

### Step 6: Create a Test PR

```bash
cd ~/hackathonblackbox42

# Create a new branch
git checkout -b test-pr-bot

# Add the demo files (they should already be there from step 2)
git add examples/
git commit -m "Add demo files with intentional issues for bot testing"
git push origin test-pr-bot

# Create PR using GitHub CLI (or use the web interface)
gh pr create \
  --title "Test PR Review Bot" \
  --body "This PR contains intentional bugs and security issues to test the bot's detection capabilities.

Expected detections:
- 🚨 5+ critical security issues
- ⚠️ 3+ high severity bugs  
- ⚡ 4+ medium issues
- ℹ️ 3+ info/suggestions

The bot should post inline comments and a comprehensive summary within 60 seconds."
```

**Or create PR via web:**
1. Go to: https://github.com/gderamchi/hackathonblackbox42
2. Click "Compare & pull request"
3. Add title and description
4. Click "Create pull request"

### Step 7: Watch the Bot Work! 🎉

1. Go to your PR: https://github.com/gderamchi/hackathonblackbox42/pulls

2. Click on the **"Actions"** tab to see the workflow running

3. Wait 30-60 seconds

4. Return to the PR to see:
   - ✅ 20+ inline comments on specific issues
   - ✅ Comprehensive summary comment
   - ✅ Severity classifications
   - ✅ Actionable suggestions

---

## 🎯 What to Expect

### The Bot Will Detect:

**Python File (demo_security.py):**
- 🚨 3 hardcoded credentials (critical)
- 🚨 1 SQL injection (critical)
- 🚨 1 command injection (critical)
- 🚨 1 XSS vulnerability (critical)
- ⚠️ 1 weak crypto - MD5 (high)
- 🐛 3 common bugs (medium/low)
- ℹ️ 1 TODO comment (info)

**JavaScript File (demo_quality.js):**
- 🚨 2 hardcoded credentials (critical)
- 🚨 1 XSS vulnerability (critical)
- 🚨 1 eval() usage (critical)
- ⚠️ 4 code quality issues (medium)
- 🐛 3 common bugs (low)
- ℹ️ 3 TODO/FIXME comments (info)

**Total: ~22 issues detected**

---

## 📊 Example Comment Format

You'll see comments like this:

```markdown
🔒 **Security** 🚨 *Critical Severity*

Hardcoded password detected

**Code:**
```python
PASSWORD = "admin123"
```

**💡 Suggestion:**
Use environment variables for passwords:
```python
PASSWORD = os.getenv('PASSWORD')
```

**🔗 Reference:** [CWE-798](https://cwe.mitre.org/data/definitions/798.html)

---
*🤖 Generated by Blackbox AI PR Review Bot*
```

---

## 🎬 Demo Presentation Flow

### 1. Show the Setup (30 seconds)
"I've set up the bot in this fresh repository. It took just 5 minutes to copy files and configure."

### 2. Show the PR (30 seconds)
"I created a PR with intentional issues - hardcoded passwords, SQL injection, XSS vulnerabilities, and common bugs."

### 3. Show Actions Running (15 seconds)
"The bot automatically triggers on PR creation. Let's check the Actions tab..."

### 4. Show the Results (2 minutes)
"Within 60 seconds, the bot has analyzed the code and posted 22 comments. Let me walk through a few..."

**Pick 2-3 interesting issues:**
- Show a critical security issue (hardcoded password)
- Show a bug detection (division by zero)
- Show a code quality suggestion (var vs const)

### 5. Show the Summary (30 seconds)
"The bot also generates a comprehensive summary with statistics, severity breakdown, and recommendations."

### 6. Highlight Features (30 seconds)
- Multi-language support
- CWE-compliant security scanning
- Actionable suggestions with code examples
- Documentation linking
- Works across unlimited repositories

---

## 🎊 Success Checklist

After following these steps, you should have:

- ✅ Bot files in your repo
- ✅ API key configured in GitHub Secrets
- ✅ GitHub Actions enabled with proper permissions
- ✅ Demo files with intentional issues
- ✅ Test PR created
- ✅ Bot running and posting comments
- ✅ Comprehensive summary generated

---

## 🔧 Troubleshooting

### If the bot doesn't run:

1. **Check Actions tab**: https://github.com/gderamchi/hackathonblackbox42/actions
   - Is the workflow running?
   - Any error messages?

2. **Check Secrets**: https://github.com/gderamchi/hackathonblackbox42/settings/secrets/actions
   - Is `BLACKBOX_API_KEY` set?

3. **Check Permissions**: https://github.com/gderamchi/hackathonblackbox42/settings/actions
   - Are workflows allowed?
   - Are write permissions enabled?

### If you see errors:

- **"API key not found"**: Add the secret in Step 4
- **"Permission denied"**: Enable permissions in Step 5
- **"Workflow not found"**: Make sure `.github/workflows/pr-review.yml` exists

---

## 📞 Quick Links

- **Your Repo**: https://github.com/gderamchi/hackathonblackbox42
- **Settings**: https://github.com/gderamchi/hackathonblackbox42/settings
- **Secrets**: https://github.com/gderamchi/hackathonblackbox42/settings/secrets/actions
- **Actions**: https://github.com/gderamchi/hackathonblackbox42/actions
- **Pull Requests**: https://github.com/gderamchi/hackathonblackbox42/pulls

---

## 🚀 You're All Set!

Follow the steps above and you'll have a working demo in 5 minutes!

The bot will automatically review all future PRs in this repository. 🎉
