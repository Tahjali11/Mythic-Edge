"""Compare observed MTGA grpIds against the Arena-aware Scryfall lookup.

Bridge note:
- gameplay observations come from MTGA `grpId` or `overlayGrpId` fields
- the external source of truth is Scryfall's `arena_id`

Many MTGA grpIds numerically match Arena IDs, but not all do. Public result field
names in this module still use `arena_id` for compatibility with older reports,
tests, and CLI output. Internally, treat these values as observed grpIds until
the lookup confirms an exact numeric match.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .card_catalog import (
    DEFAULT_BULK_TYPE,
    DEFAULT_FORMAT,
    ensure_grp_id_overrides_file,
    load_arena_lookup,
    load_combined_card_lookup,
    load_grp_id_overrides,
    maybe_sync_card_catalog,
)
from .config import MATCH_LOGS_ROOT, ORACLE_DATA_ROOT
from .extractors import (
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_turn_info,
)


@dataclass(slots=True)
class UnmatchedArenaSample:
    arena_id: int
    count: int
    file: str
    match_id: str
    game_number: Any
    turn_number: Any
    instance_id: Any
    zone_id: Any
    owner_seat_id: Any


@dataclass(slots=True)
class ArenaIdValidationResult:
    generated_at: str
    format_key: str
    scryfall_lookup_total_cards: int
    grp_id_override_total_cards: int
    lookup_total_cards: int
    scanned_files: int
    total_observations: int
    distinct_arena_ids: int
    matched_observations: int
    unmatched_observations: int
    matched_distinct_arena_ids: int
    unmatched_distinct_arena_ids: int
    top_matched_cards: list[dict[str, Any]]
    unmatched_samples: list[UnmatchedArenaSample]
    override_file_path: Path | None = None
    report_path: Path | None = None

    def summary_line(self) -> str:
        return (
            f"Arena ID validation: {self.matched_distinct_arena_ids}/{self.distinct_arena_ids} distinct ids matched "
            f"({self.matched_observations}/{self.total_observations} observations)"
        )


@dataclass(slots=True)
class GrpIdOverrideRefreshResult:
    generated_at: str
    format_key: str
    override_file_path: Path
    total_override_entries: int
    added_stub_count: int
    unresolved_distinct_arena_ids: int
    fingerprint_report_path: Path | None = None
    fingerprint_markdown_path: Path | None = None

    def summary_line(self) -> str:
        return (
            f"grpId overrides refreshed: {self.total_override_entries} total entries, "
            f"{self.added_stub_count} new unresolved stubs"
        )


@dataclass(slots=True)
class ArenaIdEvidence:
    count: int = 0
    first_sample: UnmatchedArenaSample | None = None
    zones_seen: Counter[str] = field(default_factory=Counter)
    owner_seat_counts: Counter[str] = field(default_factory=Counter)
    local_private_hand_observations: int = 0
    opening_hand_observations: int = 0
    opening_hand_cooccurrences: Counter[str] = field(default_factory=Counter)
    observed_name_keys: Counter[str] = field(default_factory=Counter)
    overlay_grp_ids_seen: Counter[str] = field(default_factory=Counter)
    super_types_seen: Counter[str] = field(default_factory=Counter)
    card_types_seen: Counter[str] = field(default_factory=Counter)
    subtypes_seen: Counter[str] = field(default_factory=Counter)
    colors_seen: Counter[str] = field(default_factory=Counter)
    power_values_seen: Counter[str] = field(default_factory=Counter)
    toughness_values_seen: Counter[str] = field(default_factory=Counter)
    action_types_seen: Counter[str] = field(default_factory=Counter)
    mana_cost_signatures_seen: Counter[str] = field(default_factory=Counter)
    unique_ability_grp_ids_seen: Counter[str] = field(default_factory=Counter)
    sample_match_ids: list[str] = field(default_factory=list)
    sample_files: list[str] = field(default_factory=list)
    distinct_game_keys: set[tuple[str, Any]] = field(default_factory=set, repr=False)

    def note_general_observation(
        self,
        *,
        file: str,
        match_id: str,
        game_number: Any,
        zone_label: str,
        owner_seat_label: str,
        sample: UnmatchedArenaSample,
    ) -> None:
        self.count += 1
        if self.first_sample is None:
            self.first_sample = sample
        self.zones_seen[zone_label] += 1
        self.owner_seat_counts[owner_seat_label] += 1
        if match_id:
            _append_unique_limited(self.sample_match_ids, match_id)
        _append_unique_limited(self.sample_files, file, limit=3)
        if match_id or game_number not in (None, ""):
            self.distinct_game_keys.add((match_id, game_number))

    def note_local_private_hand(self, *, opening_hand: bool) -> None:
        self.local_private_hand_observations += 1
        if opening_hand:
            self.opening_hand_observations += 1

    def note_opening_hand_cooccurrences(self, card_names: list[str]) -> None:
        for card_name in sorted(set(card_names)):
            self.opening_hand_cooccurrences[card_name] += 1

    def note_object_fingerprint(
        self,
        game_object: dict[str, Any],
        *,
        actions: list[dict[str, Any]],
    ) -> None:
        name_key = game_object.get("name")
        if name_key not in (None, ""):
            self.observed_name_keys[str(name_key)] += 1

        overlay_grp_id = game_object.get("overlayGrpId")
        if overlay_grp_id not in (None, ""):
            self.overlay_grp_ids_seen[str(overlay_grp_id)] += 1

        for value in game_object.get("superTypes") or []:
            self.super_types_seen[str(value)] += 1
        for value in game_object.get("cardTypes") or []:
            self.card_types_seen[str(value)] += 1
        for value in game_object.get("subtypes") or []:
            self.subtypes_seen[str(value)] += 1
        for value in game_object.get("color") or []:
            self.colors_seen[str(value)] += 1

        power_value = ((game_object.get("power") or {}).get("value"))
        if power_value not in (None, ""):
            self.power_values_seen[str(power_value)] += 1
        toughness_value = ((game_object.get("toughness") or {}).get("value"))
        if toughness_value not in (None, ""):
            self.toughness_values_seen[str(toughness_value)] += 1

        for ability in game_object.get("uniqueAbilities") or []:
            if not isinstance(ability, dict):
                continue
            grp_id = ability.get("grpId")
            if grp_id not in (None, ""):
                self.unique_ability_grp_ids_seen[str(grp_id)] += 1

        for action in actions:
            if not isinstance(action, dict):
                continue
            action_type = str(action.get("actionType", "")).strip()
            if action_type:
                self.action_types_seen[action_type] += 1
            mana_signature = _mana_cost_signature(action.get("manaCost") or [])
            if mana_signature:
                self.mana_cost_signatures_seen[mana_signature] += 1


def _append_unique_limited(values: list[str], value: str, *, limit: int = 5) -> None:
    text = str(value or "").strip()
    if not text or text in values or len(values) >= limit:
        return
    values.append(text)


def _counter_to_sorted_dict(counter: Counter[str]) -> dict[str, int]:
    ordered: dict[str, int] = {}
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        ordered[key] = count
    return ordered


def _top_name_counts(counter: Counter[str], *, limit: int = 10) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, count in counter.most_common(limit):
        rows.append({"name": name, "count": count})
    return rows


def _top_value_counts(counter: Counter[str], *, limit: int = 10, key_name: str = "value") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for value, count in counter.most_common(limit):
        rows.append({key_name: value, "count": count})
    return rows


def _fingerprint_summary(evidence: ArenaIdEvidence) -> dict[str, list[dict[str, Any]]]:
    return {
        "observed_name_keys": _top_value_counts(evidence.observed_name_keys, key_name="name_key"),
        "overlay_grp_ids_seen": _top_value_counts(evidence.overlay_grp_ids_seen, key_name="overlay_grp_id"),
        "super_types_seen": _top_value_counts(evidence.super_types_seen, key_name="super_type"),
        "card_types_seen": _top_value_counts(evidence.card_types_seen, key_name="card_type"),
        "subtypes_seen": _top_value_counts(evidence.subtypes_seen, key_name="subtype"),
        "colors_seen": _top_value_counts(evidence.colors_seen, key_name="color"),
        "power_values_seen": _top_value_counts(evidence.power_values_seen, key_name="power"),
        "toughness_values_seen": _top_value_counts(evidence.toughness_values_seen, key_name="toughness"),
        "action_types_seen": _top_value_counts(evidence.action_types_seen, key_name="action_type"),
        "mana_cost_signatures_seen": _top_value_counts(
            evidence.mana_cost_signatures_seen,
            key_name="mana_cost_signature",
        ),
        "unique_ability_grp_ids_seen": _top_value_counts(
            evidence.unique_ability_grp_ids_seen,
            key_name="ability_grp_id",
        ),
    }


def _fingerprint_report_entry(
    observed_grp_id: int,
    evidence: ArenaIdEvidence,
    override_entry: dict[str, Any],
) -> dict[str, Any]:
    sample = evidence.first_sample
    return {
        "grp_id": observed_grp_id,
        "current_name": str(override_entry.get("name", "")).strip(),
        "name_source": str(override_entry.get("name_source", "")).strip(),
        "heuristic_role": _heuristic_role(evidence),
        "observations": evidence.count,
        "distinct_games_seen": len(evidence.distinct_game_keys),
        "local_private_hand_observations": evidence.local_private_hand_observations,
        "opening_hand_observations": evidence.opening_hand_observations,
        "sample_match_ids": list(evidence.sample_match_ids),
        "sample_files": list(evidence.sample_files),
        "top_opening_hand_cooccurrences": _top_name_counts(evidence.opening_hand_cooccurrences),
        "zones_seen": _counter_to_sorted_dict(evidence.zones_seen),
        "owner_seat_counts": _counter_to_sorted_dict(evidence.owner_seat_counts),
        "sample": {
            "match_id": sample.match_id if sample is not None else "",
            "game_number": sample.game_number if sample is not None else "",
            "turn_number": sample.turn_number if sample is not None else "",
            "instance_id": sample.instance_id if sample is not None else "",
            "zone_id": sample.zone_id if sample is not None else "",
            "owner_seat_id": sample.owner_seat_id if sample is not None else "",
            "file": sample.file if sample is not None else "",
        },
        "fingerprint": _fingerprint_summary(evidence),
    }


def write_fingerprint_report(
    *,
    generated_at: str,
    format_key: str,
    output_dir: Path,
    override_path: Path,
    entries: list[dict[str, Any]],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"arena-id-fingerprints-{format_key}-latest.json"
    markdown_path = output_dir / f"arena-id-fingerprints-{format_key}-latest.md"

    payload = {
        "object": "manasight_arena_id_fingerprint_report",
        "generated_at": generated_at,
        "format": format_key,
        "override_file_path": str(override_path),
        "entry_count": len(entries),
        "entries": entries,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"# Arena ID Fingerprint Report ({format_key})",
        "",
        f"- Generated At: `{generated_at}`",
        f"- Override File: `{override_path}`",
        f"- Entry Count: `{len(entries)}`",
        "",
    ]
    for entry in entries:
        current_name = entry.get("current_name") or "unresolved"
        lines.extend(
            [
                f"## grpId {entry['grp_id']}",
                "",
                f"- Current Name: `{current_name}`",
                f"- Name Source: `{entry.get('name_source') or 'unassigned'}`",
                f"- Heuristic Role: `{entry['heuristic_role']}`",
                f"- Observations: `{entry['observations']}`",
                f"- Distinct Games: `{entry['distinct_games_seen']}`",
                f"- Local Private Hand Observations: `{entry['local_private_hand_observations']}`",
                f"- Opening Hand Observations: `{entry['opening_hand_observations']}`",
            ]
        )
        sample_match_ids = entry.get("sample_match_ids") or []
        if sample_match_ids:
            lines.append(f"- Sample Match IDs: `{', '.join(sample_match_ids)}`")
        top_cooccurrences = entry.get("top_opening_hand_cooccurrences") or []
        if top_cooccurrences:
            rendered = ", ".join(f"{row['name']} ({row['count']})" for row in top_cooccurrences)
            lines.append(f"- Top Opening-Hand Cooccurrences: `{rendered}`")
        sample = entry.get("sample") or {}
        if sample.get("match_id"):
            lines.append(
                "- Sample: "
                f"`match={sample.get('match_id')} game={sample.get('game_number')} "
                f"turn={sample.get('turn_number')} instance={sample.get('instance_id')}`"
            )

        fingerprint = entry.get("fingerprint") or {}
        for payload_key, label, value_key in (
            ("observed_name_keys", "Observed Name Keys", "name_key"),
            ("overlay_grp_ids_seen", "Overlay grpIds", "overlay_grp_id"),
            ("super_types_seen", "Super Types", "super_type"),
            ("card_types_seen", "Card Types", "card_type"),
            ("subtypes_seen", "Subtypes", "subtype"),
            ("colors_seen", "Colors", "color"),
            ("power_values_seen", "Power Values", "power"),
            ("toughness_values_seen", "Toughness Values", "toughness"),
            ("action_types_seen", "Action Types", "action_type"),
            ("mana_cost_signatures_seen", "Mana Cost Signatures", "mana_cost_signature"),
            ("unique_ability_grp_ids_seen", "Unique Ability grpIds", "ability_grp_id"),
        ):
            rows = fingerprint.get(payload_key) or []
            if not rows:
                continue
            rendered = ", ".join(f"{row[value_key]} ({row['count']})" for row in rows)
            lines.append(f"- {label}: `{rendered}`")

        lines.append("")

    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return json_path, markdown_path


def _owner_seat_label(owner_seat: Any, local_seat: Any) -> str:
    owner_text = str(owner_seat or "").strip()
    if not owner_text:
        return "unknown"
    local_text = str(local_seat or "").strip()
    if local_text and owner_text == local_text:
        return "local"
    if local_text:
        return "opponent"
    return owner_text


def _zone_labels_by_id(gsm: dict[str, Any], local_seat: Any) -> dict[int, str]:
    zones = gsm.get("zones")
    if not isinstance(zones, list):
        return {}

    labels: dict[int, str] = {}
    for zone in zones:
        if not isinstance(zone, dict):
            continue
        zone_id = zone.get("zoneId")
        try:
            normalized_zone_id = int(zone_id)
        except (TypeError, ValueError):
            continue

        zone_type = str(zone.get("type") or "UnknownZone").strip()
        visibility = str(zone.get("visibility") or "UnknownVisibility").strip()
        owner_label = _owner_seat_label(zone.get("ownerSeatId"), local_seat)
        labels[normalized_zone_id] = f"{zone_type}|{visibility}|{owner_label}"
    return labels


def _heuristic_role(evidence: ArenaIdEvidence) -> str:
    if evidence.opening_hand_observations > 0:
        return "opening_hand_relevant"
    if evidence.local_private_hand_observations > 0:
        return "private_zone_relevant"
    if any(label.startswith("ZoneType_Battlefield") for label in evidence.zones_seen):
        return "public_card_relevant"
    return "support_or_unknown"


def _actions_by_instance_id(gsm: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
    mapped: dict[int, list[dict[str, Any]]] = {}
    for wrapped in gsm.get("actions") or []:
        if not isinstance(wrapped, dict):
            continue
        action = wrapped.get("action")
        if not isinstance(action, dict):
            continue
        instance_id = action.get("instanceId")
        try:
            normalized_instance_id = int(instance_id)
        except (TypeError, ValueError):
            continue
        mapped.setdefault(normalized_instance_id, []).append(action)
    return mapped


def _mana_cost_signature(mana_cost: list[Any]) -> str:
    parts: list[str] = []
    for raw_part in mana_cost:
        if not isinstance(raw_part, dict):
            continue
        try:
            count = int(raw_part.get("count", 0) or 0)
        except (TypeError, ValueError):
            count = 0
        colors = [str(color).replace("ManaColor_", "") for color in (raw_part.get("color") or []) if str(color)]
        label = "/".join(sorted(colors)) if colors else "Colorless"
        if count > 0:
            parts.append(f"{count}x{label}")
    return " + ".join(parts)


def _scan_saved_match_logs(
    match_logs_root: Path,
    *,
    resolved_lookup: dict[str, dict[str, Any]] | None = None,
    target_grp_ids: set[int] | None = None,
) -> tuple[int, dict[int, ArenaIdEvidence]]:
    evidence_by_observed_grp_id: dict[int, ArenaIdEvidence] = {}
    scanned_files = 0
    seen_local_hand_snapshots: set[tuple[str, str, Any, tuple[int, ...]]] = set()
    normalized_target_grp_ids = {int(grp_id) for grp_id in (target_grp_ids or set())}

    for path in sorted(match_logs_root.rglob("*.jsonl")):
        scanned_files += 1
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if row.get("kind") != "GameState":
                    continue

                payload = row.get("payload") or {}
                raw = payload.get("raw_game_state") or {}
                if not isinstance(raw, dict):
                    continue
                gsm = raw.get("gameStateMessage") or {}
                if not isinstance(gsm, dict):
                    continue

                match_id, game_number, turn_number, _, _, _, _ = _extract_turn_info(payload)
                match_id = str(match_id or (row.get("derived") or {}).get("match_id") or "")
                if game_number in (None, ""):
                    game_number = (row.get("derived") or {}).get("game_number")

                system_seat_ids = raw.get("systemSeatIds") or []
                local_seat = system_seat_ids[0] if isinstance(system_seat_ids, list) and system_seat_ids else None
                zone_labels = _zone_labels_by_id(gsm, local_seat)
                instance_grp_lookup = _extract_instance_grp_lookup(payload)
                local_hand_instance_ids = _extract_local_private_hand_instance_ids(payload)
                actions_by_instance_id = _actions_by_instance_id(gsm)

                if local_hand_instance_ids:
                    snapshot_key = (
                        str(path),
                        match_id,
                        game_number,
                        tuple(sorted(local_hand_instance_ids)),
                    )
                    if snapshot_key not in seen_local_hand_snapshots:
                        seen_local_hand_snapshots.add(snapshot_key)
                        opening_hand = turn_number == 1 and 4 <= len(local_hand_instance_ids) <= 7
                        resolved_names: list[str] = []
                        unresolved_grp_ids: list[int] = []

                        for instance_id in local_hand_instance_ids:
                            grp_id = instance_grp_lookup.get(instance_id)
                            if grp_id is None:
                                continue
                            should_track_grp_id = (
                                not normalized_target_grp_ids
                                or grp_id in normalized_target_grp_ids
                            )
                            if should_track_grp_id:
                                evidence = evidence_by_observed_grp_id.setdefault(
                                    grp_id,
                                    ArenaIdEvidence(),
                                )
                                evidence.note_local_private_hand(opening_hand=opening_hand)

                            card = resolved_lookup.get(str(grp_id)) if resolved_lookup else None
                            card_name = str(card.get("name", "")).strip() if isinstance(card, dict) else ""
                            if card_name:
                                resolved_names.append(card_name)
                            elif should_track_grp_id:
                                unresolved_grp_ids.append(grp_id)

                        if opening_hand and resolved_names:
                            for grp_id in unresolved_grp_ids:
                                evidence_by_observed_grp_id.setdefault(
                                    grp_id,
                                    ArenaIdEvidence(),
                                ).note_opening_hand_cooccurrences(
                                    resolved_names
                                )

                for game_object in gsm.get("gameObjects") or []:
                    if not isinstance(game_object, dict):
                        continue
                    observed_grp_id = game_object.get("grpId", game_object.get("overlayGrpId"))
                    try:
                        normalized_observed_grp_id = int(observed_grp_id)
                    except (TypeError, ValueError):
                        continue
                    if normalized_target_grp_ids and normalized_observed_grp_id not in normalized_target_grp_ids:
                        continue

                    zone_id = game_object.get("zoneId")
                    zone_label = f"zone:{zone_id}"
                    try:
                        normalized_zone_id = int(zone_id)
                    except (TypeError, ValueError):
                        normalized_zone_id = None
                    if normalized_zone_id is not None:
                        zone_label = zone_labels.get(normalized_zone_id, zone_label)

                    sample = UnmatchedArenaSample(
                        arena_id=normalized_observed_grp_id,
                        count=0,
                        file=str(path),
                        match_id=match_id,
                        game_number=game_number,
                        turn_number=turn_number,
                        instance_id=game_object.get("instanceId"),
                        zone_id=game_object.get("zoneId"),
                        owner_seat_id=game_object.get("ownerSeatId"),
                    )
                    evidence_by_observed_grp_id.setdefault(
                        normalized_observed_grp_id,
                        ArenaIdEvidence(),
                    ).note_general_observation(
                        file=str(path),
                        match_id=match_id,
                        game_number=game_number,
                        zone_label=zone_label,
                        owner_seat_label=_owner_seat_label(game_object.get("ownerSeatId"), local_seat),
                        sample=sample,
                    )
                    evidence_by_observed_grp_id.setdefault(
                        normalized_observed_grp_id,
                        ArenaIdEvidence(),
                    ).note_object_fingerprint(
                        game_object,
                        actions=actions_by_instance_id.get(int(game_object.get("instanceId") or -1), []),
                    )

    return scanned_files, evidence_by_observed_grp_id


def grp_ids_requiring_evidence_refresh(cards_by_grp_id: dict[str, Any]) -> set[int]:
    target_grp_ids: set[int] = set()
    for grp_id, raw_entry in cards_by_grp_id.items():
        if not isinstance(raw_entry, dict):
            continue
        try:
            normalized_grp_id = int(grp_id)
        except (TypeError, ValueError):
            continue
        current_name = str(raw_entry.get("name", "")).strip()
        if not current_name:
            target_grp_ids.add(normalized_grp_id)
    return target_grp_ids


def discover_unresolved_grp_ids_from_saved_logs(
    *,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    resolved_lookup: dict[str, dict[str, Any]],
) -> set[int]:
    unresolved_grp_ids: set[int] = set()

    for path in sorted(match_logs_root.rglob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if row.get("kind") != "GameState":
                    continue

                payload = row.get("payload") or {}
                raw = payload.get("raw_game_state") or {}
                if not isinstance(raw, dict):
                    continue
                gsm = raw.get("gameStateMessage") or {}
                if not isinstance(gsm, dict):
                    continue

                for game_object in gsm.get("gameObjects") or []:
                    if not isinstance(game_object, dict):
                        continue
                    observed_grp_id = game_object.get("grpId", game_object.get("overlayGrpId"))
                    try:
                        normalized_observed_grp_id = int(observed_grp_id)
                    except (TypeError, ValueError):
                        continue
                    if str(normalized_observed_grp_id) in resolved_lookup:
                        continue
                    unresolved_grp_ids.add(normalized_observed_grp_id)

    return unresolved_grp_ids


def validate_saved_match_logs(
    *,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    output_dir: Path = ORACLE_DATA_ROOT,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    max_unmatched_samples: int = 25,
) -> ArenaIdValidationResult:
    scryfall_lookup = load_arena_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    override_path = ensure_grp_id_overrides_file(output_dir=output_dir)
    named_overrides = load_grp_id_overrides(path=override_path, output_dir=output_dir)
    combined_lookup = load_combined_card_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    scanned_files, evidence_by_observed_grp_id = _scan_saved_match_logs(
        match_logs_root,
        resolved_lookup=combined_lookup,
    )
    matched_counts_by_observed_grp_id: dict[int, int] = {}
    unmatched_samples: list[UnmatchedArenaSample] = []

    for observed_grp_id, evidence in evidence_by_observed_grp_id.items():
        if str(observed_grp_id) in combined_lookup:
            matched_counts_by_observed_grp_id[observed_grp_id] = evidence.count
            continue
        if len(unmatched_samples) >= max_unmatched_samples:
            continue
        sample = evidence.first_sample
        if sample is None:
            continue
        unmatched_samples.append(
            UnmatchedArenaSample(
                arena_id=observed_grp_id,
                count=evidence.count,
                file=sample.file,
                match_id=sample.match_id,
                game_number=sample.game_number,
                turn_number=sample.turn_number,
                instance_id=sample.instance_id,
                zone_id=sample.zone_id,
                owner_seat_id=sample.owner_seat_id,
            )
        )

    matched_observations = sum(matched_counts_by_observed_grp_id.values())
    unmatched_observations = (
        sum(evidence.count for evidence in evidence_by_observed_grp_id.values()) - matched_observations
    )
    top_matched_cards: list[dict[str, Any]] = []
    for observed_grp_id, count in sorted(
        matched_counts_by_observed_grp_id.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:25]:
        card = combined_lookup.get(str(observed_grp_id), {})
        top_matched_cards.append(
            {
                "arena_id": observed_grp_id,
                "count": count,
                "name": card.get("name", ""),
                "set": card.get("set", ""),
                "collector_number": card.get("collector_number", ""),
            }
        )

    result = ArenaIdValidationResult(
        generated_at=datetime.now(UTC).isoformat(),
        format_key=format_key,
        scryfall_lookup_total_cards=len(scryfall_lookup),
        grp_id_override_total_cards=len(named_overrides),
        lookup_total_cards=len(combined_lookup),
        scanned_files=scanned_files,
        total_observations=sum(evidence.count for evidence in evidence_by_observed_grp_id.values()),
        distinct_arena_ids=len(evidence_by_observed_grp_id),
        matched_observations=matched_observations,
        unmatched_observations=unmatched_observations,
        matched_distinct_arena_ids=len(matched_counts_by_observed_grp_id),
        unmatched_distinct_arena_ids=(
            len(evidence_by_observed_grp_id) - len(matched_counts_by_observed_grp_id)
        ),
        top_matched_cards=top_matched_cards,
        unmatched_samples=unmatched_samples,
        override_file_path=override_path,
    )
    result.report_path = write_validation_report(result, output_dir=output_dir)
    return result


def refresh_grp_id_overrides_from_logs(
    *,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    output_dir: Path = ORACLE_DATA_ROOT,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    target_grp_ids: set[int] | None = None,
) -> GrpIdOverrideRefreshResult:
    override_path = ensure_grp_id_overrides_file(output_dir=output_dir)
    payload = json.loads(override_path.read_text(encoding="utf-8"))
    cards_by_grp_id = payload.get("cards_by_grp_id")
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    try:
        scryfall_lookup = load_arena_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    except FileNotFoundError:
        maybe_sync_card_catalog(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
        scryfall_lookup = load_arena_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    combined_lookup = load_combined_card_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    resolved_target_grp_ids = (
        {int(grp_id) for grp_id in target_grp_ids}
        if target_grp_ids is not None
        else grp_ids_requiring_evidence_refresh(cards_by_grp_id)
    )
    scanned_files, evidence_by_observed_grp_id = _scan_saved_match_logs(
        match_logs_root,
        resolved_lookup=combined_lookup,
        target_grp_ids=resolved_target_grp_ids,
    )
    added_stub_count = 0
    fingerprint_entries: list[dict[str, Any]] = []

    for observed_grp_id, evidence in sorted(
        evidence_by_observed_grp_id.items(),
        key=lambda item: (-item[1].count, item[0]),
    ):
        if str(observed_grp_id) in scryfall_lookup:
            continue

        key = str(observed_grp_id)
        existing = cards_by_grp_id.get(key)
        if not isinstance(existing, dict):
            existing = {}

        entry = dict(existing)
        existing_name = str(entry.get("name", "")).strip()
        if not existing_name and "name" not in entry:
            entry["name"] = ""
            added_stub_count += 1
        entry.setdefault("notes", "")
        entry["observations"] = evidence.count
        entry["distinct_games_seen"] = len(evidence.distinct_game_keys)
        entry["zones_seen"] = _counter_to_sorted_dict(evidence.zones_seen)
        entry["owner_seat_counts"] = _counter_to_sorted_dict(evidence.owner_seat_counts)
        entry["local_private_hand_observations"] = evidence.local_private_hand_observations
        entry["opening_hand_observations"] = evidence.opening_hand_observations
        entry["heuristic_role"] = _heuristic_role(evidence)
        entry["sample_match_ids"] = list(evidence.sample_match_ids)
        entry["sample_files"] = list(evidence.sample_files)
        entry["top_opening_hand_cooccurrences"] = _top_name_counts(evidence.opening_hand_cooccurrences)
        entry["fingerprint"] = _fingerprint_summary(evidence)

        sample = evidence.first_sample
        if sample is not None:
            entry["sample_match_id"] = sample.match_id
            entry["sample_game_number"] = sample.game_number
            entry["sample_turn_number"] = sample.turn_number
            entry["sample_instance_id"] = sample.instance_id
            entry["sample_zone_id"] = sample.zone_id
            entry["sample_owner_seat_id"] = sample.owner_seat_id

        cards_by_grp_id[key] = entry
        fingerprint_entries.append(_fingerprint_report_entry(observed_grp_id, evidence, entry))

    payload["object"] = "manasight_grp_id_overrides"
    payload["generated_at"] = datetime.now(UTC).isoformat()
    payload["format"] = format_key
    payload["bulk_type"] = bulk_type
    payload["scanned_files"] = scanned_files
    payload["cards_by_grp_id"] = cards_by_grp_id

    fingerprint_report_path, fingerprint_markdown_path = write_fingerprint_report(
        generated_at=str(payload["generated_at"]),
        format_key=format_key,
        output_dir=output_dir,
        override_path=override_path,
        entries=fingerprint_entries,
    )
    payload["fingerprint_report_path"] = str(fingerprint_report_path)
    payload["fingerprint_markdown_path"] = str(fingerprint_markdown_path)
    override_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    unresolved_distinct_ids = sum(
        1
        for observed_grp_id in evidence_by_observed_grp_id
        if str(observed_grp_id) not in scryfall_lookup
    )
    return GrpIdOverrideRefreshResult(
        generated_at=str(payload["generated_at"]),
        format_key=format_key,
        override_file_path=override_path,
        total_override_entries=len(cards_by_grp_id),
        added_stub_count=added_stub_count,
        unresolved_distinct_arena_ids=unresolved_distinct_ids,
        fingerprint_report_path=fingerprint_report_path,
        fingerprint_markdown_path=fingerprint_markdown_path,
    )


def write_validation_report(result: ArenaIdValidationResult, *, output_dir: Path = ORACLE_DATA_ROOT) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"arena-id-validation-{result.format_key}-latest.json"
    payload = asdict(result)
    if payload.get("override_file_path"):
        payload["override_file_path"] = str(payload["override_file_path"])
    if payload.get("report_path"):
        payload["report_path"] = str(payload["report_path"])
    payload["report_path"] = str(report_path)
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return report_path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate MTGA gameplay grpIds against the local Arena-aware Scryfall lookup."
    )
    parser.add_argument("--format", default=DEFAULT_FORMAT, help="Lookup format key, e.g. standard.")
    parser.add_argument(
        "--bulk-type",
        default=DEFAULT_BULK_TYPE,
        help="Bulk type used for the lookup, usually default_cards.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    result = validate_saved_match_logs(
        format_key=args.format.strip().lower() or DEFAULT_FORMAT,
        bulk_type=args.bulk_type.strip() or DEFAULT_BULK_TYPE,
    )
    print(result.summary_line())
    if result.report_path is not None:
        print(f"Report: {result.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
