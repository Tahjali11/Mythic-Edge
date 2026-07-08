# Parser Run Statistics And Dropped-Fact Counters Contract

Status: Draft contract for Codex B review
Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/531>
Parent umbrella: <https://github.com/Tahjali11/Mythic-Edge/issues/483>
Related issues: <https://github.com/Tahjali11/Mythic-Edge/issues/525>, <https://github.com/Tahjali11/Mythic-Edge/issues/526>, <https://github.com/Tahjali11/Mythic-Edge/issues/481>, <https://github.com/Tahjali11/Mythic-Edge/issues/568>
Target artifact: `docs/contracts/parser_run_statistics_and_dropped_fact_counters.md`
Risk tier: High workflow risk, low runtime risk while contract-only

## 1. Purpose

This contract defines a JSON-first, public-safe, report-only boundary for parser
run statistics and dropped-fact counters across replay, harvest, diagnostics, and
coverage-report workflows.

The contract exists to make three kinds of evidence visible without changing the
parser:

1. how much parser evidence a run considered;
2. which public-safe parser-owned fact families were observed, degraded, dropped,
   unresolved, duplicated, or blocked;
3. why a fact or event family was not carried forward into a stronger coverage,
   capture, or normalization claim.

The report is an evidence-pressure summary. It is not a parser behavior change,
truth approval mechanism, harvest authorization, fixture-promotion gate, corpus
status gate, release gate, or security/privacy assurance.

## 2. Non-Goals And Protected Boundaries

This contract does not authorize:

- parser behavior changes;
- parser event class changes;
- parser truth ownership changes;
- raw private `Player.log`, `UTC_Log`, app-data, workbook export, screenshot, or
  local runtime artifact reads;
- private harvest execution;
- fixture creation or promotion;
- Mythic Edge Corpus mutation;
- corpus readiness changes;
- CI changes or coverage enforcement;
- workbook, webhook, Apps Script, analytics, AI, coaching, frontend, or API
  behavior changes;
- claims of parser truth, coverage confirmation, readiness, release readiness,
  production readiness, security assurance, or privacy assurance.

The future implementation, if separately authorized, may only summarize
public-safe metadata and counters already supplied by approved replay, harvest,
diagnostics, or coverage-report surfaces.

## 3. Owning Layer And Truth Boundary

Owning layer: Corpus / Provenance, with Parser Reliability support.

Truth boundary:

- The parser/state layer remains the owner of parser-managed facts.
- The #481 parser-owned fact tracker remains the lifecycle scoreboard for fact
  capture and promotion progress.
- The future #525 phase-aware coverage contract owns canonical phase vocabulary
  once completed.
- The future #526 observed-but-dropped fact contract owns canonical
  observed-but-dropped fact vocabulary once completed.
- This contract owns only a public-safe report envelope, counter schema, and
  reason-code taxonomy for report-only statistics.

Counters may identify evidence pressure, data-loss pressure, or review pressure.
Counters must not rewrite parser facts, infer hidden truth, or upgrade lifecycle
status.

## 4. Accepted Workflow Kinds

`workflow_kind` must be one of:

- `replay`
- `harvest`
- `coverage_report`
- `parser_diagnostics`
- `drift_report`
- `parser_owned_fact_tracker_report`
- `synthetic_test`
- `manual_public_safe_summary`

Unknown workflow kinds are invalid unless a later contract extends the
vocabulary. Validators must fail closed on unknown workflow kinds.

## 5. Accepted Source Kinds

`source_kind` must be one of:

- `synthetic_fixture`
- `synthetic_player_log`
- `synthetic_utc_log`
- `synthetic_normalized_utc_log`
- `committed_public_fixture`
- `golden_replay_fixture`
- `user_selected_player_log`
- `user_selected_normalized_utc_log`
- `local_harvest_candidate_summary`
- `harvest_review_packet`
- `parser_diagnostics_report`
- `drift_report`
- `coverage_progress_report`
- `parser_owned_fact_tracker_report`
- `manual_public_safe_summary`

Private source kinds are allowed only as redacted labels. A report may say a run
was based on `user_selected_player_log`; it must not include the path, raw line
content, raw payload, account data, decklist, timestamp sequence, file hash, or
other source-identifying detail.

## 6. Phase Vocabulary Compatibility With #525

Until #525 defines the canonical phase vocabulary, this contract uses a
compatibility vocabulary:

- `draft_deckbuild_pre_game`
- `match_gameplay`
- `post_game_result`
- `connection_runtime`
- `local_harvest_review`
- `coverage_report`
- `corpus_fixture`
- `unknown_unrouted`
- `not_applicable`

Rules:

- A later #525 contract may supersede these names.
- Reports must keep unknown or unrouted phase pressure visible under
  `unknown_unrouted`; they must not merge unknown phase pressure into healthy or
  covered totals.
- `not_applicable` is allowed only for run-level counters that do not correspond
  to a parser fact phase.
- Phase counters are diagnostic and report-only. They do not prove coverage or
  fixture readiness.

## 7. Observed-But-Dropped Compatibility With #526

Until #526 defines the canonical observed-but-dropped vocabulary, this contract
uses a compatibility vocabulary:

- `observed`
- `preserved_raw`
- `normalized`
- `degraded`
- `dropped`
- `synthetic_covered`
- `committed_real_log_confirmed`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `duplicate_likely`
- `out_of_scope`
- `review_required`
- `unknown`

Rules:

- `observed` means a public-safe signal was seen by an approved summary surface.
  It does not mean the parser currently emits a normalized fact.
- `preserved_raw` may be used only for a public-safe field/path label or symbolic
  source reference. It must not echo raw private values.
- `normalized` means the approved input summary reports that a parser-owned fact
  was normalized. It must not be asserted from raw private logs in this contract.
- `dropped` means evidence was observed by an approved input summary but was not
  carried into the target report or downstream fact lifecycle.
- `degraded` means evidence was carried forward with reduced confidence,
  missing context, conflict, or source limitations.
- `synthetic_covered` and `committed_real_log_confirmed` are descriptive labels
  from upstream evidence surfaces only; they do not promote fixtures or corpus
  status.
- `blocked_private_evidence` and `blocked_external_boundary` must be visible
  stop states, not silent omissions.

## 8. Reason-Code Taxonomy

Reason codes must be lowercase ASCII slugs. They are public-safe categories, not
private evidence excerpts.

### 8.1 Source And Acquisition Reasons

- `source_kind_unsupported`
- `source_summary_missing`
- `source_context_unavailable`
- `source_unreadable_by_authorized_surface`
- `private_source_blocked`
- `external_boundary_blocked`
- `approved_summary_not_supplied`

### 8.2 Routing And Payload Reasons

- `unrouted_event_kind`
- `unknown_message_type`
- `malformed_payload`
- `malformed_json`
- `missing_required_field`
- `unexpected_schema_shape`
- `unsupported_schema_version`
- `timestamp_missing`
- `timestamp_parse_failure`

### 8.3 Identity And Relationship Reasons

- `unresolved_identifier`
- `orphan_target`
- `missing_match_identity`
- `missing_game_identity`
- `seat_mapping_unresolved`
- `object_identity_unresolved`
- `parent_child_relationship_unresolved`

### 8.4 Phase And Scope Reasons

- `phase_unknown`
- `phase_boundary_ambiguous`
- `phase_out_of_scope`
- `out_of_scope_format`
- `deferred_feature_expansion`
- `not_current_competitive_scope`
- `hidden_card_truth_forbidden`
- `strategy_inference_forbidden`

### 8.5 Privacy And Redaction Reasons

- `privacy_redaction_required`
- `raw_payload_suppressed`
- `raw_path_suppressed`
- `private_timestamp_sequence_suppressed`
- `decklist_suppressed`
- `account_identifier_suppressed`
- `secret_or_token_marker_blocked`

### 8.6 Duplicate And Replay Window Reasons

- `duplicate_window`
- `replay_window_overlap`
- `already_counted`
- `same_fact_family_duplicate`
- `duplicate_likely_requires_review`

### 8.7 Degradation And Conflict Reasons

- `partial_evidence`
- `conflicting_evidence`
- `stale_context`
- `truncated_source`
- `detailed_logs_disabled`
- `source_version_unknown`
- `runtime_context_missing`

### 8.8 Validation Reasons

- `unknown_counter_key`
- `counter_total_mismatch`
- `negative_counter_value`
- `non_integer_counter_value`
- `unknown_phase_kind`
- `unknown_observed_status`
- `unknown_reason_code`
- `unsafe_public_field`
- `readiness_overclaim`

Unknown reason codes must fail validation unless a later contract explicitly
extends the taxonomy.

## 9. JSON Report Envelope

The primary artifact must be JSON. Markdown summaries may be generated later only
as derived human-readable views of the JSON report.

Required top-level fields:

```json
{
  "object": "mythic_edge_parser_run_statistics_report",
  "schema_version": "parser_run_statistics_report.v1",
  "report_id": "parser-run-statistics-YYYYMMDDTHHMMSSZ-symbolic",
  "generated_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/531",
  "parent_umbrella": "https://github.com/Tahjali11/Mythic-Edge/issues/483",
  "related_issues": [],
  "run_context": {},
  "source_summary": {},
  "phase_summary": {},
  "run_counters": {},
  "fact_family_counters": [],
  "dropped_fact_counters": [],
  "degraded_fact_counters": [],
  "blocked_fact_counters": [],
  "coverage_report_links": {},
  "fact_tracker_links": {},
  "privacy": {},
  "validation": {},
  "readiness_flags": {},
  "authorization_flags": {},
  "non_claims": []
}
```

Validators must fail closed if required top-level fields are missing, if unknown
top-level fields appear without explicit schema-version support, or if any
readiness/authorization flag is missing or true when this contract requires it to
be false.

## 10. Run Context Schema

`run_context` must contain:

```json
{
  "workflow_kind": "replay|harvest|coverage_report|parser_diagnostics|drift_report|parser_owned_fact_tracker_report|synthetic_test|manual_public_safe_summary",
  "source_kind": "synthetic_fixture|synthetic_player_log|synthetic_utc_log|synthetic_normalized_utc_log|committed_public_fixture|golden_replay_fixture|user_selected_player_log|user_selected_normalized_utc_log|local_harvest_candidate_summary|harvest_review_packet|parser_diagnostics_report|drift_report|coverage_progress_report|parser_owned_fact_tracker_report|manual_public_safe_summary",
  "source_privacy_class": "public_fixture|synthetic|private_local_redacted|local_only_redacted|unknown",
  "operator_selection_mode": "none|synthetic|public_fixture|owner_selected_private_local|approved_summary_only",
  "run_scope": "single_file|single_session|multi_session|coverage_rollup|diagnostic_summary|unknown",
  "target_platform": "windows|macos|cross_platform|unknown|not_applicable",
  "schema_profile": "parser_run_statistics_report.v1"
}
```

Forbidden in `run_context`:

- local absolute paths;
- usernames;
- machine names;
- raw file names from private logs;
- file hashes derived from private sources;
- raw Arena timestamps;
- MTGA account identifiers;
- decklist values;
- webhook URLs;
- tokens or secrets.

## 11. Source Summary Schema

`source_summary` may include public-safe counts and symbolic references only:

```json
{
  "approved_input_artifact_ref": "symbolic-public-safe-ref",
  "approved_input_schema_version": "string",
  "input_artifact_family": "parser_diagnostics_report|drift_report|harvest_candidate_summary|coverage_progress_report|manual_public_safe_summary|unknown",
  "source_ref_is_symbolic": true,
  "raw_source_read_by_this_module": false,
  "private_values_included": false,
  "raw_payloads_included": false,
  "raw_paths_included": false
}
```

This report may consume sanitized summaries; it must not directly inspect raw
private logs.

## 12. Run Counters Schema

`run_counters` contains run-level numeric counts:

```json
{
  "source_units_seen": 0,
  "source_units_considered": 0,
  "source_units_skipped": 0,
  "parsed_entries": 0,
  "routed_entries": 0,
  "unknown_entries": 0,
  "malformed_entries": 0,
  "degraded_entries": 0,
  "duplicate_entries": 0,
  "redacted_values": 0,
  "warnings": 0,
  "errors": 0
}
```

Rules:

- All counter values must be non-negative integers.
- `source_units_seen` must not reveal source paths, private filenames, raw line
  numbers, byte offsets, or timestamp sequences.
- If a counter cannot be computed safely, the report must use `null` plus a
  `reason_code`; it must not guess.
- `routed_entries` plus `unknown_entries` is diagnostic only and must not be
  interpreted as parser health readiness.

## 13. Phase Summary Schema

`phase_summary` must be an object keyed by accepted `phase_kind` values. Each
phase bucket must use this shape:

```json
{
  "phase_kind": "match_gameplay",
  "source_units_considered": 0,
  "observed_fact_count": 0,
  "normalized_fact_count": 0,
  "dropped_fact_count": 0,
  "degraded_fact_count": 0,
  "blocked_fact_count": 0,
  "unknown_or_unrouted_count": 0,
  "dominant_reason_codes": []
}
```

Rules:

- Unknown or unrouted phase evidence must remain visible in
  `unknown_unrouted`.
- Phase buckets must not be converted into pass/fail readiness percentages.
- Phase buckets must not promote target matrix lifecycle status.

## 14. Fact Family Counter Schema

`fact_family_counters` must be a list of records:

```json
{
  "fact_family_id": "tier6.runtime_health_and_drift_detection.unknown_entry_count",
  "fact_family_label": "public-safe label",
  "phase_kind": "connection_runtime",
  "observed_status": "observed|preserved_raw|normalized|degraded|dropped|synthetic_covered|committed_real_log_confirmed|blocked_private_evidence|blocked_external_boundary|duplicate_likely|out_of_scope|review_required|unknown",
  "value_source_label": "observed|derived|inferred|unknown|conflict|legacy_enriched|not_applicable",
  "counter": 0,
  "reason_codes": [],
  "public_examples_included": false,
  "private_examples_included": false
}
```

Rules:

- `fact_family_id` may reference #481 target-matrix entries when available.
- The report must tolerate unknown fact families by using a symbolic
  `review_required` record rather than silently dropping them.
- `value_source_label` must use existing Mythic Edge value-source vocabulary.
- `public_examples_included` must remain false unless examples are synthetic or
  committed public fixtures.
- `private_examples_included` must always be false.

## 15. Dropped, Degraded, And Blocked Counter Schema

`dropped_fact_counters`, `degraded_fact_counters`, and `blocked_fact_counters`
must use the same record shape:

```json
{
  "counter_id": "symbolic-public-safe-id",
  "fact_family_id": "symbolic-or-known-fact-family-id",
  "phase_kind": "unknown_unrouted",
  "observed_status": "dropped",
  "reason_code": "unresolved_identifier",
  "count": 0,
  "first_observed_ref": "symbolic-public-safe-ref-or-null",
  "review_recommendation": "ignore|review|candidate_for_future_contract|blocked_until_authorized_input|unknown",
  "public_safe_note": "short category-only explanation",
  "raw_value_echoed": false,
  "private_path_echoed": false,
  "private_timestamp_echoed": false
}
```

Rules:

- Dropped counters are evidence-pressure counters, not bugs by default.
- High dropped counts may justify review but must not automatically open issues,
  alter parser behavior, or approve parser truth.
- Zero dropped counts must not be described as full coverage, readiness, or no
  data loss.
- `first_observed_ref` must be symbolic. It must not include source paths,
  offsets, private timestamps, hashes, snippets, or payload fragments.

## 16. Compatibility With #481 Parser-Owned Fact Tracker

`fact_tracker_links` may include:

```json
{
  "target_matrix_ref": "symbolic-ref-or-null",
  "session_capture_ledger_ref": "symbolic-ref-or-null",
  "coverage_progress_report_ref": "symbolic-ref-or-null",
  "fact_family_ids_used": []
}
```

Rules:

- #531 reports may reference #481 fact-family identifiers.
- #531 reports must not mutate #481 target matrices, session ledgers, coverage
  progress reports, lifecycle statuses, platform statuses, or promotion status.
- #531 reports may inform a future human review of coverage pressure.
- #531 reports must not set `parser_behavior_ready`,
  `pipeline_activation_ready_for_issue_388`, or fixture-promotion flags.

## 17. Public-Safe Markdown Summary Boundary

If a Markdown summary is later authorized, it must be derived from the JSON
report and may include only:

- report id;
- issue references;
- workflow kind;
- source kind as a redacted label;
- public-safe counts;
- phase bucket counts;
- reason-code counts;
- symbolic links to approved committed public artifacts.

It must not include:

- raw log lines;
- raw payloads;
- raw source snippets;
- raw diffs;
- private paths;
- private filenames;
- byte offsets;
- timestamp sequences;
- account identifiers;
- decklists;
- card-by-card private examples;
- webhook URLs, tokens, secrets, credentials, or environment values;
- readiness, truth, or assurance claims.

## 18. Required Privacy Section

`privacy` must include:

```json
{
  "public_safe": true,
  "raw_private_logs_read_by_this_module": false,
  "raw_payloads_included": false,
  "raw_source_snippets_included": false,
  "raw_paths_included": false,
  "private_filenames_included": false,
  "private_timestamps_included": false,
  "decklists_included": false,
  "account_identifiers_included": false,
  "secrets_or_tokens_included": false,
  "private_examples_included": false
}
```

Validators must fail closed if any value that must be false is true, missing, or
ambiguous.

## 19. Required Validation Section

`validation` must include:

```json
{
  "schema_validated": true,
  "reason_codes_validated": true,
  "phase_vocabulary_validated": true,
  "observed_status_vocabulary_validated": true,
  "counter_totals_validated": true,
  "public_safety_scan_passed": true,
  "readiness_flags_validated_false": true,
  "authorization_flags_validated_false": true,
  "validation_notes": []
}
```

Validators must reject:

- missing required fields;
- unknown workflow kinds;
- unknown source kinds;
- unknown phase kinds;
- unknown observed statuses;
- unknown reason codes;
- negative or non-integer counters;
- counter totals that cannot be reconciled and lack a reason code;
- private paths, source snippets, payload fragments, account identifiers, decklist
  values, secrets, tokens, or local-only paths;
- any readiness, truth, promotion, corpus, CI, security, or privacy-assurance
  overclaim.

## 20. Required False Flags

`readiness_flags` must include:

```json
{
  "parser_behavior_ready": false,
  "pipeline_activation_ready_for_issue_388": false,
  "fixture_promotion_ready": false,
  "corpus_readiness_claimed": false,
  "coverage_confirmed": false,
  "release_readiness_claimed": false,
  "deploy_readiness_claimed": false,
  "production_readiness_claimed": false,
  "security_assurance_claimed": false,
  "privacy_assurance_claimed": false
}
```

`authorization_flags` must include:

```json
{
  "implementation_authorized": false,
  "parser_behavior_change_authorized": false,
  "private_log_read_authorized": false,
  "private_harvest_authorized": false,
  "fixture_creation_authorized": false,
  "fixture_promotion_authorized": false,
  "corpus_status_change_authorized": false,
  "ci_change_authorized": false,
  "issue_creation_authorized": false,
  "pr_creation_authorized": false
}
```

The future implementation may not set these flags to true unless a later issue
and contract explicitly authorize that operation.

## 21. Required Non-Claims

Every report must include these `non_claims`:

- `not_parser_truth`
- `not_parser_behavior_change`
- `not_private_log_reader`
- `not_private_harvest_authorization`
- `not_fixture_creation`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_coverage_confirmation`
- `not_pipeline_activation_readiness`
- `not_release_readiness`
- `not_deploy_readiness`
- `not_production_behavior`
- `not_security_assurance`
- `not_privacy_assurance`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`
- `not_hidden_card_truth`
- `not_gameplay_advice`
- `not_player_mistake_label`
- `not_automatic_truth_approval`

## 22. Allowed Inputs

Allowed inputs for a future implementation, after explicit authorization:

- committed public fixtures;
- synthetic fixtures;
- public-safe parser diagnostics summaries;
- public-safe drift report summaries;
- public-safe local harvest candidate summaries;
- public-safe #481 coverage progress reports;
- public-safe manual summary objects supplied by the operator;
- symbolic issue, contract, and artifact references.

The implementation must treat all input as untrusted and validate schema,
privacy, reason codes, and flag boundaries before producing output.

## 23. Forbidden Inputs

Forbidden inputs:

- raw private `Player.log` files;
- raw private `UTC_Log` files;
- local MTGA app data;
- raw payloads;
- raw source snippets;
- raw diffs or patches;
- private paths or filenames;
- file hashes derived from private sources;
- private timestamp sequences;
- workbook exports;
- screenshots;
- private decklists;
- credentials, tokens, API keys, webhook URLs, or environment secrets;
- model/provider outputs;
- live MTGA data.

## 24. Side Effects

This contract authorizes no side effects.

A future implementation must not:

- write fixtures;
- promote fixtures;
- update corpus metadata;
- mutate Mythic Edge Corpus;
- update #481 ledgers;
- update GitHub issues or PRs;
- write CI artifacts;
- create runtime artifacts from private evidence;
- call external APIs;
- send webhooks;
- alter parser behavior.

Report writing, if later authorized, must be limited to explicit public-safe
JSON/Markdown output paths named by that later issue.

## 25. Example Public-Safe Report Fragment

This example is symbolic and synthetic. It is not evidence of real parser
coverage.

```json
{
  "object": "mythic_edge_parser_run_statistics_report",
  "schema_version": "parser_run_statistics_report.v1",
  "report_id": "parser-run-statistics-20260708T000000Z-example",
  "generated_at_utc": "2026-07-08T00:00:00Z",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/531",
  "parent_umbrella": "https://github.com/Tahjali11/Mythic-Edge/issues/483",
  "related_issues": [
    "https://github.com/Tahjali11/Mythic-Edge/issues/525",
    "https://github.com/Tahjali11/Mythic-Edge/issues/526",
    "https://github.com/Tahjali11/Mythic-Edge/issues/481"
  ],
  "run_context": {
    "workflow_kind": "synthetic_test",
    "source_kind": "synthetic_fixture",
    "source_privacy_class": "synthetic",
    "operator_selection_mode": "synthetic",
    "run_scope": "single_session",
    "target_platform": "not_applicable",
    "schema_profile": "parser_run_statistics_report.v1"
  },
  "source_summary": {
    "approved_input_artifact_ref": "synthetic-public-safe-ref",
    "approved_input_schema_version": "synthetic.v1",
    "input_artifact_family": "manual_public_safe_summary",
    "source_ref_is_symbolic": true,
    "raw_source_read_by_this_module": false,
    "private_values_included": false,
    "raw_payloads_included": false,
    "raw_paths_included": false
  },
  "phase_summary": {
    "match_gameplay": {
      "phase_kind": "match_gameplay",
      "source_units_considered": 3,
      "observed_fact_count": 2,
      "normalized_fact_count": 1,
      "dropped_fact_count": 1,
      "degraded_fact_count": 0,
      "blocked_fact_count": 0,
      "unknown_or_unrouted_count": 0,
      "dominant_reason_codes": ["unresolved_identifier"]
    }
  },
  "run_counters": {
    "source_units_seen": 3,
    "source_units_considered": 3,
    "source_units_skipped": 0,
    "parsed_entries": 3,
    "routed_entries": 2,
    "unknown_entries": 1,
    "malformed_entries": 0,
    "degraded_entries": 0,
    "duplicate_entries": 0,
    "redacted_values": 0,
    "warnings": 1,
    "errors": 0
  },
  "fact_family_counters": [
    {
      "fact_family_id": "tier6.runtime_health_and_drift_detection.unknown_entry_count",
      "fact_family_label": "Unknown entry count",
      "phase_kind": "connection_runtime",
      "observed_status": "observed",
      "value_source_label": "observed",
      "counter": 1,
      "reason_codes": ["unrouted_event_kind"],
      "public_examples_included": false,
      "private_examples_included": false
    }
  ],
  "dropped_fact_counters": [
    {
      "counter_id": "synthetic-drop-001",
      "fact_family_id": "synthetic.match_gameplay.object_identity",
      "phase_kind": "match_gameplay",
      "observed_status": "dropped",
      "reason_code": "unresolved_identifier",
      "count": 1,
      "first_observed_ref": "symbolic-public-safe-ref",
      "review_recommendation": "review",
      "public_safe_note": "Identifier was unavailable in the approved summary.",
      "raw_value_echoed": false,
      "private_path_echoed": false,
      "private_timestamp_echoed": false
    }
  ],
  "degraded_fact_counters": [],
  "blocked_fact_counters": [],
  "coverage_report_links": {},
  "fact_tracker_links": {},
  "privacy": {
    "public_safe": true,
    "raw_private_logs_read_by_this_module": false,
    "raw_payloads_included": false,
    "raw_source_snippets_included": false,
    "raw_paths_included": false,
    "private_filenames_included": false,
    "private_timestamps_included": false,
    "decklists_included": false,
    "account_identifiers_included": false,
    "secrets_or_tokens_included": false,
    "private_examples_included": false
  },
  "validation": {
    "schema_validated": true,
    "reason_codes_validated": true,
    "phase_vocabulary_validated": true,
    "observed_status_vocabulary_validated": true,
    "counter_totals_validated": true,
    "public_safety_scan_passed": true,
    "readiness_flags_validated_false": true,
    "authorization_flags_validated_false": true,
    "validation_notes": []
  },
  "readiness_flags": {
    "parser_behavior_ready": false,
    "pipeline_activation_ready_for_issue_388": false,
    "fixture_promotion_ready": false,
    "corpus_readiness_claimed": false,
    "coverage_confirmed": false,
    "release_readiness_claimed": false,
    "deploy_readiness_claimed": false,
    "production_readiness_claimed": false,
    "security_assurance_claimed": false,
    "privacy_assurance_claimed": false
  },
  "authorization_flags": {
    "implementation_authorized": false,
    "parser_behavior_change_authorized": false,
    "private_log_read_authorized": false,
    "private_harvest_authorized": false,
    "fixture_creation_authorized": false,
    "fixture_promotion_authorized": false,
    "corpus_status_change_authorized": false,
    "ci_change_authorized": false,
    "issue_creation_authorized": false,
    "pr_creation_authorized": false
  },
  "non_claims": [
    "not_parser_truth",
    "not_parser_behavior_change",
    "not_private_log_reader",
    "not_private_harvest_authorization",
    "not_fixture_creation",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_coverage_confirmation",
    "not_pipeline_activation_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_behavior",
    "not_security_assurance",
    "not_privacy_assurance",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
    "not_hidden_card_truth",
    "not_gameplay_advice",
    "not_player_mistake_label",
    "not_automatic_truth_approval"
  ]
}
```

## 26. Future Implementation Boundary

A future Codex C implementation may be considered only after Codex E accepts this
contract and the issue explicitly authorizes implementation.

The narrow future implementation may add:

- a pure builder for the JSON report envelope;
- a pure validator for the schema, counters, vocabularies, false flags, and
  privacy/no-echo rules;
- focused tests with synthetic/public-safe inputs only;
- an optional derived Markdown summary generator from validated JSON.

It must not add:

- raw log readers;
- harvest execution;
- parser route changes;
- parser fact normalization changes;
- fixture creation or promotion;
- corpus metadata updates;
- CI gates;
- external writes;
- issue/PR automation;
- readiness claims.

## 27. Future Validation Expectations

Later implementation validation should include at minimum:

- `PYTHONPATH=src python3 -m pytest -q tests/test_parser_run_statistics_and_dropped_fact_counters.py`
- focused compatibility tests against #481 fact-family ids;
- focused compatibility tests for the #525 phase vocabulary fallback;
- focused compatibility tests for the #526 observed-but-dropped vocabulary
  fallback;
- validator tests that reject unknown workflow kinds, source kinds, phase kinds,
  observed statuses, reason codes, and counter-total mismatches;
- validator tests that reject private paths, raw payload snippets, decklists,
  account identifiers, timestamp sequences, secrets, and readiness overclaims;
- `python3 tools/check_agent_docs.py`;
- `python3 tools/check_secret_patterns.py docs/contracts/parser_run_statistics_and_dropped_fact_counters.md`;
- `python3 tools/check_protected_surfaces.py --base origin/main` when available
  and relevant;
- `git diff --check`.

## 28. Acceptance Criteria For This Contract

This Codex B artifact is complete when:

- the report envelope and required schema fields are defined;
- run, phase, fact-family, dropped, degraded, and blocked counters are defined;
- #525 compatibility is explicit and fail-closed;
- #526 compatibility is explicit and fail-closed;
- reason codes are public-safe and enumerated;
- public-safe/no-echo rules are explicit;
- required false flags and non-claims are explicit;
- validation expectations are defined;
- no implementation, private log read, fixture promotion, corpus mutation, CI
  change, or readiness claim is introduced.

## 29. Recommended Next Role

Recommended next role: Codex E contract review.

Codex E should review the contract for schema clarity, #525/#526 compatibility,
reason-code completeness, public-safe/no-echo boundaries, and absence of hidden
implementation authority. Codex C should wait until Codex E accepts the contract
and the issue explicitly authorizes implementation.

## 30. Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for parser evidence issue #531.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/531

Parent umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/483

Related issues:
https://github.com/Tahjali11/Mythic-Edge/issues/525
https://github.com/Tahjali11/Mythic-Edge/issues/526
https://github.com/Tahjali11/Mythic-Edge/issues/481
https://github.com/Tahjali11/Mythic-Edge/issues/568

Target artifact:
docs/contracts/parser_run_statistics_and_dropped_fact_counters.md

Goal:
Review the JSON-first, public-safe, report-only parser run statistics and
dropped-fact counters contract. Verify schema clarity, #525 phase-aware coverage
compatibility, #526 observed-but-dropped fact compatibility, reason-code
taxonomy, no-echo privacy rules, false flags, and non-claims.

Protected boundaries:
Do not implement code, change parser behavior, change parser truth ownership,
read private logs, activate corpus promotion, create fixtures, mutate corpus
status, change CI, or claim parser truth/readiness/security/privacy.

Expected output:
Findings first, validation reviewed, whether Codex C may be recommended later,
remaining risks, and workflow_handoff.
```

## 31. Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/531"
  parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/525"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/526"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/481"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  verdict: "parser_run_statistics_and_dropped_fact_counters_contract_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/parser_run_statistics_and_dropped_fact_counters.md"
  implementation_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  private_log_read_authorized: false
  private_harvest_authorized: false
  fixture_creation_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  ci_change_authorized: false
  coverage_confirmed: false
  parser_truth_claimed: false
  readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
