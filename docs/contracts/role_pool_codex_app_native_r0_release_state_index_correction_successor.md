# App-Native R0 Release-State Authority-Index Correction Successor Contract

## Contract Status

| Field | Value |
| --- | --- |
| Repository | `Tahjali11/Mythic-Edge` |
| Issue | [#819](https://github.com/Tahjali11/Mythic-Edge/issues/819) |
| Parent | [#813](https://github.com/Tahjali11/Mythic-Edge/issues/813) |
| Tracker | [#746](https://github.com/Tahjali11/Mythic-Edge/issues/746) |
| Protected issue | [#769](https://github.com/Tahjali11/Mythic-Edge/issues/769) |
| Reviewed base commit | `8470dd10c91faa02d923fe5d67246fcf280095cb` |
| Reviewed base tree | `5f2d6df830047130671f8ca44804ccb17149e99b` |
| Owning predecessor contract | `docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md` |
| Predecessor contract SHA-256 | `49c9adf44a78b46f4713a9e41f2b6f1b093b17f0a42c445436c30da039526058` |
| Risk | High governance evidence; index and handoff correction only |
| Implementation authorized | `false` |
| Release mutation authorized | `false` |

This additive successor governs only the correction of the failed
authority-index portion of one already completed release attempt. It does not
rewrite the predecessor contract, reopen release construction, or authorize a
release append, retry, replacement, truncation, rollback, or normalization.

## Findings And First Failure

The release append completed exactly. The authority-index operation did not.

1. The current index readback differs from its precomputed candidate at byte
   offset `415`: the observed byte is LF (`0x0a`) and the intended byte is a
   space (`0x20`). Replacing only that byte reproduces the precomputed index
   SHA-256. This is formatting drift.
2. The `trusted_owner_release_state` row has a semantic defect independent of
   that formatting drift. Its `canonical_reference` cell contains the release
   path, contract, review and decision comments, and implementation handoff.
   The existing frozen invariant requires exactly the release JSONL path.
3. Finding `ME-RP-819-E-006`: the same row's
   `authority_effect_or_explicit_non_effect` cell uses different wording from
   the two phrases required by the existing frozen semantic invariant. This
   defect remains after the formatting and canonical-reference corrections.
4. The original implementation handoff truthfully records the release success,
   index failure, stopped validation, and spent authority. Its initial history
   must remain unchanged.

Formatting normalization and canonical-reference correction alone leave the
authority-effect semantic defect. The smallest lawful repair is one exact
three-correction index candidate plus one append-only handoff correction
addendum.

## Immutable Release Input

The release artifact is a read-only input to this contract:

| Binding | Exact value |
| --- | --- |
| Path | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` |
| Record count | `2` |
| Byte count | `2434` |
| Complete SHA-256 | `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2` |
| Immutable first-line byte count | `981` |
| Immutable first-line SHA-256 | `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9` |
| Second-line byte count | `1453` |
| Second-line SHA-256 | `cabd911f9e89ba0a3db35defd4aa70ee1a2af0aa554e02481da0fd5c7c30a09e` |
| Current tip | `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91` |
| Current rung | `R0` |
| Observation receipts | Exactly `[]` |

Existing record, chain, current-tip, current-rung, and R0-ceiling validators
must return no errors before and after the correction. The complete release
bytes and every release-derived value above must remain unchanged.

No role acting under this contract may open the release path for writing,
append a line, reuse the spent record ID, consume the spent decision again,
create a successor release event, or repair release content.

## Starting Correction Inputs

### Authority index

- Path: `docs/role_pool_current_authority_index.md`.
- Starting byte count: `17925`.
- Starting SHA-256:
  `c8c34b54265f803787b4f45f40b2777ebdb9cb4cc51940a2af2e8c4586e8e960`.
- Precomputed formatting-only candidate SHA-256:
  `d3a6b1ac51a6dfe01f7ec352b15c5ab47b19fc4fa7af9f5b6595022c3bf427fd`.

The formatting-only candidate is diagnostic evidence, not an acceptable final
artifact.

### Implementation handoff

- Path:
  `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`.
- Starting byte count: `7437`.
- Starting SHA-256:
  `e75d5f5c74347dcc957b7e24ccfcc1bb353d7b47801d2074a2496400bf8de4d5`.

The complete starting handoff is immutable history and must remain an exact
byte prefix of the corrected handoff.

### Consumed authority

- Prior owner decision:
  <https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228678653>.
- Status: `permanently_spent_nonreusable`.
- Append-call entries: `1`.

The prior decision and record identity are evidence only. They create no
correction, submission, integration, observation, or retry authority.

## Exact Final Index Candidate

The final index candidate is derived from the exact starting index through
exactly three changes in the same file.

### IC-01: prose-wrap correction

Require byte offset `415` to be LF and require its bounded surrounding ASCII
text to be:

```text
full binding, a candidate two-line R0
offline-only release state
```

Replace that one LF with one ASCII space. The bounded text becomes:

```text
full binding, a candidate two-line R0 offline-only release state
```

No other prose wrapping or whitespace may change.

### IC-02: canonical-reference ownership correction

In the sole six-cell row whose first cell is
`trusted_owner_release_state`, replace the exact 403-character
`canonical_reference` cell:

```text
`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`<br>`docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228654366><br><https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228678653><br>`docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`
```

with exactly this 60-character cell:

```text
`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`
```

The contract, review, owner-decision, and handoff references remain available
in their owning evidence rows and surrounding index prose. They must not be
moved into another canonical-reference cell as compensation.

### IC-03: authority-effect semantic correction

In that same `trusted_owner_release_state` row, replace the exact 158-character
text in the `authority_effect_or_explicit_non_effect` cell:

```text
R0 remains offline validation only and creates no observation, process, task, claim, command, dispatch, R1-R8, retired legacy Stage 4, or readiness authority.
```

with exactly this 130-character text:

```text
R0 permits offline validation only and creates no process, task, claim, command, dispatch, R1-R8, Stage-4, or readiness authority.
```

No other text in that cell may change. Observation authority remains false
under this contract and the owning release-state authority; IC-03 does not
create, remove, or alter an observation receipt or authority flag.

### Final binding

After IC-01, IC-02, and IC-03:

- byte count: `17554`;
- SHA-256:
  `a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9`;
- encoding: ASCII;
- CR byte count: `0`;
- final LF count: exactly one terminal LF;
- authority/lifecycle table row count: `12`;
- cells per row: `6`;
- `trusted_owner_release_state` row count: `1`; and
- its first four cells are exactly:

```text
`trusted_owner_release_state`
`current_normative_authority`
`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`
`active_r0_offline_only_release_state`
```

The refresh-trigger cell remains byte-exact. The authority-effect cell changes
only through IC-03.

Any different byte count, digest, occurrence count, row count, cell count,
canonical reference, or additional changed byte is a hard stop.

## Handoff Correction Addendum

Only after exact final index readback may the implementation append one
`## Correction Addendum` section to the existing handoff. It must not edit,
delete, reflow, relabel, or contradict any byte in the starting 7437-byte
handoff.

The addendum must record, in this order:

1. this successor contract path and accepted SHA-256;
2. the independent Codex E contract-review reference and digest;
3. the fresh owner correction-decision reference, issuance, expiry,
   consumption instant, and terminal nonreuse status;
4. the preserved release path, byte count, complete digest, current tip, rung,
   and zero-observation state;
5. the starting, formatting-only, and final index byte counts and digests;
6. IC-01, IC-02, and IC-03 as the only index changes;
7. exact final index readback and semantic-validation results;
8. the original failure history as preserved and not erased;
9. validation command-result evidence;
10. generated-residue and process counts; and
11. every operational, observation, R1-R8, retired legacy Stage 4, submission,
    merge, deployment, and readiness authority flag.

The addendum may report successful correction only after exact index readback
and all in-scope validation pass. If index publication or readback is failed or
ambiguous, the addendum must report that truthful terminal result instead.

## Fresh Correction Authority

Contract acceptance creates no mutation authority. A separate fresh,
public-safe, expiring, single-use owner decision is required after independent
Codex E accepts this exact contract.

That decision must bind:

- exact base commit and tree;
- this contract path and accepted SHA-256;
- independent contract-review reference and digest;
- immutable release byte count, digest, and current tip;
- starting and final index byte counts and digests;
- starting handoff byte count and digest;
- exactly two implementation paths;
- IC-01, IC-02, and IC-03;
- one index-write entry and one handoff-addendum write entry;
- `single_use=true`;
- `reuse_authorized=false`;
- `release_write_authorized=false`; and
- every observation, task, claim, dispatch, R1-R8, retired legacy Stage 4,
  submission, merge, deployment, and readiness authority false.

Read-only preflight does not consume the decision. The decision becomes
permanently spent immediately before the first index-write entry. Every
post-entry result is nonreusable, including failed write, partial write, failed
flush, failed close, failed readback, semantic failure, handoff failure, or
unknown outcome. No retry or replacement is authorized.

## Exact Later Implementation Scope

After contract acceptance and fresh owner correction authority, Codex C may
change exactly:

1. `docs/role_pool_current_authority_index.md`; and
2. `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`.

The release file is an exact read-only prerequisite, not an implementation
path. No third path is permitted.

Implementation order:

1. revalidate all exact starting bindings and #769's zero-comment state;
2. construct the complete final index candidate in bounded memory;
3. parse its table and run the semantic invariant in memory;
4. construct the handoff addendum in bounded memory;
5. consume the fresh correction decision immediately before index-write entry;
6. write, flush, close, and read back the index once;
7. require exact equality with the 17554-byte candidate and exact SHA-256;
8. rerun the index semantic invariant and release validations;
9. append, flush, close, and exactly read back the handoff addendum; and
10. stop for independent Codex E implementation review.

Do not stage, commit, push, submit, merge, or integrate under the correction
decision.

## Failure And Nonretry Behavior

- Starting-byte, release-byte, issue-state, or contract drift stops before
  consumption.
- A stale or changed index, handoff, release, base, review, or owner decision
  stops before mutation.
- Any state after index-write entry is terminal and nonreusable.
- Failed or ambiguous index readback leaves the observed bytes untouched and
  routes to read-only reconciliation.
- Handoff failure after exact index correction does not invalidate or revert
  the index and does not permit another index write.
- No automatic repair, retry, rollback, replacement, cleanup of ambiguous
  bytes, release mutation, third path, or new lifecycle event is permitted.

## Preserved Behavior And Nonclaims

This contract must not change:

- release bytes, records, chain, current tip, current rung, or release schema;
- stable validator-bundle bytes or algorithm;
- source, installed tree, registry, profile, checker, observer, or launcher;
- test files, KATs, selectors, lifecycle states, no-echo rules, effects, or
  false authority fields;
- issue #769 or its zero-comment rule; or
- historical failure and authority-consumption evidence.

```yaml
implementation_authorized: false
release_mutation_authorized: false
release_append_retry_authorized: false
index_mutation_authorized: false
handoff_mutation_authorized: false
observation_authorized: false
task_claim_or_dispatch_authorized: false
r0_r8_advancement_authorized: false
retired_legacy_stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
live_ready: false
```

The valid release candidate remains candidate evidence until corrected index
and handoff bytes receive independent implementation acceptance and separately
approved integration. Neither the release candidate nor this contract alone is
current integrated release authority.

## Validation

Future implementation and independent review must run:

```powershell
py -3.13 -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_offline_observation.py
py -3.13 -B -m pytest -q tests\test_run_role_pool_r0_trusted_launch_observer.py
py -3.13 -B -m pytest -q docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py -k "release"
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B tools\check_protected_surfaces.py --base origin/main
py -3.13 -B tools\check_secret_patterns.py --all
git diff --check
```

Acceptance requires:

- bootstrap and offline-observation modules report `270 passed`;
- the authority-index semantic assertion passes;
- independent release record, chain, current-tip, and R0-ceiling validation
  passes;
- trusted-launch-observer tests remain passing;
- the release artifact remains exactly 2434 bytes with SHA-256
  `fff6025b...b125f2`;
- the final index is exactly 17554 bytes with SHA-256
  `a04fee4d...10b9`;
- the starting handoff is an exact prefix of the final handoff;
- protected/private scans report zero forbidden findings and zero warnings;
- #769 remains open with zero comments;
- matching process count is zero; and
- generated residue count is zero.

Run the full repository suite only after focused validation. Classify the
known analytics failure separately if it remains exact. It does not authorize
another #819 path and cannot waive an in-scope failure.

## Stop Conditions

Stop and return to Codex B if:

- any exact starting or final binding differs;
- the final index cannot be produced by IC-01, IC-02, and IC-03 only;
- any path beyond the index and handoff requires an edit;
- release, test, validator, schema, lifecycle, or authority behavior would
  change;
- a safety or semantic test would need weakening;
- the fresh owner decision does not bind this exact correction; or
- uncertain state cannot be reconciled read-only.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent R0 Authority-Index Correction Successor Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/819
Branch: codex/role-pool-r0-rebaseline-stage3-819

Review only:
docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md

Use the exact contract SHA-256 from the Codex B handoff. Verify the reviewed
base commit/tree, predecessor stable-reconstruction contract, exact existing
release/index/handoff bytes, spent owner decision, and the independent
reconciliation findings.

Independently derive the exact three-change index candidate: byte 415 LF to
space, then the trusted_owner_release_state canonical-reference cell reduced
from the exact 403-character multi-reference value to only the exact
60-character release JSONL path, then the same row's authority-effect wording
changed from the exact 158-character old text to the exact 130-character text
containing both frozen required phrases. Require final index 17554 bytes and
SHA-256
a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9.
Confirm the release remains immutable at 2434 bytes and SHA-256
fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2.

Confirm the later implementation scope is exactly the index and append-only
handoff addendum, with fresh owner authority required before mutation. Do not
edit the release, index, handoff, tests, validators, GitHub, or issue #769. Do
not construct or consume authority, implement, submit, merge, run an
observation, advance R0-R8 or retired legacy Stage 4, or claim readiness.
Lead with findings and state whether one exact owner correction decision is
eligible after contract acceptance.
```

## Instruction Context

```yaml
instruction_context:
  role: "B"
  risk_tier: "high"
  authority_sources_read:
    - "AGENTS.md"
    - "docs/agent_rules.yml"
    - "docs/agent_constitution.md"
    - "docs/codex_module_workflow.md"
    - "docs/agent_threads/module_contract.md"
    - "docs/templates/module_contract.md"
    - "issue #819"
    - "stable-reconstruction predecessor contract"
    - "Codex C implementation handoff"
    - "fresh Codex E release/index reconciliation"
  protected_surfaces:
    - "release-state authority"
    - "current-authority index"
    - "owner single-use decision"
    - "issue #769 zero-comment state"
    - "R0-R8 and retired legacy Stage 4 authority"
  authority_conflicts_found: false
  stop_conditions:
    - "release bytes would change"
    - "more than index and handoff require edits"
    - "historical failure or spent authority would be rewritten"
    - "schema, lifecycle, validator, test, or operational behavior would change"
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
  source_finding: "ME-RP-819-E-006"
  source_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_index_correction_successor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "codex/role-pool-r0-rebaseline-stage3-819"
  branch: "codex/role-pool-r0-rebaseline-stage3-819"
  release_result: "valid_exact_candidate_preserve_unchanged"
  release_artifact_sha256: "fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2"
  starting_index_sha256: "c8c34b54265f803787b4f45f40b2777ebdb9cb4cc51940a2af2e8c4586e8e960"
  final_index_sha256: "a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9"
  later_implementation_scope:
    - "docs/role_pool_current_authority_index.md"
    - "docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md"
  prior_owner_decision_status: "permanently_spent_nonreusable"
  implementation_authorized: false
  release_mutation_authorized: false
  observation_authorized: false
  r0_r8_authorized: false
  retired_legacy_stage4_authorized: false
  live_ready: false
  validation:
    - "exact index candidate derived in memory"
    - "release candidate independently preserved"
    - "contract structural and safety validation required"
  stop_conditions:
    - "release change"
    - "third implementation path"
    - "historical rewrite or authority reuse"
  next_recommended_role: "Codex E: independent index-correction successor contract reviewer"
```
