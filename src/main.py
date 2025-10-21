#!/usr/bin/env python3
"""
Main entry point for the PR Review Bot.
Orchestrates the entire review process.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any

from github_client import GitHubClient
from blackbox_client import BlackboxClient
from analyzers.bug_detector import BugDetector
from analyzers.security_scanner import SecurityScanner
from analyzers.doc_linker import DocLinker
from analyzers.summarizer import Summarizer
from utils.diff_parser import DiffParser
from utils.comment_formatter import CommentFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PRReviewBot:
    """Main PR Review Bot orchestrator."""

    def __init__(self):
        """Initialize the bot with necessary clients and analyzers."""
        self.github_client = GitHubClient(
            token=os.getenv("GITHUB_TOKEN"), repo_name=os.getenv("REPO_NAME")
        )
        self.blackbox_client = BlackboxClient(api_key=os.getenv("BLACKBOX_API_KEY"))

        # Initialize analyzers
        self.bug_detector = BugDetector()
        self.security_scanner = SecurityScanner()
        self.doc_linker = DocLinker()
        self.summarizer = Summarizer()

        self.diff_parser = DiffParser()
        self.comment_formatter = CommentFormatter()

        self.pr_number = int(os.getenv("PR_NUMBER", 0))
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from repository or use defaults."""
        try:
            config_content = self.github_client.get_file_content(".pr-review-bot.json")
            if config_content:
                return json.loads(config_content)
        except Exception as e:
            logger.warning(f"Could not load config file: {e}")

        # Default configuration
        return {
            "enabled": True,
            "auto_comment": True,
            "severity_threshold": "low",
            "ignore_patterns": ["*.md", "*.txt", "package-lock.json", "yarn.lock"],
            "features": {
                "bug_detection": True,
                "security_scan": True,
                "doc_linking": True,
                "summarization": True,
            },
            "max_comments": 50,
        }

    def should_ignore_file(self, filename: str) -> bool:
        """Check if file should be ignored based on patterns."""
        import fnmatch

        for pattern in self.config.get("ignore_patterns", []):
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False

    def analyze_code_with_blackbox(
        self, code: str, filename: str, context: str = "", diff_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Analyze code using Blackbox API with fallback to local analysis."""
        try:
            # Include diff information in the prompt
            diff_context = ""
            if diff_info:
                diff_context = f"\n\nDiff Summary:\n- Additions: {diff_info.get('additions', 0)} lines\n- Deletions: {diff_info.get('deletions', 0)} lines\n- Changed lines: {diff_info.get('changed_lines', [])}"
                
                # Include specific changed code snippets
                if diff_info.get('snippets'):
                    diff_context += "\n\nChanged Code Sections:\n"
                    for snippet in diff_info['snippets'][:3]:  # Limit to first 3 snippets
                        diff_context += f"Lines {snippet.get('start_line', '?')}-{snippet.get('start_line', 0) + len(snippet.get('lines', []))}:\n```\n{snippet.get('content', '')}\n```\n"

            prompt = f"""Analyze this code for potential issues, bugs, and improvements with focus on the recent changes.

File: {filename}
Context: {context}{diff_context}

Full Code:
```
{code}
```

Please provide a comprehensive code review focusing on:
1. Issues in the changed areas (highest priority)
2. Potential bugs or logic errors
3. Security vulnerabilities
4. Code quality and maintainability issues
5. Performance concerns
6. Best practice violations
7. Suggestions for improvement

Format your response as JSON with this structure:
{{
    "issues": [
        {{
            "type": "bug|security|quality|performance|style",
            "severity": "critical|high|medium|low|info",
            "line": <line_number>,
            "message": "Description of the issue",
            "suggestion": "How to fix it",
            "code_snippet": "Suggested code fix",
            "diff_related": true/false
        }}
    ],
    "summary": "Overall code review assessment focusing on code quality and changes",
    "code_quality_score": "A|B|C|D|F",
    "main_concerns": ["list", "of", "main", "concerns"]
}}
"""

            response = self.blackbox_client.analyze_code(prompt)

            # Check if response is valid
            if response and len(response) > 50 and "Login to continue" not in response:
                return self._parse_blackbox_response(response)
            else:
                logger.warning(
                    "Blackbox API returned invalid response, using local analysis only"
                )
                return {"issues": [], "summary": "Using local pattern-based analysis", "code_quality_score": "C", "main_concerns": []}

        except Exception as e:
            logger.error(f"Error analyzing code with Blackbox: {e}")
            return {"issues": [], "summary": "Using local pattern-based analysis", "code_quality_score": "C", "main_concerns": []}

    def _parse_blackbox_response(self, response: str) -> Dict[str, Any]:
        """Parse Blackbox API response."""
        try:
            # Try to extract JSON from response
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Fallback: create structured response from text
            return {"issues": [], "summary": response[:500]}  # First 500 chars
        except Exception as e:
            logger.error(f"Error parsing Blackbox response: {e}")
            return {"issues": [], "summary": response[:500] if response else ""}

    def run_local_analyzers(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Run local pattern-based analyzers."""
        issues = []

        if self.config["features"].get("bug_detection", True):
            issues.extend(self.bug_detector.analyze(code, filename))

        if self.config["features"].get("security_scan", True):
            issues.extend(self.security_scanner.analyze(code, filename))

        return issues

    def process_pr(self):
        """Main process to review the PR."""
        try:
            logger.info(f"Starting PR review for PR #{self.pr_number}")

            if not self.config.get("enabled", True):
                logger.info("Bot is disabled in configuration")
                return

            # Get PR details
            pr = self.github_client.get_pull_request(self.pr_number)
            logger.info(f"Reviewing PR: {pr.title}")

            # Get changed files
            files = self.github_client.get_pr_files(self.pr_number)
            logger.info(f"Found {len(files)} changed files")

            all_issues = []
            file_analyses = []

            # Analyze each file
            for file in files:
                if self.should_ignore_file(file.filename):
                    logger.info(f"Skipping ignored file: {file.filename}")
                    continue

                if file.status == "removed":
                    continue

                logger.info(f"Analyzing file: {file.filename}")

                try:
                    # Get file content
                    content = self.github_client.get_file_content(
                        file.filename, ref=os.getenv("HEAD_SHA")
                    )

                    if not content:
                        continue

                    # Parse diff to get comprehensive diff information
                    diff_info = {}
                    if file.patch:
                        changed_lines = self.diff_parser.parse_patch(file.patch)
                        diff_stats = self.diff_parser.get_diff_stats(file.patch)
                        diff_snippets = self.diff_parser.extract_code_snippets(file.patch)
                        
                        diff_info = {
                            "changed_lines": changed_lines,
                            "additions": diff_stats["additions"],
                            "deletions": diff_stats["deletions"],
                            "changes": diff_stats["changes"],
                            "snippets": diff_snippets,
                            "complexity": self.diff_parser.get_change_complexity(file.patch),
                            "is_significant": self.diff_parser.is_significant_change(file.patch)
                        }

                    # Run Blackbox analysis with diff information
                    blackbox_result = self.analyze_code_with_blackbox(
                        content,
                        file.filename,
                        context=f"PR: {pr.title}\nChanges: {file.additions} additions, {file.deletions} deletions",
                        diff_info=diff_info
                    )

                    # Run local analyzers
                    local_issues = self.run_local_analyzers(content, file.filename)

                    # Combine issues
                    file_issues = blackbox_result.get("issues", []) + local_issues

                    # Add documentation links
                    if self.config["features"].get("doc_linking", True):
                        for issue in file_issues:
                            doc_links = self.doc_linker.find_relevant_docs(
                                issue.get("message", ""), file.filename
                            )
                            issue["doc_links"] = doc_links

                    # Filter by severity threshold
                    severity_order = ["info", "low", "medium", "high", "critical"]
                    threshold_idx = severity_order.index(
                        self.config.get("severity_threshold", "low")
                    )

                    filtered_issues = [
                        issue
                        for issue in file_issues
                        if severity_order.index(issue.get("severity", "info"))
                        >= threshold_idx
                    ]

                    file_analyses.append(
                        {
                            "filename": file.filename,
                            "issues": filtered_issues,
                            "summary": blackbox_result.get("summary", ""),
                            "code_quality_score": blackbox_result.get("code_quality_score", "C"),
                            "main_concerns": blackbox_result.get("main_concerns", []),
                            "stats": {
                                "additions": file.additions,
                                "deletions": file.deletions,
                                "changes": file.changes,
                            },
                            "diff_info": diff_info,
                        }
                    )

                    all_issues.extend(filtered_issues)

                except Exception as e:
                    logger.error(f"Error analyzing file {file.filename}: {e}")
                    continue

            # Post comments
            if self.config.get("auto_comment", True) and all_issues:
                self._post_review_comments(file_analyses)

            # Generate and post summary with diff information
            if self.config["features"].get("summarization", True):
                # Prepare comprehensive diff summary
                diff_summary = {
                    "total_additions": sum(fa["stats"]["additions"] for fa in file_analyses),
                    "total_deletions": sum(fa["stats"]["deletions"] for fa in file_analyses),
                    "significant_files": [
                        {
                            "filename": fa["filename"],
                            "additions": fa["stats"]["additions"],
                            "deletions": fa["stats"]["deletions"],
                            "complexity": fa.get("diff_info", {}).get("complexity", "medium")
                        }
                        for fa in file_analyses
                        if fa.get("diff_info", {}).get("is_significant", False)
                    ],
                    "overall_complexity": self._calculate_overall_complexity(file_analyses)
                }
                
                summary = self.summarizer.generate_summary(
                    pr_title=pr.title,
                    pr_description=pr.body or "",
                    file_analyses=file_analyses,
                    total_files=len(files),
                    diff_summary=diff_summary
                )
                self._post_summary_comment(summary)

            # Save results
            self._save_results(file_analyses, all_issues)

            logger.info(f"PR review completed. Found {len(all_issues)} issues.")

        except Exception as e:
            logger.error(f"Error processing PR: {e}", exc_info=True)
            sys.exit(1)

    def _calculate_overall_complexity(self, file_analyses: List[Dict[str, Any]]) -> str:
        """Calculate overall complexity of the PR changes."""
        if not file_analyses:
            return "low"
        
        complexity_scores = {"low": 1, "medium": 2, "high": 3}
        total_score = 0
        count = 0
        
        for fa in file_analyses:
            diff_info = fa.get("diff_info", {})
            complexity = diff_info.get("complexity", "medium")
            if complexity in complexity_scores:
                total_score += complexity_scores[complexity]
                count += 1
        
        if count == 0:
            return "medium"
        
        avg_score = total_score / count
        if avg_score <= 1.3:
            return "low"
        elif avg_score <= 2.3:
            return "medium"
        else:
            return "high"

    def _post_review_comments(self, file_analyses: List[Dict[str, Any]]):
        """Post inline review comments on the PR."""
        comment_count = 0
        max_comments = self.config.get("max_comments", 50)

        for file_analysis in file_analyses:
            filename = file_analysis["filename"]

            for issue in file_analysis["issues"]:
                if comment_count >= max_comments:
                    logger.warning(f"Reached maximum comment limit ({max_comments})")
                    break

                try:
                    comment_body = self.comment_formatter.format_issue(issue)

                    # Post comment on specific line if available
                    line = issue.get("line")
                    if line:
                        self.github_client.create_review_comment(
                            pr_number=self.pr_number,
                            body=comment_body,
                            path=filename,
                            line=line,
                        )
                        comment_count += 1
                        logger.info(f"Posted comment on {filename}:{line}")

                except Exception as e:
                    logger.error(f"Error posting comment: {e}")
                    continue

            if comment_count >= max_comments:
                break

    def _post_summary_comment(self, summary: str):
        """Post a summary comment on the PR."""
        try:
            self.github_client.create_issue_comment(
                pr_number=self.pr_number, body=summary
            )
            logger.info("Posted summary comment")
        except Exception as e:
            logger.error(f"Error posting summary: {e}")

    def _save_results(
        self, file_analyses: List[Dict[str, Any]], all_issues: List[Dict[str, Any]]
    ):
        """Save analysis results to files."""
        try:
            # Save detailed results
            with open("analysis-results.json", "w") as f:
                json.dump(
                    {
                        "pr_number": self.pr_number,
                        "file_analyses": file_analyses,
                        "total_issues": len(all_issues),
                        "config": self.config,
                    },
                    f,
                    indent=2,
                )

            logger.info("Saved analysis results to analysis-results.json")

        except Exception as e:
            logger.error(f"Error saving results: {e}")


def main():
    """Main entry point."""
    # Validate environment variables
    required_vars = ["GITHUB_TOKEN", "BLACKBOX_API_KEY", "PR_NUMBER", "REPO_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        sys.exit(1)

    # Run the bot
    bot = PRReviewBot()
    bot.process_pr()


if __name__ == "__main__":
    main()
