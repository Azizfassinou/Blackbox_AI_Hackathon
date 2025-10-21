#!/usr/bin/env python3
"""Quick test of Blackbox API."""

import sys
sys.path.insert(0, 'src')

from blackbox_client import BlackboxClient

# Test the API
client = BlackboxClient('sk-zduYOC3n0GcsEQnyjNrnvg')

print("Testing Blackbox API...")
print("=" * 50)

code = """
def divide(a, b):
    return a / b
"""

result = client.analyze_code(f"Analyze this code for bugs:\n{code}")

print(f"Response length: {len(result)} chars")
print(f"Response preview: {result[:200] if result else 'EMPTY'}")
print("=" * 50)

if result:
    print("✅ API is working!")
else:
    print("❌ API returned empty response")
