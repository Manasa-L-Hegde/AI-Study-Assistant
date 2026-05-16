# Contributing to AI Study Assistant

First off, thank you for considering contributing to AI Study Assistant! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful**: Treat everyone with respect and kindness
- **Be collaborative**: Work together and help each other
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be constructive**: Provide helpful feedback and suggestions

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** and motivation
- **Proposed solution** or implementation ideas
- **Alternative solutions** you've considered

### Code Contributions

We welcome code contributions! Here are some areas where you can help:

- **Bug fixes**: Fix reported issues
- **New features**: Implement requested features
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **UI/UX**: Enhance user interface and experience

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Study-Assistant.git
   cd AI-Study-Assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized in groups (standard library, third-party, local)

### Code Formatting

We use **Black** for code formatting:

```bash
black src/ tests/
```

### Linting

We use **Flake8** for linting:

```bash
flake8 src/ tests/
```

### Type Hints

Use type hints for function parameters and return values:

```python
def process_data(input_text: str, max_length: int = 100) -> dict:
    """Process input text and return structured data."""
    pass
```

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain why, not what
- **README**: Update if adding new features

Example docstring:

```python
def validate_input(text: str, max_length: int) -> tuple[bool, Optional[str]]:
    """
    Validate user input text.
    
    Args:
        text: The input text to validate
        max_length: Maximum allowed length
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Raises:
        ValueError: If max_length is negative
    """
    pass
```

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(ui): add dark mode toggle button

Add a toggle button in the sidebar to switch between dark and light themes.
The theme preference is saved in session state.

Closes #123
```

```bash
fix(api): handle rate limit errors gracefully

Add proper error handling for Groq API rate limit errors.
Display user-friendly message and suggest retry.

Fixes #456
```

## 🔄 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Follow the PR template**
6. **Request review** from maintainers

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings
- [ ] CHANGELOG.md updated

### PR Title Format

Use the same format as commit messages:

```
feat(component): add new feature
fix(module): resolve bug
docs: update README
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py

# Run specific test
pytest tests/test_validators.py::TestInputValidator::test_validate_topic_valid
```

### Writing Tests

- **Test file naming**: `test_<module>.py`
- **Test function naming**: `test_<function>_<scenario>`
- **Use fixtures**: For common setup
- **Mock external calls**: Don't make real API calls in tests

Example test:

```python
def test_validate_topic_valid():
    """Test validation of valid topic."""
    is_valid, error = validate_topic("Machine Learning")
    assert is_valid is True
    assert error is None
```

### Test Coverage

Aim for at least 80% code coverage. Check coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

## 🎨 UI/UX Guidelines

### Design Principles

- **Simplicity**: Keep interfaces clean and intuitive
- **Consistency**: Use consistent patterns and components
- **Accessibility**: Ensure WCAG 2.1 AA compliance
- **Responsiveness**: Support all screen sizes
- **Performance**: Optimize for fast load times

### Color Palette

- **Primary**: `#667eea` (Purple)
- **Secondary**: `#764ba2` (Dark Purple)
- **Success**: `#10b981` (Green)
- **Error**: `#ef4444` (Red)
- **Warning**: `#f59e0b` (Orange)

### Typography

- **Headings**: System font stack
- **Body**: System font stack
- **Code**: Monospace font stack

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## 🙋 Questions?

If you have questions, feel free to:

- Open an issue with the `question` label
- Join our community discussions
- Contact the maintainers

## 🎉 Recognition

Contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md for their contributions
- GitHub contributors page

Thank you for contributing! 🚀