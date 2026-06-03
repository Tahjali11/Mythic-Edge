# Private Local V1 Clean Checkout Install And Launch Contract-Test Report

## Findings

No blocking findings remain for the disposable live `--proof` readiness run.

The proof now demonstrates the private-local-v1 clean-checkout path in a
disposable temp root: GitHub clone, proof virtualenv creation, Python dependency
installation, proof import check, frontend `npm ci`, setup install, empty
SQLite migration, backend/frontend startup, HTTP checks, and rendered DOM smoke
all passed.

### CT-253-003 P3: full clean-install proof remains unverified

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed_for_disposable_live_proof`
- blocking_status: `not_blocking_for_next_readiness_check_but_blocking_for_default_root_install_claim`
- original_evidence:
  - Prior report versions kept the live `--proof` path deferred.
  - Live GitHub clone, real dependency installs, backend/frontend startup,
    rendered panel smoke, and default-root readiness were not yet proven.
- verification_evidence:
  - Disposable proof root was created under `<temp>\MythicEdgePrivateLocalV1Proof-...`.
  - The proof root did not exist before the run.
  - The proof root was outside this repo, outside any Git checkout, and not
    `%LOCALAPPDATA%\MythicEdge` or `%LOCALAPPDATA%\MythicEdgeDev`.
  - `powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -InstallRoot <temp_proof_root> -NoOpen -LeaveRunning -BackendPort 52398 -FrontendPort 52399 -JsonReport`
    completed with exit code 0.
  - Proof JSON status was `degraded` only because the helper correctly records
    built-in status-panel verification as `http_only`.
  - Git clone step passed.
  - Python virtualenv creation passed.
  - Python dependency installation passed.
  - Proof import check for `mythic_edge_parser`, FastAPI, and Uvicorn passed.
  - Frontend dependency installation with `npm ci` passed.
  - Setup install created the required v1 folder tree, install manifest, setup
    report, and empty migrated analytics SQLite database.
  - SQLite applied `0001_initial_analytics_schema`; table count was 31.
  - No parser fact rows were inserted; only the expected
    `parser_schema_versions` metadata row was present outside
    `schema_migrations`.
  - Backend and frontend startup passed.
  - HTTP checks passed for health, setup status, analytics database status, and
    frontend root.
  - Separate rendered DOM smoke through the Codex in-app Browser passed:
    rendered body contained Mythic Edge, Setup, Status, Import, and
    Database/SQLite surfaces; the React root had rendered children; no proof
    root marker, raw local AppData path, or stack-trace marker was present.
  - Proof-started listeners on ports 52398 and 52399 were stopped after smoke
    verification.
  - The proof clone `git status --short --untracked-files=all` was clean.
  - The main repo `git status --short --branch --untracked-files=all` remained
    clean before the report update.
- remaining_scope_limit:
  - Real default `%LOCALAPPDATA%\MythicEdge` readiness was not exercised.
  - User-facing manual install against the real machine default root remains a
    separate final readiness check.
- next_route: Codex E final/manual-install readiness check or Codex F if the
  updated report is to be submitted first.

### CT-253-005 P1: proof launch can pass on ambient Python instead of the proof virtualenv

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - The live proof dependency plan created `<proof_source_checkout>\.venv`.
  - The proof import check ran via `<venv_python>`.
  - Backend launch in the proof path used the proof virtualenv interpreter as
    verified by the earlier focused tests and the live proof startup.
- next_route: none.

### CT-253-006 P2: status-panel verification is overclaimed from HTTP checks

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - The live proof report kept `status_panel_verification` as `http_only`.
  - The live proof report included `status_panel_verification_http_only` in
    warnings and therefore reported overall status as `degraded`.
  - A separate in-app Browser rendered DOM smoke was run and passed, so this
    report does not rely on the helper's HTTP-only status as rendered-panel
    evidence.
- next_route: none.

### CT-253-001 P1: install mode could silently overwrite existing install metadata

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - Existing install state is checked before folder creation, SQLite
    initialization, and manifest/report writes.
  - The live disposable proof ran against an absent temp root and recorded
    existing install handling as `not_detected`.
- next_route: none.

### CT-253-002 P2: existing-install overwrite/mutation behavior lacked focused tests

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - Focused setup tests include existing metadata and database collision cases.
- next_route: none.

## Role Performed

Codex E: Readiness Proof Runner / Contract-Test Updater.

## Issue / Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/253
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`

Issue #253 and tracker #136 remain open.

## Contract And Handoffs Reviewed

- Contract:
  `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- Implementation handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- Fixer handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`
- Report updated:
  `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`

## Files Reviewed

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_private_local_v1_setup.py`
- `pyproject.toml`
- `frontend/package.json`
- `frontend/package-lock.json`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

This report updates the prior confirmation report with live disposable proof
evidence. It does not authorize production deployment, issue closure, tracker
closure, main targeting, or real default-root setup.

## Readiness Verdict

`ready_for_final_manual_install_readiness_check`

The disposable live proof passed. The user should not yet run a real manual
fresh install against `%LOCALAPPDATA%\MythicEdge` until a final manual-install
readiness check explicitly approves touching the real default root.

Ready for:

- final Codex E manual-install readiness check;
- Codex F submission of this updated report if the workflow wants the proof
  evidence committed first.

Not yet ready for:

- retiring or overwriting the user's current Mythic Edge folder;
- using real default `%LOCALAPPDATA%\MythicEdge`;
- issue #253 closure;
- tracker #136 closure;
- production or main targeting.

## Contract Matches

- The proof helper interface exposes `--proof` and the PowerShell wrapper
  exposes `-Proof`.
- The disposable proof root was unique, absent before the run, outside the repo,
  outside any Git checkout, and outside `%LOCALAPPDATA%\MythicEdge` and
  `%LOCALAPPDATA%\MythicEdgeDev`.
- The proof used the source-controlled wrapper/helper interface.
- GitHub clone through the live proof passed.
- Python virtualenv creation through the live proof passed.
- Python dependency installation through the live proof passed.
- Python import check through the live proof passed.
- Frontend dependency installation through `npm ci` passed.
- Setup install with initialized empty SQLite passed.
- Empty SQLite migration status was `schema_current` with
  `0001_initial_analytics_schema` applied.
- Backend and frontend startup passed.
- HTTP status checks passed.
- Rendered DOM smoke passed through the in-app Browser.
- Main repo and proof clone stayed clean.
- Proof output used symbolic paths and did not include raw paths, raw logs,
  JSONL payloads, raw SQL, secrets, API keys, provider keys, or stack traces.
- No parser behavior, analytics schema/migration semantics, workbook/webhook,
  Apps Script, Sheets, OpenAI/AI, model-provider, or production behavior change
  was observed.

## Contract Mismatches

None for the disposable live proof.

The remaining real default-root check is a readiness boundary, not a mismatch
in the disposable proof.

## Missing Tests Or Safeguards

No missing safeguard was found for the disposable proof path.

Still not performed:

- real default `%LOCALAPPDATA%\MythicEdge` install-root proof;
- user-facing manual install against the actual machine setup.

## Validation Run And Result

- `git status --short --branch --untracked-files=all` -> clean on
  `codex/analytics-foundation` before report update.
- `gh issue view 253 --comments` -> issue open; PR #255 and PR #256 merge
  comments reviewed.
- `gh issue view 136` -> tracker open.
- `py tools\dev_app\private_local_v1_setup.py --help` -> `--proof`,
  `--install-root`, `--no-open`, `--leave-running`, `--stop-after-verify`,
  `--backend-port`, `--frontend-port`, and `--json-report` present.
- Disposable root policy check -> proof root absent before run; outside repo,
  outside any Git checkout, outside `%LOCALAPPDATA%\MythicEdge`, and outside
  `%LOCALAPPDATA%\MythicEdgeDev`.
- `powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -InstallRoot <temp_proof_root> -NoOpen -LeaveRunning -BackendPort 52398 -FrontendPort 52399 -JsonReport`
  -> exit code 0; proof status `degraded` with only
  `status_panel_verification_http_only` warning.
- Proof clone -> passed.
- Python virtualenv creation -> passed.
- Python dependency install -> passed.
- Python import check -> passed.
- Frontend `npm ci` -> passed.
- Setup install -> passed.
- SQLite check -> 31 tables; `0001_initial_analytics_schema` applied; no
  parser fact rows inserted; only expected `parser_schema_versions` metadata
  row present outside `schema_migrations`.
- Backend `/api/health` -> 200, status `ok`.
- Backend `/api/app/setup-status` -> 200, symbolic paths only; no raw
  Player.log contents; live watcher/process controls disabled or deferred.
- Backend `/api/analytics/database/status` -> 200, status `ok`,
  `schema_current`.
- Frontend root -> 200.
- In-app Browser rendered DOM smoke -> passed; title
  `Mythic Edge Local Status`, rendered body length 4213, snapshot length 15059,
  React root rendered children, no proof-root marker, no raw AppData path, and
  no stack-trace marker.
- Proof-started listener cleanup -> stopped 2 listeners on ports 52398 and
  52399; remaining listener count 0.
- Proof clone `git status --short --untracked-files=all` -> clean.
- Main repo `git status --short --branch --untracked-files=all` -> clean
  before report update.
- Disposable proof root cleanup -> removed after verification; proof root no
  longer exists.
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> 8 passed.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> 62 passed, 1 existing FastAPI/Starlette warning.
- `py -m ruff check tools tests` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, 46 checked files, 0 errors,
  0 warnings.
- Path-scoped protected-surface scan over #253 files -> passed, forbidden 0,
  warnings 0.
- Path-scoped secret/private-marker scan over #253 files -> passed, forbidden
  0, warnings 0.
- Final `git status --short --branch --untracked-files=all` -> only this
  report is modified.

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0. No
protected parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/
production surface was changed. The proof exercised setup tooling, dependency
installation in the disposable clone, local generated app-data creation under
the disposable root, local backend/frontend startup, HTTP status checks, and
rendered UI smoke only.

## Secret / Private-Marker Status

The proof JSON and inspected API/UI outputs used symbolic path labels and did
not expose raw paths, raw Player.log contents, JSONL payloads, raw SQL, secrets,
credential values, API keys, provider keys, webhook URLs, spreadsheet IDs, or
stack traces.

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

## Generated Artifact Status

The proof created generated/private artifacts only under the disposable proof
root:

- `data\config\install_manifest.json`
- `data\db\mythic_edge.sqlite3`
- `data\diagnostics\setup_proof_report.json`
- `data\diagnostics\setup_report.json`
- launcher backend/frontend/log files
- cloned app checkout dependencies under the disposable `app` root

No generated proof artifacts appeared in the main repo Git status or the proof
clone Git status. The disposable proof root was removed after verification.

## Forbidden Scope

Forbidden scope was not touched. This proof did not use the real default
`%LOCALAPPDATA%\MythicEdge`, delete or retire the user's current Mythic Edge
folder, inspect private app-data, inspect raw Player.log contents, stage,
commit, push, open a PR, merge, target main, close #253, or close tracker #136.

## Recommendation

Do not tell the user to run the real manual fresh install yet.

Recommended next route:

- Codex E final manual-install readiness check before touching
  `%LOCALAPPDATA%\MythicEdge`; or
- Codex F submitter if this updated report should be committed first.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Final Manual-Install Readiness Checker for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_clean_checkout_install_launch.md

Current report:
docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md

Goal:
Perform the final readiness check before the user touches the real default
%LOCALAPPDATA%\MythicEdge install root. The disposable live --proof passed, but
real default-root/manual-install readiness is not yet approved.

Review:
- the updated #253 contract-test report;
- issue #253 and tracker #136;
- current git status;
- whether any default-root state already exists;
- whether the setup command and expected user-facing checklist are clear enough
  to run safely.

Do not use or mutate %LOCALAPPDATA%\MythicEdge unless the user explicitly
approves that final check. Do not delete, overwrite, reset, or retire the
current Mythic Edge folder. Do not close #253 or tracker #136 unless explicitly
asked and the report supports it.

Output:
- findings first;
- readiness verdict;
- whether the user may attempt manual fresh install;
- exact manual command/checklist if approved;
- remaining blockers if not approved;
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Readiness Proof Runner / Contract-Test Updater"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "E or F"
  next_role: "Codex E final manual-install readiness check, or Codex F submitter for this updated report"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  implementation_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md"
  updated_report: "docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md"
  proof_command: "powershell -ExecutionPolicy Bypass -File tools\\dev_app\\setup_private_local_v1.ps1 -Proof -InstallRoot <temp_proof_root> -NoOpen -LeaveRunning -BackendPort 52398 -FrontendPort 52399 -JsonReport"
  proof_root: "<temp>\\MythicEdgePrivateLocalV1Proof-..."
  proof_result: "degraded_only_due_to_status_panel_verification_http_only"
  rendered_dom_smoke: "passed"
  readiness_verdict: "ready_for_final_manual_install_readiness_check"
  user_manual_fresh_install_status: "not_yet_approved_for_real_default_root"
  validation:
    - "live GitHub clone through --proof -> passed"
    - "proof virtualenv creation -> passed"
    - "Python dependency installation -> passed"
    - "proof import check -> passed"
    - "frontend npm ci -> passed"
    - "setup install with empty SQLite initialization -> passed"
    - "backend/frontend startup -> passed"
    - "HTTP health/setup/database/frontend checks -> passed"
    - "in-app Browser rendered DOM smoke -> passed"
    - "proof-started listeners stopped -> passed"
    - "proof clone git status -> clean"
    - "main repo git status before report update -> clean"
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> 8 passed"
    - "adjacent setup/launcher/local-app/migration tests -> 62 passed, 1 existing warning"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  remaining_unverified:
    - "Real default %LOCALAPPDATA%\\MythicEdge readiness"
    - "User-facing manual fresh install against the actual machine setup"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  recommendation: "Run final manual-install readiness check before touching real default root."
```
