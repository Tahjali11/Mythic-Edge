from __future__ import annotations

import ast
import hashlib
import inspect
import itertools
from collections import deque
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import run_role_pool_r0_direct_interpreter_identity_characterizer as accepted
from tools import (
    run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress as target,
)

REPOSITORY_ROOT = Path(__file__).absolute().parent.parent
BOOTSTRAP_PATH = (
    REPOSITORY_ROOT
    / "tools"
    / "start_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.ps1"
)
CONTROLLER_PATH = REPOSITORY_ROOT / target.CONTROLLER_PATH
VALID_ID = "r0_direct_interpreter_identity_characterization_v1_0123456789abcdef0123456789abcdef"
VALID_DECISION = "https://github.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-5157000000"
SYNTHETIC_PRIVATE_PATH = r"C:\synthetic-private\python.exe"


def _canonical_payload() -> bytes:
    record = accepted.CharacterizationRecord(
        lifecycle_evidence_state="exact",
        prelaunch_metadata_state="exact",
        pre_resume_image_state="exact",
        post_exit_image_state="exact",
        postlaunch_metadata_state="available",
        metadata_equality_state="exact",
        process_launch_count=1,
        top_level_process_count=1,
        descendant_process_count=0,
        exit_state="zero",
        stdout_byte_count=0,
        stderr_byte_count=0,
        timed_out=False,
        streams_drained=True,
        cleanup_confirmed=True,
        surviving_process_count=0,
    )
    bindings = accepted.PublicBindingSnapshot(
        exact=True,
        characterizer_sha256="3" * 64,
        characterizer_test_sha256="4" * 64,
        parent_api=object(),
    )
    result = accepted.seal_result(
        record,
        bindings,
        VALID_ID,
        "2026-08-02T00:00:00Z",
    )
    return accepted.canonical_bytes(result)


CANONICAL_PAYLOAD = _canonical_payload()


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


class FakeConsole:
    def __init__(
        self,
        keys: list[str] | None = None,
        *,
        initial_pending: bool = False,
        initial_mode: int = 7,
        snapshot_fails: bool = False,
        ui_fails: bool = False,
        restore_ok: bool = True,
    ) -> None:
        self.keys = deque(keys or [])
        self.initial_pending = initial_pending
        self.mode = initial_mode
        self.snapshot_fails = snapshot_fails
        self.ui_fails = ui_fails
        self.restore_ok = restore_ok
        self.ready = False
        self.ui: list[str] = []
        self.read_count = 0
        self.restore_count = 0

    def snapshot_input_mode(self) -> int:
        if self.snapshot_fails:
            raise RuntimeError("synthetic-mode-failure")
        return self.mode

    def pending_input(self) -> bool:
        if not self.ready:
            return self.initial_pending
        return bool(self.keys)

    def read_key(self) -> str:
        self.read_count += 1
        return self.keys.popleft()

    def write_ui(self, value: str) -> None:
        if self.ui_fails:
            raise RuntimeError("synthetic-ui-failure")
        self.ui.append(value)
        self.ready = True

    def current_input_mode(self) -> int:
        return self.mode

    def restore_input_mode(self, mode: int) -> bool:
        self.restore_count += 1
        if not self.restore_ok:
            return False
        self.mode = mode
        return True


class FakePublicOutput:
    def __init__(
        self,
        *,
        write_state: str = "complete",
        flush_fails: bool = False,
    ) -> None:
        self.write_state = write_state
        self.flush_fails = flush_fails
        self.pending = bytearray()
        self.committed = bytearray()
        self.write_count = 0
        self.flush_count = 0

    def write(self, payload: bytes) -> int:
        self.write_count += 1
        if self.write_state == "failed":
            raise RuntimeError("synthetic-write-failure")
        if self.write_state == "incomplete":
            self.pending.extend(payload[:-1])
            return len(payload) - 1
        self.pending.extend(payload)
        return len(payload)

    def flush(self) -> None:
        self.flush_count += 1
        if self.flush_fails:
            raise RuntimeError("synthetic-flush-failure")
        self.committed.extend(self.pending)


class FakeCharacterizer:
    RESULT_FIELDS = accepted.RESULT_FIELDS
    AUTHORITY_FIELDS = accepted.AUTHORITY_FIELDS

    def __init__(
        self,
        *,
        code: int = 0,
        payload: bytes = CANONICAL_PAYLOAD,
        parse_fails: bool = False,
        aborts: bool = False,
        after_wrapper: object | None = None,
    ) -> None:
        self.code = code
        self.payload = payload
        self.parse_fails = parse_fails
        self.aborts = aborts
        self.after_wrapper = after_wrapper
        self.calls = 0
        self.inputs: list[bytes] = []
        self.reader: object | None = None
        self.sink: object | None = None

    def run_consumed_characterization(
        self,
        *,
        characterization_id: str,
        stdin: object,
        stdout: object,
    ) -> int:
        self.calls += 1
        assert characterization_id == VALID_ID
        self.reader = stdin
        self.sink = stdout
        self.inputs.append(stdin.read(4097))
        assert stdin.read(4097) == b""
        if self.aborts:
            raise SystemExit(99)
        if self.code == 0:
            assert stdout.write(self.payload) == len(self.payload)
            stdout.flush()
        if callable(self.after_wrapper):
            self.after_wrapper()
        return self.code

    def parse_result(self, payload: bytes) -> dict[str, object]:
        if self.parse_fails:
            raise RuntimeError("synthetic-parse-failure")
        return accepted.parse_result(payload)


def _loaded(characterizer: FakeCharacterizer) -> target.LoadedCharacterizer:
    parent = SimpleNamespace(validate_running_direct_interpreter=lambda: object())
    return target.LoadedCharacterizer(characterizer, parent)


def _public_arguments() -> target.PublicArguments:
    return target.parse_public_arguments(
        [
            "--characterization-id",
            VALID_ID,
            "--owner-decision-ref",
            VALID_DECISION,
        ]
    )


def _keys(value: str = SYNTHETIC_PRIVATE_PATH) -> list[str]:
    return [*value, "\r"]


def _run(
    characterizer: FakeCharacterizer | None = None,
    *,
    console: FakeConsole | None = None,
    output: FakePublicOutput | None = None,
    loader_fails: bool = False,
    runtime_fails: bool = False,
) -> tuple[int, FakeCharacterizer, FakeConsole, FakePublicOutput, list[str]]:
    selected_characterizer = characterizer or FakeCharacterizer()
    selected_console = console or FakeConsole(_keys())
    selected_output = output or FakePublicOutput()
    clock = FakeClock()
    events: list[str] = []

    def loader(_root: Path) -> target.LoadedCharacterizer:
        events.append("load")
        if loader_fails:
            raise RuntimeError("synthetic-loader-failure")
        return _loaded(selected_characterizer)

    def runtime_validator(_loaded_characterizer: target.LoadedCharacterizer) -> None:
        events.append("runtime")
        if runtime_fails:
            raise RuntimeError("synthetic-runtime-failure")

    code = target.run_secure_ingress(
        _public_arguments(),
        console=selected_console,
        stdout=selected_output,
        repository_root=Path(r"C:\synthetic-repository"),
        clock=clock,
        sleeper=clock.sleep,
        characterizer_loader=loader,
        runtime_validator=runtime_validator,
    )
    return code, selected_characterizer, selected_console, selected_output, events


def test_contract_and_review_bindings_are_exact() -> None:
    expected = {
        target.SECURE_INGRESS_CONTRACT_PATH: target.SECURE_INGRESS_CONTRACT_SHA256,
        target.SECURE_INGRESS_CONTRACT_REVIEW_PATH: target.SECURE_INGRESS_CONTRACT_REVIEW_SHA256,
    }
    for relative_path, digest in expected.items():
        path = REPOSITORY_ROOT / relative_path
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest


def test_exact_three_implementation_paths_exist() -> None:
    expected = {
        Path("tools/start_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.ps1"),
        target.CONTROLLER_PATH,
        Path("tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py"),
    }
    present = {
        path.relative_to(REPOSITORY_ROOT)
        for root in (REPOSITORY_ROOT / "tools", REPOSITORY_ROOT / "tests")
        for path in root.glob("*identity_characterizer_secure_ingress*")
    }
    assert present == expected


def test_bootstrap_pins_exact_public_files_and_controller_bytes() -> None:
    source = BOOTSTRAP_PATH.read_text(encoding="utf-8")
    controller_digest = hashlib.sha256(CONTROLLER_PATH.read_bytes()).hexdigest()

    assert target.SECURE_INGRESS_CONTRACT_SHA256 in source
    assert target.SECURE_INGRESS_CONTRACT_REVIEW_SHA256 in source
    assert controller_digest in source
    assert "$ControllerSha256" in source
    assert "Test-ExactSha256 -Path $controllerPath" in source
    assert "Test-OrdinaryNonReparseFile -Path $PSCommandPath" in source


def test_bootstrap_uses_one_in_process_no_echo_reader_and_one_controller_start() -> None:
    source = BOOTSTRAP_PATH.read_text(encoding="utf-8")

    assert source.count("[Console]::ReadKey($true)") == 1
    assert source.count("[Diagnostics.Process]::Start($startInfo)") == 1
    assert "$startInfo.UseShellExecute = $false" in source
    assert "$startInfo.FileName = $launchImage" in source
    assert "$startInfo.Arguments = $entry.Arguments" in source
    assert "$startInfo.WorkingDirectory = $entry.RepositoryRoot" in source
    assert "$startInfo.RedirectStandardInput = $false" in source
    assert "$startInfo.RedirectStandardOutput = $false" in source
    assert "$startInfo.RedirectStandardError = $false" in source


def test_bootstrap_has_exact_seven_public_argument_tokens() -> None:
    source = BOOTSTRAP_PATH.read_text(encoding="utf-8")
    maximum_id = "r0_direct_interpreter_identity_characterization_v1_" + "f" * 32
    maximum_ref = "https://github.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-" + "9" * 20
    tokens = [
        "-I",
        "-B",
        str(target.CONTROLLER_PATH).replace("/", "\\"),
        "--characterization-id",
        maximum_id,
        "--owner-decision-ref",
        maximum_ref,
    ]
    arguments = " ".join(tokens)

    assert len(tokens) == 7
    assert arguments.count(" ") == 6
    assert len(arguments.encode("utf-8")) == 301
    assert len(arguments.encode("utf-8")) <= 512
    assert "[string]::Join(' ', $ControllerReadinessArguments)" in source
    assert "$ControllerReadinessArguments.Count -ne 7" in source
    assert "[Diagnostics.ProcessStartInfo].GetProperty('Arguments')" in source
    assert "ArgumentList" not in source


@pytest.mark.parametrize(
    "forbidden",
    [
        "Start-Process",
        "Invoke-Expression",
        "Invoke-Command",
        "cmd.exe",
        "powershell.exe",
        "pwsh.exe",
        "$env:Path",
        "Get-Command",
        "RedirectStandardInput = $true",
        "RedirectStandardOutput = $true",
        "RedirectStandardError = $true",
        "System.Threading.Thread]::new",
        "System.Threading.Tasks.Task",
    ],
)
def test_bootstrap_forbids_alternate_launch_or_input_paths(forbidden: str) -> None:
    assert forbidden not in BOOTSTRAP_PATH.read_text(encoding="utf-8")


def test_controller_source_contains_no_process_creation_or_external_access_api() -> None:
    source = CONTROLLER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "subprocess" not in imported
    assert "socket" not in imported
    assert "requests" not in imported
    assert "urllib" not in imported
    for forbidden in (
        "Popen",
        "CreateProcessW",
        "ShellExecute",
        "os.system",
        "os.startfile",
        "winreg",
        "clipboard",
        "SetConsoleTitle",
    ):
        assert forbidden not in source


def test_controller_public_argument_shape_is_exact() -> None:
    parsed = _public_arguments()

    assert parsed.characterization_id == VALID_ID
    assert parsed.owner_decision_ref == VALID_DECISION


def test_internal_controller_entry_revalidates_public_arguments() -> None:
    malformed = target.PublicArguments(VALID_ID, VALID_DECISION + " ")
    console = FakeConsole(_keys())
    output = FakePublicOutput()
    clock = FakeClock()

    code = target.run_secure_ingress(
        malformed,
        console=console,
        stdout=output,
        repository_root=Path(r"C:\synthetic-repository"),
        clock=clock,
        sleeper=clock.sleep,
        characterizer_loader=lambda _root: pytest.fail("loader must not run"),
        runtime_validator=lambda _loaded_characterizer: pytest.fail("runtime must not run"),
    )

    assert code == 2
    assert console.ui == []
    assert console.read_count == 0
    assert output.write_count == 0


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["--characterization-id", VALID_ID],
        ["--owner-decision-ref", VALID_DECISION, "--characterization-id", VALID_ID],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION, "extra"],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", "--option"],
        ["--characterization-id", VALID_ID.upper(), "--owner-decision-ref", VALID_DECISION],
        ["--characterization-id", VALID_ID[:-1], "--owner-decision-ref", VALID_DECISION],
        ["--characterization-id", VALID_ID + "0", "--owner-decision-ref", VALID_DECISION],
        ["--characterization-id", VALID_ID + " ", "--owner-decision-ref", VALID_DECISION],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION.replace("795", "780")],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION + " "],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION.replace("https", "http")],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION.replace("#", "/")],
        ["--characterization-id", VALID_ID, "--owner-decision-ref", VALID_DECISION.replace("5157", "05157")],
    ],
)
def test_controller_rejects_nonexact_public_arguments(arguments: list[str]) -> None:
    with pytest.raises(target.SecureIngressError):
        target.parse_public_arguments(arguments)


def test_terminal_selector_preserves_nine_values_and_conflict_precedence() -> None:
    codes = tuple(target.TERMINAL_PHASE_BY_CODE)
    cases = [(code,) for code in codes]
    cases.extend(itertools.combinations(codes, 2))
    selected = [target.select_terminal_phase(case) for case in cases]

    assert len(codes) == 9
    assert set(selected[:9]) == set(target.TERMINAL_PHASE_BY_CODE.values())
    assert all(value == "unknown" for value in selected[9:])
    assert target.select_terminal_phase((99,)) == "unknown"
    assert target.select_terminal_phase(()) == "unknown"


def test_one_shot_reader_returns_one_line_then_eof_and_has_safe_repr() -> None:
    payload = bytearray(b"synthetic-private-value\n")
    reader = target.OneShotPrivateLineReader(payload)

    assert "synthetic-private-value" not in repr(reader)
    assert reader.read(4097) == b"synthetic-private-value\n"
    assert reader.read(4097) == b""
    reader.clear()
    assert reader.clear_attempted is True
    assert payload == bytearray()


def test_one_shot_reader_rejects_partial_or_invalid_reads() -> None:
    reader = target.OneShotPrivateLineReader(bytearray(b"private\n"))

    with pytest.raises(target.SecureIngressError):
        reader.read(1)
    with pytest.raises(target.SecureIngressError):
        reader.read(0)


def test_bounded_sink_enforces_limit_and_clears() -> None:
    sink = target.BoundedOutputSink()
    payload = b"x" * target.MAX_OUTPUT_BYTES

    assert sink.write(payload) == len(payload)
    with pytest.raises(target.SecureIngressError):
        sink.write(b"x")
    assert sink.value() == payload
    sink.clear()
    assert sink.clear_attempted is True
    assert sink.value() == b""


def test_private_ingress_projects_one_lf_without_echo() -> None:
    console = FakeConsole(_keys())
    console.ready = True
    clock = FakeClock()

    reader = target._read_private_line(console, clock=clock, sleeper=clock.sleep)

    assert reader.read(4097) == SYNTHETIC_PRIVATE_PATH.encode("utf-8") + b"\n"
    assert console.ui == []
    assert console.read_count == len(SYNTHETIC_PRIVATE_PATH) + 1
    reader.clear()


def test_private_ingress_handles_unicode_scalar_and_backspace_as_one_unit() -> None:
    prefix = "C:\\synthetic-private"
    keys = [*prefix, "\ud83d", "\ude00", "\b", *"\\python.exe", "\r"]
    console = FakeConsole(keys)
    console.ready = True
    clock = FakeClock()

    reader = target._read_private_line(console, clock=clock, sleeper=clock.sleep)

    assert reader.read(4097) == SYNTHETIC_PRIVATE_PATH.encode("utf-8") + b"\n"
    reader.clear()


@pytest.mark.parametrize(
    "keys",
    [
        ["\x00"],
        ["\xe0"],
        ["\n"],
        ["\x01"],
        ["\b"],
        ["\udc00"],
        ["\ud800", "\r"],
        ["\ud800", "x"],
    ],
)
def test_private_ingress_rejects_control_special_and_malformed_unicode(keys: list[str]) -> None:
    console = FakeConsole(keys)
    console.ready = True
    clock = FakeClock()

    with pytest.raises(target.SecureIngressError):
        target._read_private_line(console, clock=clock, sleeper=clock.sleep)


def test_private_ingress_rejects_buffered_second_line() -> None:
    console = FakeConsole([*_keys(), *"second-line", "\r"])
    console.ready = True
    clock = FakeClock()

    with pytest.raises(target.SecureIngressError):
        target._read_private_line(console, clock=clock, sleeper=clock.sleep)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "python.exe",
        r"\\server\share\python.exe",
        r"C:\synthetic-private\Python.exe",
        r"C:\synthetic-private\pythonw.exe",
        r"C:\WindowsApps\python.exe",
    ],
)
def test_private_ingress_rejects_nonbound_path_shapes(value: str) -> None:
    console = FakeConsole(_keys(value))
    console.ready = True
    clock = FakeClock()

    with pytest.raises(target.SecureIngressError):
        target._read_private_line(console, clock=clock, sleeper=clock.sleep)


def test_private_ingress_rejects_overflow_before_wrapper_projection() -> None:
    value = "C:\\" + "x" * 4090 + "\\python.exe"
    console = FakeConsole(_keys(value))
    console.ready = True
    clock = FakeClock()

    with pytest.raises(target.SecureIngressError):
        target._read_private_line(console, clock=clock, sleeper=clock.sleep)


def test_private_ingress_timeout_is_bounded() -> None:
    console = FakeConsole([])
    console.ready = True
    clock = FakeClock()

    with pytest.raises(target.SecureIngressError):
        target._read_private_line(console, clock=clock, sleeper=clock.sleep)
    assert clock.value >= target.PRIVATE_INPUT_TIMEOUT_SECONDS
    assert console.read_count == 0


def test_success_calls_wrapper_once_and_routes_byte_identical_result() -> None:
    code, characterizer, console, output, events = _run()

    assert code == 0
    assert events == ["load", "runtime"]
    assert characterizer.calls == 1
    assert characterizer.inputs == [SYNTHETIC_PRIVATE_PATH.encode("utf-8") + b"\n"]
    assert characterizer.reader.clear_attempted is True
    assert characterizer.sink.clear_attempted is True
    assert console.ui == [target.READINESS_LINE]
    assert output.write_count == 1
    assert output.flush_count == 1
    assert bytes(output.committed) == CANONICAL_PAYLOAD
    parsed = accepted.parse_result(bytes(output.committed))
    assert tuple(parsed) == accepted.RESULT_FIELDS
    assert tuple(parsed["authority_flags"]) == accepted.AUTHORITY_FIELDS
    assert len(parsed["authority_flags"]) == 18
    assert not any(parsed["authority_flags"].values())


@pytest.mark.parametrize("code", [2, 10, 11, 12, 13, 14, 15, 16])
def test_known_nonzero_wrapper_codes_are_preserved_without_public_result(code: int) -> None:
    result, characterizer, _console, output, _events = _run(FakeCharacterizer(code=code))

    assert result == code
    assert characterizer.calls == 1
    assert output.write_count == 0
    assert bytes(output.committed) == b""


@pytest.mark.parametrize("code", [-1, 1, 3, 9, 17, 99])
def test_unknown_wrapper_code_fails_closed(code: int) -> None:
    result, characterizer, _console, output, _events = _run(FakeCharacterizer(code=code))

    assert result == 2
    assert characterizer.calls == 1
    assert output.write_count == 0


def test_wrapper_abort_fails_closed_without_retry_or_output() -> None:
    result, characterizer, _console, output, _events = _run(FakeCharacterizer(aborts=True))

    assert result == 2
    assert characterizer.calls == 1
    assert output.write_count == 0


def test_private_reader_abort_fails_closed_without_wrapper_or_output() -> None:
    console = FakeConsole(_keys())

    def aborting_read() -> str:
        raise KeyboardInterrupt

    console.read_key = aborting_read  # type: ignore[method-assign]
    result, characterizer, selected_console, output, _events = _run(console=console)

    assert result == 2
    assert characterizer.calls == 0
    assert selected_console.ui == [target.READINESS_LINE]
    assert output.write_count == 0


def test_invalid_wrapper_result_fails_before_public_write() -> None:
    result, characterizer, _console, output, _events = _run(
        FakeCharacterizer(payload=b'{}\n', parse_fails=True)
    )

    assert result == 2
    assert characterizer.calls == 1
    assert output.write_count == 0


@pytest.mark.parametrize(
    ("boundary", "expected_events", "expected_ui"),
    [
        ("loader", ["load"], []),
        ("runtime", ["load", "runtime"], []),
        ("snapshot", ["load", "runtime"], []),
        ("stale", ["load", "runtime"], []),
        ("ui", ["load", "runtime"], []),
    ],
)
def test_readiness_first_failures_never_read_private_input_or_call_wrapper(
    boundary: str,
    expected_events: list[str],
    expected_ui: list[str],
) -> None:
    console = FakeConsole(
        _keys(),
        initial_pending=boundary == "stale",
        snapshot_fails=boundary == "snapshot",
        ui_fails=boundary == "ui",
    )
    result, characterizer, selected_console, output, events = _run(
        console=console,
        loader_fails=boundary == "loader",
        runtime_fails=boundary == "runtime",
    )

    assert result == 2
    assert events == expected_events
    assert characterizer.calls == 0
    assert selected_console.read_count == 0
    assert selected_console.ui == expected_ui
    assert output.write_count == 0


def test_private_ingress_failure_never_calls_wrapper() -> None:
    console = FakeConsole([*r"C:\not-python.txt", "\r"])

    result, characterizer, selected_console, output, _events = _run(console=console)

    assert result == 2
    assert characterizer.calls == 0
    assert selected_console.ui == [target.READINESS_LINE]
    assert output.write_count == 0


def test_console_mode_drift_is_restored_before_result_write() -> None:
    console = FakeConsole(_keys(), initial_mode=7)
    characterizer = FakeCharacterizer(after_wrapper=lambda: setattr(console, "mode", 9))

    result, _characterizer, selected_console, output, _events = _run(
        characterizer,
        console=console,
    )

    assert result == 0
    assert selected_console.restore_count == 1
    assert selected_console.mode == 7
    assert bytes(output.committed) == CANONICAL_PAYLOAD


def test_unconfirmed_console_restoration_discards_result() -> None:
    console = FakeConsole(_keys(), initial_mode=7, restore_ok=False)
    characterizer = FakeCharacterizer(after_wrapper=lambda: setattr(console, "mode", 9))

    result, _characterizer, selected_console, output, _events = _run(
        characterizer,
        console=console,
    )

    assert result == 2
    assert selected_console.restore_count == 1
    assert output.write_count == 0


@pytest.mark.parametrize(
    ("write_state", "flush_fails"),
    [("failed", False), ("incomplete", False), ("complete", True)],
)
def test_controller_stdout_failure_is_unknown_and_not_committed(
    write_state: str,
    flush_fails: bool,
) -> None:
    output = FakePublicOutput(write_state=write_state, flush_fails=flush_fails)

    result, characterizer, _console, selected_output, _events = _run(output=output)

    assert result == 2
    assert characterizer.calls == 1
    assert bytes(selected_output.committed) == b""


def test_actual_loader_validates_frozen_public_artifacts_without_runtime_probe() -> None:
    loaded = target.load_accepted_characterizer(REPOSITORY_ROOT)
    parameters = inspect.signature(loaded.module.run_consumed_characterization).parameters

    assert tuple(parameters) == ("characterization_id", "stdin", "stdout")
    assert all(parameter.kind is inspect.Parameter.KEYWORD_ONLY for parameter in parameters.values())
    assert len(loaded.module.RESULT_FIELDS) == 33
    assert len(loaded.module.AUTHORITY_FIELDS) == 18
    assert callable(loaded.parent_api.validate_running_direct_interpreter)


def test_runtime_validator_is_called_before_readiness() -> None:
    result, characterizer, console, output, events = _run(runtime_fails=True)

    assert result == 2
    assert events == ["load", "runtime"]
    assert characterizer.calls == 0
    assert console.ui == []
    assert console.read_count == 0
    assert output.write_count == 0


def test_controller_main_rejects_invalid_arguments_without_constructing_console(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    constructed = False

    def fail_if_constructed() -> object:
        nonlocal constructed
        constructed = True
        raise AssertionError

    monkeypatch.setattr(target, "WindowsConsolePort", fail_if_constructed)

    assert target.main([]) == 2
    assert constructed is False


def test_secure_ingress_has_no_durable_or_coordination_surface() -> None:
    source = CONTROLLER_PATH.read_text(encoding="utf-8")
    bootstrap = BOOTSTRAP_PATH.read_text(encoding="utf-8")

    for forbidden in (
        "issuecomment-5156641209",
        "issues/769",
        "sqlite",
        "registry",
        "receipt",
        "release_state",
        "R1",
        "canary",
    ):
        assert forbidden not in source
        assert forbidden not in bootstrap


def test_controller_import_is_inert_and_direct_entry_is_explicit() -> None:
    source = CONTROLLER_PATH.read_text(encoding="utf-8")

    assert 'if __name__ == "__main__":' in source
    assert "raise SystemExit(main())" in source
    assert target.REPOSITORY_ID == 1235264383
    assert target.ISSUE_NUMBER == 795
    assert target.PARENT_ISSUE_NUMBER == 780
    assert target.DIRECT_INTERPRETER_BINDING_SHA256 == accepted.DIRECT_INTERPRETER_BINDING_SHA256
