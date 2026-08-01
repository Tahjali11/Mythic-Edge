from __future__ import annotations

import hashlib
import io
import itertools
import stat
import sys
from collections import Counter
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import run_role_pool_r0_direct_interpreter_preflight as target

REPOSITORY_ROOT = Path(__file__).absolute().parent.parent
PRIVATE_PATH = Path(r"C:\synthetic-private\python.exe")
OBSERVED_AT = "2026-08-01T00:00:00Z"


def _early_effect(*, pre: str = "not_started") -> target.LocalEffectObservation:
    return target.LocalEffectObservation(
        "not_entered",
        pre,
        "not_required",
        "exact_zero",
        0,
        0,
        0,
        target.UNAVAILABLE,
        target.UNAVAILABLE,
        target.UNAVAILABLE,
    )


def _sampled_effect(
    *,
    post: str = "exact_equal",
    audit: str = "exact_zero",
    repository_attempts: int | str = 0,
    installed_attempts: int | str = 0,
    network: int | str = 0,
    repository_delta: int | str = 0,
    installed_delta: int | str = 0,
    residue_delta: int | str = 0,
) -> target.LocalEffectObservation:
    return target.LocalEffectObservation(
        "entered",
        "exact",
        post,
        audit,
        repository_attempts,
        installed_attempts,
        network,
        repository_delta,
        installed_delta,
        residue_delta,
    )


def _process_record(record: target.SourceRecord) -> target.ProcessRecord:
    return target.ProcessRecord(
        historical_direct_use_proven=record.historical_direct_use_proven,
        public_binding_state=record.public_binding_state,
        owner_decision_state=record.owner_decision_state,
        private_binding_state=record.private_binding_state,
        ambient_job_state=record.ambient_job_state,
        precreate_setup_state=record.precreate_setup_state,
        create_call_entered=record.create_call_entered,
        create_return_state=record.create_return_state,
        top_level_identity_exact=record.top_level_identity_exact,
        parentage_known=record.parentage_known,
        exit_status=record.exit_status,
        stdout_byte_count=record.stdout_byte_count,
        stderr_byte_count=record.stderr_byte_count,
        top_level_process_count=record.top_level_process_count,
        descendant_process_count=record.descendant_process_count,
        descendant_attempt_detected=record.descendant_attempt_detected,
        timed_out=record.timed_out,
        cleanup_confirmed=record.cleanup_confirmed,
        output_complete=record.output_complete,
    )


def _parent_api():
    return target._load_parent_api(REPOSITORY_ROOT)


def _bindings(*, exact: bool = True) -> target.PublicBindingSnapshot:
    return target.PublicBindingSnapshot(
        exact=exact,
        executor_sha256="3" * 64,
        executor_test_sha256="4" * 64,
        parent_api=_parent_api(),
    )


def _prelaunch(route: str, *, cleanup: bool = True) -> target.SourceRecord:
    prefix = {
        "PR-01": (True, "not_observed", "not_observed", "not_observed", "not_observed", "not_observed"),
        "PR-02": (False, "rejected", "not_observed", "not_observed", "not_observed", "not_observed"),
        "PR-03": (False, "exact", "rejected", "not_observed", "not_observed", "not_observed"),
        "PR-04": (False, "exact", "exact", "rejected", "not_observed", "not_observed"),
        "PR-05": (False, "exact", "exact", "exact", "rejected", "not_observed"),
        "PR-05A": (False, "exact", "exact", "exact", "admitted", "failed_no_process"),
    }[route]
    return target.SourceRecord(
        historical_direct_use_proven=prefix[0],
        public_binding_state=prefix[1],
        owner_decision_state=prefix[2],
        private_binding_state=prefix[3],
        ambient_job_state=prefix[4],
        precreate_setup_state=prefix[5],
        create_call_entered=False,
        create_return_state="not_entered",
        top_level_identity_exact=False,
        parentage_known=False,
        exit_status="not_started",
        stdout_byte_count=0,
        stderr_byte_count=0,
        top_level_process_count=0,
        descendant_process_count=0,
        descendant_attempt_detected=False,
        timed_out=False,
        effect_derivation_state=(
            "early_terminal_structural_zero"
            if route in {"PR-01", "PR-02", "PR-03", "PR-04", "PR-05"}
            else "sampled_exact_zero"
        ),
        repository_write_count=0,
        installed_write_count=0,
        generated_residue_delta_count=0,
        executor_network_operation_count=0,
        cleanup_confirmed=cleanup,
        output_complete=True,
    )


def _create_failure() -> target.SourceRecord:
    return target.source_record_from_process(
        target._create_failure_record(),
        _sampled_effect(),
    )


def _postcreate(
    *,
    early_unknown: bool = False,
    descendant: bool = False,
    late_unknown: bool = False,
) -> target.SourceRecord:
    count = 1 if descendant else 0
    return target.SourceRecord(
        historical_direct_use_proven=False,
        public_binding_state="exact",
        owner_decision_state="exact",
        private_binding_state="exact",
        ambient_job_state="admitted",
        precreate_setup_state="complete",
        create_call_entered=True,
        create_return_state="succeeded_one_process",
        top_level_identity_exact=True,
        parentage_known=True,
        exit_status="zero",
        stdout_byte_count=1 if late_unknown else 0,
        stderr_byte_count=0,
        top_level_process_count=1,
        descendant_process_count=count,
        descendant_attempt_detected=descendant,
        timed_out=early_unknown,
        effect_derivation_state="sampled_exact_zero",
        repository_write_count=0,
        installed_write_count=0,
        generated_residue_delta_count=0,
        executor_network_operation_count=0,
        cleanup_confirmed=True,
        output_complete=True,
    )


def _positive_fixtures() -> list[tuple[str, target.SourceRecord]]:
    fixtures = [
        ("PR-01", _prelaunch("PR-01")),
        ("PR-02", _prelaunch("PR-02")),
        ("PR-03", _prelaunch("PR-03")),
        ("PR-04", _prelaunch("PR-04")),
        ("PR-05", _prelaunch("PR-05")),
        ("PR-05A", _prelaunch("PR-05A", cleanup=True)),
        ("PR-05A", _prelaunch("PR-05A", cleanup=False)),
        ("PR-06", _create_failure()),
    ]
    for early, descendant, late in itertools.product((False, True), repeat=3):
        if early:
            row = "PR-07"
        elif descendant:
            row = "PR-08"
        elif late:
            row = "PR-07"
        else:
            row = "PR-09"
        fixtures.append(
            (
                row,
                _postcreate(
                    early_unknown=early,
                    descendant=descendant,
                    late_unknown=late,
                ),
            )
        )
    return fixtures


class FakeEffectMonitor:
    def __init__(
        self,
        calls: list[str],
        *,
        pre_state: str = "exact",
        post_observation: target.LocalEffectObservation | None = None,
    ) -> None:
        self.calls = calls
        self.pre_state = pre_state
        self.post_observation = post_observation or _sampled_effect()
        self.pre_observed = False
        self.boundary_entered = False

    def observe_pre(self, parent_api) -> str:
        self.calls.append("effects_pre")
        self.pre_observed = True
        return self.pre_state

    def observe_early_terminal(self) -> target.LocalEffectObservation:
        self.calls.append("effects_early")
        return _early_effect(pre=self.pre_state if self.pre_observed else "not_started")

    def enter_effect_boundary(self) -> None:
        self.calls.append("effects_boundary")
        if not self.pre_observed or self.pre_state != "exact":
            raise target.LocalEffectEvidenceError
        self.boundary_entered = True

    def observe_post_terminal(self) -> target.LocalEffectObservation:
        self.calls.append("effects_post")
        if not self.boundary_entered:
            raise target.LocalEffectEvidenceError
        return self.post_observation


class FakeAdapter:
    def __init__(
        self,
        record: target.ProcessRecord | None = None,
        *,
        public_exact: bool = True,
        private_exact: bool = True,
        ambient: target.AmbientJobObservation | None = None,
        pre_state: str = "exact",
        post_observation: target.LocalEffectObservation | None = None,
    ) -> None:
        self.record = _process_record(_postcreate()) if record is None else record
        self.public_exact = public_exact
        self.private_exact = private_exact
        self.ambient = ambient or target.AmbientJobObservation(True, False)
        self.calls: list[str] = []
        self.request: target.FixedLaunchRequest | None = None
        self.effects = FakeEffectMonitor(
            self.calls,
            pre_state=pre_state,
            post_observation=post_observation,
        )

    def begin_local_effect_observation(self, repository_root: Path) -> FakeEffectMonitor:
        self.calls.append("effects_begin")
        return self.effects

    def validate_public_bindings(self, repository_root: Path) -> target.PublicBindingSnapshot:
        self.calls.append("public")
        return target.PublicBindingSnapshot(
            self.public_exact,
            "3" * 64,
            "4" * 64,
            _parent_api(),
        )

    def validate_private_binding(self, path: Path, parent_api) -> None:
        self.calls.append("private")
        if not self.private_exact:
            raise target.PreflightFailure

    def revalidate_private_binding(self, path: Path, parent_api) -> None:
        self.calls.append("revalidate")
        if not self.private_exact:
            raise target.PreflightFailure

    def observe_ambient_job(self) -> target.AmbientJobObservation:
        self.calls.append("ambient")
        return self.ambient

    def execute_once(self, request, selection, parent_api) -> target.ProcessRecord:
        self.calls.append("execute")
        self.request = request
        return self.record

    def observed_at_utc(self) -> str:
        return OBSERVED_AT


def _resign(document: dict[str, object]) -> bytes:
    document["result_sha256"] = target.self_digest(document, "result_sha256")
    return target.canonical_bytes(document)


def test_exact_public_bindings_are_current_and_targets_are_ordinary() -> None:
    snapshot = target._public_bindings(REPOSITORY_ROOT)
    assert snapshot.exact is True
    assert snapshot.executor_sha256 == hashlib.sha256(
        (REPOSITORY_ROOT / target.EXECUTOR_PATH).read_bytes()
    ).hexdigest()
    assert snapshot.executor_test_sha256 == hashlib.sha256(
        (REPOSITORY_ROOT / target.EXECUTOR_TEST_PATH).read_bytes()
    ).hexdigest()


@pytest.mark.parametrize(
    "drift_path",
    [
        target.EXECUTOR_CONTRACT_PATH,
        target.EXECUTOR_REVIEW_PATH,
        target.PARENT_CONTRACT_PATH,
        target.PARENT_REVIEW_PATH,
        target.HARNESS_PATH,
        target.HARNESS_TEST_PATH,
    ],
)
def test_each_public_input_drift_is_rejected(monkeypatch, drift_path: Path) -> None:
    original = target._stable_file_sha256

    def drift_one(path: Path) -> str:
        if path == REPOSITORY_ROOT / drift_path:
            return "0" * 64
        return original(path)

    monkeypatch.setattr(target, "_stable_file_sha256", drift_one)
    monkeypatch.setattr(
        target,
        "_load_parent_api",
        lambda repository_root: pytest.fail("drifted parent must not be imported"),
    )
    assert target._public_bindings(REPOSITORY_ROOT).exact is False


def test_public_drift_stops_before_private_access() -> None:
    adapter = FakeAdapter(public_exact=False)
    result = target.execute_preflight(PRIVATE_PATH, adapter=adapter)
    assert result["result_status"] == "observation_binding_rejected"
    assert result["preflight_authority_consumed"] is False
    assert adapter.calls == ["effects_begin", "public", "effects_early"]


def test_private_binding_failure_stops_before_ambient_or_launch() -> None:
    adapter = FakeAdapter(private_exact=False)
    result = target.execute_preflight(PRIVATE_PATH, adapter=adapter)
    assert result["result_status"] == "observation_binding_rejected"
    assert adapter.calls == [
        "effects_begin",
        "public",
        "effects_pre",
        "private",
        "effects_early",
    ]


def test_ambient_rejection_stops_before_setup() -> None:
    adapter = FakeAdapter(ambient=target.AmbientJobObservation(False, None))
    result = target.execute_preflight(PRIVATE_PATH, adapter=adapter)
    assert result["result_status"] == "observation_binding_rejected"
    assert adapter.calls == [
        "effects_begin",
        "public",
        "effects_pre",
        "private",
        "revalidate",
        "ambient",
        "effects_early",
    ]


def test_fake_adapter_flow_uses_fixed_request_and_never_retries(monkeypatch) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Windows")
    monkeypatch.setenv("WINDIR", r"C:\Windows")
    adapter = FakeAdapter()
    result = target.execute_preflight(PRIVATE_PATH, adapter=adapter)
    assert result["result_status"] == "direct_interpreter_preflight_passed"
    assert adapter.calls == [
        "effects_begin",
        "public",
        "effects_pre",
        "private",
        "revalidate",
        "ambient",
        "effects_boundary",
        "execute",
        "effects_post",
    ]
    assert adapter.request is not None
    assert adapter.request.application_path == PRIVATE_PATH
    assert adapter.request.arguments == ("-B", "-c", "pass")
    assert adapter.request.repository_root == REPOSITORY_ROOT
    assert adapter.request.timeout_seconds == 30.0
    assert adapter.request.creation_flags == target.BASE_CREATION_FLAGS
    assert adapter.request.inherited_streams == (
        "stdin_read",
        "stdout_write",
        "stderr_write",
    )
    assert {name for name, _ in adapter.request.environment} == {
        "SystemRoot",
        "WINDIR",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONNOUSERSITE",
        "PYTHONUTF8",
    }
    assert result["process_launch_count"] == 1
    assert result["retry_count"] == 0


@pytest.mark.parametrize(
    ("payload", "accepted"),
    [
        (b"C:\\synthetic-private\\python.exe\n", True),
        (b"", False),
        (b"\n", False),
        (b"\xef\xbb\xbfC:\\synthetic-private\\python.exe\n", False),
        (b"C:\\synthetic\x00\\python.exe\n", False),
        (b"C:\\synthetic-private\\python.exe\r\n", False),
        (b"C:\\synthetic-private\\python.exe\nextra\n", False),
        (b"relative\\python.exe\n", False),
        (b"C:\\synthetic-private\\other.exe\n", False),
        (b"\xff\n", False),
    ],
)
def test_private_stdin_is_strict_and_no_echo(payload: bytes, accepted: bool) -> None:
    if accepted:
        assert target.parse_private_path_stdin(io.BytesIO(payload)) == PRIVATE_PATH
    else:
        with pytest.raises(target.PreflightFailure) as failure:
            target.parse_private_path_stdin(io.BytesIO(payload))
        private_text = payload.rstrip(b"\n").decode("utf-8", errors="ignore")
        if private_text:
            assert private_text not in str(failure.value)


def test_private_stdin_rejects_over_limit() -> None:
    with pytest.raises(target.PreflightFailure):
        target.parse_private_path_stdin(io.BytesIO(b"C:\\" + b"x" * 4090 + b"\\python.exe\n"))


def test_cli_has_only_the_fixed_ingress_and_does_not_touch_adapter(monkeypatch) -> None:
    stderr = SimpleNamespace(buffer=io.BytesIO())
    monkeypatch.setattr(sys, "stderr", stderr)
    assert target.run(["--path", r"C:\synthetic-private\python.exe"]) == 3
    assert stderr.buffer.getvalue() == target.UNKNOWN_SENTINEL


def test_cli_checks_public_bindings_before_reading_private_stdin(monkeypatch) -> None:
    class ExplodingInput:
        def read(self, size=-1):
            raise AssertionError("private stdin was read before public binding rejection")

    adapter = FakeAdapter(public_exact=False)
    stdout = SimpleNamespace(buffer=io.BytesIO())
    stderr = SimpleNamespace(buffer=io.BytesIO())
    monkeypatch.setattr(target, "CtypesDirectWindowsPreflightAdapter", lambda: adapter)
    monkeypatch.setattr(sys, "stdin", SimpleNamespace(buffer=ExplodingInput()))
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    assert target.run(["--private-path-stdin"]) == 2
    result = target.parse_result(stdout.buffer.getvalue())
    assert result["result_status"] == "observation_binding_rejected"
    assert adapter.calls == ["effects_begin", "public", "effects_early"]
    assert stderr.buffer.getvalue() == b""


def test_cli_valid_path_uses_one_public_check_and_fake_adapter_only(monkeypatch) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Windows")
    monkeypatch.setenv("WINDIR", r"C:\Windows")
    adapter = FakeAdapter()
    stdout = SimpleNamespace(buffer=io.BytesIO())
    stderr = SimpleNamespace(buffer=io.BytesIO())
    monkeypatch.setattr(target, "CtypesDirectWindowsPreflightAdapter", lambda: adapter)
    monkeypatch.setattr(
        sys,
        "stdin",
        SimpleNamespace(buffer=io.BytesIO(b"C:\\synthetic-private\\python.exe\n")),
    )
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    assert target.run(["--private-path-stdin"]) == 0
    assert target.parse_result(stdout.buffer.getvalue())["result_status"] == (
        "direct_interpreter_preflight_passed"
    )
    assert adapter.calls == [
        "effects_begin",
        "public",
        "effects_pre",
        "private",
        "revalidate",
        "ambient",
        "effects_boundary",
        "execute",
        "effects_post",
    ]
    assert stderr.buffer.getvalue() == b""


def test_cli_effect_evidence_failure_uses_only_the_fixed_no_echo_sentinel(monkeypatch) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Windows")
    monkeypatch.setenv("WINDIR", r"C:\Windows")
    adapter = FakeAdapter(
        post_observation=_sampled_effect(
            audit="nonzero",
            network=1,
        )
    )
    stdout = SimpleNamespace(buffer=io.BytesIO())
    stderr = SimpleNamespace(buffer=io.BytesIO())
    monkeypatch.setattr(target, "CtypesDirectWindowsPreflightAdapter", lambda: adapter)
    monkeypatch.setattr(
        sys,
        "stdin",
        SimpleNamespace(buffer=io.BytesIO(b"C:\\synthetic-private\\python.exe\n")),
    )
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    assert target.run(["--private-path-stdin"]) == 3
    assert stdout.buffer.getvalue() == b""
    assert stderr.buffer.getvalue() == target.UNKNOWN_SENTINEL
    assert b"synthetic-private" not in stderr.buffer.getvalue()


def test_cli_inventory_failure_does_not_echo_row_paths(monkeypatch) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Windows")
    monkeypatch.setenv("WINDIR", r"C:\Windows")
    adapter = FakeAdapter()
    private_row = "invented/private-row.txt"

    def fail_post():
        raise OSError(private_row)

    adapter.effects.observe_post_terminal = fail_post
    stdout = SimpleNamespace(buffer=io.BytesIO())
    stderr = SimpleNamespace(buffer=io.BytesIO())
    monkeypatch.setattr(target, "CtypesDirectWindowsPreflightAdapter", lambda: adapter)
    monkeypatch.setattr(
        sys,
        "stdin",
        SimpleNamespace(buffer=io.BytesIO(b"C:\\synthetic-private\\python.exe\n")),
    )
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)
    assert target.run(["--private-path-stdin"]) == 3
    assert stdout.buffer.getvalue() == b""
    assert stderr.buffer.getvalue() == target.UNKNOWN_SENTINEL
    assert private_row.encode("ascii") not in stderr.buffer.getvalue()


def test_no_alternate_process_ingress_is_imported() -> None:
    source = (REPOSITORY_ROOT / target.EXECUTOR_PATH).read_text(encoding="utf-8")
    assert "import subprocess" not in source
    assert "os.system(" not in source
    assert "os.startfile(" not in source
    assert "shell=True" not in source


def test_production_adapter_reuses_parent_validator_and_classifier_boundary() -> None:
    calls: list[str] = []

    class Parent:
        DirectPreflightObservation = SimpleNamespace

        @staticmethod
        def validate_running_direct_interpreter(path):
            calls.append("parent_two_handle_validation")

        @staticmethod
        def _observe_windows_direct_interpreter(path):
            calls.append("parent_single_handle_revalidation")
            return "metadata"

        @staticmethod
        def validate_direct_interpreter_metadata(metadata):
            calls.append("parent_metadata_validation")

    class Kernel:
        @staticmethod
        def observe_ambient_job():
            return target.AmbientJobObservation(True, False)

        @staticmethod
        def execute_once(request, selection, parent_api):
            return _postcreate()

    adapter = target.CtypesDirectWindowsPreflightAdapter(kernel=Kernel())
    adapter.validate_private_binding(PRIVATE_PATH, Parent)
    adapter.revalidate_private_binding(PRIVATE_PATH, Parent)
    assert calls == [
        "parent_two_handle_validation",
        "parent_single_handle_revalidation",
        "parent_metadata_validation",
    ]


def test_ambient_selector_covers_all_eight_rows_and_reduced_counts() -> None:
    observations = [target.AmbientJobObservation(False, None)]
    observations.append(target.AmbientJobObservation(True, False))
    observations.append(target.AmbientJobObservation(True, True))
    for silent, breakaway, nested, ui in itertools.product((False, True), repeat=4):
        observations.append(
            target.AmbientJobObservation(
                True,
                True,
                True,
                True,
                True,
                silent,
                breakaway,
                nested,
                int(ui),
            )
        )
    counts = Counter(target.select_ambient_job(item).row_id for item in observations)
    assert counts == {
        "AJ-01": 1,
        "AJ-02": 1,
        "AJ-03": 1,
        "AJ-04": 8,
        "AJ-05": 4,
        "AJ-06": 1,
        "AJ-07": 2,
        "AJ-08": 1,
    }
    both = target.select_ambient_job(
        target.AmbientJobObservation(True, True, True, True, True, True, True, True, 0)
    )
    assert both.row_id == "AJ-04"
    assert both.creation_flags == target.BASE_CREATION_FLAGS


def test_ambient_selector_rejects_bad_query_shape_and_uses_unsigned_ui() -> None:
    malformed = target.AmbientJobObservation(True, True, True, True, True, False, False, True, -1)
    assert target.select_ambient_job(malformed).row_id == "AJ-03"
    oversized = replace(malformed, ui_restrictions_class=0x1_0000_0000)
    assert target.select_ambient_job(oversized).row_id == "AJ-03"
    breakaway = replace(malformed, ui_restrictions_class=0, breakaway=True)
    selected = target.select_ambient_job(breakaway)
    assert selected.row_id == "AJ-05"
    assert selected.creation_flags == target.BASE_CREATION_FLAGS | target.CREATE_BREAKAWAY_FROM_JOB


def test_raw_local_effect_selector_is_disjoint_and_complete() -> None:
    counts = Counter()
    first_applicable = Counter()
    for boundary, pre, post, audit in itertools.product(
        ("not_entered", "entered"),
        ("not_started", "failed_or_ambiguous", "exact"),
        ("not_required", "failed_or_ambiguous", "exact_equal", "exact_drift"),
        ("exact_zero", "nonzero", "unreadable_or_ambiguous"),
    ):
        observation = target.LocalEffectObservation(
            boundary,
            pre,
            post,
            audit,
            0,
            0,
            0,
            target.UNAVAILABLE,
            target.UNAVAILABLE,
            target.UNAVAILABLE,
        )
        matches = target.local_effect_predicate_rows(observation)
        assert len(matches) == 1
        counts[matches[0]] += 1
        first_applicable[matches[0]] += 1
    assert counts == first_applicable == {
        "LE-01": 3,
        "LE-02": 1,
        "LE-03": 6,
        "LE-04": 8,
        "LE-05": 54,
    }


def test_local_effect_derivation_is_evidence_owned_and_fail_closed() -> None:
    early = target.derive_local_effects(_early_effect(pre="exact"))
    sampled = target.derive_local_effects(_sampled_effect())
    assert early == target.LocalEffectDerivation(
        "early_terminal_structural_zero", 0, 0, 0, 0, 0
    )
    assert sampled == target.LocalEffectDerivation("sampled_exact_zero", 0, 0, 0, 0, 0)

    double_counted = target.calculate_sampled_effect_counts(
        _sampled_effect(repository_delta=1, residue_delta=1)
    )
    assert double_counted.repository_write_count == 1
    assert double_counted.generated_residue_delta_count == 1
    assert double_counted.external_effect_count == 2

    nonzero_cases = (
        _sampled_effect(repository_attempts=1, audit="nonzero"),
        _sampled_effect(installed_attempts=1, audit="nonzero"),
        _sampled_effect(network=1, audit="nonzero"),
        _sampled_effect(repository_delta=1, post="exact_drift"),
        _sampled_effect(installed_delta=1, post="exact_drift"),
        _sampled_effect(residue_delta=1, post="exact_drift"),
        _sampled_effect(post="failed_or_ambiguous", repository_delta=target.UNAVAILABLE),
    )
    for observation in nonzero_cases:
        with pytest.raises(target.LocalEffectEvidenceError):
            target.derive_local_effects(observation)


def test_fake_adapter_pre_inventory_and_post_drift_fail_closed(monkeypatch) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Windows")
    monkeypatch.setenv("WINDIR", r"C:\Windows")
    pre_failed = FakeAdapter(pre_state="failed_or_ambiguous")
    with pytest.raises(target.LocalEffectEvidenceError):
        target.execute_preflight(PRIVATE_PATH, adapter=pre_failed)
    assert pre_failed.calls == ["effects_begin", "public", "effects_pre"]

    drifted = FakeAdapter(
        post_observation=_sampled_effect(
            post="exact_drift",
            repository_delta=1,
        )
    )
    with pytest.raises(target.LocalEffectEvidenceError):
        target.execute_preflight(PRIVATE_PATH, adapter=drifted)
    assert drifted.calls[-1] == "effects_post"


def test_pipe_handle_states_and_close_once_are_deterministic() -> None:
    class Kernel:
        def __init__(self) -> None:
            self.flags = {value: target.HANDLE_FLAG_INHERIT for value in range(1, 7)}
            self.closed: list[int] = []

        def SetHandleInformation(self, handle, mask, flags):
            value = int(handle.value)
            self.flags[value] = (self.flags[value] & ~int(mask)) | int(flags)
            return True

        def GetHandleInformation(self, handle, output):
            output._obj.value = self.flags[int(handle.value)]
            return True

        def CloseHandle(self, handle):
            self.closed.append(int(handle.value))
            return True

    kernel = Kernel()
    names = (
        "stdin_read",
        "stdin_write",
        "stdout_read",
        "stdout_write",
        "stderr_read",
        "stderr_write",
    )
    handles = {
        name: target._OwnedHandle(kernel, value)
        for value, name in enumerate(names, start=1)
    }
    target._set_and_verify_pipe_inheritance(kernel, handles)
    assert {name for name, handle in handles.items() if kernel.flags[handle.value] & 1} == {
        "stdin_read",
        "stdout_write",
        "stderr_write",
    }
    assert target._close_all(handles) is True
    assert kernel.closed == [6, 5, 4, 3, 2, 1]
    assert target._close_all(handles) is True
    assert kernel.closed == [6, 5, 4, 3, 2, 1]


def test_close_all_attempts_every_owned_handle_after_failures() -> None:
    class Kernel:
        def __init__(self) -> None:
            self.closed: list[int] = []

        def CloseHandle(self, handle):
            value = int(handle.value)
            self.closed.append(value)
            if value == 2:
                raise OSError("invented close failure")
            return value != 3

    kernel = Kernel()
    handles = {
        str(value): target._OwnedHandle(kernel, value)
        for value in (1, 2, 3)
    }
    assert target._close_all(handles) is False
    assert kernel.closed == [3, 2, 1]
    assert all(not handle.open for handle in handles.values())
    assert target._close_all(handles) is False
    assert kernel.closed == [3, 2, 1]


def test_attribute_list_deletion_requires_successful_initialization(monkeypatch) -> None:
    class Kernel:
        def __init__(self, *, initialize_ok: bool = True, size: int = 64) -> None:
            self.initialize_ok = initialize_ok
            self.size = size
            self.initialize_calls = 0
            self.deleted = 0

        def InitializeProcThreadAttributeList(self, pointer, count, flags, size):
            self.initialize_calls += 1
            if pointer is None:
                size._obj.value = self.size
                return False
            return self.initialize_ok

        def DeleteProcThreadAttributeList(self, pointer):
            self.deleted += 1

    no_size = Kernel(size=0)
    owner = target._OwnedAttributeList(no_size)
    with pytest.raises(target.PreflightFailure):
        owner.initialize()
    assert owner.close() is True
    assert no_size.deleted == 0

    allocation = Kernel()
    owner = target._OwnedAttributeList(allocation)
    monkeypatch.setattr(
        target.ctypes,
        "create_string_buffer",
        lambda size: (_ for _ in ()).throw(MemoryError),
    )
    with pytest.raises(MemoryError):
        owner.initialize()
    assert owner.close() is True
    assert allocation.deleted == 0
    monkeypatch.undo()

    rejected = Kernel(initialize_ok=False)
    owner = target._OwnedAttributeList(rejected)
    with pytest.raises(target.PreflightFailure):
        owner.initialize()
    assert owner.close() is True
    assert rejected.deleted == 0

    accepted = Kernel()
    owner = target._OwnedAttributeList(accepted)
    assert owner.initialize() is not None
    assert owner.close() is True
    assert owner.close() is True
    assert accepted.deleted == 1


def test_attribute_list_delete_failure_is_not_retried() -> None:
    class Kernel:
        def __init__(self) -> None:
            self.deleted = 0

        def InitializeProcThreadAttributeList(self, pointer, count, flags, size):
            if pointer is None:
                size._obj.value = 64
                return False
            return True

        def DeleteProcThreadAttributeList(self, pointer):
            self.deleted += 1
            raise OSError("invented delete failure")

    kernel = Kernel()
    owner = target._OwnedAttributeList(kernel)
    owner.initialize()
    assert owner.close() is False
    assert owner.close() is False
    assert kernel.deleted == 1


def test_environment_is_closed_and_case_insensitive_duplicates_fail(monkeypatch) -> None:
    monkeypatch.setattr(
        target.os,
        "environ",
        {
            "SystemRoot": r"C:\Windows",
            "WINDIR": r"C:\Windows",
            "PATH": r"C:\not-inherited",
            "TOKEN": "not-inherited",
        },
    )
    environment = target._fixed_environment()
    assert tuple(name for name, _ in environment) == (
        "SystemRoot",
        "WINDIR",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONNOUSERSITE",
        "PYTHONUTF8",
    )
    with pytest.raises(target.PreflightFailure):
        target._environment_block((('Name', 'one'), ('NAME', 'two')))


def test_stable_inventory_excludes_only_top_level_git_and_derives_deltas(tmp_path) -> None:
    root = tmp_path / "repository"
    root.mkdir()
    (root / ".git").mkdir()
    (root / ".git" / "private-control").write_text("ignored", encoding="utf-8")
    (root / "pkg").mkdir()
    (root / "pkg" / "one.txt").write_text("one", encoding="utf-8")
    (root / "pkg" / ".git").mkdir()
    (root / "pkg" / ".git" / "kept.txt").write_text("kept", encoding="utf-8")
    before = target.observe_tree_inventory(root, exclude_top_level_git=True)
    paths = tuple(row.relative_path for row in before.rows)
    assert ".git" not in paths
    assert "pkg/.git" in paths
    assert "pkg/.git/kept.txt" in paths
    installed_shape = target.observe_tree_inventory(root, exclude_top_level_git=False)
    assert ".git" in tuple(row.relative_path for row in installed_shape.rows)

    (root / "pkg" / "one.txt").write_text("changed", encoding="utf-8")
    (root / "pkg" / "two.txt").write_text("two", encoding="utf-8")
    after = target.observe_tree_inventory(root, exclude_top_level_git=True)
    assert target.inventory_row_delta_count(before.rows, after.rows) == 2


def test_windows_directory_guard_is_no_follow_and_handle_enumerated() -> None:
    class Kernel:
        def __init__(self, attributes: int) -> None:
            self.attributes = attributes
            self.created: list[tuple[int, int]] = []
            self.closed: list[int] = []

        def CreateFileW(
            self,
            path,
            access,
            share,
            security,
            disposition,
            flags,
            template,
        ):
            self.created.append((int(share), int(flags)))
            return 101

        def GetFileInformationByHandle(self, handle, output):
            output._obj.dwFileAttributes = self.attributes
            output._obj.dwVolumeSerialNumber = 17
            output._obj.nFileIndexHigh = 0
            output._obj.nFileIndexLow = 23
            return True

        def CloseHandle(self, handle):
            self.closed.append(int(handle))
            return True

    ordinary = Kernel(target.DIRECTORY_ATTRIBUTE)
    guard = target._open_windows_directory_guard(Path(r"C:\synthetic"), ordinary)
    assert ordinary.created == [
        (
            target.DIRECTORY_SHARE_READ
            | target.DIRECTORY_SHARE_WRITE
            | target.DIRECTORY_SHARE_DELETE,
            target.DIRECTORY_OPEN_REPARSE_POINT | target.DIRECTORY_BACKUP_SEMANTICS,
        )
    ]
    assert guard.identity == (17, 23)
    assert guard.close() is True
    assert guard.close() is True
    assert ordinary.closed == [101]

    reparse = Kernel(
        target.DIRECTORY_ATTRIBUTE
        | target.REPARSE_POINT_ATTRIBUTE
    )
    with pytest.raises(target.PreflightFailure):
        target._open_windows_directory_guard(Path(r"C:\synthetic-link"), reparse)
    assert reparse.closed == [101]


def test_windows_directory_guard_enumerates_original_after_path_replacement(tmp_path) -> None:
    root = tmp_path / "replacement"
    child = root / "child"
    renamed = root / "renamed"
    root.mkdir()
    child.mkdir()
    (child / "original.txt").write_text("original", encoding="utf-8")
    guard = target._open_directory_guard(child)
    try:
        child.rename(renamed)
        child.mkdir()
        (child / "replacement.txt").write_text("replacement", encoding="utf-8")
        assert tuple(entry.name for entry in guard.enumerate()) == ("original.txt",)
    finally:
        assert guard.close() is True
    assert child.is_dir()
    assert renamed.is_dir()


def test_inventory_guards_every_directory_before_enumeration_and_closes_reverse(
    tmp_path,
    monkeypatch,
) -> None:
    root = (tmp_path / "guarded").absolute()
    child = root / "child"
    root.mkdir()
    child.mkdir()
    (child / "payload.txt").write_text("payload", encoding="utf-8")
    opened: list[Path] = []
    enumerated: list[Path] = []
    closed: list[Path] = []

    class Guard:
        def __init__(self, path: Path) -> None:
            self.path = path
            self.identity = (1, path.lstat().st_ino)

        def close(self) -> bool:
            closed.append(self.path)
            return True

        def enumerate(self):
            enumerated.append(self.path)
            rows = []
            with target.os.scandir(self.path) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name.encode("utf-8"))
            for entry in entries:
                metadata = entry.stat(follow_symlinks=False)
                rows.append(
                    target._NativeDirectoryEntry(
                        entry.name,
                        entry.inode(),
                        (
                            target.DIRECTORY_ATTRIBUTE
                            if stat.S_ISDIR(metadata.st_mode)
                            else 0
                        ),
                        0 if stat.S_ISDIR(metadata.st_mode) else metadata.st_size,
                    )
                )
            return tuple(rows)

    def open_guard(path: Path):
        opened.append(path)
        return Guard(path)

    monkeypatch.setattr(target, "_open_directory_guard", open_guard)
    inventory = target.observe_tree_inventory(root, exclude_top_level_git=False)
    assert tuple(row.relative_path for row in inventory.rows) == (
        "child",
        "child/payload.txt",
    )
    assert opened == [root, child]
    assert enumerated == [root, child, root, child]
    assert closed == [child, root]


def test_inventory_rejects_guard_identity_mismatch_and_aggregates_closes(
    tmp_path,
    monkeypatch,
) -> None:
    root = (tmp_path / "mismatch").absolute()
    child = root / "child"
    root.mkdir()
    child.mkdir()
    closed: list[Path] = []

    class Guard:
        def __init__(self, path: Path) -> None:
            self.path = path
            file_index = path.lstat().st_ino
            self.identity = (1, file_index + int(path == child))

        def close(self) -> bool:
            closed.append(self.path)
            return self.path != child

        def enumerate(self):
            rows = []
            with target.os.scandir(self.path) as iterator:
                entries = tuple(iterator)
            for entry in entries:
                metadata = entry.stat(follow_symlinks=False)
                rows.append(
                    target._NativeDirectoryEntry(
                        entry.name,
                        entry.inode(),
                        (
                            target.DIRECTORY_ATTRIBUTE
                            if stat.S_ISDIR(metadata.st_mode)
                            else 0
                        ),
                        0 if stat.S_ISDIR(metadata.st_mode) else metadata.st_size,
                    )
                )
            return tuple(rows)

    monkeypatch.setattr(target, "_open_directory_guard", Guard)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)
    assert closed == [child, root]


def test_inventory_delta_counts_added_removed_modified_renamed_and_kind_changed(
    tmp_path,
) -> None:
    root = tmp_path / "delta"
    root.mkdir()
    (root / "removed.txt").write_text("removed", encoding="utf-8")
    (root / "modified.txt").write_text("before", encoding="utf-8")
    (root / "renamed-before.txt").write_text("rename", encoding="utf-8")
    (root / "kind-change").write_text("file", encoding="utf-8")
    before = target.observe_tree_inventory(root, exclude_top_level_git=False)

    (root / "removed.txt").unlink()
    (root / "modified.txt").write_text("after", encoding="utf-8")
    (root / "renamed-before.txt").rename(root / "renamed-after.txt")
    (root / "kind-change").unlink()
    (root / "kind-change").mkdir()
    (root / "added.txt").write_text("added", encoding="utf-8")
    after = target.observe_tree_inventory(root, exclude_top_level_git=False)

    assert target.inventory_row_delta_count(before.rows, after.rows) == 6


def test_repository_role_pool_projection_matches_the_accepted_tree_binding() -> None:
    inventory = target.observe_tree_inventory(
        REPOSITORY_ROOT / target.ROLE_POOL_SOURCE_PREFIX,
        exclude_top_level_git=False,
    )
    assert target._tree_manifest_binding(inventory.rows) == (
        target.ROLE_POOL_TREE_NODE_COUNT,
        target.ROLE_POOL_TREE_FILE_COUNT,
        target.ROLE_POOL_TREE_MANIFEST_BYTE_COUNT,
        target.ROLE_POOL_TREE_SHA256,
    )


def test_residue_projection_and_inventory_budgets_are_exact(tmp_path, monkeypatch) -> None:
    rows = (
        target.InventoryRow("safe.txt", "file", 0, "0" * 64),
        target.InventoryRow("a/__pycache__", "directory", 0, "0" * 64),
        target.InventoryRow("a/value.pyc", "file", 0, "0" * 64),
        target.InventoryRow("a/value.pyo", "file", 0, "0" * 64),
        target.InventoryRow("a/.pytest_cache/x", "file", 0, "0" * 64),
        target.InventoryRow("a/.ruff_cache/x", "file", 0, "0" * 64),
    )
    assert tuple(row.relative_path for row in target._residue_projection(rows)) == (
        "a/__pycache__",
        "a/value.pyc",
        "a/value.pyo",
        "a/.pytest_cache/x",
        "a/.ruff_cache/x",
    )

    root = tmp_path / "budget"
    root.mkdir()
    (root / "one").write_bytes(b"1")
    (root / "two").write_bytes(b"2")
    monkeypatch.setattr(target, "MAX_INVENTORY_ROWS", 1)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)


def test_inventory_file_total_and_time_budgets_fail_closed(tmp_path, monkeypatch) -> None:
    root = tmp_path / "budget"
    root.mkdir()
    (root / "one").write_bytes(b"1")
    (root / "two").write_bytes(b"2")

    monkeypatch.setattr(target, "MAX_INVENTORY_FILE_BYTES", 0)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)
    monkeypatch.setattr(target, "MAX_INVENTORY_FILE_BYTES", 1)
    monkeypatch.setattr(target, "MAX_INVENTORY_TOTAL_BYTES", 1)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)

    monkeypatch.setattr(target, "MAX_INVENTORY_TOTAL_BYTES", 2)
    monkeypatch.setattr(target, "MAX_INVENTORY_ROWS", 2)
    assert len(target.observe_tree_inventory(root, exclude_top_level_git=False).rows) == 2
    target._validate_relative_path("x" * target.MAX_RELATIVE_PATH_BYTES)

    ticks = iter((0.0, 31.0))
    monkeypatch.setattr(target.time, "monotonic", lambda: next(ticks))
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)


def test_inventory_path_registry_and_root_shape_fail_closed(tmp_path, monkeypatch) -> None:
    seen: set[str] = set()
    folded: set[str] = set()
    target._register_inventory_path("Case.txt", seen, folded)
    with pytest.raises(target.PreflightFailure):
        target._register_inventory_path("Case.txt", seen, folded)
    with pytest.raises(target.PreflightFailure):
        target._register_inventory_path("case.txt", seen, folded)

    missing = tmp_path / "missing"
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(missing, exclude_top_level_git=False)
    ordinary_file = tmp_path / "ordinary-file"
    ordinary_file.write_text("file", encoding="utf-8")
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(ordinary_file, exclude_top_level_git=False)

    root = tmp_path / "reparse-root"
    root.mkdir()
    metadata = root.lstat()
    original_lstat = target.Path.lstat

    def reparse_lstat(path):
        if path == root:
            return SimpleNamespace(
                st_dev=metadata.st_dev,
                st_ino=metadata.st_ino,
                st_mode=stat.S_IFDIR,
                st_size=metadata.st_size,
                st_mtime_ns=metadata.st_mtime_ns,
                st_file_attributes=(
                    getattr(metadata, "st_file_attributes", 0)
                    | stat.FILE_ATTRIBUTE_REPARSE_POINT
                ),
            )
        return original_lstat(path)

    monkeypatch.setattr(target.Path, "lstat", reparse_lstat)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)


def test_inventory_unreadability_and_open_identity_drift_fail_closed(
    tmp_path,
    monkeypatch,
) -> None:
    root = tmp_path / "unstable"
    root.mkdir()
    payload = root / "payload.txt"
    payload.write_text("payload", encoding="utf-8")
    original_open = target.Path.open

    def unreadable(path, *args, **kwargs):
        if path == payload:
            raise OSError("invented unreadability")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(target.Path, "open", unreadable)
    with pytest.raises(OSError, match="invented unreadability"):
        target.observe_tree_inventory(root, exclude_top_level_git=False)
    monkeypatch.setattr(target.Path, "open", original_open)

    original_fstat = target.os.fstat

    def drifted_fstat(file_descriptor):
        metadata = original_fstat(file_descriptor)
        return SimpleNamespace(
            st_dev=metadata.st_dev,
            st_ino=metadata.st_ino,
            st_mode=metadata.st_mode,
            st_size=metadata.st_size,
            st_mtime_ns=metadata.st_mtime_ns + 1,
            st_file_attributes=getattr(metadata, "st_file_attributes", 0),
        )

    monkeypatch.setattr(target.os, "fstat", drifted_fstat)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)


def test_residue_delta_rejects_new_removed_and_modified_rows() -> None:
    empty_digest = hashlib.sha256(b"").hexdigest()
    before = (
        target.InventoryRow(".pytest_cache", "directory", 0, empty_digest),
        target.InventoryRow(".pytest_cache/removed", "file", 1, "1" * 64),
        target.InventoryRow("pkg/__pycache__/modified.pyc", "file", 1, "2" * 64),
    )
    after = (
        target.InventoryRow(".pytest_cache", "directory", 0, empty_digest),
        target.InventoryRow("pkg/__pycache__/modified.pyc", "file", 2, "3" * 64),
        target.InventoryRow("pkg/.ruff_cache/added", "file", 1, "4" * 64),
    )
    assert target.inventory_row_delta_count(
        target._residue_projection(before),
        target._residue_projection(after),
    ) == 3
    assert target.inventory_row_delta_count(
        target._residue_projection(before),
        target._residue_projection(before),
    ) == 0


def test_post_observation_attempts_both_roots_when_repository_read_fails(
    monkeypatch,
) -> None:
    repository_root = Path(r"C:\synthetic-repository")
    installed_root = Path(r"C:\synthetic-installed")
    empty = target.TreeInventory((1, 1), ())
    monitor = object.__new__(target._ProductionLocalEffectMonitor)
    monitor.repository_root = repository_root
    monitor.installed_root = installed_root
    monitor.audit = target._ExecutorAuditOwner(repository_root)
    monitor.audit.bind_installed_root(installed_root)
    monitor.pre_inventory_state = "exact"
    monitor.effect_boundary_state = "entered"
    monitor.pre_snapshot = target._EffectSnapshot(empty, empty, ())
    calls: list[Path] = []

    def observe(root, *, exclude_top_level_git):
        calls.append(root)
        if root == repository_root:
            raise target.PreflightFailure
        return empty

    monkeypatch.setattr(target, "observe_tree_inventory", observe)
    result = monitor.observe_post_terminal()
    assert calls == [repository_root, installed_root]
    assert result.post_inventory_state == "failed_or_ambiguous"
    with pytest.raises(target.LocalEffectEvidenceError):
        target.derive_local_effects(result)


def test_inventory_rejects_path_and_second_enumeration_drift(tmp_path, monkeypatch) -> None:
    with pytest.raises(target.PreflightFailure):
        target._validate_relative_path("../escape")
    with pytest.raises(target.PreflightFailure):
        target._validate_relative_path("C:/drive")
    with pytest.raises(target.PreflightFailure):
        target._validate_relative_path("x" * (target.MAX_RELATIVE_PATH_BYTES + 1))

    root = tmp_path / "drift"
    root.mkdir()
    (root / "one.txt").write_text("one", encoding="utf-8")
    original = target._enumerate_kind_map

    def drift(*args, **kwargs):
        rows = original(*args, **kwargs)
        rows["invented.txt"] = "file"
        return rows

    monkeypatch.setattr(target, "_enumerate_kind_map", drift)
    with pytest.raises(target.PreflightFailure):
        target.observe_tree_inventory(root, exclude_top_level_git=False)


def test_executor_audit_owner_derives_write_and_network_counts() -> None:
    repository = Path(r"C:\synthetic-repository")
    installed = Path(r"C:\synthetic-installed")
    owner = target._ExecutorAuditOwner(repository)
    owner.bind_installed_root(installed)
    with pytest.raises(target.LocalEffectEvidenceError):
        owner("open", (repository / "one.txt", "w", 0))
    with pytest.raises(target.LocalEffectEvidenceError):
        owner("open", (installed / "two.txt", "a", 0))
    with pytest.raises(target.LocalEffectEvidenceError):
        owner("socket.connect", ())
    assert owner.values() == ("nonzero", 1, 1, 1)

    invalid = target._ExecutorAuditOwner(repository)
    with pytest.raises(target.LocalEffectEvidenceError):
        invalid("os.putenv", ())
    assert invalid.values() == (
        "unreadable_or_ambiguous",
        target.UNAVAILABLE,
        target.UNAVAILABLE,
        target.UNAVAILABLE,
    )


def test_installed_role_pool_root_is_derived_only_from_the_accepted_checker() -> None:
    expected = Path(r"C:\synthetic-codex-home\skills\mythic-edge-role-pool")

    class Checker:
        @staticmethod
        def _production_roots():
            return SimpleNamespace(
                repository_root=REPOSITORY_ROOT,
                installed_skills_root=expected.parent,
            )

    class Parent:
        @staticmethod
        def _load_checker(repository_root):
            assert repository_root == REPOSITORY_ROOT
            return Checker

    assert target._derive_installed_role_pool_root(REPOSITORY_ROOT, Parent) == expected

    class MissingChecker:
        @staticmethod
        def _production_roots():
            return SimpleNamespace(
                repository_root=REPOSITORY_ROOT,
                installed_skills_root=None,
            )

    class MissingParent:
        @staticmethod
        def _load_checker(repository_root):
            return MissingChecker

    with pytest.raises(target.PreflightFailure):
        target._derive_installed_role_pool_root(REPOSITORY_ROOT, MissingParent)


def test_alternate_codex_home_cannot_supply_the_installed_root(monkeypatch) -> None:
    monkeypatch.setenv("CODEX_HOME", r"C:\synthetic-alternate-home")
    with pytest.raises(target.PreflightFailure):
        target._derive_installed_role_pool_root(REPOSITORY_ROOT, _parent_api())


def test_network_count_is_executor_owned_without_child_isolation_claims() -> None:
    record = _postcreate()
    result = target.seal_result(record, _bindings(), OBSERVED_AT)
    assert result["network_operation_count"] == record.executor_network_operation_count
    source = (REPOSITORY_ROOT / target.EXECUTOR_PATH).read_text(encoding="utf-8").lower()
    for forbidden_claim in (
        "child_network",
        "network_isolation",
        "firewall_enforced",
        "complete_network_observation",
        "network_impossible",
    ):
        assert forbidden_claim not in source


def test_production_source_has_one_create_and_one_resume_call_site() -> None:
    source = (REPOSITORY_ROOT / target.EXECUTOR_PATH).read_text(encoding="utf-8")
    assert source.count("kernel32.CreateProcessW(") == 1
    assert source.count("kernel32.ResumeThread(") == 1
    assert source.count("retry_count\": 0") == 1


def test_source_state_audit_is_exact() -> None:
    assert target.audit_source_state_domain() == (8, 5824)


def test_sixteen_positive_projection_fixtures_have_exact_counts() -> None:
    fixtures = _positive_fixtures()
    assert len(fixtures) == 16
    assert Counter(row for row, _ in fixtures) == {
        "PR-01": 1,
        "PR-02": 1,
        "PR-03": 1,
        "PR-04": 1,
        "PR-05": 1,
        "PR-05A": 2,
        "PR-06": 1,
        "PR-07": 5,
        "PR-08": 2,
        "PR-09": 1,
    }
    for _, record in fixtures:
        result = target.seal_result(record, _bindings(), OBSERVED_AT)
        assert target.parse_result(target.canonical_bytes(result)) == result


def test_precreate_failure_is_unconsumed_terminal_and_cleanup_is_exact() -> None:
    for cleanup in (False, True):
        result = target.seal_result(_prelaunch("PR-05A", cleanup=cleanup), _bindings(), OBSERVED_AT)
        assert result["result_status"] == "direct_interpreter_preflight_unknown"
        assert result["preflight_authority_consumed"] is False
        assert result["cleanup_confirmed"] is cleanup
        assert result["process_launch_count"] == 0
        assert result["retry_count"] == 0


def test_classifier_precedence_is_timeout_then_descendant_then_late_failure() -> None:
    early = target.seal_result(
        _postcreate(early_unknown=True, descendant=True, late_unknown=True),
        _bindings(),
        OBSERVED_AT,
    )
    descendant = target.seal_result(
        _postcreate(descendant=True, late_unknown=True),
        _bindings(),
        OBSERVED_AT,
    )
    assert early["result_status"] == "direct_interpreter_preflight_unknown"
    assert descendant["result_status"] == "direct_interpreter_preflight_descendant_observed"


def test_parent_selector_audit_has_exact_outcome_counts() -> None:
    states = ("not_run", "descendant", "unknown", "passed")
    counts = Counter(
        target.select_parent_outcome(history, public, owner, private, state)
        for history, public, owner, private, state in itertools.product(
            (False, True), (False, True), (False, True), (False, True), states
        )
    )
    assert counts == {
        "direct_interpreter_hypothesis_rejected": 32,
        "observation_binding_rejected": 20,
        "direct_interpreter_preflight_required": 9,
        "direct_interpreter_preflight_descendant_observed": 1,
        "direct_interpreter_preflight_unknown": 1,
        "direct_interpreter_preflight_passed": 1,
    }


def test_ten_consumption_flip_negatives_are_rejected() -> None:
    representatives: dict[str, target.SourceRecord] = {}
    for row, record in _positive_fixtures():
        representatives.setdefault(row, record)
    assert len(representatives) == 10
    for record in representatives.values():
        result = target.seal_result(record, _bindings(), OBSERVED_AT)
        result["preflight_authority_consumed"] = not result["preflight_authority_consumed"]
        with pytest.raises(target.ResultProjectionError):
            target.validate_result_source_binding(result, record, _parent_api())


def test_ten_effect_derivation_mode_flip_negatives_are_rejected() -> None:
    representatives: dict[str, target.SourceRecord] = {}
    for row, record in _positive_fixtures():
        representatives.setdefault(row, record)
    assert len(representatives) == 10
    for record in representatives.values():
        flipped = replace(
            record,
            effect_derivation_state=(
                "sampled_exact_zero"
                if record.effect_derivation_state == "early_terminal_structural_zero"
                else "early_terminal_structural_zero"
            ),
        )
        with pytest.raises(target.ResultProjectionError):
            target.seal_result(flipped, _bindings(), OBSERVED_AT)


def test_eleven_named_single_defect_fixtures_are_rejected() -> None:
    passed = target.seal_result(_postcreate(), _bindings(), OBSERVED_AT)
    defects: list[dict[str, object]] = []
    for field, value in (
        ("preflight_authority_consumed", False),
        ("exit_status", "nonzero"),
        ("process_launch_count", 0),
        ("stdout_byte_count", 1),
        ("timed_out", True),
        ("cleanup_confirmed", False),
        ("output_complete", False),
    ):
        candidate = dict(passed)
        candidate[field] = value
        defects.append(candidate)
    prelaunch = target.seal_result(_prelaunch("PR-02"), _bindings(), OBSERVED_AT)
    consumed_prelaunch = dict(prelaunch)
    consumed_prelaunch["preflight_authority_consumed"] = True
    defects.append(consumed_prelaunch)
    launched_preflight = dict(prelaunch)
    launched_preflight["process_launch_count"] = 1
    defects.append(launched_preflight)
    setup = target.seal_result(_prelaunch("PR-05A"), _bindings(), OBSERVED_AT)
    launched_setup = dict(setup)
    launched_setup["process_launch_count"] = 1
    defects.append(launched_setup)
    pass_shaped_unknown = dict(passed)
    pass_shaped_unknown["result_status"] = "direct_interpreter_preflight_unknown"
    defects.append(pass_shaped_unknown)
    assert len(defects) == 11
    for document in defects:
        with pytest.raises(target.ResultProjectionError):
            target.parse_result(_resign(document))


def test_known_answer_vector_is_byte_exact() -> None:
    result = target.seal_result(_postcreate(), _bindings(), OBSERVED_AT)
    result["executor_contract_sha256"] = "1" * 64
    result["executor_contract_review_sha256"] = "2" * 64
    result["executor_sha256"] = "3" * 64
    result["executor_test_sha256"] = "4" * 64
    payload = _resign(result)
    preimage = target.canonical_bytes(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    assert len(preimage) == 2156
    assert len(payload) == 2239
    assert result["result_sha256"] == (
        "7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56"
    )
    assert hashlib.sha256(payload).hexdigest() == (
        "cdcb9a8155006d0fe458e5a486c3d86eb83bf85316aba0afdfd21899587cb807"
    )
    assert target.parse_result(payload) == result


def test_result_parser_rejects_duplicate_reordered_missing_unknown_and_mistyped() -> None:
    result = target.seal_result(_postcreate(), _bindings(), OBSERVED_AT)
    payload = target.canonical_bytes(result)
    duplicate = payload.replace(b'{"schema_version":', b'{"schema_version":"duplicate","schema_version":', 1)
    candidates = [duplicate]
    reordered = {key: result[key] for key in reversed(tuple(result))}
    candidates.append(target.canonical_bytes(reordered))
    missing = dict(result)
    missing.pop("retry_count")
    candidates.append(_resign(missing))
    unknown = dict(result)
    unknown["new_authority"] = False
    candidates.append(_resign(unknown))
    mistyped = dict(result)
    mistyped["repository_id"] = True
    candidates.append(_resign(mistyped))
    for candidate in candidates:
        with pytest.raises(target.ResultProjectionError):
            target.parse_result(candidate)


def test_success_lifecycle_trace_requires_resume_once_and_exact_close_order() -> None:
    target.validate_success_lifecycle_trace(target.SUCCESS_LIFECYCLE_EVENTS)
    for mutation in (
        target.SUCCESS_LIFECYCLE_EVENTS[:-1],
        (*target.SUCCESS_LIFECYCLE_EVENTS, "resumed_once"),
        tuple(reversed(target.SUCCESS_LIFECYCLE_EVENTS)),
    ):
        with pytest.raises(target.ResultProjectionError):
            target.validate_success_lifecycle_trace(mutation)
    assert target.SUCCESS_LIFECYCLE_EVENTS.index("job_limits_set") < target.SUCCESS_LIFECYCLE_EVENTS.index(
        "resumed_once"
    )
    assert target.SUCCESS_LIFECYCLE_EVENTS.index("job_assigned") < target.SUCCESS_LIFECYCLE_EVENTS.index(
        "resumed_once"
    )
    assert target.SUCCESS_LIFECYCLE_EVENTS.index("one_process_readback") < target.SUCCESS_LIFECYCLE_EVENTS.index(
        "resumed_once"
    )
    assert target.SUCCESS_LIFECYCLE_EVENTS.index("image_validated") < target.SUCCESS_LIFECYCLE_EVENTS.index(
        "resumed_once"
    )
    assert target.SUCCESS_LIFECYCLE_EVENTS.index("parentage_validated") < target.SUCCESS_LIFECYCLE_EVENTS.index(
        "resumed_once"
    )


def test_terminal_failure_shapes_are_consumed_once_and_never_retryable() -> None:
    records = [
        _create_failure(),
        replace(_postcreate(), timed_out=True),
        replace(_postcreate(), exit_status="unknown"),
        replace(_postcreate(), stderr_byte_count=1),
        replace(_postcreate(), output_complete=False),
        replace(_postcreate(), top_level_identity_exact=False),
        replace(_postcreate(), cleanup_confirmed=False),
    ]
    for record in records:
        result = target.seal_result(record, _bindings(), OBSERVED_AT)
        assert result["result_status"] == "direct_interpreter_preflight_unknown"
        assert result["preflight_authority_consumed"] is True
        assert result["retry_count"] == 0


def test_windows_quoting_preserves_fixed_vector_without_shell() -> None:
    path = Path(r"C:\synthetic path\python.exe")
    line = target.fixed_command_line(path)
    assert line == '"C:\\synthetic path\\python.exe" -B -c pass'
    assert "cmd" not in line.casefold()


def test_all_public_results_have_zero_authority_and_effects() -> None:
    for _, record in _positive_fixtures():
        result = target.seal_result(record, _bindings(), OBSERVED_AT)
        assert tuple(result["authority_flags"]) == target.AUTHORITY_FIELDS
        assert not any(result["authority_flags"].values())
        for field in (
            "retry_count",
            "repository_write_count",
            "installed_write_count",
            "network_operation_count",
            "external_effect_count",
        ):
            assert result[field] == 0
        assert result["private_value_emitted"] is False
        assert str(PRIVATE_PATH) not in target.canonical_bytes(result).decode("utf-8")
