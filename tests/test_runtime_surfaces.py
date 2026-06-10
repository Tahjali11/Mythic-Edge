import json
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app import diagnostics, runtime_surfaces, state
from mythic_edge_parser.app.models import MatchSummary
from mythic_edge_parser.events import (
    ClientActionEvent,
    CollectionEvent,
    DeckCollectionEvent,
    EventMetadata,
    GameStateEvent,
    MatchStateEvent,
    RankEvent,
)


def _reset_runtime_surface_state() -> None:
    runtime_surfaces.reset_runtime_surface_state()
    state.reset_runtime_state()


def _patch_surface_paths(tmp_path: Path, monkeypatch) -> Path:
    status_root = tmp_path / "status"
    monkeypatch.setattr(
        runtime_surfaces, "ACTIVE_MATCH_SNAPSHOT_PATH", status_root / "active_match_snapshot_latest.json"
    )
    monkeypatch.setattr(
        runtime_surfaces, "ACTIVE_MATCH_TIMELINE_PATH", status_root / "active_match_timeline_latest.json"
    )
    monkeypatch.setattr(runtime_surfaces, "STATUS_TIMELINES_ROOT", status_root / "timelines")
    monkeypatch.setattr(runtime_surfaces, "ACTIVE_DECK_PROFILE_PATH", status_root / "active_deck_profile_latest.json")
    monkeypatch.setattr(runtime_surfaces, "MATCH_HISTORY_PATH", status_root / "match_history_latest.json")
    monkeypatch.setattr(runtime_surfaces, "COLLECTION_PROFILE_PATH", status_root / "collection_profile_latest.json")
    monkeypatch.setattr(
        runtime_surfaces, "ACTIVE_SUBMITTED_DECK_PATH", status_root / "active_submitted_deck_latest.json"
    )
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", status_root)
    monkeypatch.setattr(diagnostics, "ACTIVE_SUBMITTED_DECK_PATH", status_root / "active_submitted_deck_latest.json")
    monkeypatch.setattr(diagnostics, "_STATUS_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_STATE", {})
    return status_root


def test_match_timeline_filename_uses_safe_stem_without_changing_payload_match_id(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    raw_match_id = r"..\outside/match:evil"
    runtime_surfaces._MATCH_TIMELINES[raw_match_id] = [{"kind": "synthetic"}]

    runtime_surfaces._write_timeline_payload(raw_match_id)

    timeline_root = status_root / "timelines"
    timeline_files = list(timeline_root.glob("*.json"))
    assert len(timeline_files) == 1
    assert timeline_files[0].parent == timeline_root
    assert ".." not in timeline_files[0].name
    assert ":" not in timeline_files[0].name
    assert "/" not in timeline_files[0].name
    assert "\\" not in timeline_files[0].name
    assert not (tmp_path / "outside").exists()

    payload = json.loads(timeline_files[0].read_text(encoding="utf-8"))
    assert payload["match_id"] == raw_match_id
    assert runtime_surfaces.load_active_timeline_payload(raw_match_id)["match_id"] == raw_match_id


def test_observe_event_builds_deck_profile_collection_report_and_timeline(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    runtime_surfaces._CARD_LOOKUP_CACHE = {
        "1001": {
            "name": "Card A",
            "rarity": "rare",
            "set": "set1",
            "set_name": "Set One",
            "mana_cost": "{1}{G}",
            "cmc": 2,
            "type_line": "Creature",
            "colors": ["G"],
        },
        "2002": {
            "name": "Card B",
            "rarity": "common",
            "set": "set1",
            "set_name": "Set One",
            "mana_cost": "",
            "cmc": 0,
            "type_line": "Land",
            "colors": [],
        },
        "3003": {
            "name": "Card C",
            "rarity": "mythic",
            "set": "set2",
            "set_name": "Set Two",
            "mana_cost": "{B}",
            "cmc": 1,
            "type_line": "Instant",
            "colors": ["B"],
        },
    }

    state._CONTEXT.update(
        {
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )

    deck_collection_event = DeckCollectionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 0, tzinfo=UTC), b"raw"),
        {
            "type": "deck_collection_snapshot",
            "decks": {
                "deck-1": {
                    "DeckId": "deck-1",
                    "Name": "Test Deck",
                    "Attributes": [
                        {"name": "Format", "value": "TraditionalStandard"},
                    ],
                    "list": {
                        "MainDeck": [
                            {"cardId": 1001, "quantity": 2},
                            {"cardId": 2002, "quantity": 1},
                        ],
                        "Sideboard": [
                            {"cardId": 3003, "quantity": 1},
                        ],
                    },
                }
            },
        },
    )
    collection_event = CollectionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 1, tzinfo=UTC), b"raw"),
        {
            "type": "collection_snapshot",
            "player_cards": {
                "1001": 1,
                "2002": 4,
            },
        },
    )
    submit_event = ClientActionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 2, tzinfo=UTC), b"raw"),
        {
            "type": "submit_deck_resp",
            "deck_cards": [1001, 1001, 2002],
            "sideboard_cards": [3003],
            "game_state_id": 77,
            "resp_id": 88,
            "request_id": 99,
        },
    )

    runtime_surfaces.observe_event(deck_collection_event, include_in_timeline=False)
    runtime_surfaces.observe_event(collection_event, include_in_timeline=False)
    runtime_surfaces.observe_event(submit_event, include_in_timeline=True)

    deck_profile = json.loads((status_root / "active_deck_profile_latest.json").read_text(encoding="utf-8"))
    assert deck_profile["matched_decks"][0]["name"] == "Test Deck"
    assert deck_profile["stats"]["mainboard_count"] == 3
    assert deck_profile["collection_status"]["missing_by_rarity"] == {"mythic": 1, "rare": 1}

    collection_profile = json.loads((status_root / "collection_profile_latest.json").read_text(encoding="utf-8"))
    assert collection_profile["collection_available"] is True
    assert collection_profile["active_deck_missing_by_rarity"] == {"mythic": 1, "rare": 1}

    timeline_payload = json.loads((status_root / "active_match_timeline_latest.json").read_text(encoding="utf-8"))
    assert timeline_payload["match_id"] == "match-1"
    assert timeline_payload["total_entries"] == 1
    assert timeline_payload["entries"][0]["event_kind"] == "ClientAction"


def test_connect_resp_deck_evidence_does_not_update_active_submitted_deck(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    state._CONTEXT.update(
        {
            "current_match_id": "match-connect",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )
    event = GameStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 0, 2, tzinfo=UTC), b"connect-raw"),
        {
            "type": "connect_resp",
            "deck_cards": [1001, 1002],
            "sideboard_cards": [2001],
            "game_state_id": 77,
            "raw_connect_resp": {
                "type": "GREMessageType_ConnectResp",
                "connectResp": {"deckMessage": {"deckCards": [1001, 1002], "sideboardCards": [2001]}},
            },
        },
    )

    runtime_surfaces.observe_event(event, include_in_timeline=True)

    assert not (status_root / "active_submitted_deck_latest.json").exists()
    assert not (status_root / "active_deck_profile_latest.json").exists()
    timeline_payload = json.loads((status_root / "active_match_timeline_latest.json").read_text(encoding="utf-8"))
    assert timeline_payload["entries"][0]["event_kind"] == "GameState"
    assert timeline_payload["entries"][0]["event_type"] == "connect_resp"


def test_filter_match_history_payload_applies_filters() -> None:
    payload = {
        "matches": [
            {
                "match_id": "m1",
                "result": "W",
                "mtga_format": "Standard",
                "mtga_queue_type": "Best of 3",
                "event_id": "Play",
                "rank_match_type": "unranked",
                "play_mode_family": "constructed",
                "event_family": "queue",
                "queue_subtype": "traditional_play_queue",
                "date": "2026-05-05",
                "deck": {"name": "Deck A", "signature": "aaa"},
            },
            {
                "match_id": "m2",
                "result": "L",
                "mtga_format": "Standard",
                "mtga_queue_type": "Best of 1",
                "event_id": "Play",
                "rank_match_type": "unranked",
                "play_mode_family": "constructed",
                "event_family": "queue",
                "queue_subtype": "play_queue",
                "date": "2026-05-05",
                "deck": {"name": "Deck B", "signature": "bbb"},
            },
        ]
    }

    filtered = runtime_surfaces.filter_match_history_payload(
        payload,
        {
            "deck_name": "Deck A",
            "result": "W",
            "rank_match_type": "unranked",
            "play_mode_family": "constructed",
            "event_family": "queue",
            "queue_subtype": "traditional_play_queue",
        },
    )

    assert filtered["total_matches"] == 1
    assert filtered["matches"][0]["match_id"] == "m1"
    assert filtered["available_filters"]["event_families"] == ["queue"]


def test_observe_event_writes_match_history_for_ready_summary(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    runtime_surfaces._CARD_LOOKUP_CACHE = {}

    summary = MatchSummary(match_id="match-ready")
    summary.first_event_time = "2026-05-05T21:00:00+00:00"
    summary.last_event_time = "2026-05-05T21:30:00+00:00"
    summary.player_team = 1
    summary.match_winner_team = 1
    summary.super_format = "SuperFormat_Standard"
    summary.match_win_condition = "MatchWinCondition_BestOfThree"
    summary.event_id = "Play"
    summary.games[1].winner_team = 1
    summary.games[1].starting_player = 1
    summary.games[1].mulligans = 1
    state._MATCH_SUMMARIES["match-ready"] = summary
    state._CONTEXT.update(
        {
            "current_match_id": "match-ready",
            "current_game_number": 1,
            "current_player_team": 1,
        }
    )
    runtime_surfaces._MATCH_DECK_CONTEXTS["match-ready"] = {
        "signature": "deck-sig",
        "submitted_at": "2026-05-05T21:01:00+00:00",
        "mainboard_count": 60,
        "sideboard_count": 15,
    }

    match_state_event = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 30, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_completed",
            "state_type": "MatchGameRoomStateType_MatchCompleted",
            "match_id": "match-ready",
            "players": [],
        },
    )

    runtime_surfaces.observe_event(match_state_event, include_in_timeline=True)

    history_payload = json.loads((status_root / "match_history_latest.json").read_text(encoding="utf-8"))
    assert history_payload["total_matches"] == 1
    assert history_payload["matches"][0]["match_id"] == "match-ready"
    assert history_payload["matches"][0]["deck"]["signature"] == "deck-sig"


def test_refresh_match_history_snapshot_rewrites_current_history_contract(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)

    summary = MatchSummary(match_id="match-refresh")
    summary.first_event_time = "2026-05-10T17:08:48+00:00"
    summary.last_event_time = "2026-05-10T17:27:50+00:00"
    summary.player_team = 1
    summary.match_winner_team = 2
    summary.event_id = "Traditional_Ladder"
    summary.super_format = "SuperFormat_Constructed"
    summary.match_win_condition = "MatchWinCondition_Best2of3"
    summary.games[1].winner_team = 2
    summary.games[2].winner_team = 1
    summary.games[3].winner_team = 2
    state._MATCH_SUMMARIES["match-refresh"] = summary

    payload = runtime_surfaces.refresh_match_history_snapshot()

    assert payload["total_matches"] == 1
    match = payload["matches"][0]
    assert match["match_id"] == "match-refresh"
    assert match["rank_match_type"] == "ranked"
    assert match["play_mode_family"] == "constructed"
    assert match["event_family"] == "ladder"
    assert match["queue_subtype"] == "traditional_ranked_ladder"
    written = json.loads((status_root / "match_history_latest.json").read_text(encoding="utf-8"))
    assert written["matches"][0]["match_id"] == "match-refresh"


def test_observe_event_refreshes_ready_match_history_when_late_enrichment_arrives(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    runtime_surfaces._CARD_LOOKUP_CACHE = {}

    summary = MatchSummary(match_id="match-enriched")
    summary.first_event_time = "2026-05-05T21:00:00+00:00"
    summary.last_event_time = "2026-05-05T21:30:00+00:00"
    summary.player_team = 1
    summary.match_winner_team = 2
    summary.super_format = "SuperFormat_Standard"
    summary.match_win_condition = "MatchWinCondition_BestOfThree"
    summary.event_id = "Traditional_Ladder"
    summary.games[1].winner_team = 2
    summary.games[2].winner_team = 2
    state._MATCH_SUMMARIES["match-enriched"] = summary
    state._CONTEXT.update(
        {
            "current_match_id": "match-enriched",
            "current_game_number": 2,
            "current_player_team": 1,
        }
    )
    runtime_surfaces._MATCH_DECK_CONTEXTS["match-enriched"] = {
        "signature": "deck-sig",
        "submitted_at": "2026-05-05T21:01:00+00:00",
        "mainboard_count": 3,
        "sideboard_count": 1,
        "deck_cards": [1001, 1001, 2002],
        "sideboard_cards": [3003],
    }

    match_state_event = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 30, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_completed",
            "state_type": "MatchGameRoomStateType_MatchCompleted",
            "match_id": "match-enriched",
            "players": [],
        },
    )
    runtime_surfaces.observe_event(match_state_event, include_in_timeline=False)

    history_payload = json.loads((status_root / "match_history_latest.json").read_text(encoding="utf-8"))
    history_item = history_payload["matches"][0]
    assert history_item["deck"]["name"] == ""
    assert history_item["rank"] == ""
    assert history_item["constructed_rank_raw"] == ""

    deck_collection_event = DeckCollectionEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 30, 1, tzinfo=UTC), b"raw"),
        {
            "type": "deck_collection_snapshot",
            "decks": {
                "deck-1": {
                    "DeckId": "deck-1",
                    "Name": "GBv2",
                    "Attributes": [
                        {"name": "Format", "value": "Standard"},
                    ],
                    "list": {
                        "MainDeck": [
                            {"cardId": 1001, "quantity": 2},
                            {"cardId": 2002, "quantity": 1},
                        ],
                        "Sideboard": [
                            {"cardId": 3003, "quantity": 1},
                        ],
                    },
                }
            },
        },
    )
    runtime_surfaces.observe_event(deck_collection_event, include_in_timeline=False)

    history_payload = json.loads((status_root / "match_history_latest.json").read_text(encoding="utf-8"))
    history_item = history_payload["matches"][0]
    assert history_item["deck"]["name"] == "GBv2"
    assert history_item["deck"]["deck_id"] == "deck-1"
    assert history_item["deck"]["format"] == "Standard"
    assert history_item["rank"] == ""
    assert history_item["constructed_rank_raw"] == ""

    summary.constructed_rank = "Diamond 4"
    summary.constructed_class = "Diamond"
    summary.constructed_level = "4"
    rank_event = RankEvent(
        EventMetadata(datetime(2026, 5, 5, 21, 30, 2, tzinfo=UTC), b"raw"),
        {
            "type": "rank_snapshot",
            "constructed_class": "Diamond",
            "constructed_level": 4,
            "raw_rank": {},
        },
    )
    runtime_surfaces.observe_event(rank_event, include_in_timeline=False)

    history_payload = json.loads((status_root / "match_history_latest.json").read_text(encoding="utf-8"))
    history_item = history_payload["matches"][0]
    assert history_item["rank"] == "Diamond"
    assert history_item["constructed_rank_raw"] == "Diamond 4"


def test_bootstrap_runtime_surfaces_restores_surface_state_without_rebinding_aliases(tmp_path, monkeypatch) -> None:
    _reset_runtime_surface_state()
    status_root = _patch_surface_paths(tmp_path, monkeypatch)
    status_root.mkdir(parents=True, exist_ok=True)

    (status_root / "active_submitted_deck_latest.json").write_text(
        json.dumps(
            {
                "submitted_at": "2026-05-05T21:01:00+00:00",
                "match_id": "match-bootstrap",
                "game_number": 2,
                "deck_cards": [1001, 1001, 2002],
                "sideboard_cards": [3003],
            }
        ),
        encoding="utf-8",
    )
    (status_root / "match_history_latest.json").write_text(
        json.dumps(
            {
                "matches": [
                    {
                        "match_id": "match-bootstrap",
                        "result": "W",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    runtime_surfaces.bootstrap_runtime_surfaces()

    assert runtime_surfaces._ACTIVE_DECK_STATE["match_id"] == "match-bootstrap"
    assert runtime_surfaces.SURFACE_STATE.active_deck_state["match_id"] == "match-bootstrap"
    assert runtime_surfaces._ACTIVE_DECK_STATE is runtime_surfaces.SURFACE_STATE.active_deck_state
    assert runtime_surfaces._MATCH_HISTORY["match-bootstrap"]["result"] == "W"
    assert runtime_surfaces.SURFACE_STATE.match_history["match-bootstrap"]["result"] == "W"
    assert runtime_surfaces._MATCH_HISTORY is runtime_surfaces.SURFACE_STATE.match_history
