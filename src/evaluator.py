#!/usr/bin/env python3
"""
AMBench Evaluator — delegates to harness.py.

This file is kept for backward compatibility. Use harness.py directly.

Usage:
    python src/harness.py --tasks tasks/ --mock
    python src/harness.py --tasks tasks/ --model deepseek/deepseek-v4-flash
"""

import sys
from pathlib import Path

if __name__ == "__main__":
    print("NOTE: evaluator.py delegates to harness.py", file=sys.stderr)
    print("Run: python src/harness.py --help", file=sys.stderr)
    print()
    
    # Forward to harness
    import subprocess
    cmd = [sys.executable, str(Path(__file__).parent / "harness.py")] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
