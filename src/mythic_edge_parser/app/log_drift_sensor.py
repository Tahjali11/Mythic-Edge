from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..log.entry import LineBuffer, LogEntry
from ..router import Router
from .config import LOG_PATH, STATUS_ROOT

DEFAULT_DRIFT_REPORT_PATH = STATUS_ROOT / "player_log_drift_latest.json"
DEFAULT_DRIFT_BASELINE_PATH = STATUS_ROOT / "player_log_drift_baseline.json"
_MAX_TOP_ITEMS = 25
_UNITY_TIMESTAMP_LINE_RE = re.compile(r"^\[UnityCrossThreadLogger\]\d{1,2}/\d{1,2}/\d{4}\b")
_HEADER_PREFIX_RE = re.compile(r"^\[[^\]]+\]")
_UUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)
_LONG_NUMBER_RE = re.compile(r"\b\d{4,}\b")
_LONG_TOKEN_RE = re.compile(r"\b[A-Za-z0-9_-]{12,}\b")
_PREFIX_SIGNATURE_RE = re.compile(r"^(?P<label>[A-Za-z][A-Za-z0-9_-]+):")
_REQUEST_NAME_RE = re.compile(r"^==>\s*(?P<name>[-A-Za-z0-9_.]+)")
_RESPONSE_NAME_RE = re.compile(r"^<==\s*(?P<name>[-A-Za-z0-9_.]+)")


@dataclass(slots=True)
class DriftSensorResult:
    report_path: Path
    baseline_path: Path
    report: dict[str, Any]

    def summary_line(self) -> str:
        counts = self.report.get("entry_counts", {})
        return (
            f"Player.log drift audit: {counts.get('routed', 0)} routed / "
            f"{counts.get('unknown', 0)} unknown entries"
        )


def iter_log_entries(path: Path, *, chunk_size: int = 1024 * 1024) -> list[LogEntry]:
    buffer = LineBuffer()
    entries: list[LogEntry] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        while chunk := handle.read(chunk_size):
            entries.extend(buffer.feed(chunk))
    entries.extend(buffer.flush())
    return entries


def build_player_log_drift_report(
    source_path: Path,
    *,
    baseline_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    router = Router()
    header_counts: Counter[str] = Counter()
    routed_event_kinds: Counter[str] = Counter()
    unknown_signatures: Counter[str] = Counter()
    unmatched_api_names: Counter[str] = Counter()
    unmatched_request_api_names: Counter[str] = Counter()

    for entry in iter_log_entries(source_path):
        header_counts[entry.header.value] += 1
        events = router.route(entry)
        if events:
            for event in events:
                routed_event_kinds[event.kind] += 1
            continue
        signature = _entry_signature(entry)
        if signature:
            unknown_signatures[signature] += 1
        api_name, api_family = _api_name(entry)
        if api_name:
            if api_family == "request":
                unmatched_request_api_names[api_name] += 1
            else:
                unmatched_api_names[api_name] += 1

    stats = router.stats
    baseline_delta = _baseline_delta(
        unknown_signatures=unknown_signatures,
        unmatched_api_names=unmatched_api_names,
        unmatched_request_api_names=unmatched_request_api_names,
        baseline_payload=baseline_payload or {},
    )
    unknown_rate = round((stats.unknown / max(stats.routed + stats.unknown, 1)) * 100, 2)
    status = "ok"
    if stats.unknown or baseline_delta["new_unknown_signatures"] or baseline_delta["new_unmatched_api_names"]:
        status = "review"

    return {
        "object": "player_log_drift_report",
        "status": status,
        "analyzed_at": datetime.now(UTC).isoformat(),
        "source_path": str(source_path),
        "entry_counts": {
            "total": stats.routed + stats.unknown,
            "routed": stats.routed,
            "unknown": stats.unknown,
            "unknown_rate_pct": unknown_rate,
            "timestamp_missing": stats.timestamp_missing,
            "timestamp_parse_failure": stats.timestamp_parse_failure,
        },
        "headers": dict(sorted(header_counts.items())),
        "routed_event_kinds": dict(sorted(routed_event_kinds.items())),
        "top_unknown_signatures": _counter_payload(unknown_signatures, key_name="signature"),
        "top_unmatched_api_names": _counter_payload(unmatched_api_names, key_name="api_name"),
        "top_unmatched_request_api_names": _counter_payload(unmatched_request_api_names, key_name="api_name"),
        "baseline_delta": baseline_delta,
    }


def write_player_log_drift_report(
    *,
    source_path: Path = LOG_PATH,
    report_path: Path = DEFAULT_DRIFT_REPORT_PATH,
    baseline_path: Path = DEFAULT_DRIFT_BASELINE_PATH,
    refresh_baseline: bool = False,
) -> DriftSensorResult:
    baseline_payload = _load_json_dict(baseline_path)
    report = build_player_log_drift_report(source_path, baseline_payload=baseline_payload)
    _write_json(report_path, report)
    if refresh_baseline:
        _write_json(baseline_path, report)
    return DriftSensorResult(report_path=report_path, baseline_path=baseline_path, report=report)


def _meaningful_lines(entry: LogEntry) -> list[str]:
    lines: list[str] = []
    for raw_line in entry.body.splitlines():
        line = raw_line.strip()
        if not line or _UNITY_TIMESTAMP_LINE_RE.match(line):
            continue
        lines.append(_HEADER_PREFIX_RE.sub("", line).strip())
    return lines


def _api_name(entry: LogEntry) -> tuple[str, str]:
    for line in _meaningful_lines(entry):
        if line.startswith("Client.SceneChange"):
            return "Client.SceneChange", "signal"
        request_match = _REQUEST_NAME_RE.match(line)
        if request_match:
            return request_match.group("name"), "request"
        response_match = _RESPONSE_NAME_RE.match(line)
        if response_match:
            return response_match.group("name"), "response"
    return "", ""


def _entry_signature(entry: LogEntry) -> str:
    api_name, _ = _api_name(entry)
    if api_name:
        return api_name
    for line in _meaningful_lines(entry):
        prefix_match = _PREFIX_SIGNATURE_RE.match(line)
        if prefix_match:
            return prefix_match.group("label")
        scrubbed = _LONG_NUMBER_RE.sub("<n>", _UUID_RE.sub("<uuid>", line))
        scrubbed = _LONG_TOKEN_RE.sub("<token>", scrubbed)
        scrubbed = " ".join(scrubbed.split())
        if scrubbed:
            return scrubbed[:160]
    return ""


def _counter_payload(counter: Counter[str], *, key_name: str) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for name, count in counter.most_common(_MAX_TOP_ITEMS):
        payload.append({key_name: name, "count": count})
    return payload


def _baseline_delta(
    *,
    unknown_signatures: Counter[str],
    unmatched_api_names: Counter[str],
    unmatched_request_api_names: Counter[str],
    baseline_payload: dict[str, Any],
) -> dict[str, Any]:
    baseline_unknown = {
        str(item.get("signature", "")).strip()
        for item in baseline_payload.get("top_unknown_signatures", [])
        if isinstance(item, dict) and str(item.get("signature", "")).strip()
    }
    baseline_api_names = {
        str(item.get("api_name", "")).strip()
        for item in baseline_payload.get("top_unmatched_api_names", [])
        if isinstance(item, dict) and str(item.get("api_name", "")).strip()
    }
    baseline_request_api_names = {
        str(item.get("api_name", "")).strip()
        for item in baseline_payload.get("top_unmatched_request_api_names", [])
        if isinstance(item, dict) and str(item.get("api_name", "")).strip()
    }
    current_unknown = set(unknown_signatures)
    current_api_names = set(unmatched_api_names)
    current_request_api_names = set(unmatched_request_api_names)
    return {
        "new_unknown_signatures": sorted(current_unknown - baseline_unknown),
        "resolved_unknown_signatures": sorted(baseline_unknown - current_unknown),
        "new_unmatched_api_names": sorted(current_api_names - baseline_api_names),
        "resolved_unmatched_api_names": sorted(baseline_api_names - current_api_names),
        "new_unmatched_request_api_names": sorted(current_request_api_names - baseline_request_api_names),
        "resolved_unmatched_request_api_names": sorted(
            baseline_request_api_names - current_request_api_names
        ),
    }


def _load_json_dict(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit Player.log routing coverage and flag raw entry families that need parser work."
    )
    parser.add_argument("source_log", nargs="?", default=str(LOG_PATH), help="Path to Player.log or a saved log slice.")
    parser.add_argument(
        "--out",
        default=str(DEFAULT_DRIFT_REPORT_PATH),
        help="Where to write the latest drift report JSON.",
    )
    parser.add_argument(
        "--baseline",
        default=str(DEFAULT_DRIFT_BASELINE_PATH),
        help="Baseline report used to flag newly unknown entry families.",
    )
    parser.add_argument(
        "--refresh-baseline",
        action="store_true",
        help="Overwrite the baseline file with the current report after the audit runs.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    result = write_player_log_drift_report(
        source_path=Path(args.source_log),
        report_path=Path(args.out),
        baseline_path=Path(args.baseline),
        refresh_baseline=args.refresh_baseline,
    )

    print(result.summary_line())
    print(f"Report written: {result.report_path}")
    if args.refresh_baseline:
        print(f"Baseline refreshed: {result.baseline_path}")
    baseline_delta = result.report.get("baseline_delta", {})
    new_api_names = baseline_delta.get("new_unmatched_api_names", [])
    new_request_api_names = baseline_delta.get("new_unmatched_request_api_names", [])
    new_signatures = baseline_delta.get("new_unknown_signatures", [])
    if new_api_names:
        print("New unmatched API names:")
        for name in new_api_names:
            print(f"  - {name}")
    if new_request_api_names:
        print("New unmatched request API names:")
        for name in new_request_api_names:
            print(f"  - {name}")
    if new_signatures:
        print("New unknown entry signatures:")
        for name in new_signatures[:10]:
            print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
