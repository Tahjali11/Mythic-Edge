import re
from pathlib import Path

from mythic_edge_parser.app import sheet_schema

APP_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "google_apps_script" / "Code.gs"


def _apps_script_field_map_keys(function_name: str) -> set[str]:
    source = APP_SCRIPT_PATH.read_text(encoding="utf-8")
    match = re.search(
        rf"function {re.escape(function_name)}\(data\) \{{.*?return \{{(?P<body>.*?)^\s*\}};",
        source,
        re.DOTALL | re.MULTILINE,
    )
    assert match is not None
    return set(re.findall(r'^\s*"([^"]+)":', match.group("body"), re.MULTILINE))


def test_runtime_sheet_spec_returns_expected_action_log_contract() -> None:
    spec = sheet_schema.runtime_sheet_spec(sheet_schema.ACTION_LOG_FAMILY)

    assert spec.family == "ActionLogRow"
    assert spec.event_type == "action_log_row"
    assert spec.scope == "Match"
    assert spec.headers == sheet_schema.ACTION_LOG_HEADERS


def test_sync_fields_returns_expected_game_log_contract() -> None:
    assert sheet_schema.sync_fields("game_log") == sheet_schema.GAME_LOG_SYNC_FIELDS


def test_sync_fields_returns_expected_match_log_contract() -> None:
    assert sheet_schema.sync_fields("match_log") == sheet_schema.MATCH_LOG_SYNC_FIELDS


def test_apps_script_match_log_field_map_matches_python_sync_fields() -> None:
    assert _apps_script_field_map_keys("buildMatchLogFieldMap_") == set(sheet_schema.MATCH_LOG_SYNC_FIELDS)


def test_apps_script_game_log_field_map_matches_python_sync_fields() -> None:
    assert _apps_script_field_map_keys("buildGameLogFieldMap_") == set(sheet_schema.GAME_LOG_SYNC_FIELDS)
