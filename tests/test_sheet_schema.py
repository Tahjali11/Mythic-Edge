import re
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from mythic_edge_parser.app import sheet_schema
from mythic_edge_parser.app.models import MatchSummary

APP_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "google_apps_script" / "Code.gs"


EXPECTED_MATCH_LOG_SYNC_FIELDS = (
    "Date",
    "My Rank",
    "G1 Play / Draw",
    "Game 1 Result",
    "G2 Play / Draw",
    "Game 2 Result",
    "G3 Play / Draw",
    "Game 3 Result",
    "Games Won",
    "Games Lost",
    "Match Win?",
    "Total Games",
    "Match Win Flag",
    "Game Win %",
    "MTGA Match ID",
    "MTGA Format",
    "MTGA Event ID",
    "MTGA Queue Type",
    "G1 Mulligans",
    "G2 Mulligans",
    "G3 Mulligans",
    "G1 Turn Count",
    "G2 Turn Count",
    "G3 Turn Count",
    "MGTA Start Time",
    "MTGA End Time",
    "MTGA Rank Raw",
    "MTGA Mulligans",
    "MTGA Sideboard Entered",
    "MTGA Submit Deck Seen",
    "MTGA Sync Status",
)

EXPECTED_GAME_LOG_SYNC_FIELDS = (
    "Date",
    "MTGA Format",
    "My Rank",
    "MTGA Match ID",
    "Game Number",
    "Pre / Postboard",
    "Play / Draw",
    "Mulligans",
    "Opening Hand Size",
    "Opening Hand",
    "Mulliganed Away",
    "Game Result",
    "Turn Count",
    "Game Duration",
    "MTGA Event ID",
    "MTGA Queue Type",
)


def _apps_script_return_object_keys(function_name: str) -> tuple[str, ...]:
    source = APP_SCRIPT_PATH.read_text(encoding="utf-8")
    match = re.search(
        rf"function {re.escape(function_name)}\(data\) \{{.*?return \{{(?P<body>.*?)^\s*\}};",
        source,
        re.DOTALL | re.MULTILINE,
    )
    assert match is not None
    return tuple(re.findall(r'^\s*"([^"]+)":', match.group("body"), re.MULTILINE))


def _apps_script_landing_headers(schema_key: str) -> tuple[str, ...]:
    source = APP_SCRIPT_PATH.read_text(encoding="utf-8")
    match = re.search(
        rf"^\s*{re.escape(schema_key)}:\s*\[(?P<body>.*?)^\s*\],",
        source,
        re.DOTALL | re.MULTILINE,
    )
    assert match is not None
    return tuple(re.findall(r'^\s*"([^"]+)",?$', match.group("body"), re.MULTILINE))


def test_runtime_sheet_spec_is_frozen_and_slotted() -> None:
    spec = sheet_schema.RuntimeSheetSpec(
        family="ExampleRow",
        event_type="example_row",
        scope="Runtime",
        headers=("Generated At",),
    )

    assert not hasattr(spec, "__dict__")
    with pytest.raises(FrozenInstanceError):
        setattr(spec, "scope", "Match")


@pytest.mark.parametrize(
    ("family", "event_type", "scope", "headers"),
    (
        ("ActionLogRow", "action_log_row", "Match", sheet_schema.ACTION_LOG_HEADERS),
        ("DeckSnapshotRow", "deck_snapshot_row", "Deck", sheet_schema.DECK_SNAPSHOT_HEADERS),
        (
            "CollectionSnapshotRow",
            "collection_snapshot_row",
            "Collection",
            sheet_schema.COLLECTION_SNAPSHOT_HEADERS,
        ),
        ("ParserStatusRow", "parser_status_row", "Runtime", sheet_schema.PARSER_STATUS_HEADERS),
        ("CardPerformanceRow", "card_performance_row", "Card", sheet_schema.CARD_PERFORMANCE_HEADERS),
    ),
)
def test_runtime_sheet_specs_return_expected_contract(
    family: str,
    event_type: str,
    scope: str,
    headers: tuple[str, ...],
) -> None:
    spec = sheet_schema.runtime_sheet_spec(family)

    assert spec.family == family
    assert spec.event_type == event_type
    assert spec.scope == scope
    assert spec.headers == headers
    assert sheet_schema.runtime_sheet_headers(family) == headers


def test_runtime_sheet_spec_registry_keys_match_spec_families() -> None:
    assert set(sheet_schema.RUNTIME_SHEET_SPECS) == {
        "ActionLogRow",
        "DeckSnapshotRow",
        "CollectionSnapshotRow",
        "ParserStatusRow",
        "CardPerformanceRow",
    }
    assert all(family == spec.family for family, spec in sheet_schema.RUNTIME_SHEET_SPECS.items())


def test_runtime_sheet_spec_returns_expected_action_log_contract() -> None:
    spec = sheet_schema.runtime_sheet_spec(sheet_schema.ACTION_LOG_FAMILY)

    assert spec.family == "ActionLogRow"
    assert spec.event_type == "action_log_row"
    assert spec.scope == "Match"
    assert spec.headers == sheet_schema.ACTION_LOG_HEADERS


def test_sync_field_registry_maps_only_known_row_kinds() -> None:
    assert sheet_schema.SYNC_FIELDS_BY_ROW_KIND == {
        "match_log": sheet_schema.MATCH_LOG_SYNC_FIELDS,
        "game_log": sheet_schema.GAME_LOG_SYNC_FIELDS,
    }


def test_match_log_sync_fields_order_is_stable() -> None:
    assert sheet_schema.MATCH_LOG_SYNC_FIELDS == EXPECTED_MATCH_LOG_SYNC_FIELDS


def test_game_log_sync_fields_order_is_stable() -> None:
    assert sheet_schema.GAME_LOG_SYNC_FIELDS == EXPECTED_GAME_LOG_SYNC_FIELDS


def test_sync_fields_returns_expected_game_log_contract() -> None:
    assert sheet_schema.sync_fields("game_log") == sheet_schema.GAME_LOG_SYNC_FIELDS


def test_sync_fields_returns_expected_match_log_contract() -> None:
    assert sheet_schema.sync_fields("match_log") == sheet_schema.MATCH_LOG_SYNC_FIELDS


def test_lookup_helpers_raise_key_error_for_unknown_values() -> None:
    with pytest.raises(KeyError):
        sheet_schema.runtime_sheet_spec("UnknownRow")
    with pytest.raises(KeyError):
        sheet_schema.runtime_sheet_headers("UnknownRow")
    with pytest.raises(KeyError):
        sheet_schema.sync_fields("unknown_log")


def test_apps_script_match_log_field_map_matches_python_sync_fields() -> None:
    assert _apps_script_return_object_keys("buildMatchLogFieldMap_") == sheet_schema.MATCH_LOG_SYNC_FIELDS


def test_apps_script_game_log_field_map_matches_python_sync_fields() -> None:
    assert _apps_script_return_object_keys("buildGameLogFieldMap_") == sheet_schema.GAME_LOG_SYNC_FIELDS


@pytest.mark.parametrize(
    ("schema_key", "headers"),
    (
        ("actionLog", sheet_schema.ACTION_LOG_HEADERS),
        ("deckSnapshot", sheet_schema.DECK_SNAPSHOT_HEADERS),
        ("collectionSnapshot", sheet_schema.COLLECTION_SNAPSHOT_HEADERS),
        ("parserStatus", sheet_schema.PARSER_STATUS_HEADERS),
        ("cardPerformance", sheet_schema.CARD_PERFORMANCE_HEADERS),
    ),
)
def test_apps_script_landing_headers_match_python_runtime_headers(
    schema_key: str,
    headers: tuple[str, ...],
) -> None:
    assert _apps_script_landing_headers(schema_key) == headers


@pytest.mark.parametrize(
    ("function_name", "headers"),
    (
        ("buildActionLogRowObject_", sheet_schema.ACTION_LOG_HEADERS),
        ("buildDeckSnapshotRowObject_", sheet_schema.DECK_SNAPSHOT_HEADERS),
        ("buildCollectionSnapshotRowObject_", sheet_schema.COLLECTION_SNAPSHOT_HEADERS),
        ("buildParserStatusRowObject_", sheet_schema.PARSER_STATUS_HEADERS),
        ("buildCardPerformanceRowObject_", sheet_schema.CARD_PERFORMANCE_HEADERS),
    ),
)
def test_apps_script_runtime_row_object_keys_cover_runtime_headers(
    function_name: str,
    headers: tuple[str, ...],
) -> None:
    assert _apps_script_return_object_keys(function_name) == headers


def test_legacy_mgta_start_time_spelling_is_preserved_across_schema_surfaces() -> None:
    row = MatchSummary(match_id="legacy-spelling").to_match_log_row()

    assert "MGTA Start Time" in sheet_schema.MATCH_LOG_SYNC_FIELDS
    assert "MGTA Start Time" in row
    assert "MGTA Start Time" in _apps_script_return_object_keys("buildMatchLogFieldMap_")
