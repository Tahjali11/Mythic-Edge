# Parser Corpus Draft With Games Behavior Uplift Contract

## Module

`core_gameplay.draft_with_games` parser corpus behavior uplift planning.

Plain English: Mythic Edge already has draft-only parser-family coverage and a
report-only boundary for draft-with-games. This contract defines the evidence
required to move `core_gameplay.draft_with_games` toward parser-behavior
readiness without overclaiming from draft-only evidence, `DraftComplete`, or
the current synthetic GameState anchor.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/479
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Latest completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/477
- Latest completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/478
- Latest merge commit: `8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
- Prior boundary PR: https://github.com/Tahjali11/Mythic-Edge/pull/401
- Base branch inspected: `main`
- Contract branch: `codex/parser-corpus-draft-with-games-behavior-uplift-479`
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

- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_draft_with_games_coverage.md`
- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/contracts/parser_draft_surface_parity_recommendation.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_gre_game_result.md`
- `docs/contracts/parser_match_state.md`
- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/golden_replay/draft_parser_family.manifest.json`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `tests/test_golden_replay_harness.py`
- `tests/test_draft_bot_parser.py`
- `tests/test_draft_human_parser.py`
- `tests/test_draft_complete_parser.py`

## Purpose

Define the minimum safe evidence model for moving
`core_gameplay.draft_with_games` beyond the #400 report-only boundary.

This contract answers:

- what parser-owned facts are required for draft-with-games behavior evidence;
- whether owned synthetic evidence is acceptable;
- what future manifest/session-ledger status movement is allowed;
- which adjacent draft and game facts are evidence versus non-claims; and
- which privacy, fixture, #388, and protected-surface boundaries must remain
  intact.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live draft checks, activate #388/#381, or claim draft-with-games
parser support.

## Observed Current Behavior

Observed on `main` at
`8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0`:

- Issue #479 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #477 is complete after PR #478.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=14, report_only=19, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current applicability metrics:

```yaml
parser_behavior_applicability_ready: false
parser_behavior_applicable_family_count: 37
parser_behavior_applicable_ready_family_count: 19
parser_behavior_applicable_not_ready_family_count: 18
parser_behavior_not_applicable_family_count: 8
```

Current `core_gameplay.draft_with_games` row:

```yaml
scenario_family: "core_gameplay.draft_with_games"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "draft_with_games_boundary_report_v1"
```

Current adjacent evidence:

- `draft_parser_family_v1` covers `core_gameplay.draft_only`.
- `draft_parser_family_v1` has `match_shape == "draft_only"`.
- `draft_parser_family_v1` has `game_rows.count == 0`.
- `draft_parser_family_v1` has `game_rows.result_shape == "not_applicable"`.
- The draft golden replay fixture emits `DraftBot`, `DraftHuman`,
  `DraftComplete`, and one `GameState` anchor.
- The draft golden replay fixture has empty game results and no match winner.
- The #400 boundary explicitly says the current draft-only fixture and
  GameState anchor are not draft-with-games evidence.

## Scope Decision

Recommended future path: reduced synthetic completed draft match fixture.

A later Codex C implementation may move `core_gameplay.draft_with_games` from
`covered_report_only` toward `covered_synthetic` with
`parser_behavior_verified` only if it adds Mythic Edge-owned synthetic evidence
that proves both:

1. draft parser-family evidence appears in the same owned fixture; and
2. completed limited gameplay produces parser-owned game/match result facts
   through the normal golden replay parser path.

This contract does not recommend waiting for #388 by default. A reduced
synthetic fixture is acceptable because the required claim is narrow:
synthetic draft-event evidence plus synthetic limited game/result flow can be
reviewed without private logs, external corpus contents, draft picks, deck
construction, decklists, or strategy notes.

Fallback rule:

- If Codex C cannot build an honest reduced synthetic fixture without changing
  parser behavior or smuggling in private/external evidence, the row must remain
  `covered_report_only` and route back to Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Draft parsers own `DraftBot`, `DraftHuman`, and `DraftComplete` event
  recognition and payload normalization.
- Match-state and GRE game-result parsers own match/game event evidence.
- Parser state owns final game and match reconciliation from parsed events.
- Golden replay owns executing committed synthetic or sanitized fixtures
  through the normal parser path and comparing reduced parser-owned outputs.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
or release-readiness surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the producer of draft/game/match facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, or parser-evidence pipeline
activation.

## Truth Owner

Truth owner for the current report-only status:

- `docs/contracts/parser_corpus_draft_with_games_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for any future behavior-ready uplift:

- the future synthetic or sanitized golden replay fixture and manifest;
- `src/mythic_edge_parser/app/golden_replay.py`;
- draft parser modules and tests;
- match-state, GRE game-result, parser-state, and focused replay tests;
- corpus manifest/session-ledger entries that cite this contract;
- the Codex C implementation handoff and Codex E contract-test report.

Truth boundary:

- The corpus row may become behavior-ready only when the normal parser path
  emits the required draft, game, and match evidence from owned fixture input.
- The corpus row must not claim parser support from #400 report-only metadata,
  `draft_parser_family_v1`, `DraftComplete` alone, or the existing GameState
  anchor.
- The corpus row must not claim draft-pick quality, draft pool truth, decklist
  truth, sideboard choice truth, archetype truth, hidden-card truth, gameplay
  advice, analytics truth, AI truth, coaching truth, private smoke success,
  release readiness, production behavior, or tracker completion.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic or sanitized draft-with-games replay fixture
  -> normal parser path and parser-owned reduced outputs
  -> golden replay report
  -> corpus manifest/session-ledger behavior evidence
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from replay output.
- Corpus metadata must not force `DraftComplete`, draft-only evidence, or a
  GameState anchor to mean completed draft gameplay.
- Corpus metadata must not move draft picks, decklists, archetypes, analytics,
  AI, coaching, workbook, webhook, or Apps Script interpretation into parser
  truth.

Protected surfaces explicitly not touched:

- parser behavior;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- match/game identity;
- deduplication;
- diagnostics behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status files;
- failed posts;
- workbook exports;
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

- `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- a new synthetic golden replay fixture under `tests/fixtures/`, with an
  obvious draft-with-games name;
- a new golden replay manifest under `tests/fixtures/golden_replay/`;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- `tests/test_golden_replay_harness.py`;
- `docs/implementation_handoffs/parser_corpus_draft_with_games_behavior_uplift_comparison.md`;
- `docs/contract_test_reports/parser_corpus_draft_with_games_behavior_uplift.md`.

Files Codex C may inspect but must not change unless the implementation
contract is looped back:

- draft parser source files;
- GRE game-state / game-result source files;
- match-state parser source files;
- parser state source files;
- current `draft_parser_family` fixture and manifest;
- focused draft, game-result, match-state, and parser-state tests.

Not owned by this contract:

- parser semantics;
- draft parser behavior;
- game-result or match-state parser behavior;
- parser state final reconciliation;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic fixture and corpus metadata that
make the corpus parity public report show `core_gameplay.draft_with_games` as
behavior-ready. The intended eventual corpus row shape is:

```yaml
scenario_family: "core_gameplay.draft_with_games"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

The existing report-only entry `draft_with_games_boundary_report_v1` should
remain as historical non-claim metadata unless Codex C has a strong reason to
route back for a replacement/migration contract. A new synthetic evidence entry
should be added rather than rewriting #400's boundary into a behavior claim.

## Minimum Parser-Owned Evidence

Future uplift requires one owned synthetic or sanitized fixture that proves the
following through golden replay.

### Draft Evidence

Required:

- at least one emitted `DraftBot` or `DraftHuman` event;
- one emitted `DraftComplete` event;
- exact draft marker parsing through existing parser modules;
- raw parsed draft payload preservation per existing draft contracts;
- no parser failures or unexpected unknown entries.

Allowed:

- minimal synthetic card IDs or pack/pick placeholders only when required by
  existing draft parser fixtures;
- bot or human draft mode, as long as the fixture labels the chosen mode.

Not sufficient:

- `DraftComplete` alone;
- draft-only fixture evidence;
- draft payload metadata without later game/result evidence.

### Completed Gameplay Evidence

Required:

- at least one parser-owned match identity or synthetic match anchor;
- at least one emitted `GameState` event from the limited gameplay segment;
- at least one emitted paired `GameResult` event from game-over GRE evidence,
  or equivalent existing parser-owned result evidence already accepted by
  golden replay;
- parser state records at least one game result;
- final reconciliation exposes a non-empty game result list and a match winner
  or match outcome consistent with the synthetic fixture;
- parser-owned game-log rows include at least one game row;
- parser-owned match-log output is present or the fixture explicitly proves why
  match-log output is unavailable and routes back before promotion.

Not sufficient:

- a single GameState anchor with no result;
- parser-state `current_game_number` without completed result evidence;
- game rows with no result/outcome evidence;
- corpus metadata asserting a game was played without parser output.

### Limited / Draft-With-Games Context

Required:

- fixture metadata must label the scenario as `limited_draft`;
- the fixture must contain draft event evidence and completed game/result
  evidence in one ordered synthetic session;
- any parser-owned format, queue, or event context emitted by existing parser
  surfaces must be preserved in expected output;
- the contract-test report must distinguish parser-owned limited context from
  fixture-level scenario labeling.

Not required for v1:

- proving every Arena draft queue;
- proving sideboarding;
- proving BO3 draft matches;
- proving draft deck construction;
- proving draft pick-to-deck continuity.

## Recommended Evidence / Status Path

Recommended Codex C path:

1. Add a new reduced synthetic fixture for one completed limited draft session
   with one game result.
2. Add a golden replay manifest for that fixture.
3. Assert reduced parser-owned outputs:
   - draft event family counts;
   - game/match event family counts;
   - final reconciliation;
   - parser-owned game rows;
   - unknown/truncation/degradation counts;
   - privacy fields.
4. Add one new corpus manifest entry for the synthetic evidence.
5. Add one new session-ledger entry for the synthetic evidence.
6. Keep `draft_with_games_boundary_report_v1` as report-only non-claim
   metadata.
7. Update focused corpus and golden replay tests.

Allowed future status movement:

- from `covered_report_only` to `covered_synthetic`;
- with `coverage_basis` including both `fixture_metadata_only` and
  `parser_behavior_verified`;
- only after the new synthetic fixture passes golden replay through the normal
  parser path.

Disallowed in this lane:

- `covered_committed`, unless a later sanitized fixture-promotion issue
  explicitly creates a reviewed sanitized fixture;
- private/local-only report evidence;
- external corpus evidence;
- status movement without a new fixture and tests;
- status movement based only on #400, `draft_parser_family_v1`,
  `DraftComplete`, or the existing GameState anchor.

## Behavior-Uplift Packet

This section is a small reusable packet pattern for future behavior-uplift
rows. In this contract it applies only to `core_gameplay.draft_with_games`.
It must not be used here to solve, promote, or reclassify any other corpus row.

| Question | Contracted answer for #479 |
| --- | --- |
| Scenario family | `core_gameplay.draft_with_games` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `draft_with_games_boundary_report_v1` |
| Target status, if any | `covered_synthetic` only after owned golden replay evidence exists |
| May `parser_behavior_verified` be added? | Yes, but only to a new synthetic evidence entry after the fixture passes through the normal parser path |
| Evidence type | Synthetic committed fixture preferred; committed sanitized evidence requires a later fixture-promotion issue; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | One new reduced synthetic fixture and one golden replay manifest are allowed for Codex C; mutating the existing draft-only fixture into draft-with-games evidence is forbidden |
| Manifest/session-ledger changes | Additive entries citing this contract are allowed for Codex C; changing unrelated rows or removing #400 report-only boundary metadata is forbidden |
| Parser behavior changes | Forbidden; if existing parser behavior cannot support the reduced fixture, route back instead of changing parser behavior |
| Private/external inputs | Private Player.log, UTC_Log, live draft runs, Manasight/external raw corpora, decklists, draft pools, card choices, and private reports are forbidden |
| Required non-claims | No draft pick quality, deck construction, decklist, archetype, hidden-card, gameplay advice, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Corpus parity report/tests, golden replay tests, DraftBot/DraftHuman/DraftComplete parser tests, docs check, ruff, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; the row may improve readiness counts but does not start the parser-evidence pipeline by itself |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Required Future Manifest Entry Shape

The exact `entry_id` may vary, but future Codex C should prefer:

```yaml
entry_id: "draft_with_games_synthetic_v1"
title: "Draft with games synthetic replay"
entry_type: "golden_replay_manifest"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
scenario_families:
  - "core_gameplay.draft_with_games"
parser_event_families:
  - "DraftBot" # or "DraftHuman", depending on fixture mode
  - "DraftComplete"
  - "MatchState"
  - "GameState"
  - "GameResult"
parser_claim_families:
  - "draft_event_flow"
  - "draft_complete_signal"
  - "limited_gameplay_result_flow"
  - "draft_with_games_synthetic_boundary"
  - "draft_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/479"
authorized_by_contract: "docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md"
```

Required known-gap language:

- The fixture proves a reduced synthetic completed draft-with-games path only.
- It does not prove all Arena draft queues, live private draft behavior, BO3
  draft, sideboarding, deck construction, draft pick quality, decklists,
  archetypes, analytics truth, AI truth, coaching truth, release readiness, or
  production behavior.

## Required Future Session-Ledger Shape

The exact `session_id` may vary, but future Codex C should prefer:

```yaml
session_id: "draft_with_games_synthetic_v1"
title: "Draft with games synthetic replay"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/479"
authorized_by_contract: "docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md"
scenario_families:
  - "core_gameplay.draft_with_games"
format_family: "limited_draft"
match_shape: "draft_with_games_single_game_synthetic"
record_summary: "synthetic_completed_draft_with_games_summary"
parser_coverage:
  event_families:
    DraftComplete: 1
    GameResult: 1
  unknown_entries: 0
  truncation_count: 0
  dedicated_draft_with_games_fixtures: 1
  completed_draft_game_rows: 1
  game_result_events: 1
  match_result_events: 1
game_rows:
  count: 1
  result_shape: "single_game_result"
```

Required redaction/privacy flags:

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

## Fixture Rules

Allowed future fixture classes:

- synthetic committed `Player.log` slice authored for this contract;
- sanitized committed fixture only after a separate fixture-promotion review if
  the source began as private evidence.

Forbidden fixture content:

- private Player.log or UTC_Log excerpts;
- live MTGA draft output;
- draft pools;
- submitted decklists;
- deck names;
- draft picks or card choices beyond minimal parser-shape placeholders;
- sideboard choices;
- strategy notes;
- screenshots;
- Manasight or other external raw corpus contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs.

The fixture must be minimal. It should include only lines needed to prove the
contracted draft event and completed game/result behavior.

## Explicit Non-Claims

This contract does not claim:

- draft-with-games behavior support today;
- completed limited gameplay support from `draft_parser_family_v1`;
- game-result evidence from `DraftComplete`;
- match-result evidence from `DraftComplete`;
- completed games from the current GameState anchor;
- draft deck construction truth;
- draft pool truth;
- draft pick quality truth;
- decklist truth;
- sideboard choice truth;
- hidden-card truth;
- archetype truth;
- matchup-plan truth;
- gameplay advice;
- player-mistake labels;
- analytics truth;
- AI truth;
- coaching truth;
- private smoke success;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 / #381 activation.

## Inputs

Allowed inputs:

- repo-owned contracts, handoffs, reports, fixtures, and tests;
- existing synthetic draft parser-family fixture as negative/adjacent evidence;
- existing BO1/BO3 golden replay fixtures as examples of game/match result
  fixture structure;
- existing parser contracts for draft, match state, game state, and game
  result behavior;
- public external taxonomy labels only through already committed corpus parity
  references.

Forbidden inputs:

- private Player.log or UTC_Log files;
- live MTGA draft runs;
- private draft picks, draft pools, decklists, deck names, card choices,
  sideboard choices, strategy notes, screenshots, or private reports;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source, or
  external corpus contents;
- generated/private/runtime artifacts, SQLite files, workbook exports,
  credentials, tokens, API keys, webhook URLs, or local-only artifacts.

## Outputs

Allowed output for this Codex B pass:

- this contract file;
- a workflow handoff to Codex C, if implementation is selected;
- optional future review report.

Future Codex C output, if separately authorized:

- one reduced synthetic fixture;
- one golden replay manifest;
- additive corpus manifest/session-ledger entries;
- focused tests;
- implementation handoff;
- contract-test report.

Forbidden output:

- parser behavior changes;
- parser event class changes;
- current draft fixture mutation unless the contract is looped back;
- private evidence artifacts;
- external corpus artifacts;
- live/private check output;
- readiness claims outside the contracted row.

## Required Guarantees

- `core_gameplay.draft_with_games` is the only scenario family targeted by this
  contract.
- #400 report-only boundary remains a non-claim.
- Current `draft_parser_family_v1` remains draft-only evidence.
- Future uplift requires owned fixture evidence plus `parser_behavior_verified`.
- Future uplift must run through golden replay's normal parser path.
- `DraftComplete` alone must never count as game evidence.
- The existing GameState anchor must never count as completed limited
  gameplay.
- No private or external evidence may be committed.
- #388 and #381 remain deferred.

## Unknowns

- Whether the existing parser can process a reduced synthetic draft-with-games
  fixture without behavior changes.
- Whether the reduced synthetic fixture should use `DraftBot` or `DraftHuman`
  as the draft-event mode.
- Whether match-result evidence should come from match-state final result,
  GRE game result final reconciliation, or both.
- Whether future sanitized private evidence should later add a
  `covered_committed` fixture after separate approval.

## Suspected Gaps

- The current draft fixture is useful but too easy to overread because it has a
  GameState anchor.
- Draft completion is useful but too easy to overread as evidence that games
  were played.
- Existing BO1/BO3 fixtures show game/match flow, but they are not draft
  sessions.
- The parser may not have a durable parser-owned draft-to-match continuity
  concept. This contract permits fixture-level scenario continuity, but not a
  parser claim that draft and match IDs were reconciled unless output proves it.

## Invariants

- `pipeline_activation_ready_for_issue_388` remains false at the observed base.
- `parser_behavior_applicability_ready` remains false at the observed base.
- The new row must not activate #388 or #381.
- The future fixture must be synthetic or sanitized and committable.
- No raw/private/external corpus evidence is committed.
- Corpus metadata remains evidence metadata, not parser truth.

## Error Behavior

If implementation requires parser behavior changes, route back to Codex A/B.

If implementation requires private or live draft evidence, stop and record the
blocked condition. Do not run private/live checks.

If implementation cannot produce game result and match result evidence through
golden replay, keep the row `covered_report_only` and route back.

If implementation would mutate the existing draft-only fixture to become
draft-with-games evidence, route back unless the user explicitly approves that
scope.

If implementation would claim deck construction, draft-pick strategy, decklist,
archetype, analytics, AI, coaching, release, or production truth, stop and
route back to Codex B.

## Side Effects

Contract pass side effect:

- adds `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md`

Future Codex C side effects authorized only if implementation is selected:

- adds one synthetic fixture and one golden replay manifest;
- adds additive manifest/session-ledger entries;
- updates focused tests;
- creates implementation handoff and contract-test report.

No runtime side effects are authorized.

## Dependency Order

1. Preserve the current report-only #400 boundary.
2. Add the reduced synthetic fixture.
3. Add the golden replay manifest and expected reduced parser-owned facts.
4. Verify golden replay passes.
5. Add corpus manifest and session-ledger entries citing this contract.
6. Update focused corpus tests.
7. Write implementation handoff and contract-test report.
8. Route to Codex E review.

## Compatibility

Backward compatibility requirements:

- Existing draft parser tests stay valid.
- Existing `draft_parser_family` golden replay manifest stays valid.
- Existing `draft_with_games_boundary_report_v1` stays visible.
- Existing corpus report schema stays backward compatible.
- Existing readiness metrics may change counts only because the target row
  gains parser-behavior evidence; no status vocabulary changes are authorized.

## Tests Required

For this contract-only pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped checks:

```bash
printf '%s\n' docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Future Codex C must run the same checks and add focused assertions for:

- new golden replay fixture result;
- new manifest/session-ledger entries;
- `core_gameplay.draft_with_games` becomes `covered_synthetic` only after
  parser-behavior evidence exists;
- #400 report-only boundary remains a non-claim;
- current `draft_parser_family` fixture remains draft-only;
- no private/external evidence was committed.

No private/live checks are allowed.

## Acceptance Criteria

- `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md` exists.
- The contract names the minimum evidence required for behavior uplift.
- The contract recommends a reduced synthetic fixture path and defines fallback
  behavior if that path fails.
- The contract distinguishes #400 report-only boundary metadata from behavior
  evidence.
- The contract rejects overclaims from draft-only evidence, `DraftComplete`, and
  the existing GameState anchor.
- The contract defines privacy and fixture boundaries.
- The contract keeps #388 and #381 deferred by default.
- The contract preserves parser truth, private evidence, analytics, AI,
  coaching, readiness, and production non-claims.

## Next Workflow Action

Recommended next role: Codex C: Module Implementer, if the user wants the
synthetic fixture/status uplift implemented next.

If the user wants independent review before implementation, route to Codex E
with this same contract.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #479.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/479

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Latest completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/477

Latest completed PR:
https://github.com/Tahjali11/Mythic-Edge/pull/478

Latest merge commit:
8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0

Prior boundary issue:
https://github.com/Tahjali11/Mythic-Edge/issues/400

Base branch:
main

Contract:
docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md

Goal:
Implement the smallest synthetic fixture, golden replay, corpus manifest/session-ledger, and focused test changes needed to move `core_gameplay.draft_with_games` beyond the #400 report-only boundary only if parser-behavior evidence can be proven through the normal parser path.

Do:
- Compare current behavior against the contract before editing.
- Honor the Behavior-Uplift Packet as a scoped checklist for this row only.
- Preserve `draft_with_games_boundary_report_v1` as report-only non-claim metadata.
- Add a reduced Mythic Edge-owned synthetic completed draft-with-games fixture only if it can honestly prove draft-event evidence plus completed limited game/result flow.
- Add a golden replay manifest for the new fixture.
- Add additive corpus manifest and session-ledger entries citing the contract.
- Update focused corpus and golden replay tests.
- Write `docs/implementation_handoffs/parser_corpus_draft_with_games_behavior_uplift_comparison.md`.
- Write `docs/contract_test_reports/parser_corpus_draft_with_games_behavior_uplift.md`.

Do not:
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, game/match identity, deduplication, diagnostics behavior, golden replay behavior outside fixture registration, feature-equity behavior, evidence-ledger behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, release readiness, production behavior, CI gates, merge readiness, deploy readiness, or final integration policy.
- Mutate the existing draft-only fixture into draft-with-games evidence.
- Run private Player.log, UTC_Log, app-data, live MTGA, draft, network, or private smoke checks.
- Import, copy, mirror, or commit Manasight raw logs or external corpus contents.
- Claim draft-with-games parser support from draft-only fixture, DraftComplete, or GameState anchor evidence.
- Claim draft pick quality, deck construction, decklists, archetypes, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation.

Validation:
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
- `PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py`
- `PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py`
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
- `python3 tools/check_agent_docs.py`
- `python3 -m ruff check src tests tools`
- `git diff --check`
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/479"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/477"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/478"
  previous_merge_commit: "8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #479"
  target_artifact: "docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md"
  verdict: "draft_with_games_behavior_uplift_contract_ready"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-behavior-uplift-479"
  base_branch: "main"
  selected_family: "core_gameplay.draft_with_games"
  current_status: "covered_report_only"
  recommended_status_path: "covered_report_only_to_covered_synthetic_with_parser_behavior_verified"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  parser_behavior_applicability_ready: false
  recommended_after_implementation:
    - "Codex E review / contract test"
    - "Continue one behavior-applicable row at a time under tracker #158"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close tracker #388 or parent #434."
    - "Do not activate #388 or #381."
    - "Do not promote core_gameplay.draft_with_games from report-only without a dedicated fixture, golden replay evidence, and tests."
    - "Do not claim draft-with-games parser support from draft-only fixture, DraftComplete, or GameState anchor evidence."
    - "Do not claim parser support, full corpus parity, private smoke success, release readiness, production behavior, analytics truth, AI truth, coaching truth, or tracker completion."
```
