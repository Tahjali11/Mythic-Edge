from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from mythic_edge_parser.log.entry import UTC_PREFIX_RE

UtcLogSourceKind = Literal["synthetic", "user_selected_local"]
UtcLogPrivacyClass = Literal["public_fixture", "private_local"]
UtcLogDegradationStatus = Literal["ok", "review", "degraded", "failed"]


class UtcLogSourceAccessError(ValueError):
    """Raised when a UTC_Log source operation is outside the approved boundary."""


@dataclass(frozen=True, slots=True)
class UtcLogCandidate:
    source_label: str
    display_name: str
    size_bytes: int | None
    modified_time: str | None
    source_kind: UtcLogSourceKind
    privacy_class: UtcLogPrivacyClass


@dataclass(frozen=True, slots=True)
class UtcLogNormalizationStats:
    input_line_count: int
    output_line_count: int
    utc_frame_prefix_lines: int
    unchanged_lines: int
    dropped_lines: int
    replacement_character_count: int
    degradation_status: UtcLogDegradationStatus


@dataclass(frozen=True, slots=True)
class UtcLogNormalizationResult:
    text: str
    stats: UtcLogNormalizationStats
    source_label: str
    source_kind: UtcLogSourceKind
    warnings: tuple[str, ...]


_SYMBOLIC_LABEL_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-")


def normalize_utc_log_text(
    text: str,
    *,
    source_label: str,
    source_kind: UtcLogSourceKind = "synthetic",
) -> UtcLogNormalizationResult:
    """Normalize synthetic UTC_Log-style text for existing Player.log parser paths."""

    if not isinstance(text, str):
        raise TypeError("UTC_Log source text must be a string")
    _validate_source_kind(source_kind)
    _validate_symbolic_source_label(source_label)
    if source_kind != "synthetic":
        raise UtcLogSourceAccessError("private/local UTC_Log source normalization is not authorized")

    line_ending_normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = line_ending_normalized.splitlines(keepends=True)
    output_lines: list[str] = []
    prefix_count = 0
    unchanged_count = 0

    for line in lines:
        has_newline = line.endswith("\n")
        body = line[:-1] if has_newline else line
        normalized_body, replacements = UTC_PREFIX_RE.subn("", body, count=1)
        if replacements:
            prefix_count += 1
        else:
            unchanged_count += 1
        output_lines.append(f"{normalized_body}\n" if has_newline else normalized_body)

    warnings = _normalization_warnings(text, lines)
    stats = UtcLogNormalizationStats(
        input_line_count=len(lines),
        output_line_count=len(output_lines),
        utc_frame_prefix_lines=prefix_count,
        unchanged_lines=unchanged_count,
        dropped_lines=0,
        replacement_character_count=text.count("\ufffd"),
        degradation_status=_degradation_status(warnings),
    )
    return UtcLogNormalizationResult(
        text="".join(output_lines),
        stats=stats,
        source_label=source_label,
        source_kind=source_kind,
        warnings=warnings,
    )


def describe_user_selected_utc_log_candidate(path: Path) -> UtcLogCandidate:
    """Fail closed for private/local candidate discovery until a later approval exists."""

    if not isinstance(path, Path):
        raise TypeError("UTC_Log candidate path must be a pathlib.Path")
    raise UtcLogSourceAccessError("private/local UTC_Log candidate inspection is not authorized")


def _validate_source_kind(source_kind: str) -> None:
    if source_kind not in {"synthetic", "user_selected_local"}:
        raise ValueError("unknown UTC_Log source kind")


def _validate_symbolic_source_label(source_label: str) -> None:
    if not source_label or any(char not in _SYMBOLIC_LABEL_CHARS for char in source_label):
        raise UtcLogSourceAccessError("source_label must be symbolic and public-safe")


def _normalization_warnings(original_text: str, lines: list[str]) -> tuple[str, ...]:
    warnings: list[str] = []
    if original_text == "":
        warnings.append("empty_input")
    if "\ufffd" in original_text:
        warnings.append("replacement_characters_present")
    if "\x00" in original_text:
        warnings.append("nul_characters_present")
    if lines and not original_text.endswith(("\n", "\r")):
        warnings.append("input_has_no_line_ending")
    return tuple(warnings)


def _degradation_status(warnings: tuple[str, ...]) -> UtcLogDegradationStatus:
    if "nul_characters_present" in warnings:
        return "degraded"
    if warnings:
        return "review"
    return "ok"
