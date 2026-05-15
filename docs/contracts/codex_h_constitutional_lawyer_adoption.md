# Codex H Constitutional Lawyer Adoption Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/76

Tracker: N/A

Branch target: `main`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`

Related local skills inspected as evidence, not repo authority:

- `$mythic-edge-workflow`
- `$mythic-edge-constitution-review`
- `$mythic-edge-constitutional-lawyer`

Related ADRs:

- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

This is a contract-writing artifact only. It does not implement Codex H
adoption, create feedback packet templates, create Codex H role docs, rewrite
authority docs, create raw feedback packet storage, change parser behavior,
change workbook or webhook surfaces, change Apps Script behavior, change CI
gates, open a PR, or merge anything.

## Module

Codex H / Constitutional Lawyer repo adoption.

Plain English: Codex H is a governance synthesis role. It reads constitution
feedback packets, inventories the source evidence, and proposes amendments,
consolidations, unresolved conflicts, or watch-list items for later workflow
threads. Codex H does not directly rewrite authority documents.

## Source Issue

https://github.com/Tahjali11/Mythic-Edge/issues/76

Issue #76 defines the problem representation for adopting Codex H into the
repo workflow. The issue was revised to include:

- raw feedback packets should not be committed to the repo by default
- formal feedback-round storage may exist only when authorized by issue and
  contract
- Codex H should produce a source coverage table before proposing amendments
  when multiple feedback packets are supplied
- Codex H should not be confused with authority to rewrite governing docs
  directly

## Owning Layer

Owning layer: repository coordination and agent workflow governance.

Truth boundary:

- Codex H synthesis, feedback packets, issue comments, local skills, chat
  history, and memory are evidence and workflow inputs.
- They are not parser truth, workbook truth, webhook truth, Apps Script truth,
  production deployment truth, or accepted repo authority by themselves.
- Parser and state interpretation remain the truth owners for MTGA event
  interpretation and normalized match/game facts.
- Accepted repo authority remains governed by `AGENTS.md`,
  `docs/agent_rules.yml`, `docs/agent_constitution.md`, current issues,
  current contracts, accepted ADRs, reviewed PRs, and merged docs.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/codex_h_constitutional_lawyer_adoption.md`

Expected future implementation files if Codex C is authorized:

- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`
- narrow references in `AGENTS.md`
- narrow references in `docs/agent_constitution.md`
- narrow references in `docs/agent_rules.yml`
- narrow references in `docs/codex_module_workflow.md`

Optional future implementation file if Codex C needs a durable storage policy
home:

- `docs/constitution_feedback/README.md`

Codex C must not create raw feedback packet files, round folders, or stored
packet archives unless a formal feedback-round issue and contract explicitly
authorize that storage.

## Observed Current Governance State

Observed on `main` during this contract pass:

- `git status --short --branch` reported `## main...origin/main`.
- `docs/templates/constitution_feedback_packet.md` does not exist.
- `docs/agent_threads/constitutional_lawyer.md` does not exist.
- `AGENTS.md`, `docs/agent_constitution.md`, `docs/agent_rules.yml`, and
  `docs/codex_module_workflow.md` define the current A-G workflow authority.
- `docs/agent_threads/` contains A-G role docs, but no committed Codex H role
  doc.
- `docs/templates/workflow_handoff.md` and `docs/templates/module_contract.md`
  exist, but no committed constitution feedback packet template exists.
- The local constitution-review skill has a fallback packet format and says
  feedback packets should not be committed by default.
- The local constitutional-lawyer skill describes Codex H as a synthesis role
  and requires a source coverage table before amendment synthesis.
- Local skills are useful operational evidence, but the repo remains the
  authority.
- Existing ADRs do not directly adopt Codex H as a repo workflow role or define
  formal constitution feedback-round storage.
- Existing code-hardening policy artifacts mention E2 as an optional Codex E
  mode, not as a permanent role.

## Public Interface

This contract creates no runtime public interface.

The future governance interface should define these repo-visible concepts:

- Codex H / Constitutional Lawyer
- constitution feedback packet
- constitution feedback round
- raw feedback packet
- formal feedback-round repo storage
- source coverage table
- amendment synthesis
- watch-list or minority-report item
- unresolved conflict
- later adoption workflow

### Codex H / Constitutional Lawyer

Codex H is an auxiliary governance role, not part of the normal A-G module
implementation path.

Codex H should be documented in `docs/agent_threads/constitutional_lawyer.md`.

Codex H may be referenced from `AGENTS.md`, `docs/agent_constitution.md`,
`docs/agent_rules.yml`, and `docs/codex_module_workflow.md`, but the normal
module path remains:

```text
A -> B -> C -> E -> F -> G
```

If `docs/agent_rules.yml` encodes Codex H, it should distinguish H as an
auxiliary governance synthesis role rather than inserting H into the normal
module implementation route.

### Constitution Feedback Packet

A constitution feedback packet is a structured, redacted packet from a prior
thread or user-provided comment that describes a constitutional improvement,
workflow friction, unresolved conflict, or watch-list concern.

The required template should live at:

```text
docs/templates/constitution_feedback_packet.md
```

The template must support the compact packet shape used in issue #76:

- `source_role`
- `source_thread_or_context`
- `related_issue_or_pr`
- `date_collected`
- `status`
- original constitutional comment or pasteable text
- proposed constitutional improvement
- why it matters
- suggested authority level
- affected roles
- affected protected surfaces
- conflict or tension
- confidence
- evidence quote
- routing recommendation
- storage recommendation

The template may include optional user notes when useful, but user notes must
not be required for every packet.

### Raw Feedback Packet

A raw feedback packet is evidence. It is not authority by itself.

Raw packets should default to:

- pasteable chat output
- GitHub issue comments during an active constitution feedback round

Raw packets must not be committed to the repo by default.

### Formal Feedback-Round Repo Storage

Formal repo storage for raw feedback packets may exist only when an issue and
contract explicitly authorize a feedback round.

If authorized, the preferred path is:

```text
docs/constitution_feedback/rounds/YYYY-MM-DD/packets/
```

Recommended lifecycle for an authorized round:

1. Open or identify a constitution feedback-round issue.
2. Authorize repo storage through a scoped issue and contract.
3. Store only redacted raw packet files under the round path.
4. Include a round-level README or issue link naming the round purpose, source
   issue, storage rules, and stop conditions.
5. Run Codex H synthesis with a source coverage table.
6. Route proposed amendments to normal A-G workflow or an explicit H-to-A/B
   handoff.
7. Leave raw packets as historical evidence, not accepted authority.

The initial Codex H adoption implementation should not create round packet
files. It may add `docs/constitution_feedback/README.md` only if needed to
document the storage model without opening a round.

### Source Coverage Table

When Codex H receives multiple feedback packets, it must produce a source
coverage table before proposing amendments.

For seven or more packets, this is mandatory and must not be skipped.

Recommended columns:

- source role
- source thread/context
- main recommendation
- affected authority level
- evidence quote
- confidence
- conflicts or tensions
- routing recommendation

For a single packet, Codex H may produce a concise one-row coverage table or a
short source coverage note, but it still must identify the source and routing
recommendation before synthesis.

### Amendment Synthesis

After source coverage, Codex H may synthesize:

- proposed amendments
- proposed removals or consolidations
- unresolved conflicts
- watch-list items
- items that should not be adopted yet
- recommended next workflow role

Codex H output remains advisory until adopted through reviewed repo changes.

## Inputs

Codex H adoption work may read:

- issue #76
- current governance docs
- current role docs
- current templates
- accepted ADRs
- local skill instructions as evidence
- user-provided feedback packets
- GitHub issue comments containing redacted packets
- formal feedback-round packet files, only when such a round is authorized

Input redaction requirements:

- no secrets
- no webhook URLs
- no API keys or tokens
- no raw MTGA logs
- no workbook IDs
- no generated local artifacts
- no runtime status files
- no failed posts
- no workbook exports
- no unrelated private transcript dumps

## Outputs

Codex B output from this pass:

- `docs/contracts/codex_h_constitutional_lawyer_adoption.md`

Expected Codex C output after this contract:

- `docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md`
- narrow docs/template/rule edits authorized by this contract

Expected Codex E output after implementation:

- `docs/contract_test_reports/codex_h_constitutional_lawyer_adoption.md` or
  a PR review verifying the implementation against this contract

No output from this workflow may change parser/runtime behavior, workbook
schema, webhook shape, Apps Script behavior, production deployment behavior, or
protected runtime/data surfaces.

## Required Guarantees

### Codex H Role Boundary

Codex H must:

- inventory supplied feedback packets and sources
- produce a source coverage table before synthesis when multiple packets are
  supplied
- preserve minority reports and low-confidence items as watch-list items
- propose amendments, consolidations, unresolved conflicts, and next workflow
  routing
- cite short redacted evidence quotes when useful
- treat current repo governance and accepted ADRs as higher authority than
  local skills, memory, chat history, and raw packets
- route actual docs edits to the normal issue, contract, implementation,
  review, submitter, and deployer path

Codex H must not:

- rewrite `AGENTS.md` directly
- rewrite `docs/agent_constitution.md` directly
- rewrite `docs/agent_rules.yml` directly
- rewrite role docs or templates directly while acting as H
- treat its synthesis as accepted authority
- bypass Codex B/C/E/F/G for implementation and PR work
- include protected secrets or raw/local artifacts
- change parser/runtime/workbook/webhook/App Script behavior
- change merge-to-main policy
- promote E2 to permanent-role status

### Authority Updates

Future implementation should add Codex H as an auxiliary governance role, not a
replacement for the A-G module workflow.

Allowed narrow updates:

- `AGENTS.md`: add a concise pointer that Codex H exists for constitution
  feedback synthesis and does not merge or rewrite authority docs directly.
- `docs/agent_constitution.md`: add a short auxiliary governance role section
  or role note for Codex H.
- `docs/agent_rules.yml`: add a terse machine-readable Codex H rule or
  auxiliary role entry, preserving the existing A-G normal path.
- `docs/codex_module_workflow.md`: add H routing guidance for constitution
  feedback synthesis and return-to-A/B/C flow.
- `docs/agent_threads/constitutional_lawyer.md`: define the Codex H mission,
  required reads, required outputs, coverage-table guard, stop conditions, and
  next-role routing.
- `docs/templates/constitution_feedback_packet.md`: define the compact packet
  format.

Forbidden broad updates:

- broad constitution rewrite
- wholesale role-model redesign
- protected-surface policy weakening
- branch or merge policy changes
- new CI gates
- parser/runtime/product behavior changes
- mandatory repo storage for every raw packet

### Feedback Packet Template

The template must be compact enough for issue comments and chat output.

It must distinguish:

- raw comment text
- proposed improvement
- authority level
- affected roles
- affected protected surfaces
- conflict or tension
- confidence
- evidence quote
- routing recommendation
- storage recommendation

It must include redaction warnings for secrets, raw logs, workbook IDs,
webhook URLs, generated artifacts, runtime status files, failed posts, and
unrelated private transcript content.

### Feedback-Round Storage

Repo storage for raw packets is opt-in and formal-round only.

The default storage recommendation for ordinary feedback packets is:

```text
issue comment by default; repo file only during formal feedback round
```

Formal-round storage must not be made mandatory for every thread.

If formal-round storage is documented, the policy must state that raw packets
are evidence, not accepted authority, and that accepted changes still require
normal reviewed repo changes.

### E2 Boundary

This contract does not adopt E2 as a permanent role.

Future Codex H adoption docs may mention E2 only as a role-boundary caution:
E2 is an optional Codex E mode unless a separate governance issue and contract
authorize a different status.

### ADR Boundary

No new ADR is required for the initial Codex H adoption if implementation stays
within the narrow role-doc, template, and workflow-reference scope defined by
this contract.

Route back to Codex A/B for ADR consideration if future implementation:

- changes branch, merge, or deploy policy
- changes protected-surface policy
- changes validation gate policy
- changes authority order
- makes raw feedback packet repo storage mandatory
- promotes E2 to permanent-role status
- creates durable cross-project retention or privacy policy beyond this
  feedback workflow

## Invariants

- `main` is the approved branch for this governance adoption issue because
  issue #76 and the handoff explicitly name `main`.
- Codex H remains advisory until amendments are implemented and reviewed by the
  normal workflow.
- Local skills are not repo authority.
- Raw packets and Codex H synthesis are evidence, not accepted policy.
- Formal feedback-round repo storage is optional and must be explicitly
  authorized.
- The normal module path remains A-G.
- E2 remains optional Codex E mode, not a permanent role.
- Parser truth ownership and all protected runtime/data surfaces remain
  unchanged.
- Repo docs should prefer concise references over duplicating long protected
  surface lists in every file.

## Error Behavior

If `docs/templates/constitution_feedback_packet.md` is still missing after
implementation, Codex E should treat that as a contract mismatch.

If `docs/agent_threads/constitutional_lawyer.md` is still missing after
implementation, Codex E should treat that as a contract mismatch unless Codex C
records a contract ambiguity and routes back to Codex B.

If implementation makes raw packet repo storage mandatory for every thread,
Codex E should treat that as a blocking contract mismatch.

If implementation inserts H into the normal A-G module implementation path,
Codex E should treat that as a blocking contract mismatch.

If implementation promotes E2 to permanent-role status, Codex E should treat
that as out of scope.

If a future issue asks Codex H to edit authority docs directly, the thread must
route to Codex A or B for a scoped adoption problem/contract and then to Codex
C for implementation.

If a packet includes secrets, raw logs, workbook IDs, webhook URLs, or local
runtime artifacts, Codex H must refuse to reproduce the sensitive content and
ask for a redacted packet or summarize only safe metadata.

## Side Effects

This contract pass has only one intended side effect:

- create `docs/contracts/codex_h_constitutional_lawyer_adoption.md`

Future implementation may edit only the governance docs and templates
authorized above.

Future implementation must not:

- create raw feedback packet files
- create committed raw feedback round data
- open or close issues
- open or merge PRs
- change runtime code
- change tests unrelated to docs validation
- change parser/runtime/workbook/webhook/App Script behavior
- touch local artifacts, generated data, secrets, or workbook exports

## Dependency Order

Future implementation should proceed in this order:

1. Create `docs/templates/constitution_feedback_packet.md`.
2. Create `docs/agent_threads/constitutional_lawyer.md`.
3. Add concise cross-references in `docs/codex_module_workflow.md`.
4. Add terse machine-readable rule/index support in `docs/agent_rules.yml`.
5. Add short entrypoint and constitution references in `AGENTS.md` and
   `docs/agent_constitution.md`.
6. Add `docs/constitution_feedback/README.md` only if needed to document the
   formal-round storage policy without creating raw packet files.
7. Write an implementation comparison handoff.
8. Route to Codex E for contract verification.

## Compatibility

Compatibility requirements:

- Existing A-G workflow prompts remain valid.
- Existing module contracts, implementation handoffs, review reports, and PR
  templates remain valid.
- Existing local constitution-review and constitutional-lawyer skills remain
  usable, but repo docs outrank them.
- Existing hardening policy that treats E2 as an optional Codex E mode remains
  unchanged.
- Existing ADR authority remains unchanged.

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
- CI failure gates

Workflow surfaces in scope only for narrow implementation:

- issue/contract-defined Codex H role boundary
- constitution feedback packet template
- formal feedback-round storage documentation
- concise references in current governance docs

## Validation Requirements

Codex C should run at minimum:

```powershell
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
```

If `docs/agent_rules.yml` is edited, Codex C should also verify that the YAML
parses with an available repo-compatible command. A suitable command may be:

```powershell
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
```

If broader repo checks are available and not disruptive, Codex C may run:

```powershell
.\tools\run_repo_checks.ps1
```

Codex E should verify:

- the Codex H role doc exists and keeps H advisory
- the constitution feedback packet template exists and includes storage,
  confidence, authority, affected roles, protected surfaces, conflict, evidence
  quote, and routing fields
- raw packet repo storage is optional/formal-round only
- the coverage-table guard exists
- local skills are not treated as authority over repo docs
- H is not inserted into the normal A-G implementation path
- E2 is not promoted to permanent-role status
- parser truth ownership and protected surfaces remain unchanged
- docs changes are narrow and not a broad constitution rewrite

## Acceptance Criteria

- `docs/contracts/codex_h_constitutional_lawyer_adoption.md` exists and links
  to issue #76.
- The contract defines Codex H allowed behavior and forbidden behavior.
- The contract decides that Codex H should get a committed role doc.
- The contract decides that `docs/templates/constitution_feedback_packet.md`
  should be added.
- The contract defines issue-comment/pasteable output as the default for raw
  packets.
- The contract defines formal feedback-round repo storage as opt-in and
  authorized-only.
- The contract defines the preferred formal storage path:
  `docs/constitution_feedback/rounds/YYYY-MM-DD/packets/`.
- The contract defines the source coverage table guard before synthesis.
- The contract preserves A-G as the normal module workflow.
- The contract keeps E2 optional and out of permanent-role status.
- The contract states that no ADR is required for narrow first adoption.
- The contract names validation expectations for Codex C and E.
- The contract includes a pasteable Codex C prompt and workflow handoff.

## Unknowns And Open Questions

- Whether future formal feedback rounds should keep packet files forever,
  archive them after synthesis, or rely primarily on GitHub issue comments.
- Whether future Codex H synthesis artifacts should live under
  `docs/constitution_feedback/rounds/`, `docs/contracts/`, or issue comments.
- Whether a future ADR should be written if Codex H becomes central to
  recurring governance work beyond the first adoption.
- Whether `docs/agent_rules.yml` should encode H under `auxiliary_roles`,
  `governance_roles`, or another compact structure.
- Whether formal feedback-round storage needs a README in the first
  implementation or whether the template plus role doc is enough.

## Suspected Gaps

- The repo has local skills for constitution review and Codex H behavior, but
  no committed role doc for Codex H.
- The repo has a local skill fallback packet format, but no committed feedback
  packet template.
- Current A-G docs do not explain how a Codex H synthesis routes back into the
  normal workflow.
- Current governance docs do not define formal feedback-round storage.
- Current docs do not require a source coverage table before Codex H synthesis.
- Current docs do not explicitly warn that raw packets are not authority.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Codex C should compare current repo docs to this contract, then make only the
narrow docs/template/rule edits authorized here. Codex C should write an
implementation handoff at:

```text
docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md
```

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\Tahj Blow\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex C: Module Implementer / comparison thread for the governance adoption issue:

https://github.com/Tahjali11/Mythic-Edge/issues/76

Branch target: main

Source contract:
- docs/contracts/codex_h_constitutional_lawyer_adoption.md

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/
- docs/templates/
- docs/decisions/README.md
- accepted ADRs in docs/decisions/
- docs/contracts/codex_h_constitutional_lawyer_adoption.md
- issue #76

Before editing:
- Confirm branch is main.
- Inspect git status and exclude unrelated changes.
- State what Codex H adoption is supposed to do, what the repo currently does, what gaps remain, and the exact minimal implementation plan.

Implement only the narrow docs/template/rule adoption authorized by the contract:
- create docs/templates/constitution_feedback_packet.md
- create docs/agent_threads/constitutional_lawyer.md
- add concise Codex H references to AGENTS.md, docs/agent_constitution.md, docs/agent_rules.yml, and docs/codex_module_workflow.md as needed
- optionally add docs/constitution_feedback/README.md only if needed to document formal feedback-round storage without creating raw packet files
- produce docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md

Preserve:
- A-G as the normal module workflow
- Codex H as advisory synthesis, not direct authority-doc implementation
- raw feedback packets as issue-comment/pasteable output by default
- formal repo storage as opt-in and authorized-only
- the source coverage table guard before synthesis
- E2 as optional Codex E mode, not a permanent role
- parser truth ownership and all protected surfaces

Do not:
- rewrite authority docs broadly
- create raw feedback packet files or feedback round packet folders
- make raw packet repo storage mandatory
- promote E2 to permanent-role status
- change parser/runtime/workbook/webhook/App Script behavior
- change protected surfaces, CI gates, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, fixtures, snapshots, or baselines
- stage, commit, open a PR, merge, or close issue #76 unless explicitly asked

Validation:
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
If docs/agent_rules.yml is edited, run a YAML parse check with an available repo-compatible command.
If time allows and not disruptive, run .\tools\run_repo_checks.ps1.

Final handoff must include:
- role performed
- issue used
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
  source_artifact: "docs/contracts/codex_h_constitutional_lawyer_adoption.md"
  target_artifact: "docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md"
  risk_tier: "Medium"
  branch: "main"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not rewrite authority docs broadly."
    - "Do not create raw feedback packet files or make raw packet repo storage mandatory."
    - "Do not promote E2 to permanent-role status."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
