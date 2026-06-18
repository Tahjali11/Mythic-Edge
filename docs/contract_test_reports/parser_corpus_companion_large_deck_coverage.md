# Parser Corpus Companion / Large-Deck Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/407
- previous_merge_commit: `bece21b5d5e01ccaff110b7caaf6a1bfbe320bea`
- contract: `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- branch: `codex/parser-corpus-companion-large-deck-coverage`
- base_branch: `codex/parser-parity`
- selected_path: `covered_report_only_boundary`
- risk_tier: High

## Source Snapshot

PR #407 is merged into `codex/parser-parity`, and the local implementation
branch starts at the required merge commit:

- local HEAD before implementation:
  `bece21b5d5e01ccaff110b7caaf6a1bfbe320bea`
- merge-base ancestry check: passed
- issue #408 state: open
- tracker #158 state: open

The pre-change corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Pre-change result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 7
- partial: 3
- missing: 9
- deferred: 0
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- not_applicable: 0

Pre-change companion / large-deck row:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `gameplay_stress.companion_or_large_deck` | `missing` | `external_reference_only` | none |

## Implementation Summary

Added the single report-only boundary metadata path authorized by the
contract:

- manifest entry: `companion_large_deck_boundary_report_v1`
- session ledger entry: `companion_large_deck_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- scenario family: `gameplay_stress.companion_or_large_deck`
- coverage status: `covered_report_only`
- coverage basis:
  - `fixture_metadata_only`
- parser event families: none
- parser claim families:
  - `companion_large_deck_boundary_report`
  - `generic_deck_snapshot_not_companion_or_large_deck`
  - `submitted_deck_cards_not_decklist_truth`
  - `card_identity_not_deck_shape_truth`
  - `companion_legality_not_claimed`
  - `decklist_completion_non_claim`

The committed metadata is a boundary report only. It is not a raw fixture, not
a synthetic gameplay fixture, not a parser behavior claim, and not evidence of
companion presence, companion legality, companion castability, large-deck
size, complete decklists, deck identity, hidden-card truth, or archetype
classification.

No parser source, parser behavior, parser event class, router behavior,
StartHook parser behavior, client-action parser behavior, submitted-deck
parsing behavior, card-list normalization behavior, diagnostics behavior,
golden replay behavior, feature-equity behavior, evidence-ledger behavior,
runtime behavior, workbook behavior, webhook behavior, Apps Script behavior,
analytics behavior, AI behavior, coaching behavior, CI behavior, merge
policy, deploy policy, release policy, production behavior, raw log fixture,
private smoke artifact, generated artifact, decklist, deck name, deck ID,
sideboard choice, companion candidate, card-choice artifact, strategy note, or
external corpus content was changed.

## Post-Change Corpus Snapshot

Post-change corpus report result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 8
- partial: 3
- missing: 8
- deferred: 0
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- not_applicable: 0

Post-change companion / large-deck and adjacent rows:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries |
| --- | --- | --- | --- |
| `gameplay_stress.opponent_auto_concede` | `covered_report_only` | `fixture_metadata_only` | `opponent_auto_concede_boundary_report_v1` |
| `gameplay_stress.companion_or_large_deck` | `covered_report_only` | `fixture_metadata_only` | `companion_large_deck_boundary_report_v1` |
| `gameplay_stress.conjure` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.spellbook` | `blocked_external_boundary` | `external_reference_only` | `external_reference_category_boundary` |
| `gameplay_stress.action_attribution` | `missing` | `external_reference_only` | none |
| `gameplay_stress.event_ordering` | `missing` | `external_reference_only` | none |

The companion / large-deck row includes this non-claim note:

```text
Companion / large-deck coverage is report-only boundary metadata: generic deck snapshots, submitted-deck card-content evidence, StartHook summaries, card identity provenance, and public taxonomy metadata do not prove companion presence, companion legality, large-deck size, complete decklists, deck identity, hidden-card truth, archetype classification, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior.
```

The session-ledger entry records:

- deck snapshot reference entries: 1
- submitted deck reference entries: 1
- card identity reference entries: 1
- dedicated companion fixtures: 0
- dedicated large-deck fixtures: 0
- companion legality claims: 0
- decklist completion claims: 0
- game rows: 0

## Privacy And Protected-Surface Assertions

- No raw Player.log excerpts were added.
- No Manasight raw logs, external corpus content, private local logs, private
  smoke outputs, generated data, SQLite databases, runtime artifacts, failed
  posts, workbook exports, credentials, tokens, API keys, webhook URLs,
  private decklists, raw submitted-deck payloads, deck names, deck IDs,
  sideboard choices, companion candidates, card choices, or strategy notes
  were committed.
- No parser source, parser event schema, router dispatch, parser state,
  StartHook parser behavior, client-action parser behavior, submitted-deck
  parsing behavior, card-list normalization behavior, workbook, webhook, Apps
  Script, analytics, AI, coaching, runtime, CI, merge, deploy, release, or
  production surface was changed.
- `gameplay_stress.opponent_auto_concede` remains independently report-only.
- `gameplay_stress.conjure` and `gameplay_stress.spellbook` remain external
  boundary rows.
- `gameplay_stress.action_attribution` and
  `gameplay_stress.event_ordering` remain missing.

## Explicit Non-Claims

- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from public taxonomy metadata.
- This report does not claim companion presence, companion legality, or
  companion castability.
- This report does not claim large-deck size.
- This report does not claim complete decklist contents, deck identity, deck
  ownership, sideboard truth, hidden-card truth, or archetype classification.
- This report does not claim matchup plans, gameplay advice,
  player-mistake labeling, analytics truth, AI truth, or coaching truth.
- This report does not claim private smoke success.
- This report does not claim runtime health, release readiness, deploy
  readiness, merge readiness, or production readiness.
- This report does not claim issue closure or tracker completion.

## Validation

Validation is recorded in the companion implementation handoff:

- `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The implementation moves only
`gameplay_stress.companion_or_large_deck` from `missing` to
`covered_report_only`, with exact `coverage_basis: ["fixture_metadata_only"]`.
The row is owned only by `companion_large_deck_boundary_report_v1`, and
`parser_event_families` is empty.

The session-ledger metadata preserves the required zero-count boundary:

- dedicated companion fixtures: 0
- dedicated large-deck fixtures: 0
- companion-legality claims: 0
- decklist-completion claims: 0

The row remains report-only boundary metadata. It does not turn generic deck
snapshots, submitted-deck card-content evidence, StartHook summaries, card
identity provenance, public taxonomy metadata, private deck material, or
large-looking card lists into parser-owned companion / large-deck truth.

Adjacent gameplay-stress rows remain separate:

- `gameplay_stress.opponent_auto_concede`: `covered_report_only`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `gameplay_stress.action_attribution`: `missing`
- `gameplay_stress.event_ordering`: `missing`

### Protected-Surface Status

No protected parser or downstream behavior drift was found. Reviewer inspection
found no changes under `src`, `tools`, `.github`, `main.py`,
`live_print_filtered_v11_match_summary.py`,
`tests/test_collection_parser.py`, `tests/test_client_actions_parser.py`,
`tests/test_runtime_surfaces.py`, `tests/test_evidence_ledger.py`,
`tests/test_grp_id_candidates.py`, or `tests/fixtures/golden_replay`.

The changed package is limited to:

- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

### Validation Reviewed

Codex E reran:

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  - result: 7 passed
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - result: `partial_coverage_map_ready` with 45 families, 6 committed, 8 missing
- `python3 tools/check_agent_docs.py`
  - result: passed with 0 errors and 0 warnings
- `python3 -m ruff check src tests tools`
  - result: passed
- `git diff --check`
  - result: passed
- path-scoped secret/private marker scan for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped protected-surface gate for the changed package
  - result: passed with 0 forbidden and 0 warnings
- path-scoped validation selector sanity check for the changed package
  - result: `selection_status: ok`
- `PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_runtime_surfaces.py tests/test_evidence_ledger.py tests/test_grp_id_candidates.py`
  - result: 185 passed
- `PYTHONPATH=src python3 -m pytest -q`
  - result: 1770 passed

Additional reviewer checks:

- Previous merge commit
  `bece21b5d5e01ccaff110b7caaf6a1bfbe320bea` is an ancestor of `HEAD`.
- Reviewer manifest inspection confirms only
  `companion_large_deck_boundary_report_v1` owns
  `gameplay_stress.companion_or_large_deck`.
- Reviewer corpus matrix inspection confirms
  `gameplay_stress.companion_or_large_deck` is `covered_report_only` with
  `["fixture_metadata_only"]` and
  `["companion_large_deck_boundary_report_v1"]`.
- Reviewer session-ledger inspection confirms the required zero dedicated
  companion/large-deck/companion-legality/decklist-completion counts.
- Reviewer corpus matrix inspection confirms `gameplay_stress.opponent_auto_concede`,
  `gameplay_stress.conjure`, `gameplay_stress.spellbook`,
  `gameplay_stress.action_attribution`, and
  `gameplay_stress.event_ordering` remain separately scoped.
- Changed-package ASCII scan produced no findings.
- Generated SQLite/database artifact scan produced no findings.

### Remaining Non-Blocking Gaps

This remains report-only boundary metadata. It does not prove parser support,
synthetic gameplay fixture support, companion presence, companion legality,
companion castability, large-deck size, complete decklist contents, deck
identity, deck ownership, sideboard truth, hidden-card truth, archetype
classification, matchup plans, gameplay advice, player-mistake labeling,
analytics truth, AI truth, coaching truth, private smoke success, release
readiness, deploy readiness, merge readiness, production behavior, full corpus
parity, issue closure, or tracker completion. Future parser-owned support,
synthetic gameplay evidence, deck-shape evidence, private evidence collection,
or sanctioned companion / large-deck fixture design requires separate contract
authority.

### Next Recommended Role

Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/407"
  previous_merge_commit: "bece21b5d5e01ccaff110b7caaf6a1bfbe320bea"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md"
  target_artifact: "draft PR for companion / large-deck report-only boundary"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-companion-large-deck-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_runtime_surfaces.py tests/test_evidence_ledger.py tests/test_grp_id_candidates.py"
    - "PYTHONPATH=src python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #408 or tracker #158."
    - "Do not use companion / large-deck report-only coverage as parser support, companion presence truth, companion legality truth, large-deck truth, decklist truth, deck identity truth, hidden-card truth, archetype truth, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, merge readiness, deploy readiness, production behavior, or tracker-completion authority."
    - "Do not promote gameplay_stress.companion_or_large_deck beyond report-only boundary metadata without separate contract authority."
    - "Do not change parser behavior, StartHook parser behavior, client-action parser behavior, submitted-deck parsing behavior, card-list normalization behavior, parser event classes, router behavior, parser state final reconciliation, match/game identity, deduplication, runtime behavior, workbook/webhook/App Script/output surfaces, analytics truth, AI truth, coaching truth, CI, or production behavior."
    - "Do not commit raw private Player.log excerpts, private local logs, raw submitted-deck payloads, decklists, deck names, deck IDs, companion choices, sideboard choices, card choices, strategy notes, private smoke reports, generated/private/runtime artifacts, workbook exports, credentials, webhook URLs, or external corpus content."
```
