# Local Artifact Manifest And Environment Profiles Contract

## Module

Local artifact manifest and environment profile checker.

This contract defines how Mythic Edge should distinguish repo-owned source
files from generated, private, and local-only artifacts across clean-clone,
local developer app, analytics-development, live-parser, and historical-import
workflows.

Plain English: this is a safety map and readiness report. It helps a fresh
checkout say "what do I have, what am I missing, and what must never be
committed" without reading private payloads, fixing the machine, or changing
runtime behavior.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/153>
- Related companion issue: <https://github.com/Tahjali11/Mythic-Edge/issues/227>
- Stale source-material PR: <https://github.com/Tahjali11/Mythic-Edge/pull/65>

Issue #153 is the active contract source. Issue #227 remains related
clean-install and local-checkout-retirement work, but it is not implemented or
closed by this contract.

PR #65 is source material only. Its `docs/local_artifacts_manifest.json` and
`tools/check_local_environment.py` ideas may inform the new implementation, but
the stale branch must not be merged, revived, or treated as authority.

## Tracker

N/A.

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

This contract must not target `main`.

## Risk Tier

Medium-High.

Reasons:

- classifies private local files, generated data, runtime artifacts, SQLite
  files, and secret-adjacent configuration surfaces;
- may guide future clean-install, local-app, analytics, and live-parser
  workflows;
- can accidentally expose local paths or private filenames if report output is
  loose;
- can accidentally grow into cleanup, migration, import, or setup automation;
- touches quality/governance policy near protected local-artifact and
  environment surfaces.

## Owning Layer

Primary owner: Quality / Governance.

Supporting project areas:

- Generated / Local Artifacts
- Local App / UI
- Analytics
- Parser runtime status surfaces, read-only only

## Internal Project Area

Quality / Governance.

This is `shared_support` for Local App / UI, Analytics, Parser runtime
readiness, and future clean-install work. It documents and reports local
readiness; it does not own parser truth, analytics truth, local-app runtime
behavior, setup authority, cleanup authority, or deployment readiness.

## Truth Owner

Truth ownership remains layered:

- Git owns the tracked repo source set.
- `.gitignore`, protected-surface checks, and secret/private-marker checks own
  guardrail evidence about what must not be committed.
- `%LOCALAPPDATA%\MythicEdgeDev\` owns local app generated state.
- MTGA `Player.log` remains local observable evidence only.
- Parser/state owns parser interpretation and normalized facts.
- Analytics SQLite owns downstream local storage of parser-normalized facts,
  not parser truth.
- The manifest and checker own only classification and readiness reporting.

The checker must not decide what happened in Arena, whether analytics facts are
correct, whether a PR is merge-ready, whether production is deployable, or
whether a local checkout may be deleted.

## Bridge-Code Status

`shared_support`.

Allowed data flow:

```text
repo metadata + manifest + safe filesystem metadata
  -> local environment report
  -> human / Codex readiness decision
```

Forbidden reverse flow:

- environment report must not write repo files;
- environment report must not modify local app state;
- environment report must not create, import, sanitize, move, delete, archive,
  upload, hash, or copy private artifacts;
- environment report must not update parser, analytics, workbook, webhook,
  Apps Script, GitHub, Google, OpenAI, or CI state.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/local_artifact_manifest_environment_profiles.md`

Future Codex C implementation files authorized by this contract:

- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md`

Reference-only source surfaces:

- `.gitignore`
- `pyproject.toml`
- `README.md`
- `docs/project_roadmap.md`
- `docs/internal_project_map.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `src/mythic_edge_parser/local_app/`
- `tools/dev_app/`
- current local app, import, protected-surface, and secret-scan tests
- stale PR #65 files, as source material only

Not owned by this contract:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest, or view behavior;
- local app UI/backend behavior beyond later report-only checker invocation;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  behavior, output transport, production behavior, AI/model-provider behavior,
  Line Tracer, or coaching behavior;
- generated SQLite databases, WAL/SHM/journal files, raw logs, local JSONL
  artifacts, runtime status files, failed posts, workbook exports, secrets,
  credentials, tokens, API keys, webhook URLs, or local-only artifacts.

## Observed Current Behavior

Repo and issue state:

- Issue #153 is open and asks for a local artifact manifest and environment
  profile checker.
- Issue #227 is open and asks for a separate pre-v1 clean-install transition
  and local-checkout retirement audit.
- PR #65 is closed and stale. It contains a simple JSON manifest and Python
  checker that classify several local artifacts, but it predates the current
  analytics and local-app work.
- `.gitignore` already ignores common generated/local roots:
  `data/match_logs/`, `data/decklists/`, `data/runtime_logs/`,
  `data/status/`, `data/failed_posts/`, `data/bad_events/`,
  `data/analytics/`, `data/oracle_data/`,
  `data/tier_sources/latest_tier_snapshot.json`, `_review_*/`,
  `.github/Mythic-Edge/`, `frontend/node_modules/`, `frontend/dist/`,
  `frontend/.vite/`, and `frontend/coverage/`.
- `tools/check_protected_surfaces.py` path-classifies many forbidden local
  artifact families and protected parser/workbook/workflow surfaces.
- `tools/check_secret_patterns.py` scans content for live webhook URLs,
  credentials, private local paths, raw Player.log markers, runtime payloads,
  failed-post payloads, generated-data dumps, and workbook-export markers.

Local app and analytics state:

- The local app generated root is already defined as
  `%LOCALAPPDATA%\MythicEdgeDev\`.
- `src/mythic_edge_parser/local_app/paths.py` defines the app-data subfolders:
  `config`, `db`, `logs`, `imports`, `jobs`, and `diagnostics`.
- Local app setup/status code reports symbolic paths such as `<app_data>` and
  `<configured_player_log>` instead of raw absolute paths.
- Setup/status routes are tested to avoid creating local app folders or
  database files.
- Local app import jobs may create app-owned SQLite state under
  `%LOCALAPPDATA%\MythicEdgeDev\db\` during explicit import flows, but those
  import flows are outside this contract.
- Current local app tests assert that raw paths, raw config values, webhook
  values, and temp paths are not echoed in backend responses.

Observed gaps:

- There is no current source-controlled canonical local artifact manifest.
- There is no current profile checker for clean clone, local developer app,
  analytics development, live parser readiness, or historical import
  readiness.
- There is no single place explaining which artifact families are repo-owned,
  generated, private input, private output, app-owned, or never-commit.
- There is no profile report shape that future #227 clean-install work can
  cite without inventing its own classifications.
- Existing `.gitignore`, protected-surface gate, and secret scanner overlap but
  do not provide a human-readable environment readiness report.

## Required Manifest Contract

The first implementation should create a source-controlled JSON manifest:

```text
docs/local_artifacts_manifest.json
```

JSON is required for v1 because:

- it is machine-readable without importing executable Python;
- it needs no new dependency;
- it matches the useful shape from stale PR #65 while allowing a safer current
  schema;
- it can be schema-tested with the Python standard library.

Markdown may summarize the manifest later, but it must not be the source of
truth for the checker. YAML is not required in v1. Python-owned structured data
is forbidden for v1 because loading the manifest must not execute project code.

Required top-level fields:

```json
{
  "schema_version": "local_artifacts_manifest.v1",
  "object": "mythic_edge_local_artifacts_manifest",
  "description": "...",
  "profiles": {},
  "artifact_classes": {},
  "artifacts": []
}
```

Each artifact entry must include:

- `id`: stable kebab_case or snake_case identifier;
- `label`: human-readable display label;
- `classification`: one of the required classifications below;
- `path_scope`: `repo_relative`, `app_data_relative`, `env_relative`,
  `user_selected`, `external_only`, or `git_metadata`;
- `path_pattern`: symbolic path only, never a machine-specific absolute path;
- `git_policy`: `tracked_allowed`, `ignored_required`, `never_commit`, or
  `external_only`;
- `privacy`: `public_repo_source`, `generated_nonprivate`,
  `private_local`, `secret_or_credential`, or `unknown_private`;
- `profiles`: object naming profile requirements and severities;
- `safe_checks`: allowed metadata checks for the checker;
- `forbidden_checks`: content or side-effect checks the checker must not do;
- `notes`: short text explaining why the artifact is classified this way.

Optional fields:

- `env_var`, only for environment-variable names, never values;
- `example_display_path`, using symbolic placeholders such as `<repo>`,
  `<app_data>`, `<configured_player_log>`, or `%LOCALAPPDATA%`;
- `gitignore_expectation`, such as `covered`, `not_applicable`,
  `report_if_missing`, or `unknown`;
- `related_contracts`;
- `safe_fixture_policy`, only when a sanitized fixture contract exists.

The manifest must not include:

- raw private filenames from the current machine;
- raw absolute user paths;
- raw Player.log paths beyond symbolic Windows examples;
- webhook URLs, API keys, tokens, spreadsheet IDs, workbook URLs, OAuth values,
  or credential values;
- raw hashes of private files;
- file contents, payload excerpts, stack traces, or exception dumps;
- clean-install deletion, rename, archive, or migration steps.

## Required Artifact Classifications

The v1 manifest must support these classifications.

### Repo-Owned Source Files

Tracked source, tests, docs, config, and tooling that may be committed when
reviewed and within scope.

Examples:

- `AGENTS.md`
- `README.md`
- `pyproject.toml`
- `.gitignore`
- `src/`
- `tests/`
- `tools/`
- `frontend/src/`
- `frontend/package.json`
- `frontend/package-lock.json`
- `docs/contracts/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`

Policy:

- `git_policy`: `tracked_allowed`
- checker may inspect existence and Git tracked/untracked status;
- checker must not decide whether a code change is correct.

### Generated Local App State

App-owned generated state under:

```text
%LOCALAPPDATA%\MythicEdgeDev\
```

Required symbolic children:

- `<app_data>\config\app_config.json`
- `<app_data>\db\mythic_edge.sqlite3`
- `<app_data>\logs\`
- `<app_data>\imports\`
- `<app_data>\jobs\`
- `<app_data>\diagnostics\`
- SQLite sidecars: `*.sqlite3-wal`, `*.sqlite3-shm`, `*.sqlite3-journal`

Policy:

- `git_policy`: `never_commit`
- checker may report existence, missing status, and symbolic display paths;
- checker may not read database rows, config values, raw import contents, job
  payloads, logs, or diagnostics in v1;
- checker may not create app-data folders or initialize databases.

### Private Local Inputs

Operator-selected or machine-local inputs that may feed parser, import, or
analytics workflows.

Examples:

- MTGA `Player.log`
- historical saved-event JSONL artifacts;
- selected local folders containing JSONL artifacts;
- local workbook exports used for manual comparison;
- local decklist snapshots or current-deck files.

Policy:

- `git_policy`: `never_commit`
- checker may report selected/missing/present using symbolic labels;
- checker may validate extension, file-vs-directory kind, and existence only
  when the path is supplied by config, environment, or explicit CLI argument;
- checker must not read, hash, copy, sanitize, upload, import, enumerate deep
  contents, or echo raw paths.

### Private Local Outputs

Generated outputs from parser/runtime/import workflows that may contain private
payloads or local state.

Examples:

- `data/match_logs/`
- `data/runtime_logs/`
- `data/status/`
- `data/failed_posts/`
- `data/bad_events/`
- `data/decklists/`
- raw workbook exports
- local generated import reports

Policy:

- `git_policy`: `ignored_required` or `never_commit`
- checker may report whether the repo ignore policy appears to cover the
  family;
- checker may report coarse existence, such as "directory present";
- checker must not list private filenames by default, read contents, hash
  contents, or move/delete files.

### Generated Nonprivate Support Data

Regenerable support outputs that may not be private but still should not become
source by accident.

Examples:

- `data/oracle_data/`
- generated tier-source snapshots;
- frontend build output;
- Python caches;
- coverage output;
- dependency caches such as `frontend/node_modules/`.

Policy:

- `git_policy`: `ignored_required` unless a current contract authorizes a
  specific committed fixture or override file;
- checker may report ignore coverage and presence;
- checker must not refresh, regenerate, or clean the data.

### Secret And Credential Surfaces

Secret-adjacent values and files.

Examples:

- `.env`
- `.env.*`
- credential JSON files;
- webhook URL files;
- API key files;
- OAuth token files;
- local config fields with names containing token, secret, credential, OAuth,
  API key, or webhook.

Policy:

- `git_policy`: `never_commit`
- checker may report "secret-like file or field detected" with redacted labels;
- checker must not print values, read private config values into reports, or
  offer credential rotation or creation.

## Required Environment Profiles

The manifest must define these first profiles.

### `clean_clone`

Purpose: a fresh repository checkout with no private MTGA data and no local app
state.

Required:

- repo-owned source files needed for normal tests and documentation;
- no private local artifacts.

Expected report behavior:

- missing `Player.log`, app-data root, JSONL artifacts, runtime logs, failed
  posts, and SQLite files are `info` or `not_applicable`, not failures;
- generated/private artifacts present inside the repo are warnings or blockers
  depending on Git status and ignore coverage;
- checker must not create app-data folders.

### `local_developer_app`

Purpose: a checkout that can run the local developer app shell.

Required:

- Python package metadata;
- `src/mythic_edge_parser/local_app/`;
- `frontend/package.json` and frontend source;
- `tools/dev_app/`;
- app-data root availability or a clear `missing`/`unavailable` report.

Expected report behavior:

- app-data subfolders may be missing if setup has not run;
- database may be missing;
- missing generated app state is informational unless a later explicit profile
  requires an initialized app;
- report must use symbolic app-data paths only.

### `analytics_development`

Purpose: a checkout that can run analytics schema, migration, ingest, and view
tests without relying on private local data.

Required:

- analytics migration SQL as package data;
- analytics ingest and migration loader modules;
- analytics tests and synthetic fixtures;
- no repo-local SQLite database requirement.

Expected report behavior:

- generated `data/analytics/` SQLite files inside the repo are warnings if
  present and must remain ignored;
- in-memory and pytest temporary SQLite use is allowed;
- raw Player.log and private JSONL artifacts are not required.

### `live_parser_readiness`

Purpose: a machine intended to run the live parser against MTGA.

Required:

- parser entrypoint/source files;
- a configured or detected `Player.log` path;
- safe local runtime artifact roots;
- no committed secrets or live webhook URL values.

Expected report behavior:

- missing `Player.log` is a `blocked` readiness finding for this profile only;
- checker must report `contents_read: false`;
- webhook posting readiness is advisory unless a separate contract defines a
  credential/config check;
- checker must not start the parser, tail `Player.log`, post webhooks, or read
  runtime payloads.

### `historical_import_readiness`

Purpose: a machine intended to import selected historical JSONL artifacts
through approved local import flows.

Required:

- local app import code;
- analytics legacy JSONL adapter and ingest dependencies;
- app-data root availability;
- optional user-supplied source path or source folder.

Expected report behavior:

- no source selected is `info`, not failure;
- an explicitly supplied missing/invalid source is `blocked`;
- checker may validate extension and file/directory kind without reading
  payloads;
- checker must not import, upload, copy, sanitize, hash, or retain raw JSONL.

## Deferred Profile For #227

The checker may reserve the name:

```text
clean_install_transition_audit
```

but it must not implement destructive or state-changing clean-install behavior
under issue #153.

Issue #227 should receive its own contract before any thread:

- renames the current checkout;
- creates a fresh clone;
- copies or migrates app data;
- archives, deletes, or cleans old folders;
- records rollback steps;
- performs final cleanup.

The #153 manifest/checker may become evidence for #227, but it must not
replace #227.

## Required Checker Contract

Codex C should implement a report-only local CLI:

```powershell
py tools\check_local_environment.py --profile clean_clone
py tools\check_local_environment.py --profile local_developer_app
py tools\check_local_environment.py --profile analytics_development
py tools\check_local_environment.py --profile live_parser_readiness
py tools\check_local_environment.py --profile historical_import_readiness
```

Recommended optional arguments:

```powershell
--repo-root <path>
--manifest docs/local_artifacts_manifest.json
--format text|json
--app-data-root <path>
--player-log-path <path>
--source-path <path>
--source-folder <path>
```

All path arguments are local metadata inputs. The checker must not treat them as
authorization to read payloads, copy files, import data, sanitize data, or print
raw paths.

### Report Shape

The JSON report must use a stable object shape:

```json
{
  "object": "mythic_edge_local_environment_report",
  "schema_version": "local_artifact_manifest_environment_profiles.v1",
  "profile": "clean_clone",
  "status": "ok",
  "summary": {
    "checks": 0,
    "ok": 0,
    "info": 0,
    "warnings": 0,
    "blocked": 0,
    "errors": 0
  },
  "privacy": {
    "raw_paths_echoed": false,
    "private_contents_read": false,
    "files_modified": false
  },
  "findings": []
}
```

Each finding must include:

- `check_id`;
- `artifact_id`;
- `classification`;
- `severity`: `ok`, `info`, `warning`, `blocked`, or `error`;
- `display_path`: symbolic path only;
- `expected`;
- `observed`;
- `message`;
- `remediation`;
- `contents_read`: always `false` for private artifacts;
- `path_echoed`: `false` for private/local paths.

Text output must be human-readable and must follow the same redaction rules as
JSON output.

### Exit Code Policy

The v1 checker is report-only.

Required exit behavior:

- exit `0` for successful report generation, even when findings are warning or
  blocked;
- exit `2` for invocation errors, unreadable manifest, invalid manifest, or
  unsupported profile;
- do not use exit `1` as a CI-style failure gate in v1.

Rationale: issue #153 is a local quality/readiness report, not a new required
CI gate or clean-install blocker.

## Privacy And Local Artifact Safety Rules

The manifest and checker must preserve these rules:

- do not read raw `Player.log` contents;
- do not read raw JSONL payloads;
- do not read failed-post payloads;
- do not read runtime status payload bodies for report output;
- do not read workbook exports;
- do not inspect SQLite rows;
- do not hash private files;
- do not print absolute private paths, local usernames, raw filenames from
  private directories, webhook URLs, tokens, API keys, spreadsheet IDs, or
  credential values;
- do not create, delete, rename, move, copy, sanitize, upload, import, archive,
  compress, or clean private files;
- do not create app-data folders, SQLite databases, WAL/SHM/journal files,
  runtime logs, failed-post queues, generated card data, or frontend build
  output;
- do not modify `.gitignore`, config files, environment variables, GitHub
  issues, PRs, Google Sheets, Apps Script, or OpenAI/model-provider settings.

Allowed safe checks:

- repo-relative existence checks for source-controlled files;
- Git tracked/untracked/ignored checks;
- symbolic app-data root availability;
- file-vs-directory kind checks for explicitly supplied paths;
- extension checks for explicitly supplied JSONL paths;
- environment variable name presence, but not value printing;
- coarse "present/missing/unavailable" status;
- use of temporary files/directories in tests only.

## Required Relationship To Existing Gates

The checker must complement existing tools:

- `tools/check_protected_surfaces.py` remains the path-based protected and
  forbidden artifact gate.
- `tools/check_secret_patterns.py` remains the content scanner for changed or
  all-repo advisory scans.
- The new local environment checker reports profile readiness and artifact
  classification. It does not replace either existing tool.

The v1 checker must not be added as a required CI gate. A later issue and
contract may decide whether a subset of manifest validation becomes CI-required.

## Error Behavior

Malformed manifest:

- report invocation error;
- exit `2`;
- do not fall back to stale PR #65 behavior.

Unknown profile:

- list known profile names;
- exit `2`;
- do not infer the closest profile.

Missing optional artifact:

- report `info` or `not_applicable` depending on profile.

Missing required profile artifact:

- report `blocked`;
- exit `0` if the report was generated.

Uninspectable private path:

- report `warning` or `blocked` based on profile;
- do not print raw path or exception detail.

Git unavailable:

- report `error` for Git metadata checks;
- keep non-Git checks if they can run safely;
- exit `0` if the profile report was generated, unless Git is required to load
  the repo root or manifest.

## Side Effects

Codex B side effects:

- creates this contract only.

Future Codex C side effects authorized:

- create `docs/local_artifacts_manifest.json`;
- create `tools/check_local_environment.py`;
- create focused tests;
- create implementation handoff.

Future Codex C side effects not authorized:

- no parser/runtime behavior changes;
- no app-data creation;
- no SQLite creation;
- no import execution;
- no `.gitignore` edits in the first implementation pass;
- no CI gate changes;
- no cleanup, deletion, rename, copy, move, sanitize, upload, or archive
  behavior.

If Codex C discovers missing `.gitignore` coverage, it should record a
suspected gap in the implementation handoff and route a narrow follow-up,
rather than editing `.gitignore` under this first #153 implementation.

## Dependency Order

Codex C should implement in this order:

1. Reconfirm branch `codex/analytics-foundation` and inspect current status.
2. Create the manifest schema and v1 entries.
3. Add schema/manifest tests that do not inspect private local files.
4. Implement manifest loading and profile selection.
5. Implement safe metadata-only checks.
6. Implement redacted text and JSON reports.
7. Add tests for redaction, no content reads, no file creation, and report-only
   exit behavior.
8. Write implementation handoff.

## Compatibility

The v1 manifest may reuse useful artifact IDs from PR #65 when they still make
sense, but it must update names and profile coverage to current branch reality.

Compatibility requirements:

- `clean_clone`, `live_parser`, and `analytics_dev` concepts from PR #65 should
  map to current profile names or aliases in tests/handoff.
- If aliases are implemented, they must be documented and must not create new
  profile semantics.
- Current local app symbolic path behavior must be preserved.
- Existing protected-surface and secret/private-marker checks must keep their
  current command behavior.

## Unknowns

- Whether a later CI job should validate only the manifest schema.
- Whether `.gitignore` should gain additional explicit patterns for `.env*`,
  SQLite sidecars outside `data/analytics/`, or app-data mirror accidents.
- Whether #227 should add a dedicated clean-install profile or consume the v1
  profiles without adding a new one.
- Whether future macOS/Linux local-app paths should be formalized before or
  after Windows pre-v1 install work.
- Whether environment variable names from parser config should be enumerated in
  the manifest or kept as broad secret/config categories.

## Suspected Gaps

- No current canonical manifest exists.
- No current report-only checker exists.
- `.gitignore` may not explicitly cover every local/private artifact family
  named by current contracts, especially credential-style files and local app
  mirrors outside `%LOCALAPPDATA%`.
- README still describes several local `data/` folders as operational surfaces
  but does not provide a machine-readable commit policy.
- Existing local app status checks are route-level and do not provide a
  repo-wide clean-clone or live-parser readiness profile.

## Protected Surfaces

Implementation must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest, or deterministic view behavior;
- local app backend/frontend behavior outside explicitly adding a later
  checker invocation if separately contracted;
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
- generated data;
- runtime status files;
- failed posts;
- workbook exports;
- local-only artifacts;
- CI gate behavior.

## Tests Required

Focused checker tests:

```powershell
py -m pytest -q tests\test_check_local_environment.py
```

Required assertions:

- manifest has required top-level fields and valid artifact entries;
- every profile references known artifact IDs;
- unknown profile exits `2`;
- malformed manifest exits `2`;
- `clean_clone` does not require private artifacts;
- profile missing required artifacts reports `blocked` but exits `0`;
- private path values are not echoed in text or JSON reports;
- private file contents are not read;
- checker does not create app-data folders, SQLite files, logs, or repo-local
  artifacts;
- environment variable names may be shown but values are not shown;
- JSON report fields are stable;
- text report redacts symbolic/private paths;
- stale PR #65 behavior that printed raw expanded paths is not reintroduced.

Regression and guardrail tests:

```powershell
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
```

Static validation:

```powershell
py -m ruff check tools tests src
git diff --check
py tools\check_secret_patterns.py --all
```

Path-scoped protected-surface scan:

```powershell
@'
docs/contracts/local_artifact_manifest_environment_profiles.md
docs/local_artifacts_manifest.json
tools/check_local_environment.py
tests/test_check_local_environment.py
docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
docs/contracts/local_artifact_manifest_environment_profiles.md
docs/local_artifacts_manifest.json
tools/check_local_environment.py
tests/test_check_local_environment.py
docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated/private artifact check:

- report `git status --short --branch`;
- confirm no raw Player.log, private JSONL artifacts, SQLite DB/WAL/SHM/journal
  files, runtime logs/status, failed posts, workbook exports, frontend build
  output, `node_modules`, credentials, secrets, or local-only artifacts were
  created or changed.

## Acceptance Criteria

- `docs/local_artifacts_manifest.json` exists with the v1 schema.
- `tools/check_local_environment.py` exists and is report-only.
- The checker supports `clean_clone`, `local_developer_app`,
  `analytics_development`, `live_parser_readiness`, and
  `historical_import_readiness`.
- The checker produces stable text and JSON output.
- The checker exits `0` for successful reports, including reports with blocked
  readiness findings, and exits `2` for invocation/configuration errors.
- Reports use symbolic paths and do not expose raw absolute paths, local
  usernames, private filenames from local artifact directories, raw payloads,
  hashes, webhook URLs, tokens, API keys, credentials, spreadsheet IDs, or
  config values.
- The checker never reads private file contents and never mutates local or repo
  state.
- Existing protected-surface and secret/private-marker tooling remains
  unchanged.
- Existing local app setup/status and import behavior remains unchanged.
- Issue #227 remains open and separately scoped.
- No generated/private/local artifacts are committed.
- No parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior
  changes are made.

## Expected Codex C Implementation Scope

Codex C should compare the current repo against this contract, then implement
only:

- the JSON manifest;
- the report-only local environment checker;
- focused tests;
- implementation handoff.

Codex C should not edit `.gitignore`, CI, parser modules, analytics ingest,
local app runtime behavior, frontend UI, import behavior, or clean-install
workflow steps unless the user explicitly reroutes or a follow-up contract
authorizes that scope.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #153.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_artifact_manifest_environment_profiles.md

Goal:
Compare the current repo, stale PR #65 source material, local app setup/status behavior, protected-surface checker, secret/private-marker checker, and tests against the contract. Implement only the v1 source-controlled local artifact manifest, report-only local environment checker, focused tests, and implementation handoff.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the manifest/checker is supposed to do, what the current repo already does, what gaps remain, and the exact minimal implementation plan.

Implement:
- docs/local_artifacts_manifest.json
- tools/check_local_environment.py
- tests/test_check_local_environment.py
- docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md

Preserve:
- report-only behavior
- symbolic/redacted paths
- no private content reads
- no file creation or cleanup
- no CI gate changes
- existing local app setup/status/import behavior
- existing protected-surface and secret/private-marker behavior

Do not:
- implement #227 clean-install or checkout-retirement behavior
- merge or revive stale PR #65 directly
- edit .gitignore in the first pass unless the user explicitly authorizes a follow-up
- create, delete, move, rename, copy, sanitize, upload, import, hash, or archive private/local artifacts
- create SQLite databases, WAL/SHM/journal files, app-data folders, runtime logs, failed posts, workbook exports, frontend build output, node_modules, secrets, credentials, tokens, API keys, webhook URLs, or local-only artifacts
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest/views, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/model-provider behavior, Line Tracer, or coaching behavior
- target main
- close issue #153 or #227
- stage, commit, push, or open a PR unless explicitly asked

Validation:
py -m pytest -q tests\test_check_local_environment.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py
py -m ruff check tools tests src
git diff --check
py tools\check_secret_patterns.py --all
Path-scoped protected-surface and secret/private-marker scans over the contract, manifest, checker, tests, and handoff.
Report git status and confirm no generated/private/local artifacts were created or changed.

Final handoff must include role performed, source issue reviewed, related issue reviewed, contract used, files changed, exact manifest/checker/test sections changed, validation run, protected-surface status, secret/private-marker status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #153 and stale PR #65 source material"
  target_artifact: "docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md"
  contract_artifact: "docs/contracts/local_artifact_manifest_environment_profiles.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/local_artifact_manifest_environment_profiles.md"
    - "path-scoped secret/private-marker scan for docs/contracts/local_artifact_manifest_environment_profiles.md"
  stop_conditions:
    - "Do not implement #227 clean-install or checkout-retirement behavior."
    - "Do not merge or revive stale PR #65 directly."
    - "Do not edit .gitignore, CI gates, parser/runtime behavior, analytics schema/migrations/ingest/views, local app runtime behavior, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create, delete, move, rename, copy, sanitize, upload, import, hash, archive, or commit generated/private/local artifacts or secrets."
    - "Do not target main."
```
