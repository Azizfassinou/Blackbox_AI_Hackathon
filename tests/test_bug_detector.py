"""
Unit tests for bug detector.
"""

import pytest
from src.analyzers.bug_detector import BugDetector


class TestBugDetector:
    """Test cases for BugDetector."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = BugDetector()

    def test_detect_bare_except(self):
        """Test detection of bare except clauses."""
        code = """
try:
    risky_operation()
except:
    pass
"""
        issues = self.detector.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("except" in issue["message"].lower() for issue in issues)

    def test_detect_equality_with_none(self):
        """Test detection of == None comparisons."""
        code = """
if user == None:
    return False
"""
        issues = self.detector.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("none" in issue["message"].lower() for issue in issues)

    def test_detect_javascript_equality(self):
        """Test detection of == in JavaScript."""
        code = """
if (value == null) {
    return false;
}
"""
        issues = self.detector.analyze(code, "test.js")
        assert len(issues) > 0
        assert any("===" in issue["suggestion"] for issue in issues)

    def test_detect_console_log(self):
        """Test detection of console.log."""
        code = """
function debug() {
    console.log("Debug info");
}
"""
        issues = self.detector.analyze(code, "test.js")
        assert len(issues) > 0
        assert any("console.log" in issue["message"].lower() for issue in issues)

    def test_detect_debugger(self):
        """Test detection of debugger statements."""
        code = """
function test() {
    debugger;
    return true;
}
"""
        issues = self.detector.analyze(code, "test.js")
        assert len(issues) > 0
        assert any("debugger" in issue["message"].lower() for issue in issues)

    def test_no_issues_clean_code(self):
        """Test that clean code produces no issues."""
        code = """
def calculate(x, y):
    if x is None or y is None:
        raise ValueError("Arguments cannot be None")
    return x + y
"""
        issues = self.detector.analyze(code, "test.py")
        # Should have minimal or no issues
        assert len(issues) == 0 or all(
            issue["severity"] in ["info", "low"] for issue in issues
        )

    def test_language_detection(self):
        """Test language detection from filename."""
        assert self.detector._detect_language("test.py") == "python"
        assert self.detector._detect_language("test.js") == "javascript"
        assert self.detector._detect_language("test.ts") == "javascript"
        assert self.detector._detect_language("test.java") == "java"

    def test_comment_detection(self):
        """Test that issues in comments are ignored."""
        code = """
# This is a comment with except: in it
def valid_function():
    pass
"""
        issues = self.detector.analyze(code, "test.py")
        # Should not detect the except in the comment
        assert not any("except" in issue["message"].lower() for issue in issues)

    def test_complexity_check(self):
        """Test code complexity checking."""
        code = """
def complex_function():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                if i > j:
                    if j > k:
                        print(i, j, k)
"""
        metrics = self.detector.check_complexity(code)
        assert metrics["max_nesting_depth"] > 2
        assert metrics["complexity_score"] > 0


if __name__ == "__main__":
    pytest.main([__file__])
