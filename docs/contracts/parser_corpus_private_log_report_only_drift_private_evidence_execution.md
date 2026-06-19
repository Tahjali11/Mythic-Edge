# Parser Corpus Private Log Drift Private Evidence Execution Contract

## Module

Private log report-only drift private evidence execution scoping for the
`mythic_edge.private_log_report_only_drift` corpus family.

Plain English: this contract defines how a later, explicitly approved local
private evidence packet may be scoped for private Player.log or normalized
UTC_Log drift review. It uses the offset-window process from issue #439 as a
preferred safety boundary, but it does not run private checks, read private
logs in Codex B, implement executable tooling, commit private evidence, promote
the blocked row, or claim parser support, private smoke success, drift health,
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/442
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/439
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/441
- Previous merge commit:
  `85c0bdc7b6f674ad18828e903a6518531f9d3553`
- Related prior boundary: https://github.com/Tahjali11/Mythic-Edge/issues/422
- Parent/private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-private-log-drift-execution-442`
- base_branch: `main`
- observed_base_commit: `85c0bdc7b6f674ad18828e903a6518531f9d3553`
- target_artifact:
  `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority inspected:

- issue #442, tracker #158, issue #434, issue #439, issue #422, PR #441,
  and PR #423
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/templates/private_evidence_window_offset_capture.md`
- `docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/local_artifacts_manifest.json`
- `docs/internal_project_map.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_log_drift_sensor.py`
- parser-evidence workflow issues #381 through #387 as future pipeline
  context only

## Observed Current Behavior

Observed on `main` at
`85c0bdc7b6f674ad18828e903a6518531f9d3553`:

- Issue #442 is open.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- Issue #439 is closed after PR #441.
- Issue #422 is closed after PR #423.
- PR #441 is merged into `main`.
- PR #423 was merged into `codex/parser-parity` before the parser-parity line
  was later integrated.
- The corpus manifest contains
  `private_log_report_only_drift_private_evidence_boundary_v1`.
- `mythic_edge.private_log_report_only_drift` is
  `blocked_private_evidence`.
- The row has `coverage_basis == ["local_report_only"]`.
- The row has no parser event families and no committed private report paths.
- The session ledger has no `private_log_report_only_drift` session entry.
- The corpus parity CLI reports:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- `log_drift_sensor.py` can build a local drift report from a supplied log
  path and optional baseline, but its default report includes private-source
  path data and is a local/runtime artifact unless separately normalized and
  redacted.
- The #439 offset-capture contract and template define a safer future local
  window process, but they do not authorize private log reads, appended-range
  inspection, private drift execution, public summaries, or corpus status
  promotion by themselves.

## Scope Decision

This contract authorizes a V1 documentation/process scaffold for future
private-log drift execution packets.

Codex C may implement only docs/template support for this process:

- a metadata-only private-log drift execution checklist or template;
- an implementation handoff documenting that no private evidence was read;
- focused documentation, secret/private-marker, protected-surface,
  surface-authorization, corpus-parity, and whitespace validation.

Codex C must not implement executable private drift tooling in this slice.

Codex C must not run private drift checks in this slice.

Actual local private-log drift execution requires a later explicit user
approval that names the exact source class, symbolic source label, approved
window, artifact classes, offset policy, baseline policy, operator-note policy,
and redacted-summary policy. If that later approval is ambiguous, the workflow
must stop and route back to Codex A, Codex B, or the user.

This contract does not authorize status promotion for
`mythic_edge.private_log_report_only_drift`, `connection.firewall_or_network_drop`,
or any other blocked corpus row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns private evidence execution-scoping vocabulary, approval
requirements, redaction requirements, local-only artifact boundaries, and
non-claim language for future private-log drift evidence packets.

Quality / Governance owns review, validation, protected-surface checks,
secret/private-marker checks, and handoff discipline.

Generated / Local Artifacts owns any future local-only offset state, private
drift report, private drift baseline, operator note, or private packet.

This contract does not own parser interpretation, parser state final
reconciliation, parser events, router semantics, diagnostics behavior, drift
report implementation, local app watcher behavior, runtime status shape,
network behavior, live MTGA behavior, workbook behavior, webhook behavior,
Apps Script behavior, Google Sheets sync, analytics truth, AI truth, coaching
truth, release readiness, deploy readiness, production behavior, or tracker
completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting areas:

- Quality / Governance, for contracts, templates, handoffs, redaction checks,
  secret/private-marker scans, protected-surface gates, and review.
- Generated / Local Artifacts, for any later local-only source, offset state,
  private drift report, baseline, operator notes, or packet.

This is not a Parser module, diagnostics implementation, log-drift
implementation, local app module, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, readiness gate, or production module.

## Truth Owner

Current corpus status truth remains owned by:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Current private drift boundary truth remains owned by:

- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `private_log_report_only_drift_private_evidence_boundary_v1` in
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`

Current offset-window process truth remains owned by:

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/templates/private_evidence_window_offset_capture.md`

Future private drift execution state, if approved, is temporary local-only
process evidence. It may inform a later human-reviewed corpus evidence
decision, but it is not parser truth, live Player.log health truth, drift
health truth, readiness truth, analytics truth, AI truth, coaching truth, or
full corpus parity truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract does not authorize bridge code.

Potential future source area:

- Generated / Local Artifacts, if the user explicitly approves local private
  drift execution.

Potential future consuming area:

- Corpus / Provenance, if a later approved redacted summary candidate is
  reviewed and accepted.

Forbidden reverse flow:

- Private drift evidence must not change parser behavior, parser events,
  router dispatch, parser diagnostics, log-drift implementation, runtime
  status shape, corpus report semantics, workbook behavior, webhook behavior,
  Apps Script behavior, Google Sheets sync, output transport, analytics, AI,
  coaching, CI, merge, deploy, production, or tracker lifecycle.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`

Future Codex C docs-only files authorized by this contract:

- `docs/templates/private_log_drift_private_evidence_execution.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md`

Expected future Codex E review artifact:

- `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`

Files this contract may reference but does not authorize Codex C to change:

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/templates/private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_log_drift_sensor.py`
- adjacent diagnostics, unknown-entry, live-diagnostics, and corpus parity
  contracts, handoffs, reports, source, and focused tests

Not owned by this contract:

- raw Player.log files;
- normalized UTC_Log source files;
- local private offset state;
- local private drift reports;
- local private drift baselines;
- private app-data contents;
- private smoke outputs;
- runtime logs;
- runtime status files;
- failed posts;
- SQLite files;
- workbook exports;
- screenshots;
- raw hashes;
- exact private paths;
- exact offsets;
- exact file sizes;
- exact private timestamps;
- firewall logs;
- Wi-Fi logs;
- OS/router diagnostics;
- packet captures;
- network traces;
- secrets, credentials, tokens, API keys, or webhook URLs;
- decklists, card choices, or private strategy notes;
- parser source, parser events, runtime source, diagnostics source, drift
  source, workbook/webhook/App Script/Sheets surfaces, analytics, AI,
  coaching, CI, merge, deploy, production, or tracker lifecycle surfaces.

## Public Interface

This contract defines a metadata-only evidence execution-scoping interface for
future private-log drift evidence windows.

It adds no runtime public API, CLI, environment variable contract, parser event
class, parser payload shape, workbook schema, webhook payload shape, Apps
Script behavior, analytics schema, or local app behavior.

### Approval Record

A future private-log drift execution packet must have an approval record with:

- `approved_issue`: issue authorizing the local run;
- `approved_source_class`: `player_log` or `normalized_utc_log`;
- `approved_source_label`: symbolic label only, not an exact path or filename;
- `approved_window_label`: coarse symbolic window label;
- `approved_window_start_action`: operator action or marker label;
- `approved_window_end_action`: operator action or marker label;
- `offset_capture_allowed`: boolean;
- `appended_range_inspection_allowed`: boolean;
- `drift_report_execution_allowed`: boolean;
- `drift_report_builder_allowed`: symbolic builder label only, such as
  `existing_log_drift_sensor_local_only` or `manual_local_review`;
- `baseline_input_allowed`: `none`, `empty_in_memory_baseline`, or
  `symbolic_existing_local_baseline`;
- `refresh_baseline_allowed`: boolean, default false;
- `operator_notes_allowed`: boolean;
- `local_state_class`: allowed local-only artifact class;
- `redacted_lifecycle_summary_allowed`: boolean;
- `redacted_drift_summary_allowed`: boolean;
- `status_transition_authorized`: boolean, default false;
- `retention_policy`: symbolic local retention expectation.

The approval record must not contain exact private paths, exact offsets, exact
file sizes, exact private timestamps, raw hashes, raw lines, source filenames,
private report paths, or local-only artifact paths.

### Local-Only Window Metadata

If a future approval allows offset capture, the packet should reuse the start,
end, and derived window fields from:

- `docs/templates/private_evidence_window_offset_capture.md`

Local-only window metadata must not be committed by default.

If offset metadata is unavailable, the packet must not silently widen the read
scope. It must use one of these outcomes:

- `approval_required`
- `offset_window_unavailable`
- `timestamp_fallback_requires_explicit_approval`
- `manual_review_required`
- `blocked_private_evidence_preserved`

### Local-Only Drift Report Metadata

A future approved local packet may record these drift-specific fields locally:

- `local_run_id`;
- `window_id`;
- `source_class`;
- `source_label`;
- `range_mode`;
- `range_read_scope`;
- `drift_report_builder`;
- `baseline_mode`;
- `baseline_refresh_performed`: must be false unless explicitly approved;
- `local_report_created`;
- `local_report_status`;
- `local_report_object`;
- `entry_count_total`;
- `entry_count_routed`;
- `entry_count_unknown`;
- `unknown_rate_pct`;
- `timestamp_missing_count`;
- `timestamp_parse_failure_count`;
- `new_unknown_signature_count`;
- `new_unmatched_api_name_count`;
- `new_unmatched_request_api_name_count`;
- `local_packet_verdict`;
- `redaction_status`;
- `local_report_error`, if execution failed.

Local-only drift report metadata must not be committed by default.

Exact counts, exact percentages, raw signatures, raw API names, raw headers,
private source paths, private report paths, private baseline paths, and raw
report JSON must remain local-only unless a later contract and approval
explicitly authorize a redacted aggregate summary candidate. Even then, raw
signatures, raw API names, raw paths, raw hashes, and raw lines remain
forbidden.

### Sanitized Public Lifecycle Summary Candidate

A future committed lifecycle summary may include only:

- issue and approval references;
- repo branch and commit;
- symbolic `window_id`;
- symbolic `source_class`;
- `offset_capture_used`: boolean;
- `start_marker_recorded`: boolean;
- `end_marker_recorded`: boolean;
- `range_mode`;
- `range_read_scope`, such as `approved_appended_range_only`;
- `drift_execution_performed`: boolean;
- `drift_report_builder`: symbolic label only;
- `baseline_mode`: symbolic label only;
- `baseline_refresh_performed`: boolean;
- count buckets, not exact private counts by default:
  - `entry_count_bucket`;
  - `unknown_count_bucket`;
  - `new_unknown_signature_count_bucket`;
  - `new_unmatched_api_name_count_bucket`;
  - `new_unmatched_request_api_name_count_bucket`;
- `redaction_checklist_status`;
- non-claims;
- statement that raw/private artifacts stayed local and outside Git history.

A future committed lifecycle summary must not include:

- exact private paths;
- exact offsets;
- exact file sizes;
- exact private timestamps;
- raw hashes;
- raw log lines;
- source filenames;
- raw drift report JSON;
- raw baseline JSON;
- exact private counts or percentages unless separately authorized;
- raw signatures;
- raw API names;
- raw headers;
- private app-data contents;
- runtime logs;
- runtime status files;
- failed posts;
- SQLite contents;
- workbook exports;
- screenshots;
- network identifiers;
- packet details;
- decklists;
- card choices;
- private strategy notes;
- credentials, tokens, API keys, or webhook URLs.

## Inputs

### Allowed Inputs For This Contract Pass

- issue #442, tracker #158, issue #434, issue #439, issue #422, PR #441, and
  PR #423 metadata;
- committed contracts, templates, handoffs, reports, manifest, session ledger,
  corpus parity code, log-drift code, and focused tests;
- parser-evidence workflow issue titles/states for #381 through #387.

### Future Local-Only Inputs After Explicit Approval

Only after later explicit approval:

- one local `Player.log` source or one normalized `UTC_Log` source;
- one approved symbolic window label;
- one approved start action;
- one approved end action;
- optional operator-authored notes;
- local-only file metadata needed to bound the approved appended range;
- an approved local baseline mode.

### Forbidden Inputs

Forbidden in Codex B and any committed artifact:

- raw Player.log or UTC_Log excerpts;
- raw lines;
- exact private paths;
- raw hashes;
- private app-data contents;
- private drift reports;
- private drift baselines;
- private smoke outputs;
- runtime logs;
- runtime status files;
- failed posts;
- SQLite files;
- workbook exports;
- screenshots;
- secrets, credentials, tokens, API keys, webhook URLs;
- decklists, card choices, private strategy notes;
- firewall logs;
- Wi-Fi logs;
- OS/router diagnostics;
- packet captures;
- network traces;
- Manasight raw logs, compressed corpus files, raw session payloads, hash
  lists, byte-size lists, capture-date row lists, parser source, or external
  corpus contents.

## Outputs

Output of this Codex B pass:

- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`

Authorized V1 Codex C outputs:

- `docs/templates/private_log_drift_private_evidence_execution.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md`

Deferred outputs requiring later approval:

- executable private drift tooling;
- local offset state;
- local appended-range inspection packet;
- local private drift report;
- local private drift baseline refresh;
- operator-authored private incident notes;
- redacted lifecycle summary from real private data;
- redacted drift summary from real private data;
- corpus manifest or session-ledger status changes.

## Local State Policy

Future local drift execution state should live outside Git by default.

If a later approved helper writes local state inside a repo checkout, it must
use an ignored, private-local artifact family and must pass local artifact,
secret/private-marker, and protected-surface policy before any surrounding
repo work is submitted.

Committed docs may use symbolic labels such as:

```text
source_label: user_selected_player_log_source_a
window_id: issue_442_private_log_drift_window_a
baseline_mode: empty_in_memory_baseline
drift_report_builder: existing_log_drift_sensor_local_only
```

Committed docs must not include:

```text
source_path: <exact private path>
report_path: <exact private path>
baseline_path: <exact private path>
start_offset_bytes: <exact private value from a real run>
end_offset_bytes: <exact private value from a real run>
raw_hash: <real hash>
raw_unknown_signature: <private value from a real run>
```

Template placeholders may show field names, but they must not contain live
private values.

## Redaction Vocabulary

Allowed redaction statuses:

- `not_started`
- `local_state_only`
- `redaction_in_progress`
- `redaction_failed`
- `redacted_lifecycle_summary_ready_for_review`
- `redacted_lifecycle_summary_rejected`
- `redacted_lifecycle_summary_approved`
- `redacted_drift_summary_ready_for_review`
- `redacted_drift_summary_rejected`
- `redacted_drift_summary_approved`

Allowed process verdict labels:

- `not_run`
- `approval_required`
- `offset_window_ready`
- `offset_window_unavailable`
- `timestamp_fallback_requires_explicit_approval`
- `manual_review_required`
- `local_drift_execution_approved`
- `local_drift_execution_not_approved`
- `local_drift_report_created`
- `local_drift_report_failed`
- `redacted_summary_review_required`
- `blocked_private_evidence_preserved`

Allowed public count buckets:

- `not_reported`
- `zero`
- `one`
- `few`
- `many`
- `unknown`
- `withheld_private`

These labels are process vocabulary only. They are not parser truth, live
Player.log health truth, drift health truth, readiness truth, analytics truth,
AI truth, coaching truth, or corpus status truth.

## Status-Transition Rules

This contract does not authorize status transitions.

`mythic_edge.private_log_report_only_drift` must remain
`blocked_private_evidence` unless a later explicit status-transition contract
and review authorize a change.

The following rows must not be changed in this slice:

- `mythic_edge.private_log_report_only_drift`
- `connection.firewall_or_network_drop`
- any other `blocked_private_evidence` row

Private drift execution, even if later approved and successful, does not by
itself prove parser support, private smoke success, live Player.log health,
drift health, release readiness, deploy readiness, production behavior,
analytics truth, AI truth, coaching truth, or full corpus parity.

## Relationship To Existing Drift Code

`src/mythic_edge_parser/app/log_drift_sensor.py` can build a local
`player_log_drift_report` from a supplied source path. The report includes
local path data and detailed drift counters before any normalization.

This contract may reference that code as existing local machinery, but it does
not authorize:

- running it against private data;
- changing its behavior;
- changing its report shape;
- committing its raw report output;
- treating its output as parser truth;
- treating its output as live Player.log health or drift health;
- refreshing any local baseline by default.

If a later approved execution uses existing drift code, the raw output remains
local-only. Any public summary must be a separate redacted candidate and must
pass privacy review.

## Relationship To Offset Capture

The #439 offset-capture process is the preferred future window boundary for
private drift execution. It reduces the chance that a local pass reads content
outside the approved window.

Offset capture does not authorize drift execution. Drift execution does not
authorize public summaries. Public summaries do not authorize corpus status
promotion.

If offset capture is unavailable, a timestamp fallback or manual review path
requires explicit approval. The implementation must not silently widen scope.

## Relationship To Parser-Evidence Pipeline Issues

The later parser-evidence pipeline sequence remains:

1. #381 UTC_Log source adapter for local harvest.
2. #382 local Player.log/UTC_Log harvest candidate reports.
3. #383 human-readable harvest review packets.
4. #384 report-only fixture promotion proof generator.
5. #386 corpus metadata diff generator for fixture promotions.
6. #385 golden replay fixture and manifest draft generator.
7. #387 PR-assist workflow for reviewed fixture promotions.

Issue #388 remains the umbrella.

This contract does not implement, reorder, or close those issues. It only
defines a private drift execution-scoping boundary that those later issues may
reference if they need approval-gated local private evidence.

## Invariants

- Codex B must not read private logs.
- Codex B must not run private checks.
- Codex C must not run private checks in this docs-only slice.
- No raw/private/local artifacts may be committed.
- Private drift reports are local-only by default.
- Private drift baselines are local-only by default.
- Offset state is local-only by default.
- Exact offsets, exact file sizes, exact private timestamps, exact private
  paths, raw hashes, raw lines, raw signatures, raw API names, and raw report
  JSON must not be committed from real runs.
- Public lifecycle evidence may use symbolic labels, booleans, and count
  buckets, not raw private values.
- Offset capture does not authorize appended-range inspection unless the
  approval record says so.
- Appended-range inspection does not authorize drift execution unless the
  approval record says so.
- Drift execution does not authorize corpus status promotion.
- Blocked rows remain blocked by default.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- No parser/runtime/workbook/webhook/App Script/Sheets/analytics/AI/coaching/
  CI/merge/deploy/production behavior is authorized to change.

## Error Behavior

If approval is missing, stop before collecting offsets or running drift
execution.

If the approved source/window/artifact class is ambiguous, stop and route back
to Codex A, Codex B, or the user.

If offset capture is expected but start or end metadata is unavailable, record
the condition in local-only notes and do not inspect private data without a
new explicit fallback approval.

If the source appears rotated, replaced, truncated, summarized, or otherwise
changed between start and end markers, route to a future log-runtime,
recycle/rollback, or UTC_Log adapter contract. Do not solve those mechanics in
this issue.

If baseline mode is ambiguous, use `none` or `empty_in_memory_baseline`; do
not refresh a local baseline by default.

If a local drift report includes private paths, raw signatures, raw API names,
raw headers, or raw counts, keep it local and do not commit it.

If a public summary candidate includes forbidden content, reject it and keep
the relevant corpus row blocked.

If validation finds a secret/private-marker or protected-surface issue, stop
and route to Codex D or Codex B depending on whether the fix is concrete or
requires contract clarification.

## Side Effects

Allowed in this contract pass:

- write this contract file;
- inspect GitHub issue and PR metadata;
- inspect committed repo docs, code, tests, manifests, templates, and reports;
- run documentation, corpus parity, secret/private-marker, protected-surface,
  surface-authorization, and whitespace checks.

Allowed in Codex C under this contract:

- add a docs-only private-log drift execution template/checklist;
- add an implementation handoff;
- run validation over changed docs and unchanged corpus parity surfaces.

Forbidden in this contract pass and Codex C docs-only pass:

- read private logs;
- run private Player.log, normalized UTC_Log, app-data, firewall/drop,
  network, live MTGA, packet, OS/router, diagnostics, drift, or private smoke
  checks;
- create local offset state;
- create local private drift reports;
- refresh local private baselines;
- create local private packets;
- create redacted lifecycle summaries from real private data;
- implement executable tooling;
- change corpus manifest/session-ledger status;
- change parser/runtime/downstream behavior;
- open a PR;
- close #158, #434, or #442.

## Dependency Order

Future work must proceed in this order:

1. Codex B completes this contract.
2. Codex C may add docs-only template/checklist support if the contract is
   accepted.
3. Codex E reviews the docs-only scaffold.
4. Codex F/G submit and merge only reviewed docs, if requested.
5. A later Codex A/G or user approval names an exact local source class,
   symbolic source label, approved window, artifact class, offset policy,
   baseline policy, operator-note policy, and redacted-summary policy.
6. A later Codex B contract confirms any executable helper or exact private
   execution packet.
7. A later Codex C may run a private local execution only after explicit user
   approval names the exact approved scope.
8. A later Codex E review verifies redaction before any public lifecycle or
   drift summary is proposed.
9. Any status transition requires a separate explicit status-transition
   contract and review.

## Compatibility

This contract preserves:

- existing corpus parity vocabulary;
- existing private-evidence boundary vocabulary;
- existing `blocked_private_evidence` rows;
- existing private-log drift boundary from issue #422;
- existing offset-window contract and template from issue #439;
- existing private evidence parent issue #434;
- existing parser-evidence pipeline issues #381 through #388;
- existing parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior.

## Tests Required

Minimum validation for this contract pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_drift_sensor.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md
```

Recommended validation for Codex C if it adds the authorized docs-only
template/checklist:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_drift_sensor.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  docs/templates/private_log_drift_private_evidence_execution.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  docs/templates/private_log_drift_private_evidence_execution.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  docs/templates/private_log_drift_private_evidence_execution.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md \
  | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md
LC_ALL=C rg -n '[^[:ascii:]]' \
  docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md \
  docs/templates/private_log_drift_private_evidence_execution.md \
  docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md
```

Codex E should verify:

- the contract/template remains docs-only;
- no private logs were read;
- no private drift execution was run;
- no executable tooling was added;
- no corpus manifest/session-ledger status changed;
- `mythic_edge.private_log_report_only_drift` remains
  `blocked_private_evidence`;
- no private values, exact offsets, exact file sizes, exact private
  timestamps, exact private paths, raw hashes, raw signatures, raw API names,
  raw reports, or local-only artifacts are present;
- public lifecycle fields are symbolic, boolean, or bucketed;
- no parser/runtime/downstream behavior changed.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`.
- The contract names Corpus / Provenance as the owning layer.
- The contract preserves `mythic_edge.private_log_report_only_drift` as
  `blocked_private_evidence`.
- The contract defines the approval record required before any future private
  drift execution.
- The contract defines allowed source classes, local-only artifact classes,
  offset handling, baseline handling, operator-note handling, redacted summary
  rules, retention expectations, and non-claims.
- The contract forbids raw/private/local artifacts and exact private metadata
  in committed files.
- The contract routes only docs/template implementation to Codex C.
- The contract preserves parser-evidence pipeline issues #381 through #387 as
  later work.
- Validation is recorded.

## Open Questions

- Whether a future private execution packet should use existing
  `log_drift_sensor.py` directly, a wrapper around it, or a manual local
  review checklist remains deferred.
- Whether a redacted drift summary may include exact aggregate counts remains
  deferred; this contract allows count buckets by default.
- Whether a future status transition from `blocked_private_evidence` to any
  stronger status is possible remains deferred to a separate
  status-transition contract.
- Whether UTC_Log adapter work from #381 should become the preferred source
  class for private drift packets remains deferred.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Codex C should implement only the docs/template scaffold authorized by this
contract.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #442.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/442

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Contract:
docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md

Goal:
Implement only the docs/template scaffold authorized by the private-log drift
private-evidence execution contract. This is process documentation only. Do not
run private checks, read private logs, implement executable tooling, change
corpus status, or change parser/runtime/downstream behavior.

Do:
- Refresh live GitHub and local git state.
- Verify main includes 85c0bdc7b6f674ad18828e903a6518531f9d3553.
- Compare the current repo state against the contract before editing.
- Add docs/templates/private_log_drift_private_evidence_execution.md.
- Add docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md.
- Keep the template metadata-only and non-executable.
- Preserve `mythic_edge.private_log_report_only_drift` as blocked_private_evidence.
- Preserve parser-evidence pipeline issues #381 through #387 as later work.

Do not:
- Implement code.
- Open a PR unless separately asked.
- Close tracker #158, parent issue #434, or issue #442.
- Read private logs.
- Run private Player.log, normalized UTC_Log, app-data, firewall/drop,
  network, live MTGA, packet, OS/router, diagnostics, drift, or private smoke
  checks.
- Commit raw Player.log, UTC_Log, raw lines, exact private paths, exact
  offsets, exact file sizes, exact private timestamps, raw hashes, app-data
  contents, runtime logs, runtime status files, failed posts, SQLite files,
  workbook exports, screenshots, secrets, credentials, tokens, API keys,
  webhook URLs, decklists, private strategy notes, private reports,
  local-only artifacts, IP/network traces, packet captures, firewall logs,
  Wi-Fi logs, OS/router diagnostics, or external corpus contents.
- Promote mythic_edge.private_log_report_only_drift or any blocked row by
  default.
- Claim parser support, private smoke success, live Player.log health, drift
  health, release readiness, production behavior, analytics truth, AI truth,
  coaching truth, or full corpus parity.
- Change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics report shape, drift report behavior,
  golden replay behavior, feature-equity behavior, evidence-ledger behavior,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.

Validation:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_drift_sensor.py
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
- path-scoped surface authorization check
- ASCII scan over changed docs
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/442"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/439"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/441"
  previous_merge_commit: "85c0bdc7b6f674ad18828e903a6518531f9d3553"
  related_prior_boundary: "https://github.com/Tahjali11/Mythic-Edge/issues/422"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #442"
  target_artifact: "docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md"
  expected_next_artifacts:
    - "docs/templates/private_log_drift_private_evidence_execution.md"
    - "docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md"
  verdict: "private_log_drift_execution_contract_ready_for_docs_only_scaffold"
  risk_tier: "High"
  branch: "codex/parser-corpus-private-log-drift-execution-442"
  base_branch: "main"
  selected_family: "mythic_edge.private_log_report_only_drift"
  status_decision: "remain_blocked_private_evidence"
  tracker_status: "open"
  parent_issue_status: "open"
  later_pipeline_sequence:
    - "#381 UTC_Log source adapter for local harvest"
    - "#382 local Player.log/UTC_Log harvest candidate reports"
    - "#383 human-readable harvest review packets"
    - "#384 report-only fixture promotion proof generator"
    - "#386 corpus metadata diff generator for fixture promotions"
    - "#385 golden replay fixture and manifest draft generator"
    - "#387 PR-assist workflow for reviewed fixture promotions"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_log_drift_sensor.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
    - "ASCII scan"
  stop_conditions:
    - "Do not read private logs."
    - "Do not run private checks without exact user-approved source/window/artifact class."
    - "Do not implement executable private drift tooling in this slice."
    - "Do not commit raw private evidence, exact private paths, exact offsets, exact file sizes, exact private timestamps, raw hashes, raw signatures, raw API names, private reports, private baselines, or local-only artifacts."
    - "Do not promote mythic_edge.private_log_report_only_drift or any blocked row by default."
    - "Do not claim private smoke success, live Player.log health, drift health, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
