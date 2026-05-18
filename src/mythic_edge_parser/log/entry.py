from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class EntryHeader(str, Enum):
    METADATA = "Metadata"
    UNITY_CROSS_THREAD_LOGGER = "UnityCrossThreadLogger"
    CONNECTION_MANAGER = "ConnectionManager"
    MATCHMAKING = "Matchmaking"
    CLIENT_GRE = "Client GRE"
    TRUNCATION_MARKER = "TruncationMarker"
    UNKNOWN = "Unknown"


HEADER_RE = re.compile(r"^(?:\[\d+\]\s+)?(\[(?P<header>[^\]]+)\]|DETAILED LOGS:)")
UTC_PREFIX_RE = re.compile(r"^\[\d+\]\s+")
_LINE_ENDINGS = ("\n", "\r")
TRUNCATION_MARKER_PREFIX = "[Message summarized"


@dataclass(frozen=True, slots=True)
class HeaderPolicy:
    header: EntryHeader
    is_single_line: Callable[[str], bool]


def _always_single_line(_: str) -> bool:
    return True


def _never_single_line(_: str) -> bool:
    return False


def _unity_cross_thread_logger_is_single_line(line: str) -> bool:
    suffix = line.removeprefix("[UnityCrossThreadLogger]")
    return bool(suffix) and not suffix[:1].isdigit()


_METADATA_POLICY = HeaderPolicy(
    header=EntryHeader.METADATA,
    is_single_line=_always_single_line,
)
_MATCHMAKING_POLICY = HeaderPolicy(
    header=EntryHeader.MATCHMAKING,
    is_single_line=_always_single_line,
)
_TRUNCATION_MARKER_POLICY = HeaderPolicy(
    header=EntryHeader.TRUNCATION_MARKER,
    is_single_line=_never_single_line,
)
_UNKNOWN_HEADER_POLICY = HeaderPolicy(
    header=EntryHeader.UNKNOWN,
    is_single_line=_never_single_line,
)
_HEADER_POLICIES_BY_NAME = {
    "UnityCrossThreadLogger": HeaderPolicy(
        header=EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        is_single_line=_unity_cross_thread_logger_is_single_line,
    ),
    "ConnectionManager": HeaderPolicy(
        header=EntryHeader.CONNECTION_MANAGER,
        is_single_line=_always_single_line,
    ),
    "Client GRE": HeaderPolicy(
        header=EntryHeader.CLIENT_GRE,
        is_single_line=_never_single_line,
    ),
}
_HEADER_POLICIES_BY_HEADER = {
    policy.header: policy
    for policy in (
        _METADATA_POLICY,
        _MATCHMAKING_POLICY,
        _TRUNCATION_MARKER_POLICY,
        _UNKNOWN_HEADER_POLICY,
        *_HEADER_POLICIES_BY_NAME.values(),
    )
}


@dataclass(slots=True)
class LogEntry:
    header: EntryHeader
    body: str


class LineBuffer:
    def __init__(self) -> None:
        self._current_lines: list[str] = []
        self._current_header: EntryHeader | None = None
        self._pending_fragment = ""

    def feed(self, text: str) -> list[LogEntry]:
        entries: list[LogEntry] = []
        for line in self._consume_complete_lines(text):
            self._process_complete_line(line, entries)
        return entries

    def flush(self) -> list[LogEntry]:
        entries: list[LogEntry] = []
        if self._pending_fragment:
            pending_fragment = self._pending_fragment
            self._pending_fragment = ""
            self._process_complete_line(pending_fragment, entries)
        self._emit_current_entry(entries)
        return entries

    def _consume_complete_lines(self, text: str) -> list[str]:
        combined = f"{self._pending_fragment}{text}"
        self._pending_fragment = ""
        if not combined:
            return []
        raw_lines = combined.splitlines(keepends=True)
        if raw_lines and not raw_lines[-1].endswith(_LINE_ENDINGS):
            self._pending_fragment = raw_lines.pop()
        return [line.rstrip("\r\n") for line in raw_lines]

    def _process_complete_line(self, line: str, entries: list[LogEntry]) -> None:
        normalized_line = UTC_PREFIX_RE.sub("", line)
        policy = resolve_header_policy(normalized_line)
        if policy is None:
            self._append_non_header_line(normalized_line)
            return
        self._emit_current_entry(entries)
        if policy.is_single_line(normalized_line):
            entries.append(LogEntry(policy.header, normalized_line))
            return
        self._current_lines = [normalized_line]
        self._current_header = policy.header

    def _append_non_header_line(self, line: str) -> None:
        if self._current_lines:
            self._current_lines.append(line)

    def _emit_current_entry(self, entries: list[LogEntry]) -> None:
        if not self._current_lines:
            return
        entries.append(
            LogEntry(
                self._current_header or EntryHeader.UNKNOWN,
                "\n".join(self._current_lines),
            )
        )
        self._current_lines = []
        self._current_header = None


def resolve_header_policy(line: str) -> HeaderPolicy | None:
    normalized_line = UTC_PREFIX_RE.sub("", line.lstrip())
    # Keep these explicit prefix rules for now. If entry.py gets another
    # structural review, revisit whether metadata and matchmaking should move
    # into the same ordered rule registry as the bracketed header families.
    if normalized_line.startswith("DETAILED LOGS:"):
        return _METADATA_POLICY
    if normalized_line.startswith("Matchmaking: "):
        return _MATCHMAKING_POLICY
    if normalized_line.startswith(TRUNCATION_MARKER_PREFIX):
        return _TRUNCATION_MARKER_POLICY
    match = HEADER_RE.match(normalized_line)
    if not match:
        return None
    name = match.group("header") or ""
    return _HEADER_POLICIES_BY_NAME.get(name, _UNKNOWN_HEADER_POLICY)


def classify_line_header(line: str) -> EntryHeader | None:
    policy = resolve_header_policy(line)
    return None if policy is None else policy.header


def is_single_line_header(line: str, header: EntryHeader | None = None) -> bool:
    if header is not None:
        policy = _HEADER_POLICIES_BY_HEADER.get(header)
    else:
        policy = resolve_header_policy(line)
    if policy is None:
        return False
    return policy.is_single_line(line)
