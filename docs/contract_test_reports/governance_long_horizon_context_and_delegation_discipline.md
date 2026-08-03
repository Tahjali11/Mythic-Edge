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
