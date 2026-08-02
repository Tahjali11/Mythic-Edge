"""Secure, no-echo ingress for the accepted R0 identity characterizer.

The controller is inert on import. A separately authorized PowerShell bootstrap
starts it with public arguments only. The controller then validates its fixed
runtime and repository bindings, reads one private path from an inherited
Windows console without echo, and invokes the accepted characterizer wrapper
once in-process.
"""

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import inspect
import ntpath
import os
import re
import stat
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import BinaryIO, Protocol

REPOSITORY_ID = 1235264383
ISSUE_NUMBER = 795
PARENT_ISSUE_NUMBER = 780

SECURE_INGRESS_CONTRACT_SHA256 = (
    "7c7d5cd414b8a893703b014d470b84800b3444a11fe498135a7dd965adeacb69"
)
SECURE_INGRESS_CONTRACT_REVIEW_SHA256 = (
    "ceac5499f7d281e99cefea69a4684debc6d86b5bc50fb29dff1eae25fca971f5"
)
CHARACTERIZER_SHA256 = (
    "46404b68c7005ff1df06c24426514ceedc8478956b95fbb1c753e247550bd1d0"
)
CHARACTERIZER_TEST_SHA256 = (
    "64e6ba5bae8bf75908212f521658853e100ca53686005495255b767653a47493"
)
CHARACTERIZER_CONTRACT_SHA256 = (
    "42661d3f445c7d93e6253105c09d27454a96607b9acb2f7b2499290abcfda904"
)
CHARACTERIZER_CONTRACT_REVIEW_SHA256 = (
    "89ee9144a2dee459a819259f05db7b659c6dc589fc8ef635234333f0e03a2127"
)
CHARACTERIZER_IMPLEMENTATION_REVIEW_SHA256 = (
    "e7194ec6dad4ed1a678c18f7d80fa9155d257b290c2bf53142ee9d1f1de71dff"
)
TERMINAL_OBSERVABILITY_CONTRACT_SHA256 = (
    "f1e9ab7642ba191edf5568638c83fe4df01babae5b379733d6172a2e426e33a1"
)
TERMINAL_OBSERVABILITY_REVIEW_SHA256 = (
    "78a46dfafbfb5fc61cb0b22937cb96873873acf8173d2af89bbbd7132e2572c6"
)
DIRECT_INTERPRETER_BINDING_SHA256 = (
    "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
)

SECURE_INGRESS_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_"
    "identity_characterizer_secure_ingress_successor.md"
)
SECURE_INGRESS_CONTRACT_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
    "interpreter_identity_characterizer_secure_ingress_successor.md"
)
CHARACTERIZER_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_"
    "identity_characterizer.md"
)
CHARACTERIZER_CONTRACT_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
    "interpreter_identity_characterizer.md"
)
CHARACTERIZER_IMPLEMENTATION_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
    "interpreter_identity_characterizer_implementation.md"
)
TERMINAL_OBSERVABILITY_CONTRACT_PATH = Path(
    "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_"
    "identity_characterizer_terminal_observability_successor.md"
)
TERMINAL_OBSERVABILITY_REVIEW_PATH = Path(
    "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_"
    "interpreter_identity_characterizer_terminal_observability_successor.md"
)
CHARACTERIZER_PATH = Path(
    "tools/run_role_pool_r0_direct_interpreter_identity_characterizer.py"
)
CHARACTERIZER_TEST_PATH = Path(
    "tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py"
)
CONTROLLER_PATH = Path(
    "tools/run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py"
)

FROZEN_PUBLIC_ARTIFACTS = {
    SECURE_INGRESS_CONTRACT_PATH: SECURE_INGRESS_CONTRACT_SHA256,
    SECURE_INGRESS_CONTRACT_REVIEW_PATH: SECURE_INGRESS_CONTRACT_REVIEW_SHA256,
    CHARACTERIZER_CONTRACT_PATH: CHARACTERIZER_CONTRACT_SHA256,
    CHARACTERIZER_CONTRACT_REVIEW_PATH: CHARACTERIZER_CONTRACT_REVIEW_SHA256,
    CHARACTERIZER_IMPLEMENTATION_REVIEW_PATH: CHARACTERIZER_IMPLEMENTATION_REVIEW_SHA256,
    TERMINAL_OBSERVABILITY_CONTRACT_PATH: TERMINAL_OBSERVABILITY_CONTRACT_SHA256,
    TERMINAL_OBSERVABILITY_REVIEW_PATH: TERMINAL_OBSERVABILITY_REVIEW_SHA256,
    CHARACTERIZER_PATH: CHARACTERIZER_SHA256,
    CHARACTERIZER_TEST_PATH: CHARACTERIZER_TEST_SHA256,
}

READINESS_LINE = "R0 identity characterizer target ingress ready; enter the bound path."
MAX_PRIVATE_PATH_BYTES = 4095
MAX_KEY_READS = 8192
MAX_AVAILABILITY_POLLS = 12001
PRIVATE_INPUT_TIMEOUT_SECONDS = 120.0
MAX_OUTPUT_BYTES = 4096

CHARACTERIZATION_ID_PATTERN = re.compile(
    r"r0_direct_interpreter_identity_characterization_v1_[0-9a-f]{32}\Z"
)
OWNER_DECISION_REF_PATTERN = re.compile(
    r"https://github\.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-[1-9][0-9]{0,19}\Z"
)

TERMINAL_PHASE_BY_CODE = {
    10: "id_validation_failed",
    11: "public_binding_validation_failed",
    12: "private_ingress_failed",
    13: "characterization_failed",
    14: "canonical_sealing_failed",
    15: "stdout_write_failed",
    16: "stdout_flush_failed",
    0: "wrapper_complete",
    2: "unknown",
}


class SecureIngressError(RuntimeError):
    """A symbolic controller failure that carries no private detail."""


@dataclass(frozen=True)
class PublicArguments:
    characterization_id: str
    owner_decision_ref: str


@dataclass(frozen=True)
class LoadedCharacterizer:
    module: ModuleType
    parent_api: ModuleType | object


class ConsolePort(Protocol):
    def snapshot_input_mode(self) -> int: ...

    def pending_input(self) -> bool: ...

    def read_key(self) -> str: ...

    def write_ui(self, value: str) -> None: ...

    def current_input_mode(self) -> int: ...

    def restore_input_mode(self, mode: int) -> bool: ...


def _is_ordinal_ascii(value: str) -> bool:
    return bool(value) and all(0x21 <= ord(character) <= 0x7E for character in value)


def parse_public_arguments(arguments: Sequence[str]) -> PublicArguments:
    if type(arguments) not in {list, tuple} or len(arguments) != 4:
        raise SecureIngressError
    option_a, characterization_id, option_b, owner_decision_ref = arguments
    if option_a != "--characterization-id" or option_b != "--owner-decision-ref":
        raise SecureIngressError
    if type(characterization_id) is not str or type(owner_decision_ref) is not str:
        raise SecureIngressError
    if not _is_ordinal_ascii(characterization_id) or not _is_ordinal_ascii(owner_decision_ref):
        raise SecureIngressError
    if CHARACTERIZATION_ID_PATTERN.fullmatch(characterization_id) is None:
        raise SecureIngressError
    if OWNER_DECISION_REF_PATTERN.fullmatch(owner_decision_ref) is None:
        raise SecureIngressError
    return PublicArguments(characterization_id, owner_decision_ref)


def select_terminal_phase(codes: Sequence[int]) -> str:
    if type(codes) not in {list, tuple} or len(codes) != 1:
        return "unknown"
    code = codes[0]
    if type(code) is not int:
        return "unknown"
    return TERMINAL_PHASE_BY_CODE.get(code, "unknown")


def _stable_file_sha256(path: Path) -> str:
    before = path.lstat()
    attributes = getattr(before, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if not stat.S_ISREG(before.st_mode) or attributes & reparse:
        raise SecureIngressError
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size) != (
            before.st_dev,
            before.st_ino,
            before.st_size,
        ):
            raise SecureIngressError
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise SecureIngressError
    if identity != (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns):
        raise SecureIngressError
    return digest.hexdigest()


def _validate_controller_source(repository_root: Path) -> None:
    expected = repository_root / CONTROLLER_PATH
    current = Path(__file__).absolute()
    if os.path.normcase(os.path.abspath(current)) != os.path.normcase(os.path.abspath(expected)):
        raise SecureIngressError
    _stable_file_sha256(expected)


def load_accepted_characterizer(repository_root: Path) -> LoadedCharacterizer:
    if Path.cwd() != repository_root:
        raise SecureIngressError
    _validate_controller_source(repository_root)
    for relative_path, expected_digest in FROZEN_PUBLIC_ARTIFACTS.items():
        if _stable_file_sha256(repository_root / relative_path) != expected_digest:
            raise SecureIngressError

    path = repository_root / CHARACTERIZER_PATH
    spec = importlib.util.spec_from_file_location("_r0_secure_ingress_characterizer", path)
    if spec is None or spec.loader is None:
        raise SecureIngressError
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        wrapper = getattr(module, "run_consumed_characterization", None)
        parser = getattr(module, "parse_result", None)
        result_fields = getattr(module, "RESULT_FIELDS", ())
        authority_fields = getattr(module, "AUTHORITY_FIELDS", ())
        if not callable(wrapper) or not callable(parser):
            raise SecureIngressError
        parameters = inspect.signature(wrapper).parameters
        if tuple(parameters) != ("characterization_id", "stdin", "stdout"):
            raise SecureIngressError
        if any(parameter.kind is not inspect.Parameter.KEYWORD_ONLY for parameter in parameters.values()):
            raise SecureIngressError
        if len(result_fields) != 33 or len(authority_fields) != 18:
            raise SecureIngressError
        bindings = module._public_bindings(repository_root)
        if (
            bindings.exact is not True
            or bindings.characterizer_sha256 != CHARACTERIZER_SHA256
            or bindings.characterizer_test_sha256 != CHARACTERIZER_TEST_SHA256
        ):
            raise SecureIngressError
        runtime_validator = getattr(bindings.parent_api, "validate_running_direct_interpreter", None)
        if not callable(runtime_validator):
            raise SecureIngressError
    except BaseException as exc:
        sys.modules.pop(spec.name, None)
        if isinstance(exc, SecureIngressError):
            raise
        raise SecureIngressError from exc
    return LoadedCharacterizer(module, bindings.parent_api)


def validate_running_runtime(loaded: LoadedCharacterizer) -> None:
    if (
        os.name != "nt"
        or sys.platform != "win32"
        or sys.implementation.name != "cpython"
        or sys.version_info[:3] != (3, 13, 14)
        or ntpath.basename(sys.executable) != "python.exe"
    ):
        raise SecureIngressError
    validator = getattr(loaded.parent_api, "validate_running_direct_interpreter", None)
    if not callable(validator):
        raise SecureIngressError
    try:
        metadata = validator()
    except BaseException as exc:
        raise SecureIngressError from exc
    if metadata is None:
        raise SecureIngressError


class WindowsConsolePort:
    """Narrow inherited-console adapter; construction performs no input read."""

    _STD_INPUT_HANDLE = -10
    _FILE_TYPE_CHAR = 0x0001

    def __init__(self) -> None:
        if os.name != "nt" or sys.platform != "win32" or not sys.stdin.isatty():
            raise SecureIngressError
        try:
            import msvcrt

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GetStdHandle.argtypes = (ctypes.c_int,)
            kernel32.GetStdHandle.restype = ctypes.c_void_p
            kernel32.GetFileType.argtypes = (ctypes.c_void_p,)
            kernel32.GetFileType.restype = ctypes.c_uint32
            kernel32.GetConsoleMode.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32))
            kernel32.GetConsoleMode.restype = ctypes.c_int
            kernel32.SetConsoleMode.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
            kernel32.SetConsoleMode.restype = ctypes.c_int
            handle = kernel32.GetStdHandle(self._STD_INPUT_HANDLE)
            if handle in {None, 0, ctypes.c_void_p(-1).value}:
                raise SecureIngressError
            if kernel32.GetFileType(handle) != self._FILE_TYPE_CHAR:
                raise SecureIngressError
            if msvcrt.get_osfhandle(sys.stdin.fileno()) != handle:
                raise SecureIngressError
            if not all(callable(value) for value in (msvcrt.kbhit, msvcrt.getwch, msvcrt.putwch)):
                raise SecureIngressError
        except BaseException as exc:
            if isinstance(exc, SecureIngressError):
                raise
            raise SecureIngressError from exc
        self._msvcrt = msvcrt
        self._kernel32 = kernel32
        self._handle = handle

    def snapshot_input_mode(self) -> int:
        return self.current_input_mode()

    def pending_input(self) -> bool:
        return bool(self._msvcrt.kbhit())

    def read_key(self) -> str:
        value = self._msvcrt.getwch()
        if type(value) is not str or len(value) != 1:
            raise SecureIngressError
        return value

    def write_ui(self, value: str) -> None:
        if type(value) is not str or not value:
            raise SecureIngressError
        for character in value + "\r\n":
            self._msvcrt.putwch(character)

    def current_input_mode(self) -> int:
        mode = ctypes.c_uint32()
        if not self._kernel32.GetConsoleMode(self._handle, ctypes.byref(mode)):
            raise SecureIngressError
        return int(mode.value)

    def restore_input_mode(self, mode: int) -> bool:
        if type(mode) is not int or mode < 0:
            return False
        try:
            if not self._kernel32.SetConsoleMode(self._handle, mode):
                return False
            return self.current_input_mode() == mode
        except BaseException:
            return False


class OneShotPrivateLineReader:
    __slots__ = ("_buffer", "_consumed", "clear_attempted")

    def __init__(self, payload: bytearray) -> None:
        self._buffer = payload
        self._consumed = False
        self.clear_attempted = False

    def __repr__(self) -> str:
        return "<OneShotPrivateLineReader>"

    def read(self, size: int = -1) -> bytes:
        if self._consumed:
            return b""
        if type(size) is not int or size == 0 or size < -1:
            raise SecureIngressError
        if size != -1 and size < len(self._buffer):
            raise SecureIngressError
        self._consumed = True
        return bytes(self._buffer)

    def clear(self) -> None:
        self.clear_attempted = True
        for index in range(len(self._buffer)):
            self._buffer[index] = 0
        self._buffer.clear()


class BoundedOutputSink:
    __slots__ = ("_buffer", "clear_attempted", "flush_count")

    def __init__(self) -> None:
        self._buffer = bytearray()
        self.clear_attempted = False
        self.flush_count = 0

    def write(self, payload: bytes) -> int:
        if type(payload) is not bytes or len(self._buffer) + len(payload) > MAX_OUTPUT_BYTES:
            raise SecureIngressError
        self._buffer.extend(payload)
        return len(payload)

    def flush(self) -> None:
        self.flush_count += 1

    def value(self) -> bytes:
        return bytes(self._buffer)

    def clear(self) -> None:
        self.clear_attempted = True
        for index in range(len(self._buffer)):
            self._buffer[index] = 0
        self._buffer.clear()


def _validate_private_path_text(value: str) -> None:
    if type(value) is not str or not value or "\x00" in value:
        raise SecureIngressError
    if not ntpath.isabs(value) or ntpath.basename(value) != "python.exe":
        raise SecureIngressError
    drive, tail = ntpath.splitdrive(value)
    components = tuple(
        component.casefold()
        for component in value.replace("/", "\\").split("\\")
        if component
    )
    if (
        len(drive) != 2
        or drive[1] != ":"
        or not drive[0].isalpha()
        or not tail.startswith(("\\", "/"))
        or "windowsapps" in components
    ):
        raise SecureIngressError


def _read_private_line(
    console: ConsolePort,
    *,
    clock: Callable[[], float],
    sleeper: Callable[[float], None],
) -> OneShotPrivateLineReader:
    scalars: list[str] = []
    pending_high_surrogate: str | None = None
    utf8_length = 0
    key_reads = 0
    polls = 0
    start = clock()
    try:
        while True:
            if polls >= MAX_AVAILABILITY_POLLS or clock() - start >= PRIVATE_INPUT_TIMEOUT_SECONDS:
                raise SecureIngressError
            polls += 1
            if not console.pending_input():
                sleeper(0.01)
                continue
            if key_reads >= MAX_KEY_READS or clock() - start >= PRIVATE_INPUT_TIMEOUT_SECONDS:
                raise SecureIngressError
            character = console.read_key()
            key_reads += 1
            if type(character) is not str or len(character) != 1:
                raise SecureIngressError
            codepoint = ord(character)
            if character in {"\x00", "\xe0", "\n"}:
                raise SecureIngressError
            if character == "\r":
                if pending_high_surrogate is not None:
                    raise SecureIngressError
                break
            if character == "\b":
                if pending_high_surrogate is not None:
                    raise SecureIngressError
                if not scalars:
                    raise SecureIngressError
                removed = scalars.pop()
                utf8_length -= len(removed.encode("utf-8"))
                continue
            if 0xD800 <= codepoint <= 0xDBFF:
                if pending_high_surrogate is not None:
                    raise SecureIngressError
                pending_high_surrogate = character
                continue
            if 0xDC00 <= codepoint <= 0xDFFF:
                if pending_high_surrogate is None:
                    raise SecureIngressError
                high = ord(pending_high_surrogate)
                scalar = chr(0x10000 + ((high - 0xD800) << 10) + (codepoint - 0xDC00))
                pending_high_surrogate = None
            else:
                if pending_high_surrogate is not None or codepoint < 0x20 or codepoint == 0x7F:
                    raise SecureIngressError
                scalar = character
            scalar_length = len(scalar.encode("utf-8"))
            if utf8_length + scalar_length > MAX_PRIVATE_PATH_BYTES:
                raise SecureIngressError
            scalars.append(scalar)
            utf8_length += scalar_length

        if console.pending_input():
            raise SecureIngressError
        value = "".join(scalars)
        _validate_private_path_text(value)
        encoded = bytearray(value.encode("utf-8"))
        if not encoded or len(encoded) > MAX_PRIVATE_PATH_BYTES:
            raise SecureIngressError
        encoded.append(0x0A)
        return OneShotPrivateLineReader(encoded)
    except BaseException as exc:
        if isinstance(exc, SecureIngressError):
            raise
        raise SecureIngressError from exc
    finally:
        pending_high_surrogate = None
        for index, scalar in enumerate(scalars):
            scalars[index] = "\x00" * len(scalar)
        scalars.clear()


def _console_state_exact_or_restored(console: ConsolePort, initial_mode: int | None) -> bool:
    if initial_mode is None:
        return True
    try:
        current = console.current_input_mode()
        if current == initial_mode:
            return True
        if console.restore_input_mode(initial_mode) is not True:
            return False
        return console.current_input_mode() == initial_mode
    except BaseException:
        return False


def run_secure_ingress(
    public_arguments: PublicArguments,
    *,
    console: ConsolePort,
    stdout: BinaryIO,
    repository_root: Path,
    clock: Callable[[], float],
    sleeper: Callable[[float], None],
    characterizer_loader: Callable[[Path], LoadedCharacterizer] = load_accepted_characterizer,
    runtime_validator: Callable[[LoadedCharacterizer], None] = validate_running_runtime,
) -> int:
    initial_mode: int | None = None
    private_line: OneShotPrivateLineReader | None = None
    sink: BoundedOutputSink | None = None
    payload: bytes | None = None
    result_code = 2
    try:
        if type(public_arguments) is not PublicArguments:
            raise SecureIngressError
        reparsed = parse_public_arguments(
            [
                "--characterization-id",
                public_arguments.characterization_id,
                "--owner-decision-ref",
                public_arguments.owner_decision_ref,
            ]
        )
        if reparsed != public_arguments:
            raise SecureIngressError
        if not callable(getattr(stdout, "write", None)) or not callable(getattr(stdout, "flush", None)):
            raise SecureIngressError
        loaded = characterizer_loader(repository_root)
        runtime_validator(loaded)
        initial_mode = console.snapshot_input_mode()
        if type(initial_mode) is not int or initial_mode < 0 or console.pending_input():
            raise SecureIngressError
        console.write_ui(READINESS_LINE)
        private_line = _read_private_line(console, clock=clock, sleeper=sleeper)
        sink = BoundedOutputSink()
        wrapper = loaded.module.run_consumed_characterization
        wrapper_code = wrapper(
            characterization_id=public_arguments.characterization_id,
            stdin=private_line,
            stdout=sink,
        )
        phase = select_terminal_phase((wrapper_code,))
        if phase == "unknown" and wrapper_code != 2:
            result_code = 2
        elif wrapper_code != 0:
            result_code = wrapper_code
        else:
            candidate = sink.value()
            loaded.module.parse_result(candidate)
            payload = candidate
            result_code = 0
    except BaseException:
        result_code = 2
        payload = None
    finally:
        cleanup_exact = True
        if private_line is not None:
            try:
                private_line.clear()
            except BaseException:
                cleanup_exact = False
        if sink is not None:
            try:
                sink.clear()
            except BaseException:
                cleanup_exact = False
        if not _console_state_exact_or_restored(console, initial_mode):
            cleanup_exact = False
        if not cleanup_exact:
            result_code = 2
            payload = None

    if result_code != 0 or payload is None:
        return result_code
    try:
        written = stdout.write(payload)
        if type(written) is not int or written != len(payload):
            return 2
        stdout.flush()
    except BaseException:
        return 2
    return 0


def main(arguments: Sequence[str] | None = None) -> int:
    try:
        public_arguments = parse_public_arguments(
            list(sys.argv[1:]) if arguments is None else arguments
        )
        repository_root = Path(__file__).absolute().parent.parent
        output = getattr(sys.stdout, "buffer", None)
        if output is None:
            raise SecureIngressError
        console = WindowsConsolePort()
        return run_secure_ingress(
            public_arguments,
            console=console,
            stdout=output,
            repository_root=repository_root,
            clock=time.monotonic,
            sleeper=time.sleep,
        )
    except BaseException:
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
