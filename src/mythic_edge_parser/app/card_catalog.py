from __future__ import annotations

import argparse
import csv
import gzip
import html
import json
import re
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator, cast
from urllib.parse import urlparse

import requests

from .config import GRP_ID_OVERRIDES_PATH, ORACLE_DATA_ROOT

BULK_INDEX_URL = "https://api.scryfall.com/bulk-data"
WOTC_STANDARD_URL = "https://magic.wizards.com/en/formats/standard"
DEFAULT_BULK_TYPE = "default_cards"
DEFAULT_FORMAT = "arena"
DOWNLOAD_DIRNAME = "_downloads"
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
STREAM_CHUNK_SIZE = 64 * 1024
ALL_ARENA_FORMAT_KEYS = {"all", "arena", "all_arena"}
GRP_ID_OVERRIDES_FILENAME = GRP_ID_OVERRIDES_PATH.name
SYNC_STATE_FILENAME = "card-catalog-sync-state.json"
SYNC_HISTORY_FILENAME = "card-catalog-sync-history.jsonl"
SOURCE_STAMP_FALLBACK_RE = re.compile(r"(\d{14})")
SCRIPT_STYLE_RE = re.compile(r"(?is)<(script|style)[^>]*>.*?</\\1>")
HTML_TAG_RE = re.compile(r"(?s)<[^>]+>")
MANA_TOKEN_RE = re.compile(r"\{([^}]+)\}")

MANA_SYMBOL_TO_COLOR = {
    "W": "White",
    "U": "Blue",
    "B": "Black",
    "R": "Red",
    "G": "Green",
}
SUPER_TYPE_NAMES = {"Basic", "Legendary", "Snow", "World", "Ongoing", "Elite", "Host"}
CARD_TYPE_NAMES = {
    "Artifact",
    "Battle",
    "Creature",
    "Enchantment",
    "Instant",
    "Land",
    "Planeswalker",
    "Sorcery",
    "Kindred",
    "Tribal",
}

REQUEST_HEADERS = {
    "User-Agent": "Mythic Edge/1.0 (card catalog sync)",
    "Accept": "application/json;q=0.9,*/*;q=0.8",
}

CARD_FACE_FIELDS = (
    "name",
    "mana_cost",
    "type_line",
    "oracle_text",
    "colors",
    "power",
    "toughness",
    "loyalty",
    "defense",
    "produced_mana",
)

CSV_FIELDS = (
    "arena_id",
    "oracle_id",
    "scryfall_id",
    "name",
    "rarity",
    "set",
    "set_name",
    "collector_number",
    "released_at",
    "layout",
    "mana_cost",
    "cmc",
    "type_line",
    "oracle_text",
    "colors",
    "color_identity",
    "keywords",
    "produced_mana",
    "games",
    "card_faces_json",
)


def catalog_stem(
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
) -> str:
    return f"scryfall-{bulk_type}-{format_key}"


def latest_arena_lookup_path(
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    stem = catalog_stem(format_key=format_key, bulk_type=bulk_type)
    preferred = output_dir / f"{stem}-latest-arena-lookup.json"
    if preferred.exists():
        return preferred

    dated_candidates = sorted(
        output_dir.glob(f"{stem}-*-arena-lookup.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if dated_candidates:
        return dated_candidates[0]

    raise FileNotFoundError(
        f"No Arena lookup file found for format='{format_key}' and bulk_type='{bulk_type}' under {output_dir}"
    )


def latest_catalog_json_path(
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    stem = catalog_stem(format_key=format_key, bulk_type=bulk_type)
    return output_dir / f"{stem}-latest.json"


def latest_raw_source_path(
    *,
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    return output_dir / f"scryfall-{bulk_type}-latest-source.json.gz"


def sync_history_path(output_dir: Path = ORACLE_DATA_ROOT) -> Path:
    return output_dir / SYNC_HISTORY_FILENAME


def sync_state_path(
    output_dir: Path = ORACLE_DATA_ROOT,
    *,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
) -> Path:
    return output_dir / f"card-catalog-sync-state-{bulk_type}-{format_key}.json"


def load_sync_state(
    output_dir: Path = ORACLE_DATA_ROOT,
    *,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
) -> dict[str, Any]:
    path = sync_state_path(output_dir, format_key=format_key, bulk_type=bulk_type)
    if not path.exists():
        legacy_path = output_dir / SYNC_STATE_FILENAME
        if legacy_path.exists():
            path = legacy_path
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def write_sync_state(
    payload: dict[str, Any],
    output_dir: Path = ORACLE_DATA_ROOT,
    *,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
) -> Path:
    path = sync_state_path(output_dir, format_key=format_key, bulk_type=bulk_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _normalize_source_stamp(text: str) -> str:
    normalized = text.strip()
    if not normalized:
        return ""
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
        return parsed.astimezone(UTC).strftime("%Y%m%d%H%M%S")
    except Exception:
        match = SOURCE_STAMP_FALLBACK_RE.search(normalized)
        if match:
            return match.group(1)
    return normalized


def source_stamp_from_bulk_item(bulk_item: dict[str, Any]) -> str:
    updated_at = str(bulk_item.get("updated_at", "")).strip()
    if updated_at:
        normalized = _normalize_source_stamp(updated_at)
        if normalized:
            return normalized
    download_url = str(bulk_item.get("download_uri", "")).strip()
    normalized = _normalize_source_stamp(download_url)
    if normalized:
        return normalized
    return datetime.now(UTC).strftime("%Y%m%d%H%M%S")


def _html_text_lines(html_text: str) -> list[str]:
    without_scripts = SCRIPT_STYLE_RE.sub(" ", html_text)
    without_tags = HTML_TAG_RE.sub("\n", without_scripts)
    decoded = html.unescape(without_tags)
    lines: list[str] = []
    for raw_line in decoded.splitlines():
        line = " ".join(raw_line.split()).strip()
        if line:
            lines.append(line)
    return lines


def parse_wotc_standard_set_names(html_text: str) -> list[str]:
    lines = _html_text_lines(html_text)
    set_names: list[str] = []
    capture = False
    for line in lines:
        if line == "What Sets Are Legal in Standard?":
            capture = True
            continue
        if not capture:
            continue
        if line in {"Different Ways to Play", "Latest Products", "Discover More MTG"}:
            break
        if line in {
            "What Sets Are Legal in Standard?",
            "How does set rotation work?",
            "Set Releases",
        }:
            continue
        if line.startswith("Learn More"):
            continue
        if line not in set_names:
            set_names.append(line)
    return set_names


def fetch_wotc_standard_set_names(session: requests.Session) -> list[str]:
    response = session.get(WOTC_STANDARD_URL, timeout=30)
    response.raise_for_status()
    response.encoding = "utf-8"
    return parse_wotc_standard_set_names(response.text)


def load_arena_lookup(
    path: Path | None = None,
    *,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> dict[str, dict[str, Any]]:
    lookup_path = path or latest_arena_lookup_path(
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )
    payload = json.loads(lookup_path.read_text(encoding="utf-8"))
    cards_by_arena_id = payload.get("cards_by_arena_id")
    if not isinstance(cards_by_arena_id, dict):
        raise ValueError(f"Arena lookup file is missing cards_by_arena_id: {lookup_path}")
    return cards_by_arena_id


def ensure_grp_id_overrides_file(
    path: Path | None = None,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    override_path = path or (output_dir / GRP_ID_OVERRIDES_FILENAME)
    if override_path.exists():
        return override_path

    override_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "object": "manasight_grp_id_overrides",
        "generated_at": datetime.now(UTC).isoformat(),
        "cards_by_grp_id": {},
    }
    override_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return override_path


def load_grp_id_overrides(
    path: Path | None = None,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> dict[str, dict[str, Any]]:
    override_path = ensure_grp_id_overrides_file(path=path, output_dir=output_dir)
    payload = json.loads(override_path.read_text(encoding="utf-8"))
    cards_by_grp_id = payload.get("cards_by_grp_id")
    if not isinstance(cards_by_grp_id, dict):
        raise ValueError(f"grpId override file is missing cards_by_grp_id: {override_path}")

    normalized: dict[str, dict[str, Any]] = {}
    for grp_id, raw_card in cards_by_grp_id.items():
        if not isinstance(raw_card, dict):
            continue
        card_name = str(raw_card.get("name", "")).strip()
        if not card_name:
            continue
        card = dict(raw_card)
        card["name"] = card_name
        normalized[str(grp_id)] = card
    return normalized


def load_combined_card_lookup(
    *,
    grp_id_override_path: Path | None = None,
    arena_lookup_path: Path | None = None,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> dict[str, dict[str, Any]]:
    combined = load_arena_lookup(
        path=arena_lookup_path,
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )
    overrides = load_grp_id_overrides(path=grp_id_override_path, output_dir=output_dir)
    if not overrides:
        return combined

    merged = dict(combined)
    for grp_id, card in overrides.items():
        override_card = dict(card)
        override_card.setdefault("grp_id", grp_id)
        override_card.setdefault("source", "grp_id_override")
        merged[str(grp_id)] = override_card
    return merged


@dataclass(slots=True)
class CatalogSyncResult:
    format_key: str
    bulk_type: str
    source_download_url: str
    bulk_file_path: Path
    catalog_json_path: Path
    arena_lookup_json_path: Path
    csv_path: Path
    total_cards: int
    generated_at: str

    def summary_line(self) -> str:
        scope_label = (
            "Arena cards"
            if self.format_key in ALL_ARENA_FORMAT_KEYS
            else f"{self.format_key}-legal Arena cards"
        )
        return (
            f"Card catalog sync: {self.total_cards} {scope_label} "
            f"from {self.bulk_type} -> {self.catalog_json_path}"
        )


@dataclass(slots=True)
class CatalogAutoSyncDecision:
    checked_at: str
    format_key: str
    bulk_type: str
    synced: bool
    reason: str
    source_stamp: str
    wotc_standard_sets: list[str]
    wotc_standard_sets_changed_since_sync: bool
    state_path: Path
    sync_result: CatalogSyncResult | None = None

    def summary_line(self) -> str:
        prefix = "Card catalog auto-sync"
        action = "synced" if self.synced else "skipped"
        return f"{prefix}: {action} ({self.reason})"


def sync_card_catalog(
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    keep_download: bool = False,
    *,
    session: requests.Session | None = None,
    bulk_item: dict[str, Any] | None = None,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> CatalogSyncResult:
    own_session = session is None
    session = session or requests.Session()
    session.headers.update(REQUEST_HEADERS)
    try:
        bulk_item = bulk_item or get_bulk_item(session, bulk_type)
        bulk_path = download_bulk_file(session, bulk_item, output_dir / DOWNLOAD_DIRNAME)
        catalog = build_catalog_from_bulk_file(
            bulk_path=bulk_path,
            format_key=format_key,
            bulk_item=bulk_item,
        )
        retained_raw_source = retain_latest_raw_source(
            bulk_path=bulk_path,
            bulk_type=bulk_type,
            output_dir=output_dir,
        )
        result = write_catalog_outputs(
            catalog,
            output_dir,
            raw_source_path=retained_raw_source,
        )

        if not keep_download:
            bulk_path.unlink(missing_ok=True)
        return result
    finally:
        if own_session:
            session.close()


def update_sync_state(
    *,
    format_key: str,
    bulk_type: str,
    checked_at: str,
    source_stamp: str,
    reason: str,
    synced: bool,
    manual_trigger: bool,
    output_dir: Path = ORACLE_DATA_ROOT,
    wotc_standard_sets: list[str] | None = None,
    wotc_error: str = "",
    sync_result: CatalogSyncResult | None = None,
) -> Path:
    prior_state = load_sync_state(output_dir, format_key=format_key, bulk_type=bulk_type)
    last_synced_source_stamp = str(prior_state.get("last_synced_source_stamp", "")).strip()
    last_synced_wotc_sets = list(prior_state.get("last_synced_wotc_standard_sets") or [])
    last_successful_sync_at = str(prior_state.get("last_successful_sync_at", "")).strip()
    last_successful_manual_sync_at = str(prior_state.get("last_successful_manual_sync_at", "")).strip()
    last_sync_generated_at = str(prior_state.get("last_sync_generated_at", "")).strip()
    source_download_url = str(prior_state.get("source_download_url", "")).strip()

    if sync_result is not None:
        last_synced_source_stamp = source_stamp
        last_sync_generated_at = sync_result.generated_at
        last_successful_sync_at = sync_result.generated_at
        source_download_url = sync_result.source_download_url
        if manual_trigger:
            last_successful_manual_sync_at = sync_result.generated_at
        if wotc_standard_sets:
            last_synced_wotc_sets = list(wotc_standard_sets)

    state_payload: dict[str, Any] = {
        "object": "manasight_card_catalog_sync_state",
        "updated_at": checked_at,
        "format": format_key,
        "bulk_type": bulk_type,
        "last_checked_at": checked_at,
        "last_seen_source_stamp": source_stamp,
        "last_seen_wotc_standard_sets": list(wotc_standard_sets or []),
        "last_synced_source_stamp": last_synced_source_stamp,
        "last_synced_wotc_standard_sets": last_synced_wotc_sets,
        "wotc_standard_gate_available": bool(wotc_standard_sets),
        "wotc_standard_gate_error": wotc_error,
        "last_decision_reason": reason,
        "last_decision_synced": synced,
        "last_decision_manual_trigger": manual_trigger,
        "last_successful_sync_at": last_successful_sync_at,
        "last_successful_manual_sync_at": last_successful_manual_sync_at,
        "last_sync_generated_at": last_sync_generated_at,
        "source_download_url": source_download_url,
    }

    latest_catalog = latest_catalog_json_path(
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )
    latest_lookup = output_dir / f"{catalog_stem(format_key=format_key, bulk_type=bulk_type)}-latest-arena-lookup.json"
    latest_csv = output_dir / f"{catalog_stem(format_key=format_key, bulk_type=bulk_type)}-latest.csv"
    latest_raw = latest_raw_source_path(bulk_type=bulk_type, output_dir=output_dir)

    if sync_result is not None:
        state_payload["latest_catalog_json_path"] = str(sync_result.catalog_json_path)
        state_payload["latest_arena_lookup_json_path"] = str(sync_result.arena_lookup_json_path)
        state_payload["latest_csv_path"] = str(sync_result.csv_path)
        state_payload["latest_raw_source_path"] = str(sync_result.bulk_file_path)
    else:
        if latest_catalog.exists():
            state_payload["latest_catalog_json_path"] = str(latest_catalog)
        if latest_lookup.exists():
            state_payload["latest_arena_lookup_json_path"] = str(latest_lookup)
        if latest_csv.exists():
            state_payload["latest_csv_path"] = str(latest_csv)
        if latest_raw.exists():
            state_payload["latest_raw_source_path"] = str(latest_raw)

    path = write_sync_state(state_payload, output_dir, format_key=format_key, bulk_type=bulk_type)
    if sync_result is not None:
        append_sync_history(
            {
                "recorded_at": checked_at,
                "format": format_key,
                "bulk_type": bulk_type,
                "manual_trigger": manual_trigger,
                "reason": reason,
                "source_stamp": source_stamp,
                "generated_at": sync_result.generated_at,
                "source_download_url": sync_result.source_download_url,
                "latest_catalog_json_path": str(sync_result.catalog_json_path),
                "latest_arena_lookup_json_path": str(sync_result.arena_lookup_json_path),
                "latest_csv_path": str(sync_result.csv_path),
                "latest_raw_source_path": str(sync_result.bulk_file_path),
                "total_cards": sync_result.total_cards,
            },
            output_dir=output_dir,
        )
    return path


def append_sync_history(entry: dict[str, Any], *, output_dir: Path = ORACLE_DATA_ROOT) -> Path:
    path = sync_history_path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def maybe_sync_card_catalog(
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    keep_download: bool = False,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> CatalogAutoSyncDecision:
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    checked_at = datetime.now(UTC).isoformat()
    state = load_sync_state(output_dir, format_key=format_key, bulk_type=bulk_type)
    state_path_value = sync_state_path(output_dir, format_key=format_key, bulk_type=bulk_type)

    preferred_lookup_stem = catalog_stem(format_key=format_key, bulk_type=bulk_type)
    preferred_lookup_path = output_dir / f"{preferred_lookup_stem}-latest-arena-lookup.json"
    latest_lookup_exists = preferred_lookup_path.exists()

    try:
        wotc_standard_sets: list[str] = []
        wotc_error = ""
        if format_key == "standard":
            try:
                wotc_standard_sets = fetch_wotc_standard_set_names(session)
            except Exception as exc:
                wotc_error = str(exc)

        bulk_item = get_bulk_item(session, bulk_type)
        source_stamp = source_stamp_from_bulk_item(bulk_item)
        last_synced_source_stamp = str(state.get("last_synced_source_stamp", "")).strip()
        last_synced_wotc_sets = list(state.get("last_synced_wotc_standard_sets") or [])
        wotc_changed_since_sync = bool(wotc_standard_sets) and wotc_standard_sets != last_synced_wotc_sets

        should_sync = False
        reason = ""
        if not latest_lookup_exists:
            should_sync = True
            reason = "local latest Arena lookup is missing"
        elif source_stamp == last_synced_source_stamp:
            if wotc_changed_since_sync:
                reason = "WotC Standard list changed, but Scryfall bulk source has not changed yet"
            else:
                reason = "Scryfall bulk source stamp is unchanged"
        elif format_key != "standard":
            should_sync = True
            reason = "Scryfall bulk source changed"
        elif not wotc_standard_sets:
            should_sync = True
            reason = "Scryfall bulk source changed and no live WotC Standard gate was available"
        elif wotc_changed_since_sync:
            should_sync = True
            reason = "Scryfall bulk source changed after the live WotC Standard set list changed"
        else:
            reason = "Scryfall bulk source changed, but the live WotC Standard set list is unchanged"

        sync_result: CatalogSyncResult | None = None
        if should_sync:
            sync_result = sync_card_catalog(
                format_key=format_key,
                bulk_type=bulk_type,
                keep_download=keep_download,
                session=session,
                bulk_item=bulk_item,
                output_dir=output_dir,
            )
            last_synced_source_stamp = source_stamp
            if wotc_standard_sets:
                last_synced_wotc_sets = list(wotc_standard_sets)

        update_sync_state(
            format_key=format_key,
            bulk_type=bulk_type,
            checked_at=checked_at,
            source_stamp=source_stamp,
            reason=reason,
            synced=should_sync,
            manual_trigger=False,
            output_dir=output_dir,
            wotc_standard_sets=wotc_standard_sets,
            wotc_error=wotc_error,
            sync_result=sync_result,
        )
        return CatalogAutoSyncDecision(
            checked_at=checked_at,
            format_key=format_key,
            bulk_type=bulk_type,
            synced=should_sync,
            reason=reason,
            source_stamp=source_stamp,
            wotc_standard_sets=list(wotc_standard_sets),
            wotc_standard_sets_changed_since_sync=wotc_changed_since_sync,
            state_path=state_path_value,
            sync_result=sync_result,
        )
    finally:
        session.close()


def get_bulk_item(session: requests.Session, bulk_type: str) -> dict[str, Any]:
    response = session.get(BULK_INDEX_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    items = payload.get("data") or []
    for item in items:
        if item.get("type") == bulk_type:
            return item
    available = ", ".join(sorted(str(item.get("type")) for item in items))
    raise ValueError(f"Bulk type '{bulk_type}' not found. Available types: {available}")


def download_bulk_file(
    session: requests.Session,
    bulk_item: dict[str, Any],
    download_dir: Path,
) -> Path:
    download_dir.mkdir(parents=True, exist_ok=True)
    download_url = str(bulk_item["download_uri"])
    filename = Path(urlparse(download_url).path).name
    target_path = download_dir / filename
    if target_path.exists() and target_path.stat().st_size > 0:
        return target_path

    with session.get(download_url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with target_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    handle.write(chunk)
    return target_path


def retain_latest_raw_source(
    *,
    bulk_path: Path,
    bulk_type: str,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = latest_raw_source_path(bulk_type=bulk_type, output_dir=output_dir)
    with bulk_path.open("rb") as source_handle, gzip.open(target_path, "wb") as target_handle:
        shutil.copyfileobj(source_handle, target_handle)
    return target_path


def build_catalog_from_bulk_file(
    bulk_path: Path,
    format_key: str,
    bulk_item: dict[str, Any],
) -> dict[str, Any]:
    cards_by_arena_id: dict[str, dict[str, Any]] = {}
    for card in iter_bulk_cards(bulk_path):
        if not is_relevant_card(card, format_key):
            continue
        reduced = reduce_card(card)
        cards_by_arena_id[str(reduced["arena_id"])] = reduced

    cards = sorted(cards_by_arena_id.values(), key=lambda item: (item["name"], item["set"], item["collector_number"]))
    generated_at = datetime.now(UTC).isoformat()
    return {
        "object": "manasight_card_catalog",
        "generated_at": generated_at,
        "format": format_key,
        "bulk_type": bulk_item.get("type", ""),
        "bulk_updated_at": bulk_item.get("updated_at", ""),
        "source_download_url": bulk_item.get("download_uri", ""),
        "total_cards": len(cards),
        "cards": cards,
        "cards_by_arena_id": cards_by_arena_id,
    }


def iter_bulk_cards(path: Path) -> Iterator[dict[str, Any]]:
    decoder = json.JSONDecoder()
    with path.open("r", encoding="utf-8") as handle:
        buffer = ""
        saw_array_start = False

        while True:
            if not saw_array_start:
                chunk = handle.read(STREAM_CHUNK_SIZE)
                if not chunk:
                    return
                buffer += chunk
                stripped = buffer.lstrip()
                if not stripped:
                    continue
                if stripped[0] != "[":
                    raise ValueError("Expected Scryfall bulk file to begin with a JSON array.")
                buffer = stripped[1:]
                saw_array_start = True

            buffer = buffer.lstrip()
            if buffer.startswith("]"):
                return
            if buffer.startswith(","):
                buffer = buffer[1:]
                continue

            try:
                card, end_index = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                chunk = handle.read(STREAM_CHUNK_SIZE)
                if not chunk:
                    raise
                buffer += chunk
                continue

            if not isinstance(card, dict):
                raise ValueError("Expected each bulk-data entry to be a JSON object.")
            yield card
            buffer = buffer[end_index:]


def is_relevant_card(card: dict[str, Any], format_key: str) -> bool:
    games = card.get("games") or []
    if "arena" not in games:
        return False
    if card.get("arena_id") in (None, ""):
        return False
    if format_key in ALL_ARENA_FORMAT_KEYS:
        return True
    legalities = card.get("legalities") or {}
    return legalities.get(format_key) == "legal"


def reduce_card(card: dict[str, Any]) -> dict[str, Any]:
    reduced_card_faces = [reduce_card_face(face) for face in (card.get("card_faces") or [])]
    reduced = {
        "arena_id": card.get("arena_id"),
        "oracle_id": card.get("oracle_id"),
        "scryfall_id": card.get("id"),
        "name": card.get("name", ""),
        "rarity": card.get("rarity", ""),
        "set": card.get("set", ""),
        "set_name": card.get("set_name", ""),
        "collector_number": card.get("collector_number", ""),
        "released_at": card.get("released_at", ""),
        "layout": card.get("layout", ""),
        "mana_cost": card.get("mana_cost", ""),
        "cmc": card.get("cmc"),
        "type_line": card.get("type_line", ""),
        "oracle_text": card.get("oracle_text", ""),
        "colors": card.get("colors") or [],
        "color_identity": card.get("color_identity") or [],
        "color_indicator": card.get("color_indicator") or [],
        "keywords": card.get("keywords") or [],
        "power": card.get("power", ""),
        "toughness": card.get("toughness", ""),
        "loyalty": card.get("loyalty", ""),
        "defense": card.get("defense", ""),
        "produced_mana": card.get("produced_mana") or [],
        "games": card.get("games") or [],
        "card_faces": reduced_card_faces,
    }
    reduced["parser_fingerprint"] = build_parser_fingerprint(reduced)
    return reduced


def reduce_card_face(face: dict[str, Any]) -> dict[str, Any]:
    reduced: dict[str, Any] = {}
    for field in CARD_FACE_FIELDS:
        value = face.get(field)
        if value in (None, "", []):
            continue
        reduced[field] = value
    color_indicator = face.get("color_indicator")
    if color_indicator not in (None, "", []):
        reduced["color_indicator"] = color_indicator
    reduced["parser_fingerprint"] = build_parser_fingerprint(reduced)
    return reduced


def _normalize_text_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    normalized: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def _normalize_color_names(values: Any) -> list[str]:
    normalized: list[str] = []
    for value in _normalize_text_list(values):
        upper_value = value.upper()
        color_name = MANA_SYMBOL_TO_COLOR.get(upper_value, value.replace("CardColor_", ""))
        if color_name and color_name not in normalized:
            normalized.append(color_name)
    return normalized


def _face_names(card_faces: Any) -> list[str]:
    if not isinstance(card_faces, list):
        return []
    face_names: list[str] = []
    for face in card_faces:
        if not isinstance(face, dict):
            continue
        name = str(face.get("name", "")).strip()
        if name and name not in face_names:
            face_names.append(name)
    return face_names


def _normalize_type_line(type_line: Any) -> str:
    return (
        str(type_line or "")
        .replace("â€”", "—")
        .replace("Ã¢â‚¬â€", "—")
        .replace("â€“", "—")
        .strip()
    )


def _split_type_line(type_line: Any) -> tuple[list[str], list[str], list[str]]:
    normalized = _normalize_type_line(type_line).replace("—", "-")
    left, right = normalized, ""
    if "-" in normalized:
        left, right = normalized.split("-", 1)
    left_tokens = {token.strip() for token in left.split() if token.strip()}
    right_tokens = {token.strip() for token in right.split() if token.strip()}
    super_types = sorted(left_tokens & SUPER_TYPE_NAMES)
    card_types = sorted(left_tokens & CARD_TYPE_NAMES)
    subtypes = sorted(right_tokens)
    return super_types, card_types, subtypes


def _mana_cost_signature(mana_cost: Any) -> str:
    mana_cost_text = str(mana_cost or "").strip()
    if not mana_cost_text:
        return ""

    color_counts: dict[str, int] = {}
    colorless_total = 0
    for token in MANA_TOKEN_RE.findall(mana_cost_text):
        token = token.strip().upper()
        if not token:
            continue
        if token.isdigit():
            colorless_total += int(token)
            continue
        if token in MANA_SYMBOL_TO_COLOR:
            color_name = MANA_SYMBOL_TO_COLOR[token]
            color_counts[color_name] = color_counts.get(color_name, 0) + 1
            continue
        hybrid_parts = [part for part in token.split("/") if part in MANA_SYMBOL_TO_COLOR]
        if hybrid_parts:
            for part in hybrid_parts:
                color_name = MANA_SYMBOL_TO_COLOR[part]
                color_counts[color_name] = color_counts.get(color_name, 0) + 1
            continue
        colorless_total += 1

    parts: list[str] = []
    for color_name in sorted(color_counts):
        parts.append(f"{color_counts[color_name]}x{color_name}")
    if colorless_total > 0:
        parts.append(f"{colorless_total}xColorless")
    return " + ".join(parts)


def build_parser_fingerprint(card_like: dict[str, Any]) -> dict[str, Any]:
    normalized_type_line = _normalize_type_line(card_like.get("type_line"))
    super_types, card_types, subtypes = _split_type_line(normalized_type_line)
    return {
        "name": str(card_like.get("name", "")).strip(),
        "layout": str(card_like.get("layout", "")).strip(),
        "face_names": _face_names(card_like.get("card_faces")),
        "games": _normalize_text_list(card_like.get("games")),
        "mana_cost": str(card_like.get("mana_cost", "")).strip(),
        "mana_cost_signature": _mana_cost_signature(card_like.get("mana_cost")),
        "cmc": card_like.get("cmc"),
        "type_line": normalized_type_line,
        "super_types": super_types,
        "card_types": card_types,
        "subtypes": subtypes,
        "colors": _normalize_color_names(card_like.get("colors")),
        "color_identity": _normalize_color_names(card_like.get("color_identity")),
        "color_indicator": _normalize_color_names(card_like.get("color_indicator")),
        "keywords": _normalize_text_list(card_like.get("keywords")),
        "oracle_text": str(card_like.get("oracle_text", "")).strip(),
        "power": str(card_like.get("power", "")).strip(),
        "toughness": str(card_like.get("toughness", "")).strip(),
        "loyalty": str(card_like.get("loyalty", "")).strip(),
        "defense": str(card_like.get("defense", "")).strip(),
        "produced_mana": _normalize_color_names(card_like.get("produced_mana")),
    }


def _prune_old_catalog_outputs(output_dir: Path, *, stem: str) -> None:
    keep_names = {
        f"{stem}-latest.json",
        f"{stem}-latest-arena-lookup.json",
        f"{stem}-latest.csv",
    }
    for pattern in (f"{stem}-*.json", f"{stem}-*-arena-lookup.json", f"{stem}-*.csv"):
        for path in output_dir.glob(pattern):
            if path.name in keep_names:
                continue
            path.unlink(missing_ok=True)


def write_catalog_outputs(
    catalog: dict[str, Any],
    output_dir: Path,
    *,
    raw_source_path: Path,
) -> CatalogSyncResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    format_key = str(catalog["format"])
    bulk_type = str(catalog["bulk_type"])
    stem = f"scryfall-{bulk_type}-{format_key}"
    latest_catalog_json_path = output_dir / f"{stem}-latest.json"
    latest_arena_lookup_json_path = output_dir / f"{stem}-latest-arena-lookup.json"
    latest_csv_path = output_dir / f"{stem}-latest.csv"
    _prune_old_catalog_outputs(output_dir, stem=stem)

    catalog_payload = {
        key: value
        for key, value in catalog.items()
        if key != "cards_by_arena_id"
    }
    lookup_payload = {
        "object": "manasight_card_lookup",
        "generated_at": catalog["generated_at"],
        "format": format_key,
        "bulk_type": bulk_type,
        "bulk_updated_at": catalog["bulk_updated_at"],
        "source_download_url": catalog["source_download_url"],
        "total_cards": catalog["total_cards"],
        "cards_by_arena_id": catalog["cards_by_arena_id"],
    }

    catalog_json_text = json.dumps(catalog_payload, indent=2, ensure_ascii=False)
    lookup_json_text = json.dumps(lookup_payload, indent=2, ensure_ascii=False)
    latest_catalog_json_path.write_text(catalog_json_text, encoding="utf-8")
    latest_arena_lookup_json_path.write_text(lookup_json_text, encoding="utf-8")

    write_catalog_csv(latest_csv_path, catalog["cards"])

    return CatalogSyncResult(
        format_key=format_key,
        bulk_type=bulk_type,
        source_download_url=str(catalog["source_download_url"]),
        bulk_file_path=raw_source_path,
        catalog_json_path=latest_catalog_json_path,
        arena_lookup_json_path=latest_arena_lookup_json_path,
        csv_path=latest_csv_path,
        total_cards=int(catalog["total_cards"]),
        generated_at=str(catalog["generated_at"]),
    )


def write_catalog_csv(path: Path, cards: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for card in cards:
            row = {
                "arena_id": card.get("arena_id", ""),
                "oracle_id": card.get("oracle_id", ""),
                "scryfall_id": card.get("scryfall_id", ""),
                "name": card.get("name", ""),
                "rarity": card.get("rarity", ""),
                "set": card.get("set", ""),
                "set_name": card.get("set_name", ""),
                "collector_number": card.get("collector_number", ""),
                "released_at": card.get("released_at", ""),
                "layout": card.get("layout", ""),
                "mana_cost": card.get("mana_cost", ""),
                "cmc": card.get("cmc", ""),
                "type_line": card.get("type_line", ""),
                "oracle_text": card.get("oracle_text", ""),
                "colors": " ".join(card.get("colors") or []),
                "color_identity": " ".join(card.get("color_identity") or []),
                "keywords": " | ".join(card.get("keywords") or []),
                "produced_mana": " ".join(card.get("produced_mana") or []),
                "games": " ".join(card.get("games") or []),
                "card_faces_json": json.dumps(card.get("card_faces") or [], ensure_ascii=False),
            }
            writer.writerow(cast(Any, row))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a compact Arena-aware Scryfall card catalog for Mythic Edge.")
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        help="Scryfall legality key to keep. Use 'arena' to keep all Arena cards, or a format like 'standard'.",
    )
    parser.add_argument(
        "--bulk-type",
        default=DEFAULT_BULK_TYPE,
        help="Scryfall bulk-data type to download. default_cards is recommended for Arena integration.",
    )
    parser.add_argument(
        "--keep-download",
        action="store_true",
        help=(
            "Also keep the temporary downloaded JSON under data/oracle_data/_downloads "
            "after the latest raw source is compressed."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    result = sync_card_catalog(
        format_key=args.format.strip().lower() or DEFAULT_FORMAT,
        bulk_type=args.bulk_type.strip() or DEFAULT_BULK_TYPE,
        keep_download=args.keep_download,
    )
    print(result.summary_line())
    print(f"Arena lookup: {result.arena_lookup_json_path}")
    print(f"CSV export:   {result.csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
