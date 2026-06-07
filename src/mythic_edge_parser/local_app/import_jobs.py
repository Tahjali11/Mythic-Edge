from __future__ import annotations

import re
import sqlite3
import uuid
from collections import OrderedDict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_legacy_jsonl_adapter import (
    BROWSER_JSONL_UPLOAD_SOURCE_MODE,
    LegacyJsonlAdapterError,
    LegacyJsonlUploadSource,
    adapt_legacy_jsonl_artifacts,
    adapt_legacy_jsonl_file_batch,
    adapt_legacy_jsonl_upload_batch,
    failed_legacy_jsonl_import_quality,
)

from .paths import LocalAppPaths, build_local_app_paths, display_app_path

MANUAL_JSONL_IMPORT_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1"
MANUAL_JSONL_IMPORT_OBJECT = "mythic_edge_local_app_manual_jsonl_import_job"
MAX_LEGACY_JSONL_BATCH_FILES = 100
MAX_BROWSER_JSONL_UPLOAD_FILES = 100
MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES = 25 * 1024 * 1024
MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES = 250 * 1024 * 1024

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
    source_mode: str = "single_file"
    source_paths: tuple[Path, ...] = ()
    upload_sources: tuple[LegacyJsonlUploadSource, ...] = ()
    files_selected: int = 0
    files_accepted: int = 0
    files_rejected: int = 0
    source_artifacts: tuple[dict[str, object], ...] = ()
    error: str | None = None


@dataclass(frozen=True, slots=True)
class BrowserJsonlUploadFile:
    filename: str
    content_bytes: bytes
    content_type: str = ""


def run_manual_jsonl_import(
    request: object,
    *,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]:
    return _run_import_from_source(
        _validate_source_request(request),
        app_data_root=app_data_root,
        now=now,
        job_id_factory=job_id_factory,
    )


def run_browser_jsonl_upload_import(
    files: Sequence[BrowserJsonlUploadFile],
    *,
    source_artifact_label: str | None = None,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]:
    return _run_import_from_source(
        _validate_upload_request(files, source_artifact_label=source_artifact_label),
        app_data_root=app_data_root,
        now=now,
        job_id_factory=job_id_factory,
    )


def reject_browser_jsonl_upload_import(
    error: str,
    *,
    files_selected: int = 0,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]:
    return _run_import_from_source(
        _invalid_source(
            error,
            source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
            source_file_extension=".jsonl",
            files_selected=max(0, files_selected),
        ),
        app_data_root=app_data_root,
        now=now,
        job_id_factory=job_id_factory,
    )


def _run_import_from_source(
    source: _SourceValidation,
    *,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]:
    now_fn = now or _utc_now
    created_at = now_fn()
    job_id = (job_id_factory or _default_job_id)()
    if source.error is not None or not _source_has_selection(source):
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
        adapter_result = _adapt_source(source)
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
                source=_source_with_adapter_result(source, adapter_result),
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
                source=_source_with_adapter_result(source, adapter_result),
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
                source=_source_with_adapter_result(source, adapter_result),
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
            source=_source_with_adapter_result(source, adapter_result),
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

    has_source_path = "source_path" in request
    has_source_paths = "source_paths" in request
    if has_source_path and has_source_paths:
        return _invalid_source("source_path_and_source_paths_conflict")
    if has_source_paths:
        return _validate_batch_source_request(request)
    if not has_source_path:
        return _invalid_source("source_path_required")
    return _validate_single_source_request(request)


def _validate_upload_request(
    files: Sequence[BrowserJsonlUploadFile],
    *,
    source_artifact_label: str | None,
) -> _SourceValidation:
    if isinstance(files, (str, bytes)) or not files:
        return _invalid_source("upload_files_required", source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE)
    if len(files) > MAX_BROWSER_JSONL_UPLOAD_FILES:
        return _invalid_source(
            "upload_files_too_many",
            source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
            files_selected=len(files),
        )

    if source_artifact_label is not None:
        if not isinstance(source_artifact_label, str) or not source_artifact_label.strip():
            return _invalid_source(
                "source_artifact_label_invalid",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                files_selected=len(files),
            )
        safe_source_artifact_label = source_artifact_label.strip()
        if _safe_label_or_empty(safe_source_artifact_label) != safe_source_artifact_label:
            return _invalid_source(
                "source_artifact_label_invalid",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                files_selected=len(files),
            )
    else:
        safe_source_artifact_label = None

    upload_sources: list[LegacyJsonlUploadSource] = []
    total_size = 0
    for index, upload_file in enumerate(files):
        raw_filename = str(upload_file.filename or "").strip()
        basename = _uploaded_basename(raw_filename)
        if not basename:
            return _invalid_source(
                "upload_filename_required",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                files_selected=len(files),
            )
        display_label = _safe_uploaded_display_label(basename)
        if Path(basename).suffix.lower() != ".jsonl":
            return _invalid_source(
                "upload_file_extension_not_allowed",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=Path(basename).suffix.lower(),
                source_display_label=display_label,
                files_selected=len(files),
            )

        content_bytes = bytes(upload_file.content_bytes)
        size_bytes = len(content_bytes)
        if size_bytes <= 0:
            return _invalid_source(
                "upload_file_empty",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                source_display_label=display_label,
                files_selected=len(files),
            )
        if size_bytes > MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES:
            return _invalid_source(
                "upload_file_too_large",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                source_display_label=display_label,
                files_selected=len(files),
            )
        total_size += size_bytes
        if total_size > MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES:
            return _invalid_source(
                "upload_total_size_too_large",
                source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
                source_file_extension=".jsonl",
                files_selected=len(files),
            )

        upload_sources.append(
            LegacyJsonlUploadSource(
                display_name=basename,
                content_bytes=content_bytes,
                size_bytes=size_bytes,
                original_index=index,
            )
        )

    return _SourceValidation(
        source_path=None,
        upload_sources=tuple(upload_sources),
        source_artifact_label=safe_source_artifact_label,
        source_display_label=f"{len(upload_sources)} uploaded JSONL files",
        source_file_extension=".jsonl",
        source_mode=BROWSER_JSONL_UPLOAD_SOURCE_MODE,
        files_selected=len(files),
        files_accepted=len(upload_sources),
        files_rejected=0,
    )


def _validate_single_source_request(request: Mapping[object, object]) -> _SourceValidation:
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
        files_selected=1,
        files_accepted=1,
    )


def _validate_batch_source_request(request: Mapping[object, object]) -> _SourceValidation:
    raw_source_paths = request.get("source_paths")
    if not isinstance(raw_source_paths, list):
        return _invalid_source("source_paths_required", source_mode="explicit_file_batch")
    if not raw_source_paths:
        return _invalid_source("source_paths_empty", source_mode="explicit_file_batch")
    if len(raw_source_paths) > MAX_LEGACY_JSONL_BATCH_FILES:
        return _invalid_source(
            "source_paths_too_many",
            source_mode="explicit_file_batch",
            files_selected=len(raw_source_paths),
        )

    raw_label = request.get("source_artifact_label")
    if raw_label is not None:
        if not isinstance(raw_label, str) or not raw_label.strip():
            return _invalid_source(
                "source_artifact_label_invalid",
                source_mode="explicit_file_batch",
                source_file_extension=".jsonl",
            )
        source_artifact_label = raw_label.strip()
    else:
        source_artifact_label = None

    selected: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for raw_source_path in raw_source_paths:
        if not isinstance(raw_source_path, str) or not raw_source_path.strip():
            return _invalid_source(
                "source_path_invalid",
                source_mode="explicit_file_batch",
                source_file_extension=".jsonl",
                files_selected=len(raw_source_paths),
            )

        source_text = _normalize_source_path_text(raw_source_path)
        source_path = Path(source_text)
        extension = source_path.suffix.lower()
        display_label = _safe_source_display_label(source_path)

        if _looks_like_url(source_text):
            return _invalid_source(
                "source_path_url_not_allowed",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )
        if _looks_like_unc_path(source_text):
            return _invalid_source(
                "source_path_unc_not_allowed",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )
        if not source_path.exists():
            return _invalid_source(
                "source_path_missing",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )
        if source_path.is_dir():
            return _invalid_source(
                "source_path_directory_not_allowed",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )
        if extension != ".jsonl":
            return _invalid_source(
                "source_path_extension_not_allowed",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )
        if not source_path.is_file():
            return _invalid_source(
                "source_path_not_file",
                source_mode="explicit_file_batch",
                source_file_extension=extension,
                source_display_label=display_label,
                files_selected=len(raw_source_paths),
            )

        resolved_path = source_path.resolve()
        key = str(resolved_path).casefold()
        if key in seen:
            return _invalid_source(
                "source_path_duplicate",
                source_mode="explicit_file_batch",
                source_file_extension=".jsonl",
                files_selected=len(raw_source_paths),
            )
        seen.add(key)
        selected.append((resolved_path, source_text))

    sorted_paths = tuple(path for path, _ in sorted(selected, key=lambda item: (str(item[0]).casefold(), item[1])))
    return _SourceValidation(
        source_path=None,
        source_paths=sorted_paths,
        source_artifact_label=source_artifact_label,
        source_display_label=f"{len(sorted_paths)} selected JSONL files",
        source_file_extension=".jsonl",
        source_mode="explicit_file_batch",
        files_selected=len(raw_source_paths),
        files_accepted=len(sorted_paths),
        files_rejected=0,
    )


def _invalid_source(
    error: str,
    *,
    source_file_extension: str = "",
    source_display_label: str = "<selected_jsonl>",
    source_mode: str = "single_file",
    files_selected: int = 0,
    files_accepted: int = 0,
    files_rejected: int = 0,
) -> _SourceValidation:
    return _SourceValidation(
        source_path=None,
        source_artifact_label=None,
        source_display_label=source_display_label,
        source_file_extension=source_file_extension,
        source_mode=source_mode,
        files_selected=files_selected,
        files_accepted=files_accepted,
        files_rejected=files_rejected,
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
            "source_mode": source.source_mode,
            "files_selected": source.files_selected,
            "files_accepted": source.files_accepted,
            "files_rejected": source.files_rejected,
            "source_group_label": _safe_label_or_empty(source.source_artifact_label),
            "source_artifacts": list(source.source_artifacts),
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


def _source_has_selection(source: _SourceValidation) -> bool:
    if source.source_mode == BROWSER_JSONL_UPLOAD_SOURCE_MODE:
        return bool(source.upload_sources)
    if source.source_mode == "explicit_file_batch":
        return bool(source.source_paths)
    return source.source_path is not None


def _adapt_source(source: _SourceValidation) -> object:
    if source.source_mode == BROWSER_JSONL_UPLOAD_SOURCE_MODE:
        return adapt_legacy_jsonl_upload_batch(
            source.upload_sources,
            source_artifact_label=source.source_artifact_label,
        )
    if source.source_mode == "explicit_file_batch":
        return adapt_legacy_jsonl_file_batch(
            source.source_paths,
            source_artifact_label=source.source_artifact_label,
        )
    if source.source_path is None:
        raise LegacyJsonlAdapterError("source_path_required")
    return adapt_legacy_jsonl_artifacts(
        source.source_path,
        source_artifact_label=source.source_artifact_label,
    )


def _source_with_adapter_result(source: _SourceValidation, adapter_result: object) -> _SourceValidation:
    return _SourceValidation(
        source_path=source.source_path,
        source_paths=source.source_paths,
        upload_sources=source.upload_sources,
        source_artifact_label=str(getattr(adapter_result, "source_artifact_label")),
        source_display_label=source.source_display_label,
        source_file_extension=source.source_file_extension,
        source_mode=str(getattr(adapter_result, "source_mode", source.source_mode)),
        files_selected=int(getattr(adapter_result, "files_selected", source.files_selected)),
        files_accepted=int(getattr(adapter_result, "files_accepted", source.files_accepted)),
        files_rejected=int(getattr(adapter_result, "files_rejected", source.files_rejected)),
        source_artifacts=tuple(_safe_source_artifact_summaries(getattr(adapter_result, "source_artifacts", []))),
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
            "source_mode": "",
            "files_selected": 0,
            "files_accepted": 0,
            "files_rejected": 0,
            "source_artifacts": [],
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
        "source_mode": str(getattr(result, "source_mode", "single_file")),
        "files_selected": int(getattr(result, "files_selected", int(getattr(result, "files_processed")))),
        "files_accepted": int(getattr(result, "files_accepted", int(getattr(result, "files_processed")))),
        "files_rejected": int(getattr(result, "files_rejected", 0)),
        "source_artifacts": _safe_source_artifact_summaries(getattr(result, "source_artifacts", [])),
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


def _uploaded_basename(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return re.split(r"[\\/]+", text)[-1].strip()


def _safe_uploaded_display_label(value: str) -> str:
    return _safe_source_display_label(Path(value))


def _safe_label_or_empty(value: str | None) -> str:
    if not value:
        return ""
    marker_text = value.lower()
    if _SAFE_LABEL_RE.fullmatch(value) and not any(marker in marker_text for marker in _PRIVATE_MARKERS):
        return value
    return ""


def _safe_source_artifact_summaries(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []

    summaries: list[dict[str, object]] = []
    for entry in value:
        if not isinstance(entry, Mapping):
            continue
        summaries.append(
            {
                "batch_index": _non_negative_int(entry.get("batch_index")),
                "source_artifact_label": _safe_label_or_empty(str(entry.get("source_artifact_label") or "")),
                "source_display_label": _safe_display_label_text(entry.get("source_display_label")),
                "status": _safe_source_artifact_status(entry.get("status")),
                "records_seen": _non_negative_int(entry.get("records_seen")),
                "events_processed": _non_negative_int(entry.get("events_processed")),
                "events_skipped": _non_negative_int(entry.get("events_skipped")),
                "processed_kind_counts": _safe_count_map(entry.get("processed_kind_counts")),
                "unsupported_kind_counts": _safe_count_map(entry.get("unsupported_kind_counts")),
                "skipped_reason_counts": _safe_count_map(entry.get("skipped_reason_counts")),
                "adapter_warning_codes": _safe_code_list(entry.get("adapter_warning_codes")),
            }
        )
    return summaries


def _safe_display_label_text(value: object) -> str:
    text = str(value or "").strip()
    marker_text = text.lower()
    if (
        _SAFE_DISPLAY_BASENAME_RE.fullmatch(text)
        and "://" not in text
        and "\\" not in text
        and "/" not in text
        and "#" not in text
        and not any(marker in marker_text for marker in _PRIVATE_MARKERS)
    ):
        return text
    return "<selected_jsonl>"


def _safe_source_artifact_status(value: object) -> str:
    text = str(value or "").strip()
    if text in {"processed", "processed_with_skips", "rejected", "failed"}:
        return text
    return "processed"


def _safe_count_map(value: object) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, int] = {}
    for key, count in value.items():
        safe_key = _safe_quality_code(str(key))
        if safe_key:
            result[safe_key] = _non_negative_int(count)
    return dict(sorted(result.items()))


def _safe_code_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted({_safe_quality_code(str(entry)) for entry in value if _safe_quality_code(str(entry))})


def _non_negative_int(value: object) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, number)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _default_job_id() -> str:
    return str(uuid.uuid4())
