# Parser Corpus Draft With Games Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/400

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_draft_with_games_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`draft_with_games_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `draft_with_games_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching report-only draft-with-games boundary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated report-only/missing summary counts.
  - Added focused checks for manifest/session shape, empty parser event
    families, `fixture_metadata_only` basis, draft-with-games non-claims,
    redaction flags, and unchanged `core_gameplay.draft_only` status.
- `docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_draft_with_games_coverage.md`

No draft fixture log, golden replay manifest, parser source, parser tests
outside corpus parity, draft parser behavior, parser event classes, router
semantics, parser state final reconciliation, game-result behavior,
match-result behavior, diagnostics source, feature-equity source,
evidence-ledger source, runtime source, workbook export, generated/private
artifact, raw fixture, private log, draft picks, sealed or draft pools,
decklists, deck names, card choices, sideboard choices, strategy notes, or
external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 5
- partial: 3
- missing: 12
- `core_gameplay.draft_only`: `covered_synthetic`
- `core_gameplay.draft_with_games`: `missing`

This matched the contract's expected starting state after issue #398.

Repo inspection confirmed the current `draft_parser_family` entry is scoped to
`core_gameplay.draft_only`, with `known_gaps: ["draft_with_games"]`. The
session ledger has `match_shape == "draft_only"`, `game_rows.count == 0`, and
`game_rows.result_shape == "not_applicable"`. The golden replay manifest
includes `DraftBot`, `DraftHuman`, `DraftComplete`, and a GameState anchor,
but no completed limited game rows, game-result evidence, match-result
evidence, or completed draft session continuity.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `core_gameplay.draft_with_games` | `missing` | `covered_report_only` |

Preserved the required adjacent draft boundary:

- `core_gameplay.draft_only` remains `covered_synthetic` through
  `draft_parser_family`.
- The current draft fixture log is unchanged.
- The current draft golden replay manifest is unchanged.
- `DraftBot`, `DraftHuman`, and `DraftComplete` parser behavior is unchanged.

Added the required report-only metadata:

- entry id: `draft_with_games_boundary_report_v1`
- session id: `draft_with_games_boundary_report_v1`
- source kind: `committed_count_only_report`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- parser event families: none
- parser claim families:
  - `draft_with_games_boundary_report`
  - `draft_only_reference_only`
  - `draft_parser_family_not_completed_games`
  - `limited_game_result_evidence_not_claimed`
  - `draft_privacy_boundary`
- coverage basis:
  - `fixture_metadata_only`

The coverage row intentionally does not use `parser_behavior_verified`,
`diagnostics_only`, `evidence_ledger_only`, `count_ratchet_only`, or
`external_reference_only`.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `draft_with_games_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and `fixture_metadata_only` basis;
- absence of `parser_behavior_verified` from the draft-with-games boundary row;
- required known-gap and review-note non-claims;
- session-ledger parser coverage counts:
  - `event_families: {}`
  - `unknown_entries: 0`
  - `truncation_count: 0`
  - `draft_only_reference_entries: 1`
  - `draft_parser_family_reference_entries: 1`
  - `completed_draft_game_rows: 0`
  - `game_result_events: 0`
  - `match_result_events: 0`
  - `dedicated_draft_with_games_fixtures: 0`
- game-row non-applicability;
- privacy redaction flags, including no draft picks, draft pools, decklists,
  private deck names, card choices, or strategy notes;
- report summary movement from 5 to 6 report-only families and 12 to 11
  missing families;
- the exact `core_gameplay.draft_with_games` matrix row;
- unchanged `core_gameplay.draft_only` matrix row.

## Contract Mismatches

No blocking mismatches were found.

The selected report-only boundary path was viable without parser behavior,
draft fixture, golden replay manifest, or parser test changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future coverage for a completed draft-with-games fixture, limited gameplay,
game-result evidence, match-result evidence, draft deck construction, private
draft logs, draft picks, draft pools, decklists, deck names, card choices,
sideboard choices, strategy notes, diagnostics readiness, release readiness,
analytics truth, AI truth, coaching truth, or production behavior needs
separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required report-only metadata
and boundary assertions.

This package does not add parser behavior tests, private smoke, live log,
diagnostics, analytics, release, or production tests because those claims are
outside the contract.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
```

- passed: 13 passed

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
```

- passed: 115 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 11 missing)`

```bash
PYTHONPATH=src python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
for f in docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md; do git diff --no-index --check /dev/null "$f"; rc=$?; if [ "$rc" -eq 1 ]; then true; elif [ "$rc" -ne 0 ]; then exit "$rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_draft_with_games_coverage.md docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/fixtures/draft_parser_family_slice.log tests/fixtures/golden_replay/draft_parser_family.manifest.json tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/source, draft fixture, golden replay manifest, tools, app entrypoint, or CI paths changed

## Open Risks

- `core_gameplay.draft_with_games` is intentionally `covered_report_only`; this
  does not prove completed draft-with-games fixture support.
- `DraftBot`, `DraftHuman`, `DraftComplete`, and the synthetic GameState anchor
  remain draft-only reference evidence for this row.
- Future dedicated coverage remains blocked until Mythic Edge has owned,
  sanitized, parser-supported evidence for a completed draft session with
  games and results.
- Tracker #158 remains open.

## Next Recommended Role

Codex E: Module Reviewer / Contract-Test Reviewer.

Codex E should verify that the package is metadata/test/report-only, that
`core_gameplay.draft_with_games` moved only to `covered_report_only`, that
`coverage_basis` is exactly `["fixture_metadata_only"]`, and that draft-only
evidence was not promoted to completed draft-with-games parser truth.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer / Contract-Test Reviewer for issue #400,
  parser corpus draft-with-games report-only boundary coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/398
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/399
    - Previous merge commit: 5a512507b262eac468d80e283b5afcb2099452ad
    - Branch: codex/parser-corpus-draft-with-games-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_draft_with_games_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md

  Goal:
    Review the Codex C implementation against the contract. Confirm whether the
    package is ready for Codex F submission without overclaiming parser support.

  Review:
    - Confirm `core_gameplay.draft_with_games` moved from `missing` to
      `covered_report_only` only.
    - Confirm `coverage_basis` is exactly `["fixture_metadata_only"]`.
    - Confirm `parser_event_families` is empty and no
      `parser_behavior_verified` basis is used for draft-with-games.
    - Confirm the current draft-only fixture, DraftBot, DraftHuman,
      DraftComplete, and synthetic GameState anchor remain reference-only and
      are not completed draft-with-games parser truth.
    - Confirm `core_gameplay.draft_only` remains `covered_synthetic`.
    - Confirm the draft fixture log and golden replay manifest are unchanged.
    - Confirm no parser behavior, parser state, parser event classes, runtime,
      workbook, webhook, Apps Script, analytics, AI/coaching, generated/private
      artifacts, raw logs, private draft evidence, or external corpus content
      changed.
    - Rerun focused validation and record the verdict in the report/handoff if
      appropriate.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
    - PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private marker scan for changed files
    - path-scoped protected-surface check for changed files
    - path-scoped selector sanity check for changed files

  Do not:
    - Target main directly.
    - Close #400 or tracker #158 unless separately authorized.
    - Add parser behavior, parser event classes, runtime behavior, workbook,
      webhook, Apps Script, analytics, AI/coaching, CI, generated/private
      artifacts, raw logs, private draft evidence, or external corpus content.
    - Promote draft-only fixture, DraftBot, DraftHuman, DraftComplete, or
      GameState anchor evidence into completed draft-with-games support.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/399"
  previous_merge_commit: "5a512507b262eac468d80e283b5afcb2099452ad"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_draft_with_games_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md"
  verdict: "draft_with_games_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/399"
  previous_merge_commit: "5a512507b262eac468d80e283b5afcb2099452ad"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_draft_with_games_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_draft_with_games_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_draft_with_games_coverage.md"
  verdict: "draft_with_games_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
