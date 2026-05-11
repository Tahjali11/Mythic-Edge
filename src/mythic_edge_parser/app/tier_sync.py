from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from .config import TIER_NORMALIZATION_PATH, TIER_SOURCES_ROOT, WEBHOOK_URL
from .outputs import post_row_to_google_sheets

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT_SECONDS = 20
SNAPSHOT_FILENAME = "latest_tier_snapshot.json"
SOURCE_WINDOW_LABELS = {
    "mtggoldfish": "Past 14 days",
    "mtgtop8": "Past 14 days",
    "untapped": "Past 30 days",
}
SOURCE_LABELS = {
    "mtggoldfish": "MTGGoldfish",
    "mtgtop8": "MTGTop8",
    "untapped": "Untapped",
}
SOURCE_URLS = {
    "mtggoldfish": "https://www.mtggoldfish.com/metagame/standard#paper",
    "mtgtop8": "https://www.mtgtop8.com/archetype?a=770&meta=50&f=ST",
    "untapped": "https://mtga.untapped.gg/constructed/standard/tier-list?wincon=bo3&rank=MYTHIC_TO_MYTHIC",
}
SOURCE_SCOPE = {
    "mtggoldfish": "Standard paper meta, public site",
    "mtgtop8": "Standard tournament meta, public site",
    "untapped": "Standard Bo3 Mythic ladder, premium site",
}
STARTER_NORMALIZATION_OVERRIDES = {
    "_comment": (
        "Map raw website deck names to the canonical archetype names you want to use in the workbook. "
        "Leave a source section empty if you want names to pass through unchanged."
    ),
    "global": {},
    "mtggoldfish": {},
    "mtgtop8": {},
    "untapped": {},
}


@dataclass(slots=True)
class TierRecord:
    source_key: str
    source_label: str
    refreshed_at: str
    source_url: str
    meta_window: str
    source_scope: str
    status: str
    notes: str
    raw_archetype: str = ""
    normalized_archetype: str = ""
    meta_share_pct: float | None = None
    tier_bucket: str = ""
    tier_letter: str = ""

    def to_sheet_row(self) -> dict[str, Any]:
        row = asdict(self)
        row["meta_share_pct"] = "" if self.meta_share_pct is None else self.meta_share_pct
        return row


@dataclass(slots=True)
class TierSyncResult:
    snapshot_path: Path
    payload: dict[str, Any]

    @property
    def records(self) -> list[dict[str, Any]]:
        return list(self.payload.get("records") or [])

    @property
    def ok_rows(self) -> int:
        return sum(1 for row in self.records if row.get("status") == "ok")

    @property
    def available_sources(self) -> int:
        return len({row["source_key"] for row in self.records if row.get("status") == "ok"})

    def summary_line(self) -> str:
        total_sources = len({row["source_key"] for row in self.records})
        return (
            f"Tier sync: {self.available_sources}/{total_sources} sources ready, "
            f"{self.ok_rows} deck rows -> {self.snapshot_path}"
        )


def sync_tier_sources(post_to_webhook: bool = True) -> TierSyncResult:
    snapshot = build_tier_snapshot_payload()
    snapshot_path = write_tier_snapshot(snapshot)

    if post_to_webhook and WEBHOOK_URL:
        post_row_to_google_sheets(snapshot)

    return TierSyncResult(snapshot_path=snapshot_path, payload=snapshot)


def build_tier_snapshot_payload() -> dict[str, Any]:
    refreshed_at = datetime.now(UTC).isoformat()
    overrides = load_normalization_overrides()
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)

    records: list[TierRecord] = []
    records.extend(_scrape_mtggoldfish(session, refreshed_at, overrides))
    records.extend(_scrape_mtgtop8(session, refreshed_at, overrides))
    records.extend(_scrape_untapped(session, refreshed_at, overrides))

    return {
        "event_family": "TierSourceSnapshot",
        "event_type": "tier_source_snapshot",
        "scope": "Workbook",
        "timestamp": refreshed_at,
        "records": [record.to_sheet_row() for record in records],
        "raw_json": json.dumps([record.to_sheet_row() for record in records], ensure_ascii=False),
    }


def write_tier_snapshot(snapshot: dict[str, Any]) -> Path:
    TIER_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
    if not TIER_NORMALIZATION_PATH.exists():
        _write_json(TIER_NORMALIZATION_PATH, STARTER_NORMALIZATION_OVERRIDES)

    out_path = TIER_SOURCES_ROOT / SNAPSHOT_FILENAME
    _write_json(out_path, snapshot)
    return out_path


def load_normalization_overrides() -> dict[str, dict[str, str]]:
    TIER_SOURCES_ROOT.mkdir(parents=True, exist_ok=True)
    if not TIER_NORMALIZATION_PATH.exists():
        _write_json(TIER_NORMALIZATION_PATH, STARTER_NORMALIZATION_OVERRIDES)

    try:
        raw = json.loads(TIER_NORMALIZATION_PATH.read_text(encoding="utf-8"))
    except Exception:
        raw = STARTER_NORMALIZATION_OVERRIDES

    normalized: dict[str, dict[str, str]] = {"global": {}, "mtggoldfish": {}, "mtgtop8": {}, "untapped": {}}
    for source_key in normalized:
        section = raw.get(source_key, {})
        if not isinstance(section, dict):
            continue
        normalized[source_key] = {
            _normalize_key(key): str(value).strip() for key, value in section.items() if str(value).strip()
        }
    return normalized


def _scrape_mtggoldfish(
    session: requests.Session,
    refreshed_at: str,
    overrides: dict[str, dict[str, str]],
) -> list[TierRecord]:
    source_key = "mtggoldfish"
    try:
        response = session.get(SOURCE_URLS[source_key], timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        records: list[TierRecord] = []
        for tile in soup.select("div.archetype-tile"):
            title = tile.select_one(".archetype-tile-title .deck-price-paper a") or tile.select_one(
                ".archetype-tile-title a"
            )
            if title is None:
                continue

            raw_name = _clean_text(title.get_text(" ", strip=True))
            if not raw_name:
                continue

            stat = tile.select_one(".archetype-tile-statistic.metagame-percentage .archetype-tile-statistic-value")
            meta_share = _parse_percent(stat.get_text(" ", strip=True) if stat else "")
            records.append(
                _build_ok_record(
                    source_key=source_key,
                    refreshed_at=refreshed_at,
                    raw_name=raw_name,
                    meta_share_pct=meta_share,
                    tier_letter="",
                    overrides=overrides,
                )
            )

        return records or [
            _build_unavailable_record(source_key, refreshed_at, "No metagame rows were found on the page.")
        ]
    except Exception as exc:
        return [_build_unavailable_record(source_key, refreshed_at, str(exc))]


def _scrape_mtgtop8(
    session: requests.Session,
    refreshed_at: str,
    overrides: dict[str, dict[str, str]],
) -> list[TierRecord]:
    source_key = "mtgtop8"
    try:
        response = session.get(SOURCE_URLS[source_key], timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        records: list[TierRecord] = []
        seen_names: set[str] = set()
        for row in soup.select("div.hover_tr"):
            link = row.find("a", href=lambda href: isinstance(href, str) and href.startswith("archetype?a="))
            if link is None:
                continue

            raw_name = _clean_text(link.get_text(" ", strip=True))
            if not raw_name or raw_name in seen_names:
                continue

            meta_share = _parse_percent(row.get_text(" ", strip=True))
            if meta_share is None:
                continue

            seen_names.add(raw_name)
            records.append(
                _build_ok_record(
                    source_key=source_key,
                    refreshed_at=refreshed_at,
                    raw_name=raw_name,
                    meta_share_pct=meta_share,
                    tier_letter="",
                    overrides=overrides,
                )
            )

        return records or [
            _build_unavailable_record(source_key, refreshed_at, "No metagame rows were found on the page.")
        ]
    except Exception as exc:
        return [_build_unavailable_record(source_key, refreshed_at, str(exc))]


def _scrape_untapped(
    session: requests.Session,
    refreshed_at: str,
    overrides: dict[str, dict[str, str]],
) -> list[TierRecord]:
    source_key = "untapped"
    try:
        response = session.get(SOURCE_URLS[source_key], timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        body_text = BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)

        # Untapped's public HTML currently exposes the tier framework, but not the actual
        # archetype rows for the Mythic Bo3 tier list unless the page is hydrated with
        # authenticated premium data in-browser.
        if "Premium users" in body_text and "Total matches" in body_text:
            return [
                _build_unavailable_record(
                    source_key,
                    refreshed_at,
                    "Untapped's Mythic Bo3 archetype rows were not available in the public HTML. "
                    "The page appears to require authenticated premium browser data.",
                )
            ]

        # If Untapped later starts rendering public rows in the initial HTML, wire that here.
        return [
            _build_unavailable_record(
                source_key,
                refreshed_at,
                "Untapped tier rows were not found in the fetched HTML.",
            )
        ]
    except Exception as exc:
        return [_build_unavailable_record(source_key, refreshed_at, str(exc))]


def _build_ok_record(
    source_key: str,
    refreshed_at: str,
    raw_name: str,
    meta_share_pct: float | None,
    tier_letter: str,
    overrides: dict[str, dict[str, str]],
) -> TierRecord:
    return TierRecord(
        source_key=source_key,
        source_label=SOURCE_LABELS[source_key],
        refreshed_at=refreshed_at,
        source_url=SOURCE_URLS[source_key],
        meta_window=SOURCE_WINDOW_LABELS[source_key],
        source_scope=SOURCE_SCOPE[source_key],
        status="ok",
        notes="",
        raw_archetype=raw_name,
        normalized_archetype=normalize_archetype_name(source_key, raw_name, overrides),
        meta_share_pct=meta_share_pct,
        tier_bucket=classify_tier_bucket(meta_share_pct, tier_letter),
        tier_letter=tier_letter,
    )


def _build_unavailable_record(source_key: str, refreshed_at: str, notes: str) -> TierRecord:
    return TierRecord(
        source_key=source_key,
        source_label=SOURCE_LABELS[source_key],
        refreshed_at=refreshed_at,
        source_url=SOURCE_URLS[source_key],
        meta_window=SOURCE_WINDOW_LABELS[source_key],
        source_scope=SOURCE_SCOPE[source_key],
        status="unavailable",
        notes=_clean_text(notes),
    )


def normalize_archetype_name(source_key: str, raw_name: str, overrides: dict[str, dict[str, str]]) -> str:
    clean_name = _clean_text(raw_name)
    normalized_key = _normalize_key(clean_name)

    source_overrides = overrides.get(source_key, {})
    global_overrides = overrides.get("global", {})
    if normalized_key in source_overrides:
        return source_overrides[normalized_key]
    if normalized_key in global_overrides:
        return global_overrides[normalized_key]
    return clean_name


def classify_tier_bucket(meta_share_pct: float | None, tier_letter: str) -> str:
    tier_text = str(tier_letter or "").strip().upper()
    if tier_text:
        if tier_text == "A":
            return "Tier 1"
        if tier_text == "B":
            return "Tier 2"
        if tier_text == "C":
            return "Tier 3"
        return "Fringe"

    if meta_share_pct is None:
        return "Fringe"
    if meta_share_pct >= 5:
        return "Tier 1"
    if meta_share_pct >= 2:
        return "Tier 2"
    if meta_share_pct >= 1:
        return "Tier 3"
    return "Fringe"


def _parse_percent(text: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", text or "")
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _normalize_key(text: str) -> str:
    return _clean_text(text).casefold()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
