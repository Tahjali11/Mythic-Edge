# App-Native R0 Release-State Rebaseline Contract

## Contract Status

| Field | Value |
| --- | --- |
| Repository | `Tahjali11/Mythic-Edge` |
| Issue | [#819](https://github.com/Tahjali11/Mythic-Edge/issues/819) |
| Parent | [#813](https://github.com/Tahjali11/Mythic-Edge/issues/813) |
| Tracker | [#746](https://github.com/Tahjali11/Mythic-Edge/issues/746) |
| Protected issue | [#769](https://github.com/Tahjali11/Mythic-Edge/issues/769) |
| Contract version | `role_pool_codex_app_native_r0_release_state_rebaseline.v1` |
| Risk tier | `High` |
| Implementation authorized | `false` |
| Release append authorized | `false` |
| Observation authorized | `false` |
| R0-R8 advancement authorized | `false` |
| Stage 4 authorized | `false` |
| Live ready | `false` |

This task-specific contract defines one future append-only R0 rebaseline. It
does not append the release line, consume an owner decision, refresh the index,
or grant release authority.

## Decision And Scope

The current Role Pool source and installed copy are exact for the app-native
successor, but the sole release-state record still owns the predecessor tuple.
The existing R0 checker therefore truthfully returns
`blocked_release_state_conflict`.

The smallest correction is exactly one
`trusted_owner_native_release_rebaseline_record.v1` line appended to the
existing release file. This contract references the accepted profile's
19-field schema, canonicalization, self-digest, chain, current-tip, and R0
ceiling rules. It creates no schema, validator family, persistent writer,
scheduler, second release file, observation framework, or broader lifecycle.

## Exact Current Bindings

All values below were revalidated at
`origin/main@2d87be45b7cd4887fe79ed41c6fe4748afa1f8e0`.

| Binding | Exact value |
| --- | --- |
| Accepted successor profile | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| App-native binding/sync contract | `docs/contracts/role_pool_codex_app_native_r0_binding_and_sync_successor.md`, SHA-256 `ef440f1fe4ce9b0fd342057864e41cbdef93c1ac12ea85a1f9d01912eec4cd02` |
| Successor source and installed tree | 43 nodes, 38 files, 6840 canonical bytes, SHA-256 `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| Registry artifact | `docs/role_pool/trusted_owner_repository_registry.v1.json`, 1478 bytes, artifact SHA-256 `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |
| Registry self-digest | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Successor validator bundle | `c344058dfc2738d891cd63f67411203aac56073c824b3f3de14b992498972e5d` |
| Current release artifact | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, 981 bytes, SHA-256 `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9` |
| Current release tip | `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| Current authority index | `docs/role_pool_current_authority_index.md`, SHA-256 `2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0` |
| Current R0 evidence packet | self-digest `2c49dc45c7ab46ea332a8e4ac200847a37391f60a5c0e1476be07bc1667de2f6`; terminal `blocked_release_state_conflict` |

The registry remains Core-only, role `A`, operation `offline_validation`, read
scope `docs`, with no mutation scope, approved command, or code-execution
authority. Issue #769 is open with zero comments and must remain untouched.

## Immutable Predecessor

The existing 981-byte artifact contains exactly one LF-terminated
`trusted_owner_native_release_record.v1` bootstrap line. Its binding tuple is:

| Field | Exact predecessor value |
| --- | --- |
| `record_sha256` | `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| `contract_sha256` | `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| `skill_tree_sha256` | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| `registry_sha256` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| `validator_bundle_sha256` | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| `to_rung` | `R0` |
| `observation_receipt_sha256s` | `[]` |
| `accepted_at_utc` | `2026-07-31T11:09:36Z` |

The existing bytes, line order, fields, references, self-digest, and final LF
are immutable. The future implementation may append after byte 981 only. It
must not rewrite, normalize, replace, truncate, repair, or relabel the
historical line.

## Exact Successor Projection

The future line must use the exact 19-field order and validation rules already
defined under `R0 Current-Profile Rebaseline` in the accepted profile.
This contract fixes every non-fresh field as follows:

| Field | Required value |
| --- | --- |
| `schema_version` | `trusted_owner_native_release_rebaseline_record.v1` |
| `record_id` | One fresh globally unique `r0.rebaseline.*` identity generated only after owner authorization |
| `predecessor_record_sha256` | `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| `from_rung` | `R0` |
| `to_rung` | `R0` |
| `predecessor_contract_sha256` | `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| `contract_sha256` | `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| `predecessor_skill_tree_sha256` | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| `skill_tree_sha256` | `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| `predecessor_registry_sha256` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| `registry_sha256` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| `predecessor_validator_bundle_sha256` | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| `validator_bundle_sha256` | `c344058dfc2738d891cd63f67411203aac56073c824b3f3de14b992498972e5d` |
| `observation_receipt_sha256s` | Exactly `[]` |
| `codex_e_review_ref` | Exact fresh post-integration tuple-review public reference |
| `codex_e_review_sha256` | SHA-256 of that exact public-safe review artifact |
| `owner_decision_ref` | Exact fresh owner-decision public reference |
| `accepted_at_utc` | Fresh whole-second UTC construction instant, later than the predecessor and not later than owner-decision expiry |
| `record_sha256` | Existing canonical release self-digest over the first 18 fields |

No fresh value is selected by Codex B. The existing profile KAT remains the
only schema KAT; this contract does not create another vector or digest family.

## Fresh Codex E Eligibility Review

After this contract and its independent contract review are accepted and
integrated, a separate fresh Codex E review must inspect the then-current
public state and produce one immutable public-safe review artifact. The review
must bind:

1. this exact integrated task contract and its accepted contract review;
2. the exact predecessor release artifact, line, tip, and R0 state;
3. the exact successor profile, source tree, installed tree, registry, and
   validator bundle shown above;
4. exact source/install equality and an ordinary, non-reparse fixed release
   path and parent;
5. no accepted successor-profile R0 observation and no prior rebaseline;
6. issue #769 open with zero comments;
7. the exact three-file future implementation scope;
8. reuse of the existing record, chain, self-digest, and current-tip
   validators; and
9. all operational and readiness authority remaining false.

Its public reference and exact artifact SHA-256 become the two `codex_e_review`
fields. A contract-review report from this B lane, an older review, a draft,
or an unintegrated artifact is not eligible.

## Fresh Owner Decision

Only after the exact eligibility review exists may the owner publish one
public issue #819 decision. The decision must be owner-authored, unedited,
unexpired, and bound to:

- this integrated contract and accepted review;
- the eligibility reference and artifact SHA-256;
- the exact predecessor and successor tuples;
- the fixed release path and exact three-file implementation scope;
- one append attempt, one fresh `r0.rebaseline.*` record ID, and no retry;
- an exact creation time and expiry time; and
- `single_use=true`, `reuse_authorized=false`, R0-to-R0 only, with every
  observation, task, claim, dispatch, R1-R8, Stage 4, merge, deployment, and
  readiness authority false.

The owner-decision body SHA-256 must be recomputed from the exact GitHub body
and recorded in the index and implementation handoff. The release event uses
only its public URL because the accepted 19-field schema has no owner-decision
digest field. This contract must not add one.

Read-only preflight does not consume the decision. The decision becomes
permanently nonreusable immediately before entry into the sole append call.
Every result after that boundary is spent, including known failure, collision,
partial append, unknown write state, failed readback, failed index refresh, or
failed handoff creation. No role may revive or replace it.

## Pre-Append Preconditions

Future Codex C must stop before consumption unless all of these are exact:

1. current `origin/main`, issue #819, tracker #746, and accepted artifacts;
2. the fresh eligibility review and owner decision, including expiry;
3. the three current target files at their expected starting bytes;
4. the release file is an ordinary non-reparse file in its exact ordinary
   non-reparse parent and is exactly the 981-byte predecessor artifact;
5. strict parsing yields exactly one valid bootstrap record and exact current
   tip `78bff761...e4a9ba7`;
6. no duplicate record ID, owner decision, successor, rebaseline, fork, or
   accepted successor-profile observation exists;
7. source and installed trees remain exact and equal at the successor digest;
8. registry and validator bindings remain exact;
9. issue #769 remains open with zero comments;
10. the complete candidate line, resulting two-line bytes, resulting artifact
    SHA-256, authority-index bytes, and comparison-handoff plan validate in
    bounded memory; and
11. no fourth repository path, code edit, validator edit, observation, task,
    network operation, package action, or unrelated worktree change is needed.

Any pre-consumption failure leaves the decision unconsumed. Missing,
contradictory, unreadable, stale, forked, or unsafe state selects the existing
fail-closed release-state-invalid route. Do not infer replacement values.

## One Append And Exact Readback

No persistent writer is introduced. The later implementation may use one
bounded direct operation against the fixed release file, with exclusive access
that prevents another writer during the final tip check and append.

The ordered operation is:

1. acquire exclusive access to the exact fixed file without following a
   reparse point;
2. reread and revalidate the exact 981-byte predecessor and current tip while
   exclusive access is held;
3. permanently consume the fresh owner decision immediately before entering
   the one append call;
4. append exactly one prevalidated canonical LF-terminated line at byte 981;
5. flush, synchronize, and close every owned handle;
6. reopen the fixed file read-only and read it once to completion;
7. require exact equality with the precomputed two-line candidate bytes and
   exact complete artifact SHA-256;
8. strictly parse exactly two lines and require the existing record and chain
   validators to return no errors;
9. require the second record self-digest to be the current tip, current rung to
   remain `R0`, and its four successor values to be the current binding tuple;
10. only after exact release readback, write and exactly read back the frozen
    authority-index refresh; and
11. write the exact comparison handoff last.

No truncation, replacement, temporary release file, rename, overwrite,
historical-line rewrite, second append, second record, automatic retry,
rollback, repair in place, or cleanup of uncertain release bytes is allowed.

## Stale, Collision, Fork, And Unknown Outcomes

- A changed tip, altered 981-byte artifact, existing second line, duplicate
  record ID, prior use of the owner decision, or competing successor observed
  before consumption stops without append.
- A change discovered after exclusive access but before append stops before
  consumption when the append call has not been entered.
- Any state in which append entry or byte publication may have occurred is
  permanently nonreusable and requires read-only reconciliation.
- Exact predecessor-only bytes after a known append failure are a failed spent
  attempt. They do not authorize retry.
- Exact two-line candidate bytes after reported success or an unknown call are
  a candidate result that may continue to index refresh and independent review.
- A partial line, additional line, different second line, unreadable file,
  changed predecessor, or any other uncertain bytes select
  `unknown_outcome_reconciliation_required`. Preserve the file unchanged.
- A valid but different successor is a fork or collision and selects the
  existing fail-closed release-state-invalid route. Do not choose a winner.
- Index or handoff failure after an exact append does not invalidate or remove
  the release bytes. It blocks acceptance and routes to reconciliation without
  another append.

Later reconciliation is read-only against the same record ID, decision, and
candidate bytes. It cannot create, append, replace, repair, or retry.

## Current-Authority Index Refresh

The same future package must preserve the index's authority precedence,
six-column family table, stale-entry behavior, manual-refresh rule, immutable
history, Security references, and no-authority statement.

It must update only facts mechanically made stale by the integrated app-native
source/sync package and this exact rebaseline candidate, including:

- current base and refresh date;
- accepted successor profile and source/install tree tuple;
- current registry and validator bindings;
- this contract and accepted contract review;
- fresh eligibility-review reference and artifact SHA-256;
- owner-decision reference and exact-body SHA-256;
- predecessor and new release-tip self-digests;
- complete two-line release artifact SHA-256;
- the comparison handoff; and
- the truthful R0 offline-only authority ceiling.

Historical bootstrap, predecessor, synchronization, and observation artifacts
remain historical. The index must not relabel them as app-native successor
observations or claim R1, task, dispatch, Stage 4, or readiness authority.

## Exact Later Implementation Scope

After contract integration, fresh eligibility review, and fresh owner
authorization, Codex C may change exactly these three paths:

1. `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`;
2. `docs/role_pool_current_authority_index.md`; and
3. `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`.

No implementation, test, validator, profile, registry, installed-skill,
workflow, issue, or fourth repository path is permitted. The handoff must
record the exact pre/post hashes, record self-digest, release artifact digest,
review and owner references, owner body digest, accepted time, first failing
boundary if any, decision disposition, readback result, index result, changed
paths, residue, and all false authority flags.

If these three paths and existing validators are insufficient, stop and route
to Codex B. Do not widen the implementation envelope during C or D.

## Validation Requirements

Contract review must independently:

1. recompute every current artifact and tuple binding in this contract;
2. reproduce the 981-byte historical artifact and exact first-line digest;
3. run the existing record, rebaseline, and chain validator tests;
4. prove a valid synthetic two-line chain selects the second line as tip and
   keeps the current rung at R0;
5. test stale predecessor, changed tuple, duplicate ID, second rebaseline,
   fork, partial line, extra line, missing LF, CRLF, and digest mismatch;
6. verify the R0 checker currently returns only
   `blocked_release_state_conflict` with all effect counts zero and all
   authority flags false;
7. verify issue #769 remains open with zero comments;
8. run agent-doc, diff, protected-surface, secret/private-marker, process, and
   generated-residue checks; and
9. confirm this contract is the only changed path.

Future implementation and review must additionally validate the exact dynamic
line, two-line artifact, one-call append/readback behavior, current-tip
selection, index refresh, three-path scope, and nonretry outcomes without
running an observation or task.

## Acceptance And Routing

1. Fresh Codex E reviews this exact contract first.
2. Contract acceptance permits only separately authorized Codex F/G
   contract integration.
3. After integration, a fresh Codex E exact-tuple eligibility review is
   required.
4. The owner may then create one exact expiring nonreusable decision.
5. Codex C may perform only the three-path attempt under that decision.
6. Fresh Codex E reviews exact result bytes and evidence.
7. Codex F/G integration requires separate authority.

Contract acceptance, eligibility, owner decision, candidate creation,
implementation review, and integration are distinct. None alone advances a
rung or establishes readiness.

## R0 Ceiling And Non-Claims

The historical bootstrap remains immutable. A valid rebaseline keeps
`from_rung=R0`, `to_rung=R0`, and `observation_receipt_sha256s=[]`. It changes
only the current binding tuple. It is not Observation 1 or 2 and does not
advance to R1.

```yaml
implementation_authorized: false
release_append_authorized: false
authority_index_mutation_authorized: false
owner_decision_created_or_consumed: false
observation_authorized: false
task_or_claim_authorized: false
dispatch_authorized: false
registry_mutation_authorized: false
installed_skill_mutation_authorized: false
r0_r8_advancement_authorized: false
stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
security_assurance_claimed: false
privacy_assurance_claimed: false
live_ready: false
```

This contract does not claim live compatibility, successful future append,
observation acceptance, task creation, dispatch safety, security, privacy,
correctness, deployment readiness, or global Role Pool readiness.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Independent App-Native R0 Release-State Rebaseline Contract
Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/819

Parent:
https://github.com/Tahjali11/Mythic-Edge/issues/813

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Protected issue:
https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_codex_app_native_r0_release_state_rebaseline.md

Use the exact contract SHA-256 from the Codex B handoff. Refresh origin/main,
issue and PR state, accepted governance, the profile, release artifact,
registry, current authority index, source/install trees, validator bundle, and
R0 checker evidence.

Verify the exact predecessor and successor tuples, immutable 981-byte bootstrap
line, reuse of the accepted 19-field rebaseline schema, fresh post-integration
E eligibility boundary, separate expiring nonreusable owner decision, one
append with exact two-line readback, stale-tip/collision/fork/unknown-write
handling, no retry or rollback, exact index refresh, three-file future scope,
and R0 offline-only ceiling.

Run the contract-required release-record, chain, R0 checker, agent-doc,
protected-surface, private-marker, process, and residue validation. Confirm
issue #769 remains open with zero comments and this contract is the only
changed path.

Do not append release state, consume authority, edit the index, implement,
synchronize, create a task, claim, or observation, mutate #769, advance R0-R8
or Stage 4, submit, merge, deploy, or claim readiness. Lead with findings.
Contract acceptance routes only to separately authorized contract submission
and integration, not directly to eligibility review or Codex C.
```

## Instruction Context

```yaml
instruction_context:
  role: "B"
  risk_tier: "High"
  repository_authority_read: true
  issue_and_tracker_read: true
  accepted_adrs_read:
    - "ADR-0008"
    - "ADR-0012"
  protected_surfaces:
    - "release-state authority"
    - "current-authority index"
    - "owner single-use decision"
    - "issue #769 zero-comment state"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "Owner activation is exact for this one docs-only path; PRs #374 and #391 are disjoint."
  stop_conditions:
    - "binding or current-tip drift"
    - "issue #769 receives a comment"
    - "need for a new schema, validator, writer, status, or fourth implementation path"
    - "any implementation or release mutation in this B lane"
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: App-Native R0 Release-State Rebaseline Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/819"
  parent: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "B"
  next_thread: "E"
  base: "2d87be45b7cd4887fe79ed41c6fe4748afa1f8e0"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_rebaseline.md"
  verdict: "contract_ready_for_independent_review_only"
  predecessor_release_artifact_sha256: "723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9"
  predecessor_tip_sha256: "78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7"
  successor_profile_sha256: "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
  successor_tree_sha256: "3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6"
  successor_registry_sha256: "93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7"
  successor_validator_bundle_sha256: "c344058dfc2738d891cd63f67411203aac56073c824b3f3de14b992498972e5d"
  future_implementation_path_count: 3
  owner_decision_created_or_consumed: false
  release_append_authorized: false
  implementation_authorized: false
  observation_authorized: false
  r0_r8_advancement_authorized: false
  stage4_authorized: false
  live_ready: false
  issue_769_comment_count: 0
  next_recommended_role: "Codex E: independent rebaseline contract reviewer"
```
