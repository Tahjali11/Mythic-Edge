from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import saved_event_replay, state

ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION = "analytics_legacy_jsonl_artifact_adapter.v1"
ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT = "mythic_edge_legacy_jsonl_import_quality"
ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION = "analytics_legacy_jsonl_import_quality_breakdown.v1"

SOURCE_KIND = "saved_event_replay"

_SAFE_KIND_RE = re.compile(r"^[A-Za-z0-9_.-]{1,80}$")
_SAFE_CODE_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,100}$")
_WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
_PRIVATE_LABEL_MARKERS = (
    "player.log",
    "webhook",
    "script.google.com",
    "hooks.",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
    "secret",
    "password",
    "token",
)


class LegacyJsonlAdapterError(ValueError):
    """Raised when a legacy JSONL archive cannot become analytics replay input."""


@dataclass(frozen=True, slots=True)
class LegacyJsonlAdapterResult:
    replay: dict[str, object]
    source_kind: str
    source_artifact_label: str
    files_processed: int
    records_seen: int
    events_processed: int
    events_skipped: int
    unsupported_kind_counts: dict[str, int]
    warnings: list[str]
    quality: dict[str, object]


def adapt_legacy_jsonl_artifacts(
    source: Path,
    *,
    source_artifact_label: str | None = None,
) -> LegacyJsonlAdapterResult:
    selected_files = _selected_jsonl_files(Path(source))
    label = _safe_source_artifact_label(
        source_artifact_label,
        selected_files=selected_files,
        source_is_dir=Path(source).is_dir(),
    )

    records_seen = 0
    events_processed = 0
    events_skipped = 0
    blank_line_count = 0
    duplicate_raw_hash_count = 0
    unsupported_kind_skip_count = 0
    processed_kind_counts: Counter[str] = Counter()
    unsupported_kind_counts: Counter[str] = Counter()
    warnings: list[str] = []
    seen_raw_hashes: set[str] = set()
    derived_match_ids: set[str] = set()
    latest_timestamp = ""

    state.reset_runtime_state()
    _seed_empty_card_lookup()
    try:
        for jsonl_path in selected_files:
            for line_number, raw_line in _iter_jsonl_lines(jsonl_path):
                line = raw_line.strip()
                if not line:
                    events_skipped += 1
                    blank_line_count += 1
                    continue

                records_seen += 1
                record = _json_record(line, jsonl_path=jsonl_path, line_number=line_number)
                raw_hash = str(record.get("raw_bytes_hash") or "").strip()
                if raw_hash:
                    if raw_hash in seen_raw_hashes:
                        events_skipped += 1
                        duplicate_raw_hash_count += 1
                        continue
                    seen_raw_hashes.add(raw_hash)

                kind = _required_kind(record, jsonl_path=jsonl_path, line_number=line_number)
                if kind not in saved_event_replay.EVENT_CLASS_BY_KIND:
                    kind_label = _safe_kind_label(kind)
                    unsupported_kind_counts[kind_label] += 1
                    unsupported_kind_skip_count += 1
                    events_skipped += 1
                    continue

                derived_match_id = _derived_match_id(record.get("derived"))
                if derived_match_id:
                    derived_match_ids.add(derived_match_id)

                event = _event_from_record(line, record, jsonl_path=jsonl_path, line_number=line_number)
                state._update_match_summary(event)
                processed_kind_counts[_safe_kind_label(kind)] += 1
                events_processed += 1
                timestamp = getattr(event.metadata, "timestamp", None)
                if timestamp is not None:
                    latest_timestamp = timestamp.isoformat()

        replay, incomplete_count = _build_replay(label=label, generated_at=latest_timestamp)
        warnings.extend(_derived_warnings(derived_match_ids, replay["match_log_rows"]))
        if incomplete_count:
            warnings.append(f"incomplete_match_summaries_skipped:{incomplete_count}")
        quality = _quality_summary(
            records_seen=records_seen,
            events_processed=events_processed,
            events_skipped=events_skipped,
            processed_kind_counts=processed_kind_counts,
            unsupported_kind_counts=unsupported_kind_counts,
            blank_line_count=blank_line_count,
            duplicate_raw_hash_count=duplicate_raw_hash_count,
            unsupported_kind_skip_count=unsupported_kind_skip_count,
            incomplete_summary_unclassified_count=incomplete_count,
            warnings=warnings,
        )

        return LegacyJsonlAdapterResult(
            replay=replay,
            source_kind=SOURCE_KIND,
            source_artifact_label=label,
            files_processed=len(selected_files),
            records_seen=records_seen,
            events_processed=events_processed,
            events_skipped=events_skipped,
            unsupported_kind_counts=dict(sorted(unsupported_kind_counts.items())),
            warnings=warnings,
            quality=quality,
        )
    finally:
        state.reset_runtime_state()


def failed_legacy_jsonl_import_quality(error_code: str) -> dict[str, object]:
    code = _safe_code_label(error_code, fallback="adapter_failed")
    return _quality_summary(
        quality_status="failed",
        records_seen=0,
        events_processed=0,
        events_skipped=0,
        processed_kind_counts=Counter(),
        unsupported_kind_counts=Counter(),
        blank_line_count=0,
        duplicate_raw_hash_count=0,
        unsupported_kind_skip_count=0,
        incomplete_summary_unclassified_count=0,
        warning_codes=[code],
        routing_hints=[
            _routing_hint(
                code=code,
                category=_failure_routing_category(code),
                severity="action_needed",
                count=1,
            )
        ],
    )


def _selected_jsonl_files(source: Path) -> list[Path]:
    if not source.exists():
        raise LegacyJsonlAdapterError(f"Source does not exist: {_safe_path_label(source)}")
    if source.is_file():
        if source.suffix.lower() != ".jsonl":
            raise LegacyJsonlAdapterError(f"Source file must be a JSONL file: {_safe_path_label(source)}")
        return [source]
    if source.is_dir():
        selected = saved_event_replay.latest_jsonl_files(source)
        if not selected:
            raise LegacyJsonlAdapterError(f"No JSONL files selected from source: {_safe_path_label(source)}")
        return selected
    raise LegacyJsonlAdapterError(f"Source is neither a JSONL file nor a directory: {_safe_path_label(source)}")


def _safe_source_artifact_label(
    requested_label: str | None,
    *,
    selected_files: Iterable[Path],
    source_is_dir: bool,
) -> str:
    if requested_label is not None:
        label = requested_label.strip()
        if not label:
            raise LegacyJsonlAdapterError("source_artifact_label must be a non-empty safe label")
        _validate_safe_label(label)
        return label

    digest_source = "|".join(path.name for path in selected_files)
    short_hash = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:12]
    label_prefix = "legacy_jsonl_bundle" if source_is_dir else "legacy_jsonl_saved_event_replay"
    return f"{label_prefix}:{short_hash}"


def _validate_safe_label(label: str) -> None:
    marker_text = label.lower()
    if (
        "://" in label
        or "\\" in label
        or "/" in label
        or label.startswith((".", "~"))
        or _WINDOWS_ABSOLUTE_PATH_RE.search(label)
        or any(marker in marker_text for marker in _PRIVATE_LABEL_MARKERS)
    ):
        raise LegacyJsonlAdapterError("source_artifact_label must be a safe label, not a local path or URL")


def _iter_jsonl_lines(path: Path) -> Iterable[tuple[int, str]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                yield line_number, raw_line
    except UnicodeDecodeError as exc:
        raise LegacyJsonlAdapterError(f"Selected JSONL file is not valid UTF-8: {_safe_path_label(path)}") from exc
    except OSError as exc:
        raise LegacyJsonlAdapterError(f"Selected JSONL file could not be read: {_safe_path_label(path)}") from exc


def _json_record(line: str, *, jsonl_path: Path, line_number: int) -> dict[str, Any]:
    try:
        record = json.loads(line)
    except json.JSONDecodeError as exc:
        raise LegacyJsonlAdapterError(
            f"Invalid JSON in selected JSONL record: {_safe_path_label(jsonl_path)}:{line_number}"
        ) from exc
    if not isinstance(record, dict):
        raise LegacyJsonlAdapterError(
            f"JSONL record must be an object: {_safe_path_label(jsonl_path)}:{line_number}"
        )
    return record


def _required_kind(record: dict[str, Any], *, jsonl_path: Path, line_number: int) -> str:
    kind = record.get("kind")
    if not isinstance(kind, str) or not kind.strip():
        raise LegacyJsonlAdapterError(
            f"JSONL record must include a string kind: {_safe_path_label(jsonl_path)}:{line_number}"
        )
    return kind.strip()


def _event_from_record(line: str, record: dict[str, Any], *, jsonl_path: Path, line_number: int) -> Any:
    try:
        event = saved_event_replay.event_from_saved_record(line, record)
    except Exception as exc:
        kind = _safe_kind_label(str(record.get("kind") or "unknown"))
        raise LegacyJsonlAdapterError(
            f"Malformed saved event record for kind {kind}: {_safe_path_label(jsonl_path)}:{line_number}"
        ) from exc
    if event is None:
        kind = _safe_kind_label(str(record.get("kind") or "unknown"))
        raise LegacyJsonlAdapterError(
            f"Supported saved event record could not be reconstructed for kind {kind}: "
            f"{_safe_path_label(jsonl_path)}:{line_number}"
        )
    return event


def _derived_match_id(value: object) -> str:
    if not isinstance(value, dict):
        return ""
    text = str(value.get("match_id") or "").strip()
    if not text or not _SAFE_KIND_RE.fullmatch(text):
        return ""
    return text


def _build_replay(*, label: str, generated_at: str) -> tuple[dict[str, object], int]:
    match_log_rows: list[dict[str, Any]] = []
    game_log_rows: list[dict[str, Any]] = []
    incomplete_count = 0

    for summary in sorted(state.iter_match_summaries(), key=lambda item: item.match_id):
        row = state.build_match_log_row(summary.match_id)
        if row is None:
            incomplete_count += 1
            continue
        rows_for_match = state.build_game_summary_rows(summary.match_id)
        if not rows_for_match:
            incomplete_count += 1
            continue
        match_log_rows.append(row)
        game_log_rows.extend(rows_for_match)

    if not match_log_rows or not game_log_rows:
        raise LegacyJsonlAdapterError("Replay produced no ingestable parser-normalized match/game rows")

    return (
        {
            "source_kind": SOURCE_KIND,
            "source_artifact_label": label,
            "match_log_rows": match_log_rows,
            "game_log_rows": game_log_rows,
            "gameplay_action_entries": [],
            "opponent_card_observations": [],
            "field_evidence_entries": [],
            "parser_commit": "",
            "parser_version": "",
            "generated_at": generated_at,
        },
        incomplete_count,
    )


def _derived_warnings(derived_match_ids: set[str], match_log_rows: object) -> list[str]:
    if not isinstance(match_log_rows, list) or not derived_match_ids:
        return []
    produced_match_ids = {
        str(row.get("match_id") or row.get("MTGA Match ID") or "").strip()
        for row in match_log_rows
        if isinstance(row, dict)
    }
    mismatches = sorted(derived_match_ids - produced_match_ids)
    return [f"derived_match_id_mismatch:{_safe_kind_label(match_id)}" for match_id in mismatches]


def _quality_summary(
    *,
    records_seen: int,
    events_processed: int,
    events_skipped: int,
    processed_kind_counts: Counter[str],
    unsupported_kind_counts: Counter[str],
    blank_line_count: int,
    duplicate_raw_hash_count: int,
    unsupported_kind_skip_count: int,
    incomplete_summary_unclassified_count: int,
    warnings: list[str] | None = None,
    warning_codes: list[str] | None = None,
    routing_hints: list[dict[str, object]] | None = None,
    quality_status: str | None = None,
) -> dict[str, object]:
    output_gap_counts = {
        "incomplete_match_summary": 0,
        "incomplete_game_summary": 0,
        "incomplete_summary_unclassified": incomplete_summary_unclassified_count,
    }
    adapter_warning_counts = Counter(_warning_code(warning) for warning in warnings or [])
    for code in warning_codes or []:
        adapter_warning_counts[_safe_code_label(code, fallback="adapter_warning")] += 1
    if events_skipped:
        adapter_warning_counts["events_skipped"] += 1
    if unsupported_kind_counts:
        adapter_warning_counts["unsupported_event_kinds"] += 1

    if quality_status is None:
        has_quality_issues = bool(events_skipped or adapter_warning_counts or incomplete_summary_unclassified_count)
        quality_status = "degraded" if has_quality_issues else "complete"

    return {
        "object": ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
        "schema_version": ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
        "quality_status": quality_status,
        "records_seen": records_seen,
        "events_processed": events_processed,
        "events_skipped": events_skipped,
        "processed_kind_counts": dict(sorted(processed_kind_counts.items())),
        "unsupported_kind_counts": dict(sorted(unsupported_kind_counts.items())),
        "skipped_reason_counts": {
            "blank_line": blank_line_count,
            "duplicate_raw_hash": duplicate_raw_hash_count,
            "unsupported_kind": unsupported_kind_skip_count,
        },
        "blank_line_count": blank_line_count,
        "duplicate_raw_hash_count": duplicate_raw_hash_count,
        "unsupported_kind_skip_count": unsupported_kind_skip_count,
        "output_gap_counts": output_gap_counts,
        "adapter_warning_counts": dict(sorted(adapter_warning_counts.items())),
        "adapter_warning_codes": sorted(adapter_warning_counts),
        "ingest_warning_codes": [],
        "routing_hints": routing_hints
        if routing_hints is not None
        else _quality_routing_hints(
            blank_line_count=blank_line_count,
            duplicate_raw_hash_count=duplicate_raw_hash_count,
            unsupported_kind_skip_count=unsupported_kind_skip_count,
            incomplete_summary_unclassified_count=incomplete_summary_unclassified_count,
        ),
        "privacy": {
            "has_private_path_echo": False,
            "raw_payload_exposed": False,
            "raw_hash_exposed": False,
        },
    }


def _quality_routing_hints(
    *,
    blank_line_count: int,
    duplicate_raw_hash_count: int,
    unsupported_kind_skip_count: int,
    incomplete_summary_unclassified_count: int,
) -> list[dict[str, object]]:
    hints: list[dict[str, object]] = []
    if blank_line_count:
        hints.append(
            _routing_hint(
                code="blank_lines",
                category="harmless_expected_skip",
                severity="info",
                count=blank_line_count,
            )
        )
    if duplicate_raw_hash_count:
        hints.append(
            _routing_hint(
                code="duplicate_raw_hashes",
                category="harmless_or_repeated_export",
                severity="info",
                count=duplicate_raw_hash_count,
            )
        )
    if unsupported_kind_skip_count:
        hints.append(
            _routing_hint(
                code="unsupported_event_kinds",
                category="parser_or_adapter_backlog",
                severity="warning",
                count=unsupported_kind_skip_count,
            )
        )
    if incomplete_summary_unclassified_count:
        hints.append(
            _routing_hint(
                code="incomplete_summaries",
                category="analytics_ingest_backlog",
                severity="warning",
                count=incomplete_summary_unclassified_count,
            )
        )
    return hints


def _routing_hint(*, code: str, category: str, severity: str, count: int) -> dict[str, object]:
    return {
        "code": _safe_code_label(code, fallback="unknown"),
        "category": _safe_code_label(category, fallback="unknown"),
        "severity": _safe_code_label(severity, fallback="warning"),
        "count": count,
    }


def _warning_code(value: str) -> str:
    base = str(value or "").split(":", maxsplit=1)[0].strip()
    return _safe_code_label(base, fallback="adapter_warning")


def _failure_routing_category(code: str) -> str:
    if code in {"invalid_jsonl", "invalid_utf8", "malformed_saved_event", "no_ingestable_rows"}:
        return "source_artifact_problem"
    if code in {"source_artifact_label_invalid", "adapter_failed"}:
        return "unsupported_legacy_shape"
    return "unknown"


def _safe_kind_label(value: str) -> str:
    text = str(value or "").strip()
    if _SAFE_KIND_RE.fullmatch(text):
        return text
    return "unsafe_or_unknown_kind"


def _safe_code_label(value: str, *, fallback: str) -> str:
    text = str(value or "").strip()
    if _SAFE_CODE_RE.fullmatch(text) and not any(marker in text.lower() for marker in _PRIVATE_LABEL_MARKERS):
        return text
    return fallback


def _safe_path_label(path: Path) -> str:
    return Path(path).name or "[selected-path]"


def _seed_empty_card_lookup() -> None:
    lookup: dict[str, dict[str, Any]] = {}
    state._ARENA_CARD_LOOKUP = lookup
    state.RUNTIME_STATE.arena_card_lookup = lookup
    state._ARENA_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.arena_card_lookup_ready = True
    state._GAMEPLAY_CARD_LOOKUP_READY = True
    state.RUNTIME_STATE.gameplay_card_lookup_ready = True
