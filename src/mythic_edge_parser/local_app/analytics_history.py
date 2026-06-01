from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status

HISTORY_SCHEMA_VERSION = "analytics_app_match_game_history_views.v1"
MATCH_HISTORY_OBJECT = "mythic_edge_local_app_match_history"
GAME_HISTORY_OBJECT = "mythic_edge_local_app_game_history"
DEFAULT_HISTORY_LIMIT = 50
MAX_HISTORY_LIMIT = 100
DEGRADED_DRIFT_STATUSES = {"degraded", "conflict", "missing_expected_evidence", "redacted"}


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


def _build_history(
    paths: LocalAppPaths,
    *,
    object_name: str,
    limit: int,
    offset: int,
    query: str,
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
            status=status,
            database=database,
            limit=normalized_limit,
            offset=normalized_offset,
            rows=[],
        )
    if status == "error":
        return _payload(
            object_name=object_name,
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
        status="ok" if mapped_rows else "empty",
        database=database,
        limit=normalized_limit,
        offset=normalized_offset,
        rows=mapped_rows,
    )


def _query_history(database_path: Path, *, query: str, limit: int, offset: int) -> list[sqlite3.Row]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return list(connection.execute(query, (limit, offset)).fetchall())
    finally:
        connection.close()


def _payload(
    *,
    object_name: str,
    status: str,
    database: dict[str, object],
    limit: int,
    offset: int,
    rows: list[dict[str, object]],
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": object_name,
        "schema_version": HISTORY_SCHEMA_VERSION,
        "status": status,
        "database": database,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "returned": len(rows),
        },
        "summary": _summary(rows),
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


def _summary(rows: list[dict[str, object]]) -> dict[str, int]:
    return {
        "row_count": len(rows),
        "degraded_row_count": sum(1 for row in rows if _row_is_degraded(row)),
        "unavailable_row_count": sum(1 for row in rows if _row_is_unavailable(row)),
        "conflict_row_count": sum(1 for row in rows if _row_is_conflict(row)),
    }


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
    for key in ("match_status", "game_status", "result_status", "context_status"):
        value = row.get(key)
        if isinstance(value, dict):
            statuses.append(value)
    return statuses


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
