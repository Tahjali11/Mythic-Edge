# Parser Corpus Missing Message Type Behavior Uplift Contract

## Module

`drift_debug.missing_message_type` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records missing-message-type coverage as
report-only boundary metadata from issue #414. This contract defines the
narrowest safe path for moving the row toward parser-behavior readiness:
reduced synthetic missing/blank type fallback and default-preservation evidence
only. The uplift may prove that existing parser behavior handles selected
owned malformed payloads without losing raw evidence. It must not claim parser
message recovery, hidden payload truth, GameState reconstruction, unknown
future MTGA message support, generic unknown-entry support, parser resilience
truth, live drift health, release readiness, production behavior, analytics
truth, AI truth, coaching truth, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/500
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/498
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/499
- Previous merge commit: `b3d8dfc1527bfef7d0828d41c7fce6128a745883`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/414
- Adjacent family: `log_runtime.unknown_entry`
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-missing-message-type-behavior-uplift-500`
- Risk tier: High
- Status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
- `docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- relevant diagnostics, unknown-entry, GRE, client-action, golden replay, and
  drift tests as reference only

## Purpose

Define the minimum safe evidence model for moving
`drift_debug.missing_message_type` beyond the #414 report-only boundary.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic malformed/missing-message-type behavior is
  sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- how `log_runtime.unknown_entry` remains adjacent context only; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim support beyond the
reduced missing/blank type fallback and default-preservation packet.

## Observed Current Behavior

Observed on `main` at
`b3d8dfc1527bfef7d0828d41c7fce6128a745883`:

- Issue #500 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #498 is complete after PR #499.
- The corpus parity report state recorded by issue #500 is:

```text
45 families; committed=6, synthetic=19, report_only=14,
blocked_private=2, blocked_external=4, missing=0,
parser_behavior_ready=false,
pipeline_activation_ready_for_issue_388=false
```

Current `drift_debug.missing_message_type` row:

```yaml
scenario_family: "drift_debug.missing_message_type"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "missing_message_type_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "missing_message_type_boundary_report"
  - "unknown_entry_not_missing_message_type_truth"
  - "gsm_truncation_not_type_field_failure_truth"
  - "timestamp_anomaly_not_message_type_truth"
  - "generic_client_action_not_drift_debug_support"
  - "gre_game_state_message_type_not_recovery_truth"
  - "message_recovery_non_claim"
```

Current adjacent behavior:

- `log_runtime.unknown_entry` is `covered_report_only` with drift,
  diagnostics, and evidence-ledger review metadata. It is not parser-understood
  event truth.
- `client_actions.py` emits `generic_client_action` for an inner GRE client
  payload whose `type` is missing, blank, whitespace, or `None`, provided the
  inner payload itself is a dict.
- The generic client-action payload normalizes missing or blank inner message
  type to `message_type == ""` and preserves `raw_client_action`.
- `game_state.py` builds a `GameStateEvent` payload whose `message_type`
  defaults to `"GREMessageType_GameStateMessage"` when the selected GRE
  message dictionary has no top-level `type`.
- GRE dispatch can emit `GameStateEvent` when the selected
  `gameStateMessage` or `queuedGameStateMessage.gameStateMessage` is a dict.
- Existing tests already exercise generic client-action fallback for missing
  or blank type values and helper-level GameState payload defaults.

Current non-evidence:

- The #414 boundary explicitly says unknown-entry drift reporting, GSM
  truncation coverage, timestamp-anomaly coverage, generic client-action
  fallback, GRE GameState parsing, diagnostics, golden replay,
  feature-equity, evidence-ledger provenance, analytics ingest, and public
  taxonomy metadata are not missing-message-type support by themselves.
- `log_runtime.unknown_entry` does not prove missing-message-type recovery or
  parser-understood unknown semantic content.
- The current GRE GameState default is a parser default for a parseable
  GameState shape, not message recovery or GameState reconstruction.
- The current generic client-action fallback is a fallback event for a dict
  payload, not unknown future MTGA message support.
- `gameplay_stress.event_ordering` is separate and must not be reinterpreted
  beyond #498.

## Scope Decision

Recommended future path: reduced synthetic missing-message-type behavior
uplift.

A later Codex C implementation may move
`drift_debug.missing_message_type` from `covered_report_only` toward
`covered_synthetic` with `parser_behavior_verified` only if it adds
Mythic Edge-owned synthetic evidence proving a reduced two-leg packet through
existing parser behavior:

1. Client-action missing/blank inner `type` fallback.
2. GRE GameState missing top-level `type` default preservation.

The reduced packet must prove parser-owned preservation of:

- a synthetic GRE client-action payload whose inner payload is a dict but whose
  inner `type` is missing, blank, whitespace, or `None`;
- emitted `ClientActionEvent` payload shape `type == "generic_client_action"`;
- normalized generic client-action `message_type == ""`;
- raw client-action envelope preservation;
- a synthetic GRE GameState message with a parseable `gameStateMessage` and no
  top-level `type` in the JSON message object;
- emitted `GameStateEvent` payload shape `type == "game_state_message"`;
- default-preserved `message_type == "GREMessageType_GameStateMessage"`;
- raw GameState message preservation; and
- explicit non-claims that the packet does not recover or reconstruct a
  missing message type.

The behavior claim is intentionally small:

- fallback/default preservation for selected synthetic payloads;
- existing parser behavior, not new parser interpretation;
- raw evidence preservation, not hidden payload truth;
- parseable input shapes only, not unknown entries or malformed JSON recovery;
- parser test evidence, not live Player.log drift health.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize parser behavior changes. If Codex C cannot prove the reduced packet
using existing behavior, the row must remain `covered_report_only` and route
back to Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- `client_actions.py` owns current client-action marker recognition, payload
  extraction, generic fallback, `message_type` normalization, and raw envelope
  preservation.
- `gre/__init__.py` owns current GRE dispatch and event emission.
- `game_state.py` owns current GameState payload construction and
  `message_type` defaulting.
- Router and diagnostics own unknown-entry accounting and review surfaces, not
  missing-message-type truth.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, unknown-entry
reports, diagnostics, drift reports, workbook formulas, dashboards, Apps
Script, webhook transport, analytics, AI, coaching, readiness, deploy,
production, or tracker lifecycle surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the existing producer of client-action and GameState events.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private-evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for future reduced synthetic behavior evidence:

- `tests/test_client_actions_parser.py`;
- `tests/test_gre_game_state_parser.py` or another focused GRE parser test if
  Codex C selects a dispatch-level route;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- the future Codex C implementation handoff; and
- the future Codex E contract-test report.

Truth boundary:

- A synthetic client-action test may prove only that existing generic fallback
  emits a `ClientActionEvent` with empty `message_type` and raw envelope
  preservation for selected missing/blank inner `type` values.
- A synthetic GRE GameState test may prove only that existing GameState
  parsing/defaulting emits a `GameStateEvent` with default
  `"GREMessageType_GameStateMessage"` for a parseable selected GameState shape
  missing a top-level message `type`.
- Corpus parity may claim `parser_behavior_verified` only for the reduced
  packet described above.
- Corpus parity must not claim parser message recovery, hidden payload truth,
  GameState reconstruction, unknown future MTGA message support, generic
  unknown-entry support, parser resilience truth, live private Player.log drift
  health, analytics truth, AI truth, coaching truth, release readiness,
  production behavior, #388/#381 activation, tracker completion, or full
  corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic missing/blank type parser tests
  -> existing client_actions.py and GRE GameState behavior
  -> focused test assertions
  -> corpus manifest/session-ledger behavior metadata
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from parser output.
- Corpus metadata must not turn unknown entries, GSM truncation markers,
  timestamp anomalies, generic client-action fallback, GRE defaults,
  diagnostics, drift reports, golden replay, feature-equity, evidence-ledger
  provenance, analytics ingest, public taxonomy labels, private malformed
  payloads, or local runtime artifacts into broad missing-message-type support.
- Corpus metadata must not move hidden payload inference, GameState
  reconstruction, future-message interpretation, analytics, AI, coaching,
  workbook, webhook, or Apps Script interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior;
- router behavior;
- GRE parser behavior;
- client-action parser behavior;
- parser event classes;
- parser state final reconciliation;
- match/game identity;
- deduplication;
- diagnostics behavior;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- analytics ingest behavior;
- runtime status files or schema;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- failed posts;
- workbook exports;
- SQLite/local app behavior;
- analytics truth;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- `tests/test_client_actions_parser.py`, for a dedicated missing/blank
  client-action inner type fallback test if existing assertions are not enough;
- `tests/test_gre_game_state_parser.py`, for a dedicated GRE missing top-level
  message type default-preservation test if existing assertions are not
  enough;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- `docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md`;
- `docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md`.

Files Codex C may inspect but must not change unless the implementation
contract is looped back:

- `src/mythic_edge_parser/router.py`;
- `src/mythic_edge_parser/parsers/gre/__init__.py`;
- `src/mythic_edge_parser/parsers/gre/game_state.py`;
- `src/mythic_edge_parser/parsers/client_actions.py`;
- `src/mythic_edge_parser/app/parser_diagnostics.py`;
- `src/mythic_edge_parser/app/log_drift_sensor.py`;
- `src/mythic_edge_parser/app/golden_replay.py`;
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`;
- `src/mythic_edge_parser/app/evidence_ledger.py`;
- adjacent contracts, handoffs, and reports.

Not owned by this contract:

- parser semantics;
- router semantics;
- GRE or GameState parser behavior;
- client-action parser behavior;
- unknown-entry routing behavior;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic tests and corpus metadata that make
the corpus parity public report show `drift_debug.missing_message_type` as a
reduced synthetic behavior-ready row. The intended eventual corpus row shape
is:

```yaml
scenario_family: "drift_debug.missing_message_type"
coverage_status: "covered_synthetic"
coverage_basis:
  - "parser_behavior_verified"
  - "fixture_metadata_only"
```

The existing report-only entry `missing_message_type_boundary_report_v1`
should remain as historical non-claim metadata unless Codex C has a strong
reason to route back for a replacement or migration contract. A new synthetic
evidence entry should be added rather than rewriting #414's boundary entry into
a behavior claim.

Recommended new manifest entry id:

```text
missing_message_type_synthetic_fallback_defaults_v1
```

Recommended new session id:

```text
missing_message_type_synthetic_fallback_defaults_v1
```

Recommended manifest claim families:

```yaml
parser_claim_families:
  - "synthetic_missing_message_type_fallback_defaults"
  - "client_action_missing_type_generic_fallback"
  - "client_action_blank_type_generic_fallback"
  - "gre_game_state_missing_type_default_preservation"
  - "raw_payload_preservation"
  - "missing_message_type_synthetic_boundary"
  - "message_recovery_non_claim"
  - "game_state_reconstruction_non_claim"
  - "unknown_future_message_support_non_claim"
  - "unknown_entry_support_non_claim"
```

Recommended manifest paths, adjusted only if Codex C selects a different
focused test route:

```yaml
paths:
  client_actions_test: "tests/test_client_actions_parser.py"
  gre_game_state_test: "tests/test_gre_game_state_parser.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
```

Recommended `parser_event_families`:

```yaml
parser_event_families:
  - "ClientAction"
  - "GameState"
```

## Minimum Parser-Owned Evidence

Future uplift requires dedicated reduced assertions. Codex C must not rely on
#414 report-only metadata or `log_runtime.unknown_entry` evidence alone.

### Client-Action Leg

Required:

- at least one synthetic GRE client-action envelope with an inner dict payload
  missing `type`;
- at least one synthetic GRE client-action envelope with an inner dict payload
  whose `type` is blank, whitespace, or `None`;
- emitted `ClientActionEvent`;
- emitted payload `type == "generic_client_action"`;
- emitted `message_type == ""`;
- preserved `raw_client_action`;
- no private logs, external corpus contents, malformed JSON recovery, or live
  checks.

Allowed:

- existing focused test coverage may be cited if it already proves these
  assertions and Codex C adds the corpus metadata/test wiring required by this
  contract;
- adding a dedicated test name or explicit row-related assertions is preferred
  if current tests are too generic for review.

Not sufficient:

- generic client-action fallback for a known future message type only;
- UI message parsing;
- specialized mulligan/select/submit-deck parsing;
- unknown-entry counts;
- drift report samples with no parser event assertion.

### GRE GameState Leg

Required:

- at least one synthetic GRE GameState input with a parseable selected
  `gameStateMessage`;
- no top-level `type` in the parsed message object;
- emitted `GameStateEvent` through public GRE parsing if feasible, or a clear
  route-back if only helper-level defaulting can be proven;
- emitted payload `type == "game_state_message"`;
- emitted `message_type == "GREMessageType_GameStateMessage"`;
- preserved `raw_game_state`;
- no GameState reconstruction from incomplete payloads.

Allowed:

- a log-prefix marker or other existing marker path may be used to make public
  GRE dispatch recognize the synthetic input while the JSON message object
  itself lacks a top-level `type`;
- helper-level `build_game_state_payload()` assertions may support the claim
  but should not be the only evidence unless Codex C explains why dispatch
  evidence is not feasible and routes back if needed.

Not sufficient:

- current GameState tests with present `type`;
- connect-response parsing;
- game-result parsing;
- GSM truncation evidence;
- malformed JSON routing;
- unknown-entry reporting.

### Required Non-Claims

Every manifest/session-ledger entry and implementation handoff must preserve
these non-claims:

- no parser message recovery;
- no hidden payload truth;
- no GameState reconstruction;
- no unknown future MTGA message support;
- no generic unknown-entry support;
- no parser resilience truth;
- no live private Player.log drift health;
- no diagnostics readiness;
- no analytics truth;
- no AI truth;
- no coaching truth;
- no private smoke success;
- no release readiness;
- no production behavior;
- no #388/#381 activation;
- no tracker completion;
- no full corpus parity.

## Behavior-Uplift Packet

This row's reusable packet is:

```yaml
scenario_family: "drift_debug.missing_message_type"
current_status: "covered_report_only"
current_basis:
  - "fixture_metadata_only"
target_status_if_successful: "covered_synthetic"
parser_behavior_verified_may_be_added: true
evidence_type: "synthetic"
fixture_or_test_route:
  preferred: "focused synthetic client-action and GRE GameState parser tests"
  optional: "small synthetic golden replay only if later contract requires it"
fixture_golden_replay_changes:
  allowed:
    - "dedicated synthetic test data if required"
  forbidden:
    - "private Player.log or external corpus contents"
    - "fixture that claims parser recovery or hidden payload truth"
manifest_session_ledger_changes:
  allowed:
    - "add missing_message_type_synthetic_fallback_defaults_v1"
    - "preserve missing_message_type_boundary_report_v1 as report-only history"
  forbidden:
    - "rewrite #414 boundary entry into behavior evidence"
    - "promote log_runtime.unknown_entry"
    - "promote unrelated rows"
parser_behavior_changes_allowed: false
private_external_inputs_forbidden: true
required_non_claims:
  - "parser_message_recovery"
  - "hidden_payload_truth"
  - "game_state_reconstruction"
  - "unknown_future_mtga_message_support"
  - "generic_unknown_entry_support"
  - "parser_resilience_truth"
  - "analytics_truth"
  - "ai_truth"
  - "coaching_truth"
  - "release_readiness"
  - "production_behavior"
focused_validation_commands:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_game_state_parser.py tests/test_corpus_parity_report.py"
  - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
stop_conditions_for_issue_388_381_activation:
  - "do not activate #388/#381"
  - "do not mark pipeline_activation_ready_for_issue_388 true"
  - "do not close tracker #158"
```

This packet is a pattern note for future behavior-uplift rows, but this
contract applies it only to `drift_debug.missing_message_type`.

## Compatibility Expectations

- Existing #414 report-only boundary must remain readable and testable.
- Existing `log_runtime.unknown_entry` coverage must remain scoped to
  unknown-entry drift/diagnostics review metadata.
- Existing #498 event-ordering behavior uplift must not be reinterpreted as
  missing-message-type evidence.
- Readiness metrics may count this row as parser-behavior-ready only after the
  family's winning status is `covered_synthetic` and its coverage basis
  includes `parser_behavior_verified`.
- `pipeline_activation_ready_for_issue_388` must remain false unless every
  separately required readiness gate is satisfied by later contracts.
- Public reports must continue to sanitize private paths, raw logs, secrets,
  runtime artifacts, failed posts, workbook exports, private reports, and
  external corpus contents.

## Validation Obligations For Codex C

Codex C must produce:

- a comparison handoff at
  `docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md`;
- a contract-test report at
  `docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md`;
- focused test evidence for the reduced missing-message-type packet;
- corpus metadata tests proving the intended manifest and session-ledger
  changes;
- explicit evidence that `log_runtime.unknown_entry` is not reinterpreted
  beyond its report-only boundary;
- explicit evidence that #498 event-ordering is unchanged; and
- clean git status with no private/generated artifacts.

Minimum validation commands:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_game_state_parser.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex C may add focused router, diagnostics, drift, golden replay, or
evidence-ledger tests only if its implementation touches those surfaces. Any
such expansion must be explained in the handoff.

## Acceptance Criteria

Future implementation is acceptable only if:

- `drift_debug.missing_message_type` has a new synthetic behavior entry;
- the row's winning status becomes `covered_synthetic` only with
  `parser_behavior_verified`;
- both the client-action leg and the GRE GameState leg have focused test
  evidence or a contract loopback explains why one leg is infeasible;
- the old report-only boundary entry remains report-only or is migrated only
  through an explicit contract loopback;
- all required non-claims are present in metadata, handoff, and report;
- `log_runtime.unknown_entry` remains report-only and is not reinterpreted as
  missing-message-type support;
- #498 event-ordering remains unchanged;
- #388/#381 remain inactive; and
- no protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  surfaces are changed.

Route back to Codex B or Codex A if:

- existing behavior cannot prove the reduced packet without parser code
  changes;
- the only available evidence is unknown-entry drift reporting;
- a fixture would require private or external raw logs;
- the implementation would need to claim parser message recovery, hidden
  payload truth, GameState reconstruction, or unknown future message support;
  or
- validation changes would touch protected surfaces.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should implement metadata/test/docs only. It should not implement
parser behavior changes.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #500.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/500

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/498

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/499

Previous merge commit:
b3d8dfc1527bfef7d0828d41c7fce6128a745883

Base branch:
main

Contract:
docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md

Goal:
Implement the smallest metadata/test/docs change needed to satisfy the
missing-message-type behavior uplift contract for
`drift_debug.missing_message_type`.

Required implementation boundary:
- Add a dedicated reduced synthetic missing-message-type behavior packet.
- Prove the client-action leg: missing/blank inner `type` emits
  `generic_client_action` with `message_type == ""` and preserves
  `raw_client_action`.
- Prove the GRE GameState leg: a parseable GameState message missing top-level
  `type` emits or builds a `GameStateEvent` payload with default
  `message_type == "GREMessageType_GameStateMessage"` and preserves
  `raw_game_state`.
- Add or update corpus manifest/session-ledger metadata so the row may move
  from `covered_report_only` to `covered_synthetic` only with
  `parser_behavior_verified`.
- Preserve `missing_message_type_boundary_report_v1` as report-only historical
  boundary metadata unless you route back for a contract loopback.
- Do not use `log_runtime.unknown_entry` evidence alone as
  missing-message-type support.
- Do not change parser behavior.

Expected files:
- tests/test_client_actions_parser.py
- tests/test_gre_game_state_parser.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md

Do not:
- Activate #388 / #381.
- Close #158, #388, #434, or #500.
- Promote blocked or unrelated report-only rows.
- Change parser behavior, router behavior, GRE parser behavior,
  client-action parser behavior, parser event classes, diagnostics behavior,
  drift behavior, golden replay behavior, feature-equity behavior,
  evidence-ledger behavior, analytics behavior, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  CI gates, merge readiness, deploy readiness, production behavior, or final
  integration policy.
- Run private Player.log, UTC_Log, live MTGA, malformed-payload, network, or
  private smoke checks.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed
  corpus files, parser source, external corpus contents, private logs,
  generated/runtime artifacts, workbook exports, secrets, tokens, API keys,
  webhook URLs, decklists, card choices, screenshots, private strategy notes,
  private malformed payloads, or private reports.
- Claim parser message recovery, hidden payload truth, GameState
  reconstruction, unknown future MTGA message support, generic unknown-entry
  support, parser resilience truth, release readiness, production behavior,
  tracker completion, analytics truth, AI truth, coaching truth, or full
  corpus parity.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_game_state_parser.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- run path-scoped secret/protected-surface checks for changed files
- git diff --check

End with:
- files changed
- reduced missing-message-type evidence added
- validation run
- remaining risks/open questions
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/500"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/498"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/499"
  previous_merge_commit: "b3d8dfc1527bfef7d0828d41c7fce6128a745883"
  completed_thread: "B"
  next_thread: "C"
  base_branch: "main"
  selected_family: "drift_debug.missing_message_type"
  adjacent_family: "log_runtime.unknown_entry"
  prior_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  target_contract: "docs/contracts/parser_corpus_missing_message_type_behavior_uplift.md"
  expected_implementation_handoff: "docs/implementation_handoffs/parser_corpus_missing_message_type_behavior_uplift_comparison.md"
  expected_contract_test_report: "docs/contract_test_reports/parser_corpus_missing_message_type_behavior_uplift.md"
  verdict: "reduced_synthetic_missing_message_type_behavior_uplift_authorized"
  risk_tier: "High"
  stop_conditions:
    - "Do not activate #388 / #381."
    - "Do not close #158, #388, #434, or #500."
    - "Do not promote blocked or unrelated report-only rows."
    - "Do not claim missing-message-type support from unknown-entry evidence alone."
    - "Do not claim parser message recovery, hidden payload truth, GameState reconstruction, unknown future MTGA message support, generic unknown-entry support, parser resilience truth, analytics truth, AI truth, coaching truth, release readiness, production behavior, tracker completion, or full corpus parity."
    - "Do not change parser behavior, router behavior, GRE parser behavior, client-action parser behavior, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching truth, CI gates, deploy policy, production behavior, or final integration policy."
```
