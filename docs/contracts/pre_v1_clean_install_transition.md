# Pre-v1 Clean-Install Transition Contract

## Module

Pre-v1 clean-install transition and local checkout retirement audit.

This contract defines how Mythic Edge may safely inspect the current
pre-release checkout, classify local/private/generated artifacts, verify what a
future clean install must prove, and prepare for a v1.0-ready local setup
without deleting, moving, archiving, cloning, copying, sanitizing, or modifying
local artifacts in this contract-writing thread.

Plain English: this is the "make sure the old folder is not secretly holding
the project together" contract. It is an audit and checklist surface, not a
cleanup button.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/227>
- Related completed issue: <https://github.com/Tahjali11/Mythic-Edge/issues/153>
- Related local app umbrella: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Related analytics usability tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>

Issue #153 is complete and closed. Its manifest/checker artifacts are required
inputs for this contract.

Issue #227 remains open. This contract does not close it and does not perform
retirement, cleanup, rename, clone, archive, migration, or deletion work.

## Tracker

N/A.

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Do not target `main`.

## Risk Tier

High.

Reasons:

- future workflow may touch local-only history, generated runtime files,
  private JSONL/log artifacts, SQLite databases, secrets, stashes, and
  uncommitted work;
- a bad cleanup plan could lose private historical data;
- a weak clean-install plan could hide dependency on local ignored clutter;
- live parser, local app, analytics, workbook, webhook, and AI boundaries are
  nearby and must not be crossed;
- actual rename/delete/archive/copy/clone steps need explicit user approval and
  a later scoped implementation or operator checklist.

## Owning Layer

Primary owner: Quality / Governance.

Supporting areas:

- Generated / Local Artifacts
- Local App / UI
- Analytics
- Parser runtime readiness, read-only only

## Internal Project Area

Quality / Governance.

This contract is `shared_support` for local install readiness. It does not own
parser truth, analytics truth, runtime truth, local app behavior, app-data
migration, GitHub lifecycle, deployment readiness, or credential policy.

## Truth Owner

Truth ownership remains unchanged:

- Git owns tracked repository source state.
- The #153 manifest and checker own report-only local artifact classification.
- `%LOCALAPPDATA%\MythicEdgeDev\` owns local app generated state.
- MTGA `Player.log` remains local observable evidence only.
- Parser/state owns parser interpretation and normalized facts.
- Analytics SQLite owns downstream local storage of parser-normalized facts,
  not parser truth.
- The pre-v1 audit owns only transition-readiness reporting and checklist
  vocabulary.

The audit must never decide that a local checkout is safe to delete. Only the
human can approve deletion, archival, clone replacement, or final retirement.

## Bridge-Code Status

`shared_support`.

Allowed data flow:

```text
repo metadata + #153 manifest/checker + safe local metadata
  -> pre-v1 transition audit report/checklist
  -> human decision about a later clean-install or retirement action
```

Forbidden reverse flow:

- audit findings must not write repo files except for explicitly reviewed docs
  or future tests/tooling under a Codex C implementation;
- audit findings must not modify app data, SQLite files, raw logs, JSONL
  artifacts, secrets, environment variables, Git stashes, remotes, branches, or
  ignored/generated folders;
- audit findings must not start parser runtime, run imports, post webhooks,
  update Google Sheets, deploy Apps Script, invoke model providers, or decide
  production readiness.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/pre_v1_clean_install_transition.md`

Reference artifacts from #153:

- `docs/contracts/local_artifact_manifest_environment_profiles.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md`
- `docs/contract_test_reports/local_artifact_manifest_environment_profiles.md`

Future Codex C implementation files authorized by this contract:

- `docs/local_artifacts_manifest.json`, only to add or adjust
  pre-v1-transition profile entries and the `.env.example` template policy;
- `tools/check_local_environment.py`, only to add report-only
  clean-install-transition metadata checks and `.env.example` handling;
- `tests/test_check_local_environment.py`, only for focused regression coverage;
- optional `tests/test_pre_v1_clean_install_transition.py`, only if separating
  the new audit tests makes review clearer;
- `docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md`.

Referenced but not owned:

- `.gitignore`
- `README.md`
- `pyproject.toml`
- `docs/project_roadmap.md`
- `tools/dev_app/`
- `src/mythic_edge_parser/local_app/`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- current local app setup/status/config/import tests

Not owned:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest, or deterministic view behavior;
- local app backend/frontend behavior except report-only checker integration if
  explicitly implemented;
- launcher start behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- Line Tracer or coaching behavior;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment-variable contracts;
- raw logs, private JSONL artifacts, generated SQLite databases, WAL/SHM/
  journal files, runtime status files, failed posts, workbook exports, frontend
  build output, dependency caches, stashes, or local-only artifacts.

## Observed Current Behavior

Issue and branch state:

- Issue #227 is open and asks for pre-v1 clean-install transition and local
  checkout retirement semantics.
- Issue #153 is closed as completed on `codex/analytics-foundation` with direct
  integration commit `2d95827615bbc7659fecc45d3748d5bb2f0b83ff`.
- The #153 package added a source-controlled local artifact manifest, a
  report-only local environment checker, focused tests, an implementation
  handoff, and a contract-test report.
- #153 validation passed. The #153 smoke run proved privacy flags:
  `files_modified: false`, `private_contents_read: false`, and
  `raw_paths_echoed: false`.

Current repo/local state observed during this contract pass:

- `docs/local_artifacts_manifest.json` defines profiles for `clean_clone`,
  `local_developer_app`, `analytics_development`, `live_parser_readiness`, and
  `historical_import_readiness`.
- `tools/check_local_environment.py` can generate report-only JSON/text
  findings without reading private payloads.
- `py tools\check_local_environment.py --profile clean_clone --format json`
  returns a report and does not modify files.
- The current local checkout contains ignored/generated local families such as
  repo-local `data/` outputs and `frontend/node_modules/`.
- `.env.example` is a tracked source file.
- The current checker treats repo-root `.env*` as a secret-adjacent family, so
  tracked `.env.example` currently causes a `clean_clone` `blocked` finding.

Local app state:

- Local app generated state is expected under
  `%LOCALAPPDATA%\MythicEdgeDev\`.
- Local app paths include `config`, `db`, `logs`, `imports`, `jobs`, and
  `diagnostics`.
- Setup/status helpers report symbolic paths and avoid creating app-data
  folders.
- The developer launcher has a dry-run `check` mode and a mutating `start`
  mode. This contract may use check-mode evidence, but must not start the app
  without a later explicit authorization.

## Contract Decision

Issue #227 should become a focused pre-v1 transition contract, not an addition
to the already-completed #153 contract.

The #153 manifest/checker should remain the reusable local artifact
classification foundation. The #227 implementation may extend that checker
narrowly for transition-readiness reporting, but must not become a cleanup,
clone, archive, rename, copy, migration, or installer workflow.

## What The Audit Must Accomplish

The pre-v1 audit must answer:

- Is the current checkout clean enough to reason about?
- What branch and upstream state is the checkout on?
- Are there uncommitted, untracked, ignored, or stashed items needing manual
  review before retirement?
- Which artifacts are repo-owned source and should reproduce from Git?
- Which artifacts are generated and can be regenerated?
- Which artifacts are private/local and must be preserved outside Git?
- Which artifacts must never be committed?
- Does a clean-clone profile have enough source to run local setup checks?
- Does the local app have app-data state that must be preserved or explicitly
  initialized later?
- What remains manual-only before any old checkout is renamed, archived, or
  deleted?

The audit must produce transition readiness evidence, not transition actions.

## Current Local Checkout Risks To Identify

The audit must identify, without reading private contents:

- dirty working tree;
- untracked source-looking files;
- ignored generated/private artifact families;
- stashes that might contain uncommitted work;
- branch ahead/behind state;
- missing upstream tracking;
- local dependency/build artifacts such as `frontend/node_modules/`,
  `frontend/dist/`, Python caches, pytest caches, and Ruff caches;
- repo-local parser/runtime output families such as `data/match_logs/`,
  `data/runtime_logs/`, `data/status/`, `data/failed_posts/`,
  `data/bad_events/`, `data/decklists/`, `data/oracle_data/`, and
  `data/tier_sources/latest_tier_snapshot.json`;
- app-data state under `%LOCALAPPDATA%\MythicEdgeDev\`;
- app SQLite database and SQLite sidecars;
- local config files and secret-adjacent `.env*` files;
- historical JSONL sources selected for import workflows;
- workbook exports or other local external data files;
- false dependency on generated files inside the old checkout;
- `.env.example` template false-positive versus real local secret files.

## Artifact Preservation And Classification Policy

Use the #153 manifest classifications as the base vocabulary.

### Repo-Owned Source

Examples:

- `AGENTS.md`
- `README.md`
- `pyproject.toml`
- `.gitignore`
- `docs/`
- `src/`
- `tests/`
- `tools/`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/src/`
- `Start Mythic Edge Dev App.cmd`, if present and tracked

Policy:

- must reproduce from Git in a fresh clone;
- may be committed only through normal reviewed workflow;
- should not be copied manually from old checkout to new checkout unless the
  file is uncommitted and intentionally carried forward through Git workflow.

### Generated Local App State

Examples:

- `%LOCALAPPDATA%\MythicEdgeDev\config\app_config.json`
- `%LOCALAPPDATA%\MythicEdgeDev\db\mythic_edge.sqlite3`
- `%LOCALAPPDATA%\MythicEdgeDev\db\*.sqlite3-wal`
- `%LOCALAPPDATA%\MythicEdgeDev\db\*.sqlite3-shm`
- `%LOCALAPPDATA%\MythicEdgeDev\db\*.sqlite3-journal`
- `%LOCALAPPDATA%\MythicEdgeDev\logs\`
- `%LOCALAPPDATA%\MythicEdgeDev\imports\`
- `%LOCALAPPDATA%\MythicEdgeDev\jobs\`
- `%LOCALAPPDATA%\MythicEdgeDev\diagnostics\`

Policy:

- must never be committed;
- should be preserved for v1 transition unless intentionally reinitialized by a
  later user-approved action;
- SQLite DB and sidecars must be treated as one consistency group for any
  future copy/backup step;
- current audit may check existence/kind only and may not inspect rows,
  payloads, logs, config values, job records, or diagnostics.

### Private Local Inputs

Examples:

- MTGA `Player.log`;
- historical saved-event JSONL artifacts;
- selected JSONL folders;
- workbook exports;
- local decklists or current-deck snapshots;
- manually collected comparison artifacts.

Policy:

- must never be committed;
- current audit may only classify selected/present/missing by symbolic labels
  or coarse counts;
- raw paths, filenames, hashes, excerpts, and contents must not be written to
  repo artifacts;
- future preservation/copy/import requires explicit user approval and a scoped
  implementation or manual operator step.

### Private Local Outputs

Examples:

- `data/match_logs/`
- `data/runtime_logs/`
- `data/status/`
- `data/failed_posts/`
- `data/bad_events/`
- `data/decklists/`
- raw workbook exports

Policy:

- must never be committed;
- should be reported by category and ignored/tracked status, not by private
  filenames;
- may be preserved manually before checkout retirement;
- must not be read, copied, sanitized, archived, or deleted by this audit.

### Generated Regenerable Artifacts

Examples:

- `frontend/node_modules/`
- `frontend/dist/`
- `frontend/.vite/`
- `frontend/coverage/`
- Python caches;
- `.pytest_cache/`;
- `.ruff_cache/`;
- generated card catalog and tier snapshots.

Policy:

- usually do not need preservation;
- must remain ignored unless a specific fixture/source-data contract says
  otherwise;
- current audit may report presence/kind/ignore coverage;
- cleanup remains manual-only and explicitly out of scope.

### Manual Review Artifacts

Examples:

- untracked source-looking files;
- stashes;
- modified tracked files;
- local scripts not covered by the manifest;
- `.env*` files other than exact tracked `.env.example`;
- anything classified `unknown_private`.

Policy:

- must be manually reviewed before retirement;
- audit may report counts and categories;
- audit must not discard, stash, apply, pop, drop, rename, move, copy, or delete
  anything.

## `.env.example` Policy Recommendation

Recommendation: keep `.env.example` as a tracked source template and document it
as a special allowed template case.

Required policy:

- exact repo-root `.env.example` is repo-owned source when it is tracked and
  contains only blank or placeholder/example values;
- exact `.env.example` should not block `clean_clone`;
- exact `.env.example` should not be renamed merely to appease the broad
  `.env*` artifact family;
- real local secret files remain blocked/never-commit:
  - `.env`
  - `.env.local`
  - `.env.production`
  - `.env.<anything-except-example>`
- `.env.example` must never contain real webhook URLs, API keys, tokens,
  credentials, spreadsheet IDs, raw private paths, or user-specific values;
- secret/private-marker scanning remains authoritative for catching real values
  inside `.env.example` or any other tracked file.

Expected Codex C implementation:

- add or adjust manifest/checker logic so exact tracked `.env.example` is a
  template artifact, not a local secret file;
- keep `.env*` detection for real local secret files;
- add tests proving:
  - tracked placeholder `.env.example` is accepted in `clean_clone`;
  - untracked `.env.example` is a manual-review warning or blocked finding;
  - `.env`, `.env.local`, and `.env.production` remain blocked;
  - `.env.example` with live-looking secret material is caught by the
    secret/private-marker scanner, not silently accepted.

## Clean-Clone Verification Policy

A future clean clone is considered ready only when it can prove all of the
following without relying on old checkout clutter:

- repo source files are present and tracked;
- Python package metadata and optional `dev`/`app` dependency groups are
  present;
- local app source, frontend package metadata, and dev app launcher source are
  present;
- #153 manifest and checker are present;
- `clean_clone` checker profile has no blocked finding except none; exact
  tracked `.env.example` must be allowed as described above;
- generated/private artifacts inside the repo are absent or reported only as
  ignored local state;
- `%LOCALAPPDATA%\MythicEdgeDev\` may be absent, present, or intentionally
  initialized, but the distinction must be explicit;
- local app setup/status check can run without exposing raw paths or creating
  data in check mode;
- tests can run from repo-owned source and synthetic fixtures;
- no raw Player.log, private JSONL, generated SQLite DB, WAL/SHM/journal,
  runtime status, failed posts, workbook export, secret, credential, API key,
  token, webhook URL, or local-only artifact is required in Git.

Recommended verification commands for a future clean clone:

```powershell
git status --short --branch --untracked-files=all
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile local_developer_app --format json
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
py -m pytest -q tests\test_check_local_environment.py tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m ruff check tools tests src
```

Starting the app, importing data, initializing app data, copying databases, or
running live parser mode requires later explicit approval.

## Local Checkout Retirement Audit Policy

The current checkout may be considered "ready for manual retirement review" only
after a report records:

- current branch and upstream alignment;
- current `HEAD` commit;
- working tree status;
- stash count, without stash contents;
- untracked-unignored count/category, without private filenames by default;
- ignored/generated artifact category summary;
- #153 checker reports for:
  - `clean_clone`;
  - `local_developer_app`;
  - `analytics_development`;
  - `live_parser_readiness`, when live parser transition matters;
  - `historical_import_readiness`, when historical import transition matters;
- app-data root availability and subfolder existence by symbolic label;
- SQLite DB presence and sidecar presence by symbolic label;
- `.env.example` template status;
- real `.env*` local-secret status;
- preservation recommendations by category;
- manual-only steps still requiring human approval.

The audit must not mark the checkout safe to delete. It may only say "ready for
manual review" or "blocked until manual review."

## Safe Inspection Commands

The following commands are safe for local inspection when their output is kept
local and reviewed carefully:

```powershell
git status --short --branch --untracked-files=all
git branch -vv
git log --oneline --decorate -5
git stash list
git ls-files -o --exclude-standard
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile local_developer_app --format json
py tools\check_local_environment.py --profile analytics_development --format json
py tools\check_local_environment.py --profile historical_import_readiness --format json
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
```

The following commands are safe only as manual dry-run inspection and must not
be pasted into repo artifacts if they reveal private filenames:

```powershell
git clean -ndx
Get-ChildItem "$env:LOCALAPPDATA\MythicEdgeDev" -Force
Get-ChildItem "$env:LOCALAPPDATA\MythicEdgeDev\db" -Force
```

If a future tool consumes dry-run output, it must summarize by category and
must not persist raw private paths, raw filenames, or contents.

## Forbidden Commands And Actions

Forbidden in Codex B and in the first Codex C implementation unless a later
issue and explicit user approval authorize them:

```powershell
git clean -fd
git clean -fdx
git reset --hard
git stash drop
git stash pop
git branch -D <branch>
Remove-Item -Recurse <path>
Move-Item <old> <new>
Copy-Item -Recurse <private-path> <destination>
rmdir /s
del /s
```

Also forbidden:

- renaming the current checkout;
- creating a fresh clone;
- archiving old checkout folders;
- deleting old checkout folders;
- copying SQLite DBs, logs, or JSONL data;
- sanitizing private artifacts;
- uploading private artifacts;
- changing secrets or environment variables;
- starting live parser mode;
- importing historical data;
- starting the local app in `-Start` mode;
- changing CI gates.

## Manual-Only Versus Tool-Assisted

Tool-assisted in this contract:

- metadata-only report generation;
- manifest/profile classification;
- branch/upstream count reporting;
- stash count reporting;
- app-data existence/kind reporting;
- SQLite file and sidecar existence/kind reporting;
- `.env.example` template classification;
- real `.env*` local-secret detection without reading values;
- clean-clone readiness report;
- generated/private artifact category summaries.

Manual-only:

- inspecting secret values;
- deciding whether local JSONL/log history should be kept;
- deciding whether app SQLite data should be backed up;
- copying databases or historical files;
- stopping running apps/processes before a future DB copy;
- renaming the old checkout;
- creating a fresh clone;
- restoring or migrating app data;
- running app start/import/live parser modes;
- deleting, archiving, or cleaning the old checkout;
- closing #227 after implementation/review/merge evidence.

## Rollback And Preservation Checklist

The contract requires any future retirement plan to include this manual
checklist, but Codex C must not execute it.

Before any future rename/delete/archive step:

1. Confirm branch, upstream, and `HEAD` commit.
2. Confirm no uncommitted source changes are being abandoned.
3. Confirm stash count and manually decide what to preserve.
4. Confirm untracked files are classified.
5. Confirm ignored/generated artifacts are classified.
6. Confirm app-data root state.
7. Confirm SQLite DB and sidecars are preserved or intentionally unnecessary.
8. Confirm historical JSONL/log artifacts are preserved or intentionally
   unnecessary.
9. Confirm local secrets remain local and are not copied into Git.
10. Confirm a fresh clone can run clean-clone and local-app check profiles.
11. Keep the old checkout available until the clean install has been validated
    and the user explicitly approves final cleanup.

Rollback rule:

- If clean-install validation fails, keep using the old checkout and preserve
  all local app data. Do not delete or overwrite anything while investigating.

## Public Interface

This contract authorizes future Codex C to add or update report-only surfaces:

```powershell
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
py tools\check_local_environment.py --profile clean_clone --format json
```

The audit report should reuse the existing #153 report shape unless Codex C
finds a compelling reason to add a documented nested `transition` section.

Required report guarantees:

- `files_modified: false`;
- `private_contents_read: false`;
- `raw_paths_echoed: false`;
- report-only exit `0` when a report is generated, even if manual-review or
  blocked findings exist;
- exit `2` only for invocation/configuration errors.

## Inputs

Allowed inputs:

- repo root path;
- #153 manifest file;
- selected profile;
- safe Git metadata;
- app-data root path, symbolic in output;
- optional user-selected private paths, symbolic in output;
- launcher check-mode output, if invoked manually or in a future controlled
  test.

Forbidden inputs:

- raw Player.log contents;
- raw JSONL payloads;
- SQLite rows;
- workbook export contents;
- failed-post payloads;
- runtime status payload bodies;
- secret values;
- OAuth tokens, API keys, webhook URLs, spreadsheet IDs, or credential files.

## Outputs

Allowed outputs:

- this contract;
- future implementation handoff;
- report-only JSON/text findings with symbolic paths;
- test evidence from synthetic temp directories;
- summary counts by artifact class.

Forbidden outputs:

- raw private paths;
- local usernames;
- private filenames from ignored artifact directories;
- file hashes of private artifacts;
- raw payload excerpts;
- SQLite row values;
- secret values;
- webhook URLs;
- API keys or tokens;
- spreadsheet IDs or workbook URLs;
- cleanup scripts that perform destructive operations.

## Error Behavior

Dirty working tree:

- report manual review required;
- do not stash, reset, clean, or modify.

Stashes present:

- report stash count only;
- do not show stash contents;
- do not drop, pop, apply, or inspect stash diffs unless the user explicitly
  asks in a separate review step.

Untracked files:

- report categories and counts;
- route source-looking unknowns to manual review;
- do not stage, delete, or print private filenames by default.

Ignored generated/private folders:

- report category presence and ignore coverage;
- do not list private contents by default.

Missing app-data root:

- report as acceptable for clean clone but manual-review relevant for local
  migration.

SQLite DB present:

- report symbolic presence/kind only;
- do not open rows or run migrations.

`.env.example` present:

- accept as tracked template if exact tracked path and placeholder/blank-safe;
- block or warn if untracked, modified suspiciously, or containing secret-like
  values according to scanner evidence.

Real `.env*` files present:

- report blocked/manual review;
- do not print values.

## Side Effects

Codex B side effects authorized:

- create this contract only.

Future Codex C side effects authorized:

- update the #153 manifest/checker/tests for report-only #227 audit support;
- create implementation handoff.

Future Codex C side effects not authorized:

- no file/folder deletion;
- no file/folder rename;
- no file/folder move;
- no archive creation;
- no clone creation;
- no raw/private artifact copy;
- no app-data initialization;
- no SQLite database creation or migration;
- no local app `-Start`;
- no parser/live watcher start;
- no import execution;
- no `.gitignore` edit unless the user explicitly authorizes a separate
  follow-up;
- no CI gate change.

## Dependency Order

Future Codex C should proceed in this order:

1. Confirm branch `codex/analytics-foundation` and clean/even status.
2. Compare current #153 manifest/checker/report behavior against this contract.
3. Implement `.env.example` special-case policy first.
4. Add `clean_install_transition_audit` profile/metadata only if it can stay
   report-only and privacy-preserving.
5. Add focused tests using temporary Git repos and temp app-data folders.
6. Validate no private contents are read and no files are created outside test
   temp directories.
7. Write the implementation handoff.

## Compatibility

Required compatibility:

- existing #153 profiles continue to work;
- `live_parser` and `analytics_dev` aliases remain compatible;
- existing report object and privacy flags remain stable;
- existing local app setup/status and import tests remain unchanged;
- existing protected-surface and secret/private-marker tools remain
  authoritative;
- exact tracked `.env.example` policy must not weaken real `.env*` blocking.

## Unknowns

- Whether future v1 installer work should create app-data folders, or whether
  launcher start remains the only initializer.
- Whether v1 should provide a separate backup/export flow for
  `%LOCALAPPDATA%\MythicEdgeDev\`.
- Whether historical JSONL/log preservation should receive its own user-facing
  import/export checklist.
- Whether macOS/Linux clean-install paths should be formalized before v1.
- Whether an eventual cleanup issue should include a signed-off manual command
  transcript or stay purely operator-driven.

## Suspected Gaps

- `.env.example` currently blocks `clean_clone` because the checker treats
  `.env*` as one secret-adjacent family.
- `.gitignore` does not currently list `.env*`; whether that should change is
  not authorized by this contract.
- Current README still describes repo-local generated `data/` folders as
  operational surfaces, but clean-install policy is not yet documented in a
  user-facing setup guide.
- The current local checkout has ignored generated artifacts, including
  frontend dependencies and repo-local runtime/generated data.
- No current report summarizes branch/upstream/stash/untracked/ignored state
  as a pre-v1 retirement audit.

## Protected Surfaces

Implementation must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest, or deterministic views;
- local app backend/frontend behavior;
- launcher start behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- Line Tracer or coaching behavior;
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, or
  environment-variable contracts;
- raw logs;
- private JSONL artifacts;
- generated SQLite databases, WAL/SHM/journal files;
- runtime status files;
- failed posts;
- workbook exports;
- local-only artifacts;
- CI gates.

## Tests Required

Focused #227 tests:

```powershell
py -m pytest -q tests\test_check_local_environment.py
```

Required assertions:

- exact tracked `.env.example` is accepted as repo-owned template source in
  `clean_clone`;
- `.env`, `.env.local`, and `.env.production` remain blocked;
- `.env.example` values are not printed;
- untracked or modified `.env.example` receives manual-review warning or
  blocked status according to implementation design;
- `clean_install_transition_audit` profile, if added, references known
  artifacts and returns report-only exit `0`;
- audit report does not print raw private paths, stash contents, private
  filenames from generated folders, secret values, or payloads;
- audit report does not create app-data folders, SQLite files, logs, archives,
  clones, or cleanup artifacts;
- temporary Git repos can simulate dirty, stashed, untracked, ignored, and
  ahead/behind states without touching real local state.

Adjacent checks:

```powershell
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
```

Static checks:

```powershell
py -m ruff check tools tests src
git diff --check
py tools\check_agent_docs.py
```

Path-scoped scans:

```powershell
@'
docs/contracts/pre_v1_clean_install_transition.md
docs/local_artifacts_manifest.json
tools/check_local_environment.py
tests/test_check_local_environment.py
tests/test_pre_v1_clean_install_transition.py
docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

```powershell
@'
docs/contracts/pre_v1_clean_install_transition.md
docs/local_artifacts_manifest.json
tools/check_local_environment.py
tests/test_check_local_environment.py
tests/test_pre_v1_clean_install_transition.py
docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated/private artifact check:

- report `git status --short --branch --untracked-files=all`;
- confirm no raw Player.log files, private JSONL artifacts, SQLite DB/WAL/SHM/
  journal files, runtime logs/status files, failed posts, workbook exports,
  frontend build output, `node_modules`, archives, cloned checkouts, copied app
  data, credentials, secrets, or local-only artifacts were created or changed.

## Acceptance Criteria

- This contract exists at `docs/contracts/pre_v1_clean_install_transition.md`.
- The contract clearly separates report-only audit from actual retirement,
  cleanup, rename, clone, archive, copy, or migration actions.
- The contract uses #153 manifest/checker outputs as the base local artifact
  vocabulary.
- The contract defines clean-clone verification requirements.
- The contract defines local checkout retirement audit requirements.
- The contract defines artifact preservation/classification policy.
- The contract explicitly recommends tracked `.env.example` as an allowed
  template source while preserving blocked semantics for real `.env*` secret
  files.
- Protected surfaces and forbidden side effects are named.
- Codex C implementation scope is narrow, report-only, and testable.

## Expected Codex C Implementation Scope

Codex C should implement only:

- `.env.example` special-case policy in the manifest/checker/tests;
- optional `clean_install_transition_audit` profile and report-only metadata
  checks if they can be implemented without reading private contents or
  mutating local state;
- focused tests with synthetic temporary repos/app-data folders;
- implementation handoff.

Codex C should not implement actual checkout retirement, clone creation,
renaming, deletion, archiving, copying, backup, restore, app start, import,
live parser, `.gitignore`, CI, parser, analytics, workbook, webhook, Apps
Script, Sheets, AI, Line Tracer, coaching, or production changes.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #227.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Related completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Branch:
codex/analytics-foundation

Contract:
docs/contracts/pre_v1_clean_install_transition.md

Goal:
Compare the current #153 manifest/checker implementation, local app setup/status behavior, developer launcher check mode, protected-surface checker, secret/private-marker checker, and tests against the pre-v1 clean-install transition contract. Implement only narrow report-only support for #227.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the clean-install transition audit is supposed to do, what current #153 tooling already does, what gaps remain, and the exact minimal implementation plan.

Allowed implementation scope:
- add or adjust manifest/checker/tests so exact tracked .env.example is treated as an allowed repo-owned template in clean_clone while real .env, .env.local, .env.production, and .env.<other> remain blocked;
- optionally add a clean_install_transition_audit profile and report-only Git/app-data metadata checks if they stay privacy-preserving and non-mutating;
- add focused tests with temporary Git repos and temporary app-data folders;
- write docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md.

Do not:
- delete, move, rename, archive, copy, sanitize, upload, import, hash, or clean local files;
- run destructive cleanup commands;
- create a fresh clone or rename the current checkout;
- inspect secret values or private payload contents;
- create, rotate, edit, or print secrets or credentials;
- commit raw Player.log files, private JSONL artifacts, generated SQLite databases, WAL/SHM/journal files, runtime logs, failed posts, workbook exports, secrets, credentials, API keys, tokens, webhook URLs, node_modules, frontend build output, archives, copied app data, or local-only artifacts;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest/views, local app backend/frontend behavior, launcher start behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/model-provider behavior, Line Tracer, or coaching behavior;
- edit .gitignore or CI gates unless explicitly rerouted by the user;
- target main;
- close issue #227.

Validation:
py -m pytest -q tests\test_check_local_environment.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
py -m ruff check tools tests src
git diff --check
py tools\check_agent_docs.py
Path-scoped protected-surface and secret/private-marker scans over changed docs/checker/tests/handoff.
Report git status and confirm no generated/private/local artifacts, clone folders, archives, copied app data, SQLite sidecars, node_modules changes, frontend build output, secrets, raw logs, private JSONL, runtime files, failed posts, or workbook exports were created or changed.

Final handoff must include role performed, source issue reviewed, #153 artifacts reviewed, contract used, files changed, exact manifest/checker/test sections changed, validation run, .env.example policy result, protected-surface status, secret/private-marker status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  related_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  related_app_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_analytics_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #227 and completed #153 manifest/checker artifacts"
  target_artifact: "docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md"
  contract_artifact: "docs/contracts/pre_v1_clean_install_transition.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/pre_v1_clean_install_transition.md"
    - "path-scoped secret/private-marker scan for docs/contracts/pre_v1_clean_install_transition.md"
    - "new-file whitespace/final-newline check"
  stop_conditions:
    - "Do not delete, move, rename, archive, copy, sanitize, upload, import, hash, clean, or commit local/private/generated artifacts."
    - "Do not create a fresh clone, rename the current checkout, run destructive cleanup commands, or start local app/parser/import workflows."
    - "Do not inspect secret values or private payload contents."
    - "Do not change parser/runtime/analytics schema or ingest/local app backend or frontend/launcher start/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not edit .gitignore or CI gates unless explicitly rerouted by the user."
    - "Do not target main or close #227."
```
