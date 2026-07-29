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

- Pull request: https://github.com/Tahjali11/Mythic-Edge/pull/753
- Branch: `codex/trusted-owner-native-profile-contract-744`
- Starting commit: `0e58eacfe5f0530880c36adfc529c64f08525e79`
- Current PR head and local parent:
  `f45e5db1ea975c1cbe961c9727ea7f1367e9a9d6`
- Canonical source file count: `34`
- Canonical source byte count: `2,001,219`
- Canonical manifest byte count: `4,921`
- Canonical manifest SHA-256:
  `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`

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
consistent. The three earlier narrow Codex D corrections close the
implementation preflight blocker, Git clean-filter byte-preservation blocker,
and cached-diff CR-at-EOL policy blocker. The first no-echo correction removed
trusted-native validator details from CLI stderr. This second no-echo
correction removes the remaining shared validator-returned string sink while
preserving validation decisions and the seven fixed plan/result CLI binding
messages.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-744-E-012` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | The initial review found that the installer checked only `_trusted_windows_host_observed()` even though the contract requires both trusted Windows host observation and exact native-task capability before installer staging or destination mutation. | Current bytes use `_role_pool_mutation_preflight_failure_reason()` at initial install, public sync, and internal sync boundaries. Seven focused tests prove each missing half blocks before mutation, only both injected synthetic observations permit temporary install/sync, and read-only `--check` observes neither predicate. | F after a separate owner submission decision |
| `ME-RP-744-F-001` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | Codex F found that the repository-wide LF clean filter would change two exact byte-bound candidate artifacts when written to the Git index. | Exact path-specific `-text` rules preserve both artifacts. Their accepted SHA-256 values and byte counts are unchanged, raw and filtered Git blob IDs match, all 34 candidate files have zero clean-filter mismatches, and the real index remains unstaged. | F |
| `ME-RP-744-F-002` | P1 | `fixed_state_followup` | `fixed_confirmed` | not_blocking | After F-001, the two byte-bound artifacts staged byte-for-byte, but `git diff --cached --check` still classified their intentional CRLF carriage returns as trailing whitespace. | Both exact rules retain `-text` and add only `whitespace=cr-at-eol`. An isolated index containing all 42 submission paths produced zero candidate blob mismatches and `git diff --cached --check` exit `0` with zero output. The isolated index and lock were removed; the real index remains empty. | F |
| `codeql_alert_21` | high | `fixed_state_followup` | `second_local_fix_confirmed_ci_pending` | non_blocking | CodeQL first traced operator-supplied trusted-native validator detail to the generic stderr loop on PR head `5fed7873...ce6`. After the first local correction was published, CodeQL analyzed `f45e5db1...9d6` and still identified the shared validator-returned string sink. | The shared `for error in errors` stderr loop is now absent. A separate list contains exactly seven fixed CLI binding messages; validator-returned strings remain in memory for validation decisions but cannot enter that list. AST inspection found no `error` or `errors` value in a `print` call. Two focused regressions, three real subprocess probes, all 94 canonical tests, four adjacent command-line tests, and the full repository suite pass. Alert closure remains pending a successor commit and CodeQL rerun. | F, then GitHub CI; return to D only if the alert persists |

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
- Focused generic and trusted-native CLI no-echo regressions: `2 passed`.
- Actual generic fixed-guidance, generic withheld-detail, and trusted-native
  marker probes: exit `1`, exact expected stderr, marker absent, stdout empty.
- Static generic-stderr audit: exactly seven literal public diagnostics,
  no validator-error print site, and one bounded public-diagnostic print loop.
- Focused Role Pool: `94 passed`.
- Adjacent plan/result command-line gates: `4 passed`.
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
- Canonical source: `34` files, `2,001,219` bytes, `4,921` manifest bytes,
  SHA-256
  `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`.
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
the contract-required `test_check_pool_plan.py` suite passed all `92` tests at
that review point, now passes `93` with the new no-echo regression, and the
full repository suite passed all `2,094` runnable tests.

The first focused no-echo invocation used a dotted module path that omitted
the candidate script directory from `sys.path`; it failed during import before
running a test. The corrected direct-script invocation passed. This was a
review-command setup error, not candidate behavior.

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
At the F-002 confirmation point, the canonical manifest was
`549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba`.
The first reviewed no-echo source and test changes produced manifest
`00a4f44b08e6c528afea4058e06af0ac23d3a8e909ec6674216c06f98e2d3dab`.
The second reviewed no-echo correction retains the same 34-path inventory and
produces the current manifest
`6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`.

For cached-diff confirmation, a disposable `GIT_INDEX_FILE` was initialized
from `HEAD` and populated with exactly the complete `42`-path submission set:
the `34` canonical Role Pool files plus the eight contract, report, installer,
test, handoff, and attribute paths. All `34` staged candidate blob identities
matched the reviewed working-tree bytes. `git diff --cached --check` exited
`0` with zero output. The disposable index and lock were removed afterward,
and the real index has zero staged files.

## CodeQL Alert 21 First Local No-Echo Confirmation

This section preserves the first local correction and its then-current
evidence. GitHub later analyzed that correction at `f45e5db1...9d6` and kept
alert `21` open on the remaining shared generic sink. The next section records
the independent review of the second correction.

**Observed**

GitHub currently reports alert `21`,
`py/clear-text-logging-sensitive-data`, as open on PR head
`5fed78739ad7c54a099685cfd46f695e19f42ce6`. The three language analysis jobs
passed on that head, but the aggregate CodeQL check failed because the alert
was introduced there.

The source alert is real: the old generic CLI path passed the list returned by
`validate_trusted_native_document()` into `print(f"- {error}")`. Trusted-native
errors can derive from operator-supplied document content.

**Current behavior**

The local candidate adds one earlier CLI branch for schema versions beginning
with `trusted_owner_native_` or `trusted_owner_repository_`. It retains the
existing validator and its return values for in-process callers. On any CLI
validation error it now emits exactly:

```text
role-pool document invalid:
- validation details withheld
```

and exits `1`. The generic diagnostic loop remains unchanged for plan and
result schemas, preserving their fixed sidecar and binding guidance.

An independent actual-process probe supplied a private marker in an invalid
trusted-native document. The command returned the exact fixed message, emitted
no stdout, and did not expose the marker. The focused regression also forces a
tainted validator return value and proves it cannot reach stderr.

**Bindings**

- Historical reviewed manifest:
  `549a7157282401ba39898c187aa2d6a21aed0e9e01e5691597961faca1c2c4ba`.
- Prospective accepted local manifest:
  `00a4f44b08e6c528afea4058e06af0ac23d3a8e909ec6674216c06f98e2d3dab`.
- `check_pool_plan.py` SHA-256:
  `bbc5b7e1999a2f0b14e2cc35eb2e43fdbe0d38c3a75618f6f5be05c368306fc6`.
- `test_check_pool_plan.py` SHA-256:
  `c7346aa5ae5634ac40aaab541eca58ad75803b4852452dd72ae76e81d4d3edc2`.

The local source fix is independently confirmed. GitHub CodeQL closure is not
yet confirmed because the local bytes have not been committed or pushed.

## CodeQL Alert 21 Generic-Stderr Completion Confirmation

**Observed**

GitHub currently reports alert `21`,
`py/clear-text-logging-sensitive-data`, as open on PR head
`f45e5db1ea975c1cbe961c9727ea7f1367e9a9d6`. The latest Python analysis points
to the shared validator-error stderr sink. The three language analysis jobs
and both repository test jobs pass, while the aggregate CodeQL check fails
because the alert remains open.

The current local diff removes that sink. Validator-returned strings still
determine validation success or failure, but none is printed. A separate
`public_diagnostics` list is populated only by seven source literals for
missing CLI sidecars or bindings. If that list is empty, the CLI emits only
`validation details withheld`.

**Independent verification**

- AST inspection found exactly seven literal assignments to `diagnostic`, in
  the contract-preserving order, and no `print` call that references `error`
  or `errors`.
- A real invalid plan containing an invented private marker emitted only the
  fixed missing-`--discovery` message.
- The same invalid plan with a valid discovery sidecar emitted only
  `validation details withheld`.
- A real invalid trusted-native request retained the same withheld-detail
  behavior.
- All three subprocess probes returned exit `1`, emitted no stdout, and did
  not expose their markers.
- The two focused no-echo regressions, four adjacent CLI gate tests, all `94`
  canonical Role Pool tests, and the full `2,094`-test repository suite pass.

**Bindings**

- Published predecessor commit:
  `f45e5db1ea975c1cbe961c9727ea7f1367e9a9d6`.
- Published predecessor manifest:
  `00a4f44b08e6c528afea4058e06af0ac23d3a8e909ec6674216c06f98e2d3dab`.
- Prospective candidate manifest:
  `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`.
- `check_pool_plan.py` SHA-256:
  `cd85d9a33fbd92d8b29d8ec092a03492d7e05915a973796c5218a6eaf903fae0`.
- `test_check_pool_plan.py` SHA-256:
  `8ca31a9276d5bb092686010968dce8d7e98715a15d4a581616ec60c06a2b4243`.

The second local source correction is independently confirmed. It is not yet
GitHub-confirmed: alert `21` remains open against the predecessor commit until
Codex F publishes these reviewed bytes and CodeQL analyzes the successor.

## Recommendation

Accept the exact inert Windows-first implementation candidate.
`ME-RP-744-E-012`, `ME-RP-744-F-001`, and `ME-RP-744-F-002` are
fixed-confirmed. The second source correction for `codeql_alert_21` is locally
confirmed, with CI closure pending. No blocking implementation, staged-byte,
cached-diff, or local no-echo finding remains. Route exactly the four reviewed
local paths back to Codex F for a successor commit and PR push. Codex F must
verify current owner submission authority before staging.

Do not call alert `21` fixed or the PR merge-ready until CodeQL analyzes the
successor commit and the aggregate CodeQL check passes. If the alert remains,
route its new exact evidence back to Codex D. If it closes, route the draft PR
to Codex G only after a separate owner integration request.

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
ME-RP-744-E-012, ME-RP-744-F-001, and ME-RP-744-F-002 remain fixed and that
the second local source correction for CodeQL alert 21 is accepted by this
report. Recompute the 34-file candidate manifest and require SHA-256
6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175.

Verify the current branch, base, issue, tracker, exact reviewed diff, and
validation. Stage only:
- docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py
- docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py
- docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md
- docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md

Commit and push those exact reviewed paths to update existing draft PR #753.
Then require the successor CodeQL analysis and aggregate CodeQL check to pass
and verify alert 21 no longer applies to the successor head. Do not dismiss the
alert. Do not install or synchronize the skill, probe platform capability,
populate registry or release state, dispatch, publish a claim, run a canary,
advance Stage 4, merge, deploy, or claim live readiness.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/744"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  role_performed: "Codex E: Independent CodeQL Alert 21 Generic-Stderr Confirmation Reviewer"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md"
  target_artifact: "docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md"
  branch: "codex/trusted-owner-native-profile-contract-744"
  contract_sha256: "2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322"
  predecessor_commit: "f45e5db1ea975c1cbe961c9727ea7f1367e9a9d6"
  prior_reviewed_manifest_sha256: "00a4f44b08e6c528afea4058e06af0ac23d3a8e909ec6674216c06f98e2d3dab"
  reviewed_manifest_sha256: "6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175"
  finding_status:
    ME-RP-744-E-012: "fixed_confirmed"
    ME-RP-744-F-001: "fixed_confirmed"
    ME-RP-744-F-002: "fixed_confirmed"
    codeql_alert_21: "second_local_fix_confirmed_ci_pending"
  implementation_verdict: "accepted_generic_stderr_no_echo_fix_pending_successor_codeql"
  confirmed_scope_path_count: 8
  installer_fixer_scope_path_count: 2
  line_ending_fixer_scope_path_count: 2
  no_echo_fixer_scope_path_count: 3
  e_reviewed_local_path_count: 4
  candidate_file_count: 34
  git_filter_mismatch_count: 0
  staged_blob_mismatch_count: 0
  cached_diff_check: "passed_zero_output_in_isolated_42_path_index"
  isolated_index_removed: true
  real_index_staged_path_count: 0
  affected_artifact_bytes_changed: false
  staged_files: []
  installed_skill_modified: false
  codeql_alert_state_on_current_pr_head: "open_on_f45e5db1ea975c1cbe961c9727ea7f1367e9a9d6"
  codeql_ci_confirmation: "pending_successor_commit_and_ci_rerun"
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
    - "focused generic and trusted-native CLI no-echo regressions: 2 passed"
    - "three actual CLI marker probes: passed"
    - "static generic-stderr audit: seven literals; no validator-error print site"
    - "canonical Role Pool: 94 passed"
    - "adjacent plan/result command-line gates: 4 passed"
    - "repository: 2094 passed, 4 skipped"
    - "isolated 42-path cached diff check: exit 0, zero output"
    - "installed offline gate: 350 passed; structural validation passed"
  stop_conditions:
    - "Do not treat this review as installation, sync, dispatch, canary, Stage 4, merge, deployment, or live authority."
    - "Codex F must verify current owner submission authority before staging."
    - "Do not mark CodeQL alert 21 fixed until the successor commit is analyzed and the aggregate CodeQL check passes."
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
    - "ADR-0008"
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
