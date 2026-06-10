from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from .paths import LocalAppPaths
from .setup_status import build_analytics_database_status

ANALYTICS_REFRESH_STATE_OBJECT = "mythic_edge_local_app_analytics_refresh_state"
ANALYTICS_REFRESH_STATE_SCHEMA_VERSION = "analytics_auto_refresh_after_match_completion.v1"

ROW_COUNT_TABLES = ("ingest_runs", "matches", "games", "match_results", "game_results")
TIMESTAMP_TABLES = ("ingest_runs", "matches", "games", "match_results", "game_results")
ZERO_ROW_COUNTS = {table: 0 for table in ROW_COUNT_TABLES}


def build_analytics_refresh_state(paths: LocalAppPaths) -> dict[str, object]:
    database_status = build_analytics_database_status(paths)
    status = str(database_status.get("status", "error"))
    database = database_status.get("database")
    schema_status = str(database.get("schema_status", "unknown")) if isinstance(database, dict) else "unknown"

    if status in {"missing", "unavailable"}:
        return _payload(status=status, row_counts=ZERO_ROW_COUNTS)

    if status == "error":
        return _payload(
            status="error",
            row_counts=ZERO_ROW_COUNTS,
            errors=_stable_codes(
                database_status.get("errors"),
                fallback="analytics_refresh_state_database_unavailable",
            ),
        )

    if schema_status != "schema_current":
        return _payload(status="degraded", row_counts=ZERO_ROW_COUNTS, warnings=["analytics_schema_not_current"])

    database_path = paths.analytics_database
    if database_path is None:
        return _payload(status="unavailable", row_counts=ZERO_ROW_COUNTS, errors=["app_data_root_unavailable"])

    try:
        metadata = _query_refresh_metadata(database_path)
    except (OSError, sqlite3.DatabaseError):
        return _payload(
            status="error",
            row_counts=ZERO_ROW_COUNTS,
            errors=["analytics_refresh_state_query_failed"],
        )

    top_status = "ok" if metadata["latest_completed_match_result_available"] else "empty"
    return _payload(
        status=top_status,
        analytics_revision=_revision_for_metadata(metadata),
        latest_completed_match_result_available=bool(metadata["latest_completed_match_result_available"]),
        latest_completed_match_seen_at=_safe_iso_or_none(metadata["latest_completed_match_seen_at"]),
        latest_completed_ingest_finished_at=_safe_iso_or_none(metadata["latest_completed_ingest_finished_at"]),
        row_counts=_int_row_counts(metadata["row_counts"]),
    )


def _query_refresh_metadata(database_path: Path) -> dict[str, object]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        row_counts = {table: _table_count(connection, table) for table in ROW_COUNT_TABLES}
        table_timestamps = {table: _max_updated_at(connection, table) for table in TIMESTAMP_TABLES}
        latest_completed_match_seen_at = _latest_completed_match_seen_at(connection)
        latest_completed_ingest_finished_at = _latest_completed_ingest_finished_at(connection)
    finally:
        connection.close()

    return {
        "row_counts": row_counts,
        "table_timestamps": table_timestamps,
        "latest_completed_match_result_available": row_counts["match_results"] > 0,
        "latest_completed_match_seen_at": latest_completed_match_seen_at,
        "latest_completed_ingest_finished_at": latest_completed_ingest_finished_at,
    }


def _table_count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _max_updated_at(connection: sqlite3.Connection, table_name: str) -> str | None:
    value = connection.execute(f"SELECT MAX(updated_at) FROM {table_name}").fetchone()[0]
    return _safe_iso_or_none(value)


def _latest_completed_match_seen_at(connection: sqlite3.Connection) -> str | None:
    value = connection.execute(
        """
        SELECT MAX(COALESCE(match_results.updated_at, matches.match_completed_at, matches.updated_at))
        FROM match_results
        LEFT JOIN matches ON matches.match_id = match_results.match_id
        """
    ).fetchone()[0]
    return _safe_iso_or_none(value)


def _latest_completed_ingest_finished_at(connection: sqlite3.Connection) -> str | None:
    value = connection.execute(
        """
        SELECT MAX(finished_at)
        FROM ingest_runs
        WHERE status = 'completed'
        """
    ).fetchone()[0]
    return _safe_iso_or_none(value)


def _revision_for_metadata(metadata: dict[str, object]) -> str:
    table_timestamps = _safe_timestamp_mapping(metadata.get("table_timestamps"))
    revision_payload = {
        "row_counts": metadata["row_counts"],
        "table_timestamps": table_timestamps,
        "latest_completed_match_result_available": metadata["latest_completed_match_result_available"],
        "latest_completed_match_seen_at": _safe_iso_or_none(metadata.get("latest_completed_match_seen_at")),
        "latest_completed_ingest_finished_at": _safe_iso_or_none(
            metadata.get("latest_completed_ingest_finished_at")
        ),
    }
    encoded = json.dumps(revision_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"analytics-refresh-v1:{hashlib.sha256(encoded).hexdigest()[:16]}"


def _payload(
    *,
    status: str,
    row_counts: dict[str, int],
    analytics_revision: str | None = None,
    latest_completed_match_result_available: bool = False,
    latest_completed_match_seen_at: str | None = None,
    latest_completed_ingest_finished_at: str | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": ANALYTICS_REFRESH_STATE_OBJECT,
        "schema_version": ANALYTICS_REFRESH_STATE_SCHEMA_VERSION,
        "status": status,
        "analytics_revision": analytics_revision,
        "latest_completed_match_result_available": latest_completed_match_result_available,
        "latest_completed_match_seen_at": latest_completed_match_seen_at,
        "latest_completed_ingest_finished_at": latest_completed_ingest_finished_at,
        "row_counts": dict(row_counts),
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _stable_codes(value: object, *, fallback: str) -> list[str]:
    if not isinstance(value, list):
        return [fallback]
    codes = sorted({code for code in value if isinstance(code, str) and code})
    return codes or [fallback]


def _int_row_counts(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return dict(ZERO_ROW_COUNTS)
    return {table: max(0, int(value.get(table, 0))) for table in ROW_COUNT_TABLES}


def _safe_timestamp_mapping(value: object) -> dict[str, str | None]:
    if not isinstance(value, dict):
        return {table: None for table in TIMESTAMP_TABLES}
    return {table: _safe_iso_or_none(value.get(table)) for table in TIMESTAMP_TABLES}


def _safe_iso_or_none(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return text
