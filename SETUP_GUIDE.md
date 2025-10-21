# 🚀 Setup Guide - Blackbox AI PR Review Bot

This guide will walk you through setting up the PR Review Bot in your repository.

## Prerequisites

- GitHub repository with admin access
- Blackbox API key
- Basic understanding of GitHub Actions

## 📋 Step-by-Step Setup

### Step 1: Get Your Blackbox API Key

1. Visit [Blackbox AI](https://www.blackbox.ai/)
2. Sign up or log in to your account
3. Navigate to API settings
4. Generate a new API key
5. Copy the key (starts with `sk-`)

### Step 2: Add the Bot to Your Repository

#### Option A: Copy Files Directly

1. **Copy the workflow file:**
   ```bash
   mkdir -p .github/workflows
   cp pr-review-bot/.github/workflows/pr-review.yml .github/workflows/
   ```

2. **Copy the source code:**
   ```bash
   mkdir -p pr-review-bot
   cp -r pr-review-bot/src pr-review-bot/
   cp pr-review-bot/requirements.txt pr-review-bot/
   ```

3. **Copy configuration (optional):**
   ```bash
   cp pr-review-bot/.pr-review-bot.json .
   ```

#### Option B: Use as Submodule

```bash
git submodule add https://github.com/yourusername/pr-review-bot.git
```

### Step 3: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - **Name:** `BLACKBOX_API_KEY`
   - **Value:** Your Blackbox API key (e.g., `sk-zduYOC3n0GcsEQnyjNrnvg`)

> **Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions

### Step 4: Adjust Workflow Permissions

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Check **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### Step 5: Customize Configuration (Optional)

Create a `.pr-review-bot.json` file in your repository root:

```json
{
  "enabled": true,
  "auto_comment": true,
  "severity_threshold": "low",
  "ignore_patterns": [
    "*.md",
    "*.txt",
    "package-lock.json",
    "yarn.lock"
  ],
  "features": {
    "bug_detection": true,
    "security_scan": true,
    "doc_linking": true,
    "summarization": true
  },
  "max_comments": 50
}
```

### Step 6: Test the Bot

1. Create a test branch:
   ```bash
   git checkout -b test-pr-bot
   ```

2. Make a simple change:
   ```bash
   echo "# Test" >> test.py
   git add test.py
   git commit -m "Test PR review bot"
   git push origin test-pr-bot
   ```

3. Create a Pull Request on GitHub

4. Wait for the bot to analyze (usually 1-2 minutes)

5. Check for:
   - ✅ Bot comments on the PR
   - ✅ Summary comment
   - ✅ Inline code comments (if issues found)

## 🔧 Advanced Configuration

### Custom Rules

Edit `config/rules.json` to add custom detection patterns:

```json
{
  "bug_patterns": [
    {
      "pattern": "your_regex_pattern",
      "message": "Issue description",
      "severity": "high",
      "language": "python"
    }
  ]
}
```

### Ignore Specific Files

Add patterns to `.pr-review-bot.json`:

```json
{
  "ignore_patterns": [
    "vendor/**",
    "node_modules/**",
    "*.generated.js",
    "dist/**"
  ]
}
```

### Adjust Severity Threshold

Only show issues above a certain severity:

```json
{
  "severity_threshold": "medium"
}
```

Options: `info`, `low`, `medium`, `high`, `critical`

### Limit Comments

Prevent comment spam:

```json
{
  "max_comments": 25
}
```

### Disable Specific Features

```json
{
  "features": {
    "bug_detection": true,
    "security_scan": true,
    "doc_linking": false,
    "summarization": true
  }
}
```

## 🐛 Troubleshooting

### Bot Not Running

**Check workflow file location:**
- Must be in `.github/workflows/pr-review.yml`

**Check workflow permissions:**
- Settings → Actions → General → Workflow permissions
- Must have "Read and write permissions"

**Check secrets:**
- Settings → Secrets and variables → Actions
- Verify `BLACKBOX_API_KEY` is set

### Bot Running But No Comments

**Check PR changes:**
- Bot only comments on code files
- Markdown and config files are ignored by default

**Check severity threshold:**
- Lower the threshold in `.pr-review-bot.json`

**Check logs:**
- Go to Actions tab
- Click on the workflow run
- Check "Run PR Review Bot" step for errors

### API Rate Limiting

If you hit rate limits:

1. **Reduce frequency:**
   ```yaml
   on:
     pull_request:
       types: [opened]  # Remove synchronize
   ```

2. **Add delays:**
   Edit `src/blackbox_client.py`:
   ```python
   self.min_request_interval = 1.0  # Increase delay
   ```

### Comments Not Appearing on Correct Lines

**Check diff parsing:**
- Ensure PR has actual code changes
- Verify line numbers in analysis results

**Check file paths:**
- Paths must be relative to repository root

## 📊 Monitoring

### View Analysis Results

Results are saved as artifacts:

1. Go to Actions tab
2. Click on workflow run
3. Download "pr-review-results" artifact
4. Extract and view `analysis-results.json`

### Check Logs

```bash
# In workflow logs, look for:
- "Starting PR review for PR #X"
- "Found Y changed files"
- "Analyzing file: filename"
- "Posted comment on filename:line"
```

## 🔄 Updating the Bot

### Update to Latest Version

```bash
cd pr-review-bot
git pull origin main
```

### Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

## 🎯 Best Practices

1. **Start with low threshold** - See all issues first
2. **Gradually increase threshold** - As you fix issues
3. **Customize ignore patterns** - For your project structure
4. **Review bot suggestions** - Not all are critical
5. **Provide feedback** - Help improve the bot

## 📞 Getting Help

- **Issues:** [GitHub Issues](https://github.com/yourusername/pr-review-bot/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/pr-review-bot/discussions)
- **Documentation:** [README.md](README.md)

## 🎉 Success!

Your PR Review Bot is now set up! Every new PR will be automatically analyzed.

### What Happens Next?

1. **PR opened** → Bot triggers
2. **Code analyzed** → Blackbox AI reviews changes
3. **Issues detected** → Bot posts comments
4. **Summary generated** → Overall assessment posted
5. **Developer reviews** → Addresses feedback
6. **PR updated** → Bot re-analyzes

---

**Need help?** Open an issue or check the troubleshooting section above.
