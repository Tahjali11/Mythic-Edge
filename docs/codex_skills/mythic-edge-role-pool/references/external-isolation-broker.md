# External-Isolation Broker Contract

Contract ID: `mythic_edge_role_pool_external_isolation_broker.v1`

Package-authority profile:
`mythic_edge_role_pool_external_isolation_broker_package_authority.v2`

Status: `draft_implementation_required_stage4_blocked`

This contract defines the minimum Windows broker boundary needed to collect
Stage-4 evidence without treating an unrelated later process start as isolated.
It is a Codex B contract only. It does not implement, install, activate, or use
a broker; launch Codex; authorize a canary; resolve `MRP-RC-003`; advance a
stage; or declare the Role Pool live-ready.

## Contents

- [Decision](#decision)
- [Authority and eligibility](#authority-and-eligibility)
- [Frozen entry evidence](#frozen-entry-evidence)
- [Versioned implementation package and artifact authority](#versioned-implementation-package-and-artifact-authority)
- [Broker service and IPC boundary](#broker-service-and-ipc-boundary)
- [Component ownership](#component-ownership)
- [Strict documents](#strict-documents)
- [Atomic launch sequence](#atomic-launch-sequence)
- [Isolation policy](#isolation-policy)
- [Verifier issuance boundary](#verifier-issuance-boundary)
- [Lifecycle and recovery](#lifecycle-and-recovery)
- [Reconciliation with the direct launcher](#reconciliation-with-the-direct-launcher)
- [Stage-4 use](#stage-4-use)
- [Implementation and review acceptance](#implementation-and-review-acceptance)

## Decision

Only the broker may create a production-quality or Stage-4 canary process. The
coordinator may prepare and validate the exact launch request, but it must not
call `subprocess.Popen`, `CreateProcess*`, or another process-creation API for
that launch. The broker must create the authoritative child with its final
token, AppContainer or equivalent capability boundary, job containment,
filesystem policy, network policy, handle policy, and process limits in place
before any child instruction executes.

The current direct Python launcher is retained only for deterministic offline
tests. Its `subprocess_popen` backend and
`mythic_edge_role_pool_single_start_receipt.v2` receipt are permanently
non-live and must use `production_eligible=false`. A verifier receipt observed
before an unrelated `Popen` cannot upgrade that later process.

Use production launcher identity `codex:broker-single-start/v1`. Retain
`codex:exec-single-start/v2` only as the direct offline launcher and as the
argument/preflight builder during migration. No current runtime implements the
broker identity, so all live launch and Stage-4 execution remains blocked.

## Authority and eligibility

Broker evidence proves process placement and isolation facts only. It never
grants repository access, workflow action, a claim, reservation, role task,
write, credential use, external mutation, finding resolution, stage
advancement, pooled dispatch, or live readiness.

Keep these decisions separate:

- `stage4_evidence_eligible` is derived by the Stage-4 harness from a current
  validated canary exception plus accepted broker and verifier evidence;
- normal pooled-dispatch eligibility remains false until its later staged gates
  pass; and
- `live_ready` remains false until every release stage and independent review
  required by the Role Pool completes.

Do not put `stage4_evidence_eligible`, `pooled_dispatch_eligible`,
`stage_advancement_claimed`, `finding_resolution_claimed`, or `live_ready` in a
broker receipt. Those are workflow conclusions outside the broker's authority.

This draft does not authorize broker or verifier installation, service,
firewall, registry, credential, repository, GitHub, or other persistent or
external changes. Those actions need their own current authority and reviewed
implementation artifacts.

## Frozen entry evidence

Treat the prepared verifier package only as reviewed entry evidence:

```text
package_inventory_sha256=b2a3765724c235744d8891d7087d744844c091513e1d37753c7de31d8601865e
package_inventory_root_digest=6b26769b7a37c039a31b72cb8a6a8140d9ffdcfaf35a748f200e9d4c611d8ca4
provider_id=mythic_edge_role_pool_windows_isolation_broker.v1
evidence_source_id=windows_kernel_appcontainer_job_acl_network_state.v1
verifier_identity=mythic_edge_role_pool_windows_isolation_verifier_service.v1
```

These pins do not claim that a broker or positive-attestation producer exists.
The current verifier protocol is verify-only and production acquisition is
disabled. Any broker implementation or positive-attestation protocol changes
the reviewed bytes and requires a new canonical inventory plus independent
review. The final broker and verifier executable hashes, service SIDs,
protocols, installation identities, and package digests must be pinned outside
storage writable by either service. An implementation is non-conforming until
every machine-specific pin named below is populated in that independently
reviewed inventory; an unset or wildcard pin is a hard activation failure.

## Versioned implementation package and artifact authority

This section closes the package-layout ambiguity that previously blocked an
implementation preflight. It defines the only permissible shape for a future
implementation workspace and its review artifacts. It does not create that
workspace or authorize Codex C, a build, package execution, installation,
service mutation, canary, or external mutation.

The broker runtime contract remains
`mythic_edge_role_pool_external_isolation_broker.v1` because this reconciliation
does not change its service, protocol, receipt, isolation, or Stage-4 semantics.
The package-authority profile, successor package identity, inventory schema,
handoff schema, basenames, and owner activation must use v2 because the failed
v1 package lifecycle and clean-pass requirements are materially different.

### Package identities and roots

Keep the existing verifier preparation package immutable as historical entry
evidence. Its logical role is `verifier_preparation_entry_evidence`; its
inventory remains
`mythic_edge_role_pool_windows_verifier_package_inventory.v2` with the exact
inventory SHA-256 and root digest in [Frozen entry evidence](#frozen-entry-evidence).
Do not edit it in place, regenerate its inventory, rebuild its `dist/` files,
or treat it as the next implementation package.

The sole clean-retry successor package identity is closed as follows:

```text
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
package_parent_resolver=windows_current_owner_desktop_mtg_resources.v1
package_parent_suffix=MTG Resources
historical_package_directory_name=MythicEdge-Role-Pool-Windows-Verifier-Prep
package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2
inventory_schema=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v2
inventory_filename=package-inventory.json
inventory_staging_filename=package-inventory.json.tmp
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v2
implementation_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2.implementation-handoff.v2.json
implementation_handoff_staging_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2.implementation-handoff.v2.json.tmp
```

The earlier v1 successor attempt is a failed, non-authoritative lifecycle fact,
not an alternate source or retry root:

```text
failed_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v1
failed_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1
failed_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1.implementation-handoff.v1.json
failed_attempt_status=blocked_fail_closed_before_inventory
failed_inventory_status=not_created
failed_handoff_status=not_created
failed_source_repository_access_status=unknown
failed_attempt_reuse_authorized=false
```

This reconciliation records only the public-safe Codex C handoff and exact-path
presence checks. The v1 tree is incomplete because its native bootstrap was
absent when full validation ran; full validation reported two errors and two
skips. No inventory or external handoff was created. Installation, service
mutation, canary execution, and external mutation were all reported false.
Those observations do not validate any v1 bytes, prove whether a source
repository was accessed, or grant review, reuse, repair, copy, or deletion
authority. Preserve the v1 tree without mutation. Never use it as a baseline,
copy source or build output from it, finish it in place, inventory it, or
convert it into the v2 successor.

Resolve the parent exactly once from the current non-elevated owner's Windows
Desktop known folder using
`Environment.GetFolderPath(SpecialFolder.DesktopDirectory)`, then append the
single literal segment `MTG Resources`. Do not use `%USERPROFILE%`, the current
working directory, registry search, filesystem search, package discovery, an
environment override, or a fallback root. The result must be absolute, on a
fixed local volume, owned by the current owner SID, and free of reparse points
at the Desktop, suffix, and package-root components. Empty, relative, remote,
removable, substituted, differently owned, or multiply resolved results fail
closed.

Only the exact historical root, exact active v2 successor root, exact external
handoff and staging paths, privately owner-named trusted Go archive path,
contracted Role Pool paths, and fresh tool-owned temporary roots created by the
exact authorized build or test command may be resolved or opened. A temporary
root must use the command's closed generated-basename rule beneath the canonical
local temporary directory, start absent, contain only ephemeral build or
invented test data, and be removed before hygiene validation. It grants no
sibling or parent enumeration. Before build authority validates,
the archive exception permits only an ordinary-file check and exact SHA-256
read. After validation, only the contracted native-build script may read and
extract those exact bytes into its fresh private build tree; the exception
grants no parent enumeration or neighboring-file access. Do not enumerate,
recurse, hash, search, or probe
the shared parent or any sibling to discover repositories or packages. In
particular, a parent-wide
`Get-ChildItem -Recurse`, wildcard hash search, repository discovery, or
best-match lookup is prohibited. If any operation may have opened content
outside the exact allowlist and its reach cannot be proven, record
`source_repository_access_status=unknown`; do not infer `not_accessed`.

Under that one resolved parent, the historical root is exactly
`historical_package_directory_name`, the successor root is exactly
`package_directory_name`, and the external handoff path is exactly
`implementation_handoff_filename`. The two staging paths are exactly
`inventory_staging_filename` beneath the successor and
`implementation_handoff_staging_filename` beneath the resolved parent. The
historical root must match both frozen inventory pins before a successor,
handoff, or staging path is considered. The successor, handoff, and both
staging paths must be absent before an authorized preparation pass.
The successor, final handoff, and external handoff staging path are ordinary
siblings outside the historical package and Role Pool skill; inventory staging
is a reserved child of the successor. Their absolute paths are private local
resolution inputs and must never appear in inventory, handoff, logs,
diagnostics, tests, or public-safe output.

A reparse point, symbolic link, junction, hard-linked file, pre-existing
successor, handoff, or staging path, nested successor, alternate basename,
case-folded alias, short-name alias, or fallback root fails closed. Do not
delete, merge, replace, rename, or repair a pre-existing path automatically.

### Historical source-copy boundary

A later explicitly authorized preparation pass may create the successor only
from the historical package bound above. It must first validate the historical
inventory without rewriting it. It may then make ordinary independent copies
of exactly the 37 inventory rows whose paths do not begin with `dist/`, after
verifying every copied row's relative path, byte length, and SHA-256. It must
not copy:

- any of the four historical `dist/` executables;
- the historical `package-inventory.json` as the successor inventory;
- `__pycache__/`, `.git/`, `install-evidence/`, `*.pyc`, `*.pyo`, `*.tmp`, or
  another transient or machine-state artifact; or
- service state, registry state, keys, receipts, logs, canary material, user
  data, repository content, credentials, or private evidence.

The predecessor inventory SHA-256 and root digest provide provenance; they do
not authorize copying until the owner explicitly activates a reviewed Codex C
pass. A mismatch, missing row, extra row, changed byte, or failed inventory
check stops before successor creation.

The failed v1 successor is never part of this copy boundary. The v2 successor
must start absent and be populated only from the same 37 validated non-`dist/`
historical rows. Any byte, path, generated output, report, or implementation
choice found only in v1 must be independently recreated under the reviewed v2
contract and owner activation; it must not be copied or treated as evidence.

### Future implementation edit envelope

After independent review and a separate exact owner activation, a Codex C pass
may edit only these Role Pool paths:

```text
SKILL.md
references/fallback-and-recovery.md
references/pool-state-schema.md
references/release-remediation-matrix.md
references/role-readiness-and-safety.md
scripts/check_pool_plan.py
scripts/codex_launcher_contract.py
scripts/pool_test_fixtures.py
scripts/run_release_tests.py
scripts/test_check_pool_plan.py
scripts/test_codex_launcher_contract.py
scripts/test_pool_results.py
scripts/test_release_adversarial.py
scripts/test_skill_contract.py
```

The source contract itself is review authority and is not in that future edit
allowlist. A required Role Pool path outside the list routes back to Codex B
before editing.

Within the new successor package only, the future edit envelope is the closed
set `.gitignore`, `README.md`, and the ordinary directory prefixes
`bootstrap/`, `client/`, `docs/`, `scripts/`, `src/`, `tests/`, and `tools/`.
New broker, verifier-issuance, inventory, build, and focused-test files must stay
within those prefixes. `dist/` is reserved for later owner-authorized build
outputs and may not contain hand-written source. `package-inventory.json` is
reserved for the final inventory generator and must never be edited manually.
`package-inventory.json.tmp` is reserved solely for the publication protocol,
is excluded from inventory content, and must not survive a successful publish.
No file outside these two closed envelopes is implementation scope.

### Clean-pass build and validation order

The v2 retry is a new single implementation attempt, not continuation of v1.
Before successor creation, a future separately authorized pass must validate
the exact reviewed contract bytes, exact owner activation, parent/root
resolution, historical inventory pins, Role Pool manifest-before pin, both edit
envelopes, and the absence of the v2 successor, v2 handoff, and both staging
paths. The owner
activation must separately authorize local package builds and non-installing
package self-tests. It must privately name one already-present trusted Go
archive and bind this exact SHA-256:

```text
trusted_go_archive_sha256=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
```

The archive path is a private local activation input. It never appears in the
package, inventory, handoff, command summary, log, diagnostic, or review
artifact. The pass must not download, discover, substitute, update, or install
a Go toolchain or use a package index or network fallback. Missing build or
self-test authority, an absent trusted archive, or a digest mismatch stops
before successor creation. After a valid activation, the external v2 handoff
may record that pre-creation block with empty package path arrays and no
inventory; it grants no retry or build authority.

After preflight, the pass must perform these phases in order:

1. create the fresh v2 root and copy exactly the 37 historical source rows;
2. apply only the two closed edit envelopes and run source-focused package and
   Role Pool validation that does not require generated binaries;
3. run `scripts/build.ps1` from the v2 root with no network or installation;
4. run `scripts/build-native-bootstrap.ps1` from the v2 root with the private
   owner-approved archive path and the exact expected digest above;
5. prove that these five and only these contracted executable outputs required
   by this package exist as ordinary non-reparse files:

   ```text
   dist/MythicEdgeRolePoolIsolationBroker.exe
   dist/MythicEdgeRolePoolVerifierActivationHost.exe
   dist/MythicEdgeRolePoolVerifierBootstrap.exe
   dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe
   dist/MythicEdgeRolePoolVerifierService.exe
   ```

6. run `py -I -B -m unittest discover -s .\tests -p "test_*.py" -v` from the
   v2 root and require exit code zero with positive passes and zero failures,
   errors, or skips;
7. run the non-installing service, broker, activation-host, and protected-
   filesystem-replay self-test commands already owned by the package; the
   Python suite must exercise the native bootstrap, so a missing or skipped
   native-bootstrap runtime test is a failure, not an acceptable degradation;
8. run the full Role Pool offline gate with
   `py -B scripts\run_release_tests.py` and require its tests and structural
   validation to pass while preserving its `NOT LIVE-READY` conclusion;
9. remove only transient files inside the active v2 root and contracted Role
   Pool transient locations, then run artifact hygiene and exact source-copy,
   manifest-after, and output-set checks;
10. construct and validate the canonical inventory and candidate handoff bytes,
    stage both with exclusive creation at their exact staging paths, and use the
    publication protocol below to publish the inventory followed by the
    external handoff; or
11. stage and publish a blocked handoff without an inventory when an earlier
    authorized phase fails.

The source-focused package row is the aggregate of exact discovery runs for
`test_broker_service_contracts.py` and `test_windows_broker_client.py`; the
owner activation must name the exact invocations before execution. The Role
Pool focused row similarly binds the exact allowlisted focused commands in the
activation. Neither aggregate may omit, filter, relabel, or convert a failed,
errored, or skipped test into a pass.

Do not run full package validation before both build phases pass and all five
outputs exist. Do not publish a final inventory before every preceding phase
passes. Do not rerun a build, build-owning test, generator, or byte-changing
package cleanup after final inventory publication. A failure inside one active
pass may be corrected and revalidated only before terminal publication begins.
The bounded publication reconciliation below is not an implementation retry
and may not change package bytes. Once a blocked handoff is published, a frozen
inventory lacks its matching published handoff, or the pass otherwise ends
without a candidate-ready handoff, that successor root is sealed and cannot be
resumed; another implementation attempt requires a new contracted package
identity, basename, schema versions, owner activation, and independent review.

`source_repository_access_status` has the closed vocabulary `not_accessed`,
`accessed`, and `unknown`. It is `not_accessed` only when every command and file
operation is proven to stay within the exact historical root, active successor
root, external handoff path, trusted archive path, and Role Pool allowlist.
Opening source-repository content makes it `accessed`. A terminated, partial,
broad, wildcard, parent-wide, or otherwise unbounded search whose reach cannot
be proven makes it `unknown`. `accessed` and `unknown` both stop the pass,
forbid inventory creation, require a blocked-handoff publication attempt when
handoff authority is already valid, use the closed publication-failure workflow
projection if that attempt cannot complete, and permanently disqualify that
successor root from reuse.

### Successor inventory contract

The successor inventory is a new family, not a rewrite or version claim over
the verifier-only v2 inventory. It uses strict UTF-8 compact sorted-key
ASCII-escaped JSON, rejects duplicate or unknown keys and non-finite numbers,
and has exactly these root fields:

```text
schema_version
package_id
package_authority_profile
package_status
predecessor_inventory_sha256
predecessor_inventory_root_digest
predecessor_source_row_count
source_copy_status
failed_package_id
failed_package_directory_name
failed_handoff_filename
failed_attempt_status
failed_inventory_status
failed_handoff_status
failed_source_repository_access_status
failed_attempt_reuse_authorized
source_contract_id
source_contract_path
source_contract_sha256
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

The fixed values are:

```text
schema_version=mythic_edge_role_pool_windows_broker_verifier_package_inventory.v2
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v2
package_status=implementation_candidate_uninstalled_unreviewed
predecessor_inventory_sha256=b2a3765724c235744d8891d7087d744844c091513e1d37753c7de31d8601865e
predecessor_inventory_root_digest=6b26769b7a37c039a31b72cb8a6a8140d9ffdcfaf35a748f200e9d4c611d8ca4
predecessor_source_row_count=37
source_copy_status=complete
failed_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v1
failed_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1
failed_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1.implementation-handoff.v1.json
failed_attempt_status=blocked_fail_closed_before_inventory
failed_inventory_status=not_created
failed_handoff_status=not_created
failed_source_repository_access_status=unknown
failed_attempt_reuse_authorized=false
source_contract_id=mythic_edge_role_pool_external_isolation_broker.v1
source_contract_path=references/external-isolation-broker.md
role_pool_manifest_profile=mythic_edge_role_pool_stage4_frozen_skill_manifest.v1
role_pool_manifest_helper_path=scripts/check_stage4_canary_exception.py
role_pool_manifest_file_count_before=33
role_pool_manifest_file_count_after=33
broker_protocol_id=mythic_edge_role_pool_windows_isolation_broker.v1
verifier_protocol_id=mythic_edge_role_pool_windows_isolation_verifier_service.v1
trusted_go_archive_sha256=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
required_dist_paths=["dist/MythicEdgeRolePoolIsolationBroker.exe","dist/MythicEdgeRolePoolVerifierActivationHost.exe","dist/MythicEdgeRolePoolVerifierBootstrap.exe","dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe","dist/MythicEdgeRolePoolVerifierService.exe"]
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

`source_contract_sha256` is the reviewed byte SHA-256 of this contract at the
future implementation baseline. It and both manifest digests are lowercase
64-character SHA-256 values. Both manifest counts are positive JSON integers.
None of these values may be embedded back into this contract.

The five `required_dist_paths` literals are exact, sorted, unique, and must each
appear exactly once in `files`. No other `dist/` path is permitted in the first
v2 candidate. The failed-attempt fields are immutable reconciliation metadata;
they do not establish predecessor provenance, source-copy authority, or
implementation evidence. The only predecessor remains the frozen historical
inventory. A candidate inventory is invalid unless
`source_repository_access_status=not_accessed`.

Compute both Role Pool manifests only with
`scripts/check_stage4_canary_exception.py::frozen_skill_manifest()` and
`current_skill_manifest_digest()`. The manifest is the helper's sorted array of
exact resolved-path strings and SHA-256 values for every ordinary Role Pool
file outside `__pycache__/`, followed by the exact workflow snapshot files
declared by that helper. Its digest is SHA-256 of UTF-8 compact sorted-key
ASCII-escaped JSON with no newline, using the helper's existing canonical
function. No alternate Stage-3 manifest, relative-path projection, filtered
manifest, or caller-built row set is compatible.

Capture the before count and digest after the contract SHA-256 and owner
activation validate but before any successor creation, source copy, Role Pool
edit, or handoff write. They must equal the count and digest named by that
activation. Capture the after count and digest after the final allowed Role
Pool edit and cleanup but before inventory or handoff creation. The row-level
before/after comparison must show changes only at the Role Pool allowlist in
this contract. A count change is permitted only for an explicitly reported new
or removed allowlisted path; the current envelope authorizes neither, so this
first implementation requires equal before and after counts.

The inventory is emitted only for a complete implementation candidate after
all contracted focused validation and the full offline gate pass, transient
files are absent, every package file is ready to freeze, and
`source_copy_status=complete`. An incomplete or failed pass before final
inventory publication must not emit or retain `package-inventory.json`. Once
the final inventory has been atomically published and validated, a later
external-handoff publication failure does not invalidate it and never
authorizes its deletion or modification. That terminal external lifecycle is
`frozen_candidate_handoff_unpublished`; it is not review-ready, does not change
the inventory's internal package status, and seals the successor for contract
reconciliation. The immutable candidate inventory uses this exact sorted
`blockers` value:

```text
blockers=["independent_review_pending","installation_not_authorized","stage4_canary_not_authorized"]
```

The three literals are always present and no other blocker literal is allowed.
Review outcome, installation state, and Stage-4 authority remain external
lifecycle facts and never mutate this inventory. Failed or incomplete
pre-freeze reasons belong only in the external handoff's closed blocker
projection defined below.

The inventory includes every ordinary package file except itself and the same
closed transient exclusions used by the historical generator:
`__pycache__/`, `.git/`, `install-evidence/`, `*.pyc`, `*.pyo`, and `*.tmp`.
It rejects reparse points and non-files. Each `files` row has exactly `path`,
`sha256`, and `length_bytes`; paths are unique, ascending, slash-normalized,
relative, and non-escaping. `file_count` and `total_length_bytes` are exact.
The root `digest` is SHA-256 of the canonical root object with only its own
`digest` omitted. Generate the inventory after all source edits, allowed builds,
tests, documentation, and cleanup. Any later package-byte change invalidates
the inventory and requires a fresh review candidate; it never mutates the
historical package.

### External implementation handoff

The external handoff file avoids a self-reference between package inventory
and Role Pool manifest. It is a public-safe strict JSON document, not Markdown,
with exactly these root fields:

```text
schema_version
handoff_status
contract_id
contract_path
contract_sha256
package_authority_profile
owner_activation_ref
owner_activation_sha256
owner_activation_status
package_parent_resolver
package_parent_suffix
historical_package_directory_name
package_id
package_directory_name
implementation_handoff_filename
implementation_handoff_staging_filename
predecessor_inventory_sha256
predecessor_inventory_root_digest
predecessor_source_row_count
source_copy_status
failed_package_id
failed_package_directory_name
failed_handoff_filename
failed_attempt_status
failed_inventory_status
failed_handoff_status
failed_source_repository_access_status
failed_attempt_reuse_authorized
role_pool_manifest_helper_path
role_pool_manifest_file_count_before
role_pool_manifest_before_sha256
role_pool_manifest_file_count_after
role_pool_manifest_after_sha256
inventory_status
inventory_filename
inventory_staging_filename
inventory_file_sha256
inventory_root_digest
inventory_file_count
inventory_total_length_bytes
baseline_copied_paths
failed_source_copy_paths
modified_baseline_paths
unchanged_baseline_paths
created_source_paths
generated_output_paths
changed_role_pool_paths
removed_paths
unexpected_paths
trusted_go_archive_sha256
required_dist_paths
local_build_authorized
package_self_tests_authorized
trusted_build_input_status
build_performed
package_self_tests_performed
source_repository_access_status
successor_reuse_authorized
validation_rows
install_performed
service_mutation_performed
canary_performed
external_mutation_performed
stage_advancement_claimed
finding_resolution_claimed
live_ready
blockers
next_role
digest
```

The fixed identity values are:

```text
schema_version=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v2
contract_id=mythic_edge_role_pool_external_isolation_broker.v1
contract_path=references/external-isolation-broker.md
package_authority_profile=mythic_edge_role_pool_external_isolation_broker_package_authority.v2
owner_activation_status=validated_exact_scope
package_parent_resolver=windows_current_owner_desktop_mtg_resources.v1
package_parent_suffix=MTG Resources
historical_package_directory_name=MythicEdge-Role-Pool-Windows-Verifier-Prep
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2
implementation_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2.implementation-handoff.v2.json
implementation_handoff_staging_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v2.implementation-handoff.v2.json.tmp
predecessor_inventory_sha256=b2a3765724c235744d8891d7087d744844c091513e1d37753c7de31d8601865e
predecessor_inventory_root_digest=6b26769b7a37c039a31b72cb8a6a8140d9ffdcfaf35a748f200e9d4c611d8ca4
predecessor_source_row_count=37
failed_package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v1
failed_package_directory_name=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1
failed_handoff_filename=MythicEdge-Role-Pool-Windows-Broker-Verifier-Prep-v1.implementation-handoff.v1.json
failed_attempt_status=blocked_fail_closed_before_inventory
failed_inventory_status=not_created
failed_handoff_status=not_created
failed_source_repository_access_status=unknown
failed_attempt_reuse_authorized=false
role_pool_manifest_helper_path=scripts/check_stage4_canary_exception.py
role_pool_manifest_file_count_before=33
role_pool_manifest_file_count_after=33
inventory_filename=package-inventory.json
inventory_staging_filename=package-inventory.json.tmp
trusted_go_archive_sha256=3ca8fb4630b07c419cbdd51f754e31363cfcfb83b3a5354d9e895c90be2cc345
required_dist_paths=["dist/MythicEdgeRolePoolIsolationBroker.exe","dist/MythicEdgeRolePoolVerifierActivationHost.exe","dist/MythicEdgeRolePoolVerifierBootstrap.exe","dist/MythicEdgeRolePoolVerifierProtectedFilesystemReplay.exe","dist/MythicEdgeRolePoolVerifierService.exe"]
successor_reuse_authorized=false
install_performed=false
service_mutation_performed=false
canary_performed=false
external_mutation_performed=false
stage_advancement_claimed=false
finding_resolution_claimed=false
live_ready=false
```

`owner_activation_ref` is one symbolic public-safe owner-authority reference;
`owner_activation_sha256` is the lowercase SHA-256 of its exact private source
bytes. The reference is a nonempty ASCII string of at most 256 characters using
only letters, digits, `.`, `:`, `/`, `_`, and `-`. The handoff never contains
approval text. Contract, activation, manifest, and root self-digests are
lowercase 64-character SHA-256 values. Inventory digests have that form only
for `frozen_candidate` and are both `none` for `not_created`. Manifest counts
and inventory counts are nonnegative JSON integers, with both manifest counts
positive.

The four dynamic build fields are booleans except
`trusted_build_input_status`, whose closed vocabulary is `not_checked`,
`missing`, `digest_mismatch`, or `validated`. The access-status vocabulary and
derivation are defined in [Clean-pass build and validation order](#clean-pass-build-and-validation-order).
The handoff never contains the trusted archive path. `successor_reuse_authorized`
is always false: a frozen candidate is immutable review input, while a blocked
attempt is terminal.

The path arrays are sorted, unique, slash-normalized package-relative or Role
Pool-relative strings with no absolute path, `..`, empty segment, drive,
alternate data stream, or reparse alias. `source_copy_status` has the closed
vocabulary `not_started`, `failed_incomplete`, and `complete`, with these exact
derivations:

- `not_started`: `baseline_copied_paths`, `failed_source_copy_paths`,
  `modified_baseline_paths`, and `unchanged_baseline_paths` are empty, and the
  source-copy validation row is `not_run`;
- `failed_incomplete`: `baseline_copied_paths` is the exact sorted subset of
  predecessor rows whose copied bytes, length, and SHA-256 passed readback;
  `failed_source_copy_paths` is a nonempty disjoint sorted subset containing
  every attempted predecessor row that did not validate;
  `modified_baseline_paths` is empty, `unchanged_baseline_paths` equals
  `baseline_copied_paths`, and the source-copy validation row is `failed`; the
  unattempted rows are derived as the 37-row predecessor set minus both listed
  subsets; and
- `complete`: `baseline_copied_paths` is exactly all 37 predecessor source
  rows, `failed_source_copy_paths` is empty, the source-copy validation row is
  `passed`, and `modified_baseline_paths` plus `unchanged_baseline_paths` are a
  disjoint exact partition of the 37 rows after allowed edits.

No implementation edit, generated output, Role Pool edit, or later validation
may begin unless `source_copy_status=complete`. A failed-incomplete handoff
therefore has empty `created_source_paths`, `generated_output_paths`, and
`changed_role_pool_paths`, while `removed_paths` is empty;
`unexpected_paths` remains the exact observed out-of-envelope projection and,
when nonempty, also adds `forbidden_scope_detected`. The pass preserves the
partial successor without repair or deletion, adds `source_copy_binding_failed`,
and seals that successor. A
candidate-ready handoff requires `source_copy_status=complete`.
`created_source_paths` contains only new ordinary source, test, tool, script, or
documentation paths in the successor edit envelope.
`generated_output_paths` contains only `dist/` outputs explicitly permitted by
the owner activation plus `package-inventory.json`; it is disjoint from the
other package path arrays. `changed_role_pool_paths` is a subset of the exact
Role Pool allowlist. A review-ready handoff requires empty `removed_paths` and
`unexpected_paths`. A blocked handoff lists only outputs proven to exist; it
must not project an expected output as generated. A candidate-ready handoff
contains every `required_dist_paths` literal exactly once plus
`package-inventory.json` exactly once.

For a pre-creation blocked handoff, `created_source_paths`,
`generated_output_paths`, `changed_role_pool_paths`, `removed_paths`, and
`unexpected_paths` are also empty, and the manifest-after count and digest
equal their manifest-before values. After successor creation, every path array
must project only the exact observed state at stop time; absence of an expected
path is never filled in speculatively.

`validation_rows` is a sorted, unique array containing exactly one row for each
of these command IDs:

```text
artifact_hygiene_check
historical_inventory_check
managed_build
native_bootstrap_build
package_binary_self_tests
package_full_validation
package_source_focused_validation
role_pool_focused_validation
role_pool_offline_gate
source_copy_binding_check
successor_inventory_check
```

Each row has exactly `command_id`, `status`, `exit_code`, `passed_count`,
`failed_count`, `error_count`, `skipped_count`, and `sanitized_error_code`.
`status` is one of `passed`, `failed`, or `not_run`. `exit_code` is `-1` exactly
for `not_run` and otherwise a nonnegative integer. Counts are nonnegative
integers and all are zero for `not_run`. `sanitized_error_code` is exactly one
of `none`, `not_run`, `precondition_failed`, `nonzero_exit`,
`digest_mismatch`, `scope_violation`, `inventory_freeze_failed`,
`hygiene_failed`, `build_failed`, `required_output_missing`, `test_failure`,
`test_error`, `test_skipped`, or `internal_error`; it is `none` exactly for
`passed` and `not_run` exactly for `not_run`. Rows contain no command text or
raw output.
For `passed`, exit code is zero, `passed_count` is positive, the other three
counts are zero, and the error code is `none`. For `failed`, the error code is
neither `none` nor `not_run`, and at least one of a nonzero exit code,
`failed_count`, `error_count`, or `skipped_count` is nonzero. A skipped package
or Role Pool test therefore cannot produce `passed` even when its process exits
zero.

`handoff_status` is exactly `candidate_ready_for_independent_review` or
`blocked_before_inventory`. For `candidate_ready_for_independent_review`:

- every validation row is `passed` with exit code zero and zero failed and
  error and skipped counts;
- `source_copy_status=complete` and `failed_source_copy_paths` is empty;
- `local_build_authorized=true`, `package_self_tests_authorized=true`,
  `trusted_build_input_status=validated`, `build_performed=true`,
  `package_self_tests_performed=true`, and
  `source_repository_access_status=not_accessed`;
- before and after Role Pool manifest counts are equal, all changed Role Pool
  rows are allowlisted, and `removed_paths` and `unexpected_paths` are empty;
- `inventory_status=frozen_candidate`, both inventory digests are lowercase
  SHA-256 values, both inventory counts are positive, and
  every required executable plus `package-inventory.json` appears exactly once
  in `generated_output_paths`; and
- `blockers` is exactly
  `["independent_review_pending","installation_not_authorized","stage4_canary_not_authorized"]`, while
  `next_role=codex_e_independent_review`.

For that candidate status, `inventory_file_sha256` is SHA-256 of the exact
canonical `package-inventory.json` bytes including its root `digest`;
`inventory_root_digest`, `inventory_file_count`, and
`inventory_total_length_bytes` equal the corresponding values parsed from
those same bytes.

For both handoff statuses, `local_build_authorized` and
`package_self_tests_authorized` reproduce only the two explicit booleans in the
validated owner activation. `build_performed=true` exactly when both build rows
are not `not_run`; it does not imply they passed. `package_self_tests_performed`
is true exactly when its validation row is not `not_run`.
`trusted_build_input_status` is `not_checked` before the private path check,
`missing` when the exact owner-named file is absent, `digest_mismatch` when its
bytes do not match the fixed digest, and `validated` only after the exact bytes
match. The public handoff records no archive filename or path.

For `blocked_before_inventory`, `inventory_status=not_created`, both inventory
digest fields are `none`, both inventory counts are zero, and
`package-inventory.json` is absent from every path array, while
`next_role=codex_b_contract_reconciliation`. Its lexically sorted unique
`blockers` array
contains the same three authority blockers plus every applicable literal from
this closed failure vocabulary:

```text
artifact_hygiene_failed
build_authority_missing
forbidden_scope_detected
historical_inventory_invalid
managed_build_failed
native_bootstrap_build_failed
offline_gate_failed
package_binary_self_tests_failed
package_full_validation_failed
package_self_test_authority_missing
package_source_validation_failed
package_validation_skipped
required_dist_output_missing
role_pool_manifest_drift
role_pool_validation_failed
source_repository_accessed
source_repository_access_unknown
source_copy_binding_failed
successor_inventory_failed
trusted_build_input_mismatch
trusted_build_input_missing
```

Map each `failed` validation row by exact command ID:

```text
artifact_hygiene_check=artifact_hygiene_failed
historical_inventory_check=historical_inventory_invalid
managed_build=managed_build_failed
native_bootstrap_build=native_bootstrap_build_failed
package_binary_self_tests=package_binary_self_tests_failed
package_full_validation=package_full_validation_failed
package_source_focused_validation=package_source_validation_failed
role_pool_focused_validation=role_pool_validation_failed
role_pool_offline_gate=offline_gate_failed
source_copy_binding_check=source_copy_binding_failed
successor_inventory_check=successor_inventory_failed
```

A `not_run` row adds no command-specific blocker; it must be downstream of at
least one applicable precondition or failed-row blocker under the fixed phase
order. Add `build_authority_missing` when `local_build_authorized=false`,
`package_self_test_authority_missing` when
`package_self_tests_authorized=false`, and the matching trusted-input blocker
for `missing` or `digest_mismatch`. Add `required_dist_output_missing` when any
required executable is absent after the build rows. Add
`package_validation_skipped` whenever a package validation or self-test row has
a positive skip count. Add the exact source-access blocker for `accessed` or
`unknown`. Add `role_pool_manifest_drift` for count, digest, or row-diff
inconsistency, and `forbidden_scope_detected` for a nonempty
removed/unexpected list or an out-of-envelope path. No other blocker or status
literal is allowed.

A contract or owner-activation mismatch stops before any successor or handoff
write and therefore has no handoff projection. The blocked handoff status is
available only after the exact contract and owner activation have validated and
an authorized implementation pass later fails an authority, trusted-input,
source-access, package, manifest, validation, inventory, or hygiene condition.

Serialize the root as strict UTF-8 compact sorted-key ASCII-escaped JSON with
no trailing newline. Reject duplicate, missing, or unknown fields and
non-finite numbers. Compute `digest` as SHA-256 of the canonical root object
with only its own root `digest` omitted. The handoff is not package content,
not Role Pool manifest content, and not an authority packet. Absolute local
paths, raw outputs, exception text, secrets, credentials, private paths,
package bytes, machine-state evidence, or unknown fields make it invalid.

### Inventory and handoff publication

Inventory and handoff publication is a bounded two-file state machine. It is
not a cross-filesystem atomic transaction and must never pretend otherwise.
Both staging files use strict exclusive creation, ordinary non-reparse files,
flush-to-disk, canonical-byte readback, and exact digest revalidation. A final
move is atomic within its directory and must use no-replace semantics. Neither
an existing final path nor an existing staging path may be overwritten,
deleted, merged, or adopted.

For a candidate-ready result, perform these steps exactly once in order:

1. construct the final inventory bytes in memory from the clean package state,
   excluding the final inventory and package-local inventory staging file; the
   external handoff staging file is outside the package inventory root;
2. construct the candidate handoff bytes in memory from that inventory's exact
   file SHA-256, root digest, counts, and path projections;
3. exclusively write, flush, reread, and validate
   `inventory_staging_filename` and
   `implementation_handoff_staging_filename`;
4. atomically move the inventory staging file to `inventory_filename` with
   no replacement, then reread and validate the final inventory;
5. atomically move the handoff staging file to
   `implementation_handoff_filename` with no replacement, then reread and
   validate the final handoff; and
6. report `candidate_ready_for_independent_review` only after both final files
   validate and both staging paths are absent.

For a blocked result before inventory, construct only the blocked handoff,
write and validate it at the handoff staging path, atomically move it to the
final handoff path with no replacement, and validate the final bytes. No final
or staged inventory may exist for that route.

Before final inventory publication is confirmed, a staging, validation, move,
or cleanup failure that conclusively leaves the final inventory absent uses
`inventory_status=not_created`. The pass may remove only a staging file that it
exclusively created and whose exact bytes still match its in-memory candidate.
It must not remove any final file or unknown/colliding path. A blocked handoff
is valid only if its final bytes were actually published and validated.

An ambiguous or failed inventory move receives one bounded reconciliation
before handoff publication: an exact matching final inventory is treated as
published; an absent final path plus the exact staging bytes permits one
no-replace move and readback; a conflicting final path, changed staging bytes,
second failure, or unreadable state stops. A confirmed absent final inventory
uses `failed_pre_inventory`; a validated matching final inventory continues as
the immutable frozen candidate; an unresolved state uses
`unknown_after_publish_attempt`. Never publish the handoff while final inventory
state is absent, conflicting, or unknown.

After final inventory publication, never delete, rewrite, regenerate, or
invalidate that inventory merely because handoff publication failed. Reconcile
the handoff publication once as follows:

- if the final handoff exists and exactly matches the staged canonical bytes,
  treat publication as complete and require the staging path to be absent;
- if the final handoff is absent and the exact validated staging handoff still
  exists, permit one no-replace move to the final path and validate it;
- if the final path contains different bytes, either path has unknown type or
  identity, the staging bytes changed, state cannot be read back, or the one
  bounded move still fails, stop with no overwrite and no further retry.

After a terminal post-inventory failure, cleanup may remove only the exact
attempt-created external handoff staging file after verifying its identity and
bytes; it may not touch package content. Cleanup failure is itself reported but
does not authorize another move or inventory mutation. The terminal successor
status is `frozen_candidate_handoff_unpublished`, it is not review-ready, and a
later implementation attempt requires a new versioned package identity.

If no final external handoff can be published, Codex C must return a public-safe
workflow handoff rather than create a fallback local file. That workflow
handoff contains one closed `package_publication_failure` object with exactly:

```text
contract_id
contract_sha256
package_id
handoff_schema
owner_activation_ref
owner_activation_sha256
external_handoff_publication_status
inventory_status
inventory_file_sha256
inventory_root_digest
source_copy_status
baseline_copied_count
failed_source_copy_count
source_repository_access_status
sanitized_error_code
successor_terminal_status
successor_reuse_authorized
installation_performed
service_mutation_performed
canary_performed
external_mutation_performed
stage_advancement_claimed
live_ready
next_role
```

The fixed identity values are:

```text
contract_id=mythic_edge_role_pool_external_isolation_broker.v1
package_id=mythic_edge_role_pool_windows_broker_verifier_preparation.v2
handoff_schema=mythic_edge_role_pool_external_isolation_broker_implementation_handoff.v2
successor_reuse_authorized=false
installation_performed=false
service_mutation_performed=false
canary_performed=false
external_mutation_performed=false
stage_advancement_claimed=false
live_ready=false
next_role=codex_b_contract_reconciliation
```

`external_handoff_publication_status` is exactly `failed_pre_inventory`,
`failed_post_inventory`, or `unknown_after_publish_attempt`.
The contract, package, handoff-schema, and owner-activation fields use the exact
validated values required by the external handoff schema; both SHA-256 fields
are lowercase 64-character values, and no approval text is included.
`inventory_status` is respectively `not_created`, `frozen_candidate`, or
`unknown`. For `not_created`, both digest fields are `none`; for
`frozen_candidate`, both are the validated lowercase SHA-256 values from the
immutable final inventory; for `unknown`, both are `none` and no state is
inferred. `successor_terminal_status` is respectively
`failed_before_inventory`, `frozen_candidate_handoff_unpublished`, or
`publication_state_unknown`.

The source-copy and source-access statuses use their existing closed
vocabularies. Counts are nonnegative integers. `not_started` requires `0` and
`0`; `failed_incomplete` requires `baseline_copied_count` from `0` through `36`,
positive `failed_source_copy_count`, and a sum no greater than `37`; `complete`
requires `37` and `0`. These counts summarize only already-derived path arrays
and never replace or reconstruct an unpublished external handoff.

`sanitized_error_code` is exactly one of
`inventory_staging_write_failed`, `handoff_staging_write_failed`,
`inventory_publish_failed`, `handoff_publish_failed`,
`handoff_publish_collision`, `publication_state_unknown`, or
`staging_cleanup_failed`. `successor_reuse_authorized` and all six authority or
effect booleans are false, and `next_role=codex_b_contract_reconciliation`.
The object contains no local path, command, raw output, exception, package
content, approval text, credential, or inferred publication fact. It is a
failure-routing projection only, not an external implementation handoff,
inventory, review artifact, authority packet, or readiness claim.

### Activation and stop rule

Contract acceptance and independent review still do not authorize Codex C. A
future owner activation must name this contract's reviewed SHA-256, the package
parent resolver, its privately resolved absolute parent and current owner SID,
the package ID and sibling basename, the exact approved 33-file Role Pool
manifest-before digest, the two predecessor pins, both closed edit envelopes,
the failed v1 identity and non-reuse status, the inventory and handoff final
basenames, and both staging basenames.
It must privately name the exact pre-existing trusted Go archive path, repeat
its fixed expected SHA-256, and separately state whether local builds,
non-installing package self-tests, and external handoff writing are permitted.
External handoff authority must explicitly include exclusive staging,
no-replace publication, the one bounded publication reconciliation, and cleanup
of only exact attempt-created staging bytes; it never includes deleting or
rewriting a final inventory or colliding path.
It must prohibit source-repository access and parent-wide discovery. Its
symbolic reference and exact source-byte SHA-256 must populate the future
handoff without copying approval text or any private path.
Absent that exact activation, only read-only contract and inventory validation
is permitted. Installation, service/firewall/registry mutation, package
execution, Stage-4 canary execution, source-repository access, credentials,
external mutation, and live use remain blocked in every case.

Even with that activation, package execution is limited to the exact
non-installing validation and self-test commands in the clean-pass order.
Installation, service startup or mutation, firewall or registry work, canary
execution, Codex launch, source-repository access, and external mutation remain
blocked.

## Broker service and IPC boundary

Freeze the broker itself as follows:

- service name and virtual account:
  `MythicEdgeRolePoolIsolationBroker` and
  `NT SERVICE\MythicEdgeRolePoolIsolationBroker`;
- service SID type: restricted, with the resolved service SID pinned in the
  reviewed installation inventory;
- maximum enabled privilege set: `SeAssignPrimaryTokenPrivilege`,
  `SeIncreaseQuotaPrivilege`, and `SeImpersonatePrivilege`; every other
  privilege, especially debug, TCB, backup, restore, ownership, and security
  privileges, must be absent or disabled. A strict subset is preferred when
  implementation tests prove it sufficient;
- fixed local pipe: `\\.\pipe\MythicEdgeRolePoolIsolationBroker.v1`, created
  with remote clients rejected and first-instance enforcement;
- exact pipe DACL: only Local System, the resolved broker service SID, and one
  installation-pinned local coordinator SID may connect. Network, anonymous,
  guest, Everyone, and unpinned administrator-group access are denied;
- immediately after connect and before reading even a length prefix, impersonate
  the pipe client, verify the exact local coordinator SID, authentication ID,
  session, integrity level, and non-network token, capture the kernel-reported
  client PID and non-reusable creation identity, and verify that process against
  the installation-pinned coordinator executable path/hash/length and signer,
  then revert. After strict parsing, bind those same observed values to the
  request rather than trusting caller-supplied identity fields;
- one request per connection, a four-byte little-endian unsigned length prefix,
  a 1,048,576-byte maximum canonical control document, a five-second caller
  authentication deadline, and a ten-second request-frame deadline; and
- stdout and stderr are separate bounded streams, at most 16,777,216 bytes each,
  transported in chunks no larger than 1,048,576 bytes. Overflow terminates the
  job and can never be truncated into a successful result; and
- broker and verifier service processes have inbound and outbound network access
  denied; their only control paths are the fixed local pipes.

The verifier issuance pipe has the same local-only, first-instance, bounded-
frame, pre-parse authentication, and exact-DACL requirements, except its sole
non-System client is the pinned broker service SID. Service configuration, pipe
DACLs, resolved SIDs, enabled privileges, binary pins, protocol constants, and
bounds are all verifier-observed receipt fields, not caller assertions.

## Component ownership

| Component | Owns | Must not own |
| --- | --- | --- |
| Coordinator | Request authority, exact packet and command construction, strict receipt validation, typed JSONL parsing, workflow conclusions | Process creation, child handles, direct kill, isolation assertions, verifier key material |
| Broker | One launch ID, request of one verifier-held start reservation, final boundary construction, process creation, stdio handles, wait, cancellation, termination, cleanup | Workflow authority, arbitrary commands, repository discovery, verifier key material, generic signing |
| Verifier | Machine-exclusive pre-create start reservation, independent kernel observation, and fixed receipt issuance under a service-only key | Process creation, caller-authored isolation facts, caller-selected domains or payloads, workflow authority |
| Workload | Exact frozen command and packet inside the contracted boundary | Broker/verifier IPC, credentials, caller profile, unlisted paths, unrestricted child creation or tool network |

The coordinator may receive a PID for evidence but never a process or job handle
that permits it to bypass broker lifecycle ownership. Cancellation and status
queries go through the broker and remain bound to the original launch ID.

## Strict documents

All documents reject duplicate keys, missing fields, unknown fields,
non-finite numbers, and non-canonical bytes. Use UTF-8 compact sorted-key
ASCII-escaped JSON:

```python
json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
```

Every self-digested document computes `digest` from the canonical object with
only its own root `digest` omitted.

### Launch request

Use `mythic_edge_role_pool_broker_launch_request.v1`. It must bind:

- unique `launch_id`, `attempt_series_id`, `sequence_index`, idempotency key,
  current request digest, canary exception digest when applicable, expiry, and
  the current independently observed broker and verifier service-instance epoch
  IDs. Each is a fresh unpredictable value on every service-process start, not
  merely an OS boot ID;
- production launcher identity and exact broker/verifier identity pins;
- complete launcher preflight and selected executable path, SHA-256, byte
  length, CLI version, exact argument array, and argument-array digest;
- exact packet path, SHA-256, byte length, and statement that packet-file bytes
  equal stdin bytes;
- output-schema and child-script paths, SHA-256 values, and byte lengths;
- exact working directory, one scoped allowed namespace root, read-only roots
  wholly inside that namespace, sole writable OS-temporary scope, denied-
  repository policy ID/digest, and cleanup requirement. No denied repository
  path is placed in the request or exposed to the workload;
- exact child environment keys and digest, with no credential-like ambient
  values and no caller profile access;
- token/AppContainer, job, handle, filesystem, network, process-count, timeout,
  and control-plane policy IDs plus their canonical digests;
- one root workload start, the exact allowed tool-descendant count, no nested
  agent, no relaunch, and no shell mediation; and
- current authority and intended use `stage4_evidence_only` or a later
  separately reviewed role-pool mode.

The request contains no fixture content, hostile text, secret marker, verifier
key, expected tag, arbitrary attestation domain, or workflow conclusion.

### Start reservation

Use `mythic_edge_role_pool_broker_start_reservation.v1`. Before any process
creation, the verifier atomically reserves the tuple of authority digest,
attempt-series ID, sequence index, idempotency key, launch ID, launch-request
digest, broker epoch, and verifier epoch. Within one verifier epoch, any repeat
or conflicting tuple returns the existing non-starting status and cannot create
another reservation. The verifier, not the broker, owns this protected in-memory
reservation state so it survives a broker crash.

This start reservation is an isolation-level one-shot authority token. It is not
a Role Pool scheduling claim, lease, or lane reservation and does not increment
those workflow counters.

The reservation is valid only for its exact broker epoch and is consumed by
binding one non-reusable kernel process identity. A broker restart changes the
broker epoch and cannot reuse it. A verifier restart changes the verifier epoch,
invalidates the request, permanently closes the current attempt as unknown, and
requires fresh user authority, attempt series, request, and packet; it never
permits the coordinator to mint a replacement request for the same attempt.

### Boundary-ready receipt

Use `mythic_edge_role_pool_broker_boundary_ready_receipt.v1`. The verifier must
construct it from independent observation of the exact broker-created,
suspended process. It binds:

- launch-request, start-reservation, and launch-ID digests;
- broker service SID, PID, binary path/hash/length, installation identity, and
  provider ID;
- verifier service SID, PID, binary path/hash/length, installation identity,
  key ID, and evidence-source ID;
- child PID plus creation time or another non-reusable kernel process identity;
- exact executable, command, packet, environment, workspace, and writable-root
  bindings;
- observed token/AppContainer identity, final job membership and limits,
  no-breakaway and kill-on-close policy, explicit inherited-handle set,
  filesystem ACL/capability state, network policy, and process limits;
- `primary_thread_suspended=true`, `process_created_count=1`, and
  `process_resumed_count=0`;
- observation/expiry times, fixed receipt domain, attestation algorithm and
  key ID, attestation bytes, and self-digest.

This receipt authorizes the broker to resume only that exact primary thread. It
does not prove the process is running and cannot be reused for another process.

### Start receipt

Use `mythic_edge_role_pool_broker_start_receipt.v1`. It binds the exact start
reservation and boundary-ready receipt and adds the broker-observed single resume result,
start time, process identity, `process_created_count=1`,
`process_resumed_count=1`, `relaunch_attempted=false`, and a fresh independent
post-resume observation of the same process and job. The verifier constructs
and authenticates the fixed receipt; the broker cannot supply arbitrary fields
for signing.

A start receipt proves one exact process was created and resumed inside the
observed boundary. It does not prove the process is still running. A running
claim requires a fresh broker/verifier status observation.

### Terminal receipt

Use `mythic_edge_role_pool_broker_terminal_receipt.v1`. It binds the exact
start receipt and records:

- terminal status and reason, completion time, exit code, timeout and explicit
  cancellation state;
- stdout/stderr SHA-256 and lengths, with content returned only in bounded
  in-memory response channels and never embedded in the receipt;
- final process/job counts, job termination result where applicable, writable
  scope cleanup result, and zero remaining tracked process and temporary-file
  counts;
- `process_created_count=1`, `process_resumed_count=1`,
  `relaunch_attempted=false`, and the original launch ID; and
- a fresh verifier-constructed terminal observation, fixed domain,
  attestation, and self-digest.

The broker owns wait, timeout termination, cancellation, stream draining, and
job cleanup. The coordinator must not call `kill`, `terminate`, or `Popen` for
the workload.

### Abort receipt

Use `mythic_edge_role_pool_broker_abort_receipt.v1` when a reservation was
created but the normal start-to-terminal chain did not complete. The verifier
constructs it from the launch request, start reservation, latest valid
boundary-ready or start receipt when one exists, exact process identity and
created/resumed counts, first failed stage, sanitized reason, termination
observation, zero-survivor observation, and temporary-scope cleanup result. It
distinguishes `definitive_not_started`, `created_never_resumed`,
`resumed_without_start_receipt`, and `started_then_aborted`.

An abort receipt is failure/cleanup evidence, never launch success. If the
verifier cannot construct it from independent observations, the outcome is
`unknown`; broker assertions alone cannot close the attempt.

### Reconciliation receipt

Use `mythic_edge_role_pool_broker_reconciliation_receipt.v1` for read-only
status lookup. Its state is exactly one of `definitive_not_started`, `started`,
`terminal`, `aborted`, or `unknown`. It binds the original launch ID and request
digest and, when present, the exact start, terminal, or abort receipt digest.
Lookup never creates, resumes, cancels, or relaunches a process.

## Atomic launch sequence

The only valid order is:

1. coordinator strictly validates authority, exception, preflight, packet,
   command, environment, schema, and all exact byte bindings;
2. coordinator calls the fixed local broker `start_once` operation once;
3. broker applies the fixed pre-parse IPC authentication and independently
   revalidates its own identity/configuration pins, canonical request bytes,
   expiry, epochs, launch ID, and caller executable binding;
4. broker resolves every executable, packet, script, schema, working-directory,
   fixture, and allowed-root path without following reparse points; opens
   identity-bound handles that deny write and delete sharing; hashes and verifies
   the files through those handles; and keeps them open until the child is
   terminal or aborted, then closes them before temporary-scope cleanup;
5. broker asks the verifier to atomically issue the exact start reservation
   before its first process-creation call; a duplicate or conflicting authority
   can return read-only status but can never create a second process;
6. broker prepares the final protected writable scope, scoped read-only path access,
   network policy, restricted token/AppContainer, job limits, and explicit
   inherited handles;
7. broker creates the exact child suspended with job and security attributes
   applied at creation; no child instruction may run outside the boundary;
8. broker atomically binds the reservation to the child's non-reusable kernel
   identity, after which that reservation can never authorize another child;
9. verifier independently observes the exact suspended child and constructs a
   valid boundary-ready receipt;
10. broker validates that receipt, proves every verifier observation handle is
    closed, and resumes the exact primary thread once;
11. verifier independently observes the same resumed process and constructs the
   start receipt; failure terminates the same job, returns no live evidence,
   permits no relaunch, and returns an abort receipt only when independently
   observable;
12. broker alone waits, responds to explicit cancellation, drains bounded
    streams, cleans the exact temporary scope, and returns the terminal or abort
    receipt;
13. coordinator validates the complete applicable reservation/receipt chain,
    its exact byte and process bindings,
    the returned stream hashes, child JSONL, typed output, and before/after
    state before drawing any Stage-4 conclusion.

There is no fallback from a broker failure to direct `subprocess.Popen`.

## Isolation policy

The broker implementation must prove these properties for the exact child and
all descendants:

- final restricted token/AppContainer or an independently reviewed equivalent;
- job assignment at creation, no breakaway, kill-on-last-broker-handle, and
  exact active-process and descendant-start limits. The broker owns the sole
  non-inheritable job handle; the coordinator, verifier, child, and every other
  process receive no duplicate. The verifier may use only bounded query handles
  and must close all of them before issuing boundary-ready/start evidence;
- no inherited handle except the exact stdin/stdout/stderr and explicitly
  reviewed runtime handles;
- one scoped allowed namespace, with the working directory and every read-only
  root inside it; exactly one writable OS-temporary scope; no reparse traversal;
  and no caller credential or profile access. Using a common ancestor that
  contains another repository is forbidden. The broker resolves the denied-
  repository policy from trusted local configuration and rejects any allowed
  root equal to or ancestral to a denied path without disclosing that path to
  the child;
- no network for tool descendants; Codex control-plane transport is separately
  identified and cannot be inherited or used by tool processes;
- exact executable, arguments, working directory, environment, packet, child
  script, and output schema; and
- no persistent launch journal for the Stage-4 `mutation_scope=none` path.
  The broker may use protected in-memory state and kernel objects, while the
  independent verifier retains the pre-create reservation for its service
  epoch. On broker failure, its sole job handle closes and must contain the
  process tree; lost status becomes `unknown` and is never reconstructed as
  success.

An implementation may choose the reviewed Windows APIs that satisfy these
properties. Experimental sandbox APIs are not a required or accepted shortcut.

## Verifier issuance boundary

The current verifier v1 `VerifyAllowlistedAttestation` operation is not a
positive evidence producer. Do not enable its existing client and do not invert
`verify(domain, payload, tag)` into a signing endpoint.

A separately reviewed protocol version must add fixed broker-only operations
for the exact reservation, boundary-ready, start, terminal, and abort schemas.
Each operation must:

- accept connections only from the pinned broker service SID and independently
  bind the broker SCM PID, pipe-server PID, binary path/hash/length,
  installation identity, and restricted service configuration;
- accept only a launch ID plus bounded query-only kernel-observation handles or
  identities needed to locate the exact process and policy; never accept or
  duplicate a job handle, and never accept a caller-selected
  domain, arbitrary canonical payload, asserted isolation booleans, or expected
  tag;
- independently recompute every emitted field from pinned request bytes and
  kernel state, construct the canonical receipt itself, and issue only the
  compiled receipt domain;
- use one-time challenge/replay state and exact PID-plus-creation identity;
- return the exact typed receipt and its authentication value, never key bytes,
  a generic MAC, or a tag for caller-authored bytes; and
- fail closed on stale identity, duplicate issuance, observation uncertainty,
  broker/verifier drift, or any policy mismatch.

Prefer a distinct broker-only issuance pipe. The existing operator-accessible
verify-only pipe may remain unchanged for its current health and verification
operations.

## Lifecycle and recovery

Use this state machine:

```text
validated
  -> start_reserved
  -> definitive_not_started | start_unknown | boundary_ready
boundary_ready
  -> abort_receipt | started
started
  -> running_observed | terminal | abort_receipt
running_observed
  -> terminal | abort_receipt
terminal
  -> result_validated
  -> routing_recorded
  -> released
abort_receipt
  -> reconciliation_recorded
  -> released
```

Rules:

- a broker-call timeout is `start_unknown`, not proof of no start;
- the coordinator never calls `start_once` again for the same or a replacement
  launch ID in the same authorized attempt;
- read-only reconciliation may query the original launch ID but cannot create
  or resume a process;
- a polling timeout does not authorize cancellation or relaunch;
- explicit cancellation and an execution deadline ask the broker to terminate
  only the same job and return a terminal receipt when a start receipt exists,
  otherwise an abort receipt; unavailable independent evidence remains unknown;
- missing, invalid, or unknown start/terminal evidence routes to
  reconciliation and preserves the original claim/attempt state;
- a broker crash must terminate the contained job through handle ownership; if
  the parent cannot prove that result, the outcome remains unknown; and
- a later attempt requires fresh user authority, packet, exception, launch ID,
  attempt series, and evidence. It is never an automatic retry; and
- a broker restart invalidates its old epoch, while the verifier-held reservation
  rejects replay; a verifier restart invalidates the whole request and closes
  the attempt unknown rather than enabling replacement authority.

The process-local Python `SingleStartGuard` may remain as defense in depth in
the parent. It is not the machine-exclusive launch authority and cannot prove
broker exactly-once behavior.

## Reconciliation with the direct launcher

The current `scripts/codex_launcher_contract.py` is fail-closed migration code.
Its public direct launcher validates legacy inputs and then refuses process
creation; its receipt validator rejects both a direct-Popen production claim and
a broker claim represented by the legacy receipt schema. The current pool-plan
validator likewise rejects direct Popen for production and explicitly blocks
the broker backend until the receipt-chain implementation exists. Do not
provision `ProductionVerificationContext` or connect that placeholder to the
verifier.

The Codex C implementation must make these migrations together:

1. introduce an opaque, pinned broker client and `broker_launch_once`; the
   coordinator prepares the same exact arguments and packet but makes no
   process-creation call;
2. preserve the now-enforced rule that every direct `subprocess_popen` receipt
   is production-ineligible and retain the injected process factory only in
   private deterministic tests;
3. accept `windows_isolation_broker` as the only Stage-4/live-capable backend
   and `codex:broker-single-start/v1` as its launcher identity;
4. replace the pre-creation
   `mythic_edge_role_pool_external_isolation.v3` production claim with the exact
   reservation/boundary-ready/start/terminal-or-abort receipt chain; v3 may
   remain non-live policy input during migration;
5. move timeout, kill, wait, stream-drain, and cleanup ownership from Python's
   `Popen` object to the broker protocol;
6. replace the current explicit broker-not-implemented validation error with
   strict reservation/boundary-ready/start/terminal/abort validation across
   launcher sidecars, plan/result projections, and active-runtime evidence;
7. require a start receipt for `running` and a terminal receipt for completed
   output; never infer one from the other; and
8. keep `gpt-5.6-sol` and `max` advisory, with the platform-default fallback
   unchanged and never treated as an isolation or authority gate.

Until all eight changes pass focused tests and independent review, the current
runtime is `NOT LIVE-READY` and no Stage-4 broker launch is authorized.

## Stage-4 use

The broker may support the standalone Stage-4 exception only after its
implementation, verifier issuance protocol, exact pins, adversarial tests, and
independent review are accepted. A valid current canary request and exception
remain mandatory; broker evidence cannot supply them.

For the Stage-4 `mutation_scope=none` path:

- use one request, one launch ID, one process creation, one resume, and no
  relaunch;
- permit only the exact pre-provisioned packet, child script, schema, named fake
  fixture, scoped authorized-repository namespace, and OS-temporary writable
  scope; never use a shared parent directory as the working/read-only root;
- deny the named unlisted repository before any request and provide no path for
  it;
- record zero workflow claims, scheduling reservations, pooled launches, nested
  agents, persistent writes, repository/GitHub writes, credentials, external
  mutations, stage advancement, and finding-resolution actions. The verifier's
  in-memory start reservation is recorded separately and grants none of those
  workflow authorities;
- return typed output and complete broker/verifier receipts without raw fixture
  or matched content; and
- clean the entire temporary scope before accepting the observation.

Real second-host rejection, reboot continuity, and full
install/rollback/uninstall-cycle evidence remain later production and
live-readiness concerns. This contract does not silently add them to the
evidence-only Stage-4 canary gate. It also does not waive them for later live
dispatch.

## Implementation and review acceptance

Before any broker-backed Stage-4 observation, require deterministic and
adversarial evidence for:

- strict request and receipt schemas, canonical bytes, self-digests,
  authentication, freshness, replay denial, and exact cross-document bindings;
- verifier-held pre-create reservation behavior, exact broker/verifier epoch
  invalidation, and no second child after broker restart;
- broker-only creation with no reachable coordinator `Popen` or fallback;
- creation-time boundary installation and no child execution before the
  boundary-ready receipt;
- wrong executable/packet/script/schema/argument/environment/path/token/job/
  handle/network/process-limit rejection before resume;
- verifier construction of fixed receipts and rejection of generic signing,
  caller-selected domains/payloads, operator issuance, stale PID reuse, and
  duplicate issuance;
- exact one-start behavior across concurrent callers, parent timeout, lost
  response, and broker crash within one verifier epoch; fail-closed invalidation
  without retry across verifier restart/failure, child timeout, cancellation,
  and cleanup failure;
- job crash containment, zero surviving descendants, sole writable-scope
  enforcement, tool-network denial, credential/profile denial, and temporary
  cleanup;
- reservation-versus-start-versus-running-versus-terminal/abort receipt
  semantics and read-only reconciliation; and
- unchanged Stage-4 authority, no-mutation counters, fallback pickup, and
  advisory model/effort behavior.

Run the Role Pool offline gate after implementation, freeze new broker and
verifier inventories last, and submit the exact bytes, tests, threat model,
install/audit evidence where separately authorized, and before/after Role Pool
manifest to an independent Codex E review. Contract acceptance alone grants no
activation or execution authority.
