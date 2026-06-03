# Private Local V1 Clean Checkout Install And Launch Implementation Comparison

## C Stability Follow-Up

This Codex C pass revalidated the existing #253 implementation from the
contract handoff. Focused validation exposed that proof-mode tests depended on
real workstation port availability for ports `8765` and `5173`, even though
the command, HTTP, and process surfaces were already fake-runner based.

Minimal fix:

- `run_private_local_v1_proof(...)` now accepts an injectable `port_checker`.
- proof-mode tests pass a fake `port_checker` so tests do not depend on local
  port state or running app processes.

This does not change parser behavior, analytics schema, local app runtime
behavior outside setup proof orchestration, workbook/webhook/App Script/Sheets
behavior, AI behavior, production behavior, or generated/private artifact
policy.

Validation for this stability follow-up:

- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 8 passed.
- `py -m pytest -q tests\test_private_local_v1_setup.py tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> passed, 70 passed, 1 existing FastAPI/Starlette warning.
- `py -m ruff check src tests tools` -> passed.
- `py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report`
  -> passed; temp root stayed absent.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- path-scoped protected-surface scan over touched #253 files -> passed,
  forbidden 0, warnings 0.
- path-scoped secret/private-marker scan over touched #253 files -> passed,
  forbidden 0, warnings 0.

Unrelated untracked file left untouched:

- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`

## Follow-Up C Pass After Codex E Readiness Proof

Codex E updated
`docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
with verdict `not_ready_for_user_manual_fresh_install`. The remaining blocker
was not the setup foundation itself; it was that the successful disposable
proof still required reviewer-only manual orchestration.

This Codex C follow-up implements a contract-owned setup proof orchestration
path while keeping validation fake-runner based. No real GitHub clone,
dependency install, long-running backend/frontend process, browser open, or
real default `%LOCALAPPDATA%\MythicEdge\` setup was run by this implementation
pass.

### Follow-Up Current Behavior Compared To Contract

Before this follow-up:

- `--check` and `--install` existed.
- install mode could create the v1 generated folder tree, manifest, setup
  report, and optional empty migrated analytics SQLite database.
- clone/install/start/browser proof evidence existed only in the Codex E
  manual disposable proof report.
- the helper still reported dependency install, backend startup, frontend
  startup, browser open, and status-panel verification as `not_run`.
- clone into `<install_root>\app` was not represented as a helper-owned flow.

After this follow-up:

- `tools/dev_app/private_local_v1_setup.py` exposes `--proof`.
- `tools/dev_app/setup_private_local_v1.ps1` exposes `-Proof`.
- proof mode owns the sequence for source selection or clone, venv creation,
  Python dependency install, frontend dependency install, setup install,
  backend/frontend startup, loopback HTTP checks, optional browser open, and
  cleanup of only proof-started processes.
- focused tests cover the proof sequence with fake command/http/process hooks,
  including fake clone into `<install_root>\app`.
- generated setup reports can now be updated with proof statuses when proof
  mode reaches the durable-report stage.

### Follow-Up Implementation Option Chosen

Implemented proof orchestration with injectable runners rather than running the
real proof during C validation. This closes the repo-owned orchestration gap
without performing real machine mutation in the implementation thread.

Full live proof remains Codex E work.

### Follow-Up Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`

Pre-existing modified file from Codex E, left intact:

- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`

### Follow-Up Exact Sections Changed

`tools/dev_app/private_local_v1_setup.py`:

- added `PrivateLocalV1ProofConfig`;
- added `CommandOutcome`, `CommandRunner`, and `HttpVerifier`;
- added `run_private_local_v1_proof(...)`;
- added sanitized `run_command(...)` and `verify_http_url(...)` helpers;
- added proof dependency/report helpers;
- added managed-app-checkout handling so setup-owned clone into
  `<install_root>\app` is not mistaken for unrelated existing install state;
- added CLI flags `--proof`, `--repo-url`, `--release-ref`, `--no-open`,
  `--leave-running`, `--stop-after-verify`, `--backend-port`, and
  `--frontend-port`.

`tools/dev_app/setup_private_local_v1.ps1`:

- added `-Proof`;
- added pass-through flags for repo URL, release ref, browser/open behavior,
  process cleanup behavior, and backend/frontend ports;
- preserved wrapper shape without inline `git clone`, `npm ci`, `pip install`,
  delete, reset, or cleanup commands.

`tests/test_private_local_v1_setup.py`:

- added fake-runner proof coverage for controlled existing-checkout mode;
- added fake-runner proof coverage for clone into `<install_root>\app`;
- extended wrapper assertions for the new public flags.

### Follow-Up Still Unverified

- Live GitHub clone through the new proof command.
- Real virtualenv creation through the new proof command.
- Real Python dependency install through the new proof command.
- Real `npm ci` through the new proof command.
- Real backend/frontend startup through the new proof command.
- Real browser-open/rendered status-panel smoke.
- Real default `%LOCALAPPDATA%\MythicEdge\` readiness.
- Git cleanliness after a real proof run.

### Follow-Up Validation Run

```powershell
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_private_local_v1_setup.py tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched #253 files
path-scoped secret/private-marker scan over touched #253 files
git status --short --branch --untracked-files=all
```

Results:

- focused setup tests -> passed, 8 passed;
- adjacent setup/launcher/local-app/migration tests -> passed, 70 passed,
  1 existing FastAPI/Starlette warning;
- Ruff over `src`, `tests`, and `tools` -> passed;
- direct helper `--check` smoke -> passed and left temp root absent;
- `git diff --check` -> passed, with only the Windows line-ending notice for
  the PowerShell wrapper;
- `py tools\check_agent_docs.py` -> passed;
- path-scoped protected-surface scan -> passed, forbidden 0, warnings 0;
- path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0;
- final git status showed only #253 report/handoff/helper/wrapper/test files
  modified.

### Follow-Up Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migration semantics,
analytics ingest semantics, workbook schema, webhook payload shape, Apps Script
behavior, Google Sheets behavior, output transport, production behavior,
OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or
truth ownership was changed.

### Follow-Up Generated/Private Artifact Status

No real GitHub clone, dependency install, backend/frontend process, browser
open, default `%LOCALAPPDATA%\MythicEdge\` setup, generated SQLite database,
raw log, private JSONL artifact, runtime artifact, or local-only artifact was
created or kept by this C validation pass. Tests used only pytest temp roots
and fake command/http/process hooks.

### Follow-Up Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_clean_checkout_install_launch.md

Updated Codex E report:
docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md

Goal:
Review the Codex C follow-up implementation that adds a contract-owned
private-local-v1 setup proof orchestration path. Lead with findings. Verify
that the implementation closes the manual-orchestration gap without overclaiming
live fresh-install readiness.

Review focus:
- Confirm `--check` remains a dry run and creates no v1 folders, database,
  manifest, or report.
- Confirm `--install` behavior remains non-destructive and blocks existing
  install state.
- Confirm new `--proof` / `-Proof` mode owns the sequence for clone/source
  selection, venv creation, Python dependency install, frontend dependency
  install, setup install, backend/frontend startup, loopback HTTP checks,
  optional browser open, and cleanup of only proof-started processes.
- Confirm unit tests use fake command/http/process hooks and do not clone
  GitHub, install dependencies, start real long-running processes, open a
  browser, or use real `%LOCALAPPDATA%\MythicEdge`.
- Confirm fake clone mode can populate `<install_root>\app` and setup mode does
  not misclassify that managed app checkout as an unrelated existing install.
- Confirm generated proof output uses symbolic/redacted paths and excludes raw
  command output, raw logs, raw paths, secrets, environment values, stack
  traces, raw SQL, private JSONL payloads, Player.log contents, AI provider
  keys, and external sends.
- Confirm no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior changed.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched #253 files
path-scoped secret/private-marker scan over touched #253 files

Optional live proof, only if explicitly approved and disposable:
- Run the new `--proof` flow against a controlled disposable install root.
- If live proof is run, do not use real default `%LOCALAPPDATA%\MythicEdge`
  unless the user explicitly approves.
- Stop only proof-started processes unless the user explicitly asks to leave
  them running.

Do not:
- Delete, overwrite, move, reset, retire, or uninstall the user's current
  Mythic Edge folder.
- Inspect raw Player.log contents or private app-data.
- Keep generated/private/local artifacts in the repo.
- Implement AI runtime or model-provider behavior.
- Change parser/runtime/analytics schema/migrations/ingest semantics, workbook,
  transport, production, or AI truth.
- Stage, commit, push, open a PR, merge, close issue #253, or close tracker
  #136 unless explicitly asked.

Final review report must include:
- role performed
- issue/tracker reviewed
- contract, report, and handoff reviewed
- findings first, ordered by severity
- validation run and result
- proof-orchestration readiness verdict
- generated/private artifact status
- protected-surface status
- secret/private-marker status
- whether forbidden scope was touched
- whether #253 should route to Codex D, Codex B, Codex F, or another Codex E
  live proof pass
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md and updated Codex E readiness report"
  target_artifact: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> passed, 8 passed"
    - "adjacent setup/launcher/local-app/migration tests -> passed, 70 passed, 1 existing FastAPI/Starlette warning"
    - "py -m ruff check src tests tools -> passed"
    - "private_local_v1_setup.py --check smoke -> passed, temp root absent"
    - "git diff --check -> passed, Windows line-ending notice only"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  remaining_unverified:
    - "Live GitHub clone through --proof"
    - "Real virtualenv and dependency installs through --proof"
    - "Real backend/frontend startup through --proof"
    - "Real browser-open/rendered status-panel smoke"
    - "Real default %LOCALAPPDATA%\\MythicEdge readiness"
    - "Git cleanliness after a real proof run"
  stop_conditions:
    - "Do not delete, overwrite, move, reset, retire, or uninstall the user's current Mythic Edge folder."
    - "Do not inspect raw Player.log contents or private app-data."
    - "Do not keep generated/private/local artifacts in the repo."
    - "Do not implement AI runtime or model-provider behavior."
    - "Do not change parser/runtime/analytics schema/migrations/ingest semantics, workbook, transport, production, or AI truth."
    - "Do not target main or close tracker #136."
```

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/253

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/private_local_v1_clean_checkout_install_launch.md`

## Internal Project Area

Quality / Governance release readiness, with supporting Local App / UI,
Generated / Local Artifacts, and Analytics setup surfaces.

## Truth Owner

The setup foundation owns install and launch readiness evidence only. Parser
truth, analytics fact truth, workbook truth, Match Journal truth, AI truth, and
production truth remain unchanged.

## Bridge-Code Status

`shared_support`

Allowed flow implemented:

```text
controlled source checkout + user/test selected install root
  -> v1 setup foundation
  -> generated folder tree, install manifest, setup report, optional empty SQLite init
```

## Role Performed

Codex C: Module Implementer / comparison thread

## What The Contract Is Supposed To Prove

The private-local-v1 path is supposed to prove that Mythic Edge can be installed
and launched from a clean checkout or explicitly controlled clean local setup
without relying on hidden local clutter. It eventually needs dependency install
evidence, generated folder policy, an install manifest, setup diagnostics,
empty migrated analytics SQLite initialization, backend/frontend/browser/status
proof, and generated-artifact safety evidence.

## Current Behavior Compared To Contract

Current repo behavior before this pass:

- The developer launcher could run preflight and start backend/frontend from an
  existing checkout using `%LOCALAPPDATA%\MythicEdgeDev\`.
- Local app path/status code understood the developer app-data root and
  analytics database status.
- The analytics migration loader could apply source-controlled migrations to a
  caller-supplied SQLite connection.
- No private-local-v1 setup wizard existed.
- No `%LOCALAPPDATA%\MythicEdge\app` / `%LOCALAPPDATA%\MythicEdge\data`
  release-profile folder policy existed in code.
- No v1 install manifest or setup diagnostic report existed.
- No Git-checkout app-data refusal helper existed.
- No setup flow created reserved `ai_review` folders.
- No setup flow initialized a fresh empty analytics SQLite database for v1.

## Implementation Option Chosen

Implemented the smallest safe setup-wizard foundation:

- no repository cloning;
- no real dependency installation;
- no process startup;
- no browser opening;
- no cleanup/reset/delete behavior;
- no default developer launcher root change;
- SQLite initialization only when explicitly requested and only inside the
  caller-supplied install root, covered by temp-root tests.

Clone-from-GitHub, virtualenv creation, `pip install`, `npm ci`, backend/frontend
startup proof, browser smoke, existing-install backup/reset choices, and final
contract-test report remain future work.

## Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`

Untracked contract from Codex B:

- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`

## Exact Code/Test/Doc Sections Changed

### Setup Helper

Added `tools/dev_app/private_local_v1_setup.py` with:

- v1 schema/object constants;
- `%LOCALAPPDATA%\MythicEdge\` default install-root policy;
- `build_private_local_v1_paths(...)`;
- `validate_app_data_root(...)`;
- `nearest_git_metadata_root(...)`;
- `create_v1_folder_tree(...)`;
- `initialize_analytics_sqlite(...)`;
- `run_private_local_v1_setup(...)`;
- sanitized install manifest and setup report builders;
- `--check`, `--install`, `--existing-checkout`, `--source-checkout`,
  `--install-root`, `--initialize-sqlite`, and `--json-report` CLI flags.

The helper outputs symbolic display paths such as `<install_root>\data` instead
of raw local paths.

### PowerShell Wrapper

Added `tools/dev_app/setup_private_local_v1.ps1` as a thin Windows-first wrapper
around the Python helper. The wrapper does not run `git clone`, `pip install`,
`npm ci`, cleanup, delete, or process-launch commands.

### Tests

Added `tests/test_private_local_v1_setup.py` covering:

- check mode is a dry run and does not create folders or databases;
- app-data roots inside a Git checkout are blocked without creating data;
- install mode creates the v1 generated folder tree, reserved `ai_review`
  folders, manifest, report, and empty migrated analytics database in a temp
  install root;
- migrated database contains zero parser fact rows in `matches` and `games`;
- manifest/report do not include raw install-root paths;
- PowerShell wrapper remains thin and non-destructive.

### Handoff

Added this comparison handoff and Codex E prompt.

## Code Changed

Yes. Repo-owned local setup tooling was added under `tools/dev_app/`.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest
semantics, local app runtime behavior outside setup flow, workbook schema,
webhook payload shape, Apps Script behavior, Google Sheets behavior, output
transport, production behavior, OpenAI/model-provider behavior, AI/coaching
behavior, Line Tracer, hidden-card inference, archetype inference,
player-mistake labels, or gameplay advice changed.

## Tests Added Or Updated

- Added `tests/test_private_local_v1_setup.py`.

## Interface Changes

Added source-controlled setup command:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1
```

Added Python helper command:

```powershell
py tools\dev_app\private_local_v1_setup.py --check --json-report
py tools\dev_app\private_local_v1_setup.py --install --existing-checkout --install-root <path> --initialize-sqlite
```

No environment-variable contract changed. No SQLite schema changed. No existing
developer launcher default changed.

## Contracted Area Status

The implementation stayed within setup tooling, generated/local artifact policy,
and analytics SQLite initialization through existing migrations. It did not
touch downstream parser/runtime/workbook/webhook/App Script/Sheets/AI/production
surfaces.

## Generated/Private Artifact Status

No real `%LOCALAPPDATA%\MythicEdge\` folders, real SQLite databases, local logs,
runtime artifacts, private JSONL files, Player.log files, workbook exports, or
secrets were created by implementation validation. Tests created only temporary
pytest folders and temporary SQLite files under `tmp_path`.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check tools tests
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched files
path-scoped secret/private-marker scan over touched files
direct trailing-whitespace, final-newline, and ASCII checks for new files
```

Results:

- `py -m pytest -q tests\test_private_local_v1_setup.py` -> passed, 4 passed.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> passed, 62 passed, 1 existing FastAPI/Starlette warning.
- `py -m ruff check tools tests` -> passed after wrapping one test assertion.
- `py -m ruff check src tests tools` -> passed.
- `py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report`
  -> passed; report status `passed`, no dependency install, SQLite init, process
  start, or browser open.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over the 5 touched files -> passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the 5 touched files -> passed,
  forbidden 0, warnings 0.
- Direct trailing-whitespace, final-newline, and ASCII checks for new files ->
  passed.

## Still Unverified

- Clone-from-GitHub clean install.
- Python virtualenv creation.
- Python dependency installation from `pyproject.toml`.
- Frontend dependency installation with `npm ci`.
- Backend/frontend startup from the v1 setup helper.
- Browser open and frontend status-panel smoke.
- Real default `%LOCALAPPDATA%\MythicEdge\` readiness.
- Existing-install choice handling beyond safe block/defer semantics.
- Final `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`.
- Production behavior, live workbook state, deployed Apps Script state, Google
  Sheets behavior, AI/model-provider behavior.

## Reviewer Focus

Codex E should pay special attention to:

- whether the setup helper is truly non-destructive by default;
- whether `--check` is a dry run;
- whether install mode writes only under the caller-selected install root;
- whether app-data roots inside Git checkouts are refused;
- whether manifest/report output avoids raw private paths, raw SQL, secrets,
  environment values, and stack traces;
- whether SQLite initialization uses only existing migrations and inserts no
  parser facts;
- whether the PowerShell wrapper remains thin and does not clone, install,
  launch, delete, or reset anything;
- whether clone/install/launch proof is correctly left unverified rather than
  overclaimed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_clean_checkout_install_launch.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md

Goal:
Review the Codex C private-local-v1 setup foundation against the contract. Lead with findings. Verify that the helper and wrapper remain local, non-destructive, path-redacted, test-root safe, and do not overclaim full clean-checkout install/launch readiness.

Review focus:
- Confirm `--check` is a dry run and creates no v1 folders, database, manifest, or report.
- Confirm install mode writes only under a caller-selected install root.
- Confirm app-data roots inside Git checkouts are blocked.
- Confirm the setup helper does not clone repositories, install dependencies, start backend/frontend processes, open a browser, delete/reset/move local folders, or touch real `%LOCALAPPDATA%\MythicEdge\` during tests.
- Confirm the manifest/report include symbolic paths only and no raw paths, raw logs, private JSONL payloads, raw SQL, stack traces, secrets, environment values, or AI provider keys.
- Confirm SQLite initialization applies existing analytics migrations only and inserts no parser fact rows.
- Confirm reserved `ai_review` folders are storage placeholders only and do not enable AI runtime/model-provider behavior.
- Confirm parser/runtime/analytics schema/migrations/ingest semantics/local app runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior were not changed.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check tools tests
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation

Do not:
- Clone repositories, install dependencies, initialize real local SQLite databases, start long-running processes, or open a browser.
- Delete, overwrite, move, reset, or uninstall local Mythic Edge folders.
- Ask for, store, print, or modify secrets/API keys/LLM provider keys.
- Create or commit generated/private/local artifacts.
- Implement AI runtime or model-provider behavior.
- Change parser, analytics schema/migrations/ingest semantics, local app runtime behavior outside setup flow, workbook/transport, production, or AI truth.
- Stage, commit, push, open a PR, merge, close issue #253, or close tracker #136 unless explicitly asked.

Final review report must include:
- role performed
- issue/tracker reviewed
- contract and handoff reviewed
- findings first, ordered by severity
- validation run and result
- generated/private artifact status
- protected-surface status
- secret/private-marker status
- whether forbidden scope was touched
- whether #253 should route to Codex D, Codex B, or Codex F
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> passed, 4 passed"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py tests\\test_analytics_migration_loader.py -> passed, 62 passed, 1 existing warning"
    - "py -m ruff check tools tests -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\dev_app\\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0"
    - "direct trailing-whitespace/final-newline/ASCII checks for new files -> passed"
  stop_conditions:
    - "Do not clone repositories, install dependencies, initialize real local SQLite databases, start long-running processes, or open a browser."
    - "Do not delete, overwrite, move, reset, or uninstall local Mythic Edge folders."
    - "Do not ask for, store, print, or modify secrets/API keys/LLM provider keys."
    - "Do not create or commit generated/private/local artifacts."
    - "Do not implement AI runtime or model-provider behavior."
    - "Do not change parser, analytics schema/migrations/ingest semantics, local app runtime behavior outside setup flow, workbook/transport, production, or AI truth."
    - "Do not target main or close tracker #136."
```
