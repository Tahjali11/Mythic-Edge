import json

import pytest

from mythic_edge_parser.parsers import api_common


def test_find_json_value_returns_first_json_object_from_mixed_text() -> None:
    value = api_common.find_json_value("prefix noise {\"a\": 1, \"b\": [2, 3]} suffix")

    assert value == {"a": 1, "b": [2, 3]}


def test_find_json_value_skips_malformed_candidates_before_valid_json() -> None:
    value = api_common.find_json_value("prefix {bad} middle [oops] suffix {\"ok\": true} trailing")

    assert value == {"ok": True}


def test_find_json_value_returns_first_decodable_array_even_when_object_follows() -> None:
    value = api_common.find_json_value("prefix [1, 2, 3] suffix {\"later\": true}")

    assert value == [1, 2, 3]


def test_find_json_value_all_malformed_or_missing_json_returns_none() -> None:
    assert api_common.find_json_value("no json here") is None
    assert api_common.find_json_value("prefix {bad} middle [oops] suffix") is None


def test_find_json_value_allows_trailing_text_after_decoded_json() -> None:
    value = api_common.find_json_value("prefix {\"a\": 1} trailing text that is not json")

    assert value == {"a": 1}


@pytest.mark.parametrize(
    "text",
    [
        "",
        "plain log text without json candidates",
        "prefix {bad} middle [oops] suffix",
        "dangling object start {",
        "dangling array start [",
    ],
)
def test_find_json_value_property_bounded_malformed_strings_do_not_raise(text: str) -> None:
    assert api_common.find_json_value(text) is None


@pytest.mark.parametrize(
    "json_value",
    [
        {"alpha": 1, "nested": ["x", 2], "flag": True},
        [1, "two", {"three": 3}],
        {"empty": [], "text": "literal braces: {not json}"},
    ],
)
def test_find_json_value_property_valid_json_after_noise_round_trips(json_value: object) -> None:
    encoded = json.dumps(json_value, sort_keys=True)
    body = f"prefix {{bad}} middle [oops] payload {encoded} trailing noise"

    assert api_common.find_json_value(body) == json_value


def test_parse_json_from_body_returns_none_for_non_dict_json() -> None:
    assert api_common.parse_json_from_body("prefix [1, 2, 3] suffix") is None


def test_parse_json_from_body_stops_at_first_decodable_array() -> None:
    assert api_common.parse_json_from_body("prefix [1, 2, 3] suffix {\"later\": true}") is None


def test_parse_json_from_body_context_does_not_change_output() -> None:
    body = "prefix {\"a\": 1} suffix"

    assert api_common.parse_json_from_body(body) == {"a": 1}
    assert api_common.parse_json_from_body(body, "diagnostic context") == {"a": 1}


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("prefix {\"payload\": {\"id\": 1}} trailing", {"payload": {"id": 1}}),
        ("prefix [1, 2, 3] suffix {\"later\": true}", None),
        ("prefix {bad} middle [oops] suffix", None),
    ],
)
def test_parse_json_from_body_property_dict_only_return_values(
    body: str,
    expected: dict[str, object] | None,
) -> None:
    assert api_common.parse_json_from_body(body) == expected
    assert api_common.parse_json_from_body(body, "ignored context") == expected


def test_is_api_request_and_response_match_exact_names() -> None:
    assert api_common.is_api_request("==> GetPlayerInventory", "GetPlayerInventory") is True
    assert api_common.is_api_request("==> GetPlayerInventory", "GetPlayerCards") is False
    assert api_common.is_api_response("<== EventGetCourses", "EventGetCourses") is True
    assert api_common.is_api_response("<== EventGetCourses", "EventGetCourse") is False


def test_api_marker_matching_is_case_sensitive() -> None:
    assert api_common.is_api_request("==> getplayerinventory", "GetPlayerInventory") is False
    assert api_common.is_api_response("<== eventGetCourses", "EventGetCourses") is False


def test_api_marker_matching_allows_whitespace_and_newline_after_marker() -> None:
    assert api_common.is_api_request("prefix ==>\nGetPlayerInventory", "GetPlayerInventory") is True
    assert api_common.is_api_response("prefix <== \nEventGetCourses", "EventGetCourses") is True


def test_api_marker_matching_uses_first_match_only() -> None:
    body = "==> WrongMethod\n==> GetPlayerInventory"

    assert api_common.is_api_request(body, "GetPlayerInventory") is False
    assert api_common.is_api_request(body, "WrongMethod") is True


def test_api_marker_matching_partially_captures_before_punctuation() -> None:
    assert api_common.is_api_request("==> Start-Hook", "Start") is True
    assert api_common.is_api_request("==> Start-Hook", "Start-Hook") is False
    assert api_common.is_api_response("<== Event.GetCourses", "Event") is True
    assert api_common.is_api_response("<== Event.GetCourses", "Event.GetCourses") is False


@pytest.mark.parametrize(
    "api_name",
    [
        "A",
        "GetPlayerInventory",
        "Event_123",
        "ABC123_xyz",
    ],
)
def test_api_marker_property_exact_ascii_names_match(api_name: str) -> None:
    assert api_common.is_api_request(f"noise ==>\n\t{api_name} payload", api_name) is True
    assert api_common.is_api_response(f"noise <== \r\n{api_name} payload", api_name) is True
    assert api_common.is_api_request(f"noise ==>\n\t{api_name}Extra payload", api_name) is False
    assert api_common.is_api_response(f"noise <== \r\n{api_name}Extra payload", api_name) is False

    lower_name = api_name.lower()
    if lower_name != api_name:
        assert api_common.is_api_request(f"==> {lower_name}", api_name) is False
        assert api_common.is_api_response(f"<== {lower_name}", api_name) is False


def test_normalize_int_list_ignores_bools_and_normalizes_digit_strings() -> None:
    assert api_common.normalize_int_list([1, "2", " 3 ", True, False, "x", 4]) == [1, 2, 3, 4]


def test_normalize_int_list_returns_empty_for_non_lists() -> None:
    assert api_common.normalize_int_list(None) == []
    assert api_common.normalize_int_list("1") == []
    assert api_common.normalize_int_list((1, 2)) == []
    assert api_common.normalize_int_list({1, 2}) == []
    assert api_common.normalize_int_list({"id": 1}) == []


def test_normalize_int_list_preserves_order_duplicates_and_new_output_list() -> None:
    source = [3, "3", "003", 3]
    result = api_common.normalize_int_list(source)

    assert result == [3, 3, 3, 3]
    result.append(99)
    assert source == [3, "3", "003", 3]


def test_normalize_int_list_locks_strict_member_filtering() -> None:
    source = [
        0,
        -2,
        "010",
        "-3",
        "+4",
        "4.5",
        4.5,
        "",
        " ",
        None,
        True,
        False,
        {"id": 5},
        [6],
        object(),
    ]

    assert api_common.normalize_int_list(source) == [0, -2, 10]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            [0, -1, 1, "2", " 003 ", "004\n", True, False, "-5", "+6", "7.0", 8.1, {}, [], None, ""],
            [0, -1, 1, 2, 3, 4],
        ),
        (["000", "9", " 10 ", 11, 11], [0, 9, 10, 11, 11]),
        ("123", []),
        ((1, 2), []),
        ({"ids": [1]}, []),
    ],
)
def test_normalize_int_list_property_returns_only_non_bool_ints(value: object, expected: list[int]) -> None:
    result = api_common.normalize_int_list(value)

    assert result == expected
    assert all(isinstance(item, int) and not isinstance(item, bool) for item in result)
