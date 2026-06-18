# Parser Corpus Deck Upsert Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/396
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/395
- previous_merge_commit: `3a128565b33ef512c8edcba13083449cb284b55b`
- contract: `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- branch: `codex/parser-corpus-deck-upsert-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_report_only_boundary`
- risk_tier: High

## Source Snapshot

PR #395 is present in the local branch:

- required merge commit:
  `3a128565b33ef512c8edcba13083449cb284b55b`
- local HEAD before implementation: `3a12856`
- merge-base ancestry check: passed

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 3
- partial: 3
- missing: 14
- blocked_external_boundary: 6

Pre-change deck API rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `deck_api.start_hook_deck_snapshot` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `start_hook_deck_snapshot_synthetic_v1` |
| `deck_api.deck_summary` | `covered_report_only` | `fixture_metadata_only` | `deck_summary_boundary_report_v1` |
| `deck_api.deck_upsert` | `missing` | `external_reference_only` | none |
| `deck_api.event_set_deck` | `covered_committed` | `fixture_metadata_only`, `parser_behavior_verified` | `bo1_match_win_basic` |
| `deck_api.store_pack_inbox_or_crafting` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only boundary metadata path authorized by the contract:

- manifest entry: `deck_upsert_boundary_report_v1`
- session ledger entry: `deck_upsert_boundary_report_v1`
- scenario family: `deck_api.deck_upsert`
- coverage status: `covered_report_only`
- coverage basis:
  - `fixture_metadata_only`
- parser event families: none
- parser claim families:
  - `deck_upsert_boundary_report`
  - `event_set_deck_reference_only`
  - `submit_deck_reference_only`
  - `dedicated_deck_upsert_api_not_claimed`
  - `deck_upsert_privacy_boundary`

No parser test or parser source was added for deck-upsert behavior. The row
records an inspected boundary: current Mythic Edge evidence includes nearby
event-set deck, deck-summary, StartHook deck snapshot, submit-deck, and
submitted-deck-card surfaces, but none are promoted to dedicated deck-upsert API
parser support.

No parser source, client-action parser behavior, parser event classes, router
semantics, parser state final reconciliation, runtime behavior, diagnostics
behavior, golden replay behavior, feature-equity behavior, evidence-ledger
behavior, workbook behavior, webhook behavior, Apps Script behavior, analytics
behavior, AI behavior, coaching behavior, CI behavior, merge policy, deploy
policy, release policy, or production behavior was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 13
- covered_report_only: 4
- partial: 3
- missing: 13
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

Post-change deck API rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `deck_api.start_hook_deck_snapshot` | `covered_synthetic` | `fixture_metadata_only`, `parser_behavior_verified` | `start_hook_deck_snapshot_synthetic_v1` |
| `deck_api.deck_summary` | `covered_report_only` | `fixture_metadata_only` | `deck_summary_boundary_report_v1` |
| `deck_api.deck_upsert` | `covered_report_only` | `fixture_metadata_only` | `deck_upsert_boundary_report_v1` |
| `deck_api.event_set_deck` | `covered_committed` | `fixture_metadata_only`, `parser_behavior_verified` | `bo1_match_win_basic` |
| `deck_api.store_pack_inbox_or_crafting` | `missing` | `external_reference_only` | none |

The deck-upsert row includes this non-claim note:

```text
The deck-upsert row is intentionally report-only and prevents false parity claims by documenting why nearby event-set, deck-summary, StartHook, submit-deck, and submitted-deck-card evidence is not deck-upsert evidence; future dedicated deck-upsert fixture work remains blocked until Mythic Edge has owned, sanitized, parser-supported evidence.
```

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No private logs, external corpus content, runtime artifacts, generated data,
  SQLite databases, workbook exports, failed posts, credentials, tokens, API
  keys, webhook URLs, private deck names, private collection data, decklists,
  card choices, sideboard plans, strategy notes, or private smoke outputs were
  committed.
- The deck-upsert row is committed boundary metadata only.
- `deck_api.deck_summary` remains `covered_report_only`.
- `deck_api.start_hook_deck_snapshot` remains `covered_synthetic`.
- `deck_api.event_set_deck` remains `covered_committed`.
- `deck_api.store_pack_inbox_or_crafting` remains `missing`.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from corpus metadata alone.
- This report does not claim a dedicated deck-upsert API parser.
- This report does not claim that event-set deck, deck summary, StartHook deck
  snapshot, submit-deck, or submitted-deck-card evidence proves deck-upsert
  behavior.
- This report does not claim live private deck-upsert payload diversity.
- This report does not claim private deck contents, private deck names, exact
  deck identity truth, submitted-deck truth beyond existing parser-owned
  fields, active-deck truth, sideboard-delta truth, collection ownership truth,
  inventory/economy state, store/pack/inbox/crafting coverage, hidden-card
  inference, decklist completion, archetype classification, gameplay advice,
  player-mistake labels, diagnostics readiness, analytics truth, AI truth, or
  coaching truth.
- This report does not claim release readiness, merge readiness, deploy
  readiness, production behavior, issue closure, or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The package moves only `deck_api.deck_upsert` to
`covered_report_only` with exact `coverage_basis: ["fixture_metadata_only"]`.
The new manifest entry uses `parser_event_families: []` and does not use
`parser_behavior_verified` or any parser event family as deck-upsert truth.

Adjacent deck API rows remain bounded:

- `deck_api.start_hook_deck_snapshot`: `covered_synthetic`
- `deck_api.deck_summary`: `covered_report_only`
- `deck_api.event_set_deck`: `covered_committed`
- `deck_api.store_pack_inbox_or_crafting`: `missing`

The implementation stays metadata/test/report-only. No parser source,
client-action parser behavior, parser event class, parser state, router,
runtime surface, workbook surface, webhook surface, Apps Script surface,
analytics surface, AI/coaching surface, generated artifact, private log,
private decklist, private deck name, private collection data, or external
corpus content changed.

### Validation Reviewed

Codex E reran:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py
```

- passed: 73 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 13 missing)`

```bash
PYTHONPATH=src python3 -m ruff check src tests tools
git diff --check
python3 tools/check_agent_docs.py
```

- passed: Ruff all checks passed; `git diff --check` no output; agent docs
  errors 0, warnings 0

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
PYTHONPATH=src python3 -m pytest -q
```

- passed: 1770 passed

Additional reviewer checks:

- branch HEAD contains required merge commit
  `3a128565b33ef512c8edcba13083449cb284b55b`.
- no changed paths under `src`, `tools`, `.github`, `main.py`,
  `live_print_filtered_v11_match_summary.py`, `tests/test_client_actions_parser.py`,
  or `tests/test_parsers.py`.
- no generated SQLite artifacts found.
- ASCII scan over the changed package found no matches.
- untracked contract/handoff/report whitespace checks produced no check output.
- `python3 tools/check_secret_patterns.py --all` remains advisory-failed on
  pre-existing repo-wide findings outside the changed #396 package; the
  path-scoped scan over the six #396 files is clean.

### Remaining Non-Blocking Gaps

- This is still report-only boundary coverage. It does not prove a dedicated
  deck-upsert API parser, live/private deck-upsert payload diversity, exact deck
  identity truth, active-deck truth, submitted-deck truth beyond existing
  parser-owned fields, inventory/economy truth, analytics truth, AI truth,
  coaching truth, release readiness, deploy readiness, production behavior, or
  tracker #158 completion.
- Future promotion of `deck_api.deck_upsert` to parser-behavior coverage needs
  a new issue and contract loopback with owned sanitized evidence.

## Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/395"
  previous_merge_commit: "3a128565b33ef512c8edcba13083449cb284b55b"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md"
  target_artifact: "draft PR for deck-upsert report-only boundary coverage"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_client_actions_parser.py tests/test_parsers.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private-marker scan over the #396 package"
    - "path-scoped protected-surface gate over the #396 package"
    - "path-scoped validation selector over the #396 package"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #396 or tracker #158."
    - "Do not promote deck_api.deck_upsert to parser-behavior coverage without contract loopback."
    - "Do not claim a dedicated deck-upsert API parser."
    - "Do not broaden coverage to store/pack/inbox/crafting, inventory/economy, runtime active-deck matching, analytics, AI, coaching, release, deploy, or production behavior."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/output surfaces."
    - "Do not commit raw private Player.log excerpts, private decklists, generated/private/runtime artifacts, or external corpus content."
```
