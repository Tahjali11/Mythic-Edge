# Parser Corpus Private Evidence Window Offset Capture Contract

## Module

Private evidence window file-size and byte-offset capture for future
local-only parser corpus evidence windows.

Plain English: this contract defines a safer process for future private
evidence windows. Instead of relying only on timestamps, a future approved
local run should capture local-only start and end file-size or byte-offset
markers so the later inspection can read only bytes appended during the
approved window. This is process safety only. It does not read private logs in
Codex B, run private checks, commit raw evidence, promote blocked corpus rows,
change parser behavior, or claim parser support, private smoke success,
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/439
- Parent/private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Completed local execution packet:
  https://github.com/Tahjali11/Mythic-Edge/issues/438
- Related PR: https://github.com/Tahjali11/Mythic-Edge/pull/440
- Verified base merge commit:
  `a51760af738761c390dd4818fb9e86a839a1b241`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-private-evidence-window-offset-capture`
- base_branch: `main`
- observed_base_commit: `a51760af738761c390dd4818fb9e86a839a1b241`
- target_artifact:
  `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
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

- issue #439, issue #438, issue #434, tracker #158, and PR #440
- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/implementation_handoffs/parser_corpus_firewall_network_drop_redacted_summary_candidate.md`
- `docs/contract_test_reports/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- `docs/local_artifacts_manifest.json`
- `docs/templates/parser_corpus_session.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- parser-evidence workflow issues #381 through #388 as future pipeline
  context only

## Observed Current Behavior

Observed on `origin/main` at
`a51760af738761c390dd4818fb9e86a839a1b241`:

- PR #440 is merged into `main`.
- Issue #438 is closed after PR #440.
- Parent issue #434 remains open.
- Issue #439 remains open.
- Tracker #158 remains open.
- `connection.firewall_or_network_drop` remains `blocked_private_evidence`.
- `mythic_edge.private_log_report_only_drift` remains
  `blocked_private_evidence`.
- The corpus parity CLI reports:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- PR #440 added a redacted report-only summary candidate and contract-test
  report for the completed #438 local-only packet.
- The #438 redacted summary candidate uses a coarse symbolic window label and
  sanitized aggregate counts. It intentionally omits exact private-evidence
  timestamps, exact private paths, raw hashes, raw log lines, network
  identifiers, and private artifacts.
- The #438 packet used timestamp-bounded inspection. That preserved the agreed
  privacy boundary, but future packets can reduce private exposure further by
  capturing local-only start/end file-size or byte-offset markers.

## Scope Decision

This contract approves a V1 documentation/process scaffold for offset-aware
private evidence windows.

Codex C may implement only docs/template support for this process:

- a metadata-only operator template or checklist;
- an implementation handoff documenting that no private evidence was read;
- focused documentation, secret/private-marker, protected-surface, and
  whitespace validation.

Codex C must not implement executable offset-capture code in this slice.

Executable tooling that opens a private source, reads file metadata, records
local offset state, or inspects appended bytes requires a later scoped issue,
contract confirmation or amendment, and explicit user approval. Running that
tool against private data requires a still-later approval that names the exact
source/window/artifact class.

This contract does not authorize status promotion for
`connection.firewall_or_network_drop`, `mythic_edge.private_log_report_only_drift`,
or any other blocked row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns workflow metadata and redaction boundaries for future
private evidence windows. Quality / Governance owns review, validation, and
protected-surface checks. Generated / Local Artifacts owns any future
local-only offset state.

This contract does not own parser interpretation, parser state final
reconciliation, router semantics, diagnostics behavior, drift report behavior,
network behavior, firewall behavior, live MTGA behavior, workbook behavior,
webhook behavior, Apps Script behavior, analytics truth, AI truth, coaching
truth, release readiness, deploy readiness, production behavior, or tracker
completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting areas:

- Quality / Governance, for contracts, templates, handoffs, redaction checks,
  secret/private-marker scans, and protected-surface gates.
- Generated / Local Artifacts, for future local-only offset state.

This is not a Parser module, diagnostics module, local app module, analytics
module, AI module, coaching module, CI gate, merge gate, deploy gate, or
production module.

## Truth Owner

Current corpus status truth remains owned by:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

This contract owns only the offset-capture process vocabulary and future
metadata boundary.

Future local offset state, if approved, is temporary local-only process state.
It may constrain a later local inspection window, but it is not parser truth,
network truth, corpus status truth, private smoke truth, readiness truth,
analytics truth, AI truth, coaching truth, or full corpus parity truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract does not authorize bridge code.

Potential future source area:

- Generated / Local Artifacts, if a later approved local run records offsets.

Potential future consumer:

- Corpus / Provenance, if a later redacted report-only summary records that an
  offset-aware process was used.

Forbidden reverse flow:

- Offset metadata must not change parser behavior, parser event classes,
  router behavior, diagnostics behavior, runtime status shape, drift report
  behavior, corpus report semantics, workbook behavior, webhook behavior, Apps
  Script behavior, Google Sheets sync, output transport, analytics, AI,
  coaching, CI, merge, deploy, production, or tracker lifecycle.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`

Future Codex C docs-only files authorized by this contract:

- `docs/templates/private_evidence_window_offset_capture.md`
- `docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md`

Expected future Codex E review artifact:

- `docs/contract_test_reports/parser_corpus_private_evidence_window_offset_capture.md`

Files this contract may reference but does not authorize Codex C to change:

- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/implementation_handoffs/parser_corpus_firewall_network_drop_redacted_summary_candidate.md`
- `docs/contract_test_reports/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/local_artifacts_manifest.json`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Not owned by this contract:

- raw Player.log files;
- normalized UTC_Log source files;
- local private offset state;
- private app-data contents;
- private smoke outputs;
- runtime logs;
- SQLite files;
- workbook exports;
- screenshots;
- raw hashes;
- exact private paths;
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

The public interface is a metadata-only process vocabulary for future private
evidence windows.

### Approval Record

A future offset-aware run must have an approval record with:

- `approved_issue`: issue authorizing the local run;
- `approved_source_class`: `player_log` or `normalized_utc_log`;
- `approved_source_label`: symbolic label only, not an exact path;
- `approved_window_label`: coarse symbolic window label;
- `approved_window_start_action`: operator action or marker label;
- `approved_window_end_action`: operator action or marker label;
- `offset_capture_allowed`: boolean;
- `appended_range_inspection_allowed`: boolean;
- `operator_notes_allowed`: boolean;
- `local_state_class`: allowed local-only state class;
- `redacted_lifecycle_summary_allowed`: boolean;
- `status_transition_authorized`: boolean, default false.

### Local-Only Start Metadata

A future approved start marker may record these fields locally:

- `window_id`;
- `source_class`;
- `source_label`;
- `start_marker_captured_at_local`;
- `start_file_size_bytes`;
- `start_offset_bytes`;
- `start_source_generation_local`;
- `start_capture_tool_version`;
- `local_run_id`;
- `operator_start_note`;
- `start_error`, if capture failed.

Local-only start metadata must not be committed by default.

### Local-Only End Metadata

A future approved end marker may record these fields locally:

- `window_id`;
- `end_marker_captured_at_local`;
- `end_file_size_bytes`;
- `end_offset_bytes`;
- `end_source_generation_local`;
- `end_capture_tool_version`;
- `local_run_id`;
- `operator_end_note`;
- `end_error`, if capture failed.

Local-only end metadata must not be committed by default.

### Local-Only Derived Window Metadata

A future approved local pass may derive these fields locally:

- `range_mode`: `offset_bounded`, `timestamp_bounded`, or `manual_review`;
- `start_offset_available`;
- `end_offset_available`;
- `end_offset_gte_start_offset`;
- `appended_byte_count`;
- `appended_range_read`;
- `fallback_reason`;
- `raw_lines_read_count`;
- `raw_lines_committed`: must be false;
- `local_packet_verdict`;
- `redaction_status`.

Exact offsets, exact file sizes, exact local timestamps, exact local paths,
raw hashes, and raw lines must remain local-only unless a future contract
explicitly allows a redacted lifecycle statement. Even then, exact private
paths, raw hashes, and raw lines remain forbidden.

### Sanitized Public Lifecycle Evidence

A future committed lifecycle summary may include only:

- issue and approval references;
- repo branch and commit;
- `window_id` or symbolic window label;
- `source_class`;
- `offset_capture_used`: boolean;
- `start_marker_recorded`: boolean;
- `end_marker_recorded`: boolean;
- `range_mode`;
- `range_read_scope`: e.g. `approved_appended_range_only`;
- `appended_byte_count_bucket`, not exact byte count by default;
- `fallback_reason`, if offset capture failed;
- redaction checklist result;
- non-claims;
- statement that raw/private artifacts stayed local and outside Git history.

A public lifecycle summary must not include exact offsets, exact file sizes,
exact private paths, exact private timestamps, raw hashes, raw log lines,
source filenames, private app-data contents, runtime logs, SQLite contents,
workbook exports, screenshots, network identifiers, packet details, decklists,
private strategy notes, secrets, credentials, tokens, API keys, or webhook
URLs.

## Inputs

### Allowed Inputs For This Contract Pass

- issue #439, issue #438, issue #434, tracker #158, and PR #440 metadata;
- current committed contracts, handoffs, reports, manifest, session ledger,
  corpus parity code, and focused tests;
- parser-evidence workflow issue titles/states for #381 through #388.

### Future Local-Only Inputs After Explicit Approval

Only after later explicit approval:

- one local `Player.log` source or one normalized `UTC_Log` source;
- one approved window label;
- one approved start action;
- one approved end action;
- optional operator-authored notes;
- local-only file metadata needed to bound the approved appended range.

### Forbidden Inputs

Forbidden in Codex B and any committed artifact:

- raw Player.log or UTC_Log excerpts;
- raw lines;
- exact private paths;
- raw hashes;
- private app-data contents;
- runtime logs;
- SQLite files;
- workbook exports;
- screenshots;
- secrets, credentials, tokens, API keys, webhook URLs;
- decklists, card choices, private strategy notes;
- private reports;
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

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`

Authorized V1 Codex C outputs:

- a metadata-only template or checklist for future offset-aware windows;
- an implementation handoff stating that no private evidence was read and no
  local-only state was created.

Deferred outputs requiring later approval:

- executable offset-capture tooling;
- local offset state;
- local appended-range packet;
- redacted lifecycle summary from a real private window;
- corpus manifest or session-ledger status changes.

## Local State Policy

Future local offset state should live outside Git by default.

If a later approved tool writes local state inside a repo checkout, it must use
an ignored, private-local artifact family and must pass local artifact and
secret/private-marker policy before any surrounding repo work is submitted.

Committed docs may use symbolic labels such as:

```text
source_label: user_selected_source_a
window_id: issue_439_example_window_a
```

Committed docs must not include:

```text
source_path: <exact private path>
start_offset_bytes: <exact private value from a real run>
end_offset_bytes: <exact private value from a real run>
raw_hash: <real hash>
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

Allowed process verdict labels:

- `not_run`
- `approval_required`
- `offset_start_captured`
- `offset_end_captured`
- `offset_window_ready`
- `offset_window_unavailable`
- `timestamp_fallback_required`
- `manual_review_required`
- `local_packet_ready`
- `redacted_lifecycle_review_required`
- `blocked_private_evidence_preserved`

These labels are process vocabulary only. They are not parser truth, network
truth, runtime health truth, drift health truth, readiness truth, analytics
truth, AI truth, coaching truth, or corpus status truth.

## Status-Transition Rules

This contract does not authorize status transitions.

The following rows must remain blocked unless a later explicit
status-transition contract and review authorize a change:

- `connection.firewall_or_network_drop`
- `mythic_edge.private_log_report_only_drift`
- any other `blocked_private_evidence` row

Offset-aware collection may improve privacy and auditability, but it does not
prove parser support, network reliability, private smoke success, drift health,
release readiness, deploy readiness, production behavior, analytics truth, AI
truth, coaching truth, or full corpus parity.

## Relationship To Private Log Drift

The next staged tracker #158 private-evidence row is
`mythic_edge.private_log_report_only_drift`.

This contract should support that future row by making any private drift
evidence window offset-aware when possible. It does not implement private-log
drift evidence, read private logs, run drift reports, create private reports,
or promote the private-log drift row.

Future Codex A/B work for `mythic_edge.private_log_report_only_drift` should
reference this offset process when defining local evidence windows.

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
defines a safer private-evidence window primitive they may later consume.

## Invariants

- Codex B must not read private logs.
- Codex B must not run private checks.
- This contract must not commit raw/private/local artifacts.
- Offset state is local-only by default.
- Exact offsets, exact file sizes, exact private timestamps, exact private
  paths, and raw hashes must not be committed from real runs.
- Public lifecycle evidence may use symbolic labels and booleans, not raw
  private values.
- Offset capture does not authorize appended-range inspection unless the
  approval record says so.
- Appended-range inspection does not authorize corpus status promotion.
- Blocked rows remain blocked by default.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- No parser/runtime/workbook/webhook/App Script/Sheets/analytics/AI/coaching/
  CI/merge/deploy/production behavior is authorized to change.

## Error Behavior

If approval is missing, stop before collecting offsets.

If the approved source/window/artifact class is ambiguous, stop and route back
to Codex A or the user.

If a start offset is missing, record `offset_window_unavailable` locally and
do not infer a byte-bounded range.

If an end offset is missing, record `manual_review_required` locally and do not
claim offset-bounded inspection.

If the end offset is smaller than the start offset, record
`manual_review_required` or `timestamp_fallback_required`; do not inspect or
summarize beyond the approved window without new approval.

If the source appears rotated, replaced, truncated, or otherwise changed
between start and end markers, route to a future log-runtime/recycle/rotation
contract. Do not solve rotation or rollback in this issue.

If private content is accidentally produced, keep it local, do not commit it,
and route to redaction review.

If a public summary candidate includes forbidden content, reject it and keep
the relevant corpus row blocked.

## Side Effects

Allowed in this contract pass:

- write this contract file;
- inspect GitHub issue and PR metadata;
- inspect committed repo docs, code, tests, manifests, and reports;
- run documentation, corpus parity, secret/private-marker, protected-surface,
  and whitespace checks.

Forbidden in this contract pass:

- read private logs;
- run private Player.log, app-data, firewall/drop, network, live MTGA, packet,
  OS/router, or private smoke checks;
- create local offset state;
- create local private packets;
- create redacted lifecycle summaries from real private data;
- implement executable tooling;
- change corpus manifest/session-ledger status;
- change parser/runtime/downstream behavior;
- open a PR;
- close #158, #434, or #439.

## Dependency Order

Future work must proceed in this order:

1. Codex B completes this contract.
2. Codex C may add docs-only template/checklist support if the contract is
   accepted.
3. Codex E reviews the docs-only scaffold.
4. Codex F/G submit and merge only reviewed docs, if requested.
5. A later Codex A issue frames an exact local evidence window or the staged
   `mythic_edge.private_log_report_only_drift` row.
6. A later Codex B contract authorizes any executable helper or exact local
   evidence run.
7. A later Codex C run may capture offsets only after explicit user approval
   names the exact source/window/artifact class.
8. A later Codex E review verifies redaction before any public lifecycle
   summary is proposed.
9. Any status transition requires a separate explicit status-transition
   contract and review.

## Compatibility

This contract preserves:

- existing corpus parity vocabulary;
- existing private-evidence boundary vocabulary;
- existing `blocked_private_evidence` rows;
- existing #438 redacted report-only summary candidate;
- existing private-log drift boundary;
- existing parser-evidence pipeline issues #381 through #388;
- existing parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior.

## Tests Required

Minimum validation for this contract pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped safety checks for this contract file:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Future Codex C docs-only implementation should additionally run:

```bash
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

and path-scoped secret/private-marker and protected-surface scans over all
changed docs.

Future private evidence execution must add:

- local artifact boundary verification;
- redaction checklist validation;
- forbidden-content scans over any public lifecycle summary candidate;
- proof that raw/private artifacts were not staged or committed;
- proof that exact offsets, exact file sizes, exact private timestamps, exact
  private paths, and raw hashes were not committed.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`.
- Contract names Corpus / Provenance as owning layer.
- Contract distinguishes local-only start metadata, local-only end metadata,
  local-only derived metadata, and sanitized public lifecycle evidence.
- Contract states that Codex B does not read private logs or run private
  checks.
- Contract forbids committing raw evidence, exact private paths, raw hashes,
  exact offsets, exact file sizes, exact private timestamps, local-only state,
  and private artifacts.
- Contract preserves blocked status for `connection.firewall_or_network_drop`
  and `mythic_edge.private_log_report_only_drift`.
- Contract stages `mythic_edge.private_log_report_only_drift` as the next
  private-evidence row without implementing it.
- Contract preserves parser-evidence pipeline issues #381, #382, #383, #384,
  #386, #385, and #387 as later work.
- Contract authorizes only docs/template V1 implementation, not executable
  private evidence tooling.

## Next Workflow Action

Next recommended role: Codex C for docs-only scaffold implementation.

Codex C may create only the approved metadata-only template/checklist and
implementation handoff. Codex C must not implement executable offset-capture
code, run private checks, read private logs, create local state, or promote any
blocked row.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #439.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/439

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Contract:
docs/contracts/parser_corpus_private_evidence_window_offset_capture.md

Base:
main at or after merge commit a51760af738761c390dd4818fb9e86a839a1b241

Goal:
Implement only the docs-only offset-window scaffold authorized by the contract.
Create a metadata-only template/checklist for future private evidence window
file-size or byte-offset capture and an implementation handoff. Do not create
executable tooling.

Allowed files:
- docs/templates/private_evidence_window_offset_capture.md
- docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md

Do not:
- read private logs;
- run private Player.log, app-data, firewall/drop, network, live MTGA, packet,
  OS/router, or private smoke checks;
- create local offset state;
- commit raw Player.log, UTC_Log, raw lines, exact private paths, raw hashes,
  app-data contents, runtime logs, SQLite files, workbook exports,
  screenshots, secrets, credentials, tokens, API keys, webhook URLs,
  decklists, private strategy notes, private reports, or local-only artifacts;
- promote connection.firewall_or_network_drop,
  mythic_edge.private_log_report_only_drift, or any blocked row;
- claim parser support, network reliability, private smoke success, release
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  or full corpus parity;
- change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics report shape, drift report behavior,
  golden replay behavior, feature-equity behavior, evidence-ledger behavior,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.

Validation:
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan over changed docs
- path-scoped protected-surface scan over changed docs
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/439"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/438"
  related_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/440"
  completed_thread: "B"
  next_thread: "C"
  verdict: "offset_capture_contract_ready_for_docs_only_scaffold"
  risk_tier: "High"
  branch: "codex/parser-corpus-private-evidence-window-offset-capture"
  base_branch: "main"
  verified_main_merge_commit: "a51760af738761c390dd4818fb9e86a839a1b241"
  source_artifact: "GitHub issue #439"
  target_artifact: "docs/contracts/parser_corpus_private_evidence_window_offset_capture.md"
  authorized_next_artifacts:
    - "docs/templates/private_evidence_window_offset_capture.md"
    - "docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md"
  staged_follow_up: "mythic_edge.private_log_report_only_drift"
  later_pipeline_sequence:
    - "#381 UTC_Log source adapter for local harvest"
    - "#382 local Player.log/UTC_Log harvest candidate reports"
    - "#383 human-readable harvest review packets"
    - "#384 report-only fixture promotion proof generator"
    - "#386 corpus metadata diff generator for fixture promotions"
    - "#385 golden replay fixture and manifest draft generator"
    - "#387 PR-assist workflow for reviewed fixture promotions"
  tracker_status: "open"
  stop_conditions:
    - "Do not read private logs in Codex B or Codex C."
    - "Do not run private/firewall/network/live checks without explicit approval."
    - "Do not create executable offset-capture tooling in this slice."
    - "Do not commit raw private evidence, exact private paths, exact offsets, exact file sizes, exact private timestamps, raw hashes, or local-only artifacts."
    - "Do not promote blocked corpus rows by default."
    - "Do not claim parser support, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
