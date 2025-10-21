# ⚡ Quick Start Guide

Get the Blackbox AI PR Review Bot running in 5 minutes!

## 🎯 Prerequisites

- GitHub repository with admin access
- Blackbox API key: `sk-zduYOC3n0GcsEQnyjNrnvg`

## 🚀 Setup (3 Steps)

### Step 1: Add Workflow File (1 min)

Copy the workflow to your repository:

```bash
# In your repository root
mkdir -p .github/workflows
curl -o .github/workflows/pr-review.yml https://raw.githubusercontent.com/yourusername/pr-review-bot/main/.github/workflows/pr-review.yml
```

Or manually create `.github/workflows/pr-review.yml` with the workflow content.

### Step 2: Add Bot Files (1 min)

```bash
# Clone or download the bot
git clone https://github.com/yourusername/pr-review-bot.git temp-bot
cp -r temp-bot/src .
cp temp-bot/requirements.txt .
rm -rf temp-bot
```

### Step 3: Configure Secrets (1 min)

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:
   - Name: `BLACKBOX_API_KEY`
   - Value: `sk-zduYOC3n0GcsEQnyjNrnvg`

## ✅ Test It!

Create a test PR:

```bash
git checkout -b test-bot
echo "print('hello')" > test.py
git add test.py
git commit -m "Test PR bot"
git push origin test-bot
```

Then create a PR on GitHub and watch the bot work! 🎉

## 📊 What Happens Next?

1. **PR Created** → Bot triggers automatically
2. **Analysis Runs** → Takes 1-2 minutes
3. **Comments Posted** → Issues highlighted inline
4. **Summary Added** → Overall assessment posted

## 🎨 Customize (Optional)

Create `.pr-review-bot.json` in your repo root:

```json
{
  "enabled": true,
  "severity_threshold": "medium",
  "max_comments": 25
}
```

## 🐛 Troubleshooting

**Bot not running?**
- Check `.github/workflows/pr-review.yml` exists
- Verify `BLACKBOX_API_KEY` secret is set
- Check Actions tab for errors

**No comments?**
- Bot only comments on code files
- Lower severity threshold in config
- Check workflow logs in Actions tab

## 📚 Learn More

- [Full Setup Guide](SETUP_GUIDE.md)
- [Configuration Options](README.md#configuration)
- [Example Output](examples/example_pr_review.md)

## 💬 Need Help?

- [Open an Issue](https://github.com/yourusername/pr-review-bot/issues)
- [Read the Docs](README.md)
- [See Examples](examples/)

---

**That's it!** Your PR review bot is now active. Every new PR will be automatically reviewed! 🚀
