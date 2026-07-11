# Core Frontend API Client Residual Decomposition Decision Packet Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/732

## Trackers

- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Parent residual queue: https://github.com/Tahjali11/Mythic-Edge/issues/715

## Contract

`docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md`

## Implementation Under Test

No implementation is under test. This is an independent docs-only contract
review on branch `codex/frontend-api-validation-residual-732` at
`ea7bda2466bd78fa35a0529fa46a65cc7fb3a569`.

## Report Lifecycle

`report_lifecycle: final_approval`

## Findings

### CT-732-E-002 - P1 - Fixed-state confirmation

`finding_lifecycle: fixed_state_followup`

Observed in the revised contract:

- The complete ARS/Refactor projection distinguishes absent retained evidence,
  issue #148 lineage, and actual retained tool-result evidence.
- V1 now sets `owner_exception_route: unsupported_v1`, requires
  `owner_exception_ref: none` and lifecycle `not_applicable`, and keeps every
  exception authority boolean false.
- Any missing, non-`none`, approval-like, consumed, replayed, expired, unknown,
  caller-overridden, or prose-contradicted exception value fails closed to
  `review_required`, keeps fresh evidence required, and keeps Codex C false.
- V1 defines no exception-consumption transition because it recognizes no
  exception route.
- Before implementation review, evidence must exist as a retained, current,
  matching-scope result. A separate implementation issue must independently
  authorize the selected child and supporting predicates.

Derived:

The owner-exception bypass and its caller-asserted lifecycle have been removed
instead of weakened. Issue #148 remains lineage only, fresh retained evidence
is mandatory, and implementation authority remains a separate unsatisfied
gate. CT-732-E-002 is fixed and no longer blocking.

No further clarification is required for the v1 lifecycle finding.

### CT-732-E-001 - P1 - The Phase 5 extension and decision route do not fail closed

`finding_lifecycle: original_finding`

Observed:

- The shared Phase 5 contract requires its literal base `packet_schema`,
  `candidate_scope: governance_report_helper_only`, a complete required
  envelope, and exactly one decision per candidate.
- It permits `mixed_governance_runtime_surface` only with `review_required` or
  `request_scope_split_child`.
- The #732 packet instead declares a custom `packet_schema`, a frontend-specific
  candidate scope, `candidate_surface_class: mixed_governance_runtime_surface`,
  `candidate_decision: same_repo_decomposition_candidate`, and
  `final_decision: request_fresh_ars_refactor_evidence`.
- The packet says it extends the shared shape, but it does not explicitly state
  that it is not a direct base-schema instance, define an exact
  `schema_extension_scope`, identify which vocabulary fields are inherited or
  overridden, or define a cross-field route that permits this class/decision
  pair.
- Required base envelope fields including `repository`, `tracker`,
  `related_decomposition_tracker`, `related_ars_gate_issue`,
  `phase_5_order_preserved`, the three deferred-surface flags,
  `source_mutation_authorized`, and `truth_or_assurance_claimed` are absent from
  the packet envelope.

Derived:

The current envelope has two decision-like fields and a final route the base
contract forbids for its selected primary class. A base-only validator must
reject it, while the #732 contract does not define a complete issue-specific
extension that could validate it. This is blocking because later evidence and
implementation routing cannot deterministically distinguish the advisory
same-repo assessment from the authoritative fail-closed decision.

Required contract clarification:

- Define a complete issue #732 schema extension, including exact extension
  scope, inherited vocabulary, overridden fields, and all required false
  authority/deferred-surface fields.
- Define the selected class and allowed final-decision cross-field pair.
- Retain exactly one authoritative `final_decision`. Represent the possible
  same-repo child as a clearly non-authoritative assessment, not a second
  decision field.
- Require unknown, missing, contradictory, or unsupported extension fields to
  fail closed to `review_required` and `ready_for_codex_c: false`.

### CT-732-E-002 - P1 - Current ARS/Refactor evidence state is not a complete closed projection

`finding_lifecycle: original_finding`

Observed:

- The prose correctly says Automation Artifacts issue #148 produced no retained
  ARS or Refactor Scout artifact and cannot be reused.
- The packet envelope records only
  `ars_refactor_evidence_status: fresh_scoped_evidence_required_before_implementation`
  and `fresh_scoped_evidence_needed: yes`.
- It omits the shared evidence fields for prior ARS and Refactor Scout results,
  reviewed repository/scope/commit, version bundle, current target commit,
  relevant changes, exact evidence status, and reason.
- It also has no closed current value for an actual retained tool-result
  reference, and no closed fields that distinguish an absent result from an
  exact future owner exception and that exception's bounded/unconsumed
  lifecycle.

Derived:

The prose is conservative, but the durable packet cannot mechanically prove
that approval or issue lineage is not being treated as tool evidence. It also
cannot validate a future exception without relying on free-form interpretation.

Required contract clarification:

- Add the complete shared evidence-status projection with current values that
  express no prior retained result and no reviewed target.
- Add an exact retained-result reference sentinel such as `none`, or bind the
  canonical owning-repository result field if one exists.
- If an owner exception remains an allowed route, define its exact required
  reference, target/scope binding, lifecycle status, and fail-closed
  missing/consumed/expired behavior. Keep it separate from ARS/Refactor result
  evidence and from implementation authority.

### CT-732-E-003 - P2 - The proposed private import graph omits required existing authorities

`finding_lifecycle: original_finding`

Observed:

- The allowed import diagram names only `api.ts -> match_journal.ts ->
  primitives.ts`.
- The current validator also depends on `MatchJournalApiError` from
  `frontend/src/api/errors.ts` and on Match Journal constants and types from
  `frontend/src/types.ts`.
- The contract closes the #695/#696 error ownership and says `types.ts` retains
  response-shape ownership, but it does not state how the proposed private
  validator may import those authorities.

Derived:

A later implementer cannot satisfy the listed import graph and compile the
validator without either adding undeclared dependency edges, duplicating
constants/errors, or changing ownership. The intended solution appears narrow,
but the contract should say it explicitly.

Required contract clarification:

- Extend the import graph to allow the private Match Journal validator to
  import the existing error class and Match Journal constants/types from their
  current owning modules.
- Prohibit duplication, re-export, and ownership changes for those dependencies.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-732-E-001 | P1 | `fixed_state_followup` | fixed | not_blocking | #732 envelope conflicted with the shared Phase 5 schema and encoded two decision-like fields. | Revised contract lines 492-651 define a non-base extension, complete envelope, one candidate row, one `final_decision`, and fail-closed routing. | none |
| CT-732-E-002 | P1 | `fixed_state_followup` | fixed | not_blocking | No retained evidence existed, and earlier revisions retained an unverifiable owner-exception lifecycle. | Revised contract lines 340-432 removes the bypass, fixes the only exception state to `unsupported_v1`, fails attempted exception values closed, and requires retained current matching-scope evidence. | none |
| CT-732-E-003 | P2 | `fixed_state_followup` | fixed | not_blocking | Proposed import graph omitted required existing error and type authorities. | Revised contract lines 181-230 permits exact imports from `errors.ts` and `types.ts` and forbids duplication, re-export, ownership drift, and reverse imports. | none |

## Contract Summary

The packet must preserve the completed #695/#696 API-client boundary, select
  one smallest private response-validation family, keep `frontend/src/api.ts` as
  the stable public facade and HTTP orchestrator, freeze behavior, and require
  fresh retained matching-scope evidence before any later implementation issue.

No implementation, file move, ARS/Refactor execution, protected behavior
change, or readiness/truth/assurance claim is authorized.

## Internal Project Area Reviewed

Local App frontend browser-to-loopback API validation, specifically the Match
Journal response validator behind the stable frontend API facade.

## Bridge-Code Status Reviewed

`mixed_governance_runtime_surface`, with a proposed future private same-repo
validator child. The current packet remains docs-only and non-authoritative for
implementation.

## Checks Run

```text
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git diff --name-status origin/main...HEAD
gh issue view 732 --repo Tahjali11/Mythic-Edge --json number,title,state,body,url,comments
gh issue view 715 --repo Tahjali11/Mythic-Edge --comments
gh issue view 695 --repo Tahjali11/Mythic-Edge --json number,state,title,url
gh pr view 696 --repo Tahjali11/Mythic-Edge --json number,state,mergedAt,mergeCommit,baseRefName,headRefName,url,title,files
gh issue view 148 --repo Tahjali11/Mythic-Edge-Automation-Artifacts --json number,state,title,url,comments
git rev-parse HEAD
git rev-parse origin/main
git rev-parse HEAD:frontend/src/api.ts
git rev-parse HEAD:frontend/src/api.test.ts
py tools/check_agent_docs.py
git diff --check
new-file whitespace checks for the contract and review report
py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
py tools/select_validation.py --base origin/main --paths-from-stdin
```

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed for both docs-only paths.
- Vocabulary coherence: passed; the Phase 5, evidence, and unsupported-exception
  vocabularies are closed.
- Authority semantics: implementation and evidence execution remain false;
  no owner exception or approval substitutes for retained evidence.
- Fail-closed schemas: passed for the Phase 5 extension, final decision,
  evidence state, unsupported exception route, and import graph.
- Protected-surface rollout: remains docs-only; no source or runtime change was
  made.

## Results

- Branch and `origin/main` matched at
  `ea7bda2466bd78fa35a0529fa46a65cc7fb3a569` with left/right count `0 0`.
- The only pre-review change was the untracked contract. This review added only
  the untracked contract-test report.
- The bound `api.ts` blob is
  `854d692fabc17075ce9c609f67100f8ba02f115c`; the bound `api.test.ts` blob is
  `62ecce496f018a76adf20bdcb5dcc6760d1c0c24`.
- Agent docs passed: errors 0, warnings 0.
- Tracked diff and both new-file whitespace checks passed.
- Protected-surface scan passed: forbidden 0, warnings 0.
- Secret/private-marker scan passed: forbidden 0, warnings 0.
- Validation selector passed with no warnings and selected docs-only checks.
- Runtime/frontend tests were not run because no implementation or runtime
  behavior is under test or authorized.
- CT-732-E-001 and CT-732-E-003 are fixed-state confirmed.
- CT-732-E-002 is fixed-state confirmed. V1 has no owner-exception bypass or
  consumption transition, and retained current matching-scope evidence remains
  mandatory.

## Confirmed Contract Matches

- The inspected commit and `api.ts`/`api.test.ts` blobs match the packet.
- Issue #695 is closed and PR #696 is merged at the recorded merge commit.
- The completed errors, paths, and request-helper boundary is preserved.
- Match Journal response validation is the smallest named domain validator
  family in the current facade.
- `REQUIRED_MATCH_JOURNAL_FIELDS`, `validateMatchJournalResponse`, and
  `isMatchJournalStatus` form one coherent invariant.
- `isRecord` and `isStringArray` are genuinely shared and must not become
  Match Journal-owned or public.
- Public fetch/control functions, request orchestration, JSON parsing,
  non-OK-envelope handling, guard use, and facade exports remain outside the
  proposed child.
- The accepted status vocabulary and current validation behavior match source.
- The validation and rollback plans are narrow and behavior-preserving.
- Issue #148 is correctly classified as overtaken without retained tool
  evidence.
- The extension is explicitly not a direct base-schema instance and contains
  exactly one authoritative `final_decision`.
- The private validator import graph preserves existing error/type ownership
  without duplication, re-export, or circular imports.
- All implementation, movement, tool-run, behavior-change, readiness, truth,
  and assurance authority remains false.

## Contract Mismatches

- None.

## Missing Tests

No runtime tests are required for this docs-only review. The future validation
plan correctly requires focused facade tests for accepted/rejected Match
Journal payloads, request behavior, safe errors, and the full frontend suite.

## Drift Notes

- Source drift: none; both bound frontend blobs match the reviewed commit and
  current `origin/main`.
- Issue/PR lifecycle drift: none; #732 is open, #695 is closed, and #696 is
  merged.
- Evidence lifecycle drift: none. Issue #148 and absent retained evidence are
  encoded correctly, and v1 does not recognize an exception lifecycle.
- Private/local, deployment, and production drift were not inspected and are
  outside this docs-only review.

## Recommendation

Approve the revised docs-only decision packet for Codex F submission after
target-branch authority is confirmed. Contract acceptance does not authorize
Codex C or implementation. After durable submission, route only to a separately
authorized fresh scoped ARS/Refactor evidence lane.

## Next Workflow Action

Next role: Codex F / docs-only submitter after target-branch authority check.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/732"
  parent_residual_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  completed_thread: "E_contract_confirmation"
  next_thread: "F_docs_only_submitter_after_target_authority_check"
  branch: "codex/frontend-api-validation-residual-732"
  source_artifact: "docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md"
  target_artifact: "docs/contract_test_reports/core_frontend_api_client_residual_decomposition_decision_packet.md"
  risk_tier: "High overall; Medium-High selected child"
  reviewed_commit: "ea7bda2466bd78fa35a0529fa46a65cc7fb3a569"
  finding_status:
    CT-732-E-001: "fixed_state_confirmed"
    CT-732-E-002: "fixed_state_confirmed"
    CT-732-E-003: "fixed_state_confirmed"
  review_verdict: "contract_accepted_docs_only"
  packet_final_decision: "request_fresh_ars_refactor_evidence"
  owner_exception_route: "unsupported_v1"
  fresh_scoped_evidence_needed_before_implementation: true
  ready_for_codex_c: false
  implementation_authorized: false
  file_move_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  frontend_behavior_change_authorized: false
  validator_behavior_change_authorized: false
  public_facade_change_authorized: false
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  next_recommended_role: "Codex F docs-only submitter; then separately authorized fresh scoped evidence lane"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "High"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0001-parser-owns-truth.md"
    - "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
    - "docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md"
  protected_surfaces:
    - "frontend browser-to-loopback response validation"
    - "local request-guarded Match Journal routes"
    - "stable public frontend API facade"
    - "parser, analytics, and Match Journal truth boundaries"
    - "private and local artifact boundaries"
  authority_conflicts_found: false
  authority_conflict_notes: "None. V1 removes the owner-exception bypass, requires retained current matching-scope evidence, and keeps implementation separately unauthorized."
  stop_conditions:
    - "Do not authorize Codex C, implementation, or file movement."
    - "Do not run ARS or Refactor Scout from this contract review."
    - "Do not change frontend/API/backend/runtime/truth/transport/CI/deployment behavior."
```
