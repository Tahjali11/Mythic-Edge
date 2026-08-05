# Contract Test Report: Direct App-Native Trusted-Owner Task Contract

`report_lifecycle: contract_clarification_review`

`contract_verdict: accepted_exact_direct_app_native_contract_for_inert_implementation`

## Review Scope

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/813>
- Branch: `codex/role-pool-app-native-direct-task-contract-813`
- Base: `c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`
- Profile contract:
  `docs/contracts/trusted_owner_native_role_pool_profile.md`
- Companion contract:
  `docs/contracts/role_pool_codex_app_native_direct_task_adapter.md`
- Review authority: `docs/agent_constitution.md`,
  `docs/agent_threads/contract_test.md`, and
  `docs/templates/contract_test_report.md`

This was a contract-only review. No implementation, task operation, claim,
observation, installation, registry or release mutation, submission, merge,
deployment, rung advancement, or Stage 4 action was performed.

## Findings

No blocking findings remain in the corrected contract-only package.

### ME-RP-813-E-001: The successor profile has no valid R0 release-state rebaseline path

Severity: high

`finding_lifecycle: fixed_state_followup`

`finding_status: fixed_confirmed_contract_only`

`blocking_status: not_blocking`

Original observed evidence:

- The reviewed successor profile SHA-256 is
  `59ed6ac6ea0c3763fc558d99f506e530f72f663e6ae483263e5df14333a4177e`.
- The one current R0 release record remains bound through
  `contract_sha256` to predecessor profile
  `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`.
- The profile requires each release record to bind the accepted current
  contract and says stale binding blocks all new native work.
- The existing release-chain validator forbids `contract_sha256` drift between
  successor records, so an ordinary R1 append cannot switch to the reviewed
  successor profile.
- The companion's six-path C envelope permits only mechanical checker binding
  updates and says release semantics remain unchanged. It defines no separate
  current-profile cross-check, R0 rebaseline record, migration, or prerequisite
  route.
- Existing request validation cross-binds a release record to its record,
  skill-tree, and registry digests, but not to the accepted current profile
  digest.

Original derived impact:

- After this profile becomes current, the existing R0 record cannot satisfy
  the profile's own `accepted current contract` rule.
- A later implementation could preserve a structurally valid old release
  chain while failing to prove that the active R0 authority belongs to the
  app-native successor profile.
- The package therefore cannot truthfully route from inert implementation
  toward R1/R2 without an explicit fail-closed rebaseline or migration rule.

Required correction from the initial review:

Codex B must define the smallest exact release-state/current-profile binding
transition and its validator behavior. It must preserve the historical R0
record, keep current operational authority false, and name any separately
reviewed release-state or validator scope required before R1. Codex C must not
infer or implement that transition from the present text.

Current verification evidence:

- The corrected profile defines exactly one 19-field
  `trusted_owner_native_release_rebaseline_record.v1` line in the existing
  append-only release file.
- The historical R0 artifact and record digests remain exact and immutable.
- The event keeps `from_rung=R0`, `to_rung=R0`, and an empty observation array;
  it grants no authority and cannot serve as an observation.
- Absence, stale predecessor, wrong rung, duplicate, fork, reordered,
  post-observation, second-rebaseline, or current-tuple drift fails closed as
  `blocked_release_state_invalid` before claim or task creation.
- The validator selects the rebaseline as the current R0 tip, and the next
  ordinary R1 record must name it as predecessor and preserve its complete
  current four-value tuple.
- Creation and append remain a separately reviewed and separately authorized
  integration action. The six-path inert implementation may add only parsing,
  validation, current-tip selection, and operation-free tests.
- The KAT reproduces exactly: 19 fields, 1,352-byte preimage,
  `50e60de91339280e4afe6b2e588c8d6be801e825405eae675703ff01451af32f`,
  1,435-byte artifact, and
  `5ba515bcf5023803d8233672459940c504b7158337a8e6ede575b8a926e0e5ff`.

Next route: separate owner inert-implementation decision, then `C`.

### ME-RP-813-E-002: The terminal-readback digest preimage is not canonical enough to implement independently

Severity: high

`finding_lifecycle: fixed_state_followup`

`finding_status: fixed_confirmed_contract_only`

`blocking_status: not_blocking`

Original observed evidence:

- The companion defines exact schemas and field orders for the operation
  binding, target readback, and 24-field platform receipt.
- `terminal_readback_sha256` is described only as hashing a canonical
  projection of five conceptual facts. The contract does not define that
  projection's schema version, exact field names, exact field order, or a
  known-answer vector.
- The platform-receipt KAT supplies an arbitrary 64-hex terminal-readback
  value, so it does not prove derivation from the five required facts.

Original derived impact:

- Two conforming-looking implementations can serialize different bytes and
  produce different terminal-readback digests for the same observation.
- A validator can accept a syntactically valid digest without independently
  proving its binding to the task, status, operation, target, and read time.

Required correction from the initial review:

Codex B must define one exact private in-memory terminal-readback object,
including schema/version, field names and order, scalar rules, final LF, and
one operation-free known-answer vector. This does not require a new public
receipt family or any operational authority.

Current verification evidence:

- The corrected companion defines exactly six ordered fields under
  `trusted_owner_app_native_terminal_readback.v1`.
- Canonicalization is closed over NFC, ordered keys, UTF-8 without BOM, no
  whitespace, and exactly one final LF. Missing, duplicate, unknown,
  reordered, wrongly typed, nonterminal, noncanonical-time, final-byte,
  digest, and cross-binding drift are rejected.
- The 391-byte KAT hashes to
  `09a3d716d4f14baf67ebc5b4914b7e4daea24d8fd4c5376924859b5885a76e45`.
- That digest exactly cross-binds the terminal status, operation identity,
  task identity, and target-readback digest in the revised 24-field platform
  receipt KAT.
- The platform receipt KAT reproduces a 1,489-byte preimage with self-digest
  `c0af9c0be3cd43c4a1db80e1b525749d6c91cb2c8dc057e193c3badf17327918`
  and a 1,582-byte artifact with SHA-256
  `5df194e378dad42d515879fff05c671da3c4852394c2cbb87a3564ef9c33b0e4`.
- The object remains private, in memory, and discarded after validation. It
  adds no public receipt family, durable private value, or authority.

Next route: separate owner inert-implementation decision, then `C`.

## Confirmed Contract Behavior

- The corrected profile SHA-256 is
  `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952`.
- The corrected companion SHA-256 is
  `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4`.
- The predecessor and both reviewed hashes are exact; the changed contract
  set is exactly the profile amendment plus the new companion.
- Issue #813 and tracker #746 are open. Issue #810 is closed, PR #812 is
  merged at the exact base with six successful checks, and issue #769 remains
  open with zero comments.
- The owner activation body is exactly 1,061 UTF-8 bytes with SHA-256
  `7d0f97e6606242f6a9dba099ccae70b0d3a1728a26c8b23579b6f632cc1106dc`,
  authored by immutable actor ID `229644849` and unedited.
- PRs #374 and #391 are the only open PRs and do not own either reviewed path.
- Existing public request, task receipt, result, handoff, claim, worktree,
  registry, release, authority, Safe/Automatic, F, 20-outcome, and R0-R8
  structures are textually unchanged by the profile diff.
- The direct companion requires one create call, one stable task identity,
  exact target readback, no second prompt, no retry or replacement, retained
  claim on ambiguity, and same-task read-only reconciliation.
- The first proposed R2 observation remains one read-only E task. Exact live
  project/worktree/base readback remains explicitly unestablished and blocks
  R2 rather than being claimed as evidence.
- The App Server, direct-interpreter, broker, hostile-content, and OS-isolation
  records remain preserved and are neither direct-path prerequisites nor
  fallbacks.
- The corrected terminal-readback and platform-receipt KATs reproduce exactly
  with the byte counts and digests recorded in the fixed findings above.
- The future inert implementation envelope is exactly six named paths and
  exposes no real connector or task operation.

## Validation

- Both reviewed files are ordinary non-reparse ASCII files with LF endings,
  one final LF, no CR bytes, and no trailing whitespace.
- `git diff --check`: passed.
- Agent docs: 55 files, 0 errors, 0 warnings.
- Path-fed protected-surface scan: 2 paths, forbidden 0, warnings 0.
- Path-fed secret/private-marker scan: 2 paths, forbidden 0, warnings 0.
- Validation selector: 3 required and 1 recommended checks, warnings 0.
- Existing planner suite: 97 passed.
- Planner plus R0 bootstrap suites: 168 passed, 5 failed. All five failures
  are the expected predecessor-binding drift from the deliberately unchanged
  R0 checker; no unrelated runtime regression was observed.
- Read-only production R0 checker:
  `blocked_contract_binding_invalid`, zero effect counts, and all authority
  flags false.
- Matching task-operation process count: 0.
- Generated-residue count: 0.

## Remaining Live Unknowns

- The current reviewer tool inventory does not expose the three contracted
  app-task descriptors. The contract correctly makes then-current descriptor
  availability and exact project/worktree/base/operation readback future R2
  gates; neither is treated as established evidence here.
- The current installed target remains `unsafe_or_unreadable`, the registry
  remains A-only/offline, and the release state still contains only the
  historical R0 record. These are expected pre-R2 blockers, not contract
  acceptance evidence.
- No rebaseline record, implementation, live task observation, or platform
  receipt exists. Each requires its own later review and authority.

## Authority And Routing

- `owner_implementation_decision_eligible=true`
- `implementation_authorized=false`
- `task_creation_authorized=false`
- `task_observation_authorized=false`
- `claim_or_receipt_authorized=false`
- `registry_or_release_state_authorized=false`
- `installation_or_sync_authorized=false`
- `submission_authorized=false`
- `merge_authorized=false`
- `r0_r8_authorized=false`
- `stage4_authorized=false`
- `live_ready=false`

The corrected bytes are eligible for one separate owner decision authorizing
the exact six-path inert Codex C implementation. This review does not itself
authorize implementation or any operational action.

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Owner: if you choose to proceed, issue one fresh exact implementation decision
for issue #813 bound to profile SHA-256
8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952 and
companion SHA-256
00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4.
Authorize Codex C to implement only the six paths named by the accepted
contract, using fake clients and operation-free tests. Do not authorize a real
task operation, release append, registry change, installation, R0-R8
advancement, Stage 4, submission, merge, deployment, or readiness.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Independent Direct App-Native Trusted-Owner Task Contract Reviewer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  branch: "codex/role-pool-app-native-direct-task-contract-813"
  reviewed_base: "c24f1edf0a09a98439bdbd92ccf4e13155a3dd87"
  reviewed_profile_sha256: "8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952"
  reviewed_companion_sha256: "00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4"
  contract_verdict: "accepted_exact_direct_app_native_contract_for_inert_implementation"
  finding_status:
    ME-RP-813-E-001: "fixed_confirmed_contract_only"
    ME-RP-813-E-002: "fixed_confirmed_contract_only"
  owner_implementation_decision_eligible: true
  implementation_authorized: false
  task_creation_authorized: false
  observation_authorized: false
  registry_or_release_state_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Owner exact inert-implementation decision, then Codex C exact six-path implementer"
```
