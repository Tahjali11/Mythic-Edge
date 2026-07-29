from __future__ import annotations

import importlib.util
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
