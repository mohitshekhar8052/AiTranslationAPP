# Contributing to AI Meeting Summarizer

Thank you for your interest in contributing to the AI Meeting Summarizer project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professional communication

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/ai-meeting-summarizer.git
   cd ai-meeting-summarizer
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/ai-meeting-summarizer.git
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies** (for testing):
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Coding Standards

### Python Style Guide

We follow **PEP 8** guidelines with some modifications:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Group in order (standard library, third-party, local)
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

### Code Formatting

Use **Black** for automatic code formatting:

```bash
black .
```

### Linting

Run **flake8** to check code quality:

```bash
flake8 --max-line-length=100 --exclude=venv,__pycache__
```

### Type Hints

Use type hints where appropriate:

```python
def transcribe(audio_path: str, model_name: str = 'base') -> Tuple[str, Optional[str]]:
    """Function with type hints."""
    pass
```

### Documentation

- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Comments**: Explain "why" not "what"
- **README updates**: Update documentation when adding features

Example docstring:

```python
def summarize(text: str, max_length: int = 150) -> str:
    """
    Generate a summary from the input text.
    
    Args:
        text (str): Input text to summarize
        max_length (int): Maximum length of summary in tokens
    
    Returns:
        str: Summarized text
    
    Raises:
        ValueError: If text is empty
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Group related tests in classes

Example:

```python
class TestTranscribe:
    def test_transcribe_valid_audio_returns_text(self):
        """Test that valid audio file returns transcribed text."""
        pass
    
    def test_transcribe_invalid_path_returns_error(self):
        """Test that invalid path returns error message."""
        pass
```

### Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_transcribe.py
```

Run with coverage:

```bash
pytest --cov=summarizer --cov-report=html
```

Run only fast tests (exclude slow tests):

```bash
pytest -m "not slow"
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.slow
def test_large_file_processing():
    """This test takes a long time."""
    pass

@pytest.mark.integration
def test_full_pipeline():
    """Integration test for complete workflow."""
    pass
```

## Commit Message Guidelines

Follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(transcribe): add support for FLAC audio format

Added FLAC format to supported audio types and updated validation logic.

Closes #123
```

```
fix(summarize): handle empty text input gracefully

Previously crashed when empty text was provided. Now returns appropriate
error message.

Fixes #456
```

## Pull Request Process

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests** and ensure they pass:
   ```bash
   pytest
   ```

3. **Run linting** and fix issues:
   ```bash
   black .
   flake8
   ```

4. **Update documentation** if needed

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to related issues
   - Screenshots (if UI changes)

7. **Address review feedback** promptly

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added for new features
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main branch

## Issue Reporting

### Bug Reports

Include the following information:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Detailed steps to recreate the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, package versions
- **Screenshots**: If applicable
- **Error messages**: Full error traceback

### Feature Requests

Include:

- **Use case**: Why this feature is needed
- **Proposed solution**: How you envision it working
- **Alternatives considered**: Other approaches you've thought about
- **Additional context**: Any other relevant information

## Branch Naming Conventions

Use descriptive branch names:

- `feature/add-live-transcription`
- `fix/empty-text-crash`
- `docs/update-installation-guide`
- `refactor/simplify-export-logic`
- `test/add-integration-tests`

## Code Review Expectations

As a **reviewer**:

- Be constructive and respectful
- Focus on code quality and maintainability
- Suggest improvements, don't demand changes
- Approve when ready, request changes if needed

As a **contributor**:

- Respond to feedback promptly
- Ask questions if feedback is unclear
- Make requested changes or discuss alternatives
- Thank reviewers for their time

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the `question` label
- Reach out to project maintainers
- Check existing documentation and issues

Thank you for contributing! 🎉
