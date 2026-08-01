# R0 Direct-Interpreter Preflight Implementation Review

## Findings

### ME-RP-780-PREFLIGHT-EXEC-E-004 - Handle cleanup short-circuits

- Severity: high
- Finding lifecycle: `original_finding`
- Finding status: `open_blocking`
- Blocking status: blocking
- First proven failure point:
  `tools/run_role_pool_r0_direct_interpreter_preflight.py:1802` implements
  `_close_all` with `all(handle.close() for ...)`. Python's `all` stops at the
  first false result, so a failed close prevents every remaining owned handle
  from even receiving its one required close attempt.
- Reproduction: three synthetic owned handles were supplied in memory, with
  the first reverse-order close returning false. Only that handle was
  attempted; the other two remained unattempted.
- Exact failed contract claim:
  `docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md:299`
  requires every branch to close every owned handle exactly once, and line
  740 requires every owned handle to close with no target surviving.
- Dependent cleanup issue: `attribute_list` becomes non-null before the second
  `InitializeProcThreadAttributeList` call succeeds, while the `finally` block
  calls `DeleteProcThreadAttributeList` whenever the pointer is non-null. The
  implementation does not separately track successful attribute-list
  initialization.
- Required correction: eagerly attempt every owned-handle close exactly once,
  aggregate all close results without short-circuiting, track successful
  attribute-list initialization separately, and add injected-failure tests for
  every cleanup stage. Any failed close must keep cleanup unconfirmed.
- Next route: Codex D.

### ME-RP-780-PREFLIGHT-EXEC-E-005 - Zero-effect claims lack owning observations

- Severity: high
- Finding lifecycle: `original_finding`
- Finding status: `open_blocking`
- Blocking status: blocking
- First proven failure point:
  `tools/run_role_pool_r0_direct_interpreter_preflight.py:2113` derives
  `cleanup_confirmed` only from job active-count, process wait, and handle-close
  results. The production call path takes no before/after repository,
  installed-tree, or generated-residue observation.
- Independent AST audit: `_execute_win32_once` contains zero calls to
  `_stable_file_sha256` and no call whose name owns a snapshot, residue, or
  write check. The caller at lines 1111-1160 adds no such observation.
- The result projector at lines 856-859 nevertheless hard-codes
  `repository_write_count`, `installed_write_count`,
  `network_operation_count`, and `external_effect_count` to zero for every
  result.
- Exact failed contract claim:
  `docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md:333-336`
  permits cleanup confirmation only when the exact
  repository/installed/residue checks remain unchanged. The current bytes can
  publish a successful, review-eligible result without that evidence.
- Required correction: take deterministic pre/post observations for every
  contract-owned local effect surface, fail closed on drift or observation
  ambiguity, and derive effect counts and `cleanup_confirmed` from those
  observations rather than constants. Add fake-kernel tests for repository,
  installed-tree, and residue drift. If the zero-network claim cannot be
  enforced or observed within the accepted two-file interface, route that
  narrower constructibility ambiguity to Codex B instead of weakening the
  result.
- Next route: Codex D, with Codex B only if the accepted interface cannot own
  the required evidence.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/780

Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

Protected coordination surface:
https://github.com/Tahjali11/Mythic-Edge/issues/769

## Contract

`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`

SHA-256:
`d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848`

Accepted contract-review report:
`docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`

SHA-256:
`97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038`

## Implementation Under Test

Branch:
`codex/role-pool-r0-direct-interpreter-preflight-executor-contract-780`

Reviewed head and `origin/main`:
`3c3b4bfa7ddcd066d54b8b17ca9f3d496919d23f`

Exactly two implementation paths were reviewed:

1. `tools/run_role_pool_r0_direct_interpreter_preflight.py`
   - byte count: 78,988
   - SHA-256:
     `3490a3c2a0492b3375def91effa8ff0eeb7704d705cf3d103a4737bf086b660a`
2. `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`
   - byte count: 27,936
   - SHA-256:
     `4cd7182ad7e0daa8b9ec0751aacd461f163656546696425d399fc1a55933fcdb`

Both are ordinary, non-reparse files without a UTF-8 BOM and with exactly one
final LF. Their hashes remained stable after validation.

## Report Lifecycle

`report_lifecycle: initial_contract_test`

## Implementation Verdict

`blocked_two_cleanup_and_effect_evidence_findings`

## Intended Behavior

The executor must perform at most one separately authorized synthetic launch
of the exact private CPython binding through the contracted Win32 boundary.
It must preserve exact source-state and result projection, close every owned
resource, prove cleanup and zero effects, emit no private value, and return no
operational authority.

## Actual Behavior

The pure selectors, canonical result model, static Win32 creation order, and
fake-adapter projections match the contract. The production cleanup helper can
leave proven-owned handles unattempted after one close failure, and the
production path can claim unchanged effect surfaces without observing them.

No real interpreter, process preflight, observation, receipt, issue comment,
or release-state operation was executed during this review.

## Internal Project Area Reviewed

`Governance / Role Pool`, matching the contract.

## Bridge-Code Status Reviewed

`shared_support`, matching the contract. Truth ownership remains with the
accepted direct-interpreter successor, parent harness, this executor's actual
Win32 observations, and independent review; the executor does not gain
release-state or readiness authority.

## Checks Run

```powershell
py -B -m pytest tests\test_run_role_pool_r0_direct_interpreter_preflight.py -q
py -B -m pytest tests\test_check_role_pool_r0_offline_observation.py -q
py -B -m ruff check tools\run_role_pool_r0_direct_interpreter_preflight.py tests\test_run_role_pool_r0_direct_interpreter_preflight.py
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py -B tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Additional read-only checks recomputed exact artifact hashes, ordinary-file
and reparse status, all canonical vectors and selectors, live issue comment
counts, matching process count, generated residue, the close-failure witness,
and the production-call AST effect-observation audit.

## Results

- Executor focused suite: 45 passed.
- Parent observation harness: 121 passed.
- Ruff: passed.
- Agent docs: 54 files, 0 errors, 0 warnings.
- Diff check: passed.
- Path-fed protected-surface scan: forbidden 0, warnings 0.
- Path-fed secret/private-marker scan: forbidden 0, warnings 0.
- Issue #780: open, zero comments.
- Protected issue #769: open, zero comments.
- Matching target-process count: zero.
- Generated task residue: zero after review cleanup.
- Real preflight execution count: zero.

Green fake-adapter tests do not prove the real Windows kernel boundary. They
prove pure selectors, projections, and injected-adapter behavior only; a
separately authorized synthetic preflight remains necessary after the two
implementation findings are fixed and independently confirmed.

## Independent Contract Evidence

- Public artifact bindings: exact.
- Source-state audit: 2,916 combinations; 8 valid; 2,908 rejected; no overlap.
- Ambient-job selector: 19 tuples; outcomes `1/1/1/8/4/1/2/1`; audit
  `0/0/0`.
- Terminal selector: 16 tuples; outcomes `1/1/1/1/1/2/1/5/2/1`; audit
  `0/0/0`.
- Parent 64-tuple classifier outcomes: `32/20/9/1/1/1`; audit `0/0/0`.
- Result fixtures: all 16 canonical positive projections sealed and parsed;
  declared row counts reproduced.
- Success KAT: 38 fields; 2,156-byte preimage; 2,239-byte complete artifact;
  self-digest
  `7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56`;
  artifact SHA-256
  `cdcb9a8155006d0fe458e5a486c3d86eb83f85316aba0afdfd21899587cb807`.
- All 16 result authority fields: false.
- No-echo tests and fixed public sentinel behavior: passed.
- Static launch ordering: CreateProcessW is suspended, the exact three-handle
  inheritance list is bound, job assignment/readback/image/parentage checks
  precede resume, and no retry path is present.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-780-PREFLIGHT-EXEC-E-004` | high | `original_finding` | `open_blocking_handle_cleanup_short_circuit` | blocking | Contract requires every owned handle to receive exactly one close attempt on every branch. | Direct in-memory failure witness attempted only the first reverse-order handle; two owned handles were skipped. | D |
| `ME-RP-780-PREFLIGHT-EXEC-E-005` | high | `original_finding` | `open_blocking_zero_effect_evidence_absent` | blocking | Cleanup confirmation requires exact repository, installed-tree, and residue checks to remain unchanged. | Production call-path and AST audit found no owning pre/post observation, while four effect counts are constants. | D, or B only if exact two-file constructibility fails |

## Confirmed Contract Matches

- Exact contract, review, parent, harness, implementation, and test bindings.
- Closed source-state, ambient-job, terminal, parent, and result selectors.
- Exact 38-field KAT and all-false authority object.
- Fixed command, environment allowlist, suspended process creation, one private
  Job Object, exact inherited-handle list, and pre-resume validation order.
- Canonical result parsing and fixed no-echo failure projection.
- No implementation, observation, publication, R1-R8, Stage 4, or live
  authority widening.

## Contract Mismatches

- `_close_all` does not attempt all remaining owned handles after one close
  failure, violating exact-once cleanup closure.
- `cleanup_confirmed` and the zero-effect fields are not supported by the
  contract-required repository, installed-tree, and residue observations.

## Missing Tests

- A close-failure injection proving every other owned handle is still
  attempted exactly once and cleanup remains false.
- Attribute-list initialization failure proving deletion occurs only after
  successful initialization.
- Pre/post repository, installed-tree, and generated-residue drift tests for
  both success and failure lifecycles.
- A production-boundary test proving effect counters and cleanup truth are
  derived from observations rather than fixed literals.

## Drift Notes

No repository, branch, issue, tracker, installation, release-state, or local
data drift was observed. The findings are current implementation defects, not
environment or setup failures.

## Remaining Operational Risk

The review deliberately did not exercise the real interpreter or Win32 kernel
boundary. Fake adapters cannot establish real Job Object event delivery,
handle-close behavior, process termination, private executable startup hooks,
or host effect isolation. Those remain unknown until a corrected exact-byte
implementation passes a fresh independent review and the owner separately
authorizes one synthetic preflight.

## Recommendation

Request one consolidated implementation fix. Do not route to a synthetic
preflight decision while either finding remains open.

## Next Workflow Action

Next role: Codex D, narrow cleanup and effect-evidence fixer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex D: R0 Direct-Interpreter Preflight Cleanup and Effect-Evidence
Fixer.

Worktree: C:\ME780B2
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Contract SHA-256:
d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848

Fix only ME-RP-780-PREFLIGHT-EXEC-E-004 and
ME-RP-780-PREFLIGHT-EXEC-E-005 in:
- tools/run_role_pool_r0_direct_interpreter_preflight.py
- tests/test_run_role_pool_r0_direct_interpreter_preflight.py

For E-004, make every proven-owned handle receive exactly one close attempt
even when an earlier close fails, aggregate cleanup truth without
short-circuiting, and delete the process attribute list only after successful
initialization. Add deterministic failure-injection coverage.

For E-005, add the contract-required pre/post repository, installed-tree, and
generated-residue observations, fail closed on drift or ambiguity, and derive
cleanup/effect fields from evidence rather than constants. If the zero-network
claim cannot be enforced or observed within the accepted two-file interface,
stop and route that exact constructibility ambiguity to Codex B.

Preserve every accepted binding, selector, KAT, no-echo rule, lifecycle
precedence, process topology, and all-false authority output. Do not execute a
real interpreter or preflight, access private authority, publish, mutate
release state, install, authorize R1-R8, or advance Stage 4.

Run the contract-required focused tests, Ruff, diff, agent-doc, path-fed
protected-surface, private-marker, process, and residue checks. Return exact
resulting hashes and route to Codex E for independent confirmation.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "D"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_implementation.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_fixed_state_review"
  branch: "codex/role-pool-r0-direct-interpreter-preflight-executor-contract-780"
  contract_sha256: "d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848"
  implementation_hashes:
    tools/run_role_pool_r0_direct_interpreter_preflight.py: "3490a3c2a0492b3375def91effa8ff0eeb7704d705cf3d103a4737bf086b660a"
    tests/test_run_role_pool_r0_direct_interpreter_preflight.py: "4cd7182ad7e0daa8b9ec0751aacd461f163656546696425d399fc1a55933fcdb"
  finding_status:
    ME-RP-780-PREFLIGHT-EXEC-E-004: "open_blocking_handle_cleanup_short_circuit"
    ME-RP-780-PREFLIGHT-EXEC-E-005: "open_blocking_zero_effect_evidence_absent"
  validation:
    - "45 executor-focused tests passed"
    - "121 parent harness tests passed"
    - "Ruff, agent docs, diff, path-fed safety scans passed"
    - "selectors and KAT independently reproduced"
  real_preflight_executed: false
  observation_created: false
  release_state_mutated: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  stop_conditions:
    - "Stop if the fix requires a third implementation path or contract change."
    - "Stop before any real interpreter or private-path execution."
  next_recommended_role: "Codex D: one consolidated cleanup and effect-evidence fix"
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
  accepted_adrs_read: []
  protected_surfaces:
    - "private interpreter path and owning bytes"
    - "Windows process and Job Object boundary"
    - "repository and installed Role Pool trees"
    - "release state and observation receipts"
  authority_conflicts_found: false
  authority_conflict_notes: "No authority conflict; two current implementation blockers remain."
  stop_conditions:
    - "No real preflight or interpreter execution."
    - "No implementation edits by Codex E."
    - "No publication, release-state, R1-R8, Stage 4, or readiness action."
```
