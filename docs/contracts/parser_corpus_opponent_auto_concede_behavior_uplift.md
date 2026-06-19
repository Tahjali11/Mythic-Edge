# Parser Corpus Opponent Auto-Concede Behavior Uplift Contract

## Module

`gameplay_stress.opponent_auto_concede` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records opponent auto-concede / no-action
games as a report-only boundary from issue #406. This contract defines the
minimum safe evidence required to move that corpus row toward parser-behavior
readiness without claiming opponent intent, hidden-action absence, timeout
reason, disconnection reason, player mistakes, gameplay advice, analytics
truth, AI truth, coaching truth, release readiness, production behavior, or
full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/482
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Latest completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/479
- Latest completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/480
- Latest merge commit: `93ba9f2b9f0a62fee6a78db06b0942cb902d75c7`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
- Prior boundary PR: https://github.com/Tahjali11/Mythic-Edge/pull/407
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-opponent-auto-concede-behavior-uplift-482`
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
- `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_gre_game_result.md`
- `docs/contracts/parser_match_state.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/player_log_evidence_ledger_tier3_game_results.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/golden_replay/*.manifest.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_corpus_parity_report.py`
- `tests/test_golden_replay_harness.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_state.py`

## Purpose

Define whether and how a future implementation may add behavior evidence for
`gameplay_stress.opponent_auto_concede`.

This contract answers:

- what parser-owned observable evidence is required;
- whether a safe synthetic fixture path is approved;
- which existing report-only metadata must remain visible;
- when `parser_behavior_verified` may be added;
- which claims remain forbidden; and
- how #388 / #381 activation stays deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim opponent
auto-concede parser support today.

## Observed Current Behavior

Observed on `main` at
`93ba9f2b9f0a62fee6a78db06b0942cb902d75c7`:

- Issue #482 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #479 is complete after PR #480.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=15, report_only=18, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current applicability metrics:

```yaml
parser_behavior_applicability_ready: false
parser_behavior_applicable_family_count: 37
parser_behavior_applicable_ready_family_count: 20
parser_behavior_applicable_not_ready_family_count: 17
parser_behavior_not_applicable_family_count: 8
```

Current `gameplay_stress.opponent_auto_concede` row:

```yaml
scenario_family: "gameplay_stress.opponent_auto_concede"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "opponent_auto_concede_boundary_report_v1"
notes:
  - "Opponent auto-concede/no-action coverage is report-only boundary metadata: normal GameResult, local-win, opponent-loss, short-duration, sparse-action, and public-taxonomy evidence do not prove opponent auto-concede or no-action behavior."
```

Current parser behavior context:

- GRE game-result parsing can detect `GameStage_GameOver`.
- GRE game-result parsing preserves game-scope `winningTeamId`, `result`, and
  `reason` fields.
- GRE game-result parsing does not promote match-scope results into game
  winners.
- Parser state can reconcile game winners, match winners, match result type,
  and match result reason from parsed events.
- Parser state does not have a first-class opponent auto-concede classifier.
- Existing game-result fixtures prove normal result and reconciliation paths,
  not opponent intent or hidden-action absence.

## Scope Decision

Recommended future path: reduced synthetic early game-end result fixture.

A later Codex C implementation may move
`gameplay_stress.opponent_auto_concede` from `covered_report_only` toward
`covered_synthetic` with `parser_behavior_verified` only if it adds
Mythic Edge-owned synthetic evidence that proves a bounded parser behavior:

1. a minimal match/game context enters the normal parser path;
2. parser-owned GRE game-over/result evidence is emitted;
3. parser-owned state reconciliation records the expected game and match
   result;
4. the fixture contains no private, external, or live MTGA evidence; and
5. every artifact says the proof is a bounded early game-end/result path, not
   concession intent or no-action truth.

This contract does not require waiting for #388 by default. A reduced
synthetic fixture is acceptable because the allowed claim is narrow and
reviewable: Mythic Edge can parse and reconcile a game that ends early with
owned result evidence. The row name remains the existing corpus taxonomy label,
but the parser-behavior proof must be phrased as bounded observable behavior,
not as proof of why the opponent conceded.

Fallback rule:

- If Codex C cannot build an honest reduced synthetic fixture without changing
  parser behavior or smuggling in intent/no-action/private/external evidence,
  the row must remain `covered_report_only` and route back to Codex B or
  Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- GRE game-state and game-result parsers own event detection and result payload
  preservation.
- Match-state parsing owns match-room result payload normalization.
- Parser state owns final game and match reconciliation from parsed events.
- Golden replay owns executing committed synthetic or sanitized fixtures
  through the normal parser path and comparing reduced parser-owned outputs.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, or production surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the producer of game/match facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for the current report-only status:

- `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for any future behavior-ready uplift:

- a future synthetic golden replay fixture and manifest;
- `src/mythic_edge_parser/app/golden_replay.py`;
- GRE game-state, GRE game-result, match-state, and parser-state behavior
  already present in parser code;
- corpus manifest/session-ledger entries that cite this contract;
- the Codex C implementation handoff and Codex E contract-test report.

Truth boundary:

- The corpus row may become behavior-ready only when the normal parser path
  emits the required game/result/reconciliation evidence from owned fixture
  input.
- The corpus row must not claim parser behavior from #406 report-only
  metadata, ordinary game-result fixtures, local-win/opponent-loss facts,
  short game duration, sparse action history, public taxonomy, or missing
  action evidence.
- The corpus row must not claim opponent intent, concession motive, hidden
  action absence, timeout reason, disconnection reason, player mistakes,
  archetype truth, hidden-card truth, decklist truth, gameplay advice,
  analytics truth, AI truth, coaching truth, private smoke success, release
  readiness, production behavior, full corpus parity, tracker completion, or
  #388/#381 activation.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic early game-end replay fixture
  -> normal parser path and parser-owned reduced outputs
  -> golden replay report
  -> corpus manifest/session-ledger behavior evidence
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from replay output.
- Corpus metadata must not force normal result evidence to mean
  auto-concede/no-action/intent truth.
- Corpus metadata must not move gameplay advice, analytics, AI, coaching,
  workbook, webhook, or Apps Script interpretation into parser truth.

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

- `docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- a new synthetic golden replay fixture under `tests/fixtures/`, with an
  obvious opponent-auto-concede or early-game-end name;
- a new golden replay manifest under `tests/fixtures/golden_replay/`;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- `tests/test_golden_replay_harness.py`;
- `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md`;
- `docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md`.

Files Codex C may inspect but must not change unless the implementation
contract is looped back:

- GRE game-state and game-result parser source files;
- match-state parser source files;
- parser state source files;
- existing BO1/BO3/draft golden replay fixtures and manifests;
- focused game-result, game-state, match-state, state, and golden-replay tests.

Not owned by this contract:

- parser semantics;
- game-result or match-state parser behavior;
- parser state final reconciliation;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic fixture and corpus metadata that
make the corpus parity public report show
`gameplay_stress.opponent_auto_concede` as behavior-ready. The intended
eventual corpus row shape is:

```yaml
scenario_family: "gameplay_stress.opponent_auto_concede"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

The existing report-only entry `opponent_auto_concede_boundary_report_v1` must
remain as historical non-claim metadata. A new synthetic evidence entry should
be added rather than rewriting #406's boundary into a behavior claim.

## Minimum Parser-Owned Evidence

Future uplift requires one owned synthetic or sanitized fixture that proves the
following through golden replay.

### Match And Player Context

Required:

- a parser-owned match identity or synthetic match anchor;
- a local player/team context sufficient for parser state to derive player
  result rows;
- a game number, preferably `1` for the reduced V1 fixture;
- no private opponent identifiers or private match context.

Allowed:

- synthetic player names or generic player payloads already accepted by
  existing parser fixtures;
- minimal queue/format fields if needed to keep parser state coherent.

Not sufficient:

- corpus metadata naming the family without a replay fixture;
- a match anchor with no game-over result evidence.

### Early Game-End Result Evidence

Required:

- at least one emitted `GameState` event before or at the game-end boundary;
- at least one emitted paired `GameResult` event from GRE game-over evidence,
  or equivalent existing parser-owned result evidence already accepted by
  golden replay;
- `GameStage_GameOver` evidence on the result-producing game state;
- a game-scope result with a known winner, result type, and result reason;
- parser state records at least one game result;
- final reconciliation exposes the expected game result and match outcome;
- parser-owned game-log rows include exactly the expected reduced game row.

Preferred, if existing parser behavior supports it without code changes:

- a game-scope result reason such as `ResultReason_Concede` or another
  explicit game-end reason string preserved by the parser.

Important boundary:

- Preserving a result reason string is behavior evidence.
- Interpreting that reason as opponent motive, hidden-action absence,
  timeout/disconnect cause, or player mistake truth is forbidden.

Not sufficient:

- local win or opponent loss alone;
- short duration alone;
- sparse action history alone;
- a normal game-result fixture with `ResultReason_Normal`;
- match-scope concession reason without game-scope result evidence;
- missing actions or missing action log rows;
- public taxonomy metadata.

### No-Action / Sparse-Action Boundary

Allowed:

- The fixture may be small enough that the replay contains few gameplay
  actions.
- The manifest/session ledger may say this is a reduced early game-end edge
  fixture.
- The parser may verify the game/result path even when no dedicated gameplay
  action attribution is expected.

Forbidden:

- claiming the opponent took no hidden actions;
- claiming Arena exposed the absence of actions as truth;
- claiming no-action behavior from missing log evidence;
- using action count, turn count, or duration as proof of concession intent.

## Recommended Evidence / Status Path

Recommended Codex C path:

1. Add one new reduced synthetic fixture for one completed early game-end
   scenario.
2. Add one golden replay manifest for that fixture.
3. Assert reduced parser-owned outputs:
   - event family counts;
   - `GameState` / `GameResult` sequencing;
   - game-scope winner/result/reason preservation;
   - parser state final reconciliation;
   - parser-owned match and game rows;
   - unknown/truncation/degradation counts;
   - privacy fields.
4. Add one new corpus manifest entry for the synthetic evidence.
5. Add one new session-ledger entry for the synthetic evidence.
6. Preserve `opponent_auto_concede_boundary_report_v1` as report-only
   non-claim metadata.
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
- status movement based only on #406, ordinary game-result fixtures, public
  taxonomy, local-win/opponent-loss facts, sparse action history, short
  duration, or missing actions.

## Behavior-Uplift Packet

This section is a reusable packet pattern for future behavior-uplift rows. In
this contract it applies only to `gameplay_stress.opponent_auto_concede`. It
must not be used here to solve, promote, or reclassify any other corpus row.

| Question | Contracted answer for #482 |
| --- | --- |
| Scenario family | `gameplay_stress.opponent_auto_concede` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `opponent_auto_concede_boundary_report_v1` |
| Target status, if any | `covered_synthetic` only after owned golden replay evidence exists |
| May `parser_behavior_verified` be added? | Yes, but only to a new synthetic evidence entry after the fixture passes through the normal parser path |
| Evidence type | Synthetic committed fixture preferred; committed sanitized evidence requires a later fixture-promotion issue; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | One new reduced synthetic early game-end fixture and one golden replay manifest are allowed for Codex C; mutating existing normal result fixtures into auto-concede evidence is forbidden |
| Manifest/session-ledger changes | Additive entries citing this contract are allowed for Codex C; changing unrelated rows or removing #406 report-only boundary metadata is forbidden |
| Parser behavior changes | Forbidden; if existing parser behavior cannot support the reduced fixture, route back instead of changing parser behavior |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA checks, Manasight/external raw corpora, opponent identifiers, decklists, strategy notes, and private reports are forbidden |
| Required non-claims | No concession intent, hidden-action absence, timeout reason, disconnection reason, player mistakes, archetype truth, hidden-card truth, decklist truth, gameplay advice, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Corpus parity report/tests, golden replay tests, GRE game-result/game-state parser tests, parser-state tests, docs check, ruff, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; the row may improve readiness counts but does not start the parser-evidence pipeline by itself |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Required Future Manifest Entry Shape

The exact `entry_id` may vary, but future Codex C should prefer:

```yaml
entry_id: "opponent_auto_concede_early_game_end_synthetic_v1"
title: "Opponent auto-concede early game-end synthetic replay"
entry_type: "golden_replay_manifest"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
scenario_families:
  - "gameplay_stress.opponent_auto_concede"
parser_event_families:
  - "MatchState"
  - "GameState"
  - "GameResult"
parser_claim_families:
  - "early_game_end_result_flow"
  - "game_result_reason_preservation"
  - "final_reconciliation_result_flow"
  - "opponent_auto_concede_synthetic_boundary"
  - "concession_intent_non_claim"
  - "hidden_action_absence_non_claim"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/482"
authorized_by_contract: "docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md"
```

Required known-gap language:

- The fixture proves a reduced synthetic early game-end result path only.
- It does not prove opponent intent, real auto-concede behavior, no-action
  truth, timeout cause, disconnect cause, player mistakes, live private Arena
  behavior, gameplay advice, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, or full corpus parity.

## Required Future Session-Ledger Shape

The exact `session_id` may vary, but future Codex C should prefer:

```yaml
session_id: "opponent_auto_concede_early_game_end_synthetic_v1"
title: "Opponent auto-concede early game-end synthetic replay"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/482"
authorized_by_contract: "docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md"
scenario_families:
  - "gameplay_stress.opponent_auto_concede"
format_family: "gameplay_stress"
match_shape: "single_game_early_game_end_synthetic"
record_summary: "synthetic_early_game_end_result_summary"
parser_coverage:
  event_families:
    MatchState: 1
    GameState: 2
    GameResult: 1
  unknown_entries: 0
  truncation_count: 0
  dedicated_auto_concede_fixtures: 1
  dedicated_no_action_fixtures: 0
  early_game_end_result_fixtures: 1
  concession_intent_claims: 0
  hidden_action_absence_claims: 0
  timeout_reason_claims: 0
  disconnection_reason_claims: 0
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
opponent_identifiers_included: false
private_match_context_included: false
decklists_included: false
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
- live MTGA output;
- private opponent identifiers;
- private match context;
- decklists;
- deck names;
- card choices;
- strategy notes;
- screenshots;
- Manasight or other external raw corpus contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs.

The fixture must be minimal. It should include only lines needed to prove the
contracted match context, game-over result evidence, and final reconciliation.

## Explicit Non-Claims

This contract does not claim:

- opponent auto-concede behavior support today;
- opponent intent;
- concession motive;
- hidden action absence;
- no-action truth;
- timeout reason;
- disconnection reason;
- network behavior;
- live Arena behavior;
- private smoke success;
- local win or opponent loss as auto-concede proof;
- short duration as concession proof;
- sparse action history as no-action proof;
- ordinary `GameResult` as auto-concede proof;
- match-scope reason as game-scope auto-concede proof;
- player-mistake labels;
- hidden-card truth;
- decklist truth;
- archetype truth;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 / #381 activation.

## Inputs

Allowed inputs:

- repo-owned contracts, handoffs, reports, fixtures, and tests;
- existing BO1/BO3 golden replay fixtures as examples of game/match result
  fixture structure;
- existing parser contracts for match state, game state, game result, and
  parser state;
- public external taxonomy labels only through already committed corpus
  parity references.

Forbidden inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines from private sources;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- network, firewall, timeout, disconnect, packet, OS/router, or private smoke
  checks;
- exact private paths;
- raw hashes;
- screenshots;
- Manasight raw logs, `.log.gz` files, compressed corpus files, hash lists,
  byte-size lists, capture-date row lists, parser source, or external corpus
  contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, webhook URLs, or local-only
  artifacts.

## Outputs

Codex B output:

- `docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md`

Future Codex C outputs only if implementation proceeds:

- synthetic fixture and golden replay manifest;
- additive corpus manifest/session-ledger entries;
- focused test updates;
- implementation handoff;
- contract-test report.

The public corpus row may become `covered_synthetic` only after the future
fixture passes validation. Until then, the current `covered_report_only` row is
the durable truth.

## Error Behavior

Codex C must stop and route back to Codex B or Codex A if:

- parser behavior changes are needed;
- the only available evidence is a local win, opponent loss, short duration,
  sparse action history, or public taxonomy label;
- the fixture would rely on hidden-action absence;
- the fixture would need private/live/external data;
- the generated report would need to claim opponent intent, timeout reason,
  disconnection reason, network behavior, gameplay advice, analytics truth,
  AI truth, coaching truth, readiness, or production behavior;
- validation would require private/live MTGA checks; or
- adding the row would start #388 or #381 by implication.

## Compatibility Expectations

- Existing corpus parity schema versions remain unchanged.
- Existing report status vocabulary remains unchanged.
- Existing game-result, game-state, match-state, and parser-state behavior
  remains unchanged.
- Existing parser event classes and payload shapes remain unchanged.
- Existing `opponent_auto_concede_boundary_report_v1` metadata remains visible.
- Existing normal gameplay, mulligan, connection, runtime, deck API, drift,
  diagnostics, golden replay, feature-equity, evidence-ledger, analytics,
  workbook, runtime, local app, AI, and production behavior remain unchanged.

## #388 / #381 Activation Semantics

#388 and #381 remain deferred by default.

This row may improve parser-behavior readiness metrics if future Codex C adds
valid synthetic evidence. That improvement must not start #388 or #381 by
itself.

#388 / #381 may start only when:

1. their explicit readiness gate is satisfied by repo-owned metrics and
   contract authority; or
2. a later explicit issue and contract amends the gate and the user explicitly
   approves starting it.

Neither `classification_complete: true`, `missing: 0`, this contract, nor one
new behavior-uplift row is enough.

## Validation Obligations

Codex B validation:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_482_corpus_report.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Future Codex C validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_state.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md \
  docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_golden_replay_harness.py \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md \
  docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_golden_replay_harness.py \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Codex E must verify:

- the synthetic evidence proves only bounded early game-end/result handling;
- `opponent_auto_concede_boundary_report_v1` remains visible and report-only;
- `parser_behavior_verified` appears only on a new synthetic entry;
- no parser behavior changed;
- no private/live/external evidence was committed;
- no row claims opponent intent, hidden action absence, timeout reason,
  disconnection reason, gameplay advice, analytics truth, AI truth, coaching
  truth, readiness, production behavior, full corpus parity, or #388/#381
  activation.

Codex F/G must preserve the same protected boundaries and must not use this
row as release readiness, deploy readiness, production readiness, or
tracker-completion authority.

## Acceptance Criteria

- `docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md`
  exists.
- The contract preserves #406 report-only boundary metadata.
- The contract authorizes only a reduced synthetic early game-end result path.
- The contract forbids parser behavior changes.
- The contract includes the behavior-uplift packet for this row only.
- The contract keeps #388 and #381 deferred.
- The contract includes Codex C validation and stop conditions.

## Open Questions

- Which result reason string should the future synthetic fixture use if
  `ResultReason_Concede` is not representative of real MTGA game-scope
  evidence?
- Should the future fixture prove a local win, local loss, or both? V1 should
  prefer one minimal game unless Codex C finds a reason to route back.
- Should later sanitized evidence replace or supplement the synthetic fixture?
  That requires a separate fixture-promotion issue.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #482, opponent auto-concede behavior uplift planning.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/482

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/479

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/480

Previous merge commit:
93ba9f2b9f0a62fee6a78db06b0942cb902d75c7

Base branch:
main

Contract:
docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md

Goal:
Implement the smallest synthetic fixture, golden replay, corpus manifest/session-ledger, and focused test changes needed to move `gameplay_stress.opponent_auto_concede` beyond the #406 report-only boundary only if bounded parser-behavior evidence can be proven through the normal parser path.

Required scope:
- Compare current repo behavior to the contract before editing.
- Add one reduced synthetic early game-end result fixture only if it can pass through the normal parser path without parser behavior changes.
- Add one golden replay manifest for that fixture.
- Preserve `opponent_auto_concede_boundary_report_v1` as report-only non-claim metadata.
- Add additive corpus manifest and session-ledger entries citing the #482 contract.
- Add focused assertions in `tests/test_corpus_parity_report.py` and `tests/test_golden_replay_harness.py`.
- Write `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md`.
- Write `docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md`.
- Route back to Codex B/A if existing parser behavior cannot support the reduced fixture.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
- PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_state.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

Do not close tracker #158, #388, #434, or #482.
Do not activate #388 or #381.
Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics behavior, drift behavior, feature-equity behavior, evidence-ledger behavior, analytics truth, AI truth, coaching behavior, release readiness, production behavior, CI gates, merge readiness, deploy readiness, or final integration policy.
Do not run private Player.log, UTC_Log, live MTGA, network, timeout, disconnect, or private smoke checks.
Do not import or commit Manasight raw logs, external corpus contents, private logs, generated/runtime artifacts, workbook exports, SQLite files, secrets, credentials, tokens, API keys, webhook URLs, decklists, card choices, strategy notes, screenshots, or private reports.
Do not claim opponent intent, concession motive, hidden-action absence, no-action truth, timeout reason, disconnection reason, network behavior, player mistakes, gameplay advice, analytics truth, AI truth, coaching truth, private smoke success, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation.
Do not promote the row unless a dedicated synthetic fixture, golden replay evidence, corpus metadata, and focused tests satisfy the contract.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/482"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/479"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/480"
  previous_merge_commit: "93ba9f2b9f0a62fee6a78db06b0942cb902d75c7"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_opponent_auto_concede_behavior_uplift_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_opponent_auto_concede_behavior_uplift.md"
  verdict: "opponent_auto_concede_behavior_uplift_contract_ready"
  risk_tier: "High"
  branch: "codex/parser-corpus-opponent-auto-concede-behavior-uplift-482"
  base_branch: "main"
  selected_family: "gameplay_stress.opponent_auto_concede"
  current_status: "covered_report_only"
  recommended_status_path: "covered_report_only_to_covered_synthetic_with_parser_behavior_verified"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_482_corpus_report.json"
    - "python3 tools/check_agent_docs.py"
    - "printf '%s\\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_opponent_auto_concede_behavior_uplift.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
  stop_conditions:
    - "Do not close tracker #158, #388, #434, or #482."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
    - "Do not run private Player.log, UTC_Log, live MTGA, network, timeout, disconnect, or private smoke checks."
    - "Do not commit private logs, external corpus contents, generated/runtime artifacts, workbook exports, SQLite files, secrets, credentials, tokens, API keys, webhook URLs, decklists, card choices, strategy notes, screenshots, or private reports."
    - "Do not claim opponent intent, concession motive, hidden-action absence, no-action truth, timeout reason, disconnection reason, network behavior, player mistakes, gameplay advice, analytics truth, AI truth, coaching truth, private smoke success, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation."
    - "Do not promote gameplay_stress.opponent_auto_concede without a dedicated synthetic fixture, golden replay evidence, corpus metadata, and focused tests satisfying this contract."
```
