# Private Local V1 Package Footprint And Release Ref Contract

## Module

`private_local_v1_package_footprint_release_ref`

Plain English: this contract defines the acceptable private-local-v1 install
footprint, release reference, installed folder tree, manifest/report evidence,
launcher expectations, and future slim-package boundary for Mythic Edge.

This is a contract-writing artifact only. It does not implement setup-script,
launcher, packaging, tag, branch, installer, runtime, parser, analytics,
workbook, webhook, Apps Script, AI, credential, or production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/272
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Related readiness issue: https://github.com/Tahjali11/Mythic-Edge/issues/270
- Related readiness PR: https://github.com/Tahjali11/Mythic-Edge/pull/271
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_package_footprint_release_ref.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- `docs/internal_project_map.md`
- issue #272
- tracker #136
- issue #270 and PR #271
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `docs/contract_test_reports/private_local_v1_readiness_baseline_refresh.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contracts/private_local_v1_scanner_readiness_reconciliation.md`
- `docs/contract_test_reports/private_local_v1_scanner_readiness_reconciliation.md`
- `docs/local_artifacts_manifest.json`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tools/check_local_environment.py`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_private_local_v1_setup.py`
- `tests/test_analytics_dev_app_launcher.py`
- `README.md`
- `pyproject.toml`
- `frontend/package.json`
- `frontend/package-lock.json`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 remains open. This contract does not mark the tracker complete.

## Risk Tier

Medium-High.

Reasons:

- the decision affects v1.0/private-local-v1 release claims and setup UX;
- setup code can clone source, install dependencies, initialize local SQLite,
  create local folders, and launch backend/frontend processes in later threads;
- unsafe reinstall, upgrade, or uninstall behavior could damage private local
  state;
- package-shape changes can accidentally omit required app files or include
  generated/private artifacts;
- release-ref changes can make installs unreproducible or target the wrong
  branch/tag;
- public release and production readiness remain explicitly unclaimed.

## Owning Layer

Primary owner: Quality / Governance release readiness.

Supporting areas:

- Local App / UI setup and launcher;
- Generated / Local Artifacts;
- Analytics SQLite initialization;
- Installability and operational portability.

## Internal Project Area

Quality / Governance.

Supporting internal project areas:

- Local App / UI;
- Generated / Local Artifacts;
- Analytics;
- Future AI Integration, reserved vocabulary only.

Naming Future AI Integration here only covers reserved local folder names. It
does not authorize OpenAI runtime behavior, model-provider integration, AI
coaching evaluation, AI-owned parser truth, AI-owned analytics truth,
hidden-card truth, gameplay correctness truth, or strategic certainty.

## Truth Owner

This contract owns package-footprint and release-ref expectations for the
private-local-v1 release profile.

Truth ownership remains unchanged:

- Git owns tracked repository source state.
- The setup helper owns local setup orchestration evidence only.
- The install manifest and setup report own local install evidence only.
- The local app owns local orchestration and display surfaces.
- Analytics migrations own SQLite schema migration history.
- SQLite owns local storage of parser-normalized facts, not parser truth.
- Parser/state owns MTGA event interpretation, match/game identity,
  deduplication, final reconciliation, and parser-managed facts.

The installed folder tree, launcher, manifest, setup report, SQLite database,
browser UI, and release reference must not become parser truth, analytics
truth, workbook truth, AI truth, production truth, deployment truth, or public
release authority.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
chosen release ref + setup helper + local install root
  -> managed app source or future slim package
  -> generated local data tree
  -> manifest/report evidence
  -> launcher startup and status proof
```

Forbidden reverse flow:

- install footprint decisions must not change parser behavior;
- install footprint decisions must not alter analytics schema or ingest
  semantics;
- install footprint decisions must not alter workbook, webhook, Apps Script,
  Google Sheets, production, OpenAI/model-provider, AI/coaching, or Line Tracer
  behavior;
- package-shape work must not authorize destructive cleanup or local-data
  migration without explicit later scope.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_package_footprint_release_ref.md`

Expected future comparison artifact:

- `docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md`

Expected future review or contract-test artifact:

- `docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md`

Future Codex C may compare or, if explicitly authorized, change only scoped
setup/package docs or tooling such as:

- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_private_local_v1_setup.py`
- setup/launcher documentation or release-readiness reports

Codex C must route back to Codex B before changing parser behavior, analytics
schema or migration semantics, local app runtime behavior outside setup/package
scope, workbook/webhook/App Script/Sheets behavior, AI/model-provider behavior,
credential policy, CI gates, Pyright gate behavior, or destructive local-data
handling.

## Observed Current Behavior

### Readiness Baseline

Issue #270 and the readiness refresh report record:

- original private-local-v1 blockers are no longer active in their original
  form;
- private-local-v1 status is ready for continued release-polish work;
- issue #253 is closed for install mechanics;
- issue #268 closed scanner-readiness reconciliation;
- tracker #136 remains open;
- public release readiness, production readiness, all-repo scanner cleanliness,
  Pyright gating, AI/coaching readiness, live workbook state, and deployed Apps
  Script state are not claimed;
- v1.0 release-footprint polish remains real but deferred.

### Current Setup Footprint

Current setup code defines:

| Surface | Observed value |
| --- | --- |
| Default install root | `%LOCALAPPDATA%\MythicEdge\` |
| Managed app folder | `<install_root>\app` |
| Generated data root | `<install_root>\data` |
| Analytics database | `<install_root>\data\db\mythic_edge.sqlite3` |
| Install manifest | `<install_root>\data\config\install_manifest.json` |
| Setup report | `<install_root>\data\diagnostics\setup_report.json` |
| Default repo URL | `https://github.com/Tahjali11/Mythic-Edge.git` |
| Current default release ref | `codex/analytics-foundation` |

Generated data subfolders currently include:

- `<install_root>\data\config\`
- `<install_root>\data\db\`
- `<install_root>\data\logs\`
- `<install_root>\data\imports\`
- `<install_root>\data\jobs\`
- `<install_root>\data\diagnostics\`
- `<install_root>\data\exports\`
- `<install_root>\data\ai_review\`
- `<install_root>\data\ai_review\sources\`
- `<install_root>\data\ai_review\packets\`
- `<install_root>\data\ai_review\reports\`

The current setup helper supports a managed full source checkout under
`<install_root>\app`. The #253 report verified install mechanics and preserved
the distinction between "setup works" and "the package looks like a polished
end-user bundle."

## Contract Decision

For private-local-v1, a full managed checkout under
`%LOCALAPPDATA%\MythicEdge\app` is acceptable.

This acceptance is release-profile-limited:

- acceptable for the private, local, current-user profile;
- acceptable while the source ref remains explicit and manifest-recorded;
- acceptable while generated/private data remains under `data\` and out of Git;
- acceptable while launcher UX presents Mythic Edge as a local app, not as a
  polished public installer;
- not sufficient for public release or production readiness;
- not a substitute for a future slim package if shared-with-developer or public
  release polish requires one.

A slimmer runtime package is not required before private-local-v1 can proceed,
unless Codex C/E finds that the current managed checkout violates privacy,
local-artifact safety, launch reliability, reinstall safety, or manifest/report
requirements.

## Package-Footprint Recommendation

### Private-Local-V1 Allowed Footprint

The allowed private-local-v1 footprint is:

```text
%LOCALAPPDATA%\MythicEdge\
  app\       # managed app source checkout or future package root
  data\      # generated/private local state
```

`app\` may be a full managed Git checkout for private-local-v1.

`data\` is the only default location for generated/private app state under the
install root.

The setup helper must never use a repo checkout itself, or any folder inside a
repo checkout, as the app-data root.

### Current Full-Checkout Package

The current full-checkout install may include repo-owned source and developer
support files in `app\`, including:

- governance docs;
- source code;
- tests;
- tools;
- frontend source;
- package metadata;
- dependency manifests;
- local app backend/frontend files.

This is acceptable because it is a managed source-based package, not because it
is a polished end-user bundle.

The manifest/report must make the package mode explicit, for example:

- `package_mode`: `managed_full_checkout`;
- `release_profile`: `private_local_v1`;
- `public_release_ready`: false;
- `production_ready`: false.

### Future Slim Package

A future slim package would be expected to include only what is needed to run
the local app and approved setup/status flows:

- Python package source needed at runtime;
- package metadata and dependency manifests needed for installation;
- analytics migration SQL package data;
- local app backend package;
- frontend runtime/build artifacts or a documented frontend install path;
- launcher/setup wrappers;
- README or operator setup instructions;
- license and release metadata when public/shared release work begins.

A future slim package should exclude, unless explicitly justified:

- parser audit contracts, handoffs, and review reports;
- most tests and test fixtures;
- Codex workflow/governance history not needed by the local app;
- development-only helper scripts;
- archived docs;
- generated app data;
- generated SQLite databases and SQLite sidecar files;
- private JSONL artifacts;
- raw logs;
- workbook exports;
- local runtime artifacts;
- credentials or environment files.

The slim package remains deferred unless a later issue and contract make it a
private-local-v1 blocker.

## Release-Ref Recommendation

Before v1.0:

- the default release ref may remain `codex/analytics-foundation`;
- the setup helper must record the chosen ref in manifest/report output;
- an explicit `--release-ref` override remains acceptable for proof and
  controlled tests;
- release-readiness reports must state when the ref is an integration branch
  rather than a stable tag.

Recommended next release-ref progression:

1. continue using `codex/analytics-foundation` while release-polish work is
   still landing;
2. create a dedicated release candidate ref only after Codex G says the
   private-local-v1 release packet is ready for freeze;
3. create a `v1.0.0` tag only after the final readiness packet passes and the
   user explicitly approves tagging;
4. update setup defaults to a tag only after that tag exists and a later
   implementation contract authorizes the change.

Do not create a v1.0 tag in Codex B, Codex C comparison, or Codex E review.

## Install-Root And Folder-Tree Expectations

Required symbolic tree:

```text
<install_root>\
  app\
  data\
    config\
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

Folder expectations:

- `<install_root>` defaults to `%LOCALAPPDATA%\MythicEdge\` on Windows;
- `<install_root>\app` is managed app source/package state;
- `<install_root>\data` is generated/private app state;
- AI-review folders are reserved local-only placeholders and do not enable AI
  runtime behavior;
- generated folders must remain outside the repo and out of Git;
- setup reports may use symbolic paths such as `<install_root>` instead of raw
  machine paths.

## Manifest And Setup Report Expectations

The install manifest and setup report must prove:

- release profile: `private_local_v1`;
- release ref used;
- repo URL or package source, redacted or symbolic where needed;
- package mode, such as `managed_full_checkout` or future `slim_package`;
- source/package validation status;
- managed app root and generated data root symbolic locations;
- required folder tree status;
- analytics database initialization status;
- migration IDs applied without embedding raw SQL;
- parser rows inserted during setup: false;
- dependency installation status;
- launcher/backend/frontend startup status when proof mode runs;
- browser/status verification status and whether it was HTTP-only or rendered;
- privacy flags showing no raw paths, raw payloads, secrets, endpoint values,
  external sends, or AI runtime behavior were included or performed;
- existing-install handling status;
- public release readiness: false unless a later public-release contract
  authorizes otherwise;
- production readiness: false.

Manifest/report output must not include:

- raw local paths when symbolic paths are sufficient;
- raw Player.log contents;
- private JSONL payloads;
- generated database contents;
- transport-failure payload contents;
- workbook export contents;
- secrets, credentials, endpoint values, spreadsheet IDs, tokens, API keys, or
  environment values;
- frontend build output contents;
- local-only artifact contents.

## Launcher UX Expectations

Launcher UX for private-local-v1 must guarantee:

- one obvious way to start the local app after setup;
- loopback-only backend/frontend URLs unless a later contract changes network
  exposure;
- no destructive controls in the initial private-local-v1 package-footprint
  work;
- status surfaces are available without requiring raw private data inspection;
- errors are actionable and beginner-readable;
- raw machine paths are redacted or summarized in reports and UI where
  possible;
- generated/private artifacts are not opened, uploaded, copied, or cleaned
  automatically;
- AI-review folders remain visibly reserved if surfaced at all, not active AI
  features.

The launcher may be source-checkout-shaped for private-local-v1, but it should
not require the user to understand repo internals for normal launch.

## Reinstall, Upgrade, Uninstall, And Existing-Install Boundaries

### Existing Install

If `%LOCALAPPDATA%\MythicEdge\` already exists, later implementation must not
overwrite or mutate it silently.

Allowed report-only behavior:

- detect an existing manifest;
- detect an existing setup report;
- detect an existing analytics database;
- detect existing generated data folders;
- detect an existing managed app checkout;
- summarize state by symbolic path and category.

Forbidden behavior without explicit later approval:

- delete local data;
- move local data;
- archive local data;
- overwrite local data;
- reset the managed app checkout;
- drop or migrate SQLite data destructively;
- inspect private payload contents;
- uninstall automatically.

### Reinstall

Reinstall behavior must be opt-in. The first safe private-local-v1 behavior is
to block with an explanatory report when existing install state is detected.

Future reinstall support must define:

- backup or preservation policy;
- whether the managed app checkout can be refreshed separately from `data\`;
- how manifest/report history is preserved;
- how user approval is captured.

### Upgrade

Upgrade behavior is deferred.

Future upgrade support must define:

- source ref transition;
- migration behavior;
- app checkout/package replacement behavior;
- compatibility between old manifest schema and new setup code;
- rollback or stop conditions.

### Uninstall

Uninstall behavior is deferred and must remain manual-only until a later
contract authorizes tooling.

Any uninstall tool must be separately contracted because it can destroy private
local state.

## Private And Generated Artifact Boundaries

Generated/private data must remain:

- under `<install_root>\data\` for the installed app profile;
- ignored or outside the source repo;
- absent from commits, PRs, reports, screenshots, and issue text except as
  symbolic path/category summaries;
- local-only unless a future contract explicitly authorizes export.

The package contract must not authorize committing:

- raw logs;
- private JSONL artifacts;
- generated SQLite databases or sidecar files;
- runtime logs;
- transport-failure artifacts;
- workbook exports;
- secrets, credentials, endpoint values, tokens, API keys, spreadsheet IDs, or
  environment values;
- frontend build output unless a future slim-package contract explicitly
  defines build-artifact policy;
- app-data files;
- local-only artifacts.

## Public Interface

Commands and surfaces governed by this contract:

```powershell
py tools\dev_app\private_local_v1_setup.py --check --json-report
py tools\dev_app\private_local_v1_setup.py --install --initialize-sqlite --json-report
py tools\dev_app\private_local_v1_setup.py --proof --json-report
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -JsonReport
```

Public setup flags covered:

- `--install-root`;
- `--source-checkout`;
- `--existing-checkout`;
- `--repo-url`;
- `--release-ref`;
- `--initialize-sqlite`;
- `--no-open`;
- `--leave-running`;
- `--stop-after-verify`;
- `--backend-port`;
- `--frontend-port`;
- `--json-report`.

Manifest/report fields covered:

- install profile;
- package mode;
- release ref;
- install root;
- app/package root;
- generated data root;
- folder tree status;
- source/package status;
- dependency status;
- SQLite initialization status;
- launcher/status proof;
- privacy flags;
- public/production readiness flags;
- existing-install handling.

## Inputs

Allowed inputs:

- issue #272 and tracker #136;
- current setup helper constants and tests;
- release ref string;
- repo URL or future package source;
- install root path selected by user or default environment;
- Git/source marker presence;
- manifest and setup report shape;
- validation command outputs;
- symbolic folder-tree summaries.

Forbidden inputs:

- raw private log contents;
- private JSONL payloads;
- generated database contents;
- runtime log contents;
- transport-failure payload contents;
- workbook export contents;
- secrets, credentials, endpoint values, spreadsheet IDs, tokens, API keys, or
  environment values;
- private local artifact contents.

## Outputs

Required future comparison/report output:

- package-footprint verdict;
- release-ref verdict;
- whether current full managed checkout remains acceptable for
  private-local-v1;
- whether slim package work is required now or deferred;
- expected installed folder tree;
- manifest/report field comparison;
- launcher UX comparison;
- existing-install/reinstall/upgrade/uninstall boundary comparison;
- generated/private artifact safety status;
- validation commands and results;
- remaining unverified layers;
- next recommended workflow role.

Forbidden output:

- raw private data;
- raw local machine paths when symbolic paths are enough;
- raw scanner excerpts;
- secret-looking values;
- generated database rows;
- raw setup logs that include private paths or environment values.

## Validation Requirements

Codex C must run or explain why it could not run:

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py tools\dev_app\private_local_v1_setup.py --check --json-report
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
@'
docs/contracts/private_local_v1_package_footprint_release_ref.md
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_package_footprint_release_ref.md
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If Codex C implements code changes later, it must also run focused tests for
the changed setup/launcher behavior and a controlled proof/check command
against a disposable install root outside the repo and outside the real default
root. It must not touch the actual default install root unless a later prompt
explicitly approves that action.

Codex E must verify:

- no destructive local-folder operation was performed;
- no real default-root install was mutated without approval;
- no raw/private/generated content was copied into artifacts;
- package mode and release ref are recorded clearly;
- public/production readiness is not claimed;
- slim-package deferral is explicit if no slim package is implemented.

## Acceptance Criteria

The #272 package-footprint contract is satisfied when:

- current full managed checkout is classified as acceptable or unacceptable for
  private-local-v1 with evidence;
- slim-package work is either deferred or scoped as a clear blocker;
- release-ref policy is explicit for pre-v1.0 and v1.0 tag timing;
- installed folder-tree expectations are explicit;
- manifest/report requirements include package mode and readiness boundaries;
- launcher UX expectations preserve beginner-readable startup without
  destructive controls;
- reinstall, upgrade, uninstall, and existing-install boundaries are safe;
- private/generated artifact boundaries are preserved;
- validation evidence is recorded;
- protected surfaces remain untouched.

## Suspected Gaps

- Current setup code may not yet have an explicit `package_mode` field in the
  manifest/report.
- The current release ref defaults to an integration branch, which is adequate
  before v1.0 but should not be mistaken for a stable release tag.
- README/onboarding may still describe older parser/Google Sheets workflows
  more prominently than the private-local-v1 local app setup path.
- Full checkout footprint may remain visually noisy for a brand-new user even
  if it is technically acceptable for private local use.
- Upgrade and uninstall behavior remain intentionally deferred.

## Unknowns

- Whether the user wants private-local-v1 to stay source-checkout based for a
  while or move quickly to a slim package.
- Whether a future release candidate branch should be named
  `release/private-local-v1`, `release/v1.0.0`, or another ref.
- Whether frontend build output should ever be committed for a slim package or
  always rebuilt locally.
- Whether future shared-with-developer packaging should use Git clone, a zip
  archive, a wheel, a PowerShell bootstrapper, or an installer.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics schema, migrations, or ingest semantics;
- local app/UI behavior outside later scoped setup/package work;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- CI gates;
- Pyright gate behavior;
- scanner category semantics or severity;
- secrets, credentials, tokens, API keys, endpoint values, spreadsheet IDs, or
  environment values;
- raw logs, private JSONL artifacts, generated SQLite databases, SQLite sidecar
  files, runtime files, transport-failure artifacts, workbook exports,
  frontend build output, app-data files, generated data, or local-only
  artifacts.

## Codex C Implementation Scope

Codex C should first perform a comparison/report pass:

1. verify current branch and git status;
2. inspect issue #272, tracker #136, issue #270, PR #271, and setup/helper
   code;
3. compare current setup manifest/report shape against this contract;
4. decide whether a docs/report-only comparison is enough or whether narrow
   setup metadata changes are required;
5. avoid real default-root mutation;
6. produce
   `docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md`;
7. route to Codex E for review before Codex F/G lifecycle work.

If implementation is authorized in the same Codex C prompt, the narrow likely
scope is manifest/report metadata only: package mode, release-ref clarity, and
public/production readiness flags. It must not implement slim packaging,
uninstall, upgrade, or destructive reinstall behavior unless a later contract
explicitly scopes that work.

## Pasteable Codex C/E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #272.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/272

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_package_footprint_release_ref.md

Goal:
Compare the current private-local-v1 setup/package footprint against the contract and produce docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md. Keep the pass report-first unless the prompt explicitly authorizes narrow setup metadata changes.

Before editing:
- Confirm branch and git status.
- Inspect issue #272, tracker #136, issue #270, PR #271, the #253 install proof report, private_local_v1_setup.py, setup_private_local_v1.ps1, launcher code, and focused setup tests.
- State what the package footprint is supposed to prove, what the current managed checkout install does, what gap remains, and the exact minimal comparison or implementation plan.

Do:
- Decide whether the full managed checkout under %LOCALAPPDATA%\MythicEdge\app is acceptable for private-local-v1.
- Verify release-ref expectations and v1.0 tag timing.
- Compare install-root folder tree, manifest/report fields, launcher UX, existing-install handling, reinstall/upgrade/uninstall boundaries, and private/generated artifact boundaries.
- Produce the implementation handoff with validation and remaining risks.

Do not:
- Delete, move, overwrite, uninstall, archive, clean, or reset local folders.
- Mutate the actual default install root unless explicitly approved in a later thread.
- Create a release tag, release branch, PR, installer, slim package, or CI gate.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema or ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, or Line Tracer behavior.
- Touch secrets, credentials, raw logs, private JSONL artifacts, generated SQLite files, runtime files, transport-failure artifacts, workbook exports, frontend build output, app-data files, environment values, or local-only artifacts.
- Target main.

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py tools\dev_app\private_local_v1_setup.py --check --json-report
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/private_local_v1_package_footprint_release_ref.md
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_package_footprint_release_ref.md
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- artifact produced
- package-footprint verdict
- release-ref verdict
- install-root/folder-tree assessment
- manifest/report assessment
- launcher UX assessment
- reinstall/upgrade/uninstall boundary assessment
- validation results
- protected surfaces status
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/272"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #272 package-footprint problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md"
  contract_artifact: "docs/contracts/private_local_v1_package_footprint_release_ref.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan for contract"
    - "path-scoped secret/private-marker scan for contract"
  stop_conditions:
    - "Do not implement setup, launcher, packaging, release-ref, branch, or tag changes in Codex B."
    - "Do not delete, move, overwrite, uninstall, archive, clean, or reset local folders."
    - "Do not mutate the actual default install root without explicit later approval."
    - "Do not claim public release, production, all-repo scanner, Pyright-gated, AI/coaching, live workbook, or deployed Apps Script readiness."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
```
