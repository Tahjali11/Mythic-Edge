# Parser Corpus Opponent Auto-Concede Coverage Contract

## Module

Opponent auto-concede / no-action game corpus evidence boundary for the parser
corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`gameplay_stress.opponent_auto_concede` as report-only boundary metadata. It
does not add parser support, committed gameplay fixtures, synthetic gameplay
fixtures, concession classification, hidden-action inference, player-mistake
labeling, gameplay advice, analytics truth, AI truth, coaching truth, release
readiness, production behavior, or full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating normal game-result
evidence as opponent auto-concede or no-action evidence. A local win, opponent
loss, short game, sparse action history, `GameResult`, `MatchState`, final
reconciliation, or public taxonomy category is not enough to claim this
scenario family.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/404
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/405
- Previous merge commit:
  `e7d5219f04a8c1e29f0daae98e976f6abe904acb`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-opponent-auto-concede-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `e7d5219f04a8c1e29f0daae98e976f6abe904acb`
- target_artifact:
  `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md`
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
- `docs/contracts/parser_corpus_firewall_network_drop_coverage.md`
- `docs/contract_test_reports/parser_corpus_firewall_network_drop_coverage.md`
- `docs/implementation_handoffs/parser_corpus_firewall_network_drop_coverage_comparison.md`
- `docs/contracts/parser_gre_game_result.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_match_state.md`
- `docs/contracts/player_log_evidence_ledger_tier3_game_results.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_state.py`
- `tests/fixtures/golden_replay/*.manifest.json`
- `tests/fixtures/parser_regression_*`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, opponent identifiers, private match
  context, decklists, card choices, or strategy notes.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic opponent auto-concede coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, or blocked-private-evidence status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage.

Reasoning:

- Mythic Edge already parses normal game-end evidence through GRE
  `GameResult`, `MatchState`, parser state, and final reconciliation.
- Those parser-owned facts can prove game winners, match winners, game results,
  and game summary rows. They do not prove concession intent, auto-concede
  behavior, hidden opponent action absence, timeout reason, disconnection
  reason, or opponent decision-making.
- Current committed fixtures and parser regression slices contain normal
  game-result evidence, but no dedicated owned auto-concede/no-action fixture.
- A synthetic gameplay fixture would need its own future contract because it
  must define the exact observable evidence that makes the auto-concede or
  no-action claim bounded and not inferential.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic or sanitized evidence; the
  current blocker is not inherently private-only.
- Leaving the row as plain `missing` hides an important inspected boundary:
  normal game results are intentionally not enough for this family.

This decision records `gameplay_stress.opponent_auto_concede` as report-only
boundary metadata. It changes corpus parity metadata and tests only; it does
not change parser behavior or create a dedicated auto-concede fixture.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`gameplay_stress.opponent_auto_concede` scenario family. Parser modules own
observed game-state, game-result, match-state, match/game identity, player/team
relation, and final reconciliation behavior. Corpus parity artifacts own only
the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance evidence
for context, but it is not a Parser behavior module, final-reconciliation
module, diagnostics module, golden replay module, analytics module, AI module,
coaching module, release-readiness module, or production module.

## Truth Owner

Truth owner for `gameplay_stress.opponent_auto_concede` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for parser behavior referenced only as non-claim context:

- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`

Truth boundary:

- Parser modules may say which game or match result was observed.
- Parser state may reconcile observed game/match facts into match summaries.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for opponent auto-concede/no-action coverage.
- Corpus parity must not infer concession intent, auto-concede behavior,
  no-action behavior, hidden opponent action absence, timeout reason,
  disconnection reason, opponent intent, player mistakes, gameplay advice,
  archetypes, hidden cards, decklists, analytics truth, AI truth, coaching
  truth, release readiness, production behavior, or full corpus parity from
  normal result evidence.

Coverage status is review metadata. It is not parser truth, game-result truth,
final-reconciliation truth, analytics truth, AI truth, coaching truth, merge
readiness, deploy readiness, public/private release readiness, or
tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing normal game-result/final-reconciliation behavior and report rows
  -> explicit non-claim boundary metadata
  -> corpus parity row for gameplay_stress.opponent_auto_concede
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change game-result parsing, game-state parsing,
  match-state parsing, parser state final reconciliation, match/game identity,
  event classes, router dispatch, workbook output, analytics, AI, coaching,
  release policy, or production behavior.
- Corpus metadata must not turn a local win, opponent loss, short duration,
  sparse action log, `GameResult`, `MatchState`, final reconciliation, or
  public taxonomy label into an auto-concede/no-action claim.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
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

- `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_state.py`
- existing golden replay manifests and parser regression fixtures

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- router changes
- parser state final reconciliation changes
- match/game identity or deduplication changes
- new concession classifier behavior
- hidden opponent action inference
- player-mistake labeling
- gameplay advice
- archetype, decklist, or hidden-card inference
- analytics, AI, coaching, release, production, or private-smoke truth
- raw private Player.log harvesting
- Manasight raw log import/copy/mirroring
- auto-concede/no-action synthetic fixture claims
- normal game-result coverage changes
- mulligan, Conjure, Spellbook, companion/large-deck, action-attribution, or
  event-ordering corpus coverage work

## Public Interface

The public interface remains the existing corpus parity report API:

```python
build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]
```

The command-line interface remains:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

No new parser function, parser event, router dispatch behavior, parser-state
behavior, workbook field, webhook field, Apps Script field, diagnostics
section, analytics field, AI field, or production behavior is authorized.

## Observed Current Behavior

Observed on `origin/codex/parser-parity` at
`e7d5219f04a8c1e29f0daae98e976f6abe904acb`:

- `gameplay_stress.opponent_auto_concede` is present in the corpus taxonomy.
- The Manasight taxonomy audit maps the public category as
  "Opponent auto-concede or no-action games" and says Mythic Edge needs an
  owned game-end edge fixture.
- The corpus parity report currently shows:

```yaml
scenario_family: "gameplay_stress.opponent_auto_concede"
coverage_status: "missing"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries: []
external_reference_status: "reference_category_not_checked"
notes: []
```

- The current corpus summary is:

```json
{
  "covered_committed": 6,
  "covered_synthetic": 14,
  "covered_report_only": 6,
  "partial": 3,
  "missing": 10,
  "deferred": 0,
  "blocked_private_evidence": 1,
  "blocked_external_boundary": 5,
  "not_applicable": 0
}
```

- Existing committed game-result fixtures and regression slices prove normal
  game-result and match-result behavior only.
- `gameplay_stress.mulligan` is covered by existing Bo3 fixture metadata, but
  that does not prove opponent auto-concede/no-action behavior.
- Current parser contracts define game-over detection, winner extraction, and
  final reconciliation, but do not define auto-concede/no-action
  classification.

## First Bad Value

The first bad value is any row, note, fixture, or test assertion that marks
`gameplay_stress.opponent_auto_concede` as parser-verified because normal
game-result evidence exists.

Examples of bad values:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
parser_claim_families:
  - "game_result"
  - "final_reconciliation"
```

```yaml
notes:
  - "A short local win with sparse actions proves the opponent auto-conceded."
```

The current plain `missing` row is not unsafe, but it is under-specified. The
required improvement is a report-only boundary row that records the inspected
non-claim and future fixture prerequisite.

## Required Guarantees

Future Codex C must make only the smallest coherent corpus metadata/test
changes needed for these guarantees:

- `gameplay_stress.opponent_auto_concede` moves from plain `missing` to
  `covered_report_only`.
- The row uses committed count-only/report metadata only; it does not add a
  committed raw log, committed synthetic gameplay fixture, local private
  artifact, or parser behavior.
- The row's `coverage_basis` is exactly:

```json
["fixture_metadata_only"]
```

- The row's `mythic_edge_entries` includes only:

```json
["opponent_auto_concede_boundary_report_v1"]
```

- The row's notes state that this is a report-only non-claim boundary and that
  normal `GameResult`, local-win, opponent-loss, short-duration, sparse-action,
  and public-taxonomy evidence do not prove auto-concede/no-action behavior.
- `gameplay_stress.mulligan` remains unchanged.
- `gameplay_stress.conjure`, `gameplay_stress.spellbook`,
  `gameplay_stress.companion_or_large_deck`,
  `gameplay_stress.action_attribution`, and
  `gameplay_stress.event_ordering` remain unchanged.
- No parser behavior changes are required or authorized.
- No raw logs, private Player.log excerpts, private smoke outputs, generated
  data, SQLite files, workbook exports, credentials, tokens, keys, webhook
  URLs, opponent identifiers, decklists, card choices, or private match context
  may be committed.

Expected status-summary impact, assuming no unrelated changes:

```json
{
  "covered_committed": 6,
  "covered_synthetic": 14,
  "covered_report_only": 7,
  "partial": 3,
  "missing": 9,
  "deferred": 0,
  "blocked_private_evidence": 1,
  "blocked_external_boundary": 5,
  "not_applicable": 0
}
```

The overall report status remains `partial_coverage_map_ready`.

## Authorized Manifest Entry

Codex C may add this manifest entry shape, adjusting only ordering and wording
needed to match existing fixture style:

```yaml
entry_id: "opponent_auto_concede_boundary_report_v1"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
authorized_by_contract: "docs/contracts/parser_corpus_opponent_auto_concede_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  game_result_contract: "docs/contracts/parser_gre_game_result.md"
  game_result_ledger_contract: "docs/contracts/player_log_evidence_ledger_tier3_game_results.md"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "gameplay_stress.opponent_auto_concede"
parser_event_families: []
parser_claim_families:
  - "opponent_auto_concede_boundary_report"
  - "normal_game_result_not_auto_concede"
  - "no_action_not_inferred"
  - "concession_intent_not_claimed"
  - "game_end_edge_fixture_required"
  - "gameplay_advice_non_claim"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
known_gaps:
  - "Opponent auto-concede coverage is report-only boundary metadata; Mythic Edge has normal game-result and final-reconciliation evidence, but that evidence does not prove auto-concede behavior, no-action behavior, concession intent, hidden opponent actions, timeout reason, disconnection reason, player mistakes, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
review_notes:
  - "Opponent auto-concede/no-action coverage is report-only boundary metadata: normal GameResult, local-win, opponent-loss, short-duration, sparse-action, and public-taxonomy evidence do not prove opponent auto-concede or no-action behavior."
```

## Authorized Session Ledger Entry

Codex C may add this session-ledger entry shape, adjusting only ordering and
wording needed to match existing fixture style:

```yaml
session_id: "opponent_auto_concede_boundary_report_v1"
title: "Opponent auto-concede boundary report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
authorized_by_contract: "docs/contracts/parser_corpus_opponent_auto_concede_coverage.md"
scenario_families:
  - "gameplay_stress.opponent_auto_concede"
format_family: "gameplay_stress"
match_shape: "opponent_auto_concede_boundary_report_only"
record_summary: "committed_opponent_auto_concede_boundary_metadata_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  normal_game_result_reference_entries: 1
  dedicated_auto_concede_fixtures: 0
  dedicated_no_action_fixtures: 0
  concession_intent_claims: 0
  hidden_action_absence_claims: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Report-only opponent auto-concede boundary metadata does not include a dedicated auto-concede/no-action fixture and does not prove concession intent, hidden action absence, timeout reason, disconnection reason, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
report_only_redactions:
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

Dedicated auto-concede fixture, no-action fixture, concession-intent claim, and
hidden-action-absence claim counts must remain zero in this slice.

## Required Report Row

`corpus_parity_report` must report:

```yaml
scenario_family: "gameplay_stress.opponent_auto_concede"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "opponent_auto_concede_boundary_report_v1"
external_reference_status: "reference_category_not_checked"
notes:
  - "Opponent auto-concede/no-action coverage is report-only boundary metadata: normal GameResult, local-win, opponent-loss, short-duration, sparse-action, and public-taxonomy evidence do not prove opponent auto-concede or no-action behavior."
```

## Unknowns

- Whether a future Mythic Edge-owned synthetic fixture can safely represent
  this family without inferring opponent intent.
- Whether a future sanitized fixture can provide enough observable evidence for
  a bounded "no-action game-end edge" claim.
- Whether MTGA exposes a specific concession or inactivity marker that should
  become parser-owned in a future module. This contract does not define one.

## Suspected Gaps

- Current parser behavior has no first-class auto-concede/no-action classifier.
- Current game-result and final-reconciliation fixtures are normal result
  evidence, not auto-concede/no-action evidence.
- Current corpus metadata can explain the boundary but cannot prove support.
- Public Manasight taxonomy can identify the scenario family but cannot prove
  Mythic Edge support.

## Malformed, Private, And External Input Rules

Allowed inputs:

- Existing Mythic Edge docs, contracts, handoffs, reports, source files, and
  focused tests on `codex/parser-parity`.
- Existing corpus manifest and session ledger metadata.
- Existing normal game-result, game-state, match-state, parser-state, golden
  replay, and parser regression artifacts for non-claim context only.
- Public category-level Manasight metadata already represented by the taxonomy
  audit, used only as reference context.

Forbidden inputs:

- Raw private Player.log excerpts.
- Private local logs or private smoke outputs.
- Raw Manasight logs, compressed corpora, session payloads, hash lists,
  byte-size lists, capture-date row lists, parser source, or external corpus
  contents.
- Runtime status files, failed delivery artifacts, generated data, SQLite
  files, workbook exports, decklists, card choices, strategy notes, opponent
  names, account identifiers, local paths, private match context, credentials,
  tokens, keys, or webhook URLs.

Malformed or unknown game-result behavior remains owned by parser contracts
and focused parser tests. Corpus metadata must not accept malformed input as
opponent auto-concede/no-action coverage evidence.

## Compatibility Expectations

- Existing corpus parity schema versions remain unchanged.
- Existing report status vocabulary remains unchanged.
- Existing game-result, game-state, match-state, and parser-state behavior
  remains unchanged.
- Existing parser event classes and payload shapes remain unchanged.
- Existing normal gameplay, mulligan, connection, runtime, deck API, drift,
  diagnostics, golden replay, feature-equity, evidence-ledger, analytics,
  workbook, runtime, local app, AI, and production behavior remain unchanged.

## Validation Obligations

Codex C must run, at minimum:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_game_result_parser.py tests/test_state.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_opponent_auto_concede_coverage.md \
  docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_opponent_auto_concede_coverage.md \
  docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C may also run focused game-state and golden-replay checks for context:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_golden_replay_harness.py
```

Codex E must verify:

- `gameplay_stress.opponent_auto_concede` is `covered_report_only`, not
  `covered_synthetic`, `covered_committed`, or `blocked_private_evidence`.
- The row is exactly scoped to a non-claim boundary and future fixture
  prerequisite.
- Summary counts changed only as expected: `covered_report_only` increases by
  one and `missing` decreases by one.
- `gameplay_stress.mulligan` and the remaining gameplay-stress rows stay
  unchanged.
- No parser source, parser state final reconciliation, event classes, match or
  game identity, deduplication, diagnostics behavior, runtime behavior,
  workbook/webhook/App Script/Sheets behavior, analytics, AI, production, or
  private artifact behavior changed.
- No raw/private/external corpus artifacts were introduced.

Codex F/G must preserve the same protected boundaries and must not use this
boundary row as release readiness, deploy readiness, or tracker-completion
authority.

## Stop Conditions

Stop and route back to Codex B or Codex A if:

- Codex C needs to change parser source, parser state, event payload
  semantics, match/game identity, or final reconciliation.
- Codex C finds an existing owned auto-concede/no-action fixture that might
  justify synthetic coverage instead of report-only boundary metadata.
- The implementation would require a committed raw log, private live smoke
  artifact, external corpus content, opponent identifier, private match
  context, generated data, runtime artifact, SQLite file, workbook export,
  credential, token, key, or webhook URL.
- The implementation would make corpus coverage into concession intent truth,
  hidden-action truth, player-mistake truth, gameplay advice, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, release
  readiness, or tracker-completion authority.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #406, opponent auto-concede/no-action corpus evidence boundary.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/406

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_opponent_auto_concede_coverage.md

Goal:
Implement the smallest metadata/test/report changes needed to move
gameplay_stress.opponent_auto_concede from plain missing to covered_report_only
boundary metadata. Do not change parser behavior.

Required scope:
- Add only the report-only manifest and session-ledger metadata authorized by
  docs/contracts/parser_corpus_opponent_auto_concede_coverage.md.
- Update tests/test_corpus_parity_report.py to assert the new row, required
  non-claims, zero dedicated fixture counts, and expected summary-count shift.
- Preserve gameplay_stress.mulligan and all remaining gameplay-stress rows
  unchanged.
- Produce docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_game_result_parser.py tests/test_state.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_coverage.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_opponent_auto_concede_coverage.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
- python3 -m ruff check src tests tools
- git diff --check

Do not target main.
Do not close tracker #158.
Do not claim full Mythic Edge corpus parity.
Do not claim parser support from public taxonomy metadata alone.
Do not claim opponent auto-concede/no-action support from normal GameResult, local-win, opponent-loss, short-duration, sparse-action, or public-taxonomy evidence alone.
Do not infer concession intent, hidden opponent actions, disconnection reason, timeout reason, player mistakes, archetypes, hidden cards, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior.
Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents.
Do not commit private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, private strategy notes, private reports, opponent identifiers, or private match context.
Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, drift report behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, failed delivery artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy without a new explicit contract.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/404"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/405"
  previous_merge_commit: "e7d5219f04a8c1e29f0daae98e976f6abe904acb"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_opponent_auto_concede_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-opponent-auto-concede-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_game_result_parser.py tests/test_state.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "printf '%s\\n' docs/contracts/parser_corpus_opponent_auto_concede_coverage.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_opponent_auto_concede_coverage.md docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from public taxonomy metadata alone."
    - "Do not claim opponent auto-concede/no-action support from normal GameResult, local-win, opponent-loss, short-duration, sparse-action, or public-taxonomy evidence alone."
    - "Do not infer concession intent, hidden opponent actions, disconnection reason, timeout reason, player mistakes, archetypes, hidden cards, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, card choices, private strategy notes, private reports, opponent identifiers, or private match context."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
