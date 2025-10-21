"""
PR summarizer - generates comprehensive summaries of pull requests.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class Summarizer:
    """Generates summaries for pull requests."""

    def __init__(self):
        """Initialize summarizer."""
        pass

    def generate_summary(
        self,
        pr_title: str,
        pr_description: str,
        file_analyses: List[Dict[str, Any]],
        total_files: int,
        diff_summary: Dict[str, Any] = None,
    ) -> str:
        """
        Generate a comprehensive PR summary with diff information.

        Args:
            pr_title: PR title
            pr_description: PR description
            file_analyses: List of file analysis results
            total_files: Total number of files changed
            diff_summary: Summary of diff information

        Returns:
            Formatted summary as markdown
        """
        # Calculate statistics
        total_issues = sum(len(fa["issues"]) for fa in file_analyses)

        # Group issues by severity and type
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        type_counts = {"bug": 0, "security": 0, "quality": 0, "performance": 0, "style": 0}
        code_quality_scores = []

        for file_analysis in file_analyses:
            # Extract code quality score if available
            if "code_quality_score" in file_analysis:
                score = file_analysis["code_quality_score"]
                if score in ["A", "B", "C", "D", "F"]:
                    code_quality_scores.append(score)

            for issue in file_analysis["issues"]:
                severity = issue.get("severity", "info")
                issue_type = issue.get("type", "quality")

                if severity in severity_counts:
                    severity_counts[severity] += 1
                if issue_type in type_counts:
                    type_counts[issue_type] += 1

        # Prepare diff summary information
        if not diff_summary:
            diff_summary = {
                "total_additions": sum(fa["stats"]["additions"] for fa in file_analyses),
                "total_deletions": sum(fa["stats"]["deletions"] for fa in file_analyses),
                "overall_complexity": "medium",
                "significant_files": [
                    {
                        "filename": fa["filename"],
                        "additions": fa["stats"]["additions"],
                        "deletions": fa["stats"]["deletions"]
                    }
                    for fa in file_analyses
                    if fa["stats"]["additions"] + fa["stats"]["deletions"] > 10
                ]
            }

        # Prepare code quality overview
        code_quality_overview = {}
        if code_quality_scores:
            # Calculate average score (A=4, B=3, C=2, D=1, F=0)
            score_values = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
            avg_score_value = sum(score_values.get(s, 2) for s in code_quality_scores) / len(code_quality_scores)
            
            for score, value in score_values.items():
                if abs(avg_score_value - value) < 0.5:
                    code_quality_overview["average_score"] = score
                    break
            else:
                code_quality_overview["average_score"] = "C"

        # Extract main concerns from file analyses
        main_concerns = []
        for fa in file_analyses:
            if "main_concerns" in fa:
                main_concerns.extend(fa["main_concerns"])
        
        # Remove duplicates and limit
        main_concerns = list(dict.fromkeys(main_concerns))[:5]
        if main_concerns:
            code_quality_overview["main_concerns"] = main_concerns

        # Get top issues with file context
        top_issues = []
        for file_analysis in file_analyses:
            for issue in file_analysis["issues"]:
                issue_with_file = issue.copy()
                issue_with_file["file"] = file_analysis["filename"]
                top_issues.append(issue_with_file)

        # Sort by severity (critical first)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        top_issues.sort(key=lambda x: severity_order.get(x.get("severity", "info"), 4))

        # Use the enhanced comment formatter
        from utils.comment_formatter import CommentFormatter
        formatter = CommentFormatter()
        
        summary = formatter.format_summary_comment(
            total_files=total_files,
            total_issues=total_issues,
            severity_breakdown=severity_counts,
            top_issues=top_issues[:10],  # Top 10 issues
            diff_summary=diff_summary,
            code_quality_overview=code_quality_overview
        )

        return summary

    def _determine_assessment(self, severity_counts: Dict[str, int]) -> str:
        """Determine overall assessment based on severity counts."""
        if severity_counts["critical"] > 0:
            return "🚨 Critical Issues Found"
        elif severity_counts["high"] > 0:
            return "⚠️ Needs Attention"
        elif severity_counts["medium"] > 0:
            return "⚡ Minor Issues"
        elif severity_counts["low"] > 0 or severity_counts["info"] > 0:
            return "✅ Looks Good"
        else:
            return "✨ Excellent"

    def _build_summary_header(self, pr_title: str, assessment: str) -> str:
        """Build summary header."""
        return f"""## 🤖 Blackbox AI PR Review

**PR Title:** {pr_title}

**Overall Assessment:** {assessment}

---

"""

    def _build_statistics_section(
        self, total_files: int, additions: int, deletions: int, issues: int
    ) -> str:
        """Build statistics section."""
        return f"""### 📊 Statistics

- **Files Changed:** {total_files}
- **Lines Added:** +{additions}
- **Lines Removed:** -{deletions}
- **Issues Found:** {issues}

"""

    def _build_findings_section(
        self, severity_counts: Dict[str, int], type_counts: Dict[str, int]
    ) -> str:
        """Build findings section."""
        section = "### 🔍 Key Findings\n\n"

        # Severity breakdown
        if any(severity_counts.values()):
            section += "**By Severity:**\n"
            if severity_counts["critical"] > 0:
                section += f"- 🚨 {severity_counts['critical']} Critical\n"
            if severity_counts["high"] > 0:
                section += f"- ⚠️ {severity_counts['high']} High\n"
            if severity_counts["medium"] > 0:
                section += f"- ⚡ {severity_counts['medium']} Medium\n"
            if severity_counts["low"] > 0:
                section += f"- ℹ️ {severity_counts['low']} Low\n"
            if severity_counts["info"] > 0:
                section += f"- 💡 {severity_counts['info']} Info\n"
            section += "\n"

        # Type breakdown
        if any(type_counts.values()):
            section += "**By Type:**\n"
            if type_counts["security"] > 0:
                section += f"- 🔒 {type_counts['security']} Security Issues\n"
            if type_counts["bug"] > 0:
                section += f"- 🐛 {type_counts['bug']} Potential Bugs\n"
            if type_counts["performance"] > 0:
                section += f"- ⚡ {type_counts['performance']} Performance Concerns\n"
            if type_counts["quality"] > 0:
                section += f"- 📝 {type_counts['quality']} Code Quality Issues\n"
            section += "\n"

        return section

    def _build_description_section(self, pr_description: str) -> str:
        """Build description section."""
        if not pr_description or pr_description.strip() == "":
            return ""

        # Truncate if too long
        max_length = 500
        if len(pr_description) > max_length:
            pr_description = pr_description[:max_length] + "..."

        return f"""### 📝 PR Description

{pr_description}

"""

    def _build_critical_issues_section(
        self, file_analyses: List[Dict[str, Any]]
    ) -> str:
        """Build critical issues section."""
        critical_issues = []

        for file_analysis in file_analyses:
            for issue in file_analysis["issues"]:
                if issue.get("severity") in ["critical", "high"]:
                    critical_issues.append(
                        {
                            "file": file_analysis["filename"],
                            "line": issue.get("line", "N/A"),
                            "severity": issue.get("severity", "unknown"),
                            "message": issue.get("message", "No message"),
                            "type": issue.get("type", "unknown"),
                        }
                    )

        if not critical_issues:
            return "### ✅ No Critical Issues\n\nNo critical or high-severity issues were detected.\n\n"

        section = "### ⚠️ Critical Issues\n\n"

        # Limit to top 5 critical issues
        for i, issue in enumerate(critical_issues[:5], 1):
            emoji = "🚨" if issue["severity"] == "critical" else "⚠️"
            section += f"{i}. {emoji} **{issue['file']}:{issue['line']}** - {issue['message']}\n"

        if len(critical_issues) > 5:
            section += f"\n*...and {len(critical_issues) - 5} more critical issues. See inline comments for details.*\n"

        section += "\n"
        return section

    def _build_recommendations_section(
        self, file_analyses: List[Dict[str, Any]], severity_counts: Dict[str, int]
    ) -> str:
        """Build recommendations section."""
        section = "### 💡 Recommendations\n\n"

        recommendations = []

        # Generate recommendations based on findings
        if severity_counts["critical"] > 0:
            recommendations.append(
                "🚨 **Address all critical security vulnerabilities before merging**"
            )

        # Count security and bug issues from file_analyses
        security_count = sum(
            1
            for fa in file_analyses
            for issue in fa["issues"]
            if issue.get("type") == "security"
        )
        bug_count = sum(
            1
            for fa in file_analyses
            for issue in fa["issues"]
            if issue.get("type") == "bug"
        )

        if security_count > 0:
            recommendations.append(
                "🔒 Review and fix security issues to prevent vulnerabilities"
            )

        if bug_count > 0:
            recommendations.append("🐛 Fix potential bugs to improve code reliability")

        # Check for missing tests
        has_test_files = any("test" in fa["filename"].lower() for fa in file_analyses)
        if not has_test_files and len(file_analyses) > 0:
            recommendations.append(
                "🧪 Consider adding unit tests for new functionality"
            )

        # Check for documentation
        has_docs = any(
            fa["filename"].endswith((".md", ".rst", ".txt")) for fa in file_analyses
        )
        if not has_docs and len(file_analyses) > 3:
            recommendations.append("📚 Update documentation to reflect changes")

        if not recommendations:
            recommendations.append(
                "✅ Code looks good! Consider adding more tests and documentation."
            )

        for rec in recommendations:
            section += f"- {rec}\n"

        section += "\n"
        return section

    def _build_file_breakdown_section(self, file_analyses: List[Dict[str, Any]]) -> str:
        """Build file-by-file breakdown section."""
        if not file_analyses:
            return ""

        section = "### 📁 File Breakdown\n\n"

        for file_analysis in file_analyses[:10]:  # Limit to 10 files
            filename = file_analysis["filename"]
            issues = file_analysis["issues"]
            stats = file_analysis["stats"]

            issue_count = len(issues)
            if issue_count == 0:
                status = "✅"
            elif any(i.get("severity") in ["critical", "high"] for i in issues):
                status = "⚠️"
            else:
                status = "ℹ️"

            section += f"{status} **{filename}** "
            section += f"(+{stats['additions']}/-{stats['deletions']}) - "
            section += f"{issue_count} issue(s)\n"

        if len(file_analyses) > 10:
            section += f"\n*...and {len(file_analyses) - 10} more files*\n"

        section += "\n"
        return section

    def _build_footer(self) -> str:
        """Build summary footer."""
        return """---

*This review was automatically generated by [Blackbox AI PR Review Bot](https://github.com/yourusername/pr-review-bot)*

*💡 Tip: Review inline comments for detailed suggestions and fixes*
"""

    def generate_quick_summary(self, file_analyses: List[Dict[str, Any]]) -> str:
        """
        Generate a quick one-line summary.

        Args:
            file_analyses: List of file analysis results

        Returns:
            Quick summary string
        """
        total_issues = sum(len(fa["issues"]) for fa in file_analyses)
        critical_count = sum(
            1
            for fa in file_analyses
            for issue in fa["issues"]
            if issue.get("severity") == "critical"
        )

        if critical_count > 0:
            return f"🚨 Found {total_issues} issues including {critical_count} critical"
        elif total_issues > 0:
            return f"⚠️ Found {total_issues} issues to review"
        else:
            return "✅ No issues found"
