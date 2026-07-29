# External-Isolation Broker v3 Corrective Successor Contract

Status: `contract_candidate_manifest_integration_blocked`

Contract ID:
`mythic_edge_role_pool_external_isolation_broker_v3_corrective_successor.v1`

Risk tier: high

## Decision and findings

This additive contract resolves two blocking findings against the rejected v2
implementation candidate:

- `EIB-PKG-IMPL-E-001`: reconciliation could classify verifier restart or
  state loss as `definitive_not_started`, and the receipt comparison did not
  pin every required attestation field;
- `EIB-PKG-IMPL-E-002`: source-copy and publication failures did not have a
  mechanically complete, bounded, public-safe terminal projection.

The reviewed parent contract remains immutable at:

```text
parent_contract_id=mythic_edge_role_pool_external_isolation_broker.v1
parent_contract_path=references/external-isolation-broker.md
parent_contract_sha256=b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa
```

This document supplements that parent only for a possible v3 package attempt.
It does not rewrite the historical v2 authority or repair the rejected v2
package in place. Where this document is more restrictive for v3, this document
controls that future attempt. All other parent requirements remain in force.
Any contradiction not expressly resolved here fails closed and routes to Codex
B and the owner.

The v2 package contains 46 non-generated rows: the 37 historical baseline rows
required by the parent contract and nine source rows created during v2. The v3
copy protocol therefore preserves the exact 37-row baseline projection and
adds a separate exact nine-row created-source projection. Neither group may be
silently omitted.

The runtime broker, verifier, request, receipt, and IPC protocols remain v1.
The corrections are implementable within their existing closed fields. The
package authority, inventory, and handoff change semantics and therefore move
to v3.

## Authority boundary

This contract is docs-only. Its creation or acceptance does not authorize
Codex C, copying, package creation, builds, tests that execute package code,
inventory generation, publication, installation, service mutation, source
repository access, Stage-4 execution, canary execution, stage advancement, or
live use.

Independent Codex E review may begin against the exact bytes of this artifact.
Even an accepted review leaves `ready_for_codex_c=false`. A later owner
activation must independently name the accepted contract digest and the exact
bounded operation before any implementation work starts.

Independent review may assess this contract's semantics now, but it cannot
classify the installed Role Pool as validation-clean until the manifest
integration blocker below is resolved under separate authority.

## Exact identities and paths

The v3 identities are closed:

```text
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v3
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v3
package_parent_resolver=windows_current_owner_desktop_mtg_resources.v1
package_parent_suffix=MTG Resources
package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v3
inventory_schema=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v3
inventory_filename=package-inventory.json
inventory_staging_filename=package-inventory.json.tmp
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v3
implementation_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v3.implementation-handoff.v3.json
implementation_handoff_staging_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v3.implementation-handoff.v3.json.tmp
broker_protocol_id=mythic_edge_role_pool_windows_isolation_broker.v1
verifier_protocol_id=mythic_edge_role_pool_windows_isolation_verifier_service.v1
receipt_chain_schema=mythic_edge_role_pool_broker_receipt_chain.v1
reconciliation_receipt_schema=mythic_edge_role_pool_broker_reconciliation_receipt.v1
```

The parent resolver, reparse-point refusal, owner-SID check, fixed-local-volume
check, no-discovery rule, and symbolic public-output rule are inherited
unchanged. Absolute paths are private activation inputs. Public artifacts use
only the basenames above and symbolic contract paths.

## Frozen predecessor lineage

The rejected v2 candidate is immutable historical review evidence:

```text
rejected_v2_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
rejected_v2_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2
rejected_v2_inventory_filename=package-inventory.json
rejected_v2_inventory_file_sha256=aa9cfb5d37466d2bf427d5da751456395e2db8b2d1131f55425fb8f61b8c890c
rejected_v2_inventory_root_digest=78a636f0a7995dd2780897631a14ed4e15b44a7eceb8057e1daf7177aeeadc8f
rejected_v2_inventory_file_count=51
rejected_v2_inventory_total_length_bytes=6055115
rejected_v2_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2.implementation-handoff.v2.json
rejected_v2_handoff_file_sha256=f440dae0e42a75ad704dc3e1e7bc4cd0b77aba21c37d7b33d1c19476e4d7c8fe
rejected_v2_handoff_root_digest=ae8365efff2a973063cb15709f31c9115ab38dfdae9a6dad2047deadd4126bc8
rejected_v2_review_status=rejected_blocking_contract_findings
rejected_v2_installed=false
rejected_v2_live_ready=false
rejected_v2_reuse_authorized=false
```

The v2 root must not be edited, deleted, renamed, inventoried again, repaired,
installed, executed, or treated as a resumable workspace. Exact-byte
carry-forward under this contract means creation of independent ordinary-file
copies in a new absent v3 root after all v2 pins validate. It does not mean
reuse, adoption, or continuation of the v2 package.

## Exact-byte carry-forward manifest

The following 46 rows are the complete permitted non-`dist/` input. A future
activated implementation may read only these exact v2 files for bounded copy
and digest verification. Path, byte length, and SHA-256 must all match before a
row is accepted. No wildcard, recursive discovery, neighboring-file access, or
best-match substitution is allowed.

| class | path | length_bytes | sha256 |
|---|---|---:|---|
| historical_baseline | `.gitignore` | 65 | `5a517a75a644ce3b540570de632fac3007ac2171ec3263d1565b31f6b498fc0a` |
| historical_baseline | `bootstrap/go.mod` | 67 | `5826f5b60dd4d2bf1a0618b0a5946726579766e2f6f8f17a5ca4e58aa70d3b09` |
| historical_baseline | `bootstrap/inventory.go` | 8376 | `d78ddbc2381d54ad9a3e39c80cd8c0a55cc777eee0d1923e86b6481bb076b45d` |
| historical_baseline | `bootstrap/main.go` | 24584 | `a215b01137a90188639ca2374fe847630f07ecf0cc52b49f920ae3d420099898` |
| historical_baseline | `bootstrap/main_test.go` | 10283 | `c97c0fab9868ee33b97a194194ae143132c31131ab8dcb9647f57bde44968596` |
| historical_baseline | `bootstrap/windows_native.go` | 32098 | `c22aed939e69af340afe1e7152414bb7213c953ddbeeaf41c051d0512e9d0dc6` |
| historical_baseline | `client/__init__.py` | 479 | `9043f35bb080b9dbe2566ac19c2935324f12f1eabaefd653d18231e826bb6526` |
| v2_created | `client/windows_broker_client.py` | 36916 | `53ea7048e6adf65cbad08a2ff5e309ba4e64fa660c1e2d799fb9edd0627fc65e` |
| historical_baseline | `client/windows_verifier_client.py` | 56718 | `a7541576499036a7bc98baa142772d2a107bd92ffa7320110f7b7cd497e64b36` |
| v2_created | `docs/broker-service-contract.md` | 3630 | `2c864cb03abda716850ce7ceff607e48308d8f0f871d4882ad3c33acb8b897f2` |
| historical_baseline | `docs/verifier-service-contract.md` | 28377 | `03160342eac73e184d14f902263a3a37d63fff21c3c7dd3fdc924127d3e27aee` |
| historical_baseline | `README.md` | 14316 | `6e910b6c1807e81a8499b859f7cc61f2723b33605457183c4c798365db042c03` |
| historical_baseline | `scripts/audit-installation.ps1` | 3227 | `96e2d94cd3e9da0b879eb2e3b4adf44a45442dc629f19b3c0269cd4d821ba4ac` |
| historical_baseline | `scripts/build.ps1` | 7831 | `5238274174a21eb83a3ff09b7ee0c87adb5d9db345c0a5a02065ad48c041a3c3` |
| historical_baseline | `scripts/build-native-bootstrap.ps1` | 15483 | `e75fda45f9e4070b7b7d651799a986bfd0da3a1b03f467ee2ae5f48b9e9c59cd` |
| historical_baseline | `scripts/diagnostic-exit.ps1` | 4302 | `99d7b64de51d7cff4f8fffa32ec94a93c8b180dddd6392c86afa2add5f420f31` |
| historical_baseline | `scripts/install.ps1` | 8376 | `48bfda5d042df8acc6e1d5dc8d4a7bc9e9a15b40b2462a8f483d02c3f0ea089a` |
| historical_baseline | `scripts/test-adversarial.ps1` | 3488 | `1971be102ac0ad41192898e1b4fb09b35793c0bd2c1e24b9bfba1a676dcd203a` |
| historical_baseline | `scripts/uninstall.ps1` | 3433 | `13764ef618548268aa0778d8f0eb26bd5e47b7d3ba59ffef93f5a25ab59706c0` |
| historical_baseline | `src/build-activation-host.ps1` | 2078 | `7ade15110bfccaef19fb0cdcfa49ae2e8a4733614cb096e2aab693f2fe2f65ba` |
| v2_created | `src/MythicEdgeRolePoolBrokerContracts.cs` | 68657 | `f0b8d6f3f1775def54e5652ad6878e464f373c33abf1d04986ba172332e237f2` |
| v2_created | `src/MythicEdgeRolePoolBrokerVerifierIssuance.cs` | 53555 | `57b64434ca53b152dbd2f64ab65cd303030f55a51dab07d8c0f4671339320dac` |
| v2_created | `src/MythicEdgeRolePoolIsolationBroker.cs` | 108917 | `c4335ff47c346b19dba0ee9ba322327e3b0e8ff9fc3bf7a46705b66226d75174` |
| historical_baseline | `src/MythicEdgeRolePoolVerifierActivationContracts.cs` | 43120 | `034e79ab0fa65039fb93b412dfb82f86a0c3581938f99ecf4db87106a8348e96` |
| historical_baseline | `src/MythicEdgeRolePoolVerifierActivationHost.cs` | 116346 | `a46f52f758c19e8c6ac435cd7555550bbfba3f0f7e4df4da4d6dac7182431329` |
| historical_baseline | `src/MythicEdgeRolePoolVerifierActivationSystemState.cs` | 62477 | `5575d14175bd199ac955ed559e4814a41541b9f438c7f6d06f06c72440c51311` |
| historical_baseline | `src/MythicEdgeRolePoolVerifierActivationWindowsNative.cs` | 114164 | `bc71c371784abaef3ea14c795277ccbc46a1ce61642d86dadd5cdb11f264ca85` |
| historical_baseline | `src/MythicEdgeRolePoolVerifierService.cs` | 146431 | `f404beb681fd3b84199d20bbbe96bd528d6e6f26a7b59370d142b609ba3f747c` |
| historical_baseline | `tests/__init__.py` | 69 | `fd38ac84f43edaafc96e17d7210c56e8b40774339c2ca06128ea8ee30f29cd85` |
| historical_baseline | `tests/test_activation_contracts.py` | 16836 | `10e807878183b4361af4538b203ac0908bb6e29810a12f0ff261a11f004e4d57` |
| historical_baseline | `tests/test_activation_host_runtime.py` | 47069 | `13fcc484ebe52363ab546023294306f482b3e8010eacdfb95b21c93e27c36b95` |
| v2_created | `tests/test_broker_service_contracts.py` | 9421 | `9c77c2316f4603f79f34a002406578ada481f0a6c036d22527996644651288dd` |
| v2_created | `tests/test_implementation_handoff.py` | 6587 | `eaa069f4199326684de1c71198d7a2f5c5c57a2eeac262d2fd89d9071d108bfd` |
| historical_baseline | `tests/test_native_bootstrap_contracts.py` | 18713 | `a29470f215194f6129400a32bbf944bc96fcb12741e3e774b4b05056113558da` |
| historical_baseline | `tests/test_package_inventory.py` | 5675 | `bbe439b0e5275411ae0ae801e8c0635e17faf520a10c87d865614f8a73c1ccc9` |
| historical_baseline | `tests/test_powershell_contracts.py` | 18606 | `4ca85fdd8069a6f25503a0d9b548252db3cd1c5ae17bdb110e09a19f928706ab` |
| historical_baseline | `tests/test_service_contracts.py` | 8976 | `14a83767067dfa3a49e902a42c80d78d38c07afd051f30be7d32371e50845aee` |
| historical_baseline | `tests/test_trust_manifest_tool.py` | 5429 | `a4974c8ccf92a6820449642d03c3a257d62ee4405e38eaf2424deed3e165e902` |
| v2_created | `tests/test_windows_broker_client.py` | 16540 | `00cb03fe4a620e3ee31cc0c6ee59b0767556b6fc6a282626c41b003483c57639` |
| historical_baseline | `tests/test_windows_verifier_client.py` | 40064 | `a685ec87357138be10c0ef1ec1ff382fd83d04d44fd32b4dba19b1239be627ba` |
| historical_baseline | `tools/live_raw_protocol_probe.py` | 8846 | `860dfe1f8b0e937e2a086c1a6a0933ed232bdca0ee9b82ea1bd6b940a720884f` |
| historical_baseline | `tools/live_verifier_probe.py` | 3519 | `a7b958cd885e32247a997fefee8e50a46534348af00a4ccebfeead8120bbe055` |
| historical_baseline | `tools/make_package_inventory.py` | 11425 | `b44cf55fa97deed3f890b8a35a0cf09ed3ec595e78fd6ec351a0daa9cdf4d4ed` |
| historical_baseline | `tools/make_trust_manifest.py` | 13127 | `2d085bc4f8faba56f45b397ef71933799c047194848a34ea48058f9c211fc09e` |
| historical_baseline | `tools/ProtectedFilesystemReplay.cs` | 35016 | `1fcc024274987b343ff279bfacc9378101e75fe4f2feb068cfe6a11b3ffd8dee` |
| v2_created | `tools/publish_implementation_candidate.py` | 27787 | `ab90b863b998282807738609599dffb44c68b8010eb30441ceb31b07c28955c4` |

The v2 inventory and external handoff must validate before the v3 root is
created. A mismatch in either exact file SHA-256, root digest, file count, or
total length blocks carry-forward. The existing v2 inventory checker may be
run read-only; it must not rewrite the inventory.

## Source-copy outcome contract

Copy rows in ordinal relative-path order. Each destination is exclusively
created as an ordinary non-reparse file, reread, and checked for exact length
and SHA-256 before the next row. No generated output or inventory file may be
copied.

The v3 handoff and publication-failure projection use these four sorted unique
arrays:

```text
baseline_copied_paths
failed_source_copy_paths
carried_forward_created_paths
failed_created_source_paths
```

Their derivation is closed:

- `not_started`: all four arrays are empty; no v3 root or copy-created row
  exists;
- `failed_incomplete`: the two baseline arrays are disjoint and their union is
  exactly the 37 `historical_baseline` paths; the two created-source arrays are
  disjoint and their union is exactly the nine `v2_created` paths; at least one
  failed array is nonempty; a failed array includes every row not successfully
  copied and validated, including rows not attempted after the first failure;
- `complete`: `baseline_copied_paths` is exactly all 37 baseline paths,
  `carried_forward_created_paths` is exactly all nine created-source paths, and
  both failed arrays are empty.

Any duplicate, extra, missing, overlapping, unsorted, or differently spelled
path is invalid. `failed_incomplete` is terminal for that v3 root. It does not
authorize editing, building, inventory generation, retry, repair, or reuse.

## Future edit envelope

After an accepted independent review and a separate exact owner activation, a
future implementation may modify only these v3 package source paths:

```text
client/windows_broker_client.py
docs/broker-service-contract.md
src/MythicEdgeRolePoolBrokerContracts.cs
tests/test_broker_service_contracts.py
tests/test_implementation_handoff.py
tests/test_package_inventory.py
tests/test_windows_broker_client.py
tools/make_package_inventory.py
tools/publish_implementation_candidate.py
```

The client, shared C# contract, broker documentation, and their focused tests
own the reconciliation correction. The handoff and inventory tests plus the
two publication tools own v3 identity, inventory, handoff, and publication
validation. The future pass may change only what is necessary for this
contract. No Role Pool skill file may change. No new source path may be
created. A required path outside this envelope routes to Codex B before edits.

## Mandatory rebuild and carry-forward matrix

Generated v2 outputs are lineage evidence only and must never be copied into
v3. The existing clean build sequence produces all five outputs from carried
forward or corrected source:

| output | exact-byte carry-forward | direct dependency on corrected shared C# | v3 action |
|---|---|---|---|
| `dist/MythicEdgeRolePoolIsolationBroker.exe` | forbidden | yes, `MythicEdgeRolePoolBrokerContracts.cs` | rebuild with managed build |
| `dist/MythicEdgeRolePoolVerifierService.exe` | forbidden | yes, `MythicEdgeRolePoolBrokerContracts.cs` | rebuild with managed build |
| `dist/MythicEdgeRolePoolVerifierActivationHost.exe` | forbidden | no | rebuild in the same clean managed build |
| `dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe` | forbidden | no | rebuild in the same clean managed build |
| `dist/MythicEdgeRolePoolVerifierBootstrap.exe` | forbidden | no; Go source only | rebuild with trusted offline Go archive |

The affected shared-C# dependency closure is exactly Isolation Broker and
Verifier Service. The v3 package-freshness build closure is all five outputs
because no generated v2 output may be carried forward and the managed build
already produces its four outputs as one bounded invocation. This does not
authorize unrelated builds or acquisition.

The only reusable build input outside the 46-row source envelope is one
already-present owner-named trusted Go archive. The future activation must bind
its private absolute path and this fixed digest:

```text
trusted_go_archive_sha256=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
```

The path is never serialized. Only ordinary-file identity and exact digest may
be checked before the existing native build reads the archive into a fresh
private temporary tree. Download, package-index access, network fallback,
archive discovery, parent enumeration, neighboring-file access, substitution,
installation, or toolchain update is forbidden.

## Reconciliation correction

### Immutable expected epoch

The original validated launch request owns `expected_verifier_epoch`. The
coordinator retains it with the original launch ID and launch-request digest
and uses the same value for every read-only reconciliation comparison. A
reconciliation caller cannot replace, omit, or refresh it from the current
verifier response.

Every verifier service start creates a fresh nonempty verifier epoch that must
not equal any epoch intentionally reused by that installation. Loss of the
original in-memory record plus a different current epoch is verifier restart or
state loss and resolves to `unknown`. It can never resolve to
`definitive_not_started`.

### Closed receipt fields and pins

The reconciliation receipt remains
`mythic_edge_role_pool_broker_reconciliation_receipt.v1` with exactly:

```text
schema_version
attestation_domain
attestation_algorithm
attestation_key_id
verifier_identity
evidence_source
launch_id
launch_request_digest
state
start_receipt_digest
terminal_receipt_digest
abort_receipt_digest
verifier_epoch
observed_at
attestation
digest
```

Validation requires:

```text
schema_version=mythic_edge_role_pool_broker_reconciliation_receipt.v1
attestation_domain=mythic_edge_role_pool.broker_reconciliation_receipt.v1
attestation_algorithm=hmac-sha256
verifier_identity=mythic_edge_role_pool_windows_isolation_verifier_service.v1
evidence_source=windows_kernel_appcontainer_job_acl_network_state.v1
```

`attestation_key_id` must equal the exact nonempty key identifier in the
independently reviewed installation inventory. No wildcard, default, caller
value, or response-only adoption is valid. `verifier_epoch` must equal the
original `expected_verifier_epoch`. `observed_at` must match
`YYYY-MM-DDTHH:MM:SS.mmmZ`, parse as UTC, and be nondecreasing relative to the
last accepted receipt in the same launch attempt. A later timestamp is not
proof of process state.

`attestation` and `digest` are lowercase 64-character SHA-256 hex strings.
`digest` is SHA-256 of strict UTF-8 compact sorted-key ASCII-escaped JSON with
only root `digest` omitted. `attestation` is HMAC-SHA-256 over the canonical
receipt without `attestation` and `digest`, under the fixed domain and the
installation-pinned key. The coordinator verifies the self-digest and
attestation before deriving state.

### State and digest matrix

| state | start digest | terminal digest | abort digest | additional condition |
|---|---|---|---|---|
| `definitive_not_started` | null | null | null | current epoch equals expected epoch and verifier attests no created/resumed process for the exact request |
| `started` | required | null | null | digest equals the validated start receipt for the exact request |
| `terminal` | required | required | null | both digests equal the validated chain for the exact request |
| `aborted` | null or required | null | required | abort digest equals the validated abort receipt; start digest is present exactly when that chain has a start receipt |
| `unknown` | null | null | null | no stronger state is accepted |

Every required digest is lowercase 64-character SHA-256. `null` is JSON null,
not an absent key or string. A digest supplied in a forbidden cell, an absent
required digest, cross-request digest, invalid chain, terminal/abort conflict,
or mismatch with an already validated receipt makes the receipt invalid and the
outcome `unknown`.

The validator must compare all of these dimensions independently: schema,
domain, algorithm, key ID, verifier identity, evidence source, launch ID,
request digest, expected verifier epoch, timestamp shape/order, state/digest
matrix, self-digest, and HMAC attestation. Mutation of any one dimension must
fail closed.

Read-only reconciliation may query only the original launch ID and request
digest. It may not create a reservation, create or resume a process, cancel,
terminate, relaunch, replace an epoch, mint replacement authority, or mutate
workflow state. Malformed, mismatched, cross-epoch, unverifiable, missing, or
contradictory evidence returns or projects `unknown` and preserves the original
attempt as unresolved.

## v3 inventory contract

The inventory uses strict UTF-8 compact sorted-key ASCII-escaped JSON, rejects
duplicate, missing, and unknown keys and non-finite numbers, and has exactly:

```text
schema_version
package_id
package_authority_profile
package_status
contract_id
contract_path
contract_sha256
parent_contract_id
parent_contract_path
parent_contract_sha256
rejected_v2_package_id
rejected_v2_inventory_file_sha256
rejected_v2_inventory_root_digest
rejected_v2_handoff_file_sha256
rejected_v2_handoff_root_digest
carry_forward_baseline_row_count
carry_forward_created_row_count
source_copy_status
role_pool_manifest_profile
role_pool_manifest_helper_path
role_pool_manifest_file_count_before
role_pool_manifest_before_sha256
role_pool_manifest_file_count_after
role_pool_manifest_after_sha256
broker_protocol_id
verifier_protocol_id
trusted_go_archive_sha256
required_dist_paths
source_repository_access_status
broker_provisioned
production_context_available
package_reviewed
package_installed
stage4_canary_authorized
stage4_evidence_eligible
pooled_dispatch_eligible
stage_advancement_claimed
finding_resolution_claimed
live_ready
blockers
file_count
total_length_bytes
files
digest
```

Candidate inventory fixed values include:

```text
schema_version=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v3
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v3
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v3
package_status=implementation_candidate_uninstalled_unreviewed
contract_id=mythic_edge_role_pool_external_isolation_broker_v3_corrective_successor.v1
contract_path=references/external-isolation-broker-v3-corrective-successor.md
parent_contract_id=mythic_edge_role_pool_external_isolation_broker.v1
parent_contract_path=references/external-isolation-broker.md
parent_contract_sha256=b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa
rejected_v2_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
rejected_v2_inventory_file_sha256=aa9cfb5d37466d2bf427d5da751456395e2db8b2d1131f55425fb8f61b8c890c
rejected_v2_inventory_root_digest=78a636f0a7995dd2780897631a14ed4e15b44a7eceb8057e1daf7177aeeadc8f
rejected_v2_handoff_file_sha256=f440dae0e42a75ad704dc3e1e7bc4cd0b77aba21c37d7b33d1c19476e4d7c8fe
rejected_v2_handoff_root_digest=ae8365efff2a973063cb15709f31c9115ab38dfdae9a6dad2047deadd4126bc8
carry_forward_baseline_row_count=37
carry_forward_created_row_count=9
source_copy_status=complete
broker_protocol_id=mythic_edge_role_pool_windows_isolation_broker.v1
verifier_protocol_id=mythic_edge_role_pool_windows_isolation_verifier_service.v1
trusted_go_archive_sha256=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
source_repository_access_status=not_accessed
broker_provisioned=false
production_context_available=false
package_reviewed=false
package_installed=false
stage4_canary_authorized=false
stage4_evidence_eligible=false
pooled_dispatch_eligible=false
stage_advancement_claimed=false
finding_resolution_claimed=false
live_ready=false
```

`contract_sha256` is the accepted reviewed digest of this artifact. The Role
Pool before/after profile remains the current frozen Stage-4 manifest selected
by the future activation; counts and digests must be equal because this v3
attempt authorizes no Role Pool edits. `required_dist_paths` is the exact sorted
five-output list in the rebuild matrix. `blockers` is exactly
`["independent_review_pending","installation_not_authorized","stage4_canary_not_authorized"]`.

The `files` rows retain the parent inventory row schema and include only final
v3 package content other than the inventory itself and its staging file. The
root `digest` omits only itself. The final inventory file SHA-256 includes the
root digest.

## v3 implementation handoff contract

The v3 handoff uses the same canonical JSON rules and has exactly:

```text
schema_version
contract_id
contract_path
contract_sha256
parent_contract_id
parent_contract_path
parent_contract_sha256
owner_activation_ref
owner_activation_sha256
owner_activation_status
package_authority_profile
package_id
package_parent_resolver
package_parent_suffix
package_directory_name
inventory_filename
inventory_staging_filename
implementation_handoff_filename
implementation_handoff_staging_filename
rejected_v2_package_id
rejected_v2_inventory_file_sha256
rejected_v2_inventory_root_digest
rejected_v2_handoff_file_sha256
rejected_v2_handoff_root_digest
rejected_v2_reuse_authorized
trusted_go_archive_sha256
trusted_build_input_status
local_build_authorized
package_self_tests_authorized
source_copy_status
baseline_copied_paths
failed_source_copy_paths
carried_forward_created_paths
failed_created_source_paths
modified_carry_forward_paths
unchanged_carry_forward_paths
created_source_paths
removed_paths
unexpected_paths
required_dist_paths
generated_output_paths
source_repository_access_status
build_performed
package_self_tests_performed
role_pool_manifest_helper_path
role_pool_manifest_file_count_before
role_pool_manifest_before_sha256
role_pool_manifest_file_count_after
role_pool_manifest_after_sha256
changed_role_pool_paths
validation_rows
inventory_status
inventory_file_sha256
inventory_root_digest
inventory_file_count
inventory_total_length_bytes
handoff_status
blockers
install_performed
service_mutation_performed
canary_performed
external_mutation_performed
stage_advancement_claimed
finding_resolution_claimed
live_ready
successor_reuse_authorized
next_role
digest
```

The handoff statuses are exactly `blocked_before_inventory` and
`candidate_ready_for_independent_review`. A blocked handoff has no inventory,
uses the exact four source-copy arrays derived above, sets all effect and claim
booleans false, sets `successor_reuse_authorized=false`, and routes to
`codex_b_contract_reconciliation`. A candidate handoff requires complete copy,
all required validation rows passed, a frozen matching inventory, all five
rebuilt executables plus `package-inventory.json` in
`generated_output_paths`, no removed or unexpected paths, no Role Pool change,
all effect and claim booleans false, and routes to
`codex_e_independent_review`.

`modified_carry_forward_paths` is a sorted subset of the future edit envelope.
`unchanged_carry_forward_paths` is the exact remaining subset of the 46-row
manifest. `created_source_paths`, `removed_paths`, `unexpected_paths`, and
`changed_role_pool_paths` must be empty. A future contract amendment is required
before any new source file is allowed.

Each validation row has exactly:

```text
command_id
status
exit_code
passed_count
failed_count
error_count
skipped_count
sanitized_error_code
```

Allowed `status` values are `not_run`, `passed`, and `failed`. Candidate-ready
requires exit code zero, a positive passed count where the command runs tests,
and zero failed, error, and skipped counts for every required package test row.
Raw output, exception text, commands containing private paths, and local paths
are forbidden.

## Publication correction

### State machine

Inventory then external handoff publication is bounded and no-replace. Every
staging file is exclusively created, flushed, reread, and byte-validated.
Final paths are never overwritten, deleted, adopted, repaired, or treated as
the active attempt merely because they parse.

For a candidate-ready attempt:

1. construct canonical inventory and handoff bytes in memory;
2. exclusively stage and validate both files;
3. move inventory staging to final once with no replacement;
4. perform at most one bounded inventory reconciliation;
5. only after a matching immutable final inventory is confirmed, move handoff
   staging to final once with no replacement;
6. perform at most one bounded handoff reconciliation; and
7. report candidate-ready only when both finals match and both staging paths
   are absent.

For a blocked-before-inventory attempt, construct and publish only the blocked
handoff using the same handoff staging, no-replace move, and one bounded
reconciliation. No final or staged inventory may exist.

### Bounded reconciliation table

The table applies independently to the currently published target:

| final state | staging state | one permitted action | result |
|---|---|---|---|
| exact matching ordinary file | absent | none | published |
| absent | exact attempt-owned ordinary file | one no-replace move, then one readback | published only if final matches and staging is absent |
| exact matching ordinary file | exact attempt-owned ordinary file | remove only that verified staging file once | published only if cleanup succeeds |
| absent | absent | none | publication absent |
| conflicting final | any | none | collision |
| unknown final type or unreadable final | any | none | unknown |
| any | changed, unknown, or unreadable staging | none | unknown |
| any state after the one move or cleanup fails | any | no retry | retry exhausted or cleanup failed |

Reconciliation performs no byte-changing package operation. It never creates
or modifies inventory or handoff content, adopts an unrelated final, removes a
final, retries without bound, or advances to the next publication phase while
the current final is absent, conflicting, or unknown.

If inventory publication fails conclusively before a final inventory exists,
the terminal status is `failed_before_inventory`. If inventory state cannot be
proved, it is `publication_state_unknown`. If final inventory is matching but
handoff publication fails, the inventory remains immutable and the terminal
status is `frozen_candidate_handoff_unpublished`. The package is not usable or
reusable in all three cases.

Cleanup may remove only an exact attempt-created staging file after its bytes
and identity match the in-memory candidate. Cleanup failure is terminal,
projected publicly, and grants no second move, deletion, overwrite, or retry.

### Closed publication-failure projection

When no final handoff can be published, return exactly one public-safe workflow
projection named `package_publication_failure` with exactly:

```text
contract_id
contract_sha256
parent_contract_sha256
package_id
handoff_schema
owner_activation_ref
owner_activation_sha256
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
contract_id=mythic_edge_role_pool_external_isolation_broker_v3_corrective_successor.v1
parent_contract_sha256=b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v3
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v3
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

`external_handoff_publication_status` is exactly `failed_pre_inventory`,
`failed_post_inventory`, or `unknown_after_publish_attempt`.
`inventory_status` is respectively `not_created`, `frozen_candidate`, or
`unknown`. For `not_created` and `unknown`, both inventory digest fields are
the string `none`; for `frozen_candidate`, both are the validated lowercase
SHA-256 values from the immutable final inventory.

`successor_terminal_status` is respectively `failed_before_inventory`,
`frozen_candidate_handoff_unpublished`, or `publication_state_unknown`.
`sanitized_error_code` is exactly one of:

```text
source_copy_failed
inventory_staging_write_failed
handoff_staging_write_failed
inventory_publish_absent
inventory_publish_collision
handoff_publish_absent
handoff_publish_collision
publication_state_unknown
publication_retry_exhausted
staging_cleanup_failed
```

The four source-copy arrays must satisfy the complete outcome derivation in
this contract. The object contains no absolute path, raw command, raw output,
exception, stack trace, approval text, source bytes, receipt key, credential,
or inferred state. It is failure-routing evidence only, not an inventory,
external handoff, implementation authority, accepted finding resolution, or
readiness claim.

## Required validation matrix

### Current installed-skill manifest blocker

Adding this required sibling artifact changes the currently frozen Role Pool
manifest from 34 to 35 files. The current Stage-3 transition validator allows
only its existing four added paths and does not include
`references/external-isolation-broker-v3-corrective-successor.md`.

The resulting offline gate deterministically runs 290 tests and fails five
Stage-3 manifest-transition tests with
`contract_transition: unexpected or missing added paths`; the structural skill
validation still passes. This is an artifact-lifecycle integration blocker,
not evidence that the v3 package correction was implemented or tested.

This Codex B authority does not permit editing the Stage-3 validator, fixtures,
tests, Skill manifest policy, or any runtime file. Therefore:

```text
runtime_manifest_integration_status=blocked_owner_decision_required
runtime_manifest_integration_authorized=false
contract_acceptance_ready=false
ready_for_codex_c=false
```

The owner must choose one separately reviewed route before this contract can be
accepted as validation-clean:

1. authorize a narrow Role Pool manifest-transition amendment that binds this
   exact path and reviewed digest without weakening any existing check; or
2. designate a different non-runtime authority location, then require a move,
   new path binding, new artifact digest, and fresh independent review.

Do not infer either choice. Do not delete or move this candidate, weaken the
gate, or edit validator expectations under this contract thread. Until a route
is selected, the Role Pool offline-gate requirement remains active and failed,
and the conclusion remains `NOT LIVE-READY`.

### Contract and lineage validation

- verify this artifact's exact SHA-256 and parent SHA-256;
- verify the exact v2 inventory file SHA-256, root digest, count, total length,
  and all 46 carry-forward rows without rewriting v2;
- verify the exact v2 handoff file SHA-256, root digest, package identity, and
  `successor_reuse_authorized=false`;
- verify absence of the v3 package root, final handoff, and both staging paths
  before a future activated attempt;
- verify no Role Pool skill bytes changed during v3 implementation.

### EIB-PKG-IMPL-E-001 focused adversarial tests

- same request, expected epoch, and attested no-start evidence accepts
  `definitive_not_started`;
- verifier restart with a changed epoch resolves to `unknown`;
- verifier state loss or missing original record with epoch mismatch resolves
  to `unknown`;
- mutations of algorithm, key ID, verifier identity, evidence source, verifier
  epoch, and timestamp shape/order each fail closed;
- malformed self-digest, bad HMAC, cross-request receipt, invalid digest
  matrix, terminal/abort conflict, and unknown field each fail closed;
- reconciliation is proven read-only: no create, resume, cancel, terminate, or
  relaunch call is made.

### EIB-PKG-IMPL-E-002 focused adversarial tests

- `not_started`, every representative partial-copy boundary, and `complete`
  derive exact four-array projections;
- a failed row causes every later unvalidated row to appear in the matching
  failed array and blocks edits/builds/inventory;
- blocked handoff publication covers matching final, absent final, collision,
  changed staging, unreadable state, retry exhaustion, and cleanup failure;
- candidate inventory publication covers the same states and never publishes a
  handoff while inventory is absent, conflicting, or unknown;
- post-inventory handoff failure preserves and validates the immutable final
  inventory and emits the exact failure projection;
- all failure projections reject extra keys, raw paths, raw output, exceptions,
  approval text, and contradictory authority booleans.

### Current-byte package and offline validation

A future authorized implementation must run focused source tests first, then
the clean managed build, native bootstrap build, native self-tests, and full
package test suite. Current-byte package tests require zero failures, zero
errors, and zero skips. All five outputs must be fresh v3 build products and
must appear exactly once in the final inventory.

The Role Pool offline gate remains required:

```powershell
py -B scripts\run_release_tests.py
```

It must pass its tests and structural validation while retaining the explicit
`NOT LIVE-READY` conclusion. Prior evidence may be cited only for exact
unchanged bytes bound in this contract. It cannot replace tests for changed
source, fresh outputs, v3 inventory/handoff behavior, or the two findings. No
package acquisition, unrelated source read, redundant toolchain acquisition,
or unrelated rebuild is required or allowed.

## Owner activation and independent review gates

Codex E must review the exact candidate bytes against this parent binding, the
v2 lineage pins, both findings, the carry-forward table, schema closures,
reconciliation matrix, publication matrix, validation matrix, and all
false-authority fields. Review produces no implementation authority.

A later owner activation must be new, exact, unexpired, and single-attempt. It
must name or bind:

- this contract ID, path, and accepted SHA-256;
- the parent contract ID and SHA-256;
- all v2 inventory and handoff pins;
- the v3 package identity, parent resolver, basename, schemas, and staging/final
  basenames;
- `exact_byte_carry_forward_authorized=true` for only the 46 listed rows;
- the closed future edit envelope;
- the exact Role Pool manifest-before profile, count, and digest;
- `local_build_authorized=true` and
  `package_self_tests_authorized=true` if those operations are intended;
- the private trusted Go archive path and fixed digest;
- exact focused and full validation invocations;
- activation expiry and one-attempt consumption semantics; and
- all forbidden effects and non-claims below.

Missing, placeholder, stale, contradictory, broader, reused, or partially
bound activation data fails before v3 root creation. Contract review cannot be
used as owner activation.

## False-authority and non-claim fields

At completion of this Codex B thread and after contract review, all remain:

```text
ready_for_codex_c=false
implementation_authorized=false
runtime_manifest_integration_authorized=false
contract_acceptance_ready=false
exact_byte_carry_forward_authorized=false
package_creation_authorized=false
package_build_authorized=false
inventory_creation_authorized=false
handoff_publication_authorized=false
source_repository_access_authorized=false
installation_authorized=false
service_mutation_authorized=false
stage4_execution_authorized=false
canary_authorized=false
stage_advancement_authorized=false
live_ready=false
finding_resolution_claimed=false
correctness_claimed=false
security_assurance_claimed=false
privacy_assurance_claimed=false
production_readiness_claimed=false
```

The v2 package remains uninstalled, unreviewed as an accepted candidate,
non-live, immutable, and non-reusable. The v3 package does not exist. This
contract makes no claim that either finding is implemented, that the broker is
correct or secure, or that any Stage-4 or production operation is ready.

## Stop conditions and next role

Stop and route to Codex B and the owner for any identity mismatch, absent or
changed v2 row, source-copy ambiguity, private-path exposure, need for a new
file, runtime protocol change, broader source access, package acquisition,
unbounded retry, publication state not covered above, or authority conflict.

Codex E may perform semantic review of this exact candidate, but the immediate
authority decision is the owner-selected manifest-integration route above.
After that route is completed and independently reviewed, Codex E must review
the final exact contract bytes again. Codex C is not authorized by either
review alone.
