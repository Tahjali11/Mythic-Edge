from datetime import UTC, datetime

from mythic_edge_parser.app import state
from mythic_edge_parser.app import transforms as transforms_module
from mythic_edge_parser.app.config import KEEP_EVENT_LIFECYCLE_TYPES
from mythic_edge_parser.app.transforms import include_event, summarize, to_serializable, to_sheet_rows
from mythic_edge_parser.events import (
    ClientActionEvent,
    ConnectionErrorEvent,
    DeckCollectionEvent,
    EventLifecycleEvent,
    EventMetadata,
    GameStateEvent,
    InventoryEvent,
    RankEvent,
)


def test_include_event_keeps_local_private_hand_snapshot_without_active_player() -> None:
    state._LOCAL_TURN_KEYS.clear()
    state._LOCAL_HAND_SNAPSHOT_KEYS.clear()

    event = GameStateEvent(
        EventMetadata(datetime(2026, 4, 27, 21, 12, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "game_info": {"matchID": "m_hand_archive", "gameNumber": 1},
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "gameInfo": {"matchID": "m_hand_archive", "gameNumber": 1},
                    "turnInfo": {"turnNumber": 1},
                    "zones": [
                        {
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [101, 102, 103, 104, 105, 106, 107],
                        }
                    ],
                    "gameObjects": [
                        {"instanceId": 101, "grpId": 91829},
                        {"instanceId": 102, "grpId": 93940},
                        {"instanceId": 103, "grpId": 98436},
                        {"instanceId": 104, "grpId": 72579},
                        {"instanceId": 105, "grpId": 86752},
                        {"instanceId": 106, "grpId": 90452},
                        {"instanceId": 107, "grpId": 87235},
                    ],
                }
            },
        },
    )

    assert include_event(event) is True
    assert include_event(event) is False


def test_include_event_still_dedupes_normal_turn_rows() -> None:
    state._LOCAL_TURN_KEYS.clear()
    state._LOCAL_HAND_SNAPSHOT_KEYS.clear()

    event = GameStateEvent(
        EventMetadata(datetime(2026, 4, 27, 21, 13, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "game_info": {"matchID": "m_turn_archive", "gameNumber": 1},
            "raw_game_state": {
                "gameStateMessage": {
                    "gameInfo": {"matchID": "m_turn_archive", "gameNumber": 1},
                    "turnInfo": {
                        "turnNumber": 2,
                        "activePlayer": 1,
                        "phase": "Phase_Main1",
                        "step": "Step_None",
                    },
                }
            },
        },
    )

    assert include_event(event) is True
    assert include_event(event) is False


def test_include_event_keeps_connection_error_and_deck_collection() -> None:
    connection_event = ConnectionErrorEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 0, tzinfo=UTC), b"raw"),
        {"error_type": "reconnect_result", "result": "Error"},
    )
    deck_event = DeckCollectionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 1, 0, tzinfo=UTC), b"raw"),
        {"type": "deck_collection_snapshot", "decks": {"deck-1": {"Name": "Test"}}},
    )

    assert include_event(connection_event) is True
    assert include_event(deck_event) is True


def test_include_event_keeps_inventory_snapshot() -> None:
    inventory_event = InventoryEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 2, 0, tzinfo=UTC), b"raw"),
        {"type": "inventory_snapshot", "inventory": {"gold": 1234}},
    )

    assert include_event(inventory_event) is True


def test_event_lifecycle_transform_config_keeps_all_emitted_types() -> None:
    assert KEEP_EVENT_LIFECYCLE_TYPES == {
        "event_join",
        "event_enter_pairing",
        "event_claim_prize",
    }

    for event_type in KEEP_EVENT_LIFECYCLE_TYPES:
        event = EventLifecycleEvent(
            EventMetadata(datetime(2026, 5, 5, 21, 3, 0, tzinfo=UTC), f"raw-{event_type}".encode()),
            {"type": event_type, "raw_event_lifecycle": f"raw-{event_type}"},
        )

        assert include_event(event) is True
        assert summarize(event) == f"EventLifecycle type={event_type}"
        assert to_sheet_rows(event) == []
        assert to_serializable(event)["payload"] == {
            "type": event_type,
            "raw_event_lifecycle": f"raw-{event_type}",
        }


def test_event_lifecycle_transform_rejects_unknown_lifecycle_type() -> None:
    event = EventLifecycleEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 3, 0, tzinfo=UTC), b"raw"),
        {"type": "event_unknown", "raw_event_lifecycle": "raw"},
    )

    assert include_event(event) is False


def test_to_serializable_uses_context_fallback_for_missing_game_identity() -> None:
    state._CONTEXT["current_match_id"] = "match-context"
    state._CONTEXT["current_game_number"] = 2

    event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 3, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "raw_game_state": {
                "gameStateMessage": {
                    "turnInfo": {
                        "turnNumber": 3,
                        "activePlayer": 1,
                        "phase": "Phase_Main1",
                        "step": "Step_None",
                    }
                }
            },
        },
    )

    serialized = to_serializable(event)

    assert serialized["derived"]["match_id"] == "match-context"
    assert serialized["derived"]["game_number"] == 2
    assert serialized["derived"]["identity_source"] == "context"
    assert serialized["derived"]["identity_ready"] is True


def test_to_sheet_rows_rank_event_uses_shared_rank_dedupe_state() -> None:
    state.reset_runtime_state()

    event = RankEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 4, 0, tzinfo=UTC), b"raw"),
        {
            "constructed_class": "Diamond",
            "constructed_level": 4,
            "constructed_percentile": "",
        },
    )

    first_rows = to_sheet_rows(event)
    second_rows = to_sheet_rows(event)

    assert len(first_rows) == 1
    assert first_rows[0]["constructed_rank"] == "Diamond 4"
    assert second_rows == []
    assert state.get_last_posted_rank() == "Diamond 4"


def test_to_sheet_rows_keeps_turn_one_checkpoint_when_gamestate_posting_is_disabled(monkeypatch) -> None:
    state.reset_runtime_state()
    monkeypatch.setattr(transforms_module, "POST_GAMESTATE_ROWS", False)

    event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 5, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "game_info": {"matchID": "match-turn-one", "gameNumber": 1},
            "raw_game_state": {
                "gameStateMessage": {
                    "gameInfo": {"matchID": "match-turn-one", "gameNumber": 1},
                    "turnInfo": {
                        "turnNumber": 1,
                        "activePlayer": 2,
                        "phase": "Phase_Beginning",
                        "step": "Step_Upkeep",
                    },
                }
            },
        },
    )

    first_rows = to_sheet_rows(event)
    second_rows = to_sheet_rows(event)

    assert len(first_rows) == 1
    assert first_rows[0]["scope"] == "Turn"
    assert first_rows[0]["turn_number"] == 1
    assert first_rows[0]["active_player"] == 2
    assert second_rows == []


def test_to_sheet_rows_mulligan_row_does_not_increment_shared_counter_twice() -> None:
    state.reset_runtime_state()
    state._CONTEXT["current_match_id"] = "match-mulligan"
    state._CONTEXT["current_game_number"] = 1

    event = ClientActionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 6, 0, tzinfo=UTC), b"raw"),
        {
            "type": "mulligan_resp",
            "decision": "mulligan",
            "request_id": 77,
        },
    )

    state._update_match_summary(event)
    rows = to_sheet_rows(event)

    assert len(rows) == 1
    assert rows[0]["mulligan_count"] == 1
    assert state._MULLIGAN_COUNTS[("match-mulligan", 1)] == 1
