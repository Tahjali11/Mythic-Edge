from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_local_environment.py"
SPEC = importlib.util.spec_from_file_location("check_local_environment", MODULE_PATH)
assert SPEC is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "docs" / "local_artifacts_manifest.json"
REQUIRED_PROFILES = {
    "clean_clone",
    "local_developer_app",
    "analytics_development",
    "live_parser_readiness",
    "historical_import_readiness",
    "clean_install_transition_audit",
}


def _load_manifest() -> dict[str, object]:
    return checker.load_manifest(MANIFEST_PATH)


def _required_artifact_classes() -> dict[str, dict[str, str]]:
    return {
        name: {"description": name, "default_git_policy": "tracked_allowed"}
        for name in checker.REQUIRED_ARTIFACT_CLASSES
    }


def _minimal_manifest(*, path_pattern: str = "missing.txt", required: bool = True) -> dict[str, object]:
    return {
        "schema_version": checker.MANIFEST_SCHEMA_VERSION,
        "object": checker.MANIFEST_OBJECT,
        "description": "Test manifest.",
        "profiles": {
            "clean_clone": {
                "label": "Clean clone",
                "description": "Test profile.",
                "artifacts": ["required_source"],
            }
        },
        "artifact_classes": _required_artifact_classes(),
        "artifacts": [
            {
                "id": "required_source",
                "label": "Required source",
                "classification": "Repo-Owned Source Files",
                "path_scope": "repo_relative",
                "path_pattern": path_pattern,
                "git_policy": "tracked_allowed",
                "privacy": "public_repo_source",
                "profiles": {"clean_clone": {"required": required}},
                "safe_checks": ["exists", "file_kind", "git_tracked"],
                "forbidden_checks": ["read_private_contents"],
                "notes": "Test artifact.",
            }
        ],
    }


def _write_manifest(tmp_path: Path, manifest: dict[str, object]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _init_git_repo(path: Path) -> None:
    path.mkdir()
    _git(path, "init")
    _git(path, "config", "user.email", "local-test@example.invalid")
    _git(path, "config", "user.name", "Local Test")


def _git(repo_root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo_root, capture_output=True, text=True, check=True)


def _commit_file(repo_root: Path, relative_path: str, text: str) -> None:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    _git(repo_root, "add", relative_path)
    _git(repo_root, "commit", "-m", "initial test commit")


def test_manifest_has_required_schema_profiles_classes_and_artifact_fields() -> None:
    manifest = _load_manifest()

    assert manifest["schema_version"] == "local_artifacts_manifest.v1"
    assert manifest["object"] == "mythic_edge_local_artifacts_manifest"
    assert REQUIRED_PROFILES.issubset(manifest["profiles"])
    assert set(checker.REQUIRED_ARTIFACT_CLASSES).issubset(manifest["artifact_classes"])

    required_fields = {
        "id",
        "label",
        "classification",
        "path_scope",
        "path_pattern",
        "git_policy",
        "privacy",
        "profiles",
        "safe_checks",
        "forbidden_checks",
        "notes",
    }
    for artifact in manifest["artifacts"]:
        assert required_fields.issubset(artifact)
        assert artifact["path_scope"] in checker.PATH_SCOPES
        assert artifact["git_policy"] in checker.GIT_POLICIES
        assert artifact["privacy"] in checker.PRIVACY_VALUES


def test_every_profile_and_alias_references_known_artifact_ids() -> None:
    manifest = _load_manifest()
    artifact_ids = {artifact["id"] for artifact in manifest["artifacts"]}

    for profile in manifest["profiles"].values():
        assert set(profile["artifacts"]).issubset(artifact_ids)

    assert manifest["profile_aliases"]["live_parser"] == "live_parser_readiness"
    assert manifest["profile_aliases"]["analytics_dev"] == "analytics_development"


def test_unknown_profile_exits_2(capsys) -> None:
    exit_code = checker.main(["--repo-root", str(REPO_ROOT), "--profile", "not_a_profile"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "unsupported profile" in captured.err
    assert "clean_clone" in captured.err


def test_malformed_manifest_exits_2(capsys, tmp_path: Path) -> None:
    manifest_path = tmp_path / "bad_manifest.json"
    manifest_path.write_text("{", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(tmp_path),
            "--manifest",
            str(manifest_path),
            "--profile",
            "clean_clone",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid manifest JSON" in captured.err


def test_clean_clone_does_not_require_private_artifacts() -> None:
    manifest = _load_manifest()

    for artifact in manifest["artifacts"]:
        if artifact["classification"] in {"Private Local Inputs", "Private Local Outputs"}:
            settings = artifact["profiles"].get("clean_clone", {})
            assert settings.get("required") is not True


def test_tracked_env_example_is_accepted_as_clean_clone_template(capsys) -> None:
    exit_code = checker.main(["--repo-root", str(REPO_ROOT), "--profile", "clean_clone", "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    env_example = next(item for item in report["findings"] if item["artifact_id"] == "env_example_template")
    env_files = next(item for item in report["findings"] if item["artifact_id"] == "env_files")
    assert exit_code == 0
    assert env_example["severity"] == "ok"
    assert env_example["observed"] == "present_tracked"
    assert env_files["severity"] != "blocked"
    assert env_files["observed"] != "present_not_ignored"


def test_repo_gitignore_ignores_real_env_variants_but_not_env_example() -> None:
    def check_ignore(path: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "check-ignore", "-q", path],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    ignored_paths = [
        ".env",
        ".env.local",
        ".env.production",
        "frontend/.env.example",
        "src/.env.example",
        "nested/path/.env.example",
    ]

    for ignored_path in ignored_paths:
        assert check_ignore(ignored_path).returncode == 0

    not_ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".env.example"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert not_ignored.returncode == 1
    assert not_ignored.stdout == ""


def test_untracked_env_example_requires_manual_review_without_reading_values(capsys, tmp_path: Path) -> None:
    repo_root = tmp_path / "untracked_env_example"
    _init_git_repo(repo_root)
    secret_value = "example-template-value-must-not-print"
    (repo_root / ".env.example").write_text(f"MYTHICEDGE_SHEETS_WEBHOOK={secret_value}", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(repo_root),
            "--manifest",
            str(MANIFEST_PATH),
            "--profile",
            "clean_clone",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    env_example = next(item for item in report["findings"] if item["artifact_id"] == "env_example_template")
    env_files = next(item for item in report["findings"] if item["artifact_id"] == "env_files")
    assert exit_code == 0
    assert env_example["severity"] == "warning"
    assert env_example["observed"] == "present_untracked"
    assert env_files["severity"] == "blocked"
    assert env_files["observed"] == "present_not_ignored"
    assert secret_value not in captured.out
    assert "MYTHICEDGE_SHEETS_WEBHOOK" not in captured.out


def test_modified_tracked_env_example_warns_without_reading_values(capsys, tmp_path: Path) -> None:
    repo_root = tmp_path / "modified_env_example"
    _init_git_repo(repo_root)
    _commit_file(repo_root, ".env.example", "MYTHICEDGE_SHEETS_WEBHOOK=\n")
    changed_value = "changed-example-value-must-not-print"
    (repo_root / ".env.example").write_text(f"MYTHICEDGE_SHEETS_WEBHOOK={changed_value}", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(repo_root),
            "--manifest",
            str(MANIFEST_PATH),
            "--profile",
            "clean_clone",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    env_example = next(item for item in report["findings"] if item["artifact_id"] == "env_example_template")
    env_files = next(item for item in report["findings"] if item["artifact_id"] == "env_files")
    assert exit_code == 0
    assert env_example["severity"] == "warning"
    assert env_example["observed"] == "present_tracked_modified"
    assert env_files["observed"] in {"missing", "missing_ignored", "missing_not_ignored"}
    assert changed_value not in captured.out
    assert "MYTHICEDGE_SHEETS_WEBHOOK" not in captured.out


def test_dotenv_pattern_detects_env_variants_without_reading_values(capsys, tmp_path: Path) -> None:
    secret_value = "secret-value-should-not-appear"
    for env_filename in (".env", ".env.local", ".env.production"):
        repo_root = tmp_path / env_filename.replace(".", "_").strip("_")
        _init_git_repo(repo_root)
        (repo_root / env_filename).write_text(f"MYTHIC_EDGE_SECRET={secret_value}", encoding="utf-8")

        exit_code = checker.main(
            [
                "--repo-root",
                str(repo_root),
                "--manifest",
                str(MANIFEST_PATH),
                "--profile",
                "clean_clone",
                "--format",
                "json",
            ]
        )

        captured = capsys.readouterr()
        report = json.loads(captured.out)
        finding = next(item for item in report["findings"] if item["artifact_id"] == "env_files")
        assert exit_code == 0
        assert report["status"] == "blocked"
        assert finding["severity"] == "blocked"
        assert finding["observed"] == "present_not_ignored"
        assert finding["display_path"] == "<repo>\\.env*"
        assert finding["contents_read"] is False
        assert secret_value not in captured.out
        assert "MYTHIC_EDGE_SECRET" not in captured.out
        if env_filename != ".env":
            assert env_filename not in captured.out


def test_clean_install_transition_audit_profile_reports_only(capsys) -> None:
    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "clean_install_transition_audit",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    artifact_ids = {finding["artifact_id"] for finding in report["findings"]}
    assert exit_code == 0
    assert report["profile"] == "clean_install_transition_audit"
    assert report["privacy"] == {
        "raw_paths_echoed": False,
        "private_contents_read": False,
        "files_modified": False,
    }
    assert {
        "git_working_tree_state",
        "git_branch_upstream_state",
        "git_stash_count",
        "git_untracked_unignored_count",
    }.issubset(artifact_ids)


def test_transition_audit_counts_git_state_without_printing_private_names(capsys, tmp_path: Path) -> None:
    repo_root = tmp_path / "transition_repo"
    _init_git_repo(repo_root)
    _commit_file(repo_root, "tracked.txt", "base\n")
    (repo_root / "tracked.txt").write_text("changed\n", encoding="utf-8")
    _git(repo_root, "stash", "push", "-m", "local-only-review-marker")
    private_untracked_name = "local-only-review-note.txt"
    private_untracked_content = "private-payload-token-should-not-appear"
    (repo_root / private_untracked_name).write_text(f"{private_untracked_content}\n", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(repo_root),
            "--manifest",
            str(MANIFEST_PATH),
            "--profile",
            "clean_install_transition_audit",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    stash_finding = next(item for item in report["findings"] if item["artifact_id"] == "git_stash_count")
    untracked_finding = next(
        item for item in report["findings"] if item["artifact_id"] == "git_untracked_unignored_count"
    )
    assert exit_code == 0
    assert stash_finding["severity"] == "warning"
    assert stash_finding["observed"] == "manual_review_required_stash_count_1"
    assert untracked_finding["severity"] == "warning"
    assert untracked_finding["observed"] == "manual_review_required_untracked_count_1"
    assert private_untracked_name not in captured.out
    assert "local-only-review-marker" not in captured.out
    assert private_untracked_content not in captured.out


def test_missing_required_artifact_reports_blocked_but_exits_0(capsys, tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path, _minimal_manifest(path_pattern="missing.txt", required=True))

    exit_code = checker.main(
        [
            "--repo-root",
            str(tmp_path),
            "--manifest",
            str(manifest_path),
            "--profile",
            "clean_clone",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert exit_code == 0
    assert report["status"] == "blocked"
    assert report["summary"]["blocked"] == 1
    assert report["findings"][0]["observed"] == "missing_required"


def test_live_parser_blocked_readiness_still_exits_0(capsys) -> None:
    exit_code = checker.main(["--repo-root", str(REPO_ROOT), "--profile", "live_parser_readiness", "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert exit_code == 0
    assert report["status"] == "blocked"
    assert any(finding["artifact_id"] == "private_input_player_log" for finding in report["findings"])


def test_private_path_values_are_not_echoed_in_json(capsys, tmp_path: Path) -> None:
    private_path = tmp_path / "Private User" / "Player.log"
    private_path.parent.mkdir()
    private_path.write_text("private log body must not be read", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "live_parser_readiness",
            "--player-log-path",
            str(private_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(private_path) not in captured.out
    assert "Private User" not in captured.out
    assert "private log body must not be read" not in captured.out

    report = json.loads(captured.out)
    player_log = next(finding for finding in report["findings"] if finding["artifact_id"] == "private_input_player_log")
    assert player_log["display_path"] == "<configured_player_log>"
    assert player_log["observed"] == "supplied_present"
    assert player_log["contents_read"] is False
    assert player_log["path_echoed"] is False


def test_private_path_values_are_not_echoed_in_text(capsys, tmp_path: Path) -> None:
    private_path = tmp_path / "Local Operator" / "Player.log"
    private_path.parent.mkdir()
    private_path.write_text("private body", encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "live_parser",
            "--player-log-path",
            str(private_path),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "<configured_player_log>" in captured.out
    assert str(private_path) not in captured.out
    assert "Local Operator" not in captured.out
    assert "private body" not in captured.out


def test_checker_does_not_create_app_data_folders_or_sqlite_files(capsys, tmp_path: Path) -> None:
    app_data_root = tmp_path / "app-data"

    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "local_developer_app",
            "--app-data-root",
            str(app_data_root),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert exit_code == 0
    assert report["privacy"]["files_modified"] is False
    assert not app_data_root.exists()
    assert not (app_data_root / "db" / "mythic_edge.sqlite3").exists()
    assert not (app_data_root / "db" / "mythic_edge.sqlite3-wal").exists()
    assert not (app_data_root / "logs").exists()


def test_environment_variable_values_are_not_shown(monkeypatch, capsys) -> None:
    secret_value = "secret-value-should-not-appear"
    monkeypatch.setenv("MYTHICEDGE_SHEETS_WEBHOOK", secret_value)

    exit_code = checker.main(["--repo-root", str(REPO_ROOT), "--profile", "live_parser_readiness", "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    webhook_finding = next(finding for finding in report["findings"] if finding["artifact_id"] == "webhook_url_files")
    assert exit_code == 0
    assert webhook_finding["observed"] == "env_var_present"
    assert secret_value not in captured.out


def test_json_report_has_stable_top_level_fields_and_privacy_flags(capsys) -> None:
    exit_code = checker.main(["--repo-root", str(REPO_ROOT), "--profile", "clean_clone", "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert exit_code == 0
    assert set(report) == {
        "object",
        "schema_version",
        "profile",
        "requested_profile",
        "status",
        "summary",
        "privacy",
        "findings",
    }
    assert report["object"] == "mythic_edge_local_environment_report"
    assert report["schema_version"] == "local_artifact_manifest_environment_profiles.v1"
    assert report["privacy"] == {
        "raw_paths_echoed": False,
        "private_contents_read": False,
        "files_modified": False,
    }
    assert set(report["summary"]) == {"checks", "ok", "info", "warnings", "blocked", "errors"}


def test_stale_pr_65_raw_expanded_paths_are_not_reintroduced(capsys) -> None:
    raw_path = (
        "C:"
        + "\\Users\\"
        + "Local Operator"
        + "\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
    )

    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "live_parser_readiness",
            "--player-log-path",
            raw_path,
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert raw_path not in captured.out
    assert "Local Operator" not in captured.out
    assert "<configured_player_log>" in captured.out


def test_supplied_jsonl_source_checks_extension_without_reading_payload(capsys, tmp_path: Path) -> None:
    source_path = tmp_path / "events.txt"
    source_path.write_text('{"raw": "private saved event"}', encoding="utf-8")

    exit_code = checker.main(
        [
            "--repo-root",
            str(REPO_ROOT),
            "--profile",
            "historical_import_readiness",
            "--source-path",
            str(source_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    source_finding = next(
        finding for finding in report["findings"] if finding["artifact_id"] == "private_input_historical_jsonl_file"
    )
    assert exit_code == 0
    assert source_finding["observed"] == "supplied_wrong_extension"
    assert source_finding["severity"] == "blocked"
    assert str(source_path) not in captured.out
    assert "private saved event" not in captured.out
