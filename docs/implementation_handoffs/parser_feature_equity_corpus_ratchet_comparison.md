# Parser Feature-Equity Corpus Ratchet Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/119

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

## Contract

`docs/contracts/parser_feature_equity_corpus_ratchet.md`

## Role Performed

Codex C: Module Implementer / comparison thread

## Branch And Git Status

- Branch confirmed: `codex/parser-reliability-intelligence`
- Initial status: branch tracking `origin/codex/parser-reliability-intelligence`; only the contract file was untracked before implementation.
- Final status at handoff creation: implementation files are untracked or modified locally and have not been staged.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_golden_replay_harness.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_gre_annotations_parser.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_diff_parser.py`
- `tests/test_opponent_card_observations.py`
- `tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json`
- `tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json`

## Current Behavior Compared To Contract

The repo already had fixture-level golden replay assertions, parser diagnostics, GRE annotation/timer/diff mechanics tests, event schema snapshots, and two committed sanitized golden replay manifests.

The contract gap was real: there was no corpus-level report-only utility that summarizes feature-family coverage across explicit golden replay manifests, compares count-shaped observations to a manually reviewed baseline, and keeps that report out of parser truth ownership.

## Implementation Option Chosen

Implemented the contract's V1 option exactly as a report-only module:

- Consumes explicit golden replay manifest files or manifest directories.
- Expands directories deterministically to `*.manifest.json`.
- Runs golden replay validation and normal parser routing over the manifest fixtures.
- Counts only coverage-shaped observations, paths, and metadata.
- Compares all V1 count sections with exact-match policy.
- Uses a manually maintained count-only baseline.
- Keeps `ok`, `review`, and `diff` non-gating CLI statuses with exit code `0`.
- Uses `fail` only for unsafe/malformed input, invalid baseline, or unreliable report construction.

## Files Changed

- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
- `docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md`

## Exact Sections Changed

`src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`

- Added public constants required by the contract.
- Added `build_feature_equity_corpus_report()`.
- Added `write_feature_equity_corpus_report()`.
- Added `main()`.
- Added deterministic manifest expansion, baseline validation, exact/minimum comparison helpers, parser-routing count collection, privacy/protected-surface report sections, and CLI argument parsing.

`tests/test_feature_equity_corpus_ratchet.py`

- Added focused tests for:
  - committed corpus matching the initial baseline
  - missing baseline -> `review`
  - count mismatch -> report-only `diff` with CLI exit `0`
  - private manifest -> `fail` without raw fixture payload leakage
  - invalid baseline schema -> `fail`
  - explicit report writing only
  - absence of an automatic baseline update CLI option

`tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

- Added the initial manually reviewed count-only baseline for:
  - the two committed golden replay manifests
  - exact-match count sections
  - committed-count-only privacy summary
  - review notes explaining the current positive GameState diff review/degradation counters

## Code Changed

Runtime parser behavior did not change.

New report-only application code was added under `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`. It does not alter parser event classes, parser state final reconciliation, workbook rows, webhook payloads, Apps Script, match/game identity, or deduplication.

## Tests Changed

Focused tests were added in `tests/test_feature_equity_corpus_ratchet.py`.

No existing test file was changed.

## Initial Count-Only Baseline Result

The initial baseline covers two explicit committed golden replay manifests:

- `tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json`
- `tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json`

Report command:

```powershell
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
```

Result:

```text
Feature-equity corpus ratchet: ok (2 manifests, 2 source files)
```

Key observed baseline counts:

- `router_stats.routed`: 13
- `event_family_counts.GameState`: 6
- `event_family_counts.GameResult`: 3
- `event_family_counts.ClientAction`: 3
- `event_family_counts.MatchState`: 2
- `event_family_counts.Rank`: 2
- `payload_type_counts.GameState:game_state_message`: 6
- `parser_claim_counts.final_reconciliation_claims`: 3
- `game_state_evidence_counts.diff_review_required`: 6
- `unknowns_and_degradation.unknown_entries`: 0
- `truncation_and_data_loss.truncation_events`: 0

The six GameState diff review/degradation counters are existing count-shaped evidence from current fixtures missing update-kind evidence. They are recorded in the baseline as coverage shape only; the ratchet does not reinterpret or fix that parser evidence.

## Contract Matches

- Public module path and function names match the contract.
- Report and baseline object/schema constants match the contract.
- Input scope is explicit golden replay manifests only.
- Directory expansion is deterministic and sorted by repo-relative path.
- Missing baseline produces `review`, not `ok`.
- Baseline mismatch produces `diff`, not `fail`.
- Malformed baseline produces `fail`.
- Private manifest metadata produces `fail`.
- CLI exits `0` for `ok`, `review`, and `diff`; exits non-zero for `fail`.
- No automatic baseline update, bless, accept, or environment-refresh path was added.
- Baseline and report contain counts, paths, and metadata only, not raw log lines or full parser payloads.
- Protected-surface self-declaration is included in the report.

## Contract Mismatches

No known contract mismatch remains in the implemented V1 scope.

## Missing Tests Or Safeguards

Not implemented in V1 because the contract defers or excludes them:

- No direct raw Player.log input mode.
- No saved-event replay input mode.
- No local private-log ratchet mode.
- No automatic baseline refresh tooling.
- No CI or merge gate.
- No synthetic extra manifest for broader GRE annotation/timer/diff coverage.
- No full Player.log evidence ledger.

## Validation Run

Completed:

```powershell
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py
# 7 passed

py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py
# 48 passed

py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py
# 41 passed

py -m pytest -q tests\test_event_schema_snapshots.py
# 6 passed

py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
# Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)

py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
# Feature-equity corpus ratchet: ok (2 manifests, 2 source files)

py -m ruff check src tests tools
# All checks passed

git diff --check
# passed

@'
docs/contracts/parser_feature_equity_corpus_ratchet.md
src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
tests/test_feature_equity_corpus_ratchet.py
tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: 5 changed paths, 0 forbidden, 0 warnings

py tools\check_protected_surfaces.py --base origin/main
# passed: 57 branch-diff paths, 0 forbidden, 9 warnings from pre-existing branch changes outside this module's touched paths

rg -n "[ \t]+$" docs\contracts\parser_feature_equity_corpus_ratchet.md src\mythic_edge_parser\app\feature_equity_corpus_ratchet.py tests\test_feature_equity_corpus_ratchet.py tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json docs\implementation_handoffs\parser_feature_equity_corpus_ratchet_comparison.md
# no matches
```

## Protected-Surface Status

The implementation intentionally avoided protected behavior surfaces:

- Parser behavior: not changed
- Parser state final reconciliation: not changed
- Parser event classes or event kind values: not changed
- Match/game identity: not changed
- Deduplication: not changed
- Workbook schema: not changed
- Webhook payload shape: not changed
- Apps Script behavior: not changed
- CI/Pyright gate behavior: not changed
- Production behavior: not changed

## Still Unverified

- Live workbook state
- Deployed Apps Script state
- Production behavior
- Future synthetic manifest behavior beyond the existing focused tests
- Future private local log mode, which is explicitly out of scope
- Full Player.log evidence ledger integration, which is explicitly out of scope

## Forbidden Scope

No forbidden scope was touched. No raw local logs, secrets, credentials, generated card data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, or production behavior were changed.

## Reviewer Focus

Codex E should independently verify:

- Baseline/report schema stability and deterministic path ordering.
- No raw log lines or full payloads appear in the baseline or report.
- The initial baseline is count-only and reviewable.
- `diff` remains report-only and exits `0`.
- Missing baseline -> `review`.
- Invalid/private inputs -> `fail`.
- No hidden baseline update/bless path exists.
- Count sources remain parser/replay observations, not workbook or AI interpretations.

## Next Workflow Action

Next role: Codex E / Module Reviewer / contract-test thread

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #119: parser feature-equity corpus ratchet.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/119

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_feature_equity_corpus_ratchet.md

Implementation handoff:
docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md

Review:
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md
- relevant golden replay and parser diagnostics surfaces

Task:
Review the implementation against the contract. Lead with findings ordered by severity. Verify that the ratchet is report-only, deterministic, count-only, and non-authoritative; that it does not change parser behavior or protected surfaces; and that the initial baseline is safe to review as a count-only fixture.

Focus especially on:
- report schema stability
- baseline schema stability
- deterministic manifest discovery and JSON output
- no raw log lines or full parser payloads in baseline/report
- no automatic baseline update/bless path
- `diff` exits zero and remains report-only
- missing baseline yields `review`
- invalid/private input yields `fail`
- golden replay failures propagate to the ratchet report
- protected surfaces remain untouched

Validation to run:
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py
py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py
py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/parser_feature_equity_corpus_ratchet.md
src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
tests/test_feature_equity_corpus_ratchet.py
tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

Do not:
- change parser behavior
- change parser state final reconciliation
- change parser event classes or event kind values
- change match/game identity or deduplication
- change workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, CI gates, production behavior, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports
- stage, commit, open a PR, close issue #119, or mark tracker #47 complete unless explicitly asked

Final review handoff must include:
- role performed
- issue/tracker
- contract used
- findings first, ordered by severity
- validation run and result
- protected-surface status
- remaining risks
- whether work should route to Codex D, Codex F, or back to Codex B/A
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/119"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/parser_feature_equity_corpus_ratchet.md"
  target_artifact: "docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md"
  implementation_artifacts:
    - "src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py"
    - "tests/test_feature_equity_corpus_ratchet.py"
    - "tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json"
  risk_tier: "Medium"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "py -m pytest -q tests\\test_feature_equity_corpus_ratchet.py -> 7 passed"
    - "py -m pytest -q tests\\test_golden_replay_harness.py tests\\test_parser_diagnostics_mode.py tests\\test_saved_event_replay.py -> 48 passed"
    - "py -m pytest -q tests\\test_gre_game_state_parser.py tests\\test_gre_annotations_parser.py tests\\test_gre_timers_parser.py tests\\test_gre_game_state_diff_parser.py tests\\test_opponent_card_observations.py tests\\test_gsm_truncation_parser.py -> 41 passed"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed"
    - "py -m mythic_edge_parser.app.golden_replay tests\\fixtures\\golden_replay -> pass"
    - "py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\\fixtures\\golden_replay --baseline tests\\fixtures\\feature_equity_corpus\\feature_equity_corpus_baseline.v1.json -> ok"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check for touched files -> passed, 0 forbidden, 0 warnings"
    - "py tools\\check_protected_surfaces.py --base origin/main -> passed with 0 forbidden and 9 warnings from pre-existing branch diff outside this module's touched paths"
    - "direct trailing-whitespace scan over touched files -> no matches"
  remaining_unverified:
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
    - "Future private local log mode"
    - "Full Player.log evidence ledger"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not add automatic baseline refresh or bless behavior."
    - "Do not add CI or merge gates."
    - "Do not commit raw private logs or local reports."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, runtime status files, failed posts, workbook exports, or production behavior."
    - "Do not close issue #119 or tracker #47."
```
