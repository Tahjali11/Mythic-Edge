# Player.log Evidence Ledger Tier 7 Derived Analytics Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/173

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md`

## Implementation Under Test

- Branch: `codex/player-log-evidence-ledger-tier7-derived-analytics`
- Base branch: `codex/parser-reliability-intelligence`
- Previous merge commit: `d084512bab464bf5566a84e5dd807a2c6c07b861`
- Handoff: `docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md`

## Findings

No blocking findings remain after the Codex D fixer pass.

### Resolved Prior Blocking Finding: `card_performance` evidence paths did not cover all contracted report facets

`docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md` requires
the broad `card_performance` entry to cover card-performance report metadata,
card identity/display facets, local count/rate facets, and local
co-occurrence/display facets, including `baseline_game_win_rate`,
`seen_in_game_win_rate`, `opening_hand_win_rate`, `cast_win_rate`,
`postboard_cast_win_rate`, `mulliganed_away_win_rate`, `mulligan_tax`,
`top_matchups`, and `top_packages`.

The implementation only records `baseline_game_win_rate` under report metadata
with `allowed_types: ["str", "int"]`, and records a subset of count/rate
facets under `metric_facets` with `allowed_types: ["int", "unknown"]`. It does
not include `opening_hand_win_rate`, `cast_win_rate`,
`postboard_cast_win_rate`, `mulliganed_away_win_rate`, `top_matchups`, or
`top_packages` in the direct evidence `normalized_payload_path`.

Evidence:

- Contract required surfaces:
  `docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md`
  lines 207-212 and 358-369.
- Implemented metadata:
  `src/mythic_edge_parser/app/evidence_ledger.py` lines 7785-7810.
- Actual card-performance payload shape:
  `src/mythic_edge_parser/app/card_performance.py` lines 308-378.

Why this blocks submit: the implementation correctly avoids seeding subfields,
but the broad entry's provenance metadata must still name the contracted
facets it covers. As written, the metadata and tests can pass while omitting
some required analytics facets and under-describing the rate/list-shaped
payloads.

Resolved by Codex D with a metadata/test-only fix. No card-performance
calculation or report-shape behavior changed.

### Codex D Resolution

Resolved by Codex D.

`tier7.derived_analytics_outputs.card_performance` now documents the complete
contracted card-performance facet set across direct evidence paths:

- report metadata, including `baseline_game_win_rate`
- card identity/display facets
- local count/rate facets, including all win-rate fields and `mulligan_tax`
- local co-occurrence/display facets, including `top_matchups` and
  `top_packages`

Focused tests now assert those facets directly and document that current
float-or-empty rate values are represented without changing the ledger
allowed-type vocabulary.

## Contract Summary

Issue #173 seeds Tier 7 derived analytics provenance for exactly two
evidence-ledger fields: `card_performance` and `feature_equity_counts`.

These are downstream derived analytics and report-count outputs. They are not
parser-owned match/game/card/action facts, semantic correctness, no-drift
proof, CI truth, merge readiness, deploy readiness, workbook truth, Apps
Script truth, analytics truth, model-provider truth, AI truth, gameplay
advice, sideboarding recommendations, or player-mistake labels.

## Checks Run

```bash
git status --short --branch
git fetch --prune
gh issue view 173 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body,labels,comments
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md \
  src/mythic_edge_parser/app/evidence_ledger.py \
  tests/test_evidence_ledger.py \
  docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md \
  docs/contract_test_reports/player_log_evidence_ledger_tier7_derived_analytics.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app import evidence_ledger
ledger = evidence_ledger.build_player_log_evidence_ledger()
entries = [e for e in evidence_ledger.iter_ledger_entries() if e["output_family"] == "derived_analytics_outputs"]
print("ledger_errors=", evidence_ledger.validate_player_log_evidence_ledger(ledger))
for entry in entries:
    print(entry["entry_id"], evidence_ledger.validate_ledger_entry(entry))
PY
python3 -m pytest -q
```

## Results

- `python3 -m pytest -q tests/test_evidence_ledger.py` -> `101 passed`
- `python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py` -> `8 passed`
- `python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py` -> `39 passed`
- `python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py` -> `21 passed`
- `python3 -m ruff check src tests tools` -> `All checks passed!`
- `git diff --check` -> passed with no output
- Path-scoped protected-surface check -> `changed_paths: 5`, `forbidden: 0`,
  `warnings: 0`, `result: passed`
- Built-in ledger validation spot-check -> `ledger_errors=[]`; both Tier 7 entries validate cleanly
- `python3 -m pytest -q` -> `960 passed`

## Confirmed Contract Matches

- Tier 7 `derived_analytics_outputs.status` is `seeded_sample`.
- Tier 7 `seed_fields` is exactly `["card_performance", "feature_equity_counts"]`.
- Tier 7 `future_fields` is exactly `[]`.
- The only Tier 7 entry IDs are:
  - `tier7.derived_analytics_outputs.card_performance`
  - `tier7.derived_analytics_outputs.feature_equity_counts`
- `card_performance` remains a broad Tier 7 entry and does not seed separate
  card-performance submetrics.
- `card_performance` references local card-performance report evidence, local
  match/action artifacts, card identity lookup, Tier 3 dependencies, Tier 5
  dependencies, and Tier 6 degradation context.
- `card_performance` notes reject parser fact truth, global performance truth,
  archetype truth, deckbuilding truth, sideboarding advice, gameplay advice,
  player-mistake labels, workbook truth, analytics truth, model-provider
  output, and AI truth.
- `feature_equity_counts` references feature-equity report metadata, manifest
  metadata, count sections, golden replay reports, baseline comparison,
  privacy/protected-surface sections, and Tier 6 degradation context.
- `feature_equity_counts` remains report-only corpus-count evidence; `ok`
  status is documented as not semantic correctness, no-drift proof, CI truth,
  merge readiness, deploy readiness, workbook truth, analytics truth,
  model-provider output, or AI truth.
- No forbidden Tier 7 fields are seeded.
- Built-in ledger and Tier 7 entries validate cleanly.
- Privacy classes for Tier 7 evidence signals remain `path_only_no_values`.

## Contract Mismatches

None remaining.

Resolved: Codex D expanded `card_performance` direct evidence paths to cover
the complete contracted facet set. No remaining blocking mismatches found in
the local fixer pass.

## Missing Tests

Resolved missing focused test coverage:

- `tests/test_evidence_ledger.py` now asserts that the `card_performance`
  evidence paths include all contracted report metadata, card
  identity/display, local count/rate, and co-occurrence/display facets.
- The focused tests now catch omission of win-rate fields, `mulligan_tax`,
  `top_matchups`, `top_packages`, and the current rate/list facet
  type-description limitation.

## Drift Notes

- Repo drift: prior metadata/test mismatch resolved in reviewed scope.
- Workbook drift: none found; workbook schema and exports were not changed.
- Deployment drift: none found; no CI, merge/deploy policy, production
  behavior, Apps Script, or webhook behavior changed.
- Local-data drift: none found; no raw logs, runtime artifacts, failed posts,
  generated data, workbook exports, secrets, or local runtime artifacts were
  added.
- Issue/tracker drift: issue #173 is open; tracker #11 remains open as
  expected.

## Protected-Surface Status

Clean for behavior surfaces. The reviewed diff is limited to the expected
contract, evidence-ledger metadata, focused evidence-ledger tests, and
implementation handoff. No card-performance calculations, feature-equity
behavior, golden replay behavior, diagnostics behavior, drift behavior, parser
behavior, router behavior, runtime artifacts, workbook schema, webhook payload
shape, Apps Script behavior, analytics truth, AI truth, CI gates,
merge/deploy policy, production behavior, secrets, raw logs, generated data,
runtime status files, failed posts, or workbook exports changed.

## Remaining Risks

- GitHub Actions were not run locally.
- Runtime field-evidence attachment remains deferred.
- Schema snapshot and invariant execution remain deferred.
- Tier 7 entries document derived report provenance only; they do not validate
  semantic analytics correctness.

## Recommendation

Approve.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #173, Tier 7 derived analytics provenance under tracker #11.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/173

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Base branch:
codex/parser-reliability-intelligence

Implementation branch:
codex/player-log-evidence-ledger-tier7-derived-analytics

Reviewed artifacts:
- docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md
docs/contract_test_reports/player_log_evidence_ledger_tier7_derived_analytics.md

Codex E verdict:
No blocking findings remain after the Codex D fixer pass. The prior card_performance facet-coverage gap is resolved. The Tier 7 derived analytics implementation is metadata/test-only, seeds exactly card_performance and feature_equity_counts, preserves analytics as downstream/report provenance, and does not change protected parser/runtime/workbook/webhook/App Script/analytics/AI behavior.

Validation reviewed:
- python3 -m pytest -q tests/test_evidence_ledger.py -> 101 passed
- python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py -> 8 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 39 passed
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py -> 21 passed
- python3 -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface check -> passed
- python3 -m pytest -q -> 960 passed

Submitter task:
- Inspect git status.
- Stage only the reviewed issue #173 files.
- Commit with an issue-linked message.
- Push the implementation branch.
- Open or update a draft PR targeting codex/parser-reliability-intelligence, not main.
- Do not merge, close issue #173, close tracker #11, or mark tracker #11 complete.

Do not:
- Target main directly.
- Stage unrelated files.
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, schema snapshots, invariant execution, golden replay behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, archetype classification behavior, CI gates, merge/deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Add Tier 7 seed fields beyond card_performance and feature_equity_counts.
- Infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/173"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/171"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/172"
  previous_merge_commit: "d084512bab464bf5566a84e5dd807a2c6c07b861"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md; docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md; docs/contract_test_reports/player_log_evidence_ledger_tier7_derived_analytics.md"
  target_artifact: "Codex F draft PR submission for issue #173"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier7-derived-analytics"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 101 passed"
    - "python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py -> 8 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 39 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py -> 21 passed"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, changed_paths 5, forbidden 0, warnings 0"
    - "built-in ledger validation spot-check -> ledger_errors=[], Tier 7 entries validate cleanly"
    - "python3 -m pytest -q -> 960 passed"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not merge, close issue #173, close tracker #11, or mark tracker #11 complete."
    - "Do not stage unrelated files."
    - "Do not change protected parser/runtime/workbook/webhook/App Script/analytics/AI behavior."
```
