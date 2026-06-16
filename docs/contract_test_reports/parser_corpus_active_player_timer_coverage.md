# Parser Corpus Active Player Timer Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/373
- previous_merge_commit: `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`
- contract: `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- branch: `codex/parser-corpus-active-player-timer-coverage`
- base_branch: `codex/parser-parity`
- report_lifecycle: final_approval
- risk_tier: High

## Source Snapshot

PR #373 is present in the local branch:

- required merge commit:
  `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`
- local HEAD before implementation:
  `41e0c4a`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 10
- covered_report_only: 0
- partial: 3
- missing: 20
- blocked_external_boundary: 6

Pre-change timer rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `timer.active_player_timer` | `missing` | `external_reference_only` | none |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `timer.pre_match_idle` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `active_player_timer_synthetic_v1`
- session ledger entry: `active_player_timer_synthetic_v1`
- scenario family: `timer.active_player_timer`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families:
  - `GameState`
- parser claim families:
  - `gre_timer_normalization`
  - `active_player_timer_record`
  - `active_player_timer_direct_seat_evidence`
  - `timer_turn_info_context_boundary`
  - `timer_time_unit_boundary`
  - `timer_privacy_boundary`

The synthetic entry ties existing GRE timer normalization and GameState
`normalized_timers` behavior into the corpus coverage row. It does not add
raw log fixtures, private runtime reports, actual Player.log timer drift
evidence, external corpus material, or parser source changes.

## Focused Parser Evidence

The focused timer test verifies a clean synthetic active-player timer record:

- collection object `mythic_edge_gre_timers`;
- schema version `parser_gre_timers.v1`;
- stable timer id, type, name, state, and boolean field;
- direct `playerSeatId` evidence;
- direct-seat grouping via `timer_records_by_direct_seat(...)`;
- contextual `turn_info.active_player_seat_id` carried as context only;
- explicit seconds and milliseconds fields normalized by field-name policy;
- no degraded records and no review-required flag.

Existing GameState tests continue to verify additive `normalized_timers`,
preserved raw `timers`, contextual active-player data, and malformed timer
fallback behavior.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 11
- covered_report_only: 0
- partial: 3
- missing: 19
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change timer rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `timer.active_player_timer` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `active_player_timer_synthetic_v1` |
| `timer.inactivity_timeout` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `timer.pre_match_idle` | `missing` | `external_reference_only` | none |

The active-player timer row includes this non-claim note:

```text
Synthetic active player timer coverage proves parser-owned normalized_timers GameState metadata only; it does not infer timer ownership from turn_info context or claim clock-pressure, rope, inactivity-timeout, gameplay-advice, analytics, AI, coaching, release, or production truth.
```

## Privacy And Protected-Surface Assertions

- No parser source behavior changed.
- No GRE timer normalization source, GameState payload construction,
  parser event class, parser state final reconciliation, router semantic,
  diagnostics, golden replay, feature-equity, runtime status, workbook,
  webhook, Apps Script, Google Sheets, analytics, AI, coaching, CI, merge
  policy, deploy policy, or production surface changed.
- No raw log fixture, private Player.log excerpt, private smoke output,
  actual timer payload, local app-data content, local path, runtime artifact,
  workbook export, generated/private artifact, external corpus content, or
  credential was added.
- The synthetic session entry records summary counts only and includes no raw
  log lines, private paths, raw payloads, external logs, decklists, account
  identifiers, machine identifiers, or local report locations.

## Explicit Non-Claims

- This report does not claim inactivity timeout coverage.
- This report does not claim pre-match idle timer coverage.
- This report does not claim Arena rope behavior.
- This report does not claim clock-pressure analytics.
- This report does not claim gameplay advice or player-mistake labels.
- This report does not claim live private Player.log timer drift.
- This report does not claim diagnostics readiness, golden replay readiness,
  feature-equity readiness, release readiness, or production behavior.
- This report does not claim analytics truth, AI truth, coaching truth,
  hidden-card truth, decklist truth, archetype truth, full timer parity, or
  full Mythic Edge corpus parity.
- This report does not decide merge readiness, deploy readiness,
  public/private-release readiness, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`

## Next Recommended Role

Codex E: Module Reviewer.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

No contract mismatches were found. No missing focused tests or safeguards were
identified for the contracted metadata/test-only coverage slice.

Validation caveat: the literal contract-suggested secret/private-marker scan
that includes unchanged `tests/test_gre_game_state_parser.py` reproduces four
pre-existing `raw_player_log_content` findings in that unchanged file. The
seven-file changed-package scan passes with 0 forbidden findings and 0
warnings.

### Contract-Test Verdict

Pass. The package is ready for Codex F: Module Submitter.

The implementation matches the contracted V1 synthetic metadata slice:

- only `timer.active_player_timer` moved from `missing` to
  `covered_synthetic`;
- `timer.inactivity_timeout` remains `blocked_external_boundary`;
- `timer.pre_match_idle` remains `missing`;
- `active_player_timer_synthetic_v1` exists exactly once in the corpus
  manifest and session ledger;
- the manifest entry uses `parser_event_families: ["GameState"]`;
- the parser claim families include GRE timer normalization, active-player
  timer record evidence, direct-seat evidence, turn-info context boundary,
  time-unit boundary, and privacy boundary;
- the session-ledger entry records summary counts only, including one
  normalized timer record, one active-player timer record, one direct-seat
  evidence record, one contextual active-player record, one seconds value, one
  milliseconds value, and zero degraded timer records;
- the focused timer test proves clean direct-seat, seconds, milliseconds, and
  contextual turn-info boundaries through existing parser APIs;
- evidence remains grounded in existing GRE timer normalization and GameState
  `normalized_timers`, while raw `timers` preservation remains existing
  GameState behavior;
- no parser behavior, GRE timer normalization source, GameState payload
  semantics, parser event classes, schema snapshots, diagnostics, golden
  replay, feature-equity, runtime, workbook, webhook, Apps Script, analytics,
  AI, coaching, CI, merge/deploy, or production surface changed;
- no raw/private/external logs, actual timer payloads, local app-data contents,
  local paths, runtime artifacts, private reports, credentials, webhook URLs,
  workbook exports, generated/private artifacts, or external corpus contents
  are committed.

### Validation Results

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
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from mythic_edge_parser.app.corpus_parity_report import build_corpus_parity_report
report = build_corpus_parity_report(
    Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json"),
    session_ledger_path=Path("tests/fixtures/parser_corpus/session_ledger.v1.json"),
)
print(report["status"])
print(report["summary"])
for family in ["timer.active_player_timer", "timer.inactivity_timeout", "timer.pre_match_idle"]:
    row = next(row for row in report["coverage_matrix"] if row["scenario_family"] == family)
    print(family, row)
PY
```

- passed: status `partial_coverage_map_ready`; summary shows 45 families, 6
  committed, 11 synthetic, 19 missing, and 6 blocked external boundary.
- `timer.active_player_timer`: `covered_synthetic` with
  `active_player_timer_synthetic_v1`.
- `timer.inactivity_timeout`: `blocked_external_boundary`.
- `timer.pre_match_idle`: `missing`.

```bash
python3 -m ruff check src tests
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

```bash
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_active_player_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
python3 -m pytest -q
```

- passed: 1768 passed

### Protected-Surface Status

No protected parser/runtime/downstream surfaces changed. The reviewed package
is limited to:

- `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_gre_timers_parser.py`
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`

Live GitHub check during review confirmed:

- issue #375 is open;
- tracker #158 is open;
- issue #372 is closed;
- PR #373 is merged into `codex/parser-parity` with merge commit
  `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`.

Local source-surface check showed no changes under `src`, `tools`, `.github`,
`main.py`, or `live_print_filtered_v11_match_summary.py`.

### Remaining Risks

- This is synthetic parser-timer corpus metadata only, not private Player.log
  smoke evidence or live Arena timer drift proof.
- It does not cover inactivity timeout, pre-match idle timers, rope behavior,
  clock-pressure analytics, player-mistake labels, gameplay advice, release
  readiness, analytics truth, AI truth, coaching truth, production behavior,
  full timer parity, or full Mythic Edge corpus parity.
- The pre-existing raw-log-shaped synthetic strings in unchanged
  `tests/test_gre_game_state_parser.py` still trip the literal
  secret/private-marker scan when that file is included by path; this slice did
  not change that file.

### Next Recommended Role

Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/373"
  previous_merge_commit: "41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md"
  target_artifact: "draft PR for synthetic active-player timer coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-active-player-timer-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m ruff check src tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private-marker scan for the seven reviewed files"
    - "path-scoped protected-surface check for the seven reviewed files"
    - "path-scoped validation selector check for the seven reviewed files"
    - "python3 -m pytest -q"
  validation_caveat:
    - "The literal contract-suggested secret/private-marker scan including unchanged tests/test_gre_game_state_parser.py fails on four pre-existing raw_player_log_content findings in that unchanged file; the seven-file changed-package scan passes cleanly."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #375 or tracker #158."
    - "Do not change parser behavior, GRE timer normalization behavior, GameState payload semantics, raw timers preservation, parser event classes, schema snapshots, router semantics, parser state final reconciliation, match/game identity, deduplication, diagnostics behavior, golden replay behavior, feature-equity behavior, runtime status artifacts, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, release readiness, production behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-delivery artifacts, workbook exports, or local runtime artifacts."
    - "Do not mark timer.inactivity_timeout or timer.pre_match_idle as covered."
    - "Do not claim clock pressure, rope behavior, inactivity timeout, player mistakes, gameplay advice, diagnostics readiness, release readiness, private smoke success, analytics truth, AI truth, coaching truth, full timer parity, or full corpus parity."
    - "Do not commit raw/private/external timer payloads, local app-data contents, external corpus contents, generated databases, runtime status files, local delivery failure artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, or secrets."
```
