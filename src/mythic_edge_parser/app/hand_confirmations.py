from __future__ import annotations

import json
from datetime import UTC, date, datetime, time
from pathlib import Path
from typing import Any
from uuid import uuid4

from .config import HAND_CONFIRMATIONS_PATH, ORACLE_DATA_ROOT

DEFAULT_CANDIDATE_REPORT_PATH = ORACLE_DATA_ROOT / "grp-id-candidate-report-latest.json"
HAND_WINDOW_LABELS: dict[str, str] = {
    "opening_hand": "Opening hand",
    "mulliganed_hand": "Mulliganed hand",
    "later_draw_step": "Later hand at draw step",
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _markdown_path_for(json_path: Path) -> Path:
    return json_path.with_suffix(".md")


def _load_json_dict(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def normalize_hand_window(value: str | None) -> str:
    normalized = str(value or "").strip().lower()
    if not normalized:
        return "opening_hand"
    if normalized not in HAND_WINDOW_LABELS:
        raise ValueError(
            "hand_window must be one of: "
            + ", ".join(sorted(HAND_WINDOW_LABELS))
        )
    return normalized


def hand_window_label(value: str | None) -> str:
    try:
        normalized = normalize_hand_window(value)
    except ValueError:
        normalized = "opening_hand"
    return HAND_WINDOW_LABELS.get(normalized, "Opening hand")


def load_candidate_report(path: Path | None = None) -> dict[str, Any]:
    report_path = path or DEFAULT_CANDIDATE_REPORT_PATH
    if not report_path.exists():
        raise FileNotFoundError(f"Candidate report not found: {report_path}")
    return _load_json_dict(report_path)


def _sorted_watchlist(section: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, count in sorted(section.items()):
        rows.append({"name": str(name), "count": int(count)})
    return rows


def _sorted_watchlist_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("name", "")).strip().lower(),
            int(row.get("count", 0) or 0),
        ),
    )


def _build_watchlist_from_remaining_names(report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    mainboard = report.get("remaining_mainboard_names") or {}
    sideboard = report.get("remaining_sideboard_names") or {}
    if not isinstance(mainboard, dict) or not isinstance(sideboard, dict):
        raise ValueError("Candidate report is missing remaining deck-name sections.")
    return {
        "mainboard": _sorted_watchlist(mainboard),
        "sideboard": _sorted_watchlist(sideboard),
    }


def _int_value(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _report_rows(report: dict[str, Any], key: str) -> list[dict[str, Any]]:
    rows = report.get(key) or []
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _top_ranked_candidate_summary(row: dict[str, Any]) -> tuple[str, int]:
    ranked_candidates = row.get("ranked_candidates") or []
    if not isinstance(ranked_candidates, list) or not ranked_candidates:
        return "", 0

    first = ranked_candidates[0]
    if not isinstance(first, dict):
        return "", 0

    return str(first.get("name", "")).strip(), _int_value(first.get("score"))


def _watchlist_entry(
    *,
    name: str,
    count: int,
    source: str,
    grp_id: int,
) -> dict[str, Any]:
    return {
        "name": name,
        "count": count,
        "source": source,
        "grp_id": grp_id,
    }


def _watchlist_diagnostic_entry(
    *,
    grp_id: int,
    count: int,
    top_candidate_name: str,
    top_candidate_score: int,
) -> dict[str, Any]:
    return {
        "grp_id": grp_id,
        "count": count,
        "top_candidate_name": top_candidate_name,
        "top_candidate_score": top_candidate_score,
    }


def _build_watchlist_from_submitted_deck(
    report: dict[str, Any],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    watchlist: dict[str, list[dict[str, Any]]] = {"mainboard": [], "sideboard": []}
    diagnostics: dict[str, list[dict[str, Any]]] = {"mainboard": [], "sideboard": []}

    for section_name, report_key in (
        ("mainboard", "unresolved_mainboard_grp_ids"),
        ("sideboard", "unresolved_sideboard_grp_ids"),
    ):
        for row in _report_rows(report, report_key):
            submitted_count = _int_value(row.get("submitted_count"))
            grp_id = _int_value(row.get("grp_id"))
            auto_suggestion = str(row.get("auto_suggestion", "")).strip()
            top_candidate_name, top_candidate_score = _top_ranked_candidate_summary(row)

            if auto_suggestion:
                watchlist[section_name].append(_watchlist_entry(
                    name=auto_suggestion,
                    count=submitted_count,
                    source="submitted_deck_auto_suggestion",
                    grp_id=grp_id,
                ))
                continue

            diagnostics[section_name].append(
                _watchlist_diagnostic_entry(
                    grp_id=grp_id,
                    count=submitted_count,
                    top_candidate_name=top_candidate_name,
                    top_candidate_score=top_candidate_score,
                )
            )

        watchlist[section_name] = _sorted_watchlist_rows(watchlist[section_name])
        diagnostics[section_name] = sorted(
            diagnostics[section_name],
            key=lambda row: (-int(row.get("count", 0)), int(row.get("grp_id", 0))),
        )

    return watchlist, diagnostics


def _watchlist_payload_from_report(
    report: dict[str, Any],
) -> tuple[dict[str, list[dict[str, Any]]], str, dict[str, list[dict[str, Any]]]]:
    decklist_alignment = str(report.get("decklist_alignment", "aligned")).strip().lower() or "aligned"
    if decklist_alignment == "aligned":
        return _build_watchlist_from_remaining_names(report), "remaining_decklist_names", {
            "mainboard": [],
            "sideboard": [],
        }
    watchlist, diagnostics = _build_watchlist_from_submitted_deck(report)
    return watchlist, "submitted_deck_auto_suggestions", diagnostics


def _card_names_in_section(watchlist: dict[str, list[dict[str, Any]]], section: str) -> set[str]:
    rows = watchlist.get(section) or []
    return {str(row.get("name", "")).strip() for row in rows if str(row.get("name", "")).strip()}


def _section_hint_for_name(watchlist: dict[str, list[dict[str, Any]]], card_name: str) -> str:
    normalized = card_name.strip()
    if normalized in _card_names_in_section(watchlist, "mainboard"):
        return "mainboard"
    if normalized in _card_names_in_section(watchlist, "sideboard"):
        return "sideboard"
    return "unknown"


def _new_payload_from_report(report: dict[str, Any], *, candidate_report_path: Path) -> dict[str, Any]:
    now = _now_iso()
    watchlist, watchlist_source, watchlist_diagnostics = _watchlist_payload_from_report(report)
    return {
        "object": "manasight_hand_confirmations",
        "generated_at": now,
        "updated_at": now,
        "deck_label": str(report.get("deck_label", "")).strip(),
        "candidate_report_path": str(candidate_report_path),
        "candidate_report_generated_at": str(report.get("generated_at", "")).strip(),
        "decklist_alignment": str(report.get("decklist_alignment", "aligned")).strip() or "aligned",
        "decklist_alignment_notes": list(report.get("decklist_alignment_notes") or []),
        "watchlist_source": watchlist_source,
        "watchlist": watchlist,
        "watchlist_diagnostics": watchlist_diagnostics,
        "confirmations": [],
    }


def _existing_confirmation_payload(
    confirmation_path: Path,
    *,
    candidate_report_path: Path | None = None,
) -> dict[str, Any]:
    refresh_hand_confirmation_file(path=confirmation_path, candidate_report_path=candidate_report_path)
    payload = load_hand_confirmation_payload(confirmation_path)
    watchlist = payload.get("watchlist") or {}
    if not isinstance(watchlist, dict):
        watchlist = {"mainboard": [], "sideboard": []}
    payload["watchlist"] = watchlist
    return payload


def _confirmation_entry(
    *,
    card_name: str,
    hand_window: str,
    watchlist: dict[str, list[dict[str, Any]]],
    match_id_hint: str,
    game_number: int | None,
    match_date_hint: str,
    match_time_hint: str,
    opponent_archetype: str,
    note: str,
) -> dict[str, Any]:
    return {
        "confirmation_id": uuid4().hex,
        "recorded_at": _now_iso(),
        "card_name": card_name,
        "hand_window": hand_window,
        "section_hint": _section_hint_for_name(watchlist, card_name),
        "match_id_hint": match_id_hint.strip(),
        "game_number": int(game_number) if game_number is not None else None,
        "match_date_hint": match_date_hint.strip(),
        "match_time_hint": match_time_hint.strip(),
        "opponent_archetype": opponent_archetype.strip(),
        "note": note.strip(),
        "status": "open",
    }


def load_hand_confirmation_payload(path: Path | None = None) -> dict[str, Any]:
    confirmation_path = path or HAND_CONFIRMATIONS_PATH
    if not confirmation_path.exists():
        raise FileNotFoundError(f"Hand confirmation file not found: {confirmation_path}")
    payload = _load_json_dict(confirmation_path)
    if payload.get("object") != "manasight_hand_confirmations":
        raise ValueError(f"Unexpected hand confirmation payload type in {confirmation_path}")
    return payload


def write_hand_confirmation_payload(payload: dict[str, Any], *, path: Path | None = None) -> tuple[Path, Path]:
    confirmation_path = path or HAND_CONFIRMATIONS_PATH
    confirmation_path.parent.mkdir(parents=True, exist_ok=True)
    confirmation_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    markdown_path = _markdown_path_for(confirmation_path)
    markdown_path.write_text(render_hand_confirmation_markdown(payload), encoding="utf-8")
    return confirmation_path, markdown_path


def refresh_hand_confirmation_file(
    *,
    path: Path | None = None,
    candidate_report_path: Path | None = None,
    rebuild_candidate_report: bool = False,
) -> tuple[Path, Path]:
    confirmation_path = path or HAND_CONFIRMATIONS_PATH
    report_path = candidate_report_path or DEFAULT_CANDIDATE_REPORT_PATH
    if rebuild_candidate_report:
        from .grp_id_candidates import build_grp_id_candidate_report

        report = build_grp_id_candidate_report()
        if report.report_path is None:
            raise RuntimeError("Candidate report rebuild completed without a report path.")
        report_path = report.report_path
    report = load_candidate_report(report_path)
    fresh_payload = _new_payload_from_report(report, candidate_report_path=report_path)

    if confirmation_path.exists():
        existing_payload = load_hand_confirmation_payload(confirmation_path)
        fresh_payload["generated_at"] = str(existing_payload.get("generated_at", fresh_payload["generated_at"]))
        fresh_payload["confirmations"] = list(existing_payload.get("confirmations") or [])

    fresh_payload["updated_at"] = _now_iso()
    return write_hand_confirmation_payload(fresh_payload, path=confirmation_path)


def record_hand_confirmation(
    *,
    card_name: str,
    hand_window: str = "opening_hand",
    match_id_hint: str = "",
    game_number: int | None = None,
    match_date_hint: str = "",
    match_time_hint: str = "",
    opponent_archetype: str = "",
    note: str = "",
    path: Path | None = None,
    candidate_report_path: Path | None = None,
) -> tuple[dict[str, Any], Path, Path]:
    normalized_name = card_name.strip()
    if not normalized_name:
        raise ValueError("card_name must not be blank.")
    normalized_hand_window = normalize_hand_window(hand_window)

    confirmation_path = path or HAND_CONFIRMATIONS_PATH
    payload = _existing_confirmation_payload(
        confirmation_path,
        candidate_report_path=candidate_report_path,
    )
    watchlist = payload["watchlist"]
    entry = _confirmation_entry(
        card_name=normalized_name,
        hand_window=normalized_hand_window,
        watchlist=watchlist,
        match_id_hint=match_id_hint,
        game_number=game_number,
        match_date_hint=match_date_hint,
        match_time_hint=match_time_hint,
        opponent_archetype=opponent_archetype,
        note=note,
    )

    confirmations = list(payload.get("confirmations") or [])
    confirmations.append(entry)
    payload["confirmations"] = confirmations
    payload["updated_at"] = _now_iso()
    json_path, markdown_path = write_hand_confirmation_payload(payload, path=confirmation_path)
    return entry, json_path, markdown_path


def render_hand_confirmation_markdown(payload: dict[str, Any]) -> str:
    deck_label = str(payload.get("deck_label", "")).strip()
    candidate_report_path = str(payload.get("candidate_report_path", "")).strip()
    decklist_alignment = str(payload.get("decklist_alignment", "aligned")).strip()
    decklist_alignment_notes = list(payload.get("decklist_alignment_notes") or [])
    watchlist_source = str(payload.get("watchlist_source", "")).strip()
    watchlist = payload.get("watchlist") or {}
    watchlist_diagnostics = payload.get("watchlist_diagnostics") or {}
    confirmations = list(payload.get("confirmations") or [])

    lines = [
        "# Hand Confirmation Tracker",
        "",
        f"- Deck: `{deck_label}`",
        f"- Candidate report: `{candidate_report_path}`",
        f"- Decklist alignment: `{decklist_alignment}`",
        f"- Watchlist source: `{watchlist_source}`",
        f"- Last updated: `{payload.get('updated_at', '')}`",
        "",
        "Use this file to record cards you actually saw in your opening hand or mulligan hand.",
        (
            "You can also record later draw-step hand sightings for future automation, but the current "
            "singleton promotion logic only trusts opening-hand and mulliganed-hand confirmations."
        ),
        (
            "The goal is to tie a real observed card name to a saved match/game window so the unresolved "
            "MTGA `grpId` can be identified later."
        ),
        "",
    ]

    if decklist_alignment_notes:
        lines.extend(["## Decklist Alignment Notes", ""])
        for note in decklist_alignment_notes:
            lines.append(f"- {note}")
        lines.append("")

    mainboard = list(watchlist.get("mainboard") or [])
    sideboard = list(watchlist.get("sideboard") or [])
    lines.extend(["## Current Watchlist", ""])
    _append_watchlist_markdown_section(lines, "Mainboard", mainboard)
    _append_watchlist_markdown_section(lines, "Sideboard", sideboard)

    diagnostics_mainboard = list(watchlist_diagnostics.get("mainboard") or [])
    diagnostics_sideboard = list(watchlist_diagnostics.get("sideboard") or [])
    if diagnostics_mainboard or diagnostics_sideboard:
        lines.extend(["", "## Submitted-Deck Unresolved grpIds Still Missing Exact Names", ""])
        _append_watchlist_diagnostics_markdown_section(lines, "Mainboard", diagnostics_mainboard)
        _append_watchlist_diagnostics_markdown_section(lines, "Sideboard", diagnostics_sideboard)

    lines.extend(
        [
            "",
            "## Recorded Confirmations",
            "",
            (
                "| Recorded At | Card | Hand Window | Section | Match ID | Game | Match Date | Match Time | "
                "Opponent | Status | Note |"
            ),
            "|---|---|---|---|---|---:|---|---|---|---|---|",
        ]
    )

    if confirmations:
        for entry in confirmations:
            lines.append(_confirmation_markdown_row(entry))
    else:
        lines.append("|  |  |  |  |  |  |  |  |  |  |  |")

    return "\n".join(lines) + "\n"


def _append_watchlist_markdown_section(
    lines: list[str],
    title: str,
    rows: list[dict[str, Any]],
) -> None:
    lines.extend([f"### {title}", ""])
    if rows:
        for row in rows:
            lines.append(f"- `{row.get('count', 0)}x` {row.get('name', '')}")
    else:
        lines.append("- None")
    lines.append("")


def _append_watchlist_diagnostics_markdown_section(
    lines: list[str],
    title: str,
    rows: list[dict[str, Any]],
) -> None:
    lines.extend([f"### {title}", ""])
    if not rows:
        lines.extend(["- None", ""])
        return

    for row in rows:
        grp_id = row.get("grp_id", 0)
        count = row.get("count", 0)
        top_name = str(row.get("top_candidate_name", "")).strip()
        top_score = row.get("top_candidate_score", 0)
        if top_name:
            lines.append(
                f"- `grpId {grp_id}` `{count}x` unresolved. Current top candidate: "
                f"`{top_name}` (score `{top_score}`)."
            )
        else:
            lines.append(f"- `grpId {grp_id}` `{count}x` unresolved.")
    lines.append("")


def _confirmation_markdown_row(entry: dict[str, Any]) -> str:
    return (
        "| {recorded_at} | {card_name} | {hand_window} | {section_hint} | {match_id_hint} | {game_number} | "
        "{match_date_hint} | {match_time_hint} | {opponent_archetype} | {status} | {note} |"
    ).format(
        recorded_at=str(entry.get("recorded_at", "")).replace("|", "/"),
        card_name=str(entry.get("card_name", "")).replace("|", "/"),
        hand_window=hand_window_label(entry.get("hand_window")),
        section_hint=str(entry.get("section_hint", "")).replace("|", "/"),
        match_id_hint=str(entry.get("match_id_hint", "")).replace("|", "/"),
        game_number="" if entry.get("game_number") is None else int(entry["game_number"]),
        match_date_hint=str(entry.get("match_date_hint", "")).replace("|", "/"),
        match_time_hint=str(entry.get("match_time_hint", "")).replace("|", "/"),
        opponent_archetype=str(entry.get("opponent_archetype", "")).replace("|", "/"),
        status=str(entry.get("status", "")).replace("|", "/"),
        note=str(entry.get("note", "")).replace("|", "/"),
    )


def _valid_date_hint(value: str) -> str:
    if not value.strip():
        return ""
    date.fromisoformat(value.strip())
    return value.strip()


def _valid_time_hint(value: str) -> str:
    if not value.strip():
        return ""
    time.fromisoformat(value.strip())
    return value.strip()


def main_sync(candidate_report_path: Path | None = None) -> tuple[Path, Path]:
    return refresh_hand_confirmation_file(
        candidate_report_path=candidate_report_path,
        rebuild_candidate_report=candidate_report_path is None,
    )


def main_record(
    *,
    card_name: str,
    hand_window: str = "opening_hand",
    match_id_hint: str = "",
    game_number: int | None = None,
    match_date_hint: str = "",
    match_time_hint: str = "",
    opponent_archetype: str = "",
    note: str = "",
    candidate_report_path: Path | None = None,
) -> tuple[dict[str, Any], Path, Path]:
    return record_hand_confirmation(
        card_name=card_name,
        hand_window=normalize_hand_window(hand_window),
        match_id_hint=match_id_hint,
        game_number=game_number,
        match_date_hint=_valid_date_hint(match_date_hint),
        match_time_hint=_valid_time_hint(match_time_hint),
        opponent_archetype=opponent_archetype,
        note=note,
        candidate_report_path=candidate_report_path,
    )
