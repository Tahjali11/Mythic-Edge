from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    AnalyticsReplayIngestResult,
    ingest_parser_normalized_replay,
    normalize_parser_normalized_replay,
)

ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION = "analytics_json_ingest_cli.v1"
ANALYTICS_JSON_INGEST_MAX_BYTES = 10_485_760
SUPPORTED_ANALYTICS_JSON_SHAPES = ("parser_normalized_replay",)
REQUIRED_ANALYTICS_VIEWS = (
    "v_opening_hand_cards",
    "v_opening_lines",
    "v_gameplay_action_review",
    "v_mulligan_outcomes",
    "v_game1_vs_postboard",
    "v_play_draw_splits",
    "v_sample_size_warnings",
    "v_matchup_label_performance",
    "v_opponent_card_observation_review",
)

SUMMARY_OBJECT = "mythic_edge_analytics_json_ingest_summary"
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2


class AnalyticsJsonIngestCliError(ValueError):
    """Raised for expected local analytics JSON ingest CLI failures."""

    def __init__(
        self,
        message: str,
        *,
        files_seen: int = 0,
        files_unsupported: int = 0,
        unsupported_files: Sequence[Mapping[str, str]] = (),
        warnings: Sequence[str] = (),
    ) -> None:
        super().__init__(message)
        self.files_seen = files_seen
        self.files_unsupported = files_unsupported
        self.unsupported_files = [dict(item) for item in unsupported_files]
        self.warnings = list(warnings)


@dataclass(frozen=True, slots=True)
class _PreparedInput:
    path: Path
    file_label: str
    payload: Mapping[str, object]
    shape: str


@dataclass(frozen=True, slots=True)
class AnalyticsJsonIngestCliResult:
    ok: bool
    status: str
    database_label: str
    files_seen: int
    files_supported: int
    files_ingested: int
    files_unsupported: int
    unsupported_files: list[dict[str, str]]
    ingest_runs: list[dict[str, object]]
    row_counts: dict[str, int]
    warnings: list[str]
    skipped: dict[str, int]
    view_readiness: dict[str, dict[str, object]]

    def summary(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "object": SUMMARY_OBJECT,
            "schema_version": ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION,
            "status": self.status,
            "database_label": self.database_label,
            "files_seen": self.files_seen,
            "files_supported": self.files_supported,
            "files_ingested": self.files_ingested,
            "files_unsupported": self.files_unsupported,
            "unsupported_files": self.unsupported_files,
            "ingest_runs": self.ingest_runs,
            "row_counts": self.row_counts,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "view_readiness": self.view_readiness,
        }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m mythic_edge_parser.app.analytics_json_ingest",
        description="Load supported Mythic Edge analytics JSON into a caller-specified SQLite database.",
    )
    parser.add_argument("--input", action="append", required=True, help="JSON file or non-recursive JSON directory")
    parser.add_argument("--database", required=True, help="Caller-specified local SQLite database path")
    parser.add_argument("--print-summary", action="store_true", help="Print deterministic JSON summary to stdout")
    parser.add_argument(
        "--check-views",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Query required analytics views after ingest (enabled by default)",
    )
    parser.add_argument("--fail-on-warning", action="store_true", help="Return exit code 1 when warnings are present")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else EXIT_USAGE

    try:
        result = ingest_analytics_json_inputs(
            inputs=tuple(Path(value) for value in args.input),
            database_path=Path(args.database),
            check_views=bool(args.check_views),
            fail_on_warning=bool(args.fail_on_warning),
        )
    except AnalyticsJsonIngestCliError as exc:
        print(f"analytics-json-ingest: {_safe_message(str(exc))}", file=sys.stderr)
        if args.print_summary:
            _print_summary(
                _failure_result(
                    database_path=Path(args.database),
                    status="failed",
                    warning=_safe_message(str(exc)),
                    files_seen=exc.files_seen,
                    files_unsupported=exc.files_unsupported,
                    unsupported_files=exc.unsupported_files,
                    warnings=exc.warnings,
                )
            )
        return EXIT_FAILURE

    if args.print_summary:
        _print_summary(result)
    return EXIT_SUCCESS if result.ok else EXIT_FAILURE


def discover_analytics_json_inputs(inputs: Sequence[Path]) -> tuple[Path, ...]:
    discovered, _warnings = _discover_inputs(inputs)
    return discovered


def load_analytics_json_file(path: Path) -> Mapping[str, object]:
    label = _file_label(path)
    if path.suffix.lower() != ".json":
        raise AnalyticsJsonIngestCliError(f"{label}: only .json files are supported")
    try:
        file_size = path.stat().st_size
    except OSError as exc:
        raise AnalyticsJsonIngestCliError(f"{label}: file is not readable") from exc
    if file_size > ANALYTICS_JSON_INGEST_MAX_BYTES:
        raise AnalyticsJsonIngestCliError(f"{label}: file exceeds maximum supported size")
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise AnalyticsJsonIngestCliError(f"{label}: file is not valid UTF-8") from exc
    except OSError as exc:
        raise AnalyticsJsonIngestCliError(f"{label}: file is not readable") from exc
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise AnalyticsJsonIngestCliError(f"{label}: invalid JSON") from exc
    if not isinstance(payload, Mapping):
        raise AnalyticsJsonIngestCliError(f"{label}: top-level JSON object is required")
    return payload


def classify_analytics_json_payload(payload: Mapping[str, object]) -> str:
    try:
        normalize_parser_normalized_replay(payload)
    except AnalyticsReplayIngestError as exc:
        raise AnalyticsJsonIngestCliError(f"unsupported analytics JSON shape: {_safe_message(str(exc))}") from exc
    return "parser_normalized_replay"


def ingest_analytics_json_inputs(
    *,
    inputs: Sequence[Path],
    database_path: Path,
    check_views: bool = True,
    fail_on_warning: bool = False,
) -> AnalyticsJsonIngestCliResult:
    prepared_inputs, warnings = _preflight_inputs(inputs)
    if not prepared_inputs:
        raise AnalyticsJsonIngestCliError("no supported JSON files were discovered")
    if database_path.exists() and database_path.is_dir():
        raise AnalyticsJsonIngestCliError("database path points to a directory")

    _ensure_database_parent(database_path)

    ingest_results: list[AnalyticsReplayIngestResult] = []
    try:
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        try:
            for prepared in prepared_inputs:
                ingest_results.append(ingest_parser_normalized_replay(connection, prepared.payload))
            view_readiness = _view_readiness(connection) if check_views else _unchecked_view_readiness()
        finally:
            connection.close()
    except (sqlite3.Error, AnalyticsReplayIngestError) as exc:
        raise AnalyticsJsonIngestCliError(f"SQLite ingest failed: {_safe_message(str(exc))}") from exc

    cli_warnings = list(warnings)
    for result in ingest_results:
        cli_warnings.extend(_ingest_warning(result.source_artifact_label, warning) for warning in result.warnings)
    skipped = _aggregate_skipped(ingest_results)
    row_counts = dict(ingest_results[-1].row_counts) if ingest_results else {}
    failed_views = [
        view_name
        for view_name, view_state in view_readiness.items()
        if view_state.get("status") not in {"queryable", "not_checked"}
    ]
    ok = not failed_views and not (fail_on_warning and cli_warnings)
    status = "completed"
    if failed_views:
        status = "view_check_failed"
    elif fail_on_warning and cli_warnings:
        status = "warning"
    return AnalyticsJsonIngestCliResult(
        ok=ok,
        status=status,
        database_label=_file_label(database_path),
        files_seen=len(prepared_inputs),
        files_supported=len(prepared_inputs),
        files_ingested=len(ingest_results),
        files_unsupported=0,
        unsupported_files=[],
        ingest_runs=[
            {
                "file_label": prepared.file_label,
                "shape": prepared.shape,
                "ingest_run_id": result.ingest_run_id,
                "source_kind": result.source_kind,
                "source_artifact_label": result.source_artifact_label,
                "status": result.status,
            }
            for prepared, result in zip(prepared_inputs, ingest_results, strict=True)
        ],
        row_counts=row_counts,
        warnings=cli_warnings,
        skipped=skipped,
        view_readiness=view_readiness,
    )


def _preflight_inputs(inputs: Sequence[Path]) -> tuple[tuple[_PreparedInput, ...], tuple[str, ...]]:
    discovered, warnings = _discover_inputs(inputs)
    prepared: list[_PreparedInput] = []
    unsupported: list[dict[str, str]] = []
    for path in discovered:
        label = _file_label(path)
        try:
            payload = load_analytics_json_file(path)
            shape = classify_analytics_json_payload(payload)
        except AnalyticsJsonIngestCliError as exc:
            unsupported.append({"file_label": label, "reason": _safe_message(str(exc))})
            continue
        prepared.append(_PreparedInput(path=path, file_label=label, payload=payload, shape=shape))
    if unsupported:
        labels = ", ".join(item["file_label"] for item in unsupported)
        raise AnalyticsJsonIngestCliError(
            f"unsupported input files: {labels}",
            files_seen=len(discovered),
            files_unsupported=len(unsupported),
            unsupported_files=unsupported,
            warnings=warnings,
        )
    return tuple(prepared), tuple(warnings)


def _discover_inputs(inputs: Sequence[Path]) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    if not inputs:
        raise AnalyticsJsonIngestCliError("at least one --input path is required")
    paths: list[Path] = []
    warnings: list[str] = []
    seen: set[Path] = set()
    for raw_path in inputs:
        if _looks_remote(raw_path):
            raise AnalyticsJsonIngestCliError(f"{_file_label(raw_path)}: remote URLs are not supported")
        path = raw_path.expanduser()
        label = _file_label(path)
        if not path.exists():
            raise AnalyticsJsonIngestCliError(f"{label}: input path does not exist")
        if path.is_dir():
            directory_children = tuple(sorted(path.glob("*.json"), key=lambda child: child.name))
            if not directory_children:
                raise AnalyticsJsonIngestCliError(f"{label}: directory contains no .json files")
            candidates = directory_children
        else:
            candidates = (path,)
        for candidate in candidates:
            if candidate.suffix.lower() != ".json":
                raise AnalyticsJsonIngestCliError(f"{_file_label(candidate)}: only .json files are supported")
            resolved = candidate.resolve()
            if resolved in seen:
                warnings.append(f"duplicate input skipped: {_file_label(candidate)}")
                continue
            seen.add(resolved)
            paths.append(candidate)
    if not paths:
        raise AnalyticsJsonIngestCliError("no JSON files were discovered")
    return tuple(paths), tuple(warnings)


def _view_readiness(connection: sqlite3.Connection) -> dict[str, dict[str, object]]:
    readiness: dict[str, dict[str, object]] = {}
    for view_name in REQUIRED_ANALYTICS_VIEWS:
        try:
            row = connection.execute(f"SELECT COUNT(*) AS row_count FROM {view_name}").fetchone()
        except sqlite3.OperationalError as exc:
            message = _safe_message(str(exc)).lower()
            status = "missing" if "no such table" in message else "failed"
            readiness[view_name] = {"status": status, "row_count": 0}
            continue
        readiness[view_name] = {"status": "queryable", "row_count": int(row["row_count"])}
    return readiness


def _unchecked_view_readiness() -> dict[str, dict[str, object]]:
    return {view_name: {"status": "not_checked", "row_count": 0} for view_name in REQUIRED_ANALYTICS_VIEWS}


def _aggregate_skipped(results: Sequence[AnalyticsReplayIngestResult]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for result in results:
        counts.update(result.skipped)
    return dict(sorted(counts.items()))


def _ingest_warning(source_label: str, warning: str) -> str:
    return f"{source_label}: {_safe_message(warning)}"


def _ensure_database_parent(database_path: Path) -> None:
    parent = database_path.expanduser().parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise AnalyticsJsonIngestCliError(f"{_file_label(parent)}: database parent cannot be created") from exc


def _failure_result(
    database_path: Path,
    status: str,
    warning: str,
    *,
    files_seen: int = 0,
    files_unsupported: int = 0,
    unsupported_files: Sequence[Mapping[str, str]] = (),
    warnings: Sequence[str] = (),
) -> AnalyticsJsonIngestCliResult:
    return AnalyticsJsonIngestCliResult(
        ok=False,
        status=status,
        database_label=_file_label(database_path),
        files_seen=files_seen,
        files_supported=0,
        files_ingested=0,
        files_unsupported=files_unsupported,
        unsupported_files=[dict(item) for item in unsupported_files],
        ingest_runs=[],
        row_counts={},
        warnings=[*warnings, warning],
        skipped={},
        view_readiness={},
    )


def _print_summary(result: AnalyticsJsonIngestCliResult) -> None:
    print(json.dumps(result.summary(), sort_keys=True, separators=(",", ":")))


def _looks_remote(path: Path) -> bool:
    raw = str(path)
    return "://" in raw


def _file_label(path: Path) -> str:
    name = path.name
    if name:
        return name
    return "<input>"


def _safe_message(message: str) -> str:
    line = str(message or "analytics JSON ingest failed").splitlines()[0]
    if len(line) > 180:
        return line[:177] + "..."
    return line


if __name__ == "__main__":
    raise SystemExit(main())
