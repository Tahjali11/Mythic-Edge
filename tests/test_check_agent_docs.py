from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_agent_docs.py"
SPEC = importlib.util.spec_from_file_location("check_agent_docs", MODULE_PATH)
assert SPEC is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)


def _agent_rules_text() -> str:
    role_sections = "\n".join(
        f"  {role_id}:\n    name: {role_name}"
        for role_id, (role_name, _) in checker.CANONICAL_ROLES.items()
        if role_id != "H"
    )
    prompt_required = "\n".join(f"    - {item}" for item in checker.PROMPT_SCHEMA_REQUIRED)
    handoff_required = "\n".join(f"    - {item}" for item in checker.HANDOFF_SCHEMA_REQUIRED)
    return f"""version: 2
status: active
authority_order:
  - system_and_developer
  - current_user_instruction
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - current_issue_or_problem_representation
  - current_contract
  - accepted_architecture_decision_records
  - current_handoff_or_report
  - docs/agent_threads
  - docs/templates
  - older_docs_examples_memory
architecture_decision_records:
  statuses:
    - Proposed
    - Accepted
    - Superseded
    - Deprecated
    - Rejected
roles:
{role_sections}
auxiliary_roles:
  H:
    name: Constitutional Lawyer
    normal_path_member: false
routing:
  normal_path:
    - A
    - B
    - C
    - E
    - F
    - G
prompt_schema:
  required:
{prompt_required}
handoff_schema:
  required:
{handoff_required}
"""


def _all_roles_line() -> str:
    return (
        "Thinker (A), Module Contract Writer (B), Module Implementer (C), "
        "Module Fixer (D), Module Reviewer (E), Module Submitter (F), "
        "Integration Deployer (G), and Constitutional Lawyer (H) auxiliary."
    )


def _governance_text() -> str:
    return (
        _all_roles_line()
        + "\nNever commit secrets, webhook urls, api keys, tokens, credentials, "
        "local mtga logs, failed posts, runtime status files, generated card data, "
        "or raw workbook exports. Do not move parser truth into workbook formulas, "
        "dashboard logic, apps script transport, webhook transport, or "
        "ai-generated interpretation. External tools, connectors, Google Docs, "
        "Google Sheets, and OpenAI documentation tooling are access or "
        "collaboration surfaces and must not own project truth or repo authority "
        "by default."
    )


def _constitution_text() -> str:
    return (
        _governance_text()
        + "\nAuthority: active system and developer instructions, explicit user "
        "instructions, AGENTS.md, docs/agent_rules.yml, "
        "docs/agent_constitution.md, current GitHub issue, current module "
        "contract, current implementation handoff, role-specific files, "
        "workflow templates, and older docs. Draft files under `docs/archive/` "
        "have no authority unless explicitly named. Accepted ADRs sit below "
        "active governing docs."
    )


def _workflow_text() -> str:
    return (
        _governance_text()
        + "\nA Thinker -> B Module Contract Writer -> C Module Implementer -> "
        "E Module Reviewer -> F Module Submitter -> G Integration Deployer\n"
        "Use D only as loopback. Every continuing thread needs a durable artifact, "
        "pasteable next-thread prompt, and workflow_handoff block."
    )


def _workflow_handoff_template() -> str:
    return """# Workflow Handoff

```yaml
workflow_handoff:
  repository: ""
  repository_url: ""
  issue: ""
  tracker: ""
  completed_thread: ""
  next_thread: ""
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```

Valid `next_thread` values are `A`, `B`, `C`, `D`, `E`, `F`, `G`, or `none`.
"""


def _issue_template_text() -> str:
    ids = "\n".join(f"  - type: textarea\n    id: {field_id}" for field_id in checker.ISSUE_TEMPLATE_IDS)
    return f"""name: Module workflow
body:
{ids}
  - type: textarea
    id: protected_surfaces
    attributes:
      value: Do not change workbook schema, webhook payload shape, Apps Script behavior.
"""


def _adr_readme_text(status: str = "Accepted") -> str:
    return f"""# Architecture Decision Records

## Status Values

- `Proposed`: proposed.
- `Accepted`: accepted.
- `Superseded`: superseded.
- `Deprecated`: deprecated.
- `Rejected`: rejected.

## ADR Index

| ADR | Status | Decision |
| --- | --- | --- |
| [ADR-0001: Test Decision](ADR-0001-test-decision.md) | {status} | Test decision. |
"""


def _adr_text(status: str = "Accepted", *, include_followups: bool = True) -> str:
    followups = "## Follow-Ups\n\nNone.\n" if include_followups else ""
    return f"""# ADR-0001: Test Decision

Status: {status}

Date: 2026-05-16

Decision owners / workflow role:

Related issues:

Related PRs:

Related contracts, handoffs, or review reports:

## Context

## Decision

## Scope

## Non-Goals

## Consequences

## Truth Ownership Impact

## Protected Surfaces

## Validation Or Review Evidence

## Supersedes

## Superseded By

{followups}"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_minimal_repo(root: Path) -> None:
    for relative in checker.REQUIRED_FILES:
        if relative == "docs/agent_rules.yml":
            text = _agent_rules_text()
        elif relative == "AGENTS.md":
            text = _governance_text()
        elif relative == "docs/agent_constitution.md":
            text = _constitution_text()
        elif relative == "docs/codex_module_workflow.md":
            text = _workflow_text()
        elif relative == "docs/templates/workflow_handoff.md":
            text = _workflow_handoff_template()
        elif relative == ".github/ISSUE_TEMPLATE/module_workflow.yml":
            text = _issue_template_text()
        elif relative == "docs/decisions/README.md":
            text = _adr_readme_text()
        elif relative == "docs/decisions/ADR_TEMPLATE.md":
            text = "# ADR Template\n"
        else:
            text = f"# {relative}\nworkflow_handoff\n"
        _write(root / relative, text)
    _write(root / "docs/decisions/ADR-0001-test-decision.md", _adr_text())


def test_repo_check_reports_required_shape(capsys, tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)

    assert checker.main(["--repo-root", str(tmp_path)]) == 0

    captured = capsys.readouterr()
    assert "Agent Docs Consistency Check" in captured.out
    assert "mode: repo" in captured.out
    assert "checked_files:" in captured.out
    assert "errors: 0" in captured.out
    assert "warnings: 0" in captured.out
    assert captured.out.rstrip().endswith("result: passed")


def test_warning_only_results_exit_zero(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / "docs/decisions/ADR-0001-test-decision.md",
        _adr_text(include_followups=False),
    )

    result = checker.run_check(tmp_path)

    assert result.exit_code == 0
    assert result.result == checker.RESULT_WARNING
    assert result.warnings[0].category_id == "adr_required_field_missing"


def test_error_findings_exit_one(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    (tmp_path / "docs/templates/current_status.md").unlink()

    result = checker.run_check(tmp_path)

    assert result.exit_code == 1
    assert any(finding.category_id == "missing_required_file" for finding in result.errors)


def test_invalid_repo_root_is_runtime_configuration_error(tmp_path: Path) -> None:
    result = checker.run_check(tmp_path / "missing")

    assert result.exit_code == 2
    assert result.result == checker.RESULT_ERROR


def test_findings_are_sorted_deterministically() -> None:
    result = checker.CheckResult(
        checker.MODE_REPO,
        (),
        (
            checker.Finding(checker.SEVERITY_WARNING, "z_warning", "b.md", "later"),
            checker.Finding(checker.SEVERITY_ERROR, "b_error", "b.md", "second"),
            checker.Finding(checker.SEVERITY_ERROR, "a_error", "c.md", "first"),
        ),
    )

    report = checker.render_report(
        checker.CheckResult(result.mode, result.checked_files, checker._sort_findings(result.findings)),
    )

    assert report.index("ERROR a_error") < report.index("ERROR b_error") < report.index("WARNING z_warning")


def test_missing_backticked_reference_is_error_but_url_and_anchor_are_ignored(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / "AGENTS.md",
        _governance_text()
        + "\nSee `docs/missing_authority.md`, `https://example.com/private`, and `#anchor`.",
    )

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "missing_referenced_file" for finding in result.errors)
    assert all("https://example.com" not in finding.reason for finding in result.findings)


def test_glob_references_require_at_least_one_match(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(tmp_path / "AGENTS.md", _governance_text() + "\nSee `docs/empty/*.md`.")

    result = checker.run_check(tmp_path)

    assert any("docs/empty/*.md" in finding.reason for finding in result.errors)


def test_role_registry_and_normal_path_mismatches_are_errors(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    bad_rules = _agent_rules_text().replace("name: Module Implementer", "name: Builder")
    bad_rules = bad_rules.replace("    - E\n    - F", "    - D\n    - E\n    - F")
    _write(tmp_path / "docs/agent_rules.yml", bad_rules)

    result = checker.run_check(tmp_path)
    categories = {finding.category_id for finding in result.errors}

    assert "role_registry_mismatch" in categories
    assert "normal_path_mismatch" in categories


def test_missing_d_loopback_workflow_prose_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    workflow = _workflow_text().replace(
        "Use D only as loopback. Every continuing thread needs a durable artifact, ",
        "Every continuing thread needs a durable artifact, ",
    )
    _write(tmp_path / "docs/codex_module_workflow.md", workflow)

    result = checker.run_check(tmp_path)

    assert any(
        finding.category_id == "normal_path_mismatch"
        and finding.path == "docs/codex_module_workflow.md"
        and "Codex D" in finding.reason
        for finding in result.errors
    )
    assert not any(
        finding.category_id == "normal_path_mismatch" and finding.path == "docs/agent_rules.yml"
        for finding in result.errors
    )


def test_auxiliary_role_mismatch_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    bad_rules = _agent_rules_text().replace("normal_path_member: false", "normal_path_member: true")
    _write(tmp_path / "docs/agent_rules.yml", bad_rules)

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "auxiliary_role_mismatch" for finding in result.errors)


def test_authority_order_inversion_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    bad_rules = _agent_rules_text().replace(
        "  - AGENTS.md\n  - docs/agent_rules.yml",
        "  - docs/agent_rules.yml\n  - AGENTS.md",
    )
    _write(tmp_path / "docs/agent_rules.yml", bad_rules)

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "authority_order_mismatch" for finding in result.errors)


def test_workflow_handoff_template_missing_key_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / "docs/templates/workflow_handoff.md",
        _workflow_handoff_template().replace('  branch: ""\n', ""),
    )

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "handoff_schema_mismatch" for finding in result.errors)


def test_workflow_handoff_template_missing_repository_identity_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / "docs/templates/workflow_handoff.md",
        _workflow_handoff_template().replace('  repository_url: ""\n', ""),
    )

    result = checker.run_check(tmp_path)

    assert any(
        finding.category_id == "handoff_schema_mismatch"
        and "repository_url" in finding.reason
        for finding in result.errors
    )


def test_issue_template_missing_required_field_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / ".github/ISSUE_TEMPLATE/module_workflow.yml",
        _issue_template_text().replace("    id: target_artifact\n", ""),
    )

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "prompt_schema_mismatch" for finding in result.errors)


def test_issue_template_missing_repository_identity_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(
        tmp_path / ".github/ISSUE_TEMPLATE/module_workflow.yml",
        _issue_template_text().replace("    id: repository_url\n", ""),
    )

    result = checker.run_check(tmp_path)

    assert any(
        finding.category_id == "prompt_schema_mismatch"
        and "repository_url" in finding.reason
        for finding in result.errors
    )


def test_adr_status_and_index_mismatch_are_errors(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    _write(tmp_path / "docs/decisions/README.md", _adr_readme_text(status="Proposed"))

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "adr_index_mismatch" for finding in result.errors)


def test_adr_template_is_not_treated_as_numbered_adr(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)

    result = checker.run_check(tmp_path)

    assert all("ADR_TEMPLATE" not in finding.path for finding in result.findings)


def test_missing_protected_surface_text_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    stripped = _all_roles_line() + " auxiliary external tools."
    _write(tmp_path / "AGENTS.md", stripped)
    _write(tmp_path / "docs/agent_constitution.md", stripped + "\n" + _constitution_text().split("\nAuthority:", 1)[1])
    _write(
        tmp_path / "docs/codex_module_workflow.md",
        stripped
        + "\nA Thinker -> B Module Contract Writer -> C Module Implementer -> "
        "E Module Reviewer -> F Module Submitter -> G Integration Deployer\n"
        "Use D only as loopback. Every continuing thread needs a durable artifact, "
        "pasteable next-thread prompt, and workflow_handoff block.",
    )

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "protected_surface_rule_mismatch" for finding in result.errors)


def test_missing_external_surface_boundary_is_error(tmp_path: Path) -> None:
    _write_minimal_repo(tmp_path)
    stripped = _governance_text().replace("OpenAI documentation tooling", "reference docs")
    _write(tmp_path / "AGENTS.md", stripped)
    _write(
        tmp_path / "docs/agent_constitution.md",
        _constitution_text().replace("OpenAI documentation tooling", "reference docs"),
    )
    _write(
        tmp_path / "docs/codex_module_workflow.md",
        _workflow_text().replace("OpenAI documentation tooling", "reference docs"),
    )

    result = checker.run_check(tmp_path)

    assert any(finding.category_id == "external_surface_rule_mismatch" for finding in result.errors)
