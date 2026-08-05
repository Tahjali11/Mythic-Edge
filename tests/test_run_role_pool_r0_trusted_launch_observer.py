from __future__ import annotations

import ast
import ctypes
import hashlib
import importlib.util
import inspect
import shutil
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVER_PATH = REPO_ROOT / "tools/run_role_pool_r0_trusted_launch_observer.py"
OWNER_PATH = REPO_ROOT / "tools/check_role_pool_r0_offline_observation.py"


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


observer = _load("run_role_pool_r0_trusted_launch_observer", OBSERVER_PATH)
owner = _load("check_role_pool_r0_offline_observation_for_observer", OWNER_PATH)
_REAL_LOAD_OWNER_API = observer._load_owner_api
OWNER_TEST_PREDECESSOR_SHA256 = (
    "79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784"
)
OWNER_TEST_SUCCESSOR_SHA256 = (
    "c43b57072c99c166a9e7f578f67ecffecb2ee53c28e67c3c040e66cf33deb86a"
)
OWNER_TEST_FIXTURE_MARKER = b"synthetic-owner-test-predecessor-binding-v1\n"


@contextmanager
def _bounded_historical_owner_fixture() -> object:
    temporary = tempfile.TemporaryDirectory(prefix="mythic-edge-r0-owner-")
    root = Path(temporary.name)
    for relative_path in observer.FROZEN_BINDINGS:
        source = REPO_ROOT / relative_path
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    owner_test_path = root / observer.OWNER_TEST_PATH
    current_payload = owner_test_path.read_bytes()
    assert (
        hashlib.sha256(current_payload).hexdigest()
        == OWNER_TEST_SUCCESSOR_SHA256
    )
    owner_test_path.write_bytes(OWNER_TEST_FIXTURE_MARKER)
    real_stable_file_bytes = observer._stable_file_bytes
    real_hashlib = observer.hashlib

    class PathBoundPayload(bytes):
        relative_path: Path

        def __new__(
            cls,
            payload: bytes,
            relative_path: Path,
        ) -> object:
            value = super().__new__(cls, payload)
            value.relative_path = relative_path
            return value

    class FixedDigest:
        def hexdigest(self) -> str:
            return OWNER_TEST_PREDECESSOR_SHA256

    class BoundedHashlib:
        def sha256(self, payload: bytes = b"") -> object:
            if (
                isinstance(payload, PathBoundPayload)
                and payload.relative_path == observer.OWNER_TEST_PATH
                and bytes(payload) == OWNER_TEST_FIXTURE_MARKER
            ):
                return FixedDigest()
            return hashlib.sha256(payload)

        def __getattr__(self, name: str) -> object:
            return getattr(hashlib, name)

    def stable_file_bytes(path: Path) -> bytes:
        payload = real_stable_file_bytes(path)
        if path == owner_test_path:
            return PathBoundPayload(payload, observer.OWNER_TEST_PATH)
        return payload

    try:
        with (
            mock.patch.object(observer, "hashlib", BoundedHashlib()),
            mock.patch.object(
                observer,
                "_stable_file_bytes",
                stable_file_bytes,
            ),
        ):
            yield root, stable_file_bytes
    finally:
        temporary.cleanup()
        assert not root.exists()
        assert observer.hashlib is real_hashlib
        assert observer._stable_file_bytes is real_stable_file_bytes


def _bootstrap_packet() -> dict[str, object]:
    packet: dict[str, object] = {
        "schema_version": "trusted_owner_r0_offline_bootstrap_evidence.v1",
        "operation": "evaluate_r0_bootstrap_eligibility_read_only",
        "repository_id": owner.REPOSITORY_ID,
        "repository_name": "tahjali11/mythic-edge",
        "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/761",
        "base_commit": "10d4a4a79053fe33297a612599667d9b58bb4296",
        "profile_contract_sha256": owner.PROFILE_CONTRACT_SHA256,
        "app_server_contract_sha256": (
            "814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8"
        ),
        "r0_contract_sha256": (
            "07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82"
        ),
        "contract_binding_status": "exact",
        "stage3_manifest_file_count": 39,
        "stage3_manifest_byte_count": 5729,
        "stage3_manifest_sha256": (
            "cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06"
        ),
        "manifest_status": "exact",
        "source_tree_node_count": 41,
        "source_tree_file_count": 36,
        "source_tree_manifest_byte_count": 6495,
        "source_tree_sha256": owner.SOURCE_TREE_SHA256,
        "installed_tree_node_count": 41,
        "installed_tree_file_count": 36,
        "installed_tree_manifest_byte_count": 6495,
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
    return packet


def _validation_payload() -> bytes:
    return owner.canonical_bytes(_bootstrap_packet())


def _identity() -> object:
    return observer._FileIdentity(1, 2, 1024, 3, "a" * 64)


def _snapshot(**changes: object) -> object:
    values: dict[str, object] = {
        "exact": True,
        "repository_digest": "b" * 64,
        "installed_digest": "c" * 64,
        "generated_residue": frozenset(),
    }
    values.update(changes)
    return observer._EffectSnapshot(**values)


def _closes() -> tuple[object, ...]:
    names = (
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
    )
    return tuple(observer._CloseObservation(name, 1, True) for name in names)


def _evidence(descendants: int = 0, **changes: object) -> object:
    top_id = 101
    descendant_ids = tuple(range(202, 202 + descendants))
    events = (
        (observer._JobEvent("new", top_id),)
        + tuple(observer._JobEvent("new", value) for value in descendant_ids)
        + tuple(observer._JobEvent("exit", value) for value in reversed(descendant_ids))
        + (
            observer._JobEvent("exit", top_id),
            observer._JobEvent("active_zero", None),
        )
    )
    values: dict[str, object] = {
        "creation_attempt_count": 1,
        "top_level_created": True,
        "top_level_process_id": top_id,
        "job_assigned_at_creation": True,
        "job_handle_unique": True,
        "events": events,
        "cumulative_process_total": 1 + descendants,
        "active_process_count": 0,
        "exit_code": 0,
        "stdout": _validation_payload(),
        "stderr": b"",
        "stdout_eof": True,
        "stderr_eof": True,
        "stdout_overflow": False,
        "stderr_overflow": False,
        "top_level_identity_exact": None,
        "timed_out": False,
        "termination_requested": False,
        "termination_succeeded": None,
        "terminal_wait_succeeded": True,
        "close_observations": _closes(),
    }
    values.update(changes)
    return observer._LaunchEvidence(**values)


class FakeAdapter:
    def __init__(self, evidence: object | None = None) -> None:
        self.runtime = ("nt", "win32")
        self.launcher = observer._LauncherBinding(
            True,
            r"C:\Windows\py.exe",
            r"C:\Windows",
            _identity(),
        )
        self.snapshots = [_snapshot(), _snapshot()]
        self.audit = observer._AuditCounts(0, 0, 0, 0)
        self.evidence = _evidence() if evidence is None else evidence
        self.raise_on_launch: BaseException | None = None
        self.install_calls = 0
        self.bind_calls = 0
        self.launch_calls = 0
        self.requests: list[object] = []
        self.snapshot_calls = 0

    def runtime_identity(self) -> tuple[str, str]:
        return self.runtime

    def install_audit(self, repository_root: Path) -> None:
        assert repository_root == REPO_ROOT
        self.install_calls += 1

    def bind_installed_root(self, installed_root: Path) -> None:
        assert installed_root == REPO_ROOT
        self.bind_calls += 1

    def resolve_launcher(self) -> object:
        return self.launcher

    def snapshot_effects(
        self,
        repository_root: Path,
        installed_root: Path,
        owner_module: ModuleType,
    ) -> object:
        assert repository_root == REPO_ROOT
        assert installed_root == REPO_ROOT
        assert owner_module is owner
        value = self.snapshots[self.snapshot_calls]
        self.snapshot_calls += 1
        return value

    def launch_once(self, request: object) -> object:
        self.launch_calls += 1
        self.requests.append(request)
        if self.raise_on_launch is not None:
            raise self.raise_on_launch
        return self.evidence

    def audit_counts(self) -> object:
        return self.audit


class _FakeNativeKernel:
    def __init__(self, timeline: list[str]) -> None:
        self.timeline = timeline
        self.close_calls = 0
        self.termination_calls = 0
        self.wait_timeouts: list[int] = []
        self.cancel_next_close = False
        self.cancel_on_close_call: int | None = None

    def CreateJobObjectW(self, *_args: object) -> int:
        return 100

    def SetInformationJobObject(self, *_args: object) -> bool:
        return True

    def CreateIoCompletionPort(self, *_args: object) -> int:
        return 101

    def UpdateProcThreadAttribute(self, *_args: object) -> bool:
        return True

    def CreateProcessW(self, *_args: object) -> bool:
        self.timeline.append("create")
        information = ctypes.cast(
            _args[-1],
            ctypes.POINTER(observer._ProcessInformation),
        ).contents
        information.hProcess = 102
        information.hThread = 103
        information.dwProcessId = 104
        information.dwThreadId = 105
        return True

    def WaitForSingleObject(self, _handle: object, timeout: int) -> int:
        self.wait_timeouts.append(int(timeout))
        return observer.WAIT_OBJECT_0

    def TerminateJobObject(self, *_args: object) -> bool:
        self.termination_calls += 1
        return True

    def GetExitCodeProcess(self, _handle: object, code: object) -> bool:
        ctypes.cast(code, ctypes.POINTER(observer.wintypes.DWORD)).contents.value = 0
        return True

    def CloseHandle(self, _handle: object) -> bool:
        self.close_calls += 1
        if self.cancel_next_close or self.close_calls == self.cancel_on_close_call:
            self.cancel_next_close = False
            raise KeyboardInterrupt("private close cancellation detail")
        return True


class _FakeAttributeList:
    def __init__(self, _kernel32: object) -> None:
        self.attempt_count = 0
        self.succeeded = False

    def initialize(self) -> None:
        return None

    def close(self) -> bool:
        if not self.attempt_count:
            self.attempt_count = 1
            self.succeeded = True
        return self.succeeded

    def observation(self) -> object:
        return observer._CloseObservation(
            "attribute_list",
            self.attempt_count,
            self.succeeded,
        )


def _fake_native_boundary(
    monkeypatch: pytest.MonkeyPatch,
    *,
    cancel_first_event_drain: bool = False,
    cancel_first_cleanup_close: bool = False,
) -> tuple[object, _FakeNativeKernel, dict[str, int], list[str]]:
    timeline: list[str] = []
    kernel32 = _FakeNativeKernel(timeline)
    next_handle = iter(range(200, 206))
    calls = {"event_drains": 0, "pipe_drains": 0, "accounting": 0}

    def create_pipe(
        seen_kernel32: object,
        _security: object,
        read_name: str,
        write_name: str,
    ) -> tuple[object, object]:
        assert seen_kernel32 is kernel32
        return (
            observer._OwnedHandle(kernel32, read_name, next(next_handle)),
            observer._OwnedHandle(kernel32, write_name, next(next_handle)),
        )

    def drain_events(
        _kernel32: object,
        _completion_port: object,
        events: list[object],
    ) -> bool:
        calls["event_drains"] += 1
        if cancel_first_event_drain and calls["event_drains"] == 1:
            kernel32.cancel_next_close = cancel_first_cleanup_close
            raise KeyboardInterrupt("private cancellation detail")
        if not events:
            events.extend(
                (
                    observer._JobEvent("new", 104),
                    observer._JobEvent("exit", 104),
                    observer._JobEvent("active_zero", None),
                )
            )
        return True

    def drain_pipe(*_args: object) -> tuple[bool, bool, bool]:
        calls["pipe_drains"] += 1
        return True, False, True

    def query_accounting(*_args: object) -> tuple[int, int]:
        calls["accounting"] += 1
        return 1, 0

    monkeypatch.setattr(observer, "_OwnedAttributeList", _FakeAttributeList)
    monkeypatch.setattr(observer, "_create_pipe", create_pipe)
    monkeypatch.setattr(
        observer,
        "_make_parent_end_noninheritable",
        lambda *_args: None,
    )
    monkeypatch.setattr(observer, "_query_process_identity", lambda *_args: True)
    monkeypatch.setattr(observer, "_drain_events", drain_events)
    monkeypatch.setattr(observer, "_drain_pipe", drain_pipe)
    monkeypatch.setattr(observer, "_query_accounting", query_accounting)
    monkeypatch.setattr(observer.time, "sleep", lambda _seconds: None)
    request = observer._fixed_request(owner, REPO_ROOT, FakeAdapter().launcher)
    return request, kernel32, calls, timeline


@pytest.fixture(autouse=True)
def _operation_free_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    monkeypatch.setattr(observer, "_repository_root", lambda: REPO_ROOT)
    monkeypatch.setattr(observer, "_load_owner_api", lambda _root: owner)
    monkeypatch.setattr(observer, "_installed_root", lambda _owner, _root: REPO_ROOT)


def _run(adapter: FakeAdapter) -> bytes | str:
    return observer._run_observation_1(adapter)


def test_exact_contract_and_owner_bindings_are_frozen() -> None:
    expected = {
        observer.CONTRACT_PATH: observer.CONTRACT_SHA256,
        **observer.FROZEN_BINDINGS,
    }
    for relative_path, digest in expected.items():
        payload = (REPO_ROOT / relative_path).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if relative_path == observer.OWNER_TEST_PATH:
            assert digest == OWNER_TEST_PREDECESSOR_SHA256
            assert actual == OWNER_TEST_SUCCESSOR_SHA256
            assert actual != digest
        else:
            assert actual == digest

    with _bounded_historical_owner_fixture() as (fixture_root, _stable_bytes):
        for relative_path, digest in expected.items():
            payload = observer._stable_file_bytes(fixture_root / relative_path)
            assert observer.hashlib.sha256(payload).hexdigest() == digest


def test_owner_executes_only_the_verified_payload() -> None:
    source = OBSERVER_PATH.read_text(encoding="utf-8")
    assert "exec_module" not in source
    assert "verified_payloads[OWNER_PATH]" in source
    assert "compile(" in source
    assert "exec(code, module.__dict__)" in source
    with _bounded_historical_owner_fixture() as (fixture_root, _stable_bytes):
        loaded = _REAL_LOAD_OWNER_API(fixture_root)
        assert loaded.OBSERVATION_IDS == owner.OBSERVATION_IDS
        assert loaded.MAX_STDOUT_BYTES == owner.MAX_STDOUT_BYTES


def test_owner_path_replacement_cannot_change_verified_execution() -> None:
    with _bounded_historical_owner_fixture() as (fixture_root, stable_bytes):
        payloads = {
            relative_path: stable_bytes(fixture_root / relative_path)
            for relative_path in observer.FROZEN_BINDINGS
        }

        def verified_bytes(path: Path) -> bytes:
            return payloads[path.relative_to(fixture_root)]

        def reject_reopen(*_args: object, **_kwargs: object) -> object:
            raise AssertionError("verified owner path was reopened")

        with (
            mock.patch.object(observer, "_stable_file_bytes", verified_bytes),
            mock.patch.object(Path, "open", reject_reopen),
        ):
            loaded = _REAL_LOAD_OWNER_API(fixture_root)
        assert loaded.OBSERVATION_IDS == owner.OBSERVATION_IDS


def test_historical_owner_fixture_is_path_and_marker_bounded() -> None:
    with _bounded_historical_owner_fixture() as (fixture_root, stable_bytes):
        target = fixture_root / observer.OWNER_TEST_PATH
        marker = target.read_bytes()
        assert marker == OWNER_TEST_FIXTURE_MARKER
        assert hashlib.sha256(marker).hexdigest() not in {
            OWNER_TEST_PREDECESSOR_SHA256,
            OWNER_TEST_SUCCESSOR_SHA256,
        }
        assert (
            observer.hashlib.sha256(marker).hexdigest()
            == hashlib.sha256(marker).hexdigest()
        )

        bound_payload = stable_bytes(target)
        assert (
            observer.hashlib.sha256(bound_payload).hexdigest()
            == OWNER_TEST_PREDECESSOR_SHA256
        )

        wrong_path = fixture_root / "unlisted-owner-test-marker"
        wrong_path.write_bytes(marker)
        wrong_payload = stable_bytes(wrong_path)
        assert (
            observer.hashlib.sha256(wrong_payload).hexdigest()
            == hashlib.sha256(marker).hexdigest()
        )

        wrong_marker = marker + b"unexpected"
        target.write_bytes(wrong_marker)
        with pytest.raises(observer._ObserverError) as error:
            _REAL_LOAD_OWNER_API(fixture_root)
        assert error.value.status == "observation_binding_rejected"
        target.write_bytes(marker)


def test_current_owner_test_successor_rejects_before_adapter_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert (
        observer.FROZEN_BINDINGS[observer.OWNER_TEST_PATH]
        == OWNER_TEST_PREDECESSOR_SHA256
    )
    current_payload = (REPO_ROOT / observer.OWNER_TEST_PATH).read_bytes()
    assert (
        hashlib.sha256(current_payload).hexdigest()
        == OWNER_TEST_SUCCESSOR_SHA256
    )
    assert OWNER_TEST_SUCCESSOR_SHA256 != OWNER_TEST_PREDECESSOR_SHA256

    monkeypatch.setattr(observer, "_load_owner_api", _REAL_LOAD_OWNER_API)
    adapter = FakeAdapter()
    assert _run(adapter) == "observation_binding_rejected"
    assert adapter.install_calls == 0
    assert adapter.bind_calls == 0
    assert adapter.snapshot_calls == 0
    assert adapter.launch_calls == 0


def test_zero_argument_public_surface_and_fixed_request() -> None:
    assert tuple(inspect.signature(observer.main).parameters) == ("argv",)
    assert tuple(inspect.signature(observer._run_observation_1).parameters) == (
        "adapter",
    )
    adapter = FakeAdapter()
    result = _run(adapter)
    assert isinstance(result, bytes)
    assert adapter.install_calls == adapter.bind_calls == adapter.launch_calls == 1
    request = adapter.requests[0]
    assert request.tokens == (
        "py",
        "-3.13",
        "-B",
        "tools/check_role_pool_r0_offline_observation.py",
        owner.OBSERVATION_IDS[0],
    )
    assert request.application_path == r"C:\Windows\py.exe"
    assert request.repository_root == REPO_ROOT
    assert request.timeout_seconds == 120.0
    assert request.max_stdout_bytes == owner.MAX_STDOUT_BYTES
    assert request.max_stderr_bytes == owner.MAX_FAILURE_STDERR_BYTES
    assert request.environment == (
        ("PYTHONDONTWRITEBYTECODE", "1"),
        ("SYSTEMROOT", r"C:\Windows"),
    )
    forbidden = {
        "PATH",
        "PYTHONPATH",
        "CODEX_HOME",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "TOKEN",
        "CREDENTIAL",
    }
    assert forbidden.isdisjoint({name.upper() for name, _ in request.environment})


def test_arguments_reject_before_adapter_construction(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden() -> object:
        raise AssertionError("production adapter reached")

    monkeypatch.setattr(observer, "_WindowsTrustedLaunchAdapter", forbidden)
    assert observer.main(["unexpected"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "observation_sequence_rejected\n"


def test_non_windows_and_prelaunch_drift_never_launch() -> None:
    host = FakeAdapter()
    host.runtime = ("posix", "linux")
    assert _run(host) == "observation_host_rejected"
    assert host.launch_calls == 0

    baseline = FakeAdapter()
    baseline.snapshots[0] = _snapshot(exact=False)
    assert _run(baseline) == "observation_binding_rejected"
    assert baseline.launch_calls == 0

    launcher = FakeAdapter()
    launcher.launcher = replace(launcher.launcher, exact=False)
    assert _run(launcher) == "observation_binding_rejected"
    assert launcher.launch_calls == 0


def test_binding_failure_and_environment_drift_stop_before_launch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = FakeAdapter()

    def stale(_root: Path) -> ModuleType:
        raise observer._ObserverError("observation_binding_rejected")

    monkeypatch.setattr(observer, "_load_owner_api", stale)
    assert _run(adapter) == "observation_binding_rejected"
    assert adapter.launch_calls == 0

    with pytest.raises(observer._ObserverError):
        observer._environment_block((("PATH", "x\0y"),))
    with pytest.raises(observer._ObserverError):
        observer._environment_block((("A", "1"), ("a", "2")))


def test_launch_exception_is_single_attempt_and_never_retried() -> None:
    adapter = FakeAdapter()
    adapter.raise_on_launch = RuntimeError("private detail")
    assert _run(adapter) == "observation_launch_unknown"
    assert adapter.launch_calls == 1
    assert len(adapter.requests) == 1

    binding = FakeAdapter()
    binding.raise_on_launch = observer._ObserverError("observation_binding_rejected")
    assert _run(binding) == "observation_binding_rejected"
    assert binding.launch_calls == 1
    assert len(binding.requests) == 1


@pytest.mark.parametrize("descendants", [0, 1])
@pytest.mark.parametrize("identity_exact", [True, False, None])
def test_allowed_topologies_and_diagnostic_identity_seal(
    descendants: int,
    identity_exact: bool | None,
) -> None:
    adapter = FakeAdapter(
        _evidence(descendants, top_level_identity_exact=identity_exact)
    )
    result = _run(adapter)
    assert isinstance(result, bytes)
    receipt = owner.parse_receipt(result)
    assert receipt["sequence_position"] == 1
    assert receipt["observation_id"] == owner.OBSERVATION_IDS[0]
    assert receipt["descendant_process_count"] == descendants
    assert receipt["top_level_identity_exact"] is identity_exact


@pytest.mark.parametrize(
    ("evidence", "status"),
    [
        (_evidence(2), "observation_safety_boundary_failed"),
        (
            _evidence(events=(observer._JobEvent("new", 101),)),
            "observation_timeout_unknown",
        ),
        (
            _evidence(
                events=(
                    observer._JobEvent("new", 101),
                    observer._JobEvent("new", 101),
                )
            ),
            "observation_launch_unknown",
        ),
        (
            _evidence(cumulative_process_total=None),
            "observation_launch_unknown",
        ),
        (
            _evidence(terminal_wait_succeeded=False),
            "observation_timeout_unknown",
        ),
        (
            _evidence(timed_out=True),
            "observation_timeout_unknown",
        ),
        (
            _evidence(
                termination_requested=True,
                termination_succeeded=False,
            ),
            "observation_timeout_unknown",
        ),
    ],
)
def test_process_and_terminal_failures_use_existing_statuses(
    evidence: object,
    status: str,
) -> None:
    assert _run(FakeAdapter(evidence)) == status


@pytest.mark.parametrize(
    ("changes", "status"),
    [
        ({"stdout_overflow": True}, "observation_result_unknown"),
        ({"stderr_overflow": True}, "observation_result_unknown"),
        ({"stdout_eof": False}, "observation_timeout_unknown"),
        ({"stderr_eof": False}, "observation_timeout_unknown"),
        ({"exit_code": 4}, "observation_safety_boundary_failed"),
        ({"exit_code": 3}, "observation_result_unknown"),
        ({"exit_code": 2}, "observation_validation_failed"),
        ({"stderr": b"failure"}, "observation_validation_failed"),
        ({"stdout": b"{}"}, "observation_validation_failed"),
    ],
)
def test_stream_and_child_result_failures(
    changes: dict[str, object],
    status: str,
) -> None:
    assert _run(FakeAdapter(_evidence(**changes))) == status


@pytest.mark.parametrize(
    "changes",
    [
        {"stdout_eof": False},
        {"stderr_eof": False},
    ],
)
def test_cleanup_confirmation_requires_complete_output_drain(
    changes: dict[str, object],
) -> None:
    facts = observer._post_exit_facts(
        owner,
        _evidence(**changes),
        _snapshot(),
        _snapshot(),
        observer._AuditCounts(0, 0, 0, 0),
    )
    assert facts.output_complete is False
    assert facts.cleanup_confirmed is False


def test_close_failures_do_not_claim_cleanup() -> None:
    closes = list(_closes())
    closes[2] = replace(closes[2], succeeded=False)
    closes[5] = replace(closes[5], succeeded=False)
    assert _run(
        FakeAdapter(_evidence(close_observations=tuple(closes)))
    ) == "observation_timeout_unknown"
    assert all(value.attempt_count == 1 for value in closes)

    duplicate = _closes() + (_closes()[0],)
    assert _run(
        FakeAdapter(_evidence(close_observations=duplicate))
    ) == "observation_timeout_unknown"

    assert not observer._close_state_exact(
        (observer._CloseObservation("job", 1, True),)
    )
    for index in range(len(_closes())):
        incomplete = _closes()[:index] + _closes()[index + 1 :]
        assert _run(
            FakeAdapter(_evidence(close_observations=incomplete))
        ) == "observation_timeout_unknown"


def test_launcher_guard_blocks_replacement_before_create(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = observer._fixed_request(
        owner,
        REPO_ROOT,
        FakeAdapter().launcher,
    )

    class Guard:
        open = True

        def __init__(self) -> None:
            self.close_calls = 0

        def close(self) -> bool:
            self.close_calls += 1
            return True

    kernel32 = object()
    guard = Guard()
    evidence = _evidence()
    execute_calls: list[object] = []
    monkeypatch.setattr(observer, "_kernel32", lambda: kernel32)
    monkeypatch.setattr(observer, "_open_launcher_guard", lambda *_args: guard)
    monkeypatch.setattr(
        observer,
        "_stable_file_identity",
        lambda _path: request.launcher_identity,
    )

    def execute(
        seen_request: object,
        seen_kernel32: object,
        seen_guard: object,
    ) -> object:
        execute_calls.append((seen_request, seen_kernel32, seen_guard))
        return evidence

    monkeypatch.setattr(observer, "_execute_windows_once", execute)
    adapter = observer._WindowsTrustedLaunchAdapter()
    assert adapter.launch_once(request) is evidence
    assert execute_calls == [(request, kernel32, guard)]
    assert guard.close_calls == 0

    replacement_guard = Guard()
    monkeypatch.setattr(
        observer,
        "_open_launcher_guard",
        lambda *_args: replacement_guard,
    )
    monkeypatch.setattr(
        observer,
        "_stable_file_identity",
        lambda _path: replace(request.launcher_identity, size=2048),
    )
    replacement_adapter = observer._WindowsTrustedLaunchAdapter()
    with pytest.raises(observer._ObserverError) as error:
        replacement_adapter.launch_once(request)
    assert error.value.status == "observation_binding_rejected"
    assert replacement_guard.close_calls == 1
    assert len(execute_calls) == 1


@pytest.mark.parametrize(
    "audit",
    [
        observer._AuditCounts(1, 0, 0, 0),
        observer._AuditCounts(0, 1, 0, 0),
        observer._AuditCounts(0, 0, 1, 0),
        observer._AuditCounts(0, 0, 0, 1),
    ],
)
def test_each_observer_effect_count_is_derived_and_fails_closed(audit: object) -> None:
    adapter = FakeAdapter()
    adapter.audit = audit
    assert _run(adapter) == "observation_safety_boundary_failed"


@pytest.mark.parametrize(
    "event",
    [
        "os.rename",
        "os.renames",
        "os.replace",
        "os.link",
        "os.symlink",
        "shutil.copyfile",
        "shutil.move",
    ],
)
@pytest.mark.parametrize(
    ("destination_domain", "expected_counts"),
    [
        ("repository", observer._AuditCounts(0, 1, 0, 0)),
        ("installed", observer._AuditCounts(0, 0, 1, 0)),
        ("external", observer._AuditCounts(0, 0, 0, 1)),
    ],
)
def test_multi_path_mutations_are_counted_once_by_destination_domain(
    event: str,
    destination_domain: str,
    expected_counts: object,
    tmp_path: Path,
) -> None:
    installed_root = tmp_path / "installed"
    external_root = tmp_path / "external"
    counter = observer._AuditCounter(REPO_ROOT)
    counter.bind_installed_root(installed_root)
    destinations = {
        "repository": REPO_ROOT / "synthetic-destination",
        "installed": installed_root / "synthetic-destination",
        "external": external_root / "synthetic-destination",
    }
    source = (
        REPO_ROOT / "synthetic-source"
        if destination_domain == "external"
        else external_root / "synthetic-source"
    )

    with pytest.raises(observer._SafetyEffect):
        counter(event, (source, destinations[destination_domain]))

    assert counter.snapshot() == expected_counts


def test_manifest_drift_and_new_residue_fail_closed() -> None:
    repository = FakeAdapter()
    repository.snapshots[1] = _snapshot(repository_digest="d" * 64)
    assert _run(repository) == "observation_safety_boundary_failed"

    installed = FakeAdapter()
    installed.snapshots[1] = _snapshot(installed_digest="e" * 64)
    assert _run(installed) == "observation_safety_boundary_failed"

    residue = FakeAdapter()
    residue.snapshots[1] = _snapshot(
        generated_residue=frozenset({"__pycache__/new.pyc"})
    )
    assert _run(residue) == "observation_safety_boundary_failed"

    unknown = FakeAdapter()
    unknown.snapshots[1] = _snapshot(exact=False)
    assert _run(unknown) == "observation_timeout_unknown"


def test_owner_parser_and_sealer_are_used_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parser_calls = 0
    sealer_calls = 0
    real_parser = owner.parse_validation_payload
    real_sealer = owner.seal_proportionate_observation_receipt

    def parser(payload: bytes) -> dict[str, object]:
        nonlocal parser_calls
        parser_calls += 1
        return real_parser(payload)

    def sealer(payload: bytes, facts: object, position: int) -> bytes | str:
        nonlocal sealer_calls
        sealer_calls += 1
        return real_sealer(payload, facts, position)

    monkeypatch.setattr(owner, "parse_validation_payload", parser)
    monkeypatch.setattr(owner, "seal_proportionate_observation_receipt", sealer)
    assert isinstance(_run(FakeAdapter()), bytes)
    assert parser_calls == 1
    assert sealer_calls == 1


def test_sealer_status_exception_and_receipt_mismatch_never_emit_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        owner,
        "seal_proportionate_observation_receipt",
        lambda *_args: "observation_receipt_sealing_failed",
    )
    assert _run(FakeAdapter()) == "observation_receipt_sealing_failed"

    monkeypatch.setattr(
        owner,
        "seal_proportionate_observation_receipt",
        lambda *_args: b"{}",
    )
    assert _run(FakeAdapter()) == "observation_receipt_sealing_failed"

    def explode(*_args: object) -> bytes:
        raise RuntimeError("private detail")

    monkeypatch.setattr(owner, "seal_proportionate_observation_receipt", explode)
    assert _run(FakeAdapter()) == "observation_result_unknown"


def test_main_emits_only_public_safe_result(
    monkeypatch: pytest.MonkeyPatch,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    adapter = FakeAdapter()
    monkeypatch.setattr(observer, "_WindowsTrustedLaunchAdapter", lambda: adapter)
    assert observer.main([]) == 0
    captured = capsysbinary.readouterr()
    assert captured.err == b""
    assert owner.parse_receipt(captured.out)["sequence_position"] == 1

    monkeypatch.setattr(
        observer,
        "_run_observation_1",
        lambda _adapter: "observation_timeout_unknown",
    )
    assert observer.main([]) == 3
    captured = capsysbinary.readouterr()
    assert captured.out == b""
    assert captured.err == b"observation_timeout_unknown\n"


def test_deadline_starts_immediately_before_the_create_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, kernel32, _calls, timeline = _fake_native_boundary(monkeypatch)

    def monotonic() -> float:
        timeline.append("clock")
        return 0.0

    monkeypatch.setattr(observer.time, "monotonic", monotonic)
    evidence = observer._execute_windows_once(
        request,
        kernel32,
        observer._OwnedHandle(kernel32, "launcher_guard", 300),
    )

    assert timeline[:2] == ["clock", "create"]
    assert evidence.creation_attempt_count == 1


def test_completed_state_after_deadline_is_still_timed_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, kernel32, _calls, _timeline = _fake_native_boundary(monkeypatch)
    ticks = iter((0.0, request.timeout_seconds + 1.0))
    monkeypatch.setattr(observer.time, "monotonic", lambda: next(ticks))

    evidence = observer._execute_windows_once(
        request,
        kernel32,
        observer._OwnedHandle(kernel32, "launcher_guard", 300),
    )

    assert evidence.timed_out is True
    assert evidence.termination_requested is True
    assert kernel32.termination_calls == 1


@pytest.mark.parametrize(
    ("cancel_on_close_call", "top_level_created", "termination_calls"),
    [(1, False, 0), (2, True, 1)],
)
def test_setup_close_cancellation_routes_to_owned_reconciliation(
    monkeypatch: pytest.MonkeyPatch,
    cancel_on_close_call: int,
    top_level_created: bool,
    termination_calls: int,
) -> None:
    request, kernel32, _calls, timeline = _fake_native_boundary(monkeypatch)
    kernel32.cancel_on_close_call = cancel_on_close_call
    monkeypatch.setattr(observer.time, "monotonic", lambda: 0.0)

    evidence = observer._execute_windows_once(
        request,
        kernel32,
        observer._OwnedHandle(kernel32, "launcher_guard", 300),
    )

    assert evidence.top_level_created is top_level_created
    assert evidence.creation_attempt_count == int(top_level_created)
    assert ("create" in timeline) is top_level_created
    assert kernel32.termination_calls == termination_calls
    assert all(item.attempt_count == 1 for item in evidence.close_observations)
    assert sum(not item.succeeded for item in evidence.close_observations) == 1


def test_cancellation_reconciles_owned_resources_before_returning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, kernel32, calls, _timeline = _fake_native_boundary(
        monkeypatch,
        cancel_first_event_drain=True,
        cancel_first_cleanup_close=True,
    )
    monkeypatch.setattr(observer.time, "monotonic", lambda: 0.0)

    try:
        evidence = observer._execute_windows_once(
            request,
            kernel32,
            observer._OwnedHandle(kernel32, "launcher_guard", 300),
        )
    except BaseException as exc:
        pytest.fail(f"cancellation escaped the owned cleanup boundary: {type(exc)}")

    assert kernel32.termination_calls == 1
    assert int(observer.TERMINATION_GRACE_SECONDS * 1000) in kernel32.wait_timeouts
    assert calls["event_drains"] >= 2
    assert calls["pipe_drains"] == 2
    assert calls["accounting"] == 1
    assert evidence.active_process_count == 0
    assert evidence.stdout_eof is True
    assert evidence.stderr_eof is True
    assert all(item.attempt_count == 1 for item in evidence.close_observations)
    assert sum(not item.succeeded for item in evidence.close_observations) == 1
    facts = observer._post_exit_facts(
        owner,
        evidence,
        _snapshot(),
        _snapshot(),
        observer._AuditCounts(0, 0, 0, 0),
    )
    assert facts.cleanup_confirmed is False
    assert owner._post_exit_status(facts) in observer._CLOSED_FAILURE_STATUSES


def test_main_converts_cancellation_to_fixed_public_status(
    monkeypatch: pytest.MonkeyPatch,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    def cancel(_adapter: object) -> bytes | str:
        raise KeyboardInterrupt("private cancellation detail")

    monkeypatch.setattr(observer, "_run_observation_1", cancel)
    try:
        result = observer.main([])
    except BaseException as exc:
        pytest.fail(f"public cancellation escaped: {type(exc)}")

    captured = capsysbinary.readouterr()
    assert result == 3
    assert captured.out == b""
    assert captured.err == b"observation_result_unknown\n"


def test_native_source_has_one_fixed_create_and_no_fallback_or_old_dependency() -> None:
    source = OBSERVER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    create_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "CreateProcessW"
    ]
    assert len(create_calls) == 1
    assert "PROC_THREAD_ATTRIBUTE_JOB_LIST" in source
    assert "PROC_THREAD_ATTRIBUTE_HANDLE_LIST" in source
    assert "ActiveProcessLimit = 2" in source
    assert "CreateFileW" in source
    assert "FILE_SHARE_WRITE" not in source
    assert "FILE_SHARE_DELETE" not in source
    assert "JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE" in source
    assert "AssignProcessToJobObject" not in source
    assert "DuplicateHandle" not in source
    assert "def _tree_snapshot" not in source
    assert "os.walk" not in source
    assert "_owned_state_snapshot" in source
    assert "_tree_observations" in source
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert "subprocess" not in imports
    assert "shell=" not in source
    assert "issue 780" not in source.lower()
    assert "issue 795" not in source.lower()
    assert "executor_network_operation_count=0" not in source
    assert "repository_write_count=0" not in source
    assert "installed_write_count=0" not in source
    assert "external_effect_count=0" not in source
    assert "generated_residue_count=0" not in source


def test_no_publication_authority_or_observation_two_surface_exists() -> None:
    source = OBSERVER_PATH.read_text(encoding="utf-8")
    forbidden = (
        "github",
        "publish_receipt",
        "create_comment",
        "release_state_write",
        "registry_write",
        "observation_2",
        "r1_authorized",
        "stage4_authorized",
        "live_ready = true",
    )
    lowered = source.lower()
    assert all(value not in lowered for value in forbidden)


def test_existing_owner_known_answers_remain_exact() -> None:
    owner._validate_known_answers()
    payload = _validation_payload()
    assert owner.parse_validation_payload(payload) == _bootstrap_packet()
    for receipts in owner.EXPECTED_RECEIPTS:
        for receipt in receipts:
            encoded = owner.canonical_bytes(receipt)
            assert owner.parse_receipt(encoded) == receipt
