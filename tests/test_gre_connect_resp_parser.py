from mythic_edge_parser.parsers.gre.connect_resp import build_connect_resp_payload


def test_build_connect_resp_payload_happy_path_fields() -> None:
    message = {
        "type": "GREMessageType_ConnectResp",
        "msgId": "msg-1",
        "gameStateId": "state-4",
        "systemSeatIds": [1, "2", "2"],
        "connectResp": {
            "deckMessage": {
                "deckCards": [11, "12", "12"],
                "sideboardCards": [21, "22"],
            },
            "settings": {
                "matchClockSec": 1800,
            },
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload["type"] == "connect_resp"
    assert payload["message_type"] == "GREMessageType_ConnectResp"
    assert payload["msg_id"] == "msg-1"
    assert payload["game_state_id"] == "state-4"
    assert payload["system_seat_ids"] == [1, 2, 2]
    assert payload["deck_cards"] == [11, 12, 12]
    assert payload["sideboard_cards"] == [21, 22]
    assert payload["settings"] == {"matchClockSec": 1800}
    assert payload["raw_connect_resp"] is message


def test_build_connect_resp_payload_shallow_copies_settings() -> None:
    message = {
        "type": "GREMessageType_ConnectResp",
        "msgId": 1,
        "gameStateId": 4,
        "systemSeatIds": [1, 2],
        "connectResp": {
            "deckMessage": {
                "deckCards": [11, 12],
                "sideboardCards": [21],
            },
            "settings": {
                "matchClockSec": 1800,
                "stops": [{"stopType": "StopType_UpkeepStep"}],
            },
        },
    }

    payload = build_connect_resp_payload(message)

    payload["settings"]["matchClockSec"] = 900

    assert message["connectResp"]["settings"]["matchClockSec"] == 1800
    assert payload["deck_cards"] == [11, 12]
    assert payload["sideboard_cards"] == [21]
    assert payload["raw_connect_resp"] is message


def test_build_connect_resp_payload_settings_copy_is_shallow_for_nested_values() -> None:
    message = {
        "connectResp": {
            "settings": {
                "nested": {"stopType": "StopType_UpkeepStep"},
            },
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload["settings"] is not message["connectResp"]["settings"]
    assert payload["settings"]["nested"] is message["connectResp"]["settings"]["nested"]


def test_build_connect_resp_payload_handles_missing_and_malformed_sections() -> None:
    message = {
        "msgId": "2",
        "gameStateId": "5",
        "systemSeatIds": ["1", "2", "x"],
        "connectResp": {
            "deckMessage": "bad",
            "settings": "bad",
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload == {
        "type": "connect_resp",
        "message_type": "GREMessageType_ConnectResp",
        "msg_id": "2",
        "game_state_id": "5",
        "system_seat_ids": [1, 2],
        "deck_cards": [],
        "sideboard_cards": [],
        "settings": {},
        "raw_connect_resp": message,
    }


def test_build_connect_resp_payload_handles_missing_connect_resp_dict() -> None:
    payload = build_connect_resp_payload({"connectResp": "bad"})

    assert payload["settings"] == {}
    assert payload["deck_cards"] == []
    assert payload["sideboard_cards"] == []


def test_build_connect_resp_payload_defaults_missing_scalar_fields_and_lists() -> None:
    message = {
        "connectResp": {
            "deckMessage": {},
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload["message_type"] == "GREMessageType_ConnectResp"
    assert payload["msg_id"] == 0
    assert payload["game_state_id"] == 0
    assert payload["system_seat_ids"] == []
    assert payload["deck_cards"] == []
    assert payload["sideboard_cards"] == []


def test_build_connect_resp_payload_filters_malformed_int_list_members() -> None:
    message = {
        "systemSeatIds": [1, True, "2", " 3 ", "-4", 5.5, {}, [], None, "bad", 0],
        "connectResp": {
            "deckMessage": {
                "deckCards": [11, False, "12", " 13 ", "-14", 15.5, {}, [], None, "bad", 11],
                "sideboardCards": [21, True, "022", "-23", 24.0, {"id": 25}, [26]],
            },
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload["system_seat_ids"] == [1, 2, 3, 0]
    assert payload["deck_cards"] == [11, 12, 13, 11]
    assert payload["sideboard_cards"] == [21, 22]


def test_build_connect_resp_payload_non_list_sources_normalize_to_empty_lists() -> None:
    message = {
        "systemSeatIds": "1",
        "connectResp": {
            "deckMessage": {
                "deckCards": "11",
                "sideboardCards": {"card": 21},
            },
        },
    }

    payload = build_connect_resp_payload(message)

    assert payload["system_seat_ids"] == []
    assert payload["deck_cards"] == []
    assert payload["sideboard_cards"] == []
