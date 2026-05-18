# Parser Diagnostics Mode Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/49

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous parser reliability issue:
https://github.com/Tahjali11/Mythic-Edge/issues/107

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/108

Previous merge commit:
`5d80789c24e2a5783f97f2ff9c5c9e147547d4c0`

## Contract

- `docs/contracts/parser_diagnostics_mode.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_diagnostics_mode.md`
- `docs/implementation_handoffs/parser_diagnostics_mode_comparison.md`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`

Unrelated local files observed and excluded from this review:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Findings

No blocking findings.

## Contract Summary

Parser diagnostics mode must provide a local, report-first acceptance harness
for live-game parser reliability without becoming a second parser or changing
truth-producing parser, state, workbook, webhook, Apps Script, or transport
behavior. It must reuse parser-produced events and existing drift evidence,
emit a versioned redacted report, distinguish parser health from transport and
workbook/App Script health, and keep reports in ignored local status paths by
default.

## Checks Run

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
{ git diff --name-only; printf '%s\n' docs/contracts/parser_diagnostics_mode.md docs/implementation_handoffs/parser_diagnostics_mode_comparison.md src/mythic_edge_parser/app/parser_diagnostics.py tests/test_parser_diagnostics_mode.py; } | sort -u | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
python3 -m mythic_edge_parser.app.parser_diagnostics --help
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

## Results

- Focused diagnostics and adjacent runtime suite: `39 passed in 0.68s`.
- Parser reliability regression suite: `35 passed in 0.11s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Protected-surface gate against `origin/main`: `forbidden: 0`,
  `warnings: 4`, `result: passed`.
- Explicit local changed-path protected-surface gate for this module:
  `changed_paths: 4`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Full local test suite: `695 passed in 0.98s`.
- Parser diagnostics CLI help: passed and showed the expected local report
  options.
- `tools/select_validation.py`: unavailable on this branch.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The four protected-surface warnings from the `origin/main` branch diff are
from the previously merged GSM truncation issue #107 surfaces:
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`. The explicit #49 local
changed-path check has no warnings.

## Confirmed Contract Matches

- `src/mythic_edge_parser/app/parser_diagnostics.py` exposes
  `build_parser_diagnostics_report()`, `write_parser_diagnostics_report()`,
  and `ParserDiagnosticsResult.summary_line()`.
- The module supports `python3 -m mythic_edge_parser.app.parser_diagnostics`
  with `--profile`, `--out`, and `--drift-baseline` options.
- The default write path is the ignored local status report
  `data/status/parser_diagnostics_latest.json`.
- Reports use the contracted object and version shape:
  `object: mythic_edge_parser_diagnostics_report` and
  `schema_version: parser_diagnostics.v1`.
- Reports include the contracted top-level sections for source metadata,
  privacy posture, parser health, event-family coverage, truncation and data
  loss, unknown/degradation signals, final reconciliation evidence, transport
  health, workbook/App Script separation, manual checklist, and validation
  evidence.
- The diagnostics harness reuses `log_drift_sensor` and `Router` output rather
  than reimplementing parser truth or parsing raw GRE/client payloads
  downstream.
- Healthy parser evidence produces a passing parser-health result.
- Unknown entries, malformed/missing timestamp evidence, and truncation
  evidence route to review states without inventing parser facts.
- Unreadable or fully unrouted logs fail parser health as contracted.
- Webhook/runtime transport evidence is reported separately from parser health.
- Missing runtime status evidence remains `unknown` rather than failing parser
  health.
- Final reconciliation evidence is observational and derived from
  parser-produced events.
- Report output redacts local paths, sensitive URL-looking values, bearer
  tokens, passwords, and full source-log paths.
- Tests assert raw log snippets and raw GRE payload markers are not present in
  rendered reports.
- The CLI writes only local diagnostics reports and prints a safe summary.
- No workbook schema, webhook payload shape, Apps Script behavior, parser
  event classes, parser state final reconciliation, match/game identity,
  deduplication, runtime status schema, failed-post schema, workbook export, or
  production deployment behavior changes were found in the #49 module scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

The focused tests cover report schema shape, healthy pass behavior, unknown
and malformed evidence review behavior, truncation review behavior, unreadable
failure behavior, transport separation, missing runtime status behavior, redacted
report rendering, default report path behavior, custom output writing, and CLI
execution.

## Drift Notes

- Repo drift: expected addition of a report-only diagnostics module, focused
  tests, contract, handoff, and this contract-test report.
- Parser behavior drift: none found.
- Parser state final reconciliation drift: none found.
- Parser event class drift: none found.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local-data drift: no raw private logs or generated runtime artifacts were
  added in the reviewed module scope.
- Previous issue #107 drift: still present in the branch as merged parser
  reliability work and not part of the #49 diagnostics-mode finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- This review did not execute against a private live Player.log; tests use
  sanitized synthetic fixtures.
- The CLI accepts runtime status evidence through the API surface rather than
  auto-discovering runtime status files.
- `tools/select_validation.py` and `tools/check_secret_patterns.py` are absent
  from this branch, so those optional hardening validations were recorded as
  unavailable.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #49.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/49

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous parser reliability issue:
https://github.com/Tahjali11/Mythic-Edge/issues/107

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/108

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_diagnostics_mode.md
- docs/implementation_handoffs/parser_diagnostics_mode_comparison.md
- docs/contract_test_reports/parser_diagnostics_mode.md

Goal:
Stage only the reviewed parser diagnostics mode docs, implementation, tests,
and contract-test report, then commit, push, and open or update a draft PR
against codex/parser-reliability-intelligence. Do not target main.

Reviewed files:
- docs/contracts/parser_diagnostics_mode.md
- docs/implementation_handoffs/parser_diagnostics_mode_comparison.md
- docs/contract_test_reports/parser_diagnostics_mode.md
- src/mythic_edge_parser/app/parser_diagnostics.py
- tests/test_parser_diagnostics_mode.py

Confirm before staging:
- No raw private Player.log excerpts, secrets, webhook URLs, generated runtime
  artifacts, runtime status files, failed posts, or workbook exports are included.
- The unrelated local files docs/.DS_Store,
  docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md,
  docs/contracts/repo_wide_llm_advisory_review_scaffold.md, and
  docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md
  are not staged.
- Workbook schema, webhook payload shape, Apps Script behavior, parser event
  classes, parser state final reconciliation, extractor behavior, match/game
  identity, deduplication, runtime status schema, failed-post schema, workbook
  exports, and production deployment behavior are unchanged.

Validation evidence to include:
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py -> 39 passed
- python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py -> 35 passed
- python3 -m ruff check src tests tools -> All checks passed!
- git diff --check -> passed
- python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings
- explicit #49 local changed-path protected-surface stdin check -> passed with 0 warnings
- python3 -m pytest -q -> 695 passed
- python3 -m mythic_edge_parser.app.parser_diagnostics --help -> passed
- tools/select_validation.py and tools/check_secret_patterns.py were unavailable on this branch

Do not stage unrelated files. Do not merge, close issue #49, mark tracker #47
complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/108"
  previous_merge_commit: "5d80789c24e2a5783f97f2ff9c5c9e147547d4c0"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_diagnostics_mode.md"
  target_artifact: "docs/contract_test_reports/parser_diagnostics_mode.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "No blocking findings. Ready for Codex F."
  validation:
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py -> 39 passed"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py -> 35 passed"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with only prior #107 protected-surface warnings"
    - "explicit #49 local changed-path protected-surface stdin check -> passed with 0 warnings"
    - "python3 -m pytest -q -> 695 passed"
    - "python3 -m mythic_edge_parser.app.parser_diagnostics --help -> passed"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not paste raw private Player.log excerpts into repo files."
    - "Do not move parser truth into diagnostics reports, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI interpretation."
    - "Do not use diagnostics mode to infer match winner, game winner, match identity, game identity, or final reconciliation facts beyond parser-produced evidence."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, workbook exports, or production deployment behavior."
    - "Do not stage unrelated docs/.DS_Store, repo-wide hardening local report, or LLM advisory scaffold files."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
```
