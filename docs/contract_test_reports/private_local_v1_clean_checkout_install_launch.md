# Private Local V1 Clean Checkout Install And Launch Contract-Test Report

## Findings

No blocking findings remain for the reviewed Codex D proof-orchestration fix
slice.

### CT-253-005 P1: proof launch can pass on ambient Python instead of the proof virtualenv

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- original_evidence:
  - Proof mode created and installed into `<proof_source_checkout>\.venv`, but
    delegated backend startup to the normal launcher command builder, which
    selected ambient `py` when available.
  - The focused tests did not previously assert the backend process command
    used the proof virtualenv interpreter.
- verification_evidence:
  - `tools/dev_app/private_local_v1_setup.py` now adds a proof virtualenv import
    check using `<venv_python> -c "import mythic_edge_parser, fastapi, uvicorn"`.
  - Proof launch now passes `backend_python=str(proof_python)` into
    `launcher.build_config(...)`.
  - `tools/dev_app/dev_app_launcher.py` now supports an optional internal
    `backend_python` override and preserves ambient Python behavior when the
    override is absent.
  - Focused tests assert existing-checkout and clone-mode proof backend
    commands begin with the expected proof virtualenv Python path.
  - `py -m pytest -q tests\test_private_local_v1_setup.py` passed: 8 passed.
- next_route: Codex F for the reviewed fix slice.

### CT-253-006 P2: status-panel verification is overclaimed from HTTP checks

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- original_evidence:
  - Proof mode marked `status_panel_verification` as `passed` when only loopback
    HTTP checks had run.
  - No browser-rendered setup/status panel evidence was produced.
- verification_evidence:
  - Proof mode now records `status_panel_verification` as `http_only` after
    successful HTTP checks.
  - Proof mode appends `status_panel_verification_http_only` to warnings, so the
    proof result is degraded rather than overclaimed as fully passed.
  - Focused tests assert both the durable proof report and setup report carry
    the `http_only` value.
  - `py -m pytest -q tests\test_private_local_v1_setup.py` passed: 8 passed.
- next_route: Codex F for the reviewed fix slice.

### CT-253-004 P1: manual orchestration blocker

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed_for_repo_owned_proof_orchestration`
- blocking_status: `not_blocking_for_codex_f`
- verification_evidence:
  - `--proof` and `-Proof` now exist.
  - Proof mode owns clone/source selection, dependency command construction,
    setup install, backend/frontend launch orchestration, HTTP checks, and
    cleanup hooks.
  - CT-253-005 and CT-253-006 are verified fixed in this confirmation pass.
- remaining_scope_limit:
  - This does not prove user manual fresh-install readiness. Live proof,
    rendered panel smoke, and default-root readiness remain unverified.
- next_route: Codex F for the reviewed fix slice.

### CT-253-001 P1: install mode could silently overwrite existing install metadata

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - Existing install state is checked before folder creation, SQLite
    initialization, and manifest/report writes.
  - Focused tests preserve existing manifest/report and existing database state.
- next_route: none.

### CT-253-002 P2: existing-install overwrite/mutation behavior lacked focused tests

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- verification_evidence:
  - Focused setup tests include existing metadata and database collision cases.
- next_route: none.

### CT-253-003 P3: full clean-install proof remains unverified

- finding_lifecycle: `deferred_followup`
- finding_status: `known_scope_limit`
- blocking_status: `not_blocking_for_codex_f_but_blocking_for_manual_fresh_install_claim`
- verification_evidence:
  - Prior Codex E disposable manual proof verified clone, virtualenv,
    dependency install, `npm ci`, setup install, empty SQLite migration,
    backend/frontend HTTP availability, and generated artifact cleanup.
  - The current repo-owned proof command now has safer orchestration and no
    longer overclaims rendered-panel proof.
- remaining_unverified:
  - live GitHub clone through `--proof`;
  - real dependency installs through `--proof`;
  - real backend/frontend/browser proof through `--proof`;
  - rendered setup/status panel DOM smoke;
  - real default `%LOCALAPPDATA%\MythicEdge` readiness.
- next_route: Codex F for the reviewed implementation slice; later Codex E
  readiness proof before telling the user to attempt manual fresh install.

## Role Performed

Codex E: Module Reviewer / confirmation thread.

## Issue / Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/253
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`

Issue #253 and tracker #136 remain open.

## Contract And Handoffs Reviewed

- Contract:
  `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- Prior implementation handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- Fixer handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`
- Review artifact updated:
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

## Report Lifecycle

`report_lifecycle`: `final_approval`

Final approval here means no blocking findings remain for the reviewed
proof-orchestration fix slice. It does not authorize production merge, tracker
closure, issue closure, real default-root setup, real manual fresh install,
browser/DOM readiness claims, or main targeting.

## Readiness Verdict

`not_ready_for_user_manual_fresh_install`

`ready_for_codex_f_for_reviewed_proof_orchestration_slice`

Ready for:

- Codex F submitter handling of the reviewed #253 proof-orchestration slice.

Not ready for:

- user manual fresh install;
- retiring or overwriting the user's current Mythic Edge folder;
- real default `%LOCALAPPDATA%\MythicEdge` setup;
- issue #253 closure;
- tracker #136 closure.

## Contract Matches

- Focused setup tests pass with 8 tests.
- `--proof` exists in `tools/dev_app/private_local_v1_setup.py`.
- `-Proof` exists in `tools/dev_app/setup_private_local_v1.ps1`.
- `--check` remains non-mutating in direct smoke validation and left the temp
  install root absent.
- Install mode still blocks existing manifest/report/database state before
  writes.
- Fake-runner proof tests avoid real GitHub clone, dependency installation,
  long-running backend/frontend processes, browser open, and real default
  `%LOCALAPPDATA%\MythicEdge` use.
- Proof backend launch now uses the proof virtualenv Python via the
  contract-owned `backend_python` override.
- Proof dependency status includes a virtualenv import check for
  `mythic_edge_parser`, FastAPI, and Uvicorn.
- HTTP-only proof no longer claims rendered-panel verification; it records
  `http_only` and produces a warning/degraded proof status.
- Proof output paths and command shapes are symbolic/redacted.
- No parser behavior, analytics schema/migration semantics, workbook/webhook,
  Apps Script, Sheets, OpenAI/AI, or production behavior changes were observed.

## Contract Mismatches

None remaining for the reviewed proof-orchestration fix slice.

Remaining full-issue readiness gaps are recorded under CT-253-003 as deferred
proof work, not current implementation mismatches.

## Missing Tests Or Safeguards

No missing focused safeguard remains for CT-253-005 or CT-253-006.

Still not performed in this confirmation thread:

- live `--proof` run;
- real dependency installs through `--proof`;
- real backend/frontend/browser proof through `--proof`;
- rendered setup/status panel DOM smoke;
- real default-root readiness proof.

## Validation Run And Result

- `git status --short --branch --untracked-files=all` -> on
  `codex/analytics-foundation`, with modified #253 report/handoff/helper/
  launcher/wrapper/test files only.
- `gh issue view 253 --comments` -> issue open; prior readiness comments
  reviewed.
- `gh issue view 136` -> tracker open.
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> 8 passed.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> 62 passed, 1 existing FastAPI/Starlette warning.
- `py -m ruff check tools tests` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report`
  -> passed; temp root absent.
- `git diff --check` -> passed, with the expected Windows line-ending notice
  for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py` -> passed, 46 checked files, 0 errors,
  0 warnings.
- Path-scoped protected-surface scan over touched #253 files -> passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over touched #253 files -> passed,
  forbidden 0, warnings 0.

## Protected-Surface Status

Protected-surface scan passed. No parser behavior, parser state final
reconciliation, parser event classes, match/game identity, deduplication,
analytics schema or migration semantics, analytics ingest semantics, workbook
schema, webhook payload shape, Apps Script behavior, Google Sheets behavior,
output transport, production behavior, OpenAI/model-provider behavior,
AI/coaching behavior, Line Tracer behavior, or truth ownership change was
observed.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.
The review did not ask for, store, print, or modify secrets, credentials,
tokens, webhook URLs, spreadsheet IDs, API keys, environment values, or LLM
provider keys.

## Generated Artifact Status

The direct `--check` smoke left its temp root absent. No live `--proof` run was
performed in this review. Git status shows no generated SQLite databases,
runtime files, raw logs, frontend build output, dependency folders, workbook
exports, or local-only artifacts added to the repo.

## Forbidden Scope

Forbidden scope was not touched. This review did not use real default
`%LOCALAPPDATA%\MythicEdge`, delete or retire the user's current Mythic Edge
folder, inspect private app-data, inspect raw Player.log contents, stage,
commit, push, open a PR, merge, target main, close #253, or close tracker #136.

## Recommendation

Route to Codex F for the reviewed proof-orchestration slice.

Keep issue #253 and tracker #136 open. Do not tell the user to attempt a manual
fresh install yet.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Reviewed artifacts:
- docs/contracts/private_local_v1_clean_checkout_install_launch.md
- docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md
- docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md
- docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md

Reviewed implementation files:
- tools/dev_app/private_local_v1_setup.py
- tools/dev_app/setup_private_local_v1.ps1
- tools/dev_app/dev_app_launcher.py
- tests/test_private_local_v1_setup.py

Codex E confirmation result:
No blocking findings remain for the reviewed proof-orchestration slice.
CT-253-005 and CT-253-006 are verified fixed. CT-253-003 remains a deferred
scope limit: live --proof execution, rendered panel DOM smoke, and real default
%LOCALAPPDATA%\MythicEdge readiness are not yet proven.

Submitter task:
- Inspect git status and identify unrelated changes.
- Stage only the reviewed #253 files listed above.
- Commit with a concise #253 proof-orchestration message.
- Push the branch.
- Open or update a draft PR targeting codex/analytics-foundation unless current
  workflow authority names a different non-main integration target.
- Link issue #253 and tracker #136.
- Do not close issue #253 or tracker #136.

Do not target main, merge, close issues, install dependencies, clone
repositories, initialize real local SQLite databases, start long-running
processes, open a browser, delete/reset/move local folders, create generated or
private local artifacts, change parser behavior, change analytics
schema/migrations/ingest semantics, change local app runtime behavior outside
setup flow, change workbook/transport/production behavior, or implement AI
runtime/model-provider behavior.
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  implementation_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md"
  updated_report: "docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md"
  readiness_verdict: "not_ready_for_user_manual_fresh_install"
  codex_f_status: "ready_for_codex_f_for_reviewed_proof_orchestration_slice"
  fixed_findings_verified:
    - "CT-253-005 P1: proof backend launch now uses the proof virtualenv Python."
    - "CT-253-006 P2: HTTP-only checks now report status_panel_verification as http_only, not passed."
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> 8 passed"
    - "adjacent setup/launcher/local-app/migration tests -> 62 passed, 1 existing warning"
    - "py -m ruff check tools tests -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "private_local_v1_setup.py --check smoke -> passed, temp root absent"
    - "git diff --check -> passed, Windows line-ending notice only"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  remaining_unverified:
    - "Live GitHub clone through --proof"
    - "Real dependency installs through --proof"
    - "Real backend/frontend/browser proof through --proof"
    - "Rendered status-panel/browser DOM smoke"
    - "Real default %LOCALAPPDATA%\\MythicEdge readiness"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  recommendation: "Route to Codex F for this reviewed slice; keep #253 and #136 open."
```
