"""End-to-end robustness tests for the AMBench harness."""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_DIR))


def test_empty_task_dir_exits_with_error():
    """Harness should exit with code 1 when task directory is empty."""
    with tempfile.TemporaryDirectory() as tmpdir:
        empty_tasks = Path(tmpdir) / "tasks"
        empty_tasks.mkdir()
        result = subprocess.run(
            [
                "python3",
                "src/harness.py",
                "--mock",
                "--tasks",
                str(empty_tasks),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=REPO_DIR,
        )
        assert result.returncode != 0, "Should exit with error on empty tasks"
        assert "No tasks loaded" in result.stderr or "No tasks" in result.stdout


def test_malformed_provider_config_handled():
    """Harness should handle missing API key gracefully (exit 1, message)."""
    result = subprocess.run(
        [
            "python3",
            "src/harness.py",
            "--model",
            "gpt-4",
            "--base-url",
            "https://api.openai.com/v1",
            "--max-tasks",
            "1",
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=REPO_DIR,
    )
    assert result.returncode != 0, "Should exit with error without API key"
    output_combined = result.stderr + result.stdout
    assert any(
        msg in output_combined
        for msg in ["No API key", "401", "Unauthorized", "Incorrect API key"]
    ), f"Expected auth error in: {output_combined[:200]}"


def test_network_timeout_with_retry():
    """TaskRunner should handle network timeouts gracefully without crashing."""
    from src.harness import TaskRunner

    class TimeoutClient:
        def __init__(self):
            self.model = "timeout"
            self.attempts = 0

        def complete(self, messages):
            self.attempts += 1
            raise RuntimeError("Connection timeout after 30s")

    client = TimeoutClient()
    runner = TaskRunner(client, scoring="exact")
    task = {
        "id": "timeout-test",
        "cell": "test/cell",
        "query": "test?",
        "expected": ["answer"],
        "context": "context",
        "difficulty": 1,
        "modality": "text",
    }
    result = runner.run_task(task)
    assert result.error is not None
    assert "timeout" in result.error.lower() or "Connection" in result.error
    assert result.score == 0.0
    assert client.attempts == 1


def test_max_tasks_zero_loads_all():
    """--max-tasks 0 (default) should load all tasks without error."""
    from src.harness import load_tasks

    tasks = load_tasks(REPO_DIR / "tasks")
    assert len(tasks) > 0, "Should load tasks with max-tasks=0 (default)"


def test_dual_run_and_resume_compatibility():
    """--dual-run --resume should work together without conflict."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_path = tmp.name

    resume_dir = REPO_DIR / "results"
    resume_dir.mkdir(exist_ok=True)
    resume_file = resume_dir / "resume_state.jsonl"
    if resume_file.exists():
        resume_file.unlink()

    result = subprocess.run(
        [
            "python3",
            "src/harness.py",
            "--mock",
            "--dual-run",
            "--resume",
            "--max-tasks",
            "3",
            "--output",
            output_path,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=REPO_DIR,
    )

    output = Path(output_path)
    assert output.exists(), f"Output file missing. stdout: {result.stdout}"
    with open(output) as f:
        data = json.load(f)
    assert data.get("dual_run") is True
    assert "baseline" in data
    assert "memory" in data
    output.unlink(missing_ok=True)
    if resume_file.exists():
        resume_file.unlink()


def test_resume_state_compaction_reduces_size():
    """compact_resume_state should remove duplicate entries and reduce file size."""
    from src.harness import compact_resume_state

    with tempfile.TemporaryDirectory() as tmpdir:
        resume_file = Path(tmpdir) / "resume_state.jsonl"
        entries = [
            {
                "task_id": "T1",
                "status": "ok",
                "score": 1.0,
                "response": "a",
                "timestamp": "t1",
            },
            {
                "task_id": "T2",
                "status": "ok",
                "score": 0.5,
                "response": "b",
                "timestamp": "t2",
            },
            {
                "task_id": "T1",
                "status": "ok",
                "score": 1.0,
                "response": "a",
                "timestamp": "t3",
            },
            {
                "task_id": "T3",
                "status": "error",
                "score": 0.0,
                "response": "",
                "timestamp": "t4",
            },
        ]
        with open(resume_file, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")

        before_size = resume_file.stat().st_size
        compact_resume_state(resume_file)
        after_size = resume_file.stat().st_size

        assert after_size < before_size, (
            f"Compaction should reduce size: {before_size} -> {after_size}"
        )
        with open(resume_file) as f:
            lines = [l.strip() for l in f if l.strip()]
        task_ids = [json.loads(l)["task_id"] for l in lines]
        assert len(task_ids) == len(set(task_ids)), (
            f"Duplicate task_ids after compaction: {task_ids}"
        )
        assert "T1" in task_ids
        assert "T2" in task_ids
        assert "T3" in task_ids


def test_excluded_fields_never_in_prompt():
    """EXCLUDED_FIELDS should never appear in constructed prompts, even with different templates."""
    from src.harness import EXCLUDED_FIELDS, TaskRunner

    class SpyClient:
        def __init__(self):
            self.last_messages = None
            self.model = "spy"

        def complete(self, messages):
            self.last_messages = messages
            return "response", 10, 2.0

    spy = SpyClient()
    runner = TaskRunner(
        spy, system_prompt="Custom template for testing field exclusion"
    )

    task = {
        "id": "exclude-robust",
        "cell": "test/cell",
        "query": "test query",
        "expected": ["answer"],
        "context": "test context",
        "hidden": {"expected_action": "do_secret_thing"},
        "alternatives": ["alt answer"],
        "distractors": ["distraction"],
    }
    runner.run_task(task)
    prompt_str = json.dumps(spy.last_messages)
    for field in EXCLUDED_FIELDS:
        assert field not in prompt_str, f"Excluded field '{field}' leaked into prompt"


def test_multi_turn_with_dual_run_no_conflict():
    """When both --multi-turn and --dual-run are set, multi-turn takes priority."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_path = tmp.name

    result = subprocess.run(
        [
            "python3",
            "src/harness.py",
            "--mock",
            "--multi-turn",
            "--dual-run",
            "--cells",
            "factual/parametric/formation",
            "--output",
            output_path,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=REPO_DIR,
    )

    output = Path(output_path)
    assert output.exists()
    with open(output) as f:
        data = json.load(f)
    assert data.get("multi_turn") is True
    output.unlink(missing_ok=True)


def test_compact_resume_cli():
    """--compact-resume CLI flag should run without error."""
    resume_dir = REPO_DIR / "results"
    resume_dir.mkdir(exist_ok=True)
    resume_file = resume_dir / "resume_state.jsonl"
    with open(resume_file, "w") as f:
        f.write(json.dumps({"task_id": "T1", "status": "ok", "score": 1.0}) + "\n")
        f.write(json.dumps({"task_id": "T1", "status": "ok", "score": 1.0}) + "\n")

    result = subprocess.run(
        ["python3", "src/harness.py", "--compact-resume"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0
    resume_file.unlink(missing_ok=True)
