from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from .analytics_migration_loader import ANALYTICS_SCHEMA_VERSION, apply_analytics_migrations

ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION = "analytics_parser_normalized_replay_ingest.v1"

_ALLOWED_SOURCE_KINDS = {"sanitized_golden_replay", "saved_event_replay"}
_TOUCHED_TABLES = (
    "ingest_runs",
    "matches",
    "games",
    "match_results",
    "game_results",
    "match_context",
    "rank_snapshots",
    "opening_hands",
    "opening_hand_cards",
    "mulligan_events",
    "mulligan_bottomed_or_discarded_cards",
    "fact_provenance",
)
_UNAVAILABLE_CARD_VALUES = {"", "[]", "{}", "n/a", "na", "none", "unknown", "unavailable", "not available"}
_PRIVATE_LABEL_RE = re.compile(r"(^[a-zA-Z]:[\\/]|^[\\/]|://)")
_INTEGER_TEXT_RE = re.compile(r"[+-]?\d+")


class AnalyticsReplayIngestError(ValueError):
    """Raised when parser-normalized analytics replay input is invalid."""


@dataclass(frozen=True, slots=True)
class ParserNormalizedReplayInput:
    source_kind: str
    source_artifact_label: str
    match_log_rows: tuple[dict[str, object], ...]
    game_log_rows: tuple[dict[str, object], ...]
    gameplay_action_entries: tuple[dict[str, object], ...] = ()
    opponent_card_observations: tuple[dict[str, object], ...] = ()
    field_evidence_entries: tuple[dict[str, object], ...] = ()
    parser_commit: str = ""
    parser_version: str = ""
    generated_at: str = ""


@dataclass(frozen=True, slots=True)
class AnalyticsReplayIngestResult:
    ingest_run_id: str
    source_kind: str
    source_artifact_label: str
    status: str
    row_counts: dict[str, int]
    warnings: list[str]
    skipped: dict[str, int]


def normalize_parser_normalized_replay(replay: Mapping[str, object]) -> ParserNormalizedReplayInput:
    if not isinstance(replay, Mapping):
        raise AnalyticsReplayIngestError("Parser-normalized replay input must be a mapping")

    source_kind = _required_text(replay.get("source_kind"), "source_kind")
    if source_kind not in _ALLOWED_SOURCE_KINDS:
        raise AnalyticsReplayIngestError(f"Unsupported parser-normalized replay source_kind: {source_kind}")

    source_artifact_label = _required_text(replay.get("source_artifact_label"), "source_artifact_label")
    if _PRIVATE_LABEL_RE.search(source_artifact_label):
        raise AnalyticsReplayIngestError("source_artifact_label must be a safe label, not a local path or URL")

    return ParserNormalizedReplayInput(
        source_kind=source_kind,
        source_artifact_label=source_artifact_label,
        match_log_rows=_mapping_tuple(replay.get("match_log_rows"), "match_log_rows", required=True),
        game_log_rows=_mapping_tuple(replay.get("game_log_rows"), "game_log_rows", required=True),
        gameplay_action_entries=_mapping_tuple(replay.get("gameplay_action_entries"), "gameplay_action_entries"),
        opponent_card_observations=_mapping_tuple(
            replay.get("opponent_card_observations"),
            "opponent_card_observations",
        ),
        field_evidence_entries=_mapping_tuple(replay.get("field_evidence_entries"), "field_evidence_entries"),
        parser_commit=_optional_text(replay.get("parser_commit")) or "",
        parser_version=_optional_text(replay.get("parser_version")) or "",
        generated_at=_optional_text(replay.get("generated_at")) or "",
    )


def deterministic_ingest_run_id(replay: ParserNormalizedReplayInput) -> str:
    canonical_payload = {
        "source_kind": replay.source_kind,
        "source_artifact_label": replay.source_artifact_label,
        "match_log_rows": replay.match_log_rows,
        "game_log_rows": replay.game_log_rows,
        "gameplay_action_entries": replay.gameplay_action_entries,
        "opponent_card_observations": replay.opponent_card_observations,
        "field_evidence_entries": replay.field_evidence_entries,
        "parser_commit": replay.parser_commit,
        "parser_version": replay.parser_version,
        "generated_at": replay.generated_at,
    }
    canonical_json = json.dumps(
        _jsonable(canonical_payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    digest = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
    return f"analytics_replay_ingest:{digest}"


def ingest_parser_normalized_replay(
    connection: sqlite3.Connection,
    replay: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult:
    normalized = normalize_parser_normalized_replay(replay)
    ingest_run_id = deterministic_ingest_run_id(normalized)
    timestamp = _ingest_timestamp(started_at, normalized.generated_at)
    completed_at = finished_at or timestamp
    warnings = _deferred_optional_warnings(normalized)
    skipped = _deferred_optional_skips(normalized)

    apply_analytics_migrations(connection)

    try:
        connection.execute("BEGIN")
        _upsert_ingest_run(
            connection,
            ingest_run_id=ingest_run_id,
            replay=normalized,
            started_at=timestamp,
            finished_at=None,
            status="started",
            row_counts={},
            now=timestamp,
        )
        known_match_ids = _ingest_match_log_rows(
            connection,
            normalized.match_log_rows,
            ingest_run_id=ingest_run_id,
            now=timestamp,
        )
        _ingest_game_log_rows(
            connection,
            normalized.game_log_rows,
            known_match_ids=known_match_ids,
            ingest_run_id=ingest_run_id,
            now=timestamp,
            warnings=warnings,
        )
        row_counts = _table_counts(connection, _TOUCHED_TABLES)
        _upsert_ingest_run(
            connection,
            ingest_run_id=ingest_run_id,
            replay=normalized,
            started_at=timestamp,
            finished_at=completed_at,
            status="completed",
            row_counts=row_counts,
            now=timestamp,
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise

    final_row_counts = _table_counts(connection, _TOUCHED_TABLES)
    return AnalyticsReplayIngestResult(
        ingest_run_id=ingest_run_id,
        source_kind=normalized.source_kind,
        source_artifact_label=normalized.source_artifact_label,
        status="completed",
        row_counts=final_row_counts,
        warnings=warnings,
        skipped=skipped,
    )


def _ingest_match_log_rows(
    connection: sqlite3.Connection,
    match_log_rows: tuple[dict[str, object], ...],
    *,
    ingest_run_id: str,
    now: str,
) -> set[str]:
    known_match_ids: set[str] = set()
    for index, row in enumerate(match_log_rows):
        match_id = _match_id(row, f"match_log_rows[{index}]")
        known_match_ids.add(match_id)
        finality = _match_finality(row)

        _upsert(
            connection,
            "matches",
            "match_id",
            {
                "match_id": match_id,
                "session_id": None,
                "parser_match_key": match_id,
                "match_started_at": _optional_text(row.get("MGTA Start Time")) or _optional_text(row.get("timestamp")),
                "match_completed_at": _optional_text(row.get("MTGA End Time")),
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="MatchSummary.to_match_log_row",
                    source_fact_key="match_id",
                    finality=finality,
                    now=now,
                ),
            },
        )
        _upsert(
            connection,
            "match_results",
            "match_result_id",
            {
                "match_result_id": f"{match_id}:match_result",
                "match_id": match_id,
                "match_result": _optional_text(row.get("Match Win?")),
                "winner_team_id": None,
                "games_won": _optional_int(row.get("Games Won"), "Games Won"),
                "games_lost": _optional_int(row.get("Games Lost"), "Games Lost"),
                "total_games": _optional_int(row.get("Total Games"), "Total Games"),
                "match_win": _optional_int(row.get("Match Win Flag"), "Match Win Flag"),
                "game_win_rate": _optional_float(row.get("Game Win %"), "Game Win %"),
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="MatchSummary.to_match_log_row",
                    source_fact_key="match_result",
                    finality=finality,
                    now=now,
                ),
            },
        )
        _upsert(
            connection,
            "match_context",
            "match_context_id",
            {
                "match_context_id": f"{match_id}:match_context",
                "match_id": match_id,
                "queue_name": _optional_text(row.get("MTGA Queue Type")),
                "format_name": _optional_text(row.get("MTGA Format")),
                "event_id": _optional_text(row.get("MTGA Event ID")),
                "match_win_condition": None,
                "event_type": None,
                "event_scope": None,
                "event_source": None,
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="MatchSummary.to_match_log_row",
                    source_fact_key="match_context",
                    finality=finality,
                    now=now,
                ),
            },
        )
        if _optional_text(row.get("MTGA Rank Raw")) or _optional_text(row.get("My Rank")):
            _upsert(
                connection,
                "rank_snapshots",
                "rank_snapshot_id",
                {
                    "rank_snapshot_id": f"{match_id}:rank_snapshot:match",
                    "match_id": match_id,
                    "game_id": None,
                    "rank_context": "match",
                    "rank_source": "MatchLogRow",
                    "constructed_rank": _optional_text(row.get("MTGA Rank Raw")),
                    "constructed_tier": _optional_text(row.get("My Rank")),
                    "limited_rank": None,
                    "limited_tier": None,
                    "season_ordinal": None,
                    **_core_columns(
                        ingest_run_id=ingest_run_id,
                        source_parser_surface="MatchSummary.to_match_log_row",
                        source_fact_key="rank_snapshot",
                        finality=finality,
                        now=now,
                    ),
                },
            )

        _upsert_fact_provenance(
            connection,
            fact_table="matches",
            fact_id=match_id,
            fact_field="match_id",
            source_parser_surface="MatchSummary.to_match_log_row",
            source_fact_key="match_id",
            ingest_run_id=ingest_run_id,
            finality=finality,
            now=now,
        )
        _upsert_fact_provenance(
            connection,
            fact_table="match_results",
            fact_id=f"{match_id}:match_result",
            fact_field="match_result",
            source_parser_surface="MatchSummary.to_match_log_row",
            source_fact_key="Match Win?",
            ingest_run_id=ingest_run_id,
            finality=finality,
            now=now,
        )

    return known_match_ids


def _ingest_game_log_rows(
    connection: sqlite3.Connection,
    game_log_rows: tuple[dict[str, object], ...],
    *,
    known_match_ids: set[str],
    ingest_run_id: str,
    now: str,
    warnings: list[str],
) -> None:
    for index, row in enumerate(game_log_rows):
        match_id = _match_id(row, f"game_log_rows[{index}]")
        if match_id not in known_match_ids:
            raise AnalyticsReplayIngestError(f"game_log_rows[{index}] references unknown match_id: {match_id}")
        game_number = _required_positive_int(row.get("Game Number"), f"game_log_rows[{index}].Game Number")
        game_id = f"{match_id}:g{game_number}"

        _upsert(
            connection,
            "games",
            "game_id",
            {
                "game_id": game_id,
                "match_id": match_id,
                "game_number": game_number,
                "game_started_at": None,
                "game_completed_at": _optional_text(row.get("timestamp")),
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="GameSummary.to_game_log_row",
                    source_fact_key="game_id",
                    finality="final",
                    now=now,
                ),
            },
        )
        _upsert(
            connection,
            "game_results",
            "game_result_id",
            {
                "game_result_id": f"{game_id}:game_result",
                "game_id": game_id,
                "match_id": match_id,
                "game_number": game_number,
                "winner_team_id": None,
                "local_result": _local_result(row.get("Game Result")),
                "pre_postboard_label": _pre_postboard(row.get("Pre / Postboard")),
                "play_draw": _play_draw(row.get("Play / Draw")),
                "turn_count": _optional_int(row.get("Turn Count"), "Turn Count"),
                "game_started_at": None,
                "game_completed_at": _optional_text(row.get("timestamp")),
                "game_duration_seconds": _optional_float(row.get("Game Duration"), "Game Duration"),
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="GameSummary.to_game_log_row",
                    source_fact_key="game_result",
                    finality="final",
                    now=now,
                ),
            },
        )
        _upsert_fact_provenance(
            connection,
            fact_table="game_results",
            fact_id=f"{game_id}:game_result",
            fact_field="local_result",
            source_parser_surface="GameSummary.to_game_log_row",
            source_fact_key="Game Result",
            ingest_run_id=ingest_run_id,
            finality="final",
            now=now,
        )
        _ingest_opening_hand(
            connection,
            row,
            match_id=match_id,
            game_id=game_id,
            game_number=game_number,
            ingest_run_id=ingest_run_id,
            now=now,
            warnings=warnings,
        )
        _ingest_mulligan(
            connection,
            row,
            match_id=match_id,
            game_id=game_id,
            game_number=game_number,
            ingest_run_id=ingest_run_id,
            now=now,
            warnings=warnings,
        )


def _ingest_opening_hand(
    connection: sqlite3.Connection,
    row: Mapping[str, object],
    *,
    match_id: str,
    game_id: str,
    game_number: int,
    ingest_run_id: str,
    now: str,
    warnings: list[str],
) -> None:
    hand_size = _optional_int(row.get("Opening Hand Size"), "Opening Hand Size")
    card_names = _card_names(row.get("Opening Hand"), "Opening Hand", warnings)
    if hand_size is None and not card_names:
        return

    opening_hand_id = f"{game_id}:opening_hand"
    _upsert(
        connection,
        "opening_hands",
        "opening_hand_id",
        {
            "opening_hand_id": opening_hand_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "hand_size": hand_size,
            "exact_card_count": len(card_names) if card_names else None,
            **_core_columns(
                ingest_run_id=ingest_run_id,
                source_parser_surface="GameSummary.to_game_log_row",
                source_fact_key="opening_hand",
                finality="final",
                now=now,
            ),
        },
    )
    _upsert_fact_provenance(
        connection,
        fact_table="opening_hands",
        fact_id=opening_hand_id,
        fact_field="hand_size",
        source_parser_surface="GameSummary.to_game_log_row",
        source_fact_key="Opening Hand Size",
        ingest_run_id=ingest_run_id,
        finality="final",
        now=now,
    )
    for position, card_name in enumerate(card_names, start=1):
        _upsert(
            connection,
            "opening_hand_cards",
            "opening_hand_card_id",
            {
                "opening_hand_card_id": f"{opening_hand_id}:slot{position}",
                "opening_hand_id": opening_hand_id,
                "game_id": game_id,
                "card_position": position,
                "grp_id": None,
                "card_name": card_name,
                "identity_hint_source": "name_only_from_parser_row",
                "name_resolution_status": "name_only",
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="GameSummary.to_game_log_row",
                    source_fact_key="Opening Hand",
                    finality="final",
                    now=now,
                ),
            },
        )


def _ingest_mulligan(
    connection: sqlite3.Connection,
    row: Mapping[str, object],
    *,
    match_id: str,
    game_id: str,
    game_number: int,
    ingest_run_id: str,
    now: str,
    warnings: list[str],
) -> None:
    mulligan_count = _optional_int(row.get("Mulligans"), "Mulligans")
    card_names = _card_names(row.get("Mulliganed Away"), "Mulliganed Away", warnings)
    if mulligan_count is None and not card_names:
        return

    ordinal_or_count = str(mulligan_count) if mulligan_count is not None else "unknown"
    mulligan_event_id = f"{game_id}:mulligan:{ordinal_or_count}"
    availability_status = "not_observed" if mulligan_count == 0 else "available"
    decision_detail = "kept_initial_hand" if mulligan_count == 0 else "mulligan_count_from_parser_row"
    if mulligan_count is None:
        decision_detail = "mulliganed_away_from_parser_row"
    _upsert(
        connection,
        "mulligan_events",
        "mulligan_event_id",
        {
            "mulligan_event_id": mulligan_event_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "ordinal_or_count": ordinal_or_count,
            "mulligan_count": mulligan_count,
            "decision_detail": decision_detail,
            **_core_columns(
                ingest_run_id=ingest_run_id,
                source_parser_surface="GameSummary.to_game_log_row",
                source_fact_key="Mulligans",
                finality="final",
                availability_status=availability_status,
                now=now,
            ),
        },
    )
    _upsert_fact_provenance(
        connection,
        fact_table="mulligan_events",
        fact_id=mulligan_event_id,
        fact_field="mulligan_count",
        source_parser_surface="GameSummary.to_game_log_row",
        source_fact_key="Mulligans",
        ingest_run_id=ingest_run_id,
        finality="final",
        now=now,
    )
    for position, card_name in enumerate(card_names, start=1):
        _upsert(
            connection,
            "mulligan_bottomed_or_discarded_cards",
            "mulligan_card_id",
            {
                "mulligan_card_id": f"{mulligan_event_id}:card{position}",
                "mulligan_event_id": mulligan_event_id,
                "game_id": game_id,
                "card_position": position,
                "card_action": "unknown",
                "grp_id": None,
                "card_name": card_name,
                "identity_hint_source": "name_only_from_parser_row",
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="GameSummary.to_game_log_row",
                    source_fact_key="Mulliganed Away",
                    finality="final",
                    now=now,
                ),
            },
        )


def _upsert_ingest_run(
    connection: sqlite3.Connection,
    *,
    ingest_run_id: str,
    replay: ParserNormalizedReplayInput,
    started_at: str,
    finished_at: str | None,
    status: str,
    row_counts: dict[str, int],
    now: str,
) -> None:
    _upsert(
        connection,
        "ingest_runs",
        "ingest_run_id",
        {
            "ingest_run_id": ingest_run_id,
            "source_kind": replay.source_kind,
            "source_artifact_label": replay.source_artifact_label,
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "parser_commit": replay.parser_commit or None,
            "parser_version": replay.parser_version or None,
            "schema_version": ANALYTICS_SCHEMA_VERSION,
            "row_counts_json": json.dumps(row_counts, sort_keys=True, separators=(",", ":")),
            "created_at": now,
            "updated_at": now,
        },
    )


def _upsert_fact_provenance(
    connection: sqlite3.Connection,
    *,
    fact_table: str,
    fact_id: str,
    fact_field: str,
    source_parser_surface: str,
    source_fact_key: str,
    ingest_run_id: str,
    finality: str,
    now: str,
) -> None:
    _upsert(
        connection,
        "fact_provenance",
        "fact_provenance_id",
        {
            "fact_provenance_id": f"{fact_table}:{fact_id}:{fact_field}:provenance",
            "fact_table": fact_table,
            "fact_id": fact_id,
            "fact_field": fact_field,
            "ledger_entry_id": None,
            "source_parser_surface": source_parser_surface,
            "source_fact_key": source_fact_key,
            "source_event_kind": None,
            "source_event_type": None,
            "source_payload_paths": json.dumps([f"/{source_fact_key}"], separators=(",", ":")),
            "source_event_timestamp": None,
            "value_source": "derived",
            "confidence": "unknown",
            "finality": finality,
            "drift_flags": "[]",
            "invariant_status": None,
            "degraded_reason": None,
            "review_required": 0,
            "ingest_run_id": ingest_run_id,
            "created_at": now,
        },
    )


def _upsert(connection: sqlite3.Connection, table_name: str, primary_key: str, values: Mapping[str, object]) -> None:
    columns = tuple(values)
    placeholders = ", ".join("?" for _ in columns)
    assignments = ", ".join(f"{column} = excluded.{column}" for column in columns if column != primary_key)
    connection.execute(
        f"""
        INSERT INTO {table_name} ({", ".join(columns)})
        VALUES ({placeholders})
        ON CONFLICT({primary_key}) DO UPDATE SET {assignments}
        """,
        tuple(values[column] for column in columns),
    )


def _core_columns(
    *,
    ingest_run_id: str,
    source_parser_surface: str,
    source_fact_key: str,
    finality: str,
    now: str,
    availability_status: str = "available",
) -> dict[str, object]:
    return {
        "value_source": "derived",
        "confidence": "unknown",
        "finality": finality,
        "drift_status": "not_checked",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": ingest_run_id,
        "source_parser_surface": source_parser_surface,
        "source_fact_key": source_fact_key,
        "availability_status": availability_status,
        "created_at": now,
        "updated_at": now,
    }


def _table_counts(connection: sqlite3.Connection, table_names: Sequence[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for table_name in table_names:
        row = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        counts[table_name] = int(row[0])
    return counts


def _mapping_tuple(value: object, field_name: str, *, required: bool = False) -> tuple[dict[str, object], ...]:
    if value is None:
        if required:
            raise AnalyticsReplayIngestError(f"{field_name} is required")
        return ()
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise AnalyticsReplayIngestError(f"{field_name} must be a list of mappings")
    rows: list[dict[str, object]] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a mapping")
        rows.append(dict(item))
    if required and not rows:
        raise AnalyticsReplayIngestError(f"{field_name} must contain at least one row")
    return tuple(rows)


def _match_id(row: Mapping[str, object], context: str) -> str:
    match_id = _optional_text(row.get("match_id")) or _optional_text(row.get("MTGA Match ID"))
    if not match_id:
        raise AnalyticsReplayIngestError(f"{context} is missing required match_id")
    return match_id


def _required_positive_int(value: object, field_name: str) -> int:
    normalized = _optional_int(value, field_name, minimum=1)
    if normalized is None:
        raise AnalyticsReplayIngestError(f"{field_name} must be a positive integer")
    return normalized


def _optional_int(value: object, field_name: str, *, minimum: int = 0) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise AnalyticsReplayIngestError(f"{field_name} must be an integer, not a boolean")
    if isinstance(value, int):
        normalized = value
    elif isinstance(value, float):
        if not value.is_integer():
            raise AnalyticsReplayIngestError(f"{field_name} must be an integer")
        normalized = int(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if not _INTEGER_TEXT_RE.fullmatch(text):
            raise AnalyticsReplayIngestError(f"{field_name} must be an integer")
        normalized = int(text)
    else:
        raise AnalyticsReplayIngestError(f"{field_name} must be an integer")

    if normalized < minimum:
        if minimum == 1:
            raise AnalyticsReplayIngestError(f"{field_name} must be a positive integer")
        raise AnalyticsReplayIngestError(f"{field_name} must be a non-negative integer")
    return normalized


def _optional_float(value: object, field_name: str) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        raise AnalyticsReplayIngestError(f"{field_name} must be numeric, not a boolean")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise AnalyticsReplayIngestError(f"{field_name} must be numeric") from exc


def _required_text(value: object, field_name: str) -> str:
    text = _optional_text(value)
    if not text:
        raise AnalyticsReplayIngestError(f"{field_name} is required")
    return text


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _match_finality(row: Mapping[str, object]) -> str:
    sync_status = str(row.get("MTGA Sync Status") or "").strip().lower()
    if sync_status == "live":
        return "provisional"
    return "reconciled"


def _local_result(value: object) -> str | None:
    text = str(value or "").strip().lower()
    if text in {"w", "win", "won"}:
        return "win"
    if text in {"l", "loss", "lost"}:
        return "loss"
    return text or None


def _play_draw(value: object) -> str | None:
    text = str(value or "").strip().lower()
    if text in {"play", "draw", "unknown"}:
        return text
    return None


def _pre_postboard(value: object) -> str | None:
    text = str(value or "").strip().lower()
    if text == "preboard":
        return "preboard"
    if text == "postboard":
        return "postboard"
    if text == "game1":
        return "game1"
    if text == "unknown":
        return "unknown"
    return None


def _card_names(value: object, field_name: str, warnings: list[str]) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        raw_values = value.split(";")
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        raw_values = list(value)
    else:
        warnings.append(f"{field_name} omitted because it was not a string or list")
        return []

    names: list[str] = []
    for raw_value in raw_values:
        text = str(raw_value or "").strip()
        if text.lower() in _UNAVAILABLE_CARD_VALUES:
            continue
        if text:
            names.append(text)
    return names


def _ingest_timestamp(started_at: str | None, generated_at: str) -> str:
    return started_at or generated_at or datetime.now(UTC).isoformat()


def _deferred_optional_warnings(replay: ParserNormalizedReplayInput) -> list[str]:
    warnings: list[str] = []
    if replay.gameplay_action_entries:
        warnings.append("gameplay_action_entries are accepted but deferred by the first ingest pass")
    if replay.opponent_card_observations:
        warnings.append("opponent_card_observations are accepted but deferred by the first ingest pass")
    if replay.field_evidence_entries:
        warnings.append("field_evidence_entries are accepted but deferred by the first ingest pass")
    return warnings


def _deferred_optional_skips(replay: ParserNormalizedReplayInput) -> dict[str, int]:
    skipped: dict[str, int] = {}
    if replay.gameplay_action_entries:
        skipped["gameplay_action_entries"] = len(replay.gameplay_action_entries)
    if replay.opponent_card_observations:
        skipped["opponent_card_observations"] = len(replay.opponent_card_observations)
    if replay.field_evidence_entries:
        skipped["field_evidence_entries"] = len(replay.field_evidence_entries)
    return skipped


def _jsonable(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_jsonable(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)
