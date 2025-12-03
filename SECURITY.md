# Security Guidelines for Dram Planner

## Automated Security Scanning

This project includes automated security scanning tools to help maintain code quality and identify potential vulnerabilities.

### Running Security Scans

#### Automated Security Scan Script
```bash
python scripts/security_scan.py
```

This script runs:
- **Bandit**: Static analysis security scanner
- **Safety**: Dependency vulnerability checker
- **Secret Detection**: Checks for hardcoded credentials

#### Individual Tools

**Bandit (Static Analysis):**
```bash
bandit -r . -c .bandit
```

**Safety (Dependencies):**
```bash
safety check
```

### Security Best Practices

1. **No Hardcoded Secrets**: Never commit passwords, API keys, or tokens to the repository
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **Input Validation**: Always validate and sanitize user input
4. **SQL Injection Prevention**: Use parameterized queries (SQLAlchemy handles this)
5. **XSS Prevention**: Flask's Jinja2 templates automatically escape content
6. **CSRF Protection**: Use Flask-WTF forms with CSRF tokens (already implemented)
7. **Password Security**: Passwords are hashed using werkzeug (already implemented)
8. **Secure Headers**: Configure security headers in production (TODO: ENH-014)

### Dependency Updates

Regularly update dependencies to patch security vulnerabilities:
```bash
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-dev.txt
safety check  # Verify no new vulnerabilities
```

### Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
1. **DO NOT** open a public GitHub issue
2. Contact the project maintainer privately
3. Allow time for the issue to be addressed before public disclosure

### CI/CD Integration

Security scans run automatically on:
- Every pull request
- Every push to main/develop branches

Reports are available as GitHub Actions artifacts.

### Configuration Files

- `.bandit`: Bandit scanner configuration
- `scripts/security_scan.py`: Automated security scanning script
- `.github/workflows/test.yml`: CI/CD security job configuration

