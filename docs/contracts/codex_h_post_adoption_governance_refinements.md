# Codex H Post-Adoption Governance Refinements Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/76

Follow-up issue: not yet provided. If implementation proceeds through a PR,
use a new follow-up issue when practical, or use `Refs #76` rather than
`Closes #76` because issue #76 is already closed.

Tracker: N/A

Branch target: `main`

Source artifact:

- Codex H synthesis handoff for post-adoption A-G feedback packets
- Codex H synthesis handoff for final constitutional amendment review packets
- Issue #76 comments and completion record
- PR #77 merge record
- Recent constitution feedback packet noting stale observed-state risk
- Final feedback packets that route E2, Pyright, and hardening-suite closure
  concerns into post-adoption governance refinement

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/module_contract.md`
- `docs/templates/constitution_feedback_packet.md`
- `docs/templates/workflow_handoff.md`

Related hardening governance contracts:

- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- `docs/contracts/code_hardening_pyright_advisory.md`

Related ADRs:

- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

This is a contract-writing artifact only. It does not implement the
refinement, rewrite authority docs, create feedback round storage, make
feedback rounds mandatory, promote E2 to permanent-role status, make Pyright a
required gate, change main-target approval gates, change
parser/runtime/workbook/webhook/App Script behavior, change CI gates, open a
PR, close issues, or merge anything.

## Module

Post-adoption governance refinements for Codex H / Constitutional Lawyer.

Plain English: after Codex H was adopted by PR #77, future Codex H synthesis
needs a small extra guard. It should compare feedback packet recommendations
against the current repo before proposing amendments, so old observations that
have already been fixed are marked as satisfied or stale instead of being
treated as still-open gaps.

## Source Issue

Primary source record: https://github.com/Tahjali11/Mythic-Edge/issues/76

Issue #76 is closed as completed by PR #77. It should be treated as the
adoption record, not as an open tracker for unlimited follow-up work.

Related closed hardening records:

- Issue #72, independent test-authoring policy, is closed.
- Issue #33, code hardening suite tracker, is closed.

Those closed issues are historical context and precedent for the refinement.
They are not open implementation trackers for this contract.

If implementation proceeds beyond this contract, the preferred route is a new
follow-up issue that references #76. If the user explicitly keeps the work
under #76, PR language should use `Refs #76`, not `Closes #76`.

## Owning Layer

Owning layer: repository coordination and agent workflow governance.

Truth boundary:

- Codex H synthesis and feedback packets are workflow evidence.
- Current repo governance docs, accepted ADRs, current issues, current
  contracts, reviewed handoffs, reviewed PRs, and merged commits remain the
  authoritative sources.
- Historical packet observations are time-stamped evidence, not current truth.
- Parser/state ownership, workbook boundaries, webhook transport boundaries,
  Apps Script boundaries, deployment behavior, and protected runtime/data
  surfaces remain unchanged.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/codex_h_post_adoption_governance_refinements.md`

Expected future implementation files if Codex C is authorized:

- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`

Optional future implementation files only if a follow-up issue and
implementation plan justify them:

- `AGENTS.md`
- `docs/agent_constitution.md`

Codex C must keep edits narrow. It must not create raw feedback packet files,
formal feedback-round directories, ADRs, CI gates, parser tests, or production
behavior changes under this contract.

## Observed Current Behavior

Observed on `main` after PR #77:

- `git status --short --branch` reported `## main...origin/main`.
- Issue #76 is closed.
- PR #77 is merged into `main` at
  `14dee482f598db9ce6629e1cf1360b8cc633aaa6`.
- Issue #72 is closed.
- Issue #33 is closed.
- `docs/templates/constitution_feedback_packet.md` exists.
- `docs/agent_threads/constitutional_lawyer.md` exists.
- `AGENTS.md` references Codex H as an auxiliary governance synthesis role.
- `docs/agent_constitution.md` includes an auxiliary governance role section
  for Codex H.
- `docs/agent_rules.yml` includes `auxiliary_roles.H` and
  `constitution_feedback` entries.
- `docs/codex_module_workflow.md` says H is only for constitution feedback
  synthesis and that H output routes back to A/B/C depending on authorization.
- Raw feedback packet repo storage remains opt-in and formal-round-only.
- A-G remains the normal module implementation workflow.
- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
  defines E2 as an optional Codex E mode, not a permanent role.
- `docs/contracts/code_hardening_pyright_advisory.md` defines Pyright as
  advisory-first, not a required/failing gate.
- No committed contract-test report for the Codex H adoption was observed at
  `docs/contract_test_reports/codex_h_constitutional_lawyer_adoption.md`;
  issue #76 and PR #77 record the review/deployer evidence instead.

Observed gap:

- `docs/agent_threads/constitutional_lawyer.md` requires source coverage
  before synthesis, but it does not yet require Codex H to classify each
  packet recommendation against current repo state.
- `docs/templates/constitution_feedback_packet.md` defines raw packet fields,
  but it does not provide an optional field or instruction for later current
  status/adoption status classification.
- `docs/agent_rules.yml` encodes source coverage requirements, but not
  stale/satisfied/superseded packet classification.

## Public Interface

This contract creates no runtime public interface.

It defines a governance-documentation interface for Codex H synthesis:

- source coverage table
- current repo check
- packet recommendation status
- stale observation handling
- satisfied recommendation handling
- superseded recommendation handling
- unresolved active recommendation handling
- watch-list preservation

### Packet Recommendation Status

Codex H should classify every packet recommendation during synthesis using one
of these status labels:

- `active`: the recommendation still appears unsatisfied and in scope.
- `partially_satisfied`: the repo addresses part of the recommendation, but a
  scoped gap remains.
- `satisfied`: current repo docs, issue/PR records, or accepted artifacts
  already address the recommendation.
- `stale`: the packet's observed-state claim is no longer true and does not
  need a new amendment.
- `superseded`: a later accepted repo artifact, ADR, issue, PR, or contract
  replaces the recommendation.
- `conflict`: the recommendation conflicts with current authority, role
  boundaries, protected-surface rules, or accepted ADRs.
- `watch_list`: the recommendation is worth preserving but should not become
  an amendment yet.

Codex C may choose a shorter field name such as `current_status` or
`recommendation_status`, but the labels and meanings above should remain
recognizable.

### Source Coverage Table

The Codex H source coverage table should gain a current-status column.

Recommended columns after refinement:

- source role
- source thread or context
- main recommendation
- affected authority level
- evidence quote
- confidence
- conflicts or tensions
- routing recommendation
- current status

For a single-packet synthesis, a short source coverage note is still
acceptable, but it should include the current status.

### Current Repo Check

Before amendment synthesis, Codex H should check the current repo governance
state relevant to the packets. The check may be lightweight, but it must be
explicit.

Examples:

- verify whether named files now exist
- verify whether named role docs/templates/rule entries now include the
  requested behavior
- verify whether a referenced issue is open or closed
- verify whether a referenced PR is merged
- verify whether a recommendation is already covered by an accepted ADR or
  current contract

Codex H should not use stale packet observations as current repo facts when
the current repo is available to inspect.

## Inputs

Allowed inputs:

- current user handoff
- source feedback packets
- Codex H synthesis output
- issue #76 and PR #77 records
- follow-up issue, if opened
- current repo governance docs
- accepted ADRs
- current contracts, handoffs, reviews, and PRs
- local skills only as evidence when current repo docs do not already answer
  the question

Forbidden input reproduction:

- secrets
- webhook URLs
- API keys or tokens
- workbook IDs
- raw MTGA logs
- generated local artifacts
- runtime status files
- failed posts
- workbook exports
- unrelated private transcript dumps

## Outputs

Codex B output from this pass:

- `docs/contracts/codex_h_post_adoption_governance_refinements.md`

Expected Codex C output after this contract:

- `docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md`
- narrow docs/template/rule edits authorized by this contract

Expected Codex E output after implementation:

- `docs/contract_test_reports/codex_h_post_adoption_governance_refinements.md`
  or a PR review verifying the implementation against this contract

## Required Guarantees

### Current-State Classification

Codex H must distinguish:

- what a packet observed at collection time
- what the current repo now contains
- which recommendations are still active
- which recommendations have been satisfied
- which recommendations are stale or superseded
- which recommendations conflict with current authority
- which recommendations should remain watch-list items

This classification should happen before amendment synthesis.

### No Re-Adoption Of Issue #76

This refinement must not re-adopt Codex H from scratch.

Issue #76 and PR #77 already established:

- Codex H as an auxiliary advisory governance role
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`
- raw feedback packets as evidence, not authority
- formal feedback-round repo storage as opt-in and authorized-only
- A-G as the normal module workflow

Future implementation should modify only the narrow sections needed to add the
current-status classification guard.

### Closed Hardening Context Remains Historical

Issue #72 and issue #33 are closed. They may be cited as accepted workflow
context, but this contract must not reopen them as active implementation
trackers.

The independent test-authoring policy may inform Codex H classification and
watch-list decisions, but it must not be expanded here into a broader hardening
suite.

### E2 Remains Optional

This refinement must not promote E2 to a permanent role.

E2 remains an optional Codex E mode for high-risk independent test
identification or adversarial contract testing, only when a scoped issue and
contract require it.

### Pyright Remains Advisory

This refinement must not make Pyright required.

The Pyright advisory contract remains report-oriented unless a future issue,
contract, implementation, review, and approval path explicitly escalates it to
a failing gate.

### Feedback Rounds Remain Optional

This refinement must not make feedback rounds mandatory.

Raw feedback packets continue to default to pasteable output or GitHub issue
comments. Repo storage for raw packets remains formal-round-only and requires
explicit issue and contract authorization.

### Main-Target Gates Remain Intact

This refinement must not weaken `main` targeting, PR lifecycle, or merge
approval gates.

Issue #76 and this handoff authorize contract work on `main`, but that does
not make `main` the default target for unrelated workflow, module audit,
parser, runtime, workbook, or production-facing work.

### Codex H Remains Advisory

Codex H remains advisory. It may propose amendments, consolidations,
unresolved conflicts, watch-list items, and next-role routing. It must not
directly rewrite authority docs or bypass A/B/C/E/F/G implementation and PR
workflow.

## Invariants

- A-G remains the normal module implementation path.
- Codex H remains auxiliary governance synthesis.
- Current repo docs outrank stale packet observations.
- Raw packets and Codex H synthesis are evidence, not accepted authority.
- Feedback rounds are optional.
- Formal feedback-round repo storage requires explicit issue and contract
  authorization.
- Main-target approval gates remain unchanged.
- E2 remains optional Codex E mode unless a separate issue and contract change
  that status.
- Pyright remains advisory unless a separate issue and contract explicitly
  escalate it.
- Closed issues #72 and #33 remain historical records, not active trackers for
  this refinement.
- Parser truth ownership and protected runtime/data surfaces remain unchanged.

## Error Behavior

If Codex C cannot determine whether a packet recommendation is active,
satisfied, stale, superseded, conflicting, or watch-list, it should route back
to Codex B or leave the uncertainty explicit rather than inventing certainty.

If implementation attempts to make feedback rounds mandatory, Codex E should
treat that as a blocking contract mismatch.

If implementation weakens `main` approval gates, Codex E should treat that as
out of scope.

If implementation promotes E2 to permanent-role status, Codex E should treat
that as out of scope.

If implementation makes Pyright required or failing, Codex E should treat that
as out of scope.

If implementation treats closed issue #72 or closed tracker #33 as active
implementation trackers, Codex E should route back to Codex B or ask for a new
follow-up issue.

If implementation rewrites Codex H broadly or reopens the entire adoption
design, Codex E should route back to Codex A/B.

If implementation changes parser/runtime/workbook/webhook/App Script behavior,
Codex E should treat that as forbidden scope.

If implementation creates raw feedback packet files or formal round folders,
Codex E should treat that as forbidden scope unless a separate issue and
contract explicitly authorize it.

## Side Effects

This contract pass has only one intended side effect:

- create `docs/contracts/codex_h_post_adoption_governance_refinements.md`

Future implementation may edit only the governance docs and templates
authorized above.

Future implementation must not:

- create raw feedback packet files
- create formal feedback-round packet folders
- open or close issues
- open or merge PRs
- change runtime code
- change parser/runtime/workbook/webhook/App Script behavior
- change tests unrelated to docs validation
- change CI gates
- make Pyright required
- promote E2 to permanent-role status
- touch local artifacts, generated data, secrets, or workbook exports

## Dependency Order

Future implementation should proceed in this order:

1. Update `docs/agent_threads/constitutional_lawyer.md` to require current
   repo status classification during source coverage.
2. Update `docs/templates/constitution_feedback_packet.md` only if useful to
   document how Codex H may annotate packet status during synthesis. The raw
   packet collector should not be forced to know future status at collection
   time.
3. Update `docs/agent_rules.yml` with a terse machine-readable field for
   current-status classification.
4. Update `docs/codex_module_workflow.md` only if a concise routing note is
   needed.
5. Avoid editing `AGENTS.md` and `docs/agent_constitution.md` unless Codex C
   finds the refinement would otherwise be undiscoverable.
6. Write an implementation comparison handoff.
7. Route to Codex E for contract verification.

## Compatibility

Compatibility requirements:

- Existing Codex H prompts remain valid.
- Existing feedback packet template remains compact.
- Existing source coverage guard remains valid and gains only a current-status
  classification requirement.
- Existing issue-comment/pasteable default for raw packets remains valid.
- Existing formal-round storage policy remains opt-in.
- Existing A-G workflow remains unchanged.
- Existing branch and merge approval policy remains unchanged.
- Existing independent test-authoring policy remains closed historical
  hardening context unless a new follow-up issue reopens it.
- Existing Pyright advisory policy remains advisory.

## Protected Surfaces

This contract explicitly does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes, event kind values, or parser payload shapes
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- production deployment behavior
- merge-to-main policy
- CI failure gates
- Pyright required/failing gates
- secrets, credentials, API keys, tokens, webhook URLs, or environment
  variables
- raw local logs
- generated card data
- runtime status files
- failed posts
- workbook exports
- committed fixtures
- expected parser outputs
- schema snapshots
- drift baselines
- raw feedback packet storage
- formal feedback-round packet directories

Workflow surfaces in scope only for narrow implementation:

- Codex H source coverage guidance
- constitution feedback packet template wording
- machine-readable governance rule index
- concise workflow routing note if needed

## Validation Requirements

Codex C should run at minimum:

```powershell
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
```

If `docs/agent_rules.yml` is edited, Codex C should verify that the YAML
parses with an available repo-compatible command. A suitable command is:

```powershell
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
```

If a new file is created and remains untracked during local validation, Codex C
should also run a path-scoped protected-surface check for the new file:

```powershell
'docs/contracts/codex_h_post_adoption_governance_refinements.md' | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If broader repo checks are available and not disruptive, Codex C may run:

```powershell
.\tools\run_repo_checks.ps1
```

Codex E should verify:

- packet recommendations are classified against current repo state before
  synthesis
- status labels are clear enough to separate active, satisfied, stale,
  superseded, conflict, and watch-list items
- closed issue #72 and closed tracker #33 are treated as historical context,
  not active trackers
- E2 remains optional and is not promoted to permanent-role status
- Pyright remains advisory and is not made required
- raw feedback rounds remain optional
- raw packet repo storage remains formal-round-only
- `main` approval gates are unchanged
- Codex H remains advisory
- A-G remains the normal module implementation path
- parser truth ownership and protected surfaces remain unchanged
- docs changes are narrow and do not reopen the broader Codex H adoption design

## Acceptance Criteria

- `docs/contracts/codex_h_post_adoption_governance_refinements.md` exists.
- The contract identifies issue #76 as a closed source/adoption record.
- The contract identifies issues #72 and #33 as closed hardening records.
- The contract does not require reopening issue #76 and recommends a new
  follow-up issue for implementation when practical.
- The contract defines current-status/adoption-status classification for
  Codex H synthesis.
- The contract defines labels for active, partially satisfied, satisfied,
  stale, superseded, conflict, and watch-list recommendations.
- The contract preserves source coverage before synthesis.
- The contract keeps feedback rounds optional.
- The contract keeps raw packet repo storage formal-round-only.
- The contract keeps E2 optional and out of permanent-role status.
- The contract keeps Pyright advisory and non-required.
- The contract preserves `main` approval gates.
- The contract preserves Codex H as advisory and A-G as the normal module
  workflow.
- The contract does not authorize parser/runtime/workbook/webhook/App Script
  behavior changes.
- The contract includes validation expectations and a pasteable Codex C prompt.

## Unknowns And Open Questions

- Whether implementation should use issue #76 as the related issue or open a
  new follow-up issue before changing governance docs.
- Whether a new follow-up issue should explicitly cite closed issues #72 and
  #33, or only cite this contract.
- Whether the status field should be named `current_status`,
  `recommendation_status`, or `adoption_status`.
- Whether the feedback packet template should include an optional status field,
  or whether status classification should live only in Codex H source coverage
  output.
- Whether future Codex H synthesis artifacts should store source coverage
  tables in issue comments only or in formal feedback-round files when a round
  is authorized.

## Suspected Gaps

- Codex H source coverage currently inventories packets, but it does not
  explicitly classify old recommendations against current repo state.
- The feedback packet template is intentionally compact, but it may not remind
  later synthesizers that raw packet observations can become stale.
- The machine-readable rule index does not yet encode recommendation status
  classification.
- The current contract does not yet have a dedicated follow-up issue, even
  though issue #76, issue #72, and tracker #33 are all closed.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Codex C should compare current repo docs to this contract, then make only the
narrow docs/template/rule edits authorized here. Codex C should write an
implementation handoff at:

```text
docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md
```

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\<redacted>\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex C: Module Implementer / comparison thread for the post-adoption governance refinement:

Source/adoption issue:
https://github.com/Tahjali11/Mythic-Edge/issues/76

Branch target:
main

Contract:
docs/contracts/codex_h_post_adoption_governance_refinements.md

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/constitutional_lawyer.md
- docs/templates/constitution_feedback_packet.md
- docs/contracts/codex_h_post_adoption_governance_refinements.md
- docs/contracts/codex_h_constitutional_lawyer_adoption.md
- docs/contracts/code_hardening_independent_test_authoring_policy.md
- docs/contracts/code_hardening_pyright_advisory.md
- docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md
- issue #76 and PR #77 records if GitHub access is available
- issue #72 and issue #33 records if GitHub access is available

Before editing:
- Confirm branch is main.
- Inspect git status and exclude unrelated changes.
- State what the post-adoption refinement is supposed to do, what current docs already do, what gap remains, and the exact minimal implementation plan.

Implement only the narrow docs/template/rule edits authorized by the contract:
- update docs/agent_threads/constitutional_lawyer.md so Codex H classifies packet recommendations against current repo state before synthesis
- update docs/templates/constitution_feedback_packet.md only if useful to clarify that later synthesis may mark raw packet recommendations as active, partially satisfied, satisfied, stale, superseded, conflict, or watch-list
- update docs/agent_rules.yml with a terse machine-readable current-status classification rule
- update docs/codex_module_workflow.md only if a concise routing note is needed
- avoid AGENTS.md and docs/agent_constitution.md unless the refinement would otherwise be undiscoverable
- produce docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md

Preserve:
- Codex H as advisory synthesis
- A-G as the normal module workflow
- feedback rounds as optional
- raw packet repo storage as formal-round-only
- main-target approval gates
- E2 as optional Codex E mode
- Pyright as advisory, not required
- issue #72 and issue #33 as closed historical context
- parser truth ownership and protected surfaces

Do not:
- reopen the broad Codex H adoption design
- make feedback rounds mandatory
- create raw feedback packet files or formal round folders
- weaken main-target approval gates
- promote E2 to permanent-role status
- make Pyright required or failing
- treat issue #72 or issue #33 as active implementation trackers
- change parser/runtime/workbook/webhook/App Script behavior
- change CI gates, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, fixtures, snapshots, or baselines
- stage, commit, open a PR, merge, or close issues unless explicitly asked

Validation:
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
If docs/agent_rules.yml is edited, run:
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
If time allows and not disruptive, run:
.\tools\run_repo_checks.ps1

Final handoff must include:
- role performed
- source issue/adoption record used
- contract used
- files changed
- exact docs/template/rule sections changed
- validation run
- remaining risks or unverified layers
- whether any forbidden/protected surfaces were touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/76"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/codex_h_post_adoption_governance_refinements.md"
  target_artifact: "docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md"
  risk_tier: "Medium"
  branch: "main"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not reopen the broad Codex H adoption design."
    - "Do not make feedback rounds mandatory."
    - "Do not create raw feedback packet files or formal round folders."
    - "Do not weaken main-target approval gates."
    - "Do not promote E2 to permanent-role status."
    - "Do not make Pyright required."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
