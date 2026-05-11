from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from .arena_id_validation import (
    GrpIdOverrideRefreshResult,
    discover_unresolved_grp_ids_from_saved_logs,
    grp_ids_requiring_evidence_refresh,
    refresh_grp_id_overrides_from_logs,
)
from .card_catalog import (
    DEFAULT_BULK_TYPE,
    DEFAULT_FORMAT,
    CatalogSyncResult,
    get_bulk_item,
    latest_arena_lookup_path,
    latest_catalog_json_path,
    latest_raw_source_path,
    load_combined_card_lookup,
    load_sync_state,
    source_stamp_from_bulk_item,
    sync_card_catalog,
    sync_history_path,
    update_sync_state,
)
from .config import CARD_CATALOG_REFRESH_STATUS_PATH, MATCH_LOGS_ROOT, ORACLE_DATA_ROOT
from .grp_id_candidates import (
    GrpIdCandidateReport,
    InferredReviewReport,
    build_grp_id_candidate_report,
    build_inferred_review_report,
    write_inferred_review_reports,
)

REQUEST_HEADERS = {
    "User-Agent": "Mythic Edge/1.0 (card catalog refresh pipeline)",
    "Accept": "application/json;q=0.9,*/*;q=0.8",
}
STALE_AFTER_DAYS = 45


@dataclass(slots=True)
class CardCatalogRefreshResult:
    generated_at: str
    format_key: str
    bulk_type: str
    sync_performed: bool
    sync_reason: str
    status_path: Path
    sync_state_path: Path
    sync_history_path: Path
    unresolved_target_grp_ids: int
    fingerprint_report_path: Path | None = None
    fingerprint_markdown_path: Path | None = None
    candidate_report_path: Path | None = None
    candidate_markdown_path: Path | None = None
    candidate_report_error: str = ""
    inferred_review_json_path: Path | None = None
    inferred_review_markdown_path: Path | None = None
    inferred_review_entry_count: int = 0
    inferred_review_report: InferredReviewReport | None = None
    sync_result: CatalogSyncResult | None = None
    override_refresh_result: GrpIdOverrideRefreshResult | None = None
    candidate_report: GrpIdCandidateReport | None = None

    def summary_line(self) -> str:
        action = "synced" if self.sync_performed else "reused current catalog"
        return (
            f"Card catalog refresh pipeline: {action}; "
            f"{self.unresolved_target_grp_ids} unresolved grpIds targeted for replay"
        )


def load_card_catalog_refresh_status(path: Path = CARD_CATALOG_REFRESH_STATUS_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_refresh_status(payload: dict[str, Any], path: Path = CARD_CATALOG_REFRESH_STATUS_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _build_refresh_status_payload(
    *,
    result: CardCatalogRefreshResult,
    last_successful_manual_refresh_at: str,
    output_dir: Path,
) -> dict[str, Any]:
    latest_lookup = latest_arena_lookup_path(
        format_key=result.format_key,
        bulk_type=result.bulk_type,
        output_dir=output_dir,
    )
    latest_catalog = latest_catalog_json_path(
        format_key=result.format_key,
        bulk_type=result.bulk_type,
        output_dir=output_dir,
    )
    latest_raw = latest_raw_source_path(bulk_type=result.bulk_type, output_dir=output_dir)

    payload: dict[str, Any] = {
        "object": "manasight_card_catalog_refresh_status",
        "generated_at": result.generated_at,
        "format": result.format_key,
        "bulk_type": result.bulk_type,
        "last_successful_manual_refresh_at": last_successful_manual_refresh_at,
        "stale_after_days": STALE_AFTER_DAYS,
        "sync_performed": result.sync_performed,
        "sync_reason": result.sync_reason,
        "activation_policy": "next_restart",
        "next_restart_required": result.sync_performed,
        "unresolved_target_grp_id_count": result.unresolved_target_grp_ids,
        "candidate_report_error": result.candidate_report_error,
        "inferred_review_entry_count": result.inferred_review_entry_count,
        "review_suggestions_pending": result.inferred_review_entry_count > 0,
        "sync_state_path": str(result.sync_state_path),
        "sync_history_path": str(result.sync_history_path),
    }
    if latest_catalog.exists():
        payload["latest_catalog_json_path"] = str(latest_catalog)
    if latest_lookup.exists():
        payload["latest_arena_lookup_json_path"] = str(latest_lookup)
    if latest_raw.exists():
        payload["latest_raw_source_path"] = str(latest_raw)
    if result.fingerprint_report_path is not None:
        payload["fingerprint_report_path"] = str(result.fingerprint_report_path)
    if result.fingerprint_markdown_path is not None:
        payload["fingerprint_markdown_path"] = str(result.fingerprint_markdown_path)
    if result.candidate_report_path is not None:
        payload["candidate_report_path"] = str(result.candidate_report_path)
    if result.candidate_markdown_path is not None:
        payload["candidate_markdown_path"] = str(result.candidate_markdown_path)
    if result.inferred_review_json_path is not None:
        payload["inferred_review_json_path"] = str(result.inferred_review_json_path)
    if result.inferred_review_markdown_path is not None:
        payload["inferred_review_markdown_path"] = str(result.inferred_review_markdown_path)
    if result.sync_result is not None:
        payload["sync_generated_at"] = result.sync_result.generated_at
        payload["source_download_url"] = result.sync_result.source_download_url
        payload["total_cards"] = result.sync_result.total_cards
    else:
        state_payload = load_sync_state(
            output_dir=output_dir,
            format_key=result.format_key,
            bulk_type=result.bulk_type,
        )
        if state_payload:
            payload["source_download_url"] = str(state_payload.get("source_download_url", "")).strip()
            payload["last_successful_sync_at"] = str(state_payload.get("last_successful_sync_at", "")).strip()
    return payload


def run_card_catalog_refresh_pipeline(
    *,
    format_key: str = DEFAULT_FORMAT,
    bulk_type: str = DEFAULT_BULK_TYPE,
    keep_download: bool = False,
    match_logs_root: Path = MATCH_LOGS_ROOT,
    output_dir: Path = ORACLE_DATA_ROOT,
    status_path: Path = CARD_CATALOG_REFRESH_STATUS_PATH,
) -> CardCatalogRefreshResult:
    checked_at = datetime.now(UTC).isoformat()
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    sync_result: CatalogSyncResult | None = None
    sync_reason = ""
    sync_state_record_path = output_dir / "missing-sync-state.json"

    try:
        bulk_item = get_bulk_item(session, bulk_type)
        source_stamp = source_stamp_from_bulk_item(bulk_item)
        sync_state = load_sync_state(output_dir, format_key=format_key, bulk_type=bulk_type)
        last_synced_source_stamp = str(sync_state.get("last_synced_source_stamp", "")).strip()
        try:
            latest_arena_lookup_path(
                format_key=format_key,
                bulk_type=bulk_type,
                output_dir=output_dir,
            )
            latest_lookup_exists = True
        except FileNotFoundError:
            latest_lookup_exists = False

        should_sync = not latest_lookup_exists or source_stamp != last_synced_source_stamp
        if not latest_lookup_exists:
            sync_reason = "local latest Arena lookup is missing"
        elif should_sync:
            sync_reason = "Scryfall bulk source changed"
        else:
            sync_reason = "Scryfall bulk source stamp is unchanged"

        if should_sync:
            sync_result = sync_card_catalog(
                format_key=format_key,
                bulk_type=bulk_type,
                keep_download=keep_download,
                session=session,
                bulk_item=bulk_item,
                output_dir=output_dir,
            )

        sync_state_record_path = update_sync_state(
            format_key=format_key,
            bulk_type=bulk_type,
            checked_at=checked_at,
            source_stamp=source_stamp,
            reason=sync_reason,
            synced=should_sync,
            manual_trigger=True,
            output_dir=output_dir,
            sync_result=sync_result,
        )
    finally:
        session.close()

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    if override_path.exists():
        try:
            override_payload = json.loads(override_path.read_text(encoding="utf-8"))
        except Exception:
            override_payload = {}
    else:
        override_payload = {}
    cards_by_grp_id = override_payload.get("cards_by_grp_id") if isinstance(override_payload, dict) else {}
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}
    combined_lookup = load_combined_card_lookup(
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )

    unresolved_target_grp_ids = grp_ids_requiring_evidence_refresh(cards_by_grp_id)
    unresolved_target_grp_ids |= discover_unresolved_grp_ids_from_saved_logs(
        match_logs_root=match_logs_root,
        resolved_lookup=combined_lookup,
    )

    override_refresh_result: GrpIdOverrideRefreshResult | None = None
    if unresolved_target_grp_ids:
        override_refresh_result = refresh_grp_id_overrides_from_logs(
            match_logs_root=match_logs_root,
            output_dir=output_dir,
            format_key=format_key,
            bulk_type=bulk_type,
            target_grp_ids=unresolved_target_grp_ids,
        )

    candidate_report: GrpIdCandidateReport | None = None
    candidate_report_error = ""
    inferred_review_report: InferredReviewReport | None = None
    inferred_review_json_path = None
    inferred_review_markdown_path = None
    inferred_review_entry_count = 0
    try:
        candidate_report = build_grp_id_candidate_report(
            match_logs_root=match_logs_root,
            output_dir=output_dir,
            format_key=format_key,
            bulk_type=bulk_type,
        )
    except (FileNotFoundError, ValueError) as exc:
        candidate_report_error = str(exc)

    inferred_review_report = build_inferred_review_report(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key=format_key,
        bulk_type=bulk_type,
    )
    inferred_review_entry_count = len(inferred_review_report.entries)
    inferred_review_json_path, inferred_review_markdown_path = write_inferred_review_reports(
        inferred_review_report,
        output_dir=output_dir,
    )
    result = CardCatalogRefreshResult(
        generated_at=datetime.now(UTC).isoformat(),
        format_key=format_key,
        bulk_type=bulk_type,
        sync_performed=sync_result is not None,
        sync_reason=sync_reason,
        status_path=status_path,
        sync_state_path=sync_state_record_path,
        sync_history_path=sync_history_path(output_dir),
        unresolved_target_grp_ids=len(unresolved_target_grp_ids),
        fingerprint_report_path=(
            override_refresh_result.fingerprint_report_path if override_refresh_result is not None else None
        ),
        fingerprint_markdown_path=(
            override_refresh_result.fingerprint_markdown_path if override_refresh_result is not None else None
        ),
        candidate_report_path=candidate_report.report_path if candidate_report is not None else None,
        candidate_markdown_path=candidate_report.markdown_report_path if candidate_report is not None else None,
        candidate_report_error=candidate_report_error,
        inferred_review_json_path=inferred_review_json_path,
        inferred_review_markdown_path=inferred_review_markdown_path,
        inferred_review_entry_count=inferred_review_entry_count,
        inferred_review_report=inferred_review_report,
        sync_result=sync_result,
        override_refresh_result=override_refresh_result,
        candidate_report=candidate_report,
    )
    sync_state_payload = load_sync_state(
        output_dir=output_dir,
        format_key=format_key,
        bulk_type=bulk_type,
    )
    status_payload = _build_refresh_status_payload(
        result=result,
        last_successful_manual_refresh_at=str(
            sync_state_payload.get("last_successful_manual_sync_at", "")
        ).strip(),
        output_dir=output_dir,
    )
    _write_refresh_status(status_payload, path=status_path)
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the full card-catalog refresh pipeline: sync Scryfall, refresh unresolved grpId evidence, "
            "rescore candidate matches, and write inferred review reports."
        )
    )
    parser.add_argument("--format", default=DEFAULT_FORMAT, help="Identity catalog scope. Default: arena.")
    parser.add_argument(
        "--bulk-type",
        default=DEFAULT_BULK_TYPE,
        help="Scryfall bulk-data type. Default: default_cards.",
    )
    parser.add_argument(
        "--keep-download",
        action="store_true",
        help="Also keep the temporary raw JSON download under data/oracle_data/_downloads.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    result = run_card_catalog_refresh_pipeline(
        format_key=args.format.strip().lower() or DEFAULT_FORMAT,
        bulk_type=args.bulk_type.strip() or DEFAULT_BULK_TYPE,
        keep_download=args.keep_download,
    )
    print(result.summary_line())
    print(f"Refresh status: {result.status_path}")
    if result.sync_result is not None:
        print(f"Arena lookup: {result.sync_result.arena_lookup_json_path}")
        print(f"Catalog JSON: {result.sync_result.catalog_json_path}")
        print(f"Raw source:   {result.sync_result.bulk_file_path}")
    if result.fingerprint_report_path is not None:
        print(f"Fingerprint report: {result.fingerprint_report_path}")
    if result.candidate_report_path is not None:
        print(f"Candidate report:   {result.candidate_report_path}")
    elif result.candidate_report_error:
        print(f"Candidate report skipped: {result.candidate_report_error}")
    if result.inferred_review_json_path is not None:
        print(f"Inferred review:    {result.inferred_review_json_path}")
    return 0
