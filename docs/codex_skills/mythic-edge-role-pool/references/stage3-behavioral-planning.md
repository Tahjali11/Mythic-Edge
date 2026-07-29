# Stage-3 Behavioral-Planning Contract

Use `mythic_edge_role_pool_stage3_behavioral_planning.v1` only for the
deterministic, zero-effect Stage-3 planning proof. Here, **behavioral planning**
means testing how the planner classifies a fixed synthetic scenario. It does
not test a Codex child's behavior; fresh-agent behavior remains exclusively a
Stage-4 concern.

This document is not a `mythic_edge_role_pool_plan.v3` plan, a dispatch, a
claim, a reservation, a lease, a launch, a role artifact, a stage-advancement
receipt, or a finding-resolution receipt. Validate one observation with:

```powershell
py -B scripts\check_stage3_behavioral_planning.py <stage3-observation.json>
```

## Entry Evidence And Contract Transition

Every observation binds the independently reviewed Stage-2 pair with attempt
series `71753f13-17a3-490c-9ea1-217e7b955779`, including the exact portable
wrapper, decompressed pair, both observation byte hashes and self-digests,
evidence-index digests, and the accepted 30-file manifest.

The Stage-2 pair recorded its review status as pending when it was created; the
independent acceptance happened afterward. The Stage-3 entry therefore records
both facts and binds the exact transcript-preserved review receipt schema,
canonical length, byte hash, self-digest, and accepted verdict. It explicitly
sets `subsequent_review_receipt_storage: transcript_only` and
`separate_review_receipt_file_claimed: false`; it does not pretend that a
separate receipt file was persisted. The current user's instruction supplies
the acceptance authority for Stage-3 entry, while the exact Stage-2 hashes
remain independently replayable.

Adding this contract necessarily changed the installed manifest. The later
Stage-4 broker contract changes it again. The reviewed v3 and v4 successors and
the exact v5 contract candidate each use a separate narrow amendment below.
The `contract_transition` object compares the entire accepted
Stage-2 30-file snapshot with the current snapshot, permits only the named
Stage-3 additions, the broker-contract additions, and their exact
documentation/test wiring, and requires every other Stage-2 file to retain its
exact hash. The later broker reconciliation explicitly permits the small
fail-closed change to `scripts/check_pool_plan.py` that rejects direct Popen for
production and blocks the broker identity until its receipt-chain validator
exists. The transition states that Stage-2 evidence is historical and
immutable, not revalidated under the newer manifest, and grants no authority
expansion.

### External-isolation broker v3 manifest-transition amendment

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_transition_external_broker_v3_amendment.v1`
only to integrate this reviewed docs-only artifact into the deterministic
manifest transition:

```text
path=mythic-edge-role-pool/references/external-isolation-broker-v3-corrective-successor.md
change_kind=added
before_sha256=null
after_sha256=44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55
entry_manifest_file_count=30
pre_amendment_current_manifest_file_count=34
amended_current_manifest_file_count=35
```

The path and digest are one indivisible binding. The validator must fail closed
when the path is missing, renamed, case-varied, duplicated, replaced by a
reparse point, or has any other digest. A directory prefix, wildcard, glob,
extension rule, current-byte adoption, dynamically trusted digest, alternate
location, or additional allowed path is forbidden. The original four
`ALLOWED_ADDED_PATHS`, the existing `ALLOWED_MODIFIED_PATHS`, every Stage-2
baseline digest, and all transition semantics remain unchanged.

The future implementation is limited to:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

The validator must add the exact path to the closed added-path set and compare
its current manifest digest with the fixed `after_sha256` above before
constructing or accepting `contract_transition`. The transition `change_set`
must contain exactly one row for this artifact with the fixed path,
`change_kind`, `before_sha256`, and `after_sha256` values above.
The focused test may change the exact current count assertion from 34 to 35 and
must add digest-mismatch, missing-path, renamed-path, reparse-point-path,
extra-path, and unchanged-legacy-set negative cases. The reparse-point-path
case must prove refusal before transition acceptance and must not follow,
replace, hash, or adopt the target. Existing transition, zero-effect,
pair-validation, offline-guard, and false-authority tests must not be weakened,
deleted, skipped, or converted to advisory checks.

No other Role Pool file is implementation scope. In particular, do not change
`SKILL.md`, the parent external-isolation broker contract, the reviewed v3
corrective-successor contract, runtime validators, launchers, package content,
or Stage-4 authority. The reviewed v3 contract remains bound to the exact digest
above; a later change to that document requires a new reviewed digest and a new
manifest-transition contract amendment rather than automatic adoption.

This amendment is contract-only. It does not authorize Codex C or the two-file
implementation, regenerate a Stage-3 observation, revalidate historical
evidence, resolve a package finding, or authorize copying, building,
publication, installation, service mutation, canary execution, stage
advancement, or live use. After independent contract review, a new exact owner
activation is required before the two-file implementation. Until that
implementation passes the focused tests and the full Role Pool offline gate,
the manifest transition remains blocked and the Role Pool remains
`NOT LIVE-READY`.

### External-isolation broker v3 acceptance lifecycle reconciliation

The v3 contract's literal
`Status: contract_candidate_manifest_integration_blocked` records the
pre-amendment state of its exact reviewed bytes. It is not a mutable lifecycle
record and must not be edited merely to project later manifest work. This
amendment is the sole companion authority for the current manifest-integration
and contract-acceptance projection. It does not alter the v3 package contract,
create package authority, or close either package implementation finding.

The closed lifecycle vocabulary is:

```text
manifest_integration_blocked
final_review_pending
accepted_owner_activation_required
revision_required
superseded
```

The lifecycle is derived as follows:

| Lifecycle status | Required condition | `contract_acceptance_ready` | `exact_owner_activation_next_gate` | `ready_for_codex_c` | Next role |
| --- | --- | --- | --- | --- | --- |
| `manifest_integration_blocked` | The exact amendment route is not owner-selected, its implementation is absent, or its focused or full validation is not clean. | `false` | `false` | `false` | owner or Codex B |
| `final_review_pending` | The owner selected this exact amendment route; the exact v3 path and digest are present; the manifest implementation and required negative tests are present; focused validation and the full offline gate are clean; and independent review of this exact amended document is still pending. | `false` | `false` | `false` | Codex E |
| `accepted_owner_activation_required` | Codex E independently accepts the exact v3 contract, parent binding, current amendment bytes, manifest implementation review evidence, count-35 manifest transition, and clean full offline gate. | `true` | `true` | `false` | owner |
| `revision_required` | Any required binding, review, implementation, test, count, or gate result is missing, stale, contradictory, or failed. | `false` | `false` | `false` | Codex B or Codex D, according to the finding |
| `superseded` | The owner names an exact replacement route and its independent review accepts the replacement. | `false` | `false` | `false` | role named by the replacement |

The only permitted forward transition from the v3 contract's embedded blocked
snapshot is `manifest_integration_blocked -> final_review_pending`. Codex E may
then record either `accepted_owner_activation_required` or
`revision_required`. A corrected `revision_required` state returns only to
`final_review_pending` before another independent review. No lifecycle status
transitions to Codex C, package creation, package build, inventory creation,
publication, installation, service mutation, canary execution, stage
advancement, or live readiness. `superseded` is terminal for this amendment.

Lifecycle progress is recorded in an independent public-safe review or
workflow handoff, not by changing the pinned v3 bytes. The handoff must contain
exactly one lifecycle status and these required fields:

```text
lifecycle_schema=mythic_edge_role_pool_external_broker_v3_acceptance_lifecycle.v1
successor_path=references/external-isolation-broker-v3-corrective-successor.md
successor_sha256=44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55
parent_sha256=b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa
manifest_amendment_path=references/stage3-behavioral-planning.md
manifest_amendment_sha256=<exact reviewed current digest>
manifest_implementation_review_ref=<public-safe exact review reference>
manifest_file_count=35
offline_gate_status=<passed|failed>
offline_gate_tests_run=<nonnegative integer>
offline_gate_failures=<nonnegative integer>
offline_gate_errors=<nonnegative integer>
offline_gate_skips=<nonnegative integer>
acceptance_lifecycle_status=<one closed lifecycle literal>
contract_acceptance_ready=<derived boolean>
exact_owner_activation_next_gate=<derived boolean>
ready_for_codex_c=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
publication_authorized=false
installation_authorized=false
stage_advancement_authorized=false
live_ready=false
next_role=<role derived by the table>
```

`offline_gate_status=passed` requires zero failures, zero errors, and zero
skips. Unknown fields, placeholder values, multiple lifecycle statuses,
contradictory booleans, a digest mismatch, an unreviewed implementation, or a
non-clean gate derive `revision_required`. The independent review handoff may
cite the already confirmed `EIB-MANIFEST-E-001` and
`EIB-MANIFEST-IMPL-E-002` findings, but it must verify their exact evidence
again against the current bytes.

For this Codex B revision the projection is
`acceptance_lifecycle_status=final_review_pending`,
`contract_acceptance_ready=false`,
`exact_owner_activation_next_gate=false`, and `ready_for_codex_c=false`.
Only an accepted independent Codex E review may project
`accepted_owner_activation_required`. That status means the owner may consider
a new exact package-implementation activation; it is not that activation and
does not authorize package work.

### External-isolation broker v4 manifest-transition amendment

The owner selected the narrow manifest-amendment route for the independently
accepted v4 corrective-successor contract. This decision authorizes only this
Codex B amendment. It is not validator implementation authority, package
authority, or an activation of any later role.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_transition_external_broker_v4_amendment.v1`
only for this exact transition row:

```text
path=mythic-edge-role-pool/references/external-isolation-broker-v4-corrective-successor.md
change_kind=added
before_sha256=null
after_sha256=628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487
entry_manifest_file_count=30
pre_amendment_current_manifest_file_count=35
amended_current_manifest_file_count=36
```

The path and digest are indivisible. Missing, renamed, case-varied, duplicate,
reparse-point, replaced, extra, or digest-mismatched input fails before target
content is trusted or a transition is constructed. Wildcards, globs, directory
allowlists, extension rules, current-byte adoption, dynamic trust, alternate
locations, or additional paths are forbidden.

The implementation scope is exactly:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

A later activated implementation must:

1. add only the exact v4 path to the closed added-path set;
2. pin only the exact v4 digest above;
3. change the exact current manifest count from 35 to 36;
4. preserve the v3 path and digest, the previous five added paths, all modified
   path rules, every Stage-2 baseline digest, and all zero-effect semantics;
5. require exactly one v4 row in `contract_transition.change_set` with the four
   fixed row values above; and
6. refuse a reparse-point v4 path before following, opening, hashing, parsing,
   normalizing, or adopting its target.

The focused test matrix must cover the valid 36-file transition plus v4 digest
mismatch, missing path, renamed path, case variation, duplicate path,
reparse-point path, extra path, unexpected modified path, count 35, count 37,
changed v3 digest, missing v3 path, and changed legacy added-path set. Existing
transition, pair-validation, zero-effect, offline-guard, false-authority, v3
digest, and v3 reparse tests must remain active and unchanged in strength.

No other Role Pool file is implementation scope. Do not change `SKILL.md`,
either broker contract, package source, package bytes, launchers, Stage-4
authority, or any runtime schema. A required third file or weaker check routes
to Codex B before edits.

The closed v4 manifest lifecycle is:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

Its transitions are exact:

| Current status | Required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E accepts this exact amended document and its v4 binding. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a new exact, unexpired, single-attempt activation for only the two implementation files and required validation. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the activated files, records exact before/after hashes, and completes focused and full validation. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts exact implementation bytes, all negative tests, the 36-file transition, and a clean full offline gate. | `complete` |
| any nonterminal status | A binding, scope, validation, review, or authority requirement is missing, stale, contradictory, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route that receives independent review. | `superseded` |

Evaluate an accepted supersession first, then any failure condition, then one
positive transition row. Exactly one next status may result. A
`revision_required` handoff must name exactly one `revision_return_status`:
contract defects return to `contract_review_pending`, activation defects return
to `owner_activation_required`, and implementation or validation defects return
to `implementation_review_pending` after a bounded correction and fresh
evidence. `superseded` is terminal. No status may skip a row or be inferred
from contract acceptance, a clean test, or owner discussion alone.

The future implementation activation must bind this amendment's exact reviewed
SHA-256, the v4 contract path and SHA-256 above, exact pre-edit hashes for both
scripts, the two-file scope, all focused cases, the full offline gate, expiry,
and single-attempt consumption. It must keep package creation, source copy,
build, inventory, handoff publication, installation, service mutation, canary,
stage advancement, and live use false.

At completion of this Codex B thread:

```text
v4_manifest_lifecycle_status=contract_review_pending
v4_manifest_implementation_authorized=false
ready_for_codex_c=false
package_codex_c_authorized=false
package_creation_authorized=false
publication_authorized=false
installation_authorized=false
stage_advancement_authorized=false
live_ready=false
```

Even `v4_manifest_lifecycle_status=complete` means only that the deterministic
manifest recognizes the reviewed contract. A separate new exact owner
activation and all v4 package-contract gates remain required before package
Codex C may be considered.

### External-isolation broker v5 manifest-transition amendment

The owner authorized only this narrow Codex B contract-writing pass. The
authorization does not implement the manifest transition, accept the v5
contract, activate Codex C, or authorize package work.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_transition_external_broker_v5_amendment.v1`
only for this indivisible transition row:

```text
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
change_kind=added
before_sha256=null
after_sha256=0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea
entry_manifest_file_count=30
pre_amendment_current_manifest_file_count=36
amended_current_manifest_file_count=37
```

The path, case, change kind, null before value, digest, and counts form one
closed binding. A missing, renamed, case-varied, duplicated, extra, replaced,
non-ordinary, reparse-point, or digest-mismatched v5 path fails before the
transition is constructed or accepted. Wildcards, globs, directory allowlists,
extension rules, alternate locations, current-byte adoption, discovered
digests, caller-owned hashes, fallback substitution, or additional allowed
paths are forbidden.

The post-amendment `ALLOWED_ADDED_PATHS` set has exactly seven members. It
preserves all six current members and adds only the v5 path:

```text
mythic-edge-role-pool/references/external-isolation-broker.md
mythic-edge-role-pool/references/external-isolation-broker-v3-corrective-successor.md
mythic-edge-role-pool/references/external-isolation-broker-v4-corrective-successor.md
mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
mythic-edge-role-pool/references/stage3-behavioral-planning.md
mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py
mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py
```

The `ALLOWED_MODIFIED_PATHS` set remains exactly these thirteen members, with no
addition, removal, rename, alias, wildcard, or changed membership rule:

```text
mythic-edge-role-pool/SKILL.md
mythic-edge-role-pool/references/fallback-and-recovery.md
mythic-edge-role-pool/references/pool-state-schema.md
mythic-edge-role-pool/references/release-remediation-matrix.md
mythic-edge-role-pool/references/role-readiness-and-safety.md
mythic-edge-role-pool/references/stage4-canary-exception.md
mythic-edge-role-pool/scripts/check_pool_plan.py
mythic-edge-role-pool/scripts/codex_launcher_contract.py
mythic-edge-role-pool/scripts/run_release_tests.py
mythic-edge-role-pool/scripts/test_check_pool_plan.py
mythic-edge-role-pool/scripts/test_codex_launcher_contract.py
mythic-edge-role-pool/scripts/test_pool_results.py
mythic-edge-role-pool/scripts/test_skill_contract.py
```

The pinned-successor map must contain exactly the existing v3 and v4 entries
plus the v5 entry:

```text
external-isolation-broker-v3-corrective-successor.md=44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55
external-isolation-broker-v4-corrective-successor.md=628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487
external-isolation-broker-v5-corrective-successor.md=0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea
```

Those basenames are shorthand only inside this map; each owning path remains
the exact `mythic-edge-role-pool/references/` manifest path above. The v3 and v4
path, digest, ordinary-file, reparse-refusal, count, change-set, and lifecycle
rules remain unchanged. Every Stage-2 baseline row and all zero-effect,
historical-evidence, false-authority, and transition-ordering semantics also
remain unchanged.

The only future implementation paths are:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their current preimplementation SHA-256 values are respectively
`31059761eb15ff590de3d5d3657100f288ce408f2f98c60b5592e098de2c9e33`
and `1b9ed1dff49b1e459f34e049dfbf419ac13362067e5e3ec3877e10cdbef206b4`.
A later implementation activation must bind those exact bytes, this amendment's
independently reviewed digest, the exact v5 path and digest, the two-file scope,
the complete test matrix below, an expiry, and single-use consumption. A stale
pre-edit digest, third path, dependency change, weaker test, or broader effect
returns to Codex B before editing.

A future activated implementation must:

1. add only the exact v5 path to the current closed added-path set;
2. add only the exact v5 path and digest to the pinned-successor map;
3. change only `EXPECTED_CURRENT_MANIFEST_FILE_COUNT` from `36` to `37`;
4. include exactly one v5 `added` row with the four fixed row values in the
   sorted `contract_transition.change_set`;
5. preserve the existing six added paths, all thirteen modified paths, v3/v4
   pins, Stage-2 baselines, transition fields, and zero-effect behavior; and
6. subject the v5 path to exact-case enumeration and non-following metadata
   validation before any open, read, hash, parse, normalization, replacement,
   target adoption, or transition construction.

An ordinary v5 path is a present regular file with the exact basename and no
reparse-point or symbolic-link identity. Metadata failure, a directory, device,
pipe, socket, link, reparse point, duplicate case-insensitive representation,
or any other non-regular identity rejects. The reparse refusal must occur from
non-following metadata. It must not call target resolution, open or read target
bytes, compute a target hash, replace the path, or adopt a target-derived value.

The focused test matrix is mandatory and additive:

- accept the exact 37-row manifest and prove the v5 change-set row, path,
  digest, count, and sorted placement while all previous rows remain valid;
- reject a shape-valid but incorrect v5 digest;
- reject a missing v5 path and its resulting 36-row count;
- reject renamed and case-varied v5 paths;
- reject duplicate v5 rows and duplicate case-insensitive representations;
- reject every extra path and every 38-row projection;
- reject a changed digest for any existing path that is not already in the
  exact modified set;
- reject every manifest count other than 37, including 36 and 38, and reject a
  37-row substitution that has the wrong path set;
- reject missing, renamed, case-varied, or digest-changed v3 or v4 rows, any
  changed legacy added-path membership, any changed modified-path membership,
  any removed Stage-2 baseline path, and any weakened legacy transition rule;
- reject non-ordinary v5 metadata before `_manifest_row`, `read_bytes`, hashing,
  replacement, target adoption, or transition construction; and
- reject a v5 reparse point before following, resolving, opening, reading,
  hashing, replacing, or adopting its target.

Existing positive and negative transition, v3, v4, pair-validation,
zero-effect, offline-guard, structural, false-authority, protected-surface,
private-marker, and `NOT LIVE-READY` tests and gates must remain active and no
weaker. Tests may use invented temporary paths and mocked non-following metadata
only; they must not retain target bytes, paths, logs, or generated artifacts.

The closed v5 manifest lifecycle reuses the v4 vocabulary and ordering:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

Codex E may move `contract_review_pending` to `owner_activation_required` only
after independently accepting both the exact v5 contract digest and this exact
amendment. Owner discussion or this contract-writing authorization is not that
transition. Every transition is exact:

| Current status | Required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E accepts the exact v5 contract digest, this exact amendment, the closed 36-to-37 effect, and the two-file future scope. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a new exact, unexpired, single-use activation binding the independently reviewed amendment digest, v5 path and digest, both exact pre-edit file hashes, two-file scope, and complete validation matrix. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated files, records exact before/after hashes, and completes every focused test and the full offline gate. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, complete negative matrix, 37-file transition, legacy preservation evidence, clean full offline gate, residue result, and false-authority projection. | `complete` |
| any nonterminal status | A required contract, digest, path, count, authority, implementation, test, review, gate, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route and Codex E accepts that replacement. | `superseded` |

Evaluate accepted supersession first, then one failure row, then one positive
row. Exactly one next status may result. A contract or authority defect returns
to `contract_review_pending` or `owner_activation_required`, respectively. A
bounded implementation or validation defect returns to
`implementation_review_pending` only after a separately authorized correction
and fresh evidence. No status may skip a row, float to changed bytes, or derive
authority from discussion, contract acceptance, or a clean test alone.

`complete` means only that the deterministic manifest recognizes the exact v5
contract. It does not accept a package candidate or authorize preparation,
copying, build, inventory, handoff, publication, installation, service
mutation, canary execution, stage advancement, or live use.

At completion of this Codex B thread:

```text
v5_manifest_contract_writing_authorized=true
v5_manifest_lifecycle_status=contract_review_pending
v5_manifest_implementation_authorized=false
ready_for_codex_c=false
package_preparation_authorized=false
source_copy_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until the exact v5 contract and this amendment receive independent review, a
separate implementation activation is granted, the two-file implementation is
reviewed, and focused plus full offline validation are clean, the manifest
transition remains blocked and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 37-to-37 manifest-rebind amendment

The owner authorized only this narrow Codex B amendment-writing pass. The
underlying v5 recipe and contract received an accepted independent review, but
that review grants no implementation or package authority. Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v1`
only for this closed existing-path digest rebind:

```text
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
rebind_change_kind=existing_path_digest_rebind
stage2_change_set_kind=added_preserved
before_sha256=0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea
after_sha256=d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
review_ref=build_recipe_review_v1_ec08ac6d109ec6aab653a6b4976309a7
review_receipt_digest=323ca61d9742da1030b4282c50a88ce9acc9417f73241dd5ba042ac49fa604cf
review_status=accepted_exact_recipe_and_contract
reviewed_at_utc=2026-07-16T16:50:59Z
review_receipt_storage=transcript_only
```

This is not a second `36_to_37` transition. The v5 path remains an `added` row
relative to the immutable Stage-2 30-file baseline, while this amendment changes
only that row's pinned `after_sha256` in the already established 37-file current
manifest. The exact 37-path set, seven-member `ALLOWED_ADDED_PATHS`,
thirteen-member `ALLOWED_MODIFIED_PATHS`, three-entry pinned-successor map,
v3/v4 paths and digests, Stage-2 baselines, historical transition rows, ordering,
counts, zero-effect rules, false-authority fields, non-claims, and every legacy
positive and negative check remain unchanged. A count change, path-set change,
second v5 row, alternate change-kind projection, or modification to any other
pin is contradictory and fails closed.

The accepted receipt is exactly the following one-line canonical JSON object
followed by one LF. The Markdown fences are not receipt bytes:

```json
{"build_recipe_execution_compatibility_claimed":false,"build_recipe_independent_review_status":"accepted_exact_recipe_and_contract","build_recipe_ref":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_schema":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_sha256":"4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3","canary_authorized":false,"contract_review_verdict":"accepted","correctness_claimed":false,"finding_ids":[],"handoff_creation_authorized":false,"historical_v4_command_tuple_verified":false,"implementation_authorized":false,"installation_authorized":false,"inventory_creation_authorized":false,"live_ready":false,"manifest_rebind_authorized":false,"next_role":"owner_manifest_rebind_decision","package_build_authorized":false,"package_creation_authorized":false,"privacy_assurance_claimed":false,"production_readiness_claimed":false,"publication_authorized":false,"ready_for_codex_c":false,"ready_for_codex_d":false,"ready_for_codex_f":false,"receipt_digest":"323ca61d9742da1030b4282c50a88ce9acc9417f73241dd5ba042ac49fa604cf","receipt_storage":"transcript_only","recipe_definition_verdict":"conformant","release_readiness_claimed":false,"review_receipt_kind":"build_recipe_contract_review","review_receipt_schema":"mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1","review_ref":"build_recipe_review_v1_ec08ac6d109ec6aab653a6b4976309a7","reviewed_at_utc":"2026-07-16T16:50:59Z","reviewed_contract_id":"mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1","reviewed_contract_path":"references/external-isolation-broker-v5-corrective-successor.md","reviewed_contract_sha256":"d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967","reviewer_role":"codex_e_independent_reviewer","security_assurance_claimed":false,"separate_review_receipt_file_claimed":false,"service_mutation_authorized":false,"stage_advancement_authorized":false}
```

The receipt has exactly 41 keys. Duplicate or unknown keys reject. Validation
must parse strict UTF-8 JSON, reject noncanonical bytes, and recompute rather
than trust either supplied digest. First omit `review_ref` and `receipt_digest`,
canonicalize with sorted keys and one final LF, and derive
`build_recipe_review_v1_` plus the first 32 lowercase hexadecimal characters of
SHA-256. The result must equal
`build_recipe_review_v1_ec08ac6d109ec6aab653a6b4976309a7`. Then restore
`review_ref`, omit only `receipt_digest`, and recompute SHA-256; the result must
equal `323ca61d9742da1030b4282c50a88ce9acc9417f73241dd5ba042ac49fa604cf`.
The complete reproduced object includes that exact `receipt_digest`; only the
digest preimage omits it, exactly as defined by the reviewed v5 contract.

Receipt cross-field validation must prove the sole accepted row:
`recipe_definition_verdict=conformant`, `contract_review_verdict=accepted`, an
empty `finding_ids` array,
`build_recipe_independent_review_status=accepted_exact_recipe_and_contract`,
and `next_role=owner_manifest_rebind_decision`. Every authority, readiness, and
claim Boolean in the receipt must be `false`; `receipt_storage` must be
`transcript_only`; and `separate_review_receipt_file_claimed` must be `false`.
A missing, malformed, stale, contradictory, cross-contract, cross-recipe,
cross-receipt, shape-valid-but-incorrect, differently ordered, or differently
timestamped object rejects. Reproduction here does not claim that a separate
receipt file exists.

The only future implementation paths are:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`4c7386640632682ddffca5e054e8adc4f44e7264b137d084c3e250dad9b81e4e` and
`992ed76fdb35f8c768c8ffb1eb5eea8285e8bb1a978502ef21cf4b251b520d87`.
A future owner activation must bind those bytes, this independently reviewed
amendment digest, the complete receipt and its two derived identifiers, the
recipe digest, the predecessor and target contract digests, the unchanged
37-path set and count, the complete test matrix below, expiry, and single-use
consumption. Any stale pre-edit digest, third path, dependency change, weaker
test, fallback, or broader effect returns to Codex B before editing.

A future activated implementation may only replace the exact v5 pinned digest
with the target digest and add or update focused validation for this rebind. It
must keep `EXPECTED_CURRENT_MANIFEST_FILE_COUNT=37`, preserve the path sets and
all other pins byte-for-byte, and preserve the v5 row's historical Stage-2
`added` classification. It must never discover, adopt, normalize, or substitute
the current digest. Before opening or hashing the v5 contract, it must enumerate
the exact-case path and use non-following metadata to prove that the path is a
present ordinary file and not a symbolic link or reparse point. Metadata failure
or a non-ordinary identity rejects before following, resolving, opening,
reading, hashing, replacing, or adopting any target.

The focused validation matrix is mandatory and additive:

- accept the exact 37-path current state with the target v5 digest, unchanged
  path set and count, exact recipe and receipt bindings, and all legacy rows;
- reject target digest mismatch, including a correctly shaped but incorrect
  digest, and reject dynamic current-byte adoption;
- reject a missing, renamed, case-varied, duplicated, or extra v5 path;
- reject any extra path, any 36- or 38-row count, any other count drift, and a
  37-row substitution with a different path set;
- reject modification of any existing non-v5 path or digest, including v3/v4,
  any Stage-2 baseline, either allowed-path set, or any legacy transition row;
- reject a non-ordinary v5 path before open, read, hash, replacement, target
  adoption, or transition construction;
- reject a v5 reparse point before following, resolving, opening, reading,
  hashing, replacing, or adopting its target;
- reject receipt drift in any field, key set, order, reference, digest,
  timestamp, verdict, status, next role, false-authority flag, or non-claim;
- reject recipe schema or digest drift, predecessor digest drift, target digest
  drift, transition-kind drift, and any count-changing reclassification; and
- rerun every existing v3, v4, original v5, pair-validation, zero-effect,
  structural, protected-surface, private-marker, offline-guard,
  false-authority, `NOT LIVE-READY`, and legacy-regression test no weaker than
  before.

The lifecycle for this rebind amendment is closed and non-skippable:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E independently accepts this exact amendment digest, the reproduced receipt, the predecessor/target/recipe bindings, the 37-to-37 effect, and the two-file future scope. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a new exact, unexpired, single-use activation binding every required value named above. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated files and records exact before/after hashes with complete focused and offline evidence. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, complete negative matrix, unchanged 37-path manifest, legacy preservation, clean gates, zero residue, and false-authority projection. | `complete` |
| any nonterminal status | Any required path, digest, count, receipt, recipe, authority, implementation, test, review, gate, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then exactly one applicable failure row,
then exactly one positive row. No status may skip a row, infer authority from
semantic acceptance, tests, or discussion, or float to changed bytes. A
contract or authority defect routes back to Codex B or the owner respectively;
a bounded implementation defect may return only through a separately authorized
Codex D correction and fresh Codex E evidence. `complete` means only that the
deterministic Stage-3 manifest recognizes the exact reviewed v5 contract digest.

At completion of this Codex B thread:

```text
v5_contract_review_status=accepted_semantics_manifest_pending
v5_contract_semantics_accepted=true
v5_manifest_rebind_contract_writing_authorized=true
v5_manifest_rebind_lifecycle_status=contract_review_pending
v5_manifest_rebind_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_bound_v5_sha256=0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea
manifest_target_v5_sha256=d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967
manifest_integration_complete=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
package_preparation_authorized=false
source_copy_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until this exact amendment is independently accepted, a new exact owner
activation is granted, the two-file implementation is independently reviewed,
and every focused and full offline gate is clean, the rebind remains incomplete
and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 static-preflight 37-to-37 manifest-rebind amendment v2

The v1 amendment above is immutable completed lineage. Its implementation
established the exact 37-path manifest and current
`d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967`
v5 pin; this v2 amendment neither rewrites nor reuses that single transition.
The owner authorized only this narrow Codex B amendment-writing pass. Use
amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v2`
for the following successor rebind:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v1
predecessor_amendment_lifecycle_status=complete
predecessor_binding_preserved_as_history=true
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
rebind_change_kind=existing_path_digest_rebind
stage2_change_set_kind=added_preserved
before_sha256=d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967
after_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
review_ref=build_recipe_review_v1_5dd95cd9042f9ba5be885675f8fab52d
review_receipt_digest=9e074c23202ecdb0f0f7d1ff8ef7c391d5e555e14897620793d84b53af3ec6ab
review_status=accepted_exact_recipe_and_contract
reviewed_at_utc=2026-07-16T21:03:30Z
review_receipt_storage=transcript_only
```

The transition changes exactly one existing manifest value from `before_sha256`
to `after_sha256`. It leaves the 37 paths, seven-member
`ALLOWED_ADDED_PATHS`, thirteen-member `ALLOWED_MODIFIED_PATHS`, v3/v4 pins,
Stage-2 baselines, the v1 transition and receipt, row order, zero-effect rules,
false-authority fields, non-claims, and every legacy check unchanged. A second
row, count change, path-set change, v1 mutation, alternate change-kind, or any
other digest change is contradictory and fails closed.

The accepted v2 receipt is exactly this one-line canonical JSON object followed
by one LF. The Markdown fences are not receipt bytes:

```json
{"build_recipe_execution_compatibility_claimed":false,"build_recipe_independent_review_status":"accepted_exact_recipe_and_contract","build_recipe_ref":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_schema":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_sha256":"4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3","canary_authorized":false,"contract_review_verdict":"accepted","correctness_claimed":false,"finding_ids":[],"handoff_creation_authorized":false,"historical_v4_command_tuple_verified":false,"implementation_authorized":false,"installation_authorized":false,"inventory_creation_authorized":false,"live_ready":false,"manifest_rebind_authorized":false,"next_role":"owner_manifest_rebind_decision","package_build_authorized":false,"package_creation_authorized":false,"privacy_assurance_claimed":false,"production_readiness_claimed":false,"publication_authorized":false,"ready_for_codex_c":false,"ready_for_codex_d":false,"ready_for_codex_f":false,"receipt_digest":"9e074c23202ecdb0f0f7d1ff8ef7c391d5e555e14897620793d84b53af3ec6ab","receipt_storage":"transcript_only","recipe_definition_verdict":"conformant","release_readiness_claimed":false,"review_receipt_kind":"build_recipe_contract_review","review_receipt_schema":"mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1","review_ref":"build_recipe_review_v1_5dd95cd9042f9ba5be885675f8fab52d","reviewed_at_utc":"2026-07-16T21:03:30Z","reviewed_contract_id":"mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1","reviewed_contract_path":"references/external-isolation-broker-v5-corrective-successor.md","reviewed_contract_sha256":"85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704","reviewer_role":"codex_e_independent_reviewer","security_assurance_claimed":false,"separate_review_receipt_file_claimed":false,"service_mutation_authorized":false,"stage_advancement_authorized":false}
```

The receipt has exactly 41 keys. Validation uses strict UTF-8 without BOM,
rejects duplicate and unknown keys, requires sorted object keys, no
insignificant whitespace, and one final LF. Omitting `review_ref` and
`receipt_digest` and hashing the canonical bytes must derive
`build_recipe_review_v1_5dd95cd9042f9ba5be885675f8fab52d`. Restoring
`review_ref`, omitting only `receipt_digest`, and hashing again must derive
`9e074c23202ecdb0f0f7d1ff8ef7c391d5e555e14897620793d84b53af3ec6ab`.
The complete object must bind the accepted contract, recipe, timestamp, empty
finding list, accepted verdicts, owner-manifest-rebind next role, transcript-only
storage, and every authority, readiness, assurance, and claim Boolean as
`false`. Reproduction here does not claim a separate receipt file exists.

The revised static-preflight bindings are exact:

```text
timestamp_floor_matrix_counts_sha256=94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792
failure_matrix_counts_sha256=2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef
projection_matrix_counts_sha256=8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06
parent_edit_envelope_sha256=f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1
candidate_edit_envelope_sha256=32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed
candidate_operation_matrix_sha256=f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d
future_activation_requirements_sha256=a22fb76fee01c5c30ada6858458632ede488e1e960ef2dbdf15a656abbd18dd1
static_preflight_sha256=c15f4b6899d28628dfb7649d65147407ce640f7a1d910143ba286b5a33b22b35
```

A future implementation must recompute these values from the accepted v5
contract and reject an omitted, extra, renamed, reordered, duplicate,
differently typed, alternate-preimage, stale, cross-amendment, or wrong-digest
value. It must preserve the contract's exact matrix dimensions and
expected/accepted/rejected counts, prove the candidate two-path edit envelope
is a strict subset of the four-path parent envelope, and bind this amendment,
scope, matrices, recipe, tests, and future activation as one review packet.

The only future implementation paths are:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`bc794bbd2fa573c4bb97aa5c504af4c4a7ca9f9931ba4d0f4293fd5f2dcb8de6`
and
`d48458dabe7e8aa5cddb6e3c569ff3fd03664702b732990fab3f2630d038b02a`.
A future owner activation must bind those bytes, the independently reviewed
v2 amendment digest, both v2 receipt identifiers, the contract and recipe
digests, predecessor and target, unchanged manifest, complete test matrix,
expiry, and single-use consumption. No current authorization follows from this
section.

A future activated implementation may update only the validator's exact v5 pin
from the predecessor to the target and add the corresponding focused v2
bindings and tests. The test file must retain the complete v1 receipt,
predecessor, target, amendment, and transition as immutable legacy evidence;
v2 values must be separately named and validated. Neither file may discover,
adopt, normalize, substitute, or infer a digest from current bytes.

The focused validation matrix is mandatory:

- accept exactly the 37-path manifest with the target digest, unchanged path
  classifications, exact v2 receipt, recipe, static-preflight bindings, and all
  legacy rows;
- reject the predecessor digest after v2 activation, every wrong target,
  correctly shaped but incorrect digest, and dynamic current-byte adoption;
- reject a missing, renamed, case-varied, duplicate, or extra v5 path, any
  unrelated extra path, any count other than 37, and a 37-row path substitution;
- reject modification of every non-v5 path or digest, including v3/v4, the v1
  predecessor/target/receipt/amendment evidence, Stage-2 baselines, allowed-path
  sets, and legacy transitions;
- reject non-ordinary and reparse-point v5 paths before following, resolving,
  opening, reading, hashing, replacing, or adopting a target;
- reject drift in any of the 41 receipt keys, ordering, reference, digest,
  timestamp, verdict, status, next role, false-authority flag, or non-claim;
- reject drift in any static-preflight vector, matrix count, envelope,
  candidate-operation matrix, recipe, amendment, predecessor, target, or
  transition field; and
- rerun every existing v3, v4, v1-v5-rebind, pair-validation, zero-effect,
  structural, protected-surface, private-marker, offline-guard,
  false-authority, `NOT LIVE-READY`, and legacy-regression test without
  weakening it.

The v2 lifecycle uses the same closed vocabulary without reusing v1 state:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E independently accepts this exact v2 amendment digest, complete receipt, static vectors, predecessor/target/recipe bindings, 37-to-37 effect, and two-file future scope. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a new exact, unexpired, single-use activation binding every required v2 value. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated files and records exact before/after hashes with complete focused and offline evidence. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts exact implementation bytes, all positive and negative tests, unchanged 37 paths, preserved legacy evidence, clean gates, zero residue, and false-authority projection. | `complete` |
| any nonterminal status | Any required binding, authority, implementation, test, review, gate, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then exactly one failure row, then exactly
one positive row. No status may skip a row, infer authority from acceptance or
validation, or float to changed bytes. `complete` means only that the
deterministic Stage-3 manifest recognizes the exact independently reviewed
v5 digest.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_lifecycle_status=complete
v5_manifest_rebind_v2_contract_writing_authorized=true
v5_manifest_rebind_v2_lifecycle_status=contract_review_pending
v5_manifest_rebind_v2_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_bound_v5_sha256=d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967
manifest_target_v5_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_integration_complete=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
package_preparation_authorized=false
source_copy_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until independent review accepts this exact v2 amendment, a new owner
activation is granted, its two-file implementation is independently reviewed,
and all focused and offline gates are clean, the current manifest remains bound
to the predecessor and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 finite-oracle 37-to-37 manifest-rebind amendment v3

The installed 37-path manifest currently binds the exact v5 predecessor
`85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704`.
The current v5 contract is an ordinary, non-reparse file whose independently
accepted digest is
`db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6`.
The owner approved only this narrow manifest-rebind amendment-writing pass.
That approval does not implement the rebind or authorize Codex C, package,
installation, service, canary, stage, or live operations.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v3`
for exactly this successor transition:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v2
predecessor_manifest_binding_status=implemented_current
predecessor_binding_preserved_as_history=true
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
rebind_change_kind=existing_path_digest_rebind
stage2_change_set_kind=added_preserved
before_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
after_sha256=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
review_evidence_schema=mythic_edge_role_pool_v5_finite_oracle_contract_confirmation.v1
review_evidence_sha256=8fbd16905c63f57bc6c8320673c93b39d0c46777da853411d8695f237868ea8c
atomic_observation_oracle_tuple_count=768
atomic_observation_oracle_outcome_counts=[1,1,45,4,717]
atomic_observation_oracle_sha256=19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269
contract_review_verdict=accepted_within_approved_scope
contract_review_status=accepted_semantics_manifest_pending
```

The transition changes exactly one existing manifest digest. It keeps the
37-path set, current path classifications, v3/v4 bindings, Stage-2 baselines,
v1 and v2 amendment lineage, row ordering, zero-effect behavior, false-authority
fields, and non-claims unchanged. A count change, path addition or removal,
second v5 row, alternate change-kind, predecessor substitution, dynamic digest
adoption, or modification to any other digest is contradictory and fails
closed.

The Codex E evidence supplied for this amendment is the following exact
canonical JSON object followed by one LF. The Markdown fences are not evidence
bytes:

```json
{"contract_review_status":"accepted_semantics_manifest_pending","contract_verdict":"accepted_within_approved_scope","edits_performed":false,"finding_id":"EIB-PKG-V5-ATOMIC-E-001","finding_status":"fixed_confirmed","implementation_performed":false,"installation_performed":false,"live_ready":false,"manifest_integration_complete":false,"manifest_rebind_authorized":false,"manifest_rebind_may_be_considered_next":true,"next_role":"owner_manifest_rebind_decision_then_codex_b_exact_37_to_37_amendment","oracle_outcome_counts":[1,1,45,4,717],"oracle_sha256":"19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269","oracle_tuple_count":768,"package_operations_performed":false,"review_evidence_schema":"mythic_edge_role_pool_v5_finite_oracle_contract_confirmation.v1","reviewer_role":"codex_e_independent_reviewer","scope_classification":"contract_defect_within_baseline","semantic_review_completed":true,"service_or_canary_performed":false,"source_sha256":"db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6","stage_advancement_authorized":false}
```

Canonical evidence validation requires strict UTF-8 without BOM, sorted unique
keys, exact JSON types and values, no insignificant whitespace, and one final
LF. Hashing those complete bytes must derive
`8fbd16905c63f57bc6c8320673c93b39d0c46777da853411d8695f237868ea8c`.
The object is an in-document binding of the current owner-supplied Codex E
handoff; it claims no separate receipt file and grants no implementation or
package authority.

The finite oracle is a mandatory semantic binding, not an implementation
artifact. Future validation must require exactly 768 tuples, exact outcome
counts `[1,1,45,4,717]`, and oracle digest
`19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269`.
An omitted, reordered, differently typed, alternate, or correctly shaped but
incorrect tuple count, outcome vector, finding status, source digest, or oracle
digest fails closed.

Only these two files may be changed by a separately activated implementation:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`3919933a2853c31da77b0de2fb983688b33ca647a6af17b3dd0cdcba05f83a8f`
and
`acea619c49d8fab7b3ae2875239d1814599089010d7957d66d32e95bc700fbc4`.
The accepted v5 contract and this planning document are read-only inputs to
that implementation. The implementation must stop before editing if either
script digest, the 37-path manifest, the predecessor digest, the accepted v5
contract digest, or the independently accepted amendment digest drifts.

A later exact owner activation must bind the independently reviewed v3
amendment digest, both script digests, predecessor and target digests, unchanged
37-path set, review-evidence digest, finite-oracle bindings, complete test
matrix, expiry, and single-use lifecycle. Current manifest-rebind approval
authorizes contract writing only and cannot be consumed as Codex C authority.

The focused validation matrix is mandatory:

- accept exactly 37 current manifest rows with the v5 target digest and every
  non-v5 path, digest, classification, and order unchanged;
- reject the predecessor after activated implementation, every wrong target,
  dynamic current-byte adoption, caller-supplied digest substitution, and a
  correctly shaped but incorrect target;
- reject missing, renamed, case-varied, duplicate, extra, or substituted paths
  and every manifest count other than 37;
- reject modification of v3/v4, v1/v2 rebind lineage, Stage-2 baselines,
  allowed path sets, zero-effect rules, or any non-v5 digest;
- reject a non-ordinary v5 path before opening or hashing and reject a reparse
  point before following, resolving, opening, reading, hashing, replacing, or
  adopting its target;
- reject any drift in the exact review-evidence object, its digest, finding ID,
  finding status, scope class, semantic verdict, false-authority values, tuple
  count, outcome counts, or oracle digest;
- reject any amendment, predecessor, target, script, count, path-set, lifecycle,
  or authority mismatch before manifest mutation;
- preserve every existing v3, v4, original v5, v1/v2 rebind, receipt,
  static-preflight, pair-validation, zero-effect, structural, protected-surface,
  private-marker, offline, false-authority, `NOT LIVE-READY`, and legacy test;
  and
- prove rollback leaves the predecessor pin and all 37 paths unchanged when a
  pre-write check fails, while a post-write validation failure restores the
  exact predecessor bytes or fails closed without claiming completion.

The Codex B preimplementation release gate is an observed fail-closed snapshot,
not a future acceptance count: structural validation passed, 329 tests ran, and
51 tests ended in errors. Forty-eight tracebacks terminated at the expected
unimplemented v5 pinned-digest mismatch. Three terminated because the legacy v2
static-vector helper requires one future-activation JSON vector that is absent
from the accepted current v5 contract. A later activated implementation must
close both causes inside the two-file scope: preserve and validate the immutable
v2 vector from its owning v2 amendment evidence, and validate the v3 finite
oracle and target binding from this amendment. It must not infer a legacy vector
from current v5 bytes, weaken the v2 regression checks, or treat these observed
counts as permission to ignore a different failure after implementation.

The v3 lifecycle uses the existing closed manifest-amendment vocabulary:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E independently accepts this exact v3 amendment digest, the 37-to-37 effect, current predecessor evidence, canonical review evidence, oracle bindings, two-file scope, lifecycle, test matrix, false-authority fields, and non-claims. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a fresh exact, unexpired, single-use activation binding every required v3 value. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated files and records exact before/after hashes, focused tests, full offline evidence, and rollback/residue results. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts exact implementation bytes, complete positive and negative tests, the unchanged 37 paths, target digest, preserved legacy evidence, clean gates, zero residue, and false-authority projection. | `complete` |
| any nonterminal status | Any authority, binding, implementation, test, review, rollback, gate, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then one failure row, then one positive
row. No status skips a row or inherits authority from review or validation.
`complete` means only that the deterministic Stage-3 manifest recognizes the
accepted v5 contract digest. The v5 contract's embedded status is an immutable
snapshot of its pre-integration state and must not be edited merely to project
manifest completion; current manifest lifecycle is owned by this amendment,
the validator implementation, and independent review evidence.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_binding_preserved=true
v5_manifest_rebind_v2_binding_preserved=true
v5_manifest_rebind_v3_contract_writing_authorized=true
v5_manifest_rebind_v3_lifecycle_status=contract_review_pending
v5_manifest_rebind_v3_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_bound_v5_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_target_v5_sha256=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
manifest_integration_complete=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
package_preparation_authorized=false
source_copy_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until Codex E accepts this exact v3 amendment, a fresh owner activation is
granted, the two-file implementation is independently reviewed, and focused
plus full offline gates are clean, the manifest remains bound to the
predecessor and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 current-recipe receipt-binding amendment v4

The installed 37-path manifest now recognizes the exact v5 contract digest
`db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6`.
The accepted v3 amendment and its implementation remain immutable lineage. A
later independent Codex E review accepted the unchanged v5 build recipe for
those exact current contract bytes, but the receipt exists only in the owner-
supplied transcript. The owner approved this narrow docs-only amendment-writing
pass so that the receipt can become a deterministic future activation input.
That approval does not implement this amendment or authorize candidate
preparation, activation consumption, package work, installation, canary work,
stage advancement, or live use.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v4`
for exactly this stable-path, stable-contract-digest receipt binding:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v3
predecessor_manifest_binding_status=implemented_current
transition_kind=37_to_37_review_receipt_binding
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
v5_contract_sha256_before=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
v5_contract_sha256_after=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
v5_contract_digest_change=none
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
build_recipe_independent_review_ref=build_recipe_review_v1_6128230418da966dd28bdc271edbf6d9
build_recipe_independent_review_sha256=b0db654fce1316984c7e0380b85e77caadac580a256313bc2f41bb872c32667f
build_recipe_independent_review_status=accepted_exact_recipe_and_contract
reviewed_at_utc=2026-07-17T01:41:59Z
receipt_storage=transcript_only
current_static_preflight_sha256=7bd7855164cfd0b70f3f51b0b4c97b82ca1237b32a0cea0bef8960f90bea5fcd
receipt_binding_status=contract_review_pending
```

The transition changes no manifest path, path classification, contract digest,
v3/v4 binding, Stage-2 baseline, allowed-added set, allowed-modified set,
operation matrix, finite oracle, build recipe, or authority rule. It makes the
complete current-contract recipe receipt a required in-document input to the
existing v5 static-preflight and candidate-activation boundary. A count change,
path or contract-digest change, second v5 row, dynamic digest adoption, prior-
receipt substitution, or change to another manifest binding is contradictory
and fails closed.

The complete accepted receipt is the following exact canonical JSON object
followed by one LF. The Markdown fences are not receipt bytes:

```json
{"build_recipe_execution_compatibility_claimed":false,"build_recipe_independent_review_status":"accepted_exact_recipe_and_contract","build_recipe_ref":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_schema":"mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_sha256":"4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3","canary_authorized":false,"contract_review_verdict":"accepted","correctness_claimed":false,"finding_ids":[],"handoff_creation_authorized":false,"historical_v4_command_tuple_verified":false,"implementation_authorized":false,"installation_authorized":false,"inventory_creation_authorized":false,"live_ready":false,"manifest_rebind_authorized":false,"next_role":"owner_manifest_rebind_decision","package_build_authorized":false,"package_creation_authorized":false,"privacy_assurance_claimed":false,"production_readiness_claimed":false,"publication_authorized":false,"ready_for_codex_c":false,"ready_for_codex_d":false,"ready_for_codex_f":false,"receipt_digest":"b0db654fce1316984c7e0380b85e77caadac580a256313bc2f41bb872c32667f","receipt_storage":"transcript_only","recipe_definition_verdict":"conformant","release_readiness_claimed":false,"review_receipt_kind":"build_recipe_contract_review","review_receipt_schema":"mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1","review_ref":"build_recipe_review_v1_6128230418da966dd28bdc271edbf6d9","reviewed_at_utc":"2026-07-17T01:41:59Z","reviewed_contract_id":"mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1","reviewed_contract_path":"references/external-isolation-broker-v5-corrective-successor.md","reviewed_contract_sha256":"db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6","reviewer_role":"codex_e_independent_reviewer","security_assurance_claimed":false,"separate_review_receipt_file_claimed":false,"service_mutation_authorized":false,"stage_advancement_authorized":false}
```

Receipt validation is exact and mechanical. Parse strict UTF-8 JSON with no
BOM, duplicate keys, unknown keys, insignificant whitespace, or missing final
LF. Require exactly 41 keys and the exact types and values above. Omit
`review_ref` and `receipt_digest`, canonicalize, hash, and derive exactly
`build_recipe_review_v1_6128230418da966dd28bdc271edbf6d9`. Restore
`review_ref`, omit only `receipt_digest`, canonicalize, and derive exactly
`b0db654fce1316984c7e0380b85e77caadac580a256313bc2f41bb872c32667f`.
The contract and recipe digests must be recomputed from their owning current
bytes and canonical recipe object rather than accepted from this amendment.

The earlier `d8ef...` and `85ba...` recipe receipts remain historical lineage
only. Neither may satisfy this binding. Missing, stale, malformed, reordered,
differently typed, contradictory, cross-contract, cross-recipe, cross-revision,
correctly shaped but incorrect, or authority-bearing receipt data fails closed.
No consumer may reconstruct a current receipt from a prior receipt plus an
unchanged recipe digest.

Only these two files may be changed by a separately activated implementation:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`5fdd0b4c66bbaa698cc65294a5d458a161a7b1bfd2dc0e597974c59be28954d4`
and
`ca3712a9b626bc214f237afa29bfa7ec548ed544c7f14268c9363a96df08d1c1`.
The accepted v5 contract and this planning document are read-only inputs to
that implementation. Drift in either script, the contract, recipe, 37-path
manifest, v3 amendment lineage, or independently accepted v4 amendment digest
stops before editing.

The focused validation matrix is mandatory:

- accept exactly the canonical 41-key current-contract receipt and recompute
  both its symbolic reference and receipt digest;
- reject each omitted, extra, renamed, duplicated, reordered, differently
  typed, alternate-preimage, or one-field-mutated receipt value;
- reject either historical receipt, the current receipt with a historical
  contract digest, and any attempt to float review across contract revisions;
- reject a wrong contract, recipe, review reference, receipt digest, timestamp,
  status, next role, finding array, storage mode, or false-authority value;
- preserve the exact 37-path set and current `db32...` v5 manifest binding and
  reject every path, count, case, nonordinary-file, reparse-point, or unrelated
  manifest mutation;
- refuse a reparse path before following, resolving, opening, reading, hashing,
  replacing, or adopting its target;
- recompute the accepted amendment digest after independent review and derive a
  successor static-preflight digest by changing only
  `manifest_rebind_amendment_sha256` in the otherwise exact current 25-field
  static-preflight object;
- reject the predecessor static-preflight digest after implementation, every
  wrong amendment or preflight digest, and shape-valid caller substitution;
- preserve all v1 through v3 amendment, finite-oracle, matrix, zero-effect,
  structural, protected-surface, private-marker, offline, false-authority,
  `NOT LIVE-READY`, and legacy checks; and
- prove every failure leaves the current 37-path manifest and `db32...` v5
  binding unchanged and creates no activation, candidate, package, or residue.

The Codex B preimplementation gate is an observed fail-closed snapshot, not an
acceptance count. The focused Stage-3 suite ran 65 tests and ended with exactly
three errors; the full offline gate ran 334 tests, structural validation passed,
and the same three errors remained. Every error was
`v5 manifest-rebind v3 binding drift` because the current helper hashes this
whole planning document as the v3 amendment while also requiring its immutable
pre-v4 digest. A later activated implementation must preserve the exact v3
digest as historical lineage and validate the new v4 amendment digest and
receipt separately. Any additional, differently caused, failed, skipped, or
unavailable result blocks rather than being accepted as part of this snapshot.

The v4 amendment lifecycle reuses the existing closed amendment vocabulary:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E independently accepts this exact amendment digest, canonical receipt, no-digest-change manifest effect, two-file scope, lifecycle, tests, and non-claims. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a fresh exact, unexpired, single-use implementation activation binding the reviewed amendment digest, both script digests, receipt reference and digest, contract and recipe digests, 37-path state, test matrix, and false-authority fields. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated files and records exact before/after hashes, receipt and preflight derivations, focused tests, full offline evidence, and zero residue. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, receipt reproduction, successor static-preflight digest, preserved 37 paths and `db32...` binding, complete negative tests, clean gates, and false-authority projection. | `complete` |
| any nonterminal status | Any authority, binding, implementation, test, review, rollback, gate, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement route and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then one failure row, then one positive
row. No status skips a row or inherits implementation authority from this
contract-writing approval. `complete` means only that the deterministic
Stage-3 boundary durably recognizes the exact current recipe receipt and its
transitive static-preflight binding. It does not create or consume candidate-
preparation authority.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_binding_preserved=true
v5_manifest_rebind_v2_binding_preserved=true
v5_manifest_rebind_v3_binding_preserved=true
v5_manifest_rebind_v4_contract_writing_authorized=true
v5_manifest_rebind_v4_lifecycle_status=contract_review_pending
v5_manifest_rebind_v4_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_bound_v5_sha256=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
manifest_v5_digest_change=none
current_recipe_review_receipt_reproduced=true
current_recipe_review_receipt_bound_for_execution=false
static_preflight_predecessor_sha256=7bd7855164cfd0b70f3f51b0b4c97b82ca1237b32a0cea0bef8960f90bea5fcd
successor_static_preflight_status=pending_reviewed_amendment_digest_and_implementation
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
candidate_preparation_authorized=false
activation_creation_authorized=false
activation_consumption_authorized=false
source_copy_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until independent Codex E review accepts this exact v4 amendment, a separate
implementation activation is granted, its two-file implementation is reviewed,
and all focused and offline gates are clean, the transcript-only receipt is not
an activation input and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 build-reconciliation digest-rebind amendment v5

The installed 37-path manifest and accepted v4 receipt-binding amendment are
current for the predecessor v5 contract digest
`db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6`.
The predecessor planning-document SHA-256 is
`6991beb7bdc50005216236b78daa348d5921b86f3e31a9228d072ed6310678e3`,
and its accepted static-preflight SHA-256 is
`ad32aa287651e721c08d1cf900f5809fdc708b3c232c3a5b9ca5e54d5b86d065`.
Codex E independently accepted the build-reconciliation semantics at v5
contract SHA-256
`8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7`.
The owner authorized this narrow docs-only amendment-writing pass. That
authorization does not implement the rebind or authorize source reads,
characterization, activation, candidate work, package operations, installation,
canary work, stage advancement, or live use.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v5`
for exactly this stable-path digest transition:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v4
predecessor_amendment_sha256=6991beb7bdc50005216236b78daa348d5921b86f3e31a9228d072ed6310678e3
predecessor_manifest_binding_status=implemented_current
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
v5_contract_sha256_before=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
v5_contract_sha256_after=8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7
v5_contract_digest_change=exact_predecessor_to_reviewed_successor
build_recipe_v1_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
build_recipe_v1_status=immutable_retired_future_execution_blocked
build_recipe_v2_defined=false
accepted_review_evidence_schema=mythic_edge_role_pool_v5_build_reconciliation_contract_review.v1
accepted_review_evidence_key_count=38
accepted_review_evidence_sha256=c2aeac32cf5e6b93f4d6cd0dbda547dc57ef959190d402ae572de2e12c399565
predecessor_static_preflight_sha256=ad32aa287651e721c08d1cf900f5809fdc708b3c232c3a5b9ca5e54d5b86d065
successor_static_preflight_status=pending_reviewed_amendment_digest_and_implementation
characterization_status=blocked_pending_rebind_completion_and_separate_owner_authorization
manifest_rebind_status=contract_review_pending
```

This transition changes only the one existing v5 digest pin and the exact
dependent evidence values required to validate that pin. It changes no path,
path count, v3/v4 contract binding, historical v1-through-v4 amendment, recipe
object, candidate edit envelope, operation matrix, finite oracle, source-read
boundary, authority field, package behavior, or Stage-4 conclusion. Dynamic
digest adoption, predecessor skipping, target substitution, a second v5 row,
or modification of another manifest row is contradictory and fails closed.

The complete accepted Codex E evidence is this exact canonical 38-key JSON
object followed by one LF. The Markdown fences are not evidence bytes:

```json
{"build_environment_root_cause":"unknown","canary_authorized":false,"characterization_status":"defined_read_only_but_unauthorized","consumed_activation_reusable":false,"edit_envelope_status":"exact_two_paths_preserved","edits_performed":false,"finding_ids":[],"generated_residue_count":0,"implementation_authorized":false,"installation_authorized":false,"live_ready":false,"manifest_file_count":37,"manifest_rebind_authorized":false,"manifest_status":"stale_digest_37_to_37_rebind_required","next_recommended_role":"owner_manifest_rebind_decision_then_codex_b_exact_37_to_37_amendment","offline_gate_error_count":54,"offline_gate_failure_count":1,"offline_gate_root_cause":"stale_digest_only","offline_gate_test_count":338,"package_build_authorized":false,"package_creation_authorized":false,"protected_surface_forbidden_count":0,"protected_surface_warning_count":0,"receipt_storage":"transcript_only","recipe_v1_status":"immutable_retired_future_execution_blocked","review_evidence_schema":"mythic_edge_role_pool_v5_build_reconciliation_contract_review.v1","reviewer_role":"codex_e_independent_reviewer","secret_private_marker_lexical_false_positive_count":1,"secret_private_marker_sensitive_material_exposed":false,"service_mutation_authorized":false,"source_artifact":"references/external-isolation-broker-v5-corrective-successor.md","source_read_authorized":false,"source_sha256":"8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7","source_stable_during_review":true,"stage_advancement_authorized":false,"structural_validation_passed":true,"unfrozen_attempt_reusable":false,"verdict":"accepted_semantics_manifest_pending"}
```

Parse the evidence with strict UTF-8 JSON rules: no BOM, duplicate or unknown
keys, insignificant whitespace, alternate types, or missing final LF. Require
exactly 38 keys and the exact values above. Canonicalization is sorted-key,
compact, ASCII JSON plus one LF and must recompute SHA-256
`c2aeac32cf5e6b93f4d6cd0dbda547dc57ef959190d402ae572de2e12c399565`.
The reviewed contract digest must also be recomputed from the owning ordinary,
non-reparse file. A copied digest or shape-valid evidence object is insufficient.

Only these two files may be changed by a separately activated implementation:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`862d6a5b90ddfca2ba5652e1ee900b8e548f4905f55ab9742937fcb46b46d9cd`
and
`22892315f46d15cbdb2a8c198a12f42526bc0becc2412df4a6468cdc8b19f3ff`.
The contract and this planning document are read-only implementation inputs.
Drift in either script, either document, the 37-path state, or any predecessor
amendment stops before editing. This amendment does not authorize Codex C.

The focused validation matrix must:

- accept exactly the predecessor-to-target v5 digest transition while preserving
  the exact 37-path set and every other row;
- reject the predecessor after implementation, wrong target, missing or renamed
  v5 path, case variation, duplicate v5 row, extra path, count drift, changed
  existing path, non-ordinary file, and reparse point;
- refuse a reparse path before following, resolving, opening, reading, hashing,
  replacing, or adopting its target;
- parse and recompute the exact 38-key review evidence and reject every omitted,
  extra, renamed, duplicate, reordered, differently typed, stale, contradictory,
  cross-contract, alternate-preimage, or one-field-mutated value;
- reject drift in the predecessor amendment, predecessor static preflight,
  recipe-v1 digest or retired status, two-path envelope, finite oracle, or
  false-authority projection;
- derive a successor static-preflight digest by changing only the reviewed
  contract digest and accepted amendment digest in the otherwise contracted
  current object, without making recipe v1 executable or defining recipe v2;
- preserve all historical amendment, structural, protected-surface, private-
  marker, zero-effect, offline, legacy-regression, and `NOT LIVE-READY` checks;
  and
- prove every failure leaves the current manifest unchanged and creates no
  characterization, activation, candidate, package, or generated residue.

Codex B's docs-only validation ran 338 offline tests and structural validation.
Structural validation passed; the suite failed closed with 54 errors and one
failure. The primary cause was the expected stale v5 successor digest, projected
through the existing v3/v4 binding-drift wrappers and predecessor assertion.
No additional root cause was observed. This is expected preimplementation
evidence, not an offline-gate pass or implementation authority.

The v5 amendment lifecycle reuses the existing closed vocabulary:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E accepts this exact amendment digest, the canonical 38-key review evidence, exact predecessor and target, stable 37-path effect, two-file scope, tests, false-authority fields, and non-claims. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a fresh, exact, unexpired, single-use implementation activation binding the accepted amendment digest, both script digests, predecessor and target contract digests, review-evidence digest, static-preflight predecessor, test matrix, and false-authority fields. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated scripts and records their exact before/after hashes, successor static-preflight derivation, focused tests, full offline evidence, and zero residue. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, positive and negative matrix, unchanged 37-path set, exact target binding, successor static preflight, clean gates, and false-authority projection. | `complete` |
| any nonterminal status | Any authority, binding, implementation, test, review, gate, rollback, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then one failure row, then one positive
row. No status skip is valid. `complete` means only that Stage-3 tooling binds
the exact reviewed build-reconciliation contract. It does not authorize the
three-row characterization, recipe v2, activation construction, candidate work,
package operations, installation, canary execution, stage advancement, or live
use.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_through_v4_bindings_preserved=true
v5_manifest_rebind_v5_contract_writing_authorized=true
v5_manifest_rebind_v5_lifecycle_status=contract_review_pending
v5_manifest_rebind_v5_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_predecessor_v5_sha256=db32db8dc5da170579aec0e4eed4f0d7b25220f7a4fdc0cdb051dc3cc49c4bb6
manifest_target_v5_sha256=8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7
accepted_review_evidence_sha256=c2aeac32cf5e6b93f4d6cd0dbda547dc57ef959190d402ae572de2e12c399565
build_recipe_v1_future_execution_authorized=false
build_recipe_v2_defined=false
characterization_authorized=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
source_read_authorized=false
activation_creation_authorized=false
activation_consumption_authorized=false
candidate_preparation_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until independent Codex E review accepts this exact amendment, a separate
implementation activation is granted, the two-file implementation is reviewed,
and focused plus full offline gates pass, the manifest remains bound to
`db32...`, characterization remains unauthorized, and the Role Pool remains
`NOT LIVE-READY`.

### External-isolation broker v5 characterization-envelope digest-rebind amendment v6

The installed manifest contains exactly 37 paths and currently binds
`references/external-isolation-broker-v5-corrective-successor.md` to SHA-256
`8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7`.
The implemented predecessor planning-document SHA-256 is
`e2742a64463940bd47e29cfc160c6792dc10822e9df3a8e1e04565bf5758ba6d`,
its accepted static-preflight SHA-256 is
`b0c44a82bccc95333b9340834c0b9dbbbf7fd5dace9788958dda3f9216f8e984`,
and the resulting 37-file manifest SHA-256 is
`6e6a2d08c3fe3dbcb00c03a9918851dd4478e3daf3f8ba8d17859d60fa1a072c`.
Codex E independently confirmed `EIB-PKG-V5-CHAR-E-001`,
`EIB-PKG-V5-CHAR-E-002`, and `EIB-PKG-V5-CHAR-E-003` fixed at contract
SHA-256
`48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be`
and stated that a manifest rebind may be considered next. The owner then
authorized only this narrow docs-only amendment-writing pass. Neither statement
implements the rebind or authorizes characterization, source access, package
work, Codex C, installation, canary execution, stage advancement, or live use.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v6`
for exactly this stable-path transition:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v5
predecessor_amendment_sha256=e2742a64463940bd47e29cfc160c6792dc10822e9df3a8e1e04565bf5758ba6d
predecessor_manifest_binding_status=implemented_current
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
v5_contract_sha256_before=8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7
v5_contract_sha256_after=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
v5_contract_digest_change=exact_predecessor_to_reviewed_successor
accepted_review_evidence_schema=mythic_edge_role_pool_v5_characterization_execution_envelope_contract_review.v1
accepted_review_evidence_root_key_count=22
accepted_review_evidence_finding_key_count=3
accepted_review_evidence_validation_key_count=3
accepted_review_evidence_sha256=5f6a6dcc5e0ad1150aeb302e049ef0ec50900aa31dd93ef1ea5c03195057db53
accepted_review_evidence_storage=transcript_only_no_separate_receipt_asserted
characterization_parser_profile=mythic_edge_role_pool_v5_powershell_ast_characterizer.v2
characterization_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_result.v2
characterization_retry_activation_schema=mythic_edge_role_pool_v5_build_dependency_characterization_activation.v4
characterization_synthetic_matrix_schema=mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1
characterization_synthetic_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
characterization_synthetic_case_count=36
characterization_retry_activation_key_count=54
characterization_synthetic_review_receipt_schema=mythic_edge_role_pool_v5_characterization_synthetic_review_receipt.v1
characterization_synthetic_review_receipt_key_count=16
predecessor_static_preflight_sha256=b0c44a82bccc95333b9340834c0b9dbbbf7fd5dace9788958dda3f9216f8e984
successor_static_preflight_status=pending_reviewed_amendment_digest_and_implementation
characterization_status=blocked_pending_rebind_completion_and_separate_owner_authorization
manifest_rebind_status=contract_review_pending
```

This transition changes only the digest pinned to the one existing v5 path and
the dependent evidence values needed to validate that digest. It changes no
path, count, v3/v4 binding, historical v1-through-v5 amendment, build recipe,
candidate edit envelope, atomic oracle, source-read boundary, characterization
authority, package behavior, or Stage-4 conclusion. Dynamic digest adoption,
predecessor skipping, target substitution, a second v5 row, or modification of
any other manifest row is contradictory and fails closed.

The complete accepted Codex E evidence is the following exact canonical JSON
object followed by one LF. The Markdown fences are not evidence bytes. No
review reference or review timestamp was supplied, so neither is invented or
admitted as an optional field:

```json
{"canary_authorized":false,"characterization_authorized":false,"contract_artifact":"references/external-isolation-broker-v5-corrective-successor.md","contract_sha256":"48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be","contract_status":"characterization_execution_envelope_review_and_manifest_rebind_blocked","finding_status":{"EIB-PKG-V5-CHAR-E-001":"fixed_confirmed","EIB-PKG-V5-CHAR-E-002":"fixed_confirmed","EIB-PKG-V5-CHAR-E-003":"fixed_confirmed"},"implementation_authorized":false,"installation_authorized":false,"live_ready":false,"manifest_rebind_authorized":false,"manifest_rebind_may_be_considered_next":true,"next_recommended_role":"Codex B: narrow 37-to-37 manifest-rebind amendment writer","package_operations_authorized":false,"retry_activation_key_count":54,"role_performed":"Codex E: Independent V5 Characterization Contract Re-reviewer","service_mutation_authorized":false,"source_read_authorized":false,"stage_advancement_authorized":false,"synthetic_case_count":36,"synthetic_matrix_sha256":"9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526","synthetic_review_receipt_key_count":16,"validation":{"generated_residue_count":0,"offline_gate":"342 tests; expected 52 errors and 1 failure from stale manifest digest only","structural_validation":"passed"}}
```

Parse this evidence with strict UTF-8 JSON rules: no BOM, duplicate or unknown
keys, insignificant whitespace in canonical evidence, alternate types, or
missing final LF. Require exactly 22 root keys, exactly three `finding_status`
keys, exactly three `validation` keys, and the exact values above. Canonical
serialization is recursively sorted-key, compact, ASCII JSON plus one LF and
must recompute SHA-256
`5f6a6dcc5e0ad1150aeb302e049ef0ec50900aa31dd93ef1ea5c03195057db53`.
The reviewed contract digest, synthetic-matrix digest, and every predecessor
binding must also be recomputed from its owning ordinary, non-reparse artifact.
A copied digest, shape-valid object, alternate preimage, or transcript summary
without the complete object is insufficient.

Only these two files may be changed by a later, separately reviewed and
owner-activated implementation:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`6101f1a1d7a24c0b2dc6faa0e378e93aaff845729e56368baff03815e91188bc`
and
`4de1f059934b193d80362aff51029aa342097400b9d0aa2bcd04c85b6fff8c74`.
The v5 contract and this planning document are read-only implementation inputs.
Drift in either script, either document, the 37-path state, or any predecessor
amendment stops before editing. This amendment does not authorize Codex C.

The focused validation matrix must:

- accept only the exact `8b8d...` to `48d...` transition while preserving all
  37 paths and every non-v5 row byte-for-byte;
- reject the predecessor after implementation, wrong target, missing or renamed
  v5 path, case variation, duplicate v5 row, extra path, count drift, changed
  existing path, non-ordinary file, and reparse point;
- refuse a reparse path before following, resolving, opening, reading, hashing,
  replacing, or adopting its target;
- parse and recompute the exact accepted review object and reject any omitted,
  extra, renamed, duplicate, reordered, differently typed, stale,
  contradictory, cross-contract, alternate-preimage, or one-field-mutated
  value;
- require the exact parser-v2, result-v2, activation-v4, matrix-v1, review-v1,
  36-case, 54-key, and 16-key bindings and reject drift in any one of them;
- recompute the matrix digest from its owning contract bytes and reject a
  correctly shaped but incorrect digest or count;
- reject drift in amendments v1 through v5, the predecessor planning digest,
  predecessor static preflight, 37-file manifest digest, script digests, build
  recipe, two-path candidate envelope, atomic oracle, or false-authority fields;
- derive the successor static-preflight digest by changing only the reviewed
  contract digest and accepted amendment digest in the otherwise contracted
  current object;
- preserve every structural, protected-surface, private-marker, zero-effect,
  offline, legacy-regression, and `NOT LIVE-READY` check; and
- prove every failure leaves the installed manifest unchanged and creates no
  characterization, activation, source-read, candidate, package, or generated
  residue.

Codex B's docs-only validation ran all 342 offline tests after Skill Creator
structural validation passed. The suite failed closed with 52 errors and one
failure. Every observed error and the failure derived from the exact stale v5
successor digest, including the existing v5 binding-drift wrappers and legacy
predecessor assertion. No second root cause was observed. This is expected
preimplementation evidence, not an offline-gate pass or implementation
authority.

The amendment lifecycle uses this closed vocabulary:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E accepts this exact amendment digest, canonical 22-key review evidence, predecessor and target, stable 37-path effect, characterization profile bindings, two-file scope, tests, false-authority fields, and non-claims. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a fresh, exact, unexpired, single-use implementation activation binding the accepted amendment digest, both script digests, predecessor and target contract digests, review-evidence digest, predecessor static preflight, matrix digest and counts, schema versions, complete test matrix, and false-authority fields. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated scripts and records exact before/after hashes, successor static-preflight derivation, focused tests, full offline evidence, and zero residue. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, positive and negative matrix, unchanged 37-path set, target binding, successor static preflight, clean gates, and false-authority projection. | `complete` |
| any nonterminal status | Any authority, binding, implementation, test, review, gate, rollback, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then exactly one failure row, then exactly
one positive row. No status skip is valid. `complete` means only that Stage-3
tooling binds the exact reviewed characterization-envelope contract. It does
not authorize characterization, source access, activation construction, package
work, installation, canary execution, stage advancement, or live use.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_through_v5_bindings_preserved=true
v5_manifest_rebind_v6_contract_writing_authorized=true
v5_manifest_rebind_v6_lifecycle_status=contract_review_pending
v5_manifest_rebind_v6_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_predecessor_v5_sha256=8b8d5f1631f8d546ee7c477a7bf626f6d73f4f460827a92550e7712f3cfe35b7
manifest_target_v5_sha256=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
accepted_review_evidence_sha256=5f6a6dcc5e0ad1150aeb302e049ef0ec50900aa31dd93ef1ea5c03195057db53
characterization_synthetic_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
characterization_synthetic_case_count=36
characterization_retry_activation_key_count=54
characterization_synthetic_review_receipt_key_count=16
characterization_authorized=false
source_read_authorized=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
implementation_authorized=false
activation_creation_authorized=false
activation_consumption_authorized=false
candidate_preparation_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until independent Codex E review accepts this exact amendment, the owner
separately grants an exact implementation activation, its two-file
implementation is completed and reviewed, and focused plus full offline gates
pass, the manifest remains bound to `8b8d...`, characterization and source
reads remain unauthorized, and the Role Pool remains `NOT LIVE-READY`.

### External-isolation broker v5 real-source-adapter digest-rebind amendment v7

The implemented v6 manifest contains exactly 37 paths and binds
`references/external-isolation-broker-v5-corrective-successor.md` to SHA-256
`48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be`.
The implemented predecessor planning-document SHA-256 is
`9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d`,
its accepted static-preflight SHA-256 is
`95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af`,
and its 37-file manifest SHA-256 is
`5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc`.

Codex E independently confirmed `EIB-PKG-V5-ADAPTER-E-001` fixed at contract
SHA-256
`81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4`.
It confirmed the 37-case adapter matrix and complete 15,360-tuple outer oracle,
classified the semantics as accepted with a manifest rebind required, and made
the rebind eligible but not authorized. The owner then authorized only this
narrow docs-only amendment-writing pass. Neither fact implements the rebind or
authorizes validator changes, source access, activation construction,
characterization, package work, Codex C, installation, canary execution, stage
advancement, or live use.

Use amendment ID
`mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v7`
for exactly this stable-path transition:

```text
predecessor_amendment_id=mythic_edge_role_pool_stage3_manifest_rebind_external_broker_v5_amendment.v6
predecessor_amendment_sha256=9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d
predecessor_manifest_binding_status=implemented_current
transition_kind=37_to_37_digest_rebind
path=mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md
manifest_file_count_before=37
manifest_file_count_after=37
path_set_change=none
v5_contract_sha256_before=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
v5_contract_sha256_after=81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4
v5_contract_digest_change=exact_predecessor_to_reviewed_successor
v5_contract_status=outer_launcher_contract_review_and_manifest_rebind_blocked
accepted_review_evidence_schema=mythic_edge_role_pool_v5_real_source_adapter_contract_review.v1
accepted_review_evidence_root_key_count=17
accepted_review_evidence_finding_key_count=1
accepted_review_evidence_sha256=bdef51e12ae9de10670c09076349e84ff23e5b543f67838b320bbb892a1e2be4
accepted_review_evidence_storage=transcript_only_no_separate_receipt_asserted
characterization_activation_schema=mythic_edge_role_pool_v5_build_dependency_characterization_activation.v5
characterization_activation_key_count=64
characterization_controller_profile=mythic_edge_role_pool_v5_characterization_controller.v1
characterization_controller_request_schema=mythic_edge_role_pool_v5_characterization_controller_request.v1
characterization_controller_request_key_count=10
characterization_parser_profile=mythic_edge_role_pool_v5_powershell_ast_characterizer.v3
characterization_child_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_child_result.v1
characterization_child_result_key_count=13
characterization_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_result.v3
characterization_result_key_count=20
characterization_attempt_handoff_schema=mythic_edge_role_pool_v5_build_dependency_characterization_attempt_handoff.v1
characterization_attempt_handoff_key_count=27
characterization_program_bundle_schema=mythic_edge_role_pool_v5_characterization_program_bundle.v2
characterization_program_bundle_key_count=18
characterization_core_matrix_schema=mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1
characterization_core_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
characterization_core_case_count=36
characterization_adapter_matrix_schema=mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2
characterization_adapter_matrix_sha256=2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7
characterization_adapter_case_count=37
characterization_outer_oracle_tuple_count=15360
characterization_outer_oracle_accepted_count=3
characterization_outer_oracle_blocked_before_start_count=2
characterization_outer_oracle_blocked_after_start_count=157
characterization_outer_oracle_cleanup_unknown_count=15198
characterization_bundle_review_schema=mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3
characterization_bundle_review_key_count=29
predecessor_static_preflight_sha256=95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af
successor_static_preflight_status=pending_reviewed_amendment_digest_and_implementation
manifest_rebind_status=contract_review_pending
```

This transition changes only the digest pinned to the one existing v5 path and
the dependent evidence values needed to validate that digest. It changes no
path, count, v3/v4 binding, historical v1-through-v6 amendment, build recipe,
candidate edit envelope, atomic oracle, source-read boundary, characterization
authority, package behavior, or Stage-4 conclusion. Dynamic digest adoption,
predecessor skipping, target substitution, a second v5 row, or modification of
any other manifest row is contradictory and fails closed.

The complete accepted Codex E evidence is the following exact canonical JSON
object followed by one LF. The Markdown fences are not evidence bytes. No
review reference or review timestamp was supplied, so neither is invented or
admitted as an optional field:

```json
{"activation_creation_authorized":false,"adapter_matrix":"37 unique cases; digest matched","contract_sha256":"81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4","contract_verdict":"accepted_semantics_manifest_rebind_required","exhaustive_outer_oracle":"15360 tuples; all counts matched","finding_status":{"EIB-PKG-V5-ADAPTER-E-001":"fixed_confirmed"},"generated_residue_count":0,"implementation_authorized":false,"live_ready":false,"manifest_rebind_authorized":false,"manifest_rebind_eligible":true,"next_recommended_role":"Codex B: narrow 37-to-37 manifest-rebind amendment writer, after exact owner approval","offline_gate":"346 tests; 52 errors and 1 failure from stale v5 digest only","package_operations_authorized":false,"role_performed":"Codex E: Independent V5 Real-Source Adapter Contract Re-reviewer","source_access_authorized":false,"stage_advancement_authorized":false}
```

Parse this evidence with strict UTF-8 JSON rules: no BOM, duplicate or unknown
keys, insignificant whitespace in canonical evidence, alternate types, or
missing final LF. Require exactly 17 root keys, exactly one `finding_status`
key, and the exact values above. Canonical serialization is recursively sorted-
key, compact, ASCII JSON plus one LF and must recompute SHA-256
`bdef51e12ae9de10670c09076349e84ff23e5b543f67838b320bbb892a1e2be4`.
The reviewed contract, core matrix, adapter matrix, predecessor planning
document, predecessor static preflight, and predecessor manifest digests must
also be recomputed from their owning ordinary, non-reparse artifacts or
canonical preimages. A copied digest, shape-valid object, alternate preimage,
or transcript summary without the complete object is insufficient.

Only these two files may be changed by a later, separately reviewed and owner-
activated implementation:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

Their exact preimplementation SHA-256 values are respectively
`1333f9e1fd176fa4a8e19ea3f09b9632134d5bfbbd63cb77aa2ea664372912f9`
and
`fc9224f36028f95b62836e4a3d5a125b5c0dfefee558b33ba77f4089d0675cf4`.
The v5 contract and this planning document are read-only implementation inputs.
Drift in either script, either document, the 37-path state, or any predecessor
amendment stops before editing. This amendment does not authorize Codex C.

The focused validation matrix must:

- accept only the exact `48d7...` to `81aa...` transition while preserving all
  37 paths and every non-v5 row byte-for-byte;
- reject the predecessor after implementation, wrong target, missing or renamed
  v5 path, case variation, duplicate v5 row, extra path, count drift, changed
  existing path, non-ordinary file, and reparse point;
- refuse a reparse path before following, resolving, opening, reading, hashing,
  replacing, or adopting its target;
- parse and recompute the exact accepted review object and reject any omitted,
  extra, renamed, duplicate, reordered, differently typed, stale,
  contradictory, cross-contract, alternate-preimage, or one-field-mutated
  value;
- require the exact activation, controller-request, child-result, public-result,
  attempt-handoff, program-bundle, matrix, and bundle-review schema versions and
  field counts listed above;
- recompute both matrix digests from their canonical contract preimages, require
  36 plus 37 cases, and enumerate all 15,360 outer-oracle tuples exactly once;
- require outer-oracle outcome counts `3`, `2`, `157`, and `15198` and reject an
  unclassified, duplicate, multiply classified, reordered-dimension, or count-
  mismatched tuple;
- reject drift in amendments v1 through v6, the predecessor planning digest,
  predecessor static preflight, predecessor 37-file manifest digest, script
  digests, build recipe, two-path candidate envelope, atomic oracle, or false-
  authority fields;
- derive the successor static-preflight digest by changing only the reviewed
  contract digest and accepted amendment digest in the otherwise contracted
  current object;
- preserve every structural, protected-surface, private-marker, zero-effect,
  offline, legacy-regression, and `NOT LIVE-READY` check; and
- prove every failure leaves the installed manifest unchanged and creates no
  characterization, activation, source-read, candidate, package, or generated
  residue.

Codex B's docs-only validation must run the Skill Creator structural validator
and the complete offline release gate. Before implementation, the expected
fail-closed shape is 346 tests, 52 errors, and one failure, all derived from
`v5 successor digest does not match the pinned digest`. Any second unique root
cause blocks. This expected shape is not an offline-gate pass or implementation
authority.

The amendment lifecycle uses this closed vocabulary:

```text
contract_review_pending
owner_activation_required
implementation_in_progress
implementation_review_pending
complete
revision_required
superseded
```

| Current status | Exact required evidence | Next status |
| --- | --- | --- |
| `contract_review_pending` | Codex E accepts this exact amendment digest, canonical 17-key review evidence, predecessor and target, stable 37-path effect, adapter and outer-oracle bindings, two-file scope, tests, false-authority fields, and non-claims. | `owner_activation_required` |
| `owner_activation_required` | The owner supplies a fresh, exact, unexpired, single-use implementation activation binding the accepted amendment digest, both script digests, predecessor and target contract digests, review-evidence digest, predecessor static preflight, both matrices, oracle counts, complete test matrix, and false-authority fields. | `implementation_in_progress` |
| `implementation_in_progress` | Codex C changes only the two activated scripts and records exact before/after hashes, successor static-preflight derivation, focused tests, full offline evidence, and zero residue. | `implementation_review_pending` |
| `implementation_review_pending` | Codex E accepts the exact implementation bytes, positive and negative matrix, unchanged 37-path set, target binding, successor static preflight, clean gates, and false-authority projection. | `complete` |
| any nonterminal status | Any authority, binding, implementation, test, review, gate, rollback, or residue condition is missing, stale, contradictory, broadened, or failed. | `revision_required` |
| any nonterminal status | The owner names an exact replacement and Codex E accepts it. | `superseded` |

Evaluate accepted supersession first, then exactly one failure row, then exactly
one positive row. No status skip is valid. `complete` means only that Stage-3
tooling binds the exact reviewed real-source-adapter contract. It does not
authorize characterization, source access, activation construction, package
work, installation, canary execution, stage advancement, or live use.

At completion of this Codex B thread:

```text
v5_manifest_rebind_v1_through_v6_bindings_preserved=true
v5_manifest_rebind_v7_contract_writing_authorized=true
v5_manifest_rebind_v7_lifecycle_status=contract_review_pending
v5_manifest_rebind_v7_implementation_authorized=false
manifest_file_count=37
manifest_path_set_unchanged=true
manifest_predecessor_v5_sha256=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
manifest_target_v5_sha256=81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4
accepted_review_evidence_sha256=bdef51e12ae9de10670c09076349e84ff23e5b543f67838b320bbb892a1e2be4
characterization_adapter_matrix_sha256=2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7
characterization_adapter_case_count=37
characterization_outer_oracle_tuple_count=15360
characterization_authorized=false
source_read_authorized=false
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
implementation_authorized=false
activation_creation_authorized=false
activation_consumption_authorized=false
candidate_preparation_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_write_authorized=false
live_ready=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

Until independent Codex E review accepts this exact amendment, the owner
separately grants an exact implementation activation, its two-file
implementation is completed and reviewed, and focused plus full offline gates
pass, the manifest remains bound to `48d7...`, characterization and source
reads remain unauthorized, and the Role Pool remains `NOT LIVE-READY`.


## Fixed Synthetic Scenario

The positive scenario contains exactly three repository-shaped synthetic
identities and exactly one lane in each:

- `synthetic/mythic-edge-analytics`;
- `synthetic/mythic-edge-corpus`; and
- `synthetic/mythic-edge-fable-engine`.

All three lanes use the shared role `Codex B`. The identities grant no access
to repositories with similar real names. The contract performs no repository,
Git, GitHub, connector, browser, or API request.

The lanes model the same repository-relative contract path in three distinct
synthetic repositories. The compatibility derivation must correctly treat
those paths as repository-local while still treating global contracts,
protected surfaces, external state, dependencies, and invalidation risks as
cross-lane risks. Exactly three pair rows are required, and every risk set in
the positive case must be empty before the overall verdict can be
`safe_to_run_concurrently`.

The single `planning_projection` is a synthetic parallel-compatibility
assessment only. It is not a v3 plan, selects no lane for dispatch, records zero
claims, leases, reservations, and launches, emits no v3 plan document, and sets
`live_transition_authorized: false`.

## Fail-Closed Exclusion Probes

Every observation runs these seven exact synthetic negative probes through the
checker-owned classifier:

1. missing compatibility evidence;
2. an unlisted repository;
3. a dependency cycle;
4. an overlapping write path;
5. a shared global contract surface;
6. a protected surface; and
7. a required external effect.

Every probe must derive `excluded_fail_closed` plus its exact stable fallback
condition and reason code. A claimed result that does not follow from the probe
input fails validation.

## Zero-Effect Boundary

The strict `effect_counters` object rejects missing or additional counters and
requires zero for all repository reads, Git/GitHub/connector/browser/API
requests, claims, leases, reservations, role-task creation, pooled or nested
agent launches, v3 plan documents, role-artifact/repository/persistent/GitHub/
issue writes, commits, pushes, PR writes, integration actions, credential
access, external mutation, deployment, production effects, stage advancement,
and finding resolution. Running the trusted local validator is not a pooled
agent launch and is outside these Role Pool operation counters.

The observation also requires:

- `finding_resolution_claimed: false`;
- `stage_advancement_claimed: false`;
- `live_ready_claimed: false`;
- `no_mutation: true`;
- `MRP-RC-003` still `unresolved`; and
- agent behavior explicitly not tested and reserved for Stage 4.

For digest calculation, canonical JSON is UTF-8, sorted-key, compact,
ASCII-escaped JSON. The root `digest` is SHA-256 of that canonical object with
only its own root `digest` field omitted. The checker may read an equivalent
whitespace-formatted JSON document, but duplicate keys, non-finite numbers,
missing fields, unknown fields, or a noncanonical self-digest fail closed.

The counters are self-digested assertions, not independent runtime evidence.
The `evidence_boundary` states that checker exit `0` proves deterministic
structure and derived classifier results only. Observation acceptance also
requires the offline release-gate result, exact validator command transcript,
an independent operation audit, and before/after persistent-state comparison.

## Observation Pair And Independent Review

Produce two separate passing observations, `1_of_2` and `2_of_2`, with one
fresh shared Stage-3 attempt-series ID, sequence indexes `1` and `2`, distinct
observation IDs and digests, and increasing timestamps. Each observation must
bind the same accepted Stage-2 entry, current contract snapshot, scenario,
compatibility derivation, exclusion probes, and zero-effect boundary. Check
pair readiness with:

```powershell
py -B scripts\check_stage3_behavioral_planning.py <attempt-1.json> --pair-with <attempt-2.json>
```

Pair-checker success means only that the two observations are ready to be sent
to an independent reviewer.

Both observations retain `independent_review.status: pending`. A later
independent review must replay both exact canonical documents, confirm distinct
identities and complementary attempts, compare every binding and counter, and
record pair acceptance separately from any stage-advancement decision.
Stage-3 pair acceptance does not resolve `MRP-RC-003`, establish live readiness,
or authorize Stage 4.

Stage 4 uses only
`mythic_edge_role_pool_stage4_canary_exception.v1` for the fresh isolated
malicious-content experiment. Neither Stage 3 nor Stage 4 needs a real issue to
be advanced. A real low-risk B or E issue is first required for the later
single-lane real-dispatch stage, under a fresh current-user authorization.
