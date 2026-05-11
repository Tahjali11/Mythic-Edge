from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace


def _load_launcher_module():
    launcher_path = Path(__file__).resolve().parents[1] / "tools" / "auto_launcher" / "manasight_launcher_auto.py"
    spec = importlib.util.spec_from_file_location("manasight_launcher_auto", launcher_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load launcher module from {launcher_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_runtime_status_returns_dict_for_valid_payload(tmp_path: Path) -> None:
    launcher = _load_launcher_module()
    project_root = tmp_path / "project"
    status_path = project_root / launcher.STATUS_RELATIVE_PATH
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps({"status": "running"}), encoding="utf-8")

    payload = launcher.load_runtime_status(project_root)

    assert payload == {"status": "running"}


def test_load_runtime_status_returns_empty_dict_for_missing_payload(tmp_path: Path) -> None:
    launcher = _load_launcher_module()
    project_root = tmp_path / "project"

    payload = launcher.load_runtime_status(project_root)

    assert payload == {}


def test_mousewheel_units_normalize_windows_and_linux_events() -> None:
    launcher = _load_launcher_module()

    assert launcher.LauncherApp._mousewheel_units(object(), SimpleNamespace(delta=120)) == -1
    assert launcher.LauncherApp._mousewheel_units(object(), SimpleNamespace(delta=-240)) == 2
    assert launcher.LauncherApp._mousewheel_units(object(), SimpleNamespace(delta=0, num=4)) == -1
    assert launcher.LauncherApp._mousewheel_units(object(), SimpleNamespace(delta=0, num=5)) == 1


def test_build_overview_readiness_marks_missing_script_as_blocked(tmp_path: Path) -> None:
    launcher = _load_launcher_module()
    project_root = tmp_path / "project"
    project_root.mkdir()
    player_log = tmp_path / "Player.log"
    player_log.write_text("", encoding="utf-8")

    items = launcher.build_overview_readiness(
        project_root=project_root,
        script_path=tmp_path / "missing_script.py",
        player_log_path=player_log,
        webhook_url="",
        sheet_posting_enabled=False,
        catalog_status_payload={},
    )

    by_key = {item["key"]: item for item in items}
    assert by_key["project_root"]["state"] == "ready"
    assert by_key["script"]["state"] == "blocked"
    assert by_key["webhook"]["detail"] == "Local logging only"


def test_build_overview_hero_prefers_blocked_state_when_setup_is_incomplete() -> None:
    launcher = _load_launcher_module()
    hero = launcher.build_overview_hero(
        readiness_items=[
            {"key": "project_root", "title": "Project root", "state": "ready", "detail": "Found"},
            {"key": "script", "title": "Filtered script", "state": "blocked", "detail": "Missing"},
        ],
        parser_running=False,
        status_payload={},
    )

    assert hero["badge"] == "Blocked"
    assert hero["tone"] == "danger"


def test_build_overview_hero_uses_warning_triangle_copy_for_review_state() -> None:
    launcher = _load_launcher_module()
    hero = launcher.build_overview_hero(
        readiness_items=[
            {"key": "project_root", "title": "Project root", "state": "ready", "detail": "Found"},
            {"key": "catalog", "title": "Card catalog", "state": "warning", "detail": "Refresh recommended"},
        ],
        parser_running=False,
        status_payload={},
    )

    assert hero["badge"] == "Review"
    assert hero["headline"] == "\u25b2 1 item(s) should be reviewed before you begin"


def test_format_scryfall_refresh_timestamp_uses_requested_readable_format() -> None:
    launcher = _load_launcher_module()

    formatted = launcher.format_scryfall_refresh_timestamp("2026-05-08T09:02:43+00:00")

    assert formatted.endswith("AM")
    assert "08-05-2026 at " in formatted


def test_build_candidate_confirmation_snapshot_marks_deferred_rows() -> None:
    launcher = _load_launcher_module()
    report_payload = {
        "unresolved_mainboard_grp_ids": [
            {
                "grp_id": 99991,
                "section": "mainboard",
                "top_candidate_name": "Mosswood Dreadknight // Dread Whispers",
                "top_candidate_score": 164,
                "confidence_percent": 87,
                "auto_suggestion": "Mosswood Dreadknight // Dread Whispers",
                "confirmation_status": "ready",
                "confirmation_reasons": ["Strong evidence"],
                "ranked_candidates": [
                    {
                        "name": "Mosswood Dreadknight // Dread Whispers",
                        "score": 164,
                        "reasons": ["Top match"],
                    }
                ],
            }
        ],
        "unresolved_sideboard_grp_ids": [],
    }
    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "candidate_review": {
                    "status": "deferred",
                    "suggested_name": "Mosswood Dreadknight // Dread Whispers",
                    "deferred_at": "2026-05-08T09:02:43+00:00",
                }
            }
        }
    }

    snapshot = launcher.build_candidate_confirmation_snapshot(report_payload, override_payload)

    assert "deferred" in snapshot["summary"].lower()
    assert len(snapshot["entries"]) == 1
    assert snapshot["entries"][0]["promotion_status"] == "Deferred"
    assert snapshot["entries"][0]["evidence_match_percent"] == ""
    assert snapshot["entries"][0]["evidence_label"] == "Not scored yet"
    assert snapshot["entries"][0]["legacy_confidence_percent"] == 87


def test_build_candidate_confirmation_snapshot_marks_missing_confidence_as_not_scored_yet() -> None:
    launcher = _load_launcher_module()
    report_payload = {
        "unresolved_mainboard_grp_ids": [
            {
                "grp_id": 97452,
                "section": "mainboard",
                "auto_suggestion": "Earthbender Ascension",
                "confirmation_status": "ready",
                "opening_hand_observations": 0,
                "local_private_hand_observations": 61,
                "manual_confirmation_hits": 61,
                "exact_manual_confirmation_hits": 0,
                "confirmation_reasons": ["Top candidate leads clearly."],
                "ranked_candidates": [
                    {
                        "name": "Earthbender Ascension",
                        "score": 262,
                        "reasons": ["Exact count match with submitted deck"],
                    }
                ],
            }
        ],
        "unresolved_sideboard_grp_ids": [],
    }

    snapshot = launcher.build_candidate_confirmation_snapshot(report_payload, {"cards_by_grp_id": {}})

    entry = snapshot["entries"][0]
    assert entry["evidence_match_percent"] == ""
    assert entry["evidence_label"] == "Not scored yet"
    assert entry["top_candidate_score"] == 262
    assert "Refresh the MTGA card library review queue" in " ".join(entry["next_actions"])


def test_build_candidate_confirmation_snapshot_marks_blocked_rows_as_blocked() -> None:
    launcher = _load_launcher_module()
    report_payload = {
        "unresolved_mainboard_grp_ids": [
            {
                "grp_id": 97547,
                "section": "mainboard",
                "top_candidate_name": "Example Card",
                "confidence_percent": 14,
                "confirmation_status": "blocked",
                "confirmation_reasons": ["Blocked by contradiction or an explicit no-promotion flag."],
                "ranked_candidates": [
                    {
                        "name": "Example Card",
                        "score": 88,
                        "reasons": ["Observed in private hand zones"],
                    }
                ],
            }
        ],
        "unresolved_sideboard_grp_ids": [],
    }

    snapshot = launcher.build_candidate_confirmation_snapshot(report_payload, {"cards_by_grp_id": {}})

    entry = snapshot["entries"][0]
    assert entry["promotion_status"] == "Blocked by contradiction"
    assert entry["evidence_label"] == "Blocked"
    assert "contradiction" in " ".join(entry["next_actions"]).lower()


def test_build_candidate_confirmation_snapshot_skips_already_confirmed_rows() -> None:
    launcher = _load_launcher_module()
    report_payload = {
        "unresolved_mainboard_grp_ids": [
            {
                "grp_id": 99991,
                "section": "mainboard",
                "top_candidate_name": "Mosswood Dreadknight // Dread Whispers",
                "evidence_match_percent": 91,
                "promotion_status": "Ready for confirmation",
                "confirmation_status": "ready",
                "ranked_candidates": [
                    {
                        "name": "Mosswood Dreadknight // Dread Whispers",
                        "score": 164,
                        "reasons": ["Top match"],
                    }
                ],
            }
        ],
        "unresolved_sideboard_grp_ids": [],
    }
    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "Mosswood Dreadknight // Dread Whispers",
                "name_source": "manual_review_confirmed_candidate",
            }
        }
    }

    snapshot = launcher.build_candidate_confirmation_snapshot(report_payload, override_payload)

    assert snapshot["entries"] == []


def test_build_catalog_candidate_item_id_is_unique_across_duplicate_sections() -> None:
    launcher = _load_launcher_module()
    mainboard_entry = {"grp_id": 97369, "section": "mainboard"}
    sideboard_entry = {"grp_id": 97369, "section": "sideboard"}
    repeated_sideboard_entry = {"grp_id": 97369, "section": "sideboard"}

    mainboard_id = launcher.build_catalog_candidate_item_id(mainboard_entry)
    sideboard_id = launcher.build_catalog_candidate_item_id(sideboard_entry)
    repeated_sideboard_id = launcher.build_catalog_candidate_item_id(
        repeated_sideboard_entry,
        duplicate_index=1,
    )

    assert mainboard_id == "97369::mainboard"
    assert sideboard_id == "97369::sideboard"
    assert repeated_sideboard_id == "97369::sideboard::2"


def test_set_catalog_candidate_detail_preserves_scroll_for_same_selected_item() -> None:
    launcher = _load_launcher_module()

    class FakeText:
        def __init__(self) -> None:
            self.value = "Existing detail"
            self.view = (0.72, 0.96)

        def configure(self, **_kwargs: object) -> None:
            pass

        def delete(self, _start: str, _end: str) -> None:
            self.value = ""

        def insert(self, _start: str, text: str) -> None:
            self.value = text

        def get(self, _start: str, _end: str) -> str:
            return self.value

        def yview(self) -> tuple[float, float]:
            return self.view

        def yview_moveto(self, first: float) -> None:
            span = self.view[1] - self.view[0]
            self.view = (first, first + span)

    app = launcher.LauncherApp.__new__(launcher.LauncherApp)
    app.catalog_candidate_detail_text = FakeText()
    app._catalog_candidate_detail_item_id = "97369::sideboard"

    app._set_catalog_candidate_detail(
        "Updated detail",
        selected_item_id="97369::sideboard",
        preserve_view=True,
    )

    assert app.catalog_candidate_detail_text.value == "Updated detail"
    assert app.catalog_candidate_detail_text.view[0] == 0.72
    assert app._catalog_candidate_detail_item_id == "97369::sideboard"
