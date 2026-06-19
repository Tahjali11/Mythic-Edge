# Parser Corpus Drift Recycle/Rollback External Boundary Contract

## Module

Drift recycle/rollback external-boundary planning for the parser corpus parity
report.

Plain English: this contract defines the safe Mythic Edge boundary for
`drift_debug.recycle_or_rollback`. The row remains blocked because committed
tailer rotation, stream rotation events, log-runtime rotation metadata,
rename/rotation collision metadata, unknown-entry reporting, diagnostics,
log-drift reporting, and public taxonomy metadata do not prove recycle or
rollback behavior.

This is corpus/provenance planning only. It is not parser support, runtime
support, watcher correctness, duplicate/replay prevention, drift recovery,
private smoke success, release readiness, production behavior, analytics truth,
AI truth, coaching truth, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/446
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Parent/private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/444
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/445
- Previous merge commit:
  `40b07a6618f9f5be5cec961a77b5783c0d3f88d2`

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-drift-recycle-rollback-boundary-446`
- base_branch: `main`
- observed_base_commit: `40b07a6618f9f5be5cec961a77b5783c0d3f88d2`
- selected_family: `drift_debug.recycle_or_rollback`
- target_artifact:
  `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`
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

- issue #446, tracker #158, parent issue #434, issue #444, and PR #445
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md`
- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- parser-evidence pipeline issues #381 through #387 as later workflow context
  only

## Observed Current Behavior

Observed on `main` at
`40b07a6618f9f5be5cec961a77b5783c0d3f88d2`:

- Issue #446 is open.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- PR #445 is merged into `main`.
- The corpus parity CLI reports:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- `log_runtime.rotation` is now `covered_report_only` through
  `log_runtime_rotation_boundary_report_v1`.
- `drift_debug.rename_or_rotation_collision` is already
  `covered_report_only` through
  `rename_rotation_collision_boundary_report_v1`.
- `drift_debug.recycle_or_rollback` is still represented only by
  `external_reference_category_boundary`.
- `drift_debug.recycle_or_rollback` currently has:
  - `coverage_status`: `blocked_external_boundary`
  - `coverage_basis`: `["external_reference_only"]`
  - `mythic_edge_entries`: `["external_reference_category_boundary"]`
  - `parser_event_families`: `[]`
- `external_reference_category_boundary` also covers:
  - `timer.inactivity_timeout`
  - `gameplay_stress.conjure`
  - `gameplay_stress.spellbook`
- `FileTailer.poll_once(...)` reports `TailBatch.rotated=True` when current
  file size is smaller than the prior offset. It resets the line buffer and
  reads replacement content from the beginning.
- `MtgaEventStream` publishes a sanitized `LogFileRotatedEvent` when a polled
  `TailBatch` is rotated.
- `log_drift_sensor.py` can build local drift reports from supplied log paths,
  but those reports include private source path data before any separate
  redaction process.
- Current committed code and tests do not define a recycle detector, rollback
  detector, file identity model, append-window rollback model,
  duplicate/replay prevention proof, live watcher proof, or private drift
  execution packet for this family.

## Scope Decision

Selected path: remain `blocked_external_boundary`.

Codex B considered these paths:

1. Move `drift_debug.recycle_or_rollback` to `covered_report_only`.
2. Add synthetic or committed fixture coverage.
3. Define a future evidence-generation prerequisite and keep the row blocked.
4. Leave the row in the broad external-reference boundary without sharper
   contract language.

This contract selects path 3.

Reasoning:

- `drift_debug.recycle_or_rollback` is more interpretive than
  `log_runtime.rotation`.
- Current tailer/stream evidence can show a simple size-shrink rotation signal
  and a sanitized rotation event, but it does not identify the underlying file,
  prove the old file was recycled, prove a prior file range rolled back, or
  prove duplicate/replay prevention.
- Current rename/rotation collision metadata explicitly preserves
  recycle/rollback as a non-claim.
- Current log-drift, unknown-entry, diagnostics, and live-diagnostics surfaces
  can summarize review signals, but they do not prove the source log actually
  recycled or rolled back.
- Public external taxonomy can name the scenario family, but it is not Mythic
  Edge evidence.
- A future move out of `blocked_external_boundary` needs a separate evidence
  model. That model may be a reduced safe synthetic file-state model, an
  approval-gated private evidence packet, or a parser-evidence pipeline output
  after issues #381 through #387. This contract does not choose that later
  implementation path.

This decision does not authorize source-code changes, manifest status changes,
session-ledger changes, focused test changes, private/live execution, or
status promotion for this row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns the corpus coverage boundary for
`drift_debug.recycle_or_rollback`. Parser/log runtime code owns current tailer
and stream behavior. Diagnostics and drift reports own local review summaries.
Corpus parity may describe why those surfaces are insufficient, but it must not
reinterpret them as recycle/rollback support.

## Internal Project Area

Corpus / Provenance, with Quality / Governance support for contract, validation,
review, and protected-surface checks.

This slice is not a Parser behavior module, tailer behavior module, stream
module, event-shape module, diagnostics implementation, drift-report
implementation, local app watcher implementation, analytics module, AI module,
coaching module, CI gate, merge gate, deploy gate, readiness gate, or
production module.

## Truth Owner

Truth owner for current corpus coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`

Truth boundary:

- `FileTailer` may report one simple size-shrink rotation condition.
- `MtgaEventStream` may emit a sanitized `LogFileRotatedEvent` from that
  condition.
- Corpus parity may say `log_runtime.rotation` and
  `drift_debug.rename_or_rotation_collision` have report-only boundaries.
- Corpus parity may say `drift_debug.recycle_or_rollback` remains blocked
  because no Mythic Edge-owned evidence model exists yet.
- Corpus parity must not infer recycle behavior, rollback behavior,
  duplicate/replay prevention, file identity tracking, parser drift recovery,
  private smoke success, live Player.log health, readiness, production
  behavior, analytics truth, AI truth, coaching truth, tracker completion, or
  full corpus parity.

## Bridge-Code Status

`deferred_future_boundary`

This contract does not authorize bridge code.

Potential future source areas:

- Parser / log runtime support, if a reduced synthetic model is contracted.
- Generated / Local Artifacts, if a future user-approved private evidence
  packet is contracted.
- Parser Evidence Pipeline, if issues #381 through #387 later produce reviewed
  harvest or fixture-promotion evidence.

Potential future consuming area:

- Corpus / Provenance, only after a later contract defines the evidence model,
  redaction rules, status-transition criteria, and review requirements.

Forbidden reverse flow:

- Corpus metadata must not change parser, tailer, stream, event class,
  diagnostics, drift, golden replay, feature-equity, evidence-ledger, workbook,
  webhook, Apps Script, Sheets, analytics, AI, coaching, CI, merge, deploy,
  production, or tracker behavior.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`

This contract does not authorize Codex C to edit:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- parser, tailer, stream, diagnostics, drift, evidence-ledger, golden replay,
  feature-equity, workbook, webhook, Apps Script, analytics, AI, coaching, CI,
  merge, deploy, production, or runtime files

If the team wants a no-status-change comparison package before submitter work,
it may be a docs-only follow-up with:

- `docs/implementation_handoffs/parser_corpus_drift_recycle_rollback_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_drift_recycle_rollback_external_boundary.md`

Those artifacts must not modify corpus metadata or tests.

Not owned by this contract:

- raw Player.log files;
- normalized UTC_Log source files;
- private app-data contents;
- private smoke outputs;
- runtime logs;
- runtime status files;
- failed posts;
- SQLite files;
- workbook exports;
- screenshots;
- exact private paths;
- exact offsets;
- exact file sizes;
- exact private timestamps;
- raw hashes;
- private reports;
- local-only artifacts;
- file-system watcher behavior;
- live MTGA behavior;
- OS/router diagnostics;
- packet captures;
- network traces;
- secrets, credentials, tokens, API keys, or webhook URLs;
- Manasight raw logs, compressed corpus files, raw session payloads, hash
  lists, byte-size lists, capture-date row lists, parser source, or external
  corpus contents.

## Public Interface

This contract adds no runtime public API.

The public interface remains the corpus parity compatibility report generated
from committed corpus manifest and session ledger inputs.

Required report behavior:

- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- The row remains represented by `external_reference_category_boundary`.
- The row keeps `coverage_basis == ["external_reference_only"]`.
- The row has no parser event families.
- No dedicated session-ledger entry is required in this slice.
- `log_runtime.rotation` remains `covered_report_only`.
- `drift_debug.rename_or_rotation_collision` remains `covered_report_only`.
- Private-evidence rows remain `blocked_private_evidence`.
- The still blocked external rows remain separate future candidates:
  - `timer.inactivity_timeout`
  - `gameplay_stress.conjure`
  - `gameplay_stress.spellbook`

## Required Future Evidence Before Promotion

A future contract may reconsider the status only if it defines at least one
safe Mythic Edge-owned evidence path.

Potential safe evidence paths:

1. A reduced synthetic file-state model that explicitly defines:
   - allowed file identities;
   - offset transitions;
   - replacement, recycle, and rollback cases;
   - duplicate/read replay expectations;
   - missing-read expectations;
   - expected report-only output;
   - protected non-claims.
2. An approval-gated private evidence packet that explicitly defines:
   - approved local source class;
   - symbolic source label;
   - offset-window or appended-range boundary;
   - redaction and retention rules;
   - local-only artifact policy;
   - public summary limits;
   - status-transition criteria.
3. A parser-evidence pipeline output from issues #381 through #387 that:
   - avoids raw/private log commits;
   - produces reviewed harvest or fixture-promotion evidence;
   - separates recycle/rollback evidence from rotation, unknown-entry, and
     generic drift evidence.

Any future status transition must explicitly decide whether the target status
is `covered_report_only`, `covered_synthetic`, `blocked_private_evidence`, or
another existing corpus vocabulary value. A successful private or synthetic
experiment must not promote the row by default.

## Required Adjacent-Row Protections

This contract preserves:

- `drift_debug.recycle_or_rollback`: `blocked_external_boundary`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `connection.firewall_or_network_drop`: `blocked_private_evidence`
- `mythic_edge.private_log_report_only_drift`: `blocked_private_evidence`
- `log_runtime.rotation`: `covered_report_only`
- `drift_debug.rename_or_rotation_collision`: `covered_report_only`

These surfaces must not be reinterpreted as recycle/rollback coverage:

- `log_runtime.rotation`
- `drift_debug.rename_or_rotation_collision`
- `drift_debug.missing_message_type`
- `drift_debug.phantom_or_deck_origin`
- `log_runtime.timestamp_anomaly`
- `log_runtime.unknown_entry`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `connection.firewall_or_network_drop`
- diagnostics reports
- log-drift reports
- public external taxonomy metadata

## Inputs

Allowed inputs for this contract pass:

- issue #446, tracker #158, parent issue #434, issue #444, PR #445, and
  current `main` metadata;
- current committed contracts, handoffs, reports, manifest, session ledger,
  corpus parity code, tailer code, stream code, drift code, and focused tests;
- parser-evidence workflow issue titles and states for #381 through #387.

Forbidden inputs:

- raw Player.log or UTC_Log excerpts;
- raw lines;
- exact private paths;
- exact offsets;
- exact file sizes;
- exact private timestamps;
- raw hashes;
- private app-data contents;
- runtime logs;
- runtime status files;
- failed posts;
- SQLite files;
- workbook exports;
- screenshots;
- secrets, credentials, tokens, API keys, webhook URLs;
- decklists, card choices, private strategy notes;
- private reports;
- local-only artifacts;
- IP/network traces;
- packet captures;
- OS/router diagnostics;
- firewall logs;
- Wi-Fi logs;
- Manasight raw logs, compressed corpus files, raw session payloads, hash
  lists, byte-size lists, capture-date row lists, parser source, or external
  corpus contents.

Forbidden execution inputs:

- private Player.log checks;
- UTC_Log checks;
- app-data checks;
- live MTGA checks;
- firewall/drop checks;
- network checks;
- packet checks;
- OS/router checks;
- file-system rotation checks;
- recycle or rollback checks;
- watcher checks;
- tailer checks against private logs;
- drift checks against private logs;
- diagnostics checks against private logs;
- private smoke checks.

## Outputs

Output of this Codex B pass:

- `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`

Authorized follow-up outputs only if the team wants a no-change verification
package:

- `docs/implementation_handoffs/parser_corpus_drift_recycle_rollback_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_drift_recycle_rollback_external_boundary.md`

Forbidden outputs:

- parser, tailer, stream, event, diagnostics, drift, golden replay,
  feature-equity, evidence-ledger, workbook, webhook, Apps Script, Sheets,
  analytics, AI, coaching, CI, merge, deploy, production, or final integration
  behavior changes;
- corpus manifest or session-ledger status promotion;
- executable tooling;
- local/private evidence packets;
- generated runtime artifacts;
- private smoke outputs;
- private drift reports;
- recycle/rollback support claims;
- any claim that `blocked_external_boundary` has been resolved.

## Required Guarantees

- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- `drift_debug.recycle_or_rollback` remains represented by
  `external_reference_category_boundary`.
- `drift_debug.recycle_or_rollback` keeps
  `coverage_basis == ["external_reference_only"]`.
- No parser event families are added for the row.
- No dedicated session-ledger entry is added in this slice.
- No adjacent row changes status in this slice.
- No private or external raw artifacts are read, created, or committed.
- No parser, tailer, stream, event, diagnostics, drift, corpus report code,
  golden replay, feature-equity, evidence-ledger, workbook, webhook,
  Apps Script, Sheets, analytics, AI, coaching, CI, merge, deploy, production,
  or final integration behavior changes.

## Unknowns

- Which real MTGA or operating-system log behaviors should count as
  "recycle" rather than "rotation", "rename collision", "rollback", or
  ordinary truncation.
- Whether a safe synthetic model can represent recycle/rollback without
  overclaiming production watcher correctness.
- Whether private evidence is required, or whether a future reduced synthetic
  model is enough for report-only coverage.
- Whether the UTC_Log adapter and harvest pipeline from #381 through #387 will
  provide a safer evidence path.
- Whether duplicate/replay prevention belongs in tailer, stream, diagnostics,
  drift report, golden replay, or a separate parser-resilience artifact.

## Suspected Gaps

- The current tailer only detects one size-shrink replacement condition.
- The current stream only emits a sanitized rotation event from a rotated flag.
- The current corpus metadata has report-only boundaries around adjacent
  rotation and rename/collision rows, but no dedicated recycle/rollback
  evidence.
- Current log-drift reports can find unknown or changed entry families, but do
  not prove source file recycle/rollback mechanics.
- A future status change will likely need either a synthetic file-state model
  or an approval-gated private evidence workflow.

## Invariants

- Codex B must not implement code.
- Codex B must not run private or live checks.
- `drift_debug.recycle_or_rollback` remains blocked by default.
- Public external taxonomy is category context only.
- Report-only log-runtime rotation metadata is not recycle/rollback truth.
- Report-only rename/rotation collision metadata is not recycle/rollback
  truth.
- Unknown-entry, timestamp-anomaly, missing-message-type, diagnostics, drift,
  and private-log drift surfaces are not recycle/rollback truth.
- No raw/private/local artifacts may be committed.
- Tracker #158 remains open.
- Parent issue #434 remains open.

## Error Behavior

If current repo state does not include merge commit
`40b07a6618f9f5be5cec961a77b5783c0d3f88d2`, stop and refresh before using this
contract as current.

If Codex C or Codex E finds `drift_debug.recycle_or_rollback` already changed
from `blocked_external_boundary`, record the exact observed row and route back
to Codex B unless the status change is explained by a later merged contract.

If implementation appears to require parser, tailer, stream, diagnostics,
drift, corpus report, workbook, webhook, Apps Script, analytics, AI, coaching,
CI, merge, deploy, production, or runtime changes, stop and route back to
Codex A/B for a new issue and contract.

If validation requires private/live data, stop and record the blocked
condition. Do not run private checks as a workaround.

If a proposed public summary includes raw/private paths, offsets, file sizes,
timestamps, hashes, report payloads, log lines, API names, screenshots,
secrets, tokens, credentials, webhook URLs, workbook exports, SQLite files, or
external corpus contents, reject it and keep the row blocked.

## Side Effects

Allowed in this contract pass:

- write this contract file;
- inspect GitHub issue and PR metadata;
- inspect committed repo docs, code, tests, manifests, templates, and reports;
- run documentation, corpus parity, secret/private-marker, protected-surface,
  and whitespace checks.

Forbidden in this contract pass:

- run private Player.log, UTC_Log, app-data, file-system rotation, recycle,
  rollback, live MTGA, watcher, tailer, drift, diagnostics, network, or
  private smoke checks;
- read private logs;
- implement parser, tailer, stream, event, diagnostics, drift, or corpus
  report changes;
- update corpus manifest or session-ledger statuses;
- add synthetic file-system fixtures;
- open a PR;
- close #158, #434, or #446.

## Dependency Order

Future work must proceed in this order:

1. Codex B completes this contract.
2. Optional Codex E reviews the contract-only boundary, or optional Codex C
   produces no-change docs verification artifacts if the team wants a
   handoff/report package before submission.
3. Codex F may submit the reviewed contract-only artifact if requested.
4. Codex G may merge/close/update trackers only after explicit user approval
   and normal gates.
5. A later Codex A/B issue may define a reduced synthetic model or
   approval-gated private evidence model for recycle/rollback.
6. Parser-evidence pipeline issues #381 through #387 remain later work and are
   not reordered by this contract.

## Compatibility

This contract preserves:

- existing corpus parity vocabulary;
- existing `blocked_external_boundary` status for
  `drift_debug.recycle_or_rollback`;
- existing broad external-reference category entry for the remaining blocked
  external rows;
- existing report-only boundary vocabulary for `log_runtime.rotation`;
- existing report-only boundary vocabulary for
  `drift_debug.rename_or_rotation_collision`;
- existing blocked private-evidence rows;
- existing parser-evidence pipeline issues #381 through #387;
- existing parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior.

## Tests Required

Required Codex B validation:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_log_drift_sensor.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md
printf '%s\n' \
  docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md
```

If a later no-change Codex C verification package is requested, use the same
validation and add the implementation handoff and report paths to the
secret/private-marker and protected-surface scans.

Codex E should verify:

- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- No manifest, session-ledger, focused test, or source behavior change is
  authorized by this contract.
- Adjacent report-only rows do not become recycle/rollback evidence.
- No private/live/file-system/recycle/rollback/watcher checks were run.
- No private/raw/local artifacts were read, created, or committed.
- Non-claims are preserved in contract, handoff, report, issue, and PR text.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`.
- The contract names Corpus / Provenance as the owning layer.
- The contract deliberately preserves
  `drift_debug.recycle_or_rollback` as `blocked_external_boundary`.
- The contract states that no Codex C metadata promotion is authorized by
  default.
- The contract defines future evidence prerequisites before any status change.
- The contract defines adjacent-row protections.
- The contract forbids private/live/file-system/recycle/rollback/watcher
  checks.
- The contract forbids parser/tailer/stream/event/drift/diagnostics behavior
  changes.
- The contract defines validation expectations for Codex C/E/F/G.

## Next Workflow Action

Recommended next role: Codex E: Module Reviewer, if the team wants an
independent contract-only review before submitter work.

Codex C is not required for a metadata implementation because this contract
does not authorize corpus status promotion, manifest edits, session-ledger
edits, or focused test changes. If the team wants a no-change verification
package anyway, Codex C must produce docs-only comparison/report artifacts and
leave corpus metadata untouched.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #446.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/446

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/444

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/445

Previous merge commit:
40b07a6618f9f5be5cec961a77b5783c0d3f88d2

Base branch:
main

Contract:
docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md

Goal:
Review the contract-only boundary for drift_debug.recycle_or_rollback. Verify
that the selected status remains blocked_external_boundary, no Codex C metadata
promotion is authorized by default, and adjacent report-only surfaces are not
overread as recycle/rollback support.

Review:
- docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md
- docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md
- docs/contracts/parser_corpus_rename_rotation_collision_coverage.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/log/tailer.py
- src/mythic_edge_parser/stream.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- tests/test_corpus_parity_report.py

Lead with findings. If no issues are found, say so and record residual risks.

Do not implement code. Do not target main directly. Do not close #158, #434,
or #446. Do not run private Player.log, UTC_Log, app-data, filesystem,
recycle/rollback, live MTGA, watcher, drift, diagnostics, network, or private
smoke checks. Do not claim parser support, recycle handling, rollback
detection, watcher correctness, duplicate/replay prevention, drift recovery,
private smoke success, readiness, production behavior, analytics truth, AI
truth, coaching truth, or full corpus parity.
```

Optional Codex C prompt, only if the team explicitly wants a no-change
verification package:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #446.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/446

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Contract:
docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md

Goal:
Produce a no-change docs verification package for the drift_debug.recycle_or_rollback
external-boundary contract. Do not promote the row or edit corpus metadata.

Expected artifacts:
- docs/implementation_handoffs/parser_corpus_drift_recycle_rollback_external_boundary_comparison.md
- docs/contract_test_reports/parser_corpus_drift_recycle_rollback_external_boundary.md

Do:
- Verify main includes 40b07a6618f9f5be5cec961a77b5783c0d3f88d2.
- Confirm drift_debug.recycle_or_rollback remains blocked_external_boundary.
- Confirm log_runtime.rotation remains covered_report_only.
- Confirm drift_debug.rename_or_rotation_collision remains covered_report_only.
- Confirm no private/live/file-system/recycle/rollback checks are needed.
- Record validation and residual risks.

Do not:
- Implement code.
- Edit tests.
- Edit corpus manifest or session ledger.
- Promote drift_debug.recycle_or_rollback or any blocked row.
- Run private/live/file-system/recycle/rollback/watcher/drift checks.
- Read private logs.
- Claim parser support, recycle handling, rollback detection, duplicate/replay
  prevention, private smoke success, readiness, production behavior, analytics
  truth, AI truth, coaching truth, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/446"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/444"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/445"
  previous_merge_commit: "40b07a6618f9f5be5cec961a77b5783c0d3f88d2"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #446"
  target_artifact: "docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md"
  optional_no_change_c_artifacts:
    - "docs/implementation_handoffs/parser_corpus_drift_recycle_rollback_external_boundary_comparison.md"
    - "docs/contract_test_reports/parser_corpus_drift_recycle_rollback_external_boundary.md"
  verdict: "recycle_rollback_contract_preserves_blocked_external_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-drift-recycle-rollback-boundary-446"
  base_branch: "main"
  selected_family: "drift_debug.recycle_or_rollback"
  status_decision: "remain_blocked_external_boundary"
  implementation_authorized: "no_metadata_promotion_by_default"
  tracker_status: "open"
  parent_issue_status: "open"
  later_external_candidates:
    - "timer.inactivity_timeout"
    - "gameplay_stress.conjure"
    - "gameplay_stress.spellbook"
  staged_later_sequence:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/381"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/382"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/383"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/384"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/386"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/385"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/387"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_log_drift_sensor.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close parent issue #434 without explicit authorization."
    - "Do not run private/live/file-system/recycle/rollback/watcher/drift checks."
    - "Do not read private logs in Codex B/C/E."
    - "Do not promote drift_debug.recycle_or_rollback or any blocked row by default."
    - "Do not claim parser support, recycle handling, rollback detection, watcher correctness, duplicate/replay prevention, drift recovery, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
