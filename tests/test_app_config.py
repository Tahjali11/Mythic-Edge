import importlib
import tomllib
from pathlib import Path

import mythic_edge_parser.app.config as app_config


def test_default_match_logs_root_uses_data_folder(monkeypatch) -> None:
    project_root = Path(r"C:\example\Mythic Edge")
    monkeypatch.setenv("MYTHICEDGE_PROJECT_ROOT", str(project_root))
    monkeypatch.delenv("MYTHICEDGE_MATCH_LOGS_ROOT", raising=False)
    monkeypatch.delenv("MYTHICEDGE_RUNTIME_LOGS_ROOT", raising=False)
    monkeypatch.delenv("MYTHICEDGE_FAILED_POSTS_ROOT", raising=False)
    monkeypatch.delenv("MYTHICEDGE_BAD_EVENTS_ROOT", raising=False)
    monkeypatch.delenv("MYTHICEDGE_POST_RAW_EVENTS", raising=False)
    monkeypatch.delenv("MYTHICEDGE_POST_GAME_LOG_ROWS", raising=False)
    monkeypatch.delenv("MYTHICEDGE_POST_MATCH_LOG_ROWS", raising=False)
    monkeypatch.delenv("MYTHICEDGE_SYNC_TIER_BUCKETS", raising=False)

    config = importlib.reload(app_config)
    assert config.MATCH_LOGS_ROOT == project_root / "data" / "match_logs"
    assert config.TIER_SOURCES_ROOT == project_root / "data" / "tier_sources"
    assert config.RUNTIME_LOGS_ROOT == project_root / "data" / "runtime_logs"
    assert config.FAILED_POSTS_ROOT == project_root / "data" / "failed_posts"
    assert config.BAD_EVENTS_ROOT == project_root / "data" / "bad_events"
    assert config.POST_RAW_EVENT_ROWS is False
    assert config.POST_GAME_LOG_ROWS is True
    assert config.POST_MATCH_LOG_ROWS is True
    assert config.SYNC_TIER_BUCKETS is True


def test_default_mtga_player_log_uses_home_directory_without_committed_profile_name() -> None:
    windows_home = Path("C:") / "Users" / "Arena Player"
    mac_home = Path("/") / "Users" / "arena-player"

    assert app_config._default_mtga_player_log(home=windows_home, platform="win32") == (
        windows_home / "AppData" / "LocalLow" / "Wizards Of The Coast" / "MTGA" / "Player.log"
    )
    assert app_config._default_mtga_player_log(home=mac_home, platform="darwin") == (
        mac_home / "Library" / "Logs" / "Wizards Of The Coast" / "MTGA" / "Player.log"
    )


def test_package_author_metadata_uses_project_owner() -> None:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert pyproject["project"]["authors"] == [{"name": "Tahj Blow"}]


def test_invalid_integer_env_values_fall_back_to_defaults(monkeypatch) -> None:
    monkeypatch.setenv("MYTHICEDGE_LOCAL_PLAYER_INDEX", "not-a-number")
    monkeypatch.setenv("MYTHICEDGE_STATUS_API_PORT", "bad-port")

    config = importlib.reload(app_config)

    assert config.LOCAL_PLAYER_INDEX == 0
    assert config.STATUS_API_PORT == 6843


def test_blank_status_api_host_falls_back_to_loopback(monkeypatch) -> None:
    monkeypatch.setenv("MYTHICEDGE_STATUS_API_HOST", "   ")

    config = importlib.reload(app_config)

    assert config.STATUS_API_HOST == "127.0.0.1"


def test_legacy_manasight_env_prefix_still_overrides_defaults(monkeypatch) -> None:
    legacy_root = Path(r"C:\example\LegacyManasight")
    monkeypatch.delenv("MYTHICEDGE_PROJECT_ROOT", raising=False)
    monkeypatch.setenv("MANASIGHT_PROJECT_ROOT", str(legacy_root))

    config = importlib.reload(app_config)

    assert config.PROJECT_ROOT == legacy_root
