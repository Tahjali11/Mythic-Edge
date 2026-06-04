# Private Local V1 Package Footprint And Release Ref Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/272

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/private_local_v1_package_footprint_release_ref.md`

## Internal Project Area

Primary: Quality / Governance.

Supporting areas: Local App / UI, Generated / Local Artifacts, Analytics, and
reserved Future AI Integration vocabulary only.

## Truth Owner

The #272 contract owns private-local-v1 package-footprint and release-ref
expectations only. Parser/state remains the owner of parser truth. SQLite
remains a local analytics support layer and does not become parser truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Context Reviewed

- Issue #272 is open.
- Tracker #136 is open.
- Related issue #270 is closed.
- PR #271 is merged into `codex/analytics-foundation` at merge commit
  `7e7ca9e1327fbb8934b08fc8097950bd1bf172ab`.
- The private-local-v1 readiness refresh says the original private-local-v1
  blockers are resolved or reclassified and the project is ready for continued
  release-polish work.
- The #253 install proof report says install mechanics passed, while the
  user-facing package footprint and release polish remain separate follow-up
  scope.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_readiness_baseline_refresh.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_private_local_v1_setup.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_migration_loader.py`

## What The Package Footprint Is Supposed To Prove

The package-footprint pass is supposed to decide whether private-local-v1 can
ship as a managed source checkout under the current-user app root, or whether
a slimmer runtime package is required before release-polish work can continue.

It must also keep release-ref language honest: an integration branch can remain
the pre-v1.0 install ref, but it must not be described as a stable v1.0 tag.

## Current Managed Checkout Behavior

Current setup/proof behavior is source-checkout based:

- default install root is `%LOCALAPPDATA%\MythicEdge`;
- managed app/package root is `<install_root>\app`;
- generated/private state root is `<install_root>\data`;
- generated subfolders include config, db, logs, imports, jobs, diagnostics,
  exports, and reserved AI-review folders;
- proof mode can clone the selected source ref into `<install_root>\app`;
- setup mode can initialize an empty migrated analytics SQLite database;
- existing install state is detected before install-mode writes;
- launcher startup remains loopback-oriented and non-destructive.

The current shape looks like a managed repo checkout. That is acceptable for
private-local-v1 under the #272 contract, but it is not a polished public
installer or slim end-user package.

## Exact Minimal Plan

Chosen implementation option: report-only comparison.

Reason: the user prompt says to keep this pass report-first unless it
explicitly authorizes narrow setup metadata changes. The prompt does not
authorize setup metadata edits, so this pass records the current gap rather
than changing setup code.

## What Changed

Added this handoff:

- `docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md`

## Code Changed

No runtime code changed.

No setup script, launcher, parser, analytics, workbook, webhook, Apps Script,
Sheets, OpenAI/model-provider, AI/coaching, Line Tracer, production, packaging,
tagging, release-branch, installer, CI, or dependency behavior changed.

## Tests Added Or Updated

None.

## Interface Changes

None.

No function signature, setup flag, manifest schema, report schema, environment
variable contract, workbook schema, webhook shape, launcher command, or CLI
behavior was changed.

## Package-Footprint Verdict

`managed_full_checkout_acceptable_for_private_local_v1`

A full managed checkout under `%LOCALAPPDATA%\MythicEdge\app` is acceptable for
private-local-v1 because the contract explicitly allows it for the private,
local, current-user release profile.

This verdict is profile-limited:

- acceptable for private-local-v1;
- not sufficient for public release;
- not sufficient for production readiness;
- not proof of a slim v1.0 package;
- not a reason to hide source-checkout-shaped files from the user.

Slim-package work is deferred unless Codex E finds a blocker in this report.

## Release-Ref Verdict

`codex/analytics-foundation_pre_v1_allowed`

The current default release ref is `codex/analytics-foundation`. This remains
acceptable before v1.0 while release-polish work is still landing.

The v1.0 tag should not be created by this pass. The recommended sequence is:

1. keep `codex/analytics-foundation` while release-polish work continues;
2. create a release candidate ref only after Codex G says the private-local-v1
   release packet is ready for freeze;
3. create a `v1.0.0` tag only after final readiness passes and the user
   explicitly approves tagging;
4. update setup defaults to a tag only under a later implementation contract.

## Install-Root And Folder-Tree Assessment

Status: mostly aligned.

The code defines and tests the expected symbolic tree:

```text
<install_root>
  app
  data
    config
    db
    logs
    imports
    jobs
    diagnostics
    exports
    ai_review
      sources
      packets
      reports
```

The setup helper refuses app-data roots inside the source checkout or another
Git checkout. Check mode reports symbolic paths and does not create folders or
database files.

The default install root currently has existing install indicators. Check mode
reported this symbolically as blocked existing install state with these
categories: install manifest, setup report, analytics database, app checkout
root, and generated data. This pass did not inspect private contents and did
not mutate the default root.

## Manifest And Setup Report Assessment

Status: partially aligned, implementation gap remains.

Current manifest/report strengths:

- manifest object and report object are stable;
- `install_profile` is `private_local_v1`;
- roots are symbolic;
- source checkout status is symbolic;
- folder creation and SQLite status are represented;
- migration IDs are listed without raw SQL;
- parser rows inserted during setup remain false in SQLite setup status;
- existing install handling is reported;
- privacy flags record no raw paths, raw logs, private payloads, secret/env
  reads, raw SQL, stack traces, external sends, or AI provider key reads;
- AI-review folders are reserved-only and AI runtime is disabled;
- proof mode records clone status and release ref in the clone subsection.

Current manifest/report gaps against #272:

- no top-level `package_mode` field;
- no top-level `release_ref` field in check/install manifest output;
- no top-level `public_release_ready: false` field;
- no top-level `production_ready: false` field;
- non-proof check/install configuration does not carry release ref or package
  mode as first-class metadata;
- release-ref status appears only as deferred Git status metadata unless proof
  mode records a clone ref.

Recommended next implementation slice, if approved after Codex E:

- add focused manifest/report metadata only:
  - `package_mode: managed_full_checkout`;
  - `release_profile: private_local_v1` or preserve `install_profile` with a
    clearly documented alias;
  - `release_ref`;
  - `public_release_ready: false`;
  - `production_ready: false`;
- add focused tests for those fields;
- do not change install behavior, clone behavior, runtime behavior, or default
  release ref in the same slice unless a contract explicitly authorizes it.

## Launcher UX Assessment

Status: aligned for current private-local-v1 support.

The PowerShell wrapper exposes one obvious local setup entrypoint and forwards
safe setup flags to the Python helper. Focused tests assert that the wrapper
does not directly contain destructive shell commands, direct clone commands,
direct dependency install commands, or remove/delete commands.

The launcher uses loopback host/port validation and does not expose destructive
database, import, cleanup, or uninstall controls as part of this package
footprint work.

Remaining UX limitation:

- the installed `app` folder is source-checkout-shaped, so it may still look
  noisy to a brand-new user. The #272 contract accepts that only for
  private-local-v1 and preserves slim-package polish as future work.

## Existing-Install, Reinstall, Upgrade, And Uninstall Boundary Assessment

Status: aligned for safe first behavior.

Current behavior:

- install mode blocks when existing install state is detected;
- existing manifest/report metadata is not overwritten;
- an existing analytics database is not migrated or overwritten by the blocked
  install path;
- a managed app checkout can be recognized separately from unrelated stale
  state in proof flow;
- reinstall choices are not implemented;
- upgrade behavior is deferred;
- uninstall behavior is deferred and manual-only.

This pass did not delete, move, archive, clean, overwrite, reset, uninstall, or
migrate any local folder or generated state.

## Private / Generated Artifact Boundary Assessment

Status: aligned.

Generated/private state belongs under `<install_root>\data` for the installed
profile and must remain outside Git. This pass did not read, copy, sanitize,
upload, move, delete, or commit generated/private artifacts.

Reserved AI-review folders remain local-only reserved vocabulary and do not
enable OpenAI runtime behavior, model-provider behavior, AI/coaching behavior,
hidden-card inference, or AI-owned analytics truth.

## Contracted Area Status

The implementation stayed inside the contracted Quality/Governance comparison
area. No downstream protected consumer was changed.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py tools\dev_app\private_local_v1_setup.py --check --json-report
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
```

Results are recorded after final validation:

- `git status --short --branch --untracked-files=all` -> branch
  `codex/analytics-foundation...origin/codex/analytics-foundation`; #272
  contract and handoff are untracked.
- `py -m pytest -q tests\test_private_local_v1_setup.py` -> 8 passed.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py`
  -> 62 passed, 1 existing FastAPI/Starlette deprecation warning.
- `py tools\dev_app\private_local_v1_setup.py --check --json-report` ->
  passed; status passed, mode check, warnings 0, errors 0; output used
  symbolic roots.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, checked files 46, errors 0,
  warnings 0.
- `py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation`
  -> passed, changed paths 0, forbidden 0, warnings 0.
- `py tools\check_secret_patterns.py --base origin/codex/analytics-foundation`
  -> passed, scanned paths 0, forbidden 0, warnings 0.
- path-scoped protected-surface scan over contract and handoff -> passed,
  changed paths 2, forbidden 0, warnings 0.
- path-scoped secret/private-marker scan over contract and handoff -> passed,
  scanned paths 2, forbidden 0, warnings 0.
- direct docs whitespace/ascii/final-newline check over contract and handoff
  -> passed.

## Protected-Surface Status

No protected surface was changed.

Specifically unchanged:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema or ingest semantics;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior.

## Secret / Private-Marker Status

No secret, credential, raw log, private JSONL artifact, generated SQLite file,
runtime file, transport-failure artifact, workbook export, frontend build
output, app-data file, environment value, or local-only artifact was added,
copied, inspected for contents, committed, or exposed.

## Still Unverified

- Codex E has not yet independently reviewed the package-footprint verdict.
- The manifest/report metadata gap has not been implemented.
- No release candidate branch or tag exists from this pass.
- No slim package exists from this pass.
- No installer exists from this pass.
- Public release readiness is not claimed.
- Production readiness is not claimed.
- Live workbook and deployed Apps Script readiness are not claimed.
- AI/coaching readiness is not claimed.

## Reviewer Focus

Codex E should pay special attention to:

- whether report-only handling is acceptable for #272;
- whether missing `package_mode`, `release_ref`, `public_release_ready`, and
  `production_ready` fields should be blocking or routed to a narrow Codex C/D
  metadata implementation slice;
- whether the managed full checkout verdict is worded narrowly enough for
  private-local-v1 only;
- whether release-ref and v1.0 tag timing avoid overclaiming stable release
  status;
- whether existing-install blocking remains non-destructive and beginner-safe.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #272.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/272

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_package_footprint_release_ref.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md

Goal:
Review the #272 package-footprint/release-ref comparison against the contract. Decide whether report-only handling is sufficient, or whether the missing setup manifest/report metadata fields require a narrow Codex D/C metadata implementation slice before submission.

Review focus:
- package-footprint verdict for managed_full_checkout under private-local-v1;
- release-ref verdict for codex/analytics-foundation before v1.0;
- v1.0 tag timing and overclaim prevention;
- installed folder tree and generated/private artifact boundaries;
- manifest/report gap for package_mode, release_ref, public_release_ready, and production_ready;
- launcher UX and destructive-control boundaries;
- existing-install, reinstall, upgrade, and uninstall safety boundaries;
- validation evidence and protected-surface status.

Do not:
- mutate the real default install root;
- delete, move, overwrite, uninstall, archive, clean, or reset local folders;
- create a release tag, release branch, PR, installer, slim package, or CI gate;
- change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior;
- stage, commit, push, merge, close #272, or mark tracker #136 complete unless explicitly asked.

Validation:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_private_local_v1_setup.py
- py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
- py tools\dev_app\private_local_v1_setup.py --check --json-report
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over contract and handoff
- path-scoped secret/private-marker scan over contract and handoff

Produce:
- docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md

Final report must include:
- findings first;
- issue/tracker reviewed;
- contract and handoff reviewed;
- package-footprint verdict;
- release-ref verdict;
- whether metadata gaps are blocking;
- validation results;
- protected-surface status;
- remaining risks;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/272"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  role_performed: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/private_local_v1_package_footprint_release_ref.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  package_footprint_verdict: "managed full checkout acceptable for private-local-v1 only"
  release_ref_verdict: "codex/analytics-foundation acceptable before v1.0; v1.0 tag deferred until final readiness and explicit user approval"
  implementation_option: "report-only comparison"
  code_changed: false
  tests_changed: false
  validation:
    - "git status --short --branch --untracked-files=all -> #272 contract and handoff untracked"
    - "py -m pytest -q tests/test_private_local_v1_setup.py -> 8 passed"
    - "adjacent setup/local-app/migration tests -> 62 passed, 1 existing FastAPI/Starlette deprecation warning"
    - "py tools/dev_app/private_local_v1_setup.py --check --json-report -> passed, symbolic output, warnings 0, errors 0"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "base protected-surface scan -> passed, forbidden 0, warnings 0"
    - "base secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "path-scoped contract/handoff protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped contract/handoff secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "direct #272 docs whitespace/ascii/final-newline check -> passed"
  protected_surfaces_touched: false
  forbidden_scope_touched: false
  generated_private_artifacts_created: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
