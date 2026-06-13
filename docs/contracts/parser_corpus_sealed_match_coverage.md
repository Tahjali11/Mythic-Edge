# Parser Corpus Sealed Match Coverage Contract

## Module

Sealed match corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge move exactly
`core_gameplay.sealed_matches` from missing coverage to safe synthetic metadata
coverage. It proves only that Mythic Edge has repo-owned corpus evidence tying
sealed event context to parser-owned match/game behavior. It does not prove
sealed deckbuilding, sealed pool contents, submitted-deck card content,
decklists, card choices, archetypes, gameplay advice, AI truth, or coaching
truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/359
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/357
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/358
- Previous merge commit: `01234355c9505c4c35c28f6cf56fb0d1d4940cc6`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-sealed-match-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `01234355c9505c4c35c28f6cf56fb0d1d4940cc6`
- target_artifact: `docs/contracts/parser_corpus_sealed_match_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md`
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
- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`
- `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md`
- `docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/event_identity.py`

External reference status:

- Public Manasight metadata may be used only through already merged taxonomy,
  sealed lifecycle, and sealed entry audits or as category-level reference
  context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the sealed match scenario
family. Parser modules and parser state own the underlying match/game
interpretation. The corpus parity report owns only the coverage status claim
that Mythic Edge has safe repo-owned evidence for a sealed match coverage
family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and prior corpus audits, but it is
not a Parser behavior module and is not an analytics, AI, workbook, local app,
or production module.

## Truth Owner

Truth owner for sealed match coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for sealed match parser behavior:

- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`

Truth boundary:

- `event_identity.classify_event_identity(...)` owns sealed event identity
  classification.
- `match_state.try_parse(...)` owns match-state payload extraction, including
  event ID and final match result payload fields.
- GRE `game_state.py` owns GameState payload extraction, including `game_info`
  and identity fields.
- GRE `game_result.py` owns GameResult detection and payload construction from
  GameState GameOver evidence.
- `state.py` and `models.py` own parser-state and model summary facts for
  match/game result and event identity.
- Corpus parity artifacts own the claim that Mythic Edge has safe corpus
  evidence for `core_gameplay.sealed_matches`.
- The sealed match corpus claim is review metadata. It is not parser truth,
  deck-state truth, workbook truth, analytics truth, AI truth, coaching truth,
  merge readiness, deploy readiness, public-release readiness, or
  tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing sealed event identity, match state, GameState, GameResult, and
MatchSummary behavior
  -> synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for core_gameplay.sealed_matches
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change event identity classification.
- Corpus metadata must not change match state parsing, GRE GameState parsing,
  GRE GameResult parsing, parser state final reconciliation, model row shape,
  parser event classes, router semantics, workbook output, analytics, AI,
  coaching, or production behavior.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status artifacts
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

- `docs/contracts/parser_corpus_sealed_match_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_state.py`
- `docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_match_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that is routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- focused parser tests for event identity, match state, GameState, GameResult,
  app models, parser state, and corpus parity

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- router changes
- parser state final reconciliation changes
- golden replay fixtures
- feature-equity baselines
- committed raw log fixtures
- sealed deckbuild fixture work
- submitted-deck card-content fixture work
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public interface remains the existing corpus parity report API:

```python
def build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]:
    ...

def validate_session_ledger(payload: Mapping[str, Any]) -> list[str]:
    ...
```

The contracted report row is the existing `coverage_matrix` entry whose
`scenario_family` is `core_gameplay.sealed_matches`.

No new public Python API is required.

No new CLI flag is required.

No new environment variable is authorized.

## Observed Current Behavior

Observed from `codex/parser-parity` at
`01234355c9505c4c35c28f6cf56fb0d1d4940cc6`:

- Issue #359 is open.
- Tracker #158 is open.
- Issue #357 is closed and PR #358 is merged into `codex/parser-parity`.
- The Mythic Edge corpus parity report is
  `partial_coverage_map_ready`.
- Report summary:
  - total scenario families: 45
  - covered committed: 6
  - covered synthetic: 3
  - covered report-only: 0
  - partial: 3
  - missing: 27
  - deferred: 0
  - blocked private evidence: 0
  - blocked external boundary: 6
  - not applicable: 0
- `core_gameplay.sealed_entry` is currently `covered_synthetic` through
  `sealed_entry_lifecycle_synthetic_v1`.
- `core_gameplay.sealed_deckbuild` is currently `missing` with
  `coverage_basis == ["external_reference_only"]`.
- `core_gameplay.sealed_matches` is currently `missing` with
  `coverage_basis == ["external_reference_only"]`.

Observed parser behavior relevant to this slice:

- `event_identity.classify_event_identity(...)` recognizes event IDs
  containing sealed as limited sealed identity.
- `match_state.try_parse(...)` extracts match ID, event ID, players, raw match
  state, final match reason, and game/match results from match room state
  payloads.
- GRE `game_state.py` builds GameState payloads with `game_info`, identity,
  match state, game number, turn info, and raw GameState preservation.
- GRE `game_result.py` emits GameResult payloads from GameOver GameState
  evidence and selects the latest known game-scope winner for top-level game
  winner fields.
- `state.py` ingests MatchState, GameState, and GameResult events into
  `MatchSummary`, including event ID, `game_info`, game winners, match winner,
  match result type, and match result reason.
- `models.py` exposes normalized event identity and match/game summary fields.
- Current corpus parity data does not yet tie sealed context to match/game
  result behavior in an owned entry.

## Required Guarantees

Codex C may implement the narrow V1 synthetic metadata and focused-test path.

The only authorized status promotion is:

| Scenario family | From | To |
| --- | --- | --- |
| `core_gameplay.sealed_matches` | `missing` | `covered_synthetic` |

Codex C must preserve:

| Scenario family | Required status |
| --- | --- |
| `core_gameplay.sealed_entry` | `covered_synthetic` |
| `core_gameplay.sealed_deckbuild` | `missing` |

The V1 coverage claim must mean only:

- Mythic Edge has a committed synthetic metadata/session-ledger entry for
  sealed match coverage.
- The entry ties sealed event context to existing parser-owned match/game
  behavior.
- Focused tests verify the parser/model path for sealed context plus
  match/game result summary evidence without changing parser behavior.
- The coverage is synthetic review metadata, not committed raw gameplay
  evidence.

The V1 coverage claim must not mean:

- sealed deckbuilding is covered;
- sealed pool contents are covered;
- submitted-deck card contents are covered;
- deck names, deck IDs, card choices, sideboarding quality, archetypes,
  matchup plans, gameplay advice, player mistakes, analytics truth, AI truth,
  or coaching truth are covered;
- Mythic Edge has full corpus parity with Manasight;
- parser behavior changed.

## Coverage Preconditions

`core_gameplay.sealed_matches` may become `covered_synthetic` only when the
synthetic metadata and tests prove all of these parser-owned ingredients:

1. Sealed context:
   - event ID or event identity evidence classifies the match as sealed.
2. Match identity:
   - a match ID and event ID are present through match-state or parser state
     context.
3. GameState identity:
   - GameState evidence can carry match ID, game number, match state, stage,
     `superFormat`, and `matchWinCondition` through `game_info`.
4. Game result evidence:
   - GameResult evidence can record at least one game result in sealed context.
5. Match summary evidence:
   - parser state/model summary can expose sealed event identity together with
     match/game result fields.

Evidence that is not enough by itself:

- public Manasight sealed category labels;
- #357 sealed entry coverage;
- sealed event ID classification alone;
- generic match-state parsing without sealed context;
- a generic limited or draft match fixture;
- manual prose claiming a sealed match was observed.

## Inputs

### Corpus Manifest Entry

Type: JSON object inside `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.

Required V1 entry id:

```text
sealed_match_synthetic_v1
```

Required fields:

```yaml
entry_id: "sealed_match_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/359"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_match_coverage.md"
scenario_families:
  - "core_gameplay.sealed_matches"
parser_event_families:
  - "MatchState"
  - "GameState"
  - "GameResult"
parser_claim_families:
  - "sealed_event_identity"
  - "sealed_match_state"
  - "sealed_game_state"
  - "sealed_game_result"
  - "match_summary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

Allowed `paths` fields may reference only repo-owned metadata, tests, or docs.
Recommended paths:

```yaml
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  event_identity_test: "tests/test_event_identity.py"
  match_state_test: "tests/test_match_state_parser.py"
  game_state_test: "tests/test_gre_game_state_parser.py"
  game_result_test: "tests/test_gre_game_result_parser.py"
  state_summary_test: "tests/test_state.py"
```

The entry must include review notes or known gaps that say sealed match
coverage does not prove sealed deckbuilding, sealed pool contents,
submitted-deck contents, decklists, archetypes, gameplay advice, analytics
truth, AI truth, or coaching truth.

### Session Ledger Entry

Type: JSON object inside `tests/fixtures/parser_corpus/session_ledger.v1.json`.

Required V1 session id:

```text
sealed_match_synthetic_v1
```

Required fields:

```yaml
session_id: "sealed_match_synthetic_v1"
title: "Synthetic sealed match evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/359"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_match_coverage.md"
scenario_families:
  - "core_gameplay.sealed_matches"
format_family: "limited_sealed"
match_shape: "sealed_match_single_game"
record_summary: "synthetic_metadata_summary_only"
parser_coverage:
  event_families:
    MatchState: 1
    GameState: 1
    GameResult: 1
  unknown_entries: 0
  truncation_count: 0
game_rows:
  count: 1
  result_shape: "single_game_result"
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

The session ledger entry must include known gaps stating that this is synthetic
sealed match metadata only.

### Allowed Evidence Classes

- Repo-owned parser source and focused tests.
- Repo-owned corpus manifest and session ledger metadata.
- Synthetic metadata examples that contain no raw log lines.
- Focused synthetic test payloads in tests when they use fake IDs, fake teams,
  and no card/deck/pool contents.
- Public Manasight taxonomy only as category-level reference context through
  prior audits.

### Forbidden Evidence Classes

- Manasight raw logs.
- `.log.gz` files.
- raw session payloads.
- compressed corpus files.
- hash lists, byte-size row lists, capture-date row lists, or mirrored
  external manifest rows.
- copied external parser source.
- private `Player.log` excerpts.
- private local logs.
- raw sealed pool data.
- raw submitted decklists.
- deck names, deck IDs, card choices, or private strategy notes.
- generated data.
- SQLite files.
- runtime artifacts.
- failed delivery artifacts.
- workbook exports.
- credentials, tokens, API keys, or webhook URLs.

## Outputs

### Corpus Parity Report Row

After Codex C implementation, the `core_gameplay.sealed_matches` row should
be:

```yaml
scenario_family: "core_gameplay.sealed_matches"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
mythic_edge_entries:
  - "sealed_match_synthetic_v1"
external_reference_status: "reference_category_not_checked"
```

Notes must include an explicit non-claim similar to:

```text
Synthetic sealed match coverage proves sealed context plus parser-owned match/game result summary metadata only; sealed deckbuild remains missing.
```

The exact note wording may vary, but the non-claim must be present in either
the row notes or the entry review notes and covered by tests.

### Corpus Parity Summary

With the current 45-family taxonomy, adding this entry should update the
summary as follows:

```yaml
covered_committed: 6
covered_synthetic: 4
covered_report_only: 0
partial: 3
missing: 26
deferred: 0
blocked_private_evidence: 0
blocked_external_boundary: 6
not_applicable: 0
```

If the taxonomy changes before Codex C runs, Codex C must update only the
assertions that depend on total family counts and explain the change in the
handoff.

### Required Handoff Artifacts

Codex C must create:

- `docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_match_coverage.md`

The comparison/handoff must summarize:

- observed pre-change corpus status;
- files changed;
- exact coverage status change;
- validation run;
- non-claims for sealed deckbuilding and private deck/card evidence;
- residual risks;
- next recommended role.

## Unknowns

- Whether a future sealed match replay fixture should be sanitized log-based,
  fully synthetic log-based, or remain metadata-only.
- Whether sealed BO3 match coverage needs a separate child after this
  single-game synthetic metadata path.
- Whether future taxonomy work should split sealed matches by BO1, BO3,
  queue, or event phase.

These unknowns do not block the sealed match V1 synthetic metadata path.

## Suspected Gaps

- Current corpus parity fixtures do not replay a sealed match log.
- This V1 entry will be metadata-level coverage, not a golden replay fixture.
- Existing parser tests cover the parser ingredients separately; Codex C should
  add a focused parser/state test tying sealed context to match/game result
  summary behavior.

## Invariants

- Only `core_gameplay.sealed_matches` may move to `covered_synthetic`.
- `core_gameplay.sealed_entry` must remain `covered_synthetic`.
- `core_gameplay.sealed_deckbuild` must remain `missing`.
- Public Manasight metadata remains reference taxonomy only.
- Corpus coverage does not decide parser truth.
- Corpus coverage does not decide match/game truth.
- Corpus coverage does not decide merge readiness, deploy readiness, tracker
  completion, public-release readiness, analytics truth, AI truth, or gameplay
  advice.
- Synthetic sealed match metadata must contain no raw log lines, private
  paths, external corpus contents, decklists, sealed pool contents, card
  choices, or strategy notes.
- Sealed event identity alone is not sealed match coverage.
- #357 sealed entry coverage alone is not sealed match coverage.
- Generic match-state parsing alone is not sealed match coverage.
- Sealed match coverage requires the synthetic metadata entry to connect sealed
  context and parser-owned match/game behavior.

## Error Behavior

Codex C must stop and route back to Codex B if:

- `core_gameplay.sealed_matches` is missing from the taxonomy;
- current corpus validation fails before implementation;
- current sealed match status is already not `missing` and no intervening
  merged contract explains why;
- current sealed entry status is not `covered_synthetic`;
- the manifest/session-ledger schemas reject the required synthetic entry
  shape;
- implementation requires parser behavior changes;
- implementation requires raw external or private log evidence;
- implementation would change sealed deckbuild status;
- implementation would touch protected downstream surfaces.

If a focused test reveals that existing parser behavior does not support the
claimed sealed-context match/game summary path, Codex C must not patch parser
behavior in this slice. It must record the blocker and route to Codex A or
Codex B for a smaller prerequisite.

## Side Effects

Allowed Codex C side effects:

- append one manifest entry to `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- append one session ledger entry to `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- update focused corpus parity tests for the new synthetic row and summary;
- add focused parser/state tests that prove existing sealed-context match/game
  summary behavior without changing parser code;
- write the required implementation handoff and contract test report.

Forbidden Codex C side effects:

- modifying parser source;
- modifying parser event classes;
- modifying router behavior;
- modifying parser state final reconciliation behavior;
- changing sealed deckbuild corpus status;
- adding committed raw log fixtures;
- adding golden replay fixtures;
- adding feature-equity baseline changes;
- writing runtime status artifacts;
- updating workbook, webhook, Apps Script, Google Sheets, analytics, AI,
  coaching, local app, production, CI, merge, deploy, or final integration
  surfaces;
- closing tracker #158.

## Dependency Order

Codex C should work in this order:

1. Verify branch state includes PR #358 merge commit
   `01234355c9505c4c35c28f6cf56fb0d1d4940cc6`.
2. Regenerate the corpus parity report from repo-owned inputs.
3. Confirm sealed entry is `covered_synthetic` and sealed deckbuild plus
   sealed matches are currently `missing`.
4. Add or update the focused parser/state test proving sealed context plus
   match/game result summary behavior without parser code changes.
5. Add the single synthetic manifest entry.
6. Add the matching single synthetic session ledger entry.
7. Update focused corpus parity tests for the sealed match row, summary counts,
   and sealed deckbuild non-claim.
8. Run validation and write the handoff/report artifacts.

## Compatibility

This slice must preserve:

- `SCENARIO_FAMILIES` ordering and values;
- `COVERAGE_STATUSES` vocabulary;
- corpus manifest schema version;
- session ledger schema version;
- corpus parity report schema version;
- current parser event classes;
- current event identity classifier behavior;
- current match state parser behavior;
- current GRE GameState parser behavior;
- current GRE GameResult parser behavior;
- current parser state final reconciliation behavior;
- current workbook/webhook/App Script/output/local app behavior.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_match_state_parser.py tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_models.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If Codex C changes additional files, it must include them in the path-scoped
privacy/protected-surface/selector checks.

Codex E should verify:

- only `core_gameplay.sealed_matches` changed coverage status;
- sealed entry remains `covered_synthetic`;
- sealed deckbuild remains `missing`;
- the new entry is synthetic, committed, and privacy-safe;
- no external/raw/private log artifacts or deck contents were committed;
- parser behavior was not changed;
- focused tests prove existing sealed-context match/game summary behavior;
- corpus report notes preserve the non-claims.

Codex F should stage only reviewed files.

Codex G must not close tracker #158 unless explicitly instructed by the user.

## Acceptance Criteria

- `docs/contracts/parser_corpus_sealed_match_coverage.md` exists.
- The contract names `core_gameplay.sealed_matches` as the only authorized
  status promotion.
- The contract keeps `core_gameplay.sealed_entry` as `covered_synthetic`.
- The contract keeps `core_gameplay.sealed_deckbuild` as `missing`.
- The contract defines the exact synthetic manifest and session ledger entry
  IDs.
- The contract defines coverage preconditions involving sealed context plus
  parser-owned match/game result summary evidence.
- The contract defines allowed and forbidden evidence classes.
- The contract requires no parser behavior changes.
- The contract forbids external/raw/private logs and deck-content artifacts.
- The contract defines validation expectations and a Codex C handoff.

## Open Questions And Contract Risks

- The coverage is synthetic metadata coverage, not replayed sealed match log
  coverage.
- Future sealed deckbuild work will need a separate privacy-sensitive contract.
- Future sealed BO3 coverage may need another child issue if a single-game
  synthetic metadata entry is too narrow for later parity claims.
- The corpus parity report currently derives status from manifest/session
  entries, so non-claims must be visible in notes/tests rather than inferred
  by the report engine.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #359 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/359

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Previous issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/357

  Previous PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/358

  Previous merge commit:
  01234355c9505c4c35c28f6cf56fb0d1d4940cc6

  Branch:
  codex/parser-corpus-sealed-match-coverage

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_sealed_match_coverage.md

  Goal:
  Implement the narrow synthetic metadata/session-ledger slice for
  core_gameplay.sealed_matches. Move only sealed matches from missing to
  covered_synthetic by adding repo-owned synthetic corpus metadata and focused
  tests that tie sealed event context to existing parser-owned match/game
  behavior. Keep sealed entry covered_synthetic and sealed deckbuild missing.

  Do:
    - Verify PR #358 is present in the local branch at or after merge commit
      01234355c9505c4c35c28f6cf56fb0d1d4940cc6.
    - Regenerate the current corpus parity report from repo-owned inputs.
    - Confirm core_gameplay.sealed_entry is covered_synthetic and
      core_gameplay.sealed_deckbuild plus core_gameplay.sealed_matches are
      currently missing before editing.
    - Add or update a focused parser/state test proving existing sealed-context
      match/game result summary behavior without parser source changes.
    - Add exactly one synthetic manifest entry:
      sealed_match_synthetic_v1.
    - Add exactly one synthetic session ledger entry:
      sealed_match_synthetic_v1.
    - Update focused corpus parity tests so sealed matches is
      covered_synthetic, sealed entry remains covered_synthetic, sealed
      deckbuild remains missing, and the summary counts reflect the one-family
      change.
    - Preserve explicit non-claims in notes/tests.
    - Create docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md.
    - Create docs/contract_test_reports/parser_corpus_sealed_match_coverage.md.

  Do not:
    - Implement parser behavior changes.
    - Change event identity, match state, GRE GameState, GRE GameResult,
      parser state, router, parser event classes, match/game identity, or
      deduplication behavior.
    - Change sealed deckbuild corpus status.
    - Add committed raw log fixtures, golden replay fixtures, or feature-equity
      baseline changes.
    - Open a PR.
    - Close tracker #158 or issue #359.
    - Target main directly.
    - Import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw
      session payloads, compressed corpus files, hash lists, byte-size lists,
      capture-date row lists, parser source, or external corpus contents.
    - Commit private Player.log excerpts, private local logs, generated data,
      SQLite files, runtime artifacts, workbook exports, credentials, tokens,
      API keys, webhook URLs, sealed pool data, decklists, deck names, card
      choices, or private strategy notes.
    - Claim full Mythic Edge corpus parity, sealed deckbuild support, sealed
      pool support, decklist support, archetype classification, gameplay
      advice, AI truth, or coaching truth.
    - Change workbook schema, webhook payload shape, Apps Script behavior,
      Google Sheets sync, output transport, analytics truth, AI truth, coaching
      behavior, OpenAI/model-provider behavior, CI gates, merge readiness,
      deploy readiness, production behavior, or final integration policy.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_match_state_parser.py tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_models.py
    - python3 -m ruff check src tests tools
    - python3 tools/check_agent_docs.py
    - git diff --check
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_match_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/359"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/357"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/358"
  previous_merge_commit: "01234355c9505c4c35c28f6cf56fb0d1d4940cc6"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_sealed_match_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_sealed_match_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_sealed_match_coverage.md"
  verdict: "contract_ready_for_synthetic_sealed_match_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-match-coverage"
  base_branch: "codex/parser-parity"
  base_commit: "01234355c9505c4c35c28f6cf56fb0d1d4940cc6"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_match_state_parser.py tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_models.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan against origin/codex/parser-parity"
    - "path-scoped protected-surface gate against origin/codex/parser-parity"
    - "validation selector against origin/codex/parser-parity"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not change event identity, match state, GRE GameState, GRE GameResult, parser state, router, parser event classes, match/game identity, or deduplication behavior."
    - "Do not change sealed deckbuild corpus status."
    - "Do not add committed raw log fixtures, golden replay fixtures, or feature-equity baseline changes."
    - "Do not open a PR."
    - "Do not close tracker #158 or issue #359."
    - "Do not target main directly."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, sealed pool data, decklists, deck names, card choices, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, sealed deckbuild support, sealed pool support, decklist support, archetype classification, gameplay advice, AI truth, or coaching truth."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
```
