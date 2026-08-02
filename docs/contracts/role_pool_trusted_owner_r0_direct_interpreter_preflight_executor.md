# Role Pool R0 Direct-Interpreter Preflight Executor Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: `https://github.com/Tahjali11/Mythic-Edge/issues/780`.
- Parent: `https://github.com/Tahjali11/Mythic-Edge/issues/776`.
- Tracker: `https://github.com/Tahjali11/Mythic-Edge/issues/746`.
- Protected coordination surface:
  `https://github.com/Tahjali11/Mythic-Edge/issues/769`.
- Role: Codex B, narrow R0 terminal-stage and consumption fallback contract
  writer.
- Base: `origin/main@9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a`.
- Branch:
  `codex/role-pool-r0-terminal-fact-contract-780`.
- Risk tier: `high`.
- Source finding: `ME-RP-780-PREFLIGHT-TERM-B-001`.

This contract follows `AGENTS.md`, `docs/agent_rules.yml`,
`docs/agent_constitution.md`, `docs/codex_module_workflow.md`,
`docs/agent_threads/module_contract.md`,
`docs/templates/module_contract.md`, and accepted ADR-0008.

The current user instruction is a task-scoped ADR-0008
`explicit_user_override` for this one docs-only Codex B artifact. Issue #780
is the active lane. Open PRs #374 and #391 remain unrelated. The override is
recorded here, expires at this B handoff, and grants no implementation,
private-path observation, process, preflight, observation, publication,
release, submission, merge, deployment, Stage-4, or readiness authority.

## Findings

1. **Observed:** PR #791 merged the accepted direct-interpreter successor and
   its reviewed two-file implementation into `main` at
   `3c3b4bfa7ddcd066d54b8b17ca9f3d496919d23f`.
2. **Observed:** the merged harness provides exact two-handle interpreter
   metadata validation, the closed preflight selector, and public-safe result
   classification. It intentionally does not create a real process.
3. **Observed:** the supplied post-merge prevalidator handoff reports
   `public_path_binding_status=exact`,
   `stable_identity_revalidated=false`, and
   `preflight_status=blocked_missing_reviewed_operational_executor`. It also
   reports no approval consumption, process launch, repository mutation, or
   GitHub mutation.
4. **Derived:** the first current failure is not another interpreter-binding
   or harness defect. It is the absence of a reviewed owner for the single
   permitted `CreateProcessW` call, target process handle, descendant
   observation, timeout, output capture, and cleanup lifecycle.
5. **Decision:** add one dedicated Core-owned preflight executor and one
   focused test. Reuse the accepted harness as the sole owner of binding and
   outcome semantics. Do not add a general launcher, subprocess capability,
   observation executor, broker, service, package, or fallback.
6. **Authority disposition:** the supplied prevalidator handoff is routing
   evidence, not a durable authority object. Its unconsumed approval may be
   used later only if its exact terms already bind this accepted contract,
   the future contract-review artifact, and the exact independently reviewed
   executor bytes. Otherwise a fresh owner preflight decision is required.
7. **Observed:** independent review of predecessor SHA-256
   `4c835147d2ddab0b2855c27f86d45b6cb69dd65a372f5124fde236d9785c0e0d`
   opened `ME-RP-780-PREFLIGHT-EXEC-E-001` through `E-003`: the stdin handle
   was invalid, the ambient-job decision was not closed, and terminal result
   cross-fields were underconstrained.
8. **Decision:** close all three findings in this artifact without adding a
   path, process, authority field, public status, retry, or fallback.
9. **Observed:** follow-up review of SHA-256
   `c3f7da7ac3d64dac3d9c7ff54e5fdb8ce181a7eaafcdd106f003ee4d4c08fac0`
   confirmed `E-001`, narrowed `E-002` to the incorrect native UI member, and
   proved `E-003` still overlapped on missing source facts and left the
   descendant-plus-timeout state uncovered.
10. **Decision:** preserve the fixed stdin lifecycle, use the exact native
    `UIRestrictionsClass` scalar, remove `projection_id` from source input,
    and derive co-occurring failure precedence exactly from the accepted
    parent classifier.
11. **Observed:** second follow-up review of SHA-256
    `77e8867d76db9599d556d043c26a32eb7e882955b898b61887621c59b6fe95f5`
    confirmed `E-001` and `E-002` but identified one representable local setup
    failure after ambient admission and before `CreateProcessW` entry that the
    seven-route source grammar omitted.
12. **Decision:** preserve the `CreateProcessW`-entry consumption point and add
    one exact pre-create setup-failure state, canonical unknown projection,
    and terminal unconsumed-nonreusable owner-decision disposition. No new
    public status, schema field, process, retry, or fallback is required.
13. **Observed:** independent contract review accepted SHA-256
    `d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848`
    exactly. The accepted review artifact is 26,523 bytes at SHA-256
    `97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038`.
14. **Observed:** independent implementation review of the exact two-file
    candidate opened `ME-RP-780-PREFLIGHT-EXEC-E-004` and `E-005`. The review
    artifact is 16,673 bytes at SHA-256
    `49d66f9ce38f0fab01bbeebf02deba4451f87f45600a21552b47a3e9292e0dac`.
15. **Observed:** retained Codex G evidence establishes that the prior harness
    exited `0`, emitted the exact expected receipt bytes with empty stderr, and
    first failed only at the outer zero-descendant predicate. No process,
    residue, receipt, or reusable identity survived. No child-network failure
    was recorded by that retained evidence.
16. **Observed:** rejected contract SHA-256
    `bcc6a7e6e32b76503de9fdb42dcc95cb3cfce0720f7d3662cec005f9d969eefd`
    introduced complete child-network evidence as a new eligibility gate. The
    owner rejects that expansion and directs this contract to remain about the
    exact direct-interpreter process topology, cleanup, and owned local-effect
    evidence.
17. **Decision:** `network_operation_count` in this outer preflight reports
    only executor-owned network operations observed by the executor's exact
    audit boundary. It has no child contribution. Zero means only that the
    executor observed zero executor-owned network operations; it is not proof
    of child-network denial, complete observation, firewall isolation, or
    technical impossibility.
18. **Decision:** the accepted in-harness Python audit guard remains unchanged
    and reports only Python audit events observed in that harness process.
    Neither count may be represented as complete native child-network
    evidence. `network_authorized=false` remains an authority denial, not an
    isolation or completeness claim.
19. **Derived:** the accepted parent and receipt schemas contain zero network
    counts and false network authority but do not make independent child-network
    prevention or complete observation a preflight prerequisite. The exact
    `External-Isolation Escalation` clause in
    `docs/contracts/trusted_owner_native_role_pool_profile.md` rejects a native
    wave when there is "a need for independently proven ... network isolation."
    This owner rescope defines no such need or claim for this trusted-owner
    synthetic preflight, so the conditional escalation clause is not a direct
    authority contradiction.
20. **Decision:** remove the rejected child-network state, blocked outcome,
    KAT, selector dimensions, success-unreachability rule, and
    enforcement-successor route. Restore the accepted process-entry and
    passing routes whenever every
    non-network prerequisite is exact. Do not add a replacement network field,
    status, schema, KAT, lifecycle, mechanism, package, or implementation path.
21. **Preserved implementation finding:** `E-004` remains a concrete Codex D
    repair obligation. Every proven-owned handle must receive exactly one close
    attempt, close failures must aggregate without short-circuiting, and
    `DeleteProcThreadAttributeList` is permitted only after successful
    attribute-list initialization. No current process execution becomes
    authorized by preserving those requirements.
22. **Narrowed implementation finding:** `E-005` remains blocking only for
    exact repository, installed-tree, and generated-residue pre/post evidence,
    derived executor-owned network-event accounting, and derived external-effect
    accounting. Hard-coded effect counts remain prohibited. Complete child
    network prevention or observation is superseded and is not blocking.
23. **Observed:** the latest independent rescope review returned
    `blocked_effect_observation_profile_closure_required`. It preserved `E-004`
    for Codex D and found the `E-005` correction incomplete because the exact
    roots, inventory algorithm, sampling order, drift rules, and count
    derivations for local-effect evidence were not mechanically defined. The
    review changed no file and created no execution authority.
24. **Observed:** independent re-review of contract SHA-256
    `70b45f739e567837beaf5bca69b9da9b0c0d05514f376d20f04b83512c3c19bf`
    returned `contract_re_review_blocked`. It preserved `E-004` for Codex D and
    kept `E-005` open for exact source-state and sampling closure. No preflight
    ran, no file changed, and no operational authority was created.
25. **Derived:** the first remaining contract failure is that pre-effect
    terminal routes have no exact derivation mode for their public zero effect
    counts, while post-entry drift or sampling ambiguity cannot inhabit the
    integer-zero public schema. A raw observation state and an exact
    canonical-result eligibility reduction are required; a new public field,
    status, KAT, lifecycle outcome, or authority is not.
26. **Observed:** independent re-review of contract SHA-256
    `b6b2a2ff0bc1479f57ea62f5853b04dfea948feb098ac89077c4fe5041428094`
    found one literal overlap between LE-03 and LE-04: boundary entered,
    pre-inventory exact, post-inventory failed or ambiguous, and audit nonzero.
    First-applicable evaluation produced `3/1/7/7/54` instead of the declared
    disjoint `3/1/6/8/54`. The normalized source audit remained exact at
    `8/5,824`; no file changed and no execution authority was created.
27. **Observed:** PR #792 merged the independently accepted executor package at
    `4b51761cde2310df3e9cda3a3e3ad34e617c8e79`; its exact-head E review is
    `https://github.com/Tahjali11/Mythic-Edge/pull/792#pullrequestreview-4835311363`.
28. **Observed:** the current D candidate adds the three missing raw checks for
    the predecessor review, implementation review, and executor test without
    changing execution behavior.
29. **Observed:** it also added an executor-owned checksum-field-excluded
    digest. Changing the source and recomputing that embedded value remained
    self-admitted, proving `ME-RP-780-PUBLIC-BINDING-E-006`.
30. **Decision:** fresh E review plus the exact owner decision own acceptance
    of executor bytes. Runtime owns the other independent public bindings and
    raw executor measurement; no new trust mechanism is required.
31. **Observed:** PR #793 merged the independently reviewed public-binding
    correction at `9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a`; the reviewed tree is
    `dc4ff2cb56e2e3556fd176f14b23a139ec068748`.
32. **Observed:** one later owner-authorized preflight at those exact bytes
    exited `3` after approximately `31.4` seconds with empty stdout and the
    exact 37-byte generic unknown sentinel at SHA-256
    `f8ef6df4e5fa677e28cd29a82b1a0d1d983ca336610971c842a725c25c17018e`.
    No canonical result was sealed. The owner decision is
    `consumed_unknown_nonreusable`, and no retry is authorized.
33. **Observed:** fresh independent adjudication could prove only the outer
    sealing failure. The public evidence could not distinguish pre-inventory,
    pre-create setup, `CreateProcessW` entry, target timeout, post-effect, or
    cleanup failure. Timing alone is non-discriminating because both inventory
    and target-execution budgets are 30 seconds.
34. **Decision:** preserve the existing canonical result and public status
    vocabulary. When canonical sealing fails after exact CLI admission, emit
    one of three fixed public-safe ASCII terminal diagnostics that carries only
    the coarse create-boundary stage and conservative consumption disposition.
    Do not add a JSON schema, result field, lifecycle status, durable artifact,
    retry, process, or diagnostic detail.

Finding `ME-RP-780-PREFLIGHT-EXEC-B-001` is `fixed_confirmed`.
Finding `ME-RP-780-PREFLIGHT-EXEC-E-001` is `fixed_confirmed_preserved`.
Finding `ME-RP-780-PREFLIGHT-EXEC-E-002` is `fixed_confirmed_preserved`.
Finding `ME-RP-780-PREFLIGHT-EXEC-E-003` is `fixed_confirmed`.
Finding `ME-RP-780-PREFLIGHT-EXEC-E-004` is
`fixed_confirmed_preserved`.
Finding `ME-RP-780-PREFLIGHT-EXEC-E-005` is
`fixed_confirmed`.
Finding `ME-RP-780-PUBLIC-BINDING-E-006` is
`fixed_confirmed_preserved`.
Finding `ME-RP-780-PREFLIGHT-TERM-B-001` is
`active_clause_reconciliation_authored_re_review_pending`.

## Module And Truth Ownership

Module: one Windows-hosted, zero-effect direct-CPython synthetic-preflight
constructibility gate and conditional executor.

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership remains unchanged:

- the accepted direct-interpreter successor owns the selected executable
  binding, preflight command, limits, outcomes, and later observation route;
- `tools/check_role_pool_r0_offline_observation.py` owns exact interpreter
  metadata validation and preflight classification;
- the executor owns the current prelaunch constructibility fact, real Win32
  process creation and topology observations for one synthetic preflight, its
  own local-effect observations, and only its own observed network events;
- a private absolute executable path is bounded runtime input and owns no
  public truth; and
- independent Codex E review owns acceptance of the executor bytes and any
  later public-safe preflight result. The fresh owner decision binds those
  accepted bytes before execution; the executor does not self-certify them.

No parser, release-state, registry, Role Pool skill, installed copy, managed
validator, observation receipt, or issue #769 truth moves into this module.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Current merged base | `9b70ca0637f51f08b7fb6aa87c8ca30dcdd0b26a` |
| Current merged tree | `dc4ff2cb56e2e3556fd176f14b23a139ec068748` |
| Current integration PR | `https://github.com/Tahjali11/Mythic-Edge/pull/793`; merged; all six checks passed |
| Current exact-head review | `https://github.com/Tahjali11/Mythic-Edge/pull/793#pullrequestreview-4836016353`; reviewed head `c0fc77183038d961dea98a61be70fd0db29e543c`; review-body SHA-256 `699835c8d25117b4854486650c8a1ba1dd9bdab5bbb48a7ea1a2f5cf5b285128` |
| Immediate contract predecessor | this artifact at SHA-256 `d2bfd244a4c20c0631cd7d16bc3209f08f471368d8ba090997acfecd16a314c7` |
| Immediate contract-review predecessor | `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_public_binding_trust_anchor.md`; SHA-256 `25acde0c0095929069952caf1fa458dee4b725c9c96212c9d3c8118c0e702ca0` |
| Current executor | `tools/run_role_pool_r0_direct_interpreter_preflight.py`; 126,139 bytes; SHA-256 `8569209525e7e6eca56f91a7801ee3c763cfb437767da0af5739b68eb1e7d382` |
| Current executor test | `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`; 62,156 bytes; SHA-256 `a05c537d30cb5e3c4ed77ec7747cc87f19ec5f9729bed4f1fc50818f19f54cfe` |
| Terminal execution evidence | exit `3`; stdout `0` bytes; stderr `37` bytes at SHA-256 `f8ef6df4e5fa677e28cd29a82b1a0d1d983ca336610971c842a725c25c17018e`; no canonical result |
| Terminal authority disposition | `consumed_unknown_nonreusable`; retry false; accepted observation count `0` |
| Integrated base | `3c3b4bfa7ddcd066d54b8b17ca9f3d496919d23f` |
| Reviewed implementation head | `4893d53960f25370aa4d9c2313d7fc33ffeb707e` |
| Integration PR | `https://github.com/Tahjali11/Mythic-Edge/pull/791`; merged |
| Integrated executor base | `4b51761cde2310df3e9cda3a3e3ad34e617c8e79` |
| Executor integration PR | `https://github.com/Tahjali11/Mythic-Edge/pull/792`; merged |
| Exact-head executor review | `https://github.com/Tahjali11/Mythic-Edge/pull/792#pullrequestreview-4835311363`; reviewed head `28036bc82266702c00308cbb6d60a168a2f32142`; `accepted_exact_head_no_blocking_findings` |
| Accepted merged executor predecessor | `tools/run_role_pool_r0_direct_interpreter_preflight.py`; 124,909 bytes; SHA-256 `a681dac983478cfda1d64729dd1a67258dc26f1e90d7873be0805e1581e0f170` |
| Accepted merged executor-test predecessor | `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`; 61,765 bytes; SHA-256 `53e98df75a04ec55530b2279af366f1ccf32d9b6d3b45afbd2f8dcd2dbe4dc3e` |
| Post-merge source finding | `https://github.com/Tahjali11/Mythic-Edge/pull/792#discussion_r3696262736` |
| Post-merge D handoff | `docs/implementation_handoffs/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_post_merge_binding_fixer.md`; current candidate SHA-256 `c029076f2eb4c9c4e7e5576c14bc7b1ef79ba313b9bbd77302f5eed6209a914e` |
| Unaccepted D executor candidate | 128,048 bytes; SHA-256 `8e244cb973012d811b2d1a4cdfe0dd831b0b53fa2d0d2bdfae9169343e71eeba` |
| Unaccepted D executor-test candidate | 63,312 bytes; SHA-256 `087ea97b9b16d6463294d08453ff723502853c8aeecf515b4057873eeead45bf` |
| Parent direct-interpreter contract | `docs/contracts/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md`; 41,834 bytes; SHA-256 `17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84` |
| Parent independent review | `docs/contract_test_reports/role_pool_trusted_owner_r0_offline_observation_direct_interpreter_successor.md`; 8,464 bytes; SHA-256 `0fd7d921a92fbd58576f053a0e8938d3ae4a0266e9a023b762f933e65aee450f`; `final_approval` |
| Accepted harness | `tools/check_role_pool_r0_offline_observation.py`; 67,314 bytes; SHA-256 `001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6` |
| Accepted harness test | `tests/test_check_role_pool_r0_offline_observation.py`; 52,662 bytes; SHA-256 `3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3` |
| Initial reviewed predecessor | this artifact at SHA-256 `4c835147d2ddab0b2855c27f86d45b6cb69dd65a372f5124fde236d9785c0e0d` |
| First revised predecessor | this artifact at SHA-256 `c3f7da7ac3d64dac3d9c7ff54e5fdb8ce181a7eaafcdd106f003ee4d4c08fac0` |
| Immediate reviewed predecessor | this artifact at SHA-256 `77e8867d76db9599d556d043c26a32eb7e882955b898b61887621c59b6fe95f5` |
| Initial report state | current follow-up report records the prior 8,949-byte state at SHA-256 `a70a337a0b4db8c556061b37ee62ef022b7b489c6ce6afe044c70065c7072742`; lineage only |
| First follow-up review report | `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`; historical 15,760-byte state at SHA-256 `03b0e001a55ef1116ebc3599dca02cd3b5f9b10ea655fce69931c94d1ba51a43`; lineage only |
| Accepted executor contract | this artifact at SHA-256 `d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848`; predecessor to this reconciliation |
| Rejected network-expansion state | this artifact at SHA-256 `bcc6a7e6e32b76503de9fdb42dcc95cb3cfce0720f7d3662cec005f9d969eefd`; owner-rejected, superseded, and retained as lineage only |
| Accepted contract-review report | `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md`; 26,523 bytes; SHA-256 `97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038`; `accepted_exact_r0_direct_interpreter_preflight_executor_contract` |
| Implementation review | `docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_implementation.md`; 16,673 bytes; SHA-256 `49d66f9ce38f0fab01bbeebf02deba4451f87f45600a21552b47a3e9292e0dac`; `changes_requested` |
| Reviewed executor candidate | `tools/run_role_pool_r0_direct_interpreter_preflight.py`; 78,988 bytes; SHA-256 `3490a3c2a0492b3375def91effa8ff0eeb7704d705cf3d103a4737bf086b660a` |
| Reviewed executor test candidate | `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`; 27,936 bytes; SHA-256 `4cd7182ad7e0daa8b9ec0751aacd461f163656546696425d399fc1a55933fcdb` |
| Direct-interpreter binding self-digest | `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333` |
| Direct-interpreter binding artifact | `235e21a04acb454adb5471f2136b53547c35a279a63b8e09d8c6a10926d3bb9b` |
| Fresh sequence | `r0.offline.sequence.3.5c7174d35ea27e21812024c5f8afbfaa`; unexecuted |
| Accepted observation count | `0` |
| Issue #780 | open with zero top-level comments |
| Issue #769 | open with zero top-level comments |

The first ten rows are the controlling current bindings for this amendment.
The remaining rows preserve predecessor lineage or immutable parent inputs and
cannot override those current values.

The parent contract, review report, harness, and harness test are immutable
inputs to this successor. Drift stops before implementation. The historical
v2 sequence remains spent and nonreusable. This contract neither retires nor
consumes the unexecuted v3 identities.

## Scope

### Future implementation paths

After independent acceptance and a separate owner implementation decision, the
implementation role may modify exactly the current reviewed bytes of:

1. `tools/run_role_pool_r0_direct_interpreter_preflight.py`; 126,139 bytes;
   SHA-256 `8569209525e7e6eca56f91a7801ee3c763cfb437767da0af5739b68eb1e7d382`;
   and
2. `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`; 62,156
   bytes; SHA-256
   `a05c537d30cb5e3c4ed77ec7747cc87f19ec5f9729bed4f1fc50818f19f54cfe`.

The accepted harness and its test remain byte-exact. In only the executor and
focused test, implementation may add the process-local monotonic tracker, the
three exact ASCII fallback constants, outer fallback selection, and the exact
focused tests required below. It may refresh only the mechanically dependent
contract, contract-review, and focused-test digest bindings. Existing public
binding checks, process behavior, canonical result behavior, and every other
byte remain unchanged unless formatting is mechanically required.

No sidecar, signature, key, launcher, wrapper, new input, digest algorithm,
masking rule, schema, status, process, or third implementation path is allowed.
The executor is dedicated to this one preflight command and cannot
accept an observation ID, script path, module, arbitrary argument, cwd,
timeout, executable fallback, environment override, output destination, or
command supplied by a caller.

### Explicit exclusions

This contract does not authorize or define:

- a general process, shell, SDK, broker, service, task, command, or launch API;
- the R0 observation executor or issue-comment publication;
- interpreter discovery, installation, repair, replacement, or fallback;
- source, installed-skill, registry, release-state, or authority-index writes;
- network access, package access, credentials, candidate access, or private
  evidence discovery; or
- R1-R8, dispatch, canaries, Stage 4, submission, merge, deployment,
  readiness, compatibility, reliability, correctness, privacy, security, or
  assurance claims.

## Public Interface

The implementation exposes only:

```python
execute_preflight(
    private_interpreter_path: pathlib.Path,
    *,
    adapter: DirectWindowsPreflightAdapter | None = None,
) -> Mapping[str, object]
```

The production call omits `adapter` and therefore uses the fixed Win32
adapter. Adapter injection exists only for in-process focused tests. The CLI
accepts exactly `--private-path-stdin`; no other option or positional argument
is valid.

The CLI reads one private absolute path as one strict UTF-8 line from standard
input. The input is limited to 4,096 bytes, requires exactly one final LF,
forbids BOM, NUL, CR, blank input, and additional lines, and is zeroized from
mutable buffers after conversion to the bounded in-memory path object. It is
not echoed. The path may not arrive through argv, an environment variable,
PATH, registry, current directory, config file, issue field, receipt, shell
expansion, wildcard, alias, or search.

The controller process that hosts this executor is outside the measured
target job and grants no alternate launcher authority. In particular, a
controller's own Python or shell identity cannot be substituted for, or
reported as, the selected target `python.exe`.

### Public-safe terminal fallback boundary

For an exact `--private-path-stdin` invocation, the executor creates one local,
in-memory, non-durable terminal-boundary tracker immediately after argument
admission and before the first fallible binding, inventory, or private-ingress
operation. Its initial state is `precreate`. It may transition exactly once to
`create_entered`, immediately before the first and only `CreateProcessW` call.
It may never reset, transition backward, or be inferred from elapsed time,
process scans, output, cleanup, exception type, or a later observation.

The tracker has no public API, file, environment variable, registry value,
issue field, result field, or reusable authority. The implementation may use a
local object or callback, but it must remain owned by the one CLI invocation
and visible to the outer exception-to-terminal boundary. Invalid, missing,
duplicated, or contradictory tracker state is `ambiguous`.

If the ordinary 38-field canonical result seals, behavior is unchanged and no
fallback diagnostic is emitted. If it cannot seal after exact CLI admission,
stdout remains empty, exit code remains `3`, and stderr is exactly one of:

| Tracker fact | Exact ASCII stderr including final LF | Bytes | SHA-256 | Workflow disposition |
| --- | --- | ---: | --- | --- |
| exact `precreate` | `direct_interpreter_preflight_unknown_precreate_unconsumed\n` | 58 | `7584ac48a50925e117afb55e6127b27f5ceb36ccb753a5ab8eee32cd0b290473` | retire unconsumed and nonreusable |
| exact `create_entered` | `direct_interpreter_preflight_unknown_create_entered_consumed\n` | 61 | `96b69d4593abab39f9d256461aa0b692f58750059af5d6277273dd49de1ba97c` | consumed and nonreusable |
| `ambiguous` | `direct_interpreter_preflight_unknown_stage_ambiguous_consumed\n` | 62 | `6f7649de0b4db9c2b5db46635ff52ff4fdcb47fef8daa41a1c4cb7766e4729bd` | conservatively consumed and nonreusable |

These are diagnostics, not `result_status` values, receipts, or authority
objects. They reveal no failure reason inside a stage. They do not distinguish
inventory, binding, setup, target, effect, identity, timeout, or cleanup
subconditions. Invalid CLI arguments before tracker creation retain the
existing 37-byte generic sentinel and create no claim about an owner decision.
If terminal emission is partial, missing, reordered, CRLF-translated, or
otherwise not byte-exact, the workflow makes no stage claim and conservatively
treats any supplied owner decision as consumed and nonreusable.

### Executor-byte acceptance boundary

Executor-byte acceptance is an external workflow gate, not a runtime
self-admission predicate. This is the controlling interpretation wherever an
older clause says that public bindings reject executor drift.

Before starting the executor process, the separately authorized execution role
must:

1. require a fresh independent Codex E implementation review bound to one exact
   repository head and exact SHA-256 values for the executor and focused test;
2. require the fresh owner preflight decision to repeat those two hashes and
   bind the accepted contract and contract-review hashes;
3. independently read each of the two ordinary, non-reparse files with stable
   before/open/after identity and compute its raw SHA-256;
4. compare both raw digests with the E-accepted and owner-bound values before
   starting the executor or supplying private stdin; and
5. stop without starting the executor, supplying private input, or creating a
   result when either identity or digest is not exact.

Such a stop reuses the existing
`retired_unconsumed_precreate_failure_nonreusable` owner-decision disposition.
It creates no executor result and requires a fresh review or owner decision as
appropriate. No retry, alternate bytes, or nearest-match acceptance exists.

Runtime `_public_bindings()` must still compare the accepted contract review,
predecessor contract review, implementation review, parent contract and review,
harness and harness test, local-effect reconciliation review, and focused
executor test against their exact embedded digests before parent loading,
private input, or target-process entry. It computes the raw executor SHA-256
only for result field `executor_sha256`; it does not compare that value with a
digest stored in the executor itself.

`public_bindings_exact=true` therefore means that all independently owned
runtime inputs are exact. It is not a claim that the executor cryptographically
authenticated itself. A preflight result becomes reviewable only when Codex E
also confirms that fields `executor_sha256` and `executor_test_sha256` equal the
same hashes accepted before execution. The external pre-check, runtime
non-self checks, and post-result E comparison are one chain; none substitutes
for another.

This boundary makes no hostile-code authenticity, code-signing, privileged
isolation, or concurrent same-user tamper-prevention claim. Those are not
eligibility requirements for this trusted-owner R0 preflight. Adding any such
claim or mechanism requires a separate owner decision and contract; it cannot
block the current external acceptance chain without new concrete evidence that
the chain cannot truthfully execute this preflight.

### Network-count ownership and nonclaim

The accepted observation harness and harness test remain byte-exact. Their
existing `AuditBoundary` increments its in-harness `network_operation_count`
only for Python audit-event names beginning with `socket.`. That count covers
only events observed inside that harness process.

The outer preflight executor owns a separate bounded counter using that same
closed `socket.` audit-event predicate. Production observation begins before
the first prelaunch binding check and remains active through terminal result
sealing. A matching executor event increments the counter and fails closed;
the count may never be hard-coded. The public preflight
`network_operation_count` equals this
executor-owned count exactly and has no child contribution.

Therefore `network_operation_count=0` means only that the outer executor
observed zero executor-owned matching events. It does not mean that child
networking was prevented, completely observed, firewall-blocked, or technically
impossible. `network_authorized=false` denies authority to use network resources
but makes no isolation or observation-completeness claim. Absence of independent
child-network evidence does not block setup, `CreateProcessW` entry, child
creation, a passing result, independent review, or later owner-decision
eligibility.

Any nonzero, unreadable, or ambiguous executor-owned count prevents canonical
result sealing and uses the exact diagnostic selected by the terminal-boundary
tracker. The owner decision's consumed fact still derives only from actual
`CreateProcessW` entry; regardless of that fact, the failed attempt is terminal
and nonreusable. This adds no network status, result field, KAT, lifecycle
outcome, retry, or successor route.

### Exact local-effect observation profile

`ME-RP-780-PREFLIGHT-EXEC-E-005` is constructible through one closed,
in-memory observation profile. It creates no durable schema, snapshot artifact,
digest family, output field, path inventory, or third implementation path.

The profile owns exactly these two roots and one derived subset:

1. `repository_root` is the ordinary, non-reparse directory obtained as
   `Path(__file__).absolute().parent.parent` from the already validated
   executor file. Its value is not caller supplied, resolved through PATH, or
   emitted. Its observed working-tree surface contains the root and every
   descendant except the exact top-level `.git` control entry and all of that
   entry's descendants. There is no other exclusion: tracked, untracked,
   hidden, cache, data, contract, report, source, and test entries are all in
   scope.
2. `installed_role_pool_root` is the exact
   `<default Codex home>/skills/mythic-edge-role-pool` target derived through
   the accepted `check_role_pool_r0_bootstrap._production_roots` and exact
   installer binding. `CODEX_HOME` presence, a null installed root, an
   alternate root, a missing target, or root drift rejects the profile. The
   private absolute value is never emitted. The complete target tree has no
   exclusions.
3. `generated_residue_surface` is a projection, not a third traversal. From
   the repository and installed rows, retain every row whose relative path has
   a component exactly `__pycache__`, `.pytest_cache`, or `.ruff_cache`, or
   whose final component ends exactly in `.pyc` or `.pyo`. Preexisting residue
   is permitted only when its complete rows remain byte-identical; this
   preflight owns zero residue creation, deletion, or modification.

The repository `.git` exclusion limits this evidence to working-tree effects;
it makes no claim about Git administrative state. The two roots and the fixed
residue predicate are the complete local filesystem effect surface owned by
this synthetic preflight. No search outside them, no alternate installed root,
and no claim about unrelated host paths is permitted.

The internal observation vocabulary is closed. A root inventory is `exact` or
`unreadable_or_ambiguous`; a pre/post comparison is `equal`, `drift`, or
`not_comparable`; and an audit counter is `exact_zero`, `nonzero`, or
`unreadable_or_ambiguous`. `not_comparable` is required whenever either owning
inventory is not exact. No other spelling or implicit null state is accepted.

The executor retains one non-durable `LocalEffectObservation` record with keys
in this order:

1. `effect_boundary_state`: `not_entered` or `entered`;
2. `pre_inventory_state`: `not_started`, `failed_or_ambiguous`, or `exact`;
3. `post_inventory_state`: `not_required`, `failed_or_ambiguous`,
   `exact_equal`, or `exact_drift`;
4. `executor_audit_state`: `exact_zero`, `nonzero`, or
   `unreadable_or_ambiguous`;
5. `repository_write_attempt_count`;
6. `installed_write_attempt_count`;
7. `executor_network_operation_count`;
8. `repository_row_delta_count`;
9. `installed_row_delta_count`; and
10. `residue_row_delta_count`.

Each of the six count fields is either a checked nonnegative integer when its
owning source is exact or the exact internal sentinel `unavailable`. The
sentinel cannot be normalized to zero. This is a typed in-memory record, not a
public schema, serialized object, snapshot, path inventory, or digest family.

#### Stable inventory algorithm

Each root observation uses this exact read-only algorithm:

1. Open the fixed root for metadata only without following reparse points.
   Require an ordinary directory, no reparse attribute, and one readable
   Windows identity tuple of volume serial number, file-index high, and
   file-index low. Retain the identity only in bounded memory.
2. Recursively enumerate descendants without following links or reparse
   points. Reject an unsupported node kind, path escape, reparse point,
   duplicate relative path, or two names equal under Windows ordinal
   case-insensitive comparison. Apply only the exact `.git` exclusion above.
3. Convert each accepted relative name to a case-preserving POSIX path. Reject
   a NUL, `.` or `..` component, absolute path, drive prefix, or path longer
   than 1,024 UTF-8 bytes. Order rows by ordinal comparison of their UTF-8 path
   bytes.
4. Represent a directory in memory as
   `(relative_path, "directory", 0, sha256(empty_bytes))`. Observe its ordinary
   directory and non-reparse state before and after the traversal.
5. Represent a file as
   `(relative_path, "file", byte_count, sha256(exact_payload))`. Before read,
   open, after read, and after close, require the same ordinary-file identity,
   byte count, non-reparse state, and fixed-root containment. A short read,
   identity change, metadata change, unreadable byte, or close ambiguity
   invalidates the observation.
6. Re-enumerate the relative path and node-kind set, reobserve the root
   identity, and require exact equality with step 2. No row or private metadata
   may be serialized or emitted.

Every metadata or file handle acquired by this algorithm is a proven-owned
handle under E-004: it receives exactly one close attempt, close attempts do
not short-circuit, and any close failure invalidates that root observation.

One root inventory is bounded to 4,096 descendant rows, 256 MiB of file
payload, 64 MiB per file, and 30 seconds measured with a monotonic clock. A
budget overrun is `unreadable_or_ambiguous`, never an empty or zero snapshot.
The repository rows under the exact
`docs/codex_skills/mythic-edge-role-pool` subtree, after stripping that fixed
prefix, and the complete installed root must each reproduce the accepted
41-node, 36-file, 6,495-byte install-tree projection and SHA-256
`18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`
before process entry and after cleanup. The repository working-tree inventory
has no predeclared digest; its exact pre-observation is the one comparison
baseline for the same attempt.

#### Sampling order and ownership

The executor installs one process-global, fail-closed audit owner before the
first retained-history, public-binding, or owner-decision read. It remains
active through final result sealing and
cannot be replaced, disabled, or reset. Production can activate it once;
focused tests use the adapter boundary and do not stack live audit hooks.

After public and owner-decision validation, but before private-path ingress or
any Win32 setup, the executor derives the two roots, takes the repository
pre-inventory, takes the installed pre-inventory, and derives the residue
pre-projection in that order. `pre_inventory_state` is `not_started` before
that sequence, `failed_or_ambiguous` if any required source is not exact, and
`exact` only after all three observations are exact. A failure stops before
`CreateProcessW`, sets `private_binding_state=rejected`, and leaves the owner
decision unconsumed but terminally nonreusable for this attempted operation.

The one local-effect boundary is entered immediately before the first step-8
operation that can allocate an attempt-owned pipe, Job Object, attribute list,
or other setup resource. Everything before that point is restricted to the
installed audit owner, bound public or owner-decision reads, fixed-root
inventory reads, bounded private metadata reads, and ambient-job metadata
queries. No call on that pre-boundary path may create, write, delete, rename,
replace, connect, launch, or mutate process-global environment state.

If a route terminates before this boundary, set
`effect_boundary_state=not_entered` and
`post_inventory_state=not_required`. A post-inventory is neither required nor
permitted merely to support that terminal result. This route can derive a
canonical zero-effect result only from the closed pre-boundary call graph,
exact closure of every temporary metadata handle, and
`executor_audit_state=exact_zero`. It does not claim repository-tree,
installed-tree, or residue equality across time.

After the boundary is entered and every setup or process-lifecycle branch has
attempted all contract-owned cleanup, the executor takes the repository
post-inventory, installed post-inventory, and residue post-projection in the
same order. It must attempt all three unless continued traversal is itself
unsafe. Exact equal comparisons set `post_inventory_state=exact_equal`; any
exact row delta sets `exact_drift`; and an unsafe, unreadable, incomplete,
budget-exceeded, identity-unstable, or not-attempted terminal observation sets
`failed_or_ambiguous`. Boundary entry requires
`pre_inventory_state=exact`; every other combination is source-state
corruption. No post-observation failure authorizes deletion or repair.

The audit owner uses the accepted harness `AuditBoundary` write-event and
`socket.` vocabularies. A write event whose path is within `repository_root`
increments `repository_write_attempt_count`; one within
`installed_role_pool_root` increments `installed_write_attempt_count`; an
executor `socket.*` event increments `executor_network_operation_count`.
Environment mutation, an unclassifiable write path, a write outside both roots,
or counter overflow is a safety-boundary failure and prevents canonical result
sealing. These are executor observations only; no child audit event is inferred.

#### Exact count and result-eligibility derivation

For each exact pre/post row map, `row_delta_count` is the number of distinct
relative paths that are added, removed, change kind, change byte count, or
change payload digest. A path with several changed attributes counts once.

There are exactly two canonical-result derivation modes:

1. `early_terminal_structural_zero`: the effect boundary was not entered, the
   post state is `not_required`, the route-specific pre state is valid, every
   acquired metadata handle closed exactly, the closed call graph contains no
   effect-capable operation, and the executor audit is exact zero. Derive
   repository, installed, residue, network, and external counts as zero from
   that combined structural and audit proof. This mode makes no pre/post tree
   equality claim.
2. `sampled_exact_zero`: the boundary was entered, the pre state is `exact`,
   the post state is `exact_equal`, and the executor audit is exact zero.
   Derive:
   - `repository_write_count = repository_write_attempt_count +
     repository_row_delta_count`;
   - `installed_write_count = installed_write_attempt_count +
     installed_row_delta_count`;
   - `generated_residue_delta_count = residue_row_delta_count`; and
   - `external_effect_count = repository_write_count +
     installed_write_count + generated_residue_delta_count +
     executor_network_operation_count`.

Both modes require all five resulting counts to be exactly zero before a
canonical public object can exist. The selected mode is retained in the
normalized source record as `effect_derivation_state`; it is not public.

The sums use checked nonnegative integers. A residue row can deliberately
contribute to both its owning tree delta and the residue delta; these values are
deterministic evidence-witness counts, not a claim about unique OS mutation
cardinality. The active success KAT and 38-field public schema remain
unchanged.

An exact nonzero count, `exact_drift`, source unreadability, counter overflow,
or ambiguity cannot inhabit the public integer-zero fields. It therefore
creates no normalized `SourceRecord` and no JSON object. The executor emits
only the exact diagnostic selected by the terminal-boundary tracker and exits
`3`; this is the existing unknown terminal route, not a seventh result status
or a fabricated zero-count object. The owner decision disposition is derived
independently from whether `CreateProcessW` was entered.

For `early_terminal_structural_zero`, `cleanup_confirmed=true` requires exact
closure of every acquired metadata handle and proof that no attempt-owned setup
resource exists. For `sampled_exact_zero`, it additionally requires every
E-004 resource-cleanup condition. Resource cleanup cannot make effect evidence
true, and effect evidence cannot make failed handle or process cleanup true.

The raw local-effect selector enumerates the Cartesian product of:

- two boundary states;
- three pre-inventory states;
- four post-inventory states; and
- three audit states.

Across all `72` tuples, literal predicate cardinalities are:

| Row | Exact condition | Internal outcome | Cardinality |
|---|---|---|---:|
| LE-01 | boundary not entered; post not required; any pre; audit exact zero | `early_terminal_structural_zero` | 3 |
| LE-02 | boundary entered; pre exact; post exact equal; audit exact zero | `sampled_exact_zero` | 1 |
| LE-03 | boundary not entered with post not required and audit nonzero; or boundary entered with pre exact, post exact equal and audit nonzero; or boundary entered with pre exact, post exact drift and audit exact zero/nonzero | `effect_observed_nonzero` | 6 |
| LE-04 | boundary not entered with post not required and audit unreadable/ambiguous; or boundary entered with pre exact and post failed/ambiguous regardless of audit; or boundary entered with pre exact, post exact equal/drift and audit unreadable/ambiguous | `effect_evidence_unavailable` | 8 |
| LE-05 | every other phase/pre/post combination | `invalid_effect_source_state` | 54 |

The selector does not use first-match ordering to resolve predicate overlap;
the predicates are literally disjoint and no tuple matches more than one row.
It must reproduce overlap, uncovered, and
unreachable counts `0/0/0`. Only LE-01 and LE-02 may construct a normalized
source record. LE-03 through LE-05 use the exact diagnostic selected by the
terminal-boundary tracker. This selector is review evidence only and creates no
public status, schema field, or durable object.

## Exact Prelaunch Order

The external executor-byte acceptance boundary above completes before this
numbered runtime order begins. It is not an additional process, implementation
path, result field, or durable artifact. One later authorized executor must
then perform this order once:

1. Activate the exact executor audit owner and inspect the retained historical
   proof. If exact direct use is proven, stop through the early structural-zero
   gate without observing any later source state. Otherwise recompute the
   parent contract, parent review, harness, harness-test, integrated-base,
   issue-state, and zero-comment bindings.
2. Verify that the owner preflight decision is exact, current, unexpired,
   unconsumed, nonreusable, and bound to the accepted executor contract,
   contract review, and the two externally verified implementation hashes.
   This remains a workflow gate; the executable does not invent, broaden, or
   self-certify authority.
3. Derive the fixed repository and installed roots and take the exact
   repository, installed-tree, and residue pre-observations defined above.
4. Parse the private path through the one-line stdin boundary without
   normalization, search, or echo.
5. Call the accepted harness's `validate_running_direct_interpreter(path)`;
   this performs two separate exact handle observations.
6. Reopen and validate the same object once more immediately before launch.
7. Derive one ambient-job state and creation-flag choice through the closed
   selector below. A rejected or unreadable state stops here through
   `early_terminal_structural_zero` when its audit and cleanup proof is exact;
   otherwise only the exact tracker-selected terminal diagnostic may be
   emitted.
8. Atomically mark `effect_boundary_state=entered`, then enter the one
   pre-create setup phase. Create the three anonymous pipes and
   the private job object, validate all six pipe handles, configure the
   completion port and process attributes, then close the parent-owned stdin
   writer to establish EOF. At this point no target process exists and the
   owner decision remains unconsumed. If any setup operation fails, is
   interrupted, or cannot be proved complete before step 9, normalize
   `precreate_setup_state=failed_no_process`, close every proven-owned local
   handle once, perform the fixed post-observations, emit the exact pre-create
   unknown projection below, and retire
   this owner decision as `retired_unconsumed_precreate_failure_nonreusable`.
9. The first call to `CreateProcessW` is the single consumption point. Entry
   into that call permanently spends the owner preflight decision even when
   process creation fails or the outcome becomes unknown.
10. Complete process and handle cleanup, take the fixed post-observations,
     derive all four public effect counts, the internal residue count, and
     `cleanup_confirmed`, classify through the
    accepted `classify_direct_preflight_observation`, seal one public-safe
    result, and stop. No retry, relaunch, replacement target, or second process
    is allowed.

Failure before step 9 leaves the decision unconsumed but does not authorize
the executor to loop. A step-8 terminal result is nonreusable despite the
exact `preflight_authority_consumed=false` fact. Its canonical result, or an
exact precreate diagnostic caused by nonzero, unavailable, or invalid effect
evidence after setup entry, requires a fresh owner decision in every later task.
Failure at or after step 9 is consumed and nonreusable. If the caller cannot
establish which side of step 9 was reached, classify the decision as consumed
and use the exact ambiguous diagnostic; do not fabricate a public count or JSON
object.

## Exact Win32 Process Boundary

This section is the active conditional process-entry boundary and the owner of
the `E-004` cleanup correction. Once every non-network precondition is exact,
at least one structural route reaches `CreateProcessW` and at least one exact
terminal route reaches `direct_interpreter_preflight_passed`. Independent
child-network prevention or complete observation is not an eligibility
requirement for either route.

The production adapter must use direct Windows APIs through `ctypes`; it may
not use `subprocess`, `os.system`, `os.startfile`, PowerShell, `cmd.exe`, WMI,
Task Scheduler, App Server, `codex exec`, a broker, a service, or a helper
process.

The controlling API semantics are Microsoft Learn's
[`CreateProcessW`](https://learn.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw),
[`CreatePipe`](https://learn.microsoft.com/windows/win32/api/namedpipeapi/nf-namedpipeapi-createpipe),
[`UpdateProcThreadAttribute`](https://learn.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute),
[`AssignProcessToJobObject`](https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject),
[`QueryInformationJobObject`](https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject),
[Nested Jobs](https://learn.microsoft.com/windows/win32/procthread/nested-jobs),
[Job Objects](https://learn.microsoft.com/windows/win32/procthread/job-objects),
and
[`JOBOBJECT_ASSOCIATE_COMPLETION_PORT`](https://learn.microsoft.com/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port).
In particular, contract acceptance must not reinterpret completion-port
delivery as guaranteed.

The fixed target is exactly:

```text
[<private exact python.exe>, "-B", "-c", "pass"]
```

Requirements:

1. `CreateProcessW.lpApplicationName` is the exact private path. No search
   function or shell parses the application name.
2. The command line is derived only from the fixed four-element vector using
   one Windows-compatible quoting function. It is never serialized publicly.
3. `lpCurrentDirectory` is the exact repository root. Create three anonymous
   pipes with `CreatePipe`: stdin `(read, write)`, stdout `(read, write)`, and
   stderr `(read, write)`. Each returned value must be a valid ordinary kernel
   handle. The stdin read handle and stdout/stderr write handles are created
   inheritable. Immediately clear `HANDLE_FLAG_INHERIT` on the stdin write and
   stdout/stderr read handles with `SetHandleInformation`, then prove all six
   states with `GetHandleInformation`. Set `STARTF_USESTDHANDLES`, with the
   still-open stdin read handle as `hStdInput` and the two output write handles
   as `hStdOutput` and `hStdError`.
4. After `STARTUPINFOEXW` and the attribute-list backing storage are complete,
   close the sole parent-owned stdin write handle exactly once and before
   entering `CreateProcessW`. The valid inherited stdin read handle then
   produces EOF because no writer remains. The exact
   `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, in order, is `[stdin_read,
   stdout_write, stderr_write]`. All three entries remain valid and inheritable
   through `CreateProcessW`; no closed, pseudo, unrelated, or additional
   handle is inheritable or listed. On successful creation, close the parent's
   copies of those three inherited handles immediately. Retain only the
   noninheritable stdout/stderr read handles for bounded draining. On failed
   creation, close every still-owned pipe handle. Every branch closes every
   owned handle exactly once. Cleanup must eagerly attempt each close in the
   exact reverse-ownership order even after an earlier close fails, aggregate
   all close outcomes without boolean short-circuiting, and set
   `cleanup_confirmed=false` if any close fails. Track successful
   `InitializeProcThreadAttributeList` completion separately from allocation;
   call `DeleteProcThreadAttributeList` exactly once only after successful
   initialization and never merely because backing storage or a pointer exists.
5. The Unicode environment block contains only exact current values for
   `SystemRoot` and `WINDIR`, plus
   `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, and `PYTHONUTF8=1`.
   Missing or duplicate case-insensitive names fail before launch. `PATH`,
   Python path/home overrides, credentials, tokens, proxy values, and every
   other ambient variable are not inherited or serialized.
6. Before creation, create one private Job Object with
   `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and `ActiveProcessLimit=1`, and attach
   one I/O completion port while the job is still empty. Do not set
   `JOB_OBJECT_LIMIT_BREAKAWAY_OK` or
   `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK` on the private job.
7. Call `CreateProcessW` with `bInheritHandles=TRUE` and exactly
   `CREATE_SUSPENDED`, `CREATE_NO_WINDOW`, `CREATE_UNICODE_ENVIRONMENT`, and
   `EXTENDED_STARTUPINFO_PRESENT`, plus only the flag selected by the closed
   ambient-job table below. No other creation flag is permitted.
8. Before resuming the target, assign its returned process handle to the
   private job, prove the job contains exactly that one process, query the
   process image privately, and reproduce the accepted executable identity.
   Assignment, identity, or parentage ambiguity terminates the suspended
   process, closes the job, and is `direct_interpreter_preflight_unknown`.
9. Resume exactly the returned primary thread once. The returned target
   process is the one top-level process.
10. Observe the job completion stream, process handle, and job accounting until
   exit. Any new process event other than the admitted target, any
   active-process-limit notification, or any accounting state above one active
   process is `direct_interpreter_preflight_descendant_observed`.
11. Bound stdout and stderr to 4,096 bytes each. Overflow, incomplete drain,
    nonempty output, missing exit code, nonzero exit code, or process-image
    drift is `direct_interpreter_preflight_unknown`.
12. The wall-clock deadline is 30 seconds. On timeout or any terminal failure,
    terminate the job, wait for `ACTIVE_PROCESS_ZERO`, drain bounded pipes,
    and close every thread, process, pipe, completion-port, and job handle.
13. Revalidate the private executable after target exit. Cleanup is confirmed
    only when the job reports zero active processes, all owned handles close,
    no matching target survives, both post-inventories and the residue
    projection are exact and equal to their pre-observations, and every derived
    local-effect count is zero under the closed profile above.

### Closed ambient-job selector

The adapter calls `IsProcessInJob(GetCurrentProcess(), NULL, ...)` exactly
once before any pipe, job, or target creation. API failure is
`ambient_membership_unreadable`. When membership is true, it calls
`QueryInformationJobObject(NULL, ...)` exactly once for each of
`JobObjectExtendedLimitInformation` and `JobObjectBasicUIRestrictions` and
requires the exact structure size and return length. The first query supplies
only the immediate job's `LimitFlags`; the second supplies the one native
unsigned 32-bit `JOBOBJECT_BASIC_UI_RESTRICTIONS.UIRestrictionsClass` scalar.
No nested member exists or may be inferred. It also reads
`sys.getwindowsversion()` once to determine whether the host is Windows 8 /
Server 2012 or later, where nested jobs exist. These values remain bounded
in-memory facts and are never serialized.

Apply the rows below in order. `base` means the four fixed creation flags in
requirement 7. `reject` means `observation_binding_rejected`, no
`CreateProcessW` entry, unconsumed authority, and complete local handle
cleanup. `silent` takes precedence when both breakaway bits are set.

| Row | Exact observed state | Creation flags | Exact post-create action | Result |
| --- | --- | --- | --- | --- |
| AJ-01 | membership API failed or did not return one boolean | none | none | reject |
| AJ-02 | `in_job=false` | `base` | assign target to the private job once | proceed once |
| AJ-03 | `in_job=true` and either exact job/version query failed or a job query returned the wrong byte count | none | none | reject |
| AJ-04 | exact job facts and `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK=true` | `base` | rely on silent breakaway, then assign target to the private job once | proceed once |
| AJ-05 | exact job facts, silent false, and `JOB_OBJECT_LIMIT_BREAKAWAY_OK=true` | `base + CREATE_BREAKAWAY_FROM_JOB` | request explicit breakaway, then assign target to the private job once | proceed once |
| AJ-06 | exact job facts, both breakaway bits false, nested jobs supported, and `UIRestrictionsClass=0` | `base` | inherit the ambient chain, then assign target to the private nested job once | proceed once |
| AJ-07 | exact job facts, both breakaway bits false, and nested jobs unsupported | none | none | reject |
| AJ-08 | exact job facts, both breakaway bits false, nested jobs supported, and `UIRestrictionsClass!=0` | none | none | reject |

No row probes by launching. AJ-04 and AJ-05 still require exact post-creation
private-job assignment and readback; an unobservable ancestor-job effect or
assignment failure is the single consumed unknown outcome, not permission to
retry with AJ-06. AJ-06 requires the private job to have zero UI restrictions
and relies only on the documented nested-job relation. Unknown membership,
query, version, flag, or UI facts select a reject row. Focused tests must cover
all eight rows, including both breakaway bits true, malformed query lengths,
and every rejected state. The selector has eight reachable rows with overlap,
uncovered, and unreachable counts `0/0/0`. Its 19-tuple reduced domain has
outcome counts AJ-01 through AJ-08 of `1/1/1/8/4/1/2/1`.

The job limit is enforcement, not permission for a child. A child-start event
or active-process-limit notification is terminal. Completion-port message
delivery is not treated as guaranteed; absence of a message is never the sole
proof of absence. Success instead requires the non-breakaway one-process limit,
the pre-resume one-target accounting readback, no contradictory notification,
and final zero-active-process accounting. The zero-descendant rule is not
weakened merely because Windows prevented a child from remaining active.

## Closed Result Schema

On a sealable terminal route, the executor emits exactly one canonical
`trusted_owner_r0_direct_interpreter_preflight_result.v1` object to stdout and
nothing else. Keys appear in the order below. Unknown, duplicate, missing,
reordered, or mistyped fields fail closed. After exact CLI admission, an
unsealable route emits no JSON object and instead uses the terminal-boundary
tracker projection defined above.

1. `schema_version`: exact schema string.
2. `repository_id`: integer `1235264383`.
3. `issue_number`: integer `780`.
4. `executor_contract_sha256`: lowercase SHA-256 selected by the accepted
   contract review.
5. `executor_contract_review_sha256`: lowercase SHA-256 of that review.
6. `parent_contract_sha256`: exact parent contract SHA-256.
7. `parent_review_sha256`: exact parent review SHA-256.
8. `harness_sha256`: exact accepted harness SHA-256.
9. `harness_test_sha256`: exact accepted harness-test SHA-256.
10. `executor_sha256`: SHA-256 of the running executor file.
11. `executor_test_sha256`: exact independently reviewed test-file SHA-256.
12. `direct_interpreter_binding_sha256`: exact public binding self-digest.
13. `observed_at_utc`: whole-second RFC3339 UTC string.
14. `preflight_authority_consumed`: boolean.
15. `public_bindings_exact`: boolean.
16. `private_binding_exact`: boolean.
17. `top_level_identity_exact`: boolean; for a launched target this is true
    only when both pre-resume and post-exit executable identity are exact.
18. `parentage_known`: boolean.
19. `exit_status`: one of `not_started`, `zero`, `nonzero`, or `unknown`.
20. `stdout_byte_count`: integer from `0` through `4096`.
21. `stderr_byte_count`: integer from `0` through `4096`.
22. `top_level_process_count`: integer `0` or `1`.
23. `descendant_process_count`: nonnegative cumulative count of distinct
    non-target process-start or active-process-limit evidence; an enforced
    attempt counts even if no descendant remains active.
24. `descendant_attempt_detected`: boolean; true exactly when field 23 is
    greater than zero.
25. `timed_out`: boolean.
26. `cleanup_confirmed`: boolean.
27. `output_complete`: boolean.
28. `process_launch_count`: integer `0` or `1`.
29. `retry_count`: integer `0`.
30. `repository_write_count`: integer `0`; derived from the exact mode-specific
    repository rule under the local-effect profile, never inserted.
31. `installed_write_count`: integer `0`; derived from the exact mode-specific
    installed-tree rule under the local-effect profile, never inserted.
32. `network_operation_count`: integer `0`; it is derived, never inserted, and
    equals only the executor-owned network operations observed by the outer
    preflight executor's exact audit boundary. It has no child contribution.
    Zero means only that the executor observed zero executor-owned network
    operations. It does not establish child-network prevention, complete
    native-network observation, firewall denial, or technical impossibility.
33. `external_effect_count`: integer `0`; the mode-specific exact checked sum
    of repository writes, installed writes, generated-residue delta, and the
    executor-owned network operation count. No child-network term is inserted
    or inferred. A nonzero or unavailable source cannot produce this field.
34. `private_value_emitted`: boolean `false`.
35. `result_status`: exactly one of the six closed values in `Result And Exit
    Semantics` below.
36. `eligible_for_independent_review`: boolean; exactly `true` for every
    completely sealed, projection-valid, read-back-equivalent stdout object.
    It means only that Codex E may review the object, not that an observation
    decision is eligible.
37. `authority_flags`: the parent's exact 16-field all-false object.
38. `result_sha256`: SHA-256 of the same object with this field omitted.

Canonical encoding is compact JSON, UTF-8 without BOM, no insignificant
whitespace, insertion order as listed, and exactly one final LF. Maximum
stdout is 4,096 bytes. The successful preflight known-answer vector is active
and structurally reachable whenever every non-network precondition and every
terminal success fact is exact:

```json
{"schema_version":"trusted_owner_r0_direct_interpreter_preflight_result.v1","repository_id":1235264383,"issue_number":780,"executor_contract_sha256":"1111111111111111111111111111111111111111111111111111111111111111","executor_contract_review_sha256":"2222222222222222222222222222222222222222222222222222222222222222","parent_contract_sha256":"17d0d2f5fe965643888ea70c71a278afdb7797033c311252bce1dde56486ea84","parent_review_sha256":"0fd7d921a92fbd58576f053a0e8938d3ae4a0266e9a023b762f933e65aee450f","harness_sha256":"001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6","harness_test_sha256":"3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3","executor_sha256":"3333333333333333333333333333333333333333333333333333333333333333","executor_test_sha256":"4444444444444444444444444444444444444444444444444444444444444444","direct_interpreter_binding_sha256":"2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333","observed_at_utc":"2026-08-01T00:00:00Z","preflight_authority_consumed":true,"public_bindings_exact":true,"private_binding_exact":true,"top_level_identity_exact":true,"parentage_known":true,"exit_status":"zero","stdout_byte_count":0,"stderr_byte_count":0,"top_level_process_count":1,"descendant_process_count":0,"descendant_attempt_detected":false,"timed_out":false,"cleanup_confirmed":true,"output_complete":true,"process_launch_count":1,"retry_count":0,"repository_write_count":0,"installed_write_count":0,"network_operation_count":0,"external_effect_count":0,"private_value_emitted":false,"result_status":"direct_interpreter_preflight_passed","eligible_for_independent_review":true,"authority_flags":{"repository_mutation_authorized":false,"implementation_authorized":false,"publication_authorized":false,"merge_authorized":false,"deployment_authorized":false,"installation_authorized":false,"package_operations_authorized":false,"network_authorized":false,"secrets_authorized":false,"external_isolation_authorized":false,"canary_authorized":false,"stage4_authorized":false,"stage_advancement_authorized":false,"dispatch_authorized":false,"live_ready":false,"trusted_owner_native_profile_ready":false},"result_sha256":"7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56"}
```

The fixture hashes in fields 4, 5, 10, and 11 are KAT values, not current
artifact claims. The vector has a 2,156-byte self-digest preimage, a
2,239-byte complete object, self-digest
`7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56`,
and complete artifact SHA-256
`cdcb9a8155006d0fe458e5a486c3d86eb83bf85316aba0afdfd21899587cb807`.

### Normalized terminal facts and exact result projections

Before serialization, the executor creates one internal typed source record
with these keys in this order: `historical_direct_use_proven`,
`public_binding_state`, `owner_decision_state`, `private_binding_state`,
`ambient_job_state`, `precreate_setup_state`, `create_call_entered`,
`create_return_state`,
`top_level_identity_exact`, `parentage_known`, `exit_status`,
`stdout_byte_count`, `stderr_byte_count`, `top_level_process_count`,
`descendant_process_count`, `descendant_attempt_detected`, `timed_out`,
`effect_derivation_state`, `repository_write_count`, `installed_write_count`,
`generated_residue_delta_count`, `executor_network_operation_count`,
`cleanup_confirmed`, and `output_complete`. This record is bounded memory, not
a durable schema or public object. It contains no caller-supplied or
preselected projection identifier.

The closed source-state domains are:

- `historical_direct_use_proven`: boolean derived only from retained evidence;
- `public_binding_state`: `not_observed`, `rejected`, or `exact`;
- `owner_decision_state`: `not_observed`, `rejected`, or `exact`;
- `private_binding_state`: `not_observed`, `rejected`, or `exact`;
- `ambient_job_state`: `not_observed`, `rejected`, or `admitted`;
- `precreate_setup_state`: `not_observed`, `failed_no_process`, or `complete`;
  `complete` may be recorded only when all step-8 setup is exact and execution
  enters `CreateProcessW`; any setup failure, interruption, or pre-entry
  uncertainty is `failed_no_process`;
- `create_call_entered`: boolean derived at the first instruction of the exact
  `CreateProcessW` call; and
- `create_return_state`: `not_entered`, `failed_no_process`, or
  `succeeded_one_process`;
- `effect_derivation_state`: `early_terminal_structural_zero` or
  `sampled_exact_zero`; and
- `repository_write_count`, `installed_write_count`,
  `generated_residue_delta_count`, and `executor_network_operation_count`:
  integer zero derived by the selected exact local-effect mode. A nonzero,
  unreadable, overflowing, unstable, ambiguous, or invalid observation cannot
  construct this source record and never becomes zero.

Those stage states are sequential. Historical proof requires every later
state to be `not_observed`. A rejected stage requires every later stage to be
`not_observed`. An exact/admitted stage requires every earlier stage to have
passed. Ambient inspection is permitted after public, owner, and private
states are `exact`. `CreateProcessW` may be entered only after those states are
exact, ambient state is `admitted`, and pre-create setup is `complete`.
Ambient admission requires setup to become either
`failed_no_process` or `complete`; it cannot remain `not_observed` in a
terminal record. `precreate_setup_state=failed_no_process` requires
`create_call_entered=false` and `create_return_state=not_entered`.
`precreate_setup_state=complete` requires
`create_call_entered=true` and a create return of `failed_no_process` or
`succeeded_one_process`. Any other combination is an invalid source record and
cannot produce JSON.

The effect derivation is also sequential. Historical proof, public rejection,
owner rejection, private rejection, and ambient rejection require
`early_terminal_structural_zero`. Pre-create setup failure, known create
failure, and every post-create route require `sampled_exact_zero`. The first
mode requires `effect_boundary_state=not_entered`; the second requires
`effect_boundary_state=entered`. A route/mode mismatch is source-state
corruption and cannot produce JSON.

The reduced normalized source-state audit enumerates `5,832` combinations
(`2 * 3^6 * 2 * 2`) of the historical boolean, six three-valued
stage/setup/create states, `create_call_entered`, and the two derivation modes.
Exactly eight sequential route/mode pairs are valid, `5,824` are rejected,
and overlap is zero. The eight routes
are historical proof, public rejection, owner rejection, private rejection,
ambient rejection, pre-create setup failure, known create failure, and
successful creation. These are in-memory contract audits, not runtime search
or durable schema. The four public effect counters remain projection facts in
this source-state audit and are independently closed by the 72-tuple raw
local-effect selector. Every exact emitted row requires all four public counts
and the internal residue count to be zero; every nonzero, unreadable,
ambiguous, or invalid effect state bypasses source-record construction and is
covered by terminal-diagnostic and negative fixtures.

The projector first enforces these invariants:

- `public_bindings_exact` is true exactly when
  `public_binding_state=exact`;
- `private_binding_exact` is true exactly when
  `private_binding_state=exact`;
- `preflight_authority_consumed` equals `create_call_entered`;
- `process_launch_count` and `top_level_process_count` are both `1` exactly
  when `create_return_state=succeeded_one_process`, otherwise both are `0`;
- `create_call_entered=false` requires `create_return_state=not_entered`;
- PR-01 through PR-05 require
  `effect_derivation_state=early_terminal_structural_zero`; PR-05A through
  PR-09 require `effect_derivation_state=sampled_exact_zero`;
- `early_terminal_structural_zero` requires no effect-boundary entry, no
  attempt-owned setup resource, exact closure of any metadata handle, an exact
  zero audit, and the route-specific pre-inventory state; it does not assert
  pre/post tree equality;
- `sampled_exact_zero` requires exact pre-inventories, exact equal
  post-inventories, exact zero audit and row deltas, and completion of every
  required post-observation attempt;
- `precreate_setup_state=failed_no_process` requires unconsumed authority,
  zero process/output/descendant facts, `timed_out=false`,
  `exit_status=not_started`, and `output_complete=true`; cleanup may be true or
  false and is reported exactly;
- `create_return_state=failed_no_process` requires call entry, zero process counts,
  `exit_status=not_started`, zero output, no descendant, no timeout, complete
  output, and confirmed closure of every locally owned handle;
- a successful create requires call entry, both process counts equal to `1`,
  and `exit_status` other than `not_started`;
- `descendant_attempt_detected` is true exactly when
  `descendant_process_count>0`; an active-process-limit or non-target-start
  event increments this cumulative evidence count even when Windows prevents
  a descendant from remaining active;
- output counts are retained byte counts in `0..4096`; overflow sets
  `output_complete=false` rather than fabricating a larger count; and
- every emitted object derives, rather than assumes, every
  write/network/external-effect count; has `retry_count=0`,
  `private_value_emitted=false`, the exact all-false authority object, and
  `eligible_for_independent_review=true`;
- public `network_operation_count` equals the bounded internal
  `executor_network_operation_count` exactly and has no child contribution;
  its required zero value must be derived from the executor's observation,
  never inserted; and
- `external_effect_count` is the exact mode-specific sum of
  `repository_write_count`, `installed_write_count`,
  `generated_residue_delta_count`, and `executor_network_operation_count`.

It then derives exactly one row below from those facts. `0/0` under `out/err`
means both byte counts are zero; `bounded` means each is `0..4096`; `0/0`
under `top/launch` means both process counts are zero. `F` and `T` are exact
booleans, while `bool` is an observed boolean constrained by the row. In the
source route column, `later=not_observed` binds every later stage state.
Every table row also binds the effect derivation mode by the PR-01-through-05
and PR-05A-through-09 split above. Omitting or flipping that mode matches zero
rows.

| Projection | Exact source route | consumed | public | private | identity/parent | exit | out/err | top/launch | descendants `(count, attempt)` | timeout | cleanup/complete | Exact public status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-01 historical proof | `history=T; later=not_observed` | F | F | F | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `direct_interpreter_hypothesis_rejected` |
| PR-02 public drift | `history=F; public=rejected; later=not_observed` | F | F | F | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `observation_binding_rejected` |
| PR-03 authority rejected | `history=F; public=exact; owner=rejected; later=not_observed` | F | T | F | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `direct_interpreter_preflight_required` |
| PR-04 private binding rejected | `history=F; public=exact; owner=exact; private=rejected; later=not_observed` | F | T | F | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `observation_binding_rejected` |
| PR-05 ambient job rejected | `history=F; public/owner/private=exact; ambient=rejected; later=not_observed` | F | T | T | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `observation_binding_rejected` |
| PR-05A pre-create setup failure | `history=F; public/owner/private=exact; ambient=admitted; setup=failed_no_process; create=not_entered` | F | T | T | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(bool,T)` | `direct_interpreter_preflight_unknown` |
| PR-06 known create failure | `history=F; public/owner/private=exact; ambient=admitted; setup=complete; create=failed_no_process` | T | T | T | `(F,F)` | `not_started` | 0/0 | 0/0 | `(0,F)` | F | `(T,T)` | `direct_interpreter_preflight_unknown` |
| PR-07 post-create unknown | `all non-network prerequisites passed; create=succeeded_one_process; early_unknown=T OR (early_unknown=F; descendant=F; late_unknown=T)` | T | T | T | `(bool,bool)` | `zero`, `nonzero`, or `unknown` | bounded | 1/1 | `(>=0,bool)` | bool | `(bool,bool)` | `direct_interpreter_preflight_unknown` |
| PR-08 descendant observed | `all non-network prerequisites passed; create=succeeded_one_process; early_unknown=F; descendant=T` | T | T | T | `(T,T)` | `zero` or `nonzero` | bounded | 1/1 | `(>0,T)` | F | `(T,bool)` | `direct_interpreter_preflight_descendant_observed` |
| PR-09 passed | `all non-network prerequisites passed; create=succeeded_one_process; early_unknown=F; descendant=F; late_unknown=F` | T | T | T | `(T,T)` | `zero` | 0/0 | 1/1 | `(0,F)` | F | `(T,T)` | `direct_interpreter_preflight_passed` |

The post-create predicates reproduce the accepted parent classifier exactly:

- `early_unknown` is `timed_out=true`, `cleanup_confirmed=false`,
  `top_level_identity_exact=false`, `parentage_known=false`, or
  `exit_status=unknown`;
- `descendant` is `descendant_process_count>0`, which is equivalent to
  `descendant_attempt_detected=true`; and
- `late_unknown` is `exit_status=nonzero`, nonzero stdout or stderr, or
  `output_complete=false`.

Evaluate those predicates in that order. A descendant-plus-timeout or
descendant-plus-cleanup-uncertainty witness selects PR-07. With no early
unknown, descendant evidence selects PR-08 even when a late-output or nonzero
failure co-occurs. An all-success-shaped object cannot claim unknown.
Post-exit identity drift is projected as `top_level_identity_exact=false`.

Fields 1 through 13 use their exact bound values and field 13 uses the one
whole-second observation instant. Field 38 is computed only after all row
constraints pass. If the normalized facts violate an invariant, match zero or
multiple rows, or the object cannot be sealed, no JSON object is emitted. After
exact CLI admission, emit the exact tracker-selected diagnostic and exit `3`;
the generic sentinel is available only before tracker creation or when exact
terminal emission cannot be established. No contradictory object may be
normalized into a nearby row.

For PR-05A, the exact canonical object is the public-safe terminal disposition
for the uniquely bound owner decision. A fresh task must validate and retain
that object with the decision evidence before accepting any later authority.
If the PR-05A object is absent, malformed, or unsealed after setup entry, an
exact `precreate` tracker selects the precreate diagnostic and
`retired_unconsumed_precreate_failure_nonreusable`; `consumed=false` is never
evidence that setup may be retried. Ambiguous tracker, output, or decision
association selects the ambiguous diagnostic and a conservatively consumed
disposition. This reconciliation rule introduces no publication path or new
schema field.

PR-05A may carry `cleanup_confirmed=false` only when the sampled local-effect
evidence is still exact zero and a separate E-004 resource-close fact is false.
If post sampling is unavailable, drifted, or nonzero, no PR-05A object exists;
the tracker-selected diagnostic is the only output. The equivalent rule applies
to PR-06 through PR-09, with consumption derived solely from
`create_call_entered`; ambiguity remains consumed and nonreusable.

The reduced selector domain contains eight sequential prefix routes, with the
PR-05A setup-failure route expanded across exact cleanup true/false, plus the
eight products of `early_unknown`, `descendant`, and `late_unknown` after
successful creation. Its 16 tuples select PR-01, PR-02, PR-03, PR-04, PR-05,
PR-05A, PR-06, PR-07, PR-08, and PR-09 with counts
`1/1/1/1/1/2/1/5/2/1` and overlap, uncovered, and unreachable counts
`0/0/0`. The descendant-plus-timeout witness is one of the four early-unknown
products; the two PR-08 products differ only on late failure.

Focused tests contain exactly 16 positive fixtures, one for each reduced
selector tuple. They contain ten negative fixtures made by flipping only
`preflight_authority_consumed` in one canonical fixture for each row and ten
more made by flipping only `effect_derivation_state` in one canonical fixture
for each row. They also contain eleven single-defect fixtures: passed with consumption false,
exit nonzero, launch zero, stdout nonzero, timeout true, cleanup false, or
incomplete output; binding-rejected prelaunch with consumption true or launch
one; setup failure with launch one; and unknown with every pass-shape fact.
All 31 negative fixtures must be rejected before hashing. Total projection
fixtures are `47`.

## Result And Exit Semantics

The executor must call the accepted parent classifier for every conditional
post-create route. It may not reinterpret a parent outcome. The only
`result_status` values are:

- `direct_interpreter_hypothesis_rejected`;
- `observation_binding_rejected`;
- `direct_interpreter_preflight_required`;
- `direct_interpreter_preflight_descendant_observed`;
- `direct_interpreter_preflight_unknown`; and
- `direct_interpreter_preflight_passed`.

Exit codes are `0` for passed, `2` for hypothesis/binding/required, `3` for
unknown, and `4` for descendant observed. When a canonical object cannot be
sealed after exact CLI admission, stdout is empty, stderr is the one exact
diagnostic selected by the public-safe terminal fallback boundary, and exit
code is `3`. The existing generic unknown sentinel remains valid only before
tracker creation or when no exact fallback diagnostic can be emitted. Raw
paths, identities, PIDs, handles, commands, environment values, Win32 errors,
exceptions, traces, stdout, or stderr from the target are never emitted.

Only `direct_interpreter_preflight_passed` plus fresh independent Codex E
acceptance may make a separate owner observation decision eligible. That state
is active and structurally reachable whenever every non-network prerequisite
and terminal success fact is exact. Every outcome is terminal for this
preflight authority. A passed preflight is single-use and cannot be rerun for
confidence or evidence strengthening.

## Lifecycle Precedence

Before applying a public projection row, normalize the raw local-effect record.
LE-03 through LE-05 prohibit `SourceRecord` construction and therefore prohibit
every JSON row below. Emit only the exact fallback diagnostic selected from the
monotonic terminal-boundary tracker, retire the attempt, and derive consumption
solely from the tracker's exact `create_entered` fact. Ambiguous tracker or
terminal bytes are conservatively consumed. This sealing guard is not a new
lifecycle status and cannot be bypassed by an earlier binding classification.

When the sealing guard admits LE-01 or LE-02, apply first match:

1. retained proof that the historical attempt used this exact interpreter ->
   `direct_interpreter_hypothesis_rejected`, no launch;
2. public artifact, review, implementation, issue, or protected-surface drift
   -> `observation_binding_rejected`, no launch;
3. missing, stale, expired, reused, scope-mismatched, or unverifiable owner
   preflight decision -> `direct_interpreter_preflight_required`, no launch;
4. fixed-root derivation, any required pre-inventory, private ingress, or any
   prelaunch executable observation is not exact ->
   `observation_binding_rejected`, no launch;
5. the ambient-job selector chooses AJ-01, AJ-03, AJ-07, or AJ-08 ->
   `observation_binding_rejected`, no launch;
6. step-8 local setup fails, is interrupted, or cannot be proved complete
   before `CreateProcessW` entry -> `direct_interpreter_preflight_unknown`, no
   launch, `preflight_authority_consumed=false`, and owner decision disposition
   `retired_unconsumed_precreate_failure_nonreusable` after exact local cleanup
   projection;
7. `CreateProcessW` was entered and returned a known failure with no process
   object -> `direct_interpreter_preflight_unknown`, consumed;
8. after setup entry, timeout or resource-cleanup uncertainty,
   identity/parentage uncertainty including post-exit identity drift, or exit
   uncertainty occurs while sampled effect evidence remains exact zero ->
   `direct_interpreter_preflight_unknown`; consumption equals
   `create_call_entered`;
9. with row 8 false, a non-target job process event or active-process-limit
   event occurs -> `direct_interpreter_preflight_descendant_observed`,
   consumed;
10. with rows 8 and 9 false, nonempty output, nonzero exit, or output overflow
    occurs -> `direct_interpreter_preflight_unknown`, consumed; and
11. exact binding, one target, no descendant event, exit `0`, empty complete
    output, exact post-exit identity, confirmed cleanup, and sealed result ->
    `direct_interpreter_preflight_passed`, consumed.

The sealing guard owns post-inventory unreadability, exact drift, nonzero or
ambiguous effect counts, and invalid effect source states before any public
row. Row 8 owns descendant-plus-timeout and descendant-plus-resource-cleanup
uncertainty only when effect derivation is sampled exact zero.
Row 9 owns descendant-plus-row-10 output or nonzero failures. Row 10 requires
`descendant_attempt_detected=false`.
No broader earlier row shadows a known later outcome. Unknown facts fail
closed. For row 6, the canonical pair
`preflight_authority_consumed=false` and
the exact result status is a public-safe terminal disposition;
exact cleanup is retained separately in `cleanup_confirmed`. A missing,
malformed, unsealed, or ambiguous row-6 result still retires that decision,
and every fresh task must reject it rather than retry setup.
No terminal row authorizes retry, fallback, an observation, or receipt
publication.

The contract-review selector audit uses booleans
`historical_direct_use_proven`, `public_bindings_exact`,
`owner_decision_exact`, and `private_binding_exact`, plus parent state
`{not_run, descendant, unknown, passed}`. Across all 64 tuples, first-match
outcome counts are:

- `direct_interpreter_hypothesis_rejected`: `32`;
- `observation_binding_rejected`: `20`;
- `direct_interpreter_preflight_required`: `9`;
- `direct_interpreter_preflight_descendant_observed`: `1`;
- `direct_interpreter_preflight_unknown`: `1`; and
- `direct_interpreter_preflight_passed`: `1`.

Independent review must reproduce `overlap_count=0`, `uncovered_count=0`, and
`unreachable_outcome_count=0` for this 64-tuple parent selector, the eight-row
ambient-job selector, the 72-tuple raw local-effect selector, the 5,832-tuple
normalized source-state audit, and the ten-row result-projection matrix. It
must also
confirm at least one process-entry route and the exact passing route are
structurally reachable when every non-network prerequisite is exact. These audits
are review evidence only; they create no durable schema, runtime search,
retry, or authority packet.

## Side Effects

Contract writing: exactly this docs file. The historical terminal-unknown
attempt remains consumed and nonreusable; this amendment cannot reinterpret,
repair, continue, or rerun it.

Future implementation or Codex D correction, only after separate owner
authorization: exactly the two current reviewed implementation files named
above. It adds only the local monotonic tracker, three fixed fallback byte
constants, selection at the outer terminal boundary, and focused tests. It
creates no third implementation path or broader diagnostic mechanism.

A separately authorized future synthetic preflight may create exactly one
top-level process plus its attempt-owned pipes and Job Object, then must clean
them completely. It creates no file, directory, issue comment, receipt,
registry entry, release record, claim, task, worktree, command record, package
operation, installed mutation, or persistent external effect. This contract
does not authorize that preflight.

## Required Tests

Codex D must use fake adapters only; implementation and review do not launch
the real interpreter. Focused tests must prove:

1. exact runtime rejection of contract-review, predecessor-review,
   implementation-review, parent, harness, and executor-test drift; raw
   executor measurement without an embedded expected executor digest; and
   independent external rejection when either implementation hash differs from
   the E-accepted owner binding;
2. strict stdin framing and path no-echo;
3. no argv, environment, PATH, registry, alias, shell, or fallback ingress;
4. accepted validator and classifier reuse without copied binding logic;
5. exact fixed-root derivation, the sole top-level `.git` exclusion, no
   installed-tree exclusions, and rejection of alternate `CODEX_HOME`, missing,
   reparse, nonordinary, escaped, duplicate, or case-colliding roots or rows;
6. stable pre/post inventory of added, removed, modified, renamed, and
   kind-changed rows; before/open/after identity drift; second-enumeration drift;
   unreadability; and every row, byte, path, and monotonic-time budget boundary;
7. the exact residue predicate, unchanged preexisting residue acceptance, new,
   removed, and modified residue rejection, fixed sampling order, and no durable
   path or snapshot emission;
8. exact `early_terminal_structural_zero` derivation without a tree-equality
   claim, exact sampled attempt-plus-row sums, residue delta, checked
   external-effect sum, deliberate residue double contribution, and
   tracker-selected diagnostic output rather than a zero-count object for every
   nonzero, unavailable, or invalid source;
9. the 72-tuple raw local-effect selector reproduces literal and
   first-applicable counts `3/1/6/8/54` with overlap, uncovered, and
   unreachable counts `0/0/0`;
10. one exact executor audit owner derives
   `executor_network_operation_count`; public `network_operation_count` equals
   that count, never a literal, and contains no child contribution;
11. zero executor-owned network events means only zero executor-owned observed
   operations; tests reject any child-isolation, complete-observation, firewall,
   or technical-impossibility claim and prove child evidence is not a setup,
   process-entry, passing-result, review, or later-eligibility prerequisite;
12. every proven-owned handle receives exactly one close attempt in reverse
   ownership order even after an earlier failure, all close failures aggregate,
   and any failed close leaves cleanup unconfirmed;
13. `DeleteProcThreadAttributeList` is called exactly once only after successful
   attribute-list initialization, with injected failures covering allocation,
   first-size query, initialization, update, and later cleanup stages;
14. the active conditional boundary preserves the fixed command vector, cwd,
    environment, output, timeout, and one-launch limits;
15. one valid EOF-producing stdin pipe, exact three-handle inheritance list,
    writer-close point, and all success/failure handle-ownership transitions;
16. all eight ambient-job rows, the exact unsigned 32-bit
    `UIRestrictionsClass` member, exact query classes and return lengths, exact
    creation flags, no launch probe, and no retry;
17. the `5,832`-tuple normalized source-state audit admits exactly eight
    sequential route/mode pairs and rejects `5,824` with no overlap, including
    reachable process-entry and passing routes;
18. both cleanup-known and cleanup-uncertain pre-create setup failures emit the
    exact unconsumed-but-terminal PR-05A projection and require a fresh owner
    decision without retry;
19. job creation and limits precede target resume;
20. target assignment, one-process job readback, process-image validation, and
    parentage proof precede resume;
21. the accepted classifier maps timeout/cleanup/identity uncertainty before
    descendant evidence, then descendant evidence before late output/nonzero
    failures, with the two co-occurrence witnesses exact;
22. creation failure, timeout, unknown exit, nonempty or excessive output,
    identity drift, and uncertain cleanup are terminal and nonretryable;
23. the 64-tuple selector reproduces outcome counts `32/20/9/1/1/1` with
    audit `0/0/0`;
24. all 16 reduced-domain positive fixtures, ten consumption-flip negatives,
    ten derivation-mode-flip negatives, and eleven named contradiction fixtures
    reproduce counts `1/1/1/1/1/2/1/5/2/1` and projection audit `0/0/0`;
25. the one 38-field success KAT is byte-exact, active, and reachable, and
    malformed, duplicate, reordered, missing, unknown, or mistyped fields
    fail;
26. stdout/stderr never contain a supplied path, row path, file identity, or raw
    private value; and
27. the existing 121-test harness suite remains unchanged and passing.
28. invalid CLI arguments retain the exact generic 37-byte sentinel and do not
    create a stage or owner-decision claim;
29. after exact CLI admission, injected failures at every fallible boundary
    before `CreateProcessW` emit only the exact 58-byte precreate/unconsumed
    diagnostic;
30. the tracker transitions immediately before the one `CreateProcessW` call,
    and injected call-entry, call-return, post-create, timeout, effect,
    identity, projection, and cleanup failures emit only the exact 61-byte
    create-entered/consumed diagnostic when that transition is exact;
31. missing, duplicated, backward, contradictory, or unreadable tracker state
    emits only the exact 62-byte stage-ambiguous/consumed diagnostic;
32. all three diagnostics have exact ASCII bytes, one LF, no CR or BOM, empty
    stdout, exit code `3`, and the byte counts and SHA-256 values above;
33. partial, extra, reordered, CRLF-translated, or mixed diagnostic output is
    rejected and cannot establish a stage or unconsumed disposition;
34. no diagnostic contains a path, identity, PID, handle, command, environment
    value, exception, Win32 error, target output, or detailed failure reason;
    and
35. no diagnostic is accepted as a result object, receipt, retry authority,
    Observation 1 evidence, or rung-advancement evidence.

Required validation after implementation is:

```powershell
git diff --check
py -B -m pytest tests\test_run_role_pool_r0_direct_interpreter_preflight.py -q
py -B -m pytest tests\test_check_role_pool_r0_offline_observation.py -q
py -B -m ruff check tools\run_role_pool_r0_direct_interpreter_preflight.py tests\test_run_role_pool_r0_direct_interpreter_preflight.py
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Independent Codex E must additionally verify exact file hashes after all
tests, absence of an executor-owned self-admission digest or equivalent
checksum cycle, no real process execution, issue #769 and #780 comment counts,
zero matching target processes, and zero generated residue.

## Acceptance Criteria

Independent Codex E may accept this contract only if:

1. every current binding is exact and the prevalidator handoff is treated as
   non-authoritative routing evidence;
2. the accepted harness and test remain immutable owners of binding and
   classification semantics;
3. exactly the two reviewed current implementation paths are sufficient for D;
4. independent child-network prevention or complete observation is not an
   eligibility prerequisite, and no replacement field, status, schema, KAT,
   lifecycle, enforcement mechanism, or successor requirement remains;
5. `network_operation_count` derives only executor-owned observed operations,
   has no child contribution, and carries the exact child-network nonclaim;
6. `network_authorized=false` remains an authority denial rather than an
   isolation or completeness claim;
7. the local-effect profile closes the exact roots, sole `.git` exclusion,
   stable row algorithm, budgets, residue predicate, sampling order, audit
   ownership, pre-effect and sampled derivation modes, cleanup conjunction,
   72-tuple selector, and unreadable/drift terminal-diagnostic behavior without
   a durable schema or path emission;
8. the active Win32 order supplies only valid inherited handles, closes the stdin
   writer before launch, and prevents target execution before job assignment
   and exact process-image validation;
9. E-004 requires one close attempt per owned handle without short-circuiting
   and attribute-list deletion only after successful initialization;
10. one target and zero descendants remain strict in the active boundary, with
   no retry or fallback;
11. all ambient-job states choose one exact pre-consumption reject or one exact
    creation-flag path from the native `UIRestrictionsClass` scalar without
    probe-and-retry;
12. the private path has one bounded non-echo ingress and no durable output;
13. the sequential normalized source states, exact route/mode compatibility,
    ten projection classes including the unconsumed-terminal pre-create setup
    route, descendant-plus-timeout precedence, result schema, active success
    KAT, lifecycle, exit mapping, and authority ceiling are deterministic and
    closed;
14. implementation and fake tests require no real process launch;
15. any existing owner approval is not silently transferred across the new
    contract or future implementation bytes; and
16. executor-byte acceptance is externally owned by exact E-reviewed hashes
    repeated in the owner decision, while runtime admission checks only
    independently owned artifacts and reports its raw executor hash;
17. no sidecar, signature, key, wrapper, launcher, new schema, digest family,
    result field, status, process, or third implementation path was introduced;
18. the terminal fallback has exactly three post-admission diagnostics, one
    monotonic create-boundary tracker, no detailed stage or cause vocabulary,
    and conservative consumption on ambiguity;
19. the historical 37-byte terminal attempt remains consumed, unknown,
    nonreusable, and ineligible for reconstruction or retry;
20. the correction grants no implementation, private-path, preflight,
    observation, publication, release, R1-R8, Stage 4, or readiness authority;
    and
21. only this contract changed in B, issue #769 remains untouched, and
    generated residue is zero.

Contract acceptance sets only `owner_implementation_decision_eligible=true`.
Implementation remains separately owner-authorized and limited to the exact
two files. Contract review, implementation, implementation review, and a fresh
owner preflight decision remain distinct. No accepted artifact automatically
authorizes another process execution.

## Authority And Non-Claims

Current, post-contract, post-review, and terminal authority remains false for
implementation, private-path access, preflight execution, observation
consumption, observation execution, receipt publication, registry/release/
index mutation, installation, synchronization, task/claim/command/dispatch,
App Server, broker, service, canary, package operations, R1-R8, Stage 4,
submission, merge, deployment, live readiness, compatibility, reliability,
correctness, privacy, security, or assurance.

This contract does not claim that the direct interpreter caused or repairs the
historical descendant, that stable identity was revalidated after the supplied
prevalidator handoff, that a preflight ran, that child-network access is denied,
completely observed, firewall-blocked, or technically impossible, or that a
preflight or observation decision is eligible. The accepted harness audit count
means only Python audit events observed in the harness process. The outer
preflight count means only executor-owned events observed by the executor. It
also does not claim that mutable code can cryptographically authenticate its
own independent acceptance; that acceptance remains the external E/owner gate.

## Historical Next Workflow Action (Superseded)

Next role: fresh independent Codex E E-005 raw-effect predicate-disjointness
confirmation reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Independent R0 Direct-Interpreter E-005 Raw-Effect
Predicate-Disjointness Confirmation Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/780
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected coordination surface: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md

Accepted predecessor contract SHA-256:
d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848

Immediate predecessor before the local-effect closure SHA-256:
18fb661e49bb462397af091b6eea0c2fbbcc3549ffe105f08bcd1339e7301b14

Reviewed predecessor requiring this reconciliation SHA-256:
b6b2a2ff0bc1479f57ea62f5853b04dfea948feb098ac89077c4fe5041428094

Rejected superseded contract SHA-256:
bcc6a7e6e32b76503de9fdb42dcc95cb3cfce0720f7d3662cec005f9d969eefd

Accepted predecessor review SHA-256:
97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038

Source implementation review SHA-256:
49d66f9ce38f0fab01bbeebf02deba4451f87f45600a21552b47a3e9292e0dac

Source findings:
- ME-RP-780-PREFLIGHT-EXEC-E-004
- ME-RP-780-PREFLIGHT-EXEC-E-005

Independently recompute the revised contract and every public binding. Confirm
that the owner's trusted-owner rescope removes complete child-network
prevention or observation as an eligibility prerequisite without weakening the
fixed direct-interpreter command, one-process/zero-descendant topology,
single-use consumption, cleanup, local-effect, no-echo, or false-authority
boundaries.

Reproduce the exact local-effect profile. Confirm its fixed repository and
installed roots, sole top-level `.git` exclusion, stable ordinary/non-reparse
row algorithm, case-collision and second-enumeration checks, row/byte/path/time
budgets, residue predicate, audit ownership, and checked counts are
mechanically executable inside the two reviewed files. Independently verify
the closed ten-key raw observation record, the exact effect-boundary entry
point, pre/post sampling states, and both canonical derivation modes.

Confirm `early_terminal_structural_zero` is allowed only before the effect
boundary, with an exact-zero audit, no effect-capable call, exact metadata
handle closure, and no tree-equality claim. Confirm `sampled_exact_zero`
requires exact pre-inventories, exact-equal post-inventories, and exact-zero
audit and deltas. Confirm every nonzero, unavailable, or invalid effect source
emits only the existing unknown sentinel, never a zero-count JSON object.
Confirm no path, row, file identity, or snapshot is durable or public and that
no new public schema, field, status, KAT, digest family, or third
implementation path was added.

Confirm the accepted harness audit guard still reports only Python audit events
observed in that harness process. Confirm outer preflight
network_operation_count equals only executor-owned events observed by the
executor, has no child contribution, and is derived rather than inserted. A
zero value must mean only zero executor-owned observed network operations.
Confirm the contract expressly makes no child-network denial, complete native
observation, firewall, or impossibility claim and that network_authorized=false
is an authority denial rather than an isolation claim.

Confirm no child-network state, status, schema, KAT, lifecycle row, selector
dimension, enforcement mechanism, or successor requirement remains. Strictly
parse the one active 38-field success KAT and recompute its 2,156-byte preimage,
2,239-byte complete object, self-digest
7afecf48375ce52d88fa4e2afd8abccd5fb315bf691b30d17a3a6d21be481a56,
and artifact SHA-256
cdcb9a8155006d0fe458e5a486c3d86eb83bf85316aba0afdfd21899587cb807.

Reproduce the 5,832-state normalized source audit with 8 valid and 5,824
rejected; the 72-tuple raw local-effect selector counts 3/1/6/8/54; the
64-tuple parent selector counts 32/20/9/1/1/1; the 16-tuple projection counts
1/1/1/1/1/2/1/5/2/1; all 47 projection fixtures; and overlap, uncovered, and
unreachable counts 0/0/0. Confirm at least one process-entry route and the
exact passing route are structurally reachable whenever all non-network
preconditions and sampled zero-effect facts are exact.

Evaluate LE-01 through LE-05 as literal predicate sets without first-match
short-circuiting. Confirm the previously overlapping tuple of entered boundary,
exact pre-inventory, failed/ambiguous post-inventory, and nonzero audit matches
LE-04 only. Require literal overlap count zero, uncovered count zero, every row
reachable, and first-applicable counts equal to the literal disjoint counts
`3/1/6/8/54`.

Confirm E-004 remains blocking for D: every owned handle receives exactly one
close attempt without short-circuiting, failures aggregate, and the attribute
list is deleted only after successful initialization. Confirm E-005 now has an
exact contract-owned observation profile, closed early-terminal derivation,
and exact source/sentinel split, and remains a concrete D implementation
obligation only for that profile and its derived counts. Confirm Codex D may
change only the exact reviewed executor and focused test while the accepted
harness and test remain byte-exact.

Run strict JSON validation, git diff --check, agent-doc validation,
path-scoped protected-surface and secret/private-marker scans, issue #769/#780
comment checks, process checks, and residue checks. Do not implement, access
the private path, consume authority, launch a process, run the preflight or an
observation, publish a receipt, mutate GitHub or release state, submit, merge,
deploy, authorize R1-R8 or Stage 4, or claim readiness.

If exact, create one new review artifact at:
docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_local_effect_reconciliation.md

Do not modify the accepted predecessor review or implementation review. Return
findings first, reviewed SHA-256, E-004 and E-005 dispositions, local-effect
profile and network-semantics verdicts, KAT and selector audits, exact future D
file scope, validation, authority flags, residue count, contract verdict,
D-repair routing eligibility, and a compact workflow_handoff.
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
    - "private direct-interpreter path and raw file identity"
    - "single-use preflight process and zero-descendant boundary"
    - "executor-owned local-effect observations and narrow network count"
    - "immutable R0 observation identities and receipts"
    - "issue #769 zero-comment boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "The trusted profile escalates only when independently proven isolation is needed; this owner rescope makes no child-isolation claim or requirement, so no direct contradiction remains."
  stop_conditions:
    - "binding, issue, contract-review, implementation-review, harness, executor, or test drift"
    - "need to inspect or emit the private executable path"
    - "scope beyond one contract or the two reviewed implementation paths"
    - "need to add a child-network field, gate, mechanism, or successor"
    - "need to launch a process or mutate GitHub, release, registry, or installed state"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  role_performed: "Codex B: Narrow R0 E-005 LE-03/LE-04 Predicate-Disjointness Corrector"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_implementation.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor_local_effect_reconciliation.md"
  contract_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_preflight_executor.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/role-pool-r0-direct-interpreter-preflight-executor-contract-780"
  base_commit: "3c3b4bfa7ddcd066d54b8b17ca9f3d496919d23f"
  predecessor_contract_sha256: "d69bd91540486d4aeadc46a3f217f7e3fd95baaee84b44178e38ae0dce14f848"
  reviewed_predecessor_sha256: "b6b2a2ff0bc1479f57ea62f5853b04dfea948feb098ac89077c4fe5041428094"
  rejected_contract_sha256: "bcc6a7e6e32b76503de9fdb42dcc95cb3cfce0720f7d3662cec005f9d969eefd"
  predecessor_review_sha256: "97adebc7fc8033125ac19dddb861361c7b4d40babdee338ca73b239394fa8038"
  implementation_review_sha256: "49d66f9ce38f0fab01bbeebf02deba4451f87f45600a21552b47a3e9292e0dac"
  finding_status:
    ME-RP-780-PREFLIGHT-EXEC-E-004: "open_blocking_preserved_for_codex_d"
    ME-RP-780-PREFLIGHT-EXEC-E-005: "raw_effect_selector_predicates_disjoint_re_review_pending"
  local_effect_profile: "closed_raw_state_pre_effect_structural_zero_sampled_zero_and_sentinel_routes"
  network_semantics: "executor_owned_observations_only_no_child_contribution"
  child_network_isolation_required: false
  child_network_claim: "none"
  process_entry_route_reachable: true
  passing_route_reachable: true
  preflight_execution_status: "not_run_not_authorized"
  accepted_observation_count: 0
  future_implementation_scope: "exact_two_reviewed_files_codex_d"
  codex_d_repair_routing_eligible: false
  owner_implementation_decision_eligible: false
  implementation_authorized: false
  private_path_access_authorized: false
  preflight_authorized: false
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
    - "current base, issues, accepted contract review, implementation review, harness, executor, and test bindings exact"
    - "six-status result vocabulary and active success KAT restored"
    - "E-004 preserved and the sole E-005 LE-03/LE-04 literal overlap removed"
    - "fixed roots, raw observation state, effect boundary, two derivation modes, and sentinel rules defined"
    - "5,832 normalized source states split 8/5,824 with process-entry and pass reachable"
    - "72-tuple raw effect selector requires literal and first-applicable 3/1/6/8/54 with audit 0/0/0"
    - "47 projection fixtures and one active exact 38-field success KAT"
    - "no process executed and no private path accessed in B"
  stop_conditions:
    - "binding or issue drift"
    - "private path or process access"
    - "scope beyond two reviewed implementation paths"
    - "child-network gate or enforcement architecture reintroduced"
    - "issue #769 comment or protected-state mutation"
  next_recommended_role: "Codex E: independent R0 E-005 raw-effect predicate-disjointness confirmation reviewer"
```

## Current Next Workflow Action

Fresh independent Codex E re-reviews only finding
`ME-RP-780-PREFLIGHT-TERM-B-001` and the reconciled terminal-fallback clauses
in this contract revision. E must confirm that every active post-CLI-admission
unsealed route selects the tracker-bound precreate, create-entered, or ambiguous
diagnostic; the generic sentinel remains only before tracker creation or when
exact terminal emission cannot be established; and sealed 38-field results are
unchanged.

E must reject any detailed error vocabulary, new JSON schema, durable stage
record, sidecar, log, trace, receipt, retry, additional process, private-value
output, parent-harness change, third implementation path, Observation 1 change,
or R1/Stage 4 expansion. E must also confirm that the historical attempt is
not reclassified or made reusable.

If exact, E creates only the normal contract-test report and sets
`owner_implementation_decision_eligible=true`. No implementation, preflight,
observation, publication, release, R1-R8, Stage 4, submission, merge,
deployment, or readiness authority follows from review acceptance.

The exact review artifact is:
`docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_preflight_terminal_fallback.md`.

```yaml
workflow_handoff:
  role_performed: "Codex B: Narrow R0 Terminal-Fallback Clause Reconciler"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  source_finding: "ME-RP-780-PREFLIGHT-TERM-B-001"
  reviewed_predecessor_sha256: "8a256548b34fc97f2fa926a87a9167abc2c7821c166f0f19b97660d784b79e8a"
  finding_status: "active_clause_reconciliation_authored_re_review_pending"
  historical_attempt_status: "consumed_unknown_nonreusable"
  accepted_observation_count: 0
  correction_scope: "active terminal-fallback clauses only"
  future_implementation_scope: "exact_existing_two_files"
  new_schema_count: 0
  new_result_field_count: 0
  new_process_count: 0
  retry_authorized: false
  owner_implementation_decision_eligible: false
  implementation_authorized: false
  private_path_access_authorized: false
  preflight_authorized: false
  observation_1_authorized: false
  receipt_publication_authorized: false
  release_state_mutation_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: independent narrow terminal-fallback contract re-reviewer"
```
