# Repo-Wide Pyright Advisory Report Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/98

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_pyright_advisory_report.md`

Related artifacts:

- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`
- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed before editing:

- `codex/repo-wide-hardening-run`

Initial status:

```text
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
?? docs/contracts/repo_wide_pyright_advisory_report.md
```

The untracked contract was the source artifact for issue #98 and was treated as in scope.

Final status after validation and removal of the temporary `.tmp\issue-98.md` helper:

```text
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
 M tests/test_select_validation.py
 M tools/select_validation.py
?? docs/contracts/repo_wide_pyright_advisory_report.md
?? docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md
?? tests/test_pyright_advisory_report.py
?? tools/run_pyright_advisory_report.py
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`
- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `pyproject.toml`
- `pyrightconfig.json`
- `tools/run_pyright_advisory.ps1`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `.github/workflows/repo-checks.yml`

## Current Behavior Compared To Contract

Current Pyright tooling already provides an advisory signal:

- `pyright>=1.1,<2` is configured as a dev dependency.
- `pyrightconfig.json` exists with `typeCheckingMode: basic`.
- `.github/workflows/repo-checks.yml` does not run Pyright as a required CI gate.
- `tools/run_pyright_advisory.ps1` runs `pyright --project pyrightconfig.json --pythonpath <resolved interpreter>` and reports cleanly on this machine.

Current gap:

- The approved PowerShell wrapper is Windows-specific and prints a full local interpreter path.
- The selector recommended raw `python3 -m pyright`, which can confuse future handoffs when raw local invocations show resolver noise.
- There was no stable cross-platform report shape for classifying `type_findings`, `local_resolver_noise`, and `tooling_config_blockers`.

## Chosen Implementation Option

Implemented the contract's smallest first option:

- Add a cross-platform Python report helper.
- Keep the existing PowerShell wrapper unchanged.
- Update the selector's Pyright recommendation text to point at the repo-approved helper.
- Add focused tests for report parsing/classification/redaction and selector expectation changes.

## What Changed

- Added `tools/run_pyright_advisory_report.py`.
- Added `tests/test_pyright_advisory_report.py`.
- Updated `tools/select_validation.py` so `pyright_advisory` recommends `python3 tools/run_pyright_advisory_report.py`.
- Updated `tests/test_select_validation.py` expectations for that command.
- Produced this implementation handoff.

## Files Changed

- `tools/run_pyright_advisory_report.py`
- `tests/test_pyright_advisory_report.py`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`

Also present as an untracked source artifact before this implementation pass:

- `docs/contracts/repo_wide_pyright_advisory_report.md`

## Code Changed

Only repo hardening/reporting tooling changed.

No parser, runtime, workbook, webhook, Apps Script, CI workflow, Pyright config, dependency metadata, generated data, runtime status, failed-post, workbook export, or production behavior changed.

## Report Helper Details

`tools/run_pyright_advisory_report.py`:

- runs `pyright --project pyrightconfig.json --pythonpath <active interpreter>`
- prints `Pyright Advisory Report`
- normalizes the Python path to `<resolved-python>`
- prints stable fields required by the contract
- classifies:
  - `type_findings`
  - `local_resolver_noise`
  - `tooling_config_blockers`
- returns `0` for `clean`, `advisory_findings`, or `local_resolver_noise`
- returns `2` for `tooling_config_blocker` or `error`
- supports `--project`, `--repo-root`, and `--format text|json`
- does not write a report file

Stable text report fields implemented:

- `mode`
- `project`
- `python`
- `platform`
- `runner`
- `command`
- `pyright_version`
- `exit_code`
- `errors`
- `warnings`
- `information`
- `type_findings`
- `local_resolver_noise`
- `tooling_config_blockers`
- `status`
- `gate_behavior`

Optional JSON output is implemented as additive convenience for future tooling.

## Test Details

`tests/test_pyright_advisory_report.py` covers:

- clean report rendering
- stable field output
- local Python path redaction/normalization
- local resolver noise classification
- advisory type-finding classification
- tooling/config blocker classification and helper exit behavior
- JSON output shape

`tests/test_select_validation.py` was updated only where it expected the old raw Pyright command.

## Selector Change

Previous selector command:

```text
python3 -m pyright
```

New selector command:

```text
python3 tools/run_pyright_advisory_report.py
```

New reason:

```text
Source, hardening tool, or dependency configuration changed; run the repo-approved Pyright advisory report so type findings are separated from local resolver noise.
```

Pyright remains `recommended`, not `required`.

## Contract Matches

- Keeps Pyright advisory-only and non-gating.
- Does not require zero Pyright findings.
- Does not change `typeCheckingMode`.
- Does not change `pyrightconfig.json`.
- Does not change dependency strategy or introduce npm/npx/package-lock files.
- Does not edit CI.
- Adds a cross-platform Python helper with stable text output.
- Normalizes the local Python interpreter path in durable report output.
- Classifies type findings, resolver noise, and tooling/config blockers.
- Updates selector command text to recommend the repo-approved advisory report helper.
- Adds focused tests for helper parsing/classification/redaction and selector command expectations.

## Contract Mismatches

No contract mismatch was found that required changing Pyright posture, CI, config, dependency metadata, or parser/runtime behavior.

The only pre-existing mismatch was missing report tooling and selector command text, which this pass addresses.

## Missing Safeguards Or Missing Tests

Addressed:

- Missing stable report helper.
- Missing local path normalization in durable Pyright report output.
- Missing classification tests for type findings, local resolver noise, and tooling/config blockers.
- Selector recommending raw Pyright instead of the repo-approved report command.

Still intentionally missing:

- CI advisory artifact.
- Persistent generated report file.
- Pyright baseline comparison.
- macOS/Linux live execution in this Windows thread.
- Any requirement that Pyright findings be zero.

## Pyright Advisory / No-Gate Confirmation

This pass does not:

- add Pyright to CI
- make Pyright required or failing
- require zero Pyright findings
- change submitter/deployer readiness gates
- change parser/runtime behavior to satisfy Pyright

The helper reports Pyright evidence but exits `0` for advisory findings and local resolver noise.

## Raw Pyright Vs Approved Report Comparison

Observed before implementation:

- `powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1` passed with `0 errors, 0 warnings, 0 informations`.
- Raw `py -m pyright` failed with 19 errors and 5 warnings tied to local resolver/import noise for `pytest`, `requests`, and `bs4`, plus the Windows Store `python` alias message.

Observed after implementation:

```text
py tools\run_pyright_advisory_report.py
Pyright Advisory Report
mode: advisory
project: pyrightconfig.json
python: <resolved-python>
platform: windows
runner: tools/run_pyright_advisory_report.py
command: pyright --project pyrightconfig.json --pythonpath <python>
pyright_version: 1.1.409
exit_code: 0
errors: 0
warnings: 0
information: 0
type_findings: 0
local_resolver_noise: 0
tooling_config_blockers: 0
status: clean
gate_behavior: advisory_non_blocking
```

Classification for this local approved report:

- type findings: `0`
- local resolver noise: `0`
- tooling/config blockers: `0`
- status: `clean`

The raw command caveat remains historical/local context, but the approved report command now produces the durable signal for future handoffs.

## Secret/Private-Marker Status

Broad changed-file scan:

- `py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run`
- Result: passed, but scanned `0` paths because current changes include untracked files and unstaged edits not visible to the base/head changed-file mode.

Path-scoped scan over the contract, handoff, helper, helper tests, selector, and selector tests:

- Result: warning, with `0` forbidden findings and `4` artifact-path-reference warnings.
- Warnings were textual failed-post/protected-surface scope references in the contract and handoff. No secret, credential, webhook URL, workbook ID, deployment ID, raw private log, generated data, local interpreter path, or local username finding was reported.

## Protected-Surface Status

Broad changed-file scan:

- `py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run`
- Result: passed, but scanned `0` changed paths.

Path-scoped scan over the contract, handoff, helper, helper tests, selector, and selector tests:

- Result: passed, `forbidden: 0`, `warnings: 0`.

## Surface-Authorization Status

Broad changed-file scan:

- `py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md`
- Result: `authorization_status: ok`, but scanned `0` changed paths.

Path-scoped scan over the contract, handoff, helper, helper tests, selector, and selector tests:

- Result: `authorization_status: ok`.
- All six paths were reported as `NOT_PROTECTED allowed`.
- Temporary `.tmp\issue-98.md` was created for this validation command and removed afterward so it would not remain as a local artifact.

## Validation-Selector Status

Confirmed during implementation with path-scoped examples:

- parser source path example recommends `python3 tools/run_pyright_advisory_report.py`
- dependency/config path example recommends `python3 tools/run_pyright_advisory_report.py`
- recommendation remains `recommended`

Broad changed-file selector:

- `py tools\select_validation.py --base origin/codex/repo-wide-hardening-run`
- Result: `selection_status: ok`, with advisory `zero_changed_paths`.

Path-scoped selector over the contract, handoff, helper, helper tests, selector, and selector tests:

- Result: `selection_status: ok`.
- Required commands selected: `git diff --check`, protected-surface gate, Ruff, secret/private-marker scan, `tests/test_select_validation.py`, and `tests/test_pyright_advisory_report.py`.
- Recommended commands selected: `python3 tools/check_agent_docs.py` and `python3 tools/run_pyright_advisory_report.py`.

## Validation Run

Pre-edit focused validation:

```text
py -m pytest -q tests\test_select_validation.py
25 passed in 0.63s
```

Pre-edit Pyright context:

```text
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
0 errors, 0 warnings, 0 informations
```

```text
py -m pyright
19 errors, 5 warnings, 0 informations
```

The raw Pyright failure is local resolver noise, not a module implementation failure.

Post-edit focused validation:

```text
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
30 passed in 0.61s
```

```text
py tools\run_pyright_advisory_report.py
status: clean
```

Full validation:

```text
git status --short --branch
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
 M tests/test_select_validation.py
 M tools/select_validation.py
?? .tmp/
?? docs/contracts/repo_wide_pyright_advisory_report.md
?? docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md
?? tests/test_pyright_advisory_report.py
?? tools/run_pyright_advisory_report.py
```

Note: `.tmp/` contained only the temporary issue authorization note used for surface-authorization validation. It was removed after the command ran.

```text
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
30 passed in 0.68s
```

```text
py tools\run_pyright_advisory_report.py
Pyright Advisory Report
mode: advisory
project: pyrightconfig.json
python: <resolved-python>
platform: windows
runner: tools/run_pyright_advisory_report.py
command: pyright --project pyrightconfig.json --pythonpath <python>
pyright_version: 1.1.409
exit_code: 0
errors: 0
warnings: 0
information: 0
type_findings: 0
local_resolver_noise: 0
tooling_config_blockers: 0
status: clean
gate_behavior: advisory_non_blocking
```

```text
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
0 errors, 0 warnings, 0 informations
```

```text
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
selection_status: ok
```

The broad selector reported advisory `zero_changed_paths`. Path-scoped selector over the actual touched paths reported `selection_status: ok` and recommended the new Pyright advisory report helper.

```text
py -m ruff check src tests tools
All checks passed!
```

```text
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
result: passed
```

The broad secret/private-marker scan reported `scanned_paths: 0`. Path-scoped scan over touched paths reported `forbidden: 0`, `warnings: 4`, with warnings limited to textual failed-post artifact references in the contract and handoff.

```text
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
result: passed
```

The broad protected-surface scan reported `changed_paths: 0`. Path-scoped scan over touched paths passed with `forbidden: 0`, `warnings: 0`.

```text
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md
authorization_status: ok
```

The broad surface-authorization scan reported `changed_paths: 0`. Path-scoped authorization over touched paths also returned `authorization_status: ok`.

```text
git diff --check
```

Result: passed with exit code `0`.

Additional recommended validation:

```text
py tools\check_agent_docs.py
result: passed
```

Supplemental raw Pyright comparison after implementation:

```text
py -m pyright
19 errors, 5 warnings, 0 informations
```

Raw Pyright still reports local resolver/import noise for `pytest`, `requests`, and `bs4`, plus the Windows Store `python` alias message. The approved report helper and existing PowerShell wrapper both report cleanly, so this remains classified as local resolver noise, not an issue #98 module blocker.

## Still Unverified

Pending:

- macOS/Linux live execution
- GitHub Actions result after PR submission

Out of scope:

- CI Pyright integration
- Pyright strictness escalation
- broad type cleanup
- parser/runtime/workbook/webhook/App Script behavior changes

## Forbidden Scope Touched

No forbidden parser/runtime/workbook/webhook/App Script/deployment surface was intentionally touched.

No secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, `main` target, #96 closure, or #82 closure were touched.

## Reviewer Focus

Codex E should verify:

- Pyright remains advisory-only and non-gating.
- `tools/run_pyright_advisory_report.py` redacts or normalizes local interpreter paths.
- Report status/classification semantics match the contract.
- Selector now recommends the repo-approved helper, not raw Pyright.
- Tests cover helper classification and selector command text.
- No CI, config, dependency, parser/runtime, workbook/webhook, Apps Script, or production behavior changed.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for repo-wide hardening issue #98: Pyright advisory report artifact.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/98

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_pyright_advisory_report.md

Implementation handoff:
docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md

Expected review artifact:
docs/contract_test_reports/repo_wide_pyright_advisory_report.md

Review the implementation against the issue, contract, diff, and handoff. Lead with findings.

Verify:
- Pyright remains advisory-only and non-gating.
- Zero Pyright findings is not required.
- No CI Pyright gate was added.
- pyrightconfig.json and pyproject.toml were not changed.
- tools/run_pyright_advisory_report.py runs Pyright with pyrightconfig.json and the active Python interpreter path.
- durable report output normalizes or redacts local interpreter paths.
- the report classifies type findings, local resolver noise, and tooling/config blockers.
- helper exit behavior is 0 for clean/advisory/local-resolver-noise reports and 2 for tooling/config blockers or errors.
- tools/select_validation.py recommends python3 tools/run_pyright_advisory_report.py instead of raw pyright, and keeps it recommended rather than required.
- tests/test_pyright_advisory_report.py covers parsing/classification/path redaction.
- tests/test_select_validation.py covers the selector command update.
- parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, main targeting, #96 closure, and #82 closure were not changed.

Run or review:
git status --short --branch
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
py tools\run_pyright_advisory_report.py
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md
git diff --check

If .tmp\issue-98.md is absent locally, create a temporary authorization note from issue #98 before running the surface-authorization command, then remove it afterward unless explicitly asked to keep local helper files.

Produce docs/contract_test_reports/repo_wide_pyright_advisory_report.md with findings, validation, remaining risks, and next recommended role. Do not stage, commit, open a PR, close issues, mark tracker #82 complete, target main, or change runtime/parser/workbook/webhook/App Script behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/98"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/repo_wide_pyright_advisory_report.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_pyright_advisory_report.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "py -m pytest -q tests\\test_pyright_advisory_report.py tests\\test_select_validation.py -> passed, 30 passed"
    - "py tools\\run_pyright_advisory_report.py -> passed, status clean, advisory_non_blocking"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> passed, 0 errors, 0 warnings"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> ok, zero_changed_paths advisory"
    - "path-scoped validation selector over touched paths -> ok, recommends python3 tools/run_pyright_advisory_report.py"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped secret/private-marker scan over touched paths -> warning, 0 forbidden, 4 textual artifact-reference warnings"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped protected-surface gate over touched paths -> passed, 0 forbidden, 0 warnings"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-98.md --authorization-file contract=docs\\contracts\\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\\implementation_handoffs\\repo_wide_pyright_advisory_report_comparison.md -> ok, scanned 0 changed paths"
    - "path-scoped surface authorization over touched paths -> ok, all paths NOT_PROTECTED allowed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "py -m pyright -> supplemental raw-command local resolver noise, 19 errors and 5 warnings"
  stop_conditions:
    - "Do not make Pyright required or failing."
    - "Do not require zero Pyright findings."
    - "Do not change typeCheckingMode, pyrightconfig.json source coverage, broad excludes, or pyproject.toml dependency strategy."
    - "Do not introduce npm, npx, package.json, or package lockfiles."
    - "Do not edit CI unless the user explicitly authorizes a later issue/contract to do so."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or main."
    - "Do not close issue #96."
    - "Do not mark tracker #82 complete."
    - "Do not stage, commit, open a PR, close issues, or merge unless explicitly asked."
```
