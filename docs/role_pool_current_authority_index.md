# Role Pool Current-Authority Index

This document is a human-readable navigation index for the current public Role
Pool authority and lifecycle surfaces. It distinguishes normative authority,
canonical source, accepted evidence, immutable history, reviewed source
bindings, accepted deployment-copy equality, the Core validation-only registry,
unactivated release state, stronger external-isolation tracks, and
evidence-triggered watch items without replacing or elevating any owning
source.

## Snapshot Bindings

- Manual refresh date: `2026-07-30`.
- Core implementation base:
  `origin/main@17a71d182a1a189973f02a8e8c51669344823eb3`.
- Current index contract SHA-256:
  `0bf511be26724fb0963525a14e682cb8cbb47fe7169c603348c0358de1f2e5e0`.
- Canonical repository-registry bootstrap contract SHA-256:
  `f64dc584f780b0454d0dab59224796928e85f07c2f1bfb7a0574f7e0e217ac77`.
- Accepted independent registry-contract review SHA-256:
  `198e10e6f193999b66f7d22b430fe5897fdf6b64aec2ac0d82151b6573d4c002`.
- Current trusted-owner profile contract SHA-256:
  `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`.
- Reviewed canonical and installed Role Pool tree binding: `41` nodes, `36`
  files, `6495` canonical bytes, SHA-256
  `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`.
- Accepted offline-sync evidence self-digest:
  `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869`.
- Canonical registry entry self-digest:
  `30bd9fec65f1c4c08158c2f0777646fc2c53113a845604c8f16aad072628ec1e`.
- Canonical registry self-digest:
  `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7`.
- Complete registry artifact SHA-256:
  `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`.

## Authority Precedence

Use this index only after applying the following authority order:

1. current system and developer instructions;
2. the current explicit user instruction;
3. `AGENTS.md`, `docs/agent_rules.yml`, and
   `docs/agent_constitution.md`;
4. current live GitHub state, the active issue, and the current accepted
   contract;
5. accepted ADRs;
6. current accepted handoffs, review reports, PR, and validation evidence;
7. this navigation index; and
8. older examples, comments, summaries, or memory.

The index never upgrades evidence into mutation or execution authority. A link
does not import another issue's authority. An accepted review proves only the
scope it reviewed. A manifest proves only the exact source bytes it binds.

### Stale-Entry Failure Behavior

This index fails closed to manual reconciliation when:

- a referenced existing path or public GitHub target is missing;
- a reference resolves to a different repository, issue, PR, or artifact;
- the Core base, current contract, accepted evidence, or manifest binding
  differs from the snapshot above;
- the canonical 41-node inventory, file count, canonical byte count, or
  manifest SHA-256 differs;
- the installed-copy observation no longer supports exact source equality;
- the registry bytes, registry contract, owner selection, or issue #769
  zero-comment condition changes;
- the release-state path appears or changes;
- a linked Security issue's lifecycle or authority effect changes;
- a row conflicts with its owning source or current live GitHub state; or
- the fixed row count, order, fields, classification, or state token changes.

On stale state, stop using this index for routing, read the owning source, and
return the index to the appropriate A/B/C/E workflow. Do not infer a
replacement value, edit an accepted source, continue a protected operation, or
claim that the index remains current.

## Authority And Lifecycle Inventory

| surface_or_artifact_family | classification | canonical_reference | observed_lifecycle_state | authority_effect_or_explicit_non_effect | refresh_trigger |
| --- | --- | --- | --- | --- | --- |
| `repository_governance_and_workflow_authority` | `current_normative_authority` | `AGENTS.md`<br>`docs/agent_rules.yml`<br>`docs/agent_constitution.md`<br>`docs/codex_module_workflow.md`<br>`docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/755><br><https://github.com/Tahjali11/Mythic-Edge/issues/743><br><https://github.com/Tahjali11/Mythic-Edge/issues/746> | `active_current_governance` | These sources retain their existing precedence and govern repo workflow within their own scopes. This index adds no authority and cannot authorize mutation or execution. | First change to a listed governance source, accepted ADR, or relevant issue lifecycle or authority state. |
| `trusted_owner_native_profile_contract` | `current_normative_authority` | `docs/contracts/trusted_owner_native_role_pool_profile.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/744><br><https://github.com/Tahjali11/Mythic-Edge/pull/753> | `accepted_current_contract` | The contract governs the Windows-first trusted-owner profile. The exact registry permits only Core `A` / `offline_validation` / `docs` read after acceptance and integration; release state, dispatch, canaries, rung advancement, Stage 4, and readiness remain unauthorized. | First contract-byte change or relevant lifecycle or authority change to issue #744 or PR #753. |
| `canonical_role_pool_source` | `current_canonical_source` | `docs/codex_skills/mythic-edge-role-pool/` | `merged_canonical_source` | This is repository source, not an installed, synchronized, activated, or dispatch-authorized copy. | First canonical-source, Core-base, or reviewed-manifest change. |
| `current_implementation_and_review_evidence` | `current_accepted_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`<br>`docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md` | `accepted_current_evidence` | These artifacts provide accepted evidence for exact profile and registry-contract bytes and reviewed behavior only. They grant no claim, command, task, mutation, release, or rung authority. | First artifact-byte change or acceptance of a successor implementation or review artifact. |
| `role_pool_corrective_and_predecessor_history` | `immutable_historical_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `preserved_immutable_history` | These artifacts preserve predecessor findings, corrective addenda, earlier manifests, and superseded observations in context. Historical evidence is not current mutation, execution, or readiness authority. | First accepted successor that changes which corrective or predecessor evidence is current history. |
| `reviewed_role_pool_manifest` | `reviewed_manifest_binding` | `docs/codex_skills/mythic-edge-role-pool/`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md` | `reviewed_exact_manifest` | The reviewed binding is exactly 41 nodes, 36 files, 6495 canonical bytes, and SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`. It grants no install, sync, dispatch, canary, Stage 4, merge, deployment, or readiness authority. | First canonical path, byte, node-count, file-count, manifest-length, manifest-digest, or accepted-review change. |
| `installed_role_pool_deployment_copy` | `current_accepted_evidence` | <https://github.com/Tahjali11/Mythic-Edge/issues/768><br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md` | `identical_after_accepted_offline_sync` | Accepted issue #768 evidence self-digest `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869` records source/install equality at the reviewed 41-node binding. Deployment bytes remain non-authoritative and equality grants no dispatch, task, release, or rung authority. | First new installed-copy comparison, source-manifest change, or accepted evidence that changes the equality observation. |
| `trusted_owner_repository_registry` | `current_normative_authority` | `docs/role_pool/trusted_owner_repository_registry.v1.json`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`<br>`docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/769><br><https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208> | `active_core_validation_only_registry` | After independent acceptance and integration of this exact package, the registry permits only Core role `A`, operation `offline_validation`, and read scope `docs`; mutation scope and approved commands are empty and code execution is forbidden. Candidate branch bytes and this index grant no authority before then. | First registry-byte, owner-selection, issue-comment, identity, contract, acceptance, or integration-state change. |
| `trusted_owner_release_state` | `unactivated_registry_or_release_state` | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` | `absent_unactivated_release_state` | The absent path means no R0 bootstrap or later rung is active and `trusted_owner_native_profile_ready` remains false. | First appearance or change of the exact contracted release-state path. |
| `external_isolation_capability_tracks` | `blocked_external_isolation_track` | <https://github.com/Tahjali11/Mythic-Edge-Security/issues/116><br><https://github.com/Tahjali11/Mythic-Edge-Security/issues/118><br><https://github.com/Tahjali11/Mythic-Edge-Security/issues/139><br><https://github.com/Tahjali11/Mythic-Edge-Security/issues/140><br><https://github.com/Tahjali11/Mythic-Edge-Security/issues/141> | `open_separate_external_isolation_tracks` | These separate tracks do not block this docs-only index or the narrower trusted-owner source. Each applicable accepted track remains a prerequisite for the stronger external-isolation capability it governs; no Security-repository authority is copied here. | First lifecycle, scope, authority, or accepted-evidence change in any linked Security issue. |
| `mandatory_array_repair_advisory` | `watch_list_evidence_triggered` | <https://github.com/Tahjali11/Mythic-Edge-Security/issues/117> | `open_deferred_nonblocking_repair` | This advisory remains deferred and nonblocking unless its own current evidence proves it blocks a currently required operation. | First lifecycle or evidence change in Security issue #117 that affects a currently required operation. |
| `role_pool_validator_decomposition` | `watch_list_evidence_triggered` | <https://github.com/Tahjali11/Mythic-Edge/issues/755><br><https://github.com/Tahjali11/Mythic-Edge/issues/743> | `watch_only_no_trigger_evidence` | No decomposition issue or implementation authority exists. Route to a later Codex A problem representation only after concrete maintenance-failure, contradictory-rule-ownership, or unsafe-change-amplification evidence. | First concrete qualifying evidence recorded in the owning current-authority or leanability workflow. |

## Refresh Rules

Manually refresh this index:

- before any Role Pool install, sync, registry, release, dispatch, canary,
  rung, external-isolation, Stage 4, or readiness decision;
- after a change to any referenced path or accepted artifact;
- after a Core base or canonical Role Pool manifest change;
- after a new installed-copy comparison;
- when the contracted registry changes or the release-state path appears or
  changes;
- when issue #769, its zero-comment condition, or its owner-selection comment
  changes;
- when PR #753, issue #744, issue #755, parent #743, tracker #746, or a linked
  Security issue changes relevant lifecycle state; or
- when an accepted governance source or ADR changes precedence or authority.

Manual validation means reading current GitHub and owning-source state,
rechecking the exact artifact bindings, recomputing the canonical 41-node /
36-file manifest with the existing deterministic repository logic, validating
the exact registry through its existing owner, and confirming release state
remains absent while its row says `absent_unactivated_release_state`. Refresh
is read-only reconciliation; it does not imply automatic mutation.

## No Authority Or Readiness Claim

This index is navigational only. It owns no independent authority or lifecycle
fact. The exact registry becomes current only after independent acceptance and
separately authorized integration of this package, and even then permits only
the listed validation-only read scope. This index creates no release state,
validator, freshness checker, decomposition issue, installation,
synchronization, claim, command, task, dispatch, canary, Project update,
R0 acceptance, rung advancement, Stage-4 action, submission, merge, deployment,
readiness, security, privacy, assurance, or live-use authority. Every
operational and readiness authority flag remains false.
