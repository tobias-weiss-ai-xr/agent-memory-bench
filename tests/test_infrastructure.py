"""Tests for AMBench infrastructure (Makefile, CI, scripts)."""

from pathlib import Path
import yaml


REPO_DIR = Path(__file__).parent.parent


def test_makefile_exists():
    """Makefile must exist with validate, test, coverage targets."""
    mf = REPO_DIR / "Makefile"
    assert mf.exists(), "Makefile not found"
    content = mf.read_text()
    for target in ["validate", "test", "coverage", "clean"]:
        assert f"{target}:" in content, f"Makefile missing '{target}' target"


def test_ci_workflow_exists():
    """GitHub Actions CI workflow must exist."""
    ci = REPO_DIR / ".github" / "workflows" / "validate.yml"
    assert ci.exists(), "CI workflow not found"
    content = ci.read_text()
    assert "make validate" in content, "CI missing validation step"
    assert "pytest" in content, "CI missing pytest step"


def test_validate_script_exists():
    """validate.py must exist and be valid Python."""
    vs = REPO_DIR / "scripts" / "validate.py"
    assert vs.exists(), "validate.py not found"
    compile(vs.read_text(), str(vs), "exec")


def test_coverage_script_exists():
    """coverage.py must exist and be valid Python."""
    cs = REPO_DIR / "scripts" / "coverage.py"
    assert cs.exists(), "coverage.py not found"
    compile(cs.read_text(), str(cs), "exec")


def test_coverage_json_up_to_date():
    """coverage-report.json must exist and be valid."""
    cj = REPO_DIR / "docs" / "coverage-report.json"
    assert cj.exists(), "coverage-report.json not found"
    import json
    with open(cj) as f:
        data = json.load(f)
    assert "total_tasks" in data
    assert "cells_covered" in data
    assert data["cells_total"] == 27
    assert data["cells_covered"] == 27


def test_readme_has_badges():
    """README must have key badges."""
    readme = (REPO_DIR / "README.md").read_text()
    for badge in ["GitHub", "GitLab", "License", "MIT"]:
        assert badge in readme, f"README missing '{badge}'"


def test_specification_exists():
    """Specification document must exist."""
    spec = REPO_DIR / "docs" / "specification.md"
    assert spec.exists(), "specification.md not found"
    content = spec.read_text()
    for section in ["Design Principles", "Taxonomy Coverage", "Evaluation Protocol"]:
        assert section in content, f"spec missing '{section}'"


def test_gaps_doc_exists():
    """Gaps analysis document must exist."""
    gaps = REPO_DIR / "docs" / "gaps-to-fill.md"
    assert gaps.exists(), "gaps-to-fill.md not found"
    assert "Tier 1" in gaps.read_text(), "gaps doc missing priority tiers"
