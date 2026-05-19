from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "generate_hardening_report.py"
SPEC = importlib.util.spec_from_file_location("generate_hardening_report", MODULE_PATH)
assert SPEC is not None
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
assert SPEC.loader is not None
SPEC.loader.exec_module(generator)


def _write(repo_root: Path, relative_path: str, text: str = "placeholder\n") -> Path:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_manifest(repo_root: Path, payload: dict) -> Path:
    path = repo_root / "evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_cli_with_no_manifest_prints_markdown_without_writing(capsys, tmp_path: Path) -> None:
    assert generator.main(["--repo-root", str(tmp_path)]) == 0

    captured = capsys.readouterr()
    output = captured.out

    assert "# Repo-Wide Hardening Status Report" in output
    assert "report_kind: repo_wide_hardening_status" in output
    assert "merge_readiness: not_decided_by_report" in output
    assert "deploy_readiness: not_decided_by_report" in output
    assert "tracker_completion: not_decided_by_report" in output
    for section in (
        "## Evidence Sources",
        "## Artifact Inventory",
        "## Completed Or Merged Items",
        "## Open Lifecycle Items",
        "## Validation Evidence",
        "## Tool Evidence",
        "## Protected Surface And Secret Scan Evidence",
        "## Pyright Advisory Evidence",
        "## Golden Fixture And Drift Baseline Status",
        "## Missing Evidence",
        "## Residual Risks",
        "## Next Recommended Role",
        "## Workflow Handoff",
    ):
        assert section in output
    assert "evidence manifest" in output
    assert "not_supplied" in output
    assert "checks passed" not in output.lower()
    assert "ready to merge" not in output.lower()
    assert not (tmp_path / generator.APPROVED_STATUS_REPORT).exists()


def test_cli_with_output_writes_approved_report(capsys, tmp_path: Path) -> None:
    target = tmp_path / generator.APPROVED_STATUS_REPORT

    assert generator.main(["--repo-root", str(tmp_path), "--output", generator.APPROVED_STATUS_REPORT]) == 0

    captured = capsys.readouterr()
    assert target.exists()
    assert target.read_text(encoding="utf-8") == captured.out
    assert "generated_status_report" in target.read_text(encoding="utf-8")


def test_cli_rejects_output_under_private_artifact_paths(capsys, tmp_path: Path) -> None:
    assert generator.main(["--repo-root", str(tmp_path), "--output", "data/status/report.md"]) == 2

    captured = capsys.readouterr()
    assert "ERROR configuration" in captured.err
    assert "docs/contract_test_reports" in captured.err
    assert not (tmp_path / "data" / "status" / "report.md").exists()


def test_malformed_manifest_exits_two(capsys, tmp_path: Path) -> None:
    manifest = tmp_path / "bad.json"
    manifest.write_text("{not-json", encoding="utf-8")

    assert generator.main(["--repo-root", str(tmp_path), "--evidence-manifest", str(manifest)]) == 2

    captured = capsys.readouterr()
    assert "malformed evidence manifest" in captured.err


def test_minimal_manifest_renders_operator_evidence(capsys, tmp_path: Path) -> None:
    manifest = _write_manifest(
        tmp_path,
        {
            "object": "mythic_edge_hardening_report_inputs",
            "schema_version": 1,
            "issues": [
                {
                    "number": 100,
                    "url": "https://github.com/Tahjali11/Mythic-Edge/issues/100",
                    "state": "open",
                    "role": "lifecycle_item",
                    "note": "Issue remains open for review.",
                    "source": "operator_supplied",
                },
            ],
            "pull_requests": [
                {
                    "number": 99,
                    "url": "https://github.com/Tahjali11/Mythic-Edge/pull/99",
                    "state": "merged",
                    "base": "codex/repo-wide-hardening-run",
                    "merge_commit": "fd23db71d4878c58359839f8499d1914b98f8326",
                    "source": "pr_metadata",
                },
            ],
            "validation": [
                {
                    "command": r"py -m pytest -q tests\test_hardening_report_generator.py",
                    "status": "passed",
                    "summary": "focused tests passed",
                    "source": "tracker_comment",
                },
            ],
            "ci": [{"context": "PR #99", "status": "passed", "source": "ci_summary"}],
            "residual_risks": [
                {"risk": "Issue #100 still needs Codex E review.", "severity": "medium", "source": "operator_supplied"},
            ],
            "next_recommended_role": "Codex E: Module Reviewer / contract-test thread",
        },
    )

    assert generator.main(["--repo-root", str(tmp_path), "--evidence-manifest", str(manifest)]) == 0

    output = capsys.readouterr().out
    assert "https://github.com/Tahjali11/Mythic-Edge/issues/100" in output
    assert "https://github.com/Tahjali11/Mythic-Edge/pull/99" in output
    assert "passed" in output
    assert "tracker_comment" in output
    assert "pr_metadata" in output
    assert "ci_summary" in output
    assert "Issue #100 still needs Codex E review." in output


def test_unsupported_manifest_statuses_render_unknown_with_warning(capsys, tmp_path: Path) -> None:
    manifest = _write_manifest(
        tmp_path,
        {
            "unexpected_field": "ignored",
            "issues": [{"number": 100, "state": "blocked"}],
            "validation": [{"command": "py tools\\generate_hardening_report.py", "status": "great"}],
        },
    )

    assert generator.main(["--repo-root", str(tmp_path), "--evidence-manifest", str(manifest)]) == 0

    output = capsys.readouterr().out
    assert "unknown" in output
    assert "Unsupported status rendered as unknown" in output
    assert "Unsupported issue or PR state rendered as unknown" in output
    assert "ignored_field: unexpected_field" in output


def test_artifact_inventory_is_sorted_and_presence_is_not_validation_success(tmp_path: Path) -> None:
    _write(tmp_path, "tools/generate_hardening_report.py")
    _write(tmp_path, "docs/contracts/repo_wide_validation_selector.md")

    artifacts = generator.collect_artifact_inventory(tmp_path)
    paths = [item.path for item in artifacts]
    by_path = {item.path: item for item in artifacts}

    assert paths == sorted(paths)
    assert by_path["tools/generate_hardening_report.py"].status == "present"
    assert by_path["docs/contracts/repo_wide_validation_selector.md"].confidence == "inferred_from_presence"
    rendered = generator.render_markdown(
        generator.build_report(repo_root=tmp_path),
    )
    assert "validation success" in rendered
    assert "checks passed" not in rendered.lower()


def test_report_redacts_private_values_from_manifest(capsys, tmp_path: Path) -> None:
    local_path = str(Path.home() / "private" / "report.txt")
    hook_value = "https://" + "script.google.com" + "/macros/s/" + ("A" * 24) + "/exec"
    workbook_value = "spreadsheet_" + "id=" + ("B" * 32)
    credential_value = "api_" + "key=" + ("C" * 24)
    raw_marker = "[" + "Client GRE" + "] " + "ClientToGRE" + "Message"
    manifest = _write_manifest(
        tmp_path,
        {
            "issues": [{"number": 100, "state": "open", "note": f"{local_path} {hook_value}"}],
            "pull_requests": [{"number": 100, "state": "draft", "base": hook_value}],
            "validation": [
                {
                    "command": "py tools\\generate_hardening_report.py",
                    "status": "advisory",
                    "summary": f"{workbook_value} {credential_value}",
                },
            ],
            "residual_risks": [{"risk": raw_marker, "severity": "medium"}],
        },
    )

    assert generator.main(["--repo-root", str(tmp_path), "--evidence-manifest", str(manifest)]) == 0

    output = capsys.readouterr().out
    assert str(Path.home()) not in output
    assert hook_value not in output
    assert "A" * 24 not in output
    assert "B" * 32 not in output
    assert "C" * 24 not in output
    assert raw_marker not in output
    assert "<redacted-local-path>" in output
    assert "<redacted-webhook-url>" in output
    assert "<redacted-workbook-or-deployment-id>" in output
    assert "<redacted-secret>" in output
    assert "<redacted-raw-log-content>" in output


def test_report_redacts_standalone_google_ids_from_manifest_values(capsys, tmp_path: Path) -> None:
    document_id = "1AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcd"
    workbook_id = "1ZyXwVuTsRqPoNmLkJiHgFeDcBa9876543210ZYXW"
    deployment_id = "AKfycbxStandaloneDeploymentValue1234567890abcdefGhIj"
    commit_hash = "fd23db71d4878c58359839f8499d1914b98f8326"
    manifest = _write_manifest(
        tmp_path,
        {
            "issues": [
                {
                    "number": 100,
                    "state": "open",
                    "note": f"operator pasted a bare document id {document_id}; commit {commit_hash}",
                },
            ],
            "pull_requests": [
                {
                    "number": 100,
                    "state": "merged",
                    "merge_commit": commit_hash,
                },
            ],
            "validation": [
                {
                    "command": "py tools\\generate_hardening_report.py",
                    "status": "advisory",
                    "summary": f"bare workbook id {workbook_id}",
                },
            ],
            "residual_risks": [
                {
                    "risk": f"operator pasted deployment id {deployment_id}",
                    "severity": "medium",
                },
            ],
        },
    )

    assert generator.main(["--repo-root", str(tmp_path), "--evidence-manifest", str(manifest)]) == 0

    output = capsys.readouterr().out
    assert document_id not in output
    assert workbook_id not in output
    assert deployment_id not in output
    assert commit_hash in output
    assert output.count("<redacted-google-id>") == 3


def test_generator_does_not_import_command_or_network_modules() -> None:
    assert "subprocess" not in generator.__dict__
    assert "urllib" not in generator.__dict__
    assert "requests" not in generator.__dict__
    assert "socket" not in generator.__dict__
