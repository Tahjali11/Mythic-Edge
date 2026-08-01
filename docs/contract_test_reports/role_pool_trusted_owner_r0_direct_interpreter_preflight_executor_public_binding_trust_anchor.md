# R0 Direct-Interpreter Public-Binding Trust-Anchor Contract Review

## Findings

No blocking contract findings.

### ME-RP-780-PUBLIC-BINDING-E-006 - Fixed At Contract Level

- Severity: high.
- Finding lifecycle: `fixed_state_followup`.
- Finding status: `fixed_confirmed_contract_only`.
- Blocking status: closed for contract clarification; the unaccepted D
  candidate remains unaccepted and still requires the exact two-file
  correction and fresh implementation review.
- Original evidence: the source D handoff records that the executor-owned
  checksum-field-excluded digest accepted changed source after its embedded
  digest was recomputed. The same file therefore owned both the measured bytes
  and expected value and could self-admit.
- Verification evidence: the revised contract makes executor-byte acceptance
  an external workflow gate. A fresh independent Codex E implementation review
  must bind one exact repository head and exact executor and focused-test raw
  SHA-256 values. The exact owner preflight decision must repeat those two
  hashes and bind the accepted contract and contract-review hashes. Before
  process start or private stdin, the separately authorized execution role
  must independently perform stable ordinary/non-reparse reads, recompute both
  raw hashes, compare them with both bindings, and fail closed on drift.
- Runtime boundary: `_public_bindings()` retains the three independent raw
  artifact comparisons for the predecessor contract review, implementation
  review, and focused executor test. Runtime reports the raw executor digest in
  `executor_sha256` but has no embedded expected executor digest and performs
  no executor self-admission comparison.
- No mechanism expansion: no sidecar, signature, key, launcher, wrapper,
  masking rule, new digest family, schema, lifecycle, status, process,
  hostile-code assurance requirement, or third implementation path is added.
- Next route: exact owner repair authorization, Codex D two-file correction,
  fresh independent Codex E implementation review, then a separate exact
  owner preflight decision. This report is not that implementation review or
  owner decision.

## Open Questions Or Assumptions

None.

The `fresh owner decision` immediately before Codex D in the contract's current
routing paragraph is read as the separately confirmed repair authorization
required by the controlling acceptance clause. It is not the owner preflight
decision that binds final executor bytes. The controlling sequence is explicit:
D first, fresh E implementation review second, and the exact owner preflight
decision only after those final hashes exist.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/780

Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

Protected coordination surface:
https://github.com/Tahjali11/Mythic-Edge/issues/769

## Contract

`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`

- Reviewed SHA-256:
  `d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7`.
- Byte count: `103,819`.
- Accepted predecessor SHA-256:
  `1b44310c1b4398c02ecaff55b520beedf20f7456eee71469976c8c7af3cf5a8b`.
- Source D handoff SHA-256:
  `c029076f2eb4c9c4e7e5576c14bc7b1ef79ba313b9bbd77302f5eed6209a914e`.

The reviewed contract and source handoff are ordinary, non-reparse files. The
contract SHA-256 remained exact after validation.

## Source Finding

`ME-RP-780-PUBLIC-BINDING-E-006`.

The post-merge P1 source comment is:
https://github.com/Tahjali11/Mythic-Edge/pull/792#discussion_r3696262736

Current GitHub evidence confirms that comment is bound to accepted PR #792 head
`28036bc82266702c00308cbb6d60a168a2f32142` at the executor path. It identifies
the missing focused-test, predecessor-review, and implementation-review drift
checks. The exact source D handoff records the later adversarial self-admission
witness and routes E-006 to contract clarification.

## Implementation Under Test

Contract clarification only. No implementation was reviewed or accepted.

The current D candidates remain explicitly unaccepted:

- executor:
  `8e244cb973012d811b2d1a4cdfe0dd831b0b53fa2d0d2bdfae9169343e71eeba`;
- focused test:
  `087ea97b9b16d6463294d08453ff723502853c8aeecf515b4057873eeead45bf`.

Those candidate files were not read, executed, tested, edited, or independently
accepted in this review. Their supplied hashes are context for the future D
boundary, not E validation evidence.

## Report Lifecycle

`report_lifecycle: contract_clarification_review`

## Contract Summary

Fresh independent E review and the exact owner preflight decision jointly own
acceptance of final executor and focused-test bytes. A separately authorized
execution role must independently re-read and compare those bytes before
starting the executor. Runtime retains the three non-self public-artifact
checks and reports its raw executor SHA-256 without using that value as a
self-admission predicate.

The external pre-check, runtime independent-artifact checks, and post-result E
comparison are distinct and cumulative. None grants process, preflight,
observation, publication, release, or readiness authority.

## Exact Future Codex D Scope

After a separate exact owner repair authorization, Codex D may change only:

1. `tools/run_role_pool_r0_direct_interpreter_preflight.py`;
2. `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`.

Inside those two existing paths, D may only:

- retain the three new independent raw-digest comparisons for the predecessor
  contract review, implementation review, and executor test;
- remove `EXECUTOR_SOURCE_BINDING_SHA256`;
- remove `_stable_self_binding_sha256()`;
- remove its otherwise-unused private byte-reader, runtime invocation, and
  self-admission tests;
- remove the executor from the runtime drift matrix;
- refresh only the dependent contract, contract-review, and
  `EXECUTOR_TEST_SHA256` bindings; and
- make mechanical formatting changes required by those removals.

All other behavior and bytes remain unchanged. The accepted harness and harness
test remain byte-exact. D must not add a sidecar, signature, key, launcher,
wrapper, input, masking rule, schema, lifecycle, status, process, digest family,
hostile-code assurance requirement, or third implementation path.

## Internal Project Area Reviewed

`Governance / Role Pool`.

## Bridge-Code Status Reviewed

`shared_support`.

The executor remains bounded R0 preflight bridge code. This contract review
does not move truth ownership, execute the bridge, or accept its unreviewed
candidate bytes.

## Checks Run

```powershell
git fetch --prune
git status --short --branch
git rev-parse HEAD origin/main
Get-FileHash -Algorithm SHA256 <reviewed contract and D handoff>
git show HEAD:<accepted predecessor> | <raw SHA-256 check>
git diff --no-ext-diff --unified=25 -- docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
git diff --check -- docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
py -B - <bounded structural, scope, trust-sequence, and canonical-KAT validator>
py -B tools/check_agent_docs.py
<contract/report path list> | py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
<contract/report path list> | py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
gh pr view 792 --repo Tahjali11/Mythic-Edge --json ...
gh api repos/Tahjali11/Mythic-Edge/pulls/792/reviews/4835311363
gh api repos/Tahjali11/Mythic-Edge/pulls/comments/3696262736
gh api repos/Tahjali11/Mythic-Edge/issues/769
gh api repos/Tahjali11/Mythic-Edge/issues/780
<read-only public-marker process count>
<read-only generated-residue count>
```

No implementation test, private-path operation, executor invocation, preflight,
or observation was run.

## Validation Results

- Repository base: `HEAD` and `origin/main` both
  `4b51761cde2310df3e9cda3a3e3ad34e617c8e79`.
- Revised contract: exact required SHA-256 and `103,819` bytes.
- Accepted predecessor: exact SHA-256 and `96,265` bytes from `HEAD`.
- Source D handoff: exact SHA-256 and `10,858` bytes.
- Public binding inventory: nine current ordinary/non-reparse artifacts exact;
  accepted `HEAD` contract, executor, and focused-test predecessor blobs exact.
- Contract diff: `134` additions, `24` deletions, `16` bounded hunks. The diff
  adds the external acceptance boundary and narrows future D work; it does not
  alter the existing result KAT, selector logic, process behavior, or public
  schema.
- Structural trust-anchor audit: exact E review -> exact owner binding -> stable
  external raw reads -> raw hash comparisons -> fail-closed stop.
- Runtime binding audit: three independent raw-artifact comparisons retained;
  raw executor measurement reported; no self-admission digest or equivalent
  checksum cycle contracted.
- Future D scope audit: exactly two paths; exactly the circular machinery and
  dependent tests removed; no third path or mechanism.
- Canonical KAT: strict duplicate-key JSON parse passed; `38` ordered top-level
  fields; `16` all-false authority fields; `2,156`-byte self-digest preimage;
  `2,239`-byte complete object; self-digest and complete artifact SHA-256 exact.
- Diff whitespace: passed.
- Agent docs: `54` files checked; `0` errors; `0` warnings.
- Path-scoped protected-surface gate: passed; `0` forbidden; `0` warnings.
- Path-scoped secret/private-marker scan: passed; `0` forbidden; `0` warnings.
- PR #792: merged to `main` as
  `4b51761cde2310df3e9cda3a3e3ad34e617c8e79`; exact-head owner-published E
  review remains bound to `28036bc82266702c00308cbb6d60a168a2f32142`.
- Issues #769 and #780: open with `0` top-level comments each.
- Matching preflight/fixed-target process count: `0`.
- Task-generated residue count: `0` before and after review validation.

Two preliminary versions of the bounded ad hoc validator stopped on its own
line-wrap and final-LF assumptions. The corrected validator passed all stated
checks. These were checker-assumption errors, not contract, repository,
implementation, or environment failures.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. No private path, identity, handle,
  command, source bytes, or raw private value was accessed or emitted.
- Vocabulary coherence: passed. The trust anchor is an external workflow gate;
  `public_bindings_exact` remains runtime evidence for independently owned
  inputs, not executor self-authentication.
- Authority semantics: passed. Contract acceptance does not transfer repair,
  implementation, private-input, process, preflight, observation, publication,
  release, submission, merge, deployment, or readiness authority.
- Fail-closed behavior: passed. External identity or digest drift stops before
  executor start, private stdin, or result creation. No retry, alternate bytes,
  or nearest-match acceptance exists.
- Protected-surface rollout: passed. Current E is contract review only. Future D
  remains exactly two files and requires separate repair authorization; final
  executor bytes then require fresh E review and a separate exact owner
  preflight decision.

## Results

- E-006 disposition: `fixed_confirmed_contract_only`.
- Contract verdict:
  `accepted_exact_r0_public_binding_external_trust_anchor_contract`.
- External executor-byte trust anchor: fresh exact-head Codex E implementation
  review plus exact owner preflight decision repeating the E-accepted executor
  and focused-test hashes and binding this accepted contract and review.
- Runtime contract: retains three independent raw-artifact checks and reports
  raw `executor_sha256` without self-admission.
- Future D path count: `2`.
- New trust mechanism count: `0`.
- New public schema, lifecycle, status, process, or digest-family count: `0`.
- D candidate acceptance status: `unaccepted_not_reviewed`.
- Matching process count: `0`.
- Generated residue count: `0`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-780-PUBLIC-BINDING-E-006` | high | `fixed_state_followup` | `fixed_confirmed_contract_only` | closed for contract clarification; future implementation remains unaccepted | Executor-owned masked self-digest accepted changed source after embedded-value recomputation. | External E/owner hash binding, stable pre-start raw comparison, runtime independent-artifact checks, and raw executor reporting without self-comparison are exact. | owner repair authorization -> D -> E implementation review -> owner preflight decision |

## Confirmed Contract Matches

- Fresh E implementation review and the exact owner preflight decision are the
  external acceptance owners for final executor and test bytes.
- The execution role independently re-reads both files and compares both raw
  hashes before process start or private stdin.
- Runtime retains the three independent checks identified by the source P1 and
  D handoff.
- Runtime reports the raw executor hash but contains no expected executor hash
  and makes no self-authentication claim.
- The future D correction is exactly the existing executor and focused test,
  removes only circular machinery and dependent tests, refreshes only dependent
  digests, and preserves every other behavior.
- The contract expressly rejects all requested out-of-scope mechanisms and
  hostile-code assurance expansion absent a separate owner decision and
  contract. No contrary current evidence was found.

## Contract Mismatches

None.

## Missing Tests

None at contract level.

The future D correction must update only the focused fake-adapter tests required
by the accepted scope. This report does not assert that the current unaccepted
candidate already satisfies that obligation.

## Drift Notes

- Repository drift: none. The branch base is exact current `origin/main`.
- Contract drift: intended, bounded, and exactly identified by the required
  revised SHA-256.
- Implementation drift: present and explicitly unaccepted in the two D
  candidate paths; not inspected by this contract-only review.
- GitHub drift: none observed for PR #792 or issues #769/#780.
- Private-path, process, installed-state, release-state, and observation drift:
  not exercised; no authority existed to inspect or mutate those layers.

## Authority Flags

These are post-review operational flags. The current user instruction
separately authorized creation of this one contract-test report and nothing
else.

```yaml
authority_flags:
  owner_repair_decision_eligible: true
  codex_d_repair_routing_eligible: true
  current_d_candidate_accepted: false
  implementation_authorized: false
  private_path_access_authorized: false
  private_path_accessed: false
  process_execution_authorized: false
  preflight_authorized: false
  preflight_executed: false
  observation_consumption_authorized: false
  observation_authorized: false
  observation_executed: false
  receipt_publication_authorized: false
  repository_mutation_authorized: false
  release_state_mutation_authorized: false
  installation_authorized: false
  package_operations_authorized: false
  network_authorized: false
  secrets_authorized: false
  external_isolation_authorized: false
  canary_authorized: false
  r1_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  stage_advancement_authorized: false
  dispatch_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  owner_preflight_decision_eligible: false
  live_ready: false
  trusted_owner_native_profile_ready: false
```

## Recommendation

`request implementation fix`

The contract is accepted. The next effect is a separate exact owner repair
authorization, followed by Codex D's two-file correction. Fresh Codex E must
then review the exact resulting head and hashes. Only after that review may a
separate exact owner preflight decision become eligible. No current process,
preflight, observation, publication, submission, merge, deployment, or
readiness action is authorized.

## Next Workflow Action

Next role: owner exact two-file repair authorization, then Codex D.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex D: Narrow R0 Public-Binding Circular-Self-Admission Fixer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780

Accepted contract:
docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
SHA-256:
d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7

Accepted contract review:
docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_public_binding_trust_anchor.md

Source finding: ME-RP-780-PUBLIC-BINDING-E-006
Source D handoff SHA-256:
c029076f2eb4c9c4e7e5576c14bc7b1ef79ba313b9bbd77302f5eed6209a914e

Change only:
- tools/run_role_pool_r0_direct_interpreter_preflight.py
- tests/test_run_role_pool_r0_direct_interpreter_preflight.py

Retain the three independent raw-artifact checks. Remove
EXECUTOR_SOURCE_BINDING_SHA256, _stable_self_binding_sha256(), its otherwise
unused private byte-reader and runtime call, the executor runtime-drift-matrix
entry, and self-admission tests. Refresh only the dependent contract,
contract-review, and executor-test digests. Preserve all other behavior.

Do not add a sidecar, signature, key, launcher, wrapper, input, masking rule,
schema, lifecycle, status, process, digest family, hostile-code assurance
requirement, or third implementation path. Use fake adapters only. Do not
access the private interpreter path, run the preflight, execute or authorize an
observation, publish a receipt, mutate release or installed state, submit,
merge, deploy, or claim readiness.

Return the exact resulting executor and focused-test hashes, validation,
authority flags, residue count, and a handoff to fresh independent Codex E
implementation review. Do not treat this contract review as acceptance of the
current D candidate.
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
    - "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md"
    - "docs/decisions/ADR-0006-repository-boundary-strategy.md"
    - "docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md"
  protected_surfaces:
    - "public reviewed-artifact binding admission"
    - "private direct-interpreter input boundary"
    - "single-use preflight process and zero-descendant boundary"
    - "issue #769 zero-comment coordination boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "The controlling clauses distinguish pre-D repair authorization from the post-D, post-E exact owner preflight decision."
  stop_conditions:
    - "need to inspect or accept the current unaccepted D candidate"
    - "need to access private interpreter input or execute a process"
    - "scope beyond the contract and one review report"
    - "need for a new trust mechanism, schema, lifecycle, status, process, digest family, assurance claim, or third path"
    - "need to mutate GitHub, release, registry, installed, submission, merge, or deployment state"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "E"
  next_thread: "owner_exact_repair_decision_then_D"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md"
  target_artifact: "exact two-file Codex D correction and implementation handoff"
  review_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_public_binding_trust_anchor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-r0-public-binding-fix-780"
  base_commit: "4b51761cde2310df3e9cda3a3e3ad34e617c8e79"
  reviewed_contract_sha256: "d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7"
  accepted_predecessor_sha256: "1b44310c1b4398c02ecaff55b520beedf20f7456eee71469976c8c7af3cf5a8b"
  source_handoff_sha256: "c029076f2eb4c9c4e7e5576c14bc7b1ef79ba313b9bbd77302f5eed6209a914e"
  source_finding: "ME-RP-780-PUBLIC-BINDING-E-006"
  finding_status: "fixed_confirmed_contract_only"
  contract_verdict: "accepted_exact_r0_public_binding_external_trust_anchor_contract"
  external_trust_anchor: "fresh exact-head E implementation review plus exact owner preflight decision"
  runtime_binding: "three independent raw-artifact checks plus raw executor reporting without self-admission"
  future_d_scope:
    - "tools/run_role_pool_r0_direct_interpreter_preflight.py"
    - "tests/test_run_role_pool_r0_direct_interpreter_preflight.py"
  current_d_candidate_accepted: false
  owner_repair_decision_eligible: true
  codex_d_repair_routing_eligible: true
  owner_preflight_decision_eligible: false
  implementation_authorized: false
  private_path_accessed: false
  process_executed: false
  preflight_executed: false
  observation_executed: false
  receipt_published: false
  r1_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  matching_process_count: 0
  generated_residue_count: 0
  validation:
    - "revised, predecessor, and source-handoff SHA-256 values exact"
    - "external trust-anchor ordering and fail-closed raw comparison exact"
    - "runtime three-check retention and raw executor reporting without self-admission exact"
    - "future D path count 2; new trust mechanism and third-path count 0"
    - "38-field canonical KAT and 16 all-false authority fields exact"
    - "diff, agent-doc, protected-surface, and private-marker checks passed"
    - "issues 769 and 780 open with zero comments; PR 792 merged from exact reviewed head"
    - "no D candidate access, private-path access, process execution, preflight, or observation"
  stop_conditions:
    - "binding, issue, PR, contract-review, or owner-decision drift"
    - "scope beyond the exact two future D paths"
    - "private interpreter path or real process access"
    - "new sidecar, signature, key, launcher, wrapper, schema, lifecycle, status, process, digest family, assurance requirement, or third implementation path"
    - "issue #769 comment or protected-state mutation"
```
