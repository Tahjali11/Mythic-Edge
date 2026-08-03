"""Run one fixed, bounded R0 Observation 1 child operation on Windows.

The existing observation owner remains the sole parser and receipt sealer.
This module owns only volatile parent-side launch, process-tree, stream,
timeout, effect, and cleanup observations. Importing it performs no operation.
"""

from __future__ import annotations

import ctypes
import hashlib
import os
import stat
import sys
import time
from collections import Counter
from collections.abc import Mapping, Sequence
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_offline_observation_"
    "trusted_launch_observer.md"
)
PREDECESSOR_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_"
    "observation_successor.md"
)
OWNER_PATH = Path("tools/check_role_pool_r0_offline_observation.py")
OWNER_TEST_PATH = Path("tests/test_check_role_pool_r0_offline_observation.py")
OBSERVER_PATH = Path("tools/run_role_pool_r0_trusted_launch_observer.py")

CONTRACT_SHA256 = "dd1e54709d3d9c33ff957d3057f0840ce8243678ecdcb3f3e1bc9ef140563c34"
FROZEN_BINDINGS = {
    PREDECESSOR_CONTRACT_PATH: (
        "129ceb8f2bb21f4773e8258ad04238784d986c14168179e1d009b30c584588ae"
    ),
    OWNER_PATH: "ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5",
    OWNER_TEST_PATH: (
        "79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784"
    ),
    CONTRACT_PATH: CONTRACT_SHA256,
}

FIXED_LAUNCHER_TOKEN = "py"
FIXED_VERSION_TOKEN = "-3.13"
FIXED_NO_BYTECODE_TOKEN = "-B"
FIXED_CHILD_SCRIPT = "tools/check_role_pool_r0_offline_observation.py"
TIMEOUT_SECONDS = 120.0
TERMINATION_GRACE_SECONDS = 5.0

_STATUS_EXIT_CODES = {
    "observation_safety_boundary_failed": 4,
    "observation_launch_unknown": 3,
    "observation_timeout_unknown": 3,
    "observation_result_unknown": 3,
}
_CLOSED_FAILURE_STATUSES = {
    "observation_binding_rejected",
    "observation_host_rejected",
    "observation_sequence_rejected",
    "observation_launch_unknown",
    "observation_timeout_unknown",
    "observation_safety_boundary_failed",
    "observation_result_unknown",
    "observation_validation_failed",
    "observation_receipt_sealing_failed",
}

_REPARSE_MARKER = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
class _ObserverError(RuntimeError):
    def __init__(self, status: str) -> None:
        super().__init__(status)
        self.status = status


class _SafetyEffect(_ObserverError):
    def __init__(self) -> None:
        super().__init__("observation_safety_boundary_failed")


@dataclass(frozen=True)
class _FileIdentity:
    device: int
    inode: int
    size: int
    modified_ns: int
    sha256: str


@dataclass(frozen=True)
class _StableFileSnapshot:
    payload: bytes
    identity: _FileIdentity


@dataclass(frozen=True)
class _LauncherBinding:
    exact: bool
    application_path: str
    windows_directory: str
    identity: _FileIdentity | None


@dataclass(frozen=True)
class _EffectSnapshot:
    exact: bool
    repository_digest: str
    installed_digest: str
    generated_residue: frozenset[str]


@dataclass(frozen=True)
class _AuditCounts:
    network_operations: int
    repository_writes: int
    installed_writes: int
    external_effects: int


@dataclass(frozen=True)
class _LaunchRequest:
    application_path: str
    launcher_identity: _FileIdentity
    tokens: tuple[str, ...]
    repository_root: Path
    environment: tuple[tuple[str, str], ...]
    timeout_seconds: float
    max_stdout_bytes: int
    max_stderr_bytes: int


@dataclass(frozen=True)
class _JobEvent:
    kind: str
    process_id: int | None


@dataclass(frozen=True)
class _CloseObservation:
    resource: str
    attempt_count: int
    succeeded: bool


@dataclass(frozen=True)
class _LaunchEvidence:
    creation_attempt_count: int
    top_level_created: bool | None
    top_level_process_id: int | None
    job_assigned_at_creation: bool | None
    job_handle_unique: bool | None
    events: tuple[_JobEvent, ...]
    cumulative_process_total: int | None
    active_process_count: int | None
    exit_code: int | None
    stdout: bytes
    stderr: bytes
    stdout_eof: bool
    stderr_eof: bool
    stdout_overflow: bool
    stderr_overflow: bool
    top_level_identity_exact: bool | None
    timed_out: bool
    termination_requested: bool
    termination_succeeded: bool | None
    terminal_wait_succeeded: bool | None
    close_observations: tuple[_CloseObservation, ...]


class TrustedLaunchAdapter(Protocol):
    """Closed seam implemented by the production adapter and test fakes."""

    def runtime_identity(self) -> tuple[str, str]: ...

    def install_audit(self, repository_root: Path) -> None: ...

    def bind_installed_root(self, installed_root: Path) -> None: ...

    def resolve_launcher(self) -> _LauncherBinding: ...

    def snapshot_effects(
        self,
        repository_root: Path,
        installed_root: Path,
        owner: ModuleType,
    ) -> _EffectSnapshot: ...

    def launch_once(self, request: _LaunchRequest) -> _LaunchEvidence: ...

    def audit_counts(self) -> _AuditCounts: ...


def _ordinary_nonreparse(info: os.stat_result, *, directory: bool = False) -> bool:
    expected = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    return (
        expected
        and not stat.S_ISLNK(info.st_mode)
        and not bool(getattr(info, "st_file_attributes", 0) & _REPARSE_MARKER)
    )


def _identity_tuple(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        int(info.st_dev),
        int(info.st_ino),
        int(info.st_mode),
        int(info.st_size),
        int(info.st_mtime_ns),
    )


def _stable_file_snapshot(path: Path) -> _StableFileSnapshot:
    try:
        before = path.lstat()
        if not _ordinary_nonreparse(before):
            raise _ObserverError("observation_binding_rejected")
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            payload = stream.read()
            after_read = os.fstat(stream.fileno())
        after = path.lstat()
    except _ObserverError:
        raise
    except OSError as exc:
        raise _ObserverError("observation_binding_rejected") from exc
    expected = _identity_tuple(before)
    if any(
        _identity_tuple(value) != expected for value in (opened, after_read, after)
    ):
        raise _ObserverError("observation_binding_rejected")
    return _StableFileSnapshot(
        payload=payload,
        identity=_FileIdentity(
            device=int(opened.st_dev),
            inode=int(opened.st_ino),
            size=int(opened.st_size),
            modified_ns=int(opened.st_mtime_ns),
            sha256=hashlib.sha256(payload).hexdigest(),
        ),
    )


def _stable_file_bytes(path: Path) -> bytes:
    return _stable_file_snapshot(path).payload


def _stable_file_identity(path: Path) -> _FileIdentity:
    return _stable_file_snapshot(path).identity


def _repository_root() -> Path:
    module_path = Path(__file__).absolute()
    root = module_path.parent.parent
    if module_path != root / OBSERVER_PATH:
        raise _ObserverError("observation_binding_rejected")
    try:
        info = root.lstat()
    except OSError as exc:
        raise _ObserverError("observation_binding_rejected") from exc
    if not _ordinary_nonreparse(info, directory=True):
        raise _ObserverError("observation_binding_rejected")
    return root


def _load_owner_api(repository_root: Path) -> ModuleType:
    verified_payloads: dict[Path, bytes] = {}
    for relative_path, expected_sha256 in FROZEN_BINDINGS.items():
        payload = _stable_file_bytes(repository_root / relative_path)
        if hashlib.sha256(payload).hexdigest() != expected_sha256:
            raise _ObserverError("observation_binding_rejected")
        verified_payloads[relative_path] = payload
    path = repository_root / OWNER_PATH
    module_name = "_r0_trusted_launch_owner"
    module = ModuleType(module_name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__spec__ = None
    sys.modules[module_name] = module
    try:
        code = compile(
            verified_payloads[OWNER_PATH],
            os.fspath(path),
            "exec",
            dont_inherit=True,
        )
        exec(code, module.__dict__)
    except Exception as exc:
        sys.modules.pop(module_name, None)
        raise _ObserverError("observation_binding_rejected") from exc
    required = (
        "OBSERVATION_IDS",
        "MAX_STDOUT_BYTES",
        "MAX_FAILURE_STDERR_BYTES",
        "PostExitFacts",
        "_post_exit_status",
        "seal_proportionate_observation_receipt",
        "parse_receipt",
        "canonical_bytes",
        "EXPECTED_RECEIPTS",
        "_load_checker",
        "_validate_release_and_reobserve",
    )
    if any(not hasattr(module, name) for name in required):
        raise _ObserverError("observation_binding_rejected")
    observation_ids = module.OBSERVATION_IDS
    if (
        type(observation_ids) is not tuple
        or len(observation_ids) != 2
        or any(type(value) is not str or not value for value in observation_ids)
    ):
        raise _ObserverError("observation_sequence_rejected")
    return module


def _installed_root(owner: ModuleType, repository_root: Path) -> Path:
    try:
        checker = owner._load_checker(repository_root)
        roots = checker._production_roots()
        installed = roots.installed_skills_root
        if type(installed) is not Path:
            raise _ObserverError("observation_binding_rejected")
        info = installed.lstat()
        if not installed.is_absolute() or not _ordinary_nonreparse(info, directory=True):
            raise _ObserverError("observation_binding_rejected")
        owner._validate_release_and_reobserve(checker, roots)
    except _ObserverError:
        raise
    except Exception as exc:
        raise _ObserverError("observation_binding_rejected") from exc
    return installed


def _residue_rows(path: Path, label: str) -> tuple[str, ...]:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return ()
    except OSError as exc:
        raise _ObserverError("observation_result_unknown") from exc
    if not _ordinary_nonreparse(info, directory=True):
        raise _ObserverError("observation_result_unknown")
    rows: list[str] = [f"{label}/"]
    pending = [path]
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda item: item.name)
        except OSError as exc:
            raise _ObserverError("observation_result_unknown") from exc
        child_directories: list[Path] = []
        for entry in entries:
            child = Path(entry.path)
            relative = child.relative_to(path).as_posix()
            try:
                child_info = child.lstat()
            except OSError as exc:
                raise _ObserverError("observation_result_unknown") from exc
            if _ordinary_nonreparse(child_info, directory=True):
                rows.append(f"{label}/{relative}/")
                child_directories.append(child)
            elif _ordinary_nonreparse(child_info):
                rows.append(
                    f"{label}/{relative}|{child_info.st_size}|"
                    f"{child_info.st_mtime_ns}"
                )
            else:
                raise _ObserverError("observation_result_unknown")
        pending.extend(reversed(child_directories))
    return tuple(rows)


def _generated_residue_snapshot(
    repository_root: Path,
    installed_root: Path,
) -> frozenset[str]:
    candidates = (
        (repository_root / ".pytest_cache", "repository/.pytest_cache"),
        (repository_root / "tools/__pycache__", "repository/tools/__pycache__"),
        (repository_root / "tests/__pycache__", "repository/tests/__pycache__"),
        (
            repository_root
            / "docs/codex_skills/mythic-edge-role-pool/scripts/__pycache__",
            "source/scripts/__pycache__",
        ),
        (
            installed_root / "mythic-edge-role-pool/scripts/__pycache__",
            "installed/scripts/__pycache__",
        ),
    )
    return frozenset(
        row
        for path, label in candidates
        for row in _residue_rows(path, label)
    )


def _owned_state_snapshot(
    owner: ModuleType,
    repository_root: Path,
    installed_root: Path,
) -> _EffectSnapshot:
    checker = owner._load_checker(repository_root)
    roots = checker._production_roots()
    if os.path.normcase(os.path.abspath(roots.installed_skills_root)) != os.path.normcase(
        os.path.abspath(installed_root)
    ):
        raise _ObserverError("observation_binding_rejected")
    owner._validate_release_and_reobserve(checker, roots)
    owners = checker._load_owner_modules(repository_root)
    binding_status, observed_bindings = checker._binding_status(repository_root)
    manifest = checker._manifest_observation(
        owners.stage3,
        installed_root / "mythic-edge-workflow",
    )
    source, installed, source_install = checker._tree_observations(roots, owners)
    fixed = checker._fixed_inputs(repository_root, owners.pool)
    repository_state = (
        binding_status,
        tuple(sorted(observed_bindings.items())),
        source.node_count,
        source.file_count,
        source.canonical_byte_count,
        source.sha256,
        source.status,
        source_install,
        fixed.registry_status,
        fixed.registry_sha256,
        fixed.release_state_status,
        fixed.release_state_sha256,
    )
    installed_state = (
        manifest.file_count,
        manifest.canonical_byte_count,
        manifest.sha256,
        manifest.status,
        installed.node_count,
        installed.file_count,
        installed.canonical_byte_count,
        installed.sha256,
        installed.status,
    )
    return _EffectSnapshot(
        exact=True,
        repository_digest=hashlib.sha256(
            repr(repository_state).encode("ascii")
        ).hexdigest(),
        installed_digest=hashlib.sha256(
            repr(installed_state).encode("ascii")
        ).hexdigest(),
        generated_residue=_generated_residue_snapshot(
            repository_root,
            installed_root,
        ),
    )


def _fixed_environment(windows_directory: str) -> tuple[tuple[str, str], ...]:
    if not windows_directory or "\0" in windows_directory:
        raise _ObserverError("observation_binding_rejected")
    return (
        ("PYTHONDONTWRITEBYTECODE", "1"),
        ("SYSTEMROOT", windows_directory),
    )


def _fixed_request(
    owner: ModuleType,
    repository_root: Path,
    launcher: _LauncherBinding,
) -> _LaunchRequest:
    if not launcher.exact or launcher.identity is None:
        raise _ObserverError("observation_binding_rejected")
    return _LaunchRequest(
        application_path=launcher.application_path,
        launcher_identity=launcher.identity,
        tokens=(
            FIXED_LAUNCHER_TOKEN,
            FIXED_VERSION_TOKEN,
            FIXED_NO_BYTECODE_TOKEN,
            FIXED_CHILD_SCRIPT,
            owner.OBSERVATION_IDS[0],
        ),
        repository_root=repository_root,
        environment=_fixed_environment(launcher.windows_directory),
        timeout_seconds=TIMEOUT_SECONDS,
        max_stdout_bytes=owner.MAX_STDOUT_BYTES,
        max_stderr_bytes=owner.MAX_FAILURE_STDERR_BYTES,
    )


def _close_state_exact(observations: tuple[_CloseObservation, ...]) -> bool:
    names = [item.resource for item in observations]
    return (
        frozenset(names) == _SUCCESS_CLOSE_RESOURCES
        and len(names) == len(_SUCCESS_CLOSE_RESOURCES)
        and all(
            type(item.resource) is str
            and bool(item.resource)
            and item.attempt_count == 1
            and type(item.succeeded) is bool
            and item.succeeded
            for item in observations
        )
    )


def _process_projection(
    evidence: _LaunchEvidence,
) -> tuple[int, bool, bool, int]:
    top_id = evidence.top_level_process_id
    valid_kinds = {"new", "exit", "active_zero", "active_limit"}
    events_valid = all(event.kind in valid_kinds for event in evidence.events)
    events_valid = events_valid and all(
        (
            type(event.process_id) is int and event.process_id > 0
            if event.kind in {"new", "exit"}
            else event.process_id is None
        )
        for event in evidence.events
    )
    new_ids = [event.process_id for event in evidence.events if event.kind == "new"]
    exit_ids = [event.process_id for event in evidence.events if event.kind == "exit"]
    active_zero_count = sum(event.kind == "active_zero" for event in evidence.events)
    active_limit_count = sum(event.kind == "active_limit" for event in evidence.events)
    total = evidence.cumulative_process_total
    relationships_known = (
        evidence.creation_attempt_count == 1
        and evidence.top_level_created is True
        and type(top_id) is int
        and top_id > 0
        and evidence.job_assigned_at_creation is True
        and evidence.job_handle_unique is True
        and events_valid
        and len(new_ids) == len(set(new_ids))
        and active_limit_count == 0
        and new_ids.count(top_id) == 1
        and type(total) is int
        and total >= 1
        and total == len(new_ids)
    )
    descendant_count = total - 1 if relationships_known else 0
    terminal_known = (
        relationships_known
        and len(exit_ids) == len(set(exit_ids))
        and set(exit_ids) == set(new_ids)
        and active_zero_count == 1
        and evidence.active_process_count == 0
        and evidence.terminal_wait_succeeded is True
        and type(evidence.exit_code) is int
    )
    active = evidence.active_process_count
    survivor_count = active if type(active) is int and active >= 0 else 1
    return descendant_count, relationships_known, terminal_known, survivor_count


def _post_exit_facts(
    owner: ModuleType,
    evidence: _LaunchEvidence,
    before: _EffectSnapshot,
    after: _EffectSnapshot,
    audit: _AuditCounts,
) -> object:
    descendants, relationships, terminal, survivors = _process_projection(evidence)
    snapshots_exact = before.exact and after.exact
    repository_writes = audit.repository_writes + int(
        snapshots_exact and before.repository_digest != after.repository_digest
    )
    installed_writes = audit.installed_writes + int(
        snapshots_exact and before.installed_digest != after.installed_digest
    )
    generated_residue = (
        len(after.generated_residue - before.generated_residue)
        if snapshots_exact
        else 1
    )
    output_drained = evidence.stdout_eof and evidence.stderr_eof
    output_complete = (
        output_drained
        and not evidence.stdout_overflow
        and not evidence.stderr_overflow
        and len(evidence.stdout) <= owner.MAX_STDOUT_BYTES
        and len(evidence.stderr) <= owner.MAX_FAILURE_STDERR_BYTES
    )
    termination_uncertain = (
        evidence.termination_succeeded is False
        or (evidence.termination_requested and evidence.termination_succeeded is not True)
        or evidence.terminal_wait_succeeded is not True
    )
    cleanup_confirmed = (
        snapshots_exact
        and terminal
        and survivors == 0
        and output_drained
        and _close_state_exact(evidence.close_observations)
        and not termination_uncertain
    )
    return owner.PostExitFacts(
        top_level_process_count=int(
            evidence.creation_attempt_count == 1 and evidence.top_level_created is True
        ),
        descendant_process_count=descendants,
        process_relationships_known=relationships,
        process_terminal_states_known=terminal,
        surviving_process_count=survivors,
        top_level_identity_exact=evidence.top_level_identity_exact,
        timed_out=evidence.timed_out,
        termination_uncertain=termination_uncertain,
        cleanup_confirmed=cleanup_confirmed,
        output_complete=output_complete,
        executor_network_operation_count=audit.network_operations,
        repository_write_count=repository_writes,
        installed_write_count=installed_writes,
        external_effect_count=audit.external_effects,
        generated_residue_count=generated_residue,
    )


def _receipt_is_exact(owner: ModuleType, payload: bytes) -> bool:
    try:
        receipt = owner.parse_receipt(payload)
        expected = tuple(
            owner.canonical_bytes(value) for value in owner.EXPECTED_RECEIPTS[0]
        )
    except _SafetyEffect:
        raise
    except Exception:
        return False
    return (
        receipt.get("sequence_position") == 1
        and receipt.get("observation_id") == owner.OBSERVATION_IDS[0]
        and payload in expected
    )


def _run_observation_1(adapter: TrustedLaunchAdapter) -> bytes | str:
    """Derive and seal Observation 1 from one closed adapter operation."""

    try:
        if adapter.runtime_identity() != ("nt", "win32"):
            return "observation_host_rejected"
        if not sys.dont_write_bytecode:
            return "observation_binding_rejected"
        repository_root = _repository_root()
        owner = _load_owner_api(repository_root)
        adapter.install_audit(repository_root)
        installed_root = _installed_root(owner, repository_root)
        adapter.bind_installed_root(installed_root)
        before = adapter.snapshot_effects(repository_root, installed_root, owner)
        if not before.exact:
            return "observation_binding_rejected"
        request = _fixed_request(owner, repository_root, adapter.resolve_launcher())
    except _SafetyEffect as exc:
        return exc.status
    except _ObserverError as exc:
        return exc.status
    except Exception:
        return "observation_binding_rejected"

    try:
        evidence = adapter.launch_once(request)
    except _SafetyEffect as exc:
        return exc.status
    except _ObserverError as exc:
        return exc.status
    except Exception:
        return "observation_launch_unknown"

    try:
        after = adapter.snapshot_effects(repository_root, installed_root, owner)
        facts = _post_exit_facts(
            owner,
            evidence,
            before,
            after,
            adapter.audit_counts(),
        )
        status = owner._post_exit_status(facts)
    except _SafetyEffect as exc:
        return exc.status
    except Exception:
        return "observation_timeout_unknown"
    if status != "accepted_exact_r0_offline_observation":
        return status if status in _CLOSED_FAILURE_STATUSES else "observation_result_unknown"
    if evidence.exit_code == 4:
        return "observation_safety_boundary_failed"
    if evidence.exit_code == 3:
        return "observation_result_unknown"
    if evidence.exit_code != 0 or evidence.stderr:
        return "observation_validation_failed"
    try:
        sealed = owner.seal_proportionate_observation_receipt(
            evidence.stdout,
            facts,
            1,
        )
    except _SafetyEffect as exc:
        return exc.status
    except Exception:
        return "observation_result_unknown"
    if type(sealed) is str:
        return sealed if sealed in _CLOSED_FAILURE_STATUSES else "observation_result_unknown"
    if type(sealed) is not bytes or not _receipt_is_exact(owner, sealed):
        return "observation_receipt_sealing_failed"
    return sealed


class _AuditCounter:
    _PROCESS_EVENTS = {
        "subprocess.Popen",
        "os.system",
        "os.posix_spawn",
        "os.posix_spawnp",
        "os.startfile",
        "os.startfile/2",
    }
    _MUTATION_EVENTS = {
        "os.remove",
        "os.rename",
        "os.renames",
        "os.replace",
        "os.rmdir",
        "os.mkdir",
        "os.link",
        "os.symlink",
        "os.truncate",
        "os.chmod",
        "os.chown",
        "os.utime",
        "shutil.copyfile",
        "shutil.rmtree",
        "shutil.move",
    }
    _DESTINATION_MUTATION_EVENTS = {
        "os.rename",
        "os.renames",
        "os.replace",
        "os.link",
        "os.symlink",
        "shutil.copyfile",
        "shutil.move",
    }
    _ENVIRONMENT_EVENTS = {"os.putenv", "os.unsetenv"}

    def __init__(self, repository_root: Path) -> None:
        self._repository_root = os.path.normcase(os.path.abspath(repository_root))
        self._installed_root: str | None = None
        self._counts: Counter[str] = Counter()

    def bind_installed_root(self, installed_root: Path) -> None:
        self._installed_root = os.path.normcase(os.path.abspath(installed_root))

    @staticmethod
    def _within(path: object, root: str | None) -> bool:
        if root is None or not isinstance(path, (str, bytes, os.PathLike)):
            return False
        try:
            candidate = os.path.normcase(os.path.abspath(os.fspath(path)))
            return os.path.commonpath((candidate, root)) == root
        except (OSError, TypeError, ValueError):
            return False

    @staticmethod
    def _write_open(args: tuple[object, ...]) -> bool:
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        if isinstance(mode, str) and any(marker in mode for marker in "wax+"):
            return True
        write_flags = (
            os.O_WRONLY
            | os.O_RDWR
            | os.O_APPEND
            | os.O_CREAT
            | os.O_TRUNC
            | os.O_EXCL
        )
        return isinstance(flags, int) and bool(flags & write_flags)

    def _record_write(self, path: object) -> None:
        if self._within(path, self._repository_root):
            self._counts["repository"] += 1
        elif self._within(path, self._installed_root):
            self._counts["installed"] += 1
        else:
            self._counts["external"] += 1
        raise _SafetyEffect

    def __call__(self, event: str, args: tuple[object, ...]) -> None:
        if event in self._PROCESS_EVENTS or event.startswith("os.spawn"):
            self._counts["external"] += 1
            raise _SafetyEffect
        if event.startswith("socket."):
            self._counts["network"] += 1
            raise _SafetyEffect
        if event in self._ENVIRONMENT_EVENTS:
            self._counts["external"] += 1
            raise _SafetyEffect
        if event == "open" and self._write_open(args):
            self._record_write(args[0] if args else None)
        if event in self._MUTATION_EVENTS:
            path_index = 1 if event in self._DESTINATION_MUTATION_EVENTS else 0
            self._record_write(args[path_index] if len(args) > path_index else None)

    def snapshot(self) -> _AuditCounts:
        return _AuditCounts(
            network_operations=self._counts["network"],
            repository_writes=self._counts["repository"],
            installed_writes=self._counts["installed"],
            external_effects=self._counts["external"],
        )


# Native declarations stay below the pure projection. Importing the module does
# not instantiate a Windows API, create a handle, or launch a process.

HANDLE_FLAG_INHERIT = 0x00000001
GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
STARTF_USESTDHANDLES = 0x00000100
PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
PROC_THREAD_ATTRIBUTE_JOB_LIST = 0x0002000D
CREATE_NO_WINDOW = 0x08000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT = 3
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO = 4
JOB_OBJECT_MSG_NEW_PROCESS = 6
JOB_OBJECT_MSG_EXIT_PROCESS = 7
JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS = 8
JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS = 1
JOB_OBJECT_ASSOCIATE_COMPLETION_PORT_INFORMATION_CLASS = 7
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 258
ERROR_BROKEN_PIPE = 109
STILL_ACTIVE = 259

_SUCCESS_CLOSE_RESOURCES = frozenset(
    {
        "attribute_list",
        "completion_port",
        "job",
        "launcher_guard",
        "process",
        "stderr_read",
        "stderr_write",
        "stdin_read",
        "stdin_write",
        "stdout_read",
        "stdout_write",
        "thread",
    }
)


class _SecurityAttributes(ctypes.Structure):
    _fields_ = (
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", wintypes.LPVOID),
        ("bInheritHandle", wintypes.BOOL),
    )


class _StartupInfoW(ctypes.Structure):
    _fields_ = (
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    )


class _StartupInfoExW(ctypes.Structure):
    _fields_ = (("StartupInfo", _StartupInfoW), ("lpAttributeList", wintypes.LPVOID))


class _ProcessInformation(ctypes.Structure):
    _fields_ = (
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    )


class _IoCounters(ctypes.Structure):
    _fields_ = tuple(
        (name, ctypes.c_ulonglong)
        for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        )
    )


class _JobBasicLimitInformation(ctypes.Structure):
    _fields_ = (
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    )


class _JobExtendedLimitInformation(ctypes.Structure):
    _fields_ = (
        ("BasicLimitInformation", _JobBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    )


class _JobAssociateCompletionPort(ctypes.Structure):
    _fields_ = (
        ("CompletionKey", wintypes.LPVOID),
        ("CompletionPort", wintypes.HANDLE),
    )


class _JobBasicAccountingInformation(ctypes.Structure):
    _fields_ = (
        ("TotalUserTime", ctypes.c_longlong),
        ("TotalKernelTime", ctypes.c_longlong),
        ("ThisPeriodTotalUserTime", ctypes.c_longlong),
        ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    )


class _OwnedHandle:
    def __init__(self, kernel32: object, name: str, value: int | None) -> None:
        self.kernel32 = kernel32
        self.name = name
        self.value = 0 if value is None else int(value)
        self.attempt_count = 0
        self.succeeded = False

    @property
    def open(self) -> bool:
        invalid = {-1, int(ctypes.c_void_p(-1).value or -1)}
        return bool(self.value) and self.value not in invalid and self.attempt_count == 0

    def close(self) -> bool:
        if self.attempt_count:
            return self.succeeded
        self.attempt_count = 1
        if not self.value or self.value == -1:
            self.succeeded = True
        else:
            try:
                self.succeeded = bool(
                    self.kernel32.CloseHandle(wintypes.HANDLE(self.value))
                )
            except BaseException:
                self.succeeded = False
        self.value = 0
        return self.succeeded

    def observation(self) -> _CloseObservation:
        return _CloseObservation(self.name, self.attempt_count, self.succeeded)


class _OwnedAttributeList:
    def __init__(self, kernel32: object) -> None:
        self.kernel32 = kernel32
        self.buffer: object | None = None
        self.pointer: object | None = None
        self.attempt_count = 0
        self.succeeded = False

    def initialize(self) -> object:
        size = ctypes.c_size_t()
        self.kernel32.InitializeProcThreadAttributeList(
            None,
            2,
            0,
            ctypes.byref(size),
        )
        if not size.value:
            raise _ObserverError("observation_launch_unknown")
        self.buffer = ctypes.create_string_buffer(size.value)
        self.pointer = ctypes.cast(self.buffer, wintypes.LPVOID)
        if not self.kernel32.InitializeProcThreadAttributeList(
            self.pointer,
            2,
            0,
            ctypes.byref(size),
        ):
            raise _ObserverError("observation_launch_unknown")
        return self.pointer

    def close(self) -> bool:
        if self.attempt_count:
            return self.succeeded
        self.attempt_count = 1
        if self.pointer is None:
            self.succeeded = True
        else:
            try:
                self.kernel32.DeleteProcThreadAttributeList(self.pointer)
                self.succeeded = True
            except BaseException:
                self.succeeded = False
        self.pointer = None
        self.buffer = None
        return self.succeeded

    def observation(self) -> _CloseObservation:
        return _CloseObservation(
            "attribute_list",
            self.attempt_count,
            self.succeeded,
        )


def _kernel32() -> object:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetWindowsDirectoryW.argtypes = (wintypes.LPWSTR, wintypes.UINT)
    kernel32.GetWindowsDirectoryW.restype = wintypes.UINT
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.CreatePipe.argtypes = (
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(_SecurityAttributes),
        wintypes.DWORD,
    )
    kernel32.CreatePipe.restype = wintypes.BOOL
    kernel32.SetHandleInformation.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
    )
    kernel32.SetHandleInformation.restype = wintypes.BOOL
    kernel32.CreateJobObjectW.argtypes = (wintypes.LPVOID, wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.CreateIoCompletionPort.argtypes = (
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.c_size_t,
        wintypes.DWORD,
    )
    kernel32.CreateIoCompletionPort.restype = wintypes.HANDLE
    kernel32.InitializeProcThreadAttributeList.argtypes = (
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_size_t),
    )
    kernel32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
    kernel32.UpdateProcThreadAttribute.argtypes = (
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.c_size_t,
        wintypes.LPVOID,
        ctypes.c_size_t,
        wintypes.LPVOID,
        ctypes.POINTER(ctypes.c_size_t),
    )
    kernel32.UpdateProcThreadAttribute.restype = wintypes.BOOL
    kernel32.DeleteProcThreadAttributeList.argtypes = (wintypes.LPVOID,)
    kernel32.DeleteProcThreadAttributeList.restype = None
    kernel32.CreateProcessW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.BOOL,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.LPCWSTR,
        ctypes.POINTER(_StartupInfoW),
        ctypes.POINTER(_ProcessInformation),
    )
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.GetQueuedCompletionStatus.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(wintypes.LPVOID),
        wintypes.DWORD,
    )
    kernel32.GetQueuedCompletionStatus.restype = wintypes.BOOL
    kernel32.PeekNamedPipe.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.PeekNamedPipe.restype = wintypes.BOOL
    kernel32.ReadFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.GetExitCodeProcess.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.QueryFullProcessImageNameW.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def _windows_directory(kernel32: object) -> str:
    capacity = 32768
    buffer = ctypes.create_unicode_buffer(capacity)
    length = int(kernel32.GetWindowsDirectoryW(buffer, capacity))
    if length <= 0 or length >= capacity:
        raise _ObserverError("observation_binding_rejected")
    value = buffer.value
    if not value or "\0" in value:
        raise _ObserverError("observation_binding_rejected")
    return value


def _quote_windows_argument(value: str) -> str:
    if not value or any(character in value for character in ' \t"'):
        result = '"'
        backslashes = 0
        for character in value:
            if character == "\\":
                backslashes += 1
                continue
            if character == '"':
                result += "\\" * (backslashes * 2 + 1) + '"'
            else:
                result += "\\" * backslashes + character
            backslashes = 0
        return result + "\\" * (backslashes * 2) + '"'
    return value


def _command_line(tokens: tuple[str, ...]) -> str:
    if any(not token or "\0" in token for token in tokens):
        raise _ObserverError("observation_binding_rejected")
    return " ".join(_quote_windows_argument(token) for token in tokens)


def _environment_block(environment: tuple[tuple[str, str], ...]) -> object:
    names = [name.upper() for name, _ in environment]
    if len(names) != len(set(names)):
        raise _ObserverError("observation_binding_rejected")
    if any(
        not name
        or "=" in name
        or "\0" in name
        or "\0" in value
        for name, value in environment
    ):
        raise _ObserverError("observation_binding_rejected")
    text = "\0".join(f"{name}={value}" for name, value in environment) + "\0"
    return ctypes.create_unicode_buffer(text, len(text) + 1)


def _create_pipe(
    kernel32: object,
    security: _SecurityAttributes,
    read_name: str,
    write_name: str,
) -> tuple[_OwnedHandle, _OwnedHandle]:
    read = wintypes.HANDLE()
    write = wintypes.HANDLE()
    if not kernel32.CreatePipe(
        ctypes.byref(read),
        ctypes.byref(write),
        ctypes.byref(security),
        0,
    ):
        raise _ObserverError("observation_launch_unknown")
    return (
        _OwnedHandle(kernel32, read_name, cast(int, read.value)),
        _OwnedHandle(kernel32, write_name, cast(int, write.value)),
    )


def _open_launcher_guard(kernel32: object, path: Path) -> _OwnedHandle:
    guard = _OwnedHandle(
        kernel32,
        "launcher_guard",
        cast(
            int,
            kernel32.CreateFileW(
                os.fspath(path),
                GENERIC_READ,
                FILE_SHARE_READ,
                None,
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            ),
        ),
    )
    if not guard.open:
        raise _ObserverError("observation_binding_rejected")
    return guard


def _make_parent_end_noninheritable(kernel32: object, handle: _OwnedHandle) -> None:
    if not handle.open or not kernel32.SetHandleInformation(
        wintypes.HANDLE(handle.value),
        HANDLE_FLAG_INHERIT,
        0,
    ):
        raise _ObserverError("observation_launch_unknown")


def _query_accounting(
    kernel32: object,
    job: _OwnedHandle,
) -> tuple[int | None, int | None]:
    information = _JobBasicAccountingInformation()
    if not kernel32.QueryInformationJobObject(
        wintypes.HANDLE(job.value),
        JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION_CLASS,
        ctypes.byref(information),
        ctypes.sizeof(information),
        None,
    ):
        return None, None
    return int(information.TotalProcesses), int(information.ActiveProcesses)


def _drain_events(
    kernel32: object,
    completion_port: _OwnedHandle,
    events: list[_JobEvent],
) -> bool:
    while True:
        message = wintypes.DWORD()
        key = ctypes.c_size_t()
        overlapped = wintypes.LPVOID()
        ok = kernel32.GetQueuedCompletionStatus(
            wintypes.HANDLE(completion_port.value),
            ctypes.byref(message),
            ctypes.byref(key),
            ctypes.byref(overlapped),
            0,
        )
        if not ok:
            return ctypes.get_last_error() == WAIT_TIMEOUT
        process_id = ctypes.cast(overlapped, ctypes.c_void_p).value
        if message.value == JOB_OBJECT_MSG_NEW_PROCESS:
            events.append(_JobEvent("new", int(process_id or 0)))
        elif message.value in {
            JOB_OBJECT_MSG_EXIT_PROCESS,
            JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS,
        }:
            events.append(_JobEvent("exit", int(process_id or 0)))
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
            events.append(_JobEvent("active_zero", None))
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT:
            events.append(_JobEvent("active_limit", None))
        else:
            return False


def _drain_pipe(
    kernel32: object,
    handle: _OwnedHandle,
    buffer: bytearray,
    limit: int,
) -> tuple[bool, bool, bool]:
    eof = False
    overflow = False
    while True:
        available = wintypes.DWORD()
        if not kernel32.PeekNamedPipe(
            wintypes.HANDLE(handle.value),
            None,
            0,
            None,
            ctypes.byref(available),
            None,
        ):
            if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
                eof = True
                break
            return eof, overflow, False
        if available.value == 0:
            break
        read_size = min(int(available.value), 65536)
        chunk = ctypes.create_string_buffer(read_size)
        read = wintypes.DWORD()
        if not kernel32.ReadFile(
            wintypes.HANDLE(handle.value),
            chunk,
            read_size,
            ctypes.byref(read),
            None,
        ):
            if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
                eof = True
                break
            return eof, overflow, False
        payload = chunk.raw[: read.value]
        room = max(0, limit - len(buffer))
        buffer.extend(payload[:room])
        if len(payload) > room:
            overflow = True
            break
    return eof, overflow, True


def _query_process_identity(
    kernel32: object,
    process: _OwnedHandle,
    expected: _FileIdentity,
) -> bool | None:
    capacity = wintypes.DWORD(32768)
    buffer = ctypes.create_unicode_buffer(capacity.value)
    if not kernel32.QueryFullProcessImageNameW(
        wintypes.HANDLE(process.value),
        0,
        buffer,
        ctypes.byref(capacity),
    ):
        return None
    try:
        actual = _stable_file_identity(Path(buffer.value))
    except _ObserverError:
        return None
    return actual == expected


def _close_all(
    handles: Mapping[str, _OwnedHandle],
    attributes: _OwnedAttributeList,
) -> tuple[_CloseObservation, ...]:
    for name in sorted(handles):
        handles[name].close()
    attributes.close()
    return tuple(
        [handles[name].observation() for name in sorted(handles)]
        + [attributes.observation()]
    )


def _failed_launch_evidence(
    handles: Mapping[str, _OwnedHandle],
    attributes: _OwnedAttributeList,
    creation_attempt_count: int,
) -> _LaunchEvidence:
    return _LaunchEvidence(
        creation_attempt_count=creation_attempt_count,
        top_level_created=False,
        top_level_process_id=None,
        job_assigned_at_creation=None,
        job_handle_unique=True,
        events=(),
        cumulative_process_total=None,
        active_process_count=None,
        exit_code=None,
        stdout=b"",
        stderr=b"",
        stdout_eof=False,
        stderr_eof=False,
        stdout_overflow=False,
        stderr_overflow=False,
        top_level_identity_exact=None,
        timed_out=False,
        termination_requested=False,
        termination_succeeded=None,
        terminal_wait_succeeded=None,
        close_observations=_close_all(handles, attributes),
    )


def _execute_windows_once(
    request: _LaunchRequest,
    kernel32: object,
    launcher_guard: _OwnedHandle,
) -> _LaunchEvidence:
    handles: dict[str, _OwnedHandle] = {"launcher_guard": launcher_guard}
    attributes = _OwnedAttributeList(kernel32)
    information = _ProcessInformation()
    creation_attempts = 0
    created = False
    termination_requested = False
    termination_succeeded: bool | None = None
    timed_out = False
    events: list[_JobEvent] = []
    stdout_buffer = bytearray()
    stderr_buffer = bytearray()
    stdout_eof = False
    stderr_eof = False
    stdout_overflow = False
    stderr_overflow = False
    event_stream_exact = True
    process_stopped = False
    identity_exact: bool | None = None
    total: int | None = None
    active: int | None = None
    exit_code: int | None = None
    try:
        security = _SecurityAttributes(ctypes.sizeof(_SecurityAttributes), None, True)
        handles["stdin_read"], handles["stdin_write"] = _create_pipe(
            kernel32,
            security,
            "stdin_read",
            "stdin_write",
        )
        handles["stdout_read"], handles["stdout_write"] = _create_pipe(
            kernel32,
            security,
            "stdout_read",
            "stdout_write",
        )
        handles["stderr_read"], handles["stderr_write"] = _create_pipe(
            kernel32,
            security,
            "stderr_read",
            "stderr_write",
        )
        for name in ("stdin_write", "stdout_read", "stderr_read"):
            _make_parent_end_noninheritable(kernel32, handles[name])
        handles["job"] = _OwnedHandle(
            kernel32,
            "job",
            cast(int, kernel32.CreateJobObjectW(None, None)),
        )
        if not handles["job"].open:
            raise _ObserverError("observation_launch_unknown")
        limits = _JobExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = (
            JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        limits.BasicLimitInformation.ActiveProcessLimit = 2
        if not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            raise _ObserverError("observation_launch_unknown")
        invalid_handle = wintypes.HANDLE(ctypes.c_void_p(-1).value)
        handles["completion_port"] = _OwnedHandle(
            kernel32,
            "completion_port",
            cast(int, kernel32.CreateIoCompletionPort(invalid_handle, None, 0, 1)),
        )
        if not handles["completion_port"].open:
            raise _ObserverError("observation_launch_unknown")
        association = _JobAssociateCompletionPort(
            None,
            wintypes.HANDLE(handles["completion_port"].value),
        )
        if not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_ASSOCIATE_COMPLETION_PORT_INFORMATION_CLASS,
            ctypes.byref(association),
            ctypes.sizeof(association),
        ):
            raise _ObserverError("observation_launch_unknown")
        attribute_list = attributes.initialize()
        inherited = (wintypes.HANDLE * 3)(
            wintypes.HANDLE(handles["stdin_read"].value),
            wintypes.HANDLE(handles["stdout_write"].value),
            wintypes.HANDLE(handles["stderr_write"].value),
        )
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
            ctypes.byref(inherited),
            ctypes.sizeof(inherited),
            None,
            None,
        ):
            raise _ObserverError("observation_launch_unknown")
        jobs = (wintypes.HANDLE * 1)(wintypes.HANDLE(handles["job"].value))
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_JOB_LIST,
            ctypes.byref(jobs),
            ctypes.sizeof(jobs),
            None,
            None,
        ):
            raise _ObserverError("observation_launch_unknown")
        startup = _StartupInfoExW()
        startup.StartupInfo.cb = ctypes.sizeof(startup)
        startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
        startup.StartupInfo.hStdInput = wintypes.HANDLE(handles["stdin_read"].value)
        startup.StartupInfo.hStdOutput = wintypes.HANDLE(handles["stdout_write"].value)
        startup.StartupInfo.hStdError = wintypes.HANDLE(handles["stderr_write"].value)
        startup.lpAttributeList = attribute_list
        handles["stdin_write"].close()
        command_line = ctypes.create_unicode_buffer(_command_line(request.tokens))
        environment = _environment_block(request.environment)
        creation_attempts = 1
        deadline = time.monotonic() + request.timeout_seconds
        created = bool(
            kernel32.CreateProcessW(
                request.application_path,
                command_line,
                None,
                None,
                True,
                (
                    CREATE_NO_WINDOW
                    | CREATE_UNICODE_ENVIRONMENT
                    | EXTENDED_STARTUPINFO_PRESENT
                ),
                ctypes.cast(environment, wintypes.LPVOID),
                os.fspath(request.repository_root),
                ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_StartupInfoW)),
                ctypes.byref(information),
            )
        )
        if not created:
            return _failed_launch_evidence(handles, attributes, creation_attempts)
        handles["process"] = _OwnedHandle(
            kernel32,
            "process",
            cast(int, information.hProcess),
        )
        handles["thread"] = _OwnedHandle(
            kernel32,
            "thread",
            cast(int, information.hThread),
        )
        if not handles["process"].open or not handles["thread"].open:
            raise _ObserverError("observation_launch_unknown")
        attributes.close()
        for name in ("stdin_read", "stdout_write", "stderr_write", "thread"):
            handles[name].close()
        identity_exact = _query_process_identity(
            kernel32,
            handles["process"],
            request.launcher_identity,
        )
        grace_deadline: float | None = None
        while True:
            event_stream_exact = (
                _drain_events(kernel32, handles["completion_port"], events)
                and event_stream_exact
            )
            out_eof, out_overflow, out_exact = _drain_pipe(
                kernel32,
                handles["stdout_read"],
                stdout_buffer,
                request.max_stdout_bytes,
            )
            err_eof, err_overflow, err_exact = _drain_pipe(
                kernel32,
                handles["stderr_read"],
                stderr_buffer,
                request.max_stderr_bytes,
            )
            stdout_eof = stdout_eof or out_eof
            stderr_eof = stderr_eof or err_eof
            stdout_overflow = stdout_overflow or out_overflow or not out_exact
            stderr_overflow = stderr_overflow or err_overflow or not err_exact
            wait = kernel32.WaitForSingleObject(
                wintypes.HANDLE(handles["process"].value),
                0,
            )
            process_stopped = wait == WAIT_OBJECT_0
            total, active = _query_accounting(kernel32, handles["job"])
            known_new = sum(event.kind == "new" for event in events)
            unsafe = (
                stdout_overflow
                or stderr_overflow
                or not event_stream_exact
                or any(event.kind == "active_limit" for event in events)
                or known_new > 2
                or (type(total) is int and total > 2)
            )
            now = time.monotonic()
            complete = (
                process_stopped
                and active == 0
                and stdout_eof
                and stderr_eof
                and any(event.kind == "active_zero" for event in events)
            )
            if now >= deadline:
                timed_out = True
                unsafe = True
            if unsafe and not termination_requested:
                termination_requested = True
                termination_succeeded = bool(
                    kernel32.TerminateJobObject(
                        wintypes.HANDLE(handles["job"].value),
                        1,
                    )
                )
                grace_deadline = now + TERMINATION_GRACE_SECONDS
            if complete:
                break
            if grace_deadline is not None and now >= grace_deadline:
                break
            time.sleep(0.01)
    except BaseException:
        event_stream_exact = False
        if information.hProcess and "process" not in handles:
            handles["process"] = _OwnedHandle(
                kernel32,
                "process",
                cast(int, information.hProcess),
            )
            created = True
        if information.hThread and "thread" not in handles:
            handles["thread"] = _OwnedHandle(
                kernel32,
                "thread",
                cast(int, information.hThread),
            )
            created = True
        if created and "job" in handles and handles["job"].open:
            if not termination_requested:
                termination_requested = True
                try:
                    termination_succeeded = bool(
                        kernel32.TerminateJobObject(
                            wintypes.HANDLE(handles["job"].value),
                            1,
                        )
                    )
                except BaseException:
                    termination_succeeded = False
            if "process" in handles and handles["process"].open:
                try:
                    process_stopped = (
                        kernel32.WaitForSingleObject(
                            wintypes.HANDLE(handles["process"].value),
                            int(TERMINATION_GRACE_SECONDS * 1000),
                        )
                        == WAIT_OBJECT_0
                    )
                except BaseException:
                    process_stopped = False
    try:
        if created:
            if "completion_port" in handles and handles["completion_port"].open:
                try:
                    event_stream_exact = (
                        _drain_events(kernel32, handles["completion_port"], events)
                        and event_stream_exact
                    )
                except BaseException:
                    event_stream_exact = False
            else:
                event_stream_exact = False
            if "stdout_read" in handles and handles["stdout_read"].open:
                try:
                    out_eof, out_overflow, out_exact = _drain_pipe(
                        kernel32,
                        handles["stdout_read"],
                        stdout_buffer,
                        request.max_stdout_bytes,
                    )
                    stdout_eof = stdout_eof or out_eof
                    stdout_overflow = (
                        stdout_overflow or out_overflow or not out_exact
                    )
                except BaseException:
                    stdout_overflow = True
            if "stderr_read" in handles and handles["stderr_read"].open:
                try:
                    err_eof, err_overflow, err_exact = _drain_pipe(
                        kernel32,
                        handles["stderr_read"],
                        stderr_buffer,
                        request.max_stderr_bytes,
                    )
                    stderr_eof = stderr_eof or err_eof
                    stderr_overflow = (
                        stderr_overflow or err_overflow or not err_exact
                    )
                except BaseException:
                    stderr_overflow = True
            if "job" in handles and handles["job"].open:
                try:
                    total, active = _query_accounting(kernel32, handles["job"])
                except BaseException:
                    total, active = None, None
            if "process" in handles and handles["process"].open:
                try:
                    code = wintypes.DWORD(STILL_ACTIVE)
                    if kernel32.GetExitCodeProcess(
                        wintypes.HANDLE(handles["process"].value),
                        ctypes.byref(code),
                    ) and code.value != STILL_ACTIVE:
                        exit_code = int(code.value)
                except BaseException:
                    exit_code = None
                try:
                    process_stopped = (
                        kernel32.WaitForSingleObject(
                            wintypes.HANDLE(handles["process"].value),
                            0,
                        )
                        == WAIT_OBJECT_0
                    )
                except BaseException:
                    process_stopped = False
    except BaseException:
        event_stream_exact = False
        total, active = None, None
        process_stopped = False
        stdout_overflow = True
        stderr_overflow = True
    finally:
        closes = _close_all(handles, attributes)
    if not event_stream_exact:
        events.append(_JobEvent("unknown", None))
    return _LaunchEvidence(
        creation_attempt_count=creation_attempts,
        top_level_created=created,
        top_level_process_id=int(information.dwProcessId) if created else None,
        job_assigned_at_creation=True if created else None,
        job_handle_unique=True,
        events=tuple(events),
        cumulative_process_total=total,
        active_process_count=active,
        exit_code=exit_code,
        stdout=bytes(stdout_buffer),
        stderr=bytes(stderr_buffer),
        stdout_eof=stdout_eof,
        stderr_eof=stderr_eof,
        stdout_overflow=stdout_overflow,
        stderr_overflow=stderr_overflow,
        top_level_identity_exact=identity_exact,
        timed_out=timed_out,
        termination_requested=termination_requested,
        termination_succeeded=termination_succeeded,
        terminal_wait_succeeded=process_stopped and active == 0,
        close_observations=closes,
    )


class _WindowsTrustedLaunchAdapter:
    def __init__(self) -> None:
        self._audit: _AuditCounter | None = None
        self._launch_calls = 0

    def runtime_identity(self) -> tuple[str, str]:
        return os.name, sys.platform

    def install_audit(self, repository_root: Path) -> None:
        if self._audit is not None:
            raise _ObserverError("observation_binding_rejected")
        self._audit = _AuditCounter(repository_root)
        sys.addaudithook(self._audit)

    def bind_installed_root(self, installed_root: Path) -> None:
        if self._audit is None:
            raise _ObserverError("observation_binding_rejected")
        self._audit.bind_installed_root(installed_root)

    def resolve_launcher(self) -> _LauncherBinding:
        if os.name != "nt" or sys.platform != "win32":
            return _LauncherBinding(False, "", "", None)
        try:
            kernel32 = _kernel32()
            windows_directory = _windows_directory(kernel32)
            path = Path(windows_directory) / "py.exe"
            first = _stable_file_identity(path)
            second = _stable_file_identity(path)
            exact = first == second and path.name.lower() == "py.exe"
        except Exception:
            return _LauncherBinding(False, "", "", None)
        return _LauncherBinding(exact, os.fspath(path), windows_directory, first)

    def snapshot_effects(
        self,
        repository_root: Path,
        installed_root: Path,
        owner: ModuleType,
    ) -> _EffectSnapshot:
        try:
            return _owned_state_snapshot(owner, repository_root, installed_root)
        except _SafetyEffect:
            raise
        except Exception:
            return _EffectSnapshot(False, "", "", frozenset())

    def launch_once(self, request: _LaunchRequest) -> _LaunchEvidence:
        self._launch_calls += 1
        if self._launch_calls != 1:
            raise _SafetyEffect
        expected_environment = _fixed_environment(
            os.fspath(Path(request.application_path).parent)
        )
        if (
            request.tokens[:4]
            != (
                FIXED_LAUNCHER_TOKEN,
                FIXED_VERSION_TOKEN,
                FIXED_NO_BYTECODE_TOKEN,
                FIXED_CHILD_SCRIPT,
            )
            or len(request.tokens) != 5
            or request.timeout_seconds != TIMEOUT_SECONDS
            or request.environment != expected_environment
            or request.max_stdout_bytes <= 0
            or request.max_stderr_bytes <= 0
        ):
            raise _ObserverError("observation_binding_rejected")
        kernel32 = _kernel32()
        guard = _open_launcher_guard(kernel32, Path(request.application_path))
        try:
            if _stable_file_identity(Path(request.application_path)) != (
                request.launcher_identity
            ):
                raise _ObserverError("observation_binding_rejected")
        except Exception:
            if not guard.close():
                raise _ObserverError("observation_timeout_unknown") from None
            raise
        return _execute_windows_once(request, kernel32, guard)

    def audit_counts(self) -> _AuditCounts:
        if self._audit is None:
            raise _ObserverError("observation_timeout_unknown")
        return self._audit.snapshot()


def _write_exact(stream: object, payload: bytes) -> None:
    binary = getattr(stream, "buffer", None)
    if binary is None:
        stream.write(payload.decode("utf-8"))
    else:
        binary.write(payload)


def _emit_failure(status: str) -> None:
    if status not in _CLOSED_FAILURE_STATUSES:
        status = "observation_result_unknown"
    _write_exact(sys.stderr, status.encode("ascii") + b"\n")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        _emit_failure("observation_sequence_rejected")
        return 2
    try:
        result = _run_observation_1(_WindowsTrustedLaunchAdapter())
    except BaseException:
        result = "observation_result_unknown"
    if type(result) is bytes:
        _write_exact(sys.stdout, result)
        return 0
    status = result if type(result) is str else "observation_result_unknown"
    _emit_failure(status)
    return _STATUS_EXIT_CODES.get(status, 2)


if __name__ == "__main__":
    raise SystemExit(main())
