from mythic_edge_parser.app import sheet_schema


def test_runtime_sheet_spec_returns_expected_action_log_contract() -> None:
    spec = sheet_schema.runtime_sheet_spec(sheet_schema.ACTION_LOG_FAMILY)

    assert spec.family == "ActionLogRow"
    assert spec.event_type == "action_log_row"
    assert spec.scope == "Match"
    assert spec.headers == sheet_schema.ACTION_LOG_HEADERS


def test_sync_fields_returns_expected_game_log_contract() -> None:
    assert sheet_schema.sync_fields("game_log") == sheet_schema.GAME_LOG_SYNC_FIELDS
