from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import pytest

from mythic_edge_parser import parsers
from mythic_edge_parser.events import DraftCompleteEvent, PerformanceClass
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import draft_complete
from mythic_edge_parser.router import Router

TS = datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC)


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


def test_draft_complete_response_emits_contract_payload() -> None:
    payload = {
        "draftId": " draft-1 ",
        "eventName": " PremierDraft_Example ",
        "queueId": " PremierDraft ",
        "draftStatus": " Open ",
        "completionStatus": " Complete ",
        "draftType": " HumanDraft ",
        "draftMode": " Premier ",
        "completionSource": " ArenaCompletion ",
        "isBotDraft": False,
        "isHumanDraft": True,
    }
    entry = _api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, payload)

    event = draft_complete.try_parse(entry, TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.kind == "DraftComplete"
    assert event.performance_class == PerformanceClass.DURABLE_PER_EVENT
    assert event.metadata.timestamp is TS
    assert event.metadata.raw_bytes == entry.body.encode()
    assert event.payload == {
        "type": "draft_complete_draft",
        "source_method": "DraftCompleteDraft",
        "api_direction": "response",
        "draft_id": "draft-1",
        "event_id": "PremierDraft_Example",
        "queue_id": "PremierDraft",
        "draft_status": "Open",
        "completion_status": "Complete",
        "draft_type": "HumanDraft",
        "draft_mode": "Premier",
        "completion_source": "ArenaCompletion",
        "is_bot_draft": False,
        "is_human_draft": True,
        "raw_draft_complete": payload,
    }


def test_draft_complete_request_marker_wrapped_payload_uses_nested_fields() -> None:
    payload = {
        "DraftCompleteDraft": {
            "DraftId": "draft-2",
            "EventName": "TraditionalDraft_FDN",
            "EventQueueId": "TraditionalDraft",
            "state": "Submitted",
            "Result": "Complete",
            "DraftCategory": "HumanDraft",
            "Mode": "Traditional",
            "Source": "DraftCompleteDraft",
            "BotDraft": False,
            "HumanDraft": True,
        },
        "ignored": {"draftId": "top-level"},
    }
    entry = _api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, payload, direction="==>")

    event = draft_complete.try_parse(entry, TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload["api_direction"] == "request"
    assert event.payload["draft_id"] == "draft-2"
    assert event.payload["event_id"] == "TraditionalDraft_FDN"
    assert event.payload["queue_id"] == "TraditionalDraft"
    assert event.payload["draft_status"] == "Submitted"
    assert event.payload["completion_status"] == "Complete"
    assert event.payload["draft_type"] == "HumanDraft"
    assert event.payload["draft_mode"] == "Traditional"
    assert event.payload["completion_source"] == "DraftCompleteDraft"
    assert event.payload["is_bot_draft"] is False
    assert event.payload["is_human_draft"] is True
    assert event.payload["raw_draft_complete"] == payload


def test_draft_complete_defaults_missing_optional_fields() -> None:
    event = draft_complete.try_parse(_api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, {}), TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload == {
        "type": "draft_complete_draft",
        "source_method": "DraftCompleteDraft",
        "api_direction": "response",
        "draft_id": "",
        "event_id": "",
        "queue_id": "",
        "draft_status": "",
        "completion_status": "",
        "draft_type": "",
        "draft_mode": "",
        "completion_source": "DraftCompleteDraft",
        "is_bot_draft": None,
        "is_human_draft": None,
        "raw_draft_complete": {},
    }


def test_draft_complete_nested_non_mapping_uses_top_level_payload() -> None:
    payload = {
        "DraftCompleteDraft": "not-a-mapping",
        "eventName": "QuickDraft_FDN",
        "completionStatus": "Done",
    }

    event = draft_complete.try_parse(_api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, payload), TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload["event_id"] == "QuickDraft_FDN"
    assert event.payload["completion_status"] == "Done"
    assert event.payload["raw_draft_complete"] == payload


@pytest.mark.parametrize("bad_value", [None, True, False, 0, 1, 1.2, [], {}, {"value": "draft"}])
def test_draft_complete_string_fields_reject_non_strings(bad_value: Any) -> None:
    payload = {
        "draftId": bad_value,
        "eventName": bad_value,
        "queueId": bad_value,
        "draftStatus": bad_value,
        "completionStatus": bad_value,
        "draftType": bad_value,
        "draftMode": bad_value,
        "completionSource": bad_value,
    }

    event = draft_complete.try_parse(_api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, payload), TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload["draft_id"] == ""
    assert event.payload["event_id"] == ""
    assert event.payload["queue_id"] == ""
    assert event.payload["draft_status"] == ""
    assert event.payload["completion_status"] == ""
    assert event.payload["draft_type"] == ""
    assert event.payload["draft_mode"] == ""
    assert event.payload["completion_source"] == "DraftCompleteDraft"


@pytest.mark.parametrize("bad_value", ["true", "false", 0, 1, 1.0, [], {}, None])
def test_draft_complete_boolean_fields_accept_only_real_booleans(bad_value: Any) -> None:
    payload = {
        "isBotDraft": bad_value,
        "isHumanDraft": bad_value,
    }

    event = draft_complete.try_parse(_api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, payload), TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload["is_bot_draft"] is None
    assert event.payload["is_human_draft"] is None


@pytest.mark.parametrize(
    "body",
    [
        "[UnityCrossThreadLogger]<== DraftCompleteDraft\nnot json",
        "[UnityCrossThreadLogger]<== DraftCompleteDraft\n[1, 2, 3]",
        "[UnityCrossThreadLogger]<== DraftCompleteDraft",
    ],
)
def test_draft_complete_malformed_marker_like_input_returns_none(body: str) -> None:
    assert draft_complete.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS) is None


@pytest.mark.parametrize(
    "body",
    [
        "[UnityCrossThreadLogger]<== draftcompletedraft\n{}",
        "[UnityCrossThreadLogger]<== DraftCompleteDraftExtra\n{}",
        "[UnityCrossThreadLogger]<== DraftCompleteDraft.Extra\n{}",
        '[UnityCrossThreadLogger]<== BotDraftDraftStatus\n{"draftId":"draft"}',
        '[UnityCrossThreadLogger]<== BotDraftDraftPick\n{"pickedCardId":1001}',
        '[UnityCrossThreadLogger]<== Draft.Notify\n{"PickGrpId":1001}',
        '[UnityCrossThreadLogger]<== EventPlayerDraftMakePick\n{"PickGrpId":1001}',
        '[UnityCrossThreadLogger]<== LogBusinessEvents\n{"PickGrpId":1001}',
        '[UnityCrossThreadLogger]PickGrpId appears in prose\n{"PickGrpId":1001}',
        "[UnityCrossThreadLogger]generic prose mentions DraftCompleteDraft but is not an API marker\n{}",
    ],
)
def test_draft_complete_ignores_case_variants_other_draft_markers_and_prose(body: str) -> None:
    assert draft_complete.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS) is None


def test_draft_complete_first_marker_policy_is_deterministic() -> None:
    body = (
        "[UnityCrossThreadLogger]==> DraftCompleteDraft "
        "<== DraftCompleteDraft\n"
        '{"draftId":"draft-3"}'
    )

    event = draft_complete.try_parse(LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body), TS)

    assert isinstance(event, DraftCompleteEvent)
    assert event.payload["api_direction"] == "request"
    assert event.payload["draft_id"] == "draft-3"


def test_draft_complete_package_import_is_public() -> None:
    assert parsers.draft_complete is draft_complete
    assert "draft_complete" in parsers.__all__


@pytest.mark.parametrize(
    "entry",
    [
        _api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, {"draftId": "draft-4"}),
        _unknown_api_entry(draft_complete.DRAFT_COMPLETE_DRAFT_MARKER, {"draftId": "draft-5"}, direction="==>"),
    ],
)
def test_draft_complete_routes_from_unity_and_unknown_headers(entry: LogEntry) -> None:
    test_router = Router()

    routed = test_router.route(entry)

    assert len(routed) == 1
    assert routed[0].kind == "DraftComplete"
    assert test_router.stats.routed == 1
    assert test_router.stats.unknown == 0
    assert test_router.stats.timestamp_missing == 1


def test_draft_complete_router_preserves_draft_bot_and_human_precedence() -> None:
    test_router = Router()

    bot_routed = test_router.route(_api_entry("BotDraftDraftPick", {"pickedCardId": 8001}, direction="==>"))
    human_routed = test_router.route(_api_entry("Draft.Notify", {"draftId": "draft", "pickedCardId": 8002}))

    assert [event.kind for event in bot_routed] == ["DraftBot"]
    assert [event.kind for event in human_routed] == ["DraftHuman"]
