# Parser Corpus Deck Upsert Coverage Contract

## Module

Deck upsert corpus evidence boundary for the parser corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`deck_api.deck_upsert` as a report-only corpus boundary. It does not claim that
Mythic Edge has a dedicated deck-upsert parser, does not reuse
`deck_api.event_set_deck` as upsert support, and does not turn submit-deck
signals into broad deck API truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/396
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/395
- Previous merge commit:
  `3a128565b33ef512c8edcba13083449cb284b55b`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-deck-upsert-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `3a128565b33ef512c8edcba13083449cb284b55b`
- target_artifact:
  `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md`
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
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `tests/test_parsers.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, deck examples, or
  external corpus contents.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite or deferred status.

Selected path: report-only boundary coverage.

Reasoning:

- The repo has no dedicated parser, event family, or committed fixture that
  proves standalone `deck_api.deck_upsert` support.
- `deck_api.event_set_deck` is already `covered_committed` through
  `bo1_match_win_basic`, but the taxonomy audit explicitly treats deck upsert
  as a separate family that must not be overread from event-set evidence.
- `ClientMessageType_SubmitDeckResp` parser behavior and submitted-deck card
  provenance are real Mythic Edge evidence surfaces, but they are submit-deck
  signals and card-content evidence, not deck-upsert API support.
- A synthetic deck-upsert fixture would imply a parser behavior claim that the
  current parser does not own.
- Leaving the row as plain `missing` hides the useful boundary decision that
  Mythic Edge has inspected the family and intentionally refuses to conflate
  event-set deck, submit-deck, deck summary, or StartHook deck snapshot evidence
  with deck-upsert coverage.

This decision records `deck_api.deck_upsert` as a report-only corpus boundary.
It changes corpus parity metadata and tests only; it does not change parser
behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the `deck_api.deck_upsert`
scenario family. Parser modules own their existing event-set, StartHook,
client-action, and submitted-deck behavior. Runtime surfaces, analytics,
workbook outputs, and AI/coaching surfaces remain downstream consumers and
must not own this coverage claim.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence. It is not a Parser behavior module and is not a runtime,
workbook, webhook, Apps Script, Google Sheets, analytics, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `deck_api.deck_upsert` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Related parser truth owners that must not be reclassified by this contract:

- `src/mythic_edge_parser/parsers/client_actions.py` owns
  `ClientMessageType_SubmitDeckResp` normalization.
- `src/mythic_edge_parser/app/state.py` owns `submit_deck_seen` state updates.
- Existing golden replay and corpus fixtures own their existing event-set deck
  and submit-deck observations.
- Evidence-ledger contracts own submit-deck signal and submitted-deck
  card-content provenance boundaries.

Truth boundary:

- `deck_api.event_set_deck` remains its own corpus family.
- `deck_api.deck_summary` remains report-only boundary metadata from issue
  #394.
- `deck_api.start_hook_deck_snapshot` remains synthetic StartHook snapshot
  coverage from issue #392.
- `ClientAction.submit_deck_resp`, `submit_deck_seen`, and
  `submitted_deck_cards` remain parser/evidence-ledger surfaces. They do not
  prove deck-upsert behavior.
- This contract owns only the report-only deck-upsert boundary row: Mythic
  Edge has no current dedicated deck-upsert parser claim.
- Corpus coverage status is review metadata. It is not deck identity truth,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, match/game truth, inventory/economy truth, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, release
  readiness, production behavior, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing event-set, submit-deck, deck-summary, StartHook, taxonomy-audit docs
  -> bounded committed report-only manifest/session-ledger metadata
  -> corpus parity boundary row for deck_api.deck_upsert
```

Forbidden reverse flow:

- Corpus coverage status must not change client-action parser behavior.
- Corpus metadata must not create, imply, or require a dedicated deck-upsert
  parser.
- Corpus metadata must not rename or reclassify `deck_api.event_set_deck`,
  `deck_api.deck_summary`, or `deck_api.start_hook_deck_snapshot`.
- Corpus metadata must not change `ClientActionEvent`, submitted-deck payload
  shape, evidence-ledger entries, runtime artifacts, workbook output, webhook
  output, Apps Script behavior, analytics, AI, coaching, release policy, or
  production behavior.
- Corpus metadata must not turn event-set or submit-deck evidence into a claim
  about live private deck contents, exact deck identity, active deck identity,
  submitted deck facts beyond existing parser-owned fields, sideboard deltas,
  decklist completion, archetypes, card choices, collection ownership, economy
  state, or gameplay advice.

Protected surfaces explicitly not touched:

- parser behavior
- client-action parser behavior
- parser event classes
- parser state final reconciliation
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime surfaces
- local active-deck or collection artifacts
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- failed delivery artifacts
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

- `docs/contracts/parser_corpus_deck_upsert_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md`

Files Codex C may inspect but must not change unless it routes back for a
contract clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `tests/test_parsers.py`
- `tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- client-action parser semantics changes
- dedicated deck-upsert parser implementation
- submitted-deck payload shape changes
- event-set deck coverage changes
- deck-summary coverage changes
- StartHook deck snapshot coverage changes
- store, pack, inbox, crafting, wildcard, inventory, or economy coverage
- runtime active-deck or collection-profile behavior changes

## Public Interface

The public interface is the corpus parity report generated from:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

No parser API, runtime API, workbook API, webhook payload, Apps Script entry
point, Google Sheets surface, analytics schema, Match Journal schema, overlay
API, local app route, OpenAI/model-provider API, or production interface is
changed by this contract.

## Observed Current Behavior

Observed from the issue and current repo state:

- Issue #396 is open and routed to Codex B for contract writing.
- Tracker #158 remains open.
- PR #395 merged issue #394 into `codex/parser-parity` at
  `3a128565b33ef512c8edcba13083449cb284b55b`.
- The current corpus parity matrix reports `deck_api.deck_summary` as
  `covered_report_only` with entry `deck_summary_boundary_report_v1`.
- The current corpus parity matrix reports `deck_api.deck_upsert` as
  `missing` with `coverage_basis == ["external_reference_only"]` and no Mythic
  Edge entries.
- The current corpus parity matrix reports `deck_api.event_set_deck` as
  `covered_committed` with entry `bo1_match_win_basic`.
- Focused parser tests cover submit-deck responses as `submit_deck_resp`.
- Evidence-ledger contracts and tests distinguish `submit_deck_seen` and
  `submitted_deck_cards` from broad deck-state or deck identity truth.
- No inspected contract or test authorizes treating event-set deck,
  submit-deck, deck summary, or StartHook deck snapshot evidence as dedicated
  deck-upsert parser support.

## Required Guarantees

Codex C must preserve these guarantees:

- The only scenario family whose corpus parity status may change in this slice
  is `deck_api.deck_upsert`.
- `deck_api.deck_upsert` must become `covered_report_only`, not
  `covered_committed` or `covered_synthetic`.
- `coverage_basis` for the new deck-upsert boundary must be exactly
  `["fixture_metadata_only"]` unless Codex C routes back for contract
  clarification.
- `parser_behavior_verified` must not be used for `deck_api.deck_upsert` in
  this slice.
- The new manifest entry must have no parser event families.
- The new manifest entry must state that dedicated deck-upsert API behavior is
  not claimed.
- The new manifest entry must explicitly reject using event-set deck,
  submit-deck, deck summary, StartHook deck snapshot, submitted-deck cards, or
  deck-state evidence as proof of deck-upsert parser support.
- Existing rows for `deck_api.event_set_deck`, `deck_api.deck_summary`,
  `deck_api.start_hook_deck_snapshot`, and
  `deck_api.store_pack_inbox_or_crafting` must retain their existing semantic
  boundaries.
- No raw private evidence, external corpus contents, private decklists, private
  deck names, card choices, strategy notes, generated artifacts, runtime
  artifacts, SQLite files, workbook exports, credentials, tokens, keys, or
  webhook endpoints may be committed or reproduced.

## Authorized Manifest Entry

Codex C should add one report-only manifest entry with this intended shape:

```yaml
entry_id: "deck_upsert_boundary_report_v1"
title: "Deck upsert boundary report"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
scenario_families:
  - "deck_api.deck_upsert"
parser_event_families: []
parser_claim_families:
  - "deck_upsert_boundary_report"
  - "event_set_deck_reference_only"
  - "submit_deck_reference_only"
  - "dedicated_deck_upsert_api_not_claimed"
  - "deck_upsert_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
linked_issues:
  - "https://github.com/Tahjali11/Mythic-Edge/issues/396"
authorized_by_contract:
  - "docs/contracts/parser_corpus_deck_upsert_coverage.md"
```

Expected known gap language:

- Deck-upsert coverage is report-only boundary metadata.
- Mythic Edge has event-set deck coverage, deck-summary boundary coverage, and
  submit-deck parser/provenance surfaces, but none of those are dedicated
  deck-upsert API parser support.
- The entry does not prove private deck contents, exact deck identity,
  active-deck identity, submitted-deck truth beyond existing parser-owned
  fields, sideboard-delta truth, decklist completion, collection ownership,
  inventory/economy state, analytics truth, AI truth, coaching truth, release
  readiness, or production behavior.

Expected review-note language:

- The row is intentionally report-only.
- It prevents false parity claims by documenting why nearby deck evidence is
  not deck-upsert evidence.
- It leaves future dedicated deck-upsert fixture work blocked until Mythic Edge
  has owned, sanitized, parser-supported evidence.

## Authorized Session-Ledger Entry

Codex C should add one session-ledger entry with this intended shape:

```yaml
session_id: "deck_upsert_boundary_report_v1"
title: "Deck upsert boundary report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
authorized_by_contract: "docs/contracts/parser_corpus_deck_upsert_coverage.md"
scenario_families:
  - "deck_api.deck_upsert"
format_family: "deck_api"
match_shape: "deck_upsert_boundary_report_only"
record_summary: "committed_deck_upsert_boundary_metadata_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  event_set_deck_reference_entries: 1
  submit_deck_reference_entries: 1
  dedicated_deck_upsert_api_events: 0
  dedicated_deck_upsert_parser_routes: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
```

The exact numeric reference counts may be adjusted only if Codex C documents
the observed fixture evidence in the implementation handoff. Dedicated
deck-upsert API event and parser-route counts must remain zero in this slice.

Required report-only redactions:

```yaml
raw_log_lines_included: false
private_paths_included: false
raw_payloads_included: false
external_logs_included: false
decklists_included: false
private_deck_names_included: false
private_collection_data_included: false
```

## Expected Corpus Report Change

After Codex C, the matrix row for `deck_api.deck_upsert` should be:

```yaml
scenario_family: "deck_api.deck_upsert"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "deck_upsert_boundary_report_v1"
external_reference_status: "reference_category_not_checked"
```

Expected note:

- Deck upsert coverage is report-only boundary metadata.
- Mythic Edge has adjacent event-set, deck-summary, StartHook, and submit-deck
  evidence, but does not claim dedicated deck-upsert API parser support or deck
  identity/submitted-deck truth from those surfaces.

Expected summary count movement, assuming no other branch changes:

- `covered_report_only`: increases by 1.
- `missing`: decreases by 1.
- `covered_committed`: unchanged.
- `covered_synthetic`: unchanged.
- `partial`: unchanged.
- `blocked_external_boundary`: unchanged.

Codex C must record the actual before/after counts in its implementation
handoff and contract test report.

## Validation Obligations

Codex C must run focused validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --all
printf '%s\n' \
  docs/contracts/parser_corpus_deck_upsert_coverage.md \
  docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests
git diff --check
```

Codex C may add narrower or platform-specific commands if local tool behavior
requires it. Any skipped command must be reported with the reason.

Codex E/F/G should verify:

- Only authorized files changed.
- The contract path is cited by the new manifest/session-ledger entries.
- `deck_api.deck_upsert` is `covered_report_only`, not synthetic or committed.
- `parser_behavior_verified` is absent from the deck-upsert row.
- `deck_api.event_set_deck` remains `covered_committed`.
- `deck_api.deck_summary` remains `covered_report_only`.
- `deck_api.store_pack_inbox_or_crafting` remains outside this slice.
- No private or external corpus evidence was committed.
- No parser/runtime/workbook/webhook/App Script/analytics/AI behavior changed.

## Acceptance Criteria

This module is complete when:

- `docs/contracts/parser_corpus_deck_upsert_coverage.md` exists and is cited by
  the implementation handoff and report.
- `deck_upsert_boundary_report_v1` exists in the corpus manifest and session
  ledger.
- The corpus parity report maps `deck_api.deck_upsert` to
  `covered_report_only` with `coverage_basis == ["fixture_metadata_only"]`.
- The report clearly distinguishes deck-upsert boundary metadata from
  event-set deck, deck summary, StartHook deck snapshot, submit-deck signal,
  and submitted-deck card-content evidence.
- Focused corpus parity tests cover the new manifest, session-ledger, report
  row, non-claims, and unchanged adjacent family statuses.
- The implementation handoff records comparison, files changed, validation run,
  open risks, and next recommended role.
- The contract test report records the validation evidence and final row
  counts.

## Unknowns

- Whether future owned Mythic Edge evidence will expose a genuine dedicated
  deck-upsert API response shape.
- Whether a future sanitized fixture can prove deck-upsert parser behavior
  without committing private deck contents, deck names, card choices, strategy
  notes, or external corpus contents.
- Whether deck-upsert should eventually be split into more than one scenario
  family if owned evidence reveals multiple distinct payload shapes.

These unknowns do not block report-only boundary coverage.

## Suspected Gaps

- The current corpus matrix can make `deck_api.deck_upsert` look simply
  unexamined, even though adjacent deck evidence has been deliberately scoped
  away from upsert.
- Event-set and submit-deck terminology are easy to overread as broad deck API
  support.
- Future work could accidentally use submitted-deck card-content evidence as
  deck-upsert parity evidence unless this boundary is explicit.

## Non-Claims

This contract does not claim:

- dedicated deck-upsert parser support
- event-set deck support beyond the existing `deck_api.event_set_deck` family
- deck-summary support beyond the existing report-only row
- StartHook deck snapshot support beyond the existing synthetic row
- submitted-deck card-content truth beyond existing parser/evidence-ledger
  fields
- active-deck identity
- exact deck identity
- decklist completion
- sideboard-delta truth
- private deck contents
- private deck names
- collection ownership truth
- inventory/economy truth
- archetype truth
- matchup-plan truth
- gameplay advice
- player-mistake labels
- analytics truth
- AI truth
- coaching truth
- release readiness
- production behavior
- tracker completion

## Stop Conditions

Codex C must stop and route back to Codex B if implementation would require:

- parser code changes
- parser event class changes
- client-action parser behavior changes
- submitted-deck payload shape changes
- corpus vocabulary changes outside existing allowed values
- reclassifying `deck_api.event_set_deck`
- reclassifying `deck_api.deck_summary`
- reclassifying `deck_api.start_hook_deck_snapshot`
- reclassifying `deck_api.store_pack_inbox_or_crafting`
- private or external corpus evidence
- raw Player.log excerpts
- Manasight source or raw corpus contents
- workbook, webhook, Apps Script, Google Sheets, runtime, analytics, local app,
  AI, OpenAI/model-provider, CI, merge, deploy, release, or production changes

## Recommended Next Role

Codex C: Module Implementer.

Implementation should proceed as a metadata/test-only corpus parity update.

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #396, deck upsert corpus evidence boundary.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/396

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_deck_upsert_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change that satisfies the deck-upsert coverage contract. Add report-only boundary coverage for exactly deck_api.deck_upsert without changing parser behavior or claiming dedicated deck-upsert parser support.

  Required behavior:
  - Add deck_upsert_boundary_report_v1 to the corpus manifest and session ledger.
  - Change the corpus parity row for deck_api.deck_upsert from missing/external_reference_only to covered_report_only/fixture_metadata_only.
  - Keep parser_event_families empty for the deck-upsert boundary entry.
  - Do not include parser_behavior_verified for deck_api.deck_upsert.
  - Explicitly document that event-set deck, deck summary, StartHook deck snapshot, submit-deck signals, and submitted-deck cards are reference-only adjacent evidence, not deck-upsert parser support.
  - Preserve the existing statuses and meanings of deck_api.event_set_deck, deck_api.deck_summary, deck_api.start_hook_deck_snapshot, and deck_api.store_pack_inbox_or_crafting.
  - Produce docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md and docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report
  - python3 tools/check_agent_docs.py
  - python3 tools/check_secret_patterns.py --all
  - printf '%s\n' docs/contracts/parser_corpus_deck_upsert_coverage.md docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests
  - git diff --check

  Do not:
  - Implement parser behavior.
  - Change client-action parser behavior.
  - Change parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics, golden replay, feature-equity, evidence-ledger behavior, runtime artifacts, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, release policy, or production behavior.
  - Commit or reproduce raw/private Player.log excerpts, Manasight logs, external corpus contents, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, or strategy notes.
  - Claim full Mythic Edge corpus parity or dedicated deck-upsert support.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/395"
  previous_merge_commit: "3a128565b33ef512c8edcba13083449cb284b55b"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_deck_upsert_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md"
  verdict: "contract_ready_for_report_only_deck_upsert_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim dedicated deck-upsert parser support from adjacent deck evidence."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, strategy notes, or private reports."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/395"
  previous_merge_commit: "3a128565b33ef512c8edcba13083449cb284b55b"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_deck_upsert_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md"
  verdict: "contract_ready_for_report_only_deck_upsert_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "pending - Codex C implementation should run focused corpus parity, client-action parser, report generation, docs, secret, protected-surface, ruff, and diff checks."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim dedicated deck-upsert parser support from adjacent deck evidence."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, strategy notes, or private reports."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
