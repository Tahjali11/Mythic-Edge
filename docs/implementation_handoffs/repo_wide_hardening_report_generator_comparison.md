# Repo-Wide Hardening Report Generator Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/100

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_hardening_report_generator.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed before editing:

- `codex/repo-wide-hardening-run`

Initial in-scope status:

```text
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
?? docs/contracts/repo_wide_hardening_report_generator.md
```

During implementation, unrelated untracked local files were observed and excluded from this module:

- `docs/codex_skill_bundle.md`
- `docs/codex_skills/`
- `tools/install_codex_skills.py`
- `tools/install_mythic_edge_skill.py`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/repo_wide_hardening_report_generator.md`
- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/contracts/repo_wide_golden_fixture_first_pass.md`
- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`
- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`
- `tools/check_secret_patterns.py`
- `tools/check_agent_docs.py`
- `tools/check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tools/select_validation.py`
- `tools/run_pyright_advisory_report.py`
- `.github/pull_request_template.md`

## Current Behavior Compared To Contract

Current repo-wide hardening state already has individual evidence producers:

- secret/private-marker scanner
- protected-surface gate
- protected-surface authorization checker
- agent-docs checker
- validation selector
- Pyright advisory report helper
- repo-wide child contracts, handoffs, and several review reports

Current gap addressed by this pass:

- No tracked, deterministic status-report generator existed to assemble repo-local artifact presence and optional operator-supplied evidence into one Markdown hardening status report.
- No focused tests existed for report generation, manifest handling, missing evidence, redaction, output-path restrictions, or no command/network execution.
- The validation selector did not yet map the new generator to its focused tests.

## Implementation Option Chosen

Implemented the smallest report-only generator:

- Markdown-only first pass.
- Optional JSON evidence manifest input.
- Direct repo-local artifact presence inventory.
- Missing evidence rendered explicitly.
- Output writes allowed only under `docs/contract_test_reports/`.
- No subprocess, no network imports, no live GitHub calls, no validation execution.
- No merge readiness, deploy readiness, issue closure, or tracker completion decision.
- Narrow selector mapping added for the new generator and its focused tests.

JSON report output was deferred because the contract makes it optional and Markdown is the required first output format.

## Files Changed

- `tools/generate_hardening_report.py`
- `tests/test_hardening_report_generator.py`
- `tools/select_validation.py`
- `tests/test_select_validation.py`
- `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`
- `docs/contract_test_reports/repo_wide_hardening_status_report.md`

Also present as the in-scope source artifact:

- `docs/contracts/repo_wide_hardening_report_generator.md`

## Code Changed

Only repo hardening/reporting tooling changed.

No parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only runtime artifacts, production behavior, or `main` targeting changed.

## CLI / Report / Test Sections Changed

`tools/generate_hardening_report.py` adds:

- constants for report metadata and expected repo-wide hardening artifacts
- repo-relative artifact inventory
- optional evidence manifest loading and validation
- unsupported status/state normalization to `unknown`
- missing-evidence collection
- redaction for local paths, usernames, webhook URLs, workbook/document/deployment IDs, credential-like values, private-key markers, raw log markers, and private artifact snippets
- deterministic Markdown rendering with the required sections
- `--repo-root`, `--output`, `--evidence-manifest`, and `--format markdown`
- output-path validation restricted to Markdown files under `docs/contract_test_reports/`

`tests/test_hardening_report_generator.py` covers:

- stdout-only Markdown rendering
- approved output file writing
- unsafe output-path rejection
- malformed manifest exit `2`
- operator-supplied issue, PR, validation, CI, residual-risk, and next-role evidence
- unsupported status/state warnings rendered as deterministic report notes
- sorted artifact inventory
- artifact presence not treated as validation success
- redaction of private values
- no command/network module imports

`tools/select_validation.py` adds a focused mapping for:

- `tools/generate_hardening_report.py`
- `tests/test_hardening_report_generator.py`

`tests/test_select_validation.py` adds selector coverage for that mapping.

## Generated Status Report

Generated report path:

- `docs/contract_test_reports/repo_wide_hardening_status_report.md`

The generated report is a status report, not the future post-hardening comparison report. It includes:

- `merge_readiness: not_decided_by_report`
- `deploy_readiness: not_decided_by_report`
- `tracker_completion: not_decided_by_report`

## Contract Matches

- Standard-library-only generator.
- Deterministic Markdown report.
- Stdout support with no file writes.
- `--output` support for the approved report location.
- Optional JSON evidence manifest support.
- Missing evidence rendered as `not_supplied`, `not_run`, or `missing`.
- Artifact presence is separate from validation success.
- Merge readiness, deploy readiness, and tracker completion are not decided.
- Private/local values are redacted before rendering.
- The generator does not run validation commands.
- The generator does not query GitHub live.
- No CI gates or merge-readiness automation were added.
- No parser/runtime/workbook/webhook/App Script/protected data behavior changed.

## Contract Mismatches

No clear contract mismatch remains in the implemented scope.

Intentional deferrals:

- JSON report output is not implemented in this first pass.
- The generator does not parse arbitrary Markdown handoffs or tool reports.
- The first durable report does not decide the future post-hardening comparison report.

## Missing Safeguards Or Missing Tests

Addressed:

- Missing report generator.
- Missing report-generator tests.
- Missing redaction tests for manifest-rendered values.
- Missing output-path restriction tests.
- Missing selector focused-test mapping.

Still intentionally missing:

- Live GitHub metadata collection.
- Automatic validation command execution.
- CI report generation or publishing.
- Merge/deploy readiness automation.
- Tool-report file parsing beyond artifact presence and manifest-supplied evidence.

## Missing-Evidence Behavior

Missing evidence is rendered explicitly in `## Missing Evidence`.

The report does not treat absent validation, absent CI metadata, absent issue/PR state, absent review reports, or absent artifacts as passed. It labels them as `not_supplied`, `not_run`, or `missing`.

## Redaction / Private-Data Behavior

The generator redacts rendered manifest values before Markdown output.

Covered by focused tests:

- local home paths and usernames
- live-looking Apps Script/webhook URLs
- spreadsheet/workbook/deployment identifiers
- credential-like assignments
- raw log markers

The generator rejects unsafe output paths under local/private/generated areas by allowing only Markdown outputs under `docs/contract_test_reports/`.

## No-Command / No-Live-GitHub Confirmation

`tools/generate_hardening_report.py` does not import `subprocess`, `requests`, `urllib`, or `socket`.

The generator reads repo-local files and an optional local JSON manifest only. It does not run validation commands, query GitHub, update issues, comment on PRs, or mutate trackers.

## Merge / Deploy Readiness No-Authority Confirmation

The report explicitly says:

- `merge_readiness: not_decided_by_report`
- `deploy_readiness: not_decided_by_report`
- `tracker_completion: not_decided_by_report`

The workflow handoff section warns that the generated report is not merge or deploy approval.

## Validation Run

Status:

```text
git status --short --branch
## codex/repo-wide-hardening-run...origin/codex/repo-wide-hardening-run
 M tests/test_select_validation.py
 M tools/select_validation.py
?? docs/codex_skill_bundle.md
?? docs/codex_skills/
?? docs/contract_test_reports/repo_wide_hardening_status_report.md
?? docs/contracts/repo_wide_hardening_report_generator.md
?? docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md
?? tests/test_hardening_report_generator.py
?? tools/generate_hardening_report.py
?? tools/install_codex_skills.py
?? tools/install_mythic_edge_skill.py
```

Focused validation:

```text
py -m pytest -q tests\test_hardening_report_generator.py
9 passed
```

```text
py -m pytest -q tests\test_hardening_report_generator.py tests\test_select_validation.py
35 passed
```

Style validation:

```text
py -m ruff check src tests tools
All checks passed!
```

Generator validation:

```text
py tools\generate_hardening_report.py
passed; printed deterministic Markdown to stdout and did not write an output file
```

```text
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
passed; wrote docs/contract_test_reports/repo_wide_hardening_status_report.md
```

Hardening gates:

```text
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
result: passed; scanned_paths: 0
```

Path-scoped secret/private-marker scan over the seven touched/in-scope paths:

```text
result: warning; forbidden: 0; warnings: 5
```

The five warnings are policy-text artifact references in the contract and handoff stop-condition wording. No secret, credential, webhook URL, workbook ID, deployment ID, raw private log, local username, generated data dump, runtime status payload, failed-post payload, or workbook export was reported.

```text
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
result: passed; changed_paths: 0
```

Path-scoped protected-surface gate over the seven touched/in-scope paths:

```text
result: passed; forbidden: 0; warnings: 0
```

```text
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
authorization_status: ok; changed_paths: 0
```

Path-scoped surface-authorization check over the seven touched/in-scope paths:

```text
authorization_status: ok; all paths NOT_PROTECTED allowed
```

Temporary `.tmp\issue-100.md` authorization evidence was created for the surface-authorization command and removed afterward.

Selector and related checks:

```text
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
selection_status: ok; zero_changed_paths advisory
```

Path-scoped selector over the seven touched/in-scope paths:

```text
selection_status: ok
```

It selected the new `hardening_report_generator_tests` focused command, existing selector tests, Ruff, protected-surface gate, secret/private-marker scan, `git diff --check`, and recommended the agent-docs checker and Pyright advisory report.

```text
py tools\check_agent_docs.py
result: passed
```

```text
py tools\run_pyright_advisory_report.py
status: clean; gate_behavior: advisory_non_blocking
```

```text
git diff --check
passed
```

## Protected-Surface Status

No parser/runtime/workbook/webhook/App Script protected surfaces were intentionally touched.

Touched surfaces are hardening tool/test/report surfaces.

## Surface-Authorization Status

Broad changed-file mode returned `authorization_status: ok` with `changed_paths: 0`.

Path-scoped mode over the actual touched paths returned `authorization_status: ok`; all paths were `NOT_PROTECTED allowed`.

## Secret / Private-Marker Status

Broad changed-file mode passed with `scanned_paths: 0`.

Path-scoped mode over the actual touched paths returned `result: warning`, `forbidden: 0`, `warnings: 5`. The warnings are expected policy-text artifact references in the contract/handoff, not leaked private data.

## Validation-Selector Status

The selector now recommends `python3 -m pytest -q tests/test_hardening_report_generator.py` for generator/tool test changes.

Broad selector mode returned `selection_status: ok` with zero changed paths.

Path-scoped selector mode over the actual touched paths returned `selection_status: ok` and selected the new focused report-generator test command.

## What Remains Unverified

- Codex E independent review.
- GitHub Actions behavior after PR submission.
- Any future operator-supplied evidence manifest for final hardening status.
- Any future post-hardening comparison report.
- Cross-platform execution outside this Windows thread.

## Forbidden Scope Touched

No forbidden parser/runtime/workbook/webhook/App Script/deployment or private-data scope was touched.

The unrelated untracked skill-installation files observed in the worktree were not edited or absorbed into this module.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for repo-wide hardening issue #100: Hardening report generator.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/100

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_hardening_report_generator.md

Implementation handoff:
docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md

Generated status report:
docs/contract_test_reports/repo_wide_hardening_status_report.md

Expected review artifact:
docs/contract_test_reports/repo_wide_hardening_report_generator.md

Review the implementation against the issue, contract, diff, generated report, and handoff. Lead with findings.

Verify:
- tools/generate_hardening_report.py is report-only evidence assembly tooling.
- The generator uses only the Python standard library.
- The generator supports stdout and --output docs/contract_test_reports/repo_wide_hardening_status_report.md.
- The generator supports an optional JSON evidence manifest.
- Missing evidence is visible as missing/not_supplied/not_run and is not treated as passed.
- Artifact presence is distinct from validation success.
- The report includes merge_readiness: not_decided_by_report, deploy_readiness: not_decided_by_report, and tracker_completion: not_decided_by_report.
- The generator does not run validation commands.
- The generator does not query GitHub live or import network/command modules.
- The report does not decide merge readiness, deploy readiness, issue closure, or tracker completion.
- Output paths under private/generated/local artifact areas are rejected.
- Private local paths, usernames, webhook URLs, workbook/document/deployment IDs, credential-like values, raw log markers, private artifact snippets, generated data, runtime status, failed posts, and workbook exports are redacted or rejected before durable output.
- The generated status report is not treated as the future post-hardening comparison report.
- tests/test_hardening_report_generator.py covers manifest behavior, missing evidence, deterministic rendering, redaction, output-path restrictions, and no command/network execution.
- tools/select_validation.py only adds the narrow focused-test mapping for the new generator.
- No parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only runtime artifacts, production behavior, main targeting, #96/#98/#100 closure, or tracker #82 completion changed.

Run or review:
git status --short --branch
py -m pytest -q tests\test_hardening_report_generator.py tests\test_select_validation.py
py tools\generate_hardening_report.py
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

If .tmp\issue-100.md is absent locally, create a temporary authorization note from issue #100 before running the surface-authorization command, then remove it afterward unless explicitly asked to keep local helper files.

Produce docs/contract_test_reports/repo_wide_hardening_report_generator.md with findings, validation, remaining risks, and next recommended role. Do not stage, commit, open a PR, close issues, mark tracker #82 complete, target main, or change runtime/parser/workbook/webhook/App Script behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/100"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/repo_wide_hardening_report_generator.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_hardening_report_generator.md"
  generated_status_report: "docs/contract_test_reports/repo_wide_hardening_status_report.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git status --short --branch -> on codex/repo-wide-hardening-run; in-scope files plus unrelated untracked skill-installation files"
    - "py -m pytest -q tests\\test_hardening_report_generator.py -> passed, 9 passed"
    - "py -m pytest -q tests\\test_hardening_report_generator.py tests\\test_select_validation.py -> passed, 35 passed"
    - "py tools\\generate_hardening_report.py -> passed, Markdown stdout"
    - "py tools\\generate_hardening_report.py --output docs\\contract_test_reports\\repo_wide_hardening_status_report.md -> passed, wrote status report"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped secret/private-marker scan over touched paths -> warning, 0 forbidden, 5 policy-text artifact-reference warnings"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed, scanned 0 changed paths"
    - "path-scoped protected-surface gate over touched paths -> passed, 0 forbidden, 0 warnings"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-100.md --authorization-file contract=docs\\contracts\\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\\implementation_handoffs\\repo_wide_hardening_report_generator_comparison.md -> ok, scanned 0 changed paths"
    - "path-scoped surface authorization over touched paths -> ok, all paths NOT_PROTECTED allowed"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> ok, zero_changed_paths advisory"
    - "path-scoped validation selector over touched paths -> ok, selects hardening_report_generator_tests"
    - "py tools\\check_agent_docs.py -> passed"
    - "py tools\\run_pyright_advisory_report.py -> passed, status clean, advisory_non_blocking"
    - "git diff --check -> passed"
  stop_conditions:
    - "Do not query GitHub live from the generator."
    - "Do not run validation commands from the generator."
    - "Do not add CI gates or merge-readiness automation."
    - "Do not decide merge readiness, deploy readiness, issue closure, or tracker completion."
    - "Do not close #96, #98, #100, or tracker #82."
    - "Do not refresh fixtures, snapshots, baselines, expected outputs, or drift reports."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shape, match identity, game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, credentials, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, production behavior, or main."
    - "Do not stage, commit, open a PR, close issues, or merge unless explicitly asked."
```
