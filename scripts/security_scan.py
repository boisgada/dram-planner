#!/usr/bin/env python3
"""
Automated security scanning script for Dram Planner.
Runs Bandit (static analysis) and Safety (dependency check).
"""

import subprocess
import sys
import os
from pathlib import Path


def run_bandit():
    """Run Bandit security scanner."""
    print("=" * 60)
    print("Running Bandit Security Scan...")
    print("=" * 60)
    
    try:
        # Run bandit on the codebase
        result = subprocess.run(
            ['bandit', '-r', '.', '-f', 'txt', '--exclude', 'tests/,venv/,env/,migrations/'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Bandit exits with non-zero on high-severity issues
        return result.returncode == 0
    except FileNotFoundError:
        print("ERROR: Bandit not installed. Install with: pip install bandit")
        return False
    except Exception as e:
        print(f"ERROR running Bandit: {e}")
        return False


def run_safety():
    """Run Safety dependency vulnerability checker."""
    print("\n" + "=" * 60)
    print("Running Safety Dependency Check...")
    print("=" * 60)
    
    try:
        # Find requirements files
        project_root = Path(__file__).parent.parent
        req_files = []
        
        if (project_root / 'requirements.txt').exists():
            req_files.append(str(project_root / 'requirements.txt'))
        if (project_root / 'web' / 'requirements.txt').exists():
            req_files.append(str(project_root / 'web' / 'requirements.txt'))
        if (project_root / 'requirements-dev.txt').exists():
            req_files.append(str(project_root / 'requirements-dev.txt'))
        
        if not req_files:
            print("WARNING: No requirements.txt files found.")
            return True
        
        # Run safety check
        result = subprocess.run(
            ['safety', 'check'] + req_files,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("ERROR: Safety not installed. Install with: pip install safety")
        return False
    except Exception as e:
        print(f"ERROR running Safety: {e}")
        return False


def check_secrets():
    """Check for common secrets and credentials in code."""
    print("\n" + "=" * 60)
    print("Checking for Hardcoded Secrets...")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    secrets_found = []
    
    # Patterns to check for
    secret_patterns = [
        ('password', ['password', 'passwd', 'pwd']),
        ('api_key', ['api_key', 'apikey', 'api-key']),
        ('secret', ['secret', 'secret_key', 'secret-key']),
        ('token', ['token', 'access_token', 'refresh_token']),
    ]
    
    # Files to check
    code_extensions = ['.py', '.js', '.json', '.yml', '.yaml']
    exclude_dirs = {'tests', 'venv', 'env', '__pycache__', '.git', 'node_modules'}
    
    for file_path in project_root.rglob('*'):
        if file_path.is_file():
            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            
            # Skip if not a code file
            if file_path.suffix not in code_extensions:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern_name, patterns in secret_patterns:
                            for pattern in patterns:
                                if pattern in line and 'example' not in line and 'TODO' not in line:
                                    # Check if it's a hardcoded value (not just a variable name)
                                    if '=' in line or ':' in line:
                                        secrets_found.append((str(file_path.relative_to(project_root)), line_num, pattern_name, line.strip()[:80]))
            except Exception as e:
                pass
    
    if secrets_found:
        print("WARNING: Potential hardcoded secrets found:")
        for file_path, line_num, pattern, line in secrets_found[:10]:  # Limit output
            print(f"  {file_path}:{line_num} - {pattern} - {line}")
        if len(secrets_found) > 10:
            print(f"  ... and {len(secrets_found) - 10} more")
        return False
    else:
        print("✓ No obvious hardcoded secrets found.")
        return True


def main():
    """Run all security scans."""
    print("\n" + "=" * 60)
    print("Dram Planner Security Scan")
    print("=" * 60 + "\n")
    
    results = {
        'bandit': run_bandit(),
        'safety': run_safety(),
        'secrets': check_secrets()
    }
    
    print("\n" + "=" * 60)
    print("Security Scan Summary")
    print("=" * 60)
    for scan_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{scan_name.upper()}: {status}")
    
    # Exit with error if any scan failed
    if not all(results.values()):
        print("\n⚠️  Some security checks failed. Please review the output above.")
        sys.exit(1)
    else:
        print("\n✓ All security checks passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()

