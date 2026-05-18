# Parser Feature-Equity Corpus Ratchet Contract-Test Report

## Findings

No blocking findings.

### Non-blocking: golden replay status propagation has only partial direct ratchet coverage

The implementation handles golden replay `fail`, `diff`, `review`, and
`degraded` statuses in the ratchet aggregation path
(`src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py:65`). The
private-input test exercises a golden replay failure path, and the baseline
mismatch test exercises report-only `diff` behavior. There is not yet a focused
ratchet test that monkeypatches `golden_replay.run_golden_replay()` to return
`diff`, `review`, or `degraded` and asserts those statuses appear in
`status_reasons` as required by the contract
(`docs/contracts/parser_feature_equity_corpus_ratchet.md:907`).

This is not blocking because the code path is direct, adjacent golden replay
tests cover those statuses, and the current validation shows the committed
corpus reports `ok`. Add a small propagation test later if this module sees
more status handling changes.

### Non-blocking: ratchet-only counts currently replay fixture lines through the parser

The contract says not to parse raw log lines separately when golden replay owns
routing for the manifest inputs
(`docs/contracts/parser_feature_equity_corpus_ratchet.md:829`). The
implementation first runs golden replay for validation and fixture-local
expected checks, then replays the same explicit fixture through `LineBuffer` and
`Router` to collect ratchet-only count sections
(`src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py:230`). This does
not copy raw lines, does not reinterpret parser truth outside the parser, and
does not bypass golden replay failures. It is still worth treating as bridge
code: if golden replay later exposes the needed observed event/count data, the
ratchet should consume that shared structure rather than maintaining a second
fixture replay loop.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/119

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

## Contract

- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

## Contract Summary

The feature-equity corpus ratchet must be a report-only, count-only coverage
tool over explicit committed golden replay manifests. It must compare observed
coverage counts to a manually reviewed baseline, keep `ok`, `review`, and
`diff` non-gating, fail invalid or private inputs, avoid raw log or full payload
storage, and avoid changing parser/runtime/workbook/webhook/App Script
behavior.

## Checks Run

```powershell
git fetch --prune origin
gh issue view 119 --json number,title,state,url,body,labels
git status --short --branch
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
git diff --check
py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py
py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m ruff check src tests tools
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
@'
docs/contracts/parser_feature_equity_corpus_ratchet.md
src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
tests/test_feature_equity_corpus_ratchet.py
tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_protected_surfaces.py --base origin/main
py -m pytest -q
```

Additional temporary report privacy probe:

```powershell
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json --out $env:TEMP\feature_equity_corpus_ratchet_review_report.json
rg -n "opening_hand|raw_game_state|C:\\Users|script\.google|hooks\.|spreadsheets|Bearer|api[_-]?key|secret|token" $env:TEMP\feature_equity_corpus_ratchet_review_report.json
```

## Results

- Issue #119 is open and targets `codex/parser-reliability-intelligence`.
- Branch is even with `origin/codex/parser-reliability-intelligence`.
- New ratchet files are local/untracked, as expected before Codex F.
- Focused ratchet tests: `7 passed in 0.67s`.
- Ratchet baseline command: `Feature-equity corpus ratchet: ok (2 manifests, 2 source files)`.
- Golden replay/diagnostics/saved-event slice: `48 passed in 0.85s`.
- GRE/parser reliability slice: `41 passed in 0.69s`.
- Event schema snapshots: `6 passed in 0.57s`.
- Golden replay CLI: `pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Path-scoped protected-surface gate for the issue #119 files:
  `changed_paths: 5`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Branch-wide protected-surface gate against `origin/main` passed with
  `forbidden: 0` and 9 warnings from earlier parser reliability branch work
  outside issue #119.
- Full local suite: `743 passed in 4.71s`.
- Generated temp report private-marker probe found no forbidden/private markers.
- `tools/check_secret_patterns.py` is not present on this branch; this was
  recorded as a validation limitation.

## Confirmed Contract Matches

- The ratchet is isolated to a new report-only module and focused tests.
- The committed baseline is count-only JSON with no raw log lines or full parser
  payloads.
- Inputs are explicit golden replay manifest files or directories expanded to
  `*.manifest.json`.
- Directory expansion is sorted and deterministic by repo-relative path.
- Public object/schema constants match the contract.
- Public APIs include `build_feature_equity_corpus_report()`,
  `write_feature_equity_corpus_report()`, and `main()`.
- `ok`, `review`, `diff`, and `fail` status precedence matches the contract.
- Missing baseline with no supplied path returns `review` with
  `baseline_missing`.
- Invalid baseline schema returns `fail`.
- Count mismatch returns `diff` while CLI exit remains `0`.
- Invalid/private manifest input returns `fail` and does not copy raw fixture
  content into the report.
- Reports write only when `--out` or `report_path` is explicitly supplied.
- No `--update-baseline`, `--bless`, `--accept`, or auto-refresh path exists.
- Generated reports include inputs, baseline, observed, comparison, privacy,
  protected surfaces, and limitations sections.
- Observed sections cover input counts, router stats, event family counts, event
  kind counts, payload type counts, parser claim counts, GameState evidence
  counts, truncation/data-loss, and unknown/degradation counts.
- Protected surfaces are reported false and path-scoped protected-surface checks
  found no issue #119 warnings.
- No workbook schema, webhook payload shape, Apps Script behavior, parser
  behavior, parser state final reconciliation, parser event class, match/game
  identity, deduplication, runtime status, failed-post, workbook export, live
  workbook, deployment, CI-gate, Pyright-gate, secret, raw private log, or
  production behavior change was found in the issue #119 scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests.

Non-blocking future hardening:

- Add direct ratchet-level monkeypatch tests for golden replay `diff`, `review`,
  and `degraded` propagation if this module changes again.
- If golden replay exposes ratchet-ready observed count data later, add a
  regression test that prevents the ratchet from growing a divergent fixture
  replay path.

## Drift Notes

- Repo drift: expected local untracked issue #119 additions only.
- Branch drift: branch-wide protected-surface warnings are from earlier parser
  reliability work already present on `codex/parser-reliability-intelligence`;
  the path-scoped issue #119 check is clean.
- Parser/runtime/workbook/webhook/App Script drift: none found in the reviewed
  issue #119 scope.
- Secret/private-data drift: no raw private log, local path, webhook URL,
  workbook ID, generated data, runtime status file, failed post, or workbook
  export was found in the reviewed baseline or generated temp report.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #119.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/119

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Branch:
codex/parser-reliability-intelligence

Reviewed artifacts:
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md
- docs/contract_test_reports/parser_feature_equity_corpus_ratchet.md
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json

Codex E verdict:
No blocking findings. The module is ready to submit.

Expected scope:
- Stage only the issue #119 files listed above.
- Do not stage unrelated parser reliability branch files unless they are already part of this branch baseline and explicitly required.
- Commit the reviewed issue #119 package.
- Push codex/parser-reliability-intelligence.
- Open a draft PR targeting the parser reliability integration branch, not main.
- Link issue #119 and tracker #47.

Validation evidence from Codex E:
- py -m pytest -q tests\test_feature_equity_corpus_ratchet.py -> 7 passed
- py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json -> ok
- py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py -> 48 passed
- py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py -> 41 passed
- py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed
- py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay -> pass
- py -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface gate for issue #119 files -> passed with 0 warnings
- py -m pytest -q -> 743 passed

Residual risks to mention in the PR:
- Remote CI has not run yet.
- tools/check_secret_patterns.py is not present on this branch, so secret scanning was limited to the contract-specific baseline/report probe and protected-surface checks.
- Ratchet-level tests do not directly monkeypatch golden replay diff/review/degraded status propagation; current implementation handles those statuses and adjacent golden replay tests cover status production.
- Ratchet-only observed counts currently replay explicit fixture lines through LineBuffer/Router after golden replay validation; this is deterministic and report-only, but should be consolidated if golden replay later exposes ratchet-ready observed counts.

Stop conditions:
- Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, generated card data, runtime status files, failed posts, workbook exports, production behavior, CI gate behavior, Pyright gate behavior, secrets, credentials, raw private logs, or local-only artifacts.
- Do not add an automatic baseline update, bless, accept, or refresh path.
- Do not target main.
- Do not mark tracker #47 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/119"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/parser_feature_equity_corpus_ratchet.md"
  implementation_handoff: "docs/implementation_handoffs/parser_feature_equity_corpus_ratchet_comparison.md"
  review_artifact: "docs/contract_test_reports/parser_feature_equity_corpus_ratchet.md"
  branch: "codex/parser-reliability-intelligence"
  verdict: "ready for Codex F"
  findings:
    blocking: []
    non_blocking:
      - "Direct ratchet-level tests for golden replay diff/review/degraded propagation would be useful future hardening."
      - "Ratchet-only counts replay explicit fixture lines through LineBuffer/Router after golden replay validation; consolidate later if golden replay exposes ratchet-ready observed count data."
  validation:
    - "py -m pytest -q tests\\test_feature_equity_corpus_ratchet.py -> 7 passed in 0.67s"
    - "py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\\fixtures\\golden_replay --baseline tests\\fixtures\\feature_equity_corpus\\feature_equity_corpus_baseline.v1.json -> ok"
    - "py -m pytest -q tests\\test_golden_replay_harness.py tests\\test_parser_diagnostics_mode.py tests\\test_saved_event_replay.py -> 48 passed in 0.85s"
    - "py -m pytest -q tests\\test_gre_game_state_parser.py tests\\test_gre_annotations_parser.py tests\\test_gre_timers_parser.py tests\\test_gre_game_state_diff_parser.py tests\\test_opponent_card_observations.py tests\\test_gsm_truncation_parser.py -> 41 passed in 0.69s"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed in 0.57s"
    - "py -m mythic_edge_parser.app.golden_replay tests\\fixtures\\golden_replay -> pass"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface gate for issue #119 files -> passed with 0 warnings"
    - "py -m pytest -q -> 743 passed in 4.71s"
    - "tools/check_secret_patterns.py unavailable on this branch"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not stage unrelated files outside the issue #119 package."
    - "Do not change parser behavior or protected runtime/workbook/webhook/App Script surfaces."
    - "Do not add automatic baseline update or CI-gating behavior."
    - "Do not target main."
    - "Do not mark tracker #47 complete."
```
