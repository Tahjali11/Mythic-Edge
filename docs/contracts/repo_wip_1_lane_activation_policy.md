# Repo WIP-1 Lane Activation Policy Contract

## Module

Repo-scoped WIP-1 lane activation governance for Mythic Edge.

## Source Issue

- https://github.com/Tahjali11/Mythic-Edge/issues/543
- Codex H synthesis comment on issue #543:
  https://github.com/Tahjali11/Mythic-Edge/issues/543#issuecomment-4763165913

## Tracker

N/A.

## Owning Layer

Repository coordination and agent workflow.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- External / Collaboration Surface, because GitHub issues, PRs, comments,
  trackers, and Codex threads are coordination surfaces.
- Generated / Local Artifacts, because local worktrees and local workflow
  indexes may provide evidence but do not own repo authority.

## Truth Owner

Repo authority for lane activation is owned by current user instructions,
`AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, current
GitHub issues, current contracts, accepted ADRs, reviewed PRs, and merge
evidence.

Local worktree names, stale prompts, local status indexes, local Codex skills,
handoffs, and chat memory are evidence only. They must not override current
GitHub issue/PR state, branch state, accepted ADRs, or active repo governance.

## Bridge-Code Status

`not_bridge_code`

This is workflow governance. It does not bridge runtime data between project
layers and does not authorize parser, runtime, workbook, webhook, Apps Script,
analytics, AI, release, deploy, or production behavior changes.

## Risk Tier

High.

Reason: this changes durable workflow intake policy and should become an ADR
plus authority-doc/template updates before later threads treat it as active
governance.

## Files Owned By This Contract

This contract owns the proposed docs-only governance implementation scope for:

- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/decisions/README.md`
- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_rules.yml`
- `docs/templates/problem_representation.md`
- `docs/templates/workflow_handoff.md`

Protected surface authorization: `workflow_authority_docs` changes to the
listed governance docs and templates are explicitly authorized for the WIP-1
lane activation policy only.

This contract does not authorize edits to sibling repositories, runtime code,
parser code, workbook/App Script assets, CI gate behavior, deployment policy,
local worktrees, stale issue comments, historical PR bodies, or old handoffs.

Optional later surfaces, not authorized in this issue:

- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/templates/current_status.md`
- workflow-status indexes or local status reports
- checkers or enforcement tooling beyond validation commands
- sibling-repo adoption issues or PRs

## Public Interface

The public governance interface is a WIP-1 lane activation vocabulary and
metadata pattern that future Mythic Edge prompts, issue bodies, contracts, and
handoffs may cite.

Codex C should add a proposed ADR and narrow docs/template updates that expose:

- the repo default of one active issue/lane per repository;
- canonical lane status terms;
- canonical named exceptions;
- required exception metadata;
- active-slot clearing conditions;
- ADR numbering behavior;
- sibling-repo adoption as future watch-list work only.

The public machine-readable handoff interface should gain a small optional
`lane_activation` block. The exact field placement belongs to Codex C's docs
implementation pass, but it must support this shape:

```yaml
lane_activation:
  repo: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "https://github.com/Tahjali11/Mythic-Edge/issues/543"
  lane_status: "active"
  tracker_selected_next_lane: ""
  exception:
    name: ""
    blocked_active_issue_or_pr: ""
    reason: ""
    allowed_scope: ""
    expiration_condition: ""
    authorized_by: ""
    recorded_in: ""
```

Allowed `lane_status` values:

- `active`
- `parked`
- `deferred`
- `tracker_selected_next_lane`
- `blocked_no_current_work`
- `blocked_current_work_expected`
- `cancelled`
- `complete`

## Inputs

### Current governance sources

Type: committed docs and current GitHub issue/comment context.

Required sources:

- issue #543 problem representation;
- Codex H synthesis comment on issue #543;
- `AGENTS.md`;
- `docs/agent_constitution.md`;
- `docs/codex_module_workflow.md`;
- `docs/agent_rules.yml`;
- `docs/templates/problem_representation.md`;
- `docs/templates/workflow_handoff.md`;
- `docs/decisions/README.md`;
- `docs/decisions/ADR_TEMPLATE.md`;
- `docs/decisions/ADR-0001` through `docs/decisions/ADR-0007`.

### Repo state

Type: current git and GitHub state.

Required checks before Codex C edits:

- local checkout remote normalizes to
  `https://github.com/Tahjali11/Mythic-Edge`;
- working branch is based on current `main`;
- no `docs/decisions/ADR-0008-*.md` exists unless the user explicitly
  reserved or directed a different ADR number;
- issue #543 is still the source issue for this policy.

## Outputs

### Proposed ADR-0008

Type: committed markdown decision record.

Destination:

- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`

Required state:

- `Status: Proposed`
- related issue #543;
- related contract:
  `docs/contracts/repo_wip_1_lane_activation_policy.md`;
- related ADRs at least ADR-0004, ADR-0005, and ADR-0006;
- explicit non-goals covering parser/runtime/workbook/webhook/App Script,
  analytics, AI, release, deploy, production, and sibling-repo adoption;
- explicit statement that WIP-1 is a repo coordination policy, not runtime
  product behavior.

### Governance docs and template amendments

Type: narrow docs-only updates.

Destinations:

- ADR index entry in `docs/decisions/README.md`;
- short entrypoint warning in `AGENTS.md`;
- constitution workflow/issue lifecycle policy in
  `docs/agent_constitution.md`;
- start/intake gate in `docs/codex_module_workflow.md`;
- machine-readable policy fields in `docs/agent_rules.yml`;
- optional prompt fields in `docs/templates/problem_representation.md`;
- optional `lane_activation` block in `docs/templates/workflow_handoff.md`.

These outputs are final docs once reviewed and merged. They do not create
runtime state.

## Canonical Policy

Default rule:

```text
Each Mythic Edge repository defaults to one active issue/lane at a time.
```

Exception rule:

```text
A second active lane may start only when a named exception is recorded with
the repository, reason, allowed scope, linked active or blocked issue/PR when
applicable, authorization source, record location, and expiration condition.
```

Parked/deferred rule:

```text
Parked or deferred issues do not count as active WIP when they are explicitly
recorded as parked or deferred and have no active PR, active implementation,
review, submission, deployment, or expected current-thread work.
```

Tracker queue rule:

```text
A tracker-selected next lane is queued work. It does not occupy the repo active
slot until a user or current workflow artifact starts it or explicitly assigns
it the active slot.
```

## Canonical Vocabulary

### `active_issue_or_lane`

The single repository work slot currently expected to receive Codex or human
implementation, review, submission, deployer, or closeout attention.

An active issue/lane may be represented by an issue, a tracker-selected child,
an active PR, a current contract/implementation/review path, or a user-directed
repo-scoped prompt.

### `parked_issue`

A valid issue intentionally paused with no current work expectation and no
active PR. Parking must be recorded in an issue comment, tracker comment,
handoff, contract, or PR note.

### `deferred_issue`

A valid future issue or follow-up outside the current active slot. A deferred
issue may be planned or queued, but it must not have current implementation,
review, submission, deployment, or PR work unless activated later.

### `active_pr`

An open PR that still expects review, fixes, submitter, deployer, closeout, or
tracker-update work.

An active PR normally occupies the same active slot as its source issue. If a
PR is open but no current work is expected, the lane must be explicitly parked
or deferred before it stops occupying the active slot.

### `active_worktree`

A local checkout or branch with possible work evidence. It may indicate a lane
needs cleanup or status classification, but it is not repo authority by
itself. A local worktree must not make a parked/deferred GitHub issue active
without current issue, PR, contract, or user instruction evidence.

### `tracker_selected_next_lane`

Work selected by a tracker as the next candidate. It is a queue decision, not
an active-slot assignment, until a user or workflow artifact starts the lane.

### `active_slot_exception`

A named, scoped, expiring permission for more than one active lane in the same
repository.

## Named Exceptions

Codex C should encode the following canonical exception names:

- `security_hotfix`: urgent security vulnerability or exploit mitigation.
- `privacy_or_raw_log_leak`: secrets, raw logs, private artifacts, or sensitive
  data leaked or at immediate risk.
- `data_loss_or_corruption`: active or likely data loss, corruption, or
  irreversible local artifact damage.
- `ci_blocking_all_work`: CI or validation infrastructure blocks all current
  repo progress and needs a narrow unblocker.
- `dependency_security_update`: security-relevant dependency update or
  advisory response.
- `blocked_lane_unblocker`: a narrow prerequisite needed to unblock the active
  lane, without broadening into a second feature lane.
- `repo_bootstrap_or_split`: temporary repo setup, split, or bootstrap work
  with an explicit finish condition.
- `explicit_user_override`: direct user instruction to run a second active
  lane, still requiring scope and expiration metadata.

These exceptions are permissions to start narrowly scoped work. They are not
permission to edit protected runtime surfaces, bypass review, merge, deploy,
or close trackers.

## Required Exception Metadata

Every `active_slot_exception` must record:

- `exception_name`
- `repository`
- `active_issue_or_lane`
- `blocked_active_issue_or_pr`, if any
- `reason`
- `allowed_scope`
- `expiration_condition`
- `authorized_by`
- `recorded_in`

Allowed `authorized_by` examples:

- current user instruction;
- current GitHub issue;
- current contract;
- accepted ADR;
- deployer closeout or tracker update.

Allowed `recorded_in` examples:

- GitHub issue comment;
- tracker comment;
- PR body or PR comment;
- module contract;
- workflow handoff;
- proposed or accepted ADR.

Local-only notes, local worktree names, local status indexes, or chat memory
may support investigation, but they are not sufficient record locations for a
public repo exception.

## Active-Slot Clearing Conditions

An active slot is cleared only when one of these is recorded:

- source issue is closed after merge/deployer closeout;
- source PR is merged and completion evidence is recorded;
- source PR is closed and the issue is cancelled, parked, deferred, or routed
  to a different active slot;
- lane is explicitly parked or deferred with no active PR and no current
  implementation, review, submission, or deployment expectation;
- lane is blocked awaiting external or user evidence and current work is
  explicitly paused;
- separate `blocked_lane_unblocker` exception is opened for a narrow unblocker;
- user explicitly cancels, reassigns, or overrides the active slot;
- `repo_bootstrap_or_split` reaches its recorded expiration condition;
- stale local worktree is classified as local cleanup only and no GitHub issue
  or PR remains active.

When none of these conditions is recorded, continuing threads should treat the
lane as still active or route to Codex A/B for status reconciliation.

## ADR Numbering Policy

Codex C should create:

```text
docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md
```

unless the user explicitly reserves ADR numbers or directs a different number.

If an `ADR-0008-*` file exists when Codex C starts, Codex C must stop before
creating another ADR and route to Codex B or the user for numbering
reconciliation. It must not silently skip to ADR-0009 or ADR-0010.

The ADR index in `docs/decisions/README.md` must be updated only after the ADR
file is added.

## Sibling-Repo Adoption Boundary

This issue governs the `Tahjali11/Mythic-Edge` repository only.

The policy should be written so it can be adopted by sibling Mythic Edge repos
later, but Codex C must not create, edit, label, or close sibling-repo issues
or PRs in this implementation.

Sibling-repo adoption is watch-list/future work for repos such as:

- `Tahjali11/Mythic-Edge-Automation-Artifacts`
- `Tahjali11/Mythic-Edge-Analytics`
- future Mythic Edge repos

Each sibling repo needs its own repo-scoped handoff, issue, contract, or
explicit user instruction before mutation.

## Invariants

- WIP-1 is repo scoped, not machine scoped.
- A tracker-selected next lane is not active by default.
- Parked and deferred issues do not occupy WIP only when the no-current-work
  state is explicit.
- An active PR normally keeps the source lane active until merged, closed, or
  explicitly parked/deferred.
- Named exceptions must be scoped and expiring.
- `explicit_user_override` is valid, but it still requires metadata.
- Local worktrees and local status indexes are evidence, not authority.
- Sibling repo references are read-only unless explicitly authorized.
- The policy must not rewrite historical issue comments, PR bodies, or old
  handoffs.
- The policy must not change parser/runtime/workbook/webhook/App Script,
  analytics, AI, CI gate, release, deploy, or production behavior.

## Error Behavior

- Missing repository identity in a handoff: hard stop before mutation and ask
  for a repo-scoped handoff.
- Checkout remote mismatch: hard stop before reading beyond approved reference
  scope, editing, staging, committing, pushing, cleaning, stashing, resetting,
  deleting, or otherwise mutating repo content.
- Existing active lane found with no valid exception: stop new work and route
  to Codex A/B for lane reconciliation or ask the user for an explicit
  override.
- Ambiguous parked/deferred status: treat the lane as active until an issue,
  tracker, PR, contract, or user instruction records otherwise.
- Existing ADR-0008 file found: stop ADR creation and route for numbering
  reconciliation.
- Contract conflicts with accepted ADRs: route to Codex A/B unless the current
  issue and contract explicitly authorize ADR amendment or supersession.

## Side Effects

Allowed Codex C side effects:

- add the proposed ADR file;
- update ADR index and governance docs/templates listed in this contract;
- produce an implementation handoff under `docs/implementation_handoffs/`;
- run docs validation and static scans.

Forbidden side effects:

- runtime code edits;
- parser behavior edits;
- workbook/webhook/App Script edits;
- analytics or AI behavior edits;
- CI gate or deploy policy changes;
- sibling-repo edits;
- GitHub issue or PR lifecycle changes other than references in docs;
- staging, committing, pushing, opening PRs, merging, closing, or relabeling,
  unless a later Codex F/G prompt explicitly authorizes that role.

## Dependency Order

Codex C should edit in this order:

1. Verify checkout remote, branch, and ADR numbering.
2. Draft `ADR-0008-repo-wip-1-lane-activation-policy.md` from
   `docs/decisions/ADR_TEMPLATE.md`.
3. Add the ADR index row in `docs/decisions/README.md`.
4. Add terse entrypoint guidance in `AGENTS.md`.
5. Add durable workflow language in `docs/agent_constitution.md`.
6. Add the start/intake gate in `docs/codex_module_workflow.md`.
7. Add machine-readable vocabulary in `docs/agent_rules.yml`.
8. Add optional fields to `docs/templates/problem_representation.md`.
9. Add optional `lane_activation` block guidance to
   `docs/templates/workflow_handoff.md`.
10. Write the implementation handoff.
11. Run validation.

## Compatibility

Older handoffs and issue bodies without `lane_activation` metadata remain
valid historical artifacts. Continuing threads should verify current repo
state live before mutation.

Existing `freshness` metadata in handoffs remains advisory and should not be
removed. The new lane-activation vocabulary complements freshness checks; it
does not replace repository identity, branch, issue, tracker, or local dirty
state checks.

Existing role routing A-G and H remains unchanged. This policy adds a start
gate; it does not change implementation, review, submitter, or deployer role
authority.

## Tests Required

Codex C should run:

```bash
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

For the path-fed commands, Codex C should pass only the docs files changed in
the implementation package.

Runtime unit tests are not required for this docs-only contract unless Codex C
changes code or validation tooling against this contract. This contract does
not authorize code or tooling changes.

## Acceptance Criteria

- A proposed ADR-0008 exists unless the user explicitly reserved or skipped
  the number.
- The ADR index includes the proposed ADR.
- WIP-1 default, canonical vocabulary, named exceptions, metadata, and active
  slot clearing conditions are documented in the governance docs.
- Problem representation and workflow handoff templates expose optional
  active-slot and exception metadata without local absolute paths.
- Sibling-repo adoption is documented as future watch-list work only.
- Protected-surface non-claims are explicit.
- Validation commands are run or any skipped check is explained.
- No runtime code, parser behavior, workbook/webhook/App Script behavior,
  analytics behavior, AI behavior, CI gates, deploy policy, production
  behavior, sibling repos, historical comments, or old handoffs are changed.

## Open Questions Or Contract Risks

- Existing open issues/PRs may need a later inventory pass after ADR adoption;
  this contract does not classify or close them.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` may later need WIP-1 fields,
  but this contract keeps that out of V1 to avoid changing GitHub issue form
  behavior without a narrower implementation review.
- A future warning tool could help detect WIP-1 conflicts, but tooling must not
  become authoritative over GitHub issue/PR/repo governance without its own
  issue and contract.
- `explicit_user_override` is intentionally allowed, but reviewers should
  reject override metadata that lacks scope or expiration.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #543.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/543

Base branch:
main

Contract:
docs/contracts/repo_wip_1_lane_activation_policy.md

Goal:
Implement the docs-only WIP-1 repo lane activation governance package exactly
as contracted. Create proposed ADR-0008 unless the user explicitly reserved or
skipped ADR numbers, then make narrow governance/template updates for WIP-1
lane activation vocabulary, named exceptions, exception metadata, and active
slot clearing conditions.

Required target files:
- docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md
- docs/decisions/README.md
- AGENTS.md
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_rules.yml
- docs/templates/problem_representation.md
- docs/templates/workflow_handoff.md
- docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md

Before editing:
1. Verify the local checkout remote normalizes to
   https://github.com/Tahjali11/Mythic-Edge.
2. Fetch origin and verify the branch is based on current main.
3. Verify no ADR-0008 file already exists. If one exists, stop and route to
   Codex B or the user for numbering reconciliation.
4. Inspect issue #543, the Codex H synthesis comment, and the contract.

Protected boundaries:
- Do not edit runtime code.
- Do not change parser behavior, parser state final reconciliation, parser
  event classes, workbook schema, webhook payload shape, Apps Script behavior,
  analytics behavior, AI/model-provider behavior, CI gates, release policy,
  deploy policy, production behavior, secrets, raw logs, generated/private
  artifacts, or local-only files.
- Do not create sibling-repo adoption issues or PRs.
- Do not rewrite historical issue comments, PR bodies, or old handoffs.
- Do not stage, commit, push, open a PR, merge, close, or relabel anything.
- Do not skip ADR-0008 unless the user explicitly reserves or redirects ADR
  numbering.

Validation:
- python3 tools/check_agent_docs.py
- git diff --check
- path-fed secret, protected-surface, and validation-selector checks for the
  changed docs files

Expected output:
- docs-only implementation completed
- implementation handoff written
- validation summary
- remaining risks
- recommended next role
- workflow_handoff block with repository and repository_url
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/543"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Issue #543 problem representation plus Codex H constitutional synthesis comment"
  target_artifact: "docs/contracts/repo_wip_1_lane_activation_policy.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  internal_project_area: "Quality / Governance"
  truth_owner: "Current user instructions, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, current GitHub issues, current contracts, accepted ADRs, reviewed PRs, and merge evidence own repo lane activation authority. Local worktrees, local status indexes, skills, and handoffs are evidence only."
  bridge_code_status: "not_bridge_code"
  validation:
    - "Verified local main and origin/main at 871b4f6b7e573ac96e715705b5cda5c7f6a61de5 before writing the contract."
    - "Verified docs/contracts/repo_wip_1_lane_activation_policy.md did not already exist."
    - "Verified docs/decisions currently contains ADR-0001 through ADR-0007 and ADR-0008 is missing."
    - "Inspected issue #543 and Codex H synthesis comment."
    - "Inspected AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/templates/problem_representation.md, docs/templates/workflow_handoff.md, docs/decisions/README.md, docs/decisions/ADR_TEMPLATE.md, and ADR-0001 through ADR-0007."
    - "Ran git diff --check."
    - "Ran python3 tools/check_agent_docs.py."
    - "Ran python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin for docs/contracts/repo_wip_1_lane_activation_policy.md."
    - "Ran python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin for docs/contracts/repo_wip_1_lane_activation_policy.md."
    - "Ran python3 tools/select_validation.py --base origin/main --paths-from-stdin for docs/contracts/repo_wip_1_lane_activation_policy.md."
    - "Ran ASCII and local-absolute-path marker scan on docs/contracts/repo_wip_1_lane_activation_policy.md."
  stop_conditions:
    - "Do not skip ADR-0008 unless the user explicitly reserves or redirects ADR numbering."
    - "Do not create sibling-repo adoption issues or PRs."
    - "Do not edit runtime code."
    - "Do not change parser/runtime/workbook/webhook/App Script/analytics/AI behavior, CI gates, release policy, deploy policy, production behavior, secrets, raw logs, generated/private artifacts, or local-only files."
    - "Do not make local worktrees, stale prompts, local status indexes, skills, or handoffs authoritative over GitHub issue/PR/repo governance."
    - "Do not close, relabel, stage, commit, push, open PRs, merge, mutate worktrees, mutate stashes, or alter automations."
```
