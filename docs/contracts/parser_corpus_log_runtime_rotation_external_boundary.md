# Parser Corpus Log Runtime Rotation External Boundary Contract

## Module

Log runtime rotation external-boundary planning for the parser corpus parity
report.

Plain English: this contract defines the narrowest safe Mythic Edge-owned
boundary for `log_runtime.rotation`. Mythic Edge has tailer and stream
rotation signals that can be referenced as committed report-only context, but
those signals do not prove live file-system watcher correctness, log-rotation
resilience, duplicate/replay prevention, private smoke success, parser
support, release readiness, production behavior, analytics truth, AI truth,
coaching truth, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/444
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/442
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/443
- Previous merge commit:
  `32b11c3238b1d572213c5953708f19aa359a2c2f`
- Parent/private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-log-runtime-rotation-boundary-444`
- base_branch: `main`
- observed_base_commit: `32b11c3238b1d572213c5953708f19aa359a2c2f`
- selected_family: `log_runtime.rotation`
- deferred_family: `drift_debug.recycle_or_rollback`
- target_artifact:
  `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
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

- issue #444, tracker #158, parent issue #434, issue #442, and PR #443
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `docs/contracts/parser_corpus_live_diagnostics_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_stream_unit.py`
- `tests/test_event_schema_snapshots.py`
- parser-evidence workflow issues #381 through #387 as later pipeline
  context only

## Observed Current Behavior

Observed on `main` at
`32b11c3238b1d572213c5953708f19aa359a2c2f`:

- Issue #444 is open.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- Issue #442 is complete after PR #443.
- The corpus parity CLI reports:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- `log_runtime.rotation` is currently represented only by
  `external_reference_category_boundary`.
- `log_runtime.rotation` currently has:
  - `coverage_status`: `blocked_external_boundary`
  - `coverage_basis`: `["external_reference_only"]`
  - `mythic_edge_entries`: `["external_reference_category_boundary"]`
- The same broad external-reference entry also covers:
  - `timer.inactivity_timeout`
  - `gameplay_stress.conjure`
  - `gameplay_stress.spellbook`
  - `drift_debug.recycle_or_rollback`
- `drift_debug.rename_or_rotation_collision` is already
  `covered_report_only` through
  `rename_rotation_collision_boundary_report_v1`, and that contract
  explicitly says tailer/stream rotation signals do not prove collision
  support, live file-system truth, duplicate/replay prevention, private smoke
  success, release readiness, production behavior, analytics truth, AI truth,
  coaching truth, or full corpus parity.
- `FileTailer.poll_once(...)` produces `TailBatch.rotated=True` when the
  current file size is smaller than the prior offset, resets the line buffer,
  and reads replacement content from the beginning.
- `MtgaEventStream` publishes a `LogFileRotatedEvent` with a sanitized file
  name when a polled `TailBatch` is rotated.
- Focused tests cover:
  - synthetic replacement-content rotation in `tests/test_tailer.py`;
  - sanitized `LogFileRotatedEvent` output in
    `tests/test_stream_integration.py`.
- Current committed tests do not prove live MTGA log rotation resilience,
  watcher correctness, file identity tracking, duplicate/replay prevention,
  recycle/rollback behavior, private smoke success, production behavior, or
  full corpus parity.

## Scope Decision

Selected path: report-only boundary metadata for `log_runtime.rotation`.

Implementation may proceed as corpus metadata/test work only:

- add a dedicated report-only manifest entry for `log_runtime.rotation`;
- add a dedicated session-ledger entry for `log_runtime.rotation`;
- update focused corpus parity tests to pin the row and adjacent-row
  protections;
- produce an implementation handoff and contract-test report.

Codex C must remove `log_runtime.rotation` from the broad
`external_reference_category_boundary` entry when adding the dedicated
report-only row. This keeps the matrix from mixing
`fixture_metadata_only` and `external_reference_only` basis values for the
same family. The broad external boundary must continue to cover the still
blocked external rows:

- `timer.inactivity_timeout`
- `gameplay_stress.conjure`
- `gameplay_stress.spellbook`
- `drift_debug.recycle_or_rollback`

Reasoning:

- The selected family is narrower than recycle/rollback or
  rename/rotation-collision.
- Mythic Edge has committed, inspectable reference surfaces for the narrow
  rotation signal: `TailBatch.rotated`, `LogFileRotatedEvent`, and focused
  tests around synthetic replacement/truncation and sanitized event payloads.
- Those reference surfaces are enough for report-only boundary metadata, but
  not enough for parser support, live watcher correctness, real filesystem
  rotation truth, duplicate/replay prevention, private smoke, readiness,
  production, analytics, AI, coaching, or full corpus parity claims.
- Leaving the row in `blocked_external_boundary` would understate the
  inspected Mythic Edge-owned reference boundary now available.
- Moving the row to a stronger status than `covered_report_only` would
  overstate the evidence.

This decision does not authorize parser, tailer, stream, event, diagnostics,
drift, golden replay, feature-equity, evidence-ledger, workbook, webhook,
Apps Script, Sheets, analytics, AI, coaching, CI, merge, deploy, production,
or final integration behavior changes.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for `log_runtime.rotation`.
Parser/log runtime code owns the current tailer and stream behavior. Corpus
parity may reference that behavior as report-only context, but it must not
reinterpret it as live runtime support or readiness.

## Internal Project Area

Corpus / Provenance, with Quality / Governance support for contracts,
handoffs, reports, validation, secret/private-marker scans, and
protected-surface checks.

This slice is not a Parser behavior module, tailer behavior module, stream
module, event-shape module, diagnostics implementation, drift-report
implementation, local app watcher implementation, analytics module, AI module,
coaching module, CI gate, merge gate, deploy gate, readiness gate, or
production module.

## Truth Owner

Truth owner for `log_runtime.rotation` corpus coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_stream_unit.py`
- `tests/test_event_schema_snapshots.py`

Truth boundary:

- `FileTailer` may report a simple rotated flag for one observed
  size-shrink/replacement condition.
- `MtgaEventStream` may emit a sanitized `LogFileRotatedEvent` when it sees
  that flag.
- Corpus parity may record an inspected report-only coverage boundary for
  `log_runtime.rotation`.
- Corpus parity must not infer live file-system watcher correctness,
  robust log-rotation resilience, duplicate/replay prevention, file identity
  tracking, recycle/rollback truth, private smoke success, live Player.log
  health, parser support, release readiness, production behavior, analytics
  truth, AI truth, coaching truth, tracker completion, or full corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser / log runtime support.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing committed tailer/stream/event code and focused tests
  -> bounded report-only manifest/session-ledger metadata
  -> corpus parity row for log_runtime.rotation
```

Forbidden reverse flow:

- Corpus metadata must not change parser, tailer, stream, event class,
  diagnostics, drift, golden replay, feature-equity, evidence-ledger,
  workbook, webhook, Apps Script, Sheets, analytics, AI, coaching, CI, merge,
  deploy, production, or tracker behavior.
- Corpus metadata must not cause `TailBatch.rotated` or
  `LogFileRotatedEvent` to become proof of live watcher correctness, real
  filesystem rotation truth, duplicate/replay prevention, recycle/rollback
  truth, private smoke success, readiness, production behavior, analytics
  truth, AI truth, coaching truth, or full corpus parity.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- tailer behavior
- stream behavior
- `LogFileRotatedEvent` shape
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status files
- failed posts
- workbook exports
- analytics truth
- AI/model-provider behavior
- coaching behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md`

Files Codex C may inspect but must not change unless a separate contract
explicitly authorizes it:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_stream_unit.py`
- `tests/test_event_schema_snapshots.py`
- adjacent corpus, diagnostics, drift, golden replay, feature-equity, and
  evidence-ledger contracts, handoffs, reports, source, and focused tests

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
- parser source, parser events, runtime source, diagnostics source, drift
  source, workbook/webhook/App Script/Sheets surfaces, analytics, AI,
  coaching, CI, merge, deploy, production, or tracker lifecycle surfaces.

## Public Interface

This contract adds no runtime public API.

The public interface is the corpus parity compatibility report generated from
the committed corpus manifest and session ledger.

Expected corpus report effect after Codex C:

- `log_runtime.rotation` changes from `blocked_external_boundary` to
  `covered_report_only`.
- `log_runtime.rotation` uses a dedicated Mythic Edge entry:
  `log_runtime_rotation_boundary_report_v1`.
- `coverage_basis` is exactly `["fixture_metadata_only"]`.
- `parser_event_families` remains `[]`.
- The row carries explicit notes that report-only rotation coverage does not
  prove parser support, live watcher correctness, file-system truth,
  duplicate/replay prevention, recycle/rollback truth, private smoke success,
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  or full corpus parity.
- `external_reference_category_boundary` no longer lists
  `log_runtime.rotation`; it continues to list the still blocked external
  rows named above.
- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.

## Required Corpus Manifest Entry

Codex C should add one dedicated Mythic Edge entry for
`log_runtime.rotation`.

Recommended manifest entry values:

- `entry_id`: `log_runtime_rotation_boundary_report_v1`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/444`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `scenario_families`: `["log_runtime.rotation"]`
- `parser_event_families`: `[]`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["fixture_metadata_only"]`
- `paths` should point only to committed source/test/docs artifacts, such as:
  - `tailer_module`: `src/mythic_edge_parser/log/tailer.py`
  - `stream_module`: `src/mythic_edge_parser/stream.py`
  - `events_module`: `src/mythic_edge_parser/events.py`
  - `tailer_test`: `tests/test_tailer.py`
  - `stream_integration_test`: `tests/test_stream_integration.py`
  - `event_schema_snapshot_test`: `tests/test_event_schema_snapshots.py`
  - `corpus_parity_test`: `tests/test_corpus_parity_report.py`
  - `session_ledger`: `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - `rename_rotation_collision_contract`:
    `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`

Required `parser_claim_families`:

- `log_runtime_rotation_boundary_report`
- `tailer_rotation_reference_only`
- `stream_log_file_rotated_reference_only`
- `live_watcher_correctness_non_claim`
- `filesystem_rotation_truth_non_claim`
- `duplicate_replay_prevention_non_claim`
- `recycle_or_rollback_non_claim`
- `private_smoke_non_claim`
- `readiness_production_non_claim`
- `analytics_ai_coaching_non_claim`

Required notes must state that this is report-only boundary metadata and is
not evidence of:

- parser support;
- live file-system watcher correctness;
- robust log-rotation resilience;
- duplicate/replay prevention;
- file identity tracking;
- recycle/rollback truth;
- private smoke success;
- live Player.log health;
- release readiness;
- deploy readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- full Mythic Edge corpus parity.

## Required Session Ledger Entry

Codex C should add one session-ledger entry:

- `session_id`: `log_runtime_rotation_boundary_report_v1`
- `title`: `Log runtime rotation boundary report`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`
- `linked_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/444`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`
- `scenario_families`: `["log_runtime.rotation"]`
- `format_family`: `log_runtime`
- `match_shape`: `log_runtime_rotation_boundary_report_only`
- `record_summary`: `committed_log_runtime_rotation_boundary_metadata_only`
- `game_rows`: `{"count": 0, "result_shape": "not_applicable"}`

Recommended `parser_coverage` fields:

- `tailer_rotation_reference_entries`: 1
- `stream_rotation_event_reference_entries`: 1
- `dedicated_live_rotation_fixtures`: 0
- `private_smoke_success_claims`: 0
- `live_watcher_correctness_claims`: 0
- `filesystem_rotation_truth_claims`: 0
- `duplicate_replay_prevention_claims`: 0
- `file_identity_tracking_claims`: 0
- `recycle_or_rollback_claims`: 0
- `production_support_claims`: 0
- `event_families`: `{}`

Required `report_only_redactions` must set every private/raw field to false,
including at least:

- `raw_log_lines_included`: false
- `raw_payloads_included`: false
- `private_paths_included`: false
- `private_smoke_outputs_included`: false
- `generated_private_runtime_artifacts_included`: false
- `file_hashes_included`: false
- `file_path_identities_included`: false
- `external_logs_included`: false
- `sqlite_files_included`: false
- `workbook_exports_included`: false
- `credentials_tokens_keys_webhooks_included`: false

## Required Adjacent-Row Protections

Codex C must preserve:

- `drift_debug.recycle_or_rollback`: `blocked_external_boundary`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `connection.firewall_or_network_drop`: `blocked_private_evidence`
- `mythic_edge.private_log_report_only_drift`: `blocked_private_evidence`
- `drift_debug.rename_or_rotation_collision`: `covered_report_only`

Codex C must not reinterpret these rows as covered by
`log_runtime.rotation`:

- `drift_debug.rename_or_rotation_collision`
- `drift_debug.recycle_or_rollback`
- `log_runtime.malformed_or_headerless`
- `log_runtime.timestamp_anomaly`
- `log_runtime.unknown_entry`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `connection.firewall_or_network_drop`

## Inputs

### Allowed Inputs For This Contract Pass

- issue #444, tracker #158, issue #434, issue #442, PR #443, and current
  `main` metadata;
- current committed contracts, handoffs, reports, manifest, session ledger,
  corpus parity code, tailer code, stream code, event definitions, and focused
  tests;
- parser-evidence workflow issue titles/states for #381 through #387.

### Allowed Inputs For Codex C

- committed repo source, docs, tests, manifest, session ledger, and issue/PR
  metadata;
- focused test output from synthetic temp-directory tailer/stream tests;
- corpus parity CLI output.

### Forbidden Inputs

Forbidden in Codex B, Codex C, and any committed artifact:

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
- app-data checks;
- live MTGA checks;
- firewall/drop checks;
- network checks;
- packet checks;
- OS/router checks;
- file-system rotation checks against local private files;
- watcher checks;
- tailer checks against private logs;
- drift checks against private logs;
- diagnostics checks against private logs;
- private smoke checks.

## Outputs

Output of this Codex B pass:

- `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`

Authorized Codex C outputs:

- updated `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- updated `tests/fixtures/parser_corpus/session_ledger.v1.json`
- updated `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md`

Forbidden outputs:

- parser/tailer/stream/event behavior changes;
- executable tooling;
- local/private evidence packets;
- generated runtime artifacts;
- private smoke outputs;
- live rotation reports;
- private drift reports;
- corpus status promotion for any row other than the deliberate
  `log_runtime.rotation` report-only boundary;
- any claim that `covered_report_only` means runtime support or readiness.

## Required Guarantees

The future implementation must guarantee:

- Only `log_runtime.rotation` changes coverage status in this slice.
- `log_runtime.rotation` becomes `covered_report_only`.
- `log_runtime.rotation` uses `coverage_basis == ["fixture_metadata_only"]`.
- `log_runtime.rotation` has no parser event families.
- `external_reference_category_boundary` no longer lists
  `log_runtime.rotation`.
- `external_reference_category_boundary` continues to list the still blocked
  external rows.
- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- Private-evidence rows remain `blocked_private_evidence`.
- No private or external raw artifacts are committed.
- Tailer, stream, event, diagnostics, drift, corpus report code, parser,
  workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge, deploy,
  production, and final integration behavior remain unchanged.

## Unknowns

- Whether future coverage should include a committed synthetic fixture that
  exercises a reduced rotation model remains outside this slice.
- Whether future local/private evidence can prove live watcher correctness
  remains outside this slice.
- Whether `drift_debug.recycle_or_rollback` can be report-only or needs
  evidence-generation work remains deferred.
- Whether future UTC_Log adapter work from #381 changes the evidence path for
  live rotation remains deferred.

## Suspected Gaps

- Current tailer rotation detection is size-shrink based; it does not prove
  all real-world Arena rotation shapes.
- Current stream behavior emits a sanitized rotation event; it does not prove
  end-to-end runtime recovery.
- Current tests use temp-file and fake-tailer surfaces; they do not prove live
  watcher correctness.
- Current corpus metadata can name report-only boundaries, but it cannot prove
  private smoke success or production readiness.

## Invariants

- Codex B must not implement code.
- Codex B must not run private checks.
- Codex C must not run private/live/file-system rotation/watcher checks.
- Codex C must not change parser/tailer/stream/event behavior.
- No raw/private/local artifacts may be committed.
- `log_runtime.rotation` report-only coverage is not parser support.
- `log_runtime.rotation` report-only coverage is not live watcher
  correctness.
- `log_runtime.rotation` report-only coverage is not file-system rotation
  truth.
- `log_runtime.rotation` report-only coverage is not duplicate/replay
  prevention.
- `log_runtime.rotation` report-only coverage is not recycle/rollback truth.
- `drift_debug.recycle_or_rollback` remains deferred and blocked.
- Tracker #158 remains open.
- Parent issue #434 remains open.

## Error Behavior

If current repo state does not include merge commit
`32b11c3238b1d572213c5953708f19aa359a2c2f`, stop and refresh/rebase before
contract or implementation work.

If Codex C finds `log_runtime.rotation` already changed from the observed
state, it must record the mismatch and route back to Codex B or Codex A unless
the new state is already explained by a merged contract.

If the broad external boundary cannot be narrowed without changing unrelated
rows, stop and route back to Codex B.

If any proposed implementation requires changing tailer, stream, event,
diagnostics, drift, parser, workbook, webhook, Apps Script, analytics, AI, or
production behavior, stop and route back to Codex A/B for a new scope.

If private or raw artifacts appear in the diff, stop, remove them, and route
to Codex D only if the fix is concrete and contract-preserving.

## Side Effects

Allowed in this contract pass:

- write this contract file;
- inspect GitHub issue and PR metadata;
- inspect committed repo docs, code, tests, manifests, templates, and reports;
- run documentation, corpus parity, secret/private-marker, protected-surface,
  and whitespace checks.

Allowed in Codex C:

- change corpus manifest/session ledger/test metadata for this selected row;
- write an implementation handoff;
- write a contract-test report;
- run focused validation.

Forbidden in this contract pass and Codex C implementation pass:

- run private Player.log, UTC_Log, app-data, file-system rotation, live MTGA,
  watcher, tailer, drift, diagnostics, network, or private smoke checks;
- read private logs;
- implement parser/tailer/stream/event changes;
- implement executable tooling;
- add synthetic file-system fixtures beyond metadata unless a future contract
  authorizes that evidence path;
- open a PR;
- close #158, #434, or #444.

## Dependency Order

Future work must proceed in this order:

1. Codex B completes this contract.
2. Codex C updates corpus metadata/tests/report artifacts only.
3. Codex E reviews the implementation against this contract.
4. Codex F submits reviewed files if requested.
5. Codex G handles merge/close/tracker work only after explicit user request.
6. A later Codex A/B issue may address `drift_debug.recycle_or_rollback`.
7. Parser-evidence pipeline issues #381 through #387 remain later work and
   are not reordered by this contract.

## Compatibility

This contract preserves:

- existing corpus parity vocabulary;
- existing report-only boundary vocabulary;
- existing private-evidence blocked rows;
- existing external-boundary rows other than the selected row;
- existing rename/rotation collision report-only boundary;
- existing tailer/stream/event behavior;
- existing parser-evidence pipeline issues #381 through #387;
- existing parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior.

## Tests Required

Required Codex B validation:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_event_schema_snapshots.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md
printf '%s\n' \
  docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md
```

Required Codex C validation:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_event_schema_snapshots.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md \
  docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md \
  docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Codex E should verify:

- Only `log_runtime.rotation` changes status.
- `drift_debug.recycle_or_rollback` remains blocked and deferred.
- `external_reference_category_boundary` still covers the remaining external
  rows but no longer covers `log_runtime.rotation`.
- `log_runtime.rotation` is report-only with no parser event families.
- No tailer/stream/event/runtime behavior changed.
- No private/raw/local artifacts were committed.
- Non-claims are preserved in contract, handoff, report, tests, and PR text.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md`.
- The contract names Corpus / Provenance as the owning layer.
- The contract deliberately selects report-only boundary metadata for
  `log_runtime.rotation`.
- The contract explicitly defers `drift_debug.recycle_or_rollback`.
- The contract defines required manifest and session-ledger shapes.
- The contract defines adjacent-row protections.
- The contract forbids private/live/file-system rotation/watcher checks.
- The contract forbids parser/tailer/stream/event behavior changes.
- The contract defines validation expectations for Codex C/E/F/G.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Codex C should implement only the corpus metadata/test/report package
authorized by this contract.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #444.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/444

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/443

Previous merge commit:
32b11c3238b1d572213c5953708f19aa359a2c2f

Base branch:
main

Contract:
docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md

Goal:
Implement the report-only corpus boundary for log_runtime.rotation exactly as
contracted. This is corpus metadata, focused test, handoff, and report work
only. Do not change parser/tailer/stream/event/runtime behavior and do not run
private/live/file-system rotation checks.

Do:
- Refresh live GitHub and local git state.
- Verify main includes 32b11c3238b1d572213c5953708f19aa359a2c2f.
- Compare current corpus manifest/session ledger/tests against the contract
  before editing.
- Add log_runtime_rotation_boundary_report_v1 as a dedicated report-only
  manifest entry.
- Add the matching session-ledger entry.
- Remove log_runtime.rotation from external_reference_category_boundary while
  preserving timer.inactivity_timeout, gameplay_stress.conjure,
  gameplay_stress.spellbook, and drift_debug.recycle_or_rollback there.
- Update focused corpus parity tests.
- Preserve drift_debug.recycle_or_rollback as blocked_external_boundary.
- Produce docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md.

Do not:
- Implement code.
- Open a PR unless separately asked.
- Close tracker #158, parent issue #434, or issue #444.
- Run private Player.log, UTC_Log, app-data, filesystem-rotation, live MTGA,
  watcher, tailer, drift, diagnostics, network, or private smoke checks.
- Read private logs.
- Commit raw private logs, exact private paths, exact offsets, exact file
  sizes, exact private timestamps, raw hashes, runtime logs, runtime status
  files, failed posts, SQLite files, workbook exports, screenshots, secrets,
  credentials, tokens, API keys, webhook URLs, local-only artifacts, private
  reports, or external corpus contents.
- Promote drift_debug.recycle_or_rollback or any blocked row by default.
- Claim parser support, tailer correctness, filesystem rotation correctness,
  private smoke success, live Player.log health, drift health, release
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  or full corpus parity.
- Change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, tailer behavior, stream behavior,
  LogFileRotatedEvent shape, diagnostics report shape, drift report behavior,
  golden replay behavior, feature-equity behavior, evidence-ledger behavior,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.

Validation:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_event_schema_snapshots.py
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/444"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/442"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/443"
  previous_merge_commit: "32b11c3238b1d572213c5953708f19aa359a2c2f"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #444"
  target_artifact: "docs/contracts/parser_corpus_log_runtime_rotation_external_boundary.md"
  expected_next_artifacts:
    - "docs/implementation_handoffs/parser_corpus_log_runtime_rotation_external_boundary_comparison.md"
    - "docs/contract_test_reports/parser_corpus_log_runtime_rotation_external_boundary.md"
  verdict: "log_runtime_rotation_contract_ready_for_report_only_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-log-runtime-rotation-boundary-444"
  base_branch: "main"
  selected_family: "log_runtime.rotation"
  deferred_family: "drift_debug.recycle_or_rollback"
  status_decision: "covered_report_only_boundary_metadata"
  tracker_status: "open"
  parent_issue_status: "open"
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
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_tailer.py tests/test_stream_integration.py tests/test_stream_unit.py tests/test_event_schema_snapshots.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close parent issue #434 without explicit authorization."
    - "Do not run private/live/file-system rotation/watcher checks."
    - "Do not read private logs in Codex B/C."
    - "Do not promote drift_debug.recycle_or_rollback or any blocked row by default."
    - "Do not claim parser support, file-system watcher correctness, log-rotation resilience, recycle/rollback truth, private smoke success, live Player.log health, release readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
