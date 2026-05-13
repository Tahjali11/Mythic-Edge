import pytest

from mythic_edge_parser.app.event_identity import EventIdentity, classify_event_identity


def _assert_boolean_invariants(identity: EventIdentity) -> None:
    assert identity.is_ranked_match is (identity.rank_match_type == "ranked")
    assert identity.is_unranked_match is (identity.rank_match_type == "unranked")
    assert identity.is_constructed_match is (identity.play_mode_family == "constructed")
    assert identity.is_limited_match is (identity.play_mode_family == "limited")
    assert identity.is_draft_match is (identity.event_family == "draft")
    assert identity.is_sealed_match is (identity.event_family == "sealed")
    assert identity.is_ladder_match is (identity.event_family == "ladder")
    assert identity.is_special_event_match is (identity.event_family == "special_event")
    assert identity.is_event_match is (identity.event_family in {"draft", "sealed", "special_event"})
    assert identity.rank_eligible is identity.is_ranked_match


def test_classify_traditional_ladder_as_ranked_constructed_ladder() -> None:
    identity = classify_event_identity(
        "Traditional_Ladder",
        "SuperFormat_Constructed",
        "MatchWinCondition_Best2of3",
    )

    assert identity.rank_match_type == "ranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "ladder"
    assert identity.queue_subtype == "traditional_ranked_ladder"
    assert identity.rank_eligible is True


def test_classify_play_queue_as_unranked_constructed_queue() -> None:
    identity = classify_event_identity(
        "Play",
        "SuperFormat_Standard",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "queue"
    assert identity.queue_subtype == "play_queue"
    assert identity.is_event_match is False


def test_classify_constructed_event_best_of_one_as_unranked_queue() -> None:
    identity = classify_event_identity(
        "Event_Constructed_BestOfOne",
        "SuperFormat_Constructed",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "queue"
    assert identity.queue_subtype == "play_queue"


def test_classify_constructed_event_best_of_three_as_unranked_traditional_queue() -> None:
    identity = classify_event_identity(
        "Event_Constructed_BestOfThree",
        "SuperFormat_Constructed",
        "MatchWinCondition_Best2of3",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "queue"
    assert identity.queue_subtype == "traditional_play_queue"


def test_classify_quick_draft_as_ranked_limited_draft() -> None:
    identity = classify_event_identity(
        "QuickDraft_BLOOMBURROW",
        "SuperFormat_Limited",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "ranked"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "draft"
    assert identity.queue_subtype == "quick_draft"
    assert identity.is_draft_match is True


def test_classify_traditional_draft_as_unranked_limited_draft() -> None:
    identity = classify_event_identity(
        "TraditionalDraft_FDN",
        "SuperFormat_Limited",
        "MatchWinCondition_Best2of3",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "draft"
    assert identity.queue_subtype == "traditional_draft"


def test_classify_sealed_event_as_unranked_limited_sealed() -> None:
    identity = classify_event_identity(
        "Sealed_MOM",
        "SuperFormat_Limited",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "sealed"
    assert identity.queue_subtype == "sealed"
    assert identity.is_sealed_match is True


def test_classify_midweek_magic_as_special_event() -> None:
    identity = classify_event_identity(
        "MidweekMagic_AllAccess",
        "SuperFormat_Constructed",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "special_event"
    assert identity.queue_subtype == "midweek_magic"
    assert identity.is_special_event_match is True


def test_classify_premier_draft_as_ranked_limited_draft() -> None:
    identity = classify_event_identity(
        "PremierDraft_TDM",
        "SuperFormat_Limited",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "ranked"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "draft"
    assert identity.queue_subtype == "premier_draft"
    assert identity.rank_eligible is True


def test_classify_generic_draft_as_unknown_rankedness_limited_draft() -> None:
    identity = classify_event_identity(
        "Draft_BLOOMBURROW",
        "SuperFormat_Limited",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unknown"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "draft"
    assert identity.queue_subtype == "draft"
    assert identity.rank_eligible is False


def test_classify_best_of_one_ladder_as_ranked_ladder() -> None:
    identity = classify_event_identity(
        "Ladder",
        "SuperFormat_Standard",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "ranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "ladder"
    assert identity.queue_subtype == "ranked_ladder"


def test_classify_constructed_fallback_as_constructed_queue() -> None:
    identity = classify_event_identity(
        "Standard_ShakeUp",
        "SuperFormat_Constructed",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unranked"
    assert identity.play_mode_family == "constructed"
    assert identity.event_family == "queue"
    assert identity.queue_subtype == "constructed_queue"


@pytest.mark.parametrize(
    ("event_id", "expected_subtype", "expected_rank_match_type"),
    (
        ("MidweekMagic_AllAccess", "midweek_magic", "unranked"),
        ("Festival_MWM", "festival", "unranked"),
        ("QualifierWeekend_Day1", "qualifier", "unknown"),
        ("ArenaOpen_Day2", "arena_open", "unknown"),
        ("PlayIn_BestOfOne", "play_in", "unknown"),
        ("Decathlon_Finals", "decathlon", "unranked"),
        ("JumpIn_Packets", "jump_in", "unranked"),
        ("Cube_Event", "cube_event", "unranked"),
        ("Momir_Event", "momir_event", "unranked"),
        ("Omniscience_Event", "omniscience_event", "unranked"),
        ("Special_Challenge", "special_event", "unknown"),
    ),
)
def test_classify_special_event_keyword_subtypes(
    event_id: str,
    expected_subtype: str,
    expected_rank_match_type: str,
) -> None:
    identity = classify_event_identity(
        event_id,
        "SuperFormat_Constructed",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == expected_rank_match_type
    assert identity.event_family == "special_event"
    assert identity.queue_subtype == expected_subtype
    assert identity.rank_eligible is (expected_rank_match_type == "ranked")


@pytest.mark.parametrize(
    "event_id",
    (
        "QualifierWeekend_Day1",
        "ArenaOpen_Day2",
        "PlayIn_BestOfOne",
        "Special_Challenge",
    ),
)
def test_competitive_special_events_keep_unknown_rankedness(event_id: str) -> None:
    identity = classify_event_identity(
        event_id,
        "SuperFormat_Constructed",
        "MatchWinCondition_BestOfOne",
    )

    assert identity.rank_match_type == "unknown"
    assert identity.event_family == "special_event"
    assert identity.rank_eligible is False


@pytest.mark.parametrize(
    ("event_id", "super_format", "match_win_condition"),
    (
        (None, None, None),
        ("", "", ""),
        (0, 0, 0),
        (False, False, False),
        (12345, 67890, 111),
        ("Totally_New_Format", "Unknown_Format", "Unknown_Condition"),
    ),
)
def test_missing_numeric_and_novel_descriptors_return_unknowns(
    event_id: object,
    super_format: object,
    match_win_condition: object,
) -> None:
    identity = classify_event_identity(event_id, super_format, match_win_condition)

    assert identity.rank_match_type == "unknown"
    assert identity.play_mode_family == "unknown"
    assert identity.event_family == "unknown"
    assert identity.queue_subtype == "unknown"
    assert identity.rank_eligible is False


def test_normalization_ignores_case_punctuation_and_separators() -> None:
    identity = classify_event_identity(
        " quick-draft: BLOOMBURROW! ",
        " super format limited ",
        " match win condition best of one ",
    )

    assert identity.rank_match_type == "ranked"
    assert identity.play_mode_family == "limited"
    assert identity.event_family == "draft"
    assert identity.queue_subtype == "quick_draft"


def test_event_identity_boolean_invariants() -> None:
    identities = [
        classify_event_identity("Traditional_Ladder", "SuperFormat_Constructed", "MatchWinCondition_Best2of3"),
        classify_event_identity("Play", "SuperFormat_Standard", "MatchWinCondition_BestOfOne"),
        classify_event_identity("QuickDraft_BLOOMBURROW", "SuperFormat_Limited", "MatchWinCondition_BestOfOne"),
        classify_event_identity("Sealed_MOM", "SuperFormat_Limited", "MatchWinCondition_BestOfOne"),
        classify_event_identity("MidweekMagic_AllAccess", "SuperFormat_Constructed", "MatchWinCondition_BestOfOne"),
        classify_event_identity(None, None, None),
    ]

    for identity in identities:
        _assert_boolean_invariants(identity)


def test_event_identity_to_dict_contains_stable_key_shape() -> None:
    payload = classify_event_identity(
        "Traditional_Ladder",
        "SuperFormat_Constructed",
        "MatchWinCondition_Best2of3",
    ).to_dict()

    assert set(payload) == {
        "rank_match_type",
        "play_mode_family",
        "event_family",
        "queue_subtype",
        "rank_eligible",
        "is_ranked_match",
        "is_unranked_match",
        "is_constructed_match",
        "is_limited_match",
        "is_draft_match",
        "is_sealed_match",
        "is_ladder_match",
        "is_special_event_match",
        "is_event_match",
    }
