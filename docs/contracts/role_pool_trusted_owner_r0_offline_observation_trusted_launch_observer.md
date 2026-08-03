# Bounded R0 Trusted Launch Observer Contract

## Module

Repository-owned Windows trusted launch observer for R0 Observation 1.

## Source Issue

- Capability issue: <https://github.com/Tahjali11/Mythic-Edge/issues/803>
- Parent observation issue: <https://github.com/Tahjali11/Mythic-Edge/issues/776>
- Protected coordination issue: <https://github.com/Tahjali11/Mythic-Edge/issues/769>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/746>

## Governing Sources

- [`docs/agent_constitution.md`](../agent_constitution.md)
- [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md)
- [`docs/templates/module_contract.md`](../templates/module_contract.md)
- [`docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`](../decisions/ADR-0008-repo-wip-1-lane-activation-policy.md)
- [`docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md`](../decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md)
- [`role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md`](role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md)

## Owning Layer

Role Pool trusted-owner R0 release-evidence control plane.

## Internal Project Area

Role Pool governance and offline release validation.

## Truth Owner

`tools/check_role_pool_r0_offline_observation.py` continues to own the fixed
validation algorithm, validation-payload parser, immutable `PostExitFacts`
type, status precedence, receipt-v2 construction, and pure receipt sealer.

The future trusted launch observer owns only parent-observed process, stream,
timeout, termination, cleanup, and local-effect evidence for one fixed
Observation 1 operation. Child output and caller claims never own those facts.
Issue #776 retains authority-consumption and receipt-publication ownership.

## Bridge-Code Status

`shared_support`. The observer joins one reviewed Windows process operation to
the existing pure Observation sealer. It changes no parser, workbook,
transport, analytics, registry, release-state, installed-tree, or receipt
truth owner.

## Refreshed Authority And Bindings

Codex B refreshed `origin/main` to
`2650ec6fbec4a04134954caea21eb0608f9a31b9`. Issue #801 is closed. Issue #803
is open under the owner's exact docs-only instruction. Issue #769 is open with
zero comments. No duplicate issue, contract, implementation, or open-PR path
ownership was found.

The companion is bound to these exact ordinary repository files:

| Artifact | SHA-256 |
| --- | --- |
| `docs/contracts/role_pool_trusted_owner_r0_proportionate_offline_observation_successor.md` | `129ceb8f2bb21f4773e8258ad04238784d986c14168179e1d009b30c584588ae` |
| `tools/check_role_pool_r0_offline_observation.py` | `ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5` |
| `tests/test_check_role_pool_r0_offline_observation.py` | `79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784` |

Any drift in these bindings stops later implementation or execution and routes
to Codex B. The accepted validation-payload and receipt-v2 schemas, canonical
vectors, observation profile, status vocabulary, and pure sealer remain
unchanged.

The owner decision at #776 comment `5162537737` is unconsumed but stale because
it binds main commit `1c2451020d8ff3ff3f7b8b2be023a91d322c61b8`. It may not
be consumed, reused, refreshed, reinterpreted, or transferred. This contract
generates and activates no observation identity. A fresh owner decision is
required after accepted implementation, independent implementation review,
integration, and current-binding revalidation.

## Files Owned By This Contract

This Codex B task creates only:

- `docs/contracts/role_pool_trusted_owner_r0_offline_observation_trusted_launch_observer.md`

The exact later Codex C implementation scope is limited to:

- `tools/run_role_pool_r0_trusted_launch_observer.py`
- `tests/test_run_role_pool_r0_trusted_launch_observer.py`

No third implementation, helper, configuration, schema, fixture, service,
broker, scheduler, or durable evidence path is permitted. If either existing
Observation file must change, Codex C must stop and return to Codex B.

## Public Interface

The future script exposes only:

```text
main(argv: Sequence[str] | None = None) -> int
_run_observation_1(adapter: TrustedLaunchAdapter) -> bytes | str
```

`main` accepts zero arguments. Any argument or option is rejected before
launch. `_run_observation_1` is a private typed seam for the production
adapter and operation-free tests; it accepts no executable, command, cwd,
environment, timeout, observation identity, receipt field, or authority fact.

The observer imports the exact bound Observation module before any future
authority consumption. It derives Observation 1 from that module's first
contract-reserved identity and builds only this logical child token vector:

```text
["py", "-3.13", "-B",
 "tools/check_role_pool_r0_offline_observation.py",
 <exact bound OBSERVATION_IDS[0]>]
```

The repository root is the ordinary, non-reparse parent of the observer's
fixed repository-relative path. No caller-selected path is accepted.

The production adapter is private to the implementation module. Its methods
represent fixed launch setup, bounded wait/drain, complete process accounting,
effect snapshots, and cleanup. It is not exported as a general process API.
The fake adapter implements the same typed observations without calling an OS
process primitive.

## Inputs

The only runtime inputs are current trusted observations:

1. Windows runtime identity from `os.name == "nt"` and
   `sys.platform == "win32"`;
2. the exact three repository bindings above;
3. the exact Observation 1 identity already present in the bound module;
4. the inherited exact source, installed-tree, registry, release-state, and
   validator bindings resolved by the existing Observation owner; and
5. the future owner's exact, unexpired, single-use Observation 1 decision and
   its existing atomic-consumption readback, completed outside this module
   before `main` is invoked.

The observer does not parse, fetch, construct, publish, or mutate authority.
It accepts no stdin. It reads no private interpreter path and accepts no path,
command, environment, credential, receipt, or process fact from a caller.

## Fixed Windows Launch Boundary

The observer performs at most one child-creation call. It uses direct Windows
process creation with an explicit application path, `shell=false`, closed
stdin, bounded anonymous stdout and stderr pipes, a minimal environment, and
repository-root cwd.

The public command remains the exact `py -3.13 -B ...` vector above. To avoid
PATH lookup, the production adapter derives the application path only as the
fixed `py.exe` child of the directory returned by the Windows-directory API.
The derived path remains in bounded memory and is never emitted. It must be an
existing ordinary, non-reparse file with stable prelaunch identity. Absence,
ambiguity, reparse state, identity instability, or incompatibility fails as
`observation_binding_rejected`; there is no PATH, WindowsApps, registry,
caller, alternate launcher, direct-interpreter, shell, or acquisition fallback.

The command line uses deterministic Windows argument quoting from the fixed
tokens. The environment contains only the exact variables required by the
accepted validation algorithm, including `PYTHONDONTWRITEBYTECODE=1`, and no
credential, token, proxy, Python-path override, arbitrary ambient variable, or
caller-provided value. Environment construction failure stops before launch.

Before creation, the observer creates one attempt-owned Job Object configured
to terminate the child tree on job close and to report process creation and
exit. The fixed top-level process is assigned at creation, before any child
code can run. Breakaway is forbidden. The job handle is non-inheritable and no
other assignment call is permitted. The Job Object's completion channel and
cumulative basic-accounting query are the sole process-tree accounting source.
The final cumulative process total must equal the unique job-member creation
count, and both must equal one plus the derived descendant count. A platform
that cannot provide this pre-execution assignment and cross-check must fail
before launch; snapshot-only or polling-only accounting is not a substitute.

The observer itself is not counted in receipt topology. The directly created
`py.exe` operation is the one top-level process. Zero or one process created
beneath it is an allowed transient descendant. More than one descendant,
missing or contradictory job events, an unpaired process event, unknown
parentage, an unknown terminal state, or a nonzero active-process count after
the terminal boundary fails closed.

## Stream, Timeout, And Cleanup Boundary

- Timeout is exactly the inherited 120 seconds measured by a monotonic clock.
- Stdout is bounded by the existing `MAX_STDOUT_BYTES`; stderr is bounded by
  the existing `MAX_FAILURE_STDERR_BYTES`.
- Reader state is bounded. Overflow closes acceptance, initiates termination,
  and returns `observation_result_unknown` after cleanup.
- Successful output requires top-level exit `0`, stdout EOF containing exactly
  one canonical validation payload, and stderr EOF with zero bytes.
- Timeout or unsafe process state triggers one Job Object termination request,
  one bounded terminal wait, and no relaunch.
- Every proven-owned process, thread, pipe, job, completion, and temporary
  native handle receives exactly one close attempt. Close attempts continue
  after a failure and aggregate deterministically.
- Cleanup is confirmed only after terminal process accounting, complete pipe
  drain, zero active job processes, zero survivors, all required close results,
  and exact post-operation effect and residue observations.
- No exception text, Win32 code, PID, handle, path, command line, environment,
  or private value may reach stdout, stderr, a receipt, a handoff, or durable
  state.

No staging file, transcript, log, cache, receipt, or runtime-status artifact is
created by the observer. The only successful output is the existing canonical
receipt-v2 byte string returned by the existing pure sealer. Emission to local
stdout is not GitHub publication.

## Exact PostExitFacts Ownership

The observer constructs the existing immutable 15-field `PostExitFacts` only
after the complete terminal boundary. Field order and types remain owned by the
bound Observation module.

| Field | Exact parent-owned derivation |
| --- | --- |
| `top_level_process_count` | `1` only when the single direct creation produced one owned top-level process and no second creation was attempted; otherwise no sealing route exists. |
| `descendant_process_count` | Job cumulative process total minus the one top-level process, required to equal the unique non-top-level creation-event count; only `0` or `1` can pass. |
| `process_relationships_known` | `true` only when pre-execution assignment to the fresh non-inheritable job succeeded and cumulative accounting exactly matches a complete event set with no duplicate, breakaway, or ambiguous member. |
| `process_terminal_states_known` | `true` only when the top-level wait and every job member have one terminal event and the job reports zero active processes. |
| `surviving_process_count` | Active job members after the terminal wait and before job close; acceptance requires `0`. |
| `top_level_identity_exact` | Diagnostic `true`, `false`, or `null` from stable prelaunch versus process-image metadata; unavailable or nonexact identity alone is nonblocking and creates no provenance claim. |
| `timed_out` | Monotonic deadline expired before the complete terminal boundary. |
| `termination_uncertain` | Any required terminate request, terminal wait, active-process query, or terminal-event reconciliation is unavailable, contradictory, or unsuccessful. |
| `cleanup_confirmed` | All required drain, zero-survivor, handle-close, effect, and residue checks completed exactly with no uncertainty. |
| `output_complete` | Both bounded pipes reached EOF, no overflow occurred, and stdout/stderr bytes remained fully available for existing parsing. |
| `executor_network_operation_count` | Observer-process Python audit events in the existing network event family; acceptance requires `0`. It has no child contribution. |
| `repository_write_count` | Count of observer-process audit events for repository writes, plus one mismatch event when the exact post manifest differs from the exact pre manifest; acceptance requires `0`. |
| `installed_write_count` | Count of observer-process audit events for installed-tree writes, plus one mismatch event when the exact post manifest differs from the exact pre manifest; acceptance requires `0`. |
| `external_effect_count` | Count of observer-process audit events for environment mutation, an additional process attempt, or a write outside the repository and installed tree; acceptance requires `0`. The fixed one-child operation is excluded. |
| `generated_residue_count` | Exact post-minus-pre count of contract-defined generated-residue entries; acceptance requires `0`. |

The child validation payload is evidence only for the existing validation
algorithm. It never supplies a `PostExitFacts` field. The observer installs its
own audit counter before effect baselines and keeps it active through sealing
and cleanup. Counts are derived; fixed zero literals are forbidden.

The accepted limited network meaning is unchanged:
`executor_network_operation_count=0` means only that the observer saw zero
observer-owned Python network events. It does not claim child-network
prevention, complete child-network observation, firewall isolation, or
technical impossibility. `network_authorized=false` remains an authority
denial, not an isolation claim.

The fixed child retains its existing in-process audit boundary. Exact source,
installed-tree, protected-state, and residue pre/post equality supplements but
does not replace either audit boundary. This contract creates no global
zero-effect, complete transient-write observation, or hostile-child containment
assurance.

## Sealing And Schema Preservation

After terminal fact derivation, the observer passes exactly:

```text
seal_proportionate_observation_receipt(
    validation_payload,
    post_exit_facts,
    1,
)
```

to the already imported bound module in the same observer process. It does not
reimplement parsing, status precedence, receipt construction, canonical JSON,
self-digests, or known-answer vectors.

The following remain byte- and semantics-exact:

- `trusted_owner_r0_offline_bootstrap_evidence.v1` validation payload;
- `trusted_owner_r0_offline_observation_profile.v3`;
- `trusted_owner_r0_offline_observation_consumption.v2`;
- the 41-field `trusted_owner_r0_offline_observation_receipt.v2`;
- the 16 all-false authority fields;
- all 12 receipt variants and both six-digest position allowlists; and
- every existing status and precedence rule.

No new durable schema, receipt, status, lifecycle, digest family, or authority
field is introduced. A sealer string result is an existing public-safe failure
status, never receipt bytes.

## Closed Failure And Nonretry Lifecycle

Existing status vocabulary is sufficient and remains authoritative:

| First condition | Existing result |
| --- | --- |
| Stale repository/module/owner binding, unsafe launcher file, or prelaunch effect baseline mismatch | `observation_binding_rejected` |
| Non-Windows host | `observation_host_rejected` |
| Observation identity mismatch | `observation_sequence_rejected` |
| Child creation uncertainty, incomplete job assignment, unknown relationship, or missing top-level ownership | `observation_launch_unknown` |
| Timeout, termination uncertainty, unknown terminal state, failed required close, survivor ambiguity, or cleanup uncertainty | `observation_timeout_unknown` |
| More than one descendant, any survivor, observed write/network/external effect, or residue | `observation_safety_boundary_failed` |
| Output overflow, incomplete drain, or unavailable complete output | `observation_result_unknown` |
| Nonzero child exit outside the existing safety/unknown projection, nonempty stderr, or malformed validation payload | `observation_validation_failed` |
| Pure-sealer rejection after otherwise accepted evidence | existing sealer status, including `observation_receipt_sealing_failed` |
| Every predicate exact | existing canonical receipt-v2 bytes |

The first applicable existing status wins according to the bound Observation
module. The observer may not create a competing selector.

A future exact decision permits one observer invocation and at most one child-
creation attempt. Once the existing atomic consumption readback permits launch,
every success, failure, exception, cancellation, timeout, ambiguous return,
or lost output permanently retires that attempt. Retry, relaunch, resume,
replacement, fallback, evidence reconstruction, and silent reclassification
are forbidden. An unknown outcome remains consumed and nonreusable.

## Side Effects

Codex B performs no runtime side effect. The future observer may create only
attempt-owned volatile process, pipe, Job Object, completion, and handle state
for one separately authorized execution. It may emit existing public-safe
bytes locally after cleanup. It may not publish, persist, write, install,
modify, or delete any repository, installed-tree, registry, release, GitHub,
credential, network, or external state.

Issue #769 remains open with zero comments. Receipt publication, if separately
authorized later, remains the inherited issue-776-only no-replace/readback
operation and is outside the observer.

## Compatibility And Non-Claims

- The accepted Observation 1 algorithm and schemas are unchanged.
- Historical #780 and #795 preflight, identity, characterizer, terminal, and
  secure-ingress work remains historical or deferred and is not an eligibility
  dependency.
- Exact top-level identity remains diagnostic and nonblocking.
- The observer is not a shell, command runner, launcher service, broker,
  scheduler, subprocess API, reusable authority, or generic execution tool.
- No support is claimed for alternate Python, WindowsApps, user launcher,
  private interpreter, non-Windows hosts, fallback, or hostile-child isolation.
- Passing tests or review establishes prerequisite evidence only. It does not
  authorize implementation, execution, consumption, publication, Observation
  1 or 2, R1-R8, Stage 4, submission, merge, deployment, readiness,
  correctness, security, privacy, reliability, or assurance.

## Remaining Constructibility Risk

During this Codex B task, the fixed system `py.exe` was present but its
metadata-only inventory reported no installed Python. No child command was
executed. This is current host evidence, not a permanent platform conclusion.

Operation-free Codex C implementation and tests may proceed after contract
acceptance, but a real Observation 1 decision is ineligible until a later
current-host check proves that the exact no-PATH launcher can select compatible
Python 3.13. Missing compatibility must remain
`observation_binding_rejected`. This contract does not authorize installation,
runtime acquisition, PATH repair, alternate Python, or fallback.

## Dependency Order

1. Fresh Codex E accepts this exact contract.
2. A separate owner decision authorizes Codex C for exactly the two paths.
3. Codex C implements only the fixed observer and operation-free fake tests.
4. Fresh Codex E reviews exact implementation bytes and evidence.
5. Codex F and G perform separately authorized submission and integration.
6. Current bindings, issue #769, and authority eligibility are revalidated.
7. A fresh, expiring, nonreusable owner Observation 1 decision is recorded.

No earlier step grants a later step's authority.

## Tests Required

All observer tests are operation-free. They patch or inject the fake adapter
before any production adapter or OS process primitive is reachable. The suite
must prove:

1. only zero CLI arguments are accepted and the child vector is exact;
2. non-Windows, stale bindings, unsafe launcher, caller-selected values, and
   environment drift reject before fake launch;
3. exactly one launch call occurs and no retry, fallback, or second call is
   reachable;
4. descendant counts `0` and `1` can seal only with complete relationships,
   known terminal state, zero survivors, complete output, and exact cleanup;
5. count greater than `1`, any survivor, unknown relationship or terminal
   state, timeout, termination uncertainty, drain failure, output overflow,
   handle-close failure, or cleanup uncertainty fails with the existing status;
6. every owned handle receives exactly one close attempt, close failures do not
   short-circuit, and ambiguous ownership is never claimed cleaned;
7. nonzero exit, stderr, malformed validation payload, sealer string result,
   or receipt mismatch never emits receipt bytes;
8. false or unavailable exact identity alone remains nonblocking;
9. audit and pre/post fixtures derive each nonzero network, repository,
   installed, external-effect, and residue count and fail closed;
10. hard-coded zero effect counts are absent;
11. the exact existing validation parser and sealer are invoked in-process
    once, while fake adapters launch no process and perform no external effect;
12. all existing payload, receipt-v2, authority, and known-answer bytes remain
    unchanged;
13. the stale #776 decision is rejected and all historical #780/#795 routes
    remain absent from eligibility; and
14. issue #769 publication, Observation 2, R1-R8, and every authority flag are
    false.

Required later implementation validation:

```powershell
py -B -m pytest tests/test_run_role_pool_r0_trusted_launch_observer.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_offline_observation.py -q -p no:cacheprovider
py -B tools/check_agent_docs.py
py -B tools/check_protected_surfaces.py --base origin/main
py -B tools/check_secret_patterns.py --base origin/main
py -B -m ruff check tools/run_role_pool_r0_trusted_launch_observer.py tests/test_run_role_pool_r0_trusted_launch_observer.py
git diff --check
```

These commands do not authorize or execute the real observer operation.

## Acceptance Criteria

Fresh Codex E may accept only if:

1. current authority, #769 protection, and all exact predecessor hashes pass;
2. this contract is the only changed path;
3. the fixed child command and direct no-shell/no-PATH boundary are closed;
4. the observer has no general command, argument, cwd, environment, retry, or
   fallback interface;
5. every `PostExitFacts` field has one parent-owned derivation and unknown
   evidence cannot reach sealing;
6. zero or one known transient descendant can pass only with zero survivors;
7. timeout, termination, drain, handles, process accounting, effects, residue,
   and cleanup fail closed under existing statuses;
8. the validation payload, receipt-v2, authority object, sealer, canonical
   vectors, and status vocabulary are unchanged;
9. all future tests are operation-free and future implementation is exactly
   the two named paths;
10. the stale decision is preserved unconsumed and unusable on current main;
11. no process, authority, receipt, GitHub, release, registry, installed-tree,
    or source mutation occurred; and
12. generated residue is zero.

Acceptance makes only a separate owner Codex C implementation decision
eligible. It creates no implementation or operational authority.

## Next Workflow Action

Next role: Codex E, independent bounded R0 trusted launch observer contract
reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Bounded R0 Trusted Launch Observer Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/803
Parent: https://github.com/Tahjali11/Mythic-Edge/issues/776
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_trusted_owner_r0_offline_observation_trusted_launch_observer.md

Bind the exact contract SHA-256 and base commit from the Codex B handoff.
Independently refresh authority and GitHub state, confirm #769 is open with
zero comments, recompute all three predecessor hashes, and reject any duplicate
or open-PR ownership overlap.

Verify the fixed no-shell/no-PATH command, Windows launcher derivation, one
launch, bounded Job Object topology, zero-or-one descendant rule, zero
survivors, stream/timeout/termination/handle/cleanup closure, and exact
parent-owned derivation of all 15 immutable PostExitFacts. Confirm the existing
validation payload, profile, consumption-v2, receipt-v2, all-false authority,
canonical vectors, statuses, and pure sealer are unchanged. Confirm the
limited executor-owned network meaning and all child-network nonclaims.

Audit every failure route, operation-free fake-adapter requirement, stale
#776 decision disposition, historical #780/#795 nondependency, exact two-file
future implementation scope, and all false authority fields. Run the
contract-required path-scoped docs and safety validation.

Do not implement, execute, consume authority, publish a receipt, touch #769,
mutate release/registry/installed state, submit, merge, deploy, authorize
Observation 1 or 2, R1-R8, or Stage 4, or claim readiness. Findings lead. If
exact, route only to a separate owner Codex C implementation decision.
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Bounded R0 Trusted Launch Observer Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/803"
  parent: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/803"
  target_artifact: "docs/contracts/role_pool_trusted_owner_r0_offline_observation_trusted_launch_observer.md"
  risk_tier: "high release-evidence control; no runtime change"
  base_branch: "origin/main"
  target_branch: "unselected_pending_review"
  branch: "codex/r0-trusted-launch-observer-contract-803"
  base_commit: "2650ec6fbec4a04134954caea21eb0608f9a31b9"
  predecessor_binding_status: "exact"
  stale_owner_decision_status: "unconsumed_stale_nonusable"
  current_py_launcher_status: "present_no_installed_python_observed"
  validation_payload_schema_changed: false
  receipt_v2_schema_changed: false
  implementation_authorized: false
  observer_execution_authorized: false
  authority_consumption_authorized: false
  receipt_publication_authorized: false
  observation_1_authorized: false
  observation_2_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  generated_residue_count: 0
  validation:
    - "git diff --check: passed"
    - "agent docs consistency: passed with 0 errors and 0 warnings"
    - "protected-surface gate: passed with 0 forbidden and 0 warnings"
    - "secret/private-marker scan: passed with 0 forbidden and 0 warnings"
    - "validation selection: passed with 3 required and 1 recommended check"
    - "exact path, hashes, PostExitFacts, ASCII, whitespace, and final LF: passed"
  remaining_risk: "fixed system py launcher currently reports no installed Python; real execution remains ineligible"
  next_recommended_role: "Codex E: independent bounded R0 trusted launch observer contract reviewer"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high release-evidence control; no runtime change"
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
    - "ADR-0012"
  protected_surfaces:
    - "R0 authority consumption and receipt publication"
    - "process and local-effect evidence"
    - "release, registry, installed-tree, and source integrity"
    - "protected issue #769"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #801 is closed; #803 owns one disjoint contract path."
  stop_conditions:
    - "any changed path outside the exact contract"
    - "any predecessor or authority drift"
    - "any process execution or authority consumption"
    - "any new schema, generic launch capability, retry, or fallback"
    - "any mutation of issue #769 or release/registry/installed state"
```
