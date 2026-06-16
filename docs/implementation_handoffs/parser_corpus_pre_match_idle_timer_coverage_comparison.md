# Parser Corpus Pre-Match Idle Timer Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/389

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_pre_match_idle_timer_coverage_ready_for_review`

## Files Changed

- `tests/test_gre_timers_parser.py`
  - Added a focused synthetic pre-match idle timer normalization test.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `pre_match_idle_timer_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic pre-match idle timer summary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated synthetic/missing summary counts.
  - Added focused checks for manifest/session shape, parser event family,
    bounded basis, timer non-claims, and adjacent timer rows.
- `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`

No parser source, GRE timer normalizer source, GameState source, diagnostics
source, golden replay source, feature-equity source, evidence-ledger source,
runtime source, workbook export, generated/private artifact, raw fixture,
private log, or external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 2
- partial: 3
- missing: 17
- `timer.active_player_timer`: `covered_synthetic`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `timer.pre_match_idle`: `missing`

This matched the contract's expected starting state after issue #379.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `timer.pre_match_idle` | `missing` | `covered_synthetic` |

Preserved the required adjacent timer boundary:

- `timer.active_player_timer` remains `covered_synthetic` through
  `active_player_timer_synthetic_v1`.
- `timer.inactivity_timeout` remains `blocked_external_boundary`.

Added the required synthetic metadata:

- entry id: `pre_match_idle_timer_synthetic_v1`
- session id: `pre_match_idle_timer_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families: `GameState`
- parser claim families:
  - `gre_timer_normalization`
  - `pre_match_idle_timer_record`
  - `pre_match_idle_no_direct_seat_boundary`
  - `pre_match_idle_time_unit_boundary`
  - `timer_privacy_boundary`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`

The coverage row intentionally does not use `diagnostics_only`,
`evidence_ledger_only`, `count_ratchet_only`, or `external_reference_only`.

## Focused Test Coverage

`tests/test_gre_timers_parser.py` now pins:

- collection object `mythic_edge_gre_timers`;
- schema version `parser_gre_timers.v1`;
- one `TimerType_PreMatchIdle` record;
- no degraded records;
- `review_required is False`;
- timer id `21`;
- no direct seat IDs;
- no contextual active/decision/priority player when no turn info is supplied;
- timer name `PreMatchIdleTimer`;
- timer state `waiting`;
- empty seat fields;
- `running: false`;
- `idleSeconds` normalized as seconds;
- `durationMs` normalized as milliseconds;
- observed/high-confidence/derived evidence;
- no degradation flags;
- `timer_records_by_direct_seat(...) == {}`.

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `pre_match_idle_timer_synthetic_v1` manifest entry shape;
- `parser_event_families: ["GameState"]`;
- exact `covered_synthetic` status and basis;
- session-ledger parser coverage counts:
  - `normalized_timer_records: 1`
  - `pre_match_idle_timer_records: 1`
  - `timer_records_with_direct_seat_evidence: 0`
  - `timer_records_without_direct_seat_evidence: 1`
  - `timer_records_with_contextual_active_player: 0`
  - `timer_records_with_seconds_values: 1`
  - `timer_records_with_milliseconds_values: 1`
  - `timer_degraded_records: 0`
- game-row non-applicability;
- privacy redaction flags;
- report summary movement from 11 to 12 synthetic families and 17 to 16
  missing families;
- the exact `timer.pre_match_idle` matrix row;
- unchanged `timer.active_player_timer` and `timer.inactivity_timeout` rows.

## Contract Mismatches

No blocking mismatches were found.

The selected safe synthetic path was viable without parser behavior changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future coverage for inactivity timeout, live Arena pre-match idle behavior,
private Player.log timer drift, diagnostics readiness, release readiness,
analytics truth, AI truth, coaching truth, or production behavior needs
separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required synthetic metadata
and timer-normalization behavior.

This package does not add private smoke, live log, diagnostics, analytics,
release, or production tests because those claims are outside the contract.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
```

- passed: 13 passed

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 16 missing)`

```bash
PYTHONPATH=src python3 -m ruff check src tests
```

- passed: all checks passed

```bash
PYTHONPATH=src python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed with no output

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

Changed-package path-scoped checks included the untracked Codex B source
contract and the Codex C handoff/report:

```bash
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md
```

- passed: no non-ASCII matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

## Open Risks

- This is synthetic corpus coverage. It does not prove live Arena pre-match
  idle behavior or private Player.log timer drift health.
- It does not cover inactivity timeout, rope behavior, clock pressure, player
  waiting behavior, player mistakes, gameplay advice, analytics truth, AI
  truth, coaching truth, diagnostics readiness, release readiness, production
  behavior, or tracker #158 completion.
- Future private smoke or real-world timer payloads may require a separate
  issue and contract if their shape differs from the bounded synthetic record.
- External Manasight metadata remains taxonomy/category context only and was
  not imported, copied, mirrored, or committed.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #389, parser corpus pre-match idle timer coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/379
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/380
    - Previous merge commit: 8359148957fd9f37399dff6e12a834cf78373e5c
    - Branch: codex/parser-corpus-pre-match-idle-timer-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md
    - Selected path: safe_synthetic_coverage

  Goal:
    Review the implementation package against the contract. Confirm that only timer.pre_match_idle moved to covered_synthetic, that active-player and inactivity-timeout boundaries remain intact, and that the row is bounded synthetic timer-normalization evidence rather than live Arena behavior proof.

  Review:
    - tests/test_gre_timers_parser.py
    - tests/fixtures/parser_corpus/corpus_manifest.v1.json
    - tests/fixtures/parser_corpus/session_ledger.v1.json
    - tests/test_corpus_parity_report.py
    - docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md
    - docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md

  Do:
    - Verify the branch is based on codex/parser-parity and includes merge commit 8359148957fd9f37399dff6e12a834cf78373e5c.
    - Confirm pre_match_idle_timer_synthetic_v1 is the only new corpus coverage entry.
    - Confirm timer.pre_match_idle is covered_synthetic with fixture_metadata_only and parser_behavior_verified basis.
    - Confirm covered_synthetic increased by one and missing decreased by one.
    - Confirm parser_event_families is ["GameState"].
    - Confirm the focused timer test proves no direct seat IDs, seconds and milliseconds values, no degradation, and no seat grouping.
    - Confirm timer.active_player_timer remains covered only by active_player_timer_synthetic_v1.
    - Confirm timer.inactivity_timeout remains blocked_external_boundary.
    - Confirm no parser source, timer normalizer source, GameState source, runtime source, workbook/webhook/App Script surface, generated/private artifact, raw Player.log excerpt, private report, credential, or external corpus content was changed or committed.
    - Run or inspect validation and produce Codex E findings plus verdict.

  Do not:
    - Implement fixes.
    - Target main directly.
    - Close issue #389 or tracker #158.
    - Change parser behavior, GRE timer normalization behavior, GameState payload shape, diagnostics, golden replay, feature-equity, evidence-ledger behavior, runtime, workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge/deploy, release-readiness, or production behavior.
    - Claim live Arena pre-match idle behavior, private smoke success, inactivity-timeout support, rope behavior, clock pressure, gameplay advice, player-mistake labels, release readiness, analytics truth, AI truth, coaching truth, production behavior, full corpus parity, or parser support from corpus metadata alone.

  Validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m ruff check src tests
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private-marker scan
    - path-scoped protected-surface gate
    - selector check for the changed package

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/380"
  previous_merge_commit: "8359148957fd9f37399dff6e12a834cf78373e5c"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md"
  verdict: "synthetic_pre_match_idle_timer_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-pre-match-idle-timer-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/380"
  previous_merge_commit: "8359148957fd9f37399dff6e12a834cf78373e5c"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md"
  verdict: "synthetic_pre_match_idle_timer_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-pre-match-idle-timer-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
```
