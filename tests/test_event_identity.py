from mythic_edge_parser.app.event_identity import classify_event_identity


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
