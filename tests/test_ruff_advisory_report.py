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


def _write_checkout_markers(checkout: Path) -> None:
    checkout.mkdir(parents=True, exist_ok=True)
    (checkout / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
    (checkout / "AGENTS.md").write_text("# Synthetic checkout\n", encoding="utf-8")
    (checkout / ".git").write_text("gitdir: synthetic\n", encoding="utf-8")


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


def test_absolute_ruff_filename_under_measured_checkout_is_normalized(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    source_file = checkout / "src" / "package" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")

    report = reporter.build_report(
        [_finding("F401", str(source_file))],
        measured_checkout_root=checkout,
    )

    summary = report["rule_summaries"][0]
    rendered = reporter.render_json(report)

    assert summary["affected_paths"] == ["src/package/example.py"]
    assert str(source_file) not in rendered
    assert str(checkout) not in rendered


def test_absolute_ruff_filename_outside_measured_checkout_is_rejected(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    outside_file = tmp_path / "outside" / "src" / "example.py"
    outside_file.parent.mkdir(parents=True)
    outside_file.write_text("print('synthetic')\n", encoding="utf-8")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_path_outside_checkout"):
        reporter.build_report([_finding("F401", str(outside_file))], measured_checkout_root=checkout)


def test_double_slash_unc_like_ruff_filename_is_rejected(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)

    for filename in (
        "//server/share/src/example.py",
        "\\\\server\\share\\src\\example.py",
    ):
        with pytest.raises(
            reporter.RuffAdvisoryError,
            match="measurement_blocked_path_normalization_unsupported",
        ):
            reporter.build_report(
                [_finding("F401", filename)],
                measured_checkout_root=checkout,
            )


def test_uri_scheme_like_ruff_filename_is_rejected_without_echo(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)

    for scheme in ("https", "smb"):
        for separator in ("://", ":/"):
            unsafe_filename = scheme + separator + "example.invalid/src/example.py"
            with pytest.raises(
                reporter.RuffAdvisoryError,
                match="measurement_blocked_path_normalization_unsupported",
            ) as exc_info:
                reporter.build_report(
                    [_finding("F401", unsafe_filename)],
                    measured_checkout_root=checkout,
                )

            assert unsafe_filename not in str(exc_info.value)


def test_single_colon_uri_scheme_like_ruff_filename_is_rejected_without_echo(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    unsafe_filename = "https" + ":/" + "example.invalid/src/example.py"

    with pytest.raises(
        reporter.RuffAdvisoryError,
        match="measurement_blocked_path_normalization_unsupported",
    ) as exc_info:
        reporter.build_report(
            [_finding("F401", unsafe_filename)],
            measured_checkout_root=checkout,
        )

    assert unsafe_filename not in str(exc_info.value)


def test_windows_drive_like_absolute_filename_is_not_treated_as_uri() -> None:
    assert not reporter._is_uri_scheme_path("C:/workspace/Mythic-Edge/src/example.py")
    assert not reporter._is_uri_scheme_path("C:\\workspace\\Mythic-Edge\\src\\example.py")


def test_too_broad_measured_checkout_root_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    checkout = workspace / "checkout"
    _write_checkout_markers(checkout)
    sibling_file = workspace / "private-sibling" / "src" / "example.py"
    sibling_file.parent.mkdir(parents=True)
    sibling_file.write_text("print('synthetic')\n", encoding="utf-8")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_path_normalization_unsupported"):
        reporter.build_report(
            [_finding("F401", str(sibling_file))],
            measured_checkout_root=workspace,
        )


def test_generated_private_ruff_filename_under_checkout_is_rejected(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    generated_file = checkout / "_review_" / "quality" / "example.py"
    generated_file.parent.mkdir(parents=True)
    generated_file.write_text("print('synthetic')\n", encoding="utf-8")

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_local_path_leak"):
        reporter.build_report([_finding("F401", str(generated_file))], measured_checkout_root=checkout)


def test_local_path_and_private_marker_messages_are_not_emitted(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    source_file = checkout / "src" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")
    marker = "Player" + ".log"
    private_message = f"Synthetic advisory references {source_file} and {marker}."

    report = reporter.build_report(
        [_finding("F401", str(source_file), private_message)],
        measured_checkout_root=checkout,
    )
    rendered = reporter.render_json(report)

    assert report["rule_summaries"][0]["affected_paths"] == ["src/example.py"]
    assert private_message not in rendered
    assert str(source_file) not in rendered
    assert marker not in rendered


def test_private_marker_diagnostic_filename_is_counted_and_omitted(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    marker = "Player" + ".log"
    source_file = checkout / "tests" / marker / "private_marker_case.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")

    report = reporter.build_report(
        [_finding("F401", str(source_file))],
        measured_checkout_root=checkout,
    )
    summary = report["rule_summaries"][0]
    rendered = reporter.render_json(report)

    assert report["totals"]["findings"] == 1
    assert summary["rule_code"] == "F401"
    assert summary["count"] == 1
    assert summary["affected_file_count"] == 1
    assert summary["affected_paths"] == []
    assert summary["omitted_affected_path_count"] == 1
    assert summary["path_handling_policy"] == "symbolic_private_marker_filename_omission"
    assert summary["path_omission_reason"] == "path_omitted_private_marker_filename"
    assert summary["path_scope_buckets"] == ["tests"]
    assert summary["protected_surface_impact"] == "private_artifact_or_secret_surface"
    assert summary["disposition"] == "protected_surface_review_required"
    assert str(source_file) not in rendered
    assert str(checkout) not in rendered
    assert marker not in rendered
    assert source_file.name not in rendered


def test_private_marker_diagnostic_filename_outside_scan_scope_fails_closed_without_echo(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    marker = "Player" + ".log"
    source_file = checkout / "docs" / marker / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("synthetic\n", encoding="utf-8")

    with pytest.raises(
        reporter.RuffAdvisoryError,
        match="measurement_blocked_private_marker",
    ) as exc_info:
        reporter.build_report(
            [_finding("F401", str(source_file))],
            measured_checkout_root=checkout,
        )

    assert str(source_file) not in str(exc_info.value)
    assert marker not in str(exc_info.value)


def test_secret_like_output_is_rejected() -> None:
    secret_text = "api_" + "key=" + ("A" * 24)

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_secret_like_output"):
        reporter.build_report([_finding("S105", "tools/example.py", secret_text)])


def test_raw_source_or_fix_edit_messages_fail_closed_without_echo() -> None:
    raw_source_message = "Synthetic diagnostic:\n" + "def synthetic_example():\n    return 1"
    fix_edit_message = "Synthetic diagnostic:\n" + "diff --git a/src/example.py b/src/example.py"

    for message in (raw_source_message, fix_edit_message):
        with pytest.raises(
            reporter.RuffAdvisoryError,
            match="measurement_blocked_raw_source_snippet_public",
        ) as exc_info:
            reporter.build_report([_finding("S101", "tools/example.py", message)])

        assert "synthetic_example" not in str(exc_info.value)
        assert "diff --git" not in str(exc_info.value)


def test_natural_language_diagnostic_messages_are_ignored_without_echo() -> None:
    messages = (
        "Return the condition directly.",
        "Use a public collection import instead.",
        "Use a named class declaration instead.",
    )

    for message in messages:
        report = reporter.build_report([_finding("SIM103", "tools/example.py", message)])
        rendered = reporter.render_json(report)

        assert report["totals"]["findings"] == 1
        assert message not in rendered


def test_readiness_claim_message_fails_closed_without_echo() -> None:
    message = "Synthetic diagnostic says release readiness approved."

    with pytest.raises(reporter.RuffAdvisoryError, match="measurement_blocked_raw_output_public") as exc_info:
        reporter.build_report([_finding("S101", "tools/example.py", message)])

    assert message not in str(exc_info.value)


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


def test_quoted_secret_like_field_shapes_are_rejected_without_echo() -> None:
    token_value = "A" * 24
    webhook_value = "https://example.invalid/hook/" + token_value
    secret_texts = (
        '"' + "api_" + "key" + '": "' + token_value + '"',
        '"' + "api " + "key" + '": "' + token_value + '"',
        '"' + "api" + "Key" + '": "' + token_value + '"',
        '"' + "access_" + "token" + '": "' + token_value + '"',
        '"' + "client_" + "secret" + '": "' + token_value + '"',
        '"' + "web" + "hook_url" + '": "' + webhook_value + '"',
    )

    for secret_text in secret_texts:
        with pytest.raises(
            reporter.RuffAdvisoryError,
            match="measurement_blocked_secret_like_output",
        ) as metadata_exc:
            reporter.build_report([], metadata=reporter.ReportMetadata(commands=(secret_text,)))

        with pytest.raises(
            reporter.RuffAdvisoryError,
            match="measurement_blocked_secret_like_output",
        ) as finding_exc:
            reporter.build_report([_finding("S105", "tools/example.py", secret_text)])

        assert token_value not in str(metadata_exc.value)
        assert token_value not in str(finding_exc.value)
        assert webhook_value not in str(metadata_exc.value)
        assert webhook_value not in str(finding_exc.value)
        assert secret_text not in str(metadata_exc.value)
        assert secret_text not in str(finding_exc.value)


def test_raw_record_secret_like_fields_are_rejected_without_echo() -> None:
    token_value = "A" * 24
    cases = (
        {"api_" + "key": "synthetic-redacted"},
        {"api" + "Key": "synthetic-redacted"},
        {"access_" + "token": token_value},
        {"client_" + "secret": token_value},
        {"nested": {"web" + "hook_url": "https://example.invalid/hook/" + token_value}},
    )

    for extra_fields in cases:
        record = _finding("S105", "tools/example.py", "Synthetic advisory finding.")
        record.update(extra_fields)

        with pytest.raises(
            reporter.RuffAdvisoryError,
            match="measurement_blocked_secret_like_output",
        ) as exc_info:
            reporter.build_report([record])

        assert token_value not in str(exc_info.value)
        assert "synthetic-redacted" not in str(exc_info.value)


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


def test_cli_normalizes_absolute_ruff_filename_without_echoing_checkout_root(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    source_file = checkout / "tools" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text(json.dumps([_finding("F401", str(source_file))]), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--measured-checkout-root",
            str(checkout),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(completed.stdout)

    assert report["rule_summaries"][0]["affected_paths"] == ["tools/example.py"]
    assert str(source_file) not in completed.stdout
    assert str(checkout) not in completed.stdout


def test_cli_rejects_double_slash_unc_like_filename_without_echoing_path(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    unsafe_filename = "//server/share/src/private_example.py"
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text(json.dumps([_finding("F401", unsafe_filename)]), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--measured-checkout-root",
            str(checkout),
        ],
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    assert "measurement_blocked_path_normalization_unsupported" in completed.stderr
    assert unsafe_filename not in completed.stderr
    assert "server/share" not in completed.stderr


def test_cli_rejects_uri_scheme_like_filename_without_echoing_path(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)

    for scheme in ("https", "smb"):
        for separator in ("://", ":/"):
            unsafe_filename = scheme + separator + "example.invalid/src/example.py"
            ruff_json = tmp_path / f"{scheme}-{len(separator)}-ruff.json"
            ruff_json.write_text(json.dumps([_finding("F401", unsafe_filename)]), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--input",
                    str(ruff_json),
                    "--measured-checkout-root",
                    str(checkout),
                ],
                text=True,
                capture_output=True,
            )

            assert completed.returncode == 2
            assert "measurement_blocked_path_normalization_unsupported" in completed.stderr
            assert unsafe_filename not in completed.stderr
            assert "example.invalid" not in completed.stderr


def test_cli_does_not_emit_diagnostic_message_text(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    source_file = checkout / "tools" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")
    marker = "Player" + ".log"
    diagnostic_message = f"Synthetic advisory references {source_file} and {marker}."
    ruff_json = tmp_path / "ruff.json"
    ruff_json.write_text(
        json.dumps([_finding("F401", str(source_file), diagnostic_message)]),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--measured-checkout-root",
            str(checkout),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(completed.stdout)

    assert report["rule_summaries"][0]["affected_paths"] == ["tools/example.py"]
    assert diagnostic_message not in completed.stdout
    assert diagnostic_message not in completed.stderr
    assert str(source_file) not in completed.stdout
    assert marker not in completed.stdout


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
