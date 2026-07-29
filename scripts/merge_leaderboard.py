#!/usr/bin/env python3
"""Merge leaderboard submissions into ranked results.json."""

import json
import sys
from pathlib import Path

RESULTS_FILE = Path("leaderboard/results.json")
SUBMISSIONS_DIR = Path("leaderboard/submissions")


def load_results() -> list:
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    return []


def load_submissions() -> list:
    entries = []
    if not SUBMISSIONS_DIR.exists():
        return entries
    for fpath in sorted(SUBMISSIONS_DIR.glob("*.json")):
        with open(fpath) as f:
            data = json.load(f)
        entries.append(data)
    return entries


def deduplicate(entries: list) -> list:
    seen = {}
    for e in entries:
        key = (e.get("system", ""), e.get("model", ""), e.get("date", ""))
        seen[key] = e
    return list(seen.values())


def main():
    existing = load_results()
    submissions = load_submissions()

    all_entries = deduplicate(existing + submissions)
    ranked = sorted(
        all_entries, key=lambda e: e.get("scores", {}).get("overall", 0), reverse=True
    )

    output = []
    for i, entry in enumerate(ranked, 1):
        output.append({"rank": i, **entry})

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(
        f"Merged {len(submissions)} submission(s) into {len(output)} ranked entries in {RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()
