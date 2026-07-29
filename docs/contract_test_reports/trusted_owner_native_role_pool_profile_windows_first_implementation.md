# Contract Test Report: Windows-First Trusted-Owner Native Role Pool Implementation

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/744

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/trusted_owner_native_role_pool_profile.md`

Reviewed contract SHA-256:
`2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322`

Review authority:

- [Agent constitution](../agent_constitution.md)
- [Contract-test role](../agent_threads/contract_test.md)
- [Contract-test report template](../templates/contract_test_report.md)

## Implementation Under Test

- Branch: `codex/trusted-owner-native-profile-contract-744`
- Starting commit: `0e58eacfe5f0530880c36adfc529c64f08525e79`
- Canonical source file count: `34`
- Canonical source byte count: `1,997,696`
- Canonical manifest byte count: `4,921`
- Canonical manifest SHA-256:
  `549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba`

The six contract-authorized canonical source paths are the only managed paths
that differ from the accepted migration rows. The two Core installer paths are
the only tracked implementation paths changed from the starting commit.

## Report Lifecycle

`report_lifecycle: final_approval`

## Contract Summary

The implementation must keep the trusted-owner native profile inert while
adding a Windows-first barrier. Before installer staging, destination creation,
claim publication, worktree or task creation, command execution, release
advancement, or another persistent effect, both the trusted Windows runtime
observation and the exact compatible `codex:native-task-create/v1` capability
must be established. Missing either input must fail closed with no fallback.

Read-only `--check` remains platform-neutral. Native macOS dispatch remains
deferred and nonblocking. No schema, digest family, terminal outcome,
installation, dispatch, canary, Stage-4, or readiness authority is added.

## Internal Project Area Reviewed

`Quality / Governance`

## Bridge-Code Status Reviewed

`bridge_code`

The repository-owned candidate remains inert and the installed skill remains
unchanged.

## Checks Run

```powershell
py -3.13 -B -m unittest discover -s docs\codex_skills\mythic-edge-role-pool\scripts -p test_check_pool_plan.py -v
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_install_codex_skills.py
py -3.13 -B -m pytest -q -p no:cacheprovider
py -3.13 -B -m ruff check src tests tools
py -3.13 -B -m ruff check docs\codex_skills\mythic-edge-role-pool\scripts\check_pool_plan.py docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py docs\codex_skills\mythic-edge-role-pool\scripts\test_skill_contract.py --select F,I
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B "%USERPROFILE%\.codex\skills\.system\skill-creator\scripts\quick_validate.py" docs\codex_skills\mythic-edge-role-pool
py -3.13 -B docs\codex_skills\mythic-edge-role-pool\scripts\test_skill_contract.py SkillContractTests.test_trusted_owner_native_profile_is_windows_first_and_inert -v
py -3.13 -B scripts\run_release_tests.py
py -3.13 -B tools\install_codex_skills.py --check --skill mythic-edge-role-pool
git diff --check
```

The installed offline gate was run from
`%USERPROFILE%\.codex\skills\mythic-edge-role-pool`. The initial review's
path-scoped scans covered the exact eight implementation paths. This follow-up
scanned the two fixer paths, the implementation handoff, and this report.

## Results

`approve`

The Windows-first validator, state-transition, terminal-selector, release-rung,
documentation, no-fallback behavior, and installer boundary are internally
consistent. The three narrow Codex D corrections close the implementation
preflight blocker, Git clean-filter byte-preservation blocker, and cached-diff
CR-at-EOL policy blocker.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-744-E-012` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | The initial review found that the installer checked only `_trusted_windows_host_observed()` even though the contract requires both trusted Windows host observation and exact native-task capability before installer staging or destination mutation. | Current bytes use `_role_pool_mutation_preflight_failure_reason()` at initial install, public sync, and internal sync boundaries. Seven focused tests prove each missing half blocks before mutation, only both injected synthetic observations permit temporary install/sync, and read-only `--check` observes neither predicate. | F after a separate owner submission decision |
| `ME-RP-744-F-001` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | Codex F found that the repository-wide LF clean filter would change two exact byte-bound candidate artifacts when written to the Git index. | Exact path-specific `-text` rules preserve both artifacts. Their accepted SHA-256 values and byte counts are unchanged, raw and filtered Git blob IDs match, all 34 candidate files have zero clean-filter mismatches, and the real index remains unstaged. | F |
| `ME-RP-744-F-002` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | After F-001, the two byte-bound artifacts staged byte-for-byte, but `git diff --cached --check` still classified their intentional CRLF carriage returns as trailing whitespace. | Both exact rules retain `-text` and add only `whitespace=cr-at-eol`. An isolated index containing all 42 submission paths produced zero candidate blob mismatches and `git diff --cached --check` exit `0` with zero output. The isolated index and lock were removed; the real index remains empty. | F |

## Historical Contract Mismatch And Fix Verification

### ME-RP-744-E-012: Installer mutation omits the native-task capability gate

**Intended behavior**

Before initial installation or synchronization can create staging or mutate a
destination, the trusted runtime must establish both:

1. `os.name == "nt"` and `sys.platform == "win32"`; and
2. the exact compatible `codex:native-task-create/v1` capability with the
   contracted request, one-task, receipt, timeout, unknown-outcome, no-retry,
   and no-fallback guarantees.

**Original actual behavior**

At the initial review, `tools/install_codex_skills.py` gated initial
installation, `_sync_action`, and `_synchronize_existing_skill` only with
`_trusted_windows_host_observed()`. It defined no capability observation or
combined preflight for these mutating paths.

**Original first proven failure point**

After action planning, the initial-install branch allowed destination creation
whenever the host predicate was true. The exact native-task capability was
never checked.

**Original counterexample**

`tests/test_install_codex_skills.py` monkeypatches only
`_trusted_windows_host_observed` to return true and then requires temporary
installation and synchronization to succeed. The test therefore confirms the
contract omission.

**Required fix**

In the same two files:

- add one fail-closed exact native-task capability predicate or combined
  installation preflight;
- require both host and capability before initial destination creation,
  synchronization staging, or replacement;
- keep the production capability false/unavailable until exact owning
  capability evidence exists;
- add focused cases proving host-true/capability-false blocks before mutation,
  capability-true/host-false blocks before mutation, and only both true permit
  temporary install/sync; and
- preserve platform-neutral `--check`, all existing rollback behavior, and all
  non-authority boundaries.

No contract, schema, canonical source, or additional implementation path is
needed.

**Current behavior and verification**

The current installer defines a fail-closed
`_exact_native_task_capability_observed()` that remains false until exact
owning capability evidence exists. `_role_pool_mutation_preflight_failure_reason()`
requires both the trusted Windows host and that capability. Initial Role Pool
installation checks the combined preflight before destination creation;
`_sync_action` checks it before staging; and `_synchronize_existing_skill`
repeats it before snapshots, staging, or replacement.

The seven focused Role Pool installer cases independently verify:

- capability true plus host false refuses before destination mutation;
- host true plus capability false refuses before destination mutation;
- both injected synthetic observations permit only temporary test install and
  synchronization;
- the internal sync helper cannot bypass the combined preflight; and
- read-only `--check` calls neither observer.

Current implementation SHA-256 values:

- `tools/install_codex_skills.py`:
  `7954d1c6b4cd816b4fb9d09be68a42ea89df9f6ffff20e13b76bab97e965dbda`
- `tests/test_install_codex_skills.py`:
  `8dae8aa4d4bf7338c5a586437ec75cabc8f9287d617144d980ae12a531115f00`

## Confirmed Contract Matches

- Runtime host identity comes from `os.name` and `sys.platform`, not packet
  input.
- The exact launcher identity remains `codex:native-task-create/v1`.
- Unsupported hosts and incompatible capability observations select
  priority-1 `blocked_request_or_packet_invalid` in the native preflight.
- Offline validation remains non-authorizing and platform-neutral.
- Remote Mac control does not alter the Windows execution host.
- Native Mac dispatch remains deferred and nonblocking.
- No broker, shell, `codex exec`, subprocess, repository executable, weaker
  receipt, or silent platform fallback was added.
- Schemas, digest families, field counts, and the 20 terminal outcomes remain
  unchanged.
- The production registry and release-state destinations remain absent.
- The installed skill was not modified or synchronized.
- Production native-task capability remains unavailable until exact owning
  evidence is separately reviewed and bound.
- Initial install, public sync, and internal sync all enforce the combined
  host-and-capability preflight before mutation.

## Validation Results

- Focused installer preflight: `7 passed`.
- Focused byte-preservation and cached-diff attribute regression: `1 passed`.
- Focused Role Pool: `92 passed`.
- Installer: `22 passed, 3 skipped` for unavailable directory symlinks.
- Full repository: `2094 passed, 4 skipped`; skips are the known unavailable
  symlink cases. One existing third-party Starlette deprecation warning
  remains.
- Exact changed documentation test: `1 passed`.
- Installed offline gate: `350 passed` plus structural validation and
  `NOT LIVE-READY`.
- Ruff, agent docs, source structural validation, path-scoped safety scans,
  process checks, residue checks, and `git diff --check`: passed.
- Read-only installer comparison: expected `target_differs` / `drift`; no
  synchronization occurred.
- Canonical source: `34` files, `1,997,696` bytes, `4,921` manifest bytes,
  SHA-256
  `549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba`.
- Isolated 42-path cached-diff check: exit `0`, output line count `0`, candidate
  staged-blob mismatch count `0`.
- Isolated review index and lock after cleanup: absent. Real index staged path
  count: `0`.
- Matching task process count: `0`.
- Generated residue count: `0`.

One exploratory `unittest discover` command used the over-broad
`test_*.py` pattern and therefore selected Stage-4 exception tests that require
the sibling repository-owned `mythic-edge-workflow` source, which is absent
from this inert candidate tree. It reported `144` setup errors across `376`
tests. This was a test-selection/setup error, not an implementation regression:
the contract-required `test_check_pool_plan.py` suite passed all `92` tests,
and the full repository suite passed all `2,094` runnable tests.

## Staged-Byte Preservation Confirmation

The current `.gitattributes` retains the repository-wide text policy and adds
only two exact exceptions:

- `references/external-isolation-broker-v5-corrective-successor.md`;
- `references/fallback-pickup-fixture/pickup.json`.

Each exact rule is `-text whitespace=cr-at-eol`. Git reports `text: unset` and
`whitespace: cr-at-eol` for both paths. Independent clean-filter simulation
with `git hash-object --path` produced the same blob identity as `git
hash-object --no-filters`:

- V5 successor: raw and filtered
  `ff8f963faffaaed5ccf5d4a1f8fd55e57463333a`;
- pickup fixture: raw and filtered
  `56d2c9e1f95d80bb1d837fd28059ba7d272865ce`.

The reviewed artifact bytes remain:

- V5 successor: `232,713` bytes, SHA-256
  `81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4`;
- pickup fixture: `1,567` bytes, SHA-256
  `1b11d1f74d379e8f6b75ea2ae921e1c4ac11685b5d5f11ada39c68e7df8d7a32`.

All `34` candidate files have identical raw and Git-filtered blob identities.
The canonical manifest remains
`549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba`.

For cached-diff confirmation, a disposable `GIT_INDEX_FILE` was initialized
from `HEAD` and populated with exactly the complete `42`-path submission set:
the `34` canonical Role Pool files plus the eight contract, report, installer,
test, handoff, and attribute paths. All `34` staged candidate blob identities
matched the reviewed working-tree bytes. `git diff --cached --check` exited
`0` with zero output. The disposable index and lock were removed afterward,
and the real index has zero staged files.

## Recommendation

Accept the exact inert Windows-first implementation candidate.
`ME-RP-744-E-012`, `ME-RP-744-F-001`, and `ME-RP-744-F-002` are
fixed-confirmed and no blocking implementation, staged-byte, or cached-diff
findings remain. Route the candidate back to Codex F. This review grants no
new submission authority; Codex F must verify the current owner submission
authority before staging.

Installation, registry population, claims, task/worktree creation, dispatch,
canaries, rung advancement, Stage 4, submission, merge, deployment, and live
use remain unauthorized by this review. Exact Windows native-task capability
evidence and a separate installation or synchronization decision are still
required before installer mutation.

## Next Workflow Action

Next role: Codex F, resuming only under current owner submission authority.

Pasteable next-thread prompt after owner authorization:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #744.

Submit only the independently reviewed inert Windows-first trusted-owner
native Role Pool candidate on branch
codex/trusted-owner-native-profile-contract-744. Read the contract at SHA-256
2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322,
the implementation handoff, and the final Codex E report. Confirm
ME-RP-744-E-012, ME-RP-744-F-001, and ME-RP-744-F-002 remain fixed. Recompute
the 34-file candidate manifest and require SHA-256
549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba.

Verify the current branch, base, issue, tracker, exact reviewed diff, and
validation before staging explicit reviewed paths. Recheck that all 34 staged
blob identities equal the reviewed working-tree bytes and that `git diff
--cached --check` passes with zero output over the complete 42-path staged
set. Open or update only a draft PR to the approved base. Do not install or
synchronize the skill, probe platform capability, populate registry or release
state, dispatch, publish a claim, run a canary, advance Stage 4, merge, deploy,
or claim live readiness.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/744"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  role_performed: "Codex E: Independent Windows-First Implementation and Staged-Byte Confirmation Reviewer"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md"
  target_artifact: "docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md"
  branch: "codex/trusted-owner-native-profile-contract-744"
  contract_sha256: "2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322"
  reviewed_manifest_sha256: "549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba"
  finding_status:
    ME-RP-744-E-012: "fixed_confirmed"
    ME-RP-744-F-001: "fixed_confirmed"
    ME-RP-744-F-002: "fixed_confirmed"
  implementation_verdict: "accepted_inert_windows_first_candidate"
  confirmed_scope_path_count: 8
  installer_fixer_scope_path_count: 2
  line_ending_fixer_scope_path_count: 2
  candidate_file_count: 34
  git_filter_mismatch_count: 0
  staged_blob_mismatch_count: 0
  cached_diff_check: "passed_zero_output_in_isolated_42_path_index"
  isolated_index_removed: true
  real_index_staged_path_count: 0
  affected_artifact_bytes_changed: false
  staged_files: []
  installed_skill_modified: false
  platform_capability_probed: false
  installation_or_sync_performed: false
  dispatch_authorized: false
  canary_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Codex F: resume exact reviewed submission lane under current owner authority"
  validation:
    - "focused byte-preservation and cached-diff attribute regression: 1 passed"
    - "focused installer preflight: 7 passed"
    - "installer: 22 passed, 3 skipped"
    - "canonical Role Pool: 92 passed"
    - "repository: 2094 passed, 4 skipped"
    - "isolated 42-path cached diff check: exit 0, zero output"
    - "installed offline gate: 350 passed; structural validation passed"
  stop_conditions:
    - "Do not treat this review as installation, sync, dispatch, canary, Stage 4, merge, deployment, or live authority."
    - "Codex F must verify current owner submission authority before staging."
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
  issue_or_tracker_read: false
  contract_or_handoff_read: true
  accepted_adrs_read: []
  protected_surfaces:
    - "installation and synchronization boundary"
    - "native task capability boundary"
    - "dispatch and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - "Review artifact is the only permitted edit."
    - "No installation, sync, capability probe, dispatch, canary, Stage 4, submission, merge, or deployment."
```
