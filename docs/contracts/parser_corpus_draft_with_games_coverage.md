# Parser Corpus Draft With Games Coverage Contract

## Module

Draft-with-games corpus evidence boundary for the parser corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`core_gameplay.draft_with_games` as a report-only corpus boundary. It does not
claim that the current synthetic draft parser-family fixture covers a complete
draft session with games, match rows, game results, match results, draft deck
construction, draft picks as strategy evidence, or limited gameplay parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/398
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/399
- Previous merge commit:
  `5a512507b262eac468d80e283b5afcb2099452ad`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-draft-with-games-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `5a512507b262eac468d80e283b5afcb2099452ad`
- target_artifact:
  `docs/contracts/parser_corpus_draft_with_games_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md`
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
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/contracts/parser_draft_surface_parity_recommendation.md`
- `docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md`
- `docs/contract_test_reports/parser_draft_fixture_coverage.md`
- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_draft_human_parser.py`
- `tests/test_draft_complete_parser.py`
- `tests/test_golden_replay_harness.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, draft examples,
  deck examples, match examples, game-result examples, or external corpus
  contents.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic draft-with-games coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, or blocked-private-evidence status.

Selected path: report-only boundary coverage.

Reasoning:

- Mythic Edge has current synthetic draft parser-family coverage for
  `DraftBot`, `DraftHuman`, and `DraftComplete`.
- The current draft fixture is explicitly `core_gameplay.draft_only`.
- The current draft session ledger entry has `match_shape == "draft_only"`,
  `game_rows.count == 0`, and `game_rows.result_shape == "not_applicable"`.
- The current draft golden replay manifest includes a small synthetic GameState
  anchor only so the fixture can pass diagnostics and parser-state review. That
  anchor does not prove completed limited gameplay, game-result evidence,
  match-result evidence, game rows, or draft-with-games session continuity.
- A synthetic draft-with-games fixture would need a larger dedicated contract
  because it would combine draft event evidence with game/match result evidence
  and limited gameplay facts.
- A deferred status would be accurate but less useful than report-only
  boundary coverage because the row is an inspected blind spot and the current
  draft-only fixture already names `draft_with_games` as a known gap.

This decision records `core_gameplay.draft_with_games` as a report-only corpus
boundary. It changes corpus parity metadata and tests only; it does not change
parser behavior or expand the draft fixture.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`core_gameplay.draft_with_games` scenario family. Draft parser modules own
draft event interpretation. Game/match parser and state modules own
parser-derived game and match facts. Golden replay owns replaying committed
fixtures through the normal parser path. Runtime surfaces, analytics, workbook
outputs, and AI/coaching surfaces remain downstream consumers and must not own
this coverage claim.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence. It is not a Parser behavior module and is not a runtime,
workbook, webhook, Apps Script, Google Sheets, analytics, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `core_gameplay.draft_with_games` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Related parser and harness truth owners that must not be reclassified by this
contract:

- Draft parser modules own `DraftBot`, `DraftHuman`, and `DraftComplete`
  event interpretation.
- Golden replay owns `draft_parser_family` fixture replay behavior.
- Parser state owns game/match facts when a real or synthetic fixture provides
  actual game and result evidence.
- Existing draft fixture artifacts own only draft-only coverage.

Truth boundary:

- `core_gameplay.draft_only` remains synthetic draft parser-family coverage.
- `draft_parser_family_v1` remains `match_shape == "draft_only"` with zero
  game rows.
- `DraftBot`, `DraftHuman`, and `DraftComplete` coverage does not imply
  draft-with-games coverage.
- A GameState anchor in the current draft fixture does not imply completed
  limited gameplay, game-result evidence, match-result evidence, or game rows.
- This contract owns only the report-only draft-with-games boundary row:
  Mythic Edge has no current dedicated completed draft-with-games fixture
  claim.
- Corpus coverage status is review metadata. It is not draft-pick truth,
  limited deck-construction truth, decklist truth, hidden-card truth,
  match/game truth beyond existing parser-owned fixtures, analytics truth, AI
  truth, coaching truth, merge readiness, deploy readiness, release readiness,
  production behavior, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing draft-only parser fixture, golden replay manifest, and corpus rows
  -> bounded committed report-only manifest/session-ledger metadata
  -> corpus parity boundary row for core_gameplay.draft_with_games
```

Forbidden reverse flow:

- Corpus coverage status must not change draft parser behavior.
- Corpus metadata must not create, imply, or require a dedicated
  draft-with-games parser.
- Corpus metadata must not change `DraftBot`, `DraftHuman`, or
  `DraftComplete` payload semantics.
- Corpus metadata must not expand the current draft fixture into game-result
  or match-result evidence.
- Corpus metadata must not change parser state final reconciliation, game
  result handling, match result handling, runtime artifacts, workbook output,
  webhook output, Apps Script behavior, analytics, AI, coaching, release
  policy, or production behavior.
- Corpus metadata must not turn draft events, draft picks, draft completion,
  or a GameState anchor into limited deck construction, gameplay result, deck
  quality, archetype, strategy, or coaching truth.

Protected surfaces explicitly not touched:

- parser behavior
- draft parser behavior
- parser event classes
- parser state final reconciliation
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime surfaces
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

- `docs/contracts/parser_corpus_draft_with_games_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md`

Files Codex C may inspect but must not change unless it routes back for a
contract clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- `tests/test_golden_replay_harness.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_draft_human_parser.py`
- `tests/test_draft_complete_parser.py`
- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/implementation_handoffs/parser_draft_fixture_coverage_comparison.md`
- `docs/contract_test_reports/parser_draft_fixture_coverage.md`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- draft parser semantics changes
- draft fixture log or golden manifest changes
- game-result or match-result parser changes
- new draft-with-games synthetic fixture implementation
- private live draft evidence collection
- feature-equity baseline changes
- draft picks, draft pool, decklist, sideboard, card-choice, archetype, or
  strategy evidence

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

- Issue #400 is open and routed to Codex B for contract writing.
- Tracker #158 remains open.
- PR #399 merged issue #398 into `codex/parser-parity` at
  `5a512507b262eac468d80e283b5afcb2099452ad`.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 12 missing)`.
- The current corpus parity matrix reports `core_gameplay.draft_only` as
  `covered_synthetic`.
- The current corpus parity matrix reports `core_gameplay.draft_with_games` as
  `missing` with `coverage_basis == ["external_reference_only"]` and no Mythic
  Edge entries.
- The current `draft_parser_family_v1` session-ledger entry covers only
  `core_gameplay.draft_only`.
- The current `draft_parser_family_v1` session-ledger entry records
  `match_shape == "draft_only"`, `game_rows.count == 0`, and
  `game_rows.result_shape == "not_applicable"`.
- The current draft golden replay manifest emits `DraftBot`, `DraftHuman`,
  `DraftComplete`, and one `GameState` anchor.
- The current draft golden replay manifest does not include game completion,
  game result, match result, completed limited match rows, draft deck
  construction, or limited gameplay result evidence.
- The draft fixture coverage report explicitly states that live private draft
  evidence remains intentionally unused and the fixture does not prove every
  live draft variant.

## First Bad Value

```yaml
scenario_family: "core_gameplay.draft_with_games"
coverage_status: "missing"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries: []
```

Nearby boundary value:

```yaml
entry_id: "draft_parser_family"
scenario_families:
  - "core_gameplay.draft_only"
known_gaps:
  - "draft_with_games"
```

## Required Guarantees

Codex C must preserve these guarantees:

- The only scenario family whose corpus parity status may change in this slice
  is `core_gameplay.draft_with_games`.
- `core_gameplay.draft_with_games` must become `covered_report_only`, not
  `covered_committed` or `covered_synthetic`.
- `coverage_basis` for the new boundary must be exactly
  `["fixture_metadata_only"]` unless Codex C routes back for contract
  clarification.
- `parser_behavior_verified` must not be used for
  `core_gameplay.draft_with_games` in this slice.
- The new manifest entry must have no parser event families.
- The new manifest entry must state that completed draft-with-games behavior is
  not claimed.
- The new manifest entry must explicitly reject using the current draft-only
  fixture, draft parser event coverage, `DraftComplete`, or the synthetic
  GameState anchor as proof of completed limited gameplay or result coverage.
- Existing rows and meanings for `core_gameplay.draft_only`,
  `core_gameplay.standard_bo1`, `core_gameplay.standard_bo3`, and
  `core_gameplay.traditional_bo3` must retain their existing semantic
  boundaries.
- No raw private evidence, external corpus contents, private draft logs, draft
  picks, sealed/draft pools, decklists, deck names, card choices, sideboard
  choices, strategy notes, generated artifacts, runtime artifacts, SQLite
  files, workbook exports, credentials, tokens, keys, or webhook endpoints may
  be committed or reproduced.

## Authorized Manifest Entry

Codex C should add one report-only manifest entry with this intended shape:

```yaml
entry_id: "draft_with_games_boundary_report_v1"
title: "Draft with games boundary report"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
scenario_families:
  - "core_gameplay.draft_with_games"
parser_event_families: []
parser_claim_families:
  - "draft_with_games_boundary_report"
  - "draft_only_reference_only"
  - "draft_parser_family_not_completed_games"
  - "limited_game_result_evidence_not_claimed"
  - "draft_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
linked_issues:
  - "https://github.com/Tahjali11/Mythic-Edge/issues/400"
authorized_by_contract:
  - "docs/contracts/parser_corpus_draft_with_games_coverage.md"
```

Expected known gap language:

- Draft-with-games coverage is report-only boundary metadata.
- Mythic Edge has synthetic draft parser-family coverage for DraftBot,
  DraftHuman, and DraftComplete, but that coverage is draft-only and does not
  prove completed limited gameplay, game-result evidence, match-result
  evidence, game rows, draft deck construction, draft picks as strategy
  evidence, analytics truth, AI truth, coaching truth, release readiness, or
  production behavior.

Expected review-note language:

- The row is intentionally report-only.
- It prevents false parity claims by documenting why the current draft-only
  fixture and synthetic GameState anchor are not draft-with-games evidence.
- Future dedicated coverage remains blocked until Mythic Edge has owned,
  sanitized, parser-supported evidence for a completed draft session with games
  and results.

## Authorized Session-Ledger Entry

Codex C should add one session-ledger entry with this intended shape:

```yaml
session_id: "draft_with_games_boundary_report_v1"
title: "Draft with games boundary report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
authorized_by_contract: "docs/contracts/parser_corpus_draft_with_games_coverage.md"
scenario_families:
  - "core_gameplay.draft_with_games"
format_family: "limited_draft"
match_shape: "draft_with_games_boundary_report_only"
record_summary: "committed_draft_with_games_boundary_metadata_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  draft_only_reference_entries: 1
  draft_parser_family_reference_entries: 1
  completed_draft_game_rows: 0
  game_result_events: 0
  match_result_events: 0
  dedicated_draft_with_games_fixtures: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
```

Dedicated draft-with-games fixture, completed-game-row, game-result, and
match-result counts must remain zero in this slice.

Required report-only redactions:

```yaml
raw_log_lines_included: false
private_paths_included: false
raw_payloads_included: false
external_logs_included: false
draft_picks_included: false
draft_pools_included: false
decklists_included: false
private_deck_names_included: false
card_choices_included: false
strategy_notes_included: false
```

## Expected Corpus Report Change

After Codex C, the matrix row for `core_gameplay.draft_with_games` should be:

```yaml
scenario_family: "core_gameplay.draft_with_games"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "draft_with_games_boundary_report_v1"
external_reference_status: "reference_category_not_checked"
```

Expected note:

- Draft-with-games coverage is report-only boundary metadata.
- Mythic Edge has draft-only synthetic parser-family coverage, but does not
  claim a completed draft session with games, game rows, game-result evidence,
  match-result evidence, limited deck construction, draft-pick strategy truth,
  analytics truth, AI truth, coaching truth, release readiness, or production
  behavior from that fixture.

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
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_draft_with_games_coverage.md \
  docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_draft_with_games_coverage.md \
  docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C may add narrower or platform-specific commands if local tool behavior
requires it. Any skipped command must be reported with the reason.

Codex E/F/G should verify:

- Only authorized files changed.
- The contract path is cited by the new manifest/session-ledger entries.
- `core_gameplay.draft_with_games` is `covered_report_only`, not synthetic or
  committed.
- `parser_behavior_verified` is absent from the draft-with-games row.
- `parser_event_families` is empty for the new boundary entry.
- `core_gameplay.draft_only` remains `covered_synthetic`.
- The current draft fixture and golden replay manifest are unchanged.
- No private or external corpus evidence was committed.
- No parser/runtime/workbook/webhook/App Script/analytics/AI behavior changed.

## Acceptance Criteria

This module is complete when:

- `docs/contracts/parser_corpus_draft_with_games_coverage.md` exists and is
  cited by the implementation handoff and report.
- `draft_with_games_boundary_report_v1` exists in the corpus manifest and
  session ledger.
- The corpus parity report maps `core_gameplay.draft_with_games` to
  `covered_report_only` with `coverage_basis == ["fixture_metadata_only"]`.
- The report clearly distinguishes draft-with-games boundary metadata from
  draft-only parser-family coverage, `DraftComplete`, GameState anchor
  evidence, game rows, game-result evidence, match-result evidence, limited
  deck construction, draft-pick strategy truth, analytics truth, AI truth, and
  coaching truth.
- Focused corpus parity tests cover the new manifest, session-ledger, report
  row, non-claims, and unchanged adjacent family statuses.
- The implementation handoff records comparison, files changed, validation run,
  open risks, and next recommended role.
- The contract test report records the validation evidence and final row
  counts.

## Unknowns

- Whether future owned Mythic Edge evidence will expose a complete draft
  session with draft event flow, games, game results, match result, and limited
  context.
- Whether a future synthetic fixture can safely model a completed
  draft-with-games session without creating misleading deck construction,
  draft-pick, or gameplay claims.
- Whether future private live draft evidence collection should remain local
  report-only or be sanitized into a committed fixture after explicit approval.
- Whether `core_gameplay.draft_with_games` should later split into smaller
  families for draft event flow, limited match gameplay, and draft-result
  reconciliation.

These unknowns do not block report-only boundary coverage.

## Suspected Gaps

- The current corpus matrix can make `core_gameplay.draft_with_games` look
  simply unexamined, even though the draft-only fixture already names it as a
  known gap.
- `DraftComplete` can be overread as proof of games played; it is only draft
  completion evidence.
- The current GameState anchor can be overread as limited gameplay evidence;
  it is only a diagnostics/parser-state anchor for the synthetic fixture.
- Future work could accidentally use private draft choices, decklists, or
  strategy notes as parity evidence unless this boundary is explicit.

## Non-Claims

This contract does not claim:

- completed draft-with-games fixture support
- completed limited gameplay support
- draft match result evidence
- draft game result evidence
- game rows from the current draft fixture
- match rows from the current draft fixture
- draft deck construction truth
- draft pick quality truth
- draft pool truth
- draft decklist truth
- sideboard choice truth
- hidden-card truth
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
- draft parser behavior changes
- router behavior changes
- parser state final reconciliation changes
- game-result or match-result behavior changes
- changing `tests/fixtures/draft_parser_family_slice.log`
- changing `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- changing feature-equity baseline counts
- corpus vocabulary changes outside existing allowed values
- reclassifying `core_gameplay.draft_only`
- private or external corpus evidence
- raw Player.log excerpts
- Manasight source or raw corpus contents
- private draft logs
- draft picks
- sealed or draft pools
- decklists, deck names, card choices, sideboard choices, or strategy notes
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

  Act as Codex C: Module Implementer for issue #400, draft-with-games corpus evidence boundary.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/400

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_draft_with_games_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change that satisfies the draft-with-games coverage contract. Add report-only boundary coverage for exactly core_gameplay.draft_with_games without changing parser behavior or claiming completed limited gameplay, game-result evidence, match-result evidence, draft deck construction, or draft-pick strategy truth.

  Required behavior:
  - Add draft_with_games_boundary_report_v1 to the corpus manifest and session ledger.
  - Change the corpus parity row for core_gameplay.draft_with_games from missing/external_reference_only to covered_report_only/fixture_metadata_only.
  - Keep parser_event_families empty for the new boundary entry.
  - Do not include parser_behavior_verified for core_gameplay.draft_with_games.
  - Explicitly document that the current draft_parser_family fixture is draft_only and reference-only for this row.
  - Explicitly document that DraftBot, DraftHuman, DraftComplete, and the synthetic GameState anchor are not draft-with-games evidence.
  - Preserve core_gameplay.draft_only as covered_synthetic and do not change the current draft fixture or golden replay manifest.
  - Produce docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md and docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
  - PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - printf '%s\n' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
  - printf '%s\n' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests tools
  - git diff --check

  Do not:
  - Implement parser behavior.
  - Change draft parser behavior.
  - Change parser event classes, router semantics, parser state final reconciliation, game-result behavior, match-result behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics, golden replay, feature-equity, evidence-ledger behavior, runtime artifacts, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, release policy, or production behavior.
  - Change tests/fixtures/draft_parser_family_slice.log or tests/fixtures/golden_replay/draft_parser_family.manifest.json.
  - Commit or reproduce raw/private Player.log excerpts, Manasight logs, external corpus contents, private draft logs, draft picks, sealed/draft pools, decklists, deck names, card choices, sideboard choices, strategy notes, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, or private reports.
  - Claim full Mythic Edge corpus parity or completed draft-with-games support.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/399"
  previous_merge_commit: "5a512507b262eac468d80e283b5afcb2099452ad"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_draft_with_games_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md"
  verdict: "contract_ready_for_report_only_draft_with_games_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim draft-with-games coverage from the current draft-only fixture."
    - "Do not reopen or broaden DraftBot, DraftHuman, DraftComplete, or draft-only fixture coverage."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, draft picks, sealed/draft pools, decklists, deck names, card choices, sideboard choices, private strategy notes, generated/private/runtime artifacts, or secrets."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/analytics/AI/production surfaces without a new explicit contract."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/399"
  previous_merge_commit: "5a512507b262eac468d80e283b5afcb2099452ad"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_draft_with_games_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md"
  verdict: "contract_ready_for_report_only_draft_with_games_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "pending - Codex C implementation should run focused corpus parity, draft parser, golden replay, report generation, docs, secret, protected-surface, ruff, and diff checks."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim draft-with-games coverage from the current draft-only fixture."
    - "Do not reopen or broaden DraftBot, DraftHuman, DraftComplete, or draft-only fixture coverage."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, draft picks, sealed/draft pools, decklists, deck names, card choices, sideboard choices, private strategy notes, generated/private/runtime artifacts, or secrets."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/analytics/AI/production surfaces without a new explicit contract."
```
