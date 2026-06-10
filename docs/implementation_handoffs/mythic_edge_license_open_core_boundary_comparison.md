# Mythic Edge License And Open-Core Boundary Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/332

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/mythic_edge_license_open_core_boundary.md`

## Internal Project Area

Quality / Governance.

## Truth Owner

The reviewed repository source artifacts own the project license posture:

- root `LICENSE`;
- `pyproject.toml` license metadata;
- `README.md` license/open-core summary;
- `LICENSE_POLICY.md`.

This implementation does not provide legal advice.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
issue #332 -> license/open-core contract -> docs and package metadata -> Codex E review
```

Forbidden reverse flow:

- license docs do not authorize parser behavior changes;
- package metadata does not imply public release readiness;
- open-core policy does not implement external services, account flows,
  production deployment, model-provider runtime behavior, AI/coaching behavior,
  or Line Tracer behavior;
- repo license docs do not claim private/generated/local artifacts are source.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/module_contract.md`
- `docs/contracts/mythic_edge_license_open_core_boundary.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/internal_project_map.md`
- `README.md`
- `pyproject.toml`
- `frontend/package.json`
- root license/notice file search results
- GitHub issue #332
- tracker #136 status

## Current Behavior Compared To Contract

Contract expectation:

- root `LICENSE` exists and contains Apache-2.0 text;
- `pyproject.toml` license metadata says `Apache-2.0`;
- README includes concise license/open-core language;
- a policy document exists unless README alone can carry the boundary cleanly;
- private/generated/local artifacts, trademarks, future services, and legal
  non-claims are explicit;
- no `NOTICE` file is added without a current notice requirement;
- no runtime product behavior changes are included.

Observed before implementation:

- `pyproject.toml` declared `license = "MIT"`;
- no root `LICENSE`, `LICENCE`, `COPYING`, or `NOTICE` file was present;
- README documented private-local-v1 and privacy boundaries, but did not define
  the repository license or open-core service boundary;
- `frontend/package.json` is private and has no project license field;
- no current notice requirement was identified during the scoped inspection.

Gap:

- package metadata and repo-level license posture were inconsistent because the
  package advertised MIT while the repo had no root license file or policy.

## Implementation Option Chosen

Implemented the contract's recommended Apache-2.0 path:

- added root `LICENSE` with Apache License 2.0 text;
- changed `pyproject.toml` license metadata from `MIT` to `Apache-2.0`;
- added a concise README section named `License And Open-Core Boundary`;
- added `LICENSE_POLICY.md` so project-specific boundary language stays out of
  the legal license text;
- deferred `NOTICE` because no current project-specific or third-party notice
  requirement was found in this slice.

## Files Changed

- `LICENSE`
- `LICENSE_POLICY.md`
- `README.md`
- `pyproject.toml`
- `docs/contracts/mythic_edge_license_open_core_boundary.md`
- `docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md`

## Exact Sections Changed

### `LICENSE`

- Added root Apache License 2.0 text.
- Kept project-specific open-core language out of the legal license file.
- Left the official appendix text unmodified; no project-specific copyright
  owner was inserted because the contract listed that as an open question.

### `pyproject.toml`

- Updated `[project]` license metadata:

```toml
license = "Apache-2.0"
```

- No dependency, package name, import root, package data, script entrypoint, or
  optional dependency changes were made.

### `README.md`

- Added `License And Open-Core Boundary`.
- Linked `LICENSE` and `LICENSE_POLICY.md`.
- Stated that committed public/local source is Apache-2.0.
- Stated that the local parser, analytics, app, setup tooling, tests, and docs
  are the local open core.
- Stated that generated/private/local artifacts are not source and must not be
  committed.
- Stated that future separately offered services may be separate.
- Preserved non-claims for legal advice, public release readiness, production
  readiness, and service promises.

### `LICENSE_POLICY.md`

- Added `What Is Licensed`.
- Added `Local Open Core`.
- Added `Future Separately Offered Services`.
- Added `Private And Generated Data`.
- Added `Trademarks And Brand Assets`.
- Added `No Legal Advice`.
- Added `Current Non-Claims`.

### Contract And Handoff

- Preserved the untracked Codex B contract as part of the #332 scope.
- Added this implementation handoff.

## Code Changed

No runtime code changed.

## Tests Added Or Updated

No tests were added or updated. The contract did not require tests for this
docs/package metadata slice.

## Interface Changes

Package metadata changed from MIT to Apache-2.0.

No function signatures, API payloads, workbook columns, environment variables,
scripts, backend routes, frontend routes, parser outputs, analytics schema, or
runtime behavior changed.

## Contracted Area Status

Stayed inside Quality / Governance and package metadata.

No parser, runtime, analytics, local app, workbook, webhook, Apps Script,
Google Sheets, OpenAI/model-provider, AI/coaching, Line Tracer, output
transport, production, or local/private artifact behavior was changed.

## Validation Run

```text
git status --short --branch --untracked-files=all -> branch codex/license-open-core-boundary-332; changed README.md and pyproject.toml; untracked LICENSE, LICENSE_POLICY.md, contract, and handoff
py -c "import tomllib; data=tomllib.load(open('pyproject.toml','rb')); print(data['project']['license'])" -> Apache-2.0
py -m pip install -e . --dry-run -> passed; editable metadata prepared and package would install
git diff --check -> passed
new-file whitespace/final-newline/ascii check -> passed
py tools\check_agent_docs.py -> passed; errors 0, warnings 0
path-scoped protected-surface scan over changed files -> passed; forbidden 0, warnings 0
path-scoped secret/private-marker scan over changed files -> passed; forbidden 0, warnings 0
```

## Protected-Surface Status

Passed.

Path-scoped scan over changed files reported forbidden 0 and warnings 0.

No protected runtime surface was touched.

## Secret / Private-Marker Status

Passed.

Path-scoped scan over changed files reported forbidden 0 and warnings 0.

No secrets, raw logs, private JSONL artifacts, generated SQLite databases,
runtime files, failed posts, workbook exports, app-data files, environment
values, or local-only artifacts were added.

## Generated / Private Artifact Status

No generated/private/local artifacts were created or committed.

No `NOTICE` file was added because this implementation did not identify a
current notice requirement.

## Still Unverified

- Legal suitability remains unverified and outside Codex scope.
- Exact copyright owner/header choice remains unverified; the root license
  keeps the official license text and does not insert a project-specific owner.
- Third-party dependency license audit remains a future maturity task.
- Public release readiness and production readiness remain unclaimed.
- GitHub Actions were not run in Codex C.

## Reviewer Focus

Codex E should verify:

- Apache-2.0 adoption matches issue #332 and the contract;
- no MIT half-state remains in project license metadata;
- README and `LICENSE_POLICY.md` do not modify or weaken the Apache-2.0 license
  text;
- service-boundary language preserves future optional services without
  implementing or promising them;
- generated/private/local artifacts and trademarks are excluded by policy
  without making legal-advice claims;
- no unrelated CodeQL/security remediation or runtime behavior changes leaked
  into this slice.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #332.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/332

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/license-open-core-boundary-332

Base branch:
codex/analytics-foundation

Contract:
docs/contracts/mythic_edge_license_open_core_boundary.md

Implementation handoff:
docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md

Risk tier:
Medium

Goal:
Review the #332 license/open-core implementation against the contract. Verify
that the package now has a coherent Apache-2.0 root license, matching
`pyproject.toml` metadata, concise README language, and a project-specific
open-core policy without legal-advice claims or runtime behavior changes.

Review:
- LICENSE
- LICENSE_POLICY.md
- README.md
- pyproject.toml
- docs/contracts/mythic_edge_license_open_core_boundary.md
- docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md

Verify:
- root LICENSE exists and contains Apache-2.0 text;
- pyproject.toml metadata is Apache-2.0, not MIT;
- README links LICENSE and LICENSE_POLICY.md and stays concise;
- LICENSE_POLICY.md explains local open core, future separately offered services,
  private/generated data, trademarks, no legal advice, and current non-claims;
- NOTICE remains absent with a documented rationale;
- no runtime code, parser behavior, analytics behavior, local app behavior,
  workbook/webhook/App Script/Sheets behavior, model-provider/AI/coaching behavior,
  production behavior, CodeQL remediation, secrets, raw logs, generated data,
  or local-only artifacts are included.

Validation:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools\check_agent_docs.py
- packaging metadata check or TOML parse for pyproject license metadata
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Do not:
- treat this as legal advice;
- target main;
- implement fixes in Codex E unless explicitly asked;
- stage, commit, push, open a PR, merge, close #332, or mark tracker #136
  complete unless explicitly asked.

Output:
- findings first, ordered by severity;
- contract-test verdict;
- validation run;
- protected-surface status;
- secret/private-marker status;
- remaining risks;
- next recommended role, likely Codex F if review is clean or Codex D if
  concrete findings exist;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/332"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/mythic_edge_license_open_core_boundary.md"
  target_artifact: "docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md"
  risk_tier: "Medium"
  branch: "codex/license-open-core-boundary-332"
  base_branch: "codex/analytics-foundation"
  isolated_worktree: true
  validation:
    - "pyproject.toml TOML parse -> Apache-2.0"
    - "py -m pip install -e . --dry-run -> passed"
    - "git diff --check -> passed"
    - "new-file whitespace/final-newline/ascii check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not treat this as legal advice."
    - "Do not target main."
    - "Do not mix unrelated CodeQL/security remediation changes into this license slice."
    - "Do not change parser/runtime/analytics/local-app/workbook/webhook/App Script/Sheets/output transport/model-provider/AI/coaching/production behavior."
    - "Do not touch secrets, raw logs, private JSONL artifacts, generated databases, runtime files, failed posts, workbook exports, app-data files, or local-only artifacts."
```
