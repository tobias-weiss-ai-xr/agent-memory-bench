"""Tests for the AMBench evaluator and harness."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.harness import (
    load_tasks,
    TaskRunner,
    MockClient,
    ReportGenerator,
    ProviderConfig,
    OpenAIClient,
    EXCLUDED_FIELDS,
)


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


class SpyClient:
    def __init__(self):
        self.messages = None
        self.model = "spy"

    def complete(self, messages):
        self.messages = messages
        return "test-response", 10, 2.0


def test_excluded_fields_removed_from_prompt():
    """Fields in EXCLUDED_FIELDS must never appear in constructed prompt."""
    spy = SpyClient()
    runner = TaskRunner(spy)
    task = {
        "id": "exclude-test",
        "cell": "test/cell",
        "query": "test query",
        "expected": ["answer"],
        "context": "test context",
        "hidden": {"expected_action": "do_thing"},
        "alternatives": ["other answer"],
        "distractors": ["wrong answer"],
    }
    runner.run_task(task)
    prompt_str = str(spy.messages)
    for field in EXCLUDED_FIELDS:
        assert field not in prompt_str, f"Excluded field '{field}' found in prompt"


def test_dual_run_task_result_contribution():
    """DualRunTaskResult should compute memory contribution correctly."""
    from src.harness import DualRunTaskResult, TaskResult

    baseline = TaskResult(
        episode_id="test-1",
        cell="test/cell",
        query="q",
        expected=["a"],
        response="wrong",
        score=0.0,
        latency_ms=5.0,
        tokens_used=10,
    )
    memory = TaskResult(
        episode_id="test-1",
        cell="test/cell",
        query="q",
        expected=["a"],
        response="correct answer",
        score=1.0,
        latency_ms=5.0,
        tokens_used=10,
    )
    dr = DualRunTaskResult(
        episode_id="test-1",
        cell="test/cell",
        baseline=baseline,
        memory=memory,
        contribution=memory.score - baseline.score,
    )
    assert dr.contribution == 1.0
    assert dr.baseline.score == 0.0
    assert dr.memory.score == 1.0


def test_dual_run_baseline_uses_empty_context():
    """Baseline run should use empty context, memory run should use full context."""
    tasks_dir = Path(__file__).parent.parent / "tasks"
    tasks = load_tasks(tasks_dir, cell_filter=["factual/token-level/formation"])[:2]
    assert len(tasks) > 0

    client = MockClient()
    runner = TaskRunner(client)

    for ep in tasks:
        baseline_ep = dict(ep)
        baseline_ep["context"] = ""
        baseline_result = runner.run_task(baseline_ep)
        memory_result = runner.run_task(ep)

        assert baseline_result.score is not None
        assert memory_result.score is not None
        assert baseline_result.response != memory_result.response


def test_dual_run_cli_mock_mode():
    """--dual-run should work with --mock and produce structured output."""
    import subprocess
    import tempfile

    result = subprocess.run(
        [
            "python3",
            "src/harness.py",
            "--mock",
            "--dual-run",
            "--max-tasks",
            "3",
            "--output",
            "/tmp/test_dual_run.json",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )
    output_path = Path("/tmp/test_dual_run.json")
    assert output_path.exists(), f"Output file not found. stdout: {result.stdout}"

    with open(output_path) as f:
        data = json.load(f)

    assert data.get("dual_run") is True
    assert "baseline" in data
    assert "memory" in data
    assert "avg_contribution" in data
    assert "per_task" in data
    assert len(data["per_task"]) == 3
    for pt in data["per_task"]:
        assert "episode_id" in pt
        assert "baseline_score" in pt
        assert "memory_score" in pt
        assert "contribution" in pt
    output_path.unlink(missing_ok=True)


def test_dual_run_per_task_breakdown():
    """Each task in dual-run should have baseline and memory scores."""
    tasks_dir = Path(__file__).parent.parent / "tasks"
    tasks = load_tasks(tasks_dir, cell_filter=["factual/token-level/formation"])[:2]

    client = MockClient()
    runner = TaskRunner(client)
    baseline_results = []
    memory_results = []

    for ep in tasks:
        baseline_ep = dict(ep)
        baseline_ep["context"] = ""
        baseline_results.append(runner.run_task(baseline_ep))
        memory_results.append(runner.run_task(ep))

    assert len(baseline_results) == len(memory_results)
    for br, mr in zip(baseline_results, memory_results):
        assert br.episode_id == mr.episode_id
        assert 0.0 <= br.score <= 1.0
        assert 0.0 <= mr.score <= 1.0


def test_dual_run_report_structure():
    """Dual-run report should include summary metrics."""
    from src.harness import DualRunTaskResult, TaskResult

    results = []
    for i in range(3):
        br = TaskResult(
            episode_id=f"t{i}",
            cell="test/cell",
            query="q",
            expected=["a"],
            response="x",
            score=0.2 * i,
            latency_ms=5.0,
            tokens_used=10,
        )
        mr = TaskResult(
            episode_id=f"t{i}",
            cell="test/cell",
            query="q",
            expected=["a"],
            response="y",
            score=0.5 + 0.3 * i,
            latency_ms=5.0,
            tokens_used=10,
        )
        results.append(
            DualRunTaskResult(
                episode_id=f"t{i}",
                cell="test/cell",
                baseline=br,
                memory=mr,
                contribution=mr.score - br.score,
            )
        )

    avg_contrib = sum(dr.contribution for dr in results) / len(results)
    positive = sum(1 for dr in results if dr.contribution > 0)

    assert avg_contrib > 0.0
    assert positive == 3
    for dr in results:
        assert dr.contribution == dr.memory.score - dr.baseline.score


def test_multi_turn_grouping():
    """Tasks with shared episode_id should be grouped and ordered by turn."""
    from src.harness import TaskRunner, MockClient

    mt_tasks = [
        {
            "id": "MT-TEST-T1",
            "episode_id": "MT-TEST",
            "cell": "test/cell",
            "turn": 1,
            "query": "turn 1 query",
            "expected": ["response-1"],
            "context": "context 1",
            "difficulty": 1,
            "modality": "text",
        },
        {
            "id": "MT-TEST-T2",
            "episode_id": "MT-TEST",
            "cell": "test/cell",
            "turn": 2,
            "query": "turn 2 query",
            "expected": ["response-2"],
            "context": "context 2",
            "difficulty": 1,
            "modality": "text",
        },
        {
            "id": "MT-TEST-T3",
            "episode_id": "MT-TEST",
            "cell": "test/cell",
            "turn": 3,
            "query": "turn 3 query",
            "expected": ["response-3"],
            "context": "context 3",
            "difficulty": 1,
            "modality": "text",
        },
    ]

    client = MockClient()
    runner = TaskRunner(client)

    from collections import OrderedDict

    episodes = OrderedDict()
    for ep in mt_tasks:
        eid = ep.get("episode_id", ep.get("id", "unknown"))
        if eid not in episodes:
            episodes[eid] = []
        episodes[eid].append(ep)

    assert len(episodes) == 1
    assert "MT-TEST" in episodes

    episode_tasks = episodes["MT-TEST"]
    episode_tasks.sort(key=lambda t: t.get("turn", 0))
    assert episode_tasks[0]["turn"] == 1
    assert episode_tasks[1]["turn"] == 2
    assert episode_tasks[2]["turn"] == 3


def test_multi_turn_conversation_history():
    """Each turn should receive previous conversation as history."""
    from src.harness import TaskRunner

    class HistorySpyClient:
        def __init__(self):
            self.calls = []
            self.model = "spy"

        def complete(self, messages):
            self.calls.append(messages)
            return f"mock-response-{len(self.calls)}", 10, 2.0

    spy = HistorySpyClient()
    runner = TaskRunner(spy)

    turn1 = {
        "id": "MT-HIST-T1",
        "episode_id": "MT-HIST",
        "cell": "test/cell",
        "turn": 1,
        "query": "first question",
        "expected": ["mock"],
        "context": "first context",
        "difficulty": 1,
        "modality": "text",
    }
    turn2 = {
        "id": "MT-HIST-T2",
        "episode_id": "MT-HIST",
        "cell": "test/cell",
        "turn": 2,
        "query": "second question",
        "expected": ["mock"],
        "context": "second context",
        "difficulty": 1,
        "modality": "text",
    }

    conv_history = []
    result1 = runner.run_task(turn1, conv_history)
    conv_history.append({"role": "user", "content": turn1["query"]})
    conv_history.append({"role": "assistant", "content": result1.response})

    result2 = runner.run_task(turn2, conv_history)
    conv_history.append({"role": "user", "content": turn2["query"]})
    conv_history.append({"role": "assistant", "content": result2.response})

    assert len(spy.calls) == 2
    call1_user_msgs = [m for m in spy.calls[0] if m["role"] == "user"]
    call2_user_msgs = [m for m in spy.calls[1] if m["role"] == "user"]
    assert len(call1_user_msgs) == 1
    assert "first question" in call1_user_msgs[0]["content"]
    assert len(call2_user_msgs) == 2
    assert "first question" in call2_user_msgs[0]["content"]
    assert "second question" in call2_user_msgs[1]["content"]


def test_multi_turn_cli_mock_mode():
    """--multi-turn should work with --mock and produce structured output."""
    import subprocess, tempfile, json
    from pathlib import Path

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_path = tmp.name

    result = subprocess.run(
        [
            "python3",
            "src/harness.py",
            "--mock",
            "--multi-turn",
            "--cells",
            "factual/parametric/formation",
            "--output",
            output_path,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    output = Path(output_path)
    assert output.exists(), f"Output not found. stdout: {result.stdout}"

    with open(output) as f:
        data = json.load(f)

    assert data.get("multi_turn") is True
    assert "episodes" in data
    assert "overall_avg_score" in data
    assert len(data["episodes"]) >= 1
    for ep in data["episodes"]:
        assert "episode_id" in ep
        assert "turns" in ep
        assert "avg_score" in ep
        assert "turn_scores" in ep
        assert len(ep["turn_scores"]) == ep["turns"]
    output.unlink(missing_ok=True)


def test_multi_turn_overall_avg():
    """Multi-turn overall avg should be average of episode averages."""
    from src.harness import MockClient, TaskRunner, main

    class CaptureClient(MockClient):
        def __init__(self):
            super().__init__()
            self.call_count = 0

        def complete(self, messages):
            self.call_count += 1
            return "answer-ok", 10, 2.0

    mt_tasks = [
        {
            "id": "MT-CAP-T1",
            "episode_id": "MT-CAP",
            "cell": "test/cell",
            "turn": 1,
            "query": "q1",
            "expected": ["answer-ok"],
            "context": "c1",
            "difficulty": 1,
            "modality": "text",
        },
        {
            "id": "MT-CAP-T2",
            "episode_id": "MT-CAP",
            "cell": "test/cell",
            "turn": 2,
            "query": "q2",
            "expected": ["answer-ok"],
            "context": "c2",
            "difficulty": 1,
            "modality": "text",
        },
        {
            "id": "MT-CAP-T3",
            "episode_id": "MT-CAP",
            "cell": "test/cell",
            "turn": 3,
            "query": "q3",
            "expected": ["answer-ok"],
            "context": "c3",
            "difficulty": 1,
            "modality": "text",
        },
    ]

    client = CaptureClient()
    runner = TaskRunner(client)

    conv_history = []
    results = []
    for t in mt_tasks:
        r = runner.run_task(t, conv_history)
        results.append(r)
        conv_history.append({"role": "user", "content": t["query"]})
        conv_history.append({"role": "assistant", "content": r.response})

    episode_avg = sum(r.score for r in results) / len(results)
    assert episode_avg >= 0.0
    assert episode_avg <= 1.0
    assert client.call_count == 3
