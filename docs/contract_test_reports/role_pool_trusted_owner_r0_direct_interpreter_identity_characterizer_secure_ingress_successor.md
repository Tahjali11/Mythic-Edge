# R0 Identity Characterizer Secure-Ingress Successor Contract Review

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/795>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/746>

## Contract

[`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md`](../contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md)

Reviewed SHA-256:
`246f50d84245e4c7512bcabeee3108941a1f3e4d3c391e40d1e9c8930cc115d9`
(`35181` bytes).

## Implementation Under Test

Contract-only review on branch
`codex/r0-identity-characterizer-secure-ingress-contract-795` at
`4a126a9f0ccb9234f08f5d706dbba49f31a3c176`. No implementation exists or was
reviewed.

## Report Lifecycle

`report_lifecycle: initial_contract_test`

## Contract Summary

The proposed successor adds one future repository-owned controller and one
operation-free test. The controller is intended to run under the exact bound
private CPython image, prove an inherited no-echo Windows console before
authority consumption, accept one private line after durable consumption, and
invoke the unchanged identity characterizer once in-process. It must not add a
launcher, helper, shell fallback, process lane, schema, authority, retry, or
operational permission.

## Internal Project Area Reviewed

Role Pool trusted-owner R0 local execution boundary. The review remained
contract-only and did not access the private interpreter path or execute a
process.

## Bridge-Code Status Reviewed

The proposed controller is prospective bridge code between an owner-controlled
terminal and the accepted characterizer. It is not yet eligible for
implementation because its own launch ingress is not closed.

## Checks Run

```powershell
git diff --check
git diff --no-index --check -- NUL docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md
py -B tools/check_agent_docs.py
'docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md' | py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
'docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md' | py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py -q -p no:cacheprovider
```

## Contract Clarification Re-review

`report_lifecycle: contract_clarification_review`

Reviewed successor SHA-256:
`436811c649bc57d74c995dd3e9a1398d01d37e880b45a3a8624c0bc9ca41162d`
(`44416` bytes).

### Re-review Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ME-RP-795-INGRESS-E-001 | High | fixed_state_followup | fixed_confirmed_contract_only | not_blocking | The predecessor defined no permitted private `lpApplicationName` ingress before the controller existed. | The successor adds one repository-owned PowerShell bootstrap that runs in the pre-existing terminal process, reads the launch image with `[Console]::ReadKey($true)` only after durable consumption, places it only in `ProcessStartInfo.FileName`, and starts exactly one controller. The third future path and dependent topology/test language are explicit; no private argument, environment value, helper process, retry, or new execution lane was added. | none |
| ME-RP-795-INGRESS-E-002 | High | remaining_blocker | current_windows_powershell_argument_list_capability_absent | blocking | The successor requires `ProcessStartInfo.ArgumentList` as the sole public argument transport and requires Codex E to confirm that capability before acceptance. | The current and only available host reports Windows PowerShell `5.1.19041.6456`, `PSEdition=Desktop`, and `[Diagnostics.ProcessStartInfo].GetProperty('ArgumentList') = null`; `pwsh.exe` is absent. `Console.KeyAvailable` and `Console.ReadKey(Boolean)` are available. A conforming implementation therefore must stop before consumption and cannot launch the controller on this host. | B |

### Re-review Results

- The revised contract hash and byte count are exact. The predecessor review
  remains byte-exact at
  `1759abe1563a8bab26c398e9c6148a08a901055c377516be58fb88cc092dc973`
  (`12039` bytes).
- Every current repository artifact, PR #797 binding, and historical issue
  #795 binding remains exact. Issues #795, #780, and #746 remain open; issue
  #769 remains open with zero comments; PR #797 remains merged with six passing
  checks; open PRs #374 and #391 are unrelated.
- The corrected ADR-0010 link resolves to the actual proposed,
  non-precedential ADR.
- The three future implementation paths are absent. No implementation,
  private-path access, authority consumption, process launch, GitHub write, or
  external-state mutation occurred.
- Microsoft documents that `Console.ReadKey(true)` suppresses display of the
  pressed key. That closes the original no-echo ingress design issue.
- Microsoft documents `ProcessStartInfo.ArgumentList` as a collection-based
  API and `ProcessStartInfo.Arguments` as the single-string alternative. The
  current Windows PowerShell runtime exposes only the latter.
- `187` focused operation-free tests passed. Agent docs, whitespace,
  protected-surface, private-marker, process, and generated-residue checks
  passed.

### Re-review Recommendation

`request contract clarification`

The smallest correction is limited to the public controller argument
construction. Codex B should replace the unavailable `ArgumentList`
requirement with one exact Windows PowerShell 5.1-compatible `Arguments`
string built only from fixed flags, the fixed relative controller path, and
strictly validated public characterization/decision tokens. The private launch
image must remain solely in `ProcessStartInfo.FileName`. Mechanically dependent
readiness, tests, and acceptance wording may change; process topology, the
three-file scope, schemas, characterizer behavior, private ingress, authority,
and execution boundaries must not.

```yaml
workflow_handoff:
  role_performed: "Codex E: Independent R0 Identity Characterizer Secure-Ingress Successor Contract Re-reviewer"
  reviewed_sha256: "436811c649bc57d74c995dd3e9a1398d01d37e880b45a3a8624c0bc9ca41162d"
  finding_status:
    ME-RP-795-INGRESS-A-001: "contract_correction_partially_confirmed"
    ME-RP-795-INGRESS-E-001: "fixed_confirmed_contract_only"
    ME-RP-795-INGRESS-E-002: "open_blocking_current_host_api_mismatch"
  implementation_authorized: false
  execution_authorized: false
  preflight_authorized: false
  observation_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Codex B: narrow Windows PowerShell 5.1 public-argument transport corrector"
```

The review also recomputed every frozen artifact digest and byte count,
re-read the exact PR #797 review and historical issue #795 comment, reconciled
open issues and pull requests, checked both future implementation paths were
absent, and ran read-only process and generated-residue checks.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: the controller's post-start `getwch` design is
  bounded and no-echo, but the pre-controller executable-path ingress is not
  defined.
- Vocabulary coherence: the existing 33-field result, 18 false authorities,
  nine terminal phases, target command, and historical nonreuse remain
  unchanged.
- Authority semantics: implementation, execution, consumption, Observation 1,
  R1-R8, Stage 4, deployment, and readiness remain false.
- Fail-closed behavior: the proposed controller stops before consumption when
  its runtime or console checks fail.
- Protected-surface rollout: only a contract exists; no private path,
  implementation, process, GitHub mutation, registry, installed state, or
  release state was accessed or changed.

## Results

The exact contract and all deterministic validation gates passed. The contract
is not accepted because the first required secure launch cannot be performed
from the defined topology without an ingress mechanism that the contract
either prohibits or leaves undocumented.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ME-RP-795-INGRESS-E-001 | High | remaining_blocker | direct_launch_private_runtime_ingress_undefined | blocking | The contract requires `lpApplicationName` to equal the privately held exact `python.exe`, while prohibiting that path in arguments, environment, files, clipboard, history, logs, and durable output and prohibiting a launcher, helper, shell fallback, or undocumented Codex capability. | The owner-operated controller does not exist until after this launch. The contract defines no pre-controller no-echo transfer or already-held launch primitive by which the terminal host obtains and passes the exact private application name. Entering the path in a shell exposes or persists it; adding a parent reader/native launcher adds an uncontracted capability outside the exact two-file scope. | B |

## Confirmed Contract Matches

- The contract is an ordinary non-reparse file at the exact required hash and
  byte count.
- Every frozen repository artifact, PR review body, and historical issue
  comment recomputed to the contract's stated digest and byte count.
- PR #797 is merged at the exact base commit with all six checks passing;
  issues #795, #780, and #746 remain open; issue #769 remains open with zero
  comments; open PRs #374 and #391 are unrelated.
- The future scope is exactly two currently absent new files. Existing
  characterizer bytes, test bytes, schemas, categories, target behavior, and
  authority fields remain frozen.
- The post-start console reader uses documented no-echo character input and
  keeps the private line out of controller arguments, environment, files,
  clipboard, registry, and durable output.
- The historical characterization remains consumed and nonreusable.
- `187` focused operation-free tests passed. Agent docs, protected-surface,
  private-marker, whitespace, process, and residue checks passed.

## Contract Mismatches

- **ME-RP-795-INGRESS-E-001:** `Exact Controller Runtime And Direct Launch`,
  `Acceptance And Validation`, and the embedded next-review prompt require an
  exact direct launch with no launcher, helper, shell, or undocumented input
  capability. The contract never defines how the pre-existing terminal host
  receives the private `lpApplicationName` without exposing it or adding one
  of those forbidden mechanisms. The smallest coherent correction is for
  Codex B to define one explicit, owner-controlled, no-echo pre-controller
  launch-ingress primitive and account for it in the process/capability scope,
  or to choose a controller runtime whose invocation does not itself require
  the private binding. No implementation change is authorized.

The contract also links to
`docs/decisions/ADR-0010-trusted-owner-local-execution-boundary.md`, which is
absent; the existing ADR-0010 has a different basename. This is nonblocking in
this review because the contract explicitly treats ADR-0010 as proposed and
non-precedential and derives no authority from it. It should be corrected with
the blocking contract revision without opening a separate lane.

## Missing Tests

No currently required operation-free test is missing. The future tests cannot
close ME-RP-795-INGRESS-E-001 because the missing behavior is outside the
controller that those tests would exercise.

Exact-byte external capture of successful controller stdout remains a future
execution-transport risk. It is not opened as a second blocker in this review;
the launch boundary fails first and the contract assigns public-safe capture
to a separately authorized execution role.

## Drift Notes

No repository, issue, PR, process, or generated-residue drift was found. The
absent ADR link is documentation-lineage drift only. The blocking issue is a
contract closure gap, not implementation or environment drift.

## Recommendation

`request contract clarification`

## Next Workflow Action

Next role: Codex B, limited to the exact pre-controller launch-ingress clause
and mechanically dependent topology, acceptance, and test language.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex B: Narrow R0 Secure-Ingress Pre-Controller Launch Closure
Corrector.

Review only ME-RP-795-INGRESS-E-001 in
docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md
at predecessor SHA-256
246f50d84245e4c7512bcabeee3108941a1f3e4d3c391e40d1e9c8930cc115d9.

Define exactly one explicit owner-controlled, no-echo mechanism by which the
pre-existing terminal host obtains and supplies the private bound
lpApplicationName before the controller exists. Reconcile only mechanically
dependent process topology, capability, no-echo, acceptance, and operation-free
test language. The mechanism must not place the private path in argv,
environment, files, clipboard, history, logs, comments, handoffs, or durable
output, and it must not smuggle in an undocumented launcher or Codex input
capability. If the existing exact-two-file implementation scope cannot contain
the truthful mechanism, state that explicitly rather than hiding the parent
boundary.

Preserve the accepted characterizer bytes, 33-field result, 18 false
authorities, nine terminal phases, one target-process limit, zero descendants,
historical nonreuse, and all false operational authority. Correct the broken
non-precedential ADR-0010 link in the same docs-only revision. Do not implement,
execute, access the private path, consume authority, or expand into preflight,
Observation 1, R1-R8, Stage 4, deployment, or readiness.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/795"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "B"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md"
  target_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/r0-identity-characterizer-secure-ingress-contract-795"
  validation:
    - "contract SHA-256 and 35181-byte count exact"
    - "all frozen repository and GitHub bindings exact"
    - "187 focused operation-free tests passed"
    - "agent-doc and path-scoped safety gates passed"
    - "matching process count 0; generated residue count 0"
  stop_conditions:
    - "any scope beyond the pre-controller launch-ingress closure"
    - "any private-path access or durable private value"
    - "any implementation, execution, consumption, observation, or stage authority"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md"
  protected_surfaces:
    - "private direct-interpreter path and runtime identity"
    - "single-use authority consumption and historical nonreuse"
    - "controller and target process topology"
    - "issue #769 zero-comment boundary"
    - "R0, Observation 1, R1-R8, Stage 4, and readiness authority"
  authority_conflicts_found: true
  authority_conflict_notes: "The controller must be launched through a private runtime path before the controller's no-echo reader exists, but the contract defines no permitted pre-controller ingress capability."
  stop_conditions:
    - "Any implementation or execution"
    - "Any private-path access"
    - "Any schema, algorithm, target-process, or authority expansion"
```

## Final Windows PowerShell 5.1 Transport Confirmation

`report_lifecycle: final_approval`

Reviewed successor SHA-256:
`7c7d5cd414b8a893703b014d470b84800b3444a11fe498135a7dd965adeacb69`
(`47461` bytes).

### Final Finding Dispositions

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- |
| ME-RP-795-INGRESS-A-001 | High | fixed_state_followup | fixed_confirmed_contract_only | not_blocking | The accepted contract now defines both the pre-controller no-echo launch ingress and the controller's later no-echo target ingress without changing the accepted characterizer. | none |
| ME-RP-795-INGRESS-E-001 | High | fixed_state_followup | fixed_confirmed_contract_only | not_blocking | The repository-owned bootstrap executes in the existing terminal host, keeps the private launch image only in `ProcessStartInfo.FileName`, and creates exactly the one controller process after durable consumption. | none |
| ME-RP-795-INGRESS-E-002 | High | fixed_state_followup | fixed_confirmed_contract_only | not_blocking | On Windows PowerShell `5.1.19041.6456` Desktop, `ProcessStartInfo.Arguments` is present and exact assignment/readback succeeds while `ArgumentList` remains absent. The seven-token maximum vector is ASCII, contains six single spaces, is `301` UTF-8 bytes, matches both closed regexes, and remains below the `512`-byte ceiling. Negative uppercase, short, whitespace, option, zero-ID, and overlength witnesses all reject. No process was started. | none |

### Final Validation

- The source review remained exact at
  `f6d81ea9af445802c1132488f04ce54aaceb503e80bee826d222471b9e0dd760`
  (`16533` bytes) before this final update.
- Every frozen current repository artifact remains ordinary, non-reparse, and
  exact. PR #797 remains merged with six successful checks; issues #795,
  #780, and #746 remain open; issue #769 remains open with zero comments; open
  PRs #374 and #391 remain unrelated.
- The three future implementation paths remain absent. The existing
  characterizer, 33-field result, 18 all-false authorities, nine terminal
  phases, one-target/zero-descendant behavior, and historical nonreuse remain
  unchanged.
- `187` focused operation-free tests passed. Agent docs, whitespace,
  protected-surface, private-marker, process, and generated-residue checks
  passed.
- No private path, authority, characterizer, preflight, observation, process,
  GitHub write, installed state, registry, or release state was accessed,
  consumed, executed, or mutated.

### Final Verdict

`accepted_exact_r0_identity_characterizer_secure_ingress_successor`

Acceptance makes only a separate owner implementation decision eligible for
the exact three absent files. It grants no implementation or operational
authority.

```yaml
workflow_handoff:
  role_performed: "Codex E: Final R0 Identity Characterizer Secure-Ingress Successor Contract Re-reviewer"
  reviewed_sha256: "7c7d5cd414b8a893703b014d470b84800b3444a11fe498135a7dd965adeacb69"
  contract_verdict: "accepted_exact_r0_identity_characterizer_secure_ingress_successor"
  finding_status:
    ME-RP-795-INGRESS-A-001: "fixed_confirmed_contract_only"
    ME-RP-795-INGRESS-E-001: "fixed_confirmed_contract_only"
    ME-RP-795-INGRESS-E-002: "fixed_confirmed_contract_only"
  owner_implementation_decision_eligible: true
  implementation_authorized: false
  execution_authorized: false
  preflight_authorized: false
  observation_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Owner exact three-file implementation decision, then Codex C"
```
