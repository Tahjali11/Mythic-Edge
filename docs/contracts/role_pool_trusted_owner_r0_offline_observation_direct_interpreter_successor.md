# Role Pool R0 Offline Observation Direct-Interpreter Successor Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: `https://github.com/Tahjali11/Mythic-Edge/issues/780`.
- Parent: `https://github.com/Tahjali11/Mythic-Edge/issues/776`.
- Tracker: `https://github.com/Tahjali11/Mythic-Edge/issues/746`.
- Protected coordination surface:
  `https://github.com/Tahjali11/Mythic-Edge/issues/769`.
- Role: Codex B, direct-interpreter successor contract writer.
- Base: `origin/main@dcd7f4a276ba87e30de0dbd2b07ed21a06a39b2a`.
- Branch: `codex/role-pool-r0-direct-interpreter-successor-780`.
- Risk tier: `high`.
- Source finding: `ME-RP-776-A-001`.

This contract follows `AGENTS.md`, `docs/agent_rules.yml`,
`docs/agent_constitution.md`, `docs/codex_module_workflow.md`,
`docs/agent_threads/module_contract.md`,
`docs/templates/module_contract.md`, and accepted ADR-0008.

The current owner instruction is a task-scoped ADR-0008
`explicit_user_override` for this one docs-only Codex B artifact. The active
lane is issue #780; open PRs #374 and #391 remain unrelated. The override is
recorded here, expires at this B handoff, and transfers no implementation,
process, observation, publication, release, submission, merge, deployment,
Stage-4, or readiness authority.

## Findings

1. **Observed:** the spent observation-1 harness process exited `0`, emitted
   zero stderr bytes, and emitted stdout with SHA-256
   `36454313391b747c05cb95891e88e0bae1f0936aaa5917ad83dd7b9af2aecfa2`,
   exactly the expected observation-1 receipt artifact.
2. **Observed:** the outer observer counted one descendant and selected
   `observation_safety_boundary_failed`. No receipt was published, no process
   survived, no temporary residue remained, and observation 2 was not
   executed or made eligible by an accepted observation-1 receipt.
3. **Observed:** the retained public evidence does not identify the
   descendant executable, parent edge, or exact top-level executable used by
   the spent attempt. The cause remains `unknown`; this contract does not
   reconstruct it or claim that `py.exe` caused it.
4. **Observed:** metadata-only inspection found the selected CPython console
   executable as an ordinary, non-reparse file. Two independent handle reads
   produced one stable identity digest. Its absolute path was neither emitted
   nor persisted, and the executable was not run.
5. **Derived:** the observation algorithm is not the first proven failure. It
   completed byte-exactly. The smallest current correction is an exact outer
   launcher binding plus mechanically dependent fresh identities and KATs.
6. **Decision:** one exact CPython 3.13.14 `python.exe` is the only admissible
   top-level process. Launcher discovery, wrappers, aliases, shells, alternate
   interpreters, fallback, acquisition, and installation are prohibited.
7. **Stop condition checked:** current public evidence does not prove that the
   spent attempt already used the exact binding below. If such retained
   evidence becomes available before acceptance or implementation, stop with
   `direct_interpreter_hypothesis_rejected`; do not implement this contract.

Finding `ME-RP-776-A-001` is
`contracted_direct_interpreter_successor_review_pending`.

## Module And Truth Ownership

Module: Windows-hosted R0 offline observation launcher binding and fresh
single-use sequence.

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership remains unchanged:

- issue #780 and immutable issue #776 comments own public historical facts;
- the accepted sequence and receipt-order contracts own the observation
  algorithm, canonical receipt model, chronology, consumption, publication,
  and no-retry lifecycle;
- the public binding object below owns the selected executable metadata;
- a private local absolute path is an executor input only and owns no public
  truth;
- the outer Windows process observer owns top-level and descendant facts; and
- the existing two-file harness owns deterministic in-process validation and
  public-safe projection.

No parser, release-state, registry, Role Pool skill, installed copy, managed
validator, or issue #769 truth moves into this contract.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Base commit | `dcd7f4a276ba87e30de0dbd2b07ed21a06a39b2a` |
| Issue #780 body | 9,754 UTF-8 bytes; SHA-256 `5186379f8c9ca597d7f0f3a0f6dbde9aac196d90b29f7d6ed9101f7a311e69aa`; zero comments |
| Accepted sequence contract | `docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md`; SHA-256 `df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8` |
| Accepted receipt-order successor | `docs/contracts/role_pool_trusted_owner_r0_offline_observation_receipt_order_reconciliation_successor.md`; SHA-256 `8cbd996f729d77eff3bd954fd054aa2012926e1d9c06f7e43e7e7d0a08a939a7` |
| Receipt-order contract review | SHA-256 `9a54ffd8de7ace8092316de7637f76db2de2d8ede6e0163b8c33d22e68930ff2` |
| Receipt-order implementation review | SHA-256 `09c0cf2894ad031399273185bb58e96c557f49ef1c38077cbc8e863c8e5feb2d` |
| Current harness | `tools/check_role_pool_r0_offline_observation.py`; 48,623 bytes; SHA-256 `ae129735b434c35fb27a0fb636f5a0536856a6ff315d06b510bc4b0858636ac0` |
| Current focused test | `tests/test_check_role_pool_r0_offline_observation.py`; 37,227 bytes; SHA-256 `62271153c7eecb1311dd533113dec4a72cc7bd7fe8acdeb622253d4e3fb2f7e0` |
| R0 profile contract | SHA-256 `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| Release artifact / record | `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9` / `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| Source / installed trees | exact equality at `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Registry artifact / self-digest | `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` / `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Validator bundle | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| R0 checker / tests | `34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914` / `976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34` |
| Release validator / authority index | `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` / `2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0` |
| Protected issue #769 | open with zero top-level comments |

Any drift stops before implementation or process authority.

## Spent Sequence Retirement

The following public objects are immutable historical lineage:

- owner decision:
  `https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-5147585057`,
  created and last updated `2026-07-31T21:22:58Z`, 6,378 bytes, SHA-256
  `38de4193fc0146dc068adf3e0d7304d66077d435b6a70cace144522ff0a4359b`;
- sequence: `r0.offline.sequence.2.45c8f6d057ddc04aa60650b0c09090f0`;
- observation 1:
  `r0.offline.observation.1.v2.f6b5effa4a357e784cbbf1dd39efff2c`;
- observation 2:
  `r0.offline.observation.2.v2.7b491e38edb350b7a9b6864c1d60cb39`;
- observation-1 consumption comment:
  `https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-5147599535`,
  created and last updated `2026-07-31T21:24:58Z`, self-digest
  `3c3537c680b9d413b10d32f9444d5667a1348f54afe39ade24912154ce2949c3`,
  2,865 bytes, artifact SHA-256
  `8e947fbf97e515bb69688aacdb71835a9164154e69cb5d653c1f865f1476da51`;
- observation-1 expected receipt self/artifact digests:
  `ecfcaf5a007f1734511615536d94add079014a83113f3b4ca4df36974af383e9` /
  `36454313391b747c05cb95891e88e0bae1f0936aaa5917ad83dd7b9af2aecfa2`;
  and
- observation-2 expected receipt self/artifact digests:
  `23b9a29596f4e73378da60cdc5827465f8fd1f317b59987b77ecbf586be6d64e` /
  `41e5b7ce534abace41658a6bd307d950dd2edcb30f668232040baef8759ef3e8`.

The sequence and owner decision are `spent_terminal_nonreusable`.
Observation 1 is `consumed_execution_failed_nonreusable`. Observation 2 and
both old receipt identities are `retired_with_sequence_nonreusable` even
though observation 2 never executed and its conditional launch authority
never matured. Nothing above may be retried, resumed, replaced in place,
edited, deleted, or treated as accepted evidence. Accepted observation count
remains zero.

## Direct CPython Binding

The closed 18-field object below uses insertion order as shown, UTF-8 without
BOM, compact JSON, and one final LF. Unknown, duplicate, reordered, missing,
or mistyped fields fail closed. `binding_sha256` is SHA-256 over the same
object with that field omitted.

```json
{"schema_version":"trusted_owner_r0_direct_cpython_binding.v1","repository_id":1235264383,"issue_number":780,"host_os_name":"nt","host_sys_platform":"win32","runtime_implementation":"CPython","executable_basename":"python.exe","file_version":"3.13.14","product_version":"3.13.14","byte_length":105696,"file_sha256":"ef8f51028ac5329641985112f8efb1c2d4c47c86b8011ddf7e6fae21e2b4e5a1","stable_identity_schema":"trusted_owner_direct_cpython_file_identity.v1","stable_identity_sha256":"570754cbc03fb52f4e846c3611e48e18334f08e621babfa2e8eb76f4a0e5c953","ordinary_file":true,"reparse_point":false,"private_path_source":"owner_supplied_local_absolute_path","private_path_publication_authorized":false,"binding_sha256":"2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"}
```

- field count: `18`;
- self-digest preimage: `694` bytes;
- complete object: `778` bytes;
- self-digest:
  `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333`;
- artifact SHA-256:
  `235e21a04acb454adb5471f2136b53547c35a279a63b8e09d8c6a10926d3bb9b`.

The private path is supplied locally by the owner or separately authorized
executor. It is never accepted from a receipt, issue field, environment
variable, PATH lookup, registry search, current directory, command alias, or
caller-selected fallback. It must be an absolute path whose final component
is exactly `python.exe` and whose opened object reproduces every public field
above.

Codex B selects that exact 3.13.14 object as the sole candidate. No `latest`,
launcher-default, registry-priority, or compatibility-fallback rule survives
into execution; every other interpreter is an exact mismatch.

Stable identity is derived from one ordinary file handle opened with read-
attributes access, `FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE`,
`OPEN_EXISTING`, and `FILE_FLAG_OPEN_REPARSE_POINT`. The private raw
`dwVolumeSerialNumber` and 64-bit file index form this exact ASCII preimage:

```text
trusted_owner_direct_cpython_file_identity.v1|volume_serial_number=<8 lowercase hex>|file_index=<16 lowercase hex>
```

Only its SHA-256 may leave bounded memory. The raw identity, volume value,
file index, handle, and absolute/final path are forbidden durable output.
Two separately opened handles must reproduce the exact identity digest, file
length, version fields, SHA-256, ordinary-file state, and non-reparse state.
Any mismatch or inability to read one field is `observation_binding_rejected`.

The runtime must reject before consumption: `py.exe`, WindowsApps aliases,
App Execution Aliases, PATH or `SearchPathW` resolution, shims, wrappers,
shells, script hosts, batch files, PowerShell, `cmd.exe`, `codex exec`, SDK or
broker launch, alternate Python files, virtual-environment launchers,
replacement interpreters, fallback runtimes, downloads, package acquisition,
installation, or repair of the selected executable.

## Fresh Deterministic Identities

No search, nonce, random value, timestamp, alternate preimage, retry, or
digest-order grinding is permitted. Take the first 32 lowercase hexadecimal
characters of SHA-256 over each exact ASCII preimage:

```text
trusted_owner_r0_offline_direct_interpreter_sequence.v1|1235264383|776|780|78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7|r0.offline.sequence.2.45c8f6d057ddc04aa60650b0c09090f0|3c3537c680b9d413b10d32f9444d5667a1348f54afe39ade24912154ce2949c3|2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333
trusted_owner_r0_offline_direct_interpreter_observation.v1|1235264383|776|780|r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa|1
trusted_owner_r0_offline_direct_interpreter_observation.v1|1235264383|776|780|r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa|2
```

The only fresh identities are:

- sequence: `r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa`;
- observation 1:
  `r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461`;
- observation 2:
  `r0.offline.observation.2.v3.7269e523cea1b426a7ecedb3ef6e7fb1`.

They are contract-reserved and cannot be replaced by another derivation. A
failed or unknown real synthetic preflight retires all three without reuse.
After an owner observation decision, entry into either consumption POST spends
that observation identity exactly as the accepted predecessor requires.

## Observation Profile V2

The receipt schema remains v1. Its existing
`observation_profile_sha256` field now binds this closed 29-field profile,
which adds only the direct-interpreter binding and launcher mode. All other
bindings and limits remain exact.

```json
{"schema_version":"trusted_owner_r0_offline_observation_profile.v2","repository_id":1235264383,"issue_number":776,"current_rung":"R0","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","r0_checker_sha256":"34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914","r0_checker_test_sha256":"976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34","release_validator_sha256":"af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d","authority_index_sha256":"2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0","implementation_paths":["tools/check_role_pool_r0_offline_observation.py","tests/test_check_role_pool_r0_offline_observation.py"],"direct_interpreter_binding_sha256":"2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333","launcher_mode":"exact_direct_absolute_cpython_no_shell","host_os_name":"nt","host_sys_platform":"win32","top_level_process_limit":1,"descendant_process_limit":0,"process_launch_attempt_limit":0,"network_operation_limit":0,"external_effect_limit":0,"observation_count":2,"timeout_seconds":120,"retry_limit":0}
```

The profile is `1,776` bytes including its final LF and has SHA-256
`ce57f4e4b337056bcf301177c404578dfbcfa52ac1382fa755fad4074ff7b668`.

## Fresh Receipt Known Answers

The accepted 37-field
`trusted_owner_r0_offline_observation_receipt.v1` schema, field order, types,
authority flags, canonicalization, and self-digest rule remain unchanged.

### Observation 1

```json
{"schema_version":"trusted_owner_r0_offline_observation_receipt.v1","sequence_id":"r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa","observation_id":"r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461","sequence_position":1,"predecessor_observation_id":null,"repository_id":1235264383,"issue_number":776,"current_rung":"R0","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","observation_profile_sha256":"ce57f4e4b337056bcf301177c404578dfbcfa52ac1382fa755fad4074ff7b668","host_os_name":"nt","host_sys_platform":"win32","validation_status":"accepted_exact_r0_offline_observation","release_state_status":"present_valid_chain","bootstrap_checker_terminal_status":"blocked_release_state_conflict_expected","derived_current_rung":"R0","process_topology":"single_top_level_process_zero_descendants","top_level_process_count":1,"descendant_process_count":0,"process_launch_attempt_count":0,"network_operation_count":0,"repository_write_count":0,"installed_write_count":0,"external_effect_count":0,"retry_count":0,"unknown_outcome_count":0,"cleanup_status":"no_attempt_owned_artifacts","accepted_for_independent_review":true,"authority_flags":{"repository_mutation_authorized":false,"implementation_authorized":false,"publication_authorized":false,"merge_authorized":false,"deployment_authorized":false,"installation_authorized":false,"package_operations_authorized":false,"network_authorized":false,"secrets_authorized":false,"external_isolation_authorized":false,"canary_authorized":false,"stage4_authorized":false,"stage_advancement_authorized":false,"dispatch_authorized":false,"live_ready":false,"trusted_owner_native_profile_ready":false},"receipt_sha256":"46b1c205529a9a39476a2d50255e7dadbd2866949a0dd81f6558505f0f51ccce"}
```

- preimage / complete bytes: `2,338 / 2,422`;
- self-digest:
  `46b1c205529a9a39476a2d50255e7dadbd2866949a0dd81f6558505f0f51ccce`;
- artifact SHA-256:
  `b79ef2b59e2e9e34ef8fcebf1dcc95e44ea53cc09efb97bdeb78bced11e78e7e`.

### Observation 2

```json
{"schema_version":"trusted_owner_r0_offline_observation_receipt.v1","sequence_id":"r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa","observation_id":"r0.offline.observation.2.v3.7269e523cea1b426a7ecedb3ef6e7fb1","sequence_position":2,"predecessor_observation_id":"r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461","repository_id":1235264383,"issue_number":776,"current_rung":"R0","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","observation_profile_sha256":"ce57f4e4b337056bcf301177c404578dfbcfa52ac1382fa755fad4074ff7b668","host_os_name":"nt","host_sys_platform":"win32","validation_status":"accepted_exact_r0_offline_observation","release_state_status":"present_valid_chain","bootstrap_checker_terminal_status":"blocked_release_state_conflict_expected","derived_current_rung":"R0","process_topology":"single_top_level_process_zero_descendants","top_level_process_count":1,"descendant_process_count":0,"process_launch_attempt_count":0,"network_operation_count":0,"repository_write_count":0,"installed_write_count":0,"external_effect_count":0,"retry_count":0,"unknown_outcome_count":0,"cleanup_status":"no_attempt_owned_artifacts","accepted_for_independent_review":true,"authority_flags":{"repository_mutation_authorized":false,"implementation_authorized":false,"publication_authorized":false,"merge_authorized":false,"deployment_authorized":false,"installation_authorized":false,"package_operations_authorized":false,"network_authorized":false,"secrets_authorized":false,"external_isolation_authorized":false,"canary_authorized":false,"stage4_authorized":false,"stage_advancement_authorized":false,"dispatch_authorized":false,"live_ready":false,"trusted_owner_native_profile_ready":false},"receipt_sha256":"d62ee96557ed05d64c192e027ca7b43ab918401034369f683b73e3ca388c4c52"}
```

- preimage / complete bytes: `2,396 / 2,480`;
- self-digest:
  `d62ee96557ed05d64c192e027ca7b43ab918401034369f683b73e3ca388c4c52`;
- artifact SHA-256:
  `9481cebbb6dbf1a21c42d4670b07f44fae7ed47ac40f9f6dbb58186c62adb252`.

The chronological digest tuple is `(46b1...ccce, d62e...4c52)` and is also
lexically ascending. This is an incidental result of the single fixed
derivation, not an acceptance rule or permission to search. The accepted
receipt-order successor still owns chronology through exact position,
identity, predecessor, and expected tuple equality.

## Fresh Consumption Known Answer

The 36-field consumption schema and lifecycle remain unchanged. Only the
fresh identities, issue-780 review references, profile digest, and expected
receipt digest change mechanically.

```json
{"schema_version":"trusted_owner_r0_offline_observation_consumption.v1","sequence_id":"r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa","observation_id":"r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461","sequence_position":1,"predecessor_consumption_sha256":null,"repository_id":1235264383,"issue_number":776,"owner_decision_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-owner","owner_decision_sha256":"1111111111111111111111111111111111111111111111111111111111111111","owner_decision_created_at_utc":"2026-08-01T00:00:00Z","owner_decision_expires_at_utc":"2026-08-01T12:00:00Z","sequence_contract_sha256":"2222222222222222222222222222222222222222222222222222222222222222","sequence_contract_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/780#issuecomment-kat-contract-review","sequence_contract_review_sha256":"3333333333333333333333333333333333333333333333333333333333333333","harness_sha256":"4444444444444444444444444444444444444444444444444444444444444444","harness_test_sha256":"5555555555555555555555555555555555555555555555555555555555555555","implementation_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/780#issuecomment-kat-implementation-review","implementation_review_sha256":"6666666666666666666666666666666666666666666666666666666666666666","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","observation_profile_sha256":"ce57f4e4b337056bcf301177c404578dfbcfa52ac1382fa755fad4074ff7b668","expected_receipt_sha256":"46b1c205529a9a39476a2d50255e7dadbd2866949a0dd81f6558505f0f51ccce","decision":"consume_one_r0_offline_observation_identity","transition":"approved_unconsumed_to_consumed_exact_nonreusable","attempt_limit":1,"retry_authorized":false,"reuse_authorized":false,"launch_authorized_after_exact_readback":true,"status":"consumed_exact_nonreusable","consumption_sha256":"b49572e1faad02c68270c0832dc86158da3b24d2eff5772669521a7e53955efa"}
```

- preimage / complete bytes: `2,531 / 2,619`;
- self-digest:
  `b49572e1faad02c68270c0832dc86158da3b24d2eff5772669521a7e53955efa`;
- artifact SHA-256:
  `d3e1f80d0c755c65c8c9cb905275cff09ca92c38f2bb662ddcd553de08d1e360`.

This is a KAT, not authority. A real object must bind the accepted integrated
successor, exact review and implementation bytes, fresh owner decision, and
immutable GitHub metadata.

## Exact Direct Launch Boundary

The future executor receives the private path out of band and performs this
fixed order:

1. Recompute every public binding and prove current public evidence still
   does not identify the spent attempt as this exact interpreter.
2. Validate the private path twice against the exact binding object using
   separate handles. Do not consume an observation identity.
3. Require one accepted synthetic-preflight result for this exact binding and
   exact implementation package when the future owner decision includes that
   bounded authority.
4. Revalidate the same file immediately before the consumption POST.
5. Perform the accepted single no-retry consumption transition.
6. Reopen and revalidate the same file after exact consumption readback and
   immediately before launch. Drift now spends the identity and selects
   `observation_launch_unknown`; it cannot return to preflight.
7. Invoke Windows process creation with the private path as the explicit
   application, not as a search token. The exact observation argument vector
   is `[<private exact python.exe>, "-B",
   "tools/check_role_pool_r0_offline_observation.py", <exact observation ID>]`.
8. Use repository-root cwd, `shell=false`, closed stdin, bounded stdout and
   stderr, the accepted environment and bytecode boundary, and the existing
   120-second timeout.
9. Bind the returned process handle to the same executable identity. Count
   that interpreter as the single top-level process and observe its complete
   descendant tree by stable process identity, not PID alone.
10. Apply the accepted harness classification, cleanup, receipt sealing,
    issue-776 publication, and readback lifecycle unchanged.

The direct executable is not a descendant of an admitted launcher. It is the
one admitted top-level harness process. Any process whose parent chain reaches
that process during its lifetime is a descendant and is terminal. The
observer, Codex host, and controlling thread are outside the launched process
tree and cannot be counted as substitutes for the one direct process.

## Bounded Synthetic Preflight

This contract does not execute a preflight. A later exact Codex C owner
decision may authorize at most one preflight after the two-file implementation
and before independent implementation review. It launches only:

```text
[<private exact python.exe>, "-B", "-c", "pass"]
```

The preflight uses the same explicit-application, cwd, closed-stdin,
no-search, no-shell, environment, process-observer, identity-readback, and
cleanup rules. Limits are one execution, one top-level process, zero
descendants, zero output bytes on success, zero network, zero writes, zero
external effects, a 30-second timeout, no retry, and no replacement runtime.
It publishes no GitHub comment or observation receipt.

Closed outcomes are:

- `direct_interpreter_preflight_passed`;
- `direct_interpreter_preflight_descendant_observed`;
- `direct_interpreter_preflight_unknown`;
- `direct_interpreter_preflight_required`;
- `direct_interpreter_hypothesis_rejected`; and
- `observation_binding_rejected`.

Only `direct_interpreter_preflight_passed` may support later observation-
decision eligibility. A descendant, timeout, missing exit state, uncertain
cleanup, output, mutation, process-observer ambiguity, or identity drift is
terminal, retires the contract-bound v3 identities, and routes to fresh Codex
A or B. It must never increase the descendant limit.

The finite preflight selector uses booleans
`historical_direct_use_proven`, `public_bindings_exact`, and
`private_binding_exact`, plus state
`{not_run, passed, descendant, unknown}`. First-failure precedence is:

1. proven historical direct use -> `direct_interpreter_hypothesis_rejected`;
2. public or private binding failure -> `observation_binding_rejected`;
3. `not_run` -> `direct_interpreter_preflight_required`;
4. `descendant` -> `direct_interpreter_preflight_descendant_observed`;
5. `unknown` -> `direct_interpreter_preflight_unknown`; and
6. `passed` -> `direct_interpreter_preflight_passed`.

Across all 32 tuples the outcome cardinalities are `16/12/1/1/1/1`, with
`overlap_count=0`, `uncovered_count=0`, and
`unreachable_outcome_count=0`.

## Preserved Observation Lifecycle

The accepted 15-tuple consumption selector, 18-row observation lifecycle,
receipt publication, reconciliation, timeout, output, no-echo, cleanup, and
terminal nonreuse rules remain authoritative. This successor inserts only:

- exact direct binding before consumption;
- exact identity revalidation after consumption and before launch; and
- the direct process as the single top-level process.

Existing statuses apply after consumption:

- binding or process identity uncertainty before launch selects
  `observation_launch_unknown`;
- any descendant selects `observation_safety_boundary_failed`;
- timeout or cleanup uncertainty selects `observation_timeout_unknown`;
- noncanonical or incomplete output selects `observation_result_unknown` or
  `observation_validation_failed` according to the accepted precedence; and
- only exact issue-776 receipt publication and readback selects
  `accepted_exact_r0_offline_observation`.

Observation 2 remains unavailable until observation 1 has an exact immutable
accepted receipt. No failure creates retry, relaunch, replacement-identity,
or fallback authority.

## Exact Later Codex C Scope

After independent contract acceptance and a separate owner implementation
decision, Codex C may modify exactly:

1. `tools/check_role_pool_r0_offline_observation.py`; and
2. `tests/test_check_role_pool_r0_offline_observation.py`.

The implementation is limited to:

- binding this accepted successor and review;
- adding the exact public interpreter binding and profile-v2 KAT;
- replacing v2 sequence, observation, receipt, and consumption constants with
  the exact v3 values above;
- adding in-process no-echo validation of the running `sys.executable`
  metadata and stable identity through Windows APIs without a helper process;
- preserving the accepted observation algorithm and receipt-pair validator;
  and
- adding focused fake-launcher, metadata, preflight-selector, direct-process,
  rejection, timeout, cleanup, and KAT tests.

No third durable file, persistent launcher, profile, release state, registry,
authority index, Role Pool source/install file, managed validator, schema,
package, configuration, or issue comment may change. If the exact direct
binding cannot be enforced within these two paths and the separately
authorized executor, C stops and returns to B.

## Required Validation

Codex C and independent Codex E must prove:

1. exact starting hashes and all public/private binding projections;
2. all five canonical JSON blocks above parse with exact field order, type,
   byte count, self-digest, and artifact digest;
3. the single fixed identity derivation reproduces the three v3 IDs without
   search;
4. both exact chronological receipts pass; reversed, duplicate, missing,
   substituted, wrong-position, wrong-predecessor, wrong-profile, and old-v2
   receipts fail;
5. `py.exe`, aliases, PATH lookup, wrappers, shells, shims, alternate
   interpreters, reparse files, wrong versions, wrong lengths, wrong hashes,
   wrong identities, and unstable readbacks fail before consumption;
6. the 32-tuple preflight selector is `0/0/0` and every outcome is reachable;
7. fake direct launch admits exactly one top-level process and zero
   descendants; one descendant, unknown parentage, timeout, output overflow,
   identity drift, or cleanup uncertainty fails closed;
8. the future real synthetic preflight, if explicitly authorized, uses the
   one fixed command, runs once, and does not execute an observation;
9. all existing observation, consumption, publication, no-echo, authority,
   and cleanup tests remain green;
10. issue #769 remains open with zero comments, issue #780 remains unchanged,
    and generated residue and matching process counts are zero.

Required contract-review commands are:

```powershell
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
py -B -m pytest tests\test_check_role_pool_r0_offline_observation.py -q
py -B -m pytest tests\test_check_role_pool_r0_bootstrap.py -q
py -B -m pytest docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py -q -k release
```

These are contract or synthetic validation only. They are not either R0
observation and grant no process or publication authority.

## Acceptance Criteria

Independent Codex E may accept only if:

1. all current, historical, executable, protected-surface, and KAT bindings
   are exact;
2. the historical sequence and every old identity are sealed and nonreusable;
3. current retained evidence does not prove prior use of this exact direct
   interpreter;
4. the direct binding is exact without a public path or raw file identity;
5. every prohibited launcher and fallback is rejected before consumption;
6. the interpreter is the one top-level process and descendant limit remains
   zero;
7. the v3 identities are the first and only fixed derivation;
8. the existing harness algorithm, receipt model, ordering, consumption,
   publication, validator bindings, and zero-effect boundary remain intact;
9. the exact two-file implementation envelope is sufficient;
10. no implementation, process, observation, receipt, release mutation,
    submission, merge, deployment, R1-R8, Stage-4, or readiness authority was
    created; and
11. only this contract changed and generated residue is zero.

Contract acceptance makes only a separate owner Codex C implementation
decision eligible. A successful synthetic preflight and independent exact-byte
implementation review are still required before a fresh owner observation
decision.

## Privacy And Non-Claims

Durable output may contain only contract-defined categorical statuses,
counts, public repository references, version, byte length, and SHA-256
values. It must never contain the private executable path, final path, raw
file identity, volume data, file index, handle, PID, account identity,
environment value, command line, raw stdout/stderr, exception, stack trace, or
private diagnostics.

Current, post-contract, post-review, and terminal authority remains false for
implementation, synthetic preflight, observation consumption, observation
execution, receipt publication, registry/release/index mutation,
installation, synchronization, process/task/claim/command/dispatch, App
Server, canary, package operations, R1-R8, Stage 4, submission, merge,
deployment, live readiness, compatibility, reliability, correctness,
security, privacy, or assurance.

This contract does not claim that the direct interpreter caused or fixes the
historical descendant, that a preflight ran, that either v3 observation ran or
passed, or that R1 is eligible.

## Next Workflow Action

Next role: fresh independent Codex E contract reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Independent R0 Direct-Interpreter Successor Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected coordination surface: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md

Recompute the artifact SHA-256 and independently verify every current and
historical binding, the spent/nonreusable v2 disposition, the 18-field direct
CPython binding, the private file-identity digest algorithm without emitting
raw identity or path values, the 29-field profile, all three v3 identity
preimages, both receipt KATs, the consumption KAT, and the 32-tuple preflight
selector.

Confirm current retained evidence does not prove that the spent attempt used
the exact direct interpreter. Confirm py.exe, aliases, PATH discovery, shims,
wrappers, shells, fallbacks, alternate interpreters, reparse files, drift,
and unstable identities fail before consumption. Confirm the direct
interpreter remains the single top-level process with zero descendants and
that any real synthetic preflight requires separate owner authority.

Confirm the exact future implementation scope is only the existing harness
and focused test, the validated observation algorithm and receipt model are
unchanged, issue #769 remains open with zero comments, and every operational
authority flag remains false.

Run the contract-defined docs, canonical, safety, focused observation,
bootstrap, release-focused, process, and residue checks. Do not implement,
launch the interpreter, execute a synthetic preflight or observation, publish
a receipt, mutate GitHub or release state, submit, merge, deploy, authorize
R1-R8 or Stage 4, or claim readiness.

Return findings first, reviewed SHA-256, ME-RP-776-A-001 disposition,
historical retirement verdict, interpreter/profile/KAT validation, selector
audit, exact future file scope, authority flags, residue count, contract
verdict, and a compact workflow_handoff.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
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
    - "immutable issue #776 consumption and observation lineage"
    - "R0 observation identities, receipts, and zero-descendant boundary"
    - "private direct-interpreter path and raw file identity"
    - "R0 release, registry, validator, source/install, and authority bindings"
    - "issue #769 zero-comment boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "The current user instruction is a one-contract explicit_user_override; it grants no implementation or process authority."
  stop_conditions:
    - "binding, historical-state, or issue drift"
    - "retained proof that the spent attempt used the exact direct interpreter"
    - "scope beyond the one contract or two later implementation paths"
    - "need to execute a process, observation, publication, or protected mutation"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  role_performed: "Codex B: R0 Direct-Interpreter Successor Contract Writer"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md"
  contract_artifact: "docs/contracts/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/role-pool-r0-direct-interpreter-successor-780"
  finding_status:
    ME-RP-776-A-001: "contracted_direct_interpreter_successor_review_pending"
  historical_sequence_status: "spent_terminal_nonreusable"
  historical_observation_1_status: "consumed_execution_failed_nonreusable"
  historical_observation_2_status: "retired_with_sequence_nonreusable"
  accepted_observation_count: 0
  direct_interpreter_binding_sha256: "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
  direct_interpreter_preflight_status: "not_run_not_authorized"
  fresh_sequence_id: "r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa"
  future_implementation_scope: "exact_existing_two_files"
  owner_implementation_decision_eligible: false
  implementation_authorized: false
  synthetic_preflight_authorized: false
  observation_authorized: false
  consumption_authorized: false
  receipt_publication_authorized: false
  release_state_mutation_authorized: false
  r1_authorized: false
  r1_r8_authorized: false
  dispatch_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  generated_residue_count: 0
  validation:
    - "exact direct CPython metadata and stable identity readback; no private path emitted"
    - "one fixed v3 derivation; two receipt KATs and one consumption KAT"
    - "32 preflight tuples; cardinalities 16/12/1/1/1/1; audit 0/0/0"
    - "docs, safety, focused tests, process, and residue checks required"
  stop_conditions:
    - "binding or historical-state drift"
    - "retained proof of prior exact-direct-interpreter use"
    - "direct interpreter synthetic descendant or unknown state"
    - "scope beyond the two existing implementation paths"
    - "issue #769 comment or protected-state mutation"
  next_recommended_role: "Codex E: independent R0 direct-interpreter successor contract reviewer"
```
