#!/usr/bin/env python3
"""Classify the fixed R0 prelaunch gates without entering child creation."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Protocol

MATRIX_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_prelaunch_gate_matrix.md"
)
OBSERVER_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_offline_observation_"
    "trusted_launch_observer.md"
)
PROPORTIONATE_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_"
    "observation_successor.md"
)
OWNER_PATH = Path("tools/check_role_pool_r0_offline_observation.py")
OWNER_TEST_PATH = Path("tests/test_check_role_pool_r0_offline_observation.py")
OBSERVER_PATH = Path("tools/run_role_pool_r0_trusted_launch_observer.py")
OBSERVER_TEST_PATH = Path("tests/test_run_role_pool_r0_trusted_launch_observer.py")
MATRIX_PATH = Path("tools/check_role_pool_r0_prelaunch_gate_matrix.py")

MATRIX_CONTRACT_SHA256 = (
    "58e553452602a991950eaa02ff20ac26c45cee2dcf891e069e45ea9e300f0840"
)
FROZEN_BINDINGS = {
    MATRIX_CONTRACT_PATH: MATRIX_CONTRACT_SHA256,
    PROPORTIONATE_CONTRACT_PATH: (
        "129ceb8f2bb21f4773e8258ad04238784d986c14168179e1d009b30c584588ae"
    ),
    OBSERVER_CONTRACT_PATH: (
        "dd1e54709d3d9c33ff957d3057f0840ce8243678ecdcb3f3e1bc9ef140563c34"
    ),
    OWNER_PATH: "ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5",
    OWNER_TEST_PATH: (
        "79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784"
    ),
    OBSERVER_PATH: (
        "ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a"
    ),
    OBSERVER_TEST_PATH: (
        "e504f417a9d47e24f095b7354facaf4ae6cad98fa129b01370bdee656bad4be1"
    ),
}

SCHEMA_VERSION = "trusted_owner_r0_prelaunch_gate_matrix.v1"
MINIMUM_COMPLETE_STATE = "prelaunch_matrix_complete_child_creation_not_entered"
EVALUATED_STATE = "gate_evaluated_before_child_creation"
BLOCKED_STATE = "gate_not_evaluated_dependency_blocked"
FAILURE_LINE = b"r0_prelaunch_gate_matrix_failed\n"
_AUDIT_REGISTRATION_EVENT = (
    "mythic_edge.r0_prelaunch_gate_matrix.audit_registration_probe"
)

GATE_FIELDS = (
    "gate_id",
    "result",
    "reason_code",
    "dependencies",
    "minimum_lifecycle_state",
)
AGGREGATE_FIELDS = (
    "schema_version",
    "aggregate_result",
    "minimum_lifecycle_state",
    "gates",
)
_REPARSE_MARKER = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


@dataclass(frozen=True)
class _GateSpec:
    gate_id: str
    dependencies: tuple[str, ...]
    method_name: str | None
    ordinary_reason: str | None


GATE_REGISTRY = (
    _GateSpec(
        "PLG-01-runtime-bytecode",
        (),
        "probe_runtime_bytecode",
        "runtime_or_bytecode_rejected",
    ),
    _GateSpec(
        "PLG-02-repository-root",
        (),
        "probe_repository_root",
        "repository_root_rejected",
    ),
    _GateSpec(
        "PLG-03-frozen-owner-api",
        ("PLG-02-repository-root",),
        "probe_frozen_owner_api",
        "frozen_owner_api_rejected",
    ),
    _GateSpec(
        "PLG-04-installed-release-state",
        ("PLG-02-repository-root", "PLG-03-frozen-owner-api"),
        "probe_installed_release_state",
        "installed_release_state_rejected",
    ),
    _GateSpec(
        "PLG-05-prelaunch-effect-snapshot",
        (
            "PLG-02-repository-root",
            "PLG-03-frozen-owner-api",
            "PLG-04-installed-release-state",
        ),
        "probe_prelaunch_effect_snapshot",
        "prelaunch_effect_snapshot_rejected",
    ),
    _GateSpec(
        "PLG-06-fixed-launcher-identity",
        ("PLG-01-runtime-bytecode",),
        "probe_fixed_launcher_identity",
        "fixed_launcher_identity_rejected",
    ),
    _GateSpec(
        "PLG-07-fixed-request-prerequisites",
        (
            "PLG-01-runtime-bytecode",
            "PLG-02-repository-root",
            "PLG-03-frozen-owner-api",
            "PLG-06-fixed-launcher-identity",
        ),
        "probe_fixed_request_prerequisites",
        "fixed_request_prerequisite_rejected",
    ),
    _GateSpec(
        "PLG-08-launcher-guard-revalidation",
        (
            "PLG-01-runtime-bytecode",
            "PLG-06-fixed-launcher-identity",
            "PLG-07-fixed-request-prerequisites",
        ),
        "probe_launcher_guard_revalidation",
        "launcher_guard_revalidation_rejected",
    ),
    _GateSpec(
        "PLG-09-exact-ready",
        tuple(f"PLG-{index:02d}-{suffix}" for index, suffix in (
            (1, "runtime-bytecode"),
            (2, "repository-root"),
            (3, "frozen-owner-api"),
            (4, "installed-release-state"),
            (5, "prelaunch-effect-snapshot"),
            (6, "fixed-launcher-identity"),
            (7, "fixed-request-prerequisites"),
            (8, "launcher-guard-revalidation"),
        )),
        None,
        None,
    ),
)


class PrelaunchGateAdapter(Protocol):
    def probe_runtime_bytecode(self) -> object: ...

    def probe_repository_root(self) -> object: ...

    def probe_frozen_owner_api(self, repository_root: object) -> object: ...

    def probe_installed_release_state(
        self,
        repository_root: object,
        owner_api: object,
    ) -> object: ...

    def probe_prelaunch_effect_snapshot(
        self,
        repository_root: object,
        owner_api: object,
        installed_root: object,
    ) -> object: ...

    def probe_fixed_launcher_identity(self) -> object: ...

    def probe_fixed_request_prerequisites(
        self,
        repository_root: object,
        owner_api: object,
        launcher: object,
    ) -> object: ...

    def probe_launcher_guard_revalidation(self, launcher: object) -> object: ...


class _MatrixFailure(RuntimeError):
    pass


class _BoundaryViolation(_MatrixFailure):
    pass


class _ProbeRejected(RuntimeError):
    pass


class _ProbeUnknown(RuntimeError):
    def __init__(self, reason_code: str = "probe_unavailable_or_ambiguous") -> None:
        if reason_code not in {
            "probe_unavailable_or_ambiguous",
            "cleanup_unconfirmed",
        }:
            raise ValueError("probe_reason_invalid")
        self.reason_code = reason_code
        super().__init__(reason_code)


def _gate_row(
    spec: _GateSpec,
    result: str,
    reason_code: str,
) -> dict[str, object]:
    return {
        "gate_id": spec.gate_id,
        "result": result,
        "reason_code": reason_code,
        "dependencies": list(spec.dependencies),
        "minimum_lifecycle_state": (
            BLOCKED_STATE if result == "blocked" else EVALUATED_STATE
        ),
    }


def _probe_arguments(
    gate_id: str,
    payloads: Mapping[str, object],
) -> tuple[object, ...]:
    if gate_id in {
        "PLG-01-runtime-bytecode",
        "PLG-02-repository-root",
        "PLG-06-fixed-launcher-identity",
    }:
        return ()
    if gate_id == "PLG-03-frozen-owner-api":
        return (payloads["PLG-02-repository-root"],)
    if gate_id == "PLG-04-installed-release-state":
        return (
            payloads["PLG-02-repository-root"],
            payloads["PLG-03-frozen-owner-api"],
        )
    if gate_id == "PLG-05-prelaunch-effect-snapshot":
        return (
            payloads["PLG-02-repository-root"],
            payloads["PLG-03-frozen-owner-api"],
            payloads["PLG-04-installed-release-state"],
        )
    if gate_id == "PLG-07-fixed-request-prerequisites":
        return (
            payloads["PLG-02-repository-root"],
            payloads["PLG-03-frozen-owner-api"],
            payloads["PLG-06-fixed-launcher-identity"],
        )
    if gate_id == "PLG-08-launcher-guard-revalidation":
        return (payloads["PLG-06-fixed-launcher-identity"],)
    raise _MatrixFailure("gate_dispatch_invalid")


def _derive_aggregate_result(gates: Sequence[Mapping[str, object]]) -> str:
    if any(gate.get("result") == "unknown_failed_closed" for gate in gates):
        return "indeterminate_failed_closed"
    if gates[-1].get("result") == "passed":
        return "exact_ready"
    return "not_ready"


def _validate_gate_row(
    row: Mapping[str, object],
    spec: _GateSpec,
    prior_results: Mapping[str, str],
) -> None:
    if tuple(row) != GATE_FIELDS:
        raise _MatrixFailure("gate_fields_invalid")
    if row["gate_id"] != spec.gate_id:
        raise _MatrixFailure("gate_identity_invalid")
    if row["dependencies"] != list(spec.dependencies):
        raise _MatrixFailure("gate_dependencies_invalid")
    result = row["result"]
    reason = row["reason_code"]
    lifecycle = row["minimum_lifecycle_state"]
    if type(result) is not str or type(reason) is not str or type(lifecycle) is not str:
        raise _MatrixFailure("gate_type_invalid")
    dependencies_passed = all(
        prior_results.get(dependency) == "passed" for dependency in spec.dependencies
    )
    if result == "blocked":
        if dependencies_passed or reason != "dependency_not_passed" or lifecycle != BLOCKED_STATE:
            raise _MatrixFailure("gate_blocked_invalid")
        return
    if not dependencies_passed or lifecycle != EVALUATED_STATE:
        raise _MatrixFailure("gate_evaluation_invalid")
    if result == "passed":
        expected_reason = "all_prelaunch_gates_exact" if spec.method_name is None else "exact"
        if reason != expected_reason:
            raise _MatrixFailure("gate_pass_invalid")
        return
    if spec.method_name is None:
        raise _MatrixFailure("aggregate_gate_result_invalid")
    if result == "failed" and reason == spec.ordinary_reason:
        return
    if result == "unknown_failed_closed" and reason in {
        "probe_unavailable_or_ambiguous",
        "cleanup_unconfirmed",
    }:
        return
    raise _MatrixFailure("gate_result_invalid")


def _render_aggregate(aggregate: Mapping[str, object]) -> bytes:
    if tuple(aggregate) != AGGREGATE_FIELDS:
        raise _MatrixFailure("aggregate_fields_invalid")
    if aggregate["schema_version"] != SCHEMA_VERSION:
        raise _MatrixFailure("aggregate_schema_invalid")
    if aggregate["minimum_lifecycle_state"] != MINIMUM_COMPLETE_STATE:
        raise _MatrixFailure("aggregate_lifecycle_invalid")
    gates = aggregate["gates"]
    if type(gates) is not list or len(gates) != len(GATE_REGISTRY):
        raise _MatrixFailure("aggregate_gates_invalid")
    prior_results: dict[str, str] = {}
    for row, spec in zip(gates, GATE_REGISTRY, strict=True):
        if type(row) is not dict:
            raise _MatrixFailure("gate_object_invalid")
        _validate_gate_row(row, spec, prior_results)
        prior_results[spec.gate_id] = str(row["result"])
    expected = _derive_aggregate_result(gates)
    if aggregate["aggregate_result"] != expected:
        raise _MatrixFailure("aggregate_result_invalid")
    try:
        return (
            json.dumps(
                aggregate,
                ensure_ascii=True,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )
    except (TypeError, ValueError) as exc:
        raise _MatrixFailure("aggregate_render_failed") from exc


def evaluate_prelaunch_gate_matrix(adapter: PrelaunchGateAdapter) -> bytes:
    """Evaluate the immutable gate registry once without entering a child path."""

    rows: list[dict[str, object]] = []
    results: dict[str, str] = {}
    payloads: dict[str, object] = {}
    for spec in GATE_REGISTRY:
        if any(results.get(dependency) != "passed" for dependency in spec.dependencies):
            row = _gate_row(spec, "blocked", "dependency_not_passed")
        elif spec.method_name is None:
            row = _gate_row(spec, "passed", "all_prelaunch_gates_exact")
        else:
            method = getattr(adapter, spec.method_name)
            try:
                payload = method(*_probe_arguments(spec.gate_id, payloads))
            except _BoundaryViolation:
                raise
            except _ProbeRejected:
                row = _gate_row(spec, "failed", str(spec.ordinary_reason))
            except _ProbeUnknown as exc:
                row = _gate_row(spec, "unknown_failed_closed", exc.reason_code)
            except Exception:
                row = _gate_row(
                    spec,
                    "unknown_failed_closed",
                    "probe_unavailable_or_ambiguous",
                )
            else:
                payloads[spec.gate_id] = payload
                row = _gate_row(spec, "passed", "exact")
        rows.append(row)
        results[spec.gate_id] = str(row["result"])
    aggregate = {
        "schema_version": SCHEMA_VERSION,
        "aggregate_result": _derive_aggregate_result(rows),
        "minimum_lifecycle_state": MINIMUM_COMPLETE_STATE,
        "gates": rows,
    }
    return _render_aggregate(aggregate)


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


def _stable_bytes(path: Path) -> bytes:
    try:
        before = path.lstat()
        if not _ordinary_nonreparse(before):
            raise _MatrixFailure("binding_invalid")
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            payload = stream.read()
            after_read = os.fstat(stream.fileno())
        after = path.lstat()
    except _MatrixFailure:
        raise
    except OSError as exc:
        raise _MatrixFailure("binding_invalid") from exc
    expected = _identity_tuple(before)
    if any(_identity_tuple(item) != expected for item in (opened, after_read, after)):
        raise _MatrixFailure("binding_invalid")
    return payload


def _matrix_repository_root() -> Path:
    module_path = Path(__file__).absolute()
    root = module_path.parent.parent
    if module_path != root / MATRIX_PATH:
        raise _MatrixFailure("binding_invalid")
    try:
        info = root.lstat()
    except OSError as exc:
        raise _MatrixFailure("binding_invalid") from exc
    if not _ordinary_nonreparse(info, directory=True):
        raise _MatrixFailure("binding_invalid")
    return root


def _load_bound_observer() -> ModuleType:
    repository_root = _matrix_repository_root()
    verified: dict[Path, bytes] = {}
    for relative_path, expected_sha256 in FROZEN_BINDINGS.items():
        payload = _stable_bytes(repository_root / relative_path)
        if hashlib.sha256(payload).hexdigest() != expected_sha256:
            raise _MatrixFailure("binding_invalid")
        verified[relative_path] = payload
    module_name = "_r0_prelaunch_gate_matrix_observer"
    module = ModuleType(module_name)
    module.__file__ = os.fspath(repository_root / OBSERVER_PATH)
    module.__package__ = ""
    module.__spec__ = None
    sys.modules[module_name] = module
    try:
        code = compile(
            verified[OBSERVER_PATH],
            module.__file__,
            "exec",
            dont_inherit=True,
        )
        exec(code, module.__dict__)
    except BaseException as exc:
        sys.modules.pop(module_name, None)
        raise _MatrixFailure("binding_invalid") from exc
    required = (
        "_AuditCounter",
        "_SafetyEffect",
        "_ObserverError",
        "_FileIdentity",
        "_LauncherBinding",
        "_repository_root",
        "_load_owner_api",
        "_installed_root",
        "_owned_state_snapshot",
        "_fixed_environment",
        "_kernel32",
        "_windows_directory",
        "_stable_file_identity",
        "_open_launcher_guard",
        "FIXED_LAUNCHER_TOKEN",
        "FIXED_VERSION_TOKEN",
        "FIXED_NO_BYTECODE_TOKEN",
        "FIXED_CHILD_SCRIPT",
        "TIMEOUT_SECONDS",
    )
    if any(not hasattr(module, name) for name in required):
        raise _MatrixFailure("binding_invalid")
    return module


def _observer_status(exc: BaseException) -> str | None:
    status = getattr(exc, "status", None)
    return status if type(status) is str else None


class _ProductionPrelaunchGateAdapter:
    def __init__(self) -> None:
        self._observer = _load_bound_observer()
        self._audit: object | None = None

    def _translate(self, exc: BaseException) -> None:
        if isinstance(exc, self._observer._SafetyEffect):
            raise _BoundaryViolation("operation_boundary_violated") from None
        if isinstance(exc, self._observer._ObserverError):
            if _observer_status(exc) in {
                "observation_binding_rejected",
                "observation_host_rejected",
                "observation_sequence_rejected",
            }:
                raise _ProbeRejected from None
        raise _ProbeUnknown from None

    def probe_runtime_bytecode(self) -> object:
        if (os.name, sys.platform) != ("nt", "win32") or not sys.dont_write_bytecode:
            raise _ProbeRejected
        return True

    def probe_repository_root(self) -> object:
        try:
            return self._observer._repository_root()
        except BaseException as exc:
            self._translate(exc)

    def probe_frozen_owner_api(self, repository_root: object) -> object:
        if not isinstance(repository_root, Path):
            raise _ProbeRejected
        try:
            return self._observer._load_owner_api(repository_root)
        except BaseException as exc:
            self._translate(exc)

    def probe_installed_release_state(
        self,
        repository_root: object,
        owner_api: object,
    ) -> object:
        if not isinstance(repository_root, Path) or not isinstance(owner_api, ModuleType):
            raise _ProbeRejected
        if self._audit is not None:
            raise _ProbeUnknown
        try:
            audit = self._observer._AuditCounter(repository_root)
            registration_observed = False

            def registered_audit(event: str, args: tuple[object, ...]) -> None:
                nonlocal registration_observed
                if event == _AUDIT_REGISTRATION_EVENT:
                    registration_observed = True
                    return
                audit(event, args)

            sys.addaudithook(registered_audit)
            sys.audit(_AUDIT_REGISTRATION_EVENT)
            if not registration_observed:
                raise _ProbeUnknown
            self._audit = audit
            installed_root = self._observer._installed_root(owner_api, repository_root)
            audit.bind_installed_root(installed_root)
            return installed_root
        except _ProbeUnknown:
            raise
        except BaseException as exc:
            self._translate(exc)

    def probe_prelaunch_effect_snapshot(
        self,
        repository_root: object,
        owner_api: object,
        installed_root: object,
    ) -> object:
        if (
            not isinstance(repository_root, Path)
            or not isinstance(owner_api, ModuleType)
            or not isinstance(installed_root, Path)
            or self._audit is None
        ):
            raise _ProbeRejected
        try:
            snapshot = self._observer._owned_state_snapshot(
                owner_api,
                repository_root,
                installed_root,
            )
            if snapshot.exact is not True:
                raise _ProbeRejected
            return snapshot
        except _ProbeRejected:
            raise
        except BaseException as exc:
            self._translate(exc)

    def probe_fixed_launcher_identity(self) -> object:
        try:
            kernel32 = self._observer._kernel32()
            windows_directory = self._observer._windows_directory(kernel32)
            path = Path(windows_directory) / "py.exe"
            first = self._observer._stable_file_identity(path)
            second = self._observer._stable_file_identity(path)
            exact = first == second and path.name.lower() == "py.exe"
            if not exact:
                raise _ProbeRejected
            return self._observer._LauncherBinding(
                True,
                os.fspath(path),
                windows_directory,
                first,
            )
        except _ProbeRejected:
            raise
        except BaseException as exc:
            self._translate(exc)

    def probe_fixed_request_prerequisites(
        self,
        repository_root: object,
        owner_api: object,
        launcher: object,
    ) -> object:
        try:
            exact = (
                isinstance(repository_root, Path)
                and isinstance(owner_api, ModuleType)
                and isinstance(launcher, self._observer._LauncherBinding)
                and launcher.exact is True
                and launcher.identity is not None
                and self._observer.FIXED_LAUNCHER_TOKEN == "py"
                and self._observer.FIXED_VERSION_TOKEN == "-3.13"
                and self._observer.FIXED_NO_BYTECODE_TOKEN == "-B"
                and self._observer.FIXED_CHILD_SCRIPT
                == "tools/check_role_pool_r0_offline_observation.py"
                and self._observer.TIMEOUT_SECONDS == 120.0
                and type(owner_api.MAX_STDOUT_BYTES) is int
                and owner_api.MAX_STDOUT_BYTES == 4096
                and type(owner_api.MAX_FAILURE_STDERR_BYTES) is int
                and owner_api.MAX_FAILURE_STDERR_BYTES == 128
                and self._observer._fixed_environment(launcher.windows_directory)
                == (
                    ("PYTHONDONTWRITEBYTECODE", "1"),
                    ("SYSTEMROOT", launcher.windows_directory),
                )
                and repository_root == self._observer._repository_root()
            )
        except BaseException as exc:
            self._translate(exc)
        if not exact:
            raise _ProbeRejected
        return True

    def probe_launcher_guard_revalidation(self, launcher: object) -> object:
        if not isinstance(launcher, self._observer._LauncherBinding):
            raise _ProbeRejected
        guard = None
        failure: BaseException | None = None
        try:
            kernel32 = self._observer._kernel32()
            guard = self._observer._open_launcher_guard(
                kernel32,
                Path(launcher.application_path),
            )
            if self._observer._stable_file_identity(
                Path(launcher.application_path)
            ) != launcher.identity:
                failure = _ProbeRejected()
        except BaseException as exc:
            failure = exc
        close_exact = True
        if guard is not None:
            try:
                close_exact = guard.close() is True and guard.attempt_count == 1
            except BaseException:
                close_exact = False
        if not close_exact:
            raise _ProbeUnknown("cleanup_unconfirmed")
        if failure is not None:
            if isinstance(failure, _ProbeRejected):
                raise failure
            self._translate(failure)
        return True


def _write_exact(stream: object, payload: bytes) -> None:
    binary = getattr(stream, "buffer", None)
    if binary is None:
        stream.write(payload.decode("utf-8"))
    else:
        binary.write(payload)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        _write_exact(sys.stderr, FAILURE_LINE)
        return 2
    try:
        payload = evaluate_prelaunch_gate_matrix(_ProductionPrelaunchGateAdapter())
    except BaseException:
        _write_exact(sys.stderr, FAILURE_LINE)
        return 2
    _write_exact(sys.stdout, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
