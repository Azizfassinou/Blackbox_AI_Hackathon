# GitHub PR Analysis Bot

A bot that analyzes GitHub Pull Requests using Blackbox AI to provide recaps, bug detection, and documentation links.

## Features
- Automatically analyzes PR diffs on open/sync
- Provides recap of changes
- Detects potential bugs
- Suggests relevant documentation links
- Posts comments directly on PRs

## Setup
1. Clone this repo to your GitHub repository.
2. Add secrets in GitHub repo settings: BLACKBOX_API_KEY (from Blackbox API), GITHUB_TOKEN (auto-provided by Actions).
3. Ensure .github/workflows/pr-analyzer.yml and analyze_pr.py are in the repo.
4. Create a PR to test—the bot will analyze and comment automatically.

## Demo
Create a PR with code changes, the bot will comment with analysis.
