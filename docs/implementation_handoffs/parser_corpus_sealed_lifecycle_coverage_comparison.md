# Parser Corpus Sealed Lifecycle Coverage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/355

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`

## Role Performed

Codex C: Module Implementer / Report-Only Coverage Inspector

## Verdict

`report_only_sealed_lifecycle_inspection_ready_for_review`

No implementation fix was needed or authorized. The current parser has useful
sealed-adjacent ingredients, but the corpus still has no Mythic Edge-owned
sealed entry, sealed deckbuild, or sealed match evidence. The three sealed
rows remain `missing` as required by the contract.

## Files Changed

- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
  - New Codex C report-only sealed lifecycle inspection.
- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`
  - New Codex C implementation handoff.

No parser code, parser tests, corpus manifest rows, session ledger rows,
fixtures, runtime artifacts, workbook exports, or generated/private artifacts
were changed.

## Dependency Check

PR #354 is present:

- previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/354
- required merge commit:
  `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- local HEAD:
  `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- merge-base ancestry check: passed

## Confirmed Matches

- The contract artifact exists at
  `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`.
- The current corpus parity report remains
  `partial_coverage_map_ready`.
- The three in-scope sealed rows are present and remain `missing`:
  - `core_gameplay.sealed_entry`
  - `core_gameplay.sealed_deckbuild`
  - `core_gameplay.sealed_matches`
- Each sealed row has `coverage_basis == ["external_reference_only"]` and no
  Mythic Edge entries.
- The #352 taxonomy audit maps public sealed labels to these rows as reference
  taxonomy only and does not claim parser support.
- Event identity classification can recognize sealed context from
  parser-produced event fields.
- Event lifecycle parsing can recognize generic entry lifecycle markers.
- Submit-deck parsing and state summary support can observe submit-deck
  signals.
- No current owned fixture/report ties those ingredients together as sealed
  lifecycle corpus evidence.

## Contract Mismatches

No blocking mismatches were found.

The contract requires report-only inspection and explicitly forbids V1 status
promotion. Current repo behavior matches that boundary.

## Missing Safeguards

No new safeguard implementation was authorized in this issue.

Future sealed deckbuild work needs an explicit privacy safeguard before any
committed fixture or report can include card-content-derived evidence. The
recommended safe shape is summary-only metadata such as sealed context plus
submit-deck signal/count/signature, not raw card lists or sealed pool content.

## Missing Or Weak Tests

No tests were added because V1 is report-only.

Observed future test needs:

- A sealed entry lifecycle fixture/report test that proves sealed context plus
  lifecycle markers through the normal parser route.
- A sealed match fixture/report test that proves sealed context through match
  state, GameState, game result, and summary identity.
- A sealed deckbuild privacy test or report validation that rejects raw card
  lists, private pool data, deck names, and private log snippets.

Those tests should be scoped by future contracts before implementation.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 28 missing)`

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py
```

- passed: 161 passed

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
git diff --check
```

- passed with no output for tracked local diffs

```bash
git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed:
  - secret/private-marker scan: scanned_paths 0, forbidden 0, warnings 0
  - protected-surface gate: changed_paths 0, forbidden 0, warnings 0
  - validation selector: selection_status ok, advisory zero_changed_paths

Because this work is uncommitted and includes untracked Markdown files, Codex C
also runs explicit changed-file scans over:

- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`

Explicit changed-file results:

- secret/private-marker scan: passed, scanned_paths 3, forbidden 0,
  warnings 0
- protected-surface gate: passed, changed_paths 3, forbidden 0, warnings 0
- validation selector: selection_status ok; required checks were diff check,
  protected-surface gate, and secret/private-marker scan; recommended check was
  agent docs checker
- untracked no-index whitespace checks: passed for all three Markdown files

## Still Unverified

- No CI was inspected.
- No PR was opened.
- No external corpus contents were fetched or inspected.
- No actual private logs or local private app data were inspected.
- No future fixture safety policy was implemented.
- No parser behavior was changed or expanded.

## Remaining Risks

- Sealed lifecycle coverage may require multiple future children because
  sealed entry, sealed deckbuild, and sealed match evidence have different
  privacy and parser-behavior boundaries.
- Sealed deckbuild is especially privacy-sensitive because raw submitted deck
  contents or sealed pool data must not enter committed artifacts.
- Event identity sealed classification is useful context, but it is not enough
  for corpus coverage without lifecycle or match evidence.
- Generic event lifecycle and submit-deck signals are useful ingredients, but
  neither proves sealed support without sealed event context.

## Next Recommended Role

Codex E: Module Reviewer.

If Codex E finds no issue, route to Codex F for docs-only submission. If Codex
E finds overclaiming or missing non-claims, route to Codex D. Future coverage
promotion should start with Codex A or Codex B to split sealed entry, sealed
matches, and sealed deckbuild into narrower implementation contracts.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #355 under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/355

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Branch:
codex/parser-corpus-sealed-lifecycle-coverage

Contract:
docs/contracts/parser_corpus_sealed_lifecycle_coverage.md

Artifacts to review:
- docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md
- docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md

Review focus:
- Verify the V1 report does not change sealed corpus statuses.
- Verify no external/raw/private log artifacts or deck contents are committed.
- Verify parser behavior is inspected but not changed.
- Verify core_gameplay.sealed_entry, core_gameplay.sealed_deckbuild, and core_gameplay.sealed_matches remain missing.
- Verify sealed entry, deckbuild, and match non-claims are explicit.
- Verify future coverage paths require Mythic Edge-owned evidence.
- Verify the report does not claim sealed support from taxonomy mapping alone.

Expected verdict if clean:
ready_for_module_submitter

Do not:
- Target main directly.
- Close #158 or #355.
- Implement parser behavior changes.
- Change corpus manifest or session ledger statuses.
- Add committed log fixtures.
- Import, copy, mirror, or commit Manasight raw logs, compressed corpus files, raw session payloads, or external corpus contents.
- Commit private Player.log excerpts, private local logs, raw sealed pool data, raw submitted decklists, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.
- Claim full Mythic Edge corpus parity or sealed support from taxonomy mapping alone.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/355"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/354"
  previous_merge_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_sealed_lifecycle_coverage.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md"
  expected_handoff: "docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md"
  verdict: "report_only_sealed_lifecycle_inspection_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-lifecycle-coverage"
  base_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
```
