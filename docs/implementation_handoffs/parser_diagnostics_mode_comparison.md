# Parser Diagnostics Mode Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/49

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous parser reliability issue: https://github.com/Tahjali11/Mythic-Edge/issues/107

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/108

Previous merge commit: `5d80789c24e2a5783f97f2ff9c5c9e147547d4c0`

## Contract

`docs/contracts/parser_diagnostics_mode.md`

## Role Performed

Codex C: Module Implementer

## Comparison Before Editing

Confirmed matches:

- Existing `app/diagnostics.py` already owns runtime status writes, webhook
  success/failure counters, router/event failure records, URL redaction, and
  safe JSON normalization.
- Existing `app/log_drift_sensor.py` already replays `Player.log` slices
  through `LineBuffer` and `Router`, producing routed/unknown counts, routed
  event-kind counts, unknown signatures, unmatched API names, baseline deltas,
  and timestamp anomaly counts.
- Existing status API, runner, runtime surfaces, saved replay, and transforms
  remained available as evidence/consumer surfaces.
- Existing #107 truncation support was present at merge commit `5d80789`:
  `Truncation` events are routed, replayable, included in local archives, and
  summarized from normalized fields.

Confirmed gaps:

- No `src/mythic_edge_parser/app/parser_diagnostics.py` module existed.
- No v1 parser diagnostics report schema existed.
- No local parser diagnostics CLI/module entrypoint existed.
- No report builder separated parser health from transport health.
- No focused tests covered pass, review, fail, truncation/data-loss, transport
  separation, privacy redaction, malformed baseline handling, or CLI report
  writing.

Protected boundaries preserved:

- Diagnostics mode observes existing parser/router/drift/runtime evidence. It
  does not create a second parser.
- No parser behavior, parser state final reconciliation, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw logs,
  generated data committed to the repo, runtime status file schema,
  failed-post schema, or workbook exports were changed.
- No missing GameState data is reconstructed, and no match/game facts are
  inferred from incomplete evidence.
- Diagnostics status labels are local advisory report labels only; they are
  not CI, merge, deploy, parser-truth, workbook-truth, or AI-truth authority.

## What Changed

Added the local diagnostics report harness:

- New module: `src/mythic_edge_parser/app/parser_diagnostics.py`
- New focused tests: `tests/test_parser_diagnostics_mode.py`
- New handoff: `docs/implementation_handoffs/parser_diagnostics_mode_comparison.md`

Implemented:

- `build_parser_diagnostics_report(source_log, *, profile, runtime_status, drift_baseline)`
- `write_parser_diagnostics_report(*, source_log, report_path, profile, drift_baseline_path)`
- `ParserDiagnosticsResult`
- `python3 -m mythic_edge_parser.app.parser_diagnostics` entrypoint
- Default generated report path:
  `data/status/parser_diagnostics_latest.json`

The default report path is already under ignored `data/status/`, so no
`.gitignore` change was required.

## Behavior Summary

The report builder:

- Reads a local log or sanitized fixture.
- Uses `log_drift_sensor.build_player_log_drift_report()` for routing/unknown
  evidence.
- Uses the existing `LineBuffer` and `Router` to collect event-kind counts and
  normalized `Truncation` data-loss summaries.
- Produces the contracted `parser_diagnostics.v1` report shape.
- Redacts source paths, local user paths, URLs, and sensitive text in report
  strings.
- Reports raw-log and raw-payload inclusion as false and does not copy raw log
  lines into the report.
- Classifies parser, event-family, truncation/data-loss, unknown/degraded,
  final-reconciliation, transport, workbook/App Script, and manual checklist
  sections separately.
- Treats webhook failures as transport review evidence, not parser failure.
- Treats missing optional runtime status as `unknown`, not parser failure.
- Treats unreadable source logs and parser/router aggregation failures as
  parser-health failures.
- Treats malformed drift baseline JSON as review evidence without failing the
  parser run.

## Files Changed

Added:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `docs/implementation_handoffs/parser_diagnostics_mode_comparison.md`

Source artifact note:

- `docs/contracts/parser_diagnostics_mode.md` was already present as an
  untracked source artifact before this implementation pass and was read but
  not edited.

Unrelated untracked files present and not touched:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Interface Changes

New local parser diagnostics API:

```python
def build_parser_diagnostics_report(
    source_log: Path,
    *,
    profile: str = "live_game",
    runtime_status: dict[str, Any] | None = None,
    drift_baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def write_parser_diagnostics_report(
    *,
    source_log: Path,
    report_path: Path | None = None,
    profile: str = "live_game",
    drift_baseline_path: Path | None = None,
) -> ParserDiagnosticsResult:
    ...
```

New local CLI/module entrypoint:

```bash
python3 -m mythic_edge_parser.app.parser_diagnostics [source_log] --profile fixture|local_log|live_game --out <path>
```

Report object:

- `object: "mythic_edge_parser_diagnostics_report"`
- `schema_version: "parser_diagnostics.v1"`

No package script, environment variable, workbook field, webhook field, Apps
Script mapping, runtime status field, failed-post schema, or parser event class
was added or changed.

## Validation Run

Focused diagnostics suite:

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py
```

Result:

```text
39 passed in 0.72s
```

Regression and adjacent parser reliability suite:

```bash
python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py
```

Result:

```text
35 passed in 0.11s
```

Ruff:

```bash
python3 -m ruff check src tests tools
```

Result:

```text
All checks passed!
```

Whitespace:

```bash
git diff --check
```

Result: passed with no output.

Protected-surface gate, base-vs-HEAD mode:

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result:

```text
changed_paths: 21
forbidden: 0
warnings: 4
result: passed
```

The four warnings are existing contract-authorized parser/event/parser-module
warnings from the already-merged #107 truncation package on this integration
branch.

Protected-surface gate, explicit local changed-path mode:

```bash
{ git diff --name-only; printf '%s\n' docs/contracts/parser_diagnostics_mode.md docs/implementation_handoffs/parser_diagnostics_mode_comparison.md src/mythic_edge_parser/app/parser_diagnostics.py tests/test_parser_diagnostics_mode.py; } | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result:

```text
changed_paths: 4
forbidden: 0
warnings: 0
result: passed
```

Module entrypoint:

```bash
python3 -m mythic_edge_parser.app.parser_diagnostics --help
```

Result: help text printed successfully.

Full local test suite:

```bash
python3 -m pytest -q
```

Result:

```text
695 passed in 1.11s
```

Unavailable on this branch:

```bash
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

Result: both tools are absent from `codex/parser-reliability-intelligence`, so
they were recorded as unavailable per the contract.

## Open Risks

- Remote CI has not run in this Codex C pass.
- No private live `Player.log` or live MTGA game was exercised; tests use
  synthetic/sanitized fixture snippets only.
- Final reconciliation reporting is intentionally shallow in v1: it reports
  observed `GameResult` or match-completion `MatchState` evidence and otherwise
  stays `unknown`.
- Runtime status is optional input to the report builder; the v1 CLI does not
  read the current runtime status file automatically.
- Diagnostics does not query Google Sheets, Apps Script, workbook state,
  webhook endpoints, or model providers.
- Tracker #47 and related issue #11 remain open.

## Reviewer Focus

Codex E should verify:

- The report harness uses existing parser/router/drift evidence and is not a
  second parser.
- `overall_status`, section statuses, and parser-vs-transport separation match
  the contract.
- `Truncation` events become data-loss review evidence without reconstructing
  missing GameState facts.
- The report does not include raw log lines, raw payload bodies, local paths,
  webhook URLs, secrets, tokens, credentials, failed-post rows, or workbook
  exports.
- Missing optional runtime status remains `unknown`, not parser failure.
- The CLI writes only a local ignored JSON report and prints a sanitized
  summary.
- Existing diagnostics, drift, status API, runner, replay, and truncation tests
  keep their meaning.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #49:
https://github.com/Tahjali11/Mythic-Edge/issues/49

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_diagnostics_mode.md
- docs/implementation_handoffs/parser_diagnostics_mode_comparison.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_gsm_truncation.md
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/runner.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/saved_event_replay.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/stream.py
- tests/test_parser_diagnostics_mode.py
- tests/test_log_drift_sensor.py
- tests/test_diagnostics.py
- tests/test_status_api.py
- tests/test_runner.py
- tests/test_parser_regressions.py
- tests/test_saved_event_replay.py
- tests/test_gsm_truncation_parser.py

Goal:
Verify the Codex C diagnostics implementation against the parser diagnostics mode contract.

Confirm:
- Diagnostics mode observes existing parser/router/drift/runtime evidence and does not create a second parser.
- `build_parser_diagnostics_report()` and `write_parser_diagnostics_report()` match the contracted v1 public interface.
- The v1 report shape includes all contracted top-level sections and stable status vocabulary.
- Healthy sanitized fixture evidence can produce `overall_status = "pass"`.
- Unknown signatures produce `review`.
- `Truncation` events produce data-loss `review` without reconstructing missing GameState facts.
- Unreadable source logs produce `fail`.
- Webhook failures affect transport health, not parser health.
- Missing optional runtime status produces `unknown`, not parser failure.
- Report output redacts local paths and webhook URLs and does not include raw log lines or raw payload bodies.
- The CLI writes a local ignored report and prints a sanitized summary.
- Existing diagnostics, log drift, status API, runner, saved replay, parser regression, and GSM truncation tests still pass.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status file schema, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py
python3 -m ruff check src tests tools
python3 -m pytest -q
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main

If reviewing uncommitted local files before submission, also run the protected-surface gate with an explicit changed-path stdin list because base-vs-HEAD mode may not include untracked files.

Record `tools/select_validation.py` and `tools/check_secret_patterns.py` as unavailable if they are still absent from this branch.

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- workflow_handoff block.

Do not fix code in review mode.
Do not target main directly.
Do not close tracker #47 or related issue #11.
Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status file schema, failed posts, or workbook exports.
Do not reconstruct missing GameState data or infer match/game facts from incomplete evidence.
Do not make diagnostics a CI gate, merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source.
Do not stage or commit.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_diagnostics_mode.md"
  target_artifact: "docs/implementation_handoffs/parser_diagnostics_mode_comparison.md"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/108"
  previous_merge_commit: "5d80789c24e2a5783f97f2ff9c5c9e147547d4c0"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py"
    - "python3 -m ruff check src tests tools"
    - "python3 -m pytest -q"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "explicit local changed-path protected-surface stdin check"
    - "python3 -m mythic_edge_parser.app.parser_diagnostics --help"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47 or related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data committed to the repo, runtime status file schema, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game facts from incomplete evidence."
    - "Do not make diagnostics a CI gate, merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
```
