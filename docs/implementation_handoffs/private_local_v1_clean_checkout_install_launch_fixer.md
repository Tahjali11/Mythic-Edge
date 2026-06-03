# Private Local V1 Clean Checkout Install And Launch Proof Fixer Handoff

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

The setup proof owns install and launch readiness evidence only. Parser truth,
analytics fact truth, workbook truth, Match Journal truth, AI truth, and
production truth remain unchanged.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer.

## Source Findings

- CT-253-005 P1: proof launch can pass on ambient Python instead of the proof
  virtualenv.
- CT-253-006 P2: status-panel verification is overclaimed from HTTP checks.

Previously fixed findings remain fixed:

- CT-253-001: existing install metadata/database state blocks before writes.
- CT-253-002: focused existing-install overwrite/mutation tests exist.

## Fault Category

Implementation gap plus missing regression coverage. Proof mode installed
dependencies into the proof virtualenv, but delegated backend launch to the
normal developer launcher command builder, which used ambient `py` when
available. Proof mode also treated loopback HTTP checks as rendered frontend
status-panel proof.

## What Changed

- Added focused tests that prove proof mode launches the backend with
  `<proof_source_checkout>\.venv` Python, not ambient Python.
- Added a proof virtualenv import check:
  `<venv_python> -c "import mythic_edge_parser, fastapi, uvicorn"`.
- Added an optional `backend_python` override to the developer launcher config.
  Normal launcher behavior is unchanged when the override is absent.
- Updated proof mode to pass the proof virtualenv interpreter into backend
  launch.
- Changed proof `status_panel_verification` from `passed` to `http_only` when
  only HTTP checks were run.
- Added a `status_panel_verification_http_only` warning so the overall proof
  status is degraded rather than overclaiming complete rendered-panel proof.

## Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_fixer.md`

Other issue #253 package files were already modified before this fixer pass and
were preserved:

- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/implementation_handoffs/private_local_v1_clean_checkout_install_launch_comparison.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `tools/dev_app/setup_private_local_v1.ps1`

## Code Changed

Yes. Runtime code changed only in repo-owned private-local-v1 setup proof
tooling and the developer launcher command builder override hook.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest
semantics, workbook schema, webhook payload shape, Apps Script behavior, Google
Sheets behavior, output transport, production behavior, OpenAI/model-provider
behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype
inference, player-mistake labels, or gameplay advice changed.

## Tests Changed

Updated `tests/test_private_local_v1_setup.py` with focused coverage proving:

- existing-checkout proof backend launch starts with the proof virtualenv
  Python command;
- clone proof backend launch starts with the cloned app checkout virtualenv
  Python command;
- proof dependency command sequence includes the virtualenv import check;
- HTTP-only checks produce `status_panel_verification = "http_only"`;
- proof warnings include `status_panel_verification_http_only`;
- final setup report carries the same honest `http_only` panel status.

The new tests failed before the fix with 2 failures, then passed after the proof
launch and status-reporting changes.

## Interface Changes

No new public setup command, CLI flag, environment-variable contract, route,
schema, migration, workbook column, or webhook payload shape was added.

Internal launcher config gained an optional `backend_python` field. Existing
launcher callers preserve the previous ambient Python behavior unless they pass
that override explicitly.

## Contracted Area Status

The fix stayed inside setup/proof tooling and focused tests. It did not run a
live `--proof`, clone repositories, install dependencies, start long-running
processes, open a browser, delete/reset/move local folders, use real default
`%LOCALAPPDATA%\MythicEdge`, create generated/private/local artifacts outside
test temp roots, or implement AI/model-provider behavior.

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

- Focused setup tests before fix: failed, 2 failures reproducing CT-253-005 and
  CT-253-006 coverage gaps.
- Focused setup tests after fix: passed, 8 passed.
- Adjacent launcher/backend/config/migration tests: passed, 62 passed, 1
  existing FastAPI/Starlette deprecation warning.
- `py -m ruff check tools tests`: passed.
- `py -m ruff check src tests tools`: passed.
- Check-only setup JSON report: passed and left the unique temp root absent.
- `git diff --check`: passed with the known PowerShell CRLF notice for
  `tools/dev_app/setup_private_local_v1.ps1`.
- Agent docs check: passed, 46 checked files, 0 errors, 0 warnings.
- Path-scoped protected-surface scan over 8 issue #253 paths: passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 8 issue #253 paths: passed,
  forbidden 0, warnings 0.

## Still Unverified

- Live GitHub clone through `--proof`.
- Real dependency installs through `--proof`.
- Real backend/frontend/browser proof through `--proof`.
- Rendered browser DOM smoke for the setup/status panel.
- Real default `%LOCALAPPDATA%\MythicEdge` readiness.
- User manual fresh install readiness.
- Issue #253 and tracker #136 completion.

## Reviewer Focus

Codex E should confirm:

- proof backend commands use the proof virtualenv interpreter;
- proof dependency status includes the virtualenv import check;
- proof status-panel verification no longer claims rendered panel proof from
  HTTP checks;
- degraded proof status is expected while rendered status-panel/browser DOM
  smoke remains unverified;
- normal developer launcher behavior remains compatible when `backend_python`
  is not supplied;
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

Confirm only the Codex D fixes for CT-253-005 and CT-253-006. Verify proof
backend launch uses the proof virtualenv, proof dependency status includes the
virtualenv import check, and status-panel verification is reported as
HTTP-only rather than rendered-panel proof. Do not route the user to manual
fresh install unless confirmation proves readiness.
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
    - "CT-253-005 P1: proof backend launch now uses the proof virtualenv Python."
    - "CT-253-006 P2: HTTP-only checks now report status_panel_verification as http_only, not passed."
  validation:
    - "focused setup tests passed: 8 passed"
    - "adjacent launcher/backend/config/migration tests passed: 62 passed, 1 existing warning"
    - "ruff tools/tests passed"
    - "ruff src/tests/tools passed"
    - "check-only setup JSON report passed and left unique temp root absent"
    - "git diff --check passed with known PowerShell CRLF notice"
    - "agent docs check passed"
    - "path-scoped protected-surface scan passed: forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan passed: forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  readiness_verdict: "not_ready_for_user_manual_fresh_install_until Codex E confirms"
  recommendation: "Route to Codex E for confirmation."
```
