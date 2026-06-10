from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PostingState:
    """Downstream posting and delivery bookkeeping, not parser truth."""

    posted_submit_deck_keys: set[tuple[Any, Any]] = field(default_factory=set)
    posted_sideboard_keys: set[tuple[Any, Any]] = field(default_factory=set)
    game_rows_posted: set[tuple[Any, Any]] = field(default_factory=set)
    match_rows_posted: set[Any] = field(default_factory=set)
    posted_match_summaries: set[str] = field(default_factory=set)
    posted_match_log_rows: set[str] = field(default_factory=set)
    last_posted_match_log_rows: dict[str, dict[str, Any]] = field(default_factory=dict)
    last_posted_game_log_rows: dict[tuple[str, int], dict[str, Any]] = field(default_factory=dict)

    def reset(self) -> None:
        self.posted_submit_deck_keys.clear()
        self.posted_sideboard_keys.clear()
        self.game_rows_posted.clear()
        self.match_rows_posted.clear()
        self.posted_match_summaries.clear()
        self.posted_match_log_rows.clear()
        self.last_posted_match_log_rows.clear()
        self.last_posted_game_log_rows.clear()

    def mark_match_log_posted(self, match_id: str, row: dict[str, Any]) -> None:
        self.last_posted_match_log_rows[match_id] = dict(row)

    def mark_game_log_posted(self, key: tuple[str, int], row: dict[str, Any]) -> None:
        self.last_posted_game_log_rows[key] = dict(row)
