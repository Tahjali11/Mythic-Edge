from __future__ import annotations

import json
import os
import re
from collections.abc import Sequence
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, get_args

import pytest

from mythic_edge_parser import events
from mythic_edge_parser.app import models, sheet_exports, sheet_schema
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import (
    client_actions,
    collection,
    connection_close,
    connection_error,
    connection_state,
    event_lifecycle,
    gre,
    inventory,
    match_state,
    metadata,
    rank,
    session,
    truncation,
)

SNAPSHOT_VERSION = 1
UPDATE_ENV_VAR = "MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS"
REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = Path(__file__).resolve().parent / "fixtures" / "schema_snapshots"
APPS_SCRIPT_PATH = REPO_ROOT / "tools" / "google_apps_script" / "Code.gs"
TS = datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC)

_RUNTIME_FAMILY_TO_APPS_SCRIPT_HEADER_KEY = {
    sheet_schema.ACTION_LOG_FAMILY: "actionLog",
    sheet_schema.DECK_SNAPSHOT_FAMILY: "deckSnapshot",
    sheet_schema.COLLECTION_SNAPSHOT_FAMILY: "collectionSnapshot",
    sheet_schema.PARSER_STATUS_FAMILY: "parserStatus",
    sheet_schema.CARD_PERFORMANCE_FAMILY: "cardPerformance",
}
_RUNTIME_FAMILY_TO_APPS_SCRIPT_BUILD_FUNCTION = {
    sheet_schema.ACTION_LOG_FAMILY: "buildActionLogRowObject_",
    sheet_schema.DECK_SNAPSHOT_FAMILY: "buildDeckSnapshotRowObject_",
    sheet_schema.COLLECTION_SNAPSHOT_FAMILY: "buildCollectionSnapshotRowObject_",
    sheet_schema.PARSER_STATUS_FAMILY: "buildParserStatusRowObject_",
    sheet_schema.CARD_PERFORMANCE_FAMILY: "buildCardPerformanceRowObject_",
}
_APPS_SCRIPT_DISPATCH_FAMILIES_UNDER_TEST = (
    "MatchLogRow",
    "GameLogRow",
    sheet_schema.ACTION_LOG_FAMILY,
    sheet_schema.DECK_SNAPSHOT_FAMILY,
    sheet_schema.COLLECTION_SNAPSHOT_FAMILY,
    sheet_schema.PARSER_STATUS_FAMILY,
    sheet_schema.CARD_PERFORMANCE_FAMILY,
    "MatchSummary",
)
_FORBIDDEN_SNAPSHOT_VALUE_SNIPPETS = (
    "script.google.com/macros/s/",
    "AKfy",
    "WEBHOOK_URL",
    "spreadsheetId",
    "deploymentTag",
    "C:\\Users\\",
    "/Users/",
    "data/match_logs/",
    "data/runtime_logs/",
    "data/failed_posts/",
    "data/status/",
)


def test_parser_event_class_snapshot_matches_contract() -> None:
    _assert_snapshot("parser_event_classes.json", _parser_event_class_snapshot())


def test_parser_payload_key_snapshot_matches_contract() -> None:
    _assert_snapshot("parser_payload_keys.json", _parser_payload_key_snapshot())


def test_workbook_row_key_snapshot_matches_contract() -> None:
    snapshot = _workbook_row_key_snapshot()
    row_snapshots = snapshot["current_landing_rows"]

    assert "MGTA Start Time" in row_snapshots["MatchLogRow"]["keys"]
    assert set(sheet_schema.MATCH_LOG_SYNC_FIELDS) <= set(row_snapshots["MatchLogRow"]["keys"])
    assert set(sheet_schema.GAME_LOG_SYNC_FIELDS) <= set(row_snapshots["GameLogRow"]["keys"])
    _assert_snapshot("workbook_row_keys.json", snapshot)


def test_sheet_schema_surface_snapshot_matches_contract() -> None:
    _assert_snapshot("sheet_schema_surfaces.json", _sheet_schema_surface_snapshot())


def test_runtime_export_row_key_snapshot_matches_contract() -> None:
    snapshot = _runtime_export_row_key_snapshot()

    for family, row_schema in snapshot["runtime_export_rows"].items():
        spec = sheet_schema.runtime_sheet_spec(family)
        assert row_schema["metadata"] == {
            "event_family": spec.family,
            "event_type": spec.event_type,
            "scope": spec.scope,
        }

    _assert_snapshot("runtime_export_row_keys.json", snapshot)


def test_apps_script_repo_parity_snapshot_matches_contract() -> None:
    snapshot = _apps_script_repo_parity_snapshot()

    assert set(_APPS_SCRIPT_DISPATCH_FAMILIES_UNDER_TEST) <= set(snapshot["dispatch_event_families_under_test"])
    assert snapshot["match_log_field_map_keys"] == list(sheet_schema.MATCH_LOG_SYNC_FIELDS)
    assert snapshot["game_log_field_map_keys"] == list(sheet_schema.GAME_LOG_SYNC_FIELDS)

    for family, header_key in _RUNTIME_FAMILY_TO_APPS_SCRIPT_HEADER_KEY.items():
        expected_headers = list(sheet_schema.runtime_sheet_headers(family))
        assert snapshot["runtime_landing_headers"][header_key] == expected_headers
        assert snapshot["runtime_build_object_headers"][family] == expected_headers

    runtime_rows = _runtime_export_rows_by_family()
    for family, consumed_keys in snapshot["runtime_build_object_data_keys"].items():
        assert set(consumed_keys) <= set(runtime_rows[family])

    _assert_snapshot("apps_script_repo_parity.json", snapshot)


def _assert_snapshot(filename: str, current: dict[str, Any]) -> None:
    _assert_no_forbidden_snapshot_content(current)
    snapshot_path = SNAPSHOT_ROOT / filename
    encoded_current = _encode_snapshot(current)

    if os.environ.get(UPDATE_ENV_VAR) == "1":
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(encoded_current, encoding="utf-8")
        return

    assert snapshot_path.exists(), _snapshot_policy_message(snapshot_path)
    expected = json.loads(snapshot_path.read_text(encoding="utf-8"))
    assert current == expected, _snapshot_policy_message(snapshot_path)


def _snapshot_policy_message(snapshot_path: Path) -> str:
    return (
        f"Schema snapshot mismatch for {snapshot_path}. Do not auto-update schema snapshots. "
        "Snapshot changes require explicit issue, contract, and review approval. "
        f"After approval only, set {UPDATE_ENV_VAR}=1 and rerun tests/test_event_schema_snapshots.py."
    )


def _encode_snapshot(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _assert_no_forbidden_snapshot_content(payload: dict[str, Any]) -> None:
    encoded = _encode_snapshot(payload)
    for snippet in _FORBIDDEN_SNAPSHOT_VALUE_SNIPPETS:
        assert snippet not in encoded


def _parser_event_class_snapshot() -> dict[str, Any]:
    concrete_event_classes = _concrete_event_classes()
    game_event_union = [event_cls.__name__ for event_cls in get_args(events.GameEvent)]

    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "dataclass_fields": {
            "BaseEvent": [field.name for field in fields(events.BaseEvent)],
            "EventMetadata": [field.name for field in fields(events.EventMetadata)],
            "RuntimeSheetSpec": [field.name for field in fields(sheet_schema.RuntimeSheetSpec)],
        },
        "event_classes": [
            {
                "class": event_cls.__name__,
                "in_game_event_union": event_cls.__name__ in game_event_union,
                "kind": event_cls.kind,
                "performance_class": event_cls.performance_class.value,
            }
            for event_cls in concrete_event_classes
        ],
        "game_event_union": game_event_union,
        "performance_class_values": [performance_class.value for performance_class in events.PerformanceClass],
    }


def _concrete_event_classes() -> list[type[events.BaseEvent]]:
    return [
        obj
        for obj in vars(events).values()
        if isinstance(obj, type) and issubclass(obj, events.BaseEvent) and obj is not events.BaseEvent
    ]


def _parser_payload_key_snapshot() -> dict[str, Any]:
    payloads = {}
    for label, event in _parser_payload_sample_events():
        discriminator = _payload_discriminator(label, event.payload)
        payloads[f"{event.kind}.{discriminator}"] = {
            "discriminator": discriminator,
            "event_kind": event.kind,
            "keys": list(event.payload),
        }

    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "payloads": payloads,
    }


def _payload_discriminator(label: str, payload: dict[str, Any]) -> str:
    payload_type = payload.get("type")
    return payload_type if isinstance(payload_type, str) and payload_type else label


def _parser_payload_sample_events() -> list[tuple[str, events.BaseEvent]]:
    samples: list[tuple[str, events.BaseEvent]] = []
    samples.extend(_client_action_sample_events())
    samples.extend(_match_state_sample_events())
    samples.extend(_gre_sample_events())
    samples.extend(_truncation_sample_events())
    samples.extend(_collection_sample_events())
    samples.extend(_small_parser_sample_events())
    samples.extend(_connection_sample_events())
    samples.append(
        (
            "log_file_rotated",
            events.LogFileRotatedEvent(
                events.EventMetadata.empty(),
                {"type": "log_file_rotated", "path": "Player.log"},
            ),
        )
    )
    return samples


def _client_action_sample_events() -> list[tuple[str, events.BaseEvent]]:
    return [
        (
            "client_ui_message",
            _expect_one_event(
                client_actions.try_parse(
                    _unity_json_entry(
                        "ClientToGREUIMessage",
                        {
                            "requestId": 1,
                            "clientToMatchServiceMessageType": "ClientToMatchServiceMessageType_ClientToGREUIMessage",
                            "payload": {"type": "ClientMessageType_UIMessage"},
                        },
                    ),
                    TS,
                )
            ),
        ),
        (
            "generic_client_action",
            _expect_one_event(
                client_actions.try_parse(
                    _client_to_gre_message(
                        request_id=2,
                        payload={
                            "type": "ClientMessageType_ChooseStartingPlayerResp",
                            "gameStateId": 1,
                            "respId": 2,
                        },
                    ),
                    TS,
                )
            ),
        ),
        (
            "mulligan_resp",
            _expect_one_event(
                client_actions.try_parse(
                    _client_to_gre_message(
                        request_id=3,
                        payload={
                            "type": "ClientMessageType_MulliganResp",
                            "gameStateId": 5,
                            "respId": 1,
                            "mulliganResp": {"decision": "MulliganOption_AcceptHand"},
                        },
                    ),
                    TS,
                )
            ),
        ),
        (
            "select_n_resp",
            _expect_one_event(
                client_actions.try_parse(
                    _client_to_gre_message(
                        request_id=4,
                        payload={
                            "type": "ClientMessageType_SelectNResp",
                            "gameStateId": 6,
                            "respId": 2,
                            "selectNResp": {"selectedOptionIds": [1], "selectedObjectIds": [2]},
                        },
                    ),
                    TS,
                )
            ),
        ),
        (
            "submit_deck_resp",
            _expect_one_event(
                client_actions.try_parse(
                    _client_to_gre_message(
                        request_id=5,
                        payload={
                            "type": "ClientMessageType_SubmitDeckResp",
                            "gameStateId": 7,
                            "respId": 3,
                            "submitDeckResp": {"deckCards": [11], "sideboardCards": [21]},
                        },
                    ),
                    TS,
                )
            ),
        ),
    ]


def _match_state_sample_events() -> list[tuple[str, events.BaseEvent]]:
    return [
        (
            "match_started",
            _expect_one_event(
                match_state.try_parse(
                    _match_state_entry(
                        {
                            "gameRoomInfo": {
                                "stateType": "MatchGameRoomStateType_Playing",
                                "gameRoomConfig": {
                                    "matchId": "schema-match",
                                    "eventId": "Traditional_Ladder",
                                    "reservedPlayers": [
                                        {
                                            "userId": "local-user",
                                            "playerName": "Local",
                                            "systemSeatId": 1,
                                            "teamId": 1,
                                        }
                                    ],
                                },
                            }
                        }
                    ),
                    TS,
                )
            ),
        ),
        (
            "match_completed",
            _expect_one_event(
                match_state.try_parse(
                    _match_state_entry(
                        {
                            "gameRoomInfo": {
                                "stateType": "MatchGameRoomStateType_MatchCompleted",
                                "gameRoomConfig": {"matchId": "schema-match"},
                                "finalMatchResult": {
                                    "matchCompletedReason": "MatchCompletedReasonType_Success",
                                    "resultList": [
                                        {
                                            "scope": "MatchScope_Match",
                                            "result": "ResultType_WinLoss",
                                            "winningTeamId": 1,
                                            "reason": "ResultReason_Game",
                                        }
                                    ],
                                },
                            }
                        }
                    ),
                    TS,
                )
            ),
        ),
        (
            "state_changed",
            _expect_one_event(
                match_state.try_parse(
                    _match_state_entry(
                        {
                            "gameRoomInfo": {
                                "stateType": "MatchGameRoomStateType_Sideboarding",
                                "gameRoomConfig": {"matchId": "schema-match"},
                            }
                        }
                    ),
                    TS,
                )
            ),
        ),
    ]


def _gre_sample_events() -> list[tuple[str, events.BaseEvent]]:
    game_state_event = _expect_one_event(
        gre.try_parse(
            _gre_entry(
                [
                    {
                        "type": "GREMessageType_GameStateMessage",
                        "msgId": 1,
                        "gameStateId": 2,
                        "systemSeatIds": [1, 2],
                        "gameStateMessage": {
                            "gameInfo": {
                                "matchID": "schema-match",
                                "gameNumber": 1,
                                "stage": "GameStage_Play",
                                "matchState": "MatchState_GameInProgress",
                            },
                            "turnInfo": {"turnNumber": 3, "activePlayer": 1},
                        },
                    }
                ]
            ),
            TS,
        )
    )
    queued_event = _expect_one_event(
        gre.try_parse(
            _gre_entry(
                [
                    {
                        "type": "GREMessageType_QueuedGameStateMessage",
                        "msgId": 3,
                        "gameStateId": 4,
                        "queuedGameStateMessage": {
                            "gameStateMessage": {
                                "gameInfo": {"matchID": "schema-match", "gameNumber": 1},
                            }
                        },
                    }
                ]
            ),
            TS,
        )
    )
    connect_resp_event = _expect_one_event(
        gre.try_parse(
            _gre_entry(
                [
                    {
                        "type": "GREMessageType_ConnectResp",
                        "msgId": 5,
                        "gameStateId": 6,
                        "systemSeatIds": [1, 2],
                        "connectResp": {
                            "deckMessage": {"deckCards": [11], "sideboardCards": [21]},
                            "settings": {"matchClockSec": 1800},
                        },
                    }
                ]
            ),
            TS,
        )
    )
    game_over_events = gre.try_parse(
        _gre_entry(
            [
                {
                    "type": "GREMessageType_GameStateMessage",
                    "msgId": 7,
                    "gameStateId": 8,
                    "gameStateMessage": {
                        "gameInfo": {
                            "stage": "GameStage_GameOver",
                            "matchState": "MatchState_GameComplete",
                            "results": [
                                {
                                    "scope": "MatchScope_Game",
                                    "winningTeamId": 1,
                                    "result": "ResultType_WinLoss",
                                    "reason": "ResultReason_Game",
                                }
                            ],
                        }
                    },
                }
            ]
        ),
        TS,
    )
    game_result_event = _expect_one_event(
        [event for event in game_over_events if isinstance(event, events.GameResultEvent)]
    )

    return [
        ("game_state_message", game_state_event),
        ("queued_game_state_message", queued_event),
        ("connect_resp", connect_resp_event),
        ("game_result", game_result_event),
    ]


def _truncation_sample_events() -> list[tuple[str, events.BaseEvent]]:
    return [
        (
            "game_state_message_truncation",
            _expect_one_event(
                truncation.try_parse(
                    LogEntry(
                        EntryHeader.TRUNCATION_MARKER,
                        "[Message summarized - GREMessageType_GameStateMessage payload omitted]\n"
                        "GameObject Count: 12\n"
                        "Annotation Count: 3",
                    ),
                    TS,
                )
            ),
        )
    ]


def _collection_sample_events() -> list[tuple[str, events.BaseEvent]]:
    parsed = collection.try_parse(
        _api_response_entry(
            "StartHook",
            {
                "PlayerCards": {"1001": 4},
                "DeckSummaries": [{"DeckId": "deck-1", "Name": "Schema Deck"}],
                "Decks": {"deck-1": {"MainDeck": [{"cardId": 1001, "quantity": 4}]}},
            },
        ),
        TS,
    )
    collection_events = _flatten_events(parsed)
    return [
        (
            "collection_snapshot",
            _expect_one_event([event for event in collection_events if event.kind == "Collection"]),
        ),
        (
            "deck_collection_snapshot",
            _expect_one_event([event for event in collection_events if event.kind == "DeckCollection"]),
        ),
    ]


def _small_parser_sample_events() -> list[tuple[str, events.BaseEvent]]:
    return [
        (
            "inventory_snapshot",
            _expect_one_event(
                inventory.try_parse(_api_response_entry("StartHook", {"InventoryInfo": {"Gold": 1000}}), TS)
            ),
        ),
        (
            "rank_snapshot",
            _expect_one_event(
                rank.try_parse(
                    _api_response_entry(
                        "RankGetCombinedRankInfo",
                        {
                            "constructedClass": "Mythic",
                            "constructedLevel": 1,
                            "limitedClass": "Gold",
                            "limitedLevel": 4,
                        },
                    ),
                    TS,
                )
            ),
        ),
        (
            "session_account_update",
            _expect_one_event(
                session.try_parse(
                    LogEntry(
                        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
                        "[UnityCrossThreadLogger]Updated account. DisplayName:Local, AccountID:account-1",
                    ),
                    TS,
                )
            ),
        ),
        (
            "session_authenticated",
            _expect_one_event(
                session.try_parse(
                    _api_response_entry(
                        "AuthenticateResponse",
                        {"displayName": "Local", "accountId": "account-1", "screenName": "LocalScreen"},
                    ),
                    TS,
                )
            ),
        ),
        (
            "session_logout",
            _expect_one_event(
                session.try_parse(
                    LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]User logout requested"),
                    TS,
                )
            ),
        ),
        (
            "event_join",
            _expect_one_event(
                event_lifecycle.try_parse(
                    LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]==> EventJoin"),
                    TS,
                )
            ),
        ),
        (
            "event_claim_prize",
            _expect_one_event(
                event_lifecycle.try_parse(
                    LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]==> EventClaimPrize"),
                    TS,
                )
            ),
        ),
        (
            "event_enter_pairing",
            _expect_one_event(
                event_lifecycle.try_parse(
                    LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]==> EventEnterPairing"),
                    TS,
                )
            ),
        ),
        (
            "detailed_logging_status",
            _expect_one_event(metadata.try_parse(LogEntry(EntryHeader.METADATA, "DETAILED LOGS: ENABLED"), TS)),
        ),
    ]


def _connection_sample_events() -> list[tuple[str, events.BaseEvent]]:
    return [
        (
            "state_changed",
            _expect_one_event(
                connection_state.try_parse(
                    _unity_json_entry("STATE CHANGED ", {"old": "Playing", "new": "Disconnected"}),
                    TS,
                )
            ),
        ),
        (
            "tcp_connection_close",
            _expect_one_event(
                connection_close.try_parse(
                    _unity_json_entry(
                        "Client.TcpConnection.Close ",
                        {"status": 7, "reason": "Closed by remote end", "host": "matchdoor.example", "port": 30003},
                    ),
                    TS,
                )
            ),
        ),
        (
            "websocket_closed",
            _expect_one_event(
                connection_close.try_parse(
                    _unity_json_entry(
                        "GREConnection.HandleWebSocketClosed ",
                        {"closeType": 1, "reason": "network"},
                    ),
                    TS,
                )
            ),
        ),
        (
            "unity_error_payload",
            _expect_one_event(
                connection_error.try_parse(
                    _unity_json_entry(
                        "TcpConnection.ProcessRead.Exception ",
                        {"message": "socket read failed", "code": 10054},
                    ),
                    TS,
                )
            ),
        ),
        (
            "reconnect_result",
            _expect_one_event(
                connection_error.try_parse(
                    LogEntry(EntryHeader.CONNECTION_MANAGER, "[ConnectionManager] Reconnect result : Error"),
                    TS,
                )
            ),
        ),
        (
            "reconnect_outcome",
            _expect_one_event(
                connection_error.try_parse(
                    LogEntry(
                        EntryHeader.CONNECTION_MANAGER,
                        "[ConnectionManager] Reconnect succeeded after 3 attempts",
                    ),
                    TS,
                )
            ),
        ),
        (
            "matchmaking_gre_connection_lost",
            _expect_one_event(
                connection_error.try_parse(
                    LogEntry(EntryHeader.MATCHMAKING, "Matchmaking: GRE connection lost, attempting reconnect"),
                    TS,
                )
            ),
        ),
    ]


def _client_to_gre_message(*, request_id: int, payload: dict[str, Any]) -> LogEntry:
    return _unity_json_entry(
        "ClientToGREMessage",
        {
            "requestId": request_id,
            "clientToMatchServiceMessageType": "ClientToMatchServiceMessageType_ClientToGREMessage",
            "payload": payload,
        },
    )


def _unity_json_entry(marker: str, payload: dict[str, Any]) -> LogEntry:
    return LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"[UnityCrossThreadLogger]{marker}\n{json.dumps(payload, sort_keys=True)}",
    )


def _api_response_entry(name: str, payload: dict[str, Any]) -> LogEntry:
    return LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"[UnityCrossThreadLogger]<== {name}\n{json.dumps(payload, sort_keys=True)}",
    )


def _match_state_entry(payload: dict[str, Any]) -> LogEntry:
    return _unity_json_entry("matchGameRoomStateChangedEvent", {"matchGameRoomStateChangedEvent": payload})


def _gre_entry(messages: list[dict[str, Any]]) -> LogEntry:
    return _unity_json_entry("greToClientEvent", {"greToClientEvent": {"greToClientMessages": messages}})


def _expect_one_event(value: events.BaseEvent | Sequence[events.BaseEvent] | None) -> events.BaseEvent:
    parsed_events = _flatten_events(value)
    if len(parsed_events) != 1:
        pytest.fail(f"Expected one schema sample event, got {len(parsed_events)}")
    return parsed_events[0]


def _flatten_events(value: events.BaseEvent | Sequence[events.BaseEvent] | None) -> list[events.BaseEvent]:
    if value is None:
        return []
    if isinstance(value, Sequence):
        return list(value)
    return [value]


def _workbook_row_key_snapshot() -> dict[str, Any]:
    summary = _schema_match_summary()
    match_log_row = summary.to_match_log_row()
    game_log_row = summary.to_game_sheet_rows()[0]

    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "current_landing_rows": {
            "GameLogRow": {
                "keys": list(game_log_row),
                "metadata": _row_metadata(game_log_row),
            },
            "MatchLogRow": {
                "keys": list(match_log_row),
                "metadata": _row_metadata(match_log_row),
            },
        },
        "sync_fields": {
            "GAME_LOG_SYNC_FIELDS": list(sheet_schema.GAME_LOG_SYNC_FIELDS),
            "MATCH_LOG_SYNC_FIELDS": list(sheet_schema.MATCH_LOG_SYNC_FIELDS),
        },
    }


def _schema_match_summary() -> models.MatchSummary:
    summary = models.MatchSummary(match_id="schema-match")
    summary.first_event_time = "2026-05-08T12:00:00+00:00"
    summary.last_event_time = "2026-05-08T12:30:00+00:00"
    summary.player_team = 1
    summary.match_winner_team = 1
    summary.constructed_rank = "Mythic 99.1"
    summary.constructed_class = "Mythic"
    summary.constructed_percentile = 99.1
    summary.event_id = "Traditional_Ladder"
    summary.super_format = "SuperFormat_Constructed"
    summary.match_win_condition = "MatchWinCondition_Best2of3"
    summary.sideboarding_entered = True
    summary.submit_deck_seen = True
    summary.touch_game(1, "2026-05-08T12:01:00+00:00")
    summary.touch_game(1, "2026-05-08T12:10:00+00:00")
    summary.set_game_starting_player(1, 1)
    summary.set_game_winner(1, 1)
    summary.set_game_mulligans(1, 1)
    summary.set_game_opening_hand(1, ["Forest", "Swamp", "Duress"])
    summary.add_game_mulliganed_away(1, ["Cut Down"])
    summary.set_game_turn_count(1, 7)
    return summary


def _row_metadata(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_family": row["event_family"],
        "event_type": row["event_type"],
        "scope": row["scope"],
    }


def _sheet_schema_surface_snapshot() -> dict[str, Any]:
    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "runtime_sheet_specs": {
            family: {
                "event_type": spec.event_type,
                "headers": list(spec.headers),
                "scope": spec.scope,
            }
            for family, spec in sheet_schema.RUNTIME_SHEET_SPECS.items()
        },
        "sync_fields": {
            "game_log": list(sheet_schema.GAME_LOG_SYNC_FIELDS),
            "match_log": list(sheet_schema.MATCH_LOG_SYNC_FIELDS),
        },
        "sync_fields_by_row_kind": {
            row_kind: list(sync_fields)
            for row_kind, sync_fields in sheet_schema.SYNC_FIELDS_BY_ROW_KIND.items()
        },
    }


def _runtime_export_row_key_snapshot() -> dict[str, Any]:
    rows_by_family = _runtime_export_rows_by_family()

    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "runtime_export_rows": {
            family: {
                "keys": list(row),
                "metadata": _row_metadata(row),
            }
            for family, row in rows_by_family.items()
        },
    }


def _runtime_export_rows_by_family() -> dict[str, dict[str, Any]]:
    sheet_exports.reset_sheet_export_state()
    try:
        rows = sheet_exports.collect_runtime_sheet_rows(
            action_payload={
                "generated_at": "stable-generated-at",
                "entries": [
                    {
                        "match_id": "schema-match",
                        "game_number": 1,
                        "turn_number": 3,
                        "timestamp": "stable-action-time",
                        "action_type": "spell_cast",
                        "cast_mode": "normal",
                        "grp_id": 1001,
                        "card_name": "Schema Card",
                        "display_name": "Schema Card",
                        "resolution_status": "confirmed",
                        "actor_relation": "local",
                        "from_zone_type": "ZoneType_Hand",
                        "to_zone_type": "ZoneType_Stack",
                        "summary": "schema action",
                    }
                ],
            },
            deck_payload={
                "generated_at": "stable-generated-at",
                "submitted_at": "stable-submitted-at",
                "match_id": "schema-match",
                "signature": "schema-deck-signature",
                "matched_decks": [{"name": "Schema Deck", "match_mode": "exact", "format": "TraditionalStandard"}],
                "mainboard": [
                    {
                        "arena_id": 1001,
                        "count": 4,
                        "section": "mainboard",
                        "name": "Schema Card",
                        "rarity": "common",
                        "set": "SCH",
                        "type_line": "Creature",
                        "colors": ["G"],
                        "owned_copies": 4,
                        "missing_copies": 0,
                    }
                ],
                "sideboard": [],
            },
            collection_payload={
                "generated_at": "stable-generated-at",
                "collection_available": True,
                "inventory_available": True,
                "owned_unique_cards": 1,
                "owned_total_card_copies": 4,
                "owned_by_rarity": {"common": 4},
                "inventory": {"gold": 1000, "gems": 250},
                "active_deck_missing_by_rarity": {"rare": 0},
                "active_deck_completion": {"completion_rate": 1.0},
                "wanted_cards": [],
            },
            status_payload={
                "updated_at": "stable-updated-at",
                "status": "running",
                "current_match_id": "schema-match",
                "current_game_number": 1,
                "current_player_team": 1,
                "last_event_kind": "GameState",
                "last_event_at": "stable-event-at",
                "webhook_successes": 1,
                "webhook_failures": 0,
                "event_failures": 0,
                "router_failures": 0,
                "active_deck_signature": "schema-deck-signature",
                "active_deck_name": "Schema Deck",
                "active_match_action_count": 1,
            },
            card_performance_payload={
                "generated_at": "stable-generated-at",
                "cards": [
                    {
                        "card_key": "grp:1001",
                        "grp_id": 1001,
                        "card_name": "Schema Card",
                        "display_name": "Schema Card",
                        "resolution_status": "confirmed",
                        "layout": "normal",
                        "card_faces": [],
                        "games_seen": 1,
                        "seen_in_game_games": 1,
                        "seen_in_game_win_rate": 1.0,
                        "opening_hand_games": 1,
                        "opening_hand_win_rate": 1.0,
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
    finally:
        sheet_exports.reset_sheet_export_state()

    return {row["event_family"]: row for row in rows}


def _apps_script_repo_parity_snapshot() -> dict[str, Any]:
    code = APPS_SCRIPT_PATH.read_text(encoding="utf-8")
    all_dispatch_families = _extract_apps_script_dispatch_families(code)
    dispatch_under_test = [
        family for family in all_dispatch_families if family in _APPS_SCRIPT_DISPATCH_FAMILIES_UNDER_TEST
    ]
    runtime_build_headers = {
        family: _extract_apps_script_return_object_keys(code, function_name)
        for family, function_name in _RUNTIME_FAMILY_TO_APPS_SCRIPT_BUILD_FUNCTION.items()
    }

    return {
        "schema_snapshot_version": SNAPSHOT_VERSION,
        "dispatch_event_families_under_test": dispatch_under_test,
        "game_log_field_map_keys": _extract_apps_script_return_object_keys(code, "buildGameLogFieldMap_"),
        "match_log_field_map_keys": _extract_apps_script_return_object_keys(code, "buildMatchLogFieldMap_"),
        "runtime_build_object_data_keys": {
            family: _extract_apps_script_data_keys(code, function_name)
            for family, function_name in _RUNTIME_FAMILY_TO_APPS_SCRIPT_BUILD_FUNCTION.items()
        },
        "runtime_build_object_headers": runtime_build_headers,
        "runtime_landing_headers": {
            header_key: _extract_apps_script_landing_headers(code, header_key)
            for header_key in _RUNTIME_FAMILY_TO_APPS_SCRIPT_HEADER_KEY.values()
        },
    }


def _extract_apps_script_dispatch_families(code: str) -> list[str]:
    return re.findall(r'data\.event_family\s*===\s*"([^"]+)"', code)


def _extract_apps_script_landing_headers(code: str, header_key: str) -> list[str]:
    match = re.search(rf"\b{re.escape(header_key)}:\s*\[(?P<body>.*?)^\s*\],", code, re.MULTILINE | re.DOTALL)
    if match is None:
        pytest.fail(f"Could not find Apps Script landing header array {header_key}")
    assert match is not None
    return re.findall(r'"([^"]+)"', match.group("body"))


def _extract_apps_script_return_object_keys(code: str, function_name: str) -> list[str]:
    body = _extract_apps_script_function_body(code, function_name)
    return re.findall(r'^\s*"([^"]+)":', body, re.MULTILINE)


def _extract_apps_script_data_keys(code: str, function_name: str) -> list[str]:
    body = _extract_apps_script_function_body(code, function_name)
    dot_keys = re.findall(r"\bdata\.([A-Za-z_][A-Za-z0-9_]*)", body)
    bracket_keys = re.findall(r'data\["([^"]+)"\]', body)
    return sorted(set(dot_keys + bracket_keys))


def _extract_apps_script_function_body(code: str, function_name: str) -> str:
    match = re.search(
        rf"function {re.escape(function_name)}\(data\) {{(?P<body>.*?)^}}",
        code,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        pytest.fail(f"Could not find Apps Script function {function_name}")
    assert match is not None
    return match.group("body")
