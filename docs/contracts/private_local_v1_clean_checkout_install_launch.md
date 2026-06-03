# Private Local V1 Clean Checkout Install And Launch Contract

## Module

`private_local_v1_clean_checkout_install_launch`

This contract defines the private-local-v1 clean checkout install and launch
path for Mythic Edge.

Plain English: this is the "can I get Mythic Edge running from a fresh,
controlled install without relying on hidden local clutter?" contract. It
defines a future Windows CLI setup wizard, generated folder policy, install
manifest, setup diagnostics, SQLite initialization, dependency policy, and
launch proof. This contract does not implement the setup wizard.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/253
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source baseline issue: https://github.com/Tahjali11/Mythic-Edge/issues/249
- Source framework issue: https://github.com/Tahjali11/Mythic-Edge/issues/248
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/251
- Codex A problem representation:
  https://github.com/Tahjali11/Mythic-Edge/issues/253#issuecomment-4608622032

Expected later report:

- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

This contract must not target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue #253 and Codex A problem representation
- GitHub issue #251 and completion comment
- GitHub issue #249 and completion comment
- GitHub tracker #136
- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/contracts/local_artifact_manifest_environment_profiles.md`
- `docs/contracts/pre_v1_clean_install_transition.md`
- `docs/local_artifacts_manifest.json`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tools/check_local_environment.py`
- `Start Mythic Edge Dev App.cmd`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/`
- `pyproject.toml`
- `frontend/package.json`
- `frontend/package-lock.json`
- focused launcher, local app, config, migration, and frontend tests

## Risk Tier

High.

Reasons:

- this issue is release-blocking for `private_local_v1`;
- setup work may clone a repo, install dependencies, create a virtual
  environment, run `npm ci`, initialize SQLite, create generated folders, start
  backend/frontend processes, and open a browser;
- existing install handling can destroy or overwrite private local data if
  implemented carelessly;
- dependency installation can modify machine state;
- setup diagnostics can leak private paths, environment values, stack traces,
  secrets, or generated artifact contents if not redacted;
- the requested `ai_review` folder tree sits near future AI behavior and must
  remain reserved-only.

## Owning Layer

Primary owning layer: Quality / Governance release readiness.

Supporting areas:

- Local App / UI setup and launcher;
- Generated / Local Artifacts;
- Analytics SQLite initialization;
- Installability and operational portability.

## Internal Project Area

Quality / Governance.

Supporting internal project areas:

- Local App / UI;
- Generated / Local Artifacts;
- Analytics;
- Future AI Integration, reserved vocabulary only.

Naming Future AI Integration here does not authorize OpenAI runtime behavior,
model-provider integration, AI coaching evaluation, AI-owned parser truth,
AI-owned analytics truth, hidden-card truth, gameplay correctness truth, or
strategic certainty.

## Truth Owner

This setup flow owns install and launch readiness evidence only.

Truth ownership remains unchanged:

- Git owns tracked repository source state.
- Parser/state owns MTGA event interpretation, match/game identity,
  deduplication, final reconciliation, and parser-managed facts.
- Analytics migrations own SQLite schema migration history and local storage
  shape.
- SQLite owns local queryable storage of parser-normalized facts, not parser
  truth.
- The local app owns local orchestration, setup/status display, and safe
  browser-facing state.
- The setup wizard owns local setup orchestration and diagnostic reporting.
- Future AI folders are local/private generated storage placeholders only.

The setup wizard, install manifest, setup report, local app status payloads,
SQLite database, and browser UI must not become parser truth, analytics truth,
workbook truth, Match Journal truth, AI truth, production truth, or deployment
truth.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
repo/release reference + local toolchain metadata + user-approved install root
  -> local setup wizard
  -> app checkout, generated data folders, install manifest, setup report
  -> local app startup/status proof
  -> contract-test report
```

Forbidden reverse flow:

- setup output must not alter parser behavior;
- setup output must not alter analytics schema or ingest semantics;
- setup output must not alter workbook, webhook, Apps Script, Google Sheets,
  production, OpenAI/model-provider, AI/coaching, or Line Tracer behavior;
- setup output must not decide match/game/card truth;
- setup output must not authorize cleanup or deletion without explicit human
  selection and contract-scoped behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`

Expected later report:

- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`

Future Codex C implementation may propose or add:

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- focused tests such as `tests/test_private_local_v1_setup.py`
- focused launcher/local app setup tests when needed
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`

Codex C may choose different file names only if the comparison explains why the
repo's existing naming pattern is better. The implementation must remain under
repo-owned tooling, not under generated app-data folders.

Reference-only files:

- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `Start Mythic Edge Dev App.cmd`
- `tools/check_local_environment.py`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/local_app/`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `frontend/`
- `.gitignore`
- `pyproject.toml`

Codex C must route back to Codex B before changing parser behavior, analytics
schema or migration semantics, local app runtime behavior outside setup flow,
workbook/webhook/App Script/Sheets behavior, AI/model-provider behavior,
credential policy, CI gates, or Pyright gate behavior.

## Observed Current Behavior

### Baseline And Issue State

- The engineering maturity baseline scored `Installability and operational
  portability` as `3`.
- The target score for `private_local_v1` is `4`.
- The row is a `private_local_v1` blocker until clean checkout install/launch
  proof exists.
- Issue #251 completed disposable-root local app startup/status smoke and
  merged PR #254 into `codex/analytics-foundation`.
- The #251 smoke passed as `degraded_acceptable`, but actual default app-data
  root readiness and clean-checkout install/launch proof remain unverified.
- Issue #253 is open and owns the clean checkout install/launch proof.

### Existing Developer Launcher

Observed existing launcher behavior:

- `tools/dev_app/start_mythic_edge_dev_app.ps1` supports `-Check`, `-Start`,
  `-NoOpen`, `-LogToConsole`, `-BackendPort`, `-FrontendPort`, and
  `-AppDataRoot`.
- `tools/dev_app/dev_app_launcher.py` can run preflight, start backend and
  frontend child processes, create developer app subfolders, redact repo and
  app-data paths in logs, and clean up children it started.
- The developer launcher currently defaults to
  `%LOCALAPPDATA%\MythicEdgeDev\`.
- `src/mythic_edge_parser/local_app/paths.py` also defaults local app data to
  `%LOCALAPPDATA%\MythicEdgeDev\` unless
  `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` is provided.
- Current required app subfolders are `config`, `db`, `logs`, `imports`,
  `jobs`, and `diagnostics`.
- Current launcher tests assert that start mode creates only app subdirectories
  and launcher logs, not analytics or Match Journal SQLite files.

Observed gap:

- no v1 setup wizard exists;
- no clone-from-GitHub workflow exists;
- no `%LOCALAPPDATA%\MythicEdge\` release-profile install root exists;
- no install manifest exists;
- no setup diagnostic report exists;
- no v1 setup flow initializes an empty analytics SQLite database;
- no setup flow creates reserved `ai_review` folders;
- no setup flow refuses app-data roots inside Git checkouts;
- no clean-checkout report proves install and launch from a controlled setup.

### Existing Dependency And Migration Inputs

- `pyproject.toml` requires Python `>=3.11`.
- `pyproject.toml` defines optional `app` dependencies including FastAPI,
  Uvicorn, and Python multipart support.
- `pyproject.toml` defines `dev` dependencies including Pytest, Ruff, Pyright,
  FastAPI, HTTPX, Uvicorn, and Python multipart support.
- `frontend/package.json` requires Node `>=20`.
- `frontend/package-lock.json` exists and supports deterministic `npm ci`.
- `src/mythic_edge_parser/app/analytics_migration_loader.py` applies
  source-controlled SQL migrations to a caller-supplied SQLite connection.
- Analytics migration package data is configured in `pyproject.toml`.

### Existing Local Artifact Policy

- `docs/local_artifacts_manifest.json` defines profile vocabulary including
  `clean_clone`, `local_developer_app`, `analytics_development`,
  `live_parser_readiness`, `historical_import_readiness`, and
  `clean_install_transition_audit`.
- `tools/check_local_environment.py` reports local artifact readiness without
  reading private payloads.
- `.gitignore` ignores repo-local generated data roots, frontend dependency and
  build folders, caches, and local review folders.
- Existing local artifact policy does not yet define the
  `%LOCALAPPDATA%\MythicEdge\app` and `%LOCALAPPDATA%\MythicEdge\data` v1
  setup structure.

## Contract Decision

Issue #253 should own the full private-local-v1 install target, but
implementation should be allowed to land in controlled phases.

Required final #253 proof:

- begin from a clean checkout or explicitly controlled clean local setup;
- install Python and frontend dependencies through approved commands;
- initialize a generated local app data root;
- create an empty migrated analytics SQLite database;
- start backend and frontend;
- open or verify the local browser URL;
- verify local status panels;
- prove generated/private/local artifacts remain out of Git;
- produce a durable report.

Recommended implementation phases:

1. `setup_foundation_existing_checkout`
   - add the v1 setup wizard foundation using the current checkout as the
     source;
   - create the v1 install/data folder policy;
   - refuse unsafe app-data roots;
   - create manifest and setup report;
   - initialize analytics SQLite with migrations;
   - launch backend/frontend through existing launcher-compatible commands;
   - verify local status surfaces.
2. `clone_from_github_clean_install`
   - clone the repo into the v1 app checkout root;
   - select a future v1.0 branch or tag when one exists;
   - create the virtual environment in the cloned checkout;
   - install dependencies from source-controlled manifests;
   - run the phase-1 proof from the cloned checkout.

The final issue #253 report may only claim complete satisfaction after either:

- the full clone-from-GitHub path is implemented and proven; or
- the report explicitly states that an "explicitly controlled clean local
  setup" was used, explains why that is accepted for `private_local_v1`, and
  records clone-from-GitHub as deferred follow-up.

## Fresh-Install Target Behavior

The private-local-v1 setup target should:

1. verify Windows local setup context;
2. detect Git, Python, Node.js, and npm;
3. clone Mythic Edge from GitHub or validate a controlled source checkout;
4. select the future v1.0 release branch or tag by default when available;
5. create a per-project Python virtual environment;
6. install Python dependencies from `pyproject.toml`;
7. install frontend dependencies with `npm ci`;
8. create the v1 generated data folder structure;
9. create an install manifest;
10. create a setup diagnostic report;
11. initialize an empty analytics SQLite database and apply migrations;
12. treat a fresh empty migrated analytics database as healthy;
13. start backend and frontend on loopback ports;
14. open the browser or record browser-open failure as a setup warning;
15. verify status panels or local backend/frontend readiness;
16. leave the app running when the user selected normal setup mode;
17. confirm generated/private/local artifacts are not tracked by Git.

## Setup Wizard Responsibilities

The future setup wizard owns:

- release-profile install root selection;
- Git checkout or controlled source-checkout validation;
- app-data root validation;
- toolchain detection;
- dependency installation orchestration;
- virtualenv creation;
- generated folder creation;
- install manifest creation;
- setup diagnostic report creation;
- analytics SQLite initialization through existing migration loader;
- backend/frontend startup orchestration through existing launcher-compatible
  behavior;
- browser-open attempt and status verification;
- cleanup of only processes it started when run in test/proof mode.

The setup wizard must not own:

- parser runtime behavior;
- live Player.log watching;
- manual JSONL import;
- Match Journal writes;
- analytics ingest from real data;
- workbook, webhook, Apps Script, or Google Sheets transport;
- OpenAI/model-provider runtime behavior;
- production deployment;
- credential creation, rotation, or storage.

## Existing Developer Launcher Responsibilities

The existing developer launcher remains a developer convenience surface.

It continues to own:

- existing-checkout preflight;
- backend/frontend launch from a known checkout;
- loopback host and port handling;
- path-redacted launcher logs;
- `%LOCALAPPDATA%\MythicEdgeDev\` compatibility.

The future v1 setup wizard may reuse launcher helpers or route through the
PowerShell wrapper, but it must not silently change the developer launcher's
current default root from `MythicEdgeDev` to `MythicEdge`.

Compatibility rule:

- `MythicEdgeDev` remains the current developer profile root.
- `%LOCALAPPDATA%\MythicEdge\` is the private-local-v1 install profile root.
- If the setup wizard launches the local app from the v1 root, it must pass the
  v1 data root explicitly through `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` or an
  equivalent contract-owned parameter.
- Changing the default in `src/mythic_edge_parser/local_app/paths.py` or
  `tools/dev_app/dev_app_launcher.py` requires a compatibility comparison and
  must preserve existing developer workflow unless a later contract authorizes
  migration.

## Generated Folder Contract

Default v1 root:

```text
%LOCALAPPDATA%\MythicEdge\
```

Required default structure:

```text
%LOCALAPPDATA%\MythicEdge\
  app\
  data\
    config\
    db\
    logs\
    imports\
    jobs\
    diagnostics\
    exports\
    ai_review\
      sources\
      packets\
      reports\
```

Meaning:

- `app\`: cloned or controlled Mythic Edge checkout.
- `data\`: generated app-owned state.
- `data\config\`: local app config and install manifest.
- `data\db\`: analytics and future app-owned SQLite databases.
- `data\logs\`: setup, launcher, backend, frontend, and diagnostic logs.
- `data\imports\`: future user-selected import staging or job metadata.
- `data\jobs\`: job and process state.
- `data\diagnostics\`: setup and local diagnostic reports.
- `data\exports\`: future user-requested safe exports.
- `data\ai_review\`: reserved future AI review storage only.

Optional on-demand backup root:

```text
%LOCALAPPDATA%\MythicEdge\backups\
```

The backup root should not be created unless the user explicitly chooses a
backup/reset option in a later implementation.

## Install Root And App-Data Root Policy

The setup wizard must separate source checkout from generated data:

- checkout root: `%LOCALAPPDATA%\MythicEdge\app\`
- generated app-data root: `%LOCALAPPDATA%\MythicEdge\data\`

The app-data root may not be:

- a Git checkout root;
- any folder inside any Git checkout;
- the current working repo root;
- `frontend\`, `src\`, `tests\`, or any source-controlled repo subfolder;
- a raw Player.log folder;
- a folder containing secrets or private artifacts selected only because the
  user mistyped a path.

The setup wizard may create missing v1 folders after user confirmation or in a
noninteractive mode explicitly scoped for tests. It must not delete or overwrite
existing folders silently.

## Git-Checkout Refusal Policy

The setup wizard must refuse to use any Git checkout or descendant of a Git
checkout as an app-data folder.

Required checks:

- run a metadata-only Git worktree/root check for existing paths;
- inspect parent folders for `.git` metadata when the candidate folder does
  not yet exist;
- treat uncertain Git metadata as blocked until the user chooses a safer path;
- report only symbolic or redacted paths in setup output.

Required user-facing message shape:

```text
Mythic Edge cannot use a Git checkout folder, or any folder inside a Git checkout, as its app-data folder.
Please choose a folder outside the repo. Recommended: %LOCALAPPDATA%\MythicEdge\data\
```

No advanced override is approved for `private_local_v1`.

## Existing Install Handling Policy

When an existing `%LOCALAPPDATA%\MythicEdge\` install is detected, the setup
wizard must stop and ask the user to choose one of:

1. use existing data and continue;
2. back up existing data, then reset;
3. choose a different folder;
4. cancel setup.

Required guarantees:

- no silent overwrite;
- no silent deletion;
- no duplicate database creation inside the same app-data root;
- no migration of `MythicEdgeDev` data into `MythicEdge` unless a later
  compatibility contract authorizes it;
- no inspection of private payload contents;
- no printing raw private paths beyond approved redacted/symbolic labels.

Backup/reset behavior is high-risk. If implemented in the first Codex C pass,
it must be user-confirmed, non-destructive, and test-covered with temporary
directories only. If not implemented in the first pass, the setup wizard must
report existing installs as blocked/deferred with safe instructions.

## Dependency, Virtualenv, And Npm Policy

### Tool Detection

The setup wizard must detect:

- Git;
- Python launcher or Python executable;
- Python version compatible with `pyproject.toml`;
- Node.js version compatible with `frontend/package.json`;
- npm;
- `frontend/package-lock.json`.

Missing required tools must be reported as blockers, not silently skipped.

### System Dependency Installation

Executing system-level dependency installation, including `winget`, is deferred
by default.

Allowed in this contract:

- detect missing Python/Node/npm/Git;
- show user-approved prompt text;
- produce remediation instructions;
- optionally implement a dry-run or explicit confirmation branch that records
  what would be installed.

Not allowed without a later explicit user approval or scoped implementation
contract:

- silently run `winget`;
- install or modify system-level Python, Node.js, npm, Git, PATH, shell
  profiles, registry entries, or machine-wide settings.

### Python Virtual Environment

Required v1 virtualenv location:

```text
%LOCALAPPDATA%\MythicEdge\app\.venv\
```

Required Python install command shape:

```powershell
<venv_python> -m pip install -e ".[dev,app]"
```

The exact command may be split into pip upgrade/install steps if Codex C proves
that is more reliable, but it must still install from `pyproject.toml` and keep
dependencies inside the per-project virtualenv.

### Frontend Dependencies

Required frontend install command:

```powershell
npm --prefix frontend ci
```

`npm install` is not the release setup path because it can update dependency
state instead of reproducing `frontend/package-lock.json`.

## Manifest Schema Expectations

The setup wizard must write a generated install manifest under:

```text
%LOCALAPPDATA%\MythicEdge\data\config\install_manifest.json
```

Required fields:

- `object = "mythic_edge_private_local_v1_install_manifest"`
- `schema_version = "private_local_v1_clean_checkout_install_launch.v1"`
- `install_id`
- `install_created_at`
- `setup_flow_version`
- `release_ref_type`: `branch`, `tag`, `commit`, or `controlled_checkout`
- `release_ref`
- `repo_url`
- `checkout_display_path`
- `app_data_display_path`
- `config_display_path`
- `analytics_database_display_path`
- `backend_host`
- `backend_port`
- `frontend_host`
- `frontend_port`
- `created_folder_keys`
- `python`: object with executable kind, version, virtualenv display path, and
  install status
- `node`: object with Node/npm versions and install status
- `git`: object with checkout status and release ref status
- `migrations`: object with analytics schema status and applied migration IDs
- `privacy`: object with booleans proving raw paths, raw logs, private JSONL
  payloads, secrets, environment values, and AI provider keys were not read or
  printed
- `warnings`
- `errors`

The manifest may include symbolic display paths. It must not include raw full
private paths, raw command logs, raw stack traces, raw SQL, secrets, environment
values, or private artifact contents.

## Setup Diagnostic Report Expectations

The setup wizard must write a generated diagnostic report under:

```text
%LOCALAPPDATA%\MythicEdge\data\diagnostics\setup_report.json
```

Required fields:

- `object = "mythic_edge_private_local_v1_setup_report"`
- `schema_version = "private_local_v1_clean_checkout_install_launch.v1"`
- `status`: `passed`, `degraded`, `blocked`, or `failed`
- `duration_seconds`
- `toolchain`
- `dependency_install`
- `folder_creation`
- `git_checkout`
- `existing_install_handling`
- `sqlite_initialization`
- `migration_status`
- `backend_startup`
- `frontend_startup`
- `browser_open`
- `status_panel_verification`
- `git_artifact_safety`
- `privacy`
- `warnings`
- `errors`
- `next_steps`

The report is a diagnostic support artifact, not a user-facing parser truth
source. It must stay generated/local/private and must not be committed.

## SQLite Initialization And Migration Policy

The setup wizard should initialize this analytics database:

```text
%LOCALAPPDATA%\MythicEdge\data\db\mythic_edge.sqlite3
```

Required behavior:

- create the database only inside the approved v1 app-data root;
- apply repo-owned analytics migrations through
  `analytics_migration_loader.apply_analytics_migrations(...)`;
- treat a fresh empty migrated analytics database as healthy;
- record applied migration IDs in the install manifest and setup report;
- avoid raw SQL dumps in output;
- avoid inserting parser facts, generated fixture rows, manual import data, or
  live Player.log facts during setup.

Match Journal database initialization is not required for #253. A missing
Match Journal database may remain `not_initialized` if the status surface
explains that safely. Initializing Match Journal SQLite eagerly requires a
separate comparison against Match Journal contracts.

## Backend, Frontend, Browser, And Status Verification Policy

After setup, the wizard or proof harness must verify:

- backend starts on a loopback host;
- frontend starts on a loopback host;
- browser opens to the frontend or browser-open failure is recorded as
  degraded with remediation;
- `GET /api/health` returns safe JSON;
- `GET /api/app/setup-status` returns safe setup status;
- `GET /api/analytics/database/status` reports the new analytics database as
  healthy/current;
- live Player.log status remains metadata-only;
- watcher process/start/stop controls remain disabled unless a later contract
  authorizes them;
- frontend renders the setup/status panel;
- no destructive controls, arbitrary SQL, production transport, or AI/coaching
  controls are exposed.

The setup proof may reuse the #251 startup/status smoke checks after replacing
the disposable app-data root with the v1 app-data root.

## AI Review Reserved-Folder Policy

The setup wizard should create:

```text
%LOCALAPPDATA%\MythicEdge\data\ai_review\sources\
%LOCALAPPDATA%\MythicEdge\data\ai_review\packets\
%LOCALAPPDATA%\MythicEdge\data\ai_review\reports\
```

Private-local-v1 rules:

- folders are empty/reserved;
- no AI runtime behavior;
- no OpenAI/model-provider integration;
- no LLM API keys;
- no external sends;
- no AI coaching output;
- no direct filesystem access for future AI;
- no AI-owned parser truth, analytics truth, hidden-card truth, gameplay
  correctness truth, player-mistake truth, or strategic certainty;
- all files under `ai_review\` are local/private/generated and must remain out
  of Git.

Future AI should consume curated review packets and approved source docs only,
under a separate issue and contract.

## Generated And Private Artifact Policy

The setup wizard may create local generated artifacts only under the approved
v1 root or ignored dependency/build locations:

- `%LOCALAPPDATA%\MythicEdge\app\`
- `%LOCALAPPDATA%\MythicEdge\data\`
- `%LOCALAPPDATA%\MythicEdge\app\.venv\`
- `%LOCALAPPDATA%\MythicEdge\app\frontend\node_modules\`
- generated frontend build output, if produced by validation, removed or kept
  ignored according to current `.gitignore`;
- optional `%LOCALAPPDATA%\MythicEdge\backups\` only after explicit user
  selection.

The setup wizard must not commit or report contents from:

- raw Player.log files;
- private JSONL artifacts;
- generated SQLite database rows;
- WAL/SHM/journal files;
- runtime logs;
- setup logs;
- import/job artifacts;
- diagnostics contents beyond sanitized summaries;
- workbook exports;
- secrets, credentials, tokens, webhook URLs, spreadsheet IDs, API keys,
  environment values, or AI provider keys;
- local-only artifacts.

## Public Interface Contract

The future implementation should expose a Windows-first setup command. The
preferred source-controlled interface is:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1
```

Preferred modes:

- `-Check`: report readiness without cloning, installing, creating folders,
  initializing DB, or starting processes.
- `-Install`: perform user-approved setup.
- `-ExistingCheckout`: use the current checkout as source for a controlled
  first-phase proof.
- `-RepoUrl <url>`: clone source, defaulting to the Mythic Edge GitHub repo.
- `-ReleaseRef <branch-or-tag>`: select branch/tag/commit.
- `-InstallRoot <path>`: override `%LOCALAPPDATA%\MythicEdge\` for tests or
  explicit user selection.
- `-NoOpen`: do not open browser, but still verify URLs/status when possible.
- `-LeaveRunning`: leave backend/frontend running after setup.
- `-StopAfterVerify`: stop only setup-started processes after proof.
- `-JsonReport`: print sanitized report JSON.

The Python helper may expose equivalent CLI flags. All modes must use loopback
network hosts only.

## Inputs

Allowed inputs:

- repo URL, defaulting to the Mythic Edge GitHub repository;
- release ref, branch, tag, commit, or controlled-checkout marker;
- install root path selected by user or test harness;
- app-data root derived from install root;
- explicit existing-install choice;
- local toolchain metadata;
- source-controlled `pyproject.toml`;
- source-controlled `frontend/package-lock.json`;
- source-controlled analytics migration resources.

Forbidden inputs:

- raw Player.log contents;
- private JSONL payloads;
- raw workbook exports;
- webhook URLs;
- spreadsheet IDs;
- API keys, tokens, credentials, OAuth secrets, LLM provider keys;
- generated database contents as setup decisions;
- AI/model-provider responses.

## Outputs

Generated local outputs:

- app checkout under `%LOCALAPPDATA%\MythicEdge\app\`;
- v1 data root under `%LOCALAPPDATA%\MythicEdge\data\`;
- install manifest;
- setup diagnostic report;
- initialized empty analytics SQLite database;
- optional setup logs;
- reserved AI review folders;
- backend/frontend running processes, only when selected setup mode leaves them
  running.

Repo outputs for implementation:

- setup wizard source files;
- focused tests;
- implementation handoff;
- later contract-test report.

## Error Behavior

The setup wizard must:

- report missing Git/Python/Node/npm as blockers or explicit remediation steps;
- report incompatible Python or Node versions as blockers;
- refuse unsafe app-data roots;
- refuse silent overwrite/reset of existing installs;
- report port conflicts without killing unrelated processes;
- report dependency install failures with sanitized summaries;
- report migration failures with error codes, not raw SQL dumps;
- report browser-open failure as degraded when backend/frontend/status still
  pass;
- preserve generated diagnostics for troubleshooting without exposing private
  data;
- stop only processes it started when proof mode requests cleanup.

## Side Effects

Codex B side effects:

- create this contract only.

Future implementation side effects, if authorized:

- clone source into v1 app checkout root;
- create a virtual environment;
- install Python dependencies into the virtual environment;
- run `npm ci` under the app checkout frontend;
- create v1 generated data folders;
- write install manifest and setup report;
- create and migrate analytics SQLite database;
- start backend/frontend processes;
- open browser;
- leave app running or stop setup-started processes depending on selected mode.

Forbidden side effects:

- deleting, overwriting, moving, resetting, or uninstalling current local Mythic
  Edge folders without explicit user selection and tested behavior;
- modifying system PATH, shell profile, registry, Python, Node, npm, Git, or
  package managers without explicit user approval;
- reading/copying/sanitizing/importing raw private data;
- external sends;
- workbook/webhook/App Script/Sheets writes;
- production deployment;
- AI/model-provider calls.

## Dependency Order

Future implementation should proceed in this order:

1. Add setup wizard comparison and dry-run/check behavior.
2. Add v1 folder and Git-checkout refusal tests.
3. Add install manifest and setup-report schema tests.
4. Add analytics SQLite initialization through migration loader using temporary
   roots.
5. Add existing-checkout setup proof mode.
6. Add backend/frontend startup verification integration.
7. Add clone-from-GitHub support only after local proof mode is safe.
8. Add final #253 contract-test report.

## Compatibility

- Preserve `MythicEdgeDev` as the existing developer app profile.
- Preserve `tools/dev_app/start_mythic_edge_dev_app.ps1` behavior unless the
  implementation comparison proves a narrow backward-compatible update is
  required.
- Preserve `Start Mythic Edge Dev App.cmd` as the existing user-facing shortcut
  unless a future shortcut contract updates it.
- Preserve `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` override behavior.
- Preserve current analytics migration semantics.
- Preserve #251 startup/status smoke report as prerequisite evidence, not as
  clean-install proof.

## Validation Requirements

Codex C implementation validation should include:

```powershell
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
```

Later clean-install proof validation should include:

- fresh clone or controlled clean local setup evidence;
- Python virtualenv creation evidence;
- `pyproject.toml` dependency install evidence;
- `npm ci` evidence;
- v1 folder tree evidence with paths redacted;
- install manifest and setup report shape validation;
- empty migrated analytics SQLite health evidence;
- backend/frontend startup and browser/status evidence;
- git cleanliness and generated/private artifact exclusion evidence;
- explicit no-AI-runtime/no-external-send statement.

Codex B validation for this contract is docs-only:

```powershell
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/private_local_v1_clean_checkout_install_launch.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_clean_checkout_install_launch.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, or ingest semantics, except creating an empty
  database by applying existing migrations;
- local app/UI behavior outside the setup flow;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- CI gates;
- Pyright required/failing behavior;
- secrets, credentials, environment variable contracts, raw logs, generated
  data, runtime status files, failed posts, workbook exports, local JSONL
  artifacts, generated SQLite files, or local-only artifacts.

## Unknowns

- The future v1.0 release branch/tag does not appear to exist yet; controlled
  checkout mode may be necessary until v1.0 is cut.
- Whether the first Codex C pass should implement clone-from-GitHub behavior or
  only the existing-checkout setup foundation depends on risk and available
  implementation time.
- Whether system-level dependency installation through `winget` should ever be
  implemented is deferred.
- Whether Match Journal DB initialization should become part of setup is
  deferred.
- Whether #252 private-artifact scanner/env posture must finish before final
  #253 closure depends on tracker/release decision by Codex G.

## Suspected Gaps

- No setup wizard exists.
- No v1 `%LOCALAPPDATA%\MythicEdge\` folder policy exists in code.
- No v1 install manifest or setup report exists.
- No Git-checkout refusal helper exists for app-data roots.
- No setup flow creates reserved AI review folders.
- No setup flow initializes analytics SQLite for a fresh install.
- Existing launcher cleanup may need extra proof because #251 observed Vite
  child-process cleanup required targeted handling.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_local_v1_clean_checkout_install_launch.md`.
- Fresh-install target behavior is defined.
- Phase recommendation is defined.
- Setup wizard responsibilities are defined.
- Existing developer launcher responsibilities and compatibility boundaries are
  defined.
- Generated folder contract is defined.
- Install root and app-data root policy is defined.
- Git-checkout app-data refusal policy is defined.
- Existing install handling policy is defined.
- Dependency, virtualenv, and npm policy is defined.
- Manifest and setup report schema expectations are defined.
- SQLite initialization and migration policy is defined.
- Backend/frontend/browser/status verification policy is defined.
- AI review reserved-folder policy is defined.
- Generated/private artifact policy is defined.
- Protected surfaces and validation requirements are defined.
- No implementation behavior changes are made in Codex B.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Codex C should first compare current setup/launcher/local environment code to
this contract. It may then implement the smallest safe setup-wizard foundation
or route back if clone/install behavior is too broad for one implementation
slice.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_clean_checkout_install_launch.md

Goal:
Compare the current developer launcher, local app path/config/status code, local environment checker, analytics migration loader, pyproject/frontend dependency manifests, and tests against the private-local-v1 clean checkout install/launch contract. Produce docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md and implement only the smallest safe setup-wizard foundation if the comparison shows it is ready.

Before editing:
- confirm branch and git status;
- inspect issue #253, #251, #249, and tracker #136;
- state what the clean checkout install/launch path is supposed to prove, what current code already does, what gaps remain, and the exact minimal comparison/implementation plan.

Implementation boundaries:
- do not clone repositories during implementation unless using test-managed temporary fake repos;
- do not install dependencies on the real machine unless explicitly approved;
- do not initialize real local SQLite databases outside test temp roots;
- do not start long-running backend/frontend processes except in controlled tests;
- do not open the browser unless explicitly approved;
- do not delete, overwrite, move, reset, or uninstall current local Mythic Edge folders;
- do not ask for, store, print, or modify secrets, credentials, tokens, webhook URLs, spreadsheet IDs, API keys, environment values, or LLM provider keys;
- do not implement AI runtime behavior or model-provider integration;
- do not send data to any external service;
- do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.

Expected validation:
- focused setup wizard tests, if implemented;
- launcher/local app/migration focused tests;
- frontend typecheck/test when startup/status surface is affected;
- git diff --check;
- agent docs check;
- protected-surface scan;
- secret/private-marker scan.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #253 Codex A problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/private_local_v1_clean_checkout_install_launch.md"
    - "path-scoped secret/private-marker scan for docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not clone repositories, install dependencies, initialize real local SQLite databases, start long-running processes, or open a browser in Codex B."
    - "Do not delete, overwrite, move, reset, or uninstall local Mythic Edge folders."
    - "Do not ask for, store, print, or modify secrets/API keys/LLM provider keys."
    - "Do not create or commit generated/private/local artifacts."
    - "Do not implement AI runtime or model-provider behavior."
    - "Do not change parser, analytics schema/migrations/ingest semantics, local app runtime behavior outside setup flow, workbook/transport, production, or AI truth."
    - "Do not target main or close tracker #136."
```
