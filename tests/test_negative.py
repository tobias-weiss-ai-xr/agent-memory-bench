"""Negative tests: verify that invalid tasks are rejected by the validator."""

import subprocess
import tempfile
import os
from pathlib import Path


def _write_and_validate(content: str) -> tuple[bool, str]:
    """Write a temp YAML file and run validate.py against its directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a subdirectory for tasks
        task_subdir = Path(tmpdir) / "tasks"
        task_subdir.mkdir()
        task_file = task_subdir / "test_task.yaml"
        task_file.write_text(content)
        
        result = subprocess.run(
            ["python3", "scripts/validate.py", str(task_subdir)],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0, result.stderr + result.stdout


def test_invalid_yaml_syntax():
    """Malformed YAML should be rejected."""
    ok, out = _write_and_validate("{bad yaml: [}")
    assert not ok, f"Malformed YAML should fail validation, got: {out[:100]}"


def test_missing_episode_key():
    """YAML without 'episode' key should be rejected."""
    ok, out = _write_and_validate("not_episode: {id: test}")
    assert not ok, f"Missing episode key should fail, got: {out[:100]}"


def test_empty_expected():
    """Episode with empty expected list should be rejected."""
    content = """episode:
  id: "TEST-001"
  cell: "factual/token-level/formation"
  query: "test?"
  expected: []
  context: "test context"
  difficulty: 1
  turn: 0
  modality: "text"
"""
    ok, out = _write_and_validate(content)
    assert not ok, f"Empty expected should fail, got: {out[:100]}"


def test_difficulty_out_of_range():
    """Difficulty outside 1-5 should be flagged."""
    content = """episode:
  id: "TEST-002"
  cell: "factual/token-level/formation"
  query: "test?"
  expected: ["answer"]
  context: "test context"
  difficulty: 99
  turn: 0
  modality: "text"
"""
    ok, _ = _write_and_validate(content)
    assert not ok, "Difficulty 99 should fail validation"


def test_invalid_cell_value():
    """Invalid cell value should be flagged."""
    content = """episode:
  id: "TEST-003"
  cell: "invalid/cell/value/extra"
  query: "test?"
  expected: ["answer"]
  context: "test context"
  difficulty: 1
  turn: 0
  modality: "text"
"""
    ok, _ = _write_and_validate(content)
    assert not ok, "Invalid cell should fail validation"


def test_missing_query():
    """Episode without query should fail."""
    content = """episode:
  id: "TEST-004"
  cell: "factual/token-level/formation"
  expected: ["answer"]
  context: "test"
  difficulty: 1
  turn: 0
  modality: "text"
"""
    ok, _ = _write_and_validate(content)
    assert not ok, "Missing query should fail validation"


def test_expected_is_not_list():
    """Expected must be a list."""
    content = """episode:
  id: "TEST-005"
  cell: "factual/token-level/formation"
  query: "test?"
  expected: "string instead of list"
  context: "test"
  difficulty: 1
  turn: 0
  modality: "text"
"""
    ok, _ = _write_and_validate(content)
    assert not ok, "Non-list expected should fail"


def test_missing_required_fields():
    """Missing multiple required fields should all be reported."""
    content = """episode:
  id: "TEST-006"
"""
    ok, out = _write_and_validate(content)
    assert not ok, "Missing fields should fail"
    # Should report all missing fields
    for field in ["cell", "query", "expected", "context", "difficulty", "turn", "modality"]:
        assert field in out, f"Should report missing '{field}', got: {out[:200]}"


def test_wrong_directory():
    """File in wrong directory should fail."""
    content = """episode:
  id: "TEST-007"
  cell: "factual/token-level/formation"
  query: "test?"
  expected: ["answer"]
  context: "test"
  difficulty: 1
  turn: 0
  modality: "text"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Put the file in the WRONG subdirectory (experiential/token-level instead of factual/token-level)
        wrong_dir = Path(tmpdir) / "tasks" / "experiential" / "token-level" / "formation"
        wrong_dir.mkdir(parents=True)
        task_file = wrong_dir / "test_task.yaml"
        task_file.write_text(content)
        
        result = subprocess.run(
            ["python3", "scripts/validate.py", str(Path(tmpdir) / "tasks")],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0, "Wrong directory should fail validation"
