import os
import json
import requests
import sys

def analyze_pr(pr_number, repo, token):
    try:
        # Fetch PR diff
        diff_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3.diff'
        }
        diff_response = requests.get(diff_url, headers=headers)
        diff_response.raise_for_status()
        diff = diff_response.text

        # Analyze with Blackbox API (assuming endpoint; adjust if needed)
        blackbox_url = "https://api.blackbox.ai/analyze"  # Replace with actual Blackbox API endpoint
        blackbox_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ.get("BLACKBOX_API_KEY")}'
        }
        blackbox_data = {
            'prompt': f"Analyze this PR diff: Provide a recap of changes, detect potential bugs, and suggest relevant documentation links. Diff: {diff[:5000]}"  # Limit diff size
        }
        analysis_response = requests.post(blackbox_url, json=blackbox_data, headers=blackbox_headers)
        analysis_response.raise_for_status()
        analysis = analysis_response.json()

        # Post comment
        comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        comment_data = {
            'body': f"🤖 PR Analysis:\n\n**Recap:** {analysis.get('recap', 'N/A')}\n\n**Potential Bugs:** {analysis.get('bugs', 'None detected')}\n\n**Doc Links:** {analysis.get('docs', 'N/A')}"
        }
        comment_response = requests.post(comment_url, json=comment_data, headers={
            'Authorization': f'token {token}',
            'Content-Type': 'application/json'
        })
        comment_response.raise_for_status()

        print("Analysis complete, comment posted.")

    except requests.RequestException as e:
        print(f"Error: {e}")
        # Post error comment
        try:
            error_comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
            error_comment_data = {'body': '🤖 PR Analysis failed. Please check the bot configuration.'}
            requests.post(error_comment_url, json=error_comment_data, headers={
                'Authorization': f'token {token}',
                'Content-Type': 'application/json'
            })
        except:
            pass

if __name__ == "__main__":
    pr_number = os.environ.get('PR_NUMBER')
    repo = os.environ.get('REPO')
    token = os.environ.get('GITHUB_TOKEN')

    if not all([pr_number, repo, token]):
        print("Missing environment variables")
        sys.exit(1)

    analyze_pr(pr_number, repo, token)
