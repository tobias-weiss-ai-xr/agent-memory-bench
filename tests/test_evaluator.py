"""Tests for the AMBench evaluator stub."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.harness import load_tasks, TaskRunner, MockClient, ReportGenerator


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
        assert "id" in t
        assert "cell" in t
        assert "query" in t
        assert "expected" in t


def test_harness_mock_run():
    """Harness should run with mock client and produce a report."""
    tasks_dir = Path(__file__).parent.parent / "tasks"
    tasks = load_tasks(tasks_dir, cell_filter=["factual/token-level/formation"])[:3]
    assert len(tasks) > 0, "No factual/token-level/formation tasks found"
    
    client = MockClient()
    runner = TaskRunner(client)
    results = [runner.run_task(t) for t in tasks]
    
    report = ReportGenerator.generate(results, "mock-test", {})
    assert report.total_tasks == len(tasks)
    assert isinstance(report.avg_score, float)
    assert len(report.cell_results) > 0


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
