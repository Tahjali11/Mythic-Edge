# Setup App Interactive Wizard Player.log Selection Contract Test Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/317
- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/314

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

- `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

## Implementation Under Test

- Branch: `codex/setup-app-interactive-wizard-player-log-314`
- Base branch: `origin/codex/analytics-foundation`
- Implementation handoff: `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md`
- Changed files reviewed:
  - `tools/dev_app/private_local_v1_setup.py`
  - `tools/dev_app/setup_private_local_v1.ps1`
  - `tests/test_private_local_v1_setup.py`
  - `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`
  - `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md`
  - `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md`
  - `docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add a private-local-v1 CLI wizard and PowerShell wrapper path for first-run setup and `Player.log` selection. The wizard must remain metadata-only for `Player.log`, write config only after explicit confirmation and accepted file metadata, preserve existing local app-data/config state, avoid backend/browser config write surfaces, avoid live capture start, and keep parser/runtime/analytics/workbook/AI/production behavior unchanged.

## Internal Project Area Reviewed

- Primary area: Local App / UI setup tooling.
- Supporting areas: Quality / Governance, Generated / Local Artifacts, and Analytics through existing SQLite initialization only.

## Bridge-Code Status Reviewed

`shared_support`. The setup wizard orchestrates existing setup/config helpers but does not own parser truth, analytics truth, workbook truth, production truth, or AI/coaching truth.

## Findings First

No remaining blocking findings.

CT-317-001 is confirmed fixed. The D pass added wizard-specific tests for manual `Player.log` directory/not-file selection and metadata-denied selection, both followed by operator cancel, with assertions that no setup result exists, the install root is not created, and raw selected path or raw `Player.log` body text is not echoed.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --name-status
gh issue view 317 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 314 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 136 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Path-scoped protected-surface and secret/private-marker scans were run over:

- `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`
- `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md`
- `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md`
- `docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`

## Results

- Active branch confirmed: `codex/setup-app-interactive-wizard-player-log-314`.
- Branch sync against `origin/codex/analytics-foundation`: `0 2`; branch is behind by the merged #315 frontend package, which does not overlap the reviewed #317 setup files.
- Issue #317 open.
- Parent issue #314 open.
- Tracker #136 open.
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 25 tests.
- `py -m pytest -q tests\test_analytics_local_app_config.py` -> passed, 22 tests.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py` -> passed, 39 tests, 1 existing FastAPI/Starlette deprecation warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed with the existing Windows line-ending notice for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-317-001 | P2 | `fixed_state_followup` | fixed | not_blocking | Original review found wizard-specific directory/not-file and metadata-denied selected `Player.log` path coverage missing; those cases were covered only by install-mode tests. | `tests/test_private_local_v1_setup.py` now includes `test_wizard_manual_player_log_directory_can_cancel_without_writing` and `test_wizard_manual_player_log_metadata_denied_can_cancel_without_writing`; focused setup pytest passed with 25 tests. | F |

## Confirmed Contract Matches

- Python CLI `--wizard` exists and is mutually exclusive with `--check`, `--install`, and `--proof`.
- PowerShell wrapper `-Wizard` exists and passes `--wizard` to the Python setup helper.
- `--wizard` help text states that the wizard implies install mode and SQLite initialization.
- The implementation uses injected prompt/output helpers for testability.
- Default Windows `Player.log` candidate detection is metadata-only and uses `detected_default` plus `<detected_mtga_player_log>`.
- Manual valid `Player.log` selection is accepted after metadata validation and uses `<selected_player_log>` in reports.
- Skipped `Player.log` produces degraded setup, symbolic `<player_log_not_configured>`, no `player_log_path` config write, and initialized SQLite.
- Missing manual path can be canceled without creating the install root.
- Directory/not-file manual path can be canceled without creating the install root, without a setup result, and without raw selected path echo.
- Metadata-denied manual path can be canceled without creating the install root, without a setup result, and without raw selected path or raw `Player.log` body echo.
- JSON report stdout remains parseable while prompt/status text goes to stderr.
- Existing install/config preservation remains covered by the prior setup tests and the wizard delegates setup writes to `run_private_local_v1_setup(...)`.
- No backend config write route or browser config editing was added.
- No live capture start, parser/runtime behavior, analytics schema/migration definition, analytics ingest semantics, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior changed.

## Contract Mismatches

None remaining.

## Missing Tests

No blocking missing tests remain for CT-317-001.

## Drift Notes

- Branch/package drift: the branch is behind `origin/codex/analytics-foundation` by 2 commits from the merged #315 frontend package. Those commits touch frontend/dashboard files and do not overlap the reviewed #317 setup package. Codex F should resync/recheck before PR submission.
- Repo drift: no reviewed setup-file drift found beyond the active #317 package.
- Workbook/deployment/local-data drift: not applicable; no live workbook, Apps Script, production, real app-data root, or private `Player.log` state was inspected.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the reviewed #317 files reported forbidden 0 and warnings 0.

## Secret And Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the reviewed #317 files reported forbidden 0 and warnings 0.

## Generated/Private Artifact Status

No generated/private artifacts were kept. Validation used pytest temporary directories only.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Approve for Codex F. Stage only the reviewed #317 files, then commit, push, and open or update a draft PR targeting `codex/analytics-foundation`. Codex F should account for the branch being behind by the unrelated merged #315 frontend package before submission.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #317.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/317

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/setup-app-interactive-wizard-player-log-314

Target branch:
codex/analytics-foundation

Contract:
docs/contracts/setup_app_interactive_wizard_player_log_selection.md

Implementation handoff:
docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md

Fixer handoff:
docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md

Review artifact:
docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md

Goal:
Submit the reviewed #317 setup wizard Player.log selection package. Stage only reviewed #317 files, commit, push, and open or update a draft PR targeting codex/analytics-foundation. Do not merge or close issues.

Files approved for staging:
- docs/contracts/setup_app_interactive_wizard_player_log_selection.md
- docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md
- docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md
- docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md
- tools/dev_app/private_local_v1_setup.py
- tools/dev_app/setup_private_local_v1.ps1
- tests/test_private_local_v1_setup.py

Before staging:
- Confirm branch and git status.
- Account for branch drift: branch is known to be behind origin/codex/analytics-foundation by unrelated #315 frontend commits from the Codex E review. Resync/recheck safely before PR submission if needed.
- Confirm no unrelated files are staged.

Suggested validation before commit:
- py -m pytest -q tests\test_private_local_v1_setup.py
- py -m pytest -q tests\test_analytics_local_app_config.py
- py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
- py -m ruff check src tests tools
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over staged files

Do not:
- stage unrelated files
- use or mutate the real default `%LOCALAPPDATA%\MythicEdge` root
- read, copy, hash, tail, summarize, store, or expose raw Player.log contents
- add backend config write routes or browser config editing
- start live capture
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- target main, merge, close #317, close #314, or close tracker #136

Final output:
- role performed
- branch and target branch
- files staged
- commit hash
- PR URL
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- remaining risk
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/317"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/setup-app-interactive-wizard-player-log-314"
  target_branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/setup_app_interactive_wizard_player_log_selection.md"
  implementation_handoff: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md"
  review_artifact: "docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md"
  findings_confirmed_fixed:
    - "CT-317-001 P2: wizard invalid-path tests now cover manual Player.log directory/not-file and metadata-denied cancel paths."
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> passed, 25 tests"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py -> passed, 22 tests"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py -> passed, 39 tests, 1 existing warning"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with existing PowerShell line-ending notice"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Route to Codex F."
```
