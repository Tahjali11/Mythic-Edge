# Role Pool R0 Direct-Interpreter Identity Characterizer Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: `https://github.com/Tahjali11/Mythic-Edge/issues/795`.
- Parent: `https://github.com/Tahjali11/Mythic-Edge/issues/780`.
- Tracker: `https://github.com/Tahjali11/Mythic-Edge/issues/746`.
- Protected coordination surface:
  `https://github.com/Tahjali11/Mythic-Edge/issues/769`.
- Role: Codex B, R0 direct-interpreter identity characterizer contract writer.
- Base: `origin/main@99658f2a72f08cc93c61414c91a1fdaf6a9bffc2`.
- Branch:
  `codex/role-pool-r0-direct-interpreter-identity-characterizer-contract-795`.
- Risk tier: `high`.
- Source finding: `ME-RP-780-IDCHAR-A-001`.

This contract follows `AGENTS.md`, `docs/agent_rules.yml`,
`docs/agent_constitution.md`, `docs/codex_module_workflow.md`,
`docs/agent_threads/module_contract.md`,
`docs/templates/module_contract.md`, and accepted ADR-0008.

The current user instruction is a task-scoped ADR-0008
`explicit_user_override` for this one docs-only Codex B artifact. Issue #780
is parked after its consumed terminal preflight. Open PRs #374 and #391 are
unrelated. The override is recorded here, expires with this B handoff, and
does not transfer contract-review, implementation, execution, publication,
release, R0, R1-R8, dispatch, Stage-4, submission, merge, deployment, or
readiness authority to a later role.

## Findings And Decision

1. **Observed:** PR #794 merged at base commit
   `99658f2a72f08cc93c61414c91a1fdaf6a9bffc2`. The merged preflight result
   retains one composite field, `top_level_identity_exact`.
2. **Observed:** the current executor sets that field only after prelaunch
   metadata validation, pre-resume image comparison, post-exit image
   comparison, postlaunch metadata validation, and equality of the prelaunch
   and postlaunch metadata snapshots.
3. **Observed:** exceptions during the post-exit image or metadata block are
   reduced to the same composite `false` as a categorical mismatch.
4. **Observed:** the accepted terminal evidence proves only
   `top_level_identity_exact=false`. It does not identify which internal
   predicate failed. The consumed preflight and all of its identities remain
   terminal and nonreusable.
5. **Derived:** changing the preflight or choosing a different identity
   strategy now would guess at the cause. The smallest evidence-producing
   boundary is one separate characterizer that projects the existing internal
   predicates to closed public-safe categories.
6. **Decision:** contract one standalone characterizer and one operation-free
   focused test. It may perform at most one later owner-authorized synthetic
   process operation. It is not a preflight retry and cannot itself repair or
   relax identity.
7. **Observed:** independent review of predecessor SHA-256
   `41b702b9b144d00d4472eb8fb44713d83535b43461b956756f681f2cd3a417ac`
   confirmed the 4000-tuple selector and one-process design, but opened
   `ME-RP-795-E-001` through `E-003` for source-byte ownership, historical
   noncausality, and private `normcase` scope.
8. **Decision:** make the accepted 38-field source result a literal
   contract-owned known-answer vector, without adding an evidence file or
   reconstructing it during future execution.
9. **Decision:** a future characterizer result describes only its own later
   operation. It cannot establish the cause of, rewrite, or supersede the
   accepted historical result.
10. **Decision:** constrain both path operands and both `normcase` products to
    bounded private memory and exact lexical comparison only. No additional
    path operation, identity relaxation, or public projection is introduced.

Finding `ME-RP-780-IDCHAR-A-001` is
`contract_correction_authored_re_review_pending`.
Finding `ME-RP-795-E-001` is
`source_result_owning_bytes_defined_re_review_pending`.
Finding `ME-RP-795-E-002` is
`historical_noncausality_defined_re_review_pending`.
Finding `ME-RP-795-E-003` is
`normcase_private_scope_closed_re_review_pending`.

## Frozen Public Bindings

| Binding | Exact value |
| --- | --- |
| Repository ID | `1235264383` |
| Base commit | `99658f2a72f08cc93c61414c91a1fdaf6a9bffc2` |
| Integrated terminal-fallback PR | `https://github.com/Tahjali11/Mythic-Edge/pull/794` |
| PR #794 reviewed head | `8a6a871fc166821a719ca04c7ae0602d25107bdc` |
| Parent preflight contract SHA-256 | `cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4` |
| Parent preflight contract byte count | `114199` |
| Terminal-fallback review SHA-256 | `8fa95ada34171e0e040acea13de52a87d72138995bbcc8b6dc982fb0ecca3880` |
| Terminal-fallback implementation review SHA-256 | `1e44189d09664c86539bc8e9441bfb2ef8b51199f04b7087333908d1035ac81b` |
| Current preflight executor SHA-256 | `429021301e9aad9958dfafae22fa98665ed75d0f80b241963cc4ecfb97ce97ed` |
| Current preflight executor test SHA-256 | `435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b` |
| Interpreter metadata owner SHA-256 | `001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6` |
| Direct-interpreter binding self-digest | `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333` |
| Accepted source preflight result artifact SHA-256 | `352acfdaf6879d114d983d2635e42b664a093874a54dd0d074d08c9e9f6f6c71` |
| Accepted source preflight result self-digest | `7605ffbb2a6f019a97a73a23a69cd8ec8d0c983e65af37a11c451ed49eb83d91` |
| Accepted source preflight result schema | `trusted_owner_r0_direct_interpreter_preflight_result.v1` |
| Accepted source preflight result field count | `38` |
| Accepted source preflight result artifact byte count | `2243` |
| Accepted source preflight result owning bytes | Exact canonical line in `Canonical Accepted Source Preflight Result` below, plus its one final LF |
| Accepted source preflight result status | `direct_interpreter_preflight_unknown` |
| Accepted source preflight authority disposition | `consumed_exact_nonreusable` |
| Accepted source authority-disposition owner | `https://github.com/Tahjali11/Mythic-Edge/issues/780#issuecomment-5155751558` |
| Accepted source preflight top-level identity | `false` |
| Accepted source preflight parentage known | `true` |
| Accepted source preflight exit status | `nonzero` |
| Accepted source preflight process launch count | `1` |
| Accepted source preflight top-level process count | `1` |
| Accepted source preflight descendant process count | `2` |
| Accepted source preflight descendant attempt detected | `true` |
| Accepted source preflight timed out | `false` |
| Accepted source preflight cleanup confirmed | `true` |
| Accepted source preflight output complete | `true` |
| Accepted source preflight stdout/stderr byte counts | `0/0` |
| Accepted source preflight surviving process count | `0`, owned by the bounded cleanup reconciliation at `https://github.com/Tahjali11/Mythic-Edge/issues/780#issuecomment-5155751558` |

Every named repository artifact must be an ordinary, non-reparse file at the
exact bound base before implementation or execution may become eligible. The
accepted source result is instead owned solely by the literal canonical block
below; it has no separate repository path and must not be searched for,
materialized, or caller-supplied. Its survivor fact is owned by the cited
public cleanup reconciliation because survivor count is not a field in the
38-field result schema. A binding change routes to Codex B. It must not be
accepted as drift, repaired in place, or silently rebound.

Issue #795, parent #780, and tracker #746 must remain open. Issue #769 must
remain open with zero top-level comments. Neither the characterizer nor any
later result may post to, edit, label, close, or otherwise mutate #769.

## Canonical Accepted Source Preflight Result

The single JSON line in this fenced block, followed by exactly one LF and no
other byte, is the contract-owned accepted source-result artifact. The fence
and surrounding Markdown are not artifact bytes.

```json
{"schema_version":"trusted_owner_r0_direct_interpreter_preflight_result.v1","repository_id":1235264383,"issue_number":780,"executor_contract_sha256":"cdf059021cbfbcc6813c8c20b02001d98bf03a7590efa9286fb4b905bad908d4","executor_contract_review_sha256":"8fa95ada34171e0e040acea13de52a87d72138995bbcc8b6dc982fb0ecca3880","parent_contract_sha256":"17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84","parent_review_sha256":"0fd7d921a92fbd58576f053a0e8938d3ae4a0266e9a023b762f933e65aee450f","harness_sha256":"001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6","harness_test_sha256":"3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3","executor_sha256":"429021301e9aad9958dfafae22fa98665ed75d0f80b241963cc4ecfb97ce97ed","executor_test_sha256":"435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b","direct_interpreter_binding_sha256":"2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333","observed_at_utc":"2026-08-02T04:41:26Z","preflight_authority_consumed":true,"public_bindings_exact":true,"private_binding_exact":true,"top_level_identity_exact":false,"parentage_known":true,"exit_status":"nonzero","stdout_byte_count":0,"stderr_byte_count":0,"top_level_process_count":1,"descendant_process_count":2,"descendant_attempt_detected":true,"timed_out":false,"cleanup_confirmed":true,"output_complete":true,"process_launch_count":1,"retry_count":0,"repository_write_count":0,"installed_write_count":0,"network_operation_count":0,"external_effect_count":0,"private_value_emitted":false,"result_status":"direct_interpreter_preflight_unknown","eligible_for_independent_review":true,"authority_flags":{"repository_mutation_authorized":false,"implementation_authorized":false,"publication_authorized":false,"merge_authorized":false,"deployment_authorized":false,"installation_authorized":false,"package_operations_authorized":false,"network_authorized":false,"secrets_authorized":false,"external_isolation_authorized":false,"canary_authorized":false,"stage4_authorized":false,"stage_advancement_authorized":false,"dispatch_authorized":false,"live_ready":false,"trusted_owner_native_profile_ready":false},"result_sha256":"7605ffbb2a6f019a97a73a23a69cd8ec8d0c983e65af37a11c451ed49eb83d91"}
```

Strict parsing must prove exact 38-field order and scalar types, no duplicate
or unknown key, exact nested authority order and all-false values, the parent
result semantics, self-digest
`7605ffbb2a6f019a97a73a23a69cd8ec8d0c983e65af37a11c451ed49eb83d91`,
artifact byte count `2243`, and complete artifact SHA-256
`352acfdaf6879d114d983d2635e42b664a093874a54dd0d074d08c9e9f6f6c71`.
The vector is immutable historical input. Future code reads no separate source
result file and accepts no caller-supplied replacement.

## Module And Truth Ownership

Module: one Windows-hosted, synthetic, public-safe direct-interpreter identity
characterizer.

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership is closed as follows:

- the accepted parent observation module owns the exact interpreter metadata
  structure, binding, ordinary-file checks, stable-file-identity derivation,
  and binding validator;
- the characterizer owns only its one execution's categorical image and
  metadata observations, process lifecycle, and public-safe result;
- the fixed private executable path and raw machine observations remain
  bounded runtime inputs and own no public truth;
- the characterizer result is diagnostic evidence only; and
- fresh independent Codex E review owns acceptance of future implementation
  bytes and, separately, any later executed result.

The characterizer may explain which existing predicate was not established.
It must not declare the current preflight defective, relax exact identity,
select a replacement identity design, or make a failed predicate acceptable.

## Historical Noncausality

The accepted source result is a historical terminal fact about the consumed
2026-08-02 preflight. The future characterizer is a distinct operation with a
fresh authority, time, process, and then-current metadata observations.

Therefore:

- no future category may be described as the cause of the historical
  `top_level_identity_exact=false`;
- an identical future failure category establishes only a repeated category,
  not common causation;
- `direct_interpreter_identity_exact` establishes only that all characterizer
  predicates were exact during the future operation; it does not make the
  historical result exact, accepted, retryable, or erroneous;
- a future mismatch cannot add a field, detail, or diagnosis to the historical
  38-field object;
- the historical authority remains `consumed_exact_nonreusable`, its result
  remains `direct_interpreter_preflight_unknown`, and accepted observation
  count remains unchanged; and
- only a later Codex A strategy reconciliation may compare the two accepted
  evidence objects and propose a next contract. It must label any causal
  explanation `unknown` unless separately proven.

This clause prohibits retrospective reconstruction while preserving the value
of current categorical evidence.

## Scope

The exact later Codex C implementation scope is:

1. `tools/run_role_pool_r0_direct_interpreter_identity_characterizer.py`
2. `tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py`

Both paths must be absent before implementation. No existing preflight,
observation harness, test, contract, registry, release record, installed skill,
or canonical Role Pool source may change in this lane.

The production characterizer may import the accepted metadata owner. It may
not invoke the current preflight executor, alter its result, or add a mode to
it. It must expose no reusable subprocess, launcher, command, identity,
filesystem, network, package, installation, registry, release, or dispatch
interface.

## Exact Input Boundary

A later execution accepts exactly one bounded private input: the absolute path
already bound by a fresh owner characterization decision to the accepted
direct-interpreter binding. The input rules are:

- one UTF-8 line, no BOM, one final LF, and at most 4096 bytes;
- the value is read from a dedicated inherited stdin pipe, never an argument,
  environment variable, ambient configuration, PATH search, registry lookup,
  current interpreter, or prompt;
- the basename is exactly `python.exe` and the path is absolute;
- `py.exe`, WindowsApps aliases, shims, wrappers, shells, alternate
  interpreters, and fallback runtimes are rejected;
- the bounded input buffer is zeroized after the process path has been copied
  into bounded native storage and again on every terminal path; and
- the value must never appear in stdout, stderr, an exception, log, receipt,
  report, process title, repository file, issue comment, or handoff.

The characterizer accepts no caller-selected command, arguments, cwd,
environment, timeout, output limit, category, adapter, retry, or fallback.

## Exact Identity Observations

The characterizer observes five closed facts in this order:

1. `prelaunch_metadata_state`: observe the exact bound executable before
   process creation and validate the complete accepted metadata object.
2. `pre_resume_image_state`: after one suspended `CreateProcessW` succeeds and
   before `ResumeThread`, query the process image and compare it with the bound
   absolute path.
3. `post_exit_image_state`: after terminal process observation and before the
   process handle is closed, query and compare the process image again.
4. `postlaunch_metadata_state`: after terminal process observation, observe a
   second complete metadata object for the bound executable.
5. `metadata_equality_state`: compare the complete prelaunch and postlaunch
   metadata objects for exact object equality.

The complete metadata object is the accepted ordered tuple of runtime
implementation, executable basename, file version, product version, byte
length, file SHA-256, stable ordinary-file identity SHA-256, ordinary-file
state, and reparse-point state. No component may be omitted, substituted,
normalized to a weaker value, or exposed.

Image equality uses the existing parent comparator exactly:
`normcase(queried_image) == normcase(bound_absolute_path)`. Both operands and
both normalized products are private ephemeral values:

- `bound_absolute_path` is exactly the authority-bound absolute input after
  strict one-line decoding; it is not recomputed from cwd or ambient state;
- `queried_image` is exactly the returned slice from one
  `QueryFullProcessImageNameW` call using a 32768-wide-character buffer, with
  returned length from `1` through `32767` and no embedded NUL;
- Windows `ntpath.normcase` semantics are applied exactly once to each string
  in bounded memory; no `abspath`, `realpath`, `resolve`, `expanduser`,
  `expandvars`, basename, prefix, parent, symlink, filesystem, registry, PATH,
  casefold, trim, or caller-selected transformation is permitted;
- comparison is exact string equality of only those two normalized products;
- neither operand, normalized product, length, hash, prefix, suffix, mismatch
  position, or exception is serialized, persisted, logged, or emitted; and
- both products become unreachable on the same terminal cleanup path as the
  other bounded private values. No stronger zeroization claim is made for
  immutable Python strings.

An invalid returned length, embedded NUL, query failure, normalization failure,
or unavailable operand selects the applicable unavailable or ambiguous
category without fallback. Path equality is only one predicate; it does not
substitute for the independently required exact metadata identity. No
basename-only, relaxed, resolved-target, case-sensitive, hash-only, or
best-effort comparison is permitted.

Prelaunch metadata must be exact before process creation. A pre-resume image
mismatch or unavailable observation terminates the suspended process without
resuming it. Later stages then remain `not_reached`.

Postlaunch metadata has only availability state in the public packet. Because
prelaunch metadata is already exact, an available postlaunch object unequal to
the accepted binding is necessarily unequal to the prelaunch object and is
reported through `metadata_equality_state=mismatch`. Conversely, exact object
equality with the exact prelaunch object mechanically establishes exact
postlaunch metadata. This reduction avoids a duplicate, unreachable
postlaunch-mismatch category while still preserving the postlaunch observation
and the equality fact independently.

## Raw State Domains

The selector accepts only these internal categorical domains:

| Field | Closed values |
| --- | --- |
| `lifecycle_evidence_state` | `exact`, `ambiguous` |
| `prelaunch_metadata_state` | `exact`, `mismatch`, `unavailable`, `ambiguous` |
| `pre_resume_image_state` | `not_reached`, `exact`, `mismatch`, `unavailable`, `ambiguous` |
| `post_exit_image_state` | `not_reached`, `exact`, `mismatch`, `unavailable`, `ambiguous` |
| `postlaunch_metadata_state` | `not_reached`, `available`, `unavailable`, `ambiguous` |
| `metadata_equality_state` | `not_reached`, `exact`, `mismatch`, `unavailable`, `ambiguous` |

`unavailable` means the named observation produced no complete, trustworthy
categorical value. `ambiguous` means its state, ordering, ownership, or
reliability cannot be established. No raw error number, exception text,
partial value, or machine identifier is retained.

The temporal consistency grammar is exact:

- a prelaunch failure requires every later field to be `not_reached`;
- a pre-resume failure requires both post-exit fields and metadata equality to
  be `not_reached`;
- post-exit image failure requires postlaunch metadata and equality to be
  `not_reached`;
- postlaunch metadata failure requires equality to be `not_reached`;
- equality is evaluated only after both metadata observations are complete;
- `identity_exact` requires every stage exact or available as appropriate;
  and
- every other combination is inconsistent and selects the ambiguous category.

## Closed Result Categories And Precedence

Exactly one category is selected in this order:

| Precedence | Category | Exact trigger |
| ---: | --- | --- |
| 1 | `direct_interpreter_identity_evidence_ambiguous` | lifecycle evidence is ambiguous; any stage is ambiguous; the temporal grammar is violated; process, output, survivor, termination, or cleanup evidence is not exact; or contradictory raw facts exist |
| 2 | `direct_interpreter_identity_prelaunch_metadata_unavailable` | prelaunch metadata is unavailable and every later stage is `not_reached` |
| 3 | `direct_interpreter_identity_prelaunch_metadata_mismatch` | prelaunch metadata is complete but differs from the accepted binding and every later stage is `not_reached` |
| 4 | `direct_interpreter_identity_pre_resume_image_unavailable` | prelaunch metadata is exact, the pre-resume image is unavailable, and later stages are `not_reached` |
| 5 | `direct_interpreter_identity_pre_resume_image_mismatch` | prelaunch metadata is exact, the pre-resume image mismatches, and later stages are `not_reached` |
| 6 | `direct_interpreter_identity_post_exit_image_unavailable` | all earlier stages are exact, the post-exit image is unavailable, and later metadata stages are `not_reached` |
| 7 | `direct_interpreter_identity_post_exit_image_mismatch` | all earlier stages are exact, the post-exit image mismatches, and later metadata stages are `not_reached` |
| 8 | `direct_interpreter_identity_postlaunch_metadata_unavailable` | both image observations are exact and postlaunch metadata is unavailable |
| 9 | `direct_interpreter_identity_metadata_equality_unavailable` | both metadata objects are complete but exact equality cannot be established |
| 10 | `direct_interpreter_identity_metadata_equality_mismatch` | both metadata objects are complete and unequal |
| 11 | `direct_interpreter_identity_exact` | lifecycle, both image observations, both metadata observations, metadata equality, process topology, output, survivor, and cleanup evidence are all exact |

Precedence is first-applicable only after the temporal consistency grammar is
checked. Ambiguity dominates every known mismatch. A known mismatch never
becomes exact, and a later failure never hides an earlier trustworthy failure.
No selector input may produce zero or multiple categories.

The pure selector audit covers all
`2 * 4 * 5 * 5 * 4 * 5 = 4000` raw tuples. It must prove
`overlap_count=0`, `uncovered_count=0`, and `unreachable_category_count=0`.
Its exact outcome cardinality is one tuple for each of the ten
non-ambiguous categories and 3990 tuples for
`direct_interpreter_identity_evidence_ambiguous`.

## Fixed Process Boundary

The characterizer's sole permitted real operation, under later authority, is
one direct Windows process with the fixed command represented internally as:

`[bound python.exe, "-B", "-c", "pass"]`

The command is contract text only and is not serialized in the result. The
operation must:

1. use direct `CreateProcessW` with `CREATE_SUSPENDED`, no shell, no launcher,
   no PATH lookup, and no alternate process API;
2. use a Core-owned Job Object with active-process limit `1` and
   kill-on-job-close before the single resume;
3. treat the target as the one top-level process and require zero descendants;
4. use the exact repository root as `lpCurrentDirectory` and the existing
   minimal environment that omits credentials, tokens, proxy values, Python
   path overrides, and arbitrary ambient variables; neither value is caller
   selectable or emitted;
5. permit exactly one `ResumeThread` call only after prelaunch metadata,
   pre-resume image, parentage, job assignment, and active-process count are
   exact;
6. permit one launch, no retry, no relaunch, no replacement, and no fallback;
7. use a 30-second execution timeout and a 5-second termination grace;
8. bound captured stdout and stderr independently to 4096 bytes, drain both
   streams through terminal state, and require both exact byte counts to be
   zero for an exact result;
9. account for active-process-limit messages, Job Object accounting,
   parentage, target exit, timeout, termination, and survivors;
10. give every proven-owned handle exactly one close attempt in reverse
    ownership order without short-circuiting later close attempts;
11. delete a process attribute list only if initialization succeeded, exactly
    once; and
12. classify any timeout, descendant, survivor, nonzero or unknown exit,
    output, incomplete drain, failed close, uncertain termination, or uncertain
    cleanup as `direct_interpreter_identity_evidence_ambiguous`.

The characterizer creates no temporary filesystem object. Cleanup means
process-tree termination where required, stream drain, owned-handle closure,
attribute-list disposal, bounded-buffer zeroization, and proof of zero
surviving matching processes. Uncertain cleanup is terminal and nonreusable.

The non-ambiguous categories use exactly these process profiles:

| Categories | Launch/top-level counts | Exit | Output and timeout | Final state |
| --- | --- | --- | --- | --- |
| prelaunch metadata unavailable or mismatch | `0/0` | `not_started` | `0/0`, not timed out; streams vacuously drained | zero descendants and survivors; cleanup confirmed |
| pre-resume image unavailable or mismatch | `1/1` | `nonzero` after bounded termination of the never-resumed target | `0/0`, not timed out; streams drained | zero descendants and survivors; cleanup confirmed |
| post-exit image, postlaunch metadata, or metadata-equality failure; exact identity | `1/1` | `zero` | `0/0`, not timed out; streams drained | zero descendants and survivors; cleanup confirmed |

Only the ambiguous category may carry another truthful cross-field profile.
It is eligible for independent review only when the result is canonical and
public-safe, all known counts are honestly projected, and cleanup and survivor
evidence are exact. Otherwise its result remains terminal but
`eligible_for_independent_review=false`.

## Network And Effect Boundary

The operation is offline and `network_authorized=false`. The characterizer
must not call a network API, read network configuration, or emit network
evidence. This contract does not claim OS-enforced child-network isolation or
complete native child-network observation. The fixed child source is `pass`;
absence of a child-network claim is not permission to change that source or
use a network resource.

The characterizer may not write the repository, installed skill, registry,
release state, filesystem, GitHub, or any external surface. Any observed or
ambiguous write, unexpected process, or persistent residue selects the
ambiguous category and permanently retires the consumed authority.

## Public-Safe Result Schema

The characterizer emits at most one canonical JSON object to stdout and zero
bytes to stderr. The object has exactly these fields in this order:

1. `schema_version`: string, exact value
   `trusted_owner_r0_direct_interpreter_identity_characterization.v1`.
2. `repository_id`: integer, exact value `1235264383`.
3. `issue_number`: integer, exact value `795`.
4. `parent_issue_number`: integer, exact value `780`.
5. `characterizer_contract_sha256`: 64 lowercase hexadecimal characters.
6. `characterizer_contract_review_sha256`: 64 lowercase hexadecimal
   characters.
7. `characterizer_sha256`: 64 lowercase hexadecimal characters.
8. `characterizer_test_sha256`: 64 lowercase hexadecimal characters.
9. `direct_interpreter_binding_sha256`: exact value
   `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333`.
10. `characterization_id`: a predeclared public-safe identifier bound by the
    fresh owner decision.
11. `observed_at_utc`: whole-second UTC timestamp ending in `Z`.
12. `characterization_authority_consumed`: boolean, exact value `true`.
13. `lifecycle_evidence_state`: closed raw value from this contract.
14. `prelaunch_metadata_state`: closed raw value from this contract.
15. `pre_resume_image_state`: closed raw value from this contract.
16. `post_exit_image_state`: closed raw value from this contract.
17. `postlaunch_metadata_state`: closed raw value from this contract.
18. `metadata_equality_state`: closed raw value from this contract.
19. `category`: one exact closed result category.
20. `process_launch_count`: integer in `{0,1}`.
21. `top_level_process_count`: integer in `{0,1}`.
22. `descendant_process_count`: nonnegative integer; exact acceptance requires
    `0`.
23. `exit_state`: one of `not_started`, `zero`, `nonzero`, `unknown`.
24. `stdout_byte_count`: integer from `0` through `4096`.
25. `stderr_byte_count`: integer from `0` through `4096`.
26. `timed_out`: boolean.
27. `streams_drained`: boolean.
28. `cleanup_confirmed`: boolean.
29. `surviving_process_count`: nonnegative integer; exact acceptance requires
    `0`.
30. `private_value_emitted`: boolean, exact value `false`.
31. `eligible_for_independent_review`: boolean.
32. `authority_flags`: the exact closed object below.
33. `result_sha256`: self-digest string.

`authority_flags` has exactly these fields, in this order, all boolean and all
`false`:

1. `characterizer_authorized`
2. `implementation_authorized`
3. `private_path_access_authorized`
4. `preflight_authorized`
5. `observation_authorized`
6. `receipt_publication_authorized`
7. `release_state_mutation_authorized`
8. `installation_authorized`
9. `package_operations_authorized`
10. `network_authorized`
11. `dispatch_authorized`
12. `r1_r8_authorized`
13. `stage4_authorized`
14. `submission_authorized`
15. `merge_authorized`
16. `deployment_authorized`
17. `live_ready`
18. `security_assurance_claimed`

Unknown or duplicate keys, reordered keys, wrong scalar types, noncanonical
numbers, or values outside the closed vocabularies are invalid.

Canonical bytes are UTF-8 without BOM, contain no insignificant whitespace,
use JSON lowercase booleans, preserve the stated key order, and end in exactly
one LF. `result_sha256` is SHA-256 over the canonical object without the final
LF after replacing its own value with 64 lowercase zeroes. The emitted
artifact SHA-256 is computed over the complete canonical object plus final LF
and is reported only by the later handoff.

`eligible_for_independent_review=true` requires exact public and private
bindings, exact authority consumption, one selected category, exact schema and
self-digest, no private output, no unaccounted process or effect, exact stream
drain, exact cleanup, zero survivors, and category-consistent process fields.
It does not require `category=direct_interpreter_identity_exact`.

## No-Echo Projection

Durable or displayed output must never contain a private path, path fragment,
PID, process or thread handle, raw command, environment name or value, raw
Win32 error, exception text, stack trace, account or SID, volume or file
identity, version string, file length, executable digest, credential, token,
machine name, installation root, inventory, or machine-specific value.

Only the closed categorical states, bounded counts, fixed public digests,
timestamps, and false authorities in the result schema may leave bounded
memory. A possible disclosure stops execution, emits no detailed result, and
retires the authority as ambiguous and nonreusable.

## Single-Use Lifecycle

A later characterizer execution requires, in order:

1. accepted Codex E contract review of these exact bytes;
2. independently accepted exact two-file implementation review;
3. integration of only those reviewed bytes;
4. one separate, exact, expiring owner characterization decision bound to the
   contract, contract review, implementation files, direct-interpreter
   binding, fixed command, limits, characterization ID, and issue #795;
5. public-binding and authority validation before private input access;
6. durable atomic consumption on issue #795, exact readback, and permanent
   transition to `consumed_nonreusable` before the first private byte is read;
7. at most one execution and at most one canonical public-safe result; and
8. fresh independent Codex E result review before any strategy decision.

Invalid or expired authority is rejected before consumption. A consumption
collision, failed readback, unknown commit, duplicate marker, or ambiguous
state retires the decision without private input or process entry. After exact
consumption, every failure, timeout, interruption, invalid result, unknown
state, or cleanup uncertainty is terminal and nonreusable. No retry, reuse,
relaunch, replacement identity, nonce search, result repair, or evidence
reconstruction is permitted. A new attempt requires a new issue-scoped owner
decision and whatever successor contract current evidence proves necessary.

No characterizer result is published to issue #769. The characterizer itself
does not publish a result to GitHub or write a durable local receipt; it emits
only the canonical stdout packet for the separately authorized execution role
to route to independent review under issue #795.

## Operation-Free Test Contract

The focused test must import the selector and a fake native adapter without
starting any process, opening the private path, reading an executable,
mutating the filesystem, or using the network.

Required tests are:

1. one exact fixture for each of the 11 result categories;
2. all 36 pairwise conflicts among the nine known non-exact failure
   categories, each selecting the ambiguous category because two distinct
   terminal failure positions cannot coexist in one valid temporal trace;
3. each component's `ambiguous` state overriding every known mismatch;
4. every allowed `not_reached` boundary and representative impossible early,
   late, duplicate, missing, and out-of-order fact combinations;
5. the exhaustive 4000-tuple selector audit with `0/0/0` overlap,
   uncovered, and unreachable-category counts;
6. exact process-adapter call counts of zero or one for every route;
7. proof that prelaunch failures do not call process creation and pre-resume
   failures do not call resume;
8. timeout, termination, output overflow, descendant, survivor, close-failure,
   stream-drain, and cleanup-uncertainty projection to the ambiguous category;
9. canonical 33-field result ordering, scalar types, self-digest, final LF,
   unknown-key rejection, duplicate-key rejection, and negative cross-field
   vectors;
10. no-echo sentinel tests for every prohibited private-value class;
11. exact 18-field all-false terminal authority validation; and
12. rejection of basename-only, relaxed, alternate, shim, shell, fallback,
   second-process, retry, and caller-selected inputs.

Tests may use fixed public placeholder values only. They must not retain or
reconstruct any real machine value or historical private path.

## Acceptance And Validation

Codex C implementation becomes eligible only after independent Codex E accepts
this exact contract. Codex E must confirm:

- all frozen bindings and issue states are exact;
- the embedded source-result line is the sole owning copy, is exactly 2243
  bytes with its final LF, passes the parent 38-field validator, and recomputes
  both bound digests;
- the future operation has no retrospective causal or reclassification effect
  on that source result;
- both path operands and normalized products remain private, bounded,
  ephemeral, lexical-only values;
- the two-file scope is sufficient and no existing runtime path changes;
- every current composite identity input has a public-safe categorical
  projection;
- the postlaunch/equality reduction is mechanically sound and introduces no
  unreachable duplicate category;
- the 4000-tuple selector is deterministic and every category reachable;
- one-process, zero-descendant, timeout, output, cleanup, no-echo, and
  nonreuse boundaries are complete;
- the fake-adapter test requirements execute no operation;
- exact identity has not been weakened; and
- every operational and readiness authority remains false.

Contract validation requires:

- `git diff --check`;
- `py -B tools/check_agent_docs.py`;
- path-scoped protected-surface validation;
- path-scoped secret and private-marker validation;
- strict extraction and validation of the one canonical source-result JSON
  block;
- exact SHA-256 and byte-count recomputation for every frozen artifact;
- issue #795/#780/#746 state and issue #769 zero-comment revalidation;
- proof that only this contract changed;
- matching task-process count `0`; and
- generated residue count `0`.

## Protected Boundaries And Nonclaims

This contract creates no current implementation, private-path access,
characterizer, process, preflight, observation, publication, release-state,
registry, installation, package, network, dispatch, R1-R8, canary, Stage-4,
submission, merge, deployment, assurance, or readiness authority.

An accepted characterizer result does not count as the direct-interpreter
preflight, Observation 1, Observation 2, a release receipt, R0 acceptance, an
R1 decision, rung evidence, deployment evidence, or security/privacy
assurance. It supports only a later Codex A strategy reconciliation. The
consumed #780 preflight remains consumed and nonreusable.

## Next Independent Review Prompt

Use the Mythic Edge agent constitution and `$mythic-edge-workflow`.

Act as Codex E: Independent R0 Direct-Interpreter Identity Characterizer
Contract Reviewer.

Review only
`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer.md`
from the exact Codex B handoff for issue #795. Recompute the contract and all
frozen public bindings. Confirm `ME-RP-795-E-001` through `E-003` against the
embedded 2243-byte canonical source result, the historical noncausality
clause, and the bounded private lexical `normcase` rule. Also confirm the
standalone two-file scope, exact identity semantics, closed five-stage raw
observation model, deterministic 11-category selector, 4000-tuple `0/0/0`
audit requirement, one-process and zero-descendant boundary, bounded output
and cleanup lifecycle, single-use consumption, no-echo schema, operation-free
fake-adapter tests, issue #769 protection, and all false authority fields.

Reject any preflight retry, existing-runtime edit, relaxed identity,
machine-value output, second process, shell or fallback, dynamic command,
runtime selection or installation, child-network assurance claim, result
publication by the characterizer, R0/R1-R8/Stage-4 authority, or scope beyond
the exact two future implementation paths. Do not implement or execute the
characterizer, access a private path, consume authority, publish a result,
modify GitHub or release state, or route to Codex D.

If exact, create one contract-test report, report
`ME-RP-780-IDCHAR-A-001=contract_exact_characterizer_ready_for_owner_implementation_decision`,
report `ME-RP-795-E-001` through `E-003` as `fixed_confirmed`, and route to a
separate owner implementation decision followed by Codex C.

## Instruction Context

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
    - "private direct-interpreter path and raw identity"
    - "single-use process, timeout, and cleanup lifecycle"
    - "consumed #780 preflight and immutable observation identities"
    - "issue #769 zero-comment boundary"
    - "R0, R1-R8, Stage-4, deployment, and readiness authority"
  authority_conflicts_found: false
  authority_conflict_notes: "The owner instruction is a task-scoped explicit_user_override for this one B contract and expires at handoff."
  stop_conditions:
    - "current base, issue, PR, or frozen artifact binding drift"
    - "need to access, infer, retain, or emit a private path or raw identity"
    - "need to change an existing implementation, test, contract, release, registry, or installed path"
    - "need for more than one process, a relaxed identity rule, shell, fallback, or runtime installation"
    - "issue #769 comment or protected-state mutation"
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Consolidated Narrow R0 Identity Characterizer Contract Corrector"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/795"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  base_commit: "99658f2a72f08cc93c61414c91a1fdaf6a9bffc2"
  branch: "codex/role-pool-r0-direct-interpreter-identity-characterizer-contract-795"
  contract_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer.md"
  source_finding: "ME-RP-780-IDCHAR-A-001"
  finding_status:
    ME-RP-780-IDCHAR-A-001: "contract_correction_authored_re_review_pending"
    ME-RP-795-E-001: "source_result_owning_bytes_defined_re_review_pending"
    ME-RP-795-E-002: "historical_noncausality_defined_re_review_pending"
    ME-RP-795-E-003: "normcase_private_scope_closed_re_review_pending"
  source_result_artifact_sha256: "352acfdaf6879d114d983d2635e42b664a093874a54dd0d074d08c9e9f6f6c71"
  source_result_self_digest: "7605ffbb2a6f019a97a73a23a69cd8ec8d0c983e65af37a11c451ed49eb83d91"
  source_result_byte_count: 2243
  historical_causality_claim: "none"
  normcase_scope: "two_private_ephemeral_lexical_operands_only"
  future_implementation_scope: "exact_two_new_files"
  identity_category_count: 11
  raw_selector_tuple_count: 4000
  process_execution_limit: 1
  process_executed: false
  private_path_accessed: false
  current_authority_all_false: true
  implementation_authorized: false
  characterizer_authorized: false
  preflight_authorized: false
  observation_authorized: false
  receipt_publication_authorized: false
  release_state_mutation_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  owner_implementation_decision_eligible: false
  generated_residue_count: 0
  next_recommended_role: "Codex E: independent R0 direct-interpreter identity characterizer contract reviewer"
```
