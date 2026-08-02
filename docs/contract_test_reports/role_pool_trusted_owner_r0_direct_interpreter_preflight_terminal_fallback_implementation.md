# R0 Terminal-Fallback Implementation Review

## Findings

### ME-RP-780-PREFLIGHT-TERM-E-001 - Blocking

Severity: high.

`_terminal_fallback_diagnostic()` accepts any object whose `diagnostic()`
method returns one of the three known byte strings. It does not require the
invocation-owned `_TerminalBoundaryTracker` type. A foreign tracker can make
`mark_create_entered()` a no-op, return the 58-byte precreate diagnostic, and
therefore report `unconsumed` after the execution boundary was entered.

This contradicts the accepted contract requirement that invalid, missing,
contradictory, or corrupt tracker state fail closed as the 62-byte
ambiguous/consumed diagnostic. It is a concrete implementation defect in the
reviewed two-file scope, not a contract ambiguity.

Evidence:

- `tools/run_role_pool_r0_direct_interpreter_preflight.py:532` calls
  `getattr(tracker, "diagnostic")()` on an arbitrary object.
- `tools/run_role_pool_r0_direct_interpreter_preflight.py:537` accepts the
  returned precreate diagnostic solely because its bytes are in the known set.
- The in-memory fake-adapter witness entered `execute_once`, raised a terminal
  post-entry failure, and emitted
  `direct_interpreter_preflight_unknown_precreate_unconsumed\n`.
- The focused tests cover missing, unreadable, and internally contradictory
  trackers, but do not reject a foreign tracker that returns a valid-looking
  token.

Smallest coherent repair:

1. Require the tracker supplied to `_terminal_fallback_diagnostic()` to be the
   exact invocation-owned tracker type before trusting `diagnostic()`.
2. Route every foreign or substituted tracker to
   `UNKNOWN_STAGE_AMBIGUOUS_CONSUMED`.
3. Add one focused helper-level negative and one CLI-level post-entry witness
   proving that a foreign tracker cannot claim precreate/unconsumed.
4. Do not change the three diagnostics, canonical result schema, process
   boundary, public bindings, or any path outside the exact executor and its
   focused test.

## Open Questions Or Assumptions

None blocking beyond ME-RP-780-PREFLIGHT-TERM-E-001.

The review does not treat hostile mutation of Python code or arbitrary memory
tampering as an in-scope isolation claim. It does require the explicit object
substitution already representable at the reviewed helper boundary to fail
closed.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/780

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`

- SHA-256:
  `cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4`
- Accepted review SHA-256:
  `8fa95ada34171e0e040acea13de52a87d72138995bbcc8b6dc982fb0ecca3880`

## Implementation Under Test

Branch: `codex/role-pool-r0-terminal-fact-contract-780`

- `tools/run_role_pool_r0_direct_interpreter_preflight.py`
  - 129,059 bytes
  - SHA-256:
    `1aa5f31f39035e623431bcab99fd81c0f25fa32710b829653ed82c93b5cc35f3`
- `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`
  - 70,008 bytes
  - SHA-256:
    `91a8902a47069edf1805d0c73079a56c26dc0a5a4dede9ea2c78c8064af3b288`

No implementation file was edited by this review.

## Report Lifecycle

`initial_contract_test`

## Contract Summary

One invocation-local monotonic tracker starts at `precreate` after exact CLI
admission and transitions immediately before the sole `CreateProcessW` call.
An unsealed terminal result emits exactly one of the 58-, 61-, or 62-byte
public-safe diagnostics. Any invalid or ambiguous tracker must select the
62-byte consumed diagnostic. Sealed 38-field results remain unchanged.

## Internal Project Area Reviewed

Governance / Role Pool.

## Bridge-Code Status Reviewed

`shared_support`.

## Checks Run

```powershell
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_preflight.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_offline_observation.py -q -p no:cacheprovider
py -B -m ruff check tools/run_role_pool_r0_direct_interpreter_preflight.py tests/test_run_role_pool_r0_direct_interpreter_preflight.py
git diff --check
py -B tools/check_agent_docs.py
@('tools/run_role_pool_r0_direct_interpreter_preflight.py','tests/test_run_role_pool_r0_direct_interpreter_preflight.py') | py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
@('tools/run_role_pool_r0_direct_interpreter_preflight.py','tests/test_run_role_pool_r0_direct_interpreter_preflight.py') | py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

A pure in-memory fake-adapter witness substituted a foreign tracker whose
`mark_create_entered()` was a no-op and whose `diagnostic()` returned the
precreate token. No real process or private path was used.

## Validation Results

- Focused executor suite: 98 passed.
- Unchanged parent harness: 121 passed.
- Ruff: passed.
- Agent docs: 54 files; 0 errors; 0 warnings.
- Protected-surface scan: forbidden 0; warnings 0.
- Secret/private-marker scan: forbidden 0; warnings 0.
- `git diff --check`: passed.
- Diagnostic vectors: 58/61/62 bytes and all three SHA-256 values exact.
- Matching executor process count: 0.
- Issues #780 and #769: open with zero comments.
- Real preflight executed: false.
- Private interpreter path accessed: false.
- Generated residue count: 0.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed for the exact diagnostics and reviewed
  tests; no private value or detailed cause is emitted.
- Vocabulary coherence: blocking only at the foreign-tracker consumption
  classification described above.
- Authority semantics: no implementation, preflight, Observation 1, R1-R8,
  Stage 4, or readiness authority was created.
- Fail-closed behavior: failed for a substituted tracker returning a known
  diagnostic.
- Protected-surface rollout: remains an inert implementation candidate.

## Results

- implementation_verdict: `changes_requested`
- finding_status:
  - `ME-RP-780-PREFLIGHT-TERM-B-001`:
    `implemented_pending_confirmation`
  - `ME-RP-780-PREFLIGHT-TERM-E-001`:
    `open_blocking_foreign_tracker_underclaims_consumption`
- implementation_authorized: false
- preflight_authorized: false
- observation_1_authorized: false
- retry_authorized: false
- stage4_authorized: false
- live_ready: false

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ME-RP-780-PREFLIGHT-TERM-B-001 | high | fixed_state_followup | implemented_pending_confirmation | blocking | Contract required exact fail-closed tracker-selected fallback diagnostics. | Exact diagnostics, transition placement, canonical-result preservation, and no-echo tests pass, but E-001 prevents final confirmation. | D |
| ME-RP-780-PREFLIGHT-TERM-E-001 | high | original_finding | open_blocking_foreign_tracker_underclaims_consumption | blocking | A foreign tracker can return the valid precreate token after a simulated create-entry failure. | Pure in-memory witness returned exit 3 and the 58-byte unconsumed diagnostic after `execute_once` was entered. | D |

## Confirmed Contract Matches

- Only the executor and focused test changed.
- The tracker is created after exact CLI admission.
- Production transition is immediately before the sole `CreateProcessW` call.
- The 58-, 61-, and 62-byte diagnostics and hashes are exact.
- Invalid CLI retains the legacy generic sentinel.
- Normal sealed canonical results remain unchanged.
- Existing focused and parent harness tests pass.
- No detailed or private information is emitted.

## Contract Mismatches

- A foreign tracker object returning a known diagnostic is trusted without an
  exact tracker-type check, allowing a false precreate/unconsumed claim.

## Missing Tests

- Helper-level rejection of a foreign tracker returning each valid-looking
  diagnostic.
- CLI-level proof that a substituted tracker cannot underclaim consumption
  after fake create-entry execution.

## Drift Notes

No repository, installed-copy, release-state, GitHub, or external drift was
observed. The mismatch is local implementation drift from the accepted
fail-closed tracker contract.

## Recommendation

Request the narrow Codex D implementation fix described above, then return the
same exact two files to Codex E.

## Next Workflow Action

Next role: Codex D, limited to the exact executor and focused test.

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex D: Narrow R0 Foreign-Tracker Fail-Closed Fixer.

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Branch: codex/role-pool-r0-terminal-fact-contract-780

Accepted contract SHA-256:
cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4

Source finding:
ME-RP-780-PREFLIGHT-TERM-E-001

Starting implementation hashes:
- executor: 1aa5f31f39035e623431bcab99fd81c0f25fa32710b829653ed82c93b5cc35f3
- focused test: 91a8902a47069edf1805d0c73079a56c26dc0a5a4dede9ea2c78c8064af3b288

Modify exactly those two files. Require `_terminal_fallback_diagnostic()` to
trust only the exact invocation-owned tracker type. Every foreign or
substituted tracker must select the 62-byte ambiguous/consumed diagnostic.
Add one helper-level negative and one CLI-level fake post-entry witness.

Do not change diagnostic bytes, the canonical schema, process behavior,
public bindings, contracts, reports, or any third path. Do not run a real
preflight or access a private interpreter path. Return exact resulting hashes,
focused validation, residue, authority flags, and route back to Codex E.
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
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback_implementation.md"
  risk_tier: "high"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/role-pool-r0-terminal-fact-contract-780"
  finding_status:
    ME-RP-780-PREFLIGHT-TERM-E-001: "open_blocking_foreign_tracker_underclaims_consumption"
  validation:
    - "focused executor: 98 passed"
    - "unchanged parent harness: 121 passed"
    - "Ruff, agent-doc, diff, protected-surface, and private-marker checks passed"
    - "pure in-memory foreign-tracker witness reproduced the underclaim"
  stop_conditions:
    - "Do not modify any third path."
    - "Do not execute the real preflight or access the private interpreter path."
    - "Do not authorize Observation 1, R1-R8, Stage 4, or readiness."
```

## Followup After Fixer - Fixed State

`report_lifecycle: followup_after_fixer`

This section is append-only. The original finding evidence and the initial
review lifecycle above remain unchanged.

### Fixed-State Findings

No blocking findings remain for the exact fixed bytes.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- |
| ME-RP-780-PREFLIGHT-TERM-B-001 | high | fixed_state_followup | fixed_confirmed | not_blocking | Exact tracker states, fallback vectors, CLI boundaries, public bindings, and preservation checks passed. | owner submission decision |
| ME-RP-780-PREFLIGHT-TERM-E-001 | high | fixed_state_followup | fixed_confirmed | not_blocking | Exact-type admission rejects foreign objects, subclasses, missing or unreadable objects, and all three valid-token spoofers; the fake post-entry CLI witness emitted only the 62-byte consumed diagnostic. | owner submission decision |

### Fixed Bytes And D Delta

- Executor: 129,161 bytes; SHA-256
  `429021301e9aad9958dfafae22fa98665ed75d0f80b241963cc4ecfb97ce97ed`.
- Focused test: 71,756 bytes; SHA-256
  `435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b`.
- The executor delta from the reviewed 129,059-byte predecessor is the unique
  102-byte exact-type guard plus the mechanically dependent same-length
  `EXECUTOR_TEST_SHA256` rebind. A read-only byte-delta audit reproduced prior
  SHA-256
  `1aa5f31f39035e623431bcab99fd81c0f25fa32710b829653ed82c93b5cc35f3`.
- The focused-test delta is exactly a 540-byte three-token foreign-helper block
  plus a 1,208-byte fake post-entry CLI witness. A read-only byte-delta audit
  reproduced prior SHA-256
  `91a8902a47069edf1805d0c73079a56c26dc0a5a4dede9ea2c78c8064af3b288`.
- No third D path, schema, status, process, retry, Observation 1 behavior, or
  authority surface changed.

### Independent Witnesses

- Exact invocation tracker: 58-byte precreate/unconsumed before transition;
  61-byte create-entered/consumed after its sole transition.
- Duplicate transition, contradictory state, corrupt state, and deleted-slot
  unreadability: exact 62-byte ambiguous/consumed diagnostic.
- Foreign tracker returning each of the three valid-looking tokens: exact
  62-byte ambiguous/consumed diagnostic in all three cases.
- Tracker subclasses returning each valid-looking token, missing tracker, and
  unreadable foreign object: exact 62-byte ambiguous/consumed diagnostic.
- Fake CLI post-entry witness: `execute_once` entered once; exit `3`; stdout
  `0` bytes; stderr `62` bytes at SHA-256
  `6f7649de0b4db9c2b5db46635ff52ff4fdcb47fef8daa41a1c4cb7766e4729bd`;
  the 58-byte diagnostic was not emitted.
- Invalid CLI: exit `3`; stdout `0` bytes; exact 37-byte generic sentinel at
  SHA-256
  `f8ef6df4e5fa677e28cd29a82b1a0d1d983ca336610971c842a725c25c17018e`.

### Preservation And Validation

- The tracker is constructed after exact CLI admission and before the first
  fallible post-admission operation.
- Its transition remains immediately before the sole `CreateProcessW` call.
- Result fields: 38. Result statuses: 6. Authority fields: 16, all false.
- Public bindings are exact for the reviewed executor and focused-test hashes.
- Process topology remains one `CreateProcessW` and one `ResumeThread` call
  site. No retry or third process path was added.
- No-echo, canonical-result, cleanup, output, identity, process, and effect
  fixtures remain passing.
- Parent harness and test remain 67,314 and 52,662 bytes at SHA-256
  `001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6`
  and
  `3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3`.
- Historical terminal attempt remains `consumed_unknown_nonreusable`.

Validation results:

- Focused executor suite: 102 passed.
- Unchanged parent harness suite: 121 passed.
- Ruff: passed; a validation-created ignored cache was removed with
  `py -B -m ruff clean`, and the no-cache rerun passed.
- `git diff --check`: passed.
- Agent docs: 54 checked; 0 errors; 0 warnings.
- Exact two-path protected-surface scan: forbidden 0; warnings 0.
- Exact two-path secret/private-marker scan: forbidden 0; warnings 0.
- Issues #780 and #769: open with zero top-level comments each.
- Matching executor process count: 0.
- Final generated-residue count: 0.
- Real preflight executed: false.
- Private interpreter path accessed: false.
- Observation 1 executed: false.

### Fixed-State Result

- implementation_verdict:
  `accepted_exact_r0_terminal_fallback_implementation`
- `ME-RP-780-PREFLIGHT-TERM-B-001: fixed_confirmed`
- `ME-RP-780-PREFLIGHT-TERM-E-001: fixed_confirmed`
- eligible_for_submission_decision: true
- implementation_authorized: false
- preflight_authorized: false
- observation_1_authorized: false
- retry_authorized: false
- stage4_authorized: false
- live_ready: false

### Next Workflow Action

An explicit owner submission decision is required. After that decision, Codex
F may stage only this reviewed five-path package for a draft PR:

1. `docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`
2. `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback.md`
3. `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback_implementation.md`
4. `tools/run_role_pool_r0_direct_interpreter_preflight.py`
5. `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`

Integration and current-main eligibility review remain separate before any new
preflight decision.

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high"
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
    - "single-use R0 terminal and process boundary"
    - "private direct-interpreter path"
    - "historical attempt and Observation 1 authority"
    - "issue #769 zero-comment boundary"
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - "Any reviewed-byte drift."
    - "Any preflight, private-path, Observation 1, release, or protected-state operation."
    - "Any scope outside the reviewed five-path submission package."
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "E"
  next_thread: "explicit owner submission decision, then F"
  source_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback_implementation.md"
  target_artifact: "draft PR containing only the reviewed five-path package"
  risk_tier: "high"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/role-pool-r0-terminal-fact-contract-780"
  base_commit: "9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a"
  implementation_verdict: "accepted_exact_r0_terminal_fallback_implementation"
  finding_status:
    ME-RP-780-PREFLIGHT-TERM-B-001: "fixed_confirmed"
    ME-RP-780-PREFLIGHT-TERM-E-001: "fixed_confirmed"
  eligible_for_submission_decision: true
  implementation_authorized: false
  preflight_authorized: false
  observation_1_authorized: false
  retry_authorized: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "focused executor: 102 passed"
    - "unchanged parent harness: 121 passed"
    - "Ruff, diff, agent-doc, exact path-fed safety scans passed"
    - "helper and fake CLI witnesses fail closed to the exact 62-byte diagnostic"
    - "matching executor processes 0; generated residue 0"
  stop_conditions:
    - "Do not stage any path outside the reviewed five-path package."
    - "Do not execute or authorize the preflight or Observation 1."
    - "Keep integration and current-main eligibility as separate reviews."
```
