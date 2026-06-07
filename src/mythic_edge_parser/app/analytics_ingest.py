from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from . import evidence_ledger
from .analytics_migration_loader import ANALYTICS_SCHEMA_VERSION, apply_analytics_migrations
from .opponent_card_observations import (
    OPPONENT_CARD_OBSERVATION_OBJECT,
)
from .opponent_card_observations import (
    SCHEMA_VERSION as OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION,
)

ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION = "analytics_parser_normalized_replay_ingest.v1"
LIVE_PARSER_OWNED_FACT_CAPTURE_SCHEMA_VERSION = "live_app_parser_owned_fact_capture_sqlite.v1"

_ALLOWED_SOURCE_KINDS = {"sanitized_golden_replay", "saved_event_replay"}
_LIVE_SOURCE_KIND = "live_parser"
_LIVE_ALLOWED_FINALITIES = {"final", "reconciled"}
_LIVE_DEFERRED_PAYLOAD_FIELDS = {
    "gameplay_action_entries": "live_gameplay_action_capture_deferred",
    "gameplay_actions": "live_gameplay_action_capture_deferred",
    "opponent_card_observations": "live_opponent_observation_capture_deferred",
    "field_evidence_entries": "live_field_evidence_capture_deferred",
    "field_evidence": "live_field_evidence_capture_deferred",
}
_LIVE_FORBIDDEN_PAYLOAD_FIELDS = {
    "raw_player_log_lines",
    "player_log_lines",
    "raw_saved_event_lines",
    "saved_event_lines",
    "raw_webhook_payloads",
    "webhook_payloads",
    "raw_local_file_paths",
    "local_file_paths",
    "player_log_path",
    "source_path",
    "source_paths",
    "private_jsonl_source_paths",
    "raw_log_hash",
    "raw_log_hashes",
}
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
    "gameplay_actions",
    "gameplay_action_cards",
    "opponent_card_observations",
    "opponent_card_observation_cards",
    "fact_provenance",
)
_UNAVAILABLE_CARD_VALUES = {"", "[]", "{}", "n/a", "na", "none", "unknown", "unavailable", "not available"}
_PRIVATE_LABEL_RE = re.compile(r"(^[a-zA-Z]:[\\/]|^[\\/]|://)")
_INTEGER_TEXT_RE = re.compile(r"[+-]?\d+")
_SAFE_DEGRADATION_FLAG_RE = re.compile(r"[A-Za-z0-9_.-]+")
_PRIVATE_DEGRADATION_MARKERS = (
    "player.log",
    "failed_" + "posts",
    "runtime_" + "status",
    "webhook",
    "api_" + "key",
    "apikey",
    "access_" + "token",
    "secret",
    "password",
    "payload",
)
_ALLOWED_GAMEPLAY_ACTOR_RELATIONS = {"local", "opponent", "unknown", ""}
_GAMEPLAY_ACTION_LEDGER_ENTRY_ID = "tier5.gameplay_action.gameplay_action"
_OPPONENT_CARD_OBSERVATION_LEDGER_ENTRY_ID = (
    "tier5.opponent_card_observation.opponent_card_observation"
)
_ALLOWED_OBSERVATION_VALUE_SOURCES = {"observed", "derived", "inferred", "unknown", "conflict", "legacy_enriched"}
_ALLOWED_OBSERVATION_CONFIDENCE = {"high", "medium", "low", "unknown"}
_ALLOWED_OBSERVATION_EVIDENCE_STATUS = {"observed", "derived", "inferred", "unknown", "conflict", "degraded"}
_ALLOWED_OBSERVATION_VISIBILITY = {
    "action_visible",
    "public_zone",
    "revealed",
    "derived_zone_transition",
    "ambiguous",
    "hidden_not_recorded",
}
_ALLOWED_OBSERVATION_FINALITY = {"reconciled", "final", "provisional", "live"}
_ALLOWED_OBSERVATION_DRIFT_STATUS = {
    "none",
    "not_checked",
    "degraded",
    "conflict",
    "missing_expected_evidence",
    "redacted",
}
_FIELD_EVIDENCE_FACT_TABLE_PRIMARY_KEYS = {
    "matches": "match_id",
    "games": "game_id",
    "match_results": "match_result_id",
    "game_results": "game_result_id",
    "match_context": "match_context_id",
    "rank_snapshots": "rank_snapshot_id",
    "opening_hands": "opening_hand_id",
    "opening_hand_cards": "opening_hand_card_id",
    "mulligan_events": "mulligan_event_id",
    "mulligan_bottomed_or_discarded_cards": "mulligan_card_id",
    "gameplay_actions": "gameplay_action_id",
    "gameplay_action_cards": "gameplay_action_card_id",
    "opponent_card_observations": "opponent_card_observation_id",
    "opponent_card_observation_cards": "opponent_card_observation_card_id",
}
_SAFE_FIELD_EVIDENCE_LABEL_RE = re.compile(r"^[A-Za-z0-9_./:+ -]+$")
_PRIVATE_FIELD_EVIDENCE_MARKERS = (
    "player.log",
    "[unitycrossthreadlogger]",
    "[client gre]",
    "detailed logs:",
    "script.google.com",
    "https://hooks.",
    "http://hooks.",
    "failed_" + "posts",
    "runtime_" + "status",
    "webhook",
    "api_" + "key",
    "apikey",
    "access_" + "token",
    "bearer ",
    "secret",
    "password",
)
_LIVE_PRIVATE_ROW_VALUE_MARKERS = (
    "player.log",
    "[unitycrossthreadlogger]",
    "[clientgre]",
    "detailedlogs:",
    "script.google.com",
    "https://hooks.",
    "http://hooks.",
    "failed_posts",
    "runtime_status",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
)
_LIVE_PRIVATE_ROW_FIELD_MARKERS = (
    "player_log",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "secret",
    "password",
    "local_file_path",
    "raw_log",
    "raw_saved_event",
)
_LOCAL_ABSOLUTE_PATH_ROOTS = (
    "/applications",
    "/etc",
    "/home",
    "/mnt",
    "/opt",
    "/private",
    "/tmp",
    "/users",
    "/var",
    "/volumes",
)
_SLASH_PREFIXED_DRIVE_PATH_RE = re.compile(r"^/[a-z]:($|/)")


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
    session_id: str = ""


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
    _validate_safe_source_artifact_label(source_artifact_label)

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


def normalize_live_parser_owned_facts(payload: Mapping[str, object]) -> ParserNormalizedReplayInput:
    if not isinstance(payload, Mapping):
        raise AnalyticsReplayIngestError("Live parser-owned fact payload must be a mapping")

    source_kind = _required_text(payload.get("source_kind"), "source_kind")
    if source_kind != _LIVE_SOURCE_KIND:
        raise AnalyticsReplayIngestError("Live parser-owned fact payload source_kind must be live_parser")

    source_artifact_label = _required_live_safe_label(payload.get("source_artifact_label"), "source_artifact_label")
    session_id = _required_live_safe_label(payload.get("session_id"), "session_id")
    _reject_live_forbidden_payload_fields(payload)

    match_log_rows = _mapping_tuple(payload.get("match_log_rows"), "match_log_rows", required=True)
    game_log_rows = _mapping_tuple(payload.get("game_log_rows"), "game_log_rows", required=True)
    _reject_live_unsafe_row_payloads(match_log_rows, row_group="match_log_rows")
    _reject_live_unsafe_row_payloads(game_log_rows, row_group="game_log_rows")
    _require_live_final_rows(match_log_rows, row_group="match_log_rows", default_finality="reconciled")
    _require_live_final_rows(game_log_rows, row_group="game_log_rows", default_finality="final")

    return ParserNormalizedReplayInput(
        source_kind=source_kind,
        source_artifact_label=source_artifact_label,
        match_log_rows=match_log_rows,
        game_log_rows=game_log_rows,
        parser_version=_optional_text(payload.get("parser_version")) or "",
        generated_at=_optional_text(payload.get("capture_finished_at"))
        or _optional_text(payload.get("capture_started_at"))
        or "",
        session_id=session_id,
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
        "session_id": replay.session_id,
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
    return _ingest_normalized_replay(
        connection,
        normalized,
        started_at=started_at,
        finished_at=finished_at,
        ingest_optional_fact_families=True,
    )


def ingest_live_parser_owned_facts(
    connection: sqlite3.Connection,
    payload: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult:
    normalized = normalize_live_parser_owned_facts(payload)
    live_warnings = _live_payload_warnings(payload)
    live_skipped = _live_payload_skips(payload)
    return _ingest_normalized_replay(
        connection,
        normalized,
        started_at=started_at or _optional_text(payload.get("capture_started_at")),
        finished_at=finished_at or _optional_text(payload.get("capture_finished_at")),
        ingest_optional_fact_families=False,
        initial_warnings=live_warnings,
        initial_skipped=live_skipped,
    )


def _ingest_normalized_replay(
    connection: sqlite3.Connection,
    normalized: ParserNormalizedReplayInput,
    *,
    started_at: str | None,
    finished_at: str | None,
    ingest_optional_fact_families: bool,
    initial_warnings: list[str] | None = None,
    initial_skipped: dict[str, int] | None = None,
) -> AnalyticsReplayIngestResult:
    ingest_run_id = deterministic_ingest_run_id(normalized)
    timestamp = _ingest_timestamp(started_at, normalized.generated_at)
    completed_at = finished_at or timestamp
    warnings = list(initial_warnings or [])
    warnings.extend(warning for warning in _deferred_optional_warnings(normalized) if warning not in warnings)
    skipped = dict(initial_skipped or {})
    for key, value in _deferred_optional_skips(normalized).items():
        skipped[key] = skipped.get(key, 0) + value

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
        known_game_ids = _ingest_game_log_rows(
            connection,
            normalized.game_log_rows,
            known_match_ids=known_match_ids,
            ingest_run_id=ingest_run_id,
            now=timestamp,
            warnings=warnings,
        )
        if ingest_optional_fact_families:
            _ingest_gameplay_action_entries(
                connection,
                normalized.gameplay_action_entries,
                known_game_ids=known_game_ids,
                ingest_run_id=ingest_run_id,
                now=timestamp,
            )
            _ingest_opponent_card_observations(
                connection,
                normalized.opponent_card_observations,
                known_game_ids=known_game_ids,
                ingest_run_id=ingest_run_id,
                now=timestamp,
                warnings=warnings,
            )
            _ingest_field_evidence_entries(
                connection,
                normalized.field_evidence_entries,
                ingest_run_id=ingest_run_id,
                now=timestamp,
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
) -> set[str]:
    known_game_ids: set[str] = set()
    for index, row in enumerate(game_log_rows):
        match_id = _match_id(row, f"game_log_rows[{index}]")
        if match_id not in known_match_ids:
            raise AnalyticsReplayIngestError(f"game_log_rows[{index}] references unknown match_id: {match_id}")
        game_number = _required_positive_int(row.get("Game Number"), f"game_log_rows[{index}].Game Number")
        game_id = f"{match_id}:g{game_number}"
        known_game_ids.add(game_id)

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
    return known_game_ids


def _ingest_gameplay_action_entries(
    connection: sqlite3.Connection,
    action_entries: tuple[dict[str, object], ...],
    *,
    known_game_ids: set[str],
    ingest_run_id: str,
    now: str,
) -> None:
    for index, entry in enumerate(action_entries):
        normalized = _normalize_gameplay_action_entry(entry, index)
        if normalized["game_id"] not in known_game_ids and not _game_exists(connection, str(normalized["game_id"])):
            raise AnalyticsReplayIngestError(
                f"gameplay_action_entries[{index}] references unknown game parent: {normalized['game_id']}"
            )

        action_id = _gameplay_action_id(normalized)
        source_fact_key = action_id
        _upsert(
            connection,
            "gameplay_actions",
            "gameplay_action_id",
            {
                "gameplay_action_id": action_id,
                "game_id": normalized["game_id"],
                "match_id": normalized["match_id"],
                "game_number": normalized["game_number"],
                "timestamp": normalized["timestamp"],
                "game_state_id": normalized["game_state_id"],
                "turn_number": normalized["turn_number"],
                "action_type": normalized["action_type"],
                "actor_relation": normalized["actor_relation"],
                "from_zone_type": normalized["from_zone_type"],
                "to_zone_type": normalized["to_zone_type"],
                "source_status": "parser_normalized",
                "annotation_context_label": normalized["annotation_context_label"],
                "raw_action_type_labels": normalized["raw_action_type_labels"],
                "annotation_type_labels": normalized["annotation_type_labels"],
                "visible_in_log": normalized["visible_in_log"],
                **_core_columns(
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="gameplay_actions.py",
                    source_fact_key=source_fact_key,
                    finality="reconciled",
                    now=now,
                ),
            },
        )
        _upsert_gameplay_action_provenance(
            connection,
            action_id=action_id,
            index=index,
            fact_field="action_type",
            source_fact_key=source_fact_key,
            ingest_run_id=ingest_run_id,
            now=now,
            event_timestamp=normalized["timestamp"],
            has_game_state_id=normalized["game_state_id"] is not None,
        )
        _upsert_gameplay_action_provenance(
            connection,
            action_id=action_id,
            index=index,
            fact_field="actor_relation",
            source_fact_key=source_fact_key,
            ingest_run_id=ingest_run_id,
            now=now,
            event_timestamp=normalized["timestamp"],
            has_game_state_id=normalized["game_state_id"] is not None,
        )
        for zone_field in ("from_zone_type", "to_zone_type"):
            if normalized[zone_field] is not None:
                _upsert_gameplay_action_provenance(
                    connection,
                    action_id=action_id,
                    index=index,
                    fact_field=zone_field,
                    source_fact_key=source_fact_key,
                    ingest_run_id=ingest_run_id,
                    now=now,
                    event_timestamp=normalized["timestamp"],
                    has_game_state_id=normalized["game_state_id"] is not None,
                )

        for card in _gameplay_action_card_rows(
            entry,
            action_id=action_id,
            game_id=str(normalized["game_id"]),
            action_index=index,
        ):
            _upsert(
                connection,
                "gameplay_action_cards",
                "gameplay_action_card_id",
                {
                    "gameplay_action_card_id": card["gameplay_action_card_id"],
                    "gameplay_action_id": action_id,
                    "game_id": normalized["game_id"],
                    "card_ordinal": card["card_ordinal"],
                    "instance_id": card["instance_id"],
                    "grp_id": card["grp_id"],
                    "observed_grp_id": card["observed_grp_id"],
                    "overlay_grp_id": card["overlay_grp_id"],
                    "object_source_grp_id": card["object_source_grp_id"],
                    "identity_hint_source": card["identity_hint_source"],
                    "card_name": card["card_name"],
                    "display_name": card["display_name"],
                    "name_resolution_status": card["name_resolution_status"],
                    "enrichment_status": card["enrichment_status"],
                    **_core_columns(
                        ingest_run_id=ingest_run_id,
                        source_parser_surface="gameplay_actions.py",
                        source_fact_key=source_fact_key,
                        finality="reconciled",
                        now=now,
                    ),
                },
            )
            if card["grp_id"] is not None:
                _upsert_gameplay_action_card_provenance(
                    connection,
                    card_id=str(card["gameplay_action_card_id"]),
                    fact_field="grp_id",
                    source_payload_prefix=str(card["source_payload_prefix"]),
                    source_fact_key=source_fact_key,
                    ingest_run_id=ingest_run_id,
                    now=now,
                    event_timestamp=normalized["timestamp"],
                    has_game_state_id=normalized["game_state_id"] is not None,
                )
            elif card["instance_id"] is not None:
                _upsert_gameplay_action_card_provenance(
                    connection,
                    card_id=str(card["gameplay_action_card_id"]),
                    fact_field="instance_id",
                    source_payload_prefix=str(card["source_payload_prefix"]),
                    source_fact_key=source_fact_key,
                    ingest_run_id=ingest_run_id,
                    now=now,
                    event_timestamp=normalized["timestamp"],
                    has_game_state_id=normalized["game_state_id"] is not None,
                )


def _normalize_gameplay_action_entry(entry: Mapping[str, object], index: int) -> dict[str, object]:
    context = f"gameplay_action_entries[{index}]"
    match_id = _required_text(entry.get("match_id"), f"{context}.match_id")
    game_number = _required_positive_int(entry.get("game_number"), f"{context}.game_number")
    action_type = _required_text(entry.get("action_type"), f"{context}.action_type")
    actor_relation = _gameplay_actor_relation(entry.get("actor_relation"), f"{context}.actor_relation")
    raw_action_types = _text_list(entry.get("raw_action_types"), f"{context}.raw_action_types")
    annotation_types = _text_list(entry.get("annotation_types"), f"{context}.annotation_types")
    annotation_categories = _text_list(entry.get("annotation_categories"), f"{context}.annotation_categories")
    return {
        "game_id": f"{match_id}:g{game_number}",
        "match_id": match_id,
        "game_number": game_number,
        "timestamp": _optional_text(entry.get("timestamp")),
        "game_state_id": _optional_int(entry.get("game_state_id"), f"{context}.game_state_id"),
        "turn_number": _optional_int(entry.get("turn_number"), f"{context}.turn_number"),
        "action_type": action_type,
        "cast_mode": _optional_text(entry.get("cast_mode")),
        "instance_id": _optional_int(entry.get("instance_id"), f"{context}.instance_id"),
        "grp_id": _optional_int(entry.get("grp_id"), f"{context}.grp_id"),
        "observed_grp_id": _optional_int(entry.get("observed_grp_id"), f"{context}.observed_grp_id"),
        "overlay_grp_id": _optional_int(entry.get("overlay_grp_id"), f"{context}.overlay_grp_id"),
        "object_source_grp_id": _optional_int(
            entry.get("object_source_grp_id"),
            f"{context}.object_source_grp_id",
        ),
        "parent_id": _optional_int(entry.get("parent_id"), f"{context}.parent_id"),
        "identity_hint_source": _optional_text(entry.get("identity_hint_source")),
        "actor_relation": actor_relation,
        "from_zone_type": _optional_text(entry.get("from_zone_type")),
        "to_zone_type": _optional_text(entry.get("to_zone_type")),
        "raw_action_types": raw_action_types,
        "annotation_types": annotation_types,
        "raw_action_type_labels": _stable_text_list(raw_action_types),
        "annotation_type_labels": _stable_text_list(annotation_types),
        "annotation_context_label": _annotation_context_label(annotation_categories),
        "visible_in_log": _optional_bool_int(entry.get("visible_in_log"), f"{context}.visible_in_log"),
    }


def _gameplay_action_id(normalized: Mapping[str, object]) -> str:
    id_payload = {
        "match_id": normalized["match_id"],
        "game_number": normalized["game_number"],
        "game_state_id": normalized["game_state_id"],
        "turn_number": normalized["turn_number"],
        "action_type": normalized["action_type"],
        "cast_mode": normalized["cast_mode"],
        "actor_relation": normalized["actor_relation"],
        "instance_id": normalized["instance_id"],
        "grp_id": normalized["grp_id"],
        "observed_grp_id": normalized["observed_grp_id"],
        "overlay_grp_id": normalized["overlay_grp_id"],
        "object_source_grp_id": normalized["object_source_grp_id"],
        "parent_id": normalized["parent_id"],
        "from_zone_type": normalized["from_zone_type"],
        "to_zone_type": normalized["to_zone_type"],
        "raw_action_types": normalized["raw_action_types"],
        "annotation_types": normalized["annotation_types"],
    }
    digest = hashlib.sha256(_canonical_json(id_payload).encode("utf-8")).hexdigest()
    return f"gameplay_action:{digest}"


def _gameplay_action_card_rows(
    entry: Mapping[str, object],
    *,
    action_id: str,
    game_id: str,
    action_index: int,
) -> list[dict[str, object]]:
    raw_cards = _card_identity_inputs(entry, action_index=action_index)
    rows: list[dict[str, object]] = []
    for fallback_ordinal, (raw_card, source_payload_prefix) in enumerate(raw_cards, start=1):
        context = f"{action_id}.card[{fallback_ordinal}]"
        raw_ordinal = raw_card.get("card_ordinal")
        card_ordinal = (
            fallback_ordinal
            if raw_ordinal in (None, "")
            else _required_positive_int(raw_ordinal, f"{context}.card_ordinal")
        )
        card = {
            "card_ordinal": card_ordinal,
            "instance_id": _optional_int(raw_card.get("instance_id"), f"{context}.instance_id"),
            "grp_id": _optional_int(raw_card.get("grp_id"), f"{context}.grp_id"),
            "observed_grp_id": _optional_int(raw_card.get("observed_grp_id"), f"{context}.observed_grp_id"),
            "overlay_grp_id": _optional_int(raw_card.get("overlay_grp_id"), f"{context}.overlay_grp_id"),
            "object_source_grp_id": _optional_int(
                raw_card.get("object_source_grp_id"),
                f"{context}.object_source_grp_id",
            ),
            "identity_hint_source": _optional_text(raw_card.get("identity_hint_source")),
            "card_name": _optional_text(raw_card.get("card_name")),
            "display_name": _optional_text(raw_card.get("display_name")),
            "name_resolution_status": _optional_text(raw_card.get("resolution_status")),
        }
        if not _has_gameplay_card_identity(card):
            continue
        card["enrichment_status"] = _gameplay_card_enrichment_status(card)
        digest = hashlib.sha256(_canonical_json({"action_id": action_id, "card_ordinal": card_ordinal}).encode("utf-8"))
        rows.append(
            {
                "gameplay_action_card_id": f"gameplay_action_card:{digest.hexdigest()}",
                "gameplay_action_id": action_id,
                "game_id": game_id,
                "source_payload_prefix": source_payload_prefix,
                **card,
            }
        )
    return rows


def _card_identity_inputs(entry: Mapping[str, object], *, action_index: int) -> list[tuple[Mapping[str, object], str]]:
    for field_name in ("associated_cards", "cards", "card_identities"):
        value = entry.get(field_name)
        if value is None:
            continue
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise AnalyticsReplayIngestError(f"{field_name} must be a list of mappings")
        cards: list[tuple[Mapping[str, object], str]] = []
        for index, item in enumerate(value):
            if not isinstance(item, Mapping):
                raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a mapping")
            cards.append((item, f"/gameplay_action_entries/{action_index}/{field_name}/{index}"))
        return cards
    return [(entry, f"/gameplay_action_entries/{action_index}")]


def _has_gameplay_card_identity(card: Mapping[str, object]) -> bool:
    return any(
        card.get(field_name) not in (None, "")
        for field_name in (
            "instance_id",
            "grp_id",
            "observed_grp_id",
            "overlay_grp_id",
            "object_source_grp_id",
            "card_name",
            "display_name",
        )
    )


def _gameplay_card_enrichment_status(card: Mapping[str, object]) -> str | None:
    has_numeric_identity = any(
        card.get(field_name) is not None
        for field_name in (
            "instance_id",
            "grp_id",
            "observed_grp_id",
            "overlay_grp_id",
            "object_source_grp_id",
        )
    )
    has_name = card.get("card_name") is not None or card.get("display_name") is not None
    if has_numeric_identity and has_name:
        return "parser_rendered"
    if has_name:
        return "name_only"
    if has_numeric_identity:
        return "unresolved_id"
    return None


def _upsert_gameplay_action_provenance(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    index: int,
    fact_field: str,
    source_fact_key: str,
    ingest_run_id: str,
    now: str,
    event_timestamp: object,
    has_game_state_id: bool,
) -> None:
    _upsert_fact_provenance(
        connection,
        fact_table="gameplay_actions",
        fact_id=action_id,
        fact_field=fact_field,
        source_parser_surface="gameplay_actions.py",
        source_fact_key=source_fact_key,
        ingest_run_id=ingest_run_id,
        finality="reconciled",
        now=now,
        ledger_entry_id=_GAMEPLAY_ACTION_LEDGER_ENTRY_ID,
        source_event_kind="GameState" if has_game_state_id else None,
        source_event_type=None,
        source_payload_paths=[f"/gameplay_action_entries/{index}/{fact_field}"],
        source_event_timestamp=_optional_text(event_timestamp),
    )


def _upsert_gameplay_action_card_provenance(
    connection: sqlite3.Connection,
    *,
    card_id: str,
    fact_field: str,
    source_payload_prefix: str,
    source_fact_key: str,
    ingest_run_id: str,
    now: str,
    event_timestamp: object,
    has_game_state_id: bool,
) -> None:
    _upsert_fact_provenance(
        connection,
        fact_table="gameplay_action_cards",
        fact_id=card_id,
        fact_field=fact_field,
        source_parser_surface="gameplay_actions.py",
        source_fact_key=source_fact_key,
        ingest_run_id=ingest_run_id,
        finality="reconciled",
        now=now,
        ledger_entry_id=_GAMEPLAY_ACTION_LEDGER_ENTRY_ID,
        source_event_kind="GameState" if has_game_state_id else None,
        source_event_type=None,
        source_payload_paths=[f"{source_payload_prefix}/{fact_field}"],
        source_event_timestamp=_optional_text(event_timestamp),
    )


def _ingest_opponent_card_observations(
    connection: sqlite3.Connection,
    observations: tuple[dict[str, object], ...],
    *,
    known_game_ids: set[str],
    ingest_run_id: str,
    now: str,
    warnings: list[str],
) -> None:
    for index, observation in enumerate(observations):
        normalized = _normalize_opponent_card_observation(observation, index)
        game_id = str(normalized["game_id"])
        if game_id not in known_game_ids and not _game_exists(connection, game_id):
            raise AnalyticsReplayIngestError(
                f"opponent_card_observations[{index}] references unknown game parent: {game_id}"
            )

        explicit_gameplay_action_id = _optional_text(observation.get("gameplay_action_id"))
        gameplay_action_id = _resolve_opponent_observation_gameplay_action_id(
            connection,
            explicit_gameplay_action_id=explicit_gameplay_action_id,
            observation=observation,
            index=index,
        )
        if explicit_gameplay_action_id and gameplay_action_id is None:
            warnings.append(
                f"opponent_card_observations[{index}] gameplay_action_id did not match an ingested action"
            )

        observation_id = _opponent_card_observation_id(normalized)
        source_fact_key = observation_id
        _upsert(
            connection,
            "opponent_card_observations",
            "opponent_card_observation_id",
            {
                "opponent_card_observation_id": observation_id,
                "game_id": normalized["game_id"],
                "match_id": normalized["match_id"],
                "game_number": normalized["game_number"],
                "gameplay_action_id": gameplay_action_id,
                "timestamp": normalized["timestamp"],
                "game_state_id": normalized["game_state_id"],
                "turn_number": normalized["turn_number"],
                "actor_relation": "opponent",
                "actor_seat_id": normalized["actor_seat_id"],
                "local_seat_id": normalized["local_seat_id"],
                "instance_id": normalized["instance_id"],
                "grp_id": normalized["grp_id"],
                "observed_grp_id": normalized["observed_grp_id"],
                "overlay_grp_id": normalized["overlay_grp_id"],
                "object_source_grp_id": normalized["object_source_grp_id"],
                "parent_id": normalized["parent_id"],
                "identity_hint_source": normalized["identity_hint_source"],
                "card_name": normalized["card_name"],
                "display_name": normalized["display_name"],
                "resolution_status": normalized["resolution_status"],
                "name_resolution_source": normalized["name_resolution_source"],
                "action_type": normalized["action_type"],
                "cast_mode": normalized["cast_mode"],
                "source_evidence": normalized["source_evidence"],
                "evidence_status": normalized["evidence_status"],
                "visibility": normalized["visibility"],
                "from_zone_type": normalized["from_zone_type"],
                "to_zone_type": normalized["to_zone_type"],
                "degradation_flags": normalized["degradation_flags_json"],
                "review_required": normalized["review_required"],
                **_observation_core_columns(
                    normalized,
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="opponent_card_observations.py",
                    source_fact_key=source_fact_key,
                    now=now,
                ),
            },
        )

        for fact_field in (
            "visibility",
            "evidence_status",
            "value_source",
            "confidence",
            "review_required",
            "degradation_flags",
            "action_type",
        ):
            _upsert_opponent_observation_provenance(
                connection,
                fact_table="opponent_card_observations",
                fact_id=observation_id,
                fact_field=fact_field,
                index=index,
                source_fact_key=source_fact_key,
                normalized=normalized,
                ingest_run_id=ingest_run_id,
                now=now,
            )

        card = _opponent_observation_card_row(normalized, observation_id=observation_id)
        if card is None:
            continue

        _upsert(
            connection,
            "opponent_card_observation_cards",
            "opponent_card_observation_card_id",
            {
                "opponent_card_observation_card_id": card["opponent_card_observation_card_id"],
                "opponent_card_observation_id": observation_id,
                "game_id": normalized["game_id"],
                "card_ordinal": card["card_ordinal"],
                "grp_id": normalized["grp_id"],
                "observed_grp_id": normalized["observed_grp_id"],
                "overlay_grp_id": normalized["overlay_grp_id"],
                "object_source_grp_id": normalized["object_source_grp_id"],
                "identity_hint_source": normalized["identity_hint_source"],
                "card_name": normalized["card_name"],
                "resolution_status": normalized["resolution_status"],
                "visibility": normalized["visibility"],
                **_observation_core_columns(
                    normalized,
                    ingest_run_id=ingest_run_id,
                    source_parser_surface="opponent_card_observations.py",
                    source_fact_key=source_fact_key,
                    now=now,
                ),
            },
        )
        if normalized["grp_id"] is not None:
            _upsert_opponent_observation_provenance(
                connection,
                fact_table="opponent_card_observation_cards",
                fact_id=str(card["opponent_card_observation_card_id"]),
                fact_field="grp_id",
                index=index,
                source_fact_key=source_fact_key,
                normalized=normalized,
                ingest_run_id=ingest_run_id,
                now=now,
            )
        if normalized["observed_grp_id"] is not None and normalized["observed_grp_id"] != normalized["grp_id"]:
            _upsert_opponent_observation_provenance(
                connection,
                fact_table="opponent_card_observation_cards",
                fact_id=str(card["opponent_card_observation_card_id"]),
                fact_field="observed_grp_id",
                index=index,
                source_fact_key=source_fact_key,
                normalized=normalized,
                ingest_run_id=ingest_run_id,
                now=now,
            )
        if not _has_opponent_observation_numeric_identity(normalized) and normalized["card_name"] is not None:
            _upsert_opponent_observation_provenance(
                connection,
                fact_table="opponent_card_observation_cards",
                fact_id=str(card["opponent_card_observation_card_id"]),
                fact_field="card_name",
                index=index,
                source_fact_key=source_fact_key,
                normalized=normalized,
                ingest_run_id=ingest_run_id,
                now=now,
            )


def _normalize_opponent_card_observation(entry: Mapping[str, object], index: int) -> dict[str, object]:
    context = f"opponent_card_observations[{index}]"
    object_marker = _required_text(entry.get("object"), f"{context}.object")
    if object_marker != OPPONENT_CARD_OBSERVATION_OBJECT:
        raise AnalyticsReplayIngestError(f"{context}.object must be {OPPONENT_CARD_OBSERVATION_OBJECT}")
    schema_version = _required_text(entry.get("schema_version"), f"{context}.schema_version")
    if schema_version != OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION:
        raise AnalyticsReplayIngestError(
            f"{context}.schema_version must be {OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION}"
        )

    match_id = _required_text(entry.get("match_id"), f"{context}.match_id")
    game_number = _required_positive_int(entry.get("game_number"), f"{context}.game_number")
    actor_relation = _required_text(entry.get("actor_relation"), f"{context}.actor_relation")
    if actor_relation != "opponent":
        raise AnalyticsReplayIngestError(f"{context}.actor_relation must be opponent")

    evidence_status = _required_enum(
        entry.get("evidence_status"),
        f"{context}.evidence_status",
        _ALLOWED_OBSERVATION_EVIDENCE_STATUS,
    )
    value_source = _required_enum(
        entry.get("value_source"),
        f"{context}.value_source",
        _ALLOWED_OBSERVATION_VALUE_SOURCES,
    )
    confidence = _required_enum(
        entry.get("confidence"),
        f"{context}.confidence",
        _ALLOWED_OBSERVATION_CONFIDENCE,
    )
    visibility = _required_enum(
        entry.get("visibility"),
        f"{context}.visibility",
        _ALLOWED_OBSERVATION_VISIBILITY,
    )
    degradation_flags = _required_string_list(entry.get("degradation_flags"), f"{context}.degradation_flags")
    review_required = _required_bool_int(entry.get("review_required"), f"{context}.review_required")
    finality = _optional_enum(
        entry.get("finality"),
        f"{context}.finality",
        _ALLOWED_OBSERVATION_FINALITY,
        default="reconciled",
    )
    drift_status = _optional_enum(
        entry.get("drift_status"),
        f"{context}.drift_status",
        _ALLOWED_OBSERVATION_DRIFT_STATUS,
        default=_default_observation_drift_status(
            evidence_status=evidence_status,
            degradation_flags=degradation_flags,
            review_required=bool(review_required),
        ),
    )
    return {
        "game_id": f"{match_id}:g{game_number}",
        "match_id": match_id,
        "game_number": game_number,
        "timestamp": _optional_text(entry.get("timestamp")),
        "game_state_id": _optional_int(entry.get("game_state_id"), f"{context}.game_state_id"),
        "turn_number": _optional_int(entry.get("turn_number"), f"{context}.turn_number"),
        "actor_seat_id": _optional_int(entry.get("actor_seat_id"), f"{context}.actor_seat_id"),
        "local_seat_id": _optional_int(entry.get("local_seat_id"), f"{context}.local_seat_id"),
        "instance_id": _optional_int(entry.get("instance_id"), f"{context}.instance_id"),
        "grp_id": _optional_int(entry.get("grp_id"), f"{context}.grp_id"),
        "observed_grp_id": _optional_int(entry.get("observed_grp_id"), f"{context}.observed_grp_id"),
        "overlay_grp_id": _optional_int(entry.get("overlay_grp_id"), f"{context}.overlay_grp_id"),
        "object_source_grp_id": _optional_int(
            entry.get("object_source_grp_id"),
            f"{context}.object_source_grp_id",
        ),
        "parent_id": _optional_int(entry.get("parent_id"), f"{context}.parent_id"),
        "identity_hint_source": _optional_text(entry.get("identity_hint_source")),
        "card_name": _optional_text(entry.get("card_name")),
        "display_name": _optional_text(entry.get("display_name")),
        "resolution_status": _optional_text(entry.get("resolution_status")),
        "name_resolution_source": _optional_text(entry.get("name_resolution_source")),
        "action_type": _required_text(entry.get("action_type"), f"{context}.action_type"),
        "cast_mode": _optional_text(entry.get("cast_mode")),
        "source_evidence": _required_text(entry.get("source_evidence"), f"{context}.source_evidence"),
        "evidence_status": evidence_status,
        "visibility": visibility,
        "from_zone_type": _optional_text(entry.get("from_zone_type")),
        "to_zone_type": _optional_text(entry.get("to_zone_type")),
        "degradation_flags": degradation_flags,
        "degradation_flags_json": _stable_text_list(degradation_flags),
        "review_required": review_required,
        "value_source": value_source,
        "confidence": confidence,
        "finality": finality,
        "drift_status": drift_status,
        "degraded_reason": _observation_degraded_reason(
            evidence_status=evidence_status,
            degradation_flags=degradation_flags,
        ),
    }


def _opponent_card_observation_id(normalized: Mapping[str, object]) -> str:
    id_payload = {
        "match_id": normalized["match_id"],
        "game_number": normalized["game_number"],
        "game_state_id": normalized["game_state_id"],
        "turn_number": normalized["turn_number"],
        "actor_relation": "opponent",
        "actor_seat_id": normalized["actor_seat_id"],
        "local_seat_id": normalized["local_seat_id"],
        "instance_id": normalized["instance_id"],
        "grp_id": normalized["grp_id"],
        "observed_grp_id": normalized["observed_grp_id"],
        "overlay_grp_id": normalized["overlay_grp_id"],
        "object_source_grp_id": normalized["object_source_grp_id"],
        "parent_id": normalized["parent_id"],
        "action_type": normalized["action_type"],
        "cast_mode": normalized["cast_mode"],
        "source_evidence": normalized["source_evidence"],
        "visibility": normalized["visibility"],
        "from_zone_type": normalized["from_zone_type"],
        "to_zone_type": normalized["to_zone_type"],
    }
    digest = hashlib.sha256(_canonical_json(id_payload).encode("utf-8")).hexdigest()
    return f"opponent_card_observation:{digest}"


def _resolve_opponent_observation_gameplay_action_id(
    connection: sqlite3.Connection,
    *,
    explicit_gameplay_action_id: str | None,
    observation: Mapping[str, object],
    index: int,
) -> str | None:
    if explicit_gameplay_action_id and _gameplay_action_exists(connection, explicit_gameplay_action_id):
        return explicit_gameplay_action_id

    candidate = _gameplay_action_id(_normalize_gameplay_action_entry(observation, index))
    if _gameplay_action_exists(connection, candidate):
        return candidate
    return None


def _opponent_observation_card_row(
    normalized: Mapping[str, object],
    *,
    observation_id: str,
) -> dict[str, object] | None:
    if not _has_opponent_observation_card_identity(normalized):
        return None
    card_ordinal = 1
    digest = hashlib.sha256(
        _canonical_json({"observation_id": observation_id, "card_ordinal": card_ordinal}).encode("utf-8")
    )
    return {
        "opponent_card_observation_card_id": f"opponent_card_observation_card:{digest.hexdigest()}",
        "card_ordinal": card_ordinal,
    }


def _has_opponent_observation_card_identity(normalized: Mapping[str, object]) -> bool:
    return any(
        normalized.get(field_name) is not None
        for field_name in (
            "grp_id",
            "observed_grp_id",
            "overlay_grp_id",
            "object_source_grp_id",
            "identity_hint_source",
            "card_name",
        )
    )


def _has_opponent_observation_numeric_identity(normalized: Mapping[str, object]) -> bool:
    return any(
        normalized.get(field_name) is not None
        for field_name in ("grp_id", "observed_grp_id", "overlay_grp_id", "object_source_grp_id")
    )


def _observation_core_columns(
    normalized: Mapping[str, object],
    *,
    ingest_run_id: str,
    source_parser_surface: str,
    source_fact_key: str,
    now: str,
) -> dict[str, object]:
    values = _core_columns(
        ingest_run_id=ingest_run_id,
        source_parser_surface=source_parser_surface,
        source_fact_key=source_fact_key,
        finality=str(normalized["finality"]),
        now=now,
    )
    values["value_source"] = normalized["value_source"]
    values["confidence"] = normalized["confidence"]
    values["drift_status"] = normalized["drift_status"]
    return values


def _upsert_opponent_observation_provenance(
    connection: sqlite3.Connection,
    *,
    fact_table: str,
    fact_id: str,
    fact_field: str,
    index: int,
    source_fact_key: str,
    normalized: Mapping[str, object],
    ingest_run_id: str,
    now: str,
) -> None:
    _upsert_fact_provenance(
        connection,
        fact_table=fact_table,
        fact_id=fact_id,
        fact_field=fact_field,
        source_parser_surface="opponent_card_observations.py",
        source_fact_key=source_fact_key,
        ingest_run_id=ingest_run_id,
        finality=str(normalized["finality"]),
        now=now,
        ledger_entry_id=_OPPONENT_CARD_OBSERVATION_LEDGER_ENTRY_ID,
        source_event_kind="GameState" if normalized["game_state_id"] is not None else None,
        source_event_type=None,
        source_payload_paths=[f"/opponent_card_observations/{index}/{fact_field}"],
        source_event_timestamp=_optional_text(normalized["timestamp"]),
        value_source=str(normalized["value_source"]),
        confidence=str(normalized["confidence"]),
        drift_flags=list(normalized["degradation_flags"]),  # type: ignore[arg-type]
        degraded_reason=_optional_text(normalized["degraded_reason"]),
        review_required=int(normalized["review_required"]),
    )


def _gameplay_action_exists(connection: sqlite3.Connection, gameplay_action_id: str) -> bool:
    row = connection.execute(
        "SELECT 1 FROM gameplay_actions WHERE gameplay_action_id = ? LIMIT 1",
        (gameplay_action_id,),
    ).fetchone()
    return row is not None


def _ingest_field_evidence_entries(
    connection: sqlite3.Connection,
    field_evidence_entries: tuple[dict[str, object], ...],
    *,
    ingest_run_id: str,
    now: str,
) -> None:
    for index, entry in enumerate(field_evidence_entries):
        normalized = _normalize_field_evidence_entry(entry, index)
        _require_target_fact_row(
            connection,
            fact_table=str(normalized["fact_table"]),
            fact_id=str(normalized["fact_id"]),
            context=f"field_evidence_entries[{index}]",
        )
        _upsert_fact_provenance(
            connection,
            fact_table=str(normalized["fact_table"]),
            fact_id=str(normalized["fact_id"]),
            fact_field=str(normalized["fact_field"]),
            source_parser_surface=str(normalized["source_parser_surface"]),
            source_fact_key=str(normalized["source_fact_key"]),
            ingest_run_id=ingest_run_id,
            finality=str(normalized["finality"]),
            now=now,
            fact_provenance_id=str(normalized["fact_provenance_id"]),
            ledger_entry_id=str(normalized["entry_id"]),
            source_event_kind=_optional_text(normalized["source_event_kind"]),
            source_event_type=_optional_text(normalized["source_event_type"]),
            source_payload_paths=normalized["source_payload_paths"],  # type: ignore[arg-type]
            source_event_timestamp=_optional_text(normalized["source_event_timestamp"]),
            value_source=str(normalized["value_source"]),
            confidence=str(normalized["confidence"]),
            drift_flags=normalized["drift_flags"],  # type: ignore[arg-type]
            invariant_status=str(normalized["invariant_status"]),
            degraded_reason=_optional_text(normalized["degraded_reason"]),
            review_required=int(normalized["review_required"]),
        )


def _normalize_field_evidence_entry(entry: Mapping[str, object], index: int) -> dict[str, object]:
    context = f"field_evidence_entries[{index}]"
    canonical = {
        field_name: entry[field_name]
        for field_name in evidence_ledger.REQUIRED_FIELD_EVIDENCE_FIELDS
        if field_name in entry
    }
    validation_errors = [
        error
        for error in evidence_ledger.validate_field_evidence(canonical)
        if not error.startswith("privacy:absolute_path:field_evidence.source_payload_paths[")
    ]
    if validation_errors:
        raise AnalyticsReplayIngestError(f"{context} invalid field evidence: {', '.join(validation_errors)}")

    fact_table = _required_field_evidence_label(entry.get("fact_table"), f"{context}.fact_table")
    if fact_table not in _FIELD_EVIDENCE_FACT_TABLE_PRIMARY_KEYS:
        raise AnalyticsReplayIngestError(f"{context}.fact_table must be an existing analytics fact table")

    source_payload_paths = _required_safe_string_list(
        entry.get("source_payload_paths"),
        f"{context}.source_payload_paths",
        allow_json_pointers=True,
    )
    drift_flags = _required_safe_string_list(
        entry.get("drift_flags"),
        f"{context}.drift_flags",
        allow_json_pointers=False,
    )
    normalized = {
        "entry_id": _required_field_evidence_label(entry.get("entry_id"), f"{context}.entry_id"),
        "fact_table": fact_table,
        "fact_id": _required_field_evidence_label(entry.get("fact_id"), f"{context}.fact_id"),
        "fact_field": _required_field_evidence_label(entry.get("fact_field"), f"{context}.fact_field"),
        "source_parser_surface": _required_field_evidence_label(
            entry.get("source_parser_surface"),
            f"{context}.source_parser_surface",
        ),
        "source_fact_key": _required_field_evidence_label(
            entry.get("source_fact_key"),
            f"{context}.source_fact_key",
        ),
        "source_event_kind": _optional_field_evidence_label(
            entry.get("source_event_kind"),
            f"{context}.source_event_kind",
        ),
        "source_event_type": _optional_field_evidence_label(
            entry.get("source_event_type"),
            f"{context}.source_event_type",
        ),
        "source_payload_paths": source_payload_paths,
        "source_event_timestamp": _optional_field_evidence_label(
            entry.get("source_event_timestamp"),
            f"{context}.source_event_timestamp",
        ),
        "value_source": str(entry["value_source"]),
        "confidence": str(entry["confidence"]),
        "finality": str(entry["finality"]),
        "drift_flags": drift_flags,
        "invariant_status": str(entry["invariant_status"]),
        "degraded_reason": _optional_field_evidence_label(
            entry.get("degraded_reason"),
            f"{context}.degraded_reason",
        ),
        "review_required": int(bool(entry["review_required"])),
    }
    normalized["fact_provenance_id"] = _field_evidence_provenance_id(normalized)
    return normalized


def _field_evidence_provenance_id(normalized: Mapping[str, object]) -> str:
    id_payload = {
        "fact_table": normalized["fact_table"],
        "fact_id": normalized["fact_id"],
        "fact_field": normalized["fact_field"],
        "entry_id": normalized["entry_id"],
        "source_parser_surface": normalized["source_parser_surface"],
        "source_fact_key": normalized["source_fact_key"],
        "source_event_kind": normalized["source_event_kind"],
        "source_event_type": normalized["source_event_type"],
        "source_payload_paths": normalized["source_payload_paths"],
    }
    digest = hashlib.sha256(_canonical_json(id_payload).encode("utf-8")).hexdigest()
    return f"field_evidence:{digest}"


def _require_target_fact_row(
    connection: sqlite3.Connection,
    *,
    fact_table: str,
    fact_id: str,
    context: str,
) -> None:
    primary_key = _FIELD_EVIDENCE_FACT_TABLE_PRIMARY_KEYS[fact_table]
    row = connection.execute(
        f"SELECT 1 FROM {fact_table} WHERE {primary_key} = ? LIMIT 1",
        (fact_id,),
    ).fetchone()
    if row is None:
        raise AnalyticsReplayIngestError(f"{context} references missing target fact row: {fact_table}.{fact_id}")


def _required_field_evidence_label(value: object, field_name: str) -> str:
    text = _required_text(value, field_name)
    _validate_safe_field_evidence_label(text, field_name, allow_json_pointer=False)
    return text


def _optional_field_evidence_label(value: object, field_name: str) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    _validate_safe_field_evidence_label(text, field_name, allow_json_pointer=False)
    return text


def _required_safe_string_list(
    value: object,
    field_name: str,
    *,
    allow_json_pointers: bool,
) -> list[str]:
    if not isinstance(value, list):
        raise AnalyticsReplayIngestError(f"{field_name} must be a list of strings")
    values: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a string")
        text = item.strip()
        if not text:
            raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a non-empty safe label")
        _validate_safe_field_evidence_label(
            text,
            f"{field_name}[{index}]",
            allow_json_pointer=allow_json_pointers,
        )
        values.append(text)
    return values


def _validate_safe_field_evidence_label(value: str, field_name: str, *, allow_json_pointer: bool) -> None:
    normalized = value.lower().replace("\\", "/")
    if (
        any(normalized == root or normalized.startswith(f"{root}/") for root in _LOCAL_ABSOLUTE_PATH_ROOTS)
        or _SLASH_PREFIXED_DRIVE_PATH_RE.match(normalized) is not None
    ):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe field-evidence label")
    private_shape = _PRIVATE_LABEL_RE.search(value) is not None
    allowed_json_pointer = allow_json_pointer and value.startswith("/") and not normalized.startswith("//")
    if (private_shape and not allowed_json_pointer) or normalized.startswith("//"):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe field-evidence label")
    if not allow_json_pointer and value.startswith("/"):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe field-evidence label")
    if not _SAFE_FIELD_EVIDENCE_LABEL_RE.fullmatch(value):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe field-evidence label")
    marker_text = normalized.replace("-", "_").replace(" ", "")
    if any(marker in marker_text for marker in _PRIVATE_FIELD_EVIDENCE_MARKERS):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe field-evidence label")


def _required_enum(value: object, field_name: str, allowed_values: set[str]) -> str:
    text = _required_text(value, field_name)
    if text not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        raise AnalyticsReplayIngestError(f"{field_name} must be one of {allowed}")
    return text


def _optional_enum(value: object, field_name: str, allowed_values: set[str], *, default: str) -> str:
    text = _optional_text(value)
    if text is None:
        return default
    if text not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        raise AnalyticsReplayIngestError(f"{field_name} must be one of {allowed}")
    return text


def _required_bool_int(value: object, field_name: str) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int) and value in {0, 1}:
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1"}:
            return 1
        if normalized in {"false", "no", "0"}:
            return 0
    raise AnalyticsReplayIngestError(f"{field_name} must be a boolean or safe boolean-like value")


def _required_string_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise AnalyticsReplayIngestError(f"{field_name} must be a list of strings")
    values: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a string")
        text = item.strip()
        if not text:
            raise AnalyticsReplayIngestError(f"{field_name}[{index}] must be a non-empty safe label")
        _validate_safe_degradation_flag(text, f"{field_name}[{index}]")
        values.append(text)
    return values


def _validate_safe_degradation_flag(value: str, field_name: str) -> None:
    marker_text = value.lower().replace("-", "_").replace(" ", "")
    if (
        _PRIVATE_LABEL_RE.search(value)
        or not _SAFE_DEGRADATION_FLAG_RE.fullmatch(value)
        or any(marker in marker_text for marker in _PRIVATE_DEGRADATION_MARKERS)
    ):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe degradation_flags label")


def _default_observation_drift_status(
    *,
    evidence_status: str,
    degradation_flags: Sequence[str],
    review_required: bool,
) -> str:
    if evidence_status == "conflict":
        return "conflict"
    if evidence_status == "degraded" or degradation_flags or review_required:
        return "degraded"
    return "not_checked"


def _observation_degraded_reason(
    *,
    evidence_status: str,
    degradation_flags: Sequence[str],
) -> str | None:
    if evidence_status == "conflict":
        return "conflict"
    if evidence_status == "degraded" and not degradation_flags:
        return "degraded"
    if degradation_flags:
        return ";".join(degradation_flags)
    return None


def _game_exists(connection: sqlite3.Connection, game_id: str) -> bool:
    row = connection.execute("SELECT 1 FROM games WHERE game_id = ? LIMIT 1", (game_id,)).fetchone()
    return row is not None


def _gameplay_actor_relation(value: object, field_name: str) -> str:
    text = _optional_text(value)
    if text is None:
        return ""
    normalized = text.lower()
    if normalized not in _ALLOWED_GAMEPLAY_ACTOR_RELATIONS:
        raise AnalyticsReplayIngestError(
            f"{field_name} must be one of local, opponent, unknown, or blank"
        )
    return normalized


def _optional_bool_int(value: object, field_name: str) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int) and value in {0, 1}:
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes"}:
            return 1
        if normalized in {"false", "no"}:
            return 0
    raise AnalyticsReplayIngestError(f"{field_name} must be 1, 0, true, false, or blank")


def _text_list(value: object, field_name: str) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [text for item in value if (text := str(item or "").strip())]
    raise AnalyticsReplayIngestError(f"{field_name} must be a list of labels")


def _stable_text_list(values: Sequence[str]) -> str:
    return json.dumps(list(values), separators=(",", ":"), ensure_ascii=False)


def _annotation_context_label(annotation_categories: Sequence[str]) -> str | None:
    if not annotation_categories:
        return None
    return ";".join(annotation_categories)


def _canonical_json(value: object) -> str:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


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
    ledger_entry_id: str | None = None,
    source_event_kind: str | None = None,
    source_event_type: str | None = None,
    source_payload_paths: Sequence[str] | None = None,
    source_event_timestamp: str | None = None,
    value_source: str = "derived",
    confidence: str = "unknown",
    drift_flags: Sequence[str] | None = None,
    invariant_status: str | None = None,
    degraded_reason: str | None = None,
    review_required: int = 0,
    fact_provenance_id: str | None = None,
) -> None:
    payload_paths = list(source_payload_paths) if source_payload_paths is not None else [f"/{source_fact_key}"]
    drift_flag_values = list(drift_flags) if drift_flags is not None else []
    provenance_id = fact_provenance_id or f"{fact_table}:{fact_id}:{fact_field}:provenance"
    _upsert(
        connection,
        "fact_provenance",
        "fact_provenance_id",
        {
            "fact_provenance_id": provenance_id,
            "fact_table": fact_table,
            "fact_id": fact_id,
            "fact_field": fact_field,
            "ledger_entry_id": ledger_entry_id,
            "source_parser_surface": source_parser_surface,
            "source_fact_key": source_fact_key,
            "source_event_kind": source_event_kind,
            "source_event_type": source_event_type,
            "source_payload_paths": json.dumps(payload_paths, separators=(",", ":")),
            "source_event_timestamp": source_event_timestamp,
            "value_source": value_source,
            "confidence": confidence,
            "finality": finality,
            "drift_flags": json.dumps(drift_flag_values, separators=(",", ":")),
            "invariant_status": invariant_status,
            "degraded_reason": degraded_reason,
            "review_required": review_required,
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


def _validate_safe_source_artifact_label(source_artifact_label: str) -> None:
    if _PRIVATE_LABEL_RE.search(source_artifact_label):
        raise AnalyticsReplayIngestError("source_artifact_label must be a safe label, not a local path or URL")


def _required_live_safe_label(value: object, field_name: str) -> str:
    text = _required_text(value, field_name)
    normalized = text.lower().replace("\\", "/")
    if _PRIVATE_LABEL_RE.search(text) or normalized.startswith("//") or "/" in normalized:
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe live parser label")
    marker_text = normalized.replace("-", "_").replace(" ", "")
    if any(marker in marker_text for marker in _PRIVATE_FIELD_EVIDENCE_MARKERS):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe live parser label")
    if not _SAFE_DEGRADATION_FLAG_RE.fullmatch(text):
        raise AnalyticsReplayIngestError(f"{field_name} must be a safe live parser label")
    return text


def _reject_live_forbidden_payload_fields(payload: Mapping[str, object]) -> None:
    for field_name in sorted(_LIVE_FORBIDDEN_PAYLOAD_FIELDS):
        if field_name in payload:
            raise AnalyticsReplayIngestError(f"{field_name} is not allowed in live parser-owned fact payloads")


def _reject_live_unsafe_row_payloads(rows: Sequence[Mapping[str, object]], *, row_group: str) -> None:
    for row_index, row in enumerate(rows):
        _reject_live_unsafe_row_value(row, f"{row_group}[{row_index}]")


def _reject_live_unsafe_row_value(value: object, context: str) -> None:
    if isinstance(value, Mapping):
        for field_name, field_value in value.items():
            if not isinstance(field_name, str):
                raise AnalyticsReplayIngestError(f"{context} field names must be strings")
            field_context = f"{context}.{field_name}"
            if _is_live_forbidden_row_field_name(field_name):
                raise AnalyticsReplayIngestError(
                    f"{field_context} is not allowed in live parser-owned fact payloads"
                )
            _reject_live_unsafe_row_value(field_value, field_context)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            _reject_live_unsafe_row_value(item, f"{context}[{index}]")
        return
    if isinstance(value, str) and _is_live_private_row_value(value):
        raise AnalyticsReplayIngestError(f"{context} must be a safe live parser row value")


def _is_live_forbidden_row_field_name(field_name: str) -> bool:
    normalized = field_name.lower().replace("-", "_").replace(" ", "_")
    marker_text = normalized.replace("__", "_")
    return normalized in _LIVE_FORBIDDEN_PAYLOAD_FIELDS or any(
        marker in marker_text for marker in _LIVE_PRIVATE_ROW_FIELD_MARKERS
    )


def _is_live_private_row_value(value: str) -> bool:
    text = value.strip()
    if not text:
        return False
    normalized = text.lower().replace("\\", "/")
    marker_text = normalized.replace("-", "_").replace(" ", "")
    if (
        _PRIVATE_LABEL_RE.search(text)
        or normalized.startswith("//")
        or any(normalized == root or normalized.startswith(f"{root}/") for root in _LOCAL_ABSOLUTE_PATH_ROOTS)
        or _SLASH_PREFIXED_DRIVE_PATH_RE.match(normalized) is not None
        or "bearer " in normalized
        or any(marker in marker_text for marker in _LIVE_PRIVATE_ROW_VALUE_MARKERS)
    ):
        return True
    return any(
        marker in normalized
        for marker in (
            "secret=",
            "secret:",
            "password=",
            "password:",
            "token=",
            "token:",
        )
    )


def _require_live_final_rows(
    rows: Sequence[Mapping[str, object]],
    *,
    row_group: str,
    default_finality: str,
) -> None:
    for index, row in enumerate(rows):
        finality = _live_row_finality(row, default_finality=default_finality)
        if finality not in _LIVE_ALLOWED_FINALITIES:
            allowed = ", ".join(sorted(_LIVE_ALLOWED_FINALITIES))
            raise AnalyticsReplayIngestError(f"{row_group}[{index}] finality must be one of {allowed}")


def _live_row_finality(row: Mapping[str, object], *, default_finality: str) -> str:
    for field_name in ("finality", "Finality", "finality_status", "sync_finality", "MTGA Sync Status"):
        text = _optional_text(row.get(field_name))
        if text:
            normalized = text.lower()
            if normalized == "live":
                return "live"
            if normalized == "provisional":
                return "provisional"
            if normalized == "final":
                return "final"
            if normalized == "reconciled":
                return "reconciled"
            return normalized
    return default_finality


def _live_payload_warnings(payload: Mapping[str, object]) -> list[str]:
    warnings: list[str] = []
    for field_name, warning in _LIVE_DEFERRED_PAYLOAD_FIELDS.items():
        if _payload_field_has_entries(payload.get(field_name)) and warning not in warnings:
            warnings.append(warning)
    payload_warnings = _text_list(payload.get("warnings"), "warnings")
    for warning in payload_warnings:
        if not _SAFE_DEGRADATION_FLAG_RE.fullmatch(warning):
            raise AnalyticsReplayIngestError("warnings must contain safe labels")
        if warning not in warnings:
            warnings.append(warning)
    return warnings


def _live_payload_skips(payload: Mapping[str, object]) -> dict[str, int]:
    skipped: dict[str, int] = {}
    for field_name in _LIVE_DEFERRED_PAYLOAD_FIELDS:
        value = payload.get(field_name)
        if _payload_field_has_entries(value):
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                skipped[field_name] = len(value)
            else:
                skipped[field_name] = 1
    return skipped


def _payload_field_has_entries(value: object) -> bool:
    if value in (None, "", (), [], {}):
        return False
    return True


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
    _ = replay
    return []


def _deferred_optional_skips(replay: ParserNormalizedReplayInput) -> dict[str, int]:
    _ = replay
    return {}


def _jsonable(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_jsonable(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)
