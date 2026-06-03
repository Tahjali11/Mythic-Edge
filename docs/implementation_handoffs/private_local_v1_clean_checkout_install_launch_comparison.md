# Private Local V1 Clean Checkout Install And Launch Implementation Comparison

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
