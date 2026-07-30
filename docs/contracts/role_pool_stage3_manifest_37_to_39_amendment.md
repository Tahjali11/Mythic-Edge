# Role Pool Stage-3 Manifest 37-to-39 Amendment Contract

## Module

Stage-3 Role Pool manifest transition for the reviewed Windows App Server
native-task adapter candidate.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/758
- Predecessor issue: https://github.com/Tahjali11/Mythic-Edge/issues/757
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

## Authority And WIP Reconciliation

This contract is authorized by the owner's task-scoped
`explicit_user_override` for Codex B. The exception is recorded here with:

- repository: `Tahjali11/Mythic-Edge`;
- reason: contract the exclusive frozen Stage-3 manifest blocker for issue
  #758;
- allowed scope:
  `docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md`;
- parallel state: open PR #374 remains a separate draft lane and open PR #391
  remains a separate dependency lane;
- expiration: the Codex B handoff for this artifact; and
- transfer: none. Codex C receives only the implementation scope defined by
  this contract, not the WIP exception itself.

Issue #758 is open, issue #757 is closed, and tracker #746 is open. ADR-0008
remains controlling for later lane activation.

## Owning Layer

Quality / Governance owns this manifest-transition contract and the Stage-3
validation semantics. It does not own or establish runtime App Server behavior.

## Internal Project Area

Quality / Governance.

## Truth Owner

The exact repository bytes and the deterministic Stage-3 manifest algorithm
own manifest membership and digests. This contract owns the permitted
37-to-39 transition. Tests and review evidence verify those facts but do not
create operational authority.

## Bridge-Code Status

`shared_support`

The Stage-3 validator supports Role Pool release validation. It must not become
a dispatch, installation, runtime, or Stage-4 authority surface.

## Bound Evidence

| Binding | Exact value |
| --- | --- |
| Repository base | `origin/main` at `26ca98ce81c0f393bf1ec9df470c10ae911c01f7` |
| #757 capability-evidence contract | `docs/contracts/role_pool_windows_native_task_capability_evidence.md` at `d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef` |
| Accepted predecessor profile | `docs/contracts/trusted_owner_native_role_pool_profile.md` at origin/main SHA-256 `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322` |
| Accepted #758 implementation contract | `docs/contracts/role_pool_codex_app_server_native_task_adapter.md` at `814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8` |
| Reviewed #758 profile candidate | `docs/contracts/trusted_owner_native_role_pool_profile.md` at `4a0ba9efe5c987735c09df66f94f42924a92a40ca68fd15a84ffb2c41842c94d` |
| Preserved durable E report | `docs/contract_test_reports/role_pool_codex_app_server_native_task_adapter.md` at `5cf3cdc4c59c6cf8ca18a25135014c2c0adb507e03cd0c82a113dbd7e7eb0195` |

The durable E report preserves the earlier implementation review and its
pre-fix 39-row manifest. It is immutable historical evidence. The current
owner-supplied Codex E confirmation handoff binds the four hashes below and
records:

- `ME-RP-758-E-004: fixed_confirmed`;
- `ME-RP-758-E-005: fixed_confirmed`;
- focused validation: `128 passed`;
- broad non-Stage-3 validation: `295 passed`; and
- aggregate release gate blocked only by the frozen 37-to-39 Stage-3 manifest
  transition.

No separate durable final-E artifact digest was supplied. This contract does
not invent one. Future Codex E review must bind the exact implementation
handoff and current four files directly.

## Manifest Algorithm

The existing Stage-3 convention remains authoritative:

1. Include every ordinary file under
   `docs/codex_skills/mythic-edge-role-pool`, excluding `__pycache__`, `.pyc`,
   and `.pyo`.
2. Include the three frozen `mythic-edge-workflow` snapshot files already
   named by `WORKFLOW_SNAPSHOT_FILES`.
3. Represent each row with exactly `path` and `sha256`.
4. Use forward-slash manifest paths rooted at `mythic-edge-role-pool/` or
   `mythic-edge-workflow/`.
5. Sort rows by ordinal path order.
6. Canonicalize with UTF-8 JSON, ASCII escaping, object keys sorted,
   `separators=(",", ":")`, `allow_nan=false`, and no trailing LF.
7. Hash the complete canonical byte sequence with SHA-256.

The three frozen workflow rows remain:

| Path | SHA-256 |
| --- | --- |
| `mythic-edge-workflow/SKILL.md` | `04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb` |
| `mythic-edge-workflow/agents/openai.yaml` | `0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f` |
| `mythic-edge-workflow/scripts/accept_fallback_prompt.py` | `47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d` |

Their absence from the candidate worktree does not permit omission or
replacement. Validation must use their exact frozen bytes in an isolated
test-only sibling layout; it must not install or synchronize either skill.

## Exact Snapshot Bindings

### Accepted 37-File Predecessor

The immutable predecessor is the exact `origin/main` Role Pool source at the
bound base plus the three frozen workflow rows:

- file count: `37`;
- canonical byte count: `5416`; and
- manifest SHA-256:
  `2c6e3772fcfbd2eb68618486520d2d309b0594f8a1a7dafd2d3f32fd6ee76bcb`.

This snapshot remains historical evidence. It must not be rewritten,
relabelled as the current snapshot, or presented as revalidated by later
Stage-3 evidence.

### Historical Pre-Fix 39-File Review Snapshot

The durable E report's historical pre-fix snapshot has:

- file count: `39`;
- canonical byte count: `5729`; and
- manifest SHA-256:
  `900c4b4e66478aa1c92a2960392346ad66bd730a04bcb7042a0d4f88465a5e46`.

That digest reproduces only with the four pre-fix implementation hashes in the
durable report. It is not the current candidate digest and must not be adopted
as one.

### Current Reviewed 39-File Candidate

The exact current candidate has:

- file count: `39`;
- canonical byte count: `5729`; and
- manifest SHA-256:
  `b0a0dfeae17aa4c56e3b9abe8e3104e3f8893f38387a31c577cf3b54401de2a4`.

The predecessor comprises 34 Role Pool rows plus three frozen workflow rows;
the candidate comprises 36 Role Pool rows plus the same three workflow rows.
Relative to the accepted 37-file predecessor, exactly 35 rows are unchanged,
two rows are added, two rows are modified, and zero rows are removed.

## Exact Transition Inventory

### Added Rows

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `mythic-edge-role-pool/scripts/test_trusted_native_app_server_adapter.py` | `null` | `42e1d4d2e1edbf3c80b9d85e1b256afdc5f4475e18f0d662f7414c23af7a33be` |
| `mythic-edge-role-pool/scripts/trusted_native_app_server_adapter.py` | `null` | `9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18` |

### Modified Rows

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `mythic-edge-role-pool/scripts/check_pool_plan.py` | `cd85d9a33fbd92d8b29d8ec092a03492d7e05915a973796c5218a6eaf903fae0` | `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` |
| `mythic-edge-role-pool/scripts/test_check_pool_plan.py` | `8ca31a9276d5bb092686010968dce8d7e98715a15d4a581616ec60c06a2b4243` | `60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49` |

### Removed Rows

None. `removed_path_count=0`.

Missing, extra, duplicate, renamed, case-varied, reordered, or
digest-mismatched rows fail closed.

## Files Owned By This Contract

This Codex B thread writes only:

- `docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md`

The future Codex C implementation envelope is exactly:

- `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py`
- `docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py`

Their required starting bindings are:

| Path | Byte count | Starting SHA-256 |
| --- | ---: | --- |
| `mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | `51575` | `0c82bab47e45d87d66cd317027a2a7c63b11341bb734d75f5f780c7c7ac72b2e` |
| `mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py` | `194490` | `f334ebbe67d5fff8f68797e0709770d00cb254215e710d59e9fb331daca7ab08` |

No third implementation or test path is permitted unless a concrete failure
proves it strictly necessary and routes back to Codex B.

## Codex C Requirements

Codex C must make the smallest coherent Stage-3 validator and focused-test
change that:

1. preserves the 30-file Stage-2 baseline and the 37-file accepted predecessor
   as immutable historical evidence;
2. extends the existing allowed-added set by exactly the two adapter paths;
3. pins both added-path digests to the exact reviewed hashes;
4. changes the current manifest cardinality from `37` to `39` only where the
   value semantically represents this manifest;
5. changes count-derived negative expectations mechanically:
   - one missing current path is `38`;
   - one extra current path is `40`;
   - a wrong-path substitution remains `39`;
6. leaves unrelated values of `37`, `38`, `39`, or `40` unchanged, including
   lifecycle-registry cardinality, tuple counts, schema values, timestamps,
   fixture data, and historical evidence;
7. requires exact case-sensitive path membership, exact digests, unique paths,
   and ordinal path ordering before producing the transition;
8. preserves `removed_path_count=0`;
9. leaves every Stage-2 and prior Stage-3 receipt or observation historical,
   rather than silently rebinding it under the 39-file snapshot;
10. preserves all existing Stage-3 schemas, projections, authority fields, and
    terminal vocabulary unless an exact current failing test proves a
    mechanically necessary count-only update; and
11. preserves the output as synthetic, projection-only, claim-free, and
    zero-effect.

Blind global numeric replacement is forbidden.

## Self-Included Validator Rule

The two future Codex C paths are themselves manifest rows. Their post-C hashes,
and therefore the post-C 39-row manifest digest, cannot be hardcoded into the
same self-included validator without a circular dependency.

Codex C must:

- preserve the current reviewed candidate snapshot above as transition input
  evidence;
- report exact before and after hashes for both Codex C files;
- recompute the complete post-C 39-row manifest and report its canonical byte
  count and SHA-256;
- prove that the post-C manifest differs from the current reviewed 39-row
  candidate only in those two Codex C rows; and
- route that exact post-C digest and both changed files to independent Codex E.

Codex E, not an internal self-digest constant, accepts or rejects that exact
post-C snapshot.

## Negative Tests Required

Focused tests must independently reject:

- either new adapter path missing;
- any extra path;
- duplicate exact paths;
- case-insensitive duplicate representations;
- either new path renamed;
- either new path case-varied;
- any non-ordinal row order;
- either new adapter digest mismatched;
- either reviewed modified-row digest mismatched;
- any removed predecessor path; and
- a 39-row substitution that preserves count while changing membership.

The tests must also prove:

- the exact 37-file predecessor binding is historical and unchanged;
- the current candidate derives as 39 rows with exactly two additions, two
  reviewed modifications, and zero removals before the two validator-file
  implementation changes;
- Stage-2 evidence is not marked revalidated under the current manifest;
- `authority_expansion=false`; and
- no observation, task, claim, installation, dispatch, or runtime effect is
  performed.

## Error Behavior

Any binding drift, nonordinary or reparse path, unreadable file, duplicate
representation, count mismatch, path-set mismatch, row-order mismatch, digest
mismatch, unexpected modified row, or removed row fails closed before a
Stage-3 observation can be accepted.

An unknown or incomplete post-C manifest is not accepted and does not route to
Codex F. Historical evidence remains preserved; no automatic retry,
reconstruction, or silent reclassification is permitted.

## Protected-Surface Classification

```yaml
surface_classification:
  level: guarded_path
  categories:
    - workflow_enforcement
  current_role_performs_mutation: false
  evidence:
    issue: "https://github.com/Tahjali11/Mythic-Edge/issues/758"
    contract: "docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md"
    reviewed_diff: "current Codex E handoff binds the exact four implementation hashes"
    validation: "contract-only validation in the Codex B handoff"
```

For the later Codex C operation, the same category becomes
`protected_mutation` with `current_role_performs_mutation=true` because C
changes a validation gate. The issue, this contract, independent E review, and
all required validation remain mandatory.

## Side Effects And Authority

This contract creates no operational side effect. It grants no authority to:

- acquire, install, or synchronize the Role Pool or Codex;
- start an App Server process or create a task;
- create or mutate registry, release, claim, worktree, or scheduling state;
- dispatch a lane or run a canary;
- advance R0-R8 or Stage 4;
- submit, merge, deploy, or publish a release;
- claim compatibility, readiness, assurance, privacy, security, or live
  support.

Codex C may edit only the two named implementation paths. A passing aggregate
gate plus independent Codex E acceptance permits only routing to Codex F. It
does not grant any authority listed above.

## Validation Required

Codex C must run and report:

```powershell
py -B -m unittest test_stage3_behavioral_planning.py
py -B -m unittest test_trusted_native_app_server_adapter.py test_check_pool_plan.py
py -B run_release_tests.py
```

The first two commands run from
`docs/codex_skills/mythic-edge-role-pool/scripts`. The aggregate command runs
from the Role Pool root in the same isolated sibling layout used by the
accepted E evidence.

Acceptance requires:

- focused Stage-3 tests all pass with zero failures, errors, or skips;
- the existing adapter/planner focused gate remains exactly `128 passed`;
- the broad non-Stage-3 gate remains at least the accepted `295 passed`;
- the aggregate gate exits zero, collects at least the current `412` tests,
  has no failure, error, skip, or expected failure, and passes both structural
  validations;
- reviewed source bytes are unchanged by tests;
- deterministic predecessor, reviewed-candidate, and post-C manifest
  inventories reproduce;
- `git diff --check` passes;
- agent-doc, protected-surface, and secret/private-marker checks pass; and
- generated residue and task-created process counts are zero.

The exact post-C test count and manifest digest are evidence outputs and must
be recorded in the implementation handoff. They are not operational authority.

## Acceptance Criteria

- The contract's base and all supplied implementation hashes remain exact.
- The 37-row predecessor and current 39-row reviewed candidate reproduce their
  declared counts, byte counts, and digests.
- The transition inventory is exactly two added, two reviewed modified, and
  zero removed rows.
- Codex C changes only the two contracted Stage-3 files.
- All required negative tests exist and pass.
- The post-C 39-row manifest differs from the reviewed candidate only in the
  two contracted validator rows.
- The aggregate release gate passes.
- Independent Codex E accepts the exact two-file diff, post-C manifest, and
  validation evidence.
- Every operational authority and readiness claim remains false.

## Remaining Unknowns

- The post-C hashes of the two self-included validator files and the resulting
  post-C manifest digest are intentionally unknown until Codex C implements
  the contracted change.
- Real App Server compatibility remains unestablished. This manifest amendment
  cannot establish it.
- R0 entry remains separately gated.

## Next Workflow Action

Next role: Codex C, Stage-3 Manifest 37-to-39 Amendment Implementer.

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex C: Stage-3 Manifest 37-to-39 Amendment Implementer for issue #758.

Use the exact Codex B handoff for
docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md and stop if its
SHA-256, the bound origin/main commit, or any of the four reviewed candidate
hashes drift.

Reconcile ADR-0008 and live WIP before editing. Proceed only if issue #758 owns
the current slot or this pasted invocation is recorded as a fresh, C-scoped
explicit_user_override.

Edit only:
- docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py
- docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py

Implement the contract's exact 37-to-39 additive manifest transition,
historical-evidence preservation, count-specific updates, exact added-path
digest checks, ordinal ordering check, and required negative tests. Do not
perform blind numeric replacement and do not change App Server adapter
behavior.

Run the focused Stage-3, existing 128-test adapter/planner, broad non-Stage-3,
and aggregate release gates in the accepted isolated sibling layout. Report
the exact two-file before/after hashes, final 39-row manifest byte count and
SHA-256, test counts, structural validation, safety checks, and residue.

Do not install or synchronize the Role Pool, start App Server, create a task,
dispatch, run canaries, advance R0-R8 or Stage 4, stage, commit, push, open a
PR, or claim readiness. Route the exact implementation handoff to independent
Codex E.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/758"
  predecessor_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/757"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md"
  target_artifacts:
    - "docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py"
    - "docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py"
  risk_tier: "medium"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/role-pool-app-server-native-task-adapter-758"
  wip_exception: "explicit_user_override_expired_at_b_handoff"
  protected_surface: "workflow_enforcement"
  predecessor_manifest: "37 files; 2c6e3772fcfbd2eb68618486520d2d309b0594f8a1a7dafd2d3f32fd6ee76bcb"
  reviewed_candidate_manifest: "39 files; b0a0dfeae17aa4c56e3b9abe8e3104e3f8893f38387a31c577cf3b54401de2a4"
  implementation_performed: false
  installation_authorized: false
  synchronization_authorized: false
  app_server_execution_authorized: false
  task_creation_authorized: false
  dispatch_authorized: false
  canary_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  stop_conditions:
    - "contract, base, or reviewed candidate binding drift"
    - "implementation requires a third path"
    - "post-C manifest differs outside the two contracted validator rows"
    - "any required focused, aggregate, structural, or safety check fails"
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
    - "ADR-0004"
    - "ADR-0008"
    - "ADR-0011"
  protected_surfaces:
    - "workflow_enforcement"
  authority_conflicts_found: false
  authority_conflict_notes: "The owner-scoped WIP exception expires at the B handoff and does not transfer."
  stop_conditions:
    - "binding drift"
    - "nonexclusive aggregate blocker"
    - "unrelated Role Pool source change"
    - "third implementation path required"
```
