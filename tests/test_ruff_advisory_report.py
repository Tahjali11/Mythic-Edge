from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "generate_ruff_advisory_report.py"
SPEC = importlib.util.spec_from_file_location("generate_ruff_advisory_report", MODULE_PATH)
assert SPEC is not None
reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(reporter)


def _finding(
    code: str,
    filename: str = "tools/example.py",
    message: str = "Synthetic advisory finding.",
    *,
    fix: dict | None = None,
) -> dict:
    payload = {
        "code": code,
        "filename": filename,
        "message": message,
        "location": {"row": 1, "column": 1},
    }
    if fix is not None:
        payload["fix"] = fix
    return payload


def test_build_report_classifies_exact_zero_and_nonzero_rule_codes() -> None:
    report = reporter.build_report(
        [
            _finding("F401", "tools/example.py", fix={"applicability": "safe"}),
            _finding("BLE001", "src/mythic_edge_parser/app/state.py"),
        ],
        metadata=reporter.ReportMetadata(branch_or_ref="main", commit="abc123", ruff_version="0.15.12"),
        candidate_rule_codes=("B002", "F401"),
    )

    by_code = {item["rule_code"]: item for item in report["rule_summaries"]}

    assert report["object"] == "mythic_edge_quality_ruff_advisory_report"
    assert report["schema_version"] == "quality_ruff_advisory_report.v1"
    assert report["exit_behavior"] == "advisory_exit_zero"
    assert report["totals"] == {
        "findings": 2,
        "triggered_rule_codes": 2,
        "zero_baseline_rule_codes": 1,
    }
    assert by_code["B002"]["disposition"] == "zero_baseline_candidate"
    assert by_code["F401"]["disposition"] == "advisory"
    assert by_code["F401"]["affected_paths"] == ["tools/example.py"]
    assert by_code["F401"]["autofix_available"] == "safe"
    assert by_code["BLE001"]["protected_surface_impact"] == "parser_truth_surface"
    assert by_code["BLE001"]["disposition"] == "protected_surface_review_required"
    assert report["zero_baseline_candidates"][0]["rule_code"] == "B002"


def test_broad_family_candidate_is_rejected() -> None:
    with pytest.raises(reporter.RuffAdvisoryError, match="candidate_rejected_broad_family"):
        reporter.build_report([], candidate_rule_codes=("S",))


def test_malformed_json_fails_closed() -> None:
    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_malformed_json"):
        reporter.load_ruff_json("{not-json")


def test_unsupported_rule_record_fails_closed() -> None:
    with pytest.raises(reporter.RuffAdvisoryError, match="unsupported_rule_record"):
        reporter.build_report([{"code": "S", "filename": "tools/example.py", "message": "bad"}])


def test_local_absolute_path_is_rejected() -> None:
    private_filename = str(Path.home() / "project" / "src" / "example.py")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_local_path_leak"):
        reporter.build_report([_finding("F401", private_filename)])


def test_secret_like_output_is_rejected() -> None:
    secret_text = "api_" + "key=" + ("A" * 24)

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
        reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_private_marker_output_is_rejected() -> None:
    marker = "Player" + ".log"

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_private_marker"):
        reporter.build_report([_finding("S101", "tools/example.py", marker)])


def test_metadata_local_path_output_is_rejected() -> None:
    private_scope = str(Path.home() / "project" / "src")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_local_path_leak"):
        reporter.build_report([], metadata=reporter.ReportMetadata(scan_scope=(private_scope,)))


def test_metadata_command_with_local_path_is_rejected() -> None:
    private_output = str(Path.home() / "ruff.json")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_local_path_leak"):
        reporter.build_report(
            [],
            metadata=reporter.ReportMetadata(
                commands=(f"python3 -m ruff check --output-file {private_output}",)
            ),
        )


def test_metadata_command_with_generic_absolute_path_is_rejected() -> None:
    for command in (
        "python3 -m ruff check --output-file /tmp/ruff.json",
        "python3 -m ruff check --output-file=D:\\tmp\\ruff.json",
    ):
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_local_path_leak"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(command,)))


def test_metadata_command_with_secret_or_private_marker_is_rejected() -> None:
    secret_text = "api_" + "key=" + ("A" * 24)
    marker = "Player" + ".log"

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
        reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_private_marker"):
        reporter.build_report([], metadata=reporter.ReportMetadata(commands=(marker,)))


def test_secret_like_token_forms_are_rejected() -> None:
    token_value = "A" * 24
    secret_texts = (
        "Bearer " + token_value,
        "Authorization: Bearer " + token_value,
        "--token " + token_value,
        "--api-" + "key " + token_value,
        "secret=" + token_value,
        "auth_token=" + token_value,
        "github_" + "pat_" + ("A" * 40),
        "gho_" + ("A" * 36),
    )

    for secret_text in secret_texts:
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_quoted_assignment_secret_like_token_forms_are_rejected() -> None:
    token_value = "A" * 24
    secret_texts = (
        "token=" + '"' + token_value + '"',
        "token=" + "'" + token_value + "'",
        "api_" + "key=" + '"' + token_value + '"',
        "secret = " + '"' + token_value + '"',
        "--token " + '"' + token_value + '"',
    )

    for secret_text in secret_texts:
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_credential_and_webhook_secret_like_forms_are_rejected() -> None:
    token_value = "A" * 24
    webhook_value = "https://example.invalid/hook/" + token_value
    secret_texts = (
        "credential=" + token_value,
        "credentials=" + token_value,
        "credential=" + '"' + token_value + '"',
        "web" + "hook_url=" + webhook_value,
        "web" + "hook-url=" + webhook_value,
        "web" + "hook url: " + webhook_value,
        "web" + "hook_url=" + '"' + webhook_value + '"',
    )

    for secret_text in secret_texts:
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_secret_key_assignment_forms_are_rejected() -> None:
    token_value = "A" * 24
    field_name = "secret" + "_key"
    secret_texts = (
        field_name + "=" + token_value,
        "secret" + "-key=" + token_value,
        "secret" + " key: " + token_value,
        field_name + "=" + '"' + token_value + '"',
        field_name + " := " + token_value,
        field_name + " => " + token_value,
        '"' + field_name + '": "' + token_value + '"',
        "{" + '"' + field_name + '": "' + token_value + '"' + "}",
    )

    for secret_text in secret_texts:
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_aws_style_access_key_shapes_are_rejected() -> None:
    key_suffix = "A" * 16
    secret_texts = (
        "aws_access_key_id=" + "AK" + "IA" + key_suffix,
        "aws_session_key=" + "AS" + "IA" + key_suffix,
    )

    for secret_text in secret_texts:
        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_metadata_command_with_autofix_flags_is_rejected() -> None:
    for command in (
        "ruff check --fix",
        "ruff check --fix=always",
        "ruff check --fix-only",
        "ruff check --unsafe-fixes",
        "ruff check --unsafe-fixes=true",
    ):
        with pytest.raises(reporter.RuffAdvisoryError, match="autofix_blocked_not_authorized"):
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(command,)))


def test_cli_reads_file_and_outputs_deterministic_json(tmp_path: Path) -> None:
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text(json.dumps([_finding("F401"), _finding("F401")]), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--rule-code",
            "B002",
            "--branch-or-ref",
            "main",
            "--commit",
            "abc123",
            "--ruff-version",
            "0.15.12",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(completed.stdout)
    assert report["branch_or_ref"] == "main"
    assert report["commit"] == "abc123"
    assert report["totals"]["findings"] == 2
    assert report["totals"]["triggered_rule_codes"] == 1
    assert report["totals"]["zero_baseline_rule_codes"] == 1
    assert "not CI readiness" in report["non_claims"]


def test_cli_exits_two_for_broad_family_candidate(tmp_path: Path) -> None:
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text("[]", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--rule-code",
            "S",
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "candidate_rejected_broad_family" in completed.stderr


def test_cli_input_read_error_does_not_echo_input_path() -> None:
    private_input = str(Path.home() / "missing-ruff-output.json")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            private_input,
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "measurement_blocked_input_unreadable" in completed.stderr
    assert private_input not in completed.stderr
    assert str(Path.home()) not in completed.stderr


def test_cli_rule_codes_file_read_error_does_not_echo_input_path(tmp_path: Path) -> None:
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text("[]", encoding="utf-8")
    private_input = str(Path.home() / "missing-rule-codes.json")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--rule-codes-file",
            private_input,
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "measurement_blocked_input_unreadable" in completed.stderr
    assert private_input not in completed.stderr
    assert str(Path.home()) not in completed.stderr


def test_cli_metadata_rejection_does_not_echo_private_value(tmp_path: Path) -> None:
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text("[]", encoding="utf-8")
    private_output = str(Path.home() / "ruff.json")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--command",
            f"python3 -m ruff check --output-file {private_output}",
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "measurement_blocked_local_path_leak" in completed.stderr
    assert private_output not in completed.stderr


def test_cli_secret_rejection_does_not_echo_secret_like_token(tmp_path: Path) -> None:
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text("[]", encoding="utf-8")
    token_value = "A" * 24
    command = "--token " + token_value

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--command",
            command,
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "measurement_blocked_secret_like_output" in completed.stderr
    assert token_value not in completed.stderr
