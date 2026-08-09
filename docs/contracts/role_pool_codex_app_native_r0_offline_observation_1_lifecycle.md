# App-Native R0 Offline Observation 1 Lifecycle Contract

## Source And Authority

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/826>.
- Parent profile issue: <https://github.com/Tahjali11/Mythic-Edge/issues/813>.
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>.
- Historical predecessor: <https://github.com/Tahjali11/Mythic-Edge/issues/776>.
- Protected coordination issue: <https://github.com/Tahjali11/Mythic-Edge/issues/769>.
- Constitution: `docs/agent_constitution.md`.
- Role: `docs/agent_threads/module_contract.md`.
- Template: `docs/templates/module_contract.md`.
- Risk tier: high.
- Authoritative base commit:
  `f5eda24457527dcc603c6d3900ac7cf527c0f046`.
- Authoritative base tree:
  `c3c726150cf1821c8ec2d5850009ab1d33071145`.

This Codex B artifact creates no implementation, observation, identity,
consumption, publication, release, or rung authority. A future operation must
use the accepted and integrated bytes of this contract, an independently
accepted implementation, and a separate exact owner decision.

## Findings And Decision

1. **Observed:** the current source and installed Role Pool trees are equal at
   `43` nodes, `38` files, `6840` canonical bytes, and SHA-256
   `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6`.
2. **Observed:** the current bootstrap checker validates the app-native R0
   tuple and terminates at `blocked_release_state_conflict`, with all effect
   counts zero and all authority flags false. That terminal is the expected
   post-release R0 boundary, not an observation failure.
3. **Observed:** the existing observation harness owns the needed canonical
   profile, consumption, validation-payload, receipt, selector, sealing, and
   no-echo machinery. Its production constants remain bound to immutable
   issue #776 history.
4. **Derived:** the current stable validator bundle excludes the observation
   harness, its focused test, and the trusted-launch-observer test. Rebinding
   those three files therefore does not change the stable validator-bundle
   digest.
5. **Observed:** the prelaunch matrix and trusted launch observer retain the
   predecessor harness digest as historical fail-closed evidence. They are not
   current app-native R0 bundle owners.
6. **Observed:** the trusted-launch-observer test imports the current owner API
   directly and accepts the predecessor's one-descendant receipt variants in
   three active cases. Those expectations conflict with this successor's exact
   zero-descendant rule even though the production trusted-launch observer is
   correctly frozen to predecessor bytes.
7. **Decision:** reuse the existing observation harness and focused test, plus
   reconcile only the direct owner-API expectations in the one mixed
   trusted-launch-observer test. A separate app-native harness or new execution
   mechanism is not required. The future implementation envelope is exactly
   three files.
8. **Observed (ME-RP-826-E-002):** PR #809 independently accepted the exact current production
   observer at reviewed head
   `6996f10fa222a192b2eb21e04919dbb8251ee7bb`, including its operation-free
   predecessor-payload and path-replacement coverage, before merge commit
   `707adfedd6740e0843ebdb8bb78312361def262d`. The reviewed observer SHA-256
   was and remains
   `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a`.
9. **Decision:** issue #826 inherits that durable exact-head acceptance as
   immutable historical evidence. It does not reconstruct predecessor bytes
   or re-prove predecessor execution. The mixed bridge test must retain
   current fail-closed successor-drift coverage and the direct current-owner
   topology tests without changing the production observer.

If implementation or independent review proves that any fourth file must change
for this observation to be truthful, work stops for owner scope reconciliation.
That evidence is not permission to widen this contract.

## Owning Layer

The Core Role Pool R0 evidence layer owns the observation profile,
single-use consumption state, candidate receipt, and deterministic lifecycle.
The bootstrap checker owns the current source, install, registry, release, and
validator facts. The app-native adapter owns its inert fake-client behavior.
The parent observation controller owns launch, timeout, process, cleanup,
candidate-receipt publication, and publication readback facts.

The child harness never owns parent-observed process, cleanup, or publication
facts. Fake-client output never owns repository, release, authority, or task
truth.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Repository ID | `1235264383` |
| Repository name | `tahjali11/mythic-edge` |
| Issue | `826` |
| Current rung | `R0` |
| Trusted-owner profile | `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| App-native adapter contract | `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4` |
| App-native adapter | `b0eb739e960a342d95f148f6d2c57b121a2bed48c972907bc379cdbd2042d831` |
| App-native adapter test | `98bdec5936129946cc95a6cebce2645a3da50c81894e6c018e2b42739af50375` |
| Source tree | `43` nodes; `38` files; `6840` bytes; `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| Installed tree | `43` nodes; `38` files; `6840` bytes; `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| Registry artifact | `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |
| Registry self-digest | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Release artifact | `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2` |
| Release tip | `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91` |
| Authority index | `a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9` |
| Bootstrap checker | `897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a` |
| Bootstrap checker test | `55a40f12d7d161eb40fca2905f442b3b6ecd1fc029e3313c81566db89dd6ae3f` |
| Stable validator bundle | `be432ceab519e42fc688800c2cda1b172845abb329acc942ba11c5a5490826ca` |
| Release validator | `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| Starting harness | `78832` bytes; `ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5` |
| Starting harness test | `76374` bytes; `e995299858bebaafafcbd19ffe71cf8aacf2f85fbe17a51d6bf0009af8087427` |
| Current observation receipt list | empty |

Every binding is revalidated before implementation review, integration,
owner decision, consumption, launch, sealing, publication, and receipt review.
Drift fails closed. No hash is repaired, inferred, or globally replaced.

## Immutable Historical Boundary

Every issue #776 sequence, observation, consumption, receipt, execution,
preflight, characterizer, and owner-decision identity remains spent,
consumed, retired, or otherwise permanently nonreusable according to its
recorded disposition. None is rebound to issue #826.

These current files remain read-only historical consumers:

| Path | Current SHA-256 | Required disposition |
| --- | --- | --- |
| `tools/check_role_pool_r0_prelaunch_gate_matrix.py` | `485c7965ec73c9f9c4fe387b6644eb1c04a4d082e4bc8f79d1ef19be32d55b7c` | Retain predecessor binding and fail closed against successor harness bytes. |
| `tests/test_check_role_pool_r0_prelaunch_gate_matrix.py` | `29d3098ac0f74198f7a2991938a8289d2969d78fd0da06c2487c4f1624b6e734` | Preserve historical matrix behavior. |
| `tools/run_role_pool_r0_trusted_launch_observer.py` | `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a` | Retain predecessor binding and fail closed against successor harness bytes. |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | `40858` bytes; `33d83c47e222505ba2de36ff5a50f669e26257f09c9737648dc9fabf88cb4e72` | Mixed bridge test: retain current successor-drift rejection and reconcile only direct current owner-API topology expectations; do not re-prove predecessor execution. |

The two production tools' rejection of successor bytes is expected historical
separation, not a reason to edit them. The trusted-launch-observer test is the
sole mixed consumer: its production-observer path must reject the successor
harness bytes before adapter construction or launch, while its direct import of
the current owner API must enforce the successor's zero-descendant domain. It
must not reconstruct, embed, retrieve, or execute predecessor bytes. If an
aggregate gate requires either production tool or the prelaunch-matrix test to
accept successor bytes, this contract is nonconstructible within its three-file
ceiling and must return to the owner.

### Inherited Exact-Head Acceptance Evidence

Issue #826 relies on, and does not recreate, this public historical evidence:

| Property | Exact value |
| --- | --- |
| Pull request | <https://github.com/Tahjali11/Mythic-Edge/pull/809> |
| Reviewed head | `6996f10fa222a192b2eb21e04919dbb8251ee7bb` |
| Reviewed tree | `26e1d04302e96f2c129b835f197b304195342dd7` |
| Merge commit | `707adfedd6740e0843ebdb8bb78312361def262d` |
| Independent verdict | `accepted_exact_r0_trusted_launch_observer_close_cancellation_fix` |
| Production observer SHA-256 | `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a` |
| Reviewed observer-test SHA-256 | `e504f417a9d47e24f095b7354facaf4ae6cad98fa129b01370bdee656bad4be1` |
| Operation-free validation | `72` focused observer tests and `187` parent observation tests passed |

At that reviewed head, the exact observer-test bytes included affirmative
verified-payload and path-replacement coverage for the same exact production
observer bytes. This table is an evidence reference, not a fixture, authority,
or requirement to rerun historical behavior. Drift in the production observer
hash invalidates this inheritance and stops work; drift in later test bytes
does not relabel or erase the accepted historical review.

## Reused Schema Decision

No new lifecycle, receipt, consumption, validation-payload, authority, or
digest family is permitted.

- Reuse the 32-field `trusted_owner_r0_offline_observation_profile.v3` shape
  for one new current-tuple instance.
- Reuse the 36-field
  `trusted_owner_r0_offline_observation_consumption.v2` schema.
- Reuse the 37-field `trusted_owner_r0_offline_observation_validation.v1`
  bootstrap payload without adding fields.
- Reuse the 41-field `trusted_owner_r0_offline_observation_receipt.v2`
  schema and canonical field order.
- Reuse the 12-input lifecycle selector and its existing closed values.
- Narrow the predecessor variant domain to exactly three allowed post-exit
  receipt variants for one position: `top_level_identity_exact` equal to
  `null`, `false`, or `true`. Every accepted variant has exactly one top-level
  process, zero descendants, and zero survivors.

The receipt's `top_level_identity_exact` remains diagnostic and nonblocking.
It creates no executable-provenance, image-identity, secure-ingress, hostile
content, or OS-isolation claim.

### Exact Profile Instance

The exact canonical profile instance has 32 fields, 1975 bytes including its
final LF, and SHA-256
`a657ed989026996329150d5a64212c85260857ce998dea271241828cad0e333f`.

```json
{"schema_version":"trusted_owner_r0_offline_observation_profile.v3","repository_id":1235264383,"issue_number":826,"current_rung":"R0","profile_contract_sha256":"8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952","release_state_artifact_sha256":"fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2","release_record_sha256":"836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91","source_tree_sha256":"3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6","installed_tree_sha256":"3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6","registry_artifact_sha256":"4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"be432ceab519e42fc688800c2cda1b172845abb329acc942ba11c5a5490826ca","r0_checker_sha256":"897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a","r0_checker_test_sha256":"55a40f12d7d161eb40fca2905f442b3b6ecd1fc029e3313c81566db89dd6ae3f","release_validator_sha256":"5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361","authority_index_sha256":"a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9","implementation_paths":["tools/check_role_pool_r0_offline_observation.py","tests/test_check_role_pool_r0_offline_observation.py","tests/test_run_role_pool_r0_trusted_launch_observer.py"],"fixed_command":["python.exe","-B","tools/check_role_pool_r0_offline_observation.py","<observation_id>"],"host_os_name":"nt","host_sys_platform":"win32","top_level_operation_limit":1,"descendant_process_limit":0,"surviving_process_limit":0,"process_relationships_known_required":true,"process_terminal_states_known_required":true,"top_level_identity_role":"diagnostic_nonblocking","network_observation_scope":"executor_owned_observed_only","network_operation_limit":0,"external_effect_limit":0,"observation_count":1,"timeout_seconds":120,"retry_limit":0}
```

`python.exe` is the public-safe basename projection. The parent controller must
directly invoke one owner-bound absolute Python 3.13 executable without PATH
lookup, shell, `py.exe`, alias, shim, wrapper, or alternate runtime. The path
exists only in bounded parent memory and is never a profile, prompt, argument,
receipt, comment, log, exception, or handoff value. This requirement does not
revive issue #780 or #795 as an eligibility dependency and makes no exact
image-identity claim.

## Fresh Identity And Owner Decision

Codex B and Codex C create no live sequence or observation identity. After the
contract is integrated and the exact implementation has independent Codex E
acceptance, a separate owner decision may create exactly one pair:

- `sequence_id = r0.app_native.offline.sequence.1.<token>`;
- `observation_id = r0.app_native.offline.observation.1.<token>`.

`<token>` is exactly 32 lowercase hexadecimal characters, is selected once
without search, permutation, grinding, or retry, and is not all zero. The same
token cross-binds the pair. It must not equal or alias any historical identity.
The all-zero token is reserved solely for operation-free test vectors and is
rejected by the live path.

The owner decision is one canonical, immutable GitHub comment on issue #826.
It binds the exact current commit, this contract and review, exact three-file
implementation and review, profile instance, sequence and observation IDs,
three allowed candidate-receipt digests, decision digest, issuance at a whole UTC
second, expiry exactly 12 hours later, `attempt_limit=1`, `retry_authorized=false`,
and `reuse_authorized=false`. It grants no Observation 2 or rung authority.

## Fixed Operation And Fake Transport

The one future operation is Windows-hosted and consists of one directly
launched top-level harness process. Its canonical public command projection is:

```text
[python.exe, -B, tools/check_role_pool_r0_offline_observation.py, <observation_id>]
```

The parent supplies no caller-selected command, arguments, cwd, environment,
input, prompt, model, task target, or task API. The cwd is the exact reviewed
repository root. The environment is minimal and excludes credentials, tokens,
proxy variables, Python path overrides, arbitrary ambient variables, and
bytecode writes.

The harness must:

1. reject every observation ID outside the owner-bound grammar and exact
   consumption object;
2. require `os.name=nt` and `sys.platform=win32`;
3. validate the exact profile and every current binding above;
4. call the current bootstrap checker in-process and require exact canonical
   payload bytes, `offline_validation_status=passed`,
   `release_state_status=present_valid_chain`, and
   `terminal_status=blocked_release_state_conflict`;
5. execute the accepted app-native adapter only through injected objects whose
   `synthetic_only` member is exactly `true`;
6. exercise the fixed operation-free fake-client cases for request, receipt,
   lifecycle, claim, duplicate, timeout, unknown-result, no-retry, and
   reconciliation behavior;
7. require every fake-client task-creation, listing, and readback count to be a
   contract-selected synthetic value and every real app-task operation count
   to remain zero;
8. emit only one canonical 37-field validation payload on stdout after every
   check passes; and
9. emit no stderr and write no file, receipt, cache, bytecode, registry,
   release, issue, task, claim, worktree, or external state.

The fake transport is deterministic in-memory test data. It cannot call
`create_thread`, `list_threads`, `read_thread`, a subagent, App Server, broker,
shell, `codex exec`, direct app connector, network client, or fallback. A fake
success is control evidence only; it does not prove live app compatibility.

## Parent Process And Timeout Boundary

The parent controller owns launch and all PostExitFacts. It must establish
before launch that the direct executable, cwd, argument array, environment,
source/install tuple, release tuple, process baseline, repository baseline,
and residue baseline are exact.

The limits are:

- one launch attempt;
- exactly one top-level harness process after process creation is entered;
- zero descendants;
- zero survivors;
- known parentage and terminal state;
- `120` elapsed seconds;
- bounded stdout of one canonical payload plus no extra bytes;
- bounded stderr of zero accepted bytes;
- one drain and one close attempt for every owned stream or process handle;
- no retry, relaunch, replacement, cancellation attempt, or fallback.

Timeout, output overflow, drain uncertainty, handle-close failure, unknown
parentage, unknown terminal state, any descendant, any survivor, or incomplete
cleanup is terminal failure. Best-effort termination after timeout is cleanup,
not retry. If termination or cleanup cannot be proven, the outcome is unknown.

## Consumption And Nonreuse

The parent validates every public binding before consumption. It then creates
the existing 36-field consumption-v2 object in memory, posts it exactly once
to issue #826, reads that exact comment once, and requires byte-identical
canonical readback before reading a private launch path or creating a process.
No comment is posted to issue #769.

The only successful transition is:

```text
approved_unconsumed -> consumed_exact_nonreusable
```

A known rejection before post entry consumes nothing and creates no process.
An ambiguous post, collision, appeared competing consumption, failed exact
readback, or any state after post entry makes the owner decision and identity
unavailable for automatic use. Reconciliation may read existing public state
only; it cannot repost, repair, replace, or reconstruct consumption.

After exact consumption readback, every outcome is permanently nonreusable:
success, child rejection, timeout, termination, cleanup failure, unknown
state, cancellation, malformed output, sealing failure, publication failure,
or publication ambiguity. No fresh identity is created automatically.

## Candidate Receipt Custody

The child output is a validation payload, never a receipt. After exact child
exit and PostExitFact derivation, the parent invokes the existing pure
`seal_proportionate_observation_receipt` function in-process. It supplies only
parent-owned facts and the exact owner-bound identity.

An acceptable candidate is one canonical 41-field receipt-v2 object with:

- current issue #826 and current tuple bindings;
- `current_rung=R0` and `derived_current_rung=R0`;
- `validation_status=accepted_exact_r0_offline_observation`;
- `release_state_status=present_valid_chain`;
- `bootstrap_checker_terminal_status=blocked_release_state_conflict_expected`;
- exactly one top-level process, zero descendants, known relationships and
  terminal states, and zero survivors;
- `process_topology=single_top_level_zero_descendants_terminal` and
  `process_launch_attempt_count=1`;
- zero process retries and zero unknown outcomes;
- zero executor-owned observed network operations;
- zero repository writes, installed-tree writes, and unauthorized external
  effects;
- `cleanup_status=complete_no_survivors_no_residue`;
- `accepted_for_independent_review=true`;
- every authority flag false; and
- an exact self-digest and final LF.

No candidate exists if any preceding field cannot be proven. The parent holds
the candidate in bounded memory until publication. Raw stdout, stderr, paths,
environment, process IDs, handles, transcripts, private values, and fake-client
fixtures are never durable receipt content.

The exact owner decision may authorize one no-replace candidate publication
on issue #826 after successful sealing. Publication is control-plane custody,
not an observation effect. Exact readback is required. A collision, appeared
comment, failed readback, or ambiguous publication preserves all appeared
state, publishes no success claim, spends the identity, and routes to fresh
read-only reconciliation. Publication is forbidden on every non-success route.
The harness itself cannot publish.

The published object remains a candidate for fresh Codex E review. It cannot
accept itself, alter release state, authorize Observation 2, or advance R0.

## Deterministic First-Failure Order

Apply the existing 12-input lifecycle selector. At minimum, precedence is:

1. public binding mismatch;
2. missing, stale, expired, reused, or malformed authority;
3. wrong sequence or observation identity;
4. consumption collision, ambiguity, or non-exact readback;
5. unsupported host or non-exact direct launch setup;
6. process-entry, timeout, termination, drain, relationship, survivor, handle,
   cleanup, effect, or residue failure;
7. malformed, noncanonical, nonzero-stderr, or extra output;
8. validation-payload or fake-transport failure;
9. receipt sealing or self-digest failure;
10. publication collision, ambiguity, or readback failure; and
11. candidate published for independent review.

Later checks never erase an earlier failure. Independent checks may continue
only when they create no process, task, write, network action, or ambiguity.
Unknown evidence is never converted to success.

## Effects, Privacy, And Cleanup

Before and after execution, the parent proves exact equality for repository
HEAD and tree status, installed tree, registry, release artifact and tip,
authority index, stable validator bundle, and generated-residue inventory.

Accepted observation effect counts are all zero. The network count covers only
executor-owned observed network operations and makes no claim that child
networking was OS-blocked or completely observed. `network_authorized=false`
grants no network authority; it is not an isolation claim.

Public output may contain only contract fields and public-safe digests. It must
not contain a private path, filename, PID, handle, command-line path,
environment value, credential, token, proxy value, raw error, transcript,
active-worktree content, machine identity, or lane conclusion. Unsafe values
cause rejection without echo.

Cleanup removes only proven attempt-owned unpublished temporary state. It must
not clean, reset, revert, delete, repair, or replace repository, installed,
GitHub, release, registry, or ambiguous state. Residue or cleanup uncertainty
is terminal and nonreusable.

## Exact Future Implementation Envelope

Codex C may later edit exactly:

1. `tools/check_role_pool_r0_offline_observation.py`;
2. `tests/test_check_role_pool_r0_offline_observation.py`;
3. `tests/test_run_role_pool_r0_trusted_launch_observer.py`.

The implementation may only:

- replace predecessor production bindings with the current profile instance;
- validate one post-integration owner-supplied identity pair without embedding
  a live identity;
- execute the fixed inert fake-client matrix in-process;
- preserve the 36-, 37-, and 41-field schemas and existing selector/sealer;
- reject all historical identities and all-zero live tokens;
- update deterministic synthetic KATs and focused tests; and
- preserve every no-echo, zero-effect, cleanup, nonretry, nonpublication, and
  false-authority rule above.

The third path is test-only. Its permitted change is exactly:

- keep `test_allowed_topologies_and_diagnostic_identity_seal` accepting the
  three `descendants=0` cases for identity diagnostics `true`, `false`, and
  `null`;
- require the same three `descendants=1` direct owner-API cases to return
  `observation_safety_boundary_failed` and emit no receipt; and
- update only mechanically dependent direct current-owner KAT assertions when
  the successor harness freezes its three-variant receipt domain.

The third path must preserve unchanged:

- `OWNER_TEST_PREDECESSOR_SHA256` and `OWNER_TEST_FIXTURE_MARKER`;
- `_bounded_historical_owner_fixture` as existing test-only plumbing, without
  treating successor bytes copied by that helper as predecessor evidence;
- every assertion that the production trusted-launch observer uses exact
  predecessor contract, owner, owner-test, and observer bytes;
- current-owner-drift, verified-payload, and path-replacement fail-closed
  tests, each requiring `observation_binding_rejected` before adapter
  construction or launch when presented with successor owner bytes;
- all fake native-boundary, timeout, handle, cleanup, no-publication,
  no-fallback, and false-authority tests; and
- the production observer bytes.

No fixture helper, marker, or constant cleanup is authorized by this
correction. The inherited PR #809 evidence owns historical acceptance; issue
#826 tests own only current fail-closed and direct current-owner behavior.

Repository-wide inspection found no literal consumer of the third path's
current SHA-256. The prelaunch matrix binds historical digest
`e504f417a9d47e24f095b7354facaf4ae6cad98fa129b01370bdee656bad4be1`,
not the current test digest, and remains unchanged and fail-closed. No fourth
path is mechanically required by this correction.

No production app-native adapter, bootstrap checker, release validator,
profile, release, registry, index, prelaunch matrix, trusted launch observer,
or other path may change. No schema field, lifecycle value, authority flag,
task API, launcher helper, executor, or runtime dependency may be added.

## Operation-Free Tests Required

All tests use injected clocks, fake transports, fake parent facts, synthetic
reserved identities, and temporary in-memory or test-owned state. They launch
no real process and call no real app-task or GitHub operation.

The focused suite must prove:

1. the exact 32-field profile bytes, length, digest, and current bindings;
2. old profile, release, tree, registry, index, validator, harness, test, and
   issue bindings fail closed;
3. the stable validator bundle remains exact and independent of harness/test
   bytes;
4. the fresh identity grammar, pair cross-binding, all-zero rejection,
   historical nonreuse, and no search or replacement route;
5. the 36-field consumption object, prelaunch readback, collision, ambiguous
   commit, duplicate consumption, and permanent nonreuse behavior;
6. all accepted inert fake-client request, receipt, lifecycle, claim,
   duplicate, timeout, unknown, no-retry, and reconciliation cases;
7. non-synthetic clients and every real task-management method are rejected or
   remain at call count zero;
8. exactly one top-level process and zero descendants can pass under fake
   PostExitFacts;
9. zero or more than one top-level process, any descendant, any survivor,
   unknown relationship or terminal state, timeout, incomplete drain, failed
   close, effect, mutation, or residue fails;
10. the three allowed candidate-receipt KATs are exact and every unlisted
    permutation fails;
11. candidate publication occurs only after sealing, once, on issue #826, with
    exact readback; all failure and ambiguity routes publish no success;
12. the 37-field child payload is never accepted as a receipt;
13. private values never appear in stdout, stderr, receipts, errors, comments,
    or handoffs;
14. all authority flags remain false and one accepted candidate remains R0;
15. Observation 2 and R1 routes remain unreachable; and
16. the historical prelaunch and production trusted-launch consumers remain
    unchanged and fail closed against successor harness bytes;
17. the mixed trusted-launch test preserves exact production-observer binding
    assertions, rejects successor owner bytes before adapter construction or
    launch, and divides its six direct current-owner cases into three
    zero-descendant accepted receipts and three one-descendant safety-boundary
    rejections; and
18. no fourth deterministic consumer exists.

Required validation after implementation includes:

```powershell
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_check_role_pool_r0_offline_observation.py
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_prelaunch_gate_matrix.py tests\test_run_role_pool_r0_trusted_launch_observer.py
py -3.13 -B -m pytest -q -p no:cacheprovider docs\codex_skills\mythic-edge-role-pool\scripts\test_trusted_native_app_direct_task_adapter.py
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B tools\check_protected_surfaces.py --base origin/main
py -3.13 -B tools\check_secret_patterns.py --base origin/main
git diff --check
```

No command above may create a real process through the observation harness,
task, claim, receipt, GitHub mutation, registry mutation, release mutation, or
installed-tree mutation.

## Stop Conditions

Stop and return to the owner if:

- a fourth implementation or test path is mechanically required;
- a separate harness, parent executable, launcher helper, broker, task API,
  network client, or new execution mechanism is required;
- a new schema field, receipt family, lifecycle state, authority field, or
  digest family is required;
- current bindings drift before acceptance or use;
- direct launch cannot produce exactly one top-level process and zero
  descendants;
- operation-free fake transport cannot cover the required adapter controls;
- the historical consumers must accept successor bytes;
- a private value must enter durable or public-safe evidence;
- a test or safety boundary would need to be skipped, weakened, or made
  advisory; or
- issue #769 would need any comment, dependency, or mutation.

## Acceptance And Ladder Boundary

Contract acceptance makes only the exact three-file inert implementation eligible
for a separate owner decision. Implementation acceptance and integration make
only one fresh Observation 1 owner decision eligible. An accepted candidate
receipt still requires fresh independent Codex E review.

One independently accepted Observation 1 receipt leaves the release at R0.
Observation 2 requires a later separate contract or successor, a distinct
identity, the same still-current bindings, and separate authority. R1
eligibility requires two distinct consecutive accepted observations, fresh
independent review, a separate owner advancement decision, and an exact
append-only release-state event.

This contract authorizes none of those future effects. It does not establish
task dispatch, live app compatibility, hostile-content isolation, exact
executable provenance, complete network observation, R1-R8, Stage 4,
submission, merge, deployment, assurance, or live readiness.

## Next Workflow Action

Next role: Codex E, fresh independent contract reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Independent App-Native R0 Observation 1 Lifecycle Contract
Re-reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/826
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review exactly:
docs/contracts/role_pool_codex_app_native_r0_offline_observation_1_lifecycle.md

Bind the exact SHA-256 reported by Codex B. Refresh origin/main and GitHub
state first. Confirm the contract reuses the existing observation harness and
focused test plus exactly one test-only trusted-launch bridge consumer,
preserves historical #776 identities, and introduces no fourth implementation
path or new execution mechanism.

Independently recompute the current profile, source/install, registry, release
tip, authority index, validator bundle, harness, test, and 32-field profile
KAT. Verify the 36-field consumption, 37-field payload, 41-field receipt, and
12-input lifecycle schemas are reused without new fields or values.

Confirm the operation is Windows-hosted, fake-transport-only, one top-level
process, zero descendants, zero survivors, zero real task calls, zero effects,
single-use, nonretryable, public-safe, and fail-closed. Audit consumption,
timeout, cleanup, unknown outcome, candidate publication/nonpublication,
historical consumer separation, Observation 2 denial, and the R0 ceiling.

Confirm `tests/test_run_role_pool_r0_trusted_launch_observer.py` is the sole
added test-only consumer. Confirm PR #809 provides durable exact-head acceptance
for the unchanged production observer SHA-256 and that #826 does not reconstruct
or re-execute predecessor bytes. The bridge test must retain current
successor-drift rejection before adapter construction or launch, while its
three direct current-owner `descendants=1` cases reject with
`observation_safety_boundary_failed` and emit no receipt.

Dispose ME-RP-826-E-002 as fixed only if the inherited PR #809 evidence is
exact, the production observer remains byte-identical, no predecessor-byte
fixture or execution is required, and all current fail-closed tests remain
mandatory.

Run the contract-required operation-free focused tests and structural/safety
checks. Do not implement, launch an observation process, create or consume an
identity, call a task API, publish a receipt, mutate issue #769, change release
or installed state, submit, merge, deploy, advance R0-R8 or Stage 4, or claim
readiness.

Lead with findings and return an exact contract verdict, reviewed SHA-256,
schema and three-file-scope verdicts, validation, authority flags, residue count,
and workflow_handoff. If accepted, the next role is an owner decision for the
exact three-file inert implementation, then Codex C.
```

```yaml
instruction_context:
  observed:
    - "Current app-native source and installed trees are equal."
    - "The current bootstrap terminal is blocked_release_state_conflict with zero effects and false authority."
    - "The existing observation harness is predecessor-bound but owns the reusable schemas and pure sealing logic."
    - "Historical prelaunch and trusted-launch tools intentionally pin predecessor harness bytes."
    - "PR #809 independently accepted the exact unchanged production observer bytes at exact head before merge."
  derived:
    - "The stable validator bundle does not include the observation harness or its test."
    - "A three-file rebind is coherent without predecessor-byte reconstruction when current fail-closed tests and direct owner-API topology tests remain exact."
  proposed:
    - "Reuse the existing harness and test with one test-only bridge consumer, inherit PR #809 historical acceptance, and retain current synthetic-only app-native validation."
  unknown:
    - "Whether independent review will find any deterministic fourth-path consumer."
  authority_conflicts_found: false

workflow_handoff:
  role_performed: "Codex B: Narrow R0 Predecessor-Acceptance Evidence Contract Reconciler"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/826"
  parent: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  historical_predecessor: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  base_commit: "f5eda24457527dcc603c6d3900ac7cf527c0f046"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/826"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_offline_observation_1_lifecycle.md"
  risk_tier: "high"
  harness_decision: "reuse_existing_harness_with_one_test_only_bridge_consumer"
  historical_acceptance_evidence: "PR #809 exact-head review inherited; no predecessor-byte reproof"
  finding_status:
    ME-RP-826-E-002: "contract_corrected_pending_independent_confirmation"
  implementation_path_count: 3
  stable_validator_bundle_sha256: "be432ceab519e42fc688800c2cda1b172845abb329acc942ba11c5a5490826ca"
  observation_identity_created: false
  implementation_authorized: false
  observation_authorized: false
  receipt_publication_authorized: false
  observation_2_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: Independent App-Native R0 Observation 1 Lifecycle Contract Reviewer"
```
