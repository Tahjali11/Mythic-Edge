# App-Native R0 Release-State Handoff Completion Successor Contract

## Contract Status

| Field | Value |
|---|---|
| Repository | `Tahjali11/Mythic-Edge` |
| Issue | <https://github.com/Tahjali11/Mythic-Edge/issues/819> |
| Tracker | <https://github.com/Tahjali11/Mythic-Edge/issues/746> |
| Protected coordination issue | <https://github.com/Tahjali11/Mythic-Edge/issues/769> |
| Base commit | `8470dd10c91faa02d923fe5d67246fcf280095cb` |
| Base tree | `5f2d6df830047130671f8ca44804ccb17149e99b` |
| Accepted index-correction contract | `docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md` |
| Accepted index-correction contract SHA-256 | `03634091fc3e544d4850ce1da65001106d3c450d96d4dd779a91b65cbbfb66e5` |
| Accepted contract review | <https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5229306249> |
| Spent correction decision | <https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5229309213> |
| Source findings | `ME-RP-819-E-007`, `ME-RP-819-E-008` |
| Risk | High governance evidence; one append-only handoff path |

This contract is a narrow successor to the accepted authority-index correction
contract. It completes only the historical implementation handoff after the
index correction succeeded and the first addendum operation failed. It does
not reopen release construction, index correction, validation ownership, or
any R0 observation lane.

The Codex B authoring authority is the current owner-provided reconciliation
handoff directing the work to Codex B. It expires with this Codex B handoff and
creates no implementation, submission, integration, or operational authority.

## Governing Sources

This contract is governed by:

- `AGENTS.md`;
- `docs/agent_rules.yml`;
- `docs/agent_constitution.md`;
- `docs/codex_module_workflow.md`;
- `docs/agent_threads/module_contract.md`;
- `docs/templates/module_contract.md`;
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`;
- issue #819 and tracker #746; and
- the accepted index-correction contract and its independent review.

Issue #819 is the active lane. Issue #769 must remain open with zero comments
and must not be read as a writable coordination surface.

## Finding And First Failure

`ME-RP-819-E-007` is the original incomplete-handoff finding.
`ME-RP-819-E-008` is the blocking contract-review finding that the addendum
serialization was not deterministic because its exact labels, punctuation,
quoting, separators, blank lines, and optional governance blocks were not
frozen.

Observed current state:

1. The two-record release artifact is exact and valid.
2. The corrected authority index is exact and passes the existing semantic
   validator.
3. The original 7437-byte handoff remains a truthful record of the first
   failed index attempt.
4. The handoff is incomplete as the current package handoff because it does
   not record the later successful index correction or the subsequent
   addendum failure.
5. The prior correction decision is permanently spent and cannot authorize a
   handoff-only completion.
6. The failed addendum path assumed `System.Convert.ToHexString`, which is not
   available in the observed Windows PowerShell 5.1 environment.

The smallest lawful successor is one append-only handoff completion using a
PowerShell 5.1-compatible SHA-256 renderer. No release, index, validator, test,
schema, lifecycle, or authority change is required.

## Owning Layer And Truth Boundary

- Internal project area: Role Pool governance and R0 release evidence.
- Truth owner: the exact release JSONL bytes, exact current-authority index
  bytes, and append-only implementation handoff history.
- Bridge-code status: `not_bridge_code`.
- This contract owns documentation and workflow evidence only.
- Passing validation is prerequisite evidence, not mutation, integration,
  observation, advancement, or readiness authority.

## Frozen Read-Only Inputs

### Release artifact

| Property | Required value |
|---|---|
| Path | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` |
| Byte count | `2434` |
| SHA-256 | `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2` |
| Record count | `2` |
| Current tip | `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91` |
| Current rung | `R0` |
| Observation receipts | empty |
| Mutation authorized | `false` |

The release is a hash-bound read-only input. No append, retry, replacement,
truncation, rollback, repair, normalization, or third release event is
authorized.

### Corrected authority index

| Property | Required value |
|---|---|
| Path | `docs/role_pool_current_authority_index.md` |
| Byte count | `17554` |
| SHA-256 | `a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9` |
| Lifecycle rows | `12` |
| Cells per row | `6` |
| Release canonical reference | exactly `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` |
| Mutation authorized | `false` |

The index is a hash-bound read-only input. The accepted IC-01, IC-02, and
IC-03 corrections are historical completed work. No index write, retry,
replacement, repair, or normalization is authorized.

### Historical handoff prefix

| Property | Required value |
|---|---|
| Path | `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md` |
| Byte count | `7437` |
| SHA-256 | `e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5` |
| Required disposition | immutable exact prefix of the completed handoff |

The historical prefix must not be edited, reordered, normalized, regenerated,
or replaced. It remains truthful evidence of the first failed index attempt.

## PowerShell 5.1 SHA-256 Preflight

Before any fresh owner decision is consumed, the future implementer must prove
the exact digest renderer in the same Windows PowerShell process that would
perform the append.

The permitted renderer uses only:

1. `[System.Security.Cryptography.SHA256]::Create()`;
2. `ComputeHash()` over an exact byte array or read-only file stream;
3. `[System.BitConverter]::ToString($digestBytes)`;
4. `.Replace('-', '')`; and
5. `.ToLowerInvariant()`.

`System.Convert.ToHexString`, PowerShell 7-only behavior, external hash tools,
shell fallback, `certutil`, another runtime, package installation, PATH
discovery, and network retrieval are forbidden.

The operation-free known-answer test is:

| Property | Required value |
|---|---|
| Input bytes | ASCII `abc` (`61 62 63`) |
| Expected SHA-256 | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| Required comparison | ordinal lowercase equality |

The SHA-256 object and any opened stream must each receive exactly one dispose
attempt. A KAT mismatch, exception, unavailable member, failed disposal, or
ambiguous result stops before authority consumption.

The same renderer must then read and confirm the frozen release, index, and
historical handoff prefix bindings. A different helper may not be substituted
after the KAT.

The observed Windows PowerShell version `5.1.19041.6456` and absence of
`System.Convert.ToHexString` explain the prior failure. Exact OS build identity
is evidence, not an additional eligibility gate; the KAT and exact input
digests own compatibility for this operation.

## Exact Completion Addendum

The future implementation may append only the instantiated literal byte
template below. The outer four-backtick fence is display-only and is not part
of the template. The template's first byte is LF (`0x0a`), represented by the
empty first displayed line. Every non-final displayed line is followed by one
LF, the final displayed line is also followed by one LF, blank lines contain
zero spaces, and no line has trailing whitespace. The encoding is ASCII, which
is also valid UTF-8. CR bytes and a BOM are forbidden.

The three double-brace tokens are literal placeholders. The
`instruction_context` and `workflow_handoff` blocks shown here are mandatory
template bytes. No optional block, line, field, comment, or separator exists.

````text

## Authority-Index Correction Completion Addendum

- Completion contract path: `docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md`.
- Accepted completion contract SHA-256: `{{ACCEPTED_COMPLETION_CONTRACT_SHA256}}`.
- Independent completion-contract review reference: `{{INDEPENDENT_COMPLETION_CONTRACT_REVIEW_REF}}`.
- Fresh handoff-only owner-decision reference: `{{FRESH_HANDOFF_ONLY_OWNER_DECISION_REF}}`.
- Owner-decision status: `consumed_nonreusable`.
- Frozen release: `byte_count=2434; sha256=fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2`.
- Frozen index: `byte_count=17554; sha256=a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9`.
- Corrected index result: `valid_exact_candidate_frozen_read_only`.
- Historical handoff prefix: `byte_count=7437; sha256=e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5`.
- Prior index-correction decision status: `permanently_spent_nonreusable`.
- Prior addendum result: `powershell_5_1_sha256_renderer_incompatible_no_handoff_bytes_published`.
- SHA-256 KAT result: `passed_exact`.
- Handoff append-call entry count: `1`.
- Implementation result: `handoff_completion_candidate_written_pending_independent_review`.
- Bootstrap/offline validation result: `270 passed`.
- Matching process count: `0`.
- Generated residue count: `0`.
- Authority flags: `implementation_authorized=false; handoff_mutation_authorized=false; release_mutation_authorized=false; release_write_authorized=false; release_append_retry_authorized=false; index_mutation_authorized=false; index_write_authorized=false; observation_authorized=false; task_authorized=false; claim_authorized=false; dispatch_authorized=false; r1_r8_authorized=false; retired_legacy_stage4_authorized=false; submission_authorized=false; merge_authorized=false; deployment_authorized=false; correctness_assurance_claimed=false; security_assurance_claimed=false; privacy_assurance_claimed=false; live_ready=false`.

### Instruction Context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "C"
  risk_tier: "high_governance_evidence"
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
    - "release-state evidence"
    - "current-authority index"
    - "implementation handoff history"
    - "owner single-use authority"
    - "R0-R8 and retired legacy Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #819 remains the active lane; consumed decisions create no continuing authority."
  stop_conditions:
    - "no second append, rewrite, repair, or retry"
    - "release and index remain frozen read-only inputs"
    - "fresh independent Codex E review is required"
```

### Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/819"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md"
  target_artifact: "docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md"
  risk_tier: "high_governance_evidence"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-r0-rebaseline-stage3-819"
  internal_project_area: "Role Pool governance and R0 release evidence"
  truth_owner: "exact release, index, and append-only handoff bytes"
  bridge_code_status: "not_bridge_code"
  completion_contract_sha256: "{{ACCEPTED_COMPLETION_CONTRACT_SHA256}}"
  completion_contract_review_ref: "{{INDEPENDENT_COMPLETION_CONTRACT_REVIEW_REF}}"
  owner_decision_ref: "{{FRESH_HANDOFF_ONLY_OWNER_DECISION_REF}}"
  owner_decision_status: "consumed_nonreusable"
  finding_status:
    ME-RP-819-E-007: "candidate_written_pending_independent_review"
    ME-RP-819-E-008: "exact_literal_serialization_applied_pending_independent_review"
  frozen_release_sha256: "fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2"
  frozen_index_sha256: "a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9"
  starting_handoff_sha256: "e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5"
  sha256_kat_result: "passed_exact"
  focused_validation: "270 passed"
  matching_process_count: 0
  generated_residue_count: 0
  implementation_authorized: false
  handoff_mutation_authorized: false
  release_mutation_authorized: false
  index_mutation_authorized: false
  observation_authorized: false
  task_claim_or_dispatch_authorized: false
  r1_r8_authorized: false
  retired_legacy_stage4_authorized: false
  submission_merge_or_deployment_authorized: false
  correctness_security_privacy_assurance_claimed: false
  live_ready: false
  validation:
    - "PowerShell 5.1 SHA-256 known-answer vector passed exactly"
    - "focused bootstrap and offline validation reported 270 passed"
    - "exact candidate and historical prefix equality require independent review"
  stop_conditions:
    - "do not alter the frozen release or index"
    - "do not retry, repair, replace, or append again"
    - "stop for fresh independent Codex E review"
```
````

Instantiation is deterministic and permits exactly these substitutions:

1. Replace both literal occurrences of
   `{{ACCEPTED_COMPLETION_CONTRACT_SHA256}}` with the accepted contract's exact
   64-character lowercase ASCII hexadecimal SHA-256.
2. Replace both literal occurrences of
   `{{INDEPENDENT_COMPLETION_CONTRACT_REVIEW_REF}}` with the exact public-safe
   ASCII HTTPS reference bound by the accepted independent review and fresh
   owner decision.
3. Replace both literal occurrences of
   `{{FRESH_HANDOFF_ONLY_OWNER_DECISION_REF}}` with the exact public-safe ASCII
   HTTPS reference of the fresh owner decision.

The two references must be nonempty, contain no whitespace, backtick, control
character, query, fragment ambiguity, percent-encoding, or trailing slash, and
must be exact GitHub references inside `Tahjali11/Mythic-Edge`. Replacement is
simultaneous literal byte replacement with no escaping, normalization,
reflow, wrapping, indentation change, or line-ending conversion. Each token
must have exactly two occurrences before replacement and zero afterward. No
other byte may vary. The completed handoff candidate is exactly the immutable
7437-byte prefix followed by this instantiated addendum.

The addendum must not contain a handoff artifact SHA-256 or final handoff byte
count. Embedding either value in the bytes it describes would create a circular
self-binding. The future implementer must compute and report the final
handoff byte count and SHA-256 only after exact readback, outside the handoff
artifact, for independent Codex E verification.

No raw PowerShell error, stack trace, machine-local path, PID, handle, private
value, credential, token, environment value, or temporary artifact may enter
the addendum or public handoff.

## Fresh Handoff-Only Authority

Contract acceptance creates no mutation authority. After independent Codex E
acceptance, the owner must issue one fresh, public-safe, expiring, single-use,
nonreusable decision for this exact handoff-only operation.

The decision must bind:

- issue #819, tracker #746, and protected issue #769;
- exact base commit and tree;
- this contract path and accepted SHA-256;
- independent contract-review reference and digest;
- all three frozen input paths, byte counts, and SHA-256 values;
- the complete literal addendum template, all three exact substitution values,
  the two-occurrence rule for each token, and the permitted renderer;
- the exact SHA-256 KAT vector;
- authorized path count `1`;
- append-call entry limit `1`;
- `single_use=true`;
- `retry_authorized=false`;
- `reuse_authorized=false`;
- `replacement_authorized=false`;
- `release_write_authorized=false`;
- `index_write_authorized=false`; and
- every observation, task, claim, dispatch, R1-R8, retired legacy Stage 4,
  submission, merge, deployment, assurance, and readiness authority as false.

The decision must provide exact issuance and expiry instants and must be
unexpired at consumption. Read-only preflight does not consume it. Consumption
occurs immediately before entry into the sole handoff append call. Every
post-entry outcome is terminal and permanently nonreusable.

The previous decisions ending in issue comments `5228678653` and `5229309213`
remain spent historical evidence and cannot be reused, refreshed, or
reinterpreted.

## Exact Later Implementation Scope

After contract acceptance and fresh owner authority, Codex C may modify
exactly one repository path:

`docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`

The release, index, contracts, tests, validators, source, installed skill,
registry, and every other repository path are read-only inputs.

The implementation sequence is closed:

1. verify repository, branch, issue, contract, review, and owner-decision
   bindings read-only;
2. verify #819 open and #769 open with zero comments;
3. run the exact PowerShell 5.1 SHA-256 KAT;
4. verify the release, index, and handoff-prefix bytes with the same renderer;
5. verify the index semantic invariant and the existing 270-test focused gate;
6. instantiate the literal addendum template by the three permitted
   substitutions only and construct the complete final handoff candidate in
   bounded memory;
7. confirm the candidate preserves the historical handoff as an exact prefix;
8. consume the fresh decision immediately before append-call entry;
9. open the handoff once for exclusive append, append the exact addendum once,
   flush through the file stream, close, and dispose owned objects;
10. read back the complete handoff once;
11. require exact candidate equality and exact prefix equality;
12. compute and report the final byte count and SHA-256 outside the artifact;
13. confirm release and index digests remain frozen; and
14. stop for fresh independent Codex E implementation review.

No staging file, backup, replacement, truncate, rewrite, repair-in-place,
second append, retry, cleanup rewrite, or handoff regeneration is permitted.

## Failure And Unknown-Outcome Behavior

- Any preconsumption drift or failed preflight stops without consuming the
  decision and requires a fresh task after reconciliation.
- Any state after append-call entry permanently spends the decision.
- Open, append, flush, close, dispose, readback, prefix, equality, digest,
  validation, or cleanup uncertainty fails closed.
- Partial or ambiguous append bytes remain untouched for independent review.
- No retry, truncation, rollback, replacement, or second addendum is allowed.
- A handoff failure does not invalidate, rewrite, or revert the frozen release
  or index.
- No success claim is allowed without exact final readback and digest
  verification.

## Preserved Nonclaims And Authority

```yaml
implementation_authorized: false
handoff_mutation_authorized: false
release_mutation_authorized: false
release_append_retry_authorized: false
index_mutation_authorized: false
observation_authorized: false
task_claim_or_dispatch_authorized: false
r1_r8_authorized: false
retired_legacy_stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
correctness_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
live_ready: false
```

These values describe this contract-writing lane. Later handoff mutation
requires the separate accepted review and fresh owner decision above. Exact
release, index, handoff, and validation evidence does not itself create
integration or operational authority.

## Validation

Contract-only validation for Codex B and independent contract review:

```powershell
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B tools\check_protected_surfaces.py --base origin/main
py -3.13 -B tools\check_secret_patterns.py --all
git diff --check
```

The future implementation and independent review must additionally require:

```powershell
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_offline_observation.py
```

Acceptance requires:

- the SHA-256 KAT passes in Windows PowerShell 5.1;
- release remains exactly 2434 bytes at its frozen SHA-256;
- index remains exactly 17554 bytes at its frozen SHA-256;
- the starting 7437-byte handoff is an exact prefix of the final handoff;
- the addendum equals the instantiated literal template byte-for-byte, with
  exactly 18 ordered list fields, both mandatory governance blocks, and no
  optional or extra bytes;
- the focused suite reports `270 passed`;
- final readback equals the preconsumption candidate exactly;
- the final handoff byte count and SHA-256 are externally reported;
- #769 remains open with zero comments;
- matching process count is zero;
- generated residue count is zero; and
- all prohibited authority remains false.

## Stop Conditions

Stop and return to Codex B or the owner if:

- any frozen binding differs;
- any path beyond the handoff requires modification;
- the historical prefix would need editing or normalization;
- the SHA-256 KAT cannot run exactly in Windows PowerShell 5.1;
- final handoff truth would require invented historical details;
- a release, index, test, validator, schema, lifecycle, or authority change is
  required;
- a safety or semantic gate would need weakening;
- #769 has a comment or is not open;
- the fresh owner decision is absent, stale, expired, reused, or ambiguous; or
- a post-consumption outcome cannot be reconciled read-only.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent R0 Handoff Completion Successor Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/819
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md

Use the exact contract SHA-256 from the Codex B handoff. Confirm the release is
frozen at 2434 bytes and SHA-256
fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2,
the corrected index is frozen at 17554 bytes and SHA-256
a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9,
and the historical handoff begins at 7437 bytes and SHA-256
e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5.

Verify ME-RP-819-E-007 and ME-RP-819-E-008 are closed by exactly one future
append-only handoff path with no release or index write. Reconstruct the exact
literal addendum bytes from the frozen template and the three substitution
values; confirm both mandatory governance blocks and prove no optional bytes
remain. Verify the PowerShell 5.1 SHA-256 renderer and ASCII abc known-answer
vector, exact prefix preservation, nonretry lifecycle, fresh owner-decision
boundary, external final-artifact digest ownership, and all false authority
fields.

Do not edit any file, construct or consume authority, append the handoff,
mutate release or index bytes, comment on issue #769, run an observation,
submit, merge, deploy, advance R0-R8 or retired legacy Stage 4, or claim
readiness. Lead with findings and route an accepted contract to a separate
owner handoff-only implementation decision.
```

## Instruction Context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high_governance_evidence"
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
    - "release-state evidence"
    - "current-authority index"
    - "implementation handoff history"
    - "owner single-use authority"
    - "R0-R8 and retired legacy Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #819 remains the active lane; prior decisions are spent and create no successor authority."
  stop_conditions:
    - "more than the one handoff path requires an edit"
    - "release or index bytes would change"
    - "historical prefix would be rewritten"
    - "PowerShell 5.1 SHA-256 KAT is not exact"
    - "fresh owner authority is absent or ambiguous"
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
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_handoff_completion_successor.md"
  risk_tier: "high_governance_evidence"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-r0-rebaseline-stage3-819"
  internal_project_area: "Role Pool governance and R0 release evidence"
  truth_owner: "exact release, index, and append-only handoff bytes"
  bridge_code_status: "not_bridge_code"
  finding_status:
    ME-RP-819-E-007: "contracted_pending_independent_review"
    ME-RP-819-E-008: "exact_literal_serialization_closed_pending_independent_review"
  frozen_release_sha256: "fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2"
  frozen_index_sha256: "a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9"
  starting_handoff_sha256: "e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5"
  later_implementation_scope:
    - "docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md"
  prior_decision_status: "permanently_spent_nonreusable"
  implementation_authorized: false
  handoff_mutation_authorized: false
  release_mutation_authorized: false
  index_mutation_authorized: false
  observation_authorized: false
  r1_r8_authorized: false
  retired_legacy_stage4_authorized: false
  live_ready: false
  validation:
    - "PowerShell 5.1 SHA-256 known-answer vector contractually closed"
    - "contract documentation and safety checks required"
  stop_conditions:
    - "any second implementation path is required"
    - "release or index bytes drift"
    - "historical handoff prefix cannot remain exact"
    - "fresh owner decision is absent"
```
