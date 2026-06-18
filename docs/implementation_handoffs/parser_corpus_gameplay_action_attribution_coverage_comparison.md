# Parser Corpus Gameplay Action-Attribution Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/410

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`gameplay_action_attribution_report_only_boundary_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `gameplay_action_attribution_boundary_report_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added count-only/report-only session metadata for
    `gameplay_action_attribution_boundary_report_v1`.
- `tests/test_corpus_parity_report.py`
  - Updated summary-count expectations.
  - Added focused manifest and session-ledger assertions for
    `gameplay_stress.action_attribution`.
  - Added exact matrix-row assertions for
    `gameplay_stress.action_attribution`.
  - Preserved exact adjacent row assertions for
    `gameplay_stress.companion_or_large_deck`,
    `gameplay_stress.event_ordering`, `gameplay_stress.conjure`, and
    `gameplay_stress.spellbook`.
- `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`

No parser source, parser behavior, gameplay-action extraction behavior,
opponent-card-observation behavior, parser event class, ActionLogRow shape,
router behavior, analytics ingest behavior, diagnostics source, golden replay
source, feature-equity source, evidence-ledger source, runtime source,
workbook export, webhook surface, Apps Script surface, AI/coaching behavior,
generated/private artifact, raw fixture, private log, private smoke output,
private action artifact, decklist, deck name, card-choice artifact, sideboard
choice, strategy note, runtime status file, failed post, workbook export, or
external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 14
- covered_report_only: 8
- partial: 3
- missing: 8
- blocked_private_evidence: 1
- blocked_external_boundary: 5
- `gameplay_stress.companion_or_large_deck`: `covered_report_only`
- `gameplay_stress.action_attribution`: `missing`
- `gameplay_stress.event_ordering`: `missing`
- `gameplay_stress.conjure`: `blocked_external_boundary`
- `gameplay_stress.spellbook`: `blocked_external_boundary`

Repo inspection confirmed existing gameplay-action, opponent-card-observation,
ActionLogRow, evidence-ledger, and analytics-ingest surfaces, but no committed
parser-owned action-attribution stress fixture and no contract authority to
infer causal action truth, hidden actions, hidden cards, opponent intent, why
an action happened, event ordering, player mistakes, or best-line truth from
those surfaces.

## Contract Changes Implemented

Implemented exactly one authorized coverage movement:

| Scenario family | Before | After |
| --- | --- | --- |
| `gameplay_stress.action_attribution` | `missing` | `covered_report_only` |

Preserved the adjacent family:

| Scenario family | Status |
| --- | --- |
| `gameplay_stress.event_ordering` | `missing` |

Added the required boundary metadata:

- entry id: `gameplay_action_attribution_boundary_report_v1`
- entry type: `session_ledger_entry`
- source kind: `committed_count_only_report`
- commit status: `committed`
- privacy class: `committed_count_only`
- sanitization status: `not_applicable_count_only`
- parser event families: none
- parser claim families:
  - `gameplay_action_attribution_boundary_report`
  - `gameplay_action_extraction_not_stress_coverage`
  - `opponent_card_observation_not_action_attribution_truth`
  - `action_log_row_not_causal_truth`
  - `analytics_ingest_not_parser_truth`
  - `event_ordering_not_claimed`
  - `hidden_action_inference_non_claim`
- coverage basis:
  - `fixture_metadata_only`

The coverage row intentionally does not claim parser support,
parser-behavior verification, synthetic gameplay fixture support,
action-attribution parser stress support, causal action truth, hidden actions,
hidden cards, opponent intent, why an action happened, event ordering, player
mistakes, best-line truth, gameplay advice, analytics truth, AI truth,
coaching truth, release readiness, merge readiness, deploy readiness, or
production behavior.

## Focused Test Coverage

`tests/test_corpus_parity_report.py` now pins:

- the `gameplay_action_attribution_boundary_report_v1` manifest entry shape;
- `parser_event_families: []`;
- exact `covered_report_only` status and `["fixture_metadata_only"]` basis;
- non-claim parser claim families;
- known-gap and review-note non-claims;
- the session-ledger entry shape;
- count-only parser coverage fields, including zero dedicated
  action-attribution fixtures, zero dedicated event-ordering fixtures, zero
  hidden-action claims, zero causal-intent claims, and zero event-ordering
  claims;
- report-only redaction flags for private action artifacts, private smoke
  outputs, generated/private/runtime artifacts, decklists, deck names, card
  choices, sideboard choices, strategy notes, opponent identifiers, private
  match context, and credentials/tokens/keys/webhooks;
- report summary movement from 8 to 7 missing families and 8 to 9
  covered-report-only families;
- the exact `gameplay_stress.action_attribution` matrix row;
- `gameplay_stress.event_ordering` remains missing.

## Contract Mismatches

No blocking mismatches were found.

The selected `covered_report_only_boundary` path was viable without parser
behavior, parser source, gameplay-action extraction changes,
opponent-card-observation changes, analytics ingest changes, router, event
schema, diagnostics, golden replay, feature-equity, evidence-ledger, runtime,
workbook, webhook, Apps Script, AI/coaching, private smoke, generated
artifact, raw fixture, private action artifact, or decklist changes.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future action-attribution parser stress support, synthetic gameplay evidence,
reduced expected-facts models, private evidence collection, or event-ordering
movement needs separate contract authority.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required corpus metadata,
session-ledger metadata, summary movement, adjacent-row preservation, and
boundary assertions.

No new parser or analytics tests were added because the contract explicitly
does not authorize parser behavior, gameplay-action extraction, opponent-card
observation, analytics ingest, or dedicated action-attribution fixture claims.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 7 missing)`

```bash
python3 tools/check_agent_docs.py
```

- passed: checked_files 32, errors 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 6, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
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
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok

```bash
for docfile in docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md; do git diff --no-index --check /dev/null "$docfile"; rc=$?; if [ "$rc" -eq 1 ]; then true; elif [ "$rc" -ne 0 ]; then exit "$rc"; fi; done
```

- passed

```bash
LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py
```

- passed: no matches

```bash
find . \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \) -print
```

- passed: no generated SQLite artifacts found

```bash
git diff --name-only -- src tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_analytics_gameplay_action_ingest.py tests/test_evidence_ledger.py tests/fixtures/golden_replay tools main.py live_print_filtered_v11_match_summary.py .github
```

- passed: no protected parser/source, adjacent gameplay-action, golden
  replay, tool, app entrypoint, or CI paths changed

Optional adjacent confidence check:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_analytics_gameplay_action_ingest.py tests/test_evidence_ledger.py
```

- passed: 147 passed

## Open Risks

- `gameplay_stress.action_attribution` remains report-only boundary metadata,
  not parser-verified support.
- No dedicated committed action-attribution fixture exists in this slice.
- `gameplay_stress.event_ordering` remains missing and needs a separate child
  issue/contract for movement.
- Existing gameplay-action, opponent-card-observation, ActionLogRow,
  evidence-ledger, and analytics-ingest surfaces do not prove
  action-attribution parser stress support, causal action truth, hidden
  actions, hidden cards, opponent intent, why an action happened, event
  ordering, player mistakes, gameplay advice, analytics truth, AI truth,
  coaching truth, release readiness, or production behavior.
- Future parser-owned support or synthetic/private evidence needs separate
  contract authority.
- Tracker #158 remains open.

## Next Recommended Role

Codex E: Module Reviewer / Contract-Test Reviewer.

Codex E should verify that the implementation is metadata/test/report-only,
that `gameplay_stress.action_attribution` is `covered_report_only` with exact
`["fixture_metadata_only"]` basis, that the only owning entry is
`gameplay_action_attribution_boundary_report_v1`, that session-ledger counts
do not claim dedicated action-attribution fixtures, event-ordering fixtures,
hidden actions, causal intent, or event ordering, and that
`gameplay_stress.event_ordering` remains missing.

## Pasteable Codex E Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer / Contract-Test Reviewer for issue #410,
  parser corpus gameplay action-attribution coverage.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/410
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/409
    - Previous merge commit: 574cd23d046d19fb64266d079d1d6173d23f7cf4
    - Branch: codex/parser-corpus-gameplay-action-attribution-coverage
    - Base branch: codex/parser-parity
    - Contract: docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md
    - Implementation handoff: docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md
    - Report: docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md
    - Risk tier: High

  Review goal:
    Verify the implementation satisfies the report-only boundary contract
    without turning generic gameplay-action extraction, opponent-card
    observations, ActionLogRow surfaces, analytics ingest, evidence-ledger
    provenance, or public taxonomy metadata into parser-owned
    action-attribution stress truth.

  Check:
    - Only contract-authorized files changed.
    - gameplay_stress.action_attribution moved from missing to covered_report_only.
    - gameplay_stress.event_ordering remains missing.
    - coverage_basis is exactly ["fixture_metadata_only"].
    - mythic_edge_entries is exactly ["gameplay_action_attribution_boundary_report_v1"].
    - parser_event_families is empty.
    - session-ledger counts show zero dedicated action-attribution fixtures,
      zero dedicated event-ordering fixtures, zero hidden-action claims, zero
      causal-intent claims, and zero event-ordering claims.
    - Notes explicitly say gameplay-action extraction, opponent-card
      observations, ActionLogRow surfaces, analytics gameplay-action ingest,
      evidence-ledger provenance, and public taxonomy metadata do not prove
      action-attribution stress support, causal truth, hidden actions, hidden
      cards, opponent intent, event ordering, player mistakes, gameplay advice,
      analytics truth, AI truth, coaching truth, release readiness, or
      production behavior.
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
    - optional adjacent gameplay-action/opponent-observation/analytics tests

  Do not:
    - Target main directly.
    - Close #158 or #410.
    - Change parser behavior or downstream protected surfaces.
    - Commit raw/private/generated/external corpus artifacts, private action
      artifacts, decklists, deck names, card choices, sideboard choices,
      strategy notes, or secrets.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/410"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/409"
  previous_merge_commit: "574cd23d046d19fb64266d079d1d6173d23f7cf4"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md"
  verdict: "gameplay_action_attribution_report_only_boundary_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-action-attribution-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
```
