# Private Local V1 Clean Checkout Install And Launch Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/253

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/private_local_v1_clean_checkout_install_launch.md`

## Review Artifact

`docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`

## Prior Implementation Handoff

`docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`

## Repo Authority Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_fixer.md`

## Internal Project Area

Quality / Governance release readiness, with supporting Local App / UI,
Generated / Local Artifacts, and Analytics setup surfaces.

## Truth Owner

The setup foundation owns install and launch readiness evidence only. Parser
truth, analytics fact truth, workbook truth, Match Journal truth, AI truth, and
production truth remain unchanged.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer.

## Source Finding

- CT-253-001 P1: install mode can silently overwrite existing install metadata.
- CT-253-002 P2: existing-install overwrite/mutation behavior was not covered by
  focused tests.

CT-253-003 remains a known deferred follow-up, not fixed in this pass.

## Fault Category

Implementation gap plus missing regression coverage. The setup helper reported
existing-install handling as deferred but did not enforce that deferred status
before writing setup metadata or initializing SQLite.

## What Changed

- Added focused tests for pre-existing `install_manifest.json` and
  `setup_report.json`.
- Added focused tests for a pre-existing analytics database under the selected
  install root.
- Added existing-install detection before install-mode folder creation,
  manifest/report writes, or SQLite migration.
- While existing-install choices remain deferred, install mode now blocks with
  `existing_install_detected` and writes nothing.
- Setup reports now include concrete `existing_install_handling` status:
  `not_detected` for fresh installs/checks, or `blocked` with symbolic detected
  indicators for existing install state.

## Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`

Existing issue #253 package files remain untracked from prior threads:

- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `tools/dev_app/setup_private_local_v1.ps1`

## Code Changed

Yes. Runtime code changed only in repo-owned private-local-v1 setup tooling:
`tools/dev_app/private_local_v1_setup.py`.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest
semantics, local app runtime behavior outside setup flow, workbook schema,
webhook payload shape, Apps Script behavior, Google Sheets behavior, output
transport, production behavior, OpenAI/model-provider behavior, AI/coaching
behavior, Line Tracer, hidden-card inference, archetype inference,
player-mistake labels, or gameplay advice changed.

## Tests Changed

Updated `tests/test_private_local_v1_setup.py` with focused coverage proving:

- existing manifest/report metadata is preserved;
- existing manifest/report state blocks install mode;
- existing analytics database state blocks install mode;
- existing database contents are not migrated or modified;
- no manifest/report is written in the existing-database blocked case;
- raw install-root paths remain absent from returned report JSON.

The new tests failed before the fix with 2 failures, then passed after the
existing-install guard was added.

## Interface Changes

No new public command, CLI flag, environment-variable contract, route, schema,
migration, workbook column, or webhook payload shape was added.

The existing setup report's `existing_install_handling` object is now populated
from real detection state instead of always reporting deferred.

## Contracted Area Status

The fix stayed inside setup tooling and focused tests. It did not clone
repositories, install dependencies, initialize real local SQLite databases,
start long-running processes, open a browser, delete/reset/move local folders,
create generated/private/local artifacts outside test temp roots, or implement
AI/model-provider behavior.

## Validation Run

```powershell
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check tools tests
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <unique_temp_root> --json-report
git diff --check
py tools\check_agent_docs.py
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Results:

- Focused setup tests before fix: failed, 2 failures reproducing CT-253-001.
- Focused setup tests after fix: passed, 6 passed.
- Adjacent launcher/backend/config/migration tests: passed, 62 passed, 1
  existing FastAPI/Starlette deprecation warning.
- `py -m ruff check tools tests`: passed.
- `py -m ruff check src tests tools`: passed.
- Check-only setup JSON report: passed and left the unique temp root absent.
- `git diff --check`: passed.
- Agent docs check: passed, 46 checked files, 0 errors, 0 warnings.
- Path-scoped protected-surface scan over 7 issue #253 paths: passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 7 issue #253 paths: passed,
  forbidden 0, warnings 0.

## Still Unverified

- Clone-from-GitHub clean install.
- Python virtualenv creation.
- Python dependency installation from `pyproject.toml`.
- Frontend dependency installation with `npm ci`.
- Backend/frontend startup from the v1 setup helper.
- Browser open and frontend status-panel smoke.
- Real default `%LOCALAPPDATA%\MythicEdge\` readiness.
- User-choice handling for use-existing-data, backup/reset, choose folder, or
  cancel setup.

## Reviewer Focus

Codex E should confirm:

- install mode blocks before writing when existing manifest/report metadata is
  present;
- install mode blocks before migrating when an existing analytics database is
  present;
- blocked output remains path-redacted/symbolic;
- check mode remains a dry run;
- fresh temp install mode still creates the expected folder tree, manifest,
  report, and optional empty migrated SQLite database;
- no forbidden parser/runtime/analytics schema/workbook/webhook/App
  Script/Sheets/OpenAI/AI/coaching/production scope was touched.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #253.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/253

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_clean_checkout_install_launch.md

Review artifact:
docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md

Confirm only the Codex D fixes for CT-253-001 and CT-253-002. Verify existing
install metadata/database state blocks install mode before writes or SQLite
migration, while fresh temp install and check mode behavior remain intact.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_clean_checkout_install_launch.md"
  review_artifact: "docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md"
  findings_fixed:
    - "CT-253-001 P1: install mode now blocks existing install metadata/database state before writes."
    - "CT-253-002 P2: focused existing-install overwrite/mutation tests were added."
  validation:
    - "focused setup tests passed: 6 passed"
    - "adjacent launcher/backend/config/migration tests passed: 62 passed, 1 existing warning"
    - "ruff tools/tests passed"
    - "ruff src/tests/tools passed"
    - "check-only setup JSON report passed and left unique temp root absent"
    - "git diff --check passed"
    - "agent docs check passed"
    - "path-scoped protected-surface scan passed: forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan passed: forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  recommendation: "Route to Codex E for confirmation."
```
