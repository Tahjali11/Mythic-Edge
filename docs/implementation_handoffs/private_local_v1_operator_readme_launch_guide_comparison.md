# Private Local V1 Operator README And Launch Guide Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Tracker Reviewed

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/274
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Preceding issue: https://github.com/Tahjali11/Mythic-Edge/issues/272
- Preceding PR: https://github.com/Tahjali11/Mythic-Edge/pull/273

## Contract Used

- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`

## Branch And Git Status

- Branch confirmed: `codex/analytics-foundation`
- Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/private_local_v1_operator_readme_launch_guide.md
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`
- `README.md`
- `docs/project_roadmap.md`
- `docs/internal_project_map.md`
- `docs/local_artifacts_manifest.json`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `pyproject.toml`
- `frontend/package.json`
- GitHub issue #274
- GitHub issue #136
- GitHub issue #272
- GitHub PR #273

## Current Behavior Compared To Contract

The contract requires a docs-only release/operator front door. The repository
already has private-local-v1 setup and launcher support with:

- release profile `private_local_v1`;
- package mode `managed_full_checkout`;
- default release ref `codex/analytics-foundation`;
- default install root `%LOCALAPPDATA%\MythicEdge\`;
- managed app checkout `<install_root>\app`;
- generated/private local state `<install_root>\data`;
- backend port `8765`;
- frontend port `5173`.

The prior README did not match that state. It still described Mythic Edge as a
Google-Sheets-first parser pipeline, pointed users at older entrypoints, listed
repo `data/` runtime folders, and referenced the older four-thread workflow.

The repository had no `docs/private_local_v1_operator_guide.md`.

## Minimal Implementation Plan Used

I chose the contract's two-surface docs-only option:

1. Refresh `README.md` as the concise current front door.
2. Create `docs/private_local_v1_operator_guide.md` as the detailed operator
   launch guide.
3. Produce this comparison handoff.

No code, tests, setup scripts, launcher behavior, runtime behavior, schemas,
frontend behavior, parser behavior, workbook behavior, Apps Script behavior,
Google Sheets behavior, AI behavior, release tags, installers, upgrade flows,
uninstall flows, or local folders were changed.

## Files Changed

- `README.md`
- `docs/private_local_v1_operator_guide.md`
- `docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md`

The untracked contract artifact remains part of the #274 package:

- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`

## Exact Sections Changed

### `README.md`

Replaced stale README content with current sections:

- `Current Shape`
- `Truth Boundaries`
- `Private-Local-V1 Path`
- `Local App Surfaces`
- `Google Sheets And Legacy Transport`
- `Local Data And Privacy`
- `Development`
- `Current Non-Claims`

Key README changes:

- reframed Mythic Edge as a private local MTG Arena analytics and review app;
- linked to `docs/private_local_v1_operator_guide.md`;
- documented parser truth ownership;
- documented private-local-v1 package mode, release ref, symbolic install root,
  app checkout root, data root, local SQLite path, and loopback URLs;
- moved Google Sheets/App Script wording to downstream or legacy transport;
- replaced the stale four-thread workflow wording with current governance
  pointers;
- listed explicit non-claims.

### `docs/private_local_v1_operator_guide.md`

Created sections:

- `Quick Terms`
- `Current Release Profile`
- `Local Folder Layout`
- `Setup Command Shapes`
- `Launch Shape`
- `Local Analytics And SQLite`
- `Manual JSONL Import`
- `Live Player.log Mode`
- `Analytics Views`
- `Match Journal`
- `Google Sheets And Workbook Surfaces`
- `Privacy And Never-Commit Rules`
- `Safe Troubleshooting`
- `Explicit Non-Claims`

The guide documents only existing command shapes from
`tools/dev_app/setup_private_local_v1.ps1`:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -NoOpen -StopAfterVerify -JsonReport
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -JsonReport
```

## Change Type

- Code changed: no
- Tests changed: no
- Docs-only: yes
- README-only: no
- Operator-guide-only: no
- Governance/release-docs only: yes

## Validation Run

Initial docs validation before this handoff was created:

```powershell
git diff --check
py tools\check_agent_docs.py
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
README.md
docs/private_local_v1_operator_guide.md
docs/contracts/private_local_v1_operator_readme_launch_guide.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Initial results:

- `git diff --check` -> passed
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0
- path-scoped secret/private-marker scan over README, guide, and contract ->
  passed, forbidden 0, warnings 0
- path-scoped protected-surface scan over README, guide, and contract ->
  passed, forbidden 0, warnings 0

Final validation including this handoff:

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

Final results:

- `git status --short --branch --untracked-files=all` -> branch
  `codex/analytics-foundation`; modified `README.md`; untracked #274 contract,
  operator guide, and implementation handoff.
- `git diff --check` -> passed
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0
- `py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation`
  -> passed, changed_paths 0 because untracked docs are not included by the
  base diff
- `py tools\check_secret_patterns.py --base origin/codex/analytics-foundation`
  -> passed, scanned_paths 0 because untracked docs are not included by the
  base diff
- path-scoped protected-surface scan over README, guide, contract, and handoff
  -> passed, changed_paths 4, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over README, guide, contract, and
  handoff -> passed, scanned_paths 4, forbidden 0, warnings 0

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the four intended #274 files
reported forbidden 0 and warnings 0.

## Secret / Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the four intended #274
files reported forbidden 0 and warnings 0.

## Generated Artifact Status

No generated/private/runtime/local artifacts were created intentionally. No
SQLite database files, frontend build output, local app data, raw logs, private
JSONL artifacts, workbook exports, secrets, credentials, provider keys, or
environment files were added.

## Manual Verification

- Documented command shapes exist in `tools/dev_app/setup_private_local_v1.ps1`
  and are forwarded to `tools/dev_app/private_local_v1_setup.py`.
- Documented default release ref and package mode match
  `tools/dev_app/private_local_v1_setup.py`.
- Documented backend and frontend ports match `tools/dev_app/dev_app_launcher.py`.
- Docs use symbolic install paths rather than machine-specific raw paths.
- Docs include explicit non-claims for public release readiness, production
  readiness, release tags, release branches, installers, upgrade/uninstall
  tooling, AI/coaching, and strategic/gameplay truth.
- Docs do not instruct deletion, cleanup, reset, upgrade, or uninstall.

## Remaining Risks Or Unverified Layers

- Live browser smoke was not run; this docs slice does not require app launch.
- Full repository tests were not run because no code changed.
- Real default install root was not inspected or mutated.
- Public-release, production, v1.0 tag, release branch, installer, upgrade, and
  uninstall readiness remain unclaimed.

## Forbidden Scope Status

Forbidden scope touched: no.

No setup scripts, launcher code, parser code, parser state reconciliation,
event classes, match/game identity, deduplication, analytics schema/migrations,
local app runtime/frontend behavior, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets behavior, production behavior,
OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior,
release tags, release branches, installers, upgrade flows, uninstall flows, or
local folders were changed.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #274.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/274

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_operator_readme_launch_guide.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md

Files to review:
- README.md
- docs/private_local_v1_operator_guide.md
- docs/contracts/private_local_v1_operator_readme_launch_guide.md
- docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md

Goal:
Review the #274 docs-only implementation against the contract. Lead with findings ordered by severity. Verify that the root README is now a concise private-local-v1 front door, the operator guide accurately documents existing setup/launch command shapes and local folder boundaries, and no docs overclaim public release readiness, production readiness, AI/coaching, parser truth, analytics truth, workbook truth, or cleanup behavior.

Check especially:
- command shapes match tools/dev_app/setup_private_local_v1.ps1 and tools/dev_app/private_local_v1_setup.py;
- package mode remains managed_full_checkout;
- default release ref remains codex/analytics-foundation;
- symbolic install root, app root, data root, SQLite path, backend URL, and frontend URL are accurate;
- README de-emphasizes Google-Sheets-first framing without changing workbook behavior;
- guide uses beginner-facing definitions;
- docs do not expose raw/private/generated artifacts, raw paths, raw payloads, raw hashes, secrets, credentials, endpoint values, or environment values;
- docs do not add destructive cleanup, upgrade, uninstall, release-tag, release-branch, installer, or production guidance;
- parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior remains unchanged.

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

Do not edit files unless routing to Codex D is necessary. Do not stage, commit, push, open a PR, merge, close issue #274, or mark tracker #136 complete unless explicitly asked.
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/274"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_operator_readme_launch_guide.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md"
  files_changed:
    - "README.md"
    - "docs/private_local_v1_operator_guide.md"
    - "docs/implementation_handoffs/private_local_v1_operator_readme_launch_guide_comparison.md"
  docs_only: true
  validation:
    - "git diff --check -> passed before handoff creation"
    - "py tools/check_agent_docs.py -> passed before handoff creation"
    - "path-scoped protected-surface scan over README/guide/contract -> passed"
    - "path-scoped secret/private-marker scan over README/guide/contract -> passed"
    - "git status --short --branch --untracked-files=all -> expected #274 modified/untracked docs"
    - "final git diff --check -> passed"
    - "final py tools/check_agent_docs.py -> passed"
    - "base protected-surface scan -> passed with changed_paths 0 because untracked docs are not included by base diff"
    - "base secret/private-marker scan -> passed with scanned_paths 0 because untracked docs are not included by base diff"
    - "path-scoped protected-surface scan over README/guide/contract/handoff -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over README/guide/contract/handoff -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
```
