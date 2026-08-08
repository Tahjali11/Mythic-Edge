# Stable Two-Line R0 Release Reconstruction Contract

## Contract Status

| Field | Value |
| --- | --- |
| Repository | `Tahjali11/Mythic-Edge` |
| Issue | [#819](https://github.com/Tahjali11/Mythic-Edge/issues/819) |
| Parent | [#813](https://github.com/Tahjali11/Mythic-Edge/issues/813) |
| Tracker | [#746](https://github.com/Tahjali11/Mythic-Edge/issues/746) |
| Protected issue | [#769](https://github.com/Tahjali11/Mythic-Edge/issues/769) |
| Authoritative starting base | `origin/main@0aa3905ac95e886cd3b3205ba34fbd1ca6b99f26` |
| Starting tree | `68b95dcb385fe8fab573cb47a1f34321f03956b3` |
| Contract version | `role_pool_codex_app_native_r0_release_state_stable_reconstruction.v1` |
| Risk tier | `High` |
| Active lane | Existing issue #819 only |
| Contract implementation authorized | `false` |
| Test reconstruction authorized | `false` |
| Release reconstruction authorized | `false` |
| Owner decision created or consumed | `false` |
| Observation authorized | `false` |
| Task, claim, or dispatch authorized | `false` |
| R0-R8 advancement authorized | `false` |
| Retired legacy Stage 4 authorized | `false` |
| Submission, merge, or deployment authorized | `false` |
| Live ready | `false` |

This contract defines a later staged reconstruction route. It does not perform
any stage, change release state, refresh the authority index, consume an owner
decision, or authorize implementation, integration, execution, or readiness.

## Intended Behavior, Actual Behavior, First Failure, Repair, And Verification

### Intended behavior

The accepted one-line R0 release must remain byte-exact while the three test
consumers are made stable before a successor validator bundle is computed. A
later, separately authorized release attempt may then append exactly one fresh
19-field `trusted_owner_native_release_rebaseline_record.v1` line that binds
that stable bundle. The resulting chain has exactly two records, selects the
new line as the current tip, and remains at `R0` with every operational and
advancement effect false.

### Actual behavior

The accepted `origin/main` release is still the immutable 981-byte one-line
chain. The prior local two-line candidate is unsubmitted retired evidence. Its
tests were changed after candidate construction and bind mutable complete
artifacts and downstream test hashes. Recomputing any bound input therefore
changes another input that was already embedded upstream.

### First proven failure point

`ME-RP-819-E-003` is blocking. The current bundle algorithm includes the exact
SHA-256 of `tests/test_check_role_pool_r0_bootstrap.py`. The retired bootstrap
test pins the complete two-line release artifact. That release's second line
embeds the validator-bundle SHA-256. The offline-observation test then pins the
bootstrap-test successor hash and the mutable release and authority-index
hashes, while the trusted-launch-observer test pins the offline-observation-test
successor hash.

The deterministic cycle is:

```text
bootstrap-test bytes
  -> validator-bundle digest
  -> future rebaseline record
  -> complete release-artifact digest
  -> bootstrap-test bytes
```

The offline-observation and trusted-launch-observer test pins extend the
rebuild chain downstream. Hardcoding `c344058d...`, changing one more digest
literal, rewriting the spent record, or adding a third line does not remove
the cycle.

### Exact contracted repair

Reconstruct only the three test consumers so their final bytes contain no
future complete release digest, future authority-index digest, future record
self-digest, future bundle digest, or changing downstream test-file digest.
Tests must instead use the existing canonicalization, self-digest, record,
chain, current-tip, and bundle rules to derive candidate facts mechanically.
Historical fixtures and current-state projections must be separate and
fail-closed. No production code or validator behavior changes.

After independent review and integration freeze the three test files, compute
the stable successor bundle once with the unchanged bundle algorithm. Only
after a fresh exact-base Codex E eligibility review and a separate fresh owner
decision may one clean two-line candidate be constructed from the accepted
one-line release.

### Verification

Verification must prove the dependency graph is acyclic before any owner
decision exists; freeze all three test byte counts and hashes; recompute the
bundle from the frozen inputs; prohibit any later bundle-input edit; validate
the immutable first line and synthetic/current two-line chains through the
existing validators; and, after a future candidate exists, prove exact
two-record state, current-tip ownership, the R0 ceiling, zero effects, and all
false authority flags.

## Explicit Owner Supersession And Expiry

The initiating owner prompt is a narrow `explicit_user_override` inside the
existing #819 lane. It supersedes only the prior #819 no-retry/no-replacement
boundary enough to authorize this Codex B contract-writing pass and select the
fresh no-new-schema reconstruction route.

The owner selects and binds these decisions:

1. use the existing `trusted_owner_native_release_rebaseline_record.v1` schema;
2. construct from the accepted one-line release on a later exact clean base;
3. do not create a third release event;
4. do not create a second rebaseline mechanism;
5. do not create a correction-record schema;
6. do not expand the R0 lifecycle;
7. treat the prior local two-line candidate as retired evidence only; and
8. keep the prior owner decision permanently spent and nonreusable.

This override expires when the Codex B handoff in this contract is complete.
It creates no C, D, E, F, or G authority; no implementation, append,
submission, merge, observation, task, claim, dispatch, rung, retired legacy Stage 4,
deployment, or readiness authority; and no authority to mutate GitHub. Issue
#819 remains the single existing active lane. No parallel lane is created.

## Current Accepted Bindings

These values were refreshed from the exact starting base:

| Artifact | Bytes | SHA-256 or self-digest |
| --- | ---: | --- |
| `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` | 981 | `723b1faeef731d9c526cdf9c19bfc2546b08d3eca94d4ee79eb62a5370f719c9` |
| Immutable first-record self-digest | N/A | `78bff761396daaa72b0bd27ac1a799f5c01f5815f902a37ca84a024f5e4a9ba7` |
| `docs/role_pool_current_authority_index.md` | 15,479 | `2a4b4629c2faaa77f1c8f65d0f8f2c6c42aef8f34fc57ab4164fbb84d5579de0` |
| `tests/test_check_role_pool_r0_bootstrap.py` | 59,999 | `6378c9af6ffba7e8692b3f3653a722cbdb835ae5bcf9b86bdb4098691839dbdb` |
| `tests/test_check_role_pool_r0_offline_observation.py` | 65,511 | `8201a348b563b80fb7018851680adf44313e60ce583b944a528be2cfb4b3d60f` |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | 41,286 | `fe9a1f3773d1f5fcdbb17f611c0dbb992866c8bd78d26f92eaaf359d22dbfd23` |
| Current derived validator bundle | 788-byte canonical preimage | `c344058dfc2738d891cd63f67411203aac56073c824b3f3de14b992498972e5d` |

The unchanged bundle algorithm currently derives `c344058d...` from checker
SHA-256 `897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a`
and bootstrap-test SHA-256 `6378c9af...9dbdb`, together with the existing
ordered bundle fields. The production bootstrap checker observes the accepted
one-line chain as `present_valid_chain` and selects
`blocked_release_state_conflict`; its five effect counts are zero and every
authority flag is false.

Issue #769 was refreshed as open with zero comments. Any change to that state
is a hard stop.

## Retired Evidence Inventory

The following unsubmitted local #819-C artifacts are immutable historical
evidence only:

| Retired evidence | SHA-256 or identity |
| --- | --- |
| Complete two-line release artifact | `d2e621a5274e77325bd0280b9cf16258daa09034f1aacde4e322bb43a64cf83e` |
| Retired candidate tip and record self-digest | `3d4bebc4e73e9b33f5e425cf07b947112f76597e9358abdc8cdb2732849fb841` |
| Authority index | `8a39f41432bad54c7f39a8f914312cdfeb92771bb2a10e5b4e03c7dff8f07ad2` |
| Bootstrap test | `1c4a82fc855723f236760827426a80bcc4c63a75d74b23e073d81ff89e93c657` |
| Offline-observation test | `2e2996997a8312e2d3ef610248badb6e1dcb1f1aebeae7baeea19d4abd1e1561` |
| Trusted-launch-observer test | `1ef5b8bbf26e8a9e9bd1988c54f41038050650c0e64f8c66862b849657c77792` |
| Implementation handoff | `57b377c3c3ec0692dca745883b1009f1165b14c2634af621559871624576ee69` |
| Spent record ID | `r0.rebaseline.bbf9d180a617495a93c253c91ccfde01` |
| Spent owner decision | [issue comment 5226864364](https://github.com/Tahjali11/Mythic-Edge/issues/819#issuecomment-5226864364) |

These artifacts and the spent decision must never be submitted, committed,
merged, installed, relabeled as current release state, copied into the clean
candidate, rewritten, or cited as implementation authority. The spent record
ID is unavailable forever. The retired worktree must not be continued,
cleaned, reset, staged, committed, or otherwise mutated under this contract.

## Owning Truth Layer And Interfaces

This is workflow-governance and deterministic test-fixture work. Parser truth
is not involved.

- `docs/contracts/trusted_owner_native_role_pool_profile.md` owns the accepted
  release schemas, R0 rebaseline constraints, and R0-R8 ceiling vocabulary.
- `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` owns
  canonical release-record self-digests, schema validation, chain validation,
  current-rung selection, and current-tip binding derivation.
- `tools/check_role_pool_r0_bootstrap.py` owns the read-only prerequisite
  projection and the existing validator-bundle algorithm.
- `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` owns the
  repository's accepted release-chain state.
- `docs/role_pool_current_authority_index.md` is a derived, manually refreshed
  authority index. It does not override the release chain, validators, issue,
  review, or owner authority.
- The three permitted test files own test fixtures and assertions only. Test
  literals, mocks, and AI interpretation are not release authority.

The existing public interfaces remain unchanged:

- `validate_trusted_native_release_record`;
- `validate_trusted_native_release_rebaseline_record`;
- `validate_trusted_native_release_state_record`;
- `validate_trusted_native_release_chain`;
- `trusted_native_current_rung`;
- `trusted_native_current_release_bindings`;
- `trusted_native_self_digest` and `trusted_native_canonical_bytes`; and
- `_validator_bundle(checker_sha256, checker_test_sha256, pool)`.

No schema, signature, status, selector, KAT, bundle family, release path,
writer, checker, observer, launcher, or lifecycle behavior may change.

## Deterministic Consumer Audit And Scope Reconciliation

The inspected executable consumers are classified as follows:

| Consumer | Deterministic dependency | Contract disposition |
| --- | --- | --- |
| `tools/check_role_pool_r0_bootstrap.py` | Reads release state; hashes its checker and bootstrap test into the existing bundle | Production owner; unchanged |
| `tests/test_check_role_pool_r0_bootstrap.py` | Exercises release parsing, chain, tip, drift, and bundle behavior | Stage 1 permitted |
| `tools/check_role_pool_r0_offline_observation.py` | Carries historical release, bundle, bootstrap-test, validator, and authority-index bindings | Historical fail-closed production consumer; unchanged |
| `tests/test_check_role_pool_r0_offline_observation.py` | Exercises those frozen bindings and repository nonmutation | Stage 1 permitted |
| `tools/run_role_pool_r0_trusted_launch_observer.py` | Pins the historical offline-observation owner/test bundle | Historical fail-closed production consumer; unchanged |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | Exercises exact binding rejection and trusted-launch behavior | Stage 1 permitted |
| `tools/run_role_pool_r0_direct_interpreter_preflight.py` | Pins a retired historical offline-observation harness/test | Inspected downstream old-world gate; unchanged and out of scope |
| `tools/check_role_pool_r0_prelaunch_gate_matrix.py` | Pins historical owner, owner-test, observer, and observer-test bytes | Inspected downstream old-world gate; unchanged and out of scope |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py` | Exercises the release schema and chain validators | Existing aggregate validator test; unchanged |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_skill_contract.py` | Checks the canonical release path in the installed-skill contract | Existing path consumer; unchanged |
| `docs/role_pool/trusted_owner_repository_registry.v1.json` | Declares the canonical release path | Data binding only; unchanged |

The direct-interpreter preflight and prelaunch matrix are additional executable
consumers, but their deliberately older frozen bindings are already fail-closed
historical gates. They are not bundle inputs and do not close the circular
edge. This contract does not refresh or reactivate them. If implementation,
review, or aggregate validation concludes that either executable must accept
the reconstructed test bytes for #819 acceptance, stop and route to Codex B
scope reconciliation. Do not widen Stage 1.

Repo-wide exact-reference inspection also includes the accepted profile and
#819 contract, registry, current authority index, and historical contracts,
reviews, and handoffs that record predecessor release/index/bundle digests.
Those documentation records are evidence or governing prose, not executable
bundle inputs. They remain unchanged in Stage 1 and must not be rewritten to
hide drift. Stage 2 must classify every exact-reference match as an active
executable edge, immutable historical evidence, current derived index content,
or governing contract binding.

The Stage 2 audit must repeat this inventory repo-wide. Any newly discovered
executable consumer that would require an edit is a stop condition, not
permission to add a path.

## Stage 1: Stable Test Reconstruction

Stage 1 may be implemented only after this contract is independently accepted,
integrated under separate authority, and a separately activated Codex C pass
exists. The only possible changed paths are:

1. `tests/test_check_role_pool_r0_bootstrap.py`;
2. `tests/test_check_role_pool_r0_offline_observation.py`; and
3. `tests/test_run_role_pool_r0_trusted_launch_observer.py`.

### Required stable-fixture design

1. Preserve the exact 981-byte historical first line as the only immutable
   release-byte fixture. Verify its SHA-256, final LF, no CR, schema, field
   order, canonical self-digest, and record ID through the existing rules.
2. Separate historical fixtures from current-state projections. Historical
   tests must use the immutable first line or explicit synthetic marker bytes;
   they must not slice a future current release to recover history.
3. Construct any synthetic rebaseline record from an explicit ordered
   18-field preimage and compute `record_sha256` with
   `trusted_native_self_digest`. Serialize with
   `trusted_native_canonical_bytes`; never insert a mutable complete-artifact
   digest as the record self-digest.
4. Derive current release facts by strict parsing and the existing record,
   chain, current-rung, and current-binding helpers. Current production bytes
   may match only the exact immutable one-line state or an exact valid
   two-line state satisfying this contract. Arbitrary bytes, extra lines,
   alternate second records, malformed JSON, duplicate keys, missing final LF,
   CRLF, partial lines, stale predecessors, forks, duplicate IDs, wrong tuples,
   wrong self-digests, and second rebaselines must fail closed.
5. Derive the expected successor validator bundle at runtime with the existing
   bundle algorithm over the actual frozen checker and bootstrap-test bytes.
   No future bundle digest literal may occur in any of the three test files.
6. Compare a candidate current-tip tuple mechanically. The predecessor tuple
   must come from the validated immutable first record. The successor profile,
   source/install tree, and registry values remain exact accepted bindings;
   the successor bundle is the runtime-derived stable bundle. The rung must be
   `R0` and observations must remain empty.
7. For historical production constants in the offline-observation and trusted
   launch surfaces, use path- and payload-bounded synthetic fixtures or dynamic
   comparisons to the production owner's frozen constant. Do not hardcode the
   changing successor hash of another test file.
8. A path-bound digest shim, if retained, must activate only for one named
   synthetic path and one exact marker payload. The same bytes at another path,
   different bytes at the allowed path, or ordinary hashing outside that one
   pair must use the real SHA-256 and fail when appropriate.
9. Authority-index tests must use semantic invariants, dynamic before/after
   nonmutation comparison, or an exact path-and-marker-bounded historical
   fixture. They must not pin the mutable complete index digest and must not
   treat arbitrary index bytes as accepted.
10. Preserve exact schema-aware validation, release-chain validation,
    mechanically derived current-tip comparison, R0 ceiling checks,
    historical/current separation, all negative and drift cases, fail-closed
    behavior, zero effect counts, and every false authority field.

### Forbidden test dependencies

The final bytes of all three tests must be independent of:

- the mutable complete release-artifact digest;
- the mutable complete current-authority-index digest;
- a future rebaseline record self-digest;
- a future validator-bundle digest;
- another affected test file's changing successor digest; and
- the retired candidate, spent record ID, or spent owner decision as authority.

The tests may retain the immutable 981-byte first-line digest and immutable
first-record self-digest. They may dynamically hash current files, but they
must not encode a future result back into their source bytes.

No production validator, checker, observation owner, launcher, preflight,
matrix, schema, KAT, lifecycle, status vocabulary, authority behavior, contract,
release artifact, index, handoff, registry, or installed skill may change in
Stage 1.

## Stage 2: Freeze And Bundle Computation

Stage 2 begins only after Stage 1 implementation is complete and stops on the
first changed input.

1. Run focused validation for each of the three final test files, then run
   them together with the existing record, rebaseline, chain, current-tip,
   observation, and trusted-launch-observer coverage.
2. Independently freeze and record the exact byte count and SHA-256 of all
   three final test files. The implementer and independent reviewer must
   calculate them separately from ordinary non-reparse files.
3. Perform a repo-wide deterministic consumer audit for release/index paths,
   bundle fields and algorithms, all three test paths, and every old and new
   exact digest. Produce a directed dependency inventory and prove no path
   returns from a bundle input through release, index, or a downstream test to
   that bundle input.
4. Compute the successor validator bundle only with the unchanged existing
   algorithm and its existing ordered fields. The algorithm directly consumes
   the checker and final bootstrap-test hash; the final offline-observation and
   trusted-launch-observer hashes are separately frozen review bindings and
   must not be added to the bundle schema.
5. Record the stable bundle, its exact canonical preimage byte count, the
   checker hash, and all three frozen test hashes in review and handoff
   evidence.
6. After bundle computation, do not edit any bundle input or any of the three
   frozen tests. Any byte change invalidates the freeze and requires a fresh
   Stage 1 implementation/review/integration cycle before a new Stage 2
   computation. It does not authorize a literal update.

Do not add a schema, bundle field or family, release file, validator, KAT,
persistent writer, or lifecycle event.

## Stage 3: Fresh Review And Owner Authority

Exact clean-base review requires integration. The accepted reconstruction
contract and independently accepted Stage 1 three-test package must be
integrated into `origin/main` first under separate F/G authority. The release
artifact on that integrated base must still be exactly the accepted 981-byte
one-line chain. The authority index must still be the accepted predecessor
index. No retired-candidate bytes may be present.

Only then may a fresh public-safe Codex E eligibility review bind all of:

1. exact `origin/main` commit and tree;
2. accepted integrated reconstruction-contract path and SHA-256;
3. final byte counts and SHA-256 values for all three Stage 1 tests;
4. checker hash, stable bundle canonical-preimage byte count, and stable
   validator-bundle SHA-256;
5. immutable predecessor release artifact SHA-256, 981-byte count, exact first
   line, and tip self-digest;
6. successor profile `8f885d...a71952`, source/install tree
   `3aadf0...717d6`, and registry self-digest `93a29e...d69a7`;
7. source/install equality and exact registry artifact;
8. zero prior accepted rebaseline records on the reviewed clean base;
9. no accepted successor-profile R0 observation;
10. exactly one future rebaseline event required and no third event required;
11. the complete repo-wide consumer inventory and no remaining circular edge;
12. exact reconstruction Stage 4 three-path scope;
13. #769 open with zero comments; and
14. every implementation, release, observation, task, claim, dispatch,
    advancement, retired legacy Stage 4, submission, merge, deployment, and readiness flag
    false.

Only after that review may the owner publish a separate fresh, expiring,
single-use, nonreusable decision authorizing exactly one new candidate attempt.
The decision must bind the exact reviewed main commit/tree, contract, review,
three test hashes and byte counts, stable bundle, predecessor and successor
tuples, exact three-path reconstruction Stage 4 scope, one fresh unused `r0.rebaseline.*`
record ID, one append-call entry, and no retry or replacement.

The new decision must not cite the retired candidate, retired record ID, or
spent decision as implementation authority. Read-only preflight does not
consume it. It becomes permanently spent immediately before entry into the
sole append call and remains spent for every known, failed, partial, or unknown
result.

## Stage 4: One Clean Two-Line Candidate

Reconstruction Stage 4 may start only from the exact reviewed `origin/main` base whose release
artifact is the accepted one-line state. It is a later release implementation
stage, not authority created by this contract.

“Stage 4” in this heading is only the fourth reconstruction dependency stage.
It is not the retired legacy Stage 4 work and grants no authority for that
work. This contract concerns only stable release binding for the Role Pool
R0-R8 ladder.

The release result must contain exactly:

1. the immutable historical 981-byte bootstrap line; and
2. one fresh canonical 19-field
   `trusted_owner_native_release_rebaseline_record.v1` line.

The second line must use the fresh owner-authorized record ID; name immutable
tip `78bff761...e4a9ba7`; keep `from_rung=R0`, `to_rung=R0`, and
`observation_receipt_sha256s=[]`; preserve the exact four predecessor values;
bind the reviewed successor profile, tree, registry, and stable Stage 2 bundle;
bind only the fresh Stage 3 review and owner decision; use a valid fresh
whole-second UTC time; and compute its self-digest through the existing
canonical rule.

Normal later implementation scope is exactly:

1. `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`;
2. `docs/role_pool_current_authority_index.md`; and
3. `docs/implementation_handoffs/role_pool_codex_app_native_r0_release_state_rebaseline.md`.

No test edit is permitted after the Stage 2 freeze. The release append must
retain exclusive final-tip check, single append-call entry, flush/synchronize,
close, exact full readback, strict two-line parse, record/chain validation,
current-tip derivation, and only-then index and handoff writes.

Collision, changed tip, stale base, duplicate ID, fork, existing second line,
ambiguous append entry, partial write, failed flush, failed close, unreadable
state, failed exact readback, index failure, or handoff failure retains the
existing fail-closed and unknown-outcome behavior. No automatic retry,
replacement, truncation, rollback, repair, second append, or cleanup of
uncertain release bytes is allowed. Later reconciliation is read-only.

Exactly two release records are permitted. A third record, correction record,
second rebaseline, alternate lifecycle event, historical rewrite, truncation,
rollback, replacement, or normalization of the first line is forbidden.

## Validation Requirements

Validation is ordered smallest-first. Exact selections may be expanded by the
independent reviewer, but no failing in-scope check may be waived.

### Focused and aggregate behavior

```powershell
py -3.13 -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py
py -3.13 -B -m pytest -q tests\test_check_role_pool_r0_offline_observation.py
py -3.13 -B -m pytest -q tests\test_run_role_pool_r0_trusted_launch_observer.py
py -3.13 -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_offline_observation.py tests\test_run_role_pool_r0_trusted_launch_observer.py
py -3.13 -B -m pytest -q docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py docs\codex_skills\mythic-edge-role-pool\scripts\test_skill_contract.py
```

The focused selection must cover bootstrap, rebaseline record, release-chain,
current-tip, current-rung, R0 ceiling, observation, and trusted-launch-observer
tests; immutable/current fixture separation; computed candidate self-digests;
one-line and exact two-line states; negative and drift cases; arbitrary-byte
rejection; zero effects; and all false authority flags.

### Consumer, governance, safety, and repository checks

```powershell
rg -n --hidden -g '!frontend/.wrangler/**' -g '!.git/**' "trusted_owner_native_release_state|role_pool_current_authority_index|validator_bundle|test_check_role_pool_r0_bootstrap|test_check_role_pool_r0_offline_observation|test_run_role_pool_r0_trusted_launch_observer" .
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B tools\check_protected_surfaces.py --base origin/main
py -3.13 -B tools\check_secret_patterns.py --all
git diff --check
```

Also require:

- exact changed-path comparison for the active stage;
- no CR bytes, valid UTF-8/ASCII where the existing artifact requires it, and
  one final LF for every changed text artifact;
- no matching Role Pool checker, observer, launcher, preflight, or matrix
  process left running;
- no new `__pycache__`, `.pyc`, `.pytest_cache`, generated receipt, runtime
  state, failed-post, log, or other validation residue;
- #769 live-read as open with zero comments at each stage boundary; and
- `git status --short --branch` with all unrelated residue preserved and
  excluded.

### Full pytest classification

Run the full repository suite only after focused and relevant aggregate checks:

```powershell
py -3.13 -B -m pytest -q
```

Classify every failure at its first observed boundary as in-scope regression,
missing setup, pre-existing failure, repository drift, or unrelated subsystem
failure. Any unrelated analytics failure must be reported separately with its
exact first boundary. It does not authorize another #819 route, does not waive
an in-scope failure, and must not be described as a #819 pass.

## Acceptance Criteria

Acceptance requires deterministic evidence that:

- the three final test files contain no future complete release/index digest,
  future record self-digest, future bundle digest, or changing downstream-test
  digest;
- their fixtures reject arbitrary release and index bytes;
- the exact immutable first line remains 981 bytes with SHA-256
  `723b1fae...f719c9` and self-digest `78bff761...e4a9ba7`;
- existing schema-aware record, chain, current-tip, current-rung, and R0
  ceiling behavior remains unchanged;
- the stable bundle is reproducible after the final three-test freeze and no
  bundle input changes afterward;
- the repo-wide dependency graph has no circular consumer and every additional
  executable consumer remains unchanged and fail-closed;
- the clean reviewed base has exactly one historical record and zero accepted
  rebaselines;
- the future candidate has exactly two valid records and no third event;
- the current tip mechanically owns the reviewed successor profile, tree,
  registry, and stable bundle tuple;
- current rung remains `R0` and observations remain empty;
- all five bootstrap effect counts and all observation/task/dispatch effect
  counts remain zero;
- every observation, task, claim, dispatch, R1-R8, retired legacy Stage 4, submission, merge,
  deployment, and readiness flag remains false; and
- the retired candidate and spent decision remain unsubmitted immutable
  historical evidence only.

Passing tests, a computed bundle, contract acceptance, an eligibility review,
an owner decision, candidate construction, or implementation review is
prerequisite evidence only. None alone grants integration, observation,
advancement, deployment, or readiness authority.

## Stop Conditions

Stop without implementation or release authority if:

- the circular binding cannot be removed within the three Stage 1 test paths;
- production code, validator, checker, observer, launcher, preflight, matrix,
  schema, KAT, bundle, status, or authority behavior must change;
- another executable consumer requires an edit;
- a new schema, release file, lifecycle event, correction record, second
  rebaseline, or third release line is required;
- historical release bytes must change;
- tests must be weakened, made advisory, or allowed to accept arbitrary bytes;
- a stable bundle cannot be computed without editing a frozen input;
- any frozen test or bundle input changes after computation;
- the exact clean base is no longer the one-line accepted release;
- the accepted contract or reviewed base drifts;
- the spent decision or retired record ID would need to be reused;
- the retired candidate would need to be submitted, copied, or rewritten;
- exact exclusive append/readback and unknown-outcome controls cannot be
  retained;
- #769 is not open and comment-free; or
- the work would create observation, task, claim, dispatch, R1-R8, retired legacy Stage 4,
  deployment, or readiness effects.

## Authority And Non-Claims

```yaml
contract_writing_authority_expired_at_handoff: true
test_reconstruction_authorized: false
release_reconstruction_authorized: false
authority_index_mutation_authorized: false
owner_decision_created_or_consumed: false
spent_owner_decision_reusable: false
retired_candidate_current: false
observation_authorized: false
task_authorized: false
claim_authorized: false
dispatch_authorized: false
r0_r8_advancement_authorized: false
stage4_authorized: false
stage4_label: "retired_legacy_stage4"
submission_authorized: false
merge_authorized: false
deployment_authorized: false
registry_mutation_authorized: false
installed_skill_mutation_authorized: false
network_mutation_authorized: false
security_assurance_claimed: false
privacy_assurance_claimed: false
correctness_assurance_claimed: false
release_ready: false
live_ready: false
```

This contract does not claim that the future test reconstruction, bundle,
candidate, index, or release will succeed. It does not claim operational,
security, privacy, correctness, deployment, production, or live readiness.

## Unresolved Risks

- Stage 1 implementation technique remains subject to independent review; a
  path-bound fixture can itself be unsafe if it is not exact-path and
  exact-payload bounded.
- The two additional old-world executable consumers intentionally remain
  drifted and fail-closed. Any future request to reactivate them is separate
  protected work.
- Final Stage 1 byte counts, hashes, and stable bundle do not exist until a
  separately authorized implementation and review complete.
- A full repository suite may expose unrelated analytics or setup failures;
  those require separate classification and authority.
- All live GitHub, base, release, and #769 bindings may drift before a later
  stage and must be refreshed rather than assumed.

## Next Workflow Action

Next role: fresh independent Codex E contract review only.

### Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: #819 Stable Two-Line R0 Release Reconstruction Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/819
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769
Authoritative starting base:
origin/main@0aa3905ac95e886cd3b3205ba34fbd1ca6b99f26

Review only:
docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md

Use the exact contract SHA-256 and byte count from the Codex B handoff. Refresh
origin/main, issue #819 and all comments, #769 state/comment count, governance,
the accepted #819 contract, release schema and chain validators, the current
release/index/test hashes, the validator-bundle algorithm, every deterministic
consumer, and the retired local #819-C candidate read-only. Do not publish the
retired worktree's local absolute path.

Independently reproduce ME-RP-819-E-003. Verify that the contract removes the
circular dependency only through the three-test Stage 1 scope, preserves exact
historical/current fixture separation and arbitrary-byte rejection, leaves all
production consumers unchanged, treats the direct-interpreter preflight and
prelaunch matrix as unchanged historical fail-closed consumers, freezes all
three tests before unchanged-algorithm bundle computation, requires integration
before exact clean-base eligibility review, requires a fresh separate owner
decision and record ID, and permits only one later exact two-line candidate.

Verify the retired evidence inventory, explicit owner supersession and expiry,
permitted/forbidden paths, staged dependency order, validation, acceptance,
stop conditions, R0 ceiling, zero effects, and all false authority flags.
Confirm #769 remains open with zero comments and this contract is the only new
repository path.

Do not implement tests or release state, refresh the index, consume an owner
decision, mutate GitHub, stage, commit, push, submit, merge, observe, create a
task/claim/dispatch, advance a rung, enter reconstruction Stage 4, deploy, or
claim readiness.
Lead with findings. Route any contract defect back to Codex B. A clean review
permits only separately authorized contract submission/integration, not Stage
1 implementation.
```

## Instruction Context

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "High"
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
    - "release-state authority"
    - "validator-bundle binding"
    - "current-authority index"
    - "single-use owner decision"
    - "issue #769 zero-comment state"
    - "R0-R8 and retired legacy Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "The owner narrowly superseded only the prior no-replacement boundary for this B contract pass; the spent decision remains permanently nonreusable."
  stop_conditions:
    - "need for any path beyond the contract in B or beyond the three tests in Stage 1"
    - "need for production behavior, schema, KAT, bundle-family, or lifecycle change"
    - "clean one-line base or issue #769 state drifts"
    - "retired evidence or spent authority would need reuse"
```

## Codex B Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: #819 Stable Two-Line R0 Release Reconstruction Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/819"
  parent: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "owner prompt plus issue #819 and accepted origin/main contract"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_release_state_stable_reconstruction.md"
  risk_tier: "High"
  truth_owner: "accepted release schema and chain validators; release JSONL owns current chain state"
  base_branch: "origin/main"
  target_branch: "separately authorized non-production contract branch"
  branch: "not created by this B pass"
  authoritative_base: "0aa3905ac95e886cd3b3205ba34fbd1ca6b99f26"
  authoritative_tree: "68b95dcb385fe8fab573cb47a1f34321f03956b3"
  owner_supersession_scope: "fresh no-new-schema reconstruction route and this B contract pass only"
  owner_supersession_expiry: "this Codex B handoff completion"
  first_proven_failure: "ME-RP-819-E-003 circular self-binding"
  exact_stage_order:
    - "independent E contract review"
    - "separately authorized contract integration"
    - "separately authorized three-test C reconstruction"
    - "independent E test review and Stage 2 freeze"
    - "separately authorized three-test integration"
    - "fresh exact-main E eligibility review"
    - "fresh separate expiring single-use owner decision"
    - "one clean three-path C release candidate"
    - "fresh E candidate review"
    - "separately authorized F/G integration"
  stage1_permitted_path_count: 3
  reconstruction_stage4_permitted_path_count: 3
  retired_record_id: "r0.rebaseline.bbf9d180a617495a93c253c91ccfde01"
  retired_candidate_current: false
  spent_owner_decision_reusable: false
  issue_769_state: "OPEN"
  issue_769_comment_count: 0
  validation:
    - "current base, tree, bytes, hashes, and bundle independently recomputed"
    - "current checker reproduced blocked_release_state_conflict with zero effects and all authority flags false"
    - "repo-wide deterministic consumer inventory completed"
    - "retired candidate inventory inspected read-only"
    - "contract-only validation recorded in Codex B final handoff"
  stop_conditions:
    - "circular edge cannot be removed within three tests"
    - "another executable consumer requires an edit"
    - "production, schema, KAT, bundle, lifecycle, historical bytes, or #769 must change"
    - "clean base is not exact accepted one-line release"
    - "retired candidate or spent decision would need reuse"
  contract_review_only: true
  implementation_authorized: false
  release_append_authorized: false
  owner_decision_created_or_consumed: false
  observation_authorized: false
  task_claim_or_dispatch_authorized: false
  r0_r8_advancement_authorized: false
  stage4_authorized: false
  stage4_label: "retired_legacy_stage4"
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  next_recommended_role: "fresh independent Codex E contract review"
```

## References

- [Issue #819](https://github.com/Tahjali11/Mythic-Edge/issues/819)
- [`docs/agent_constitution.md`](../agent_constitution.md)
- [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md)
- [`docs/templates/module_contract.md`](../templates/module_contract.md)
- [`ADR-0008`](../decisions/ADR-0008-repo-wip-1-lane-activation-policy.md)
- [`role_pool_codex_app_native_r0_release_state_rebaseline.md`](role_pool_codex_app_native_r0_release_state_rebaseline.md)
- [`trusted_owner_native_role_pool_profile.md`](trusted_owner_native_role_pool_profile.md)
