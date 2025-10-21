#!/bin/bash

# Quick Demo Setup Script for PR Review Bot
# This script helps you set up the bot in a new repository for demo purposes

set -e

echo "🎬 PR Review Bot - Quick Demo Setup"
echo "===================================="
echo ""

# Check if target directory is provided
if [ -z "$1" ]; then
    echo "Usage: ./QUICK_DEMO_SCRIPT.sh /path/to/your/demo/repo"
    echo ""
    echo "Example: ./QUICK_DEMO_SCRIPT.sh ~/projects/my-demo-repo"
    exit 1
fi

TARGET_REPO="$1"

# Check if target directory exists
if [ ! -d "$TARGET_REPO" ]; then
    echo "❌ Error: Directory $TARGET_REPO does not exist"
    echo ""
    echo "Create it first with: mkdir -p $TARGET_REPO && cd $TARGET_REPO && git init"
    exit 1
fi

echo "📁 Target repository: $TARGET_REPO"
echo ""

# Copy essential files
echo "📦 Copying bot files..."

# Create directories
mkdir -p "$TARGET_REPO/.github/workflows"
mkdir -p "$TARGET_REPO/src/analyzers"
mkdir -p "$TARGET_REPO/src/utils"
mkdir -p "$TARGET_REPO/config"
mkdir -p "$TARGET_REPO/examples"

# Copy workflow
cp .github/workflows/pr-review.yml "$TARGET_REPO/.github/workflows/"
echo "  ✅ Copied workflow file"

# Copy source files
cp -r src/* "$TARGET_REPO/src/"
echo "  ✅ Copied source files"

# Copy config
cp .pr-review-bot.json "$TARGET_REPO/"
cp config/rules.json "$TARGET_REPO/config/" 2>/dev/null || true
echo "  ✅ Copied configuration"

# Copy requirements
cp requirements.txt "$TARGET_REPO/"
echo "  ✅ Copied requirements.txt"

# Copy README
cp README.md "$TARGET_REPO/"
echo "  ✅ Copied README.md"

# Create demo files
echo ""
echo "📝 Creating demo files with intentional issues..."

# Python demo file
cat > "$TARGET_REPO/examples/demo_security.py" << 'EOF'
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

echo "  ✅ Created examples/demo_security.py"

# JavaScript demo file
cat > "$TARGET_REPO/examples/demo_quality.js" << 'EOF'
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

echo "  ✅ Created examples/demo_quality.js"

# Create a simple README for the demo
cat > "$TARGET_REPO/DEMO_README.md" << 'EOF'
# PR Review Bot Demo

This repository demonstrates the PR Review Bot in action.

## Quick Test

1. Make sure you've added `BLACKBOX_API_KEY` to GitHub Secrets
2. Create a PR with the demo files
3. Watch the bot analyze and comment!

## Demo Files

- `examples/demo_security.py` - Security vulnerabilities (10+ issues)
- `examples/demo_quality.js` - Code quality issues (12+ issues)

## Expected Results

The bot will detect:
- 🚨 Critical security issues (hardcoded credentials, SQL injection, etc.)
- ⚠️ High severity bugs (null pointers, division by zero, etc.)
- ⚡ Medium issues (code quality, best practices)
- ℹ️ Low/info issues (TODO comments, console.log, etc.)

## Next Steps

1. Review the bot's comments
2. Check the PR summary
3. See how it helps improve code quality!
EOF

echo "  ✅ Created DEMO_README.md"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Go to your demo repository:"
echo "   cd $TARGET_REPO"
echo ""
echo "2. Commit the files:"
echo "   git add ."
echo "   git commit -m 'Add PR Review Bot'"
echo "   git push origin main"
echo ""
echo "3. Add GitHub Secret:"
echo "   Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions"
echo "   Name: BLACKBOX_API_KEY"
echo "   Value: sk-zduYOC3n0GcsEQnyjNrnvg"
echo ""
echo "4. Enable GitHub Actions:"
echo "   Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/actions"
echo "   - Allow all actions"
echo "   - Read and write permissions"
echo "   - Allow creating PRs"
echo ""
echo "5. Create a test PR:"
echo "   git checkout -b demo-pr"
echo "   git add examples/"
echo "   git commit -m 'Add demo files with issues'"
echo "   git push origin demo-pr"
echo "   gh pr create --title 'Demo PR' --body 'Testing the bot'"
echo ""
echo "6. Watch the bot work! 🎉"
echo "   The bot will post 20+ comments within 60 seconds"
echo ""
echo "🎬 Your demo is ready!"
