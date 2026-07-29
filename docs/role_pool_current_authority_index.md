# Role Pool Current-Authority Index

This document is a human-readable navigation index for the current public Role
Pool authority and lifecycle surfaces. It distinguishes normative authority,
canonical source, accepted evidence, immutable history, reviewed source
bindings, deployment-copy drift, unactivated state, stronger external-isolation
tracks, and evidence-triggered watch items without replacing or elevating any
owning source.

## Snapshot Bindings

- Manual refresh date: `2026-07-29`.
- Core base and merged PR #753 commit:
  `origin/main@11f89782c4eeb65a9874e2a150201c1665d78070`.
- Current index contract SHA-256:
  `0bf511be26724fb0963525a14e682cb8cbb47fe7169c603348c0358de1f2e5e0`.
- Current trusted-owner profile contract SHA-256:
  `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322`.
- Current implementation handoff SHA-256:
  `0d06874a2abe65dae9a557a5e6d391ce1eb015fa24764b6a0bfb37835548d264`.
- Accepted implementation report SHA-256:
  `7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8`.
- Accepted Windows-first implementation report SHA-256:
  `67e134737fff4d59baef9156132dd3f6fc527bb2b6dd3214db2aecc833189080`.
- Reviewed canonical Role Pool source binding: `34` files, `2001219` bytes,
  `4921` manifest bytes, SHA-256
  `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`.

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
- the canonical 34-path inventory, file count, byte count, manifest byte
  count, or manifest SHA-256 differs;
- the installed-copy observation no longer supports the stated drift status;
- either registry or release-state path appears or changes;
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
| `trusted_owner_native_profile_contract` | `current_normative_authority` | `docs/contracts/trusted_owner_native_role_pool_profile.md`<br><https://github.com/Tahjali11/Mythic-Edge/issues/744><br><https://github.com/Tahjali11/Mythic-Edge/pull/753> | `accepted_current_contract` | The contract governs the inert Windows-first profile. Installation, registry population, dispatch, canaries, rung advancement, Stage 4, and readiness remain unauthorized. | First contract-byte change or relevant lifecycle or authority change to issue #744 or PR #753. |
| `canonical_role_pool_source` | `current_canonical_source` | `docs/codex_skills/mythic-edge-role-pool/` | `merged_canonical_source` | This is repository source, not an installed, synchronized, activated, or dispatch-authorized copy. | First canonical-source, Core-base, or reviewed-manifest change. |
| `current_implementation_and_review_evidence` | `current_accepted_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `accepted_current_evidence` | These artifacts provide accepted evidence for the exact inert bytes and reviewed behavior only. They grant no operational authority. | First artifact-byte change or acceptance of a successor implementation or review artifact. |
| `role_pool_corrective_and_predecessor_history` | `immutable_historical_evidence` | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `preserved_immutable_history` | These artifacts preserve predecessor findings, corrective addenda, earlier manifests, and superseded observations in context. Historical evidence is not current mutation, execution, or readiness authority. | First accepted successor that changes which corrective or predecessor evidence is current history. |
| `reviewed_role_pool_manifest` | `reviewed_manifest_binding` | `docs/codex_skills/mythic-edge-role-pool/`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `reviewed_exact_manifest` | The reviewed binding is exactly 34 files, 2001219 source bytes, 4921 manifest bytes, and SHA-256 `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`. It grants no install, sync, dispatch, canary, Stage 4, merge, deployment, or readiness authority. | First canonical path, byte, file-count, manifest-length, manifest-digest, or accepted-review change. |
| `installed_role_pool_deployment_copy` | `deployment_copy_drift` | `docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`<br>`docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md` | `drift_observed_not_synchronized` | The accepted reports record read-only `target_differs / drift`. Installed deployment bytes are not repo authority; drift blocks native dispatch but does not authorize synchronization. | First new installed-copy comparison or accepted change to the reports that own the observation. |
| `trusted_owner_repository_registry` | `unactivated_registry_or_release_state` | `docs/role_pool/trusted_owner_repository_registry.v1.json` | `absent_unactivated_registry` | The absent path means no repository entry or command allowlist is active. Schemas and tests cannot imply registry population. | First appearance or change of the exact contracted registry path. |
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
- when either contracted registry or release-state path appears or changes;
- when PR #753, issue #744, issue #755, parent #743, tracker #746, or a linked
  Security issue changes relevant lifecycle state; or
- when an accepted governance source or ADR changes precedence or authority.

Manual validation means reading current GitHub and owning-source state,
rechecking the exact artifact bindings, recomputing the canonical 34-file
manifest with the existing deterministic repository logic, and confirming the
two future state paths remain absent when their rows say `absent_unactivated_*`.
Refresh is read-only reconciliation; it does not imply automatic mutation.

## No Authority Or Readiness Claim

This index is navigational only. It owns no independent authority or lifecycle
fact and creates no schema, registry, release state, validator, freshness
checker, decomposition issue, installation, synchronization, claim, dispatch,
canary, Project update, Stage-4 action, submission, merge, deployment,
readiness, security, privacy, assurance, or live-use authority. Every
operational and readiness authority flag remains false.
