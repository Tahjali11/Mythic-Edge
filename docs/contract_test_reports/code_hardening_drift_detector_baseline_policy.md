# Code Hardening Drift Detector Baseline Policy Contract-Test Report

## Findings

No blocking findings.

The docs-only comparison accurately covers the current drift detector build/write/report/baseline behavior against `docs/contracts/code_hardening_drift_detector_baseline_policy.md`. It preserves the report-only baseline posture, does not authorize detector behavior changes, and correctly treats the `new_unmatched_request_api_names` status behavior as a documented gap rather than a fix target for this pass.

Non-blocking residual risk: the current detector includes `new_unmatched_request_api_names` in `baseline_delta` and CLI output, but `status == "review"` is triggered only by unknown entries, new unknown signatures, or new unmatched API names. This is accurately recorded in the comparison and contract as future policy/implementation work, not as an issue #70 scope requirement.

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/70

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Contract Reviewed

`docs/contracts/code_hardening_drift_detector_baseline_policy.md`

## Artifacts Reviewed

- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `audit_player_log_drift.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_protected_surfaces.py`
- `tests/fixtures/`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

## Implementation Under Test

Branch: `codex/code-hardening-suite`

Implementation/comparison artifact:

- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`

Implementation type: docs-only comparison pass.

## Contract Summary

Drift detector baselines are comparison artifacts for Player.log drift reports. They may help identify unknown signatures, unmatched API names, unmatched request API names, and follow-up parser audit work, but they must remain report-only by default.

The contract does not authorize committed baselines, detector behavior changes, `--refresh-baseline` semantic changes, failing CI gates, fixture changes, schema snapshot refreshes, parser expected-output refreshes, parser behavior changes, workbook/webhook/App Script changes, or production deployment changes.

## Confirmed Contract Matches

- Current report and baseline defaults are local runtime paths: `DEFAULT_DRIFT_REPORT_PATH = STATUS_ROOT / "player_log_drift_latest.json"` and `DEFAULT_DRIFT_BASELINE_PATH = STATUS_ROOT / "player_log_drift_baseline.json"`.
- `build_player_log_drift_report()` routes entries through `Router`, counts unknown signatures, unmatched API names, unmatched request API names, routed event kinds, headers, and produces a `baseline_delta`.
- Report output includes local/volatile fields, `analyzed_at` and `source_path`; the comparison correctly identifies those as fine for local runtime reports and unsuitable for committed expected-output baselines without normalization.
- `_baseline_delta()` compares unknown signatures, unmatched API names, and unmatched request API names against baseline payload lists and reports new/resolved values for each.
- Missing, invalid JSON, and non-object baselines load as `{}`, which matches the comparison's observed behavior and the contract's report-only treatment of missing/malformed baselines.
- `write_player_log_drift_report()` writes the report and overwrites the baseline only when `refresh_baseline=True`; the comparison does not propose changing that behavior.
- CLI output prints report path, optional baseline refresh path, new unmatched API names, new unmatched request API names, and new unknown signatures, then returns `0` on normal completion.
- `tests/test_log_drift_sensor.py` uses temporary `Player.log`, `report.json`, and `baseline.json` paths rather than committing runtime reports or baselines.
- Existing tests cover selected report generation, baseline deltas, and one privacy-preserving signature path without turning drift deltas into a failing gate.
- No committed drift baseline or drift-report expected-output fixture was found under `tests/fixtures/` or schema snapshot fixtures.
- The comparison accurately links baseline policy to the golden fixture policy: any future committed baseline or expected drift report would need sanitized/synthetic evidence, provenance metadata, and explicit issue/contract/review approval.
- The comparison accurately links schema snapshot policy: snapshot updates stay opt-in and must not be auto-refreshed by drift reports.
- The comparison accurately links the protected-surface gate: runtime status paths and raw local logs are forbidden committed artifacts, while `tests/fixtures/` paths are allowed by path but not content-sanitized by the gate.
- The comparison accurately links PR drift budget policy: fixture/evidence or protected-surface drift must be disclosed and cited, and the PR template does not authorize protected changes by itself.
- ADR alignment is preserved: parser/state owns truth, Player.log is evidence rather than absolute truth, and protected-surface changes require explicit issue/contract/review authorization.

## Contract Mismatches

None found.

## Missing Tests

The comparison accurately identifies these as future gaps, not required fixes for this docs-only pass:

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

## Drift Notes

Repo drift: none found in the reviewed scope. The branch is `codex/code-hardening-suite` and was even with `origin/codex/code-hardening-suite` during review.

Workbook drift: not inspected and not required. No workbook schema, helper formula, live workbook, webhook, or Apps Script behavior changed.

Deployment drift: not inspected and not required. No deployed Apps Script, CI failing gate, webhook, or production behavior changed.

Local-data drift: no drift baselines, runtime reports, runtime status files, raw logs, failed posts, generated data, workbook exports, fixtures, schema snapshots, or expected outputs were created or modified.

## Remaining Risks

- The request-name status gap remains unimplemented by design.
- No committed drift baseline design exists.
- No baseline manifest or sidecar metadata exists.
- No content secret/private-data scanner exists on this branch.
- No evidence-ledger implementation exists, so drift reports do not yet map signals to affected parser-managed output families.
- Live workbook and deployed Apps Script state remain unverified.
- PR/CI checks have not run for this unsubmitted docs-only package.

## Checks Run

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md','docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
```

Additional local scope check:

```powershell
rg -n "[ \t]+$" docs\contract_test_reports\code_hardening_drift_detector_baseline_policy.md
```

## Validation Result

- `git diff --check` -> passed with no output.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite` -> passed with `changed_paths: 0`, `forbidden: 0`, `warnings: 0`.
- Issue #70 path-scoped protected-surface check over the contract, implementation handoff, and report paths -> passed with `changed_paths: 3`, `forbidden: 0`, `warnings: 0`.
- `py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py` -> `57 passed in 0.51s`.
- `py -m ruff check src tests tools` -> `All checks passed!`.
- `rg -n "[ \t]+$" docs\contract_test_reports\code_hardening_drift_detector_baseline_policy.md` -> no trailing whitespace matches.

## Files Changed

- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`

## Code Changed Or Docs-Only

Docs-only.

No production code, test code, fixture data, expected-output snapshots, schema snapshots, drift baselines, runtime status artifacts, raw logs, generated data, failed posts, workbook exports, secrets, environment variables, workbook schema, webhook payloads, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, parser state final reconciliation, detector behavior, `--refresh-baseline` behavior, CI gates, or parser behavior were changed.

## Recommendation

Approve for Module Submitter.

Next recommended role: Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex F: Module Submitter for the Code Hardening child issue: Drift detector baseline policy.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/70

Branch target:
codex/code-hardening-suite

Reviewed artifacts:
- docs/contracts/code_hardening_drift_detector_baseline_policy.md
- docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md
- docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md

Goal:
Submit the docs-only drift detector baseline policy package after confirming scope, validation, and protected-surface status. Stage only the issue #70 files, commit, push, and open or update a draft PR targeting codex/code-hardening-suite. Do not target main.

Expected issue #70 files:
- docs/contracts/code_hardening_drift_detector_baseline_policy.md
- docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md
- docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md

Before staging:
- Inspect git status.
- Confirm there are no unrelated modified or untracked files included.
- Confirm no drift baselines, runtime reports, fixture files, parser code, tests, schema snapshots, expected outputs, raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, environment variables, webhook payloads, workbook schema, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, detector behavior, --refresh-baseline behavior, CI gates, or parser behavior were changed.
- Run or cite current validation.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md','docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools

Do not:
- Create or modify drift baselines.
- Change log drift detector behavior.
- Change --refresh-baseline behavior.
- Add failing CI gates.
- Refresh schema snapshots or expected outputs.
- Create or modify fixture files.
- Commit raw Player.log files.
- Add sanitized fixture data.
- Implement sanitizer tooling.
- Implement the Player.log evidence ledger.
- Modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.
- Target main.
- Mark tracker #33 complete.
- Merge the PR.

Final handoff must include current branch, commit hash, PR URL, target branch, validation result, files staged, protected-surface status, remaining risks, and next recommended role.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/70"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/code_hardening_drift_detector_baseline_policy.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md"
  target_artifact: "docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check -> passed with no output"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed with changed_paths: 0, forbidden: 0, warnings: 0"
    - "issue #70 path protected-surface check -> passed with changed_paths: 3, forbidden: 0, warnings: 0"
    - "py -m pytest -q tests\\test_log_drift_sensor.py tests\\test_check_protected_surfaces.py -> 57 passed in 0.51s"
    - "py -m ruff check src tests tools -> All checks passed"
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
    - "Do not merge the PR."
```
