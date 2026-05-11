from __future__ import annotations

import re
from dataclasses import asdict, dataclass

_SPECIAL_EVENT_KEYWORDS = {
    "midweekmagic": "midweek_magic",
    "festival": "festival",
    "qualifier": "qualifier",
    "arenaopen": "arena_open",
    "playin": "play_in",
    "decathlon": "decathlon",
    "jumpin": "jump_in",
    "cube": "cube_event",
    "momir": "momir_event",
    "omniscience": "omniscience_event",
}
_COMPETITIVE_SPECIAL_EVENT_KEYWORDS = {
    "qualifier",
    "arenaopen",
    "playin",
    "challenge",
}


def _normalized_text(value: object) -> str:
    return str(value or "").strip()


def _collapsed_text(value: object) -> str:
    text = _normalized_text(value).lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def _looks_best_of_three(event_id_key: str, match_win_condition_key: str) -> bool:
    return any(
        marker in event_id_key or marker in match_win_condition_key
        for marker in ("bestof3", "best2of3", "bestofthree", "traditional")
    )


def _play_mode_family(event_id_key: str, super_format_key: str) -> str:
    combined = f"{event_id_key} {super_format_key}"
    if any(keyword in combined for keyword in ("draft", "sealed", "limited")):
        return "limited"
    if any(
        keyword in combined
        for keyword in (
            "constructed",
            "standard",
            "alchemy",
            "historic",
            "explorer",
            "timeless",
            "brawl",
            "play",
            "ladder",
        )
    ):
        return "constructed"
    return "unknown"


def _special_event_subtype(event_id_key: str) -> str:
    for keyword, subtype in _SPECIAL_EVENT_KEYWORDS.items():
        if keyword in event_id_key:
            return subtype
    if "special" in event_id_key:
        return "special_event"
    return ""


def _queue_subtype(
    event_id_key: str,
    match_win_condition_key: str,
    *,
    play_mode_family: str,
) -> str:
    special_subtype = _special_event_subtype(event_id_key)
    if special_subtype:
        return special_subtype
    if "quickdraft" in event_id_key:
        return "quick_draft"
    if "premierdraft" in event_id_key:
        return "premier_draft"
    if "traditionaldraft" in event_id_key:
        return "traditional_draft"
    if "draft" in event_id_key:
        return "draft"
    if "sealed" in event_id_key:
        return "sealed"
    if "ladder" in event_id_key:
        if _looks_best_of_three(event_id_key, match_win_condition_key):
            return "traditional_ranked_ladder"
        return "ranked_ladder"
    if event_id_key == "play":
        if _looks_best_of_three(event_id_key, match_win_condition_key):
            return "traditional_play_queue"
        return "play_queue"
    if "eventconstructedbestofthree" in event_id_key or "constructedbestofthree" in event_id_key:
        return "traditional_play_queue"
    if "eventconstructedbestofone" in event_id_key or "constructedbestofone" in event_id_key:
        return "play_queue"
    if play_mode_family == "constructed":
        return "constructed_queue"
    return "unknown"


def _event_family(event_id_key: str, queue_subtype: str) -> str:
    if queue_subtype in {"quick_draft", "premier_draft", "traditional_draft", "draft"}:
        return "draft"
    if queue_subtype == "sealed":
        return "sealed"
    if queue_subtype in {"ranked_ladder", "traditional_ranked_ladder"}:
        return "ladder"
    if queue_subtype.endswith("_event") or queue_subtype in {
        "midweek_magic",
        "festival",
        "qualifier",
        "arena_open",
        "play_in",
        "decathlon",
        "jump_in",
    }:
        return "special_event"
    if event_id_key == "play" or queue_subtype in {
        "play_queue",
        "traditional_play_queue",
        "constructed_queue",
    }:
        return "queue"
    return "unknown"


def _rank_match_type(event_id_key: str, queue_subtype: str, event_family: str) -> str:
    if queue_subtype in {"ranked_ladder", "traditional_ranked_ladder", "quick_draft", "premier_draft"}:
        return "ranked"
    if queue_subtype in {
        "play_queue",
        "traditional_play_queue",
        "constructed_queue",
        "traditional_draft",
        "sealed",
        "jump_in",
        "midweek_magic",
        "festival",
        "decathlon",
        "cube_event",
        "momir_event",
        "omniscience_event",
    }:
        return "unranked"
    if event_family == "special_event":
        if any(keyword in event_id_key for keyword in _COMPETITIVE_SPECIAL_EVENT_KEYWORDS):
            return "unknown"
        return "unranked"
    return "unknown"


@dataclass(frozen=True, slots=True)
class EventIdentity:
    rank_match_type: str = "unknown"
    play_mode_family: str = "unknown"
    event_family: str = "unknown"
    queue_subtype: str = "unknown"
    rank_eligible: bool = False

    @property
    def is_ranked_match(self) -> bool:
        return self.rank_match_type == "ranked"

    @property
    def is_unranked_match(self) -> bool:
        return self.rank_match_type == "unranked"

    @property
    def is_constructed_match(self) -> bool:
        return self.play_mode_family == "constructed"

    @property
    def is_limited_match(self) -> bool:
        return self.play_mode_family == "limited"

    @property
    def is_draft_match(self) -> bool:
        return self.event_family == "draft"

    @property
    def is_sealed_match(self) -> bool:
        return self.event_family == "sealed"

    @property
    def is_ladder_match(self) -> bool:
        return self.event_family == "ladder"

    @property
    def is_special_event_match(self) -> bool:
        return self.event_family == "special_event"

    @property
    def is_event_match(self) -> bool:
        return self.event_family in {"draft", "sealed", "special_event"}

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload.update(
            {
                "is_ranked_match": self.is_ranked_match,
                "is_unranked_match": self.is_unranked_match,
                "is_constructed_match": self.is_constructed_match,
                "is_limited_match": self.is_limited_match,
                "is_draft_match": self.is_draft_match,
                "is_sealed_match": self.is_sealed_match,
                "is_ladder_match": self.is_ladder_match,
                "is_special_event_match": self.is_special_event_match,
                "is_event_match": self.is_event_match,
            }
        )
        return payload


def classify_event_identity(
    event_id: object,
    super_format: object,
    match_win_condition: object,
) -> EventIdentity:
    event_id_key = _collapsed_text(event_id)
    super_format_key = _collapsed_text(super_format)
    match_win_condition_key = _collapsed_text(match_win_condition)

    play_mode_family = _play_mode_family(event_id_key, super_format_key)
    queue_subtype = _queue_subtype(
        event_id_key,
        match_win_condition_key,
        play_mode_family=play_mode_family,
    )
    event_family = _event_family(event_id_key, queue_subtype)
    rank_match_type = _rank_match_type(event_id_key, queue_subtype, event_family)

    return EventIdentity(
        rank_match_type=rank_match_type,
        play_mode_family=play_mode_family,
        event_family=event_family,
        queue_subtype=queue_subtype,
        rank_eligible=rank_match_type == "ranked",
    )
