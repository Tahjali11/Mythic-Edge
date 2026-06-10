# Private Local V1 Installation Wizard And First-Run Configuration - Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Contract Used

- `docs/contracts/setup_app_private_local_v1_installation_wizard.md`

## Artifact Produced

- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- GitHub issue #314
- `docs/contracts/setup_app_private_local_v1_installation_wizard.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_private_local_v1_setup.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`

## Current Behavior Compared To Contract

The repo already had a strong private-local-v1 setup foundation:

- clean/check/proof setup modes;
- generated app-data folder layout;
- existing-install preservation blockers;
- SQLite initialization through existing migrations;
- sanitized manifest/report path labels;
- local app setup status and Player.log status surfaces;
- explicit live capture controls that do not auto-start capture.

The confirmed gaps were:

- local app config reads used plain UTF-8 and rejected UTF-8 with BOM config files;
- setup did not write `app_config.json`;
- setup did not accept a user-confirmed Player.log path;
- setup manifest/report did not include symbolic config-write and Player.log setup status;
- existing `app_config.json` was preserved via generic generated-data detection, but not identified by name.

## Implementation Option Chosen

Implemented a narrow noninteractive setup/config foundation instead of a full interactive wizard.

The chosen slice:

- makes local app config reads tolerate UTF-8 with BOM;
- adds a local app config write helper for approved fields only;
- writes config as UTF-8 without BOM;
- adds `--player-log-path` to the Python setup helper and PowerShell wrapper;
- validates an explicitly selected Player.log path with metadata only;
- writes `player_log_path` and `analytics_database_path` into local-only `app_config.json` during install mode after validation;
- records symbolic Player.log/config-write status in setup result, manifest, and report;
- blocks missing/not-file/unreadable selected Player.log paths before creating folders or writing config;
- names existing `app_config.json` as an existing-install indicator and preserves it.

Deferred:

- interactive wizard prompts;
- generic current-user MTGA Player.log auto-detection;
- browser first-run config editing;
- backend config write route;
- dependency installation as normal install behavior;
- launch-after-setup default behavior changes.

## Files Changed

- `docs/contracts/setup_app_private_local_v1_installation_wizard.md`
- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`
- `src/mythic_edge_parser/local_app/config.py`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_analytics_local_app_config.py`
- `tests/test_private_local_v1_setup.py`

## Exact Sections Changed

### `src/mythic_edge_parser/local_app/config.py`

- Switched config read decoding to `utf-8-sig` for BOM-tolerant reads.
- Added `LocalAppConfigWrite`.
- Added `write_local_app_config()` for approved-field writes only.
- Added shape validation for non-empty string `player_log_path` and `analytics_database_path`.

### `tools/dev_app/private_local_v1_setup.py`

- Added `player_log_path` to `PrivateLocalV1Config`.
- Added explicit selected Player.log metadata-only validation.
- Added symbolic `player_log_configuration` and `config_write` report fields.
- Added setup-owned config writing through the local app config helper.
- Added `--player-log-path`.
- Added existing `app_config.json` detection as a named existing-install blocker.

### `tools/dev_app/setup_private_local_v1.ps1`

- Added `-PlayerLogPath`.
- Routed it to `--player-log-path`.

### `tests/test_analytics_local_app_config.py`

- Added UTF-8 BOM config read coverage.
- Added UTF-8 without BOM config write coverage.
- Added unexpected-field write rejection coverage.

### `tests/test_private_local_v1_setup.py`

- Added install-mode Player.log config write coverage.
- Added check-mode metadata-only, non-mutating Player.log validation coverage.
- Added missing selected Player.log blocker coverage.
- Added existing `app_config.json` preservation coverage.
- Updated wrapper coverage for `--player-log-path`.

## Change Classification

- Code changed: yes, setup/local-app config only.
- Tests changed: yes, focused setup/config tests.
- Docs changed: yes, contract artifact and implementation handoff.
- Frontend changed: no.
- Backend route shape changed: no.
- Analytics schema or migrations changed: no.
- Parser behavior changed: no.
- Live capture behavior changed: no.
- Generated artifacts kept: no.

## Validation Run

- `py -m pytest -q tests\test_private_local_v1_setup.py tests\test_analytics_local_app_config.py` -> passed, 36 tests
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py` -> passed, 39 tests, 1 existing FastAPI/Starlette deprecation warning
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 14 tests
- `py -m pytest -q tests\test_analytics_local_app_config.py` -> passed, 22 tests
- `py -m ruff check src tests tools` -> passed
- `git diff --check` -> passed with PowerShell line-ending normalization warning for `tools/dev_app/setup_private_local_v1.ps1`
- `py tools\check_agent_docs.py` -> passed
- path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0

## Protected Surface Status

No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or production behavior was intentionally changed.

No live capture startup behavior was added. The setup helper only validates selected Player.log metadata and writes local config when explicitly supplied.

## Secret / Private Marker Status

The implementation stores raw `player_log_path` and `analytics_database_path` only in local-only `app_config.json`, which is the contract-approved local config target.

Setup results, manifests, reports, tests, and handoff text use symbolic labels and do not include raw private paths, raw Player.log body, hashes, secrets, endpoint values, environment values, generated SQLite contents, or raw logs.

## Generated / Private Artifact Status

No generated SQLite files, app-data files, runtime logs, frontend build output, Player.log files, JSONL artifacts, failed posts, workbook exports, secrets, credentials, or local-only artifacts were committed.

Tests used pytest temporary directories only.

## Remaining Risks Or Unverified Layers

- No interactive wizard prompt was implemented.
- No generic current-user MTGA Player.log auto-detector was implemented in this slice.
- No browser first-run setup UI was changed.
- No backend config write route was added.
- No real default private-local-v1 root was mutated.
- No live browser or launcher proof was run in this thread.
- The PowerShell wrapper line-ending warning remains a Git working-tree normalization warning, not a behavior change.

## Forbidden Scope

Forbidden scope was not touched intentionally:

- no live capture auto-start;
- no raw Player.log read/copy/hash/tail/print/exposure;
- no parser/runtime behavior change;
- no analytics schema/migration/ingest semantic change;
- no workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior change;
- no destructive cleanup, reset, uninstall, import, SQL browser, or external send behavior;
- no staging, commit, push, PR, merge, or issue closure.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #314.

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

Goal:
Review the #314 setup/config implementation against the contract. Start from a contract-test stance: verify the implementation is a narrow private-local-v1 setup/config slice, not a broad wizard, parser, live capture, analytics schema, backend route, or production behavior change.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/setup_app_private_local_v1_installation_wizard.md
- docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md
- src/mythic_edge_parser/local_app/config.py
- tools/dev_app/private_local_v1_setup.py
- tools/dev_app/setup_private_local_v1.ps1
- tests/test_analytics_local_app_config.py
- tests/test_private_local_v1_setup.py
- relevant setup/backend tests if needed

Review focus:
- Local app config reads tolerate UTF-8 with BOM.
- Config writes use approved fields only and write UTF-8 without BOM.
- Explicit `--player-log-path` is treated as user-confirmed input.
- Selected Player.log validation uses metadata only and does not read, copy, hash, tail, print, or expose raw Player.log content.
- Setup writes raw paths only to local-only `app_config.json`, not reports/handoffs/API display.
- Setup report and manifest use symbolic Player.log/config status.
- Missing/not-file/unreadable selected Player.log paths fail closed before config/database writes.
- Existing `app_config.json` is preserved and not overwritten.
- Check mode remains non-mutating.
- No live capture auto-start was added.
- No parser/runtime, analytics schema/migration/ingest, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Validation:
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Output:
- findings first, ordered by severity
- contract matches and mismatches
- validation run and result
- protected-surface/private-artifact status
- whether #314 can proceed to Codex F or must route to Codex D/B
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/setup_app_private_local_v1_installation_wizard.md"
  implementation_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  implementation_summary:
    - "Added BOM-tolerant local app config reads."
    - "Added approved-field config writes as UTF-8 without BOM."
    - "Added explicit setup --player-log-path metadata-only validation and local config writing."
    - "Added symbolic Player.log/config write status to setup result, manifest, and report."
    - "Preserved existing app_config.json as a named existing-install blocker."
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py tests\\test_analytics_local_app_config.py -> passed, 36 tests"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py -> passed, 39 tests, 1 existing FastAPI/Starlette deprecation warning"
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> passed, 14 tests"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py -> passed, 22 tests"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with PowerShell line-ending normalization warning for tools/dev_app/setup_private_local_v1.ps1"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
