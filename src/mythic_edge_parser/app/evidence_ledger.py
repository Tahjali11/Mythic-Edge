from __future__ import annotations

import copy
import re
from collections.abc import Mapping, Sequence
from typing import Any

LEDGER_OBJECT = "mythic_edge_player_log_evidence_ledger"
LEDGER_SCHEMA_VERSION = "player_log_evidence_ledger_schema.v1"
LEDGER_VERSION = "player_log_evidence_ledger.v1"

FIELD_EVIDENCE_OBJECT = "mythic_edge_player_log_field_evidence"
FIELD_EVIDENCE_SCHEMA_VERSION = "player_log_field_evidence.v1"

VALUE_SOURCES = (
    "observed",
    "derived",
    "inferred",
    "unknown",
    "conflict",
    "legacy_enriched",
)

CONFIDENCE_LEVELS = (
    "high",
    "medium",
    "low",
    "unknown",
)

FINALITY_LABELS = (
    "live",
    "provisional",
    "final",
    "reconciled",
)

INVARIANT_STATUSES = (
    "passed",
    "failed",
    "not_applicable",
    "not_checked",
    "degraded",
)

DRIFT_FLAGS = (
    "missing_expected_event_family",
    "missing_expected_payload_path",
    "changed_signal_type",
    "new_unknown_event_family",
    "new_unknown_payload_path",
    "fallback_used",
    "weak_fallback_used",
    "conflicting_evidence",
    "invariant_failed",
    "schema_snapshot_missing",
    "fixture_gap",
    "parser_exception",
    "transport_failure",
    "workbook_drift",
    "deployment_drift",
    "sensitive_evidence_redacted",
)

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/128"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/11"
BRANCH_TARGET = "codex/parser-reliability-intelligence"
RELATED_ADRS = ("docs/decisions/ADR-0003-player-log-drift-policy.md",)

FAMILY_STATUSES = ("seeded_sample", "registered_future")
EVIDENCE_PRIVACY_CLASSES = ("path_only_no_values",)
ALLOWED_TYPE_LABELS = ("str", "int", "bool", "dict", "list", "str-int", "unknown")
ENTRY_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")
ABSOLUTE_PATH_RE = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\)")
FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,})",
    re.IGNORECASE,
)

REQUIRED_LEDGER_FIELDS = (
    "object",
    "schema_version",
    "ledger_version",
    "source_issue",
    "parent_issue",
    "related_adrs",
    "branch_target",
    "privacy",
    "vocabulary",
    "output_families",
    "entries",
)

REQUIRED_OUTPUT_FAMILY_FIELDS = (
    "tier",
    "output_family",
    "status",
    "description",
    "seed_fields",
    "future_fields",
    "owner_modules",
    "notes",
)

REQUIRED_ENTRY_FIELDS = (
    "entry_id",
    "tier",
    "output_family",
    "output_field",
    "display_name",
    "parser_owner",
    "model_surface",
    "downstream_surfaces",
    "parser_managed_truth",
    "coverage_status",
    "direct_evidence",
    "fallback_evidence",
    "value_source_policy",
    "confidence_policy",
    "finality_policy",
    "invariant_checks",
    "degradation_behavior",
    "drift_flags",
    "recommended_review_modules",
    "tests",
    "fixture_refs",
    "notes",
)

REQUIRED_EVIDENCE_FIELDS = (
    "signal_id",
    "parser_event_kind",
    "parser_event_type",
    "raw_event_family",
    "raw_message_type",
    "normalized_payload_path",
    "raw_payload_path",
    "required_for_final",
    "value_source_when_used",
    "confidence_when_used",
    "finality_when_used",
    "allowed_types",
    "missing_behavior",
    "privacy_class",
)

REQUIRED_FIELD_EVIDENCE_FIELDS = (
    "object",
    "schema_version",
    "ledger_version",
    "entry_id",
    "output_family",
    "output_field",
    "value_source",
    "confidence",
    "finality",
    "source_event_kind",
    "source_event_type",
    "source_payload_paths",
    "source_event_timestamp",
    "drift_flags",
    "invariant_status",
    "degraded_reason",
    "review_required",
)

_OUTPUT_FAMILIES: tuple[dict[str, Any], ...] = (
    {
        "tier": 1,
        "output_family": "match_identity_and_lifecycle",
        "status": "seeded_sample",
        "description": "Match identity and lifecycle outputs owned by parser state.",
        "seed_fields": [
            "match_id",
            "player_team",
            "opponent_team",
            "local_system_seat_id",
            "participant_team_mapping",
            "match_started_at",
            "match_finished_at",
            "match_winner_team",
            "match_result",
            "match_sync_status",
            "games_won",
            "games_lost",
            "total_games",
            "match_win_flag",
            "game_win_rate",
        ],
        "future_fields": [],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ],
        "notes": [
            "Issue #128 match_id anchor remains preserved.",
            "Issue #130 maps Tier 1 match lifecycle, result, and sync-status fields.",
            "Issue #132 maps Tier 1 game-derived aggregate fields.",
            "Issue #137 maps participant and player-team dependency provenance.",
            "Participant entries support prior #130, #132, and #134 player-relative fields.",
        ],
    },
    {
        "tier": 2,
        "output_family": "queue_format_rank_event_context",
        "status": "registered_future",
        "description": "Queue, format, rank, and event-context parser outputs.",
        "seed_fields": [],
        "future_fields": ["event_id", "super_format", "constructed_rank", "queue_type"],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/event_identity.py",
        ],
        "notes": ["Registered for later field-level provenance mapping."],
    },
    {
        "tier": 3,
        "output_family": "game_level_facts",
        "status": "seeded_sample",
        "description": "Game result, play/draw, mulligan, turn, and opening-hand parser outputs.",
        "seed_fields": [
            "game_number",
            "game1_winner_team",
            "game2_winner_team",
            "game3_winner_team",
            "game1_result",
            "game2_result",
            "game3_result",
            "game1_starting_player",
            "game2_starting_player",
            "game3_starting_player",
            "game1_play_draw",
            "game2_play_draw",
            "game3_play_draw",
        ],
        "future_fields": [
            "mulligans",
            "turn_count",
            "opening_hand",
            "game_timing",
            "game_duration",
            "pre_postboard",
            "sideboarding",
            "deck_state",
        ],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ],
        "notes": [
            "Issue #134 maps a seeded game-result provenance slice only.",
            "Game-level winners come from game-scope evidence; match-scope results are not promoted.",
            "Issue #139 maps starting-player and play/draw provenance using #137 participant "
            "provenance and #134 game-result dependencies.",
            "Mulligan, turn-count, opening-hand, timing, duration, sideboarding, "
            "and deck-state provenance remain deferred.",
        ],
    },
    {
        "tier": 4,
        "output_family": "sideboarding_and_deck_state",
        "status": "registered_future",
        "description": "Sideboarding and submitted-deck parser outputs.",
        "seed_fields": [],
        "future_fields": ["sideboarding_entered", "submit_deck_seen", "submitted_deck_cards"],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/gameplay_actions.py",
        ],
        "notes": ["Registered for later field-level provenance mapping."],
    },
    {
        "tier": 5,
        "output_family": "card_identity_and_gameplay_actions",
        "status": "registered_future",
        "description": "Card identity, gameplay-action, and visible-card parser outputs.",
        "seed_fields": [],
        "future_fields": ["grp_id", "gameplay_action", "opponent_card_observation"],
        "owner_modules": [
            "src/mythic_edge_parser/app/gameplay_actions.py",
            "src/mythic_edge_parser/app/opponent_card_observations.py",
        ],
        "notes": ["Registered for later field-level provenance mapping."],
    },
    {
        "tier": 6,
        "output_family": "runtime_health_and_drift_detection",
        "status": "registered_future",
        "description": "Parser diagnostics, drift, and runtime-health report outputs.",
        "seed_fields": [],
        "future_fields": ["diagnostics_status", "unknown_entry_count", "truncation_count"],
        "owner_modules": [
            "src/mythic_edge_parser/app/log_drift_sensor.py",
            "src/mythic_edge_parser/app/parser_diagnostics.py",
        ],
        "notes": ["Registered for later field-level provenance mapping."],
    },
    {
        "tier": 7,
        "output_family": "derived_analytics_outputs",
        "status": "registered_future",
        "description": "Derived parser-adjacent analytics outputs that must remain downstream consumers.",
        "seed_fields": [],
        "future_fields": ["card_performance", "feature_equity_counts"],
        "owner_modules": [
            "src/mythic_edge_parser/app/card_performance.py",
            "src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py",
        ],
        "notes": ["Registered only as future consumer metadata; this family is not parser truth."],
    },
)

_MATCH_ID_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_identity.match_id",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_id",
    "display_name": "MTGA Match ID",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.to_match_log_row",
    "downstream_surfaces": ["MatchLogRow", "GameLogRow", "match_history"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "match_state.match_id",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_started",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "payload.match_id",
            "raw_payload_path": "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.matchId",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["str"],
            "missing_behavior": "mark match_id unknown and block final match-level rows",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "game_state.identity.match_id",
            "parser_event_kind": "GameState",
            "parser_event_type": "game_state_message",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.identity.match_id",
            "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.matchID",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["str"],
            "missing_behavior": "mark match_id unknown and block final match-level rows",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "game_result.identity.match_id",
            "parser_event_kind": "GameResult",
            "parser_event_type": "game_result",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.identity.match_id",
            "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.matchID",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["str"],
            "missing_behavior": "mark match_id unknown and block final match-level rows",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_context.current_match_id",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "state_context.current_match_id",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["str"],
            "missing_behavior": "mark match_id unknown and block final match-level rows",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
        "historical": "legacy_enriched",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "stable_match_id_required",
        "final_match_row_requires_match_id",
        "game_rows_must_not_attach_to_unknown_match_id",
    ],
    "degradation_behavior": [
        "missing direct and fallback match identity yields value_source=unknown",
        "missing match identity yields confidence=unknown",
        "future field-evidence results must mark review_required when match identity is missing",
        "block final match-level row identity when match_id is missing",
    ],
    "drift_flags": ["missing_expected_payload_path"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/parsers/match_state.py",
        "src/mythic_edge_parser/parsers/gre/game_state.py",
        "src/mythic_edge_parser/parsers/gre/game_result.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_state.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "Issue #128 anchor entry preserved by issue #130.",
        "Broader Tier 1 lifecycle and result entries are mapped as separate entries.",
    ],
}

_PLAYER_TEAM_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.participants.player_team",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "player_team",
    "display_name": "player_team",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.player_team",
    "downstream_surfaces": ["MatchLogRow", "GameLogRow", "gameplay_actions", "opponent_card_observations"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "match_state.players.selected_local_player_team",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_started",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "payload.players[].team_id",
            "raw_payload_path": "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].teamId",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "unknown-like selected player teams cannot support high-confidence player results",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "game_state.system_seat_ids.local_player_team",
            "parser_event_kind": "GameState",
            "parser_event_type": "game_state_message",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.system_seat_ids[0] + payload.players[].team_id",
            "raw_payload_path": (
                "greToClientMessages[].systemSeatIds[0] + "
                "greToClientMessages[].gameStateMessage.players[].teamId"
            ),
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing local seat or matching player team leaves player_team unknown",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "client_action.local_player_team",
            "parser_event_kind": "ClientAction",
            "parser_event_type": "client_action",
            "raw_event_family": "ClientToGREMessage",
            "raw_message_type": "",
            "normalized_payload_path": "payload.team_id",
            "raw_payload_path": "ClientToGREMessage.payload.*.teamId",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "ClientAction team fields are supplemental and do not override conflicts",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_context.current_player_team",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "state_context.current_player_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "matchless or stale context is low-confidence and review-required",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.player_team",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.player_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "missing summary player_team prevents high-confidence player-facing fields",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "player_facing_results_require_known_non_conflicting_player_team",
        "known_winner_does_not_repair_missing_player_team",
        "unknown_like_player_team_values_are_unknown",
        "stale_context_is_not_high_confidence_participant_evidence",
    ],
    "degradation_behavior": [
        "None, empty strings, whitespace-only strings, zero, string zero, and booleans are unknown",
        "missing player_team prevents high-confidence player-facing W/L fields",
        "conflicting MatchState, GameState, ClientAction, or parser context evidence requires review",
        "known match or game winners are not enough to derive player-facing results without player_team",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/extractors.py",
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_state.py",
        "tests/test_app_extractors.py",
    ],
    "fixture_refs": [],
    "notes": [
        "Issue #137 documents provenance only and does not change LOCAL_PLAYER_INDEX behavior.",
        "This entry is the canonical ledger dependency for parser_state.match_summary.player_team_dependency.",
    ],
}

_OPPONENT_TEAM_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.participants.opponent_team",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "opponent_team",
    "display_name": "opponent_team",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.opponent_team",
    "downstream_surfaces": ["GameLogRow", "gameplay_actions", "opponent_card_observations"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.opponent_team",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.opponent_team()",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "unknown or non-two-team player_team yields blank opponent_team",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "missing or degraded player_team leaves opponent_team unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "opponent_team_derived_only_from_known_player_team",
        "opponent_team_not_guessed_when_player_team_unknown",
        "opponent_team_does_not_create_hidden_information_claims",
    ],
    "degradation_behavior": [
        "opponent_team is blank when player_team is unknown, degraded, conflicting, stale, or not 1 or 2",
        "workbook formulas, dashboards, AI output, and output transport do not observe opponent_team",
        "derived opponent_team does not imply hidden cards, decklists, archetypes, or advice",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": ["tests/test_evidence_ledger.py", "tests/test_state.py"],
    "fixture_refs": [],
    "notes": [
        "Documents current two-team MatchSummary.opponent_team behavior only.",
        "Issue #137 does not add opponent-team parser behavior.",
    ],
}

_LOCAL_SYSTEM_SEAT_ID_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.participants.local_system_seat_id",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "local_system_seat_id",
    "display_name": "local_system_seat_id",
    "parser_owner": "src/mythic_edge_parser/app/extractors.py",
    "model_surface": "_game_state_system_seat_ids",
    "downstream_surfaces": ["gameplay_actions", "opponent_card_observations", "local_zone_reasoning"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "game_state.system_seat_ids.local_system_seat",
            "parser_event_kind": "GameState",
            "parser_event_type": "game_state_message",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.system_seat_ids[0]",
            "raw_payload_path": "greToClientMessages[].systemSeatIds[0]",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing local system seat degrades local/private-zone and actor-relation evidence",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "match_state.players.selected_local_player_seat",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_started",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "payload.players[].system_seat_id",
            "raw_payload_path": (
                "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].systemSeatId"
            ),
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing selected-player seat leaves MatchState seat evidence unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "gameplay_actions.local_seat_id",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "GameplayGameState.local_seat_id",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "gameplay carry-forward is degraded if detached from current GameState evidence",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "local_private_zone_interpretation_requires_known_local_seat",
        "actor_relation_requires_known_local_and_actor_seats",
        "missing_local_seat_degrades_instead_of_inferring_opponent",
        "unknown_like_local_seat_values_are_unknown",
    ],
    "degradation_behavior": [
        "None, empty strings, whitespace-only strings, zero, string zero, and booleans are unknown",
        "missing local seat prevents high-confidence local/private-zone and actor-relation labels",
        "conflicting MatchState, GameState, or gameplay local seat evidence requires review",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/extractors.py",
        "src/mythic_edge_parser/app/gameplay_actions.py",
        "src/mythic_edge_parser/app/opponent_card_observations.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_extractors.py",
        "tests/test_gameplay_actions.py",
        "tests/test_opponent_card_observations.py",
    ],
    "fixture_refs": [],
    "notes": [
        "Documents current first-systemSeatIds local-seat convention without changing behavior.",
    ],
}

_PARTICIPANT_TEAM_MAPPING_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.participants.participant_team_mapping",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "participant_team_mapping",
    "display_name": "participant_team_mapping",
    "parser_owner": "src/mythic_edge_parser/app/evidence_ledger.py",
    "model_surface": "participant/player-team provenance registry",
    "downstream_surfaces": ["MatchLogRow", "GameLogRow", "gameplay_actions", "opponent_card_observations"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "match_state.players.participant_team_mapping",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_started",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "payload.players[]",
            "raw_payload_path": "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[]",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["list"],
            "missing_behavior": "missing participant records make mapping unknown",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "game_state.players.participant_team_mapping",
            "parser_event_kind": "GameState",
            "parser_event_type": "game_state_message",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.system_seat_ids + payload.players[]",
            "raw_payload_path": (
                "greToClientMessages[].systemSeatIds[] + greToClientMessages[].gameStateMessage.players[]"
            ),
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["list"],
            "missing_behavior": "missing local seat or player records make mapping unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "client_action.participant_team_supplement",
            "parser_event_kind": "ClientAction",
            "parser_event_type": "client_action",
            "raw_event_family": "ClientToGREMessage",
            "raw_message_type": "",
            "normalized_payload_path": "payload.team_id",
            "raw_payload_path": "ClientToGREMessage.payload.*.teamId",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "supplemental ClientAction evidence cannot silently resolve conflicts",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_context.participant_team_carry_forward",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "state_context.current_player_team + MatchSummary.player_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "stale or matchless carry-forward is low-confidence and review-required",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "opponent_card_observations.missing_seat_mapping_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "opponent_card_observations.degradation_flags[]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "low",
            "finality_when_used": "provisional",
            "allowed_types": ["list"],
            "missing_behavior": "missing seat mapping degrades local/opponent-dependent observations",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "participant_mapping_stays_parser_owned",
        "missing_mapping_degrades_player_relative_outputs",
        "conflicting_mapping_requires_review",
        "participant_mapping_does_not_infer_hidden_information",
    ],
    "degradation_behavior": [
        "missing player_team or local_system_seat_id makes participant mapping unknown",
        "conflicting MatchState, GameState, ClientAction, context, or gameplay evidence is low confidence",
        "missing mapping degrades player-facing results and local/opponent-dependent outputs",
        "participant mapping must not infer hidden cards, decklists, archetypes, gameplay advice, or AI truth",
    ],
    "drift_flags": [
        "missing_expected_payload_path",
        "weak_fallback_used",
        "conflicting_evidence",
        "invariant_failed",
    ],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/extractors.py",
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/gameplay_actions.py",
        "src/mythic_edge_parser/app/opponent_card_observations.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_extractors.py",
        "tests/test_gameplay_actions.py",
        "tests/test_opponent_card_observations.py",
    ],
    "fixture_refs": [],
    "notes": [
        "This entry documents a cross-field dependency and does not add a workbook or webhook field.",
        "Issue #137 keeps opponent observations and gameplay actor-relation behavior unchanged.",
    ],
}

_MATCH_STARTED_AT_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_lifecycle.match_started_at",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_started_at",
    "display_name": "MGTA Start Time",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.to_match_log_row",
    "downstream_surfaces": ["MatchLogRow", "match_history"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "match_state.match_started.timestamp",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_started",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "metadata.timestamp",
            "raw_payload_path": "log_entry.timestamp",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "live",
            "allowed_types": ["str"],
            "missing_behavior": "leave MGTA Start Time blank and mark timing evidence unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.first_event_time",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.first_event_time",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["str"],
            "missing_behavior": "leave MGTA Start Time blank and require review",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "match_start_time_not_inferred_from_runtime_clock",
        "mgta_start_time_legacy_spelling_preserved",
    ],
    "degradation_behavior": [
        "missing event timestamp leaves start time blank",
        "first-summary-touch fallback is medium confidence and review-worthy",
        "never infer start time from wall-clock runtime, workbook state, or file metadata",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/parsers/match_state.py",
    ],
    "tests": ["tests/test_evidence_ledger.py", "tests/test_state.py"],
    "fixture_refs": [],
    "notes": [
        "Documents MatchSummary.first_event_time provenance only; no runtime field evidence is attached.",
    ],
}

_MATCH_FINISHED_AT_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_lifecycle.match_finished_at",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_finished_at",
    "display_name": "MTGA End Time",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.to_match_log_row",
    "downstream_surfaces": ["MatchLogRow", "match_history"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "game_result.match_complete.timestamp",
            "parser_event_kind": "GameResult",
            "parser_event_type": "game_result",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "metadata.timestamp",
            "raw_payload_path": "log_entry.timestamp",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["str"],
            "missing_behavior": "leave MTGA End Time blank and require review",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "match_state.match_complete.timestamp",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_completed",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "metadata.timestamp",
            "raw_payload_path": "log_entry.timestamp",
            "required_for_final": False,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["str"],
            "missing_behavior": "leave MTGA End Time blank and require review",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.last_event_time",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.last_event_time",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["str"],
            "missing_behavior": "leave MTGA End Time blank without blocking final readiness",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "live_match_rows_leave_end_time_blank",
        "missing_finish_timestamp_does_not_block_current_final_readiness",
    ],
    "degradation_behavior": [
        "live rows leave MTGA End Time blank",
        "missing finish timestamp leaves the field blank and review-worthy",
        "latest-summary-touch fallback is medium confidence",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/parsers/match_state.py",
        "src/mythic_edge_parser/parsers/gre/game_result.py",
    ],
    "tests": ["tests/test_evidence_ledger.py", "tests/test_state.py"],
    "fixture_refs": [],
    "notes": [
        "Documents MatchSummary.last_event_time provenance only; final readiness remains unchanged.",
    ],
}

_MATCH_WINNER_TEAM_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_result.match_winner_team",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_winner_team",
    "display_name": "match_winner_team",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.match_winner_team",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "game_result.results.match_scope_winner",
            "parser_event_kind": "GameResult",
            "parser_event_type": "game_result",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.results[].winning_team_id",
            "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "keep match winner unknown and block final match readiness",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "match_state.game_results.match_scope_winner",
            "parser_event_kind": "MatchState",
            "parser_event_type": "match_completed",
            "raw_event_family": "matchGameRoomStateChangedEvent",
            "raw_message_type": "",
            "normalized_payload_path": "payload.game_results[].winning_team_id",
            "raw_payload_path": "matchGameRoomStateChangedEvent.gameRoomInfo.results[].winningTeamId",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "keep match winner unknown and block final match readiness",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "game_result.top_level_match_complete_winner",
            "parser_event_kind": "GameResult",
            "parser_event_type": "game_result",
            "raw_event_family": "greToClientEvent",
            "raw_message_type": "GREMessageType_GameStateMessage",
            "normalized_payload_path": "payload.winning_team_id",
            "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId",
            "required_for_final": True,
            "value_source_when_used": "observed",
            "confidence_when_used": "medium",
            "finality_when_used": "final",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "fallback only when MatchState_MatchComplete has no nested match winner",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "observed",
        "fallback": "observed",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "provisional",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "nested_match_scope_winner_precedence",
        "top_level_winner_fallback_requires_match_complete",
        "unknown_winner_values_do_not_overwrite_known_winner",
    ],
    "degradation_behavior": [
        "None, empty string, 0, and string 0 are unknown winner values",
        "unknown winner values must not set or overwrite a known match winner",
        "game-level result aggregation must not infer match winner",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/parsers/match_state.py",
        "src/mythic_edge_parser/parsers/gre/game_result.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_state.py",
        "tests/test_gre_game_result_parser.py",
    ],
    "fixture_refs": [],
    "notes": [
        "Documents existing GameResult and MatchState winner precedence without changing reconciliation.",
    ],
}

_MATCH_RESULT_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_result.match_result",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_result",
    "display_name": "Match Win?",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.match_wl",
    "downstream_surfaces": ["MatchLogRow", "match_history"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.match_wl",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.match_wl",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["str"],
            "missing_behavior": "leave Match Win? blank when winner or local team is unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.match_winner_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.match_winner_team",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing or unknown winner prevents high-confidence Match Win?",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.player_team",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing local team prevents high-confidence Match Win?",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing participant provenance prevents high-confidence Match Win?",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "provisional",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "match_result_derived_from_winner_and_player_team",
        "match_result_not_directly_observed_as_win_loss",
    ],
    "degradation_behavior": [
        "missing player_team prevents high-confidence Match Win?",
        "missing or unknown match_winner_team leaves Match Win? blank or unknown",
        "known winner without known local team is not enough to mark win or loss",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": ["tests/test_evidence_ledger.py", "tests/test_state.py"],
    "fixture_refs": [],
    "notes": [
        "Documents derived win/loss provenance.",
        "Issue #137 maps the participant provenance dependency behind MatchSummary.player_team.",
    ],
}

_MATCH_SYNC_STATUS_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_lifecycle.match_sync_status",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_sync_status",
    "display_name": "MTGA Sync Status",
    "parser_owner": "src/mythic_edge_parser/app/state.py",
    "model_surface": "MatchSummary.to_match_log_row",
    "downstream_surfaces": ["MatchLogRow", "match_history"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary_ready",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.is_ready()",
            "raw_payload_path": "",
            "required_for_final": True,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["bool"],
            "missing_behavior": "keep row live or unknown when readiness ingredients are missing",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.live_match_log_row",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "state.build_live_match_log_row",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "live",
            "allowed_types": ["dict"],
            "missing_behavior": "missing match ID prevents meaningful sync-status evidence",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "models.match_summary.to_match_log_row.final_argument",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.to_match_log_row(final=...)",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["bool"],
            "missing_behavior": "missing readiness arguments keep status live or unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "match_sync_status_derived_from_parser_state_readiness",
        "workbook_transport_must_not_decide_finality",
    ],
    "degradation_behavior": [
        "missing match ID prevents meaningful sync-status evidence",
        "missing winner or local team keeps current status live or provisional",
        "row presence, Apps Script upsert state, and webhook delivery do not decide finality",
    ],
    "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/state.py",
        "src/mythic_edge_parser/app/models.py",
    ],
    "tests": ["tests/test_evidence_ledger.py", "tests/test_state.py"],
    "fixture_refs": [],
    "notes": [
        "Documents current Live/Final row status provenance without changing readiness rules.",
    ],
}

_GAMES_WON_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_aggregates.games_won",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "games_won",
    "display_name": "Games Won",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.game_wins",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_wins",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_wins",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int"],
            "missing_behavior": "leave Games Won blank in workbook rows when total_games is zero",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_winner_dependencies",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.games[].winner_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "missing game winners are not counted as wins and must not be invented",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.player_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing local player team makes wins degraded rather than confidently zero",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing participant provenance makes Games Won degraded rather than confident",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.total_games_display_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.total_games",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "workbook-facing Games Won is blank when total_games is zero",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "aggregate_fields_derived_not_observed",
        "game_wins_non_negative",
        "game_wins_not_greater_than_total_games",
        "game_aggregate_expected_blank_when_total_games_zero",
    ],
    "degradation_behavior": [
        "missing player_team prevents high-confidence Games Won",
        "unknown-like winner values such as 0 or string 0 make future evidence review-required",
        "debug and history surfaces may expose numeric zero while workbook-facing Games Won is blank",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_models.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "Documents existing MatchSummary.game_wins math without computing field evidence at runtime.",
        "Issue #134 maps tier3.game_results game-winner dependencies for future field-evidence attachment.",
        "Issue #137 maps the participant provenance dependency behind MatchSummary.player_team.",
    ],
}

_GAMES_LOST_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_aggregates.games_lost",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "games_lost",
    "display_name": "Games Lost",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.game_losses",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_losses",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_losses",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int"],
            "missing_behavior": "leave Games Lost blank in workbook rows when total_games is zero",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.completed_game_dependencies",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.games[].winner_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int", "unknown"],
            "missing_behavior": "missing game winners are not completed games and are not counted as losses",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.game_wins_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_wins",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "missing wins dependency makes losses degraded or unknown",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.player_team",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "missing local player team makes losses degraded rather than confidently counted",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing participant provenance makes Games Lost degraded rather than confident",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "aggregate_fields_derived_not_observed",
        "game_losses_non_negative",
        "game_losses_not_greater_than_total_games",
        "game_aggregate_expected_blank_when_total_games_zero",
    ],
    "degradation_behavior": [
        "missing player_team prevents high-confidence Games Lost",
        "unknown-like winner values such as 0 or string 0 make future evidence review-required",
        "debug and history surfaces may expose numeric zero while workbook-facing Games Lost is blank",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_models.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "Documents existing MatchSummary.game_losses math without computing field evidence at runtime.",
        "Issue #134 maps tier3.game_results game-winner dependencies for future field-evidence attachment.",
        "Issue #137 maps the participant provenance dependency behind MatchSummary.player_team.",
    ],
}

_TOTAL_GAMES_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_aggregates.total_games",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "total_games",
    "display_name": "Total Games",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.total_games",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.total_games",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.total_games",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int"],
            "missing_behavior": "leave Total Games blank in workbook rows when total_games is zero",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_wins_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_wins",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "missing wins dependency makes total games degraded or unknown",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.game_losses_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_losses",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "missing losses dependency makes total games degraded or unknown",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "aggregate_fields_derived_not_observed",
        "games_won_plus_games_lost_equals_total_games",
        "total_games_non_negative",
        "total_games_not_inferred_from_match_format",
        "game_aggregate_expected_blank_when_total_games_zero",
    ],
    "degradation_behavior": [
        "blank Total Games with no completed game evidence is expected",
        "impossible totals or totals that disagree with wins plus losses require review",
        "do not infer total games from match format, sideboarding, workbook formulas, or AI output",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_models.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "Documents existing MatchSummary.total_games math without computing field evidence at runtime.",
        "Issue #134 maps tier3.game_results game-result dependencies for future field-evidence attachment.",
    ],
}

_MATCH_WIN_FLAG_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_aggregates.match_win_flag",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "match_win_flag",
    "display_name": "Match Win Flag",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.match_win_flag",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.match_win_flag",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.match_win_flag",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["int", "str"],
            "missing_behavior": "blank Match Win Flag is expected when Match Win? is blank",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.match_wl_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.match_wl",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["str"],
            "missing_behavior": "missing or degraded match result yields blank or degraded Match Win Flag",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.match_result.match_result_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.match_result.match_result]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["str"],
            "missing_behavior": "match_result ledger dependency must explain blank or degraded flag evidence",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing participant provenance explains blank or degraded Match Win Flag",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "aggregate_fields_derived_not_observed",
        "match_win_flag_agrees_with_match_result",
        "match_win_flag_blank_when_match_result_blank",
        "match_win_flag_not_inferred_from_game_aggregates",
    ],
    "degradation_behavior": [
        "blank Match Win Flag is expected when Match Win? is blank",
        "conflict between Match Win Flag and Match Win? requires review",
        "do not infer Match Win Flag from games_won, games_lost, best-of structure, workbook formulas, or AI output",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_models.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "Documents existing MatchSummary.match_win_flag aliasing of match_wl.",
        "The authoritative match result dependency remains tier1.match_result.match_result.",
        "Issue #137 maps the participant provenance dependency behind MatchSummary.player_team.",
    ],
}

_GAME_WIN_RATE_ENTRY: dict[str, Any] = {
    "entry_id": "tier1.match_aggregates.game_win_rate",
    "tier": 1,
    "output_family": "match_identity_and_lifecycle",
    "output_field": "game_win_rate",
    "display_name": "Game Win %",
    "parser_owner": "src/mythic_edge_parser/app/models.py",
    "model_surface": "MatchSummary.game_win_rate",
    "downstream_surfaces": ["MatchLogRow", "match_history", "state_snapshots"],
    "parser_managed_truth": True,
    "coverage_status": "seeded_sample",
    "direct_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_win_rate",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_win_rate",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "high",
            "finality_when_used": "final",
            "allowed_types": ["str", "unknown"],
            "missing_behavior": "blank Game Win % is expected and not applicable when total_games is zero",
            "privacy_class": "path_only_no_values",
        },
    ],
    "fallback_evidence": [
        {
            "signal_id": "parser_state.match_summary.game_wins_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.game_wins",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "missing or degraded wins dependency makes Game Win % degraded or unknown",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "parser_state.match_summary.total_games_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "MatchSummary.total_games",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int"],
            "missing_behavior": "zero completed games means Game Win % is blank and not applicable, not zero",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "participant provenance flows through Games Won and Games Lost dependencies",
            "privacy_class": "path_only_no_values",
        },
    ],
    "value_source_policy": {
        "direct": "derived",
        "fallback": "derived",
        "missing": "unknown",
        "contradiction": "conflict",
    },
    "confidence_policy": {
        "direct": "high",
        "fallback": "medium",
        "weak_fallback": "low",
        "missing": "unknown",
        "contradiction": "low",
    },
    "finality_policy": {
        "live": "live",
        "provisional": "provisional",
        "final": "final",
        "corrected_by_later_evidence": "reconciled",
    },
    "invariant_checks": [
        "aggregate_fields_derived_not_observed",
        "game_win_rate_equals_game_wins_div_total_games",
        "game_win_rate_blank_when_total_games_zero",
        "game_win_rate_within_zero_and_one",
        "division_by_zero_not_applicable",
    ],
    "degradation_behavior": [
        "blank Game Win % with no completed games is expected and should not require review by itself",
        "blank rate with completed games or nonblank rate with zero completed games requires review",
        "negative rate or rate outside zero through one requires review",
    ],
    "drift_flags": ["missing_expected_payload_path", "weak_fallback_used", "conflicting_evidence", "invariant_failed"],
    "recommended_review_modules": [
        "src/mythic_edge_parser/app/models.py",
        "src/mythic_edge_parser/app/state.py",
    ],
    "tests": [
        "tests/test_evidence_ledger.py",
        "tests/test_app_models.py",
        "tests/test_golden_replay_harness.py",
    ],
    "fixture_refs": [
        "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
        "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
    ],
    "notes": [
        "The #128 allowed-type labels do not include float; invariants document numeric rate behavior.",
        "Issue #134 maps tier3.game_results game aggregate dependencies for future field-evidence attachment.",
        "Issue #137 maps participant provenance through Games Won and Games Lost dependencies.",
    ],
}


def _game_number_entry() -> dict[str, Any]:
    return {
        "entry_id": "tier3.game_results.game_number",
        "tier": 3,
        "output_family": "game_level_facts",
        "output_field": "game_number",
        "display_name": "Game Number",
        "parser_owner": "src/mythic_edge_parser/app/state.py",
        "model_surface": "GameSummary.to_game_log_row",
        "downstream_surfaces": ["GameLogRow", "MatchLogRow", "golden_replay"],
        "parser_managed_truth": True,
        "coverage_status": "seeded_sample",
        "direct_evidence": [
            {
                "signal_id": "game_result.identity.game_number",
                "parser_event_kind": "GameResult",
                "parser_event_type": "game_result",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.identity.game_number",
                "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.gameNumber",
                "required_for_final": True,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "final",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "game result cannot attach to a per-game slot without a known game number",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "game_result.game_info.game_number",
                "parser_event_kind": "GameResult",
                "parser_event_type": "game_result",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.game_info.gameNumber",
                "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.gameNumber",
                "required_for_final": True,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "final",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "fall back to parser context only while preserving degraded provenance",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "game_state.identity.game_number",
                "parser_event_kind": "GameState",
                "parser_event_type": "game_state_message",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.identity.game_number",
                "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.gameNumber",
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "live",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "do not synthesize a slot from unrelated game state",
                "privacy_class": "path_only_no_values",
            },
        ],
        "fallback_evidence": [
            {
                "signal_id": "parser_context.current_game_number",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": "state_context.current_game_number",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "leave game-level fields blank or degraded when context is unknown",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "match_state.game_results.list_order",
                "parser_event_kind": "MatchState",
                "parser_event_type": "match_completed",
                "raw_event_family": "matchGameRoomStateChangedEvent",
                "raw_message_type": "",
                "normalized_payload_path": "payload.game_results[]",
                "raw_payload_path": "matchGameRoomStateChangedEvent.gameRoomInfo.finalMatchResult.resultList[]",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "final",
                "allowed_types": ["list"],
                "missing_behavior": "ordered MatchState game results remain review-worthy slot evidence",
                "privacy_class": "path_only_no_values",
            },
        ],
        "value_source_policy": {
            "direct": "observed",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        },
        "confidence_policy": {
            "direct": "high",
            "fallback": "medium",
            "weak_fallback": "low",
            "missing": "unknown",
            "contradiction": "low",
        },
        "finality_policy": {
            "live": "live",
            "provisional": "provisional",
            "final": "final",
            "corrected_by_later_evidence": "reconciled",
        },
        "invariant_checks": [
            "game_number_must_be_slot_1_2_or_3",
            "per_game_results_require_known_game_number",
            "match_state_list_order_is_medium_confidence_slot_evidence",
            "game_log_row_identity_match_id_and_game_number",
        ],
        "degradation_behavior": [
            "missing game number does not create or guess a game slot",
            "MatchState list-order mapping is usable only as medium confidence ordered slot evidence",
            "out-of-range game numbers are degraded and should not populate game1 through game3 fields",
        ],
        "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence", "invariant_failed"],
        "recommended_review_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/parsers/gre/game_result.py",
            "src/mythic_edge_parser/parsers/match_state.py",
        ],
        "tests": [
            "tests/test_evidence_ledger.py",
            "tests/test_state.py",
            "tests/test_gre_game_result_parser.py",
            "tests/test_match_summary_from_match_state.py",
        ],
        "fixture_refs": [
            "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
            "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
        ],
        "notes": [
            "This entry documents slot identity; it does not attach runtime field evidence.",
            "Issue #134 keeps per-game slots limited to games 1 through 3.",
        ],
    }


def _game_winner_entry(game_number: int) -> dict[str, Any]:
    game_label = f"game{game_number}"
    return {
        "entry_id": f"tier3.game_results.{game_label}_winner_team",
        "tier": 3,
        "output_family": "game_level_facts",
        "output_field": f"{game_label}_winner_team",
        "display_name": f"g{game_number}_winner_team",
        "parser_owner": "src/mythic_edge_parser/app/state.py",
        "model_surface": "MatchSummary._game_winner_fields",
        "downstream_surfaces": ["MatchLogRow", "GameLogRow", "match_history", "state_snapshots"],
        "parser_managed_truth": True,
        "coverage_status": "seeded_sample",
        "direct_evidence": [
            {
                "signal_id": f"game_result.{game_label}.game_scope_winner",
                "parser_event_kind": "GameResult",
                "parser_event_type": "game_result",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.results[].winning_team_id",
                "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId",
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "final",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "game winner remains unknown when no valid nested MatchScope_Game result exists",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": f"match_state.{game_label}.game_scope_winner",
                "parser_event_kind": "MatchState",
                "parser_event_type": "match_completed",
                "raw_event_family": "matchGameRoomStateChangedEvent",
                "raw_message_type": "",
                "normalized_payload_path": "payload.game_results[].winning_team_id",
                "raw_payload_path": (
                    "matchGameRoomStateChangedEvent.gameRoomInfo.finalMatchResult.resultList[].winningTeamId"
                ),
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "medium",
                "finality_when_used": "final",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "MatchState ordered game result maps only to its list-order game slot",
                "privacy_class": "path_only_no_values",
            },
        ],
        "fallback_evidence": [
            {
                "signal_id": f"game_result.{game_label}.top_level_legacy_winner",
                "parser_event_kind": "GameResult",
                "parser_event_type": "game_result",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.winning_team_id",
                "raw_payload_path": "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId",
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": (
                    "legacy top-level winner is used only when no nested results list exists "
                    "and slot identity is known"
                ),
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "tier3.game_results.game_number_dependency",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": "ledger.entries[tier3.game_results.game_number]",
                "raw_payload_path": "",
                "required_for_final": True,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "winner evidence is degraded when the game slot cannot be identified",
                "privacy_class": "path_only_no_values",
            },
        ],
        "value_source_policy": {
            "direct": "observed",
            "fallback": "observed",
            "missing": "unknown",
            "contradiction": "conflict",
        },
        "confidence_policy": {
            "direct": "high",
            "fallback": "medium",
            "weak_fallback": "low",
            "missing": "unknown",
            "contradiction": "low",
        },
        "finality_policy": {
            "live": "live",
            "provisional": "provisional",
            "final": "final",
            "corrected_by_later_evidence": "reconciled",
        },
        "invariant_checks": [
            f"{game_label}_winner_uses_game_scope_evidence",
            f"{game_label}_winner_does_not_promote_match_scope_result",
            f"{game_label}_winner_requires_valid_game_slot",
            "latest_valid_nested_game_scope_result_wins",
            "unknown_like_winners_do_not_become_high_confidence",
        ],
        "degradation_behavior": [
            "None, empty string, zero, string zero, whitespace zero, and bool winners are unknown",
            "match-scope results, match winner, aggregates, workbook formulas, "
            "and AI output must not populate game winner",
            "unknown winner evidence must not overwrite a known game winner",
            "missing game-scope evidence for an unplayed slot is expected blank behavior",
        ],
        "drift_flags": ["missing_expected_payload_path", "fallback_used", "conflicting_evidence", "invariant_failed"],
        "recommended_review_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/parsers/gre/game_result.py",
            "src/mythic_edge_parser/parsers/match_state.py",
        ],
        "tests": [
            "tests/test_evidence_ledger.py",
            "tests/test_state.py",
            "tests/test_gre_game_result_parser.py",
            "tests/test_match_summary_from_match_state.py",
        ],
        "fixture_refs": [
            "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
            "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
        ],
        "notes": [
            "GameResult nested MatchScope_Game is the high-confidence game winner source.",
            "MatchState finalMatchResult.resultList is medium-confidence ordered game-slot evidence.",
            "MatchScope_Match and top-level match winners are not promoted into game winner fields.",
        ],
    }


def _game_result_entry(game_number: int) -> dict[str, Any]:
    game_label = f"game{game_number}"
    return {
        "entry_id": f"tier3.game_results.{game_label}_result",
        "tier": 3,
        "output_family": "game_level_facts",
        "output_field": f"{game_label}_result",
        "display_name": f"Game {game_number} Result",
        "parser_owner": "src/mythic_edge_parser/app/models.py",
        "model_surface": "MatchSummary._game_result_fields",
        "downstream_surfaces": ["MatchLogRow", "GameLogRow", "match_history", "state_snapshots"],
        "parser_managed_truth": True,
        "coverage_status": "seeded_sample",
        "direct_evidence": [
            {
                "signal_id": f"parser_state.match_summary.{game_label}_result",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": f"MatchSummary._game_result_fields().g{game_number}_result",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "high",
                "finality_when_used": "final",
                "allowed_types": ["str", "unknown"],
                "missing_behavior": "blank is expected when winner or local player team is unknown",
                "privacy_class": "path_only_no_values",
            },
        ],
        "fallback_evidence": [
            {
                "signal_id": f"ledger.tier3.game_results.{game_label}_winner_team_dependency",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": f"ledger.entries[tier3.game_results.{game_label}_winner_team]",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["int", "str-int", "unknown"],
                "missing_behavior": "missing or degraded winner dependency yields blank or degraded game result",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "parser_state.match_summary.player_team_dependency",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": "MatchSummary.player_team",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["int", "str-int", "unknown"],
                "missing_behavior": "missing local player team leaves per-game result blank",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": "ledger.tier1.participants.player_team_dependency",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "medium",
                "finality_when_used": "provisional",
                "allowed_types": ["dict"],
                "missing_behavior": "missing participant provenance leaves per-game result blank or degraded",
                "privacy_class": "path_only_no_values",
            },
        ],
        "value_source_policy": {
            "direct": "derived",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        },
        "confidence_policy": {
            "direct": "high",
            "fallback": "medium",
            "weak_fallback": "low",
            "missing": "unknown",
            "contradiction": "low",
        },
        "finality_policy": {
            "live": "live",
            "provisional": "provisional",
            "final": "final",
            "corrected_by_later_evidence": "reconciled",
        },
        "invariant_checks": [
            f"{game_label}_result_derived_from_winner_and_player_team",
            f"{game_label}_result_missing_winner_not_inferred_loss",
            f"{game_label}_result_expected_blank_when_not_played",
            f"{game_label}_result_not_inferred_from_match_result_or_aggregates",
        ],
        "degradation_behavior": [
            "blank result for an unplayed game slot is expected",
            "a played game with missing winner or local player team is degraded and review-worthy",
            "do not infer game result from match result, match winner, aggregate counts, "
            "workbook formulas, or AI output",
        ],
        "drift_flags": [
            "missing_expected_payload_path",
            "weak_fallback_used",
            "conflicting_evidence",
            "invariant_failed",
        ],
        "recommended_review_modules": [
            "src/mythic_edge_parser/app/models.py",
            "src/mythic_edge_parser/app/state.py",
        ],
        "tests": [
            "tests/test_evidence_ledger.py",
            "tests/test_state.py",
            "tests/test_golden_replay_harness.py",
        ],
        "fixture_refs": [
            "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
            "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
        ],
        "notes": [
            "The result is player-relative and derived from winner_team plus MatchSummary.player_team.",
            "Expected blank behavior separates unplayed game slots from degraded played slots.",
            "Issue #137 maps the participant provenance dependency behind MatchSummary.player_team.",
        ],
    }


def _play_draw_starting_player_entry(game_number: int) -> dict[str, Any]:
    game_label = f"game{game_number}"
    previous_game = game_number - 1
    fallback_evidence: list[dict[str, Any]] = [
        {
            "signal_id": "tier3.game_results.game_number_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier3.game_results.game_number]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["int", "str-int"],
            "missing_behavior": "starting-player evidence is degraded when the game slot cannot be identified",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.participant_team_mapping_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.participant_team_mapping]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "seat-only starting-player evidence stays degraded without participant mapping",
            "privacy_class": "path_only_no_values",
        },
    ]
    if game_number > 1:
        fallback_evidence.extend(
            [
                {
                    "signal_id": f"model.{game_label}.inferred_starting_player_from_previous_game",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": f"MatchSummary.effective_starting_player({game_number})",
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "inferred",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["int", "str-int", "unknown"],
                    "missing_behavior": (
                        "later-game inference is unavailable when the previous winner or participant "
                        "context is missing"
                    ),
                    "privacy_class": "path_only_no_values",
                },
                {
                    "signal_id": f"ledger.tier3.game_results.game{previous_game}_winner_team_dependency",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": (
                        f"ledger.entries[tier3.game_results.game{previous_game}_winner_team]"
                    ),
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "derived",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["int", "str-int", "unknown"],
                    "missing_behavior": (
                        f"missing game {previous_game} winner prevents inferred game {game_number} starter"
                    ),
                    "privacy_class": "path_only_no_values",
                },
                {
                    "signal_id": "ledger.tier1.participants.player_team_dependency",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "derived",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["dict"],
                    "missing_behavior": "missing local player team prevents inferred later-game starter",
                    "privacy_class": "path_only_no_values",
                },
                {
                    "signal_id": "ledger.tier1.participants.opponent_team_dependency",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": "ledger.entries[tier1.participants.opponent_team]",
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "derived",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["dict"],
                    "missing_behavior": "missing opponent team prevents inferred starter when prior winner is local",
                    "privacy_class": "path_only_no_values",
                },
            ]
        )

    return {
        "entry_id": f"tier3.play_draw.{game_label}_starting_player",
        "tier": 3,
        "output_family": "game_level_facts",
        "output_field": f"{game_label}_starting_player",
        "display_name": f"g{game_number}_starting_player",
        "parser_owner": "src/mythic_edge_parser/app/models.py",
        "model_surface": f"MatchSummary.effective_starting_player({game_number})",
        "downstream_surfaces": ["MatchLogRow", "GameLogRow", "match_history", "state_snapshots"],
        "parser_managed_truth": True,
        "coverage_status": "seeded_sample",
        "direct_evidence": [
            {
                "signal_id": f"client_action.{game_label}.choose_starting_player",
                "parser_event_kind": "ClientAction",
                "parser_event_type": "generic_client_action",
                "raw_event_family": "ClientToGREMessage",
                "raw_message_type": "ClientMessageType_ChooseStartingPlayerResp",
                "normalized_payload_path": "_extract_starting_player_from_client_action(payload)",
                "raw_payload_path": "ClientToGREMessage.payload.chooseStartingPlayerResp.systemSeatId",
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "live",
                "allowed_types": ["int", "str-int", "unknown"],
                "missing_behavior": "missing choose-starting-player response does not infer the starter",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": f"game_state.{game_label}.turn_one_active_player_team",
                "parser_event_kind": "GameState",
                "parser_event_type": "game_state_message",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": (
                    "payload.turn_info.active_player_seat_id + payload.players[].team_id"
                ),
                "raw_payload_path": (
                    "greToClientMessages[].gameStateMessage.turnInfo.activePlayer + "
                    "greToClientMessages[].gameStateMessage.players[].teamId"
                ),
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "high",
                "finality_when_used": "live",
                "allowed_types": ["int", "str-int"],
                "missing_behavior": "turn-one active-player evidence must map to a known team",
                "privacy_class": "path_only_no_values",
            },
            {
                "signal_id": f"game_state.{game_label}.turn_one_active_player_seat",
                "parser_event_kind": "GameState",
                "parser_event_type": "game_state_message",
                "raw_event_family": "greToClientEvent",
                "raw_message_type": "GREMessageType_GameStateMessage",
                "normalized_payload_path": "payload.turn_info.active_player_seat_id",
                "raw_payload_path": (
                    "greToClientMessages[].gameStateMessage.turnInfo.activePlayerSeatId"
                ),
                "required_for_final": False,
                "value_source_when_used": "observed",
                "confidence_when_used": "low",
                "finality_when_used": "live",
                "allowed_types": ["int", "str-int", "unknown"],
                "missing_behavior": "seat-only active-player evidence is degraded without team mapping",
                "privacy_class": "path_only_no_values",
            },
        ],
        "fallback_evidence": fallback_evidence,
        "value_source_policy": {
            "direct": "observed",
            "fallback": "inferred" if game_number > 1 else "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        },
        "confidence_policy": {
            "direct": "high",
            "fallback": "medium",
            "weak_fallback": "low",
            "missing": "unknown",
            "contradiction": "low",
        },
        "finality_policy": {
            "live": "live",
            "provisional": "provisional",
            "final": "final",
            "corrected_by_later_evidence": "reconciled",
        },
        "invariant_checks": [
            f"{game_label}_starting_player_explicit_evidence_outranks_inference",
            f"{game_label}_starting_player_turn_one_evidence_requires_turn_number_1",
            f"{game_label}_starting_player_seat_only_evidence_degraded_without_mapping",
            f"{game_label}_starting_player_unknown_like_values_are_unknown",
            f"{game_label}_starting_player_expected_blank_when_unplayed",
            *(
                [
                    f"{game_label}_starting_player_inference_requires_game{previous_game}_winner_and_participants",
                    f"{game_label}_starting_player_inference_labeled_inferred_not_observed",
                ]
                if game_number > 1
                else [f"{game_label}_starting_player_not_inferred_from_previous_game"]
            ),
        ],
        "degradation_behavior": [
            "None, empty strings, whitespace-only strings, zero, string zero, and booleans are unknown",
            "seat-only starting-player evidence is degraded unless participant mapping proves the team",
            f"blank {game_label} starting player is expected when game {game_number} is unplayed",
            f"played game {game_number} with missing starting-player evidence is degraded and review-worthy",
            "conflicting ClientAction, GameState, model, or participant evidence requires review",
            "workbook formulas, dashboards, Apps Script, webhook transport, and AI do not populate starters",
        ],
        "drift_flags": [
            "missing_expected_payload_path",
            "weak_fallback_used",
            "conflicting_evidence",
            "invariant_failed",
        ],
        "recommended_review_modules": [
            "src/mythic_edge_parser/app/extractors.py",
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ],
        "tests": [
            "tests/test_evidence_ledger.py",
            "tests/test_app_extractors.py",
            "tests/test_app_models.py",
            "tests/test_match_summary_from_match_state.py",
            "tests/test_state.py",
        ],
        "fixture_refs": [],
        "notes": [
            "Issue #139 documents starting-player provenance without changing parser behavior.",
            "Issue #137 participant mapping controls seat-to-team confidence for play/draw.",
            "Issue #134 game-number and game-result entries provide slot and inference dependencies.",
            "Issue #140 mulligan provenance remains deferred and is not required by this entry.",
        ],
    }


def _play_draw_label_entry(game_number: int) -> dict[str, Any]:
    game_label = f"game{game_number}"
    previous_game = game_number - 1
    fallback_evidence: list[dict[str, Any]] = [
        {
            "signal_id": f"ledger.tier3.play_draw.{game_label}_starting_player_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": f"ledger.entries[tier3.play_draw.{game_label}_starting_player]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing or degraded starting-player provenance leaves play/draw blank",
            "privacy_class": "path_only_no_values",
        },
        {
            "signal_id": "ledger.tier1.participants.player_team_dependency",
            "parser_event_kind": "parser_context",
            "parser_event_type": "",
            "raw_event_family": "parser_context",
            "raw_message_type": "",
            "normalized_payload_path": "ledger.entries[tier1.participants.player_team]",
            "raw_payload_path": "",
            "required_for_final": False,
            "value_source_when_used": "derived",
            "confidence_when_used": "medium",
            "finality_when_used": "provisional",
            "allowed_types": ["dict"],
            "missing_behavior": "missing local player team leaves play/draw blank",
            "privacy_class": "path_only_no_values",
        },
    ]
    if game_number > 1:
        fallback_evidence.extend(
            [
                {
                    "signal_id": "ledger.tier1.participants.opponent_team_dependency",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": "ledger.entries[tier1.participants.opponent_team]",
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "derived",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["dict"],
                    "missing_behavior": "missing opponent team weakens inferred later-game play/draw",
                    "privacy_class": "path_only_no_values",
                },
                {
                    "signal_id": f"ledger.tier3.game_results.game{previous_game}_winner_team_dependency",
                    "parser_event_kind": "parser_context",
                    "parser_event_type": "",
                    "raw_event_family": "parser_context",
                    "raw_message_type": "",
                    "normalized_payload_path": (
                        f"ledger.entries[tier3.game_results.game{previous_game}_winner_team]"
                    ),
                    "raw_payload_path": "",
                    "required_for_final": False,
                    "value_source_when_used": "derived",
                    "confidence_when_used": "medium",
                    "finality_when_used": "provisional",
                    "allowed_types": ["int", "str-int", "unknown"],
                    "missing_behavior": (
                        f"missing game {previous_game} winner weakens inferred game {game_number} play/draw"
                    ),
                    "privacy_class": "path_only_no_values",
                },
            ]
        )

    return {
        "entry_id": f"tier3.play_draw.{game_label}_play_draw",
        "tier": 3,
        "output_family": "game_level_facts",
        "output_field": f"{game_label}_play_draw",
        "display_name": f"G{game_number} Play / Draw",
        "parser_owner": "src/mythic_edge_parser/app/models.py",
        "model_surface": f"MatchSummary.game_play_draw({game_number})",
        "downstream_surfaces": ["MatchLogRow", "GameLogRow", "match_history", "state_snapshots"],
        "parser_managed_truth": True,
        "coverage_status": "seeded_sample",
        "direct_evidence": [
            {
                "signal_id": f"parser_state.match_summary.{game_label}_play_draw",
                "parser_event_kind": "parser_context",
                "parser_event_type": "",
                "raw_event_family": "parser_context",
                "raw_message_type": "",
                "normalized_payload_path": f"MatchSummary._game_play_draw_fields().g{game_number}_play_draw",
                "raw_payload_path": "",
                "required_for_final": False,
                "value_source_when_used": "derived",
                "confidence_when_used": "high",
                "finality_when_used": "provisional",
                "allowed_types": ["str", "unknown"],
                "missing_behavior": "blank is expected when starting player or local player team is unknown",
                "privacy_class": "path_only_no_values",
            },
        ],
        "fallback_evidence": fallback_evidence,
        "value_source_policy": {
            "direct": "derived",
            "fallback": "derived",
            "missing": "unknown",
            "contradiction": "conflict",
        },
        "confidence_policy": {
            "direct": "high",
            "fallback": "medium",
            "weak_fallback": "low",
            "missing": "unknown",
            "contradiction": "low",
        },
        "finality_policy": {
            "live": "live",
            "provisional": "provisional",
            "final": "final",
            "corrected_by_later_evidence": "reconciled",
        },
        "invariant_checks": [
            f"{game_label}_play_draw_requires_starting_player_and_player_team",
            f"{game_label}_play_draw_missing_starting_player_not_draw",
            f"{game_label}_play_draw_expected_blank_when_unplayed",
            f"{game_label}_play_draw_not_inferred_from_match_result_aggregates_or_ai",
            *(
                [f"{game_label}_play_draw_exposes_inferred_starting_player_dependency"]
                if game_number > 1
                else []
            ),
        ],
        "degradation_behavior": [
            "missing starting player leaves play/draw blank",
            "missing local player team leaves play/draw blank",
            "known starting player without known player team is not high-confidence play/draw",
            "known player team without starting-player evidence is not high-confidence play/draw",
            f"blank {game_label} play/draw is expected when game {game_number} is unplayed",
            f"played game {game_number} with missing starting-player evidence is degraded and review-worthy",
            "match result, aggregate counts, workbook formulas, dashboards, Apps Script, webhook "
            "transport, and AI must not populate play/draw",
        ],
        "drift_flags": [
            "missing_expected_payload_path",
            "weak_fallback_used",
            "conflicting_evidence",
            "invariant_failed",
        ],
        "recommended_review_modules": [
            "src/mythic_edge_parser/app/models.py",
            "src/mythic_edge_parser/app/state.py",
        ],
        "tests": [
            "tests/test_evidence_ledger.py",
            "tests/test_app_models.py",
            "tests/test_match_summary_from_match_state.py",
            "tests/test_state.py",
        ],
        "fixture_refs": [],
        "notes": [
            "Issue #139 documents derived play/draw labels without changing model behavior.",
            "Issue #137 participant provenance supplies player-team dependencies.",
            "Issue #134 game-result dependencies are cited only for later-game inference context.",
            "Issue #140 mulligan provenance remains deferred and is not required by this entry.",
        ],
    }


_GAME_NUMBER_ENTRY = _game_number_entry()
_GAME1_WINNER_TEAM_ENTRY = _game_winner_entry(1)
_GAME2_WINNER_TEAM_ENTRY = _game_winner_entry(2)
_GAME3_WINNER_TEAM_ENTRY = _game_winner_entry(3)
_GAME1_RESULT_ENTRY = _game_result_entry(1)
_GAME2_RESULT_ENTRY = _game_result_entry(2)
_GAME3_RESULT_ENTRY = _game_result_entry(3)
_GAME1_STARTING_PLAYER_ENTRY = _play_draw_starting_player_entry(1)
_GAME2_STARTING_PLAYER_ENTRY = _play_draw_starting_player_entry(2)
_GAME3_STARTING_PLAYER_ENTRY = _play_draw_starting_player_entry(3)
_GAME1_PLAY_DRAW_ENTRY = _play_draw_label_entry(1)
_GAME2_PLAY_DRAW_ENTRY = _play_draw_label_entry(2)
_GAME3_PLAY_DRAW_ENTRY = _play_draw_label_entry(3)

_LEDGER_ENTRIES: tuple[dict[str, Any], ...] = (
    _MATCH_ID_ENTRY,
    _PLAYER_TEAM_ENTRY,
    _OPPONENT_TEAM_ENTRY,
    _LOCAL_SYSTEM_SEAT_ID_ENTRY,
    _PARTICIPANT_TEAM_MAPPING_ENTRY,
    _MATCH_STARTED_AT_ENTRY,
    _MATCH_FINISHED_AT_ENTRY,
    _MATCH_WINNER_TEAM_ENTRY,
    _MATCH_RESULT_ENTRY,
    _MATCH_SYNC_STATUS_ENTRY,
    _GAMES_WON_ENTRY,
    _GAMES_LOST_ENTRY,
    _TOTAL_GAMES_ENTRY,
    _MATCH_WIN_FLAG_ENTRY,
    _GAME_WIN_RATE_ENTRY,
    _GAME_NUMBER_ENTRY,
    _GAME1_WINNER_TEAM_ENTRY,
    _GAME2_WINNER_TEAM_ENTRY,
    _GAME3_WINNER_TEAM_ENTRY,
    _GAME1_RESULT_ENTRY,
    _GAME2_RESULT_ENTRY,
    _GAME3_RESULT_ENTRY,
    _GAME1_STARTING_PLAYER_ENTRY,
    _GAME2_STARTING_PLAYER_ENTRY,
    _GAME3_STARTING_PLAYER_ENTRY,
    _GAME1_PLAY_DRAW_ENTRY,
    _GAME2_PLAY_DRAW_ENTRY,
    _GAME3_PLAY_DRAW_ENTRY,
)


def build_player_log_evidence_ledger() -> dict[str, Any]:
    return {
        "object": LEDGER_OBJECT,
        "schema_version": LEDGER_SCHEMA_VERSION,
        "ledger_version": LEDGER_VERSION,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "related_adrs": list(RELATED_ADRS),
        "branch_target": BRANCH_TARGET,
        "privacy": {
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "source_paths_are_repo_relative_or_symbolic": True,
        },
        "vocabulary": {
            "value_sources": list(VALUE_SOURCES),
            "confidence_levels": list(CONFIDENCE_LEVELS),
            "finality_labels": list(FINALITY_LABELS),
            "drift_flags": list(DRIFT_FLAGS),
            "invariant_statuses": list(INVARIANT_STATUSES),
        },
        "output_families": [copy.deepcopy(family) for family in _OUTPUT_FAMILIES],
        "entries": list(iter_ledger_entries()),
    }


def iter_ledger_entries() -> tuple[dict[str, Any], ...]:
    return tuple(copy.deepcopy(entry) for entry in _LEDGER_ENTRIES)


def validate_player_log_evidence_ledger(payload: Mapping[str, Any] | None = None) -> list[str]:
    ledger = build_player_log_evidence_ledger() if payload is None else payload
    if not isinstance(ledger, Mapping):
        return ["ledger:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(ledger, REQUIRED_LEDGER_FIELDS, "ledger"))
    if ledger.get("object") != LEDGER_OBJECT:
        errors.append("ledger:invalid_object")
    if ledger.get("schema_version") != LEDGER_SCHEMA_VERSION:
        errors.append("ledger:invalid_schema_version")
    if ledger.get("ledger_version") != LEDGER_VERSION:
        errors.append("ledger:invalid_ledger_version")
    if ledger.get("source_issue") != SOURCE_ISSUE:
        errors.append("ledger:invalid_source_issue")
    if ledger.get("parent_issue") != PARENT_ISSUE:
        errors.append("ledger:invalid_parent_issue")

    errors.extend(_validate_privacy(ledger.get("privacy")))
    errors.extend(_validate_vocabulary(ledger.get("vocabulary")))
    errors.extend(_validate_output_families(ledger.get("output_families")))

    entries = ledger.get("entries")
    if not isinstance(entries, list):
        errors.append("ledger:entries_not_list")
    else:
        errors.extend(_duplicate_value_errors(entries, key="entry_id", label="entry_id"))
        for index, entry in enumerate(entries):
            for error in validate_ledger_entry(entry if isinstance(entry, Mapping) else {}):
                errors.append(f"ledger:entries[{index}]:{error}")

    errors.extend(_privacy_errors(ledger, "ledger"))
    return _dedupe_errors(errors)


def validate_ledger_entry(entry: Mapping[str, Any]) -> list[str]:
    if not isinstance(entry, Mapping):
        return ["entry:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(entry, REQUIRED_ENTRY_FIELDS, "entry"))
    entry_id = str(entry.get("entry_id") or "")
    if not ENTRY_ID_RE.fullmatch(entry_id):
        errors.append("entry:invalid_entry_id")
    tier = entry.get("tier")
    if isinstance(tier, bool) or not isinstance(tier, int) or tier < 0 or tier > 7:
        errors.append("entry:invalid_tier")
    if entry.get("parser_managed_truth") is not True:
        errors.append("entry:parser_managed_truth_not_true")
    if entry.get("coverage_status") not in FAMILY_STATUSES:
        errors.append("entry:invalid_coverage_status")

    _validate_policy(entry.get("value_source_policy"), VALUE_SOURCES, "value_source_policy", errors)
    _validate_policy(entry.get("confidence_policy"), CONFIDENCE_LEVELS, "confidence_policy", errors)
    _validate_policy(entry.get("finality_policy"), FINALITY_LABELS, "finality_policy", errors)
    _validate_string_list(entry.get("drift_flags"), DRIFT_FLAGS, "drift_flags", errors)

    signal_entries = _signal_entries(entry)
    errors.extend(_duplicate_value_errors(signal_entries, key="signal_id", label="signal_id"))
    for evidence_key in ("direct_evidence", "fallback_evidence"):
        evidence_list = entry.get(evidence_key)
        if not isinstance(evidence_list, list):
            errors.append(f"entry:{evidence_key}_not_list")
            continue
        for index, signal in enumerate(evidence_list):
            errors.extend(
                f"entry:{evidence_key}[{index}]:{error}" for error in _validate_evidence_signal(signal)
            )

    for key in (
        "downstream_surfaces",
        "invariant_checks",
        "degradation_behavior",
        "recommended_review_modules",
        "tests",
        "fixture_refs",
        "notes",
    ):
        if key in entry and not isinstance(entry.get(key), list):
            errors.append(f"entry:{key}_not_list")

    errors.extend(_privacy_errors(entry, "entry"))
    return _dedupe_errors(errors)


def validate_field_evidence(payload: Mapping[str, Any]) -> list[str]:
    if not isinstance(payload, Mapping):
        return ["field_evidence:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(payload, REQUIRED_FIELD_EVIDENCE_FIELDS, "field_evidence"))
    if payload.get("object") != FIELD_EVIDENCE_OBJECT:
        errors.append("field_evidence:invalid_object")
    if payload.get("schema_version") != FIELD_EVIDENCE_SCHEMA_VERSION:
        errors.append("field_evidence:invalid_schema_version")
    if payload.get("ledger_version") != LEDGER_VERSION:
        errors.append("field_evidence:invalid_ledger_version")
    _validate_scalar(payload.get("value_source"), VALUE_SOURCES, "field_evidence:value_source", errors)
    _validate_scalar(payload.get("confidence"), CONFIDENCE_LEVELS, "field_evidence:confidence", errors)
    _validate_scalar(payload.get("finality"), FINALITY_LABELS, "field_evidence:finality", errors)
    _validate_string_list(payload.get("drift_flags"), DRIFT_FLAGS, "field_evidence:drift_flags", errors)
    _validate_scalar(payload.get("invariant_status"), INVARIANT_STATUSES, "field_evidence:invariant_status", errors)
    if payload.get("review_required") is not _field_evidence_review_required(payload):
        errors.append("field_evidence:invalid_review_required")
    errors.extend(_privacy_errors(payload, "field_evidence"))
    return _dedupe_errors(errors)


def _validate_privacy(value: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["ledger:privacy_not_mapping"]
    errors: list[str] = []
    if value.get("raw_private_logs_included") is not False:
        errors.append("ledger:privacy_raw_private_logs_included")
    if value.get("raw_payload_values_included") is not False:
        errors.append("ledger:privacy_raw_payload_values_included")
    if value.get("source_paths_are_repo_relative_or_symbolic") is not True:
        errors.append("ledger:privacy_source_paths_not_repo_relative_or_symbolic")
    return errors


def _validate_vocabulary(value: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["ledger:vocabulary_not_mapping"]
    expected = {
        "value_sources": list(VALUE_SOURCES),
        "confidence_levels": list(CONFIDENCE_LEVELS),
        "finality_labels": list(FINALITY_LABELS),
        "drift_flags": list(DRIFT_FLAGS),
        "invariant_statuses": list(INVARIANT_STATUSES),
    }
    return [
        f"ledger:vocabulary:{key}_mismatch"
        for key, expected_values in expected.items()
        if value.get(key) != expected_values
    ]


def _validate_output_families(value: Any) -> list[str]:
    if not isinstance(value, list):
        return ["ledger:output_families_not_list"]

    errors: list[str] = []
    errors.extend(_duplicate_value_errors(value, key="output_family", label="output_family"))
    families = {item.get("output_family"): item for item in value if isinstance(item, Mapping)}
    required_statuses = {
        "match_identity_and_lifecycle": "seeded_sample",
        "queue_format_rank_event_context": "registered_future",
        "game_level_facts": "seeded_sample",
        "sideboarding_and_deck_state": "registered_future",
        "card_identity_and_gameplay_actions": "registered_future",
        "runtime_health_and_drift_detection": "registered_future",
        "derived_analytics_outputs": "registered_future",
    }
    for family_name, expected_status in required_statuses.items():
        family = families.get(family_name)
        if not isinstance(family, Mapping):
            errors.append(f"ledger:output_family_missing:{family_name}")
            continue
        errors.extend(_missing_required_fields(family, REQUIRED_OUTPUT_FAMILY_FIELDS, f"output_family:{family_name}"))
        if family.get("status") != expected_status:
            errors.append(f"ledger:output_family_status:{family_name}")
        if family.get("status") not in FAMILY_STATUSES:
            errors.append(f"ledger:output_family_invalid_status:{family_name}")
    for index, family in enumerate(value):
        if not isinstance(family, Mapping):
            errors.append(f"ledger:output_families[{index}]:not_mapping")
            continue
        errors.extend(_privacy_errors(family, f"output_family:{family.get('output_family') or index}"))
    return errors


def _validate_evidence_signal(signal: Any) -> list[str]:
    if not isinstance(signal, Mapping):
        return ["evidence:not_mapping"]

    errors: list[str] = []
    errors.extend(_missing_required_fields(signal, REQUIRED_EVIDENCE_FIELDS, "evidence"))
    signal_id = str(signal.get("signal_id") or "")
    if not ENTRY_ID_RE.fullmatch(signal_id):
        errors.append("evidence:invalid_signal_id")
    if not isinstance(signal.get("required_for_final"), bool):
        errors.append("evidence:required_for_final_not_bool")
    _validate_scalar(signal.get("value_source_when_used"), VALUE_SOURCES, "evidence:value_source_when_used", errors)
    _validate_scalar(signal.get("confidence_when_used"), CONFIDENCE_LEVELS, "evidence:confidence_when_used", errors)
    _validate_scalar(signal.get("finality_when_used"), FINALITY_LABELS, "evidence:finality_when_used", errors)
    _validate_string_list(signal.get("allowed_types"), ALLOWED_TYPE_LABELS, "evidence:allowed_types", errors)
    _validate_scalar(signal.get("privacy_class"), EVIDENCE_PRIVACY_CLASSES, "evidence:privacy_class", errors)
    errors.extend(_privacy_errors(signal, "evidence"))
    return errors


def _validate_policy(value: Any, allowed: Sequence[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"entry:{label}_not_mapping")
        return
    for policy_key, policy_value in value.items():
        if policy_value not in allowed:
            errors.append(f"entry:{label}:unknown:{policy_key}:{policy_value}")


def _validate_scalar(value: Any, allowed: Sequence[str], label: str, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{label}:unknown:{value}")


def _validate_string_list(value: Any, allowed: Sequence[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label}_not_list")
        return
    for item in value:
        if item not in allowed:
            errors.append(f"{label}:unknown:{item}")


def _signal_entries(entry: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    signals: list[Mapping[str, Any]] = []
    for key in ("direct_evidence", "fallback_evidence"):
        value = entry.get(key)
        if isinstance(value, list):
            signals.extend(item for item in value if isinstance(item, Mapping))
    return signals


def _duplicate_value_errors(items: Sequence[Any], *, key: str, label: str) -> list[str]:
    seen: set[str] = set()
    duplicate_errors: list[str] = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        value = str(item.get(key) or "").strip()
        if not value:
            continue
        if value in seen:
            duplicate_errors.append(f"duplicate_{label}:{value}")
        seen.add(value)
    return duplicate_errors


def _missing_required_fields(payload: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in fields if field not in payload]


def _field_evidence_review_required(payload: Mapping[str, Any]) -> bool:
    invariant_status = payload.get("invariant_status")
    value_source = payload.get("value_source")
    confidence = payload.get("confidence")
    finality = payload.get("finality")
    return bool(
        invariant_status == "failed"
        or value_source == "conflict"
        or (confidence == "low" and finality in ("final", "reconciled"))
    )


def _privacy_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    _collect_privacy_errors(value, path, errors)
    return errors


def _collect_privacy_errors(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            _collect_privacy_errors(item, f"{path}.{key}", errors)
        return
    if isinstance(value, list | tuple):
        for index, item in enumerate(value):
            _collect_privacy_errors(item, f"{path}[{index}]", errors)
        return
    if not isinstance(value, str):
        return

    if ABSOLUTE_PATH_RE.match(value):
        errors.append(f"privacy:absolute_path:{path}")
    if FORBIDDEN_TEXT_RE.search(value):
        errors.append(f"privacy:forbidden_text:{path}")


def _dedupe_errors(errors: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(errors))
