# Parser Corpus Missing Message Type Coverage Contract

## Module

Missing-message-type corpus evidence boundary for the parser corpus parity
report.

Plain English: this slice lets Mythic Edge account for exactly
`drift_debug.missing_message_type` as report-only boundary metadata. It does
not add parser support, committed log fixtures, synthetic malformed payload
fixtures, message recovery, hidden payload truth, GameState reconstruction,
unknown future MTGA message support, generic unknown-entry support, parser
resilience truth, release readiness, production behavior, analytics truth, AI
truth, coaching truth, or full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating unknown-entry
drift reporting, GSM truncation coverage, timestamp-anomaly coverage, generic
client-action fallback, GRE GameState parsing, diagnostics, golden replay,
feature-equity behavior, evidence-ledger provenance, or public taxonomy
metadata as missing-message-type support.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/412
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/413
- Previous merge commit:
  `b082f8e11124c0824436a9fad6885af5821816d8`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-missing-message-type-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `b082f8e11124c0824436a9fad6885af5821816d8`
- target_artifact:
  `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md`
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
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, generated/private/runtime artifacts, workbook exports, SQLite files,
  credentials, tokens, API keys, webhook URLs, decklists, card choices,
  private strategy notes, or private reports.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`b082f8e11124c0824436a9fad6885af5821816d8`:

- Issue #414 is open and tracker #158 remains open.
- Issue #412 is closed after PR #413 merged gameplay event-ordering
  report-only boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current issue #414 report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 10
  - `partial`: 3
  - `missing`: 6
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `drift_debug.missing_message_type` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- `log_runtime.unknown_entry` is `covered_report_only` with entry
  `unknown_entry_drift_report_reference_v1`, but its known gap says it does
  not prove missing-message-type recovery.
- `drift_debug.gsm_truncation` has partial count-ratchet evidence and
  `covered_synthetic` truncation marker coverage, but GSM truncation is
  data-loss evidence, not missing parser type-field truth.
- `log_runtime.timestamp_anomaly` is `covered_synthetic`, but timestamp
  anomaly evidence is router timestamp accounting, not parser message-type
  recovery.
- `drift_debug.recycle_or_rollback`,
  `drift_debug.rename_or_rotation_collision`, and
  `drift_debug.phantom_or_deck_origin` remain separate future families.
- GRE parsing recognizes selected GRE markers and can emit `GameState` or
  queued GameState events when the current parser can identify usable payloads.
- GRE GameState payloads preserve or default a `message_type` value for
  current GameState parsing, but current code does not emit a dedicated
  missing-message-type parser event or recovery signal.
- Client action parsing has a generic fallback for unrecognized client-action
  message types, but that fallback is not drift-debug missing-message-type
  support.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic missing-message-type coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, blocked-private-evidence, or
   blocked-external-boundary status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage for
`drift_debug.missing_message_type` only.

Reasoning:

- Mythic Edge has adjacent parser and review surfaces that explain what it does
  with unknown entries, GSM truncation markers, timestamp anomalies, generic
  client-action payloads, and GRE GameState payloads.
- Those adjacent surfaces are intentionally not enough to claim
  missing-message-type support. They do not prove that Mythic Edge can recover
  a parser message type, reconstruct a missing GameState, identify unknown
  future MTGA messages, or safely classify every payload that lacks a type
  field.
- A synthetic missing-message-type fixture would need a later contract that
  defines a reduced malformed-payload model, expected parser behavior, allowed
  event families, and exactly which missing type fields count as supported.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic or sanitized metadata.
- Leaving the row plain `missing` hides an important inspected boundary:
  adjacent drift and parser surfaces have been reviewed and explicitly do not
  count as this scenario family.

This decision records `drift_debug.missing_message_type` as report-only
boundary metadata. It changes corpus parity metadata and tests only; it does
not change parser behavior, router behavior, GRE parsing, client-action
parsing, diagnostics, golden replay, feature-equity behavior, evidence-ledger
behavior, runtime behavior, analytics behavior, or production behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`drift_debug.missing_message_type`. Parser modules own observed event
interpretation, GRE payload handling, client-action payload handling, router
dispatch, parser event classes, parser state behavior, match/game identity,
and deduplication. Diagnostics, golden replay, feature-equity, evidence
ledger, and analytics are downstream or review surfaces unless a separate
contract grants them a stronger role. Corpus parity artifacts own only the
coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance evidence
for context, but it is not a Parser behavior module, router module, GRE parser
module, client-action parser module, diagnostics module, golden replay module,
feature-equity module, evidence-ledger module, analytics module, AI module,
coaching module, release-readiness module, or production module.

## Truth Owner

Truth owner for `drift_debug.missing_message_type` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for parser and downstream behavior referenced only as non-claim
context:

- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`

Truth boundary:

- Router and parser modules may say which current log entries produced parser
  events or were routed as unknown.
- GRE parsing may say which current GRE payload shapes produce GameState or
  queued GameState events.
- Client-action parsing may say which current client-action payloads produce
  specialized or generic client-action events.
- Diagnostics, golden replay, feature-equity, and evidence-ledger reports may
  summarize parser/replay/provenance output for review.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `drift_debug.missing_message_type`.
- Corpus parity must not infer missing-message-type parser support, message
  recovery, hidden payload truth, GameState reconstruction, unknown future MTGA
  message support, live private Player.log drift health, production behavior,
  analytics truth, AI truth, coaching truth, release readiness, or full corpus
  parity from those adjacent surfaces.

Coverage status is review metadata. It is not parser truth,
missing-message-type truth, diagnostics truth, replay truth, evidence-ledger
truth, analytics truth, AI truth, coaching truth, merge readiness, deploy
readiness, public/private release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing parser/drift/diagnostics/evidence-ledger adjacent behavior
  -> bounded committed report-only corpus manifest/session-ledger metadata
  -> corpus parity coverage row for drift_debug.missing_message_type
```

Forbidden reverse flow:

- Corpus coverage status must not change parser, router, GRE, or client-action
  behavior.
- Corpus metadata must not add missing-message-type events, alter parser event
  classes, reinterpret unknown entries, reinterpret GSM truncation markers,
  reinterpret timestamp anomalies, change diagnostics, change golden replay,
  change feature-equity behavior, change evidence-ledger behavior, change
  runtime status, change workbook output, change analytics, change AI/coaching,
  or change release/production policy.
- Corpus metadata must not turn report-only boundary notes into parser support,
  synthetic fixture truth, live private drift proof, merge readiness, deploy
  readiness, or full parity.

Protected surfaces explicitly not touched:

- parser behavior
- router semantics
- GRE parser behavior
- client-action parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- diagnostics report shape
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime status artifacts or schema
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

- `docs/contracts/parser_corpus_missing_message_type_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- relevant focused tests for corpus parity, GRE parsing, client actions,
  diagnostics, golden replay, feature-equity, and evidence-ledger review

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- router dispatch changes
- GRE parser behavior changes
- client-action parser behavior changes
- parser event class changes
- new missing-message-type parser events
- new malformed payload parser fixtures
- new committed raw log fixtures
- synthetic malformed-payload support claims
- diagnostics report shape changes
- golden replay behavior changes
- feature-equity behavior changes
- evidence-ledger schema/vocabulary changes
- runtime status changes
- local live smoke execution
- Manasight corpus import
- unknown-entry, GSM truncation, timestamp-anomaly, recycle/rollback,
  rename/rotation-collision, phantom/deck-origin, private-log-drift,
  analytics-readiness, AI, coaching, CI, final integration, and production
  surfaces

## Public Interface

No new runtime public API is authorized.

Authorized corpus manifest row:

- `scenario_family`: `drift_debug.missing_message_type`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["fixture_metadata_only"]`
- `parser_event_families`: `[]`
- `entry_id`: `missing_message_type_boundary_report_v1`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`

Required parser claim families for the entry:

- `missing_message_type_boundary_report`
- `unknown_entry_not_missing_message_type_truth`
- `gsm_truncation_not_type_field_failure_truth`
- `timestamp_anomaly_not_message_type_truth`
- `generic_client_action_not_drift_debug_support`
- `gre_game_state_message_type_not_recovery_truth`
- `message_recovery_non_claim`

Required note non-claims:

- missing-message-type parser support
- parser message recovery
- hidden payload truth
- GameState reconstruction
- unknown future MTGA message support
- unknown-entry drift truth
- GSM truncation truth
- timestamp anomaly truth
- generic client-action support truth
- diagnostics readiness
- release readiness
- production behavior
- analytics truth
- AI truth
- coaching truth
- full Mythic Edge corpus parity

Authorized session-ledger entry:

- `session_id`: `missing_message_type_boundary_report_v1`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `scenario_families`: `["drift_debug.missing_message_type"]`
- `format_family`: `drift_debug`
- `match_shape`: `missing_message_type_boundary_report_only`
- `record_summary`: `committed_missing_message_type_boundary_metadata_only`
- `game_rows_count`: `0`
- `result_shape`: `not_applicable`

Required `parser_coverage` facts:

- `event_families`: `{}`
- `unknown_entries`: `0`
- `truncation_count`: `0`
- `unknown_entry_reference_entries`: `1`
- `gsm_truncation_reference_entries`: `1`
- `timestamp_anomaly_reference_entries`: `1`
- `gre_game_state_reference_entries`: `1`
- `client_action_reference_entries`: `1`
- `diagnostics_reference_entries`: `1`
- `evidence_ledger_reference_entries`: `1`
- `dedicated_missing_message_type_fixtures`: `0`
- `message_recovery_claims`: `0`
- `game_state_reconstruction_claims`: `0`
- `unknown_future_message_support_claims`: `0`

## Required Guarantees

- Only `drift_debug.missing_message_type` may be changed by Codex C.
- The selected coverage status must be `covered_report_only`.
- The selected coverage basis must be exactly `["fixture_metadata_only"]`.
- The row must not list parser event families.
- The session-ledger entry must be committed metadata only and must not contain
  raw log lines, raw private payloads, raw external payloads, message bodies,
  decklists, card choices, generated data, runtime artifacts, SQLite files,
  workbook exports, credentials, tokens, API keys, or webhook URLs.
- The row must explicitly say that adjacent unknown-entry, GSM truncation,
  timestamp anomaly, generic client-action, GRE GameState, diagnostics, golden
  replay, feature-equity, and evidence-ledger surfaces are non-claims for
  missing-message-type support.
- Existing coverage statuses for adjacent families must not be changed.
- Corpus parity summary counts may change only as the direct result of moving
  one family from `missing` to `covered_report_only`.
- No parser behavior or protected downstream behavior may change.

## Unknowns

- Which MTGA log payload families can actually omit, corrupt, or rename a
  message type field in live logs.
- Whether a future safe synthetic fixture should model missing GRE message
  type, missing client-action type, missing top-level API marker, or a smaller
  subset.
- Whether the correct future behavior should be unknown-entry routing, a
  dedicated drift signal, diagnostics-only evidence, parser event emission, or
  no behavior change.
- Which future fixture shape would be privacy-safe and representative without
  importing external or private raw logs.

## Suspected Gaps

- Current corpus parity has no dedicated Mythic Edge entry for
  `drift_debug.missing_message_type`.
- Current parser code has adjacent fallback/default behavior but no dedicated
  missing-message-type support claim.
- Current unknown-entry, GSM truncation, timestamp-anomaly, and generic
  client-action coverage could be overread unless this boundary is explicit.

## Validation Obligations

Codex C must run, at minimum:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_missing_message_type_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_missing_message_type_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C may add focused corpus parity tests only when needed to enforce:

- `drift_debug.missing_message_type` is `covered_report_only`.
- `coverage_basis` is exactly `["fixture_metadata_only"]`.
- `parser_event_families` is empty.
- The session-ledger entry has zero parser-event, raw-log, fixture, recovery,
  reconstruction, and unknown future message support claims.
- Adjacent family statuses remain unchanged.

Codex C must produce:

- `docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md`

## Stop Conditions

- Do not target main directly.
- Do not close issue #414.
- Do not close tracker #158.
- Do not open a PR unless separately asked.
- Do not claim full Mythic Edge corpus parity.
- Do not claim missing-message-type parser support.
- Do not claim support from corpus metadata alone.
- Do not import, copy, mirror, or commit Manasight raw logs or external corpus
  contents.
- Do not commit private Player.log excerpts, private local logs, private smoke
  outputs, generated data, SQLite files, runtime artifacts, workbook exports,
  credentials, tokens, API keys, webhook URLs, decklists, strategy notes, or
  private reports.
- Do not change parser behavior, parser state final reconciliation, parser
  event classes, router semantics, GRE parsing, client-action parsing,
  diagnostics, golden replay, feature-equity, evidence-ledger, analytics,
  workbook, webhook, Apps Script, AI, coaching, production, CI, merge, or
  deploy surfaces without a new explicit contract.

## Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #414.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/414

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_missing_message_type_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change for
  `drift_debug.missing_message_type` according to the contract. The selected
  path is report-only boundary coverage, not parser support and not synthetic
  malformed-payload support.

  Required scope:
  - Update only the corpus manifest/session ledger and focused corpus parity
    tests needed for the contract.
  - Add docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md.
  - Add docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md.
  - Keep `drift_debug.missing_message_type` as `covered_report_only`.
  - Keep `coverage_basis` exactly `["fixture_metadata_only"]`.
  - Keep `parser_event_families` empty.
  - Explicitly preserve non-claims for unknown-entry, GSM truncation,
    timestamp anomaly, generic client-action fallback, GRE GameState parsing,
    diagnostics, golden replay, feature-equity, and evidence-ledger surfaces.
  - Do not change adjacent scenario-family statuses except for summary counts
    caused by this one coverage move.

  Do not:
  - Implement parser behavior.
  - Change router, GRE parser, client-action parser, diagnostics, golden
    replay, feature-equity, evidence-ledger, analytics, workbook, webhook,
    Apps Script, AI/coaching, production, CI, merge, or deploy behavior.
  - Add raw log fixtures, private artifacts, external corpus contents, or
    malformed-payload parser fixtures.
  - Claim missing-message-type parser support, message recovery, GameState
    reconstruction, unknown future MTGA message support, release readiness,
    production readiness, AI truth, analytics truth, or full corpus parity.
  - Target main directly.
  - Close issue #414 or tracker #158.
  - Stage or commit unless explicitly asked.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - printf '%s\n' docs/contracts/parser_corpus_missing_message_type_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
  - printf '%s\n' docs/contracts/parser_corpus_missing_message_type_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests tools
  - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/412"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/413"
  previous_merge_commit: "b082f8e11124c0824436a9fad6885af5821816d8"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_missing_message_type_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-missing-message-type-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/414"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/412"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/413"
  previous_merge_commit: "b082f8e11124c0824436a9fad6885af5821816d8"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_missing_message_type_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_missing_message_type_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_missing_message_type_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-missing-message-type-coverage"
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
    - "Do not close issue #414."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim missing-message-type parser support, parser message recovery, GameState reconstruction, unknown future MTGA message support, release readiness, production readiness, AI truth, analytics truth, or coaching truth."
    - "Do not import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, private smoke outputs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, strategy notes, or private reports."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, GRE parsing, client-action parsing, diagnostics, golden replay, feature-equity, evidence-ledger, analytics, workbook, webhook, Apps Script, AI, coaching, production, CI, merge, or deploy surfaces without a new explicit contract."
```
