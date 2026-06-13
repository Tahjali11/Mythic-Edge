# Parser Corpus Sealed Deckbuild Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/361

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_sealed_deckbuild_coverage.md`

## Role Performed

Codex C: Module Implementer

## Verdict

`synthetic_sealed_deckbuild_coverage_ready_for_review`

## Files Changed

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - Added `sealed_deckbuild_synthetic_v1`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Added matching synthetic session ledger metadata.
- `tests/test_corpus_parity_report.py`
  - Updated summary counts and sealed deckbuild row assertions.
  - Added focused checks for the synthetic entry shape and privacy flags.
- `tests/test_state.py`
  - Added a synthetic sealed context plus submit-deck signal test using
    existing event and state paths.
- `docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md`
  - New Codex C evidence report.
- `docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md`
  - New implementation handoff.

The Codex B contract was present as an untracked source artifact:

- `docs/contracts/parser_corpus_sealed_deckbuild_coverage.md`

No parser source, parser event class, router, parser state final
reconciliation, raw fixture, golden replay fixture, feature-equity baseline,
runtime artifact, workbook export, generated/private artifact, submitted deck
artifact, or external corpus content was added or changed.

## Pre-Change Comparison

Before editing, the repo-owned corpus parity report showed:

- status: `partial_coverage_map_ready`
- covered_committed: 6
- covered_synthetic: 4
- missing: 26
- `core_gameplay.sealed_entry`: `covered_synthetic`
- `core_gameplay.sealed_deckbuild`: `missing`
- `core_gameplay.sealed_matches`: `covered_synthetic`

This matched the contract's expected starting state after issue #359.

## Contract Changes Implemented

Implemented exactly one authorized coverage promotion:

| Scenario family | Before | After |
| --- | --- | --- |
| `core_gameplay.sealed_deckbuild` | `missing` | `covered_synthetic` |

Preserved the required sealed lifecycle boundary:

- `core_gameplay.sealed_entry` remains `covered_synthetic`.
- `core_gameplay.sealed_matches` remains `covered_synthetic`.

Added the required synthetic metadata:

- entry id: `sealed_deckbuild_synthetic_v1`
- session id: `sealed_deckbuild_synthetic_v1`
- source kind: `synthetic_committed_fixture`
- privacy class: `synthetic_committable`
- sanitization status: `synthetic`
- parser event families: `MatchState`, `ClientAction`
- parser claim families:
  - `sealed_event_identity`
  - `sealed_submit_deck_signal`
  - `bounded_submit_deck_shape`
  - `deckbuild_privacy_boundary`
- coverage basis: `fixture_metadata_only`, `parser_behavior_verified`

The corpus row includes the required non-claim that sealed deckbuild coverage
is bounded submit-deck signal metadata only.

## Focused Test Coverage

`tests/test_state.py` now includes a synthetic sealed deckbuild signal path
through existing parser-owned model/state behavior. It verifies that a sealed
event ID plus a `submit_deck_resp` client action sets
`MatchSummary.submit_deck_seen` without storing deck-card or sideboard-card
fields in summary output.

`tests/test_corpus_parity_report.py` now pins the manifest entry, session
ledger entry, corpus summary counts, sealed deckbuild coverage row, and
privacy redaction flags.

Existing `tests/test_client_actions_parser.py` already covers specialized
submit-deck parsing and bounded payload shape behavior; it was included in the
validation bundle.

## Contract Mismatches

No blocking mismatches were found.

The manifest/session ledger schemas accepted the synthetic entry shape. No
parser behavior change was required.

## Missing Safeguards

No additional safeguard implementation was needed for this slice.

Future sealed pool or submitted-deck card-content corpus work remains outside
this issue and will require a separate privacy-specific contract.

## Missing Or Weak Tests

No missing focused tests remain for the contract-required metadata behavior.

Future replay or local-private sealed deckbuild evidence should not inherit
support claims from this synthetic metadata entry.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 25 missing)`

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py
```

- passed: 135 passed

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
git diff --check
```

- passed with no output

Path-scoped checks for the changed implementation/report files included the
untracked source contract:

```bash
printf '%s\n' docs/contracts/parser_corpus_sealed_deckbuild_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: scanned_paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_sealed_deckbuild_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: changed_paths 7, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_sealed_deckbuild_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

- passed: selection_status ok
- required checks selected: diff check, protected-surface gate, Ruff,
  secret/private-marker scan, `tests/test_corpus_parity_report.py`, and
  `tests/test_state.py`
- recommended check selected: agent docs checker

The literal contract scan command was also attempted with
`tests/test_client_actions_parser.py` included. That file is unchanged in this
implementation, but full-file scanning it reports pre-existing
`raw_player_log_content` findings from older synthetic parser tests:

```bash
printf '%s\n' docs/contracts/parser_corpus_sealed_deckbuild_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
```

- failed: scanned_paths 8, forbidden 14, warnings 0
- all findings were in unchanged `tests/test_client_actions_parser.py`
- no findings were reported in the changed implementation/report files

## Still Unverified

- No CI was inspected.
- No PR was opened.
- No actual private logs or app data were inspected.
- No external corpus contents were fetched or inspected.
- No sealed pool, submitted-deck card-content, decklist, deck-name, or
  strategy-note evidence was attempted.

## Residual Risks

- This is synthetic metadata coverage, not replayed sealed private log
  coverage.
- Sealed pool and submitted-deck card-content truth remain intentionally
  outside this slice.
- Corpus coverage remains review metadata and not parser truth, workbook
  truth, analytics truth, AI truth, merge readiness, deploy readiness, or
  tracker completion authority.

## Next Recommended Role

Codex E: Module Reviewer.

If review is clean, route to Codex F for module submission to
`codex/parser-parity`. If review finds overclaiming, privacy leakage, or scope
drift, route to Codex D with concrete findings.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #361 under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/361

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/359

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/360

Previous merge commit:
369e2d5396f0fc9b42565f102a88e6ad498bedf7

Branch:
codex/parser-corpus-sealed-deckbuild-coverage

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_sealed_deckbuild_coverage.md

Artifacts to review:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- tests/test_state.py
- docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md
- docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md

Review focus:
- Verify only core_gameplay.sealed_deckbuild moved from missing to covered_synthetic.
- Verify core_gameplay.sealed_entry remains covered_synthetic.
- Verify core_gameplay.sealed_matches remains covered_synthetic.
- Verify the new entry is synthetic, committed, and privacy-safe.
- Verify the focused state test uses existing parser/state behavior without parser source changes.
- Verify no external/raw/private log artifacts, submitted card-list values, deck contents, sealed pool contents, deck names, card choices, or strategy notes are committed.
- Verify corpus report notes preserve deckbuild privacy non-claims.

Expected verdict if clean:
ready_for_module_submitter

Do not:
- Target main directly.
- Close #158 or #361.
- Implement parser behavior changes.
- Change event identity, client-action parsing, submit-deck parsing, card-list normalization, parser state, router, parser event classes, match/game identity, or deduplication behavior.
- Add raw log fixtures, golden replay fixtures, feature-equity baseline changes, external corpus contents, private logs, generated/private artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.
- Claim full Mythic Edge corpus parity, sealed pool support, submitted-deck card-content truth, decklist support, archetype classification, gameplay advice, AI truth, analytics truth, or coaching truth.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/361"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/359"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/360"
  previous_merge_commit: "369e2d5396f0fc9b42565f102a88e6ad498bedf7"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_sealed_deckbuild_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md"
  verdict: "synthetic_sealed_deckbuild_coverage_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-deckbuild-coverage"
  base_branch: "codex/parser-parity"
```
