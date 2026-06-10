# Private Local V1 Installation Wizard And First-Run Configuration Contract

## Module

`setup_app_private_local_v1_installation_wizard`

Plain English: this contract defines the safe setup path that should get a
private-local-v1 user from fresh checkout/download to a working Mythic Edge
local app without hand-editing JSON config files, knowing app-data paths, or
running fragile one-off PowerShell snippets.

This is a Codex B contract-writing artifact only. It does not implement setup,
launcher, backend, frontend, parser, analytics, workbook, transport, OpenAI, AI,
or production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Maturity tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Historical analytics tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Historical local app umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Related launcher issue: https://github.com/Tahjali11/Mythic-Edge/issues/210
- Related clean install issue: https://github.com/Tahjali11/Mythic-Edge/issues/253
- Related live Player.log control issue: https://github.com/Tahjali11/Mythic-Edge/issues/297
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/setup_app_private_local_v1_installation_wizard.md`

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- issue #314
- tracker #136
- historical issues #204 and #207
- issues #210, #253, and #297
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- focused setup, launcher, config, setup-status, and Player.log status tests

## Risk Tier

High.

Reasons:

- the flow touches private-local-v1 release readiness;
- it may create local app folders, write local config, initialize SQLite,
  install project dependencies, launch backend/frontend processes, and open a
  browser in later implementation threads;
- it configures a private Player.log path;
- setup reports can leak private paths, environment values, stack traces, raw
  logs, generated database details, or secret-looking values if not redacted;
- it sits near live capture, but must not start capture automatically.

## Owning Layer

Primary owner: Local App / UI setup and launcher.

Supporting owners:

- Quality / Governance release readiness;
- Generated / Local Artifacts;
- Analytics, only for applying existing migrations to an empty local SQLite
  database;
- Parser, reference-only for Player.log and parser truth boundaries.

## Internal Project Area

Local App / UI.

Supporting internal project areas:

- Quality / Governance;
- Generated / Local Artifacts;
- Analytics.

## Truth Owner

The setup wizard owns local setup orchestration and readiness evidence only.

Truth ownership remains unchanged:

- MTGA `Player.log` remains the raw observable source.
- Parser/state owns event interpretation, match/game identity, deduplication,
  final reconciliation, and parser-normalized facts.
- Analytics migrations own SQLite schema history.
- SQLite stores downstream analytics facts; it does not own parser truth.
- The local app owns setup/status display, launch orchestration, and local
  operator workflow.
- The setup report and install manifest own local setup evidence only.

The setup wizard, browser first-run screen, config file, install manifest, setup
report, SQLite database, and local app status payloads must not become parser
truth, analytics truth, workbook truth, production truth, AI truth, or
deployment authority.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
repo release ref + local toolchain metadata + user-approved local setup choices
  -> setup helper / setup wizard
  -> app-data folders, local config, install manifest, setup report
  -> local backend/frontend launch and setup-status verification
```

Forbidden reverse flow:

- setup output must not change parser behavior;
- setup output must not change analytics schema, migrations, or ingest
  semantics;
- setup output must not change workbook, webhook, Apps Script, Google Sheets,
  output transport, production, OpenAI/model-provider, AI/coaching, Line Tracer,
  hidden-card, archetype, player-mistake, or gameplay-advice behavior;
- frontend status must not infer parser-owned facts or live capture success.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/setup_app_private_local_v1_installation_wizard.md`

Expected future Codex C artifact:

- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`

Expected future Codex E artifact:

- `docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md`

Future Codex C may compare or change only scoped setup/local-app surfaces, such
as:

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`, only for setup/config/status
  routes explicitly authorized by this contract;
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- focused tests for setup, config, launcher, setup status, and frontend
  first-run display.

Codex C must route back to Codex B before changing parser behavior, parser
runtime defaults, analytics schema or migrations, live capture semantics,
workbook/webhook/App Script/Sheets behavior, OpenAI/model-provider behavior,
credential policy, production behavior, CI gates, or Pyright gate behavior.

## Observed Current Behavior

### Issue And Tracker State

- Issue #314 is open and frames a private-local-v1 release-readiness gap.
- Tracker #136 remains open.
- Historical issues #204 and #207 are closed as local app readiness trackers
  with acceptable private-local degradation, not public or production
  readiness.
- Issue #210 completed a Windows developer launcher/preflight slice.
- Issue #253 completed clean install mechanics and setup proof foundations.
- Issue #297 completed explicit Start Capture control, but live capture must
  remain explicit and must not begin during setup.

### Existing Setup Foundation

`tools/dev_app/private_local_v1_setup.py` already defines:

- default private-local-v1 install root `%LOCALAPPDATA%\MythicEdge`;
- managed app checkout root `<install_root>\app`;
- generated data root `<install_root>\data`;
- generated subfolders for `config`, `db`, `logs`, `imports`, `jobs`,
  `diagnostics`, `exports`, and reserved `ai_review` folders;
- install manifest path `<install_root>\data\config\install_manifest.json`;
- setup report path `<install_root>\data\diagnostics\setup_report.json`;
- analytics database path `<install_root>\data\db\mythic_edge.sqlite3`;
- controlled check/install/proof modes;
- app-data-root refusal when the data root is inside a source or Git checkout;
- existing-install blocking that preserves prior manifest/report/database data;
- SQLite initialization through the existing analytics migration loader;
- JSON writing with `encoding="utf-8"`;
- symbolic setup output that avoids raw install-root strings.

`tools/dev_app/setup_private_local_v1.ps1` is a thin wrapper over the Python
helper. It does not perform destructive setup commands directly.

### Existing Developer Launcher

`tools/dev_app/start_mythic_edge_dev_app.ps1` and
`tools/dev_app/dev_app_launcher.py` support existing-checkout local app launch
with a developer default app-data root named `MythicEdgeDev`. The private-local
setup helper uses `MythicEdge` as the release-profile root and must keep passing
the desired data root explicitly when launching from a v1 install.

### Existing Local App Config

`src/mythic_edge_parser/local_app/config.py` currently allows these local config
fields:

- `player_log_path`
- `analytics_database_path`
- `backend_host`
- `backend_port`
- `frontend_origin`

The config status reader:

- reports missing, invalid, unreadable, and present config states;
- avoids echoing config values;
- redacts secret-like unexpected fields;
- currently reads JSON using plain UTF-8.

Issue #314 reports a real setup failure where a UTF-8 with BOM config file was
classified as invalid JSON. That is a setup/config robustness gap.

### Existing Player.log Status

`src/mythic_edge_parser/local_app/setup_status.py` already:

- reads the configured `player_log_path`;
- falls back to a default MTGA Player.log candidate;
- checks metadata only;
- reports symbolic display paths such as `<configured_player_log>` and
  `<detected_mtga_player_log>`;
- returns `contents_read = false` and `tailing_started = false`;
- does not read raw Player.log contents.

The current parser runtime config also contains a developer-specific
`DEFAULT_MTGA_PLAYER_LOG` constant. This contract does not authorize changing
parser runtime defaults. A setup-specific detector may be added under local app
or setup tooling if needed, but parser runtime behavior must remain unchanged
unless a future parser contract authorizes a change.

### Existing Local App Backend And Frontend

The local app backend already exposes setup/status, config status,
Player.log/live status, analytics database status, live capture status, and
other local app endpoints. Existing frontend tests verify symbolic app-data and
Player.log display values and redaction behavior.

Observed gap:

- there is no first-run setup wizard that writes the local app config;
- a normal user still may need to hand-create or hand-edit
  `app_config.json`;
- the setup flow does not yet safely detect/confirm/write Player.log
  configuration as part of private-local-v1 setup;
- the setup flow does not yet explicitly guarantee BOM-tolerant config reads.

## Contract Decision

Private-local-v1 setup should be a Windows-first CLI setup wizard followed by a
browser first-run status screen.

Decision:

- CLI-first for installation and local machine setup.
- Browser first-run status for confirmation, troubleshooting, and next steps.
- Do not make the first v1 setup implementation frontend-first, because the
  backend, app-data root, config, dependency state, and SQLite database must be
  available before the browser can be relied on.

The first implementation may be interactive CLI, prompt-driven PowerShell, or a
Python CLI wizard routed through the existing PowerShell wrapper. It should
open or point to the local frontend after success, unless the user selects a
no-open mode.

Frontend first-run behavior may display setup status, blocked/degraded states,
safe remediation text, and route links. It should not become the first approved
raw path editor unless Codex C proves that a backend-owned config write route
is required and can preserve all privacy and path-redaction rules.

## Setup Wizard Objective

The setup wizard must prove and, where explicitly allowed, create:

1. supported Windows local setup context;
2. usable source checkout or managed private-local-v1 install root;
3. toolchain readiness for Python, Node.js, npm, and Git;
4. generated app-data folder tree outside the repo;
5. empty/current analytics SQLite database using existing migrations;
6. safe local app config containing a user-confirmed Player.log path;
7. backend/frontend launch readiness on loopback;
8. browser first-run setup/status visibility;
9. sanitized install manifest and setup report;
10. no raw/private/generated artifacts committed or exposed.

The setup wizard is successful only when the user can start the local app and
understand setup status without manually creating JSON config files or knowing
internal app-data paths.

## Setup Wizard Model

Preferred source-controlled entrypoint:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite
```

Future implementation may add explicit wizard/configuration flags, for example:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -Wizard
.\tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
```

The Python helper may expose equivalent flags, for example:

```powershell
py tools\dev_app\private_local_v1_setup.py --install --initialize-sqlite --wizard
py tools\dev_app\private_local_v1_setup.py --check --json-report
```

Codex C may choose different flag names only if the implementation comparison
explains why they better match current repo patterns. Existing `--check`,
`--install`, `--proof`, `--initialize-sqlite`, `--install-root`,
`--source-checkout`, `--release-ref`, `--no-open`, and JSON-report behavior
must remain backward-compatible.

## Automatic Versus User-Confirmed Steps

### Automatic In Normal Install Mode

After the user chooses an install/setup mode, the wizard may automatically:

- inspect tool availability and versions;
- validate source checkout markers;
- validate that app-data root is outside Git checkouts;
- create missing generated folders for a clean app-data root;
- initialize or verify the analytics SQLite database using existing
  migrations;
- detect a candidate MTGA Player.log path using metadata only;
- write install manifest and setup report;
- launch backend/frontend through existing launcher-compatible behavior;
- open the browser or report browser-open failure as degraded.

### Requires User Confirmation

The wizard must ask or require explicit user selection before:

- using a non-default install root;
- reusing an existing app-data root with prior manifest/report/database or
  generated data;
- changing `player_log_path` in local config;
- accepting a detected Player.log candidate;
- using a manually entered Player.log path;
- installing project dependencies if the action can be long-running or
  machine-specific;
- leaving backend/frontend processes running after proof/setup;
- writing to the actual default private-local root during a Codex validation
  thread.

### Deferred Or Manual-Only

The wizard must not automatically:

- install system-level Python, Node.js, npm, or Git;
- alter system PATH, registry, shell profile, or global package-manager state;
- delete, move, archive, reset, clean, or uninstall local folders;
- start live Player.log capture;
- import JSONL files;
- write parser facts to SQLite;
- send data to external services.

## App-Data Behavior

Default private-local-v1 structure remains:

```text
%LOCALAPPDATA%\MythicEdge\
  app\
  data\
    config\
      app_config.json
      install_manifest.json
    db\
      mythic_edge.sqlite3
    logs\
    imports\
    jobs\
    diagnostics\
      setup_report.json
    exports\
    ai_review\
      sources\
      packets\
      reports\
```

Clean app-data root behavior:

- create missing required generated folders;
- create `app_config.json` only after a safe config payload is available;
- initialize or verify an empty migrated analytics SQLite database;
- write sanitized manifest/report artifacts;
- launch local app when setup succeeds unless `NoOpen` or stop-after-proof mode
  is selected.

Existing app-data root behavior:

- inspect metadata only;
- detect manifest, setup report, analytics database, config file, generated
  subfolders, and app checkout state;
- preserve existing files by default;
- block or ask for an explicit choice before updating local config;
- never silently overwrite manifest, report, config, database, logs, imports,
  jobs, diagnostics, exports, or local-only artifacts;
- never delete, move, archive, reset, clean, or uninstall local folders in this
  issue.

Existing `MythicEdgeDev` developer data must not be migrated into
`MythicEdge` in this issue.

## Dependency Check Behavior

The setup wizard should report:

- Windows platform status;
- Git availability;
- Python executable and version compatibility with `pyproject.toml`;
- whether a virtual environment is present or can be created;
- whether required Python dependencies can be installed/imported in the
  setup-owned environment;
- Node.js availability and version compatibility with `frontend/package.json`;
- npm availability;
- whether `frontend/package-lock.json` is present for deterministic
  `npm ci`;
- backend/frontend port availability.

Missing system tools must be blockers with safe remediation text. The first
private-local-v1 wizard must not silently run system installers.

Project dependency installation is allowed only inside the managed checkout or
setup-owned virtual environment and frontend folder. Command output included in
reports must be summarized with safe status codes, not raw logs.

## SQLite Behavior

The setup wizard may initialize or verify:

```text
<install_root>\data\db\mythic_edge.sqlite3
```

Required guarantees:

- use the existing analytics migration loader;
- apply source-controlled migrations only;
- treat an empty migrated database as healthy;
- record applied migration IDs without raw SQL dumps;
- insert no parser facts, fixture rows, private data, live data, manual import
  data, or synthetic match/game rows during setup;
- keep SQLite database files and sidecar files generated/local-only and out of
  Git.

Changing analytics schema, migrations, ingest semantics, curated views, or live
fact writes is out of scope.

## Player.log Detection And Configuration Behavior

The setup wizard must configure Player.log safely and explicitly.

Allowed detection evidence:

- candidate path exists or is missing;
- candidate is a file or not a file;
- metadata access status;
- file size;
- last modified timestamp or age;
- symbolic source label, such as `detected_default`, `configured`, or
  `manual_selection`.

Forbidden detection evidence:

- raw Player.log content;
- raw log lines;
- hashes of Player.log content;
- copied or sanitized Player.log excerpts;
- persistent tail handles;
- parser event extraction during setup;
- live capture startup;
- storing Player.log payloads in SQLite, reports, issue text, screenshots, or
  committed artifacts.

Configuration rule:

- `app_config.json` may store the actual local `player_log_path` because it is
  a local-only config file required for operation.
- setup reports, install manifests, browser UI, logs, issue text, and Codex
  handoffs must use symbolic labels or redacted summaries instead of raw full
  private paths.

The setup wizard should not rely solely on a developer-specific parser default
path for private-local-v1 detection. If a generic current-user Windows MTGA
path detector is needed, implement it in setup/local-app code and keep parser
runtime defaults unchanged.

If no safe candidate exists, setup may complete as `degraded` only if the app
can still launch and the final status clearly says Player.log configuration is
required before live capture. It must not claim live capture readiness.

## Config Write And Read Behavior

### Local Config Shape

`app_config.json` should remain a simple local JSON object using currently
approved fields unless a future config contract authorizes a schema expansion:

```json
{
  "player_log_path": "<local-only actual path>",
  "analytics_database_path": "<local-only actual path, optional>",
  "backend_host": "127.0.0.1",
  "backend_port": 8765,
  "frontend_origin": "http://127.0.0.1:5173"
}
```

The setup wizard must not add secret, credential, webhook, spreadsheet, model
provider, OAuth, or external endpoint fields to this local config.

### UTF-8 And BOM Policy

Required write behavior:

- write config JSON as UTF-8 without BOM;
- use stable formatting with a trailing newline;
- create parent folders only under the approved app-data root;
- write atomically or with a temporary-file-and-replace pattern where
  practical;
- never echo config values in setup reports or frontend status payloads.

Required read behavior:

- backend config loading should defensively tolerate UTF-8 with BOM for
  existing local config files;
- BOM tolerance must not make malformed JSON look valid;
- a recovered BOM may be reported as a sanitized warning such as
  `config_bom_tolerated`;
- read-only status routes must not rewrite the config file just because a BOM
  was detected;
- the next user-approved config write should rewrite without BOM.

Malformed config behavior:

- return `invalid_json`, `invalid_shape`, `unreadable`, or equivalent stable
  codes;
- display beginner-readable remediation text;
- never include raw config contents, raw local paths, stack traces, or
  secret-like values in API responses, UI, reports, or committed artifacts.

## Backend Responsibility Boundary

The backend may:

- load setup/config/status metadata;
- tolerate UTF-8 BOM in local config reads;
- expose setup-status and config-status payloads;
- expose safe Player.log metadata/status payloads;
- accept a scoped local config write route only if Codex C proves it is needed
  for the first-run flow and it writes only approved fields;
- validate loopback host/origin values;
- keep path display symbolic or redacted.

The backend must not:

- start live capture during setup;
- tail Player.log from setup/status routes;
- read raw Player.log content from setup/status routes;
- write parser facts to SQLite during setup;
- expose destructive reset/cleanup/uninstall controls;
- expose arbitrary SQL or database browsing;
- upload reports or open external writes.

If Codex C adds a config write route, it must be loopback-only, local operator
driven, explicit, previewable, and test-covered for privacy. It must not store
secret-like fields or external endpoints.

## Frontend Responsibility Boundary

The frontend may:

- display first-run readiness after the CLI setup starts backend/frontend;
- show setup status, Player.log status, SQLite status, dependency readiness,
  and blocked/degraded next steps;
- display symbolic paths only;
- provide copyable safe commands for the approved setup wrapper;
- display that live capture requires explicit Start Capture later;
- continue to use backend status as the source of setup truth.

The frontend must not:

- infer whether Player.log is valid beyond backend status;
- infer live capture success;
- expose raw private paths;
- show raw config values;
- embed raw setup logs or stack traces;
- add destructive reset/cleanup/uninstall controls;
- auto-submit reports externally;
- start live capture automatically.

## Setup Report And Install Manifest Policy

The setup report and install manifest may include:

- release profile;
- package mode;
- release ref;
- symbolic install root, app root, and data root;
- setup mode;
- dependency readiness statuses;
- folder tree statuses;
- SQLite migration IDs and schema status;
- Player.log configuration status using symbolic labels;
- config write/read status;
- BOM recovery warning code, if applicable;
- backend/frontend launch status;
- browser-open status;
- privacy flags;
- warnings, errors, and next steps.

They must not include:

- raw full private paths when symbolic labels are enough;
- raw Player.log contents or snippets;
- private JSONL payloads;
- generated SQLite contents;
- raw SQL dumps;
- runtime logs;
- failed-post payloads;
- workbook export contents;
- stack traces with private data;
- secret values, credentials, tokens, endpoint values, spreadsheet IDs,
  environment values, or model-provider keys.

Reports are generated/local/private artifacts. They must remain out of Git.

## Public Interface

Current required compatibility:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
.\tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -JsonReport
.\tools\dev_app\setup_private_local_v1.ps1 -Proof -JsonReport
```

Future wizard behavior should remain routed through the same wrapper family
rather than adding an unrelated script unless Codex C explains a better repo
pattern.

Potential additional local-only options may include:

- `-Wizard` or equivalent interactive mode;
- `-PlayerLogPath <path>` or equivalent test/operator path input;
- `-AcceptDetectedPlayerLog` or equivalent explicit confirmation;
- `-LaunchAfterSetup` or equivalent default launch behavior;
- `-NoOpen` for validation and headless runs;
- `-JsonReport` for sanitized evidence.

Any flag that accepts a path may receive a raw local path as input, but command
echo, JSON reports, frontend display, issue comments, and test artifacts must
redact or symbolize that value.

## Error Behavior

The wizard must fail closed for:

- missing or incompatible Python;
- missing Node.js or npm;
- missing Git when clone/ref behavior is required;
- missing package manifests;
- unsafe app-data root inside a Git checkout;
- existing app-data state that requires a preservation decision;
- missing Player.log when setup requires live-ready status;
- unreadable Player.log metadata;
- selected Player.log path is not a file;
- invalid local config shape;
- malformed JSON that cannot be recovered;
- SQLite migration failure;
- backend/frontend port conflicts;
- backend/frontend launch failure.

Allowed degraded states:

- browser-open failed but backend/frontend status endpoints pass;
- Player.log not configured yet, if setup clearly labels live capture as
  blocked and local app still launches;
- live watcher stopped or unavailable, because setup must not start live
  capture;
- Match Journal database not initialized until first write, if current status
  contracts allow that state.

Error messages must be beginner-readable and must separate:

- what failed;
- whether setup preserved local data;
- what the user should do next;
- which raw/private data was not read or exposed.

## Side Effects

Codex B side effects:

- create this contract only.

Future implementation side effects, if authorized:

- create generated folders under the selected app-data root;
- write or update `app_config.json` under the selected app-data root after user
  confirmation;
- write install manifest and setup report under the selected app-data root;
- create and migrate the local analytics SQLite database;
- install project dependencies inside the managed checkout or virtual
  environment;
- start backend/frontend local loopback processes;
- open the local frontend in a browser.

Forbidden side effects:

- deleting, moving, archiving, resetting, cleaning, or uninstalling local
  folders;
- changing parser runtime behavior;
- starting live capture automatically;
- importing private data;
- external sends or uploads;
- workbook, webhook, Apps Script, Google Sheets, output transport, production,
  OpenAI/model-provider, AI/coaching, or Line Tracer behavior;
- changing system-level tools without explicit user approval.

## Dependency Order

Future implementation should proceed in this order:

1. Produce the Codex C comparison handoff against this contract.
2. Add config read tests for UTF-8 BOM tolerance and no raw value leakage.
3. Add config write helper tests for UTF-8 without BOM.
4. Add setup wizard/check/report shape tests.
5. Add Player.log metadata-only detection/confirmation tests.
6. Add app-data clean/existing-root tests.
7. Add SQLite verify/init and launch-status integration tests as needed.
8. Add frontend first-run status tests only if frontend display changes.
9. Run protected-surface and secret/private-marker scans.
10. Route to Codex E for review.

## Compatibility

- Preserve the existing private-local-v1 setup helper and wrapper commands.
- Preserve existing `MythicEdgeDev` developer-launch profile behavior.
- Preserve `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` override behavior.
- Preserve existing setup/status response fields unless adding backward
  compatible fields.
- Preserve current live capture explicit-start boundary from issue #297.
- Preserve analytics migration semantics.
- Preserve local app config allowed-field policy unless a later contract
  expands it.
- Do not change parser runtime `LOG_PATH` behavior in this issue.

## Tests Required

Focused Codex C validation should include:

```powershell
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_backend.py
```

If Codex C changes frontend first-run/status display:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
```

If frontend build creates `frontend/dist`, Codex C must remove that generated
output before handoff unless a future contract explicitly authorizes committing
it.

Hygiene checks:

```powershell
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Path-scoped scans must cover the contract, handoff, changed setup scripts,
changed backend/frontend files, and changed tests:

```powershell
@'
<changed paths>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Required new or updated test cases:

- check mode remains non-mutating;
- install mode writes config as UTF-8 without BOM;
- backend config loading tolerates UTF-8 with BOM;
- invalid JSON remains invalid and does not echo content;
- Player.log candidate detection uses metadata only;
- configured Player.log status does not expose the raw path or raw body;
- selected Player.log path that is missing, unreadable, or not a file is
  handled with stable codes;
- clean app-data root is initialized safely;
- existing app-data root preserves prior manifest/report/database/config;
- setup report and manifest use symbolic paths;
- setup does not start live capture automatically;
- backend/frontend launch proof remains loopback-only.

## Acceptance Criteria

The contract is satisfied when:

- this contract artifact exists at the expected path;
- the setup model decision is explicit;
- automatic versus user-confirmed steps are defined;
- clean and existing app-data behavior is safe;
- dependency readiness behavior is defined;
- SQLite initialization/verification is scoped to existing migrations;
- Player.log detection/configuration is metadata-only and user-confirmed;
- config write/read behavior includes UTF-8 without BOM and BOM-tolerant reads;
- backend and frontend responsibilities are bounded;
- reports/manifests avoid private data leakage;
- protected surfaces remain untouched;
- validation requirements are testable;
- Codex C has a pasteable handoff.

## Unknowns

- Whether the first Codex C pass should implement a fully interactive prompt
  or a smaller noninteractive foundation with explicit flags.
- Whether frontend first-run config editing is needed after CLI setup, or
  whether frontend status plus CLI wizard is enough for private-local-v1.
- Whether the generic current-user Windows MTGA Player.log detector should live
  in setup tooling, local app paths/status code, or a future shared helper.
- Whether dependency installation should remain proof-only or become normal
  wizard behavior before v1.0.
- Whether the default private-local-v1 flow should leave the app running or ask
  at the end of setup.

## Suspected Gaps

- No setup wizard currently writes `app_config.json`.
- No setup flow currently confirms or stores Player.log configuration for the
  user.
- Backend config reads currently use plain UTF-8 and can treat UTF-8 with BOM
  as invalid JSON.
- The current default Player.log candidate is not sufficient as a generic
  private-local-v1 detector if it remains developer-specific.
- Existing setup proof is strong for install mechanics but not yet a normal
  user first-run configuration experience.
- Browser first-run status currently displays readiness but does not replace
  setup/configuration.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
- parser payload shapes;
- match/game identity or deduplication;
- analytics schema, migrations, or ingest semantics, except applying existing
  migrations to an empty setup-owned local database;
- live parser ingest behavior;
- live watcher behavior except setup/status display that it is not started;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- CI gates;
- Pyright required/failing behavior;
- secrets, credentials, tokens, API keys, endpoint values, spreadsheet IDs, or
  environment values;
- raw Player.log files, raw local logs, private JSONL artifacts, generated
  SQLite databases or sidecar files, runtime files, failed posts, workbook
  exports, frontend build output, app-data files, or local-only artifacts.

## Out Of Scope

- public installer polish;
- public release readiness claims;
- production readiness claims;
- release tag creation;
- uninstall or destructive reinstall tooling;
- system package installation;
- automatic live capture on app launch;
- live parser fact writes as part of setup;
- manual JSONL import;
- Match Journal write smoke;
- analytics dashboard redesign;
- GitHub issue submission;
- AI/OpenAI runtime integration;
- coaching evaluation;
- Google Sheets sync;
- deployed Apps Script state;
- arbitrary SQL or database browsing.

## Codex C Implementation Scope

Codex C should:

1. confirm branch and git status;
2. inspect issue #314 and this contract;
3. compare the current setup helper, wrapper, local app config reader, setup
   status, backend routes, frontend first-run display, and focused tests;
4. produce
   `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`;
5. implement only the smallest safe setup/config slice if the comparison shows
   it is ready;
6. keep live capture, parser/runtime behavior, analytics schema changes, and
   destructive local actions out of scope;
7. route to Codex E.

Recommended smallest implementation slice:

- add UTF-8 BOM-tolerant local app config reads;
- add a setup-owned config write helper that writes UTF-8 without BOM;
- extend private-local-v1 setup to write user-confirmed `player_log_path` in
  local app config;
- add metadata-only Player.log detection/confirmation in setup tooling;
- update setup manifest/report with symbolic Player.log/config status;
- add focused tests.

If Codex C cannot implement the full wizard safely in one pass, it should still
produce the comparison handoff and route a narrower follow-up rather than
expanding into live capture or destructive setup behavior.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #314.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/setup_app_private_local_v1_installation_wizard.md

Goal:
Compare the current private-local-v1 setup helper, PowerShell wrapper, local app config reader, setup-status surfaces, backend routes, frontend first-run/status display, and focused tests against the contract. Produce docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md. Implement only the smallest safe setup/configuration slice if the comparison shows it is ready.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty files and preserve them.
- Read issue #314, tracker #136, and docs/contracts/setup_app_private_local_v1_installation_wizard.md.
- State what the setup wizard is supposed to guarantee, what current code already does, what gaps remain, and the exact minimal plan.

Recommended implementation slice:
- Make local app config reads tolerate UTF-8 with BOM while still writing config as UTF-8 without BOM.
- Add or extend setup-owned config writing for approved app_config.json fields only.
- Add metadata-only Player.log detection/confirmation behavior for setup.
- Write user-confirmed player_log_path to local app config without echoing raw paths in reports.
- Extend manifest/setup report with symbolic config and Player.log status.
- Add focused backend/setup tests and frontend tests only if frontend display changes.

Do not:
- target main;
- start live Player.log capture automatically;
- implement live parser ingest changes;
- write live parser facts to SQLite as part of setup;
- read, copy, hash, store, tail, print, or expose raw Player.log content;
- commit raw Player.log files, private JSONL artifacts, generated SQLite files, runtime logs, app-data files, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment values, frontend build output, or local-only artifacts;
- change parser behavior, parser final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest semantics, workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI/coaching behavior;
- expose destructive UI controls or arbitrary SQL/database browsing.

Validation:
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_backend.py
If frontend changes:
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
Then:
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.
Remove frontend/dist before handoff if build created it.

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- artifact produced
- observed current behavior
- gaps found
- implementation summary, if any
- files changed
- validation results
- protected-surface and secret/private-marker status
- remaining risks
- next recommended role
- workflow_handoff block routing to Codex E
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #314"
  contract_artifact: "docs/contracts/setup_app_private_local_v1_installation_wizard.md"
  target_artifact: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  decision: "Use a Windows-first CLI setup wizard followed by browser first-run status; setup may configure Player.log after user confirmation, but must not start live capture automatically."
  validation:
    - "git diff --check -- docs\\contracts\\setup_app_private_local_v1_installation_wizard.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/setup_app_private_local_v1_installation_wizard.md"
    - "path-scoped secret/private-marker scan for docs/contracts/setup_app_private_local_v1_installation_wizard.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not start live Player.log capture automatically."
    - "Do not read, copy, hash, store, tail, print, or expose raw Player.log content."
    - "Do not create or commit generated/private/local artifacts or secrets."
    - "Do not delete, move, archive, reset, clean, uninstall, or overwrite local folders."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
