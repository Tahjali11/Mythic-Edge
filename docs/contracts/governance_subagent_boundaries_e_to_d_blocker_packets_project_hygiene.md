# Governance Subagent Boundaries, E-to-D Blocker Packets, And Project Hygiene Contract

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/682>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Target artifact:
`docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`

Stash source reference:
`stash@{0}: cleanup: preserve governance issue 682 source hunks 2026-07-06`

Stash inspection performed for this contract: metadata and file list only.

## Module

`governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene`

This contract defines a docs-only governance policy package for three related
workflow concerns:

1. subagent boundaries;
2. Codex E to Codex D blocker packets;
3. GitHub Project hygiene for lane metadata.

Plain English: helper agents can be useful, but they must stay helpers. They do
not become new Mythic Edge roles, do not own verdicts, and do not get merge,
deploy, parser-truth, readiness, or authorization power. When Codex E sends
work to Codex D, E must leave a concrete blocker packet so D fixes a known
finding instead of guessing. GitHub Project fields can help coordination, but
they are status labels, not the source of truth.

This contract does not edit authority docs or templates. It defines the later
docs implementation boundary only.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/682
- Project roadmap / tracker: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Target artifact:
  `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`

## Source Artifacts Inspected

- GitHub issue #682
- GitHub issue #568
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/module_fixer.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/implementation_handoff.md`
- `docs/internal_project_map.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `stash@{0}` metadata and file list only

The stash patch contents were not inspected, applied, copied, or dropped.
No authority docs, templates, parser code, EventBus code, API code, frontend
code, workbook/webhook files, CI files, GitHub Project fields, issues, PRs,
branches, commits, or stash entries were mutated.

## Stash Boundary

The preserved stash is source provenance, not repo authority.

Allowed use in this Codex B contract:

- cite the stash name as the preservation source;
- inspect stash metadata and file lists only;
- classify which families of paths may be considered by a later implementation;
- define what stale or unrelated source material must be rejected.

Forbidden use in this Codex B contract:

- apply the stash;
- drop the stash;
- inspect patch hunks;
- copy stash wording into authority docs;
- treat stash content as accepted repo policy;
- treat stash content as authority over current issues, current contracts,
  accepted ADRs, merged PRs, or current `origin/main`.

The metadata-only file list contains these governance/template surfaces:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/*`
- `docs/templates/*`

Issue #682 also records stale source material that must not be adopted from
the stash if encountered by any later implementation:

- a stale `docs/project_roadmap.md` edit that treated #388 as the active
  ordering gate;
- an older untracked copy of
  `docs/contracts/parser_parity_gre_annotation_semantics.md`, now superseded
  by the committed contract on `main`.

Those stale materials are rejected for this governance lane.

## Owning Layer

Primary layer: Quality / Governance.

This contract covers workflow role boundaries, review-to-fixer handoff shape,
template guidance, and GitHub Project hygiene. It does not cover parser truth,
EventBus behavior, API payloads, frontend behavior, live-capture behavior,
workbook/webhook behavior, Apps Script behavior, CI behavior, deployment, or
production behavior.

## Internal Project Area

Quality / Governance.

## Truth Owner

- Current repo authority docs, accepted ADRs, active GitHub issues, active
  contracts, reviewed handoffs, reviewed reports, PRs, and merge records own
  workflow authority.
- The future docs implementation, if authorized, may clarify authority docs and
  templates. It must not use local stash material, memory, subagent output, or
  GitHub Project fields as higher authority than current repo artifacts.
- GitHub issues, PRs, commits, and reviewed repo artifacts remain stronger
  truth than GitHub Project field values.
- Subagent output is evidence for the active role to synthesize. It is not
  final workflow authority.

## Bridge-Code Status

`not_bridge_code`

This is a governance policy contract. It does not bridge parser, runtime,
analytics, workbook, webhook, UI, or deployment layers.

## Files Owned By This Contract

- `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`

Governance surfaces named by this contract for possible later implementation:

1. `AGENTS.md`
2. `docs/agent_constitution.md`
3. `docs/agent_rules.yml`
4. `docs/codex_module_workflow.md`
5. `docs/agent_threads/*`
6. `docs/templates/*`

This contract does not authorize edits to those six surfaces.

## Authorization State

The following flags remain false for issue #682 and for this Codex B pass:

```yaml
implementation_authorized: false
authority_doc_edits_authorized: false
agent_rules_edits_authorized: false
constitution_edits_authorized: false
template_edits_authorized: false
github_project_field_writes_authorized: false
subagent_tool_creation_authorized: false
subagent_authority_expansion_authorized: false
stash_apply_authorized: false
stash_drop_authorized: false
stash_hunk_inspection_authorized: false
parser_behavior_change_authorized: false
eventbus_behavior_change_authorized: false
api_payload_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
ci_change_authorized: false
deployment_change_authorized: false
readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

Any later handoff that flips one of these flags without a reviewed issue,
contract, explicit owner routing, and validation must fail closed.

## Current Behavior

Current repo governance already defines A-G workflow roles, Codex H as an
auxiliary constitutional role, artifact-first handoffs, WIP-1 lane activation,
protected surfaces, external tool boundaries, and tracker hygiene.

Current docs do not yet fully codify these #682 topics:

- subagents as optional assistants inside an active role;
- explicit authorization required before subagent use;
- Codex D as patch owner even when helpers assist;
- Codex E as reviewer/verdict owner even when helpers assist;
- Codex H as synthesis owner with optional read-only source-coverage help;
- durable detailed blocker packets when Codex E routes to Codex D;
- optional E-to-D blocker-packet blocks in handoffs/templates;
- GitHub Project field hygiene for `Lane State`, `Wave`, `Next Role`, and
  `Blocked By / Join Gate`.

## Problem Statement And First Bad Values

The intended behavior is a small governance clarification that reduces
workflow ambiguity without adding unbounded ceremony.

The first bad value is treating a subagent as a new Mythic Edge role or as an
authority that can stage, commit, merge, deploy, create issues, change flags,
or own final review verdicts.

The second bad value is routing from Codex E to Codex D without a concrete
finding packet. That leaves D guessing whether the problem is code, contract,
test, CI, repo drift, or scope ambiguity.

The third bad value is using GitHub Project fields as the source of truth for
lane state, blocker status, or merge readiness. Project fields are coordination
metadata only.

The fourth bad value is applying local stash hunks wholesale into authority
docs, especially when the stash is known to have contained stale roadmap or
superseded contract material.

## Decision Overview

This contract separates the three policy topics so a later implementation may
accept, revise, or defer them independently:

| Topic | Contract decision | Later implementation surface |
| --- | --- | --- |
| Subagent boundaries | Accept as governance policy, scoped as helper-only evidence. | `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, `docs/codex_module_workflow.md`, relevant role docs. |
| E-to-D blocker packets | Accept as required when Codex E routes to Codex D. | `docs/codex_module_workflow.md`, `docs/agent_threads/review.md`, `docs/agent_threads/contract_test.md`, `docs/agent_threads/module_fixer.md`, relevant templates. |
| GitHub Project hygiene | Accept as optional/contextual handoff metadata, not every handoff. | `docs/codex_module_workflow.md`, `docs/templates/workflow_handoff.md`, role docs for A/F/G/E where relevant. |

GitHub Project hygiene fields should not be mandatory in every handoff.
Instead, they should be optional but expected when lane state, project-board
routing, blockers, PR submission, or deployer closeout are materially relevant.
This keeps low-risk docs-only or local fixes from carrying noisy project-field
ceremony while preserving project-field clarity for workflow coordination.

## Subagent Boundary Contract

Allowed subagent role:

- optional helper inside the active Codex role;
- evidence gatherer, source coverage assistant, bounded review lens, or
  parallel inspection aide when explicitly requested or authorized;
- producer of notes the active role may synthesize.

Forbidden subagent role:

- new canonical workflow role;
- substitute for Codex A-G or H;
- owner of issue scope, contract decisions, implementation decisions,
  reviewer severity, final verdict, submitter staging, PR creation, merge,
  deploy, tracker closure, authorization flags, parser truth, readiness,
  security assurance, or privacy assurance.

Subagent use requires one of:

- explicit user request in the active thread;
- explicit issue authorization;
- explicit contract authorization;
- explicit handoff authorization.

If no authorization exists, the active role may not invent subagent work.

### Codex D With Subagents

Codex D remains patch owner.

Subagents may help Codex D only as bounded assistants, such as:

- read-only reproduction notes;
- nearby test inspection;
- adjacent-risk review;
- post-patch validation;
- disjoint-file edit assistance only when the issue or contract explicitly
  authorizes parallel edits and Codex D names file ownership before editing.

Codex D must synthesize helper output, choose the fix, make or approve the
patch, and produce the final handoff. Subagent output must not become the
implementation handoff by itself.

### Codex E With Subagents

Codex E remains reviewer, severity, and routing owner.

Subagents may help Codex E only as bounded review lenses, such as:

- security/privacy lens;
- parser truth ownership lens;
- contract continuity lens;
- test gap lens;
- drift lens;
- maintainability lens.

Codex E must synthesize findings, assign severity, decide blocking status, and
route the next role. Subagents may not issue final findings or overrule Codex
E.

### Codex H With Subagents

Codex H remains constitutional synthesis owner.

Subagents may help Codex H only with authorized read-only source coverage,
inventory, or classification support. Codex H must still produce the source
coverage table or note, current-status classification, amendment quality test,
rule-type classification, ceremony assessment, and final synthesis.

Subagents may not rewrite authority docs, adopt amendments, bypass A-G roles,
or promote advisory synthesis into accepted policy.

## Subagent Evidence Packet

When subagent output is cited in a durable artifact, the active role should
summarize it with public-safe fields:

| Field | Requirement |
| --- | --- |
| `subagent_scope` | Bounded task or lens. |
| `authorized_by` | User request, issue, contract, or handoff. |
| `files_or_sources_reviewed` | Public-safe list, no private paths or secrets. |
| `edits_performed` | Usually `none`; any edit requires explicit authority and disjoint scope. |
| `finding_or_observation_summary` | Evidence summary, not final verdict. |
| `confidence` | `high`, `medium`, `low`, or `unknown`. |
| `active_role_synthesis` | How the main role used or rejected the output. |

Subagent packets must not include private values, secrets, raw logs, local
paths, exploit payloads, private evidence, or unstated authority flags.

## E-to-D Blocker Packet Contract

When Codex E routes to Codex D, Codex E must leave a durable blocker packet.
The blocker packet may live in a review report, PR review/comment, issue
comment, contract-test report, or final handoff, depending on the active lane.

Required blocker-packet fields:

| Field | Requirement |
| --- | --- |
| `finding_id` | Stable id for the blocker. |
| `severity` | Clear severity label. |
| `blocking_status` | `blocking`, `non_blocking`, or `not_blocking`. |
| `source_issue` | Issue being reviewed. |
| `source_artifact` | Contract, handoff, PR, diff, or report reviewed. |
| `affected_surface` | File, section, function, command, schema, or artifact. |
| `expected_behavior` | What the contract or issue required. |
| `actual_behavior` | What review found. |
| `evidence` | Concrete public-safe evidence or failing check. |
| `fault_category` | `implementation`, `test_gap`, `validation_failure`, `ci_failure`, `repo_drift`, `contract_ambiguity`, `scope_mismatch`, or `environment_setup`. |
| `why_route_to_d` | Why the issue is concrete enough for Codex D instead of A or B. |
| `fix_boundary` | Exact allowed D scope. |
| `forbidden_changes` | Protected surfaces D must not touch. |
| `validation_for_d` | Focused checks D should run. |
| `return_route` | Usually Codex E after D. |
| `pasteable_codex_d_prompt` | Prompt D can use without reconstructing context from chat. |
| `workflow_handoff` | Machine-readable continuation block. |

If the issue is not concrete enough for D, Codex E must route to Codex B for
contract clarification or Codex A for reframing. Codex E must not send vague
"fix this" instructions to D.

## Template Placement Decision

The E-to-D blocker-packet block should be added later as an optional section
where it naturally belongs:

- `docs/templates/contract_test_report.md`: primary home for contract-test
  findings and follow-up after fixes;
- `docs/templates/workflow_handoff.md`: optional continuation block when E
  routes directly to D;
- `docs/templates/implementation_handoff.md`: optional D-return summary when D
  records how it addressed an E blocker;
- role docs for review, contract-test, and fixer roles.

It should not be mandatory in every template. It is required only when E routes
to D.

## GitHub Project Hygiene Contract

Project fields covered by this contract:

- `Lane State`
- `Wave`
- `Next Role`
- `Blocked By / Join Gate`

Allowed use:

- record or summarize project-field status when relevant to lane routing;
- route a needed project-field update to Codex G, Codex F, or another
  authorized role when tooling or permissions are not available;
- include project-field state in handoffs as context;
- state when project-field state is unknown, unavailable, stale, or not
  applicable.

Forbidden use:

- treat project fields as source of truth over issues, PRs, commits, contracts,
  accepted ADRs, or reviewed handoffs;
- write project fields without explicit authorization;
- use project fields to close issues, merge PRs, activate lanes, claim
  readiness, or override workflow authority;
- let missing project access block local docs-only work unless the current
  issue makes project update evidence required.

Project-field status vocabulary:

- `project_fields_updated`: authorized write occurred and evidence is linked.
- `project_fields_checked_no_update_needed`: fields were inspected and already
  match current issue/PR state.
- `project_fields_update_routed`: update is needed but routed to an authorized
  role or owner.
- `project_fields_unavailable`: tooling, permissions, or project access were
  unavailable.
- `project_fields_unknown`: fields were not checked.
- `project_fields_not_applicable`: project metadata is not relevant to this
  lane.

For issue #682, `github_project_field_writes_authorized` remains false.

## Project Hygiene Fallback Behavior

When project-field writes are unavailable or unauthorized, the role should
prefer a public-safe fallback in this order:

1. record the needed update in the issue or PR comment when the workflow
   authorizes comments;
2. record the needed update in the durable handoff;
3. route to Codex G or the owner for project-field update authority;
4. state `project_fields_unavailable` or `project_fields_update_routed`.

The fallback must name the source issue or PR, the desired field state, why the
field could not be updated directly, and the next owner or role. It must not
claim the project was updated when it was only routed.

## Public Interface

This contract defines future governance documentation interfaces only:

- subagent boundary vocabulary;
- subagent evidence packet fields;
- E-to-D blocker-packet fields;
- GitHub Project hygiene field vocabulary;
- project-field fallback vocabulary;
- route labels and non-claim flags.

No runtime public interface, parser interface, EventBus interface, API payload,
frontend behavior, workbook/webhook behavior, Apps Script behavior, CLI
behavior, or CI behavior is changed.

## Inputs

Allowed inputs:

- current GitHub issue #682;
- current tracker #568;
- current repo authority docs and templates on the active branch;
- accepted ADRs;
- stash metadata and file list only;
- public-safe issue, PR, and contract history.

Forbidden inputs:

- stash patch hunks in this Codex B pass;
- wholesale stash application;
- stale roadmap stash material;
- superseded GRE annotation contract material;
- private logs;
- raw runtime artifacts;
- generated data;
- secrets, credentials, tokens, endpoint values, or private local paths;
- GitHub Project field writes;
- private source snippets or raw diffs outside the current repo authority
  review scope.

## Outputs

Output of this Codex B pass:

- one contract artifact under `docs/contracts/`;
- summary and workflow handoff.

Possible later outputs after separate authorization:

- narrow authority-doc edits to the six named surfaces;
- narrow template edits for optional blocker-packet and project-hygiene
  fields;
- implementation handoff comparing the accepted contract to edited docs;
- Codex E review or contract-test report.

## Invariants

- Subagents are helper evidence surfaces, not workflow roles or authority.
- The active Codex role owns synthesis, decisions, routing, and final handoff.
- Codex D owns patches and final D handoffs.
- Codex E owns review findings, severity, blocking status, and routing.
- Codex H owns constitutional synthesis and does not directly edit authority
  docs.
- E-to-D routing requires a durable blocker packet.
- GitHub Project fields are coordination metadata, not issue/PR/contract
  truth.
- Project-field writes require explicit authorization.
- Stash material is provenance only until normalized through current issue,
  contract, implementation, review, and PR flow.
- Stale roadmap and superseded GRE contract material are rejected.

## Error Behavior

Fail closed and route back to Codex B or A when:

- subagent authority is ambiguous;
- a subagent is treated as final role owner;
- E-to-D routing lacks a concrete blocker packet;
- a finding lacks evidence, expected behavior, actual behavior, or fix
  boundary;
- project-field status is treated as stronger than GitHub issue/PR truth;
- project-field writes are attempted without authorization;
- stash hunks are applied or copied without implementation authority;
- stale roadmap or superseded GRE material appears in proposed changes;
- the proposed implementation touches parser, EventBus, API, frontend,
  live-capture, workbook/webhook, Apps Script, CI, deployment, production, or
  private evidence surfaces.

## Side Effects

This contract writes only:

- `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`

No authority docs, templates, code, tests, CI, GitHub Projects, issues, PRs,
branches, commits, stash entries, parser/runtime surfaces, or private
artifacts are changed by this contract.

## Dependency Order

If this contract is accepted, later implementation should proceed in this
order:

1. Codex E reviews this contract.
2. Codex F submits the reviewed contract if E finds no blockers.
3. Codex G merges/closes/updates only after explicit deployer routing.
4. A later Codex A/B or explicit owner route authorizes implementation edits
   to authority docs/templates.
5. Codex C edits only the reviewed surfaces and ignores stale stash material.
6. Codex E reviews the authority-doc/template implementation.
7. Codex F/G handle submission and merge only after review.

## Compatibility

This contract preserves:

- A-G role names and order;
- Codex H auxiliary status;
- WIP-1 lane policy;
- artifact-first handoffs;
- current public-safe handoff rules;
- current authority order;
- current ADR policy;
- current protected-surface and truth-ownership rules;
- current template flat-layout policy.

It does not promote subagents to roles, does not create new mandatory workflow
steps for every thread, and does not require GitHub Project fields in every
handoff.

## Tests Required

Validation for this Codex B contract:

```bash
git diff --check
python3 tools/check_agent_docs.py
printf "%s\n" docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf "%s\n" docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf "%s\n" docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Recommended hygiene checks:

```bash
LC_ALL=C grep -n '[^ -~]' docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md
tail -c 1 docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md | od -An -t x1
rg -n '[ \t]$' docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md
```

Validation for a later authority-doc/template implementation should include:

```bash
git diff --check
python3 tools/check_agent_docs.py
printf "%s\n" <changed-paths> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Codex E should also review that the implementation edits only the six named
governance surfaces, rejects stale stash material, keeps subagents helper-only,
requires E-to-D blocker packets, and treats project fields as metadata only.

## Acceptance Criteria

- Contract artifact exists at the target path.
- The six governance surfaces are named.
- Subagent assistance, E-to-D blocker packets, and GitHub Project hygiene are
  separable decisions.
- Subagents remain evidence helpers only.
- Codex E remains final owner of review severity, blocking status, and routing.
- Codex D remains patch owner.
- Codex H remains synthesis owner and may use only authorized read-only helper
  support.
- E-to-D blocker-packet fields are defined.
- `Lane State`, `Wave`, `Next Role`, and `Blocked By / Join Gate` are named as
  GitHub Project hygiene fields.
- Project-field fallback behavior is defined.
- Project-field writes remain unauthorized by this contract.
- Stale roadmap and superseded GRE annotation stash material are rejected.
- No parser, EventBus, API, frontend, live-capture, workbook/webhook, Apps
  Script, CI, deployment, production, readiness, parser-truth, security, or
  privacy assurance claims are made.

## Open Questions And Contract Risks

- Later implementation must decide exact wording placement across the six
  surfaces. This contract recommends narrow placement but does not edit those
  files.
- GitHub Project field names may differ by project configuration. If the field
  labels differ, later roles should map them explicitly instead of guessing.
- If future subagent tooling gains edit capabilities, a separate issue and
  contract must decide whether Mythic Edge allows that for any role.
- If Codex E routes to D from a GitHub PR review instead of a report artifact,
  the blocker packet may live in a PR comment or review thread, but it must
  still include the required fields or link to an artifact that does.

## Non-Claims

This contract does not claim:

- implementation readiness;
- authority-doc edit authority;
- template edit authority;
- GitHub Project write authority;
- subagent execution authority;
- subagent tool creation authority;
- parser truth;
- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- production readiness.

## Recommended Next Role

Next role: Codex E - Module Reviewer.

Codex E should review this contract against issue #682, current governance
docs, current templates, accepted ADRs, and the stated stash boundary. If no
blockers remain, route to Codex F for docs-only contract submission. Do not
route directly to authority-doc implementation unless a later owner route
explicitly authorizes that scope.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #682.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/682

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Target artifact:
docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md

Review goal:
Review the contract-only governance policy for subagent boundaries, E-to-D
blocker packets, and GitHub Project hygiene. Verify that it names the six
governance surfaces, keeps subagents as evidence helpers only, preserves Codex
E as reviewer/verdict owner, preserves Codex D as patch owner, keeps Codex H
advisory/synthesis-only, defines E-to-D blocker-packet requirements, treats
GitHub Project fields as metadata only, defines fallback behavior, rejects
stale roadmap and superseded GRE stash material, and does not authorize
authority-doc edits, template edits, project-field writes, parser/runtime
behavior changes, readiness claims, security assurance, privacy assurance, or
parser truth claims.

Protected boundaries:
Do not implement code, edit authority docs, edit templates, apply/drop/inspect
stash hunks, write GitHub Project fields, change parser/EventBus/API/frontend/
live-capture/workbook/webhook/Apps Script/CI/deployment behavior, or claim
readiness/security/privacy/parser truth.

Expected output:
Findings first. State whether the contract is ready for Codex F submission,
needs Codex B clarification, or is blocked. Include validation reviewed,
remaining risk, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/682"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  verdict: "governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene_contract_ready_for_review"
  target_artifact: "docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md"
  stash_source: "stash@{0}: cleanup: preserve governance issue 682 source hunks 2026-07-06"
  stash_inspection: "metadata_and_file_list_only"
  stash_applied: false
  stash_dropped: false
  implementation_authorized: false
  authority_doc_edits_authorized: false
  agent_rules_edits_authorized: false
  constitution_edits_authorized: false
  template_edits_authorized: false
  github_project_field_writes_authorized: false
  subagent_tool_creation_authorized: false
  subagent_authority_expansion_authorized: false
  parser_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  api_payload_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  deployment_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
