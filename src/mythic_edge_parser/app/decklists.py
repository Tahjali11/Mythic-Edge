from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import CURRENT_DECKLIST_PATH, DECKLISTS_ROOT

ARENA_DECK_LINE_RE = re.compile(r"^\s*(?P<count>\d+)\s+(?P<rest>.+?)\s*$")
TRAILING_SET_INFO_RE = re.compile(r"\s+\([A-Za-z0-9]+\)\s+\S+\s*$")


@dataclass(slots=True)
class DeckCardEntry:
    name: str
    count: int


@dataclass(slots=True)
class DecklistSnapshot:
    label: str
    generated_at: str
    source_path: str
    mainboard: list[DeckCardEntry]
    sideboard: list[DeckCardEntry]

    def mainboard_counts(self) -> Counter[str]:
        return _entry_counts(self.mainboard)

    def sideboard_counts(self) -> Counter[str]:
        return _entry_counts(self.sideboard)


def ensure_decklists_root(root: Path = DECKLISTS_ROOT) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    return root


def _normalized_entry_name(raw_name: str) -> str:
    name = TRAILING_SET_INFO_RE.sub("", raw_name).strip()
    return name


def _entry_counts(entries: list[DeckCardEntry]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for entry in entries:
        counter[entry.name] += entry.count
    return counter


def _normalized_count(value: Any) -> int:
    try:
        count = int(value)
    except (TypeError, ValueError):
        return 0
    return count if count > 0 else 0


def _entry_from_payload(payload: Any) -> DeckCardEntry | None:
    if not isinstance(payload, dict):
        return None
    name = str(payload.get("name", "")).strip()
    count = _normalized_count(payload.get("count", 0))
    if not name or count <= 0:
        return None
    return DeckCardEntry(name=name, count=count)


def _entries_from_payload(payload: Any) -> list[DeckCardEntry]:
    rows = payload if isinstance(payload, list) else []
    entries: list[DeckCardEntry] = []
    for row in rows:
        entry = _entry_from_payload(row)
        if entry is not None:
            entries.append(entry)
    return entries


def _canonicalized_entries(entries: list[DeckCardEntry], aliases: dict[str, str]) -> list[DeckCardEntry]:
    canonical_counts: Counter[str] = Counter()
    canonical_order: list[str] = []
    for entry in entries:
        canonical_name = aliases.get(entry.name, entry.name)
        if canonical_name not in canonical_counts:
            canonical_order.append(canonical_name)
        canonical_counts[canonical_name] += entry.count
    return [DeckCardEntry(name=name, count=canonical_counts[name]) for name in canonical_order]


def _parsed_deck_entry(line: str) -> DeckCardEntry | None:
    match = ARENA_DECK_LINE_RE.match(line)
    if not match:
        return None
    count = _normalized_count(match.group("count"))
    name = _normalized_entry_name(match.group("rest"))
    if not name or count <= 0:
        return None
    return DeckCardEntry(name=name, count=count)


def build_catalog_name_aliases(cards_by_arena_id: dict[str, dict[str, Any]]) -> dict[str, str]:
    direct_names: dict[str, str] = {}
    face_name_candidates: dict[str, set[str]] = {}

    for card in cards_by_arena_id.values():
        if not isinstance(card, dict):
            continue
        full_name = str(card.get("name", "")).strip()
        if not full_name:
            continue
        direct_names.setdefault(full_name, full_name)

        for face in card.get("card_faces") or []:
            if not isinstance(face, dict):
                continue
            face_name = str(face.get("name", "")).strip()
            if not face_name:
                continue
            face_name_candidates.setdefault(face_name, set()).add(full_name)

    aliases = dict(direct_names)
    for face_name, candidates in face_name_candidates.items():
        if len(candidates) == 1:
            aliases.setdefault(face_name, next(iter(candidates)))
    return aliases


def canonicalize_decklist_names(
    snapshot: DecklistSnapshot,
    *,
    cards_by_arena_id: dict[str, dict[str, Any]],
) -> DecklistSnapshot:
    aliases = build_catalog_name_aliases(cards_by_arena_id)

    return DecklistSnapshot(
        label=snapshot.label,
        generated_at=snapshot.generated_at,
        source_path=snapshot.source_path,
        mainboard=_canonicalized_entries(snapshot.mainboard, aliases),
        sideboard=_canonicalized_entries(snapshot.sideboard, aliases),
    )


def parse_arena_decklist_text(
    text: str,
    *,
    label: str = "Current Deck",
    source_path: str = "",
) -> DecklistSnapshot:
    section = "mainboard"
    mainboard: list[DeckCardEntry] = []
    sideboard: list[DeckCardEntry] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lowered = line.lower()
        if lowered == "deck":
            section = "mainboard"
            continue
        if lowered == "sideboard":
            section = "sideboard"
            continue
        if lowered in {"companion", "commander", "about"}:
            section = "ignore"
            continue
        if section == "ignore":
            continue

        entry = _parsed_deck_entry(line)
        if entry is None:
            continue

        if section == "sideboard":
            sideboard.append(entry)
        else:
            mainboard.append(entry)

    return DecklistSnapshot(
        label=label.strip() or "Current Deck",
        generated_at=datetime.now(UTC).isoformat(),
        source_path=source_path,
        mainboard=mainboard,
        sideboard=sideboard,
    )


def save_current_decklist(snapshot: DecklistSnapshot, *, path: Path = CURRENT_DECKLIST_PATH) -> Path:
    ensure_decklists_root(path.parent)
    payload = {
        "object": "manasight_current_decklist",
        "label": snapshot.label,
        "generated_at": snapshot.generated_at,
        "source_path": snapshot.source_path,
        "mainboard": [asdict(entry) for entry in snapshot.mainboard],
        "sideboard": [asdict(entry) for entry in snapshot.sideboard],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_current_decklist(path: Path = CURRENT_DECKLIST_PATH) -> DecklistSnapshot:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected current decklist payload in {path}")
    return DecklistSnapshot(
        label=str(payload.get("label", "Current Deck")),
        generated_at=str(payload.get("generated_at", "")),
        source_path=str(payload.get("source_path", "")),
        mainboard=_entries_from_payload(payload.get("mainboard")),
        sideboard=_entries_from_payload(payload.get("sideboard")),
    )


def load_current_decklist_text(path: Path) -> DecklistSnapshot:
    return parse_arena_decklist_text(
        path.read_text(encoding="utf-8"),
        label=path.stem,
        source_path=str(path),
    )


def validate_decklist_names(
    snapshot: DecklistSnapshot,
    *,
    known_names: set[str],
) -> dict[str, Any]:
    missing_mainboard = sorted(entry.name for entry in snapshot.mainboard if entry.name not in known_names)
    missing_sideboard = sorted(entry.name for entry in snapshot.sideboard if entry.name not in known_names)
    return {
        "label": snapshot.label,
        "missing_mainboard_names": missing_mainboard,
        "missing_sideboard_names": missing_sideboard,
    }
