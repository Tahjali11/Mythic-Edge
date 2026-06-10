# Private Local V1 Installation Wizard And First-Run Configuration - Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/314

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/setup_app_private_local_v1_installation_wizard.md`

## Internal Project Area

Private Local V1 setup app and local-only first-run configuration.

## Truth Owner

Setup helper owns local app-data folder/config setup status only. Parser facts, live capture, analytics schema, workbook, webhook, Apps Script, Sheets, OpenAI/model-provider, AI/coaching, and production behavior remain outside this slice.

## Bridge-Code Status

shared_support

## Role Performed

Codex D: Module Fixer.

## Finding Fixed

CT-314-001 P2: setup-helper tests did not cover selected Player.log not-file and unreadable metadata cases required by the contract.

## What Changed

Added focused setup-helper regression tests for two selected Player.log failure modes:

- a selected `Player.log` path that is actually a directory;
- a selected `Player.log` path whose metadata access is denied.

Both tests prove setup blocks before config/database writes, keeps symbolic display paths, avoids reading Player.log contents, and avoids echoing raw selected paths.

## Files Changed

- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md`

## Code Changed

Runtime code changed: no.

This fixer pass was tests plus handoff only. The existing setup helper already returned stable `not_file` and `unreadable` metadata-denial states.

## Tests Added Or Updated

- Added `test_install_mode_blocks_player_log_directory_without_writing_config`.
- Added `test_install_mode_blocks_unreadable_player_log_metadata_without_writing_config`.

## Interface Changes

None.

## Contracted Area Status

The fix stayed inside the private-local-v1 setup-helper contract-test area. No downstream parser, live capture, analytics schema/migration/ingest, workbook/webhook, Apps Script, Sheets, OpenAI/model-provider, AI/coaching, or production boundary was changed.

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

- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 16 tests.
- `py -m pytest -q tests\test_analytics_local_app_config.py` -> passed, 22 tests.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py` -> passed, 39 tests, 1 existing FastAPI/Starlette warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed with the existing PowerShell line-ending normalization warning for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan over changed #314 files: passed, forbidden 0, warnings 0.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan over changed #314 files: passed, forbidden 0, warnings 0.

## Generated / Private Artifact Status

No generated SQLite files, app-data files, runtime logs, frontend build output, Player.log files, JSONL artifacts, failed posts, workbook exports, secrets, credentials, or local-only artifacts were created or kept.

Tests used pytest temporary directories only.

## Still Unverified

- No interactive setup wizard prompt was implemented or tested in this fixer pass.
- No real default private-local-v1 app-data root was mutated.
- No real Player.log was read, copied, hashed, tailed, summarized, stored, or exposed.
- No browser or live launcher proof was run in this fixer pass.

## Reviewer Focus

Ask Codex E to confirm:

- selected Player.log directory/not-file blocks before config/database writes;
- selected Player.log metadata denial blocks before config/database writes;
- setup result/report surfaces keep `<selected_player_log>` and do not echo raw paths or Player.log contents;
- no runtime code or forbidden product behavior changed in this D pass.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #314.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/setup_app_private_local_v1_installation_wizard.md

Implementation handoff:
docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md

Fixer handoff:
docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md

Prior review artifact:
docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md

Confirm the CT-314-001 fix only:
- setup-helper coverage now includes selected Player.log directory/not-file handling;
- setup-helper coverage now includes selected Player.log unreadable metadata handling;
- both cases block before config/database writes;
- result/report payloads keep symbolic labels and do not expose raw selected paths or Player.log contents;
- this D pass did not change runtime code or forbidden parser/live-capture/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed #314 files.

Do not stage, commit, push, open a PR, merge, close #314, close tracker #136, target main, mutate real app-data roots, read/copy/hash/tail raw Player.log contents, or change parser/runtime/live-capture/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/setup_app_private_local_v1_installation_wizard.md"
  implementation_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md"
  review_artifact: "docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md"
  finding_fixed:
    - "CT-314-001 P2: setup-helper tests now cover selected Player.log not-file and unreadable metadata cases."
  code_changed: false
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
