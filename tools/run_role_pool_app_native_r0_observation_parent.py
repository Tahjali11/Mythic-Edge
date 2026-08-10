"""Own one app-native R0 observation child boundary on Windows.

Importing this module is inert. The public entry point accepts only the closed
metadata or execution mode. Private executable custody and native process
evidence remain inside the Windows adapter; tests replace that adapter with fakes.
"""

from __future__ import annotations

import base64
import binascii
import ctypes
import hashlib
import json
import os
import re
import stat
import sys
import time
from collections.abc import Mapping, Sequence
from ctypes import wintypes
from dataclasses import dataclass, replace
from pathlib import Path, PureWindowsPath
from types import ModuleType
from typing import Protocol, cast

CONTROLLER_PATH = Path("tools/run_role_pool_app_native_r0_observation_parent.py")
OWNER_PATH = Path("tools/check_role_pool_r0_offline_observation.py")
OWNER_TEST_PATH = Path("tests/test_check_role_pool_r0_offline_observation.py")
BRIDGE_TEST_PATH = Path("tests/test_run_role_pool_r0_trusted_launch_observer.py")
PREDECESSOR_PATH = Path("tools/run_role_pool_r0_trusted_launch_observer.py")
LIFECYCLE_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_codex_app_native_r0_offline_observation_1_lifecycle.md"
)

FROZEN_BINDINGS = {
    LIFECYCLE_CONTRACT_PATH: "be7974ba998257981df5c876dfa441b03326ae776405bd269d1470957a785cde",
    OWNER_PATH: "cfd3a0baaff6c4bbc5144403fd72f404722b8b96e8eca30fbf588f3180ec0b42",
    OWNER_TEST_PATH: "3fc6c35eada99f3a319e1ebe94bd5f33494821301cfdf1ec67f5f35bfc97dc4c",
    BRIDGE_TEST_PATH: "53738a8d2108edaf13cd138cad7d3c771cdaff58c32c13cd464fec758a8bc9a7",
    PREDECESSOR_PATH: "ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a",
}
STATE_BINDINGS = {
    **FROZEN_BINDINGS,
    Path("docs/contracts/trusted_owner_native_role_pool_profile.md"): (
        "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
    ),
    Path("tools/check_role_pool_r0_bootstrap.py"): (
        "897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a"
    ),
    Path("tests/test_check_role_pool_r0_bootstrap.py"): (
        "55a40f12d7d161eb40fca2905f442b3b6ecd1fc029e3313c81566db89dd6ae3f"
    ),
    Path("docs/role_pool/trusted_owner_repository_registry.v1.json"): (
        "4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb"
    ),
    Path("docs/role_pool/trusted_owner_native_release_state.v1.jsonl"): (
        "fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2"
    ),
    Path("docs/role_pool_current_authority_index.md"): (
        "a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9"
    ),
}

OBSERVATION_PATTERN = re.compile(r"r0\.app_native\.offline\.observation\.1\.([0-9a-f]{32})\Z")
VERSION_PATTERN = re.compile(r"3\.13\.(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))?\Z")
DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
TRANSPORT_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,2048}\Z")
TARGET_BINDING_SCHEMA = "trusted_owner_app_native_r0_successor_target_binding.v1"
STABLE_IDENTITY_SCHEMA = "trusted_owner_app_native_r0_successor_file_identity.v1"
TARGET_BINDING_FIELDS = (
    "schema_version",
    "repository_id",
    "issue_number",
    "host_os_name",
    "host_sys_platform",
    "runtime_implementation",
    "executable_basename",
    "file_version",
    "product_version",
    "byte_length",
    "file_sha256",
    "stable_identity_schema",
    "stable_identity_sha256",
    "ordinary_file",
    "reparse_point",
    "private_path_source",
    "private_path_publication_authorized",
    "binding_sha256",
)
MAX_BINDING_BYTES = 1536
FIXED_CHILD_SCRIPT = "tools/check_role_pool_r0_offline_observation.py"
TIMEOUT_SECONDS = 120.0
TERMINATION_GRACE_SECONDS = 5.0
MAX_PRIVATE_PATH_UNITS = 32767
MAX_QUEUE_EVENTS = 4096
MAX_STDOUT_BYTES = 4096
MAX_STDERR_BYTES = 128
MAX_COMPLETION_EVENTS_PER_CYCLE = 32
_AUDIT_REGISTRATION_EVENT = "mythic_edge.r0_parent.audit_registration"
_REPOSITORY_METADATA_NAMES = frozenset({".git"})

ENABLE_LINE_INPUT = 0x0002
ENABLE_ECHO_INPUT = 0x0004
STD_INPUT_HANDLE = -10
KEY_EVENT = 0x0001
GENERIC_READ = 0x80000000
FILE_READ_ATTRIBUTES = 0x00000080
FILE_EXECUTE = 0x00000020
FILE_SHARE_READ = 0x00000001
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
HANDLE_FLAG_INHERIT = 0x00000001
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

_REPARSE_MARKER = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_CLOSED_FAILURE_STATUSES = frozenset(
    {
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
)
_STATUS_EXIT_CODES = {
    "observation_safety_boundary_failed": 4,
    "observation_launch_unknown": 3,
    "observation_timeout_unknown": 3,
    "observation_result_unknown": 3,
}
_REQUIRED_CLOSE_RESOURCES = frozenset(
    {
        "controller_image_guard",
        "target_guard",
        "stdin_read",
        "stdin_write",
        "stdout_read",
        "stdout_write",
        "stderr_read",
        "stderr_write",
        "job",
        "completion_port",
        "checker_guard",
        "process",
        "thread",
        "attribute_list",
    }
)


class _ControllerError(RuntimeError):
    def __init__(self, status: str) -> None:
        super().__init__(status)
        self.status = status


class _SafetyEffect(_ControllerError):
    def __init__(self) -> None:
        super().__init__("observation_safety_boundary_failed")


@dataclass(frozen=True)
class _FileIdentity:
    device: int
    inode: int
    size: int
    modified_ns: int
    sha256: str
    file_version: str
    product_version: str
    stable_identity_sha256: str = "0" * 64


@dataclass(frozen=True)
class _TargetBinding:
    opaque_path: object
    identity: _FileIdentity


@dataclass(frozen=True)
class _CanonicalTargetBinding:
    fields: tuple[tuple[str, object], ...]
    canonical_bytes: bytes

    @property
    def binding_sha256(self) -> str:
        return cast(str, self.fields[-1][1])

    @property
    def artifact_sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes).hexdigest()

    @property
    def transport(self) -> str:
        return base64.urlsafe_b64encode(self.canonical_bytes).rstrip(b"=").decode("ascii")


@dataclass(frozen=True)
class _QueueRecord:
    event_type: int
    key_down: bool
    unicode_character: str


@dataclass(frozen=True)
class _QueueAudit:
    first_count: int | None
    records: tuple[_QueueRecord, ...]
    returned_count: int | None
    second_count: int | None
    api_exact: bool = True


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
    target_identity_exact: bool | None
    timed_out: bool
    termination_requested: bool
    termination_succeeded: bool | None
    terminal_wait_succeeded: bool | None
    close_observations: tuple[_CloseObservation, ...]


@dataclass(frozen=True)
class _LaunchRequest:
    target: _TargetBinding
    tokens: tuple[str, ...]
    repository_root: Path
    environment: tuple[tuple[str, str], ...]
    timeout_seconds: float
    max_stdout_bytes: int
    max_stderr_bytes: int


class ParentAdapter(Protocol):
    """Closed native seam. Production owns it; tests provide inert fakes."""

    def runtime_identity(self) -> tuple[str, str]: ...

    def install_audit(self, repository_root: Path) -> None: ...

    def snapshot_effects(self, repository_root: Path) -> _EffectSnapshot: ...

    def windows_directory(self) -> str: ...

    def open_console(self) -> tuple[object, int]: ...

    def set_console_mode(self, console: object, mode: int) -> bool: ...

    def audit_console_queue(self, console: object) -> _QueueAudit: ...

    def read_console_line(self, console: object, capacity: int) -> object: ...

    def validate_controller_image(self) -> _TargetBinding: ...

    def validate_target(self, private_line: object) -> _TargetBinding: ...

    def image_bindings_exact(
        self,
        controller: _TargetBinding,
        target: _TargetBinding,
    ) -> bool | None: ...

    def clear_private(self, *values: object) -> bool: ...

    def launch_once(self, request: _LaunchRequest) -> _LaunchEvidence: ...

    def finish_image_guards(self) -> tuple[_CloseObservation, ...]: ...

    def finish_checker_guard(self) -> tuple[bool | None, _CloseObservation | None]: ...

    def target_identity_exact(self, target: _TargetBinding) -> bool | None: ...

    def audit_counts(self) -> _AuditCounts: ...


def _ordinary_nonreparse(info: os.stat_result, *, directory: bool = False) -> bool:
    expected = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    return expected and not stat.S_ISLNK(info.st_mode) and not bool(
        getattr(info, "st_file_attributes", 0) & _REPARSE_MARKER
    )


def _identity_tuple(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        int(info.st_dev),
        int(info.st_ino),
        int(info.st_mode),
        int(info.st_size),
        int(info.st_mtime_ns),
    )


def _stable_file_bytes(path: Path) -> bytes:
    try:
        before = path.lstat()
        if not _ordinary_nonreparse(before):
            raise _ControllerError("observation_binding_rejected")
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            payload = stream.read()
            after_read = os.fstat(stream.fileno())
        after = path.lstat()
    except _ControllerError:
        raise
    except OSError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    expected = _identity_tuple(before)
    if any(_identity_tuple(value) != expected for value in (opened, after_read, after)):
        raise _ControllerError("observation_binding_rejected")
    return payload


def _repository_root() -> Path:
    module_path = Path(__file__).absolute()
    root = module_path.parent.parent
    if module_path != root / CONTROLLER_PATH:
        raise _ControllerError("observation_binding_rejected")
    try:
        info = root.lstat()
    except OSError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    if not _ordinary_nonreparse(info, directory=True):
        raise _ControllerError("observation_binding_rejected")
    return root


def _load_owner(repository_root: Path) -> ModuleType:
    verified: dict[Path, bytes] = {}
    for relative, digest in FROZEN_BINDINGS.items():
        payload = _stable_file_bytes(repository_root / relative)
        if hashlib.sha256(payload).hexdigest() != digest:
            raise _ControllerError("observation_binding_rejected")
        verified[relative] = payload
    name = "_r0_app_native_observation_owner"
    module = ModuleType(name)
    path = repository_root / OWNER_PATH
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__spec__ = None
    sys.modules[name] = module
    try:
        code = compile(verified[OWNER_PATH], os.fspath(path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
    except Exception as exc:
        sys.modules.pop(name, None)
        raise _ControllerError("observation_binding_rejected") from exc
    required = (
        "PostExitFacts",
        "observation_identity_pair",
        "parse_validation_payload",
        "seal_proportionate_observation_receipt",
    )
    if any(not hasattr(module, item) for item in required):
        raise _ControllerError("observation_binding_rejected")
    return module


def _validate_observation_id(value: object) -> str:
    if type(value) is not str or not value.isascii():
        raise _ControllerError("observation_sequence_rejected")
    match = OBSERVATION_PATTERN.fullmatch(value)
    if match is None or match.group(1) == "0" * 32:
        raise _ControllerError("observation_sequence_rejected")
    return value


def _stable_identity_preimage(volume_serial_number: int, file_index: int) -> bytes:
    if not 0 <= volume_serial_number <= 0xFFFFFFFF or not 0 <= file_index <= 0xFFFFFFFFFFFFFFFF:
        raise _ControllerError("observation_binding_rejected")
    return (
        f"{STABLE_IDENTITY_SCHEMA}|volume_serial_number={volume_serial_number:08x}"
        f"|file_index={file_index:016x}"
    ).encode("ascii")


def _stable_identity_digest(volume_serial_number: int, file_index: int) -> str:
    return hashlib.sha256(_stable_identity_preimage(volume_serial_number, file_index)).hexdigest()


def _binding_without_digest(identity: _FileIdentity) -> tuple[tuple[str, object], ...]:
    return (
        ("schema_version", TARGET_BINDING_SCHEMA),
        ("repository_id", 1235264383),
        ("issue_number", 826),
        ("host_os_name", "nt"),
        ("host_sys_platform", "win32"),
        ("runtime_implementation", "CPython"),
        ("executable_basename", "python.exe"),
        ("file_version", identity.file_version),
        ("product_version", identity.product_version),
        ("byte_length", identity.size),
        ("file_sha256", identity.sha256),
        ("stable_identity_schema", STABLE_IDENTITY_SCHEMA),
        ("stable_identity_sha256", identity.stable_identity_sha256),
        ("ordinary_file", True),
        ("reparse_point", False),
        ("private_path_source", "owner_supplied_local_absolute_path"),
        ("private_path_publication_authorized", False),
    )


def _compact_object(fields: Sequence[tuple[str, object]]) -> bytes:
    return json.dumps(dict(fields), ensure_ascii=True, separators=(",", ":")).encode("ascii")


def _canonical_target_binding(identity: _FileIdentity) -> _CanonicalTargetBinding:
    fields = _binding_without_digest(identity)
    digest = hashlib.sha256(_compact_object(fields)).hexdigest()
    complete = fields + (("binding_sha256", digest),)
    canonical = _compact_object(complete) + b"\n"
    parsed = _validate_canonical_binding_bytes(canonical)
    if parsed.fields != complete:
        raise _ControllerError("observation_binding_rejected")
    return parsed


def _validate_binding_values(fields: tuple[tuple[str, object], ...]) -> None:
    values = dict(fields)
    exact = {
        "schema_version": TARGET_BINDING_SCHEMA,
        "repository_id": 1235264383,
        "issue_number": 826,
        "host_os_name": "nt",
        "host_sys_platform": "win32",
        "runtime_implementation": "CPython",
        "executable_basename": "python.exe",
        "stable_identity_schema": STABLE_IDENTITY_SCHEMA,
        "ordinary_file": True,
        "reparse_point": False,
        "private_path_source": "owner_supplied_local_absolute_path",
        "private_path_publication_authorized": False,
    }
    if any(type(values[name]) is not type(expected) or values[name] != expected for name, expected in exact.items()):
        raise _ControllerError("observation_sequence_rejected")
    if any(
        type(values[name]) is not str
        or VERSION_PATTERN.fullmatch(cast(str, values[name])) is None
        for name in ("file_version", "product_version")
    ):
        raise _ControllerError("observation_sequence_rejected")
    byte_length = values["byte_length"]
    if type(byte_length) is not int or not 1 <= cast(int, byte_length) <= 0x7FFFFFFFFFFFFFFF:
        raise _ControllerError("observation_sequence_rejected")
    for name in ("file_sha256", "stable_identity_sha256", "binding_sha256"):
        value = values[name]
        if type(value) is not str or DIGEST_PATTERN.fullmatch(cast(str, value)) is None:
            raise _ControllerError("observation_sequence_rejected")


def _validate_canonical_binding_bytes(payload: bytes) -> _CanonicalTargetBinding:
    if type(payload) is not bytes or not 1 <= len(payload) <= MAX_BINDING_BYTES or not payload.endswith(b"\n"):
        raise _ControllerError("observation_sequence_rejected")
    if payload.endswith(b"\n\n") or b"\r" in payload or payload.startswith(b"\xef\xbb\xbf"):
        raise _ControllerError("observation_sequence_rejected")
    try:
        text = payload[:-1].decode("ascii")
        pairs = json.loads(text, object_pairs_hook=lambda items: tuple(items))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _ControllerError("observation_sequence_rejected") from exc
    if type(pairs) is not tuple or tuple(name for name, _value in pairs) != TARGET_BINDING_FIELDS:
        raise _ControllerError("observation_sequence_rejected")
    fields = cast(tuple[tuple[str, object], ...], pairs)
    _validate_binding_values(fields)
    if _compact_object(fields) + b"\n" != payload:
        raise _ControllerError("observation_sequence_rejected")
    expected_digest = hashlib.sha256(_compact_object(fields[:-1])).hexdigest()
    if fields[-1] != ("binding_sha256", expected_digest):
        raise _ControllerError("observation_sequence_rejected")
    return _CanonicalTargetBinding(fields, payload)


def _decode_target_binding_transport(value: object) -> _CanonicalTargetBinding:
    if (
        type(value) is not str
        or not cast(str, value).isascii()
        or TRANSPORT_PATTERN.fullmatch(cast(str, value)) is None
    ):
        raise _ControllerError("observation_sequence_rejected")
    encoded = cast(str, value).encode("ascii")
    try:
        payload = base64.b64decode(encoded + b"=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise _ControllerError("observation_sequence_rejected") from exc
    if len(payload) > MAX_BINDING_BYTES or base64.urlsafe_b64encode(payload).rstrip(b"=") != encoded:
        raise _ControllerError("observation_sequence_rejected")
    return _validate_canonical_binding_bytes(payload)


def _binding_matches(target: _TargetBinding, expected: _CanonicalTargetBinding) -> bool:
    try:
        return _canonical_target_binding(target.identity).canonical_bytes == expected.canonical_bytes
    except _ControllerError:
        return False


def _queue_is_empty(audit: _QueueAudit) -> bool:
    count = audit.first_count
    if (
        not audit.api_exact
        or type(count) is not int
        or count < 0
        or count > MAX_QUEUE_EVENTS
        or type(audit.second_count) is not int
        or audit.second_count != count
    ):
        return False
    if count == 0:
        return audit.returned_count in (None, 0) and not audit.records
    if audit.returned_count != count or len(audit.records) != count:
        return False
    for record in audit.records:
        if (
            type(record.event_type) is not int
            or type(record.key_down) is not bool
            or type(record.unicode_character) is not str
            or len(record.unicode_character) > 1
        ):
            return False
        if record.event_type == KEY_EVENT and record.key_down and record.unicode_character != "\0":
            return False
    return True


def _private_line_text(value: object) -> str:
    if type(value) is not str or not value or "\0" in value:
        raise _ControllerError("observation_binding_rejected")
    if len(value) > MAX_PRIVATE_PATH_UNITS + 2:
        raise _ControllerError("observation_binding_rejected")
    if value.endswith("\r\n"):
        body = value[:-2]
    elif value.endswith("\r"):
        body = value[:-1]
    else:
        raise _ControllerError("observation_binding_rejected")
    if not body or "\r" in body or "\n" in body:
        raise _ControllerError("observation_binding_rejected")
    try:
        body.encode("utf-16-le", "strict")
    except UnicodeEncodeError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    if len(body) > MAX_PRIVATE_PATH_UNITS:
        raise _ControllerError("observation_binding_rejected")
    return body


def _acquire_target(adapter: ParentAdapter) -> _TargetBinding:
    console: object | None = None
    private_line: object | None = None
    normalized: object | None = None
    original_mode: int | None = None
    mode_changed = False
    restored = False
    restore_attempted = False
    clear_exact = True
    try:
        console, original_mode = adapter.open_console()
        if type(original_mode) is not int or not (original_mode & ENABLE_LINE_INPUT):
            raise _ControllerError("observation_binding_rejected")
        if not adapter.set_console_mode(console, original_mode & ~ENABLE_ECHO_INPUT):
            raise _ControllerError("observation_binding_rejected")
        mode_changed = True
        if not _queue_is_empty(adapter.audit_console_queue(console)):
            raise _ControllerError("observation_binding_rejected")
        private_line = adapter.read_console_line(console, MAX_PRIVATE_PATH_UNITS + 2)
        normalized = _private_line_text(private_line)
        if not _queue_is_empty(adapter.audit_console_queue(console)):
            raise _ControllerError("observation_binding_rejected")
        restore_attempted = True
        if not adapter.set_console_mode(console, original_mode):
            raise _ControllerError("observation_timeout_unknown")
        restored = True
        if not _queue_is_empty(adapter.audit_console_queue(console)):
            raise _ControllerError("observation_binding_rejected")
        return adapter.validate_target(normalized)
    finally:
        if (
            mode_changed
            and not restore_attempted
            and console is not None
            and original_mode is not None
        ):
            restore_attempted = True
            try:
                restored = adapter.set_console_mode(console, original_mode)
            except BaseException:
                restored = False
        try:
            clear_exact = adapter.clear_private(private_line, normalized)
        except BaseException:
            clear_exact = False
        if mode_changed and not restored:
            raise _ControllerError("observation_timeout_unknown")
        if not clear_exact:
            raise _ControllerError("observation_timeout_unknown")


def _fixed_environment(windows_directory: str) -> tuple[tuple[str, str], ...]:
    if not windows_directory or "\0" in windows_directory:
        raise _ControllerError("observation_binding_rejected")
    return (("PYTHONDONTWRITEBYTECODE", "1"), ("SYSTEMROOT", windows_directory))


def _valid_private_target_text(value: object) -> bool:
    if type(value) is not str:
        return False
    pure = PureWindowsPath(value)
    parts = pure.parts
    return (
        pure.is_absolute()
        and bool(pure.drive)
        and not pure.drive.startswith("\\")
        and len(parts) >= 2
        and pure.name.lower() == "python.exe"
        and ":" not in "".join(parts[1:])
        and all(
            part not in {".", ".."}
            and not part.endswith((".", " "))
            and not any(marker in part for marker in "*?")
            for part in parts[1:]
        )
    )


def _relationships_known(evidence: _LaunchEvidence) -> tuple[bool, int]:
    if (
        evidence.creation_attempt_count != 1
        or evidence.top_level_created is not True
        or type(evidence.top_level_process_id) is not int
        or evidence.top_level_process_id <= 0
        or evidence.job_assigned_at_creation is not True
        or evidence.job_handle_unique is not True
        or type(evidence.cumulative_process_total) is not int
        or evidence.cumulative_process_total < 1
        or evidence.active_process_count != 0
        or any(event.kind == "unknown" for event in evidence.events)
    ):
        return False, 0
    new_ids = [event.process_id for event in evidence.events if event.kind == "new"]
    exit_ids = [event.process_id for event in evidence.events if event.kind == "exit"]
    if (
        len(new_ids) != len(set(new_ids))
        or set(exit_ids) != set(new_ids)
        or len(exit_ids) != len(new_ids)
        or new_ids.count(evidence.top_level_process_id) != 1
        or evidence.cumulative_process_total != len(new_ids)
    ):
        return False, max(0, len(set(new_ids)) - 1)
    if sum(event.kind == "active_zero" for event in evidence.events) != 1:
        return False, 0
    descendants = len(set(new_ids) - {evidence.top_level_process_id})
    if any(event.kind == "active_limit" for event in evidence.events):
        descendants = max(1, descendants)
    return True, descendants


def _closes_exact(evidence: _LaunchEvidence) -> bool:
    names = [item.resource for item in evidence.close_observations]
    return (
        len(names) == len(_REQUIRED_CLOSE_RESOURCES)
        and set(names) == _REQUIRED_CLOSE_RESOURCES
        and all(item.attempt_count == 1 and item.succeeded for item in evidence.close_observations)
    )


def _finish_image_state(
    adapter: ParentAdapter,
    controller: _TargetBinding | None,
    target: _TargetBinding | None,
) -> bool:
    if controller is None:
        return target is None
    try:
        closes = adapter.finish_image_guards()
    except BaseException:
        closes = ()
    expected = (
        ("target_guard", "controller_image_guard")
        if target is not None
        else ("controller_image_guard",)
    )
    try:
        cleared = adapter.clear_private(
            controller.opaque_path,
            target.opaque_path if target is not None else None,
        )
    except BaseException:
        cleared = False
    return (
        tuple(item.resource for item in closes) == expected
        and all(item.attempt_count == 1 and item.succeeded for item in closes)
        and cleared
    )


def _run_metadata(
    adapter: ParentAdapter,
    *,
    repository_root: Path,
) -> bytes | str:
    runtime_os, runtime_platform = adapter.runtime_identity()
    if runtime_os != "nt" or runtime_platform != "win32":
        return "observation_host_rejected"
    controller: _TargetBinding | None = None
    target: _TargetBinding | None = None
    status: str | None = None
    binding: _CanonicalTargetBinding | None = None
    try:
        controller = adapter.validate_controller_image()
        adapter.install_audit(repository_root)
        before = adapter.snapshot_effects(repository_root)
        if not before.exact:
            raise _ControllerError("observation_binding_rejected")
        target = _acquire_target(adapter)
        if (
            controller.identity != target.identity
            or adapter.image_bindings_exact(controller, target) is not True
        ):
            raise _ControllerError("observation_binding_rejected")
        binding = _canonical_target_binding(target.identity)
    except _SafetyEffect:
        status = "observation_safety_boundary_failed"
    except _ControllerError as exc:
        status = exc.status
    except BaseException:
        status = "observation_result_unknown"
    finally:
        if not _finish_image_state(adapter, controller, target):
            status = "observation_timeout_unknown"
    if status is not None:
        return status
    if binding is None:
        return "observation_result_unknown"
    try:
        after = adapter.snapshot_effects(repository_root)
        counts = adapter.audit_counts()
    except BaseException:
        return "observation_result_unknown"
    snapshots_exact = before.exact and after.exact
    if (
        not snapshots_exact
        or before.repository_digest != after.repository_digest
        or before.installed_digest != after.installed_digest
        or after.generated_residue != before.generated_residue
        or counts != _AuditCounts(0, 0, 0, 0)
    ):
        return "observation_safety_boundary_failed"
    return binding.canonical_bytes


def _run_controller(
    observation_id: str,
    expected_binding: _CanonicalTargetBinding,
    adapter: ParentAdapter,
    *,
    repository_root: Path,
    owner: ModuleType,
) -> bytes | str:
    runtime_os, runtime_platform = adapter.runtime_identity()
    if runtime_os != "nt" or runtime_platform != "win32":
        return "observation_host_rejected"
    controller: _TargetBinding | None = None
    target: _TargetBinding | None = None
    evidence: _LaunchEvidence | None = None
    image_cleanup_complete = False
    try:
        observation_id = _validate_observation_id(observation_id)
        owner.observation_identity_pair(observation_id)
        adapter.install_audit(repository_root)
        before = adapter.snapshot_effects(repository_root)
        if not before.exact:
            return "observation_binding_rejected"
        controller = adapter.validate_controller_image()
        if not _binding_matches(controller, expected_binding):
            raise _ControllerError("observation_binding_rejected")
        target = _acquire_target(adapter)
        if (
            not _binding_matches(target, expected_binding)
            or controller.identity != target.identity
            or adapter.image_bindings_exact(controller, target) is not True
        ):
            raise _ControllerError("observation_binding_rejected")
        checker_exact: bool | None = None
        checker_close: _CloseObservation | None = None
        try:
            request = _LaunchRequest(
                target=target,
                tokens=("python.exe", "-B", FIXED_CHILD_SCRIPT, observation_id),
                repository_root=repository_root,
                environment=_fixed_environment(adapter.windows_directory()),
                timeout_seconds=TIMEOUT_SECONDS,
                max_stdout_bytes=MAX_STDOUT_BYTES,
                max_stderr_bytes=MAX_STDERR_BYTES,
            )
            evidence = adapter.launch_once(request)
            target_exact = adapter.target_identity_exact(target)
            after = adapter.snapshot_effects(repository_root)
            counts = adapter.audit_counts()
        finally:
            try:
                checker_exact, checker_close = adapter.finish_checker_guard()
            except BaseException:
                checker_exact = None
                checker_close = None
            image_cleanup_complete = _finish_image_state(adapter, controller, target)
            if not image_cleanup_complete:
                raise _ControllerError("observation_timeout_unknown")
            if checker_close is not None and (
                checker_close.attempt_count != 1 or checker_close.succeeded is not True
            ):
                raise _ControllerError("observation_timeout_unknown")
        if checker_close is None:
            raise _ControllerError("observation_timeout_unknown")
        if evidence is None:
            raise _ControllerError("observation_launch_unknown")
        evidence = replace(
            evidence,
            close_observations=evidence.close_observations + (checker_close,),
        )
        if checker_exact is not True:
            raise _ControllerError("observation_launch_unknown")
    except _SafetyEffect:
        status = "observation_safety_boundary_failed"
    except _ControllerError as exc:
        status = exc.status
    except BaseException:
        status = "observation_result_unknown"
    else:
        status = None

    if status is not None:
        if not image_cleanup_complete and not _finish_image_state(adapter, controller, target):
            return "observation_timeout_unknown"
        return status

    if target_exact is not True:
        return "observation_launch_unknown"
    relationships_known, descendant_count = _relationships_known(evidence)
    close_exact = _closes_exact(evidence)
    snapshots_exact = before.exact and after.exact
    repository_writes = counts.repository_writes + int(
        snapshots_exact and before.repository_digest != after.repository_digest
    )
    installed_writes = counts.installed_writes + int(
        snapshots_exact and before.installed_digest != after.installed_digest
    )
    residue_count = len(after.generated_residue - before.generated_residue) if snapshots_exact else 1
    cleanup_confirmed = (
        evidence.terminal_wait_succeeded is True
        and evidence.stdout_eof
        and evidence.stderr_eof
        and close_exact
        and snapshots_exact
        and target_exact is True
    )
    facts = owner.PostExitFacts(
        top_level_process_count=1 if evidence.top_level_created is True else 0,
        descendant_process_count=descendant_count,
        process_relationships_known=relationships_known,
        process_terminal_states_known=(
            evidence.exit_code is not None
            and evidence.active_process_count == 0
            and evidence.terminal_wait_succeeded is True
        ),
        surviving_process_count=max(0, evidence.active_process_count or 0),
        top_level_identity_exact=evidence.top_level_identity_exact,
        timed_out=evidence.timed_out,
        termination_uncertain=(
            (evidence.termination_requested and evidence.termination_succeeded is not True)
            or evidence.terminal_wait_succeeded is not True
        ),
        cleanup_confirmed=cleanup_confirmed,
        output_complete=(
            evidence.stdout_eof
            and evidence.stderr_eof
            and not evidence.stdout_overflow
            and not evidence.stderr_overflow
        ),
        executor_network_operation_count=counts.network_operations,
        repository_write_count=repository_writes,
        installed_write_count=installed_writes,
        external_effect_count=counts.external_effects,
        generated_residue_count=residue_count,
    )
    if not relationships_known:
        return "observation_launch_unknown"
    if (
        facts.timed_out
        or facts.termination_uncertain
        or not facts.process_terminal_states_known
        or not facts.cleanup_confirmed
    ):
        return "observation_timeout_unknown"
    if (
        facts.descendant_process_count
        or facts.surviving_process_count
        or facts.executor_network_operation_count
        or facts.repository_write_count
        or facts.installed_write_count
        or facts.external_effect_count
        or facts.generated_residue_count
    ):
        return "observation_safety_boundary_failed"
    if not facts.output_complete:
        return "observation_result_unknown"
    if (
        evidence.exit_code != 0
        or evidence.stderr
        or len(evidence.stdout) > MAX_STDOUT_BYTES
        or len(evidence.stderr) > MAX_STDERR_BYTES
    ):
        return "observation_validation_failed"
    try:
        owner.parse_validation_payload(evidence.stdout)
    except BaseException:
        return "observation_validation_failed"
    try:
        result = owner.seal_proportionate_observation_receipt(evidence.stdout, facts, observation_id)
    except BaseException:
        return "observation_result_unknown"
    if type(result) is bytes:
        return result
    return result if result in _CLOSED_FAILURE_STATUSES else "observation_result_unknown"


class _KeyEventRecord(ctypes.Structure):
    _fields_ = (
        ("bKeyDown", wintypes.BOOL),
        ("wRepeatCount", wintypes.WORD),
        ("wVirtualKeyCode", wintypes.WORD),
        ("wVirtualScanCode", wintypes.WORD),
        ("UnicodeChar", wintypes.WCHAR),
        ("dwControlKeyState", wintypes.DWORD),
    )


class _InputEventUnion(ctypes.Union):
    _fields_ = (("KeyEvent", _KeyEventRecord), ("padding", ctypes.c_byte * 16))


class _InputRecord(ctypes.Structure):
    _fields_ = (("EventType", wintypes.WORD), ("Event", _InputEventUnion))


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
    _fields_ = (("CompletionKey", wintypes.LPVOID), ("CompletionPort", wintypes.HANDLE))


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


class _VsFixedFileInfo(ctypes.Structure):
    _fields_ = tuple((name, wintypes.DWORD) for name in (
        "dwSignature",
        "dwStrucVersion",
        "dwFileVersionMS",
        "dwFileVersionLS",
        "dwProductVersionMS",
        "dwProductVersionLS",
        "dwFileFlagsMask",
        "dwFileFlags",
        "dwFileOS",
        "dwFileType",
        "dwFileSubtype",
        "dwFileDateMS",
        "dwFileDateLS",
    ))


class _ByHandleFileInformation(ctypes.Structure):
    _fields_ = (
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", wintypes.FILETIME),
        ("ftLastAccessTime", wintypes.FILETIME),
        ("ftLastWriteTime", wintypes.FILETIME),
        ("dwVolumeSerialNumber", wintypes.DWORD),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("nNumberOfLinks", wintypes.DWORD),
        ("nFileIndexHigh", wintypes.DWORD),
        ("nFileIndexLow", wintypes.DWORD),
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
        try:
            self.succeeded = not self.value or bool(self.kernel32.CloseHandle(wintypes.HANDLE(self.value)))
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
        self.kernel32.InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(size))
        if not size.value:
            raise _ControllerError("observation_launch_unknown")
        buffer = ctypes.create_string_buffer(size.value)
        pointer = ctypes.cast(buffer, wintypes.LPVOID)
        if not self.kernel32.InitializeProcThreadAttributeList(pointer, 2, 0, ctypes.byref(size)):
            raise _ControllerError("observation_launch_unknown")
        self.buffer = buffer
        self.pointer = pointer
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
        return _CloseObservation("attribute_list", self.attempt_count, self.succeeded)


def _handle_stable_identity(kernel32: object, guard: _OwnedHandle) -> str:
    if not guard.open:
        raise _ControllerError("observation_binding_rejected")
    information = _ByHandleFileInformation()
    if not kernel32.GetFileInformationByHandle(
        wintypes.HANDLE(guard.value),
        ctypes.byref(information),
    ):
        raise _ControllerError("observation_binding_rejected")
    file_index = (int(information.nFileIndexHigh) << 32) | int(information.nFileIndexLow)
    return _stable_identity_digest(int(information.dwVolumeSerialNumber), file_index)


def _checker_file_identity(path: Path) -> tuple[int, int, int, int, str]:
    payload = _stable_file_bytes(path)
    info = path.lstat()
    digest = hashlib.sha256(payload).hexdigest()
    if len(payload) != int(info.st_size):
        raise _ControllerError("observation_binding_rejected")
    return (
        int(info.st_dev),
        int(info.st_ino),
        int(info.st_size),
        int(info.st_mtime_ns),
        digest,
    )


def _open_checker_guard(
    repository_root: Path,
    kernel32: object,
) -> _OwnedHandle:
    checker = repository_root / OWNER_PATH
    current = repository_root
    try:
        for index, part in enumerate(OWNER_PATH.parts):
            current /= part
            info = current.lstat()
            if index == len(OWNER_PATH.parts) - 1:
                if not _ordinary_nonreparse(info):
                    raise _ControllerError("observation_binding_rejected")
            elif not _ordinary_nonreparse(info, directory=True):
                raise _ControllerError("observation_binding_rejected")
    except _ControllerError:
        raise
    except OSError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    guard = _OwnedHandle(
        kernel32,
        "checker_guard",
        cast(
            int,
            kernel32.CreateFileW(
                os.fspath(checker),
                GENERIC_READ | FILE_READ_ATTRIBUTES,
                FILE_SHARE_READ,
                None,
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            ),
        ),
    )
    if not guard.open:
        raise _ControllerError("observation_binding_rejected")
    return guard


def _checker_identity_exact(
    repository_root: Path,
    expected: tuple[int, int, int, int, str],
) -> bool | None:
    try:
        return _checker_file_identity(repository_root / OWNER_PATH) == expected
    except BaseException:
        return None


def _kernel32() -> object:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetStdHandle.argtypes = (wintypes.DWORD,)
    kernel32.GetStdHandle.restype = wintypes.HANDLE
    kernel32.GetConsoleMode.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetConsoleMode.restype = wintypes.BOOL
    kernel32.SetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.SetConsoleMode.restype = wintypes.BOOL
    kernel32.GetNumberOfConsoleInputEvents.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetNumberOfConsoleInputEvents.restype = wintypes.BOOL
    kernel32.PeekConsoleInputW.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(_InputRecord),
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.PeekConsoleInputW.restype = wintypes.BOOL
    kernel32.ReadConsoleW.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    kernel32.ReadConsoleW.restype = wintypes.BOOL
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
    kernel32.GetCurrentProcess.argtypes = ()
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(_ByHandleFileInformation),
    )
    kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.CreatePipe.argtypes = (
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(_SecurityAttributes),
        wintypes.DWORD,
    )
    kernel32.CreatePipe.restype = wintypes.BOOL
    kernel32.SetHandleInformation.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD)
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


def _file_versions(path: str) -> tuple[str, str]:
    version = ctypes.WinDLL("version", use_last_error=True)
    version.GetFileVersionInfoSizeW.argtypes = (
        wintypes.LPCWSTR,
        ctypes.POINTER(wintypes.DWORD),
    )
    version.GetFileVersionInfoSizeW.restype = wintypes.DWORD
    version.GetFileVersionInfoW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
    )
    version.GetFileVersionInfoW.restype = wintypes.BOOL
    version.VerQueryValueW.argtypes = (
        wintypes.LPCVOID,
        wintypes.LPCWSTR,
        ctypes.POINTER(wintypes.LPVOID),
        ctypes.POINTER(wintypes.UINT),
    )
    version.VerQueryValueW.restype = wintypes.BOOL
    ignored = wintypes.DWORD()
    size = int(version.GetFileVersionInfoSizeW(path, ctypes.byref(ignored)))
    if size <= 0:
        raise _ControllerError("observation_binding_rejected")
    payload = ctypes.create_string_buffer(size)
    if not version.GetFileVersionInfoW(path, 0, size, payload):
        raise _ControllerError("observation_binding_rejected")
    pointer = wintypes.LPVOID()
    length = wintypes.UINT()
    if not version.VerQueryValueW(payload, "\\", ctypes.byref(pointer), ctypes.byref(length)):
        raise _ControllerError("observation_binding_rejected")
    if length.value < ctypes.sizeof(_VsFixedFileInfo):
        raise _ControllerError("observation_binding_rejected")
    fixed = ctypes.cast(pointer, ctypes.POINTER(_VsFixedFileInfo)).contents

    def dotted(ms: int, ls: int) -> str:
        return f"{ms >> 16}.{ms & 0xffff}.{ls >> 16}.{ls & 0xffff}"

    return (
        dotted(int(fixed.dwFileVersionMS), int(fixed.dwFileVersionLS)),
        dotted(int(fixed.dwProductVersionMS), int(fixed.dwProductVersionLS)),
    )


def _quote_windows_argument(value: str) -> str:
    if not value or any(character in value for character in ' \t"'):
        result = '"'
        backslashes = 0
        for character in value:
            if character == "\\":
                backslashes += 1
            elif character == '"':
                result += "\\" * (backslashes * 2 + 1) + '"'
                backslashes = 0
            else:
                result += "\\" * backslashes + character
                backslashes = 0
        return result + "\\" * (backslashes * 2) + '"'
    return value


def _command_line(tokens: tuple[str, ...]) -> str:
    if any(not token or "\0" in token for token in tokens):
        raise _ControllerError("observation_binding_rejected")
    return " ".join(_quote_windows_argument(token) for token in tokens)


def _environment_block(environment: tuple[tuple[str, str], ...]) -> object:
    names = [name.upper() for name, _ in environment]
    if len(names) != len(set(names)) or any(
        not name or "=" in name or "\0" in name or "\0" in value for name, value in environment
    ):
        raise _ControllerError("observation_binding_rejected")
    text = "\0".join(f"{name}={value}" for name, value in environment) + "\0"
    return ctypes.create_unicode_buffer(text, len(text) + 1)


def _canonical_bytes(document: Mapping[str, object]) -> bytes:
    return json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


def _tree_snapshot(
    root: Path,
    *,
    excluded_root_names: frozenset[str] = frozenset(),
) -> tuple[tuple[str, str, bytes], ...]:
    try:
        root_info = root.lstat()
    except OSError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    if not _ordinary_nonreparse(root_info, directory=True):
        raise _ControllerError("observation_binding_rejected")
    rows: list[tuple[str, str, bytes]] = []
    pending = [root]
    try:
        while pending:
            directory = pending.pop()
            before = directory.lstat()
            if not _ordinary_nonreparse(before, directory=True):
                raise _ControllerError("observation_binding_rejected")
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda item: item.name)
            after = directory.lstat()
            if _identity_tuple(before) != _identity_tuple(after):
                raise _ControllerError("observation_binding_rejected")
            children: list[Path] = []
            for entry in entries:
                path = Path(entry.path)
                relative_path = path.relative_to(root)
                if len(relative_path.parts) == 1 and entry.name in excluded_root_names:
                    continue
                info = path.lstat()
                relative = relative_path.as_posix()
                if _ordinary_nonreparse(info, directory=True):
                    rows.append((relative, "directory", b""))
                    children.append(path)
                elif _ordinary_nonreparse(info):
                    rows.append((relative, "file", _stable_file_bytes(path)))
                else:
                    raise _ControllerError("observation_binding_rejected")
            pending.extend(reversed(children))
    except OSError as exc:
        raise _ControllerError("observation_binding_rejected") from exc
    final_root_info = root.lstat()
    if _identity_tuple(final_root_info) != _identity_tuple(root_info):
        raise _ControllerError("observation_binding_rejected")
    return tuple(sorted(rows, key=lambda row: row[0]))


def _tree_digest(
    root: Path,
    *,
    excluded_root_names: frozenset[str] = frozenset(),
    schema_version: str = "trusted_owner_role_pool_install_tree.v1",
) -> str:
    rows = _tree_snapshot(root, excluded_root_names=excluded_root_names)
    document = {
        "schema_version": schema_version,
        "rows": [
            {
                "path": relative,
                "kind": kind,
                "byte_count": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
            for relative, kind, payload in rows
        ],
    }
    return hashlib.sha256(_canonical_bytes(document)).hexdigest()


class _AuditCounter:
    _PROCESS_EVENTS = frozenset({"subprocess.Popen", "os.system", "os.posix_spawn"})
    _ENVIRONMENT_EVENTS = frozenset({"os.putenv", "os.unsetenv"})
    _MUTATION_EVENTS = frozenset(
        {
            "os.chdir",
            "os.chmod",
            "os.link",
            "os.mkdir",
            "os.remove",
            "os.rename",
            "os.replace",
            "os.rmdir",
            "os.symlink",
            "os.truncate",
            "os.unlink",
            "os.utime",
        }
    )
    _DESTINATION_MUTATION_EVENTS = frozenset({"os.link", "os.rename", "os.replace", "os.symlink"})

    def __init__(self, repository_root: Path, installed_root: Path) -> None:
        self.repository_root = os.path.normcase(os.path.abspath(repository_root))
        self.installed_root = os.path.normcase(os.path.abspath(installed_root))
        self.counts = {"network": 0, "repository": 0, "installed": 0, "external": 0}
        self._registration_witness: object | None = None
        self._registration_observed = False

    @staticmethod
    def _write_open(args: tuple[object, ...]) -> bool:
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        if isinstance(mode, str) and any(marker in mode for marker in "wax+"):
            return True
        write_flags = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC | os.O_EXCL
        return isinstance(flags, int) and bool(flags & write_flags)

    def _record_write(self, value: object) -> None:
        try:
            path = os.path.normcase(os.path.abspath(os.fspath(value)))
            if os.path.commonpath((path, self.repository_root)) == self.repository_root:
                self.counts["repository"] += 1
            elif os.path.commonpath((path, self.installed_root)) == self.installed_root:
                self.counts["installed"] += 1
            else:
                self.counts["external"] += 1
        except (OSError, TypeError, ValueError):
            self.counts["external"] += 1
        raise _SafetyEffect

    def __call__(self, event: str, args: tuple[object, ...]) -> None:
        if event == _AUDIT_REGISTRATION_EVENT:
            if len(args) == 1 and args[0] is self._registration_witness:
                self._registration_observed = True
            return
        if event in self._PROCESS_EVENTS or event.startswith("os.spawn"):
            self.counts["external"] += 1
            raise _SafetyEffect
        if event.startswith("socket."):
            self.counts["network"] += 1
            raise _SafetyEffect
        if event in self._ENVIRONMENT_EVENTS:
            self.counts["external"] += 1
            raise _SafetyEffect
        if event == "open" and self._write_open(args):
            self._record_write(args[0] if args else None)
        if event in self._MUTATION_EVENTS:
            index = 1 if event in self._DESTINATION_MUTATION_EVENTS else 0
            self._record_write(args[index] if len(args) > index else None)

    def snapshot(self) -> _AuditCounts:
        return _AuditCounts(
            self.counts["network"],
            self.counts["repository"],
            self.counts["installed"],
            self.counts["external"],
        )


class _WindowsParentAdapter:
    def __init__(self) -> None:
        self.kernel32 = _kernel32()
        self.audit: _AuditCounter | None = None
        self.launch_calls = 0
        self.guard: _OwnedHandle | None = None
        self.controller_guard: _OwnedHandle | None = None
        self.checker_guard: _OwnedHandle | None = None
        self.checker_identity: tuple[int, int, int, int, str] | None = None
        self.checker_repository_root: Path | None = None
        self.last_target_exact: bool | None = None

    def runtime_identity(self) -> tuple[str, str]:
        return os.name, sys.platform

    def install_audit(self, repository_root: Path) -> None:
        if self.audit is not None:
            raise _ControllerError("observation_binding_rejected")
        installed = Path.home() / ".codex" / "skills" / "mythic-edge-role-pool"
        candidate = _AuditCounter(repository_root, installed)
        witness = object()
        candidate._registration_witness = witness
        try:
            sys.addaudithook(candidate)
            sys.audit(_AUDIT_REGISTRATION_EVENT, witness)
        except BaseException as exc:
            raise _ControllerError("observation_binding_rejected") from exc
        finally:
            candidate._registration_witness = None
        if not candidate._registration_observed:
            raise _ControllerError("observation_binding_rejected")
        self.audit = candidate

    def snapshot_effects(self, repository_root: Path) -> _EffectSnapshot:
        source = repository_root / "docs" / "codex_skills" / "mythic-edge-role-pool"
        installed = Path.home() / ".codex" / "skills" / "mythic-edge-role-pool"
        try:
            source_digest = _tree_digest(source)
            installed_digest = _tree_digest(installed)
            repository_digest = _tree_digest(
                repository_root,
                excluded_root_names=_REPOSITORY_METADATA_NAMES,
                schema_version="trusted_owner_repository_working_tree.v1",
            )
            fixed_rows = tuple(
                (relative.as_posix(), hashlib.sha256(_stable_file_bytes(repository_root / relative)).hexdigest())
                for relative in sorted(STATE_BINDINGS, key=lambda item: item.as_posix())
            )
            exact = (
                source_digest == "3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6"
                and installed_digest == source_digest
                and all(observed == STATE_BINDINGS[Path(relative)] for relative, observed in fixed_rows)
            )
            residue_candidates = (
                (repository_root / ".pytest_cache", "repository/.pytest_cache"),
                (repository_root / ".ruff_cache", "repository/.ruff_cache"),
                (repository_root / "tools" / "__pycache__", "repository/tools/__pycache__"),
                (repository_root / "tests" / "__pycache__", "repository/tests/__pycache__"),
                (
                    source / "scripts" / "__pycache__",
                    "source/scripts/__pycache__",
                ),
                (
                    installed / "scripts" / "__pycache__",
                    "installed/scripts/__pycache__",
                ),
            )
            residue = frozenset(
                f"{label}/{path.relative_to(root).as_posix()}"
                for root, label in residue_candidates
                if root.exists()
                for path in (root, *root.rglob("*"))
            )
        except BaseException:
            return _EffectSnapshot(False, "", "", frozenset())
        return _EffectSnapshot(exact, repository_digest, installed_digest, residue)

    def windows_directory(self) -> str:
        capacity = 32768
        buffer = ctypes.create_unicode_buffer(capacity)
        length = int(self.kernel32.GetWindowsDirectoryW(buffer, capacity))
        if length <= 0 or length >= capacity or not buffer.value:
            raise _ControllerError("observation_binding_rejected")
        return buffer.value

    def open_console(self) -> tuple[object, int]:
        handle = self.kernel32.GetStdHandle(ctypes.c_uint32(STD_INPUT_HANDLE).value)
        mode = wintypes.DWORD()
        if not handle or not self.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            raise _ControllerError("observation_binding_rejected")
        return int(handle), int(mode.value)

    def set_console_mode(self, console: object, mode: int) -> bool:
        return bool(self.kernel32.SetConsoleMode(wintypes.HANDLE(int(console)), mode))

    def audit_console_queue(self, console: object) -> _QueueAudit:
        first = wintypes.DWORD()
        if not self.kernel32.GetNumberOfConsoleInputEvents(wintypes.HANDLE(int(console)), ctypes.byref(first)):
            return _QueueAudit(None, (), None, None, False)
        count = int(first.value)
        if count > MAX_QUEUE_EVENTS:
            return _QueueAudit(count, (), None, None, False)
        records: tuple[_QueueRecord, ...] = ()
        returned_count: int | None = 0
        if count:
            buffer = (_InputRecord * count)()
            returned = wintypes.DWORD()
            if not self.kernel32.PeekConsoleInputW(
                wintypes.HANDLE(int(console)), buffer, count, ctypes.byref(returned)
            ):
                return _QueueAudit(count, (), None, None, False)
            returned_count = int(returned.value)
            records = tuple(
                _QueueRecord(
                    int(item.EventType),
                    bool(item.Event.KeyEvent.bKeyDown) if item.EventType == KEY_EVENT else False,
                    item.Event.KeyEvent.UnicodeChar if item.EventType == KEY_EVENT else "\0",
                )
                for item in buffer[: returned.value]
            )
            ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
        second = wintypes.DWORD()
        if not self.kernel32.GetNumberOfConsoleInputEvents(wintypes.HANDLE(int(console)), ctypes.byref(second)):
            return _QueueAudit(count, records, returned_count, None, False)
        return _QueueAudit(count, records, returned_count, int(second.value), True)

    def read_console_line(self, console: object, capacity: int) -> object:
        buffer = ctypes.create_unicode_buffer(capacity + 1)
        read = wintypes.DWORD()
        if not self.kernel32.ReadConsoleW(
            wintypes.HANDLE(int(console)), buffer, capacity, ctypes.byref(read), None
        ):
            ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
            raise _ControllerError("observation_binding_rejected")
        value = buffer[: read.value]
        ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
        return value

    def _open_executable_binding(
        self,
        private_path: object,
        resource_name: str,
    ) -> tuple[_TargetBinding, _OwnedHandle]:
        if type(private_path) is not str:
            raise _ControllerError("observation_binding_rejected")
        path_text = cast(str, private_path)
        if not _valid_private_target_text(path_text):
            raise _ControllerError("observation_binding_rejected")
        pure = PureWindowsPath(path_text)
        parts = pure.parts
        path = Path(path_text)
        current = Path(pure.anchor)
        for part in parts[1:]:
            current /= part
            info = current.lstat()
            if current == path:
                if not _ordinary_nonreparse(info):
                    raise _ControllerError("observation_binding_rejected")
            elif not _ordinary_nonreparse(info, directory=True):
                raise _ControllerError("observation_binding_rejected")
        guard = _OwnedHandle(
            self.kernel32,
            resource_name,
            cast(
                int,
                self.kernel32.CreateFileW(
                    path_text,
                    GENERIC_READ | FILE_READ_ATTRIBUTES | FILE_EXECUTE,
                    FILE_SHARE_READ,
                    None,
                    OPEN_EXISTING,
                    FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OPEN_REPARSE_POINT,
                    None,
                ),
            ),
        )
        if not guard.open:
            raise _ControllerError("observation_binding_rejected")
        try:
            payload = _stable_file_bytes(path)
            info = path.lstat()
            file_version, product_version = _file_versions(path_text)
            if VERSION_PATTERN.fullmatch(file_version) is None or VERSION_PATTERN.fullmatch(product_version) is None:
                raise _ControllerError("observation_binding_rejected")
            identity = _FileIdentity(
                int(info.st_dev),
                int(info.st_ino),
                int(info.st_size),
                int(info.st_mtime_ns),
                hashlib.sha256(payload).hexdigest(),
                file_version,
                product_version,
                _handle_stable_identity(self.kernel32, guard),
            )
        except BaseException:
            guard.close()
            raise
        return _TargetBinding(bytearray(path_text.encode("utf-16-le")), identity), guard

    def validate_controller_image(self) -> _TargetBinding:
        if self.controller_guard is not None:
            raise _ControllerError("observation_binding_rejected")
        if sys.implementation.name != "cpython":
            raise _ControllerError("observation_host_rejected")
        capacity = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(capacity.value)
        try:
            process = self.kernel32.GetCurrentProcess()
            if not process or not self.kernel32.QueryFullProcessImageNameW(
                process,
                0,
                buffer,
                ctypes.byref(capacity),
            ):
                raise _ControllerError("observation_binding_rejected")
            path_text = buffer.value
            if not path_text or int(capacity.value) != len(path_text):
                raise _ControllerError("observation_binding_rejected")
            binding, guard = self._open_executable_binding(
                path_text,
                "controller_image_guard",
            )
        finally:
            ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
        self.controller_guard = guard
        return binding

    def validate_target(self, private_line: object) -> _TargetBinding:
        if self.guard is not None:
            raise _ControllerError("observation_binding_rejected")
        binding, guard = self._open_executable_binding(private_line, "target_guard")
        self.guard = guard
        return binding

    def clear_private(self, *values: object) -> bool:
        exact = True
        for value in values:
            if isinstance(value, bytearray):
                value[:] = b"\0" * len(value)
            elif value is not None and not isinstance(value, str):
                exact = False
        return exact

    def image_bindings_exact(
        self,
        controller: _TargetBinding,
        target: _TargetBinding,
    ) -> bool | None:
        if (
            self.controller_guard is None
            or self.guard is None
            or not self.controller_guard.open
            or not self.guard.open
        ):
            return None
        try:
            controller_path = bytes(cast(bytearray, controller.opaque_path)).decode("utf-16-le")
            target_path = bytes(cast(bytearray, target.opaque_path)).decode("utf-16-le")
            return (
                _handle_stable_identity(self.kernel32, self.controller_guard)
                == controller.identity.stable_identity_sha256
                == target.identity.stable_identity_sha256
                == _handle_stable_identity(self.kernel32, self.guard)
                and _path_identity_exact(controller_path, controller.identity) is True
                and _path_identity_exact(target_path, target.identity) is True
            )
        except BaseException:
            return None

    def launch_once(self, request: _LaunchRequest) -> _LaunchEvidence:
        self.launch_calls += 1
        if (
            self.launch_calls != 1
            or self.guard is None
            or not self.guard.open
            or self.controller_guard is None
            or not self.controller_guard.open
        ):
            raise _SafetyEffect
        if (
            _handle_stable_identity(self.kernel32, self.controller_guard)
            != request.target.identity.stable_identity_sha256
            or _handle_stable_identity(self.kernel32, self.guard)
            != request.target.identity.stable_identity_sha256
        ):
            raise _ControllerError("observation_binding_rejected")
        if (
            len(request.tokens) != 4
            or request.tokens[:3] != ("python.exe", "-B", FIXED_CHILD_SCRIPT)
            or _validate_observation_id(request.tokens[3]) != request.tokens[3]
            or request.timeout_seconds != TIMEOUT_SECONDS
            or request.max_stdout_bytes != MAX_STDOUT_BYTES
            or request.max_stderr_bytes != MAX_STDERR_BYTES
            or request.environment != _fixed_environment(self.windows_directory())
        ):
            raise _ControllerError("observation_binding_rejected")
        if self.checker_guard is not None or self.checker_identity is not None:
            raise _ControllerError("observation_binding_rejected")
        try:
            self.checker_guard = _open_checker_guard(
                request.repository_root,
                self.kernel32,
            )
            self.checker_repository_root = request.repository_root
            self.checker_identity = _checker_file_identity(
                request.repository_root / OWNER_PATH
            )
            if self.checker_identity[-1] != FROZEN_BINDINGS[OWNER_PATH]:
                raise _ControllerError("observation_binding_rejected")
        except BaseException:
            _checker_exact, checker_close = self.finish_checker_guard()
            self.guard.close()
            target_close = self.guard.observation()
            self.controller_guard.close()
            controller_close = self.controller_guard.observation()
            if any(
                observation is not None
                and (
                    observation.attempt_count != 1
                    or observation.succeeded is not True
                )
                for observation in (checker_close, target_close, controller_close)
            ):
                raise _ControllerError("observation_timeout_unknown") from None
            raise
        path = bytes(cast(bytearray, request.target.opaque_path)).decode("utf-16-le")
        evidence = _execute_windows_once(
            request,
            path,
            self.kernel32,
            self.controller_guard,
            self.guard,
        )
        self.last_target_exact = evidence.target_identity_exact
        return evidence

    def finish_image_guards(self) -> tuple[_CloseObservation, ...]:
        observations: list[_CloseObservation] = []
        for attribute in ("guard", "controller_guard"):
            guard = cast(_OwnedHandle | None, getattr(self, attribute))
            if guard is not None:
                guard.close()
                observations.append(guard.observation())
        return tuple(observations)

    def finish_checker_guard(self) -> tuple[bool | None, _CloseObservation | None]:
        guard = self.checker_guard
        identity = self.checker_identity
        repository_root = self.checker_repository_root
        if guard is None:
            return None, None
        try:
            exact = (
                _checker_identity_exact(repository_root, identity)
                if identity is not None and repository_root is not None
                else None
            )
        finally:
            guard.close()
            observation = guard.observation()
            self.checker_guard = None
            self.checker_identity = None
            self.checker_repository_root = None
        return exact, observation

    def target_identity_exact(self, target: _TargetBinding) -> bool | None:
        del target
        return self.last_target_exact

    def audit_counts(self) -> _AuditCounts:
        if self.audit is None:
            raise _ControllerError("observation_timeout_unknown")
        return self.audit.snapshot()


def _execute_windows_once(
    request: _LaunchRequest,
    private_path: str,
    kernel32: object,
    controller_guard: _OwnedHandle,
    target_guard: _OwnedHandle,
) -> _LaunchEvidence:
    handles: dict[str, _OwnedHandle] = {
        "controller_image_guard": controller_guard,
        "target_guard": target_guard,
    }
    attributes = _OwnedAttributeList(kernel32)
    information = _ProcessInformation()
    attempts = 0
    created: bool | None = False
    events: list[_JobEvent] = []
    stdout = bytearray()
    stderr = bytearray()
    stdout_eof = stderr_eof = False
    stdout_overflow = stderr_overflow = False
    timed_out = False
    termination_requested = False
    termination_succeeded: bool | None = None
    event_exact = True
    process_stopped = False
    total: int | None = None
    active: int | None = None
    exit_code: int | None = None
    identity_exact: bool | None = None
    target_exact: bool | None = None
    grace_deadline: float | None = None
    try:
        security = _SecurityAttributes(ctypes.sizeof(_SecurityAttributes), None, True)
        for prefix in ("stdin", "stdout", "stderr"):
            read = wintypes.HANDLE()
            write = wintypes.HANDLE()
            if not kernel32.CreatePipe(ctypes.byref(read), ctypes.byref(write), ctypes.byref(security), 0):
                raise _ControllerError("observation_launch_unknown")
            handles[f"{prefix}_read"] = _OwnedHandle(kernel32, f"{prefix}_read", cast(int, read.value))
            handles[f"{prefix}_write"] = _OwnedHandle(kernel32, f"{prefix}_write", cast(int, write.value))
        for name in ("stdin_write", "stdout_read", "stderr_read"):
            if not kernel32.SetHandleInformation(wintypes.HANDLE(handles[name].value), HANDLE_FLAG_INHERIT, 0):
                raise _ControllerError("observation_launch_unknown")
        handles["job"] = _OwnedHandle(kernel32, "job", cast(int, kernel32.CreateJobObjectW(None, None)))
        limits = _JobExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        limits.BasicLimitInformation.ActiveProcessLimit = 1
        if not handles["job"].open or not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            raise _ControllerError("observation_launch_unknown")
        invalid = wintypes.HANDLE(ctypes.c_void_p(-1).value)
        handles["completion_port"] = _OwnedHandle(
            kernel32, "completion_port", cast(int, kernel32.CreateIoCompletionPort(invalid, None, 0, 1))
        )
        association = _JobAssociateCompletionPort(None, wintypes.HANDLE(handles["completion_port"].value))
        if not handles["completion_port"].open or not kernel32.SetInformationJobObject(
            wintypes.HANDLE(handles["job"].value),
            JOB_OBJECT_ASSOCIATE_COMPLETION_PORT_INFORMATION_CLASS,
            ctypes.byref(association),
            ctypes.sizeof(association),
        ):
            raise _ControllerError("observation_launch_unknown")
        attribute_list = attributes.initialize()
        inherited = (wintypes.HANDLE * 3)(
            wintypes.HANDLE(handles["stdin_read"].value),
            wintypes.HANDLE(handles["stdout_write"].value),
            wintypes.HANDLE(handles["stderr_write"].value),
        )
        jobs = (wintypes.HANDLE * 1)(wintypes.HANDLE(handles["job"].value))
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
            ctypes.byref(inherited),
            ctypes.sizeof(inherited),
            None,
            None,
        ) or not kernel32.UpdateProcThreadAttribute(
            attribute_list, 0, PROC_THREAD_ATTRIBUTE_JOB_LIST, ctypes.byref(jobs), ctypes.sizeof(jobs), None, None
        ):
            raise _ControllerError("observation_launch_unknown")
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
        target_exact = _require_precreate_target_identity(private_path, request.target.identity)
        deadline = time.monotonic() + request.timeout_seconds
        created = None
        attempts = 1
        created = bool(
            kernel32.CreateProcessW(
                private_path,
                command_line,
                None,
                None,
                True,
                CREATE_NO_WINDOW | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT,
                ctypes.cast(environment, wintypes.LPVOID),
                os.fspath(request.repository_root),
                ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_StartupInfoW)),
                ctypes.byref(information),
            )
        )
        ctypes.memset(ctypes.addressof(command_line), 0, ctypes.sizeof(command_line))
        if not created:
            raise _ControllerError("observation_launch_unknown")
        handles["process"] = _OwnedHandle(kernel32, "process", cast(int, information.hProcess))
        handles["thread"] = _OwnedHandle(kernel32, "thread", cast(int, information.hThread))
        attributes.close()
        for name in ("stdin_read", "stdout_write", "stderr_write", "thread"):
            handles[name].close()
        while True:
            service_deadline = grace_deadline if grace_deadline is not None else deadline
            completion_queue_empty = False
            if time.monotonic() < service_deadline:
                cycle_exact, completion_queue_empty = _drain_job_events(
                    kernel32,
                    handles["completion_port"],
                    events,
                    service_deadline,
                )
                event_exact = cycle_exact and event_exact
            if time.monotonic() < service_deadline:
                stdout_eof, stdout_overflow, out_exact = _drain_pipe(
                    kernel32,
                    handles["stdout_read"],
                    stdout,
                    request.max_stdout_bytes,
                    stdout_eof,
                    stdout_overflow,
                    service_deadline,
                )
                event_exact = event_exact and out_exact
            if time.monotonic() < service_deadline:
                stderr_eof, stderr_overflow, err_exact = _drain_pipe(
                    kernel32,
                    handles["stderr_read"],
                    stderr,
                    request.max_stderr_bytes,
                    stderr_eof,
                    stderr_overflow,
                    service_deadline,
                )
                event_exact = event_exact and err_exact
            if time.monotonic() < service_deadline:
                process_stopped = (
                    kernel32.WaitForSingleObject(
                        wintypes.HANDLE(handles["process"].value), 0
                    )
                    == WAIT_OBJECT_0
                )
            if time.monotonic() < service_deadline:
                total, active = _query_accounting(kernel32, handles["job"])
            unsafe = (
                stdout_overflow
                or stderr_overflow
                or not event_exact
                or any(event.kind == "active_limit" for event in events)
                or (type(total) is int and total > 1)
            )
            now = time.monotonic()
            if grace_deadline is None and now >= deadline:
                timed_out = True
                unsafe = True
            complete = (
                completion_queue_empty
                and process_stopped
                and active == 0
                and stdout_eof
                and stderr_eof
                and any(event.kind == "active_zero" for event in events)
            )
            if unsafe and not termination_requested:
                termination_requested = True
                termination_succeeded = bool(kernel32.TerminateJobObject(wintypes.HANDLE(handles["job"].value), 1))
                grace_deadline = now + TERMINATION_GRACE_SECONDS
            if complete or (grace_deadline is not None and now >= grace_deadline):
                break
            time.sleep(0.01)
        code = wintypes.DWORD(STILL_ACTIVE)
        if (
            kernel32.GetExitCodeProcess(
                wintypes.HANDLE(handles["process"].value), ctypes.byref(code)
            )
            and code.value != STILL_ACTIVE
        ):
            exit_code = int(code.value)
        identity_exact = _query_process_identity(
            kernel32, handles["process"], request.target.identity
        )
        target_exact = _path_identity_exact(private_path, request.target.identity)
    except BaseException as exc:
        event_exact = False
        if created is False and isinstance(exc, _ControllerError):
            raise
        if attempts == 1 and created is not False:
            if _adopt_returned_process_handles(kernel32, handles, information):
                created = True
            attributes.close()
            for name in ("stdin_read", "stdout_write", "stderr_write", "thread"):
                handle = handles.get(name)
                if handle is not None:
                    handle.close()
            (
                termination_requested,
                termination_succeeded,
                stdout_eof,
                stderr_eof,
                stdout_overflow,
                stderr_overflow,
                process_stopped,
                total,
                active,
            ) = _recover_postcreation_failure(
                kernel32,
                handles,
                events,
                stdout,
                stderr,
                request,
                stdout_eof,
                stderr_eof,
                stdout_overflow,
                stderr_overflow,
                termination_requested,
                termination_succeeded,
            )
    finally:
        for name in reversed(tuple(handles)):
            handles[name].close()
        attributes.close()
    if not event_exact:
        events.append(_JobEvent("unknown", None))
    closes = tuple(handle.observation() for handle in handles.values()) + (attributes.observation(),)
    return _LaunchEvidence(
        attempts,
        created,
        int(information.dwProcessId) if created is True else None,
        True if created is True else None,
        True,
        tuple(events),
        total,
        active,
        exit_code,
        bytes(stdout),
        bytes(stderr),
        stdout_eof,
        stderr_eof,
        stdout_overflow,
        stderr_overflow,
        identity_exact,
        target_exact,
        timed_out,
        termination_requested,
        termination_succeeded,
        process_stopped and active == 0,
        closes,
    )


def _adopt_returned_process_handles(
    kernel32: object,
    handles: dict[str, _OwnedHandle],
    information: _ProcessInformation,
) -> bool:
    for name, value in (
        ("process", int(information.hProcess or 0)),
        ("thread", int(information.hThread or 0)),
    ):
        if value and name not in handles:
            handles[name] = _OwnedHandle(kernel32, name, value)
    process = handles.get("process")
    return process is not None and process.open


def _query_accounting(kernel32: object, job: _OwnedHandle) -> tuple[int | None, int | None]:
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


def _reconcile_after_failure(
    kernel32: object,
    handles: Mapping[str, _OwnedHandle],
    events: list[_JobEvent],
    stdout: bytearray,
    stderr: bytearray,
    request: _LaunchRequest,
    stdout_eof: bool,
    stderr_eof: bool,
    stdout_overflow: bool,
    stderr_overflow: bool,
) -> tuple[bool, bool, bool, bool, bool, int | None, int | None]:
    deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
    process_stopped = False
    total: int | None = None
    active: int | None = None
    while True:
        if time.monotonic() < deadline:
            try:
                _drain_job_events(
                    kernel32,
                    handles["completion_port"],
                    events,
                    deadline,
                )
            except BaseException:
                pass
        if time.monotonic() < deadline:
            try:
                stdout_eof, stdout_overflow, _stdout_exact = _drain_pipe(
                    kernel32,
                    handles["stdout_read"],
                    stdout,
                    request.max_stdout_bytes,
                    stdout_eof,
                    stdout_overflow,
                    deadline,
                )
            except BaseException:
                pass
        if time.monotonic() < deadline:
            try:
                stderr_eof, stderr_overflow, _stderr_exact = _drain_pipe(
                    kernel32,
                    handles["stderr_read"],
                    stderr,
                    request.max_stderr_bytes,
                    stderr_eof,
                    stderr_overflow,
                    deadline,
                )
            except BaseException:
                pass
        if time.monotonic() < deadline:
            try:
                process_stopped = (
                    kernel32.WaitForSingleObject(wintypes.HANDLE(handles["process"].value), 0)
                    == WAIT_OBJECT_0
                )
            except BaseException:
                process_stopped = False
        if time.monotonic() < deadline:
            try:
                total, active = _query_accounting(kernel32, handles["job"])
            except BaseException:
                total = active = None
        now = time.monotonic()
        if process_stopped and active == 0 and stdout_eof and stderr_eof:
            break
        if now >= deadline:
            break
        try:
            time.sleep(0.01)
        except BaseException:
            pass
    return (
        stdout_eof,
        stderr_eof,
        stdout_overflow,
        stderr_overflow,
        process_stopped,
        total,
        active,
    )


def _recover_postcreation_failure(
    kernel32: object,
    handles: Mapping[str, _OwnedHandle],
    events: list[_JobEvent],
    stdout: bytearray,
    stderr: bytearray,
    request: _LaunchRequest,
    stdout_eof: bool,
    stderr_eof: bool,
    stdout_overflow: bool,
    stderr_overflow: bool,
    termination_requested: bool,
    termination_succeeded: bool | None,
) -> tuple[bool, bool | None, bool, bool, bool, bool, bool, int | None, int | None]:
    job = handles.get("job")
    if not termination_requested and job is not None and job.open:
        termination_requested = True
        try:
            termination_succeeded = bool(
                kernel32.TerminateJobObject(wintypes.HANDLE(job.value), 1)
            )
        except BaseException:
            termination_succeeded = False
    reconciliation = _reconcile_after_failure(
        kernel32,
        handles,
        events,
        stdout,
        stderr,
        request,
        stdout_eof,
        stderr_eof,
        stdout_overflow,
        stderr_overflow,
    )
    return termination_requested, termination_succeeded, *reconciliation


def _path_identity_exact(path_text: str, expected: _FileIdentity) -> bool | None:
    try:
        path = Path(path_text)
        payload = _stable_file_bytes(path)
        info = path.lstat()
        file_version, product_version = _file_versions(path_text)
    except BaseException:
        return None
    return (
        int(info.st_dev),
        int(info.st_ino),
        int(info.st_size),
        int(info.st_mtime_ns),
        hashlib.sha256(payload).hexdigest(),
        file_version,
        product_version,
    ) == (
        expected.device,
        expected.inode,
        expected.size,
        expected.modified_ns,
        expected.sha256,
        expected.file_version,
        expected.product_version,
    )


def _require_precreate_target_identity(path_text: str, expected: _FileIdentity) -> bool:
    if _path_identity_exact(path_text, expected) is not True:
        raise _ControllerError("observation_binding_rejected")
    return True


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
        return _path_identity_exact(buffer.value, expected)
    finally:
        ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))


def _drain_job_events(
    kernel32: object,
    port: _OwnedHandle,
    events: list[_JobEvent],
    deadline: float,
) -> tuple[bool, bool]:
    for _ in range(MAX_COMPLETION_EVENTS_PER_CYCLE):
        if time.monotonic() >= deadline:
            return True, False
        message = wintypes.DWORD()
        key = ctypes.c_size_t()
        overlapped = wintypes.LPVOID()
        ok = kernel32.GetQueuedCompletionStatus(
            wintypes.HANDLE(port.value), ctypes.byref(message), ctypes.byref(key), ctypes.byref(overlapped), 0
        )
        deadline_reached = time.monotonic() >= deadline
        if not ok:
            empty = ctypes.get_last_error() == WAIT_TIMEOUT
            return empty, empty
        pid = int(ctypes.cast(overlapped, ctypes.c_void_p).value or 0)
        if message.value == JOB_OBJECT_MSG_NEW_PROCESS:
            events.append(_JobEvent("new", pid))
        elif message.value in {JOB_OBJECT_MSG_EXIT_PROCESS, JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS}:
            events.append(_JobEvent("exit", pid))
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO:
            events.append(_JobEvent("active_zero", None))
        elif message.value == JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT:
            events.append(_JobEvent("active_limit", None))
        else:
            return False, False
        if deadline_reached:
            return True, False
    return True, False


def _drain_pipe(
    kernel32: object,
    handle: _OwnedHandle,
    retained: bytearray,
    limit: int,
    prior_eof: bool,
    prior_overflow: bool,
    deadline: float,
) -> tuple[bool, bool, bool]:
    eof = prior_eof
    overflow = prior_overflow
    if eof or time.monotonic() >= deadline:
        return eof, overflow, True
    available = wintypes.DWORD()
    if not kernel32.PeekNamedPipe(
        wintypes.HANDLE(handle.value), None, 0, None, ctypes.byref(available), None
    ):
        if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
            eof = True
            return eof, overflow, True
        return eof, overflow, False
    if time.monotonic() >= deadline or available.value == 0:
        return eof, overflow, True
    room = max(0, limit - len(retained))
    size = min(int(available.value), room + 1, 65536)
    chunk = ctypes.create_string_buffer(size)
    read = wintypes.DWORD()
    if time.monotonic() >= deadline:
        return eof, overflow, True
    read_ok = kernel32.ReadFile(
        wintypes.HANDLE(handle.value), chunk, size, ctypes.byref(read), None
    )
    deadline_reached = time.monotonic() >= deadline
    if not read_ok:
        if ctypes.get_last_error() == ERROR_BROKEN_PIPE:
            eof = True
            return eof, overflow, True
        return eof, overflow, False
    payload = chunk.raw[: read.value]
    retained.extend(payload[:room])
    overflow = overflow or len(payload) > room
    if deadline_reached:
        return eof, overflow, True
    return eof, overflow, True


def _write_exact(stream: object, payload: bytes) -> None:
    binary = getattr(stream, "buffer", None)
    if binary is None:
        text = payload.decode("utf-8")
        written = stream.write(text)
        expected = len(text)
        selected = stream
    else:
        written = binary.write(payload)
        expected = len(payload)
        selected = binary
    if written != expected:
        raise OSError
    selected.flush()


def _emit_failure(status: str) -> None:
    if status not in _CLOSED_FAILURE_STATUSES:
        status = "observation_result_unknown"
    _write_exact(sys.stderr, status.encode("ascii") + b"\n")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    try:
        if os.name != "nt" or sys.platform != "win32":
            raise _ControllerError("observation_host_rejected")
        metadata_mode = arguments == ("--emit-target-binding",)
        if metadata_mode:
            observation_id = None
            expected_binding = None
        elif (
            len(arguments) == 3
            and arguments[1] == "--expected-target-binding-v1"
            and type(arguments[0]) is str
            and not arguments[0].startswith("-")
        ):
            observation_id = _validate_observation_id(arguments[0])
            expected_binding = _decode_target_binding_transport(arguments[2])
        else:
            raise _ControllerError("observation_sequence_rejected")
        root = _repository_root()
        if metadata_mode:
            result = _run_metadata(_WindowsParentAdapter(), repository_root=root)
        else:
            if observation_id is None or expected_binding is None:
                raise _ControllerError("observation_sequence_rejected")
            owner = _load_owner(root)
            result = _run_controller(
                observation_id,
                expected_binding,
                _WindowsParentAdapter(),
                repository_root=root,
                owner=owner,
            )
    except _ControllerError as exc:
        result = exc.status
    except BaseException:
        result = "observation_result_unknown"
    if type(result) is bytes:
        try:
            _write_exact(sys.stdout, result)
            return 0
        except BaseException:
            result = "observation_result_unknown"
    status = result if type(result) is str else "observation_result_unknown"
    _emit_failure(status)
    return _STATUS_EXIT_CODES.get(status, 2)


if __name__ == "__main__":
    raise SystemExit(main())
