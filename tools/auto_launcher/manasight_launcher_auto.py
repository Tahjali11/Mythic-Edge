import json
import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

APP_NAME = "Mythic Edge Launcher"
SETTINGS_FILE = Path.home() / ".mythic_edge_launcher_settings.json"
LEGACY_SETTINGS_FILE = Path.home() / ".manasight_launcher_settings.json"
DEFAULT_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])


def _default_player_log() -> str:
    if sys.platform == "darwin":
        return str(Path.home() / "Library" / "Logs" / "Wizards Of The Coast" / "MTGA" / "Player.log")
    return str(Path.home() / "AppData" / "LocalLow" / "Wizards Of The Coast" / "MTGA" / "Player.log")


DEFAULT_PLAYER_LOG = _default_player_log()
DEFAULT_MTGA_PROCESS = "MTGA.exe"
STATUS_RELATIVE_PATH = Path("data") / "status" / "manasight_status_latest.json"
CARD_CATALOG_REFRESH_STATUS_RELATIVE_PATH = Path("data") / "status" / "card_catalog_refresh_status_latest.json"
RUNTIME_LOGS_RELATIVE_ROOT = Path("data") / "runtime_logs"
FAILED_POSTS_RELATIVE_ROOT = Path("data") / "failed_posts"
BAD_EVENTS_RELATIVE_ROOT = Path("data") / "bad_events"
ORACLE_DATA_RELATIVE_ROOT = Path("data") / "oracle_data"
HAND_CONFIRMATIONS_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "hand-confirmations-latest.json"
HAND_CONFIRMATIONS_MARKDOWN_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "hand-confirmations-latest.md"
CANDIDATE_REPORT_JSON_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "grp-id-candidate-report-latest.json"
CANDIDATE_REPORT_MARKDOWN_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "grp-id-candidate-report-latest.md"
GRP_ID_OVERRIDES_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "mtga-grp-id-overrides-latest.json"
INFERRED_REVIEW_JSON_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "grp-id-inferred-review-latest.json"
INFERRED_REVIEW_MARKDOWN_RELATIVE_PATH = ORACLE_DATA_RELATIVE_ROOT / "grp-id-inferred-review-latest.md"
OVERVIEW_COLORS = {
    "bg": "#0f1214",
    "card": "#171b1d",
    "card_alt": "#1d2326",
    "border": "#2a3237",
    "text": "#f4f1ea",
    "muted": "#b7c0c6",
    "accent": "#87a3b4",
    "success": "#7f9a77",
    "warning": "#b59a66",
    "danger": "#a86d68",
}


def load_settings() -> dict:
    for path in (SETTINGS_FILE, LEGACY_SETTINGS_FILE):
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return payload if isinstance(payload, dict) else {}
        except Exception:
            continue
    return {}


def save_settings(data: dict) -> None:
    try:
        SETTINGS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def is_process_running(process_name: str) -> bool:
    if not process_name:
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        text = (result.stdout or "") + "\n" + (result.stderr or "")
        return process_name.lower() in text.lower()
    except Exception:
        return False


def _load_json_status(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def load_runtime_status(project_root: Path) -> dict:
    path = project_root / STATUS_RELATIVE_PATH
    return _load_json_status(path)


def load_card_catalog_refresh_status(project_root: Path) -> dict:
    path = project_root / CARD_CATALOG_REFRESH_STATUS_RELATIVE_PATH
    return _load_json_status(path)


def load_candidate_report(project_root: Path) -> dict:
    path = project_root / CANDIDATE_REPORT_JSON_RELATIVE_PATH
    return _load_json_status(path)


def load_grp_id_override_payload(project_root: Path) -> dict:
    path = project_root / GRP_ID_OVERRIDES_RELATIVE_PATH
    return _load_json_status(path)


def latest_child_dir(root: Path) -> Path | None:
    if not root.exists():
        return None
    children = [path for path in root.iterdir() if path.is_dir()]
    if not children:
        return None
    return max(children, key=lambda path: path.stat().st_mtime)


def format_status_timestamp(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "n/a"
    try:
        normalized = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
        return dt.astimezone().strftime("%Y-%m-%d %I:%M:%S %p")
    except Exception:
        return text


def format_scryfall_refresh_timestamp(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "n/a"
    try:
        normalized = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized).astimezone()
        hour = dt.strftime("%I").lstrip("0") or "0"
        return f"{dt.strftime('%d-%m-%Y')} at {hour}:{dt.strftime('%M %p')}"
    except Exception:
        return text


def _parse_status_datetime(value: object) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except Exception:
        return None


def truncate_text(value: object, *, max_len: int = 96) -> str:
    text = str(value or "").strip()
    if not text:
        return "n/a"
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def build_health_snapshot(status_payload: dict) -> dict[str, str]:
    status_text = str(status_payload.get("status", "") or "").strip() or "No status file yet"
    event_kind = str(status_payload.get("last_event_kind", "") or "").strip()
    event_time = format_status_timestamp(status_payload.get("last_event_at"))
    if event_kind:
        last_event = f"{event_kind} at {event_time}"
    else:
        last_event = "No events seen yet"

    match_id = truncate_text(status_payload.get("current_match_id", ""))
    game_number = str(status_payload.get("current_game_number", "") or "").strip() or "n/a"
    player_team = str(status_payload.get("current_player_team", "") or "").strip() or "n/a"
    current_match = f"Match {match_id} | Game {game_number} | Team {player_team}"

    webhook_successes = int(status_payload.get("webhook_successes", 0) or 0)
    webhook_failures = int(status_payload.get("webhook_failures", 0) or 0)
    webhook_attempts = status_payload.get("last_webhook_attempts", "n/a")
    webhook_match = truncate_text(status_payload.get("last_webhook_match_id", ""))
    webhook_text = (
        f"{webhook_successes} ok / {webhook_failures} failed"
        f" | last attempts: {webhook_attempts}"
        f" | last match: {webhook_match}"
    )

    if status_payload.get("last_webhook_error"):
        last_error = (
            f"Webhook: {truncate_text(status_payload.get('last_webhook_error_type', 'Error'))}"
            f" | {truncate_text(status_payload.get('last_webhook_error', ''))}"
        )
    elif status_payload.get("last_event_error"):
        last_error = (
            f"Parser event: {truncate_text(status_payload.get('last_event_error_type', 'Error'))}"
            f" | {truncate_text(status_payload.get('last_event_error', ''))}"
        )
    elif status_payload.get("last_router_error"):
        last_error = (
            f"Router: {truncate_text(status_payload.get('last_router_error_type', 'Error'))}"
            f" | {truncate_text(status_payload.get('last_router_error', ''))}"
        )
    else:
        last_error = "No recent errors recorded"

    return {
        "status": status_text,
        "last_event": last_event,
        "current_match": current_match,
        "webhook": webhook_text,
        "last_error": last_error,
        "updated_at": format_status_timestamp(status_payload.get("updated_at")),
    }


def build_card_catalog_snapshot(status_payload: dict) -> dict[str, str]:
    if not status_payload:
        return {
            "refresh": "No card-catalog refresh status yet",
            "last_manual": "n/a",
            "review": "No inferred review status yet",
            "activation": "No catalog activation state yet",
        }

    last_manual_raw = status_payload.get("last_successful_manual_refresh_at")
    last_manual = _parse_status_datetime(last_manual_raw)
    stale_after_days = int(status_payload.get("stale_after_days", 45) or 45)
    if last_manual is None:
        refresh_text = "Manual card-catalog refresh has not run yet"
    else:
        age_days = max((datetime.now(last_manual.tzinfo or datetime.now().astimezone().tzinfo) - last_manual).days, 0)
        if age_days >= stale_after_days:
            refresh_text = f"Refresh recommended: last successful manual refresh was {age_days} day(s) ago"
        else:
            refresh_text = f"Catalog refresh looks current ({age_days} day(s) since manual refresh)"

    review_count = int(status_payload.get("inferred_review_entry_count", 0) or 0)
    candidate_error = str(status_payload.get("candidate_report_error", "") or "").strip()
    if review_count > 0:
        review_text = f"{review_count} inferred review suggestion(s) waiting"
    elif candidate_error:
        review_text = f"Candidate rescoring skipped: {truncate_text(candidate_error)}"
    else:
        review_text = "No inferred review suggestions waiting"

    if status_payload.get("next_restart_required"):
        activation_text = "Restart the parser to apply the latest MTGA card library"
    else:
        activation_text = "Latest MTGA card library is ready for the next parser run"

    return {
        "refresh": refresh_text,
        "last_manual": format_scryfall_refresh_timestamp(last_manual_raw),
        "review": review_text,
        "activation": activation_text,
    }


def _launcher_promotion_status_label(status_code: str) -> str:
    return {
        "ready": "Ready for confirmation",
        "candidate_only": "Needs review",
        "blocked": "Blocked by contradiction",
    }.get(status_code, "Needs review")


def _channel_rows(value: object) -> list[dict[str, Any]]:
    rows = value if isinstance(value, list) else []
    return [row for row in rows if isinstance(row, dict)]


def _candidate_next_actions(
    *,
    promotion_status: str,
    evidence_supported: bool,
    matched_channels: list[dict[str, Any]],
    contradictory_channels: list[dict[str, Any]],
    neutral_channels: list[dict[str, Any]],
    manual_confirmation_hits: int,
    exact_manual_confirmation_hits: int,
    runner_up_gap: int | str,
) -> list[str]:
    if promotion_status == "Blocked by contradiction":
        return [
            "Inspect the contradiction details below before confirming this grpId.",
            "If the fingerprint data is wrong, gather more live evidence or fix the override entry upstream.",
        ]
    if not evidence_supported:
        return ["Refresh the MTGA card library review queue so the parser can generate an evidence-based report."]

    actions: list[str] = []
    neutral_keys = {str(channel.get("key", "")).strip() for channel in neutral_channels}
    contradictory_keys = {str(channel.get("key", "")).strip() for channel in contradictory_channels}
    matched_keys = {str(channel.get("key", "")).strip() for channel in matched_channels}

    if exact_manual_confirmation_hits == 0:
        actions.append("Record an exact hand confirmation when you are certain of the card name.")
    if "mana_signature" in neutral_keys:
        actions.append("Capture the card on the stack or in hand so the parser can observe a mana-cost signature.")
    if "subtype_overlap" in neutral_keys:
        actions.append("Let the card appear on the battlefield or stack so subtype evidence can accumulate.")
    if "power_toughness" in neutral_keys:
        actions.append("Collect battlefield observations so the parser can learn the card's power and toughness.")
    if "zone_pattern" in neutral_keys or "action_pattern" in neutral_keys:
        actions.append("Play more matches so the parser can see more of this card's gameplay pattern.")
    if "color_overlap" in contradictory_keys:
        actions.append("Check whether this grpId may belong to a different color identity than the current suggestion.")
    if "mana_signature" in contradictory_keys:
        actions.append("Compare the observed mana signature against the suggested card's mana cost.")
    if "card_type" in contradictory_keys or "supertype_identity" in contradictory_keys:
        actions.append("Re-check the card type fingerprint, because the current suggestion conflicts with it.")
    if isinstance(runner_up_gap, int) and runner_up_gap < 40 and promotion_status == "Needs review":
        actions.append("Gather a bit more evidence so the top candidate separates itself from the runner-up.")
    if manual_confirmation_hits == 0 and "exact_manual_confirmation" not in matched_keys:
        actions.append("Use the hand tracker when this card shows up in hand so the parser gets direct confirmation.")

    deduped: list[str] = []
    seen: set[str] = set()
    for action in actions:
        if action not in seen:
            seen.add(action)
            deduped.append(action)
    return deduped


def _candidate_snapshot_sort_key(entry: dict[str, Any]) -> tuple[int, int, int, int]:
    status_order = {
        "Ready for confirmation": 0,
        "Needs review": 1,
        "Deferred": 2,
        "Blocked by contradiction": 3,
    }
    evidence_value = entry.get("evidence_match_percent")
    if not isinstance(evidence_value, int):
        evidence_value = -1
    return (
        status_order.get(str(entry.get("promotion_status", "")).strip(), 9),
        -evidence_value,
        -int(entry.get("top_candidate_score", 0) or 0),
        int(entry.get("grp_id", 0) or 0),
    )


def build_candidate_confirmation_snapshot(
    report_payload: dict,
    override_payload: dict,
) -> dict[str, Any]:
    if not report_payload:
        return {
            "summary": "No candidate report available yet",
            "entries": [],
        }

    raw_override_rows = override_payload.get("cards_by_grp_id") if isinstance(override_payload, dict) else {}
    override_rows = raw_override_rows if isinstance(raw_override_rows, dict) else {}
    entries: list[dict[str, Any]] = []

    for section_key in ("unresolved_mainboard_grp_ids", "unresolved_sideboard_grp_ids"):
        for raw_row in report_payload.get(section_key) or []:
            if not isinstance(raw_row, dict):
                continue
            grp_id = int(raw_row.get("grp_id", 0) or 0)
            if grp_id <= 0:
                continue
            ranked_candidates = raw_row.get("ranked_candidates") or []
            top_reasons = []
            top_ranked_name = ""
            top_ranked_score = ""
            if isinstance(ranked_candidates, list) and ranked_candidates:
                top_candidate = ranked_candidates[0]
                if isinstance(top_candidate, dict):
                    top_ranked_name = str(top_candidate.get("name", "") or "").strip()
                    top_ranked_score = top_candidate.get("score", "")
                    top_reasons = [
                        str(reason).strip() for reason in (top_candidate.get("reasons") or []) if str(reason).strip()
                    ]

            top_candidate_name = str(raw_row.get("top_candidate_name", "") or "").strip() or top_ranked_name
            auto_suggestion = str(raw_row.get("auto_suggestion", "") or "").strip()
            suggested_name = auto_suggestion or top_candidate_name
            if not suggested_name:
                continue

            override_entry = override_rows.get(str(grp_id))
            if not isinstance(override_entry, dict):
                override_entry = {}
            existing_name = str(override_entry.get("name", "") or "").strip()
            if existing_name:
                continue
            candidate_review = override_entry.get("candidate_review") or {}
            if not isinstance(candidate_review, dict):
                candidate_review = {}

            confirmation_status = str(raw_row.get("confirmation_status", "")).strip()
            promotion_status = str(raw_row.get("promotion_status", "") or "").strip()
            if not promotion_status:
                promotion_status = _launcher_promotion_status_label(confirmation_status)
            deferred_at = ""
            if (
                str(candidate_review.get("status", "")).strip() == "deferred"
                and str(candidate_review.get("suggested_name", "")).strip() == suggested_name
            ):
                promotion_status = "Deferred"
                deferred_at = format_scryfall_refresh_timestamp(candidate_review.get("deferred_at"))
            if confirmation_status == "blocked":
                promotion_status = "Blocked by contradiction"

            confirmation_reasons = [
                str(reason).strip() for reason in (raw_row.get("confirmation_reasons") or []) if str(reason).strip()
            ]
            raw_evidence_summary = raw_row.get("evidence_summary")
            evidence_summary = raw_evidence_summary if isinstance(raw_evidence_summary, dict) else {}
            evidence_supported = raw_row.get("evidence_match_percent") not in (None, "")
            evidence_match_percent: int | str = ""
            if evidence_supported:
                evidence_match_percent = max(0, min(int(raw_row.get("evidence_match_percent", 0) or 0), 100))
            evidence_label = "Blocked" if promotion_status == "Blocked by contradiction" else "Not scored yet"
            if promotion_status != "Blocked by contradiction" and isinstance(evidence_match_percent, int):
                evidence_label = f"{evidence_match_percent}%"

            opening_hand_observations = int(raw_row.get("opening_hand_observations", 0) or 0)
            private_hand_observations = int(raw_row.get("local_private_hand_observations", 0) or 0)
            manual_confirmation_hits = int(raw_row.get("manual_confirmation_hits", 0) or 0)
            exact_manual_confirmation_hits = int(raw_row.get("exact_manual_confirmation_hits", 0) or 0)
            matched_channels = _channel_rows(evidence_summary.get("matched_channels"))
            contradictory_channels = _channel_rows(evidence_summary.get("contradictory_channels"))
            neutral_channels = _channel_rows(evidence_summary.get("neutral_channels"))
            matched_weight = int(evidence_summary.get("matched_weight", 0) or 0)
            contradicted_weight = int(evidence_summary.get("contradicted_weight", 0) or 0)
            best_variant_label = str(evidence_summary.get("best_variant_label", "") or "").strip()
            best_variant_scope = str(evidence_summary.get("best_variant_scope", "") or "").strip() or "card"
            human_verified = bool(evidence_summary.get("human_verified", False))
            runner_up_gap_raw = raw_row.get("runner_up_gap")
            runner_up_gap = (
                int(runner_up_gap_raw)
                if runner_up_gap_raw not in (None, "")
                else ""
            )
            neutral_summaries = [
                str(channel.get("label", "")).strip()
                for channel in neutral_channels
                if str(channel.get("label", "")).strip()
            ]
            next_actions = _candidate_next_actions(
                promotion_status=promotion_status,
                evidence_supported=evidence_supported,
                matched_channels=matched_channels,
                contradictory_channels=contradictory_channels,
                neutral_channels=neutral_channels,
                manual_confirmation_hits=manual_confirmation_hits,
                exact_manual_confirmation_hits=exact_manual_confirmation_hits,
                runner_up_gap=runner_up_gap,
            )

            entries.append(
                {
                    "grp_id": grp_id,
                    "section": str(raw_row.get("section", "")).strip() or "unknown",
                    "suggested_name": suggested_name,
                    "evidence_match_percent": evidence_match_percent,
                    "evidence_supported": evidence_supported,
                    "evidence_label": evidence_label,
                    "promotion_status": promotion_status,
                    "confirmation_status": confirmation_status,
                    "top_candidate_score": int(raw_row.get("top_candidate_score", top_ranked_score) or 0)
                    if raw_row.get("top_candidate_score", top_ranked_score) not in (None, "")
                    else "",
                    "top_reasons": top_reasons,
                    "confirmation_reasons": confirmation_reasons,
                    "deferred_at": deferred_at,
                    "runner_up_gap": runner_up_gap,
                    "opening_hand_observations": opening_hand_observations,
                    "private_hand_observations": private_hand_observations,
                    "manual_confirmation_hits": manual_confirmation_hits,
                    "exact_manual_confirmation_hits": exact_manual_confirmation_hits,
                    "matched_weight": matched_weight,
                    "contradicted_weight": contradicted_weight,
                    "matched_channels": matched_channels,
                    "contradictory_channels": contradictory_channels,
                    "neutral_channels": neutral_channels,
                    "neutral_channel_labels": neutral_summaries,
                    "best_variant_label": best_variant_label,
                    "best_variant_scope": best_variant_scope,
                    "human_verified": human_verified,
                    "legacy_confidence_percent": raw_row.get("confidence_percent", ""),
                    "next_actions": next_actions,
                }
            )

    entries.sort(key=_candidate_snapshot_sort_key)

    ready_count = sum(1 for entry in entries if entry["promotion_status"] == "Ready for confirmation")
    deferred_count = sum(1 for entry in entries if entry["promotion_status"] == "Deferred")
    review_count = sum(1 for entry in entries if entry["promotion_status"] == "Needs review")
    blocked_count = sum(1 for entry in entries if entry["promotion_status"] == "Blocked by contradiction")
    summary_parts = [f"{len(entries)} suggestion(s) loaded"]
    if ready_count:
        summary_parts.append(f"{ready_count} ready for confirmation")
    if review_count:
        summary_parts.append(f"{review_count} need review")
    if deferred_count:
        summary_parts.append(f"{deferred_count} deferred")
    if blocked_count:
        summary_parts.append(f"{blocked_count} blocked")
    return {
        "summary": " | ".join(summary_parts),
        "entries": entries,
    }


def build_catalog_candidate_item_id(
    entry: dict[str, Any],
    *,
    duplicate_index: int = 0,
) -> str:
    grp_id = str(entry.get("grp_id", "") or "").strip() or "unknown"
    section = str(entry.get("section", "") or "").strip() or "unknown"
    item_id = f"{grp_id}::{section}"
    if duplicate_index > 0:
        item_id = f"{item_id}::{duplicate_index + 1}"
    return item_id


def open_path_in_shell(path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def split_python_command(python_cmd: str) -> list[str]:
    normalized = python_cmd.strip()
    if not normalized:
        return [sys.executable]
    if " " in normalized and not normalized.lower().endswith(".exe"):
        return normalized.split()
    return [normalized]


def build_overview_readiness(
    *,
    project_root: Path,
    script_path: Path,
    player_log_path: Path,
    webhook_url: str,
    sheet_posting_enabled: bool,
    catalog_status_payload: dict,
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    items.append(
        {
            "key": "project_root",
            "title": "Project root",
            "state": "ready" if project_root.exists() else "blocked",
            "detail": "Found" if project_root.exists() else "Folder not found",
            "action_key": "" if project_root.exists() else "session",
            "action_label": "" if project_root.exists() else "Session",
        }
    )
    items.append(
        {
            "key": "script",
            "title": "Filtered script",
            "state": "ready" if script_path.exists() else "blocked",
            "detail": script_path.name if script_path.exists() else "Choose a valid script",
            "action_key": "" if script_path.exists() else "session",
            "action_label": "" if script_path.exists() else "Session",
        }
    )
    items.append(
        {
            "key": "player_log",
            "title": "Player.log",
            "state": "ready" if player_log_path.exists() else "blocked",
            "detail": "Found" if player_log_path.exists() else "Log file missing",
            "action_key": "" if player_log_path.exists() else "session",
            "action_label": "" if player_log_path.exists() else "Session",
        }
    )

    webhook_text = webhook_url.strip()
    if webhook_text:
        webhook_state = "ready"
        webhook_detail = "Configured"
    elif sheet_posting_enabled:
        webhook_state = "warning"
        webhook_detail = "Sheet posting enabled without webhook"
    else:
        webhook_state = "ready"
        webhook_detail = "Local logging only"
    items.append(
        {
            "key": "webhook",
            "title": "Webhook",
            "state": webhook_state,
            "detail": webhook_detail,
            "action_key": "session" if webhook_state == "warning" else "",
            "action_label": "Session" if webhook_state == "warning" else "",
        }
    )

    if not catalog_status_payload:
        catalog_state = "warning"
        catalog_detail = "No refresh status yet"
    elif catalog_status_payload.get("next_restart_required"):
        catalog_state = "warning"
        catalog_detail = "Refresh ready; restart parser next"
    else:
        last_manual = _parse_status_datetime(catalog_status_payload.get("last_successful_manual_refresh_at"))
        stale_after_days = int(catalog_status_payload.get("stale_after_days", 45) or 45)
        if last_manual is None:
            catalog_state = "warning"
            catalog_detail = "Manual refresh has not run yet"
        else:
            local_tz = last_manual.tzinfo or datetime.now().astimezone().tzinfo
            age_days = max((datetime.now(local_tz) - last_manual).days, 0)
            if age_days >= stale_after_days:
                catalog_state = "warning"
                catalog_detail = f"Refresh recommended ({age_days} day(s))"
            else:
                catalog_state = "ready"
                catalog_detail = f"Current ({age_days} day(s) old)"

    items.append(
        {
            "key": "catalog",
            "title": "MTGA card library",
            "state": catalog_state,
            "detail": catalog_detail,
            "action_key": "catalog" if catalog_state == "warning" else "",
            "action_label": "Library" if catalog_state == "warning" else "",
        }
    )
    return items


def build_overview_hero(
    *,
    readiness_items: list[dict[str, str]],
    parser_running: bool,
    status_payload: dict,
) -> dict[str, str]:
    blocked = sum(1 for item in readiness_items if item["state"] == "blocked")
    warnings = sum(1 for item in readiness_items if item["state"] == "warning")
    current_match = str(status_payload.get("current_match_id", "") or "").strip()

    if parser_running:
        return {
            "badge": "Running",
            "tone": "success",
            "headline": "Parser is live and watching MTGA",
            "detail": (
                f"Tracking active match {truncate_text(current_match, max_len=32)}"
                if current_match
                else "Live tracking is active and waiting for new events."
            ),
        }
    if blocked:
        return {
            "badge": "Blocked",
            "tone": "danger",
            "headline": "Session setup needs attention",
            "detail": f"Fix {blocked} blocking item(s) before starting the parser.",
        }
    if warnings:
        return {
            "badge": "Review",
            "tone": "warning",
            "headline": f"▲ {warnings} item(s) should be reviewed before you begin",
            "detail": "You can still start, but the highlighted items are worth checking first.",
        }
    return {
        "badge": "Ready",
        "tone": "accent",
        "headline": "Ready to start the parser",
        "detail": "Core startup checks look healthy for the next session.",
    }


class LauncherApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1120x760")
        self.minsize(940, 620)

        self.proc: subprocess.Popen | None = None
        self.log_queue: queue.Queue[str] = queue.Queue()
        self.settings = load_settings()

        self.project_root_var = tk.StringVar(value=self.settings.get("project_root", DEFAULT_PROJECT_ROOT))
        self.player_log_var = tk.StringVar(value=self.settings.get("player_log", DEFAULT_PLAYER_LOG))
        self.webhook_var = tk.StringVar(value=self.settings.get("webhook_url", ""))
        self.post_raw_events_var = tk.BooleanVar(value=bool(self.settings.get("post_raw_events", False)))
        self.post_gamestate_var = tk.BooleanVar(value=bool(self.settings.get("post_gamestate", False)))
        self.post_game_log_rows_var = tk.BooleanVar(value=bool(self.settings.get("post_game_log_rows", True)))
        self.post_match_log_rows_var = tk.BooleanVar(value=bool(self.settings.get("post_match_log_rows", True)))
        self.sync_tier_buckets_var = tk.BooleanVar(value=bool(self.settings.get("sync_tier_buckets", True)))
        self.script_var = tk.StringVar(value=self.settings.get("script_path", ""))
        self.python_cmd_var = tk.StringVar(value=self.settings.get("python_cmd", f"{sys.executable}"))
        self.mtga_process_var = tk.StringVar(value=self.settings.get("mtga_process_name", DEFAULT_MTGA_PROCESS))
        self.watch_mtga_var = tk.BooleanVar(value=bool(self.settings.get("watch_mtga", True)))
        self.auto_stop_var = tk.BooleanVar(value=bool(self.settings.get("auto_stop_on_close", True)))
        self.status_var = tk.StringVar(value="Idle")
        self.overview_badge_var = tk.StringVar(value="Checking")
        self.overview_headline_var = tk.StringVar(value="Checking launcher readiness")
        self.overview_detail_var = tk.StringVar(value="Launcher status will appear here.")
        self.health_status_var = tk.StringVar(value="No status file yet")
        self.health_last_event_var = tk.StringVar(value="No events seen yet")
        self.health_match_var = tk.StringVar(value="Match n/a | Game n/a | Team n/a")
        self.health_webhook_var = tk.StringVar(value="0 ok / 0 failed | last attempts: n/a | last match: n/a")
        self.health_error_var = tk.StringVar(value="No recent errors recorded")
        self.health_updated_at_var = tk.StringVar(value="n/a")
        self.catalog_refresh_status_var = tk.StringVar(value="No card-catalog refresh status yet")
        self.catalog_last_manual_var = tk.StringVar(value="n/a")
        self.catalog_confirmation_var = tk.StringVar(value="No confirmation suggestions yet")
        self.catalog_review_var = tk.StringVar(value="No inferred review status yet")
        self.catalog_activation_var = tk.StringVar(value="No catalog activation state yet")
        self.catalog_candidate_detail_var = tk.StringVar(value="No confirmation suggestion selected.")
        self.hand_card_var = tk.StringVar(value="")
        self.hand_match_id_var = tk.StringVar(value="")
        self.hand_game_var = tk.StringVar(value="")
        self.hand_date_var = tk.StringVar(value=datetime.now().date().isoformat())
        self.hand_time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        self.hand_opponent_var = tk.StringVar(value="")
        self.hand_note_var = tk.StringVar(value="")
        self.hand_watchlist_status_var = tk.StringVar(value="No watchlist loaded yet")
        self.last_seen_submitted_deck_signature = ""
        self._background_helper_results: queue.Queue[dict[str, Any]] = queue.Queue()
        self._hand_watchlist_refresh_in_progress = False
        self._pending_hand_watchlist_refresh = False
        self._pending_hand_watchlist_signature = ""
        self._catalog_candidate_action_in_progress = False
        self._scroll_tab_canvases: dict[int, tk.Canvas] = {}
        self._tooltip_window: tk.Toplevel | None = None
        self._tooltip_after_id: str | None = None
        self._overview_readiness_vars: dict[str, tuple[tk.StringVar, tk.StringVar]] = {}
        self._overview_readiness_badges: dict[str, tk.Label] = {}
        self._overview_readiness_buttons: dict[str, ttk.Button] = {}
        self._overview_badge_label: tk.Label | None = None
        self._overview_snapshot_vars: dict[str, tk.StringVar] = {}
        self._overview_attention_vars: dict[str, tk.StringVar] = {}
        self._tab_shells: dict[str, ttk.Frame] = {}
        self.catalog_candidate_entries: dict[str, dict[str, object]] = {}
        self.catalog_candidate_tree: ttk.Treeview | None = None
        self.catalog_candidate_detail_text: tk.Text | None = None
        self._catalog_candidate_detail_item_id = ""
        self.catalog_confirm_button: ttk.Button | None = None
        self.catalog_defer_button: ttk.Button | None = None
        self.hand_refresh_watchlist_button: ttk.Button | None = None

        self.mtga_present = False
        self.prompted_for_current_session = False
        self.watcher_enabled = False

        self._configure_styles()
        self._build_ui()
        self.refresh_scripts()
        self.refresh_health_panel()
        self.refresh_hand_confirmation_panel(sync=False)
        self.after(150, self._drain_log_queue)
        self.after(2000, self._refresh_health_loop)
        self.after(2000, self._watch_mtga_loop)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Subheader.TLabel", font=("Segoe UI", 10))
        style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"))
        style.configure("App.TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10, "bold"))
        style.configure("Section.TLabelframe", padding=10)
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 9, "bold"), foreground="#2457a7")
        style.configure("Primary.TButton", padding=(12, 8))
        style.map(
            "Primary.TButton",
            background=[("!disabled", OVERVIEW_COLORS["accent"]), ("pressed", OVERVIEW_COLORS["border"])],
            foreground=[("!disabled", OVERVIEW_COLORS["text"])],
        )

    def _build_ui(self) -> None:
        shell = ttk.Frame(self, padding=(12, 12, 12, 8))
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(1, weight=1)

        header = ttk.Frame(shell)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=APP_NAME, style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Session controls, troubleshooting, and card workflows in one organized operator UI.",
            style="Subheader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.notebook = ttk.Notebook(shell, style="App.TNotebook")
        self.notebook.grid(row=1, column=0, sticky="nsew")

        self._build_overview_tab(self._create_scrollable_tab(self.notebook, "Overview"))
        self._build_session_tab(self._create_scrollable_tab(self.notebook, "Session Setup"))
        self._build_catalog_tab(self._create_scrollable_tab(self.notebook, "MTGA Card Library"))
        self._build_hand_tab(self._create_scrollable_tab(self.notebook, "Hand Tracker"))
        self._build_output_tab(self.notebook)
        self._build_troubleshooting_tab(self._create_scrollable_tab(self.notebook, "Troubleshooting"))

        status_bar = ttk.Frame(shell, padding=(2, 8, 2, 0))
        status_bar.grid(row=2, column=0, sticky="ew")
        ttk.Label(status_bar, text="Status", style="Status.TLabel").pack(side="left")
        ttk.Label(status_bar, textvariable=self.status_var).pack(side="left", padx=(8, 0))

    def _create_scrollable_tab(self, notebook: ttk.Notebook, title: str) -> ttk.Frame:
        tab_shell = ttk.Frame(notebook)
        notebook.add(tab_shell, text=title)
        self._tab_shells[title] = tab_shell

        canvas = tk.Canvas(tab_shell, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(tab_shell, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content = ttk.Frame(canvas, padding=16)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def _sync_window_geometry(_event: object | None = None) -> None:
            width = canvas.winfo_width()
            height = max(content.winfo_reqheight(), canvas.winfo_height())
            if width > 0:
                canvas.itemconfigure(window_id, width=width)
            if height > 0:
                canvas.itemconfigure(window_id, height=height)
            canvas.configure(scrollregion=canvas.bbox("all"))

        content.bind("<Configure>", _sync_window_geometry)
        canvas.bind("<Configure>", _sync_window_geometry)
        self._scroll_tab_canvases[id(content)] = canvas
        return content

    def _enable_scrollwheel_for_tab(self, content: ttk.Frame) -> None:
        canvas = self._scroll_tab_canvases.get(id(content))
        if canvas is None:
            return
        self._bind_scrollwheel_region(content, canvas)

    def _bind_scrollwheel_region(self, widget: tk.Misc, canvas: tk.Canvas) -> None:
        widget.bind(
            "<MouseWheel>",
            lambda event, canvas=canvas: self._handle_tab_mousewheel(canvas, event),
            add="+",
        )
        widget.bind(
            "<Button-4>",
            lambda event, canvas=canvas: self._handle_tab_mousewheel(canvas, event),
            add="+",
        )
        widget.bind(
            "<Button-5>",
            lambda event, canvas=canvas: self._handle_tab_mousewheel(canvas, event),
            add="+",
        )
        for child in widget.winfo_children():
            self._bind_scrollwheel_region(child, canvas)

    def _mousewheel_units(self, event: object) -> int:
        delta = int(getattr(event, "delta", 0) or 0)
        if delta:
            if abs(delta) >= 120:
                return int(-delta / 120)
            return -1 if delta > 0 else 1

        button = getattr(event, "num", None)
        if button == 4:
            return -1
        if button == 5:
            return 1
        return 0

    def _handle_tab_mousewheel(self, canvas: tk.Canvas, event: object) -> str | None:
        widget = getattr(event, "widget", None)
        if isinstance(widget, tk.Text):
            return None

        scroll_units = self._mousewheel_units(event)
        if scroll_units == 0:
            return None

        canvas.yview_scroll(scroll_units, "units")
        return "break"

    def _section_frame(
        self,
        parent: ttk.Frame,
        *,
        title: str,
        expand: bool = False,
    ) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=title, style="Section.TLabelframe")
        frame.pack(fill="both" if expand else "x", expand=expand, pady=(0, 12))
        return frame

    def _add_value_row(
        self,
        parent: ttk.Widget,
        *,
        row_index: int,
        label_text: str,
        value_var: tk.StringVar,
        pady_value: int | tuple[int, int] = 4,
    ) -> None:
        ttk.Label(parent, text=label_text).grid(
            row=row_index,
            column=0,
            sticky="nw",
            padx=8,
            pady=pady_value,
        )
        ttk.Label(parent, textvariable=value_var).grid(
            row=row_index,
            column=1,
            sticky="nw",
            padx=8,
            pady=pady_value,
        )

    def _pack_bar_button(
        self,
        parent: ttk.Widget,
        *,
        text: str,
        command: object,
        padx_value: int | tuple[int, int] = 5,
        width: int = 18,
    ) -> ttk.Button:
        button = ttk.Button(
            parent,
            text=text,
            command=command,
            width=max(width, len(text) + 2),
        )
        button.pack(side="left", padx=padx_value)
        return button

    def _select_tab(self, title: str) -> None:
        tab_shell = self._tab_shells.get(title)
        if tab_shell is not None:
            self.notebook.select(tab_shell)

    def _grid_field_label(
        self,
        parent: ttk.Widget,
        *,
        row_index: int,
        label_text: str,
        tooltip_text: str = "",
        pady_value: int | tuple[int, int] = 6,
    ) -> None:
        label_frame = ttk.Frame(parent)
        label_frame.grid(row=row_index, column=0, sticky="w", padx=8, pady=pady_value)
        ttk.Label(label_frame, text=label_text).pack(side="left")
        if tooltip_text:
            self._tooltip_icon(label_frame, tooltip_text).pack(side="left", padx=(6, 0))

    def _tooltip_icon(self, parent: ttk.Widget, message: str) -> ttk.Label:
        icon = ttk.Label(parent, text="[i]", style="Info.TLabel", cursor="hand2")
        self._bind_tooltip(icon, message)
        return icon

    def _bind_tooltip(self, widget: tk.Misc, message: str) -> None:
        widget.bind(
            "<Enter>",
            lambda _event, widget=widget, message=message: self._schedule_tooltip(widget, message),
            add="+",
        )
        widget.bind("<Leave>", lambda _event: self._hide_tooltip(), add="+")
        widget.bind("<ButtonPress>", lambda _event: self._hide_tooltip(), add="+")

    def _schedule_tooltip(self, widget: tk.Misc, message: str) -> None:
        self._cancel_tooltip_timer()
        self._tooltip_after_id = self.after(250, lambda: self._show_tooltip(widget, message))

    def _cancel_tooltip_timer(self) -> None:
        if self._tooltip_after_id is None:
            return
        self.after_cancel(self._tooltip_after_id)
        self._tooltip_after_id = None

    def _show_tooltip(self, widget: tk.Misc, message: str) -> None:
        self._hide_tooltip()
        tooltip = tk.Toplevel(self)
        tooltip.wm_overrideredirect(True)
        tooltip.attributes("-topmost", True)
        x = widget.winfo_rootx() + widget.winfo_width() + 10
        y = widget.winfo_rooty() + 2
        tooltip.wm_geometry(f"+{x}+{y}")
        tk.Label(
            tooltip,
            text=message,
            bg="#1f2937",
            fg="#f9fafb",
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=6,
            justify="left",
            wraplength=280,
        ).pack()
        self._tooltip_window = tooltip
        self._tooltip_after_id = None

    def _hide_tooltip(self) -> None:
        self._cancel_tooltip_timer()
        if self._tooltip_window is not None:
            self._tooltip_window.destroy()
            self._tooltip_window = None

    def _option_row(
        self,
        parent: ttk.Widget,
        *,
        row_index: int,
        variable: tk.BooleanVar,
        label_text: str,
        tooltip_text: str = "",
    ) -> None:
        row_frame = ttk.Frame(parent)
        row_frame.grid(row=row_index, column=0, columnspan=4, sticky="w", padx=8, pady=6)
        ttk.Checkbutton(row_frame, text=label_text, variable=variable).pack(side="left")
        if tooltip_text:
            self._tooltip_icon(row_frame, tooltip_text).pack(side="left", padx=(6, 0))

    def _build_overview_tab(self, parent: ttk.Frame) -> None:
        shell = tk.Frame(parent, bg=OVERVIEW_COLORS["bg"], padx=8, pady=8)
        shell.pack(fill="both", expand=True)
        shell.grid_columnconfigure(0, weight=3)
        shell.grid_columnconfigure(1, weight=2)
        shell.grid_rowconfigure(1, weight=1)
        shell.grid_rowconfigure(2, weight=1)

        hero_card = self._overview_card(shell, row=0, column=0, columnspan=2, min_height=208)
        hero_header = tk.Frame(hero_card, bg=OVERVIEW_COLORS["card"])
        hero_header.pack(fill="x")
        tk.Label(
            hero_header,
            text="CONTROL ROOM",
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        self._overview_badge_label = tk.Label(
            hero_header,
            textvariable=self.overview_badge_var,
            bg=OVERVIEW_COLORS["accent"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=5,
        )
        self._overview_badge_label.pack(side="right")

        tk.Label(
            hero_card,
            textvariable=self.overview_headline_var,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 22, "bold"),
            anchor="w",
            justify="left",
            wraplength=860,
        ).pack(fill="x", pady=(18, 10))
        tk.Label(
            hero_card,
            textvariable=self.overview_detail_var,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 11),
            anchor="w",
            justify="left",
            wraplength=860,
        ).pack(fill="x")

        hero_actions = tk.Frame(hero_card, bg=OVERVIEW_COLORS["card"])
        hero_actions.pack(fill="x", pady=(20, 0))
        ttk.Button(
            hero_actions,
            text="Start Parser",
            style="Primary.TButton",
            command=self.start_script,
            width=max(18, len("Start Parser") + 2),
        ).pack(
            side="left",
            padx=(0, 10),
        )
        ttk.Button(
            hero_actions,
            text="Stop Parser",
            command=self.stop_script,
            width=max(18, len("Stop Parser") + 2),
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            hero_actions,
            text="Open Output Folder",
            command=self.open_output_folder,
            width=max(18, len("Open Output Folder") + 2),
        ).pack(side="left")

        readiness_card = self._overview_card(shell, row=1, column=0, min_height=228)
        readiness_rows = tk.Frame(readiness_card, bg=OVERVIEW_COLORS["card"])
        readiness_rows.pack(fill="both", expand=True)
        readiness_specs = [
            ("project_root", "Project root"),
            ("script", "Filtered script"),
            ("player_log", "Player.log"),
            ("webhook", "Webhook"),
            ("catalog", "MTGA card library"),
        ]
        for row_index, (key, title) in enumerate(readiness_specs):
            self._overview_readiness_row(readiness_rows, row=row_index, key=key, title=title)

        session_card = self._overview_card(shell, row=1, column=1, min_height=228)
        self._overview_card_header(
            session_card,
            title="Current session",
            subtitle="Live parser status and the latest runtime signals from the MTGA event stream.",
        )
        session_rows = tk.Frame(session_card, bg=OVERVIEW_COLORS["card"])
        session_rows.pack(fill="both", expand=True, pady=(8, 0))
        self._overview_snapshot_row(session_rows, row=0, key="status", title="Parser status")
        self._overview_snapshot_row(session_rows, row=1, key="match", title="Current match")
        self._overview_snapshot_row(session_rows, row=2, key="event", title="Last event")
        self._overview_snapshot_row(session_rows, row=3, key="webhook", title="Webhook")
        self._overview_snapshot_row(session_rows, row=4, key="error", title="Last error")

        attention_card = self._overview_card(shell, row=2, column=0, min_height=188)
        self._overview_card_header(
            attention_card,
            title="Attention and follow-up",
            subtitle="Quietly surfaces the things most likely to need your attention next.",
        )
        attention_rows = tk.Frame(attention_card, bg=OVERVIEW_COLORS["card"])
        attention_rows.pack(fill="both", expand=True, pady=(8, 0))
        self._overview_attention_row(attention_rows, row=0, key="refresh", title="Scryfall refresh")
        self._overview_attention_row(attention_rows, row=1, key="review", title="Candidate review")
        self._overview_attention_row(attention_rows, row=2, key="activation", title="Activation")
        self._overview_attention_row(
            attention_rows,
            row=3,
            key="last_manual",
            title="Last refresh from Scryfall",
        )

        quick_actions = self._overview_card(shell, row=2, column=1, min_height=188)
        self._overview_card_header(
            quick_actions,
            title="Quick actions",
            subtitle="Fast access to the things you are most likely to need during live play or troubleshooting.",
        )
        actions_grid = tk.Frame(quick_actions, bg=OVERVIEW_COLORS["card"])
        actions_grid.pack(fill="both", expand=True, pady=(14, 0))
        actions_grid.grid_columnconfigure(0, weight=1)
        actions_grid.grid_columnconfigure(1, weight=1)
        quick_buttons = [
            ("Refresh health", self.refresh_health_panel),
            ("Open runtime log", self.open_runtime_log),
            ("Open status file", self.open_status_file),
            ("Refresh MTGA card library", self.run_card_catalog_refresh_from_ui),
            ("Open inferred review", self.open_inferred_review_report),
            ("Open failed posts", self.open_failed_posts_folder),
        ]
        for index, (label, command) in enumerate(quick_buttons):
            ttk.Button(actions_grid, text=label, command=command, width=max(18, len(label) + 2)).grid(
                row=index // 2,
                column=index % 2,
                sticky="ew",
                padx=6,
                pady=6,
            )

        self._enable_scrollwheel_for_tab(parent)

    def _overview_card(
        self,
        parent: tk.Widget,
        *,
        row: int,
        column: int,
        columnspan: int = 1,
        min_height: int = 180,
    ) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=OVERVIEW_COLORS["card"],
            highlightbackground=OVERVIEW_COLORS["border"],
            highlightthickness=1,
            bd=0,
            padx=20,
            pady=18,
        )
        card.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=8, pady=8)
        card.grid_propagate(False)
        card.configure(height=min_height)
        return card

    def _overview_card_header(self, parent: tk.Frame, *, title: str, subtitle: str) -> None:
        tk.Label(
            parent,
            text=title,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            parent,
            text=subtitle,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
            wraplength=420,
        ).pack(fill="x", pady=(6, 0))

    def _overview_readiness_row(self, parent: tk.Frame, *, row: int, key: str, title: str) -> None:
        detail_var = tk.StringVar(value="Checking")
        state_var = tk.StringVar(value="...")
        row_frame = tk.Frame(parent, bg=OVERVIEW_COLORS["card"])
        row_frame.grid(row=row, column=0, sticky="ew", pady=6)
        row_frame.grid_columnconfigure(1, weight=1)
        row_frame.grid_columnconfigure(2, weight=0)

        badge = tk.Label(
            row_frame,
            textvariable=state_var,
            width=9,
            bg=OVERVIEW_COLORS["accent"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 9, "bold"),
            padx=6,
            pady=4,
        )
        badge.grid(row=0, column=0, sticky="w", padx=(0, 12))
        tk.Label(
            row_frame,
            text=title,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).grid(row=0, column=1, sticky="w")
        tk.Label(
            row_frame,
            textvariable=detail_var,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 10),
            anchor="w",
        ).grid(row=1, column=1, sticky="w", pady=(2, 0))
        action_button = ttk.Button(row_frame, text="", width=10)
        action_button.grid(row=0, column=2, rowspan=2, sticky="e")
        action_button.grid_remove()
        self._overview_readiness_vars[key] = (state_var, detail_var)
        self._overview_readiness_badges[key] = badge
        self._overview_readiness_buttons[key] = action_button

    def _overview_snapshot_row(self, parent: tk.Frame, *, row: int, key: str, title: str) -> None:
        value_var = tk.StringVar(value="n/a")
        row_frame = tk.Frame(parent, bg=OVERVIEW_COLORS["card"])
        row_frame.grid(row=row, column=0, sticky="ew", pady=6)
        tk.Label(
            row_frame,
            text=title,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            row_frame,
            textvariable=value_var,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 11),
            anchor="w",
            justify="left",
            wraplength=380,
        ).pack(anchor="w", pady=(2, 0))
        self._overview_snapshot_vars[key] = value_var

    def _overview_attention_row(self, parent: tk.Frame, *, row: int, key: str, title: str) -> None:
        value_var = tk.StringVar(value="n/a")
        row_frame = tk.Frame(parent, bg=OVERVIEW_COLORS["card"])
        row_frame.grid(row=row, column=0, sticky="ew", pady=6)
        tk.Label(
            row_frame,
            text=title,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["muted"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            row_frame,
            textvariable=value_var,
            bg=OVERVIEW_COLORS["card"],
            fg=OVERVIEW_COLORS["text"],
            font=("Segoe UI", 11),
            anchor="w",
            justify="left",
            wraplength=420,
        ).pack(anchor="w", pady=(2, 0))
        self._overview_attention_vars[key] = value_var

    def _overview_tone_color(self, tone: str) -> str:
        return {
            "ready": OVERVIEW_COLORS["success"],
            "success": OVERVIEW_COLORS["success"],
            "warning": OVERVIEW_COLORS["warning"],
            "blocked": OVERVIEW_COLORS["danger"],
            "danger": OVERVIEW_COLORS["danger"],
            "accent": OVERVIEW_COLORS["accent"],
        }.get(tone, OVERVIEW_COLORS["accent"])

    def _refresh_overview_panel(self, status_payload: dict, catalog_status_payload: dict) -> None:
        readiness_items = build_overview_readiness(
            project_root=self._project_root(),
            script_path=Path(self.script_var.get().strip()) if self.script_var.get().strip() else Path(""),
            player_log_path=Path(self.player_log_var.get().strip()) if self.player_log_var.get().strip() else Path(""),
            webhook_url=self.webhook_var.get(),
            sheet_posting_enabled=self._sheet_posting_enabled(),
            catalog_status_payload=catalog_status_payload,
        )

        for item in readiness_items:
            state_var, detail_var = self._overview_readiness_vars[item["key"]]
            badge = self._overview_readiness_badges[item["key"]]
            action_button = self._overview_readiness_buttons[item["key"]]
            state_var.set(item["state"].upper())
            detail_var.set(item["detail"])
            badge.configure(bg=self._overview_tone_color(item["state"]))
            self._configure_overview_readiness_action(
                action_button,
                action_key=str(item.get("action_key", "") or ""),
                action_label=str(item.get("action_label", "") or ""),
            )

        parser_running = self.proc is not None and self.proc.poll() is None
        hero = build_overview_hero(
            readiness_items=readiness_items,
            parser_running=parser_running,
            status_payload=status_payload,
        )
        self.overview_badge_var.set(hero["badge"])
        self.overview_headline_var.set(hero["headline"])
        self.overview_detail_var.set(hero["detail"])
        if self._overview_badge_label is not None:
            self._overview_badge_label.configure(bg=self._overview_tone_color(hero["tone"]))

        self._overview_snapshot_vars["status"].set(self.health_status_var.get())
        self._overview_snapshot_vars["match"].set(self.health_match_var.get())
        self._overview_snapshot_vars["event"].set(self.health_last_event_var.get())
        self._overview_snapshot_vars["webhook"].set(self.health_webhook_var.get())
        self._overview_snapshot_vars["error"].set(self.health_error_var.get())

        self._overview_attention_vars["refresh"].set(self.catalog_refresh_status_var.get())
        self._overview_attention_vars["review"].set(self.catalog_confirmation_var.get())
        self._overview_attention_vars["activation"].set(self.catalog_activation_var.get())
        self._overview_attention_vars["last_manual"].set(self.catalog_last_manual_var.get())

    def _configure_overview_readiness_action(
        self,
        button: ttk.Button,
        *,
        action_key: str,
        action_label: str,
    ) -> None:
        action_map = {
            "session": lambda: self._select_tab("Session Setup"),
            "catalog": lambda: self._select_tab("MTGA Card Library"),
        }
        command = action_map.get(action_key)
        if not action_label or command is None:
            button.grid_remove()
            return
        button.configure(text=action_label, command=command, width=max(10, len(action_label) + 2))
        button.grid()

    def _build_session_tab(self, parent: ttk.Frame) -> None:
        action_frame = self._section_frame(parent, title="Quick start")
        ttk.Label(
            action_frame,
            text="Start and stop the selected parser quickly, then adjust the session inputs below if needed.",
        ).pack(anchor="w", padx=8, pady=(8, 6))
        button_bar = ttk.Frame(action_frame)
        button_bar.pack(fill="x", padx=8, pady=(0, 8))
        self._pack_bar_button(button_bar, text="Start", command=self.start_script, padx_value=(0, 6), width=16)
        self._pack_bar_button(button_bar, text="Stop", command=self.stop_script, width=16)
        self._pack_bar_button(button_bar, text="Open output folder", command=self.open_output_folder)
        self._pack_bar_button(button_bar, text="Save settings", command=self.persist_settings)

        project_frame = self._section_frame(parent, title="Project and script")
        project_frame.columnconfigure(1, weight=1)
        standard_entry_width = 72
        action_button_width = 16

        self._grid_field_label(project_frame, row_index=0, label_text="Project root", pady_value=(8, 6))
        ttk.Entry(project_frame, textvariable=self.project_root_var, width=standard_entry_width).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8,
            pady=(8, 6),
        )
        ttk.Button(project_frame, text="Browse", command=self.browse_project_root, width=action_button_width).grid(
            row=0,
            column=2,
            padx=8,
            pady=(8, 6),
        )
        ttk.Button(
            project_frame,
            text="Refresh scripts",
            command=self.refresh_scripts,
            width=action_button_width,
        ).grid(
            row=0,
            column=3,
            padx=8,
            pady=(8, 6),
        )

        self._grid_field_label(project_frame, row_index=1, label_text="Filtered script")
        self.script_combo = ttk.Combobox(
            project_frame,
            textvariable=self.script_var,
            width=standard_entry_width,
            state="readonly",
        )
        self.script_combo.grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=6)
        ttk.Button(
            project_frame,
            text="Browse file",
            command=self.browse_script_file,
            width=action_button_width,
        ).grid(
            row=1,
            column=3,
            padx=8,
            pady=6,
        )

        self._grid_field_label(
            project_frame,
            row_index=2,
            label_text="Python command",
            tooltip_text="Example: py -3.13 or a full python.exe path.",
        )
        ttk.Entry(project_frame, textvariable=self.python_cmd_var, width=standard_entry_width).grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=8,
            pady=6,
        )

        runtime_frame = self._section_frame(parent, title="Runtime inputs")
        runtime_frame.columnconfigure(1, weight=1)

        self._grid_field_label(runtime_frame, row_index=0, label_text="Player.log path", pady_value=(8, 6))
        ttk.Entry(runtime_frame, textvariable=self.player_log_var, width=standard_entry_width).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8,
            pady=(8, 6),
        )
        ttk.Button(runtime_frame, text="Browse", command=self.browse_player_log, width=action_button_width).grid(
            row=0,
            column=2,
            padx=8,
            pady=(8, 6),
        )

        self._grid_field_label(runtime_frame, row_index=1, label_text="Apps Script webhook")
        ttk.Entry(runtime_frame, textvariable=self.webhook_var, width=standard_entry_width).grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=8,
            pady=6,
        )
        ttk.Button(
            runtime_frame,
            text="Clear",
            command=lambda: self.webhook_var.set(""),
            width=action_button_width,
        ).grid(
            row=1,
            column=3,
            padx=8,
            pady=6,
        )

        self._grid_field_label(runtime_frame, row_index=2, label_text="MTGA process name")
        ttk.Entry(runtime_frame, textvariable=self.mtga_process_var, width=standard_entry_width).grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=8,
            pady=6,
        )
        ttk.Checkbutton(
            runtime_frame,
            text="Watch for MTGA launch and prompt to start parser",
            variable=self.watch_mtga_var,
        ).grid(row=3, column=1, columnspan=3, sticky="w", padx=8, pady=(0, 6))
        ttk.Checkbutton(
            runtime_frame,
            text="Auto-stop parser when MTGA closes",
            variable=self.auto_stop_var,
        ).grid(row=4, column=1, columnspan=3, sticky="w", padx=8, pady=(0, 8))

        posting_frame = self._section_frame(parent, title="Sheet posting and startup options")
        self._option_row(
            posting_frame,
            row_index=0,
            variable=self.post_raw_events_var,
            label_text="Post raw archive rows to Sheets",
            tooltip_text="Leave this off unless you want the raw debug/archive rows in Sheets.",
        )
        self._option_row(
            posting_frame,
            row_index=1,
            variable=self.post_gamestate_var,
            label_text="Post GameState rows to Sheets",
            tooltip_text="Use this when you want turn-by-turn GameState rows without enabling the raw archive rows.",
        )
        self._option_row(
            posting_frame,
            row_index=2,
            variable=self.post_game_log_rows_var,
            label_text="Post Game Log rows to Sheets",
            tooltip_text="Enable this for one row per game in the Game Log tab.",
        )
        self._option_row(
            posting_frame,
            row_index=3,
            variable=self.post_match_log_rows_var,
            label_text="Post Match Log rows to Sheets",
            tooltip_text="Enable this for one row per match in the Match Log tab.",
        )
        self._option_row(
            posting_frame,
            row_index=4,
            variable=self.sync_tier_buckets_var,
            label_text="Refresh tier buckets from web sources at startup",
            tooltip_text="This updates the Helper Table source data before live match parsing begins.",
        )
        self._enable_scrollwheel_for_tab(parent)

    def _build_troubleshooting_tab(self, parent: ttk.Frame) -> None:
        health_frame = self._section_frame(parent, title="Runtime health", expand=True)
        health_frame.columnconfigure(1, weight=1)
        for health_row, (label_text, value_var, pady_value) in enumerate(
            (
                ("Parser status", self.health_status_var, (8, 4)),
                ("Last event", self.health_last_event_var, 4),
                ("Current match", self.health_match_var, 4),
                ("Webhook", self.health_webhook_var, 4),
                ("Last error", self.health_error_var, 4),
                ("Updated", self.health_updated_at_var, (4, 8)),
            )
        ):
            self._add_value_row(
                health_frame,
                row_index=health_row,
                label_text=label_text,
                value_var=value_var,
                pady_value=pady_value,
            )

        tools_frame = self._section_frame(parent, title="Troubleshooting files", expand=True)
        ttk.Label(
            tools_frame,
            text="Open the current runtime artifacts directly when the parser or webhook path needs inspection.",
        ).pack(anchor="w", padx=8, pady=(8, 6))
        troubleshooting_bar = ttk.Frame(tools_frame)
        troubleshooting_bar.pack(fill="x", padx=8, pady=(0, 8))
        self._pack_bar_button(
            troubleshooting_bar,
            text="Refresh health",
            command=self.refresh_health_panel,
            padx_value=(0, 5),
        )
        self._pack_bar_button(troubleshooting_bar, text="Open status file", command=self.open_status_file)
        self._pack_bar_button(troubleshooting_bar, text="Open runtime log", command=self.open_runtime_log)
        self._pack_bar_button(
            troubleshooting_bar,
            text="Open failed posts",
            command=self.open_failed_posts_folder,
        )
        self._pack_bar_button(
            troubleshooting_bar,
            text="Open bad events",
            command=self.open_bad_events_folder,
        )
        self._enable_scrollwheel_for_tab(parent)

    def _build_catalog_tab(self, parent: ttk.Frame) -> None:
        catalog_frame = self._section_frame(parent, title="MTGA card library status")
        catalog_frame.columnconfigure(1, weight=1)
        for catalog_row, (label_text, value_var, pady_value) in enumerate(
            (
                ("Refresh status", self.catalog_refresh_status_var, (8, 4)),
                ("Last refresh from Scryfall", self.catalog_last_manual_var, 4),
                ("Confirmation suggestions", self.catalog_confirmation_var, 4),
                ("Inferred review", self.catalog_review_var, 4),
                ("Activation", self.catalog_activation_var, 4),
            )
        ):
            self._add_value_row(
                catalog_frame,
                row_index=catalog_row,
                label_text=label_text,
                value_var=value_var,
                pady_value=pady_value,
            )

        catalog_bar = ttk.Frame(catalog_frame)
        catalog_bar.grid(row=5, column=0, columnspan=2, sticky="w", padx=8, pady=(10, 8))
        self._pack_bar_button(
            catalog_bar,
            text="Refresh MTGA card library",
            command=self.run_card_catalog_refresh_from_ui,
            padx_value=(0, 5),
        )
        self._pack_bar_button(
            catalog_bar,
            text="Open refresh status",
            command=self.open_card_catalog_refresh_status,
        )
        self._pack_bar_button(
            catalog_bar,
            text="Open inferred review",
            command=self.open_inferred_review_report,
        )

        review_frame = self._section_frame(parent, title="Confirmation review queue", expand=True)
        ttk.Label(
            review_frame,
            text=(
                "Review the current parser suggestions here. Confirm accepts the suggested card identity into the "
                "grpId override file. Defer keeps the suggestion visible but marks it as intentionally postponed."
            ),
            wraplength=920,
            justify="left",
        ).pack(anchor="w", padx=8, pady=(8, 6))

        queue_frame = ttk.Frame(review_frame)
        queue_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        queue_frame.columnconfigure(0, weight=1)
        queue_frame.rowconfigure(0, weight=1)

        self.catalog_candidate_tree = ttk.Treeview(
            queue_frame,
            columns=("grp_id", "name", "evidence", "state", "section"),
            show="headings",
            height=9,
        )
        self.catalog_candidate_tree.heading("grp_id", text="grpId")
        self.catalog_candidate_tree.heading("name", text="Suggested card")
        self.catalog_candidate_tree.heading("evidence", text="Evidence Match")
        self.catalog_candidate_tree.heading("state", text="Promotion Status")
        self.catalog_candidate_tree.heading("section", text="Section")
        self.catalog_candidate_tree.column("grp_id", width=88, anchor="center", stretch=False)
        self.catalog_candidate_tree.column("name", width=360, anchor="w")
        self.catalog_candidate_tree.column("evidence", width=120, anchor="center", stretch=False)
        self.catalog_candidate_tree.column("state", width=170, anchor="center", stretch=False)
        self.catalog_candidate_tree.column("section", width=110, anchor="center", stretch=False)
        self.catalog_candidate_tree.grid(row=0, column=0, sticky="nsew")
        self.catalog_candidate_tree.bind("<<TreeviewSelect>>", self._on_catalog_candidate_selected, add="+")

        review_scroll = ttk.Scrollbar(
            queue_frame,
            orient="vertical",
            command=self.catalog_candidate_tree.yview,
        )
        review_scroll.grid(row=0, column=1, sticky="ns")
        self.catalog_candidate_tree.configure(yscrollcommand=review_scroll.set)

        detail_frame = ttk.Frame(review_frame)
        detail_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        detail_frame.columnconfigure(0, weight=1)
        detail_frame.rowconfigure(1, weight=1)
        ttk.Label(detail_frame, text="Selected suggestion details").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.catalog_candidate_detail_text = tk.Text(detail_frame, wrap="word", height=9)
        self.catalog_candidate_detail_text.grid(row=1, column=0, sticky="nsew")
        detail_scroll = ttk.Scrollbar(
            detail_frame,
            orient="vertical",
            command=self.catalog_candidate_detail_text.yview,
        )
        detail_scroll.grid(row=1, column=1, sticky="ns")
        self.catalog_candidate_detail_text.configure(yscrollcommand=detail_scroll.set)
        self._set_catalog_candidate_detail("No confirmation suggestion selected.")

        review_bar = ttk.Frame(review_frame)
        review_bar.pack(fill="x", padx=8, pady=(0, 8))
        self.catalog_confirm_button = self._pack_bar_button(
            review_bar,
            text="Confirm selected",
            command=self.confirm_selected_candidate_from_ui,
            padx_value=(0, 5),
        )
        self.catalog_defer_button = self._pack_bar_button(
            review_bar,
            text="Defer selected",
            command=self.defer_selected_candidate_from_ui,
        )
        self._pack_bar_button(
            review_bar,
            text="Open candidate report",
            command=self.open_candidate_report,
        )
        self._enable_scrollwheel_for_tab(parent)

    def _set_catalog_candidate_detail(
        self,
        text: str,
        *,
        selected_item_id: str = "",
        preserve_view: bool = False,
    ) -> None:
        if self.catalog_candidate_detail_text is None:
            return
        normalized_text = text.strip() or "No confirmation suggestion selected."
        current_text = self.catalog_candidate_detail_text.get("1.0", "end-1c")
        current_view = self.catalog_candidate_detail_text.yview()
        if preserve_view and current_text == normalized_text:
            self._catalog_candidate_detail_item_id = selected_item_id
            return

        self.catalog_candidate_detail_text.configure(state="normal")
        self.catalog_candidate_detail_text.delete("1.0", tk.END)
        self.catalog_candidate_detail_text.insert("1.0", normalized_text)
        self.catalog_candidate_detail_text.configure(state="disabled")

        if preserve_view and current_view:
            self.catalog_candidate_detail_text.yview_moveto(float(current_view[0]))
        else:
            self.catalog_candidate_detail_text.yview_moveto(0.0)
        self._catalog_candidate_detail_item_id = selected_item_id

    def _selected_catalog_candidate_item_id(self) -> str:
        if self.catalog_candidate_tree is None:
            return ""
        selection = self.catalog_candidate_tree.selection()
        if not selection:
            return ""
        return str(selection[0])

    def _selected_catalog_candidate_entry(self) -> dict[str, Any] | None:
        item_id = self._selected_catalog_candidate_item_id()
        if not item_id:
            return None
        return self.catalog_candidate_entries.get(item_id)

    def _catalog_candidate_detail_text_for_entry(self, entry: dict[str, Any]) -> str:
        top_reasons = [f"- {reason}" for reason in entry.get("top_reasons", [])]
        confirmation_reasons = [f"- {reason}" for reason in entry.get("confirmation_reasons", [])]
        matched_channels = [
            f"- {channel.get('label', '')} ({channel.get('weight', 0)}): {channel.get('detail', '')}"
            for channel in entry.get("matched_channels", [])
        ]
        contradictory_channels = [
            f"- {channel.get('label', '')} ({channel.get('weight', 0)}): {channel.get('detail', '')}"
            for channel in entry.get("contradictory_channels", [])
        ]
        neutral_channels = [
            f"- {channel.get('label', '')}: {channel.get('detail', '')}"
            for channel in entry.get("neutral_channels", [])
        ]
        next_actions = [f"- {reason}" for reason in entry.get("next_actions", [])]
        top_candidate_score = entry.get("top_candidate_score", "")
        runner_up_gap = entry.get("runner_up_gap", "")
        evidence_label = entry.get("evidence_label", "Not scored yet")
        best_variant_scope = str(entry.get("best_variant_scope", "") or "").strip()
        best_variant_label = str(entry.get("best_variant_label", "") or "").strip()
        lines = [
            f"grpId: {entry.get('grp_id')}",
            f"Suggested card: {entry.get('suggested_name', '')}",
            f"Evidence Match: {evidence_label}",
            f"Section: {entry.get('section', '')}",
            "",
            "Evidence Match",
            f"- Promotion status: {entry.get('promotion_status', '')}",
            f"- Confirmation status code: {entry.get('confirmation_status', '')}",
            f"- Observed weighted support: {entry.get('matched_weight', 0)}",
            f"- Observed weighted contradiction: {entry.get('contradicted_weight', 0)}",
            (
                "- Top candidate score: "
                f"{top_candidate_score if top_candidate_score not in ('', None) else 'Not available yet'}"
            ),
            f"- Runner-up gap: {runner_up_gap if runner_up_gap not in ('', None) else 'n/a'}",
            f"- Opening hand observations: {entry.get('opening_hand_observations', 0)}",
            f"- Private hand observations: {entry.get('private_hand_observations', 0)}",
            f"- Manual hand confirmations: {entry.get('manual_confirmation_hits', 0)}",
            f"- Exact manual name confirmations: {entry.get('exact_manual_confirmation_hits', 0)}",
        ]
        if entry.get("human_verified"):
            lines.append("- Human verified: yes")
        if best_variant_label:
            prefix = "Best face match" if best_variant_scope == "face" else "Best card-level match"
            lines.append(f"- {prefix}: {best_variant_label}")
        legacy_confidence = entry.get("legacy_confidence_percent", "")
        if entry.get("evidence_supported") is False and legacy_confidence not in ("", None):
            lines.append(f"- Legacy heuristic score in older report: {legacy_confidence}%")
        deferred_at = str(entry.get("deferred_at", "") or "").strip()
        if deferred_at:
            lines.append(f"Deferred at: {deferred_at}")
        if matched_channels:
            lines.extend(["", "Matched Channels", *matched_channels])
        else:
            lines.extend(["", "Matched Channels", "- No direct evidence channels matched this candidate yet."])
        if contradictory_channels:
            lines.extend(["", "Contradictions", *contradictory_channels])
        else:
            lines.extend(["", "Contradictions", "- No direct contradictions are currently recorded."])
        lines.extend(["", "Promotion Decision"])
        if neutral_channels:
            lines.extend(["- Neutral / not observed yet:", *neutral_channels])
        if next_actions:
            lines.extend(["- Recommended next actions:", *next_actions])
        if top_reasons:
            lines.extend(["- Top candidate reasons:", *top_reasons])
        if confirmation_reasons:
            lines.extend(["- Confirmation policy reasons:", *confirmation_reasons])
        return "\n".join(lines)

    def _on_catalog_candidate_selected(self, _event: object | None = None) -> None:
        item_id = self._selected_catalog_candidate_item_id()
        entry = self._selected_catalog_candidate_entry()
        if entry is None:
            self._set_catalog_candidate_detail("No confirmation suggestion selected.", selected_item_id="")
            return
        self._set_catalog_candidate_detail(
            self._catalog_candidate_detail_text_for_entry(entry),
            selected_item_id=item_id,
            preserve_view=item_id == self._catalog_candidate_detail_item_id,
        )

    def refresh_card_confirmation_panel(self) -> None:
        project_root = self._project_root()
        report_payload = load_candidate_report(project_root)
        override_payload = load_grp_id_override_payload(project_root)
        snapshot = build_candidate_confirmation_snapshot(report_payload, override_payload)
        self.catalog_confirmation_var.set(snapshot["summary"])

        if self.catalog_candidate_tree is None:
            return

        prior_selection = self.catalog_candidate_tree.selection()
        prior_item_id = prior_selection[0] if prior_selection else ""
        self.catalog_candidate_entries = {}
        for item_id in self.catalog_candidate_tree.get_children():
            self.catalog_candidate_tree.delete(item_id)

        entries = list(snapshot["entries"])
        duplicate_counts: dict[str, int] = {}
        for entry in entries:
            base_item_id = build_catalog_candidate_item_id(entry)
            duplicate_index = duplicate_counts.get(base_item_id, 0)
            duplicate_counts[base_item_id] = duplicate_index + 1
            item_id = build_catalog_candidate_item_id(entry, duplicate_index=duplicate_index)
            self.catalog_candidate_entries[item_id] = entry
            self.catalog_candidate_tree.insert(
                "",
                "end",
                iid=item_id,
                values=(
                    entry["grp_id"],
                    entry["suggested_name"],
                    entry["evidence_label"],
                    entry["promotion_status"],
                    entry["section"],
                ),
            )

        next_selection = ""
        if prior_item_id and prior_item_id in self.catalog_candidate_entries:
            next_selection = prior_item_id
        elif self.catalog_candidate_entries:
            next_selection = next(iter(self.catalog_candidate_entries), "")

        if next_selection:
            self.catalog_candidate_tree.selection_set(next_selection)
            self.catalog_candidate_tree.focus(next_selection)
        self._on_catalog_candidate_selected()

    def confirm_selected_candidate_from_ui(self) -> None:
        entry = self._selected_catalog_candidate_entry()
        if entry is None:
            messagebox.showinfo(APP_NAME, "Choose a candidate suggestion first.")
            return
        if str(entry.get("promotion_status", "")).strip() == "Blocked by contradiction":
            messagebox.showerror(APP_NAME, "This suggestion is blocked and cannot be confirmed from the launcher.")
            return

        grp_id = int(entry["grp_id"])
        self._start_catalog_candidate_action(
            action="confirm",
            grp_id=grp_id,
            suggested_name=str(entry.get("suggested_name", "") or "").strip(),
            evidence_label=str(entry.get("evidence_label", "") or "").strip(),
        )

    def defer_selected_candidate_from_ui(self) -> None:
        entry = self._selected_catalog_candidate_entry()
        if entry is None:
            messagebox.showinfo(APP_NAME, "Choose a candidate suggestion first.")
            return

        grp_id = int(entry["grp_id"])
        self._start_catalog_candidate_action(
            action="defer",
            grp_id=grp_id,
            suggested_name=str(entry.get("suggested_name", "") or "").strip(),
            evidence_label=str(entry.get("evidence_label", "") or "").strip(),
        )

    def _build_hand_tab(self, parent: ttk.Frame) -> None:
        hand_frame = self._section_frame(parent, title="Hand confirmation tracker")
        hand_frame.columnconfigure(1, weight=1)
        hand_frame.columnconfigure(3, weight=1)

        ttk.Label(hand_frame, text="Watchlist card").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        self.hand_card_combo = ttk.Combobox(hand_frame, textvariable=self.hand_card_var, width=42)
        self.hand_card_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=(8, 4))
        ttk.Label(hand_frame, text="Match ID hint").grid(row=0, column=2, sticky="w", padx=8, pady=(8, 4))
        ttk.Entry(hand_frame, textvariable=self.hand_match_id_var, width=42).grid(
            row=0,
            column=3,
            sticky="ew",
            padx=8,
            pady=(8, 4),
        )

        ttk.Label(hand_frame, text="Game #").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(hand_frame, textvariable=self.hand_game_var, width=12).grid(
            row=1,
            column=1,
            sticky="w",
            padx=8,
            pady=4,
        )
        ttk.Label(hand_frame, text="Match date").grid(row=1, column=2, sticky="w", padx=8, pady=4)
        ttk.Entry(hand_frame, textvariable=self.hand_date_var, width=16).grid(
            row=1,
            column=3,
            sticky="w",
            padx=8,
            pady=4,
        )

        ttk.Label(hand_frame, text="Match time").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(hand_frame, textvariable=self.hand_time_var, width=16).grid(
            row=2,
            column=1,
            sticky="w",
            padx=8,
            pady=4,
        )
        ttk.Label(hand_frame, text="Opponent archetype").grid(row=2, column=2, sticky="w", padx=8, pady=4)
        ttk.Entry(hand_frame, textvariable=self.hand_opponent_var, width=42).grid(
            row=2,
            column=3,
            sticky="ew",
            padx=8,
            pady=4,
        )

        ttk.Label(hand_frame, text="Note").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(hand_frame, textvariable=self.hand_note_var, width=90).grid(
            row=3,
            column=1,
            columnspan=3,
            sticky="ew",
            padx=8,
            pady=4,
        )

        ttk.Label(hand_frame, text="Tracker status").grid(row=4, column=0, sticky="w", padx=8, pady=(4, 8))
        ttk.Label(hand_frame, textvariable=self.hand_watchlist_status_var).grid(
            row=4,
            column=1,
            columnspan=3,
            sticky="w",
            padx=8,
            pady=(4, 8),
        )

        hand_bar = ttk.Frame(hand_frame)
        hand_bar.grid(row=5, column=0, columnspan=4, sticky="w", padx=8, pady=(0, 8))
        self.hand_refresh_watchlist_button = self._pack_bar_button(
            hand_bar,
            text="Refresh watchlist",
            command=self.refresh_hand_confirmation_watchlist_from_ui,
            padx_value=(0, 5),
        )
        self._pack_bar_button(
            hand_bar,
            text="Use live match context",
            command=self.prefill_hand_confirmation_context,
        )
        self._pack_bar_button(
            hand_bar,
            text="Record opening hand",
            command=lambda: self.record_hand_confirmation_from_ui("opening_hand"),
        )
        self._pack_bar_button(
            hand_bar,
            text="Record mulliganed hand",
            command=lambda: self.record_hand_confirmation_from_ui("mulliganed_hand"),
        )
        self._pack_bar_button(
            hand_bar,
            text="Record draw-step hand",
            command=lambda: self.record_hand_confirmation_from_ui("later_draw_step"),
        )
        self._pack_bar_button(
            hand_bar,
            text="Promote singletons",
            command=self.run_promote_singletons_from_ui,
        )
        self._pack_bar_button(
            hand_bar,
            text="Open hand tracker",
            command=self.open_hand_confirmation_tracker,
        )
        self._pack_bar_button(
            hand_bar,
            text="Open candidate report",
            command=self.open_candidate_report,
        )

        promotion_frame = self._section_frame(parent, title="Singleton promotion output", expand=True)
        ttk.Label(
            promotion_frame,
            text=(
                "This panel keeps the latest singleton-promotion helper output "
                "available without mixing it into the live parser log."
            ),
        ).pack(anchor="w", padx=8, pady=(8, 6))
        self.singleton_promotion_text = tk.Text(promotion_frame, wrap="word", height=8, width=90)
        self.singleton_promotion_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._set_singleton_promotion_output("No singleton promotion run yet.")
        self._enable_scrollwheel_for_tab(parent)

    def _build_output_tab(self, notebook: ttk.Notebook) -> None:
        output_tab = ttk.Frame(notebook, padding=16)
        output_tab.columnconfigure(0, weight=1)
        output_tab.rowconfigure(2, weight=1)
        notebook.add(output_tab, text="Live Output")

        ttk.Label(
            output_tab,
            text="Live process output and helper-script logs appear here while the launcher is open.",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        output_bar = ttk.Frame(output_tab)
        output_bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self._pack_bar_button(output_bar, text="Clear output", command=self.clear_live_output, padx_value=(0, 5))
        self._pack_bar_button(output_bar, text="Open output folder", command=self.open_output_folder)

        log_frame = ttk.Frame(output_tab)
        log_frame.grid(row=2, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, wrap="word", height=28)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scroll.set)

    def clear_live_output(self) -> None:
        self.log_text.delete("1.0", tk.END)

    def browse_project_root(self) -> None:
        path = filedialog.askdirectory(initialdir=self.project_root_var.get() or DEFAULT_PROJECT_ROOT)
        if path:
            self.project_root_var.set(path)
            self.refresh_scripts()

    def browse_script_file(self) -> None:
        initial = self.project_root_var.get() or DEFAULT_PROJECT_ROOT
        path = filedialog.askopenfilename(
            initialdir=initial,
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
        if path:
            self.script_var.set(path)

    def browse_player_log(self) -> None:
        path = filedialog.askopenfilename(
            initialdir=str(Path(self.player_log_var.get()).parent) if self.player_log_var.get() else DEFAULT_PLAYER_LOG,
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.player_log_var.set(path)

    def refresh_scripts(self) -> None:
        root = Path(self.project_root_var.get())
        candidates: list[str] = []
        if root.exists():
            for path in (root / "main.py", root / "live_print_filtered_v11_match_summary.py"):
                if path.is_file():
                    candidates.append(str(path))
            for pattern in ("**/live_print_filtered*.py", "**/live_print*.py"):
                for path in sorted(root.glob(pattern)):
                    if path.is_file() and "examples" not in path.parts:
                        candidates.append(str(path))
            seen = set()
            candidates = [x for x in candidates if not (x in seen or seen.add(x))]
        self.script_combo["values"] = candidates
        current = self.script_var.get()
        if current in candidates:
            self.script_var.set(current)
        elif candidates:
            self.script_var.set(candidates[0])
        else:
            self.script_var.set("")

    def persist_settings(self) -> None:
        save_settings(
            {
                "project_root": self.project_root_var.get(),
                "player_log": self.player_log_var.get(),
                "webhook_url": self.webhook_var.get(),
                "post_raw_events": self.post_raw_events_var.get(),
                "post_gamestate": self.post_gamestate_var.get(),
                "post_game_log_rows": self.post_game_log_rows_var.get(),
                "post_match_log_rows": self.post_match_log_rows_var.get(),
                "sync_tier_buckets": self.sync_tier_buckets_var.get(),
                "script_path": self.script_var.get(),
                "python_cmd": self.python_cmd_var.get(),
                "mtga_process_name": self.mtga_process_var.get(),
                "watch_mtga": self.watch_mtga_var.get(),
                "auto_stop_on_close": self.auto_stop_var.get(),
            }
        )
        self.status_var.set("Settings saved")
        self.refresh_health_panel()

    def _validate(self) -> tuple[bool, str]:
        project_root = Path(self.project_root_var.get())
        script_path = Path(self.script_var.get())
        player_log = Path(self.player_log_var.get())
        if not project_root.exists():
            return False, "Project root does not exist."
        if not script_path.exists():
            return False, "Choose a valid filtered script file."
        if not player_log.exists():
            return False, "Player.log path does not exist."
        if self.proc is not None and self.proc.poll() is None:
            return False, "A script is already running."
        return True, ""

    def _project_root(self) -> Path:
        return Path(self.project_root_var.get() or DEFAULT_PROJECT_ROOT)

    def _python_cmd_parts(self) -> list[str]:
        return split_python_command(self.python_cmd_var.get().strip() or sys.executable)

    def _project_helper_command(self, script_name: str, extra_args: list[str] | None = None) -> tuple[Path, list[str]]:
        project_root = self._project_root()
        script_path = project_root / script_name
        if not project_root.exists():
            raise FileNotFoundError("Project root does not exist.")
        if not script_path.exists():
            raise FileNotFoundError(f"Helper script not found: {script_path}")

        cmd = [*self._python_cmd_parts(), str(script_path), *(extra_args or [])]
        return project_root, cmd

    @staticmethod
    def _execute_helper_command(project_root: Path, cmd: list[str]) -> tuple[bool, str, list[str], list[str]]:
        try:
            result = subprocess.run(
                cmd,
                cwd=str(project_root),
                capture_output=True,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception as exc:
            return False, str(exc), [], []

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        if result.returncode != 0:
            detail = stderr or stdout or f"Helper exited with code {result.returncode}"
            return False, detail, stdout.splitlines() if stdout else [], stderr.splitlines() if stderr else []
        return True, stdout or "OK", stdout.splitlines() if stdout else [], stderr.splitlines() if stderr else []

    def _run_project_helper(self, script_name: str, extra_args: list[str] | None = None) -> tuple[bool, str]:
        try:
            project_root, cmd = self._project_helper_command(script_name, extra_args)
        except Exception as exc:
            return False, str(exc)

        self._log(f"Helper: {' '.join(cmd)}")
        ok, detail, stdout_lines, stderr_lines = self._execute_helper_command(project_root, cmd)
        for line in stdout_lines:
            self._log(line)
        for line in stderr_lines:
            self._log(f"[stderr] {line}")
        return ok, detail

    def _sheet_posting_enabled(self) -> bool:
        return any(
            (
                self.post_raw_events_var.get(),
                self.post_gamestate_var.get(),
                self.post_game_log_rows_var.get(),
                self.post_match_log_rows_var.get(),
            )
        )

    def start_script(self) -> None:
        ok, msg = self._validate()
        if not ok:
            messagebox.showerror(APP_NAME, msg)
            return

        if self._sheet_posting_enabled() and not self.webhook_var.get().strip():
            should_continue = messagebox.askyesno(
                APP_NAME,
                "Sheet posting is enabled, but the webhook URL is blank.\n\nStart anyway with local logging only?",
            )
            if not should_continue:
                return

        self.persist_settings()

        project_root = Path(self.project_root_var.get())
        script_path = Path(self.script_var.get())
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root / "src")
        env["MTGA_PLAYER_LOG"] = self.player_log_var.get()
        runtime_flags = {
            "SHEETS_WEBHOOK": self.webhook_var.get().strip(),
            "POST_RAW_EVENTS": "1" if self.post_raw_events_var.get() else "0",
            "POST_GAMESTATE": "1" if self.post_gamestate_var.get() else "0",
            "POST_GAME_LOG_ROWS": "1" if self.post_game_log_rows_var.get() else "0",
            "POST_MATCH_LOG_ROWS": "1" if self.post_match_log_rows_var.get() else "0",
            "SYNC_TIER_BUCKETS": "1" if self.sync_tier_buckets_var.get() else "0",
        }
        for suffix, value in runtime_flags.items():
            env[f"MYTHICEDGE_{suffix}"] = value
            env[f"MYTHICEDGE_{suffix}"] = value

        cmd = self._python_cmd_parts()
        cmd.append(str(script_path))

        self.status_var.set("Running")
        self._log(f"Starting: {' '.join(cmd)}")
        self._log(f"Runtime diagnostics will be written under: {project_root / 'data' / 'runtime_logs'}")
        try:
            self.proc = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except Exception as exc:
            self.proc = None
            self.status_var.set("Start failed")
            messagebox.showerror(APP_NAME, f"Could not start script.\n\n{exc}")
            return

        threading.Thread(target=self._reader_thread, daemon=True).start()
        self._mark_card_catalog_refresh_applied()
        self.refresh_health_panel()

    def _reader_thread(self) -> None:
        assert self.proc is not None
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self.log_queue.put(line.rstrip("\n"))
        rc = self.proc.wait()
        self.log_queue.put(f"[process exited with code {rc}]")
        self.proc = None

    def _drain_log_queue(self) -> None:
        while True:
            try:
                line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._log(line)
            if line.startswith("[process exited"):
                self.status_var.set("Idle")
                self.refresh_health_panel()
        while True:
            try:
                result = self._background_helper_results.get_nowait()
            except queue.Empty:
                break
            if str(result.get("job", "")) == "hand_watchlist_refresh":
                self._handle_hand_watchlist_refresh_result(result)
            elif str(result.get("job", "")) == "catalog_candidate_action":
                self._handle_catalog_candidate_action_result(result)
        self.after(150, self._drain_log_queue)

    def _refresh_health_loop(self) -> None:
        try:
            self.refresh_health_panel()
        finally:
            self.after(2000, self._refresh_health_loop)

    def _watch_mtga_loop(self) -> None:
        try:
            process_name = self.mtga_process_var.get().strip() or DEFAULT_MTGA_PROCESS
            running = is_process_running(process_name)

            if running and not self.mtga_present:
                self.mtga_present = True
                self.prompted_for_current_session = False
                self._log(f"Detected {process_name}.")
                if self.watch_mtga_var.get():
                    self.after(200, self._prompt_start_for_mtga_session)

            elif not running and self.mtga_present:
                self.mtga_present = False
                self.prompted_for_current_session = False
                self._log(f"{process_name} closed.")
                if self.auto_stop_var.get() and self.proc is not None and self.proc.poll() is None:
                    self._log("Stopping parser because MTGA closed.")
                    self.stop_script()

        finally:
            self.after(2000, self._watch_mtga_loop)

    def _prompt_start_for_mtga_session(self) -> None:
        if self.prompted_for_current_session:
            return
        self.prompted_for_current_session = True
        if self.proc is not None and self.proc.poll() is None:
            return
        if messagebox.askyesno(APP_NAME, "MTGA is open. Start the selected parser now?"):
            self.start_script()

    def _log(self, message: str) -> None:
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def _set_hand_watchlist_refresh_busy(self, busy: bool) -> None:
        if self.hand_refresh_watchlist_button is not None:
            self.hand_refresh_watchlist_button.configure(state="disabled" if busy else "normal")

    def _set_catalog_candidate_action_busy(self, busy: bool) -> None:
        self._catalog_candidate_action_in_progress = busy
        for button in (self.catalog_confirm_button, self.catalog_defer_button):
            if button is not None:
                button.configure(state="disabled" if busy else "normal")

    def refresh_hand_confirmation_watchlist_from_ui(self) -> None:
        self._start_hand_watchlist_refresh(show_errors=True)

    def _start_hand_watchlist_refresh(
        self,
        *,
        show_errors: bool,
        requested_signature: str = "",
    ) -> None:
        normalized_signature = str(requested_signature or "").strip()
        if self._hand_watchlist_refresh_in_progress:
            self._pending_hand_watchlist_refresh = True
            if normalized_signature:
                self._pending_hand_watchlist_signature = normalized_signature
            if show_errors:
                self.status_var.set("Watchlist refresh already running in background")
            return

        try:
            project_root, cmd = self._project_helper_command("sync_hand_confirmation_file.py")
        except Exception as exc:
            self.hand_watchlist_status_var.set("Refresh failed")
            if show_errors:
                messagebox.showerror(APP_NAME, f"Could not refresh the hand confirmation tracker.\n\n{exc}")
            else:
                self.status_var.set("Hand watchlist refresh failed")
            return

        self._hand_watchlist_refresh_in_progress = True
        self._set_hand_watchlist_refresh_busy(True)
        self.hand_watchlist_status_var.set("Refreshing watchlist in background...")
        self.status_var.set("Refreshing hand watchlist...")
        self._log(f"Helper: {' '.join(cmd)}")
        threading.Thread(
            target=self._run_hand_watchlist_refresh_job,
            args=(project_root, cmd, show_errors, normalized_signature),
            daemon=True,
        ).start()

    def _run_hand_watchlist_refresh_job(
        self,
        project_root: Path,
        cmd: list[str],
        show_errors: bool,
        requested_signature: str,
    ) -> None:
        ok, detail, stdout_lines, stderr_lines = self._execute_helper_command(project_root, cmd)
        for line in stdout_lines:
            self.log_queue.put(line)
        for line in stderr_lines:
            self.log_queue.put(f"[stderr] {line}")
        self._background_helper_results.put(
            {
                "job": "hand_watchlist_refresh",
                "ok": ok,
                "detail": detail,
                "show_errors": show_errors,
                "requested_signature": requested_signature,
            }
        )

    def _handle_hand_watchlist_refresh_result(self, result: dict[str, Any]) -> None:
        self._hand_watchlist_refresh_in_progress = False
        self._set_hand_watchlist_refresh_busy(False)

        ok = bool(result.get("ok"))
        detail = str(result.get("detail", "") or "").strip()
        requested_signature = str(result.get("requested_signature", "") or "").strip()
        show_errors = bool(result.get("show_errors"))

        if ok:
            refreshed = self.refresh_hand_confirmation_panel(sync=False, show_errors=show_errors)
            if refreshed and requested_signature:
                self.last_seen_submitted_deck_signature = requested_signature
            self.status_var.set("Hand watchlist refresh complete")
        else:
            self.hand_watchlist_status_var.set("Refresh failed")
            self.status_var.set("Hand watchlist refresh failed")
            if show_errors:
                messagebox.showerror(APP_NAME, f"Could not refresh the hand confirmation tracker.\n\n{detail}")

        if self._pending_hand_watchlist_refresh:
            pending_signature = self._pending_hand_watchlist_signature
            self._pending_hand_watchlist_refresh = False
            self._pending_hand_watchlist_signature = ""
            self._start_hand_watchlist_refresh(show_errors=False, requested_signature=pending_signature)

    def _start_catalog_candidate_action(
        self,
        *,
        action: str,
        grp_id: int,
        suggested_name: str,
        evidence_label: str,
    ) -> None:
        if self._catalog_candidate_action_in_progress:
            self.status_var.set("A card-library review action is already running")
            return

        arg_flag = "--confirm-grp-id" if action == "confirm" else "--defer-grp-id"
        try:
            project_root, cmd = self._project_helper_command("score_grp_id_candidates.py", [arg_flag, str(grp_id)])
        except Exception as exc:
            messagebox.showerror(APP_NAME, f"Could not {action} the candidate suggestion.\n\n{exc}")
            return

        self._set_catalog_candidate_action_busy(True)
        verb = "Confirming" if action == "confirm" else "Deferring"
        self.status_var.set(f"{verb} grpId {grp_id}...")
        self._log(f"Helper: {' '.join(cmd)}")
        threading.Thread(
            target=self._run_catalog_candidate_action_job,
            args=(project_root, cmd, action, grp_id, suggested_name, evidence_label),
            daemon=True,
        ).start()

    def _run_catalog_candidate_action_job(
        self,
        project_root: Path,
        cmd: list[str],
        action: str,
        grp_id: int,
        suggested_name: str,
        evidence_label: str,
    ) -> None:
        ok, detail, stdout_lines, stderr_lines = self._execute_helper_command(project_root, cmd)
        for line in stdout_lines:
            self.log_queue.put(line)
        for line in stderr_lines:
            self.log_queue.put(f"[stderr] {line}")
        self._background_helper_results.put(
            {
                "job": "catalog_candidate_action",
                "ok": ok,
                "detail": detail,
                "action": action,
                "grp_id": grp_id,
                "suggested_name": suggested_name,
                "evidence_label": evidence_label,
            }
        )

    def _handle_catalog_candidate_action_result(self, result: dict[str, Any]) -> None:
        self._set_catalog_candidate_action_busy(False)
        ok = bool(result.get("ok"))
        detail = str(result.get("detail", "") or "").strip()
        action = str(result.get("action", "") or "").strip()
        grp_id = int(result.get("grp_id", 0) or 0)
        suggested_name = str(result.get("suggested_name", "") or "").strip()
        evidence_label = str(result.get("evidence_label", "") or "").strip() or "n/a"

        if not ok:
            messagebox.showerror(APP_NAME, f"Could not {action} the candidate suggestion.\n\n{detail}")
            self.status_var.set("Card-library review action failed")
            return

        self.refresh_health_panel()
        if action == "confirm":
            self.status_var.set(f"Confirmed grpId {grp_id} as {suggested_name} ({evidence_label})")
        else:
            self.status_var.set(f"Deferred grpId {grp_id} -> {suggested_name} ({evidence_label})")

    def refresh_health_panel(self) -> None:
        project_root = self._project_root()
        status_payload = load_runtime_status(project_root)
        snapshot = build_health_snapshot(status_payload)
        catalog_status_payload = load_card_catalog_refresh_status(project_root)
        catalog_snapshot = build_card_catalog_snapshot(catalog_status_payload)
        self.health_status_var.set(snapshot["status"])
        self.health_last_event_var.set(snapshot["last_event"])
        self.health_match_var.set(snapshot["current_match"])
        self.health_webhook_var.set(snapshot["webhook"])
        self.health_error_var.set(snapshot["last_error"])
        self.health_updated_at_var.set(snapshot["updated_at"])
        self.catalog_refresh_status_var.set(catalog_snapshot["refresh"])
        self.catalog_last_manual_var.set(catalog_snapshot["last_manual"])
        self.catalog_review_var.set(catalog_snapshot["review"])
        self.catalog_activation_var.set(catalog_snapshot["activation"])
        self.refresh_card_confirmation_panel()
        self._refresh_overview_panel(status_payload, catalog_status_payload)
        self.prefill_hand_confirmation_context(status_payload=status_payload, overwrite_blank_only=True)
        self.maybe_refresh_watchlist_for_active_submitted_deck(status_payload)

    def maybe_refresh_watchlist_for_active_submitted_deck(self, status_payload: dict) -> None:
        signature = str(status_payload.get("active_submitted_deck_signature", "") or "").strip()
        if not signature or signature == self.last_seen_submitted_deck_signature:
            return

        self._start_hand_watchlist_refresh(show_errors=False, requested_signature=signature)

    def prefill_hand_confirmation_context(
        self,
        *,
        status_payload: dict | None = None,
        overwrite_blank_only: bool = False,
    ) -> None:
        payload = status_payload if status_payload is not None else load_runtime_status(self._project_root())
        match_id = str(payload.get("current_match_id", "") or "").strip()
        game_number = str(payload.get("current_game_number", "") or "").strip()

        if match_id and (not overwrite_blank_only or not self.hand_match_id_var.get().strip()):
            self.hand_match_id_var.set(match_id)
        if game_number and (not overwrite_blank_only or not self.hand_game_var.get().strip()):
            self.hand_game_var.set(game_number)

    def refresh_hand_confirmation_panel(self, *, sync: bool, show_errors: bool = True) -> bool:
        if sync:
            ok, detail = self._run_project_helper("sync_hand_confirmation_file.py")
            if not ok:
                if show_errors:
                    messagebox.showerror(APP_NAME, f"Could not refresh the hand confirmation tracker.\n\n{detail}")
                self.hand_watchlist_status_var.set("Refresh failed")
                return False

        tracker_path = self._project_root() / HAND_CONFIRMATIONS_RELATIVE_PATH
        if not tracker_path.exists():
            self.hand_card_combo["values"] = []
            self.hand_watchlist_status_var.set("No hand tracker file yet. Use Refresh watchlist first.")
            return False

        try:
            payload = json.loads(tracker_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.hand_card_combo["values"] = []
            self.hand_watchlist_status_var.set("Could not read hand tracker")
            if show_errors:
                messagebox.showerror(APP_NAME, f"Could not read the hand confirmation tracker.\n\n{exc}")
            return False

        watchlist = payload.get("watchlist") or {}
        watchlist_diagnostics = payload.get("watchlist_diagnostics") or {}
        decklist_alignment = str(payload.get("decklist_alignment", "") or "").strip().lower()
        cards: list[str] = []
        for section_name in ("mainboard", "sideboard"):
            rows = watchlist.get(section_name) or []
            for row in rows:
                name = str((row or {}).get("name", "")).strip()
                if name:
                    cards.append(name)
        cards = list(dict.fromkeys(cards))
        self.hand_card_combo["values"] = cards

        current = self.hand_card_var.get().strip()
        if current not in cards:
            self.hand_card_var.set(cards[0] if cards else "")

        confirmations = list(payload.get("confirmations") or [])
        unresolved_count = 0
        for section_name in ("mainboard", "sideboard"):
            unresolved_count += len(list((watchlist_diagnostics.get(section_name) or [])))

        status_parts = [f"{len(cards)} exact watchlist cards"]
        if unresolved_count:
            status_parts.append(f"{unresolved_count} unresolved submitted grpIds")
        status_parts.append(f"{len(confirmations)} recorded confirmations")
        if decklist_alignment == "drifted":
            status_parts.append("imported deck drifted")
        if not cards:
            status_parts.append("type a card name manually if needed")
        self.hand_watchlist_status_var.set(" | ".join(status_parts))
        return True

    def record_hand_confirmation_from_ui(self, hand_window: str) -> None:
        card_name = self.hand_card_var.get().strip()
        if not card_name:
            messagebox.showerror(APP_NAME, "Choose a watchlist card first.")
            return

        args = [card_name, "--hand-window", hand_window]
        match_id = self.hand_match_id_var.get().strip()
        if match_id:
            args.extend(["--match-id", match_id])

        game_number = self.hand_game_var.get().strip()
        if game_number:
            try:
                int(game_number)
            except ValueError:
                messagebox.showerror(APP_NAME, "Game number must be an integer.")
                return
            args.extend(["--game", game_number])

        match_date = self.hand_date_var.get().strip()
        if match_date:
            args.extend(["--date", match_date])

        match_time = self.hand_time_var.get().strip()
        if match_time:
            args.extend(["--time", match_time])

        opponent = self.hand_opponent_var.get().strip()
        if opponent:
            args.extend(["--opponent", opponent])

        note = self.hand_note_var.get().strip()
        if note:
            args.extend(["--note", note])

        ok, detail = self._run_project_helper("record_hand_confirmation.py", args)
        if not ok:
            messagebox.showerror(APP_NAME, f"Could not record the hand confirmation.\n\n{detail}")
            return

        self.hand_note_var.set("")
        self.hand_time_var.set(datetime.now().strftime("%H:%M"))
        self.refresh_hand_confirmation_panel(sync=False)
        self.status_var.set(f"{hand_window.replace('_', ' ')} confirmation recorded")

    def _set_singleton_promotion_output(self, text: str) -> None:
        self.singleton_promotion_text.configure(state="normal")
        self.singleton_promotion_text.delete("1.0", tk.END)
        self.singleton_promotion_text.insert("1.0", text.strip() or "No singleton promotion output.")
        self.singleton_promotion_text.configure(state="disabled")

    def _promotion_output_summary(self, helper_output: str) -> str:
        lines = [line.strip() for line in helper_output.splitlines() if line.strip()]
        if not lines:
            return "No promotion output was returned."

        preferred_prefixes = (
            "Promoted overrides:",
            "Promoted:",
            "grpId candidate scoring:",
            "Report:",
            "Readable report:",
        )
        preferred = [line for line in lines if line.startswith(preferred_prefixes)]
        if preferred:
            return "\n".join(preferred)
        return "\n".join(lines)

    def run_promote_singletons_from_ui(self) -> None:
        ok, detail = self._run_project_helper("score_grp_id_candidates.py", ["--promote-singletons"])
        if not ok:
            self._set_singleton_promotion_output(detail)
            messagebox.showerror(APP_NAME, f"Could not run singleton promotion.\n\n{detail}")
            return

        self._set_singleton_promotion_output(self._promotion_output_summary(detail))
        self.status_var.set("Singleton promotion run complete")

    def run_card_catalog_refresh_from_ui(self) -> None:
        ok, detail = self._run_project_helper("sync_card_catalog.py")
        if not ok:
            messagebox.showerror(APP_NAME, f"Could not refresh the MTGA card library.\n\n{detail}")
            return

        self.refresh_health_panel()
        self.status_var.set("MTGA card library refresh pipeline complete")

    def open_hand_confirmation_tracker(self) -> None:
        project_root = self._project_root()
        markdown_path = project_root / HAND_CONFIRMATIONS_MARKDOWN_RELATIVE_PATH
        json_path = project_root / HAND_CONFIRMATIONS_RELATIVE_PATH
        target = markdown_path if markdown_path.exists() else (json_path if json_path.exists() else json_path.parent)
        self._open_troubleshooting_target(target)

    def open_candidate_report(self) -> None:
        project_root = self._project_root()
        markdown_path = project_root / CANDIDATE_REPORT_MARKDOWN_RELATIVE_PATH
        target = markdown_path if markdown_path.exists() else markdown_path.parent
        self._open_troubleshooting_target(target)

    def open_card_catalog_refresh_status(self) -> None:
        project_root = self._project_root()
        status_path = project_root / CARD_CATALOG_REFRESH_STATUS_RELATIVE_PATH
        target = status_path if status_path.exists() else status_path.parent
        self._open_troubleshooting_target(target)

    def open_inferred_review_report(self) -> None:
        project_root = self._project_root()
        markdown_path = project_root / INFERRED_REVIEW_MARKDOWN_RELATIVE_PATH
        json_path = project_root / INFERRED_REVIEW_JSON_RELATIVE_PATH
        if markdown_path.exists():
            target = markdown_path
        elif json_path.exists():
            target = json_path
        else:
            target = markdown_path.parent
        self._open_troubleshooting_target(target)

    def open_status_file(self) -> None:
        project_root = self._project_root()
        status_path = project_root / STATUS_RELATIVE_PATH
        target = status_path if status_path.exists() else status_path.parent
        self._open_troubleshooting_target(target)

    def open_runtime_log(self) -> None:
        project_root = self._project_root()
        status_payload = load_runtime_status(project_root)
        runtime_log_value = str(status_payload.get("runtime_log_path", "")).strip()
        runtime_log_path = Path(runtime_log_value) if runtime_log_value else None
        if runtime_log_path and runtime_log_path.exists():
            self._open_troubleshooting_target(runtime_log_path)
            return
        runtime_logs_root = project_root / RUNTIME_LOGS_RELATIVE_ROOT
        target = latest_child_dir(runtime_logs_root) or runtime_logs_root
        self._open_troubleshooting_target(target)

    def open_failed_posts_folder(self) -> None:
        project_root = self._project_root()
        failed_posts_root = project_root / FAILED_POSTS_RELATIVE_ROOT
        target = latest_child_dir(failed_posts_root) or failed_posts_root
        self._open_troubleshooting_target(target)

    def open_bad_events_folder(self) -> None:
        project_root = self._project_root()
        bad_events_root = project_root / BAD_EVENTS_RELATIVE_ROOT
        target = latest_child_dir(bad_events_root) or bad_events_root
        self._open_troubleshooting_target(target)

    def _open_troubleshooting_target(self, target: Path) -> None:
        if not target.exists():
            messagebox.showinfo(
                APP_NAME,
                f"No troubleshooting artifact exists yet at:\n\n{target}",
            )
            return
        try:
            open_path_in_shell(target)
        except Exception as exc:
            messagebox.showerror(APP_NAME, f"Could not open path.\n\n{exc}")

    def _mark_card_catalog_refresh_applied(self) -> None:
        project_root = self._project_root()
        status_path = project_root / CARD_CATALOG_REFRESH_STATUS_RELATIVE_PATH
        if not status_path.exists():
            return
        payload = load_card_catalog_refresh_status(project_root)
        if not payload or not payload.get("next_restart_required"):
            return
        payload["next_restart_required"] = False
        payload["last_applied_parser_start_at"] = datetime.now().astimezone().isoformat()
        status_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def stop_script(self) -> None:
        if self.proc is None or self.proc.poll() is not None:
            self.status_var.set("Idle")
            self.refresh_health_panel()
            return
        self.proc.terminate()
        self.status_var.set("Stopping")

    def open_output_folder(self) -> None:
        root = Path(self.project_root_var.get())
        output_root = root / "data" / "match_logs"
        if not output_root.exists():
            legacy_output_root = root / "match_logs"
            output_root = legacy_output_root if legacy_output_root.exists() else root
        try:
            if sys.platform.startswith("win"):
                os.startfile(output_root)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(output_root)])
            else:
                subprocess.Popen(["xdg-open", str(output_root)])
        except Exception as exc:
            messagebox.showerror(APP_NAME, f"Could not open folder.\n\n{exc}")

    def on_close(self) -> None:
        self.persist_settings()
        if self.proc is not None and self.proc.poll() is None:
            if messagebox.askyesno(APP_NAME, "A script is still running. Stop it and close?"):
                self.stop_script()
            else:
                return
        self.destroy()


if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
