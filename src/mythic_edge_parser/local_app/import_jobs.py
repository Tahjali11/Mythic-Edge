from __future__ import annotations

import re
import sqlite3
import uuid
from collections import OrderedDict
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_legacy_jsonl_adapter import (
    LegacyJsonlAdapterError,
    adapt_legacy_jsonl_artifacts,
    failed_legacy_jsonl_import_quality,
)

from .paths import LocalAppPaths, build_local_app_paths, display_app_path

MANUAL_JSONL_IMPORT_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1"
MANUAL_JSONL_IMPORT_OBJECT = "mythic_edge_local_app_manual_jsonl_import_job"

_MAX_STORED_JOBS = 25
_JOBS: OrderedDict[str, dict[str, object]] = OrderedDict()
_WINDOWS_DRIVE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
_UNC_PATH_RE = re.compile(r"^(\\\\|//)[^\\/]+[\\/]")
_SAFE_DISPLAY_BASENAME_RE = re.compile(r"^[A-Za-z0-9_. -]{1,80}\.jsonl$", re.IGNORECASE)
_SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,100}$")
_PRIVATE_MARKERS = (
    "player.log",
    "script.google.com",
    "hooks.",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
    "secret",
    "password",
    "token",
)


@dataclass(frozen=True, slots=True)
class _SourceValidation:
    source_path: Path | None
    source_artifact_label: str | None
    source_display_label: str
    source_file_extension: str
    error: str | None = None


def run_manual_jsonl_import(
    request: object,
    *,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]:
    now_fn = now or _utc_now
    created_at = now_fn()
    job_id = (job_id_factory or _default_job_id)()
    source = _validate_source_request(request)
    if source.error is not None or source.source_path is None:
        return _store_job(
            _job_payload(
                job_id=job_id,
                status="rejected",
                phase="failed",
                created_at=created_at,
                started_at=created_at,
                finished_at=now_fn(),
                source=source,
                adapter=_adapter_summary(status="not_started"),
                ingest=_ingest_summary(status="not_started"),
                database=_database_summary(status="not_started", created=False),
                warnings=[],
                errors=[source.error or "source_path_invalid"],
            ),
        )

    started_at = now_fn()
    try:
        adapter_result = adapt_legacy_jsonl_artifacts(
            source.source_path,
            source_artifact_label=source.source_artifact_label,
        )
    except LegacyJsonlAdapterError as exc:
        error_code = _adapter_error_category(str(exc))
        return _store_job(
            _job_payload(
                job_id=job_id,
                status="failed",
                phase="failed",
                created_at=created_at,
                started_at=started_at,
                finished_at=now_fn(),
                source=source,
                adapter=_adapter_summary(status="failed", failure_code=error_code),
                ingest=_ingest_summary(status="not_started"),
                database=_database_summary(status="not_started", created=False),
                warnings=[],
                errors=[error_code],
            ),
        )

    paths = build_local_app_paths(app_data_root)
    if paths.app_data_root is None or paths.db_dir is None or paths.analytics_database is None:
        return _store_job(
            _job_payload(
                job_id=job_id,
                status="failed",
                phase="failed",
                created_at=created_at,
                started_at=started_at,
                finished_at=now_fn(),
                source=_source_with_adapter_label(source, adapter_result.source_artifact_label),
                adapter=_adapter_summary(status="succeeded", result=adapter_result),
                ingest=_ingest_summary(status="not_started"),
                database=_database_summary(status="unavailable", created=False),
                warnings=list(adapter_result.warnings),
                errors=["app_data_unavailable"],
            ),
        )

    try:
        _create_app_data_dirs(paths)
    except OSError:
        return _store_job(
            _job_payload(
                job_id=job_id,
                status="failed",
                phase="failed",
                created_at=created_at,
                started_at=started_at,
                finished_at=now_fn(),
                source=_source_with_adapter_label(source, adapter_result.source_artifact_label),
                adapter=_adapter_summary(status="succeeded", result=adapter_result),
                ingest=_ingest_summary(status="not_started"),
                database=_database_summary(status="unavailable", created=False),
                warnings=list(adapter_result.warnings),
                errors=["app_data_unavailable"],
            ),
        )

    database_existed = paths.analytics_database.exists()
    try:
        connection = sqlite3.connect(paths.analytics_database)
        connection.row_factory = sqlite3.Row
        try:
            finished_at = now_fn()
            ingest_result = ingest_parser_normalized_replay(
                connection,
                adapter_result.replay,
                started_at=started_at,
                finished_at=finished_at,
            )
        finally:
            connection.close()
    except (sqlite3.DatabaseError, AnalyticsReplayIngestError, OSError):
        return _store_job(
            _job_payload(
                job_id=job_id,
                status="failed",
                phase="failed",
                created_at=created_at,
                started_at=started_at,
                finished_at=now_fn(),
                source=_source_with_adapter_label(source, adapter_result.source_artifact_label),
                adapter=_adapter_summary(status="succeeded", result=adapter_result),
                ingest=_ingest_summary(status="failed"),
                database=_database_summary(
                    status="failed",
                    created=not database_existed and paths.analytics_database.exists(),
                ),
                warnings=list(adapter_result.warnings),
                errors=["ingest_failed"],
            ),
        )

    warning_categories = _warning_categories(adapter_result)
    status = "degraded" if warning_categories or ingest_result.warnings else "succeeded"
    return _store_job(
        _job_payload(
            job_id=job_id,
            status=status,
            phase="completed",
            created_at=created_at,
            started_at=started_at,
            finished_at=finished_at,
            source=_source_with_adapter_label(source, adapter_result.source_artifact_label),
            adapter=_adapter_summary(status=status, result=adapter_result, ingest_warnings=ingest_result.warnings),
            ingest=_ingest_summary(status="succeeded", result=ingest_result),
            database=_database_summary(
                status="ok",
                created=not database_existed and paths.analytics_database.exists(),
            ),
            warnings=warning_categories + list(ingest_result.warnings),
            errors=[],
        ),
    )


def get_import_job(job_id: str) -> dict[str, object] | None:
    job = _JOBS.get(job_id)
    return dict(job) if job is not None else None


def clear_import_jobs_for_tests() -> None:
    _JOBS.clear()


def _validate_source_request(request: object) -> _SourceValidation:
    if not isinstance(request, Mapping):
        return _invalid_source("source_request_invalid")

    raw_source_path = request.get("source_path")
    if not isinstance(raw_source_path, str) or not raw_source_path.strip():
        return _invalid_source("source_path_required")

    source_text = _normalize_source_path_text(raw_source_path)
    source_path = Path(source_text)
    extension = source_path.suffix.lower()
    display_label = _safe_source_display_label(source_path)
    raw_label = request.get("source_artifact_label")
    if raw_label is not None:
        if not isinstance(raw_label, str) or not raw_label.strip():
            return _invalid_source(
                "source_artifact_label_invalid",
                source_file_extension=extension,
                source_display_label=display_label,
            )
        source_artifact_label = raw_label.strip()
    else:
        source_artifact_label = None

    if _looks_like_url(source_text):
        return _invalid_source(
            "source_path_url_not_allowed",
            source_file_extension=extension,
            source_display_label=display_label,
        )
    if _looks_like_unc_path(source_text):
        return _invalid_source(
            "source_path_unc_not_allowed",
            source_file_extension=extension,
            source_display_label=display_label,
        )
    if not source_path.exists():
        return _invalid_source(
            "source_path_missing",
            source_file_extension=extension,
            source_display_label=display_label,
        )
    if source_path.is_dir():
        return _invalid_source(
            "source_path_directory_not_allowed",
            source_file_extension=extension,
            source_display_label=display_label,
        )
    if extension != ".jsonl":
        return _invalid_source(
            "source_path_extension_not_allowed",
            source_file_extension=extension,
            source_display_label=display_label,
        )
    if not source_path.is_file():
        return _invalid_source(
            "source_path_not_file",
            source_file_extension=extension,
            source_display_label=display_label,
        )

    return _SourceValidation(
        source_path=source_path.resolve(),
        source_artifact_label=source_artifact_label,
        source_display_label=display_label,
        source_file_extension=".jsonl",
    )


def _invalid_source(
    error: str,
    *,
    source_file_extension: str = "",
    source_display_label: str = "<selected_jsonl>",
) -> _SourceValidation:
    return _SourceValidation(
        source_path=None,
        source_artifact_label=None,
        source_display_label=source_display_label,
        source_file_extension=source_file_extension,
        error=error,
    )


def _normalize_source_path_text(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return stripped[1:-1].strip()
    return stripped


def _job_payload(
    *,
    job_id: str,
    status: str,
    phase: str,
    created_at: str,
    started_at: str,
    finished_at: str,
    source: _SourceValidation,
    adapter: dict[str, object],
    ingest: dict[str, object],
    database: dict[str, object],
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    return {
        "object": MANUAL_JSONL_IMPORT_OBJECT,
        "schema_version": MANUAL_JSONL_IMPORT_SCHEMA_VERSION,
        "job_id": job_id,
        "status": status,
        "phase": phase,
        "created_at": created_at,
        "started_at": started_at,
        "finished_at": finished_at,
        "source": {
            "source_kind": "saved_event_replay",
            "source_artifact_label": _safe_label_or_empty(source.source_artifact_label),
            "source_display_label": source.source_display_label,
            "source_file_extension": source.source_file_extension,
            "path_echoed": False,
        },
        "adapter": adapter,
        "ingest": ingest,
        "database": database,
        "warnings": warnings,
        "errors": errors,
    }


def _store_job(job: dict[str, object]) -> dict[str, object]:
    job_id = str(job["job_id"])
    _JOBS[job_id] = job
    while len(_JOBS) > _MAX_STORED_JOBS:
        _JOBS.popitem(last=False)
    return dict(job)


def _source_with_adapter_label(source: _SourceValidation, source_artifact_label: str) -> _SourceValidation:
    return _SourceValidation(
        source_path=source.source_path,
        source_artifact_label=source_artifact_label,
        source_display_label=source.source_display_label,
        source_file_extension=source.source_file_extension,
    )


def _adapter_summary(
    status: str,
    result: object | None = None,
    *,
    ingest_warnings: list[str] | None = None,
    failure_code: str | None = None,
) -> dict[str, object]:
    if result is None:
        summary: dict[str, object] = {
            "status": status,
            "files_processed": 0,
            "records_seen": 0,
            "events_processed": 0,
            "events_skipped": 0,
            "unsupported_kind_counts": {},
            "warnings": [],
        }
        if status == "failed":
            summary["quality"] = failed_legacy_jsonl_import_quality(failure_code or "adapter_failed")
        return summary

    quality = _quality_with_ingest_warnings(dict(getattr(result, "quality")), ingest_warnings or [])
    return {
        "status": status,
        "files_processed": int(getattr(result, "files_processed")),
        "records_seen": int(getattr(result, "records_seen")),
        "events_processed": int(getattr(result, "events_processed")),
        "events_skipped": int(getattr(result, "events_skipped")),
        "unsupported_kind_counts": dict(getattr(result, "unsupported_kind_counts")),
        "warnings": list(getattr(result, "warnings")),
        "quality": quality,
    }


def _ingest_summary(status: str, result: object | None = None) -> dict[str, object]:
    if result is None:
        return {
            "status": status,
            "ingest_run_id": "",
            "source_kind": "saved_event_replay",
            "source_artifact_label": "",
            "row_counts": {},
            "warnings": [],
            "skipped": {},
        }
    return {
        "status": status,
        "ingest_run_id": str(getattr(result, "ingest_run_id")),
        "source_kind": str(getattr(result, "source_kind")),
        "source_artifact_label": str(getattr(result, "source_artifact_label")),
        "row_counts": dict(getattr(result, "row_counts")),
        "warnings": list(getattr(result, "warnings")),
        "skipped": dict(getattr(result, "skipped")),
    }


def _database_summary(*, status: str, created: bool) -> dict[str, object]:
    return {
        "status": status,
        "display_path": display_app_path("db", "mythic_edge.sqlite3"),
        "created": created,
    }


def _create_app_data_dirs(paths: LocalAppPaths) -> None:
    for path in (
        paths.config_dir,
        paths.db_dir,
        paths.logs_dir,
        paths.imports_dir,
        paths.jobs_dir,
        paths.diagnostics_dir,
    ):
        if path is not None:
            path.mkdir(parents=True, exist_ok=True)


def _warning_categories(adapter_result: object) -> list[str]:
    warnings: list[str] = []
    if getattr(adapter_result, "warnings"):
        warnings.append("adapter_warnings")
    if getattr(adapter_result, "unsupported_kind_counts"):
        warnings.append("unsupported_event_kinds")
    if int(getattr(adapter_result, "events_skipped")) > 0:
        warnings.append("events_skipped")
    return warnings


def _quality_with_ingest_warnings(quality: dict[str, object], ingest_warnings: list[str]) -> dict[str, object]:
    quality["ingest_warning_codes"] = _warning_codes(ingest_warnings)
    if quality.get("quality_status") == "complete" and ingest_warnings:
        quality["quality_status"] = "degraded"
    return quality


def _warning_codes(warnings: list[str]) -> list[str]:
    return sorted({_safe_quality_code(warning.split(":", maxsplit=1)[0]) for warning in warnings})


def _safe_quality_code(value: str) -> str:
    text = str(value or "").strip()
    marker_text = text.lower()
    if (
        text
        and len(text) <= 100
        and all(char.isalnum() or char in "_.:-" for char in text)
        and not any(marker in marker_text for marker in _PRIVATE_MARKERS)
    ):
        return text
    return "ingest_warning"


def _adapter_error_category(message: str) -> str:
    lowered = message.lower()
    if "invalid json" in lowered:
        return "invalid_jsonl"
    if "not valid utf-8" in lowered:
        return "invalid_utf8"
    if "safe label" in lowered:
        return "source_artifact_label_invalid"
    if "no ingestable" in lowered:
        return "no_ingestable_rows"
    if "malformed saved event record" in lowered:
        return "malformed_saved_event"
    return "adapter_failed"


def _looks_like_url(value: str) -> bool:
    if "://" in value:
        return True
    parsed = urlparse(value)
    return bool(parsed.scheme) and not _WINDOWS_DRIVE_PATH_RE.match(value)


def _looks_like_unc_path(value: str) -> bool:
    return bool(_UNC_PATH_RE.match(value.strip()))


def _safe_source_display_label(path: Path) -> str:
    name = path.name.strip()
    marker_text = name.lower()
    if (
        _SAFE_DISPLAY_BASENAME_RE.fullmatch(name)
        and "://" not in name
        and "\\" not in name
        and "/" not in name
        and "#" not in name
        and not any(marker in marker_text for marker in _PRIVATE_MARKERS)
    ):
        return name
    return "<selected_jsonl>"


def _safe_label_or_empty(value: str | None) -> str:
    if not value:
        return ""
    marker_text = value.lower()
    if _SAFE_LABEL_RE.fullmatch(value) and not any(marker in marker_text for marker in _PRIVATE_MARKERS):
        return value
    return ""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _default_job_id() -> str:
    return str(uuid.uuid4())
