import json
import re
from pathlib import Path

from mythic_edge_parser.app import sheet_exports, sheet_schema

APP_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "google_apps_script" / "Code.gs"

RUNTIME_METADATA_FIELDS = ("event_family", "event_type", "scope")

ACTION_ROW_FIELDS = (
    "generated_at",
    "match_id",
    "game_number",
    "turn_number",
    "timestamp",
    "action_type",
    "cast_mode",
    "grp_id",
    "card_name",
    "display_name",
    "resolution_status",
    "actor_relation",
    "from_zone_type",
    "to_zone_type",
    "summary",
)

DECK_SNAPSHOT_ROW_FIELDS = (
    "generated_at",
    "submitted_at",
    "match_id",
    "deck_signature",
    "deck_name",
    "deck_match_mode",
    "deck_format",
    "section",
    "arena_id",
    "count",
    "card_name",
    "rarity",
    "set",
    "type_line",
    "colors",
    "owned_copies",
    "missing_copies",
)

COLLECTION_SNAPSHOT_ROW_FIELDS = (
    "generated_at",
    "collection_available",
    "inventory_available",
    "owned_unique_cards",
    "owned_total_card_copies",
    "owned_by_rarity",
    "inventory_gold",
    "inventory_gems",
    "wildcards_common",
    "wildcards_uncommon",
    "wildcards_rare",
    "wildcards_mythic",
    "active_deck_missing_by_rarity",
    "active_deck_completion_rate",
    "wanted_cards",
)

PARSER_STATUS_ROW_FIELDS = (
    "updated_at",
    "status",
    "current_match_id",
    "current_game_number",
    "current_player_team",
    "last_event_kind",
    "last_event_at",
    "webhook_successes",
    "webhook_failures",
    "event_failures",
    "router_failures",
    "active_deck_signature",
    "active_deck_name",
    "active_match_action_count",
)

CARD_PERFORMANCE_ROW_FIELDS = (
    "generated_at",
    "card_key",
    "grp_id",
    "card_name",
    "display_name",
    "resolution_status",
    "layout",
    "card_faces",
    "games_seen",
    "seen_in_game_games",
    "seen_in_game_win_rate",
    "opening_hand_games",
    "opening_hand_win_rate",
    "cast_games",
    "cast_win_rate",
    "postboard_cast_games",
    "postboard_cast_win_rate",
    "mulliganed_away_games",
    "mulligan_tax",
    "top_matchups",
    "top_packages",
)

ROW_FIELDS_BY_FAMILY = {
    sheet_schema.ACTION_LOG_FAMILY: ACTION_ROW_FIELDS,
    sheet_schema.DECK_SNAPSHOT_FAMILY: DECK_SNAPSHOT_ROW_FIELDS,
    sheet_schema.COLLECTION_SNAPSHOT_FAMILY: COLLECTION_SNAPSHOT_ROW_FIELDS,
    sheet_schema.PARSER_STATUS_FAMILY: PARSER_STATUS_ROW_FIELDS,
    sheet_schema.CARD_PERFORMANCE_FAMILY: CARD_PERFORMANCE_ROW_FIELDS,
}

APP_SCRIPT_BUILD_OBJECT_BY_FAMILY = {
    sheet_schema.ACTION_LOG_FAMILY: "buildActionLogRowObject_",
    sheet_schema.DECK_SNAPSHOT_FAMILY: "buildDeckSnapshotRowObject_",
    sheet_schema.COLLECTION_SNAPSHOT_FAMILY: "buildCollectionSnapshotRowObject_",
    sheet_schema.PARSER_STATUS_FAMILY: "buildParserStatusRowObject_",
    sheet_schema.CARD_PERFORMANCE_FAMILY: "buildCardPerformanceRowObject_",
}


def _action_payload(*, entries: list[object] | None = None, generated_at: str = "2026-05-06T04:14:36+00:00"):
    return {
        "generated_at": generated_at,
        "entries": entries
        if entries is not None
        else [
            {
                "match_id": "match-1",
                "game_number": 1,
                "turn_number": 3,
                "timestamp": "2026-05-06T00:08:33+00:00",
                "action_type": "spell_cast",
                "cast_mode": "normal",
                "grp_id": 97547,
                "card_name": "Duress",
                "display_name": "Duress",
                "resolution_status": "confirmed",
                "actor_relation": "local",
                "from_zone_type": "ZoneType_Hand",
                "to_zone_type": "ZoneType_Stack",
                "summary": "local cast Duress from hand to stack",
            }
        ],
    }


def _deck_payload(*, mainboard: object | None = None, sideboard: object | None = None):
    return {
        "generated_at": "2026-05-06T04:14:48+00:00",
        "submitted_at": "2026-05-06T00:10:40+00:00",
        "match_id": "match-1",
        "signature": "deck-signature-1",
        "matched_decks": [
            {
                "name": "Azban Midrange",
                "match_mode": "same_pool_sideboarded",
                "format": "TraditionalStandard",
            }
        ],
        "mainboard": mainboard
        if mainboard is not None
        else [
            {
                "arena_id": 77508,
                "count": 2,
                "section": "mainboard",
                "name": "Duress",
                "rarity": "common",
                "set": "M19",
                "type_line": "Sorcery",
                "colors": ["B"],
                "owned_copies": 4,
                "missing_copies": 0,
            }
        ],
        "sideboard": sideboard if sideboard is not None else [],
    }


def _collection_payload(**overrides):
    payload = {
        "generated_at": "2026-05-06T04:14:48+00:00",
        "collection_available": True,
        "inventory_available": True,
        "owned_unique_cards": 100,
        "owned_total_card_copies": 400,
        "owned_by_rarity": {"rare": 20},
        "inventory": {
            "gold": 1000,
            "gems": 250,
            "wildcards_common": 10,
            "wildcards_uncommon": 8,
            "wildcards_rare": 2,
            "wildcards_mythic": 1,
        },
        "active_deck_missing_by_rarity": {"rare": 1},
        "active_deck_completion": {"completion_rate": 0.95},
        "wanted_cards": ["Card A"],
    }
    payload.update(overrides)
    return payload


def _status_payload(**overrides):
    payload = {
        "updated_at": "2026-05-06T04:14:48+00:00",
        "status": "running",
        "current_match_id": "match-1",
        "current_game_number": 1,
        "current_player_team": 1,
        "last_event_kind": "GameState",
        "last_event_at": "2026-05-06T00:14:48+00:00",
        "webhook_successes": 3,
        "webhook_failures": 0,
        "event_failures": 0,
        "router_failures": 0,
        "active_deck_signature": "deck-signature-1",
        "active_deck_name": "Azban Midrange",
        "active_match_action_count": 1,
    }
    payload.update(overrides)
    return payload


def _card_performance_payload(*, cards: list[object] | None = None, generated_at: str = "2026-05-06T04:14:48+00:00"):
    return {
        "generated_at": generated_at,
        "cards": cards
        if cards is not None
        else [
            {
                "card_key": "grp:77508",
                "grp_id": 77508,
                "card_name": "Duress",
                "display_name": "Duress",
                "resolution_status": "exact_numeric_match",
                "layout": "normal",
                "card_faces": [],
                "games_seen": 1,
                "seen_in_game_games": 1,
                "seen_in_game_win_rate": 1.0,
                "opening_hand_games": 0,
                "opening_hand_win_rate": "",
                "cast_games": 1,
                "cast_win_rate": 1.0,
                "postboard_cast_games": 0,
                "postboard_cast_win_rate": "",
                "mulliganed_away_games": 0,
                "mulligan_tax": "",
                "top_matchups": [],
                "top_packages": [],
            }
        ],
    }


def _runtime_rows_by_family() -> dict[str, dict[str, object]]:
    sheet_exports.reset_sheet_export_state()
    rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(),
        deck_payload=_deck_payload(),
        collection_payload=_collection_payload(),
        status_payload=_status_payload(),
        card_performance_payload=_card_performance_payload(),
    )
    return {str(row["event_family"]): row for row in rows}


def _apps_script_data_keys(function_name: str) -> set[str]:
    source = APP_SCRIPT_PATH.read_text(encoding="utf-8")
    match = re.search(
        rf"function {re.escape(function_name)}\(data\) \{{(?P<body>.*?)^\}}",
        source,
        re.DOTALL | re.MULTILINE,
    )
    assert match is not None
    body = match.group("body")
    dot_keys = set(re.findall(r"\bdata\.([A-Za-z_][A-Za-z0-9_]*)", body))
    bracket_keys = set(re.findall(r'data\["([^"]+)"\]', body))
    return dot_keys | bracket_keys


def test_safe_int_ignores_bool_values() -> None:
    assert sheet_exports._safe_int(True) == ""
    assert sheet_exports._safe_int(False) == ""


def test_safe_int_preserves_current_int_conversion_behavior() -> None:
    assert sheet_exports._safe_int(3) == 3
    assert sheet_exports._safe_int(" 4 ") == 4
    assert sheet_exports._safe_int(3.8) == 3
    assert sheet_exports._safe_int(None) == ""
    assert sheet_exports._safe_int("not-a-number") == ""


def test_reset_sheet_export_state_clears_fingerprints_action_keys_and_json_cache() -> None:
    sheet_exports.EXPORT_STATE.posted_action_keys.add("action-key")
    sheet_exports.EXPORT_STATE.last_deck_snapshot_fingerprint = "deck"
    sheet_exports.EXPORT_STATE.last_collection_snapshot_fingerprint = "collection"
    sheet_exports.EXPORT_STATE.last_parser_status_fingerprint = "status"
    sheet_exports.EXPORT_STATE.last_card_performance_fingerprint = "cards"
    sheet_exports._JSON_DICT_CACHE[("payload.json", 1)] = {"cached": True}

    sheet_exports.reset_sheet_export_state()

    assert sheet_exports.EXPORT_STATE.posted_action_keys == set()
    assert sheet_exports.EXPORT_STATE.last_deck_snapshot_fingerprint == ""
    assert sheet_exports.EXPORT_STATE.last_collection_snapshot_fingerprint == ""
    assert sheet_exports.EXPORT_STATE.last_parser_status_fingerprint == ""
    assert sheet_exports.EXPORT_STATE.last_card_performance_fingerprint == ""
    assert sheet_exports._JSON_DICT_CACHE == {}


def test_load_json_dict_handles_missing_invalid_non_dict_cache_reuse_and_refresh(tmp_path, monkeypatch) -> None:
    sheet_exports.reset_sheet_export_state()

    missing_path = tmp_path / "missing.json"
    assert sheet_exports._load_json_dict(missing_path) == {}

    payload_path = tmp_path / "payload.json"
    payload_path.write_text("{not json", encoding="utf-8")
    assert sheet_exports._load_json_dict(payload_path) == {}
    assert sheet_exports._JSON_DICT_CACHE == {}

    payload_path.write_text("[1, 2, 3]", encoding="utf-8")
    assert sheet_exports._load_json_dict(payload_path) == {}

    cache_key = [(str(payload_path), 1)]
    monkeypatch.setattr(sheet_exports, "_path_cache_key", lambda _path: cache_key[-1])

    payload_path.write_text(json.dumps({"value": 1}), encoding="utf-8")
    first_payload = sheet_exports._load_json_dict(payload_path)
    assert first_payload == {"value": 1}

    payload_path.write_text(json.dumps({"value": 2}), encoding="utf-8")
    assert sheet_exports._load_json_dict(payload_path) is first_payload

    cache_key.append((str(payload_path), 2))
    assert sheet_exports._load_json_dict(payload_path) == {"value": 2}
    assert list(sheet_exports._JSON_DICT_CACHE) == [(str(payload_path), 2)]


def test_collect_runtime_sheet_rows_honors_disabled_flags_without_loading_defaults(monkeypatch) -> None:
    def fail_load(*_args, **_kwargs):
        raise AssertionError("disabled family loaded a default artifact")

    monkeypatch.setattr(sheet_exports, "load_active_match_actions_payload", fail_load)
    monkeypatch.setattr(sheet_exports, "load_card_performance_payload", fail_load)
    monkeypatch.setattr(sheet_exports, "_load_json_dict", fail_load)

    rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(),
        deck_payload=_deck_payload(),
        collection_payload=_collection_payload(),
        status_payload=_status_payload(),
        card_performance_payload=_card_performance_payload(),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )

    assert rows == []


def test_runtime_rows_include_schema_metadata_and_exact_contract_fields() -> None:
    rows_by_family = _runtime_rows_by_family()

    assert list(rows_by_family) == [
        "ActionLogRow",
        "DeckSnapshotRow",
        "CollectionSnapshotRow",
        "ParserStatusRow",
        "CardPerformanceRow",
    ]

    for family, row in rows_by_family.items():
        spec = sheet_schema.runtime_sheet_spec(family)
        assert row["event_family"] == spec.family
        assert row["event_type"] == spec.event_type
        assert row["scope"] == spec.scope
        assert set(row) == set(RUNTIME_METADATA_FIELDS + ROW_FIELDS_BY_FAMILY[family])


def test_runtime_rows_cover_apps_script_consumed_snake_case_fields() -> None:
    rows_by_family = _runtime_rows_by_family()

    for family, row in rows_by_family.items():
        consumed_keys = _apps_script_data_keys(APP_SCRIPT_BUILD_OBJECT_BY_FAMILY[family])
        assert consumed_keys <= set(row)


def test_collection_snapshot_accepts_nested_wildcard_payload_shape() -> None:
    sheet_exports.reset_sheet_export_state()

    rows = sheet_exports.collect_runtime_sheet_rows(
        collection_payload=_collection_payload(
            inventory={
                "gold": 1000,
                "gems": 250,
                "wildcards": {
                    "common": 10,
                    "uncommon": 8,
                    "rare": 2,
                    "mythic": 1,
                },
            },
        ),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["wildcards_common"] == 10
    assert row["wildcards_uncommon"] == 8
    assert row["wildcards_rare"] == 2
    assert row["wildcards_mythic"] == 1


def test_collect_runtime_sheet_rows_emits_new_families_once() -> None:
    sheet_exports.reset_sheet_export_state()

    rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload={
            "generated_at": "2026-05-06T04:14:36+00:00",
            "entries": [
                {
                    "match_id": "match-1",
                    "game_number": 1,
                    "turn_number": 3,
                    "timestamp": "2026-05-06T00:08:33+00:00",
                    "action_type": "spell_cast",
                    "cast_mode": "adventure_face",
                    "grp_id": 97547,
                    "card_name": "Mosswood Dreadknight // Dread Whispers",
                    "display_name": "Mosswood Dreadknight // Dread Whispers",
                    "resolution_status": "confirmed",
                    "actor_relation": "local",
                    "from_zone_type": "ZoneType_Hand",
                    "to_zone_type": "ZoneType_Stack",
                    "summary": "local cast Mosswood Dreadknight // Dread Whispers from hand to stack",
                }
            ],
        },
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        collection_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "collection_available": True,
            "inventory_available": True,
            "owned_unique_cards": 100,
            "owned_total_card_copies": 400,
            "owned_by_rarity": {"rare": 20},
            "inventory": {"gold": 1000, "gems": 250},
            "active_deck_missing_by_rarity": {"rare": 1},
            "active_deck_completion": {"completion_rate": 0.95},
            "wanted_cards": ["Card A"],
        },
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        card_performance_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "cards": [
                {
                    "card_key": "grp:77508",
                    "grp_id": 77508,
                    "card_name": "Duress",
                    "display_name": "Duress",
                    "resolution_status": "exact_numeric_match",
                    "layout": "normal",
                    "card_faces": [],
                    "games_seen": 1,
                    "seen_in_game_games": 1,
                    "seen_in_game_win_rate": 1.0,
                    "opening_hand_games": 0,
                    "opening_hand_win_rate": "",
                    "cast_games": 1,
                    "cast_win_rate": 1.0,
                    "postboard_cast_games": 0,
                    "postboard_cast_win_rate": "",
                    "mulliganed_away_games": 0,
                    "mulligan_tax": "",
                    "top_matchups": [],
                    "top_packages": [],
                }
            ],
        },
    )

    assert {row["event_family"] for row in rows} == {
        "ActionLogRow",
        "DeckSnapshotRow",
        "CollectionSnapshotRow",
        "ParserStatusRow",
        "CardPerformanceRow",
    }

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload={
            "generated_at": "2026-05-06T04:14:36+00:00",
            "entries": [
                {
                    "match_id": "match-1",
                    "game_number": 1,
                    "timestamp": "2026-05-06T00:08:33+00:00",
                    "action_type": "spell_cast",
                    "grp_id": 97547,
                    "from_zone_type": "ZoneType_Hand",
                    "to_zone_type": "ZoneType_Stack",
                }
            ],
        },
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        collection_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "collection_available": True,
            "inventory_available": True,
            "owned_unique_cards": 100,
            "owned_total_card_copies": 400,
            "owned_by_rarity": {"rare": 20},
            "inventory": {"gold": 1000, "gems": 250},
            "active_deck_missing_by_rarity": {"rare": 1},
            "active_deck_completion": {"completion_rate": 0.95},
            "wanted_cards": ["Card A"],
        },
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        card_performance_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "cards": [
                {
                    "card_key": "grp:77508",
                    "grp_id": 77508,
                    "card_name": "Duress",
                    "display_name": "Duress",
                    "resolution_status": "exact_numeric_match",
                    "layout": "normal",
                    "card_faces": [],
                    "games_seen": 1,
                    "seen_in_game_games": 1,
                    "seen_in_game_win_rate": 1.0,
                    "opening_hand_games": 0,
                    "opening_hand_win_rate": "",
                    "cast_games": 1,
                    "cast_win_rate": 1.0,
                    "postboard_cast_games": 0,
                    "postboard_cast_win_rate": "",
                    "mulliganed_away_games": 0,
                    "mulligan_tax": "",
                    "top_matchups": [],
                    "top_packages": [],
                }
            ],
        },
    )

    assert repeated_rows == []


def test_action_row_dedupe_uses_key_fields_and_ignores_non_key_fields() -> None:
    sheet_exports.reset_sheet_export_state()
    base_entry = {
        "match_id": "match-1",
        "game_number": 1,
        "turn_number": 3,
        "timestamp": "2026-05-06T00:08:33+00:00",
        "action_type": "spell_cast",
        "cast_mode": "normal",
        "grp_id": 97547,
        "card_name": "Duress",
        "display_name": "Duress",
        "resolution_status": "confirmed",
        "actor_relation": "local",
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "summary": "local cast Duress from hand to stack",
    }

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(entries=[base_entry]),
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1

    non_key_change = {
        **base_entry,
        "turn_number": 4,
        "cast_mode": "adventure_face",
        "card_name": "Mosswood Dreadknight",
        "summary": "changed summary",
    }
    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(entries=[non_key_change], generated_at="2026-05-06T04:15:36+00:00"),
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert repeated_rows == []

    key_change = {**base_entry, "to_zone_type": "ZoneType_Battlefield"}
    changed_rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(entries=[key_change], generated_at="2026-05-06T04:16:36+00:00"),
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(changed_rows) == 1
    assert changed_rows[0]["to_zone_type"] == "ZoneType_Battlefield"


def test_non_dict_entries_in_accepted_list_sections_are_skipped() -> None:
    sheet_exports.reset_sheet_export_state()

    rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload=_action_payload(entries=["bad-action", _action_payload()["entries"][0]]),
        deck_payload=_deck_payload(mainboard=["bad-card", _deck_payload()["mainboard"][0]], sideboard="not-a-list"),
        card_performance_payload=_card_performance_payload(cards=[None, _card_performance_payload()["cards"][0]]),
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
    )

    assert [row["event_family"] for row in rows] == [
        "ActionLogRow",
        "DeckSnapshotRow",
        "CardPerformanceRow",
    ]


def test_collect_runtime_sheet_rows_reposts_parser_status_when_meaningful_values_change() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1
    assert first_rows[0]["event_family"] == "ParserStatusRow"

    second_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 2,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert second_rows == []


def test_collect_runtime_sheet_rows_reposts_parser_status_when_core_context_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1

    second_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 2,
            "current_player_team": 1,
            "last_event_kind": "GameResult",
            "last_event_at": "2026-05-06T00:15:48+00:00",
            "webhook_successes": 30,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 9,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(second_rows) == 1
    assert second_rows[0]["current_game_number"] == 2


def test_collect_runtime_sheet_rows_does_not_repost_deck_snapshot_when_only_generated_at_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        post_action_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1
    assert first_rows[0]["event_family"] == "DeckSnapshotRow"

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        deck_payload={
            "generated_at": "2026-05-06T04:15:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        post_action_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert repeated_rows == []


def test_collection_snapshot_dedupe_ignores_generated_at_and_reposts_non_transient_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        collection_payload=_collection_payload(),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        collection_payload=_collection_payload(generated_at="2026-05-06T04:15:48+00:00"),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert repeated_rows == []

    changed_rows = sheet_exports.collect_runtime_sheet_rows(
        collection_payload=_collection_payload(
            generated_at="2026-05-06T04:16:48+00:00",
            owned_unique_cards=101,
        ),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(changed_rows) == 1
    assert changed_rows[0]["owned_unique_cards"] == 101


def test_card_performance_dedupe_ignores_generated_at_and_reposts_non_transient_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        card_performance_payload=_card_performance_payload(),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
    )
    assert len(first_rows) == 1

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        card_performance_payload=_card_performance_payload(generated_at="2026-05-06T04:15:48+00:00"),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
    )
    assert repeated_rows == []

    changed_card = {**_card_performance_payload()["cards"][0], "games_seen": 2}
    changed_rows = sheet_exports.collect_runtime_sheet_rows(
        card_performance_payload=_card_performance_payload(
            cards=[changed_card],
            generated_at="2026-05-06T04:16:48+00:00",
        ),
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
    )
    assert len(changed_rows) == 1
    assert changed_rows[0]["games_seen"] == 2
