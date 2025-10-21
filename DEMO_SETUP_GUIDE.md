# 🎬 Demo Setup Guide - Deploy to Any Repository

This guide shows you how to set up the PR Review Bot in a new repository for a great demo.

---

## 🚀 Quick Setup (5 Minutes)

### Option 1: Copy to New Repository (Recommended for Demo)

#### Step 1: Copy the Bot Files

Copy these files to your new repository:

```bash
# Essential files only
.github/workflows/pr-review.yml
src/
requirements.txt
.pr-review-bot.json
README.md
```

**Or use this command:**
```bash
# From this repo, copy to your new repo
NEW_REPO_PATH="/path/to/your/new/repo"

# Copy essential files
cp -r .github "$NEW_REPO_PATH/"
cp -r src "$NEW_REPO_PATH/"
cp -r config "$NEW_REPO_PATH/"
cp requirements.txt "$NEW_REPO_PATH/"
cp .pr-review-bot.json "$NEW_REPO_PATH/"
cp README.md "$NEW_REPO_PATH/"
```

#### Step 2: Add GitHub Secret

1. Go to your new repo: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`
2. Click **"New repository secret"**
3. Name: `BLACKBOX_API_KEY`
4. Value: `sk-zduYOC3n0GcsEQnyjNrnvg`
5. Click **"Add secret"**

#### Step 3: Enable GitHub Actions

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/actions`
2. Under "Actions permissions", select **"Allow all actions and reusable workflows"**
3. Under "Workflow permissions", select **"Read and write permissions"**
4. Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
5. Click **"Save"**

#### Step 4: Create a Test PR

```bash
cd /path/to/your/new/repo

# Create a test branch
git checkout -b test-pr-bot

# Create a file with intentional issues
cat > test_demo.py << 'EOF'
# Demo file with issues for PR bot

# Security issue: hardcoded password
password = "admin123"

# Bug: division by zero risk
def calculate(a, b):
    return a / b

# Security: SQL injection
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

# Bug: bare except
try:
    risky_operation()
except:
    pass

print("Debug output")  # Should be removed
EOF

# Commit and push
git add test_demo.py
git commit -m "Add test file for PR bot demo"
git push origin test-pr-bot

# Create PR (or use GitHub UI)
gh pr create --title "Test PR Bot Demo" --body "Testing the PR review bot"
```

#### Step 5: Watch the Magic! ✨

1. Go to your PR
2. Wait 30-60 seconds
3. See the bot post comments on issues
4. Check the comprehensive summary

---

## 🎯 Option 2: Use GitHub App (Advanced)

For a more permanent solution across multiple repos:

### Step 1: Create GitHub App

1. Go to: `https://github.com/settings/apps/new`
2. Fill in:
   - **Name**: `PR Review Bot`
   - **Homepage URL**: Your repo URL
   - **Webhook**: Uncheck "Active"
   - **Permissions**:
     - Repository permissions:
       - Contents: Read
       - Pull requests: Read & Write
       - Issues: Read & Write
   - **Subscribe to events**:
     - Pull request
     - Pull request review comment

3. Click **"Create GitHub App"**
4. Generate a private key and save it
5. Install the app on your repositories

### Step 2: Update Workflow

Replace the workflow with GitHub App authentication:

```yaml
name: PR Review Bot

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate token
        id: generate_token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.APP_PRIVATE_KEY }}
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run PR Review Bot
        env:
          BLACKBOX_API_KEY: ${{ secrets.BLACKBOX_API_KEY }}
          GITHUB_TOKEN: ${{ steps.generate_token.outputs.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO_NAME: ${{ github.repository }}
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: python src/main.py
```

---

## 🎨 Demo Scenarios

### Scenario 1: Security Vulnerabilities Demo

Create a PR with security issues:

```python
# demo_security.py

# Hardcoded credentials
API_KEY = "sk-1234567890"
PASSWORD = "admin123"

# SQL Injection
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute(query)

# Command Injection
import os
def run_command(cmd):
    os.system(cmd)

# XSS Vulnerability
def render_html(user_input):
    return f"<div>{user_input}</div>"

# Weak Crypto
import hashlib
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()
```

**Expected Bot Comments:**
- 🚨 5 Critical security issues
- CWE references
- Actionable fixes

### Scenario 2: Code Quality Demo

Create a PR with code quality issues:

```javascript
// demo_quality.js

// Using var instead of const/let
var oldStyle = "bad practice";

// Using == instead of ===
if (value == null) {
    console.log("found null");
}

// Console.log in production
console.log("Debug:", API_KEY);

// Debugger statement
debugger;

// TODO comments
// TODO: Fix this later
// FIXME: This is broken
```

**Expected Bot Comments:**
- ⚠️ 6 Code quality issues
- Best practice suggestions
- Modern alternatives

### Scenario 3: Bug Detection Demo

Create a PR with common bugs:

```python
# demo_bugs.py

# Division by zero
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# Null pointer
def process_user(user):
    print(user.name)
    return user.id

# Bare except
try:
    risky_operation()
except:
    pass

# File not closed
def read_file(path):
    f = open(path)
    return f.read()

# Infinite loop
while True:
    process()
```

**Expected Bot Comments:**
- 🐛 5 Bug detections
- Specific line numbers
- Code fix suggestions

---

## 📊 Demo Presentation Tips

### 1. Show the Workflow

```
1. Create PR with issues
   ↓
2. GitHub Actions triggers
   ↓
3. Bot analyzes code
   ↓
4. Posts inline comments
   ↓
5. Generates summary
```

### 2. Highlight Key Features

**Live Demo Script:**

1. **"Let me create a PR with some security issues..."**
   - Create PR with hardcoded password
   - Show GitHub Actions running

2. **"Within 30 seconds, the bot detects the issues..."**
   - Show inline comments appearing
   - Point out severity levels

3. **"It provides actionable suggestions..."**
   - Show code fix suggestions
   - Show CWE references

4. **"And generates a comprehensive summary..."**
   - Show PR summary comment
   - Show statistics

5. **"It works across multiple languages..."**
   - Show Python and JavaScript examples
   - Show consistent detection

### 3. Emphasize Innovation

- ✨ **AI-Powered**: Uses Blackbox API for advanced analysis
- 🔒 **Security-First**: CWE-compliant vulnerability detection
- 📚 **Educational**: Links to documentation and best practices
- 🚀 **Scalable**: Works across unlimited repositories
- ⚡ **Fast**: Results in under 60 seconds

---

## 🎥 Video Demo Script

### Opening (30 seconds)
"Today I'll show you an AI-powered PR review bot that automatically detects bugs and security vulnerabilities in your code."

### Setup (30 seconds)
"Setup is simple - just copy the workflow file and add your API key. Let me create a PR with some intentional issues..."

### Demo (2 minutes)
1. Create PR with issues
2. Show Actions tab running
3. Return to PR to see comments
4. Walk through 2-3 specific comments
5. Show the summary

### Features (1 minute)
- Multi-language support
- Security scanning with CWE references
- Bug detection
- Code quality suggestions
- Documentation linking

### Closing (30 seconds)
"The bot now automatically reviews all PRs, catching issues before they reach production. It's production-ready and open source!"

---

## 🔗 Quick Links for Demo

### Your Demo Repository
- **Settings**: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings`
- **Secrets**: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`
- **Actions**: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
- **New PR**: `https://github.com/YOUR_USERNAME/YOUR_REPO/compare`

### This Repository (Source)
- **Main Repo**: `https://github.com/Azizfassinou/Blackbox_AI_Hackathon`
- **Example PR**: `https://github.com/Azizfassinou/Blackbox_AI_Hackathon/pull/3`
- **Documentation**: See README.md

---

## 🎁 Demo Repository Template

Want a ready-to-go demo? Use this structure:

```
demo-pr-review-bot/
├── .github/
│   └── workflows/
│       └── pr-review.yml
├── src/
│   ├── main.py
│   ├── blackbox_client.py
│   ├── github_client.py
│   └── analyzers/
├── examples/
│   ├── security_issues.py
│   ├── code_quality.js
│   └── common_bugs.py
├── requirements.txt
├── .pr-review-bot.json
└── README.md
```

---

## 💡 Pro Tips

### For Best Demo Results:

1. **Use Real Code**: Show it working on actual project code
2. **Mix Severities**: Include critical, high, and low issues
3. **Show Summary**: The PR summary is impressive
4. **Highlight Speed**: Emphasize the 30-60 second turnaround
5. **Show Configurability**: Demonstrate the config file

### Common Demo Questions:

**Q: Does it work with private repos?**
A: Yes! Just add the secret to your private repo.

**Q: Can I customize the rules?**
A: Yes! Edit `.pr-review-bot.json` and `config/rules.json`

**Q: What languages are supported?**
A: Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C++, and more!

**Q: How much does it cost?**
A: The bot is free! You just need a Blackbox API key.

**Q: Can it auto-fix issues?**
A: Currently it suggests fixes. Auto-fix is a future feature!

---

## 🚀 Ready to Demo!

You now have everything you need to create an impressive demo:

✅ Setup instructions (5 minutes)
✅ Demo scenarios (security, quality, bugs)
✅ Presentation script
✅ Video demo outline
✅ Pro tips and FAQs

**Go create your demo and show off the bot!** 🎉

---

## 📞 Need Help?

- Check the main README.md
- Review example PR: https://github.com/Azizfassinou/Blackbox_AI_Hackathon/pull/3
- See test results in TEST_RESULTS.md

**Good luck with your demo!** 🌟
