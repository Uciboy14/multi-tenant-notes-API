#!/usr/bin/env python3
"""
Test runner script for the Multi-Tenant Notes API.

This script provides convenient commands for running different types of tests
and managing the test environment.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} failed")
        if result.stderr:
            print(f"Error: {result.stderr}")
        sys.exit(1)


def check_requirements():
    """Check if required dependencies are installed."""
    try:
        import pytest
        import httpx
        import motor
        print("✅ All required dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)


def run_unit_tests():
    """Run unit tests only."""
    run_command(
        ["pytest", "tests/test_services.py", "-v"],
        "Running unit tests"
    )


def run_integration_tests():
    """Run integration tests only."""
    run_command(
        ["pytest", "tests/test_api.py", "-v"],
        "Running integration tests"
    )


def run_all_tests():
    """Run all tests."""
    run_command(
        ["pytest", "tests/", "-v", "--tb=short"],
        "Running all tests"
    )


def run_tests_with_coverage():
    """Run tests with coverage report."""
    run_command(
        ["pytest", "tests/", "--cov=app", "--cov-report=html", "--cov-report=term"],
        "Running tests with coverage"
    )


def lint_code():
    """Run code linting."""
    try:
        import flake8
        run_command(
            ["flake8", "app/", "tests/"],
            "Running code linting"
        )
    except ImportError:
        print("⚠️  flake8 not installed, skipping linting")
        print("Install with: pip install flake8")


def format_code():
    """Format code with black."""
    try:
        import black
        run_command(
            ["black", "app/", "tests/"],
            "Formatting code with black"
        )
    except ImportError:
        print("⚠️  black not installed, skipping formatting")
        print("Install with: pip install black")


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("""
🧪 Multi-Tenant Notes API Test Runner

Usage: python test_runner.py <command>

Commands:
  unit        Run unit tests only
  integration Run integration tests only
  all         Run all tests
  coverage    Run tests with coverage report
  lint        Run code linting
  format      Format code with black
  check       Check if dependencies are installed

Examples:
  python test_runner.py all
  python test_runner.py coverage
  python test_runner.py unit
        """)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    if command == "check":
        check_requirements()
    elif command == "unit":
        check_requirements()
        run_unit_tests()
    elif command == "integration":
        check_requirements()
        run_integration_tests()
    elif command == "all":
        check_requirements()
        run_all_tests()
    elif command == "coverage":
        check_requirements()
        run_tests_with_coverage()
    elif command == "lint":
        lint_code()
    elif command == "format":
        format_code()
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python test_runner.py' for usage information")
        sys.exit(1)


if __name__ == "__main__":
    main()
