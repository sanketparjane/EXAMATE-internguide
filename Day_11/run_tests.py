# Day_11/run_tests.py
"""
Test runner script for Day 11.
Executes pytest test suite and ruff linter check.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_checks():
    print("=" * 60)
    print("InternGuide Day 11 Test & Lint Suite")
    print("=" * 60)

    # 1. Run ruff check .
    print("\n[1/2] Running 'ruff check .' ...")
    ruff_res = subprocess.run([sys.executable, "-m", "ruff", "check", "."], cwd=PROJECT_ROOT)
    if ruff_res.returncode == 0:
        print("✅ Ruff linting passed with 0 errors!")
    else:
        print("❌ Ruff linting found issues.")
        return ruff_res.returncode

    # 2. Run pytest
    print("\n[2/2] Running 'pytest -v' ...")
    pytest_res = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=PROJECT_ROOT)
    if pytest_res.returncode == 0:
        print("✅ All pytest tests passed successfully!")
    else:
        print("❌ Some pytest tests failed.")
        return pytest_res.returncode

    print("\n" + "=" * 60)
    print("🎉 All Day 11 verification checks passed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(run_checks())
