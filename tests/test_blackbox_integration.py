"""
Integration tests for Blackbox API client.
"""

import os
import pytest
from src.blackbox_client import BlackboxClient


class TestBlackboxIntegration:
    """Test Blackbox API integration."""
    
    @pytest.fixture
    def client(self):
        """Create Blackbox client with API key."""
        api_key = os.getenv('BLACKBOX_API_KEY', 'sk-zduYOC3n0GcsEQnyjNrnvg')
        return BlackboxClient(api_key)
    
    def test_analyze_simple_code(self, client):
        """Test analyzing simple code snippet."""
        code = """
def divide(a, b):
    return a / b
"""
        prompt = f"Analyze this Python code for potential issues:\n\n{code}"
        
        result = client.analyze_code(prompt)
        
        # Should return some response
        assert result is not None
        assert len(result) > 0
        print(f"\n✅ Blackbox API Response ({len(result)} chars):")
        print(result[:500])  # Print first 500 chars
    
    def test_analyze_buggy_code(self, client):
        """Test analyzing code with obvious bugs."""
        code = """
def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)
"""
        prompt = f"""Analyze this code for security issues:

{code}

Focus on SQL injection vulnerabilities."""
        
        result = client.analyze_code(prompt)
        
        assert result is not None
        assert len(result) > 0
        # Should mention SQL injection
        assert 'sql' in result.lower() or 'injection' in result.lower()
        print(f"\n✅ Security Analysis Response:")
        print(result[:500])
    
    def test_rate_limiting(self, client):
        """Test that rate limiting works."""
        import time
        
        start_time = time.time()
        
        # Make two quick requests
        client.analyze_code("print('hello')")
        client.analyze_code("print('world')")
        
        elapsed = time.time() - start_time
        
        # Should take at least min_request_interval seconds
        assert elapsed >= client.min_request_interval
        print(f"\n✅ Rate limiting working: {elapsed:.2f}s elapsed")
    
    def test_error_handling(self, client):
        """Test error handling with invalid input."""
        # Very long prompt that might cause issues
        long_code = "x = 1\n" * 10000
        
        result = client.analyze_code(long_code)
        
        # Should handle gracefully (return empty or truncated)
        assert result is not None
        print(f"\n✅ Error handling works: returned {len(result)} chars")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
