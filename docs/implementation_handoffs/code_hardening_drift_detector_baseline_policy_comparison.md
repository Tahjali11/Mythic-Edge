# Code Hardening Drift Detector Baseline Policy Comparison

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/70

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

Source contract: `docs/contracts/code_hardening_drift_detector_baseline_policy.md`

Related contracts:

- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`

Related ADRs:

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Remote evidence-ledger context:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Worktree Check

- Confirmed branch: `codex/code-hardening-suite`.
- Confirmed tracker #33 and child issue #70 are open.
- Fetched `origin` before comparison.
- Observed current HEAD: `1432f08`.
- Observed worktree before editing: `docs/contracts/code_hardening_drift_detector_baseline_policy.md` was untracked and treated as the source artifact for this pass.
- No unrelated modified files were edited, staged, committed, pushed, or absorbed.

## What Drift Detector Baselines Are Supposed To Do

A drift detector baseline is a structured comparison point for the Player.log drift sensor. It helps answer whether the current observed log/routing surface differs from the expected or previously reviewed surface.

The contract keeps baselines report-only by default. Baselines and reports may help identify new unknown signatures, unmatched API names, unmatched request API names, and follow-up parser audit work. They must not become parser truth, workbook truth, schema truth, CI failure authority, fixture refresh authority, or production deployment authority without a future issue, contract, review, validation package, and explicit user approval.

## Current Behavior Summary

`src/mythic_edge_parser/app/log_drift_sensor.py` already provides a local report-oriented drift sensor:

- `DEFAULT_DRIFT_REPORT_PATH` points to `STATUS_ROOT / "player_log_drift_latest.json"`.
- `DEFAULT_DRIFT_BASELINE_PATH` points to `STATUS_ROOT / "player_log_drift_baseline.json"`.
- `iter_log_entries()` reads a source log through `LineBuffer`.
- `build_player_log_drift_report()` routes entries through `Router`.
- The report counts headers, routed event kinds, unknown signatures, unmatched API names, and unmatched request API names.
- `_baseline_delta()` compares current unknown/unmatched sets against `baseline_payload`.
- Reports include volatile/local fields: `analyzed_at` and `source_path`.
- `write_player_log_drift_report()` writes a report and overwrites the baseline only when `refresh_baseline=True`.
- The CLI prints a summary, report path, optional baseline refresh path, and new unmatched/unknown values.
- The CLI returns `0` on normal completion and is not a drift gate.

Current tests already cover selected report-only behavior:

- `tests/test_log_drift_sensor.py` copies `tests/fixtures/flush_timing_corpus_slice.log` into a temporary `Player.log`.
- One test asserts the report is `review`, unknown entries exist, and selected unmatched API/request names are surfaced.
- One test writes a temporary `baseline.json` and asserts new unmatched API names plus new unmatched request API names are reported.
- One test verifies `_entry_signature()` prefers a prefix label instead of preserving a full identity-bearing line.

The minimal implementation plan for this thread was docs-only comparison. No detector, test, fixture, baseline, CI, or snapshot change was required by the contract.

## Files Inspected

Governance and workflow:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

Contracts and ADRs:

- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Remote evidence-ledger artifacts:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

Drift detector, tests, and fixture surfaces:

- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `audit_player_log_drift.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_protected_surfaces.py`
- `tests/fixtures/`

## Contract Matches

- Drift detector reports are local/report-oriented by default.
- Default report and baseline paths live under runtime status paths, which are local artifacts.
- Missing baseline file, invalid JSON baseline, non-object JSON baseline, and missing baseline keys are tolerated as empty baseline payloads.
- Baseline deltas include new/resolved unknown signatures, unmatched API names, and unmatched request API names.
- `write_player_log_drift_report()` does not refresh a baseline unless `refresh_baseline=True`.
- The CLI is informational and returns success on normal completion.
- Current tests use temporary `Player.log`, `report.json`, and `baseline.json` paths rather than committing runtime artifacts.
- Current tests assert baseline-delta reporting without turning it into a failing CI gate.
- Current tests assert one privacy-preserving signature path.
- No committed drift baseline exists under `tests/fixtures/` or schema snapshot fixtures.
- Schema snapshot tests already have opt-in update behavior and "do not auto-update" messaging.
- Protected-surface gate forbids `data/status/**`, raw Player.log names outside documented fixtures, runtime logs, failed posts, generated data, workbook exports, secrets, webhook credentials, and local review artifacts.
- Protected-surface gate allows documented fixture paths under `tests/fixtures/`; this is path allowance, not content sanitization.
- PR drift-budget policy already distinguishes `No drift`, `Authorized drift`, `Residual drift`, and `N/A`, and says drift disclosure does not authorize protected changes.
- ADR-0001, ADR-0003, and ADR-0004 align with the contract: parser/state owns truth, Player.log is evidence, and protected surfaces require explicit authorization.

## Contract Gaps

These are policy and test-coverage gaps, not implementation changes authorized for this thread:

- No committed drift baseline exists.
- No committed drift-report expected-output fixture exists.
- No baseline manifest or sidecar metadata exists.
- Current baseline payload shape is implicit in `log_drift_sensor.py` and focused tests rather than a standalone schema artifact.
- Current reports include `analyzed_at` and `source_path`, which are appropriate locally but unsuitable for committed expected-output baselines without normalization.
- `status == "review"` currently considers unknown count, new unknown signatures, and new unmatched API names; it does not include `new_unmatched_request_api_names`.
- Tests cover selected report and baseline-delta behavior but do not cover missing baseline behavior, malformed baseline behavior, non-object baseline behavior, refresh overwrite behavior, CLI output/exit behavior, unreadable source logs, empty source logs, or future committed baseline metadata.
- The future evidence ledger is not implemented, so drift reports do not map signals to affected parser-managed output families.
- `tools/check_secret_patterns.py` is absent on this branch, so content-level privacy review still depends on path gates, tests, and manual review.
- The protected-surface gate does not inspect untracked local runtime reports or baseline content unless specific paths are passed to it.

## Contract Mismatches

No clear contract mismatch required code, test, fixture, baseline, schema snapshot, or CI changes in this pass.

The only behavior-level observation that may become future work is the request-name status gap: `new_unmatched_request_api_names` is included in `baseline_delta` and printed by the CLI, but it does not currently cause `status == "review"` by itself. The contract records this as an observed suspected gap and does not authorize changing detector behavior in this thread.

## Missing Tests

Missing tests that a future detector/baseline implementation could add under a separate issue:

- Missing baseline file behavior.
- Malformed baseline JSON behavior.
- Non-object baseline JSON behavior.
- Missing baseline key behavior.
- `--refresh-baseline` overwrite behavior.
- CLI output and normal exit behavior.
- Request-name-only drift status semantics, if a future contract chooses to change status behavior.
- Committed baseline metadata validation, if committed baselines are ever authorized.
- Normalization of `analyzed_at` and `source_path` for any future committed expected-output fixture.
- Content scanner checks, if `tools/check_secret_patterns.py` is added to the branch.

## Protected Surface Status

No protected runtime surface was touched.

This pass did not change:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- CI failure gates
- detector behavior
- `--refresh-baseline` semantics
- committed fixtures
- schema snapshots
- expected parser outputs
- secrets, credentials, tokens, API keys, webhook URLs, or environment variables
- raw local logs
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Files Changed

- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`

## Code Changed Or Docs-Only

Docs-only comparison artifact.

No code, tests, fixtures, baselines, schema snapshots, expected outputs, runtime status files, CI gates, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, secrets, generated data, failed posts, workbook exports, or local-only artifacts were changed.

## Interface Changes

None.

No function signatures, CLI options, parser payload fields, event classes, event `kind` values, workbook columns, webhook payloads, Apps Script entrypoints, environment variables, runtime status shapes, fixture data, expected-output schemas, or protected runtime surfaces changed.

## Tests Added Or Updated

None.

## Validation Run

```powershell
git diff --check
```

Result: passed.

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result: passed with `changed_paths: 0`, `forbidden: 0`, and `warnings: 0`.

```powershell
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result: passed with `changed_paths: 2`, `forbidden: 0`, and `warnings: 0`.

```powershell
py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
```

Result: passed, `57 passed in 0.53s`.

```powershell
py -m ruff check src tests tools
```

Result: passed, `All checks passed!`.

## Still Unverified

- No Codex E contract-test review has been performed yet for this comparison artifact.
- No committed drift baseline design exists.
- No content scanner exists on this branch.
- No evidence-ledger implementation exists.
- No live workbook state or deployed Apps Script state was inspected.
- No CI checks have run for this uncommitted docs-only handoff.
- No future failing gate behavior was designed, implemented, or validated.

## Reviewer Focus

Codex E should verify:

- The comparison accurately treats current drift reports and baselines as report-only.
- The request-name status gap is documented without being miscast as an authorized fix.
- The comparison does not imply `--refresh-baseline` behavior should change in this thread.
- The comparison preserves golden fixture, schema snapshot, protected-surface, and PR drift-budget boundaries.
- Missing tests are framed as future work requiring a separate issue/contract, not as required changes for this pass.
- No baselines, fixture files, snapshots, expected outputs, or runtime status files were created or modified.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer / contract-test thread for the Code Hardening child issue: Drift detector baseline policy.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/70

Branch target:
codex/code-hardening-suite

Review artifacts:
- docs/contracts/code_hardening_drift_detector_baseline_policy.md
- docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- src/mythic_edge_parser/app/log_drift_sensor.py
- tests/test_log_drift_sensor.py
- tests/test_event_schema_snapshots.py
- tests/test_check_protected_surfaces.py
- tests/fixtures/

Remote citation context if absent locally:
- origin/main:docs/problem_representations/player_log_evidence_ledger.md
- origin/main:docs/contracts/player_log_evidence_ledger.md

Task:
Review the implementation comparison against docs/contracts/code_hardening_drift_detector_baseline_policy.md. This was a docs-only comparison pass. Lead with findings, ordered by severity. Verify that the comparison accurately covers build/write/report/baseline behavior, report-only baseline semantics, test coverage, request-name status gap, fixture/schema/protected-surface/PR drift-budget relationships, protected-surface status, validation, and remaining risks.

Do not create or modify drift baselines, change log drift detector behavior, change --refresh-baseline behavior, add failing CI gates, refresh schema snapshots or expected outputs, create or modify fixture files, commit raw Player.log files, add sanitized fixture data, implement sanitizer tooling, implement the Player.log evidence ledger, or modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.

Do not target main. Do not mark tracker #33 complete. Do not stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md','docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools

Produce:
docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md

Final review must include:
- role performed
- issue/tracker
- contract reviewed
- artifacts reviewed
- findings first
- files changed, if any
- validation run and result
- remaining risks
- next recommended role
- pasteable next-thread prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/70"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_drift_detector_baseline_policy.md"
  target_artifact: "docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md' | py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin"
    - "py -m pytest -q tests\\test_log_drift_sensor.py tests\\test_check_protected_surfaces.py"
    - "py -m ruff check src tests tools"
  stop_conditions:
    - "Do not create or modify drift baselines."
    - "Do not change log drift detector behavior or --refresh-baseline semantics."
    - "Do not add failing CI gates."
    - "Do not refresh schema snapshots or parser expected outputs."
    - "Do not create or modify fixture files, commit raw Player.log files, or add sanitized fixture data."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
    - "Do not stage, commit, open a PR, or merge unless explicitly asked."
```
