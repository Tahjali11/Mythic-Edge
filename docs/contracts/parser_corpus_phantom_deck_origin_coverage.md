# Parser Corpus Phantom Deck Origin Coverage Contract

## Module

Phantom-card or deck-origin drift corpus evidence boundary for the parser
corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`drift_debug.phantom_or_deck_origin` as report-only boundary metadata. It does
not add parser support, committed log fixtures, synthetic phantom-card
fixtures, deck-origin truth, hidden-card truth, complete decklists, archetype
classification, phantom-card behavior proof, private smoke success, release
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating StartHook deck
snapshots, deck-summary boundaries, deck-upsert boundaries, submit-deck
provenance, broad deck-state boundary notes, card identity provenance,
gameplay actions, opponent-card observations, diagnostics, log-drift reports,
golden replay behavior, feature-equity behavior, evidence-ledger provenance,
corpus parity metadata, runtime active-deck surfaces, card catalog enrichment,
local decklist references, or public Manasight taxonomy metadata as
phantom-card support or deck-origin truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/418
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/416
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/417
- Previous merge commit:
  `b1821c21ff461081dc76b8d3f865a7e08655e155`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-phantom-deck-origin-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `b1821c21ff461081dc76b8d3f865a7e08655e155`
- target_artifact:
  `docs/contracts/parser_corpus_phantom_deck_origin_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md`
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
- `docs/contracts/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/contract_test_reports/parser_corpus_rename_rotation_collision_coverage.md`
- `docs/implementation_handoffs/parser_corpus_rename_rotation_collision_coverage_comparison.md`
- `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `docs/contracts/parser_corpus_unknown_entry_coverage.md`
- `docs/contracts/parser_corpus_timestamp_anomaly_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- relevant diagnostics, golden replay, feature-equity, deck/state,
  gameplay-action, and opponent-observation tests if inspected as adjacent
  context

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, IP/network traces, generated/private/runtime artifacts, workbook
  exports, SQLite files, credentials, tokens, API keys, webhook URLs,
  decklists, card choices, sideboard plans, private strategy notes, or private
  reports.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`b1821c21ff461081dc76b8d3f865a7e08655e155`:

- Issue #418 is open and tracker #158 remains open.
- Issue #416 is closed after PR #417 merged rename/rotation collision
  report-only boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current issue #418 report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 12
  - `partial`: 3
  - `missing`: 4
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `drift_debug.phantom_or_deck_origin` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- Remaining missing rows also include:
  - `mythic_edge.live_diagnostics`
  - `mythic_edge.private_log_report_only_drift`
  - `mythic_edge.analytics_readiness_labels`
- `drift_debug.rename_or_rotation_collision` is now `covered_report_only`.
- `drift_debug.recycle_or_rollback` remains `blocked_external_boundary`.
- Deck-adjacent corpus rows are already intentionally bounded:
  - `deck_api.start_hook_deck_snapshot` is `covered_synthetic` and does not
    prove private deck contents, exact deck identity, submitted-deck truth,
    sideboard-delta truth, collection ownership, archetype classification, or
    decklist completion.
  - `deck_api.deck_summary`, `deck_api.deck_upsert`, and
    `deck_api.store_pack_inbox_or_crafting` are `covered_report_only` boundary
    rows and do not prove broad deck API or deck-origin truth.
- The evidence-ledger deck-state boundary keeps broad `deck_state` deferred
  and refuses complete active decklist truth, exact deck identity, deck name,
  deck ID, sideboard deltas, hidden cards, card-name truth, archetypes,
  matchup plans, gameplay advice, and AI/model-provider truth.
- Tier 5 card identity, gameplay-action, and opponent-card-observation
  contracts describe parser-owned or derived evidence facets, but each keeps
  hidden-card inference, complete decklists, archetypes, sideboard deltas,
  advice, and AI/model truth out of parser truth.
- Runtime surfaces can track latest submitted-deck context, active-deck
  profiles, collection/deck matching, and missing-card summaries, but those are
  local operational/enrichment artifacts, not durable deck-origin truth.
- Current code and tests do not define a corpus-owned phantom-card fixture,
  deck-origin detector, phantom/deck-origin parser event, deck-origin evidence
  ledger field, private smoke proof, or production parser support claim for
  this scenario family.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic phantom/deck-origin coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, blocked-private-evidence, or
   blocked-external-boundary status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage for
`drift_debug.phantom_or_deck_origin` only.

Reasoning:

- Mythic Edge has many adjacent evidence surfaces for deck snapshots,
  submitted-deck cards, broad deck-state boundaries, card identity,
  gameplay-action identity, opponent-card observations, diagnostics, drift
  review, golden replay, feature-equity, and runtime active-deck enrichment.
- Those adjacent surfaces are intentionally not enough to claim
  phantom/deck-origin support. They do not prove phantom-card behavior, deck
  origin, hidden-card truth, complete decklists, exact deck identity, deck
  source, card ownership, archetypes, parser recovery, or private smoke
  success.
- A synthetic phantom/deck-origin fixture would need a later contract that
  defines a reduced expected-evidence model, allowed card-origin signals,
  fixture privacy rules, expected parser/review output, and exact non-claims.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic metadata or a safely redacted
  local review report.
- Leaving the row plain `missing` hides a useful inspected boundary: existing
  deck/card/runtime/provenance surfaces have been reviewed and explicitly do
  not count as this drift-debug family.

This decision records `drift_debug.phantom_or_deck_origin` as report-only
boundary metadata. It changes corpus parity metadata and tests only; it does
not change parser behavior, decklist behavior, runtime surface behavior,
evidence-ledger behavior, diagnostics, log-drift reports, golden replay,
feature-equity behavior, gameplay-action behavior, opponent-card-observation
behavior, analytics behavior, AI/coaching behavior, or production behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`drift_debug.phantom_or_deck_origin`. Parser modules own event interpretation.
Decklist, runtime deck, card identity, gameplay-action, opponent-card
observation, diagnostics, drift, golden replay, feature-equity, and evidence
ledger surfaces own only their already contracted observations and boundaries.
Corpus parity artifacts own only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence, deck/card/runtime context, and
Quality / Governance evidence for context, but it is not a Parser behavior
module, decklist module, deck-origin module, hidden-information module,
runtime module, diagnostics module, drift module, golden replay module,
feature-equity module, evidence-ledger module, analytics module, AI module,
coaching module, release-readiness module, or production module.

## Truth Owner

Truth owner for `drift_debug.phantom_or_deck_origin` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent behavior referenced only as non-claim context:

- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`

Truth boundary:

- StartHook deck snapshots may prove bounded StartHook collection/deck
  snapshot parser evidence only.
- Deck-summary, deck-upsert, and store/pack/inbox/crafting rows may prove
  report-only non-claim boundaries only.
- Submit-deck provenance may prove observed normalized submitted list content
  only inside its own contract.
- Runtime active-deck profiles and collection/deck matching may provide local
  operational/enrichment context only.
- Card identity, gameplay actions, and opponent-card observations may prove
  their own parser-owned or derived evidence facets only.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `drift_debug.phantom_or_deck_origin`.
- Corpus parity must not infer phantom-card behavior, deck origin, hidden-card
  truth, complete decklists, exact deck identity, collection ownership, card
  ownership, sideboard deltas, archetypes, player mistakes, gameplay advice,
  parser recovery, private smoke success, production behavior, analytics truth,
  AI truth, coaching truth, release readiness, or full corpus parity from
  those adjacent surfaces.

Coverage status is review metadata. It is not parser truth, deck-origin truth,
phantom-card truth, hidden-card truth, diagnostics truth, replay truth,
evidence-ledger truth, runtime truth, analytics truth, AI truth, coaching
truth, merge readiness, deploy readiness, public/private release readiness, or
tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing deck/card/runtime/evidence-ledger adjacent boundary docs and tests
  -> bounded committed report-only corpus manifest/session-ledger metadata
  -> corpus parity coverage row for drift_debug.phantom_or_deck_origin
```

Forbidden reverse flow:

- Corpus coverage status must not change parser, decklist, runtime surface,
  diagnostics, log-drift, golden replay, feature-equity, evidence-ledger,
  gameplay-action, opponent-card-observation, analytics, workbook, webhook,
  Apps Script, AI/coaching, or production behavior.
- Corpus metadata must not add phantom-card detection, deck-origin detection,
  hidden-card inference, decklist completion, archetype classification,
  gameplay advice, player-mistake labels, or AI/model-provider truth.
- Corpus metadata must not turn report-only boundary notes into parser support,
  synthetic fixture truth, private smoke proof, merge readiness, deploy
  readiness, or full parity.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- decklist parsing or local decklist persistence
- runtime surfaces and runtime artifact behavior
- evidence-ledger behavior
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- gameplay-action behavior
- opponent-card-observation behavior
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status files
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

- `docs/contracts/parser_corpus_phantom_deck_origin_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- relevant diagnostics, golden replay, feature-equity, deck/state,
  gameplay-action, and opponent-observation tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- decklist behavior changes
- runtime surface or runtime artifact changes
- evidence-ledger schema/vocabulary changes
- diagnostics report shape changes
- log-drift report shape changes
- golden replay behavior changes
- feature-equity behavior changes
- gameplay-action behavior changes
- opponent-card-observation behavior changes
- new phantom-card parser events
- new deck-origin parser events
- new committed raw log fixtures
- synthetic phantom/deck-origin support claims
- local live smoke execution
- Manasight corpus import
- private-log drift, live diagnostics, analytics-readiness, AI, coaching, CI,
  final integration, and production surfaces

## Public Interface

No new runtime public API is authorized.

Authorized corpus manifest row:

- `scenario_family`: `drift_debug.phantom_or_deck_origin`
- `coverage_status`: `covered_report_only`
- `coverage_basis`: `["fixture_metadata_only"]`
- `parser_event_families`: `[]`
- `entry_id`: `phantom_deck_origin_boundary_report_v1`
- `entry_type`: `session_ledger_entry`
- `source_kind`: `committed_count_only_report`
- `commit_status`: `committed`
- `privacy_class`: `committed_count_only`
- `sanitization_status`: `not_applicable_count_only`

Required parser claim families for the entry:

- `phantom_deck_origin_boundary_report`
- `start_hook_deck_snapshot_not_deck_origin_truth`
- `deck_summary_not_deck_origin_truth`
- `deck_upsert_not_deck_origin_truth`
- `submitted_deck_not_phantom_truth`
- `deck_state_boundary_not_deck_origin_truth`
- `card_identity_not_hidden_card_truth`
- `gameplay_action_not_deck_origin_truth`
- `opponent_observation_not_hidden_card_truth`
- `runtime_active_deck_not_parser_truth`
- `analytics_ai_coaching_non_claim`

Required note non-claims:

- phantom-card parser support
- deck-origin parser support
- hidden-card truth
- complete decklists
- exact deck identity
- card ownership
- collection ownership
- sideboard deltas
- archetype classification
- gameplay advice
- player mistake labels
- parser recovery
- private smoke success
- diagnostics readiness
- release readiness
- production behavior
- analytics truth
- AI truth
- coaching truth
- full Mythic Edge corpus parity

Authorized session-ledger entry:

- `session_id`: `phantom_deck_origin_boundary_report_v1`
- `authorized_by_contract`:
  `docs/contracts/parser_corpus_phantom_deck_origin_coverage.md`
- `scenario_families`: `["drift_debug.phantom_or_deck_origin"]`
- `format_family`: `drift_debug`
- `match_shape`: `phantom_deck_origin_boundary_report_only`
- `record_summary`: `committed_phantom_deck_origin_boundary_metadata_only`
- `game_rows_count`: `0`
- `result_shape`: `not_applicable`

Required `parser_coverage` facts:

- `event_families`: `{}`
- `unknown_entries`: `0`
- `truncation_count`: `0`
- `deck_snapshot_reference_entries`: `1`
- `deck_summary_reference_entries`: `1`
- `deck_upsert_reference_entries`: `1`
- `submitted_deck_reference_entries`: `1`
- `deck_state_boundary_reference_entries`: `1`
- `card_identity_reference_entries`: `1`
- `gameplay_action_reference_entries`: `1`
- `opponent_observation_reference_entries`: `1`
- `diagnostics_reference_entries`: `1`
- `evidence_ledger_reference_entries`: `1`
- `dedicated_phantom_deck_origin_fixtures`: `0`
- `phantom_card_detection_claims`: `0`
- `deck_origin_truth_claims`: `0`
- `hidden_card_inference_claims`: `0`
- `complete_decklist_claims`: `0`
- `archetype_classification_claims`: `0`
- `gameplay_advice_claims`: `0`
- `private_smoke_success_claims`: `0`

## Required Guarantees

- Only `drift_debug.phantom_or_deck_origin` may be changed by Codex C.
- The selected coverage status must be `covered_report_only`.
- The selected coverage basis must be exactly `["fixture_metadata_only"]`.
- The row must not list parser event families.
- The session-ledger entry must be committed metadata only and must not contain
  raw log lines, raw private payloads, raw external payloads, decklists, card
  choices, sideboard plans, hidden-card examples, generated data, runtime
  artifacts, SQLite files, workbook exports, credentials, tokens, API keys, or
  webhook URLs.
- The row must explicitly say that adjacent deck, card identity, diagnostics,
  drift, evidence-ledger, gameplay-action, opponent-observation, runtime,
  analytics, AI, and public taxonomy surfaces are non-claims for
  phantom/deck-origin support.
- Existing coverage statuses for adjacent families must not be changed:
  - `drift_debug.rename_or_rotation_collision`
  - `drift_debug.recycle_or_rollback`
  - `mythic_edge.private_log_report_only_drift`
  - deck API families
  - gameplay-action and opponent-observation families
- Corpus parity summary counts may change only as the direct result of moving
  one family from `missing` to `covered_report_only`.
- No parser behavior or protected downstream behavior may change.

## Unknowns

- Which live MTGA log shapes represent phantom-card or deck-origin drift.
- Whether a future safe synthetic fixture should model card identity mismatch,
  deck-source mismatch, object-source mismatch, catalog mismatch, submitted
  deck mismatch, or a smaller reduced boundary.
- Whether future support should belong to parser behavior, evidence-ledger
  review, diagnostics, golden replay, private smoke review, or a separate
  parser-resilience artifact.
- Which future fixture shape would be privacy-safe and representative without
  importing external or private raw logs.

## Suspected Gaps

- Current corpus parity has no dedicated Mythic Edge entry for
  `drift_debug.phantom_or_deck_origin`.
- Current deck/card/runtime/evidence surfaces are rich enough to tempt false
  conclusions, but none currently prove phantom-card behavior or deck-origin
  truth.
- Current private-log drift and analytics-readiness rows remain separate
  missing Mythic Edge-specific families.

## Validation Obligations

Codex C must run, at minimum:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_phantom_deck_origin_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_phantom_deck_origin_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Recommended if Codex C relies on adjacent deck/card/runtime/evidence context in
the implementation handoff:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_evidence_ledger.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
```

Codex C may add focused corpus parity tests only when needed to enforce:

- `drift_debug.phantom_or_deck_origin` is `covered_report_only`.
- `coverage_basis` is exactly `["fixture_metadata_only"]`.
- `parser_event_families` is empty.
- The session-ledger entry has zero parser-event, raw-log, phantom-card,
  deck-origin, hidden-card, complete-decklist, archetype, advice, private-smoke,
  and AI/coaching support claims.
- Adjacent family statuses remain unchanged.

Codex C must produce:

- `docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md`

## Stop Conditions

- Do not target main directly.
- Do not close issue #418.
- Do not close tracker #158.
- Do not mark tracker #158 complete.
- Do not open a PR unless separately asked.
- Do not claim full Mythic Edge corpus parity.
- Do not claim parser support from corpus metadata alone.
- Do not infer hidden cards, complete decklists, classify archetypes, prove
  deck origin, prove phantom-card behavior, provide gameplay advice, label
  player mistakes, or move analytics/AI/coaching truth into parser truth.
- Do not import, copy, mirror, or commit Manasight raw logs or external corpus
  contents.
- Do not commit private Player.log excerpts, private local logs, private smoke
  outputs, IP/network traces, generated/private/runtime artifacts, workbook
  exports, credentials, tokens, API keys, webhook URLs, decklists, card
  choices, private strategy notes, or private reports.
- Do not change parser behavior, parser state final reconciliation, parser
  event classes, router semantics, diagnostics report shape, drift report
  behavior, golden replay behavior, feature-equity behavior, evidence-ledger
  behavior, match/game identity, deduplication, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  runtime status files, delivery retry artifacts, workbook exports, analytics
  truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates,
  merge readiness, deploy readiness, production behavior, or final integration
  policy without a new explicit contract.

## Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #418.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/418

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_phantom_deck_origin_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change for
  `drift_debug.phantom_or_deck_origin` according to the contract. The selected
  path is report-only boundary coverage, not parser support, not deck-origin
  truth, not phantom-card support, and not synthetic phantom/deck-origin
  support.

  Required scope:
  - Update only the corpus manifest/session ledger and focused corpus parity
    tests needed for the contract.
  - Add docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md.
  - Add docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md.
  - Keep `drift_debug.phantom_or_deck_origin` as `covered_report_only`.
  - Keep `coverage_basis` exactly `["fixture_metadata_only"]`.
  - Keep `parser_event_families` empty.
  - Explicitly preserve non-claims for StartHook deck snapshots, deck-summary,
    deck-upsert, submitted-deck cards, broad deck-state boundary notes, card
    identity, gameplay actions, opponent-card observations, diagnostics,
    drift, evidence ledger, runtime active-deck surfaces, analytics, AI,
    coaching, and public taxonomy surfaces.
  - Do not change adjacent scenario-family statuses except for summary counts
    caused by this one coverage move.

  Do not:
  - Implement parser behavior.
  - Change decklist behavior, runtime surfaces, evidence ledger, diagnostics,
    log-drift reports, golden replay, feature-equity, gameplay actions,
    opponent-card observations, analytics, workbook, webhook, Apps Script,
    AI/coaching, production, CI, merge, or deploy behavior.
  - Add raw log fixtures, private artifacts, external corpus contents, decklist
    artifacts, private smoke outputs, or synthetic phantom/deck-origin
    parser/runtime fixtures.
  - Claim phantom-card support, deck-origin truth, hidden-card truth, complete
    decklists, exact deck identity, collection ownership, card ownership,
    sideboard deltas, archetype classification, gameplay advice, player
    mistake labels, parser recovery, private smoke success, release readiness,
    production readiness, analytics truth, AI truth, coaching truth, or full
    corpus parity.
  - Target main directly.
  - Close issue #418 or tracker #158.
  - Stage or commit unless explicitly asked.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - printf '%s\n' docs/contracts/parser_corpus_phantom_deck_origin_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
  - printf '%s\n' docs/contracts/parser_corpus_phantom_deck_origin_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests tools
  - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/417"
  previous_merge_commit: "b1821c21ff461081dc76b8d3f865a7e08655e155"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_phantom_deck_origin_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-phantom-deck-origin-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/418"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/416"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/417"
  previous_merge_commit: "b1821c21ff461081dc76b8d3f865a7e08655e155"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_phantom_deck_origin_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_phantom_deck_origin_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_phantom_deck_origin_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-phantom-deck-origin-coverage"
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
    - "Do not close issue #418."
    - "Do not close tracker #158 or mark it complete."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support, deck-origin truth, phantom-card truth, hidden-card truth, complete decklists, exact deck identity, collection ownership, card ownership, sideboard deltas, archetype classification, gameplay advice, player mistake labels, private smoke success, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
    - "Do not upgrade or reinterpret drift_debug.rename_or_rotation_collision, drift_debug.recycle_or_rollback, mythic_edge.private_log_report_only_drift, deck API families, gameplay-action families, opponent-observation families, runtime active-deck surfaces, analytics readiness, or live diagnostics without separate contract authority."
    - "Do not import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, private smoke outputs, IP/network traces, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, private strategy notes, or private reports."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, drift report behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, gameplay-action behavior, opponent-card-observation behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, delivery retry artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy without a new explicit contract."
```
