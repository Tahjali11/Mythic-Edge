from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status

HISTORY_SCHEMA_VERSION = "analytics_app_match_game_history_views.v1"
EARLY_GAME_HISTORY_SCHEMA_VERSION = "analytics_app_opening_hand_mulligan_views.v1"
MATCH_HISTORY_OBJECT = "mythic_edge_local_app_match_history"
GAME_HISTORY_OBJECT = "mythic_edge_local_app_game_history"
OPENING_HAND_HISTORY_OBJECT = "mythic_edge_local_app_opening_hand_history"
MULLIGAN_HISTORY_OBJECT = "mythic_edge_local_app_mulligan_history"
DEFAULT_HISTORY_LIMIT = 50
MAX_HISTORY_LIMIT = 100
DEGRADED_DRIFT_STATUSES = {"degraded", "conflict", "missing_expected_evidence", "redacted"}
STATUS_OBJECT_KEYS = {
    "value_source",
    "confidence",
    "finality",
    "drift_status",
    "availability_status",
    "source_parser_surface",
    "source_fact_key",
    "ingest_run_id",
}


def build_match_history(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history(
        paths,
        object_name=MATCH_HISTORY_OBJECT,
        limit=limit,
        offset=offset,
        query=_MATCH_HISTORY_QUERY,
        row_mapper=_match_row,
    )


def build_game_history(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history(
        paths,
        object_name=GAME_HISTORY_OBJECT,
        limit=limit,
        offset=offset,
        query=_GAME_HISTORY_QUERY,
        row_mapper=_game_row,
    )


def build_opening_hand_history(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history_with_children(
        paths,
        object_name=OPENING_HAND_HISTORY_OBJECT,
        schema_version=EARLY_GAME_HISTORY_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        parent_query=_OPENING_HAND_HISTORY_QUERY,
        parent_id_column="opening_hand_id",
        child_query=_query_opening_hand_cards,
        row_mapper=_opening_hand_row,
    )


def build_mulligan_history(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history_with_children(
        paths,
        object_name=MULLIGAN_HISTORY_OBJECT,
        schema_version=EARLY_GAME_HISTORY_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        parent_query=_MULLIGAN_HISTORY_QUERY,
        parent_id_column="mulligan_event_id",
        child_query=_query_mulligan_cards,
        row_mapper=_mulligan_row,
    )


def _build_history(
    paths: LocalAppPaths,
    *,
    object_name: str,
    limit: int,
    offset: int,
    query: str,
    row_mapper: Any,
    schema_version: str = HISTORY_SCHEMA_VERSION,
) -> dict[str, object]:
    normalized_limit = _normalize_limit(limit)
    normalized_offset = _normalize_offset(offset)
    database_status = build_analytics_database_status(paths)
    database = _history_database(database_status)
    status = str(database_status.get("status", "error"))
    schema_status = str(database["schema_status"])

    if status in {"missing", "unavailable"}:
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status=status,
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
        )
    if status == "error":
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="error",
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            errors=_stable_codes(database_status.get("errors"), fallback="analytics_history_database_unavailable"),
        )
    if schema_status != "schema_current":
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="degraded",
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            warnings=["analytics_schema_not_current"],
        )

    database_path = paths.analytics_database
    if database_path is None:
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="unavailable",
            database={**database, "status": "unavailable"},
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            errors=["app_data_root_unavailable"],
        )

    try:
        rows = _query_history(database_path, query=query, limit=normalized_limit, offset=normalized_offset)
    except (OSError, sqlite3.DatabaseError):
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="error",
            database={**database, "status": "error"},
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            errors=["analytics_history_query_failed"],
        )

    mapped_rows = [row_mapper(row) for row in rows]
    return _payload(
        object_name=object_name,
        schema_version=schema_version,
        status="ok" if mapped_rows else "empty",
        database=database,
        limit=normalized_limit,
        offset=normalized_offset,
        rows=mapped_rows,
    )


def _build_history_with_children(
    paths: LocalAppPaths,
    *,
    object_name: str,
    schema_version: str,
    limit: int,
    offset: int,
    parent_query: str,
    parent_id_column: str,
    child_query: Any,
    row_mapper: Any,
) -> dict[str, object]:
    normalized_limit = _normalize_limit(limit)
    normalized_offset = _normalize_offset(offset)
    database_status = build_analytics_database_status(paths)
    database = _history_database(database_status)
    status = str(database_status.get("status", "error"))
    schema_status = str(database["schema_status"])

    if status in {"missing", "unavailable"}:
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status=status,
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            card_row_count=0,
        )
    if status == "error":
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="error",
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            warnings=[],
            errors=_stable_codes(database_status.get("errors"), fallback="analytics_history_database_unavailable"),
            card_row_count=0,
        )
    if schema_status != "schema_current":
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="degraded",
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            warnings=["analytics_schema_not_current"],
            card_row_count=0,
        )

    database_path = paths.analytics_database
    if database_path is None:
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="unavailable",
            database={**database, "status": "unavailable"},
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            errors=["app_data_root_unavailable"],
            card_row_count=0,
        )

    try:
        parent_rows = _query_history(
            database_path,
            query=parent_query,
            limit=normalized_limit,
            offset=normalized_offset,
        )
        child_rows = child_query(
            database_path,
            tuple(str(row[parent_id_column]) for row in parent_rows),
        )
    except (OSError, sqlite3.DatabaseError):
        return _payload(
            object_name=object_name,
            schema_version=schema_version,
            status="error",
            database={**database, "status": "error"},
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
            errors=["analytics_history_query_failed"],
            card_row_count=0,
        )

    mapped_rows = [row_mapper(row, child_rows.get(str(row[parent_id_column]), [])) for row in parent_rows]
    return _payload(
        object_name=object_name,
        schema_version=schema_version,
        status="ok" if mapped_rows else "empty",
        database=database,
        limit=normalized_limit,
        offset=normalized_offset,
        rows=mapped_rows,
        card_row_count=sum(len(row["cards"]) for row in mapped_rows if isinstance(row.get("cards"), list)),
    )


def _query_history(database_path: Path, *, query: str, limit: int, offset: int) -> list[sqlite3.Row]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return list(connection.execute(query, (limit, offset)).fetchall())
    finally:
        connection.close()


def _query_opening_hand_cards(database_path: Path, opening_hand_ids: tuple[str, ...]) -> dict[str, list[sqlite3.Row]]:
    if not opening_hand_ids:
        return {}

    placeholders = ", ".join("?" for _ in opening_hand_ids)
    query = f"""
SELECT
    opening_hand_id,
    opening_hand_card_id,
    card_position,
    grp_id,
    card_name,
    identity_hint_source,
    name_resolution_status,
    value_source AS card_value_source,
    confidence AS card_confidence,
    finality AS card_finality,
    drift_status AS card_drift_status,
    availability_status AS card_availability_status,
    source_parser_surface AS card_source_parser_surface,
    source_fact_key AS card_source_fact_key,
    ingest_run_id AS card_ingest_run_id
FROM opening_hand_cards
WHERE opening_hand_id IN ({placeholders})
ORDER BY
    opening_hand_id ASC,
    card_position ASC,
    opening_hand_card_id ASC
"""
    return _query_child_rows(
        database_path,
        query=query,
        parent_ids=opening_hand_ids,
        parent_column="opening_hand_id",
    )


def _query_mulligan_cards(database_path: Path, mulligan_event_ids: tuple[str, ...]) -> dict[str, list[sqlite3.Row]]:
    if not mulligan_event_ids:
        return {}

    placeholders = ", ".join("?" for _ in mulligan_event_ids)
    query = f"""
SELECT
    mulligan_event_id,
    mulligan_card_id,
    card_position,
    card_action,
    grp_id,
    card_name,
    identity_hint_source,
    value_source AS card_value_source,
    confidence AS card_confidence,
    finality AS card_finality,
    drift_status AS card_drift_status,
    availability_status AS card_availability_status,
    source_parser_surface AS card_source_parser_surface,
    source_fact_key AS card_source_fact_key,
    ingest_run_id AS card_ingest_run_id
FROM mulligan_bottomed_or_discarded_cards
WHERE mulligan_event_id IN ({placeholders})
ORDER BY
    mulligan_event_id ASC,
    card_position ASC,
    mulligan_card_id ASC
"""
    return _query_child_rows(
        database_path,
        query=query,
        parent_ids=mulligan_event_ids,
        parent_column="mulligan_event_id",
    )


def _query_child_rows(
    database_path: Path,
    *,
    query: str,
    parent_ids: tuple[str, ...],
    parent_column: str,
) -> dict[str, list[sqlite3.Row]]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(query, parent_ids).fetchall()
    finally:
        connection.close()

    grouped: dict[str, list[sqlite3.Row]] = {parent_id: [] for parent_id in parent_ids}
    for row in rows:
        grouped.setdefault(str(row[parent_column]), []).append(row)
    return grouped


def _payload(
    *,
    object_name: str,
    schema_version: str = HISTORY_SCHEMA_VERSION,
    status: str,
    database: dict[str, object],
    limit: int,
    offset: int,
    rows: list[dict[str, object]],
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    card_row_count: int | None = None,
) -> dict[str, object]:
    return {
        "object": object_name,
        "schema_version": schema_version,
        "status": status,
        "database": database,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "returned": len(rows),
        },
        "summary": _summary(rows, card_row_count=card_row_count),
        "rows": rows,
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _history_database(database_status: dict[str, object]) -> dict[str, object]:
    database = database_status.get("database")
    if not isinstance(database, dict):
        return {
            "display_path": display_app_path("db", "mythic_edge.sqlite3"),
            "exists": False,
            "schema_status": "unavailable",
            "status": "error",
        }
    return {
        "display_path": str(database.get("display_path", display_app_path("db", "mythic_edge.sqlite3"))),
        "exists": bool(database.get("exists", False)),
        "schema_status": str(database.get("schema_status", "unknown")),
        "status": str(database_status.get("status", "error")),
    }


def _summary(rows: list[dict[str, object]], *, card_row_count: int | None = None) -> dict[str, int]:
    summary = {
        "row_count": len(rows),
    }
    if card_row_count is not None:
        summary["card_row_count"] = card_row_count
    summary.update(
        {
            "degraded_row_count": sum(1 for row in rows if _row_is_degraded(row)),
            "unavailable_row_count": sum(1 for row in rows if _row_is_unavailable(row)),
            "conflict_row_count": sum(1 for row in rows if _row_is_conflict(row)),
        }
    )
    return summary


def _row_is_degraded(row: dict[str, object]) -> bool:
    return any(
        _status_value(status, "drift_status") in DEGRADED_DRIFT_STATUSES
        or _status_value(status, "value_source") == "conflict"
        or _status_value(status, "confidence") in {"low", "unknown"}
        for status in _included_statuses(row)
    )


def _row_is_unavailable(row: dict[str, object]) -> bool:
    return any(_status_value(status, "availability_status") != "available" for status in _included_statuses(row))


def _row_is_conflict(row: dict[str, object]) -> bool:
    return any(
        _status_value(status, "drift_status") == "conflict" or _status_value(status, "value_source") == "conflict"
        for status in _included_statuses(row)
    )


def _included_statuses(row: dict[str, object]) -> list[dict[str, object]]:
    statuses: list[dict[str, object]] = []
    _collect_statuses(row, statuses)
    return statuses


def _collect_statuses(value: object, statuses: list[dict[str, object]]) -> None:
    if isinstance(value, dict):
        if STATUS_OBJECT_KEYS <= value.keys():
            statuses.append(value)
            return
        for nested in value.values():
            _collect_statuses(nested, statuses)
        return
    if isinstance(value, list):
        for nested in value:
            _collect_statuses(nested, statuses)


def _status_value(status: dict[str, object], key: str) -> str:
    return str(status.get(key, "")).lower()


def _status_object(row: sqlite3.Row, prefix: str) -> dict[str, object]:
    return {
        "value_source": row[f"{prefix}_value_source"],
        "confidence": row[f"{prefix}_confidence"],
        "finality": row[f"{prefix}_finality"],
        "drift_status": row[f"{prefix}_drift_status"],
        "availability_status": row[f"{prefix}_availability_status"],
        "source_parser_surface": row[f"{prefix}_source_parser_surface"],
        "source_fact_key": row[f"{prefix}_source_fact_key"],
        "ingest_run_id": row[f"{prefix}_ingest_run_id"],
    }


def _optional_status_object(row: sqlite3.Row, id_column: str, prefix: str) -> dict[str, object] | None:
    if row[id_column] is None:
        return None
    return _status_object(row, prefix)


def _match_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "match_id": row["match_id"],
        "parser_match_key": row["parser_match_key"],
        "match_started_at": row["match_started_at"],
        "match_completed_at": row["match_completed_at"],
        "match_result": row["match_result"],
        "match_win": row["match_win"],
        "games_won": row["games_won"],
        "games_lost": row["games_lost"],
        "total_games": row["total_games"],
        "game_win_rate": row["game_win_rate"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "match_status": _status_object(row, "match"),
        "result_status": _optional_status_object(row, "result_id", "result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _game_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "game_id": row["game_id"],
        "match_id": row["match_id"],
        "game_number": row["game_number"],
        "game_started_at": row["game_started_at"],
        "game_completed_at": row["game_completed_at"],
        "local_result": row["local_result"],
        "winner_team_id": row["winner_team_id"],
        "pre_postboard_label": row["pre_postboard_label"],
        "play_draw": row["play_draw"],
        "turn_count": row["turn_count"],
        "game_duration_seconds": row["game_duration_seconds"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "game_status": _status_object(row, "game"),
        "result_status": _optional_status_object(row, "result_id", "result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _opening_hand_row(row: sqlite3.Row, card_rows: list[sqlite3.Row]) -> dict[str, object]:
    return {
        "opening_hand_id": row["opening_hand_id"],
        "match_id": row["match_id"],
        "game_id": row["game_id"],
        "game_number": row["game_number"],
        "hand_size": row["hand_size"],
        "exact_card_count": row["exact_card_count"],
        "local_result": row["local_result"],
        "play_draw": row["play_draw"],
        "pre_postboard_label": row["pre_postboard_label"],
        "match_result": row["match_result"],
        "match_win": row["match_win"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "cards": [_opening_hand_card_row(card_row) for card_row in card_rows],
        "opening_hand_status": _status_object(row, "opening_hand"),
        "game_status": _optional_status_object(row, "joined_game_id", "game"),
        "game_result_status": _optional_status_object(row, "game_result_id", "game_result"),
        "match_result_status": _optional_status_object(row, "match_result_id", "match_result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _opening_hand_card_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "opening_hand_card_id": row["opening_hand_card_id"],
        "card_position": row["card_position"],
        "grp_id": row["grp_id"],
        "card_name": row["card_name"],
        "identity_hint_source": row["identity_hint_source"],
        "name_resolution_status": row["name_resolution_status"],
        "card_status": _status_object(row, "card"),
    }


def _mulligan_row(row: sqlite3.Row, card_rows: list[sqlite3.Row]) -> dict[str, object]:
    return {
        "mulligan_event_id": row["mulligan_event_id"],
        "match_id": row["match_id"],
        "game_id": row["game_id"],
        "game_number": row["game_number"],
        "ordinal_or_count": row["ordinal_or_count"],
        "mulligan_count": row["mulligan_count"],
        "decision_detail": row["decision_detail"],
        "local_result": row["local_result"],
        "play_draw": row["play_draw"],
        "pre_postboard_label": row["pre_postboard_label"],
        "match_result": row["match_result"],
        "match_win": row["match_win"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "cards": [_mulligan_card_row(card_row) for card_row in card_rows],
        "mulligan_status": _status_object(row, "mulligan"),
        "game_status": _optional_status_object(row, "joined_game_id", "game"),
        "game_result_status": _optional_status_object(row, "game_result_id", "game_result"),
        "match_result_status": _optional_status_object(row, "match_result_id", "match_result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _mulligan_card_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "mulligan_card_id": row["mulligan_card_id"],
        "card_position": row["card_position"],
        "card_action": row["card_action"],
        "grp_id": row["grp_id"],
        "card_name": row["card_name"],
        "identity_hint_source": row["identity_hint_source"],
        "card_status": _status_object(row, "card"),
    }


def _normalize_limit(value: int) -> int:
    return min(max(int(value), 1), MAX_HISTORY_LIMIT)


def _normalize_offset(value: int) -> int:
    return max(int(value), 0)


def _stable_codes(value: object, *, fallback: str) -> list[str]:
    if isinstance(value, list) and all(isinstance(entry, str) for entry in value):
        return value
    return [fallback]


_MATCH_HISTORY_QUERY = """
SELECT
    m.match_id,
    m.parser_match_key,
    m.match_started_at,
    m.match_completed_at,
    mr.match_result,
    mr.match_win,
    mr.games_won,
    mr.games_lost,
    mr.total_games,
    mr.game_win_rate,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    m.value_source AS match_value_source,
    m.confidence AS match_confidence,
    m.finality AS match_finality,
    m.drift_status AS match_drift_status,
    m.availability_status AS match_availability_status,
    m.source_parser_surface AS match_source_parser_surface,
    m.source_fact_key AS match_source_fact_key,
    m.ingest_run_id AS match_ingest_run_id,
    mr.match_result_id AS result_id,
    mr.value_source AS result_value_source,
    mr.confidence AS result_confidence,
    mr.finality AS result_finality,
    mr.drift_status AS result_drift_status,
    mr.availability_status AS result_availability_status,
    mr.source_parser_surface AS result_source_parser_surface,
    mr.source_fact_key AS result_source_fact_key,
    mr.ingest_run_id AS result_ingest_run_id,
    mc.match_context_id AS context_id,
    mc.value_source AS context_value_source,
    mc.confidence AS context_confidence,
    mc.finality AS context_finality,
    mc.drift_status AS context_drift_status,
    mc.availability_status AS context_availability_status,
    mc.source_parser_surface AS context_source_parser_surface,
    mc.source_fact_key AS context_source_fact_key,
    mc.ingest_run_id AS context_ingest_run_id
FROM matches AS m
LEFT JOIN match_results AS mr
    ON mr.match_id = m.match_id
LEFT JOIN match_context AS mc
    ON mc.match_id = m.match_id
ORDER BY
    COALESCE(m.match_completed_at, m.match_started_at, m.updated_at) DESC,
    m.match_id DESC
LIMIT ? OFFSET ?
"""

_OPENING_HAND_HISTORY_QUERY = """
SELECT
    oh.opening_hand_id,
    oh.match_id,
    oh.game_id,
    oh.game_number,
    oh.hand_size,
    oh.exact_card_count,
    gr.local_result,
    gr.play_draw,
    gr.pre_postboard_label,
    mr.match_result,
    mr.match_win,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    oh.value_source AS opening_hand_value_source,
    oh.confidence AS opening_hand_confidence,
    oh.finality AS opening_hand_finality,
    oh.drift_status AS opening_hand_drift_status,
    oh.availability_status AS opening_hand_availability_status,
    oh.source_parser_surface AS opening_hand_source_parser_surface,
    oh.source_fact_key AS opening_hand_source_fact_key,
    oh.ingest_run_id AS opening_hand_ingest_run_id,
    g.game_id AS joined_game_id,
    g.value_source AS game_value_source,
    g.confidence AS game_confidence,
    g.finality AS game_finality,
    g.drift_status AS game_drift_status,
    g.availability_status AS game_availability_status,
    g.source_parser_surface AS game_source_parser_surface,
    g.source_fact_key AS game_source_fact_key,
    g.ingest_run_id AS game_ingest_run_id,
    gr.game_result_id AS game_result_id,
    gr.value_source AS game_result_value_source,
    gr.confidence AS game_result_confidence,
    gr.finality AS game_result_finality,
    gr.drift_status AS game_result_drift_status,
    gr.availability_status AS game_result_availability_status,
    gr.source_parser_surface AS game_result_source_parser_surface,
    gr.source_fact_key AS game_result_source_fact_key,
    gr.ingest_run_id AS game_result_ingest_run_id,
    mr.match_result_id AS match_result_id,
    mr.value_source AS match_result_value_source,
    mr.confidence AS match_result_confidence,
    mr.finality AS match_result_finality,
    mr.drift_status AS match_result_drift_status,
    mr.availability_status AS match_result_availability_status,
    mr.source_parser_surface AS match_result_source_parser_surface,
    mr.source_fact_key AS match_result_source_fact_key,
    mr.ingest_run_id AS match_result_ingest_run_id,
    mc.match_context_id AS context_id,
    mc.value_source AS context_value_source,
    mc.confidence AS context_confidence,
    mc.finality AS context_finality,
    mc.drift_status AS context_drift_status,
    mc.availability_status AS context_availability_status,
    mc.source_parser_surface AS context_source_parser_surface,
    mc.source_fact_key AS context_source_fact_key,
    mc.ingest_run_id AS context_ingest_run_id
FROM opening_hands AS oh
LEFT JOIN games AS g
    ON g.game_id = oh.game_id
LEFT JOIN game_results AS gr
    ON gr.game_id = oh.game_id
LEFT JOIN match_results AS mr
    ON mr.match_id = oh.match_id
LEFT JOIN match_context AS mc
    ON mc.match_id = oh.match_id
ORDER BY
    COALESCE(g.game_completed_at, gr.game_completed_at, g.game_started_at, g.updated_at) DESC,
    oh.match_id DESC,
    oh.game_number ASC,
    oh.opening_hand_id ASC
LIMIT ? OFFSET ?
"""

_MULLIGAN_HISTORY_QUERY = """
SELECT
    me.mulligan_event_id,
    me.match_id,
    me.game_id,
    me.game_number,
    me.ordinal_or_count,
    me.mulligan_count,
    me.decision_detail,
    gr.local_result,
    gr.play_draw,
    gr.pre_postboard_label,
    mr.match_result,
    mr.match_win,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    me.value_source AS mulligan_value_source,
    me.confidence AS mulligan_confidence,
    me.finality AS mulligan_finality,
    me.drift_status AS mulligan_drift_status,
    me.availability_status AS mulligan_availability_status,
    me.source_parser_surface AS mulligan_source_parser_surface,
    me.source_fact_key AS mulligan_source_fact_key,
    me.ingest_run_id AS mulligan_ingest_run_id,
    g.game_id AS joined_game_id,
    g.value_source AS game_value_source,
    g.confidence AS game_confidence,
    g.finality AS game_finality,
    g.drift_status AS game_drift_status,
    g.availability_status AS game_availability_status,
    g.source_parser_surface AS game_source_parser_surface,
    g.source_fact_key AS game_source_fact_key,
    g.ingest_run_id AS game_ingest_run_id,
    gr.game_result_id AS game_result_id,
    gr.value_source AS game_result_value_source,
    gr.confidence AS game_result_confidence,
    gr.finality AS game_result_finality,
    gr.drift_status AS game_result_drift_status,
    gr.availability_status AS game_result_availability_status,
    gr.source_parser_surface AS game_result_source_parser_surface,
    gr.source_fact_key AS game_result_source_fact_key,
    gr.ingest_run_id AS game_result_ingest_run_id,
    mr.match_result_id AS match_result_id,
    mr.value_source AS match_result_value_source,
    mr.confidence AS match_result_confidence,
    mr.finality AS match_result_finality,
    mr.drift_status AS match_result_drift_status,
    mr.availability_status AS match_result_availability_status,
    mr.source_parser_surface AS match_result_source_parser_surface,
    mr.source_fact_key AS match_result_source_fact_key,
    mr.ingest_run_id AS match_result_ingest_run_id,
    mc.match_context_id AS context_id,
    mc.value_source AS context_value_source,
    mc.confidence AS context_confidence,
    mc.finality AS context_finality,
    mc.drift_status AS context_drift_status,
    mc.availability_status AS context_availability_status,
    mc.source_parser_surface AS context_source_parser_surface,
    mc.source_fact_key AS context_source_fact_key,
    mc.ingest_run_id AS context_ingest_run_id
FROM mulligan_events AS me
LEFT JOIN games AS g
    ON g.game_id = me.game_id
LEFT JOIN game_results AS gr
    ON gr.game_id = me.game_id
LEFT JOIN match_results AS mr
    ON mr.match_id = me.match_id
LEFT JOIN match_context AS mc
    ON mc.match_id = me.match_id
ORDER BY
    COALESCE(g.game_completed_at, gr.game_completed_at, g.game_started_at, g.updated_at) DESC,
    me.match_id DESC,
    me.game_number ASC,
    me.ordinal_or_count ASC,
    me.mulligan_event_id ASC
LIMIT ? OFFSET ?
"""

_GAME_HISTORY_QUERY = """
SELECT
    g.game_id,
    g.match_id,
    g.game_number,
    g.game_started_at,
    g.game_completed_at,
    gr.local_result,
    gr.winner_team_id,
    gr.pre_postboard_label,
    gr.play_draw,
    gr.turn_count,
    gr.game_duration_seconds,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    g.value_source AS game_value_source,
    g.confidence AS game_confidence,
    g.finality AS game_finality,
    g.drift_status AS game_drift_status,
    g.availability_status AS game_availability_status,
    g.source_parser_surface AS game_source_parser_surface,
    g.source_fact_key AS game_source_fact_key,
    g.ingest_run_id AS game_ingest_run_id,
    gr.game_result_id AS result_id,
    gr.value_source AS result_value_source,
    gr.confidence AS result_confidence,
    gr.finality AS result_finality,
    gr.drift_status AS result_drift_status,
    gr.availability_status AS result_availability_status,
    gr.source_parser_surface AS result_source_parser_surface,
    gr.source_fact_key AS result_source_fact_key,
    gr.ingest_run_id AS result_ingest_run_id,
    mc.match_context_id AS context_id,
    mc.value_source AS context_value_source,
    mc.confidence AS context_confidence,
    mc.finality AS context_finality,
    mc.drift_status AS context_drift_status,
    mc.availability_status AS context_availability_status,
    mc.source_parser_surface AS context_source_parser_surface,
    mc.source_fact_key AS context_source_fact_key,
    mc.ingest_run_id AS context_ingest_run_id
FROM games AS g
LEFT JOIN game_results AS gr
    ON gr.game_id = g.game_id
LEFT JOIN match_context AS mc
    ON mc.match_id = g.match_id
ORDER BY
    COALESCE(g.game_completed_at, gr.game_completed_at, g.game_started_at, g.updated_at) DESC,
    g.match_id DESC,
    g.game_number ASC
LIMIT ? OFFSET ?
"""
