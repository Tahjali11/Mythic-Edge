from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .event_identity import EventIdentity, classify_event_identity

GAME_NUMBERS = (1, 2, 3)
MYTHIC_RANK_LABEL = "Mythic"
MTGA_QUEUE_TYPE_MAP = {
    "MatchWinCondition_Best2of3": "Best of 3",
    "MatchWinCondition_BestOfThree": "Best of 3",
    "MatchWinCondition_BestOf3": "Best of 3",
    "MatchWinCondition_SingleGame": "Best of 1",
    "MatchWinCondition_BestOfOne": "Best of 1",
    "MatchWinCondition_SingleElimination": "Single Elimination",
}


def _placeholder_count(cards: list[str]) -> int:
    return sum(1 for card in cards if card.startswith("["))


def _contains_placeholders(cards: list[str]) -> bool:
    return any(card.startswith("[") for card in cards if card)


def _serialize_exact_card_list(cards: list[str]) -> str:
    if not cards or _contains_placeholders(cards):
        return ""
    return "; ".join(cards)


def _duration_seconds(started_at: str, finished_at: str) -> int | str:
    if not started_at or not finished_at:
        return ""
    try:
        started = datetime.fromisoformat(started_at)
        finished = datetime.fromisoformat(finished_at)
    except ValueError:
        return ""
    return max(int((finished - started).total_seconds()), 0)


def _played_date(timestamp: str) -> str:
    if not timestamp:
        return ""
    try:
        return datetime.fromisoformat(timestamp).date().isoformat()
    except ValueError:
        return timestamp[:10]


def _play_draw_label(starting_player: Any, player_team: Any) -> str:
    if starting_player in (None, "") or player_team in (None, ""):
        return ""
    return "Play" if starting_player == player_team else "Draw"


def _result_for_player(winner_team: Any, player_team: Any) -> str:
    if winner_team in (None, "") or player_team in (None, ""):
        return ""
    return "W" if winner_team == player_team else "L"


def _better_opening_hand_snapshot(current_cards: list[str], new_cards: list[str]) -> bool:
    if not new_cards:
        return False
    if not current_cards:
        return True
    if len(new_cards) > len(current_cards):
        return True
    return len(new_cards) == len(current_cards) and _placeholder_count(new_cards) < _placeholder_count(current_cards)


@dataclass(slots=True)
class GameSummary:
    game_number: int
    winner_team: Any = ""
    starting_player: Any = ""
    mulligans: int = 0
    opening_hand: list[str] = field(default_factory=list)
    mulliganed_away: list[str] = field(default_factory=list)
    first_event_time: str = ""
    last_event_time: str = ""
    turn_count: int = 0

    def touch(self, timestamp: str) -> None:
        if not timestamp:
            return
        if not self.first_event_time:
            self.first_event_time = timestamp
        self.last_event_time = timestamp

    def set_turn_count(self, turn_number: Any) -> None:
        try:
            normalized = int(turn_number)
        except (TypeError, ValueError):
            return
        if normalized > self.turn_count:
            self.turn_count = normalized

    def duration_seconds(self) -> int | str:
        return _duration_seconds(self.first_event_time, self.last_event_time)

    def opening_hand_size(self) -> int | str:
        if self.opening_hand:
            return len(self.opening_hand)
        if self.first_event_time:
            return max(7 - int(self.mulligans), 0)
        return ""

    def play_draw(self, player_team: Any) -> str:
        return _play_draw_label(self.starting_player, player_team)

    def result_for_player(self, player_team: Any) -> str:
        return _result_for_player(self.winner_team, player_team)

    def set_opening_hand(self, cards: list[str]) -> None:
        if _better_opening_hand_snapshot(self.opening_hand, cards):
            self.opening_hand = list(cards)

    def add_mulliganed_away(self, cards: list[str]) -> None:
        if not cards:
            return
        self.mulliganed_away.extend(card for card in cards if card)

    def has_summary_data(self) -> bool:
        return any(
            [
                self.winner_team not in (None, ""),
                self.starting_player not in (None, ""),
                self.mulligans > 0,
                bool(self.opening_hand),
                bool(self.mulliganed_away),
                bool(self.first_event_time),
                self.turn_count > 0,
            ]
        )

    def to_debug_dict(self, player_team: Any) -> dict[str, Any]:
        return {
            "game_number": self.game_number,
            "first_event_time": self.first_event_time,
            "last_event_time": self.last_event_time,
            "winner_team": self.winner_team,
            "starting_player": self.starting_player,
            "play_draw": self.play_draw(player_team),
            "result": self.result_for_player(player_team),
            "mulligans": self.mulligans,
            "turn_count": self.turn_count,
            "duration_seconds": self.duration_seconds(),
            "opening_hand": list(self.opening_hand),
            "mulliganed_away": list(self.mulliganed_away),
        }

    def to_sheet_row(self, match: MatchSummary) -> dict[str, Any]:
        payload = self.to_debug_dict(match.player_team)
        return {
            "timestamp": match.last_event_time or match.first_event_time,
            "event_family": "GameSummary",
            "event_type": "game_summary",
            "scope": "Game",
            "match_id": match.match_id,
            "game_number": self.game_number,
            "player_team": match.player_team,
            "winner_team": self.winner_team,
            "mulligan_count": self.mulligans,
            "starting_player": self.starting_player,
            "play_draw": self.play_draw(match.player_team),
            "constructed_rank": match.constructed_rank,
            "raw_json": json.dumps(payload, ensure_ascii=False),
        }

    def to_game_log_row(self, match: MatchSummary) -> dict[str, Any]:
        return {
            "event_family": "GameLogRow",
            "event_type": "game_log_row",
            "scope": "Game",
            "match_id": match.match_id,
            "timestamp": self.last_event_time or match.last_event_time or match.first_event_time,
            "Date": match.played_date(),
            "MTGA Format": match.mtga_format(),
            "My Rank": match.rank_bucket(),
            "MTGA Match ID": match.match_id,
            "Game Number": self.game_number,
            "Pre / Postboard": "Preboard" if self.game_number == 1 else "Postboard",
            "Play / Draw": match.game_play_draw(self.game_number),
            "Mulligans": self.mulligans if self.first_event_time else "",
            "Opening Hand Size": self.opening_hand_size(),
            "Opening Hand": _serialize_exact_card_list(self.opening_hand),
            "Mulliganed Away": _serialize_exact_card_list(self.mulliganed_away),
            "Game Result": self.result_for_player(match.player_team),
            "Turn Count": self.turn_count if self.turn_count else "",
            "Game Duration": self.duration_seconds(),
            "MTGA Event ID": match.event_id,
            "MTGA Queue Type": match.mtga_queue_type(),
        }


def _default_games() -> dict[int, GameSummary]:
    return {game_number: GameSummary(game_number) for game_number in GAME_NUMBERS}


@dataclass(slots=True)
class MatchSummary:
    match_id: str
    first_event_time: str = ""
    last_event_time: str = ""
    player_team: Any = ""
    match_winner_team: Any = ""
    match_result_type: str = ""
    match_result_reason: str = ""
    sideboarding_entered: bool = False
    submit_deck_seen: bool = False
    constructed_rank: str = ""
    constructed_class: str = ""
    constructed_level: str = ""
    constructed_percentile: Any = None
    constructed_rank_source: str = ""
    event_id: str = ""
    super_format: str = ""
    match_win_condition: str = ""
    games: dict[int, GameSummary] = field(default_factory=_default_games)

    def touch(self, timestamp: str) -> None:
        if not self.first_event_time:
            self.first_event_time = timestamp
        self.last_event_time = timestamp

    def game(self, game_number: Any) -> GameSummary | None:
        if game_number in (None, ""):
            return None
        try:
            normalized = int(game_number)
        except (TypeError, ValueError):
            return None
        return self.games.get(normalized)

    def _game_slots(self) -> list[tuple[int, GameSummary]]:
        return [(game_number, self.games[game_number]) for game_number in GAME_NUMBERS]

    def _game_debug_payloads(self) -> list[dict[str, Any]]:
        return [game.to_debug_dict(self.player_team) for _, game in self._game_slots()]

    def _game_winner_fields(self) -> dict[str, Any]:
        return {f"g{game_number}_winner_team": game.winner_team for game_number, game in self._game_slots()}

    def _game_play_draw_fields(self) -> dict[str, str]:
        return {f"g{game_number}_play_draw": self.game_play_draw(game_number) for game_number, _ in self._game_slots()}

    def _game_result_fields(self) -> dict[str, str]:
        return {
            f"g{game_number}_result": game.result_for_player(self.player_team)
            for game_number, game in self._game_slots()
        }

    def _game_mulligan_fields(self) -> dict[str, int]:
        return {f"g{game_number}_mulligans": game.mulligans for game_number, game in self._game_slots()}

    def set_game_winner(self, game_number: Any, winner_team: Any) -> None:
        game = self.game(game_number)
        if game is not None and winner_team not in (None, ""):
            game.winner_team = winner_team

    def set_game_starting_player(self, game_number: Any, starting_player: Any) -> None:
        game = self.game(game_number)
        if game is not None and starting_player not in (None, ""):
            game.starting_player = starting_player

    def set_game_mulligans(self, game_number: Any, mulligans: int) -> None:
        game = self.game(game_number)
        if game is not None:
            game.mulligans = mulligans

    def set_game_opening_hand(self, game_number: Any, opening_hand: list[str]) -> None:
        game = self.game(game_number)
        if game is None or not opening_hand:
            return
        game.set_opening_hand(opening_hand)

    def add_game_mulliganed_away(self, game_number: Any, cards: list[str]) -> None:
        game = self.game(game_number)
        if game is None:
            return
        game.add_mulliganed_away(cards)

    def touch_game(self, game_number: Any, timestamp: str) -> None:
        game = self.game(game_number)
        if game is not None:
            game.touch(timestamp)

    def set_game_turn_count(self, game_number: Any, turn_number: Any) -> None:
        game = self.game(game_number)
        if game is not None:
            game.set_turn_count(turn_number)

    def ingest_game_info(self, game_info: dict[str, Any]) -> None:
        if not isinstance(game_info, dict):
            return
        super_format = str(game_info.get("superFormat", "")).strip()
        match_win_condition = str(game_info.get("matchWinCondition", "")).strip()
        if super_format:
            self.super_format = super_format
        if match_win_condition:
            self.match_win_condition = match_win_condition

    def opponent_team(self) -> Any:
        if self.player_team == 1:
            return 2
        if self.player_team == 2:
            return 1
        return ""

    def effective_starting_player(self, game_number: int) -> Any:
        game = self.games.get(game_number)
        if game is None:
            return ""
        if game.starting_player not in (None, ""):
            return game.starting_player
        if not game.has_summary_data():
            return ""
        if game_number <= 1 or self.player_team in (None, ""):
            return ""

        previous_game = self.games.get(game_number - 1)
        if previous_game is None or previous_game.winner_team in (None, ""):
            return ""
        if previous_game.winner_team == self.player_team:
            return self.opponent_team()
        return self.player_team

    def game_play_draw(self, game_number: int) -> str:
        return _play_draw_label(self.effective_starting_player(game_number), self.player_team)

    @property
    def game_wins(self) -> int:
        if self.player_team in (None, ""):
            return 0
        return sum(1 for game in self.games.values() if game.winner_team == self.player_team)

    @property
    def game_losses(self) -> int:
        completed_games = sum(1 for game in self.games.values() if game.winner_team not in (None, ""))
        return completed_games - self.game_wins

    @property
    def match_wl(self) -> str:
        return _result_for_player(self.match_winner_team, self.player_team)

    @property
    def total_mulligans(self) -> int:
        return sum(game.mulligans for game in self.games.values())

    @property
    def total_games(self) -> int:
        return self.game_wins + self.game_losses

    @property
    def match_win_flag(self) -> int | str:
        if not self.match_wl:
            return ""
        return 1 if self.match_wl == "W" else 0

    @property
    def game_win_rate(self) -> float | str:
        if self.total_games == 0:
            return ""
        return self.game_wins / self.total_games

    def is_ready(self) -> bool:
        return bool(self.match_id and self.player_team not in (None, "") and self.match_winner_team not in (None, ""))

    def rank_bucket(self) -> str:
        rank_class = str(self.constructed_class or "").strip()
        if not rank_class:
            return ""
        if rank_class == MYTHIC_RANK_LABEL:
            if self.constructed_percentile not in (None, ""):
                return "Mythic %"
            if str(self.constructed_level or "").strip():
                return "Mythic #"
            return MYTHIC_RANK_LABEL
        return rank_class

    def mtga_format(self) -> str:
        text = str(self.super_format or "").strip()
        if text.startswith("SuperFormat_"):
            return text.removeprefix("SuperFormat_")
        if text:
            return text
        if "Constructed" in self.event_id:
            return "Constructed"
        if "Limited" in self.event_id:
            return "Limited"
        return ""

    def mtga_queue_type(self) -> str:
        text = str(self.match_win_condition or "").strip()
        if text in MTGA_QUEUE_TYPE_MAP:
            return MTGA_QUEUE_TYPE_MAP[text]
        if "BestOf3" in self.event_id or "BestOf3" in text or "Best2of3" in text:
            return "Best of 3"
        if "BestOf1" in self.event_id or "SingleGame" in text:
            return "Best of 1"
        if self.sideboarding_entered or self.total_games > 1:
            return "Best of 3"
        return text

    def event_identity(self) -> EventIdentity:
        return classify_event_identity(
            self.event_id,
            self.super_format,
            self.match_win_condition,
        )

    def played_date(self) -> str:
        return _played_date(self.first_event_time)

    def set_constructed_rank(
        self,
        rank_text: str,
        rank_class: Any,
        rank_level: Any,
        rank_percentile: Any,
        *,
        source: str,
    ) -> None:
        self.constructed_rank = str(rank_text or "").strip()
        self.constructed_class = rank_class
        self.constructed_level = rank_level
        self.constructed_percentile = rank_percentile
        self.constructed_rank_source = str(source or "").strip()

    def to_debug_dict(self) -> dict[str, Any]:
        event_identity = self.event_identity()
        return {
            "match_id": self.match_id,
            "first_event_time": self.first_event_time,
            "last_event_time": self.last_event_time,
            "player_team": self.player_team,
            "match_winner_team": self.match_winner_team,
            "match_result_type": self.match_result_type,
            "match_result_reason": self.match_result_reason,
            "my_rank": self.rank_bucket(),
            "constructed_class": self.constructed_class,
            "constructed_level": self.constructed_level,
            "constructed_percentile": self.constructed_percentile,
            "constructed_rank_source": self.constructed_rank_source,
            "event_id": self.event_id,
            "super_format": self.super_format,
            "match_win_condition": self.match_win_condition,
            "mtga_format": self.mtga_format(),
            "mtga_queue_type": self.mtga_queue_type(),
            "event_identity": event_identity.to_dict(),
            **self._game_winner_fields(),
            "g1_starting_player": self.effective_starting_player(1),
            "g2_starting_player": self.effective_starting_player(2),
            "g3_starting_player": self.effective_starting_player(3),
            **self._game_play_draw_fields(),
            **self._game_result_fields(),
            **self._game_mulligan_fields(),
            "game_wins": self.game_wins,
            "game_losses": self.game_losses,
            "match_wl": self.match_wl,
            "total_games": self.total_games,
            "match_win_flag": self.match_win_flag,
            "game_win_rate": self.game_win_rate,
            "sideboarding_entered": self.sideboarding_entered,
            "submit_deck_seen": self.submit_deck_seen,
            "constructed_rank": self.constructed_rank,
            "games": self._game_debug_payloads(),
        }

    def to_sheet_row(self) -> dict[str, Any]:
        debug_dict = self.to_debug_dict()
        return {
            "timestamp": self.last_event_time,
            "event_family": "MatchSummary",
            "event_type": "match_summary",
            "scope": "Match",
            "match_id": self.match_id,
            "player_team": self.player_team,
            "winner_team": self.match_winner_team,
            "result_type": self.match_result_type,
            "result_reason": self.match_result_reason,
            "first_event_time": self.first_event_time,
            "last_event_time": self.last_event_time,
            "match_wl": self.match_wl,
            **self._game_winner_fields(),
            **self._game_play_draw_fields(),
            **self._game_mulligan_fields(),
            "total_mulligans": self.total_mulligans,
            "game_wins": self.game_wins,
            "game_losses": self.game_losses,
            "sideboarding_entered": self.sideboarding_entered,
            "submit_deck_seen": self.submit_deck_seen,
            "constructed_rank": self.constructed_rank,
            "my_rank": self.rank_bucket(),
            **self._game_result_fields(),
            "raw_json": json.dumps(debug_dict, ensure_ascii=False),
        }

    def to_history_item(self) -> dict[str, Any]:
        event_identity = self.event_identity()
        return {
            "match_id": self.match_id,
            "date": self.played_date(),
            "started_at": self.first_event_time,
            "finished_at": self.last_event_time,
            "result": self.match_wl,
            "games_won": self.game_wins,
            "games_lost": self.game_losses,
            "total_games": self.total_games,
            "total_mulligans": self.total_mulligans,
            "rank": self.rank_bucket(),
            "constructed_rank_raw": self.constructed_rank,
            "constructed_rank_source": self.constructed_rank_source,
            "super_format": self.super_format,
            "match_win_condition": self.match_win_condition,
            "mtga_format": self.mtga_format(),
            "mtga_queue_type": self.mtga_queue_type(),
            "event_id": self.event_id,
            "rank_match_type": event_identity.rank_match_type,
            "play_mode_family": event_identity.play_mode_family,
            "event_family": event_identity.event_family,
            "queue_subtype": event_identity.queue_subtype,
            "rank_eligible": event_identity.rank_eligible,
            "is_ranked_match": event_identity.is_ranked_match,
            "is_unranked_match": event_identity.is_unranked_match,
            "is_constructed_match": event_identity.is_constructed_match,
            "is_limited_match": event_identity.is_limited_match,
            "is_draft_match": event_identity.is_draft_match,
            "is_sealed_match": event_identity.is_sealed_match,
            "is_ladder_match": event_identity.is_ladder_match,
            "is_special_event_match": event_identity.is_special_event_match,
            "is_event_match": event_identity.is_event_match,
            "match_win_flag": self.match_win_flag,
            "game_win_rate": self.game_win_rate,
            "sideboarding_entered": self.sideboarding_entered,
            "submit_deck_seen": self.submit_deck_seen,
            "games": self._game_debug_payloads(),
        }

    def to_match_log_row(self, *, final: bool = True) -> dict[str, Any]:
        sync_status = "Final" if final else "Live"
        sideboard_value = "Yes" if self.sideboarding_entered else ("No" if final else "")
        submit_deck_value = "Yes" if self.submit_deck_seen else ("No" if final else "")
        mulligan_value = self.total_mulligans if (final or self.total_mulligans) else ""
        g1 = self.games[1]
        g2 = self.games[2]
        g3 = self.games[3]
        return {
            "event_family": "MatchLogRow",
            "event_type": "match_log_row",
            "scope": "Match",
            "match_id": self.match_id,
            "timestamp": self.last_event_time or self.first_event_time,
            "Date": self.played_date(),
            "Experiment ID": "",
            "Deck Code": "",
            "Opponent Archetype": "",
            "Opponent Variant": "",
            "My Rank": self.rank_bucket(),
            "Opponent Rank": "",
            "Deck Tier": "",
            "G1 Play / Draw": self.game_play_draw(1),
            "Game 1 Result": g1.result_for_player(self.player_team),
            "G2 Play / Draw": self.game_play_draw(2),
            "Game 2 Result": g2.result_for_player(self.player_team),
            "G3 Play / Draw": self.game_play_draw(3),
            "Game 3 Result": g3.result_for_player(self.player_team),
            "Games Won": self.game_wins if self.total_games else "",
            "Games Lost": self.game_losses if self.total_games else "",
            "Match Win?": self.match_wl,
            "Valid?": "",
            "General Analysis?": "",
            "Primary Comparison Analysis?": "",
            "Reason Tag": "",
            "Pilot Error?": "",
            "One-line note": "",
            "Rank Group": "",
            "Mythic Split": "",
            "Total Games": self.total_games if self.total_games else "",
            "Match Win Flag": self.match_win_flag,
            "Game Win %": self.game_win_rate,
            "Queue Bucket (Auto)": "",
            "Primary Comparison (Auto)": "",
            "Event Round": "",
            "MTGA Match ID": self.match_id,
            "MTGA Format": self.mtga_format(),
            "MTGA Event ID": self.event_id,
            "MTGA Queue Type": self.mtga_queue_type(),
            "G1 Mulligans": g1.mulligans if g1.has_summary_data() else "",
            "G2 Mulligans": g2.mulligans if g2.has_summary_data() else "",
            "G3 Mulligans": g3.mulligans if g3.has_summary_data() else "",
            "G1 Turn Count": g1.turn_count if g1.turn_count else "",
            "G2 Turn Count": g2.turn_count if g2.turn_count else "",
            "G3 Turn Count": g3.turn_count if g3.turn_count else "",
            "MGTA Start Time": self.first_event_time,
            "MTGA End Time": self.last_event_time if final else "",
            "MTGA Rank Raw": self.constructed_rank,
            "MTGA Mulligans": mulligan_value,
            "MTGA Sideboard Entered": sideboard_value,
            "MTGA Submit Deck Seen": submit_deck_value,
            "MTGA Sync Status": sync_status,
        }

    def to_game_sheet_rows(self) -> list[dict[str, Any]]:
        return [
            game.to_game_log_row(self)
            for _, game in self._game_slots()
            if game.has_summary_data()
        ]
