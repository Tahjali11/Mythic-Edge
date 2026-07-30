# Trusted-Owner Native Role Pool Profile Contract

Status: `review_pending`

Risk tier: `high`

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/744

Current tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

Predecessor roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

Controlling owner decision:
https://github.com/Tahjali11/Mythic-Edge/issues/744#issuecomment-5109379065

Windows-first owner directive:
https://github.com/Tahjali11/Mythic-Edge/issues/744#issuecomment-5111260293

App Server baseline amendment source:
https://github.com/Tahjali11/Mythic-Edge/issues/758

Accepted amendment predecessor SHA-256:
`eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc`

Security cross-links:

- https://github.com/Tahjali11/Mythic-Edge-Security/issues/116
- https://github.com/Tahjali11/Mythic-Edge-Security/issues/117
- https://github.com/Tahjali11/Mythic-Edge-Security/issues/118
- https://github.com/Tahjali11/Mythic-Edge-Security/issues/139
- https://github.com/Tahjali11/Mythic-Edge-Security/issues/140
- https://github.com/Tahjali11/Mythic-Edge-Security/issues/141

## Findings And Current Authority

Observed against Core `origin/main`
`0e58eacfe5f0530880c36adfc529c64f08525e79`:

- The installed Role Pool `SKILL.md` is an ordinary file with SHA-256
  `130ce02b6f5eb8ec740642b67877bb0ecc33ab2ca8af17d16f76b2b3cee2756d`.
- Core has no canonical repository-owned `mythic-edge-role-pool` source.
- Owner-wide GitHub code search found no other tracked canonical source.
- Open PRs #374 and #391 have no current parked or deferred disposition.
- No open issue or PR duplicates this exact contract-authoring scope.
- ADR-0010 and ADR-0011 are Proposed and non-precedential. This contract does
  not treat either as accepted authority.

Codex E reviewed predecessor SHA-256
`d63e0d90ff2a2255ee381ddf5a8194467a33f103d9f51a3604f35d8bb7cb49f6`
and opened five contract-closure findings. Codex E then re-reviewed SHA-256
`8ad1fac753ba2618fe4461c029904d1733fe71e05e05d00afc6dd1479c6a6d98`,
confirmed `ME-RP-744-E-001` and `ME-RP-744-E-003`, retained
`ME-RP-744-E-002`, `ME-RP-744-E-004`, and `ME-RP-744-E-005`, and opened
`ME-RP-744-E-006`. The accepted predecessor addressed those blockers together:

| Finding | Contract disposition |
| --- | --- |
| `ME-RP-744-E-001` | Separate client-known immutable claim-event bytes from the server-assigned GitHub observation. |
| `ME-RP-744-E-002` | Close every packet, nested record, scalar type, field order, canonicalization rule, and self-digest preimage. |
| `ME-RP-744-E-003` | Derive contention and capacity from one complete project-wide GitHub claim snapshot with exact resource keys. |
| `ME-RP-744-E-004` | Add ordered terminal selection and one canonical release-state advancement chain; reorder the ladder. |
| `ME-RP-744-E-005` | Inventory and disposition all 50 observed installed-tree files and map all retained V5 protection families. |
| `ME-RP-744-E-006` | Bind every accepted scheduling comment to an immutable GitHub author ID admitted by the active registry. |

The Windows-first amendment timing gate is satisfied:

- Codex C completed the inert implementation against the exact accepted
  predecessor and produced
  `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`
  with artifact SHA-256
  `c0bcbb87bdd21b897293fd6dfcd3ab0cc52445bd4edf1f73ddac69ae9dacf649`.
- Codex E independently reviewed those exact implementation bytes. Its
  `final_implementation_confirmation` report is
  `docs/contract_test_reports/trusted_owner_native_role_pool_profile.md` with
  artifact SHA-256
  `7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8`.
- The terminal implementation verdict is
  `accepted_exact_inert_trusted_owner_native_profile_candidate`; findings
  `ME-RP-744-E-007` through `ME-RP-744-E-011` are `fixed_confirmed`.
- The accepted 34-file canonical implementation manifest SHA-256 is
  `f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7`.

No implementation defect remains routed through D -> E for those bytes. This
amendment changes platform scope only and does not reinterpret, edit, or
supersede the accepted implementation evidence.

Issue #757 and PR #759 are integrated on Core `origin/main`
`26ca98ce81c0f393bf1ec9df470c10ae911c01f7`. The accepted metadata-only
capability verdict remains `insufficient_evidence`: all nine production
capability facts remain unestablished and all operational counts remain zero.
Issue #758 supplies the separately activated contract lane for one candidate
production realization. It does not reinterpret the #757 result as support.

The current owner instruction is the required ADR-0008
`explicit_user_override` for this bounded Codex B lane:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #758 Windows App Server baseline contract"
  blocked_active_issue_or_pr:
    - "PR #374, open draft with no current parked/deferred record"
    - "PR #391, open Dependabot PR with no current parked/deferred record"
  reason: "The owner explicitly authorized one docs-only App Server profile amendment and companion lifecycle contract after #757 integration."
  allowed_scope:
    - "read-only authority, issue, PR, release-metadata, and source-schema inspection"
    - "revise only docs/contracts/trusted_owner_native_role_pool_profile.md"
    - "create only docs/contracts/role_pool_codex_app_server_native_task_adapter.md"
    - "run local read-only validation"
    - "produce one independent Codex E review handoff"
  expiration_condition: "Both contracts and the Codex E handoff are complete, or the owner revokes or redirects the lane."
  authorized_by: "Tahjali11 current user instruction"
  recorded_in: "this contract"
```

This exception grants no implementation, installation, dispatch, canary,
submission, merge, deployment, or Stage 4 authority.

## Module And Truth Ownership

Module: trusted-owner native Role Pool dispatch policy.

Owning layer: repository coordination and agent workflow.

Internal project area: Quality / Governance.

Truth owner:

- Core owns the canonical skill source, repository registry schema, transition
  policy, command policy, validators, and release ladder.
- Each named repository owns its issue, role authority, protected surfaces,
  validation commands, branch policy, and mutation permission.
- GitHub owns the server timestamps, immutable comment identifiers, and
  immutable author IDs used to authenticate and order independent
  registered-coordinator scheduling claims.
- The external-isolation contracts and accepted evidence own containment,
  broker, verifier, and malicious-content claims.

Bridge-code status: `shared_support`.

The profile coordinates repository-owned workflows. It does not own parser,
workbook, webhook, analytics, credential, deployment, or production truth.

## Contract Decision

This contract defines two separate profiles:

1. `trusted_owner_native`
2. `external_isolation`

Only `trusted_owner_native` is specified for implementation here.
`external_isolation` remains governed by its existing and future Security
contracts.

The initial `trusted_owner_native` execution host is Windows only. Native Mac
dispatch is deferred and is not an activation prerequisite for the Windows
profile.

The trusted-owner native profile is allowed only when every lane:

- names an exact active repository-registry entry;
- binds the repository's immutable GitHub identity and current canonical name;
- requests one permitted role and operation;
- uses only repository-approved commands;
- remains within the entry's read, mutation, protected-surface, and external
  effect ceilings; and
- has no trigger requiring external isolation.

Allowlist membership is eligibility, not execution or mutation authority.

If any lane requires external isolation, version 1 rejects the whole native
wave. It does not split, downgrade, or partially launch that wave. The caller
must submit a separate stronger-profile request.

The sole positive profile claim defined by this contract is:

`trusted_owner_native_profile_ready`

That claim is false until the complete graduated release ladder in this
contract is accepted. It never means global live readiness, security
assurance, external-isolation readiness, deployment readiness, or Stage 4
completion.

## Windows-First Execution Platform Scope

The dispatch host is the machine on which this profile would publish a claim,
create a worktree or task, run an approved command, or make another persistent
workflow mutation. For initial installation, live validation, canaries, and
every `R0` through `R8` advancement, the only supported dispatch host is
Windows.

The trusted runtime observes the host before caller input is interpreted for
dispatch. The host is supported only when the running Python process reports
both `os.name == "nt"` and `sys.platform == "win32"`. A missing value,
disagreement, alternate value, or observation failure is unsupported. The
request, registry, lane, claim, worktree, task, result, and release schemas
contain no caller-controlled platform selector. Adding one is an unknown-field
failure. Tests may inject a closed observer double, but production dispatch
must use the runtime observation and may not accept a caller override.

A Mac used only as a remote-control client for a process executing on the
Windows Desktop is Windows-hosted execution because the trusted runtime
observation is made on Windows. A process executing natively on macOS is a
non-Windows dispatch attempt and is unsupported by this profile.

Before claim publication, worktree or task creation, command execution, release
state advancement, installer staging, or any other persistent workflow
mutation, the dispatcher must:

1. confirm the trusted runtime observation is exactly Windows;
2. confirm the exact first-party task boundary
   `codex:native-task-create/v1` is present and compatible with the request,
   one-task, receipt, timeout, unknown-outcome, and no-retry guarantees in this
   contract; and
3. reject before side effects if either check is false or unavailable.

That rejection selects the existing priority-1 terminal outcome
`blocked_request_or_packet_invalid`. This outcome is sufficient because its
preclaim purpose is to reject an execution request whose current trusted
runtime cannot satisfy the contract. No platform value needs to enter a packet,
receipt, digest, lifecycle, or release record. The existing 20-outcome
vocabulary, all schemas, all field counts, and all self-digest preimages remain
unchanged.

An unsupported host or missing or incompatible Windows primitive never
activates the broker, `codex exec`, shell execution, Python `subprocess`, a
repository executable, a weaker receipt, or another fallback. It publishes no
claim, creates no worktree or task, runs no command, and makes no persistent
workflow mutation. It routes to Codex A or B for reconciliation.

Platform-neutral offline parsing, canonicalization, schema validation,
selector audits, source/install `--check`, and pure-function tests may remain
available when they create no claim, task, worktree, Role Pool lane-command
execution, or persistent external mutation. The validator process itself may
run, but it may not invoke the native task adapter, an approved lane command, a
shell or subprocess launcher, or an external mutation. Its results are
validation evidence only. A non-Windows result cannot independently satisfy
Windows installation, live validation, canary, or rung-advancement evidence.

Native Mac support requires a separate issue, an accepted contract amendment
or profile, independent Codex E review, a fresh owner activation decision, and
its own graduated evidence. It does not inherit Windows installation,
contention, canary, or `R0` through `R8` evidence automatically.

## Dedicated App Server Process Realization

The public launcher identity remains exactly
`codex:native-task-create/v1`. The only candidate production realization
admitted by this amendment is the Core-owned
`codex:app-server-stdio-direct/v1` adapter defined by
`docs/contracts/role_pool_codex_app_server_native_task_adapter.md`.
The realization is an implementation behind the existing identity, not a
fallback, alternate profile, repository command, or second task surface.

That companion contract may authorize a later implementation to expose one
private, dedicated, non-shell process-start function. The function has no
caller-selected executable, arguments, environment, transport, working
directory, or cardinality. It may start only the pinned Windows Codex
`0.146.0` CLI asset with the exact argument vector `app-server`, `--listen`,
`stdio://`, once for one validated lane. It is private to the adapter and must
not be exported or reused as a general process, subprocess, command, SDK,
broker, service, or launcher capability.

This narrow process exception does not weaken the general prohibition on
shells, `codex exec`, ambient executable discovery, repository executables,
generic subagents, the external broker, or alternate App Server executables.
A missing, drifting, failed, timed-out, or ambiguous pinned process never
selects another launcher.

The closed `trusted_owner_native_task_request.v1` remains unchanged. The
companion derives one App Server execution binding from the validated request
and the exact objects already reachable through its digests: the parent
request, lane packet, worktree observation, registry entry and command
records, profile, release-state record, skill tree, and predecessor packet.
App Server-specific values that are fixed by contract or deterministically
derived at runtime do not become caller-controlled request fields. The
existing `trusted_owner_native_task_receipt.v1` also remains unchanged; its
`platform_receipt_ref` and `platform_receipt_sha256` bind the companion's
public-safe App Server lifecycle receipt.

The initial App Server realization is a strict inspect-only baseline. It
accepts only a B or E lane whose active registry entry has
`repository_code_execution_policy=forbidden` and whose `command_ids`,
`validation_command_ids`, `mutation_scope`, `expected_artifact_paths`,
`maximum_mutation_scope`, and `approved_commands` arrays are all empty. Its
turn is read-only. Its exact private runtime config disables the shell and
other named effectful tool surfaces. The adapter grants no command or
file-change approval, and any command, file-change, patch, diff, or changed
file is a known lane failure.

This restriction does not weaken the profile's exact repository-command or
mutation rules: the candidate executes neither. A lane requiring either
effect is unsupported by this realization and stops before consumption. A
later effectful realization requires a separate issue, contract amendment,
independent Codex E review, fresh owner decision, and graduated evidence. It
cannot inherit the inspect-only observation as command or mutation evidence.

The candidate does not satisfy #757 by definition. Support remains
`insufficient_evidence` until the companion contract is independently
accepted, its exact inert implementation and fake transport are independently
accepted, installation custody is separately authorized and verified, and a
separately authorized `R2` real-surface characterization establishes all nine
#757 facts. `R0` permits only fake-transport validation and starts no Codex
process. `R1` remains inspect-only and starts no Codex process. The R2
characterization proves only the inspect-only task lifecycle. It grants no
command, mutation, R3-R8, installation, dispatch, or readiness authority.

## Canonical Source And Installation Synchronization

The future canonical Core-owned source root is:

`docs/codex_skills/mythic-edge-role-pool/`

The future repository registry is:

`docs/role_pool/trusted_owner_repository_registry.v1.json`

Neither path is created or populated by this contract.

The installed copy under the user's Codex skills directory is a deployment
copy. It must never become source authority and must never be edited in place.

The observed installed tree contains 50 files. The migration inventory below
classifies 34 as managed source inputs and 16 as generated Python bytecode
cache. The canonical source initially contains exactly the 34 managed paths.
No `__pycache__`, `.pyc`, runtime result, receipt, log, or machine-local file is
source.

The canonical managed tree digest is derived as follows:

1. Reject symlinks, junctions, reparse points, duplicate normalized paths, and
   paths outside the source root.
2. Reject every path not explicitly owned by the reviewed managed inventory.
3. Sort relative POSIX paths by ordinal UTF-8 byte order.
4. For each ordinary managed file, append a canonical JSON line with exactly
   `path`, `byte_count`, and `sha256`.
5. Encode each object as UTF-8 without BOM, with keys in the stated order, no
   insignificant whitespace, and one LF after every row.
6. SHA-256 the complete manifest bytes.

The installed-tree check requires the exact same managed paths, bytes, and
digest and rejects every extra or missing path. Native validators and dispatch
run with Python bytecode writes disabled. Therefore a regenerated
`__pycache__`, `.pyc`, or other unowned installed path is drift, not an ignored
extra. Before every native invocation, source and installed digests must equal
each other and the reviewed release binding.

The existing `tools/install_codex_skills.py` remains the installation owner.
Its successor interface must provide:

- `--check --skill mythic-edge-role-pool`: read-only result of
  `identical`, `missing`, `drift`, or `unsafe`; this check may run
  platform-neutrally;
- existing install-only behavior for a missing destination, gated to the
  trusted observed Windows host before destination creation;
- a separately authorized `--sync --skill mythic-edge-role-pool` operation
  for reviewed updates, gated to the trusted observed Windows host before
  staging or destination mutation; and
- staging, readback, atomic replacement, rollback, and final drift validation
  for synchronization.

`--sync` is not authorized by this contract. A missing, drifting, unsafe, or
unreviewed installed tree blocks native dispatch with
`blocked_skill_source_drift`.

## Canonical Packet Rules

Every JSON object defined by this contract uses the field order listed in its
schema. Unknown or duplicate fields are rejected before semantic validation.
Strings are NFC-normalized UTF-8, but path and identity values that are not
already NFC are rejected rather than rewritten. Integers are base-10 JSON
integers; floats are forbidden. Booleans are JSON `true` or `false`. Null is
allowed only where a schema says `or null`.

The following closed scalar types apply:

| Type | Exact form |
| --- | --- |
| `sha256` | 64 lowercase hexadecimal characters. |
| `git_sha` | 40 lowercase hexadecimal characters. |
| `id` | 1-128 ASCII characters matching `[a-z0-9][a-z0-9._:-]*`. |
| `repository_name` | Lowercase `owner/repository`, each component matching `[a-z0-9][a-z0-9._-]*`. |
| `relative_path` | Nonempty POSIX relative path; no empty, `.`, `..`, backslash, drive, UNC, wildcard, or NUL component. |
| `utc_second` | RFC 3339 `YYYY-MM-DDTHH:MM:SSZ`. |
| `github_url` | Exact lowercase-identity `https://github.com/<owner>/<repository>/issues/<positive integer>`. |
| `ascii_name` | 1-64 ASCII characters matching `[A-Z_][A-Z0-9_]*`. |
| `public_ref` | 1-512 NFC Unicode scalar values; no C0/C1 control, NUL, CR, LF, or leading/trailing ASCII whitespace. |
| `bounded_text` | 1-1024 NFC Unicode scalar values; no C0/C1 control, NUL, CR, or LF. |
| `argument_literal` | 0-4096 NFC Unicode scalar values; no C0/C1 control, NUL, CR, or LF; passed as exactly one argv element and never shell-parsed. |
| `git_ref` | 1-255 ASCII characters matching `[A-Za-z0-9][A-Za-z0-9._/-]*`; no `..`, `//`, `@{`, trailing `.`, trailing `/`, or `.lock` component. |
| `resource_key` | One exact `project:trusted_owner_native:v1`, `wave_slot:<1|2>`, `repository:<positive integer>`, `issue:<positive integer>:<positive integer>`, or `lane:<id>` value. |

Unless a schema says otherwise, arrays are ordinally sorted, contain no
duplicates, and retain that order in canonical bytes. Objects are serialized
as one line with no insignificant whitespace, UTF-8 without BOM, and exactly
one final LF.

Every `*_sha256` self-digest named by a schema is its final field. Its preimage
is the complete canonical object with only that member omitted. Every other
member and the final LF remain. SHA-256 is calculated over that exact byte
sequence. The complete artifact retains the self-digest member and final LF.

## Repository Registry

The registry root contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_repository_registry.v1`. |
| `profile_id` | string | Exactly `trusted_owner_native`. |
| `coordination_repository_id` | positive integer | Immutable GitHub repository ID for the scheduling surface. |
| `coordination_repository_name` | `repository_name` | Current canonical name matching that immutable ID. |
| `coordination_issue_number` | positive integer | One dedicated open scheduling issue in that repository. |
| `authorized_claim_actor_ids` | positive integer array | Nonempty, ordinally sorted, unique immutable GitHub user IDs permitted to author scheduling events. |
| `release_state_path` | `relative_path` | Exactly `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`. |
| `entries` | entry array | Sorted by `repository_id`; one or more. |
| `registry_sha256` | `sha256` | Self-digest. |

Each entry contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_repository_entry.v1`. |
| `repository_id` | positive integer | Immutable GitHub repository ID. |
| `canonical_name` | `repository_name` | Exact current identity; no wildcard or alias. |
| `status` | enum | `proposed`, `active`, `suspended`, `revoked`, or `retired`. |
| `trust_basis_refs` | nonempty `public_ref` array | Public reviewed evidence references. |
| `eligible_roles` | nonempty enum array | Ordinal subset of `A`, `B`, `D`, `E`, `F`. |
| `permitted_operations` | nonempty `id` array | Closed operations. |
| `permitted_read_scope` | `relative_path` array | Exact repository-relative roots. |
| `maximum_mutation_scope` | `relative_path` array | Empty means read-only. |
| `repository_code_execution_policy` | enum | `forbidden`, `reviewed_command_set_only`, or `external_isolation_required`. |
| `approved_commands` | command array | Sorted by `command_id`. |
| `protected_surface_restrictions` | `id` array | Exact denied or separately gated surfaces. |
| `external_effect_restrictions` | `id` array | Exact denied or separately gated effects. |
| `approving_authority_ref` | `public_ref` | Public owner or accepted governance decision. |
| `approved_at_utc` | `utc_second` | Acceptance time. |
| `review_triggers` | nonempty `id` array | Must include transfer, identity drift, authority widening, and protected-surface change. |
| `review_due_at_utc` | `utc_second` or null | Null only for event-driven review. |
| `entry_sha256` | `sha256` | Self-digest. |

An approved-command record contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `command_id` | `id` | Unique inside the entry. |
| `role` | enum | One of `A`, `B`, `D`, `E`, `F`. |
| `operation_id` | `id` | Must occur in `permitted_operations`. |
| `executable_ref` | `public_ref` | Repository-approved stable executable identifier; never ambient PATH text. |
| `executable_sha256` | `sha256` or null | Required for a mutable or repository-owned executable. |
| `executable_byte_count` | nonnegative integer or null | Null exactly when `executable_sha256` is null. |
| `argument_template` | argument array | Ordered by contiguous `ordinal` starting at zero. |
| `working_directory_policy` | enum | `worktree_root` or `exact_relative_path`. |
| `working_directory_value` | `relative_path` or null | Required only for `exact_relative_path`. |
| `environment_allowlist` | `ascii_name` array | Sorted, unique, explicit names only. |
| `maximum_runtime_seconds` | positive integer | Hard ceiling. |
| `mutation_scope` | `relative_path` array | Subset of `maximum_mutation_scope`. |
| `external_effects` | `id` array | Must not exceed entry restrictions or current authority. |
| `command_sha256` | `sha256` | Self-digest. |

An argument record contains exactly `ordinal`, `kind`, and `value`.
`ordinal` is a nonnegative integer. `kind` is `literal` or
`typed_placeholder`. For `literal`, `value` is an `argument_literal`. For
`typed_placeholder`, `value` is exactly one of `base_sha`, `branch_name`,
`contract_path`, `evidence_path`, `issue_number`, `output_path`, or
`worktree_path`. Both variants serialize `value` as a JSON string. No
shell-expression placeholder exists.

Every entry requires independent acceptance before `active`. Registry
replacement may transition `proposed -> active|revoked|retired`,
`active -> suspended|revoked|retired`, or
`suspended -> active|revoked|retired`. `revoked` and `retired` are terminal.
No other transition is valid. Suspension, revocation, or retirement prevents
new claims but does not claim running work stopped. Running or unknown work
enters reconciliation.

Rename with unchanged immutable identity requires deterministic reconciliation
and registry review. Transfer, identity mismatch, or authority widening
requires a new independent acceptance. This contract activates no entry.

## Invocation And Lane Packet

A request contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_request.v1`. |
| `request_id` | `id` | Globally unique and never reused. |
| `mode` | enum | `safe` or `automatic`. |
| `automation_series_id` | `id` or null | Null for Safe; one stable ID for an Automatic issue path. |
| `predecessor_request_sha256` | `sha256` or null | Null for Safe and the first Automatic request; otherwise the immediately preceding request. |
| `requested_role` | enum | One of `A`, `B`, `D`, `E`, `F`. |
| `skill_tree_sha256` | `sha256` | Accepted managed source-tree digest. |
| `registry_sha256` | `sha256` | Exact active registry. |
| `release_state_record_sha256` | `sha256` | Current accepted ladder record. |
| `requested_at_utc` | `utc_second` | Request time. |
| `lanes` | lane array | One to three, sorted by `lane_id`. |
| `request_sha256` | `sha256` | Self-digest. |

Each lane contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `lane_id` | `id` | Globally unique lane-series ID; stable only across exact Automatic successor roles for the same issue. |
| `repository_id` | positive integer | Exact active registry entry. |
| `canonical_name` | `repository_name` | Must match the immutable ID. |
| `issue_url` | `github_url` | One open issue dedicated to this lane. |
| `role` | enum | Must equal request `requested_role`. |
| `operation_id` | `id` | Exact registry operation. |
| `base_ref` | `git_ref` | Exact repository-authorized ref. |
| `base_sha` | `git_sha` | Resolved immutable starting commit. |
| `predecessor_packet_sha256` | `sha256` or null | Null only when the role has no predecessor. |
| `command_ids` | `id` array | Sorted unique exact approved commands. |
| `read_scope` | `relative_path` array | Subset of registry read scope. |
| `mutation_scope` | `relative_path` array | Subset of registry mutation scope. |
| `protected_surfaces` | `id` array | Exact current repository classification. |
| `validation_command_ids` | `id` array | Sorted exact approved commands. |
| `expected_artifact_paths` | `relative_path` array | Sorted exact outputs; empty for inspect-only work. |
| `stop_conditions` | nonempty `bounded_text` array | Fixed before claim. |
| `lane_packet_sha256` | `sha256` | Self-digest. |

No request may repeat a repository ID or issue URL. Wildcards, omitted
repositories, aliases, inferred repositories, forks, submodules, sibling
repositories, and transitive authority are rejected.

The first request in a lane series binds one issue not used by another lane.
An Automatic successor may reuse that exact issue and lane ID only when it
binds the immediately preceding released request and accepted result in the
same automation series. The task, worktree, request, packet, and role execution
are fresh at every transition. The task is created only after the new claim
wins. The worktree is created from the exact `base_sha`, is physically
revalidated, and is never shared. No two active lanes share an issue.

Only the predecessor packet may carry information into a lane. A lane may not
read another lane's transcript, worktree, uncommitted files, private state,
claim credentials, or local artifacts. Shared facts first become reviewed
public repository or GitHub artifacts bound by digest.

## Result And Handoff Packet

A result contains these fields in this exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_result.v1`. |
| `request_sha256` | `sha256` | Exact accepted request. |
| `claim_observation_sha256` | `sha256` | Exact winning confirmed claim observation. |
| `wave_id` | `id` | Exact claim wave. |
| `lane_id` | `id` | Exact planned lane. |
| `worktree_observation_sha256` | `sha256` | Exact accepted worktree observation. |
| `task_receipt_sha256` | `sha256` | Exact accepted one-task adapter receipt. |
| `task_id` | `id` | Fresh task identity. |
| `repository_id` | positive integer | Exact lane repository. |
| `issue_url` | `github_url` | Exact lane issue. |
| `role` | enum | Exact lane role. |
| `operation_id` | `id` | Exact lane operation. |
| `base_sha` | `git_sha` | Planned base. |
| `head_sha` | `git_sha` | Observed final head. |
| `result` | enum | `completed`, `blocked`, `finding`, or `unknown`. |
| `files_changed` | file-change array | Sorted by path. |
| `validation` | validation array | Ordered by planned validation command ID. |
| `handoff` | handoff object | Closed schema below. |
| `authority_flags` | authority object | Closed schema below. |
| `result_packet_sha256` | `sha256` | Self-digest. |

A file-change record contains exactly `path`, `change_kind`,
`before_sha256`, and `after_sha256`. `path` is a `relative_path`.
`change_kind` is `added`, `modified`, or `deleted`. `before_sha256` and
`after_sha256` are each `sha256` or null. The before digest is null only for
`added`; the after digest is null only for `deleted`. Paths are unique and the
array is sorted by ordinal path bytes.

A validation record contains exactly `command_id`, `status`, `exit_code`, and
`evidence_sha256`. `command_id` is an `id` equal to one exact lane
`validation_command_ids` member. Status is `passed`, `failed`, `blocked`, or
`not_run`. `exit_code` is an integer for an executed command and null
otherwise. `evidence_sha256` is a `sha256` for executed validation and null
otherwise. The array contains exactly one record for every planned validation
command, in planned order, with no other record.

The handoff object contains exactly `status`, `next_role`,
`source_artifact_paths`, `finding_ids`, `stop_reason`, and `handoff_sha256`.
Status is `complete`, `changes_required`, `blocked`, or `no_next_role`.
`next_role` is `A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, or null.
`source_artifact_paths` is a sorted unique `relative_path` array.
`finding_ids` is a sorted unique `id` array. `stop_reason` is `bounded_text`
or null. `handoff_sha256` is the self-digest.

The result's worktree observation, task receipt, and task ID must cross-bind.
Its embedded handoff must validate to its own `handoff_sha256`. A result with
`result=unknown` is never terminal evidence for release.

The authority object contains exactly these boolean fields in this order:

`repository_mutation_authorized`, `implementation_authorized`,
`publication_authorized`, `merge_authorized`, `deployment_authorized`,
`installation_authorized`, `package_operations_authorized`,
`network_authorized`, `secrets_authorized`,
`external_isolation_authorized`, `canary_authorized`, `stage4_authorized`,
`stage_advancement_authorized`, `dispatch_authorized`, `live_ready`, and
`trusted_owner_native_profile_ready`.

Unknown never means success, never grants authority, and never authorizes
retry.

## Shared GitHub Scheduling Claims

Independent registered Windows coordinators use the same dedicated GitHub
scheduling issue bound by the active registry. A registered coordinator is one
whose scheduling comment has an immutable `server_author_id` admitted by the
active registry and whose public-safe coordinator pseudonym is stable within
one claim chain. Local locks are advisory only.

Each claim or resolution event is one append-only top-level issue comment. The
exact comment body is the canonical event JSON and final LF. Comments are
never edited or deleted. A transition is a new event comment.

A claim event contains client-known fields only:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_claim_event.v1`. |
| `event_id` | `id` | Globally unique and never reused. |
| `claim_id` | `id` | Stable across one claim chain. |
| `predecessor_observation_sha256` | `sha256` or null | Null only for the first `reserved` event. |
| `request_sha256` | `sha256` | Exact request self-digest. |
| `wave_id` | `id` | Unique wave identity. |
| `wave_ordinal` | integer | 1 or 2. |
| `coordinator_id_sha256` | `sha256` | Public-safe coordinator pseudonym. |
| `device_id_sha256` | `sha256` | Public-safe dispatch-host pseudonym; initial accepted live events are Windows-hosted. |
| `lane_ids` | `id` array | One to three, sorted and equal to request lanes. |
| `resource_keys` | `resource_key` array | Exact sorted keys defined below. |
| `state` | enum | `reserved`, `confirmed_running`, `released`, `lost`, `failed`, or `reconciliation_required`. |
| `issued_at_utc` | `utc_second` | Client issuance. |
| `expires_at_utc` | `utc_second` | At most 24 hours later. |
| `terminal_binding` | release-binding object, failure-binding object, or null | State-selected closed union defined below. |
| `event_sha256` | `sha256` | Self-digest. |

Raw host, user, credential, token, path, or device values are forbidden.
Coordinator and device pseudonyms are correlation values only. They grant no
authority and cannot satisfy or override the trusted runtime Windows check.

GitHub assigns server metadata only after publication. Readback derives, but
does not post or edit, this canonical observation:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_claim_observation.v1`. |
| `coordination_repository_id` | positive integer | Registry value. |
| `coordination_issue_number` | positive integer | Registry value. |
| `server_comment_id` | positive integer | GitHub-assigned immutable ID. |
| `server_author_id` | positive integer | Immutable GitHub user ID from comment readback. |
| `server_author_type` | enum | Exactly `User`; bot, app, organization, or unknown authors are rejected. |
| `server_created_at` | `utc_second` | GitHub-assigned creation time. |
| `server_updated_at` | `utc_second` | Must equal `server_created_at`; an edit fails closed. |
| `event_schema_version` | enum | `trusted_owner_native_claim_event.v1` or `trusted_owner_native_claim_resolution_event.v1`. |
| `event_sha256` | `sha256` | Digest validated from exact readback body. |
| `comment_body_byte_count` | positive integer | Exact UTF-8 body length. |
| `comment_body_sha256` | `sha256` | Complete comment-body digest. |
| `claim_observation_sha256` | `sha256` | Self-digest. |

The observation is mechanically reconstructible from the immutable comment and
GitHub metadata and is byte-identical for every complete observer. Local
observation time is runtime evidence and never enters this object or its
digest. No server-assigned value occurs in the event preimage.
An observation is valid only when `server_author_id` occurs exactly once in
the request registry's `authorized_claim_actor_ids`. Every ordinary successor
in one claim chain must have the same `server_author_id` as its reservation.
The separately reviewed resolution event below may be authored by any currently
authorized actor. The client-supplied coordinator and device hashes never
substitute for this check.

The pagination-complete scheduling snapshot is a canonical in-memory object
with these fields in exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_claim_snapshot.v1`. |
| `coordination_repository_id` | positive integer | Registry value. |
| `coordination_issue_number` | positive integer | Registry value. |
| `server_high_water_comment_id` | positive integer | Greatest observed comment ID. |
| `page_count` | positive integer | Exact number of API pages consumed. |
| `observation_sha256s` | nonempty `sha256` array | Every accepted event observation in server order. |
| `pagination_complete` | boolean | Must be true. |
| `snapshot_sha256` | `sha256` | Self-digest. |

The observation array is ordered by `server_created_at`, numeric
`server_comment_id`, and then event ID. It is an explicit exception to the
default array sort rule. An unparseable, unauthorized, edited, deleted,
duplicated, missing-page, or otherwise unobservable scheduling comment makes
the snapshot invalid; it is not omitted from the projection.

A release-binding object contains exactly these fields in this order:

`schema_version`, `worktree_observation_sha256`, `task_receipt_sha256`,
`result_packet_sha256`, `handoff_sha256`, `released_at_utc`, and
`release_binding_sha256`.

Its schema version is `trusted_owner_native_claim_release_binding.v1`.
The four evidence members are `sha256`, `released_at_utc` is a `utc_second`,
and the final member is the self-digest. The result must be `completed`; its
worktree observation, task receipt, task ID, result packet, and embedded
handoff must exactly cross-bind these values. The release time equals the
enclosing event's issuance time.

A failure-binding object contains exactly these fields in this order:

`schema_version`, `failure_phase`, `worktree_observation_sha256`,
`task_receipt_sha256`, `result_packet_sha256`, `handoff_sha256`,
`failure_evidence_sha256`, `failed_at_utc`, and `failure_binding_sha256`.

Its schema version is `trusted_owner_native_claim_failure_binding.v1`.
`failure_phase` is `before_worktree`, `before_task`, or `after_task`.
The four execution-evidence members are each `sha256` or null;
`failure_evidence_sha256` is a `sha256`; `failed_at_utc` is a `utc_second`;
and the final member is the self-digest. For `before_worktree`, all four
execution-evidence members are null. For `before_task`, only
`worktree_observation_sha256` is non-null. For `after_task`, all four are
non-null and the exact result is `blocked` or `finding`, never `unknown`.
The failure time equals the enclosing event's issuance time.

`terminal_binding` is null for `reserved`, `confirmed_running`, `lost`, and
`reconciliation_required`; it is exactly a release-binding object for
`released` and exactly a failure-binding object for `failed`. Unknown fields,
the wrong union member, or inconsistent nullability reject the event.

Transition events bind the exact predecessor observation digest and repeat the
same claim ID, request, wave, coordinator, device, lanes, resource keys, and
expiry. Only event ID, predecessor, state, issuance time, and the
state-selected terminal binding may change.

Allowed event transitions are:

- null predecessor -> `reserved`;
- `reserved` -> `confirmed_running`, `lost`, `failed`, or
  `reconciliation_required`;
- `confirmed_running` -> `released`, `failed`, or
  `reconciliation_required`; and
- no claim-event successor after `released`, `lost`, `failed`, or
  `reconciliation_required`.

`reconciliation_required` is terminal for automatic execution but has one
manual, non-retry successor form. A claim-resolution event contains these
fields in exact order:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_claim_resolution_event.v1`. |
| `event_id` | `id` | Globally unique and never reused. |
| `claim_id` | `id` | Exact affected claim. |
| `trigger_observation_sha256` | `sha256` or null | Exact `reconciliation_required` observation, or null only when ambiguity prevented one accepted trigger observation. |
| `trigger_snapshot_sha256` | `sha256` | Exact pagination-complete snapshot owning the uncertainty. |
| `resolution` | enum | `known_no_task_created`, `known_task_terminal_completed`, or `known_task_terminal_failed`. |
| `worktree_observation_sha256` | `sha256` or null | Exact observed worktree when one existed. |
| `task_receipt_sha256` | `sha256` or null | Exact task receipt when one task existed. |
| `result_packet_sha256` | `sha256` or null | Exact terminal result when one task existed. |
| `handoff_sha256` | `sha256` or null | Exact embedded terminal handoff when one task existed. |
| `cleanup_evidence_sha256` | `sha256` or null | Exact approved cleanup evidence when cleanup was required. |
| `review_ref` | `public_ref` | Fresh independent Codex E reconciliation review. |
| `review_receipt_sha256` | `sha256` | Exact accepted review receipt. |
| `issued_at_utc` | `utc_second` | Resolution issuance time. |
| `event_sha256` | `sha256` | Self-digest. |

For `known_no_task_created`, task, result, and handoff digests are null.
The worktree digest may be null; if it is non-null, cleanup evidence is
required and must prove only the exact attempt-owned worktree was reconciled.
For either `known_task_terminal_*` value, worktree, task, result, and handoff
digests are all non-null and cross-bind one exact terminal task; cleanup
evidence is null unless that accepted result explicitly required cleanup.
The completed variant requires `result=completed`; the failed variant requires
`result=blocked|finding`. An unknown task or result cannot produce a resolution
event.

The resolution event is observed with the common observation schema and is
effective only when its author is currently authorized, its review receipt is
accepted, its trigger snapshot is complete, and it is the sole valid resolution
for that claim. It releases scheduling capacity but never permits reuse,
retry, relaunch, or continuation of the resolved claim. A duplicate,
conflicting, unauthorized, or unreviewed resolution leaves the claim unknown
and active.

The trigger snapshot is the immediate pagination-complete prepublication
snapshot and therefore cannot contain the resolution event. After publication,
the coordinator obtains a fresh pagination-complete snapshot containing the
new observation and independently replays it. This removes any digest cycle.

The scheduling issue is dedicated to this protocol. Every top-level comment
must be either a claim event or a claim-resolution event. The complete
competing set is every comment, across all request IDs and all API pages,
observed through one canonical pagination-complete snapshot. Missing pages,
deleted previously observed comments, edited comments, unauthorized authors,
duplicate comment IDs, unparseable comments, GitHub inconsistency, or a forked
claim chain produces `unknown_outcome_reconciliation_required`.

Each reservation carries exactly these resource keys:

- `project:trusted_owner_native:v1`
- `wave_slot:<wave_ordinal>`
- one `repository:<repository_id>` per lane
- one `issue:<repository_id>:<issue_number>` per lane
- one `lane:<lane_id>` per lane

For each claim, project its latest valid state by following the one
predecessor-bound chain in GitHub server order. Two successors to the same
predecessor are a fork and fail closed. Active capacity includes:

- every unexpired `reserved` claim that wins the ordered replay;
- every `confirmed_running` claim until a valid terminal event, even after
  expiry; and
- every `reconciliation_required` or otherwise unknown claim until exactly one
  valid, independently reviewed claim-resolution event proves a known
  non-running or terminal disposition.

A valid claim-resolution event changes only the effective replay state to
`resolved_closed` and releases that claim's capacity. It does not rewrite the
claim chain or make any request, claim, task, worktree, issue, result, or
handoff identity reusable. If the required facts remain unknown, no resolution
event is constructible and the slot remains active.

An expired reservation with no confirmed-running or ambiguous successor loses
launch authority and is not active. Expiry never proves a launched task
stopped.

Order reservation observations by `server_created_at`, then numeric
`server_comment_id`, then ordinal `claim_id`. Replay them from oldest to newest.
A reservation wins only if:

1. its exact wave slot is not occupied by an earlier active winner;
2. none of its repository, issue, or lane keys intersects an earlier active
   winner;
3. accepting it keeps at most two active waves, three lanes per wave, and six
   active lanes across the complete project; and
4. its event and request retain at least 15 minutes before expiry.

The later conflicting reservation has effective state `lost`, whether or not
its coordinator later posts the corresponding event. It consumes no capacity
and launches nothing. This replay applies project-wide, not per request or per
machine. One repository has at most one active lane. A WIP or ADR-0008
exception may make a proposed lane eligible for planning, but it does not
weaken, rename, or bypass the exact `repository:<repository_id>` conflict key.

Initial contention acceptance requires two independent registered Windows
coordinators with distinct `coordinator_id_sha256` values and different
`request_id` values to race for at least one identical exclusive resource key.
The canonical server-ordered replay must select exactly one winner and the
loser must launch nothing. Distinct device pseudonyms may be used but never
substitute for trusted host observation or immutable GitHub authorship. Native
Mac task-capability or contention evidence is not required for Windows-profile
acceptance.

After posting its reservation, a coordinator must read a pagination-complete
snapshot, derive the same winner and capacity projection, and observe its own
winning reservation before task or worktree creation. It then posts and reads
back a `confirmed_running` event. A launched wave is immutable.

Only `reserved -> confirmed_running -> released` with one valid
release-binding object and matching authorized GitHub authorship is successful.
`reserved -> lost`, `reserved -> failed`, and any transition to
`reconciliation_required` are terminal for automatic execution. No lost,
failed, expired, reconciled, forked, or unknown claim is reused.

Version 1 creates at most one new wave per scheduling pass. An Automatic role
transition starts a fresh pass only after the predecessor wave is validly
released. All project-wide active waves and lanes count against the shared
ceiling.

## Repository-Approved Command Enforcement

The dispatcher accepts command IDs, never an ambient shell string.

For every command ID it must:

1. Resolve exactly one active registry command record.
2. Confirm role and operation equality.
3. Resolve the executable to the recorded identity without PATH fallback.
4. Expand only typed placeholders declared by `argument_template`.
5. Reject additional arguments, shell metacharacters, wildcards, redirection,
   command substitution, response files, implicit config, and unapproved
   environment variables.
6. Set the exact working directory and environment allowlist.
7. Enforce runtime, mutation, protected-surface, and external-effect ceilings.

Repository hooks, build scripts, executable fixtures, package install hooks,
and arbitrary repository code require an explicit approved-command record.
An entry with `forbidden` permits no repository-controlled executable. An
entry with `external_isolation_required` is never native-eligible.
When a native-eligible operation lacks that record, dispatch returns
`blocked_command_not_approved`. When the requested execution itself meets an
external-isolation trigger, it returns `blocked_external_isolation_required`.
It never improvises a command.

## Worktree Observation

The private absolute worktree path is never serialized. Read-only git and
filesystem inspection derives this public-safe object in exact field order:

`schema_version`, `repository_id`, `canonical_name`, `base_sha`,
`branch_ref`, `branch_head_sha`, `registered_top_level_sha256`,
`common_directory_sha256`, `remote_identity_sha256`,
`ordinary_nonreparse`, `observed_at_utc`, and
`worktree_observation_sha256`.

`schema_version` is `trusted_owner_native_worktree_observation.v1`.
Repository and digest fields use common scalar types. `branch_ref` is a
`git_ref`; `branch_head_sha` is a `git_sha`;
`ordinary_nonreparse` is boolean and must be true; `observed_at_utc` is a
`utc_second`; and the final member is the self-digest.

The three identity hashes use domain-separated UTF-8 preimages:
`registered_top_level` plus NUL plus the resolved top-level path,
`common_directory` plus NUL plus the resolved common directory, and
`remote_identity` plus NUL plus the canonical remote identity. Raw local paths
never leave bounded memory. The observation is valid only when registered
top-level, common directory, immutable repository ID, remote, branch, and head
all agree with the lane packet.

## Native Task Adapter Boundary

On a supported Windows host, the only native launcher identity is
`codex:native-task-create/v1`. It is a Core-owned adapter over the first-party
Codex task-creation surface. Its only admitted candidate production
realization is the dedicated App Server process boundary above. It is not
`codex exec`, a shell command, a caller-controlled process or subprocess
facility, a repository executable, an SDK, a service, or the external broker.
No weaker fallback is permitted. The adapter may create one task only after
the Windows/primitive preflight passes, a winning claim exists, and the
worktree is verified.

Its request contains these fields in this exact order:

`schema_version`, `request_sha256`, `claim_observation_sha256`,
`lane_packet_sha256`, `repository_id`, `issue_url`, `role`, `base_sha`,
`worktree_observation_sha256`, `context_mode`, `fork_turns`,
`issued_at_utc`, and `task_request_sha256`.

Types use the common scalar definitions. `schema_version` is
`trusted_owner_native_task_request.v1`; `context_mode` is
`isolated_packet_only`; `fork_turns` is `none`; and the last member is the
self-digest.

Its accepted receipt contains these fields in this exact order:

`schema_version`, `task_request_sha256`, `task_id`, `accepted_at_utc`,
`platform_receipt_ref`, `platform_receipt_sha256`, and
`task_receipt_sha256`.

`schema_version` is `trusted_owner_native_task_receipt.v1`. `task_id` is an
`id`; `accepted_at_utc` is a `utc_second`; `platform_receipt_ref` is a
`public_ref`; both digests are `sha256`; and the last member is the
self-digest. The platform receipt binds the first-party task API response; it
is not caller-supplied host-platform authority.

The adapter accepts no ambient conversation, raw issue text, command line,
environment override, credential, secret, sibling repository, or second task.
It passes only the exact lane packet. Missing or incompatible task capability
is rejected before claim publication through priority 1. After a valid
preflight and winning claim, malformed, rejected, timed-out, or ambiguous task
creation enters the ordered terminal selector and is never automatically
retried.

A request reaches `validated` in either state machine only after the
Windows/primitive preflight passes. Unsupported-host rejection therefore
cannot reach `claim_reserved`.

## Safe Mode State Machine

Safe mode executes exactly one requested same-role wave and stops.

| State | Allowed next state |
| --- | --- |
| `request_received` | `validated`, `rejected` |
| `validated` | `claim_reserved`, `rejected` |
| `claim_reserved` | `claim_won`, `claim_lost`, `reconciliation_required` |
| `claim_won` | `lanes_started`, `reconciliation_required` |
| `lanes_started` | `results_reconciled`, `reconciliation_required` |
| `results_reconciled` | `claim_released`, `reconciliation_required` |
| `claim_released` | `stopped` |
| `claim_lost` | `stopped` |
| `rejected` | `stopped` |
| `reconciliation_required` | `manual_fallback_required` |
| `manual_fallback_required` | `stopped` |
| `stopped` | none |

Eligible Safe waves are A, B, D, E, or F only. Safe mode never starts a second
role from a handoff.

## Automatic Mode State Machine

Automatic mode may create fresh A, B, E, and F tasks. It stops before every C,
D, or G task.

| Accepted current result | Deterministic route |
| --- | --- |
| A handoff requests B | Create a fresh B task if all new-task preflights pass. |
| A handoff requests any other role | Stop for manual routing. |
| B handoff requests E | Create a fresh E task if the artifact is reviewable. |
| B handoff requests C | Stop at `manual_implementation_required`. |
| B handoff requests A, B, D, F, or G | Stop for manual routing. |
| E accepts and explicitly recommends F | Create a fresh F task only when the F boundary below passes. |
| E opens a concrete D finding | Stop at `manual_fix_approval_required`. |
| E requests A, B, C, E, or G | Stop for manual routing. |
| Separately approved D finishes and recommends E | A later invocation may create a fresh E task, then an eligible F task. |
| F completes a draft PR action | Stop before G. |
| Any blocked, failed, ambiguous, or unknown result | Reconcile and stop. |

No role result is authority for a later mutation. Each role transition requires
a fresh task, fresh worktree, current issue authority, current WIP check,
current registry and skill digests, exact predecessor packet, and profile
preflight.

Codex C, Codex G integration, and Codex H are never launched by this profile.
Codex D requires a separate exact finding and owner or repository authority.

## Codex F Draft-PR-Only Boundary

An F lane is eligible only when all are exact and current:

- independent E verdict is accepted;
- E reviewed the exact head, files, scope, and evidence;
- bound validation passes;
- repository and WIP authority are refreshed;
- the base branch is explicitly authorized;
- publication authority names the exact repository, issue, head, and files;
- only reviewed files are staged; and
- secret, protected-surface, and repository-required checks pass.

F may stage reviewed files, commit, push the reviewed branch, and open or
update a draft PR. F must stop after readback.

F may not mark ready for review, merge, close an issue, update a tracker,
deploy, mutate credentials, perform G work, or claim integration readiness.

## Failure Vocabulary And Unknown Reconciliation

The dispatcher evaluates this table from priority 1 downward. The first true
trigger selects the one terminal outcome; no later row is evaluated. Every
trigger assumes all earlier rows are false.

| Priority | Terminal outcome | Exact trigger |
| --- | --- | --- |
| 1 | `blocked_request_or_packet_invalid` | Any request, lane, nested record, type, canonical byte, digest, timestamp, field, or current-user instruction is missing, malformed, stale, expired, duplicated, or contradictory; or trusted runtime host observation is not exactly Windows, is unavailable, or disagrees; or the exact Windows `codex:native-task-create/v1` primitive is missing or incompatible. |
| 2 | `blocked_no_wip_authority` | Any repository lacks current WIP-1 authority or an exact unexpired ADR-0008 exception for the proposed lane count. |
| 3 | `blocked_skill_source_drift` | Canonical source, managed installation, release binding, or source/install tree equality is missing, unsafe, or unequal. |
| 4 | `blocked_registry_missing_or_invalid` | Registry, authorized claim-actor set, entry review, scheduling surface, or command registry is absent, noncanonical, stale, or invalid. |
| 5 | `blocked_release_state_invalid` | Release-state chain is absent, forked, stale, invalid, or below the requested mode/capacity rung. |
| 6 | `blocked_repository_inactive` | Any exact entry status is not `active`. |
| 7 | `blocked_repository_identity_mismatch` | Immutable repository ID, canonical name, remote, issue repository, base ref, or observed repository does not match. |
| 8 | `blocked_role_or_operation_not_allowed` | Role or operation is not explicitly allowed by the active entry and current repository authority. |
| 9 | `blocked_command_not_approved` | A native-eligible operation names no exact command record, has an argument or environment mismatch, or exceeds its command record. |
| 10 | `blocked_external_isolation_required` | Every proposed lane requires the stronger profile under the escalation matrix. |
| 11 | `blocked_mixed_profile_wave` | At least one proposed lane is native-eligible and at least one requires external isolation. |
| 12 | `blocked_predecessor_packet_invalid` | A role requiring a predecessor lacks one exact current predecessor packet or carries extra context. |
| 13 | `blocked_cross_lane_overlap` | Proposed lanes have an unsafe dependency, write, protected-surface, evidence, issue, repository, or integration conflict not resolved by the accepted compatibility vocabulary. |
| 14 | `blocked_capacity_exceeded` | The complete project-wide replay is known and accepting the candidate would exceed two waves, three lanes per wave, six lanes total, or the current release rung. |
| 15 | `blocked_f_boundary` | An F request fails any exact draft-PR-only precondition. |
| 16 | `blocked_claim_lost` | The canonical server-ordered replay is known and the candidate reservation loses a wave slot or resource key. |
| 17 | `failed_claim_known` | Claim publication, immutable author validation, transition, or terminal binding is known to have failed with no ambiguous GitHub object and no launch. |
| 18 | `failed_lane_known` | Worktree, task creation, approved command, validation, result, handoff, or release is known to have failed after a winning claim. |
| 19 | `unknown_outcome_reconciliation_required` | Any required GitHub, task, worktree, command, result, handoff, F publication, release, or cleanup fact is unavailable, conflicting, forked, or commit-ambiguous. |
| 20 | `accepted_wave_complete` | Every requested lane completed, every result and handoff is valid, all required validation passed, all effects match authority, and the winning claim was validly released by an authorized author with an exact release binding. |

The outcome vocabulary is closed to these 20 values. A validator must prove
one and only one match for every representable selector input and prove every
row reachable. `manual_fallback_required` is a route, not a competing terminal
outcome. It follows outcomes 16 through 19 and any other outcome whose current
repository authority explicitly requires the old workflow.

Priority 1 is the deterministic unsupported-host outcome. It occurs before
claim publication or another persistent mutation and routes to A or B. It
never falls through to `blocked_external_isolation_required`,
`failed_claim_known`, `failed_lane_known`, or an unknown outcome. Retaining
this existing preclaim rejection outcome avoids a second platform-specific
status family without weakening observability or failure closure.

For an unknown task, claim, GitHub write, worktree, command, result, or F
publication outcome:

1. Stop new task and worktree creation for the affected request.
2. Preserve all observed objects.
3. Read GitHub claims, task identity, worktree identity, branch/head, and
   repository status through approved read-only interfaces.
4. Publish no replacement claim and perform no automatic retry.
5. Derive one canonical pagination-complete claim snapshot.
6. Classify the object as known no-task, known terminal complete, known
   terminal failed, or still unknown.
7. If and only if the state is known, obtain independent Codex E review and
   publish one authorized canonical claim-resolution event with exclusive
   append semantics, then read it back and replay capacity.
8. If still unknown, publish no resolution event, keep
   `unknown_outcome_reconciliation_required` active, and route to manual
   fallback.

Suspension or revocation during execution follows the same reconciliation
path. It blocks new work but does not assert that in-flight work stopped.

Manual fallback is the existing one-issue, one-role workflow. It preserves
known work, requires a human to select the next role, and creates no automatic
retry, duplicate task, or inferred authority.

## External-Isolation Escalation

The complete native wave must be rejected when any lane has:

- an unlisted, inactive, renamed without reconciliation, transferred, or
  identity-ambiguous repository;
- an unknown or untrusted contributor boundary;
- an entry whose `repository_code_execution_policy` is
  `external_isolation_required`;
- unreviewed repository code, executable content, hooks, packages, binaries,
  fixtures, or commands;
- a command outside the approved command set;
- a requested mutation, secret, credential, network, service, broker, canary,
  installation, package, deployment, or protected-surface operation outside
  exact repository authority;
- a need for independently proven filesystem, process, identity, credential,
  descendant-process, or network isolation; or
- a malicious-content or adversarial containment requirement.

The stronger profile wins. Version 1 does not mix native and isolated lanes in
one wave.

An unsupported non-Windows host or a missing or incompatible Windows native
task primitive is not an external-isolation trigger. It is the priority-1
preclaim rejection above. Mac failure cannot activate the broker or any other
launcher fallback.

Security issue ownership remains:

| Issue | External-isolation responsibility |
| --- | --- |
| #116 | Future ARS consumer and isolation adaptation. |
| #117 | Deferred nonblocking advisory; no trusted-profile prerequisite. |
| #118 | Broker/verifier package, installation, rollback, and lifecycle prerequisite. |
| #139 | MRP-RC-003 malicious-content observation pair. |
| #140 | Reboot, crash, second-host, credential, network, descendant, and lifecycle assurance. |
| #141 | Arbitrary-repository and unknown-contributor hardening. |

These issues are not prerequisites for the trusted-owner native profile. This
profile does not resolve, weaken, supersede, or claim evidence for them.

## Release-State Record And Graduated Ladder

The old manual workflow remains available at every rung. The canonical
repository-owned advancement chain is:

`docs/role_pool/trusted_owner_native_release_state.v1.jsonl`

The file is append-only canonical JSON Lines. Each line has one final LF.
Existing lines are immutable. Every line uses this exact schema:

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Exactly `trusted_owner_native_release_record.v1`. |
| `record_id` | `id` | Globally unique. |
| `predecessor_record_sha256` | `sha256` or null | Null only for bootstrap; otherwise exact immediately preceding line. |
| `from_rung` | rung enum or null | Null only for bootstrap; otherwise exact predecessor `to_rung`. |
| `to_rung` | rung enum | Exact next rung; skipping is forbidden. |
| `contract_sha256` | `sha256` | Accepted current contract. |
| `skill_tree_sha256` | `sha256` | Reviewed managed source and installed tree. |
| `registry_sha256` | `sha256` | Reviewed active registry. |
| `validator_bundle_sha256` | `sha256` | Exact validators used by both observations. |
| `observation_receipt_sha256s` | `sha256` array | Empty only for bootstrap; otherwise exactly two distinct receipts in chronological order. |
| `codex_e_review_ref` | `public_ref` | Fresh independent review of both observations and all current bindings. |
| `codex_e_review_sha256` | `sha256` | Exact review receipt. |
| `owner_decision_ref` | `public_ref` | Separate exact release decision. |
| `accepted_at_utc` | `utc_second` | Acceptance time. |
| `record_sha256` | `sha256` | Self-digest. |

The independently reviewed bootstrap line has null predecessor, null
`from_rung`, `to_rung=R0`, and an empty observation array. It still binds the
accepted contract, source/install tree, registry, validators, Codex E review,
and owner decision. Every later line has non-null predecessor and `from_rung`
and exactly two observation receipts.

There is exactly one valid successor per record. A fork, duplicate rung,
missing line, invalid digest, stale binding, or second successor blocks all new
native work. The current rung is the `to_rung` of the last valid line.

The ordered rungs and exact ceilings are:

| Rung | Exact ceiling |
| --- | --- |
| `R0` | Offline schema, parser, scheduler, state-machine, command, selector, fallback, no-retry, and source/install drift validation only. |
| `R1` | Inspect-only comparison with one manual issue/role workflow; no claim or task. |
| `R2` | Safe mode, one low-risk B or E lane, one fresh task, no F publication. |
| `R3` | Safe mode, one wave of up to three same-role lanes; include a separate claim-conflict observation from independent registered Windows coordinators and different request IDs that launches only the winner. |
| `R4` | Safe mode, one reviewed F draft-PR-only lane. |
| `R5` | Safe mode, up to two waves and six active lanes project-wide. |
| `R6` | Automatic mode, one issue path through only the permitted A, B, E, and F transitions. |
| `R7` | Automatic mode, one wave of up to three lanes. |
| `R8` | Automatic mode, up to two waves and six active lanes project-wide. |

Before each increase `R0 -> R1` through `R7 -> R8`:

1. Complete two consecutive accepted Windows-hosted observations at the
   current rung using
   distinct request, claim, task, worktree, issue, and result identities when
   that rung creates them.
2. Use the same reviewed contract, source/install tree, registry, and validator
   bundle for both observations.
3. Accept no unknown, retry, duplicate, cross-lane leak, command breach,
   authority breach, release failure, or unreconciled object.
4. Obtain fresh independent Codex E review of both receipts and current
   bindings.
5. Obtain the separate owner or repository release decision.
6. Append and independently read back one valid next-rung record.

A failed or unknown observation does not count and cannot be retried under the
same identity. It must be reconciled before a later fresh observation.

Platform-neutral offline validation may supplement a rung packet but cannot
replace a required Windows-hosted observation, Windows installation binding,
or Windows release decision. No accepted Windows rung or receipt automatically
qualifies native Mac dispatch.

Only a valid current `R8` record permits
`trusted_owner_native_profile_ready=true`. Every earlier rung keeps it false.

## Retained V5 Protection Map

The installed V5 behavior families have these complete successor dispositions:

| V5 family | Successor owner and disposition |
| --- | --- |
| Invocation parsing, explicit mode and role, exact canonical repository names, and bounded repository count | Native request and registry validators. Native version 1 removes shorthand rather than widening it. |
| Inspect, preclaim, and prelaunch barriers | Shared native phase controller: inspect is read-only; preclaim validates all packets, current state, compatibility, commands, and capacity before a claim; prelaunch requires a winning read-back claim and complete revalidation before task creation. |
| Current GitHub/git inventory and WIP-1 | Native repository preflight and ADR-0008 validator. |
| Exact repository read authority and non-transitive scope | Registry entry plus lane packet read-scope validator. |
| External text as untrusted evidence with no authority | Lane packet ingestion validator; raw text never changes role, scope, commands, or authority. |
| Stage-3 planning observations | Historical/shared offline validation only; no native launch or readiness authority. |
| Stage-4 malicious-content exception and `MRP-RC-003` | External-isolation profile and Security #139 only. |
| Candidate ranking, twice-deferred fairness, and ambient queue selection | Historical-only and not applicable: native version 1 accepts only explicitly requested lanes and has no ambient candidate queue. |
| Project-wide two-wave, three-lane-per-wave, six-lane limits | Complete GitHub claim replay and release-rung validator. |
| Pairwise compatibility, dependency cycles, overlapping writes, protected surfaces, and integration ordering | Native lane compatibility validator before claim. |
| Launcher executable probing and broker process ownership | External-isolation profile. Native uses only the separately reviewed Windows `codex:native-task-create/v1` binding and never claims broker equivalence. |
| Exact task, worktree, packet, isolated context, and one role per child | Native lane packet, task adapter, and worktree readback validators. |
| Claim ordering, expiry, reservation, winner recheck, and launched-wave immutability | Native claim event, GitHub observation, and project replay. |
| Wait, cancellation, unknown outcome, and no automatic retry | Native terminal selector and reconciliation state machine. |
| Typed per-lane result, role artifact, validation, finding, and handoff | Native result and handoff schemas. |
| F/G sidecar evidence and publication restrictions | Native F draft-only boundary; actual G remains a separate dedicated task. |
| Coordinator packet and lane-local evidence preservation | Native result index may reference but never replace each lane result and handoff. |
| Strict old-workflow prompt, injection, and consumer pickup sidecars | Shared fallback contract and fixtures retained byte-for-byte until a separate reviewed successor changes them. |
| Offline release gate and trusted-code regression guard | Shared validation. It remains non-isolation evidence and grants no launch authority. |
| External broker request, reservation, boundary-ready, start, terminal/abort, and lifecycle receipts | External-isolation references and Security #118/#140. |
| Global security, isolation, Stage 4, and live-readiness nonclaims | Profile boundary, terminal authority object, and release-state validator. |

No retained behavior is silently dropped. A historical-only disposition is
allowed only where the successor deliberately removes the underlying feature,
such as ambient lane selection, rather than removing its safety guard.

### Installed-Tree Migration Inventory

Observed installed root: the `mythic-edge-role-pool` destination resolved by
the existing Codex skill installer. Its machine-local absolute path is not
repository evidence and is not serialized here.

The public contract records relative paths and digests only. Inventory
classification codes are:

- `B`: baseline source to migrate and then change only under a reviewed native
  implementation contract;
- `S`: shared fallback or validation source to migrate byte-for-byte;
- `X`: external-isolation source to migrate byte-for-byte and keep separate;
- `G`: generated cache, never migrated or installed.

The 34 managed files total 1,756,994 bytes. Their 4,920-byte ordinal-path
manifest has SHA-256
`c512a703977375e8275eb17ca2281ffb0acb83084d328907020fe956cb37c64d`.

| Path | Bytes | SHA-256 | Class |
| --- | ---: | --- | --- |
| `SKILL.md` | 31177 | `130ce02b6f5eb8ec740642b67877bb0ecc33ab2ca8af17d16f76b2b3cee2756d` | B |
| `agents/openai.yaml` | 290 | `34bf1fb42a79f2765d88b3c46ec728e69975759ed4839577aba5e559e6ffe2f9` | B |
| `references/external-isolation-broker-v3-corrective-successor.md` | 41678 | `44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55` | X |
| `references/external-isolation-broker-v4-corrective-successor.md` | 29803 | `628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487` | X |
| `references/external-isolation-broker-v5-corrective-successor.md` | 232713 | `81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4` | X |
| `references/external-isolation-broker.md` | 77789 | `b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa` | X |
| `references/fallback-and-recovery.md` | 22306 | `0d01fb8eab143127662876251a5c55addd3c6c6f81c0f1ec0336f0404045379b` | S |
| `references/fallback-pickup-fixture/injection.json` | 1312 | `5322c32f5e252f9b74eec3264b34c4a0e04c32440d1b2a7f07ac0810cf672e3e` | S |
| `references/fallback-pickup-fixture/pickup.json` | 1567 | `1b11d1f74d379e8f6b75ea2ae921e1c4ac11685b5d5f11ada39c68e7df8d7a32` | S |
| `references/fallback-pickup-fixture/prompt.json` | 808 | `d3d0c5b84dfaa99745a8446b7fffa54783b5e6629cb5e5d9aa9a984aa1861f0f` | S |
| `references/pool-state-schema.md` | 28064 | `5f5018586179047e2ab4f45a18a651715039d5fcdef68fe626ac37210d1bdba2` | B |
| `references/release-remediation-matrix.md` | 12842 | `01239e0959e7ffc9b962df189745e1bcd5facd7e3e516c35165faa7fb3be8ccb` | X |
| `references/role-readiness-and-safety.md` | 14262 | `a2f34e0515e7105f66694bd8659fc2061cb7e19f33a3fad927be9fad7c9be5b9` | B |
| `references/stage3-behavioral-planning.md` | 120161 | `9b29d4546da706a8ceae8f106cb4e4acd7851587700089920898781005627c34` | X |
| `references/stage4-canary-exception.md` | 10346 | `87dd645372eedfb89008b7d3d84f9b6fd87e17c2e0228ed953a1508e3308800d` | X |
| `scripts/check_fallback_pickup.py` | 27302 | `c38191547694387f27af0614edf2566b80a1adc5b31f840bb81cd3dc6f9cf406` | S |
| `scripts/check_pool_plan.py` | 317537 | `fd4b9af88f57ae34cc6a79d77c2e8c9b119754b59a740403f275add55ad64f1d` | B |
| `scripts/check_stage3_behavioral_planning.py` | 51575 | `0c82bab47e45d87d66cd317027a2a7c63b11341bb734d75f5f780c7c7ac72b2e` | X |
| `scripts/check_stage4_canary_exception.py` | 18479 | `5fc41cee93396979d2689eea43b7a82fd869b64bbe8123b50b34c91fb51d01d9` | X |
| `scripts/codex_launcher_contract.py` | 137151 | `396f031a566736a71263bc303f8a4600f77590335ff43c1c74b633b4f4b00847` | X |
| `scripts/offline_gate_guard/offline_guard.py` | 7878 | `e508217276391b327119a16f8c21bbaa845c525868b4b3977bfd8f5e6d052fd9` | S |
| `scripts/offline_gate_guard/sitecustomize.py` | 160 | `ffa0a190b3617033825a9d284fb7e612cacef079fb551cdc950f8d3c401ca80c` | S |
| `scripts/pool_test_fixtures.py` | 67071 | `3a2a6cf0c712f773de03a4c4928ed68879811a76e95f188018f1d3ced7440dab` | B |
| `scripts/regenerate_fallback_pickup_fixture.py` | 4416 | `ac871a4dfcfb1a3cf517c6517af06699357b83d734e2084abd63300a3f0ae331` | S |
| `scripts/run_release_tests.py` | 6287 | `1ac0dd02df447a35e7e95e3b534d89a2c7e0b3e5901266b780b5ba13238f8a75` | S |
| `scripts/test_check_pool_plan.py` | 47200 | `d68633d5fcc7a14a249b1d33c3e3f606aabbff264b962de402a3c109be83f632` | B |
| `scripts/test_codex_launcher_contract.py` | 80894 | `564d0ac16c3cb3179cfb6775c5a490d1c9f12d07456b54c1934237e8ad0d5a6c` | X |
| `scripts/test_fallback_pickup.py` | 30424 | `9a7e244a3ee66fb1f02e335c3967bb3b836d8347202918a24695daf23510c4de` | S |
| `scripts/test_offline_gate_guard.py` | 3366 | `f5f1f964e4b8a107a88de3c24ba340e91a9c0a4d6541bafbdcd6bf6f46e4274c` | S |
| `scripts/test_pool_results.py` | 21855 | `2ac469bba49316ec7be3e61f477caddb8a88d2219579b264ae270e4eab5ad645` | B |
| `scripts/test_release_adversarial.py` | 80047 | `717f3f5f769bbd9c6eedba998da75a85192912b0085fa98847a59f2095a7779c` | X |
| `scripts/test_skill_contract.py` | 23586 | `0b94c9835a08ba365986b133b863f5aa6cb2b32f8662080dfdf678beff09e088` | B |
| `scripts/test_stage3_behavioral_planning.py` | 194490 | `f334ebbe67d5fff8f68797e0709770d00cb254215e710d59e9fb331daca7ab08` | X |
| `scripts/test_stage4_canary_exception.py` | 12158 | `84a3272f1ad2380206e7ef9dd4ceaa1ae71ed500b6be26a36cd3090b1bd06612` | X |

The 16 generated files total 1,216,455 bytes. Their 2,670-byte
ordinal-path manifest has SHA-256
`c222fb0199c15ca6d0bd8ff2d58fa12ce77c318beb28a6d2e1230d9c2d29f997`.
Every row is class `G` and must not appear in source or a dispatch-eligible
installation:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/__pycache__/check_fallback_pickup.cpython-313.pyc` | 31918 | `16e0b93af4618ce857eb3b1bca2283ea971548878b59162c76ade90e2f7242a8` |
| `scripts/__pycache__/check_pool_plan.cpython-313.pyc` | 316958 | `48d353b8cbed00934920a5be3d4f92d3b00e34ba769d21d9c60ba6ce8c49a4ae` |
| `scripts/__pycache__/check_stage3_behavioral_planning.cpython-313.pyc` | 51637 | `1fdf63ce25f44577f2a77d5478749f528948cebe7901e2bf8761ba39bdac77ce` |
| `scripts/__pycache__/check_stage4_canary_exception.cpython-313.pyc` | 21626 | `8658d1626052ff1617ff8443f455cc57058b07e6f17e9a95ebfc6c1efbb75c38` |
| `scripts/__pycache__/codex_launcher_contract.cpython-313.pyc` | 145838 | `89eef50604b04c1e236077d1b228410c7516b1e19bb956c7bfb8d557c89a822d` |
| `scripts/__pycache__/pool_test_fixtures.cpython-313.pyc` | 56124 | `b060cddf18fe959ecf59f84e0ce3b60bc5c7e5c85f455fc400e0a4ccbbb12ae9` |
| `scripts/__pycache__/test_check_pool_plan.cpython-313.pyc` | 67175 | `0e0ab249695cf9cc1b1cca56b183af023728b454cf720c00c7a64269d3eb0284` |
| `scripts/__pycache__/test_codex_launcher_contract.cpython-313.pyc` | 88893 | `21c770beb5f4c76cc86bfeb5b476ce8325187526bc5324b41f34083b05e70bab` |
| `scripts/__pycache__/test_fallback_pickup.cpython-313.pyc` | 37082 | `16393165b4bbcc46899cc32158a6fa4ddc95b294637643c6e0e6c30bdeafd9ec` |
| `scripts/__pycache__/test_offline_gate_guard.cpython-313.pyc` | 5725 | `71d18adea58ac53728fa00e960271b291f2e05eab199f816ca4fde160688ade9` |
| `scripts/__pycache__/test_pool_results.cpython-313.pyc` | 36686 | `e33781c13ac5accae70f913fe5f9d9abe712f9f2b7f50a38d7372878164b9d93` |
| `scripts/__pycache__/test_release_adversarial.cpython-313.pyc` | 89228 | `9a69d878c49b9652c419f60272d842463b029fd620c072a8a17cc15606572b07` |
| `scripts/__pycache__/test_skill_contract.cpython-313.pyc` | 30357 | `79d9e60f80e8b804feca20ad66dde50bd5d303aeb6b006aaa87ac2663078c29a` |
| `scripts/__pycache__/test_stage3_behavioral_planning.cpython-313.pyc` | 207797 | `bc9347020698aa200b6dd0badd6dd247f9287aa0007406e5bc9c0c8bce989099` |
| `scripts/__pycache__/test_stage4_canary_exception.cpython-313.pyc` | 18199 | `2a3bd618b2697b629dc5d31ec70147688ce12d90aa55153d77fb689da55eb980` |
| `scripts/offline_gate_guard/__pycache__/offline_guard.cpython-313.pyc` | 11212 | `46dcefaea737469ba95298b18f4cc730123558b9380c220f2d1c6e8a96e3224c` |

The all-observed 50-file inventory totals 2,973,449 bytes. It is lineage
evidence only because generated cache is present. It is not a candidate source
or a dispatch-eligible installed tree.

## Prospective Windows-First Implementation Delta Inventory

This amendment authorizes no implementation. After independent acceptance and
a separate owner decision, one later Codex C delta may need to change only
these existing implementation or test surfaces:

| Path | Prospective contract-owned delta |
| --- | --- |
| `docs/codex_skills/mythic-edge-role-pool/SKILL.md` | Replace the inert platform-neutral/Windows-and-Mac nonclaim with the accepted Windows-first host barrier, offline-validation exception, no-fallback rule, and future-Mac deferral. |
| `docs/codex_skills/mythic-edge-role-pool/references/pool-state-schema.md` | Document the preclaim Windows/primitive barrier and unchanged packet schemas. |
| `docs/codex_skills/mythic-edge-role-pool/references/role-readiness-and-safety.md` | Bind initial installation, live validation, canaries, and rung advancement to Windows without changing external-isolation claims. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_server_adapter.py` | Later companion-owned, private, dedicated inspect-only App Server process adapter; no generic launcher, command, or mutation API. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_server_adapter.py` | Later fake-transport lifecycle-registry, zero-command/zero-mutation, cardinality, receipt, timeout, no-retry, no-fallback, instruction-source, and resource-boundary tests. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` | Add trusted runtime host observation, exact Windows task-capability preflight, priority-1 projection, pre-side-effect enforcement, and the minimal call into the accepted dedicated adapter while preserving all existing public packet fields and terminal outcomes. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py` | Add host, primitive, no-fallback, remote-control classification, independent Windows contention, offline-only, selector-regression, and minimal App Server integration tests. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_skill_contract.py` | Replace platform-neutral compatibility assertions with Windows-first, native-Mac-deferred, and no-fallback documentation assertions. |
| `tools/install_codex_skills.py` | Keep `--check` read-only and platform-neutral; gate install and `--sync` mutation for this skill on trusted Windows observation before staging or destination mutation. |
| `tests/test_install_codex_skills.py` | Prove non-Windows install/sync rejection occurs before staging or destination mutation while read-only `--check` remains available. |

The App Server companion narrows its later implementation envelope to its two
new files and the two named `check_pool_plan.py` integration files. The other
rows remain the already accepted Windows-first implementation inventory and
are not automatically reopened by issue #758. In particular, the remaining
managed migration rows, external-isolation references, C/E artifacts,
production registry path, and release-state path remain untouched. If
implementation proves another path is indispensable, Codex C must stop and
route the exact mismatch to B rather than silently widening scope.

## Typed Validators And Deterministic Failures

Implementation must provide typed, offline-first validators for:

1. canonical source and installed-tree manifests;
2. the exact 50-row migration inventory and 34/16 managed/generated split;
3. registry root, authorized claim actors, entries, commands, argument
   records, status transitions, and self-digests;
4. invocation, lane, result, nested result, handoff, and authority packets;
5. claim events, release and failure bindings, post-publication observations,
   claim snapshots, resolution events, predecessor chains, and self-digests;
6. project-wide claim replay and reviewed reconciliation closure across all
   pages and request IDs;
7. immutable repository identity and canonical-name reconciliation;
8. approved-command lookup and typed argument expansion;
9. native task adapter requests and receipts plus trusted Windows host and
   exact primitive preflight;
10. claim ordering, state transitions, expiry, capacity, and independent
    registered Windows coordinator contention;
11. worktree, issue, task, role, and predecessor isolation;
12. Safe and automatic transition tables;
13. ordered terminal outcome selection, including priority-1 unsupported-host
    projection;
14. F draft-PR-only eligibility;
15. escalation, mixed-profile rejection, and prohibition on platform-triggered
    broker fallback;
16. unknown-state reconciliation and manual fallback;
17. release-record chaining, rung ceilings, and two-observation advancement;
    and
18. Windows-only installation mutation with platform-neutral read-only
    source/install checking.

All validators reject duplicate keys, unknown fields, wrong scalar types,
unrecognized enums, stale or expired authority, missing digests, ambiguous
identity, wildcard scope, unauthorized widening, and inconsistent cross-field
bindings. Failure is deterministic and maps to exactly one contract status.

Required focused tests include:

- one-, two-, and three-lane requests and rejection of zero or four lanes;
- exact repository identity, rename, transfer, inactive status, and duplicate
  entry behavior;
- exact-role and operation authorization;
- arbitrary command, PATH fallback, shell expansion, hook, package, and
  environment rejection;
- construction of an immutable claim event before publication and a separate
  observation after GitHub assigns server metadata;
- rejection of a claim event containing a server-assigned field;
- rejection of an event authored by an actor absent from the active registry
  and acceptance of the same body only from the exact admitted immutable actor
  ID;
- release rejection unless task, worktree, result, and handoff evidence
  cross-bind one exact release-binding object;
- independent registered Windows coordinator contention with deterministic
  one-winner ordering across different request IDs;
- trusted observation acceptance only when `os.name == "nt"` and
  `sys.platform == "win32"`;
- classification of a Mac remotely controlling the Windows Desktop as
  Windows-hosted because the observed execution process is on Windows;
- deterministic non-Windows rejection before claim, worktree, task, command,
  installer staging, or another persistent mutation;
- missing or incompatible `codex:native-task-create/v1` rejection before claim;
- proof that unsupported-host or primitive failure cannot activate the broker,
  `codex exec`, shell, `subprocess`, repository execution, weaker receipts, or
  silent fallback;
- platform-neutral offline validation acceptance only for pure read-only or
  in-memory operations, with no promotion authority;
- pagination-complete competing sets, chain forks, duplicate comment IDs,
  claim loss, expiry, GitHub timeout, unknown write, and no-retry behavior;
- explicit `reconciliation_required`, unknown-state retention, reviewed
  known-no-task closure, reviewed known-terminal closure, duplicate-resolution
  rejection, and capacity release only after valid resolution readback;
- project-wide two-wave, three-lane-per-wave, and six-lane ceilings;
- repository and issue resource conflicts across requests;
- fresh issue, task, worktree, role, and predecessor binding;
- native adapter field, digest, one-task, and no-fallback behavior;
- App Server baseline acceptance only for B/E inspect-only lanes with empty
  command, validation-command, mutation, and artifact arrays, disabled
  effectful tools, and zero command or file-change observations;
- cross-lane path, transcript, and packet leak rejection;
- every Safe and automatic state and forbidden transition;
- C, D, G, H stop behavior;
- F accepted and rejected boundary cases;
- every external-isolation trigger;
- every terminal status and manual fallback;
- a terminal-selector audit with overlap, uncovered, and unreachable counts all
  zero;
- bootstrap, linear advancement, fork rejection, rung skip rejection, stale
  binding rejection, and exactly two observations per increase;
- prevention of a three-lane or F canary before its preceding rung; and
- Windows-hosted evidence for every installation mutation, live validation,
  canary, and rung advancement, with native Mac evidence nonblocking and
  non-inherited; and
- exact inventory counts, byte counts, manifest digest, and rejection of every
  generated cache path.

Validation success is evidence only. It grants no dispatch, installation,
publication, canary, merge, deployment, or readiness authority.

## Acceptance Criteria

Independent Codex E must confirm:

- the source-of-truth decision is exact and does not treat installed bytes as
  authority;
- the registry is separate, closed, identity-bound, and not populated;
- every invocation names one to three exact active repositories;
- command enforcement cannot fall back to arbitrary repository execution;
- the initial App Server realization accepts only the exact inspect-only B/E
  subset, mechanically exposes no command tool, grants no file change, and
  cannot represent a nonempty command, validation, mutation, or artifact
  request;
- the trusted runtime, not caller input, owns host-platform identity;
- initial installation, live validation, canaries, and all rung advancement are
  Windows-hosted, while a Mac remotely controlling Windows is correctly
  classified by the Windows execution host;
- native Mac dispatch and Mac task-capability evidence are deferred and do not
  block the Windows profile;
- a non-Windows host or missing/incompatible Windows task primitive selects
  `blocked_request_or_packet_invalid` before every claim or persistent effect
  and cannot activate any weaker launcher or receipt;
- platform-neutral offline validation remains evidence-only and cannot advance
  the Windows profile;
- immutable claim events are constructible before publication and server
  metadata is bound only through deterministic readback;
- GitHub claims deterministically coordinate independent registered Windows
  coordinators across the complete project, not merely one request;
- lane isolation and predecessor-packet rules are closed;
- immutable GitHub comment authorship, not a client pseudonym, determines
  scheduling-event authority;
- both transition state machines have no overlap, uncovered state, or
  unauthorized role transition;
- the ordered terminal selector has no overlap, uncovered state, or unreachable
  row;
- unknown outcomes cannot retry automatically;
- a reviewed canonical resolution event can release a reconciled slot without
  reviving or reusing any historical identity;
- F cannot exceed draft-PR-only publication;
- native and external-isolation responsibilities do not overlap or weaken one
  another;
- the capacity ladder requires two accepted observations and fresh E review
  plus one canonical release-state record before each increase;
- all 50 observed installed files have an exact migration disposition and all
  retained V5 protection families have one named owner;
- deterministic validators and manual fallback cover every terminal state; and
- `trusted_owner_native_profile_ready` is the only positive profile claim and
  remains false.

## Remaining Unknowns

These are owner or implementation inputs, not permission for Codex B to fill
them:

1. The initial repository entries, their reviewed command sets, and the
   immutable GitHub user IDs admitted to author scheduling events.
2. The immutable GitHub repository identity and issue number of the dedicated
   scheduling surface.
3. Windows capability evidence showing that the exact
   `codex:native-task-create/v1` adapter satisfies every contracted guarantee
   without a weaker fallback.
4. The separate owner decision naming the Windows installation targets and
   authorizing first installation or later synchronization.
5. Whether the accepted cross-repository policy should also be promoted to a
   new ADR after contract review.

Items 1 through 4 block installation, dispatch, or canary activation, but do
not leave an implementation choice in the contract. The 50-file migration
inventory and native adapter interface are closed above. Codex E may accept
the contract while keeping all operational authority false.

Native Mac capability is not an unresolved input for the Windows profile. It
is deferred to a separate future issue and acceptance path.

## Protected Boundaries And Non-Claims

This contract does not authorize:

- creating the canonical skill source or registry;
- editing or installing the Role Pool skill;
- populating or activating an allowlist entry;
- creating the scheduling issue or claims;
- dispatching tasks or creating worktrees;
- acquiring, installing, starting, or characterizing the pinned Codex App
  Server candidate;
- creating a process, thread, turn, interrupt, App Server receipt, installation
  receipt, generated-schema copy, or runtime credential binding;
- native Mac dispatch or treating Mac evidence as inherited from Windows;
- running native or external-isolation canaries;
- acquiring, installing, or operating broker/verifier packages;
- accessing secrets, private evidence, candidate packages, or denied content;
- changing parser, workbook, webhook, analytics, AI, deployment, or production
  truth;
- committing, pushing, opening a PR, merging, closing issues, updating
  trackers, or deploying;
- Stage 4 execution or advancement;
- global live readiness or security assurance; or
- `trusted_owner_native_profile_ready=true`.

Files owned by this Codex B task:

- `docs/contracts/trusted_owner_native_role_pool_profile.md`
- `docs/contracts/role_pool_codex_app_server_native_task_adapter.md`

Side effects are limited to those two worktree files.

## Historical Windows-First Review Handoff

The prompt and handoff below record the predecessor Windows-first amendment
cycle. They are immutable lineage, not the current issue #758 route, and must
not be executed again. The sole current review handoff is the one in
`docs/contracts/role_pool_codex_app_server_native_task_adapter.md`, which
requires one independent Codex E review of both final contract artifacts.

Historical next role: Codex E, independent Windows-first contract amendment
reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Windows-First Trusted-Owner Native Role Pool
Contract Amendment Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/744
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

Review only:
docs/contracts/trusted_owner_native_role_pool_profile.md

Reviewed predecessor SHA-256:
eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc

Owner platform directive:
https://github.com/Tahjali11/Mythic-Edge/issues/744#issuecomment-5111260293

Completed Codex C handoff:
docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md
SHA-256:
c0bcbb87bdd21b897293fd6dfcd3ab0cc52445bd4edf1f73ddac69ae9dacf649

Terminal Codex E implementation report:
docs/contract_test_reports/trusted_owner_native_role_pool_profile.md
SHA-256:
7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8

Accepted implementation manifest SHA-256:
f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7

Use the exact amended artifact SHA-256 from the Codex B handoff. Confirm the C
handoff and terminal E implementation report remain byte-identical and that no
implementation review remains active or unresolved. Verify current repository
authority, WIP authority, issue lineage, owner directive, branch, and exact
predecessor before reviewing the amendment.

Independently test contract closure for:
- Windows as the only initial dispatch host for installation mutation, live
  validation, canaries, and R0-R8 advancement;
- Mac remote control of a Windows process classified as Windows-hosted, while
  native macOS dispatch is deferred and nonblocking;
- trusted runtime observation from `os.name` and `sys.platform`, with no
  caller-controlled platform field;
- exact `codex:native-task-create/v1` capability on Windows and no weaker
  fallback;
- priority-1 `blocked_request_or_packet_invalid` selection before claim,
  worktree, task, command, installer staging, release advancement, or any
  persistent mutation on unsupported or unobservable hosts or when the exact
  primitive is missing or incompatible;
- no broker, `codex exec`, shell, `subprocess`, repository executable, weaker
  receipt, or silent fallback from platform failure;
- platform-neutral offline validation only when it creates no claim, task,
  worktree, command execution, or persistent external mutation;
- deterministic project-wide one-winner contention between independent
  registered Windows coordinators and different request IDs;
- unchanged GitHub scheduling, capacity, lane isolation, no-retry,
  reconciliation, receipt bindings, Safe/Automatic transitions, F boundary,
  and R0-R8 ceilings;
- unchanged 34-path migration inventory, schemas, field counts, digest
  preimages, 20-outcome vocabulary, release chain, external-isolation
  separation, and MRP-RC-003 nonclaims;
- future native Mac support requiring a separate issue, accepted contract,
  independent E review, owner activation, and graduated evidence without
  inheriting Windows evidence; and
- exact prospective implementation/test delta inventory with no implementation
  edits in this task.

Treat ADR-0010 and ADR-0011 as non-precedential while Proposed. Confirm the
Security #116, #117, #118, #139, #140, and #141 separation. Lead with
findings. Run contract, repository, structural, protected-surface,
private-marker, process, and residue validation. Confirm the C/E artifacts and
34-path source tree are untouched. Do not implement, edit tests or handoffs,
populate the registry, install or edit the skill, dispatch, run canaries,
create packages, mutate Windows, submit, merge, deploy, advance any rung or
Stage 4, or claim readiness.

Return the exact reviewed SHA-256, finding verdict, acceptance status,
Windows-host rule, unsupported-host outcome, schema/vocabulary preservation,
prospective C delta inventory, remaining unknowns, validation evidence,
authority flags, and a workflow_handoff. Route ambiguity to Codex B. An
accepted amendment grants no implementation or activation authority.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
  global_router_read: false
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0004"
    - "ADR-0005"
    - "ADR-0006"
    - "ADR-0008"
  nonprecedential_design_evidence_read:
    - "ADR-0010 Proposed"
    - "ADR-0011 Proposed"
  protected_surfaces:
    - "workflow enforcement"
    - "native task launch authority"
    - "Windows-first dispatch-host restriction"
    - "independent registered-coordinator scheduling claims"
    - "Codex F publication boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "Open PRs #374 and #391 consume WIP-1; the current owner instruction supplies the exact bounded explicit_user_override recorded in this contract."
  stop_conditions:
    - "source-decision or repository-authority drift"
    - "loss of the current explicit owner override"
    - "duplicate active contract scope"
    - "request to implement or activate this profile"
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Windows-First Trusted-Owner Native Role Pool Contract Amendment Writer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/744"
  current_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  predecessor_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  source_decision: "https://github.com/Tahjali11/Mythic-Edge/issues/744#issuecomment-5109379065"
  windows_first_directive: "https://github.com/Tahjali11/Mythic-Edge/issues/744#issuecomment-5111260293"
  source_artifact: "docs/contracts/trusted_owner_native_role_pool_profile.md"
  contract_status: "review_pending"
  predecessor_contract_sha256: "eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc"
  accepted_implementation_handoff_sha256: "c0bcbb87bdd21b897293fd6dfcd3ab0cc52445bd4edf1f73ddac69ae9dacf649"
  terminal_implementation_review_sha256: "7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8"
  accepted_implementation_manifest_sha256: "f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7"
  initial_dispatch_host: "windows"
  remote_mac_controlling_windows: "windows_hosted_execution"
  native_mac_dispatch: "deferred_nonblocking"
  unsupported_host_outcome: "blocked_request_or_packet_invalid_before_side_effects"
  terminal_outcome_count: 20
  schema_or_digest_family_added: false
  scheduling_capacity_ladder_changed: false
  c_e_artifacts_touched: false
  managed_source_tree_touched: false
  generated_residue_count: 0
  contract_accepted: false
  owner_implementation_decision_eligible: false
  trusted_owner_native_profile_ready: false
  implementation_authorized: false
  test_modification_authorized: false
  installation_authorized: false
  registry_population_authorized: false
  claim_creation_authorized: false
  task_or_worktree_creation_authorized: false
  dispatch_authorized: false
  canary_authorized: false
  package_operations_authorized: false
  stage4_authorized: false
  rung_advancement_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: independent Windows-first contract amendment reviewer"
```
