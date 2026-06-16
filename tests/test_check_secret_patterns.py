from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_secret_patterns.py"
SPEC = importlib.util.spec_from_file_location("check_secret_patterns", MODULE_PATH)
assert SPEC is not None
scanner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scanner
assert SPEC.loader is not None
SPEC.loader.exec_module(scanner)


def _write_text(repo_root: Path, relative: str, text: str) -> Path:
    path = repo_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_bytes(repo_root: Path, relative: str, content: bytes) -> Path:
    path = repo_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def _apps_script_url() -> str:
    deployment_id = "AKfycb" + ("A" * 32)
    return f"https://script.google.com/macros/s/{deployment_id}/exec"


def _credential_value() -> str:
    return "sk_live_" + ("B" * 28)


def test_missing_base_is_usage_error(capsys) -> None:
    assert scanner.main([]) == 2

    captured = capsys.readouterr()
    assert "--base is required" in captured.err


def test_invalid_git_base_is_configuration_error(monkeypatch) -> None:
    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 128, stdout="", stderr="bad revision")

    monkeypatch.setattr(scanner.subprocess, "run", fake_run)

    result = scanner.run_changed_scan("missing/ref", repo_root="/repo")

    assert result.exit_code == 2
    assert result.error == "bad revision"
    assert "result: error" in scanner.render_report(result)


def test_collect_changed_paths_uses_contract_diff_command(monkeypatch) -> None:
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="src/example.py\n", stderr="")

    monkeypatch.setattr(scanner.subprocess, "run", fake_run)

    assert scanner.collect_changed_paths("origin/main", repo_root="/repo") == ("src/example.py",)

    command, kwargs = calls[0]
    assert command == [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        "origin/main...HEAD",
    ]
    assert kwargs["cwd"] == "/repo"


def test_paths_are_normalized_deduped_sorted_and_constrained(tmp_path: Path) -> None:
    _write_text(tmp_path, "a.txt", "safe\n")
    _write_text(tmp_path, "b.txt", "safe\n")

    paths, error = scanner.normalize_candidate_paths(
        [r".\b.txt", "a.txt", "b.txt", "../outside.txt", "a.txt"],
        repo_root=tmp_path,
    )

    assert error == ""
    assert paths == ("a.txt", "b.txt")


def test_paths_from_stdin_scans_supplied_paths(monkeypatch, capsys, tmp_path: Path) -> None:
    raw_url = _apps_script_url()
    _write_text(tmp_path, "docs/changed.md", f"WEBHOOK_URL={raw_url}\n")
    monkeypatch.setattr(scanner.sys, "stdin", io.StringIO("docs/changed.md\n"))

    assert scanner.main(["--base", "origin/main", "--repo-root", str(tmp_path), "--paths-from-stdin"]) == 1

    captured = capsys.readouterr()
    assert "FORBIDDEN live_webhook_url docs/changed.md:1" in captured.out
    assert raw_url not in captured.out
    assert "<redacted:live_webhook_url>" in captured.out


def test_all_repo_mode_is_advisory_for_forbidden_findings(tmp_path: Path) -> None:
    raw_value = _credential_value()
    _write_text(tmp_path, "src/changed.py", f"API_KEY={raw_value}\n")

    result = scanner.evaluate_paths(
        ["src/changed.py"],
        base="<not-required>",
        repo_root=tmp_path,
        mode=scanner.MODE_ALL,
    )
    report = scanner.render_report(result)

    assert result.result == scanner.RESULT_FAILED
    assert result.exit_code == 0
    assert "mode: all-repo-advisory" in report
    assert raw_value not in report


def test_live_webhook_urls_fail_with_redacted_report(tmp_path: Path) -> None:
    raw_url = _apps_script_url()
    _write_text(tmp_path, "docs/changed.md", f"url = {raw_url}\n")

    result = scanner.evaluate_paths(["docs/changed.md"], base="origin/main", repo_root=tmp_path)
    report = scanner.render_report(result)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == "live_webhook_url"
    assert raw_url not in report
    assert "<redacted:live_webhook_url>" in report


def test_credential_assignments_fail_and_redact_value(tmp_path: Path) -> None:
    raw_value = _credential_value()
    _write_text(tmp_path, "src/config_notes.txt", f"client_secret={raw_value}\n")

    result = scanner.evaluate_paths(["src/config_notes.txt"], base="origin/main", repo_root=tmp_path)
    report = scanner.render_report(result)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == "credential_value"
    assert raw_value not in report
    assert "client_secret=<redacted:credential_value>" in report


def test_environment_lookup_credential_assignments_do_not_fail(tmp_path: Path) -> None:
    _write_text(
        tmp_path,
        "src/config.py",
        "\n".join(
            (
                'WEBHOOK_URL = _env_text("MYTHICEDGE_SHEETS_WEBHOOK", DEFAULT_WEBHOOK_URL)',
                'LEGACY_WEBHOOK_URL = os.environ.get("MYTHICEDGE_SHEETS_WEBHOOK", "")',
                "webhook_url=self.webhook_var.get(),",
            )
        ),
    )

    result = scanner.evaluate_paths(["src/config.py"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 0
    assert result.forbidden == ()


def test_placeholder_secret_references_warn_without_failing(tmp_path: Path) -> None:
    _write_text(tmp_path, "docs/example.md", "API_KEY=<placeholder-token>\n")

    result = scanner.evaluate_paths(["docs/example.md"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 0
    assert result.forbidden == ()
    assert result.warnings[0].category_id == "placeholder_secret_reference"


def test_private_user_paths_fail_with_username_redacted(tmp_path: Path) -> None:
    local_user = "local" + "operator"
    raw_path = f"/Users/{local_user}/Library/Logs/MTGA/Player.log"
    _write_text(tmp_path, "docs/private_path.md", f"log_path={raw_path}\n")

    result = scanner.evaluate_paths(["docs/private_path.md"], base="origin/main", repo_root=tmp_path)
    report = scanner.render_report(result)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == "private_local_path"
    assert local_user not in report
    assert "/Users/<redacted>/..." in report


def test_windows_profile_path_with_spaced_username_is_fully_redacted(tmp_path: Path) -> None:
    local_user = "Local Operator"
    raw_path = f"C:\\Users\\{local_user}\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
    _write_text(tmp_path, "docs/windows_private_path.md", f"log_path={raw_path}\n")

    result = scanner.evaluate_paths(
        ["docs/windows_private_path.md"],
        base="origin/main",
        repo_root=tmp_path,
    )
    report = scanner.render_report(result)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == "private_local_path"
    assert raw_path not in report
    assert local_user not in report
    assert "Local" not in report
    assert "Operator" not in report
    assert "C:\\Users\\<redacted>\\..." in report


def test_raw_player_log_marker_outside_fixture_fails(tmp_path: Path) -> None:
    marker = "[Unity" + "CrossThreadLogger]"
    _write_text(tmp_path, "docs/raw_log.txt", f"{marker}STATE CHANGED {{}}\n")

    result = scanner.evaluate_paths(["docs/raw_log.txt"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == "raw_player_log_content"


def test_sanitized_fixture_marker_does_not_fail(tmp_path: Path) -> None:
    marker = "[Client " + "GRE]"
    _write_text(
        tmp_path,
        "tests/fixtures/sanitized_slice.log",
        f"# Sanitized fixture with local-user labels\n{marker}synthetic payload\n",
    )

    result = scanner.evaluate_paths(
        ["tests/fixtures/sanitized_slice.log"],
        base="origin/main",
        repo_root=tmp_path,
    )

    assert result.exit_code == 0
    assert result.forbidden == ()
    assert result.warnings[0].category_id == "sanitized_fixture_marker"


@pytest.mark.parametrize(
    ("relative", "content", "category_id"),
    [
        ("docs/failed_payload.txt", '{"failed_posts": [{"payload": {"row": 1}}]}', "failed_post_payload"),
        ("docs/runtime_payload.txt", '{"runtime_status": {"webhook_successes": 1}}', "runtime_status_payload"),
        ("docs/generated_payload.txt", '{"oracle_id": "abc", "scryfall_uri": "local"}', "generated_data_dump"),
        ("docs/workbook_payload.txt", 'spreadsheetId="' + ("1" + ("C" * 36)) + '"', "workbook_export_marker"),
    ],
)
def test_artifact_payload_markers_have_stable_categories(
    tmp_path: Path,
    relative: str,
    content: str,
    category_id: str,
) -> None:
    _write_text(tmp_path, relative, f"{content}\n")

    result = scanner.evaluate_paths([relative], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 1
    assert result.forbidden[0].category_id == category_id


def test_python_source_references_to_status_helpers_do_not_count_as_payloads(tmp_path: Path) -> None:
    _write_text(
        tmp_path,
        "tools/example.py",
        "\n".join(
            (
                "def load_runtime_status(project_root: Path) -> dict:",
                '    f"{webhook_successes} ok / {webhook_failures} failed"',
                '    return {"last_manual": format_scryfall_refresh_timestamp(value)}',
                "def open_failed_posts_folder(self) -> None:",
            )
        ),
    )

    result = scanner.evaluate_paths(["tools/example.py"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 0
    assert result.forbidden == ()


def test_binary_files_warn_as_skipped(tmp_path: Path) -> None:
    _write_bytes(tmp_path, "docs/image.bin", b"\x00\x01binary")

    result = scanner.evaluate_paths(["docs/image.bin"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 0
    assert result.warnings[0].category_id == "binary_skipped"
    assert result.skipped_paths == ("docs/image.bin",)


def test_oversized_files_warn_as_skipped(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(scanner, "MAX_SCAN_BYTES", 8)
    _write_text(tmp_path, "docs/large.txt", "safe content beyond limit\n")

    result = scanner.evaluate_paths(["docs/large.txt"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 0
    assert result.warnings[0].category_id == "oversized_skipped"


def test_decode_replacement_warns_and_still_scans(tmp_path: Path) -> None:
    raw_value = _credential_value()
    _write_bytes(tmp_path, "docs/bad_encoding.txt", b"\xff" + f"\nAPI_KEY={raw_value}\n".encode())

    result = scanner.evaluate_paths(["docs/bad_encoding.txt"], base="origin/main", repo_root=tmp_path)
    categories = [finding.category_id for finding in result.findings]

    assert result.exit_code == 1
    assert "decode_replacement_used" in categories
    assert "credential_value" in categories


def test_unreadable_changed_files_exit_error(monkeypatch, tmp_path: Path) -> None:
    _write_text(tmp_path, "docs/locked.txt", "safe\n")

    def blocked(path: Path) -> bytes:
        raise OSError("blocked")

    monkeypatch.setattr(scanner, "_read_file_bytes", blocked)

    result = scanner.evaluate_paths(["docs/locked.txt"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 2
    assert result.error == "blocked"


def test_symlinks_outside_repo_exit_error(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-secret-scan.txt"
    outside.write_text("safe\n", encoding="utf-8")
    link = tmp_path / "docs" / "outside.txt"
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation unavailable on this platform")

    result = scanner.evaluate_paths(["docs/outside.txt"], base="origin/main", repo_root=tmp_path)

    assert result.exit_code == 2
    assert "outside repository root" in result.error


def test_findings_are_sorted_by_severity_path_line_and_category(tmp_path: Path) -> None:
    raw_value = _credential_value()
    _write_text(tmp_path, "b.txt", "API_KEY=<placeholder-token>\n")
    _write_text(tmp_path, "a.txt", f"API_KEY={raw_value}\n")

    result = scanner.evaluate_paths(["b.txt", "a.txt"], base="origin/main", repo_root=tmp_path)

    assert [finding.path for finding in result.findings] == ["a.txt", "b.txt"]
    assert [finding.severity for finding in result.findings] == [
        scanner.SEVERITY_FORBIDDEN,
        scanner.SEVERITY_WARNING,
    ]
