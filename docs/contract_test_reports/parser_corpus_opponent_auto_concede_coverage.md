# Parser Corpus Opponent Auto-Concede Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/404
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/405
- previous_merge_commit: `e7d5219f04a8c1e29f0daae98e976f6abe904acb`
- contract: `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- branch: `codex/parser-corpus-opponent-auto-concede-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_report_only_boundary`
- risk_tier: High

## Source Snapshot

PR #405 is merged into `codex/parser-parity`, and the local implementation
branch starts at the required merge commit:

- local HEAD before implementation:
  `e7d5219f04a8c1e29f0daae98e976f6abe904acb`
- merge-base ancestry check: passed
- issue #406 state: open
- tracker #158 state: open

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 6
- partial: 3
- missing: 10
- deferred: 0
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- not_applicable: 0

Pre-change opponent auto-concede row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `gameplay_stress.opponent_auto_concede` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only boundary metadata path authorized by the
contract:

- manifest entry: `opponent_auto_concede_boundary_report_v1`
- session ledger entry: `opponent_auto_concede_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- scenario family: `gameplay_stress.opponent_auto_concede`
- coverage status: `covered_report_only`
- coverage basis:
  - `fixture_metadata_only`
- parser event families: none
- parser claim families:
  - `opponent_auto_concede_boundary_report`
  - `normal_game_result_not_auto_concede`
  - `no_action_not_inferred`
  - `concession_intent_not_claimed`
  - `game_end_edge_fixture_required`
  - `gameplay_advice_non_claim`

The committed metadata is a boundary report only. It is not a raw fixture, not
a synthetic gameplay fixture, not a parser behavior claim, and not evidence of
opponent concession intent or hidden opponent action absence.

No parser source, parser behavior, parser event class, router behavior,
diagnostics behavior, golden replay behavior, feature-equity behavior,
evidence-ledger behavior, runtime behavior, workbook behavior, webhook
behavior, Apps Script behavior, analytics behavior, AI behavior, coaching
behavior, CI behavior, merge policy, deploy policy, release policy,
production behavior, raw log fixture, private smoke artifact, generated
artifact, or external corpus content was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 7
- partial: 3
- missing: 9
- deferred: 0
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- not_applicable: 0

Post-change opponent auto-concede and adjacent gameplay-stress rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `gameplay_stress.mulligan` | `covered_committed` | `fixture_metadata_only`, `parser_behavior_verified` | `bo3_sideboard_match_loss` |
| `gameplay_stress.opponent_auto_concede` | `covered_report_only` | `fixture_metadata_only` | `opponent_auto_concede_boundary_report_v1` |
| `gameplay_stress.conjure` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.spellbook` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.companion_or_large_deck` | `missing` | `external_reference_only` | none |
| `gameplay_stress.action_attribution` | `missing` | `external_reference_only` | none |
| `gameplay_stress.event_ordering` | `missing` | `external_reference_only` | none |

The opponent auto-concede row includes this non-claim note:

```text
Opponent auto-concede/no-action coverage is report-only boundary metadata: normal GameResult, local-win, opponent-loss, short-duration, sparse-action, and public-taxonomy evidence do not prove opponent auto-concede or no-action behavior.
```

The session-ledger entry records:

- normal game-result reference entries: 1
- dedicated auto-concede fixtures: 0
- dedicated no-action fixtures: 0
- concession-intent claims: 0
- hidden-action-absence claims: 0
- game rows: 0

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No Manasight raw logs, external corpus content, private local logs, private
  smoke outputs, generated data, SQLite databases, runtime artifacts, failed
  posts, workbook exports, credentials, tokens, API keys, webhook URLs,
  opponent identifiers, private match context, decklists, card choices, or
  strategy notes were committed.
- No parser source, parser event schema, router dispatch, parser state,
  workbook, webhook, Apps Script, analytics, AI, coaching, runtime, CI, merge,
  deploy, release, or production surface was changed.
- `gameplay_stress.mulligan` remains independently covered by existing Bo3
  metadata.
- `gameplay_stress.conjure` and `gameplay_stress.spellbook` remain external
  boundary rows.
- `gameplay_stress.companion_or_large_deck`,
  `gameplay_stress.action_attribution`, and
  `gameplay_stress.event_ordering` remain missing.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from public taxonomy metadata.
- This report does not claim opponent auto-concede behavior.
- This report does not claim no-action behavior.
- This report does not claim concession intent.
- This report does not claim hidden opponent action absence.
- This report does not claim timeout reason or disconnection reason.
- This report does not claim gameplay advice, player-mistake labeling,
  archetype classification, hidden-card inference, decklist inference,
  analytics truth, AI truth, or coaching truth.
- This report does not claim private smoke success.
- This report does not claim runtime health, release readiness, deploy
  readiness, merge readiness, or production readiness.
- This report does not claim issue closure or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The implementation moves only
`gameplay_stress.opponent_auto_concede` from `missing` to
`covered_report_only`, with exact `coverage_basis: ["fixture_metadata_only"]`.
The row is owned only by `opponent_auto_concede_boundary_report_v1`, and
`parser_event_families` is empty.

The session-ledger metadata preserves the required zero-count boundary:

- dedicated auto-concede fixtures: 0
- dedicated no-action fixtures: 0
- concession-intent claims: 0
- hidden-action-absence claims: 0

The row remains report-only boundary metadata. It does not turn normal
`GameResult`, local-win, opponent-loss, short-duration, sparse-action,
`MatchState`, final-reconciliation, or public-taxonomy evidence into
parser-owned opponent auto-concede, no-action, concession-intent, or
hidden-action-absence truth.

Adjacent gameplay-stress rows remain separate:

- `gameplay_stress.mulligan`: `covered_committed`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `gameplay_stress.companion_or_large_deck`: `missing`
- `gameplay_stress.action_attribution`: `missing`
- `gameplay_stress.event_ordering`: `missing`

### Protected-Surface Status

No protected parser or downstream behavior drift was found. Reviewer inspection
found no changes under `src`, `tools`, `.github`, `main.py`,
`live_print_filtered_v11_match_summary.py`,
`tests/test_gre_game_result_parser.py`, `tests/test_gre_game_state_parser.py`,
`tests/test_state.py`, `tests/fixtures/golden_replay`, or parser regression
fixtures.

The changed package is limited to:

- `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- `docs/implementation_handoffs/parser_corpus_opponent_auto_concede_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

### Validation Reviewed

Codex E reran:

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_game_result_parser.py tests/test_state.py`
  - result: 51 passed
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - result: `partial_coverage_map_ready` with 45 families, 6 committed, 9 missing
- `python3 tools/check_agent_docs.py`
  - result: passed with 0 errors and 0 warnings
- `python3 -m ruff check src tests tools`
  - result: passed
- `git diff --check`
  - result: passed
- path-scoped secret/private marker scan for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped protected-surface gate for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped validation selector sanity check for the changed package
  - result: `selection_status: ok`
- `PYTHONPATH=src python3 -m pytest -q`
  - result: 1770 passed

Additional reviewer checks:

- Previous merge commit
  `e7d5219f04a8c1e29f0daae98e976f6abe904acb` is an ancestor of `HEAD`.
- Reviewer manifest inspection confirms only
  `opponent_auto_concede_boundary_report_v1` owns
  `gameplay_stress.opponent_auto_concede`.
- Reviewer corpus matrix inspection confirms
  `gameplay_stress.opponent_auto_concede` is `covered_report_only` with
  `["fixture_metadata_only"]` and
  `["opponent_auto_concede_boundary_report_v1"]`.
- Reviewer session-ledger inspection confirms the required zero dedicated
  auto-concede/no-action/concession-intent/hidden-action counts.
- Reviewer corpus matrix inspection confirms `gameplay_stress.mulligan`,
  `gameplay_stress.conjure`, `gameplay_stress.spellbook`,
  `gameplay_stress.companion_or_large_deck`,
  `gameplay_stress.action_attribution`, and
  `gameplay_stress.event_ordering` remain separately scoped.
- Changed-package ASCII scan produced no findings.
- Generated SQLite/database artifact scan produced no findings.

### Remaining Non-Blocking Gaps

This remains report-only boundary metadata. It does not prove parser support,
synthetic gameplay fixture support, opponent auto-concede behavior, no-action
behavior, concession intent, hidden opponent action absence, timeout reason,
disconnection reason, gameplay advice, player-mistake labeling, archetype
classification, hidden-card inference, decklist inference, analytics truth, AI
truth, coaching truth, private smoke success, release readiness, deploy
readiness, merge readiness, production behavior, full corpus parity, issue
closure, or tracker completion. Future parser-owned support, synthetic
gameplay evidence, private evidence collection, or sanctioned no-action
fixture design requires separate contract authority.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/404"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/405"
  previous_merge_commit: "e7d5219f04a8c1e29f0daae98e976f6abe904acb"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md"
  target_artifact: "draft PR for opponent auto-concede report-only boundary"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-opponent-auto-concede-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_game_result_parser.py tests/test_state.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #406 or tracker #158."
    - "Do not use opponent auto-concede report-only coverage as parser support, concession intent truth, hidden-action truth, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, merge readiness, deploy readiness, production behavior, or tracker-completion authority."
    - "Do not promote gameplay_stress.opponent_auto_concede beyond report-only boundary metadata without separate contract authority."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, runtime behavior, workbook/webhook/App Script/output surfaces, analytics truth, AI truth, coaching truth, CI, or production behavior."
    - "Do not commit raw private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, credentials, webhook URLs, opponent identifiers, private match context, decklists, card choices, strategy notes, or external corpus content."
```
