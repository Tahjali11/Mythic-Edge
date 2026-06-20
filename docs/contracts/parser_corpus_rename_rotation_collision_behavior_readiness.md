# Parser Corpus Rename/Rotation Collision Behavior Readiness Contract

## Module

`drift_debug.rename_or_rotation_collision` parser corpus behavior-readiness
framing.

Plain English: Mythic Edge already records this family as report-only boundary
metadata from issue #416. This contract decides whether the row can safely move
toward `covered_synthetic`. The answer for this slice is no: preserve
`covered_report_only` until a later issue defines a dedicated reduced collision
model, parser-evidence-pipeline output, or approval-gated private evidence.

This is corpus/provenance planning only. It does not implement code, change
manifest status, edit session-ledger entries, run private checks, activate
#388/#381, or claim live file-system truth, watcher correctness,
rename/recycle collision handling, duplicate/replay prevention, parser drift
recovery truth, release readiness, production behavior, analytics truth, AI
truth, coaching truth, tracker completion, or full corpus parity.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/508
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Latest parser-readiness issue: https://github.com/Tahjali11/Mythic-Edge/issues/504
- Latest parser-readiness PR: https://github.com/Tahjali11/Mythic-Edge/pull/505
- Latest parser-readiness merge commit:
  `0ffd3d1c4b4d4f9d3e23946f28a67662d16df0cc`
- Latest governance issue: https://github.com/Tahjali11/Mythic-Edge/issues/506
- Latest governance PR: https://github.com/Tahjali11/Mythic-Edge/pull/507
- Current main head observed during this Codex B pass:
  `f7e89a48b319c0b8f2ee9daa3ff45c1308c0672a`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed issue state during this Codex B pass:

- Issue #508 is open.
- Tracker #158 is open.
- Related pipeline tracker #388 is open.
- Parent private-evidence issue #434 is open.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/contracts/repo_scoped_workflow_handoffs.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/contracts/parser_corpus_log_runtime_rotation_behavior_readiness.md`
- `docs/contracts/parser_corpus_unknown_entry_behavior_readiness.md`
- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`
- `docs/contracts/parser_corpus_phantom_deck_origin_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_tailer_router_integration.py`

## Purpose

Define the behavior-readiness boundary for
`drift_debug.rename_or_rotation_collision` after adjacent rows have changed:

- `log_runtime.rotation` is now `covered_synthetic` for a reduced
  tailer/stream rotation packet.
- `log_runtime.unknown_entry` is now `covered_synthetic` for reduced
  unknown-entry accounting and review behavior.
- `drift_debug.missing_message_type` is now `covered_synthetic` for reduced
  fallback/default-preservation behavior.
- `drift_debug.rename_or_rotation_collision` remains `covered_report_only`
  through `rename_rotation_collision_boundary_report_v1`.

This contract prevents the adjacent synthetic packets from being reinterpreted
as rename/rotation collision support.

## Observed Current Behavior

Current corpus parity CLI output:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current row:

```yaml
scenario_family: "drift_debug.rename_or_rotation_collision"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "rename_rotation_collision_boundary_report_v1"
parser_event_families: []
```

Current `rename_rotation_collision_boundary_report_v1` evidence says:

- there are no dedicated rename/rotation collision fixtures;
- there are no file identity tracking claims;
- there are no rename collision detection claims;
- there are no recycle collision detection claims;
- there are no duplicate/replay prevention claims;
- there are no private smoke success claims;
- there are no production watcher support claims.

Current adjacent behavior:

- `FileTailer.poll_once(...)` sets `TailBatch.rotated=True` when the current
  file size is smaller than the previous offset.
- When rotated, `FileTailer` resets its line buffer, seeks to byte zero, and
  reads replacement content from the beginning.
- `MtgaEventStream` publishes a sanitized `LogFileRotatedEvent` when a polled
  tail batch is rotated.
- `LogFileRotatedEvent` has a stable event class and schema snapshot.
- Focused tests cover reduced size-shrink rotation and sanitized stream event
  publication.

Current non-evidence:

- No code or test proves file identity tracking.
- No code or test proves a rename collision detector.
- No code or test proves a recycle/rollback detector.
- No code or test proves duplicate/replay prevention for rename or rotation
  collision cases.
- No committed fixture models competing file identities, old-file/new-file
  ambiguity, recycled handles, or rollback windows for this row.
- No private/live Player.log, UTC_Log, filesystem watcher, rename, recycle,
  rollback, rotation-collision, or smoke check was run for this contract.

## Scope Decision

Selected path: preserve `covered_report_only`.

Codex B considered four possible routes:

1. Reduced synthetic uplift.
2. Preserve report-only status.
3. Split the row into narrower future rows.
4. Defer behind #388/#381, private evidence, or an external-boundary evidence
   workflow.

This contract selects route 2 now, with route 3 or route 4 as future work if
the user wants behavior evidence later.

Reasoning:

- The already-uplifted `log_runtime.rotation` row proves only reduced
  size-shrink rotation detection, replacement-content reading from byte zero,
  sanitized `LogFileRotatedEvent` publication, and event schema compatibility.
- A rename/rotation collision claim requires more than a rotated flag or
  stream event. It needs a defined collision model: file identity ambiguity,
  rename-vs-replacement distinction, replay/duplicate prevention, or a
  specific reduced model that explains what is intentionally not proven.
- Current code intentionally lacks file identity tracking and collision
  semantics, so promoting this row now would overstate existing behavior.
- A synthetic packet that merely repeats the `log_runtime.rotation` evidence
  would duplicate an already-covered row and blur the truth boundary.
- A future synthetic packet may be possible, but it needs a new scoped problem
  representation or contract that defines the reduced file-state model and
  expected non-claims.

## Future Split Or Uplift Prerequisites

A later issue may revisit this row only if it explicitly chooses one of these
paths:

### Split Path

Split `drift_debug.rename_or_rotation_collision` into narrower rows or
sub-claims, such as:

- reduced file replacement at same path;
- rename collision model;
- recycle/rollback model;
- duplicate/replay prevention;
- file identity tracking;
- parser-evidence-pipeline observed collision evidence.

The split must not silently promote this parent row.

### Reduced Synthetic Model Path

A future reduced synthetic packet must define:

- exact synthetic file-state sequence;
- whether it models same-path replacement, rename, recycle, rollback, or
  duplicate/replay pressure;
- expected existing behavior and forbidden new behavior;
- expected corpus manifest entry shape;
- expected session-ledger `parser_coverage` counters;
- redaction fields proving no raw logs, private paths, hashes, byte-size lists,
  capture-date rows, or private artifacts are committed;
- explicit non-claims for live file-system truth, watcher correctness,
  production behavior, drift recovery, and #388/#381 activation.

### #388 / #381 Evidence Path

If parser-evidence-pipeline work later produces reviewed UTC_Log harvest or
golden replay promotion evidence, a new contract must decide whether that
evidence can support this row. This issue does not activate that pipeline.

### Private Evidence Path

If a private local packet is proposed, it must route through #434-style
approval-gated collection/redaction rules and must not commit raw logs,
private paths, hashes, byte-size lists, screenshots, runtime artifacts, or
private reports.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns only the corpus behavior-readiness decision for
`drift_debug.rename_or_rotation_collision`.

Supporting truth owners:

- `src/mythic_edge_parser/log/tailer.py` owns current `FileTailer` and
  `TailBatch.rotated` behavior.
- `src/mythic_edge_parser/stream.py` owns current rotation-event publication.
- `src/mythic_edge_parser/events.py` owns current `LogFileRotatedEvent` shape.
- `src/mythic_edge_parser/app/corpus_parity_report.py` owns corpus parity
  aggregation and readiness metrics.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json` and
  `tests/fixtures/parser_corpus/session_ledger.v1.json` own committed corpus
  row metadata.

Corpus metadata must not become parser behavior truth, live filesystem truth,
watcher truth, release truth, production truth, analytics truth, AI truth, or
coaching truth.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Quality / Governance for readiness language and protected-surface
discipline.

This is not a Parser implementation module, tailer behavior module, stream
module, diagnostics module, drift-report module, parser-evidence pipeline
activation, private-evidence execution, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, release gate, or production module.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for this behavior-readiness decision:

- `docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md`

Truth boundary:

- `TailBatch.rotated` may prove a size-shrink rotation condition only.
- `LogFileRotatedEvent` may prove sanitized event publication only.
- `log_runtime.rotation` synthetic coverage may prove the reduced
  tailer/stream packet only.
- `log_runtime.unknown_entry` synthetic coverage may prove unknown-entry
  accounting/review only.
- `drift_debug.missing_message_type` synthetic coverage may prove fallback and
  default-preservation behavior only.
- `rename_rotation_collision_boundary_report_v1` may prove that the collision
  boundary has been inspected and intentionally not claimed.
- None of the above proves rename collision handling, recycle collision
  handling, duplicate/replay prevention, file identity tracking, live watcher
  correctness, parser drift recovery truth, private smoke success, release
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  tracker completion, or full corpus parity.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future source areas:

- Parser / log runtime support, if a reduced synthetic collision model is
  contracted.
- Generated / Local Artifacts, if a user-approved private evidence packet is
  contracted.
- Parser Evidence Pipeline, if #388/#381 later produce reviewed harvest or
  promotion evidence.

Potential future consuming area:

- Corpus / Provenance, for coverage status and readiness metadata only.

Forbidden reverse flow:

- Corpus metadata must not create parser collision support.
- Drift reports must not become live filesystem truth.
- Diagnostics/golden replay/feature-equity references must not become watcher
  correctness or duplicate-prevention proof.
- Analytics, AI, coaching, workbook, webhook, Apps Script, and release
  surfaces must not infer support from this row.

## Files Owned By This Contract

This Codex B pass creates:

- `docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md`

No Codex C implementation is authorized by this contract for the current row
status. A future implementation issue may edit corpus manifest/session-ledger
metadata only after a new contract authorizes a specific split or uplift path.

Codex E may create:

- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md`

## Public Interface

The public interface is the corpus-readiness decision:

```yaml
scenario_family: "drift_debug.rename_or_rotation_collision"
selected_path: "preserve_report_only"
current_status: "covered_report_only"
future_status_change_authorized: false
parser_behavior_verified_may_be_added_now: false
pipeline_activation_ready_for_issue_388: false
```

This contract does not add parser events, payloads, CLI flags, runtime fields,
schema fields, workbook rows, webhook fields, diagnostics sections, drift
report sections, golden replay fixtures, feature-equity fixtures, evidence
ledger fields, analytics fields, AI fields, CI gates, or deployment gates.

## Inputs

Allowed inputs:

- repo-owned governance docs and workflow docs;
- issue #508 and related GitHub issue/PR metadata;
- prior report-only boundary contract for issue #416;
- corpus manifest and session ledger;
- current corpus parity report output;
- tailer, stream, event, drift, diagnostics, router, and focused tests as
  adjacent reference context only;
- public external taxonomy only as already-captured category context, never as
  parser truth.

Forbidden inputs:

- private Player.log;
- UTC_Log;
- live MTGA output;
- local app-data;
- filesystem watcher experiments;
- rename, recycle, rollback, network, firewall, packet, OS/router, or private
  smoke checks;
- raw log lines;
- raw payloads;
- exact private paths;
- raw hashes;
- byte-size lists;
- capture-date row lists;
- screenshots;
- SQLite files;
- workbook exports;
- generated/private/runtime artifacts;
- external corpus contents;
- Manasight raw logs, compressed corpus files, parser source, or raw session
  payloads;
- secrets, credentials, tokens, API keys, or webhook URLs.

## Outputs

This contract produces only:

- a docs contract artifact;
- a next-role recommendation;
- a repo-scoped `workflow_handoff` block.

It does not produce:

- manifest changes;
- session-ledger changes;
- fixture changes;
- source changes;
- tests;
- private evidence packets;
- issue closure;
- tracker completion;
- PR creation.

## Invariants

- The row remains `covered_report_only` unless a later explicit contract
  authorizes a split or uplift.
- `parser_behavior_verified` must not be added to this row by this issue.
- `parser_behavior_ready` remains false.
- `pipeline_activation_ready_for_issue_388` remains false.
- #388/#381 remain inactive.
- #158 and #434 remain open.
- Existing adjacent synthetic rows must keep their own truth boundaries.
- No public artifact may include private logs, exact private paths, raw hashes,
  byte-size lists, capture-date rows, screenshots, runtime artifacts, workbook
  exports, secrets, credentials, tokens, API keys, or webhook URLs.

## Error Behavior

Route back to Codex B or Codex A if future work tries to:

- promote the row using only `TailBatch.rotated`;
- promote the row using only `LogFileRotatedEvent`;
- promote the row using log-runtime rotation synthetic evidence;
- promote the row using unknown-entry, missing-message-type, diagnostics,
  drift, golden replay, feature-equity, evidence-ledger, or public taxonomy
  context;
- add behavior claims without a dedicated reduced collision model;
- use private evidence without approval-gated collection/redaction rules;
- activate #388/#381 from this row;
- change parser, tailer, stream, router, diagnostics, drift, analytics,
  workbook, webhook, Apps Script, AI, CI, release, deploy, production, or final
  integration behavior.

## Compatibility

Keep these existing artifacts compatible:

- `rename_rotation_collision_boundary_report_v1`;
- `log_runtime_rotation_boundary_report_v1`;
- `log_runtime_rotation_synthetic_tailer_stream_v1`;
- `unknown_entry_drift_report_reference_v1`;
- `unknown_entry_synthetic_router_drift_diagnostics_v1`;
- `missing_message_type_boundary_report_v1`;
- `missing_message_type_synthetic_fallback_defaults_v1`.

This contract must not rewrite their meanings or move their claims between
scenario families.

## Validation Obligations

Codex B validation should be docs-only and path-scoped.

Recommended checks:

```bash
python3 tools/check_agent_docs.py
git diff --check
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Codex E should verify:

- the contract preserves `covered_report_only`;
- no implementation or status promotion is authorized;
- non-claims match the protected-surface list from issue #508;
- #388/#381 activation remains false;
- adjacent `log_runtime.rotation`, `log_runtime.unknown_entry`, and
  `drift_debug.missing_message_type` rows are not reinterpreted;
- public docs contain no private paths, raw logs, hashes, or private evidence.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md`.
- It names the selected path as `preserve_report_only`.
- It explicitly says `parser_behavior_verified` may not be added now.
- It defines future split/uplift prerequisites without solving them.
- It preserves tracker #158, #388, #381, and #434 gates.
- It includes a repo-scoped handoff block.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

Codex C is not recommended because this contract does not authorize
implementation, manifest promotion, session-ledger edits, fixture creation, or
behavior changes.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #508.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/508

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Target branch:
main

Source artifact:
docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md

Goal:
Review the contract decision for `drift_debug.rename_or_rotation_collision` behavior readiness. Confirm whether preserving `covered_report_only` is complete, accurate, and safe.

Do:
- Verify the contract matches issue #508 and the current corpus manifest/session ledger.
- Confirm it does not authorize implementation, manifest promotion, session-ledger edits, fixture creation, private/live checks, #388/#381 activation, or behavior changes.
- Confirm adjacent `log_runtime.rotation`, `log_runtime.unknown_entry`, `drift_debug.missing_message_type`, and `drift_debug.recycle_or_rollback` rows are not reinterpreted.
- Produce `docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md`.

Do not:
- Implement code.
- Open a PR.
- Close #158, #388, #434, or #508.
- Promote report-only or blocked rows.
- Run private/live checks.
- Claim live file-system truth, watcher correctness, rename/recycle collision handling, duplicate/replay prevention, parser drift recovery truth, release readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/508"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/504"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/505"
  previous_merge_commit: "0ffd3d1c4b4d4f9d3e23946f28a67662d16df0cc"
  governance_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/506"
  governance_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/507"
  governance_merge_commit: "f7e89a48b319c0b8f2ee9daa3ff45c1308c0672a"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #508 and current corpus parity artifacts"
  target_artifact: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  selected_family: "drift_debug.rename_or_rotation_collision"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only"
  parser_behavior_verified_may_be_added_now: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "Codex B docs-only validation; see final response."
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close #388 or #434 without separate authorization."
    - "Do not activate #388/#381."
    - "Do not promote blocked or report-only rows by default."
    - "Do not claim live file-system truth, watcher correctness, rename collision handling, recycle collision handling, duplicate/replay prevention, parser drift recovery truth, private smoke success, release readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity."
```
