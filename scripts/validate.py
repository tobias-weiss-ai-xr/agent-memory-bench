#!/usr/bin/env python3
"""Comprehensive validator for AMBench task YAML files.

Exits with code 1 if any validation error is found.
"""

import sys
import yaml
from pathlib import Path
from collections import Counter

VALID_27_CELLS = {
    f"{func}/{form}/{dyn}"
    for func in ["factual", "experiential", "working"]
    for form in ["token-level", "parametric", "latent"]
    for dyn in ["formation", "evolution", "retrieval"]
}

VALID_EXTENDED_DOMAINS = {"temporal", "multimodal", "security", "multi-agent"}
VALID_MODALITIES = {
    "text",
    "visual",
    "audio",
    "visual_to_text",
    "audio_to_text",
    "text_to_visual",
    "text_to_audio",
    "visual_to_audio",
    "audio_to_visual",
}
VALID_HIDDEN_FIELDS = {"expected_action", "judge_spec", "leak_targets"}


def validate_task(fpath: Path, data: dict) -> list:
    """Validate a single task file. Returns list of error messages."""
    errors = []

    if data is None:
        errors.append(f"{fpath}: empty file")
        return errors

    ep = data.get("episode")
    if not ep:
        errors.append(f"{fpath}: missing top-level 'episode' key")
        return errors

    # Required fields
    for field in [
        "id",
        "cell",
        "query",
        "expected",
        "context",
        "difficulty",
        "turn",
        "modality",
    ]:
        if field not in ep:
            errors.append(f"{fpath}: missing required field '{field}'")

    if errors:
        return errors

    # Episode ID
    eid = ep.get("id", "")
    if not isinstance(eid, str) or not eid.strip():
        errors.append(f"{fpath}: 'id' must be a non-empty string")

    # Cell validation
    cell = ep.get("cell", "")
    parts = cell.split("/")
    if len(parts) == 3:
        if cell not in VALID_27_CELLS:
            errors.append(f"{fpath}: invalid 27-cell value '{cell}'")
        # Check directory matches
        expected_dir = Path("tasks") / parts[0] / parts[1] / parts[2]
        if expected_dir not in fpath.parents:
            errors.append(
                f"{fpath}: cell '{cell}' but file in {fpath.parent}, expected {expected_dir}"
            )
    elif len(parts) == 2:
        if parts[0] not in VALID_EXTENDED_DOMAINS:
            errors.append(
                f"{fpath}: unknown extended domain '{parts[0]}' in cell '{cell}'"
            )
    else:
        errors.append(f"{fpath}: cell '{cell}' has {len(parts)} parts, expected 2 or 3")

    # Query
    query = ep.get("query", "")
    if not isinstance(query, str) or not query.strip():
        errors.append(f"{fpath}: 'query' must be a non-empty string")

    # Expected
    expected = ep.get("expected", [])
    if not isinstance(expected, list):
        errors.append(
            f"{fpath}: 'expected' must be a list, got {type(expected).__name__}"
        )
    elif len(expected) == 0:
        errors.append(
            f"{fpath}: 'expected' list is empty (must have at least 1 expected answer)"
        )
    else:
        for i, item in enumerate(expected):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{fpath}: expected[{i}] is not a non-empty string")

    # Difficulty
    diff = ep.get("difficulty", 0)
    if not isinstance(diff, int) or diff < 1 or diff > 5:
        errors.append(f"{fpath}: 'difficulty' must be int 1-5, got {diff}")

    # Turn
    turn = ep.get("turn", -1)
    if not isinstance(turn, int) or turn < 0:
        errors.append(f"{fpath}: 'turn' must be non-negative int, got {turn}")

    # Modality
    modality = ep.get("modality", "")
    if modality not in VALID_MODALITIES:
        errors.append(f"{fpath}: unknown modality '{modality}'")

    # Context
    ctx = ep.get("context", "")
    if not isinstance(ctx, str) or not ctx.strip():
        errors.append(f"{fpath}: 'context' must be a non-empty string")

    # Episode ID for multi-turn (optional)
    epid = ep.get("episode_id", None)
    if epid is not None:
        if not isinstance(epid, str) or not epid.strip():
            errors.append(f"{fpath}: 'episode_id' must be a non-empty string")

    # Tags (recommended but not required)
    tags = ep.get("tags", [])
    if isinstance(tags, list) and len(tags) > 0:
        if not all(isinstance(t, str) for t in tags):
            errors.append(f"{fpath}: 'tags' must contain only strings")

    # Distractors (if present)
    dist = ep.get("distractors", None)
    if dist is not None:
        if not isinstance(dist, list):
            errors.append(f"{fpath}: 'distractors' must be a list")

    # Hidden annotation fields (optional)
    hidden = ep.get("hidden", None)
    if hidden is not None:
        if not isinstance(hidden, dict):
            errors.append(
                f"{fpath}: 'hidden' must be a dict, got {type(hidden).__name__}"
            )
        else:
            for hkey in hidden:
                if hkey not in VALID_HIDDEN_FIELDS:
                    errors.append(
                        f"{fpath}: unknown hidden field '{hkey}', valid: {VALID_HIDDEN_FIELDS}"
                    )
            # Validate expected_action if present
            if "expected_action" in hidden:
                ea = hidden["expected_action"]
                if not isinstance(ea, str) or not ea.strip():
                    errors.append(
                        f"{fpath}: 'hidden.expected_action' must be a non-empty string"
                    )
            # Validate judge_spec if present
            if "judge_spec" in hidden:
                js = hidden["judge_spec"]
                if not isinstance(js, dict):
                    errors.append(f"{fpath}: 'hidden.judge_spec' must be a dict")
                else:
                    for jkey in js:
                        if not isinstance(js[jkey], str):
                            errors.append(
                                f"{fpath}: 'hidden.judge_spec.{jkey}' must be a string"
                            )
            # Validate leak_targets if present
            if "leak_targets" in hidden:
                lt = hidden["leak_targets"]
                if not isinstance(lt, list):
                    errors.append(f"{fpath}: 'hidden.leak_targets' must be a list")
                elif not all(isinstance(t, str) for t in lt):
                    errors.append(
                        f"{fpath}: 'hidden.leak_targets' must contain only strings"
                    )
            print(
                f"  WARNING: Hidden annotation fields present in {fpath} — these are excluded from agent input",
                file=sys.stderr,
            )

    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate AMBench task YAML files")
    parser.add_argument(
        "task_dir",
        nargs="?",
        type=Path,
        default=Path("tasks"),
        help="Directory containing task YAML files (default: tasks/)",
    )
    args = parser.parse_args()
    task_dir = args.task_dir
    all_files = sorted(task_dir.rglob("*.yaml"))

    all_errors = []
    id_counts = Counter()
    file_count = 0

    for fpath in all_files:
        if ".gitkeep" in fpath.name:
            continue
        file_count += 1
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            all_errors.append(f"{fpath}: YAML syntax error: {e}")
            continue
        except Exception as e:
            all_errors.append(f"{fpath}: read error: {e}")
            continue

        errors = validate_task(fpath, data)
        all_errors.extend(errors)

        # Track IDs
        ep = data.get("episode", {}) if data else {}
        eid = ep.get("id", "")
        if eid:
            id_counts[eid] += 1

    # Check for duplicate IDs
    for eid, count in id_counts.most_common():
        if count > 1:
            all_errors.append(f"Duplicate episode ID: '{eid}' ({count}x)")

    if file_count == 0 and task_dir.exists():
        all_errors.append(f"No YAML files found in {task_dir}")
    elif not task_dir.exists():
        all_errors.append(f"Directory not found: {task_dir}")

    if all_errors:
        print(
            f"Found {len(all_errors)} error(s) in {file_count} files:\n",
            file=sys.stderr,
        )
        for err in all_errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    print(f"All {file_count} tasks valid ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
