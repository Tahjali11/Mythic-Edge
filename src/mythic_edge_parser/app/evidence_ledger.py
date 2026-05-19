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
        "seed_fields": ["match_id"],
        "future_fields": [
            "match_started_at",
            "match_finished_at",
            "match_winner_team",
            "match_result",
            "match_sync_status",
        ],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ],
        "notes": ["Only match_id is fully mapped in issue #128."],
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
        "status": "registered_future",
        "description": "Game result, play/draw, mulligan, turn, and opening-hand parser outputs.",
        "seed_fields": [],
        "future_fields": ["game_result", "play_draw", "mulligans", "turn_count", "opening_hand"],
        "owner_modules": [
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ],
        "notes": ["Registered for later field-level provenance mapping."],
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
    "notes": ["Seed entry only; broader Tier 1 coverage belongs to later issues."],
}

_LEDGER_ENTRIES: tuple[dict[str, Any], ...] = (_MATCH_ID_ENTRY,)


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
        "game_level_facts": "registered_future",
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
