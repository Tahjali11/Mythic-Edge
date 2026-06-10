from pathlib import Path


def test_repo_checks_workflow_uses_read_only_token_permissions() -> None:
    workflow_text = Path(".github/workflows/repo-checks.yml").read_text(encoding="utf-8")

    assert "\npermissions:\n  contents: read\n" in workflow_text
    assert "contents: write" not in workflow_text
    assert "actions: write" not in workflow_text
    assert "security-events: write" not in workflow_text
