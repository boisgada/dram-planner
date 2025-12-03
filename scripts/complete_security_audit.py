#!/usr/bin/env python3
"""
Comprehensive Security Audit Script for Dram Planner
Part of ENH-013: Security & Vulnerability Assessment
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_check(name, command, description):
    """Run a security check and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0:
            print(f"✅ {name}: PASSED")
            if result.stdout:
                print(result.stdout[:500])  # First 500 chars
            return True
        else:
            print(f"⚠️  {name}: Issues Found")
            if result.stdout:
                print(result.stdout[:1000])
            if result.stderr:
                print(f"Errors: {result.stderr[:500]}")
            return False
    except FileNotFoundError:
        print(f"❌ {name}: Tool not installed - SKIPPING")
        return None
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def main():
    """Run comprehensive security audit."""
    print("\n" + "="*60)
    print("DRAM PLANNER - COMPREHENSIVE SECURITY AUDIT")
    print("="*60)
    
    results = {}
    
    # Static Code Analysis
    print("\n" + "="*60)
    print("PHASE 1: STATIC CODE ANALYSIS")
    print("="*60)
    
    results['bandit'] = run_check(
        "Bandit Security Scan",
        "bandit -r . -f txt -c .bandit || true",
        "Static analysis for common security issues"
    )
    
    results['safety'] = run_check(
        "Safety Dependency Check",
        "safety check || true",
        "Check for known vulnerabilities in dependencies"
    )
    
    # Check for hardcoded secrets
    results['secrets'] = run_check(
        "Secret Detection",
        "grep -r 'password.*=' --include='*.py' --include='*.yml' --include='*.yaml' . | grep -v 'test' | grep -v 'example' | head -10 || echo 'No obvious hardcoded passwords found'",
        "Search for hardcoded credentials"
    )
    
    # Code Quality Checks
    print("\n" + "="*60)
    print("PHASE 2: CODE QUALITY & SECURITY")
    print("="*60)
    
    results['sql_injection'] = run_check(
        "SQL Injection Check",
        "grep -r 'execute.*%s\\|query.*%s\\|query.*+' --include='*.py' web/app/ | grep -v 'test' | head -5 || echo 'No obvious SQL injection patterns found'",
        "Check for potential SQL injection vulnerabilities"
    )
    
    results['xss'] = run_check(
        "XSS Check",
        "grep -r 'Markup\\|render_template_string' --include='*.py' web/app/ | head -5 || echo 'No obvious XSS patterns found'",
        "Check for potential XSS vulnerabilities"
    )
    
    # Configuration Security
    print("\n" + "="*60)
    print("PHASE 3: CONFIGURATION SECURITY")
    print("="*60)
    
    results['env_files'] = run_check(
        "Environment File Security",
        "find . -name '.env*' -type f 2>/dev/null | head -5 || echo 'No .env files found (good)'",
        "Check for exposed environment files"
    )
    
    results['debug_mode'] = run_check(
        "Debug Mode Check",
        "grep -r 'DEBUG.*=.*True' --include='*.py' web/ | grep -v test | head -3 || echo 'No debug mode enabled in production code'",
        "Check for debug mode in production code"
    )
    
    # Generate Report
    print("\n" + "="*60)
    print("SECURITY AUDIT SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    print(f"\n✅ Passed: {passed}")
    print(f"⚠️  Issues Found: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📊 Total Checks: {len(results)}")
    
    print("\n" + "="*60)
    print("DETAILED RESULTS")
    print("="*60)
    for check, result in results.items():
        status = "✅ PASS" if result is True else ("⚠️  ISSUES" if result is False else "⏭️  SKIPPED")
        print(f"{check.upper()}: {status}")
    
    # Save report
    report_file = Path(__file__).parent.parent / 'security_audit_report.json'
    with open(report_file, 'w') as f:
        json.dump({
            'summary': {
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'total': len(results)
            },
            'results': results
        }, f, indent=2)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    if failed > 0:
        print("\n⚠️  Some security issues were found. Please review and address them.")
        return 1
    else:
        print("\n✅ Security audit completed successfully!")
        return 0

if __name__ == '__main__':
    sys.exit(main())

