# Parser Corpus Active Player Timer Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/375

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_active_player_timer_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_active_player_timer_coverage_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `active_player_timer_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic active-player timer summary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary counts and timer row assertions.
  - Added focused checks for manifest/session shape, parser claim families,
    privacy flags, and adjacent timer non-claims.
- `tests/test_gre_timers_parser.py`
  - Added a focused synthetic clean active-player timer normalization test.
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_active_player_timer_coverage.md`

No parser source, GRE timer normalization source, GameState parser source,
parser event class, schema snapshot, diagnostics, golden replay,
feature-equity, runtime, workbook, webhook, Apps Script, analytics, AI,
coaching, CI, merge/deploy, production, private runtime artifact, raw fixture,
or external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 10
- missing: 20
- `timer.active_player_timer`: `missing`
- `timer.inactivity_timeout`: `blocked_external_boundary`
- `timer.pre_match_idle`: `missing`

This matched the contract's expected starting state after issue #372.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `timer.active_player_timer` | `missing` | `covered_synthetic` |

Preserved the required adjacent-family boundary:

- `timer.inactivity_timeout` remains `blocked_external_boundary`.
- `timer.pre_match_idle` remains `missing`.

Added the required synthetic metadata:

- entry id: `active_player_timer_synthetic_v1`
- session id: `active_player_timer_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families:
  - `GameState`
- parser claim families:
  - `gre_timer_normalization`
  - `active_player_timer_record`
  - `active_player_timer_direct_seat_evidence`
  - `timer_turn_info_context_boundary`
  - `timer_time_unit_boundary`
  - `timer_privacy_boundary`
- coverage basis: `fixture_metadata_only`, `parser_behavior_verified`

The session-ledger validator accepted the contract-required timer summary
fields without schema changes.

## Focused Test Coverage

`tests/test_gre_timers_parser.py` now pins a clean synthetic active-player
timer record with:

- direct `playerSeatId` evidence;
- explicit seconds and milliseconds fields;
- contextual `turn_info.active_player_seat_id`;
- no degraded records;
- no review-required flag;
- direct-seat grouping through `timer_records_by_direct_seat(...)`.

Existing timer and GameState tests continue to cover:

- timer IDs, type/name/state/boolean metadata, malformed input, placeholder
  records, mutation safety, direct-seat grouping, and contextual turn-info
  separation;
- additive `normalized_timers` GameState payload behavior;
- raw `timers` preservation;
- malformed timer-section fallback.

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `active_player_timer_synthetic_v1` manifest entry shape;
- the `active_player_timer_synthetic_v1` session ledger summary counts;
- game-row non-applicability;
- privacy redaction flags;
- report summary movement from 10 to 11 synthetic families and 20 to 19
  missing families;
- the exact `timer.active_player_timer` matrix row;
- `timer.inactivity_timeout` remaining `blocked_external_boundary`;
- `timer.pre_match_idle` remaining `missing`.

## Contract Mismatches

No blocking mismatches were found.

The existing GRE timer and GameState behavior already satisfied most of the
contract. A small focused timer test was added because the previous direct-seat
timer test also carried a deliberately degraded unknown-unit field, while this
contract needs clean non-degraded active-player timer evidence.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future inactivity-timeout, pre-match-idle, clock-pressure, rope, private timer
smoke, release-readiness, analytics, AI, or coaching evidence will require
separate contracts.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata
behavior.

Future timer-family children should not inherit support claims from this
synthetic active-player timer entry.

## Validation Run

```bash
python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
```

- passed: 12 passed

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 19 missing)`

```bash
python3 -m ruff check src tests
```

- passed: all checks passed

```bash
python3 -m ruff check src tests tools
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
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

Validation caveat:

- The literal contract-suggested secret/private-marker scan that also included
  unchanged `tests/test_gre_game_state_parser.py` reproduced four pre-existing
  `raw_player_log_content` findings in that unchanged file.
- The actual changed-package scan, including the new contract, metadata,
  timer test, handoff, and report, passed with 0 forbidden findings and 0
  warnings.

## Open Risks

- This is synthetic metadata coverage only. It does not prove live private
  Player.log timer drift, actual Arena rope behavior, inactivity timeout,
  pre-match idle timers, or clock-pressure analytics.
- The corpus parity report remains `partial_coverage_map_ready`; this package
  does not complete tracker #158.
- External Manasight metadata remains taxonomy/category context only and was
  not imported, copied, mirrored, or committed.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer for issue #375, parser corpus active-player timer coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/373
    - Previous merge commit: 41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83
    - Branch: codex/parser-corpus-active-player-timer-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_active_player_timer_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md

  Goal:
    Review the implementation package against the contract. Confirm that only timer.active_player_timer moved to covered_synthetic and that timer.inactivity_timeout and timer.pre_match_idle remain outside the support claim.

  Review:
    - tests/fixtures/parser_corpus/corpus_manifest.v1.json
    - tests/fixtures/parser_corpus/session_ledger.v1.json
    - tests/test_corpus_parity_report.py
    - tests/test_gre_timers_parser.py
    - docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md
    - docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md

  Do:
    - Verify the branch is based on codex/parser-parity and includes merge commit 41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83.
    - Confirm active_player_timer_synthetic_v1 is the only new corpus coverage entry.
    - Confirm timer.active_player_timer is covered_synthetic with fixture_metadata_only and parser_behavior_verified.
    - Confirm timer.inactivity_timeout remains blocked_external_boundary and timer.pre_match_idle remains missing.
    - Confirm the focused timer test proves clean direct-seat, seconds, milliseconds, and contextual turn-info boundaries without parser behavior changes.
    - Confirm no raw/private/external logs, local artifacts, generated data, workbook exports, credentials, or external corpus contents were committed.
    - Run or inspect validation and produce Codex E findings plus verdict.

  Do not:
    - Implement fixes.
    - Target main directly.
    - Close issue #375 or tracker #158.
    - Change parser behavior, GRE timer normalization behavior, GameState payload semantics, parser event classes, schema snapshots, diagnostics, golden replay, feature-equity, runtime, workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge/deploy, or production behavior.
    - Claim inactivity timeout, pre-match idle, rope, clock-pressure, private Player.log smoke, release readiness, analytics truth, AI truth, coaching truth, or full corpus parity.

  Validation:
    - python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
    - python3 -m pytest -q tests/test_corpus_parity_report.py
    - python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m ruff check src tests
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private-marker scan
    - path-scoped protected-surface gate
    - selector check for the changed package

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/373"
  previous_merge_commit: "41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_active_player_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md"
  verdict: "synthetic_active_player_timer_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-active-player-timer-coverage"
  base_branch: "codex/parser-parity"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/373"
  previous_merge_commit: "41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_active_player_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md"
  verdict: "synthetic_active_player_timer_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-active-player-timer-coverage"
  base_branch: "codex/parser-parity"
```
