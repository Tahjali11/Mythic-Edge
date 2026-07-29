# External-Isolation Broker v4 Corrective Successor Contract

Status: `contract_candidate_manifest_integration_blocked`

Contract ID:
`mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1`

## Decision and scope

The reviewed v3 contract and frozen v3 package remain immutable historical
lineage. The v3 package is not accepted because independent review reported:

```text
EIB-PKG-V3-E-001=valid_unknown_reconciliation_does_not_advance_timestamp_floor
EIB-PKG-V3-E-002=failure_projection_accepts_impossible_code_lifecycle_combinations
EIB-PKG-V3-E-003=absolute_path_shaped_owner_activation_reference_passes_no_echo_validation
```

This contract defines a separate v4 package candidate that may correct only
those findings after independent contract review, manifest integration, and a
new exact owner activation. It does not amend v3 in place, reuse its consumed
activation, accept its package, or authorize implementation now.

The parent v3 contract remains controlling except where this contract gives a
stricter v4 rule. A conflict, omission, or need to weaken a parent rule stops
before v4 root creation and routes to Codex B.

## Authority and non-claims

This artifact is contract-only. It authorizes no package read, source copy,
edit, build, test, inventory, handoff, publication, installation, service
mutation, canary, source-repository access, stage advancement, or live use.
The reviewed v3 package remains uninstalled, non-reusable, and unchanged.

The three findings are contract inputs, not claims that a correction exists or
works. This contract makes no correctness, security, privacy, readiness,
release, deployment, production, or live-operation claim.

## Exact lineage binding

The v4 predecessor bindings are:

```text
parent_contract_id=mythic_edge_role_pool_external_isolation_broker_v3_corrective_successor.v1
parent_contract_path=references/external-isolation-broker-v3-corrective-successor.md
parent_contract_sha256=44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55
rejected_v3_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v3
rejected_v3_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v3
rejected_v3_inventory_filename=package-inventory.json
rejected_v3_inventory_file_sha256=97665659233768d0c61c01045c2a93e3f9ca1e41d1a644962d8d543fbce80cc9
rejected_v3_inventory_root_digest=feb1976a2b2cdb1fcb8be886efc68b586ddfea9496792637041160e7eee03bd0
rejected_v3_inventory_file_count=51
rejected_v3_inventory_total_length_bytes=6097770
rejected_v3_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v3.implementation-handoff.v3.json
rejected_v3_handoff_file_sha256=538ed58d2da7b901dd7b9e795a5516f34be900044a069c14a32e7d909d3589a0
rejected_v3_handoff_root_digest=72183084e0a738358d0bf42c07374fddb3a66b7ba8252df9de51f98fbdda11c2
rejected_v3_review_status=contract_findings_block_acceptance
rejected_v3_package_bytes_unchanged=true
rejected_v3_installed=false
rejected_v3_live_ready=false
rejected_v3_reuse_authorized=false
```

All values are one indivisible binding. Any mismatch, missing file, changed
length, changed row, unreadable metadata, reparse point, or path-identity
ambiguity blocks v4. The v3 root and handoff must not be edited, deleted,
renamed, repaired, installed, executed, or used as a resumable workspace.

## v4 identity and versioning

The v4 identities are closed:

```text
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v4
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v4
package_parent_resolver=windows_current_owner_desktop_mtg_resources.v1
package_parent_suffix=MTG Resources
package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4
inventory_schema=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v4
inventory_filename=package-inventory.json
inventory_staging_filename=package-inventory.json.tmp
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v4
implementation_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4.implementation-handoff.v4.json
implementation_handoff_staging_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v4.implementation-handoff.v4.json.tmp
publication_failure_schema=mythic_edge_role_pool_package_publication_failure.v2
broker_protocol_id=mythic_edge_role_pool_windows_isolation_broker.v1
verifier_protocol_id=mythic_edge_role_pool_windows_isolation_verifier_service.v1
receipt_chain_schema=mythic_edge_role_pool_broker_receipt_chain.v1
reconciliation_receipt_schema=mythic_edge_role_pool_broker_reconciliation_receipt.v1
```

Package, inventory, handoff, authority-profile, and publication-failure
versions advance because their identity, lineage, validation, or field rules
change. Broker, verifier, receipt-chain, and reconciliation-receipt wire
schemas remain v1 because their serialized fields and cryptographic roots do
not change. The timestamp-floor correction is coordinator validation state,
not a receipt-byte change. A later wire-field change requires a new receipt
schema and contract.

The parent resolver and all v3 ordinary-file, fixed-volume, owner-SID,
reparse-point, no-discovery, no-overwrite, no-echo, and symbolic-output rules
remain unchanged.

## Source-copy and edit envelope

A later activated v4 attempt starts only from an absent v4 root. It validates
the exact v3 inventory and copies the 46 inventory rows other than these five
generated outputs:

```text
dist/MythicEdgeRolePoolIsolationBroker.exe
dist/MythicEdgeRolePoolVerifierActivationHost.exe
dist/MythicEdgeRolePoolVerifierBootstrap.exe
dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe
dist/MythicEdgeRolePoolVerifierService.exe
```

Copy order is ordinal by relative path. Each destination is exclusively
created, reread, and hash-compared before any edit. The future edit envelope is
exactly:

```text
client/windows_broker_client.py
tools/publish_implementation_candidate.py
tests/test_windows_broker_client.py
tests/test_implementation_handoff.py
```

The two implementation files may change only for the three corrections below.
The two test files may change only for the required focused tests. The other 42
source rows must remain exact-byte copies of v3. No new source path, renamed
path, removed path, broad cleanup, dependency, protocol change, Role Pool edit,
or source-repository read is allowed. All five executables and the inventory
must be rebuilt as fresh v4 outputs; no v3 generated output may be copied.

## EIB-PKG-V3-E-001 timestamp-floor correction

The parent launch attempt already owns one in-memory timestamp-ordering floor.
V4 must preserve and extend that same floor; it must not create an empty second
floor, reset the parent floor, or derive a replacement from caller input. Under
the parent per-attempt lock, the coordinator represents the preserved floor as:

```text
reconciliation_floor_observed_at
reconciliation_floor_receipt_digest
```

Before parsing a candidate reconciliation receipt, classify one atomic parent
floor snapshot under the parent per-attempt lock. The closed chain states are:

```text
proven_empty
accepted_receipt_present
unavailable_or_contradictory
```

`proven_empty` requires positive parent-owned proof that no reservation,
boundary-ready, start, terminal, abort, or prior reconciliation receipt was
accepted. `accepted_receipt_present` requires at least one accepted receipt and
one uniquely owning latest floor receipt. Reader failure, lock failure,
conflicting accepted-receipt order, multiple owners for one floor, incomplete
state, or an unprovable empty claim is `unavailable_or_contradictory`. These
states are derived from parent state and cannot be caller supplied.

The closed timestamp states are:

```text
null
valid_populated
invalid_populated
unavailable
```

The closed digest states are:

```text
null
valid_owning
valid_non_owning
invalid_populated
unavailable
```

`null` is an explicit parent-owned null, not an absent read. `valid_populated`
is one canonical UTC timestamp that equals the parent chain's current floor.
`valid_owning` is lowercase 64-character SHA-256 that equals the validated
canonical digest of the unique accepted receipt whose normalized timestamp
owns that floor. `valid_non_owning` has valid digest shape but belongs to a
different receipt or cannot be bound to the floor owner. `invalid_populated`
is present but fails the required shape or validation. `unavailable` means the
parent accessor cannot return or prove the value and must never be coerced to
`null`.

The following 20-row table is exhaustive for the timestamp/digest Cartesian
product. Its three result columns define all 60 parent-state combinations:

| timestamp state | digest state | `proven_empty` | `accepted_receipt_present` | `unavailable_or_contradictory` |
| --- | --- | --- | --- | --- |
| `null` | `null` | `accept_empty_parent_floor` | `reject_parent_floor_timestamp_missing` | `reject_parent_floor_chain_unavailable` |
| `null` | `valid_owning` | `reject_empty_chain_digest_not_null` | `reject_parent_floor_timestamp_missing` | `reject_parent_floor_chain_unavailable` |
| `null` | `valid_non_owning` | `reject_empty_chain_digest_not_null` | `reject_parent_floor_timestamp_missing` | `reject_parent_floor_chain_unavailable` |
| `null` | `invalid_populated` | `reject_empty_chain_digest_not_null` | `reject_parent_floor_timestamp_missing` | `reject_parent_floor_chain_unavailable` |
| `null` | `unavailable` | `reject_empty_chain_digest_not_null` | `reject_parent_floor_timestamp_missing` | `reject_parent_floor_chain_unavailable` |
| `valid_populated` | `null` | `reject_empty_chain_timestamp_not_null` | `reject_parent_floor_digest_missing` | `reject_parent_floor_chain_unavailable` |
| `valid_populated` | `valid_owning` | `reject_empty_chain_timestamp_not_null` | `accept_populated_parent_floor` | `reject_parent_floor_chain_unavailable` |
| `valid_populated` | `valid_non_owning` | `reject_empty_chain_timestamp_not_null` | `reject_parent_floor_digest_non_owning` | `reject_parent_floor_chain_unavailable` |
| `valid_populated` | `invalid_populated` | `reject_empty_chain_timestamp_not_null` | `reject_parent_floor_digest_invalid` | `reject_parent_floor_chain_unavailable` |
| `valid_populated` | `unavailable` | `reject_empty_chain_timestamp_not_null` | `reject_parent_floor_digest_unavailable` | `reject_parent_floor_chain_unavailable` |
| `invalid_populated` | `null` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_chain_unavailable` |
| `invalid_populated` | `valid_owning` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_chain_unavailable` |
| `invalid_populated` | `valid_non_owning` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_chain_unavailable` |
| `invalid_populated` | `invalid_populated` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_chain_unavailable` |
| `invalid_populated` | `unavailable` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_timestamp_invalid` | `reject_parent_floor_chain_unavailable` |
| `unavailable` | `null` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_chain_unavailable` |
| `unavailable` | `valid_owning` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_chain_unavailable` |
| `unavailable` | `valid_non_owning` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_chain_unavailable` |
| `unavailable` | `invalid_populated` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_chain_unavailable` |
| `unavailable` | `unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_timestamp_unavailable` | `reject_parent_floor_chain_unavailable` |

Only `accept_empty_parent_floor` and `accept_populated_parent_floor` permit
reconciliation. The first atomically initializes both represented values to
JSON null. The second atomically copies the exact parent floor timestamp and
its uniquely owning receipt digest. Every `reject_*` result returns the single
public error `parent_launch_attempt_floor_unavailable`, projects public state
`unknown`, performs no candidate-receipt validation, creates no replacement
floor, and leaves the complete parent launch-attempt state unchanged. The
specific `reject_*` literal is ephemeral test classification only and must not
be serialized, logged, or echoed.

The parent state is comparison authority; a reconciliation request cannot
omit, replace, refresh, lower, or clear it. The values are updated only under
the same per-attempt lock used to validate and return reconciliation results.
They are not durable state, process authority, or evidence of launch state.

A `valid reconciliation receipt` is a receipt that passes every parent check:
schema, domain, algorithm, pinned key ID, verifier identity, evidence source,
launch ID, request digest, expected epoch, timestamp shape, state/digest matrix,
self-digest, and HMAC. A cryptographically valid receipt whose state is
`unknown` and whose three state digests are null is valid. Malformed,
mismatched, unverifiable, cross-epoch, or contradictory input may project a
public `unknown` outcome, but it is not a valid receipt.

After all non-time checks pass, timestamp handling is exact:

| Current floor | Candidate receipt | Result |
| --- | --- | --- |
| both values null after proving the parent has no accepted receipt | any valid receipt | accept; set both floor values from the receipt |
| populated | candidate `observed_at` later than the floor | accept; atomically replace both floor values, including for valid `unknown` |
| populated | candidate timestamp equal and candidate digest equal | accept as an idempotent replay; floor is unchanged |
| populated | candidate timestamp equal and candidate digest different | reject as `reconciliation_timestamp_collision`; floor is unchanged; public state is `unknown` |
| populated | candidate timestamp earlier | reject as `reconciliation_timestamp_regression`; floor is unchanged; public state is `unknown` |

A valid result must not be returned before its required floor update commits in
memory. If cancellation, exception, or lock failure prevents the update, return
only `reconciliation_floor_update_failed`, preserve the prior floor, and do not
represent the receipt as accepted. Invalid receipts never advance the floor.
A valid `unknown` advances evidence freshness only; it does not advance or
replace process lifecycle state.

## EIB-PKG-V3-E-002 closed failure projection

The v4 public failure projection has exactly these keys:

```text
schema_version
contract_id
contract_sha256
parent_contract_sha256
package_id
handoff_schema
owner_activation_ref
owner_activation_sha256
operation_path
failure_phase
external_handoff_publication_status
inventory_status
inventory_file_sha256
inventory_root_digest
source_copy_status
baseline_copied_paths
failed_source_copy_paths
carried_forward_created_paths
failed_created_source_paths
source_repository_access_status
sanitized_error_code
successor_terminal_status
successor_reuse_authorized
installation_performed
service_mutation_performed
canary_performed
external_mutation_performed
stage_advancement_claimed
finding_resolution_claimed
live_ready
next_role
```

Fixed values are:

```text
schema_version=mythic_edge_role_pool_package_publication_failure.v2
contract_id=mythic_edge_role_pool_external_isolation_broker_v4_corrective_successor.v1
parent_contract_sha256=44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v4
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v4
successor_reuse_authorized=false
installation_performed=false
service_mutation_performed=false
canary_performed=false
external_mutation_performed=false
stage_advancement_claimed=false
finding_resolution_claimed=false
live_ready=false
next_role=codex_b_contract_reconciliation
```

Every non-fixed lifecycle field must match exactly one row below. No cell is a
wildcard. `failed_incomplete` requires the parent four-array incomplete-copy
derivation; `complete` requires its complete-copy derivation.

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
| `candidate_inventory_then_handoff` | `handoff_staging_write_failed` | `handoff_staging` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `candidate_pre_inventory_staging_cleanup_failed` | `pre_inventory_staging_cleanup` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publish_absent` | `inventory_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publish_collision` | `inventory_publication` | `failed_pre_inventory` | `not_created` | `failed_before_inventory` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publication_state_unknown` | `inventory_publication` | `unknown_after_publish_attempt` | `unknown` | `publication_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_publication_retry_exhausted` | `inventory_publication` | `unknown_after_publish_attempt` | `unknown` | `publication_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `inventory_staging_cleanup_failed` | `inventory_staging_cleanup` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publish_absent` | `handoff_publication` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publish_collision` | `handoff_publication` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_unpublished` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publication_state_unknown` | `handoff_publication` | `unknown_after_publish_attempt` | `frozen_candidate` | `frozen_candidate_handoff_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_publication_retry_exhausted` | `handoff_publication` | `unknown_after_publish_attempt` | `frozen_candidate` | `frozen_candidate_handoff_state_unknown` | `complete` |
| `candidate_inventory_then_handoff` | `handoff_staging_cleanup_failed` | `handoff_staging_cleanup` | `failed_post_inventory` | `frozen_candidate` | `frozen_candidate_handoff_cleanup_failed` | `complete` |

`frozen_candidate` requires both inventory digest fields to equal the validated
v4 final inventory values. `not_created` and `unknown` require both strings to
be `none`. A projection must be rejected before rendering if it matches zero or
multiple rows, uses an old generic v3 code, has contradictory arrays or digest
fields, or carries an unknown key. The validator must not repair, coerce, or
select the nearest row.

## EIB-PKG-V3-E-003 symbolic owner-activation reference

The private location or transport used to obtain owner approval is a separate
ephemeral activation input. It is never an `owner_activation_ref`, never enters
canonical public bytes, and is discarded before inventory, handoff, projection,
diagnostic, log, assertion, or exception construction.

Every v4 public artifact accepts `owner_activation_ref` only when it matches:

```text
^owner_activation_v1_[0-9a-f]{32}$
```

The owner must supply that public-safe token inside the exact approval. It is
opaque ASCII and is not derived from a path, filename, URI, command, approval
text, environment value, or process output. Validation is ordinal and
case-sensitive. Before any path API, normalization, serialization, or hashing,
reject a value containing whitespace, a control character, `/`, `\\`, `..`,
`://`, `%`, `~`, a drive prefix, UNC prefix, device prefix, URI scheme, or any
character outside the exact grammar. The fixed prefix is an opaque label, not
a URI scheme. Do not resolve, normalize, basename, or redact an invalid value
into acceptance.

`owner_activation_sha256` is independently required lowercase 64-character
hex and binds the exact private approval bytes. It does not make an invalid
reference valid. The only public error for reference-shape failure is
`owner_activation_ref_invalid_symbolic_shape`; it must not include the supplied
value, approval text, source location, path fragment, or exception.

## v4 inventory and handoff requirements

The v4 inventory and handoff inherit the v3 canonical JSON, duplicate-key,
unknown-key, finite-number, self-digest, ordinary-file, and no-echo rules. Their
exact key sets are the corresponding v3 sets with:

1. all v4 schema, contract, package, basename, and authority-profile values
   above;
2. the five shared `rejected_v2_*` lineage fields replaced by
   `rejected_v3_package_id`, `rejected_v3_inventory_file_sha256`,
   `rejected_v3_inventory_root_digest`, `rejected_v3_handoff_file_sha256`, and
   `rejected_v3_handoff_root_digest`;
3. in the handoff only, `rejected_v2_reuse_authorized` replaced by
   `rejected_v3_reuse_authorized=false`;
4. `rejected_v3_review_status` added immediately after those lineage fields;
5. the failure projection schema bound to v2; and
6. `owner_activation_ref` validated by the exact symbolic grammar above.

The v4 inventory has 51 file rows: 46 source rows and five fresh generated
outputs. It preserves the inherited lineage categories exactly as
`carry_forward_baseline_row_count=37` and
`carry_forward_created_row_count=9`; those values classify the predecessor
rows and do not authorize newly created v4 source. `modified_carry_forward_paths`
is exactly a nonempty subset of the four-path edit envelope, and
`unchanged_carry_forward_paths` is the exact remaining source-row set. Created,
removed, unexpected, and changed Role Pool paths are empty.

Candidate blockers are exactly:

```text
independent_review_pending
installation_not_authorized
stage4_canary_not_authorized
```

The candidate handoff remains
`candidate_ready_for_independent_review`, routes to
`codex_e_independent_review`, and keeps every effect, claim, reuse, and live
boolean false. A blocked handoff or publication projection routes to Codex B.

## Validation matrix

Future implementation validation must include, at minimum:

### Timestamp floor

- test the complete 3-by-4-by-5 Cartesian product: exactly 60 parent-floor
  combinations, with exactly the two acceptance outcomes in the table;
- for every one of the 58 rejection combinations, assert the fixed public error
  and `unknown` projection, no candidate-receipt validation, no replacement
  floor creation, and field-for-field unchanged parent state;
- prove `valid_non_owning` includes a correctly shaped digest from another
  accepted receipt and cannot become `valid_owning` through caller assertion;
- prove unavailable timestamp or digest input is distinct from explicit null
  and is never normalized, defaulted, or reset;
- an attempt proven to have no accepted parent receipt accepts only null/null,
  after which a first valid `unknown` initializes both floor values;
- an accepted parent receipt accepts only a valid populated timestamp plus its
  exact uniquely owning validated receipt digest;
- a first reconciliation older than the populated parent floor is rejected;
- later valid `unknown` advances both floor values;
- valid known state followed by later valid `unknown` advances the floor but
  not lifecycle state;
- earlier timestamp, equal timestamp with different digest, invalid HMAC,
  wrong epoch, malformed matrix, and cross-request input do not advance it;
- equal timestamp with identical digest is idempotent;
- concurrent receipts serialize under the per-attempt lock; and
- a returned valid result proves its required floor update completed.

### Failure projection

- one positive test for every matrix row;
- for every row, mutate each lifecycle field separately and require rejection;
- reject all old generic v3 ambiguity codes;
- reject frozen inventory without exact digests and non-frozen inventory with
  digest values;
- reject complete/incomplete source-copy array contradictions;
- reject unknown keys, multiple-row matches, coercion, and inferred repair; and
- prove all errors remain symbolic and no-echo.

### Owner activation reference

- accept exact lowercase symbolic tokens only;
- reject Windows drive, UNC, device, POSIX absolute, relative traversal,
  `file:` URI, network URI, percent-encoded, whitespace, control, uppercase,
  overlong, short, empty, and non-ASCII forms;
- prove invalid values never reach path APIs and never appear in output,
  exceptions, snapshots, or test failure messages; and
- independently validate the approval digest without reading approval text
  into any public artifact.

### Package and Role Pool

- validate every v3 lineage pin and all 51 inventory rows;
- prove only the four edit-envelope paths changed among source rows;
- run focused source tests before build;
- run clean managed build, native bootstrap build, binary self-tests, and full
  package validation with zero failures, errors, or skips;
- rebuild and inventory all five outputs exactly once;
- validate v4 inventory and handoff canonical digests;
- run the Role Pool focused tests and full offline release gate; and
- preserve the explicit `NOT LIVE-READY` conclusion.

Raw command output, source text, approval text, absolute paths, exceptions,
tracebacks, keys, credentials, and private activation inputs must not appear in
committed or public-safe evidence.

## Current manifest-integration blocker

Adding this v4 contract changes the installed Role Pool manifest from 35 to 36
files. Current Stage-3 manifest authority binds only the reviewed v3 contract
and does not authorize or recognize this new path. This Codex B thread cannot
edit the validator, tests, manifest policy, or Stage-3 amendment.

Therefore the expected full offline gate may fail only for the unrecognized v4
path while structural validation remains clean. That known lifecycle failure
is not a package failure and must not be suppressed. At these contract bytes,
the gate runs 298 tests and returns 27 Stage-3 errors whose first proven cause
is `current manifest file count is not 35`; any different failure is outside
this known blocker and routes to Codex B. The owner must separately authorize
either:

1. a narrow manifest-transition amendment binding this exact v4 path and an
   independently accepted digest; or
2. a different exact authority location with a new digest and fresh review.

Until that decision, all remain:

```text
manifest_integration_status=blocked_owner_decision_required
contract_acceptance_ready=false
ready_for_codex_c=false
```

## False-authority fields and next role

```text
ready_for_codex_c=false
implementation_authorized=false
package_source_read_authorized=false
source_copy_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_publication_authorized=false
installation_authorized=false
service_mutation_authorized=false
canary_authorized=false
stage_advancement_authorized=false
live_ready=false
finding_resolution_claimed=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
production_readiness_claimed=false
```

Codex E must independently review this exact contract, the three correction
matrices, v3 metadata pins, versioning, no-echo rules, manifest blocker, and all
false-authority fields. Review creates no implementation or manifest authority.
Any required fifth edit path, source read, schema relaxation, old package
mutation, or lifecycle ambiguity routes back to Codex B.
