from __future__ import annotations

import os
from pathlib import Path

_TRUE_ENV_VALUES = frozenset({"1", "true", "yes", "y"})
_PRIMARY_ENV_PREFIX = "MYTHICEDGE_"
_LEGACY_ENV_PREFIX = "MANASIGHT_"

DEFAULT_MTGA_PLAYER_LOG = Path(
    r"C:\Users\Tahj Blow\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log"
)
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WEBHOOK_URL = ""


def _legacy_env_name(name: str) -> str | None:
    if name.startswith(_PRIMARY_ENV_PREFIX):
        return _LEGACY_ENV_PREFIX + name[len(_PRIMARY_ENV_PREFIX) :]
    return None


def _env_text(name: str, default: str, *, fallback_on_blank: bool = False) -> str:
    value = os.environ.get(name)
    if value is None:
        legacy_name = _legacy_env_name(name)
        if legacy_name is not None:
            value = os.environ.get(legacy_name)
    if value is None:
        value = default
    text = str(value)
    if fallback_on_blank:
        stripped = text.strip()
        return stripped or default
    return text


def _env_path(name: str, default: Path) -> Path:
    return Path(_env_text(name, str(default)))


def _env_int(name: str, default: int) -> int:
    raw_value = _env_text(name, str(default), fallback_on_blank=True)
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return default


def _env_flag(name: str, default: bool) -> bool:
    raw_value = _env_text(name, "1" if default else "0", fallback_on_blank=True)
    return raw_value.strip().lower() in _TRUE_ENV_VALUES


def _project_data_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath("data", *parts)


def _status_path(*parts: str) -> Path:
    return STATUS_ROOT.joinpath(*parts)


def _oracle_data_path(*parts: str) -> Path:
    return ORACLE_DATA_ROOT.joinpath(*parts)


def _tier_sources_path(*parts: str) -> Path:
    return TIER_SOURCES_ROOT.joinpath(*parts)


def _decklists_path(*parts: str) -> Path:
    return DECKLISTS_ROOT.joinpath(*parts)


KEEP_EVENT_LIFECYCLE_TYPES = {
    "event_join",
    "event_enter_pairing",
    "event_claim_prize",
}

KEEP_CLIENT_ACTION_TYPES = {
    "mulligan_resp",
    "submit_deck_resp",
}

KEEP_GENERIC_CLIENT_MESSAGE_TYPES = {
    "ClientMessageType_ChooseStartingPlayerResp",
    "ClientMessageType_EnterSideboardingReq",
    "ClientMessageType_SubmitDeckResp",
    "ClientMessageType_MulliganResp",
}


LOG_PATH = _env_path("MTGA_PLAYER_LOG", DEFAULT_MTGA_PLAYER_LOG)
PROJECT_ROOT = _env_path("MYTHICEDGE_PROJECT_ROOT", DEFAULT_PROJECT_ROOT)

MATCH_LOGS_ROOT = _env_path("MYTHICEDGE_MATCH_LOGS_ROOT", _project_data_path("match_logs"))
TIER_SOURCES_ROOT = _env_path("MYTHICEDGE_TIER_SOURCES_ROOT", _project_data_path("tier_sources"))
ORACLE_DATA_ROOT = _env_path("MYTHICEDGE_ORACLE_DATA_ROOT", _project_data_path("oracle_data"))
DECKLISTS_ROOT = _env_path("MYTHICEDGE_DECKLISTS_ROOT", _project_data_path("decklists"))
RUNTIME_LOGS_ROOT = _env_path("MYTHICEDGE_RUNTIME_LOGS_ROOT", _project_data_path("runtime_logs"))
STATUS_ROOT = _env_path("MYTHICEDGE_STATUS_ROOT", _project_data_path("status"))
FAILED_POSTS_ROOT = _env_path("MYTHICEDGE_FAILED_POSTS_ROOT", _project_data_path("failed_posts"))
BAD_EVENTS_ROOT = _env_path("MYTHICEDGE_BAD_EVENTS_ROOT", _project_data_path("bad_events"))

CURRENT_DECKLIST_PATH = _env_path(
    "MYTHICEDGE_CURRENT_DECKLIST_PATH",
    _decklists_path("current_deck_latest.json"),
)
HAND_CONFIRMATIONS_PATH = _env_path(
    "MYTHICEDGE_HAND_CONFIRMATIONS_PATH",
    _oracle_data_path("hand-confirmations-latest.json"),
)
ACTIVE_MATCH_SNAPSHOT_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_MATCH_SNAPSHOT_PATH",
    _status_path("active_match_snapshot_latest.json"),
)
ACTIVE_MATCH_TIMELINE_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_MATCH_TIMELINE_PATH",
    _status_path("active_match_timeline_latest.json"),
)
STATUS_TIMELINES_ROOT = _env_path(
    "MYTHICEDGE_STATUS_TIMELINES_ROOT",
    _status_path("timelines"),
)
ACTIVE_DECK_PROFILE_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_DECK_PROFILE_PATH",
    _status_path("active_deck_profile_latest.json"),
)
MATCH_HISTORY_PATH = _env_path(
    "MYTHICEDGE_MATCH_HISTORY_PATH",
    _status_path("match_history_latest.json"),
)
COLLECTION_PROFILE_PATH = _env_path(
    "MYTHICEDGE_COLLECTION_PROFILE_PATH",
    _status_path("collection_profile_latest.json"),
)
ACTIVE_MATCH_ACTIONS_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_MATCH_ACTIONS_PATH",
    _status_path("active_match_actions_latest.json"),
)
ACTIVE_MATCH_ACTION_LOG_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_MATCH_ACTION_LOG_PATH",
    _status_path("active_match_action_log_latest.md"),
)
STATUS_ACTIONS_ROOT = _env_path(
    "MYTHICEDGE_STATUS_ACTIONS_ROOT",
    _status_path("actions"),
)
CARD_PERFORMANCE_PATH = _env_path(
    "MYTHICEDGE_CARD_PERFORMANCE_PATH",
    _status_path("card_performance_latest.json"),
)
CARD_PERFORMANCE_MARKDOWN_PATH = _env_path(
    "MYTHICEDGE_CARD_PERFORMANCE_MARKDOWN_PATH",
    _status_path("card_performance_latest.md"),
)
CARD_CATALOG_REFRESH_STATUS_PATH = _env_path(
    "MYTHICEDGE_CARD_CATALOG_REFRESH_STATUS_PATH",
    _status_path("card_catalog_refresh_status_latest.json"),
)
GRP_ID_OVERRIDES_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_OVERRIDES_PATH",
    _oracle_data_path("mtga-grp-id-overrides-latest.json"),
)
GRP_ID_CATALOG_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_CATALOG_PATH",
    _oracle_data_path("mtga-grp-id-catalog-latest.json"),
)
GRP_ID_INFERRED_REVIEW_JSON_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_INFERRED_REVIEW_JSON_PATH",
    _oracle_data_path("grp-id-inferred-review-latest.json"),
)
GRP_ID_CANDIDATE_REPORT_JSON_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_CANDIDATE_REPORT_JSON_PATH",
    _oracle_data_path("grp-id-candidate-report-latest.json"),
)
GRP_ID_CANDIDATE_REPORT_MARKDOWN_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_CANDIDATE_REPORT_MARKDOWN_PATH",
    _oracle_data_path("grp-id-candidate-report-latest.md"),
)
GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH = _env_path(
    "MYTHICEDGE_GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH",
    _oracle_data_path("grp-id-inferred-review-latest.md"),
)
ACTIVE_SUBMITTED_DECK_PATH = _env_path(
    "MYTHICEDGE_ACTIVE_SUBMITTED_DECK_PATH",
    _status_path("active_submitted_deck_latest.json"),
)
TIER_NORMALIZATION_PATH = _env_path(
    "MYTHICEDGE_TIER_NORMALIZATION_PATH",
    _tier_sources_path("normalization_overrides.json"),
)


OUT_FILENAME_PREFIX = _env_text("MYTHICEDGE_OUT_PREFIX", "mtga_filtered_events_v11")
WEBHOOK_URL = _env_text("MYTHICEDGE_SHEETS_WEBHOOK", DEFAULT_WEBHOOK_URL)
LOCAL_PLAYER_INDEX = _env_int("MYTHICEDGE_LOCAL_PLAYER_INDEX", 0)
STATUS_API_HOST = _env_text(
    "MYTHICEDGE_STATUS_API_HOST",
    "127.0.0.1",
    fallback_on_blank=True,
)
STATUS_API_PORT = _env_int("MYTHICEDGE_STATUS_API_PORT", 6843)


POST_GAMESTATE_ROWS = _env_flag("MYTHICEDGE_POST_GAMESTATE", False)
POST_RAW_EVENT_ROWS = _env_flag("MYTHICEDGE_POST_RAW_EVENTS", False)
POST_MATCH_LOG_ROWS = _env_flag("MYTHICEDGE_POST_MATCH_LOG_ROWS", True)
POST_GAME_LOG_ROWS = _env_flag("MYTHICEDGE_POST_GAME_LOG_ROWS", True)
POST_MATCH_SUMMARY_ROWS = _env_flag("MYTHICEDGE_POST_MATCH_SUMMARIES", True)
POST_ACTION_LOG_ROWS = _env_flag("MYTHICEDGE_POST_ACTION_LOG_ROWS", True)
POST_DECK_SNAPSHOT_ROWS = _env_flag("MYTHICEDGE_POST_DECK_SNAPSHOT_ROWS", True)
POST_COLLECTION_SNAPSHOT_ROWS = _env_flag("MYTHICEDGE_POST_COLLECTION_SNAPSHOT_ROWS", False)
POST_PARSER_STATUS_ROWS = _env_flag("MYTHICEDGE_POST_PARSER_STATUS_ROWS", False)
POST_CARD_PERFORMANCE_ROWS = _env_flag("MYTHICEDGE_POST_CARD_PERFORMANCE_ROWS", True)
SYNC_TIER_BUCKETS = _env_flag("MYTHICEDGE_SYNC_TIER_BUCKETS", True)
SYNC_CARD_CATALOG = _env_flag("MYTHICEDGE_SYNC_CARD_CATALOG", True)
ENABLE_STATUS_API = _env_flag("MYTHICEDGE_ENABLE_STATUS_API", True)
