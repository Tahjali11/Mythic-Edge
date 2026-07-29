#!/usr/bin/env python3
"""Run the complete offline deterministic gate and print resulting hashes."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
OFFLINE_GUARD_DIRECTORY = SCRIPTS / "offline_gate_guard"
sys.path.insert(0, str(OFFLINE_GUARD_DIRECTORY))
from offline_guard import (  # noqa: E402
    ACTIVATION_VARIABLE,
    BOUNDARY_CLASSIFICATION,
    GUARD_DIRECTORY_VARIABLE,
    WRITE_ROOTS_VARIABLE,
    install_offline_guard,
)

OLD_WORKFLOW_ROOT = SKILL_ROOT.parent / "mythic-edge-workflow"
REVIEWED_ROOTS = (SKILL_ROOT, OLD_WORKFLOW_ROOT)
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
QUICK_VALIDATE = (
    CODEX_HOME
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)
MINIMUM_TEST_COUNT = 220
REQUIRED_TEST_MODULES = {
    "test_codex_launcher_contract.py",
    "test_check_pool_plan.py",
    "test_fallback_pickup.py",
    "test_offline_gate_guard.py",
    "test_pool_results.py",
    "test_release_adversarial.py",
    "test_stage3_behavioral_planning.py",
    "test_stage4_canary_exception.py",
    "test_skill_contract.py",
}
OFFLINE_WRITE_ROOTS_TEXT = str(Path(tempfile.gettempdir()).resolve())


def guarded_environment(source: dict[str, str] | None = None) -> dict[str, str]:
    environment = dict(os.environ if source is None else source)
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(OFFLINE_GUARD_DIRECTORY)
        if not existing_pythonpath
        else str(OFFLINE_GUARD_DIRECTORY) + os.pathsep + existing_pythonpath
    )
    environment[ACTIVATION_VARIABLE] = "1"
    environment[WRITE_ROOTS_VARIABLE] = OFFLINE_WRITE_ROOTS_TEXT
    environment[GUARD_DIRECTORY_VARIABLE] = str(OFFLINE_GUARD_DIRECTORY)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def run_quick_validation(skill_root: Path) -> bool:
    if not QUICK_VALIDATE.is_file():
        print(f"release gate failed: missing Skill Creator validator: {QUICK_VALIDATE}")
        return False
    environment = guarded_environment()
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(QUICK_VALIDATE), str(skill_root)],
            cwd=skill_root,
            env=environment,
            check=False,
            text=True,
            timeout=60,
            capture_output=True,
        )
    except subprocess.TimeoutExpired:
        print("offline gate failed: Skill Creator validation exceeded 60 seconds")
        return False
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip())
    return completed.returncode == 0


def run_unit_tests() -> tuple[unittest.result.TestResult | None, int]:
    sys.path.insert(0, str(SCRIPTS))
    install_offline_guard(
        guard_directory=OFFLINE_GUARD_DIRECTORY,
        write_roots_text=OFFLINE_WRITE_ROOTS_TEXT,
    )
    missing_modules = sorted(
        name for name in REQUIRED_TEST_MODULES if not (SCRIPTS / name).is_file()
    )
    if missing_modules:
        print("offline gate failed: missing required test modules: " + ", ".join(missing_modules))
        return None, 0
    suite = unittest.defaultTestLoader.discover(
        str(SCRIPTS), pattern="test_*.py", top_level_dir=str(SCRIPTS)
    )
    count = suite.countTestCases()
    if count < MINIMUM_TEST_COUNT:
        print(
            f"offline gate failed: discovered {count} tests; minimum is {MINIMUM_TEST_COUNT}"
        )
        return None, count

    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    return result, count


def reviewed_files() -> list[Path]:
    return sorted(
        path
        for root in REVIEWED_ROOTS
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.lower() not in {".pyc", ".pyo"}
    )


def print_hashes() -> None:
    print("post-remediation SHA-256 snapshot:")
    for path in reviewed_files():
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        print(f"{digest}  {path}")


def snapshot() -> dict[str, str]:
    return {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in reviewed_files()
    }


def main() -> int:
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    before = snapshot()
    print(f"offline deterministic gate boundary: {BOUNDARY_CLASSIFICATION}", flush=True)
    print("offline deterministic gate: Skill Creator structural validation", flush=True)
    for skill_root in REVIEWED_ROOTS:
        if not skill_root.is_dir():
            print(f"release gate failed: missing reviewed skill: {skill_root}")
            return 1
        print(f"validating skill structure: {skill_root.name}")
        if not run_quick_validation(skill_root):
            return 1
    print("offline deterministic gate: isolated unit and adversarial tests")
    result, count = run_unit_tests()
    if result is None:
        return 1
    if result.skipped:
        print(f"offline gate failed: {len(result.skipped)} skipped test(s) are not permitted")
        return 1
    if result.expectedFailures:
        print(
            f"offline gate failed: {len(result.expectedFailures)} expected failure(s) are not permitted"
        )
        return 1
    if not result.wasSuccessful():
        return 1
    after = snapshot()
    if before != after:
        changed = sorted(set(before) ^ set(after) | {key for key in before if before.get(key) != after.get(key)})
        print("offline gate failed: tests changed reviewed files: " + ", ".join(changed))
        return 1
    print_hashes()
    print(f"offline deterministic gate passed: {count} tests and structural validation succeeded")
    print(
        "TRUST BOUNDARY: untrusted executable/script or live behavioral proof "
        "requires external OS-enforced read-only/no-network isolation"
    )
    print("NOT LIVE-READY: the staged behavioral canaries in fallback-and-recovery.md remain required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
