#!/usr/bin/env python3
"""Validate leaderboard submission JSON files against the template schema."""

import json
import sys
import re
from pathlib import Path

REQUIRED_SCORE_KEYS = {
    "overall",
    "factual",
    "experiential",
    "working",
    "temporal",
    "multimodal",
    "security",
    "multi-agent",
}


def validate_submission(fpath: Path) -> list:
    errors = []
    try:
        with open(fpath) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"{fpath}: invalid JSON: {e}"]

    if not isinstance(data, dict):
        return [f"{fpath}: top-level must be a JSON object"]

    system = data.get("system")
    if not isinstance(system, str) or not system.strip():
        errors.append(f"{fpath}: 'system' must be a non-empty string")

    model = data.get("model")
    if not isinstance(model, str) or not model.strip():
        errors.append(f"{fpath}: 'model' must be a non-empty string")

    scores = data.get("scores")
    if not isinstance(scores, dict):
        errors.append(f"{fpath}: 'scores' must be an object")
    else:
        for key in REQUIRED_SCORE_KEYS:
            if key not in scores:
                errors.append(f"{fpath}: missing required score key '{key}'")
        for key, val in scores.items():
            if not isinstance(val, (int, float)):
                errors.append(
                    f"{fpath}: score '{key}' must be a number, got {type(val).__name__}"
                )
            elif val < 0 or val > 1:
                errors.append(
                    f"{fpath}: score '{key}' must be between 0 and 1, got {val}"
                )

    date = data.get("date")
    if not isinstance(date, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        errors.append(f"{fpath}: 'date' must be an ISO8601 date string (YYYY-MM-DD)")

    return errors


def main():
    files = [Path(a) for a in sys.argv[1:]]
    if not files:
        print("Usage: validate_leaderboard.py <submission.json> ...", file=sys.stderr)
        sys.exit(1)

    all_errors = []
    for fpath in files:
        if not fpath.exists():
            all_errors.append(f"{fpath}: file not found")
            continue
        errors = validate_submission(fpath)
        all_errors.extend(errors)

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    print(f"All {len(files)} submission(s) valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
