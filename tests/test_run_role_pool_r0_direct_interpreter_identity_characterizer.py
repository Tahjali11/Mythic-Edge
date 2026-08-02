from __future__ import annotations

import hashlib
import inspect
import io
import itertools
import json
from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from tools import run_role_pool_r0_direct_interpreter_identity_characterizer as target

SYNTHETIC_PATH = r"C:\synthetic-private\python.exe"
SYNTHETIC_MISMATCH_PATH = r"C:\synthetic-other\python.exe"
SYNTHETIC_ID = "r0.identity.synthetic.1"
OBSERVED_AT = "2026-08-02T00:00:00Z"
REPOSITORY_ROOT = Path(r"C:\synthetic-repository")


@dataclass(frozen=True, eq=False)
class SyntheticMetadata:
    runtime_implementation: str = "CPython"
    executable_basename: str = "python.exe"
    file_version: str = "3.13.14"
    product_version: str = "3.13.14"
    byte_length: int = 105696
    file_sha256: str = "1" * 64
    stable_identity_sha256: str = "2" * 64
    ordinary_file: bool = True
    reparse_point: bool = False
    equality_unavailable: bool = False

    def _contract_tuple(self) -> tuple[object, ...]:
        return (
            self.runtime_implementation,
            self.executable_basename,
            self.file_version,
            self.product_version,
            self.byte_length,
            self.file_sha256,
            self.stable_identity_sha256,
            self.ordinary_file,
            self.reparse_point,
        )

    def __eq__(self, other: object) -> bool:
        if type(other) is not SyntheticMetadata:
            return False
        if self.equality_unavailable or other.equality_unavailable:
            raise RuntimeError("synthetic-equality-unavailable")
        return self._contract_tuple() == other._contract_tuple()


EXPECTED_METADATA = SyntheticMetadata()
MISMATCH_METADATA = replace(EXPECTED_METADATA, file_version="0.0.0")
UNAVAILABLE_EQUALITY_METADATA = replace(
    EXPECTED_METADATA,
    equality_unavailable=True,
)


class SyntheticParentApi:
    DirectInterpreterMetadata = SyntheticMetadata

    @staticmethod
    def validate_direct_interpreter_metadata(metadata: SyntheticMetadata) -> None:
        if metadata._contract_tuple() != EXPECTED_METADATA._contract_tuple():
            raise RuntimeError("synthetic-binding-mismatch")


def _bindings() -> target.PublicBindingSnapshot:
    return target.PublicBindingSnapshot(
        exact=True,
        characterizer_sha256="3" * 64,
        characterizer_test_sha256="4" * 64,
        parent_api=SyntheticParentApi(),
    )


EXACT_TERMINAL = target.TerminalObservation(
    "zero",
    0,
    0,
    False,
    True,
    0,
    True,
)
TERMINATED_TERMINAL = replace(EXACT_TERMINAL, exit_state="nonzero")
EXACT_CLEANUP = target.CleanupObservation(True, 0)
EXACT_BOUNDARY = target.PreResumeBoundary(True, 1, True)


class FakeNativeAdapter:
    def __init__(
        self,
        *,
        metadata: list[target.MetadataObservation] | None = None,
        images: list[target.ImageObservation] | None = None,
        boundary: target.PreResumeBoundary = EXACT_BOUNDARY,
        creation_state: str = "created",
        creation_cleanup: target.CleanupObservation = EXACT_CLEANUP,
        resume_ok: bool = True,
        terminate_ok: bool = True,
        terminal: target.TerminalObservation = EXACT_TERMINAL,
        cleanup: target.CleanupObservation = EXACT_CLEANUP,
        raise_on: set[str] | None = None,
        exception_text: str = "synthetic-private-sentinel",
        expected_path: str = SYNTHETIC_PATH,
    ) -> None:
        self.metadata = list(
            metadata
            if metadata is not None
            else [
                target.MetadataObservation("available", EXPECTED_METADATA),
                target.MetadataObservation("available", EXPECTED_METADATA),
            ]
        )
        self.images = list(
            images
            if images is not None
            else [
                target.ImageObservation("available", SYNTHETIC_PATH),
                target.ImageObservation("available", SYNTHETIC_PATH),
            ]
        )
        self.boundary = boundary
        self.creation_state = creation_state
        self.creation_cleanup = creation_cleanup
        self.resume_ok = resume_ok
        self.terminate_ok = terminate_ok
        self.terminal = terminal
        self.cleanup_result = cleanup
        self.raise_on = set() if raise_on is None else set(raise_on)
        self.exception_text = exception_text
        self.expected_path = expected_path
        self.calls: list[str] = []
        self.session = object()
        self.request: target.FixedLaunchRequest | None = None

    def _call(self, name: str) -> None:
        self.calls.append(name)
        if name in self.raise_on:
            raise RuntimeError(self.exception_text)

    def observe_metadata(
        self,
        path: str,
        parent_api: object,
    ) -> target.MetadataObservation:
        self._call("observe_metadata")
        assert path == self.expected_path
        assert type(parent_api) is SyntheticParentApi
        return self.metadata.pop(0)

    def create_suspended(
        self,
        request: target.FixedLaunchRequest,
    ) -> target.CreateSuspendedResult:
        self._call("create_suspended")
        self.request = request
        if self.creation_state == "created":
            return target.CreateSuspendedResult("created", self.session, self.creation_cleanup)
        return target.CreateSuspendedResult(
            self.creation_state,
            None,
            self.creation_cleanup,
        )

    def observe_image(self, session: object) -> target.ImageObservation:
        self._call("observe_image")
        assert session is self.session
        return self.images.pop(0)

    def observe_pre_resume_boundary(
        self,
        session: object,
    ) -> target.PreResumeBoundary:
        self._call("observe_pre_resume_boundary")
        assert session is self.session
        return self.boundary

    def resume_once(self, session: object) -> bool:
        self._call("resume_once")
        assert session is self.session
        return self.resume_ok

    def terminate_once(self, session: object) -> bool:
        self._call("terminate_once")
        assert session is self.session
        return self.terminate_ok

    def wait_terminal(self, session: object) -> target.TerminalObservation:
        self._call("wait_terminal")
        assert session is self.session
        return self.terminal

    def cleanup(self, session: object) -> target.CleanupObservation:
        self._call("cleanup")
        assert session is self.session
        return self.cleanup_result

    def observed_at_utc(self) -> str:
        self._call("observed_at_utc")
        return OBSERVED_AT


@pytest.fixture(autouse=True)
def _synthetic_fixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        target,
        "_fixed_environment",
        lambda: (
            ("SystemRoot", r"C:\synthetic-system"),
            ("WINDIR", r"C:\synthetic-system"),
            ("PYTHONDONTWRITEBYTECODE", "1"),
            ("PYTHONNOUSERSITE", "1"),
            ("PYTHONUTF8", "1"),
        ),
    )


def _run(adapter: FakeNativeAdapter) -> dict[str, object]:
    return target.characterize_with_adapter(
        SYNTHETIC_PATH,
        characterization_id=SYNTHETIC_ID,
        adapter=adapter,
        bindings=_bindings(),
        repository_root=REPOSITORY_ROOT,
    )


def _adapter_for_category(category: str) -> FakeNativeAdapter:
    if category == target.AMBIGUOUS_CATEGORY:
        return FakeNativeAdapter(metadata=[target.MetadataObservation("ambiguous")])
    if category == target.PRELAUNCH_UNAVAILABLE_CATEGORY:
        return FakeNativeAdapter(metadata=[target.MetadataObservation("unavailable")])
    if category == target.PRELAUNCH_MISMATCH_CATEGORY:
        return FakeNativeAdapter(
            metadata=[target.MetadataObservation("available", MISMATCH_METADATA)]
        )
    if category == target.PRE_RESUME_UNAVAILABLE_CATEGORY:
        return FakeNativeAdapter(
            metadata=[target.MetadataObservation("available", EXPECTED_METADATA)],
            images=[target.ImageObservation("unavailable")],
            terminal=TERMINATED_TERMINAL,
        )
    if category == target.PRE_RESUME_MISMATCH_CATEGORY:
        return FakeNativeAdapter(
            metadata=[target.MetadataObservation("available", EXPECTED_METADATA)],
            images=[target.ImageObservation("available", SYNTHETIC_MISMATCH_PATH)],
            terminal=TERMINATED_TERMINAL,
        )
    if category == target.POST_EXIT_UNAVAILABLE_CATEGORY:
        return FakeNativeAdapter(
            metadata=[target.MetadataObservation("available", EXPECTED_METADATA)],
            images=[
                target.ImageObservation("available", SYNTHETIC_PATH),
                target.ImageObservation("unavailable"),
            ],
        )
    if category == target.POST_EXIT_MISMATCH_CATEGORY:
        return FakeNativeAdapter(
            metadata=[target.MetadataObservation("available", EXPECTED_METADATA)],
            images=[
                target.ImageObservation("available", SYNTHETIC_PATH),
                target.ImageObservation("available", SYNTHETIC_MISMATCH_PATH),
            ],
        )
    if category == target.POSTLAUNCH_UNAVAILABLE_CATEGORY:
        return FakeNativeAdapter(
            metadata=[
                target.MetadataObservation("available", EXPECTED_METADATA),
                target.MetadataObservation("unavailable"),
            ]
        )
    if category == target.EQUALITY_UNAVAILABLE_CATEGORY:
        return FakeNativeAdapter(
            metadata=[
                target.MetadataObservation("available", EXPECTED_METADATA),
                target.MetadataObservation(
                    "available",
                    UNAVAILABLE_EQUALITY_METADATA,
                ),
            ]
        )
    if category == target.EQUALITY_MISMATCH_CATEGORY:
        return FakeNativeAdapter(
            metadata=[
                target.MetadataObservation("available", EXPECTED_METADATA),
                target.MetadataObservation("available", MISMATCH_METADATA),
            ]
        )
    if category == target.EXACT_CATEGORY:
        return FakeNativeAdapter()
    raise AssertionError(category)


@pytest.mark.parametrize("category", target.CATEGORIES)
def test_exact_fixture_for_each_closed_category(category: str) -> None:
    adapter = _adapter_for_category(category)
    result = _run(adapter)

    assert result["category"] == category
    assert target.parse_result(target.canonical_bytes(result)) == result


@pytest.mark.parametrize("left,right", itertools.combinations(target.KNOWN_FAILURE_CATEGORIES, 2))
def test_all_pairwise_known_failure_conflicts_are_ambiguous(
    left: str,
    right: str,
) -> None:
    left_trace = list(next(trace for trace, category in target._VALID_TRACES.items() if category == left))
    right_trace = list(next(trace for trace, category in target._VALID_TRACES.items() if category == right))
    failure_index = {
        target.PRELAUNCH_UNAVAILABLE_CATEGORY: 1,
        target.PRELAUNCH_MISMATCH_CATEGORY: 1,
        target.PRE_RESUME_UNAVAILABLE_CATEGORY: 2,
        target.PRE_RESUME_MISMATCH_CATEGORY: 2,
        target.POST_EXIT_UNAVAILABLE_CATEGORY: 3,
        target.POST_EXIT_MISMATCH_CATEGORY: 3,
        target.POSTLAUNCH_UNAVAILABLE_CATEGORY: 4,
        target.EQUALITY_UNAVAILABLE_CATEGORY: 5,
        target.EQUALITY_MISMATCH_CATEGORY: 5,
    }
    left_index = failure_index[left]
    right_index = failure_index[right]
    combined = list(
        next(
            trace
            for trace, category in target._VALID_TRACES.items()
            if category == target.EXACT_CATEGORY
        )
    )
    if left_index == right_index:
        combined[left_index] = "ambiguous"
    else:
        combined[left_index] = left_trace[left_index]
        combined[right_index] = right_trace[right_index]
    assert target.select_identity_category(*combined) == target.AMBIGUOUS_CATEGORY


@pytest.mark.parametrize("ambiguous_index", range(6))
@pytest.mark.parametrize("known_category", target.KNOWN_FAILURE_CATEGORIES)
def test_component_ambiguity_overrides_every_known_failure(
    ambiguous_index: int,
    known_category: str,
) -> None:
    trace = list(
        next(
            values
            for values, category in target._VALID_TRACES.items()
            if category == known_category
        )
    )
    trace[ambiguous_index] = "ambiguous"
    assert target.select_identity_category(*trace) == target.AMBIGUOUS_CATEGORY


@pytest.mark.parametrize(
    "trace",
    [
        ("exact", "exact", "not_reached", "not_reached", "not_reached", "not_reached"),
        ("exact", "mismatch", "exact", "not_reached", "not_reached", "not_reached"),
        ("exact", "exact", "mismatch", "exact", "not_reached", "not_reached"),
        ("exact", "exact", "exact", "mismatch", "available", "mismatch"),
        ("exact", "exact", "exact", "exact", "not_reached", "exact"),
        ("exact", "exact", "exact", "exact", "available", "not_reached"),
    ],
)
def test_impossible_or_out_of_order_traces_are_ambiguous(
    trace: tuple[str, str, str, str, str, str],
) -> None:
    assert target.select_identity_category(*trace) == target.AMBIGUOUS_CATEGORY


def test_selector_audit_is_exact_4000_tuple_partition() -> None:
    audit = target.audit_selector()

    assert audit.tuple_count == 4000
    assert audit.overlap_count == 0
    assert audit.uncovered_count == 0
    assert audit.unreachable_category_count == 0
    assert audit.outcome_counts[target.AMBIGUOUS_CATEGORY] == 3990
    assert all(audit.outcome_counts[category] == 1 for category in target.CATEGORIES[1:])


@pytest.mark.parametrize("category", target.CATEGORIES)
def test_adapter_call_counts_and_order_are_closed_by_route(category: str) -> None:
    adapter = _adapter_for_category(category)
    result = _run(adapter)

    assert result["category"] == category
    assert adapter.calls[0:2] == ["observed_at_utc", "observe_metadata"]
    if category in {
        target.AMBIGUOUS_CATEGORY,
        target.PRELAUNCH_UNAVAILABLE_CATEGORY,
        target.PRELAUNCH_MISMATCH_CATEGORY,
    }:
        assert adapter.calls == ["observed_at_utc", "observe_metadata"]
        return
    assert adapter.calls.count("create_suspended") == 1
    assert adapter.calls.count("observe_pre_resume_boundary") == 1
    assert adapter.calls.count("wait_terminal") == 1
    assert adapter.calls.count("cleanup") == 1
    if category in {
        target.PRE_RESUME_UNAVAILABLE_CATEGORY,
        target.PRE_RESUME_MISMATCH_CATEGORY,
    }:
        assert adapter.calls.count("resume_once") == 0
        assert adapter.calls.count("terminate_once") == 1
        assert adapter.calls.count("observe_image") == 1
    else:
        assert adapter.calls.count("resume_once") == 1
        assert adapter.calls.count("terminate_once") == 0
        assert adapter.calls.count("observe_image") == 2


def test_fixed_request_cannot_be_selected_by_fake_adapter() -> None:
    adapter = FakeNativeAdapter()
    _run(adapter)

    request = adapter.request
    assert request is not None
    assert request.application_path == SYNTHETIC_PATH
    assert request.arguments == ("-B", "-c", "pass")
    assert request.repository_root == REPOSITORY_ROOT
    assert request.creation_flags == (
        target.CREATE_SUSPENDED
        | target.CREATE_NO_WINDOW
        | target.CREATE_UNICODE_ENVIRONMENT
        | target.EXTENDED_STARTUPINFO_PRESENT
    )
    assert request.timeout_seconds == 30.0
    assert request.termination_grace_seconds == 5.0
    assert tuple(name for name, _value in request.environment) == (
        "SystemRoot",
        "WINDIR",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONNOUSERSITE",
        "PYTHONUTF8",
    )


def test_post_create_setup_failure_terminates_and_closes_adopted_handles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeKernel32:
        def __init__(self) -> None:
            self.next_handle = 10
            self.inheritable: dict[int, bool] = {}
            self.closed: list[int] = []
            self.terminated: list[int] = []

        @staticmethod
        def _value(handle: object) -> int:
            value = getattr(handle, "value", handle)
            assert type(value) is int
            return value

        def CreatePipe(self, read: object, write: object, *_args: object) -> bool:
            read_value = self.next_handle
            write_value = self.next_handle + 1
            self.next_handle += 2
            read._obj.value = read_value
            write._obj.value = write_value
            self.inheritable[read_value] = True
            self.inheritable[write_value] = True
            return True

        def SetHandleInformation(
            self,
            handle: object,
            _mask: object,
            flags: int,
        ) -> bool:
            self.inheritable[self._value(handle)] = bool(
                flags & target.HANDLE_FLAG_INHERIT
            )
            return True

        def GetHandleInformation(
            self,
            handle: object,
            flags: object,
        ) -> bool:
            flags._obj.value = (
                target.HANDLE_FLAG_INHERIT
                if self.inheritable[self._value(handle)]
                else 0
            )
            return True

        def CreateJobObjectW(self, *_args: object) -> int:
            return 70

        def SetInformationJobObject(self, *_args: object) -> bool:
            return True

        def CreateIoCompletionPort(self, *_args: object) -> int:
            return 71

        def InitializeProcThreadAttributeList(
            self,
            pointer: object,
            _count: object,
            _flags: object,
            size: object,
        ) -> bool:
            if pointer is None:
                size._obj.value = 64
                return False
            return True

        def UpdateProcThreadAttribute(self, *_args: object) -> bool:
            return True

        def DeleteProcThreadAttributeList(self, _pointer: object) -> None:
            raise RuntimeError("synthetic-attribute-disposal-failure")

        def CreateProcessW(self, *_args: object) -> bool:
            information = _args[-1]._obj
            information.hProcess = 200
            information.hThread = 201
            information.dwProcessId = 202
            information.dwThreadId = 203
            return True

        def TerminateProcess(self, handle: object, _code: object) -> bool:
            self.terminated.append(self._value(handle))
            return True

        def WaitForSingleObject(self, _handle: object, _timeout: object) -> int:
            return target.WAIT_OBJECT_0

        def CloseHandle(self, handle: object) -> bool:
            self.closed.append(self._value(handle))
            return True

    kernel32 = FakeKernel32()
    monkeypatch.setattr(target, "_kernel32", lambda: kernel32)
    adapter = object.__new__(target.CtypesIdentityAdapter)

    outcome = adapter.create_suspended(
        target._build_request(SYNTHETIC_PATH, REPOSITORY_ROOT)
    )

    assert outcome.state == "ambiguous"
    assert outcome.session is None
    assert outcome.cleanup.cleanup_confirmed is False
    assert kernel32.terminated == [200]
    assert kernel32.closed.count(200) == 1
    assert kernel32.closed.count(201) == 1


@pytest.mark.parametrize(
    "changes",
    [
        {"terminal": replace(EXACT_TERMINAL, timed_out=True)},
        {"terminal": replace(EXACT_TERMINAL, stdout_byte_count=1)},
        {"terminal": replace(EXACT_TERMINAL, stderr_byte_count=1)},
        {"terminal": replace(EXACT_TERMINAL, descendant_process_count=1)},
        {"terminal": replace(EXACT_TERMINAL, streams_drained=False)},
        {"terminal": replace(EXACT_TERMINAL, process_stopped=False)},
        {"cleanup": target.CleanupObservation(False, 1)},
        {"boundary": target.PreResumeBoundary(True, 2, True)},
        {"boundary": target.PreResumeBoundary(True, 1, False)},
        {"resume_ok": False, "terminal": TERMINATED_TERMINAL},
        {"creation_state": "ambiguous"},
    ],
)
def test_lifecycle_process_output_and_cleanup_faults_fail_ambiguous(
    changes: dict[str, object],
) -> None:
    adapter = FakeNativeAdapter(**changes)
    result = _run(adapter)

    assert result["category"] == target.AMBIGUOUS_CATEGORY
    assert result["lifecycle_evidence_state"] == "ambiguous"
    if result["cleanup_confirmed"] is False:
        assert result["eligible_for_independent_review"] is False


@pytest.mark.parametrize(
    "raise_on",
    [
        {"observe_metadata"},
        {"observe_image"},
        {"observe_pre_resume_boundary"},
        {"resume_once"},
        {"wait_terminal"},
    ],
)
def test_adapter_exceptions_are_no_echo_ambiguous_and_cleaned(
    raise_on: set[str],
) -> None:
    sentinel = "SYNTHETIC-PRIVATE-EXCEPTION-SENTINEL"
    adapter = FakeNativeAdapter(raise_on=raise_on, exception_text=sentinel)
    result = _run(adapter)
    payload = target.canonical_bytes(result)

    assert result["category"] == target.AMBIGUOUS_CATEGORY
    assert sentinel.encode("ascii") not in payload
    expected_process_calls = 0 if raise_on == {"observe_metadata"} else 1
    assert adapter.calls.count("create_suspended") == expected_process_calls
    assert adapter.calls.count("cleanup") == expected_process_calls
    assert adapter.calls.count("resume_once") <= 1
    assert adapter.calls.count("terminate_once") <= 1
    assert adapter.calls.count("wait_terminal") <= 1


def test_canonical_result_schema_digest_and_authority_are_exact() -> None:
    result = _run(FakeNativeAdapter())
    payload = target.canonical_bytes(result)

    assert tuple(result) == target.RESULT_FIELDS
    assert len(result) == 33
    assert tuple(result["authority_flags"]) == target.AUTHORITY_FIELDS
    assert len(result["authority_flags"]) == 18
    assert not any(result["authority_flags"].values())
    assert result["result_sha256"] == target.self_digest(result)
    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    assert json.loads(payload) == result
    assert target.parse_result(payload) == result


def _reseal(document: dict[str, object]) -> bytes:
    document["result_sha256"] = "0" * 64
    document["result_sha256"] = target.self_digest(document)
    return target.canonical_bytes(document)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda document: document.update(category=target.PRELAUNCH_MISMATCH_CATEGORY),
        lambda document: document.update(process_launch_count=0),
        lambda document: document.update(top_level_process_count=True),
        lambda document: document.update(exit_state="unknown"),
        lambda document: document.update(private_value_emitted=True),
        lambda document: document.update(eligible_for_independent_review=False),
        lambda document: document["authority_flags"].update(live_ready=True),
    ],
)
def test_negative_cross_field_and_false_authority_vectors_are_rejected(
    mutation,
) -> None:
    document = _run(FakeNativeAdapter())
    mutation(document)

    with pytest.raises(target.ResultValidationError):
        target.parse_result(_reseal(document))


def test_parser_rejects_duplicate_unknown_reordered_and_noncanonical_json() -> None:
    result = _run(FakeNativeAdapter())
    payload = target.canonical_bytes(result)
    duplicate = payload.replace(
        b'{"schema_version":',
        b'{"schema_version":"duplicate","schema_version":',
        1,
    )
    unknown = dict(result)
    unknown["unexpected"] = False
    reordered = {key: result[key] for key in reversed(tuple(result))}
    noncanonical = json.dumps(result, indent=2).encode("utf-8") + b"\n"

    for candidate in (
        duplicate,
        target.canonical_bytes(unknown),
        target.canonical_bytes(reordered),
        noncanonical,
        payload[:-1],
        payload + b"\n",
    ):
        with pytest.raises(target.ResultValidationError):
            target.parse_result(candidate)


def test_result_digest_uses_zero_replacement_without_final_lf() -> None:
    result = _run(FakeNativeAdapter())
    preimage = dict(result)
    preimage["result_sha256"] = "0" * 64
    expected = hashlib.sha256(
        json.dumps(preimage, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    assert result["result_sha256"] == expected


def test_private_path_metadata_and_machine_sentinels_never_enter_result() -> None:
    private_path = r"C:\SYNTHETIC-PRIVATE-PATH-SENTINEL\python.exe"
    private_metadata = replace(
        MISMATCH_METADATA,
        file_version="PRIVATE-VERSION-SENTINEL",
        product_version="PRIVATE-PRODUCT-SENTINEL",
        file_sha256="a" * 64,
        stable_identity_sha256="b" * 64,
    )
    adapter = FakeNativeAdapter(
        metadata=[target.MetadataObservation("available", private_metadata)],
        expected_path=private_path,
    )
    result = target.characterize_with_adapter(
        private_path,
        characterization_id=SYNTHETIC_ID,
        adapter=adapter,
        bindings=_bindings(),
        repository_root=REPOSITORY_ROOT,
    )
    payload = target.canonical_bytes(result)

    for sentinel in (
        "SYNTHETIC-PRIVATE-PATH-SENTINEL",
        "PRIVATE-VERSION-SENTINEL",
        "PRIVATE-PRODUCT-SENTINEL",
        "-B",
        "-c",
        "pass",
        "SystemRoot",
        "WINDIR",
    ):
        assert sentinel.encode("ascii") not in payload


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        SYNTHETIC_PATH.encode("utf-8"),
        (SYNTHETIC_PATH + "\r\n").encode("utf-8"),
        (SYNTHETIC_PATH + "\nextra\n").encode("utf-8"),
        (r"relative\python.exe" + "\n").encode("utf-8"),
        (r"C:\synthetic-private\py.exe" + "\n").encode("utf-8"),
        (r"C:\synthetic-private\pythonw.exe" + "\n").encode("utf-8"),
        (r"C:\WindowsApps\python.exe" + "\n").encode("utf-8"),
        b"\xef\xbb\xbf" + (SYNTHETIC_PATH + "\n").encode("utf-8"),
        b"C:\\synthetic-private\\py\x00thon.exe\n",
        b"\xff\n",
        ("C:\\" + "x" * target.MAX_PRIVATE_PATH_BYTES + "\\python.exe\n").encode("utf-8"),
    ],
)
def test_private_path_parser_rejects_noncontract_inputs(payload: bytes) -> None:
    with pytest.raises(target.CharacterizerError):
        target.parse_private_path_stdin(io.BytesIO(payload))


def test_private_path_parser_accepts_one_synthetic_copy_as_path_line_and_clears() -> None:
    bound = target.parse_private_path_stdin(
        io.BytesIO((SYNTHETIC_PATH + "\n").encode("utf-8"))
    )

    assert bound.value() == SYNTHETIC_PATH
    bound.clear()
    assert bound.value() == ""


@pytest.mark.parametrize(
    "value",
    [
        "",
        "UPPERCASE",
        "contains space",
        "contains/slash",
        "contains\\backslash",
        "a" * 129,
    ],
)
def test_characterization_id_is_closed_public_safe(value: str) -> None:
    with pytest.raises(target.CharacterizerError):
        target.characterize_with_adapter(
            SYNTHETIC_PATH,
            characterization_id=value,
            adapter=FakeNativeAdapter(),
            bindings=_bindings(),
            repository_root=REPOSITORY_ROOT,
        )


def test_production_wrapper_has_no_caller_selected_launch_controls() -> None:
    parameters = inspect.signature(target.run_consumed_characterization).parameters

    assert tuple(parameters) == ("characterization_id", "stdin", "stdout")
    assert all(parameter.kind is inspect.Parameter.KEYWORD_ONLY for parameter in parameters.values())


def test_public_bindings_are_exact_without_private_or_process_access() -> None:
    repository_root = Path(__file__).absolute().parent.parent
    bindings = target._public_bindings(repository_root)

    assert bindings.exact is True
    assert bindings.characterizer_sha256 == hashlib.sha256(
        (repository_root / target.CHARACTERIZER_PATH).read_bytes()
    ).hexdigest()
    assert bindings.characterizer_test_sha256 == hashlib.sha256(
        (repository_root / target.CHARACTERIZER_TEST_PATH).read_bytes()
    ).hexdigest()


def test_direct_module_entrypoint_remains_inert() -> None:
    source = inspect.getsource(target)

    assert 'if __name__ == "__main__":' in source
    assert "raise SystemExit(2)" in source
    assert "subprocess" not in source
