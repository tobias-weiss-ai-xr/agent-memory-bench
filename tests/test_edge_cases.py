"""Edge case tests for AMBench task validation."""

import yaml
import json
from pathlib import Path
from collections import Counter

TASKS_DIR = Path(__file__).parent.parent / "tasks"


def test_no_episode_id_collisions():
    """Every episode ID must be unique across all tasks."""
    ids = []
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        ids.append(ep.get("id", ""))
    duplicates = [eid for eid, count in Counter(ids).items() if count > 1]
    assert not duplicates, f"Duplicate episode IDs: {duplicates}"


def test_all_expected_values_nonempty():
    """Every expected list must contain at least one non-empty string."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        expected = ep.get("expected", [])
        assert len(expected) > 0, f"{f}: expected list is empty"
        assert any(isinstance(e, str) and e.strip() for e in expected), (
            f"{f}: all expected values are empty strings"
        )


def test_difficulty_is_positive_integer():
    """Difficulty must be an integer between 1 and 5."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        d = ep.get("difficulty", 0)
        assert isinstance(d, int), f"{f}: difficulty is not an integer"
        assert 1 <= d <= 5, f"{f}: difficulty {d} out of range"


def test_all_turns_are_nonnegative():
    """Turn numbers must be >= 0."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        turn = ep.get("turn", -1)
        assert turn >= 0, f"{f}: turn {turn} is negative"


def test_context_is_nonempty():
    """Every episode must have a non-empty context string."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        ctx = ep.get("context", "")
        assert ctx and ctx.strip(), f"{f}: context is empty or missing"


def test_tags_are_nonempty_list():
    """Tags must be a non-empty list of strings."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        tags = ep.get("tags", [])
        assert isinstance(tags, list), f"{f}: tags is not a list"
        assert len(tags) > 0, f"{f}: tags is empty"
        assert all(isinstance(t, str) for t in tags), f"{f}: tags contain non-string"


def test_all_cell_references_resolve():
    """Cells that reference the 27-cell taxonomy must have matching directories."""
    valid_domains = {"temporal", "multimodal", "security", "multi-agent"}
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        cell = ep.get("cell", "")
        parts = cell.split("/")
        if len(parts) == 3:
            # 27-cell taxonomy: file should be in matching directory
            expected_dir = TASKS_DIR / parts[0] / parts[1] / parts[2]
            assert expected_dir in f.parents or f.parent == expected_dir, (
                f"{f.name}: cell '{cell}' but file not in {expected_dir}"
            )
        elif len(parts) == 2:
            # Extended cell: domain directory should exist
            assert parts[0] in valid_domains, (
                f"{f.name}: unknown extended domain '{parts[0]}'"
            )


def test_no_missing_gitkeep_in_empty_dirs():
    """Directories with no task files should have a .gitkeep."""
    for func in ["factual", "experiential", "working"]:
        for form in ["token-level", "parametric", "latent"]:
            for dyn in ["formation", "evolution", "retrieval"]:
                d = TASKS_DIR / func / form / dyn
                if d.exists():
                    yamls = [y for y in d.glob("*.yaml") if ".gitkeep" not in y.name]
                    if len(yamls) == 0:
                        assert (d / ".gitkeep").exists(), (
                            f"{d}: no task files and no .gitkeep"
                        )
