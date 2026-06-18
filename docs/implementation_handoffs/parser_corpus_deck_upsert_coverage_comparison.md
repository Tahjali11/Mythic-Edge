# Parser Corpus Deck Upsert Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/396

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_deck_upsert_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`deck_upsert_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `deck_upsert_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching report-only deck-upsert boundary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated report-only/missing summary counts.
  - Added focused checks for manifest/session shape, empty parser event
    families, `fixture_metadata_only` basis, deck-upsert non-claims, and
    adjacent deck API rows.
- `docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_deck_upsert_coverage.md`

No parser source, parser tests outside corpus parity, client-action parser
behavior, parser event classes, router semantics, parser state final
reconciliation, diagnostics source, golden replay source, feature-equity
source, evidence-ledger source, runtime source, workbook export,
generated/private artifact, raw fixture, private log, private decklist, private
deck name, private collection data, or external corpus content was added or
changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 3
- partial: 3
- missing: 14
- `deck_api.start_hook_deck_snapshot`: `covered_synthetic`
- `deck_api.deck_summary`: `covered_report_only`
- `deck_api.deck_upsert`: `missing`
- `deck_api.event_set_deck`: `covered_committed`
- `deck_api.store_pack_inbox_or_crafting`: `missing`

This matched the contract's expected starting state after issue #394.

Repo inspection confirmed no dedicated deck-upsert parser surface was present.
The nearby `deck_api.event_set_deck`, deck-summary boundary, StartHook deck
snapshot, submit-deck response, and submitted-deck-card provenance surfaces
remain separate evidence families.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `deck_api.deck_upsert` | `missing` | `covered_report_only` |

Preserved the required adjacent deck API boundary:

- `deck_api.start_hook_deck_snapshot` remains `covered_synthetic` through
  `start_hook_deck_snapshot_synthetic_v1`.
- `deck_api.deck_summary` remains `covered_report_only` through
  `deck_summary_boundary_report_v1`.
- `deck_api.event_set_deck` remains `covered_committed` through
  `bo1_match_win_basic`.
- `deck_api.store_pack_inbox_or_crafting` remains `missing`.

Added the required report-only metadata:

- entry id: `deck_upsert_boundary_report_v1`
- session id: `deck_upsert_boundary_report_v1`
- source kind: `committed_count_only_report`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- parser event families: none
- parser claim families:
  - `deck_upsert_boundary_report`
  - `event_set_deck_reference_only`
  - `submit_deck_reference_only`
  - `dedicated_deck_upsert_api_not_claimed`
  - `deck_upsert_privacy_boundary`
- coverage basis:
  - `fixture_metadata_only`

The coverage row intentionally does not use `parser_behavior_verified`,
`diagnostics_only`, `evidence_ledger_only`, `count_ratchet_only`, or
`external_reference_only`.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `deck_upsert_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and `fixture_metadata_only` basis;
- absence of `parser_behavior_verified` from the deck-upsert boundary row;
- required known-gap and review-note non-claims;
- session-ledger parser coverage counts:
  - `event_families: {}`
  - `unknown_entries: 0`
  - `truncation_count: 0`
  - `event_set_deck_reference_entries: 1`
  - `submit_deck_reference_entries: 1`
  - `dedicated_deck_upsert_api_events: 0`
  - `dedicated_deck_upsert_parser_routes: 0`
- game-row non-applicability;
- privacy redaction flags, including no decklists, private deck names, or
  private collection data;
- report summary movement from 3 to 4 report-only families and 14 to 13
  missing families;
- the exact `deck_api.deck_upsert` matrix row;
- unchanged adjacent `deck_api.start_hook_deck_snapshot`,
  `deck_api.deck_summary`, `deck_api.event_set_deck`, and
  `deck_api.store_pack_inbox_or_crafting` rows.

## Contract Mismatches

No blocking mismatches were found.

The selected report-only boundary path was viable without parser behavior or
parser test changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future coverage for a dedicated deck-upsert API parser, store/pack/inbox or
crafting behavior, private deck contents, exact deck identity, submitted-deck
truth beyond existing parser-owned fields, active-deck truth, sideboard deltas,
inventory/economy state, diagnostics readiness, release readiness, analytics
truth, AI truth, coaching truth, or production behavior needs separate contract
authority.

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
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 13 missing)`

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py
```

- passed: 73 passed

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

Untracked-source/report whitespace checks:

```bash
git diff --no-index --check /dev/null docs/contracts/parser_corpus_deck_upsert_coverage.md
git diff --no-index --check /dev/null docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md
git diff --no-index --check /dev/null docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md
```

- passed with no output after trimming final blank lines in the new docs

```bash
python3 tools/check_agent_docs.py
```

- passed: checked files 32, errors 0, warnings 0

```bash
python3 tools/check_secret_patterns.py --all
```

- failed on pre-existing repo-wide findings outside this changed package:
  scanned paths 947, forbidden 502, warnings 890
- changed-package secret/private marker scan below passed cleanly, so no new
  secret or private-marker finding was introduced by this slice.

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_deck_upsert_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md
```

- passed: no non-ASCII matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_client_actions_parser.py tests/test_parsers.py tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/runtime/tool/CI paths changed

## Open Risks

- `deck_api.deck_upsert` is intentionally `covered_report_only`; this does
  not prove a dedicated deck-upsert parser or committed parser-behavior fixture.
- Event-set deck, deck-summary, StartHook deck snapshot, submit-deck response,
  and submitted-deck-card evidence remain adjacent references only.
- Future dedicated deck-upsert fixture work remains blocked until Mythic Edge
  has owned, sanitized, parser-supported evidence.
- `deck_api.store_pack_inbox_or_crafting` remains missing.
- `python3 tools/check_secret_patterns.py --all` still fails on pre-existing
  repo-wide findings outside this changed package; the changed-package
  path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.
- Tracker #158 remains open.

## Next Recommended Role

Codex E: Module Reviewer / Contract-Test Reviewer.

Codex E should verify that the package is metadata/test/report-only, that
`deck_api.deck_upsert` moved only to `covered_report_only`, that
`coverage_basis` is exactly `["fixture_metadata_only"]`, and that no nearby
deck evidence was promoted to parser truth.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer / Contract-Test Reviewer for issue #396,
  parser corpus deck-upsert report-only boundary coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/396
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/395
    - Previous merge commit: 3a128565b33ef512c8edcba13083449cb284b55b
    - Branch: codex/parser-corpus-deck-upsert-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_deck_upsert_coverage.md
    - Handoff: docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md

  Goal:
    Review the Codex C implementation against the contract. Confirm whether the
    package is ready for Codex F submission without overclaiming parser support.

  Review:
    - Confirm `deck_api.deck_upsert` moved from `missing` to
      `covered_report_only` only.
    - Confirm `coverage_basis` is exactly `["fixture_metadata_only"]`.
    - Confirm `parser_event_families` is empty and no
      `parser_behavior_verified` basis is used for deck upsert.
    - Confirm event-set deck, deck-summary, StartHook deck snapshot,
      submit-deck, and submitted-deck-card evidence remain adjacent references
      only, not deck-upsert parser truth.
    - Confirm `deck_api.event_set_deck` remains `covered_committed`,
      `deck_api.deck_summary` remains `covered_report_only`,
      `deck_api.start_hook_deck_snapshot` remains `covered_synthetic`, and
      `deck_api.store_pack_inbox_or_crafting` remains `missing`.
    - Confirm no parser behavior, parser state, parser event classes, runtime,
      workbook, webhook, Apps Script, analytics, AI/coaching, generated/private
      artifacts, raw logs, private decklists, or external corpus content changed.
    - Rerun focused validation and record the verdict in the report/handoff if
      appropriate.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private marker scan for changed files
    - path-scoped protected-surface check for changed files
    - path-scoped selector sanity check for changed files

  Do not:
    - Target main directly.
    - Close #396 or tracker #158 unless separately authorized.
    - Add parser behavior, parser event classes, runtime behavior, workbook,
      webhook, Apps Script, analytics, AI/coaching, CI, generated/private
      artifacts, raw logs, private decklists, or external corpus content.
    - Promote event-set, deck-summary, StartHook, submit-deck, or
      submitted-deck-card evidence into dedicated deck-upsert parser support.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/395"
  previous_merge_commit: "3a128565b33ef512c8edcba13083449cb284b55b"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_deck_upsert_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md"
  verdict: "deck_upsert_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/395"
  previous_merge_commit: "3a128565b33ef512c8edcba13083449cb284b55b"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_deck_upsert_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md"
  verdict: "deck_upsert_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
