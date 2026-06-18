# Parser Corpus StartHook Deck Snapshot Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/390
- previous_merge_commit: `6591490e6eafcb8f90773e6b8b493cfb85ee0285`
- contract: `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- branch: `codex/parser-corpus-start-hook-deck-snapshot-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `safe_synthetic_coverage`
- risk_tier: High

## Source Snapshot

PR #390 is present in the local branch:

- required merge commit:
  `6591490e6eafcb8f90773e6b8b493cfb85ee0285`
- local HEAD before implementation: `6591490`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 12
- covered_report_only: 2
- partial: 3
- missing: 16
- blocked_external_boundary: 6

Pre-change deck API rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `deck_api.start_hook_deck_snapshot` | `missing` | `external_reference_only` | none |
| `deck_api.deck_summary` | `missing` | `external_reference_only` | none |
| `deck_api.deck_upsert` | `missing` | `external_reference_only` | none |
| `deck_api.event_set_deck` | `covered_committed` | `fixture_metadata_only`, `parser_behavior_verified` | `bo1_match_win_basic` |
| `deck_api.store_pack_inbox_or_crafting` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single synthetic metadata path authorized by the contract:

- manifest entry: `start_hook_deck_snapshot_synthetic_v1`
- session ledger entry: `start_hook_deck_snapshot_synthetic_v1`
- scenario family: `deck_api.start_hook_deck_snapshot`
- coverage status: `covered_synthetic`
- coverage basis:
  - `fixture_metadata_only`
  - `parser_behavior_verified`
- parser event families:
  - `Collection`
  - `DeckCollection`
- parser claim families:
  - `start_hook_collection_snapshot`
  - `start_hook_deck_collection_snapshot`
  - `start_hook_deck_summary_to_deck_map_correlation`
  - `start_hook_raw_evidence_preservation`
  - `start_hook_deck_snapshot_privacy_boundary`

Added a focused synthetic StartHook collection parser test proving:

- a bounded `StartHook` response with `PlayerCards`, `DeckSummaries`, and
  `Decks`;
- `Collection` plus `DeckCollection` emission;
- `DeckSummaries` to `Decks` correlation by `DeckId`;
- raw StartHook evidence preservation for both emitted payloads;
- no private deck names, private decklists, raw Player.log excerpts, or
  external corpus material.

No parser source, StartHook parser behavior, parser event classes, router
semantics, parser state final reconciliation, runtime behavior, workbook
behavior, webhook behavior, Apps Script behavior, analytics behavior, AI
behavior, coaching behavior, CI behavior, merge policy, deploy policy, or
production behavior was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 2
- partial: 3
- missing: 15
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change deck API rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `deck_api.start_hook_deck_snapshot` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `start_hook_deck_snapshot_synthetic_v1` |
| `deck_api.deck_summary` | `missing` | `external_reference_only` | none |
| `deck_api.deck_upsert` | `missing` | `external_reference_only` | none |
| `deck_api.event_set_deck` | `covered_committed` | `fixture_metadata_only`, `parser_behavior_verified` | `bo1_match_win_basic` |
| `deck_api.store_pack_inbox_or_crafting` | `missing` | `external_reference_only` | none |

The StartHook deck snapshot row includes this non-claim note:

```text
Synthetic StartHook deck snapshot coverage proves parser-owned Collection and DeckCollection StartHook metadata only; it preserves a bounded deck snapshot as evidence and does not claim deck identity, submitted-deck, sideboard-delta, inventory/economy, analytics, AI, coaching, release, or production truth.
```

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No private logs, external corpus content, runtime artifacts, generated data,
  SQLite databases, workbook exports, failed posts, credentials, tokens, API
  keys, webhook URLs, private deck names, private collection data, decklists,
  or private smoke outputs were committed.
- The synthetic StartHook payload is repo-owned test evidence only.
- The session ledger records summary counts only.
- `deck_api.deck_summary`, `deck_api.deck_upsert`, and
  `deck_api.store_pack_inbox_or_crafting` remain missing.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from corpus metadata alone.
- This report does not claim live Arena StartHook payload diversity.
- This report does not claim private deck contents, exact deck identity,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, inventory/economy truth, deck-summary API coverage,
  deck-upsert behavior, store/pack/inbox/crafting behavior, hidden-card
  inference, decklist completion, archetype classification, gameplay advice,
  analytics truth, AI truth, or coaching truth.
- This report does not claim diagnostics readiness, release readiness, merge
  readiness, deploy readiness, production behavior, issue closure, or tracker
  completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`

## Next Recommended Role

Codex F: Module Submitter.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The #392 implementation matches the safe synthetic coverage contract:

- only `deck_api.start_hook_deck_snapshot` moved to `covered_synthetic`;
- the new coverage row uses exactly `fixture_metadata_only` and
  `parser_behavior_verified`;
- `parser_event_families` is exactly `["Collection", "DeckCollection"]`;
- `start_hook_deck_snapshot_synthetic_v1` is the only new corpus coverage
  entry;
- `deck_api.deck_summary`, `deck_api.deck_upsert`, and
  `deck_api.store_pack_inbox_or_crafting` remain `missing`;
- `deck_api.event_set_deck` remains `covered_committed` through
  `bo1_match_win_basic`;
- the focused parser test proves `Collection` and `DeckCollection` emission,
  `DeckId` correlation, and `raw_start_hook` evidence preservation without
  private deck data;
- the row remains bounded synthetic StartHook parser evidence, not private deck
  truth or live Arena behavior proof.

### Validation Results

- GitHub reference check:
  - issue #392: open;
  - tracker #158: open;
  - PR #390: merged into `codex/parser-parity` at
    `6591490e6eafcb8f90773e6b8b493cfb85ee0285`.
- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py`:
  15 passed.
- `PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py`:
  34 passed.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`:
  `partial_coverage_map_ready (45 families, 6 committed, 15 missing)`.
- Direct report-row inspection confirmed:
  - `deck_api.start_hook_deck_snapshot`: `covered_synthetic` with
    `start_hook_deck_snapshot_synthetic_v1`;
  - `deck_api.deck_summary`: `missing`;
  - `deck_api.deck_upsert`: `missing`;
  - `deck_api.event_set_deck`: `covered_committed` with
    `bo1_match_win_basic`;
  - `deck_api.store_pack_inbox_or_crafting`: `missing`.
- `PYTHONPATH=src python3 -m ruff check src tests`: passed.
- `PYTHONPATH=src python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- No-index whitespace checks for the new contract, handoff, and report docs:
  no output.
- `python3 tools/check_agent_docs.py`: passed.
- Path-scoped secret/private-marker scan over the #392 package: passed with
  0 forbidden findings and 0 warnings.
- Path-scoped protected-surface gate over the #392 package: passed with
  0 forbidden findings and 0 warnings.
- Path-scoped validation selector over the #392 package: `selection_status: ok`.
- ASCII scan over the #392 package: no non-ASCII output.
- SQLite/database artifact scan: no artifacts found.
- Optional broader validation,
  `PYTHONPATH=src python3 -m pytest -q`: 1770 passed.

### Protected-Surface Status

No parser source, StartHook parser behavior, parser event class, router,
parser state, runtime, workbook/webhook/App Script, diagnostics, golden replay,
feature-equity, evidence-ledger, analytics, AI/coaching, CI, merge/deploy,
release-readiness, or production surfaces changed. `git diff --name-only --
src tools main.py live_print_filtered_v11_match_summary.py .github` returned
no paths.

The worktree contains only the expected changed #392 package:

- `tests/test_collection_parser.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`

### Remaining Risks

- This is synthetic corpus coverage. It does not prove live Arena StartHook
  payload diversity, private deck contents, exact deck identity,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, inventory/economy state, deck-summary coverage,
  deck-upsert behavior, store/pack/inbox/crafting behavior, analytics truth,
  AI truth, coaching truth, release readiness, production behavior, full corpus
  parity, or tracker completion.
- Future real-world StartHook payload evidence may need a separate issue and
  contract if it differs from the bounded synthetic shape.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/390"
  previous_merge_commit: "6591490e6eafcb8f90773e6b8b493cfb85ee0285"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md"
  target_artifact: "draft PR for synthetic StartHook deck snapshot coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-start-hook-deck-snapshot-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m ruff check src tests"
    - "PYTHONPATH=src python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private-marker scan over the #392 package"
    - "path-scoped protected-surface gate over the #392 package"
    - "path-scoped validation selector over the #392 package"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #392 or tracker #158."
    - "Do not broaden coverage to deck summary, deck upsert, store/pack/inbox/crafting, inventory/economy, analytics, AI, coaching, release, or production behavior."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/output surfaces."
    - "Do not commit raw private Player.log excerpts, private decklists, generated/private/runtime artifacts, or external corpus content."
```
