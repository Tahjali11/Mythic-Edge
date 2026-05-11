from __future__ import annotations

from typing import Any


def is_game_over(game_state_payload: dict[str, Any]) -> bool:
    game_info = _game_info_payload(game_state_payload)
    stage = str(game_info.get("stage") or game_state_payload.get("stage") or "")
    return stage == "GameStage_GameOver"


def build_game_result_payload(game_state_payload: dict[str, Any]) -> dict[str, Any]:
    game_info = _game_info_payload(game_state_payload)
    results = _results_payload(game_info)
    game_scope = _selected_game_result(results)

    return {
        "type": "game_result",
        "source": "gre_game_state",
        "stage": str(game_info.get("stage") or ""),
        "match_state": str(game_info.get("matchState") or ""),
        "winning_team_id": game_scope.get("winningTeamId", 0),
        "result_type": game_scope.get("result", ""),
        "reason": game_scope.get("reason", ""),
        "results": results,
        "game_info": game_info,
        "identity": _identity_payload(game_state_payload),
        "game_state_id": game_state_payload.get("game_state_id"),
        "message_type": game_state_payload.get("message_type", ""),
    }


def _game_info_payload(game_state_payload: dict[str, Any]) -> dict[str, Any]:
    game_info = game_state_payload.get("game_info")
    if isinstance(game_info, dict):
        return dict(game_info)
    return {}


def _results_payload(game_info: dict[str, Any]) -> list[Any]:
    results = game_info.get("results")
    if isinstance(results, list):
        return list(results)
    return []


def _selected_game_result(results: list[Any]) -> dict[str, Any]:
    game_scope = _latest_game_scope_result(results)
    if game_scope is not None:
        return game_scope

    fallback_result = _last_dict_result(results)
    if fallback_result is not None:
        return fallback_result
    return {}


def _identity_payload(game_state_payload: dict[str, Any]) -> dict[str, Any]:
    identity = game_state_payload.get("identity")
    if isinstance(identity, dict):
        return dict(identity)
    return {}


def _latest_game_scope_result(results: Any) -> dict[str, Any] | None:
    if not isinstance(results, list):
        return None

    latest: dict[str, Any] | None = None
    for result in results:
        if isinstance(result, dict) and result.get("scope") == "MatchScope_Game":
            latest = result
    return latest


def _last_dict_result(results: list[Any]) -> dict[str, Any] | None:
    for result in reversed(results):
        if isinstance(result, dict):
            return result
    return None
