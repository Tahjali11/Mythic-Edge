from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status

HISTORY_SCHEMA_VERSION = "analytics_app_match_game_history_views.v1"
EARLY_GAME_HISTORY_SCHEMA_VERSION = "analytics_app_opening_hand_mulligan_views.v1"
ACTION_REVIEW_SCHEMA_VERSION = "analytics_app_gameplay_action_opponent_observation_views.v1"
SPLIT_REVIEW_SCHEMA_VERSION = "analytics_app_play_draw_postboard_split_views.v1"
MATCH_HISTORY_OBJECT = "mythic_edge_local_app_match_history"
GAME_HISTORY_OBJECT = "mythic_edge_local_app_game_history"
OPENING_HAND_HISTORY_OBJECT = "mythic_edge_local_app_opening_hand_history"
MULLIGAN_HISTORY_OBJECT = "mythic_edge_local_app_mulligan_history"
GAMEPLAY_ACTION_REVIEW_OBJECT = "mythic_edge_local_app_gameplay_action_review"
OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT = "mythic_edge_local_app_opponent_card_observation_review"
PLAY_DRAW_SPLIT_REVIEW_OBJECT = "mythic_edge_local_app_play_draw_split_review"
GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT = "mythic_edge_local_app_game1_postboard_split_review"
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
REDACTED_DEGRADATION_FLAG = "opponent_observation_degradation_flag_redacted"
PRIVATE_DEGRADATION_FLAG_MARKERS = (
    "player.log",
    "script.google.com",
    "hooks.",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
    "secret",
    "password",
    "token",
)


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


def build_gameplay_action_review(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history_with_children(
        paths,
        object_name=GAMEPLAY_ACTION_REVIEW_OBJECT,
        schema_version=ACTION_REVIEW_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        parent_query=_GAMEPLAY_ACTION_REVIEW_QUERY,
        parent_id_column="gameplay_action_id",
        child_query=_query_gameplay_action_cards,
        row_mapper=_gameplay_action_row,
        include_review_required_count=True,
    )


def build_opponent_card_observation_review(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history_with_children(
        paths,
        object_name=OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT,
        schema_version=ACTION_REVIEW_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        parent_query=_OPPONENT_CARD_OBSERVATION_REVIEW_QUERY,
        parent_id_column="opponent_card_observation_id",
        child_query=_query_opponent_card_observation_cards,
        row_mapper=_opponent_card_observation_row,
        row_warning_mapper=_opponent_card_observation_warnings,
        include_review_required_count=True,
    )


def build_play_draw_split_review(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history(
        paths,
        object_name=PLAY_DRAW_SPLIT_REVIEW_OBJECT,
        schema_version=SPLIT_REVIEW_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        query=_PLAY_DRAW_SPLIT_REVIEW_QUERY,
        row_mapper=_play_draw_split_row,
        summary_builder=_play_draw_split_summary,
    )


def build_game1_postboard_split_review(
    paths: LocalAppPaths,
    *,
    limit: int = DEFAULT_HISTORY_LIMIT,
    offset: int = 0,
) -> dict[str, object]:
    return _build_history(
        paths,
        object_name=GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
        schema_version=SPLIT_REVIEW_SCHEMA_VERSION,
        limit=limit,
        offset=offset,
        query=_GAME1_POSTBOARD_SPLIT_REVIEW_QUERY,
        row_mapper=_game1_postboard_split_row,
        summary_builder=_game1_postboard_split_summary,
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
    summary_builder: Any | None = None,
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
            summary_override=_custom_summary(summary_builder, []),
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
            summary_override=_custom_summary(summary_builder, []),
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
            summary_override=_custom_summary(summary_builder, []),
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
            summary_override=_custom_summary(summary_builder, []),
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
            summary_override=_custom_summary(summary_builder, []),
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
        summary_override=_custom_summary(summary_builder, mapped_rows),
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
    row_warning_mapper: Any | None = None,
    include_review_required_count: bool = False,
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
            include_review_required_count=include_review_required_count,
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
            include_review_required_count=include_review_required_count,
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
            include_review_required_count=include_review_required_count,
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
            include_review_required_count=include_review_required_count,
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
            include_review_required_count=include_review_required_count,
        )

    mapped_rows = [row_mapper(row, child_rows.get(str(row[parent_id_column]), [])) for row in parent_rows]
    warnings = _collect_row_warnings(parent_rows, mapped_rows, row_warning_mapper)
    return _payload(
        object_name=object_name,
        schema_version=schema_version,
        status="ok" if mapped_rows else "empty",
        database=database,
        limit=normalized_limit,
        offset=normalized_offset,
        rows=mapped_rows,
        warnings=warnings,
        card_row_count=sum(len(row["cards"]) for row in mapped_rows if isinstance(row.get("cards"), list)),
        include_review_required_count=include_review_required_count,
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


def _query_gameplay_action_cards(
    database_path: Path,
    gameplay_action_ids: tuple[str, ...],
) -> dict[str, list[sqlite3.Row]]:
    if not gameplay_action_ids:
        return {}

    placeholders = ", ".join("?" for _ in gameplay_action_ids)
    query = f"""
SELECT
    gameplay_action_id,
    gameplay_action_card_id,
    card_ordinal,
    instance_id,
    grp_id,
    observed_grp_id,
    overlay_grp_id,
    object_source_grp_id,
    identity_hint_source,
    card_name,
    display_name,
    name_resolution_status,
    enrichment_status,
    value_source AS card_value_source,
    confidence AS card_confidence,
    finality AS card_finality,
    drift_status AS card_drift_status,
    availability_status AS card_availability_status,
    source_parser_surface AS card_source_parser_surface,
    source_fact_key AS card_source_fact_key,
    ingest_run_id AS card_ingest_run_id
FROM gameplay_action_cards
WHERE gameplay_action_id IN ({placeholders})
ORDER BY
    gameplay_action_id ASC,
    card_ordinal ASC,
    gameplay_action_card_id ASC
"""
    return _query_child_rows(
        database_path,
        query=query,
        parent_ids=gameplay_action_ids,
        parent_column="gameplay_action_id",
    )


def _query_opponent_card_observation_cards(
    database_path: Path,
    opponent_card_observation_ids: tuple[str, ...],
) -> dict[str, list[sqlite3.Row]]:
    if not opponent_card_observation_ids:
        return {}

    placeholders = ", ".join("?" for _ in opponent_card_observation_ids)
    query = f"""
SELECT
    opponent_card_observation_id,
    opponent_card_observation_card_id,
    card_ordinal,
    grp_id,
    observed_grp_id,
    overlay_grp_id,
    object_source_grp_id,
    identity_hint_source,
    card_name,
    resolution_status,
    visibility,
    value_source AS card_value_source,
    confidence AS card_confidence,
    finality AS card_finality,
    drift_status AS card_drift_status,
    availability_status AS card_availability_status,
    source_parser_surface AS card_source_parser_surface,
    source_fact_key AS card_source_fact_key,
    ingest_run_id AS card_ingest_run_id
FROM opponent_card_observation_cards
WHERE opponent_card_observation_id IN ({placeholders})
ORDER BY
    opponent_card_observation_id ASC,
    card_ordinal ASC,
    opponent_card_observation_card_id ASC
"""
    return _query_child_rows(
        database_path,
        query=query,
        parent_ids=opponent_card_observation_ids,
        parent_column="opponent_card_observation_id",
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
    include_review_required_count: bool = False,
    summary_override: dict[str, object] | None = None,
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
        "summary": summary_override
        if summary_override is not None
        else _summary(
            rows,
            card_row_count=card_row_count,
            include_review_required_count=include_review_required_count,
        ),
        "rows": rows,
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _custom_summary(summary_builder: Any | None, rows: list[dict[str, object]]) -> dict[str, object] | None:
    if summary_builder is None:
        return None
    return summary_builder(rows)


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


def _summary(
    rows: list[dict[str, object]],
    *,
    card_row_count: int | None = None,
    include_review_required_count: bool = False,
) -> dict[str, int]:
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
    if include_review_required_count:
        summary["review_required_row_count"] = sum(1 for row in rows if _row_requires_review(row))
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


def _row_requires_review(row: dict[str, object]) -> bool:
    flags = row.get("degradation_flags")
    return row.get("review_required") is True or (isinstance(flags, list) and len(flags) > 0)


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


def _play_draw_split_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "play_draw": row["play_draw"],
        "game_count": _int_value(row["game_count"]),
        "known_result_count": _int_value(row["known_result_count"]),
        "wins": _int_value(row["wins"]),
        "losses": _int_value(row["losses"]),
        "unknown_result_count": _int_value(row["unknown_result_count"]),
        "unavailable_result_count": _int_value(row["unavailable_result_count"]),
        "degraded_result_count": _int_value(row["degraded_result_count"]),
        "win_rate": row["win_rate"],
        "sample_size_warning": row["sample_size_warning"],
    }


def _game1_postboard_split_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "game_result_id": row["game_result_id"],
        "match_id": row["match_id"],
        "game_id": row["game_id"],
        "game_number": row["game_number"],
        "pre_postboard_label": row["pre_postboard_label"],
        "local_result": row["local_result"],
        "play_draw": row["play_draw"],
        "turn_count": row["turn_count"],
        "game_duration_seconds": row["game_duration_seconds"],
        "game_result_status": _status_object(row, "game_result"),
    }


def _play_draw_split_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "row_count": len(rows),
        "total_game_count": sum(_int_value(row.get("game_count")) for row in rows),
        "known_result_count": sum(_int_value(row.get("known_result_count")) for row in rows),
        "wins": sum(_int_value(row.get("wins")) for row in rows),
        "losses": sum(_int_value(row.get("losses")) for row in rows),
        "unknown_result_count": sum(_int_value(row.get("unknown_result_count")) for row in rows),
        "unavailable_result_count": sum(_int_value(row.get("unavailable_result_count")) for row in rows),
        "degraded_result_count": sum(_int_value(row.get("degraded_result_count")) for row in rows),
        "small_sample_group_count": sum(1 for row in rows if row.get("sample_size_warning") == "small_sample"),
    }


def _game1_postboard_split_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "row_count": len(rows),
        "game1_row_count": sum(1 for row in rows if _is_game1_or_preboard(row.get("pre_postboard_label"))),
        "postboard_row_count": sum(1 for row in rows if row.get("pre_postboard_label") == "postboard"),
        "known_result_count": sum(1 for row in rows if row.get("local_result") in {"win", "loss"}),
        "unknown_result_count": sum(1 for row in rows if row.get("local_result") not in {"win", "loss"}),
        "degraded_row_count": sum(1 for row in rows if _row_is_degraded(row)),
        "unavailable_row_count": sum(1 for row in rows if _row_is_unavailable(row)),
        "conflict_row_count": sum(1 for row in rows if _row_is_conflict(row)),
    }


def _is_game1_or_preboard(value: object) -> bool:
    return value in {"game1", "preboard"}


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


def _gameplay_action_row(row: sqlite3.Row, card_rows: list[sqlite3.Row]) -> dict[str, object]:
    return {
        "gameplay_action_id": row["gameplay_action_id"],
        "match_id": row["match_id"],
        "game_id": row["game_id"],
        "game_number": row["game_number"],
        "timestamp": row["timestamp"],
        "game_state_id": row["game_state_id"],
        "turn_number": row["turn_number"],
        "action_type": row["action_type"],
        "actor_relation": row["actor_relation"],
        "from_zone_type": row["from_zone_type"],
        "to_zone_type": row["to_zone_type"],
        "source_status": row["source_status"],
        "annotation_context_label": row["annotation_context_label"],
        "raw_action_type_labels": row["raw_action_type_labels"],
        "annotation_type_labels": row["annotation_type_labels"],
        "visible_in_log": _optional_bool(row["visible_in_log"]),
        "card_count": row["card_count"],
        "grp_ids": _integer_csv(row["grp_ids"]),
        "local_result": row["local_result"],
        "play_draw": row["play_draw"],
        "pre_postboard_label": row["pre_postboard_label"],
        "match_result": row["match_result"],
        "match_win": row["match_win"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "cards": [_gameplay_action_card_row(card_row) for card_row in card_rows],
        "gameplay_action_status": _status_object(row, "gameplay_action"),
        "game_status": _optional_status_object(row, "joined_game_id", "game"),
        "game_result_status": _optional_status_object(row, "game_result_id", "game_result"),
        "match_result_status": _optional_status_object(row, "match_result_id", "match_result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _gameplay_action_card_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "gameplay_action_card_id": row["gameplay_action_card_id"],
        "card_ordinal": row["card_ordinal"],
        "instance_id": row["instance_id"],
        "grp_id": row["grp_id"],
        "observed_grp_id": row["observed_grp_id"],
        "overlay_grp_id": row["overlay_grp_id"],
        "object_source_grp_id": row["object_source_grp_id"],
        "identity_hint_source": row["identity_hint_source"],
        "card_name": row["card_name"],
        "display_name": row["display_name"],
        "name_resolution_status": row["name_resolution_status"],
        "enrichment_status": row["enrichment_status"],
        "card_status": _status_object(row, "card"),
    }


def _opponent_card_observation_row(row: sqlite3.Row, card_rows: list[sqlite3.Row]) -> dict[str, object]:
    return {
        "opponent_card_observation_id": row["opponent_card_observation_id"],
        "gameplay_action_id": row["gameplay_action_id"],
        "match_id": row["match_id"],
        "game_id": row["game_id"],
        "game_number": row["game_number"],
        "timestamp": row["timestamp"],
        "game_state_id": row["game_state_id"],
        "turn_number": row["turn_number"],
        "actor_relation": row["actor_relation"],
        "actor_seat_id": row["actor_seat_id"],
        "local_seat_id": row["local_seat_id"],
        "instance_id": row["instance_id"],
        "grp_id": row["grp_id"],
        "observed_grp_id": row["observed_grp_id"],
        "overlay_grp_id": row["overlay_grp_id"],
        "object_source_grp_id": row["object_source_grp_id"],
        "parent_id": row["parent_id"],
        "identity_hint_source": row["identity_hint_source"],
        "card_name": row["card_name"],
        "display_name": row["display_name"],
        "resolution_status": row["resolution_status"],
        "name_resolution_source": row["name_resolution_source"],
        "action_type": row["action_type"],
        "cast_mode": row["cast_mode"],
        "source_evidence": row["source_evidence"],
        "evidence_status": row["evidence_status"],
        "visibility": row["visibility"],
        "from_zone_type": row["from_zone_type"],
        "to_zone_type": row["to_zone_type"],
        "degradation_flags": _degradation_flags(row["degradation_flags"]),
        "review_required": bool(row["review_required"]),
        "linked_gameplay_action": _linked_gameplay_action(row),
        "local_result": row["local_result"],
        "play_draw": row["play_draw"],
        "pre_postboard_label": row["pre_postboard_label"],
        "match_result": row["match_result"],
        "match_win": row["match_win"],
        "queue_name": row["queue_name"],
        "format_name": row["format_name"],
        "event_id": row["event_id"],
        "cards": [_opponent_card_observation_card_row(card_row) for card_row in card_rows],
        "opponent_card_observation_status": _status_object(row, "opponent_card_observation"),
        "linked_gameplay_action_status": _optional_status_object(
            row,
            "linked_gameplay_action_id",
            "linked_gameplay_action",
        ),
        "game_status": _optional_status_object(row, "joined_game_id", "game"),
        "game_result_status": _optional_status_object(row, "game_result_id", "game_result"),
        "match_result_status": _optional_status_object(row, "match_result_id", "match_result"),
        "context_status": _optional_status_object(row, "context_id", "context"),
    }


def _opponent_card_observation_card_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "opponent_card_observation_card_id": row["opponent_card_observation_card_id"],
        "card_ordinal": row["card_ordinal"],
        "grp_id": row["grp_id"],
        "observed_grp_id": row["observed_grp_id"],
        "overlay_grp_id": row["overlay_grp_id"],
        "object_source_grp_id": row["object_source_grp_id"],
        "identity_hint_source": row["identity_hint_source"],
        "card_name": row["card_name"],
        "resolution_status": row["resolution_status"],
        "visibility": row["visibility"],
        "card_status": _status_object(row, "card"),
    }


def _linked_gameplay_action(row: sqlite3.Row) -> dict[str, object] | None:
    if row["linked_gameplay_action_id"] is None:
        return None
    return {
        "gameplay_action_id": row["linked_gameplay_action_id"],
        "turn_number": row["linked_turn_number"],
        "action_type": row["linked_action_type"],
        "actor_relation": row["linked_actor_relation"],
        "from_zone_type": row["linked_from_zone_type"],
        "to_zone_type": row["linked_to_zone_type"],
        "visible_in_log": _optional_bool(row["linked_visible_in_log"]),
    }


def _opponent_card_observation_warnings(row: sqlite3.Row, mapped_row: dict[str, object]) -> list[str]:
    if _degradation_flags_malformed(row["degradation_flags"]):
        return ["opponent_observation_degradation_flags_malformed"]
    return []


def _collect_row_warnings(
    parent_rows: list[sqlite3.Row],
    mapped_rows: list[dict[str, object]],
    row_warning_mapper: Any | None,
) -> list[str]:
    if row_warning_mapper is None:
        return []
    warnings: list[str] = []
    for parent_row, mapped_row in zip(parent_rows, mapped_rows, strict=False):
        warnings.extend(row_warning_mapper(parent_row, mapped_row))
    return _unique_codes(warnings)


def _unique_codes(codes: list[str]) -> list[str]:
    unique: list[str] = []
    for code in codes:
        if code not in unique:
            unique.append(code)
    return unique


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _int_value(value: object) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int | float):
        return int(value)
    return 0


def _integer_csv(value: object) -> list[int]:
    if not isinstance(value, str) or not value:
        return []
    integers: list[int] = []
    for raw_entry in value.split(","):
        try:
            integers.append(int(raw_entry))
        except ValueError:
            continue
    return integers


def _degradation_flags(value: object) -> list[str]:
    parsed = _parsed_degradation_flags(value)
    if parsed is None:
        return []
    return _safe_degradation_flags(parsed)


def _parsed_degradation_flags(value: object) -> list[str] | None:
    if value is None or value == "":
        return []
    if not isinstance(value, str):
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list) or not all(isinstance(entry, str) for entry in parsed):
        return None
    return parsed


def _degradation_flags_malformed(value: object) -> bool:
    return _parsed_degradation_flags(value) is None


def _safe_degradation_flags(flags: list[str]) -> list[str]:
    safe_flags: list[str] = []
    redacted = False
    for flag in flags:
        if _is_safe_degradation_flag(flag):
            safe_flags.append(flag)
        else:
            redacted = True
    if redacted and REDACTED_DEGRADATION_FLAG not in safe_flags:
        safe_flags.append(REDACTED_DEGRADATION_FLAG)
    return safe_flags


def _is_safe_degradation_flag(value: str) -> bool:
    if not value or len(value) > 100:
        return False
    if value[0].isalpha() and value[1:2] == ":":
        return False
    if "://" in value or "\\" in value or "/" in value or "#" in value:
        return False
    marker_text = value.lower()
    if any(marker in marker_text for marker in PRIVATE_DEGRADATION_FLAG_MARKERS):
        return False
    return all(char.isalnum() or char in "_.:-" for char in value)


def _normalize_limit(value: int) -> int:
    return min(max(int(value), 1), MAX_HISTORY_LIMIT)


def _normalize_offset(value: int) -> int:
    return max(int(value), 0)


def _stable_codes(value: object, *, fallback: str) -> list[str]:
    if isinstance(value, list) and all(isinstance(entry, str) for entry in value):
        return value
    return [fallback]


_PLAY_DRAW_SPLIT_REVIEW_QUERY = """
SELECT
    splits.play_draw,
    splits.game_count,
    splits.known_result_count,
    splits.wins,
    splits.losses,
    splits.unknown_result_count,
    splits.unavailable_result_count,
    splits.degraded_result_count,
    splits.win_rate,
    warnings.sample_size_warning
FROM v_play_draw_splits AS splits
LEFT JOIN v_sample_size_warnings AS warnings
    ON warnings.play_draw = splits.play_draw
ORDER BY
    CASE splits.play_draw
        WHEN 'play' THEN 0
        WHEN 'draw' THEN 1
        WHEN 'unknown' THEN 2
        ELSE 3
    END ASC,
    splits.play_draw ASC
LIMIT ? OFFSET ?
"""

_GAME1_POSTBOARD_SPLIT_REVIEW_QUERY = """
SELECT
    game_result_id,
    match_id,
    game_id,
    game_number,
    pre_postboard_label,
    local_result,
    play_draw,
    turn_count,
    game_duration_seconds,
    value_source AS game_result_value_source,
    confidence AS game_result_confidence,
    finality AS game_result_finality,
    drift_status AS game_result_drift_status,
    availability_status AS game_result_availability_status,
    source_parser_surface AS game_result_source_parser_surface,
    source_fact_key AS game_result_source_fact_key,
    ingest_run_id AS game_result_ingest_run_id
FROM v_game1_vs_postboard
ORDER BY
    match_id DESC,
    game_number ASC,
    game_result_id ASC
LIMIT ? OFFSET ?
"""

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

_GAMEPLAY_ACTION_REVIEW_QUERY = """
SELECT
    ga.gameplay_action_id,
    ga.match_id,
    ga.game_id,
    ga.game_number,
    ga.timestamp,
    ga.game_state_id,
    ga.turn_number,
    ga.action_type,
    ga.actor_relation,
    ga.from_zone_type,
    ga.to_zone_type,
    ga.source_status,
    ga.annotation_context_label,
    ga.raw_action_type_labels,
    ga.annotation_type_labels,
    ga.visible_in_log,
    (
        SELECT COUNT(*)
        FROM gameplay_action_cards AS gac
        WHERE gac.gameplay_action_id = ga.gameplay_action_id
    ) AS card_count,
    (
        SELECT GROUP_CONCAT(card_identity.grp_id)
        FROM (
            SELECT grp_id
            FROM gameplay_action_cards
            WHERE gameplay_action_id = ga.gameplay_action_id
              AND grp_id IS NOT NULL
            ORDER BY card_ordinal
        ) AS card_identity
    ) AS grp_ids,
    gr.local_result,
    gr.play_draw,
    gr.pre_postboard_label,
    mr.match_result,
    mr.match_win,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    ga.value_source AS gameplay_action_value_source,
    ga.confidence AS gameplay_action_confidence,
    ga.finality AS gameplay_action_finality,
    ga.drift_status AS gameplay_action_drift_status,
    ga.availability_status AS gameplay_action_availability_status,
    ga.source_parser_surface AS gameplay_action_source_parser_surface,
    ga.source_fact_key AS gameplay_action_source_fact_key,
    ga.ingest_run_id AS gameplay_action_ingest_run_id,
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
FROM gameplay_actions AS ga
LEFT JOIN games AS g
    ON g.game_id = ga.game_id
LEFT JOIN game_results AS gr
    ON gr.game_id = ga.game_id
LEFT JOIN match_results AS mr
    ON mr.match_id = ga.match_id
LEFT JOIN match_context AS mc
    ON mc.match_id = ga.match_id
ORDER BY
    COALESCE(ga.timestamp, g.game_completed_at, gr.game_completed_at, g.game_started_at, g.updated_at) DESC,
    ga.match_id DESC,
    ga.game_number ASC,
    ga.turn_number ASC,
    ga.gameplay_action_id ASC
LIMIT ? OFFSET ?
"""

_OPPONENT_CARD_OBSERVATION_REVIEW_QUERY = """
SELECT
    oco.opponent_card_observation_id,
    oco.gameplay_action_id,
    oco.match_id,
    oco.game_id,
    oco.game_number,
    oco.timestamp,
    oco.game_state_id,
    oco.turn_number,
    oco.actor_relation,
    oco.actor_seat_id,
    oco.local_seat_id,
    oco.instance_id,
    oco.grp_id,
    oco.observed_grp_id,
    oco.overlay_grp_id,
    oco.object_source_grp_id,
    oco.parent_id,
    oco.identity_hint_source,
    oco.card_name,
    oco.display_name,
    oco.resolution_status,
    oco.name_resolution_source,
    oco.action_type,
    oco.cast_mode,
    oco.source_evidence,
    oco.evidence_status,
    oco.visibility,
    oco.from_zone_type,
    oco.to_zone_type,
    oco.degradation_flags,
    oco.review_required,
    linked.gameplay_action_id AS linked_gameplay_action_id,
    linked.turn_number AS linked_turn_number,
    linked.action_type AS linked_action_type,
    linked.actor_relation AS linked_actor_relation,
    linked.from_zone_type AS linked_from_zone_type,
    linked.to_zone_type AS linked_to_zone_type,
    linked.visible_in_log AS linked_visible_in_log,
    gr.local_result,
    gr.play_draw,
    gr.pre_postboard_label,
    mr.match_result,
    mr.match_win,
    mc.queue_name,
    mc.format_name,
    mc.event_id,
    oco.value_source AS opponent_card_observation_value_source,
    oco.confidence AS opponent_card_observation_confidence,
    oco.finality AS opponent_card_observation_finality,
    oco.drift_status AS opponent_card_observation_drift_status,
    oco.availability_status AS opponent_card_observation_availability_status,
    oco.source_parser_surface AS opponent_card_observation_source_parser_surface,
    oco.source_fact_key AS opponent_card_observation_source_fact_key,
    oco.ingest_run_id AS opponent_card_observation_ingest_run_id,
    linked.value_source AS linked_gameplay_action_value_source,
    linked.confidence AS linked_gameplay_action_confidence,
    linked.finality AS linked_gameplay_action_finality,
    linked.drift_status AS linked_gameplay_action_drift_status,
    linked.availability_status AS linked_gameplay_action_availability_status,
    linked.source_parser_surface AS linked_gameplay_action_source_parser_surface,
    linked.source_fact_key AS linked_gameplay_action_source_fact_key,
    linked.ingest_run_id AS linked_gameplay_action_ingest_run_id,
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
FROM opponent_card_observations AS oco
LEFT JOIN gameplay_actions AS linked
    ON linked.gameplay_action_id = oco.gameplay_action_id
LEFT JOIN games AS g
    ON g.game_id = oco.game_id
LEFT JOIN game_results AS gr
    ON gr.game_id = oco.game_id
LEFT JOIN match_results AS mr
    ON mr.match_id = oco.match_id
LEFT JOIN match_context AS mc
    ON mc.match_id = oco.match_id
ORDER BY
    COALESCE(oco.timestamp, g.game_completed_at, gr.game_completed_at, g.game_started_at, g.updated_at) DESC,
    oco.match_id DESC,
    oco.game_number ASC,
    oco.turn_number ASC,
    oco.opponent_card_observation_id ASC
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
