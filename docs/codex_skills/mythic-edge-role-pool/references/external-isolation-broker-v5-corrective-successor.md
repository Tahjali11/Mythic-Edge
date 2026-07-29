# External-Isolation Broker v5 Corrective Successor Contract

Status: `outer_launcher_contract_review_and_manifest_rebind_blocked`

Contract ID:
`mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1`

## Decision and scope

The reviewed v4 contract and frozen v4 package remain immutable historical
lineage. Independent package review did not accept the v4 package because:

```text
EIB-PKG-V4-IMPL-E-001=frozen_candidate_digests_not_bound_to_validated_inventory
```

The v4 inventory and handoff repeat matching digest values. That equality is
necessary but insufficient: the v4 interface permits those values to arrive as
ordinary caller data rather than proving that they were projected from the
validated final inventory of the same attempt.

This contract defines a separate v5 package candidate. V5 corrects only that
provenance defect by introducing an internal ephemeral validated-final-inventory
binding, changing publication order, and closing every inventory-state-to-digest
projection. It preserves the accepted v4 corrections for timestamp floors,
failure/lifecycle combinations, and symbolic owner-activation references.

The parent v4 contract remains controlling except where this contract gives a
stricter v5 rule. Any conflict, omission, extra edit path, schema relaxation, or
need to weaken a parent rule stops before v5 root creation and routes to Codex B.

## Authority and non-claims

This artifact is contract-only. It authorizes no package read, source copy,
edit, build, test, inventory, handoff, publication, installation, service
mutation, canary, source-repository access, stage advancement, or live use.
It does not authorize Codex C or D. The v4 package remains uninstalled,
non-reusable, unchanged, and not accepted.

The finding is a contract input, not a claim that a correction exists or works.
This contract makes no correctness, security, privacy, readiness, release,
deployment, production, or live-operation claim.

## Exact v4 lineage binding

The v5 predecessor binding is one indivisible set:

```text
parent_contract_id=mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1
parent_contract_path=references/external-isolation-broker-v4-corrective-successor.md
parent_contract_sha256=628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487
rejected_v4_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v4
rejected_v4_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4
rejected_v4_inventory_filename=package-inventory.json
rejected_v4_inventory_file_sha256=a805429be56e60fa9f29a7f3562d8a11b5a5966e9177f33f15f81e3f1c8bc298
rejected_v4_inventory_root_digest=bc2240e7ceea848404becc18914d41e78699ee0aee1316c0619bd7a12e423994
rejected_v4_inventory_file_count=51
rejected_v4_inventory_total_length_bytes=6136931
rejected_v4_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4.implementation-handoff.v4.json
rejected_v4_handoff_file_sha256=adbe95cf2b37c666dcbc72fe295e50464fb20140e63053b107e58772f7af10c5
rejected_v4_handoff_root_digest=e8941e8dd92d4bf9ff581b335f639420fd493c7ac724f50c142e843b7350dc51
rejected_v4_review_status=not_accepted_contract_mismatch
rejected_v4_package_bytes_unchanged=true
rejected_v4_generated_residue_remaining=false
rejected_v4_installed=false
rejected_v4_service_mutated=false
rejected_v4_canary_performed=false
rejected_v4_live_ready=false
rejected_v4_reuse_authorized=false
```

The v4 inventory and handoff metadata above were validated without reading
package source content. Any mismatch, missing file, changed length, changed
inventory row, unreadable metadata, reparse point, non-ordinary file, or path
identity ambiguity blocks v5. The v4 package, inventory, handoff, contract, and
review evidence must not be edited, deleted, renamed, repaired, installed,
executed, or used as a resumable workspace.

## v5 identity and versioning

The v5 identities are closed:

```text
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v5
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v5
package_parent_resolver=windows_current_owner_desktop_mtg_resources.v1
package_parent_suffix=MTG Resources
package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v5
inventory_schema=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v5
inventory_filename=package-inventory.json
inventory_staging_filename=package-inventory.json.tmp
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v5
implementation_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v5.implementation-handoff.v5.json
implementation_handoff_staging_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v5.implementation-handoff.v5.json.tmp
publication_failure_schema=mythic_edge_role_pool_package_publication_failure.v3
validated_inventory_binding_schema=mythic_edge_role_pool_validated_final_inventory_binding.v1
broker_protocol_id=mythic_edge_role_pool_windows_isolation_broker.v1
verifier_protocol_id=mythic_edge_role_pool_windows_isolation_verifier_service.v1
receipt_chain_schema=mythic_edge_role_pool_broker_receipt_chain.v1
reconciliation_receipt_schema=mythic_edge_role_pool_broker_reconciliation_receipt.v1
candidate_preparation_activation_schema=mythic_edge_role_pool_v5_candidate_preparation_activation.v2
final_seal_activation_schema=mythic_edge_role_pool_v5_final_seal_activation.v2
future_activation_requirements_schema=mythic_edge_role_pool_v5_future_activation_requirements.v2
review_preflight_packet_schema=mythic_edge_role_pool_v5_review_preflight_packet.v2
candidate_independent_review_receipt_schema=mythic_edge_role_pool_v5_candidate_independent_review_receipt.v2
build_dependency_characterization_controller_profile=mythic_edge_role_pool_v5_characterization_controller.v1
build_dependency_characterization_parser_profile=mythic_edge_role_pool_v5_powershell_ast_characterizer.v3
build_dependency_characterization_child_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_child_result.v1
build_dependency_characterization_activation_schema=mythic_edge_role_pool_v5_build_dependency_characterization_activation.v5
build_dependency_characterization_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_result.v3
build_dependency_characterization_program_bundle_schema=mythic_edge_role_pool_v5_characterization_program_bundle.v2
build_dependency_characterization_attempt_handoff_schema=mythic_edge_role_pool_v5_build_dependency_characterization_attempt_handoff.v1
build_dependency_characterization_controller_request_schema=mythic_edge_role_pool_v5_characterization_controller_request.v1
```

Package, authority-profile, inventory, handoff, and publication-failure schemas
advance because inventory publication order and digest provenance change. The
validated inventory binding is a new private in-process value and receives its
own v1 identity. Broker, verifier, receipt-chain, and reconciliation-receipt
wire schemas remain v1 because their fields and cryptographic roots do not
change. Retaining a v4 public package or handoff schema under the new semantics
is forbidden.

The candidate-preparation and final-seal activation schemas, future-activation
requirements, review-preflight packet, and candidate-review receipt advance to
v2 because this revision adds the closed atomic-consumption mechanism, its seven
authority fields, and a symbolic consumption-key binding. The build-dependency
characterization activation is a separate v5 task profile because v4 bound a
single-row synthetic program without a real-source adapter or parent-owned
complete-result entrypoint. Parser profile v3, child-result v1, public result
v3, and attempt-handoff v1 bind the corrected controller/child/outer-launcher
boundary. Program-bundle v2 and bundle-review receipt v3 advance because their
predecessors omitted that handoff and its outer synthetic matrix. No package or
publication schema advances for that read-only task. V1 through v4
characterization, unversioned, missing-field, extra-field, or mixed-version
packets and receipts cannot be upgraded in place and fail closed. The package,
inventory, handoff, broker, verifier,
receipt-chain, and reconciliation-receipt schemas do not advance merely because
activation consumption or read-only characterization is now defined.

## Corrective invariant

For every v5 public handoff or failure projection with
`inventory_status=frozen_candidate`, both inventory digest fields must be copied
by the serializer from one validated-final-inventory binding created for the
same attempt. They must never be supplied by a caller, parsed from a handoff,
recovered from logs, copied from v4, defaulted, or reconstructed from an
unvalidated file.

The exact invariant is:

```text
frozen_candidate
  => validated_binding_present
  and inventory_file_sha256 == validated_binding.inventory_file_sha256
  and inventory_root_digest == validated_binding.inventory_root_digest
  and binding_attempt == current_attempt
  and binding_contract == accepted_v5_contract
  and final_inventory_revalidated_immediately_before_serialization
```

Any failed term rejects before public bytes are constructed. Digest equality
alone does not establish this invariant.

## Private validated-final-inventory binding

`mythic_edge_role_pool_validated_final_inventory_binding.v1` is an immutable,
private, in-memory capability value. It is not an authority packet, lifecycle
claim, public schema, durable record, cache entry, or output field. It has no
public constructor or deserializer.

The private factory receives only the current attempt's already constructed
canonical inventory bytes, expected validated inventory object, accepted v5
contract binding, and an already opened no-follow handle to the final v5
inventory. While the per-attempt publication lock is held, it must verify:

1. the final path is the exact v5 inventory path under the exact v5 root;
2. every inherited fixed-volume, owner-SID, ordinary-file, no-reparse, and
   no-hardlink rule;
3. file identity from the opened final handle and absence of path substitution;
4. exact byte length and raw file SHA-256 against the in-memory candidate;
5. strict duplicate-key-rejecting canonical JSON parse;
6. exact v5 schema, package, contract, authority-profile, lineage, key set,
   self-digest, row count, total length, row ordering, and inventory root;
7. exact field-for-field equality with the current attempt's expected
   inventory object; and
8. one of the two closed staging observations below.

The binding's complete private field set is:

```text
binding_schema
attempt_identity
accepted_contract_id
accepted_contract_sha256
package_id
inventory_schema
inventory_relative_name
inventory_raw_length_bytes
inventory_file_sha256
inventory_root_digest
inventory_file_count
inventory_total_length_bytes
final_file_volume_identity
final_file_identity
staging_observation
```

The field types and derivations are closed:

- `binding_schema`, `accepted_contract_id`, `package_id`, `inventory_schema`,
  and `inventory_relative_name` are the exact literals in this contract;
- `attempt_identity` is reference identity to the private current-attempt
  context object, not a string, digest, UUID, caller value, or serialized ID;
- `accepted_contract_sha256`, `inventory_file_sha256`, and
  `inventory_root_digest` are lowercase 64-character hexadecimal strings
  derived by their owning validators;
- `inventory_raw_length_bytes`, `inventory_file_count`, and
  `inventory_total_length_bytes` are non-Boolean positive integers and the
  count is exactly 51;
- `final_file_volume_identity` and `final_file_identity` are opaque immutable
  values read directly from the open final-inventory Windows file handle and
  compared by the same private implementation; and
- `staging_observation` is one closed literal below.

`attempt_identity`, file identities, and the accepted contract digest are
private comparison values. They must not be emitted. The only allowed
`staging_observation` literals are:

```text
final_validated_staging_absent
final_validated_staging_cleanup_failed
```

The first means the final inventory validates and the inventory staging file is
absent. The second means the same final validation succeeded but cleanup of the
exact inventory staging file failed and that staging file remains. No other
state creates a binding.

The factory must reject caller-created mappings, dataclass lookalikes,
subclasses, copied or deserialized objects, unknown fields, stale process
values, v4 bindings, wrong attempts, wrong contract digests, wrong final file
identities, and unsupported staging observations. The implementation may use a
module-private immutable class plus a module-private construction token; it
must not expose a general constructor, mutable registry, global cache, file
cache, or validation-witness field.

The binding exists only inside one publication attempt while its lock is held.
It is discarded after candidate handoff or failure projection construction and
must not be logged, serialized, persisted, returned to callers, reused after a
restart, or accepted across attempts.

## Corrected publication sequence

The v4 sequence that constructs candidate handoff bytes before final inventory
validation is superseded for v5. The only candidate path is:

1. construct and strictly validate canonical v5 inventory bytes in memory;
2. exclusively create and fully write the exact inventory staging file;
3. flush and close the staging writer under inherited durability rules;
4. no-replace publish or reconcile the exact final inventory;
5. open the final inventory without following a reparse point and validate it
   against the same in-memory candidate;
6. open the final inventory for read while denying write and delete sharing,
   retain that owning handle through handoff publication and reconciliation,
   observe inventory staging absence or its exact cleanup failure, and create
   the corresponding ephemeral binding;
7. immediately before handoff or failure-projection serialization, reopen or
   retain an owning final handle and revalidate final file identity, raw length,
   raw SHA-256, canonical inventory, and root digest against the binding;
8. construct public bytes with inventory digests projected only from the
   binding;
9. exclusively stage, flush, no-replace publish, and reconcile the handoff; and
10. report candidate-ready only after both final files validate and both
    staging files are absent.

Steps 4 through 9 remain inside the same per-attempt publication lock. If the
final inventory changes, becomes unavailable, changes identity, ceases to be
ordinary, becomes a reparse point, or fails strict revalidation after binding
creation, serialization is forbidden. The attempt routes through an applicable
closed failure row without frozen digests when inventory identity is unknown.
Before handoff serialization this is exactly
`inventory_publication_state_unknown`, with `inventory_status=unknown` and both
digest fields `none`. It must not repair, overwrite, delete, or trust the
changed final. If the required deny-write/delete-sharing handle cannot be
obtained and retained, binding creation fails closed.

A blocked-before-inventory path remains allowed to construct its exact blocked
handoff without an inventory binding. No candidate-ready handoff may be
constructed before final inventory publication and validation.

## Closed binding and projection matrix

The serializer and failure projector accept the following combinations only:

| public operation/result | inventory status | required binding | required staging observation | public digest source |
| --- | --- | --- | --- | --- |
| candidate handoff with `candidate_ready_for_independent_review` | `frozen_candidate` | present, current, revalidated | `final_validated_staging_absent` | copy both from binding |
| post-inventory failure other than inventory-staging cleanup failure | `frozen_candidate` | present, current, revalidated | `final_validated_staging_absent` | copy both from binding |
| `inventory_staging_cleanup_failed` projection | `frozen_candidate` | present, current, revalidated | `final_validated_staging_cleanup_failed` | copy both from binding |
| blocked-before-inventory failure | `not_created` | absent | not applicable | both literal `none` |
| inventory publication state unknown | `unknown` | absent | not applicable | both literal `none` |

For the inherited sanitized error-code literals, the second row applies
exactly to
`handoff_staging_write_failed`, `handoff_publish_absent`,
`handoff_publish_collision`, `handoff_publication_state_unknown`,
`handoff_publication_retry_exhausted`, and
`handoff_staging_cleanup_failed` after a validated final inventory exists.
The third row applies only to `inventory_staging_cleanup_failed`.

Because v5 publishes and validates inventory before constructing handoff
bytes, it deliberately supersedes the v4 projection for
`handoff_staging_write_failed`. The complete v5 failure matrix is normative:

| operation path | sanitized error code | failure phase | external publication status | inventory status | successor terminal status | source-copy status |
| --- | --- | --- | --- | --- | --- | --- |
| `blocked_handoff_only` | `source_copy_failed` | `source_copy` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_staging_write_failed` | `handoff_staging` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_publish_absent` | `handoff_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_publish_collision` | `handoff_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_publication_state_unknown` | `handoff_publication` | `unknown_after_publish_attempt` | `not_created` | `blocked_handoff_state_unknown` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_publication_retry_exhausted` | `handoff_publication` | `unknown_after_publish_attempt` | `not_created` | `blocked_handoff_state_unknown` | `failed_incomplete` |
| `blocked_handoff_only` | `blocked_handoff_staging_cleanup_failed` | `handoff_staging_cleanup` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `failed_incomplete` |
| `candidate_inventory_then_handoff` | `inventory_staging_write_failed` | `inventory_staging` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `candidate_pre_inventory_staging_cleanup_failed` | `pre_inventory_staging_cleanup` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publish_absent` | `inventory_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publish_collision` | `inventory_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publication_state_unknown` | `inventory_publication` | `unknown_after_publish_attempt` | `unknown` | `publication_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publication_retry_exhausted` | `inventory_publication` | `unknown_after_publish_attempt` | `unknown` | `publication_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_staging_cleanup_failed` | `inventory_staging_cleanup` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_staging_write_failed` | `handoff_staging` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publish_absent` | `handoff_publication` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publish_collision` | `handoff_publication` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publication_state_unknown` | `handoff_publication` | `unknown_after_publish_attempt` | `frozen_candidate` | `frozen_candidate_handoff_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publication_retry_exhausted` | `handoff_publication` | `unknown_after_publish_attempt` | `frozen_candidate` | `frozen_candidate_handoff_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_staging_cleanup_failed` | `handoff_staging_cleanup` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_cleanup_failed` | `complete` |

The following are invalid without fallback:

- `frozen_candidate` with no binding, stale binding, wrong-attempt binding,
  wrong-contract binding, wrong-package binding, or failed revalidation;
- caller-supplied `inventory_file_sha256` or `inventory_root_digest` on any
  candidate handoff or failure-projection builder;
- `frozen_candidate` plus either literal `none` or any value not copied from
  the binding;
- `not_created` or `unknown` plus a binding or non-`none` digest;
- candidate-ready plus `final_validated_staging_cleanup_failed`;
- inventory-staging-cleanup failure plus
  `final_validated_staging_absent`;
- a binding created from staging bytes, a prepublication candidate, the v4
  inventory, an unvalidated final path, or a reparsed path;
- multiple candidate bindings, binding replacement, caller coercion, or digest
  comparison used as a substitute for provenance; and
- any lifecycle/error combination not present as one of the 20 accepted rows
  in the complete normative v5 failure matrix in this contract.

Public schema keys remain closed. The private binding itself and all private
identity fields are absent from public output.

No other v4 failure-row projection is normative for v5. V4 remains lineage and
supplies inherited rules only where this contract does not supersede them. The
five-row v5 binding/projection matrix and the 20-row v5 failure matrix above are
the sole v5 state authorities; disagreement with either matrix blocks rather
than falling back to a v4 row.

## Mechanical contract and candidate preflights

Preflight has two ordered phases and no circular dependency:

1. a read-only static contract preflight runs before candidate-preparation
   activation and validates only already owned contract, parent, manifest,
   edit-envelope, matrix, and future-activation requirements; then
2. after a new exact candidate-preparation owner activation supplies and binds
   the build recipe, an activation-bound candidate preflight runs in the
   authorized staging attempt, computes the candidate-specific fields, and
   freezes the review packet before any review root is created.

The static preflight produces no file, root, authority, candidate identity, or
implementation digest. Its in-memory result is exactly:

```text
static_preflight_schema=mythic_edge_role_pool_v5_static_contract_preflight.v1
contract_path
contract_sha256
parent_contract_path
parent_contract_sha256
manifest_file_count=37
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=contract_sha256
manifest_rebind_amendment_path
manifest_rebind_amendment_sha256
manifest_rebind_status=accepted_implemented_current
parent_edit_envelope_sha256
candidate_edit_envelope_sha256
candidate_operation_profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
candidate_operation_matrix_sha256
candidate_operation_matrix_expected_pair_count=64
candidate_operation_matrix_accepted_pair_count=26
candidate_operation_matrix_rejected_pair_count=38
atomic_observation_oracle_sha256
timestamp_floor_matrix_counts_sha256
failure_matrix_counts_sha256
projection_matrix_counts_sha256
future_activation_requirements_sha256
static_preflight_sha256
```

`static_preflight_sha256` is recomputed over strict canonical JSON with only
that field omitted. A complete static preflight and a separately accepted
manifest amendment are prerequisites to the candidate-preparation owner
activation, not consequences of it.

### Static-preflight digest schemas and canonical test vectors

Every vector in this section uses strict JSON encoded as UTF-8 without BOM,
rejects duplicate and unknown keys, sorts object keys by Unicode code point,
preserves arrays in the exact displayed order, uses JSON integers and lowercase
JSON Booleans without coercion, permits no insignificant whitespace, and ends
with exactly one LF. Each expected SHA-256 is lowercase hexadecimal over those
exact bytes including the final LF. Omitted, extra, renamed, reordered,
duplicated, differently typed, alternate-preimage, or wrong-digest input fails
closed. Shape validation is never sufficient.

Each matrix-count object has exactly six top-level keys:
`accepted_tuple_count` as an integer, `dimensions` as an ordered array,
`expected_tuple_count` as an integer, `matrix_id` as a string,
`rejected_tuple_count` as an integer, and `schema` as a string. Each dimension
has exactly `cardinality` as an integer, `name` as a string, and `values` as an
ordered, duplicate-free string array. Cardinality must equal the array length;
the product of all cardinalities must equal `expected_tuple_count`; and
accepted plus rejected must equal expected.

The exact timestamp-floor matrix-count preimage is:

```json
{"accepted_tuple_count":2,"dimensions":[{"cardinality":3,"name":"parent_chain_state","values":["proven_empty","accepted_receipt_present","unavailable_or_contradictory"]},{"cardinality":4,"name":"timestamp_state","values":["null","valid_populated","invalid_populated","unavailable"]},{"cardinality":5,"name":"digest_state","values":["null","valid_owning","valid_non_owning","invalid_populated","unavailable"]}],"expected_tuple_count":60,"matrix_id":"timestamp_floor","rejected_tuple_count":58,"schema":"mythic_edge_role_pool_v5_timestamp_floor_matrix_counts.v1"}
```

```text
timestamp_floor_matrix_counts_sha256=94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792
```

The exact failure-matrix count preimage is:

```json
{"accepted_tuple_count":20,"dimensions":[{"cardinality":2,"name":"operation_path","values":["blocked_handoff_only","candidate_inventory_then_handoff"]},{"cardinality":20,"name":"sanitized_error_code","values":["source_copy_failed","blocked_handoff_staging_write_failed","blocked_handoff_publish_absent","blocked_handoff_publish_collision","blocked_handoff_publication_state_unknown","blocked_handoff_publication_retry_exhausted","blocked_handoff_staging_cleanup_failed","inventory_staging_write_failed","candidate_pre_inventory_staging_cleanup_failed","inventory_publish_absent","inventory_publish_collision","inventory_publication_state_unknown","inventory_publication_retry_exhausted","inventory_staging_cleanup_failed","handoff_staging_write_failed","handoff_publish_absent","handoff_publish_collision","handoff_publication_state_unknown","handoff_publication_retry_exhausted","handoff_staging_cleanup_failed"]},{"cardinality":8,"name":"failure_phase","values":["source_copy","handoff_staging","handoff_publication","handoff_staging_cleanup","inventory_staging","pre_inventory_staging_cleanup","inventory_publication","inventory_staging_cleanup"]},{"cardinality":3,"name":"external_publication_status","values":["failed_pre_inventory","unknown_after_publish_attempt","failed_post_inventory"]},{"cardinality":3,"name":"inventory_status","values":["not_created","unknown","frozen_candidate"]},{"cardinality":6,"name":"successor_terminal_status","values":["failed_before_inventory","blocked_handoff_state_unknown","publication_state_unknown","frozen_candidate_handoff_unpublished","frozen_candidate_handoff_state_unknown","frozen_candidate_handoff_cleanup_failed"]},{"cardinality":2,"name":"source_copy_status","values":["failed_incomplete","complete"]}],"expected_tuple_count":34560,"matrix_id":"failure","rejected_tuple_count":34540,"schema":"mythic_edge_role_pool_v5_failure_matrix_counts.v1"}
```

```text
failure_matrix_counts_sha256=2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef
```

The projection category identifiers below correspond one-for-one, in row order,
to the five normative binding/projection rows above. The exact projection-matrix
count preimage is:

```json
{"accepted_tuple_count":5,"dimensions":[{"cardinality":5,"name":"operation_result_category","values":["candidate_handoff_candidate_ready_for_independent_review","post_inventory_failure_other_than_inventory_staging_cleanup_failure","inventory_staging_cleanup_failed_projection","blocked_before_inventory_failure","inventory_publication_state_unknown"]},{"cardinality":3,"name":"inventory_status","values":["frozen_candidate","not_created","unknown"]},{"cardinality":2,"name":"binding_presence","values":["present_current_revalidated","absent"]},{"cardinality":3,"name":"staging_observation","values":["final_validated_staging_absent","final_validated_staging_cleanup_failed","not_applicable"]},{"cardinality":2,"name":"digest_source","values":["validated_binding","literal_none"]}],"expected_tuple_count":180,"matrix_id":"binding_projection","rejected_tuple_count":175,"schema":"mythic_edge_role_pool_v5_projection_matrix_counts.v1"}
```

```text
projection_matrix_counts_sha256=8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06
```

The exact atomic-observation oracle is defined under **Atomic single-use
activation consumption** below. Static preflight binds that complete oracle,
not only its tuple count, through:

```text
atomic_observation_oracle_sha256=19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269
```

The parent and candidate edit-envelope digests use bare JSON arrays, not wrapper
objects. Both arrays are sorted by Unicode code point. Their exact test vectors
are:

```json
["client/windows_broker_client.py","tests/test_implementation_handoff.py","tests/test_windows_broker_client.py","tools/publish_implementation_candidate.py"]
```

```text
parent_edit_envelope_sha256=f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1
```

```json
["tests/test_implementation_handoff.py","tools/publish_implementation_candidate.py"]
```

```text
candidate_edit_envelope_sha256=32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed
```

The existing canonical candidate-operation object above recomputes to:

```text
candidate_operation_matrix_sha256=f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d
```

`future_activation_requirements_sha256` uses exactly two keys:
`requirements`, an ordered array of 75 strings, and `schema`, a string. Each
requirement has exactly `field_name|json_type|derivation`; the vertical bars are
literal bytes. The exact canonical preimage is:

```json
{"requirements":["owner_activation_ref|string|derive_from_exact_private_owner_approval_bytes","owner_activation_sha256|string|sha256_exact_private_owner_approval_bytes","owner_activation_status|string|literal:approved_unconsumed","activation_expiry_utc|string|rfc3339_utc_whole_seconds_from_owner_approval","activation_single_use|boolean|literal:true","activation_consumption_mechanism|string|literal:mythic_edge_role_pool_v5_atomic_activation_packet_move.v1","activation_consumption_operation_kind|string|literal:final_seal","activation_consumption_preflight_authorized|boolean|literal:true","activation_consumption_synthetic_validation_authorized|boolean|literal:true","activation_consumption_state_root_creation_authorized|boolean|literal:true","activation_consumption_real_packet_move_authorized|boolean|literal:true","activation_consumption_persisted_helper_authorized|boolean|literal:false","contract_id|string|literal:mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1","contract_path|string|literal:references/external-isolation-broker-v5-corrective-successor.md","contract_sha256|string|sha256_reviewed_contract_bytes","parent_contract_id|string|literal:mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1","parent_contract_sha256|string|sha256_reviewed_parent_contract_bytes","accepted_candidate_revision_ordinal|integer|copy_from_accepted_candidate_review_receipt","accepted_candidate_revision_digest|string|recompute_from_accepted_candidate_packet","accepted_candidate_packet_sha256|string|sha256_accepted_candidate_packet_bytes","independent_candidate_review_receipt_schema|string|literal:mythic_edge_role_pool_v5_candidate_independent_review_receipt.v2","independent_candidate_review_ref|string|derive_from_accepted_review_receipt","independent_candidate_review_receipt_digest|string|recompute_from_accepted_review_receipt","independent_candidate_review_file_sha256|string|sha256_accepted_review_receipt_file_bytes","manifest_file_count|integer|literal:37","manifest_v5_path|string|literal:references/external-isolation-broker-v5-corrective-successor.md","manifest_rebind_from_sha256|string|literal:85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704","manifest_rebind_to_sha256|string|equal:contract_sha256","manifest_rebind_amendment_path|string|copy_from_accepted_manifest_amendment","manifest_rebind_amendment_sha256|string|sha256_accepted_manifest_amendment_bytes","manifest_rebind_status|string|literal:accepted_implemented_current","candidate_edit_envelope_sha256|string|sha256_canonical_candidate_edit_envelope","candidate_operation_profile|string|literal:mythic_edge_role_pool_v5_candidate_operation_authority.v1","candidate_operation_matrix_sha256|string|sha256_canonical_candidate_operation_matrix","candidate_operation_matrix_expected_pair_count|integer|literal:64","candidate_operation_matrix_accepted_pair_count|integer|literal:26","candidate_operation_matrix_rejected_pair_count|integer|literal:38","implementation_sha256|string|sha256_accepted_candidate_implementation_bytes","test_sha256|string|sha256_accepted_candidate_test_bytes","unchanged_source_rows_root_digest|string|recompute_from_accepted_candidate_unchanged_rows","build_recipe_schema|string|literal:mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_ref|string|literal:mythic_edge_role_pool_v5_build_recipe.v1","build_recipe_sha256|string|sha256_canonical_accepted_build_recipe","build_recipe_status|string|literal:complete","build_recipe_independent_review_ref|string|copy_from_accepted_recipe_review_receipt","build_recipe_independent_review_sha256|string|recompute_from_accepted_recipe_review_receipt","build_recipe_independent_review_status|string|literal:accepted_exact_recipe_and_contract","package_authority_profile|string|literal:mythic_edge_role_pool_external_isolation_broker_package_authority.v5","package_id|string|literal:mythic_edge_role_pool_windows_broker_verifier_preparation.v5","package_directory_name|string|literal:MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v5","inventory_schema|string|literal:mythic_edge_role_pool_windows_broker_verifier_package_inventory.v5","handoff_schema|string|literal:mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v5","publication_failure_schema|string|literal:mythic_edge_role_pool_package_publication_failure.v3","package_creation_authorized|boolean|literal:true","source_copy_authorized|boolean|literal:true","local_source_copy_authorized|boolean|literal:true","package_build_authorized|boolean|literal:true","local_build_authorized|boolean|literal:true","package_self_tests_authorized|boolean|literal:true","inventory_creation_authorized|boolean|literal:true","handoff_creation_authorized|boolean|literal:true","handoff_publication_authorized|boolean|literal:true","failure_artifact_creation_authorized|boolean|literal:true","installation_authorized|boolean|literal:false","service_mutation_authorized|boolean|literal:false","canary_authorized|boolean|literal:false","stage_advancement_authorized|boolean|literal:false","external_mutation_authorized|boolean|literal:false","live_ready|boolean|literal:false","current_v4_reuse_authorized|boolean|literal:false","correctness_claimed|boolean|literal:false","security_assurance_claimed|boolean|literal:false","privacy_assurance_claimed|boolean|literal:false","release_readiness_claimed|boolean|literal:false","production_readiness_claimed|boolean|literal:false"],"schema":"mythic_edge_role_pool_v5_future_activation_requirements.v2"}
```

```text
future_activation_requirements_sha256=a955b153f34f5dd861662b95ee9a1fa52b523ad666855004ec924d371b9b0bd2
```

The complete static-preflight test fixture below is synthetic and grants no
authority. Its 64 `a` characters represent an invented fixture contract digest;
its 64 `b` characters represent an invented fixture amendment digest. This
avoids impossible self-reference while exercising the exact production schema.
Production preflight must replace both with independently recomputed owning
artifact digests and must require `manifest_rebind_to_sha256` to equal
`contract_sha256`. The complete fixture is:

```json
{"atomic_observation_oracle_sha256":"19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269","candidate_edit_envelope_sha256":"32694f48845e22fcf597b5b1b32600c905e3af0478d3ac2ef2993684a44aebed","candidate_operation_matrix_accepted_pair_count":26,"candidate_operation_matrix_expected_pair_count":64,"candidate_operation_matrix_rejected_pair_count":38,"candidate_operation_matrix_sha256":"f822d52edaaf32a0d8cf84288ba741d2856bcd3d56adc621e071ebd5b343552d","candidate_operation_profile":"mythic_edge_role_pool_v5_candidate_operation_authority.v1","contract_path":"references/external-isolation-broker-v5-corrective-successor.md","contract_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","failure_matrix_counts_sha256":"2212582e3af79e7c1b125d55623de2ac757912c068e3957c688aa7a78f90e2ef","future_activation_requirements_sha256":"a955b153f34f5dd861662b95ee9a1fa52b523ad666855004ec924d371b9b0bd2","manifest_file_count":37,"manifest_rebind_amendment_path":"references/stage3-behavioral-planning.md","manifest_rebind_amendment_sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","manifest_rebind_from_sha256":"85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704","manifest_rebind_status":"accepted_implemented_current","manifest_rebind_to_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","manifest_v5_path":"references/external-isolation-broker-v5-corrective-successor.md","parent_contract_path":"references/external-isolation-broker-v4-corrective-successor.md","parent_contract_sha256":"628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487","parent_edit_envelope_sha256":"f9b27efa62cc6b7f8d6f69dbb85ba7c335daebb452eb09afe0229488768d9fa1","projection_matrix_counts_sha256":"8c12cca36ce236c55264afe1b70fb464a59e9594cb976d9e2e8178c50f8bca06","static_preflight_schema":"mythic_edge_role_pool_v5_static_contract_preflight.v1","static_preflight_sha256":"d34aa78c1ab739b668fca64f69d8b7d7fab2e79315f04fb861dc562a97683485","timestamp_floor_matrix_counts_sha256":"94374945d2619fe9c7251f78f80884560b839e7b6421d3bbfa246b1c56efb792"}
```

To recompute `static_preflight_sha256`, omit only that field, canonicalize the
remaining 24 fields under the rules above, and hash the resulting bytes. The
expected fixture result is:

```text
static_preflight_sha256=d34aa78c1ab739b668fca64f69d8b7d7fab2e79315f04fb861dc562a97683485
```

Static preflight must mechanically prove the candidate array is a strict subset
of the parent array by exact case-sensitive membership and cardinality, not by
digest equality alone. It must enumerate every matrix Cartesian product, prove
exhaustiveness and mutual exclusion, compare exact expected, accepted, and
rejected counts, and enumerate the complete atomic-observation oracle with its
five exact outcome counts. It must jointly validate the contract, accepted
manifest amendment and all manifest effects, edit scope, all matrix objects,
the exact oracle, and complete future-activation vector before an owner approval
can be requested.

The later activation-bound packet adds the independently accepted recipe,
implementation and test file digests, consumed activation binding, candidate
revision, and packet digest to this static-preflight digest. Consequently the
contract, amendment, scope, matrices, recipe, tests, and activation form one
digest-bound packet without making the static fixture an authority artifact.
Missing, stale, contradictory, cross-attempt, cross-contract, cross-amendment,
cross-recipe, or correctly shaped but incorrect bindings reject before any
candidate root, activation consumption, package state, or output exists.

After that activation is validated and atomically reserved for one candidate
workflow, the activation-bound preflight must produce and validate a canonical
review packet with:

```text
preflight_schema=mythic_edge_role_pool_v5_review_preflight_packet.v2
contract_path=references/external-isolation-broker-v5-corrective-successor.md
contract_sha256
parent_contract_path=references/external-isolation-broker-v4-corrective-successor.md
parent_contract_sha256
manifest_file_count=37
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=contract_sha256
manifest_rebind_amendment_path
manifest_rebind_amendment_sha256
manifest_rebind_status=accepted_implemented_current
parent_edit_envelope_paths
candidate_edit_envelope_paths
candidate_edit_envelope_sha256
candidate_operation_profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
candidate_operation_matrix_sha256
candidate_operation_matrix_expected_pair_count=64
candidate_operation_matrix_accepted_pair_count=26
candidate_operation_matrix_rejected_pair_count=38
implementation_path=tools/publish_implementation_candidate.py
implementation_sha256
test_path=tests/test_implementation_handoff.py
test_sha256
unchanged_source_rows_root_digest
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_ref
build_recipe_sha256
build_recipe_status=complete
build_recipe_independent_review_ref
build_recipe_independent_review_sha256
build_recipe_independent_review_status=accepted_exact_recipe_and_contract
static_preflight_sha256
candidate_preparation_owner_activation_ref
candidate_preparation_owner_activation_sha256
candidate_preparation_activation_expiry_utc
candidate_preparation_activation_single_use=true
candidate_preparation_activation_schema=mythic_edge_role_pool_v5_candidate_preparation_activation.v2
candidate_preparation_activation_packet_sha256
activation_consumption_mechanism=mythic_edge_role_pool_v5_atomic_activation_packet_move.v1
activation_consumption_operation_kind=candidate_preparation
activation_consumption_key_sha256
candidate_preparation_activation_status=consumed_for_candidate_workflow
candidate_max_correction_cycles=2
timestamp_floor_matrix_expected_tuple_count=60
timestamp_floor_matrix_accepted_tuple_count=2
timestamp_floor_matrix_rejected_tuple_count=58
failure_matrix_expected_tuple_count=34560
failure_matrix_accepted_tuple_count=20
failure_matrix_rejected_tuple_count=34540
projection_matrix_expected_tuple_count=180
projection_matrix_accepted_tuple_count=5
projection_matrix_rejected_tuple_count=175
candidate_revision_ordinal
candidate_prior_revision_digest
candidate_correction_finding_ids
candidate_lifecycle_status
future_seal_required=true
future_activation_requirements_sha256
candidate_revision_digest
packet_sha256
```

The packet is strict canonical JSON: UTF-8 without BOM, duplicate keys rejected,
unknown keys rejected, keys sorted by Unicode code point, arrays in their
contracted order, no insignificant whitespace, and one final LF. Its
`packet_sha256` is lowercase SHA-256 over those canonical bytes with only
`packet_sha256` omitted. It is a review binding, not authority, and is never a
package inventory, external handoff, lifecycle claim, or public readiness
artifact.

`candidate_preparation_activation_packet_sha256` is recomputed from the exact
moved packet bytes. `activation_consumption_key_sha256` is recomputed from the
ten-key canonical object and must select the one exact local destination without
emitting that destination. Both are lowercase digests, not caller authority.
The consumed status is valid only after this actor's successful move and full
readback; a Boolean-only, path-bearing, caller-supplied, or shape-only projection
is forbidden.

`parent_edit_envelope_paths` is recomputed from the exact accepted parent
contract and is exactly:

```text
client/windows_broker_client.py
tools/publish_implementation_candidate.py
tests/test_windows_broker_client.py
tests/test_implementation_handoff.py
```

`candidate_edit_envelope_paths` is the sorted exact two-path v5 envelope. The
preflight must mechanically prove it is a strict subset of the parent set. A
missing parent row, extra candidate row, duplicate, case variation, separator
variation, normalization change, or shape-only comparison fails closed.
`candidate_edit_envelope_sha256` is computed over the canonical two-element
array, not accepted from a caller.

Every path, count, file SHA-256, object digest, root digest, inventory binding,
handoff binding, contract binding, parent binding, manifest binding, edit-set
binding, and build-recipe binding is recomputed from its owning artifact or
canonical object. Syntax or length validation alone is never sufficient. A
caller-provided expected value is comparison-only and cannot become the owning
value.

The manifest fields require an independently accepted and implemented exact
rebind amendment that keeps the manifest at 37 files, preserves the exact v5
path, replaces only the pre-revision digest with `contract_sha256`, and leaves
every other manifest binding and rule unchanged. Until that later rebind exists,
the static preflight is incomplete and no candidate-preparation owner activation
may be accepted. This requirement does not authorize the amendment or any
manifest implementation.

The future candidate-preparation approval reuses the inherited symbolic owner-
approval reference grammar and uses the contract-defined atomic consumption
mechanism below. It has the closed 69-field profile
`mythic_edge_role_pool_v5_candidate_preparation_activation.v2`. V1 packets are
obsolete for this revised contract and fail closed. V2 must bind:

```text
candidate_preparation_owner_activation_ref
candidate_preparation_owner_activation_sha256
candidate_preparation_activation_status=approved_unconsumed
candidate_preparation_activation_expiry_utc
candidate_preparation_activation_single_use=true
activation_consumption_mechanism=mythic_edge_role_pool_v5_atomic_activation_packet_move.v1
activation_consumption_operation_kind=candidate_preparation
activation_consumption_preflight_authorized=true
activation_consumption_synthetic_validation_authorized=true
activation_consumption_state_root_creation_authorized=true
activation_consumption_real_packet_move_authorized=true
activation_consumption_persisted_helper_authorized=false
contract_id
contract_path
contract_sha256
parent_contract_id
parent_contract_sha256
static_preflight_sha256
manifest_file_count=37
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=contract_sha256
manifest_rebind_amendment_path
manifest_rebind_amendment_sha256
manifest_rebind_status=accepted_implemented_current
candidate_edit_envelope_sha256
candidate_operation_profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
candidate_operation_matrix_sha256
candidate_operation_matrix_expected_pair_count=64
candidate_operation_matrix_accepted_pair_count=26
candidate_operation_matrix_rejected_pair_count=38
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_ref
build_recipe_sha256
build_recipe_status=complete
build_recipe_independent_review_ref
build_recipe_independent_review_sha256
build_recipe_independent_review_status=accepted_exact_recipe_and_contract
candidate_revision_zero_authorized=true
candidate_max_correction_cycles=2
codex_d_corrections_conditionally_authorized=true
candidate_parent_inventory_metadata_read_authorized=true
candidate_parent_source_rows_read_authorized=true
candidate_prior_revision_read_authorized=true
candidate_source_copy_authorized=true
disposable_candidate_implementation_edit_authorized=true
disposable_candidate_test_edit_authorized=true
candidate_build_recipe_execution_authorized=true
candidate_test_execution_authorized=true
candidate_disposable_output_creation_authorized=true
candidate_staging_root_creation_authorized=true
candidate_preflight_packet_creation_authorized=true
candidate_review_root_creation_authorized=true
candidate_independent_review_read_authorized=true
independent_review_receipt_creation_authorized=true
candidate_staging_cleanup_authorized=true
final_package_root_creation_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
publication_authorized=false
source_repository_access_authorized=false
network_access_authorized=false
external_write_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_mutation_authorized=false
live_ready=false
```

`candidate_preparation_owner_activation_ref` must match the inherited exact
`^owner_activation_v1_[0-9a-f]{32}$` grammar, and its SHA-256 must be recomputed
from the exact private approval bytes. Neither value may be derived from a path
or accepted by shape alone.

The activation is valid only after the static preflight and before any
candidate staging path. It authorizes one candidate workflow, revision 0, and
at most two later D corrections tied to exact E findings; it does not authorize
one operation per revision. The contract-defined single-attempt mechanism below
atomically moves the exact validated activation packet from
`approved_unconsumed` to immutable consumed state before candidate staging
begins. Failure to prove exclusive consumption blocks without creating a
candidate root. Reuse, a second workflow, or a broader Boolean is invalid.

### Atomic single-use activation consumption

The failed preconsumption pass for
`owner_activation_v1_ddd3b91d8be64864a0ee656edabd7729` proved that no
executable or persisted inherited mechanism currently performs the transition
above. That activation was rejected before consumption, its private transport
was removed, and it is not reusable. This section replaces the undefined
inherited-mechanism assumption with exactly one contract-defined mechanism:

```text
activation_consumption_mechanism=mythic_edge_role_pool_v5_atomic_activation_packet_move.v1
activation_consumption_state_kind=exact_moved_activation_packet
activation_consumption_state_root_resolver=windows_current_user_local_application_data_known_folder.v1
activation_consumption_state_root_suffix=["MythicEdge","RolePool","activation-consumption","v1"]
activation_consumption_filesystem_profile=windows_local_fixed_ntfs_same_volume.v1
activation_consumption_api=System.IO.File.Move(source,destination)
activation_consumption_invocation_host=existing_windows_powershell_process.v1
activation_consumption_invocation_expression=[System.IO.File]::Move($source_path,$destination_path)
activation_consumption_persisted_helper_authorized=false
activation_consumption_replace_existing=false
activation_consumption_retry_count=0
activation_consumption_resume_authorized=false
activation_consumption_record_deletion_authorized=false
```

This is a contract definition, not current execution authority and not a new
executable, dependency, service, database, registry key, cache, or general
lifecycle API. It uses the Windows and .NET no-replace, same-volume move that is
already present on the supported host. Any non-Windows host, non-NTFS volume,
network or removable volume, cross-volume source, unavailable API behavior, or
inability to prove no-replace semantics blocks before state-root or candidate-
root creation.

No helper implementation is required or authorized. A future exact owner
activation may permit Codex C to invoke only the displayed two-argument .NET
method from the existing PowerShell process after all preconsumption checks.
`$source_path` and `$destination_path` are ephemeral private variables derived
under this contract; their values must never enter command logs, public output,
history, a script file, or an artifact. Reflection, another overload, a shell
cmdlet, native move utility, subprocess, fallback, or persisted wrapper is not
equivalent.

That future activation must separately authorize this closed preconsumption
scope: contract and manifest validation; private approval and packet validation;
disposable invented same-volume move tests with complete cleanup; state-root
validation or exact suffix creation; and one real packet-move invocation. It
authorizes no package/source read, candidate root, build, inventory, handoff, or
publication operation until the real move and complete readback succeed. This
contract thread grants none of those operations.

The state-root resolver calls the Windows known-folder API for the current
user's `LocalApplicationData` location. It must not trust an environment value,
caller path, working directory, symlink, junction, mount alias, short-name
substitution, or search path. The four suffix segments above are literal and
case-sensitive. Every existing component from the known-folder root through
the final state root must be an ordinary local directory, owned by the current
user or the operating system, and not a reparse point. The final directory must
not grant write, modify, delete, ownership, or permission-change access to an
untrusted principal. A future exact owner activation may authorize creation of
only missing literal suffix directories followed by immediate owner, ACL,
volume, identity, and no-reparse readback. This contract thread authorizes no
directory creation.

The root security profile is closed. The root owner SID must equal the current
Windows user SID or `S-1-5-18` (`LOCAL_SYSTEM`). Every allow ACE that grants
write, append, delete, modify, ownership, or permission-change rights must name
only the current user SID, `S-1-5-18`, or `S-1-5-32-544`
(`BUILTIN_ADMINISTRATORS`). An allow ACE for any other SID, an unresolved SID,
an inherited identity that cannot be enumerated, a null or unreadable DACL, or
an effective-access result that cannot be derived blocks. Deny ACEs do not make
an otherwise forbidden allow ACE acceptable. The source packet and moved
destination must pass the same file-owner and effective-write checks.

Same-volume proof requires equal case-insensitive canonical drive roots, each
expressed as one drive letter plus `:\`, `DriveType=Fixed`, and
`DriveFormat=NTFS`. A volume mount path, UNC path, device path, substituted
drive, unavailable drive metadata, or differing canonical root blocks before
the move. These checks are local private observations and must not be emitted.

The exact activation-consumption key object has ten keys:

```text
schema=mythic_edge_role_pool_v5_atomic_activation_consumption_key.v1
operation_kind
activation_ref
activation_sha256
activation_packet_sha256
activation_expiry_utc
contract_id
contract_sha256
manifest_rebind_amendment_sha256
static_preflight_sha256
```

`operation_kind` is exactly `candidate_preparation` or `final_seal` and is
derived from the one schema-valid activation profile; it is never caller
selected. Candidate preparation uses the candidate-preparation activation
fields; final sealing uses the separate seal activation fields. The exact
contract digest transitively binds the mechanism and root profile without
adding packet fields. All other values are recomputed from
their owning activation bytes, contract, accepted and implemented manifest
amendment, or static preflight. The key object is strict canonical JSON:
UTF-8 without BOM, sorted keys, no duplicate or unknown keys, no insignificant
whitespace, and one final LF. `activation_consumption_key_sha256` is lowercase
SHA-256 over those exact bytes. A shape-valid caller digest is comparison-only.

The destination basename is exactly:

```text
"activation-consumed-v1-" + activation_consumption_key_sha256 + ".json"
```

It is a direct child of the validated state root. The destination content is
the exact already validated activation-packet bytes, unchanged. The private
approval-source bytes, approval text, source path, destination path, known-
folder value, ACL, exception, and local identity are never copied into that
file or any public output. The activation packet's
`approved_unconsumed` literal records its issuance state; only the successful
move and complete readback below derive the later lifecycle status.

The ordered consumption algorithm is normative:

1. Recompute and validate every contract, manifest, static-preflight, approval,
   packet, recipe, expiry, field-set, false-authority, and no-echo binding while
   both private inputs remain local and before creating the state root.
2. Require the approval source and packet to be ordinary non-reparse files,
   require their exact expected SHA-256 values, derive the canonical key and
   destination basename, and prove source and destination roots are on the same
   local fixed NTFS volume.
3. Validate or, only under a fresh exact owner activation, create and read back
   the exact state root. Require the destination to be absent. An existing
   destination always blocks, even when its bytes are valid and identical.
4. Close every packet read handle, immediately restat and rehash the source,
   then invoke exactly `System.IO.File.Move(source,destination)` with no
   overwrite or fallback. Copy/delete, replace, hard-link, alternate stream,
   shell move, retry, repair, and destination adoption are forbidden.
5. Only the actor whose exact move call returns success is the winner. That
   actor must immediately reopen the destination with exclusive sharing,
   revalidate ordinary-file and no-reparse identity, exact bytes, packet hash,
   key derivation, expiry, contract, amendment, and static preflight, then close
   the handle. Only complete readback derives
   `consumed_for_candidate_workflow` or `consumed_for_final_seal`.
6. Delete the private approval-source input after validation. After a terminal
   rejection, remove only the exact attempt-owned transport packet under
   identity and no-reparse checks. Never delete, overwrite, rename, truncate,
   repair, or adopt a destination in the consumption state root.

The atomic authority event is the no-replace destination creation performed by
the successful same-volume move. Full readback is a separate prerequisite for
continuing. `activation_consumption_retry_count=0` prohibits a second move call
after an observed return or an unavailable post-invocation outcome; it does not
prohibit repeating read-only validation before any move invocation. A crash
before invocation creates no consumption state. The same still-current packet
may undergo fresh read-only validation only while its exact approval bytes also
remain present, its destination remains absent, and no package or candidate
side effect exists. That is continued preconsumption validation, not reuse.

A crash after invocation but before complete readback leaves the activation
irreversibly unavailable for work. Even if a destination later validates, no
actor may reconstruct the original call's success observation or continue. A
second actor may never infer that it is the winner from matching bytes.

Status derivation uses one finite Cartesian observation universe and the exact
ordered oracle below. Each raw observation must project to exactly one literal
in every dimension before rule selection. Caller-supplied labels are forbidden.
The dimensions, their exact value order, and their cardinalities are:

| Dimension | Ordered values | Cardinality |
| --- | --- | --- |
| `prevalidation_result` | `passed`, `failed`, `unavailable` | 3 |
| `move_invocation_result` | `not_invoked`, `returned_success`, `returned_failure`, `outcome_unavailable` | 4 |
| `source_file_state` | `exact`, `absent`, `invalid`, `unavailable` | 4 |
| `destination_file_state` | `exact`, `absent`, `invalid`, `unavailable` | 4 |
| `exclusive_readback_result` | `not_performed`, `passed`, `failed`, `unavailable` | 4 |

The product is exactly `3 * 4 * 4 * 4 * 4 = 768` tuples.
`prevalidation_result=failed` means the ordered prevalidation completed with a
blocking result; inability to obtain a stable result is `unavailable`.
For either file state, `invalid` means a present observation deterministically
failed the required ordinary-file, identity, or exact-byte checks, while
`unavailable` means no stable state could be read. `exclusive_readback_result`
describes only the post-invocation winner readback in step 5; no such attempt is
`not_performed`. Missing, unknown, or differently named values fail closed and
cannot be coerced into another literal.

The five lifecycle outcome categories and exact selectors are:

| Priority | Exact selector | Outcome category | Candidate or final root allowed |
| --- | --- | --- | --- |
| 1 | prevalidation `passed`; invocation `returned_success`; source `absent`; destination `exact`; readback `passed` | `consumed_for_derived_operation` | yes, only after operation-kind projection below |
| 2 | prevalidation `passed`; invocation `not_invoked`; source `exact`; destination `absent`; readback `not_performed` | `approved_unconsumed` | no |
| 3 | source `absent`; destination `exact`; and it is not true that invocation is `returned_success` and readback is `passed` | `activation_already_consumed` | no |
| 4 | prevalidation `failed`; invocation `not_invoked`; destination `absent`; readback `not_performed` | `rejected_before_atomic_consumption` | no |
| 5 | default after no earlier selector wins | `activation_consumption_state_unknown` | no |

The oracle predicate representation is closed. Each non-default rule has
`default=false`; every `all` clause must match; a nonempty `not_all` rejects the
rule only when all of its clauses match together. A clause has exactly
`dimension` and `values`; every listed value must occur in that dimension's
ordered vocabulary. Omitted dimensions are unconstrained. The sole default rule
has empty clause arrays, `default=true`, and is selected only after all earlier
rules fail. Priorities are the unique integers 1 through 5 and lowest wins.

There are five outcome categories because the successful category is projected
only after selection. `candidate_preparation` maps it to
`consumed_for_candidate_workflow`; `final_seal` maps it to
`consumed_for_final_seal`. Operation kind never changes another category.

The oracle has exactly six top-level keys: `dimensions`,
`expected_tuple_count`, `operation_kind_projection`, `outcome_counts`, `rules`,
and `schema`. Nested objects have exactly the keys shown. It uses the same
strict canonical JSON and final-LF rules as the static-preflight vectors. Its
exact canonical preimage is:

```json
{"dimensions":[{"cardinality":3,"name":"prevalidation_result","values":["passed","failed","unavailable"]},{"cardinality":4,"name":"move_invocation_result","values":["not_invoked","returned_success","returned_failure","outcome_unavailable"]},{"cardinality":4,"name":"source_file_state","values":["exact","absent","invalid","unavailable"]},{"cardinality":4,"name":"destination_file_state","values":["exact","absent","invalid","unavailable"]},{"cardinality":4,"name":"exclusive_readback_result","values":["not_performed","passed","failed","unavailable"]}],"expected_tuple_count":768,"operation_kind_projection":[{"operation_kind":"candidate_preparation","status_literal":"consumed_for_candidate_workflow"},{"operation_kind":"final_seal","status_literal":"consumed_for_final_seal"}],"outcome_counts":[{"count":1,"outcome":"consumed_for_derived_operation"},{"count":1,"outcome":"approved_unconsumed"},{"count":45,"outcome":"activation_already_consumed"},{"count":4,"outcome":"rejected_before_atomic_consumption"},{"count":717,"outcome":"activation_consumption_state_unknown"}],"rules":[{"all":[{"dimension":"prevalidation_result","values":["passed"]},{"dimension":"move_invocation_result","values":["returned_success"]},{"dimension":"source_file_state","values":["absent"]},{"dimension":"destination_file_state","values":["exact"]},{"dimension":"exclusive_readback_result","values":["passed"]}],"default":false,"not_all":[],"outcome":"consumed_for_derived_operation","priority":1},{"all":[{"dimension":"prevalidation_result","values":["passed"]},{"dimension":"move_invocation_result","values":["not_invoked"]},{"dimension":"source_file_state","values":["exact"]},{"dimension":"destination_file_state","values":["absent"]},{"dimension":"exclusive_readback_result","values":["not_performed"]}],"default":false,"not_all":[],"outcome":"approved_unconsumed","priority":2},{"all":[{"dimension":"source_file_state","values":["absent"]},{"dimension":"destination_file_state","values":["exact"]}],"default":false,"not_all":[{"dimension":"move_invocation_result","values":["returned_success"]},{"dimension":"exclusive_readback_result","values":["passed"]}],"outcome":"activation_already_consumed","priority":3},{"all":[{"dimension":"prevalidation_result","values":["failed"]},{"dimension":"move_invocation_result","values":["not_invoked"]},{"dimension":"destination_file_state","values":["absent"]},{"dimension":"exclusive_readback_result","values":["not_performed"]}],"default":false,"not_all":[],"outcome":"rejected_before_atomic_consumption","priority":4},{"all":[],"default":true,"not_all":[],"outcome":"activation_consumption_state_unknown","priority":5}],"schema":"mythic_edge_role_pool_v5_atomic_observation_oracle.v1"}
```

```text
atomic_observation_oracle_sha256=19f3c4bea26d510f5209bd24ebde18a1a9527af85ba61e0bb50f8a0e55923269
```

Focused contract tests must enumerate all 768 tuples, apply the ordered rules,
and prove exactly one selected outcome per tuple with these counts in displayed
order: `1`, `1`, `45`, `4`, and `717`. They must recompute the oracle digest,
reject any schema, order, value, count, predicate, projection, or digest drift,
and prove that crossing the 768 tuples with the two operation kinds yields the
two exact consumed literals without changing any other outcome. This closes the
finite-oracle requirement raised by `EIB-PKG-V5-ATOMIC-E-001`; only a later
independent Codex E review may mark that finding resolved.

No status transitions back to
`approved_unconsumed`. Neither an identical packet nor an identical valid
destination authorizes replay, recovery, resume, or continuation after a move
invocation. The immutable destination remains local-only and retained until a
separate reviewed cleanup contract and exact owner approval authorize otherwise.
Its existence is single-use lifecycle evidence only; it is not package evidence,
a public receipt, readiness evidence, a security boundary, or proof of correct
candidate behavior.

Before any real consumption, a future authorized C pass must use disposable
invented packets and temporary same-volume roots to prove: exactly one winner
under two simultaneous actors; read-only restart before move; duplicate-source
collision rejection; existing valid and malformed destination rejection;
crash-after-invocation replay blocking; all source/destination presence pairs;
returned-failure and unknown-outcome handling; source, packet, approval, expiry,
digest, ACL, root, volume, reparse, and readback failures; different operation
kinds producing different keys; zero candidate/final roots on every rejected or
unknown result; no private value in state or output; and exact cleanup limits.
Synthetic success grants no real activation or package authority.

### Candidate operation authority closure

The candidate-preparation activation authorizes only the closed operation
profile `mythic_edge_role_pool_v5_candidate_operation_authority.v1`. Its
operation vocabulary is:

```text
read_parent_inventory_metadata
read_parent_source_rows
read_prior_candidate_revision
read_prior_independent_review_receipt
create_candidate_staging_root
copy_candidate_source_rows
edit_candidate_implementation_path
edit_candidate_test_path
execute_bound_build_recipe
execute_bound_candidate_tests
create_candidate_disposable_outputs
create_candidate_preflight_packet
create_candidate_review_root
read_frozen_candidate_for_review
create_independent_review_receipt
cleanup_exact_candidate_staging_root
```

The actor/operation matrix is normative:

| actor and revision | required predecessor | allowed reads | allowed creates, edits, executions, and cleanup |
| --- | --- | --- | --- |
| `codex_c_candidate_preparer`, revision `0` | consumed candidate-workflow activation; absent staging and review roots | exact v4 inventory metadata and its 46 bound source rows | create exact staging root; copy 46 rows; edit only the two v5 paths; execute bound build and tests; create disposable outputs, preflight packet, and immutable review root; clean exact staging root |
| `codex_d_bounded_candidate_fixer`, revision `1` or `2` | exact prior E receipt with `bounded_correction_required`; ordinal available; same consumed workflow activation unexpired | exact prior frozen candidate, packet, receipt, and finding-bound two-path scope | create new exact staging root; copy prior 46 rows; edit only finding-bound content in the two v5 paths; execute the unchanged bound build and tests; create new disposable outputs, packet, and immutable review root; clean exact staging root |
| `codex_e_independent_reviewer`, revision `0`, `1`, or `2` | exact frozen candidate in `candidate_review_pending`; same workflow activation unexpired | exact frozen candidate, packet, and symbolic validation summaries | create only the no-replace sibling independent-review receipt |
| `final_seal_actor_without_activation` | accepted E receipt but no separate final-seal activation | none | none |

The canonical matrix object has exactly these keys and values; unknown keys are
forbidden and all arrays preserve the order shown:

```text
matrix_schema=mythic_edge_role_pool_v5_candidate_operation_matrix.v1
profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
operation_vocabulary=[
  read_parent_inventory_metadata,
  read_parent_source_rows,
  read_prior_candidate_revision,
  read_prior_independent_review_receipt,
  create_candidate_staging_root,
  copy_candidate_source_rows,
  edit_candidate_implementation_path,
  edit_candidate_test_path,
  execute_bound_build_recipe,
  execute_bound_candidate_tests,
  create_candidate_disposable_outputs,
  create_candidate_preflight_packet,
  create_candidate_review_root,
  read_frozen_candidate_for_review,
  create_independent_review_receipt,
  cleanup_exact_candidate_staging_root
]
rows=[
  {
    actor=codex_c_candidate_preparer,
    revision_ordinals=[0],
    predecessor=candidate_workflow_activation_consumed_revision_zero_roots_absent,
    allowed_operations=[
      read_parent_inventory_metadata,
      read_parent_source_rows,
      create_candidate_staging_root,
      copy_candidate_source_rows,
      edit_candidate_implementation_path,
      edit_candidate_test_path,
      execute_bound_build_recipe,
      execute_bound_candidate_tests,
      create_candidate_disposable_outputs,
      create_candidate_preflight_packet,
      create_candidate_review_root,
      cleanup_exact_candidate_staging_root
    ]
  },
  {
    actor=codex_d_bounded_candidate_fixer,
    revision_ordinals=[1,2],
    predecessor=prior_e_bounded_correction_receipt_unexpired_ordinal_available,
    allowed_operations=[
      read_prior_candidate_revision,
      read_prior_independent_review_receipt,
      create_candidate_staging_root,
      copy_candidate_source_rows,
      edit_candidate_implementation_path,
      edit_candidate_test_path,
      execute_bound_build_recipe,
      execute_bound_candidate_tests,
      create_candidate_disposable_outputs,
      create_candidate_preflight_packet,
      create_candidate_review_root,
      cleanup_exact_candidate_staging_root
    ]
  },
  {
    actor=codex_e_independent_reviewer,
    revision_ordinals=[0,1,2],
    predecessor=frozen_candidate_review_pending_activation_unexpired,
    allowed_operations=[
      read_frozen_candidate_for_review,
      create_independent_review_receipt
    ]
  },
  {
    actor=final_seal_actor_without_activation,
    revision_ordinals=[0,1,2],
    predecessor=accepted_e_receipt_without_final_seal_activation,
    allowed_operations=[]
  }
]
expected_pair_count=64
accepted_pair_count=26
rejected_pair_count=38
```

The text above is a schema notation for strict canonical JSON, not an alternate
serialization. Keys and literals are JSON strings, ordinal and count values are
JSON integers, and the empty allowed-operation array is the only permitted
absence representation. There are no null, omitted, wildcard, inherited,
default-allow, or free-text actor, predecessor, operation, or revision values.

`candidate_operation_matrix_sha256` is recomputed over a canonical object
containing that exact schema, profile literal, ordered operation vocabulary,
four ordered matrix rows, and three counts. Shape-valid caller input is
comparison-only. Any omitted,
extra, duplicated, reordered, relabelled, or differently scoped operation,
actor, revision, predecessor, read, write, execution, or cleanup changes the
digest and fails closed.

The matrix universe is the exact Cartesian product of four actor categories and
16 operation literals: 64 expected actor-operation pairs. The C row accepts 12,
the D row accepts 12, the E row accepts two, and the unactivated final-seal row
accepts zero, for exactly 26 accepted and 38 rejected pairs. Validation must
enumerate all 64 pairs, classify each pair exactly once, and prove every accepted
pair is owned by exactly one normative row. A nominally allowed pair still
rejects when its revision ordinal, predecessor, activation, receipt, expiry,
finding binding, path envelope, or other row precondition does not match.

For C, parent reads are limited to metadata validation and the exact 46 source
rows in the accepted v4 inventory; generated v4 outputs are never read or
copied. For D, parent-package reads are forbidden: the exact prior frozen
candidate is the sole source. For E, all reads are nonmutating and the receipt
is the sole write. C and D may execute only the bound local no-network recipe
and tests. Candidate test output is reduced to symbolic counts and statuses;
raw output is neither retained nor echoed.

The generic fields `implementation_authorized`, `package_creation_authorized`,
`inventory_creation_authorized`, and `publication_authorized` remain false
throughout candidate work. Candidate-specific true fields do not imply or
upgrade any generic authority. Every actor/operation combination not expressly
allowed by the matrix is forbidden. In particular, no candidate activation
permits source-repository access, network access, final-root creation, final
inventory or handoff creation, publication, installation, service mutation,
canary work, stage advancement, external writes, or live use.

### Closed owner-selected v5 build-recipe binding

The only permitted recipe schema is
`mythic_edge_role_pool_v5_build_recipe.v1`, with fixed reference
`mythic_edge_role_pool_v5_build_recipe.v1`. The owner has selected a new,
deterministic v5 recipe from the exact verified v4 archive, scripts, input root,
output names, command order, and result counts below. The recipe is not a
reconstruction of the unretained v4 literal command tuple and must never be
described as historically identical to that tuple. Discovery from package
source, script parsing, filesystem search, ambient shell state, command
history, logs, neighboring files, package indexes, network access,
substitution, fallback, or reinterpretation remains forbidden.

The independently inspectable v4 evidence binding is indivisible:

```text
v4_contract_id=mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1
v4_contract_path=references/external-isolation-broker-v4-corrective-successor.md
v4_contract_file_sha256=628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487
v4_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4.implementation-handoff.v4.json
v4_handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v4
v4_handoff_file_sha256=adbe95cf2b37c666dcbc72fe295e50464fb20140e63053b107e58772f7af10c5
v4_handoff_root_digest=e8941e8dd92d4bf9ff581b335f639420fd493c7ac724f50c142e843b7350dc51
v4_handoff_status=candidate_ready_for_independent_review
v4_inventory_filename=package-inventory.json
v4_inventory_schema=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v4
v4_inventory_file_sha256=a805429be56e60fa9f29a7f3562d8a11b5a5966e9177f33f15f81e3f1c8bc298
v4_inventory_root_digest=bc2240e7ceea848404becc18914d41e78699ee0aee1316c0619bd7a12e423994
v4_inventory_file_count=51
v4_inventory_total_length_bytes=6136931
v4_source_row_count=46
v4_generated_output_row_count=5
v4_trusted_go_archive_sha256_from_handoff=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
v4_trusted_go_archive_sha256_from_inventory=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
v4_component_provenance_status=verified_metadata_subset_command_tuple_unretained
historical_v4_command_tuple_verified=false
exact_v4_archive_reused=true
exact_v4_build_scripts_reused=true
v5_recipe_selection=owner_selected_from_verified_v4_components
```

The binding is component-provenance evidence, not v4 acceptance, v4 package
reuse authority, or evidence of the historical v4 invocation. Before an
independent reviewer may accept the proposed v5 recipe, that reviewer must
mechanically perform every row below without reading package source:

The exact v4 handoff resolves as the inherited package-parent resolver joined
with `v4_handoff_filename`. The exact inventory resolves as that same parent,
`rejected_v4_package_directory_name`, and `v4_inventory_filename`. The contract
resolves relative to the installed Role Pool skill root. Resolution must reject
absolute caller input, ambiguity, case drift, reparse points, and non-ordinary
files before opening or hashing; no resolved private path enters public bytes.

| claimed recipe fact | owning v4 artifact and field | required independent check |
| --- | --- | --- |
| v4 contract identity | exact contract path and bytes above | reject a reparse point or non-ordinary file and recompute the exact contract SHA-256 |
| handoff identity and lineage | exact handoff filename; `schema_version`, `contract_id`, `contract_path`, and `contract_sha256` | reject duplicate or unknown keys, recompute the file SHA-256 and canonical self-digest, and require equality with the exact v4 contract binding |
| inventory identity and lineage | exact inventory filename; `schema_version`, `contract_id`, `contract_path`, and `contract_sha256` | reject duplicate or unknown keys, recompute the file SHA-256 and canonical root digest, and require 51 rows and 6,136,931 total bytes |
| build command observations | handoff `validation_rows` keyed by `command_id` | require one `managed_build` row before one `native_bootstrap_build` row; both are `passed`, exit zero, with respective passed counts four and one and all other counts zero |
| build scripts | inventory `files` rows | require ordinary relative rows `scripts/build.ps1`, `scripts/build-native-bootstrap.ps1`, and `src/build-activation-host.ps1`; recompute row membership, lengths 7,831, 15,483, and 2,078 bytes, and the exact three SHA-256 values below |
| trusted archive digest | handoff and inventory `trusted_go_archive_sha256` | require both independently parsed values to equal each other and the exact digest below; the symbolic identity and byte size remain owner-bound contract facts, not values derived from these v4 artifacts |
| input and output inventory | inventory canonical root and `files` rows | recompute the root, source/output counts, and exact five generated output basenames; v4 output bytes and digests are not reusable v5 outputs |

The v4 handoff and inventory prove only that the two named command observations
passed and that the listed components were present. They do not contain the
executable identities, ordered argument descriptors, or environment-name set,
so `historical_v4_command_tuple_verified` is permanently `false` for this
contract. Codex B did not inspect package source, scripts, logs, command history,
or raw command output to reconstruct those values. The literals below are a new
owner-selected v5 design. They are not observed v4 history, and component
continuity must not be promoted into a command-equivalence claim.

The proposed recipe object has exactly the following JSON schema and values;
unknown keys are forbidden. `recipe_status=complete` means only that this
contract contains a closed recipe definition. It does not mean independently
accepted, executable, authorized, compatible, successful, or reusable.

```json
{
  "build_recipe_ref": "mythic_edge_role_pool_v5_build_recipe.v1",
  "build_recipe_sha256": "4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3",
  "cleanup_rules": [
    "remove_private_archive_extraction_tree",
    "remove_build_temporary_files_inside_exact_candidate_staging_root",
    "freeze_review_root_before_candidate_staging_cleanup",
    "remove_exact_candidate_staging_root_after_review_root_freeze",
    "retain_no_raw_command_output",
    "retain_no_private_path",
    "require_zero_generated_residue_outside_exact_review_root"
  ],
  "command_rows": [
    {
      "argument_descriptors": [
        {"literal": "-NoLogo"},
        {"literal": "-NoProfile"},
        {"literal": "-NonInteractive"},
        {"literal": "-ExecutionPolicy"},
        {"literal": "Bypass"},
        {"literal": "-File"},
        {"candidate_relative_path": "scripts/build.ps1"}
      ],
      "command_id": "managed_build",
      "executable_identity": "windows_powershell_5_1_system32_x64.v1",
      "expected_error_count": 0,
      "expected_exit_code": 0,
      "expected_failed_count": 0,
      "expected_passed_count": 4,
      "expected_skipped_count": 0,
      "precommand_checks": [
        "require_candidate_working_directory_identity",
        "require_exact_script_row_sha256",
        "require_closed_environment_name_set",
        "require_no_network_and_no_installation"
      ],
      "script_rows": [
        {"path": "scripts/build.ps1", "sha256": "5238274174a21eb83a3ff09b7ee0c87adb5d9db345c0a5a02065ad48c041a3c3"}
      ],
      "working_directory_kind": "candidate_package_root"
    },
    {
      "argument_descriptors": [
        {"literal": "-NoLogo"},
        {"literal": "-NoProfile"},
        {"literal": "-NonInteractive"},
        {"literal": "-ExecutionPolicy"},
        {"literal": "Bypass"},
        {"literal": "-File"},
        {"candidate_relative_path": "scripts/build-native-bootstrap.ps1"},
        {"private_value_ref": "trusted_go_archive_private_path"},
        {"literal": "3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345"}
      ],
      "command_id": "native_bootstrap_build",
      "executable_identity": "windows_powershell_5_1_system32_x64.v1",
      "expected_error_count": 0,
      "expected_exit_code": 0,
      "expected_failed_count": 0,
      "expected_passed_count": 1,
      "expected_skipped_count": 0,
      "precommand_checks": [
        "require_candidate_working_directory_identity",
        "require_exact_script_row_sha256",
        "require_trusted_archive_ordinary_non_reparse_file",
        "require_trusted_archive_sha256_match",
        "require_trusted_archive_size_match",
        "require_closed_environment_name_set",
        "require_no_network_and_no_installation"
      ],
      "script_rows": [
        {"path": "scripts/build-native-bootstrap.ps1", "sha256": "e75fda45f9e4070b7b7d651799a986bfd0da3a1b03f467ee2ae5f48b9e9c59cd"},
        {"path": "src/build-activation-host.ps1", "sha256": "7ade15110bfccaef19fb0cdcfa49ae2e8a4733614cb096e2aab693f2fe2f65ba"}
      ],
      "working_directory_kind": "candidate_package_root"
    }
  ],
  "environment_value_rules": [
    {"name": "SystemRoot", "value_source": "validated_windows_system_root_private"},
    {"name": "TEMP", "value_source": "exact_candidate_staging_temp_root_private"},
    {"name": "TMP", "value_source": "exact_candidate_staging_temp_root_private"}
  ],
  "exact_v4_archive_reused": true,
  "exact_v4_build_scripts_reused": true,
  "executable_profiles": [
    {
      "architecture": "x64",
      "identity": "windows_powershell_5_1_system32_x64.v1",
      "private_resolved_path_serialized": false,
      "required_file_kind": "ordinary_non_reparse",
      "required_product_name": "Windows PowerShell",
      "required_version": "5.1",
      "resolution_rule": "system_root_system32_windows_powershell_v1_0_powershell_exe"
    }
  ],
  "historical_v4_command_tuple_verified": false,
  "input_binding": {
    "copied_source_row_count": 46,
    "excluded_generated_output_row_count": 5,
    "input_row_root_digest": "bc2240e7ceea848404becc18914d41e78699ee0aee1316c0619bd7a12e423994",
    "input_row_root_kind": "v4_inventory_root_digest",
    "inventory_row_count": 51
  },
  "output_basenames": [
    "MythicEdgeRolePoolIsolationBroker.exe",
    "MythicEdgeRolePoolVerifierActivationHost.exe",
    "MythicEdgeRolePoolVerifierBootstrap.exe",
    "MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe",
    "MythicEdgeRolePoolVerifierService.exe"
  ],
  "permitted_environment_variable_names": [
    "SystemRoot",
    "TEMP",
    "TMP"
  ],
  "recipe_schema": "mythic_edge_role_pool_v5_build_recipe.v1",
  "recipe_status": "complete",
  "source_evidence": {
    "component_provenance_status": "verified_v4_component_metadata_only",
    "v4_command_observations": [
      {"command_id": "managed_build", "error_count": 0, "exit_code": 0, "failed_count": 0, "passed_count": 4, "skipped_count": 0, "status": "passed"},
      {"command_id": "native_bootstrap_build", "error_count": 0, "exit_code": 0, "failed_count": 0, "passed_count": 1, "skipped_count": 0, "status": "passed"}
    ],
    "v4_contract_file_sha256": "628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487",
    "v4_contract_id": "mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1",
    "v4_contract_path": "references/external-isolation-broker-v4-corrective-successor.md",
    "v4_generated_output_row_count": 5,
    "v4_handoff_file_sha256": "adbe95cf2b37c666dcbc72fe295e50464fb20140e63053b107e58772f7af10c5",
    "v4_handoff_filename": "MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4.implementation-handoff.v4.json",
    "v4_handoff_root_digest": "e8941e8dd92d4bf9ff581b335f639420fd493c7ac724f50c142e843b7350dc51",
    "v4_handoff_schema": "mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v4",
    "v4_handoff_status": "candidate_ready_for_independent_review",
    "v4_inventory_file_count": 51,
    "v4_inventory_file_sha256": "a805429be56e60fa9f29a7f3562d8a11b5a5966e9177f33f15f81e3f1c8bc298",
    "v4_inventory_filename": "package-inventory.json",
    "v4_inventory_root_digest": "bc2240e7ceea848404becc18914d41e78699ee0aee1316c0619bd7a12e423994",
    "v4_inventory_schema": "mythic_edge_role_pool_windows_broker_verifier_package_inventory.v4",
    "v4_inventory_total_length_bytes": 6136931,
    "v4_source_row_count": 46,
    "v4_trusted_go_archive_sha256_from_handoff": "3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345",
    "v4_trusted_go_archive_sha256_from_inventory": "3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345"
  },
  "trusted_toolchain": {
    "identity": "trusted_go_archive_v1",
    "private_path_serialized": false,
    "private_path_source": "owner_activation_only",
    "sha256": "3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345",
    "size_bytes": 74910419
  },
  "v5_recipe_selection": "owner_selected_from_verified_v4_components"
}
```

The executable identity resolves only to the 64-bit Windows PowerShell 5.1
host at the validated private `SystemRoot` System32 location. Resolution must
reject absence, ambiguity, reparse points, non-ordinary files, product/version
drift, architecture drift, shell aliases, `PATH` lookup, `pwsh`, and fallback.
`-ExecutionPolicy Bypass` applies only to each noninteractive child process and
only after all listed script digests match; it changes no persistent policy.

Each argument descriptor is exactly one of
`{"literal":"<exact public-safe argument>"}`,
`{"candidate_relative_path":"<exact recipe-owned path>"}`, or
`{"private_value_ref":"trusted_go_archive_private_path"}`. For
`native_bootstrap_build`, the two descriptors after the script path are the
owner-selected positional script arguments: the private archive path first and
the fixed expected archive SHA-256 second. Archive size is a mandatory
precommand check, not a script argument. This interface choice is a proposed v5
design and carries no claim that v4 used it or that the unchanged script accepts
it; later candidate execution must fail closed on any incompatibility.

The private descriptor is the only permitted representation of the archive
path. Its value comes only from a later exact owner activation and is never
serialized, logged, echoed, retained, hashed into a public object, or accepted
from another source. Environment names are exact, sorted, and unique. Their
values are set explicitly from the named private sources, are not inherited as
ambient defaults, and never enter public output. `TEMP` and `TMP` resolve to the
same exact attempt-created directory inside the disposable candidate staging
root. No other variable, credential-like name, value, or ambient environment is
permitted.

Canonical serialization is strict JSON encoded as UTF-8 without BOM, with
duplicate and unknown keys rejected, keys sorted by Unicode code point, arrays
in the contracted order, no insignificant whitespace, and one final LF.
`build_recipe_sha256` is lowercase SHA-256 over those canonical bytes with only
`build_recipe_sha256` omitted. The fixed recipe reference and digest are
comparison-only activation inputs and must be recomputed from the independently
reviewed object during activation-bound preflight.

### Independent build-recipe review receipt

Codex E's recipe decision is representable only as
`mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1`. The
receipt is a public-safe canonical JSON object returned inline in the workflow
handoff. It follows the accepted Stage-3 `transcript_only` pattern: no separate
receipt file is claimed, no new manifest path is added, and the later existing
manifest-rebind amendment must reproduce and bind the accepted object and
digest exactly before it can become a durable activation input.

The receipt has exactly these keys and no others:

```text
review_receipt_schema=mythic_edge_role_pool_v5_build_recipe_independent_review_receipt.v1
review_receipt_kind=build_recipe_contract_review
review_ref
reviewed_contract_id=mythic_edge_role_pool_external_isolation_broker_v5_corrective_successor.v1
reviewed_contract_path=references/external-isolation-broker-v5-corrective-successor.md
reviewed_contract_sha256
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_ref=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
recipe_definition_verdict
contract_review_verdict
build_recipe_independent_review_status
finding_ids
reviewer_role=codex_e_independent_reviewer
reviewed_at_utc
historical_v4_command_tuple_verified=false
build_recipe_execution_compatibility_claimed=false
receipt_storage=transcript_only
separate_review_receipt_file_claimed=false
next_role
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
implementation_authorized=false
manifest_rebind_authorized=false
package_creation_authorized=false
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
receipt_digest
```

`recipe_definition_verdict` is exactly `conformant` or `nonconformant`.
`contract_review_verdict` is exactly `accepted` or `revision_required`.
`build_recipe_independent_review_status` is exactly
`accepted_exact_recipe_and_contract` or `revision_required`. `finding_ids` is a
sorted, duplicate-free array of public-safe E finding IDs. The cross-field rows
are closed:

| Recipe verdict | Contract verdict | Finding IDs | Receipt status | Next role |
| --- | --- | --- | --- | --- |
| `conformant` | `accepted` | empty | `accepted_exact_recipe_and_contract` | `owner_manifest_rebind_decision` |
| `conformant` | `revision_required` | nonempty | `revision_required` | `codex_b_contract_revision` |
| `nonconformant` | `revision_required` | nonempty | `revision_required` | `codex_b_contract_revision` |

Every other tuple rejects. In particular, `nonconformant` plus `accepted`, an
accepted contract with findings, an empty finding array on revision, a true
authority or claim field, or a readiness-bearing next role is invalid.

The receipt uses the recipe's strict UTF-8 canonical JSON rules. First omit
both `review_ref` and `receipt_digest`, hash the canonical bytes, and set:

```text
review_ref="build_recipe_review_v1_" + first_32_lowercase_hex(sha256)
```

Then insert `review_ref` and set `receipt_digest` to lowercase SHA-256 over the
canonical object with only `receipt_digest` omitted. In every downstream packet,
`build_recipe_independent_review_ref=review_ref` and
`build_recipe_independent_review_sha256=receipt_digest`. A consumer must
recompute both values from the full receipt; shape validation, a copied digest,
or a handoff summary is insufficient.

`reviewed_at_utc` is RFC 3339 UTC at whole-second precision with literal `Z`.
The reviewer must recompute the contract and recipe digests from the reviewed
bytes. E must emit the complete receipt object without editing the contract.
Missing, malformed, stale, cross-contract, cross-recipe, contradictory,
correctly shaped but incorrect, or noncanonical receipt data fails closed.

Receipt projection is exact. A valid
`accepted_exact_recipe_and_contract` receipt derives
`contract_review_status=accepted_semantics_manifest_pending`,
`contract_semantics_accepted=true`, `manifest_integration_complete=false`,
`manifest_rebind_recommended_now=true`, `contract_acceptance_ready=false`, and
`ready_for_codex_c=false`. A valid `revision_required` receipt derives
`contract_review_status=revision_required`,
`contract_semantics_accepted=false`, `manifest_rebind_recommended_now=false`,
and routes only to Codex B. No caller may choose or override these projections.

The prior E handoff is evidence of a conformant recipe definition, but it is not
retroactively promoted into an accepted receipt because the reviewed contract
did not define this schema and this revision changes its digest:

```text
prior_reviewed_contract_sha256=bc71af53310f593587010c5d3a85757a67251bac61ef4e109640a2f56399fb89
prior_recomputed_build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
prior_recipe_definition_verdict=conformant
prior_review_finding_id=EIB-PKG-V5-REVIEW-E-001
prior_review_receipt_status=not_created_contract_schema_missing
```

A later independent review produced one accepted receipt for the immediately
preceding contract bytes. It is durable lineage, not authority for this revised
contract:

```text
prior_build_recipe_independent_review_ref=build_recipe_review_v1_5dd95cd9042f9ba5be885675f8fab52d
prior_build_recipe_independent_review_sha256=9e074c23202ecdb0f0f7d1ff8ef7c391d5e555e14897620793d84b53af3ec6ab
prior_build_recipe_reviewed_contract_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
prior_build_recipe_review_status=accepted_exact_recipe_and_pre_revision_contract
```

The current revised-contract recipe lifecycle is therefore closed:

```text
build_recipe_definition_status=complete_owner_selected
build_recipe_independent_review_status=pending_re_review_of_revised_contract
build_recipe_independent_review_ref=none
build_recipe_independent_review_sha256=none
historical_v4_command_tuple_verified=false
exact_v4_archive_reused=true
exact_v4_build_scripts_reused=true
v5_recipe_selection=owner_selected_from_verified_v4_components
build_recipe_ref=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
build_recipe_execution_compatibility_claimed=false
manifest_rebind_recommended_now=false
candidate_preparation_activation_eligible=false
```

A future candidate-preparation owner activation must bind the exact recipe
schema, fixed reference, recomputed digest, complete status, all three v4
evidence digests, trusted archive identity/digest/size, input-row root, command
rows, environment-name set, outputs, cleanup rules, expiry, and single-use
lifecycle. Any missing, stale, malformed, reordered, substituted, cross-version,
cross-attempt, private-path-bearing, correctly shaped but incorrect, or
unreviewed value blocks before activation consumption or candidate-root
creation. A prior activation cannot float to the revised contract or recipe.

Focused contract validation must reject every one-field mutation, wrong command
order, extra or missing command, script or script digest drift, argument
reordering, literal/private descriptor substitution, private path or environment
value serialization, unknown environment name, archive identity/digest/size
drift, input-root drift, output reorder/addition/removal, nonzero expected exit,
wrong result count, weakened cleanup, digest mismatch, discovery, fallback, and
unknown field. It must reject any attempt to relabel the unverified historical
tuple as verified, to replace an exact reused component, or to treat the
owner-selected recipe as accepted without an exact independent-review receipt.
Absent that receipt, no activation, candidate root, build, output, inventory, or
handoff may exist.

The manifest lifecycle state is closed and current for the contract bytes that
immediately precede this revision:

```text
manifest_file_count=37
manifest_transition_36_to_37_status=implemented_and_preserved
manifest_transition_37_to_37_0b3_to_d8ef_status=implemented_and_valid
manifest_transition_37_to_37_d8ef_to_85ba_status=implemented_and_valid
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_bound_v5_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_bound_v5_digest_status=valid_for_immediately_preceding_contract_bytes
current_revised_contract_manifest_status=stale_digest_mismatch
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=current_revised_contract_sha256_after_independent_acceptance
manifest_rebind_status=blocked_new_owner_decision_required
manifest_rebind_authorized=false
```

The completed 36-to-37 transition and completed 37-to-37 rebinds from
`0b3cc179303ddba6ece29492414b7bb942f25cc5d59d317f6c6857c93375a1ea`
to `d8ef00274def0c8b2e76b366e8fe08a075809372178504eeafaafac502d64967`
and then to
`85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704`
are historical current-state evidence and must not be rerun, rolled back, or
described as pending. The 37-file validator is valid and correctly rejects
these revised contract bytes because its exact `85ba...` v5 digest pin is now
stale. It must not adopt new bytes or a digest dynamically. A later rebind
changes only that exact v5 digest pin; the expected count remains 37 and every
path set, v3/v4 binding, completed-transition rule, and negative check remains
unchanged. Only after Codex E accepts the atomic-consumption mechanism and the
then-exact contract digest may a separate owner decision authorize an
independently reviewed manifest-rebind amendment. That amendment must bind the
accepted contract digest, unchanged recipe digest, and exact independent-review
reference and SHA-256 before any candidate-preparation activation. This contract
does not authorize the amendment or its implementation.

### Stable-count contract review and manifest integration

Contract semantics and manifest integration are separate deterministic facts.
A declared, exact manifest transition may remain pending without forcing Codex
E to label an otherwise conformant contract `revision_required`. It still blocks
Codex C, Codex D, Codex F, package work, execution, and activation until the
manifest work is separately authorized, implemented, validated, and reviewed.
This is a refinement of the existing review and manifest lanes, not a new
authority, approval, claim, lifecycle, retention, or source-action family.

The closed review vocabulary is:

```text
review_pending
accepted_semantics_manifest_pending
accepted_manifest_current
revision_required
```

| Observed state | Contract review status | Contract semantics accepted | Manifest integration complete | Next route |
| --- | --- | --- | --- | --- |
| Semantic review incomplete | `review_pending` | `false` | derived independently | Codex E |
| Semantics conformant; only the exact declared path/digest/count transition is pending | `accepted_semantics_manifest_pending` | `true` | `false` | owner manifest-integration decision |
| Semantics conformant; exact reviewed manifest transition is current and clean | `accepted_manifest_current` | `true` | `true` | next separately authorized workflow role |
| Contract ambiguity, contradiction, unclosed schema, undeclared effect, or any non-manifest semantic finding | `revision_required` | `false` | derived independently | Codex B |

An expected manifest mismatch qualifies for the second row only when its target
path, predecessor digest or absence, candidate digest, count effect, and sole
error cause all equal the declared transition. An extra path, wrong count,
unexpected digest, additional validation cause, dynamic adoption, wildcard,
fallback, or altered legacy row is not an expected pending transition and fails
closed. Semantic acceptance never makes the candidate manifest-current.

For future contract work, count effects are classified mechanically:

| Candidate relationship to accepted manifest | Count transition | Required review handling |
| --- | --- | --- |
| New path not yet accepted | exactly `X_to_X_plus_1`, once, after E accepts the final candidate bytes | keep candidate detached from the installed skill and manifest during B/E review |
| Existing accepted path with revised bytes | exactly `X_to_X`; digest rebind only | keep accepted installed bytes and pin unchanged during B/E review |
| Exact accepted path and digest unchanged | none | no manifest amendment |
| Missing, duplicate, renamed, case-varied, extra, or ambiguous path relationship | invalid | fail closed and route to Codex B |

`X_to_X_plus_1` describes only the one-time addition of a newly accepted path.
Subsequent revisions of that path must never be described as another count
transition. Before integration, a candidate lives only in a disposable review
root outside the installed skill, is unavailable to runtime, is excluded from
manifest counts, and is bound by target path, predecessor status, candidate
SHA-256, contract review receipt, and expiry. No private absolute review-root
path enters public output.

After E returns an accepted semantic-review receipt, one later exact owner
activation may authorize a separately reviewed promotion transaction. That
future transaction may copy only the accepted candidate bytes to the exact
target and update only the owning manifest digest pin and focused expected test
value. A new path may additionally change the count once. An existing path may
not change the count. The future promotion envelope would consist only of the
accepted target bytes plus the two existing manifest implementation paths:

```text
references/external-isolation-broker-v5-corrective-successor.md
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

The target row is copy-only: no implementation actor may edit accepted contract
content during promotion. Predecessor drift, candidate drift, receipt drift,
partial staging, failed focused validation, failed full validation, or crash
leaves integration incomplete and blocks adoption. No second accepted digest,
floating pin, multiple-current state, or automatic rollback/adoption is
permitted. Defining this model does not authorize its tooling, promotion
envelope, owner activation, or use in the current rebind.

The present v5 state predates this detached-review practice and remains an exact
37-to-37 stale-digest rebind. It may be semantically accepted by E under the
closed second row, but the installed manifest remains invalid until a separate
current rebind is accepted and implemented. Therefore, for this thread:

```text
stable_count_review_model_status=contract_defined_not_implemented
stable_count_review_model_authorized=false
current_manifest_count_transition=37_to_37
current_manifest_digest_rebind_required=true
manifest_rebind_recommended_now=false
contract_semantics_accepted=false
manifest_integration_complete=false
contract_acceptance_ready=false
ready_for_codex_c=false
```

The four finite validation universes are exact Cartesian products or an exact
ordered total oracle:

- timestamp-floor: the inherited 3-by-4-by-5 universe, 60 expected, two
  accepted, and 58 rejected tuples;
- failure: 2 operation paths, 20 error codes, 8 phases, 3 external statuses,
  3 inventory statuses, 6 terminal statuses, and 2 source-copy statuses,
  producing 34,560 expected, 20 accepted, and 34,540 rejected tuples; and
- binding/projection: 5 operation/result categories, 3 inventory statuses,
  2 binding-presence states, 3 staging observations including not-applicable,
  and 2 digest sources, producing 180 expected, 5 accepted, and 175 rejected
  tuples; and
- atomic observation: 3 prevalidation results, 4 invocation results, 4 source
  states, 4 destination states, and 4 readback results, producing 768 expected
  and classified tuples with exact outcome counts 1, 1, 45, 4, and 717.

The validator must enumerate each universe, prove exhaustiveness and unique
selection, compare the exact expected/accepted/rejected or outcome counts, and
reject a duplicate, unclassified, or multiply selected tuple. It must not
sample or infer closure.

Focused negative tests must independently cover missing, malformed, stale,
contradictory, cross-attempt, cross-contract, cross-package, and correctly
shaped but incorrect values for every binding family. They must also cover one
field-at-a-time mutation, wrong owning artifact, digest recomputation mismatch,
duplicate rows, reordered rows, unknown fields, and fallback attempts.

`future_activation_requirements_sha256` is recomputed over the canonical closed
field-name and derivation list in the final-seal section below. The contract,
current manifest rebind and accepted rebind amendment, implementation/test
scope, exact matrix counts, build recipe, and future activation requirements
therefore form one digest-bound review packet. Packet validation grants no
implementation, publication, or seal authority.

`candidate_revision_digest` is SHA-256 over a canonical object containing every
packet field except `candidate_lifecycle_status`, `candidate_revision_digest`,
and `packet_sha256`. Lifecycle labels therefore cannot relabel candidate bytes,
while source, tests, recipe, contract, manifest amendment, scope, matrix, prior
revision, or finding drift necessarily changes candidate identity.

## Source-copy and edit envelope

A later separately activated v5 attempt begins only from an absent v5 root. It
validates the exact v4 inventory binding above and copies its 46 source rows,
excluding these five generated outputs:

```text
dist/MythicEdgeRolePoolIsolationBroker.exe
dist/MythicEdgeRolePoolVerifierActivationHost.exe
dist/MythicEdgeRolePoolVerifierBootstrap.exe
dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe
dist/MythicEdgeRolePoolVerifierService.exe
```

Copy order remains ordinal by relative path. Each destination is exclusively
created, reread, and hash-compared before any edit. The exact future edit
envelope is:

```text
tools/publish_implementation_candidate.py
tests/test_implementation_handoff.py
```

The implementation file may change only for the private binding, reordered
publication, binding-driven serialization, and fail-closed revalidation in
this contract. The test file may change only for the required focused tests.
The other 44 source rows must remain exact-byte copies of v4. No third source
or test path, renamed path, removed path, broad cleanup, dependency, protocol
change, Role Pool edit, or source-repository read is allowed. If implementation
proves a third path necessary, stop and route to Codex B.

All five executables and the inventory must be rebuilt as fresh v5 outputs; no
v4 generated output may be copied. This statement defines future scope only
and grants no build or copy authority.

## Consumed candidate-attempt and inherited-build reconciliation

This section is the normative current-state reconciliation for the first v5
candidate-preparation attempt. It supersedes earlier current-state projections
in this document only where they describe recipe execution compatibility,
candidate-attempt lifecycle, manifest freshness, or next-role routing. It does
not alter the canonical recipe object, the accepted recipe-review receipt, the
atomic-consumption mechanism, the two-path implementation envelope, or any
package or runtime authority.

The exact public-safe attempt projection is:

```text
candidate_preparation_activation_ref=owner_activation_v1_598bcbcb457ac51a2e51612e3ef98f26
candidate_preparation_activation_status=consumed_for_candidate_workflow
candidate_preparation_activation_reuse_authorized=false
candidate_source_status=exact_46_rows_2_authorized_changes
focused_validation_status=passed_24_plus_18_plus_19_and_windows_share_denial
closed_recipe_managed_build_status=blocked_last_exit_code_unset_after_first_compiler_invocation
ambient_managed_build_status=non_authoritative_verifier_service_self_test_failed
broader_suite_status=blocked_two_execution_policy_failures_two_skips
candidate_revision_frozen=false
candidate_review_root_created=false
candidate_inventory_created=false
candidate_generated_residue_count=0
candidate_lifecycle_status=returned_to_codex_b
build_recipe_v1_definition_status=accepted_exact_definition
build_recipe_v1_execution_compatibility_status=blocked_observed
build_environment_root_cause=unknown
```

The closed-recipe result is the first proven failure point. It proves that the
v1 recipe and inherited build behavior did not complete together under the
contracted closed environment. It does not prove whether the cause is missing
executable resolution, an omitted environment dependency, incorrect process-
result handling inside an inherited script, or another bounded build-interface
dependency. No one may infer or select one of those causes from the unset
`LASTEXITCODE` observation alone.

The ambient run is a non-authoritative diagnostic signal. It used an environment
outside the canonical recipe and therefore cannot prove recipe compatibility,
candidate validity, or the cause of the verifier-service self-test failure. It
must not be substituted for the closed run or used to authorize a source edit.
The broader-suite policy failures and skips also remain unresolved validation
signals; they are not waived, relabelled as passes, or merged with the first
closed-recipe failure.

The accepted `mythic_edge_role_pool_v5_build_recipe.v1` object and digest remain
immutable historical contract evidence. Its independent review established that
the definition was closed and correctly bound; it did not establish execution
compatibility. Recipe v1 is retired from future candidate execution and may not
be retried, repaired in place, or rebound to a fresh activation. The consumed
activation and its cleaned, unfrozen attempt are non-reusable. No Codex D cycle
exists because no candidate revision or independent candidate-review receipt was
created.

### Required build-dependency characterization before a retry

A later explicit owner authorization may permit one read-only characterization
of only these exact v4 inventory rows, after their existing path, digest,
ordinary-file, no-reparse, owner, and inventory-root bindings pass:

```text
scripts/build.ps1
scripts/build-native-bootstrap.ps1
src/build-activation-host.ps1
```

That characterization is not authorized by this revision. It may not build,
execute a script, inspect another source row, read generated v4 output, use a
network, mutate a package, or retain source text. Its public-safe result must be
transcript-only and limited to symbolic command IDs, invocation kinds, resolver
kinds, required environment-variable names without values, process-result
producer/consumer kinds, self-test command IDs, exact input-row digests, and
closed `complete`, `degraded`, or `blocked` status. Source snippets, command
text, argument values, private paths, executable locations, raw output,
exceptions, and inferred fixes are forbidden.

The characterization must distinguish these possibilities without choosing by
guesswork:

| Characterized condition | Required route |
| --- | --- |
| every invoked tool already has an exact non-ambient resolver and the inherited script consumes a native-process result correctly | Codex B may define a complete recipe v2 using those exact resolver bindings |
| a required tool or environment dependency is ambient, unresolved, or only discoverable through `PATH` | Codex B must define an exact private symbolic resolver and integrity profile; a generic or ambient `PATH` remains forbidden |
| an inherited script reads process-result state that its preceding invocation cannot produce | route to Codex B for a separately reviewed edit-envelope expansion naming the exact script row; do not patch or preseed `LASTEXITCODE` |
| the evidence is missing, contradictory, degraded, or requires another row | remain blocked and return to Codex B or the owner without source expansion |

Any executable identity added later must be versioned, integrity-bound, resolved
without ambient search, and represented publicly only by a symbolic private
reference plus approved metadata. Initializing `LASTEXITCODE` to a success value,
adding an ambient `PATH`, suppressing a self-test, accepting skips, or treating
command-not-found behavior as a compiler result is forbidden.

A future executable recipe must be
`mythic_edge_role_pool_v5_build_recipe.v2`; it must receive a new digest and an
independent Codex E receipt. Any future candidate-preparation packet must use a
new versioned activation profile that binds recipe v2 and the accepted
characterization. Neither schema is defined or authorized here. If a script
edit is proven necessary, the candidate edit envelope, operation matrix, static
preflight, manifest binding, and activation profile must all be revised and
reviewed together before a fresh owner activation. Until then no fresh
candidate activation is eligible.

After a closed recipe v2 build exists, the verifier-service self-test must be
rerun only inside that accepted environment. If the same symbolic self-test
failure recurs, it becomes a new concrete implementation finding and routes to
Codex D only if its exact correction fits a then-approved edit envelope;
otherwise it returns to Codex B. The ambient result alone authorizes no fix.

### Failed characterization attempt and revised execution envelope

This section supersedes the preceding characterization execution details where
they concern partial reads, parser isolation, result shape, source-buffer
release, activation version, or current lifecycle. The exact prior attempt is
closed public-safe evidence:

```text
characterization_activation_ref=owner_characterization_activation_v2_0b0dab1b1a0e42df8d738265b57dbe42
characterization_activation_status=spent_failed_after_source_open
characterization_activation_reuse_authorized=false
three_row_binding_verdict=passed
source_access_occurred=true
source_rows_opened=1
additional_rows_opened=0
overall_status=blocked
failure_code=characterization_incomplete
characterization_rows_emitted=0
no_echo_projection=passed
durable_artifacts_created=0
generated_residue_count=0
source_buffer_disposal_certified=false
package_mutation_performed=false
```

The attempt grants no characterization evidence because it emitted no rows. Its
activation and the one-row partial read are non-reusable. The absence of a
source-buffer disposal certification is not evidence of retention, but the
prior envelope did not define an honest, mechanically checkable memory-lifetime
boundary. Physical erasure of immutable managed strings cannot be certified and
must never be claimed.

The revised parser profile is
`mythic_edge_role_pool_v5_powershell_ast_characterizer.v3`. Its exact host is
the existing symbolic executable profile
`windows_powershell_5_1_system32_x64.v1`. The parent resolves that profile only
as the 64-bit Windows PowerShell executable beneath the validated private
`SystemRoot` System32 location. Before launch it must prove an ordinary,
non-reparse file; `PSEdition=Desktop`; PowerShell major/minor version `5.1`;
64-bit process architecture; and the same fixed product, resolver, and
no-fallback checks already defined by the immutable recipe component. The
private resolved path, file metadata, and environment values never enter an
argument, result, diagnostic, or public hash.

The host argument vector is exactly, in order:

```text
-NoLogo
-NoProfile
-NonInteractive
-Command
-
```

No alias, `pwsh`, 32-bit host, extra switch, profile, module import, ambient
`PATH` lookup, encoded-command substitution, or fallback is valid. Standard
input contains only the future implementation of this contract's deterministic
algorithm; the implementation receives no authority from this docs-only
revision and must be independently reviewed against the synthetic matrix before
any real-source activation. The three private source paths may reach the child
only through the exact process-only environment names
`ME_ROLE_POOL_CHARACTERIZATION_ROW_1`,
`ME_ROLE_POOL_CHARACTERIZATION_ROW_2`, and
`ME_ROLE_POOL_CHARACTERIZATION_ROW_3`. Their values are never serialized or
echoed and are removed with process exit.

The child uses only the host's own
`System.Management.Automation.Language.Parser` type and the exact
`ParseInput(string, Token[] by-ref, ParseError[] by-ref)` overload. It may not
load a module, assembly, package, profile, or parser service. Tokens and parse
errors are ephemeral analysis inputs and are never output. The parent supplies
a 30-second wall-clock deadline. On expiry it requests termination once, waits
at most five additional seconds for confirmed exit, and makes no second parser
attempt. Unknown termination or output-capture state projects to cleanup
unknown.

This is a dedicated, short-lived, local parser process. It must not dot-source,
invoke, import, compile, build, test, or execute any source row. It receives no
network, repository, package-mutation, external-write, or child-process
authority. The child process may emit only the canonical child-result envelope
defined below on standard output. The controller consumes that envelope and
alone may emit the canonical public-safe result. Standard error, parser
diagnostics, source text, token text, command text, paths, and exceptions must
not be emitted by either process.

Before that process starts, the parent must validate the exact contract,
manifest, handoff, inventory, inventory root, three row paths, three lengths,
three digests, ordinary-file and no-reparse state, volume, owner, and read-only
scope without opening source content. Any failure blocks before process start.

Inside the dedicated process, source handling is exact:

1. open the three rows in contracted order with read-only handles that deny
   write and delete sharing;
2. after each open, revalidate ordinary-file, no-reparse, length, identity, and
   SHA-256 before parsing;
3. read no fourth row and make no partial public projection;
4. decode exact bytes as strict UTF-8 with an optional leading UTF-8 BOM and no
   replacement characters;
5. parse all three rows before emitting any characterization row;
6. treat any decoder or parser diagnostic as a closed blocked result without
   diagnostic text;
7. build the complete symbolic result in memory only after all three inputs and
   all observations validate;
8. clear mutable byte and character buffers where available, drop all source,
   token, AST, and diagnostic references, emit only canonical result bytes, and
   exit; and
9. require the parent to confirm process exit, zero durable artifacts, zero
   generated residue, and no raw output before accepting the result.

Process exit is the source-lifetime boundary. The result must set
`source_buffer_erasure_claimed=false`; complete or degraded status instead
requires `source_lifetime_boundary=dedicated_process_exit_no_durable_output`
and `dedicated_process_exit_status=confirmed`. An unknown process exit,
durable residue, or no-echo uncertainty is blocked. No retry, process reuse,
cache, temp source file, memory dump, parser server, or retained AST is allowed.

The only public result schema is
`mythic_edge_role_pool_v5_build_dependency_characterization_result.v3`. Draft
v1 is rejected and cannot be upgraded. V2 is also rejected because it did not
close the child-analysis versus parent-confirmed-exit boundary. V3 is a strict
canonical JSON object
with exactly these 20 root keys and no others:

```text
schema
contract_sha256
activation_ref
activation_status
parser_profile
source_bindings
source_rows_opened
additional_rows_opened
characterization_rows
overall_status
failure_code
no_echo_projection
durable_artifacts_created
durable_artifact_status
generated_residue_count
generated_residue_status
source_lifetime_boundary
source_buffer_erasure_claimed
dedicated_process_exit_status
result_sha256
```

`source_bindings` is the exact ordered three-row array below and may not be
caller-selected or reconstructed from source text:

```json
[
  {"length_bytes":7831,"path":"scripts/build.ps1","row_ordinal":1,"sha256":"5238274174a21eb83a3ff09b7ee0c87adb5d9db345c0a5a02065ad48c041a3c3"},
  {"length_bytes":15483,"path":"scripts/build-native-bootstrap.ps1","row_ordinal":2,"sha256":"e75fda45f9e4070b7b7d651799a986bfd0da3a1b03f467ee2ae5f48b9e9c59cd"},
  {"length_bytes":2078,"path":"src/build-activation-host.ps1","row_ordinal":3,"sha256":"7ade15110bfccaef19fb0cdcfa49ae2e8a4733614cb096e2aab693f2fe2f65ba"}
]
```

Each `characterization_rows` member has exactly:

```text
source_row_ordinal
source_order_ordinal
symbolic_command_id
invocation_kind
resolver_kind
required_environment_variable_names
process_result_producer_kind
process_result_consumer_kind
self_test_command_ids
```

Rows are sorted by `source_row_ordinal`, then `source_order_ordinal` ascending.
`symbolic_command_id` is exactly
`row_<source_row_ordinal>_invocation_<three_digit_source_order_ordinal>` and
self-test IDs use the same rule with `self_test` in place of `invocation`.
Environment names are sorted, unique strings without values. The closed
observation vocabularies are defined here and may not be supplied or widened by
an activation:

```text
invocation_kind:
  native_process_literal
  powershell_script_literal
  powershell_command_literal
  managed_api_literal
  dynamic_or_unknown

resolver_kind:
  managed_type_literal
  script_relative_literal
  ambient_name_lookup
  dynamic_or_unknown

process_result_producer_kind:
  native_exit_code
  powershell_success_state
  managed_return_value
  none
  conditional_or_unknown

process_result_consumer_kind:
  last_exit_code
  powershell_success_state
  managed_return_value
  none
  conditional_or_unknown
```

The literal resolver values classify only AST shape; they do not prove runtime
resolution and must not contain or imply a public path, executable location, or
private value. `ambient_name_lookup` is an observation of a bare lexical name
and never authorizes ambient resolution. Profile v3 performs no variable-value,
alias, command-discovery, type-resolution, or control-flow inference. A value
requiring any such inference is `dynamic_or_unknown`, making the result
degraded rather than guessed.

AST-to-row derivation is exact:

1. Parse each source row independently with the exact overload above. Any
   `ParseError` count greater than zero is `parse_failed`; token contents and
   diagnostics are discarded without projection.
2. Invocation candidates are every `CommandAst` and
   `InvokeMemberExpressionAst`. A managed member nested inside a `CommandAst`
   is its own candidate only when its `(StartOffset, EndOffset)` differs from
   the enclosing command. Exact duplicate `(node kind, StartOffset, EndOffset)`
   candidates collapse to one.
3. Sort candidates by `Extent.StartOffset`, then `Extent.EndOffset`, then node
   kind with `CommandAst` before `InvokeMemberExpressionAst`. Assign
   `source_order_ordinal` starting at one independently for each source row.
4. `InvokeMemberExpressionAst` with literal type and member names is
   `managed_api_literal` plus `managed_type_literal`; otherwise both fields are
   their unknown literal.
5. For `CommandAst`, call `GetCommandName()` once. Null, empty, variable,
   expression, splatted, or invocation-operator-only command names are unknown.
   A case-insensitive literal ending `.exe` or `.com` is
   `native_process_literal`. A literal ending `.ps1` or rooted lexically in
   `./`, `.\\`, or `$PSScriptRoot` is `powershell_script_literal`. A bare
   literal matching `^[A-Za-z][A-Za-z0-9]*-[A-Za-z][A-Za-z0-9]*$` is
   `powershell_command_literal`. Every other command is unknown.
6. A literal command containing no slash or backslash uses
   `ambient_name_lookup`; a script literal rooted in `./`, `.\\`, or
   `$PSScriptRoot` uses `script_relative_literal`; all variable-computed,
   absolute, provider-qualified, URI-shaped, or otherwise unresolved forms are
   unknown. A managed literal uses `managed_type_literal`.
7. `required_environment_variable_names` is the sorted, duplicate-free,
   uppercase set of `VariableExpressionAst.VariablePath.UserPath` values in the
   candidate subtree that begin case-insensitively with `env:` after removing
   that prefix. Invalid names make the row invalid.
8. Producer kind derives only from invocation kind: native literal produces
   `native_exit_code`; PowerShell command or script literal produces
   `powershell_success_state`; managed literal produces
   `managed_return_value`; unknown produces `conditional_or_unknown`.
9. The consumer window is the remainder of the candidate's direct statement
   plus the immediately following sibling statement in the nearest
   `StatementBlockAst`, stopping before the next invocation candidate at that
   scope. A `$LASTEXITCODE` read gives `last_exit_code`; otherwise a `$?` read
   gives `powershell_success_state`; otherwise a direct simple-variable
   assignment of the invocation whose variable is read in that window gives
   `managed_return_value`; otherwise it is `none`. More than one matching rule,
   dynamic scope, or ambiguous ownership gives `conditional_or_unknown`.
10. A candidate is a self-test only when one of its literal
    `StringConstantExpressionAst` arguments equals, using invariant
    case-insensitive comparison, `--self-test`, `-selftest`, `self-test`, or
    `selftest`. Its array then contains exactly its corresponding
    `row_<row>_self_test_<ordinal>` ID; otherwise the array is empty.

Every row field is a string except the two positive integer ordinals and the
two sorted, duplicate-free string arrays
`required_environment_variable_names` and `self_test_command_ids`. Every
environment name must match `[A-Z][A-Z0-9_]{0,63}`. A row with an empty or
unknown field outside the closed unknown literals is invalid, not degraded.

The root field types are also closed. `schema`, `contract_sha256`,
`activation_ref`, `activation_status`, `parser_profile`, `overall_status`,
`failure_code`, `no_echo_projection`, `source_lifetime_boundary`,
`dedicated_process_exit_status`, and `result_sha256` are strings.
`source_bindings` and `characterization_rows` are arrays. `source_rows_opened`,
`additional_rows_opened`, `durable_artifacts_created`, and
`generated_residue_count` are either nonnegative JSON integers or JSON `null`;
booleans are not integers. For the source counters, null is required when the
controller cannot validate a complete child-result envelope, including a child
crash, missing output, malformed output, or child self-digest failure. For the
artifact and residue counters, null is required exactly when process, capture,
or cleanup state is unknown. Null is forbidden otherwise.
`durable_artifact_status` and
`generated_residue_status` are strings. `source_buffer_erasure_claimed` is the
JSON boolean `false` only. A known `source_rows_opened` may be only 0 through 3.
`additional_rows_opened` must be zero for complete or degraded output; any
positive value is blocked with `failure_code=additional_row_required` and an
empty result-row array.

The closed root vocabularies are:

```text
activation_status:
  rejected_before_process_start_unconsumed_non_reusable
  spent_complete
  spent_degraded
  spent_blocked
  spent_cleanup_unknown

overall_status:
  complete
  degraded
  blocked

failure_code:
  none
  binding_failed_before_source_open
  activation_reuse_or_concurrency_detected
  process_start_failed
  source_open_failed
  source_digest_mismatch
  decode_failed
  parse_failed
  analysis_incomplete
  additional_row_required
  no_echo_projection_failed
  durable_residue_detected
  cleanup_state_unknown

no_echo_projection:
  passed
  failed
  unknown

durable_artifact_status:
  zero
  nonzero
  unknown

generated_residue_status:
  zero
  nonzero
  unknown

source_lifetime_boundary:
  source_not_opened
  dedicated_process_exit_no_durable_output
  unconfirmed

dedicated_process_exit_status:
  not_started
  confirmed
  unknown
```

Known count/status pairs are exact: integer zero pairs only with `zero`, an
integer greater than zero pairs only with `nonzero`, and JSON `null` pairs only
with `unknown`. Any other pair is invalid. The parent, not the child, performs
the final lifecycle projection after process-state and output-capture checks.

The lifecycle derivation order is closed:

1. A binding, expiry, reuse, concurrency, or host check that fails before a
   process-start call emits `overall_status=blocked`, empty rows, known zero
   counts and statuses, `source_lifetime_boundary=source_not_opened`,
   `dedicated_process_exit_status=not_started`, passed no-echo, and
   `activation_status=rejected_before_process_start_unconsumed_non_reusable`.
   The failure code is respectively `binding_failed_before_source_open` or
   `activation_reuse_or_concurrency_detected`. The reference is permanently
   non-reusable even though no atomic move or source open occurred.
2. A process-start call that returns a definite failure with no child created
   uses the same projection with `failure_code=process_start_failed`.
3. An unknown start outcome, unknown exit, unknown output capture, or unknown
   artifact/residue cleanup emits null unknown counts, unknown statuses,
   `source_lifetime_boundary=unconfirmed`,
   `dedicated_process_exit_status=unknown`, `no_echo_projection=unknown`,
   empty rows, `overall_status=blocked`,
   `failure_code=cleanup_state_unknown`, and
   `activation_status=spent_cleanup_unknown`. The activation is conservatively
   spent and non-reusable.
4. After confirmed process start and exit with known zero artifact and residue
   state, `complete` requires three opened rows, zero additional rows, no
   unknown observation literal, nonempty valid characterization rows,
   `failure_code=none`, passed no-echo, the dedicated-process lifetime literal,
   and false erasure claim. Its activation status is `spent_complete`.
5. `degraded` has the same requirements but contains at least one permitted
   unknown observation literal and no invalid row. Its activation status is
   `spent_degraded`.
6. Every other confirmed-cleanup started outcome is `blocked` with empty rows
   and `activation_status=spent_blocked`.

When more than one known failure condition applies, exactly one public
`failure_code` is selected by this highest-first priority list:

```text
cleanup_state_unknown
durable_residue_detected
no_echo_projection_failed
additional_row_required
source_digest_mismatch
source_open_failed
decode_failed
parse_failed
analysis_incomplete
process_start_failed
activation_reuse_or_concurrency_detected
binding_failed_before_source_open
```

`cleanup_state_unknown` always controls when any required state is unknown.
Otherwise known nonzero residue controls no-echo or analysis failures, and
failed no-echo controls source/analysis failures. A confirmed 30-second timeout
whose child then exits and leaves known zero residue is
`analysis_incomplete`; unknown termination is `cleanup_state_unknown`.

Canonical serialization is strict sorted-key, compact, ASCII JSON encoded as
UTF-8 without BOM plus one final LF. `result_sha256` is lowercase SHA-256 over
those canonical bytes with only `result_sha256` omitted. Duplicate, unknown,
missing, reordered array, alternate-type, stale, cross-attempt, shape-valid but
incorrect, or self-digest-mismatched input fails closed.

The preconsumption pass for
`owner_characterization_activation_v4_ef639662d32f47b5afb41c20b4a25516`
validated its 54-field packet, then proved that its reviewed program exposed
only a single-row synthetic entrypoint. No process started, no source row
opened, no package was accessed, and no generated residue remained. The
activation is nevertheless
`rejected_before_process_start_unconsumed_non_reusable`; it cannot be retried,
reissued, consumed, or used as evidence that the three-row capability exists.
Its v1 review receipt remains valid only for the exact synthetic program and
matrix that Codex E reviewed.

Any future real-source attempt requires the exact 64-field private activation
schema
`mythic_edge_role_pool_v5_build_dependency_characterization_activation.v5`.
Its keys are exactly:

```text
schema
activation_ref
approval_source_sha256
activation_status
issued_at_utc
expires_at_utc
single_use
reuse_authorized
contract_id
contract_path
contract_sha256
manifest_amendment_path
manifest_amendment_sha256
manifest_file_count
manifest_sha256
manifest_v5_path
manifest_v5_sha256
static_preflight_schema
static_preflight_sha256
controller_profile
parser_profile
child_result_schema
result_schema
characterizer_bundle_schema
characterizer_bundle_sha256
characterizer_controller_program_sha256
characterizer_child_program_sha256
characterizer_controller_entrypoint
characterizer_child_entrypoint
characterizer_complete_result_entrypoint
characterizer_core_synthetic_matrix_schema
characterizer_core_synthetic_matrix_sha256
characterizer_adapter_synthetic_matrix_schema
characterizer_adapter_synthetic_matrix_sha256
characterizer_synthetic_review_schema
characterizer_synthetic_review_ref
characterizer_synthetic_review_sha256
characterizer_synthetic_review_status
source_bindings
source_bindings_sha256
source_row_count
transcript_only_output
dedicated_parser_process_authorized
read_exact_three_source_rows_authorized
powershell_ast_parse_authorized
source_script_execution_authorized
build_authorized
package_mutation_authorized
durable_artifact_creation_authorized
network_access_authorized
source_repository_access_authorized
external_write_authorized
package_creation_authorized
inventory_creation_authorized
publication_authorized
installation_authorized
service_mutation_authorized
canary_authorized
stage_advancement_authorized
live_ready
correctness_claimed
security_assurance_claimed
privacy_assurance_claimed
activation_sha256
```

`activation_ref` matches
`^owner_characterization_activation_v5_[0-9a-f]{32}$`.
`activation_status=approved_unconsumed`, `single_use=true`,
`reuse_authorized=false`, `manifest_file_count=37`,
`source_row_count=3`, `transcript_only_output=true`,
`dedicated_parser_process_authorized=true`,
`read_exact_three_source_rows_authorized=true`, and
`powershell_ast_parse_authorized=true`. Every authority or claim field from
`source_script_execution_authorized` through `privacy_assurance_claimed` is
`false`. The contract, manifest-amendment, manifest, and static-preflight
digests must be recomputed from then-current owning artifacts after the
manifest rebind is independently accepted. `manifest_v5_path` is exactly this
contract path and `manifest_v5_sha256=contract_sha256`.

The interface bindings are exact:

```text
controller_profile=mythic_edge_role_pool_v5_characterization_controller.v1
parser_profile=mythic_edge_role_pool_v5_powershell_ast_characterizer.v3
child_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_child_result.v1
result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_result.v3
characterizer_bundle_schema=mythic_edge_role_pool_v5_characterization_program_bundle.v2
characterizer_controller_entrypoint=Invoke-MythicEdgeV5CharacterizationController
characterizer_child_entrypoint=Invoke-MythicEdgeV5ThreeRowSourceAdapter
characterizer_complete_result_entrypoint=Complete-MythicEdgeV5CharacterizationResult
characterizer_core_synthetic_matrix_schema=mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1
characterizer_core_synthetic_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
characterizer_adapter_synthetic_matrix_schema=mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2
characterizer_adapter_synthetic_matrix_sha256=2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7
characterizer_synthetic_review_schema=mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3
characterizer_synthetic_review_status=accepted_exact_bundle_and_matrices
```

The two program SHA-256 values are recomputed independently from the exact
reviewed ASCII, UTF-8-without-BOM, LF-only controller and child bytes.
`characterizer_bundle_sha256` is recomputed from the exact 18-field bundle
object defined below; it is not a caller digest or a digest of concatenated
program bytes.
`characterizer_synthetic_review_ref` matches
`^characterization_bundle_review_v3_[0-9a-f]{32}$`; its SHA-256 is recomputed
from the canonical v3 review receipt defined below. Missing or merely
shape-valid program, bundle, matrix, entrypoint, or review values fail before
source open.

`source_bindings` is the exact three-row array above.
`source_bindings_sha256` is SHA-256
`7e04ef6a2a869585bac9fc1790fbbf463b3721e8a08a5a273579c7c48599e116`
over its compact, sorted-key, ASCII JSON bytes plus one LF. The controller,
parser, child-result, and public-result fields are the exact versions in this
section. Any earlier controller absence, parser profile, result schema,
activation schema, or single-program receipt is a cross-version failure.
`static_preflight_schema` is
`mythic_edge_role_pool_v5_static_contract_preflight.v1`.
`issued_at_utc` and `expires_at_utc` are RFC 3339 UTC whole-second strings;
expiry must be later than issue time and no more than 24 hours later.
`approval_source_sha256` is comparison-only evidence derived from exact private
owner-approval bytes and grants no path field or public echo.

Canonical activation serialization is sorted-key, compact, ASCII JSON encoded
as UTF-8 without BOM plus one LF. `activation_sha256` is lowercase SHA-256 over
those bytes with only `activation_sha256` omitted. Missing, extra, duplicate,
renamed, differently typed, stale, cross-attempt, expired, shape-valid but
incorrect, alternate-preimage, or self-digest-mismatched values fail before
source open. The activation is private transport, not retained evidence.

That activation is not created or authorized by this revision. It is spent on
dedicated-process start whether the result is complete, degraded, or blocked;
no same-activation retry is permitted. Only one owner-named Codex C thread may
start the process. A second or concurrent start, unknown start state, reused
reference, or inability to project the spent status fails before source open.
The activation bytes are removed after the terminal result without weakening
the transcript's permanent non-reuse decision.

### Controller, child adapter, and complete-result boundary

The future capability consists of exactly two independently hashed PowerShell
programs in one disposable implementation-review root:

```text
characterization-controller.v1.ps1
characterization-child.v3.ps1
```

Those basenames are review identities, not installed paths or package rows.
Neither file may be added to the installed skill, package inventory, source
repository, manifest, or durable evidence by this contract. A separately
authorized Codex C implementation pass may create only those two disposable
files. A program change requires a new digest, complete synthetic rerun, and
new independent review receipt.

The controller program exposes exactly:

```text
Invoke-MythicEdgeV5CharacterizationController
Complete-MythicEdgeV5CharacterizationResult
```

The controller executes in the same exact Windows PowerShell 5.1 host profile
as the child. Its argument vector is exactly `-NoLogo`, `-NoProfile`,
`-NonInteractive`, `-File`, then the validated private controller-program path.
The path must be an ordinary non-reparse file whose bytes match the reviewed
controller digest; it is never output. No alias, ambient lookup, extra switch,
encoded command, profile, module, or fallback is permitted.

Standard input to the controller is one private in-memory request with schema
`mythic_edge_role_pool_v5_characterization_controller_request.v1` and exactly
these 10 keys:

```text
schema
activation_ref
activation_sha256
contract_sha256
child_program_path
child_program_sha256
source_bindings
source_bindings_sha256
private_source_paths
request_sha256
```

`private_source_paths` is an ordered three-row array whose members have exactly
`row_ordinal` and `path`; ordinals are the integers 1, 2, and 3 in that order.
The request is sorted-key compact JSON, UTF-8 without BOM, plus one LF, and
`request_sha256` omits only itself. It is created only after the external
preconsumption validator accepts the complete v5 activation. It is never
written to disk, retained, hashed into public evidence, or echoed. Missing,
extra, duplicate, reordered, cross-attempt, stale, alternate-preimage, wrong-
digest, or wrong-path-count input fails before controller invocation.

The controller's top-level body reads exactly one request and invokes
`Invoke-MythicEdgeV5CharacterizationController` exactly once. The entrypoint
recomputes the request self-digest; compares its contract, source-binding,
child-program, and activation-reference fields to the exact already validated
invocation projection; validates the child bytes and host; and then starts the
child. It does not independently validate the private activation, expiry,
approval source, or non-reuse state because those values are not in its
request. The external preconsumption validator retains sole ownership of those
checks and may create the request only from one complete accepted activation.
The controller supplies the three private paths only through the three
environment names already defined, launches the exact child host and argument
vector above, sends only the reviewed child-program bytes to child standard
input, captures bounded child standard output and standard error, removes the
three environment values after child exit, and performs no source open itself.

The child program exposes exactly
`Invoke-MythicEdgeV5ThreeRowSourceAdapter`. Its top-level body invokes that
entrypoint exactly once. It accepts no command-line parameter, pipeline input,
caller object, fourth path, mode switch, or fallback. It resolves the three
process-only environment values, opens and validates the exact three source
rows in ordinal order, applies the AST-to-row derivation above to each row,
buffers every observation until all three rows terminate, and emits exactly
one child-result envelope. Its private row analyzer may be exercised by the
synthetic harness but is not a separately callable real-source authority.

The child-result schema is
`mythic_edge_role_pool_v5_build_dependency_characterization_child_result.v1`
with exactly these 13 keys:

```text
schema
contract_sha256
parser_profile
source_bindings
source_bindings_sha256
source_rows_opened
additional_rows_opened
characterization_rows
analysis_status
failure_code
no_echo_projection
source_buffer_erasure_claimed
child_result_sha256
```

`analysis_status` is exactly `complete`, `degraded`, or `blocked`.
`failure_code` is exactly `none`, `source_open_failed`,
`source_digest_mismatch`, `decode_failed`, `parse_failed`,
`analysis_incomplete`, `additional_row_required`, or
`no_echo_projection_failed`. Complete or degraded requires three opened rows,
zero additional rows, valid nonempty characterization rows, passed no-echo,
and `failure_code=none`. Blocked requires an empty characterization-row array.
The child never claims process exit, cleanup, artifact state, residue state, or
activation consumption. `source_buffer_erasure_claimed` remains JSON `false`.
Canonical serialization and the self-digest rule match the public result, with
only `child_result_sha256` omitted from its preimage.

The child stops at the first failed row operation and opens no later row. Its
known `source_rows_opened` is therefore 0 through 3 and includes the row whose
handle was opened before a digest, decode, or parse failure. It is zero when
row 1 cannot be opened. `additional_rows_opened` is always zero in a conforming
real run; a positive injected synthetic value is blocked as
`additional_row_required` and represents a forbidden-scope attempt.
`no_echo_projection` is exactly `passed` or `failed`. When more than one
known child failure is injected synthetically, the exact priority is
`no_echo_projection_failed`, `additional_row_required`,
`source_digest_mismatch`, `source_open_failed`, `decode_failed`, `parse_failed`,
then `analysis_incomplete`. The exact source-binding array, row schema, row
ordering, unknown-literal rule, and contract digest are inherited unchanged
from the public-result rules. Any incoherent status, count, row, failure, or
no-echo combination makes the child envelope invalid; the controller projects
that invalidity as `analysis_incomplete` rather than trusting a child claim.

After confirmed child exit, the controller validates the complete child
envelope before calling `Complete-MythicEdgeV5CharacterizationResult`. The
complete-result entrypoint accepts only the validated activation's public-safe
projection, either one validated child envelope or one closed symbolic child
failure, and the controller-owned process, output-capture, artifact, residue,
and no-echo observations. It accepts no path, source byte, source text, token,
AST node, diagnostic text, exception, or environment value. It alone creates
the 20-key public v3 result and derives final lifecycle status. A missing,
malformed, partial, extra-key, wrong-schema, cross-contract, wrong-binding, or
self-digest-mismatched child envelope projects to `analysis_incomplete`, empty
public rows, and null source counters unless a higher-priority failure applies.
No child field can assert confirmed exit or override controller observations.

The controller emits no candidate, partial row, child envelope, diagnostic, or
progress output. It emits one canonical public v3 result only after complete
finalization. Nonempty or unbounded standard error, extra standard-output
bytes, output truncation, uncertain capture, unknown child exit, or uncertain
cleanup fails closed under the existing priority order. No controller or child
process may build, invoke a source script, spawn a descendant, use the network,
write a file, retain a cache, or mutate package state.

The external launcher accepts that public result only after the controller
process itself exits with code zero, its bounded standard error is empty, its
bounded standard output is exactly one canonical v3 result, and controller-
owned cleanup is known complete with zero residue. A controller start failure,
unknown exit, nonzero exit, output overflow, malformed or extra output, nonempty
standard error, or unknown cleanup accepts no result and leaves the activation
permanently non-reusable. These outer acceptance checks do not alter the child-
exit fields inside an accepted public result and grant no retry.

The outer launcher may project only one transcript-only handoff with schema
`mythic_edge_role_pool_v5_build_dependency_characterization_attempt_handoff.v1`
and exactly these 27 keys:

```text
schema
contract_sha256
activation_ref
activation_status
activation_reuse_authorized
controller_profile
controller_program_sha256
controller_start_status
controller_exit_status
controller_stdout_status
controller_stderr_status
controller_cleanup_status
result_acceptance_status
accepted_result_sha256
accepted_result_overall_status
accepted_result_failure_code
handoff_status
outer_failure_code
no_echo_projection
source_rows_opened
additional_rows_opened
source_access_status
package_access_status
generated_residue_count
handoff_storage
live_ready
handoff_sha256
```

The closed observation vocabularies are:

```text
controller_start_status:
  not_invoked
  failed
  started
  unknown

controller_exit_status:
  not_applicable
  zero
  nonzero
  unknown

controller_stdout_status:
  not_applicable
  one_canonical_result
  empty
  malformed
  extra_or_overflow
  unknown

controller_stderr_status:
  not_applicable
  empty
  nonempty_or_overflow
  unknown

controller_cleanup_status:
  not_applicable
  zero
  nonzero
  unknown

result_acceptance_status:
  not_accepted
  accepted

handoff_status:
  blocked_before_controller_start
  blocked_after_controller_start
  accepted_complete
  accepted_degraded
  accepted_blocked
  cleanup_state_unknown

outer_failure_code:
  none
  binding_failed_before_controller_start
  controller_start_failed
  controller_exit_nonzero
  controller_stdout_empty
  controller_stdout_malformed
  controller_stdout_extra_or_overflow
  controller_stderr_nonempty_or_overflow
  controller_residue_detected
  accepted_result_cross_field_mismatch
  controller_state_unknown

source_access_status:
  not_opened
  approved_rows_opened
  scope_violation_detected
  unknown

package_access_status:
  not_accessed
  approved_rows_accessed_read_only
  scope_violation_detected
  unknown
```

`activation_status` uses the public-result activation vocabulary.
`accepted_result_overall_status` and `accepted_result_failure_code` are either
the exact copied public-result literals or `not_applicable` when no result is
accepted. `accepted_result_sha256` is either the recomputed lowercase digest of
the exact accepted result or `none`. `no_echo_projection` is exactly `passed`,
`failed`, or `unknown`. The two row counters and
`generated_residue_count` are nonnegative JSON integers or JSON `null`, never
booleans. `activation_reuse_authorized=false`,
`handoff_storage=transcript_only`, and `live_ready=false` are invariant.

The five identity fields are exact bindings, not caller assertions. `schema`
is the literal handoff schema above. `contract_sha256` is recomputed from this
contract's then-current ordinary bytes. `activation_ref` is the one syntactically
valid `^owner_characterization_activation_v5_[0-9a-f]{32}$` reference under
evaluation. `controller_profile` is exactly
`mythic_edge_role_pool_v5_characterization_controller.v1`.
`controller_program_sha256` is recomputed from the exact controller bytes bound
by the independently accepted program bundle and review receipt. All five must
agree with the activation, bundle, and receipt before process invocation. A
missing, stale, cross-attempt, shape-only, caller-supplied, or contradictory
identity is the known pre-start binding refusal below; it cannot be reclassified
as a controller failure or accepted result.

The outer observations are also closed. Before a start call, exit, stdout,
stderr, and cleanup are `not_applicable`. A definite failed start uses `failed`;
a created controller uses `started`; any inability to distinguish those states
uses `unknown`. A known process exit maps only to `zero` or `nonzero`. Captured
stdout maps to `empty` for zero bytes, `one_canonical_result` only for one exact
canonical public-result byte sequence, `malformed` for one bounded noncanonical
sequence, and `extra_or_overflow` for multiple sequences or a reached/exceeded
capture bound. Captured stderr maps to `empty` for zero bytes and
`nonempty_or_overflow` for any byte or a reached/exceeded bound. Cleanup maps to
`zero` only after the controller-owned cleanup check proves zero residue and to
`nonzero` only for a known positive residue count. An unobserved, interrupted,
or contradictory exit, capture, or cleanup state maps to `unknown`; no ambient
success state, caller label, or partial byte sequence may fill the observation.

The derivation is exact. A known binding refusal before invocation uses
`not_invoked`, all other controller observations `not_applicable`, zero source,
additional-row, and residue counts, no access, passed no-echo,
`blocked_before_controller_start`, and
`binding_failed_before_controller_start`. A definite controller start failure
uses the same projection with `controller_start_status=failed` and
`outer_failure_code=controller_start_failed`. Both use
`activation_status=rejected_before_process_start_unconsumed_non_reusable`.

If controller start, exit, output capture, standard-error capture, or cleanup is
unknown, or if an observation tuple is contradictory or outside the closed
derivations, the handoff is `cleanup_state_unknown` with
`outer_failure_code=controller_state_unknown`,
`activation_status=spent_cleanup_unknown`, no accepted result, null counters,
unknown access, and `no_echo_projection=unknown`. For a known started attempt
that rejects a result, the handoff is `blocked_after_controller_start`, the
activation is `spent_blocked`, result fields are not applicable, and source
counts and access are unknown because unaccepted output cannot supply evidence.
Known nonzero residue retains its exact positive count; otherwise that blocked
projection has zero residue. `no_echo_projection=failed` exactly for
`controller_stdout_malformed`, `controller_stdout_extra_or_overflow`, or
`controller_stderr_nonempty_or_overflow`; it is `passed` for every other known
blocked-after-start code. The handoff itself never contains captured bytes,
diagnostic text, exception text, source text, arguments, or paths.

A result is accepted only for the single conjunction `started`, exit `zero`,
stdout `one_canonical_result`, stderr `empty`, cleanup `zero`, exact canonical
result and self-digest, and coherent copied cross-fields. The handoff is then
`accepted_complete`, `accepted_degraded`, or `accepted_blocked` according to
the copied public status, `outer_failure_code=none`, passed no-echo, and zero
residue. Activation status, accepted-result failure code, and source counters
are copied exactly. Zero opened rows gives `not_opened` and `not_accessed`;
one through three opened rows with zero additional rows gives
`approved_rows_opened` and `approved_rows_accessed_read_only`; a positive
additional-row count gives both scope-violation literals; null source counts
give both `unknown` literals.

When multiple known outer failures are injected, exactly one code is selected
by this highest-first order:

```text
controller_state_unknown
controller_residue_detected
controller_stderr_nonempty_or_overflow
controller_stdout_extra_or_overflow
controller_stdout_malformed
controller_stdout_empty
controller_exit_nonzero
accepted_result_cross_field_mismatch
controller_start_failed
binding_failed_before_controller_start
none
```

The handoff uses strict sorted-key compact ASCII JSON, UTF-8 without BOM, and
one final LF. `handoff_sha256` is SHA-256 over those bytes with only itself
omitted. Missing, extra, duplicate, reordered, differently typed, stale,
cross-attempt, alternate-preimage, contradictory, or self-digest-mismatched
values fail closed to the state-unknown projection without echoing captured
bytes. The handoff is not written as a file, retained result, claim, lifecycle
record, package artifact, or source-action authority.

The program-bundle object has schema
`mythic_edge_role_pool_v5_characterization_program_bundle.v2`. V1 is rejected
because it did not bind the outer handoff. V2 has exactly these 18 keys:

```text
schema
contract_sha256
controller_profile
controller_program_sha256
controller_entrypoint
complete_result_entrypoint
parser_profile
child_program_sha256
child_entrypoint
child_result_schema
public_result_schema
attempt_handoff_schema
core_matrix_schema
core_matrix_sha256
adapter_matrix_schema
adapter_matrix_sha256
source_bindings_sha256
bundle_sha256
```

It uses sorted-key compact ASCII JSON, UTF-8 without BOM, plus one LF.
`bundle_sha256` omits only itself. Every digest is recomputed from its owning
bytes; caller-supplied, concatenated, shape-only, or alternate-preimage digests
are invalid. No bundle or program digest exists for authority purposes until
Codex E accepts the exact future implementation bytes and matrices.

### Core synthetic matrix and historical receipt

No future bundle review may pass until both exact programs preserve this core
matrix and also pass the adapter matrix below. The core matrix schema is
`mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1`. Its canonical
preimage is the following single compact, sorted-key, ASCII JSON line plus one
LF:

```json
{"case_count":36,"category_counts":{"ast":14,"host":6,"lifecycle":16},"rows":[["H01","exact_host","preflight_pass"],["H02","host_missing","rejected_before_process_start_unconsumed_non_reusable|blocked|binding_failed_before_source_open|source_not_opened|not_started"],["H03","host_reparse","rejected_before_process_start_unconsumed_non_reusable|blocked|binding_failed_before_source_open|source_not_opened|not_started"],["H04","host_wrong_edition_version_or_architecture","rejected_before_process_start_unconsumed_non_reusable|blocked|binding_failed_before_source_open|source_not_opened|not_started"],["H05","host_alias_fallback_or_extra_argument","rejected_before_process_start_unconsumed_non_reusable|blocked|binding_failed_before_source_open|source_not_opened|not_started"],["H06","host_start_outcome_unknown","spent_cleanup_unknown|blocked|cleanup_state_unknown|unconfirmed|unknown"],["A01","tool.exe --version\\n","native_process_literal|ambient_name_lookup|native_exit_code|none|env=[]|self=[]"],["A02",".\\\\tool.ps1 -Mode Build\\n","powershell_script_literal|script_relative_literal|powershell_success_state|none|env=[]|self=[]"],["A03","Get-Thing\\n","powershell_command_literal|ambient_name_lookup|powershell_success_state|none|env=[]|self=[]"],["A04","[System.IO.File]::Exists($x)\\n","managed_api_literal|managed_type_literal|managed_return_value|none|env=[]|self=[]"],["A05","& $tool\\n","dynamic_or_unknown|dynamic_or_unknown|conditional_or_unknown|none|env=[]|self=[]"],["A06","tool.exe $env:TEMP $env:SystemRoot\\n","native_process_literal|ambient_name_lookup|native_exit_code|none|env=[SYSTEMROOT,TEMP]|self=[]"],["A07","tool.exe --self-test\\n","native_process_literal|ambient_name_lookup|native_exit_code|none|env=[]|self=[row_1_self_test_001]"],["A08","tool.exe; Get-Thing\\n","ids=[row_1_invocation_001,row_1_invocation_002]|ordered_by_extent"],["A09","tool.exe; if ($LASTEXITCODE -ne 0) { throw 'synthetic' }\\n","native_process_literal|last_exit_code"],["A10","Get-Thing; if (-not $?) { throw 'synthetic' }\\n","powershell_command_literal|powershell_success_state"],["A11","$r = [System.IO.File]::Exists($x); if ($r) { $null = 1 }\\n","managed_api_literal|managed_return_value"],["A12","if (\\n","spent_blocked|blocked|parse_failed|rows=[]"],["A13","hex:fffe00","spent_blocked|blocked|decode_failed|rows=[]"],["A14","tool.exe 'C:\\\\synthetic-private\\\\fixture'\\n","argument_and_path_absent_from_output|no_echo_projection=passed"],["L01","prestart_binding_failed","rejected_before_process_start_unconsumed_non_reusable|blocked|binding_failed_before_source_open|counts=0|statuses=zero"],["L02","reuse_or_concurrent_start","rejected_before_process_start_unconsumed_non_reusable|blocked|activation_reuse_or_concurrency_detected|counts=0|statuses=zero"],["L03","definite_process_start_failure","rejected_before_process_start_unconsumed_non_reusable|blocked|process_start_failed|counts=0|statuses=zero"],["L04","unknown_process_start","spent_cleanup_unknown|blocked|cleanup_state_unknown|counts=null|statuses=unknown"],["L05","three_rows_complete","spent_complete|complete|none|counts=known_zero_cleanup|erasure_claimed=false"],["L06","three_rows_with_permitted_unknown","spent_degraded|degraded|none|counts=known_zero_cleanup|erasure_claimed=false"],["L07","source_open_failure","spent_blocked|blocked|source_open_failed|rows=[]"],["L08","source_digest_mismatch","spent_blocked|blocked|source_digest_mismatch|rows=[]"],["L09","strict_utf8_decode_failure","spent_blocked|blocked|decode_failed|rows=[]"],["L10","parser_error","spent_blocked|blocked|parse_failed|rows=[]"],["L11","analysis_incomplete","spent_blocked|blocked|analysis_incomplete|rows=[]"],["L12","additional_row_opened","spent_blocked|blocked|additional_row_required|rows=[]"],["L13","no_echo_and_parse_fail","spent_blocked|blocked|no_echo_projection_failed|priority_over=parse_failed"],["L14","residue_and_no_echo_fail","spent_blocked|blocked|durable_residue_detected|priority_over=no_echo_projection_failed"],["L15","cleanup_unknown_and_residue","spent_cleanup_unknown|blocked|cleanup_state_unknown|priority_over=durable_residue_detected"],["L16","timeout_with_confirmed_exit_zero_residue","spent_blocked|blocked|analysis_incomplete|dedicated_process_exit_no_durable_output|confirmed"]],"schema":"mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1"}
```

Its SHA-256 is exactly
`9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526`.
In `A01` through `A12` and `A14`, `\\n` denotes one LF in invented UTF-8
fixture bytes; `A13` denotes exactly the three bytes `ff fe 00`. Host rows use
synthetic metadata/start adapters, AST rows use only those invented bytes, and
lifecycle rows inject only the named symbolic states. The test harness must
run exactly 36 cases, report 36 passed and zero failed, execute no source row,
emit no fixture text or diagnostics, and leave zero residue. Every closed host,
row, status, failure, unknown, no-echo, timeout, priority, and non-erasure rule
above appears in at least one case. Missing, extra, reordered, renamed,
differently typed, skipped, expected-failure, alternate-fixture, or digest-
mismatched cases fail review.

The exact previously reviewed single-row program and matrix produced only a
transcript receipt with
schema
`mythic_edge_role_pool_v5_characterization_synthetic_review_receipt.v1` and
exactly these 16 keys:

```text
schema
review_ref
contract_sha256
parser_profile
result_schema
characterizer_program_sha256
synthetic_matrix_schema
synthetic_matrix_sha256
case_count
passed_count
failed_count
no_echo_status
source_access_occurred
program_execution_scope
verdict
review_sha256
```

`review_ref` matches `^characterization_review_v1_[0-9a-f]{32}$`;
`case_count=36`, `passed_count=36`, `failed_count=0`,
`no_echo_status=passed`, `source_access_occurred=false`,
`program_execution_scope=synthetic_only`, and
`verdict=accepted_exact_program_and_matrix`. The receipt binds its historical
contract digest, parser profile v2, result schema v2, exact program digest, and
matrix digest. It uses sorted-key compact ASCII JSON, UTF-8 without BOM, plus
one LF; `review_sha256` omits only itself from its preimage. The accepted
historical receipt is bound exactly as follows:

```text
review_ref=characterization_review_v1_59295fc8186f44d0b2225958fb9092d6
contract_sha256=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
characterizer_program_sha256=16f92be872c0d2423356ff0e317ae94b12d4d7f8d254079a013f442b36a60124
synthetic_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
review_sha256=15c65235a21e68f09aed48f0d9c9679bf835ba71852700ec232dae3998637c78
verdict=accepted_exact_program_and_matrix
capability_scope=single_row_synthetic_only
real_source_adapter_reviewed=false
complete_result_entrypoint_reviewed=false
```

Those values remain valid historical synthetic evidence. The receipt grants no
source read or execution authority, does not satisfy the v3 bundle receipt, and
must not appear in a v5 activation as its current review binding.

### Adapter and complete-result synthetic matrix

The additional matrix schema is
`mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2`. V1 is
rejected because it did not close outer-launcher failures. The v2 canonical
preimage is this single compact, sorted-key, ASCII JSON line plus one LF:

```json
{"case_count":37,"category_counts":{"binding":2,"child":10,"controller":7,"determinism":1,"outer_launcher":17},"rows":[["I01","three_valid_rows_no_unknowns","child_complete|public_complete|spent_complete|rows_nonempty"],["I02","three_valid_rows_with_permitted_unknown","child_degraded|public_degraded|spent_degraded|rows_nonempty"],["I03","row_1_open_failed","child_blocked|public_blocked|source_open_failed|source_rows_opened=0"],["I04","row_2_open_failed","child_blocked|public_blocked|source_open_failed|source_rows_opened=1"],["I05","row_3_open_failed","child_blocked|public_blocked|source_open_failed|source_rows_opened=2"],["I06","row_1_digest_mismatch","child_blocked|public_blocked|source_digest_mismatch|source_rows_opened=1"],["I07","row_2_digest_mismatch","child_blocked|public_blocked|source_digest_mismatch|source_rows_opened=2"],["I08","row_3_digest_mismatch","child_blocked|public_blocked|source_digest_mismatch|source_rows_opened=3"],["I09","strict_decode_failed","child_blocked|public_blocked|decode_failed|rows=[]"],["I10","ast_parse_failed","child_blocked|public_blocked|parse_failed|rows=[]"],["I11","additional_or_missing_source_binding","process_not_started|public_blocked|binding_failed_before_source_open|source_rows_opened=0"],["I12","malformed_or_missing_child_envelope","confirmed_exit|public_blocked|analysis_incomplete|source_rows_opened=null"],["I13","child_self_digest_mismatch","confirmed_exit|public_blocked|analysis_incomplete|source_rows_opened=null"],["I14","partial_or_status_incoherent_child_rows","confirmed_exit|public_blocked|analysis_incomplete|rows=[]"],["I15","nonempty_or_uncaptured_child_stderr","public_blocked|no_echo_projection_failed|rows=[]"],["I16","timeout_confirmed_exit_zero_residue","public_blocked|analysis_incomplete|dedicated_process_exit_status=confirmed"],["I17","timeout_or_start_with_unknown_cleanup","public_blocked|cleanup_state_unknown|dedicated_process_exit_status=unknown"],["I18","definite_process_start_failure","process_not_started|public_blocked|process_start_failed|source_rows_opened=0"],["I19","stale_cross_attempt_or_reused_activation","process_not_started|public_blocked|activation_reuse_or_concurrency_detected"],["I20","identical_synthetic_bundle_repetition","byte_identical_child_and_public_results|zero_residue|no_source_access"],["O01","accepted_complete_result","handoff=accepted_complete|outer_failure=none|result=accepted|spent_complete"],["O02","accepted_degraded_result","handoff=accepted_degraded|outer_failure=none|result=accepted|spent_degraded"],["O03","accepted_blocked_result","handoff=accepted_blocked|outer_failure=none|result=accepted|spent_blocked"],["O04","outer_binding_failed_before_start","handoff=blocked_before_controller_start|outer_failure=binding_failed_before_controller_start|start=not_invoked|source_rows_opened=0"],["O05","controller_start_failed","handoff=blocked_before_controller_start|outer_failure=controller_start_failed|start=failed|source_rows_opened=0"],["O06","controller_start_state_unknown","handoff=cleanup_state_unknown|outer_failure=controller_state_unknown|start=unknown|counts=null"],["O07","controller_exit_nonzero","handoff=blocked_after_controller_start|outer_failure=controller_exit_nonzero|result=not_accepted|counts=null"],["O08","controller_exit_state_unknown","handoff=cleanup_state_unknown|outer_failure=controller_state_unknown|exit=unknown|counts=null"],["O09","controller_stdout_empty","handoff=blocked_after_controller_start|outer_failure=controller_stdout_empty|result=not_accepted|counts=null"],["O10","controller_stdout_malformed","handoff=blocked_after_controller_start|outer_failure=controller_stdout_malformed|result=not_accepted|no_echo=failed"],["O11","controller_stdout_extra_or_overflow","handoff=blocked_after_controller_start|outer_failure=controller_stdout_extra_or_overflow|result=not_accepted|no_echo=failed"],["O12","controller_stderr_nonempty_or_overflow","handoff=blocked_after_controller_start|outer_failure=controller_stderr_nonempty_or_overflow|result=not_accepted|no_echo=failed"],["O13","controller_residue_detected","handoff=blocked_after_controller_start|outer_failure=controller_residue_detected|cleanup=nonzero|generated_residue_count>0"],["O14","controller_cleanup_state_unknown","handoff=cleanup_state_unknown|outer_failure=controller_state_unknown|cleanup=unknown|counts=null"],["O15","accepted_result_cross_field_mismatch","handoff=blocked_after_controller_start|outer_failure=accepted_result_cross_field_mismatch|result=not_accepted"],["O16","outer_multi_failure_precedence","cleanup_unknown+residue+stderr+stdout_extra=>controller_state_unknown"],["O17","outer_handoff_repetition","byte_identical_handoffs|same_observations|zero_residue|no_source_access"]],"schema":"mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2"}
```

Its SHA-256 is exactly
`2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7`.
The harness must run all 37 adapter cases and all 36 core cases with invented
in-memory bytes and injected symbolic process states only. It must report 73
passed, zero failed, zero skipped, no source access, no private path, no fixture
echo, and zero residue. `I20` runs the same complete synthetic bundle at least
twice and requires byte-identical child and public result bytes, including both
self-digests. `O17` repeats the same outer observations and requires byte-
identical handoff bytes and self-digest. Missing, added, renamed, reordered,
differently typed, skipped, expected-failure, digest-mismatched, or alternate-
fixture cases fail review.

The 17 named `O` rows are mandatory readable test vectors, not a substitute for
complete enumeration. The harness must also enumerate the exact Cartesian
product of these seven ordered dimensions:

```text
prevalidation_status=[passed,failed]
controller_start_status=[not_invoked,failed,started,unknown]
controller_exit_status=[not_applicable,zero,nonzero,unknown]
controller_stdout_status=[not_applicable,one_canonical_result,empty,malformed,extra_or_overflow,unknown]
controller_stderr_status=[not_applicable,empty,nonempty_or_overflow,unknown]
controller_cleanup_status=[not_applicable,zero,nonzero,unknown]
result_candidate_status=[not_present,valid_complete,valid_degraded,valid_blocked,invalid_or_incoherent]
```

The expected tuple count is exactly 15,360. The only coherent pre-start tuples
are one failed-prevalidation/not-invoked tuple and one passed-prevalidation/
definite-start-failure tuple. The only coherent started tuples have passed
prevalidation; `started`; exit `zero` or `nonzero`; one of the four known stdout
states; one of the two known stderr states; cleanup `zero` or `nonzero`; and one
of the five result-candidate states. There are exactly 160 such started tuples.
Every other tuple is contradictory or contains unknown state and therefore
selects `controller_state_unknown`.

The exact handoff-status counts are:

```text
accepted_complete=1
accepted_degraded=1
accepted_blocked=1
blocked_before_controller_start=2
blocked_after_controller_start=157
cleanup_state_unknown=15198
```

The exact outer-failure counts are:

```text
none=3
binding_failed_before_controller_start=1
controller_start_failed=1
controller_exit_nonzero=5
controller_stdout_empty=10
controller_stdout_malformed=10
controller_stdout_extra_or_overflow=10
controller_stderr_nonempty_or_overflow=40
controller_residue_detected=80
accepted_result_cross_field_mismatch=2
controller_state_unknown=15198
```

Both count sets sum to 15,360. Every tuple must select exactly one handoff status
and one outer failure code under the stated precedence. A missing, duplicate,
multiply accepted, unclassified, count-mismatched, or differently ordered
dimension blocks synthetic review.

The future bundle review receipt has schema
`mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3` and
exactly these 29 keys:

```text
schema
review_ref
contract_sha256
controller_profile
controller_program_sha256
controller_entrypoint
complete_result_entrypoint
parser_profile
child_program_sha256
child_entrypoint
child_result_schema
public_result_schema
attempt_handoff_schema
program_bundle_schema
program_bundle_sha256
core_matrix_schema
core_matrix_sha256
core_case_count
adapter_matrix_schema
adapter_matrix_sha256
adapter_case_count
passed_count
failed_count
skipped_count
no_echo_status
source_access_occurred
program_execution_scope
verdict
review_sha256
```

`review_ref` matches
`^characterization_bundle_review_v3_[0-9a-f]{32}$`;
`core_case_count=36`, `adapter_case_count=37`, `passed_count=73`,
`failed_count=0`, `skipped_count=0`, `no_echo_status=passed`,
`source_access_occurred=false`,
`program_execution_scope=synthetic_bundle_only`, and
`verdict=accepted_exact_bundle_and_matrices`. The receipt binds the current
contract, both exact programs, all three entrypoints, both result schemas, the
attempt-handoff schema, 18-field bundle and its self-digest, and both matrix
digests. It uses sorted-key
compact ASCII JSON, UTF-8 without BOM, plus one LF; `review_sha256` omits only
itself. It is transcript-only and grants no source read, activation, package,
or stage authority.

This contract revision does not authorize controller or child creation,
synthetic execution, receipt creation, source access, or activation
construction. After contract review and manifest acceptance, a separate owner
decision may authorize one synthetic-only Codex C implementation candidate
containing exactly the two disposable program basenames above. Codex E must
review both exact byte sequences, the bundle, all 73 outcomes, repeated-run
determinism, and the canonical v3 receipt without editing them. Any byte,
entrypoint, bundle, matrix, contract, or receipt change requires a complete new
synthetic review before an owner may authorize one v5 activation.

## Review-before-seal lifecycle

Future implementation review and final package sealing are separate phases.
An exact later owner authorization may permit Codex C to create only one local,
disposable, explicitly unusable review candidate. This contract does not grant
that authorization.

Candidate-specific source and test digests do not exist when the owner grants
preparation authority. After the static preflight, activation validation, and
exclusive workflow consumption, C may create one ephemeral candidate-staging
root whose basename is derived exactly as:

```text
"MythicEdge-Role-Pool-Windows-Broker-Verifier-Prepare-v5-r"
  + decimal(candidate_revision_ordinal)
  + "-"
  + first_16_lowercase_hex(
      sha256(canonical_json([
        candidate_preparation_owner_activation_sha256,
        candidate_revision_ordinal,
        candidate_prior_revision_digest
      ]))
    )
```

The staging root is internal to the one authorized candidate workflow. It is
not a review candidate, package root, inventory, handoff, or publication state.
C or a conditionally authorized D uses it to copy, edit, build, test, and then
compute the activation-bound preflight packet and candidate revision digest.
Only after those values validate may the actor exclusively create the immutable
review root below and copy the exact frozen rows, disposable outputs, and
`review-preflight.json` into it. The staging root is then removed only under
exact identity and no-reparse checks; unknown cleanup state blocks.

The review root basename is derived exactly as:

```text
"MythicEdge-Role-Pool-Windows-Broker-Verifier-Review-v5-r"
  + decimal(candidate_revision_ordinal)
  + "-"
  + first_16_lowercase_hex(candidate_revision_digest)
```

`ordinal` is `0`, `1`, or `2`; `first16` is the first 16 lowercase hexadecimal
characters of `candidate_revision_digest`. The full digest remains inside
`review-preflight.json`. The review root is a sibling of, never equal to or
inside, the final v5 package root. Its parent is validated by the inherited
resolver, owner, volume, ordinary-path, and no-reparse rules before creation.

The candidate root may contain only the exact 46 source rows, disposable build
outputs produced by the bound recipe, and `review-preflight.json`. It must not
contain `package-inventory.json`, an external implementation handoff, a
publication-failure artifact, service state, installation state, canary state,
or a file with a final-package or final-handoff basename. Candidate outputs are
unsealed, unusable, local-only review material and may not be installed,
published, transferred, adopted, or cited as package evidence.

The closed lifecycle statuses are:

```text
static_preflight_blocked
static_preflight_complete
candidate_preparation_authorized
candidate_activation_consumed
candidate_staging_active
candidate_revision_frozen
candidate_review_pending
candidate_correction_required
candidate_accepted_for_seal
returned_to_codex_b
candidate_cleanup_blocked
expired_or_revoked
```

The only transitions are:

```text
static_preflight_blocked -> static_preflight_complete
static_preflight_complete -> candidate_preparation_authorized
candidate_preparation_authorized -> candidate_activation_consumed
candidate_activation_consumed -> candidate_staging_active
candidate_staging_active -> candidate_revision_frozen
candidate_revision_frozen -> candidate_review_pending
candidate_review_pending -> candidate_accepted_for_seal
candidate_review_pending -> candidate_correction_required
candidate_review_pending -> returned_to_codex_b
candidate_correction_required -> candidate_staging_active
candidate_staging_active -> returned_to_codex_b
candidate_staging_active -> candidate_cleanup_blocked
any nonterminal status -> expired_or_revoked
```

The first transition requires the accepted manifest amendment and complete
static preflight. The second records, but does not create, the later exact owner
authorization. The third atomically consumes that activation for the whole
candidate workflow. No staging root may precede the fourth transition. A
candidate revision becomes frozen only after the exact source/test bytes,
44-row unchanged-source root, build recipe, activation-bound preflight packet,
and disposable validation results have been reread and recomputed. Freezing is
no-replace; no actor may edit a frozen root or relabel its digest.

The direct `candidate_staging_active -> returned_to_codex_b` transition applies
only when build or test work blocks before freezing and exact attempt-owned
cleanup proves staging absence and zero generated residue. A failed, unreadable,
ambiguous, or partial cleanup instead derives `candidate_cleanup_blocked`; that
status is terminal under this contract, authorizes no retry or repair, and
routes to Codex B and the owner. Neither transition creates a candidate revision
or a Codex D correction cycle.

Each revision has immutable:

```text
implementation_sha256
test_sha256
unchanged_source_rows_root_digest
build_recipe_schema
build_recipe_ref
build_recipe_sha256
build_recipe_status
build_recipe_independent_review_ref
build_recipe_independent_review_sha256
build_recipe_independent_review_status
candidate_revision_digest
```

Revision 0 has `candidate_prior_revision_digest=none` and an empty sorted
`candidate_correction_finding_ids` array. Revisions 1 and 2 require the exact
prior candidate digest and a nonempty, sorted, duplicate-free array of open
Codex E finding IDs. A revision may not reuse its own or an earlier digest.

Codex E reviews the frozen candidate and packet without editing either. E may
accept the exact candidate digest, return concrete implementation or test
findings inside the two-path envelope to Codex D, or route contract ambiguity
to Codex B. E review grants no package, seal, publication, installation, canary,
stage, or live authority.

Codex D may perform at most two correction cycles: ordinal 1 and ordinal 2.
Each cycle requires exact open E finding IDs and creates a new sibling review
root and new immutable candidate digest. D may edit only:

```text
tools/publish_implementation_candidate.py
tests/test_implementation_handoff.py
```

D may not mutate a prior revision, change the build recipe, add or remove a
path, dependency, schema, authority field, manifest effect, output family,
external effect, or behavior outside those findings. It may not create the
final root, inventory, handoff, failure artifact, installation, service, or
canary state. A contract question, new path, new schema, new authority need,
manifest change, recipe change, broader behavior, or third requested D cycle
sets `candidate_lifecycle_status=returned_to_codex_b`.

E must independently review every new revision and must never edit candidate
bytes, tests, recipe, packet, lifecycle projection, or finding list. Acceptance
names one exact `candidate_revision_digest` and one exact `packet_sha256` and
has durable effect only through the independently published receipt below. It
does not float to a later revision.

The final v5 package root, final inventory, external handoff, publication
failure state, installation state, service state, and canary state must all be
absent throughout candidate preparation, D correction, and candidate review.
Their presence, collision, ambiguous identity, or prior partial creation blocks
review and routes to Codex B without cleanup of unknown state.

## Independent candidate-review receipt

Codex E's candidate decision is durable only through
`mythic_edge_role_pool_v5_candidate_independent_review_receipt.v2`. A chat
message, handoff summary, finding list, matching digest string, or filesystem
timestamp is not a receipt and cannot support final-seal activation.

The receipt is strict canonical JSON under the same UTF-8, duplicate-key,
unknown-key, ordering, whitespace, and final-LF rules as the preflight packet.
Its complete key set is:

```text
review_receipt_schema=mythic_edge_role_pool_v5_candidate_independent_review_receipt.v2
review_receipt_kind=candidate_implementation_review
review_ref
contract_id
contract_path
contract_sha256
parent_contract_id
parent_contract_sha256
manifest_file_count=37
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=contract_sha256
manifest_rebind_amendment_path
manifest_rebind_amendment_sha256
manifest_rebind_status=accepted_implemented_current
candidate_preparation_owner_activation_ref
candidate_preparation_owner_activation_sha256
candidate_preparation_activation_schema=mythic_edge_role_pool_v5_candidate_preparation_activation.v2
candidate_preparation_activation_packet_sha256
activation_consumption_mechanism=mythic_edge_role_pool_v5_atomic_activation_packet_move.v1
activation_consumption_operation_kind=candidate_preparation
activation_consumption_key_sha256
candidate_preparation_activation_status=consumed_for_candidate_workflow
candidate_preparation_activation_expiry_utc
candidate_revision_ordinal
candidate_revision_digest
candidate_packet_sha256
candidate_prior_revision_digest
candidate_correction_finding_ids
implementation_path=tools/publish_implementation_candidate.py
implementation_sha256
test_path=tests/test_implementation_handoff.py
test_sha256
unchanged_source_rows_root_digest
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_ref
build_recipe_sha256
build_recipe_status=complete
build_recipe_independent_review_ref
build_recipe_independent_review_sha256
build_recipe_independent_review_status=accepted_exact_recipe_and_contract
candidate_edit_envelope_sha256
candidate_operation_profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
candidate_operation_matrix_sha256
candidate_operation_matrix_expected_pair_count=64
candidate_operation_matrix_accepted_pair_count=26
candidate_operation_matrix_rejected_pair_count=38
timestamp_floor_matrix_expected_tuple_count=60
timestamp_floor_matrix_accepted_tuple_count=2
timestamp_floor_matrix_rejected_tuple_count=58
failure_matrix_expected_tuple_count=34560
failure_matrix_accepted_tuple_count=20
failure_matrix_rejected_tuple_count=34540
projection_matrix_expected_tuple_count=180
projection_matrix_accepted_tuple_count=5
projection_matrix_rejected_tuple_count=175
reviewer_role=codex_e_independent_reviewer
reviewed_at_utc
reviewed_candidate_lifecycle_status=candidate_review_pending
review_verdict
finding_class
finding_ids
resulting_candidate_lifecycle_status
candidate_bytes_mutated_by_reviewer=false
candidate_accepted_for_seal
next_role
ready_for_codex_c=false
ready_for_codex_d=false
implementation_authorized=false
final_seal_authorized=false
package_creation_authorized=false
inventory_creation_authorized=false
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
receipt_digest
```

`reviewed_at_utc` is an RFC 3339 UTC timestamp at whole-second precision with
literal `Z`. It must be no earlier than candidate freezing, no later than the
candidate-workflow activation expiry, and not in the future when validated.
All candidate, packet, activation, amendment, file, recipe, edit, and matrix
values are recomputed from their owning artifacts before receipt construction.

`review_ref` is mechanically derived, not caller selected. First construct the
canonical receipt object with both `review_ref` and `receipt_digest` omitted;
then compute its SHA-256 and set:

```text
review_ref="candidate_review_v1_" + first_32_lowercase_hex(sha256)
```

After inserting `review_ref`, `receipt_digest` is lowercase SHA-256 over the
canonical receipt with only `receipt_digest` omitted. The exact raw receipt-file
SHA-256 is separately recomputed by its consumer and is never substituted by
`receipt_digest`.

The receipt basename is the exact review-root basename plus
`.independent-review-receipt.v1.json`. It is exclusively created as a sibling
of the review root, never inside it, so E does not mutate candidate bytes. The
parent identity is revalidated without following a reparse point. Existing,
colliding, unreadable, multiply linked, non-ordinary, or ambiguous receipt paths
block without overwrite, adoption, repair, or deletion. Receipt-write failure
means no durable E decision and cannot be projected as acceptance.

The closed `finding_class` vocabulary is `none`,
`bounded_implementation_or_test`, and `contract_scope_or_authority`. Finding
IDs are sorted, unique ASCII values matching
`^[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$`. `none` requires an empty array; either
other class requires a nonempty array.

The closed verdict derivation is mutually exclusive:

| review verdict | finding class | ordinal condition | resulting lifecycle | accepted for seal | next role |
| --- | --- | --- | --- | --- | --- |
| `accepted_candidate_digest` | `none` | `0`, `1`, or `2` | `candidate_accepted_for_seal` | `true` | `owner_final_seal_activation_decision` |
| `bounded_correction_required` | `bounded_implementation_or_test` | `0` or `1` | `candidate_correction_required` | `false` | `codex_d_bounded_candidate_correction` |
| `returned_to_codex_b` | `bounded_implementation_or_test` | exhausted `2` | `returned_to_codex_b` | `false` | `codex_b_contract_reconciliation` |
| `returned_to_codex_b` | `contract_scope_or_authority` | `0`, `1`, or `2` | `returned_to_codex_b` | `false` | `codex_b_contract_reconciliation` |

No receipt tuple may match more than one row. A contract, path, dependency,
schema, authority, recipe, manifest, external-effect, or behavior-scope finding
must use `contract_scope_or_authority`; it cannot be relabelled as bounded.
`accepted_candidate_digest` requires complete review, exact byte and packet
bindings, all required candidate validation passed, no open finding, and
`candidate_bytes_mutated_by_reviewer=false`.

The transition out of `candidate_review_pending` occurs only when the exact
canonical receipt is exclusively published and reread successfully. Before
that point the candidate remains `candidate_review_pending`; an in-memory
verdict, failed write, collision, or ambiguous receipt state cannot advance it.

Every receipt keeps all authority and claim fields false. The accepted row says
only that E accepted one candidate digest for an owner final-seal decision. It
does not authorize D, final construction, inventory, publication, installation,
canary, stage advancement, or live use. A later revision requires a new receipt;
an earlier receipt never floats forward.

## Separate final-seal gate

After one exact receipt records `accepted_candidate_digest` for one frozen
candidate revision, a new exact owner activation with the closed 75-field
profile `mythic_edge_role_pool_v5_final_seal_activation.v2` is required before
final construction. V1 or unversioned seal packets fail closed. Candidate
acceptance is not that activation. The seal reuses the
inherited symbolic owner-approval reference grammar and the contract-defined
atomic consumption mechanism; it creates no new general authority family.

The activation must bind all inherited v4 owner-activation requirements plus
this complete v5 seal set:

```text
owner_activation_ref
owner_activation_sha256
owner_activation_status=approved_unconsumed
activation_expiry_utc
activation_single_use=true
activation_consumption_mechanism=mythic_edge_role_pool_v5_atomic_activation_packet_move.v1
activation_consumption_operation_kind=final_seal
activation_consumption_preflight_authorized=true
activation_consumption_synthetic_validation_authorized=true
activation_consumption_state_root_creation_authorized=true
activation_consumption_real_packet_move_authorized=true
activation_consumption_persisted_helper_authorized=false
contract_id
contract_path
contract_sha256
parent_contract_id
parent_contract_sha256
accepted_candidate_revision_ordinal
accepted_candidate_revision_digest
accepted_candidate_packet_sha256
independent_candidate_review_receipt_schema=mythic_edge_role_pool_v5_candidate_independent_review_receipt.v2
independent_candidate_review_ref
independent_candidate_review_receipt_digest
independent_candidate_review_file_sha256
manifest_file_count=37
manifest_v5_path=references/external-isolation-broker-v5-corrective-successor.md
manifest_rebind_from_sha256=85ba86efc9de549d815b6885c8d3a6708894192d1af1849839d88d55dbb71704
manifest_rebind_to_sha256=contract_sha256
manifest_rebind_amendment_path
manifest_rebind_amendment_sha256
manifest_rebind_status=accepted_implemented_current
candidate_edit_envelope_sha256
candidate_operation_profile=mythic_edge_role_pool_v5_candidate_operation_authority.v1
candidate_operation_matrix_sha256
candidate_operation_matrix_expected_pair_count=64
candidate_operation_matrix_accepted_pair_count=26
candidate_operation_matrix_rejected_pair_count=38
implementation_sha256
test_sha256
unchanged_source_rows_root_digest
build_recipe_schema=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_ref
build_recipe_sha256
build_recipe_status=complete
build_recipe_independent_review_ref
build_recipe_independent_review_sha256
build_recipe_independent_review_status=accepted_exact_recipe_and_contract
package_authority_profile
package_id
package_directory_name
inventory_schema
handoff_schema
publication_failure_schema
package_creation_authorized=true
source_copy_authorized=true
local_source_copy_authorized=true
package_build_authorized=true
local_build_authorized=true
package_self_tests_authorized=true
inventory_creation_authorized=true
handoff_creation_authorized=true
handoff_publication_authorized=true
failure_artifact_creation_authorized=true
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_mutation_authorized=false
live_ready=false
current_v4_reuse_authorized=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

This ordered field-name and derivation list is the canonical input for
`future_activation_requirements_sha256` in the preflight packet. The future
activation supplies exact values and explicit Booleans; absence, placeholder,
expiry, revocation, prior consumption, reuse, contradiction, digest mismatch,
or broader authority fails before final-root creation.

The final-seal activation must use the exact atomic activation-packet move
defined above with `operation_kind=final_seal`. Its key and destination must be
distinct from candidate preparation, and only the actor whose no-replace move
and complete destination readback both succeed may continue. An existing
destination, missing source, unknown move result, failed readback, or any
contradiction blocks before final-root creation and requires a fresh successor
activation. This contract defines that mechanism but authorizes no state-root
creation, packet move, or final-seal operation.

Final construction may read and copy only the exact accepted candidate's 46
source rows and execute only the accepted build recipe. Immediately before the
first final-root operation, it must recompute the contract, parent, manifest
amendment, packet, candidate revision, two edited file, unchanged-row root,
edit-envelope, recipe, review-receipt schema, symbolic reference, receipt
digest, raw receipt-file SHA-256, and activation bindings. It must also prove the
final root, inventory, handoff, and publication-failure paths are absent. Any
drift or ambiguity fails before final-root or inventory creation; no rebuild
from different bytes, ambient recipe, fallback source, or repaired candidate is
allowed.

After sealing, Codex E's final review is limited to exact-byte correspondence,
inventory closure, handoff projection, digest derivation, publication state,
staging/residue state, activation use, authority flags, and preserved nonclaims.
Final E must not reopen implementation design or edit sealed bytes. A defect
discovered after immutable final sealing requires a new successor contract and
package identity; v5 must not be repaired in place.

## v5 inventory, handoff, and failure requirements

The v5 inventory and handoff inherit all v4 canonical JSON, duplicate-key,
unknown-key, finite-number, self-digest, ordinary-file, identity, and no-echo
rules. Their exact key sets are the corresponding v4 sets with:

1. all v5 schema, contract, package, basename, and authority-profile literals
   above;
2. the shared `rejected_v3_*` lineage fields replaced by
   `rejected_v4_package_id`, `rejected_v4_inventory_file_sha256`,
   `rejected_v4_inventory_root_digest`, `rejected_v4_handoff_file_sha256`, and
   `rejected_v4_handoff_root_digest`;
3. in the handoff only, `rejected_v3_reuse_authorized` replaced by
   `rejected_v4_reuse_authorized=false`;
4. `rejected_v4_review_status=not_accepted_contract_mismatch` immediately after
   the lineage fields;
5. the publication-failure schema bound to v3; and
6. no new public binding, witness, inventory-provenance, private-identity, or
   source-content field.

The v5 inventory has exactly 51 rows: 46 source rows and five fresh generated
outputs. It preserves the inherited predecessor classifications as
`carry_forward_baseline_row_count=37` and
`carry_forward_created_row_count=9`. Exactly the two edit-envelope paths are
modified carry-forward paths; the other 44 are unchanged. Created, removed,
unexpected, and changed Role Pool paths remain empty.

The candidate handoff remains
`candidate_ready_for_independent_review`, routes to
`codex_e_independent_review`, and keeps every effect, claim, reuse, successor,
installation, canary, stage, and live boolean false. Candidate blockers remain:

```text
independent_review_pending
installation_not_authorized
stage4_canary_not_authorized
```

A blocked handoff or publication-failure projection routes to Codex B. Neither
the private binding nor a matching digest pair changes that route or grants
authority.

## Deterministic validation matrix

Future implementation validation must include all inherited v4 tests plus the
following focused matrix.

### Contract preflight

- prove static preflight completes from already owned artifacts before the
  candidate-preparation activation and emits no file, candidate digest,
  implementation digest, recipe value, authority, staging path, or root;
- prove a complete static digest and accepted manifest amendment are required
  before owner activation, while the owner activation supplies the exact build
  recipe before activation-bound preflight;
- prove the owner activation is validated and exclusively consumed once for
  the whole candidate workflow before any candidate-staging path is created;
- reject preflight-requires-activation and activation-requires-candidate-packet
  cycles, a recipe supplied after staging, and any staging or review root
  created out of order;
- prove the exact two-path v5 envelope is a strict subset of the recomputed
  four-path parent envelope and reject every missing, extra, duplicate,
  case-varied, separator-varied, reordered, or non-owning path projection;
- recompute every packet digest from its owning artifact or canonical object,
  then reject missing, malformed, stale, contradictory, cross-attempt, and
  correctly shaped but incorrect values one field at a time;
- enumerate the timestamp-floor universe as 60/2/58, the v5 failure universe
  as 34560/20/34540, and the v5 projection universe as 180/5/175 for
  expected/accepted/rejected counts;
- prove every tuple is classified exactly once, every accepted tuple is one
  normative row, and every other tuple is rejected;
- reject a missing, unaccepted, unimplemented, wrong-path, wrong-count,
  wrong-from-digest, or wrong-to-digest manifest rebind amendment; require 37
  files, the exact v5 path, and exact equality of the rebound digest with
  `contract_sha256`;
- prove the canonical packet digest changes for any contract, parent,
  amendment, source, test, unchanged-row, recipe, matrix, activation-requirement,
  prior-revision, or finding-ID change; and
- prove packet validation creates no authority or package state.

### Candidate operation authority

- recompute the operation-profile object and
  `candidate_operation_matrix_sha256` from the closed vocabulary and normative
  actor rows, then require exactly 64 expected, 26 accepted, and 38 rejected
  actor-operation pairs in every bound schema;
- exercise all 26 accepted pairs and prove each is accepted by exactly one row;
  enumerate and reject the other 38 pairs without an implicit or default allow;
- reject an otherwise allowed pair for a wrong actor, revision ordinal,
  predecessor state, activation status, activation expiry, prior receipt,
  finding-ID binding, path envelope, operation alias, or relabelled role;
- prove C cannot read generated v4 outputs, a prior candidate revision, or an E
  receipt, and cannot perform any E-only or final-seal operation;
- prove D cannot read the v4 parent package or act without the exact prior E
  receipt, bounded finding IDs, available ordinal, and unchanged build recipe;
- prove E cannot edit, copy, build, test, clean staging, write inside a candidate,
  or create any artifact other than the exact no-replace sibling receipt;
- prove candidate-specific authority cannot make a generic implementation,
  package, inventory, handoff, publication, installation, service, canary,
  stage-advancement, external-write, or live-readiness field true; and
- reject source-repository access, network access, raw-output retention or echo,
  final-root creation, and every operation outside the closed vocabulary for
  every actor and revision.

### Review-before-seal

- accept only ordinals 0, 1, and 2 with exact prior-digest and finding-ID
  derivations; reject a third correction, skipped ordinal, reused digest,
  mutation of a frozen root, or floating E acceptance;
- prove the review root is a validated sibling distinct from the final root
  and cannot contain a final inventory, external handoff, publication-failure
  artifact, install/service/canary state, or final basename;
- prove the ephemeral staging-root identity is activation-derived, precedes
  candidate digest calculation, never becomes the review or final root, and is
  removed only after an exact immutable review root exists;
- prove E's interface is read-only and cannot alter candidate, packet, tests,
  recipe, lifecycle, or finding IDs;
- prove D can act only after concrete E findings and can change only the two
  contracted paths without changing recipe, dependency, schema, authority,
  manifest effect, output family, or behavior scope;
- route a contract question, broadened edit, new schema/path/authority, recipe
  change, exhausted correction count, candidate drift, final-path presence, or
  ambiguous identity to Codex B; and
- prove review outputs retain all false-authority and nonclaim fields.

### Independent review receipt

- reject every missing, extra, duplicate, reordered, malformed, stale,
  cross-candidate, cross-packet, cross-activation, cross-amendment, and correctly
  shaped but incorrect receipt field;
- recompute the symbolic review reference, receipt digest, and raw receipt-file
  SHA-256 independently and reject substitution among them;
- cover every mutually exclusive verdict row, all three ordinals, empty versus
  nonempty finding arrays, every finding class, exhausted correction routing,
  and one-field mutations of lifecycle, accepted Boolean, or next role;
- reject unsorted, duplicate, malformed, unbound, or relabelled finding IDs and
  any attempt to route contract/scope/authority findings to D;
- prove E cannot write inside or mutate the review root and can create only one
  no-replace sibling receipt for the exact candidate digest;
- prove receipt collision, failed write, unreadable readback, reparse point,
  non-ordinary path, or ambiguous identity leaves the candidate review pending
  and creates no accepted projection; and
- prove every receipt authority and nonclaim field is literal false and that
  final-seal activation accepts only the exact accepted receipt's schema,
  symbolic reference, self-digest, and raw file SHA-256.

### Final seal

- require one exact E-accepted candidate/packet pair and a new unexpired,
  unconsumed, single-use owner activation containing every closed seal field;
- reject missing, stale, revoked, expired, reused, contradictory, broadened,
  placeholder, cross-candidate, cross-contract, or cross-manifest activation;
- recompute every accepted source, test, unchanged-row, recipe, contract,
  amendment, packet, review, edit-envelope, and activation digest before any
  final-root operation;
- prove any byte or recipe drift blocks before final-root and inventory
  creation and cannot fall back to ambient or reconstructed inputs;
- prove activation reservation is exclusive to one attempt and fails closed if
  the inherited mechanism cannot provide that property;
- limit final E review mechanically to bytes, inventory, handoff, digests,
  publication, residue, activation use, authority, and nonclaims; and
- prove a post-seal defect cannot mutate v5 and routes to a successor.

### Binding factory

- accept only an exact final v5 inventory whose raw bytes, strict parsed value,
  self-digest, root digest, rows, file identity, attempt, package, contract, and
  expected in-memory candidate all match;
- cover both closed staging observations and no third state;
- reject invalid UTF-8, duplicate keys, unknown keys, noncanonical bytes,
  malformed digest, bad self-digest, bad root, row drift, length drift, wrong
  count, wrong package, wrong contract, wrong attempt, wrong final identity,
  reparse point, non-ordinary file, wrong volume/owner, and inaccessible final;
- reject v4, stale, copied, forged, deserialized, subclassed, cross-process, and
  cross-attempt binding values;
- prove no public constructor, registry, cache, serialization, log, snapshot,
  exception, or return value contains the binding or private fields; and
- prove binding creation cannot occur from staging bytes or before final
  inventory publication.

### Projection and state derivation

- one positive test for every row of the closed binding/projection matrix;
- one positive test for candidate-ready handoff construction after final
  inventory validation;
- for every positive row, mutate inventory status, binding presence, binding
  state, attempt, contract, package, file identity, each digest, and lifecycle
  code separately and require rejection before serialization;
- prove candidate-ready and every frozen failure row copy both digest strings
  from the binding and expose no caller parameter for those strings;
- prove `not_created` and `unknown` accept no binding and emit two literal
  `none` values;
- mutate or replace the final inventory after binding creation and prove the
  immediate revalidation rejects before handoff or projection bytes exist;
- prove an inventory-staging-cleanup failure may project frozen digests only
  from the cleanup-failed binding state;
- prove all other post-inventory rows require staging absence;
- reject multiple matching rows, unknown error codes, unknown keys, coercion,
  inferred repair, and every lifecycle combination outside the complete v5
  matrix; and
- preserve all tests that fixed EIB-PKG-V3-E-001, EIB-PKG-V3-E-002, and
  EIB-PKG-V3-E-003.

### Publication, rollback, and no-echo

- prove inventory final publication and validation precede candidate handoff
  construction;
- prove a handoff failure never deletes, overwrites, repairs, or reclassifies a
  valid frozen inventory;
- prove partial writes remain staging-only and cannot create a binding;
- prove a crash or restart cannot recover or reuse an ephemeral binding;
- prove existing final paths, collisions, unknown publication state, cleanup
  failure, and retry exhaustion follow only their closed normative v5 matrix
  rows;
- prove raw bytes, source text, approval text, absolute paths, file identities,
  exceptions, tracebacks, digests supplied by callers, keys, credentials, and
  private activation inputs never appear in public-safe diagnostics; and
- prove v4 package, inventory, handoff, contract, and review bytes remain exact.

### Package and Role Pool

- validate all exact v4 lineage pins and all 51 v4 inventory rows before any
  v5 root or copy operation;
- prove only the two edit-envelope paths changed among v5 source rows;
- run focused source tests before build;
- run clean managed build, native bootstrap build, binary self-tests, and full
  package validation with zero failures, errors, or skips;
- rebuild and inventory all five outputs exactly once;
- validate v5 inventory and handoff canonical digests and public cross-field
  derivations;
- run Role Pool focused tests and the full offline release gate; and
- preserve the explicit `NOT LIVE-READY` conclusion.

Committed or public-safe evidence may contain only symbolic statuses, counts,
relative names, and approved digests. Raw command output, source text, approval
text, absolute paths, private file identities, exceptions, tracebacks, secrets,
credentials, and private activation inputs are prohibited.

## Rollback and residue policy

Before final inventory publication, a failed attempt may remove only its exact
v5 staging files and newly created v5 root under inherited identity checks.
After final inventory publication, the final inventory is immutable evidence of
that attempt and must not be removed or overwritten merely because handoff
publication failed. The applicable public failure projection records the
state. Unknown identity or publication state blocks cleanup.

No mutable cache, binding file, digest witness, temporary database,
uncontracted receipt, service state, install state, canary output, or
uncontracted lifecycle artifact is permitted. The only additional lifecycle
state defined by this revision is an exact immutable moved candidate-preparation
or final-seal activation packet under the validated consumption state root. It
contains no private approval bytes or path, is never public package evidence,
and cannot be deleted, repaired, replaced, or adopted under this contract.
Before final sealing, the exact frozen review root, its `review-preflight.json`,
and its no-replace sibling independent-review receipt are the only contracted
review artifacts. An accepted root and receipt must remain exact and readable
through final-seal activation and final E review; this contract grants no
deletion authority. A failed final attempt must leave no residue other than an
exact consumed activation packet and the exact final inventory, exact staging
file, exact handoff, or exact public failure artifact required by its closed
state. Existing v4 artifacts remain untouched.

## Current manifest-rebind blocker

Immediately before this revision, the installed validator recognized exactly
37 paths and bound this contract path to
`48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be`.
The implemented amendment at `references/stage3-behavioral-planning.md` had
SHA-256
`9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d`.
Its accepted successor static preflight had SHA-256
`95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af`,
and the resulting 37-file manifest had SHA-256
`5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc`.
Those are immutable pre-revision lineage facts.

Codex E then accepted only the exact single-row synthetic program and 36-case
core matrix identified by the historical v1 review receipt above. The owner
constructed one v4 characterization activation. Codex C validated its complete
packet but stopped before atomic consumption because that reviewed program had
no contracted three-row real-source adapter or parent-owned complete-result
entrypoint. No process started, no source or package row opened, and no
generated residue remained. That activation is permanently non-reusable.

The immediate contract input to this Codex B revision had SHA-256
`5501d9e18bb948edb1fe464ae28c2e4b733399ed94b430b3939ca3d115cd4da2`
and status
`real_source_adapter_contract_review_and_manifest_rebind_blocked`. Codex E
found `EIB-PKG-V5-ADAPTER-E-001` because its outer-launcher failure class had no
closed vocabulary, precedence, handoff projection, or synthetic coverage.
This docs-only revision changes only this contract's bytes. It preserves the
controller, three-row child adapter, child and public results, exact two-program
scope, host, and AST derivation while adding the 27-field transcript-only
attempt handoff, exhaustive fallback derivation, outer-failure precedence, v2
37-case adapter matrix, 18-field bundle, and 29-field review receipt. It does
not implement either program, define recipe v2, authorize synthetic or real-
source execution, change the 37-path set, or implement a manifest transition.
The installed validator must therefore fail
closed on the revised v5 contract digest until an independently accepted
37-to-37 rebind is separately approved and implemented. The only permitted
primary blocker attributable to this edit is:

```text
v5 successor digest does not match the pinned digest
```

The docs-only validation run reached all 346 tests after structural validation
passed, then failed closed with 52 errors and one failure. The primary error
above projected through the current manifest-rebind binding-drift wrappers,
while the one failure was the legacy assertion that expected the predecessor
amendment error before reaching the now-earlier stale contract check. Every
observed error and the failure derive from the same stale v5 digest. They do not
become separate accepted blockers. Any other unique root cause is unrelated or
proves that this revision changed more than declared and must block. This
expected failure shape is not an offline-gate pass.

After Codex E accepts this exact revised contract, a separate narrow 37-to-37
digest-rebind amendment and separately authorized implementation may update
only the exact v5 digest binding and its focused expected test values in:

```text
scripts/check_stage3_behavioral_planning.py
scripts/test_stage3_behavioral_planning.py
```

The path set and count must remain unchanged. Positive, digest-mismatch,
missing, renamed, case-varied, duplicate, extra-path, modified-existing-path,
non-ordinary, mandatory reparse-path, count-37, receipt-drift, recipe-drift,
predecessor-drift, and legacy-regression checks remain mandatory. Dynamic digest
adoption, an unrelated file change, a missing path, count drift, modified legacy
binding, or any unique cause other than the declared stale binding fails
closed. Contract review neither writes nor authorizes the amendment.

The required order is exact revised-contract review, separate manifest-rebind
contract and implementation authority, independent implementation review, and
then a separately owner-authorized synthetic-only controller/child
implementation. Codex E must accept both exact program digests, the 18-field
bundle, all 73 cases, the 27-field handoff projection, and the canonical v3
review receipt before the owner may
construct one fresh `owner_characterization_activation_v5_*`. Only that
activation may permit one exact three-row execution. Its accepted public-safe
v3 result returns to Codex B for recipe-v2 or exact script-envelope design.
Recipe v2, its independent review, any resulting edit-envelope change, the
dependent static preflight, and any resulting manifest rebind must all be
accepted before the owner may construct a fresh candidate-preparation
activation. The rejected v4 characterization activation, the consumed
candidate activation, and every earlier rejected activation remain
non-reusable.

Until those gates complete, all remain:

```text
manifest_pre_revision_contract_sha256=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
contract_revision_input_sha256=5501d9e18bb948edb1fe464ae28c2e4b733399ed94b430b3939ca3d115cd4da2
manifest_pre_revision_amendment_sha256=9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d
manifest_pre_revision_static_preflight_sha256=95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af
manifest_pre_revision_sha256=5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc
manifest_file_count=37
manifest_integration_status=stale_digest_rebind_required_after_contract_review
manifest_rebind_authorized=false
contract_acceptance_ready=false
ready_for_codex_c=false
```

## False-authority fields and next role

```text
ready_for_codex_c=false
ready_for_codex_d=false
ready_for_codex_f=false
implementation_authorized=false
manifest_rebind_amendment_authorized=false
candidate_preparation_authorized=false
candidate_preparation_owner_activation_created=false
candidate_preparation_activation_consumption_authorized=false
atomic_activation_consumption_contract_defined=true
atomic_observation_oracle_status=accepted_exact_768_tuple_oracle
atomic_activation_consumption_contract_review_status=accepted
atomic_activation_consumption_execution_authorized=false
activation_consumption_state_root_creation_authorized=false
activation_consumption_record_creation_authorized=false
prior_candidate_activation_ref=owner_activation_v1_598bcbcb457ac51a2e51612e3ef98f26
prior_candidate_activation_status=consumed_for_candidate_workflow
prior_candidate_activation_reuse_authorized=false
fresh_candidate_activation_required=true
candidate_lifecycle_status=returned_to_codex_b
candidate_revision_frozen=false
candidate_review_root_created=false
candidate_inventory_created=false
candidate_cleanup_status=complete_zero_generated_residue
candidate_parent_inventory_metadata_read_authorized=false
candidate_parent_source_rows_read_authorized=false
candidate_prior_revision_read_authorized=false
candidate_source_copy_authorized=false
disposable_candidate_implementation_edit_authorized=false
disposable_candidate_test_edit_authorized=false
build_recipe_definition_status=complete_owner_selected
build_recipe_v1_ref=mythic_edge_role_pool_v5_build_recipe.v1
build_recipe_v1_sha256=4bbf49f633d8d7ee506c712d96f61bf8ee64ded8cd965b6675417939c02d8eb3
build_recipe_v1_independent_review_ref=build_recipe_review_v1_6128230418da966dd28bdc271edbf6d9
build_recipe_v1_independent_review_sha256=b0db654fce1316984c7e0380b85e77caadac580a256313bc2f41bb872c32667f
build_recipe_v1_independent_review_status=accepted_exact_recipe_and_contract_definition
build_recipe_v1_execution_compatibility_status=blocked_observed
build_recipe_v1_future_execution_authorized=false
build_recipe_v2_defined=false
build_recipe_v2_independent_review_status=not_applicable
build_recipe_review_receipt_schema_defined=true
historical_v4_command_tuple_verified=false
exact_v4_archive_reused=true
exact_v4_build_scripts_reused=true
v5_recipe_selection=owner_selected_from_verified_v4_components
build_recipe_ref_created=true
build_recipe_sha256_created=true
build_recipe_execution_compatibility_claimed=false
build_dependency_characterization_contract_defined=true
build_dependency_characterization_controller_profile=mythic_edge_role_pool_v5_characterization_controller.v1
build_dependency_characterization_parser_profile=mythic_edge_role_pool_v5_powershell_ast_characterizer.v3
build_dependency_characterization_child_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_child_result.v1
build_dependency_characterization_activation_schema=mythic_edge_role_pool_v5_build_dependency_characterization_activation.v5
build_dependency_characterization_result_schema=mythic_edge_role_pool_v5_build_dependency_characterization_result.v3
build_dependency_characterization_program_bundle_schema=mythic_edge_role_pool_v5_characterization_program_bundle.v2
build_dependency_characterization_attempt_handoff_schema=mythic_edge_role_pool_v5_build_dependency_characterization_attempt_handoff.v1
build_dependency_characterization_earlier_activation_ref=owner_characterization_activation_v2_0b0dab1b1a0e42df8d738265b57dbe42
build_dependency_characterization_earlier_activation_status=spent_failed_after_source_open
build_dependency_characterization_earlier_activation_reuse_authorized=false
build_dependency_characterization_earlier_source_access_occurred=true
build_dependency_characterization_earlier_source_rows_opened=1
build_dependency_characterization_earlier_failure_code=characterization_incomplete
build_dependency_characterization_blocked_activation_ref=owner_characterization_activation_v4_ef639662d32f47b5afb41c20b4a25516
build_dependency_characterization_blocked_activation_status=rejected_before_process_start_unconsumed_non_reusable
build_dependency_characterization_blocked_activation_reuse_authorized=false
build_dependency_characterization_blocked_packet_validation=passed
build_dependency_characterization_blocked_execution_capability_validation=blocked
build_dependency_characterization_blocked_capability_blocker=single_row_synthetic_entrypoint_only
build_dependency_characterization_blocked_source_access_occurred=false
build_dependency_characterization_blocked_source_rows_opened=0
build_dependency_characterization_blocked_package_accessed=false
build_dependency_characterization_blocked_generated_residue_count=0
build_dependency_characterization_evidence_created=false
build_dependency_characterization_source_lifetime_contract_defined=true
build_dependency_characterization_exact_host_contract_defined=true
build_dependency_characterization_ast_row_derivation_defined=true
build_dependency_characterization_lifecycle_derivation_defined=true
build_dependency_characterization_multi_failure_priority_defined=true
build_dependency_characterization_core_matrix_schema=mythic_edge_role_pool_v5_characterization_synthetic_matrix.v1
build_dependency_characterization_core_matrix_sha256=9203cddc40fa42fe661c0fd0635f83b53619b462808447bf737916aa102a6526
build_dependency_characterization_core_case_count=36
build_dependency_characterization_adapter_matrix_schema=mythic_edge_role_pool_v5_characterization_adapter_synthetic_matrix.v2
build_dependency_characterization_adapter_matrix_sha256=2d6cee277836948115925f3629e4f0babe23e975dd3eac96c97a3429d776c8f7
build_dependency_characterization_adapter_case_count=37
build_dependency_characterization_historical_review_schema=mythic_edge_role_pool_v5_characterization_synthetic_review_receipt.v1
build_dependency_characterization_historical_review_ref=characterization_review_v1_59295fc8186f44d0b2225958fb9092d6
build_dependency_characterization_historical_review_sha256=15c65235a21e68f09aed48f0d9c9679bf835ba71852700ec232dae3998637c78
build_dependency_characterization_historical_review_status=accepted_single_row_synthetic_only
build_dependency_characterization_historical_review_current_authority=false
build_dependency_characterization_bundle_review_schema=mythic_edge_role_pool_v5_characterization_bundle_review_receipt.v3
build_dependency_characterization_real_source_adapter_defined=true
build_dependency_characterization_real_source_adapter_implemented=false
build_dependency_characterization_complete_result_entrypoint_defined=true
build_dependency_characterization_complete_result_entrypoint_implemented=false
build_dependency_characterization_outer_acceptance_defined=true
build_dependency_characterization_outer_failure_vocabulary_defined=true
build_dependency_characterization_outer_failure_precedence_defined=true
build_dependency_characterization_attempt_handoff_defined=true
build_dependency_characterization_attempt_handoff_created=false
build_dependency_characterization_controller_program_created=false
build_dependency_characterization_child_program_created=false
build_dependency_characterization_program_bundle_created=false
build_dependency_characterization_synthetic_execution_authorized=false
build_dependency_characterization_bundle_review_receipt_created=false
build_dependency_characterization_fresh_activation_version=v5
build_dependency_characterization_fresh_activation_profile_defined=true
build_dependency_characterization_fresh_activation_created=false
build_dependency_characterization_authorized=false
build_dependency_source_read_authorized=false
build_dependency_script_execution_authorized=false
ambient_build_substitution_authorized=false
generic_path_resolution_authorized=false
inherited_last_exit_code_success_authorized=false
manifest_transition_36_to_37_status=implemented_and_preserved
manifest_transition_37_to_37_0b3_to_d8ef_status=implemented_and_valid
manifest_transition_37_to_37_d8ef_to_85ba_status=implemented_and_valid
manifest_transition_37_to_37_db32_to_8b8d_status=implemented_and_valid
manifest_transition_37_to_37_8b8d_to_48d_status=implemented_and_valid
manifest_bound_v5_contract_sha256=48d7c28599ed6a26b48749eaae96ec51dd38fff680104b3c059b29da3cff51be
manifest_bound_amendment_sha256=9d84e547d7b71b06c3f04f6bfdd114763eb6ca3134fa627429e1f906d945ad5d
manifest_bound_static_preflight_sha256=95599612548ba08beff8c4c10377815d0aa80b203fe0e3115ccf0ea7d911e6af
manifest_bound_sha256=5f95acc7c29be1d332f893ce518f8e1bfe0900e38394821d70d51ff637f5f8fc
current_manifest_count_transition=37_to_37
current_manifest_digest_rebind_required=true
manifest_rebind_recommended_now=false
manifest_rebind_recommendation_status=pending_independent_contract_review
manifest_rebind_authorized=false
stable_count_review_model_status=contract_defined_not_implemented
stable_count_review_model_authorized=false
contract_semantics_accepted=false
manifest_integration_complete=false
static_preflight_digest_schema_status=prior_revision_accepted_current_revision_not_executed
static_preflight_artifact_created=false
static_preflight_execution_authorized=false
candidate_preparation_activation_eligible=false
candidate_build_recipe_execution_authorized=false
candidate_test_execution_authorized=false
candidate_disposable_output_creation_authorized=false
candidate_staging_root_creation_authorized=false
candidate_preflight_packet_creation_authorized=false
candidate_review_root_creation_authorized=false
candidate_independent_review_read_authorized=false
independent_review_receipt_creation_authorized=false
candidate_staging_cleanup_authorized=false
candidate_correction_authorized=false
final_seal_activation_created=false
final_seal_authorized=false
package_source_read_authorized=false
source_repository_access_authorized=false
network_access_authorized=false
external_write_authorized=false
source_copy_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_creation_authorized=false
handoff_publication_authorized=false
publication_authorized=false
failure_artifact_creation_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
external_mutation_authorized=false
live_ready=false
current_v4_reuse_authorized=false
finding_resolution_claimed=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
release_readiness_claimed=false
production_readiness_claimed=false
```

The next role is Codex E for independent contract review of this exact file.
Codex E must verify the rejected v4 activation projection, historical v1
receipt boundary, exact two-program scope, controller/child ownership split,
three-row source adapter, parent-only complete-result entrypoint, child and
public result schemas, 27-field outer handoff, 18-field bundle, deterministic
status and outer-failure derivation,
canonical self-digests, no-echo and zero-residue rules, all 36 core cases, all
37 adapter cases, 29-field v3 bundle receipt, fresh-v5 activation requirement,
recipe-v1 retirement, recipe-v2 version requirement, preserved recipe bytes and
two-path package envelope, current manifest blocker, and all false-authority
fields.

An accepted semantic review authorizes no source read, characterization,
manifest edit, activation, implementation, build, or package work. It routes
first to a separate 37-to-37 manifest-rebind decision and independent review.
Only after that gate passes may the owner authorize a synthetic-only
two-program implementation and independent review. Only after Codex E accepts
the exact controller, child, bundle, handoff projection, 73 outcomes, and v3
receipt may the owner
construct one exact fresh v5 activation for the three-row read-only
characterization. Its accepted public-safe v3 result returns to Codex B to
define recipe v2 or a proven script-envelope change. A fresh candidate
activation remains forbidden until the resulting contract, recipe, review,
manifest, static preflight, and activation profile are all current. Any attempt
to reuse any prior activation, retry recipe v1, treat the historical single-row
receipt as bundle evidence, adopt ambient evidence, treat process exit as
physical erasure, emit partial rows, skip either synthetic matrix, or expand
source without those gates fails closed.
