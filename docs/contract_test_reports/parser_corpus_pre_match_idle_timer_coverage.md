# Parser Corpus Pre-Match Idle Timer Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/379
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/380
- previous_merge_commit: `8359148957fd9f37399dff6e12a834cf78373e5c`
- contract: `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`
- branch: `codex/parser-corpus-pre-match-idle-timer-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `safe_synthetic_coverage`
- risk_tier: High

## Source Snapshot

PR #380 is present in the local branch:

- required merge commit:
  `8359148957fd9f37399dff6e12a834cf78373e5c`
- local HEAD before implementation: `8359148`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 2
- partial: 3
- missing: 17
- blocked_external_boundary: 6

Pre-change timer rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `timer.active_player_timer` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `active_player_timer_synthetic_v1` |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `timer.pre_match_idle` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `pre_match_idle_timer_synthetic_v1`
- session ledger entry: `pre_match_idle_timer_synthetic_v1`
- scenario family: `timer.pre_match_idle`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families:
  - `GameState`
- parser claim families:
  - `gre_timer_normalization`
  - `pre_match_idle_timer_record`
  - `pre_match_idle_no_direct_seat_boundary`
  - `pre_match_idle_time_unit_boundary`
  - `timer_privacy_boundary`

Added a focused synthetic timer normalization test proving:

- one `TimerType_PreMatchIdle` timer record;
- no direct seat IDs;
- empty contextual turn-info values when no turn info is supplied;
- seconds and milliseconds values are normalized;
- no degradation flags;
- no review-required flag;
- no direct-seat grouping.

No parser source, GRE timer normalization source, GameState payload shape,
diagnostics behavior, golden replay behavior, feature-equity behavior,
evidence-ledger behavior, runtime behavior, workbook behavior, webhook behavior,
Apps Script behavior, analytics behavior, AI behavior, coaching behavior, CI
behavior, merge policy, deploy policy, or production behavior was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 12
- covered_report_only: 2
- partial: 3
- missing: 16
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change timer rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `timer.active_player_timer` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `active_player_timer_synthetic_v1` |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `timer.pre_match_idle` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `pre_match_idle_timer_synthetic_v1` |

The pre-match idle row includes this non-claim note:

```text
Synthetic pre-match idle timer coverage proves parser-owned normalized_timers GameState metadata for a no-direct-seat timer shape only; it does not infer player ownership, inactivity timeout, rope behavior, clock pressure, gameplay advice, analytics, AI, coaching, release, or production truth.
```

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No private logs, external corpus content, runtime artifacts, generated data,
  SQLite databases, workbook exports, failed posts, credentials, tokens, API
  keys, webhook URLs, IP/network traces, decklists, deck names, private reports,
  or private smoke outputs were committed.
- The synthetic timer record is repo-owned metadata/test evidence only.
- The session ledger records summary counts only.
- `timer.inactivity_timeout` remains externally blocked.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from corpus metadata alone.
- This report does not claim live Arena pre-match idle behavior.
- This report does not claim private Player.log timer drift health.
- This report does not claim inactivity timeout coverage.
- This report does not claim rope behavior, clock pressure, player waiting
  behavior, player mistakes, gameplay advice, hidden-card inference, archetype
  classification, analytics truth, AI truth, or coaching truth.
- This report does not claim diagnostics readiness, release readiness, merge
  readiness, deploy readiness, production behavior, issue closure, or tracker
  completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`

## Next Recommended Role

Codex F: Module Submitter.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The #389 implementation matches the safe synthetic coverage contract:

- only `timer.pre_match_idle` moved to `covered_synthetic`;
- the new coverage row uses exactly `fixture_metadata_only` and
  `parser_behavior_verified`;
- `parser_event_families` is exactly `["GameState"]`;
- `pre_match_idle_timer_synthetic_v1` is the only new corpus coverage entry;
- `timer.active_player_timer` remains covered only by
  `active_player_timer_synthetic_v1`;
- `timer.inactivity_timeout` remains `blocked_external_boundary`;
- the focused timer test proves the no-direct-seat, seconds/milliseconds,
  non-degraded, no-seat-grouping boundary;
- the row remains bounded synthetic timer-normalization evidence, not live
  Arena behavior proof.

### Validation Results

- `PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py`:
  13 passed.
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`:
  7 passed.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`:
  `partial_coverage_map_ready (45 families, 6 committed, 16 missing)`.
- Direct report-row inspection confirmed:
  - `timer.active_player_timer`: `covered_synthetic` with
    `active_player_timer_synthetic_v1`;
  - `timer.inactivity_timeout`: `blocked_external_boundary`;
  - `timer.pre_match_idle`: `covered_synthetic` with
    `pre_match_idle_timer_synthetic_v1`.
- `PYTHONPATH=src python3 -m ruff check src tests`: passed.
- `PYTHONPATH=src python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- `python3 tools/check_agent_docs.py`: passed.
- Path-scoped secret/private-marker scan over the #389 package: passed with
  0 forbidden findings and 0 warnings.
- Path-scoped protected-surface gate over the #389 package: passed with
  0 forbidden findings and 0 warnings.
- Path-scoped validation selector over the #389 package: `selection_status: ok`.
- ASCII scan over the #389 package: no non-ASCII output.
- SQLite/database artifact scan: no artifacts found.
- Optional broader validation,
  `PYTHONPATH=src python3 -m pytest -q`: 1769 passed.

### Protected-Surface Status

No protected parser source, GRE timer normalizer source, GameState source,
runtime source, workbook/webhook/App Script surface, generated/private artifact,
raw Player.log excerpt, private report, credential, or external corpus content
changed or was committed. `git diff --name-only -- src tools main.py
live_print_filtered_v11_match_summary.py .github` returned no paths.

The worktree contains only the expected changed #389 package:

- `tests/test_gre_timers_parser.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`
- `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`

### Remaining Risks

- This is synthetic corpus coverage. It does not prove live Arena pre-match
  idle behavior, private smoke success, inactivity-timeout support, rope
  behavior, clock pressure, gameplay advice, player-mistake labels, release
  readiness, analytics truth, AI truth, coaching truth, production behavior,
  full corpus parity, or parser support from corpus metadata alone.
- Future real-world timer payload evidence may need a separate issue and
  contract if it differs from the bounded synthetic no-direct-seat shape.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/380"
  previous_merge_commit: "8359148957fd9f37399dff6e12a834cf78373e5c"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md"
  target_artifact: "draft PR for synthetic pre-match idle timer coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-pre-match-idle-timer-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m ruff check src tests"
    - "PYTHONPATH=src python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private-marker scan over the #389 package"
    - "path-scoped protected-surface gate over the #389 package"
    - "path-scoped validation selector over the #389 package"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #389 or tracker #158."
    - "Do not change parser behavior, GRE timer normalization behavior, GameState payload shape, diagnostics, golden replay, feature-equity, evidence-ledger behavior, runtime, workbook, webhook, Apps Script, analytics, AI, coaching, CI, merge/deploy, release-readiness, or production behavior."
    - "Do not claim live Arena pre-match idle behavior, private smoke success, inactivity-timeout support, rope behavior, clock pressure, gameplay advice, player-mistake labels, release readiness, analytics truth, AI truth, coaching truth, production behavior, full corpus parity, or parser support from corpus metadata alone."
```
