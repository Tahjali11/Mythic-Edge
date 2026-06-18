# Parser Corpus Companion / Large-Deck Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/408

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_companion_large_deck_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`companion_large_deck_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `companion_large_deck_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added count-only/report-only session metadata for
    `companion_large_deck_boundary_report_v1`.
- `tests/test_corpus_parity_report.py`
  - Updated summary-count expectations.
  - Added focused manifest and session-ledger assertions for
    `gameplay_stress.companion_or_large_deck`.
  - Added exact matrix-row assertions for
    `gameplay_stress.companion_or_large_deck`.
  - Preserved exact adjacent row assertions for
    `gameplay_stress.opponent_auto_concede`, `gameplay_stress.conjure`,
    `gameplay_stress.spellbook`,
    `gameplay_stress.action_attribution`, and
    `gameplay_stress.event_ordering`.
- `docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`

No parser source, parser behavior, parser event class, router behavior,
StartHook parser behavior, client-action parser behavior, submitted-deck
parsing behavior, card-list normalization behavior, diagnostics source,
golden replay source, feature-equity source, evidence-ledger source, runtime
source, workbook export, webhook surface, Apps Script surface, analytics
source, AI/coaching behavior, generated/private artifact, raw fixture, private
log, private smoke output, raw submitted-deck payload, decklist, deck name,
deck ID, sideboard choice, companion candidate, card-choice artifact, strategy
note, runtime status file, failed post, workbook export, or external corpus
content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 7
- partial: 3
- missing: 9
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- `gameplay_stress.opponent_auto_concede`: `covered_report_only`
- `gameplay_stress.companion_or_large_deck`: `missing`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`
- `gameplay_stress.action_attribution`: `missing`
- `gameplay_stress.event_ordering`: `missing`

Repo inspection confirmed existing deck/card evidence surfaces, but no
committed parser-owned companion / large-deck fixture and no contract authority
to infer companion presence, companion legality, companion castability,
large-deck size, complete decklists, deck identity, hidden-card truth, or
archetype classification from generic deck snapshots, submitted-deck
card-content evidence, StartHook summaries, card identity provenance, or public
taxonomy metadata.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `gameplay_stress.companion_or_large_deck` | `missing` | `covered_report_only` |

Added the required boundary metadata:

- entry id: `companion_large_deck_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- parser event families: none
- parser claim families:
  - `companion_large_deck_boundary_report`
  - `generic_deck_snapshot_not_companion_or_large_deck`
  - `submitted_deck_cards_not_decklist_truth`
  - `card_identity_not_deck_shape_truth`
  - `companion_legality_not_claimed`
  - `decklist_completion_non_claim`
- coverage basis:
  - `fixture_metadata_only`

The coverage row intentionally does not claim parser support,
parser-behavior verification, synthetic gameplay fixture support, companion
presence, companion legality, companion castability, large-deck size, complete
decklist contents, deck identity, deck ownership, sideboard truth, hidden-card
truth, archetype classification, matchup plans, gameplay advice, analytics
truth, AI truth, coaching truth, release readiness, merge readiness, deploy
readiness, or production behavior.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- the `companion_large_deck_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and `["fixture_metadata_only"]` basis;
- non-claim parser claim families;
- known-gap and review-note non-claims;
- the session-ledger entry shape;
- count-only parser coverage fields, including zero dedicated companion
  fixtures, zero dedicated large-deck fixtures, zero companion-legality claims,
  and zero decklist-completion claims;
- report-only redaction flags for private decklists, raw submitted-deck
  payloads, deck names, deck IDs, sideboard choices, companion candidates,
  card choices, strategy notes, local smoke outputs, generated/private/runtime
  artifacts, and credentials/tokens/keys/webhooks;
- report summary movement from 9 to 8 missing families and 7 to 8
  covered-report-only families;
- the exact `gameplay_stress.companion_or_large_deck` matrix row;
- adjacent gameplay-stress rows remain separate.

## Contract Mismatches

No blocking mismatches were found.

The selected `covered_report_only_boundary` path was viable without parser
behavior, parser source, router, event schema, diagnostics, golden replay,
feature-equity, evidence-ledger, runtime, workbook, webhook, Apps Script,
analytics, AI/coaching, private smoke, generated artifact, raw fixture, or
decklist changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future companion / large-deck parser support, synthetic gameplay evidence,
deck-shape evidence, private evidence collection, or sanctioned companion /
large-deck fixture design needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata,
session-ledger metadata, summary movement, adjacent-row preservation, and
boundary assertions.

No new parser tests were added because the contract explicitly does not
authorize parser behavior changes or dedicated companion / large-deck fixture
claims.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 8 missing)`

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 6, forbidden 0, warnings 0

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed

```bash
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
for docfile in docs/contracts/parser_corpus_companion_large_deck_coverage.md docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md; do git diff --no-index --check /dev/null "$docfile"; rc=$?; if [ "$rc" -eq 1 ]; then true; elif [ "$rc" -ne 0 ]; then exit "$rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_companion_large_deck_coverage.md docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_runtime_surfaces.py tests/test_evidence_ledger.py tests/test_grp_id_candidates.py tests/fixtures/golden_replay tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/source, adjacent deck/card test, golden replay,
  tool, app entrypoint, or CI paths changed

Optional adjacent confidence check:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_runtime_surfaces.py tests/test_evidence_ledger.py tests/test_grp_id_candidates.py
```

- passed: 185 passed

## Open Risks

- `gameplay_stress.companion_or_large_deck` remains report-only boundary
  metadata, not parser-verified support.
- No dedicated committed companion or large-deck fixture exists in this slice.
- Existing deck/card evidence surfaces do not prove companion presence,
  companion legality, companion castability, large-deck size, complete
  decklist contents, deck identity, deck ownership, sideboard truth,
  hidden-card truth, archetype classification, gameplay advice, analytics
  truth, AI truth, coaching truth, release readiness, or production behavior.
- Future parser-owned support or synthetic/private evidence needs separate
  contract authority.
- Tracker #158 remains open.

## Next Recommended Role

Codex E: Module Reviewer / Contract-Test Reviewer.

Codex E should verify that the implementation is metadata/test/report-only,
that `gameplay_stress.companion_or_large_deck` is `covered_report_only` with
exact `["fixture_metadata_only"]` basis, that the only owning entry is
`companion_large_deck_boundary_report_v1`, that session-ledger counts do not
claim dedicated companion / large-deck fixtures, companion legality, or
decklist completion, and that adjacent gameplay-stress rows remain separate.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer / Contract-Test Reviewer for issue #408,
  parser corpus companion / large-deck coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/407
    - Previous merge commit: bece21b5d5e01ccaff110b7caaf6a1bfbe320bea
    - Branch: codex/parser-corpus-companion-large-deck-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_companion_large_deck_coverage.md
    - Implementation handoff: docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md
    - Risk tier: High

  Review goal:
    Verify the implementation satisfies the report-only boundary contract
    without turning adjacent deck/card evidence into parser-owned companion /
    large-deck truth.

  Check:
    - Only contract-authorized files changed.
    - gameplay_stress.companion_or_large_deck moved from missing to covered_report_only.
    - coverage_basis is exactly ["fixture_metadata_only"].
    - mythic_edge_entries is exactly ["companion_large_deck_boundary_report_v1"].
    - parser_event_families is empty.
    - session-ledger counts show zero dedicated companion fixtures, zero
      dedicated large-deck fixtures, zero companion-legality claims, and zero
      decklist-completion claims.
    - Notes explicitly say generic deck snapshots, submitted-deck card-content
      evidence, StartHook summaries, card identity provenance, and public
      taxonomy metadata do not prove companion presence, companion legality,
      large-deck size, complete decklists, deck identity, hidden-card truth,
      archetype classification, gameplay advice, analytics truth, AI truth,
      coaching truth, release readiness, or production behavior.
    - Adjacent gameplay_stress rows remain separate.
    - No parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/CI
      or production behavior changed.
    - No raw/private/generated/external corpus artifacts were committed.

  Suggested validation:
    - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 tools/check_agent_docs.py
    - python3 -m ruff check src tests tools
    - git diff --check
    - path-scoped secret/private marker and protected-surface checks for the changed package
    - optional adjacent deck/card tests if reviewer wants broader confidence

  Do not:
    - Target main directly.
    - Close #158 or #408.
    - Change parser behavior or downstream protected surfaces.
    - Commit raw/private/generated/external corpus artifacts, decklists, deck
      names, deck IDs, companion choices, sideboard choices, card choices,
      strategy notes, or secrets.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/407"
  previous_merge_commit: "bece21b5d5e01ccaff110b7caaf6a1bfbe320bea"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_companion_large_deck_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md"
  verdict: "companion_large_deck_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-companion-large-deck-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
