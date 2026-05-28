"""Deterministic evidence-ledger schema snapshot builder."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from mythic_edge_parser.app import evidence_ledger

EVIDENCE_SCHEMA_SNAPSHOT_OBJECT = "mythic_edge_player_log_evidence_schema_snapshot"
EVIDENCE_SCHEMA_SNAPSHOT_VERSION = "player_log_evidence_schema_snapshot.v1"
EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_OBJECT = "mythic_edge_player_log_evidence_schema_snapshot_comparison"
EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_VERSION = "player_log_evidence_schema_snapshot_comparison.v1"
EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH = Path(
    "tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json",
)
UPDATE_ENV_VAR = "MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT"

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/175"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/11"
SNAPSHOT_VERSION = 1
SNAPSHOT_POLICY_MESSAGE = (
    "Evidence schema snapshot mismatch. Do not auto-update evidence schema snapshots. "
    "Snapshot changes require explicit issue, contract, and review approval. "
    f"After approval only, set {UPDATE_ENV_VAR}=1 and rerun tests/test_evidence_schema_snapshot.py."
)

FORBIDDEN_VALUE_SNIPPETS = (
    "[UnityCrossThreadLogger]",
    "[Client GRE]",
    "DETAILED LOGS:",
    "script.google.com/macros/",
    "data/runtime_logs/",
    "data/failed_posts/",
    "data/status/",
    "data/generated/",
)
FORBIDDEN_VALUE_RE = re.compile(
    r"(https?://hooks\.|\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|\bapi_key\b|\bsecret\b|\btoken\b)",
    re.IGNORECASE,
)
LOCAL_ABSOLUTE_PATH_RE = re.compile(r"(?:/Users/|[A-Za-z]:\\Users\\)", re.IGNORECASE)


def build_evidence_schema_snapshot(
    ledger: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Project the evidence ledger into a deterministic schema-only snapshot."""

    source_ledger = evidence_ledger.build_player_log_evidence_ledger() if ledger is None else ledger
    validation_errors = evidence_ledger.validate_player_log_evidence_ledger(source_ledger)
    if validation_errors:
        raise ValueError(f"invalid evidence ledger: {', '.join(validation_errors)}")

    output_families = [_snapshot_output_family(family) for family in _as_list(source_ledger.get("output_families"))]
    entries = [_snapshot_entry(entry) for entry in _as_list(source_ledger.get("entries"))]
    evidence_signals = [
        _snapshot_evidence_signal(entry, evidence_kind, signal)
        for entry in _as_list(source_ledger.get("entries"))
        for evidence_kind in ("direct", "fallback")
        for signal in _as_list(entry.get(f"{evidence_kind}_evidence"))
    ]
    snapshot: dict[str, Any] = {
        "object": EVIDENCE_SCHEMA_SNAPSHOT_OBJECT,
        "schema_version": EVIDENCE_SCHEMA_SNAPSHOT_VERSION,
        "snapshot_version": SNAPSHOT_VERSION,
        "snapshot_id": "",
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "ledger": {
            "object": source_ledger.get("object"),
            "schema_version": source_ledger.get("schema_version"),
            "ledger_version": source_ledger.get("ledger_version"),
            "source_issue": source_ledger.get("source_issue"),
            "parent_issue": source_ledger.get("parent_issue"),
            "branch_target": source_ledger.get("branch_target"),
            "related_adrs": _string_list(source_ledger.get("related_adrs")),
        },
        "privacy": {
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "local_absolute_paths_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
            "source_paths_are_repo_relative_or_symbolic": True,
        },
        "summary": {
            "output_family_count": len(output_families),
            "entry_count": len(entries),
            "evidence_signal_count": len(evidence_signals),
            "direct_evidence_signal_count": sum(
                1 for signal in evidence_signals if signal["evidence_kind"] == "direct"
            ),
            "fallback_evidence_signal_count": sum(
                1 for signal in evidence_signals if signal["evidence_kind"] == "fallback"
            ),
            "deferred_output_fields": [
                f"tier{family['tier']}.{family['output_family']}.{field}"
                for family in output_families
                for field in family["future_fields"]
            ],
        },
        "vocabulary": _snapshot_vocabulary(source_ledger.get("vocabulary")),
        "output_families": output_families,
        "entries": entries,
        "evidence_signals": evidence_signals,
        "snapshot_policy": {
            "deterministic": True,
            "update_mode_default": "disabled",
            "update_env_var": UPDATE_ENV_VAR,
            "auto_update_allowed": False,
            "comparison_authority": "review_signal_only",
        },
        "limitations": [
            "Schema snapshot compares stable evidence-ledger metadata only.",
            "Snapshot comparison is review evidence only, not parser semantic correctness, CI, merge, or deploy "
            "authority.",
            "V1 does not read golden replay, feature-equity, diagnostics, drift, runtime, workbook, or "
            "model-provider artifacts.",
        ],
    }
    _raise_for_privacy_findings(snapshot)
    snapshot["snapshot_id"] = _snapshot_id(snapshot)
    return snapshot


def compare_evidence_schema_snapshot(
    current: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> dict[str, Any]:
    current_mapping = isinstance(current, Mapping)
    expected_mapping = isinstance(expected, Mapping)
    current_snapshot = dict(current) if current_mapping else {}
    expected_snapshot = dict(expected) if expected_mapping else {}
    diff = _snapshot_diff(current_snapshot, expected_snapshot)
    privacy = _comparison_privacy(current_snapshot, expected_snapshot)
    limitations: list[str] = []
    if not current_mapping:
        limitations.append("current snapshot is not a mapping")
    if not expected_mapping:
        limitations.append("expected snapshot is not a mapping")

    diff_count = sum(len(items) for items in diff.values())
    privacy_count = len(privacy["forbidden_content_findings"]) + len(privacy["local_absolute_paths_found"])
    if limitations or privacy_count:
        status = "fail"
    elif diff_count:
        status = "diff"
    else:
        status = "pass"

    drift_flags: list[str] = []
    if limitations:
        drift_flags.append("schema_snapshot_missing")
    if diff_count:
        drift_flags.append("changed_signal_type")
    if privacy_count:
        drift_flags.append("sensitive_evidence_redacted")

    return {
        "object": EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_OBJECT,
        "schema_version": EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_VERSION,
        "status": status,
        "expected_snapshot_id": str(expected_snapshot.get("snapshot_id") or ""),
        "current_snapshot_id": str(current_snapshot.get("snapshot_id") or ""),
        "summary": {
            "output_family_changes": (
                len(diff["added_output_families"])
                + len(diff["removed_output_families"])
                + len(diff["changed_output_families"])
            ),
            "entry_changes": len(diff["added_entries"]) + len(diff["removed_entries"]) + len(diff["changed_entries"]),
            "evidence_signal_changes": (
                len(diff["added_evidence_signals"])
                + len(diff["removed_evidence_signals"])
                + len(diff["changed_evidence_signals"])
            ),
            "vocabulary_changes": len(diff["changed_vocabulary"]),
            "policy_changes": len(diff["changed_policies"]),
            "privacy_findings": privacy_count,
            "forbidden_content_findings": len(privacy["forbidden_content_findings"]),
        },
        "diff": diff,
        "privacy": privacy,
        "drift_flags": drift_flags,
        "review_required": status != "pass",
        "limitations": limitations,
    }


def load_expected_evidence_schema_snapshot(
    path: Path = EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH,
) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_evidence_schema_snapshot(
    path: Path,
    snapshot: Mapping[str, Any],
) -> None:
    _raise_for_privacy_findings(snapshot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_encode_snapshot(snapshot), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or check the Player.log evidence-ledger schema snapshot.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Compare the current snapshot to the expected snapshot.")
    mode.add_argument("--write", type=Path, help="Write the current snapshot to an explicit path.")
    mode.add_argument(
        "--update",
        action="store_true",
        help="Update the expected snapshot when the update env var is set.",
    )
    parser.add_argument("--expected", type=Path, default=EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH)
    args = parser.parse_args(argv)

    try:
        snapshot = build_evidence_schema_snapshot()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.write is not None:
        write_evidence_schema_snapshot(args.write, snapshot)
        return 0

    if args.update:
        if os.environ.get(UPDATE_ENV_VAR) != "1":
            print(SNAPSHOT_POLICY_MESSAGE, file=sys.stderr)
            return 2
        write_evidence_schema_snapshot(args.expected, snapshot)
        return 0

    try:
        expected = load_expected_evidence_schema_snapshot(args.expected)
    except OSError as exc:
        comparison = compare_evidence_schema_snapshot(snapshot, {})
        comparison["limitations"].append(f"expected snapshot could not be read: {exc.__class__.__name__}")
        comparison["status"] = "fail"
        comparison["review_required"] = True
        comparison["drift_flags"] = _dedupe([*comparison["drift_flags"], "schema_snapshot_missing"])
        print(_encode_snapshot(comparison), end="")
        print(SNAPSHOT_POLICY_MESSAGE, file=sys.stderr)
        return 1
    except json.JSONDecodeError:
        comparison = compare_evidence_schema_snapshot(snapshot, {})
        comparison["limitations"].append("expected snapshot is malformed JSON")
        comparison["status"] = "fail"
        comparison["review_required"] = True
        comparison["drift_flags"] = _dedupe([*comparison["drift_flags"], "schema_snapshot_missing"])
        print(_encode_snapshot(comparison), end="")
        print(SNAPSHOT_POLICY_MESSAGE, file=sys.stderr)
        return 1

    comparison = compare_evidence_schema_snapshot(snapshot, expected)
    print(_encode_snapshot(comparison), end="")
    if comparison["status"] != "pass":
        print(SNAPSHOT_POLICY_MESSAGE, file=sys.stderr)
        return 1
    return 0


def _snapshot_output_family(family: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "tier": family.get("tier"),
        "output_family": family.get("output_family"),
        "status": family.get("status"),
        "seed_fields": _string_list(family.get("seed_fields")),
        "future_fields": _string_list(family.get("future_fields")),
        "owner_modules": _string_list(family.get("owner_modules")),
    }


def _snapshot_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "entry_id": entry.get("entry_id"),
        "tier": entry.get("tier"),
        "output_family": entry.get("output_family"),
        "output_field": entry.get("output_field"),
        "display_name": entry.get("display_name"),
        "parser_owner": entry.get("parser_owner"),
        "model_surface": entry.get("model_surface"),
        "downstream_surfaces": _string_list(entry.get("downstream_surfaces")),
        "parser_managed_truth": entry.get("parser_managed_truth"),
        "coverage_status": entry.get("coverage_status"),
        "direct_signal_ids": [signal.get("signal_id") for signal in _as_list(entry.get("direct_evidence"))],
        "fallback_signal_ids": [signal.get("signal_id") for signal in _as_list(entry.get("fallback_evidence"))],
        "value_source_policy": dict(entry.get("value_source_policy") or {}),
        "confidence_policy": dict(entry.get("confidence_policy") or {}),
        "finality_policy": dict(entry.get("finality_policy") or {}),
        "invariant_checks": _string_list(entry.get("invariant_checks")),
        "drift_flags": _string_list(entry.get("drift_flags")),
        "recommended_review_modules": _string_list(entry.get("recommended_review_modules")),
        "tests": _string_list(entry.get("tests")),
        "fixture_refs": _string_list(entry.get("fixture_refs")),
    }


def _snapshot_evidence_signal(
    entry: Mapping[str, Any],
    evidence_kind: str,
    signal: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "entry_id": entry.get("entry_id"),
        "evidence_kind": evidence_kind,
        "signal_id": signal.get("signal_id"),
        "parser_event_kind": signal.get("parser_event_kind"),
        "parser_event_type": signal.get("parser_event_type"),
        "raw_event_family": signal.get("raw_event_family"),
        "raw_message_type": signal.get("raw_message_type"),
        "normalized_payload_path": _stable_schema_text(signal.get("normalized_payload_path")),
        "raw_payload_path": _stable_schema_text(signal.get("raw_payload_path")),
        "required_for_final": signal.get("required_for_final"),
        "value_source_when_used": signal.get("value_source_when_used"),
        "confidence_when_used": signal.get("confidence_when_used"),
        "finality_when_used": signal.get("finality_when_used"),
        "allowed_types": _string_list(signal.get("allowed_types")),
        "privacy_class": signal.get("privacy_class"),
    }


def _snapshot_vocabulary(vocabulary: Any) -> dict[str, Any]:
    if not isinstance(vocabulary, Mapping):
        return {
            "value_sources": [],
            "confidence_levels": [],
            "finality_labels": [],
            "drift_flags": [],
            "invariant_statuses": [],
        }
    return {
        "value_sources": _string_list(vocabulary.get("value_sources")),
        "confidence_levels": _string_list(vocabulary.get("confidence_levels")),
        "finality_labels": _string_list(vocabulary.get("finality_labels")),
        "drift_flags": _string_list(vocabulary.get("drift_flags")),
        "invariant_statuses": _string_list(vocabulary.get("invariant_statuses")),
    }


def _snapshot_diff(current: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, list[str]]:
    current_families = _records_by_key(current.get("output_families"), "output_family")
    expected_families = _records_by_key(expected.get("output_families"), "output_family")
    current_entries = _records_by_key(current.get("entries"), "entry_id")
    expected_entries = _records_by_key(expected.get("entries"), "entry_id")
    current_signals = _evidence_signals_by_key(current.get("evidence_signals"))
    expected_signals = _evidence_signals_by_key(expected.get("evidence_signals"))
    return {
        "added_output_families": _added_keys(current_families, expected_families),
        "removed_output_families": _removed_keys(current_families, expected_families),
        "changed_output_families": _changed_keys(current_families, expected_families),
        "added_entries": _added_keys(current_entries, expected_entries),
        "removed_entries": _removed_keys(current_entries, expected_entries),
        "changed_entries": _changed_keys(current_entries, expected_entries),
        "added_evidence_signals": _added_keys(current_signals, expected_signals),
        "removed_evidence_signals": _removed_keys(current_signals, expected_signals),
        "changed_evidence_signals": _changed_keys(current_signals, expected_signals),
        "changed_vocabulary": _changed_mapping_keys(
            _mapping_or_empty(current.get("vocabulary")),
            _mapping_or_empty(expected.get("vocabulary")),
        ),
        "changed_policies": _changed_policies(current, expected, current_entries, expected_entries),
    }


def _changed_policies(
    current: Mapping[str, Any],
    expected: Mapping[str, Any],
    current_entries: Mapping[str, Mapping[str, Any]],
    expected_entries: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    changed: list[str] = []
    if current.get("summary") != expected.get("summary"):
        changed.append("summary")
    if current.get("snapshot_id") != expected.get("snapshot_id"):
        changed.append("snapshot_id")
    if current.get("snapshot_policy") != expected.get("snapshot_policy"):
        changed.append("snapshot_policy")
    for entry_id in sorted(set(current_entries) & set(expected_entries)):
        for policy_key in ("value_source_policy", "confidence_policy", "finality_policy"):
            if current_entries[entry_id].get(policy_key) != expected_entries[entry_id].get(policy_key):
                changed.append(f"{entry_id}.{policy_key}")
    return changed


def _comparison_privacy(current: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, list[str]]:
    current_findings = _privacy_findings(current, "current")
    expected_findings = _privacy_findings(expected, "expected")
    return {
        "forbidden_content_findings": sorted(
            current_findings["forbidden_content_findings"] + expected_findings["forbidden_content_findings"],
        ),
        "local_absolute_paths_found": sorted(
            current_findings["local_absolute_paths_found"] + expected_findings["local_absolute_paths_found"],
        ),
    }


def _raise_for_privacy_findings(payload: Mapping[str, Any]) -> None:
    findings = _privacy_findings(payload, "snapshot")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden evidence schema snapshot content: {', '.join(combined)}")


def _privacy_findings(payload: Any, path: str) -> dict[str, list[str]]:
    findings = {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
    }
    _collect_privacy_findings(payload, path, findings)
    return findings


def _collect_privacy_findings(payload: Any, path: str, findings: dict[str, list[str]]) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            _collect_privacy_findings(value, f"{path}.{key}", findings)
        return
    if isinstance(payload, list | tuple):
        for index, value in enumerate(payload):
            _collect_privacy_findings(value, f"{path}[{index}]", findings)
        return
    if not isinstance(payload, str):
        return

    if LOCAL_ABSOLUTE_PATH_RE.search(payload):
        findings["local_absolute_paths_found"].append(path)
    if FORBIDDEN_VALUE_RE.search(payload) or any(snippet in payload for snippet in FORBIDDEN_VALUE_SNIPPETS):
        findings["forbidden_content_findings"].append(path)


def _snapshot_id(snapshot: Mapping[str, Any]) -> str:
    content = dict(snapshot)
    content["snapshot_id"] = ""
    digest = hashlib.sha256(_canonical_json(content).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _encode_snapshot(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list | tuple) else []


def _stable_schema_text(value: Any) -> str:
    return str(value or "").replace("generated_at", "volatile_timestamp_field_excluded")


def _mapping_or_empty(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _records_by_key(value: Any, key: str) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, list):
        return {}
    return {str(item.get(key) or ""): item for item in value if isinstance(item, Mapping)}


def _evidence_signals_by_key(value: Any) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, list):
        return {}
    return {
        _evidence_signal_key(item): item
        for item in value
        if isinstance(item, Mapping) and _evidence_signal_key(item)
    }


def _evidence_signal_key(item: Mapping[str, Any]) -> str:
    entry_id = str(item.get("entry_id") or "")
    evidence_kind = str(item.get("evidence_kind") or "")
    signal_id = str(item.get("signal_id") or "")
    if not entry_id or not evidence_kind or not signal_id:
        return ""
    return f"{entry_id}:{evidence_kind}:{signal_id}"


def _added_keys(current: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    return sorted(set(current) - set(expected))


def _removed_keys(current: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    return sorted(set(expected) - set(current))


def _changed_keys(current: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    return sorted(key for key in set(current) & set(expected) if current[key] != expected[key])


def _changed_mapping_keys(current: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    return sorted(key for key in set(current) | set(expected) if current.get(key) != expected.get(key))


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


if __name__ == "__main__":
    raise SystemExit(main())
