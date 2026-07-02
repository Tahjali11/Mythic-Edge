# Contract Test Report: Ruff Low-Churn Exact-Code Cleanup Candidate Selection

## Findings

No blocking findings.

No Ruff scope expansion, parser behavior drift, promotion, CI/config change, unsafe artifact exposure, or missing required validation was found.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/638

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Contract

`docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`

## Implementation Under Test

- Branch: `codex/ruff-low-churn-candidate-638`
- Base: `origin/main`
- Branch sync at review time: `0 0`
- Implementation handoff: `docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The contract authorizes only a tiny behavior-preserving Ruff cleanup for:

- `DTZ001`
- `TRY301`

It explicitly does not authorize:

- cleanup of `PERF403`, `RUF022`, `RUF059`, or any other rule;
- `pyproject.toml`, CI, repo-check, Ruff config, preview-mode, autofix, unsafe-fix, or promotion changes;
- parser/runtime/local app/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior changes;
- security/privacy/release/deploy readiness claims.

## Internal Project Area Reviewed

Quality / Ruff advisory cleanup.

Ruff cleanup owns style/lint conformance only. It does not own parser truth, runtime truth, security assurance, privacy assurance, release readiness, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status Reviewed

`shared_support`

## Files Reviewed

- `tests/test_app_extractors.py`
- `tests/test_diagnostics.py`
- `tools/generate_security_quality_summary.py`
- `docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
- `docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md`

## Checks Run

```powershell
git fetch --prune origin main
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
gh issue view 638 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 567 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m ruff --version
py -m ruff check src tests tools --select DTZ001,TRY301
py -m pytest -q tests\test_app_extractors.py tests\test_diagnostics.py tests\test_security_quality_summary.py
py -m ruff check src tests tools
py -m ruff check src tests tools --select PERF403,RUF022,RUF059 --statistics --exit-zero
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over changed files, contract, and handoff
path-scoped secret/private-marker scan over changed files, contract, and handoff
```

## Results

- Branch sync: `0 0` with `origin/main`
- Issue state: #638 open; tracker #567 open
- Ruff version: `ruff 0.15.12`
- Selected-code Ruff: passed for `DTZ001,TRY301`
- Focused tests: `42 passed`
- Full Ruff: passed
- Deferred-code check: still reports `PERF403` x1, `RUF022` x2, `RUF059` x3, confirming the deferred rules were not cleaned in this slice
- `git diff --check`: passed
- Agent docs check: passed, errors `0`, warnings `0`

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| None | N/A | `final_approval` | no findings | not_blocking | N/A | Contract review and validation passed | F |

## Confirmed Contract Matches

- Only the selected rules `DTZ001` and `TRY301` were cleaned.
- `PERF403`, `RUF022`, and `RUF059` remain deferred and untouched.
- `pyproject.toml` was not changed.
- CI and repo-check configuration were not changed.
- Preview mode, autofix, unsafe-fix, broad cleanup, and rule promotion were not used.
- `tests/test_app_extractors.py` now uses a timezone-aware UTC datetime while preserving the same `_event_datetime` and `_safe_iso` test intent.
- `tests/test_diagnostics.py` uses a helper to raise the same `RuntimeError` and preserves router failure assertions.
- `tools/generate_security_quality_summary.py` keeps the same `UnsafeInputError` source IDs and reason strings for CodeQL unsupported/unavailable states.
- No parser source, parser state final reconciliation, parser event class, match/game identity, deduplication, analytics, workbook, webhook, Apps Script, Sheets, AI/coaching, Line Tracer, production, fixture, or corpus behavior changed.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

The existing focused tests cover the changed test/tool behavior, including security-summary public-safe blocked-input behavior.

## Drift Notes

- Issue lifecycle drift: none. #638 and tracker #567 are open.
- Repo drift: none observed. Branch is synced with `origin/main`.
- Ruff drift: selected rules are now clean; deferred rules remain nonzero as expected.
- CI drift: GitHub Actions has not run this local branch yet.
- Workbook, deployment, local-data, parser, analytics, AI, and production drift: not applicable to this scoped quality cleanup.

## Protected-Surface Status

Path-scoped protected-surface scan:

- Forbidden: `0`
- Warnings: `0`
- Result: passed

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan:

- Forbidden: `0`
- Warnings: `1`
- Result: warning

The warning is a pre-existing test-name marker in `tests/test_diagnostics.py` mentioning runtime status. It is not raw/private/generated data, and the cleanup removed the raw-log-shaped header fixture from the touched test.

## Generated / Private Artifact Status

Generated/private artifacts kept: false.

No raw logs, generated artifacts, local-only artifacts, workbook exports, failed posts, secrets, credentials, endpoint values, tokens, private paths, or private scanner output were added.

## Forbidden Scope Touched

False.

## Recommendation

Approve for Codex F.

Codex F should stage only the reviewed #638 files and open/update the draft PR. Codex G remains responsible for any later merge, issue closure, tracker update, and CI/deployer closeout.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #638.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/638

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-low-churn-candidate-638

Base:
origin/main

Contract:
docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md

Review artifact:
docs/contract_test_reports/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

Goal:
Submit the reviewed #638 Ruff low-churn exact-code cleanup package. Stage only reviewed files, commit, push, and open/update a draft PR. Do not merge or close issues.

Reviewed files:
- tests/test_app_extractors.py
- tests/test_diagnostics.py
- tools/generate_security_quality_summary.py
- docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md
- docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md
- docs/contract_test_reports/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md

Validation to confirm before commit:
- git status --short --branch --untracked-files=all
- py -m ruff check src tests tools --select DTZ001,TRY301
- py -m pytest -q tests\test_app_extractors.py tests\test_diagnostics.py tests\test_security_quality_summary.py
- py -m ruff check src tests tools
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over reviewed files
- path-scoped secret/private-marker scan over reviewed files

Do not:
- stage unrelated files;
- edit pyproject.toml, CI, Ruff config, preview mode, autofix, unsafe-fix, or promotion settings;
- clean up PERF403, RUF022, RUF059, or any other rule;
- merge, close #638, close tracker #567, or target production behavior.

Final output:
- staged files
- commit hash
- PR URL
- validation results
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/638"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md"
  implementation_handoff: "docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md"
  risk_tier: "Medium workflow risk; low runtime risk because cleanup remained test/tool-only"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-low-churn-candidate-638"
  selected_cleaned_codes:
    - "DTZ001"
    - "TRY301"
  deferred_candidate_codes:
    - "PERF403"
    - "RUF022"
    - "RUF059"
  contract_test_verdict: "passed_no_blocking_findings"
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m ruff --version -> ruff 0.15.12"
    - "py -m ruff check src tests tools --select DTZ001,TRY301 -> passed"
    - "py -m pytest -q tests\\test_app_extractors.py tests\\test_diagnostics.py tests\\test_security_quality_summary.py -> 42 passed"
    - "py -m ruff check src tests tools -> passed"
    - "py -m ruff check src tests tools --select PERF403,RUF022,RUF059 --statistics --exit-zero -> deferred rules still nonzero as expected"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> warning, forbidden 0, warnings 1 pre-existing diagnostics test-name marker"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "warning, forbidden 0, warnings 1 pre-existing diagnostics test-name marker"
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  remaining_risks:
    - "GitHub Actions has not run this local branch yet."
    - "Codex G still owns merge, issue closure, and tracker lifecycle after submitter work."
  next_recommended_role: "Codex F: Module Submitter"
```
