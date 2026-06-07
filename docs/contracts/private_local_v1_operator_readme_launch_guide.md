# Private Local V1 Operator README And Launch Guide Contract

## Module

`private_local_v1_operator_readme_launch_guide`

Plain English: this contract defines the docs-only private-local-v1 operator
front door for Mythic Edge. It tells the next thread how to refresh the root
README and create a dedicated operator guide so a human can understand what
Mythic Edge is today, how to install and launch it, where local data lives, and
what the project still does not claim.

This is a contract-writing artifact only. It does not edit README content,
create the operator guide, implement setup behavior, change launcher behavior,
change runtime behavior, create release refs, or touch local/generated/private
artifacts.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/274
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Preceding package-footprint issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/272
- Preceding package-footprint PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/273
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_operator_readme_launch_guide.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- `README.md`
- `docs/internal_project_map.md`
- issue #274
- tracker #136
- issue #272 and PR #273
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`
- `docs/local_artifacts_manifest.json`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `pyproject.toml`
- `frontend/package.json`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 remains open. This contract does not mark the tracker complete.

## Risk Tier

Medium.

Reasons:

- this is docs-only but release-facing;
- unsafe docs can cause a user to run destructive commands, expose private
  data, misunderstand truth ownership, or overclaim readiness;
- the current README is stale and Google-Sheets-first;
- the new guide must describe local app, SQLite, manual import, live mode, and
  Match Journal without changing behavior or creating new truth owners.

## Owning Layer

Primary owner: Quality / Governance release documentation.

Supporting areas:

- Local App / UI;
- Analytics;
- Parser;
- Match Journal;
- Live Player.log Mode;
- Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

Supporting internal project areas:

- Local App / UI;
- Analytics;
- Parser;
- Generated / Local Artifacts;
- Future AI Integration, deferred vocabulary only.

Naming Future AI Integration here covers only reserved local folders and
explicit non-claims. It does not authorize OpenAI runtime behavior,
model-provider integration, AI coaching evaluation, AI-owned parser truth,
AI-owned analytics truth, hidden-card truth, gameplay correctness truth, or
strategic certainty.

## Truth Owner

The README and operator guide own human-facing orientation and safe launch
instructions only.

Truth ownership remains unchanged:

- Parser/state owns MTGA event interpretation, match/game identity,
  deduplication, final reconciliation, and parser-managed facts.
- SQLite owns local storage of parser-normalized facts, not parser truth.
- Analytics owns deterministic local analysis and views, not raw-log
  interpretation.
- Match Journal owns human notes, labels, and review context, not parser or
  analytics truth.
- Local App / UI owns local orchestration and display surfaces only.
- Workbook/webhook/App Script/Sheets remain downstream transport/display
  surfaces.
- AI/model-provider behavior is deferred and owns no truth.

Docs must not become runtime authority, parser truth, analytics truth, workbook
truth, deployment authority, credential policy, or public-release authority.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
current contracts + setup helper command shapes + local artifact policy
  -> README orientation
  -> private-local-v1 operator guide
  -> safer human install/launch/troubleshooting path
```

Forbidden reverse flow:

- docs must not change setup behavior;
- docs must not change parser, analytics, Match Journal, local app, workbook,
  webhook, Apps Script, Sheets, OpenAI/model-provider, AI/coaching, or Line
  Tracer behavior;
- docs must not authorize destructive local cleanup;
- docs must not claim public or production readiness.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`

Expected future implementation/comparison artifact:

- `docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md`

Expected future review artifact:

- `docs/contract_test_reports/private_local_v1_operator_readme_launch_guide.md`

Future Codex C may edit only docs in the approved docs slice:

- `README.md`
- `docs/private_local_v1_operator_guide.md`
- optional docs index/pointer files only if Codex C explains why a pointer is
  necessary and keeps scope docs-only.

Codex C must route back to Codex B before editing setup scripts, launcher code,
parser code, analytics code, local app code, frontend code, workbook/webhook
transport code, Apps Script code, CI, release refs, tags, installers, or
runtime behavior.

## Observed Current Behavior

### README

The root README currently presents Mythic Edge as a personal MTG Arena data
pipeline, but its first-run framing still emphasizes:

- watching MTGA's log while playing;
- pushing summaries into Google Sheets;
- older parser entrypoints;
- a four-thread workflow;
- older repo `data/` runtime folders.

That README is useful historical context, but it is not a correct
private-local-v1 front door for the current local-app-first release-polish
state.

### Current Private-Local-V1 State

Issue #274 and the #272 package-footprint report record:

- current package mode: `managed_full_checkout`;
- current release profile: `private_local_v1`;
- default install root: `%LOCALAPPDATA%\MythicEdge\`;
- managed app checkout: `<install_root>\app`;
- generated/private data root: `<install_root>\data`;
- current default release ref: `codex/analytics-foundation`;
- manifest/report metadata includes package mode, release ref, and explicit
  non-public/non-production readiness flags;
- public release readiness, production readiness, slim packaging, installers,
  release tags/branches, upgrade, and uninstall remain deferred.

### Current Local App And Data Surfaces

Current docs and code establish these concepts for operator docs:

- setup helper:
  `tools/dev_app/private_local_v1_setup.py`;
- PowerShell wrapper:
  `tools/dev_app/setup_private_local_v1.ps1`;
- local app backend: FastAPI under `src/mythic_edge_parser/local_app/`;
- local app frontend: React/Vite under `frontend/`;
- generated local data tree under `<install_root>\data`;
- SQLite database at `<install_root>\data\db\mythic_edge.sqlite3`;
- install manifest at `<install_root>\data\config\install_manifest.json`;
- setup report at `<install_root>\data\diagnostics\setup_report.json`;
- manual historical JSONL import, live Player.log mode, analytics views, and
  Match Journal are current product surfaces or readiness surfaces, with their
  own truth boundaries.

## Contract Decision

The first docs slice should update both surfaces:

1. Refresh `README.md` as the short human front door.
2. Create `docs/private_local_v1_operator_guide.md` as the detailed
   private-local-v1 operator guide.

Reason:

- README should be concise and current, not a giant operator manual.
- The dedicated guide should carry install commands, launch commands, local
  folder layout, SQLite location, privacy rules, troubleshooting, and non-claim
  boundaries.
- Keeping detailed operator material out of the README reduces future README
  drift and makes the private-local-v1 guide easier to update.

## README Responsibility Boundary

The root README must:

- describe Mythic Edge today as a private local MTGA analytics and review app;
- state that parser/state owns parser-managed facts;
- introduce the local app as the intended private-local-v1 front door;
- mention local SQLite analytics, manual JSONL import, live Player.log mode,
  curated analytics views, and Match Journal at a high level;
- clearly link to `docs/private_local_v1_operator_guide.md`;
- de-emphasize or relocate the older Google-Sheets-first framing;
- keep Google Sheets/webhook/App Script references as legacy or downstream
  surfaces, not the primary private-local-v1 path;
- keep development instructions for contributors without presenting them as
  the operator path;
- mention that private-local-v1 is not public-release or production readiness.

The README must not:

- become a full replacement for contracts or the operator guide;
- tell users to delete, reset, or manually clean app-data folders;
- expose real machine paths or private payload examples;
- claim public release, production, live workbook, deployed Apps Script,
  OpenAI/model-provider, AI/coaching, or all-repo-clean readiness;
- imply that workbook formulas, UI, Match Journal, analytics, or AI own parser
  truth.

## Operator Guide Responsibility Boundary

The dedicated operator guide should live at:

```text
docs/private_local_v1_operator_guide.md
```

The guide must explain:

- what private-local-v1 means;
- Windows/private-local assumptions;
- current package mode: `managed_full_checkout`;
- current default release ref: `codex/analytics-foundation`;
- current install root: `%LOCALAPPDATA%\MythicEdge\`;
- managed app checkout: `<install_root>\app`;
- generated/private data root: `<install_root>\data`;
- setup/check/proof command shapes;
- launch expectations;
- local folder layout;
- SQLite database location;
- manual JSONL import overview;
- live Player.log mode overview;
- curated analytics view overview;
- Match Journal overview and truth boundary;
- reserved AI-review folder boundary;
- privacy and never-commit rules;
- safe troubleshooting and stop conditions;
- explicit non-claims and deferred work.

The guide must be beginner-readable. It should define project-specific terms
such as parser, SQLite, FastAPI, React/Vite, manual JSONL import, live
Player.log mode, Match Journal, and generated local state the first time they
appear.

## Required Install And Launch Documentation

The guide must document command shapes against the existing scripts, without
inventing new commands.

Required safe command shapes:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -NoOpen -StopAfterVerify -JsonReport
```

The guide may document install command shape only with safety caveats:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -JsonReport
```

Install documentation must say:

- check/proof flows are safer before real install;
- real default-root install should not be run casually if existing app data is
  present;
- existing install handling blocks rather than overwrites;
- the setup helper records symbolic paths in reports;
- the current default ref is not a v1.0 tag.

Launch documentation must describe the intended local loopback app shape:

- backend host: `127.0.0.1`;
- default backend port: `8765`;
- frontend host: `127.0.0.1`;
- default frontend port: `5173`;
- frontend URL shape: `http://127.0.0.1:5173`;
- backend URL shape: `http://127.0.0.1:8765`.

The guide must not tell the user to expose the app on a public network.

## Required Local Folder And Data Documentation

The guide must document this symbolic tree:

```text
%LOCALAPPDATA%\MythicEdge\
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

Required explanations:

- `app\` is the managed app checkout/package root for private-local-v1;
- `data\` is generated/private local state;
- `config\` contains setup/config metadata;
- `db\` contains the local SQLite database;
- `logs\`, `imports\`, `jobs\`, `diagnostics\`, and `exports\` are local
  generated folders;
- `ai_review\` folders are reserved-only and do not enable AI runtime behavior;
- generated/private folders should not be committed or pasted into reports.

The guide must not instruct users to browse private payloads, dump database
contents, or paste raw local logs into issues.

## SQLite Documentation Requirements

The guide must explain:

- SQLite is the local database engine, meaning a small local file-based
  database;
- the default database path is
  `<install_root>\data\db\mythic_edge.sqlite3`;
- SQLite stores parser-normalized local analytics facts and app-owned local
  state, not raw Player.log payloads;
- SQLite is downstream of parser truth;
- generated database files and sidecar files are local-only and never-commit;
- database inspection should use approved app/status surfaces, not arbitrary
  SQL or raw database dumps in docs.

## Manual Import, Live Mode, Analytics, And Match Journal Requirements

### Manual JSONL Import

Docs must describe manual JSONL import as:

- a local, user-selected historical import path;
- intended for previously saved local artifacts;
- routed through approved local app/import services;
- producing parser-normalized analytics records where accepted;
- never a reason to commit private JSONL files or raw payloads.

### Live Player.log Mode

Docs must describe live mode as:

- future/current local app surfaces for selecting/status-checking a local MTGA
  log path and watcher state;
- parser-owned fact capture when implemented and approved by current contracts;
- not raw log storage in SQLite;
- not Google Sheets/webhook/App Script production behavior;
- not gameplay advice or hidden-card inference.

Docs must avoid saying live private behavior is broadly verified unless the
current report actually proves it.

### Analytics Views

Docs must describe analytics views as:

- deterministic views over parser-normalized local facts;
- useful for history, opening hands, mulligans, play/draw splits, gameplay
  actions, opponent-card observations, and import quality;
- downstream of parser truth;
- not arbitrary SQL browsing;
- not AI coaching or strategic certainty.

### Match Journal

Docs must describe Match Journal as:

- human-owned notes and labels;
- useful for matchup labels, archetype labels, match/game notes, review flags,
  experiments, and context;
- not parser truth;
- not analytics truth;
- not a mechanism to rewrite match/game results, parser facts, or card actions.

## Privacy And Private Artifact Requirements

Docs must tell operators:

- local generated/private data stays local;
- raw MTGA logs, private JSONL artifacts, generated SQLite files, runtime logs,
  transport-failure artifacts, workbook exports, secrets, credentials, API
  keys, endpoint values, spreadsheet IDs, environment values, and local-only
  artifacts must not be committed;
- issue comments and reports should use symbolic paths and category summaries;
- setup reports and app status should avoid raw private payloads;
- if something looks private, stop and ask before sharing it.

Docs must not include real examples of private paths, secrets, endpoint values,
raw log lines, JSONL payloads, database rows, workbook exports, or environment
values.

## Explicit Non-Claims

README and the operator guide must explicitly not claim:

- public release readiness;
- production readiness;
- slim-package readiness;
- installer readiness;
- v1.0 tag existence;
- release branch readiness;
- upgrade or uninstall tooling;
- all-repo scanner cleanliness;
- Pyright-clean or Pyright-gated type maturity;
- live workbook state readiness;
- deployed Apps Script readiness;
- OpenAI/model-provider runtime readiness;
- AI/coaching readiness;
- hidden-card inference;
- gameplay advice or best-line truth;
- Match Journal ownership of parser facts;
- analytics ownership of parser facts.

## Out-Of-Scope Behavior

Codex C must not:

- change setup scripts;
- change launcher behavior;
- change parser behavior;
- change parser state final reconciliation;
- change parser event classes;
- change match/game identity or deduplication;
- change analytics schema, migrations, or ingest semantics;
- change local app runtime or frontend behavior;
- change workbook schema, webhook payload shape, Apps Script behavior, Google
  Sheets behavior, output transport, or production behavior;
- change OpenAI/model-provider, AI/coaching, or Line Tracer behavior;
- create release tags, release branches, slim packages, installers, upgrade
  flows, or uninstall flows;
- delete, move, overwrite, retire, clean, or reset local folders;
- create or commit generated/private/local artifacts.

## Public Interface

Docs surfaces governed by this contract:

- `README.md`;
- `docs/private_local_v1_operator_guide.md`;
- optional docs index/pointer files if needed.

Command shapes the docs may reference:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -NoOpen -StopAfterVerify -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -JsonReport
```

Docs must not invent unimplemented flags, scripts, installer names, release
tags, release branches, or uninstall commands.

## Inputs

Allowed inputs:

- current repo docs and contracts;
- issue #274 problem representation;
- setup helper command shapes;
- symbolic install paths;
- current package metadata fields;
- current local artifact policy;
- current roadmap and internal project map;
- validation command outputs.

Forbidden inputs:

- raw local log contents;
- private JSONL payloads;
- generated database contents;
- runtime log contents;
- transport-failure payload contents;
- workbook export contents;
- secrets, credentials, API keys, endpoint values, spreadsheet IDs, tokens, or
  environment values;
- private local artifact contents.

## Outputs

Required future docs output:

- refreshed `README.md`;
- new `docs/private_local_v1_operator_guide.md`;
- implementation handoff describing sections changed and claims avoided;
- review report verifying docs against this contract.

Forbidden future docs output:

- raw private data examples;
- destructive cleanup advice;
- unimplemented commands;
- public/production readiness claims;
- AI/coaching claims;
- hidden-card or gameplay-advice claims;
- raw local path dumps;
- database dumps.

## Invariants

- README is the short front door.
- The operator guide is the detailed private-local-v1 launch guide.
- Parser truth ownership remains upstream.
- SQLite, analytics views, local app UI, Match Journal, workbook, and AI are
  downstream or deferred surfaces.
- Generated/private artifacts remain local-only.
- Current package mode remains `managed_full_checkout` unless a later contract
  changes it.
- Current default release ref remains `codex/analytics-foundation` unless a
  later contract changes it.

## Validation Requirements

Codex C must run or explain why it could not run:

```powershell
git status --short --branch --untracked-files=all
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Codex C should also manually verify:

- every documented command exists in current scripts;
- install and launch docs do not imply destructive cleanup;
- docs explain private-local-v1 without claiming public/production readiness;
- docs use symbolic paths instead of raw machine-specific examples;
- docs define beginner-facing terms clearly.

Codex E must verify:

- README and guide match current code/contracts;
- no raw/private/generated content was introduced;
- no unimplemented command was documented as available;
- non-claims are explicit;
- protected surfaces remain untouched.

## Acceptance Criteria

The #274 docs package is acceptable when:

- root README describes Mythic Edge today accurately and links to the operator
  guide;
- `docs/private_local_v1_operator_guide.md` exists;
- install/check/proof/launch command shapes match existing scripts;
- local folder tree and SQLite path are documented symbolically;
- manual import, live mode, analytics views, and Match Journal are explained
  with truth boundaries;
- privacy/private artifact rules are beginner-readable and strict;
- explicit non-claims are present;
- no runtime behavior changes are included;
- validation passes.

## Suspected Gaps

- README still references the older four-thread workflow and may need A-G
  workflow wording or a pointer to current governance docs.
- README may still overemphasize Google Sheets compared with local app and
  SQLite.
- Operator guide does not exist yet.
- Current launch instructions may need to distinguish private-local-v1 setup
  from developer-only `MythicEdgeDev` launcher paths.

## Unknowns

- Whether a future root shortcut should become the preferred private-local-v1
  launch command.
- Whether README should preserve a legacy Google Sheets section or move it into
  historical/downstream notes.
- Whether public-release docs will eventually need a separate public README
  pass after private-local-v1 polish.

## Protected Surfaces

This contract does not authorize changes to:

- setup scripts;
- launcher behavior;
- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics schema, migrations, or ingest semantics;
- local app runtime or frontend behavior;
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

Codex C should:

1. verify current branch and git status;
2. inspect issue #274, tracker #136, issue #272, PR #273, README, package
   footprint contract/report, setup helper, launcher wrapper, roadmap, and
   local artifact policy;
3. refresh README as a short front door;
4. create `docs/private_local_v1_operator_guide.md`;
5. produce
   `docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md`;
6. run docs validation and path-scoped safety scans;
7. route to Codex E for review.

Codex C must keep the pass docs-only.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #274.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/274

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_operator_readme_launch_guide.md

Goal:
Refresh README.md as the short private-local-v1 front door and create docs/private_local_v1_operator_guide.md as the detailed operator launch guide. Produce docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md.

Before editing:
- Confirm branch and git status.
- Inspect issue #274, tracker #136, issue #272, PR #273, README.md, docs/contracts/private_local_v1_package_footprint_release_ref.md, docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md, setup helper scripts, roadmap, internal project map, and local artifact manifest.
- State what the docs are supposed to do, what README currently says, why it is stale, and the exact minimal docs-only plan.

Do:
- Update README as a concise current front door.
- Create docs/private_local_v1_operator_guide.md.
- Document install/check/proof command shapes from existing scripts only.
- Document symbolic local folder paths, SQLite location, package mode, release ref, manual JSONL import, live Player.log mode, analytics views, Match Journal, privacy boundaries, and explicit non-claims.
- Define beginner-facing terms briefly.
- Preserve parser truth ownership and private artifact boundaries.

Do not:
- Change setup scripts, launcher behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema or ingest semantics, local app runtime/frontend behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, or Line Tracer behavior.
- Create release tags, release branches, slim packages, installers, upgrade flows, or uninstall flows.
- Delete, move, overwrite, retire, clean, or reset local folders.
- Create or commit generated SQLite files, raw logs, private JSONL artifacts, runtime files, transport-failure artifacts, workbook exports, app-data files, secrets, credentials, API keys, endpoint values, spreadsheet IDs, environment values, frontend build output, or local-only artifacts.
- Claim public release readiness or production readiness.
- Target main or close tracker #136.

Validation:
git status --short --branch --untracked-files=all
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- README sections changed
- operator guide sections created
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/274"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #274 private-local-v1 operator docs problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md"
  contract_artifact: "docs/contracts/private_local_v1_operator_readme_launch_guide.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan for contract"
    - "path-scoped secret/private-marker scan for contract"
  stop_conditions:
    - "Do not edit README or guide files in Codex B."
    - "Do not change setup scripts, launcher behavior, parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create release tags, release branches, slim packages, installers, upgrade flows, or uninstall flows."
    - "Do not delete, move, overwrite, retire, clean, or reset local folders."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
    - "Do not claim public release readiness or production readiness."
```
