"""
Component tests for utilities and analyzers.
"""

import pytest
from src.utils.diff_parser import DiffParser
from src.utils.comment_formatter import CommentFormatter
from src.analyzers.doc_linker import DocLinker
from src.analyzers.summarizer import Summarizer


class TestDiffParser:
    """Test diff parser functionality."""

    @pytest.fixture
    def parser(self):
        return DiffParser()

    def test_parse_simple_patch(self, parser):
        """Test parsing a simple git patch."""
        patch = """@@ -1,3 +1,4 @@
 def hello():
-    print("world")
+    print("Hello, World!")
+    return True
"""
        changed_lines = parser.parse_patch(patch)

        assert len(changed_lines) > 0
        assert any(line["type"] == "addition" for line in changed_lines)
        assert any(line["type"] == "deletion" for line in changed_lines)
        print(f"\n✅ Parsed {len(changed_lines)} changed lines")
        for line in changed_lines:
            print(f"  Line {line['line']}: {line['type']}")

    def test_parse_addition_only(self, parser):
        """Test parsing additions only."""
        patch = """@@ -1,2 +1,3 @@
 def test():
     pass
+    return None
"""
        changed_lines = parser.parse_patch(patch)

        assert len(changed_lines) > 0
        assert all(line["type"] == "addition" for line in changed_lines)
        print(f"\n✅ Parsed {len(changed_lines)} additions")


class TestCommentFormatter:
    """Test comment formatter."""

    @pytest.fixture
    def formatter(self):
        return CommentFormatter()

    def test_format_bug_issue(self, formatter):
        """Test formatting a bug issue."""
        issue = {
            "type": "bug",
            "severity": "high",
            "message": "Potential null pointer exception",
            "suggestion": "Add null check",
            "code_snippet": "user.name",
            "line": 42,
        }

        comment = formatter.format_issue(issue)

        assert "🐛" in comment
        assert "high" in comment.lower()
        assert "null pointer" in comment.lower()
        assert "Add null check" in comment
        print(f"\n✅ Formatted comment:\n{comment[:200]}")

    def test_format_security_issue(self, formatter):
        """Test formatting a security issue."""
        issue = {
            "type": "security",
            "severity": "critical",
            "message": "SQL injection vulnerability",
            "suggestion": "Use parameterized queries",
            "cwe": "CWE-89",
            "line": 15,
        }

        comment = formatter.format_issue(issue)

        assert "🔒" in comment
        assert "critical" in comment.lower()
        assert "SQL injection" in comment
        assert "CWE-89" in comment
        print(f"\n✅ Formatted security comment:\n{comment[:200]}")


class TestDocLinker:
    """Test documentation linker."""

    @pytest.fixture
    def linker(self):
        return DocLinker()

    def test_find_python_docs(self, linker):
        """Test finding Python documentation."""
        message = "Use list comprehension instead of map"
        filename = "test.py"

        docs = linker.find_relevant_docs(message, filename)

        assert isinstance(docs, list)
        if docs:
            assert "url" in docs[0]
            assert "title" in docs[0]
            print(f"\n✅ Found {len(docs)} documentation links")
            for doc in docs[:2]:
                print(f"  - {doc['title']}: {doc['url']}")

    def test_find_javascript_docs(self, linker):
        """Test finding JavaScript documentation."""
        message = "Use const instead of var"
        filename = "test.js"

        docs = linker.find_relevant_docs(message, filename)

        assert isinstance(docs, list)
        print(f"\n✅ Found {len(docs)} JS documentation links")


class TestSummarizer:
    """Test PR summarizer."""

    @pytest.fixture
    def summarizer(self):
        return Summarizer()

    def test_generate_basic_summary(self, summarizer):
        """Test generating a basic PR summary."""
        file_analyses = [
            {
                "filename": "test.py",
                "issues": [
                    {"severity": "high", "type": "bug", "message": "Bug found"},
                    {
                        "severity": "medium",
                        "type": "security",
                        "message": "Security issue",
                    },
                ],
                "summary": "File has some issues",
                "stats": {"additions": 10, "deletions": 5, "changes": 15},
            }
        ]

        summary = summarizer.generate_summary(
            pr_title="Add new feature",
            pr_description="This PR adds a new feature",
            file_analyses=file_analyses,
            total_files=1,
        )

        assert len(summary) > 0
        assert "test.py" in summary
        assert "high" in summary.lower() or "bug" in summary.lower()
        print(f"\n✅ Generated summary ({len(summary)} chars):\n{summary[:300]}")

    def test_summary_with_no_issues(self, summarizer):
        """Test summary when no issues found."""
        file_analyses = [
            {
                "filename": "clean.py",
                "issues": [],
                "summary": "Code looks good",
                "stats": {"additions": 5, "deletions": 2, "changes": 7},
            }
        ]

        summary = summarizer.generate_summary(
            pr_title="Clean code",
            pr_description="",
            file_analyses=file_analyses,
            total_files=1,
        )

        assert len(summary) > 0
        assert "✅" in summary or "good" in summary.lower()
        print(f"\n✅ Clean code summary:\n{summary[:200]}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
