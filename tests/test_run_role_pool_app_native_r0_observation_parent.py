from __future__ import annotations

import ast
import base64
import hashlib
import importlib.util
import inspect
import io
import json
import stat
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "run_role_pool_app_native_r0_observation_parent.py"
SPEC = importlib.util.spec_from_file_location("r0_app_native_parent", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
parent = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = parent
SPEC.loader.exec_module(parent)

OBSERVATION_ID = "r0.app_native.offline.observation.1." + "1" * 32
RECEIPT = b'{"receipt":"synthetic"}\n'
PRIVATE_MARKER = "private-synthetic-marker"
LAUNCH_CLOSE_NAMES = (
    "stdin_read",
    "stdin_write",
    "stdout_read",
    "stdout_write",
    "stderr_read",
    "stderr_write",
    "job",
    "completion_port",
    "process",
    "thread",
    "attribute_list",
)
CLOSE_NAMES = LAUNCH_CLOSE_NAMES + ("checker_guard", "controller_image_guard")


@dataclass(frozen=True)
class FakePostExitFacts:
    top_level_process_count: int
    descendant_process_count: int
    process_relationships_known: bool
    process_terminal_states_known: bool
    surviving_process_count: int
    top_level_identity_exact: bool | None
    timed_out: bool
    termination_uncertain: bool
    cleanup_confirmed: bool
    output_complete: bool
    executor_network_operation_count: int
    repository_write_count: int
    installed_write_count: int
    external_effect_count: int
    generated_residue_count: int


class FakeOwner:
    PostExitFacts = FakePostExitFacts

    def __init__(self) -> None:
        self.parse_calls = 0
        self.seal_calls = 0
        self.facts: FakePostExitFacts | None = None

    @staticmethod
    def observation_identity_pair(value: str) -> tuple[str, str]:
        parent._validate_observation_id(value)
        return value.replace("observation.1", "sequence.1"), value

    def parse_validation_payload(self, payload: bytes) -> dict[str, object]:
        self.parse_calls += 1
        if payload != b"valid":
            raise ValueError
        return {"valid": True}

    def seal_proportionate_observation_receipt(
        self,
        payload: bytes,
        facts: FakePostExitFacts,
        observation_id: str,
    ) -> bytes:
        self.seal_calls += 1
        self.facts = facts
        assert payload == b"valid"
        assert observation_id == OBSERVATION_ID
        return RECEIPT


def close_observations(**changes: bool) -> tuple[object, ...]:
    return tuple(
        parent._CloseObservation(name, 1, changes.get(name, True))
        for name in LAUNCH_CLOSE_NAMES
    )


def launch_evidence(**changes: object) -> object:
    values: dict[str, object] = {
        "creation_attempt_count": 1,
        "top_level_created": True,
        "top_level_process_id": 41,
        "job_assigned_at_creation": True,
        "job_handle_unique": True,
        "events": (
            parent._JobEvent("new", 41),
            parent._JobEvent("exit", 41),
            parent._JobEvent("active_zero", None),
        ),
        "cumulative_process_total": 1,
        "active_process_count": 0,
        "exit_code": 0,
        "stdout": b"valid",
        "stderr": b"",
        "stdout_eof": True,
        "stderr_eof": True,
        "stdout_overflow": False,
        "stderr_overflow": False,
        "top_level_identity_exact": True,
        "target_identity_exact": True,
        "timed_out": False,
        "termination_requested": False,
        "termination_succeeded": None,
        "terminal_wait_succeeded": True,
        "close_observations": close_observations(),
    }
    values.update(changes)
    return parent._LaunchEvidence(**values)


class FakeAdapter:
    def __init__(self) -> None:
        self.os_name = "nt"
        self.platform = "win32"
        self.calls: list[str] = []
        self.before = parent._EffectSnapshot(True, "repo", "installed", frozenset())
        self.after = self.before
        self.counts = parent._AuditCounts(0, 0, 0, 0)
        self.evidence = launch_evidence()
        self.target_exact: bool | None = True
        self.launch_error: BaseException | None = None
        self.request: object | None = None
        self.launch_path: bytes | None = None
        self.clear_count = 0
        self.checker_exact: bool | None = True
        self.checker_close_succeeded = True
        self.checker_guard_owned = False
        self.controller_guard_owned = False
        self.image_close_results = {
            "controller_image_guard": True,
        }
        self.image_exact: bool | None = True
        self.development_failure: str | None = None
        self._development_private_path: bytearray | None = None
        self.identity = parent._FileIdentity(
            1,
            2,
            105696,
            4,
            "1" * 64,
            "3.13.14",
            "3.13.14",
            "2" * 64,
        )
        self.controller_identity = self.identity

    def runtime_identity(self) -> tuple[str, str]:
        self.calls.append("runtime")
        return self.os_name, self.platform

    def development_child_creation_count(self) -> int:
        return self.calls.count("launch")

    def install_audit(self, repository_root: Path) -> None:
        assert repository_root == ROOT
        self.calls.append("install_audit")
        if self.development_failure == "audit_installed":
            raise RuntimeError("synthetic audit failure")

    def snapshot_effects(self, repository_root: Path) -> object:
        assert repository_root == ROOT
        self.calls.append("snapshot")
        snapshot_number = self.calls.count("snapshot")
        if (
            self.development_failure == "before_effect_snapshot_available"
            and snapshot_number == 1
        ) or (
            self.development_failure == "after_effect_snapshot_available"
            and snapshot_number == 2
        ):
            raise RuntimeError("synthetic snapshot failure")
        return self.before if self.calls.count("snapshot") == 1 else self.after

    def windows_directory(self) -> str:
        self.calls.append("windows_directory")
        return "C:" + chr(92) + "Windows"

    def validate_controller_image(self) -> object:
        self.calls.append("validate_controller_image")
        self.controller_guard_owned = True
        return parent._TargetBinding(
            bytearray(PRIVATE_MARKER.encode("ascii")),
            self.controller_identity,
        )

    def _development_validate_controller_image(self, recorder: object) -> object:
        self.calls.append("development_validate_controller_image")
        for predicate in parent._DEVELOPMENT_IMAGE_PREDICATES:
            if self.development_failure == predicate:
                if parent._DEVELOPMENT_PREDICATES.index(predicate) >= parent._DEVELOPMENT_PREDICATES.index(
                    "controller_image_guard_opened"
                ):
                    self.controller_guard_owned = True
                    self._development_private_path = bytearray(PRIVATE_MARKER.encode("ascii"))
                recorder.failed(
                    predicate,
                    OSError(f"synthetic {predicate}: {PRIVATE_MARKER}"),
                    values={"controller_image_path": PRIVATE_MARKER},
                    win32_last_error=5,
                )
                raise parent._DevelopmentAbort(predicate)
            recorder.passed(predicate, {"controller_image_path": PRIVATE_MARKER})
        return self.validate_controller_image()

    def _development_revalidate_controller_image(
        self,
        target: object,
        recorder: object,
    ) -> None:
        del target
        self.calls.append("development_revalidate_controller_image")
        for predicate in (
            "controller_image_guard_identity_exact",
            "controller_image_path_identity_exact",
        ):
            if self.development_failure == predicate:
                recorder.failed(
                    predicate,
                    OSError(f"synthetic {predicate}: {PRIVATE_MARKER}"),
                    values={"controller_image_path": PRIVATE_MARKER},
                    win32_last_error=5,
                )
                raise parent._DevelopmentAbort(predicate)
            recorder.passed(predicate, {"controller_image_path": PRIVATE_MARKER})

    def clear_private(self, *values: object) -> bool:
        self.calls.append("clear_private")
        self.clear_count += 1
        for value in values:
            if isinstance(value, bytearray):
                value[:] = b"\0" * len(value)
        return True

    def image_binding_exact(self, target: object) -> bool | None:
        del target
        self.calls.append("image_binding_exact")
        return self.image_exact

    def launch_once(self, request: object) -> object:
        self.calls.append("launch")
        self.request = request
        self.launch_path = bytes(request.target.opaque_path)
        self.checker_guard_owned = True
        if self.launch_error is not None:
            raise self.launch_error
        return self.evidence

    def finish_image_guards(self) -> tuple[object, ...]:
        self.calls.append("finish_image_guards")
        observations: list[object] = []
        if self.controller_guard_owned:
            self.controller_guard_owned = False
            observations.append(
                parent._CloseObservation(
                    "controller_image_guard",
                    1,
                    self.image_close_results["controller_image_guard"],
                )
            )
        return tuple(observations)

    def finish_checker_guard(self) -> tuple[bool | None, object | None]:
        self.calls.append("finish_checker_guard")
        if not self.checker_guard_owned:
            return None, None
        self.checker_guard_owned = False
        return (
            self.checker_exact,
            parent._CloseObservation(
                "checker_guard",
                1,
                self.checker_close_succeeded,
            ),
        )

    def target_identity_exact(self, target: object) -> bool | None:
        del target
        self.calls.append("target_recheck")
        return self.target_exact

    def audit_counts(self) -> object:
        self.calls.append("audit_counts")
        if self.development_failure == "audit_counts_available":
            raise RuntimeError("synthetic audit-count failure")
        return self.counts


def run(adapter: FakeAdapter, owner: object | None = None) -> tuple[bytes | str, object]:
    expected = parent._canonical_target_binding(adapter.identity)
    return run_with_expected(adapter, expected, owner)


def run_with_expected(
    adapter: FakeAdapter,
    expected: object,
    owner: object | None = None,
) -> tuple[bytes | str, object]:
    selected_owner = owner or FakeOwner()
    result = parent._run_controller(
        OBSERVATION_ID,
        expected,
        adapter,
        repository_root=ROOT,
        owner=selected_owner,
    )
    return result, selected_owner


def run_metadata(adapter: FakeAdapter) -> bytes | str:
    return parent._run_metadata(adapter, repository_root=ROOT)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_import_is_inert_and_frozen_dependencies_are_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: pytest.fail("adapter constructed"))
    for relative, expected in parent.FROZEN_BINDINGS.items():
        assert sha(ROOT / relative) == expected
    source = MODULE_PATH.read_text(encoding="ascii")
    assert "import run_role_pool_r0_trusted_launch_observer" not in source
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert "subprocess" not in imported


def test_real_owner_interface_loads_from_exact_bytes() -> None:
    owner = parent._load_owner(ROOT)
    assert callable(owner.observation_identity_pair)
    assert callable(owner.parse_validation_payload)
    assert callable(owner.seal_proportionate_observation_receipt)
    assert owner.PostExitFacts.__name__ == "PostExitFacts"


def test_audit_registration_requires_positive_self_witness(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = object.__new__(parent._WindowsParentAdapter)
    adapter.audit = None
    monkeypatch.setattr(parent.sys, "addaudithook", lambda _hook: None)
    monkeypatch.setattr(parent.sys, "audit", lambda _event, *_args: None)

    with pytest.raises(parent._ControllerError, match="observation_binding_rejected"):
        adapter.install_audit(ROOT)

    assert adapter.audit is None


def test_audit_registration_is_stored_only_after_witness(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = object.__new__(parent._WindowsParentAdapter)
    adapter.audit = None
    hooks: list[object] = []

    monkeypatch.setattr(parent.sys, "addaudithook", hooks.append)

    def emit(event: str, *args: object) -> None:
        for hook in tuple(hooks):
            hook(event, args)

    monkeypatch.setattr(parent.sys, "audit", emit)
    adapter.install_audit(ROOT)

    assert isinstance(adapter.audit, parent._AuditCounter)
    assert adapter.audit.snapshot() == parent._AuditCounts(0, 0, 0, 0)


def test_development_snapshot_exposes_exception_while_production_remains_blinded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = object.__new__(parent._WindowsParentAdapter)

    def fail_snapshot(_repository_root: Path, **_kwargs: object) -> object:
        raise OSError(f"synthetic snapshot detail: {PRIVATE_MARKER}")

    monkeypatch.setattr(adapter, "_snapshot_effects_exact", fail_snapshot)

    assert adapter.snapshot_effects(ROOT) == parent._EffectSnapshot(False, "", "", frozenset())
    with pytest.raises(OSError, match=PRIVATE_MARKER):
        adapter._development_snapshot_effects(ROOT)


def test_stable_file_failure_adds_path_only_for_development_context(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing-python.exe"

    with pytest.raises(parent._ControllerError) as production:
        parent._stable_file_bytes(missing)
    assert getattr(production.value, "__notes__", []) == []

    with pytest.raises(parent._ControllerError) as development:
        parent._stable_file_bytes(missing, development_context=True)
    assert getattr(development.value, "__notes__", []) == [
        f"development_path={missing}"
    ]


def test_stable_open_file_identity_ignores_permissions_but_not_file_type() -> None:
    common = {
        "st_dev": 11,
        "st_ino": 22,
        "st_size": 33,
        "st_mtime_ns": 44,
    }
    executable_path_stat = SimpleNamespace(st_mode=stat.S_IFREG | 0o777, **common)
    opened_file_stat = SimpleNamespace(st_mode=stat.S_IFREG | 0o666, **common)
    directory_stat = SimpleNamespace(st_mode=stat.S_IFDIR | 0o777, **common)

    assert parent._stable_open_file_identity_tuple(
        executable_path_stat
    ) == parent._stable_open_file_identity_tuple(opened_file_stat)
    assert parent._stable_open_file_identity_tuple(
        executable_path_stat
    ) != parent._stable_open_file_identity_tuple(directory_stat)


@pytest.mark.parametrize(
    "value",
    [
        None,
        1,
        "",
        "x",
        "-x",
        "r0.app_native.offline.observation.1." + "0" * 32,
        "r0.app_native.offline.observation.2." + "1" * 32,
        "r0.app_native.offline.observation.1." + "A" * 32,
        OBSERVATION_ID + "x",
        OBSERVATION_ID + "\n",
        OBSERVATION_ID[:-1],
        chr(233) + OBSERVATION_ID,
    ],
)
def test_public_identity_rejections(value: object) -> None:
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_observation_id(value)


def test_public_identity_exact_positive() -> None:
    assert parent._validate_observation_id(OBSERVATION_ID) == OBSERVATION_ID


@pytest.mark.parametrize("runtime", [("posix", "linux"), ("nt", "linux"), ("posix", "win32")])
def test_non_windows_fails_before_private_input(runtime: tuple[str, str]) -> None:
    adapter = FakeAdapter()
    adapter.os_name, adapter.platform = runtime
    result, _owner = run(adapter)
    assert result == "observation_host_rejected"
    assert adapter.calls == ["runtime"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("C:" + chr(92) + "Python313" + chr(92) + "python.exe", True),
        ("python.exe", False),
        (chr(92) * 2 + "server" + chr(92) + "python.exe", False),
        ("C:" + chr(92) + "Python313" + chr(92) + "python.exe:stream", False),
        ("C:" + chr(92) + "Python313." + chr(92) + "python.exe", False),
        ("C:" + chr(92) + "Python313 " + chr(92) + "python.exe", False),
        ("C:" + chr(92) + "Python*" + chr(92) + "python.exe", False),
        ("C:" + chr(92) + "Python313" + chr(92) + "py.exe", False),
        (None, False),
    ],
)
def test_private_target_lexical_policy(value: object, expected: bool) -> None:
    assert parent._valid_private_target_text(value) is expected


def test_success_uses_guarded_controller_image_as_the_sole_target() -> None:
    adapter = FakeAdapter()
    result, _owner = run(adapter)
    assert result == RECEIPT
    assert adapter.calls[:8] == [
        "runtime",
        "install_audit",
        "snapshot",
        "validate_controller_image",
        "image_binding_exact",
        "windows_directory",
        "launch",
        "target_recheck",
    ]
    assert cast_request(adapter).target.identity == adapter.controller_identity
    assert adapter.launch_path == PRIVATE_MARKER.encode("ascii")
    assert adapter.calls.count("validate_controller_image") == 1
    assert adapter.calls.count("image_binding_exact") == 1
    assert adapter.clear_count == 1


@pytest.mark.parametrize("image_exact", [False, None])
def test_controller_image_revalidation_rejects_before_launch(
    image_exact: bool | None,
) -> None:
    adapter = FakeAdapter()
    adapter.image_exact = image_exact
    result, _owner = run(adapter)
    assert result == "observation_binding_rejected"
    assert "launch" not in adapter.calls


@pytest.mark.parametrize(
    ("method", "status"),
    [
        ("validate_controller_image", "observation_binding_rejected"),
        ("image_binding_exact", "observation_binding_rejected"),
        ("windows_directory", "observation_binding_rejected"),
    ],
)
def test_sole_image_acquisition_failures_stop_without_process_entry(
    method: str,
    status: str,
) -> None:
    adapter = FakeAdapter()

    def fail(*_args: object, **_kwargs: object) -> object:
        raise parent._ControllerError(status)

    setattr(adapter, method, fail)
    result, _owner = run(adapter)
    assert result == status
    assert "launch" not in adapter.calls


def test_controller_path_clear_failure_after_launch_is_cleanup_unknown() -> None:
    adapter = FakeAdapter()

    def fail_clear(*_values: object) -> bool:
        adapter.calls.append("clear_private")
        return False

    adapter.clear_private = fail_clear
    result, _owner = run(adapter)
    assert result == "observation_timeout_unknown"
    assert adapter.calls.count("launch") == 1


def test_private_value_never_enters_request_result_or_exception() -> None:
    adapter = FakeAdapter()
    result, _owner = run(adapter)
    assert PRIVATE_MARKER.encode() not in result
    assert PRIVATE_MARKER not in repr(adapter.request)
    assert PRIVATE_MARKER not in " ".join(cast_request(adapter).tokens)
    assert all(PRIVATE_MARKER not in item for item in adapter.calls)


def test_launch_helper_borrows_the_exact_sole_controller_path() -> None:
    launch_source = inspect.getsource(parent._WindowsParentAdapter.launch_once)
    execute_source = inspect.getsource(parent._execute_windows_once)
    assert "path = bytes(cast(bytearray, request.target.opaque_path)).decode(\"utf-16-le\")" in launch_source
    assert "path,\n            self.kernel32,\n            self.controller_guard" in launch_source
    assert "kernel32.CreateProcessW(\n                private_path," in execute_source


@pytest.mark.parametrize("identity", [True, False, None])
def test_process_image_identity_retains_existing_three_variant_semantics(
    identity: bool | None,
) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(top_level_identity_exact=identity)
    result, owner = run(adapter)
    assert result == RECEIPT
    assert owner.facts.top_level_identity_exact is identity


@pytest.mark.parametrize("target_exact", [False, None])
def test_post_launch_target_file_drift_is_launch_unknown(target_exact: bool | None) -> None:
    adapter = FakeAdapter()
    adapter.target_exact = target_exact
    result, owner = run(adapter)
    assert result == "observation_launch_unknown"
    assert owner.seal_calls == 0
    assert adapter.clear_count == 1


@pytest.mark.parametrize("observed", [False, None])
def test_precreate_target_identity_uncertainty_rejects_before_entry(
    observed: bool | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity = parent._FileIdentity(1, 2, 3, 4, "a" * 64, "3.13", "3.13")
    monkeypatch.setattr(parent, "_path_identity_exact", lambda _path, _identity: observed)

    with pytest.raises(parent._ControllerError, match="observation_binding_rejected"):
        parent._require_precreate_target_identity(PRIVATE_MARKER, identity)


def test_precreate_target_identity_check_is_immediately_before_create_process() -> None:
    source = inspect.getsource(parent._execute_windows_once)
    binding = source.index("_require_precreate_target_identity")
    deadline = source.index("deadline = time.monotonic()")
    uncertain = source.index("created = None")
    attempt = source.index("attempts = 1")
    create = source.index("kernel32.CreateProcessW")
    assert binding < deadline < uncertain < attempt < create


def test_controller_guard_is_closed_when_identity_capture_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.close_calls = 0

        @staticmethod
        def CreateFileW(*_args: object) -> int:
            return 41

        def CloseHandle(self, _handle: object) -> bool:
            self.close_calls += 1
            return True

    target = tmp_path / "python.exe"
    target.write_bytes(b"synthetic")
    adapter = object.__new__(parent._WindowsParentAdapter)
    adapter.kernel32 = Kernel()
    monkeypatch.setattr(
        parent,
        "_stable_file_bytes",
        lambda _path: (_ for _ in ()).throw(parent._ControllerError("observation_binding_rejected")),
    )

    with pytest.raises(parent._ControllerError, match="observation_binding_rejected"):
        adapter._open_executable_binding(str(target), "controller_image_guard")

    assert adapter.kernel32.close_calls == 1


def test_checker_guard_binds_exact_bytes_and_denies_write_delete_sharing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.create_args: tuple[object, ...] | None = None
            self.close_calls = 0

        def CreateFileW(self, *args: object) -> int:
            self.create_args = args
            return 51

        def CloseHandle(self, _handle: object) -> bool:
            self.close_calls += 1
            return True

    payload = b"synthetic checker"
    checker = tmp_path / parent.OWNER_PATH
    checker.parent.mkdir(parents=True)
    checker.write_bytes(payload)
    monkeypatch.setitem(
        parent.FROZEN_BINDINGS,
        parent.OWNER_PATH,
        hashlib.sha256(payload).hexdigest(),
    )
    kernel = Kernel()

    guard = parent._open_checker_guard(tmp_path, kernel)
    identity = parent._checker_file_identity(checker)

    assert guard.open
    assert identity[-1] == hashlib.sha256(payload).hexdigest()
    assert kernel.create_args is not None
    assert kernel.create_args[0] == str(checker)
    assert kernel.create_args[2] == parent.FILE_SHARE_READ
    assert guard.close()
    assert kernel.close_calls == 1


@pytest.mark.parametrize(
    ("controller_close_succeeds", "expected_status"),
    [
        (True, "observation_binding_rejected"),
        (False, "observation_timeout_unknown"),
    ],
)
def test_checker_preentry_failure_closes_checker_then_controller_guard(
    monkeypatch: pytest.MonkeyPatch,
    controller_close_succeeds: bool,
    expected_status: str,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.closed: list[int] = []

        def CloseHandle(self, handle: object) -> bool:
            value = int(getattr(handle, "value", 0) or 0)
            self.closed.append(value)
            return value != 11 or controller_close_succeeds

    kernel = Kernel()
    adapter = object.__new__(parent._WindowsParentAdapter)
    adapter.kernel32 = kernel
    adapter.launch_calls = 0
    adapter.controller_guard = parent._OwnedHandle(kernel, "controller_image_guard", 11)
    adapter.checker_guard = None
    adapter.checker_identity = None
    adapter.checker_repository_root = None
    adapter.last_target_exact = None
    adapter.windows_directory = lambda: "C:" + chr(92) + "Windows"
    monkeypatch.setattr(
        parent,
        "_open_checker_guard",
        lambda _root, _kernel: parent._OwnedHandle(kernel, "checker_guard", 22),
    )
    monkeypatch.setattr(
        parent,
        "_checker_file_identity",
        lambda _path: (_ for _ in ()).throw(
            parent._ControllerError("observation_binding_rejected")
        ),
    )
    monkeypatch.setattr(parent, "_handle_stable_identity", lambda *_args: "0" * 64)
    target = parent._TargetBinding(
        bytearray(),
        parent._FileIdentity(1, 2, 3, 4, "a" * 64, "3.13", "3.13"),
    )
    request = parent._LaunchRequest(
        target,
        ("python.exe", "-B", parent.FIXED_CHILD_SCRIPT, OBSERVATION_ID),
        ROOT,
        (("PYTHONDONTWRITEBYTECODE", "1"), ("SYSTEMROOT", "C:" + chr(92) + "Windows")),
        parent.TIMEOUT_SECONDS,
        parent.MAX_STDOUT_BYTES,
        parent.MAX_STDERR_BYTES,
    )

    with pytest.raises(parent._ControllerError, match=expected_status):
        adapter.launch_once(request)

    assert kernel.closed == [22, 11]
    assert adapter.checker_guard is None
    assert not adapter.controller_guard.open


def test_attribute_list_is_owned_only_after_successful_initialization() -> None:
    class Kernel:
        def __init__(self) -> None:
            self.initialize_calls = 0
            self.delete_calls = 0

        def InitializeProcThreadAttributeList(
            self,
            _pointer: object,
            _count: int,
            _flags: int,
            size: object,
        ) -> bool:
            self.initialize_calls += 1
            parent.ctypes.cast(size, parent.ctypes.POINTER(parent.ctypes.c_size_t)).contents.value = 64
            return self.initialize_calls == 1

        def DeleteProcThreadAttributeList(self, _pointer: object) -> None:
            self.delete_calls += 1

    kernel = Kernel()
    attributes = parent._OwnedAttributeList(kernel)

    with pytest.raises(parent._ControllerError, match="observation_launch_unknown"):
        attributes.initialize()

    assert attributes.pointer is None
    assert attributes.buffer is None
    assert attributes.close()
    assert attributes.observation() == parent._CloseObservation("attribute_list", 1, True)
    assert kernel.delete_calls == 0


def test_uncertain_process_return_adopts_owned_handles_for_reconciliation() -> None:
    class Kernel:
        @staticmethod
        def CloseHandle(_handle: object) -> bool:
            return True

    information = parent._ProcessInformation()
    information.hProcess = 41
    information.hThread = 42
    handles: dict[str, object] = {}

    assert parent._adopt_returned_process_handles(Kernel(), handles, information)
    assert tuple(handles) == ("process", "thread")
    assert all(handle.open for handle in handles.values())


def test_process_entry_uncertainty_routes_through_reconciliation() -> None:
    source = inspect.getsource(parent._execute_windows_once)
    exception = source.index("except BaseException as exc:")
    uncertain = source.index("attempts == 1 and created is not False", exception)
    adoption = source.index("_adopt_returned_process_handles", uncertain)
    release = source.index("attributes.close()", adoption)
    inherited_closes = source.index('("stdin_read", "stdout_write", "stderr_write", "thread")', release)
    recovery = source.index("_recover_postcreation_failure(", inherited_closes)
    cleanup = source.index("finally:", recovery)
    assert exception < uncertain < adoption < release < inherited_closes < recovery < cleanup


def cast_request(adapter: FakeAdapter) -> object:
    assert isinstance(adapter.request, parent._LaunchRequest)
    return adapter.request


def test_exact_child_request_has_no_shell_path_or_ambient_environment() -> None:
    adapter = FakeAdapter()
    result, _owner = run(adapter)
    assert result == RECEIPT
    request = cast_request(adapter)
    assert request.tokens == ("python.exe", "-B", parent.FIXED_CHILD_SCRIPT, OBSERVATION_ID)
    assert request.environment == (("PYTHONDONTWRITEBYTECODE", "1"), ("SYSTEMROOT", "C:" + chr(92) + "Windows"))
    assert {name.upper() for name, _value in request.environment} == {"PYTHONDONTWRITEBYTECODE", "SYSTEMROOT"}
    assert request.timeout_seconds == 120
    assert request.max_stdout_bytes == 4096
    assert request.max_stderr_bytes == 128


def test_production_source_encodes_creation_time_job_and_handle_lists_only() -> None:
    source = MODULE_PATH.read_text(encoding="ascii")
    assert "PROC_THREAD_ATTRIBUTE_JOB_LIST" in source
    assert "PROC_THREAD_ATTRIBUTE_HANDLE_LIST" in source
    assert "ActiveProcessLimit = 1" in source
    assert "JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE" in source
    assert "CREATE_SUSPENDED" not in source
    assert "AssignProcessToJobObject" not in source


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("x"),
        KeyboardInterrupt(),
        parent._ControllerError("observation_launch_unknown"),
    ],
)
def test_launch_exception_never_retries(error: BaseException) -> None:
    adapter = FakeAdapter()
    adapter.launch_error = error
    result, _owner = run(adapter)
    assert result in {"observation_launch_unknown", "observation_result_unknown"}
    assert adapter.calls.count("launch") == 1


def test_checker_guard_close_failure_overrides_preentry_binding_rejection() -> None:
    adapter = FakeAdapter()
    adapter.launch_error = parent._ControllerError("observation_binding_rejected")
    adapter.checker_close_succeeded = False

    result, _owner = run(adapter)

    assert result == "observation_timeout_unknown"
    assert adapter.calls.count("launch") == 1
    assert adapter.calls.count("finish_checker_guard") == 1


@pytest.mark.parametrize(
    "changes",
    [
        {"creation_attempt_count": 0},
        {"creation_attempt_count": 2},
        {"top_level_created": False},
        {"top_level_process_id": None},
        {"job_assigned_at_creation": False},
        {"job_handle_unique": False},
        {"cumulative_process_total": None},
        {"cumulative_process_total": 2},
        {"active_process_count": None},
        {"events": (parent._JobEvent("unknown", None),)},
        {"events": (parent._JobEvent("new", 41), parent._JobEvent("active_zero", None))},
        {"events": (parent._JobEvent("new", 42), parent._JobEvent("exit", 42), parent._JobEvent("active_zero", None))},
    ],
)
def test_job_membership_accounting_and_event_conflicts_are_launch_unknown(changes: dict[str, object]) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(**changes)
    result, _owner = run(adapter)
    assert result == "observation_launch_unknown"


def test_descendant_and_survivor_are_safety_failures() -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(
        cumulative_process_total=2,
        events=(
            parent._JobEvent("new", 41),
            parent._JobEvent("new", 42),
            parent._JobEvent("exit", 41),
            parent._JobEvent("exit", 42),
            parent._JobEvent("active_zero", None),
        ),
    )
    result, _owner = run(adapter)
    assert result == "observation_safety_boundary_failed"
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(active_process_count=1)
    result, _owner = run(adapter)
    assert result == "observation_launch_unknown"


def test_active_process_limit_message_is_known_safety_failure() -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(
        events=(
            parent._JobEvent("new", 41),
            parent._JobEvent("exit", 41),
            parent._JobEvent("active_limit", None),
            parent._JobEvent("active_zero", None),
        )
    )
    result, _owner = run(adapter)
    assert result == "observation_safety_boundary_failed"


@pytest.mark.parametrize(
    "changes",
    [
        {"timed_out": True, "termination_requested": True, "termination_succeeded": True},
        {"termination_requested": True, "termination_succeeded": False},
        {"terminal_wait_succeeded": False},
        {"exit_code": None},
        {"close_observations": close_observations(process=False)},
    ],
)
def test_timeout_termination_terminal_and_cleanup_unknown_precedence(changes: dict[str, object]) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(**changes)
    result, _owner = run(adapter)
    assert result == "observation_timeout_unknown"


@pytest.mark.parametrize("resource", CLOSE_NAMES)
def test_every_owned_resource_requires_one_successful_close(resource: str) -> None:
    adapter = FakeAdapter()
    if resource == "checker_guard":
        adapter.checker_close_succeeded = False
    elif resource == "controller_image_guard":
        adapter.image_close_results["controller_image_guard"] = False
    else:
        adapter.evidence = launch_evidence(
            close_observations=close_observations(**{resource: False})
        )
    result, _owner = run(adapter)
    assert result == "observation_timeout_unknown"


@pytest.mark.parametrize("checker_exact", [False, None])
def test_checker_guard_drift_after_post_inventory_fails_closed(
    checker_exact: bool | None,
) -> None:
    adapter = FakeAdapter()
    adapter.checker_exact = checker_exact

    result, owner = run(adapter)

    assert result == "observation_launch_unknown"
    assert owner.seal_calls == 0
    assert adapter.calls.index("snapshot", 3) < adapter.calls.index("finish_checker_guard")
    assert adapter.calls.index("audit_counts") < adapter.calls.index("finish_checker_guard")


@pytest.mark.parametrize(
    "observations",
    [
        (parent._CloseObservation("job", 1, True),),
        close_observations()[:-1],
        close_observations() + (parent._CloseObservation("foreign", 1, True),),
    ],
)
def test_cleanup_inventory_requires_the_exact_closed_resource_set(
    observations: tuple[object, ...],
) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(close_observations=observations)
    result, _owner = run(adapter)
    assert result == "observation_timeout_unknown"


@pytest.mark.parametrize(
    "field",
    ["network_operations", "repository_writes", "installed_writes", "external_effects"],
)
def test_each_observed_effect_is_safety_failure(field: str) -> None:
    adapter = FakeAdapter()
    adapter.counts = replace(adapter.counts, **{field: 1})
    result, _owner = run(adapter)
    assert result == "observation_safety_boundary_failed"


@pytest.mark.parametrize("which", ["repository", "installed", "residue"])
def test_pre_post_drift_and_residue_are_safety_failures(which: str) -> None:
    adapter = FakeAdapter()
    if which == "repository":
        adapter.after = replace(adapter.after, repository_digest="changed")
    elif which == "installed":
        adapter.after = replace(adapter.after, installed_digest="changed")
    else:
        adapter.after = replace(adapter.after, generated_residue=frozenset({"new"}))
    result, _owner = run(adapter)
    assert result == "observation_safety_boundary_failed"


def test_repository_tree_digest_covers_every_working_tree_path_except_git_metadata(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / ".git").mkdir()
    (repository / ".git" / "index").write_bytes(b"metadata-one")
    (repository / "owned.txt").write_bytes(b"owned")
    first = parent._tree_digest(
        repository,
        excluded_root_names=parent._REPOSITORY_METADATA_NAMES,
        schema_version="trusted_owner_repository_working_tree.v1",
    )

    (repository / ".git" / "index").write_bytes(b"metadata-two")
    assert parent._tree_digest(
        repository,
        excluded_root_names=parent._REPOSITORY_METADATA_NAMES,
        schema_version="trusted_owner_repository_working_tree.v1",
    ) == first

    (repository / "foreign-output.txt").write_bytes(b"unexpected")
    assert parent._tree_digest(
        repository,
        excluded_root_names=parent._REPOSITORY_METADATA_NAMES,
        schema_version="trusted_owner_repository_working_tree.v1",
    ) != first


def test_unstable_effect_snapshot_is_cleanup_unknown() -> None:
    adapter = FakeAdapter()
    adapter.after = replace(adapter.after, exact=False)
    result, _owner = run(adapter)
    assert result == "observation_timeout_unknown"


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"stdout_eof": False}, "observation_timeout_unknown"),
        ({"stderr_eof": False}, "observation_timeout_unknown"),
        ({"stdout_overflow": True}, "observation_result_unknown"),
        ({"stderr_overflow": True}, "observation_result_unknown"),
    ],
)
def test_stream_eof_overflow_and_drain_fail_closed(
    changes: dict[str, object],
    expected: str,
) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(**changes)
    result, _owner = run(adapter)
    assert result == expected


def test_pipe_drain_continues_to_eof_after_overflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class PipeKernel:
        def __init__(self) -> None:
            self.peek_calls = 0
            self.read_calls = 0
            self.read_sizes: list[int] = []

        def PeekNamedPipe(
            self,
            _handle: object,
            _buffer: object,
            _size: int,
            _read: object,
            available: object,
            _left: object,
        ) -> bool:
            self.peek_calls += 1
            if self.peek_calls == 1:
                parent.ctypes.cast(available, parent.ctypes.POINTER(parent.wintypes.DWORD)).contents.value = 3
                return True
            return False

        def ReadFile(self, _handle: object, buffer: object, size: int, read: object, _overlapped: object) -> bool:
            self.read_calls += 1
            self.read_sizes.append(size)
            parent.ctypes.memmove(buffer, b"x" * size, size)
            parent.ctypes.cast(read, parent.ctypes.POINTER(parent.wintypes.DWORD)).contents.value = size
            return True

    kernel = PipeKernel()
    retained = bytearray(b"full")
    handle = parent._OwnedHandle(kernel, "stdout_read", 1)
    monkeypatch.setattr(parent.ctypes, "get_last_error", lambda: parent.ERROR_BROKEN_PIPE)

    first = parent._drain_pipe(
        kernel,
        handle,
        retained,
        4,
        False,
        True,
        float("inf"),
    )
    second = parent._drain_pipe(
        kernel,
        handle,
        retained,
        4,
        first[0],
        first[1],
        float("inf"),
    )

    assert first == (False, True, True)
    assert second == (True, True, True)
    assert retained == b"full"
    assert kernel.read_calls == 1
    assert kernel.read_sizes == [1]


@pytest.mark.parametrize(
    ("resource", "limit"),
    [("stdout_read", parent.MAX_STDOUT_BYTES), ("stderr_read", parent.MAX_STDERR_BYTES)],
)
def test_continuously_available_pipe_performs_one_bounded_read_per_cycle(
    resource: str,
    limit: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.peek_calls = 0
            self.read_sizes: list[int] = []

        def PeekNamedPipe(
            self,
            _handle: object,
            _buffer: object,
            _size: int,
            _read: object,
            available: object,
            _left: object,
        ) -> bool:
            self.peek_calls += 1
            parent.ctypes.cast(
                available,
                parent.ctypes.POINTER(parent.wintypes.DWORD),
            ).contents.value = 65536
            return True

        def ReadFile(
            self,
            _handle: object,
            buffer: object,
            size: int,
            read: object,
            _overlapped: object,
        ) -> bool:
            self.read_sizes.append(size)
            parent.ctypes.memset(buffer, ord("x"), size)
            parent.ctypes.cast(
                read,
                parent.ctypes.POINTER(parent.wintypes.DWORD),
            ).contents.value = size
            return True

    kernel = Kernel()
    monkeypatch.setattr(parent.time, "monotonic", lambda: 0.0)

    result = parent._drain_pipe(
        kernel,
        parent._OwnedHandle(kernel, resource, 1),
        bytearray(),
        limit,
        False,
        False,
        1.0,
    )

    assert result == (False, True, True)
    assert kernel.peek_calls == 1
    assert kernel.read_sizes == [limit + 1]


def test_completion_port_service_cycle_is_bounded_to_32_packets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.calls = 0

        def GetQueuedCompletionStatus(
            self,
            _port: object,
            message: object,
            _key: object,
            overlapped: object,
            _timeout: int,
        ) -> bool:
            self.calls += 1
            parent.ctypes.cast(
                message,
                parent.ctypes.POINTER(parent.wintypes.DWORD),
            ).contents.value = parent.JOB_OBJECT_MSG_NEW_PROCESS
            parent.ctypes.cast(
                overlapped,
                parent.ctypes.POINTER(parent.wintypes.LPVOID),
            ).contents.value = self.calls
            return True

    kernel = Kernel()
    events: list[object] = []
    monkeypatch.setattr(parent.time, "monotonic", lambda: 0.0)

    assert parent._drain_job_events(
        kernel,
        parent._OwnedHandle(kernel, "completion_port", 1),
        events,
        1.0,
    ) == (True, False)
    assert kernel.calls == parent.MAX_COMPLETION_EVENTS_PER_CYCLE
    assert len(events) == parent.MAX_COMPLETION_EVENTS_PER_CYCLE


def test_completion_port_requires_observed_empty_after_33rd_conflicting_packet(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.calls = 0

        def GetQueuedCompletionStatus(
            self,
            _port: object,
            message: object,
            _key: object,
            overlapped: object,
            _timeout: int,
        ) -> bool:
            self.calls += 1
            if self.calls == 34:
                return False
            value = (
                parent.JOB_OBJECT_MSG_ACTIVE_PROCESS_LIMIT
                if self.calls == 33
                else parent.JOB_OBJECT_MSG_NEW_PROCESS
            )
            parent.ctypes.cast(
                message,
                parent.ctypes.POINTER(parent.wintypes.DWORD),
            ).contents.value = value
            parent.ctypes.cast(
                overlapped,
                parent.ctypes.POINTER(parent.wintypes.LPVOID),
            ).contents.value = 41
            return True

    kernel = Kernel()
    events: list[object] = []
    handle = parent._OwnedHandle(kernel, "completion_port", 1)
    monkeypatch.setattr(parent.time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(parent.ctypes, "get_last_error", lambda: parent.WAIT_TIMEOUT)

    assert parent._drain_job_events(kernel, handle, events, 1.0) == (True, False)
    assert not any(event.kind == "active_limit" for event in events)
    assert parent._drain_job_events(kernel, handle, events, 1.0) == (True, True)
    assert events[-1].kind == "active_limit"


def test_continuous_completion_production_yields_at_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.calls = 0

        def GetQueuedCompletionStatus(
            self,
            _port: object,
            message: object,
            _key: object,
            overlapped: object,
            _timeout: int,
        ) -> bool:
            self.calls += 1
            parent.ctypes.cast(
                message,
                parent.ctypes.POINTER(parent.wintypes.DWORD),
            ).contents.value = parent.JOB_OBJECT_MSG_NEW_PROCESS
            parent.ctypes.cast(
                overlapped,
                parent.ctypes.POINTER(parent.wintypes.LPVOID),
            ).contents.value = 41
            return True

    kernel = Kernel()
    clock = iter((0.0, 0.0, 0.4, 0.4, 0.8, 1.0))
    monkeypatch.setattr(parent.time, "monotonic", lambda: next(clock, 1.0))

    assert parent._drain_job_events(
        kernel,
        parent._OwnedHandle(kernel, "completion_port", 1),
        [],
        1.0,
    ) == (True, False)
    assert kernel.calls == 3


def test_expired_service_deadline_performs_no_native_drain_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        @staticmethod
        def PeekNamedPipe(*_args: object) -> bool:
            raise AssertionError("pipe operation after deadline")

        @staticmethod
        def GetQueuedCompletionStatus(*_args: object) -> bool:
            raise AssertionError("completion operation after deadline")

    kernel = Kernel()
    monkeypatch.setattr(parent.time, "monotonic", lambda: 2.0)

    assert parent._drain_pipe(
        kernel,
        parent._OwnedHandle(kernel, "stdout_read", 1),
        bytearray(),
        4,
        False,
        False,
        2.0,
    ) == (False, False, True)
    assert parent._drain_job_events(
        kernel,
        parent._OwnedHandle(kernel, "completion_port", 2),
        [],
        2.0,
    ) == (True, False)


def test_postcreation_failure_requests_termination_and_reconciles_owned_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.terminate_calls = 0
            self.wait_calls = 0

        def TerminateJobObject(self, _job: object, _code: int) -> bool:
            self.terminate_calls += 1
            return True

        def WaitForSingleObject(self, _process: object, _timeout: int) -> int:
            self.wait_calls += 1
            return parent.WAIT_OBJECT_0

    kernel = Kernel()
    handles = {
        name: parent._OwnedHandle(kernel, name, index + 1)
        for index, name in enumerate(("job", "process", "completion_port", "stdout_read", "stderr_read"))
    }
    request = parent._LaunchRequest(
        parent._TargetBinding(bytearray(), parent._FileIdentity(1, 2, 3, 4, "a" * 64, "3.13", "3.13")),
        ("python.exe", "-B", parent.FIXED_CHILD_SCRIPT, OBSERVATION_ID),
        ROOT,
        (),
        120.0,
        4096,
        128,
    )
    drain_calls: list[str] = []
    monkeypatch.setattr(parent, "_drain_job_events", lambda *_args: drain_calls.append("events") or True)
    monkeypatch.setattr(
        parent,
        "_drain_pipe",
        lambda _kernel, handle, _retained, _limit, _eof, overflow, _deadline: (
            True,
            overflow,
            drain_calls.append(handle.name) is None,
        ),
    )
    monkeypatch.setattr(parent, "_query_accounting", lambda *_args: (1, 0))
    monkeypatch.setattr(parent.time, "monotonic", lambda: 0.0)

    result = parent._recover_postcreation_failure(
        kernel,
        handles,
        [],
        bytearray(),
        bytearray(),
        request,
        False,
        False,
        False,
        False,
        False,
        None,
    )

    assert result == (True, True, True, True, False, False, True, 1, 0)
    assert kernel.terminate_calls == 1
    assert kernel.wait_calls == 1
    assert drain_calls == ["events", "stdout_read", "stderr_read"]


def test_postcreation_exception_branch_routes_through_reconciliation() -> None:
    source = inspect.getsource(parent._execute_windows_once)
    exception = source.index("except BaseException as exc:")
    recovery = source.index("_recover_postcreation_failure(", exception)
    cleanup = source.index("finally:", recovery)
    assert exception < recovery < cleanup


def test_postcreation_failure_reconciliation_is_bounded_to_five_seconds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Kernel:
        def __init__(self) -> None:
            self.wait_calls = 0

        def TerminateJobObject(self, _job: object, _code: int) -> bool:
            return True

        def WaitForSingleObject(self, _process: object, _timeout: int) -> int:
            self.wait_calls += 1
            return parent.WAIT_TIMEOUT

    kernel = Kernel()
    handles = {
        name: parent._OwnedHandle(kernel, name, index + 1)
        for index, name in enumerate(("job", "process", "completion_port", "stdout_read", "stderr_read"))
    }
    request = parent._LaunchRequest(
        parent._TargetBinding(bytearray(), parent._FileIdentity(1, 2, 3, 4, "a" * 64, "3.13", "3.13")),
        ("python.exe", "-B", parent.FIXED_CHILD_SCRIPT, OBSERVATION_ID),
        ROOT,
        (),
        120.0,
        4096,
        128,
    )
    times = iter((10.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0))
    current = 11.0
    sleeps: list[float] = []

    def monotonic() -> float:
        nonlocal current
        current = next(times, 15.0)
        return current

    monkeypatch.setattr(parent.time, "monotonic", monotonic)
    monkeypatch.setattr(parent.time, "sleep", sleeps.append)
    monkeypatch.setattr(parent, "_drain_job_events", lambda *_args: True)
    monkeypatch.setattr(
        parent,
        "_drain_pipe",
        lambda _kernel, _handle, _retained, _limit, eof, overflow, _deadline: (
            eof,
            overflow,
            True,
        ),
    )
    monkeypatch.setattr(parent, "_query_accounting", lambda *_args: (1, 1))

    result = parent._recover_postcreation_failure(
        kernel,
        handles,
        [],
        bytearray(),
        bytearray(),
        request,
        False,
        False,
        False,
        False,
        False,
        None,
    )

    assert result[-3:] == (False, 1, 1)
    assert kernel.wait_calls == 1
    assert sleeps == [0.01]


@pytest.mark.parametrize(
    "changes",
    [
        {"exit_code": 1},
        {"stderr": b"x"},
        {"stdout": b"invalid"},
        {"stdout": b"x" * 4097},
        {"stderr": b"x" * 129},
    ],
)
def test_child_exit_stderr_and_payload_validation_fail_closed(changes: dict[str, object]) -> None:
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(**changes)
    result, _owner = run(adapter)
    assert result == "observation_validation_failed"


def test_all_fifteen_post_exit_facts_are_parent_derived_and_sealed_once() -> None:
    adapter = FakeAdapter()
    result, owner = run(adapter)
    assert result == RECEIPT
    assert owner.parse_calls == 1
    assert owner.seal_calls == 1
    assert owner.facts == FakePostExitFacts(
        1,
        0,
        True,
        True,
        0,
        True,
        False,
        False,
        True,
        True,
        0,
        0,
        0,
        0,
        0,
    )


def test_success_is_deterministic_for_identical_parent_evidence() -> None:
    first, _first_owner = run(FakeAdapter())
    second, _second_owner = run(FakeAdapter())
    assert first == second == RECEIPT


@pytest.mark.parametrize(
    "mutation",
    [
        lambda adapter: setattr(adapter, "before", replace(adapter.before, exact=False)),
        lambda adapter: setattr(adapter, "target_exact", None),
        lambda adapter: setattr(adapter, "evidence", launch_evidence(exit_code=1)),
        lambda adapter: setattr(adapter, "evidence", launch_evidence(stdout_eof=False)),
    ],
)
def test_sealer_is_never_called_before_complete_terminal_success(mutation: object) -> None:
    adapter = FakeAdapter()
    mutation(adapter)
    owner = FakeOwner()
    result, _owner = run(adapter, owner)
    assert result != RECEIPT
    assert owner.seal_calls == 0


@pytest.mark.parametrize(
    ("sealed", "expected"),
    [
        ("observation_receipt_sealing_failed", "observation_receipt_sealing_failed"),
        ("unexpected", "observation_result_unknown"),
        (None, "observation_result_unknown"),
    ],
)
def test_sealer_result_is_closed_and_no_unknown_value_echoes(
    sealed: object,
    expected: str,
) -> None:
    owner = FakeOwner()

    def seal(*_args: object) -> object:
        owner.seal_calls += 1
        return sealed

    owner.seal_proportionate_observation_receipt = seal
    result, _owner = run(FakeAdapter(), owner)
    assert result == expected
    assert result != repr(sealed)


def test_fixed_failure_output_is_symbolic_and_no_echo(monkeypatch: pytest.MonkeyPatch) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_load_owner", lambda _root: FakeOwner())
    adapter = FakeAdapter()
    adapter.image_exact = False
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: adapter)
    expected = parent._canonical_target_binding(adapter.identity).transport
    assert parent.main([OBSERVATION_ID, "--expected-target-binding-v1", expected]) == 2
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_binding_rejected\n"
    assert PRIVATE_MARKER not in stderr.getvalue()


@pytest.mark.parametrize("arguments", [[], [OBSERVATION_ID, "extra"], ["--help"], [OBSERVATION_ID, OBSERVATION_ID]])
def test_main_rejects_missing_extra_option_and_duplicate_arguments(
    arguments: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stderr)
    assert parent.main(arguments) == 2
    assert stderr.getvalue() == "observation_sequence_rejected\n"


def test_operation_free_fake_never_touches_process_network_github_or_durable_state() -> None:
    adapter = FakeAdapter()
    result, _owner = run(adapter)
    assert result == RECEIPT
    assert adapter.calls.count("launch") == 1
    assert adapter.counts == parent._AuditCounts(0, 0, 0, 0)
    assert not any(word in " ".join(adapter.calls) for word in ("github", "publish", "task", "network"))
    assert adapter.clear_count == 1


def known_binding() -> object:
    identity = parent._FileIdentity(
        1,
        2,
        105696,
        4,
        "1" * 64,
        "3.13.14",
        "3.13.14",
        "2" * 64,
    )
    return parent._canonical_target_binding(identity)


def transport_bytes(payload: bytes) -> str:
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")


def test_successor_target_binding_known_answer_vectors_are_exact() -> None:
    binding = known_binding()
    assert len(parent._compact_object(binding.fields[:-1])) == 715
    assert binding.binding_sha256 == "06cfed1c779da954fac24d2126042421730601de8bbc4d8fd6a9abfb57d27a49"
    assert len(binding.canonical_bytes) == 800
    assert binding.artifact_sha256 == "aa95693b259eaa888e7d1146fc1c67fcf981ab79ca559faed635c71117ebb700"
    assert len(binding.transport) == 1067
    assert parent._decode_target_binding_transport(binding.transport) == binding


def test_stable_identity_known_answer_is_exact_and_raw_values_are_not_public() -> None:
    preimage = parent._stable_identity_preimage(0x1234ABCD, 0x0123456789ABCDEF)
    assert len(preimage) == 112
    assert hashlib.sha256(preimage).hexdigest() == (
        "e860ac1f60d36d5d0e670c181d0bd563641f3f001d775db525a64a5beb9003a3"
    )
    public = known_binding().canonical_bytes
    assert b"1234abcd" not in public
    assert b"0123456789abcdef" not in public


@pytest.mark.parametrize(
    "payload_mutation",
    [
        lambda payload: payload[:-1],
        lambda payload: payload + b"\n",
        lambda payload: payload.replace(b'"repository_id":1235264383', b'"repository_id":1235264383 '),
        lambda payload: payload.replace(b'"issue_number":826', b'"issue_number":"826"'),
        lambda payload: payload.replace(b'"ordinary_file":true', b'"ordinary_file":1'),
        lambda payload: payload.replace(b'"file_version":"3.13.14"', b'"file_version":"3.13"'),
        lambda payload: payload.replace(b'"binding_sha256":"0', b'"binding_sha256":"f'),
        lambda payload: payload.replace(b'"schema_version"', b'"unexpected"', 1),
        lambda payload: payload.replace(b'"schema_version":', b'"schema_version":"x","schema_version":', 1),
    ],
)
def test_binding_parser_rejects_noncanonical_duplicate_mistyped_and_drifted_bytes(
    payload_mutation: object,
) -> None:
    payload = payload_mutation(known_binding().canonical_bytes)
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_canonical_binding_bytes(payload)


@pytest.mark.parametrize(
    ("field_name", "wrong_value"),
    [
        ("repository_id", 1),
        ("issue_number", 780),
        ("host_os_name", "posix"),
        ("host_sys_platform", "linux"),
        ("runtime_implementation", "PyPy"),
        ("executable_basename", "py.exe"),
        ("stable_identity_schema", "trusted_owner_r0_direct_interpreter_file_identity.v1"),
        ("ordinary_file", False),
        ("reparse_point", True),
        ("private_path_source", "caller_selected"),
        ("private_path_publication_authorized", True),
    ],
)
def test_binding_parser_rejects_each_closed_constant_even_with_recomputed_digest(
    field_name: str,
    wrong_value: object,
) -> None:
    fields = list(known_binding().fields)
    index = parent.TARGET_BINDING_FIELDS.index(field_name)
    fields[index] = (field_name, wrong_value)
    fields[-1] = (
        "binding_sha256",
        hashlib.sha256(parent._compact_object(tuple(fields[:-1]))).hexdigest(),
    )
    payload = parent._compact_object(tuple(fields)) + b"\n"
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_canonical_binding_bytes(payload)


@pytest.mark.parametrize("mutation", ["missing", "reordered"])
def test_binding_parser_rejects_missing_and_reordered_fields(mutation: str) -> None:
    fields = list(known_binding().fields)
    if mutation == "missing":
        del fields[7]
    else:
        fields[7], fields[8] = fields[8], fields[7]
    fields[-1] = (
        "binding_sha256",
        hashlib.sha256(parent._compact_object(tuple(fields[:-1]))).hexdigest(),
    )
    payload = parent._compact_object(tuple(fields)) + b"\n"
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_canonical_binding_bytes(payload)


@pytest.mark.parametrize(
    "transport",
    [
        "",
        "=",
        "abcd=",
        "abcd+",
        "a" * 2049,
        "\N{LATIN SMALL LETTER E WITH ACUTE}",
        transport_bytes(b"{}\n"),
    ],
)
def test_binding_transport_rejects_invalid_ambiguous_and_oversized_values(transport: str) -> None:
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._decode_target_binding_transport(transport)


def test_malformed_expected_binding_is_rejected_before_adapter_or_private_ingress(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: pytest.fail("adapter constructed"))
    monkeypatch.setattr(parent, "_load_owner", lambda _root: pytest.fail("owner loaded"))
    assert parent.main([OBSERVATION_ID, "--expected-target-binding-v1", "invalid="]) == 2
    assert stderr.getvalue() == "observation_sequence_rejected\n"


def test_historical_direct_interpreter_binding_is_rejected() -> None:
    fields = list(known_binding().fields)
    fields[0] = ("schema_version", "trusted_owner_r0_direct_interpreter_binding.v1")
    fields[2] = ("issue_number", 780)
    fields[-1] = (
        "binding_sha256",
        hashlib.sha256(parent._compact_object(tuple(fields[:-1]))).hexdigest(),
    )
    payload = parent._compact_object(tuple(fields)) + b"\n"
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_canonical_binding_bytes(payload)


def test_metadata_mode_emits_only_binding_after_cleanup_and_never_loads_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FlushTrackingOutput(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: str) -> int:
            self.write_calls += 1
            return super().write(value)

        def flush(self) -> None:
            self.flush_calls += 1

    stdout = FlushTrackingOutput()
    stderr = io.StringIO()
    adapter = FakeAdapter()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: adapter)
    monkeypatch.setattr(parent, "_load_owner", lambda _root: pytest.fail("owner loaded"))

    assert parent.main(["--emit-target-binding"]) == 0
    assert stdout.getvalue().encode("ascii") == known_binding().canonical_bytes
    assert stdout.write_calls == 1
    assert stdout.flush_calls == 1
    assert stderr.getvalue() == ""
    assert "launch" not in adapter.calls
    assert adapter.calls.count("validate_controller_image") == 1
    assert adapter.calls.count("image_binding_exact") == 1
    snapshot_indices = [index for index, value in enumerate(adapter.calls) if value == "snapshot"]
    assert adapter.calls.index("install_audit") < snapshot_indices[0]
    assert snapshot_indices[0] < adapter.calls.index("validate_controller_image")
    assert adapter.calls.index("finish_image_guards") < snapshot_indices[1]
    assert adapter.calls[-1] == "audit_counts"


@pytest.mark.parametrize("failure", ["audit", "snapshot_exception", "snapshot_inexact"])
def test_metadata_audit_boundary_failure_precedes_private_image_inspection(
    failure: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = FakeAdapter()
    if failure == "audit":
        def fail_audit(repository_root: Path) -> None:
            assert repository_root == ROOT
            adapter.calls.append("install_audit")
            raise parent._ControllerError("observation_binding_rejected")

        monkeypatch.setattr(adapter, "install_audit", fail_audit)
    elif failure == "snapshot_exception":
        def fail_snapshot(repository_root: Path) -> object:
            assert repository_root == ROOT
            adapter.calls.append("snapshot")
            raise parent._ControllerError("observation_binding_rejected")

        monkeypatch.setattr(adapter, "snapshot_effects", fail_snapshot)
    else:
        adapter.before = parent._EffectSnapshot(False, "repo", "installed", frozenset())

    assert run_metadata(adapter) == "observation_binding_rejected"
    assert "validate_controller_image" not in adapter.calls
    assert "image_binding_exact" not in adapter.calls
    assert "launch" not in adapter.calls


def test_metadata_binding_is_derived_from_the_controller_image_only() -> None:
    adapter = FakeAdapter()
    adapter.controller_identity = replace(adapter.identity, file_version="3.13.15")
    result = run_metadata(adapter)
    assert type(result) is bytes
    parsed = parent._validate_canonical_binding_bytes(result)
    assert dict(parsed.fields)["file_version"] == "3.13.15"
    assert adapter.calls.count("validate_controller_image") == 1
    assert "launch" not in adapter.calls


def test_write_exact_flushes_the_selected_binary_buffer() -> None:
    class BufferedSink:
        def __init__(self) -> None:
            self.pending = bytearray()
            self.drained = bytearray()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: bytes) -> int:
            self.write_calls += 1
            self.pending.extend(value)
            return len(value)

        def flush(self) -> None:
            self.flush_calls += 1
            self.drained.extend(self.pending)
            self.pending.clear()

    class BinaryOutput:
        def __init__(self) -> None:
            self.buffer = BufferedSink()

    output = BinaryOutput()
    payload = known_binding().canonical_bytes

    parent._write_exact(output, payload)

    assert output.buffer.write_calls == 1
    assert output.buffer.flush_calls == 1
    assert output.buffer.pending == b""
    assert output.buffer.drained == payload


def test_metadata_output_refusal_fails_symbolically_without_reported_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class RefusingOutput(io.StringIO):
        def write(self, value: str) -> int:
            del value
            return 0

    stdout = RefusingOutput()
    stderr = io.StringIO()
    adapter = FakeAdapter()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: adapter)
    assert parent.main(["--emit-target-binding"]) == 3
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == "observation_result_unknown\n"
    assert "launch" not in adapter.calls


def test_metadata_flush_failure_is_terminal_nonretryable_and_non_authoritative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FlushFailingOutput(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: str) -> int:
            self.write_calls += 1
            return super().write(value)

        def flush(self) -> None:
            self.flush_calls += 1
            raise OSError

    stdout = FlushFailingOutput()
    stderr = io.StringIO()
    adapter = FakeAdapter()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: adapter)
    monkeypatch.setattr(parent, "_load_owner", lambda _root: pytest.fail("owner loaded"))

    assert parent.main(["--emit-target-binding"]) == 3
    assert stdout.getvalue().encode("ascii") == known_binding().canonical_bytes
    assert stdout.write_calls == 1
    assert stdout.flush_calls == 1
    assert stderr.getvalue() == "observation_result_unknown\n"
    assert "launch" not in adapter.calls
    assert adapter.counts == parent._AuditCounts(0, 0, 0, 0)
    assert PRIVATE_MARKER not in stdout.getvalue()
    assert PRIVATE_MARKER not in stderr.getvalue()


def test_metadata_short_write_prefix_is_terminal_nonretryable_and_non_authoritative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ShortWritingOutput(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: str) -> int:
            self.write_calls += 1
            super().write(value[:17])
            return 17

        def flush(self) -> None:
            self.flush_calls += 1

    stdout = ShortWritingOutput()
    stderr = io.StringIO()
    adapter = FakeAdapter()
    binding = known_binding()
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: adapter)
    monkeypatch.setattr(parent, "_load_owner", lambda _root: pytest.fail("owner loaded"))

    assert parent.main(["--emit-target-binding"]) == 3

    prefix = stdout.getvalue().encode("ascii")
    assert prefix == binding.canonical_bytes[:17]
    assert stdout.write_calls == 1
    assert stdout.flush_calls == 0
    assert len(prefix) != len(binding.canonical_bytes)
    assert hashlib.sha256(prefix).hexdigest() != binding.artifact_sha256
    with pytest.raises(parent._ControllerError, match="observation_sequence_rejected"):
        parent._validate_canonical_binding_bytes(prefix)
    assert stderr.getvalue() == "observation_result_unknown\n"
    assert "launch" not in adapter.calls
    assert adapter.counts == parent._AuditCounts(0, 0, 0, 0)
    assert PRIVATE_MARKER not in stdout.getvalue()
    assert PRIVATE_MARKER not in stderr.getvalue()


@pytest.mark.parametrize("failure", ["binding", "recheck", "close", "effect"])
def test_metadata_failures_emit_no_partial_binding_and_never_launch(failure: str) -> None:
    adapter = FakeAdapter()
    if failure == "binding":
        adapter.controller_identity = replace(adapter.identity, product_version="3.14")
    elif failure == "recheck":
        adapter.image_exact = False
    elif failure == "close":
        adapter.image_close_results["controller_image_guard"] = False
    else:
        adapter.counts = parent._AuditCounts(1, 0, 0, 0)
    result = run_metadata(adapter)
    assert type(result) is str
    assert result in {
        "observation_binding_rejected",
        "observation_timeout_unknown",
        "observation_safety_boundary_failed",
    }
    assert "launch" not in adapter.calls
    assert PRIVATE_MARKER not in result


def test_execution_rejects_controller_image_mismatch_before_process_entry() -> None:
    adapter = FakeAdapter()
    expected = parent._canonical_target_binding(adapter.identity)
    adapter.controller_identity = replace(adapter.identity, stable_identity_sha256="3" * 64)
    result, owner = run_with_expected(adapter, expected)
    assert result == "observation_binding_rejected"
    assert "launch" not in adapter.calls
    assert owner.parse_calls == owner.seal_calls == 0


def test_unknown_guard_revalidation_fails_before_process_entry() -> None:
    adapter = FakeAdapter()
    adapter.image_exact = None
    result, owner = run(adapter)
    assert result == "observation_binding_rejected"
    assert "launch" not in adapter.calls
    assert owner.parse_calls == owner.seal_calls == 0


@pytest.mark.parametrize(
    "change",
    [
        {"file_version": "3.13.15"},
        {"product_version": "3.13.15"},
        {"size": 105697},
        {"sha256": "3" * 64},
        {"stable_identity_sha256": "4" * 64},
    ],
)
def test_execution_rejects_each_controller_metadata_mismatch_before_process_entry(
    change: dict[str, object],
) -> None:
    adapter = FakeAdapter()
    expected = parent._canonical_target_binding(adapter.identity)
    adapter.controller_identity = replace(adapter.identity, **change)
    result, owner = run_with_expected(adapter, expected)
    assert result == "observation_binding_rejected"
    assert "launch" not in adapter.calls
    assert owner.parse_calls == owner.seal_calls == 0


def test_expected_binding_is_not_forwarded_to_child_or_receipt() -> None:
    adapter = FakeAdapter()
    expected = parent._canonical_target_binding(adapter.identity)
    result, _owner = run_with_expected(adapter, expected)
    assert result == RECEIPT
    request = adapter.request
    assert request is not None
    projected = repr((request.tokens, request.environment, request.repository_root, result))
    assert expected.transport not in projected
    assert expected.binding_sha256 not in projected


@pytest.mark.parametrize(
    "arguments",
    [
        [OBSERVATION_ID],
        ["--expected-target-binding-v1", OBSERVATION_ID, known_binding().transport],
        [OBSERVATION_ID, known_binding().transport, "--expected-target-binding-v1"],
        [OBSERVATION_ID, "--expected-target-binding-v1"],
        [OBSERVATION_ID, "--expected-target-binding-v1", known_binding().transport, "extra"],
        ["--emit-target-binding", "--emit-target-binding"],
    ],
)
def test_main_admits_only_the_two_exact_public_modes(
    arguments: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent, "_repository_root", lambda: ROOT)
    assert parent.main(arguments) == 2
    assert stderr.getvalue() == "observation_sequence_rejected\n"


def test_malformed_public_input_precedes_repository_root_rejection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(
        parent,
        "_repository_root",
        lambda: (_ for _ in ()).throw(parent._ControllerError("observation_binding_rejected")),
    )
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: pytest.fail("adapter constructed"))

    assert parent.main(["--emit-target-binding", "extra"]) == 2
    assert stderr.getvalue() == "observation_sequence_rejected\n"


def test_non_windows_rejection_precedes_public_input_and_repository_validation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(parent.os, "name", "posix")
    monkeypatch.setattr(parent.sys, "platform", "linux")
    monkeypatch.setattr(parent, "_repository_root", lambda: pytest.fail("repository inspected"))
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: pytest.fail("adapter constructed"))

    assert parent.main(["--emit-target-binding", "extra"]) == 2
    assert stderr.getvalue() == "observation_host_rejected\n"


def test_current_controller_identity_has_one_bounded_native_source() -> None:
    source = inspect.getsource(parent._WindowsParentAdapter.validate_controller_image)
    assert source.count("QueryFullProcessImageNameW") == 1
    assert source.count("GetCurrentProcess") == 1
    assert "sys.executable" not in source
    assert "PATH" not in source
    assert "registry" not in source.lower()


def test_second_target_ingress_and_duplicate_guard_are_absent() -> None:
    source = MODULE_PATH.read_text(encoding="ascii")
    for forbidden in (
        "GetStdHandle",
        "GetConsoleMode",
        "SetConsoleMode",
        "ReadConsoleW",
        "PeekConsoleInputW",
        "ReadConsoleInputW",
        "GetNumberOfConsoleInputEvents",
        "target_guard",
        "validate_target",
    ):
        assert forbidden not in source


def parse_development_transcript(payload: bytes) -> dict[str, object]:
    lines = payload.decode("utf-8").splitlines()
    assert lines[0] == "MYTHIC_EDGE_DEVELOPMENT_DIAGNOSTIC_BEGIN"
    assert lines[-1] == "MYTHIC_EDGE_DEVELOPMENT_DIAGNOSTIC_END"
    assert payload.endswith(b"\n")
    assert len(payload) <= parent.MAX_DEVELOPMENT_DIAGNOSTIC_BYTES
    names = [line.partition("=")[0] for line in lines[1:-1]]
    assert names == [
        "profile",
        "outcome",
        "first_failed_predicate",
        "exception_type",
        "exception_message",
        "exception_traceback",
        "win32_last_error",
        "call_order",
        "relevant_values",
        "controller_image_guard_close",
        "child_creation_count",
        "network_operation_count",
        "repository_write_count",
        "installed_write_count",
        "external_effect_count",
        "generated_residue_count",
    ]
    parsed: dict[str, object] = {}
    for line in lines[1:-1]:
        name, separator, value = line.partition("=")
        assert separator == "="
        parsed[name] = json.loads(value)
    return parsed


def configure_development_failure(adapter: FakeAdapter, predicate: str) -> None:
    adapter.development_failure = predicate
    if predicate == "before_effect_snapshot_exact":
        adapter.before = replace(adapter.before, exact=False)
    elif predicate == "controller_image_guard_close_exact":
        adapter.image_close_results["controller_image_guard"] = False
        adapter.development_failure = None
    elif predicate == "after_effect_snapshot_exact":
        adapter.after = replace(adapter.after, exact=False)
    elif predicate == "effect_snapshots_equal":
        adapter.after = replace(adapter.after, repository_digest="changed")
    elif predicate == "audit_counts_zero":
        adapter.counts = parent._AuditCounts(1, 0, 0, 0)


def test_development_diagnostic_success_is_disjoint_and_non_authoritative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = FakeAdapter()
    monkeypatch.setattr(
        parent,
        "_canonical_target_binding",
        lambda _identity: pytest.fail("canonical binding constructed"),
    )
    recorder = parent._run_development_diagnostic(adapter, repository_root=ROOT)

    assert recorder.first_failed_predicate is None
    assert recorder.call_order == list(parent._DEVELOPMENT_PREDICATES[:27])
    assert recorder.controller_image_guard_close == "closed_exact"
    assert adapter.clear_count == 1
    assert "launch" not in adapter.calls
    assert "finish_checker_guard" not in adapter.calls
    payload = parent._development_transcript(recorder)
    parsed = parse_development_transcript(payload)
    assert parsed["outcome"] == "metadata_path_completed_without_binding"
    assert parsed["first_failed_predicate"] is None
    assert parsed["call_order"] == list(parent._DEVELOPMENT_PREDICATES)
    assert parsed["child_creation_count"] == 0
    assert parsed["network_operation_count"] == 0
    assert parsed["repository_write_count"] == 0
    assert parsed["installed_write_count"] == 0
    assert parsed["external_effect_count"] == 0
    assert parsed["generated_residue_count"] == 0


def test_development_transcript_derives_nonzero_audit_counts() -> None:
    adapter = FakeAdapter()
    adapter.counts = parent._AuditCounts(2, 3, 4, 5)

    recorder = parent._run_development_diagnostic(adapter, repository_root=ROOT)
    parsed = parse_development_transcript(parent._development_transcript(recorder))

    assert recorder.first_failed_predicate == "audit_counts_zero"
    assert parsed["child_creation_count"] == 0
    assert parsed["network_operation_count"] == 2
    assert parsed["repository_write_count"] == 3
    assert parsed["installed_write_count"] == 4
    assert parsed["external_effect_count"] == 5
    assert parsed["generated_residue_count"] == 0


def test_development_transcript_rejects_unclosed_effect_evidence() -> None:
    recorder = parent._DevelopmentRecorder()
    recorder.passed("host_windows_exact")
    recorder.passed("development_mode_exact")
    recorder.passed("repository_root_resolved")
    recorder.passed("audit_installed")
    snapshot = parent._EffectSnapshot(True, "repo", "installed", frozenset())
    recorder.observe_before_effect_snapshot(snapshot)
    recorder.passed("before_effect_snapshot_available")

    with pytest.raises(ValueError, match="development effect evidence is incomplete"):
        parent._development_transcript(recorder)


def test_development_transcript_derives_child_creation_calls() -> None:
    recorder = parent._DevelopmentRecorder()
    snapshot = parent._EffectSnapshot(True, "repo", "installed", frozenset())
    recorder.observe_before_effect_snapshot(snapshot)
    recorder.observe_after_effect_snapshot(snapshot)
    recorder.observe_audit_counts(parent._AuditCounts(0, 0, 0, 0))
    recorder.observe_child_creation_count(1)
    recorder.close_effect_observation()

    parsed = parse_development_transcript(parent._development_transcript(recorder))

    assert parsed["child_creation_count"] == 1


def test_development_transcript_derives_inventory_mismatches_and_residue() -> None:
    adapter = FakeAdapter()
    adapter.after = parent._EffectSnapshot(
        True,
        "changed-repository",
        "changed-installed",
        frozenset({"new-residue"}),
    )

    recorder = parent._run_development_diagnostic(adapter, repository_root=ROOT)
    parsed = parse_development_transcript(parent._development_transcript(recorder))

    assert recorder.first_failed_predicate == "effect_snapshots_equal"
    assert parsed["network_operation_count"] == 0
    assert parsed["repository_write_count"] == 1
    assert parsed["installed_write_count"] == 1
    assert parsed["external_effect_count"] == 0
    assert parsed["generated_residue_count"] == 1


def test_development_failure_still_collects_bounded_effect_evidence() -> None:
    adapter = FakeAdapter()
    adapter.development_failure = "controller_image_versions_well_formed"
    adapter.counts = parent._AuditCounts(7, 8, 9, 10)
    adapter.after = replace(adapter.before, generated_residue=frozenset({"new-residue"}))

    recorder = parent._run_development_diagnostic(adapter, repository_root=ROOT)
    parsed = parse_development_transcript(parent._development_transcript(recorder))

    assert recorder.first_failed_predicate == "controller_image_versions_well_formed"
    assert parsed["network_operation_count"] == 7
    assert parsed["repository_write_count"] == 8
    assert parsed["installed_write_count"] == 9
    assert parsed["external_effect_count"] == 10
    assert parsed["generated_residue_count"] == 1


def test_development_path_revalidation_preserves_raw_exception_while_production_blinds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = object.__new__(parent._WindowsParentAdapter)
    adapter.kernel32 = object()
    adapter.controller_guard = SimpleNamespace(open=True)
    target = parent._TargetBinding(
        bytearray(PRIVATE_MARKER.encode("utf-16-le")),
        parent._FileIdentity(
            1,
            2,
            3,
            4,
            "1" * 64,
            "3.13.14",
            "3.13.14",
            "2" * 64,
        ),
    )
    monkeypatch.setattr(
        parent,
        "_handle_stable_identity",
        lambda _kernel32, _guard: target.identity.stable_identity_sha256,
    )
    raw_failure = OSError(f"synthetic revalidation failure: {PRIVATE_MARKER}")
    monkeypatch.setattr(
        parent,
        "_stable_file_bytes",
        lambda _path, **_kwargs: (_ for _ in ()).throw(raw_failure),
    )
    recorder = parent._DevelopmentRecorder()

    with pytest.raises(parent._DevelopmentAbort):
        adapter._development_revalidate_controller_image(target, recorder)

    assert recorder.first_failed_predicate == "controller_image_path_identity_exact"
    assert recorder.exception_type == "OSError"
    assert recorder.exception_message == str(raw_failure)
    assert recorder.relevant_values["controller_image_path"] == PRIVATE_MARKER
    assert adapter.image_binding_exact(target) is False


@pytest.mark.parametrize(
    "predicate",
    [
        "audit_installed",
        "before_effect_snapshot_available",
        "before_effect_snapshot_exact",
        *parent._DEVELOPMENT_IMAGE_PREDICATES,
        "controller_image_guard_identity_exact",
        "controller_image_path_identity_exact",
        "controller_image_guard_close_exact",
        "after_effect_snapshot_available",
        "after_effect_snapshot_exact",
        "effect_snapshots_equal",
        "audit_counts_available",
        "audit_counts_zero",
    ],
)
def test_each_development_predicate_fails_first_and_stops_later_work(predicate: str) -> None:
    adapter = FakeAdapter()
    configure_development_failure(adapter, predicate)

    recorder = parent._run_development_diagnostic(adapter, repository_root=ROOT)

    assert recorder.first_failed_predicate == predicate
    assert recorder.call_order.count(predicate) == 1
    first_index = parent._DEVELOPMENT_PREDICATES.index(predicate)
    for observed in recorder.call_order[recorder.call_order.index(predicate) + 1 :]:
        assert observed == "controller_image_guard_close_exact"
    assert "launch" not in adapter.calls
    assert all(
        parent._DEVELOPMENT_PREDICATES.index(observed) <= first_index
        or observed == "controller_image_guard_close_exact"
        for observed in recorder.call_order
    )
    parsed = parse_development_transcript(parent._development_transcript(recorder))
    assert parsed["first_failed_predicate"] == predicate


def test_development_host_and_mode_fail_before_repository_or_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(parent.os, "name", "posix")
    monkeypatch.setattr(parent.sys, "platform", "linux")
    adapter = FakeAdapter()
    host = parent._run_development_diagnostic(adapter, repository_root=ROOT)
    assert host.first_failed_predicate == "host_windows_exact"
    assert adapter.calls == []
    assert parse_development_transcript(parent._development_transcript(host))[
        "first_failed_predicate"
    ] == "host_windows_exact"

    monkeypatch.setattr(parent.os, "name", "nt")
    monkeypatch.setattr(parent.sys, "platform", "win32")
    mode = parent._run_development_diagnostic(adapter, repository_root=ROOT, mode_exact=False)
    assert mode.first_failed_predicate == "development_mode_exact"
    assert adapter.calls == []
    assert parse_development_transcript(parent._development_transcript(mode))[
        "first_failed_predicate"
    ] == "development_mode_exact"


def test_development_repository_failure_is_unblinded_without_adapter_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        parent,
        "_repository_root",
        lambda: (_ for _ in ()).throw(OSError(f"root failure: {PRIVATE_MARKER}")),
    )
    monkeypatch.setattr(parent, "_WindowsParentAdapter", lambda: pytest.fail("adapter constructed"))

    recorder = parent._run_development_diagnostic()

    assert recorder.first_failed_predicate == "repository_root_resolved"
    assert PRIVATE_MARKER in (recorder.exception_message or "")
    assert parse_development_transcript(parent._development_transcript(recorder))[
        "first_failed_predicate"
    ] == "repository_root_resolved"


def test_development_host_failure_emits_one_complete_bounded_transcript(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    stdout = io.StringIO()
    monkeypatch.setattr(parent.os, "name", "posix")
    monkeypatch.setattr(parent.sys, "platform", "linux")
    monkeypatch.setattr(parent.sys, "stderr", stderr)
    monkeypatch.setattr(parent.sys, "stdout", stdout)

    assert parent.main([parent.DEVELOPMENT_MODE]) == 0

    payload = stderr.getvalue().encode("utf-8")
    parsed = parse_development_transcript(payload)
    assert parsed["first_failed_predicate"] == "host_windows_exact"
    assert parsed["child_creation_count"] == 0
    assert parsed["network_operation_count"] == 0
    assert parsed["repository_write_count"] == 0
    assert parsed["installed_write_count"] == 0
    assert parsed["external_effect_count"] == 0
    assert parsed["generated_residue_count"] == 0
    assert stdout.getvalue() == ""


def test_development_transcript_allows_only_bounded_owner_approved_private_detail() -> None:
    recorder = parent._DevelopmentRecorder()
    snapshot = parent._EffectSnapshot(True, "repo", "installed", frozenset())
    recorder.observe_before_effect_snapshot(snapshot)
    recorder.observe_after_effect_snapshot(snapshot)
    recorder.observe_audit_counts(parent._AuditCounts(0, 0, 0, 0))
    recorder.observe_child_creation_count(0)
    recorder.close_effect_observation()
    recorder.failed(
        "repository_root_resolved",
        OSError(f"private path: {PRIVATE_MARKER}"),
        values={"repository_root": PRIVATE_MARKER, "win32_return": 0},
        win32_last_error=5,
    )
    payload = parent._development_transcript(recorder)
    assert PRIVATE_MARKER.encode("ascii") in payload
    for forbidden in (
        b"credential-sentinel",
        b"token-sentinel",
        b"private-key-sentinel",
        b"browser-data-sentinel",
        b"shell-history-sentinel",
        b"environment-dump-sentinel",
        b"unrelated-file-content-sentinel",
    ):
        assert forbidden not in payload


def test_development_output_is_one_write_one_flush_and_never_stdout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class CountingOutput(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: str) -> int:
            self.write_calls += 1
            return super().write(value)

        def flush(self) -> None:
            self.flush_calls += 1

    stderr = CountingOutput()
    stdout = io.StringIO()
    recorder = parent._run_development_diagnostic(FakeAdapter(), repository_root=ROOT)
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(sys, "stdout", stdout)

    assert parent._emit_development_transcript(recorder) == "complete"
    assert stderr.write_calls == 1
    assert stderr.flush_calls == 1
    assert stdout.getvalue() == ""
    assert recorder.call_order[-2:] == [
        "development_output_write_complete",
        "development_output_flush_complete",
    ]
    parse_development_transcript(stderr.getvalue().encode("utf-8"))


@pytest.mark.parametrize("failure", ["short_write", "flush"])
def test_development_output_failure_is_terminal_without_repair(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    class FailingOutput(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.write_calls = 0
            self.flush_calls = 0

        def write(self, value: str) -> int:
            self.write_calls += 1
            if failure == "short_write":
                super().write(value[:17])
                return 17
            return super().write(value)

        def flush(self) -> None:
            self.flush_calls += 1
            if failure == "flush":
                raise OSError("synthetic flush failure")

    stderr = FailingOutput()
    recorder = parent._run_development_diagnostic(FakeAdapter(), repository_root=ROOT)
    monkeypatch.setattr(sys, "stderr", stderr)

    assert parent._emit_development_transcript(recorder) == "diagnostic_incomplete"
    assert stderr.write_calls == 1
    assert stderr.flush_calls == (0 if failure == "short_write" else 1)
    assert recorder.first_failed_predicate == (
        "development_output_write_complete"
        if failure == "short_write"
        else "development_output_flush_complete"
    )


def test_main_dispatches_exact_development_mode_without_production_callthrough(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stderr = io.StringIO()
    stdout = io.StringIO()
    recorder = parent._run_development_diagnostic(FakeAdapter(), repository_root=ROOT)
    monkeypatch.setattr(parent, "_run_development_diagnostic", lambda: recorder)
    monkeypatch.setattr(parent, "_run_metadata", lambda *_args, **_kwargs: pytest.fail("metadata called"))
    monkeypatch.setattr(parent, "_run_controller", lambda *_args, **_kwargs: pytest.fail("controller called"))
    monkeypatch.setattr(parent, "_load_owner", lambda _root: pytest.fail("owner loaded"))
    monkeypatch.setattr(sys, "stderr", stderr)
    monkeypatch.setattr(sys, "stdout", stdout)

    assert parent.main([parent.DEVELOPMENT_MODE]) == 0
    assert stdout.getvalue() == ""
    assert "MYTHIC_EDGE_DEVELOPMENT_DIAGNOSTIC_BEGIN" in stderr.getvalue()


@pytest.mark.parametrize(
    "arguments",
    [
        [parent.DEVELOPMENT_MODE, "extra"],
        [parent.DEVELOPMENT_MODE, parent.DEVELOPMENT_MODE],
        ["--emit-target-binding", parent.DEVELOPMENT_MODE],
    ],
)
def test_malformed_development_mode_never_enters_diagnostic(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
) -> None:
    stderr = io.StringIO()
    monkeypatch.setattr(parent, "_run_development_diagnostic", lambda: pytest.fail("diagnostic called"))
    monkeypatch.setattr(parent, "_repository_root", lambda: pytest.fail("repository inspected"))
    monkeypatch.setattr(sys, "stderr", stderr)

    assert parent.main(arguments) == 2
    assert stderr.getvalue() == "observation_sequence_rejected\n"


def test_two_manual_development_runs_are_independent() -> None:
    first_adapter = FakeAdapter()
    second_adapter = FakeAdapter()
    first = parent._run_development_diagnostic(first_adapter, repository_root=ROOT)
    second = parent._run_development_diagnostic(second_adapter, repository_root=ROOT)

    assert first.call_order == second.call_order == list(parent._DEVELOPMENT_PREDICATES[:27])
    assert first_adapter.clear_count == second_adapter.clear_count == 1
    assert "launch" not in first_adapter.calls + second_adapter.calls


def test_development_source_has_no_production_or_child_route() -> None:
    source = inspect.getsource(parent._run_development_diagnostic)
    for forbidden in (
        "_run_metadata(",
        "_run_controller(",
        "_canonical_target_binding(",
        "_load_owner(",
        "launch_once(",
        "CreateProcessW",
    ):
        assert forbidden not in source


def _real_validation_payload(owner: ModuleType) -> bytes:
    packet: dict[str, object] = {
        "schema_version": "trusted_owner_r0_offline_bootstrap_evidence.v1",
        "operation": "evaluate_r0_bootstrap_eligibility_read_only",
        "repository_id": owner.REPOSITORY_ID,
        "repository_name": "tahjali11/mythic-edge",
        "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/761",
        "base_commit": "ad88b264a1c7947682a00b11c4a57963a43b7548",
        "profile_contract_sha256": owner.PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8",
        "r0_contract_sha256": "ef440f1fe4ce9b0fd342057864e41cbdef93c1ac12ea85a1f9d01912eec4cd02",
        "contract_binding_status": "exact",
        "stage3_manifest_file_count": 41,
        "stage3_manifest_byte_count": 6052,
        "stage3_manifest_sha256": "9109457e5897139658183595fb11c8a7bf9d66e4fb5b5fe6842b20bac43fbce2",
        "manifest_status": "exact",
        "source_tree_node_count": 43,
        "source_tree_file_count": 38,
        "source_tree_manifest_byte_count": 6840,
        "source_tree_sha256": owner.SOURCE_TREE_SHA256,
        "installed_tree_node_count": 43,
        "installed_tree_file_count": 38,
        "installed_tree_manifest_byte_count": 6840,
        "installed_tree_sha256": owner.SOURCE_TREE_SHA256,
        "source_install_status": "identical",
        "registry_status": "valid_exact",
        "registry_sha256": owner.REGISTRY_SHA256,
        "release_state_status": "present_valid_chain",
        "release_state_sha256": owner.RELEASE_STATE_ARTIFACT_SHA256,
        "checker_sha256": owner.R0_CHECKER_SHA256,
        "checker_test_sha256": owner.R0_CHECKER_TEST_SHA256,
        "validator_bundle_sha256": owner.VALIDATOR_BUNDLE_SHA256,
        "validator_bundle_status": "exact",
        "offline_validation_status": "passed",
        "terminal_status": "blocked_release_state_conflict",
        "eligible_for_independent_review": False,
        "effect_counts": {
            "app_server_process_start_count": 0,
            "task_creation_count": 0,
            "network_operation_count": 0,
            "repository_command_count": 0,
            "persistent_mutation_count": 0,
        },
        "authority_flags": {field: False for field in owner.AUTHORITY_FIELDS},
        "evidence_sha256": "",
    }
    packet["evidence_sha256"] = owner.self_digest(packet, "evidence_sha256")
    return owner.canonical_bytes(packet)


def test_success_path_calls_the_exact_integrated_owner_parser_and_sealer() -> None:
    owner = parent._load_owner(ROOT)
    adapter = FakeAdapter()
    adapter.evidence = launch_evidence(stdout=_real_validation_payload(owner))
    result, _owner = run(adapter, owner)
    assert type(result) is bytes
    receipt = owner.parse_receipt(result)
    assert receipt["observation_id"] == OBSERVATION_ID
    assert all(value is False for value in receipt["authority_flags"].values())


def test_canonical_helpers_and_windows_quoting_are_deterministic() -> None:
    assert parent._canonical_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'
    tokens = ("python.exe", "-B", parent.FIXED_CHILD_SCRIPT, OBSERVATION_ID)
    assert parent._command_line(tokens) == parent._command_line(tokens)
    assert PRIVATE_MARKER not in parent._command_line(tokens)
    with pytest.raises(parent._ControllerError):
        parent._environment_block((("PATH", "x"), ("path", "y")))


def test_test_artifact_contains_no_real_private_path_or_secret_marker() -> None:
    payload = Path(__file__).read_bytes()
    private_runtime_fragment = b"AppData" + b"\\Local" + b"\\Programs" + b"\\Python"
    assert private_runtime_fragment not in payload
    json.dumps({"sha256": hashlib.sha256(payload).hexdigest()})
