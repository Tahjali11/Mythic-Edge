# App-Native R0 Validation-Command Scope Correction Contract

## Contract Status

| Field | Value |
|---|---|
| Repository | `Tahjali11/Mythic-Edge` |
| Issue | <https://github.com/Tahjali11/Mythic-Edge/issues/819> |
| Tracker | <https://github.com/Tahjali11/Mythic-Edge/issues/746> |
| Protected issue | <https://github.com/Tahjali11/Mythic-Edge/issues/769> |
| Merged package PR | <https://github.com/Tahjali11/Mythic-Edge/pull/824> |
| Reviewed main commit | `f29266eabecb82bd07f5b20f86442237427c55f0` |
| Reviewed main tree | `e21863c8990f8837fba9582366a2f2c5e367c14f` |
| Source finding | `ME-RP-819-E-010` |
| Review thread | <https://github.com/Tahjali11/Mythic-Edge/pull/824#discussion_r3742868092> |
| Risk | High governance validation; docs-only command ownership correction |

This additive successor corrects one internally unsatisfied validation rule in
the integrated #819 contracts. It does not rewrite either accepted contract or
change any release, index, handoff, validator, test, lifecycle, or authority
byte.

The current owner-provided handoff activates this one Codex B contract-writing
lane under issue #819. That authority expires with the Codex B handoff and does
not authorize implementation, GitHub mutation, lifecycle closeout, or any
operational action.

## Governing Sources

- `AGENTS.md`;
- `docs/agent_rules.yml`;
- `docs/agent_constitution.md`;
- `docs/codex_module_workflow.md`;
- `docs/agent_threads/module_contract.md`;
- `docs/templates/module_contract.md`;
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`;
- issue #819 and tracker #746;
- the exact integrated contracts and package below; and
- the unresolved PR #824 review thread.

Issue #819 remains the active lane. Issue #769 must remain open with zero
comments and is not a writable surface.

## Finding And First Failure

`ME-RP-819-E-010` is the only finding owned by this contract.

Observed:

1. The index-correction contract requires
   `py -3.13 -B tools\check_secret_patterns.py --all`.
2. Its acceptance language requires protected/private scans to report zero
   forbidden findings and zero warnings.
3. The completion contract repeats the same repository-wide secret command.
4. On reviewed main, the repository-wide command reports `480 forbidden` and
   `912 warnings`, so the command cannot satisfy the zero-result acceptance
   rule.
5. The five integrated #819 package paths scanned explicitly report
   `0 forbidden` and `0 warnings`.
6. No implementation defect, release defect, index defect, or handoff defect
   was found.

Derived:

- The repository-wide command and package-local acceptance criterion have
  different ownership scopes.
- A repository-wide cleanup or accepted global baseline is not required to
  assess the exact #819 package.
- The smallest correction is to make the exact package-path scan normative for
  #819 and retain the repository-wide scan as advisory evidence only.

## Owning Layer And Nonclaim

- Internal project area: Role Pool governance and R0 release evidence.
- Truth owner: the accepted contracts own their package validation commands;
  the secret/private-marker checker owns deterministic scan output.
- Bridge-code status: `not_bridge_code`.
- This contract changes validation ownership only.
- It does not suppress, resolve, accept, or waive any repository-wide finding.
- It does not claim that the repository as a whole is free of secret or private
  markers.

## Frozen Integrated Package

The following five paths and SHA-256 values are immutable read-only inputs:

| Ordinal | Path | SHA-256 |
|---:|---|---|
| 1 | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` | `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2` |
| 2 | `docs/role_pool_current_authority_index.md` | `a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9` |
| 3 | `docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md` | `03634091fc3e544d4850ce1da65001106d3c450d96d4dd779a91b65cbbfb66e5` |
| 4 | `docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md` | `150e204ed7b22d1145bdc15f3695f87a7269900db554b656c5380ccfcd70702e` |
| 5 | `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md` | `7ea5aff745d92f959fc9147dd1c4f81dd20bd62989d36e6066c94f611bb11bd6` |

These paths must not be edited, regenerated, normalized, or rebound under this
contract. The release remains a valid exact two-record R0 chain with current
tip `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91`
and zero observation receipts.

## Exact Validation Ownership Correction

This contract supersedes only these two command requirements:

1. line 342 of the integrated index-correction contract; and
2. line 443 of the integrated handoff-completion contract.

In both places, the exact command:

```powershell
py -3.13 -B tools\check_secret_patterns.py --all
```

is replaced for #819 package acceptance by an exact path-fed scan of the five
frozen package paths:

```powershell
@(
  'docs/role_pool/trusted_owner_native_release_state.v1.jsonl'
  'docs/role_pool_current_authority_index.md'
  'docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md'
  'docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md'
  'docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md'
) | py -3.13 -B tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

The existing acceptance phrase requiring zero forbidden findings and zero
warnings remains unchanged in substance. Under this successor, it applies to
the exact five-path package scan above, not to unrelated tracked repository
history.

All other commands and acceptance criteria in both integrated contracts remain
unchanged.

## Successor-Contract Scan

This new contract is not one of the historical five package paths. It must be
scanned independently before review or integration:

```powershell
'docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md' |
  py -3.13 -B tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

It must report `0 forbidden` and `0 warnings`. The protected-surface checker
must scan the same successor path explicitly and report the same zero result.

This separate scan prevents the correction contract from escaping the gate
without relabeling the historical five-path package.

## Repository-Wide Advisory Scan

`py -3.13 -B tools\check_secret_patterns.py --all` remains available as a
repository-wide advisory measurement. For the reviewed main snapshot it
reported:

```text
forbidden: 480
warnings: 912
result: failed
```

Those counts are observed snapshot evidence, not an accepted baseline, waiver,
or immutable known-answer vector. They may drift as unrelated repository work
changes. If the advisory command is run, its exact output must be reported
truthfully, but it does not determine #819 package acceptance or lifecycle
closeout.

Any future effort to classify, baseline, suppress, or remediate those
repository-wide findings requires separate issue ownership and contract scope.
This contract authorizes none of that work.

## Preserved Validation

The following integrated evidence remains required and unchanged:

- bootstrap and offline-observation tests: `270 passed`;
- trusted-launch-observer tests: `74 passed`;
- release-focused tests: `8 passed`;
- agent docs: zero errors and zero warnings;
- exact five-path protected-surface scan: zero forbidden and zero warnings;
- exact five-path secret/private-marker scan: zero forbidden and zero warnings;
- exact successor-contract protected and private scans: zero/zero;
- `git diff --check`: passed;
- matching operational process count: zero;
- task-generated residue count: zero;
- issue #769: open with zero comments; and
- all release, observation, task, claim, dispatch, R1-R8, retired legacy
  Stage 4, submission, merge, deployment, assurance, and readiness authority
  flags: false.

The isolated temporary-directory reproduction for the trusted-launch observer
is valid evidence for its 74-test result. The pre-existing ACL-protected pytest
temporary directory, ignored caches, and `frontend/.wrangler/` are not owned by
this contract and must remain untouched.

## Exact Scope And Side Effects

Codex B creates exactly one path:

`docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md`

There is no later Codex C implementation scope. Contract acceptance routes to
Codex F/G for normal docs-only integration only after fresh Codex E review and
explicit submission or merge authority.

This contract does not authorize:

- edits to either predecessor contract;
- edits to the release, index, handoff, validators, tests, or checker;
- repository-wide secret remediation or baseline adoption;
- resolution of the PR #824 thread before this successor is integrated and
  independently confirmed on current main;
- issue #819 closure or Project-field mutation by Codex B or E;
- issue #769 mutation;
- task, claim, dispatch, observation, process, release, registry, installed
  skill, R0-R8, retired legacy Stage 4, submission, merge, deployment, or
  readiness operations.

## Lifecycle Route

1. Codex B writes this one docs-only successor.
2. Fresh Codex E independently verifies the exact bytes and both scan scopes.
3. If accepted, Codex F may submit only this reviewed contract under separate
   submission authority.
4. Codex G may integrate only under separate explicit merge authority.
5. Fresh Codex E rechecks current main, the exact five frozen package paths,
   this integrated successor, and the unresolved PR thread.
6. Only after that review may Codex G resolve the PR thread and consider issue
   #819 lifecycle closeout under separate owner authority.

No step grants observation or rung-advancement authority.

## Contract Validation

```powershell
py -3.13 -B tools\check_agent_docs.py
'docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md' |
  py -3.13 -B tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
'docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md' |
  py -3.13 -B tools\check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --check
```

Codex E must additionally reproduce the exact five-path private-marker scan.
It may reproduce the repository-wide advisory scan, but its nonzero result is
not a #819 rejection after this successor.

## Acceptance Criteria

- `ME-RP-819-E-010` is closed only at the contract level.
- The two exact `--all` requirements are superseded and no third active
  occurrence owns #819 acceptance.
- The exact five frozen package paths remain byte-identical.
- Both exact five-path package scans report zero forbidden and zero warnings.
- This successor's exact path scans report zero forbidden and zero warnings.
- Repository-wide findings remain reported and unwaived.
- No package, implementation, test, validator, schema, lifecycle, or authority
  byte changes.
- No generated residue or matching operational process.
- Fresh independent Codex E acceptance precedes submission.

## Stop Conditions

Stop if:

- any frozen path or digest differs;
- another active #819 contract makes repository-wide zero findings a distinct
  substantive eligibility requirement;
- a package path fails either path-scoped scan;
- correcting the mismatch requires checker, test, contract-history, release,
  index, or handoff edits;
- repository-wide findings would need suppression or waiver;
- issue #769 changes state or gains a comment; or
- operational, observation, submission, merge, or closeout authority is
  requested in this lane.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent #819 Validation-Command Scope Correction Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/819
PR review thread: https://github.com/Tahjali11/Mythic-Edge/pull/824#discussion_r3742868092
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md

Use the exact SHA-256 from the Codex B handoff. Verify ME-RP-819-E-010 is
closed only by superseding the two integrated `check_secret_patterns.py --all`
requirements with the exact five-path package scan. Confirm the five frozen
package hashes, reproduce their private-marker and protected-surface results at
0/0, and separately scan the successor contract at 0/0.

Confirm the repository-wide 480/912 snapshot remains truthful advisory evidence
and is neither an accepted baseline nor a waiver. Confirm no implementation,
test, validator, release, index, handoff, schema, lifecycle, authority, issue,
or GitHub mutation is authorized. Do not edit files, resolve the PR thread,
close #819, touch #769, run an observation, submit, merge, deploy, advance
R0-R8 or retired legacy Stage 4, or claim readiness.

If exact, route this single contract to Codex F under separate submission
authority, then Codex G integration, then fresh current-main Codex E lifecycle
review.
```

## Instruction Context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high_governance_validation"
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
    - "validation ownership"
    - "release-state evidence"
    - "issue and PR lifecycle"
    - "issue #769 zero-comment state"
    - "R0-R8 and retired legacy Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "Package-local zero findings and repository-wide advisory findings have different owners; no waiver or remediation is created."
  stop_conditions:
    - "any frozen package byte changes"
    - "any second contract or implementation path is required"
    - "repository-wide findings would be waived"
    - "operational or lifecycle mutation authority is requested"
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/819"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_validation_command_scope_correction.md"
  risk_tier: "high_governance_validation"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-r0-validation-scope-correction-819"
  source_finding: "ME-RP-819-E-010"
  contract_verdict: "ready_for_independent_review"
  normative_package_scan: "exact_five_paths_zero_forbidden_zero_warnings"
  repository_wide_scan: "advisory_unwaived_nonblocking_for_819"
  implementation_scope_count: 0
  implementation_authorized: false
  observation_authorized: false
  r0_r8_authorized: false
  retired_legacy_stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  lifecycle_closeout_authorized: false
  live_ready: false
  validation:
    - "agent docs and exact successor-path safety scans required"
    - "exact five-path package scans required"
  stop_conditions:
    - "frozen package drift"
    - "package-local scan failure"
    - "repository-wide waiver or remediation required"
    - "scope expands beyond this one contract"
```
