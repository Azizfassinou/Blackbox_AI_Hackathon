"""
Unit tests for security scanner.
"""

import pytest
from src.analyzers.security_scanner import SecurityScanner


class TestSecurityScanner:
    """Test cases for SecurityScanner."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = SecurityScanner()

    def test_detect_sql_injection(self):
        """Test detection of SQL injection vulnerabilities."""
        code = """
query = "SELECT * FROM users WHERE id = %s" % user_id
cursor.execute(query)
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("sql injection" in issue["message"].lower() for issue in issues)
        assert any(issue["severity"] == "critical" for issue in issues)

    def test_detect_hardcoded_password(self):
        """Test detection of hardcoded passwords."""
        code = """
password = "MySecretPassword123"
api_key = "sk-1234567890abcdef"
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any(
            "password" in issue["message"].lower()
            or "api key" in issue["message"].lower()
            for issue in issues
        )

    def test_detect_xss_vulnerability(self):
        """Test detection of XSS vulnerabilities."""
        code = """
element.innerHTML = userInput;
"""
        issues = self.scanner.analyze(code, "test.js")
        assert len(issues) > 0
        assert any("xss" in issue["message"].lower() for issue in issues)

    def test_detect_eval_usage(self):
        """Test detection of eval() usage."""
        code = """
result = eval(user_input);
"""
        issues = self.scanner.analyze(code, "test.js")
        assert len(issues) > 0
        assert any("eval" in issue["message"].lower() for issue in issues)
        assert any(issue["severity"] == "critical" for issue in issues)

    def test_detect_command_injection(self):
        """Test detection of command injection."""
        code = """
import os
os.system("rm -rf " + user_input)
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any(
            "command injection" in issue["message"].lower()
            or "os.system" in issue["message"].lower()
            for issue in issues
        )

    def test_detect_weak_crypto(self):
        """Test detection of weak cryptography."""
        code = """
import hashlib
hash = hashlib.md5(password.encode()).hexdigest()
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("md5" in issue["message"].lower() for issue in issues)

    def test_detect_insecure_deserialization(self):
        """Test detection of insecure deserialization."""
        code = """
import pickle
data = pickle.loads(user_data)
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("pickle" in issue["message"].lower() for issue in issues)

    def test_detect_ssl_verification_disabled(self):
        """Test detection of disabled SSL verification."""
        code = """
response = requests.get(url, verify=False)
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any(
            "ssl" in issue["message"].lower() or "verify" in issue["message"].lower()
            for issue in issues
        )

    def test_no_issues_secure_code(self):
        """Test that secure code produces no issues."""
        code = """
import hashlib
hash = hashlib.sha256(password.encode()).hexdigest()
"""
        issues = self.scanner.analyze(code, "test.py")
        # Should have no critical security issues
        critical_issues = [i for i in issues if i["severity"] in ["critical", "high"]]
        assert len(critical_issues) == 0

    def test_cwe_references(self):
        """Test that CWE references are included."""
        code = """
query = "SELECT * FROM users WHERE id = " + user_id
"""
        issues = self.scanner.analyze(code, "test.py")
        assert len(issues) > 0
        assert any("cwe" in issue for issue in issues)

    def test_generate_security_report(self):
        """Test security report generation."""
        vulnerabilities = [
            {"severity": "critical", "message": "SQL injection"},
            {"severity": "high", "message": "XSS vulnerability"},
            {"severity": "medium", "message": "Weak crypto"},
        ]
        report = self.scanner.generate_security_report(vulnerabilities)
        assert "CRITICAL" in report
        assert "HIGH" in report
        assert "MEDIUM" in report

    def test_empty_report(self):
        """Test report generation with no vulnerabilities."""
        report = self.scanner.generate_security_report([])
        assert "No security vulnerabilities" in report


if __name__ == "__main__":
    pytest.main([__file__])
