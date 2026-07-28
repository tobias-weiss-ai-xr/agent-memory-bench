#!/usr/bin/env python3
"""Validate all task YAML files in the tasks/ directory."""

import sys
import yaml
from pathlib import Path

errors = 0
count = 0
for f in sorted(Path("tasks").rglob("*.yaml")):
    if ".gitkeep" in f.name:
        continue
    count += 1
    try:
        with open(f) as fh:
            data = yaml.safe_load(fh)
        ep = data.get("episode", {})
        assert "id" in ep, f"missing id"
        assert "cell" in ep, f"missing cell"
        assert "query" in ep, f"missing query"
        assert "expected" in ep, f"missing expected"
    except Exception as e:
        print(f"  ERROR: {f}: {e}")
        errors += 1

if errors:
    print(f"Found {errors} error(s) in {count} files")
    sys.exit(1)
print(f"All {count} tasks valid")
