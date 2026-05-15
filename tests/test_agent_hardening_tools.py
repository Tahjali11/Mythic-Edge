from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_tool(name: str):
    path = REPO_ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


check_agent_docs = _load_tool("check_agent_docs")
select_validation = _load_tool("select_validation")
check_role_scope = _load_tool("check_role_scope")
check_secret_patterns = _load_tool("check_secret_patterns")
check_local_environment = _load_tool("check_local_environment")
report_workbook_state = _load_tool("report_workbook_state")
install_mythic_edge_skill = _load_tool("install_mythic_edge_skill")


def test_agent_docs_check_passes_current_workflow_docs() -> None:
    assert check_agent_docs.check_agent_docs(REPO_ROOT) == []


def test_validation_selector_matches_workflow_and_parser_surfaces() -> None:
    matrix = select_validation.load_matrix(REPO_ROOT / "docs" / "validation_matrix.json")

    baseline, matched = select_validation.select_validation(
        matrix,
        (
            "docs/agent_constitution.md",
            "src/mythic_edge_parser/app/state.py",
        ),
        base="origin/main",
    )

    assert any("check_protected_surfaces.py" in command for command, _reason in baseline)
    assert {surface.surface_id for surface in matched} >= {"agent_workflow_docs", "parser_truth_core"}


def test_role_scope_blocks_reviewer_from_mutating_implementation() -> None:
    findings = check_role_scope.check_role_scope(
        "E",
        ("src/mythic_edge_parser/app/state.py", "docs/contract_test_reports/example.md"),
    )

    assert any("outside role E scope" in finding.message for finding in findings)
    assert not check_role_scope.check_role_scope("E", ("docs/contract_test_reports/example.md",))


def test_role_scope_blocks_constitutional_lawyer_from_mutating_authority_docs() -> None:
    findings = check_role_scope.check_role_scope(
        "H",
        ("docs/agent_constitution.md", "docs/problem_representations/agent_constitution_next.md"),
    )

    assert any("outside role H scope" in finding.message for finding in findings)
    assert not check_role_scope.check_role_scope("H", ("docs/problem_representations/agent_constitution_next.md",))


def test_secret_pattern_scanner_flags_realistic_webhook_but_allows_placeholders(tmp_path: Path) -> None:
    realistic_webhook = (
        "https://script.google.com/macros/s/"
        "AKfycb1234567890abcdefREAL"
        "/exec"
    )
    leak_path = tmp_path / "leak.txt"
    leak_path.write_text(
        f"MYTHICEDGE_SHEETS_WEBHOOK={realistic_webhook}\n",
        encoding="utf-8",
    )
    placeholder_path = tmp_path / "placeholder.txt"
    placeholder_path.write_text(
        "MYTHICEDGE_SHEETS_WEBHOOK=https://script.google.com/macros/s/AKfycb-example-secret-value/exec\n",
        encoding="utf-8",
    )

    leak_findings = check_secret_patterns.scan_paths(tmp_path, ("leak.txt",))
    placeholder_findings = check_secret_patterns.scan_paths(tmp_path, ("placeholder.txt",))

    assert leak_findings
    assert placeholder_findings == []


def test_local_environment_clean_clone_profile_does_not_require_local_data() -> None:
    manifest = check_local_environment.load_manifest(REPO_ROOT / "docs" / "local_artifacts_manifest.json")
    statuses = check_local_environment.inspect_artifacts(manifest, repo_root=REPO_ROOT, profile="clean_clone")

    assert statuses
    assert all(not status.required for status in statuses)


def test_workbook_state_probe_reports_repo_code_hash_without_live_state() -> None:
    report = report_workbook_state.build_report(REPO_ROOT)

    assert report.code_gs_sha256
    assert report.deployed_state == "unverified; no state JSON hash supplied"
    assert report.workbook_state == "unverified; no workbook headers supplied"


def test_workbook_state_probe_compares_supplied_state_json(tmp_path: Path) -> None:
    code_hash = report_workbook_state.build_report(REPO_ROOT).code_gs_sha256
    state_path = tmp_path / "workbook_state.json"
    state_path.write_text(
        json.dumps(
            {
                "deployed_apps_script": {"code_gs_sha256": code_hash},
                "workbook_headers": {"Match Log": [], "Game Log": []},
            },
        ),
        encoding="utf-8",
    )

    report = report_workbook_state.build_report(REPO_ROOT, state_json=state_path)

    assert report.deployed_state == "matches repo"
    assert report.findings


def test_repo_owned_skill_installer_copies_skill_to_codex_home(tmp_path: Path) -> None:
    target = install_mythic_edge_skill.install_skill(REPO_ROOT, codex_home=tmp_path)

    assert target == tmp_path / "skills" / "mythic-edge-workflow"
    assert target.joinpath("SKILL.md").exists()


def test_repo_owned_skill_installer_can_install_all_skills(tmp_path: Path) -> None:
    targets = install_mythic_edge_skill.install_all_skills(REPO_ROOT, codex_home=tmp_path)
    target_names = {target.name for target in targets}

    assert {
        "mythic-edge-workflow",
        "mythic-edge-constitution-review",
        "mythic-edge-constitutional-lawyer",
    } <= target_names
    assert tmp_path.joinpath("skills", "mythic-edge-constitution-review", "SKILL.md").exists()
    assert tmp_path.joinpath("skills", "mythic-edge-constitutional-lawyer", "SKILL.md").exists()
