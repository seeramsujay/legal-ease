"""
Unit tests for CI workflows, CodeRabbit configuration, and repository metadata integrity.
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_coderabbit_config_validity():
    """Verify .coderabbit.yaml exists and contains required rules."""
    config_path = REPO_ROOT / ".coderabbit.yaml"
    assert config_path.is_file(), ".coderabbit.yaml must exist in repo root"

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), ".coderabbit.yaml root must be a dict"
    reviews = data.get("reviews", {})
    auto_review = reviews.get("auto_review", {})
    assert auto_review.get("enabled") is True, "auto_review.enabled must be True"
    base_branches = auto_review.get("base_branches", [])
    for branch in ["main", "master", "dev"]:
        assert branch in base_branches, f"Branch '{branch}' missing in base_branches"


def test_super_linter_workflow_validity():
    """Verify .github/workflows/super-linter.yml exists and has required env vars."""
    workflow_path = REPO_ROOT / ".github" / "workflows" / "super-linter.yml"
    assert workflow_path.is_file(), "super-linter.yml must exist"

    with open(workflow_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "jobs" in data
    lint_job = data["jobs"].get("lint", {})
    steps = lint_job.get("steps", [])
    sl_step = next((s for s in steps if "super-linter" in s.get("uses", "")), None)
    assert sl_step is not None, "Super-Linter step not found"
    env = sl_step.get("env", {})
    assert env.get("VALIDATE_ALL_CODEBASE") is True
    assert env.get("DEFAULT_BRANCH") == "main"


def test_mega_linter_workflow_validity():
    """Verify .github/workflows/mega-linter.yml exists and has required env vars."""
    workflow_path = REPO_ROOT / ".github" / "workflows" / "mega-linter.yml"
    assert workflow_path.is_file(), "mega-linter.yml must exist"

    with open(workflow_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "jobs" in data
    ml_job = data["jobs"].get("megalinter", {})
    steps = ml_job.get("steps", [])
    ml_step = next((s for s in steps if "oxsecurity/megalinter" in s.get("uses", "")), None)
    assert ml_step is not None, "MegaLinter step not found"
    env = ml_step.get("env", {})
    assert env.get("VALIDATE_ALL_CODE_BASE") is True
    assert env.get("DEFAULT_BRANCH") == "main"
