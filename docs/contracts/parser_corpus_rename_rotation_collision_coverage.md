# Parser Corpus Rename Rotation Collision Coverage Contract

## Module

Rename / rotation / recycle-collision corpus evidence boundary for the parser
corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`drift_debug.rename_or_rotation_collision` as report-only boundary metadata.
It does not add parser support, committed log fixtures, synthetic file-system
fixtures, live watcher support, log-rotation truth, rename/recycle collision
handling, duplicate/replay prevention, parser drift recovery truth, private
smoke success, release readiness, production behavior, analytics truth, AI
truth, coaching truth, or full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating timestamp anomaly
reporting, unknown-entry reporting, missing-message-type report-only coverage,
log discovery, file tailing, stream rotation events, diagnostics,
log-drift reporting, golden replay behavior, feature-equity behavior,
corpus parity metadata, or public Manasight taxonomy metadata as
rename/rotation collision support.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/416
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/415
- Previous merge commit:
  `c0691fa4e53198179a76efdd5f05b33390f817ff`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-rename-rotation-collision-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `c0691fa4e53198179a76efdd5f05b33390f817ff`
- target_artifact:
  `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md`
- `docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/contracts/parser_corpus_malformed_headerless_coverage.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_tailer_router_integration.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, generated/private/runtime artifacts, workbook exports, SQLite files,
  credentials, tokens, API keys, webhook URLs, decklists, deck names, card
  choices, sideboard choices, private strategy notes, or private reports.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`c0691fa4e53198179a76efdd5f05b33390f817ff`:

- Issue #416 is open and tracker #158 remains open.
- Issue #414 is closed after PR #415 merged missing-message-type report-only
  boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current issue #416 report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 11
  - `partial`: 3
  - `missing`: 5
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `drift_debug.rename_or_rotation_collision` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- `log_runtime.rotation` and `drift_debug.recycle_or_rollback` are represented
  only through `external_reference_category_boundary` as
  `blocked_external_boundary`.
- `drift_debug.missing_message_type` is `covered_report_only` from issue #414.
- `drift_debug.phantom_or_deck_origin` and
  `mythic_edge.private_log_report_only_drift` remain separate future families
  with no Mythic Edge entries.
- `src/mythic_edge_parser/log/tailer.py` reports a simple `TailBatch.rotated`
  flag when the current file size is smaller than the prior offset, resets the
  line buffer, and reads replacement content from the beginning.
- `src/mythic_edge_parser/stream.py` can publish a `LogFileRotatedEvent` with
  a sanitized file name when `TailBatch.rotated` is true.
- Existing tailer and stream tests cover basic replacement-content rotation and
  sanitized rotation-event payload behavior.
- Existing code and tests do not define a corpus-owned
  rename/recycle/rotation-collision fixture, a collision detector, duplicate
  replay prevention truth, file identity tracking truth, private smoke truth,
  or live file-system watcher correctness for this scenario family.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic rename/rotation collision coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, blocked-private-evidence, or
   blocked-external-boundary status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage for
`drift_debug.rename_or_rotation_collision` only.

Reasoning:

- Mythic Edge has adjacent operational surfaces: `FileTailer` can detect one
  simple truncation/replacement rotation shape, `MtgaEventStream` can publish a
  sanitized rotation event, and drift/diagnostics/reporting surfaces can review
  routed and unknown entries.
- Those adjacent surfaces are intentionally not enough to claim
  rename/rotation collision support. They do not prove file identity tracking,
  rename collision detection, recycle/rollback detection, duplicate/replay
  prevention, live watcher correctness, private smoke success, parser drift
  recovery, or production behavior.
- A synthetic collision fixture would need a later contract that defines a
  reduced file-system model, allowed state transitions, expected event/report
  behavior, and exactly which collision shape counts as supported.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic metadata or a safely redacted
  local review report.
- Leaving the row plain `missing` hides an important inspected boundary:
  existing rotation-adjacent behavior has been reviewed and explicitly does
  not count as this drift-debug family.

This decision records `drift_debug.rename_or_rotation_collision` as
report-only boundary metadata. It changes corpus parity metadata and tests
only; it does not change parser behavior, file tailer/watcher behavior, log
discovery behavior, stream behavior, diagnostics, log-drift reports, golden
replay, feature-equity behavior, evidence-ledger behavior, runtime behavior,
analytics behavior, or production behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`drift_debug.rename_or_rotation_collision`. Parser modules own event
interpretation. The tailer/stream layer owns current operational rotation
signals. Diagnostics, log-drift reporting, golden replay, feature-equity, and
evidence ledger are downstream or review surfaces unless a separate contract
grants them a stronger role. Corpus parity artifacts own only the
coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence, tailer/stream context, and
Quality / Governance evidence for context, but it is not a Parser behavior
module, file-watcher module, log-discovery module, stream module, diagnostics
module, log-drift module, golden replay module, feature-equity module,
evidence-ledger module, analytics module, AI module, coaching module,
release-readiness module, or production module.

## Truth Owner

Truth owner for `drift_debug.rename_or_rotation_collision` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/router.py`

Truth boundary:

- `FileTailer.poll_once(...)` may say whether current code observed one simple
  replacement/truncation rotation condition for one path.
- `MtgaEventStream` may say whether current code emitted a sanitized
  `LogFileRotatedEvent` from a `TailBatch.rotated` flag.
- Router, diagnostics, log-drift, golden replay, and feature-equity modules may
  summarize their current parser/review outputs.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `drift_debug.rename_or_rotation_collision`.
- Corpus parity must not infer live file-system truth, log-rotation truth,
  rename/recycle collision handling, duplicate/replay prevention, file identity
  tracking, parser drift recovery truth, private smoke success, production
  behavior, analytics truth, AI truth, coaching truth, release readiness, or
  full corpus parity from those adjacent surfaces.

Coverage status is review metadata. It is not parser truth, file-system truth,
rotation truth, collision truth, diagnostics truth, replay truth,
evidence-ledger truth, analytics truth, AI truth, coaching truth, merge
readiness, deploy readiness, public/private release readiness, or
tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing tailer/stream/drift/diagnostics adjacent behavior
  -> bounded committed report-only corpus manifest/session-ledger metadata
  -> corpus parity coverage row for drift_debug.rename_or_rotation_collision
```

Forbidden reverse flow:

- Corpus coverage status must not change parser, router, tailer, watcher, log
  discovery, stream, diagnostics, log-drift, golden replay, feature-equity, or
  evidence-ledger behavior.
- Corpus metadata must not add collision detection, alter file identity
  tracking, reinterpret `LogFileRotatedEvent`, reinterpret unknown entries,
  reinterpret timestamp anomalies, change diagnostics, change drift reports,
  change runtime status, change workbook output, change analytics, change
  AI/coaching, or change release/production policy.
- Corpus metadata must not turn report-only boundary notes into parser support,
  file-system support, synthetic fixture truth, live private drift proof, merge
  readiness, deploy readiness, or full parity.

Protected surfaces explicitly not touched:

- parser behavior
- file tailer/watcher behavior
- log discovery behavior
- stream behavior
- parser state final reconciliation
- parser event classes
- router semantics
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime status artifacts or schema
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- delivery retry artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/router.py`
- `tests/test_tailer.py`
- `tests/test_stream_integration.py`
- `tests/test_tailer_router_integration.py`
- relevant diagnostics, log-drift, golden replay, feature-equity, and
  protected-surface tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- router dispatch changes
- tailer behavior changes
- watcher or file-discovery behavior changes
- stream behavior changes
- `LogFileRotatedEvent` shape changes
- collision detection implementation
- file identity tracking implementation
- duplicate/replay prevention implementation
- new file-system fixtures
- new committed raw log fixtures
- synthetic collision support claims
- diagnostics report shape changes
- log-drift report shape changes
- golden replay behavior changes
- feature-equity behavior changes
- evidence-ledger schema/vocabulary changes
- runtime status changes
- local live smoke execution
- Manasight corpus import
- log-runtime rotation, recycle/rollback, missing-message-type,
  phantom/deck-origin, private-log drift, analytics-readiness, AI, coaching,
  CI, final integration, and production surfaces

## Public Interface

No new runtime public API is authorized.

Authorized corpus manifest row:

- `scenario_family`: `drift_debug.rename_or_rotation_collision`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["fixture_metadata_only"]`
- `parser_event_families`: `[]`
- `entry_id`: `rename_rotation_collision_boundary_report_v1`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`

Required parser claim families for the entry:

- `rename_rotation_collision_boundary_report`
- `tailer_rotation_not_collision_truth`
- `log_runtime_rotation_not_collision_truth`
- `recycle_or_rollback_not_collision_truth`
- `unknown_entry_not_collision_truth`
- `timestamp_anomaly_not_collision_truth`
- `missing_message_type_not_collision_truth`
- `file_system_truth_non_claim`
- `duplicate_replay_prevention_non_claim`

Required note non-claims:

- rename/rotation collision parser support
- log-rotation truth
- live file-system truth
- file identity tracking truth
- rename/recycle collision handling
- duplicate/replay prevention
- parser drift recovery truth
- private smoke success
- live watcher correctness
- diagnostics readiness
- release readiness
- production behavior
- analytics truth
- AI truth
- coaching truth
- full Mythic Edge corpus parity

Authorized session-ledger entry:

- `session_id`: `rename_rotation_collision_boundary_report_v1`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `scenario_families`: `["drift_debug.rename_or_rotation_collision"]`
- `format_family`: `drift_debug`
- `match_shape`: `rename_rotation_collision_boundary_report_only`
- `record_summary`: `committed_rename_rotation_collision_boundary_metadata_only`
- `game_rows_count`: `0`
- `result_shape`: `not_applicable`

Required `parser_coverage` facts:

- `event_families`: `{}`
- `unknown_entries`: `0`
- `truncation_count`: `0`
- `tailer_rotation_reference_entries`: `1`
- `stream_rotation_event_reference_entries`: `1`
- `log_drift_reference_entries`: `1`
- `diagnostics_reference_entries`: `1`
- `golden_replay_reference_entries`: `1`
- `feature_equity_reference_entries`: `1`
- `dedicated_rename_rotation_collision_fixtures`: `0`
- `file_identity_tracking_claims`: `0`
- `rename_collision_detection_claims`: `0`
- `recycle_collision_detection_claims`: `0`
- `duplicate_replay_prevention_claims`: `0`
- `private_smoke_success_claims`: `0`
- `production_watcher_support_claims`: `0`

## Required Guarantees

- Only `drift_debug.rename_or_rotation_collision` may be changed by Codex C.
- The selected coverage status must be `covered_report_only`.
- The selected coverage basis must be exactly `["fixture_metadata_only"]`.
- The row must not list parser event families.
- The session-ledger entry must be committed metadata only and must not contain
  raw log lines, raw private payloads, raw external payloads, file path
  identities, file hashes, byte-size lists, capture-date rows, decklists,
  card choices, generated data, runtime artifacts, SQLite files, workbook
  exports, credentials, tokens, API keys, or webhook URLs.
- The row must explicitly say that adjacent tailer/stream rotation,
  log-runtime rotation, recycle/rollback, unknown-entry, timestamp anomaly,
  missing-message-type, diagnostics, log-drift, golden replay, feature-equity,
  and public taxonomy surfaces are non-claims for
  rename/rotation-collision support.
- Existing coverage statuses for adjacent families must not be changed:
  - `log_runtime.rotation`
  - `drift_debug.recycle_or_rollback`
  - `drift_debug.missing_message_type`
  - `drift_debug.phantom_or_deck_origin`
  - `mythic_edge.private_log_report_only_drift`
- Corpus parity summary counts may change only as the direct result of moving
  one family from `missing` to `covered_report_only`.
- No parser behavior or protected downstream behavior may change.

## Unknowns

- Which live MTGA log rotation, rename, recycle, or file-replacement shapes
  can create duplicate/replay or missed-entry hazards.
- Whether future safe synthetic evidence should model file-size shrink,
  inode/file-identity replacement, rename collision, rapid recycle/rollback,
  duplicate reads, missing reads, or a smaller subset.
- Whether the correct future behavior should belong to tailer, stream,
  diagnostics, log-drift report, golden replay, runtime status, or a new
  parser-resilience review artifact.
- Which future fixture shape would be privacy-safe and representative without
  importing external or private raw logs.

## Suspected Gaps

- Current corpus parity has no dedicated Mythic Edge entry for
  `drift_debug.rename_or_rotation_collision`.
- Current tailer/stream behavior has a simple rotation signal, but no
  dedicated rename/recycle collision support claim.
- Current unknown-entry, timestamp-anomaly, missing-message-type, log-runtime
  rotation, and recycle/rollback rows could be overread unless this boundary
  is explicit.

## Validation Obligations

Codex C must run, at minimum:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Recommended if Codex C relies on tailer/stream context in the implementation
handoff:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py tests/test_stream_integration.py tests/test_tailer_router_integration.py
```

Codex C may add focused corpus parity tests only when needed to enforce:

- `drift_debug.rename_or_rotation_collision` is `covered_report_only`.
- `coverage_basis` is exactly `["fixture_metadata_only"]`.
- `parser_event_families` is empty.
- The session-ledger entry has zero parser-event, raw-log, collision-fixture,
  file-identity, duplicate-prevention, private-smoke, and production-watcher
  support claims.
- Adjacent family statuses remain unchanged.

Codex C must produce:

- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`

## Stop Conditions

- Do not target main directly.
- Do not close issue #416.
- Do not close tracker #158.
- Do not open a PR unless separately asked.
- Do not claim full Mythic Edge corpus parity.
- Do not claim rename/rotation collision support.
- Do not claim support from corpus metadata alone.
- Do not infer live file-system truth, log-rotation truth,
  rename/recycle collision handling, duplicate/replay prevention, private smoke
  success, parser drift recovery truth, release readiness, production behavior,
  analytics truth, AI truth, or coaching truth.
- Do not upgrade or reinterpret `log_runtime.rotation`,
  `drift_debug.recycle_or_rollback`, `drift_debug.missing_message_type`,
  `drift_debug.phantom_or_deck_origin`, or
  `mythic_edge.private_log_report_only_drift` without separate contract
  authority.
- Do not import, copy, mirror, or commit Manasight raw logs or external corpus
  contents.
- Do not commit private Player.log excerpts, private local logs, private smoke
  outputs, generated/private/runtime artifacts, workbook exports, credentials,
  tokens, API keys, webhook URLs, decklists, deck names, card choices,
  sideboard choices, private strategy notes, or private reports.
- Do not change parser behavior, file tailer/watcher behavior, log discovery
  behavior, diagnostics behavior, log-drift behavior, golden replay behavior,
  feature-equity behavior, evidence-ledger behavior, parser state final
  reconciliation, parser event classes, router semantics, diagnostics report
  shape, drift report behavior, match/game identity, deduplication, workbook
  schema, webhook payload shape, Apps Script behavior, Google Sheets sync,
  output transport, runtime status files, delivery retry artifacts, workbook
  exports,
  analytics truth, AI truth, coaching behavior, OpenAI/model-provider
  behavior, CI gates, merge readiness, deploy readiness, production behavior,
  or final integration policy without a new explicit contract.

## Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #416.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/416

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_rename_rotation_collision_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change for
  `drift_debug.rename_or_rotation_collision` according to the contract. The
  selected path is report-only boundary coverage, not parser support, not file
  watcher support, not log-rotation truth, and not synthetic collision support.

  Required scope:
  - Update only the corpus manifest/session ledger and focused corpus parity
    tests needed for the contract.
  - Add docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md.
  - Add docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md.
  - Keep `drift_debug.rename_or_rotation_collision` as `covered_report_only`.
  - Keep `coverage_basis` exactly `["fixture_metadata_only"]`.
  - Keep `parser_event_families` empty.
  - Explicitly preserve non-claims for tailer/stream rotation,
    log-runtime rotation, recycle/rollback, unknown-entry, timestamp anomaly,
    missing-message-type, diagnostics, log-drift, golden replay,
    feature-equity, corpus parity metadata, and public taxonomy surfaces.
  - Do not change adjacent scenario-family statuses except for summary counts
    caused by this one coverage move.

  Do not:
  - Implement parser behavior.
  - Change file tailer/watcher behavior, log discovery behavior, stream
    behavior, diagnostics, log-drift reports, golden replay, feature-equity,
    evidence-ledger, analytics, workbook, webhook, Apps Script, AI/coaching,
    production, CI, merge, or deploy behavior.
  - Add raw log fixtures, private artifacts, external corpus contents, file
    system fixtures, or synthetic collision parser/runtime fixtures.
  - Claim rename/rotation collision support, log-rotation truth, live
    file-system truth, file identity tracking truth, duplicate/replay
    prevention, parser drift recovery truth, private smoke success, release
    readiness, production readiness, AI truth, analytics truth, coaching truth,
    or full corpus parity.
  - Target main directly.
  - Close issue #416 or tracker #158.
  - Stage or commit unless explicitly asked.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
  - printf '%s\n' docs/contracts/parser_corpus_rename_rotation_collision_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests tools
  - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/415"
  previous_merge_commit: "c0691fa4e53198179a76efdd5f05b33390f817ff"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_rename_rotation_collision_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-rename-rotation-collision-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/415"
  previous_merge_commit: "c0691fa4e53198179a76efdd5f05b33390f817ff"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_rename_rotation_collision_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-rename-rotation-collision-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret and protected-surface checks"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #416."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim rename/rotation collision support, log-rotation truth, live file-system truth, file identity tracking truth, duplicate/replay prevention, parser drift recovery truth, private smoke success, release readiness, production readiness, AI truth, analytics truth, or coaching truth."
    - "Do not upgrade or reinterpret log_runtime.rotation, drift_debug.recycle_or_rollback, drift_debug.missing_message_type, drift_debug.phantom_or_deck_origin, or mythic_edge.private_log_report_only_drift without separate contract authority."
    - "Do not import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, sideboard choices, private strategy notes, or private reports."
    - "Do not change parser behavior, file tailer/watcher behavior, log discovery behavior, diagnostics behavior, log-drift behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, drift report behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, delivery retry artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy without a new explicit contract."
```
