# R0 Direct-Interpreter Post-Merge Binding Fixer Handoff

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
`1b44310c1b4398c02ecaff55b520beedf20f7456eee71469976c8c7af3cf5a8b`

## Internal Project Area

Governance / Role Pool

## Truth Owner

The accepted R0 contract and independently reviewed artifact bytes own public
binding eligibility. The executor only validates and reports those bindings.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer for the post-merge P1 public-binding finding recorded at
https://github.com/Tahjali11/Mythic-Edge/pull/792#discussion_r3696262736.

## What Changed

The first D pass added raw SHA-256 comparisons for the accepted predecessor
contract review, implementation review, and focused executor test. Those three
omissions from the post-merge P1 are fixed in the current candidate.

The executor candidate also added a checksum-field-excluded self-digest. Fresh
Codex E review correctly rejected that part as
`ME-RP-780-PUBLIC-BINDING-E-006`: the executor owns both the source bytes and
the expected digest, so changed source can replace its embedded digest and
still self-admit. The self-digest is therefore not independent evidence of
Codex E acceptance.

No second implementation edit was made. The current two-file contract exposes
no independently owned accepted digest for the post-merge executor bytes, so a
further local D edit would repeat the same circular proof in another form.

## Files Changed

- `tools/run_role_pool_r0_direct_interpreter_preflight.py`
- `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`
- `docs/implementation_handoffs/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_post_merge_binding_fixer.md`

## Code Changed

Yes, in the first D pass. Only public artifact validation that runs before
private input or process entry changed. The follow-up E-006 disposition changed
this handoff only. No process, result-schema, selector, authority, local-effect,
inventory, or cleanup behavior changed.

## Tests Added Or Updated

- Expanded the public drift matrix from six to ten named artifacts.
- Added source-byte and embedded-checksum drift cases for the executor
  self-binding.
- Preserved the existing no-private-access-on-public-drift regression.

These tests establish individual drift detection but do not establish
independent executor acceptance. A bounded adversarial probe changed one source
byte, recomputed the embedded digest, and reproduced E-006:

```text
changed_bytes=True
self_accepted=True
```

## Interface Changes

None. No public field, CLI argument, output, status, environment variable, or
process interface changed.

## Contracted Area Status

The three raw omissions were fixed inside the accepted two-file implementation
boundary. E-006 cannot be closed inside that boundary because the accepted
contract assigns executor-byte acceptance to independent Codex E but supplies
no independent runtime trust anchor for those accepted bytes. No downstream
product surface was touched.

## Follow-Up Finding

`ME-RP-780-PUBLIC-BINDING-E-006` remains blocking.

Observed:

- `_stable_self_binding_sha256()` excludes the embedded expected digest and
  compares the resulting digest with that same executor-owned value.
- No current contract or accepted review artifact contains the independently
  accepted post-merge executor digest in a form the runtime can consume.
- The temporary adversarial probe changed the executor's raw SHA-256 from
  `8e244cb973012d811b2d1a4cdfe0dd831b0b53fa2d0d2bdfae9169343e71eeba`
  to `956142d3a1b1e21e1b83ea3e56bdc03fe5e83d7206bc4ce284bb320f24e26b3`
  and the recomputed embedded self-digest was accepted.

Derived:

- A raw file cannot contain its own SHA-256.
- Masking the checksum field makes construction possible but does not prove
  review acceptance when the same file owns the expected value.
- A safe repair requires an external accepted binding or a contract change to
  the meaning of runtime public-binding admission.

Proposed narrow route:

- Codex B should define one independently reviewed, contract-owned executor
  binding and its exact canonicalization/readback rule, then retain the current
  two-file D implementation envelope if possible.
- If runtime self-admission is not actually required, Codex B must explicitly
  revise that requirement rather than allowing D to infer a relaxation.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: preserved.
- Vocabulary and example coherence: preserved.
- Authority/readiness semantics: unchanged; this fix creates no execution or
  publication authority.
- Fail-closed validator checks: strengthened for three raw omissions; executor
  acceptance remains unresolved.
- Protected-surface rollout phase: contract clarification is required before
  any further implementation review or later owner decision.

## Validation Run

```text
py -B -m pytest -q tests\test_run_role_pool_r0_direct_interpreter_preflight.py
77 passed

py -B -m pytest -q tests\test_check_role_pool_r0_offline_observation.py
121 passed

py -B -m pytest -q
2389 passed, 4 skipped, 1 existing warning

py -B -m ruff check --no-cache tools\run_role_pool_r0_direct_interpreter_preflight.py tests\test_run_role_pool_r0_direct_interpreter_preflight.py
passed

py -B -m ruff check --no-cache src tests tools
passed

py -B tools\check_agent_docs.py
54 files; 0 errors; 0 warnings

path-scoped protected-surface and secret/private-marker scans
3 paths; forbidden 0; warnings 0

installed Role Pool release gate
419 passed; structural validation passed
```

## Still Unverified

- Independent Codex E reviewed the candidate and left E-006 blocking.
- No real preflight or private-path operation was run or authorized.
- Receipt publication and later-rung eligibility remain separate owner
  decisions.
- The read-only bootstrap checker still reports its separate existing
  `blocked_release_state_conflict` result with every observed effect count at
  zero.

## Reviewer Focus

The next review is a contract decision, not another implementation confirmation.
Confirm the smallest non-self-referential trust-anchor design, its ownership,
canonicalization, drift semantics, and exact future D path budget before any
further code edit.

## Next Workflow Action

Next role: Codex B, narrow public-binding trust-anchor contract clarifier.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex B: Narrow R0 Public-Binding Trust-Anchor Contract Clarifier.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Source finding: https://github.com/Tahjali11/Mythic-Edge/pull/792#discussion_r3696262736
Contract: docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md
Implementation handoff: docs/implementation_handoffs/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_post_merge_binding_fixer.md
Branch: codex/role-pool-r0-public-binding-fix-780
Base: origin/main@4b51761cde2310df3e9cda3a3e3ad34e617c8e79

Resolve only ME-RP-780-PUBLIC-BINDING-E-006. The first D pass fixed the three
raw predecessor-review, implementation-review, and executor-test omissions,
but its executor checksum-field-excluded self-digest is self-referential. A
temporary adversarial probe changed a source byte, recomputed the embedded
digest, and was accepted.

Define the smallest independently owned accepted executor binding that
_public_bindings() can validate before parent loading, private input, or process
entry. Prefer preserving the existing two-file future D envelope. Specify the
exact trust owner, artifact/path, canonicalization, readback, drift behavior,
and test matrix. Account explicitly for the raw-self-hash impossibility and do
not create a circular executor/review or executor/test checksum pair. If the
contract instead intends Codex E acceptance to remain external rather than a
runtime admission predicate, revise that semantic explicitly.

Do not implement code, run the real preflight, access private interpreter
input, or mutate receipt, release, registry, installed, or GitHub state. Route
an accepted exact contract back to Codex D, then Codex E.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
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
    - "public reviewed-artifact binding admission"
    - "private direct-interpreter input boundary"
    - "single-use preflight process boundary"
    - "issue #769 zero-comment coordination boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "The owner authorized only this narrow post-merge repair; no execution authority was inferred."
  stop_conditions:
    - "need to change the contract or public result schema"
    - "need to access private input or execute the preflight"
    - "need to mutate release, receipt, registry, installation, or GitHub state"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "D"
  next_thread: "B"
  source_artifact: "PR #792 post-merge finding 3696262736"
  target_artifact: "narrow non-self-referential public-binding contract clarification"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-r0-public-binding-fix-780"
  validation:
    - "focused executor tests -> 77 passed"
    - "immutable parent harness tests -> 121 passed"
    - "full repository tests -> 2389 passed, 4 skipped, 1 existing warning"
    - "focused Ruff -> passed"
    - "adversarial self-binding probe -> changed source self-accepted"
  findings:
    - "three raw artifact omissions fixed in candidate"
    - "ME-RP-780-PUBLIC-BINDING-E-006 remains blocking"
  stop_conditions:
    - "do not run the real preflight or access private interpreter input"
    - "do not mutate receipt, release, registry, installed, or GitHub state"
    - "do not route back to D until an independent binding source or explicit semantic revision is accepted"
```
