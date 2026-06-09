# Private Local V1 Setup Wizard Closeout - Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/314

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Source Report

`docs/contract_test_reports/setup_app_private_local_v1_wizard_closeout_readiness.md`

## Review Finding

CT-314-CLOSEOUT-001 P1: disposable managed `--proof --stop-after-verify` reported `process_cleanup: stopped_proof_started_processes`, but a proof-started frontend process tree remained alive on Windows.

## Role Performed

Codex D: Module Fixer.

## Fault Category

Implementation bug in proof/launcher cleanup semantics.

## What Changed

Updated the local dev launcher cleanup path so Windows cleanup attempts to stop the full process tree for launcher-started processes by using `taskkill /PID <pid> /T /F`.

Updated `cleanup_children(...)` to return whether all started child roots were actually stopped. Updated private-local-v1 proof reporting so it records `process_cleanup: cleanup_incomplete` and adds `process_cleanup_incomplete` to errors if cleanup does not complete. This prevents proof reports from claiming cleanup success when a started process survives.

## Files Changed

- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/private_local_v1_setup.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/setup_app_private_local_v1_wizard_closeout_fixer.md`

## Code Changed

Yes. Runtime setup/dev-launcher cleanup behavior changed only for launcher-started backend/frontend child processes.

No setup wizard prompt behavior, config writing, Player.log validation, SQLite initialization, launch/status HTTP checks, parser/runtime behavior, analytics schema, workbook/webhook/App Script/Sheets, OpenAI/model-provider, AI/coaching, live capture, or production behavior changed.

## Tests Added Or Updated

- Added launcher coverage proving Windows cleanup uses `taskkill /T /F` for a started child with a PID.
- Added launcher coverage proving cleanup returns incomplete when a started child survives terminate/kill.
- Added proof coverage proving `run_private_local_v1_proof(...)` reports `cleanup_incomplete` and fails the proof instead of overclaiming cleanup success when a started frontend process survives.

## Interface Changes

- `tools.dev_app.dev_app_launcher.cleanup_children(...)` now returns `bool`.

Existing callers may ignore the return value. The private-local-v1 proof path uses it for truthful cleanup reporting.

## Contracted Area Status

The fix stayed inside local setup proof and dev launcher cleanup behavior. It does not broaden setup, wizard, parser, analytics, workbook, webhook, Apps Script, Sheets, AI/coaching, live capture, or production scope.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Results:

- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_private_local_v1_setup.py` -> passed, 38 tests.
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py` -> passed, 51 tests, 1 existing FastAPI/Starlette warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan over changed closeout files: passed, forbidden 0, warnings 0.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan over changed closeout files: passed, forbidden 0, warnings 0.

## Generated / Private Artifact Status

No generated SQLite files, app-data files, runtime logs, frontend build output, Player.log files, JSONL artifacts, failed posts, workbook exports, secrets, credentials, or local-only artifacts were created or kept by this fixer pass.

Tests used pytest temporary directories and fake process objects only.

## Still Unverified

- A live disposable managed `--proof --stop-after-verify` rerun was not performed in this D pass.
- The real default `%LOCALAPPDATA%\MythicEdge` root was not used or mutated.
- No real Player.log was read, copied, hashed, tailed, summarized, stored, or exposed.

## Reviewer Focus

Ask Codex E to confirm:

- Windows cleanup attempts process-tree cleanup for launcher-started processes.
- Proof reporting no longer claims `stopped_proof_started_processes` when cleanup is incomplete.
- The previous disposable managed proof should be rerun in a controlled temp root to confirm the frontend process tree no longer remains alive.
- No forbidden parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/live-capture/production behavior changed.

## Next Workflow Action

Next role: Codex E closeout confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Contract Tester / readiness verifier for issue #314.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch/worktree:
codex/setup-wizard-closeout-314
MythicEdge-setup-wizard-closeout-314

Source report:
docs/contract_test_reports/setup_app_private_local_v1_wizard_closeout_readiness.md

Fixer handoff:
docs/implementation_handoffs/setup_app_private_local_v1_wizard_closeout_fixer.md

Confirm CT-314-CLOSEOUT-001 only:
- Windows cleanup uses process-tree stop for launcher-started backend/frontend processes.
- Private-local-v1 proof reports cleanup success only when cleanup actually completes.
- If cleanup is incomplete, proof reports `cleanup_incomplete` and fails instead of overclaiming success.
- Rerun the controlled disposable managed `--proof --stop-after-verify` check if safe, using temp install/app-data roots and ephemeral ports only.
- Confirm no proof-started frontend process tree remains alive afterward.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed closeout files.

Do not stage, commit, push, open a PR, merge, close #314/#136, target main, start live capture, mutate the real default app-data root, read/copy/hash/tail raw Player.log contents, or commit generated/private/local artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Contract Tester / readiness verifier"
  branch: "codex/setup-wizard-closeout-314"
  worktree: "MythicEdge-setup-wizard-closeout-314"
  base_branch: "codex/analytics-foundation"
  source_report: "docs/contract_test_reports/setup_app_private_local_v1_wizard_closeout_readiness.md"
  fixer_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_wizard_closeout_fixer.md"
  finding_fixed:
    - "CT-314-CLOSEOUT-001 P1: proof cleanup now uses Windows process-tree cleanup for launcher-started children and reports cleanup_incomplete if cleanup fails."
  generated_artifacts_kept: false
  real_default_root_mutated: false
  forbidden_scope_touched: false
```
