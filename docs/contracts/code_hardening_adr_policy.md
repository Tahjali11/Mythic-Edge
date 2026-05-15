# Code Hardening ADR Policy Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/62

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Previous hardening context:

- Issue #45 / PR #57 added Pyright advisory hardening to
  `codex/code-hardening-suite`.
- Issue #58 / PR #59 added deterministic property/fuzz-style tests for
  `api_common.py`.
- Issue #60 / PR #61 added parser event schema snapshot tests and merged into
  `codex/code-hardening-suite` at
  `8016d82e292c43c3348e94d67189a60c86897448`.
- Tracker #33 remains open.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `.github/pull_request_template.md`

Hardening contracts read:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

This contract defines the ADR policy and lightweight governance amendments for
Mythic Edge. It is a contract artifact only. It does not implement the ADR
system, create `docs/decisions/`, create seed ADRs, open a PR, target `main`,
or mark tracker #33 complete.

## Module

ADR policy and lightweight constitutional/rules amendment.

ADR means Architecture Decision Record: a short, durable document that records
an important design or process decision, the context for that decision, the
decision itself, and its consequences.

Likely future implementation artifacts:

- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- narrow amendments to:
  - `docs/agent_constitution.md`
  - `docs/agent_rules.yml`
  - `docs/codex_module_workflow.md`
  - `.github/pull_request_template.md`
- `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`
- optional `docs/contract_test_reports/code_hardening_adr_policy.md`

Plain English: ADRs should become the stable place to answer "why did Mythic
Edge choose this rule?" for durable cross-project decisions. They should not
replace issues, module contracts, review reports, or current user
instructions.

## Owning Layer

Repository governance, workflow policy, and code-hardening documentation.

Truth boundary:

- ADR policy owns durable project-decision documentation.
- ADRs may describe parser truth ownership, protected surfaces, workflow
  policy, branch policy, dependency policy, and data-boundary policy.
- ADRs do not own parser truth, event interpretation, workbook truth, webhook
  truth, Apps Script behavior, production deployment state, or live workbook
  state.
- Parser and state remain the source of truth for MTGA event interpretation,
  normalized match facts, and normalized game facts.
- Issues and module contracts remain required for scoped implementation work.
- Accepted ADRs are durable precedent; they are not automatic permission to
  change protected runtime surfaces.

## Files Owned By This Contract

- `docs/contracts/code_hardening_adr_policy.md`

Expected future implementation files owned by this contract:

- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`

Files that may receive narrow policy references under this contract:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `.github/pull_request_template.md`

Related files referenced but not owned by this contract:

- `AGENTS.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- existing hardening contracts under `docs/contracts/`
- future seed ADRs under `docs/decisions/`
- GitHub issue #33 and issue #62

## Observed Current State

Observed on `codex/code-hardening-suite` during this contract pass:

- Current HEAD is
  `8016d82e292c43c3348e94d67189a60c86897448`.
- `docs/decisions/` does not exist.
- `docs/agent_constitution.md` already has an `Amendment Process` section.
- The constitution requires material constitution changes to link to a GitHub
  issue, state the problem solved, avoid rule duplication, update affected role
  files if needed, pass repo checks, and include a short decision note in the
  issue or PR.
- `docs/agent_rules.yml` already defines authority order, source priority,
  conflict triage, protected surfaces, roles, routing, issue lifecycle, PR
  lifecycle, branch policy, validation gates, and handoff schema.
- `.github/pull_request_template.md` already has sections for linked issue and
  contract, risk tier, layer ownership, drift budget, tests, contract
  verification, still-unverified items, and workflow handoff.
- The PR drift budget already requires issue/contract citations for authorized
  or residual drift.
- Tracker #33 lists ADR policy and constitutional amendment as the current
  hardening queue item.
- Tracker #33 lists seed architecture decision records as the next queue item,
  separate from this issue.
- Unrelated untracked files are present:
  - `docs/project_roadmap.md`
  - `docs/python_tooling_inventory.md`

Codex C/F must not absorb unrelated untracked files into this module.

## Why ADRs Are Needed

Mythic Edge already uses durable role artifacts: issues, module contracts,
implementation handoffs, review reports, PR descriptions, and tracker
comments. That workflow works, but it leaves one gap.

Important recurring decisions can be scattered across old issues, contracts,
PR comments, and Codex chats. Future threads should not have to remember which
old conversation explained why parser truth stays upstream, why protected
surface warnings require issue/contract authorization, or why Pyright started
as advisory.

ADRs are required to:

- preserve rationale for decisions that outlive one module or PR
- reduce reliance on chat history and memory
- make future Codex threads cite reviewed repo artifacts instead of stale
  assumptions
- distinguish durable architectural precedent from one-off implementation
  details
- record consequences and tradeoffs, not only final rules
- provide a safe path for superseding older decisions without silently erasing
  them
- help reviewers identify when a new issue or contract conflicts with accepted
  project policy

## Public Interface

### ADR Directory

Required directory:

```text
docs/decisions/
```

The directory should contain ADR policy/index documentation and ADR files. It
must not contain raw logs, generated runtime artifacts, workbook exports,
secrets, or private local data.

### ADR README

Required file:

```text
docs/decisions/README.md
```

The README is the ADR system entrypoint. It should define:

- what ADRs are for in Mythic Edge
- when an ADR is required
- when an ADR is not required
- ADR authority and conflict handling
- lifecycle status values
- file naming and numbering rules
- required ADR template fields
- update/supersession policy
- how issues, contracts, reviews, and PRs should cite ADRs
- the index of ADR files once seed ADRs exist

The README must not itself become a seed ADR for parser truth, AI analytics,
Player.log drift, protected surfaces, schema policy, or any other durable
decision. Those belong to the later seed-ADR tracker item.

### ADR Template

Required file:

```text
docs/decisions/ADR_TEMPLATE.md
```

The template is not a decision record and must not consume an ADR number.

Required template fields:

- Title
- Status
- Date
- Decision owners / workflow role
- Related issues
- Related PRs
- Related contracts, handoffs, or review reports
- Context
- Decision
- Scope
- Non-goals
- Alternatives considered
- Consequences
- Truth ownership impact
- Protected surfaces touched or explicitly not touched
- Validation or review evidence
- Supersedes
- Superseded by
- Follow-ups
- Notes

The template may include brief field guidance, but it should remain lightweight
enough for Codex threads and humans to complete reliably.

### ADR Files

Required naming convention:

```text
docs/decisions/ADR-0001-short-kebab-title.md
```

Rules:

- Use `ADR-` plus a four-digit, zero-padded, monotonic number.
- Use a short lowercase kebab-case slug after the number.
- Never reuse numbers, even if an ADR is later rejected or superseded.
- Do not renumber existing ADRs.
- Do not use dates as the primary identifier.
- Do not create seed ADRs under issue #62. Seed decisions belong to the next
  tracker item unless a future contract explicitly expands scope.

Examples:

```text
docs/decisions/ADR-0001-parser-owns-truth.md
docs/decisions/ADR-0002-local-scorer-decides-llm-explains.md
```

The examples are illustrative only and must not be created by this issue.

## ADR Authority

Required authority model:

- Active system, developer, and current user instructions remain highest
  authority.
- `AGENTS.md`, `docs/agent_rules.yml`, and `docs/agent_constitution.md` remain
  the repo's active governing documents.
- Accepted ADRs sit below those active governing documents.
- Accepted ADRs sit above older docs, examples, uncited assumptions, stale
  memory, and chat history.
- GitHub issues and problem representations define the immediate work request,
  scope, and risk for a thread.
- Module contracts define the scoped implementation contract for a specific
  issue or module.
- ADRs define durable precedent that issues and contracts should cite when
  they operate in an area covered by an accepted ADR.
- Implementation handoffs, contract-test reports, review reports, PR
  descriptions, and tracker comments are evidence and routing artifacts. They
  can cite ADRs, but they do not supersede accepted ADRs by themselves.
- Memory is not an authority source. Memory may help locate an ADR, but future
  threads must verify against repo files or GitHub artifacts before relying on
  it.

Conflict rules:

- If an accepted ADR conflicts with active system/developer/user instructions,
  follow the active instruction and record the conflict.
- If an accepted ADR conflicts with `AGENTS.md`, `docs/agent_rules.yml`, or
  `docs/agent_constitution.md`, follow the governing document and route to a
  policy amendment if the ADR should change.
- If a current issue or module contract appears to conflict with an accepted
  ADR, the conflict must be named explicitly. Implementation must stop or
  route back to Codex A/B unless the issue and contract explicitly authorize
  an ADR amendment or supersession path.
- If two ADRs conflict, the newer accepted ADR must identify the older ADR it
  supersedes. If no supersession is recorded, route to Codex B before
  implementation.
- ADRs cannot authorize protected-surface changes by implication. Protected
  runtime, parser, workbook, webhook, Apps Script, event, identity, dedupe,
  deployment, secret, and local-artifact changes still require an issue,
  contract, review, and validation.

## Decisions That Require ADRs

ADRs are required for durable decisions that outlive one issue, module, or PR.

Required ADR categories:

- truth ownership changes or clarifications between parser/state, webhook,
  Apps Script, workbook, dashboards, and AI layers
- protected-surface policy changes
- schema-change, snapshot-update, fixture/evidence, or drift-budget policy
  changes
- parser resilience and Player.log drift policy that affects future modules
- AI analytics or coaching boundaries, especially deterministic local scoring
  versus LLM explanation
- persistent external integration boundaries, privacy boundaries, secrets
  policy, or data-retention policy
- branch, merge, deployment, or production-safety policy
- durable development dependency, tooling, code-generation, or validation-gate
  strategy
- future escalation of advisory tools into required CI gates
- retirement, migration, or compatibility decisions for legacy workbook,
  parser, event, or runtime surfaces
- decisions that intentionally supersede, reject, or materially amend a prior
  ADR
- recurring architectural tradeoffs where future Codex threads need the
  rationale, not only the rule

Plain English test: if future reviewers will ask "why is the project allowed
or required to do this across multiple modules?", write or cite an ADR.

## Decisions That Do Not Require ADRs

ADRs are not required for ordinary scoped work that is already covered by an
issue, contract, and review path.

ADR-not-required examples:

- typo fixes
- local wording improvements that do not change rules
- ordinary focused tests that preserve an existing contract
- implementation details fully scoped to one module contract
- one-off bug fixes that do not establish cross-project precedent
- small reversible tooling conveniences that do not change validation policy
- PR-specific drift disclosures that do not set future policy
- contract-test reports, implementation handoffs, or review reports that only
  verify a scoped issue
- routine dependency patching when an existing ADR or contract already covers
  the dependency policy
- generated snapshot updates explicitly authorized by a current issue,
  contract, and review, when the update does not create new policy

If a "small" change changes who owns truth, loosens a protected surface,
changes a branch/deploy policy, or creates precedent for future work, it
requires an ADR or explicit route back to Codex B/A.

## ADR Lifecycle And Status Values

Required status values:

- `Proposed`
- `Accepted`
- `Superseded`
- `Deprecated`
- `Rejected`

Definitions:

- `Proposed`: written for review but not yet accepted. It may guide a current
  PR discussion, but it is not durable precedent.
- `Accepted`: reviewed and merged into the approved branch. Future issues,
  contracts, and PRs should treat it as durable precedent.
- `Superseded`: replaced by a newer accepted ADR. The file remains for
  history and must link to the superseding ADR.
- `Deprecated`: still historically true but no longer recommended for new
  work. Use only when the old decision remains relevant during a migration.
- `Rejected`: intentionally not adopted. Keep the record when the rejected
  option is likely to recur or the rationale matters.

Lifecycle rules:

- New ADRs start as `Proposed`.
- An ADR becomes `Accepted` only through reviewed repo changes on the approved
  branch or through a later explicit user-approved workflow.
- Material changes to an `Accepted` ADR require a new ADR or explicit
  supersession path. Do not rewrite accepted rationale silently.
- Tiny typo, formatting, broken-link, or metadata fixes may be made in place
  when they do not alter the decision.
- Superseding ADRs must name the older ADR in `Supersedes`.
- Superseded ADRs must name the newer ADR in `Superseded by`.
- Rejected ADRs should not be deleted merely because they were rejected.

## Required ADR Content Rules

Every ADR must:

- have exactly one title
- have one status from the required status list
- include an ISO-like date, such as `2026-05-15`
- link related GitHub issue(s)
- link related PR(s) once available
- cite related contracts, handoffs, or review reports when applicable
- state the context in plain English
- state the decision directly
- state scope and non-goals
- list meaningful alternatives considered
- describe consequences and tradeoffs
- state truth ownership impact
- state protected surfaces touched or explicitly untouched
- state validation/review evidence or say why validation is not applicable
- state supersession metadata, even if `None`
- list follow-up issues or say `None`

ADR content must not:

- include raw MTGA logs
- include secrets, webhook URLs, tokens, credentials, or API keys
- include local absolute paths as normative requirements
- include generated card data, runtime status snapshots, failed posts, or
  workbook exports
- include live workbook IDs or production deployment details unless a future
  issue explicitly approves safe redacted documentation
- duplicate large sections from the constitution, rule index, or contracts
- replace issue-specific problem representations or module contracts

## Allowed Narrow Amendments

Codex C may make only narrow policy-reference edits needed to wire the ADR
system into existing governance docs.

### `docs/agent_constitution.md`

Allowed:

- Add a short ADR subsection near `Artifact-First Handoffs`, `GitHub
  Workflow`, or `Amendment Process`.
- State that accepted ADRs are durable decision records below the constitution
  and rule index.
- State that ADRs complement issues and module contracts.
- State that conflicts with accepted ADRs must be routed explicitly instead of
  silently ignored.

Forbidden:

- Broadly rewrite the constitution.
- Remove existing non-negotiables, truth model, workflow gates, validation
  rules, or amendment process.
- Use ADRs to weaken issue/contract/review requirements.

### `docs/agent_rules.yml`

Allowed:

- Add `docs/decisions/README.md` and `docs/decisions/ADR-*.md` to
  `document_architecture`.
- Add accepted ADRs to `authority_order` below `AGENTS.md`,
  `docs/agent_rules.yml`, and `docs/agent_constitution.md`, and above older
  docs/examples/memory.
- Add concise conflict-triage or routing rules for ADR conflicts.
- Add ADR-related validation expectations under docs/workflow checks if
  useful.

Forbidden:

- Reorder unrelated authority tiers beyond what is necessary to place ADRs.
- Remove protected surfaces, sacred rules, branch policy, issue lifecycle,
  PR lifecycle, validation gates, or role definitions.
- Encode seed ADR decisions in the rule index.

### `docs/codex_module_workflow.md`

Allowed:

- Add a concise ADR reference explaining when A/B/C/E/F/G should cite or route
  to ADRs.
- State that durable cross-project decisions need ADRs and issue-scoped work
  still needs contracts.
- Add ADR references to handoff expectations where useful.

Forbidden:

- Replace the A -> B -> C -> E -> F workflow.
- Introduce new permanent roles.
- Broaden G into a general implementer.
- Change merge-to-main policy.

### `.github/pull_request_template.md`

Allowed:

- Add one short ADR reference field under `Linked Issue And Contract` or near
  `Drift Budget`, for example:
  - `Related ADRs:`
- Add wording that PRs relying on durable decisions should cite relevant ADRs.

Forbidden:

- Remove existing issue/contract, drift-budget, risk-tier, layer ownership,
  tests, contract verification, still-unverified, or workflow handoff
  sections.
- Treat ADR citation as a substitute for issue/contract authorization.
- Make every small PR require an ADR.

## Out Of Scope

This issue does not authorize:

- creating seed ADRs
- deciding parser truth policy in a seed ADR
- deciding local deterministic scorer versus LLM explanation policy
- deciding Player.log drift policy
- deciding protected-surface/schema-change seed policy
- changing parser behavior
- changing parser state final reconciliation
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing parser event classes
- changing event `kind` values
- changing parser payload shapes
- changing match identity
- changing game identity
- changing deduplication
- changing secrets, credentials, tokens, API keys, or webhook URLs
- changing environment variable contracts
- committing raw logs
- changing generated card/tier data
- changing runtime status files
- changing failed posts
- changing workbook exports
- changing production deployment behavior
- changing merge-to-main policy
- opening a PR from the contract writer pass
- marking tracker #33 complete

## Protected Surfaces

Protected surfaces preserved by this contract:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- secrets and environment variables
- raw logs and local/private artifacts
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

Workflow surfaces intentionally in scope:

- ADR policy documentation
- ADR directory README/template
- narrow references from constitution, rule index, workflow doc, and PR
  template
- implementation handoff and review artifacts

## Validation Requirements

Contract-writer validation:

```powershell
git diff --check
```

Minimum Codex C implementation validation:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "Architecture Decision Records|ADR|docs/decisions|Related ADRs" docs\agent_constitution.md docs\agent_rules.yml docs\codex_module_workflow.md .github\pull_request_template.md docs\decisions\README.md docs\decisions\ADR_TEMPLATE.md
```

If Codex C edits only Markdown/YAML/template docs, full parser tests are not
required. The implementation handoff must explicitly record that runtime
parser tests were skipped because no runtime code changed.

If Codex C edits Python, tests, CI, executable tools, parser files, workflow
scripts, or any protected runtime surface, it must stop and route back unless
a new or amended contract authorizes that scope.

Before Codex F submitter work:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Recommended manual review checks:

- `docs/decisions/README.md` exists and defines ADR purpose, authority,
  lifecycle, naming, template fields, update policy, and index scope.
- `docs/decisions/ADR_TEMPLATE.md` exists and is not numbered as a decision.
- No seed ADR files exist under issue #62.
- Narrow amendments mention ADRs without duplicating the README/template.
- PR template still requires issue and contract citations for drift.
- `docs/agent_rules.yml` remains valid YAML in structure and indentation.

## Stop Conditions

Stop and route back to Codex B, Codex A, or the user if:

- implementation would create seed ADRs under this issue
- implementation would change parser/runtime/workbook/webhook/App Script
  behavior
- implementation would loosen protected-surface, drift-budget, issue/contract,
  review, or validation requirements
- implementation would make ADRs override active governing docs or current
  explicit user instructions
- implementation would treat ADRs as automatic authorization for protected
  behavior changes
- implementation would require broad rewrites of constitution, workflow, PR
  template, or rule index
- implementation would target `main`
- implementation would mark tracker #33 complete

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/code-hardening-suite`.
2. Confirm the branch is at or after PR #61 merge commit `8016d82`.
3. Inspect `git status` and exclude unrelated untracked files from this module.
4. Read issue #62, this contract, and the governance docs.
5. Compare current docs against this contract before editing.
6. Create `docs/decisions/README.md`.
7. Create `docs/decisions/ADR_TEMPLATE.md`.
8. Add only narrow ADR references to `docs/agent_constitution.md`,
   `docs/agent_rules.yml`, `docs/codex_module_workflow.md`, and
   `.github/pull_request_template.md` as needed.
9. Do not create any numbered ADRs.
10. Run docs/protected-surface validation.
11. Produce
    `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`.
12. Route to Codex E for contract-test review.

## Compatibility

Must remain stable:

- existing Mythic Edge truth model
- existing protected-surface requirements
- existing seven-role workflow path
- existing hardening branch target: `codex/code-hardening-suite`
- existing PR drift-budget fields and labels
- existing requirement that protected-surface changes cite issue/contract
  authority
- existing non-production merge policy
- existing parser/runtime/workbook/webhook/App Script behavior

Breaking changes requiring a new or amended contract:

- changing ADR authority above active governing docs
- requiring ADRs for every PR
- removing issue-specific problem representation or module contract
  requirements
- creating seed ADRs in this issue
- changing protected-surface enforcement semantics
- changing parser behavior or downstream schema/payload behavior
- changing merge-to-main or production deployment policy

## Unknowns And Open Questions

- Whether the first implementation should add ADRs to both `authority_order`
  and `source_priority` in `docs/agent_rules.yml`, or only
  `authority_order`.
- Whether future seed ADRs should be introduced one PR at a time or batched
  under the next tracker item.
- Whether `docs/decisions/README.md` should keep the ADR index manually sorted
  or whether a future tooling issue should generate the index.
- Whether ADR review should always require Codex E contract-test review, or
  whether low-risk documentation ADRs can use normal PR review after the first
  rollout proves stable.
- Whether rejected ADRs should remain in the main `docs/decisions/` directory
  or move to a clearly named archive section. The first implementation should
  keep them in place and use status metadata unless a later contract changes
  this.

## Suspected Implementation Gaps

- There is no `docs/decisions/` directory yet.
- There is no ADR README or template.
- Current governance docs mention decision notes in issues/PRs, but they do
  not define durable ADR authority, status values, numbering, or supersession.
- Current PR template has no dedicated ADR citation field.
- Future threads may still rely on issue comments, PR descriptions, or memory
  for durable decisions until ADR references are added.
- The seed ADR queue item is intentionally separate and must not be pulled into
  this issue.

## Acceptance Criteria

- `docs/contracts/code_hardening_adr_policy.md` exists.
- The contract explains why ADRs are needed in Mythic Edge.
- The contract defines which decisions require ADRs.
- The contract defines which decisions do not require ADRs.
- The contract defines ADR authority relative to `AGENTS.md`,
  `docs/agent_rules.yml`, `docs/agent_constitution.md`, GitHub issues, module
  contracts, handoffs, review reports, PRs, and memory.
- The contract defines ADR lifecycle/status values.
- The contract defines ADR file naming and numbering.
- The contract defines required ADR template fields.
- The contract defines `docs/decisions/README.md` scope.
- The contract defines allowed narrow edits to constitution, rules, workflow,
  and PR template files.
- The contract preserves protected surfaces and out-of-scope runtime behavior.
- The contract defines validation requirements and stop conditions.
- The contract routes next work to Codex C: Module Implementer / comparison
  thread.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/62

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract produced:
`docs/contracts/code_hardening_adr_policy.md`

Risk tier: Medium for repository governance. Escalate to High if
implementation loosens protected-surface policy, changes merge/deploy policy,
changes parser/runtime behavior, or moves truth ownership.

Owning truth layer: repository governance, workflow policy, and code-hardening
documentation.

Public interface:

- Future ADR directory: `docs/decisions/`
- Future ADR README: `docs/decisions/README.md`
- Future ADR template: `docs/decisions/ADR_TEMPLATE.md`
- Future ADR file naming: `docs/decisions/ADR-0001-short-kebab-title.md`
- Narrow references from constitution, rule index, workflow doc, and PR
  template.

Invariants:

- ADRs are durable precedent, not automatic implementation authorization.
- ADRs sit below active governing docs and above stale memory/examples.
- Issues and module contracts remain required for scoped work.
- Protected-surface changes still require explicit issue/contract/review
  authority.
- Seed ADRs remain out of scope for issue #62.
- Hardening work targets `codex/code-hardening-suite`, not `main`.

Required validation: listed above.

Acceptance criteria: listed above.

Open questions or contract risks: listed above.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: ADR policy and constitutional amendment.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/62

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/code_hardening_adr_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_pyright_advisory.md
- docs/contracts/code_hardening_api_common_property_fuzz_tests.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/templates/workflow_handoff.md
- .github/pull_request_template.md
- issue #33
- issue #62

Goal:
Compare the current governance docs against docs/contracts/code_hardening_adr_policy.md. Implement only the smallest documentation changes needed to add the ADR policy system and lightweight governance references, then produce docs/implementation_handoffs/code_hardening_adr_policy_comparison.md.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Confirm the branch is at or after PR #61 merge commit 8016d82.
- Inspect git status and exclude unrelated untracked files.
- State what ADRs are supposed to do, what the repo currently lacks, why that gap matters, and the exact minimal docs-only implementation plan.

Do:
- Create docs/decisions/README.md.
- Create docs/decisions/ADR_TEMPLATE.md.
- Add only narrow ADR references to docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md, and .github/pull_request_template.md as allowed by the contract.
- Keep ADR authority below active governing docs and above stale memory/examples.
- Preserve issue-specific problem representations, module contracts, review reports, PR drift budgets, protected-surface checks, and branch policy.
- Produce docs/implementation_handoffs/code_hardening_adr_policy_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Create seed ADRs or numbered ADR files.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy.
- Treat ADRs as automatic authorization for protected-surface changes.
- Broadly rewrite the constitution, workflow, PR template, or rule index.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "Architecture Decision Records|ADR|docs/decisions|Related ADRs" docs\agent_constitution.md docs\agent_rules.yml docs\codex_module_workflow.md .github\pull_request_template.md docs\decisions\README.md docs\decisions\ADR_TEMPLATE.md
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/62"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_adr_policy.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_adr_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not create seed ADRs or numbered ADR files under issue #62."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not treat ADRs as automatic authorization for protected-surface changes."
    - "Do not broadly rewrite the constitution, workflow, PR template, or rule index."
    - "Do not absorb unrelated untracked files into this module."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
