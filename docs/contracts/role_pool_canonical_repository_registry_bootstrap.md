# Canonical Repository-Registry Bootstrap Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/769>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>
- Owner selection:
  <https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208>
- Role: Codex B, Module Contract Writer
- Risk tier: `high`
- Governing guidance:
  - `AGENTS.md`
  - `docs/agent_rules.yml`
  - `docs/agent_constitution.md`
  - `docs/codex_module_workflow.md`
  - `docs/agent_threads/module_contract.md`
  - `docs/templates/module_contract.md`
  - `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`

## Findings

1. At `origin/main@17a71d182a1a189973f02a8e8c51669344823eb3`,
   the fixed registry and release-state paths are absent.
2. Issue #769 is open and had zero top-level comments immediately before this
   contract was written. Its issue body remains the candidate dedicated
   scheduling surface; this contract does not comment on it.
3. GitHub currently reports repository ID `1235264383`, canonical repository
   name `Tahjali11/Mythic-Edge`, and owner actor ID `229644849`. Canonical
   packet text uses lowercase `tahjali11/mythic-edge`.
4. The owner selection was created by `Tahjali11` at
   `2026-07-30T23:42:04Z`. It selects issue #769, actor set `[229644849]`,
   and the exact Core-only, validation-only authority shape below.
5. The accepted registry schema and
   `validate_trusted_native_registry` already represent the selected object.
   No schema, validator, lifecycle, release state, command registry, or
   authority mechanism is missing.
6. The current public-safe #761 packet is exact and self-digested, but selects
   `blocked_registry_missing_or_invalid`. The source and installed Role Pool
   trees are already identical.
7. `docs/role_pool_current_authority_index.md` is stale under its own refresh
   rules because it still records the predecessor profile, 34-file source, and
   drifting installed copy. It must be refreshed in the same future reviewed
   implementation package as the registry.
8. Open PRs #374 and #391 do not overlap this contract or its future two-file
   implementation. The owner selection records a task-scoped ADR-0008
   `explicit_user_override` for this Codex B contract only.

## Module And Truth Ownership

Module: first canonical trusted-owner repository-registry bootstrap.

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership is split without overlap:

- `docs/contracts/trusted_owner_native_role_pool_profile.md` owns the registry
  schema, canonicalization rules, transition rules, and fail-closed validator
  behavior.
- The future exact
  `docs/role_pool/trusted_owner_repository_registry.v1.json` owns the selected
  repository entry only after its exact implementation is independently
  accepted and integrated.
- `tools/check_role_pool_r0_bootstrap.py` owns the read-only #761 prerequisite
  evidence packet and first-failure result.
- `docs/role_pool_current_authority_index.md` remains a human-readable
  navigation index. It grants no authority and does not own registry truth.
- GitHub owns immutable repository, actor, issue, comment, and timestamp
  metadata. The current user instruction and owner-selection comment own the
  selection decision.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Contract base | `origin/main@17a71d182a1a189973f02a8e8c51669344823eb3` |
| Issue | `https://github.com/Tahjali11/Mythic-Edge/issues/769` |
| Tracker | `https://github.com/Tahjali11/Mythic-Edge/issues/746` |
| Owner approval reference | `https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208` |
| Owner approval time | `2026-07-30T23:42:04Z` |
| Repository ID | `1235264383` |
| Actor ID | `229644849` |
| Trusted-owner profile SHA-256 | `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| R0 checker contract SHA-256 | `9793951fa1a5a2e6ca7d1bb6325e89e9c2ca185aa4609b19481891405ef32a03` |
| Post-sync binding successor SHA-256 | `07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82` |
| Registry validator SHA-256 | `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` |
| Registry-validator tests SHA-256 | `60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49` |
| #761 checker SHA-256 | `34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914` |
| #761 checker tests SHA-256 | `976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34` |
| Validator-bundle SHA-256 | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| Authority-index contract SHA-256 | `0bf511be26724fb0963525a14e682cb8cbb47fe7169c603348c0358de1f2e5e0` |
| Current stale authority-index SHA-256 | `f70779be970f910459aded082c789f402883dfa9c89bf2bc3f2c9ecf76193b58` |
| Source and installed managed tree | `41` nodes, `36` files, `6495` canonical bytes, SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Current #761 evidence self-digest | `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869` |
| Current #761 packet artifact | `2559` bytes, SHA-256 `9891b9d7d505a42a0108a86be7d4cf39fe06ef4e65e0b0a0d0309c65d65162ff` |
| Current #761 terminal | `blocked_registry_missing_or_invalid` |

Any drift in these bindings, the owner-selection comment, GitHub immutable
identities, issue #769 comment count, or fixed-path absence stops future
implementation and routes to Codex B. No value may be reconstructed from an
older prompt or local index.

## Files Owned By This Contract

Codex B creates only:

- `docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`

After independent contract acceptance and a separate owner implementation
decision, Codex C may change exactly:

1. create
   `docs/role_pool/trusted_owner_repository_registry.v1.json`; and
2. refresh `docs/role_pool_current_authority_index.md`.

No validator, checker, test, release-state, skill-source, installed-skill, or
other path is in the implementation envelope. Existing focused tests are
sufficient because the selected object introduces no new schema behavior.
An observed missing behavior must return to Codex B instead of silently
expanding the C package.

## Exact Registry Object

The future registry is exactly one canonical JSON object with:

- `9` root fields in the accepted root-field order;
- exactly one `18`-field entry;
- no approved-command records;
- UTF-8 without BOM;
- no insignificant whitespace;
- ordinal object-key and array ordering required by the accepted profile; and
- exactly one final LF.

The exact complete bytes are:

```json
{"schema_version":"trusted_owner_repository_registry.v1","profile_id":"trusted_owner_native","coordination_repository_id":1235264383,"coordination_repository_name":"tahjali11/mythic-edge","coordination_issue_number":769,"authorized_claim_actor_ids":[229644849],"release_state_path":"docs/role_pool/trusted_owner_native_release_state.v1.jsonl","entries":[{"schema_version":"trusted_owner_repository_entry.v1","repository_id":1235264383,"canonical_name":"tahjali11/mythic-edge","status":"active","trust_basis_refs":["docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md","docs/contracts/role_pool_canonical_repository_registry_bootstrap.md","docs/contracts/trusted_owner_native_role_pool_profile.md"],"eligible_roles":["A"],"permitted_operations":["offline_validation"],"permitted_read_scope":["docs"],"maximum_mutation_scope":[],"repository_code_execution_policy":"forbidden","approved_commands":[],"protected_surface_restrictions":["parser_truth"],"external_effect_restrictions":["credentials","network","service"],"approving_authority_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208","approved_at_utc":"2026-07-30T23:42:04Z","review_triggers":["authority_widening","identity_drift","protected_surface_change","transfer"],"review_due_at_utc":null,"entry_sha256":"30bd9fec65f1c4c08158c2f0777646fc2c53113a845604c8f16aad072628ec1e"}],"registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7"}
```

The code block contains a final LF after the JSON line. Its known-answer
bindings are:

| Object | Preimage bytes | Complete bytes | Self-digest | Complete artifact SHA-256 |
| --- | ---: | ---: | --- | --- |
| Entry | `955` | `1037` | `30bd9fec65f1c4c08158c2f0777646fc2c53113a845604c8f16aad072628ec1e` | `754fc5e6c2046c9d6bab9dc4f550048282f0738143f9d04c63fb1b19cb93e330` |
| Registry | `1393` | `1478` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` | `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |

For each self-digest, the preimage is the canonical object with only its final
self-digest member omitted and the final LF retained. The entry digest is
present before calculating the registry digest. The complete artifact SHA-256
is evidence about the final bytes and is not substituted for the embedded
self-digest.

## Closed Authority Meaning

The entry is a positive allowlist. It permits only:

- role `A`;
- operation `offline_validation`;
- read scope `docs`; and
- no mutation, approved command, repository code execution, or external
  effect.

Everything not explicitly permitted is denied. The supplemental
`parser_truth`, `credentials`, `network`, and `service` restrictions cannot be
read as permission for an omitted surface or effect.

`status=active` is the exact post-acceptance registry value required by the
#761 checker. Candidate bytes on an implementation branch have no effective
authority. The entry becomes current only after:

1. this contract receives independent Codex E acceptance;
2. a separate owner decision authorizes the exact two-file implementation;
3. Codex C creates only the contracted bytes and index refresh;
4. fresh Codex E accepts the exact implementation; and
5. separately authorized F/G integration completes.

Before all five conditions, no claim actor, role, operation, or entry is
active. After them, the entry still permits only read-only prerequisite
validation. It does not create a claim, command, task, process, mutation,
release record, R0 acceptance, or rung authority.

## Fixed Path And Collision Behavior

The only registry destination is:

`docs/role_pool/trusted_owner_repository_registry.v1.json`

The only related release destination is:

`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`

Future Codex C must:

1. refresh `origin/main` and revalidate all bindings;
2. confirm issue #769 is open with zero top-level comments;
3. confirm the owner-selection comment is unchanged;
4. observe the fixed `docs` ancestor as ordinary and non-reparse;
5. observe `docs/role_pool` only by its fixed path;
6. require the registry and release-state destinations to be absent;
7. create the registry only as a new path, never as a replacement; and
8. read back and validate the exact `1478` bytes and both registry digests.

If `docs/role_pool` is absent, adding the exact registry path may create that
directory as its repository parent. If the parent already exists, it must be
ordinary, non-reparse, and contain no conflicting fixed destination. No broad
search, alternate parent, case variant, symlink, junction, path
normalization, registry merge, overwrite, in-place repair, or release-state
creation is permitted.

An existing final path is `registry_destination_collision`. A changed owner
selection, nonzero #769 comment count, appeared release state, unsafe parent,
unexpected sibling authority artifact, or uncertain path identity is
`registry_precondition_drift`. Either result stops before file edits and
returns to Codex B. No retry, cleanup, deletion, or adoption of appeared bytes
is authorized.

## Current-Authority Index Refresh

The future implementation must refresh the existing index in the same
reviewed package. It must preserve the six-column shape, authority precedence,
public-safe references, manual refresh model, and no-authority rule.

The refresh must:

1. bind the actual implementation date and exact `origin/main` base used by C;
2. bind profile SHA-256
   `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`;
3. bind this contract, issue #769, and the owner-selection comment;
4. replace the stale 34-file source facts with the exact 41-node, 36-file,
   6495-byte managed-tree binding and SHA-256
   `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`;
5. classify the installed deployment copy as `current_accepted_evidence` with
   lifecycle `identical_after_accepted_offline_sync`, citing issue #768 and
   post-sync evidence self-digest
   `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869`;
6. classify the registry as `current_normative_authority` with lifecycle
   `active_core_validation_only_registry`, while stating its exact limited
   effect and post-acceptance condition;
7. retain the release-state row as
   `unactivated_registry_or_release_state` /
   `absent_unactivated_release_state`;
8. preserve Security and validator-decomposition rows as non-imported
   external tracks or watch items; and
9. state that the refreshed index grants no authority and becomes current only
   with independent acceptance and integration of the exact package.

No change to
`docs/contracts/role_pool_current_authority_index.md` is authorized. This
contract is the narrow successor instruction for the event-triggered target
refresh.

## Existing Validator And Focused Tests

The implementation must reuse:

- `parse_trusted_native_json`;
- `validate_trusted_native_registry`;
- `trusted_native_self_digest`;
- `trusted_native_canonical_bytes`; and
- the existing #761 fixed-path registry and packet owners.

Copied parsing, copied digest logic, a second validator, or a generated schema
is forbidden.

Required focused validation is:

```powershell
py -B -m unittest test_check_pool_plan.py
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py
py -B tools\check_role_pool_r0_bootstrap.py
```

Run the first command from
`docs/codex_skills/mythic-edge-role-pool/scripts`. Run the latter two from the
repository root. The production checker is expected to exit `0` only after
the exact registry candidate is present and all earlier components remain
exact.

Codex C and Codex E must additionally perform an in-memory known-answer check
that:

- reads only the fixed registry path;
- requires byte count `1478`;
- requires complete artifact SHA-256
  `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`;
- strictly parses the one JSON object;
- requires `validate_trusted_native_registry` to return no errors;
- requires the exact field values and order above; and
- requires entry and registry self-digests to match their preimages.

The contract-specific known-answer equality check, followed by the generic
schema validator, must reject one-at-a-time changes to repository ID,
canonical name, issue number, actor set, role, operation, read scope, mutation
scope, code policy, approved commands, status, owner reference, approval time,
review triggers, either self-digest, final LF, or any unknown field. The
generic validator remains reusable for later independently reviewed registry
versions and is not changed to hard-code this first artifact. Existing test
helpers may provide the bootstrap equality evidence in memory; no durable test
edit is needed.

## Expected Post-Integration #761 Packet

With the exact registry integrated and release state still absent, every
current post-sync packet field remains unchanged except:

| Field | Expected value |
| --- | --- |
| `registry_status` | `valid_exact` |
| `registry_sha256` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| `terminal_status` | `eligible_for_independent_review` |
| `eligible_for_independent_review` | `true` |
| `evidence_sha256` | `142d768a20aeed30eaa1f3510926ec94ee6d544e4c7f23dfad3d5685dbad3033` |

The complete expected packet is `2621` bytes with artifact SHA-256
`894973a726fc0837064eee8d1df630994e0a3006817464f4bd317adfdf045802`.
It must also retain:

- `contract_binding_status=exact`;
- `manifest_status=exact`;
- `source_install_status=identical`;
- `release_state_status=absent_bootstrap_candidate`;
- `release_state_sha256=null`;
- `validator_bundle_status=exact`;
- `offline_validation_status=passed`;
- all five effect counts at integer zero; and
- all 16 authority flags at boolean false.

`eligible_for_independent_review` permits only fresh Codex E review of the
exact prerequisite packet and package. It is not R0 acceptance, R0 activation,
installation authority, registry-replacement authority, release-state
authority, process or task authority, dispatch authority, rung advancement,
Stage 4 authority, readiness, or assurance.

## Validation And Acceptance

Codex B must run:

```powershell
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Independent Codex E must:

1. recompute every public binding and GitHub immutable identity;
2. prove issue #769 still has zero top-level comments without commenting;
3. strictly parse the canonical registry vector and reproduce every byte count
   and digest;
4. confirm the accepted profile and current validator represent the object
   without modification;
5. confirm the future C envelope is exactly two files;
6. confirm collision behavior never overwrites or adopts an existing object;
7. reproduce the expected #761 packet transform in memory;
8. confirm the index refresh rules are complete and navigational only;
9. run the focused, structural, protected-surface, secret, process, and
   residue checks; and
10. confirm all current authority remains false.

Contract acceptance makes a separate owner implementation decision eligible.
It does not authorize Codex C, file creation, submission, integration, or any
operation.

## Protected Boundaries And Non-Claims

This contract does not authorize:

- creating the registry or its parent directory;
- creating or changing release state;
- editing validators, checkers, tests, canonical skill source, or installed
  skill bytes;
- posting a comment on issue #769;
- publishing a claim or claim-resolution event;
- approving or running a command;
- starting a process, App Server, thread, turn, task, broker, service, or
  canary;
- creating a worktree other than this contract-authoring worktree;
- installing, synchronizing, dispatching, or mutating repository state beyond
  this one contract file;
- accepting or advancing R0-R8 or Stage 4;
- staging, committing, pushing, opening a PR, submitting, merging, deploying,
  or closing an issue; or
- claiming readiness, correctness, security, privacy, reliability, assurance,
  or live support.

Current authority counts are all zero:

```yaml
registry_creation_authorized: false
release_state_authorized: false
claim_publication_authorized: false
command_execution_authorized: false
process_or_task_authorized: false
installation_or_sync_authorized: false
dispatch_authorized: false
r0_acceptance_authorized: false
r0_r8_advancement_authorized: false
stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
live_ready: false
```

## Next Workflow Action

Next role: Codex E, fresh independent canonical repository-registry bootstrap
contract reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Canonical Repository-Registry Bootstrap Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/769
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Branch: codex/role-pool-canonical-repository-registry-bootstrap-769

Review only:
docs/contracts/role_pool_canonical_repository_registry_bootstrap.md

Recompute the contract SHA-256 from the exact Codex B handoff. Verify current
origin/main, issue #769 zero-comment state, owner selection
https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208,
repository ID 1235264383, actor ID 229644849, every accepted artifact binding,
the exact 1478-byte registry vector, entry and registry self-digests, complete
artifact digest, fixed-path collision behavior, two-file future C envelope,
current-authority index refresh, and the exact expected #761 packet.

Confirm that the existing validator and tests are sufficient and that no new
schema, validator, release state, command, claim, process, task, installed
mutation, R0 acceptance, R0-R8 advancement, Stage 4 authority, or readiness
claim is introduced.

Run git diff --check, agent-doc validation, focused registry and #761 tests,
protected-surface and secret scans, and process/residue checks. Do not comment
on #769, create the registry, edit implementation, submit, merge, or advance a
rung.

If and only if there are no blocking findings, create the normal durable Codex
E contract-test report exactly at
docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md
and state that a separate owner implementation decision may be considered.
End with a workflow_handoff to the owner, then Codex C only after separate
authorization.
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
    - "workflow authority and repository registry"
    - "issue and tracker lifecycle"
    - "installed Role Pool and release state"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "The exact owner selection supplies a B-only explicit_user_override. PRs #374 and #391 are separate and non-overlapping."
  stop_conditions:
    - "binding or immutable-identity drift"
    - "any top-level comment on issue #769"
    - "registry or release-state destination collision"
    - "scope beyond this one contract file"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  target_artifact: "docs/contracts/role_pool_canonical_repository_registry_bootstrap.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_future_submission_authority"
  branch: "codex/role-pool-canonical-repository-registry-bootstrap-769"
  validation:
    - "contract canonical-vector and digest validation"
    - "git diff --check"
    - "agent-doc validation"
    - "protected-surface and secret-pattern scans"
  stop_conditions:
    - "owner-selection or public-binding drift"
    - "issue #769 receives any top-level comment"
    - "registry or release-state destination appears"
    - "future implementation requires more than the exact two-file envelope"
  registry_created: false
  release_state_created: false
  implementation_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
```
