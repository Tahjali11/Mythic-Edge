# Long-Horizon Context And Delegation Discipline Contract Test Report

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/801>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/746>

## Contract

[`docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`](../contracts/governance_long_horizon_context_and_delegation_discipline.md)

Reviewed SHA-256:
`47330b71e0a96133dd041011ea971f133717e2e2c9dfc68e534cf964b767c5a8`

## Package Under Test

Docs-only package on branch
`codex/long-horizon-context-delegation-contract-801`:

- `docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`
- `docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md`
- the ADR-0012 row in `docs/decisions/README.md`

The proposed ADR SHA-256 is
`96780a3eb63f9cf824722ce423125c7d922ecc66dbbda830058e2cd480a4831a`.

## Report Lifecycle

`report_lifecycle: initial_contract_test`

## Contract Summary

The package consolidates long-horizon current-authority refresh, bounded
context, optional read-heavy subagent assistance, exceptional parallel-write
admission, evidence-based finding reactivation, durable workflow state, and
capability non-claims. It extends accepted ADR-0008 without superseding it and
introduces no runtime behavior, enforcement mechanism, role, schema, or
execution authority.

## Internal Project Area Reviewed

`Quality / Governance`.

## Bridge-Code Status Reviewed

`not_bridge_code`. This is a proposed governance decision and contract, not a
runtime migration or compatibility layer.

## Findings

No blocking findings.

## Checks Run

```text
git fetch --prune
git status --short --branch
git rev-parse HEAD
git rev-parse HEAD^{tree}
git rev-parse origin/main
git rev-list --left-right --count origin/main...HEAD
git diff --name-only be840bc1160678a9678d792d3cfd6074ac86ebca..origin/main
git diff --check
bundled-python -B tools/check_agent_docs.py
three exact paths | bundled-python -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
three exact paths | bundled-python -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
three exact paths | bundled-python -B tools/select_validation.py --base origin/main --paths-from-stdin --format text
GitHub issue #801, activation comment, tracker, source issue #682, PR #685,
PR #800, and duplicate-PR reads
exact SHA-256, byte-count, ASCII, final-LF, process, and residue checks
manual clause-by-clause contract/ADR consistency review
```

The repository `py` launcher could not locate an installed interpreter in the
review tool session. The same repository scripts and arguments were therefore
run with the bundled workspace Python runtime; no validation logic changed.

## Results

- Contract: 15,957 bytes; required SHA-256 exact; ASCII; final LF present.
- Proposed ADR-0012: 9,520 bytes; required SHA-256 exact; ASCII; final LF
  present; status `Proposed`.
- ADR index: one ADR-0012 row; no ADR-0012 exists on refreshed `origin/main`.
- Exact package scope: three paths. The index change is only the ADR-0012 row.
- Agent docs: 55 files checked, 0 errors, 0 warnings.
- Protected-surface gate: 3 paths, 0 forbidden, 0 warnings.
- Secret/private-marker gate: 3 paths, 0 forbidden, 0 warnings.
- Validation selector: 3 required, 1 recommended, 0 warnings.
- Diff and whitespace validation: passed.
- Matching task processes: 0.
- Generated residue: 0.

## Governance Review

- Material refresh triggers are finite and tied to lifecycle or consequential
  transitions; routine reads in one unchanged task do not require repeated
  refresh.
- Current repository and GitHub authority outrank historical prompts, chat,
  memory, local worktree names, and subagent output.
- Existing handoff and `instruction_context` structures carry bounded context;
  the package creates no packet schema or database.
- Subagents remain optional evidence helpers. The active A-G/H role retains
  scope, authority interpretation, synthesis, validation, routing, judgment,
  and durable-artifact ownership.
- Parallel writes remain exceptional and require explicit disjoint ownership,
  protected-surface separation, integration ownership and order, overlap
  detection, compatible validation, conflict behavior, role boundaries, and
  ADR-0008 compatibility.
- Historical findings cannot silently regain current blocking status. A
  reactivation requires the prior disposition, new current evidence, changed
  condition, current lifecycle, blocking status, owner, and route.
- Stronger models, longer context, successful helper output, and successful
  parallel execution do not create authority, correctness, closure, readiness,
  deployment permission, or scope expansion.

## Source And Freshness Reconciliation

- ADR-0008 remains `Accepted` and unsuperseded.
- ADR-0010 and ADR-0011 remain `Proposed` and non-precedential.
- PR #685 is merged and issue #682 is closed; its contract remains source
  material without granting #801 implementation authority.
- Issue #801 and tracker #746 remain open. No duplicate open PR for this
  long-horizon package was found.
- During review, `origin/main` advanced from the bound base
  `be840bc1160678a9678d792d3cfd6074ac86ebca` to PR #800 merge commit
  `1c2451020d8ff3ff3f7b8b2be023a91d322c61b8`.
- The merge changed eleven #776 paths and none of the three #801 package paths.
  PR #800 is merged, so its competing active PR no longer occupies the WIP-1
  slot. The already activated and tracker-selected #801 lane can continue
  under ordinary WIP-1; the temporary second-lane exception grants no later
  authority.

## Contract Mismatches

None.

## Remaining Risks

- ADR-0012 remains `Proposed`; this review does not make it precedent.
- Any submission must refresh from current `origin/main`, preserve the exact
  reviewed package bytes, and stage only the package plus this report.
- Acceptance, merge, governance enforcement, subagent execution, parallel
  writes, and any runtime or external effect require their own current
  authority.

## Recommendation

`accept_exact_long_horizon_context_and_delegation_governance_package`

The package is eligible for a separate owner submission decision and Codex F.
This review grants no submission, acceptance, merge, deployment, subagent,
parallel-write, runtime, or readiness authority.

```yaml
workflow_handoff:
  role_performed: "Codex E: Independent Long-Horizon Governance Package Reviewer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/801"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  branch: "codex/long-horizon-context-delegation-contract-801"
  reviewed_base: "be840bc1160678a9678d792d3cfd6074ac86ebca"
  refreshed_origin_main: "1c2451020d8ff3ff3f7b8b2be023a91d322c61b8"
  contract_sha256: "47330b71e0a96133dd041011ea971f133717e2e2c9dfc68e534cf964b767c5a8"
  proposed_adr_sha256: "96780a3eb63f9cf824722ce423125c7d922ecc66dbbda830058e2cd480a4831a"
  reviewed_package_path_count: 3
  contract_verdict: "accepted_exact_long_horizon_context_and_delegation_governance_package"
  blocking_finding_count: 0
  adr_0012_status: "Proposed"
  adr_0008_superseded: false
  adr_0010_status_changed: false
  adr_0011_status_changed: false
  subagent_execution_performed: false
  parallel_writes_performed: false
  owner_submission_decision_eligible: true
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Owner submission decision, then Codex F: Module Submitter"
```

## Post-Merge Lifecycle Correction Candidate

PR #802 merged the reviewed four-file package as
`5b83dc33f933c6e58895277fb8bd9dfb5ab641bb`, after which two P2 review
findings remained current:

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-GOV-801-802-E-001` | P2 | `remaining_blocker` | `fix_attempted_pending_independent_confirmation` | blocking | PR #802 thread `3701539177`: the finding-reactivation rule lacked a correction path when fresh evidence proves that a prior fixed disposition was erroneous and the exact predicate never became satisfied. | PR #804 head `35500fd63a2530226abfb4601c3d2a0e49e808dc` contains the candidate contract and ADR correction; fresh Codex E verification remains pending. | E |
| `ME-GOV-801-802-E-002` | P2 | `remaining_blocker` | `fix_attempted_pending_independent_confirmation` | blocking | PR #802 thread `3701539183`: the continuing-role handoff lacked standard routing fields and a pasteable next-thread prompt. | The report-only continuation correction records the prompt, required fields, stable finding rows, exact correction binding, and freshness; fresh Codex E verification remains pending. | E |

The contract and proposed ADR now distinguish a disposition correction from a
finding recurrence. The historical review record above remains preserved.
These post-merge candidate bytes are not independently accepted by this
addition and route to fresh Codex E review before any follow-up submission.

### Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Post-Merge Lifecycle Correction Reviewer for issue
#801.

Review only the post-merge correction diff in:
- docs/contracts/governance_long_horizon_context_and_delegation_discipline.md
- docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md
- docs/contract_test_reports/governance_long_horizon_context_and_delegation_discipline.md

Confirm that fresh current evidence can correct an erroneous prior disposition
under the same finding ID when its exact predicate never became satisfied,
without allowing stale evidence or repetition alone to reactivate a finding.
Confirm that the current continuation packet contains the standard repository,
role, branch, artifact, validation, finding-lifecycle, correction-binding,
freshness, and stop-condition fields. Bind review to correction head
`35500fd63a2530226abfb4601c3d2a0e49e808dc`, the recorded contract and ADR
hashes, and the exact report SHA-256 in the current Codex D handoff. Preserve
the historical review record and ADR-0012 Status: Proposed.

Do not edit files, accept ADR-0012, authorize enforcement, stage, commit, push,
merge, close issues, or change tracker state. Lead with findings and route to
Codex F only if both P2 findings are fixed on the exact reviewed bytes.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/801"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "PR #802 review threads 3701539177 and 3701539183"
  target_artifact: "docs/contract_test_reports/governance_long_horizon_context_and_delegation_discipline.md"
  risk_tier: "high governance risk; docs-only correction"
  base_branch: "origin/main@5b83dc33f933c6e58895277fb8bd9dfb5ab641bb"
  target_branch: "main"
  branch: "codex/long-horizon-context-lifecycle-fix-801"
  correction_binding:
    correction_head: "35500fd63a2530226abfb4601c3d2a0e49e808dc"
    contract_sha256: "358accc281b26bc84504227593a49250215e15bd1b06acfc522da9d685a8bb18"
    proposed_adr_sha256: "333bcd8502f8578a919e4b7a136e7b9cde09ccff7304ca1d4e269a1091799cd8"
    report_sha256_binding: "exact SHA-256 supplied by the completing Codex D handoff; self-embedding is intentionally avoided"
  freshness:
    current_branch: "codex/long-horizon-context-lifecycle-fix-801"
    intended_branch: "codex/long-horizon-context-lifecycle-fix-801"
    upstream_branch: "origin/codex/long-horizon-context-lifecycle-fix-801"
    branch_ahead_behind: "0 ahead, 0 behind before the report-only working-tree correction"
    issue_state: "#801 open; Project status In progress"
    tracker_state: "#746 open"
    source_artifact_status: "PR #804 open, ready, mergeable clean at exact head 35500fd63a2530226abfb4601c3d2a0e49e808dc; all six checks passed"
    target_artifact_status: "report-only Codex D correction candidate; fresh Codex E verification pending"
    local_dirty_state: "exactly the target report modified; contract and ADR remain at the correction head"
    related_open_prs: "PR #804"
    last_known_merge_or_closeout: "PR #802 merged as 5b83dc33f933c6e58895277fb8bd9dfb5ab641bb; issue closeout remains blocked"
    worktree_classification: "dedicated issue #801 source worktree"
    freshness_verdict: "route_to_codex_e"
    recommended_route: "fresh Codex E exact-byte review, then F and G only if both findings are fixed"
    verified_at: "2026-08-03"
  validation:
    - "git diff --check -> passed"
    - "py -B tools/check_agent_docs.py -> 55 files, 0 errors, 0 warnings"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "path-scoped validation selector -> 3 required, 1 recommended, 0 warnings"
    - "report lifecycle vocabulary -> exactly one initial_contract_test value"
    - "finding lifecycle records -> 2 stable remaining_blocker rows routed to E"
    - "correction binding and freshness -> exact head and artifact hashes recorded"
  stop_conditions:
    - "Do not change ADR-0012 from Proposed."
    - "Do not add enforcement, runtime behavior, or new authority."
    - "Do not stage, commit, push, merge, close issues, or change tracker state."
    - "Route any remaining contract ambiguity to Codex B."
```

```yaml
instruction_context:
  required_for_risk_tier: "high governance risk"
  deferred_for_low_risk: false
  role: "Codex D: Module Fixer"
  risk_tier: "high governance risk; docs-only correction"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
  protected_surfaces:
    - "finding lifecycle"
    - "issue and PR lifecycle"
    - "tracker hygiene"
  authority_conflicts_found: false
  authority_conflict_notes: "None. The owner authorized the bounded post-merge documentation correction."
  stop_conditions:
    - "Preserve ADR-0012 Status: Proposed and non-precedential."
    - "Preserve the historical review record."
    - "Require fresh independent Codex E review before submission."
```
