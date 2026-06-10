# Setup App Interactive Wizard Player.log Selection - Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/317

## Parent And Tracker

- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

## Review Finding

`docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md`

CT-317-001 P2: required wizard invalid-path tests were incomplete. Directory/not-file and metadata-denied selected `Player.log` paths were covered only by noninteractive install-mode tests, not the wizard path.

## Internal Project Area

Local App / UI setup tooling, with Quality / Governance and Generated / Local Artifacts as supporting areas.

## Truth Owner

The setup wizard owns local setup readiness and config-writing orchestration only. Parser/state, analytics truth, workbook/webhook/App Script/Sheets, OpenAI/model-provider, AI/coaching, and production behavior remain outside this slice.

## Bridge-Code Status

shared_support

## Role Performed

Codex D: Module Fixer.

## Fault Category

Missing contract-test coverage. No implementation bug was reproduced.

## What Changed

Added two wizard-specific regression tests for invalid manual `Player.log` selection:

- a selected path that is a directory / not a file;
- a selected path whose metadata access raises `PermissionError`.

Both tests drive `run_private_local_v1_setup_wizard(...)`, then cancel after the invalid selection. They prove the wizard does not create install artifacts, does not write config, does not return a setup result, does not echo the raw selected path, and does not read or echo `Player.log` contents.

## Files Changed

- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md`

## Code Changed

Runtime code changed: no.

This D pass was tests plus handoff only.

## Tests Added Or Updated

- Added `test_wizard_manual_player_log_directory_can_cancel_without_writing`.
- Added `test_wizard_manual_player_log_metadata_denied_can_cancel_without_writing`.

## Interface Changes

None.

## Contracted Area Status

The fix stayed inside the contracted interactive setup wizard test area. No backend config write route, browser config editing, live capture startup, parser/runtime behavior, analytics schema/migration definition, workbook/webhook/App Script/Sheets, OpenAI/model-provider, AI/coaching, or production boundary changed.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Results:

- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 25 tests.
- `py -m pytest -q tests\test_analytics_local_app_config.py` -> passed, 22 tests.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py` -> passed, 39 tests, 1 existing FastAPI/Starlette warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed with the existing PowerShell line-ending normalization warning for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan over changed #317 files: passed, forbidden 0, warnings 0.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan over changed #317 files: passed, forbidden 0, warnings 0.

## Generated / Private Artifact Status

No generated SQLite files, app-data files, runtime logs, frontend build output, Player.log files, JSONL artifacts, failed posts, workbook exports, secrets, credentials, or local-only artifacts were created or kept.

Tests used pytest temporary directories only.

## Still Unverified

- Real interactive terminal flow was not manually smoke-tested.
- Real current-user `%LOCALAPPDATA%\MythicEdge` was not mutated.
- Real `Player.log` was not read, copied, hashed, tailed, summarized, stored, or exposed.
- Browser config editing and backend config write routes remain deferred by contract.
- Branch remains behind `origin/codex/analytics-foundation` by the known unrelated #315 frontend package from the review report.

## Reviewer Focus

Ask Codex E to confirm:

- wizard-specific directory/not-file manual selection coverage exists;
- wizard-specific metadata-denied manual selection coverage exists;
- both invalid selections cancel before setup/config/database writes;
- raw selected paths and raw `Player.log` contents are not exposed;
- no runtime implementation or forbidden product behavior changed in this D pass.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #317.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/317

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/setup-app-interactive-wizard-player-log-314

Contract:
docs/contracts/setup_app_interactive_wizard_player_log_selection.md

Implementation handoff:
docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md

Fixer handoff:
docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md

Prior review artifact:
docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md

Confirm CT-317-001 only:
- wizard-specific directory/not-file manual Player.log selection coverage was added;
- wizard-specific metadata-denied manual Player.log selection coverage was added;
- both paths cancel before setup/config/database writes;
- raw selected paths and Player.log contents are not exposed;
- runtime code and forbidden product surfaces were not changed in the D pass.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed #317 files.

Do not stage, commit, push, open a PR, merge, close #317, close #314, close tracker #136, target main, mutate real app-data roots, read/copy/hash/tail raw Player.log contents, add backend config write routes, add browser config editing, start live capture, or change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/317"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/setup-app-interactive-wizard-player-log-314"
  contract_artifact: "docs/contracts/setup_app_interactive_wizard_player_log_selection.md"
  implementation_handoff: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_fixer.md"
  review_artifact: "docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md"
  finding_fixed:
    - "CT-317-001 P2: wizard invalid-path tests now cover manual Player.log directory/not-file and metadata-denied cancel paths."
  code_changed: false
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
