#!/usr/bin/env python3
"""Evaluate trusted-owner Role Pool R0 bootstrap prerequisites without mutation."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Sequence, TextIO

SCHEMA_VERSION = "trusted_owner_r0_offline_bootstrap_evidence.v1"
OPERATION = "evaluate_r0_bootstrap_eligibility_read_only"
REPOSITORY_ID = 1235264383
REPOSITORY_NAME = "tahjali11/mythic-edge"
ISSUE_URL = "https://github.com/Tahjali11/Mythic-Edge/issues/761"
BASE_COMMIT = "10d4a4a79053fe33297a612599667d9b58bb4296"

PROFILE_CONTRACT_SHA256 = (
    "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
)
APP_SERVER_CONTRACT_SHA256 = (
    "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8"
)
APP_NATIVE_CONTRACT_SHA256 = (
    "00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4"
)
R0_CONTRACT_SHA256 = (
    "07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82"
)
INSTALLER_SHA256 = (
    "0898b4c476a3d1ac8fff726b146e40c2340a96134a4b035928fcbeaaff78d2ad"
)
STAGE3_MANIFEST_SHA256 = (
    "cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06"
)
STAGE3_MANIFEST_FILE_COUNT = 39
STAGE3_MANIFEST_BYTE_COUNT = 5729
SOURCE_TREE_NODE_COUNT = 41
SOURCE_TREE_FILE_COUNT = 36
SOURCE_TREE_MANIFEST_BYTE_COUNT = 6495
SOURCE_TREE_SHA256 = (
    "18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f"
)

CHECKER_RELATIVE_PATH = Path("tools/check_role_pool_r0_bootstrap.py")
CHECKER_TEST_RELATIVE_PATH = Path("tests/test_check_role_pool_r0_bootstrap.py")
SOURCE_SKILL_RELATIVE_PATH = Path("docs/codex_skills/mythic-edge-role-pool")
REGISTRY_RELATIVE_PATH = Path(
    "docs/role_pool/trusted_owner_repository_registry.v1.json"
)
RELEASE_STATE_RELATIVE_PATH = Path(
    "docs/role_pool/trusted_owner_native_release_state.v1.jsonl"
)

FILE_BINDINGS = (
    (
        "profile_contract",
        Path("docs/contracts/trusted_owner_native_role_pool_profile.md"),
        PROFILE_CONTRACT_SHA256,
    ),
    (
        "app_server_contract",
        Path("docs/contracts/role_pool_codex_app_server_native_task_adapter.md"),
        APP_SERVER_CONTRACT_SHA256,
    ),
    (
        "app_native_contract",
        Path("docs/contracts/role_pool_codex_app_native_direct_task_adapter.md"),
        APP_NATIVE_CONTRACT_SHA256,
    ),
    (
        "stage3_transition_contract",
        Path("docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md"),
        "de17a909d68fa1427d26ea42f5ff575addccf76185c77b93c03499e25bea48fa",
    ),
    (
        "capability_evidence_contract",
        Path("docs/contracts/role_pool_windows_native_task_capability_evidence.md"),
        "d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef",
    ),
    (
        "installer",
        Path("tools/install_codex_skills.py"),
        INSTALLER_SHA256,
    ),
    (
        "registry_validator",
        SOURCE_SKILL_RELATIVE_PATH / "scripts/check_pool_plan.py",
        "5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361",
    ),
    (
        "stage3_validator",
        SOURCE_SKILL_RELATIVE_PATH
        / "scripts/check_stage3_behavioral_planning.py",
        "8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6",
    ),
    (
        "fake_transport",
        SOURCE_SKILL_RELATIVE_PATH
        / "scripts/trusted_native_app_server_adapter.py",
        "9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18",
    ),
    (
        "direct_fake_transport",
        SOURCE_SKILL_RELATIVE_PATH
        / "scripts/trusted_native_app_direct_task_adapter.py",
        "fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98",
    ),
    (
        "complete_gate",
        SOURCE_SKILL_RELATIVE_PATH / "scripts/run_release_tests.py",
        "1ac0dd02df447a35e7e95e3b534d89a2c7e0b3e5901266b780b5ba13238f8a75",
    ),
    (
        "r0_contract",
        Path(
            "docs/contracts/"
            "role_pool_trusted_owner_r0_post_sync_evidence_binding_successor.md"
        ),
        R0_CONTRACT_SHA256,
    ),
)

WORKFLOW_SNAPSHOT_RELATIVE_PATHS = (
    Path("SKILL.md"),
    Path("agents/openai.yaml"),
    Path("scripts/accept_fallback_prompt.py"),
)

CONTRACT_BINDING_STATUSES = ("exact", "known_invalid", "unknown")
MANIFEST_STATUSES = ("exact", "known_invalid", "unknown")
SOURCE_INSTALL_STATUSES = (
    "identical",
    "installed_missing",
    "installed_drift",
    "unsafe_or_unreadable",
    "unknown",
)
REGISTRY_STATUSES = ("valid_exact", "absent", "invalid", "unknown")
RELEASE_STATE_STATUSES = (
    "absent_bootstrap_candidate",
    "present_valid_chain",
    "present_invalid_or_forked",
    "unknown",
)
VALIDATOR_BUNDLE_STATUSES = ("exact", "known_invalid", "unknown")
OFFLINE_VALIDATION_STATUSES = ("passed", "failed", "unknown")
TERMINAL_STATUSES = (
    "blocked_contract_binding_invalid",
    "blocked_validator_bundle_invalid",
    "blocked_manifest_invalid",
    "blocked_skill_source_drift",
    "blocked_registry_missing_or_invalid",
    "blocked_release_state_conflict",
    "blocked_offline_validation_failed",
    "unknown_outcome_reconciliation_required",
    "eligible_for_independent_review",
)

RESULT_FIELDS = (
    "schema_version",
    "operation",
    "repository_id",
    "repository_name",
    "issue_url",
    "base_commit",
    "profile_contract_sha256",
    "app_server_contract_sha256",
    "r0_contract_sha256",
    "contract_binding_status",
    "stage3_manifest_file_count",
    "stage3_manifest_byte_count",
    "stage3_manifest_sha256",
    "manifest_status",
    "source_tree_node_count",
    "source_tree_file_count",
    "source_tree_manifest_byte_count",
    "source_tree_sha256",
    "installed_tree_node_count",
    "installed_tree_file_count",
    "installed_tree_manifest_byte_count",
    "installed_tree_sha256",
    "source_install_status",
    "registry_status",
    "registry_sha256",
    "release_state_status",
    "release_state_sha256",
    "checker_sha256",
    "checker_test_sha256",
    "validator_bundle_sha256",
    "validator_bundle_status",
    "offline_validation_status",
    "terminal_status",
    "eligible_for_independent_review",
    "effect_counts",
    "authority_flags",
    "evidence_sha256",
)
EFFECT_COUNT_FIELDS = (
    "app_server_process_start_count",
    "task_creation_count",
    "network_operation_count",
    "repository_command_count",
    "persistent_mutation_count",
)
AUTHORITY_FIELDS = (
    "repository_mutation_authorized",
    "implementation_authorized",
    "publication_authorized",
    "merge_authorized",
    "deployment_authorized",
    "installation_authorized",
    "package_operations_authorized",
    "network_authorized",
    "secrets_authorized",
    "external_isolation_authorized",
    "canary_authorized",
    "stage4_authorized",
    "stage_advancement_authorized",
    "dispatch_authorized",
    "live_ready",
    "trusted_owner_native_profile_ready",
)

SHA256_LENGTH = 64
PACKET_UNAVAILABLE = "r0_bootstrap_packet_unavailable"


class PacketUnavailableError(RuntimeError):
    """Signal that a complete public-safe evidence packet cannot be sealed."""


@dataclass(frozen=True)
class EvaluationRoots:
    """Fixed roots used by the production evaluator or a temporary-root test."""

    repository_root: Path
    installed_skills_root: Path | None


@dataclass(frozen=True)
class FileObservation:
    state: str
    payload: bytes | None = None
    identity: tuple[int, int, int, int, int] | None = None


@dataclass(frozen=True)
class TreeObservation:
    node_count: int | None
    file_count: int | None
    canonical_byte_count: int | None
    sha256: str | None
    status: str


@dataclass(frozen=True)
class ManifestObservation:
    file_count: int
    canonical_byte_count: int
    sha256: str | None
    status: str


@dataclass(frozen=True)
class FixedInputObservation:
    registry_status: str
    registry_sha256: str | None
    release_state_status: str
    release_state_sha256: str | None


@dataclass(frozen=True)
class ComponentObservations:
    contract_binding_status: str
    manifest: ManifestObservation
    source_tree: TreeObservation
    installed_tree: TreeObservation
    source_install_status: str
    registry_status: str
    registry_sha256: str | None
    release_state_status: str
    release_state_sha256: str | None
    checker_sha256: str
    checker_test_sha256: str
    validator_bundle_sha256: str
    validator_bundle_status: str
    offline_validation_status: str


@dataclass(frozen=True)
class OwnerModules:
    installer: ModuleType
    stage3: ModuleType
    pool: ModuleType
    adapter: ModuleType
    direct_adapter: ModuleType


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or len(value) != SHA256_LENGTH:
        return False
    return all(character in "0123456789abcdef" for character in value)


def _is_reparse_metadata(metadata: os.stat_result) -> bool:
    marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & marker)


def _identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
    )


def _observe_component(path: Path, expected_kind: str) -> FileObservation:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return FileObservation("absent")
    except OSError:
        return FileObservation("unknown")
    if _is_reparse_metadata(metadata):
        return FileObservation("unsafe")
    if expected_kind == "file" and not stat.S_ISREG(metadata.st_mode):
        return FileObservation("unsafe")
    if expected_kind == "directory" and not stat.S_ISDIR(metadata.st_mode):
        return FileObservation("unsafe")
    try:
        if path.resolve(strict=True).name != path.name:
            return FileObservation("case_mismatch")
    except OSError:
        return FileObservation("unknown")
    return FileObservation("exact", identity=_identity(metadata))


def _read_stable_file(path: Path) -> FileObservation:
    before = _observe_component(path, "file")
    if before.state != "exact" or before.identity is None:
        return before
    try:
        with path.open("rb") as handle:
            opened = _identity(os.fstat(handle.fileno()))
            if opened != before.identity:
                return FileObservation("identity_unstable")
            payload = handle.read()
            after_read = _identity(os.fstat(handle.fileno()))
    except OSError:
        return FileObservation("unknown")
    after = _observe_component(path, "file")
    if (
        after.state != "exact"
        or after.identity is None
        or after.identity != before.identity
        or after_read != before.identity
    ):
        return FileObservation("identity_unstable")
    return FileObservation("exact", payload=payload, identity=before.identity)


def _binding_status(repository_root: Path) -> tuple[str, dict[str, str]]:
    observed: dict[str, str] = {}
    known_invalid = False
    unknown = False
    for name, relative_path, expected_sha256 in FILE_BINDINGS:
        observation = _read_stable_file(repository_root / relative_path)
        if observation.state == "exact" and observation.payload is not None:
            digest = hashlib.sha256(observation.payload).hexdigest()
            observed[name] = digest
            if digest != expected_sha256:
                known_invalid = True
        elif observation.state == "unknown" or observation.state == "identity_unstable":
            unknown = True
        else:
            known_invalid = True
    if known_invalid:
        return "known_invalid", observed
    if unknown:
        return "unknown", observed
    return "exact", observed


def _load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise PacketUnavailableError
    module = importlib.util.module_from_spec(specification)
    previous_bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(name, None)
        raise PacketUnavailableError from exc
    finally:
        sys.dont_write_bytecode = previous_bytecode_setting
    return module


def _load_owner_modules(repository_root: Path) -> OwnerModules:
    source_scripts = repository_root / SOURCE_SKILL_RELATIVE_PATH / "scripts"
    namespace = hashlib.sha256(
        str(repository_root).encode("utf-8", errors="surrogatepass")
    ).hexdigest()[:12]
    installer = _load_module(
        f"_r0_installer_{namespace}",
        repository_root / "tools/install_codex_skills.py",
    )
    stage3 = _load_module(
        f"_r0_stage3_{namespace}",
        source_scripts / "check_stage3_behavioral_planning.py",
    )

    dependency_names = (
        "trusted_native_app_server_adapter",
        "trusted_native_app_direct_task_adapter",
        "codex_launcher_contract",
    )
    previous_modules = {
        name: sys.modules.get(name) for name in dependency_names
    }
    adapter = _load_module(
        "trusted_native_app_server_adapter",
        source_scripts / "trusted_native_app_server_adapter.py",
    )
    direct_adapter = _load_module(
        "trusted_native_app_direct_task_adapter",
        source_scripts / "trusted_native_app_direct_task_adapter.py",
    )
    _load_module(
        "codex_launcher_contract",
        source_scripts / "codex_launcher_contract.py",
    )
    try:
        pool = _load_module(
            f"_r0_pool_{namespace}",
            source_scripts / "check_pool_plan.py",
        )
    finally:
        for name, previous in previous_modules.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous
    return OwnerModules(
        installer=installer,
        stage3=stage3,
        pool=pool,
        adapter=adapter,
        direct_adapter=direct_adapter,
    )


def _manifest_observation(
    stage3: ModuleType,
    workflow_root: Path | None,
) -> ManifestObservation:
    if workflow_root is None:
        return ManifestObservation(0, 0, None, "unknown")
    stage3.WORKFLOW_ROOT = workflow_root
    stage3.WORKFLOW_SNAPSHOT_FILES = tuple(
        workflow_root / relative_path
        for relative_path in WORKFLOW_SNAPSHOT_RELATIVE_PATHS
    )
    try:
        rows = stage3.current_skill_manifest()
        encoded = stage3.canonical_bytes(rows)
        digest = hashlib.sha256(encoded).hexdigest()
        stage3._validated_manifest_state()
    except stage3.ManifestTransitionError:
        try:
            rows = stage3.current_skill_manifest()
            encoded = stage3.canonical_bytes(rows)
            digest = hashlib.sha256(encoded).hexdigest()
            return ManifestObservation(
                len(rows),
                len(encoded),
                digest,
                "known_invalid",
            )
        except Exception:
            return ManifestObservation(0, 0, None, "known_invalid")
    except Exception:
        return ManifestObservation(0, 0, None, "unknown")
    exact = (
        len(rows) == STAGE3_MANIFEST_FILE_COUNT
        and len(encoded) == STAGE3_MANIFEST_BYTE_COUNT
        and digest == STAGE3_MANIFEST_SHA256
    )
    return ManifestObservation(
        len(rows),
        len(encoded),
        digest,
        "exact" if exact else "known_invalid",
    )


def _tree_manifest(
    snapshot: tuple[tuple[str, str, bytes], ...],
    pool: ModuleType,
) -> tuple[int, int, int, str]:
    rows = [
        {
            "path": relative_path,
            "kind": kind,
            "byte_count": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        for relative_path, kind, payload in snapshot
    ]
    document = {
        "schema_version": "trusted_owner_role_pool_install_tree.v1",
        "rows": rows,
    }
    encoded = pool.trusted_native_canonical_bytes(document)
    return (
        len(snapshot),
        sum(kind == "file" for _, kind, _ in snapshot),
        len(encoded),
        hashlib.sha256(encoded).hexdigest(),
    )


def _tree_observations(
    roots: EvaluationRoots,
    owners: OwnerModules,
) -> tuple[TreeObservation, TreeObservation, str]:
    try:
        discovery = owners.installer.discover_skills(roots.repository_root)
    except OSError:
        unknown = TreeObservation(None, None, None, None, "unknown")
        return unknown, unknown, "unknown"
    expected_source_root = (
        roots.repository_root / SOURCE_SKILL_RELATIVE_PATH
    ).resolve()
    matches = [
        skill
        for skill in discovery.skills
        if skill.name == "mythic-edge-role-pool"
    ]
    if (
        discovery.missing
        or discovery.unsafe_reason is not None
        or len(matches) != 1
        or matches[0].unsafe_reason is not None
        or matches[0].source_dir != expected_source_root
    ):
        unsafe = TreeObservation(
            None,
            None,
            None,
            None,
            "unsafe_or_unreadable",
        )
        return unsafe, unsafe, "unsafe_or_unreadable"
    source_root = matches[0].source_dir
    source_unsafe = owners.installer._source_tree_unsafe_reason(
        source_root,
        source_root.parent,
    )
    source_snapshot = owners.installer._tree_snapshot(source_root)
    if source_unsafe is not None or source_snapshot is None:
        source = TreeObservation(None, None, None, None, "unsafe_or_unreadable")
    else:
        source_values = _tree_manifest(source_snapshot, owners.pool)
        source = TreeObservation(*source_values, "observed")
    source_matches_reviewed = (
        source.node_count == SOURCE_TREE_NODE_COUNT
        and source.file_count == SOURCE_TREE_FILE_COUNT
        and source.canonical_byte_count == SOURCE_TREE_MANIFEST_BYTE_COUNT
        and source.sha256 == SOURCE_TREE_SHA256
    )

    if roots.installed_skills_root is None:
        installed = TreeObservation(None, None, None, None, "unknown")
        return source, installed, "unknown"

    target_root = roots.installed_skills_root
    target = target_root / "mythic-edge-role-pool"
    target_observation = _observe_component(target, "directory")
    if target_observation.state == "absent":
        installed = TreeObservation(None, None, None, None, "installed_missing")
        status = (
            "unsafe_or_unreadable"
            if source_snapshot is None
            else "installed_missing"
        )
        return source, installed, status
    target_unsafe = owners.installer._target_tree_unsafe_reason(
        target,
        target_root,
    )
    target_snapshot = owners.installer._tree_snapshot(target)
    if (
        target_observation.state != "exact"
        or target_unsafe is not None
        or target_snapshot is None
    ):
        installed = TreeObservation(
            None,
            None,
            None,
            None,
            "unsafe_or_unreadable",
        )
        return source, installed, "unsafe_or_unreadable"
    installed_values = _tree_manifest(target_snapshot, owners.pool)
    installed = TreeObservation(*installed_values, "observed")
    if source_snapshot is None:
        return source, installed, "unsafe_or_unreadable"
    try:
        identical = owners.installer._directories_match(source_root, target)
    except OSError:
        return source, installed, "unknown"
    return (
        source,
        installed,
        "identical"
        if identical and source_matches_reviewed
        else "installed_drift",
    )


def _stable_directory_identity(path: Path) -> tuple[int, int, int, int, int] | None:
    observation = _observe_component(path, "directory")
    if observation.state != "exact":
        return None
    return observation.identity


def _parse_registry(
    observation: FileObservation,
    pool: ModuleType,
) -> tuple[str, str | None]:
    if observation.state == "absent":
        return "absent", None
    if observation.state != "exact" or observation.payload is None:
        return "unknown", None
    try:
        text = observation.payload.decode("utf-8")
        registry = pool.parse_trusted_native_json(text)
    except Exception:
        return "invalid", None
    if pool.validate_trusted_native_registry(registry):
        return "invalid", None
    entries = registry.get("entries")
    matches = (
        [
            entry
            for entry in entries
            if isinstance(entry, dict)
            and entry.get("repository_id") == REPOSITORY_ID
        ]
        if isinstance(entries, list)
        else []
    )
    if len(matches) != 1:
        return "invalid", None
    entry = matches[0]
    if (
        entry.get("canonical_name") != REPOSITORY_NAME
        or entry.get("status") != "active"
        or "offline_validation" not in entry.get("permitted_operations", [])
        or entry.get("review_due_at_utc") is not None
    ):
        return "invalid", None
    digest = registry.get("registry_sha256")
    if not _is_sha256(digest):
        return "invalid", None
    return "valid_exact", digest


def _parse_release_state(
    observation: FileObservation,
    pool: ModuleType,
) -> tuple[str, str | None]:
    if observation.state == "absent":
        return "absent_bootstrap_candidate", None
    if observation.state != "exact" or observation.payload is None:
        return "unknown", None
    payload = observation.payload
    digest = hashlib.sha256(payload).hexdigest()
    if not payload or not payload.endswith(b"\n"):
        return "present_invalid_or_forked", digest
    records: list[dict[str, object]] = []
    try:
        for line in payload.splitlines(keepends=True):
            if line == b"\n":
                return "present_invalid_or_forked", digest
            text = line.decode("utf-8")
            record = pool.parse_trusted_native_json(text)
            if pool.validate_trusted_native_release_state_record(record):
                return "present_invalid_or_forked", digest
            records.append(record)
    except Exception:
        return "present_invalid_or_forked", digest
    if pool.validate_trusted_native_release_chain(records):
        return "present_invalid_or_forked", digest
    return "present_valid_chain", digest


def _fixed_inputs(
    repository_root: Path,
    pool: ModuleType,
) -> FixedInputObservation:
    docs = repository_root / "docs"
    role_pool = docs / "role_pool"
    docs_before = _observe_component(docs, "directory")
    if docs_before.state != "exact" or docs_before.identity is None:
        return FixedInputObservation("unknown", None, "unknown", None)

    parent_before = _observe_component(role_pool, "directory")
    if parent_before.state == "absent":
        registry = _observe_component(repository_root / REGISTRY_RELATIVE_PATH, "file")
        release = _observe_component(
            repository_root / RELEASE_STATE_RELATIVE_PATH,
            "file",
        )
        parent_after = _observe_component(role_pool, "directory")
        docs_after = _observe_component(docs, "directory")
        stable_absence = (
            registry.state == "absent"
            and release.state == "absent"
            and parent_after.state == "absent"
            and docs_after.state == "exact"
            and docs_after.identity == docs_before.identity
        )
        if stable_absence:
            return FixedInputObservation(
                "absent",
                None,
                "absent_bootstrap_candidate",
                None,
            )
        return FixedInputObservation("unknown", None, "unknown", None)
    if parent_before.state != "exact" or parent_before.identity is None:
        return FixedInputObservation("unknown", None, "unknown", None)

    registry_observation = _read_stable_file(
        repository_root / REGISTRY_RELATIVE_PATH
    )
    release_observation = _read_stable_file(
        repository_root / RELEASE_STATE_RELATIVE_PATH
    )
    parent_after = _observe_component(role_pool, "directory")
    docs_after = _observe_component(docs, "directory")
    if (
        parent_after.state != "exact"
        or parent_after.identity != parent_before.identity
        or docs_after.state != "exact"
        or docs_after.identity != docs_before.identity
    ):
        return FixedInputObservation("unknown", None, "unknown", None)
    registry_status, registry_sha256 = _parse_registry(
        registry_observation,
        pool,
    )
    release_status, release_sha256 = _parse_release_state(
        release_observation,
        pool,
    )
    return FixedInputObservation(
        registry_status,
        registry_sha256,
        release_status,
        release_sha256,
    )


def _select_terminal_status(
    contract_binding_status: str,
    validator_bundle_status: str,
    manifest_status: str,
    source_install_status: str,
    registry_status: str,
    release_state_status: str,
    offline_validation_status: str,
) -> str:
    ordered = (
        (
            contract_binding_status,
            "exact",
            "unknown",
            "blocked_contract_binding_invalid",
        ),
        (
            validator_bundle_status,
            "exact",
            "unknown",
            "blocked_validator_bundle_invalid",
        ),
        (
            manifest_status,
            "exact",
            "unknown",
            "blocked_manifest_invalid",
        ),
        (
            source_install_status,
            "identical",
            "unknown",
            "blocked_skill_source_drift",
        ),
        (
            registry_status,
            "valid_exact",
            "unknown",
            "blocked_registry_missing_or_invalid",
        ),
        (
            release_state_status,
            "absent_bootstrap_candidate",
            "unknown",
            "blocked_release_state_conflict",
        ),
        (
            offline_validation_status,
            "passed",
            "unknown",
            "blocked_offline_validation_failed",
        ),
    )
    for value, passing, unknown, blocker in ordered:
        if value == passing:
            continue
        if value == unknown:
            return "unknown_outcome_reconciliation_required"
        return blocker
    return "eligible_for_independent_review"


def _selector_audit() -> dict[str, int]:
    vocabularies = (
        CONTRACT_BINDING_STATUSES,
        VALIDATOR_BUNDLE_STATUSES,
        MANIFEST_STATUSES,
        SOURCE_INSTALL_STATUSES,
        REGISTRY_STATUSES,
        RELEASE_STATE_STATUSES,
        OFFLINE_VALIDATION_STATUSES,
    )
    reached: set[str] = set()
    tuple_count = 0
    for values in itertools.product(*vocabularies):
        tuple_count += 1
        terminal = _select_terminal_status(*values)
        if terminal not in TERMINAL_STATUSES:
            raise PacketUnavailableError
        reached.add(terminal)
    if tuple_count != 6480 or reached != set(TERMINAL_STATUSES):
        raise PacketUnavailableError
    return {
        "tuple_count": tuple_count,
        "overlap_count": 0,
        "uncovered_count": 0,
        "unreachable_count": 0,
    }


def _validator_bundle(
    checker_sha256: str,
    checker_test_sha256: str,
    pool: ModuleType,
) -> str:
    bundle = {
        "schema_version": "trusted_owner_r0_validator_bundle.v1",
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": APP_SERVER_CONTRACT_SHA256,
        "app_native_contract_sha256": APP_NATIVE_CONTRACT_SHA256,
        "stage3_manifest_sha256": STAGE3_MANIFEST_SHA256,
        "installer_sha256": INSTALLER_SHA256,
        "r0_contract_sha256": R0_CONTRACT_SHA256,
        "r0_checker_sha256": checker_sha256,
        "r0_checker_test_sha256": checker_test_sha256,
    }
    return hashlib.sha256(pool.trusted_native_canonical_bytes(bundle)).hexdigest()


def _offline_validation_status(owners: OwnerModules) -> str:
    try:
        owners.adapter.validate_fixed_contract_bytes()
        direct_bytes = owners.direct_adapter.validate_fixed_contract_bytes()
        if direct_bytes != {
            "terminal_byte_count": 391,
            "terminal_sha256": (
                "09a3d716d4f14baf67ebc5b4914b7e4daea24d8fd4c5376924859b5885a76e45"
            ),
            "platform_preimage_byte_count": 1489,
            "platform_self_sha256": (
                "c0af9c0be3cd43c4a1db80e1b525749d6c91cb2c8dc057e193c3badf17327918"
            ),
            "platform_artifact_byte_count": 1582,
            "platform_artifact_sha256": (
                "5df194e378dad42d515879fff05c671da3c4852394c2cbb87a3564ef9c33b0e4"
            ),
        }:
            return "failed"
        lifecycle = owners.adapter.validate_lifecycle_registry()
        if lifecycle != {
            "tuple_count": 39,
            "overlap_count": 0,
            "uncovered_count": 0,
            "unreachable_row_count": 0,
            "sha256": (
                "0d50774b0b8cb4f47a11b2cde2919f73ac887dacced761dfa4ebd7ea95e4f517"
            ),
        }:
            return "failed"
        if tuple(owners.pool.TRUSTED_NATIVE_AUTHORITY_FIELDS) != AUTHORITY_FIELDS:
            return "failed"
        if _selector_audit() != {
            "tuple_count": 6480,
            "overlap_count": 0,
            "uncovered_count": 0,
            "unreachable_count": 0,
        }:
            return "failed"
        if owners.pool.trusted_native_canonical_bytes({"known": "answer"}) != (
            b'{"known":"answer"}\n'
        ):
            return "failed"
    except Exception:
        return "failed"
    return "passed"


def _build_packet(
    observations: ComponentObservations,
    pool: ModuleType,
) -> dict[str, object]:
    terminal_status = _select_terminal_status(
        observations.contract_binding_status,
        observations.validator_bundle_status,
        observations.manifest.status,
        observations.source_install_status,
        observations.registry_status,
        observations.release_state_status,
        observations.offline_validation_status,
    )
    packet: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "repository_id": REPOSITORY_ID,
        "repository_name": REPOSITORY_NAME,
        "issue_url": ISSUE_URL,
        "base_commit": BASE_COMMIT,
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": APP_SERVER_CONTRACT_SHA256,
        "r0_contract_sha256": R0_CONTRACT_SHA256,
        "contract_binding_status": observations.contract_binding_status,
        "stage3_manifest_file_count": observations.manifest.file_count,
        "stage3_manifest_byte_count": observations.manifest.canonical_byte_count,
        "stage3_manifest_sha256": observations.manifest.sha256,
        "manifest_status": observations.manifest.status,
        "source_tree_node_count": observations.source_tree.node_count,
        "source_tree_file_count": observations.source_tree.file_count,
        "source_tree_manifest_byte_count": (
            observations.source_tree.canonical_byte_count
        ),
        "source_tree_sha256": observations.source_tree.sha256,
        "installed_tree_node_count": observations.installed_tree.node_count,
        "installed_tree_file_count": observations.installed_tree.file_count,
        "installed_tree_manifest_byte_count": (
            observations.installed_tree.canonical_byte_count
        ),
        "installed_tree_sha256": observations.installed_tree.sha256,
        "source_install_status": observations.source_install_status,
        "registry_status": observations.registry_status,
        "registry_sha256": observations.registry_sha256,
        "release_state_status": observations.release_state_status,
        "release_state_sha256": observations.release_state_sha256,
        "checker_sha256": observations.checker_sha256,
        "checker_test_sha256": observations.checker_test_sha256,
        "validator_bundle_sha256": observations.validator_bundle_sha256,
        "validator_bundle_status": observations.validator_bundle_status,
        "offline_validation_status": observations.offline_validation_status,
        "terminal_status": terminal_status,
        "eligible_for_independent_review": (
            terminal_status == "eligible_for_independent_review"
        ),
        "effect_counts": {field: 0 for field in EFFECT_COUNT_FIELDS},
        "authority_flags": {field: False for field in AUTHORITY_FIELDS},
        "evidence_sha256": "",
    }
    packet["evidence_sha256"] = pool.trusted_native_self_digest(
        packet,
        "evidence_sha256",
    )
    return packet


def _validate_packet(packet: object, pool: ModuleType) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet, dict):
        return ["packet_object_required"]
    if tuple(packet) != RESULT_FIELDS:
        return ["packet_fields_invalid"]
    exact_values = {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "repository_id": REPOSITORY_ID,
        "repository_name": REPOSITORY_NAME,
        "issue_url": ISSUE_URL,
        "base_commit": BASE_COMMIT,
        "profile_contract_sha256": PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": APP_SERVER_CONTRACT_SHA256,
        "r0_contract_sha256": R0_CONTRACT_SHA256,
    }
    for field, expected in exact_values.items():
        if packet[field] != expected:
            errors.append(f"{field}_invalid")
    enum_fields = {
        "contract_binding_status": CONTRACT_BINDING_STATUSES,
        "manifest_status": MANIFEST_STATUSES,
        "source_install_status": SOURCE_INSTALL_STATUSES,
        "registry_status": REGISTRY_STATUSES,
        "release_state_status": RELEASE_STATE_STATUSES,
        "validator_bundle_status": VALIDATOR_BUNDLE_STATUSES,
        "offline_validation_status": OFFLINE_VALIDATION_STATUSES,
        "terminal_status": TERMINAL_STATUSES,
    }
    for field, allowed in enum_fields.items():
        if packet[field] not in allowed:
            errors.append(f"{field}_invalid")
    count_fields = (
        "stage3_manifest_file_count",
        "stage3_manifest_byte_count",
        "source_tree_node_count",
        "source_tree_file_count",
        "source_tree_manifest_byte_count",
        "installed_tree_node_count",
        "installed_tree_file_count",
        "installed_tree_manifest_byte_count",
    )
    for field in count_fields:
        value = packet[field]
        if value is not None and (type(value) is not int or value < 0):
            errors.append(f"{field}_invalid")
    digest_fields = (
        "profile_contract_sha256",
        "app_server_contract_sha256",
        "r0_contract_sha256",
        "stage3_manifest_sha256",
        "source_tree_sha256",
        "installed_tree_sha256",
        "registry_sha256",
        "release_state_sha256",
        "checker_sha256",
        "checker_test_sha256",
        "validator_bundle_sha256",
        "evidence_sha256",
    )
    nullable_digests = {
        "stage3_manifest_sha256",
        "source_tree_sha256",
        "installed_tree_sha256",
        "registry_sha256",
        "release_state_sha256",
    }
    for field in digest_fields:
        value = packet[field]
        if value is None and field in nullable_digests:
            continue
        if not _is_sha256(value):
            errors.append(f"{field}_invalid")
    effect_counts = packet["effect_counts"]
    if (
        not isinstance(effect_counts, dict)
        or tuple(effect_counts) != EFFECT_COUNT_FIELDS
        or any(
            type(value) is not int or value != 0
            for value in effect_counts.values()
        )
    ):
        errors.append("effect_counts_invalid")
    authority_flags = packet["authority_flags"]
    if (
        not isinstance(authority_flags, dict)
        or tuple(authority_flags) != AUTHORITY_FIELDS
        or any(
            type(value) is not bool or value
            for value in authority_flags.values()
        )
    ):
        errors.append("authority_flags_invalid")
    expected_terminal = _select_terminal_status(
        packet["contract_binding_status"],
        packet["validator_bundle_status"],
        packet["manifest_status"],
        packet["source_install_status"],
        packet["registry_status"],
        packet["release_state_status"],
        packet["offline_validation_status"],
    )
    if packet["terminal_status"] != expected_terminal:
        errors.append("terminal_status_inconsistent")
    expected_eligible = expected_terminal == "eligible_for_independent_review"
    if packet["eligible_for_independent_review"] is not expected_eligible:
        errors.append("eligibility_inconsistent")
    if packet["manifest_status"] == "exact" and (
        packet["stage3_manifest_file_count"] != STAGE3_MANIFEST_FILE_COUNT
        or packet["stage3_manifest_byte_count"] != STAGE3_MANIFEST_BYTE_COUNT
        or packet["stage3_manifest_sha256"] != STAGE3_MANIFEST_SHA256
    ):
        errors.append("exact_manifest_projection_invalid")
    reviewed_source_projection = (
        SOURCE_TREE_NODE_COUNT,
        SOURCE_TREE_FILE_COUNT,
        SOURCE_TREE_MANIFEST_BYTE_COUNT,
        SOURCE_TREE_SHA256,
    )
    source_projection = (
        packet["source_tree_node_count"],
        packet["source_tree_file_count"],
        packet["source_tree_manifest_byte_count"],
        packet["source_tree_sha256"],
    )
    installed_projection = (
        packet["installed_tree_node_count"],
        packet["installed_tree_file_count"],
        packet["installed_tree_manifest_byte_count"],
        packet["installed_tree_sha256"],
    )
    for label, projection in (
        ("source", source_projection),
        ("installed", installed_projection),
    ):
        populated = [value is not None for value in projection]
        if any(populated) and not all(populated):
            errors.append(f"{label}_tree_projection_partial")
    if packet["source_install_status"] == "identical" and (
        source_projection != reviewed_source_projection
        or installed_projection != reviewed_source_projection
    ):
        errors.append("identical_tree_projection_invalid")
    if packet["source_install_status"] == "installed_drift" and (
        not all(value is not None for value in source_projection)
        or not all(value is not None for value in installed_projection)
    ):
        errors.append("installed_drift_projection_invalid")
    if packet["source_install_status"] == "installed_missing" and any(
        packet[field] is not None
        for field in (
            "installed_tree_node_count",
            "installed_tree_file_count",
            "installed_tree_manifest_byte_count",
            "installed_tree_sha256",
        )
    ):
        errors.append("installed_missing_projection_invalid")
    if packet["registry_status"] in {"absent", "unknown"} and (
        packet["registry_sha256"] is not None
    ):
        errors.append("registry_digest_projection_invalid")
    if packet["registry_status"] == "valid_exact" and not _is_sha256(
        packet["registry_sha256"]
    ):
        errors.append("valid_registry_digest_missing")
    if packet["release_state_status"] in {
        "absent_bootstrap_candidate",
        "unknown",
    } and packet["release_state_sha256"] is not None:
        errors.append("release_digest_projection_invalid")
    if packet["release_state_status"] in {
        "present_valid_chain",
        "present_invalid_or_forked",
    } and not _is_sha256(packet["release_state_sha256"]):
        errors.append("present_release_digest_missing")
    if (
        _is_sha256(packet["evidence_sha256"])
        and packet["evidence_sha256"]
        != pool.trusted_native_self_digest(packet, "evidence_sha256")
    ):
        errors.append("evidence_digest_mismatch")
    return errors


def _parse_packet(text: str, pool: ModuleType) -> dict[str, object]:
    packet = pool.parse_trusted_native_json(text)
    errors = _validate_packet(packet, pool)
    if errors:
        raise PacketUnavailableError
    return packet


def _evaluate_roots(roots: EvaluationRoots) -> tuple[dict[str, object], bytes]:
    binding_status, observed_bindings = _binding_status(roots.repository_root)
    checker_observation = _read_stable_file(
        roots.repository_root / CHECKER_RELATIVE_PATH
    )
    test_observation = _read_stable_file(
        roots.repository_root / CHECKER_TEST_RELATIVE_PATH
    )
    if (
        checker_observation.state != "exact"
        or checker_observation.payload is None
        or test_observation.state != "exact"
        or test_observation.payload is None
    ):
        raise PacketUnavailableError
    checker_sha256 = hashlib.sha256(checker_observation.payload).hexdigest()
    checker_test_sha256 = hashlib.sha256(test_observation.payload).hexdigest()

    required_owner_names = {
        "installer",
        "registry_validator",
        "stage3_validator",
        "fake_transport",
        "direct_fake_transport",
    }
    if not required_owner_names.issubset(observed_bindings):
        raise PacketUnavailableError
    if any(
        observed_bindings[name]
        != next(
            expected
            for binding_name, _, expected in FILE_BINDINGS
            if binding_name == name
        )
        for name in required_owner_names
    ):
        raise PacketUnavailableError
    owners = _load_owner_modules(roots.repository_root)

    workflow_root = (
        roots.installed_skills_root / "mythic-edge-workflow"
        if roots.installed_skills_root is not None
        else None
    )
    manifest = _manifest_observation(owners.stage3, workflow_root)
    source_tree, installed_tree, source_install_status = _tree_observations(
        roots,
        owners,
    )
    fixed_inputs = _fixed_inputs(roots.repository_root, owners.pool)
    validator_bundle_sha256 = _validator_bundle(
        checker_sha256,
        checker_test_sha256,
        owners.pool,
    )
    if binding_status == "exact":
        validator_bundle_status = "exact"
    elif binding_status == "known_invalid":
        validator_bundle_status = "known_invalid"
    else:
        validator_bundle_status = "unknown"
    offline_validation_status = _offline_validation_status(owners)
    observations = ComponentObservations(
        contract_binding_status=binding_status,
        manifest=manifest,
        source_tree=source_tree,
        installed_tree=installed_tree,
        source_install_status=source_install_status,
        registry_status=fixed_inputs.registry_status,
        registry_sha256=fixed_inputs.registry_sha256,
        release_state_status=fixed_inputs.release_state_status,
        release_state_sha256=fixed_inputs.release_state_sha256,
        checker_sha256=checker_sha256,
        checker_test_sha256=checker_test_sha256,
        validator_bundle_sha256=validator_bundle_sha256,
        validator_bundle_status=validator_bundle_status,
        offline_validation_status=offline_validation_status,
    )
    packet = _build_packet(observations, owners.pool)
    errors = _validate_packet(packet, owners.pool)
    if errors and offline_validation_status == "passed":
        observations = ComponentObservations(
            **{
                **observations.__dict__,
                "offline_validation_status": "failed",
            }
        )
        packet = _build_packet(observations, owners.pool)
        errors = _validate_packet(packet, owners.pool)
    if errors:
        raise PacketUnavailableError
    encoded = owners.pool.trusted_native_canonical_bytes(packet)
    if _parse_packet(encoded.decode("utf-8"), owners.pool) != packet:
        raise PacketUnavailableError
    return packet, encoded


def _production_roots() -> EvaluationRoots:
    checker = Path(__file__).absolute()
    observation = _observe_component(checker, "file")
    if observation.state != "exact":
        raise PacketUnavailableError
    repository_root = checker.parent.parent
    if "CODEX_HOME" in os.environ:
        return EvaluationRoots(repository_root, None)
    installer_path = repository_root / "tools/install_codex_skills.py"
    installer_observation = _read_stable_file(installer_path)
    if (
        installer_observation.state != "exact"
        or installer_observation.payload is None
        or hashlib.sha256(installer_observation.payload).hexdigest()
        != INSTALLER_SHA256
    ):
        raise PacketUnavailableError
    namespace = hashlib.sha256(str(repository_root).encode("utf-8")).hexdigest()[
        :12
    ]
    installer = _load_module(
        f"_r0_root_installer_{namespace}",
        installer_path,
    )
    installed_skills_root = installer._codex_home(None) / "skills"
    return EvaluationRoots(repository_root, installed_skills_root)


def _evaluate_for_tests(roots: EvaluationRoots) -> tuple[dict[str, object], bytes]:
    """Evaluate test-owned roots through the same owner-backed implementation."""

    return _evaluate_roots(roots)


def _exit_code(terminal_status: str) -> int:
    if terminal_status == "eligible_for_independent_review":
        return 0
    if terminal_status == "unknown_outcome_reconciliation_required":
        return 3
    return 2


def _write_exact_bytes(stream: TextIO, payload: bytes) -> None:
    binary_stream = getattr(stream, "buffer", None)
    if binary_stream is None:
        stream.write(payload.decode("utf-8"))
        return
    binary_stream.write(payload)


def run(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments:
        _write_exact_bytes(
            sys.stderr,
            PACKET_UNAVAILABLE.encode("ascii") + b"\n",
        )
        return 3
    try:
        packet, encoded = _evaluate_roots(_production_roots())
    except Exception:
        _write_exact_bytes(
            sys.stderr,
            PACKET_UNAVAILABLE.encode("ascii") + b"\n",
        )
        return 3
    _write_exact_bytes(sys.stdout, encoded)
    return _exit_code(str(packet["terminal_status"]))


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
