# Trusted-Owner R0 Proportionate Offline Observation Successor Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`.
- Observation issue: <https://github.com/Tahjali11/Mythic-Edge/issues/776>.
- Prior preflight issue: <https://github.com/Tahjali11/Mythic-Edge/issues/780>.
- Diagnostic issue: <https://github.com/Tahjali11/Mythic-Edge/issues/795>.
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>.
- Protected coordination surface:
  <https://github.com/Tahjali11/Mythic-Edge/issues/769>.
- Role: Codex B, Module Contract Writer.
- Risk tier: `high`.
- Base: `origin/main@be840bc1160678a9678d792d3cfd6074ac86ebca`.
- Branch: `codex/role-pool-r0-proportionate-observation-successor-776`.
- WIP-1 basis: the current owner instruction is a narrow
  `explicit_user_override` for this docs-only issue-776 contract. It expires
  with this handoff and transfers no implementation or operational authority.

This contract follows [the agent constitution](../agent_constitution.md),
[the Codex B role](../agent_threads/module_contract.md), and
[the module-contract template](../templates/module_contract.md). ADR-0008 is
accepted and controlling for lane activation. ADR-0010 remains Proposed and
non-precedential.

## Findings And Proportionality Decision

1. **Observed:** current `origin/main` is exactly the supplied starting commit.
   Issues #776, #780, #795, and #746 are open; issue #769 is open with zero
   comments. Open PRs #374 and #391 are unrelated to this docs-only override.
2. **Observed:** the retained sequence-2 attempt completed the fixed offline
   validation, exited `0`, emitted the exact expected canonical receipt bytes,
   emitted zero stderr, left no survivor or residue, and first failed only
   because the outer observer counted one descendant.
3. **Observed:** the current 37-field v1 receipt hard-codes zero descendants
   and cannot truthfully represent either one known terminal descendant or a
   survivor count. Reusing it for the owner rescope would be false.
4. **Derived:** one versioned observation protocol is necessary. It reuses the
   existing canonical JSON and SHA-256 rules, statuses, publication lifecycle,
   authority object, and release sequencing. It adds only the process facts
   required to distinguish an allowed transient descendant from an unknown or
   surviving process.
5. **Decision:** exact image identity, private executable-path transport,
   secure ingress, and zero-descendant topology are deferred hardened-profile
   evidence. They are not trusted-owner R0 observation eligibility predicates.
6. **Proportionality test:** deferring those predicates does not invalidate
   fixed validation, canonical receipt production, known termination, zero
   survivors, zero residue, source/install integrity, or the zero-effect
   boundary. Unknown process state, survivors, mutation, external effects,
   malformed output, and stale bindings remain blocking because deferring any
   of them would invalidate those properties.

No later owner decision changing this acceptance policy was found. This
current owner instruction is the controlling issue-scoped rescope.

## Review-Loop Corrections

- `ME-RP-776-PROP-E-001`: corrected. The complete canonical consumption-v2
  object is now present and independently reproduces the accepted predecessor
  one-field transformation, byte counts, self-digest, and artifact digest.
- `ME-RP-776-PROP-E-002`: corrected contract-only. The validation command now
  owns only the existing canonical validation payload. The existing trusted
  launch observer owns the exact typed post-exit facts and invokes one pure
  in-memory sealer in the already-contracted harness module before publication.
  No caller-controlled fact, new file, helper process, or execution lane is
  introduced.

## Module And Truth Ownership

- Project area: Role Pool trusted-owner R0 release validation.
- Bridge status: `shared_support`; no parser, workbook, transport, or analytics
  truth changes.
- The accepted profile, release state, repository registry, current-authority
  index, and owning validators retain their existing truth.
- `tools/check_role_pool_r0_offline_observation.py` owns deterministic offline
  validation and canonical observation construction.
- The trusted launch observer owns process relationship, terminal-state,
  survivor, timeout, cleanup, and executor-owned local-effect facts. These
  facts must come from observation, never a caller-supplied count.
- Issue #776 owns public consumption and observation-receipt publication.
  Issue #769 remains protected and receives no comment.

## Exact Inherited Bindings

| Binding | Exact value |
| --- | --- |
| Trusted-owner profile | `docs/contracts/trusted_owner_native_role_pool_profile.md`; 106,341 bytes; SHA-256 `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| R0 release artifact | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`; 981 bytes; artifact SHA-256 `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9`; record self-digest `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| Source / installed trees | 41 nodes, 36 files, 6,495 manifest bytes each; exact equality at SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Repository registry | `docs/role_pool/trusted_owner_repository_registry.v1.json`; artifact SHA-256 `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`; self-digest `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Validator bundle | SHA-256 `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| R0 checker / test | SHA-256 `34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914` / `976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34` |
| Release validator / authority index | SHA-256 `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` / `2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0` |
| Original sequence contract | SHA-256 `df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8` |
| Receipt-order successor | SHA-256 `8cbd996f729d77eff3bd954fd054aa2012926e1d9c06f7e43e7e7d0a08a939a7` |
| Direct-interpreter successor / review | SHA-256 `17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84` / `0fd7d921a92fbd58576f053a0e8938d3ae4a0266e9a023b762f933e65aee450f` |
| Current observation harness | `tools/check_role_pool_r0_offline_observation.py`; 67,314 bytes; SHA-256 `001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6` |
| Current focused test | `tests/test_check_role_pool_r0_offline_observation.py`; 52,662 bytes; SHA-256 `3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3` |

The current checker remeasurement is `offline_validation_status=passed`,
source/install `identical`, registry `valid_exact`, release
`present_valid_chain`, and terminal `blocked_release_state_conflict`. That
terminal remains the expected post-bootstrap R0 projection; it is not a
failure of this observation.

## Inheritance And Narrow Override

All unaffected requirements of the original sequence and receipt-order
successor remain inherited, including source/install/registry/release and
validator bindings, issue-776-only consumption and publication, canonical
JSON, self-digests, chronological order, single use, no retry, collision and
ambiguous-commit handling, independent review, and separate R1 authority.

This successor overrides only these trusted-owner observation predicates:

- descendant limit `0` becomes `1`;
- exact top-level image identity becomes nullable diagnostic evidence;
- direct private executable-path and secure-ingress success cease to be
  prerequisites; and
- the receipt gains exact relationship, terminal-state, survivor, and
  identity-diagnostic fields.

It does not amend any accepted predecessor bytes or create a hardened-profile
claim. The #780 and #795 artifacts remain historical or deferred evidence.

## Historical Retirement

The following observation sequences and identities are permanently
nonreusable:

| Sequence | Observation 1 | Observation 2 | Disposition |
| --- | --- | --- | --- |
| `r0.offline.sequence.1d11e7476ab400a39d222d0feab38eba` | `r0.offline.observation.1.094221964ddd0af9c3b2034a35347971` | `r0.offline.observation.2.45b674178dd44c9b6723f42e75f3b04f` | terminal consumption/readback failure; entire sequence retired |
| `r0.offline.sequence.2.45c8f6d057ddc04aa60650b0c09090f0` | `r0.offline.observation.1.v2.f6b5effa4a357e784cbbf1dd39efff2c` | `r0.offline.observation.2.v2.7b491e38edb350b7a9b6864c1d60cb39` | observation 1 consumed and executed without accepted receipt; entire sequence retired |
| `r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa` | `r0.offline.observation.1.v3.b40fa2727a0f8006ceb93945cf1b1461` | `r0.offline.observation.2.v3.7269e523cea1b426a7ecedb3ef6e7fb1` | reserved under superseded exact-identity route; retired without reuse |

Every #780 preflight and #795 characterizer or secure-ingress decision,
authority, attempt, and identifier is likewise either consumed or terminally
retired and permanently nonreusable according to its owning evidence. This
contract does not expose private identifiers or reinterpret a historical
outcome as an accepted observation. Accepted observation count remains `0`.

## Fixed Offline Operation

The only operation command is this exact token vector, from repository-root
cwd on Windows:

```text
py -3.13 -B tools/check_role_pool_r0_offline_observation.py <observation_id>
```

`<observation_id>` is exactly the position-appropriate ID below. No other
token is variable. The launcher may not accept caller-selected command text,
script, cwd, timeout, environment, runtime version, or arguments. Shell text,
fallback commands, package installation, runtime acquisition, automatic retry,
and alternate validation are forbidden. Missing or incompatible `py -3.13`
fails before observation acceptance and creates no fallback route.

The command is one logical top-level validation operation. The observer must
account for its complete process tree. Zero or one transient descendant is
allowed only when the relationship and every terminal state are known, the
top-level operation exits, and `surviving_process_count=0`. More than one
descendant, unknown relationship, unknown terminal state, timeout or
termination uncertainty, a survivor, or incomplete cleanup fails closed.

The validation command must exit `0`, emit exactly one canonical
`trusted_owner_r0_offline_bootstrap_evidence.v1` validation payload and zero
stderr, and remain within existing output and 120-second bounds. That existing
payload is held in bounded memory and is never an observation receipt or a
publishable issue comment. Its in-process Python audit guard remains unchanged:
an observed in-harness process, network, write, or environment-mutation attempt
fails. The public observation `network_operation_count` is only the trusted
observer's executor-owned observed network count. Zero does not prove that
child networking was prevented, completely observed, or impossible.
`network_authorized=false` grants no permission to use a network.

### Exact Post-Exit Receipt Owner

The already-required trusted launch observer is the sole final receipt owner.
It owns the process handle and stream drains, waits for the validation command
to exit, completes process-tree, survivor, timeout, termination, cleanup,
pre/post binding, effect, and residue observation, and only then invokes the
pure in-memory function
`seal_proportionate_observation_receipt(validation_payload, post_exit_facts,
sequence_position)` from the existing
`tools/check_role_pool_r0_offline_observation.py` module. The launch observer
loads that reviewed module in its existing control process before consumption;
the call creates no process, file, or second execution lane.

`post_exit_facts` is one immutable parent-owned value with exactly these fields
and types, in order:

```text
top_level_process_count:int, descendant_process_count:int,
process_relationships_known:bool, process_terminal_states_known:bool,
surviving_process_count:int, top_level_identity_exact:bool|null,
timed_out:bool, termination_uncertain:bool, cleanup_confirmed:bool,
output_complete:bool, executor_network_operation_count:int,
repository_write_count:int, installed_write_count:int,
external_effect_count:int, generated_residue_count:int
```

The value is passed directly from the observer to the pure function in memory.
It is not accepted from CLI arguments, stdin, stdout, stderr, environment,
files, issue comments, or the validation process. The function strictly parses
the canonical validation payload, requires its exact inherited bindings and
expected R0 projection, applies the precedence below, builds the one matching
41-field receipt variant, recomputes its self-digest, round-trips the bytes, and
returns either those final bytes or one existing symbolic failure status. It
must not publish.

The outer observation harness consists only of the existing launch observer,
the one fixed validation command, and this in-process sealer call. The harness
emits the final canonical receipt only after the command and every observed
process are terminal and cleanup is exact. Publication remains the inherited
separate issue-776 no-replace/readback step. If the future execution owner
cannot load and invoke the exact reviewed pure function in its existing control
process, it must stop before consumption; adding a launcher, helper, wrapper,
or another execution lane is forbidden.

## Fresh Sequence

- sequence: `r0.offline.sequence.4.ff3d34eee94243a6a031d3334430bfca`;
- observation 1:
  `r0.offline.observation.1.v4.209f443bcbf144d99bbb5cecf8aa8bf3`;
- observation 2:
  `r0.offline.observation.2.v4.b0dacd7eeb56422f9107c0775d972be4`.

These three contract-reserved identities were generated once without search.
They are inert until independent acceptance, exact implementation review, and
a separate fresh owner decision. Entry into a consumption POST permanently
spends the selected identity. Observation 2 cannot be consumed until
observation 1 has an accepted immutable receipt and exact readback.

## Observation Profile V3

The 32-field profile is canonical JSON, UTF-8 without BOM, no insignificant
whitespace, and exactly one final LF:

```json
{"schema_version":"trusted_owner_r0_offline_observation_profile.v3","repository_id":1235264383,"issue_number":776,"current_rung":"R0","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","r0_checker_sha256":"34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914","r0_checker_test_sha256":"976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34","release_validator_sha256":"af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d","authority_index_sha256":"2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0","implementation_paths":["tools/check_role_pool_r0_offline_observation.py","tests/test_check_role_pool_r0_offline_observation.py"],"fixed_command":["py","-3.13","-B","tools/check_role_pool_r0_offline_observation.py","<observation_id>"],"host_os_name":"nt","host_sys_platform":"win32","top_level_operation_limit":1,"descendant_process_limit":1,"surviving_process_limit":0,"process_relationships_known_required":true,"process_terminal_states_known_required":true,"top_level_identity_role":"diagnostic_nonblocking","network_observation_scope":"executor_owned_observed_only","network_operation_limit":0,"external_effect_limit":0,"observation_count":2,"timeout_seconds":120,"retry_limit":0}
```

The complete profile is 1,918 bytes and has SHA-256
`8fee508faddd873413cf655d8435e21121d9f713ede471ceaf768cfa65dd0c81`.

## Receipt V2

Receipt v1 cannot truthfully encode this policy. The versioned v2 receipt is
the sole observation-result schema change. It keeps the v1 fields and order
and inserts exactly four process-evidence fields after
`descendant_process_count`:

1. `process_relationships_known`: boolean, required `true` for acceptance;
2. `process_terminal_states_known`: boolean, required `true`;
3. `surviving_process_count`: integer, required `0`; and
4. `top_level_identity_exact`: boolean or null. `false` and null are
   nonblocking diagnostic values.

The exact 41-field order is:

```text
schema_version, sequence_id, observation_id, sequence_position,
predecessor_observation_id, repository_id, issue_number, current_rung,
profile_contract_sha256, release_state_artifact_sha256, release_record_sha256,
source_tree_sha256, installed_tree_sha256, registry_artifact_sha256,
registry_sha256, validator_bundle_sha256, observation_profile_sha256,
host_os_name, host_sys_platform, validation_status, release_state_status,
bootstrap_checker_terminal_status, derived_current_rung, process_topology,
top_level_process_count, descendant_process_count, process_relationships_known,
process_terminal_states_known, surviving_process_count,
top_level_identity_exact, process_launch_attempt_count,
network_operation_count, repository_write_count, installed_write_count,
external_effect_count, retry_count, unknown_outcome_count, cleanup_status,
accepted_for_independent_review, authority_flags, receipt_sha256
```

Unknown, missing, duplicate, reordered, or mistyped fields fail. The self-
digest preimage omits only `receipt_sha256`, retains every other key in order,
and ends in one LF. The complete object restores the lowercase SHA-256 as the
last field. Authority has the unchanged 16 fields, all `false`.

For count `0`, `process_topology` is
`single_top_level_zero_descendants_terminal`; for count `1`, it is
`single_top_level_one_transient_descendant_terminal`. All accepted variants
use top-level count `1`, known relationships and terminal states, survivor
count `0`, process-launch-attempt count `0`, executor-owned network count `0`,
write/effect/retry/unknown counts `0`, cleanup
`complete_no_survivors_no_residue`, and the inherited exact validation fields.

`top_level_identity_exact` has the closed values `null`, `false`, and `true`.
They mean unavailable, observed non-exact, and observed exact respectively.
No value makes an exact executable-provenance claim or changes acceptance.

### Receipt Known-Answer Matrix

Variant order is count `0` with identity `null/false/true`, then count `1`
with identity `null/false/true`. This fixed order is also the v2 consumption
allowlist order.

| Position | Descendants | Identity | Preimage bytes | Complete bytes | Receipt self-digest | Artifact SHA-256 |
| --- | ---: | --- | ---: | ---: | --- | --- |
| 1 | 0 | null | 2477 | 2561 | `1ee18ff073a8d998e6370fb6762b80aedaf9c656c4b4d15c1c54d216cb2b150c` | `2922a69cc5972f5b6a9901202f8749c0d3df519b9698a260f5c62e708d5a892b` |
| 1 | 0 | false | 2478 | 2562 | `54c362c1831668c8ab8130aa68541106f89536a754b212035c3a81610ef53d63` | `1e97d25b92c9ce92d594a2f33dfce5519383764d58b86f3a0a8e97d552932463` |
| 1 | 0 | true | 2477 | 2561 | `cc93c09eedcdeeb802ddafdb84abbf34be9ba9f96eccc5261e621d47fab7a6ed` | `f0ff509832a167eb4a42c51630b9683de5c4ba35fd734ad2e3aefc02444ee2ca` |
| 1 | 1 | null | 2485 | 2569 | `0c416f9a97151f14f5210feeebf13188b7d0bdb03035237e5bebebf7238deb61` | `f553e2d0ac110d988490f20122e5a6e1f92c8792bcb069d6e8d6119b9db1a9ea` |
| 1 | 1 | false | 2486 | 2570 | `8f1cadbb03d0c4b630e48e2b52e1bc97cd4f0d31ace194e34d4b881580b98e40` | `7fc75ccca246364c3b74d35bade5f5ec0dd893bbb532f8caf877ebb6c2500d1e` |
| 1 | 1 | true | 2485 | 2569 | `61a25cea3056cd0a4cfe8efd9072ad4a1a0dce0f6eeccb28033571da89a76cef` | `4ba512c8b2057223d47cec9a81604074f8598d737fc3d984ba7b0bf5cdbf0a67` |
| 2 | 0 | null | 2535 | 2619 | `1c6182fb3bfb6ec8cb069d141af4110a03bcce45fc928707451cd8281f6095a3` | `90705e6fac3ba7aefeeba3938647d23117a7a2ce193f2a1154524e32f58ec25b` |
| 2 | 0 | false | 2536 | 2620 | `ff39330edf11c3142641f2d6031d7dc540a4b65b6137fa3539a75a6ae4359ea3` | `dd1bc38ed2140fefc874d58db854f99382793f72fec65f5378a820f4e334bc2f` |
| 2 | 0 | true | 2535 | 2619 | `4294c180d32116c06c0036fa70a4826f5e15a4ae91d7761151de30605b4e8364` | `564e7a42ddaf4ba04c96ce1b93562bb6ea943a474d528a0128eae3a1ba555ef6` |
| 2 | 1 | null | 2543 | 2627 | `a641437ccceeeb0919a615981e02cb726cbc19137b5441e26656416906043c2b` | `e2351f414d40ba0022764048a850e2fa868718e0054a0fe1edc5422c3e1c193c` |
| 2 | 1 | false | 2544 | 2628 | `201e5cf48a49c4d286f7d3e6a325e5137280bec346bf18946a6e7d56fbc817b2` | `0ca85017b89062073b4764a23bc43164088d9eea19248c614772141672e83652` |
| 2 | 1 | true | 2543 | 2627 | `5c3e971c57aa34028a3ff9abdc480ab57eb5d9a456f0e0238f1db17a79f57052` | `52795d6fa8e94bfa6700c89aa0393d058bd7ca5558e254ed6a76c9816817d638` |

These twelve rows are the complete accepted receipt domain. No nonce search,
runtime sorting, identity grinding, or unlisted receipt is permitted.

## Consumption V2 Compatibility

The v1 consumption object's single `expected_receipt_sha256` cannot bind a
truthful measurement whose descendant and diagnostic identity values are not
known before launch. The same consumption family is therefore versioned to
`trusted_owner_r0_offline_observation_consumption.v2`. It retains 36 fields,
the existing field order and lifecycle, and replaces only the singular field
with `expected_receipt_sha256s`, an exact six-string array in the variant order
above. This is not a new authority or digest family.

All other consumption rules remain exact: one owner decision, one POST, exact
readback before launch, one attempt, no retry or reuse, collision and
ambiguous-commit terminal nonreuse, and no edit/delete/overwrite/repair.

The complete synthetic position-1 KAT is:

```json
{"schema_version":"trusted_owner_r0_offline_observation_consumption.v2","sequence_id":"r0.offline.sequence.4.ff3d34eee94243a6a031d3334430bfca","observation_id":"r0.offline.observation.1.v4.209f443bcbf144d99bbb5cecf8aa8bf3","sequence_position":1,"predecessor_consumption_sha256":null,"repository_id":1235264383,"issue_number":776,"owner_decision_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-owner","owner_decision_sha256":"1111111111111111111111111111111111111111111111111111111111111111","owner_decision_created_at_utc":"2026-08-01T00:00:00Z","owner_decision_expires_at_utc":"2026-08-01T12:00:00Z","sequence_contract_sha256":"2222222222222222222222222222222222222222222222222222222222222222","sequence_contract_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-contract-review","sequence_contract_review_sha256":"3333333333333333333333333333333333333333333333333333333333333333","harness_sha256":"4444444444444444444444444444444444444444444444444444444444444444","harness_test_sha256":"5555555555555555555555555555555555555555555555555555555555555555","implementation_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/776#issuecomment-kat-implementation-review","implementation_review_sha256":"6666666666666666666666666666666666666666666666666666666666666666","profile_contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","release_state_artifact_sha256":"723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9","release_record_sha256":"78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7","source_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","installed_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","observation_profile_sha256":"8fee508faddd873413cf655d8435e21121d9f713ede471ceaf768cfa65dd0c81","expected_receipt_sha256s":["1ee18ff073a8d998e6370fb6762b80aedaf9c656c4b4d15c1c54d216cb2b150c","54c362c1831668c8ab8130aa68541106f89536a754b212035c3a81610ef53d63","cc93c09eedcdeeb802ddafdb84abbf34be9ba9f96eccc5261e621d47fab7a6ed","0c416f9a97151f14f5210feeebf13188b7d0bdb03035237e5bebebf7238deb61","8f1cadbb03d0c4b630e48e2b52e1bc97cd4f0d31ace194e34d4b881580b98e40","61a25cea3056cd0a4cfe8efd9072ad4a1a0dce0f6eeccb28033571da89a76cef"],"decision":"consume_one_r0_offline_observation_identity","transition":"approved_unconsumed_to_consumed_exact_nonreusable","attempt_limit":1,"retry_authorized":false,"reuse_authorized":false,"launch_authorized_after_exact_readback":true,"status":"consumed_exact_nonreusable","consumption_sha256":"4f54d1df7627e9ac544822d4b140ed87ba47dea682137a6bbc3654910f5b29ca"}
```

It has 36 fields, preimage/complete sizes `2,869 / 2,957`, self-digest
`4f54d1df7627e9ac544822d4b140ed87ba47dea682137a6bbc3654910f5b29ca`,
and artifact SHA-256
`eab4d6326ee187d641ed0a3b63e958229e66e4aea4cc3d2573a27916d79a57e1`.
It is test data, not authority. Real consumption must bind accepted successor,
review, implementation, owner-decision, and immutable GitHub evidence.

## Deterministic Acceptance And Failure Precedence

Use the existing status vocabulary only, in this first-applicable order:

1. stale contract, source/install, registry, release, validator, harness, test,
   identity, sequence, or predecessor binding -> `observation_binding_rejected`
   or `observation_sequence_rejected` according to the owning predecessor;
2. invalid, expired, reused, collided, ambiguous, or unreadable consumption ->
   the inherited terminal consumption outcome; no launch;
3. non-Windows or incompatible fixed command -> `observation_host_rejected`;
4. top-level operation count not `1`, descendant count unavailable, process
   relationship unknown, or launch state unknown -> `observation_launch_unknown`;
5. timeout, termination uncertainty, terminal-state uncertainty, or cleanup
   uncertainty -> `observation_timeout_unknown`;
6. descendant count greater than `1`, any survivor, repository/install write,
   unauthorized external effect, executor-owned observed network operation,
   in-harness forbidden attempt, or residue ->
   `observation_safety_boundary_failed`;
7. incomplete or over-limit output -> `observation_result_unknown`;
8. nonzero harness exit, nonempty stderr, malformed/noncanonical receipt,
   receipt outside the six allowed variants, or receipt/readback mismatch ->
   `observation_validation_failed` or the inherited publication outcome;
9. all exact predicates and immutable issue-776 publication/readback ->
   `accepted_exact_r0_offline_observation`.

`top_level_identity_exact=false` or null never selects rows 4-8 by itself.
Detailed image or metadata identity is neither required nor accepted as an
executable-provenance claim. Observation 2 remains blocked until row 9 is
durably established for observation 1.

## Effects, Privacy, And Cleanup

Acceptance requires:

- repository writes `0`, installed-tree writes `0`, executor-owned observed
  network operations `0`, unauthorized external effects `0`, and generated
  residue `0`;
- exact pre/post source, installed, registry, release, validator, harness, and
  test bindings;
- zero surviving process, bounded stream drain, known terminal states, and
  complete cleanup; and
- no credential, token, proxy configuration, Python path override, or
  arbitrary ambient environment inherited by the operation.

No durable output may contain a private executable path, PID, handle, command
line, environment value, account or SID, raw process metadata, raw Win32
error, stack trace, credential, proxy, or private namespace inventory. Only
the fixed public command tokens, closed statuses, booleans, counts, public
repository references, and digests may leave bounded memory.

The observer may clean only proven attempt-owned temporary material. Unknown
ownership or cleanup state fails closed and preserves ambiguous material. No
receipt may be published while a survivor, effect, mutation, or residue fact
is unknown.

## Exact Future Codex C Scope

After independent Codex E acceptance and a separate owner implementation
decision, Codex C may modify exactly:

1. `tools/check_role_pool_r0_offline_observation.py`; and
2. `tests/test_check_role_pool_r0_offline_observation.py`.

The implementation is limited to:

- binding this successor and its review;
- retiring v1-v3 identities and installing the exact v4 sequence constants;
- replacing the blocking direct-identity/preflight dependency with the v3
  profile and proportionate process selector;
- implementing the 41-field receipt builder/parser and 36-field consumption-v2
  builder/parser with the exact known-answer matrices;
- preserving the command's existing canonical bootstrap-evidence projection
  as the bounded validation payload rather than a publishable receipt;
- implementing the pure post-exit sealer and exact `post_exit_facts` type;
- accepting only direct parent-observed process facts, never CLI-, stream-,
  environment-, file-, or child-supplied counts;
- preserving the existing validation algorithm, audit guard, no-echo,
  publication, chronological receipt-pair, and false-authority behavior; and
- adding operation-free fake-adapter tests.

No preflight executor, identity characterizer, secure-ingress path, third
durable implementation path, release/registry/index/profile artifact, package,
configuration, installation, process execution, or GitHub mutation is in C
scope. If the two files cannot consume trusted observer facts without a new
launcher/helper or caller-controlled process evidence, C must stop and return
to B rather than add an execution lane.

## Required Operation-Free Tests

Codex C and independent Codex E must prove without launching the real command:

1. descendant counts `0` and `1` pass with known relationships, known terminal
   states, zero survivors, exact validation, exact receipt, zero effects, and
   complete cleanup;
2. count greater than `1`, negative/non-integer count, any survivor, unknown
   relationship or terminal state, timeout/termination/cleanup uncertainty,
   write, external effect, executor-owned network event, residue, stale
   binding, nonzero exit, stderr, malformed receipt, or output overflow fails;
3. `top_level_identity_exact=false` and null alone do not fail; true does not
   create an executable-provenance claim;
4. all 12 receipt KATs and both six-digest consumption allowlists are exact;
   the complete position-1 consumption KAT independently reproduces `2,869 /
   2,957` bytes and digests `4f54...29ca / eab4...57e1`;
5. every receipt permutation outside its position's six variants fails;
6. chronological observation order and predecessor links remain authoritative;
7. all v1-v3 observation IDs and every #780/#795 identity remain nonreusable;
8. #780 preflight and #795 characterizer/secure ingress are absent from the
   eligibility dependency graph;
9. issue #769 publication remains impossible and every authority flag remains
   false; and
10. current bootstrap, release, and receipt-order focused tests remain green;
11. the command payload alone is never publishable; fake post-exit facts drive
    the pure sealer to each of the six accepted position variants, and every
    early, caller-supplied, malformed, incomplete, or unsafe fact set fails.

Required contract and later implementation validation:

```powershell
git diff --check
py -B tools/check_agent_docs.py
py -B tools/check_protected_surfaces.py --base origin/main
py -B tools/check_secret_patterns.py --base origin/main
py -B -m pytest tests/test_check_role_pool_r0_offline_observation.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_bootstrap.py -q -p no:cacheprovider
py -B -m pytest docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py -q -k release -p no:cacheprovider
```

These commands are contract, unit, or offline validation only. They are not an
R0 observation and grant no process or publication authority.

## Acceptance Criteria

Independent Codex E may accept only if:

1. every inherited binding and current starting byte is exact;
2. the override is limited to proportionate trusted-owner process acceptance;
3. the existing receipt's insufficiency and the minimal v2/v3 protocol delta
   are mechanically confirmed;
4. counts `0` and `1` are accepted only with known terminal state and no
   survivor, while every unsafe or unknown state fails;
5. exact identity, private-path transport, secure ingress, #780, and #795 are
   not eligibility dependencies and remain historical/deferred nonclaims;
6. all historical identities are terminal and nonreusable;
7. one fixed command, one operation, two fresh observations, one-way ordering,
   single-use consumption, no retry, and issue-776-only publication remain;
8. no child-network isolation or complete-observation claim is introduced;
9. the future implementation is exactly the two existing files and operation-
   free tests; and
10. only this contract changed, issue #769 stayed untouched, no process was
    launched, and generated residue is zero.

Contract acceptance makes only a separate owner Codex C implementation
decision eligible. Implementation acceptance makes only a separate owner
Observation 1 decision eligible. Observation 2 requires accepted Observation
1 publication and readback. R1 append/readback remains a separate owner
decision and integration action.

## Authority And Nonclaims

Current and terminal authority counts are `0`. Contract acceptance may make
only `implementation_decision_eligible=true`; it creates no authority itself.

Implementation, observation, receipt publication, release append, registry or
index mutation, installation, package operation, claim, command, task,
worktree, dispatch, canary, R1-R8, Stage 4, submission, merge, deployment,
readiness, security, privacy, or assurance authority is false. The profile
does not claim exact executable provenance, zero transient descendants,
child-network isolation, complete child-network observation, or global live
readiness.

## Next Workflow Action

Next role: Codex E, independent proportionate-observation successor contract
reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Trusted-Owner R0 Proportionate Observation
Successor Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/776
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md

Verify the exact SHA-256 from the Codex B handoff before review. Independently
confirm current-main and predecessor bindings, historical terminal nonreuse,
the fixed command, the 32-field profile, the 41-field receipt-v2 schema, all
12 receipt KATs, the 36-field consumption-v2 compatibility delta, chronological
ordering, process/effect precedence, the two-file future C scope, no-echo,
issue #769 protection, and all false authority fields.

Confirm `ME-RP-776-PROP-E-001` by independently parsing the complete canonical
36-field position-1 consumption-v2 KAT and reproducing its `2,869`-byte
preimage, `2,957`-byte complete artifact, self-digest
`4f54d1df7627e9ac544822d4b140ed87ba47dea682137a6bbc3654910f5b29ca`,
and artifact SHA-256
`eab4d6326ee187d641ed0a3b63e958229e66e4aea4cc3d2573a27916d79a57e1`.

Confirm `ME-RP-776-PROP-E-002` by proving that the fixed validation command
emits only the inherited bootstrap-evidence payload, that payload is never
publishable as an observation receipt, and the existing parent launch observer
can invoke the exact pure in-process sealer only after terminal, cleanup,
effect, and residue facts are complete. Reject any caller-controlled fact,
pre-exit sealing route, new file, helper process, or second execution lane.

Specifically test that descendant counts 0 and 1 can pass only with known
terminal state and zero survivors; count >1, any survivor, unknown state,
cleanup uncertainty, mutation, effect, malformed receipt, or stale binding
fails; and false or unavailable top-level identity alone does not fail. Confirm
#780 and #795 are historical/deferred and not eligibility dependencies.

Do not implement, execute an observation, create or consume authority, publish
a receipt, mutate issue #769 or release state, submit, merge, deploy, authorize
R1-R8 or Stage 4, or claim readiness. Findings lead. If exact, route to a
separate owner Codex C implementation decision for only the two contracted
files.
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
    - "ADR-0008"
  proposed_adrs_read:
    - "ADR-0010"
  protected_surfaces:
    - "R0 observation acceptance policy"
    - "single-use consumption and receipt publication"
    - "release-state prerequisite evidence"
    - "issue #769 no-comment boundary"
  authority_conflicts_found: true
  authority_conflict_notes: "The current owner instruction narrowly supersedes older zero-descendant and exact-identity eligibility language for trusted-owner R0 observations only."
  stop_conditions:
    - "a later owner decision supersedes the proportionate acceptance policy"
    - "the two-file implementation cannot consume trusted observer facts without caller-controlled evidence or a new execution lane"
    - "any inherited source, install, registry, release, validator, or publication binding drifts"
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Trusted-Owner R0 Proportionate Observation Successor Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/role-pool-r0-proportionate-observation-successor-776"
  base_commit: "be840bc1160678a9678d792d3cfd6074ac86ebca"
  contract_sha256: "reported_externally_by_codex_b_to_avoid_self_digest_cycle"
  schema_decision: "one versioned profile/receipt protocol plus one-field same-family consumption compatibility change"
  finding_status:
    ME-RP-776-PROP-E-001: "corrected_re_review_pending"
    ME-RP-776-PROP-E-002: "corrected_re_review_pending"
  historical_identity_status: "all_prior_observation_preflight_characterizer_identities_terminal_nonreusable"
  accepted_observation_count: 0
  files_changed:
    - "docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md"
  implementation_authorized: false
  observation_authorized: false
  receipt_publication_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "pending final Codex B validation"
  stop_conditions:
    - "scope expands beyond the one contract or two-file future implementation"
    - "process state, cleanup, effects, or bindings cannot be established exactly"
  next_recommended_role: "Codex E: independent proportionate-observation successor contract reviewer"
```
