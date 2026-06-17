# Parser Corpus StartHook Deck Snapshot Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/392

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_start_hook_deck_snapshot_coverage_ready_for_review`

## Files Changed

- `tests/test_collection_parser.py`
  - Added a focused synthetic StartHook deck snapshot evidence test.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `start_hook_deck_snapshot_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic StartHook deck snapshot summary metadata.
- `tests/test_corpus_parity_report.py`
  - Updated synthetic/missing summary counts.
  - Added focused checks for manifest/session shape, parser event family,
    bounded basis, StartHook non-claims, and adjacent deck API rows.
- `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`

No parser source, StartHook parser behavior, parser event classes, router
semantics, parser state final reconciliation, diagnostics source, golden
replay source, feature-equity source, evidence-ledger source, runtime source,
workbook export, generated/private artifact, raw fixture, private log, private
decklist, or external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 12
- covered_report_only: 2
- partial: 3
- missing: 16
- `deck_api.start_hook_deck_snapshot`: `missing`
- `deck_api.deck_summary`: `missing`
- `deck_api.deck_upsert`: `missing`
- `deck_api.event_set_deck`: `covered_committed`
- `deck_api.store_pack_inbox_or_crafting`: `missing`

This matched the contract's expected starting state after issue #389.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `deck_api.start_hook_deck_snapshot` | `missing` | `covered_synthetic` |

Preserved the required adjacent deck API boundary:

- `deck_api.deck_summary` remains `missing`.
- `deck_api.deck_upsert` remains `missing`.
- `deck_api.event_set_deck` remains `covered_committed` through
  `bo1_match_win_basic`.
- `deck_api.store_pack_inbox_or_crafting` remains `missing`.

Added the required synthetic metadata:

- entry id: `start_hook_deck_snapshot_synthetic_v1`
- session id: `start_hook_deck_snapshot_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families:
  - `Collection`
  - `DeckCollection`
- parser claim families:
  - `start_hook_collection_snapshot`
  - `start_hook_deck_collection_snapshot`
  - `start_hook_deck_summary_to_deck_map_correlation`
  - `start_hook_raw_evidence_preservation`
  - `start_hook_deck_snapshot_privacy_boundary`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`

The coverage row intentionally does not use `diagnostics_only`,
`evidence_ledger_only`, `count_ratchet_only`, or `external_reference_only`.

## Focused Test Coverage

`tests/test_collection_parser.py` now pins:

- collection object emission from synthetic `PlayerCards`;
- deck collection object emission from synthetic `DeckSummaries` plus `Decks`;
- event ordering: `Collection`, then `DeckCollection`;
- `DeckId` summary-to-deck-payload correlation;
- bounded list payload preservation under `list`;
- source evidence preservation under `raw_start_hook` for both event payloads;
- synthetic-only card/deck values;
- body-level synthetic API response literals without Player.log-style header
  lines.

`tests/test_corpus_parity_report.py` now pins:

- manifest validation and session-ledger validation;
- the `start_hook_deck_snapshot_synthetic_v1` manifest entry shape;
- `parser_event_families: ["Collection", "DeckCollection"]`;
- exact `covered_synthetic` status and basis;
- session-ledger parser coverage counts:
  - `Collection: 1`
  - `DeckCollection: 1`
  - `unknown_entries: 0`
  - `truncation_count: 0`
  - `start_hook_collection_snapshots: 1`
  - `start_hook_deck_collection_snapshots: 1`
  - `start_hook_correlated_decks: 1`
  - `start_hook_orphaned_deck_summaries_skipped: 0`
  - `start_hook_malformed_deck_summaries_skipped: 0`
- game-row non-applicability;
- privacy redaction flags, including no decklists, private deck names, or
  private collection data;
- report summary movement from 12 to 13 synthetic families and 16 to 15
  missing families;
- the exact `deck_api.start_hook_deck_snapshot` matrix row;
- unchanged adjacent `deck_api.deck_summary`, `deck_api.deck_upsert`,
  `deck_api.event_set_deck`, and `deck_api.store_pack_inbox_or_crafting` rows.

## Contract Mismatches

No blocking mismatches were found.

The selected safe synthetic path was viable without parser behavior changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future coverage for deck-summary API behavior, deck-upsert behavior,
store/pack/inbox/crafting behavior, private deck contents, exact deck identity,
submitted-deck truth, sideboard deltas, inventory/economy state, diagnostics
readiness, release readiness, analytics truth, AI truth, coaching truth, or
production behavior needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required synthetic metadata
and existing StartHook parser behavior evidence.

This package does not add private smoke, live log, diagnostics, analytics,
release, or production tests because those claims are outside the contract.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py
```

- passed: 15 passed

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py
```

- passed: 34 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 15 missing)`

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
git diff --no-index --check /dev/null docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md
git diff --no-index --check /dev/null docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md
git diff --no-index --check /dev/null docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md
```

- passed with no output after trimming final blank lines from the new Codex C docs

```bash
python3 tools/check_agent_docs.py
```

- passed: checked files 32, errors 0, warnings 0

Changed-package path-scoped checks included the untracked Codex B source
contract and the Codex C handoff/report:

```bash
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned paths 7, forbidden 0, warnings 0
- note: the first scan flagged pre-existing Player.log-style literals in
  `tests/test_collection_parser.py`; the synthetic test file now uses
  body-level API response literals without log headers, and the rerun passed

```bash
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md
```

- passed: no non-ASCII matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

## Open Risks

- This is synthetic corpus coverage. It does not prove live Arena StartHook
  payload diversity or private Player.log deck snapshot health.
- It does not cover private deck contents, exact deck identity,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, inventory/economy truth, deck-summary API coverage,
  deck-upsert behavior, store/pack/inbox/crafting behavior, hidden-card
  inference, decklist completion, archetype classification, gameplay advice,
  analytics truth, AI truth, coaching truth, diagnostics readiness, release
  readiness, production behavior, or tracker #158 completion.
- Future private smoke or real-world StartHook payloads may require a separate
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

  Act as Codex E: Module Reviewer for issue #392, StartHook deck snapshot corpus coverage under tracker #158.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/390
    - Previous merge commit: 6591490e6eafcb8f90773e6b8b493cfb85ee0285
    - Branch: codex/parser-corpus-start-hook-deck-snapshot-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md
    - Implementation handoff: docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md
    - Contract test report: docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md

  Goal:
    Review the #392 implementation against the contract, focused diff, and validation evidence. Do not implement fixes.

  Review focus:
    - Confirm only deck_api.start_hook_deck_snapshot moved from missing to covered_synthetic.
    - Confirm deck_api.deck_summary, deck_api.deck_upsert, and deck_api.store_pack_inbox_or_crafting remain missing.
    - Confirm deck_api.event_set_deck remains covered_committed through bo1_match_win_basic.
    - Confirm the synthetic StartHook parser test proves Collection and DeckCollection emission, DeckId correlation, and raw_start_hook evidence preservation without private deck data.
    - Confirm manifest/session-ledger metadata, coverage_basis, parser_event_families, parser_claim_families, known gaps, and review notes match the contract.
    - Confirm no parser behavior, runtime behavior, workbook/webhook/App Script behavior, analytics behavior, AI/coaching behavior, generated/private artifact, raw Player.log excerpt, private decklist, or external corpus content changed.

  Validation to inspect or rerun:
    - PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - PYTHONPATH=src python3 -m ruff check src tests
    - git diff --check
    - python3 tools/check_agent_docs.py
    - path-scoped secret/private-marker scan over the #392 package
    - path-scoped protected-surface gate over the #392 package
    - path-scoped validation selector over the #392 package

  Do not:
    - Implement fixes.
    - Target main directly.
    - Close #392 or tracker #158.
    - Broaden coverage to deck summary, deck upsert, store/pack/inbox/crafting, inventory/economy, analytics, AI, coaching, release, or production behavior.
    - Change parser behavior or protected parser/runtime/workbook/webhook/App Script/output surfaces.
    - Commit raw private Player.log excerpts, private decklists, generated/private/runtime artifacts, or external corpus content.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/390"
  previous_merge_commit: "6591490e6eafcb8f90773e6b8b493cfb85ee0285"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md"
  verdict: "synthetic_start_hook_deck_snapshot_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-start-hook-deck-snapshot-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
```
## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/390"
  previous_merge_commit: "6591490e6eafcb8f90773e6b8b493cfb85ee0285"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md"
  verdict: "synthetic_start_hook_deck_snapshot_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-start-hook-deck-snapshot-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
```
