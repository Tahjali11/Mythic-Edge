# Private Local V1 Clean Checkout Install And Launch Contract-Test Report

## Findings

No blocking findings remain after Codex D confirmation.

### CT-253-001 P1: install mode could silently overwrite existing install metadata

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- original_evidence:
  - Initial Codex E reproduced that install mode could overwrite an existing
    `install_manifest.json` sentinel while `existing_install_handling` was only
    reported as deferred.
  - The contract requires no silent overwrite, no silent deletion, and no
    duplicate database creation inside the same app-data root.
- verification_evidence:
  - `tools/dev_app/private_local_v1_setup.py` now computes
    `_existing_install_handling_status(...)` before folder creation, SQLite
    initialization, or manifest/report writes.
  - If existing install state is detected in install mode, the helper adds
    `existing_install_detected`, reports `status: blocked`, and does not enter
    the write path.
  - `tests/test_private_local_v1_setup.py` now proves existing manifest/report
    sentinels are preserved and existing analytics database state is not
    migrated or mutated.
  - Focused setup tests passed: 6 passed.
- next_route: Codex F.

### CT-253-002 P2: existing-install overwrite/mutation behavior lacked focused tests

- finding_lifecycle: `fixed_state_followup`
- finding_status: `fixed`
- blocking_status: `not_blocking`
- original_evidence:
  - Initial Codex E found that focused tests covered dry-run behavior,
    Git-checkout app-data refusal, fresh temp install creation, path redaction,
    and wrapper thinness, but did not cover existing manifest/report/database
    collision behavior.
- verification_evidence:
  - Added `test_install_mode_blocks_existing_manifest_and_report_without_overwriting_metadata`.
  - Added `test_install_mode_blocks_existing_database_without_migrating_or_writing_metadata`.
  - These tests check blocked status, symbolic output, preserved sentinel
    metadata, no setup report/manifest writes in the database-collision case,
    and no migration table added to a pre-existing database.
  - Focused setup tests passed: 6 passed.
- next_route: Codex F.

### CT-253-003 P3: full clone/install/launch proof remains explicitly unverified

- finding_lifecycle: `deferred_followup`
- finding_status: `known_scope_limit`
- blocking_status: `not_blocking_for_setup_foundation`
- evidence:
  - Clone-from-GitHub clean install, virtualenv creation, dependency install,
    `npm ci`, backend/frontend startup, browser smoke, and real default
    `%LOCALAPPDATA%\MythicEdge\` readiness remain outside this foundation slice.
- interpretation:
  - This is not a current implementation mismatch. The report should route the
    setup foundation to Codex F while keeping issue #253 open unless a later
    workflow explicitly accepts or completes the full proof.
- next_route: Codex F for this reviewed setup-foundation slice; follow-up
  issue/contract for full clean-install proof.

## Role Performed

Codex E: Governance Reviewer / confirmation contract-test thread.

## Issue / Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/253
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract And Handoffs Reviewed

- Contract: `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- Codex C implementation handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- Codex D fixer handoff:
  `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`

## Files Reviewed

- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_private_local_v1_setup.py`
- `tests/test_analytics_dev_app_launcher.py`
- `pyproject.toml`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

Final approval here means no blocking findings remain for this reviewed
setup-foundation slice. It does not authorize production merge, tracker closure,
issue closure, real dependency installation, real default-root setup, live
launch, browser opening, or main targeting.

## Contract Summary

The private-local-v1 setup path must improve clean-checkout install and launch
readiness without changing parser truth, analytics schema or ingest semantics,
local app runtime behavior outside setup flow, workbook/transport behavior,
production behavior, or AI/model-provider behavior.

This reviewed slice is the setup-wizard foundation only. It must remain local,
non-destructive, path-redacted, test-root safe, and honest about unverified
clone/install/launch proof.

## Contract Matches

- `--check` mode is dry-run and did not create folders, databases, manifests,
  setup reports, start processes, install dependencies, initialize SQLite, or
  open a browser.
- Install mode now blocks existing install metadata/database state before
  folder creation, manifest/report writes, or SQLite migration.
- Existing manifest/report sentinels are preserved in focused tests.
- Existing analytics database state is not migrated or modified in focused
  tests.
- The wrapper remains thin and does not run `git clone`, `pip install`,
  `npm ci`, cleanup/delete/reset, process-launch, or browser-open commands.
- App-data roots inside the source checkout remain blocked in focused tests.
- Fresh temp install mode still writes generated folders, reserved `ai_review`
  placeholder folders, manifest, setup report, and optional empty migrated
  SQLite database only under the caller-selected install root.
- SQLite initialization uses existing analytics migrations and inserts no
  parser fact rows into `matches` or `games`.
- Manifest/report output uses symbolic paths such as `<install_root>` and did
  not include raw install-root paths in focused tests or the check-only command.
- Reserved `ai_review` folders remain storage placeholders only:
  `ai_runtime_enabled` and `external_send_allowed` are false.
- No parser behavior, parser state final reconciliation, analytics schema,
  analytics ingest semantics, local app runtime behavior outside setup flow,
  workbook/transport behavior, production behavior, or AI truth changed.

## Contract Mismatches

- None remaining for the setup-foundation slice after Codex D fixes.

## Missing Tests Or Safeguards

- No missing safeguard remains for CT-253-001 or CT-253-002.
- Full clean clone, dependency install, backend/frontend startup, browser
  proof, and actual default-root readiness remain intentionally unverified and
  should not be claimed as complete.

## Validation Run And Result

- `git status --short --branch --untracked-files=all` -> branch
  `codex/analytics-foundation`; only untracked #253 contract, handoffs, report,
  setup helper, wrapper, and focused test files were listed.
- `git diff --name-status origin/codex/analytics-foundation...HEAD` -> no
  committed branch diff; #253 files are currently untracked.
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> 6 passed.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> 62 passed, 1 existing FastAPI/Starlette warning.
- `py -m ruff check tools tests` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `py tools\dev_app\private_local_v1_setup.py --check --install-root <temp_outside_checkout> --json-report`
  -> passed; report used symbolic paths, performed no dependency install,
  SQLite init, process start, or browser open, and left the temp root absent.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over #253 touched files -> passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over #253 touched files -> passed,
  forbidden 0, warnings 0.
- Direct trailing-whitespace, final-newline, and ASCII checks for current new
  files -> passed.

## Protected-Surface Status

Protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
OpenAI/AI/coaching/production surfaces were not changed. The D fix stayed
inside repo-owned private-local-v1 setup tooling, focused tests, and the fixer
handoff.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan over the #253 touched files passed with
forbidden 0 and warnings 0. The setup command output used symbolic paths and did
not print secrets, credentials, API keys, provider keys, raw logs, private JSONL
payloads, raw SQL, stack traces, generated DB contents, or private local
artifact contents.

## Generated Artifact Status

No generated/private/local artifacts were kept. Tests used pytest temporary
directories only. The check-only setup command left the selected temp install
root absent. No SQLite DB, WAL, SHM, journal, raw log, runtime, workbook export,
or frontend build artifact was created or retained in the working tree.

## Forbidden Scope

Forbidden scope was not touched. This confirmation did not implement code,
clone repositories, install dependencies, initialize real local SQLite
databases, start long-running processes, open a browser, delete/reset/move
local folders, stage files, open a PR, merge, target main, close issue #253, or
close tracker #136.

## Recommendation

Approve this reviewed setup-foundation slice for Codex F submission.

Keep issue #253 and tracker #136 open unless a later workflow explicitly covers
or accepts the remaining clean clone/install/launch proof.

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
- tests/test_private_local_v1_setup.py

Codex E confirmation result:
No blocking findings remain for the setup-foundation slice. CT-253-001 and
CT-253-002 are verified fixed. CT-253-003 remains a deferred scope limit for
full clean clone/install/launch proof and should not be claimed as complete.

Submitter task:
- Inspect git status and identify unrelated changes.
- Stage only the reviewed #253 files listed above.
- Commit with a concise #253 setup-foundation message.
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

Validation already confirmed by Codex E:
- focused setup pytest -> 6 passed
- adjacent launcher/backend/config/migration pytest -> 62 passed, 1 existing warning
- ruff tools/tests and src/tests/tools -> passed
- setup --check JSON report -> passed and left temp root absent
- git diff --check -> passed
- agent docs check -> passed
- path-scoped protected-surface scan -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0
- direct whitespace/final-newline/ASCII checks -> passed
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Governance Reviewer / confirmation contract-test thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  implementation_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md"
  target_artifact: "docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md"
  fixed_findings_verified:
    - "CT-253-001 P1: install mode blocks existing install metadata/database state before writes."
    - "CT-253-002 P2: focused existing-install overwrite/mutation tests exist and pass."
  deferred_findings:
    - "CT-253-003 P3: full clone/install/launch proof remains explicitly unverified."
  validation:
    - "py -m pytest -q tests\\test_private_local_v1_setup.py -> 6 passed"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py tests\\test_analytics_migration_loader.py -> 62 passed, 1 existing warning"
    - "py -m ruff check tools tests -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "setup --check JSON report -> passed and left temp root absent"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "direct whitespace/final-newline/ASCII checks -> passed"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  recommendation: "Route to Codex F for submitter handling of the reviewed setup-foundation slice; keep #253 and #136 open."
```
