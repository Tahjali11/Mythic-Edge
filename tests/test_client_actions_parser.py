from datetime import UTC, datetime

from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import client_actions

TS = datetime(2026, 5, 8, 5, 45, 19, tzinfo=UTC)


def test_client_actions_parse_ui_message_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGreuimessage\n"
        '{"requestId":297,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREUIMessage","payload":{"type":"ClientMessageType_UIMessage","systemSeatId":1,"uiMessage":{"seatIds":[2],"onHover":{"objectId":401}}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "client_ui_message"
    assert event.payload["raw_client_action"]["payload"]["uiMessage"]["onHover"]["objectId"] == 401


def test_client_actions_parse_generic_message_type() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":2,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_ChooseStartingPlayerResp","gameStateId":1,"respId":2}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"


def test_client_actions_parse_mulligan_response() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":6,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_MulliganResp","gameStateId":5,"respId":1,"mulliganResp":{"decision":"MulliganOption_AcceptHand"}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "mulligan_resp"
    assert event.payload["decision"] == "keep"
    assert event.payload["request_id"] == 6


def test_client_actions_parse_select_n_response() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":101,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_SelectNResp","gameStateId":9,"respId":3,"selectNResp":{"selectedOptionIds":[1,2],"selectedObjectIds":["9","10"]}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "select_n_resp"
    assert event.payload["selected_option_ids"] == [1, 2]
    assert event.payload["selected_object_ids"] == [9, 10]


def test_client_actions_parse_submit_deck_with_nested_deck_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":10,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,"submitDeckResp":{"deck":{"deckCards":[11,12,13],"sideboardCards":[21,22]}}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [11, 12, 13]
    assert event.payload["sideboard_cards"] == [21, 22]


def test_client_actions_parse_stringified_inner_payload_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":12,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage",'
        '"payload":"{\\"type\\":\\"ClientMessageType_ChooseStartingPlayerResp\\",\\"gameStateId\\":1,\\"respId\\":2}"}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "generic_client_action"
    assert event.payload["message_type"] == "ClientMessageType_ChooseStartingPlayerResp"


def test_client_actions_submit_deck_tolerates_malformed_nested_deck_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGremessage\n"
        '{"requestId":13,"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage",'
        '"payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,'
        '"submitDeckResp":{"deck":"not-a-dict","sideboard":"still-not-a-dict"}}}',
    )

    event = client_actions.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == []
    assert event.payload["sideboard_cards"] == []


def test_client_actions_ignore_entries_without_client_message_marker() -> None:
    entry = LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]NotAClientMessage\n{}")

    assert client_actions.try_parse(entry, TS) is None
