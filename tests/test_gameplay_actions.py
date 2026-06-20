import json
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app import gameplay_actions, grp_id_catalog, state
from mythic_edge_parser.events import EventMetadata, GameStateEvent


def _reset_gameplay_state() -> None:
    gameplay_actions.reset_gameplay_actions_state()
    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}
    state.reset_runtime_state()


def _patch_status_writer(monkeypatch) -> None:
    monkeypatch.setattr(gameplay_actions, "update_" + "runtime_" + "status", lambda **_: None)


def test_reset_gameplay_actions_state_clears_shared_runtime_state() -> None:
    gameplay_actions._GAME_STATES[("match-reset", 1)] = gameplay_actions.GameplayGameState(
        match_id="match-reset",
        game_number=1,
    )
    gameplay_actions._MATCH_ACTIONS["match-reset"] = [{"action_type": "spell_cast"}]
    gameplay_actions._MATCH_ACTION_KEYS["match-reset"] = {"seen-key"}
    gameplay_actions._DIRTY_MATCH_IDS.add("match-reset")
    gameplay_actions._JSON_DICT_CACHE[("cache-path", 1)] = {"object": "cached"}
    gameplay_actions._ACTIVE_DECK_INDEX = gameplay_actions.ActiveDeckIdentityIndex(
        cache_key=("deck-path", 1),
        payload={"mainboard": []},
        exact_names_by_arena_id={1001: "Forest"},
        all_names={"Forest"},
    )

    gameplay_actions.reset_gameplay_actions_state()

    assert gameplay_actions._GAME_STATES == {}
    assert gameplay_actions._MATCH_ACTIONS == {}
    assert gameplay_actions._MATCH_ACTION_KEYS == {}
    assert gameplay_actions._DIRTY_MATCH_IDS == set()
    assert gameplay_actions._JSON_DICT_CACHE == {}
    assert gameplay_actions._ACTIVE_DECK_INDEX is None


def _patch_gameplay_paths(tmp_path: Path, monkeypatch) -> Path:
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    return status_root


def test_match_action_filename_uses_safe_stem_without_changing_payload_match_id(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = _patch_gameplay_paths(tmp_path, monkeypatch)
    raw_match_id = r"..\outside/match:evil"
    gameplay_actions._MATCH_ACTIONS[raw_match_id] = []

    gameplay_actions._write_match_actions(raw_match_id)

    action_root = status_root / "actions"
    action_files = list(action_root.glob("*.json"))
    markdown_files = list(action_root.glob("*.md"))
    assert len(action_files) == 1
    assert len(markdown_files) == 1
    assert action_files[0].parent == action_root
    assert markdown_files[0].parent == action_root
    for path in (*action_files, *markdown_files):
        assert ".." not in path.name
        assert ":" not in path.name
        assert "/" not in path.name
        assert "\\" not in path.name
    assert not (tmp_path / "outside").exists()

    payload = json.loads(action_files[0].read_text(encoding="utf-8"))
    assert payload["match_id"] == raw_match_id
    assert gameplay_actions.load_active_match_actions_payload(raw_match_id)["match_id"] == raw_match_id


def test_gameplay_actions_emit_turn_land_and_spell_events(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "1001": {"name": "Shoot the Sheriff"},
                    "2002": {"name": "Forest"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 0, tzinfo=UTC), b"raw-1"),
        {
            "game_state_id": 1,
            "identity": {
                "match_id": "match-1",
                "game_number": 1,
                "turn_number": 1,
                "active_player_seat_id": 1,
                "phase": "Phase_Beginning",
                "step": "Step_Upkeep",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [11, 12]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 51, "type": "ZoneType_Stack", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [{"type": ["AnnotationType_NewTurnStarted"]}],
            "actions": [],
        },
    )
    land_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 5, tzinfo=UTC), b"raw-2"),
        {
            "game_state_id": 2,
            "identity": {
                "match_id": "match-1",
                "game_number": 1,
                "turn_number": 1,
                "active_player_seat_id": 1,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [11]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [12]},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    spell_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 9, tzinfo=UTC), b"raw-3"),
        {
            "game_state_id": 3,
            "identity": {
                "match_id": "match-1",
                "game_number": 1,
                "turn_number": 1,
                "active_player_seat_id": 1,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 51, "type": "ZoneType_Stack", "ownerSeatId": 1, "objectInstanceIds": [11]},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 51,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                }
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_Cast", "instanceId": 11}}],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(land_event)
    gameplay_actions.observe_event(spell_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    action_types = [entry["action_type"] for entry in payload["entries"]]
    assert action_types == ["turn_started", "land_played", "spell_cast"]
    assert payload["entries"][1]["display_name"] == "Forest"
    assert payload["entries"][2]["display_name"] == "Shoot the Sheriff"

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "You played Forest from hand to battlefield" in markdown
    assert "You cast Shoot the Sheriff from hand to stack" in markdown


def test_gameplay_actions_flush_once_per_game_state_event(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "1001": {"name": "Shoot the Sheriff"},
                    "2002": {"name": "Forest"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-batch",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 22, 0, 0, tzinfo=UTC), b"batch-1"),
        {
            "game_state_id": 1,
            "identity": {"match_id": "match-batch", "game_number": 1, "turn_number": 1},
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [11, 12]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 51, "type": "ZoneType_Stack", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    update_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 22, 0, 5, tzinfo=UTC), b"batch-2"),
        {
            "game_state_id": 2,
            "identity": {"match_id": "match-batch", "game_number": 1, "turn_number": 1},
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [12]},
                {"zoneId": 51, "type": "ZoneType_Stack", "ownerSeatId": 1, "objectInstanceIds": [11]},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 51,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_Cast", "instanceId": 11}}],
        },
    )

    write_calls: list[str] = []
    original_write = gameplay_actions._write_match_actions

    def _counting_write(match_id: str) -> None:
        write_calls.append(match_id)
        original_write(match_id)

    monkeypatch.setattr(gameplay_actions, "_write_match_actions", _counting_write)

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(update_event)

    assert write_calls == ["match-batch"]


def test_gameplay_actions_classify_partial_limbo_rows_and_carry_turn_context(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "1001": {"name": "Shoot the Sheriff"},
                    "2002": {"name": "Forest"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-2",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 21, 0, 0, tzinfo=UTC), b"raw-a"),
        {
            "game_state_id": 10,
            "identity": {
                "match_id": "match-2",
                "game_number": 1,
                "turn_number": 3,
                "active_player_seat_id": 1,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [11, 12]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cast_diff_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 21, 0, 4, tzinfo=UTC), b"raw-b"),
        {
            "game_state_id": 11,
            "identity": {
                "match_id": "match-2",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [12]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": [11]},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 71,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                }
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_Cast", "instanceId": 11}}],
        },
    )
    land_diff_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 21, 0, 6, tzinfo=UTC), b"raw-c"),
        {
            "game_state_id": 12,
            "identity": {
                "match_id": "match-2",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": [12]},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 71,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                }
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_Play", "instanceId": 12}}],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cast_diff_event)
    gameplay_actions.observe_event(land_diff_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    action_types = [entry["action_type"] for entry in payload["entries"]]
    assert action_types == ["spell_cast", "land_played"]
    assert payload["entries"][0]["to_zone_type"] == "ZoneType_Stack"
    assert payload["entries"][1]["to_zone_type"] == "ZoneType_Battlefield"
    assert payload["entries"][0]["turn_number"] == 3
    assert payload["entries"][1]["turn_number"] == 3

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "You cast Shoot the Sheriff from hand to stack" in markdown
    assert "You played Forest from hand to battlefield" in markdown


def test_gameplay_actions_preserve_reduced_action_attribution_facts(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = _patch_gameplay_paths(tmp_path, monkeypatch)
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-action-attribution",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 8, 18, 0, 0, tzinfo=UTC), b"synthetic-action-a"),
        {
            "game_state_id": 100,
            "identity": {
                "match_id": "match-action-attribution",
                "game_number": 1,
                "turn_number": 4,
                "active_player_seat_id": 1,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [101]},
                {"zoneId": 32, "type": "ZoneType_Hand", "ownerSeatId": 2, "objectInstanceIds": [201]},
                {"zoneId": 51, "type": "ZoneType_Stack", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 101,
                    "grpId": 1101,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 201,
                    "grpId": 2202,
                    "zoneId": 32,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Sorcery"],
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    local_cast_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 8, 18, 0, 5, tzinfo=UTC), b"synthetic-action-b"),
        {
            "game_state_id": 101,
            "identity": {
                "match_id": "match-action-attribution",
                "game_number": 1,
                "turn_number": 4,
                "active_player_seat_id": 1,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 32, "type": "ZoneType_Hand", "ownerSeatId": 2, "objectInstanceIds": [201]},
                {"zoneId": 51, "type": "ZoneType_Stack", "objectInstanceIds": [101]},
            ],
            "game_objects": [
                {
                    "instanceId": 101,
                    "grpId": 1101,
                    "zoneId": 51,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 201,
                    "grpId": 2202,
                    "zoneId": 32,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Sorcery"],
                },
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_Cast", "instanceId": 101}}],
        },
    )
    opponent_cast_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 8, 18, 0, 9, tzinfo=UTC), b"synthetic-action-c"),
        {
            "game_state_id": 102,
            "identity": {
                "match_id": "match-action-attribution",
                "game_number": 1,
                "turn_number": 4,
                "active_player_seat_id": 2,
                "phase": "Phase_Main1",
                "step": "Step_None",
                "stage": "GameStage_Play",
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 32, "type": "ZoneType_Hand", "ownerSeatId": 2, "objectInstanceIds": []},
                {"zoneId": 51, "type": "ZoneType_Stack", "objectInstanceIds": [101, 201]},
            ],
            "game_objects": [
                {
                    "instanceId": 101,
                    "grpId": 1101,
                    "zoneId": 51,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 201,
                    "grpId": 2202,
                    "zoneId": 51,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Sorcery"],
                },
            ],
            "annotations": [],
            "actions": [{"seatId": 2, "action": {"actionType": "ActionType_Cast", "instanceId": 201}}],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(local_cast_event)
    gameplay_actions.observe_event(opponent_cast_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    entries = payload["entries"]

    assert payload["match_id"] == "match-action-attribution"
    assert payload["total_entries"] == 2
    assert [entry["action_type"] for entry in entries] == ["spell_cast", "spell_cast"]
    assert [entry["actor_relation"] for entry in entries] == ["local", "opponent"]
    assert [entry["game_state_id"] for entry in entries] == [101, 102]
    assert [entry["game_number"] for entry in entries] == [1, 1]
    assert [entry["turn_number"] for entry in entries] == [4, 4]
    assert [entry["timestamp"] for entry in entries] == [
        "2026-05-08T18:00:05+00:00",
        "2026-05-08T18:00:09+00:00",
    ]
    assert [entry["instance_id"] for entry in entries] == [101, 201]
    assert [entry["grp_id"] for entry in entries] == [1101, 2202]
    assert [entry["observed_grp_id"] for entry in entries] == [1101, 2202]
    assert [entry["identity_hint_source"] for entry in entries] == ["direct_grp_id", "direct_grp_id"]
    assert [entry["from_zone_type"] for entry in entries] == ["ZoneType_Hand", "ZoneType_Hand"]
    assert [entry["to_zone_type"] for entry in entries] == ["ZoneType_Stack", "ZoneType_Stack"]
    assert [entry["raw_action_types"] for entry in entries] == [
        ["ActionType_Cast@seat1"],
        ["ActionType_Cast@seat2"],
    ]
    assert list((status_root / "actions").glob("*.json"))
    assert not (tmp_path / "active_match_actions_latest.json").exists()


def test_gameplay_actions_classify_play_land_from_annotation_chain(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "2002": {"name": "Forest"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-3",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 22, 0, 0, tzinfo=UTC), b"raw-d"),
        {
            "game_state_id": 20,
            "identity": {
                "match_id": "match-3",
                "game_number": 1,
                "turn_number": 2,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [12]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    play_land_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 22, 0, 3, tzinfo=UTC), b"raw-e"),
        {
            "game_state_id": 21,
            "identity": {
                "match_id": "match-3",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": [12]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [99]},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 71,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
                {
                    "instanceId": 99,
                    "grpId": 2002,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [
                {
                    "affectedIds": [12],
                    "type": ["AnnotationType_ObjectIdChanged"],
                    "details": [
                        {"key": "orig_id", "valueInt32": [12]},
                        {"key": "new_id", "valueInt32": [99]},
                    ],
                },
                {
                    "affectedIds": [99],
                    "type": ["AnnotationType_ZoneTransfer"],
                    "details": [
                        {"key": "category", "valueString": ["PlayLand"]},
                    ],
                },
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(play_land_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["land_played"]
    assert payload["entries"][0]["to_zone_type"] == "ZoneType_Battlefield"
    assert payload["entries"][0]["turn_number"] == 2


def test_gameplay_actions_prefer_active_deck_name_and_hide_out_of_deck_candidate(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "ACTIVE_DECK_PROFILE_PATH", status_root / "active_deck_profile_latest.json")
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps({"object": "manasight_grp_id_overrides", "cards_by_grp_id": {}}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    candidate_report_path = oracle_root / "grp-id-candidate-report-latest.json"
    candidate_report_path.write_text(
        json.dumps(
            {
                "unresolved_mainboard_grp_ids": [
                    {
                        "grp_id": 5002,
                        "section": "mainboard",
                        "submitted_count": 1,
                        "heuristic_role": "spell",
                        "ranked_candidates": [{"name": "Out of Deck Card", "score": 100}],
                    }
                ],
                "unresolved_sideboard_grp_ids": [],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=candidate_report_path,
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    (status_root / "active_deck_profile_latest.json").write_text(
        json.dumps(
            {
                "object": "manasight_active_deck_profile",
                "mainboard": [
                    {"arena_id": 5001, "name": "In Deck Exact Card"},
                    {"arena_id": 7777, "name": "In Deck Support Card"},
                ],
                "sideboard": [],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    rendered_exact = gameplay_actions._render_entry(
        {
            "action_type": "spell_cast",
            "actor_relation": "local",
            "grp_id": 5001,
            "from_zone_type": "ZoneType_Hand",
            "to_zone_type": "ZoneType_Stack",
            "turn_number": 1,
        }
    )
    rendered_candidate = gameplay_actions._render_entry(
        {
            "action_type": "spell_cast",
            "actor_relation": "local",
            "grp_id": 5002,
            "from_zone_type": "ZoneType_Hand",
            "to_zone_type": "ZoneType_Stack",
            "turn_number": 1,
        }
    )

    assert rendered_exact["display_name"] == "In Deck Exact Card"
    assert rendered_exact["visible_in_log"] is True
    assert rendered_candidate["display_name"] == "[grpId 5002]"
    assert rendered_candidate["visible_in_log"] is True


def test_gameplay_actions_use_parent_chain_for_adventure_casts(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "ACTIVE_DECK_PROFILE_PATH", status_root / "active_deck_profile_latest.json")
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "86952": {"name": "Mosswood Dreadknight // Dread Whispers"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-4",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 0, 0, tzinfo=UTC), b"raw-f"),
        {
            "game_state_id": 30,
            "identity": {
                "match_id": "match-4",
                "game_number": 1,
                "turn_number": 3,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [314, 72]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 314,
                    "grpId": 86952,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                    "subtypes": ["SubType_Human", "SubType_Knight"],
                },
                {
                    "instanceId": 72,
                    "grpId": 86953,
                    "zoneId": 31,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 314,
                    "overlayGrpId": 86953,
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cast_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 0, 4, tzinfo=UTC), b"raw-g"),
        {
            "game_state_id": 31,
            "identity": {
                "match_id": "match-4",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [314]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": [72]},
            ],
            "game_objects": [
                {
                    "instanceId": 72,
                    "grpId": 86953,
                    "zoneId": 71,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 314,
                    "overlayGrpId": 86953,
                }
            ],
            "annotations": [],
            "actions": [{"seatId": 1, "action": {"actionType": "ActionType_CastAdventure", "instanceId": 72}}],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cast_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["spell_cast"]
    assert payload["entries"][0]["grp_id"] == 86952
    assert payload["entries"][0]["observed_grp_id"] == 86953
    assert payload["entries"][0]["identity_hint_source"] == "parent_chain"
    assert payload["entries"][0]["cast_mode"] == "adventure_face"
    assert payload["entries"][0]["display_name"] == "Mosswood Dreadknight // Dread Whispers"


def test_gameplay_actions_hide_anonymous_non_card_rows_from_markdown(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "ACTIVE_DECK_PROFILE_PATH", status_root / "active_deck_profile_latest.json")
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps({"object": "manasight_grp_id_overrides", "cards_by_grp_id": {}}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-5",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 30, 0, tzinfo=UTC), b"raw-h"),
        {
            "game_state_id": 40,
            "identity": {
                "match_id": "match-5",
                "game_number": 1,
                "turn_number": 1,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [1]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 1,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Artifact"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    hidden_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 30, 2, tzinfo=UTC), b"raw-i"),
        {
            "game_state_id": 41,
            "identity": {
                "match_id": "match-5",
                "game_number": 1,
                "turn_number": 1,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [1]},
            ],
            "game_objects": [
                {
                    "instanceId": 1,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Artifact"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(hidden_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert payload["total_entries"] == 1
    assert payload["visible_entry_count"] == 0
    assert payload["entries"][0]["visible_in_log"] is False

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "No visible gameplay actions recorded yet." in markdown


def test_gameplay_actions_promote_castspell_annotation_chain_without_direct_action(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "1001": {"name": "Shoot the Sheriff"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-6",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 40, 0, tzinfo=UTC), b"raw-j"),
        {
            "game_state_id": 50,
            "identity": {
                "match_id": "match-6",
                "game_number": 1,
                "turn_number": 2,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [11]},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cast_diff_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 40, 2, tzinfo=UTC), b"raw-k"),
        {
            "game_state_id": 51,
            "identity": {
                "match_id": "match-6",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [99]},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [11]},
            ],
            "game_objects": [
                {
                    "instanceId": 11,
                    "grpId": 1001,
                    "zoneId": 30,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 99,
                    "grpId": 1001,
                    "zoneId": 27,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
            ],
            "annotations": [
                {
                    "affectedIds": [11],
                    "type": ["AnnotationType_ObjectIdChanged"],
                    "details": [
                        {"key": "orig_id", "valueInt32": [11]},
                        {"key": "new_id", "valueInt32": [99]},
                    ],
                },
                {
                    "affectedIds": [99],
                    "type": ["AnnotationType_ZoneTransfer"],
                    "details": [
                        {"key": "zone_src", "valueInt32": [31]},
                        {"key": "zone_dest", "valueInt32": [27]},
                        {"key": "category", "valueString": ["CastSpell"]},
                    ],
                },
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cast_diff_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["spell_cast"]
    assert payload["entries"][0]["grp_id"] == 1001
    assert payload["entries"][0]["to_zone_type"] == "ZoneType_Stack"

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "You cast Shoot the Sheriff from hand to stack" in markdown


def test_gameplay_actions_classify_spell_finished_and_left_battlefield_from_limbo(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "1001": {"name": "Shoot the Sheriff"},
                    "2001": {"name": "Keen-Eyed Curator"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-7",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 50, 0, tzinfo=UTC), b"raw-l"),
        {
            "game_state_id": 60,
            "identity": {
                "match_id": "match-7",
                "game_number": 1,
                "turn_number": 4,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [21]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [22]},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 21,
                    "grpId": 1001,
                    "zoneId": 27,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 22,
                    "grpId": 2001,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Creature"],
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cleanup_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 6, 23, 50, 3, tzinfo=UTC), b"raw-m"),
        {
            "game_state_id": 61,
            "identity": {
                "match_id": "match-7",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [21, 22]},
            ],
            "game_objects": [
                {
                    "instanceId": 21,
                    "grpId": 1001,
                    "zoneId": 30,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                },
                {
                    "instanceId": 22,
                    "grpId": 2001,
                    "zoneId": 30,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Creature"],
                },
            ],
            "annotations": [
                {"type": ["AnnotationType_ResolutionStart"]},
                {"type": ["AnnotationType_ResolutionComplete"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cleanup_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == [
        "spell_finished",
        "permanent_left_battlefield",
    ]

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "Shoot the Sheriff finished resolving and left the stack" in markdown
    assert "Keen-Eyed Curator left the battlefield" in markdown


def test_gameplay_actions_cast_from_exile_uses_stack_target_and_zone_aware_summary(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "86952": {"name": "Mosswood Dreadknight // Dread Whispers"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-8",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 0, 0, tzinfo=UTC), b"raw-n"),
        {
            "game_state_id": 70,
            "identity": {
                "match_id": "match-8",
                "game_number": 1,
                "turn_number": 6,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 29, "type": "ZoneType_Exile", "ownerSeatId": 1, "objectInstanceIds": [303]},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 303,
                    "grpId": 86952,
                    "zoneId": 29,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                    "subtypes": ["SubType_Human", "SubType_Knight"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cast_from_exile_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 0, 4, tzinfo=UTC), b"raw-o"),
        {
            "game_state_id": 71,
            "identity": {
                "match_id": "match-8",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 29, "type": "ZoneType_Exile", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [304]},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [303]},
            ],
            "game_objects": [
                {
                    "instanceId": 303,
                    "grpId": 86952,
                    "zoneId": 30,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                },
                {
                    "instanceId": 304,
                    "grpId": 86952,
                    "zoneId": 27,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                },
            ],
            "annotations": [
                {
                    "affectedIds": [303],
                    "type": ["AnnotationType_ObjectIdChanged"],
                    "details": [
                        {"key": "orig_id", "valueInt32": [303]},
                        {"key": "new_id", "valueInt32": [304]},
                    ],
                },
                {
                    "affectedIds": [304],
                    "type": ["AnnotationType_ZoneTransfer"],
                    "details": [
                        {"key": "zone_src", "valueInt32": [29]},
                        {"key": "zone_dest", "valueInt32": [27]},
                        {"key": "category", "valueString": ["CastSpell"]},
                    ],
                },
                {"type": ["AnnotationType_UserActionTaken"]},
                {"type": ["AnnotationType_ManaPaid"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cast_from_exile_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["spell_cast"]
    assert payload["entries"][0]["to_zone_type"] == "ZoneType_Stack"

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "You cast Mosswood Dreadknight // Dread Whispers from exile to stack" in markdown


def test_gameplay_actions_preserve_canonical_adventure_identity_across_replacement_cleanup(
    tmp_path, monkeypatch
) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "86952": {"name": "Mosswood Dreadknight // Dread Whispers"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-9",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 10, 0, tzinfo=UTC), b"raw-p"),
        {
            "game_state_id": 80,
            "identity": {
                "match_id": "match-9",
                "game_number": 1,
                "turn_number": 3,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [314, 72]},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 314,
                    "grpId": 86952,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                    "subtypes": ["SubType_Human", "SubType_Knight"],
                },
                {
                    "instanceId": 72,
                    "grpId": 86953,
                    "zoneId": 31,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 314,
                    "overlayGrpId": 86953,
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cast_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 10, 2, tzinfo=UTC), b"raw-q"),
        {
            "game_state_id": 81,
            "identity": {
                "match_id": "match-9",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [314]},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [99]},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [72]},
            ],
            "game_objects": [
                {
                    "instanceId": 72,
                    "grpId": 86953,
                    "zoneId": 30,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 314,
                    "overlayGrpId": 86953,
                },
                {
                    "instanceId": 99,
                    "grpId": 86953,
                    "zoneId": 27,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "overlayGrpId": 86953,
                },
            ],
            "annotations": [
                {
                    "affectedIds": [72],
                    "type": ["AnnotationType_ObjectIdChanged"],
                    "details": [
                        {"key": "orig_id", "valueInt32": [72]},
                        {"key": "new_id", "valueInt32": [99]},
                    ],
                },
                {
                    "affectedIds": [99],
                    "type": ["AnnotationType_ZoneTransfer"],
                    "details": [
                        {"key": "zone_src", "valueInt32": [31]},
                        {"key": "zone_dest", "valueInt32": [27]},
                        {"key": "category", "valueString": ["CastSpell"]},
                    ],
                },
            ],
            "actions": [],
        },
    )
    cleanup_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 10, 4, tzinfo=UTC), b"raw-r"),
        {
            "game_state_id": 82,
            "identity": {
                "match_id": "match-9",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [99]},
            ],
            "game_objects": [
                {
                    "instanceId": 99,
                    "grpId": 86953,
                    "zoneId": 30,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "overlayGrpId": 86953,
                }
            ],
            "annotations": [
                {"type": ["AnnotationType_ResolutionStart"]},
                {"type": ["AnnotationType_ResolutionComplete"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cast_event)
    gameplay_actions.observe_event(cleanup_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["spell_cast", "spell_finished"]
    assert payload["entries"][0]["grp_id"] == 86952
    assert payload["entries"][0]["observed_grp_id"] == 86953
    assert payload["entries"][0]["cast_mode"] == "adventure_face"
    assert payload["entries"][1]["grp_id"] == 86952
    assert payload["entries"][1]["observed_grp_id"] == 86953
    assert payload["entries"][1]["identity_hint_source"] in {"prior_instance", "replacement_chain"}

    markdown = (status_root / "active_match_action_log_latest.md").read_text(encoding="utf-8")
    assert "Mosswood Dreadknight // Dread Whispers (adventure face)" in markdown
    assert "finished resolving and left the stack" in markdown


def test_gameplay_actions_skip_replacement_followup_land_entry(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "2002": {"name": "Forest"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-10",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 20, 0, tzinfo=UTC), b"raw-s"),
        {
            "game_state_id": 90,
            "identity": {
                "match_id": "match-10",
                "game_number": 1,
                "turn_number": 2,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": [12]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 31,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    play_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 20, 3, tzinfo=UTC), b"raw-t"),
        {
            "game_state_id": 91,
            "identity": {
                "match_id": "match-10",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 31, "type": "ZoneType_Hand", "ownerSeatId": 1, "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "ownerSeatId": 1, "objectInstanceIds": [99]},
                {"zoneId": 71, "type": "ZoneType_Limbo", "ownerSeatId": 1, "objectInstanceIds": [12]},
            ],
            "game_objects": [
                {
                    "instanceId": 12,
                    "grpId": 2002,
                    "zoneId": 71,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
                {
                    "instanceId": 99,
                    "grpId": 2002,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Land"],
                },
            ],
            "annotations": [
                {
                    "affectedIds": [12],
                    "type": ["AnnotationType_ObjectIdChanged"],
                    "details": [
                        {"key": "orig_id", "valueInt32": [12]},
                        {"key": "new_id", "valueInt32": [99]},
                    ],
                },
                {
                    "affectedIds": [99],
                    "type": ["AnnotationType_ZoneTransfer"],
                    "details": [
                        {"key": "zone_src", "valueInt32": [31]},
                        {"key": "zone_dest", "valueInt32": [41]},
                        {"key": "category", "valueString": ["PlayLand"]},
                    ],
                },
                {"type": ["AnnotationType_UserActionTaken"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(play_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["land_played"]
    assert payload["entries"][0]["display_name"] == "Forest"


def test_gameplay_actions_skip_revealed_card_cleanup_from_hand(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps({"object": "manasight_grp_id_overrides", "cards_by_grp_id": {}}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-11",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 30, 0, tzinfo=UTC), b"raw-u"),
        {
            "game_state_id": 100,
            "identity": {
                "match_id": "match-11",
                "game_number": 1,
                "turn_number": 2,
                "active_player_seat_id": 2,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 35, "type": "ZoneType_Hand", "ownerSeatId": 2, "objectInstanceIds": [77]},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 77,
                    "grpId": 96608,
                    "zoneId": 35,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Creature"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    cleanup_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 30, 2, tzinfo=UTC), b"raw-v"),
        {
            "game_state_id": 101,
            "identity": {
                "match_id": "match-11",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 35, "type": "ZoneType_Hand", "ownerSeatId": 2, "objectInstanceIds": []},
                {"zoneId": 30, "type": "ZoneType_Limbo", "objectInstanceIds": [77]},
            ],
            "game_objects": [
                {
                    "instanceId": 77,
                    "grpId": 96608,
                    "zoneId": 30,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 2,
                    "controllerSeatId": 2,
                    "cardTypes": ["CardType_Creature"],
                }
            ],
            "annotations": [
                {"type": ["AnnotationType_ObjectIdChanged"]},
                {"type": ["AnnotationType_RevealedCardDeleted"]},
                {"type": ["AnnotationType_ZoneTransfer"]},
                {"type": ["AnnotationType_ResolutionComplete"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(cleanup_event)

    assert gameplay_actions._MATCH_ACTIONS.get("match-11") in (None, [])


def test_gameplay_actions_skip_shadow_child_battlefield_resolution(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "86952": {"name": "Mosswood Dreadknight // Dread Whispers"},
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-12",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 40, 0, tzinfo=UTC), b"raw-w"),
        {
            "game_state_id": 110,
            "identity": {
                "match_id": "match-12",
                "game_number": 1,
                "turn_number": 4,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [422, 423]},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 422,
                    "grpId": 86952,
                    "zoneId": 27,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                },
                {
                    "instanceId": 423,
                    "grpId": 86953,
                    "zoneId": 27,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 422,
                    "overlayGrpId": 86953,
                },
            ],
            "annotations": [],
            "actions": [],
        },
    )
    resolve_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 40, 3, tzinfo=UTC), b"raw-x"),
        {
            "game_state_id": 111,
            "identity": {
                "match_id": "match-12",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
                {"zoneId": 41, "type": "ZoneType_Battlefield", "objectInstanceIds": [422, 423]},
            ],
            "game_objects": [
                {
                    "instanceId": 422,
                    "grpId": 86952,
                    "zoneId": 41,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Creature"],
                },
                {
                    "instanceId": 423,
                    "grpId": 86953,
                    "zoneId": 41,
                    "type": "GameObjectType_Adventure",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Sorcery"],
                    "subtypes": ["SubType_Adventure"],
                    "parentId": 422,
                    "overlayGrpId": 86953,
                },
            ],
            "annotations": [
                {"type": ["AnnotationType_ResolutionStart"]},
                {"type": ["AnnotationType_ResolutionComplete"]},
                {"type": ["AnnotationType_ZoneTransfer"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(resolve_event)

    payload = json.loads((status_root / "active_match_actions_latest.json").read_text(encoding="utf-8"))
    assert [entry["action_type"] for entry in payload["entries"]] == ["permanent_resolved"]
    assert payload["entries"][0]["grp_id"] == 86952


def test_gameplay_actions_skip_pending_support_transition(tmp_path, monkeypatch) -> None:
    _reset_gameplay_state()
    status_root = tmp_path / "status"
    oracle_root = tmp_path / "oracle"
    status_root.mkdir(parents=True, exist_ok=True)
    oracle_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(gameplay_actions, "STATUS_ACTIONS_ROOT", status_root / "actions")
    monkeypatch.setattr(gameplay_actions, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "active_match_actions_latest.json")
    monkeypatch.setattr(
        gameplay_actions, "ACTIVE_MATCH_ACTION_LOG_PATH", status_root / "active_match_action_log_latest.md"
    )
    monkeypatch.setattr(gameplay_actions, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")
    _patch_status_writer(monkeypatch)
    monkeypatch.setattr(grp_id_catalog, "GRP_ID_CATALOG_PATH", oracle_root / "mtga-grp-id-catalog-latest.json")

    override_path = oracle_root / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps({"object": "manasight_grp_id_overrides", "cards_by_grp_id": {}}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    grp_id_catalog.refresh_grp_id_catalog(
        path=oracle_root / "mtga-grp-id-catalog-latest.json",
        grp_id_override_path=override_path,
        candidate_report_path=oracle_root / "missing-report.json",
        output_dir=oracle_root,
    )
    gameplay_actions.bootstrap_gameplay_actions()

    state._CONTEXT.update(
        {
            "current_match_id": "match-13",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    initial_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 50, 0, tzinfo=UTC), b"raw-y"),
        {
            "game_state_id": 120,
            "identity": {
                "match_id": "match-13",
                "game_number": 1,
                "turn_number": 3,
                "active_player_seat_id": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 26, "type": "ZoneType_Pending", "objectInstanceIds": [55]},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": []},
            ],
            "game_objects": [
                {
                    "instanceId": 55,
                    "grpId": 192763,
                    "objectSourceGrpId": 97452,
                    "zoneId": 26,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                }
            ],
            "annotations": [],
            "actions": [],
        },
    )
    support_event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 7, 0, 50, 2, tzinfo=UTC), b"raw-z"),
        {
            "game_state_id": 121,
            "identity": {
                "match_id": "match-13",
                "game_number": 1,
            },
            "system_seat_ids": [1],
            "zones": [
                {"zoneId": 26, "type": "ZoneType_Pending", "objectInstanceIds": []},
                {"zoneId": 27, "type": "ZoneType_Stack", "objectInstanceIds": [55]},
            ],
            "game_objects": [
                {
                    "instanceId": 55,
                    "grpId": 192763,
                    "objectSourceGrpId": 97452,
                    "zoneId": 27,
                    "type": "GameObjectType_Card",
                    "ownerSeatId": 1,
                    "controllerSeatId": 1,
                    "cardTypes": ["CardType_Instant"],
                }
            ],
            "annotations": [
                {"type": ["AnnotationType_Shuffle"]},
                {"type": ["AnnotationType_ResolutionComplete"]},
                {"type": ["AnnotationType_AbilityInstanceDeleted"]},
            ],
            "actions": [],
        },
    )

    gameplay_actions.observe_event(initial_event)
    gameplay_actions.observe_event(support_event)

    assert gameplay_actions._MATCH_ACTIONS.get("match-13") in (None, [])
