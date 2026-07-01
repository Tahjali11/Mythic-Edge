# Quality Protected-Surface Coverage Floor Readiness Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/605>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/566>
- Repository: `Tahjali11/Mythic-Edge`

## Contract Used

- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`

## Branch And Base

- Branch: `codex/protected-surface-coverage-readiness-566`
- Base branch: `main`
- Final measured commit: `83d3141e953913233e3457b910c2c83ff25d44aa`
- Target branch remains `main` only after explicit user approval.

During implementation, `origin/main` advanced twice. The worktree was
fast-forwarded from `024eda7` to `db3a594`, then from `db3a594` to `83d3141`.
The final coverage measurement and public-safe advisory report were regenerated
after the second refresh.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/internal_project_map.md`
- `.github/workflows/repo-checks.yml`
- `pyproject.toml`
- `tools/check_coverage_floor.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation_mappings.py`
- `tools/run_repo_checks.ps1`
- `tests/test_check_coverage_floor.py`
- `tests/test_check_protected_surfaces.py`

## Current Behavior Compared To Contract

Current repo behavior already provides a blocking global Python line coverage
floor through `tools/check_coverage_floor.py`, `pyproject.toml`, and the repo
checks workflow. That gate remains aggregate-only and line-only; branch coverage
is measured but advisory-only.

Before this pass, there was no public-safe protected-surface coverage advisory
report. The protected-surface checker classified paths, but coverage tooling did
not group coverage evidence by parser, workbook, webhook, analytics, local app,
or governance surface. The contract explicitly forbids creating a per-surface
coverage gate in this slice.

## Implementation Option Chosen

Implemented the contract's advisory-report option:

- add a standalone local helper that reads an already-produced coverage XML;
- group repo-relative tracked files into protected/protected-adjacent surface
  buckets;
- mark non-Python or outside-source surfaces as not applicable instead of
  inventing percentages;
- emit one public-safe JSON report under `docs/quality_reports/coverage/`;
- keep protected-surface floor status as `not_authorized`;
- keep branch coverage as `advisory_only`;
- leave CI, `pyproject.toml`, parser behavior, analytics behavior, workbook
  behavior, webhook behavior, Apps Script behavior, AI behavior, and production
  behavior unchanged.

## Files Changed

- `tools/generate_protected_surface_coverage_report.py`
- `tests/test_protected_surface_coverage_report.py`
- `tools/select_validation_mappings.py`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`
- `docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md`
- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md` remained in scope as the contract artifact from Codex B.

## Exact Sections Changed

`tools/generate_protected_surface_coverage_report.py`

- Added report constants for repository, issue, tracker, contract, schema,
  approved coverage source, and advisory non-claims.
- Added protected-surface group definitions for parser, workbook/transport,
  analytics, local app, Apps Script, governance docs, CI YAML, checker tools,
  and forbidden local artifact families.
- Added coverage XML parsing that normalizes coverage filenames to
  repo-relative `src/mythic_edge_parser/...` paths.
- Added report construction with global coverage fields, per-group files,
  not-applicable handling, missing-from-coverage handling, and fail-closed
  symbolic XML error states.
- Added CLI validation that restricts generated reports to
  `docs/quality_reports/coverage/protected_surface/`.

`tests/test_protected_surface_coverage_report.py`

- Added focused tests for advisory flags and global floor boundary.
- Added tests for repo-relative measured file rates.
- Added tests for missing measurable files without fake percentages.
- Added tests for non-Python/out-of-source groups as not applicable.
- Added tests for missing/malformed XML fail-closed behavior without private
  path echo.
- Added tests for default report path and restricted output path.

`tools/select_validation_mappings.py`

- Added focused validation mappings from the new helper and test module to
  `tests/test_protected_surface_coverage_report.py`.

`docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`

- Added sanitized advisory report with schema
  `protected_surface_coverage_advisory.v1`.
- Recorded measured commit `83d3141e953913233e3457b910c2c83ff25d44aa`.
- Recorded global line coverage `87.55`, branch coverage `74.8`, global line
  floor status `passed`, branch coverage status `advisory_only`, and protected
  surface floor status `not_authorized`.
- Recorded measurable and not-applicable surface groups using repo-relative
  paths only.

## Change Type

- Code changed: yes, quality/reporting helper only.
- Tests changed: yes, focused helper tests only.
- Docs changed: yes, implementation handoff and one public-safe advisory report.
- CI changed: no.
- Coverage floor changed: no.
- Protected-surface floor added: no.

## Advisory Report Summary

Final report:

`docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`

Summary:

- `overall_status`: `passed_advisory`
- `coverage_xml_status`: `parsed`
- `global_line_coverage_percent`: `87.55`
- `global_branch_coverage_percent`: `74.8`
- `global_line_floor_status`: `passed`
- `branch_coverage_status`: `advisory_only`
- `protected_surface_floor_status`: `not_authorized`
- `protected_surface_floor_authorized`: `false`
- `ci_change_authorized`: `false`
- `raw_artifacts_committed`: `false`

Measured groups:

- `parser_event_classes`
- `parser_state_final_reconciliation`
- `extractor_behavior`
- `match_game_identity`
- `workbook_schema_and_exports`
- `webhook_payload_and_transport`
- `environment_runtime_python_paths`
- `analytics_schema_and_ingest`
- `local_app_security_and_artifact_safety`

Not-applicable current coverage-scope groups:

- `apps_script_behavior`
- `workflow_authority_docs`
- `workflow_ci_yaml`
- `local_artifact_checker_tools`
- `forbidden_local_artifact_paths`

## Validation Run

- `git fetch --prune` -> passed.
- `git rev-list --left-right --count HEAD...origin/main` -> `0 0` before the final measurement pass.
- `py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term --cov-report=xml:<local ignored XML>` on commit `83d3141` -> passed, `2032 passed`, `4 skipped`, `1` FastAPI/Starlette deprecation warning.
- `py tools\check_coverage_floor.py --coverage-xml _review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\coverage.xml --line-floor 85 --command-label "protected-surface advisory measurement"` -> passed, global line `87.55%`, branch `74.80%` advisory-only.
- `py tools\generate_protected_surface_coverage_report.py --coverage-xml _review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\coverage.xml --coverage-command "py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report=xml:<local-ignored-coverage-xml>" --write-report --report-date 2026-07-01` -> passed.
- `py -m pytest -q tests\test_protected_surface_coverage_report.py` -> passed, `8 passed`.
- `py -m ruff check tools\generate_protected_surface_coverage_report.py tests\test_protected_surface_coverage_report.py` -> passed.
- `py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json > $null` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan over the six changed #605 files -> passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the six changed #605 files -> passed, `forbidden: 0`, `warnings: 0`.
- `git check-ignore -v` for `_review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\.coverage` and `coverage.xml` -> both ignored by `.gitignore:23:_review_*/`.

## Protected-Surface Status

No parser, workbook, webhook, Apps Script, analytics schema, AI, or production
behavior was changed. The only protected-adjacent code change is a quality
reporting helper plus a focused validation mapping.

## Secret/Private Artifact Status

The committed candidate report is sanitized and uses repo-relative paths. It
does not include raw coverage XML, raw terminal transcripts, `.coverage`
contents, HTML coverage output, absolute local paths, private logs, raw
Player.log content, private JSONL artifacts, SQLite databases, workbook exports,
runtime files, failed-post queue artifacts, secrets, credentials, tokens, or
webhook URLs.

Coverage XML and `.coverage` files were created only under ignored `_review_/`
paths during measurement. They are raw local validation artifacts and are not
intended for commit.

## Generated/Private Artifact Status

- Public-safe advisory JSON created under `docs/quality_reports/coverage/protected_surface/`.
- Raw coverage XML and `.coverage` artifacts remain local ignored validation
  artifacts under `_review_/`.
- No generated DB files, app-data files, frontend build output, raw logs,
  workbook exports, or local-only artifacts were added to the tracked package.

## What Remains Unverified

- GitHub Actions has not run this exact branch/package.
- CodeQL/security scans were not part of this contract.
- No protected-surface floor was proposed or calibrated; this pass only records
  advisory evidence.
- If `origin/main` advances again after final validation, Codex E should decide
  whether the report remains acceptable or should be regenerated again.

## Forbidden Scope

Forbidden scope was not touched:

- no CI gate added;
- no per-surface coverage floor added;
- no global line floor increase;
- no branch coverage enforcement;
- no parser behavior change;
- no analytics schema or ingest behavior change;
- no workbook schema, webhook payload, Apps Script, Sheets, AI/coaching, or
  production behavior change;
- no raw/private/local artifact committed.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #605.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/605

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/protected-surface-coverage-readiness-566

Contract:
docs/contracts/quality_protected_surface_coverage_floor_readiness.md

Implementation handoff:
docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md

Advisory report:
docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json

Goal:
Review the #605 package against the contract. Confirm that the implementation is advisory measurement/reporting only, that no protected-surface coverage floor or CI gate was added, and that the sanitized report is public-safe.

Review:
- Confirm branch freshness against origin/main.
- Inspect the contract, handoff, advisory JSON, helper, tests, and validation mapping.
- Verify the report schema is protected_surface_coverage_advisory.v1.
- Verify measured commit and coverage evidence are current enough for review.
- Verify branch coverage is advisory-only.
- Verify protected_surface_floor_status remains not_authorized.
- Verify no CI, pyproject coverage source/floor, parser behavior, analytics schema, workbook/webhook/App Script/Sheets, AI/coaching, production behavior, or raw/private artifact boundary changed.
- Verify the advisory report uses repo-relative paths and does not include raw XML, .coverage contents, local absolute paths, private logs, raw Player.log content, private JSONL artifacts, SQLite DBs, workbook exports, runtime files, failed-post queue artifacts, secrets, credentials, tokens, or webhook URLs.
- Lead with findings ordered by severity.

Suggested validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m pytest -q tests\test_protected_surface_coverage_report.py
py -m ruff check tools\generate_protected_surface_coverage_report.py tests\test_protected_surface_coverage_report.py
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json > $null
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Do not stage, commit, push, open a PR, merge, close #605, mark tracker #566 complete, add CI gates, add protected-surface floors, or change product behavior.

Final output must include:
- role performed
- issue/tracker reviewed
- contract used
- implementation handoff reviewed
- files reviewed
- findings ordered by severity
- advisory report/schema status
- coverage evidence freshness status
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- validation run and result
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/605"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/quality_protected_surface_coverage_floor_readiness.md"
  implementation_handoff: "docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md"
  advisory_report: "docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json"
  branch: "codex/protected-surface-coverage-readiness-566"
  measured_commit: "83d3141e953913233e3457b910c2c83ff25d44aa"
  verdict: "advisory_protected_surface_coverage_report_ready_for_contract_review"
  global_line_coverage_percent: 87.55
  global_branch_coverage_percent: 74.8
  protected_surface_floor_status: "not_authorized"
  branch_coverage_status: "advisory_only"
  raw_coverage_artifacts_committed: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
