from mythic_edge_parser.parsers import api_common


def test_find_json_value_returns_first_json_object_from_mixed_text() -> None:
    value = api_common.find_json_value("prefix noise {\"a\": 1, \"b\": [2, 3]} suffix")

    assert value == {"a": 1, "b": [2, 3]}


def test_parse_json_from_body_returns_none_for_non_dict_json() -> None:
    assert api_common.parse_json_from_body("prefix [1, 2, 3] suffix") is None


def test_is_api_request_and_response_match_exact_names() -> None:
    assert api_common.is_api_request("==> GetPlayerInventory", "GetPlayerInventory") is True
    assert api_common.is_api_request("==> GetPlayerInventory", "GetPlayerCards") is False
    assert api_common.is_api_response("<== EventGetCourses", "EventGetCourses") is True
    assert api_common.is_api_response("<== EventGetCourses", "EventGetCourse") is False


def test_normalize_int_list_ignores_bools_and_normalizes_digit_strings() -> None:
    assert api_common.normalize_int_list([1, "2", " 3 ", True, False, "x", 4]) == [1, 2, 3, 4]
