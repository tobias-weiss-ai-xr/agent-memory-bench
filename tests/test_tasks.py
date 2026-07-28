"""Tests for AMBench task validation and evaluator."""

import yaml
import json
from pathlib import Path
from collections import defaultdict

TASKS_DIR = Path(__file__).parent.parent / "tasks"


def test_all_yaml_parse():
    """Every .yaml file must parse as valid YAML."""
    files = list(TASKS_DIR.rglob("*.yaml"))
    assert len(files) > 0, "No YAML files found"
    for f in files:
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            data = yaml.safe_load(fh)
        assert data is not None, f"{f}: empty or invalid YAML"


def test_all_episodes_have_required_fields():
    """Every episode must have id, cell, query, expected."""
    required = {"id", "cell", "query", "expected"}
    for f in sorted(TASKS_DIR.rglob("*.yaml")):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        missing = required - set(ep.keys())
        assert not missing, f"{f}: missing fields: {missing}"
        assert isinstance(ep["expected"], list), f"{f}: expected must be a list"
        assert len(ep["expected"]) > 0, f"{f}: expected must not be empty"


def test_all_cells_are_valid():
    """Every cell must be in the 27-cell taxonomy."""
    valid_cells = {
        f"{func}/{form}/{dyn}"
        for func in ["factual", "experiential", "working"]
        for form in ["token-level", "parametric", "latent"]
        for dyn in ["formation", "evolution", "retrieval"]
    }
    # Extended cells: any two-part cell with known domain prefix
    valid_domains = {"temporal", "multimodal", "security", "multi-agent"}
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        cell = ep.get("cell", "")
        if cell in valid_cells:
            continue
        parts = cell.split("/", 1)
        assert len(parts) == 2, f"{f}: invalid cell '{cell}'"
        assert parts[0] in valid_domains, f"{f}: invalid cell '{cell}' (unknown domain '{parts[0]}')"


def test_difficulty_in_range():
    """Difficulty must be 1-5."""
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        d = ep.get("difficulty", 0)
        assert 1 <= d <= 5, f"{f}: difficulty {d} out of range [1-5]"


def test_all_27_cells_have_at_least_one_task():
    """Every taxonomy cell must have at least one task."""
    cells = defaultdict(int)
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" in f.name:
            continue
        with open(f) as fh:
            ep = yaml.safe_load(fh).get("episode", {})
        cells[ep.get("cell", "")] += 1

    expected = {
        f"{func}/{form}/{dyn}"
        for func in ["factual", "experiential", "working"]
        for form in ["token-level", "parametric", "latent"]
        for dyn in ["formation", "evolution", "retrieval"]
    }
    missing = expected - set(cells.keys())
    assert not missing, f"Missing cells: {missing}"


def test_cross_reference_coverage_json():
    """Coverage report JSON should match actual tasks."""
    report_path = Path(__file__).parent.parent / "docs" / "coverage-report.json"
    assert report_path.exists(), "coverage-report.json not found"
    with open(report_path) as f:
        report = json.load(f)

    actual_count = 0
    for f in TASKS_DIR.rglob("*.yaml"):
        if ".gitkeep" not in f.name:
            actual_count += 1
    assert report["total_tasks"] == actual_count, (
        f"Coverage report says {report['total_tasks']}, actual is {actual_count}"
    )
    assert report["cells_total"] == 27
    assert report["cells_covered"] == 27, (
        "Not all 27 cells have tasks"
    )


def test_core_cell_tasks_count():
    """Core cell tasks + extended tasks should equal total."""
    report_path = Path(__file__).parent.parent / "docs" / "coverage-report.json"
    with open(report_path) as f:
        report = json.load(f)
    assert report["core_cell_tasks"] + report["extended_cell_tasks"] == report["total_tasks"]
    assert report["cells_total"] == 27
    assert report["cells_covered"] == 27, (
        "Not all 27 cells have tasks"
    )
