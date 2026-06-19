# Parser Corpus Gameplay Conjure External Boundary Contract

## Module

Parser corpus parity coverage boundary for `gameplay_stress.conjure`.

Plain English: this contract keeps the Conjure gameplay-stress corpus family
blocked until Mythic Edge has owned, privacy-safe evidence for a dedicated
Conjure boundary. Existing gameplay-action, card-identity,
opponent-card-observation, evidence-ledger, diagnostics, drift, golden replay,
feature-equity, analytics, or corpus metadata surfaces are useful context, but
they are not proof of Conjure parser support or generated-card truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/450
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/448
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/449
- Previous merge commit: `9bada01874b37d58550939f5e6c6d1ba66dc53d0`
- Base branch inspected: `main`
- Contract branch: `codex/parser-corpus-gameplay-conjure-boundary-450`
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

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
- `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`
- `docs/contracts/parser_corpus_phantom_deck_origin_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/golden_replay.py`

## Purpose

Define the safest corpus/provenance boundary for
`gameplay_stress.conjure`, which remains blocked by external-reference
metadata.

This is corpus parity boundary work, not parser behavior work. The contract
does not authorize parser changes, gameplay-action changes, card-identity
changes, opponent-card-observation changes, manifest promotion, session-ledger
changes, private evidence collection, live MTGA checks, Alchemy/Conjure checks,
or readiness claims.

## Observed Current Behavior

Observed on `main` at
`9bada01874b37d58550939f5e6c6d1ba66dc53d0`:

- Issue #450 is open.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- Issue #448 is closed after PR #449 merged the inactivity-timeout boundary
  contract into `main`.
- The corpus parity CLI reports:
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- Current report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 19
  - `partial`: 0
  - `missing`: 0
  - `deferred`: 0
  - `blocked_private_evidence`: 2
  - `blocked_external_boundary`: 4
  - `not_applicable`: 0
- `gameplay_stress.conjure` is represented only by
  `external_reference_category_boundary`.
- `gameplay_stress.conjure` currently has:
  - `coverage_status`: `blocked_external_boundary`
  - `coverage_basis`: `["external_reference_only"]`
  - `mythic_edge_entries`: `["external_reference_category_boundary"]`
  - `parser_event_families`: `[]`
- `external_reference_category_boundary` also covers:
  - `timer.inactivity_timeout`
  - `gameplay_stress.spellbook`
  - `drift_debug.recycle_or_rollback`
- `gameplay_stress.action_attribution` is already
  `covered_report_only`, with explicit non-claims around causal action truth,
  hidden actions, hidden cards, opponent intent, player mistakes, best-line
  truth, archetypes, decklists, gameplay advice, analytics truth, AI truth,
  coaching truth, release readiness, and production behavior.
- `gameplay_stress.event_ordering` is already `covered_report_only`, with
  explicit non-claims around complete event-sequence truth, causal ordering,
  hidden actions, hidden cards, opponent intent, player mistakes, best-line
  truth, analytics truth, AI truth, coaching truth, release readiness, and
  production behavior.
- Tier 5 card identity, gameplay-action, and opponent-card-observation
  evidence-ledger contracts explain parser-owned provenance surfaces, but they
  keep hidden-card inference, complete decklists, sideboard deltas,
  archetypes, gameplay advice, model-provider truth, and AI truth out of parser
  truth.
- `src/mythic_edge_parser/app/gameplay_actions.py` observes `GameState`
  events and can produce parser-owned gameplay action entries from zones,
  objects, actions, annotations, replacement context, prior object state, turn
  tracking, seat mapping, and card/catalog enrichment.
- `src/mythic_edge_parser/app/opponent_card_observations.py` can derive
  visible opponent-card observations from gameplay action entries while
  suppressing hidden library-to-hand draws without reveal or public-zone
  evidence.
- Current code and tests do not define a dedicated Conjure parser event,
  Conjure detector, generated-card provenance entry, Conjure fixture, Conjure
  corpus session, spellbook/conjure paired boundary, private smoke proof, or
  production parser support claim for this scenario family.

## Scope Decision

Selected path: remain `blocked_external_boundary`.

Codex B considered these paths:

1. Move `gameplay_stress.conjure` to `covered_report_only`.
2. Add synthetic or committed fixture coverage.
3. Define a future evidence-generation prerequisite and keep the row blocked.
4. Leave the broad external-reference row without a sharper contract.

This contract selects path 3.

Reasoning:

- Public external taxonomy can name Conjure as a gameplay stress category, but
  external category naming is not Mythic Edge evidence.
- Mythic Edge has adjacent gameplay-action, event-ordering, card-identity, and
  opponent-card-observation provenance surfaces, but those surfaces do not
  prove Conjure-specific generated-card behavior.
- Generic card identity provenance can explain `grpId` support and uncertainty
  for observed objects, but it does not prove a card was conjured, where the
  generated card came from, whether the generated object was visible, or what
  hidden options existed.
- Opponent-card observations intentionally suppress or degrade hidden
  information; they must not become hidden-card, generated-card, or complete
  decklist truth for Conjure.
- A report-only status would risk suggesting that the adjacent surfaces have
  been mapped closely enough to account for Conjure. They have not.
- A synthetic fixture path might be possible later, but it needs a dedicated
  reduced expected-facts model that defines allowed observable Conjure signals
  without reconstructing hidden cards, complete decklists, spellbook options,
  or strategy.
- A private/sanitized evidence path might also be possible later, but it needs
  explicit approval, local-only handling, redaction, retention, and public
  summary constraints.

This decision does not authorize source-code changes, manifest status changes,
session-ledger changes, focused test changes, private/live execution, or
status promotion for this row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns the corpus coverage boundary for
`gameplay_stress.conjure`. Parser modules own event interpretation,
gameplay-action extraction, card identity, opponent-card observations, parser
events, router behavior, match/game identity, and parser state behavior.
Corpus parity artifacts own only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance, with Quality / Governance support for contract,
validation, review, and protected-surface checks.

This slice consumes Parser behavior evidence and evidence-ledger context for
review, but it is not a Parser behavior module, gameplay-action module,
card-identity module, opponent-card-observation module, generated-card module,
hidden-information module, diagnostics module, drift-report module, golden
replay module, feature-equity module, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, readiness gate, or production module.

## Truth Owner

Truth owner for current corpus coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for parser and adjacent provenance behavior referenced only as
non-claim context:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`

Truth boundary:

- Gameplay-action extraction may say which parser-owned action facts were
  observed or derived from existing `GameState` evidence.
- Card identity provenance may explain identifier support and uncertainty for
  observed card/object identity fields.
- Opponent-card observation provenance may explain visible opponent-card
  observations and hidden-information suppression/degradation.
- Corpus parity may say that Conjure remains blocked until a dedicated evidence
  model exists.
- No report consumer may treat these adjacent surfaces as Conjure support,
  generated-card truth, hidden-card truth, spellbook support, complete-decklist
  truth, archetype truth, gameplay advice, analytics truth, AI truth, coaching
  truth, release readiness, production behavior, or full corpus parity.

## Bridge-Code Status

Bridge-code status: deferred future boundary.

No bridge code is authorized in this contract. Codex C is not required for a
metadata implementation because the selected row stays blocked. If the team
wants a no-change verification package, Codex C must produce docs-only
comparison/report artifacts and leave corpus metadata, parser code, and tests
untouched.

## Files Owned By This Contract

This contract directly owns:

- `docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md`

Expected optional no-change verification artifacts:

- `docs/implementation_handoffs/parser_corpus_gameplay_conjure_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_gameplay_conjure_external_boundary.md`

This contract does not authorize edits to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- evidence-ledger implementation
- parser behavior
- parser events
- router behavior
- diagnostics, drift reports, golden replay, feature-equity behavior
- workbook/webhook/App Script, Google Sheets sync, output transport
- analytics, AI, coaching, CI, readiness, deploy, final integration, or
  production surfaces

## Public Interface

This contract defines no new runtime public API.

The current report-facing interface remains the corpus parity matrix row for
`gameplay_stress.conjure`:

```yaml
scenario_family: "gameplay_stress.conjure"
coverage_status: "blocked_external_boundary"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries:
  - "external_reference_category_boundary"
external_reference_status: "reference_category_not_checked"
```

No new manifest entry, session-ledger entry, parser event, gameplay event,
Conjure event, generated-card event, card-identity field, opponent-observation
field, diagnostics field, drift field, runtime status field, workbook row,
webhook payload field, Apps Script mapping, analytics view, or AI/coaching
field is authorized by this contract.

## Required Guarantees

### Status Boundary

`gameplay_stress.conjure` must remain:

```yaml
coverage_status: "blocked_external_boundary"
coverage_basis:
  - "external_reference_only"
```

No implementation may promote this row to `covered_report_only`,
`covered_synthetic`, `covered_committed`, `partial`, or
`blocked_private_evidence` without a later explicit contract.

### Adjacent Surface Boundaries

Current adjacent surfaces must not be reinterpreted:

- `gameplay_stress.action_attribution` stays limited to report-only boundary
  metadata.
- `gameplay_stress.event_ordering` stays limited to report-only boundary
  metadata.
- `gameplay_stress.spellbook` remains a later external-boundary candidate.
- Tier 5 `grp_id`, `gameplay_action`, and `opponent_card_observation`
  provenance remains provenance for already contracted parser-managed facts,
  not Conjure support.
- Generic card identity, zone movement, replacement-chain context, public-zone
  visibility, or opponent-card observations do not prove a Conjure mechanic.

### External Reference Boundary

The external-reference row may name `gameplay_stress.conjure`, but naming the
family does not prove:

- parser support;
- Conjure support;
- generated-card support;
- generated-card availability;
- generated-card identity;
- hidden-card truth;
- complete decklist truth;
- deck-origin truth;
- spellbook support;
- spellbook option truth;
- action causality;
- opponent intent;
- player mistake labels;
- gameplay advice;
- archetype truth;
- private smoke success;
- release readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- full corpus parity.

### Future Evidence Prerequisites

A future status-change contract must define at least one of these evidence
paths before promotion:

- a Mythic Edge-owned synthetic Conjure evidence model that proves only a
  reduced observable shape, without hidden-card inference or generated-card
  origin claims beyond the fixture;
- an approval-gated sanitized/private evidence execution packet with local-only
  collection, redaction, retention, review, and public-summary controls;
- a parser-evidence pipeline output after later evidence issues that defines an
  allowed non-private review artifact for Conjure-like generated-card evidence;
- a narrower prerequisite issue that first defines how Mythic Edge distinguishes
  generic replacement/zone/card-identity evidence from Conjure evidence.

Any future path must state exactly what is proved and what remains a non-claim.

### Protected Surface Guarantees

This contract must not change:

- parser behavior;
- gameplay-action extraction behavior;
- card identity behavior;
- opponent-card-observation behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics report shape;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status files;
- failed posts;
- workbook exports;
- analytics truth;
- AI truth;
- coaching behavior;
- OpenAI/model-provider behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

## Inputs

Allowed Codex B inputs:

- GitHub issue #450, tracker #158, parent issue #434, previous issue #448,
  and PR #449 metadata.
- Existing repo contracts, implementation handoffs, and contract-test reports.
- Existing corpus manifest and session ledger metadata.
- Existing corpus parity report code and focused tests.
- Existing card identity, gameplay-action, opponent-card-observation,
  evidence-ledger, diagnostics, golden replay, and feature-equity artifacts as
  reference context only.
- Existing public external taxonomy references already represented in Mythic
  Edge corpus parity artifacts.

Forbidden Codex B inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- Alchemy, Conjure, or Spellbook checks;
- firewall/drop/network/packet/OS/router checks;
- screenshots;
- exact private paths;
- raw hashes;
- runtime logs;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- decklists, card choices, private strategy notes, or private reports;
- generated hidden-card/decklist evidence;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source,
  or external corpus contents.

## Outputs

Allowed output for this contract:

- A Markdown contract file describing the blocked external-boundary decision.
- Optional future docs-only no-change comparison/report artifacts.
- A workflow handoff to Codex E by default, or an optional no-change Codex C
  route if the team explicitly requests verification artifacts.

Forbidden output:

- changed parser code;
- changed gameplay-action, card-identity, opponent-observation, evidence-ledger,
  diagnostics, drift, golden replay, feature-equity, analytics, AI, coaching,
  or production behavior;
- changed corpus manifest or session ledger;
- changed tests;
- raw or private evidence;
- generated data;
- runtime artifacts;
- private reports;
- readiness claims;
- status promotion for `gameplay_stress.conjure` or any blocked row.

## Unknowns

- Whether Arena exposes a stable, explicit Conjure evidence shape that Mythic
  Edge can represent without hidden-card inference.
- Whether an owned synthetic Conjure shape can be reduced enough to be honest
  without claiming broad generated-card support.
- Whether future sanitized/private evidence can safely summarize Conjure
  behavior without revealing raw logs, private paths, decklists, card choices,
  or strategic context.
- Whether future Conjure and Spellbook evidence should share a prerequisite
  generated-card boundary or remain separate child issues.
- Whether later parser-evidence pipeline issues #381 through #387 will create
  a safe non-private evidence source for this row.

## Suspected Gaps

- Current corpus metadata groups `gameplay_stress.conjure` under a broad
  external-reference row with unrelated external-boundary families.
- Current code and tests do not include a dedicated Conjure fixture, detector,
  parser event, or coverage entry.
- Existing gameplay-action and card-identity evidence can be mistaken for
  Conjure support unless the boundary remains explicit.
- The reduced expected-facts model for future Conjure coverage is undefined.
- Spellbook may require a separate option-generation boundary and must not be
  folded into this issue by implication.

## Invariants

- `gameplay_stress.conjure` remains `blocked_external_boundary`.
- `gameplay_stress.spellbook` remains a later external-boundary candidate.
- `timer.inactivity_timeout` remains governed by
  `docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md`.
- `drift_debug.recycle_or_rollback` remains governed by
  `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`.
- `connection.firewall_or_network_drop` and
  `mythic_edge.private_log_report_only_drift` remain private-evidence rows
  governed by their own contracts.
- External-reference metadata is not parser truth.
- Corpus parity reports are review metadata, not readiness, production,
  analytics, AI, coaching, or tracker-completion authority.

## Error Behavior

If validation observes `gameplay_stress.conjure` as anything other than
`blocked_external_boundary`, stop and route back to Codex B unless the status
change is explained by a later merged contract.

If validation observes `gameplay_stress.spellbook` as promoted by this issue,
stop and route back to Codex B.

If validation requires private/live data, stop and record the blocked
condition. Do not run private/live checks.

If any proposed implementation needs parser behavior, gameplay-action,
card-identity, opponent-observation, evidence-ledger, diagnostics, drift-report,
runtime status, workbook, webhook, Apps Script, analytics, AI, coaching, CI,
merge, deploy, production, or final integration changes, stop and create or
request a new scoped contract.

If any proposed implementation would import, copy, mirror, summarize, hash, or
commit private logs or external corpus contents, reject it and keep the row
blocked.

## Side Effects

This contract has no runtime side effects.

The only intended repository side effect is adding this contract file.

## Dependency Order

Current dependencies:

1. `docs/contracts/parser_corpus_parity_expansion.md`
2. `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
3. `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
4. `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
5. `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`
6. `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
7. `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
8. `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`

Potential future dependencies before promotion:

- parser-evidence pipeline issues #381 through #387;
- staged follow-up issues #451, #452, #453, #454, #455, and #456;
- an approval-gated private or sanitized evidence packet;
- a dedicated synthetic Conjure evidence contract;
- a narrower generated-card evidence prerequisite;
- a later contract defining an allowed sanitized fixture or report-only
  summary.

## Compatibility

This contract is compatible with the current corpus parity vocabulary because
it preserves the existing `blocked_external_boundary` status and existing
external-reference entry.

The contract deliberately avoids requiring new status vocabulary, new coverage
basis vocabulary, new parser events, new gameplay events, new generated-card
events, new runtime fields, new diagnostics fields, new workbook fields, or
new downstream consumer behavior.

## Tests Required

For this contract-only pass:

- Documentation-only checks are sufficient.
- No parser tests are required to pass before the contract exists.
- No private/live/Alchemy/Conjure/Spellbook checks are allowed.

For optional no-change Codex C verification:

- Run the corpus parity CLI and confirm `gameplay_stress.conjure` remains
  `blocked_external_boundary`.
- Run focused corpus parity tests that assert the matrix row.
- Inspect existing gameplay-action, card-identity, and
  opponent-card-observation tests only as reference evidence that adjacent
  surfaces remain bounded.
- Run protected-surface and secret/private-marker checks scoped to changed
  files.
- Produce a no-change implementation handoff and contract-test report.

Expected commands for optional verification:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_evidence_ledger.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

## Acceptance Criteria

- `docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md` exists.
- The contract selects `remain blocked_external_boundary`.
- The contract does not authorize manifest, session-ledger, parser, or test
  changes.
- The contract states that gameplay-action, card-identity,
  opponent-card-observation, evidence-ledger, diagnostics, drift, golden replay,
  feature-equity, analytics, and corpus metadata surfaces do not prove Conjure
  support.
- The contract preserves `gameplay_stress.spellbook` as a later external
  candidate.
- The contract defines future evidence prerequisites before any status change.
- The contract preserves protected surfaces and non-claims.
- The workflow handoff routes to Codex E by default, with optional no-change
  Codex C verification only if explicitly requested.

## Next Workflow Action

Recommended next role: Codex E: Module Reviewer, if the team wants an
independent contract-only review before submitter work.

Codex C is not required for a metadata implementation because this contract
does not authorize corpus status promotion, manifest edits, session-ledger
edits, parser edits, or focused test changes. If the team wants a no-change
verification package anyway, Codex C must produce docs-only comparison/report
artifacts and leave corpus metadata untouched.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #450.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/450

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/448

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/449

Previous merge commit:
9bada01874b37d58550939f5e6c6d1ba66dc53d0

Base branch:
main

Contract:
docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md

Goal:
Review the contract-only boundary for gameplay_stress.conjure. Verify that the selected status remains blocked_external_boundary, no Codex C metadata promotion is authorized by default, and adjacent gameplay-action, card-identity, opponent-observation, evidence-ledger, diagnostics, drift, replay, feature-equity, analytics, or corpus metadata is not overread as Conjure support.

Review:
- docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md
- docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md
- docs/contracts/parser_corpus_manasight_taxonomy_audit.md
- docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md
- docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py

Lead with findings. If no issues are found, say so and record residual risks.

Do not implement code. Do not target main directly. Do not close #158, #434, or #450. Do not run private Player.log, UTC_Log, app-data, live MTGA, Alchemy/conjure/spellbook, network, packet, OS/router, diagnostics, or private smoke checks. Do not read private logs. Do not promote gameplay_stress.conjure, gameplay_stress.spellbook, or any blocked row. Do not claim parser support, Conjure support, generated-card support, hidden-card truth, complete-decklist truth, archetype truth, gameplay advice, analytics truth, AI truth, coaching truth, readiness, production behavior, or full corpus parity.
```

Optional Codex C prompt, only if the team explicitly wants a no-change
verification package:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #450.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/450

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Contract:
docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md

Goal:
Produce a no-change docs verification package for the gameplay_stress.conjure external-boundary contract. Do not promote the row or edit corpus metadata.

Expected artifacts:
- docs/implementation_handoffs/parser_corpus_gameplay_conjure_external_boundary_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_conjure_external_boundary.md

Do:
- Verify main includes 9bada01874b37d58550939f5e6c6d1ba66dc53d0.
- Confirm gameplay_stress.conjure remains blocked_external_boundary.
- Confirm gameplay_stress.spellbook remains blocked_external_boundary.
- Confirm timer.inactivity_timeout remains blocked_external_boundary.
- Confirm drift_debug.recycle_or_rollback remains blocked_external_boundary.
- Confirm no private/live/Alchemy/Conjure/Spellbook checks are needed.
- Record validation and residual risks.

Do not:
- Implement code.
- Edit tests.
- Edit corpus manifest or session ledger.
- Promote gameplay_stress.conjure, gameplay_stress.spellbook, or any blocked row.
- Run private Player.log, app-data, live MTGA, Alchemy/conjure/spellbook, network, packet, OS/router, diagnostics, or private smoke checks.
- Read private logs.
- Claim parser support, Conjure support, generated-card support, hidden-card truth, complete-decklist truth, archetype truth, gameplay advice, analytics truth, AI truth, coaching truth, readiness, production behavior, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/450"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/448"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/449"
  previous_merge_commit: "9bada01874b37d58550939f5e6c6d1ba66dc53d0"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #450"
  target_artifact: "docs/contracts/parser_corpus_gameplay_conjure_external_boundary.md"
  optional_no_change_c_artifacts:
    - "docs/implementation_handoffs/parser_corpus_gameplay_conjure_external_boundary_comparison.md"
    - "docs/contract_test_reports/parser_corpus_gameplay_conjure_external_boundary.md"
  verdict: "gameplay_conjure_contract_preserves_blocked_external_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-conjure-boundary-450"
  base_branch: "main"
  selected_family: "gameplay_stress.conjure"
  status_decision: "remain_blocked_external_boundary"
  implementation_authorized: "no_metadata_promotion_by_default"
  tracker_status: "open"
  parent_issue_status: "open"
  later_external_candidates:
    - "gameplay_stress.spellbook"
  staged_after_387:
    - "#451"
    - "#452"
    - "#453"
    - "#454"
    - "#455"
    - "#456"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_evidence_ledger.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close parent issue #434 without explicit authorization."
    - "Do not run private Player.log, app-data, live MTGA, Alchemy/conjure/spellbook, network, packet, OS/router, diagnostics, or private smoke checks."
    - "Do not read private logs in Codex B/C/E."
    - "Do not promote gameplay_stress.conjure, gameplay_stress.spellbook, or any blocked row by default."
    - "Do not claim parser support, Conjure support, generated-card support, hidden-card truth, complete-decklist truth, archetype truth, gameplay advice, analytics truth, AI truth, coaching truth, readiness, production behavior, or full corpus parity."
```
