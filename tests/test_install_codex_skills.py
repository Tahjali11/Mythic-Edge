from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

INSTALLER_PATH = Path(__file__).resolve().parents[1] / "tools" / "install_codex_skills.py"
SPEC = importlib.util.spec_from_file_location("install_codex_skills", INSTALLER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)
REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_skill(repo_root: Path, name: str, body: str | None = None) -> Path:
    skill_dir = repo_root / "docs" / "codex_skills" / name
    skill_dir.mkdir(parents=True)
    skill_dir.joinpath("SKILL.md").write_text(
        body
        or (
            "---\n"
            f"name: {name}\n"
            f"description: Test skill {name}.\n"
            "---\n\n"
            f"# {name}\n"
        ),
        encoding="utf-8",
    )
    return skill_dir


def _run(args: list[str], capsys: pytest.CaptureFixture[str]) -> tuple[int, str]:
    code = installer.run(args)
    return code, capsys.readouterr().out


def _offline_sync_fixture(tmp_path: Path) -> tuple[Path, Path]:
    repo_root = tmp_path / "repo"
    source = _write_skill(repo_root, "mythic-edge-role-pool")
    source.joinpath("version.txt").write_text("reviewed\n", encoding="utf-8")
    target = tmp_path / "codex-home" / "skills" / "mythic-edge-role-pool"
    shutil.copytree(source, target)
    target.joinpath("version.txt").write_text("predecessor\n", encoding="utf-8")
    return source, target


def _configure_offline_sync(
    monkeypatch: pytest.MonkeyPatch,
    source: Path,
    target: Path,
) -> None:
    source_state, source_observation = installer._offline_tree_observation(source)
    target_state, target_observation = installer._offline_tree_observation(target)
    assert source_state == "exact"
    assert source_observation is not None
    assert target_state == "exact"
    assert target_observation is not None
    monkeypatch.setattr(
        installer,
        "OFFLINE_R0_SOURCE_BINDING",
        source_observation.binding,
    )
    monkeypatch.setattr(
        installer,
        "OFFLINE_R0_PREDECESSOR_BINDING",
        target_observation.binding,
    )
    monkeypatch.setattr(
        installer,
        "_offline_r0_default_paths",
        lambda: (source, target),
    )
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: pytest.fail("offline R0 sync must not query task capability"),
    )


def _manifest_binding_from_metadata(
    rows: list[dict[str, object]],
) -> installer.TreeManifestBinding:
    encoded = (
        json.dumps(
            {
                "schema_version": "trusted_owner_role_pool_install_tree.v1",
                "rows": rows,
            },
            ensure_ascii=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )
    return installer.TreeManifestBinding(
        node_count=len(rows),
        file_count=sum(row["kind"] == "file" for row in rows),
        canonical_byte_count=len(encoded),
        sha256=hashlib.sha256(encoded).hexdigest(),
    )


def test_offline_r0_sync_app_native_tree_bindings_are_exact() -> None:
    source_root = (
        REPO_ROOT
        / installer.SKILL_SOURCE_ROOT
        / installer.TRUSTED_WINDOWS_SKILL_NAME
    )
    snapshot = installer._tree_snapshot(source_root)
    assert snapshot is not None
    source_rows = [
        {
            "path": relative_path,
            "kind": kind,
            "byte_count": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        for relative_path, kind, payload in snapshot
    ]
    historical_modified = {
        "scripts/check_pool_plan.py": (
            467960,
            "af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d",
        ),
        "scripts/check_stage3_behavioral_planning.py": (
            54224,
            "8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6",
        ),
        "scripts/test_check_pool_plan.py": (
            140448,
            "60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49",
        ),
        "scripts/test_stage3_behavioral_planning.py": (
            207666,
            "800cea8db721ef1b1ca65f41acafd5ac2e45de29f251500ba495888acf6e81ec",
        ),
    }
    historical_added = {
        "scripts/test_trusted_native_app_direct_task_adapter.py",
        "scripts/trusted_native_app_direct_task_adapter.py",
    }
    predecessor_rows = []
    for row in source_rows:
        path = row["path"]
        if path in historical_added:
            continue
        predecessor = dict(row)
        if path in historical_modified:
            byte_count, sha256 = historical_modified[path]
            predecessor["byte_count"] = byte_count
            predecessor["sha256"] = sha256
        predecessor_rows.append(predecessor)

    assert _manifest_binding_from_metadata(source_rows) == (
        installer.OFFLINE_R0_SOURCE_BINDING
    )
    assert _manifest_binding_from_metadata(predecessor_rows) == (
        installer.OFFLINE_R0_PREDECESSOR_BINDING
    )
    assert set(historical_modified) | historical_added == {
        row["path"]
        for row in source_rows
        if row["path"] in set(historical_modified) | historical_added
    }


def test_discovers_only_skill_directories_with_skill_md(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    _write_skill(repo_root, "session-checkout")
    (repo_root / "docs" / "codex_skills" / "notes").mkdir()
    (repo_root / "docs" / "codex_skills" / ".hidden").mkdir()

    discovery = installer.discover_skills(repo_root)

    assert discovery.missing is False
    assert [skill.name for skill in discovery.skills] == ["session-checkout"]


def test_list_prints_available_skills_without_writes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")
    _write_skill(repo_root, "new-workcycle")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--list",
        ],
        capsys,
    )

    assert code == installer.EXIT_SUCCESS
    assert "mode: list" in output
    assert "skill new-workcycle: action=available" in output
    assert "skill session-checkout: action=available" in output
    assert not (codex_home / "skills").exists()


def test_dry_run_all_and_one_skill_do_not_write(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")
    _write_skill(repo_root, "new-workcycle")

    all_code, all_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--dry-run",
            "--all",
        ],
        capsys,
    )
    one_code, one_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--dry-run",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert all_code == installer.EXIT_SUCCESS
    assert one_code == installer.EXIT_SUCCESS
    assert "skill new-workcycle: action=would_install" in all_output
    assert "skill session-checkout: action=would_install" in one_output
    assert "skill new-workcycle" not in one_output
    assert not (codex_home / "skills").exists()


def test_installs_missing_skill_and_reports_identical_target_as_unchanged(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")

    install_code, install_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )
    unchanged_code, unchanged_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert install_code == installer.EXIT_SUCCESS
    assert "action=installed" in install_output
    assert (codex_home / "skills" / "session-checkout" / "SKILL.md").exists()
    assert unchanged_code == installer.EXIT_SUCCESS
    assert "action=unchanged" in unchanged_output


def test_refuses_differing_existing_target_by_default(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")
    target = codex_home / "skills" / "session-checkout"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text("different local skill\n", encoding="utf-8")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "action=refused" in output
    assert "reason=target_differs" in output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == "different local skill\n"


def test_check_reports_missing_identical_and_drift_without_writes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "session-checkout")

    missing_code, missing_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--check",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )
    assert missing_code == installer.EXIT_SOURCE_MISSING
    assert "result: missing" in missing_output
    assert not (codex_home / "skills").exists()

    target = codex_home / "skills" / "session-checkout"
    shutil.copytree(source, target)
    identical_code, identical_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--check",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )
    assert identical_code == installer.EXIT_SUCCESS
    assert "result: identical" in identical_output

    target.joinpath("SKILL.md").write_text("drift\n", encoding="utf-8")
    drift_code, drift_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--check",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )
    assert drift_code == installer.EXIT_TARGET_DIFFERS
    assert "result: drift" in drift_output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == "drift\n"


def test_sync_updates_only_existing_drift_and_leaves_no_staging_residue(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "session-checkout")
    source.joinpath("reference.md").write_text("reviewed\n", encoding="utf-8")
    target = codex_home / "skills" / "session-checkout"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text("drift\n", encoding="utf-8")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_SUCCESS
    assert "action=synchronized" in output
    assert installer._directories_match(source, target)
    assert not list(target.parent.glob(".session-checkout.sync-*"))
    assert not list(target.parent.glob(".session-checkout.backup-*"))


def test_sync_refuses_missing_target_and_does_not_install(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_SOURCE_MISSING
    assert "reason: target_missing" in output
    assert not (codex_home / "skills" / "session-checkout").exists()


def test_role_pool_install_rejects_non_windows_before_destination_mutation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "mythic-edge-role-pool")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: False)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: True,
    )

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "result: refused" in output
    assert "reason: unsupported_execution_host" in output
    assert not (codex_home / "skills").exists()


def test_role_pool_install_rejects_missing_native_task_capability_before_mutation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "mythic-edge-role-pool")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: False,
    )

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "result: refused" in output
    assert "reason: native_task_capability_unavailable" in output
    assert not (codex_home / "skills").exists()


def test_role_pool_sync_rejects_non_windows_before_staging_or_replacement(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "mythic-edge-role-pool")
    source.joinpath("version.txt").write_text("new\n", encoding="utf-8")
    target = codex_home / "skills" / "mythic-edge-role-pool"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text("old\n", encoding="utf-8")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: False)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: True,
    )
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "result: refused" in output
    assert "reason: unsupported_execution_host" in output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == "old\n"
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_role_pool_sync_rejects_missing_native_task_capability_before_staging(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "mythic-edge-role-pool")
    source.joinpath("version.txt").write_text("new\n", encoding="utf-8")
    target = codex_home / "skills" / "mythic-edge-role-pool"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text("old\n", encoding="utf-8")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: False,
    )
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "result: refused" in output
    assert "reason: native_task_capability_unavailable" in output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == "old\n"
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_role_pool_check_is_platform_neutral_and_never_observes_preflight(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "mythic-edge-role-pool")
    monkeypatch.setattr(
        installer,
        "_trusted_windows_host_observed",
        lambda: pytest.fail("read-only check must not observe the host"),
    )
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: pytest.fail("read-only check must not observe task capability"),
    )

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--check",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_SOURCE_MISSING
    assert "result: missing" in output
    assert not (codex_home / "skills").exists()


def test_role_pool_windows_gate_allows_authorized_temp_install_and_sync(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "mythic-edge-role-pool")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: True,
    )

    install_code, install_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )
    assert install_code == installer.EXIT_SUCCESS
    assert "action=installed" in install_output

    source.joinpath("version.txt").write_text("reviewed\n", encoding="utf-8")
    sync_code, sync_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )
    assert sync_code == installer.EXIT_SUCCESS
    assert "action=synchronized" in sync_output
    target = codex_home / "skills" / "mythic-edge-role-pool"
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == "reviewed\n"


def test_role_pool_internal_sync_rejects_missing_native_task_capability(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    source = _write_skill(repo_root, "mythic-edge-role-pool")
    target = tmp_path / "codex-home" / "skills" / "mythic-edge-role-pool"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text("old\n", encoding="utf-8")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_exact_native_task_capability_observed",
        lambda: False,
    )
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    assert installer._synchronize_existing_skill(source, target) is False
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == "old\n"
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_offline_r0_sync_exact_synthetic_target_is_single_use_and_no_echo(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)

    code, output = _run(
        [
            "--offline-r0-sync",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )
    replay_code, replay_output = _run(
        [
            "--offline-r0-sync",
            "--skill",
            "mythic-edge-role-pool",
        ],
        capsys,
    )

    assert code == installer.EXIT_SUCCESS
    assert output.splitlines() == [
        f"package: {installer.PACKAGE_NAME}",
        "mode: offline-r0-sync",
        "operation: offline_r0_existing_target_sync",
        "status: synchronized",
        "result: synchronized",
    ]
    assert str(tmp_path) not in output
    assert installer._directories_match(source, target)
    assert replay_code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in replay_output
    assert "result: refused" in replay_output
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


@pytest.mark.parametrize(
    "arguments",
    [
        ["--offline-r0-sync", "--skill", "session-checkout"],
        [
            "--offline-r0-sync",
            "--skill",
            "mythic-edge-role-pool",
            "--repo-root",
            "private-root",
        ],
        [
            "--offline-r0-sync",
            "--skill",
            "mythic-edge-role-pool",
            "--codex-home",
            "private-home",
        ],
        [
            "--offline-r0-sync",
            "--skill",
            "mythic-edge-role-pool",
            "--dry-run",
        ],
    ],
)
def test_offline_r0_sync_rejects_every_noncanonical_invocation_without_echo(
    arguments: list[str],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        installer,
        "_offline_r0_default_paths",
        lambda: pytest.fail("invalid invocation must stop before path derivation"),
    )

    code, output = _run(arguments, capsys)

    assert code == installer.EXIT_USAGE_ERROR
    assert output.splitlines() == [
        f"package: {installer.PACKAGE_NAME}",
        "mode: offline-r0-sync",
        "operation: offline_r0_existing_target_sync",
        "status: blocked_request_or_packet_invalid",
        "result: refused",
    ]
    assert "private-root" not in output
    assert "private-home" not in output


def test_offline_r0_sync_rejects_codex_home_and_non_windows_before_path_access(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        installer,
        "_offline_r0_default_paths",
        lambda: pytest.fail("preflight must stop before path derivation"),
    )
    monkeypatch.setenv("CODEX_HOME", "private-home")

    env_code, env_output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )
    monkeypatch.delenv("CODEX_HOME")
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: False)
    host_code, host_output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert env_code == installer.EXIT_USAGE_ERROR
    assert host_code == installer.EXIT_USAGE_ERROR
    assert "status: blocked_request_or_packet_invalid" in env_output
    assert "status: blocked_request_or_packet_invalid" in host_output
    assert "private-home" not in env_output


@pytest.mark.parametrize("variable", ["HOME", "USERPROFILE"])
def test_offline_r0_sync_rejects_home_environment_target_redirection(
    variable: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trusted_profile = tmp_path / "trusted-profile"
    alternate_profile = tmp_path / "synthetic-alternate-owner-root"
    monkeypatch.delenv("HOME", raising=False)
    monkeypatch.delenv("USERPROFILE", raising=False)
    monkeypatch.setenv(variable, str(alternate_profile))
    monkeypatch.setattr(installer, "_trusted_windows_host_observed", lambda: True)
    monkeypatch.setattr(
        installer,
        "_trusted_windows_current_user_profile",
        lambda: trusted_profile,
        raising=False,
    )
    monkeypatch.setattr(
        installer,
        "_offline_r0_sync_existing_target",
        lambda *_args: pytest.fail(
            "environment divergence must stop before the mutating owner"
        ),
    )

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_USAGE_ERROR
    assert "status: blocked_request_or_packet_invalid" in output
    assert "result: refused" in output
    assert str(trusted_profile) not in output
    assert str(alternate_profile) not in output


def test_offline_r0_sync_rejects_missing_or_drifted_bound_tree_before_staging(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    target.joinpath("version.txt").unlink()
    drift_code, drift_output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )
    shutil.rmtree(target)
    missing_code, missing_output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert drift_code == installer.EXIT_TARGET_DIFFERS
    assert missing_code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in drift_output
    assert "status: blocked_skill_source_drift" in missing_output


def test_offline_r0_sync_rejects_unsafe_tree_before_opening_or_staging(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_target_check = installer._target_tree_unsafe_reason

    def synthetic_reparse(path: Path, root: Path) -> str | None:
        if path == target:
            return "target_reparse_point"
        return real_target_check(path, root)

    monkeypatch.setattr(
        installer,
        "_target_tree_unsafe_reason",
        synthetic_reparse,
    )
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )


def test_offline_r0_sync_rejects_reparse_ancestor_before_staging(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    ancestor_identity = installer._stat_identity(target.parent.parent.lstat())
    real_reparse_check = installer._is_reparse_metadata

    def mark_codex_home_as_reparse(metadata: os.stat_result) -> bool:
        return (
            installer._stat_identity(metadata) == ancestor_identity
            or real_reparse_check(metadata)
        )

    monkeypatch.setattr(
        installer,
        "_is_reparse_metadata",
        mark_codex_home_as_reparse,
    )
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )


def test_offline_r0_default_paths_use_trusted_profile_for_safety_checks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository_root = tmp_path / "repo"
    user_home = tmp_path / "user-home"
    monkeypatch.setattr(installer, "_default_repo_root", lambda: repository_root)
    monkeypatch.setattr(
        installer,
        "_trusted_windows_current_user_profile",
        lambda: user_home,
    )
    monkeypatch.setenv("HOME", str(user_home))
    monkeypatch.setenv("USERPROFILE", str(user_home))
    monkeypatch.setattr(
        Path,
        "home",
        staticmethod(
            lambda: pytest.fail(
                "offline target derivation must not use environment-backed Path.home"
            )
        ),
    )
    monkeypatch.setattr(
        installer,
        "_codex_home",
        lambda _value: pytest.fail(
            "offline path derivation must not resolve the target before safety checks"
        ),
    )

    source, target = installer._offline_r0_default_paths()

    assert source == (
        repository_root
        / installer.SKILL_SOURCE_ROOT
        / installer.TRUSTED_WINDOWS_SKILL_NAME
    )
    assert target == (
        user_home
        / ".codex"
        / "skills"
        / installer.TRUSTED_WINDOWS_SKILL_NAME
    )


def test_offline_r0_sync_path_resolution_failure_is_unknown_and_no_echo(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_resolve = Path.resolve

    def fail_source_resolution(
        path: Path,
        *args: object,
        **kwargs: object,
    ) -> Path:
        if path == source:
            raise OSError("synthetic private path resolution failure")
        return real_resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", fail_source_resolution)
    monkeypatch.setattr(
        installer.tempfile,
        "mkdtemp",
        lambda **_kwargs: pytest.fail("staging must not be created"),
    )

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "status: unknown_outcome_reconciliation_required" in output
    assert str(tmp_path) not in output
    assert "synthetic private path" not in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )


def test_offline_r0_sync_rejects_changed_post_move_target_identity(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_replace = installer.os.replace
    calls = 0

    def substitute_same_content_target(
        source_path: Path,
        destination_path: Path,
    ) -> None:
        nonlocal calls
        calls += 1
        real_replace(source_path, destination_path)
        if calls == 2:
            shutil.rmtree(destination_path)
            shutil.copytree(source, destination_path)

    monkeypatch.setattr(installer.os, "replace", substitute_same_content_target)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    backups = list(target.parent.glob(".mythic-edge-role-pool.backup-*"))
    assert code == installer.EXIT_INSTALL_FAILURE
    assert "status: unknown_outcome_reconciliation_required" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == "reviewed\n"
    assert len(backups) == 1
    assert backups[0].joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )


def test_offline_r0_sync_preserves_unowned_backup_during_cleanup(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_replace = installer.os.replace
    calls = 0

    def substitute_same_content_backup(
        source_path: Path,
        destination_path: Path,
    ) -> None:
        nonlocal calls
        calls += 1
        real_replace(source_path, destination_path)
        if calls == 2:
            backup = next(
                target.parent.glob(".mythic-edge-role-pool.backup-*")
            )
            substitute = target.parent / ".synthetic-unowned-backup"
            shutil.copytree(backup, substitute)
            shutil.rmtree(backup)
            real_replace(substitute, backup)

    monkeypatch.setattr(installer.os, "replace", substitute_same_content_backup)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    backups = list(target.parent.glob(".mythic-edge-role-pool.backup-*"))
    assert code == installer.EXIT_INSTALL_FAILURE
    assert "status: unknown_outcome_reconciliation_required" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == "reviewed\n"
    assert len(backups) == 1
    assert backups[0].joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )


def test_offline_r0_sync_staging_mismatch_is_known_and_cleans_up(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_copytree = installer.shutil.copytree

    def corrupt_staging(
        source_path: Path,
        destination_path: Path,
        **kwargs: object,
    ) -> Path:
        result = real_copytree(source_path, destination_path, **kwargs)
        Path(destination_path).joinpath("version.txt").write_text(
            "staging-drift\n",
            encoding="utf-8",
        )
        return result

    monkeypatch.setattr(installer.shutil, "copytree", corrupt_staging)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_offline_r0_sync_copy_failure_preserves_substituted_staging_path(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)

    def substitute_staging_then_fail(
        _source_path: Path,
        destination_path: Path,
        **_kwargs: object,
    ) -> Path:
        staging = Path(destination_path)
        shutil.rmtree(staging)
        staging.mkdir()
        staging.joinpath("foreign.txt").write_text(
            "foreign ordinary directory\n",
            encoding="utf-8",
        )
        raise OSError("synthetic copy failure after staging substitution")

    monkeypatch.setattr(installer.shutil, "copytree", substitute_staging_then_fail)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    staging_paths = list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert code == installer.EXIT_INSTALL_FAILURE
    assert "status: unknown_outcome_reconciliation_required" in output
    assert str(tmp_path) not in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )
    assert len(staging_paths) == 1
    assert staging_paths[0].joinpath("foreign.txt").read_text(encoding="utf-8") == (
        "foreign ordinary directory\n"
    )
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_offline_r0_sync_detects_concurrent_source_drift_and_restores_target(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_replace = installer.os.replace
    calls = 0

    def drift_before_move(source_path: Path, destination_path: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            source.joinpath("version.txt").write_text(
                "concurrent-source-drift\n",
                encoding="utf-8",
            )
        real_replace(source_path, destination_path)

    monkeypatch.setattr(installer.os, "replace", drift_before_move)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_offline_r0_sync_known_replacement_failure_rolls_back_and_cleans_up(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_replace = installer.os.replace
    calls = 0

    def fail_second_move(source_path: Path, destination_path: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic replacement failure")
        real_replace(source_path, destination_path)

    monkeypatch.setattr(installer.os, "replace", fail_second_move)

    code, output = _run(
        ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
        capsys,
    )

    assert code == installer.EXIT_TARGET_DIFFERS
    assert "status: blocked_skill_source_drift" in output
    assert target.joinpath("version.txt").read_text(encoding="utf-8") == (
        "predecessor\n"
    )
    assert not list(target.parent.glob(".mythic-edge-role-pool.sync-*"))
    assert not list(target.parent.glob(".mythic-edge-role-pool.backup-*"))


def test_offline_r0_sync_unproven_rollback_is_unknown_and_preserves_evidence(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_replace = installer.os.replace
    calls = 0

    def fail_replacement_and_rollback(
        source_path: Path,
        destination_path: Path,
    ) -> None:
        nonlocal calls
        calls += 1
        if calls in {2, 3}:
            raise OSError("synthetic ambiguous move")
        real_replace(source_path, destination_path)

    monkeypatch.setattr(installer.os, "replace", fail_replacement_and_rollback)
    try:
        code, output = _run(
            ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
            capsys,
        )

        assert code == installer.EXIT_INSTALL_FAILURE
        assert "status: unknown_outcome_reconciliation_required" in output
        assert not target.exists()
        assert len(list(target.parent.glob(".mythic-edge-role-pool.backup-*"))) == 1
    finally:
        monkeypatch.setattr(installer.os, "replace", real_replace)
        for residue in target.parent.glob(".mythic-edge-role-pool.*-*"):
            shutil.rmtree(residue)


def test_offline_r0_sync_cleanup_failure_is_unknown_and_not_silently_successful(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, target = _offline_sync_fixture(tmp_path)
    _configure_offline_sync(monkeypatch, source, target)
    real_remove = installer._remove_owned_tree

    def fail_backup_cleanup(
        path: Path,
        expected: installer.OfflineTreeObservation | None = None,
    ) -> bool:
        if ".backup-" in path.name:
            return False
        return real_remove(path, expected)

    monkeypatch.setattr(installer, "_remove_owned_tree", fail_backup_cleanup)
    try:
        code, output = _run(
            ["--offline-r0-sync", "--skill", "mythic-edge-role-pool"],
            capsys,
        )

        assert code == installer.EXIT_INSTALL_FAILURE
        assert "status: unknown_outcome_reconciliation_required" in output
        assert installer._directories_match(source, target)
        assert len(list(target.parent.glob(".mythic-edge-role-pool.backup-*"))) == 1
    finally:
        monkeypatch.setattr(installer, "_remove_owned_tree", real_remove)
        for residue in target.parent.glob(".mythic-edge-role-pool.backup-*"):
            shutil.rmtree(residue)


def test_sync_rolls_back_after_atomic_replacement_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")
    target = codex_home / "skills" / "session-checkout"
    target.mkdir(parents=True)
    original = "preserve this local target\n"
    target.joinpath("SKILL.md").write_text(original, encoding="utf-8")
    real_replace = installer.os.replace
    calls = 0

    def fail_replacement(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic replacement failure")
        real_replace(source, destination)

    monkeypatch.setattr(installer.os, "replace", fail_replacement)
    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--sync",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_INSTALL_FAILURE
    assert "result: failed" in output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == original
    assert not list(target.parent.glob(".session-checkout.sync-*"))
    assert not list(target.parent.glob(".session-checkout.backup-*"))


def test_sync_refuses_before_mutation_when_rollback_snapshot_is_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    source = _write_skill(repo_root, "session-checkout")
    target = tmp_path / "codex-home" / "skills" / "session-checkout"
    target.mkdir(parents=True)
    original = "preserve this local target\n"
    target.joinpath("SKILL.md").write_text(original, encoding="utf-8")
    real_snapshot = installer._tree_snapshot
    snapshot_calls = 0
    replace_called = False

    def unavailable_first_snapshot(
        root: Path,
    ) -> tuple[tuple[str, str, bytes], ...] | None:
        nonlocal snapshot_calls
        snapshot_calls += 1
        if snapshot_calls == 1:
            return None
        return real_snapshot(root)

    def record_replace(source_path: Path, destination_path: Path) -> None:
        nonlocal replace_called
        replace_called = True

    monkeypatch.setattr(installer, "_tree_snapshot", unavailable_first_snapshot)
    monkeypatch.setattr(installer.os, "replace", record_replace)

    assert installer._synchronize_existing_skill(source, target) is False
    assert replace_called is False
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == original
    assert not list(target.parent.glob(".session-checkout.sync-*"))
    assert not list(target.parent.glob(".session-checkout.backup-*"))


def test_check_rejects_reparse_target_before_comparing_bytes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "session-checkout")
    target = codex_home / "skills" / "session-checkout"
    shutil.copytree(source, target)
    real_reparse = installer._is_reparse_point

    def synthetic_reparse(path: Path) -> bool:
        if path == target:
            return True
        return real_reparse(path)

    monkeypatch.setattr(installer, "_is_reparse_point", synthetic_reparse)
    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--check",
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_UNSAFE_PATH
    assert "result: unsafe" in output
    assert "target_reparse_point" in output


def test_refuses_same_size_same_mtime_target_when_bytes_differ(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source_body = (
        "---\n"
        "name: session-checkout\n"
        "description: Test skill session-checkout.\n"
        "---\n\n"
        "# A\n"
    )
    target_body = source_body.replace("# A", "# B")
    source = _write_skill(repo_root, "session-checkout", body=source_body)
    target = codex_home / "skills" / "session-checkout"
    target.mkdir(parents=True)
    target.joinpath("SKILL.md").write_text(target_body, encoding="utf-8")
    timestamp = 1_700_000_000
    os.utime(source / "SKILL.md", (timestamp, timestamp))
    os.utime(target / "SKILL.md", (timestamp, timestamp))

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert len(source_body) == len(target_body)
    assert code == installer.EXIT_TARGET_DIFFERS
    assert "action=refused" in output
    assert "reason=target_differs" in output
    assert target.joinpath("SKILL.md").read_text(encoding="utf-8") == target_body


def test_refuses_target_skill_symlink_escape_even_when_bytes_match(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    source = _write_skill(repo_root, "session-checkout")
    external = tmp_path / "external-target"
    external.mkdir()
    external.joinpath("SKILL.md").write_text(
        source.joinpath("SKILL.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    target_root = codex_home / "skills"
    target_root.mkdir(parents=True)
    target = target_root / "session-checkout"
    try:
        target.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("filesystem does not allow directory symlinks")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_UNSAFE_PATH
    assert "action=refused" in output
    assert "reason=target_symlink_escape" in output
    assert external.joinpath("SKILL.md").read_text(encoding="utf-8") == source.joinpath(
        "SKILL.md"
    ).read_text(encoding="utf-8")


def test_refuses_target_root_symlink_escape_before_installing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")
    external_skills_root = tmp_path / "external-skills"
    external_skills_root.mkdir()
    codex_home.mkdir()
    try:
        (codex_home / "skills").symlink_to(external_skills_root, target_is_directory=True)
    except OSError:
        pytest.skip("filesystem does not allow directory symlinks")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "session-checkout",
        ],
        capsys,
    )

    assert code == installer.EXIT_UNSAFE_PATH
    assert "result: failed" in output
    assert "reason: target_symlink_escape" in output
    assert not (external_skills_root / "session-checkout").exists()


def test_unknown_skill_and_missing_package_return_source_missing_status(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    _write_skill(repo_root, "session-checkout")

    unknown_code, unknown_output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            "--skill",
            "missing-skill",
        ],
        capsys,
    )
    missing_code, missing_output = _run(
        [
            "--repo-root",
            str(tmp_path / "empty-repo"),
            "--codex-home",
            str(codex_home),
            "--list",
        ],
        capsys,
    )

    assert unknown_code == installer.EXIT_SOURCE_MISSING
    assert "selected_skill_missing" in unknown_output
    assert missing_code == installer.EXIT_SOURCE_MISSING
    assert "source_package_missing" in missing_output


def test_symlink_escape_source_is_rejected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    source_root = repo_root / "docs" / "codex_skills"
    source_root.mkdir(parents=True)
    external = tmp_path / "external-skill"
    _write_skill(tmp_path, "escape")
    tmp_path.joinpath("docs", "codex_skills", "escape").rename(external)
    symlink_path = source_root / "escape"
    try:
        symlink_path.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("filesystem does not allow directory symlinks")

    code, output = _run(
        [
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(tmp_path / "codex-home"),
            "--all",
        ],
        capsys,
    )

    assert code == installer.EXIT_UNSAFE_PATH
    assert "action=unsafe" in output
    assert "source_symlink_escape" in output


def test_repo_owned_skill_sources_avoid_local_paths_and_private_markers() -> None:
    source_root = Path(__file__).resolve().parents[1] / "docs" / "codex_skills"
    skill_files = sorted(source_root.glob("*/SKILL.md"))
    unix_home_marker = "/" + "Users" + "/"
    windows_home_marker = "C:" + "\\Users"
    private_log_marker = "Player" + ".log"
    utc_log_marker = "UTC" + "_Log"

    assert [path.parent.name for path in skill_files] == [
        "mythic-edge-role-pool",
        "new-workcycle",
        "session-checkout",
    ]
    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        assert unix_home_marker not in text
        assert windows_home_marker not in text
        assert private_log_marker not in text
        assert utc_log_marker not in text
        if skill_file.parent.name == "mythic-edge-role-pool":
            assert "NOT LIVE-READY" in text
        else:
            assert "webhook URL" in text or "webhook" in text


def test_byte_bound_role_pool_sources_disable_git_text_normalization() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    attribute_rules = {
        parts[0]: parts[1:]
        for line in repo_root.joinpath(".gitattributes").read_text(
            encoding="utf-8"
        ).splitlines()
        if (parts := line.split()) and not parts[0].startswith("#")
    }
    byte_bound_paths = (
        "docs/codex_skills/mythic-edge-role-pool/references/"
        "external-isolation-broker-v5-corrective-successor.md",
        "docs/codex_skills/mythic-edge-role-pool/references/"
        "fallback-pickup-fixture/pickup.json",
    )

    for path in byte_bound_paths:
        assert attribute_rules.get(path) == ["-text", "whitespace=cr-at-eol"]
