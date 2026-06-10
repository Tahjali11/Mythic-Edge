# Setup App Interactive Wizard Player.log Selection Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/317

## Parent And Tracker

- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

## Internal Project Area

Local App / UI setup tooling, with Quality / Governance, Generated / Local
Artifacts, and Analytics as supporting areas.

## Truth Owner

The setup wizard owns local setup readiness and config-writing orchestration
only. Parser/state remains parser truth, SQLite remains downstream analytics
storage, and the local app remains setup/status display.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Branch: `codex/setup-app-interactive-wizard-player-log-314`
- Base: `origin/codex/analytics-foundation`
- Branch sync before implementation: `0 0`
- Initial status: one untracked contract artifact,
  `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`

## Current Behavior Compared To Contract

The repo already had the noninteractive private-local-v1 setup foundation from
the prior slice:

- `--check`, `--install`, and `--proof` existed.
- `--player-log-path` could write approved config fields through the existing
  config writer.
- selected `Player.log` validation was metadata-only.
- selected missing, directory, and metadata-unreadable paths blocked before
  config write.
- app-data folder creation and SQLite initialization used existing setup and
  migration helpers.
- reports and manifests used symbolic paths.
- existing install/config/generated state blocked and was preserved.
- backend setup/config/status remained read-only.

The missing contract gap was an explicit first-run interactive path:

- no Python `--wizard` mode existed;
- no PowerShell `-Wizard` pass-through existed;
- no setup-flow default Windows `Player.log` metadata detector existed;
- no prompt/decision layer allowed confirm detected, enter manual, skip, or
  cancel before config write;
- no wizard result labels existed for `healthy`, `degraded`, and `blocked`.

## Implementation Option Chosen

Implemented the smallest CLI-first wizard slice authorized by the contract:

- added explicit `--wizard` mode;
- added PowerShell `-Wizard` pass-through;
- added testable prompt/decision helpers with injected input/output;
- added metadata-only default Windows `Player.log` candidate detection;
- made `--wizard` imply install mode plus SQLite initialization after final
  confirmation;
- reused `run_private_local_v1_setup(...)` for all folder, SQLite, manifest,
  setup report, and config-write side effects;
- preserved backend config-write route and browser config editing as deferred.

## Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md`

Contract artifact preserved and included in scope:

- `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

## Exact Sections Changed

### `tools/dev_app/private_local_v1_setup.py`

- Added `WIZARD_REPORT_OBJECT`.
- Added `DEFAULT_WINDOWS_PLAYER_LOG_RELATIVE_PATH`.
- Added `PLAYER_LOG_RECENT_ACTIVITY_SECONDS`.
- Extended `PrivateLocalV1Config` with optional player-log source/display
  labels and setup warnings while preserving defaults.
- Added `PrivateLocalV1WizardConfig`.
- Added `WizardPlayerLogSelection`.
- Added prompt reader/writer type aliases.
- Added `default_windows_player_log_candidate(...)`.
- Added `detect_default_windows_player_log_candidate(...)`.
- Added `run_private_local_v1_setup_wizard(...)`.
- Added wizard prompt/selection/result helpers.
- Updated `_player_log_configuration_status(...)` and
  `_selected_player_log_status(...)` to preserve `detected_default` and
  symbolic display labels.
- Added `--wizard` CLI mode.
- Routed `--wizard --json-report` prompt/status text to stderr so stdout stays
  parseable JSON.

### `tools/dev_app/setup_private_local_v1.ps1`

- Added `[switch]$Wizard`.
- Included `-Wizard` in mutually exclusive setup mode validation.
- Passed `--wizard` to the Python setup helper.

### `tests/test_private_local_v1_setup.py`

- Added default Windows `Player.log` metadata-only detection coverage.
- Added detected-default wizard acceptance coverage.
- Added manual-path wizard acceptance coverage.
- Added skipped-Player.log degraded wizard coverage.
- Added `--wizard --json-report` stdout parseability coverage.
- Added missing-manual-path cancel/no-write coverage.
- Added `--wizard` parse and PowerShell wrapper pass-through assertions.

## Code Changed

Yes. Runtime setup tooling changed only in local private-local-v1 setup helper
and wrapper surfaces.

## Tests Added Or Updated

Yes. Focused setup tests were added in `tests/test_private_local_v1_setup.py`.

## Interface Changes

New public setup interfaces:

- Python CLI flag: `--wizard`
- PowerShell wrapper switch: `-Wizard`

New testable Python helper:

- `run_private_local_v1_setup_wizard(...)`

Additive setup-result object:

- `mythic_edge_private_local_v1_setup_wizard_report`

No backend route, frontend UI, parser event, analytics schema, workbook schema,
webhook payload, Apps Script, Sheets, AI, or production interface changed.

## Contracted Area Status

Stayed inside the contracted Local App / UI setup tooling area. Analytics was
touched only through existing SQLite initialization behavior. Backend/frontend
config editing remained deferred.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_private_local_v1_setup.py
py -m ruff check tools\dev_app\private_local_v1_setup.py tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Results:

- Branch sync: `0 0`.
- `tests\test_private_local_v1_setup.py`: passed, 23 tests.
- Focused Ruff over touched Python files: passed.
- `tests\test_analytics_local_app_config.py`: passed, 22 tests.
- `tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py`: passed, 39 tests with one existing FastAPI/Starlette deprecation warning.
- Repo-wide Ruff: passed.
- `git diff --check`: passed; Git emitted the existing Windows line-ending
  notice for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py`: passed.
- Path-scoped protected-surface scan over changed files: passed, forbidden 0,
  warnings 0.
- Path-scoped secret/private-marker scan over changed files: passed, forbidden
  0, warnings 0.

## Still Unverified

- Real interactive terminal flow was not manually smoke-tested against an
  actual current-user `%LOCALAPPDATA%\MythicEdge` root.
- Real current-user MTGA installation layouts beyond the standard Windows
  candidate remain deferred.
- Browser config editing and backend config write route remain deferred by
  contract.
- Existing-install update/repair remains deferred by contract.

## Protected-Surface Status

No parser behavior, parser final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migration definitions,
analytics ingest semantics, backend config write routes, frontend config
editing, workbook/webhook/App Script/Sheets/output transport/OpenAI/AI/coaching
or production behavior changed.

## Secret And Private Artifact Status

No raw `Player.log` contents, private JSONL artifacts, generated SQLite/WAL/SHM
files, runtime logs, app-data files, failed posts, workbook exports, frontend
build output, secrets, credentials, API keys, tokens, webhook URLs, spreadsheet
IDs, or local-only artifacts were added.

Wizard reports and manifests use symbolic labels. The local config file may
contain the selected `Player.log` path only after user confirmation, as
authorized by the contract.

## Reviewer Focus

Ask Codex E to verify:

- `--wizard` implies install plus SQLite initialization only after final
  confirmation.
- detected default `Player.log` is accepted only after user confirmation.
- manual `Player.log` is accepted only after metadata validation and user
  confirmation.
- skipped `Player.log` produces degraded setup and no config write.
- missing/invalid manual path does not write config or create setup artifacts
  when the user cancels.
- JSON report stdout is parseable while prompts/status text go to stderr.
- reports/manifests/results do not include raw private paths or log contents.
- backend config write routes and browser config editing were not added.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #317.

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

Risk tier:
Medium-High

Goal:
Review the active #317 implementation against the contract. Confirm the first
private-local-v1 setup wizard slice is Windows-first CLI/PowerShell only,
metadata-only for Player.log selection, safe around existing app-data/config,
and does not add backend config write routes or browser config editing.

Review focus:
- Verify Python `--wizard` and PowerShell `-Wizard` are explicit and mutually
  exclusive with check/install/proof modes.
- Verify `--wizard` implies install plus SQLite initialization only after final
  confirmation.
- Verify default Windows `Player.log` candidate detection is metadata-only and
  uses `detected_default` plus `<detected_mtga_player_log>`.
- Verify manual selection uses metadata-only validation and symbolic
  `<selected_player_log>`.
- Verify skipped Player.log produces degraded setup and no Player.log config
  write.
- Verify missing/directory/unreadable manual path blocks that path before config
  write and allows safe cancel/skip behavior.
- Verify existing install/config/generated state remains preserved.
- Verify JSON reports, manifests, setup reports, and test output do not expose
  raw private paths or raw Player.log contents.
- Verify no live capture starts automatically.
- Verify no backend config write route, browser config editing, parser/runtime,
  analytics schema/ingest, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching
  or production behavior changed.

Validation:
git status --short --branch --untracked-files=all
git diff --check
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over:
- docs/contracts/setup_app_interactive_wizard_player_log_selection.md
- docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md
- tools/dev_app/private_local_v1_setup.py
- tools/dev_app/setup_private_local_v1.ps1
- tests/test_private_local_v1_setup.py

Final report must include:
- findings first, ordered by severity
- issue/parent/tracker
- contract and handoff reviewed
- branch and git status
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- verdict for Codex F readiness or route back to Codex D/C/B
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/317"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/setup_app_interactive_wizard_player_log_selection.md"
  target_artifact: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/setup-app-interactive-wizard-player-log-314"
  implementation_summary:
    - "Added explicit Python --wizard mode."
    - "Added PowerShell -Wizard pass-through."
    - "Added metadata-only default Windows Player.log candidate detection."
    - "Added testable prompt/decision helpers for detected, manual, skip, and cancel flows."
    - "Reused existing setup helper for folder creation, SQLite initialization, manifests, reports, and config writes."
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> passed, 23 tests"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py -> passed, 22 tests"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py -> passed, 39 tests, one existing FastAPI/Starlette deprecation warning"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with Windows line-ending notice for setup_private_local_v1.ps1"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
