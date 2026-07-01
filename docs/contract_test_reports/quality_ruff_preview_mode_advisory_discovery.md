# Ruff Preview-Mode Advisory Discovery Contract Test Report

## Findings

No blocking findings remain after the current-base refresh confirmation.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-619-001 | P1 | `fixed_state_followup` | Fixed. The advisory report now matches current `origin/main`. | not_blocking | The contract requires branch freshness and treats a stale target ref/commit as a stop condition before measurement. The earlier report recorded measured commit `87919283dd7837e2a905caa82ae758d41667e5ab` while `origin/main` had advanced. | `git rev-list --left-right --count HEAD...origin/main` returned `0 0`; `git rev-parse HEAD` and `git rev-parse origin/main` both returned `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`. The refreshed report records commit `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`. | F |

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/619

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Contract

`docs/contracts/quality_ruff_preview_mode_advisory_discovery.md`

## Implementation Under Test

- Branch: `codex/ruff-preview-advisory-619`
- Base ref: `origin/main`
- Implementation handoff:
  `docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md`
- Sanitized advisory report:
  `docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json`

## Report Lifecycle

`report_lifecycle`: `initial_contract_test`

## Contract Summary

The contract allows an advisory-only Ruff preview-mode discovery measurement.
Preview mode must stay out of normal Ruff configuration, CI, and repo-check
scripts. Raw Ruff JSON must remain ignored and untracked, while the committed
report must be sanitized, preview-specific, aggregate-only, and explicit about
non-claims. `LOG004` must not be treated as stable blocking-ready.

## Internal Project Area Reviewed

Quality / Governance.

No runtime, parser, analytics, workbook, webhook, Apps Script, Sheets,
OpenAI/model-provider, AI, coaching, Line Tracer, or production area ownership
was moved by the reviewed package.

## Bridge-Code Status Reviewed

`not_bridge_code`

This is quality reporting tooling and documentation. It does not bridge parser
facts into analytics, UI, workbook, Apps Script, Google Sheets, AI, coaching,
or production systems.

## Checks Run

```powershell
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git rev-parse HEAD
git rev-parse origin/main
rg -n "preview|--preview|--select ALL|--fix|unsafe|output-format|LOG004" pyproject.toml .github\workflows\repo-checks.yml tools\run_repo_checks.ps1
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
git check-ignore -v _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-preview-all.json
git check-ignore -v _review_\quality_ruff_preview_advisory\2026-07-01-a3227b6\ruff-rules-all.json
py -m pytest -q tests\test_ruff_preview_advisory_report.py tests\test_ruff_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md
docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md
docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json
tests/test_ruff_preview_advisory_report.py
tools/generate_ruff_preview_advisory_report.py
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md
docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md
docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json
tests/test_ruff_preview_advisory_report.py
tools/generate_ruff_preview_advisory_report.py
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
new-file whitespace/final-newline check over #619 untracked files
```

## Results

- Branch/worktree: correct #619 checkout, synchronized with `origin/main`.
- Issue #619: open.
- Preview mode in normal config/checks: absent from `pyproject.toml`,
  `.github/workflows/repo-checks.yml`, and `tools/run_repo_checks.ps1`.
- Sanitized report JSON: valid.
- Sanitized report schema:
  `quality_ruff_preview_advisory_report.v1`.
- Sanitized report command: advisory preview command with
  `<local-only-raw-json>` placeholder.
- Sanitized report commit: `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`.
- Current `origin/main`: `a3227b611f4333b40a6131d710c3ea5d8a7a9ccc`.
- `LOG004`: `defer_until_stable`, not stable blocking-ready.
- Focused tests: passed, `46 passed`.
- Normal Ruff gate: passed.
- `git diff --check`: passed.
- Agent docs: passed.
- Path-scoped protected-surface scan: passed, `forbidden 0`, `warnings 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden 0`,
  `warnings 0`.
- New-file whitespace/final-newline check: passed.

## Confirmed Contract Matches

- Preview mode remains advisory-only and absent from normal repo checks.
- No `pyproject.toml`, CI, or repo-check script changes were present.
- The report uses a preview-specific schema and explicit preview fields.
- The report records command shape, measured commit, Ruff version, scan scope,
  totals, classification summary, and non-claims.
- Raw preview JSON and Ruff rule metadata paths are ignored by `.gitignore` and
  are not tracked.
- The report does not include raw `affected_paths`, raw diagnostic messages,
  fix edits, source snippets, local absolute paths, raw logs, generated/private
  artifacts, or secret-like values in the checked structure.
- Classification labels are within the contract's advisory label set.
- `LOG004` is deferred until stable.
- No parser/runtime/product behavior change was found in the reviewed file set.

## Contract Mismatches

None remaining.

## Missing Tests

No missing tests were found for the helper/report behavior reviewed.

## Drift Notes

No repository freshness drift remains. The active package and refreshed report
match current `origin/main`.

No workbook drift, deployment drift, parser drift, production drift, issue
lifecycle drift, or tracker lifecycle drift was found in this review.

## Recommendation

Approve for submitter routing.

Codex F may stage only the reviewed #619 files, commit, push, and open a draft
PR. The PR should preserve the advisory-only boundary and should not claim CI,
security, privacy, parser, release, deploy, production, analytics, AI, or
coaching readiness beyond the local validation evidence.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #619.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/619

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-preview-advisory-619

Base / PR target:
origin/main

Contract:
docs/contracts/quality_ruff_preview_mode_advisory_discovery.md

Review artifact:
docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md

Sanitized report:
docs/quality_reports/ruff_advisory/2026-07-01-a3227b6-ruff-preview-advisory-report.json

Goal:
Submit the reviewed #619 advisory-only Ruff preview discovery package. Stage
only the reviewed #619 files, commit, push, and open a draft PR. Preserve the
advisory-only boundary.

Do not enable preview mode in pyproject.toml, CI, or normal repo checks. Do not
run autofix or unsafe-fix. Do not promote any preview rule to blocking. Do not
change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
coaching/Line Tracer/production behavior. Do not stage, commit, push, open a PR,
close #619, or mark tracker #567 complete outside the Codex F submitter scope.

Validation:
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-a3227b6-ruff-preview-advisory-report.json
py -m pytest -q tests\test_ruff_preview_advisory_report.py tests\test_ruff_advisory_report.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over changed #619 files
path-scoped secret/private-marker scan over changed #619 files

Final output:
- branch, commit, and PR URL
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- workflow_handoff block routing to Codex G after draft PR creation
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/619"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/ruff-preview-advisory-619"
  base_ref: "origin/main"
  contract_artifact: "docs/contracts/quality_ruff_preview_mode_advisory_discovery.md"
  implementation_handoff: "docs/implementation_handoffs/quality_ruff_preview_mode_advisory_discovery_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_ruff_preview_mode_advisory_discovery.md"
  fixed_findings:
    - "CT-619-001 P1 fixed: refreshed report commit matches current origin/main a3227b611f4333b40a6131d710c3ea5d8a7a9ccc."
  validation:
    - "py -m json.tool sanitized preview report -> passed"
    - "focused Ruff advisory tests -> passed, 46 tests"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "new-file whitespace/final-newline check -> passed"
  preview_mode_config_status: "absent from pyproject, CI, and repo-check script"
  log004_classification: "defer_until_stable"
  raw_preview_json_status: "ignored and untracked under _review_"
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  codex_f_recommended: true
  next_recommended_role: "Codex F: Module Submitter"
```
