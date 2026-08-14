# Mythic Edge Issue-Wave Issue #857 Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/857>

Historical source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/855>

Source review: <https://github.com/Tahjali11/Mythic-Edge/pull/856>

## Tracker

N/A.

## Contract

`docs/contracts/mythic_edge_issue_wave_skill.md`

Codex B handoff SHA-256:
`94e1004db2e13b71bb629f58547bcaaedb1d5894976ba5c4eb2336c512794624`.

## Source Findings

- `ME-IW-855-E-009`, P1, blocking: PR #856 thread
  `discussion_r3778988283` required cross-run admission to use current
  non-final lane scopes rather than immutable candidate history.
- `ME-IW-855-E-010`, P2, blocking: PR #856 thread
  `discussion_r3778988291` required proven all-final expired runs to
  terminal-release before explicit-checkpoint consideration.
- `ME-IW-855-E-011`, P2, blocking: PR #856 thread
  `discussion_r3778988295` required one exact run-projection schema identifier
  across the contract, helper, state reference, and installer expectation.

All three source threads were refreshed as unresolved and not outdated. Issue
#857 was open, issue #855 was closed as completed, and PR #856 was merged at
`df64b8b879f62843b05cfdf41016aafa7428a96e` when D began.

## Internal Project Area

Quality / Governance.

## Truth Owner

The deterministic issue-wave state helper and the current module contract.
GitHub and repository evidence remain the owners of live collaboration and
checkout facts.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer.

## Base And Checkout Verification

- Authoritative base: `origin/main` at
  `df64b8b879f62843b05cfdf41016aafa7428a96e`, tree
  `16bb2a298f3627f56ecab81404f263bf29f6ceeb`.
- Supplied task checkout: repository-root checkout on local `main` at
  `e1fd3cf6939ef79c94e81c767d86d92f9d461c64`, tree
  `1405abef7771738e3a5d3b139ef6138eb1f82e43`, 0 ahead and 25 behind
  `origin/main`.
- Existing clean current-base checkout: sibling `MythicEdge-issue-wave-855`
  checkout on branch `agent/mythic-edge-issue-wave-855` at
  `27b0d025bb6775c6a9b912ae54a8d93853d01953`; its tree is exactly the
  authoritative-base tree above.
- D created or moved no branch or worktree. Current-base validation used an
  external non-Git archive snapshot plus the existing clean checkout; the real
  local-main Git index was not used as a synthetic base.

## Intended Behavior

1. Cross-run admission compares every saved participant through current
   `lanes[*].scope` for lanes outside `FINAL_STATES`, including accepted post-A
   refinements. `candidates[*].scope` remains immutable selection history.
2. Proven expired recovery selects in-flight interruption first, all-final
   terminal release second, a remaining complete explicit checkpoint third,
   and interruption stop otherwise.
3. The contract, helper, state reference, and installer expectation declare
   exactly `mythic_edge_issue_wave_state.v2`.

## Actual Behavior Before The Fix

- `_admission_check` read each existing run's stale `candidates` projection,
  and `authorize_segment` supplied the saved run's candidates again during
  reacquisition. A second wave could therefore miss a post-A scope collision.
- `recover_expired_run` evaluated `_segment_endpoint_reached()` before the
  all-final predicate. Because final lane states satisfy the endpoint helper,
  an expired explicit all-final run became checkpointed with no next role and
  `run_complete=false`.
- Codex B had already corrected the contract-only schema drift before D. No
  helper, reference, or installer implementation schema change was needed.

## First Proven Failure Points

- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py::_admission_check`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py::authorize_segment`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py::recover_expired_run`

The correction regressions failed before the helper edit as follows:

```text
9 failed, 2 passed, 160 deselected
```

The failures were the six scope dimensions, saved-run reacquisition, and the
one-lane and two-lane all-final recovery predicates. The final-lane exclusion,
capacity guard, completed-checkpoint, and unproven-boundary cases already
passed.

## Exact Fix

- Added one private projection helper that returns current non-final lanes.
- `_admission_check` now compares incoming scope participants with each saved
  run's current non-final lane projections. New-run admission still uses its
  validated candidates because no lane projection exists yet.
- Saved-run segment authorization explicitly supplies its current non-final
  lanes while continuing to use immutable candidates for canonical repository
  and target-root identity.
- `recover_expired_run` retains the in-flight branch first, then selects
  `terminal_release` when all lanes are final, before considering an explicit
  checkpoint.
- Added only the contract-required E-009, E-010, and E-011 regression coverage.

No public command, schema, field, event type, transition, lease, reservation,
reviewed-package binding, redaction rule, stable error code, or side-effect
boundary changed.

## Files Changed

- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
  - SHA-256:
    `4f47c1bd22cf92e7c43ab2b7eb76881627d3f864df55bbc7f8d2a53b6753600b`
- `tests/test_mythic_edge_issue_wave_skill.py`
  - SHA-256:
    `359174d9cbb72064bfd7eaa20ca24ddf2cac87a15f20d296434f3ed9106bd0a0`
- `tests/test_install_codex_skills.py`
  - SHA-256:
    `b4c619ab9422ea1b5a473872e8dc1c231070746a4008cb45b0e47d8809d361d0`
- `docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md`
  - New D handoff; its final SHA-256 is reported outside this self-referential
    artifact.

## Code Changed

Runtime product code did not change. The deterministic local coordination
helper changed only in the private cross-run admission projection and expired
recovery precedence described above.

## Tests Added Or Updated

- Parameterized all six scope dimensions after an accepted post-A refinement.
- Proved immutable candidate history, current lane projection ownership,
  rejection with zero second-run ledger or target-root effect, unchanged first
  ledger bytes/revision/reservation, and admission of genuinely disjoint
  current scopes.
- Proved saved-run reacquisition compares the checkpointed run's current
  non-final lane scope.
- Proved final-lane scopes are excluded only from scope comparison while the
  two-wave capacity guard remains active.
- Proved one-lane and multi-lane all-final expiry produce exactly one valid
  `terminal_release`, terminal projection fields, persisted recovery proof,
  preserved work/artifact/governance history, and terminal governance routing.
- Proved non-final complete checkpoints remain checkpointed, unproven
  boundaries remain stopped, and the existing in-flight unknown-outcome test
  remains green.
- Added one static coherence test for the exact contract/helper/reference/
  installer run-projection identifier.

## Interface Changes

No public interface changed. `_admission_check`, a private helper, gained an
optional current-scope participant argument used only for saved-run
reacquisition. All closed public schemas and command entrypoints are unchanged.

## Contracted Area Status

The implementation stayed inside Quality / Governance shared support. No
parser, workbook, webhook, Apps Script, credential, deployment, product
runtime, legacy Role Pool, or R0 surface was touched.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: unchanged and covered by the complete focused
  suite.
- Vocabulary and example coherence: the four canonical run-schema
  declarations resolve to exactly `mythic_edge_issue_wave_state.v2`.
- Authority/readiness semantics: unchanged; passing validation grants no
  submission, merge, installation, Dispatch, deployment, or readiness
  authority.
- Fail-closed schema or validator checks: unchanged outside the two named
  predicates; overlap and uncertain recovery still stop.
- Protected-surface rollout phase: source correction only; not installed or
  used for a real Dispatch.

## Validation Run

```text
Correction red run:
  9 failed, 2 passed, 160 deselected

Correction green run, including E-011 coherence:
  12 passed, 160 deselected

Complete issue-wave suite:
  170 passed, 1 deselected in the current-main validation snapshot
  1 passed for the unchanged legacy-tree assertion in a real Git checkout
  Total: 171 passed

Complete installer suite:
  46 passed, 3 skipped
  Skips: Windows filesystem directory-symlink capability only

Ruff on all three changed Python files:
  All checks passed

Python compilation with an external bytecode cache:
  passed

Agent docs:
  55 checked, 0 errors, 0 warnings

Repo-owned skill list mode:
  passed; no installation performed

Legacy Role Pool identity:
  tree 950768b80b760a0e0dfe3040df023de20eadaf81, 38 tracked files

Final changed-path protected-surface, secret-pattern, and diff checks:
  Protected surface: 4 paths, 0 forbidden, 0 warnings; passed
  Secret patterns: 4 paths, 0 forbidden, 0 warnings; passed
  git diff --no-index --check against current origin/main bytes: passed
```

Official skill-creator `quick_validate.py` is unavailable without a dependency
change because both available project Python environments lack `PyYAML`.
No dependency was installed.

## Preserved Evidence

- Historical issue #855 implementation handoff SHA-256:
  `0de0e71a0e446a679fd951a17d5d1a1aa00c740836af3c59d7b5e08f35935782`
- Historical issue #855 final E report SHA-256:
  `5e96cc2f7fc9a241c9cec9422f21f3cfe45a8f14a0b0af991b1feb9bbfc94063`
- State-schema reference SHA-256:
  `52f4b3e418b125faad6df8ad00f67fa7626d62e0208175c1c1e6d80a66990d9a`
- Legacy Role Pool tree:
  `950768b80b760a0e0dfe3040df023de20eadaf81`, 38 tracked files.
- Pre-existing R0 contract SHA-256:
  `0d46c5f5466d542e56fbe8ee138b4710acb7d8e5878a7be3ecb20dbb629b2581`.
- Pre-existing Wrangler file SHA-256:
  `568e64df708db1aab4d2f625c38f8d590251e28ea783e073d6d1d03f5d0f00cb`.
- Real local-main Git index: 193888 bytes, SHA-256
  `0bc17b6638f2c8e638174a5b5f9d5e3d7c1d6a95bd521c149f7a9715c469d536`.

The required local Python runs generated or refreshed these ignored bytecode
cache files before subsequent compilation was redirected outside the repo:

- `docs/codex_skills/mythic-edge-issue-wave/scripts/__pycache__/issue_wave_state.cpython-313.pyc`
- `tests/__pycache__/test_install_codex_skills.cpython-313.pyc`
- `tests/__pycache__/test_mythic_edge_issue_wave_skill.cpython-313-pytest-8.4.2.pyc`
- `tests/__pycache__/test_mythic_edge_issue_wave_skill.cpython-313.pyc`

They are non-authoritative, ignored, unstaged, and outside the four-path review
package. D did not remove them because the owner expressly prohibited worktree
cleanup.

The pre-existing R0 modification and Wrangler residue remain unrelated and
untouched. The real Git index was not staged or rewritten. No issue or PR was
mutated.

## Still Unverified

- Fresh independent Codex E review of the exact correction package.
- GitHub CI for any later submitted correction commit.
- Installation and real write-enabled Dispatch were intentionally not run and
  remain unauthorized.
- Official skill-creator validation remains unavailable for the environment
  reason above; source structure, installer behavior, agent docs, compilation,
  Ruff, and the complete focused suites provide the available local evidence.

## Reviewer Focus

1. Confirm `ME-IW-855-E-009` uses current non-final lane projections on both
   existing-run and saved-run-reacquisition sides without mutating candidates.
2. Confirm `ME-IW-855-E-010` preserves in-flight interruption precedence and
   terminal-releases every proven all-final run before checkpoint recovery.
3. Confirm `ME-IW-855-E-011` extracts declarations rather than counting
   incidental prose and resolves all four sources to the exact V2 identifier.
4. Confirm no unrelated V2, reviewed-package, redaction, historical #855,
   legacy Role Pool, or R0 byte changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer for
issue #857. Refresh origin/main, issue #857, historical issue #855, merged PR
#856, and its three unresolved review threads. Read accepted ADR-0008 and
ADR-0012, docs/contracts/mythic_edge_issue_wave_skill.md, and
docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md.
Verify the supplied checkout and exact correction bytes against current
origin/main without creating or moving a branch/worktree unless separately
authorized.

Review only the Codex B contract plus the four D paths authorized by issue
#857. Re-test ME-IW-855-E-009 across all six scope dimensions and saved-run
reacquisition, ME-IW-855-E-010 across in-flight/all-final/checkpoint/unproven
precedence, and ME-IW-855-E-011 across the exact four declarations. Confirm
candidate history remains immutable, final lanes are excluded only from scope
comparison, rejected admissions are zero-effect, terminal recovery preserves
history/governance routing, and every unrelated V2/public-safety/reviewed-
package rule is unchanged.

Write only
docs/contract_test_reports/mythic_edge_issue_wave_skill_issue_857.md. Do not
fix code, edit the contract or historical #855 artifacts, resolve or reply to
PR #856 threads, touch the legacy mythic-edge-role-pool or any R0-bound path,
install the skill, run real Dispatch, stage, commit, push, open or update a PR,
target main, merge, close issues, deploy, clean worktrees, or claim readiness.
Lead with findings ordered by severity. If there is any concrete defect, route
back to D with exact evidence; route contract ambiguity to B and scope change
to A. Otherwise report eligibility for a separately authorized Codex F only.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/857"
  tracker: "N/A"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill_issue_857.md"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main_requires_separate_owner_approval"
  branch: "not_created_or_moved_by_codex_d"
  internal_project_area: "Quality / Governance"
  truth_owner: "deterministic issue-wave state helper and current module contract"
  bridge_code_status: "shared_support"
  authority_notes:
    prerequisite_success_is_authority: false
    protected_surface_rollout_phase: "source correction only; not installed or dispatched"
    readiness_claimed: false
    security_assurance_claimed: false
    privacy_assurance_claimed: false
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "#826"
    lane_status: "active_second_lane_under_explicit_user_override"
    tracker_selected_next_lane: ""
    exception:
      name: "explicit_user_override"
      blocked_active_issue_or_pr: "#826"
      reason: "Correct the three current-main issue-wave findings before installation or real Dispatch."
      allowed_scope: "Exact ME-IW-855-E-009 through ME-IW-855-E-011 correction lifecycle only."
      expiration_condition: "Correction merge and issue closeout, explicit park/defer/cancel/reassignment, or owner revocation."
      authorized_by: "Human owner in the current task on 2026-08-13"
      recorded_in: "#857"
  freshness:
    current_branch: "main"
    intended_branch: "not created or moved by Codex D"
    upstream_branch: "origin/main@df64b8b879f62843b05cfdf41016aafa7428a96e"
    branch_ahead_behind: "local main 0 ahead, 25 behind"
    issue_state: "#857 open; #855 closed as completed"
    tracker_state: "N/A"
    source_artifact_status: "Codex B contract hash verified exact"
    target_artifact_status: "new unstaged D handoff"
    local_dirty_state: "pre-existing R0 modification and Wrangler residue preserved; B contract and D files unstaged; ignored validation bytecode retained under the no-cleanup constraint"
    untracked_artifacts:
      - "docs/contracts/mythic_edge_issue_wave_skill.md"
      - "docs/codex_skills/mythic-edge-issue-wave/"
      - "docs/implementation_handoffs/mythic_edge_issue_wave_skill_issue_857_fixer.md"
      - "tests/test_mythic_edge_issue_wave_skill.py"
      - "frontend/.wrangler/ (pre-existing, unrelated)"
    worktree_classification: "existing local main preserved; current origin/main tree independently verified"
    freshness_verdict: "eligible for fresh independent Codex E review only"
    recommended_route: "E"
    verified_at: "2026-08-13"
  validation:
    - "Correction regressions: 12 passed after red reproduction."
    - "Complete issue-wave suite: 171 passed."
    - "Complete installer suite: 46 passed, 3 Windows symlink-capability skips."
    - "Ruff and isolated compilation passed."
    - "Agent docs: 55 checked, 0 errors, 0 warnings."
    - "Changed-path protected-surface and secret-pattern gates: 4 paths, 0 forbidden, 0 warnings."
    - "Whitespace/error-marker diff checks against current origin/main bytes passed."
    - "Legacy Role Pool tree preserved at 950768b80b760a0e0dfe3040df023de20eadaf81 with 38 files."
    - "Official quick_validate unavailable because PyYAML is absent; no dependency change made."
  stop_conditions:
    - "Any contract or recovery-precedence ambiguity routes to B."
    - "Any required scope beyond the four D paths plus the unchanged Codex B contract routes to A."
    - "Any unauthorized, historical #855, legacy Role Pool, or R0-bound path change stops review."
    - "No installation, real Dispatch, GitHub write, submission, main-targeting, merge, deployment, cleanup, or readiness action."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "D"
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
    - "legacy Role Pool and R0-bound files (explicitly forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #857 and the exact Codex B contract authorize the two helper predicates and required tests without schema, reference, or scope expansion."
  stop_conditions:
    - "Any need to change the contract, state reference, or another package path."
    - "Any unrelated V2 behavior or public-safety rule change."
    - "Any legacy Role Pool, R0-bound, issue #826, #813, or #769 effect."
    - "Any operational or GitHub write outside a later separately approved role."
```
