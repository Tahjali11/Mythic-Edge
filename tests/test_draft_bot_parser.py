from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import pytest

from mythic_edge_parser import parsers
from mythic_edge_parser.events import DraftBotEvent, PerformanceClass
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import draft_bot
from mythic_edge_parser.router import Router

TS = datetime(2026, 5, 18, 12, 0, 0, tzinfo=UTC)


def _api_entry(method: str, payload: Any, *, direction: str = "<==") -> LogEntry:
    return LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"[UnityCrossThreadLogger]{direction} {method}\n{json.dumps(payload, sort_keys=True)}",
    )


def _unknown_api_entry(method: str, payload: Any, *, direction: str = "<==") -> LogEntry:
    return LogEntry(
        EntryHeader.UNKNOWN,
        f"[UnityCrossThreadLogger]{direction} {method}\n{json.dumps(payload, sort_keys=True)}",
    )


def test_draft_bot_status_response_emits_contract_payload() -> None:
    payload = {
        "draftId": " draft-1 ",
        "eventName": " QuickDraft_Example ",
        "draftStatus": " PackOpen ",
        "packNumber": 1,
        "pickNumber": 2,
        "packCards": [1001, "1002", 1002],
        "pickedCardId": 1001,
        "pickedCardIds": [1001, "1003"],
    }
    entry = _api_entry(draft_bot.BOT_DRAFT_STATUS_MARKER, payload)

    event = draft_bot.try_parse(entry, TS)

    assert isinstance(event, DraftBotEvent)
    assert event.kind == "DraftBot"
    assert event.performance_class == PerformanceClass.DURABLE_PER_EVENT
    assert event.metadata.timestamp is TS
    assert event.metadata.raw_bytes == entry.body.encode()
    assert event.payload == {
        "type": "bot_draft_status",
        "source_method": "BotDraftDraftStatus",
        "api_direction": "response",
        "draft_id": "draft-1",
        "event_id": "QuickDraft_Example",
        "draft_status": "PackOpen",
        "pack_number": 1,
        "pick_number": 2,
        "pack_card_ids": [1001, 1002, 1002],
        "picked_card_id": 1001,
        "picked_card_ids": [1001, 1003],
        "raw_draft_bot": payload,
    }


def test_draft_bot_pick_request_marker_wrapped_payload_uses_nested_fields() -> None:
    payload = {
        "BotDraftDraftPick": {
            "DraftId": "draft-2",
            "EventId": "QuickDraft_FDN",
            "status": "Submitted",
            "PackNumber": "003",
            "PickNumber": "4",
            "DraftPack": ["2001", 2002],
            "PickGrpId": "2002",
            "PickedGrpIds": ["2002", "2003"],
        },
        "ignored": {"draftId": "top-level"},
    }
    entry = _api_entry(draft_bot.BOT_DRAFT_PICK_MARKER, payload, direction="==>")

    event = draft_bot.try_parse(entry, TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["type"] == "bot_draft_pick"
    assert event.payload["source_method"] == "BotDraftDraftPick"
    assert event.payload["api_direction"] == "request"
    assert event.payload["draft_id"] == "draft-2"
    assert event.payload["event_id"] == "QuickDraft_FDN"
    assert event.payload["draft_status"] == "Submitted"
    assert event.payload["pack_number"] == 3
    assert event.payload["pick_number"] == 4
    assert event.payload["pack_card_ids"] == [2001, 2002]
    assert event.payload["picked_card_id"] == 2002
    assert event.payload["picked_card_ids"] == [2002, 2003]
    assert event.payload["raw_draft_bot"] == payload


def test_draft_bot_defaults_missing_optional_fields() -> None:
    event = draft_bot.try_parse(_api_entry(draft_bot.BOT_DRAFT_STATUS_MARKER, {}), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload == {
        "type": "bot_draft_status",
        "source_method": "BotDraftDraftStatus",
        "api_direction": "response",
        "draft_id": "",
        "event_id": "",
        "draft_status": "",
        "pack_number": None,
        "pick_number": None,
        "pack_card_ids": [],
        "picked_card_id": None,
        "picked_card_ids": [],
        "raw_draft_bot": {},
    }


def test_draft_bot_nested_non_mapping_uses_top_level_payload() -> None:
    payload = {
        "BotDraftDraftPick": "not-a-mapping",
        "pickNumber": 5,
        "pickedCardIds": ["3001", "3002"],
    }

    event = draft_bot.try_parse(_api_entry(draft_bot.BOT_DRAFT_PICK_MARKER, payload), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["pick_number"] == 5
    assert event.payload["picked_card_id"] == 3001
    assert event.payload["picked_card_ids"] == [3001, 3002]
    assert event.payload["raw_draft_bot"] == payload


@pytest.mark.parametrize(
    "bad_value",
    [True, False, -1, "-1", "+1", "1.0", " ", 1.2, [], {}, {"value": 1}],
)
def test_draft_bot_rejects_invalid_scalar_integers(bad_value: Any) -> None:
    payload = {
        "packNumber": bad_value,
        "pickNumber": bad_value,
        "pickedCardId": bad_value,
        "pickedCardIds": [4001],
    }

    event = draft_bot.try_parse(_api_entry(draft_bot.BOT_DRAFT_PICK_MARKER, payload), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["pack_number"] is None
    assert event.payload["pick_number"] is None
    assert event.payload["picked_card_id"] is None


def test_draft_bot_rejects_invalid_card_list_members_without_raising() -> None:
    payload = {
        "packCards": [1, "2", True, False, -3, "-4", "+5", "6.0", "", [], {}, 7, "007"],
        "pickedCards": [8, "9", -10, True, {"bad": 11}],
    }

    event = draft_bot.try_parse(_api_entry(draft_bot.BOT_DRAFT_STATUS_MARKER, payload), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["pack_card_ids"] == [1, 2, 7, 7]
    assert event.payload["picked_card_ids"] == [8, 9]
    assert event.payload["picked_card_id"] == 8


@pytest.mark.parametrize("container", [None, "1001", {"card": 1001}, 1001, True])
def test_draft_bot_non_list_card_containers_default_to_empty(container: Any) -> None:
    payload = {"packCards": container, "pickedCards": container}

    event = draft_bot.try_parse(_api_entry(draft_bot.BOT_DRAFT_STATUS_MARKER, payload), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["pack_card_ids"] == []
    assert event.payload["picked_card_ids"] == []
    assert event.payload["picked_card_id"] is None


def test_draft_bot_first_marker_policy_is_deterministic() -> None:
    body = (
        "[UnityCrossThreadLogger]==> BotDraftDraftPick "
        "<== BotDraftDraftStatus\n"
        '{"draftId":"draft-3","pickedCardId":5001}'
    )

    event = draft_bot.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS)

    assert isinstance(event, DraftBotEvent)
    assert event.payload["type"] == "bot_draft_pick"
    assert event.payload["source_method"] == "BotDraftDraftPick"
    assert event.payload["api_direction"] == "request"


@pytest.mark.parametrize(
    "body",
    [
        "[UnityCrossThreadLogger]<== BotDraftDraftPick\nnot json",
        "[UnityCrossThreadLogger]<== BotDraftDraftPick\n[1, 2, 3]",
        "[UnityCrossThreadLogger]<== BotDraftDraftPick",
    ],
)
def test_draft_bot_malformed_marker_like_input_returns_none(body: str) -> None:
    assert draft_bot.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS) is None


@pytest.mark.parametrize(
    "body",
    [
        "[UnityCrossThreadLogger]<== botdraftdraftpick\n{}",
        '[UnityCrossThreadLogger]<== Draft.Notify\n{"PickGrpId":1001}',
        '[UnityCrossThreadLogger]<== EventPlayerDraftMakePick\n{"PickGrpId":1001}',
        '[UnityCrossThreadLogger]<== LogBusinessEvents\n{"PickGrpId":1001}',
        "[UnityCrossThreadLogger]<== DraftCompleteDraft\n{}",
        "[UnityCrossThreadLogger]generic prose about bot draft pick pack\n{}",
    ],
)
def test_draft_bot_ignores_case_variants_human_draft_completion_and_prose(body: str) -> None:
    assert draft_bot.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS) is None


def test_draft_bot_package_import_is_public() -> None:
    assert parsers.draft_bot is draft_bot
    assert "draft_bot" in parsers.__all__


@pytest.mark.parametrize(
    "entry",
    [
        _api_entry(draft_bot.BOT_DRAFT_STATUS_MARKER, {"draftId": "draft-4"}),
        _unknown_api_entry(draft_bot.BOT_DRAFT_PICK_MARKER, {"pickedCardId": 6001}, direction="==>"),
    ],
)
def test_draft_bot_routes_from_unity_and_unknown_headers(entry: LogEntry) -> None:
    test_router = Router()

    routed = test_router.route(entry)

    assert len(routed) == 1
    assert routed[0].kind == "DraftBot"
    assert test_router.stats.routed == 1
    assert test_router.stats.unknown == 0
    assert test_router.stats.timestamp_missing == 1


def test_draft_bot_router_preserves_existing_parser_precedence() -> None:
    test_router = Router()

    routed = test_router.route(
        LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]==> EventJoin\n{}")
    )

    assert len(routed) == 1
    assert routed[0].kind == "EventLifecycle"
