"""Tests for the AMBench evaluator and harness."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.harness import load_tasks, TaskRunner, MockClient, ReportGenerator, ProviderConfig, OpenAIClient


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


def test_provider_config_litellm():
    """--litellm flag should resolve to LiteLLM provider."""
    class Args:
        litellm = True
        api_key = "sk-test-key"
        base_url = None
        model = "gpt-4"
        mock = False
    
    api_key, base_url, model, headers = ProviderConfig.resolve(Args())
    assert api_key == "sk-test-key"
    assert "localhost" in base_url
    assert headers is not None


def test_provider_config_litellm_env():
    """LITELLM_API_KEY env var should be detected."""
    import os
    os.environ["LITELLM_API_KEY"] = "sk-litellm-env-test"
    try:
        class Args:
            litellm = False
            api_key = None
            base_url = None
            model = "deepseek/deepseek-v4-flash"
            mock = False
        api_key, base_url, model, headers = ProviderConfig.resolve(Args())
        assert api_key == "sk-litellm-env-test"
        assert "localhost:4000" in base_url
    finally:
        del os.environ["LITELLM_API_KEY"]


def test_scorer_exact_match():
    """Exact match should find expected text in response."""
    from src.harness import Scorer
    s = Scorer()
    assert s.exact_match("The answer is 42.", ["42"]) == 1.0
    assert s.exact_match("No relevant info.", ["42"]) == 0.0
    assert s.exact_match("Alice and Bob", ["Alice", "Bob"]) == 1.0


def test_scorer_keyword_match():
    """Keyword match should score partial overlap."""
    from src.harness import Scorer
    s = Scorer()
    score = s.keyword_match("The capital is Paris", ["Paris"])
    assert score > 0.3, f"Expected moderate keyword match, got {score}"
    score = s.keyword_match("Nothing related", ["Paris", "France", "capital"])
    assert score == 0.0, f"Expected 0 keyword match, got {score}"


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
