# Mythic Edge License And Open-Core Boundary Contract

## Module

`mythic_edge_license_open_core_boundary`

Plain English: this contract defines the intended license posture for Mythic
Edge's public/local source code and the boundary between the local core and
possible future separately offered services.

This is a Codex B contract-writing artifact only. It is not legal advice. It
does not implement license-file changes, package metadata changes, external
services, account flows, model-provider runtime behavior, production
deployment, or parser/runtime behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/332
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Current intended branch: `codex/analytics-foundation`
- Contract artifact:
  `docs/contracts/mythic_edge_license_open_core_boundary.md`

Required authority and role docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Tracker

Engineering maturity tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 must remain open after this contract. License/open-core work is one
governance/release-readiness slice, not completion of the full maturity tracker.

## Risk Tier

Medium.

Reasons:

- this is governance and release-readiness documentation, not runtime code;
- the repo currently has package license metadata but no root license file;
- license metadata, README language, and open-core service language must stay
  consistent;
- overclaiming legal, public-release, production, or service promises
  would create project risk;
- mixing this scope with unrelated CodeQL/security remediation work would make
  review and submission unsafe.

## Owning Layer

Quality / Governance.

This contract owns licensing documentation, package metadata expectations, and
the project policy boundary for open local source versus future services. It
does not own parser truth, analytics truth, local app runtime truth, deployment
truth, service strategy, or legal advice.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- External / Collaboration Surface, because GitHub and public repository
  presentation are collaboration surfaces;
- Generated / Local Artifacts, because the license boundary must exclude
  private/generated/local artifacts from source distribution claims;
- Future AI Integration, only as a deferred boundary for possible future
  model-provider work. Naming that area here does not authorize model-provider
  runtime integration.

## Truth Owner

The repo's license posture is owned by the reviewed source artifacts that future
implementation will add or update:

- root `LICENSE`;
- `pyproject.toml` license metadata;
- root `README.md` license/open-core summary;
- optional `LICENSE_POLICY.md` or equivalent policy document.

GitHub issue #332 and this contract own the implementation scope and acceptance
criteria. They do not substitute for legal advice.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
Issue #332 problem representation
  -> Codex B license/open-core contract
  -> Codex C docs/metadata implementation
  -> Codex E contract review
  -> Codex F/G submission and lifecycle handling
```

Forbidden reverse flow:

- license/open-core docs must not authorize parser behavior changes;
- package metadata changes must not imply public release readiness by
  themselves;
- future service-boundary language must not authorize external service,
  account, model-provider, production, Google Sheets, or deployment behavior;
- repo license language must not imply that private user data, raw logs,
  generated databases, secrets, local artifacts, trademarks, logos, service
  infrastructure, or production configs are public source artifacts.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/mythic_edge_license_open_core_boundary.md`

Future Codex C may edit, if approved by this contract:

- `LICENSE`
- `pyproject.toml`
- `README.md`
- `LICENSE_POLICY.md`

Future Codex C may create `NOTICE` only if inspection identifies a current
project-specific notice or third-party notice requirement that belongs in the
repo now. Otherwise `NOTICE` should remain deferred.

Codex C must not edit runtime code, parser code, analytics behavior, local app
UI/backend behavior, workbook/webhook/App Script/Sheets behavior, external
service code, account code, model-provider runtime code, secrets, raw logs,
generated data, or local-only artifacts.

## Current License-State Finding

Observed during Codex B inspection:

- `pyproject.toml` currently declares:

```toml
license = "MIT"
```

- No root `LICENSE`, `LICENCE`, `COPYING`, or `NOTICE` file was present.
- `README.md` describes the private-local-v1 shape and non-claims, but does not
  currently define a repo license or open-core service boundary.
- `docs/contracts/private_local_v1_package_footprint_release_ref.md` notes that
  future slim package/public/shared release work should include license and
  release metadata.
- `docs/contracts/engineering_maturity_index_open_framework.md` identifies
  dependency and license visibility as part of public-open-source release
  maturity.

This is a mismatch: package metadata advertises MIT while the repository lacks
a root license file and policy explanation.

## License Decision Recommendation

Recommended decision:

- adopt Apache License 2.0 for the public/local Mythic Edge source code;
- update `pyproject.toml` license metadata from `MIT` to `Apache-2.0` in the
  same implementation change that adds the root `LICENSE`;
- include a short README license section that links to the root `LICENSE` and
  open-core policy;
- add `LICENSE_POLICY.md` to explain project-specific boundaries in plain
  English without modifying the Apache-2.0 license text.

Rationale:

- Apache-2.0 is permissive and compatible with a free local source project;
- Apache-2.0 includes explicit patent-license language, which is useful for a
  project that may later become public and service-adjacent;
- Apache-2.0 does not prevent future separately offered services from remaining
  separate from the local open core;
- Apache-2.0 is clearer than leaving MIT metadata without a root license file.

If Codex C or the user decides MIT is preferred instead, route back to Codex B
because that changes the central recommendation of this contract.

## Public / Local Open-Core Boundary

The public/local open core should include the source needed for a user or
developer to run Mythic Edge locally under the repo license.

Included source families:

- local MTGA parser code;
- parser-owned fact normalization;
- parser diagnostics and evidence/provenance support;
- local SQLite analytics schema, migrations, ingest, and deterministic views;
- local FastAPI backend;
- local React/Vite frontend source;
- manual JSONL import support;
- live Player.log capture into local SQLite;
- Match Journal local functionality;
- local analytics and decision-support views;
- private-local-v1 setup/launcher tooling needed for local use;
- tests, docs, contracts, workflow templates, and validation tooling that are
  committed source artifacts;
- package metadata and dependency manifests.

This open-core boundary preserves the current README framing: Mythic Edge is a
private local MTG Arena analytics and review app, and the local tool remains the
basic free/open source experience.

## Future Separately Offered Service Boundary

Future separately offered services may be separate from the local open core.

This contract intentionally does not describe their feature set, methods,
infrastructure, pricing, availability, or operating model.

This contract does not implement or authorize those services. It only preserves
room for them by saying the repo license for the local open core does not
promise that every future service layer, account system, deployment
configuration, operations artifact, model-provider workflow, or production
infrastructure artifact will be public source.

Any future external-service/account/model-provider/production-facing work needs
its own issue, contract, privacy boundary, credential policy, data-retention
policy, and explicit user approval.

## Excluded Assets, Data, And Infrastructure Boundary

The repo license and open-core policy must clearly exclude or reserve:

- private user data;
- raw MTGA `Player.log` files;
- private JSONL import artifacts;
- generated SQLite databases and sidecar files;
- local app data roots;
- runtime logs;
- failed posts;
- workbook exports;
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, and
  environment values;
- production configs and private deployment infrastructure;
- service account data;
- service operations data;
- trademarks, logos, brand assets, and domain names unless a future policy
  explicitly licenses them;
- generated/local-only artifacts that are not committed source.

The policy must avoid implying that private/local/generated files become
licensed source merely because they are produced by Mythic Edge.

## Root License File Contract

Future Codex C should add a root `LICENSE` file using the official Apache-2.0
license text.

Requirements:

- do not hand-edit the legal license text except for standard copyright/header
  fields if the license form requires them;
- do not add project-specific open-core explanations inside `LICENSE`;
- keep project-specific explanation in README and/or `LICENSE_POLICY.md`;
- preserve ASCII/plain-text formatting unless the official source text requires
  otherwise.

## Package Metadata Contract

Future Codex C should update `pyproject.toml` license metadata only after or at
the same time as adding root `LICENSE`.

Required behavior:

- metadata must no longer say MIT if the project adopts Apache-2.0;
- package metadata should use the repo's existing build backend conventions
  unless a packaging warning requires a narrow compatibility adjustment;
- package metadata changes must not change dependencies, package names, import
  roots, package data, entry points, optional dependencies, or build behavior
  beyond license metadata.

Expected target metadata:

```toml
license = "Apache-2.0"
```

If current packaging validation rejects that shape, Codex C should use the
smallest packaging-compatible Apache-2.0 metadata form and document the reason
in the implementation handoff.

## README Contract

Future Codex C should add a short README section named `License` or
`License And Open-Core Boundary`.

Required content:

- Mythic Edge's committed public/local source is licensed under Apache-2.0;
- the local parser, local analytics, local app, setup tooling, tests, and docs
  are part of the local open core;
- generated/private/local artifacts are not source and must not be committed;
- future separately offered services may be separate;
- license docs are not public-release, production, or legal-advice claims.

The README section should stay concise and link to `LICENSE` and
`LICENSE_POLICY.md` if that policy file is added.

## License Policy Document Contract

Future Codex C should add `LICENSE_POLICY.md` unless the implementation thread
finds the README can explain the boundary cleanly without a separate file.

Preferred `LICENSE_POLICY.md` sections:

- `What Is Licensed`
- `Local Open Core`
- `Future Separately Offered Services`
- `Private And Generated Data`
- `Trademarks And Brand Assets`
- `No Legal Advice`
- `Current Non-Claims`

The policy file must not weaken the Apache-2.0 license text. It should explain
project scope, not invent a custom license.

## NOTICE Decision

Do not add a `NOTICE` file in the first implementation unless Codex C identifies
a current notice requirement.

Reasons:

- no existing root notice file is present;
- this contract does not inspect or change third-party dependency licensing;
- an empty or vague NOTICE file would add process without evidence;
- future third-party attribution or branding policy can add NOTICE under a
  separate issue if needed.

## Compatibility

Existing package metadata currently says MIT. The future implementation should
treat that as legacy metadata to be replaced, not as a durable project decision.

The migration must avoid a half-state:

- do not add Apache-2.0 README language while leaving `pyproject.toml` as MIT;
- do not update `pyproject.toml` away from MIT without adding a root `LICENSE`;
- do not claim service-boundary policy without a README or policy explanation.

## Protected Surfaces

This contract must not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema or migrations;
- local app backend/frontend behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider runtime behavior;
- AI coaching, hidden-card inference, player-mistake labels, best-line advice,
  or Line Tracer behavior;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  environment values, raw logs, private JSONL artifacts, generated SQLite
  databases, runtime files, failed posts, workbook exports, app-data files, or
  local-only artifacts.

## Validation Requirements

Codex C should run:

```powershell
git status --short --branch --untracked-files=all
git diff --check
py tools\check_agent_docs.py
```

If `pyproject.toml` changes, Codex C should also run the smallest available
packaging metadata validation. Acceptable options include:

```powershell
py -m pip install -e . --dry-run
```

If the local pip version does not support `--dry-run`, Codex C may instead run a
non-mutating TOML parse or the smallest existing packaging/config test and must
document the limitation.

Path-scoped safety scans should run over changed files:

```powershell
@'
LICENSE
LICENSE_POLICY.md
README.md
pyproject.toml
docs/contracts/mythic_edge_license_open_core_boundary.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
LICENSE
LICENSE_POLICY.md
README.md
pyproject.toml
docs/contracts/mythic_edge_license_open_core_boundary.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Codex C should adjust the path list to files actually changed.

## Acceptance Criteria

- Root `LICENSE` exists and contains Apache-2.0 text.
- `pyproject.toml` license metadata matches Apache-2.0.
- README includes concise license/open-core language.
- `LICENSE_POLICY.md` exists or the implementation handoff justifies keeping
  the boundary in README only.
- `NOTICE` is either absent with rationale or present with specific current
  notice requirements.
- Public/local open core is defined without restricting the basic local tool.
- Future separately offered service boundary is defined without implementing or
  promising services.
- Excluded private/generated/local artifacts are named.
- Trademark/logo/brand assets are not accidentally licensed by implication.
- No runtime product behavior changes are included.
- Validation is recorded.

## Open Questions / Contract Risks

- The exact copyright owner/header text for the root `LICENSE`
  should be confirmed by the user or current repo convention during Codex C.
- If packaging tooling warns that `license = "Apache-2.0"` is not the preferred
  metadata shape, Codex C should make the smallest compatible metadata change
  and document it.
- This contract does not perform a third-party dependency license audit.
  Dependency/license visibility beyond the project license remains a future
  maturity task if needed.
- This contract does not define pricing, service terms, privacy policy, terms
  of service, trademark policy, or service data-retention policy.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/332

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source contract:
docs/contracts/mythic_edge_license_open_core_boundary.md

Current branch:
codex/license-open-core-boundary-332

Base branch:
codex/analytics-foundation

Goal:
Implement the license/open-core docs and metadata slice defined by the contract.

Expected implementation handoff:
docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- issue #332
- tracker #136
- docs/contracts/mythic_edge_license_open_core_boundary.md
- README.md
- pyproject.toml
- docs/contracts/engineering_maturity_index_open_framework.md
- docs/contracts/private_local_v1_package_footprint_release_ref.md
- any root LICENSE, LICENCE, COPYING, NOTICE, or license-policy files if present

Implement only:
- root Apache-2.0 LICENSE file;
- pyproject.toml license metadata alignment;
- concise README license/open-core section;
- LICENSE_POLICY.md if needed to keep README concise;
- implementation handoff.

Do not:
- treat this as legal advice;
- target main;
- implement external services, account flows, production deployment,
  model-provider runtime behavior, AI coaching, or Line Tracer behavior;
- change parser behavior, analytics behavior, local app/UI behavior, workbook
  schema, webhook payload shape, Apps Script behavior, Google Sheets behavior,
  output transport, or production behavior;
- touch secrets, credentials, raw logs, private JSONL artifacts, generated
  SQLite databases, runtime files, failed posts, workbook exports, app-data
  files, environment values, or local-only artifacts;
- mix unrelated CodeQL/security remediation changes into this license slice.

Validation:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools\check_agent_docs.py
- packaging metadata validation if pyproject.toml changes
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final output:
- role performed
- issue/tracker used
- contract used
- implementation handoff path
- files changed
- license/open-core changes made
- validation run
- protected-surface and secret/private-marker status
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/332"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/mythic_edge_license_open_core_boundary.md"
  target_artifact: "docs/implementation_handoffs/mythic_edge_license_open_core_boundary_comparison.md"
  risk_tier: "Medium"
  branch: "codex/license-open-core-boundary-332"
  base_branch: "codex/analytics-foundation"
  isolated_worktree: true
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git diff --check -- docs\\contracts\\mythic_edge_license_open_core_boundary.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not treat this as legal advice."
    - "Do not target main."
    - "Do not implement external service, account, production, model-provider, AI/coaching, or Line Tracer behavior."
    - "Do not change parser/runtime/analytics/local-app/workbook/webhook/App Script/Sheets/output transport behavior."
    - "Do not touch secrets, raw logs, private JSONL artifacts, generated databases, runtime files, failed posts, workbook exports, app-data files, or local-only artifacts."
    - "Do not mix unrelated CodeQL/security remediation changes into this license slice."
```
