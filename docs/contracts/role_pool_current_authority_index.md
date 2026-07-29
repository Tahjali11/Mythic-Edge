# Role Pool Current-Authority Index Contract

Status: `implementation_pending`

Risk tier: `medium`

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/755

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/743

Phase 8 tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Completed source lane:
https://github.com/Tahjali11/Mythic-Edge/issues/744

Completed source pull request:
https://github.com/Tahjali11/Mythic-Edge/pull/753

Authority references:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`

## Module And Ownership

Module: additive, human-readable Role Pool authority and lifecycle navigation.

Internal project area: `Quality / Governance`.

Truth owner: the referenced governance, contract, source, evidence, GitHub, and
deployment-state surfaces continue to own their respective facts. The index
owns no authority or lifecycle fact independently.

Bridge-code status: `shared_support`.

The index may summarize and link current public evidence. It must not replace,
rewrite, supersede, elevate, or reinterpret a referenced source.

## Current Bindings

The implementation must start from and preserve these exact reviewed bindings:

| Binding | Current exact value |
| --- | --- |
| Core base | `origin/main@11f89782c4eeb65a9874e2a150201c1665d78070` |
| Completed source PR | PR #753, merged at commit `11f89782c4eeb65a9874e2a150201c1665d78070` |
| Current trusted-owner contract | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322` |
| Current implementation handoff | `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`, SHA-256 `0d06874a2abe65dae9a557a5e6d391ce1eb015fa24764b6a0bfb37835548d264` |
| Accepted implementation report | `docs/contract_test_reports/trusted_owner_native_role_pool_profile.md`, SHA-256 `7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8` |
| Accepted Windows-first implementation report | `docs/contract_test_reports/trusted_owner_native_role_pool_profile_windows_first_implementation.md`, SHA-256 `67e134737fff4d59baef9156132dd3f6fc527bb2b6dd3214db2aecc833189080` |
| Canonical Role Pool source | `docs/codex_skills/mythic-edge-role-pool/` |
| Canonical source file count | `34` |
| Canonical source byte count | `2001219` |
| Canonical manifest byte count | `4921` |
| Reviewed canonical manifest SHA-256 | `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175` |

These values are implementation start gates, not permanent claims. Drift
before implementation selects the stale-entry behavior below and returns the
work to Codex B.

## ADR-0008 Lane Reconciliation

PRs #374 and #391 remain open and have no current parked or deferred
disposition. The owner's current invocation records this bounded exception:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #755 Role Pool current-authority index contract"
  blocked_active_issue_or_pr:
    - "PR #374"
    - "PR #391"
  reason: "The owner explicitly authorized one narrow Codex B contract while the two unrelated PR lanes remain open."
  allowed_scope:
    - "read current public repository and GitHub authority"
    - "create only docs/contracts/role_pool_current_authority_index.md"
    - "run the contract validation named below"
    - "produce one Codex C handoff"
  expiration_condition: "This Codex B contract and handoff are complete, or the owner revokes or redirects the lane."
  authorized_by: "Tahjali11 current user instruction"
  recorded_in: "docs/contracts/role_pool_current_authority_index.md"
```

The exception does not transfer to Codex C. Codex C must perform a fresh
ADR-0008 reconciliation or receive its own explicit owner override.

## Later Target

Codex C may later create:

`docs/role_pool_current_authority_index.md`

That target is a short Markdown navigation document. It is not a schema,
registry, release-state record, validator, automatic freshness checker,
authority database, accepted evidence receipt, or readiness record.

The target must contain, in this order:

1. title and one-paragraph purpose;
2. snapshot bindings for the Core base, reviewed manifest, and refresh date;
3. authority precedence and stale-entry behavior;
4. the exact authority/lifecycle table defined below;
5. refresh triggers and manual validation;
6. explicit non-authority and non-claim statements.

No other durable Role Pool artifact may be edited to implement this target.

## Closed Lifecycle Classifications

Every index row must use exactly one of these values:

1. `current_normative_authority`
2. `current_canonical_source`
3. `current_accepted_evidence`
4. `immutable_historical_evidence`
5. `reviewed_manifest_binding`
6. `deployment_copy_drift`
7. `unactivated_registry_or_release_state`
8. `blocked_external_isolation_track`
9. `watch_list_evidence_triggered`

No alias, catch-all, inferred state, or additional classification is allowed.
If a required family cannot be represented truthfully by one value, Codex C
must stop and return to Codex B rather than extend the vocabulary.

## Exact Row Shape

The index table has exactly these six fields in this order:

1. `surface_or_artifact_family`
2. `classification`
3. `canonical_reference`
4. `observed_lifecycle_state`
5. `authority_effect_or_explicit_non_effect`
6. `refresh_trigger`

The table must not add hidden fields, machine identifiers, status booleans, or
digest columns. Exact binding values belong in the snapshot section or the
human-readable cell that needs them.

Field rules:

- `surface_or_artifact_family` is one exact family name from the inventory
  below.
- `classification` is one closed value from this contract.
- `canonical_reference` contains only exact repository-relative POSIX paths or
  exact public GitHub issue/PR URLs. A family may contain an ordered list of
  exact references. Wildcards and local paths are forbidden.
- `observed_lifecycle_state` uses the exact state token assigned below and may
  add one short plain-English clarification without changing its meaning.
- `authority_effect_or_explicit_non_effect` says what the owning source
  governs and names what the row cannot authorize.
- `refresh_trigger` names the first public event that makes the row require
  readback. It may not imply automatic mutation.

## Required Family Inventory And Order

The index contains exactly these 12 family rows in this order:

| Order | `surface_or_artifact_family` | Required classification | Required lifecycle state | Required references and treatment |
| --- | --- | --- | --- | --- |
| 1 | `repository_governance_and_workflow_authority` | `current_normative_authority` | `active_current_governance` | Link `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, `docs/codex_module_workflow.md`, accepted ADR-0008, issue #755, parent #743, and tracker #746. These sources retain their existing precedence; the index adds none. |
| 2 | `trusted_owner_native_profile_contract` | `current_normative_authority` | `accepted_current_contract` | Link `docs/contracts/trusted_owner_native_role_pool_profile.md`, issue #744, and merged PR #753. State that the contract governs the inert Windows-first profile while installation, registry population, dispatch, canaries, rung advancement, Stage 4, and readiness remain unauthorized. |
| 3 | `canonical_role_pool_source` | `current_canonical_source` | `merged_canonical_source` | Link `docs/codex_skills/mythic-edge-role-pool/`. It is repository source, not an installed or activated copy. |
| 4 | `current_implementation_and_review_evidence` | `current_accepted_evidence` | `accepted_current_evidence` | Link the implementation handoff and the two accepted reports bound above. Acceptance is evidence of exact inert bytes, not operational authority. |
| 5 | `role_pool_corrective_and_predecessor_history` | `immutable_historical_evidence` | `preserved_immutable_history` | Group predecessor findings, corrective addenda, earlier manifests, and superseded observations through the current handoff/reports. Do not enumerate every historical file or relabel history as current authority. |
| 6 | `reviewed_role_pool_manifest` | `reviewed_manifest_binding` | `reviewed_exact_manifest` | State the exact 34-file, 2001219-byte, 4921-manifest-byte, SHA-256 binding above. The manifest binds reviewed source bytes only and grants no install, sync, dispatch, canary, Stage 4, merge, deployment, or readiness authority. |
| 7 | `installed_role_pool_deployment_copy` | `deployment_copy_drift` | `drift_observed_not_synchronized` | Cite the accepted implementation reports, which record read-only `target_differs / drift`. Do not name a local installed path or treat deployment bytes as repo authority. Drift blocks native dispatch but does not authorize synchronization. |
| 8 | `trusted_owner_repository_registry` | `unactivated_registry_or_release_state` | `absent_unactivated_registry` | Reference the contracted future path `docs/role_pool/trusted_owner_repository_registry.v1.json`. Its absence means no repository entry or command allowlist is active; schemas and tests cannot imply population. |
| 9 | `trusted_owner_release_state` | `unactivated_registry_or_release_state` | `absent_unactivated_release_state` | Reference the contracted future path `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`. Its absence means no R0 bootstrap or later rung is active and `trusted_owner_native_profile_ready` remains false. |
| 10 | `external_isolation_capability_tracks` | `blocked_external_isolation_track` | `open_separate_external_isolation_tracks` | Link Security #116, #118, #139, #140, and #141 individually. They do not block this docs-only index or the narrower trusted-owner source, but each applicable accepted track remains a prerequisite for the stronger external-isolation capability it governs. Copy no Security-repository authority into this index. |
| 11 | `mandatory_array_repair_advisory` | `watch_list_evidence_triggered` | `open_deferred_nonblocking_repair` | Link Security #117. Keep it deferred and nonblocking unless its own current evidence proves it blocks a currently required operation. |
| 12 | `role_pool_validator_decomposition` | `watch_list_evidence_triggered` | `watch_only_no_trigger_evidence` | No implementation issue is created. Route to a later Codex A problem representation only after concrete evidence of maintenance failure, contradictory rule ownership, or unsafe change amplification. |

Family-level grouping is mandatory. The index must not become an exhaustive
historical inventory, file manifest, finding ledger, or substitute for the
linked artifacts.

## Authority Precedence

The target must state this navigation rule:

1. current system and developer instructions;
2. the current explicit user instruction;
3. `AGENTS.md`, `docs/agent_rules.yml`, and
   `docs/agent_constitution.md`;
4. current live GitHub state, the active issue, and the current accepted
   contract;
5. accepted ADRs;
6. current accepted handoffs, review reports, PR, and validation evidence;
7. this navigation index;
8. older examples, comments, summaries, or memory.

The index never upgrades evidence into mutation or execution authority. A link
does not import another issue's authority. An accepted review proves only the
scope it reviewed. A manifest proves only the exact source bytes it binds.

## Stale-Entry Failure Behavior

The index fails closed to manual reconciliation if any of these is observed:

- a referenced existing path or public GitHub target is missing;
- a reference resolves to a different repository, issue, PR, or artifact;
- the Core base, current contract, accepted evidence, or manifest binding
  differs from this contract;
- the canonical 34-path inventory, file count, byte count, manifest byte
  count, or manifest SHA-256 differs;
- the installed-copy observation no longer supports the stated drift status;
- either registry or release-state path appears or changes;
- a linked Security issue's lifecycle or authority effect changes;
- a row conflicts with its owning source or current live GitHub state; or
- the fixed row count, order, fields, classification, or state token changes.

On stale state, a consumer must stop using the index for routing, read the
owning source, and return the index to the appropriate A/B/C/E workflow. It
must not infer a replacement value, edit an accepted source, continue a
protected operation, or claim that the index remains current.

## Public-Safe Reference Rules

- Repository references use exact POSIX paths relative to the Core repository.
- Existing-path references must resolve inside the repository to tracked
  ordinary files or directories at implementation time.
- The two exact contracted future paths may remain absent only while their
  rows say `absent_unactivated_*`.
- GitHub references use complete public HTTPS issue or PR URLs. Issue numbers
  without repository identity are insufficient in cross-repository rows.
- No glob, local absolute path, `file:` URI, private authority path, installed
  skill path, log, credential, environment value, raw runtime evidence, or
  machine-local identifier may appear.
- Security references remain read-only links. Their bodies, evidence, and
  authority are not copied into Core.

## Refresh Triggers

Manual refresh is required:

- before any Role Pool install, sync, registry, release, dispatch, canary,
  rung, external-isolation, Stage 4, or readiness decision;
- after a change to any referenced path or accepted artifact;
- after a Core base or canonical Role Pool manifest change;
- after a new installed-copy comparison;
- when either contracted registry or release-state path appears or changes;
- when PR #753, issue #744, issue #755, parent #743, tracker #746, or a linked
  Security issue changes relevant lifecycle state; or
- when an accepted governance source or ADR changes precedence or authority.

Refresh is a read-only reconciliation task. This contract authorizes no
automatic freshness checker, scheduled job, issue mutation, registry write, or
release-state write.

## Side Effects And Protected Boundaries

Codex B creates only this contract.

A later Codex C pass may create the index and its standard implementation
handoff. A later Codex E pass may create the independent review report named
in issue #755. Those roles require fresh authority and current-state
reconciliation.

This contract does not authorize:

- editing accepted artifacts or canonical Role Pool source;
- creating or populating a schema, registry, release state, validator, or
  freshness checker;
- creating a validator-decomposition issue;
- accessing private evidence;
- installing or synchronizing the Role Pool skill;
- dispatching, publishing claims, creating tasks, or running canaries;
- changing Project fields;
- submitting, merging, deploying, or advancing Stage 4; or
- readiness, security, privacy, assurance, or live-use claims.

Every operational authority flag remains false.

## Validation Required

Codex C and Codex E must verify:

- the repository remote, branch, issue, parent, tracker, ADR-0008 state, and
  current open PRs;
- the exact source bindings in this contract;
- the target has exactly 12 rows, six fields in order, and only the nine
  classifications;
- all existing Core paths resolve and the two future paths are absent;
- all GitHub links resolve to the intended public issue or PR;
- the canonical source recomputes to 34 files, 2001219 bytes, 4921 manifest
  bytes, and the exact reviewed manifest SHA-256;
- no private or machine-local value appears;
- only contract-authorized files changed; and
- the following commands pass:

```powershell
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main
py tools\check_secret_patterns.py --base origin/main
```

Validator decomposition remains an evidence-triggered watch item. Validation
success does not authorize creating a new validator or decomposition issue.

## Acceptance Criteria

- Exactly one additive human-readable current-authority index is implemented.
- The index follows the fixed 12-row family inventory and six-field order.
- Every classification and lifecycle state matches this contract.
- Current normative authority, source, accepted evidence, history, manifest,
  installed drift, unactivated state, blocked stronger capability, and watch
  items remain visibly distinct.
- Security #116, #117, #118, #139, #140, and #141 receive the exact treatment
  defined above without importing or weakening sibling-repository authority.
- Stale or conflicting rows fail closed before protected work.
- The index grants no authority and all operational/readiness claims remain
  false.
- Required validation passes with zero unintended files or generated residue.

## Remaining Risks

- The index is manually refreshed. It can become stale, so every protected
  operation must continue to read its owning sources.
- PRs #374 and #391 remain open. Their unrelated WIP state is not resolved by
  this contract.
- Registry population, release-state bootstrap, installation synchronization,
  Windows capability evidence, dispatch, canaries, and all R0-R8 advancement
  remain unactivated.
- External-isolation capability remains owned by the linked Security tracks.

## Next Workflow Action

Next role: Codex C, after a fresh ADR-0008 reconciliation or owner override.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex C: Role Pool Current-Authority Index Implementer for
https://github.com/Tahjali11/Mythic-Edge/issues/755.

Work on branch codex/role-pool-current-authority-index-755. Read
docs/contracts/role_pool_current_authority_index.md and verify its SHA-256,
origin/main, issue #755, parent #743, tracker #746, ADR-0008, open PRs #374
and #391, and the reviewed 34-file Role Pool manifest before editing. Obtain
or identify a current lane activation for this C pass; the B-only override
does not transfer.

Create only the contracted human-readable index at
docs/role_pool_current_authority_index.md plus the standard Codex C
implementation handoff. Preserve every accepted artifact and the canonical
Role Pool source. Implement exactly the contract's 12-row family inventory,
six-field order, closed classifications, authority precedence, stale-entry
behavior, public-safe references, refresh rules, and no-authority statement.

Do not create a schema, registry, release state, validator, automatic freshness
checker, decomposition issue, installation, synchronization, claim, dispatch,
canary, Stage-4 action, Project update, submission, merge, deployment, or
readiness claim. Run the contract-required validation and route the exact
resulting bytes to independent Codex E review.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/755"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/role_pool_current_authority_index.md"
  target_artifact: "docs/role_pool_current_authority_index.md"
  risk_tier: "medium"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-current-authority-index-755"
  internal_project_area: "Quality / Governance"
  truth_owner: "referenced governance, contract, source, evidence, GitHub, and deployment-state surfaces"
  bridge_code_status: "shared_support"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "py tools/check_protected_surfaces.py --base origin/main"
    - "py tools/check_secret_patterns.py --base origin/main"
  stop_conditions:
    - "repository, issue, branch, base, contract, evidence, or manifest binding drift"
    - "missing or conflicting authority source"
    - "no current ADR-0008 lane activation for Codex C"
    - "need to edit an accepted artifact or canonical Role Pool source"
    - "need for private evidence, operational mutation, or scope expansion"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "medium"
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
    - "workflow authority and role boundaries"
    - "active-lane activation"
    - "installation, registry, release, dispatch, canary, and Stage-4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "Open PRs #374 and #391 require the recorded B-only explicit_user_override; their files do not overlap this contract."
  stop_conditions:
    - "binding drift"
    - "ambiguous source ownership"
    - "private evidence required"
    - "scope expands beyond one contract"
```
