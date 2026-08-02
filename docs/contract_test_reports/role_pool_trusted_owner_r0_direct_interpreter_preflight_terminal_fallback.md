# R0 Direct-Interpreter Terminal-Fallback Clause Re-review

## Findings

No blocking contract findings.

### ME-RP-780-PREFLIGHT-TERM-B-001 - Fixed At Contract Level

- Severity: high.
- Finding lifecycle: fixed_state_followup.
- Finding status: fixed_confirmed_contract_only.
- Blocking status: not blocking.
- Original evidence: the historical owner-authorized preflight exited 3 with
  empty stdout and the exact 37-byte generic unknown sentinel, but no canonical
  result sealed. Public evidence could not establish whether CreateProcessW was
  entered.
- Verification evidence: every active unsealable route after exact CLI
  admission now selects only the exact precreate, create-entered, or ambiguous
  diagnostic from one invocation-local monotonic tracker. Ambiguous tracker
  state, terminal bytes, output association, or owner-decision association is
  conservatively consumed and nonreusable.
- Generic-sentinel boundary: the existing 37-byte sentinel remains available
  only before tracker creation or when exact terminal emission cannot be
  established.
- Historical disposition: consumed_unknown_nonreusable; accepted observation
  count 0; reconstruction, continuation, repair, reuse, and retry remain
  prohibited.
- Next route: a separate owner implementation decision, then an
  owner-authorized Codex D correction limited to the existing executor and
  focused-test files, followed by fresh independent Codex E implementation
  review.

## Open Questions Or Assumptions

None.

The current contract records two distinct lineage facts. The immediate
committed predecessor at the required base is
d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7.
The source finding and current handoff bind the reviewed predecessor as
8a256548b34fc97f2fa926a87a9167abc2c7821c166f0f19b97660d784b79e8a.
They are not treated as interchangeable.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/780

Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

Protected coordination surface:
https://github.com/Tahjali11/Mythic-Edge/issues/769

## Contract

docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md

- Reviewed SHA-256:
  cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4.
- Reviewed byte count: 114,199.
- Reviewed predecessor SHA-256:
  8a256548b34fc97f2fa926a87a9167abc2c7821c166f0f19b97660d784b79e8a.
- Immediate committed predecessor SHA-256:
  d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7.
- Base commit:
  9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a.
- Base tree:
  dc4ff2cb56e2e3556fd176f14b23a139ec068748.

## Implementation Under Test

Contract clarification only. No implementation was changed, executed, or
accepted.

Future constructibility was inspected read-only at:

1. tools/run_role_pool_r0_direct_interpreter_preflight.py
2. tests/test_run_role_pool_r0_direct_interpreter_preflight.py

The current outer run boundary, the one CreateProcessW call site, and existing
focused fake-adapter tests are sufficient for the local tracker, exact terminal
selection, and focused verification. No parent-harness change or third
implementation path is required.

## Report Lifecycle

report_lifecycle: contract_clarification_review

## Contract Summary

After exact CLI admission, one invocation-local tracker begins in precreate and
may transition once to create_entered immediately before the sole
CreateProcessW call. A sealable canonical result remains unchanged. An
unsealable route emits empty stdout, exit 3, and exactly one of three
public-safe diagnostics. Invalid or contradictory tracker state and inexact
terminal evidence fail closed to the ambiguous consumed disposition.

Acceptance creates only owner_implementation_decision_eligible=true. It creates
no implementation, private-path, process, preflight, Observation 1, retry,
receipt, release, R1-R8, Stage 4, submission, merge, deployment, or readiness
authority.

## Internal Project Area Reviewed

Governance / Role Pool.

## Bridge-Code Status Reviewed

shared_support.

The executor remains bounded R0 preflight bridge code. Parser truth, release
truth, registry truth, installed-copy truth, Observation 1 behavior, and issue
#769 ownership do not move.

## Checks Run

~~~powershell
git status --short --branch
Get-FileHash -Algorithm SHA256 <contract and five custody files>
git rev-parse HEAD HEAD^{tree}
git remote get-url origin
git diff --name-status 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a
git diff --stat 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a
git diff --no-ext-diff --unified=6 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a -- <contract>
git diff --check 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a -- <contract>
py -B - <structured fenced-block, KAT, and diagnostic-vector validator>
py -B tools/check_agent_docs.py
<contract path> | py -B tools/check_protected_surfaces.py --base 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a --paths-from-stdin
<contract path> | py -B tools/check_secret_patterns.py --base 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a --paths-from-stdin
gh issue view 780 --repo Tahjali11/Mythic-Edge --json ...
gh issue view 769 --repo Tahjali11/Mythic-Edge --json ...
<read-only matching executor process count>
git ls-files --others --exclude-standard
git status --short --branch --untracked-files=all
~~~

No implementation test, private-path operation, executor invocation, real
preflight, or Observation 1 execution was run.

## Validation Results

- Repository identity: Tahjali11/Mythic-Edge at the required branch, base
  commit, and base tree.
- Changed paths: exactly 1, the reviewed contract; 234 additions and 81
  deletions.
- Revised contract: exact required 114,199 bytes and SHA-256.
- Initial and immediate-pre-publication custody: all six required files exact.
- Diff whitespace: passed.
- Fenced-block audit: 8 balanced blocks; strict JSON passed; all 3 YAML blocks
  parsed.
- Agent docs: 54 files checked; 0 errors; 0 warnings.
- Path-fed protected-surface scan: exactly 1 contract path; 0 forbidden; 0
  warnings.
- Path-fed secret/private-marker scan: exactly 1 contract path; 0 forbidden; 0
  warnings.
- Issues #780 and #769: open with 0 top-level comments each.
- Matching executor process count: 0.
- Untracked paths before report publication: 0.
- Task-generated residue count before report publication: 0.

## Diagnostic Verification

| route | bytes | SHA-256 | byte properties | disposition |
| --- | ---: | --- | --- | --- |
| precreate | 58 | 7584ac48a50925e117afb55e6127b27f5ceb36ccb753a5ab8eee32cd0b290473 | ASCII; one LF; no CR/BOM; empty stdout; exit 3 | retired unconsumed and nonreusable |
| create-entered | 61 | 96b69d4593abab39f9d256461aa0b692f58750059af5d6277273dd49de1ba97c | ASCII; one LF; no CR/BOM; empty stdout; exit 3 | consumed and nonreusable |
| ambiguous | 62 | 6f7649de0b4db9c2b5db46635ff52ff4fdcb47fef8daa41a1c4cb7766e4729bd | ASCII; one LF; no CR/BOM; empty stdout; exit 3 | conservatively consumed and nonreusable |

The diagnostics contain only the coarse create-boundary stage and consumption
disposition. They contain no path, identity, PID, handle, command, environment
value, exception, Win32 error, target output, private value, or detailed
internal cause. The generic sentinel independently reproduced as 37 bytes at
SHA-256 f8ef6df4e5fa677e28cd29a82b1a0d1d983ca336610971c842a725c25c17018e.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. No private path was accessed, and no
  diagnostic permits private or detailed cause output.
- Vocabulary coherence: passed. The three diagnostics are not result statuses,
  schemas, receipts, or authority objects. The six result statuses are
  unchanged.
- Authority semantics: passed. Acceptance only makes a separate owner
  implementation decision eligible.
- Fail-closed behavior: passed. Ambiguous tracker state, terminal output, or
  decision association is consumed and nonreusable.
- Protected-surface rollout: passed. Current work is contract review only;
  implementation remains separately gated and limited to two existing paths.

## Results

- contract_verdict:
  accepted_exact_r0_terminal_fallback_clause_reconciliation
- finding_status:
  ME-RP-780-PREFLIGHT-TERM-B-001: fixed_confirmed_contract_only
- owner_implementation_decision_eligible: true
- implementation_authorized: false
- preflight_authorized: false
- observation_1_authorized: false
- retry_authorized: false
- stage4_authorized: false
- live_ready: false

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ME-RP-780-PREFLIGHT-TERM-B-001 | high | fixed_state_followup | fixed_confirmed_contract_only | not_blocking | Historical unsealed attempt exposed only the generic sentinel and could not establish the create boundary. | All active post-admission unsealed routes now use one of three exact tracker-selected diagnostics; ambiguity is consumed and nonreusable. | owner decision -> D -> E |

## Confirmed Contract Matches

- Every active post-CLI-admission unsealable route selects precreate,
  create-entered, or ambiguous. No active clause routes directly to the generic
  legacy sentinel.
- Generic-sentinel references that would otherwise conflict occur only in the
  explicitly superseded historical section. Active references retain it only
  before tracker creation or when exact terminal emission cannot be
  established.
- LE-03 through LE-05, prelaunch order, result projection, lifecycle
  precedence, required tests, and acceptance criteria use the same terminal
  rule.
- A sealed result still has exactly 38 ordered top-level fields and 16
  all-false authority fields.
- The schema-field list, six result statuses, and full success KAT are
  byte-identical to the committed predecessor.
- KAT validation reproduced the 2,156-byte self-digest preimage, 2,239-byte
  complete object, embedded self-digest
  7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56,
  and artifact SHA-256
  cdcb9a8155006d0fe458e5a486c3d86eb83bf85316aba0afdfd21899587cb807.
- No schema, result field, result status, process, retry, sidecar, durable trace,
  receipt, Observation 1 behavior, third implementation path, or detailed
  diagnostic vocabulary was added.
- The accepted predecessor review, executor, focused test, parent harness, and
  parent harness test remained byte-exact.
- The historical attempt remains consumed_unknown_nonreusable and cannot be
  reclassified, continued, repaired, reused, or retried.

## Contract Mismatches

None.

## Missing Tests

None at contract level.

The future owner-authorized Codex D correction must add the exact focused
fake-adapter tests required by clauses 28 through 35. This contract review does
not assert that the current implementation already emits the new diagnostics.

## Drift Notes

- Repository drift: none at the reviewed base commit and tree.
- Contract drift: intended, exact, and limited to the one reviewed path.
- Implementation drift: none; both implementation files remained byte-exact.
- GitHub drift: none observed for issue #780 or protected issue #769.
- Private-path, process, installed-state, release-state, registry-state, and
  observation drift: not exercised and not authorized.

## Authority Flags

These are post-review operational flags. The user separately authorized
creation of this one contract-test report.

~~~yaml
authority_flags:
  owner_implementation_decision_eligible: true
  implementation_authorized: false
  private_path_access_authorized: false
  private_path_accessed: false
  process_execution_authorized: false
  preflight_authorized: false
  preflight_executed: false
  observation_1_authorized: false
  observation_1_executed: false
  retry_authorized: false
  receipt_publication_authorized: false
  repository_mutation_authorized: false
  release_state_mutation_authorized: false
  installation_authorized: false
  package_operations_authorized: false
  network_authorized: false
  secrets_authorized: false
  external_isolation_authorized: false
  r1_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  stage_advancement_authorized: false
  dispatch_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  trusted_owner_native_profile_ready: false
~~~

## Recommendation

approve

The contract is accepted. The next effect is only a separate owner
implementation decision. If that owner decision authorizes implementation,
Codex D may correct exactly the existing executor and focused-test files.
Fresh independent Codex E implementation review remains required afterward.

## Next Workflow Action

Next role: separate owner implementation decision, then owner-authorized Codex
D.

Pasteable prompt:

~~~text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex D: Narrow R0 Terminal-Fallback Implementer, but proceed only after
the owner explicitly authorizes implementation.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Branch: codex/role-pool-r0-terminal-fact-contract-780

Accepted contract:
docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
SHA-256:
cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4

Accepted contract review:
docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback.md

Source finding: ME-RP-780-PREFLIGHT-TERM-B-001

Change only:
- tools/run_role_pool_r0_direct_interpreter_preflight.py
- tests/test_run_role_pool_r0_direct_interpreter_preflight.py

Add only the invocation-local monotonic precreate/create-entered tracker, the
three exact ASCII fallback constants, outer terminal selection, and focused
fake-adapter tests required by the contract. Preserve the canonical 38-field
schema, six statuses, KAT, process behavior, no-retry behavior, parent harness,
and every unrelated byte.

Do not access a private interpreter path, run the real preflight, execute
Observation 1, publish a receipt, mutate issue #769, release, registry, or
installed state, or authorize R1-R8, Stage 4, submission, merge, deployment, or
readiness. Return to fresh independent Codex E implementation review.
~~~

~~~yaml
instruction_context:
  required_for_risk_tier: medium_or_high
  deferred_for_low_risk: false
  role: E
  risk_tier: high
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md
  protected_surfaces:
    - private direct-interpreter path
    - single-use R0 preflight process and zero-descendant boundary
    - immutable historical attempt and Observation 1 authority
    - issue #769 zero-comment boundary
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - custody byte drift
    - active-clause contradiction or false consumption semantics
    - scope beyond the contract and one review report
    - private path, real preflight, Observation 1, or GitHub mutation
~~~

~~~yaml
workflow_handoff:
  repository: Tahjali11/Mythic-Edge
  repository_url: https://github.com/Tahjali11/Mythic-Edge
  issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
  tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
  protected_coordination_surface: https://github.com/Tahjali11/Mythic-Edge/issues/769
  completed_thread: E
  next_thread: owner_implementation_decision_then_D
  source_artifact: docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
  target_artifact: exact two-file Codex D correction and implementation handoff
  review_artifact: docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback.md
  risk_tier: high
  base_branch: origin/main
  target_branch: unselected_pending_owner_decision
  branch: codex/role-pool-r0-terminal-fact-contract-780
  base_commit: 9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a
  base_tree: dc4ff2cb56e2e3556fd176f14b23a139ec068748
  source_finding: ME-RP-780-PREFLIGHT-TERM-B-001
  reviewed_contract_sha256: cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4
  reviewed_contract_byte_count: 114199
  reviewed_predecessor_sha256: 8a256548b34fc97f2fa926a87a9167abc2c7821c166f0f19b97660d784b79e8a
  finding_status:
    ME-RP-780-PREFLIGHT-TERM-B-001: fixed_confirmed_contract_only
  contract_verdict: accepted_exact_r0_terminal_fallback_clause_reconciliation
  historical_attempt_status: consumed_unknown_nonreusable
  accepted_observation_count: 0
  future_implementation_scope:
    - tools/run_role_pool_r0_direct_interpreter_preflight.py
    - tests/test_run_role_pool_r0_direct_interpreter_preflight.py
  owner_implementation_decision_eligible: true
  implementation_authorized: false
  preflight_authorized: false
  observation_1_authorized: false
  retry_authorized: false
  stage4_authorized: false
  live_ready: false
  matching_executor_process_count: 0
  generated_residue_count: 0
  validation:
    - exact contract and five-file custody
    - active terminal routes and historical supersession reviewed
    - three diagnostic vectors exact
    - 38-field schema, six statuses, and KAT unchanged
    - diff, agent-doc, protected-surface, and private-marker checks passed
    - issues 780 and 769 open with zero comments
    - no private-path access, real preflight, or Observation 1 execution
  stop_conditions:
    - owner implementation decision absent
    - binding or custody drift
    - scope beyond the exact two future implementation paths
    - private path, real preflight, Observation 1, or protected-state mutation
~~~
