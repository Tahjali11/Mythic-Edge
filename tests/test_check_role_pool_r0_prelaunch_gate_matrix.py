from __future__ import annotations

import ast
import copy
import importlib.util
import json
import sys
from itertools import product
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_role_pool_r0_prelaunch_gate_matrix.py"
SPEC = importlib.util.spec_from_file_location("r0_prelaunch_gate_matrix", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
matrix = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = matrix
SPEC.loader.exec_module(matrix)

EXPECTED_GATE_REGISTRY = (
    (
        "PLG-01-runtime-bytecode",
        (),
        "probe_runtime_bytecode",
        "runtime_or_bytecode_rejected",
    ),
    (
        "PLG-02-repository-root",
        (),
        "probe_repository_root",
        "repository_root_rejected",
    ),
    (
        "PLG-03-frozen-owner-api",
        ("PLG-02-repository-root",),
        "probe_frozen_owner_api",
        "frozen_owner_api_rejected",
    ),
    (
        "PLG-04-installed-release-state",
        ("PLG-02-repository-root", "PLG-03-frozen-owner-api"),
        "probe_installed_release_state",
        "installed_release_state_rejected",
    ),
    (
        "PLG-05-prelaunch-effect-snapshot",
        (
            "PLG-02-repository-root",
            "PLG-03-frozen-owner-api",
            "PLG-04-installed-release-state",
        ),
        "probe_prelaunch_effect_snapshot",
        "prelaunch_effect_snapshot_rejected",
    ),
    (
        "PLG-06-fixed-launcher-identity",
        ("PLG-01-runtime-bytecode",),
        "probe_fixed_launcher_identity",
        "fixed_launcher_identity_rejected",
    ),
    (
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
    (
        "PLG-08-launcher-guard-revalidation",
        (
            "PLG-01-runtime-bytecode",
            "PLG-06-fixed-launcher-identity",
            "PLG-07-fixed-request-prerequisites",
        ),
        "probe_launcher_guard_revalidation",
        "launcher_guard_revalidation_rejected",
    ),
    (
        "PLG-09-exact-ready",
        (
            "PLG-01-runtime-bytecode",
            "PLG-02-repository-root",
            "PLG-03-frozen-owner-api",
            "PLG-04-installed-release-state",
            "PLG-05-prelaunch-effect-snapshot",
            "PLG-06-fixed-launcher-identity",
            "PLG-07-fixed-request-prerequisites",
            "PLG-08-launcher-guard-revalidation",
        ),
        None,
        None,
    ),
)
GATE_IDS = tuple(row[0] for row in EXPECTED_GATE_REGISTRY)
DEPENDENCIES_BY_GATE = {
    gate_id: dependencies
    for gate_id, dependencies, _method_name, _reason in EXPECTED_GATE_REGISTRY
}
METHOD_BY_GATE = {
    gate_id: method_name
    for gate_id, _dependencies, method_name, _reason in EXPECTED_GATE_REGISTRY
    if method_name is not None
}
REASON_BY_GATE = {
    gate_id: reason
    for gate_id, _dependencies, _method_name, reason in EXPECTED_GATE_REGISTRY
    if reason is not None
}


class _ExplodingStdin:
    def read(self, *_args: object, **_kwargs: object) -> str:
        raise AssertionError("stdin_must_not_be_read")


class FakeAdapter:
    def __init__(self, actions: dict[str, str] | None = None) -> None:
        self.actions = actions or {}
        self.calls: list[str] = []
        self.guard_open_count = 0
        self.guard_close_count = 0

    def _probe(self, gate_id: str) -> object:
        self.calls.append(gate_id)
        action = self.actions.get(gate_id, "pass")
        if action == "reject":
            raise matrix._ProbeRejected
        if action == "unknown":
            raise matrix._ProbeUnknown
        if action == "cleanup":
            raise matrix._ProbeUnknown("cleanup_unconfirmed")
        if action.startswith("boundary:"):
            raise matrix._BoundaryViolation(action)
        if action == "unexpected":
            raise RuntimeError("PRIVATE_FAKE_EXCEPTION")
        return f"PRIVATE_PAYLOAD::{gate_id}"

    def probe_runtime_bytecode(self) -> object:
        return self._probe(GATE_IDS[0])

    def probe_repository_root(self) -> object:
        return self._probe(GATE_IDS[1])

    def probe_frozen_owner_api(self, repository_root: object) -> object:
        assert repository_root == f"PRIVATE_PAYLOAD::{GATE_IDS[1]}"
        return self._probe(GATE_IDS[2])

    def probe_installed_release_state(
        self,
        repository_root: object,
        owner_api: object,
    ) -> object:
        assert repository_root == f"PRIVATE_PAYLOAD::{GATE_IDS[1]}"
        assert owner_api == f"PRIVATE_PAYLOAD::{GATE_IDS[2]}"
        return self._probe(GATE_IDS[3])

    def probe_prelaunch_effect_snapshot(
        self,
        repository_root: object,
        owner_api: object,
        installed_root: object,
    ) -> object:
        assert repository_root == f"PRIVATE_PAYLOAD::{GATE_IDS[1]}"
        assert owner_api == f"PRIVATE_PAYLOAD::{GATE_IDS[2]}"
        assert installed_root == f"PRIVATE_PAYLOAD::{GATE_IDS[3]}"
        return self._probe(GATE_IDS[4])

    def probe_fixed_launcher_identity(self) -> object:
        return self._probe(GATE_IDS[5])

    def probe_fixed_request_prerequisites(
        self,
        repository_root: object,
        owner_api: object,
        launcher: object,
    ) -> object:
        assert repository_root == f"PRIVATE_PAYLOAD::{GATE_IDS[1]}"
        assert owner_api == f"PRIVATE_PAYLOAD::{GATE_IDS[2]}"
        assert launcher == f"PRIVATE_PAYLOAD::{GATE_IDS[5]}"
        return self._probe(GATE_IDS[6])

    def probe_launcher_guard_revalidation(self, launcher: object) -> object:
        assert launcher == f"PRIVATE_PAYLOAD::{GATE_IDS[5]}"
        self.guard_open_count += 1
        self.guard_close_count += 1
        return self._probe(GATE_IDS[7])


class _SyntheticGuard:
    def __init__(
        self,
        *,
        close_result: bool = True,
        close_error: BaseException | None = None,
    ) -> None:
        self.close_result = close_result
        self.close_error = close_error
        self.attempt_count = 0

    def close(self) -> bool:
        self.attempt_count += 1
        if self.close_error is not None:
            raise self.close_error
        return self.close_result


class _SyntheticAuditCounter:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.installed_root: Path | None = None

    def __call__(self, _event: str, _args: tuple[object, ...]) -> None:
        pass

    def bind_installed_root(self, installed_root: Path) -> None:
        self.installed_root = installed_root


def _production_audit_probe() -> tuple[object, Path, ModuleType, list[Path]]:
    class SafetyEffect(RuntimeError):
        pass

    class ObserverError(RuntimeError):
        pass

    repository_root = Path("synthetic-repository")
    installed_root = Path("synthetic-installed")
    installed_calls: list[Path] = []
    owner = ModuleType("synthetic_owner")
    observer = ModuleType("synthetic_audit_observer")
    observer._SafetyEffect = SafetyEffect
    observer._ObserverError = ObserverError
    observer._AuditCounter = _SyntheticAuditCounter

    def installed_root_probe(_owner: ModuleType, root: Path) -> Path:
        installed_calls.append(root)
        return installed_root

    observer._installed_root = installed_root_probe
    adapter = object.__new__(matrix._ProductionPrelaunchGateAdapter)
    adapter._observer = observer
    adapter._audit = None
    return adapter, repository_root, owner, installed_calls


def _synthetic_audit_runtime(
    monkeypatch: pytest.MonkeyPatch,
    *,
    reject_registration: bool = False,
) -> tuple[list[object], list[str]]:
    hooks: list[object] = []
    events: list[str] = []

    if reject_registration:
        def reject_addaudithook(event: str, _args: tuple[object, ...]) -> None:
            if event == "sys.addaudithook":
                raise RuntimeError("PRIVATE_AUDIT_REJECTION")

        hooks.append(reject_addaudithook)

    def addaudithook(hook: object) -> None:
        for existing in tuple(hooks):
            try:
                existing("sys.addaudithook", ())
            except RuntimeError:
                return
        hooks.append(hook)

    def audit(event: str, *args: object) -> None:
        events.append(event)
        for hook in tuple(hooks):
            hook(event, args)

    monkeypatch.setattr(matrix.sys, "addaudithook", addaudithook)
    monkeypatch.setattr(matrix.sys, "audit", audit)
    return hooks, events


def _production_guard_probe(
    *,
    identity_matches: bool = True,
    close_result: bool = True,
    close_error: BaseException | None = None,
) -> tuple[object, object, _SyntheticGuard]:
    expected_identity = object()
    observed_identity = expected_identity if identity_matches else object()

    class Launcher:
        application_path = "synthetic-launcher"
        identity = expected_identity

    guard = _SyntheticGuard(
        close_result=close_result,
        close_error=close_error,
    )
    observer = ModuleType("synthetic_guard_observer")
    observer._LauncherBinding = Launcher
    observer._kernel32 = lambda: object()
    observer._open_launcher_guard = lambda _kernel32, _path: guard
    observer._stable_file_identity = lambda _path: observed_identity

    adapter = object.__new__(matrix._ProductionPrelaunchGateAdapter)
    adapter._observer = observer
    adapter._audit = None
    return adapter, Launcher(), guard


def _decode(payload: bytes) -> dict[str, object]:
    assert payload.endswith(b"\n")
    assert not payload.endswith(b"\n\n")
    return json.loads(payload)


def _rows(payload: bytes) -> list[dict[str, object]]:
    value = _decode(payload)["gates"]
    assert type(value) is list
    return value


def _row(payload: bytes, gate_id: str) -> dict[str, object]:
    return next(item for item in _rows(payload) if item["gate_id"] == gate_id)


def _aggregate_from(payload: bytes) -> dict[str, object]:
    return _decode(payload)


def test_contract_bindings_and_closed_registry_are_exact() -> None:
    assert matrix.MATRIX_CONTRACT_SHA256 == (
        "58e553452602a991950eaa02ff20ac26c45cee2dcf891e069e45ea9e300f0840"
    )
    assert len(matrix.FROZEN_BINDINGS) == 7
    actual_registry = tuple(
        (
            spec.gate_id,
            spec.dependencies,
            spec.method_name,
            spec.ordinary_reason,
        )
        for spec in matrix.GATE_REGISTRY
    )
    assert actual_registry == EXPECTED_GATE_REGISTRY


def test_all_pass_is_canonical_exact_ready_and_byte_identical() -> None:
    first = matrix.evaluate_prelaunch_gate_matrix(FakeAdapter())
    second = matrix.evaluate_prelaunch_gate_matrix(FakeAdapter())
    assert first == second
    assert b" " not in first
    aggregate = _aggregate_from(first)
    assert tuple(aggregate) == matrix.AGGREGATE_FIELDS
    assert aggregate["aggregate_result"] == "exact_ready"
    assert aggregate["minimum_lifecycle_state"] == matrix.MINIMUM_COMPLETE_STATE
    rows = aggregate["gates"]
    assert type(rows) is list
    assert [tuple(row) for row in rows] == [matrix.GATE_FIELDS] * 9
    assert [row["gate_id"] for row in rows] == list(GATE_IDS)
    assert all(row["result"] == "passed" for row in rows)
    assert rows[-1]["reason_code"] == "all_prelaunch_gates_exact"


def test_selector_exhaustively_partitions_all_probe_vectors() -> None:
    counts = {
        "exact_ready": 0,
        "not_ready": 0,
        "indeterminate_failed_closed": 0,
    }
    for actions in product(("pass", "reject", "unknown"), repeat=8):
        adapter = FakeAdapter(dict(zip(GATE_IDS[:8], actions, strict=True)))
        aggregate = _aggregate_from(
            matrix.evaluate_prelaunch_gate_matrix(adapter)
        )
        counts[aggregate["aggregate_result"]] += 1
    assert counts == {
        "exact_ready": 1,
        "not_ready": 1824,
        "indeterminate_failed_closed": 4736,
    }


@pytest.mark.parametrize("gate_id", GATE_IDS[:8])
def test_each_ordinary_failure_uses_its_reason_and_blocks_only_dependents(
    gate_id: str,
) -> None:
    adapter = FakeAdapter({gate_id: "reject"})
    payload = matrix.evaluate_prelaunch_gate_matrix(adapter)
    aggregate = _aggregate_from(payload)
    assert aggregate["aggregate_result"] == "not_ready"
    assert _row(payload, gate_id) == {
        "gate_id": gate_id,
        "result": "failed",
        "reason_code": REASON_BY_GATE[gate_id],
        "dependencies": list(DEPENDENCIES_BY_GATE[gate_id]),
        "minimum_lifecycle_state": matrix.EVALUATED_STATE,
    }
    for row in _rows(payload)[:-1]:
        method_gate = str(row["gate_id"])
        if row["result"] == "blocked":
            assert method_gate not in adapter.calls
        else:
            assert adapter.calls.count(method_gate) == 1
    assert _rows(payload)[-1]["result"] == "blocked"


@pytest.mark.parametrize("gate_id", GATE_IDS[:8])
def test_unavailable_and_ambiguous_probes_fail_closed(gate_id: str) -> None:
    adapter = FakeAdapter({gate_id: "unexpected"})
    payload = matrix.evaluate_prelaunch_gate_matrix(adapter)
    assert _aggregate_from(payload)["aggregate_result"] == "indeterminate_failed_closed"
    row = _row(payload, gate_id)
    assert row["result"] == "unknown_failed_closed"
    assert row["reason_code"] == "probe_unavailable_or_ambiguous"
    assert b"PRIVATE_FAKE_EXCEPTION" not in payload


def test_multiple_independent_failures_remain_in_registry_order() -> None:
    adapter = FakeAdapter(
        {
            "PLG-02-repository-root": "reject",
            "PLG-06-fixed-launcher-identity": "reject",
        }
    )
    payload = matrix.evaluate_prelaunch_gate_matrix(adapter)
    failed = [row["gate_id"] for row in _rows(payload) if row["result"] == "failed"]
    assert failed == ["PLG-02-repository-root", "PLG-06-fixed-launcher-identity"]
    assert adapter.calls[:3] == [
        "PLG-01-runtime-bytecode",
        "PLG-02-repository-root",
        "PLG-06-fixed-launcher-identity",
    ]


def test_dependency_blocked_methods_are_never_called() -> None:
    adapter = FakeAdapter({"PLG-02-repository-root": "unknown"})
    payload = matrix.evaluate_prelaunch_gate_matrix(adapter)
    blocked = {
        row["gate_id"] for row in _rows(payload) if row["result"] == "blocked"
    }
    assert blocked == {
        "PLG-03-frozen-owner-api",
        "PLG-04-installed-release-state",
        "PLG-05-prelaunch-effect-snapshot",
        "PLG-07-fixed-request-prerequisites",
        "PLG-08-launcher-guard-revalidation",
        "PLG-09-exact-ready",
    }
    assert blocked.isdisjoint(adapter.calls)
    assert "PLG-06-fixed-launcher-identity" in adapter.calls


@pytest.mark.parametrize("effect", ("process", "network", "environment", "write"))
def test_operation_boundary_violation_emits_no_aggregate(
    effect: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    adapter = FakeAdapter({"PLG-02-repository-root": f"boundary:{effect}"})
    monkeypatch.setattr(matrix, "_ProductionPrelaunchGateAdapter", lambda: adapter)
    assert matrix.main([]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == matrix.FAILURE_LINE.decode("ascii")
    assert adapter.calls == [
        "PLG-01-runtime-bytecode",
        "PLG-02-repository-root",
    ]


@pytest.mark.parametrize("action", ("pass", "reject", "unknown", "cleanup"))
def test_launcher_guard_has_one_open_and_one_close_on_owned_routes(action: str) -> None:
    adapter = FakeAdapter({"PLG-08-launcher-guard-revalidation": action})
    payload = matrix.evaluate_prelaunch_gate_matrix(adapter)
    assert adapter.guard_open_count == 1
    assert adapter.guard_close_count == 1
    row = _row(payload, "PLG-08-launcher-guard-revalidation")
    if action == "cleanup":
        assert row["result"] == "unknown_failed_closed"
        assert row["reason_code"] == "cleanup_unconfirmed"


@pytest.mark.parametrize("identity_matches", (True, False))
def test_production_launcher_guard_closes_once_on_owned_results(
    identity_matches: bool,
) -> None:
    adapter, launcher, guard = _production_guard_probe(
        identity_matches=identity_matches
    )

    if identity_matches:
        assert adapter.probe_launcher_guard_revalidation(launcher) is True
    else:
        with pytest.raises(matrix._ProbeRejected):
            adapter.probe_launcher_guard_revalidation(launcher)

    assert guard.attempt_count == 1


@pytest.mark.parametrize(
    ("close_result", "close_error"),
    (
        (False, None),
        (True, KeyboardInterrupt("PRIVATE_CLOSE_FAILURE")),
    ),
)
def test_production_launcher_guard_cleanup_failure_is_unknown(
    close_result: bool,
    close_error: BaseException | None,
) -> None:
    adapter, launcher, guard = _production_guard_probe(
        close_result=close_result,
        close_error=close_error,
    )

    with pytest.raises(matrix._ProbeUnknown) as caught:
        adapter.probe_launcher_guard_revalidation(launcher)

    assert caught.value.reason_code == "cleanup_unconfirmed"
    assert guard.attempt_count == 1


def test_production_audit_hook_registration_is_positively_observed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter, repository_root, owner, installed_calls = _production_audit_probe()
    hooks, events = _synthetic_audit_runtime(monkeypatch)

    result = adapter.probe_installed_release_state(repository_root, owner)

    assert result == Path("synthetic-installed")
    assert len(hooks) == 1
    assert events == [matrix._AUDIT_REGISTRATION_EVENT]
    assert isinstance(adapter._audit, _SyntheticAuditCounter)
    assert adapter._audit.installed_root == result
    assert installed_calls == [repository_root]


def test_preexisting_hook_rejection_suppresses_registration_and_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter, repository_root, owner, installed_calls = _production_audit_probe()
    hooks, events = _synthetic_audit_runtime(
        monkeypatch,
        reject_registration=True,
    )

    with pytest.raises(matrix._ProbeUnknown):
        adapter.probe_installed_release_state(repository_root, owner)

    assert len(hooks) == 1
    assert events == [matrix._AUDIT_REGISTRATION_EVENT]
    assert adapter._audit is None
    assert installed_calls == []


def test_unknown_precedence_over_ordinary_failures() -> None:
    payload = matrix.evaluate_prelaunch_gate_matrix(
        FakeAdapter(
            {
                "PLG-02-repository-root": "reject",
                "PLG-06-fixed-launcher-identity": "unknown",
            }
        )
    )
    assert _aggregate_from(payload)["aggregate_result"] == "indeterminate_failed_closed"


def test_malformed_internal_rows_and_aggregate_are_rejected() -> None:
    exact = _aggregate_from(matrix.evaluate_prelaunch_gate_matrix(FakeAdapter()))
    mutations: list[dict[str, object]] = []

    extra = copy.deepcopy(exact)
    extra["gates"][0]["extra"] = True
    mutations.append(extra)

    reordered = copy.deepcopy(exact)
    row = reordered["gates"][0]
    reordered["gates"][0] = {key: row[key] for key in reversed(row)}
    mutations.append(reordered)

    duplicate = copy.deepcopy(exact)
    duplicate["gates"][1] = copy.deepcopy(duplicate["gates"][0])
    mutations.append(duplicate)

    wrong_order = copy.deepcopy(exact)
    wrong_order["gates"][0], wrong_order["gates"][1] = (
        wrong_order["gates"][1],
        wrong_order["gates"][0],
    )
    mutations.append(wrong_order)

    invalid_pair = copy.deepcopy(exact)
    invalid_pair["gates"][0]["reason_code"] = "dependency_not_passed"
    mutations.append(invalid_pair)

    wrong_aggregate = copy.deepcopy(exact)
    wrong_aggregate["aggregate_result"] = "not_ready"
    mutations.append(wrong_aggregate)

    for aggregate in mutations:
        with pytest.raises(matrix._MatrixFailure):
            matrix._render_aggregate(aggregate)


def test_render_error_emits_only_fixed_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(matrix, "_ProductionPrelaunchGateAdapter", FakeAdapter)
    monkeypatch.setattr(matrix.json, "dumps", lambda *_args, **_kwargs: 1 / 0)
    assert matrix.main([]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == matrix.FAILURE_LINE.decode("ascii")


def test_arguments_reject_before_adapter_construction(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden() -> object:
        raise AssertionError("production_adapter_must_not_be_constructed")

    monkeypatch.setattr(matrix, "_ProductionPrelaunchGateAdapter", forbidden)
    assert matrix.main(["caller-selected"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == matrix.FAILURE_LINE.decode("ascii")


def test_main_uses_fake_adapter_and_never_reads_stdin(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(matrix, "_ProductionPrelaunchGateAdapter", FakeAdapter)
    monkeypatch.setattr(matrix.sys, "stdin", _ExplodingStdin())
    assert matrix.main([]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert json.loads(captured.out)["aggregate_result"] == "exact_ready"


def test_private_payloads_errors_and_machine_values_never_echo() -> None:
    private_values = (
        "PRIVATE_PAYLOAD",
        "PRIVATE_FAKE_EXCEPTION",
        "C:\\private\\launcher.exe",
        "secret-token",
        "S-1-5-private",
        "handle=1234",
        "--private-command",
        "ENVIRONMENT_VALUE",
        "a" * 64,
    )
    payload = matrix.evaluate_prelaunch_gate_matrix(
        FakeAdapter({"PLG-06-fixed-launcher-identity": "unexpected"})
    )
    text = payload.decode("ascii")
    assert all(value not in text for value in private_values)


def test_result_is_not_an_observation_receipt_or_r0_acceptance() -> None:
    result = _aggregate_from(matrix.evaluate_prelaunch_gate_matrix(FakeAdapter()))
    assert result["schema_version"] != "trusted_owner_r0_offline_observation_receipt.v2"
    assert "receipt_sha256" not in result
    assert "accepted_for_independent_review" not in result
    assert "authority_flags" not in result
    assert result["aggregate_result"] == "exact_ready"
    assert result["minimum_lifecycle_state"] == (
        "prelaunch_matrix_complete_child_creation_not_entered"
    )


def test_source_has_no_process_observation_authority_or_publication_surface() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    called_names = {
        node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, (ast.Attribute, ast.Name))
    }
    assert called_names.isdisjoint(
        {
            "CreateProcessW",
            "Popen",
            "system",
            "startfile",
            "spawnl",
            "spawnle",
            "spawnlp",
            "spawnlpe",
            "spawnv",
            "spawnve",
            "spawnvp",
            "spawnvpe",
        }
    )
    for forbidden in (
        "subprocess",
        "launch_once",
        "_run_observation_1",
        "CreateProcessW",
        "publish_receipt",
        "consume_one_r0_offline_observation_identity",
        "r0.offline.observation.1.v4.",
    ):
        assert forbidden not in source
    assert source.count("sys.addaudithook(") == 1


def test_fake_suite_performs_no_repository_or_external_mutation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("effect_boundary_reached")

    monkeypatch.setattr(matrix, "_load_bound_observer", forbidden)
    monkeypatch.setattr(matrix, "_stable_bytes", forbidden)
    before = tuple(ROOT.rglob("*"))
    matrix.evaluate_prelaunch_gate_matrix(FakeAdapter())
    after = tuple(ROOT.rglob("*"))
    assert after == before


def test_production_request_prerequisite_probe_never_reads_identity() -> None:
    class Owner(ModuleType):
        MAX_STDOUT_BYTES = 4096
        MAX_FAILURE_STDERR_BYTES = 128

        def __getattr__(self, name: str) -> object:
            if "IDENT" in name:
                raise AssertionError("identity_read_forbidden")
            raise AttributeError(name)

    class Launcher:
        exact = True
        identity = object()
        windows_directory = "PRIVATE_WINDOWS_DIRECTORY"

    observer = ModuleType("synthetic_observer")
    observer._LauncherBinding = Launcher
    observer.FIXED_LAUNCHER_TOKEN = "py"
    observer.FIXED_VERSION_TOKEN = "-3.13"
    observer.FIXED_NO_BYTECODE_TOKEN = "-B"
    observer.FIXED_CHILD_SCRIPT = "tools/check_role_pool_r0_offline_observation.py"
    observer.TIMEOUT_SECONDS = 120.0
    observer._fixed_environment = lambda value: (
        ("PYTHONDONTWRITEBYTECODE", "1"),
        ("SYSTEMROOT", value),
    )
    repository_root = Path("synthetic-root")
    observer._repository_root = lambda: repository_root

    adapter = object.__new__(matrix._ProductionPrelaunchGateAdapter)
    adapter._observer = observer
    adapter._audit = None
    assert adapter.probe_fixed_request_prerequisites(
        repository_root,
        Owner("synthetic_owner"),
        Launcher(),
    ) is True


def test_production_adapter_accepts_platform_path_payloads() -> None:
    observer = ModuleType("synthetic_observer")
    repository_root = Path("synthetic-root")
    installed_root = Path("synthetic-installed")
    owner = ModuleType("synthetic_owner")
    observer._load_owner_api = lambda value: owner if value == repository_root else None

    class Snapshot:
        exact = True

    observer._owned_state_snapshot = (
        lambda received_owner, received_repository, received_installed: Snapshot()
        if (
            received_owner is owner
            and received_repository == repository_root
            and received_installed == installed_root
        )
        else None
    )

    adapter = object.__new__(matrix._ProductionPrelaunchGateAdapter)
    adapter._observer = observer
    adapter._audit = object()
    assert adapter.probe_frozen_owner_api(repository_root) is owner
    assert (
        adapter.probe_prelaunch_effect_snapshot(
            repository_root,
            owner,
            installed_root,
        ).exact
        is True
    )
