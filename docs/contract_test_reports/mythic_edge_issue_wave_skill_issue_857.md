# Mythic Edge Issue-Wave Issue #857 Contract Test Report

## Findings

No blocking findings remain, and no new finding was identified.

1. `ME-IW-855-E-009` — P1 — `fixed_confirmed_current_bytes`.
   Cross-run admission now compares current non-final lane projections on both
   new-run and saved-run-reacquisition paths. Candidate scope remains immutable
   history, final lanes are excluded only from scope-token comparison, and a
   rejected admission leaves both ledgers and repository-effect boundaries
   unchanged.
2. `ME-IW-855-E-010` — P2 — `fixed_confirmed_current_bytes`.
   Expired recovery now selects in-flight interruption first, all-final
   terminal release second, an otherwise complete explicit checkpoint third,
   and interruption stop last. Terminal recovery preserves lane, artifact,
   worktree, event-chain, recovery-proof, and governance-routing evidence.
3. `ME-IW-855-E-011` — P2 — `fixed_confirmed_current_bytes`.
   The contract, helper, state reference, and installer expectation each
   declare exactly `mythic_edge_issue_wave_state.v2`.

These dispositions do not resolve or reply to the historical PR #856 threads.
They remain unresolved and not outdated as preserved source evidence.

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/857>

Historical issue: <https://github.com/Tahjali11/Mythic-Edge/issues/855>

Historical merged PR and source review:
<https://github.com/Tahjali11/Mythic-Edge/pull/856>

## Tracker

N/A.

## Contract

`docs/contracts/mythic_edge_issue_wave_skill.md`

Reviewed SHA-256:
`94e1004db2e13b71bb629f58547bcaaedb1d5894976ba5c4eb2336c512794624`.

## Implementation Under Test

The review base is current `origin/main` at
`df64b8b879f62843b05cfdf41016aafa7428a96e`, tree
`16bb2a298f3627f56ecab81404f263bf29f6ceeb`.

The existing clean verification checkout is at
`27b0d025bb6775c6a9b912ae54a8d93853d01953` and has that exact tree. The
supplied local `main` remains at
`e1fd3cf6939ef79c94e81c767d86d92f9d461c64`, 0 ahead and 25 behind. Codex E
created or moved no branch or worktree.

Codex E reviewed the Codex B contract plus exactly the four Codex D paths:

| role | path | SHA-256 |
| --- | --- | --- |
| B | `docs/contracts/mythic_edge_issue_wave_skill.md` | `94e1004db2e13b71bb629f58547bcaaedb1d5894976ba5c4eb2336c512794624` |
| D | `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py` | `4f47c1bd22cf92e7c43ab2b7eb76881627d3f864df55bbc7f8d2a53b6753600b` |
| D | `tests/test_mythic_edge_issue_wave_skill.py` | `359174d9cbb72064bfd7eaa20ca24ddf2cac87a15f20d296434f3ed9106bd0a0` |
| D | `tests/test_install_codex_skills.py` | `b4c619ab9422ea1b5a473872e8dc1c231070746a4008cb45b0e47d8809d361d0` |
| D | `docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md` | `c5baa1388e7657da5a0acb64aeb32fe4ffba78d0a2c8e73e3af156c0b6e6cfcc` |

This report is the only Codex E repository edit. It is not one of the four D
paths and does not change the reviewed implementation.

## Report Lifecycle

`report_lifecycle: final_approval`

This label is limited to independent contract review of the exact correction
bytes. It authorizes no staging, branch or worktree movement, commit, push,
draft PR, `main` target, merge, issue closure, installation, real Dispatch,
deployment, cleanup, or readiness claim. It establishes eligibility only for a
separately authorized Codex F.

## Contract Summary

The correction must satisfy three predicates without changing any other V2 or
public interface:

- admission compares every saved participant through current
  `lanes[*].scope` values outside `FINAL_STATES`, including post-A refinement,
  while `candidates[*].scope` remains immutable selection evidence;
- expired recovery selects in-flight stop, all-final terminal release,
  complete checkpoint, then unproven stop, in that order; and
- the four run-projection declarations resolve to exactly
  `mythic_edge_issue_wave_state.v2`.

Every unrelated field, transition, error, lease, reservation, event-chain,
reviewed-package, redaction, no-echo, public-path, and side-effect rule must
remain unchanged.

## Internal Project Area Reviewed

Quality / Governance.

No scope, truth-owner, or protected-surface mismatch was found.

## Bridge-Code Status Reviewed

`shared_support`

The deterministic helper remains local coordination support. It gains no Git,
GitHub, network, subagent, installation, merge, deployment, or runtime
capability.

## Authority And Freshness

- `origin/main` and its tree matched the issue #857 base after `git fetch
  --prune origin`.
- Issue #857 was open.
- Issue #855 was closed as completed.
- PR #856 was merged at the current `origin/main` commit.
- All three source review threads were unresolved and not outdated in both the
  connected GitHub read and the bundled thread-aware GraphQL read.
- The Codex B contract and Codex D handoff matched their required stop hashes.
- Issue #857 records the narrow, expiring ADR-0008
  `explicit_user_override` for E-009 through E-011 while issue #826 remains the
  other active lane.
- No authority source granted submission, `main` targeting, merge,
  installation, real Dispatch, deployment, cleanup, or readiness.

## Checks Run

Focused correction and precedence review:

```text
py -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py tests/test_install_codex_skills.py -p no:cacheprovider -k "cross_run_admission_uses_current_non_final_lane_scope_after_a or saved_run_reacquisition_uses_current_non_final_lane_scope or final_lane_scope_is_excluded_without_releasing_other_admission_guards or expired_recovery_terminal_releases_all_final_runs_before_checkpoint or expired_recovery_keeps_checkpoint_then_unproven_stop_precedence or lease_renewal_and_unknown_outcome_recovery or issue_wave_run_projection_schema_declarations_are_coherent"
-> 13 passed, 207 deselected
```

Complete focused suites:

```text
py -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py -p no:cacheprovider -k "not legacy_role_pool_tracked_tree_matches_contract_baseline"
-> 170 passed, 1 deselected

py -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py::test_legacy_role_pool_tracked_tree_matches_contract_baseline -p no:cacheprovider
-> 1 passed

py -B -m pytest -q tests/test_install_codex_skills.py -p no:cacheprovider
-> 46 passed, 3 skipped
```

The three installer skips were the existing Windows directory-symlink
capability checks.

Static and repository checks:

```text
ruff check docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py tests/test_mythic_edge_issue_wave_skill.py tests/test_install_codex_skills.py
-> passed

py -m py_compile <the same three Python files>, with bytecode cache redirected outside the repository
-> passed

py -B tools/check_agent_docs.py
-> 55 checked, 0 errors, 0 warnings

py -B tools/install_codex_skills.py --list
-> passed; list mode only, nothing installed

five reviewed inputs | py -B tools/check_protected_surfaces.py --base origin/main --repo-root . --paths-from-stdin
-> 5 paths, 0 forbidden, 0 warnings

five reviewed inputs | py -B tools/check_secret_patterns.py --base origin/main --repo-root . --paths-from-stdin
-> 5 paths, 0 forbidden, 0 warnings

git diff --no-index --check, current origin/main bytes versus each reviewed input
-> all 5 paths passed
```

The official skill-creator `quick_validate.py` was attempted with both
available project Python environments and remained unavailable because
`PyYAML` is not installed (`ModuleNotFoundError: No module named 'yaml'`). No
dependency was installed.

All tests and compilation that could create temporary files used an external
current-main snapshot or external cache/temp roots. No repository cleanup was
performed.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: unchanged. Public-output, state-integrity,
  error-behavior, and side-effect contract sections are byte-identical to
  current main; the complete issue-wave suite remains green.
- Vocabulary coherence: the exact four declarations resolve to
  `mythic_edge_issue_wave_state.v2`; no alias or migration form was added.
- Authority semantics: tests, review approval, and future CI remain
  prerequisite evidence only. They grant no F, G, merge, installation,
  Dispatch, deployment, or readiness authority.
- Fail-closed schemas: closed V2 and reviewed-package validation are unchanged.
  Malformed, stale, overlapping, uncertain, and drifted inputs retain their
  existing refusal paths.
- Protected-surface rollout: source correction only. The skill was not
  installed or used for a real Dispatch.

## Results

All three source predicates are fixed in the reviewed bytes. The complete
focused suite, installer suite, static checks, scope checks, secret checks, and
diff checks passed. No contract mismatch, implementation defect, missing
contract-required test, or unauthorized path change was found.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-IW-855-E-009` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | `not_blocking` | PR #856 `discussion_r3778988283` | Helper lines 1136-1180 and 2435-2465; tests at `tests/test_mythic_edge_issue_wave_skill.py:2355`, `:2453`, and `:2527`; 13 focused and 171 complete issue-wave checks passed | F only after separate authorization |
| `ME-IW-855-E-010` | P2 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | `not_blocking` | PR #856 `discussion_r3778988291` | Helper recovery at `issue_wave_state.py:2516` and all-final branch at `:2560`; tests at `tests/test_mythic_edge_issue_wave_skill.py:2617`, `:2722`, and existing in-flight test `:3083`; focused and complete suites passed | F only after separate authorization |
| `ME-IW-855-E-011` | P2 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | `not_blocking` | PR #856 `discussion_r3778988295` | Contract declaration at line 516, helper `STATE_SCHEMA` at line 20, state reference declaration at line 180, installer expectation at `tests/test_install_codex_skills.py:22`, and coherence test at `:327`; test passed | F only after separate authorization |

## Confirmed Contract Matches

### ME-IW-855-E-009

- `_current_non_final_scope_participants` projects only lanes outside
  `FINAL_STATES`.
- `_admission_check` uses that projection for every saved existing run and
  accepts an explicit current projection for the saved run being reacquired.
- New runs still use validated candidates only before their lane projection
  exists.
- `authorize_segment` supplies the saved run's current non-final lanes while
  retaining candidates for immutable repository and target-root identity.
- Parameterized tests cover `paths`, `interfaces`, `truth_owners`,
  `dependencies`, `shared_artifacts`, and `submission_lanes` after accepted A
  refinement.
- The tests prove candidate bytes remain unchanged, current lane scope owns the
  refinement, the rejected second run creates no run directory or ledger,
  both existing ledgers remain byte-identical on rejection, the first revision
  and reservation remain unchanged, and the candidate target root remains
  empty.
- Disjoint admission remains allowed. Final-lane scope is excluded from scope
  comparison while the independent two-wave capacity guard still rejects a
  third wave.
- The helper still has no branch, worktree, task, network, or GitHub creation
  capability, and admission remains before run-state publication or any
  root-owned repository effect.

### ME-IW-855-E-010

- `recover_expired_run` checks `RUNNING_STATES` before `FINAL_STATES`, checks
  all-final before `_segment_endpoint_reached`, and retains the final
  interruption branch.
- In-flight recovery still records `interruption_stop`, changes the in-flight
  lane to `unknown_agent_outcome`, clears the next role, and preserves the
  worktree.
- One- and two-lane all-final cases add exactly one hash-chained
  `terminal_release`, set `execution_status=terminal`, set
  `next_resumable_role=null`, set `run_complete=true`, clear hard reservation
  capacity, and persist the recovery proof.
- Terminal recovery does not alter final lane state, artifact references,
  worktree references, governance packets, or prior history. The multi-lane
  case reaches the unchanged terminal governance aggregation fallback.
- A completed non-final explicit checkpoint remains `checkpointed` with exact
  next role `C`; an unproven boundary remains `stopped` with no next role.

### ME-IW-855-E-011

The four extracted declarations are:

```text
contract:              mythic_edge_issue_wave_state.v2
helper:                mythic_edge_issue_wave_state.v2
state reference:       mythic_edge_issue_wave_state.v2
installer expectation: mythic_edge_issue_wave_state.v2
```

The regression extracts the contract and reference declarations by their
canonical markers, parses the helper assignment through Python AST, and ties
the installer assertion to one explicit expectation constant. It does not
count incidental mentions of the superseded contract-only identifier.

### Unrelated Rules And Preserved Surfaces

- AST comparison against current main found exactly three changed existing
  helper functions: `_admission_check`, `authorize_segment`, and
  `recover_expired_run`; the only added function is the private
  `_current_non_final_scope_participants`. Imports, constants, classes, and all
  other top-level declarations are unchanged.
- The contract sections for invocation through reviewed-package binding, lane
  states, public output, state integrity, lease behavior, governance feedback,
  inputs, error behavior, and side effects are byte-identical to current main.
- Historical issue #855 handoff SHA-256 remains
  `0de0e71a0e446a679fd951a17d5d1a1aa00c740836af3c59d7b5e08f35935782`.
- Historical issue #855 final E report SHA-256 remains
  `5e96cc2f7fc9a241c9cec9422f21f3cfe45a8f14a0b0af991b1feb9bbfc94063`.
- State-schema reference SHA-256 remains
  `52f4b3e418b125faad6df8ad00f67fa7626d62e0208175c1c1e6d80a66990d9a`.
- The legacy `mythic-edge-role-pool` tree remains
  `950768b80b760a0e0dfe3040df023de20eadaf81`, 38 tracked files, with zero
  working-byte mismatches.
- The pre-existing R0 contract, Wrangler file, and real Git index matched their
  supplied SHA-256 identities and were not touched.

## Contract Mismatches

None.

## Missing Tests

None for the issue #857 correction contract.

Official skill-creator validation remains unavailable because of missing
PyYAML. This is missing environment setup, not a failing correction test; no
dependency change was authorized.

## Drift Notes

- Local checkout drift: the supplied local `main` is 25 commits behind, but
  every reviewed byte was overlaid onto a non-Git snapshot of current
  `origin/main` for validation. The existing clean verification checkout
  independently matched the current-main tree. No correction-package repo
  drift was found.
- Issue lifecycle: #857 remains open as expected; #855 remains closed as
  completed.
- PR lifecycle: #856 remains merged. Its three source threads remain
  deliberately unresolved and not outdated; no reply or resolution was
  authorized.
- Local residue: the pre-existing R0 modification, Wrangler residue, real
  index, and D-generated ignored bytecode cache files were preserved. Codex E
  created no new repository cache and performed no cleanup.
- Workbook drift, deployment drift, runtime-data drift, and tracker drift:
  not observed and outside this source-only review.

## Residual Risk And Unverified Layers

- GitHub CI has not run for a future correction commit because no correction
  branch, commit, push, or PR exists.
- Installation and real write-enabled Dispatch were intentionally not run and
  remain unauthorized.
- Official skill-creator validation remains unavailable for the environment
  reason above.
- This review is not a merge, deployment, operational-safety, security,
  privacy, or production-readiness claim.

## Recommendation

`approve`

The exact correction package is eligible only for a separately authorized
Codex F. No Codex F action, target branch, submission, or later integration
effect is authorized by this report.

## Next Workflow Action

Next role: Codex F only after a fresh, explicit owner authorization for
submission and the target branch.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for
issue #857 only if the current owner instruction separately authorizes Codex F
submission and names or approves the target branch. Otherwise stop without
effect.

Refresh origin/main, issue #857, historical issue #855, merged PR #856, its
three source threads, and the local checkout/index. Read
docs/contracts/mythic_edge_issue_wave_skill.md,
docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md,
and
docs/contract_test_reports/mythic_edge_issue_wave_skill_issue_857.md. Verify
the exact reviewed hashes and current-main base before staging. If base,
contract, handoff, reviewed bytes, report, issue, thread, or authority state
drifted materially, stop and route to E, D, B, or A as appropriate.

Submit only the Codex B contract, the four Codex D paths, and the Codex E
report. Preserve the unrelated R0 modification, Wrangler residue, ignored
bytecode, historical #855 artifacts, state reference, legacy
mythic-edge-role-pool subtree, and every other path. Make no implementation or
contract edit. Stage only exact reviewed paths; do not broad-stage the mixed
worktree. Create or move a branch/worktree, commit, push, and open a draft PR
only within the fresh owner authorization. Do not resolve or reply to PR #856
threads, mark a PR ready, merge, close issues, install the skill, run real
Dispatch, deploy, clean worktrees, or claim readiness. Return exact staged,
commit, push, draft-PR, check, and remaining-risk evidence, then stop for a
separately authorized Codex G.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/857"
  tracker: "N/A"
  completed_thread: "E"
  next_thread: "F_requires_separate_owner_authorization"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill_issue_857.md"
  target_artifact: "separately_authorized_draft_pr_for_issue_857"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main_requires_separate_owner_approval"
  branch: "not_created_or_moved_by_codex_e"
  internal_project_area: "Quality / Governance"
  truth_owner: "deterministic issue-wave state helper and current module contract"
  bridge_code_status: "shared_support"
  finding_summary:
    ME-IW-855-E-009: "fixed_confirmed_current_bytes"
    ME-IW-855-E-010: "fixed_confirmed_current_bytes"
    ME-IW-855-E-011: "fixed_confirmed_current_bytes"
    new_findings: 0
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "#826"
    lane_status: "active_second_lane_under_explicit_user_override"
    tracker_selected_next_lane: ""
    exception:
      name: "explicit_user_override"
      blocked_active_issue_or_pr: "#826"
      reason: "Complete the exact issue #857 correction lifecycle before installation or real Dispatch."
      allowed_scope: "Exact ME-IW-855-E-009 through ME-IW-855-E-011 correction lifecycle only."
      expiration_condition: "Correction merge and issue closeout, explicit park/defer/cancel/reassignment, or owner revocation."
      authorized_by: "Human owner in the current task on 2026-08-13"
      recorded_in: "#857"
  freshness:
    origin_main: "df64b8b879f62843b05cfdf41016aafa7428a96e"
    origin_main_tree: "16bb2a298f3627f56ecab81404f263bf29f6ceeb"
    clean_verification_checkout: "27b0d025bb6775c6a9b912ae54a8d93853d01953 with exact origin/main tree"
    local_main: "e1fd3cf6939ef79c94e81c767d86d92f9d461c64; 0 ahead, 25 behind"
    issue_state: "#857 open; #855 closed as completed"
    pr_state: "#856 merged; three source threads unresolved and not outdated"
    verified_at: "2026-08-13"
  authority_notes:
    prerequisite_success_is_authority: false
    codex_f_authorized: false
    main_target_authorized: false
    merge_authorized: false
    installation_or_dispatch_authorized: false
    readiness_claimed: false
  validation:
    - "13 focused correction and recovery-precedence checks passed."
    - "Complete issue-wave suite: 171 passed."
    - "Complete installer suite: 46 passed, 3 Windows symlink-capability skips."
    - "Ruff, isolated compilation, skill list mode, and agent-doc checks passed."
    - "Protected-surface and secret gates: 5 reviewed inputs, 0 forbidden, 0 warnings."
    - "All five current-main byte diff checks passed."
    - "Legacy Role Pool tree preserved at 950768b80b760a0e0dfe3040df023de20eadaf81 with 38 files."
    - "Official quick_validate unavailable because PyYAML is absent; no dependency installed."
  still_unverified_layers:
    - "GitHub CI for a future correction commit and draft PR"
    - "installation"
    - "real write-enabled Dispatch"
    - "merge, deployment, and operational readiness"
  stop_conditions:
    - "No F action without fresh explicit owner authorization and approved target."
    - "Any base, issue, contract, handoff, reviewed-byte, report, or authority drift routes backward before staging."
    - "No path outside the contract, four D paths, and E report may be submitted."
    - "No historical #855, PR #856 thread, Role Pool, R0, installation, Dispatch, merge, deployment, cleanup, or readiness effect."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high workflow risk"
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
    - "ADR-0012"
  protected_surfaces:
    - "cross-run admission and concurrent repository-write isolation"
    - "expired-run recovery state and terminal governance routing"
    - "closed coordination schema identifiers"
    - "reviewed-package, public-safety, and no-echo rules"
    - "legacy Role Pool and R0-bound files (read-only and preserved)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #857 and the Codex B contract unambiguously authorize this independent correction review; no operational or submission authority follows from review success."
  stop_conditions:
    - "Any concrete implementation defect routes to D."
    - "Any contract ambiguity routes to B."
    - "Any scope expansion routes to A."
    - "No GitHub write, submission, main-targeting, merge, installation, Dispatch, deployment, cleanup, or readiness action in E."
```
