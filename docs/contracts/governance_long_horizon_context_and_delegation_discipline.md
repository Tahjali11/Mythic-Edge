# Long-Horizon Context And Delegation Discipline Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/801>.
- Parent tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>.
- Activation record:
  <https://github.com/Tahjali11/Mythic-Edge/issues/801#issuecomment-5162434870>.
- Role: Codex B, Module Contract Writer.
- Risk tier: high governance risk; no runtime behavior change.
- Base: `origin/main@be840bc1160678a9678d792d3cfd6074ac86ebca`.
- Branch: `codex/long-horizon-context-delegation-contract-801`.

The activation is an ADR-0008 `explicit_user_override` while #776 and draft
PR #800 remain active. Its file ownership is exactly this contract, proposed
ADR-0012, and the ADR-0012 row in the decisions index. PR #800 touches none of
those paths. The exception transfers no authority to later roles.

## Problem And Ownership

Mythic Edge already defines WIP-1, artifact-first workflow, fresh-context
review, finding lifecycle, and bounded subagent concepts. The rules are spread
across accepted governance, proposed ADRs, and the merged #682 source contract.
Long-running work can therefore preserve each individual rule while missing
their combined application after context or lifecycle changes.

This contract owns only a compact governance definition for refreshing current
authority, carrying bounded context, using delegation, admitting exceptional
parallel writes, and reactivating historical findings. It changes no product
truth owner, workflow role, runtime, validator, schema, or execution surface.

## Exact Source Lifecycle

- ADR-0008 is `Accepted`, controlling, and unsuperseded.
- ADR-0010 and ADR-0011 are `Proposed` and non-precedential.
- The #682 subagent-boundaries contract was merged by PR #685; issue #682 is
  closed. It is source material and does not independently authorize #801
  implementation or expansion.
- ADR-0012 is unused on the bound base and must begin as `Proposed`.
- Current repository and GitHub artifacts outrank historical prompts, local
  worktrees, local skills, chat history, and model memory.

## Definitions

- **Material authority refresh:** bounded revalidation of the facts that can
  change whether the active role may continue or perform a consequential
  effect.
- **Bounded current-context packet:** the smallest current, source-linked set
  of authority, scope, state, findings, unknowns, and stop conditions needed by
  the active role. It is a section of an existing issue, contract, handoff, or
  review artifact, not a new schema or database.
- **Subagent:** an optional helper used by the active role to gather or compare
  evidence. It is not an A-G/H role and owns no final judgment or authority.
- **Parallel write:** two or more concurrently active editors that may change
  repository or external durable state for one coordinated outcome.
- **Finding reactivation:** assigning current lifecycle and routing relevance
  to a finding previously fixed, superseded, deferred, rejected, not
  reproduced, or closed.
- **Consequential effect:** a protected mutation or persistent, shared,
  external, submission, merge, deployment, or production effect whose
  authority or target could be changed by stale context.

## Contract Clauses

### 1. Material Authority Refresh

Refresh is required after any of these material triggers:

1. resuming after interruption, context compaction, or a materially separated
   work period;
2. accepting a role handoff or changing the active A-G/H role;
3. merge, rebase, branch/base/head change, or worktree replacement;
4. contract revision, review revision, or new accepted ADR affecting scope;
5. issue, PR, tracker, lane, approval, or finding-lifecycle state change; or
6. immediately before a consequential effect.

Refresh must revalidate, in proportion to the operation: repository identity
and remote; branch, base, head, and worktree state; active lane and ADR-0008
exception; current issue/PR/tracker state; governing contract and accepted
ADRs; current finding dispositions; exact allowed and forbidden paths and
effects; unresolved unknowns; and stop conditions.

Routine reads within one unchanged task do not require repeated refresh.
Expensive evidence need not be re-created when its owning bytes and lifecycle
remain exact; the active role may verify the durable binding instead. Any
material ambiguity stops before effect and routes to the role that owns it.

### 2. Bounded Current-Context Packet

After a refresh or handoff, the active role must be able to identify:

- repository, branch/base/head, issue or lane, role, and risk tier;
- governing issue, contract, accepted ADRs, review or handoff, and exact
  durable references where required;
- current findings with lifecycle, blocking status, and route;
- allowed files and effects, forbidden files and effects, and authority expiry
  or consumption state when applicable;
- verified facts, derived classifications, unresolved unknowns, and stop
  conditions; and
- the next owner or role responsible for any unresolved gate.

The packet may reuse existing handoff and `instruction_context` fields. It
must stay bounded to the current operation and link to durable sources instead
of copying the full history. Presence in a prompt, transcript, summary,
subagent output, local note, or model memory does not make historical material
current authority.

### 3. Optional Read-Heavy Subagents

Subagents are optional and primarily read-heavy. Suitable work includes source
coverage, inventory, comparison, reproduction, independent review lenses, and
other bounded evidence gathering explicitly requested by the active role or
authorized contract.

The active role retains scope, authority interpretation, synthesis, decisions,
routing, validation judgment, and the durable artifact. It must verify
material subagent claims against current sources before relying on them.
Subagent output is evidence only and cannot consume authority, widen scope,
change finding lifecycle, approve work, or claim readiness.

No subagent is required merely because a task is long, a model has spare
context, or parallel execution is available.

### 4. Exceptional Parallel-Write Admission

Parallel writes are not the default. They are admissible only when all of the
following are recorded before either writer changes durable state:

- explicit current authority for parallel writes and each writer's operation;
- disjoint file ownership and disjoint interface or semantic ownership;
- no ambiguous shared protected surface, generated artifact, lock, schema,
  migration, or external target;
- named integration owner, integration order, conflict behavior, and final
  validation responsibility;
- compatible validation and a deterministic way to detect overlap or drift;
- preservation of role boundaries and independent review; and
- ADR-0008 compatibility, including a named scoped exception when another
  repository lane is created.

An overlap, unowned interface, incompatible base, unclear integration order,
or expired authority stops the affected writers. Successful parallel work is
not precedent for future parallel admission.

### 5. Evidence-Based Finding Reactivation

A historical finding may become current again only when one artifact records:

1. the finding ID and prior disposition;
2. new current evidence;
3. either the exact condition that changed since the prior disposition or an
   explicit correction basis showing that the prior disposition was erroneous
   because the finding's exact predicate remained unsatisfied; and
4. the new lifecycle, blocking status, owner, and route.

Fixed, superseded, deferred, rejected, not-reproduced, and closed findings
remain historical otherwise. Repetition in chat, memory, an old report, or an
unchanged stale test does not reactivate or correct a finding. Fresh current
evidence may correct an erroneous prior disposition under the existing finding
ID when it demonstrates that the exact predicate never became satisfied. This
is a disposition correction, not a claim that the defect disappeared and later
recurred. If current evidence shows a different defect, use a new finding ID
unless the prior finding's exact predicate has recurred.

Reactivation or correction preserves the earlier record; it does not rewrite
history or erase the evidence that supported the prior disposition.

### 6. Durable Workflow State

Current repository and GitHub artifacts carry workflow state: issues,
contracts, ADRs, handoffs, review reports, PRs, merge records, tracker state,
and explicitly owned status artifacts. Chat length, model context, local
memory, summaries, worktree names, and subagent transcripts are navigation or
evidence only.

When durable and conversational state differ, refresh from the current durable
sources and record the mismatch. Do not reconstruct missing authority from a
long transcript or treat context retention as persistence.

### 7. Capability Non-Claim

A stronger model, larger context window, successful subagent report,
successful parallel run, or improved tool capability does not establish
authority, correctness, finding closure, review acceptance, submission or
merge readiness, deployment readiness, or permission to widen scope. Each
claim still requires its owning artifact, evidence, and workflow gate.

## Invariants And Failure Behavior

- ADR-0008 remains Accepted and unsuperseded.
- Proposed ADR-0010 and ADR-0011 remain non-precedential.
- Roles, authority order, protected-surface rules, and fresh-context Codex E
  ownership remain unchanged.
- Historical evidence is preserved but cannot silently become current.
- No new serialized packet, validator, service, database, broker, scheduler,
  role, or enforcement gate is created.

Fail closed and route to Codex A or B when authority, scope, ownership,
reactivation basis, or parallel-write admission is ambiguous. Route concrete
implementation defects to D and independent verification to E under existing
rules. The contract creates no automatic retry or fallback path.

## Side Effects And Exact Package

This Codex B task may change exactly:

1. `docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`;
2. `docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md`;
3. the ADR-0012 index row in `docs/decisions/README.md`.

It may not edit governance authority files, roles, templates, skills,
checkers, tests, runtime files, Role Pool files, issues, PRs, or external
state. It may not create or run subagents or parallel editors.

## Validation And Acceptance

Required validation:

```powershell
git diff --check
py -B tools/check_agent_docs.py
Write-Output <three-exact-paths> | py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
Write-Output <three-exact-paths> | py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
Write-Output <three-exact-paths> | py -B tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Codex E must also verify exact changed paths, ADR-0012 uniqueness, `Proposed`
status, source lifecycle, clause consistency, ASCII, no trailing whitespace,
and one final newline per file. Acceptance requires no semantic conflict with
ADR-0008 and no change to #776, PR #800, or their files.

## Risks And Non-Claims

The main risk is adding ceremony or making optional helpers appear mandatory.
The finite triggers, bounded packet, read-heavy default, exceptional-write
test, and evidence-based reactivation rule are intended to reduce that risk.

This contract does not claim that current work is inconsistent, that prior
findings were wrongly closed, or that subagents or parallel work are needed.
It authorizes no implementation, enforcement, subagent, parallel write,
submission, acceptance, merge, closure, deployment, readiness, correctness,
security, or privacy action or claim.

## Next Role

Next role: fresh Codex E, independent contract and proposed-ADR reviewer.

## Pasteable Next-Role Prompt

Use the Mythic Edge agent constitution and `$mythic-edge-workflow`.

Act as Codex E: Independent Long-Horizon Context and Delegation Governance
Package Reviewer.

Repository: `Tahjali11/Mythic-Edge`

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/801>

Activation record:
<https://github.com/Tahjali11/Mythic-Edge/issues/801#issuecomment-5162434870>

Review exactly:

- `docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`
- `docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md`
- the ADR-0012 index row in `docs/decisions/README.md`

Bind the exact base commit, changed-path set, and artifact SHA-256 values from
the Codex B handoff. Independently verify all seven clauses, source lifecycle,
ADR-0008 compatibility, ADR-0010/ADR-0011 non-precedence, ADR-0012 `Proposed`
status, #682 source-material treatment, WIP-1 compatibility, fresh-context
review rules, finding-reactivation closure, and every non-claim. Confirm that
the package creates no implementation, subagent, parallel-write, submission,
merge, deployment, or readiness authority.

Run the contract-required path-scoped validation. Do not edit the package,
create or run subagents, change #776 or PR #800, stage, commit, push, create a
PR, accept ADR-0012, merge, close issues, or deploy. Report findings first and
return an exact workflow handoff. Route any contract defect to Codex B; route
an exact accepted package only to a separately authorized next role.

```yaml
workflow_handoff:
  role_performed: "Codex B: Long-Horizon Context and Delegation Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/801"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  activation_record: "https://github.com/Tahjali11/Mythic-Edge/issues/801#issuecomment-5162434870"
  completed_thread: "B"
  next_thread: "E"
  base_branch: "origin/main"
  target_branch: "unselected_pending_review"
  branch: "codex/long-horizon-context-delegation-contract-801"
  base_commit: "be840bc1160678a9678d792d3cfd6074ac86ebca"
  source_artifact: "docs/contracts/governance_long_horizon_context_and_delegation_discipline.md"
  target_artifact: "docs/contract_test_reports/governance_long_horizon_context_and_delegation_discipline.md"
  proposed_adr: "docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md"
  files_changed:
    - "docs/contracts/governance_long_horizon_context_and_delegation_discipline.md"
    - "docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md"
    - "docs/decisions/README.md"
  adr_0012_status: "Proposed"
  adr_0008_superseded: false
  implementation_authorized: false
  subagent_execution_authorized: false
  parallel_writes_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  generated_residue_count: 0
  validation:
    - "git diff --check: passed"
    - "agent docs consistency: passed with 0 errors and 0 warnings"
    - "protected-surface gate: passed with 0 forbidden and 0 warnings"
    - "secret/private-marker scan: passed with 0 forbidden and 0 warnings"
    - "validation selection: passed with 3 required and 1 recommended check"
    - "exact paths, lifecycle, clauses, ASCII, whitespace, and final LF: passed"
  remaining_risk: "fresh independent Codex E review and any later ADR acceptance remain outstanding"
  next_recommended_role: "Codex E: independent long-horizon governance package reviewer"
```

```yaml
instruction_context:
  role: "B"
  risk_tier: "high governance risk; no runtime change"
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
  proposed_adrs_read:
    - "ADR-0010"
    - "ADR-0011"
  protected_surfaces:
    - "repository lane authority and WIP-1"
    - "delegation and parallel-write boundaries"
    - "finding lifecycle and review authority"
  authority_conflicts_found: false
  stop_conditions:
    - "any overlap with #776 or PR #800"
    - "any changed path outside the exact three-path package"
    - "any runtime, enforcement, subagent, or parallel-write implementation"
```
