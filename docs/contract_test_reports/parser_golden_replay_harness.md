# Parser Golden Replay Harness Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/48

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/49

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/110

Previous merge commit: `a61ed4e5cd8898e25913796080a9c46e66fcff8a`

## Contract

- `docs/contracts/parser_golden_replay_harness.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_golden_replay_harness.md`
- `docs/implementation_handoffs/parser_golden_replay_harness_comparison.md`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- `tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json`
- `tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json`

Unrelated local files observed and excluded from this review:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Codex D Fixer Update

Codex D addressed the Codex E blocking finding with a test-only patch in
`tests/test_golden_replay_harness.py`.

Added focused coverage for:

- expected `degraded` status from manifest-declared known gaps;
- `degraded_cli_exit_code: 0` report metadata;
- CLI exit code `0` for expected degraded manifests;
- CLI nonzero behavior for `diff`;
- CLI nonzero behavior for validation `fail`.

No implementation behavior change was required.

## Findings

### Resolved: focused tests did not cover the full status and CLI exit contract

The contract requires the harness to return nonzero on `fail`, `diff`, or
unexpected `review` outcomes and says the expected `degraded` exit-code
decision must be explicit in tests and report metadata
(`docs/contracts/parser_golden_replay_harness.md:118`). It also defines
`degraded` as a first-class report status
(`docs/contracts/parser_golden_replay_harness.md:634`).

The implementation records the v1 degraded decision in report metadata
(`src/mythic_edge_parser/app/golden_replay.py:153`) and the current CLI return
path would return zero for `degraded`
(`src/mythic_edge_parser/app/golden_replay.py:828`). A local behavior probe
confirmed a manifest with an expected known gap returns `degraded` and CLI exit
code `0`.

At review time, `tests/test_golden_replay_harness.py` covered passing
manifests, API-level `diff`, API-level `fail`, review status, explicit report
writing, and required CLI input, but did not include a focused
degraded-status test or a test asserting the degraded CLI exit-code decision.
It also did not assert CLI nonzero behavior for `fail` and `diff`, only for
`review`.

Codex D added the requested focused coverage:

- add a focused manifest mutation with `known_gaps` or
  `expected_degradation` that asserts `run_golden_replay()` returns
  `degraded`, the report metadata keeps `degraded_cli_exit_code: 0`, and
  `main()` exits `0`;
- add small CLI assertions that a diff manifest and a validation-fail manifest
  return nonzero.

No implementation behavior change is indicated by this finding.

## Contract-Test Verdict

Implementation behavior matches the reviewed contract in the exercised paths,
and Codex D has added the missing focused status/CLI tests. Route back to Codex
E for a review-only confirmation pass before Codex F.

Next recommended role: Codex E: Module Reviewer.

## Contract Summary

The golden replay harness must replay explicit committed sanitized
`Player.log` fixture slices through the normal parser path, compare
parser-owned observed outputs against explicit reduced expected manifests, and
produce deterministic local reports with `pass`, `degraded`, `review`, `diff`,
and `fail` statuses. It must not become a second parser, a truth source, a
bless/update shortcut, or a downstream workbook/webhook/App Script/AI authority.

## Checks Run

```bash
git fetch --prune
gh issue view 48 --json number,title,state,body,labels,url
gh issue view 47 --json number,title,state,body,url
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' src/mythic_edge_parser/app/golden_replay.py tests/test_golden_replay_harness.py tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json docs/contracts/parser_golden_replay_harness.md docs/implementation_handoffs/parser_golden_replay_harness_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

Codex D fixer validation:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' src/mythic_edge_parser/app/golden_replay.py tests/test_golden_replay_harness.py tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json docs/contracts/parser_golden_replay_harness.md docs/implementation_handoffs/parser_golden_replay_harness_comparison.md docs/contract_test_reports/parser_golden_replay_harness.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
```

Additional non-mutating behavior probe:

```bash
python3 - <<'PY'
import json, tempfile
from pathlib import Path
from mythic_edge_parser.app import golden_replay

payload = json.loads(Path("tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json").read_text())
payload["coverage"]["known_gaps"] = ["fixture_gap_probe"]
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "degraded.manifest.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    result = golden_replay.run_golden_replay(p)
    print(result.status)
    print(result.degradation)
    print(golden_replay.build_golden_replay_report([p])["metadata"].get("degraded_cli_exit_code"))
    print(golden_replay.main([str(p)]))
PY
```

## Results

- Issue #48: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- Tracker #47: open, parser reliability/intelligence backlog confirmed.
- Focused golden replay tests after Codex D: `12 passed in 0.11s`.
- Adjacent parser reliability tests after Codex D: `38 passed in 0.08s`.
- Golden replay CLI over committed manifests:
  `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Protected-surface gate against `origin/main`: `changed_paths: 26`,
  `forbidden: 0`, `warnings: 4`, `result: passed`.
- Explicit #48 local changed-path protected-surface gate:
  `changed_paths: 7`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Full local test suite after Codex D: `707 passed in 1.04s`.
- Degraded behavior probe: `degraded`, `known_gaps:fixture_gap_probe`,
  metadata `degraded_cli_exit_code: 0`, CLI exit code `0`.
- `tools/select_validation.py`: unavailable on this branch.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The four protected-surface warnings from the `origin/main` branch diff are
from previously merged parser reliability issue #107 surfaces:
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`. The explicit #48 local
changed-path protected-surface check has no warnings.

## Confirmed Contract Matches

- `build_golden_replay_report()`, `run_golden_replay()`, and `main()` exist in
  `src/mythic_edge_parser/app/golden_replay.py`.
- The module CLI runs through `python3 -m mythic_edge_parser.app.golden_replay`
  and accepts manifest files or directories.
- Inputs are explicit manifests; the harness does not implicitly read private
  local `Player.log` paths.
- Fixture paths are resolved as repo-relative, non-absolute paths under the
  project root.
- Required manifest object, schema, linked issue, contract authorization,
  source kind, sanitization status, privacy class, raw-private-log flag,
  coverage lists, and expected sections are validated before replay.
- Manifest and fixture content are checked by a narrow local forbidden-marker
  screen, and failure reports include category labels rather than raw fixture
  lines or full secret-like values.
- The committed manifests compare reduced parser-owned facts rather than broad
  whole-object snapshots.
- The replay path uses `LineBuffer`, `Router`, parser modules, transforms, and
  parser state.
- Diagnostics mode is reused only as observer evidence and transport health
  remains separate from parser-output comparisons.
- Saved-event replay is not used as a raw fixture replay substitute.
- Expected manifests cover router stats, event family counts, event sequence,
  diagnostics summary, truncation/data-loss evidence, unknown/degradation
  evidence, parser state, final reconciliation, and selected parser-owned row
  values.
- No automatic expected-output bless/update behavior exists.
- Reports are written only when `--out` is explicitly supplied.
- Suite status precedence is implemented as `fail`, `diff`, `review`,
  `degraded`, then `pass`.
- `fail`, `diff`, `review`, `degraded`, and `pass` behavior exists in the
  implementation.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, output transport, parser event
  classes, match/game identity, deduplication, secrets, environment variables,
  raw logs, generated data, runtime status files, failed posts, workbook
  exports, or production deployment behavior changes were found in the #48
  module scope.

## Contract Mismatches

No implementation behavior mismatch found in exercised paths.

The previously blocking item was missing focused test coverage for
contract-required status and CLI semantics. Codex D resolved this with
test-only coverage.

## Missing Tests

Resolved by Codex D:

- Focused degraded-status test.
- Focused degraded CLI exit-code test, including
  `degraded_cli_exit_code: 0` report metadata.
- Focused CLI nonzero test for `diff` status.
- Focused CLI nonzero test for `fail` status.

Already covered:

- passing committed manifests;
- reduced expected diff payload shape;
- privacy metadata validation failure;
- absolute/private fixture path rejection;
- legacy unclassified metadata review behavior;
- forbidden fixture content redaction;
- CLI directory input and explicit `--out` report writing;
- CLI nonzero review behavior;
- explicit manifest input requirement.

## Drift Notes

- Repo drift: expected addition of a golden replay harness module, focused
  tests, manifest files, contract, handoff, and this contract-test report.
- Parser behavior drift: none found.
- Parser state final reconciliation drift: none found.
- Parser event class drift: none found.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Output transport drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local-data drift: no raw private logs, generated runtime artifacts, failed
  posts, runtime status files, or workbook exports were added in the reviewed
  #48 scope.
- Previous issue #107 drift: still present in branch comparisons against
  `origin/main` and not part of this #48 finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- The active branch does not contain `tools/select_validation.py` or
  `tools/check_secret_patterns.py`; these optional hardening validations were
  recorded as unavailable.
- The v1 forbidden-content screen is intentionally narrow and is not a full
  secret scanner.
- The committed manifests currently reference existing sanitized regression
  slice fixtures rather than adding new log slice files under
  `tests/fixtures/golden_replay/`.

## Recommendation

Route back to Codex E: Module Reviewer for a review-only confirmation pass.

If Codex E finds no blocking issues, proceed to Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex E: Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for parser reliability issue #48.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/48

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_golden_replay_harness.md
- docs/implementation_handoffs/parser_golden_replay_harness_comparison.md
- docs/contract_test_reports/parser_golden_replay_harness.md
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_golden_replay_harness.py
- tests/fixtures/golden_replay/*.manifest.json

Goal:
Verify the Codex D test-only fixer pass for the Codex E blocker. Confirm the
focused tests now cover degraded status, degraded CLI exit-code semantics,
report metadata, CLI nonzero behavior for diff, and CLI nonzero behavior for
validation fail.

Validation:
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
- python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
- python3 -m ruff check src tests tools
- git diff --check

Do not change parser behavior, parser state final reconciliation, workbook
schema, webhook payload shape, Apps Script behavior, output transport, parser
event classes, match/game identity, deduplication, secrets, environment
variables, raw logs, generated data, runtime status files, failed posts,
workbook exports, or production deployment behavior.

Do not add automatic expected-output bless/update behavior.
Do not change files in review-only mode.
Do not stage, commit, merge, close issue #48, close tracker #47, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/110"
  previous_merge_commit: "a61ed4e5cd8898e25913796080a9c46e66fcff8a"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/parser_golden_replay_harness.md"
  target_artifact: "tests/test_golden_replay_harness.py"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "Fixer pass complete: missing focused tests for degraded status and CLI status semantics were added."
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed in 0.11s"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py -> 38 passed in 0.08s"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings"
    - "explicit #48 local changed-path protected-surface stdin check -> passed with 0 warnings"
    - "python3 -m pytest -q -> 707 passed in 1.04s"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not change parser behavior unless a new focused test reveals a real behavior defect."
    - "Do not move parser truth into golden replay manifests, diagnostics reports, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI interpretation."
    - "Do not use golden replay to infer match winner, game winner, match identity, game identity, or final reconciliation facts beyond parser-produced evidence."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, workbook exports, or production deployment behavior."
    - "Do not add automatic expected-output bless/update behavior."
    - "Do not stage unrelated docs/.DS_Store, repo-wide hardening local report, or LLM advisory scaffold files."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
```
