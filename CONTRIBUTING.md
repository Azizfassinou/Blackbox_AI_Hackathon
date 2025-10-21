# Contributing to Blackbox AI PR Review Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/pr-review-bot.git
   cd pr-review-bot
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and under 50 lines when possible

### Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

### Adding New Analyzers

To add a new analyzer:

1. Create a new file in `src/analyzers/`
2. Implement the analyzer class with an `analyze()` method
3. Add tests in `tests/`
4. Update `src/main.py` to integrate the analyzer
5. Document the analyzer in README.md

Example:
```python
class MyAnalyzer:
    def analyze(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Analyze code and return issues."""
        issues = []
        # Your analysis logic here
        return issues
```

### Adding New Detection Patterns

To add new bug or security patterns:

1. Edit `src/analyzers/bug_detector.py` or `src/analyzers/security_scanner.py`
2. Add pattern to the `_load_patterns()` method
3. Include test cases
4. Document the pattern

Pattern format:
```python
{
    'pattern': r'regex_pattern',
    'language': 'python|javascript|all',
    'message': 'Description of the issue',
    'severity': 'critical|high|medium|low|info',
    'suggestion': 'How to fix it',
    'type': 'bug|security|quality|performance'
}
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

## 💡 Suggesting Features

Feature suggestions are welcome! Please:

- Check if the feature already exists or is planned
- Describe the use case and benefits
- Provide examples if possible
- Consider implementation complexity

## 📋 Pull Request Process

1. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new code
   - Update CHANGELOG.md

2. **Ensure tests pass**
   ```bash
   pytest tests/
   black src/ tests/
   flake8 src/ tests/
   ```

3. **Write a clear PR description**
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Any breaking changes

4. **Link related issues**
   - Reference issue numbers (e.g., "Fixes #123")

5. **Request review**
   - Wait for maintainer review
   - Address feedback promptly

## 🔍 Code Review Guidelines

When reviewing PRs:

- Be respectful and constructive
- Focus on code quality and maintainability
- Test the changes locally
- Check for edge cases
- Verify documentation is updated

## 📚 Documentation

Good documentation includes:

- Clear README with setup instructions
- Inline code comments for complex logic
- Docstrings for all public functions
- Examples and use cases
- Configuration options

## 🎯 Project Structure

```
pr-review-bot/
├── .github/workflows/    # GitHub Actions workflows
├── src/
│   ├── analyzers/       # Code analyzers
│   ├── utils/           # Utility functions
│   ├── main.py          # Main entry point
│   ├── blackbox_client.py
│   └── github_client.py
├── tests/               # Unit tests
├── config/              # Configuration files
└── docs/                # Documentation
```

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## 📞 Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional communication

## 🔒 Security

To report security vulnerabilities:
- Do NOT open a public issue
- Email security@example.com
- Include detailed description
- Allow time for fix before disclosure

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Blackbox AI PR Review Bot! 🎉
