# Role Pool App-Native Direct-Task Downstream Binding Transition Contract

## Module

Additive Stage-3 manifest and historical downstream-test binding transition for
the accepted issue #813 app-native direct-task package.

## Source And Authority

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/813.
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746.
- Protected coordination issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/769.
- Draft PR: https://github.com/Tahjali11/Mythic-Edge/pull/815.
- Branch: `codex/role-pool-app-native-direct-task-contract-813`.
- Submitted head: `921e645e239660defb411796fd0b14fa7875e074`.
- Submitted base: `origin/main@c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`.

The owner's current instruction authorizes this one contract-only Codex B
amendment in the existing issue #813 lane. It transfers no implementation,
review, submission, operational, or release authority. Open PRs #374 and #391
are unrelated. Issue #769 is open with zero comments and remains untouched.

## Findings And Decision

1. The submitted ten-path issue #813 package is byte-exact at the bound head.
2. The package adds two managed Role Pool files and modifies two existing
   planner files. The Stage-3 validator still owns the accepted 39-file
   predecessor, so its current transition gate rejects the 41-file successor.
3. Six root tests reproduce that expected downstream drift: four offline-
   observation tests and two direct-interpreter preflight tests. The focused
   result is `6 failed, 283 passed`.
4. Accepted issue #813 contracts select the app-native realization and keep
   the direct-interpreter, secure-ingress, identity-characterizer, and related
   offline-observation evidence historical or deferred. They are not issue
   #813 eligibility paths or fallbacks.
5. Therefore one additive amendment is sufficient. Production offline-
   observation and direct-interpreter-preflight bytes remain frozen. Only the
   Stage-3 validator pair and two focused historical-binding test files need a
   later mechanical change.

No schema, lifecycle, receipt, observation identity, authority profile, or
production observer successor is required.

## Owning Layer And Truth

Quality / Governance owns this transition. Exact repository bytes and the
repository-owned projection algorithms own path membership, row order, byte
counts, and digests. Accepted predecessor contracts own historical observation
meaning. Tests verify those facts; they do not create authority.

Bridge-code status is `shared_support`. This contract does not own app-task
runtime behavior, R0 evidence, release state, installed state, or Stage 4.

## Bound Evidence

| Artifact | Exact SHA-256 |
| --- | --- |
| `docs/contracts/role_pool_codex_app_native_direct_task_adapter.md` | `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4` |
| `docs/contracts/trusted_owner_native_role_pool_profile.md` | `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| `docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md` | `de17a909d68fa1427d26ea42f5ff575addccf76185c77b93c03499e25bea48fa` |
| `docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md` | `cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4` |
| `docs/contracts/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md` | `17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84` |
| `docs/implementation_handoffs/role_pool_codex_app_native_direct_task_downstream_binding_fixer.md` | `b4f3bb9bcabeef23978e086967dda54ecb65d0bffe7b7116878407a84b33d0ce` |

The submitted issue #813 package is exactly:

| Status | Path | Byte count | SHA-256 |
| --- | --- | ---: | --- |
| modified | `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` | 477899 | `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| modified | `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py` | 155957 | `8c9a0e3d063c601e000a5097a5dbeeac1dd6f0a33b5924f9df8186997bba935e` |
| added | `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_direct_task_adapter.py` | 33152 | `48dee1083eb5f1a9b04af58e964946676b80d92c6f65d62f5137407897ab325e` |
| added | `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py` | 58671 | `fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98` |
| added | `docs/contract_test_reports/role_pool_codex_app_native_direct_task_adapter.md` | 13019 | `020ca24e5512647f7ebbff17bc09e8460f973eac766bdf46a5b46fc37f3e7721` |
| added | `docs/contracts/role_pool_codex_app_native_direct_task_adapter.md` | 50531 | `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4` |
| modified | `docs/contracts/trusted_owner_native_role_pool_profile.md` | 119600 | `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| added | `docs/implementation_handoffs/role_pool_codex_app_native_direct_task_adapter_hash_rebinding_fixer.md` | 11437 | `a092e15706b2d0f2f4d67c8af9d92dcf11658acf48a01028ad29ecf7c9b88feb` |
| modified | `tests/test_check_role_pool_r0_bootstrap.py` | 51101 | `e79ef77bcd6248c8db7853313e63b50448f07f35177e40f49886a361546035c9` |
| modified | `tools/check_role_pool_r0_bootstrap.py` | 46642 | `954236dba7a39d3e6223fa114bc7190caf42ce853309870ed7c351ba12ae4289` |

This amendment does not change any of those ten paths.

## Stage-3 Manifest Algorithm

The existing Stage-3 algorithm remains unchanged:

1. Include every ordinary file below
   `docs/codex_skills/mythic-edge-role-pool`, excluding `__pycache__`, `.pyc`,
   and `.pyo` entries.
2. Include the three frozen `mythic-edge-workflow` snapshot rows.
3. Represent every row with exactly `path` and `sha256`.
4. Use forward-slash paths rooted at `mythic-edge-role-pool/` or
   `mythic-edge-workflow/`.
5. Require exact case-sensitive membership, unique paths, and ordinal path
   ordering.
6. Canonicalize with UTF-8 JSON, ASCII escaping, sorted object keys,
   `separators=(",", ":")`, `allow_nan=false`, and no final LF.
7. SHA-256 the complete canonical bytes.

The frozen workflow rows remain:

| Path | SHA-256 |
| --- | --- |
| `mythic-edge-workflow/SKILL.md` | `04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb` |
| `mythic-edge-workflow/agents/openai.yaml` | `0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f` |
| `mythic-edge-workflow/scripts/accept_fallback_prompt.py` | `47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d` |

## Exact Stage-3 Transition

### Accepted 39-File Predecessor

- source: `origin/main@c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`;
- file count: `39`;
- canonical byte count: `5729`; and
- SHA-256:
  `cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06`.

This predecessor remains immutable historical evidence.

### Reviewed 41-File #813 Successor

- source: submitted head `921e645e239660defb411796fd0b14fa7875e074`;
- file count: `41`;
- canonical byte count: `6052`; and
- SHA-256:
  `4feede06164d2c3fa5d4367606c281928cd8841c6cb20e39561d36b06b835579`.

Relative to the predecessor, exactly 37 rows are unchanged, two are added,
two are modified, and zero are removed.

### Added Rows

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `mythic-edge-role-pool/scripts/test_trusted_native_app_direct_task_adapter.py` | `null` | `48dee1083eb5f1a9b04af58e964946676b80d92c6f65d62f5137407897ab325e` |
| `mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py` | `null` | `fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98` |

### Modified Rows

| Path | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `mythic-edge-role-pool/scripts/check_pool_plan.py` | `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` | `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| `mythic-edge-role-pool/scripts/test_check_pool_plan.py` | `60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49` | `8c9a0e3d063c601e000a5097a5dbeeac1dd6f0a33b5924f9df8186997bba935e` |

### Removed Rows

None. `removed_path_count=0`.

### Unchanged Rows

Every row below must remain present with the exact digest shown:

| Path | SHA-256 |
| --- | --- |
| `mythic-edge-role-pool/SKILL.md` | `1357cee674615f6b4311fe679f3adf08aadf21d009675c6701f2bcbbd522015d` |
| `mythic-edge-role-pool/agents/openai.yaml` | `34bf1fb42a79f2765d88b3c46ec728e69975759ed4839577aba5e559e6ffe2f9` |
| `mythic-edge-role-pool/references/external-isolation-broker-v3-corrective-successor.md` | `44988295fcb1bf1c65763eb7415cdf8e6ea6edb6deb6295d0c5c1dae0a2f9b55` |
| `mythic-edge-role-pool/references/external-isolation-broker-v4-corrective-successor.md` | `628c23aaaf2df7a58ac340e39f783dc1ef6f3eef766dd4c4b712b627d15a9487` |
| `mythic-edge-role-pool/references/external-isolation-broker-v5-corrective-successor.md` | `81aa7400268c0c23d8a2d14633c19cebdb64d464add7650cec53468f63f0b5d4` |
| `mythic-edge-role-pool/references/external-isolation-broker.md` | `b20b8813ad69aee8bb83bfc0f4dd73d05a7f504b30ba75d75cbd86511377d5aa` |
| `mythic-edge-role-pool/references/fallback-and-recovery.md` | `0d01fb8eab143127662876251a5c55addd3c6c6f81c0f1ec0336f0404045379b` |
| `mythic-edge-role-pool/references/fallback-pickup-fixture/injection.json` | `5322c32f5e252f9b74eec3264b34c4a0e04c32440d1b2a7f07ac0810cf672e3e` |
| `mythic-edge-role-pool/references/fallback-pickup-fixture/pickup.json` | `1b11d1f74d379e8f6b75ea2ae921e1c4ac11685b5d5f11ada39c68e7df8d7a32` |
| `mythic-edge-role-pool/references/fallback-pickup-fixture/prompt.json` | `d3d0c5b84dfaa99745a8446b7fffa54783b5e6629cb5e5d9aa9a984aa1861f0f` |
| `mythic-edge-role-pool/references/pool-state-schema.md` | `8ff8c14951137ccc7458ab04ade9d75c5d29b7d4517f29d3d5251b7017a4e477` |
| `mythic-edge-role-pool/references/release-remediation-matrix.md` | `01239e0959e7ffc9b962df189745e1bcd5facd7e3e516c35165faa7fb3be8ccb` |
| `mythic-edge-role-pool/references/role-readiness-and-safety.md` | `ede19a71e9989768645a527dabcef85752317a9751a39ab5410c6a4383bc5bd4` |
| `mythic-edge-role-pool/references/stage3-behavioral-planning.md` | `9b29d4546da706a8ceae8f106cb4e4acd7851587700089920898781005627c34` |
| `mythic-edge-role-pool/references/stage4-canary-exception.md` | `87dd645372eedfb89008b7d3d84f9b6fd87e17c2e0228ed953a1508e3308800d` |
| `mythic-edge-role-pool/scripts/check_fallback_pickup.py` | `c38191547694387f27af0614edf2566b80a1adc5b31f840bb81cd3dc6f9cf406` |
| `mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | `8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6` |
| `mythic-edge-role-pool/scripts/check_stage4_canary_exception.py` | `5fc41cee93396979d2689eea43b7a82fd869b64bbe8123b50b34c91fb51d01d9` |
| `mythic-edge-role-pool/scripts/codex_launcher_contract.py` | `396f031a566736a71263bc303f8a4600f77590335ff43c1c74b633b4f4b00847` |
| `mythic-edge-role-pool/scripts/offline_gate_guard/offline_guard.py` | `e508217276391b327119a16f8c21bbaa845c525868b4b3977bfd8f5e6d052fd9` |
| `mythic-edge-role-pool/scripts/offline_gate_guard/sitecustomize.py` | `ffa0a190b3617033825a9d284fb7e612cacef079fb551cdc950f8d3c401ca80c` |
| `mythic-edge-role-pool/scripts/pool_test_fixtures.py` | `3a2a6cf0c712f773de03a4c4928ed68879811a76e95f188018f1d3ced7440dab` |
| `mythic-edge-role-pool/scripts/regenerate_fallback_pickup_fixture.py` | `ac871a4dfcfb1a3cf517c6517af06699357b83d734e2084abd63300a3f0ae331` |
| `mythic-edge-role-pool/scripts/run_release_tests.py` | `1ac0dd02df447a35e7e95e3b534d89a2c7e0b3e5901266b780b5ba13238f8a75` |
| `mythic-edge-role-pool/scripts/test_codex_launcher_contract.py` | `564d0ac16c3cb3179cfb6775c5a490d1c9f12d07456b54c1934237e8ad0d5a6c` |
| `mythic-edge-role-pool/scripts/test_fallback_pickup.py` | `9a7e244a3ee66fb1f02e335c3967bb3b836d8347202918a24695daf23510c4de` |
| `mythic-edge-role-pool/scripts/test_offline_gate_guard.py` | `f5f1f964e4b8a107a88de3c24ba340e91a9c0a4d6541bafbdcd6bf6f46e4274c` |
| `mythic-edge-role-pool/scripts/test_pool_results.py` | `2ac469bba49316ec7be3e61f477caddb8a88d2219579b264ae270e4eab5ad645` |
| `mythic-edge-role-pool/scripts/test_release_adversarial.py` | `717f3f5f769bbd9c6eedba998da75a85192912b0085fa98847a59f2095a7779c` |
| `mythic-edge-role-pool/scripts/test_skill_contract.py` | `22442b73595d30e19ea2495ec8570c69cd2dd38f53d7a5a34b39cc5b8f5dcf61` |
| `mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py` | `800cea8db721ef1b1ca65f41acafd5ac2e45de29f251500ba495888acf6e81ec` |
| `mythic-edge-role-pool/scripts/test_stage4_canary_exception.py` | `84a3272f1ad2380206e7ef9dd4ceaa1ae71ed500b6be26a36cd3090b1bd06612` |
| `mythic-edge-role-pool/scripts/test_trusted_native_app_server_adapter.py` | `42e1d4d2e1edbf3c80b9d85e1b256afdc5f4475e18f0d662f7414c23af7a33be` |
| `mythic-edge-role-pool/scripts/trusted_native_app_server_adapter.py` | `9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18` |
| `mythic-edge-workflow/SKILL.md` | `04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb` |
| `mythic-edge-workflow/agents/openai.yaml` | `0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f` |
| `mythic-edge-workflow/scripts/accept_fallback_prompt.py` | `47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d` |

Any missing, extra, duplicate, renamed, case-varied, reordered, or
digest-mismatched row fails closed. Count-preserving substitution is invalid.

## Role Pool Subtree Transition

The existing repository-owned install-tree projection also remains unchanged:

1. Enumerate every ordinary, non-reparse descendant of the Role Pool source
   root in ordinal relative-path order.
2. Represent directories with empty payload and files with exact bytes.
3. Emit row fields in order `path`, `kind`, `byte_count`, `sha256` inside
   `trusted_owner_role_pool_install_tree.v1` with top-level order
   `schema_version`, `rows`.
4. Canonicalize with the existing trusted-native JSON rule and exactly one
   final LF.

The accepted predecessor tuple is:

```text
node_count=41
file_count=36
canonical_manifest_byte_count=6495
sha256=18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f
```

The reviewed issue #813 successor tuple is:

```text
node_count=43
file_count=38
canonical_manifest_byte_count=6840
sha256=f22d6557066a0449f3b7727621aa266bc3fda7ea5811965b30d964eebc4afc01
```

The five unchanged directory rows are `agents`, `references`,
`references/fallback-pickup-fixture`, `scripts`, and
`scripts/offline_gate_guard`. The file transition is the same two added and
two modified Role Pool rows listed above, with 34 unchanged Role Pool file
rows and zero removals.

## Authorized Mechanical Transition

A later implementation may do only the following:

1. Extend the Stage-3 accepted-current layer from the historical App Server
   39-file snapshot to the exact reviewed app-native 41-file snapshot.
2. Add exactly the two app-native adapter paths and their reviewed digests.
3. Update exactly the two reviewed planner-path digests.
4. Change only count values that semantically own this current manifest:
   current `39` becomes `41`, one missing current path is `40`, one extra
   current path is `42`, and count-preserving substitution remains `41`.
5. Preserve the Stage-2, 37-file, pre-fix 39-file, and accepted App Server
   39-file snapshots as immutable historical layers.
6. Recompute every Stage-3 transition object, KAT, and focused expected value
   that mechanically embeds the current path set, count, or digest.
7. Preserve all schemas, status vocabulary, selectors, lifecycle rules,
   no-echo guarantees, effect fields, and false authority fields.

Blind global replacement of `39`, `41`, hashes, byte counts, KAT values, or
other literals is forbidden. Unrelated values that happen to equal a manifest
count remain unchanged.

## Self-Included Validator Rule

The Stage-3 validator and its focused test are themselves manifest rows. The
reviewed 41-file digest above binds their current starting bytes. A later
implementation will necessarily change those two rows, so it must not embed
its own post-edit file digest or complete post-edit manifest digest as a
self-admission condition.

Codex C must report:

- exact before and after hashes for both Stage-3 files;
- the complete post-C 41-row canonical byte count and SHA-256;
- proof that the post-C manifest differs from the reviewed #813 successor only
  in those two self-included rows; and
- all operation-free validation results.

Fresh Codex E review, not a circular internal constant, accepts or rejects the
post-C snapshot.

## Offline-Observer Ownership Decision

`tools/check_role_pool_r0_offline_observation.py` remains bound to its
historical proportionate-observation sequence, predecessor profile, release
record, validator bundle, 39-file Stage-3 manifest, and 41-node/36-file Role
Pool tree. Its production bytes remain unchanged.

`tools/run_role_pool_r0_direct_interpreter_preflight.py` likewise remains
bound to the historical predecessor tree and deferred direct-interpreter path.
Its production bytes remain unchanged.

The issue #813 profile and companion explicitly select the app-native path and
defer those paths. Current successor-tree input must therefore continue to
fail closed in both historical production owners. No historical observation,
receipt, sequence ID, consumption record, preflight result, or KAT is
regenerated, reinterpreted, relabelled, or accepted as successor-tree evidence.

The focused tests may change only to:

- reproduce historical success from bounded in-memory predecessor fixtures;
- prove the exact current successor profile/tree is rejected by the historical
  owner;
- prove all frozen constants and historical KATs remain exact;
- stop comparing frozen historical bindings to current successor files as if
  they had the same ownership; and
- isolate the alternate-`CODEX_HOME` test with a historical-compatible fake
  parent so it reaches and tests only its named installed-root boundary.

No offline-observer profile, receipt, identity, KAT, schema, or digest changes.
No direct-preflight result, KAT, schema, or digest changes. A future
successor-profile R0 observation, if any, requires its own accepted owner and
cannot be inferred from this transition.

## Exact Future Implementation Scope

After independent contract acceptance and a separate owner implementation
decision, Codex C may modify exactly:

| Path | Starting byte count | Starting SHA-256 | Permitted purpose |
| --- | ---: | --- | --- |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | 54224 | `8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6` | Adopt the exact 39-to-41 manifest transition. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py` | 207666 | `800cea8db721ef1b1ca65f41acafd5ac2e45de29f251500ba495888acf6e81ec` | Prove the transition and all negative cases. |
| `tests/test_check_role_pool_r0_offline_observation.py` | 63327 | `79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784` | Separate historical fixtures from current successor rejection. |
| `tests/test_run_role_pool_r0_direct_interpreter_preflight.py` | 72269 | `c19f79d43d4ce1ac0b913d588f14dcbcbd2786047f987f45f113284a53ce3bbc` | Preserve the historical tuple and isolate successor/alternate-root rejection tests. |

The following production files are explicitly excluded and must remain at
their starting hashes:

| Path | Required unchanged SHA-256 |
| --- | --- |
| `tools/check_role_pool_r0_offline_observation.py` | `ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5` |
| `tools/run_role_pool_r0_direct_interpreter_preflight.py` | `429021301e9aad9958dfafae22fa98665ed75d0f80b241963cc4ecfb97ce97ed` |

No fifth implementation path is permitted. Any need for another path, public
schema, interface, lifecycle, or authority change stops and returns to Codex B
or Codex A.

## Required Operation-Free Tests

The later implementation must reject:

- either added path missing;
- either added path renamed or case-varied;
- either added-path digest changed;
- either modified planner digest changed;
- any extra or duplicate path;
- any removed predecessor path;
- a count-preserving path substitution;
- non-ordinal row order;
- a stale predecessor tuple;
- a mixed predecessor/successor tuple;
- historical observation evidence presented as successor evidence;
- alternate `CODEX_HOME` input as a replacement for the canonical installed
  root; and
- any no-echo, effect, or false-authority violation.

Tests must also prove the exact 39-file and 41-file Stage-3 snapshots, exact
41-node and 43-node Role Pool tuples, historical fixture acceptance, current
successor rejection by historical owners, and unchanged historical KATs.

All tests are synthetic and operation-free. They create no task, process,
observation, authority object, receipt, claim, worktree, installation,
registry, release record, network operation, or GitHub mutation.

## Acceptance And Lifecycle

Independent Codex E may accept only if:

1. every source artifact and submitted #813 package byte is exact;
2. both canonical transition calculations reproduce independently;
3. the transition contains exactly two additions, two modifications, 37
   unchanged Stage-3 rows, and zero removals;
4. the four-file future scope is sufficient;
5. both production historical owners remain byte-exact and fail closed on the
   successor tree;
6. no historical evidence is rebound as current;
7. no schema, lifecycle, status, receipt, identity, KAT family, or authority
   field changes;
8. issue #769 remains untouched; and
9. only this contract changed in Codex B, with zero generated residue.

Contract acceptance makes only a separate owner Codex C implementation
decision eligible. A later passing aggregate gate permits routing to fresh
Codex E implementation review and then Codex F. It does not authorize task
creation, installation, synchronization, R0 evidence, release-state mutation,
submission, merge, or deployment.

## Authority And Non-Claims

Current and terminal authority remains false for implementation, task or
process creation, observation or preflight execution, authority consumption,
receipt publication, source or installed-tree mutation, registry or release
mutation, package work, dispatch, canary, R0-R8 advancement, Stage 4,
submission, merge, deployment, assurance, or live readiness.

This contract makes no compatibility, correctness, security, privacy,
assurance, deployment, or readiness claim. It does not claim that historical
observations validate the app-native successor, that a current installed copy
matches the successor, or that any operational prerequisite has passed.

## Review Route

Fresh Codex E reviews this exact contract against the bound head, source
artifacts, submitted ten-path package, both canonical transition algorithms,
the six reproduced failures, and the four-file scope. The review is read-only
except for its separately authorized contract-test report. No implementation
or operational action may overlap that review.
