# Contributing to Spirits Tasting Schedule

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/spirits-tasting-schedule/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (Python version, OS)

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and motivation
   - Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the code style (see below)
   - Add tests for new features
   - Update documentation as needed
4. **Test your changes**:
   ```bash
   python3 -m pytest tests/
   ```
5. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable
6. **Push to your fork** and create a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/spirits-tasting-schedule.git
   cd spirits-tasting-schedule
   ```

2. The project uses only Python standard library (no dependencies required)

3. Run tests:
   ```bash
   python3 -m pytest tests/
   ```

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Test edge cases and error conditions

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update CHANGELOG.md for user-facing changes
- Keep examples up to date

## Project Structure

```
spirits-tasting-schedule/
├── schedule_generator.py    # Schedule generation logic
├── tasting_manager.py      # CLI tool for managing tastings
├── add_bottle.py           # Helper to add bottles
├── tests/                  # Test files
├── docs/                   # Additional documentation
└── examples/               # Example files
```

## Questions?

Feel free to open an issue for questions or discussions. We're happy to help!

Thank you for contributing! 🥃

