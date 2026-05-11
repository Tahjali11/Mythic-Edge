from mythic_edge_parser.parsers.gre.connect_resp import build_connect_resp_payload


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
