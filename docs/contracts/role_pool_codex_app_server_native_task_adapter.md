# Role Pool Codex App Server Native-Task Adapter Contract

Status: `contract_revision_pending_review`

Risk tier: `high`

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/758

Parent capability issue:
https://github.com/Tahjali11/Mythic-Edge/issues/757

Phase 8 tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

## Findings And Decision

1. The accepted #757 result remains
   `accepted_exact_metadata_only_insufficient_evidence`. It established none
   of the nine production capability facts and performed no task, process,
   installation, dispatch, canary, or rung operation.
2. OpenAI's pinned Codex `0.146.0` source and release expose a first-party App
   Server protocol with `initialize`, `initialized`, `thread/start`,
   `turn/start`, `turn/interrupt`, and `turn/completed`. This is a
   mechanically contractible candidate surface. It is not current Role Pool
   production evidence.
3. The public `trusted_owner_native_task_request.v1` is sufficient without
   versioning. Its self-digest reaches the complete request, lane packet,
   worktree observation, registry, release state, skill tree, role,
   predecessor, command, scope, and stop-condition bindings. Values specific
   to App Server are either fixed by this contract or derived from those
   already-bound objects.
4. The existing `trusted_owner_native_task_receipt.v1` is also sufficient.
   Its `platform_receipt_ref` and `platform_receipt_sha256` can bind the
   closed public-safe lifecycle receipt defined here. No weaker receipt or
   inferred task success is admitted.
5. The selected GitHub release tag is an unsigned annotated tag. The exact
   commit, asset size, asset SHA-256, source-tag schema bytes, independent
   installation review, and prelaunch readback are the accepted provenance
   chain. This contract makes no publisher-signature claim.
6. `ME-RP-758-E-001` identified that the reviewed v2-only aggregate omitted
   wire types used by this contract. The same pinned tag contains one complete
   aggregate, `codex_app_server_protocol.schemas.json`, that includes the v1
   initialize response, v2 requests and notifications, server/client request
   unions, and JSON-RPC envelopes. This revision binds that one complete
   artifact.
7. `ME-RP-758-E-002` proved that the pinned command-approval request is not a
   universal pre-effect command gate. This revision therefore does not claim
   command or mutation support. The baseline is mechanically restricted to an
   inspect-only B or E lane with empty command, validation-command, mutation,
   and artifact arrays. Shell and other effectful tools are disabled, every
   file-change approval is denied, and any command or mutation observation is
   a terminal policy breach.
8. `ME-RP-758-E-003` identified an unreproducible prose-normalized lifecycle
   domain. This revision replaces it with one canonical 39-tuple
   raw-to-normalized registry, one exact first-applicable selector, bound
   per-outcome counts, and a fixed oracle digest.

Decision:

`feasible_with_narrow_profile_amendment`

The concrete candidate identity is
`codex:app-server-stdio-direct/v1`, implementing the existing public
`codex:native-task-create/v1` boundary. It is not a fallback or second public
task capability.

## Authority And WIP Reconciliation

Core `origin/main` and this worktree were refreshed at
`26ca98ce81c0f393bf1ec9df470c10ae911c01f7`. PR #374 remains an open draft
and PR #391 remains open. The owner's current invocation is the narrow
ADR-0008 exception for this contract only:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #758 Windows App Server baseline contract"
  blocked_active_issue_or_pr:
    - "PR #374"
    - "PR #391"
  reason: "The owner explicitly activated one docs-only profile amendment and companion App Server lifecycle contract after #757 integration."
  allowed_scope:
    - "read current public repository, GitHub, release metadata, and pinned source schema"
    - "revise docs/contracts/trusted_owner_native_role_pool_profile.md"
    - "create docs/contracts/role_pool_codex_app_server_native_task_adapter.md"
    - "run local read-only contract validation"
    - "produce one independent Codex E handoff"
  expiration_condition: "The two contracts and Codex E handoff are complete, or the owner revokes or redirects this lane."
  authorized_by: "Tahjali11 current user instruction"
  recorded_in: "this contract and the amended profile"
```

The exception does not transfer to Codex E, Codex C, package acquisition,
installation, process start, R0, R2, or any later role.

## Current Exact Bindings

| Binding | Exact value |
| --- | --- |
| Core base | `origin/main@26ca98ce81c0f393bf1ec9df470c10ae911c01f7` |
| Source issue | `https://github.com/Tahjali11/Mythic-Edge/issues/758` |
| Parent capability contract | `docs/contracts/role_pool_windows_native_task_capability_evidence.md`, SHA-256 `d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef` |
| Parent contract review | `docs/contract_test_reports/role_pool_windows_native_task_capability_evidence_contract_review.md`, SHA-256 `36d6eff2fa8e797d1b53cc60190606ec02c3dc8e1985d9d2def4c51a9bb3075c` |
| Parent metadata evidence | `docs/contract_test_reports/role_pool_windows_native_task_capability_evidence.md`, SHA-256 `f63f28080981701a1dc45ddd6b1dc620cb0702f27aae351063a0566164c17729` |
| Capability verdict | `insufficient_evidence` |
| Profile predecessor | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322` |
| Amended profile governed by this companion | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `4a0ba9efe5c987735c09df66f94f42924a92a40ca68fd15a84ffb2c41842c94d` |
| Canonical Role Pool source | `docs/codex_skills/mythic-edge-role-pool/`, 34 files, reviewed manifest SHA-256 `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175` |
| Registry destination | `docs/role_pool/trusted_owner_repository_registry.v1.json`, currently absent |
| Release-state destination | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, currently absent |

Every later role must recompute these public bindings. Drift does not authorize
an in-place reinterpretation.

## Module And Truth Ownership

Module: Core-owned trusted-native App Server adapter and process lifecycle.

Internal project area: `Quality / Governance`.

Truth owners:

- the accepted profile owns public task requests, task receipts, scheduling,
  command policy, terminal outcomes, and the R0-R8 ladder;
- this companion owns only the concrete App Server execution mapping,
  process/transport limits, private installation binding, public-safe platform
  receipt, and candidate lifecycle;
- the pinned first-party release and generated source schema own the available
  wire shapes;
- the active registry and lane packet own repository, command, path, mutation,
  role, and predecessor authority; and
- a later independent Codex E characterization owns whether the real pinned
  runtime actually satisfies these requirements.

The adapter is bridge code. It owns no repository truth, issue authority,
parser truth, credential truth, release promotion, or readiness claim.

## Public Capability And Schema Preservation

The profile-facing capability name remains
`codex:native-task-create/v1`. The App Server adapter is private behind that
name. The following public schemas remain byte-for-byte and semantically
unchanged:

- `trusted_owner_native_task_request.v1`;
- `trusted_owner_native_task_receipt.v1`;
- `trusted_owner_native_request.v1`;
- every lane, claim, worktree, result, handoff, registry, and release-state
  schema; and
- the closed 20-outcome profile vocabulary.

The existing task request is sufficient because the adapter must validate and
dereference this complete chain before launch:

| App Server binding | Existing source |
| --- | --- |
| request, claim, lane, repository, issue, role, base, worktree, isolated context, no fork, issuance | `trusted_owner_native_task_request.v1` |
| operation, predecessor, commands, read/mutation scope, protected surfaces, validation, artifacts, stops | exact lane packet |
| skill tree, registry, release state | parent request |
| zero-command, zero-validation, zero-mutation, inspect-only restriction | active registry entry and exact lane packet |
| profile, validator bundle, current rung | release-state record |
| App Server executable, schema, fixed protocol, request policy, and resource bounds | this accepted companion |

No caller-supplied App Server field is added. Unknown fields in the v1 task
request remain invalid.

The companion introduces private or platform-receipt schemas only. They do not
grant authority and do not alter the public request.

## Pinned Release And Generated Schema

The exact candidate is:

| Property | Required value |
| --- | --- |
| release | `Codex 0.146.0` |
| tag ref | `refs/tags/rust-v0.146.0` |
| annotated tag object | `be449751a978f02e5bbba886999662956c7f38f5` |
| tag commit | `e363b08c9175ac1cbe5893615dd2cb9ddf95043b` |
| tag signature status | `unsigned` |
| release state | published, not draft, not prerelease |
| Windows asset | `codex-x86_64-pc-windows-msvc.exe` |
| asset byte count | `358650672` |
| asset SHA-256 | `bc343ba420dc2e2e9f59e6fc5e5bf0aae1cd8c771fc319665241fc9c0271fddb` |
| command arguments | `app-server`, `--listen`, `stdio://` |
| process topology | one root App Server process per lane |

The separately published
`codex-app-server-x86_64-pc-windows-msvc.exe` asset is an alternate executable
and is explicitly rejected. PATH discovery, another version, a renamed copy
without the exact file identity, an SDK-managed process, and a pre-existing
process are rejected.

The exact complete generated protocol schema is the source-tag artifact:

`codex-rs/app-server-protocol/schema/json/codex_app_server_protocol.schemas.json`

Its tag-commit Git blob SHA-1 is
`f89d3eac44c55b9360a3e03bf9f8f230ac9a976b`, byte count is `590325`, and
SHA-256 is
`08cc0c836bf0caca1e65b92956c3d57fd59c6be9b66277f77afe1cf65aefa592`.
The SHA-1 is source location metadata; SHA-256 and byte count are the accepted
content binding.

This aggregate must contain the exact tagged definitions for
`InitializeResponse`, `CommandExecutionRequestApprovalParams`,
`FileChangeRequestApprovalParams`, `ServerRequest`, `ClientRequest`,
`ServerNotification`, `JSONRPCRequest`, and `JSONRPCResponse`, plus every
request, response, and notification named in this contract. An implementation
must validate wire objects against their exact versioned definitions inside
this aggregate; presence of a name alone is insufficient.

No schema is generated in this contract lane. A later authorized installer may
copy these exact source-tag bytes or run the pinned CLI schema generator, but
the installed aggregate must equal this byte count and SHA-256. A generator
result that differs is blocked; it does not replace the pin.

## Installation Custody

Core owns the future private installation. The root is resolved only from the
Windows `LocalApplicationData` known-folder API, followed by these literal
segments:

`MythicEdge`, `RolePool`, `CodexAppServer`, `0.146.0`

The absolute path never enters a repository artifact, request, receipt,
diagnostic, or handoff. Environment variables, PATH, caller paths, search,
wildcards, alternate roots, symlinks, junctions, mount points, and short-name
substitutions are forbidden.

The root may contain only these fixed basenames:

1. `codex-x86_64-pc-windows-msvc.exe`
2. `codex_app_server_protocol.schemas.json`
3. `installation-receipt.v1.json`
4. `runtime-config-manifest.v1.json`
5. `runtime-home`

Package acquisition, root creation, credential provisioning, and installation
require a separate issue or owner decision and independent Codex E review.
The adapter is read-only against this root.

Every component must be a fixed-local-NTFS ordinary non-reparse object. The
adapter opens the executable and schema without share-write or share-delete,
validates byte count, SHA-256, stable file identity, and ordinary-file state,
and holds both handles through process creation and schema loading. Identity or
content drift before process start selects the profile's
`blocked_skill_source_drift` outcome.

The private installation receipt has these fields in this exact order:

`schema_version`, `release_version`, `tag_ref`, `tag_object_sha`,
`tag_commit_sha`, `tag_signature_status`, `asset_name`, `asset_byte_count`,
`asset_sha256`, `protocol_schema_source_path`,
`protocol_schema_git_blob_sha1`, `protocol_schema_byte_count`,
`protocol_schema_sha256`, `install_root_identity_sha256`,
`executable_file_identity_sha256`, `schema_file_identity_sha256`,
`runtime_config_manifest_sha256`, `installed_at_utc`,
`installer_contract_sha256`, `codex_e_review_ref`,
`installation_receipt_sha256`.

`schema_version` is
`trusted_owner_codex_app_server_installation_receipt.v1`. SHA fields are
lowercase 64-hex except `tag_object_sha`, `tag_commit_sha`, and
`protocol_schema_git_blob_sha1`, which are lowercase 40-hex Git object IDs.
`asset_byte_count` and `protocol_schema_byte_count` are positive integers.
Timestamps are whole-second UTC. The final member is the self-digest. No path,
ACL, credential, environment value, account, or private identity is serialized.

`runtime-home` is an ordinary non-reparse directory used as the process's
exact `CODEX_HOME`. It contains only:

- the exact 780-byte `config.toml` below;
- one private ordinary `auth.json` provisioned by the existing Codex
  credential owner under separate authority; and
- `skills/mythic-edge-role-pool/`, byte-identical to the accepted managed
  source tree.

The config is UTF-8 without BOM, uses LF line endings, has exactly one final
LF, and has SHA-256
`fae8d0a1992225d30d2275c247629b31f39b3b9ee4578963fb121e1093510412`:

```toml
[features]
apps = false
artifact = false
auth_elicitation = false
browser_use = false
browser_use_external = false
browser_use_full_cdp_access = false
code_mode = false
code_mode_host = false
code_mode_only = false
computer_use = false
default_mode_request_user_input = false
enable_mcp_apps = false
goals = false
hooks = false
image_generation = false
in_app_browser = false
multi_agent = false
multi_agent_v2 = false
plugin_sharing = false
plugins = false
remote_plugin = false
request_permissions_tool = false
shell_tool = false
skill_mcp_dependency_install = false
skill_search = false
standalone_web_search = false
tool_call_mcp_elicitation = false
tool_suggest = false
unified_exec = false
web_search_cached = false
web_search_request = false
workspace_dependencies = false
```

No global user config, exec-policy rule, plugin, hook, MCP server, marketplace,
remote-control setting, or other skill is copied or linked into this home.
Credential bytes, content digests, tokens, and account values never enter a
manifest or receipt. The adapter does not parse `auth.json`; it validates only
the separately reviewed private custody state and lets the pinned App Server
consume it.

The runtime config manifest has these fields in order:

`schema_version`, `config_toml_byte_count`, `config_toml_sha256`,
`role_pool_skill_tree_sha256`, `environment_name_allowlist`,
`codex_home_identity_sha256`, `credential_mode`,
`credential_material_in_manifest`, `remote_control_enabled`, `plugin_count`,
`hook_count`, `mcp_server_count`, `runtime_config_manifest_sha256`.

`schema_version` is
`trusted_owner_app_server_runtime_config_manifest.v1`.
`config_toml_byte_count` is `780`; `config_toml_sha256` is
`fae8d0a1992225d30d2275c247629b31f39b3b9ee4578963fb121e1093510412`;
`credential_mode` is
`private_existing_codex_login`; `credential_material_in_manifest` and
`remote_control_enabled` are false; and the three counts are zero. The final
member is the self-digest.

The environment-name allowlist is exactly this ordinally sorted array:

`["CODEX_HOME","COMSPEC","LOCALAPPDATA","SYSTEMDRIVE","SYSTEMROOT","TEMP","TMP","USERPROFILE","WINDIR"]`

No PATH or caller-added variable is inherited. Private values are validated
for the current Windows host and discarded after process start. They are not
hashed into durable evidence. `environment_binding_sha256` hashes only a
public-safe canonical projection containing the exact name array,
`all_required_values_present=true`, `unexpected_name_count=0`, and
`private_values_persisted=false`. Missing, unreviewed, or drifting config or
environment state blocks process start. This contract does not create this
manifest, provision a credential, or claim a currently usable credential
path.

The installation receipt digest must be included in the later accepted
validator-bundle preimage before R2. The current release-state schema remains
unchanged.

## Pinned Inspect-Only Effect Boundary

This baseline supports exactly one inspect-only B or E task. Before
consumption, the adapter requires all of these cross-field facts:

- `role` is `B` or `E`;
- the active repository entry has
  `repository_code_execution_policy=forbidden`;
- lane `command_ids`, `validation_command_ids`, `mutation_scope`, and
  `expected_artifact_paths` are empty arrays;
- the entry's `maximum_mutation_scope` and `approved_commands` are empty
  arrays; and
- the turn timeout is exactly 120 seconds.

Any other lane is rejected before consumption with the first applicable
profile outcome. This is a strict subset of the unchanged public v1 request;
it introduces no caller field and does not reinterpret a nonempty command or
mutation scope.

The 780-byte config disables the shell, unified exec, code mode, collaboration,
apps, plugins, hooks, browser/computer/image/artifact tools, web search,
permission requests, skill search or installation, workspace dependencies,
goals, and the other named effectful feature surfaces. No command-execution
tool is model-visible. The turn sandbox is always read-only.

The freeform file-change tool cannot be disabled by a caller-controlled
request in this pinned release. Its remaining boundary is closed as follows:

1. `approvalPolicy=untrusted` maps to `AskForApproval::UnlessTrusted`.
2. The pinned patch safety classifier returns `AskUser` for that policy before
   considering writable-path auto-approval.
3. The pinned handler emits one `item/started` file-change item before entering
   the approval orchestrator.
4. The adapter never grants `item/fileChange/requestApproval`; it sends the
   exact decline response, records `AS-POL-001`, interrupts at most once, and
   performs bounded process-tree cleanup.
5. A missing request after a file-change start, an auto-approved file-change
   item, a changed file, or any write observation is `AS-POL-001` and fails R2.

These source-tag control bytes are part of the candidate proof:

| Source-tag path | Bytes | SHA-256 | Contracted fact |
| --- | ---: | --- | --- |
| `codex-rs/features/src/lib.rs` | `49982` | `737c3c3511408a3d9f35bd544359f6a5aeca4777460b9f34f902ccd38ec2a46d` | exact feature keys |
| `codex-rs/tools/src/tool_config.rs` | `6414` | `3357bef5f4cf60d38065b918a696724b7cfd16a5e9b879f1bbce05f79b2d55e3` | `shell_tool=false` yields a disabled shell surface |
| `codex-rs/core/src/safety.rs` | `7286` | `dd4d65e11b6aeee2cc6434b9b9090c646edeadc90b0c72e9da50f41c174d66b9` | `UnlessTrusted` patch classification requires approval |
| `codex-rs/core/src/tools/handlers/apply_patch.rs` | `25195` | `256987794c8239cfa808415b8fcd4dd26242e92212a91111267b461d655bfa19` | file-change begin precedes orchestrated approval |
| `codex-rs/core/src/tools/events.rs` | `29589` | `d0742ea4c7f3de2ead2701c8c5fdaf0963fed30cbb77b6c7673f19a9dd42ea6a` | begin item carries the parsed change set |
| `codex-rs/app-server-protocol/src/protocol/event_mapping.rs` | `25483` | `16cbca2e29c6b396e4a2e6d7ff4f5c7860a63d98b3e6859822adce5422298c27` | core item begin maps to the App Server notification |

The pinned command-approval request is not treated as a universal pre-effect
gate. This contract therefore claims neither command execution nor
repository mutation. Adding either requires a separate issue, exact source or
runtime mechanism, contract amendment, independent Codex E review, owner
activation, and graduated evidence. It may not inherit this baseline's R2
observation.

## Dedicated Direct Process Boundary

The later implementation may expose one private function only:

`start_pinned_app_server_once(validated_binding, private_installation)`

Its executable, argument vector, environment-name allowlist, cwd, stdio
topology, startup flags, and one-use guard are derived internally. There is no
parameter for arbitrary executable text, arguments, shell text, transport,
endpoint, service, SDK, process count, or retry.

The function may use one direct, non-shell Windows process-creation call. A
private standard-library process primitive is acceptable only when invoked
with `shell=False`, the exact held executable, the exact three arguments, no
caller extension point, redirected stdio pipes, and hidden-window behavior.
It must not be factored into or exported as a general launcher.

The process is attached at creation to one Windows Job Object with
kill-on-close. The adapter retains the process and Job handles through terminal
reconciliation. Descendants created by the App Server remain in that tree and
must not survive cleanup. A second root start under the same task request is
impossible even after known failure, timeout, crash, or ambiguous outcome.

The process transport is JSON Lines over its dedicated stdin and stdout.
Every message is one UTF-8 JSON object without BOM followed by one LF. The
JSON-RPC `jsonrpc` member is omitted, matching the pinned App Server protocol.
WebSocket, TCP, named pipe, Unix socket, remote-control daemon, inherited
terminal, console input, and shared stdio are forbidden.

## One-Use Consumption Guard

Before the process-start call, the adapter exclusively creates one private
consumption record keyed by the complete
`trusted_owner_native_task_request.v1` self-digest. Existing-record reuse is
false. The record is never deleted or reset.

Its directory is the Windows `LocalApplicationData` known-folder API result
followed by literal segments `MythicEdge`, `RolePool`,
`NativeAppServerConsumption`. Its basename is the complete lowercase
`task_request_sha256` plus `.v1.json`. The record is constructed and validated
in memory, then created directly with exclusive no-replace semantics, flushed,
closed, and read back before process start. No staging name, alternate root,
search, overwrite, or cleanup exists for this spent-state marker.

Its fields are:

`schema_version`, `task_request_sha256`, `claim_observation_sha256`,
`lane_packet_sha256`, `process_start_limit`, `consumed_at_utc`,
`consumption_status`, `consumption_sha256`.

`schema_version` is
`trusted_owner_app_server_consumption.v1`; `process_start_limit` is exactly
`1`; `consumption_status` is exactly `consumed_nonreusable`; and the last
member is the self-digest. It contains no path or private value.

Exclusive creation failure, prior existence, ambiguous creation, or readback
failure stops before process start and maps to
`unknown_outcome_reconciliation_required` when nonexistence cannot be proved.
No cleanup removes a consumption record. This guard is state, not authority.

## In-Memory Execution Binding

After all public and private preflight checks and before consumption, the
adapter constructs one closed in-memory object with these fields in order:

1. `schema_version`
2. `profile_contract_sha256`
3. `companion_contract_sha256`
4. `task_request_sha256`
5. `request_sha256`
6. `claim_observation_sha256`
7. `lane_packet_sha256`
8. `worktree_observation_sha256`
9. `registry_sha256`
10. `release_state_record_sha256`
11. `skill_tree_sha256`
12. `repository_id`
13. `issue_url`
14. `role`
15. `operation_id`
16. `predecessor_packet_sha256`
17. `cwd_identity_sha256`
18. `model_request_mode`
19. `requested_model`
20. `requested_effort`
21. `sandbox_binding_sha256`
22. `approval_policy`
23. `role_instruction_sha256`
24. `instruction_packet_sha256`
25. `role_pool_skill_sha256`
26. `output_schema_sha256`
27. `installation_receipt_sha256`
28. `executable_sha256`
29. `protocol_schema_sha256`
30. `runtime_config_manifest_sha256`
31. `environment_binding_sha256`
32. `turn_timeout_seconds`
33. `execution_binding_sha256`

`schema_version` is `trusted_owner_app_server_execution_binding.v1`.
`model_request_mode` is exactly
`platform_default_then_bind_thread_response`; `requested_model` and
`requested_effort` are exactly null. `approval_policy` is exactly
`untrusted`. The final member is the self-digest.

`cwd_identity_sha256` binds the private worktree path through the already
accepted worktree observation; no path is serialized. `predecessor_packet_sha256`
is null only where the profile allows no predecessor. `turn_timeout_seconds`
uses the deterministic rule in the resource section.

All `*_sha256` fields are lowercase 64-hex strings. `repository_id` is a
positive integer; `issue_url`, role, operation, and profile scalar values use
the existing profile types. The two requested values are JSON null.
`turn_timeout_seconds` is an integer. `sandbox_binding_sha256` hashes a
public-safe canonical projection that substitutes `cwd_identity_sha256` for
the private writable-root string; the raw RPC policy remains in bounded
memory. No private path or environment value contributes bytes to durable
evidence.

The effective model and reasoning effort returned by `thread/start` must both
be nonempty. Their domain-separated hashes are bound in the platform receipt,
and the exact returned strings are echoed into `turn/start`. A
`model/rerouted` notification is forbidden. Thus null means exact
platform-default selection before thread creation, not an unbound turn.

## Role, Instruction, Skill, And Source Binding

The role map is closed:

| Role | Exact repository role contract |
| --- | --- |
| `A` | `docs/agent_threads/problem_representation.md` |
| `B` | `docs/agent_threads/module_contract.md` |
| `D` | `docs/agent_threads/module_fixer.md` |
| `E` | `docs/agent_threads/review.md` |
| `F` | `docs/agent_threads/module_submitter.md` |

The selected role file must be ordinary, non-reparse, inside the exact
worktree, and SHA-256-bound before process start. Role C, G, H, or an unknown
role rejects before consumption.

The exact developer instruction is:

```text
Execute exactly one Mythic Edge trusted-owner lane from the supplied canonical instruction packet. Follow the loaded AGENTS.md, the role contract, and the exact repository-owned Role Pool skill. Do not infer or widen authority. Return only one JSON object matching the supplied output schema.
```

Its UTF-8 byte count and SHA-256 are declared in the validation section.

The turn text is one canonical
`trusted_owner_app_server_instruction_packet.v1` object with these fields in
order:

`schema_version`, `task_request_sha256`, `lane_packet_sha256`, `role`,
`operation_id`, `issue_url`, `predecessor_packet_sha256`,
`role_contract_path`, `role_contract_sha256`, `role_pool_skill_sha256`,
`output_schema_sha256`, `lane_packet_json`, `predecessor_packet_json`,
`instruction_packet_sha256`.

The two `*_json` fields contain the exact canonical JSON text of the validated
objects; predecessor text is null exactly when no predecessor is allowed.
The packet contains no conversation, summary, transcript, memory, sibling-lane
content, private path, credential, environment value, or unbound issue body.

The turn input array contains exactly two entries in order:

1. one `text` input whose `text` is the canonical instruction packet and whose
   `text_elements` array is empty; and
2. one `skill` input naming `mythic-edge-role-pool` and the private absolute
   path to its exact installed `SKILL.md`.

The skill path exists only in the in-memory RPC message. Source/install tree
equality and the request's `skill_tree_sha256` bind it. No other skill,
mention, image, audio, URL, or local-media input is permitted.

## Initialize And Thread Binding

Request IDs are deterministic public-safe strings:

- initialize: `rp-init-` plus the first 32 hex characters of
  `task_request_sha256`;
- thread start: `rp-thread-` plus the same 32 characters;
- turn start: `rp-turn-` plus the same 32 characters; and
- interrupt, only if used: `rp-interrupt-` plus the same 32 characters.

The prefixes make all four IDs distinct. No caller provides them.

The adapter sends exactly one `initialize` request. Its client info is
`name=mythic-edge-role-pool`, `title=Mythic Edge Role Pool`, and
`version=1`. Capabilities are exactly:

- `experimentalApi=false`;
- `mcpServerOpenaiFormElicitation=false`;
- `optOutNotificationMethods=null`; and
- `requestAttestation=false`.

The response must correlate to the exact request ID and report Windows
platform values and the pinned CLI version. Private `codexHome` is validated
in memory and never serialized. The adapter then sends exactly one
`initialized` notification with no ID and no parameters. No second handshake
is permitted.

The one `thread/start` request uses these exact values:

| Field | Value |
| --- | --- |
| `approvalPolicy` | `untrusted` |
| `approvalsReviewer` | `user` |
| `baseInstructions` | null |
| `config` | null |
| `cwd` | exact private validated worktree root |
| `developerInstructions` | exact fixed instruction above |
| `ephemeral` | true |
| `model` | null |
| `modelProvider` | null |
| `personality` | null |
| `sandbox` | exactly `read-only` |
| `serviceName` | `mythic-edge-role-pool` |
| `serviceTier` | null |
| `sessionStartSource` | null |
| `threadSource` | null |

The response must bind the request ID, one fresh thread ID, `ephemeral=true`,
an empty turn array, no parent or fork, exact cwd, exact approval policy and
reviewer, exact sandbox mode, one nonempty effective model, one nonempty
reasoning effort, and one instruction-source array.

Before `turn/start`, the adapter requires `instructionSources` to contain
exactly one entry resolving to the accepted worktree-root `AGENTS.md`. The file
must be ordinary, non-reparse, and digest-bound. The absolute value remains
private. Missing, extra, duplicated, reordered, outside-worktree, global,
user-profile, plugin, package, or sibling-repository instruction sources stop
before the turn.

The public-safe `instruction_sources_sha256` hashes the canonical array
containing only `relative_path=AGENTS.md` and that file's SHA-256.

## Turn Binding And Approval Enforcement

The adapter sends one `turn/start` only after the instruction-source check.
Its exact fields are:

| Field | Value |
| --- | --- |
| `approvalPolicy` | `untrusted` |
| `approvalsReviewer` | `user` |
| `clientUserMessageId` | `rp-message-` plus the first 32 task-request hex characters |
| `cwd` | exact private validated worktree root |
| `effort` | exact nonempty reasoning effort returned by `thread/start` |
| `input` | exact two-entry instruction/skill array |
| `model` | exact nonempty model returned by `thread/start` |
| `outputSchema` | exact canonical role-output schema below |
| `personality` | null |
| `sandboxPolicy` | exact derived policy below |
| `serviceTier` | null |
| `summary` | null |
| `threadId` | exact returned thread ID |

`sandboxPolicy` is exactly
`{"networkAccess":false,"type":"readOnly"}`. Workspace-write and every
writable-root variant are invalid for this baseline.

The adapter recognizes only these server request methods for deterministic
denial:

- `item/commandExecution/requestApproval`; and
- `item/fileChange/requestApproval`.

Each request must correlate to the active thread and turn. The adapter grants
neither request. Receipt counts for both methods must remain zero on
`AS-ACC-001`; observing either method, any command item, any file-change item,
any command output, or any diff selects `AS-POL-001`. An unrecognized server
request is also denied and selects `AS-POL-001`.

The R2 characterization must prove zero command starts, zero command approval
requests, zero file-change starts, zero file-change approval requests, zero
changed files, and zero diff notifications. A runtime that executes or begins
either effect cannot satisfy this baseline.

`auto_review` and `guardian_subagent` are forbidden. User input, permission
expansion, dynamic tools, attestation, token refresh, MCP elicitation, skill
approval, and sandbox widening are never approved.

## Closed Notification And Method Surface

The baseline may consume only these server notifications:

- `thread/started`
- `thread/status/changed`
- `thread/tokenUsage/updated`
- `turn/started`
- `turn/completed`
- `turn/plan/updated`
- `item/started`
- `item/completed`
- `item/agentMessage/delta`
- `item/plan/delta`
- `item/reasoning/summaryPartAdded`
- `item/reasoning/summaryTextDelta`
- `item/reasoning/textDelta`

Within `item/started` and `item/completed`, only agent-message, reasoning, and
plan item variants are admitted. A command-execution or file-change variant,
or any removed command, file-change, patch, or diff notification, selects
`AS-POL-001`. All stream content remains in bounded memory. Only the final
validated role output leaves it.

Any other notification or server request is a protocol-policy breach. This
explicitly prohibits remote control, plugins, hooks, MCP, app/marketplace
events, external-agent import, realtime, thread resume/fork/steer/injection,
thread mutation, process RPC, filesystem RPC, dynamic tools, model rerouting,
second-turn behavior, and replacement-task behavior. The adapter sends no
`thread/read`, `thread/list`, `thread/resume`, `thread/fork`, `turn/steer`,
`thread/inject`, or other reconciliation RPC. Unknown remains unknown.

## Exact Role Output Schema

The final assistant output must be one object with fields in this order:

`schema_version`, `result`, `files_changed`, `validation`, `handoff`.

`schema_version` is `trusted_owner_app_server_role_output.v1`. `result` is
`completed`, `blocked`, or `finding`; the model cannot assert `unknown`.
File-change, validation, and handoff records use the profile's existing scalar
and ordering rules, except that the adapter computes the final handoff
self-digest and all coordinator-owned result fields. Authority flags are
derived by the coordinator and never accepted from model output.

The canonical JSON Schema supplied to `turn/start` is:

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","additionalProperties":false,"properties":{"files_changed":{"items":{"additionalProperties":false,"properties":{"after_sha256":{"pattern":"^[0-9a-f]{64}$","type":["string","null"]},"before_sha256":{"pattern":"^[0-9a-f]{64}$","type":["string","null"]},"change_kind":{"enum":["added","deleted","modified"],"type":"string"},"path":{"minLength":1,"type":"string"}},"required":["path","change_kind","before_sha256","after_sha256"],"type":"object"},"type":"array"},"handoff":{"additionalProperties":false,"properties":{"finding_ids":{"items":{"minLength":1,"type":"string"},"type":"array"},"next_role":{"enum":["A","B","C","D","E","F","G","H",null]},"source_artifact_paths":{"items":{"minLength":1,"type":"string"},"type":"array"},"status":{"enum":["blocked","changes_required","complete","no_next_role"],"type":"string"},"stop_reason":{"type":["string","null"]}},"required":["status","next_role","source_artifact_paths","finding_ids","stop_reason"],"type":"object"},"result":{"enum":["blocked","completed","finding"],"type":"string"},"schema_version":{"const":"trusted_owner_app_server_role_output.v1","type":"string"},"validation":{"items":{"additionalProperties":false,"properties":{"command_id":{"minLength":1,"type":"string"},"evidence_sha256":{"pattern":"^[0-9a-f]{64}$","type":["string","null"]},"exit_code":{"type":["integer","null"]},"status":{"enum":["blocked","failed","not_run","passed"],"type":"string"}},"required":["command_id","status","exit_code","evidence_sha256"],"type":"object"},"type":"array"}},"required":["schema_version","result","files_changed","validation","handoff"],"type":"object"}
```

Its UTF-8 byte count and SHA-256, without a final LF because it is embedded as
an RPC value, are declared in the validation section. Semantic validation
additionally requires `files_changed=[]` and `validation=[]` for this
inspect-only baseline, sorted unique handoff arrays, allowed role routing,
authority conformity, and no raw transcript or private value. Any nonempty
file-change or validation array is invalid even if it is schema-valid.

## Public-Safe Platform Receipt

On a known terminal outcome, the adapter constructs one canonical receipt with
these fields in order:

1. `schema_version`
2. `task_request_sha256`
3. `execution_binding_sha256`
4. `installation_receipt_sha256`
5. `executable_sha256`
6. `protocol_schema_sha256`
7. `initialize_request_id`
8. `thread_start_request_id`
9. `turn_start_request_id`
10. `interrupt_request_id`
11. `thread_id_sha256`
12. `turn_id_sha256`
13. `effective_model_sha256`
14. `effective_effort_sha256`
15. `instruction_sources_sha256`
16. `process_start_count`
17. `initialize_count`
18. `initialized_count`
19. `thread_start_count`
20. `turn_start_count`
21. `interrupt_count`
22. `command_approval_count`
23. `file_change_approval_count`
24. `terminal_notification_sha256`
25. `role_output_sha256`
26. `lifecycle_case`
27. `profile_terminal_projection`
28. `process_exit_class`
29. `cleanup_status`
30. `started_at_utc`
31. `terminal_at_utc`
32. `platform_receipt_sha256`

`schema_version` is
`trusted_owner_app_server_platform_receipt.v1`. The final member is the
self-digest. Hash fields are lowercase 64-hex or null exactly where their
owning phase was not reached. The three required request IDs use the exact
derived values above; `interrupt_request_id` is either that one exact derived
value or null. Counts are nonnegative integers within this contract's limits.
Timestamps are whole-second UTC or null exactly where process start or
terminal classification was not reached.

`lifecycle_case` is one of the 25 ordered cases below.
`profile_terminal_projection` is one of the profile's existing 20 terminal
outcomes for a projected failure, or null only for `AS-ACC-001` while
downstream profile validation remains pending. `process_exit_class` is
`not_started`, `exited_zero`, `exited_nonzero`, `terminated_job`,
`running_at_classification`, or `unknown`. `cleanup_status` is `not_reached`,
`complete`, `known_incomplete`, or `unknown`. The receipt is never
success-like when a required field is null.

For `AS-ACC-001`, `command_approval_count` and
`file_change_approval_count` are exactly zero. A nonzero value can appear only
in a failure receipt selecting `AS-POL-001`; it never becomes accepted task
evidence.

Thread and turn IDs are domain-separated SHA-256 values over
`app_server_thread_id`, NUL, raw ID and `app_server_turn_id`, NUL, raw ID.
Raw IDs remain in bounded memory. Effective model and effort use the same
domain-separated pattern. Request IDs are public because they are derived only
from the already-public task-request digest.

`terminal_notification_sha256` hashes a public-safe projection containing only
the method, thread-ID digest, turn-ID digest, closed terminal status, and
whole-second receipt time. It does not hash or retain raw transcript,
reasoning, command output, error text, or item content.

The platform receipt contains no raw paths, IDs, transcript, stderr, exception,
stack trace, command output, credentials, tokens, environment values, account
data, ACLs, process IDs, handles, or private diagnostics.

For `AS-ACC-001` only, the existing
`trusted_owner_native_task_receipt.v1` uses:

- `task_id=app_server_` plus the first 32 characters of
  `thread_id_sha256`;
- `platform_receipt_ref=role_pool:app_server:` plus the first 32 characters
  of `platform_receipt_sha256`; and
- `platform_receipt_sha256` equal to the exact companion receipt self-digest.

No public task receipt is issued for a failed or unknown process lifecycle.
The profile result projects the known failure or unknown state directly. A
companion platform receipt may be published only after a valid task-request
digest was accepted and consumption succeeded; preconsumption rejection has
no companion receipt.

## Receipt Publication And Custody

The public-safe platform receipt is durable local evidence. Its directory is
resolved only from the Windows `LocalApplicationData` known-folder API,
followed by literal segments:

`MythicEdge`, `RolePool`, `NativeAppServerReceipts`

The final basename is the 64-character lowercase `task_request_sha256`
followed by `.v1.json`. The same-directory staging basename is a dot, the
first 32 task-request hex characters, and `.v1.tmp`. Absolute paths never
leave bounded memory.

Before staging appears, the complete receipt is constructed and validated in
memory. Publication requires ordinary non-reparse fixed-local-NTFS ancestors,
exclusive staging creation, write, flush, close, exact staging readback,
final-path absence recheck, same-directory atomic no-replace publication, and
exact final readback. The final file contains one canonical object and one
final LF.

An existing final, appeared final, unknown move result, or conflicting readback
is preserved and projects
`unknown_outcome_reconciliation_required`. No overwrite, replacement,
in-place repair, or second publication is permitted. Cleanup may remove only a
proven adapter-owned unpublished staging file. Uncertain ownership or cleanup
projects `AS-CLN-UNK-001`.

The final receipt is immutable. Its public
`role_pool:app_server:<digest-prefix>` reference does not reveal the local
path. The existing task receipt and result packet may bind that reference and
digest only after final readback succeeds.

## Resource, Timeout, And Cleanup Bounds

Hard limits:

| Resource | Limit |
| --- | --- |
| process root starts | 1 |
| initialize requests | 1 |
| initialized notifications | 1 |
| thread/start requests | 1 |
| turn/start requests | 1 |
| turn/interrupt requests | 1 |
| automatic retries | 0 |
| overload retries | 0 |
| replacement processes, threads, or turns | 0 |
| stdin JSON line | 1,048,576 bytes |
| stdout JSON line | 1,048,576 bytes |
| stderr line | 65,536 bytes |
| total stdin | 4,194,304 bytes |
| total stdout | 67,108,864 bytes |
| total stderr | 4,194,304 bytes |
| parsed-message queue | 256 messages and 8,388,608 bytes |
| startup wait | 15 seconds |
| initialize response | 15 seconds |
| thread/start response | 30 seconds |
| interrupt terminal grace | 15 seconds |
| ordinary process-exit grace | 10 seconds |
| forced Job close confirmation | 10 seconds |

The turn timeout is exactly `120` seconds. The parent formula reduces to this
value because both command arrays must be empty. Any other value rejects
before consumption.

Stdout and stderr are drained concurrently into bounded queues. Any line,
aggregate, queue, parser, ordering, correlation, or timeout limit breach sends
at most one interrupt if a turn ID is known, then closes the process Job.
Buffers are discarded after public-safe projection.

After timeout, the adapter sends one correlated `turn/interrupt` at most once.
If a valid terminal notification arrives within 15 seconds, it derives the
known interrupted outcome. Otherwise the state is
`unknown_outcome_reconciliation_required`. It never sends a second interrupt,
turn, thread start, or process start.

Cleanup closes stdin, waits within the stated grace, closes the Job to
terminate the tree when needed, drains bounded remaining output, and proves no
matching tree survives. Uncertain cleanup is unknown, never successful.
Consumption state and any observed final public receipt are preserved.

## Closed Process Lifecycle

The adapter owns, and no caller supplies, one typed raw observation with
exactly `phase`, `raw_observation`, and `consumption_state`. Phase validators
evaluate the case predicates below in ordinal order, emit the first true
candidate, and discard later candidates. Profile preflight first applies the
unchanged profile priorities 1 through 15. After successful consumption, the
companion applies cases 2 through 25 below. The terminal catch-all predicates
guarantee that one of `AS-UNK-001`, `AS-KNOWN-FAIL-001`, or `AS-ACC-001` is
true if no earlier post-consumption predicate is true.

A raw tuple is representable if and only if it exactly matches one row in this
canonical registry. Rows are arrays whose fields are named once by `fields`.
Ordinals are contiguous and determine precedence. The registry is UTF-8
without BOM, no insignificant whitespace, and exactly one final LF:

```json
{"schema_version":"trusted_owner_app_server_lifecycle_registry.v1","fields":["ordinal","phase","raw_observation","consumption_state","lifecycle_case","profile_projection"],"rows":[[1,"preflight","profile_priority_01_request_or_packet_invalid","not_consumed","AS-BLK-001","blocked_request_or_packet_invalid"],[2,"preflight","profile_priority_02_no_wip_authority","not_consumed","AS-BLK-001","blocked_no_wip_authority"],[3,"preflight","profile_priority_03_skill_source_drift","not_consumed","AS-BLK-001","blocked_skill_source_drift"],[4,"preflight","profile_priority_04_registry_invalid","not_consumed","AS-BLK-001","blocked_registry_missing_or_invalid"],[5,"preflight","profile_priority_05_release_state_invalid","not_consumed","AS-BLK-001","blocked_release_state_invalid"],[6,"preflight","profile_priority_06_repository_inactive","not_consumed","AS-BLK-001","blocked_repository_inactive"],[7,"preflight","profile_priority_07_repository_identity_mismatch","not_consumed","AS-BLK-001","blocked_repository_identity_mismatch"],[8,"preflight","profile_priority_08_role_or_operation_not_allowed","not_consumed","AS-BLK-001","blocked_role_or_operation_not_allowed"],[9,"preflight","profile_priority_09_command_not_approved","not_consumed","AS-BLK-001","blocked_command_not_approved"],[10,"preflight","profile_priority_10_external_isolation_required","not_consumed","AS-BLK-001","blocked_external_isolation_required"],[11,"preflight","profile_priority_11_mixed_profile_wave","not_consumed","AS-BLK-001","blocked_mixed_profile_wave"],[12,"preflight","profile_priority_12_predecessor_invalid","not_consumed","AS-BLK-001","blocked_predecessor_packet_invalid"],[13,"preflight","profile_priority_13_cross_lane_overlap","not_consumed","AS-BLK-001","blocked_cross_lane_overlap"],[14,"preflight","profile_priority_14_capacity_exceeded","not_consumed","AS-BLK-001","blocked_capacity_exceeded"],[15,"preflight","profile_priority_15_f_boundary","not_consumed","AS-BLK-001","blocked_f_boundary"],[16,"consumption","record_prior_or_collision","not_consumed","AS-CNS-REUSE-001","blocked_request_or_packet_invalid"],[17,"consumption","record_state_or_commit_unknown","unknown","AS-CNS-UNK-001","unknown_outcome_reconciliation_required"],[18,"process_start","start_known_not_started","consumed","AS-START-001","failed_lane_known"],[19,"process_start","start_observation_unknown","consumed","AS-START-UNK-001","unknown_outcome_reconciliation_required"],[20,"handshake","handshake_known_invalid","consumed","AS-HSK-001","failed_lane_known"],[21,"thread_start","thread_start_known_invalid","consumed","AS-THR-001","failed_lane_known"],[22,"pre_turn","pre_turn_binding_known_invalid","consumed","AS-INS-001","failed_lane_known"],[23,"turn_start","turn_start_known_invalid","consumed","AS-TURN-001","failed_lane_known"],[24,"execution","policy_breach_known","consumed","AS-POL-001","failed_lane_known"],[25,"execution","timeout_terminal_interrupted_known","consumed","AS-TMO-001","failed_lane_known"],[26,"execution","timeout_or_interrupt_terminal_unknown","consumed","AS-TMO-UNK-001","unknown_outcome_reconciliation_required"],[27,"role_output","role_output_known_invalid","consumed","AS-OUT-001","failed_lane_known"],[28,"execution","process_exit_before_terminal_known","consumed","AS-EXIT-001","failed_lane_known"],[29,"receipt_sealing","receipt_sealing_known_failure","consumed","AS-SEAL-001","failed_lane_known"],[30,"receipt_staging","staging_failure_cleanup_complete","consumed","AS-STG-001","failed_lane_known"],[31,"receipt_publication","final_collision_known","consumed","AS-COL-001","unknown_outcome_reconciliation_required"],[32,"receipt_publication","commit_state_unknown","consumed","AS-CMT-UNK-001","unknown_outcome_reconciliation_required"],[33,"receipt_readback","final_readback_known_invalid","consumed","AS-RDB-INV-001","failed_lane_known"],[34,"receipt_readback","final_readback_unknown","consumed","AS-RDB-UNK-001","unknown_outcome_reconciliation_required"],[35,"cleanup","cleanup_known_incomplete","consumed","AS-CLN-FAIL-001","failed_lane_known"],[36,"cleanup","cleanup_unknown","consumed","AS-CLN-UNK-001","unknown_outcome_reconciliation_required"],[37,"terminal","required_fact_unknown_no_specific_case","consumed","AS-UNK-001","unknown_outcome_reconciliation_required"],[38,"terminal","required_fact_known_invalid_no_specific_case","consumed","AS-KNOWN-FAIL-001","failed_lane_known"],[39,"terminal","all_required_facts_valid","consumed","AS-ACC-001",null]],"lifecycle_case_counts":[["AS-BLK-001",15],["AS-CNS-REUSE-001",1],["AS-CNS-UNK-001",1],["AS-START-001",1],["AS-START-UNK-001",1],["AS-HSK-001",1],["AS-THR-001",1],["AS-INS-001",1],["AS-TURN-001",1],["AS-POL-001",1],["AS-TMO-001",1],["AS-TMO-UNK-001",1],["AS-OUT-001",1],["AS-EXIT-001",1],["AS-SEAL-001",1],["AS-STG-001",1],["AS-COL-001",1],["AS-CMT-UNK-001",1],["AS-RDB-INV-001",1],["AS-RDB-UNK-001",1],["AS-CLN-FAIL-001",1],["AS-CLN-UNK-001",1],["AS-UNK-001",1],["AS-KNOWN-FAIL-001",1],["AS-ACC-001",1]],"profile_projection_counts":[["blocked_request_or_packet_invalid",2],["blocked_no_wip_authority",1],["blocked_skill_source_drift",1],["blocked_registry_missing_or_invalid",1],["blocked_release_state_invalid",1],["blocked_repository_inactive",1],["blocked_repository_identity_mismatch",1],["blocked_role_or_operation_not_allowed",1],["blocked_command_not_approved",1],["blocked_external_isolation_required",1],["blocked_mixed_profile_wave",1],["blocked_predecessor_packet_invalid",1],["blocked_cross_lane_overlap",1],["blocked_capacity_exceeded",1],["blocked_f_boundary",1],["failed_lane_known",14],["unknown_outcome_reconciliation_required",8],[null,1]]}
```

The complete registry is `5614` bytes and has SHA-256
`0d50774b0b8cb4f47a11b2cde2919f73ac887dacced761dfa4ebd7ea95e4f517`.

The exact selector is:

1. Reject a raw object with an unknown or duplicate field, wrong scalar type,
   or value outside the registry columns.
2. Evaluate the ordered phase predicates and emit only the lowest-ordinal true
   candidate.
3. Compare the emitted three-field raw tuple to all registry rows.
4. Require exactly one exact match and return that row's lifecycle case and
   profile projection.
5. Before consumption, selector construction or matching failure is the
   priority-1 `AS-BLK-001` tuple. After consumption, it is the
   `AS-UNK-001` tuple. Neither path retries or invents a success.

The canonical audit domain is exactly the 39 registry tuples, not a Cartesian
product of phase-inconsistent scalar values. Its bound counts are
`tuple_count=39`, `overlap_count=0`, `uncovered_count=0`, and
`unreachable_row_count=0`. Each lifecycle case is reachable; `AS-BLK-001`
owns 15 exact profile-preflight tuples and every other lifecycle case owns one.

The selected case descriptions are:

| Order | Case | Exact trigger | Existing profile projection |
| --- | --- | --- | --- |
| 1 | `AS-BLK-001` | Before valid consumption, any request, lane, profile, registry, release, worktree, role, predecessor, schema, installation, runtime-config, executable, selector-domain, or canonical binding is known invalid. | first applicable profile outcome from priorities 1 through 15 |
| 2 | `AS-CNS-REUSE-001` | The exact validated consumption record already exists, or exclusive creation reports a known collision with that exact record. | `blocked_request_or_packet_invalid` |
| 3 | `AS-CNS-UNK-001` | Consumption-record existence, ownership, bytes, exclusive creation, commit, or readback is unavailable or conflicting. | `unknown_outcome_reconciliation_required` |
| 4 | `AS-START-001` | Consumption succeeded and process start is known not to have occurred. | `failed_lane_known` |
| 5 | `AS-START-UNK-001` | Consumption succeeded and process-start occurrence cannot be established. | `unknown_outcome_reconciliation_required` |
| 6 | `AS-HSK-001` | With known process identity, initialize or initialized correlation, shape, count, platform, version, or deadline is known invalid. | `failed_lane_known` |
| 7 | `AS-THR-001` | Thread start is known rejected, malformed, duplicated, mismatched, absent at deadline, or otherwise invalid. | `failed_lane_known` |
| 8 | `AS-INS-001` | Instruction source, effective model or effort, ephemeral state, history, cwd, sandbox, approval, parent, or fork state is known invalid before turn start. | `failed_lane_known` |
| 9 | `AS-TURN-001` | Turn start is known rejected, malformed, duplicated, mismatched, absent at deadline, or otherwise invalid. | `failed_lane_known` |
| 10 | `AS-POL-001` | A forbidden method, notification, approval, command, mutation, remote, plugin, hook, MCP, skill, model reroute, source, path, output, second turn, or replacement is known observed. | `failed_lane_known` |
| 11 | `AS-TMO-001` | Timeout occurs, at most one interrupt is sent, and a valid known terminal interrupted state is observed. | `failed_lane_known` |
| 12 | `AS-TMO-UNK-001` | Timeout or interrupt occurs and the required terminal state is unavailable or conflicting. | `unknown_outcome_reconciliation_required` |
| 13 | `AS-OUT-001` | Terminal completion is known but the role output or coordinator projection is known invalid. | `failed_lane_known` |
| 14 | `AS-EXIT-001` | Process exit before a required terminal state and terminal absence are both proven, with no conflicting process or protocol fact. | `failed_lane_known` |
| 15 | `AS-SEAL-001` | Operation data is known, but canonical platform-receipt construction or in-memory validation fails before staging appears. | `failed_lane_known` |
| 16 | `AS-STG-001` | Staging creation, write, flush, close, or readback has a known failure; final absence and staging ownership are proven; bounded owned-staging cleanup is known complete. | `failed_lane_known` |
| 17 | `AS-COL-001` | The final receipt exists before publication or appears before the atomic move. The object is preserved. | `unknown_outcome_reconciliation_required` |
| 18 | `AS-CMT-UNK-001` | Atomic publication return, final existence, object identity, or commit state is unavailable or conflicting. | `unknown_outcome_reconciliation_required` |
| 19 | `AS-RDB-INV-001` | Atomic publication is known committed and exact final readback proves immutable noncanonical, digest-invalid, or semantically invalid bytes. | `failed_lane_known` |
| 20 | `AS-RDB-UNK-001` | Atomic publication may have committed but exact final readback or final identity is unavailable or conflicting. | `unknown_outcome_reconciliation_required` |
| 21 | `AS-CLN-FAIL-001` | A process descendant or adapter-owned unpublished staging object is known to remain after its bounded cleanup requirement. | `failed_lane_known` |
| 22 | `AS-CLN-UNK-001` | Process-tree, bounded-drain, staging ownership, staging cleanup, or final-object state is uncertain. | `unknown_outcome_reconciliation_required` |
| 23 | `AS-UNK-001` | A required process, protocol, approval, terminal, output, receipt, or cleanup fact is unavailable or conflicting and no earlier specific unknown row applies. | `unknown_outcome_reconciliation_required` |
| 24 | `AS-KNOWN-FAIL-001` | A required post-consumption fact is known invalid and no earlier specific known-failure row applies. | `failed_lane_known` |
| 25 | `AS-ACC-001` | Exactly one process, handshake, thread, turn, valid terminal completion, valid role output, complete cleanup, and exact canonical receipt readback all succeed. | no profile terminal outcome yet; existing result, handoff, claim-release, and wave logic continues |

Rows 23 and 24 explicitly exclude every earlier row. Known failures cannot
fall through to unknown, and unknown facts cannot become known failure or
success. `AS-ACC-001` does not mean `accepted_wave_complete`; it makes only
the unchanged `trusted_owner_native_task_receipt.v1` eligible for downstream
profile validation. Claim release, result and handoff validation, and every
other lane remain profile-owned prerequisites.

No case authorizes retry. Before implementation acceptance, a validator must
parse the exact registry bytes, recompute its digest and counts, evaluate all
39 canonical tuples with the exact selector, and reproduce
`overlap_count=0`, `uncovered_count=0`, and
`unreachable_row_count=0`.

## R0 Fake Transport And R2 Real Characterization

R0 implementation evidence is fake-transport only. It starts no process,
opens no installed executable, contacts no Codex service, uses no credential,
creates no task, and mutates no registry or release state.

Focused R0 tests must prove at least:

1. exact v1 request-to-execution-binding derivation;
2. exact one-process, one-handshake, one-thread, one-turn happy path;
3. request-ID correlation and duplicate-response rejection;
4. instruction-source allowlist acceptance and every missing/extra/source
   rejection;
5. effective model/effort echo and model-reroute rejection;
6. the exact 780-byte config, disabled shell/tool surface, empty command,
   validation, mutation, and artifact bindings, and read-only sandbox;
7. deterministic denial of every command or file-change request and
   `AS-POL-001` projection for every command, file-change, patch, or diff
   observation;
8. forbidden remote, plugin, hook, MCP, SDK, fork, resume, steer, injection,
   second-turn, replacement, command, and mutation behavior;
9. invalid role output and private-value receipt rejection;
10. every line, queue, aggregate, timeout, interrupt, process-exit, and cleanup
    boundary;
11. known start failure versus unknown start outcome;
12. no retry after overload, timeout, unknown, or known failure;
13. exact platform receipt and unchanged public task receipt mapping;
14. exact 39-tuple lifecycle-registry digest, counts, selector, and
    overlap/uncovered/reachability closure; and
15. zero real process-start calls under the fake transport.

A real App Server process is first eligible only at the existing R2 rung, after
all earlier ladder prerequisites. R2 additionally requires a fresh owner
decision binding the exact accepted implementation, tests, installation
receipt, runtime config, credential custody, executable and schema identities,
task request, lane, timeout, result destination, and cleanup plan. It permits
one low-risk B or E lane only, as the existing ladder requires.

Independent Codex E must observe that the real pinned process:

- honors every exact protocol and resource limit;
- exposes no ambient instruction source;
- exposes no command tool, emits no command or file-change item or approval
  request, changes no file, and emits no patch or diff;
- emits no remote-control, plugin, hook, MCP, model-reroute, second-turn, or
  replacement behavior;
- produces one exact receipt and complete cleanup; and
- establishes all nine #757 facts.

This R2 evidence characterizes task creation and lifecycle only. It does not
authorize or establish command execution, repository mutation, or eligibility
for a later rung whose exact lane packet requires either effect. Such a rung
remains blocked on the separately reviewed effectful-surface amendment named
above; the ladder's rung definitions and promotion counts do not change.

Failure preserves `capability_verdict=insufficient_evidence` or establishes
`capability_unavailable` only when authoritative evidence directly
contradicts a fact. It cannot trigger fallback.

## Later Implementation Envelope

A separately authorized Codex C may change exactly:

1. `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_server_adapter.py`
2. `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_server_adapter.py`
3. `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py`
4. `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py`

The first file owns the dedicated adapter. The second owns fake-transport
tests. The two existing files may receive only the minimal production-observer
selection, invocation, validation, and focused integration changes.

No SDK dependency, package manager, general launcher helper, shell wrapper,
service, broker, standalone App Server asset, schema generator, registry,
release-state file, credential helper, hook, plugin, MCP configuration, or
fifth path is in scope. If implementation needs another path or a v2 public
task schema, Codex C must stop and route the exact mismatch to Codex B.

## Canonical Rules And Fixed Digests

Every object defined here rejects duplicate or unknown fields. Objects use the
listed field order. Arrays use their stated fixed or ordinal order. Canonical
objects use UTF-8 without BOM, no insignificant whitespace, and exactly one
final LF.

A self-digest preimage removes only the named final self-digest member,
preserves every other byte and the final LF, and hashes the resulting complete
canonical byte sequence.

Fixed values:

| Item | UTF-8 byte count | SHA-256 |
| --- | ---: | --- |
| exact developer instruction, no final LF | `292` | `2d084e88397914bb97e1bae60be44ffeb3d29c2577f984db966937c1c91beffa` |
| canonical role-output JSON Schema, no final LF | `1663` | `fc0ade6cf9664b32b3b3e83935f69f01418356897f16e937ed597aedfdd5b247` |
| pinned complete protocol schema aggregate | `590325` | `08cc0c836bf0caca1e65b92956c3d57fd59c6be9b66277f77afe1cf65aefa592` |
| exact inspect-only `config.toml`, one final LF | `780` | `fae8d0a1992225d30d2275c247629b31f39b3b9ee4578963fb121e1093510412` |
| canonical lifecycle registry, one final LF | `5614` | `0d50774b0b8cb4f47a11b2cde2919f73ac887dacced761dfa4ebd7ea95e4f517` |

Codex E must independently recompute these exact values. Any mismatch blocks
acceptance.

## Validation And Acceptance

Codex B validation:

- refresh `origin/main`, issue #758, tracker #746, PRs, ADR-0008, profile, and
  #757 artifacts;
- verify the pinned release tag, commit, asset name, byte count, and SHA-256
  through GitHub release metadata without acquiring the executable;
- verify the generated protocol-schema source artifact, byte count, and
  SHA-256 from the exact tag without generating schemas;
- verify the complete aggregate contains every contracted envelope, request,
  response, and notification definition;
- recompute the inspect-only config and all six pinned effect-control source
  files;
- strictly inspect the existing v1 task request and receipt;
- parse and reproduce the 39-tuple lifecycle registry, counts, selector, and
  zero/zero/zero audit;
- recompute both final contract SHA-256 values;
- run `git diff --check`;
- run `py tools\check_agent_docs.py`;
- run `py tools\check_protected_surfaces.py --base origin/main`;
- run `py tools\check_secret_patterns.py --base origin/main`;
- pipe the two changed contract paths to
  `py tools\select_validation.py --paths-from-stdin --base origin/main`; and
- confirm only the two contract files changed and no generated residue exists.

Independent Codex E acceptance must lead with findings and verify:

- no public request/receipt schema or profile terminal-vocabulary change;
- exact derivability of every execution-binding field from accepted inputs;
- exact release, schema, installation, process, protocol, approval, receipt,
  resource, timeout, cleanup, lifecycle, R0, and R2 closure;
- exact zero-command/zero-mutation baseline enforcement rather than a
  prompt-only approval claim;
- no private path or transcript in durable evidence;
- no fallback or retry route;
- exact four-path later implementation scope; and
- all authority and readiness fields remain false.

Contract acceptance makes a later Codex C implementation decision eligible
only after a fresh owner decision and WIP reconciliation. It does not make
package acquisition, installation, R0 execution, or R2 characterization
eligible by itself.

## Protected Boundaries And Non-Claims

This contract does not authorize:

- implementing or testing the adapter;
- acquiring, downloading, copying, installing, generating, or starting Codex
  or its protocol schema;
- reading or provisioning credentials;
- creating a process, Job, thread, turn, interrupt, task, claim, worktree,
  registry, release record, installation receipt, consumption record, or
  platform receipt;
- installing or synchronizing the Role Pool;
- dispatching any lane or running R0-R8 evidence;
- running a broker, service, SDK, generic subagent, shell, `codex exec`, or
  fallback;
- accessing candidate packages, private evidence, parser data, workbook data,
  or deployment state;
- submitting, merging, deploying, advancing Stage 4, or changing a tracker;
- claiming correctness, reliability, security, privacy, assurance,
  `trusted_owner_native_profile_ready`, or live readiness.

Current, future-without-separate-owner, and terminal authority counts are
`0/0/0`. All operational authority booleans remain false.

## Current Review Handoff

The historical Windows-first handoff embedded in the profile is superseded for
this issue only. The sole current next role is one fresh independent Codex E
review of both final contract artifacts.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Windows App Server Baseline Contract Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/758

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Review exactly:
- docs/contracts/trusted_owner_native_role_pool_profile.md
- docs/contracts/role_pool_codex_app_server_native_task_adapter.md

Use the exact final SHA-256 values from the Codex B handoff. Refresh
origin/main, issue and tracker state, ADR-0008/WIP authority, open PRs, and all
#757 predecessor artifacts before review.

Independently verify:
- the profile amendment admits only one dedicated, pinned, direct non-shell
  App Server process realization behind codex:native-task-create/v1;
- trusted_owner_native_task_request.v1 and
  trusted_owner_native_task_receipt.v1 remain sufficient and unchanged;
- every App Server execution binding is mechanically derived from accepted
  request, lane, worktree, registry, release, skill, predecessor, and
  companion bindings;
- Codex 0.146.0 tag, commit, selected Windows asset name, byte count, SHA-256,
  exact command, source-tag protocol schema byte count and SHA-256, unsigned
  tag status, and installation custody are exact;
- one-use consumption, process, initialize/initialized, thread, turn,
  interrupt, approval, receipt, timeout, bounded-stream, cleanup, and unknown
  behavior are closed;
- exact cwd, model, effort, sandbox, approval, role, predecessor, instruction,
  skill, output-schema, and instructionSources bindings are complete;
- no remote control, plugin, hook, MCP, ambient conversation, resume, fork,
  steer, injection, second turn, replacement, SDK, generic subagent, shell,
  codex exec, broker, alternate executable, retry, or fallback is reachable;
- the complete aggregate schema is exactly 590325 bytes, contains every
  contracted wire type, and has the bound SHA-256;
- the exact 780-byte config disables the shell and named effectful tools;
- the candidate accepts only B/E inspect-only lanes with empty command,
  validation-command, mutation, and artifact arrays;
- every command or file-change request is denied, every related item or
  notification is `AS-POL-001`, and `AS-ACC-001` requires both approval counts
  and every observed effect count to be zero;
- the six pinned source files mechanically support the disabled-shell and
  deny-all-file-change boundary;
- public receipts contain no raw transcript, errors, paths, credentials, IDs,
  or private values;
- R0 remains fake-transport only and R2 real characterization requires a
  separate exact owner decision and establishes no command or mutation
  authority;
- the canonical 39-tuple lifecycle registry is 5614 bytes with the exact bound
  digest, per-outcome counts, selector, and zero/zero/zero audit;
- the existing scheduling, capacity, isolation, Safe/Automatic, F, release,
  20-outcome, and R0-R8 rules remain unchanged; and
- the later implementation envelope is exactly four paths.

Recompute both contract hashes, all fixed byte counts and digests, strict
structured blocks, source-control bindings, and the lifecycle registry and
selector. Run git diff --check,
check_agent_docs.py, check_protected_surfaces.py, check_secret_patterns.py,
and changed-path validation. Confirm no executable was acquired or started,
no schema generated, no credentials accessed, no task created, no Role Pool
installed, and no generated residue remains.

Lead with findings. If accepted, report only contract acceptance and
eligibility for a separate owner Codex C implementation decision. Grant no
implementation, package, installation, process, task, R0-R8, Stage 4, or
readiness authority.
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
    - "ADR-0005"
    - "ADR-0008"
  protected_surfaces:
    - "native task launch authority"
    - "Core-owned process creation"
    - "credential and private path custody"
    - "repository command and mutation enforcement"
    - "Role Pool release ladder"
  authority_conflicts_found: false
  authority_conflict_notes: "PRs #374 and #391 remain open; the owner supplied the task-scoped explicit_user_override recorded above."
  stop_conditions:
    - "public binding or source-tag drift"
    - "need to version the public task request without a new B decision"
    - "need to acquire, install, start, or characterize Codex"
    - "need to access a credential or private runtime value"
    - "request to implement or activate the adapter"
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Consolidated Windows App Server Baseline Contract Reviser"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/758"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  source_artifacts:
    - "docs/contracts/trusted_owner_native_role_pool_profile.md"
    - "docs/contracts/role_pool_codex_app_server_native_task_adapter.md"
  contract_status: "review_pending"
  codex_a_verdict: "feasible_with_narrow_profile_amendment"
  capability_verdict: "insufficient_evidence"
  public_task_request_schema: "trusted_owner_native_task_request.v1_unchanged"
  public_task_receipt_schema: "trusted_owner_native_task_receipt.v1_unchanged"
  candidate_identity: "codex:app-server-stdio-direct/v1"
  public_capability_identity: "codex:native-task-create/v1"
  selected_release: "Codex 0.146.0"
  selected_asset_sha256: "bc343ba420dc2e2e9f59e6fc5e5bf0aae1cd8c771fc319665241fc9c0271fddb"
  generated_protocol_schema_sha256: "08cc0c836bf0caca1e65b92956c3d57fd59c6be9b66277f77afe1cf65aefa592"
  effect_surface: "inspect_only_zero_command_zero_mutation"
  lifecycle_registry_sha256: "0d50774b0b8cb4f47a11b2cde2919f73ac887dacced761dfa4ebd7ea95e4f517"
  process_topology: "one_process_per_lane"
  r0_boundary: "fake_transport_only"
  r2_boundary: "separate_owner_inspect_only_real_characterization_required"
  files_changed: 2
  executable_acquired_or_started: false
  schema_generated: false
  credentials_accessed: false
  task_created: false
  implementation_authorized: false
  installation_authorized: false
  registry_or_release_authorized: false
  dispatch_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: independent Windows App Server baseline contract reviewer"
```
