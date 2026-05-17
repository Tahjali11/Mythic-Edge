# Repo-Wide Pyright Advisory Report Contract-Test Report

## Findings

No blocking findings.

The implementation satisfies issue #98 and `docs/contracts/repo_wide_pyright_advisory_report.md`. Pyright remains advisory-only and non-gating, zero findings are not required, no CI gate was added, and the implementation provides a stable report helper plus selector recommendation without changing parser/runtime/workbook/webhook/App Script behavior.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/98
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Branch: `codex/repo-wide-hardening-run`
- Contract: `docs/contracts/repo_wide_pyright_advisory_report.md`
- Implementation handoff: `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`

## Implementation Reviewed

Reviewed changed paths:

- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md`
- `tools/run_pyright_advisory_report.py`
- `tools/select_validation.py`
- `tests/test_pyright_advisory_report.py`
- `tests/test_select_validation.py`

Also verified unchanged protected and configuration surfaces:

- `pyrightconfig.json` unchanged
- `pyproject.toml` unchanged
- `.github/workflows/repo-checks.yml` unchanged
- `tools/run_pyright_advisory.ps1` unchanged

## Contract Matches

- Pyright remains advisory-only and non-gating.
- Zero Pyright findings are not required.
- No CI Pyright gate was added.
- `tools/run_pyright_advisory_report.py` runs `pyright --project pyrightconfig.json --pythonpath <active interpreter>`.
- Durable text and JSON report output normalizes the Python path as `<resolved-python>` and command path as `--pythonpath <python>`.
- Report output includes stable fields for project, platform, runner, command, Pyright version, exit code, finding counts, status, and `gate_behavior: advisory_non_blocking`.
- The helper classifies `clean`, `advisory_findings`, `local_resolver_noise`, `tooling_config_blocker`, and generic `error`.
- Helper exit behavior matches the contract:
  - `0` for clean/advisory/local-resolver-noise reports
  - `2` for tooling/config blockers or generic errors
- `tools/select_validation.py` recommends `python3 tools/run_pyright_advisory_report.py` instead of raw Pyright, and keeps it `recommended`, not `required`.
- `tests/test_pyright_advisory_report.py` covers parsing, classification, advisory exit behavior, local resolver noise, tooling blocker behavior, JSON/text rendering, and path redaction.
- `tests/test_select_validation.py` covers the selector command update for parser/source and dependency/config examples.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocker-level missing tests.

The focused tests cover the important report statuses and selector behavior. Generic `error` exit behavior is implemented through `AdvisoryReport.helper_exit_code`; I verified it directly with an inline import smoke check. A future hardening pass could add a dedicated unit test for that exact branch, but it is not a blocker for this contract.

## Validation Results

Commands run:

```powershell
git status --short --branch
py -m pytest -q tests\test_pyright_advisory_report.py tests\test_select_validation.py
py tools\run_pyright_advisory_report.py
py tools\run_pyright_advisory_report.py --format json
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
py -m ruff check src tests tools
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-98.md --authorization-file contract=docs\contracts\repo_wide_pyright_advisory_report.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_pyright_advisory_report_comparison.md
git diff --check
py -m pytest -q
py tools\check_agent_docs.py
```

Results:

- Branch is `codex/repo-wide-hardening-run` and is even with `origin/codex/repo-wide-hardening-run`.
- Focused tests -> `30 passed`.
- Full pytest -> `766 passed, 1 skipped`.
- Ruff -> passed.
- `py tools\run_pyright_advisory_report.py` -> `status: clean`, `exit_code: 0`, `type_findings: 0`, `local_resolver_noise: 0`, `tooling_config_blockers: 0`, `gate_behavior: advisory_non_blocking`.
- JSON report output redacts local interpreter path as `<resolved-python>`.
- PowerShell advisory wrapper -> `0 errors, 0 warnings, 0 informations`.
- Base secret/private-marker scan -> passed with `scanned_paths: 0`.
- Base protected-surface gate -> passed with `changed_paths: 0`.
- Base surface authorization -> passed with `changed_paths: 0`.
- Base validation selector -> `selection_status: ok` with expected zero-changed-paths advisory.
- `git diff --check` -> passed.
- Agent docs checker -> passed.

Because several intended files are untracked, path-scoped validation was also run over the six implementation paths:

- Path-scoped secret/private-marker scan -> warning-only, `forbidden: 0`, `warnings: 4`.
- Path-scoped protected-surface gate -> passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped surface authorization -> `authorization_status: ok`.
- Path-scoped validation selector -> `selection_status: ok`; required commands included diff check, protected-surface gate, Ruff, secret/private-marker scan, selector tests, and Pyright advisory report tests; recommended commands included agent-docs checker and `python3 tools/run_pyright_advisory_report.py`.

The temporary `.tmp\issue-98.md` authorization helper was created only for the requested surface-authorization run and removed afterward.

## Secret And Private-Marker Status

No forbidden findings.

The path-scoped warnings were expected policy text references in contract/handoff stop-condition prose, not secrets, credentials, webhook URLs, workbook IDs, deployment IDs, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, or local interpreter paths.

## Protected-Surface Status

Protected-surface status is clean.

Path-scoped protected-surface gate reported:

- `changed_paths: 6`
- `forbidden: 0`
- `warnings: 0`

Path-scoped surface authorization reported all six implementation paths as `NOT_PROTECTED allowed` and `authorization_status: ok`.

## Forbidden Scope Status

Forbidden scope was not touched.

Confirmed not changed:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shape
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- live workbook state
- deployed Apps Script state
- secrets, credentials, environment variables
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- local-only artifacts
- production behavior
- main target
- issue #96 closure
- tracker #82 closure

## Remaining Risks

- GitHub Actions have not run for this unsubmitted package.
- The helper currently relies on `pyright` being on `PATH`; if absent or config is unreadable it correctly reports `tooling_config_blocker` and exits `2`.
- A future CI advisory artifact remains out of scope; this pass adds local report tooling and selector guidance only.

## Recommendation

Approve for Codex F / Module Submitter.

Codex F should stage only the reviewed issue #98 package plus this report, commit, push, and open or update a draft PR targeting `codex/repo-wide-hardening-run`, not `main`.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for repo-wide hardening issue #98.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/98

Branch:
codex/repo-wide-hardening-run

Reviewed artifacts:
- docs/contracts/repo_wide_pyright_advisory_report.md
- docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md
- docs/contract_test_reports/repo_wide_pyright_advisory_report.md

Reviewed implementation files:
- tools/run_pyright_advisory_report.py
- tools/select_validation.py
- tests/test_pyright_advisory_report.py
- tests/test_select_validation.py

Submit only the reviewed issue #98 package. Do not stage unrelated files. Do not stage `.tmp` helper files. Do not target main. Do not close issue #98, close issue #96, or mark tracker #82 complete unless explicitly instructed.

Before committing, confirm:
- Pyright remains advisory-only and non-gating.
- Zero Pyright findings are not required.
- No CI Pyright gate was added.
- pyrightconfig.json and pyproject.toml were not changed.
- No parser/runtime/workbook/webhook/App Script behavior changed.

Open or update a draft PR targeting codex/repo-wide-hardening-run.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/98"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/repo_wide_pyright_advisory_report.md"
  reviewed_handoff: "docs/implementation_handoffs/repo_wide_pyright_advisory_report_comparison.md"
  review_artifact: "docs/contract_test_reports/repo_wide_pyright_advisory_report.md"
  target_artifact: "draft PR targeting codex/repo-wide-hardening-run"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  findings:
    - "No blocking findings."
  validation:
    - "py -m pytest -q tests\\test_pyright_advisory_report.py tests\\test_select_validation.py -> 30 passed"
    - "py tools\\run_pyright_advisory_report.py -> status clean, advisory_non_blocking"
    - "py tools\\run_pyright_advisory_report.py --format json -> local interpreter path redacted"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings, 0 informations"
    - "py -m pytest -q -> 766 passed, 1 skipped"
    - "py -m ruff check src tests tools -> passed"
    - "path-scoped secret/private-marker scan -> warning-only, forbidden 0"
    - "path-scoped protected-surface gate -> passed, forbidden 0, warnings 0"
    - "path-scoped surface authorization -> ok"
    - "path-scoped validation selector -> ok; Pyright advisory report recommended, not required"
    - "git diff --check -> passed"
  residual_risk:
    - "GitHub Actions not run."
    - "Future CI advisory artifact remains out of scope."
  stop_conditions:
    - "Do not target main."
    - "Do not close issue #98, close issue #96, or mark tracker #82 complete unless explicitly instructed."
    - "Do not stage unrelated files or temporary .tmp helper files."
    - "Do not make Pyright required or failing."
    - "Do not require zero Pyright findings."
    - "Do not change CI gates, pyrightconfig.json, pyproject.toml, parser behavior, parser state final reconciliation, parser event classes, parser payload shape, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, local-only artifacts, or production behavior."
```
