import os
import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('Content-Type') != 'application/json':
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Content-Type must be application/json"}')
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        pr_number = data.get('pr_number')
        repo = data.get('repo')
        token = data.get('token')

        if not all([pr_number, repo, token]):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Missing pr_number, repo, or token"}')
            return

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

            # Analyze with Blackbox API
            blackbox_url = "https://api.blackbox.ai/analyze"  # Replace with actual endpoint
            blackbox_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("BLACKBOX_API_KEY")}'
            }
            blackbox_data = {
                'prompt': f"Analyze this PR diff: Provide a recap of changes, detect potential bugs, and suggest relevant documentation links. Diff: {diff}"
            }
            analysis_response = requests.post(blackbox_url, json=blackbox_data, headers=blackbox_headers)
            analysis_response.raise_for_status()
            analysis = analysis_response.json()

            # Post comment
            comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
            comment_data = {
                'body': f"🤖 PR Analysis:\n\nRecap: {analysis.get('recap', 'N/A')}\n\nPotential Bugs: {analysis.get('bugs', 'None detected')}\n\nDoc Links: {analysis.get('docs', 'N/A')}"
            }
            comment_response = requests.post(comment_url, json=comment_data, headers={
                'Authorization': f'token {token}',
                'Content-Type': 'application/json'
            })
            comment_response.raise_for_status()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"success": true}')

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

            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"error": "Analysis failed"}')

        return
