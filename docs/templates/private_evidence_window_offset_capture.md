# Private Evidence Window Offset Capture Template

Use this template only after a future issue/contract and explicit user approval
authorize a local private-evidence window. This template is a checklist and
metadata shape. It is not executable tooling and it does not authorize reading
private logs by itself.

Keep real offset state local-only by default. Do not commit raw Player.log or
UTC_Log lines, exact private paths, exact offsets, exact file sizes, exact
private timestamps, raw hashes, app-data contents, runtime logs, SQLite files,
workbook exports, screenshots, credentials, tokens, webhook endpoints,
decklists, card choices, private strategy notes, private reports, or local-only
artifacts.

## Approval Record

- approved_issue:
- approved_source_class: `player_log` or `normalized_utc_log`
- approved_source_label: symbolic label only
- approved_window_label: symbolic window label only
- approved_window_start_action:
- approved_window_end_action:
- offset_capture_allowed: false
- appended_range_inspection_allowed: false
- operator_notes_allowed: false
- local_state_class:
- redacted_lifecycle_summary_allowed: false
- status_transition_authorized: false

## Local-Only Start Marker

Do not commit real values from this section.

- window_id:
- source_class:
- source_label:
- start_marker_captured_at_local: local_only_not_committed
- start_file_size_bytes: local_only_not_committed
- start_offset_bytes: local_only_not_committed
- start_source_generation_local: local_only_not_committed
- start_capture_tool_version:
- local_run_id:
- operator_start_note_allowed: false
- start_error:

## Local-Only End Marker

Do not commit real values from this section.

- window_id:
- end_marker_captured_at_local: local_only_not_committed
- end_file_size_bytes: local_only_not_committed
- end_offset_bytes: local_only_not_committed
- end_source_generation_local: local_only_not_committed
- end_capture_tool_version:
- local_run_id:
- operator_end_note_allowed: false
- end_error:

## Local-Only Derived Window Summary

Do not commit real values from this section unless a later contract authorizes a
redacted lifecycle summary candidate.

- range_mode: `offset_bounded`, `timestamp_bounded`, or `manual_review`
- start_offset_available:
- end_offset_available:
- end_offset_gte_start_offset:
- appended_byte_count: local_only_not_committed
- appended_range_read:
- fallback_reason:
- raw_lines_read_count: local_only_not_committed
- raw_lines_committed: false
- local_packet_verdict:
- redaction_status:

## Public Lifecycle Summary Candidate

Use this section only if a later approval explicitly allows a redacted
lifecycle summary candidate. Keep it symbolic and aggregate-only.

- issue:
- approval_reference:
- repo_branch:
- repo_commit:
- window_id:
- source_class:
- offset_capture_used:
- start_marker_recorded:
- end_marker_recorded:
- range_mode:
- range_read_scope:
- appended_byte_count_bucket:
- fallback_reason:
- redaction_checklist_status:
- raw_private_artifacts_stayed_local: true
- git_history_contains_private_artifacts: false

## Forbidden Public Fields

Do not include:

- exact private paths
- exact offsets from real runs
- exact file sizes from real runs
- exact private timestamps
- raw hashes
- raw log lines
- source filenames
- private app-data contents
- runtime logs
- SQLite contents
- workbook exports
- screenshots
- network identifiers
- packet details
- decklists
- card choices
- private strategy notes
- credentials, tokens, or webhook endpoints

## Redaction Checklist

- raw_log_lines_included: false
- raw_payloads_included: false
- exact_private_paths_included: false
- exact_offsets_included: false
- exact_file_sizes_included: false
- exact_private_timestamps_included: false
- raw_hashes_included: false
- local_only_state_included: false
- runtime_logs_included: false
- sqlite_files_included: false
- workbook_exports_included: false
- screenshots_included: false
- network_identifiers_included: false
- decklists_included: false
- card_choices_included: false
- private_strategy_notes_included: false
- credentials_tokens_webhooks_included: false

## Non-Claims

This template does not claim:

- parser support
- network reliability
- firewall/drop truth
- private smoke success
- drift health
- release readiness
- deploy readiness
- production behavior
- analytics truth
- AI truth
- coaching truth
- full corpus parity
- tracker completion
- corpus status promotion

Blocked corpus rows remain blocked unless a later explicit status-transition
contract and review authorize a change.
