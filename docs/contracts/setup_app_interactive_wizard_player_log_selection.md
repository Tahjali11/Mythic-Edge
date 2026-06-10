# Setup App Interactive Wizard Player.log Selection Contract

## Module

`setup_app_interactive_wizard_player_log_selection`

Plain English: this contract defines the next private-local-v1 setup slice: an
interactive first-run wizard that lets a local operator configure Mythic Edge
and select an MTGA `Player.log` without hand-editing JSON.

This is a Codex B contract-writing artifact only. It does not implement setup
code, backend routes, frontend behavior, parser behavior, analytics behavior,
workbook transport, OpenAI/model-provider behavior, or production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/317
- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Release-readiness tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Prior foundation PR: https://github.com/Tahjali11/Mythic-Edge/pull/316
- Prior merge commit: `76f633c11ede3230b064cd4fdce01664f3cacac6`
- Branch/worktree:
  `codex/setup-app-interactive-wizard-player-log-314`

Required authority and role docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 must remain open after this contract. Issue #314 also remains open
unless a later deployer thread verifies the broader setup/wizard queue is fully
satisfied.

## Risk Tier

Medium-High.

Reasons:

- the wizard writes local app config;
- it may create generated app-data folders and initialize SQLite through
  existing migrations;
- it handles a private local `Player.log` path;
- it sits beside live-capture readiness but must not start capture;
- reports, manifests, console output, and tests can accidentally leak private
  paths or raw local artifacts if not designed carefully.

## Owning Layer

Primary owner: Local App / UI setup tooling.

Supporting owners:

- Quality / Governance release readiness;
- Generated / Local Artifacts;
- Analytics, only for applying existing migrations to an empty local SQLite
  database;
- Parser, reference-only for `Player.log` and parser truth boundaries.

## Internal Project Area

Local App / UI.

Supporting areas:

- Quality / Governance;
- Generated / Local Artifacts;
- Analytics.

## Truth Owner

The setup wizard owns local setup readiness and config-writing orchestration
only.

Truth ownership remains unchanged:

- MTGA `Player.log` remains the raw observable source.
- Parser/state owns event interpretation, match/game identity, deduplication,
  final reconciliation, and parser-normalized facts.
- Analytics migrations own SQLite schema history.
- SQLite is downstream analytics storage, not parser truth.
- The local app owns setup/status display and local operator workflow.
- Install manifests and setup reports own setup evidence only.

The wizard, local config file, setup report, install manifest, backend status,
and frontend status must not become parser truth, analytics truth, workbook
truth, production truth, AI truth, or deployment authority.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
operator choices + local toolchain metadata + setup defaults
  -> setup PowerShell wrapper / Python setup helper
  -> generated app-data folders, local config, setup report, install manifest
  -> backend/frontend read-only setup status
```

Forbidden reverse flow:

- setup output must not change parser behavior;
- setup output must not change analytics schema, migrations, or ingest
  semantics except applying already-existing migrations to an empty local DB;
- setup output must not start live capture;
- frontend status must not infer parser-owned facts or capture success;
- backend/frontend config editing must not be added by this slice unless this
  contract is amended.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`

Expected future Codex C artifact:

- `docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md`

Expected future Codex E artifact:

- `docs/contract_test_reports/setup_app_interactive_wizard_player_log_selection.md`

Future Codex C may change only scoped setup surfaces such as:

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `src/mythic_edge_parser/local_app/config.py`, only if comparison shows the
  wizard needs a narrow shared helper and existing config guarantees remain
  intact;
- `tests/test_analytics_local_app_config.py`, only for config helper coverage;
- local app backend/frontend tests only when validating unchanged read-only
  setup/status behavior.

Future Codex C must not add browser config editing or a backend config write
route in this slice. If implementation discovers that a browser-first config
write path is required, route back to Codex B with a contract amendment.

## Observed Current Behavior

PR #316 completed the noninteractive setup/config foundation:

- `tools/dev_app/private_local_v1_setup.py` supports check, install, and proof
  modes;
- `--player-log-path` can write approved local config fields during install;
- selected `Player.log` validation is metadata-only;
- missing, not-file, and metadata-unreadable selected paths block before
  config write;
- config writes use UTF-8 without BOM;
- config reads tolerate UTF-8 with BOM;
- generated app-data folder creation is supported;
- SQLite can be initialized through existing migrations;
- setup reports and manifests use symbolic path labels;
- existing `app_config.json`, setup report, manifest, app checkout, generated
  data, or SQLite DB state blocks install and is preserved;
- no live capture auto-start was added;
- no interactive wizard prompt path exists yet;
- no setup-flow generic Windows current-user `Player.log` detection exists yet;
- no backend config write route exists.

The current backend exposes read-only setup/config/status endpoints. It must
remain read-only for this issue.

## Contract Decision

The first implementation slice must be a Windows-first CLI wizard routed
through the existing PowerShell wrapper and Python setup helper.

Decision:

- Add explicit CLI wizard mode.
- Add equivalent PowerShell wrapper support.
- Reuse the existing setup helper and config writer.
- Keep browser/backend config write routes out of scope.
- Keep frontend changes out of scope unless Codex C needs to verify existing
  read-only setup/status display remains compatible.

Rationale:

- CLI setup can safely run before backend/frontend are available.
- Existing setup code already owns folder creation, SQLite initialization,
  config writes, and symbolic reports.
- A backend write route would widen external-write and browser-facing risk
  before the CLI path is proven.

## Public Interface

Approved new setup interfaces:

- Python CLI flag: `--wizard`
- PowerShell wrapper switch: `-Wizard`

Approved existing interfaces to preserve:

- `--check`
- `--install`
- `--proof`
- `--install-root`
- `--source-checkout`
- `--initialize-sqlite`
- `--player-log-path`
- `--release-ref`
- `--repo-url`
- `--no-open`
- `--leave-running`
- `--stop-after-verify`
- `--backend-port`
- `--frontend-port`
- `--json-report`
- PowerShell equivalents already present in
  `tools/dev_app/setup_private_local_v1.ps1`

Recommended wizard entrypoints:

```powershell
.\tools\dev_app\setup_private_local_v1.ps1 -Wizard
.\tools\dev_app\setup_private_local_v1.ps1 -Wizard -JsonReport
py tools\dev_app\private_local_v1_setup.py --wizard
```

Codex C may choose to make `--wizard` imply install mode and SQLite
initialization, or require `--wizard --install --initialize-sqlite`, but the
chosen behavior must be explicit in help text and tests. Recommended behavior:
`--wizard` implies the private-local-v1 install flow and SQLite initialization
after final user confirmation.

The wizard implementation should expose prompt logic through testable functions
or an injected prompt/input abstraction so tests do not need a real terminal.

## Wizard UX Flow

The wizard must be short, explicit, and beginner-safe:

1. Welcome and release-profile summary.
2. State privacy boundaries: metadata-only `Player.log` validation, no raw log
   reads, no live capture auto-start.
3. Resolve default private-local-v1 install root:
   `%LOCALAPPDATA%\MythicEdge`.
4. Ask the user to accept the default root or enter an alternate root.
5. Validate the source checkout and app-data-root policy.
6. Detect existing install/config/generated state.
7. Preview planned generated folders and SQLite initialization.
8. Detect the default Windows MTGA `Player.log` candidate using metadata only.
9. Ask the user to confirm the detected candidate, enter a manual path, skip
   `Player.log` for degraded setup, or cancel.
10. Validate any selected path using metadata only.
11. Present a final summary before writing anything.
12. Run the existing install/setup path only after explicit confirmation.
13. Print a final `healthy`, `degraded`, or `blocked` result with next command
    guidance.

The wizard must not require users to hand-edit JSON, know internal app-data
subfolders, or run one-off PowerShell snippets.

## Player.log Detection And Selection

Default Windows candidate:

```text
%USERPROFILE%\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log
```

The setup-flow detector may live in setup tooling or a local-app helper. It
must not change parser runtime defaults.

Allowed metadata fields:

- exists: boolean
- path_kind: `file`, `directory`, `missing`, or `unknown`
- metadata_access: `accessible`, `denied`, `unavailable`, or `not_checked`
- size_bytes: integer or null
- last_modified_at: ISO timestamp or null
- last_modified_age_seconds: number or null
- activity_hint: `recent`, `stale`, or `unknown`

Required source labels:

- `detected_default` for the standard Windows candidate;
- `manual_selection` for a user-entered path;
- `not_provided` when the user skips selection.

Required display labels in reports/manifests:

- `<detected_mtga_player_log>`
- `<selected_player_log>`
- `<player_log_not_configured>`

Rules:

- Do not read, copy, hash, tail, summarize, or store raw `Player.log` contents.
- Do not store raw `Player.log` payloads or raw log lines in SQLite.
- Detected candidates must be user-confirmed before config write.
- Manual paths must be metadata-validated before config write.
- Missing, directory, or metadata-unreadable selected paths must block config
  write for that path.
- If no accepted `Player.log` is selected, the wizard may complete degraded
  setup for folders/SQLite/config status, but it must clearly say live capture
  is not ready.
- The wizard must not auto-start live capture after accepting a path.

## Config Write Boundary

The wizard may write local app config only through the existing approved config
writer.

Allowed fields for this slice:

- `player_log_path`, only after user-confirmed accepted file metadata;
- `analytics_database_path`, pointing to the private-local-v1 generated DB path.

Forbidden config writes:

- secrets;
- credentials;
- API keys;
- tokens;
- webhook URLs;
- spreadsheet IDs;
- model-provider settings;
- environment variable values;
- arbitrary user-supplied keys;
- backend/frontend host or port changes unless Codex C shows the existing setup
  helper already needs them and they remain loopback-only.

Config write guarantees:

- UTF-8 without BOM;
- approved fields only;
- no raw config values included in setup report or install manifest;
- no overwrite of existing `app_config.json` in the first slice.

## Existing Install And Config Preservation

Clean app-data root:

- wizard may create the generated private-local-v1 folder tree;
- wizard may initialize an empty analytics SQLite database with existing
  migrations;
- wizard may write first-run local config after final confirmation.

Existing generated/private state:

- wizard must detect and preserve it;
- wizard must default to blocking/canceling rather than overwriting;
- wizard may offer "choose another install root" or "exit and review existing
  install";
- wizard must not delete, move, rename, archive, reset, sanitize, copy, or
  repair existing local files.

Existing config:

- no overwrite in this slice;
- no merge/update mode in this slice;
- no config key deletion in this slice;
- future update/repair behavior requires a separate issue or contract
  amendment.

## SQLite And App-Data Verification Boundary

Allowed:

- create generated private-local-v1 folders under the selected install root;
- apply existing analytics migrations to initialize an empty SQLite DB;
- verify migration inventory and database status;
- report symbolic DB and app-data labels.

Forbidden:

- analytics schema or migration changes;
- parser fact ingestion during setup;
- live parser fact writes during setup;
- manual JSONL import during setup;
- raw `Player.log` storage;
- committing generated SQLite, WAL, SHM, journal, app-data, runtime, or log
  files.

## Backend, Frontend, And Setup Boundaries

Setup tooling:

- owns the wizard prompts and config write.
- may call existing setup functions.
- may produce sanitized console summary, JSON report, manifest, and setup
  report.

Backend:

- remains read-only for setup/config in this slice.
- may be used only for status verification if existing endpoints support it.
- must not gain a config write route from this issue.

Frontend:

- remains a read-only status/display consumer for this issue.
- must not gain browser config editing from this issue.
- must not infer parser truth, capture success, match completion, or live
  readiness beyond backend-provided sanitized status.

## Inputs

Wizard input sources:

- command-line flags;
- PowerShell wrapper parameters;
- terminal prompt answers;
- local environment metadata such as `LOCALAPPDATA` and `USERPROFILE`;
- filesystem metadata for candidate paths;
- existing repo markers;
- existing setup helper configuration defaults.

User-entered raw paths are allowed as input to the local wizard, but durable
reports, manifests, JSON output, test assertions, and backend/frontend payloads
must use symbolic labels rather than echoing raw private paths.

## Outputs

Allowed outputs:

- terminal setup summary;
- process exit code;
- sanitized JSON report when `--json-report` is used;
- generated app-data folder tree;
- empty/current local SQLite database;
- `app_config.json` with approved fields only;
- install manifest;
- setup report;
- implementation handoff and later review report.

Required result labels:

- `healthy`: setup completed, config written, SQLite initialized or verified,
  and selected `Player.log` metadata accepted.
- `degraded`: app-data/SQLite setup completed, but no accepted `Player.log`
  was configured or a non-blocking launch/status check could not be completed.
- `blocked`: setup must not write config or proceed because a selected path,
  source checkout, app-data policy, existing install, migration inventory, or
  write prerequisite failed.

## Invariants

- `--wizard` / `-Wizard` must be explicit.
- No live capture starts automatically.
- No raw `Player.log` contents are read, copied, hashed, tailed, printed, or
  stored.
- Selected `Player.log` path must be user-confirmed before config write.
- Missing/not-file/unreadable selected paths block that path from config write.
- Existing config/install artifacts are preserved and not overwritten.
- SQLite initialization uses existing migrations only.
- Config writes are UTF-8 without BOM and approved-field-only.
- Durable reports use symbolic path labels.
- Backend config write routes remain out of scope.
- Parser/runtime, analytics schema/ingest, workbook/webhook/App Script/Sheets,
  OpenAI/AI/coaching, Line Tracer, and production behavior remain unchanged.

## Error Behavior

Missing `LOCALAPPDATA`:

- block unless `--install-root` is provided.

Invalid source checkout:

- block before folder creation or config write.

App-data root inside a repo/Git checkout:

- block before folder creation or config write.

Existing install/config/generated state:

- block and preserve existing files.

Detected default `Player.log` missing:

- offer manual path entry, skip/degraded setup, or cancel.

Selected manual path missing, directory, or metadata-unreadable:

- do not write it to config;
- allow retry, skip/degraded setup, or cancel;
- never read contents to diagnose.

User cancellation:

- exit cleanly without partial config writes beyond any explicitly completed
  pre-confirmation read-only checks.

Prompt ambiguity or non-interactive terminal:

- fail with actionable guidance or require explicit noninteractive flags;
- do not guess a private path and write it silently.

## Side Effects

Allowed side effects after final user confirmation:

- create generated private-local-v1 folders;
- initialize empty/current SQLite database using existing migrations;
- write `app_config.json` with approved fields only;
- write sanitized install manifest and setup report.

Forbidden side effects:

- live capture start;
- live parser ingest;
- parser fact writes;
- Google Sheets/webhook/App Script transport;
- external network writes except existing setup/proof dependency behavior already
  controlled by the prior setup foundation;
- config overwrite/repair/reset;
- destructive uninstall, cleanup, deletion, archiving, renaming, or moving.

## Dependency Order

Implementation should proceed in this order:

1. Add testable wizard prompt/decision helpers.
2. Add setup-flow default Windows `Player.log` candidate metadata detection.
3. Add Python CLI `--wizard` behavior.
4. Add PowerShell `-Wizard` pass-through.
5. Reuse existing setup install/config write path.
6. Add focused wizard tests.
7. Verify existing setup/config/backend status tests still pass.
8. Write Codex C implementation handoff.

## Compatibility

Must preserve:

- existing `--check`, `--install`, and `--proof` behavior;
- existing `--player-log-path` noninteractive behavior;
- existing setup report and manifest redaction guarantees;
- existing config read/write guarantees;
- existing backend read-only config/status endpoints;
- existing tests from PR #316.

The wizard may add report fields only additively. Existing consumers must not
need to change unless Codex C documents an intentional additive schema version
or field addition.

## Tests Required

Required focused tests:

```powershell
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Required behavior coverage:

- `--wizard` routes through the intended install/setup path.
- `-Wizard` passes through from the PowerShell wrapper.
- Wizard accepts a metadata-valid detected default only after explicit
  confirmation.
- Wizard accepts a metadata-valid manual path only after explicit confirmation.
- Missing detected default can continue as degraded without config write for
  `player_log_path`.
- Missing manual path blocks that path before config write.
- Directory path blocks before config write.
- Metadata-denied path blocks before config write.
- Existing `app_config.json` blocks and remains byte-for-byte unchanged.
- Existing setup report/manifest/database/app checkout state blocks and is
  preserved.
- JSON report, manifest, setup report, and test output do not include raw
  private paths or raw `Player.log` contents.
- Config write remains UTF-8 without BOM.
- SQLite initialization remains existing-migration-only.
- No test starts live capture.

Required path-scoped scans over changed files:

```powershell
@'
<changed files>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed files>
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

If Codex C changes frontend files, it must also run the focused frontend tests
and remove generated build output before handoff:

```powershell
npm --prefix frontend test -- --run
npm --prefix frontend run build
```

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/setup_app_interactive_wizard_player_log_selection.md`.
- CLI wizard mode exists behind explicit `--wizard` and wrapper `-Wizard`.
- First implementation does not add a backend config write route.
- First implementation does not add browser config editing.
- Wizard detects the default Windows MTGA `Player.log` candidate using metadata
  only.
- Wizard lets the user confirm detected `Player.log`, enter a manual path, skip
  `Player.log` for degraded setup, or cancel.
- Config write occurs only for user-confirmed metadata-accepted file paths.
- Existing install/config state is preserved and not overwritten.
- Empty SQLite initialization uses existing migrations only.
- Reports/manifests/status output remain symbolic and redacted.
- No live capture starts automatically.
- Focused tests and scans pass.

## Unknowns And Contract Risks

- Real current-user MTGA install layouts can vary; this contract authorizes only
  the standard Windows candidate and manual selection, not a broad filesystem
  search.
- Console prompts may need to display user-entered paths for confirmation. This
  is acceptable in the local terminal only; durable reports and payloads must
  stay symbolic.
- Existing install update/repair is intentionally deferred. Users with a prior
  app-data root may need a follow-up issue for safe migration.
- Browser first-run config editing remains deferred. If user experience demands
  it, create a separate backend/frontend config-write contract.

## Protected Surfaces

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migration definitions, or ingest semantics;
- live capture behavior;
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
- Pyright gate behavior;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment variable contracts.

Do not commit or expose:

- raw `Player.log` files or contents;
- private JSONL artifacts;
- generated SQLite, WAL, SHM, or journal files;
- runtime logs;
- app-data files;
- failed posts;
- workbook exports;
- generated frontend build output;
- local-only artifacts.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/317

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch/worktree:
codex/setup-app-interactive-wizard-player-log-314

Contract:
docs/contracts/setup_app_interactive_wizard_player_log_selection.md

Target handoff artifact:
docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md

Goal:
Compare the current setup/config foundation against the contract, then implement
the smallest CLI wizard slice for private-local-v1 interactive setup and
Player.log selection.

Before editing:
- Confirm branch is codex/setup-app-interactive-wizard-player-log-314.
- Inspect git status and preserve unrelated changes.
- Read the contract, issue #317, parent issue #314, PR #316, and the current
  setup/config helper tests.
- State the exact minimal implementation plan.

Implement:
- explicit Python CLI `--wizard` mode or an equivalent contract-matched flag;
- PowerShell wrapper `-Wizard` pass-through;
- testable wizard prompt/decision helpers;
- metadata-only default Windows Player.log candidate detection;
- user confirmation or manual path entry before config write;
- degraded setup path when Player.log is skipped;
- preservation of existing install/config blockers;
- sanitized reports/manifests with symbolic labels only.

Do not:
- add a backend config write route;
- add browser config editing;
- start live capture automatically;
- read, copy, hash, tail, print, store, or commit raw Player.log contents;
- change parser behavior, parser final reconciliation, event classes,
  match/game identity, deduplication, analytics schema/migrations/ingest,
  workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI
  behavior;
- overwrite, delete, move, archive, reset, or repair existing local app-data;
- target main;
- close #317, #314, or #136;
- stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed
files.

Final output:
- role performed
- issue/parent/tracker
- branch and git status
- contract used
- implementation handoff produced
- files changed
- what current behavior already matched
- what was implemented
- what remains deferred
- validation run and result
- protected-surface and secret/private-marker scan results
- next recommended role: Codex E
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/317"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #317"
  target_artifact: "docs/implementation_handoffs/setup_app_interactive_wizard_player_log_selection_comparison.md"
  contract_artifact: "docs/contracts/setup_app_interactive_wizard_player_log_selection.md"
  risk_tier: "Medium-High"
  branch: "codex/setup-app-interactive-wizard-player-log-314"
  decision: "First implementation slice is Windows-first CLI wizard plus PowerShell wrapper support; backend config write route and browser config editing are deferred."
  validation:
    - "git diff --check -- docs\\contracts\\setup_app_interactive_wizard_player_log_selection.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract file"
    - "path-scoped secret/private-marker scan over contract file"
  stop_conditions:
    - "Do not implement backend config write routes or browser config editing in issue #317."
    - "Do not start live capture automatically."
    - "Do not read, copy, hash, tail, print, store, or expose raw Player.log contents."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not overwrite, delete, move, archive, reset, or repair existing local app-data."
    - "Do not target main."
```
