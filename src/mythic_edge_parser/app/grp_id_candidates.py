from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .arena_id_validation import ensure_grp_id_overrides_file
from .card_catalog import (
    DEFAULT_BULK_TYPE,
    build_parser_fingerprint,
    load_arena_lookup,
    load_combined_card_lookup,
)
from .config import (
    ACTIVE_SUBMITTED_DECK_PATH,
    CURRENT_DECKLIST_PATH,
    GRP_ID_CANDIDATE_REPORT_JSON_PATH,
    GRP_ID_CANDIDATE_REPORT_MARKDOWN_PATH,
    GRP_ID_INFERRED_REVIEW_JSON_PATH,
    GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH,
    HAND_CONFIRMATIONS_PATH,
    MATCH_LOGS_ROOT,
    ORACLE_DATA_ROOT,
)
from .decklists import load_current_decklist
from .extractors import (
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_turn_info,
)
from .grp_id_catalog import is_grp_id_promotable
from .hand_confirmations import load_hand_confirmation_payload, normalize_hand_window

FINGERPRINT_PREFIXES = (
    "ActionType_",
    "CardColor_",
    "CardType_",
    "SubType_",
    "SuperType_",
)
MANA_SYMBOL_TO_COLOR = {
    "W": "White",
    "U": "Blue",
    "B": "Black",
    "R": "Red",
    "G": "Green",
}
MANA_TOKEN_RE = re.compile(r"\{([^}]+)\}")
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
INFERRED_NAME_SOURCES = {
    "confirmed_inferred_candidate",
    "auto_promoted_singleton_candidate",
}
GLOBAL_INFERRED_REVIEW_SCORE_MARGIN = 10
PROMOTION_STATUS_LABELS = {
    "ready": "Ready for confirmation",
    "candidate_only": "Needs review",
    "blocked": "Blocked by contradiction",
}
EVIDENCE_CHANNEL_WEIGHTS = {
    "exact_manual_confirmation": 40,
    "mana_signature": 20,
    "supertype_identity": 18,
    "card_type": 16,
    "subtype_overlap": 14,
    "color_overlap": 10,
    "power_toughness": 8,
    "action_pattern": 5,
    "zone_pattern": 5,
}


@dataclass(slots=True)
class SubmittedDeckSnapshot:
    timestamp: str
    source_file: str
    deck_cards: Counter[int]
    sideboard_cards: Counter[int]


@dataclass(slots=True)
class CandidateScore:
    name: str
    expected_count: int
    score: int
    reasons: list[str]


@dataclass(slots=True)
class EvidenceChannel:
    key: str
    label: str
    weight: int
    status: str
    detail: str


@dataclass(slots=True)
class CandidateEvidenceSummary:
    evidence_match_percent: int
    matched_weight: int
    contradicted_weight: int
    matched_channels: list[EvidenceChannel]
    contradictory_channels: list[EvidenceChannel]
    neutral_channels: list[EvidenceChannel]
    best_variant_label: str
    best_variant_scope: str
    human_verified: bool


@dataclass(slots=True)
class GrpIdCandidateRow:
    grp_id: int
    section: str
    submitted_count: int
    heuristic_role: str
    opening_hand_observations: int
    local_private_hand_observations: int
    manual_confirmation_hits: int
    exact_manual_confirmation_hits: int
    top_opening_hand_cooccurrences: list[dict[str, Any]]
    ranked_candidates: list[CandidateScore]
    top_candidate_name: str
    top_candidate_score: int
    runner_up_gap: int | None
    auto_suggestion: str
    evidence_match_percent: int
    promotion_status: str
    evidence_summary: CandidateEvidenceSummary
    confidence_percent: int
    confirmation_status: str
    confirmation_reasons: list[str]


@dataclass(slots=True)
class GrpIdCandidateReport:
    generated_at: str
    deck_label: str
    submit_deck_timestamp: str
    submit_deck_source_file: str
    unresolved_mainboard_grp_ids: list[GrpIdCandidateRow]
    unresolved_sideboard_grp_ids: list[GrpIdCandidateRow]
    remaining_mainboard_names: dict[str, int]
    remaining_sideboard_names: dict[str, int]
    decklist_alignment: str
    decklist_alignment_notes: list[str]
    report_path: Path | None = None
    markdown_report_path: Path | None = None
    promoted_override_count: int = 0

    def summary_line(self) -> str:
        unresolved_total = len(self.unresolved_mainboard_grp_ids) + len(self.unresolved_sideboard_grp_ids)
        return f"grpId candidate scoring: {unresolved_total} unresolved submitted grpIds for deck '{self.deck_label}'"


@dataclass(slots=True)
class PromotedSuggestion:
    grp_id: int
    name: str
    section: str
    score: int
    evidence_match_percent: int
    reasons: list[str]


@dataclass(slots=True)
class InferredReviewSuggestion:
    grp_id: int
    current_name: str
    current_name_source: str
    heuristic_role: str
    current_score: int
    current_rank: int | None
    proposed_name: str
    proposed_score: int
    review_reason: str
    proposed_reasons: list[str]


@dataclass(slots=True)
class ManualConfirmationEvidence:
    possible_name_counts: Counter[str] = field(default_factory=Counter)
    exact_name_counts: Counter[str] = field(default_factory=Counter)


@dataclass(slots=True)
class InferredReviewReport:
    generated_at: str
    reviewed_inferred_match_count: int
    entries: list[InferredReviewSuggestion]

    def summary_line(self) -> str:
        return (
            "grpId inferred review: "
            f"{len(self.entries)} suggestion(s) across {self.reviewed_inferred_match_count} inferred match(es)"
        )


@dataclass(slots=True)
class DeferredSuggestion:
    grp_id: int
    name: str
    section: str
    evidence_match_percent: int
    deferred_at: str


@dataclass(slots=True)
class CandidateScoringContext:
    grp_id: int
    override_entry: dict[str, Any]
    card_details: dict[str, dict[str, Any]]
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence]
    cooccurrence_counts: dict[str, int]


@dataclass(slots=True)
class CandidateReportInputs:
    decklist: Any
    submitted_deck: SubmittedDeckSnapshot
    lookup: dict[str, dict[str, Any]]
    card_details: dict[str, dict[str, Any]]
    override_rows: dict[str, dict[str, Any]]


def _report_payload(report: GrpIdCandidateReport, *, report_path: Path) -> dict[str, Any]:
    payload = asdict(report)
    payload["report_path"] = str(report_path)
    markdown_path = payload.get("markdown_report_path")
    if isinstance(markdown_path, Path):
        payload["markdown_report_path"] = str(markdown_path)
    return payload


def _evidence_channel_from_payload(payload: dict[str, Any]) -> EvidenceChannel:
    return EvidenceChannel(
        key=str(payload.get("key", "")).strip(),
        label=str(payload.get("label", "")).strip(),
        weight=int(payload.get("weight", 0) or 0),
        status=str(payload.get("status", "")).strip(),
        detail=str(payload.get("detail", "")).strip(),
    )


def _evidence_summary_from_payload(payload: dict[str, Any]) -> CandidateEvidenceSummary:
    return CandidateEvidenceSummary(
        evidence_match_percent=int(payload.get("evidence_match_percent", 0) or 0),
        matched_weight=int(payload.get("matched_weight", 0) or 0),
        contradicted_weight=int(payload.get("contradicted_weight", 0) or 0),
        matched_channels=[
            _evidence_channel_from_payload(row)
            for row in (payload.get("matched_channels") or [])
            if isinstance(row, dict)
        ],
        contradictory_channels=[
            _evidence_channel_from_payload(row)
            for row in (payload.get("contradictory_channels") or [])
            if isinstance(row, dict)
        ],
        neutral_channels=[
            _evidence_channel_from_payload(row)
            for row in (payload.get("neutral_channels") or [])
            if isinstance(row, dict)
        ],
        best_variant_label=str(payload.get("best_variant_label", "")).strip(),
        best_variant_scope=str(payload.get("best_variant_scope", "card")).strip() or "card",
        human_verified=bool(payload.get("human_verified", False)),
    )


def _candidate_row_from_payload(payload: dict[str, Any]) -> GrpIdCandidateRow:
    evidence_payload = payload.get("evidence_summary") if isinstance(payload.get("evidence_summary"), dict) else {}
    return GrpIdCandidateRow(
        grp_id=int(payload.get("grp_id", 0) or 0),
        section=str(payload.get("section", "")).strip(),
        submitted_count=int(payload.get("submitted_count", 0) or 0),
        heuristic_role=str(payload.get("heuristic_role", "")).strip(),
        opening_hand_observations=int(payload.get("opening_hand_observations", 0) or 0),
        local_private_hand_observations=int(payload.get("local_private_hand_observations", 0) or 0),
        manual_confirmation_hits=int(payload.get("manual_confirmation_hits", 0) or 0),
        exact_manual_confirmation_hits=int(payload.get("exact_manual_confirmation_hits", 0) or 0),
        top_opening_hand_cooccurrences=list(payload.get("top_opening_hand_cooccurrences") or []),
        ranked_candidates=[
            CandidateScore(
                name=str(row.get("name", "")).strip(),
                expected_count=int(row.get("expected_count", 0) or 0),
                score=int(row.get("score", 0) or 0),
                reasons=[str(reason).strip() for reason in (row.get("reasons") or []) if str(reason).strip()],
            )
            for row in (payload.get("ranked_candidates") or [])
            if isinstance(row, dict)
        ],
        top_candidate_name=str(payload.get("top_candidate_name", "")).strip(),
        top_candidate_score=int(payload.get("top_candidate_score", 0) or 0),
        runner_up_gap=(
            int(payload.get("runner_up_gap"))
            if payload.get("runner_up_gap") not in (None, "")
            else None
        ),
        auto_suggestion=str(payload.get("auto_suggestion", "")).strip(),
        evidence_match_percent=int(payload.get("evidence_match_percent", payload.get("confidence_percent", 0)) or 0),
        promotion_status=str(payload.get("promotion_status", "")).strip()
        or _promotion_status_label(str(payload.get("confirmation_status", "")).strip()),
        evidence_summary=_evidence_summary_from_payload(evidence_payload),
        confidence_percent=int(payload.get("confidence_percent", payload.get("evidence_match_percent", 0)) or 0),
        confirmation_status=str(payload.get("confirmation_status", "")).strip(),
        confirmation_reasons=[
            str(reason).strip() for reason in (payload.get("confirmation_reasons") or []) if str(reason).strip()
        ],
    )


def load_grp_id_candidate_report(path: Path = GRP_ID_CANDIDATE_REPORT_JSON_PATH) -> GrpIdCandidateReport:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected grpId candidate report payload in {path}")
    report_path_text = str(payload.get("report_path", "")).strip()
    markdown_report_path_text = str(payload.get("markdown_report_path", "")).strip()
    return GrpIdCandidateReport(
        generated_at=str(payload.get("generated_at", "")).strip(),
        deck_label=str(payload.get("deck_label", "")).strip(),
        submit_deck_timestamp=str(payload.get("submit_deck_timestamp", "")).strip(),
        submit_deck_source_file=str(payload.get("submit_deck_source_file", "")).strip(),
        unresolved_mainboard_grp_ids=[
            _candidate_row_from_payload(row)
            for row in (payload.get("unresolved_mainboard_grp_ids") or [])
            if isinstance(row, dict)
        ],
        unresolved_sideboard_grp_ids=[
            _candidate_row_from_payload(row)
            for row in (payload.get("unresolved_sideboard_grp_ids") or [])
            if isinstance(row, dict)
        ],
        remaining_mainboard_names={
            str(name): int(count)
            for name, count in (payload.get("remaining_mainboard_names") or {}).items()
        },
        remaining_sideboard_names={
            str(name): int(count)
            for name, count in (payload.get("remaining_sideboard_names") or {}).items()
        },
        decklist_alignment=str(payload.get("decklist_alignment", "")).strip(),
        decklist_alignment_notes=[
            str(note).strip() for note in (payload.get("decklist_alignment_notes") or []) if str(note).strip()
        ],
        report_path=Path(report_path_text) if report_path_text else None,
        markdown_report_path=Path(markdown_report_path_text) if markdown_report_path_text else None,
        promoted_override_count=int(payload.get("promoted_override_count", 0) or 0),
    )


def _load_override_payload(path: Path | None = None, *, output_dir: Path = ORACLE_DATA_ROOT) -> dict[str, Any]:
    override_path = ensure_grp_id_overrides_file(path=path, output_dir=output_dir)
    return json.loads(override_path.read_text(encoding="utf-8"))


def _extract_submit_deck_lists_from_payload(payload: dict[str, Any]) -> tuple[list[int], list[int]]:
    deck_cards = payload.get("deck_cards") or []
    sideboard_cards = payload.get("sideboard_cards") or []
    if deck_cards or sideboard_cards:
        return _normalize_int_list(deck_cards), _normalize_int_list(sideboard_cards)

    raw_client_action = payload.get("raw_client_action") or {}
    if not isinstance(raw_client_action, dict):
        return [], []

    inner = raw_client_action.get("payload") or {}
    if not isinstance(inner, dict):
        return [], []

    submit = inner.get("submitDeckResp") or {}
    if not isinstance(submit, dict):
        return [], []

    nested_deck = submit.get("deck") or {}
    if not isinstance(nested_deck, dict):
        nested_deck = {}

    return (
        _normalize_int_list(submit.get("deckCards") or nested_deck.get("deckCards") or []),
        _normalize_int_list(submit.get("sideboardCards") or nested_deck.get("sideboardCards") or []),
    )


def _normalize_int_list(values: list[Any]) -> list[int]:
    normalized: list[int] = []
    for value in values:
        try:
            normalized.append(int(value))
        except (TypeError, ValueError):
            continue
    return normalized


def scan_latest_submitted_deck(match_logs_root: Path = MATCH_LOGS_ROOT) -> SubmittedDeckSnapshot | None:
    latest: SubmittedDeckSnapshot | None = None

    for path in sorted(match_logs_root.rglob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("kind") != "ClientAction":
                    continue
                payload = row.get("payload") or {}
                if payload.get("type") != "submit_deck_resp":
                    continue
                deck_cards, sideboard_cards = _extract_submit_deck_lists_from_payload(payload)
                if not deck_cards and not sideboard_cards:
                    continue

                timestamp = str(row.get("timestamp") or "")
                snapshot = SubmittedDeckSnapshot(
                    timestamp=timestamp,
                    source_file=str(path),
                    deck_cards=Counter(deck_cards),
                    sideboard_cards=Counter(sideboard_cards),
                )
                if latest is None or snapshot.timestamp >= latest.timestamp:
                    latest = snapshot

    return latest


def load_active_submitted_deck(path: Path = ACTIVE_SUBMITTED_DECK_PATH) -> SubmittedDeckSnapshot | None:
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("object") != "manasight_active_submitted_deck":
        return None

    deck_cards = _normalize_int_list(payload.get("deck_cards") or [])
    sideboard_cards = _normalize_int_list(payload.get("sideboard_cards") or [])
    if not deck_cards and not sideboard_cards:
        return None

    return SubmittedDeckSnapshot(
        timestamp=str(payload.get("submitted_at") or payload.get("updated_at") or ""),
        source_file=str(path),
        deck_cards=Counter(deck_cards),
        sideboard_cards=Counter(sideboard_cards),
    )


def resolve_latest_submitted_deck(
    *,
    active_submitted_deck_path: Path | None = None,
    match_logs_root: Path = MATCH_LOGS_ROOT,
) -> SubmittedDeckSnapshot | None:
    preferred_active_path = active_submitted_deck_path
    if preferred_active_path is None and match_logs_root == MATCH_LOGS_ROOT:
        preferred_active_path = ACTIVE_SUBMITTED_DECK_PATH

    if preferred_active_path is not None:
        active_snapshot = load_active_submitted_deck(preferred_active_path)
        if active_snapshot is not None:
            return active_snapshot
    return scan_latest_submitted_deck(match_logs_root)


def _resolved_name_counts(
    grp_counts: Counter[int],
    lookup: dict[str, dict[str, Any]],
) -> Counter[str]:
    resolved: Counter[str] = Counter()
    for grp_id, count in grp_counts.items():
        card = lookup.get(str(grp_id))
        if not isinstance(card, dict):
            continue
        name = str(card.get("name", "")).strip()
        if not name:
            continue
        resolved[name] += count
    return resolved


def _remaining_name_counts(expected: Counter[str], resolved: Counter[str]) -> Counter[str]:
    remaining = Counter(expected)
    for name, count in resolved.items():
        if remaining[name] > 0:
            remaining[name] = max(remaining[name] - count, 0)
        if remaining[name] <= 0:
            remaining.pop(name, None)
    return remaining


def _counter_total(counter: Counter[Any]) -> int:
    return int(sum(counter.values()))


def _extra_known_name_counts(expected: Counter[str], resolved: Counter[str]) -> Counter[str]:
    extra: Counter[str] = Counter()
    for name, count in resolved.items():
        extra_count = count - int(expected.get(name, 0))
        if extra_count > 0:
            extra[name] = extra_count
    return extra


def _decklist_alignment(
    *,
    expected_mainboard: Counter[str],
    expected_sideboard: Counter[str],
    resolved_mainboard: Counter[str],
    resolved_sideboard: Counter[str],
    remaining_mainboard: Counter[str],
    remaining_sideboard: Counter[str],
    unresolved_mainboard_grp_ids: Counter[int],
    unresolved_sideboard_grp_ids: Counter[int],
) -> tuple[str, list[str]]:
    notes: list[str] = []

    mainboard_remaining_total = _counter_total(remaining_mainboard)
    sideboard_remaining_total = _counter_total(remaining_sideboard)
    unresolved_mainboard_total = _counter_total(unresolved_mainboard_grp_ids)
    unresolved_sideboard_total = _counter_total(unresolved_sideboard_grp_ids)

    if mainboard_remaining_total != unresolved_mainboard_total:
        notes.append(
            "Mainboard decklist drift: imported deck expects "
            f"{mainboard_remaining_total} unresolved card(s), but the latest submitted deck has "
            f"{unresolved_mainboard_total} unresolved grpId copy/copies."
        )
    if sideboard_remaining_total != unresolved_sideboard_total:
        notes.append(
            "Sideboard decklist drift: imported deck expects "
            f"{sideboard_remaining_total} unresolved card(s), but the latest submitted deck has "
            f"{unresolved_sideboard_total} unresolved grpId copy/copies."
        )

    extra_mainboard = _extra_known_name_counts(expected_mainboard, resolved_mainboard)
    extra_sideboard = _extra_known_name_counts(expected_sideboard, resolved_sideboard)
    if extra_mainboard:
        details = ", ".join(f"{name} (+{count})" for name, count in sorted(extra_mainboard.items()))
        notes.append(
            "Mainboard decklist drift: the latest submitted deck contains known cards not accounted for by the "
            f"imported decklist: {details}."
        )
    if extra_sideboard:
        details = ", ".join(f"{name} (+{count})" for name, count in sorted(extra_sideboard.items()))
        notes.append(
            "Sideboard decklist drift: the latest submitted deck contains known cards not accounted for by the "
            f"imported decklist: {details}."
        )

    return ("aligned" if not notes else "drifted"), notes


def _card_name_details(lookup: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for card in lookup.values():
        if not isinstance(card, dict):
            continue
        name = str(card.get("name", "")).strip()
        if not name or name in details:
            continue
        details[name] = card
    return details


def _fingerprint_rows(override_entry: dict[str, Any], key: str) -> list[dict[str, Any]]:
    fingerprint = override_entry.get("fingerprint") or {}
    if not isinstance(fingerprint, dict):
        return []
    rows = fingerprint.get(key) or []
    return list(rows) if isinstance(rows, list) else []


def _fingerprint_counter(override_entry: dict[str, Any], key: str, value_key: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in _fingerprint_rows(override_entry, key):
        if not isinstance(row, dict):
            continue
        value = str(row.get(value_key, "")).strip()
        if not value:
            continue
        try:
            count = int(row.get("count", 0) or 0)
        except (TypeError, ValueError):
            count = 0
        if count > 0:
            counter[value] += count
    return counter


def _strip_fingerprint_prefix(value: str) -> str:
    for prefix in FINGERPRINT_PREFIXES:
        if value.startswith(prefix):
            return value[len(prefix) :]
    return value


def _parser_fingerprint_payload(card_like: dict[str, Any]) -> dict[str, Any]:
    raw_fingerprint = card_like.get("parser_fingerprint")
    if isinstance(raw_fingerprint, dict):
        gameplay = raw_fingerprint.get("gameplay")
        if isinstance(gameplay, dict):
            merged = dict(gameplay)
            for key in ("name", "layout", "face_names", "games"):
                if key in raw_fingerprint and key not in merged:
                    merged[key] = raw_fingerprint[key]
            return merged
        return raw_fingerprint
    return build_parser_fingerprint(card_like)


def _candidate_match_variants(details: dict[str, Any]) -> list[tuple[str, bool, dict[str, Any]]]:
    variants: list[tuple[str, bool, dict[str, Any]]] = []
    top_level_fingerprint = _parser_fingerprint_payload(details)
    top_level_name = str(top_level_fingerprint.get("name") or details.get("name") or "").strip()
    variants.append((top_level_name, False, top_level_fingerprint))

    for face in details.get("card_faces") or []:
        if not isinstance(face, dict):
            continue
        face_fingerprint = _parser_fingerprint_payload(face)
        face_name = str(face_fingerprint.get("name") or face.get("name") or "").strip()
        variants.append((face_name, True, face_fingerprint))
    return variants


def _candidate_color_names(fingerprint: dict[str, Any]) -> set[str]:
    colors: set[str] = set()
    for key in ("colors", "color_indicator", "color_identity"):
        values = fingerprint.get(key) or []
        if not isinstance(values, list):
            continue
        for value in values:
            color_name = str(value or "").strip()
            if color_name:
                colors.add(color_name)
    return colors


def _best_variant_score(
    *,
    details: dict[str, Any],
    override_entry: dict[str, Any],
    score_variant: Any,
) -> tuple[int, list[str]]:
    best_score: int | None = None
    best_reasons: list[str] = []
    best_label = ""
    best_is_face = False

    for label, is_face, fingerprint in _candidate_match_variants(details):
        score, reasons = score_variant(fingerprint, override_entry)
        if best_score is None or score > best_score:
            best_score = score
            best_reasons = reasons
            best_label = label
            best_is_face = is_face

    if best_score is None:
        return 0, []
    if best_is_face and best_score > 0 and best_label:
        return best_score, [f"Best Scryfall face match: {best_label}"] + best_reasons
    return best_score, best_reasons


def _split_type_line(type_line: str) -> tuple[set[str], set[str], set[str]]:
    normalized = type_line.replace("—", "-").replace("–", "-").replace("â€”", "-").replace("—", "-")
    left, right = normalized, ""
    if "-" in normalized:
        left, right = normalized.split("-", 1)
    left_tokens = {token.strip() for token in left.split() if token.strip()}
    right_tokens = {token.strip() for token in right.split() if token.strip()}
    super_types = left_tokens & SUPER_TYPE_NAMES
    card_types = left_tokens & CARD_TYPE_NAMES
    return super_types, card_types, right_tokens


def _card_mana_signature(details: dict[str, Any]) -> str:
    mana_cost = str(details.get("mana_cost", "")).strip()
    if not mana_cost:
        return ""

    color_counts: Counter[str] = Counter()
    colorless_total = 0
    for token in MANA_TOKEN_RE.findall(mana_cost):
        token = token.strip().upper()
        if not token:
            continue
        if token.isdigit():
            colorless_total += int(token)
            continue
        if token in MANA_SYMBOL_TO_COLOR:
            color_counts[MANA_SYMBOL_TO_COLOR[token]] += 1
            continue
        hybrid_parts = [part for part in token.split("/") if part in MANA_SYMBOL_TO_COLOR]
        if hybrid_parts:
            for part in hybrid_parts:
                color_counts[MANA_SYMBOL_TO_COLOR[part]] += 1
            continue
        colorless_total += 1

    parts: list[str] = []
    for color_name in sorted(color_counts):
        parts.append(f"{color_counts[color_name]}x{color_name}")
    if colorless_total > 0:
        parts.append(f"{colorless_total}xColorless")
    return " + ".join(parts)


def _manual_confirmation_summary(
    evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
    grp_id: int,
) -> tuple[int, int]:
    evidence = evidence_by_grp_id.get(grp_id)
    if evidence is None:
        return 0, 0
    return sum(evidence.possible_name_counts.values()), sum(evidence.exact_name_counts.values())


def _top_candidate_margin(ranked: list[CandidateScore]) -> int | None:
    if len(ranked) < 2:
        return None
    return int(ranked[0].score) - int(ranked[1].score)


def _fingerprint_signal_count(override_entry: dict[str, Any]) -> int:
    signal_keys = (
        "card_types_seen",
        "super_types_seen",
        "subtypes_seen",
        "colors_seen",
        "power_values_seen",
        "toughness_values_seen",
        "mana_cost_signatures_seen",
        "action_types_seen",
        "observed_name_keys",
        "overlay_grp_ids_seen",
        "unique_ability_grp_ids_seen",
    )
    total = 0
    for key in signal_keys:
        rows = _fingerprint_rows(override_entry, key)
        if rows:
            total += 1
    return total


def _promotion_status_label(status_code: str) -> str:
    return PROMOTION_STATUS_LABELS.get(status_code, "Needs review")


def _evidence_channel(
    *,
    key: str,
    label: str,
    status: str,
    detail: str,
) -> EvidenceChannel:
    return EvidenceChannel(
        key=key,
        label=label,
        weight=int(EVIDENCE_CHANNEL_WEIGHTS[key]),
        status=status,
        detail=detail,
    )


def _dominant_counter_value(counter: Counter[str]) -> tuple[str, int] | tuple[None, int]:
    if not counter:
        return None, 0
    value, count = counter.most_common(1)[0]
    return value, int(count)


def _candidate_variant_evidence_channels(
    fingerprint: dict[str, Any],
    override_entry: dict[str, Any],
) -> list[EvidenceChannel]:
    candidate_super_types = set(fingerprint.get("super_types") or [])
    candidate_card_types = set(fingerprint.get("card_types") or [])
    candidate_subtypes = set(fingerprint.get("subtypes") or [])
    observed_card_types = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "card_types_seen", "card_type").elements()
    )
    observed_super_types = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "super_types_seen", "super_type").elements()
    )
    observed_subtypes = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "subtypes_seen", "subtype").elements()
    )
    observed_colors = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "colors_seen", "color").elements()
    )
    observed_power_values = _fingerprint_counter(override_entry, "power_values_seen", "power")
    observed_toughness_values = _fingerprint_counter(override_entry, "toughness_values_seen", "toughness")
    observed_actions = _fingerprint_counter(override_entry, "action_types_seen", "action_type")
    observed_mana_signatures = _fingerprint_counter(
        override_entry,
        "mana_cost_signatures_seen",
        "mana_cost_signature",
    )

    channels: list[EvidenceChannel] = []

    dominant_card_type, _ = _dominant_counter_value(observed_card_types)
    if dominant_card_type is None:
        channels.append(
            _evidence_channel(
                key="card_type",
                label="Dominant card type",
                status="neutral",
                detail="No card-type fingerprint has been observed yet.",
            )
        )
    elif dominant_card_type in candidate_card_types:
        channels.append(
            _evidence_channel(
                key="card_type",
                label="Dominant card type",
                status="matched",
                detail=f"Observed dominant type {dominant_card_type} matches this candidate.",
            )
        )
    else:
        channels.append(
            _evidence_channel(
                key="card_type",
                label="Dominant card type",
                status="contradicted",
                detail=f"Observed dominant type {dominant_card_type} does not match this candidate.",
            )
        )

    observed_supertype_names = set(observed_super_types.keys())
    if not observed_supertype_names:
        channels.append(
            _evidence_channel(
                key="supertype_identity",
                label="Supertype identity",
                status="neutral",
                detail="No supertype fingerprint has been observed yet.",
            )
        )
    else:
        overlap = candidate_super_types & observed_supertype_names
        if overlap:
            channels.append(
                _evidence_channel(
                    key="supertype_identity",
                    label="Supertype identity",
                    status="matched",
                    detail=f"Observed supertypes match {', '.join(sorted(overlap))}.",
                )
            )
        else:
            channels.append(
                _evidence_channel(
                    key="supertype_identity",
                    label="Supertype identity",
                    status="contradicted",
                    detail=(
                        "Observed supertypes "
                        f"{', '.join(sorted(observed_supertype_names))} do not match this candidate."
                    ),
                )
            )

    observed_subtype_names = set(observed_subtypes.keys())
    if not observed_subtype_names:
        channels.append(
            _evidence_channel(
                key="subtype_overlap",
                label="Subtype overlap",
                status="neutral",
                detail="No subtype fingerprint has been observed yet.",
            )
        )
    else:
        overlap = candidate_subtypes & observed_subtype_names
        if overlap:
            channels.append(
                _evidence_channel(
                    key="subtype_overlap",
                    label="Subtype overlap",
                    status="matched",
                    detail=f"Observed subtypes overlap {', '.join(sorted(overlap))}.",
                )
            )
        elif candidate_subtypes:
            channels.append(
                _evidence_channel(
                    key="subtype_overlap",
                    label="Subtype overlap",
                    status="contradicted",
                    detail=(
                        "Observed subtypes "
                        f"{', '.join(sorted(observed_subtype_names))} do not overlap this candidate."
                    ),
                )
            )
        else:
            channels.append(
                _evidence_channel(
                    key="subtype_overlap",
                    label="Subtype overlap",
                    status="neutral",
                    detail="Observed subtypes exist, but this candidate has no subtype data to compare yet.",
                )
            )

    candidate_colors = _candidate_color_names(fingerprint)
    observed_color_names = set(observed_colors.keys())
    if not observed_color_names:
        channels.append(
            _evidence_channel(
                key="color_overlap",
                label="Color overlap",
                status="neutral",
                detail="No color fingerprint has been observed yet.",
            )
        )
    else:
        overlap = candidate_colors & observed_color_names
        if overlap:
            channels.append(
                _evidence_channel(
                    key="color_overlap",
                    label="Color overlap",
                    status="matched",
                    detail=f"Observed colors overlap {', '.join(sorted(overlap))}.",
                )
            )
        else:
            channels.append(
                _evidence_channel(
                    key="color_overlap",
                    label="Color overlap",
                    status="contradicted",
                    detail=(
                        "Observed colors "
                        f"{', '.join(sorted(observed_color_names))} do not match this candidate."
                    ),
                )
            )

    candidate_signature = str(fingerprint.get("mana_cost_signature", "")).strip()
    if not observed_mana_signatures:
        channels.append(
            _evidence_channel(
                key="mana_signature",
                label="Mana signature",
                status="neutral",
                detail="No mana-cost signature has been observed yet.",
            )
        )
    elif candidate_signature and observed_mana_signatures.get(candidate_signature):
        channels.append(
            _evidence_channel(
                key="mana_signature",
                label="Mana signature",
                status="matched",
                detail=f"Observed mana signature matches {candidate_signature}.",
            )
        )
    else:
        observed_signatures = ", ".join(sorted(observed_mana_signatures.keys()))
        channels.append(
            _evidence_channel(
                key="mana_signature",
                label="Mana signature",
                status="contradicted",
                detail=f"Observed mana signatures {observed_signatures} do not match this candidate.",
            )
        )

    candidate_power = str(fingerprint.get("power", "")).strip()
    candidate_toughness = str(fingerprint.get("toughness", "")).strip()
    dominant_power, _ = _dominant_counter_value(observed_power_values)
    dominant_toughness, _ = _dominant_counter_value(observed_toughness_values)
    if not observed_power_values and not observed_toughness_values:
        channels.append(
            _evidence_channel(
                key="power_toughness",
                label="Power / toughness",
                status="neutral",
                detail="No power/toughness fingerprint has been observed yet.",
            )
        )
    elif (
        candidate_power
        and candidate_toughness
        and observed_power_values.get(candidate_power)
        and observed_toughness_values.get(candidate_toughness)
    ):
        channels.append(
            _evidence_channel(
                key="power_toughness",
                label="Power / toughness",
                status="matched",
                detail=f"Observed stats match {candidate_power}/{candidate_toughness}.",
            )
        )
    elif candidate_power and candidate_toughness and (dominant_power or dominant_toughness):
        observed_stats = "/".join(part for part in (dominant_power or "?", dominant_toughness or "?"))
        channels.append(
            _evidence_channel(
                key="power_toughness",
                label="Power / toughness",
                status="contradicted",
                detail=(
                    "Observed dominant stats look more like "
                    f"{observed_stats} than {candidate_power}/{candidate_toughness}."
                ),
            )
        )
    else:
        channels.append(
            _evidence_channel(
                key="power_toughness",
                label="Power / toughness",
                status="neutral",
                detail="Observed stats are incomplete, so this channel is still inconclusive.",
            )
        )

    if not observed_actions:
        channels.append(
            _evidence_channel(
                key="action_pattern",
                label="Action pattern",
                status="neutral",
                detail="No distinctive action-pattern fingerprint has been observed yet.",
            )
        )
    else:
        is_land = "Land" in candidate_card_types
        is_nonpermanent_spell = "Instant" in candidate_card_types or "Sorcery" in candidate_card_types
        if is_land and observed_actions.get("ActionType_Activate_Mana"):
            channels.append(
                _evidence_channel(
                    key="action_pattern",
                    label="Action pattern",
                    status="matched",
                    detail="Observed mana-activation activity fits a land-like card.",
                )
            )
        elif is_nonpermanent_spell and observed_actions.get("ActionType_Cast"):
            channels.append(
                _evidence_channel(
                    key="action_pattern",
                    label="Action pattern",
                    status="matched",
                    detail="Observed cast activity fits an instant or sorcery.",
                )
            )
        else:
            channels.append(
                _evidence_channel(
                    key="action_pattern",
                    label="Action pattern",
                    status="neutral",
                    detail="Observed action activity was not distinctive enough to score this candidate yet.",
                )
            )

    battlefield_hits = _zone_total(override_entry, "ZoneType_Battlefield")
    graveyard_hits = _zone_total(override_entry, "ZoneType_Graveyard")
    stack_hits = _zone_total(override_entry, "ZoneType_Stack")
    hand_hits = _zone_total(override_entry, "ZoneType_Hand")
    library_hits = _zone_total(override_entry, "ZoneType_Library")
    zone_observed = any((battlefield_hits, graveyard_hits, stack_hits, hand_hits, library_hits))
    zone_score, zone_reasons = _card_type_score_for_variant(fingerprint, override_entry)
    if not zone_observed:
        channels.append(
            _evidence_channel(
                key="zone_pattern",
                label="Zone pattern",
                status="neutral",
                detail="No zone-pattern fingerprint has been observed yet.",
            )
        )
    elif zone_score > 0:
        channels.append(
            _evidence_channel(
                key="zone_pattern",
                label="Zone pattern",
                status="matched",
                detail=zone_reasons[0] if zone_reasons else "Observed zone flow fits this candidate.",
            )
        )
    elif zone_score < 0:
        channels.append(
            _evidence_channel(
                key="zone_pattern",
                label="Zone pattern",
                status="contradicted",
                detail=zone_reasons[0] if zone_reasons else "Observed zone flow conflicts with this candidate.",
            )
        )
    else:
        channels.append(
            _evidence_channel(
                key="zone_pattern",
                label="Zone pattern",
                status="neutral",
                detail="Observed zone flow was not distinctive enough to score this candidate yet.",
            )
        )

    return channels


def _candidate_evidence_summary(
    *,
    name: str,
    card_details: dict[str, dict[str, Any]],
    override_entry: dict[str, Any],
    exact_hits: int,
) -> CandidateEvidenceSummary:
    if not name or name not in card_details:
        neutral_channels = [
            _evidence_channel(
                key=key,
                label=label,
                status="neutral",
                detail="No candidate fingerprint is available yet for this evidence channel.",
            )
            for key, label in (
                ("card_type", "Dominant card type"),
                ("supertype_identity", "Supertype identity"),
                ("subtype_overlap", "Subtype overlap"),
                ("color_overlap", "Color overlap"),
                ("mana_signature", "Mana signature"),
                ("power_toughness", "Power / toughness"),
                ("action_pattern", "Action pattern"),
                ("zone_pattern", "Zone pattern"),
            )
        ]
        matched_channels: list[EvidenceChannel] = []
        if exact_hits > 0:
            matched_channels.append(
                _evidence_channel(
                    key="exact_manual_confirmation",
                    label="Exact manual confirmation",
                    status="matched",
                    detail=(
                        "Human hand confirmation isolated this grpId to "
                        f"{name or 'this card'} {exact_hits} time(s)."
                    ),
                )
            )
        return CandidateEvidenceSummary(
            evidence_match_percent=100 if exact_hits > 0 else 0,
            matched_weight=sum(channel.weight for channel in matched_channels),
            contradicted_weight=0,
            matched_channels=matched_channels,
            contradictory_channels=[],
            neutral_channels=neutral_channels,
            best_variant_label=str(name).strip(),
            best_variant_scope="card",
            human_verified=exact_hits > 0,
        )

    details = card_details.get(name) or {}
    best_channels: list[EvidenceChannel] = []
    best_variant_label = str(name).strip()
    best_variant_scope = "card"
    best_sort_key: tuple[int, int, int, int] | None = None

    for label, is_face, fingerprint in _candidate_match_variants(details):
        channels = _candidate_variant_evidence_channels(fingerprint, override_entry)
        matched_weight = sum(channel.weight for channel in channels if channel.status == "matched")
        contradicted_weight = sum(channel.weight for channel in channels if channel.status == "contradicted")
        observed_weight = matched_weight + contradicted_weight
        percent = round(100 * matched_weight / observed_weight) if observed_weight > 0 else 0
        sort_key = (matched_weight - contradicted_weight, matched_weight, percent, -contradicted_weight)
        if best_sort_key is None or sort_key > best_sort_key:
            best_sort_key = sort_key
            best_channels = channels
            best_variant_label = str(label or name).strip()
            best_variant_scope = "face" if is_face else "card"

    matched_channels = [channel for channel in best_channels if channel.status == "matched"]
    contradictory_channels = [channel for channel in best_channels if channel.status == "contradicted"]
    neutral_channels = [channel for channel in best_channels if channel.status == "neutral"]
    matched_weight = sum(channel.weight for channel in matched_channels)
    contradicted_weight = sum(channel.weight for channel in contradictory_channels)
    evidence_match_percent = (
        round(100 * matched_weight / (matched_weight + contradicted_weight))
        if matched_weight + contradicted_weight > 0
        else 0
    )

    if exact_hits > 0:
        matched_channels = [
            _evidence_channel(
                key="exact_manual_confirmation",
                label="Exact manual confirmation",
                status="matched",
                detail=f"Human hand confirmation isolated this grpId to {name} {exact_hits} time(s).",
            ),
            *matched_channels,
        ]
        matched_weight += int(EVIDENCE_CHANNEL_WEIGHTS["exact_manual_confirmation"])
        evidence_match_percent = 100

    return CandidateEvidenceSummary(
        evidence_match_percent=evidence_match_percent,
        matched_weight=matched_weight,
        contradicted_weight=contradicted_weight,
        matched_channels=matched_channels,
        contradictory_channels=contradictory_channels,
        neutral_channels=neutral_channels,
        best_variant_label=best_variant_label,
        best_variant_scope=best_variant_scope,
        human_verified=exact_hits > 0,
    )


def _confirmation_decision(
    *,
    grp_id: int,
    promotable: bool,
    ranked: list[CandidateScore],
    auto_suggestion: str,
    override_entry: dict[str, Any],
    manual_hits: int,
    exact_hits: int,
) -> tuple[str, list[str]]:
    if not promotable:
        return "blocked", ["Blocked by contradiction or an explicit no-promotion flag."]

    if not ranked or not auto_suggestion:
        return "candidate_only", ["No strong top candidate separated itself from the rest of the field."]

    top_candidate = ranked[0]
    margin = _top_candidate_margin(ranked)
    fingerprint_signals = _fingerprint_signal_count(override_entry)
    opening_hand_observations = int(override_entry.get("opening_hand_observations", 0) or 0)
    private_hand_observations = int(override_entry.get("local_private_hand_observations", 0) or 0)
    reasons: list[str] = []

    if exact_hits > 0:
        reasons.append("Manual hand confirmation isolated this grpId to one card identity.")
        reasons.append(f"Top candidate score is {top_candidate.score}.")
        return "ready", reasons

    if margin is None:
        reasons.append("Only one candidate remains after deck reconciliation.")
    else:
        reasons.append(f"Top candidate leads the next-best candidate by {margin} points.")

    reasons.append(f"Fingerprint provided {fingerprint_signals} independent evidence channel(s).")

    if opening_hand_observations > 0:
        reasons.append(f"Observed in opening hands {opening_hand_observations} time(s).")
    elif private_hand_observations > 0:
        reasons.append(f"Observed in private hand zones {private_hand_observations} time(s).")

    if manual_hits > 0:
        reasons.append(f"Manual confirmation evidence mentioned this candidate {manual_hits} time(s).")

    has_strong_margin = margin is None or margin >= 40
    has_behavioral_evidence = fingerprint_signals > 0 and (
        opening_hand_observations > 0 or private_hand_observations > 0 or manual_hits > 0
    )
    if top_candidate.score >= 140 and has_strong_margin and has_behavioral_evidence:
        return "ready", reasons

    reasons.append("Candidate remains unconfirmed because the score or evidence mix is not strong enough yet.")
    return "candidate_only", reasons


def _zone_total(override_entry: dict[str, Any], fragment: str) -> int:
    zones_seen = override_entry.get("zones_seen") or {}
    if not isinstance(zones_seen, dict):
        return 0
    total = 0
    for label, count in zones_seen.items():
        if fragment in str(label):
            try:
                total += int(count)
            except (TypeError, ValueError):
                continue
    return total


def _fingerprint_score_for_variant(
    fingerprint: dict[str, Any],
    override_entry: dict[str, Any],
) -> tuple[int, list[str]]:
    type_line = str(fingerprint.get("type_line", "")).strip()
    if not type_line:
        return 0, []

    candidate_super_types = set(fingerprint.get("super_types") or [])
    candidate_card_types = set(fingerprint.get("card_types") or [])
    candidate_subtypes = set(fingerprint.get("subtypes") or [])
    observed_card_types = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "card_types_seen", "card_type").elements()
    )
    observed_super_types = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "super_types_seen", "super_type").elements()
    )
    observed_subtypes = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "subtypes_seen", "subtype").elements()
    )
    observed_colors = Counter(
        _strip_fingerprint_prefix(key)
        for key in _fingerprint_counter(override_entry, "colors_seen", "color").elements()
    )
    observed_power_values = _fingerprint_counter(override_entry, "power_values_seen", "power")
    observed_toughness_values = _fingerprint_counter(override_entry, "toughness_values_seen", "toughness")
    observed_actions = _fingerprint_counter(override_entry, "action_types_seen", "action_type")
    observed_mana_signatures = _fingerprint_counter(
        override_entry,
        "mana_cost_signatures_seen",
        "mana_cost_signature",
    )

    score = 0
    reasons: list[str] = []

    if observed_card_types:
        dominant_card_type, dominant_count = observed_card_types.most_common(1)[0]
        if dominant_card_type in candidate_card_types:
            score += 18
            reasons.append(f"Fingerprint dominant card type matches {dominant_card_type}")
        elif dominant_count >= 5:
            score -= 12
            reasons.append(f"Fingerprint looks more like a {dominant_card_type}")

    if "Basic" in observed_super_types:
        if "Basic" in candidate_super_types:
            score += 35
            reasons.append("Fingerprint includes Basic supertype")
        else:
            score -= 28
            reasons.append("Fingerprint includes Basic supertype, but candidate is not basic")

    subtype_overlap = candidate_subtypes & set(observed_subtypes.keys())
    if subtype_overlap:
        score += 18 * len(subtype_overlap)
        reasons.append(f"Fingerprint subtypes match {', '.join(sorted(subtype_overlap))}")
    elif observed_subtypes and candidate_subtypes:
        score -= 10
        reasons.append("Fingerprint subtypes do not match candidate subtypes")

    candidate_colors = _candidate_color_names(fingerprint)
    if observed_colors and candidate_colors:
        observed_color_names = set(observed_colors.keys())
        overlap = candidate_colors & observed_color_names
        if overlap:
            score += 10 + (4 * len(overlap))
            reasons.append(f"Fingerprint colors overlap {', '.join(sorted(overlap))}")
        else:
            score -= 10
            reasons.append("Fingerprint colors do not match candidate colors")

    candidate_signature = str(fingerprint.get("mana_cost_signature", "")).strip()
    if candidate_signature and observed_mana_signatures.get(candidate_signature):
        score += 20
        reasons.append(f"Fingerprint mana cost signature matches {candidate_signature}")

    candidate_power = str(fingerprint.get("power", "")).strip()
    if observed_power_values and candidate_power:
        dominant_power, dominant_power_count = observed_power_values.most_common(1)[0]
        if dominant_power == candidate_power:
            score += 8
            reasons.append(f"Observed power matches {candidate_power}")
        elif dominant_power_count >= 3:
            score -= 6
            reasons.append(f"Observed power looks more like {dominant_power}")

    candidate_toughness = str(fingerprint.get("toughness", "")).strip()
    if observed_toughness_values and candidate_toughness:
        dominant_toughness, dominant_toughness_count = observed_toughness_values.most_common(1)[0]
        if dominant_toughness == candidate_toughness:
            score += 8
            reasons.append(f"Observed toughness matches {candidate_toughness}")
        elif dominant_toughness_count >= 3:
            score -= 6
            reasons.append(f"Observed toughness looks more like {dominant_toughness}")

    if (
        candidate_power
        and candidate_toughness
        and observed_power_values.get(candidate_power)
        and observed_toughness_values.get(candidate_toughness)
    ):
        score += 6
        reasons.append("Observed power/toughness pair matches candidate stats")

    if "Land" in candidate_card_types and observed_actions.get("ActionType_Activate_Mana"):
        score += 8
        reasons.append("Fingerprint includes mana activation activity")
    if ("Instant" in candidate_card_types or "Sorcery" in candidate_card_types) and observed_actions.get(
        "ActionType_Cast"
    ):
        score += 8
        reasons.append("Fingerprint includes cast activity")

    return score, reasons


def _fingerprint_score(
    *,
    name: str,
    card_details: dict[str, dict[str, Any]],
    override_entry: dict[str, Any],
) -> tuple[int, list[str]]:
    details = card_details.get(name) or {}
    return _best_variant_score(
        details=details,
        override_entry=override_entry,
        score_variant=_fingerprint_score_for_variant,
    )


def _card_type_score_for_variant(
    fingerprint: dict[str, Any],
    override_entry: dict[str, Any],
) -> tuple[int, list[str]]:
    type_line = str(fingerprint.get("type_line", "")).strip()
    if not type_line:
        return 0, []

    battlefield_hits = _zone_total(override_entry, "ZoneType_Battlefield")
    graveyard_hits = _zone_total(override_entry, "ZoneType_Graveyard")
    stack_hits = _zone_total(override_entry, "ZoneType_Stack")
    hand_hits = _zone_total(override_entry, "ZoneType_Hand")
    library_hits = _zone_total(override_entry, "ZoneType_Library")

    score = 0
    reasons: list[str] = []

    candidate_card_types = set(fingerprint.get("card_types") or [])
    is_land = "Land" in candidate_card_types
    is_creature = "Creature" in candidate_card_types
    is_nonpermanent_spell = "Instant" in candidate_card_types or "Sorcery" in candidate_card_types

    if is_land:
        if graveyard_hits == 0 and stack_hits == 0 and battlefield_hits > 0 and hand_hits > 0:
            score += 8
            reasons.append("Zone pattern looks land-like")
        elif graveyard_hits >= 3 or stack_hits > 0:
            score -= 8
            reasons.append("Zone pattern is less land-like")
        if library_hits > 0 and hand_hits > 0:
            score += 3
            reasons.append("Seen in private deck/hand flow")

    if is_creature:
        if battlefield_hits > 0:
            score += 4
            reasons.append("Battlefield activity fits a creature/permanent")
        if graveyard_hits > 0:
            score += 3
            reasons.append("Graveyard activity fits a creature/permanent")

    if is_nonpermanent_spell:
        if stack_hits > 0:
            score += 6
            reasons.append("Stack activity fits an instant/sorcery")
        if graveyard_hits > 0:
            score += 4
            reasons.append("Graveyard activity fits an instant/sorcery")
        if battlefield_hits > 0:
            score -= 4
            reasons.append("Battlefield activity is less instant/sorcery-like")

    return score, reasons


def _card_type_score(
    *,
    name: str,
    card_details: dict[str, dict[str, Any]],
    override_entry: dict[str, Any],
) -> tuple[int, list[str]]:
    details = card_details.get(name) or {}
    return _best_variant_score(
        details=details,
        override_entry=override_entry,
        score_variant=_card_type_score_for_variant,
    )


def _row_match_and_game_identity(row: dict[str, Any]) -> tuple[str, Any]:
    payload = row.get("payload") or {}
    kind = str(row.get("kind", "")).strip()

    if kind == "GameState":
        derived_match_id, derived_game_number, _, _, _, _, _ = _extract_turn_info(payload)
        row_derived = row.get("derived") or {}
        match_id = str(derived_match_id or row_derived.get("match_id") or "").strip()
        game_number = derived_game_number if derived_game_number not in (None, "") else row_derived.get("game_number")
        return match_id, game_number

    if kind == "GameResult":
        game_info = payload.get("game_info") or {}
        return str(game_info.get("matchID") or "").strip(), game_info.get("gameNumber")

    if kind == "MatchState":
        return str(payload.get("match_id") or "").strip(), None

    return "", None


def _collect_match_window_hand_snapshots(
    path: Path,
    *,
    match_id_hint: str,
) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    seen_snapshot_keys: set[tuple[str, Any, tuple[int, ...]]] = set()
    in_target_window = False
    current_game_number: Any = 1

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = row.get("payload") or {}
            kind = str(row.get("kind", "")).strip()
            row_match_id, row_game_number = _row_match_and_game_identity(row)

            if kind == "MatchState":
                row_type = str(payload.get("type", "")).strip()
                if row_match_id == match_id_hint and row_type == "match_started":
                    in_target_window = True
                    current_game_number = 1
                elif row_match_id == match_id_hint and row_type == "match_completed":
                    in_target_window = False
                continue

            if kind == "GameResult" and row_match_id == match_id_hint:
                in_target_window = True
                if row_game_number not in (None, ""):
                    current_game_number = row_game_number
                continue

            if kind == "ClientAction":
                if not in_target_window:
                    continue
                if str(payload.get("type", "")).strip() != "mulligan_resp":
                    continue

                decision = str(payload.get("decision", "")).strip().lower()
                classification = (
                    "opening_hand" if decision in {"keep", "kept", "accept", "accepted"} else "mulliganed_hand"
                )
                for snapshot in reversed(snapshots):
                    if snapshot.get("classification") is not None:
                        continue
                    if snapshot.get("game_number") != current_game_number:
                        continue
                    snapshot["classification"] = classification
                    break
                continue

            if kind != "GameState":
                continue

            derived_match_id, derived_game_number, turn_number, _, _, _, _ = _extract_turn_info(payload)
            if row_match_id == match_id_hint:
                in_target_window = True
            effective_match_id = row_match_id or (match_id_hint if in_target_window else "")
            if effective_match_id != match_id_hint:
                continue

            effective_game_number = row_game_number
            if effective_game_number in (None, ""):
                effective_game_number = current_game_number
            if effective_game_number in (None, ""):
                effective_game_number = 1
            current_game_number = effective_game_number

            local_hand_instance_ids = _extract_local_private_hand_instance_ids(payload)
            if not local_hand_instance_ids or not (1 <= len(local_hand_instance_ids) <= 7):
                continue
            if turn_number not in (None, 1):
                continue

            snapshot_key = (str(path), effective_game_number, tuple(sorted(local_hand_instance_ids)))
            if snapshot_key in seen_snapshot_keys:
                continue
            seen_snapshot_keys.add(snapshot_key)

            instance_grp_lookup = _extract_instance_grp_lookup(payload)
            snapshots.append(
                {
                    "game_number": effective_game_number,
                    "turn_number": turn_number,
                    "local_hand_instance_ids": tuple(local_hand_instance_ids),
                    "instance_grp_lookup": instance_grp_lookup,
                    "classification": None,
                }
            )

    for snapshot in snapshots:
        if snapshot.get("classification") is None and snapshot.get("turn_number") == 1:
            snapshot["classification"] = "opening_hand"

    return snapshots


def _confirmed_unresolved_grp_ids_for_match_window(
    *,
    match_logs_root: Path,
    match_id_hint: str,
    game_number: int | None,
    hand_window: str,
    unresolved_grp_ids: set[int],
) -> tuple[set[int], bool]:
    if not match_id_hint or not unresolved_grp_ids:
        return set(), False

    matching_snapshots: list[set[int]] = []

    for path in sorted(match_logs_root.rglob("*.jsonl")):
        snapshots = _collect_match_window_hand_snapshots(path, match_id_hint=match_id_hint)
        for snapshot in snapshots:
            if game_number is not None and snapshot.get("game_number") != game_number:
                continue
            if snapshot.get("classification") != hand_window:
                continue

            unresolved_in_snapshot = {
                grp_id
                for instance_id in snapshot.get("local_hand_instance_ids", ())
                if (grp_id := (snapshot.get("instance_grp_lookup") or {}).get(instance_id)) in unresolved_grp_ids
            }
            if unresolved_in_snapshot:
                matching_snapshots.append(unresolved_in_snapshot)

    if not matching_snapshots:
        return set(), False

    combined = set().union(*matching_snapshots)
    return combined, len(combined) == 1


def _build_manual_confirmation_evidence(
    *,
    match_logs_root: Path,
    unresolved_grp_ids: set[int],
    hand_confirmation_path: Path,
) -> dict[int, ManualConfirmationEvidence]:
    try:
        payload = load_hand_confirmation_payload(hand_confirmation_path)
    except (FileNotFoundError, ValueError):
        return {}

    evidence_by_grp_id: dict[int, ManualConfirmationEvidence] = {}
    confirmations = list(payload.get("confirmations") or [])
    for confirmation in confirmations:
        if not isinstance(confirmation, dict):
            continue
        status = str(confirmation.get("status", "")).strip().lower()
        if status == "rejected":
            continue
        hand_window = normalize_hand_window(confirmation.get("hand_window"))
        if hand_window == "later_draw_step":
            continue
        card_name = str(confirmation.get("card_name", "")).strip()
        match_id_hint = str(confirmation.get("match_id_hint", "")).strip()
        if not card_name or not match_id_hint:
            continue

        raw_game_number = confirmation.get("game_number")
        try:
            game_number = int(raw_game_number) if raw_game_number is not None else None
        except (TypeError, ValueError):
            game_number = None

        matching_grp_ids, exact = _confirmed_unresolved_grp_ids_for_match_window(
            match_logs_root=match_logs_root,
            match_id_hint=match_id_hint,
            game_number=game_number,
            hand_window=hand_window,
            unresolved_grp_ids=unresolved_grp_ids,
        )
        if not matching_grp_ids:
            continue

        for grp_id in matching_grp_ids:
            evidence = evidence_by_grp_id.setdefault(grp_id, ManualConfirmationEvidence())
            evidence.possible_name_counts[card_name] += 1
        if exact and len(matching_grp_ids) == 1:
            only_grp_id = next(iter(matching_grp_ids))
            evidence_by_grp_id.setdefault(only_grp_id, ManualConfirmationEvidence()).exact_name_counts[card_name] += 1

    return evidence_by_grp_id


def _manual_confirmation_score(
    *,
    name: str,
    grp_id: int,
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
) -> tuple[int, list[str]]:
    evidence = confirmation_evidence_by_grp_id.get(grp_id)
    if evidence is None:
        return 0, []

    score = 0
    reasons: list[str] = []
    exact_hits = int(evidence.exact_name_counts.get(name, 0))
    possible_hits = int(evidence.possible_name_counts.get(name, 0))

    if exact_hits > 0:
        score += 500 + (exact_hits * 40)
        reasons.append(f"Manual hand confirmation isolated this grpId as {name} {exact_hits} time(s)")
    elif possible_hits > 0:
        score += 18 * possible_hits
        reasons.append(
            f"Manual hand confirmation saw {name} in a hand window containing this grpId {possible_hits} time(s)"
        )

    return score, reasons


def _cooccurrence_counts(override_entry: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in override_entry.get("top_opening_hand_cooccurrences") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        try:
            counts[name] = int(item.get("count", 0) or 0)
        except (TypeError, ValueError):
            continue
    return counts


def _candidate_scoring_context(
    *,
    grp_id: int,
    override_entry: dict[str, Any],
    card_details: dict[str, dict[str, Any]],
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
) -> CandidateScoringContext:
    return CandidateScoringContext(
        grp_id=grp_id,
        override_entry=override_entry,
        card_details=card_details,
        confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
        cooccurrence_counts=_cooccurrence_counts(override_entry),
    )


def _score_candidate_evidence(
    *,
    name: str,
    scoring_context: CandidateScoringContext,
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0

    type_score, type_reasons = _card_type_score(
        name=name,
        card_details=scoring_context.card_details,
        override_entry=scoring_context.override_entry,
    )
    score += type_score
    reasons.extend(type_reasons)

    fingerprint_score, fingerprint_reasons = _fingerprint_score(
        name=name,
        card_details=scoring_context.card_details,
        override_entry=scoring_context.override_entry,
    )
    score += fingerprint_score
    reasons.extend(fingerprint_reasons)

    confirmation_score, confirmation_reasons = _manual_confirmation_score(
        name=name,
        grp_id=scoring_context.grp_id,
        confirmation_evidence_by_grp_id=scoring_context.confirmation_evidence_by_grp_id,
    )
    score += confirmation_score
    reasons.extend(confirmation_reasons)

    if scoring_context.cooccurrence_counts.get(name):
        score += 10 + scoring_context.cooccurrence_counts[name]
        reasons.append(f"Seen with this opener card {scoring_context.cooccurrence_counts[name]} time(s)")

    return score, reasons


def _sort_candidate_scores(ranked: list[CandidateScore], *, limit: int | None = 10) -> list[CandidateScore]:
    ranked.sort(key=lambda item: (-item.score, item.name))
    if limit is None:
        return ranked
    return ranked[:limit]


def _count_match_score(expected_count: int, submitted_count: int) -> tuple[int, str]:
    count_delta = abs(expected_count - submitted_count)
    if count_delta == 0:
        return 100, "Exact count match with submitted deck"
    return (
        -(count_delta * 15),
        f"Count mismatch: deck wants {expected_count}, grpId appears {submitted_count}",
    )


def _candidate_score_row(
    *,
    name: str,
    expected_count: int,
    count_score: int,
    count_reason: str,
    evidence_score: int,
    evidence_reasons: list[str],
) -> CandidateScore:
    return CandidateScore(
        name=name,
        expected_count=expected_count,
        score=count_score + evidence_score,
        reasons=[count_reason, *evidence_reasons],
    )


def _score_candidate_name(
    *,
    name: str,
    scoring_context: CandidateScoringContext,
    expected_count: int = 0,
    submitted_count: int | None = None,
) -> CandidateScore:
    count_score = 0
    count_reason = ""
    if submitted_count is not None:
        count_score, count_reason = _count_match_score(expected_count, submitted_count)

    evidence_score, evidence_reasons = _score_candidate_evidence(
        name=name,
        scoring_context=scoring_context,
    )
    if submitted_count is None:
        return CandidateScore(
            name=name,
            expected_count=expected_count,
            score=evidence_score,
            reasons=evidence_reasons,
        )
    return _candidate_score_row(
        name=name,
        expected_count=expected_count,
        count_score=count_score,
        count_reason=count_reason,
        evidence_score=evidence_score,
        evidence_reasons=evidence_reasons,
    )


def _score_candidates(
    *,
    grp_id: int,
    submitted_count: int,
    remaining_names: Counter[str],
    override_entry: dict[str, Any],
    card_details: dict[str, dict[str, Any]],
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
) -> list[CandidateScore]:
    scoring_context = _candidate_scoring_context(
        grp_id=grp_id,
        override_entry=override_entry,
        card_details=card_details,
        confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
    )

    ranked = [
        _score_candidate_name(
            name=name,
            scoring_context=scoring_context,
            expected_count=expected_count,
            submitted_count=submitted_count,
        )
        for name, expected_count in remaining_names.items()
    ]
    return _sort_candidate_scores(ranked)


def _score_global_review_candidates(
    *,
    grp_id: int,
    override_entry: dict[str, Any],
    card_details: dict[str, dict[str, Any]],
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
) -> list[CandidateScore]:
    scoring_context = _candidate_scoring_context(
        grp_id=grp_id,
        override_entry=override_entry,
        card_details=card_details,
        confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
    )
    ranked = [
        _score_candidate_name(
            name=name,
            scoring_context=scoring_context,
        )
        for name in card_details
    ]
    return _sort_candidate_scores(ranked, limit=None)


def _auto_suggestion(ranked: list[CandidateScore]) -> str:
    if not ranked:
        return ""
    top = ranked[0]
    if len(ranked) == 1 and top.score >= 100:
        return top.name
    if len(ranked) >= 2 and top.score >= 100 and top.score - ranked[1].score >= 40:
        return top.name
    return ""


def _candidate_rows_for_section(
    *,
    grp_counts: Counter[int],
    remaining_names: Counter[str],
    override_rows: dict[str, dict[str, Any]],
    card_details: dict[str, dict[str, Any]],
    confirmation_evidence_by_grp_id: dict[int, ManualConfirmationEvidence],
    section: str,
) -> list[GrpIdCandidateRow]:
    rows: list[GrpIdCandidateRow] = []
    for grp_id, submitted_count in sorted(grp_counts.items(), key=lambda item: (-item[1], item[0])):
        override_entry = override_rows.get(str(grp_id), {})
        promotable = is_grp_id_promotable(grp_id)
        ranked = _score_candidates(
            grp_id=grp_id,
            submitted_count=submitted_count,
            remaining_names=remaining_names,
            override_entry=override_entry,
            card_details=card_details,
            confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
        )
        manual_hits, exact_hits = _manual_confirmation_summary(confirmation_evidence_by_grp_id, grp_id)
        auto_suggestion = _auto_suggestion(ranked) if promotable else ""
        confirmation_status, confirmation_reasons = _confirmation_decision(
            grp_id=grp_id,
            promotable=promotable,
            ranked=ranked,
            auto_suggestion=auto_suggestion,
            override_entry=override_entry,
            manual_hits=manual_hits,
            exact_hits=exact_hits,
        )
        top_candidate = ranked[0] if ranked else None
        runner_up_gap = _top_candidate_margin(ranked)
        evidence_summary = _candidate_evidence_summary(
            name=top_candidate.name if top_candidate is not None else "",
            card_details=card_details,
            override_entry=override_entry,
            exact_hits=exact_hits,
        )
        evidence_match_percent = evidence_summary.evidence_match_percent
        confidence_percent = evidence_match_percent
        rows.append(
            GrpIdCandidateRow(
                grp_id=grp_id,
                section=section,
                submitted_count=submitted_count,
                heuristic_role=str(override_entry.get("heuristic_role", "")),
                opening_hand_observations=int(override_entry.get("opening_hand_observations", 0) or 0),
                local_private_hand_observations=int(override_entry.get("local_private_hand_observations", 0) or 0),
                manual_confirmation_hits=manual_hits,
                exact_manual_confirmation_hits=exact_hits,
                top_opening_hand_cooccurrences=list(override_entry.get("top_opening_hand_cooccurrences") or []),
                ranked_candidates=ranked,
                top_candidate_name=top_candidate.name if top_candidate is not None else "",
                top_candidate_score=top_candidate.score if top_candidate is not None else 0,
                runner_up_gap=runner_up_gap,
                auto_suggestion=auto_suggestion,
                evidence_match_percent=evidence_match_percent,
                promotion_status=_promotion_status_label(confirmation_status),
                evidence_summary=evidence_summary,
                confidence_percent=confidence_percent,
                confirmation_status=confirmation_status,
                confirmation_reasons=confirmation_reasons,
            )
        )
    return rows


def _candidate_report_inputs(
    *,
    decklist_path: Path | None,
    active_submitted_deck_path: Path | None,
    match_logs_root: Path,
    output_dir: Path,
    format_key: str,
    bulk_type: str,
) -> CandidateReportInputs:
    decklist = load_current_decklist(decklist_path or CURRENT_DECKLIST_PATH)
    submitted_deck = resolve_latest_submitted_deck(
        active_submitted_deck_path=active_submitted_deck_path,
        match_logs_root=match_logs_root,
    )
    if submitted_deck is None:
        raise FileNotFoundError("No non-empty submit_deck_resp rows were found in saved match logs.")

    lookup = load_combined_card_lookup(format_key=format_key, bulk_type=bulk_type, output_dir=output_dir)
    card_details = _card_name_details(lookup)
    override_payload = _load_override_payload(output_dir=output_dir)
    override_rows = override_payload.get("cards_by_grp_id") or {}
    if not isinstance(override_rows, dict):
        override_rows = {}

    return CandidateReportInputs(
        decklist=decklist,
        submitted_deck=submitted_deck,
        lookup=lookup,
        card_details=card_details,
        override_rows=override_rows,
    )


def _unresolved_submitted_grp_counts(
    submitted_deck: SubmittedDeckSnapshot,
    lookup: dict[str, dict[str, Any]],
) -> tuple[Counter[int], Counter[int]]:
    unresolved_mainboard_grp_ids = Counter(
        {grp_id: count for grp_id, count in submitted_deck.deck_cards.items() if str(grp_id) not in lookup}
    )
    unresolved_sideboard_grp_ids = Counter(
        {grp_id: count for grp_id, count in submitted_deck.sideboard_cards.items() if str(grp_id) not in lookup}
    )
    return unresolved_mainboard_grp_ids, unresolved_sideboard_grp_ids


def _confirmation_evidence_for_unresolved_grp_ids(
    *,
    unresolved_mainboard_grp_ids: Counter[int],
    unresolved_sideboard_grp_ids: Counter[int],
    match_logs_root: Path,
    hand_confirmation_path: Path | None,
) -> dict[int, ManualConfirmationEvidence]:
    return _build_manual_confirmation_evidence(
        match_logs_root=match_logs_root,
        unresolved_grp_ids=set(unresolved_mainboard_grp_ids) | set(unresolved_sideboard_grp_ids),
        hand_confirmation_path=hand_confirmation_path or HAND_CONFIRMATIONS_PATH,
    )


def build_grp_id_candidate_report(
    *,
    decklist_path: Path | None = None,
    hand_confirmation_path: Path | None = None,
    active_submitted_deck_path: Path | None = None,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    output_dir: Path = ORACLE_DATA_ROOT,
    format_key: str = "arena",
    bulk_type: str = DEFAULT_BULK_TYPE,
) -> GrpIdCandidateReport:
    inputs = _candidate_report_inputs(
        decklist_path=decklist_path,
        active_submitted_deck_path=active_submitted_deck_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key=format_key,
        bulk_type=bulk_type,
    )
    resolved_mainboard = _resolved_name_counts(inputs.submitted_deck.deck_cards, inputs.lookup)
    resolved_sideboard = _resolved_name_counts(inputs.submitted_deck.sideboard_cards, inputs.lookup)
    remaining_mainboard = _remaining_name_counts(inputs.decklist.mainboard_counts(), resolved_mainboard)
    remaining_sideboard = _remaining_name_counts(inputs.decklist.sideboard_counts(), resolved_sideboard)
    unresolved_mainboard_grp_ids, unresolved_sideboard_grp_ids = _unresolved_submitted_grp_counts(
        inputs.submitted_deck,
        inputs.lookup,
    )
    confirmation_evidence_by_grp_id = _confirmation_evidence_for_unresolved_grp_ids(
        unresolved_mainboard_grp_ids=unresolved_mainboard_grp_ids,
        unresolved_sideboard_grp_ids=unresolved_sideboard_grp_ids,
        match_logs_root=match_logs_root,
        hand_confirmation_path=hand_confirmation_path,
    )

    mainboard_rows = _candidate_rows_for_section(
        grp_counts=unresolved_mainboard_grp_ids,
        remaining_names=remaining_mainboard,
        override_rows=inputs.override_rows,
        card_details=inputs.card_details,
        confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
        section="mainboard",
    )

    sideboard_rows = _candidate_rows_for_section(
        grp_counts=unresolved_sideboard_grp_ids,
        remaining_names=remaining_sideboard,
        override_rows=inputs.override_rows,
        card_details=inputs.card_details,
        confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
        section="sideboard",
    )

    decklist_alignment, decklist_alignment_notes = _decklist_alignment(
        expected_mainboard=inputs.decklist.mainboard_counts(),
        expected_sideboard=inputs.decklist.sideboard_counts(),
        resolved_mainboard=resolved_mainboard,
        resolved_sideboard=resolved_sideboard,
        remaining_mainboard=remaining_mainboard,
        remaining_sideboard=remaining_sideboard,
        unresolved_mainboard_grp_ids=unresolved_mainboard_grp_ids,
        unresolved_sideboard_grp_ids=unresolved_sideboard_grp_ids,
    )

    report = GrpIdCandidateReport(
        generated_at=datetime.now(UTC).isoformat(),
        deck_label=inputs.decklist.label,
        submit_deck_timestamp=inputs.submitted_deck.timestamp,
        submit_deck_source_file=inputs.submitted_deck.source_file,
        unresolved_mainboard_grp_ids=mainboard_rows,
        unresolved_sideboard_grp_ids=sideboard_rows,
        remaining_mainboard_names=dict(sorted(remaining_mainboard.items())),
        remaining_sideboard_names=dict(sorted(remaining_sideboard.items())),
        decklist_alignment=decklist_alignment,
        decklist_alignment_notes=decklist_alignment_notes,
    )
    report.markdown_report_path = write_grp_id_candidate_markdown(report, output_dir=output_dir)
    report.report_path = write_grp_id_candidate_report(report, output_dir=output_dir)
    return report


def write_grp_id_candidate_report(report: GrpIdCandidateReport, *, output_dir: Path = ORACLE_DATA_ROOT) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / GRP_ID_CANDIDATE_REPORT_JSON_PATH.name
    payload = _report_payload(report, report_path=report_path)
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return report_path


def write_grp_id_candidate_markdown(report: GrpIdCandidateReport, *, output_dir: Path = ORACLE_DATA_ROOT) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / GRP_ID_CANDIDATE_REPORT_MARKDOWN_PATH.name

    lines: list[str] = [
        "# grpId Candidate Report",
        "",
        f"- Deck: `{report.deck_label}`",
        f"- Submitted deck timestamp: `{report.submit_deck_timestamp}`",
        f"- Submitted deck source file: `{report.submit_deck_source_file}`",
        f"- Decklist alignment: `{report.decklist_alignment}`",
        f"- Auto-promoted suggestions in this run: `{report.promoted_override_count}`",
        "",
    ]

    if report.decklist_alignment_notes:
        lines.extend(["## Decklist Alignment Notes", ""])
        for note in report.decklist_alignment_notes:
            lines.append(f"- {note}")
        lines.append("")

    lines.extend(
        [
            "## Remaining Mainboard Names",
            "",
        ]
    )

    if report.remaining_mainboard_names:
        for name, count in report.remaining_mainboard_names.items():
            lines.append(f"- `{count}x` {name}")
    else:
        lines.append("- None")

    lines.extend(["", "## Remaining Sideboard Names", ""])
    if report.remaining_sideboard_names:
        for name, count in report.remaining_sideboard_names.items():
            lines.append(f"- `{count}x` {name}")
    else:
        lines.append("- None")

    for title, rows in (
        ("Unresolved Mainboard grpIds", report.unresolved_mainboard_grp_ids),
        ("Unresolved Sideboard grpIds", report.unresolved_sideboard_grp_ids),
    ):
        lines.extend(["", f"## {title}", ""])
        if not rows:
            lines.append("- None")
            continue

        for row in rows:
            lines.append(f"### grpId `{row.grp_id}`")
            lines.append("")
            lines.append(f"- Section: `{row.section}`")
            lines.append(f"- Submitted count: `{row.submitted_count}`")
            lines.append(f"- Heuristic role: `{row.heuristic_role}`")
            lines.append(f"- Opening hand observations: `{row.opening_hand_observations}`")
            lines.append(f"- Private-hand observations: `{row.local_private_hand_observations}`")
            lines.append(f"- Manual confirmation hits: `{row.manual_confirmation_hits}`")
            lines.append(f"- Exact manual confirmation hits: `{row.exact_manual_confirmation_hits}`")
            lines.append(f"- Top candidate: `{row.top_candidate_name or 'None'}`")
            lines.append(f"- Top candidate score: `{row.top_candidate_score}`")
            lines.append(f"- Runner-up gap: `{row.runner_up_gap if row.runner_up_gap is not None else 'n/a'}`")
            lines.append(f"- Evidence match: `{row.evidence_match_percent}%`")
            lines.append(f"- Promotion status: `{row.promotion_status}`")
            lines.append(f"- Auto suggestion: `{row.auto_suggestion or 'None'}`")
            lines.append(f"- Confirmation status: `{row.confirmation_status}`")
            if row.evidence_summary.best_variant_scope == "face" and row.evidence_summary.best_variant_label:
                lines.append(f"- Best face match: `{row.evidence_summary.best_variant_label}`")
            if row.top_opening_hand_cooccurrences:
                co_text = ", ".join(
                    f"{item.get('name', '')} ({item.get('count', 0)})" for item in row.top_opening_hand_cooccurrences
                )
                lines.append(f"- Top opener cooccurrences: {co_text}")
            lines.append("")
            lines.append("| Evidence channel | Status | Weight | Detail |")
            lines.append("|---|---|---:|---|")
            for channel in [
                *row.evidence_summary.matched_channels,
                *row.evidence_summary.contradictory_channels,
                *row.evidence_summary.neutral_channels,
            ]:
                lines.append(f"| {channel.label} | {channel.status} | {channel.weight} | {channel.detail} |")
            lines.append("")
            lines.append("| Candidate | Score | Count | Reasons |")
            lines.append("|---|---:|---:|---|")
            for candidate in row.ranked_candidates[:5]:
                reasons = "; ".join(candidate.reasons)
                lines.append(f"| {candidate.name} | {candidate.score} | {candidate.expected_count} | {reasons} |")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def promote_auto_suggestions_with_details(
    report: GrpIdCandidateReport,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
    override_path: Path | None = None,
) -> list[PromotedSuggestion]:
    payload = _load_override_payload(path=override_path, output_dir=output_dir)
    cards_by_grp_id = payload.get("cards_by_grp_id") or {}
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    promoted: list[PromotedSuggestion] = []
    for row in [*report.unresolved_mainboard_grp_ids, *report.unresolved_sideboard_grp_ids]:
        if not is_grp_id_promotable(row.grp_id):
            continue
        if str(row.confirmation_status or "").strip() != "ready":
            continue
        suggestion = str(row.auto_suggestion or "").strip()
        if not suggestion:
            continue

        key = str(row.grp_id)
        existing = cards_by_grp_id.get(key)
        if not isinstance(existing, dict):
            existing = {}
        existing_name = str(existing.get("name", "")).strip()
        if existing_name:
            continue
        review_payload = _candidate_review_payload(existing)
        if (
            str(review_payload.get("status", "")).strip() == "deferred"
            and str(review_payload.get("suggested_name", "")).strip() == suggestion
        ):
            continue

        entry = dict(existing)
        top_score = row.ranked_candidates[0].score if row.ranked_candidates else 0
        top_reasons = list(row.ranked_candidates[0].reasons) if row.ranked_candidates else []
        entry["name"] = suggestion
        entry["name_source"] = "confirmed_inferred_candidate"
        entry["name_promoted_at"] = datetime.now(UTC).isoformat()
        entry["promotion_section"] = row.section
        entry["promotion_confirmation_status"] = row.confirmation_status
        entry["promotion_status"] = row.promotion_status
        entry["promotion_evidence_match_percent"] = row.evidence_match_percent
        entry["promotion_confirmation_reasons"] = list(row.confirmation_reasons)
        if row.ranked_candidates:
            entry["promotion_score"] = top_score
            entry["promotion_reasons"] = top_reasons
        cards_by_grp_id[key] = entry
        promoted.append(
            PromotedSuggestion(
                grp_id=row.grp_id,
                name=suggestion,
                section=row.section,
                score=top_score,
                evidence_match_percent=row.evidence_match_percent,
                reasons=top_reasons,
            )
        )

    payload["cards_by_grp_id"] = cards_by_grp_id
    payload["generated_at"] = datetime.now(UTC).isoformat()
    target_path = ensure_grp_id_overrides_file(path=override_path, output_dir=output_dir)
    target_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report.promoted_override_count = len(promoted)
    if report.report_path is not None:
        write_grp_id_candidate_report(report, output_dir=output_dir)
    if report.markdown_report_path is not None:
        write_grp_id_candidate_markdown(report, output_dir=output_dir)
    return promoted


def promote_auto_suggestions(
    report: GrpIdCandidateReport,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
    override_path: Path | None = None,
) -> int:
    promoted = promote_auto_suggestions_with_details(
        report,
        output_dir=output_dir,
        override_path=override_path,
    )
    return len(promoted)


def _candidate_row_by_grp_id(report: GrpIdCandidateReport, grp_id: int) -> GrpIdCandidateRow | None:
    for row in [*report.unresolved_mainboard_grp_ids, *report.unresolved_sideboard_grp_ids]:
        if int(row.grp_id) == int(grp_id):
            return row
    return None


def _suggested_candidate_name(row: GrpIdCandidateRow) -> str:
    suggestion = str(row.auto_suggestion or "").strip()
    if suggestion:
        return suggestion
    return str(row.top_candidate_name or "").strip()


def _candidate_review_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = entry.get("candidate_review") or {}
    return payload if isinstance(payload, dict) else {}


def confirm_candidate_suggestion(
    report: GrpIdCandidateReport,
    *,
    grp_id: int,
    output_dir: Path = ORACLE_DATA_ROOT,
    override_path: Path | None = None,
) -> PromotedSuggestion:
    row = _candidate_row_by_grp_id(report, grp_id)
    if row is None:
        raise ValueError(f"grpId {grp_id} is not present in the latest candidate report.")
    if str(row.confirmation_status or "").strip() == "blocked":
        raise ValueError(f"grpId {grp_id} is blocked from confirmation.")

    suggestion = _suggested_candidate_name(row)
    if not suggestion:
        raise ValueError(f"grpId {grp_id} does not have a suggested candidate to confirm.")

    payload = _load_override_payload(path=override_path, output_dir=output_dir)
    cards_by_grp_id = payload.get("cards_by_grp_id") or {}
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    key = str(row.grp_id)
    existing = cards_by_grp_id.get(key)
    if not isinstance(existing, dict):
        existing = {}
    existing_name = str(existing.get("name", "")).strip()
    if existing_name and existing_name != suggestion:
        raise ValueError(f"grpId {grp_id} is already confirmed as {existing_name}.")

    top_reasons = list(row.ranked_candidates[0].reasons) if row.ranked_candidates else []
    top_score = row.ranked_candidates[0].score if row.ranked_candidates else row.top_candidate_score
    promoted_at = datetime.now(UTC).isoformat()

    entry = dict(existing)
    entry["name"] = suggestion
    entry["name_source"] = "manual_review_confirmed_candidate"
    entry["name_promoted_at"] = promoted_at
    entry["manual_review_confirmed_at"] = promoted_at
    entry["manual_review_evidence_match_percent"] = row.evidence_match_percent
    entry["manual_review_confidence_percent"] = row.evidence_match_percent
    entry["manual_review_top_score"] = top_score
    entry["manual_review_confirmation_status"] = row.confirmation_status
    entry["manual_review_promotion_status"] = row.promotion_status
    entry["manual_review_section"] = row.section
    entry["manual_review_reasons"] = top_reasons
    entry.pop("candidate_review", None)
    cards_by_grp_id[key] = entry

    payload["cards_by_grp_id"] = cards_by_grp_id
    payload["generated_at"] = promoted_at
    target_path = ensure_grp_id_overrides_file(path=override_path, output_dir=output_dir)
    target_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return PromotedSuggestion(
        grp_id=row.grp_id,
        name=suggestion,
        section=row.section,
        score=top_score,
        evidence_match_percent=row.evidence_match_percent,
        reasons=top_reasons,
    )


def defer_candidate_suggestion(
    report: GrpIdCandidateReport,
    *,
    grp_id: int,
    output_dir: Path = ORACLE_DATA_ROOT,
    override_path: Path | None = None,
) -> DeferredSuggestion:
    row = _candidate_row_by_grp_id(report, grp_id)
    if row is None:
        raise ValueError(f"grpId {grp_id} is not present in the latest candidate report.")

    suggestion = _suggested_candidate_name(row)
    if not suggestion:
        raise ValueError(f"grpId {grp_id} does not have a suggested candidate to defer.")

    payload = _load_override_payload(path=override_path, output_dir=output_dir)
    cards_by_grp_id = payload.get("cards_by_grp_id") or {}
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    key = str(row.grp_id)
    existing = cards_by_grp_id.get(key)
    if not isinstance(existing, dict):
        existing = {}

    deferred_at = datetime.now(UTC).isoformat()
    entry = dict(existing)
    entry["candidate_review"] = {
        "status": "deferred",
        "suggested_name": suggestion,
        "top_score": row.top_candidate_score,
        "evidence_match_percent": row.evidence_match_percent,
        "confidence_percent": row.evidence_match_percent,
        "promotion_status": row.promotion_status,
        "section": row.section,
        "deferred_at": deferred_at,
    }
    cards_by_grp_id[key] = entry

    payload["cards_by_grp_id"] = cards_by_grp_id
    payload["generated_at"] = deferred_at
    target_path = ensure_grp_id_overrides_file(path=override_path, output_dir=output_dir)
    target_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return DeferredSuggestion(
        grp_id=row.grp_id,
        name=suggestion,
        section=row.section,
        evidence_match_percent=row.evidence_match_percent,
        deferred_at=deferred_at,
    )


def _inferred_override_rows(cards_by_grp_id: dict[str, Any]) -> dict[int, dict[str, Any]]:
    rows: dict[int, dict[str, Any]] = {}
    for grp_id_text, raw_entry in cards_by_grp_id.items():
        if not isinstance(raw_entry, dict):
            continue
        current_name = str(raw_entry.get("name", "")).strip()
        current_name_source = str(raw_entry.get("name_source", "")).strip()
        if not current_name or current_name_source not in INFERRED_NAME_SOURCES:
            continue
        try:
            grp_id = int(grp_id_text)
        except (TypeError, ValueError):
            continue
        rows[grp_id] = raw_entry
    return rows


def _candidate_rank_for_name(ranked: list[CandidateScore], name: str) -> tuple[int | None, int]:
    for index, candidate in enumerate(ranked, start=1):
        if candidate.name == name:
            return index, candidate.score
    return None, 0


def _review_reason_for_inferred_match(
    *,
    current_name: str,
    current_score: int,
    top_candidate: CandidateScore | None,
    card_details: dict[str, dict[str, Any]],
) -> str:
    if current_name not in card_details:
        return "Current inferred name is no longer present in the Arena reference catalog."
    if top_candidate is None:
        return ""
    if top_candidate.name == current_name:
        return ""
    if top_candidate.score < current_score + GLOBAL_INFERRED_REVIEW_SCORE_MARGIN:
        return ""
    return f"Global rescoring now prefers a different card identity by {top_candidate.score - current_score} point(s)."


def _inferred_review_suggestion(
    *,
    grp_id: int,
    override_entry: dict[str, Any],
    ranked: list[CandidateScore],
    card_details: dict[str, dict[str, Any]],
) -> InferredReviewSuggestion | None:
    current_name = str(override_entry.get("name", "")).strip()
    current_name_source = str(override_entry.get("name_source", "")).strip()
    top_candidate = ranked[0] if ranked else None
    current_rank, current_score = _candidate_rank_for_name(ranked, current_name)
    review_reason = _review_reason_for_inferred_match(
        current_name=current_name,
        current_score=current_score,
        top_candidate=top_candidate,
        card_details=card_details,
    )
    if not review_reason:
        return None

    return InferredReviewSuggestion(
        grp_id=grp_id,
        current_name=current_name,
        current_name_source=current_name_source,
        heuristic_role=str(override_entry.get("heuristic_role", "")),
        current_score=current_score,
        current_rank=current_rank,
        proposed_name=top_candidate.name if top_candidate is not None and top_candidate.score > 0 else "",
        proposed_score=top_candidate.score if top_candidate is not None else 0,
        review_reason=review_reason,
        proposed_reasons=list(top_candidate.reasons) if top_candidate is not None else [],
    )


def build_inferred_review_report(
    *,
    hand_confirmation_path: Path | None = None,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    output_dir: Path = ORACLE_DATA_ROOT,
    format_key: str = "arena",
    bulk_type: str = DEFAULT_BULK_TYPE,
    override_path: Path | None = None,
) -> InferredReviewReport:
    payload = _load_override_payload(path=override_path, output_dir=output_dir)
    cards_by_grp_id = payload.get("cards_by_grp_id") or {}
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    inferred_rows = _inferred_override_rows(cards_by_grp_id)
    if not inferred_rows:
        return InferredReviewReport(
            generated_at=datetime.now(UTC).isoformat(),
            reviewed_inferred_match_count=0,
            entries=[],
        )

    arena_lookup = load_arena_lookup(
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )
    card_details = _card_name_details(arena_lookup)
    confirmation_evidence_by_grp_id = _build_manual_confirmation_evidence(
        match_logs_root=match_logs_root,
        unresolved_grp_ids=set(inferred_rows),
        hand_confirmation_path=hand_confirmation_path or HAND_CONFIRMATIONS_PATH,
    )

    suggestions: list[InferredReviewSuggestion] = []
    for grp_id, override_entry in sorted(inferred_rows.items()):
        ranked = _score_global_review_candidates(
            grp_id=grp_id,
            override_entry=override_entry,
            card_details=card_details,
            confirmation_evidence_by_grp_id=confirmation_evidence_by_grp_id,
        )
        suggestion = _inferred_review_suggestion(
            grp_id=grp_id,
            override_entry=override_entry,
            ranked=ranked,
            card_details=card_details,
        )
        if suggestion is not None:
            suggestions.append(suggestion)

    return InferredReviewReport(
        generated_at=datetime.now(UTC).isoformat(),
        reviewed_inferred_match_count=len(inferred_rows),
        entries=suggestions,
    )


def write_inferred_review_reports(
    report: InferredReviewReport,
    *,
    output_dir: Path = ORACLE_DATA_ROOT,
    json_path: Path = GRP_ID_INFERRED_REVIEW_JSON_PATH,
    markdown_path: Path = GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if json_path == GRP_ID_INFERRED_REVIEW_JSON_PATH:
        json_path = output_dir / GRP_ID_INFERRED_REVIEW_JSON_PATH.name
    if markdown_path == GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH:
        markdown_path = output_dir / GRP_ID_INFERRED_REVIEW_MARKDOWN_PATH.name
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_payload = {
        "object": "manasight_grp_id_inferred_review",
        "generated_at": report.generated_at,
        "review_scope": "global_inferred_matches",
        "reviewed_inferred_match_count": report.reviewed_inferred_match_count,
        "entry_count": len(report.entries),
        "entries": [asdict(item) for item in report.entries],
    }
    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# grpId Inferred Review Suggestions",
        "",
        "- Review scope: `global_inferred_matches`",
        f"- Reviewed inferred matches: `{report.reviewed_inferred_match_count}`",
        f"- Review entry count: `{len(report.entries)}`",
        "",
    ]
    if not report.entries:
        lines.append("- No inferred review suggestions were generated in this run.")
    else:
        for suggestion in report.entries:
            current_rank_label = str(suggestion.current_rank) if suggestion.current_rank is not None else "not ranked"
            lines.extend(
                [
                    f"## grpId `{suggestion.grp_id}`",
                    "",
                    f"- Current inferred name: `{suggestion.current_name}`",
                    f"- Current name source: `{suggestion.current_name_source}`",
                    f"- Heuristic role: `{suggestion.heuristic_role}`",
                    f"- Current score: `{suggestion.current_score}`",
                    f"- Current rank: `{current_rank_label}`",
                    f"- Review reason: `{suggestion.review_reason}`",
                    f"- Proposed review candidate: `{suggestion.proposed_name or 'None'}`",
                    f"- Proposed candidate score: `{suggestion.proposed_score}`",
                ]
            )
            if suggestion.proposed_reasons:
                lines.append(f"- Proposed candidate reasons: `{'; '.join(suggestion.proposed_reasons)}`")
            lines.append("")

    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return json_path, markdown_path
