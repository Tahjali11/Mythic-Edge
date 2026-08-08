# App-Native Role Pool R0 Binding And Sync Successor Contract

Status: `review_pending`

Risk tier: `high`

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/816

Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/813

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

Protected coordination issue:
https://github.com/Tahjali11/Mythic-Edge/issues/769

Base: `origin/main@ad88b264a1c7947682a00b11c4a57963a43b7548`

Governance sources:

- [`docs/agent_constitution.md`](../agent_constitution.md)
- [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md)
- [`docs/templates/module_contract.md`](../templates/module_contract.md)
- [`docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`](../decisions/ADR-0008-repo-wip-1-lane-activation-policy.md)

## Module And Owning Layer

This is an additive Quality / Governance contract for the repository-owned
Role Pool installer and read-only R0 checker. It is `shared_support`, not
parser truth, runtime dispatch truth, release acceptance, or installed-state
authority.

The installer owns exact source/predecessor tree observation and any later
separately authorized existing-target replacement. The checker owns the
public-safe read-only prerequisite packet. The canonical registry and release
ledger continue to own their respective records and digests.

## Finding And Narrow Decision

The exact current checker exits with
`r0_bootstrap_packet_unavailable`. Eleven of its twelve `FILE_BINDINGS` rows
are exact; only `stage3_validator` remains pinned to predecessor SHA-256
`8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6`
instead of accepted current SHA-256
`177a530104461979c0ee0113be74e04092a7ad2a390300735b89f7e4835f4726`.
Its Stage-3 manifest and source-tree constants are also predecessor values.

The offline operation still accepts only source tuple
`41/36/6495/18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`
and predecessor tuple
`39/34/6159/ab56582b39474db9e2cb50f83e7e05a341376efa7c9a10f0b1ec306c94d2009e`.
It therefore rejects both the
current source and the current installed copy before staging.

Decision: supersede only those stale custody values. Preserve the existing
installer algorithm, 37-field checker packet, closed vocabularies, selector
precedence, registry/release parsers, no-echo behavior, effects, authority
fields, and every operational gate.

Independent review finding `ME-RP-816-E-001` proves one downstream test-only
dependency: `tests/test_check_role_pool_r0_offline_observation.py` reads the
live checker and checker-test bytes and requires their current-successor
SHA-256 values. This revision adds only that dependent consumer. It preserves
the test's historical owner constants and permits only its two mechanically
derived current-successor digest expectations to change after the checker
bytes are frozen.

The Codex C partial implementation against predecessor contract digest
`c913aa5215425e6c8b71e95b19deb32e7f87e40818a6dc9a39a3d175f5d70df4`
produced a fifth-path diagnostic witness at 65511 bytes and SHA-256
`f30743f4cd96ff43761d515a0c74cc328217c4b8aa541b2e054716aa1318c994`.
Aggregate validation proved one further direct test-only consumer:
`tests/test_run_role_pool_r0_trusted_launch_observer.py` still names the fifth
path's predecessor digest. This correction adds only that sixth consumer and
one same-length current-successor digest replacement. It does not reopen any
production owner or behavior.

Independent review finding `ME-RP-816-E-002` proves that the diagnostic witness
cannot be an accepted target: the checker must bind the independently accepted
digest of this contract, and that post-review input changes every downstream
file digest. This contract therefore owns the exact derivation and freeze
order, not self-dependent final hash values.

This contract supersedes only:

1. the source snapshot and two tree tuples in the accepted profile's
   `Offline R0 Existing-Target Synchronization` subsection; and
2. the current binding custody and pre/post-sync projections in
   `role_pool_trusted_owner_r0_post_sync_evidence_binding_successor.md`.

Both predecessors remain immutable historical evidence. No other profile or
R0 clause is reopened.

## Exact Frozen Inputs

| Input | Exact binding |
| --- | --- |
| Integrated source commit | `ad88b264a1c7947682a00b11c4a57963a43b7548` |
| Trusted-owner profile | 119600 bytes; `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| App-native companion | 50531 bytes; `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4` |
| Stage-3 manifest | 41 rows; 6052 canonical bytes; `9109457e5897139658183595fb11c8a7bf9d66e4fb5b5fe6842b20bac43fbce2` |
| Stage-3 validator | 56176 bytes; `177a530104461979c0ee0113be74e04092a7ad2a390300735b89f7e4835f4726` |
| Registry validator | 477899 bytes; `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| App-native adapter | 59215 bytes; `b0eb739e960a342d95f148f6d2c57b121a2bed48c972907bc379cdbd2042d831` |
| App Server adapter | `9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18` |
| Complete offline gate | `1ac0dd02df447a35e7e95e3b534d89a2c7e0b3e5901266b780b5ba13238f8a75` |
| Registry artifact | 1478 bytes; `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |
| Registry self-digest | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Release artifact | 981 bytes; `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9` |
| Release-record self-digest | `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| Release-record profile | `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| Release-record skill tree | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Release-record validator bundle | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| Historical post-sync contract | 8527 bytes; `07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82` |

The registry parses as `valid_exact`. The one-record release chain parses as
`present_valid_chain`, but it remains bound to the predecessor profile, skill
tree, and validator bundle. It is valid historical R0 evidence, not current
app-native release acceptance.

The checker packet keeps schema
`trusted_owner_r0_offline_bootstrap_evidence.v1`, operation
`evaluate_r0_bootstrap_eligibility_read_only`, issue #761 lineage, and exactly
37 fields. Its exact `base_commit` changes from the predecessor source commit
to `ad88b264a1c7947682a00b11c4a57963a43b7548`. No field is added, removed,
renamed, reordered, or retyped.

## Exact Tree Transition

The installer must use its existing canonical
`trusted_owner_role_pool_install_tree.v1` algorithm and exact ordinal path
ordering.

| Role | Nodes | Files | Canonical bytes | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Current reviewed source | 43 | 38 | 6840 | `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| Only accepted installed predecessor | 41 | 36 | 6495 | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Required post-sync installed tree | 43 | 38 | 6840 | `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |

The exact predecessor-to-source row difference is:

| Change | Path | Predecessor bytes and SHA-256 | Source bytes and SHA-256 |
| --- | --- | --- | --- |
| modified | `scripts/check_pool_plan.py` | 467960; `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` | 477899; `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| modified | `scripts/check_stage3_behavioral_planning.py` | 54224; `8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6` | 56176; `177a530104461979c0ee0113be74e04092a7ad2a390300735b89f7e4835f4726` |
| modified | `scripts/test_check_pool_plan.py` | 140448; `60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49` | 156038; `a4b7a74925f16f12dc7c3b1de71a234bff832ea1aa645d884424466bad1fb93d` |
| modified | `scripts/test_stage3_behavioral_planning.py` | 207666; `800cea8db721ef1b1ca65f41acafd5ac2e45de29f251500ba495888acf6e81ec` | 215317; `aed2481fa580232b7bf425ac647efdbdeee0e02a05a22559ac76bd5f19c5c6f9` |
| added | `scripts/test_trusted_native_app_direct_task_adapter.py` | absent | 36099; `98bdec5936129946cc95a6cebce2645a3da50c81894e6c018e2b42739af50375` |
| added | `scripts/trusted_native_app_direct_task_adapter.py` | absent | 59215; `b0eb739e960a342d95f148f6d2c57b121a2bed48c972907bc379cdbd2042d831` |

All other rows are byte-identical. There are two added files, four modified
files, zero removed files, and zero renamed, case-varied, duplicate, or extra
paths.

## Closed Future Implementation Scope

Only these six files may change after independent contract acceptance and a
separate owner implementation decision:

1. `tools/install_codex_skills.py`
2. `tests/test_install_codex_skills.py`
3. `tools/check_role_pool_r0_bootstrap.py`
4. `tests/test_check_role_pool_r0_bootstrap.py`
5. `tests/test_check_role_pool_r0_offline_observation.py`
6. `tests/test_run_role_pool_r0_trusted_launch_observer.py`

Their exact starting bindings are:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `tools/install_codex_skills.py` | 45106 | `0898b4c476a3d1ac8fff726b146e40c2340a96134a4b035928fcbeaaff78d2ad` |
| `tests/test_install_codex_skills.py` | 51615 | `dd1a509af81cffe24f5edd1a50847bf8cca50b4cdba697bade4d08c26660447e` |
| `tools/check_role_pool_r0_bootstrap.py` | 46642 | `64057be2cec60724930db3a3a8f245dc352955aa387a01d2688de5fc5668e447` |
| `tests/test_check_role_pool_r0_bootstrap.py` | 57389 | `2a1ae7a85888b545babca82096673f34dac64ea7d032e8d9589f1be6a0b1126e` |
| `tests/test_check_role_pool_r0_offline_observation.py` | 65511 | `230cff121a14937ccc19b77d2f5ae73a411e85be32175e98d3a263da2c164557` |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | 41286 | `e479c4a38e6b0a15c993b78364faccf2f97e776fc41f71c22f7951a465675213` |

No seventh path is permitted. Another production owner, schema, status,
lifecycle, release writer, or target mode is a contract stop.

### Installer delta

Change only `OFFLINE_R0_SOURCE_BINDING` and
`OFFLINE_R0_PREDECESSOR_BINDING`:

| Binding field | Predecessor | Successor |
| --- | --- | --- |
| source node count | `41` | `43` |
| source file count | `36` | `38` |
| source canonical bytes | `6495` | `6840` |
| source SHA-256 | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` | `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| predecessor node count | `39` | `41` |
| predecessor file count | `34` | `36` |
| predecessor canonical bytes | `6159` | `6495` |
| predecessor SHA-256 | `ab56582b39474db9e2cb50f83e7e05a341376efa7c9a10f0b1ec306c94d2009e` | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |

Do not change discovery, no-follow observation, identity checks, default target
derivation, staging, replacement, rollback, cleanup, no-echo, exit codes, or
result vocabulary. The focused installer test may add only the exact successor
binding and regression cases required below.

### Checker delta

The checker may change only these custody values:

- `BASE_COMMIT` to `ad88b264a1c7947682a00b11c4a57963a43b7548`;
- `STAGE3_MANIFEST_FILE_COUNT` from `39` to `41`;
- `STAGE3_MANIFEST_BYTE_COUNT` from `5729` to `6052`;
- `STAGE3_MANIFEST_SHA256` from
  `cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06`
  to `9109457e5897139658183595fb11c8a7bf9d66e4fb5b5fe6842b20bac43fbce2`;
- the reviewed source tuple from
  `41/36/6495/18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`
  to
  `43/38/6840/3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6`;
- the `stage3_validator` `FILE_BINDINGS` row to
  `177a530104461979c0ee0113be74e04092a7ad2a390300735b89f7e4835f4726`;
- the installer row and `INSTALLER_SHA256` to the final frozen successor
  installer digest;
- the `r0_contract` row and `R0_CONTRACT_SHA256` from predecessor value
  `c913aa5215425e6c8b71e95b19deb32e7f87e40818a6dc9a39a3d175f5d70df4`
  to the independently accepted artifact digest supplied by the terminal
  Codex E contract-review handoff; and
- the `r0_contract` path to
  `docs/contracts/role_pool_codex_app_native_r0_binding_and_sync_successor.md`.

Every other `FILE_BINDINGS` row, adapter KAT, selector, field, and function is
unchanged. The final checker and checker-test digests are frozen only after
the preceding values are exact. The validator bundle is then recomputed from
the unchanged `trusted_owner_r0_validator_bundle.v1` fields. This order has no
circular dependency.

### Dependent observation-test delta

The fifth path is a test-only deterministic consumer. In
`test_frozen_owner_bindings_and_current_successor_rejection_remain_exact`, it
may change exactly two lowercase 64-character SHA-256 literals:

1. the current-successor expectation for
   `tools/check_role_pool_r0_bootstrap.py`, from
   `64057be2cec60724930db3a3a8f245dc352955aa387a01d2688de5fc5668e447`
   to the exact final checker SHA-256 frozen in the preceding checker step;
2. the current-successor expectation for
   `tests/test_check_role_pool_r0_bootstrap.py`, from
   `2a1ae7a85888b545babca82096673f34dac64ea7d032e8d9589f1be6a0b1126e`
   to the exact final checker-test SHA-256 frozen in that same step.

The historical `observation.R0_CHECKER_SHA256` and
`observation.R0_CHECKER_TEST_SHA256` owner constants, their predecessor
expectations
`34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914`
and
`976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34`,
the rejection assertion, test function, imports, ordering, and every other
byte remain unchanged. The two successor digests are derived from final file
bytes; they must not be guessed, copied from an intermediate build, or used to
relabel historical evidence.

The 65511-byte
`f30743f4cd96ff43761d515a0c74cc328217c4b8aa541b2e054716aa1318c994`
artifact is a diagnostic witness produced while the checker still bound
predecessor contract digest
`c913aa5215425e6c8b71e95b19deb32e7f87e40818a6dc9a39a3d175f5d70df4`.
It is not an accepted final target.
The final fifth-path digest is computed only after the accepted contract
digest, final checker digest, and final checker-test digest are frozen.

### Dependent trusted-launch-observer test delta

The sixth path is a test-only deterministic consumer. It may replace exactly
one occurrence: the value of `OWNER_TEST_SUCCESSOR_SHA256` changes from
`230cff121a14937ccc19b77d2f5ae73a411e85be32175e98d3a263da2c164557`
to the exact final SHA-256 of
`tests/test_check_role_pool_r0_offline_observation.py` frozen in the preceding
step. The replacement preserves the 41286-byte length. Its resulting final
digest is computed from those final bytes and is not named inside this
self-bound contract.

Substituting intermediate witness
`f30743f4cd96ff43761d515a0c74cc328217c4b8aa541b2e054716aa1318c994`
would derive diagnostic witness
`a0d627b851f9b18205a64a9847ad615eabe46b2eae2a0c34578ee0965553edac`.
Both values are rejected as accepted targets because they precede the final
contract-binding correction.

`OWNER_TEST_PREDECESSOR_SHA256` remains
`79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784`.
The fixture marker, bounded historical fixture, assertions, adapter behavior,
test names, imports, ordering, and every other byte remain unchanged.

The direct-consumer inventory is closed as follows:

| Inspected occurrence | Disposition | Reason |
| --- | --- | --- |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | included | Sole executable test consumer of the fifth path's current-successor digest. |
| this contract's fifth-path starting row | preserved | Records predecessor bytes; it is not a future runtime consumer. |
| `role_pool_codex_app_native_direct_task_terminal_status_binding_transition.md` | excluded | Immutable historical transition evidence. |
| `tests/test_check_role_pool_r0_offline_observation.py` | preserved producer | Its final artifact digest is the successor value; it does not consume that value as a literal. |

Repository-wide exact-string inspection found no other executable consumer of
either digest. A seventh path or another required literal is a contract stop.

### Downstream hash ownership and freeze order

The following labels are contract terms for build-time values. They add no
runtime field, schema, status, digest family, or durable artifact:

1. `accepted_contract_sha256` is owned by the terminal independent Codex E
   acceptance handoff for the exact contract artifact.
2. `final_checker_sha256` is derived from checker bytes after
   `R0_CONTRACT_SHA256=accepted_contract_sha256` and all other contracted
   checker custody updates are applied.
3. `final_checker_test_sha256` is derived from checker-test bytes after their
   exact checker and packet expectations are updated.
4. `final_observation_test_sha256` is derived from the fifth path after only
   its two current-successor expectations become `final_checker_sha256` and
   `final_checker_test_sha256`.
5. `final_launch_observer_test_sha256` is derived from the sixth path after
   only `OWNER_TEST_SUCCESSOR_SHA256` becomes
   `final_observation_test_sha256`.

Codex C records the four final implementation digests in its handoff; Codex E
independently recomputes them from exact bytes. No implementation may use the
B-authored contract digest before E acceptance, an intermediate contract
digest, or either rejected diagnostic witness as a final binding.

## Required Checker Projections

Before synchronization, the complete canonical packet must be sealable and
must contain:

- `contract_binding_status=exact`;
- `validator_bundle_status=exact`;
- `manifest_status=exact` and the exact 41-row Stage-3 tuple;
- the exact 43-node source and 41-node installed predecessor tuples;
- `source_install_status=installed_drift`;
- `registry_status=valid_exact` and registry self-digest
  `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7`;
- `release_state_status=present_valid_chain` and release artifact SHA-256
  `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9`;
- `offline_validation_status=passed`;
- `terminal_status=blocked_skill_source_drift`;
- `eligible_for_independent_review=false`;
- all five effect counts zero; and
- all 16 authority fields false.

This ordinary exact drift state must not become
`r0_bootstrap_packet_unavailable`. That sentinel remains unchanged for a
condition in which a complete canonical packet cannot be safely sealed.

A synthetic post-sync fixture must replace only the installed observation
with the exact 43-node source tuple. It must then produce:

- `source_install_status=identical`;
- the same valid registry and historical valid release chain;
- `terminal_status=blocked_release_state_conflict`;
- `eligible_for_independent_review=false`;
- zero effects; and
- every authority field false.

The post-sync terminal follows the existing precedence. It records that the
old R0 release record has not been rebaselined; it is not a sync failure and
does not authorize a release append. Independent review may verify the packet
even though its bootstrap eligibility field remains false.

## Preserved Synchronization Boundary

The only operation remains
`--offline-r0-sync --skill mythic-edge-role-pool` for
`offline_r0_existing_target_sync` on the trusted observed Windows host.

Preserve exactly:

- the default current-user target and rejection of `CODEX_HOME`,
  `--codex-home`, `--repo-root`, alternate skill, missing target, alternate
  root, search, wildcard, PATH, symlink, junction, reparse point, path escape,
  or nonordinary object;
- exclusive single-use execution, exact source and predecessor reobservation,
  stable identity, same-parent staging, exact staging readback, atomic
  replacement, rollback, final equality, and bounded cleanup;
- `blocked_request_or_packet_invalid` before mutation for invalid authority or
  host input;
- `blocked_skill_source_drift` before mutation for known source, predecessor,
  target, safety, identity, or concurrent-drift failure;
- `unknown_outcome_reconciliation_required` for ambiguous replacement,
  unproven rollback, uncertain final state, or uncertain cleanup;
- no retry, replay, replacement attempt, false cleanup claim, or deletion of
  an ambiguously owned object; and
- no native-task-capability query only for this exact offline operation.

No synchronization is authorized by this contract. After implementation,
independent review, integration, and exact current-binding validation, one
later attempt requires a fresh, expiring, nonreusable owner approval. It must
bind the accepted contract and review, final six-file implementation commit
and hashes, source commit
`ad88b264a1c7947682a00b11c4a57963a43b7548`, exact source and predecessor tuples,
one attempt identity, the exact operation, and the existing default target.
Consumption and every post-consumption outcome permanently retire that
authority.

## Required Operation-Free Tests

Future C and E validation must require:

1. exact source and predecessor tuple constants and the six-row tree delta;
2. stale source, stale predecessor, changed file, missing/extra path,
   count-preserving substitution, case variation, and row-order drift;
3. missing or alternate target, alternate home/root, non-Windows host,
   nonordinary or reparse source/ancestor/target, and path escape;
4. concurrent source or predecessor mutation before replacement;
5. staging collision, staging mismatch, first replacement failure, second
   replacement failure, rollback failure, final readback failure, cleanup
   uncertainty, and second-attempt refusal;
6. no native-task capability query, no path echo, and no automatic retry;
7. every exact checker binding, the 41-row manifest, and 43-node source tuple;
8. the exact production-like pre-sync packet and synthetic post-sync release
   conflict projection above;
9. all existing selector, schema, canonicalization, self-digest, privacy,
   effect, and false-authority tests unchanged; and
10. immutable historical release, observation, consumption, and #768 attempt
    evidence.

Required focused command:

```powershell
py -B -m pytest -q -p no:cacheprovider tests\test_install_codex_skills.py tests\test_check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_offline_observation.py tests\test_run_role_pool_r0_trusted_launch_observer.py
```

Also run the Role Pool offline release gate, repository aggregate gate,
`tools/check_agent_docs.py`, `git diff --check`, and
path-scoped protected-surface and secret/private-marker scans. Tests must use
synthetic roots and must not synchronize the real installed copy.

Project-virtual-environment Ruff 0.16.1 already passed on the five files whose
Python semantics changed. Do not rerun Ruff solely for the sixth path's
same-length digest-literal replacement unless relevant lint semantics drift or
independent-review policy requires another execution.

## Dependency Order And Freeze

1. Verify the accepted contract digest and all frozen inputs.
2. Update the installer constants and focused installer tests only.
3. Freeze installer and installer-test hashes.
4. Update checker custody values, including
   `R0_CONTRACT_SHA256=accepted_contract_sha256`, and focused checker tests
   only.
5. Freeze `final_checker_sha256` and `final_checker_test_sha256`.
6. Update only the two contracted current-successor digest expectations in the
   dependent observation test, then freeze
   `final_observation_test_sha256`.
7. Replace only the contracted sixth-path digest literal with
   `final_observation_test_sha256`, then freeze
   `final_launch_observer_test_sha256`.
8. Recompute the validator bundle and all packet KAT bytes and self-digests.
9. Run focused, offline release, aggregate, hygiene, process, and residue gates.
10. Route the exact six-file result to fresh independent Codex E review.

Any changed starting hash, seventh path, new schema/status/lifecycle, weakened
test, or inability to produce both exact packet projections stops the
implementation and returns to Codex B.

## Side Effects And Nonclaims

Codex B, C, and E validation has zero durable operational side effects. It
does not alter source skill bytes, the installed copy, registry, release
ledger, GitHub, claims, tasks, processes, worktrees, observations, or receipts.

Neither a passing implementation nor an accepted review authorizes
synchronization, release rebaseline, task creation, dispatch, observation,
R0 acceptance, R1-R8 advancement, Stage 4, submission, merge, deployment,
readiness, compatibility, security, privacy, or assurance.

Issue #814 remains parked and nontransferable. Issue #769 remains untouched.
The required R0 rebaseline remains a later Codex A framing, independent review,
and separate owner decision after exact source/install equality is reviewed.

## Acceptance Criteria

- Exactly one contract artifact changes in Codex B.
- Exactly six future implementation paths are closed and no seventh path is
  required.
- The fifth path changes only its two current-successor digest expectations;
  every historical observation owner constant and assertion remains exact.
- The sixth path changes only `OWNER_TEST_SUCCESSOR_SHA256` through the exact
  one-literal projection and preserves every historical fixture and behavior.
- The independently accepted contract digest owns the checker input; all four
  downstream implementation digests are derived only after that acceptance.
- Intermediate witnesses
  `f30743f4cd96ff43761d515a0c74cc328217c4b8aa541b2e054716aa1318c994`
  and
  `a0d627b851f9b18205a64a9847ad615eabe46b2eae2a0c34578ee0965553edac`
  are not accepted target hashes.
- All frozen artifact, registry, release, validator, adapter, source, and
  predecessor bindings independently recompute.
- Before sync, a complete packet selects `blocked_skill_source_drift` instead
  of the unavailable sentinel.
- The synthetic post-sync packet selects `blocked_release_state_conflict`.
- The packet schema, terminal precedence, sync algorithm, failure handling,
  no-retry rule, effects, and authority fields are unchanged.
- Historical evidence is preserved and no release rebaseline is absorbed.
- Fresh independent Codex E contract review is complete before any owner
  implementation decision.

## Next Workflow Action

Next role: Codex E, independent #816 self-binding and downstream-hash
ownership contract reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent #816 Self-Binding and Downstream-Hash Ownership
Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/816
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Base: origin/main@ad88b264a1c7947682a00b11c4a57963a43b7548

Review only:
docs/contracts/role_pool_codex_app_native_r0_binding_and_sync_successor.md

Reviewed predecessor SHA-256:
af731c8af192a608c4976089357265c89bea811014831d0c71fb630fe4f32701

Source finding:
ME-RP-816-E-002

Bind the exact SHA-256 from the Codex B handoff. Independently verify the
current source, installed predecessor, six changed rows, profile, registry,
release, Stage-3 manifest, validators, adapters, and six starting files.
Confirm the contract changes only stale tuple and checker custody values,
preserves the 37-field schema and existing lifecycle, and makes the exact
pre-sync packet select blocked_skill_source_drift while the synthetic post-sync
packet selects blocked_release_state_conflict.

Confirm the Codex C `blocked_exact_scope_closure` result is closed by exactly
one sixth, test-only path whose sole permitted change is the contracted
`OWNER_TEST_SUCCESSOR_SHA256` replacement. Confirm `ME-RP-816-E-002` is closed
by making the independently accepted contract digest the first downstream
hash input and by removing every circular exact final-hash target. Confirm the
complete consumer inventory, rejected diagnostic-witness disposition, and
preservation of every historical owner constant. Confirm no seventh path is
required and that a fresh expiring single-use owner approval remains required
for any later installed-copy mutation. Do not implement, synchronize, mutate
external state, create tasks, run observations, advance R0-R8 or Stage 4, or
claim readiness.

Return findings first, reviewed SHA-256, binding and scope verdicts,
validation, authority flags, generated residue count, and workflow_handoff.
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
  protected_surfaces:
    - "installed Role Pool copy"
    - "R0 evidence and release-state bindings"
    - "issue #769"
  authority_conflicts_found: false
  authority_conflict_notes: "Task-scoped owner activation permits one docs-only contract and expires with this handoff."
  stop_conditions:
    - "another implementation path or public schema is required"
    - "a current binding differs from the exact contract inventory"
    - "implementation, synchronization, release, task, or observation authority is requested"

workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/816"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_codex_app_native_r0_binding_and_sync_successor.md"
  target_artifact: "docs/contract_test_reports/role_pool_codex_app_native_r0_binding_and_sync_successor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "codex/role-pool-app-native-r0-binding-sync-contract-816"
  branch: "codex/role-pool-app-native-r0-binding-sync-contract-816"
  finding_status:
    ME-RP-816-E-001: "fixed_confirmed_preserved"
    ME-RP-816-E-002: "self_binding_and_downstream_hash_ownership_corrected_re_review_pending"
    implementation_scope_closure: "exact_six_paths_preserved"
  source_implementation_status: "blocked_exact_scope_closure"
  implementation_scope: "exactly six existing files; fifth path has two derived digest refreshes and sixth path has one exact digest replacement"
  implementation_authorized: false
  synchronization_authorized: false
  registry_or_release_state_authorized: false
  task_or_observation_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "exact source and installed tuples independently observed"
    - "Codex E focused witness: 373 passed; 12 failed; 3 platform skips"
    - "seven failures derive from predecessor contract binding and five from the pending sixth consumer"
    - "project-venv Ruff evidence preserved without redundant B rerun"
  stop_conditions:
    - "a seventh path, second sixth-file literal, production owner, schema, status, lifecycle, or authority change is required"
    - "exact current source or installed predecessor drifts"
    - "real installation, synchronization, task, observation, release, or GitHub mutation is requested"
```
