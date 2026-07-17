# Governance Bounded Scope And Informed Approval Contract Test Report

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/737>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

[`docs/contracts/governance_bounded_scope_and_informed_approval.md`](../contracts/governance_bounded_scope_and_informed_approval.md)

## Implementation Under Test

Docs-only package on branch `codex/bounded-scope-informed-approval-737`:

- `docs/contracts/governance_bounded_scope_and_informed_approval.md`
- `docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md`
- the ADR-0010 index row in `docs/decisions/README.md`

Review authority:

- [`docs/agent_constitution.md`](../agent_constitution.md)
- [`docs/agent_threads/contract_test.md`](../agent_threads/contract_test.md)
- [`docs/templates/contract_test_report.md`](../templates/contract_test_report.md)

## Report Lifecycle

`report_lifecycle: followup_after_contract_revision`

## Contract Summary

The package must define bounded workflow authority and informed approval while
keeping routine local work proportionate. Consequential work must fail closed,
approval must not transfer or expand silently, and existing protected-surface,
WIP-1, E-to-D, submitter, merge, deployment, and truth boundaries must remain
unchanged.

## Internal Project Area Reviewed

`Quality / Governance`, matching issue #737 and the contract.

## Bridge-Code Status Reviewed

`not_bridge_code`, matching the contract. This is a proposed governance policy,
not runtime or transitional product code.

## Checks Run

```text
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status --no-renames origin/main
GitHub issue #737 and referenced-issue state checks through gh
GitHub current main commit check through gh
duplicate issue-title searches through gh
git ls-tree -r --name-only origin/main docs/decisions
manual contract and ADR case analysis against current governance
mechanical four-class precedence and six-pair overlap verification
git diff --check
py tools/check_agent_docs.py
path-scoped protected-surface scan over the reviewed package and this report
path-scoped secret/private-marker scan over the reviewed package and this report
```

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. The package contains governance
  vocabulary and public GitHub references, not credentials, private evidence,
  raw paths, or sensitive payloads.
- Vocabulary coherence: passed. The four action classes use one exact
  highest-to-lowest precedence rule, all six pairwise overlaps select one
  class, and unclassifiable actions default to
  `prohibited_without_new_authority`.
- Authority semantics: prerequisite evidence, permission, role readiness,
  review, submission, merge, deployment, truth, and assurance remain separate.
- Fail-closed schemas: no machine schema or validator is introduced. The
  natural-language classifier must still be deterministic because it selects
  materially different approval rules.
- Protected-surface rollout: docs-only proposal preserved. No runtime,
  validator, CI, protected product behavior, or external-state behavior changed.

## Results

The branch and live `main` both resolve to
`5c07b12c4b5a03b8be0a8730bf83f1d16e52a96a`. ADR-0010 is the next unused ADR
number on `origin/main`, remains `Proposed`, and its index row agrees. Issue
#737 is the sole exact informed-approval title match. Referenced issue and ADR
boundaries are preserved.

The revised package is ready for Codex F. The contract and proposed ADR now
select exactly one approval rule for every overlap without weakening the
consequential or prohibited classes.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-737-001 | P1 | `confirmation_after_contract_revision` | `fixed_confirmed` | nonblocking | The original contract and ADR required exactly one class but supplied no precedence for overlapping predicates. | Contract lines 146-160 now require `prohibited_without_new_authority > consequential > scoped_workflow > routine_local` and default unknown evidence to prohibited. Lines 560-570 cover all six class pairs plus the unknown default. ADR-0010 lines 81-93 uses the same order and preserves consequential classification for protected or external work even when bounded by an issue or contract. Mechanical verification confirmed all seven rows. | F |

## Confirmed Contract Matches

- The authority dimensions include repository, purpose, role, operations,
  artifacts, exclusions, side effects, lifecycle, validation/rollback, and next
  gate.
- Missing, stale, expired, revoked, superseded, consumed, mismatched,
  contradictory, and unverifiable authority fails closed.
- Clear current instructions may satisfy an exact informed approval without a
  magic phrase or duplicate confirmation.
- Approval does not silently transfer across repositories, roles, operations,
  paths, targets, versions, or lifecycle.
- ADR-0008 and issues #713, #682, #650, and #652 retain their narrower scopes.
- ADR-0009 remains proposed and non-precedential.
- ADR-0010 is proposed and creates no implementation, submission, merge,
  deployment, truth, readiness, security, or privacy authority.

## Contract Mismatches

None remain.

## Resolved Finding

### CT-737-001: deterministic exact-one action classification

The revised contract evaluates predicates in this exact order and stops at the
first match:

1. `prohibited_without_new_authority`
2. `consequential`
3. `scoped_workflow`
4. `routine_local`

The contract's pairwise matrix covers all six unordered class pairs. It also
requires unclassifiable actions to default to
`prohibited_without_new_authority`. The proposed ADR contains the same order
and explicitly prevents an issue or contract from downgrading protected or
external work from `consequential` to `scoped_workflow`.

## Remaining Test Gaps

None for CT-737-001. This is a natural-language governance policy, not a
validator implementation; its complete finite pairwise decision table was
verified directly.

## Drift Notes

- Repository drift: none. Local `origin/main`, branch `HEAD`, and GitHub `main`
  are the same commit.
- Issue lifecycle drift: none material. #737 and tracker #568 remain open;
  referenced issue states match the proposal's preservation claims.
- ADR drift: none. ADR-0010 is unused on `origin/main`; ADR-0009 remains
  proposed.
- Runtime, workbook, deployment, and local-data drift: not applicable to this
  docs-only review.

## Recommendation

`accept`

Route the exact reviewed docs package to Codex F. ADR-0010 remains `Proposed`;
review acceptance grants no merge, deployment, protected-surface, external, or
production authority.

## Next Workflow Action

Next role: Codex F - Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #737.

Submit only the independently reviewed docs package:
- docs/contracts/governance_bounded_scope_and_informed_approval.md
- docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md
- docs/decisions/README.md
- docs/contract_test_reports/governance_bounded_scope_and_informed_approval.md

Confirm CT-737-001 is `fixed_confirmed`, rerun the contracted docs and safety
validation, stage exactly those four files, commit, push the issue branch, and
open a draft PR against main that references #737 and tracker #568.

Do not change content during submission, stage unrelated files, mark ADR-0010
Accepted, merge, deploy, close issues, or grant implementation, protected,
external-write, merge, or deployment authority.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/737"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E_confirmation"
  next_thread: "F"
  source_artifact: "docs/contracts/governance_bounded_scope_and_informed_approval.md and proposed ADR-0010"
  target_artifact: "docs/contract_test_reports/governance_bounded_scope_and_informed_approval.md"
  risk_tier: "High workflow risk; no runtime behavior change"
  base_branch: "origin/main"
  branch: "codex/bounded-scope-informed-approval-737"
  finding_status:
    CT-737-001: "fixed_confirmed"
  validation:
    - "Current GitHub main and local branch base matched 5c07b12c4b5a03b8be0a8730bf83f1d16e52a96a."
    - "ADR-0010 remained the next unused number and Proposed."
    - "All six class-pair overlaps and the unknown default selected the required class."
    - "Docs, protected-surface, secret/private-marker, and diff validation passed."
  stop_conditions:
    - "Stage only the four independently reviewed docs files."
    - "Do not weaken consequential, protected, destructive, external, merge, deployment, or production gates."
    - "Do not edit runtime, validator, CI, role, template, constitution, or agent-rule surfaces."
    - "Do not merge, deploy, close issues, or mark ADR-0010 Accepted."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "High workflow risk; no runtime behavior change"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0004"
    - "ADR-0005"
    - "ADR-0008"
  protected_surfaces:
    - "workflow authority"
    - "issue and PR lifecycle"
    - "branch and merge policy"
    - "validation and approval gates"
  authority_conflicts_found: false
  authority_conflict_notes: "CT-737-001 is fixed: exact precedence and the prohibited default resolve every overlap without weakening higher-impact gates."
  stop_conditions:
    - "No implementation, merge, deployment, or protected behavior changes."
    - "Codex F may submit only the exact reviewed docs package; merge and ADR acceptance remain separate gates."
```
