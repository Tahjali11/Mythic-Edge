import json
from datetime import UTC, datetime
from typing import Any

import pytest

from mythic_edge_parser.events import PerformanceClass
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import client_actions

TS = datetime(2026, 5, 8, 5, 45, 19, tzinfo=UTC)
SYNTHETIC_UNITY_LOGGER_MARKER = "[UnityCrossThreadLogger]"  # test marker
SYNTHETIC_CLIENT_TO_GRE_MARKER = "ClientToGREMessage"  # test marker
SYNTHETIC_CLIENT_TO_GRE_UI_LOWERCASE_PREFIX = "ClientToGreuimessage"  # test marker
SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX = "ClientToGremessage"  # test marker


def _entry(body: str) -> LogEntry:
    return LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body)


def _entry_from_envelope(envelope: object, *, prefix_marker: str = SYNTHETIC_CLIENT_TO_GRE_MARKER) -> LogEntry:
    return _entry(f"{SYNTHETIC_UNITY_LOGGER_MARKER}{prefix_marker}\n{json.dumps(envelope)}")


def _gre_envelope(payload: Any, request_id: Any = 1) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "clientToMatchServiceMessageType": f"ClientToMatchServiceMessageType_{SYNTHETIC_CLIENT_TO_GRE_MARKER}",
    }
    if request_id is not _MISSING:
        envelope["requestId"] = request_id
    if payload is not _MISSING:
        envelope["payload"] = payload
    return envelope


def _ui_envelope(payload: Any, request_id: Any = 1) -> dict[str, Any]:
    return {
        "requestId": request_id,
        "clientToMatchServiceMessageType": "ClientToMatchServiceMessageType_ClientToGREUIMessage",
        "payload": payload,
    }


_MISSING = object()


def test_client_actions_parse_ui_message_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_UI_LOWERCASE_PREFIX}\n"
        '{"requestId":297,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREUIMessage","payload":{"type":"ClientMessageType_UIMessage","systemSeatId":1,"uiMessage":{"seatIds":[2],"onHover":{"objectId":401}}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "client_ui_message"
    assert event.payload["raw_client_action"]["payload"]["uiMessage"]["onHover"]["objectId"] == 401


def test_client_actions_event_metadata_uses_timestamp_raw_bytes_and_interactive_class() -> None:
    entry = _entry_from_envelope(
        _ui_envelope({"type": "ClientMessageType_UIMessage"}),
        prefix_marker="client-to-gre-ui-message-lowercase-prefix",
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "ClientAction"
    assert event.performance_class == PerformanceClass.INTERACTIVE_DISPATCH
    assert event.metadata.timestamp is TS
    assert event.metadata.raw_bytes == entry.body.encode()


def test_client_actions_classifies_from_json_enum_when_prefix_casing_differs() -> None:
    entry = _entry_from_envelope(
        _gre_envelope({"type": "ClientMessageType_ChooseStartingPlayerResp"}),
        prefix_marker="client-to-gre-message-lowercase-prefix",
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"


def test_client_actions_ui_marker_wins_when_body_contains_both_markers() -> None:
    entry = _entry_from_envelope(
        _ui_envelope({"type": "ClientMessageType_UIMessage"}),
        prefix_marker=SYNTHETIC_CLIENT_TO_GRE_MARKER,
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "client_ui_message"


def test_client_actions_parse_generic_message_type() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":2,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage","payload":{"type":"ClientMessageType_ChooseStartingPlayerResp","gameStateId":1,'
        '"respId":2}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"


@pytest.mark.parametrize(
    "inner_payload",
    [
        {},
        {"type": ""},
        {"type": "   "},
        {"type": None},
    ],
)
def test_client_actions_generic_fallback_allows_missing_or_blank_message_type(inner_payload: dict[str, Any]) -> None:
    entry = _entry_from_envelope(_gre_envelope(inner_payload))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == ""
    assert event.payload["raw_client_action"]["payload"] == inner_payload


def test_client_actions_generic_fallback_preserves_stringified_raw_payload() -> None:
    inner_payload = '{"type":"ClientMessageType_ChooseStartingPlayerResp","gameStateId":1,"respId":2}'
    entry = _entry_from_envelope(_gre_envelope(inner_payload))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"
    assert event.payload["raw_client_action"]["payload"] == inner_payload


def test_client_actions_parse_mulligan_response() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":6,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage","payload":{"type":"ClientMessageType_MulliganResp","gameStateId":5,"respId":1,'
        '"mulliganResp":{"decision":"MulliganOption_AcceptHand"}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "mulligan_resp"
    assert event.payload["decision"] == "keep"
    assert event.payload["request_id"] == 6


@pytest.mark.parametrize(
    ("decision", "expected"),
    [
        ("MulliganOption_Mulligan", "mulligan"),
        ("MulliganOption_AcceptHand", "keep"),
        ("MulliganOption_UnknownFutureValue", "MulliganOption_UnknownFutureValue"),
        ("", ""),
        (None, ""),
    ],
)
def test_client_actions_mulligan_decision_normalization(decision: Any, expected: str) -> None:
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_MulliganResp",
                "mulliganResp": {"decision": decision},
            },
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "mulligan_resp"
    assert event.payload["decision"] == expected


@pytest.mark.parametrize("mulligan_payload", [_MISSING, None, "bad", ["bad"], 0])
def test_client_actions_mulligan_malformed_payload_defaults_to_blank_decision(mulligan_payload: Any) -> None:
    inner: dict[str, Any] = {"type": "ClientMessageType_MulliganResp"}
    if mulligan_payload is not _MISSING:
        inner["mulliganResp"] = mulligan_payload
    entry = _entry_from_envelope(_gre_envelope(inner))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "mulligan_resp"
    assert event.payload["decision"] == ""


def test_client_actions_parse_select_n_response() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":101,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage","payload":{"type":"ClientMessageType_SelectNResp","gameStateId":9,"respId":3,'
        '"selectNResp":{"selectedOptionIds":[1,2],"selectedObjectIds":["9","10"]}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "select_n_resp"
    assert event.payload["selected_option_ids"] == [1, 2]
    assert event.payload["selected_object_ids"] == [9, 10]


def test_client_actions_select_n_filters_malformed_selected_ids() -> None:
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_SelectNResp",
                "selectNResp": {
                    "selectedOptionIds": [1, True, "2", " 3 ", "-4", 5.5, {}, [], None, "bad", 0],
                    "selectedObjectIds": [False, "9", "010", "-11", 12.0, {"id": 13}, [14]],
                },
            },
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "select_n_resp"
    assert event.payload["selected_option_ids"] == [1, 2, 3, 0]
    assert event.payload["selected_object_ids"] == [9, 10]


@pytest.mark.parametrize("select_payload", [_MISSING, None, "bad", {"selectedOptionIds": "bad"}, 0])
def test_client_actions_select_n_malformed_payload_defaults_to_empty_lists(select_payload: Any) -> None:
    inner: dict[str, Any] = {"type": "ClientMessageType_SelectNResp"}
    if select_payload is not _MISSING:
        inner["selectNResp"] = select_payload
    entry = _entry_from_envelope(_gre_envelope(inner))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "select_n_resp"
    assert event.payload["selected_option_ids"] == []
    assert event.payload["selected_object_ids"] == []


def test_client_actions_parse_submit_deck_with_nested_deck_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":10,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage","payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,'
        '"submitDeckResp":{"deck":{"deckCards":[11,12,13],"sideboardCards":[21,22]}}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [11, 12, 13]
    assert event.payload["sideboard_cards"] == [21, 22]


def test_client_actions_parse_submit_deck_direct_sources_take_precedence_when_truthy() -> None:
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_SubmitDeckResp",
                "submitDeckResp": {
                    "deckCards": [1, "2"],
                    "sideboardCards": [3, "4"],
                    "deck": {"deckCards": [11], "sideboardCards": [12]},
                    "sideboard": [13],
                },
            },
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [1, 2]
    assert event.payload["sideboard_cards"] == [3, 4]


def test_client_actions_parse_submit_deck_list_valued_deck_and_sideboard_fallbacks() -> None:
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_SubmitDeckResp",
                "submitDeckResp": {
                    "deck": [11, "12", True, "-13", 14.5, {}, [], None, "bad"],
                    "sideboard": [21, "22", False, "-23", 24.5],
                },
            },
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [11, 12]
    assert event.payload["sideboard_cards"] == [21, 22]


def test_client_actions_submit_deck_preserves_synthetic_large_deck_list_shape() -> None:
    synthetic_deck_cards = list(range(900000, 900080))
    synthetic_sideboard_cards = [910001, 910002, 910003]
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_SubmitDeckResp",
                "gameStateId": 494,
                "respId": 8,
                "submitDeckResp": {
                    "deckCards": synthetic_deck_cards,
                    "sideboardCards": synthetic_sideboard_cards,
                },
            },
            request_id=4940,
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "ClientAction"
    assert event.payload["type"] == "submit_deck_resp"
    assert len(event.payload["deck_cards"]) == 80
    assert len(event.payload["deck_cards"]) > 60
    assert event.payload["deck_cards"] == synthetic_deck_cards
    assert event.payload["sideboard_cards"] == synthetic_sideboard_cards
    assert event.payload["game_state_id"] == 494
    assert event.payload["resp_id"] == 8
    assert event.payload["request_id"] == 4940
    assert event.payload["raw_client_action"]["payload"]["submitDeckResp"]["deckCards"] == (
        synthetic_deck_cards
    )


def test_client_actions_parse_submit_deck_truthy_malformed_direct_source_blocks_nested_fallback() -> None:
    entry = _entry_from_envelope(
        _gre_envelope(
            {
                "type": "ClientMessageType_SubmitDeckResp",
                "submitDeckResp": {
                    "deckCards": "not-a-list",
                    "sideboardCards": "not-a-list",
                    "deck": {"deckCards": [11], "sideboardCards": [21]},
                },
            },
        ),
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == []
    assert event.payload["sideboard_cards"] == []


@pytest.mark.parametrize("submit_payload", [_MISSING, None, "bad", 0])
def test_client_actions_submit_deck_malformed_payload_defaults_to_empty_lists(submit_payload: Any) -> None:
    inner: dict[str, Any] = {"type": "ClientMessageType_SubmitDeckResp"}
    if submit_payload is not _MISSING:
        inner["submitDeckResp"] = submit_payload
    entry = _entry_from_envelope(_gre_envelope(inner))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == []
    assert event.payload["sideboard_cards"] == []


def test_client_actions_parse_stringified_inner_payload_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":12,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage",'
        '"payload":"{\\"type\\":\\"ClientMessageType_ChooseStartingPlayerResp\\",\\"gameStateId\\":1,\\"respId\\":2}"}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"


@pytest.mark.parametrize(
    "payload",
    [
        _MISSING,
        None,
        0,
        ["bad"],
        "not-json",
        "[1, 2, 3]",
        '"not-a-dict"',
    ],
)
def test_client_actions_gre_missing_or_non_dict_inner_payload_returns_none(payload: Any) -> None:
    entry = _entry_from_envelope(_gre_envelope(payload))

    assert client_actions.try_parse(entry, TS) is None


@pytest.mark.parametrize(
    "body",
    [
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_MARKER}\nnot-json",
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_MARKER}\n[1, 2, 3]",
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_MARKER}\n\"not-a-dict\"",
    ],
)
def test_client_actions_marker_present_without_dict_json_envelope_returns_none(body: str) -> None:
    assert client_actions.try_parse(_entry(body), TS) is None


def test_client_actions_submit_deck_tolerates_malformed_nested_deck_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}{SYNTHETIC_CLIENT_TO_GRE_LOWERCASE_PREFIX}\n"
        '{"requestId":13,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientTo'
        'GREMessage",'
        '"payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,'
        '"submitDeckResp":{"deck":"not-a-dict","sideboard":"still-not-a-dict"}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == []
    assert event.payload["sideboard_cards"] == []


@pytest.mark.parametrize(
    "inner_payload",
    [
        {"type": "ClientMessageType_MulliganResp", "mulliganResp": {"decision": "MulliganOption_AcceptHand"}},
        {"type": "ClientMessageType_SelectNResp", "selectNResp": {"selectedOptionIds": [1]}},
        {"type": "ClientMessageType_SubmitDeckResp", "submitDeckResp": {"deckCards": [1]}},
    ],
)
def test_client_actions_specialized_payloads_default_missing_request_context(inner_payload: dict[str, Any]) -> None:
    entry = _entry_from_envelope(_gre_envelope(inner_payload, request_id=_MISSING))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["game_state_id"] == 0
    assert event.payload["resp_id"] == 0
    assert event.payload["request_id"] == 0
    assert event.payload["raw_client_action"]["payload"] == inner_payload


@pytest.mark.parametrize(
    "inner_payload",
    [
        {"type": "ClientMessageType_MulliganResp", "gameStateId": "5", "respId": "6"},
        {"type": "ClientMessageType_SelectNResp", "gameStateId": "5", "respId": "6"},
        {"type": "ClientMessageType_SubmitDeckResp", "gameStateId": "5", "respId": "6"},
    ],
)
def test_client_actions_specialized_payloads_copy_request_context_as_is(inner_payload: dict[str, Any]) -> None:
    entry = _entry_from_envelope(_gre_envelope(inner_payload, request_id="7"))

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["game_state_id"] == "5"
    assert event.payload["resp_id"] == "6"
    assert event.payload["request_id"] == "7"


def test_client_actions_ignore_entries_without_client_message_marker() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        f"{SYNTHETIC_UNITY_LOGGER_MARKER}NotAClientMessage\n{{}}",
    )

    assert client_actions.try_parse(entry, TS) is None
