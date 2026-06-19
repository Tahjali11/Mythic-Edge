# Private Log Drift Private Evidence Execution Template

Use this template only after a later issue or contract and explicit user
approval authorize a local private-evidence drift review. This template is a
checklist and metadata shape. It is not executable tooling, and it does not
authorize reading private logs, running private checks, creating a public
summary, or promoting any corpus status.

Keep real source values and local drift artifacts local-only by default. Do not
commit raw Player.log or UTC_Log lines, exact private paths, exact offsets,
exact file sizes, exact private timestamps, raw hashes, raw signatures, raw API
names, app-data contents, runtime logs, database files, workbook exports,
screenshots, credential material, decklists, card choices, private strategy
notes, private reports, or local-only artifacts.

## Approval Record

Every future private drift review must start with an approval record. Leave the
default booleans false unless the approving issue or user instruction changes
that exact field.

- approved_issue:
- approved_source_class: `player_log` or `normalized_utc_log`
- approved_source_label: symbolic label only
- approved_window_label: symbolic label only
- approved_window_start_action:
- approved_window_end_action:
- offset_capture_allowed: false
- appended_range_inspection_allowed: false
- drift_report_execution_allowed: false
- drift_report_builder_allowed: none
- baseline_input_allowed: `none`
- refresh_baseline_allowed: false
- operator_notes_allowed: false
- local_state_class:
- redacted_lifecycle_summary_allowed: false
- redacted_drift_summary_allowed: false
- status_transition_authorized: false
- retention_policy:

## Offset Window Reference

The preferred future boundary is the #439 offset-window process. If offset
capture is approved, use
`docs/templates/private_evidence_window_offset_capture.md` for local-only start
and end marker capture. Do not copy real offset values into this file.

- offset_window_template:
  `docs/templates/private_evidence_window_offset_capture.md`
- window_id: `issue_442_private_log_drift_window_a`
- source_class:
- source_label: symbolic label only
- start_marker_status: `not_started`
- end_marker_status: `not_started`
- offset_window_verdict: `approval_required`

If offset metadata is unavailable, use one of these outcomes and stop before
reading private data unless a later approval explicitly allows the fallback:

- `approval_required`
- `offset_window_unavailable`
- `timestamp_fallback_requires_explicit_approval`
- `manual_review_required`
- `blocked_private_evidence_preserved`

## Local-Only Drift Execution Metadata

This section describes local-only metadata for a later approved review. Do not
commit real values from a private run.

- local_run_id: local_only_not_committed
- window_id: `issue_442_private_log_drift_window_a`
- source_class:
- source_label: symbolic label only
- range_mode: `offset_bounded`, `timestamp_bounded`, or `manual_review`
- range_read_scope: local_only_not_committed
- drift_report_builder: symbolic label only
- baseline_mode: `none`, `empty_in_memory_baseline`, or
  `symbolic_existing_local_baseline`
- baseline_refresh_performed: false
- local_report_created: false
- local_report_status: `not_run`
- local_report_object: local_only_not_committed
- entry_count_total: local_only_not_committed
- entry_count_routed: local_only_not_committed
- entry_count_unknown: local_only_not_committed
- unknown_rate_pct: local_only_not_committed
- timestamp_missing_count: local_only_not_committed
- timestamp_parse_failure_count: local_only_not_committed
- new_unknown_signature_count: local_only_not_committed
- new_unmatched_api_name_count: local_only_not_committed
- new_unmatched_request_api_name_count: local_only_not_committed
- local_packet_verdict: `not_run`
- redaction_status: `not_started`
- local_report_error: local_only_not_committed

## Baseline Handling

Use the safest baseline mode unless the approval record says otherwise.

- baseline_mode: `none`
- baseline_refresh_performed: false
- baseline_refresh_authorized: false
- baseline_contents_committed: false

Allowed baseline labels:

- `none`
- `empty_in_memory_baseline`
- `symbolic_existing_local_baseline`

## Optional Public Summary Candidate

Use this section only if a later approval explicitly allows a redacted public
summary candidate. Keep the values symbolic, boolean, or bucketed. Exact private
values remain local-only.

- issue:
- approval_reference:
- repo_branch:
- repo_commit:
- source_class:
- source_label: symbolic label only
- window_id:
- offset_capture_used:
- start_marker_recorded:
- end_marker_recorded:
- drift_execution_performed:
- drift_report_builder:
- baseline_mode:
- baseline_refresh_performed:
- range_mode:
- range_read_scope:
- entry_count_total_bucket: `not_reported`
- entry_count_unknown_bucket: `not_reported`
- unknown_rate_bucket: `not_reported`
- timestamp_issue_bucket: `not_reported`
- new_unknown_signature_bucket: `not_reported`
- new_unmatched_api_name_bucket: `not_reported`
- redaction_checklist_status:
- raw_private_artifacts_stayed_local: true
- git_history_contains_private_artifacts: false
- local_packet_verdict:
- status_transition_authorized: false

## Count Bucket Vocabulary

Use buckets instead of exact private counts unless a later contract and review
explicitly authorize more detail.

- `not_reported`
- `zero`
- `one`
- `few`
- `many`
- `unknown`
- `withheld_private`

## Redaction Checklist

- raw_log_lines_included: false
- raw_payloads_included: false
- exact_private_paths_included: false
- exact_offsets_included: false
- exact_file_sizes_included: false
- exact_private_timestamps_included: false
- raw_hashes_included: false
- raw_signatures_included: false
- raw_api_names_included: false
- raw_report_json_included: false
- baseline_contents_included: false
- local_only_state_included: false
- runtime_logs_included: false
- database_files_included: false
- workbook_exports_included: false
- screenshots_included: false
- network_identifiers_included: false
- decklists_included: false
- card_choices_included: false
- private_strategy_notes_included: false
- credential_material_included: false

## Forbidden Public Fields

Do not include these fields or values in committed artifacts:

- exact private paths
- exact offsets from real runs
- exact file sizes from real runs
- exact private timestamps
- raw hashes
- raw log lines
- raw signatures
- raw API names
- raw headers
- raw report JSON
- raw baseline JSON
- source filenames from private sources
- private app-data contents
- runtime logs or status files
- database contents
- workbook exports
- screenshots
- network identifiers
- packet details
- decklists
- card choices
- private strategy notes
- credential material

## Status Boundary

This template does not authorize status promotion. The selected corpus family
`mythic_edge.private_log_report_only_drift` remains
`blocked_private_evidence` by default. `connection.firewall_or_network_drop`
and every other blocked row also remain blocked unless a later explicit
status-transition contract and review authorize a change.

## Non-Claims

This template does not claim:

- private smoke success
- live Player.log health
- drift health
- parser support
- release readiness
- deploy readiness
- production behavior
- analytics truth
- AI truth
- coaching truth
- full corpus parity
- tracker completion
- parent issue completion
- corpus status promotion
