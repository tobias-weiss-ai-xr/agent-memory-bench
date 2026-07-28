"""Tests for the AMBench evaluator stub."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.evaluator import load_tasks


def test_load_tasks_returns_all():
    """load_tasks should find all valid task YAML files."""
    tasks_dir = Path(__file__).parent.parent / "tasks"
    tasks = load_tasks(tasks_dir)
    assert len(tasks) >= 50, f"Expected >=50 tasks, got {len(tasks)}"


def test_load_tasks_structure():
    """Each loaded task should have the expected structure."""
    tasks_dir = Path(__file__).parent.parent / "tasks"
    tasks = load_tasks(tasks_dir)
    for t in tasks:
        ep = t.get("episode", {})
        assert "id" in ep
        assert "cell" in ep
        assert "query" in ep
        assert "expected" in ep


def test_evaluator_output_format():
    """evaluate_agent should return a dict with status and tasks_loaded."""
    from src.evaluator import evaluate_agent
    result = evaluate_agent("dummy_cmd", [{"episode": {"id": "test"}}])
    assert isinstance(result, dict)
    assert "status" in result
    assert "tasks_loaded" in result
    assert result["tasks_loaded"] == 1


def test_coverage_json_exists():
    """Coverage report must exist and be valid JSON."""
    report_path = Path(__file__).parent.parent / "docs" / "coverage-report.json"
    assert report_path.exists()
    with open(report_path) as f:
        data = json.load(f)
    assert "total_tasks" in data
    assert "cells_covered" in data
    assert "cells_total" in data
    assert data["cells_total"] == 27
