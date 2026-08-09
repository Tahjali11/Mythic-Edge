# Role Pool Current-Authority Index

This document is a human-readable navigation index for the current public Role
Pool authority and lifecycle surfaces. It distinguishes normative authority,
canonical source, accepted evidence, immutable history, reviewed source
bindings, accepted deployment-copy equality, the Core validation-only registry,
the current app-native source/install binding, a candidate two-line R0 offline-only release state, stronger external-isolation tracks, and
evidence-triggered watch items without replacing or elevating any owning
source.

## Snapshot Bindings

- Manual refresh date: `2026-08-08`.
- Core implementation base:
  `origin/main@8470dd10c91faa02d923fe5d67246fcf280095cb`.
- Current index contract SHA-256:
  `0bf511be26724fb0963525a14e682cb8cbb47fe7169c603348c0358de1f2e5e0`.
- Canonical repository-registry bootstrap contract SHA-256:
  `f64dc584f780b0454d0dab59224796928e85f07c2f1bfb7a0574f7e0e217ac77`.
- Accepted independent registry-contract review SHA-256:
  `198e10e6f193999b66f7d22b430fe5897fdf6b64aec2ac0d82151b6573d4c002`.
- Current trusted-owner profile contract SHA-256:
  `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952`.
- Reviewed canonical and installed Role Pool tree binding: `43` nodes, `38`
  files, `6840` canonical bytes, SHA-256
  `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6`.
- Historical predecessor offline-sync evidence self-digest:
  `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869`.
- Canonical registry entry self-digest:
  `30bd9fec65f1c4c08158c2f0777646fc2c53113a845604c8f16aad072628ec1e`.
- Canonical registry self-digest:
  `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7`.
- Complete registry artifact SHA-256:
  `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`.
- Accepted R0 bootstrap contract SHA-256:
  `a96936c4237652ea1c74b3d63164fa6918bd9c90f509fd3d9f2fce24bb9bb61d`.
- Accepted R0 bootstrap sequencing-review SHA-256:
  `c3f07e5ba5dd51cc3bcfcbe3dbe9f2ba301da16c5988636e42d3d680bfb27ffd`.
- Accepted terminal-receipt recovery contract SHA-256:
  `a90d1f9478c48209a53cceba9607cbc3e0ee762420991ba6cd4d4871e283ed0f`.
- Accepted terminal-receipt recovery review SHA-256:
  `bb850911eb3b2c2612c94eb2d38429b88cc26043fcbef3dc65c750b359a7de82`.
- Historical bootstrap-recovery eligibility reference and exact-body SHA-256:
  <https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5142157228>,
  `d5f1aeff5ac90d0ff00fd0e43386aed2057f93729d3b98a1fc6c3fedbf70f3ee`.
- Historical bootstrap-recovery owner-decision reference and exact-body SHA-256:
  <https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5142216555>,
  `954a6065684a213d9f19f93c50110d90c76310170a163392da601c36c73dfc14`.
- Historical bootstrap consumption-receipt reference and self-digest:
  <https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5142337815>,
  `b996e0ce23a599eccba9f88159382d3b258fae0b4195175f7e337e03d80431d8`.
- Stable-reconstruction contract and integrated review package:
  `docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md`,
  SHA-256 `49c9adf44a78b46f4713a9e41f2b6f1b093b17f0a42c445436c30da039526058`,
  <https://github.com/Tahjali11/Mythic-Edge/pull/822>.
- Frozen stable validator bundle preimage and SHA-256: `788` bytes,
  `be432ceab519e42fc688800c2cda1b172845abb329acc942ba11c5a5490826ca`.
- Fresh app-native rebaseline eligibility reference and exact-body SHA-256:
  <https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228654366>,
  `689bf57c5986d846cc5b63dd488834cd4923ca4a4b11896701903cbd394fa898`.
- Fresh app-native rebaseline owner-decision reference and exact-body SHA-256:
  <https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228678653>,
  `c44dfcd311eff773b894773e4be3161af7ac73673b6aadb375da3d42201c1c2f`.
- Immutable predecessor and candidate release-tip self-digests:
  `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7`,
  `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91`.
- Candidate complete two-line release artifact: `2434` bytes, SHA-256
  `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2`.
- Candidate implementation comparison:
  `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`.

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
- the canonical 43-node inventory, file count, canonical byte count, or
  manifest SHA-256 differs;
- the installed-copy observation no longer supports exact source equality;
- the registry bytes, registry contract, owner selection, or issue #769
  zero-comment condition changes;
- the release-state bytes, implementation-review status, or integration state changes;
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
| `current_implementation_and_review_evidence` | `current_accepted_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`<br>`docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md`<br>`docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md`<br>`docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap_sequencing.md`<br>`docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md`<br>`docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md`<br>`docs/implementation_handoffs/role_pool_trusted_owner_r0_release_state_bootstrap_comparison.md`<br>`docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md`<br><https://github.com/Tahjali11/Mythic-Edge/pull/822><br><https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228654366><br><https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5228678653><br>`docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md` | `accepted_current_evidence` | The integrated contracts and reviews provide accepted evidence for exact profile, registry, bootstrap, recovery, stable reconstruction, and source/install bytes. The new rebaseline implementation handoff remains candidate evidence pending independent review and integration. These artifacts grant no claim, command, task, mutation, release, or rung authority. | First artifact-byte change or acceptance, rejection, or integration of a successor implementation or review artifact. |
| `role_pool_corrective_and_predecessor_history` | `immutable_historical_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `preserved_immutable_history` | These artifacts preserve predecessor findings, corrective addenda, earlier manifests, and superseded observations in context. Historical evidence is not current mutation, execution, or readiness authority. | First accepted successor that changes which corrective or predecessor evidence is current history. |
| `reviewed_role_pool_manifest` | `reviewed_manifest_binding` | `docs/codex_skills/mythic-edge-role-pool/`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md` | `reviewed_exact_manifest` | The reviewed app-native binding is exactly 43 nodes, 38 files, 6840 canonical bytes, and SHA-256 `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6`. It grants no install, sync, dispatch, canary, Stage 4, merge, deployment, or readiness authority. | First canonical path, byte, node-count, file-count, manifest-length, manifest-digest, or accepted-review change. |
| `installed_role_pool_deployment_copy` | `current_accepted_evidence` | <https://github.com/Tahjali11/Mythic-Edge/issues/768><br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md` | `identical_after_accepted_offline_sync` | The accepted issue #768 evidence self-digest `a6efa3700b95d6836be0757c58d0cfb30811807ffd548500155754ebd0c07869` remains immutable predecessor sync history. The fresh #819 eligibility review records current source/install equality at 43 nodes, 38 files, 6840 canonical bytes, and SHA-256 `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6`. Deployment bytes remain non-authoritative and equality grants no dispatch, task, release, or rung authority. | First new installed-copy comparison, source-manifest change, or accepted evidence that changes the equality observation. |
| `trusted_owner_repository_registry` | `current_normative_authority` | `docs/role_pool/trusted_owner_repository_registry.v1.json`<br>`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`<br>`docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/769><br><https://github.com/Tahjali11/Mythic-Edge/issues/746#issuecomment-5137411208> | `active_core_validation_only_registry` | After independent acceptance and integration of this exact package, the registry permits only Core role `A`, operation `offline_validation`, and read scope `docs`; mutation scope and approved commands are empty and code execution is forbidden. Candidate branch bytes and this index grant no authority before then. | First registry-byte, owner-selection, issue-comment, identity, contract, acceptance, or integration-state change. |
| `trusted_owner_release_state` | `current_normative_authority` | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` | `active_r0_offline_only_release_state` | The candidate two-line chain preserves predecessor tip `78bff761...e4a9ba7` and adds candidate tip `83688089...ab9a91`; its complete artifact SHA-256 is `fff6025b...b125f2`. It becomes current only after exact implementation acceptance and separately approved integration. R0 permits offline validation only and creates no process, task, claim, command, dispatch, R1-R8, Stage-4, or readiness authority. | First release-record byte change or change to implementation-review or integration status. |
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
- when the contracted registry, release-state bytes, implementation-review status,
  or integration state changes;
- when issue #769, its zero-comment condition, or its owner-selection comment
  changes;
- when PR #753, issue #744, issue #755, parent #743, tracker #746, or a linked
  Security issue changes relevant lifecycle state; or
- when an accepted governance source or ADR changes precedence or authority.

Manual validation means reading current GitHub and owning-source state,
rechecking the exact artifact bindings, recomputing the canonical 43-node /
38-file manifest with the existing deterministic repository logic, validating
the exact registry through its existing owner, validating the exact release records
and two-record chain, and reconciling its independent-review and integration
status with the `active_r0_offline_only_release_state` row. Refresh is read-only
reconciliation; it does not imply automatic mutation.

## No Authority Or Readiness Claim

This index is navigational only. It owns no independent authority or lifecycle
fact. The exact registry remains limited to its validation-only read scope. The
release record created by this package is a candidate until exact independent
implementation acceptance and separately approved integration; only then does
it establish R0 offline validation. This index creates no validator, freshness
checker, decomposition issue, installation, synchronization, claim, command,
task, dispatch, canary, Project update, R1-R8 advancement, Stage-4 action,
submission, merge, deployment, readiness, security, privacy, assurance, or
live-use authority. Every operational and readiness authority flag remains
false.
