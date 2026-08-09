# App-Native R0 Successor Parent Controller Contract

## Module And Authority

- Repository: <https://github.com/Tahjali11/Mythic-Edge>.
- Capability issue: <https://github.com/Tahjali11/Mythic-Edge/issues/828>.
- Source lifecycle issue: <https://github.com/Tahjali11/Mythic-Edge/issues/826>.
- Parent profile issue: <https://github.com/Tahjali11/Mythic-Edge/issues/813>.
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>.
- Protected coordination issue:
  <https://github.com/Tahjali11/Mythic-Edge/issues/769>.
- Constitution: [`docs/agent_constitution.md`](../agent_constitution.md).
- Codex B role:
  [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md).
- Contract template:
  [`docs/templates/module_contract.md`](../templates/module_contract.md).
- Accepted WIP policy:
  [`ADR-0008`](../decisions/ADR-0008-repo-wip-1-lane-activation-policy.md).
- Accepted context discipline:
  [`ADR-0012`](../decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md).
- Risk tier: high.
- Authoritative base commit:
  `f8e6fc186094182c68a98ebdf229123809e3d5cc`.
- Authoritative base tree:
  `816ad1985c54961048dce582a3825bfac3d26c34`.

The owner's current instruction is a task-scoped `explicit_user_override` for
this one Codex B artifact while issue #826 remains blocked. It expires with
this handoff. It creates no implementation, private-input, controller-start,
process-launch, observation, consumption, publication, or rung authority.

Issue #828 is open with zero comments. Issue #769 is open with zero comments.
Open pull requests #374 and #391 do not own any path in this contract or its
future two-path implementation envelope.

## Findings And Decision

1. **Observed:** the accepted #826 harness owns exact input validation, the
   immutable 15-field `PostExitFacts`, the existing status precedence, and the
   pure `seal_proportionate_observation_receipt` function. It does not own a
   callable native parent operation.
2. **Observed:** the current Codex shell accepts one PowerShell command string.
   It exposes neither a structured application-image plus argument-array call
   nor the required Job Object, stream, close, effect, and cleanup evidence.
3. **Observed:** the predecessor trusted launch observer is exact historical
   evidence at SHA-256
   `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a`.
   It is not a successor implementation dependency.
4. **Decision:** add one successor-only Windows parent controller and one
   operation-free focused test. The controller imports only the accepted #826
   harness interface and independently owns its native boundary.
5. **Decision:** private target selection uses bounded attached-console input
   through `ReadConsoleW` with echo disabled. The private target path is never
   a command argument, environment value, file, registry value, clipboard
   value, prompt, log, exception, result, receipt, comment, or handoff value.
6. **Decision:** this is an owner-operated boundary. The current noninteractive
   Codex shell is not a conforming live caller. That nonclaim does not block
   inert implementation or operation-free review, but it does block live use
   until a fresh owner decision selects a conforming interactive Windows host.
7. **Observed:** independent review found that the initial ingress sequence did
   not reject character-producing input already buffered before `ReadConsoleW`
   or prove that no second line remained queued after the bounded read.
8. **Decision:** close only that console-buffer boundary with three bounded,
   non-consuming queue audits. No process, identity, schema, lifecycle, or
   implementation-path requirement changes.

Finding `ME-RP-826-PARENT-A-001` is
`contracted_successor_boundary_pending_independent_review`.

Finding `ME-RP-828-E-001` is
`contract_corrected_pending_independent_confirmation`.

## Exact Frozen Bindings

| Artifact or fact | Exact binding |
| --- | --- |
| Repository ID | `1235264383` |
| Repository name | `tahjali11/mythic-edge` |
| Accepted #826 lifecycle contract | `37249` bytes; `be7974ba998257981df5c876dfa441b03326ae776405bd269d1470957a785cde` |
| Accepted #826 harness | `88401` bytes; `cfd3a0baaff6c4bbc5144403fd72f404722b8b96e8eca30fbf588f3180ec0b42` |
| Accepted #826 harness test | `76211` bytes; `3fc6c35eada99f3a319e1ebe94bd5f33494821301cfdf1ec67f5f35bfc97dc4c` |
| Accepted #826 bridge test | `41360` bytes; `53738a8d2108edaf13cd138cad7d3c771cdaff58c32c13cd464fec758a8bc9a7` |
| Frozen predecessor observer | `66397` bytes; `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a` |
| Trusted-owner profile | `119600` bytes; `8f885dcab251143ed9afb9c091d3d4beaa695bb934248ab674dd8784e8a71952` |
| Source and installed tree | `43` nodes; `38` files; `6840` canonical bytes; `3aadf078fe594dafdd870df5577d342ccf1c8ea665f2a8f53cc79a58213717d6` |
| Registry artifact | `1478` bytes; `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |
| Registry self-digest | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Release artifact | `2434` bytes; `fff6025bcb3937506b29828bbbb4bbd46e517ec7ae635744c4902d3716b125f2` |
| Release tip | `836880895e1d08aa6756155531f248d0eab7405d9987e552d1f000b4d0ab9a91` |
| Authority index | `17554` bytes; `a04fee4dab269eebbf503d5f5708cabc35a3f15910a679e53287ef757bf910b9` |
| Stable validator bundle | `be432ceab519e42fc688800c2cda1b172845abb329acc942ba11c5a5490826ca` |
| R0 checker | `46635` bytes; `897790936dc0c49401177958477f839d0cecac39bd0cf2e24849fc05954e781a` |
| R0 checker test | `66152` bytes; `55a40f12d7d161eb40fca2905f442b3b6ecd1fc029e3313c81566db89dd6ae3f` |
| Observation profile | `32` fields; `1975` bytes; `a657ed989026996329150d5a64212c85260857ce998dea271241828cad0e333f` |
| Child stdout ceiling | `4096` bytes |
| Child stderr ceiling | `128` bytes |
| Observation timeout | `120` seconds |
| Termination reconciliation grace | `5` seconds |

Every repository artifact above must remain an ordinary, non-reparse file at
its exact length and digest. The source and installed trees must remain exact
and equal. Drift stops before private input or child creation.

The owner decision at
<https://github.com/Tahjali11/Mythic-Edge/issues/826#issuecomment-5232244853>
is unedited and unconsumed, but it is nontransferable to this controller and
its identity is not reusable. A later controller execution requires a fresh
eligibility review and a fresh exact, expiring, single-use owner decision.

## Future Authority Sequence

No controller process starts before this complete later sequence:

1. this exact contract receives independent Codex E acceptance;
2. a separate owner decision authorizes only the exact two-file inert
   implementation;
3. Codex C implements only those files and fresh Codex E accepts their exact
   bytes;
4. Codex F and Codex G integrate the reviewed package under separate authority;
5. fresh Codex E eligibility review binds current repository, source/install,
   registry, release, index, validator, harness, controller, and test bytes;
6. the owner publishes one fresh 12-hour, single-use execution decision that
   binds the exact controller runtime version, length, SHA-256, stable file
   identity, exact target executable version, length, SHA-256, stable file
   identity, fresh observation ID, and all accepted lifecycle bindings; and
7. the existing #826 consumption owner publishes and exactly reads back one
   canonical consumption record before the controller starts.

The controller does not create, post, fetch, repair, or infer authority. A
controller start after exact consumption is the sole execution attempt. Every
startup, ingress, binding, launch, cancellation, timeout, cleanup, output,
sealing, or publication outcome after consumption permanently retires that
decision and identity. Unknown consumption or readback stops before controller
start and permits no replacement.

## Owning Layer And Files

The successor parent owns only private executable custody and parent-observed
process, stream, timeout, termination, cleanup, effect, and `PostExitFacts`
evidence. The accepted #826 harness remains sole owner of child validation,
schema parsing, status selection, canonical receipt construction, and sealing.
GitHub remains the durable owner of later decision, consumption, and candidate
publication evidence. The human owner alone grants execution authority.

This contract creates only:

- `docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md`

The exact later Codex C implementation envelope is two new paths:

1. `tools/run_role_pool_app_native_r0_observation_parent.py`
2. `tests/test_run_role_pool_app_native_r0_observation_parent.py`

Both paths are absent at this base. No third implementation, test, fixture,
bootstrap, configuration, schema, service, broker, or evidence path is
permitted. Every accepted #826 path and the predecessor observer remain
byte-identical.

## Public Interface

The production module exposes only:

```text
main(argv: Sequence[str] | None = None) -> int
```

The logical controller invocation contains exactly one public value:

```text
["tools/run_role_pool_app_native_r0_observation_parent.py",
 "<fresh_owner_bound_observation_id>"]
```

The observation ID must match exactly
`r0.app_native.offline.observation.1.[0-9a-f]{32}`, must not be all zero, and
must equal the separately reviewed and consumed owner decision. Missing,
extra, reordered, duplicate, option-like, non-ASCII, or nonexact input is
`observation_sequence_rejected` before private input.

The controller accepts no executable, command, argument list, cwd,
environment, timeout, receipt field, process fact, or authority claim through
`argv`. It accepts no redirected stdin. Its internal fake-native interface is
private and dependency-injected only by operation-free tests; it cannot accept
caller-selected process parameters.

The owner starts the controller once from an already-running interactive
Windows console using a separately bound direct controller runtime. The
controller runtime must itself be an exact ordinary, non-reparse file bound by
version, length, SHA-256, and stable file identity in the future owner decision.
No PATH lookup, `py.exe`, WindowsApps alias, file association, shim, wrapper,
shell child launch, broker, service, scheduled task, task API, alternate
runtime, or fallback is permitted.

The current Codex `shell_command` surface is not a conforming interactive
caller and is not authorized to start this controller. This contract does not
claim a general structured-launch capability or automate the owner-operated
controller start.

## Private Executable Ingress And Custody

After every public binding and the external exact consumption readback are
complete, `main` obtains the target executable through the attached console:

1. require Windows `os.name == "nt"` and `sys.platform == "win32"`;
2. require `GetStdHandle(STD_INPUT_HANDLE)` to identify an attached console
   accepted by `GetConsoleMode`, not a pipe, file, pseudo-input, or redirect;
3. snapshot the exact console input mode and require `ENABLE_LINE_INPUT`;
4. disable `ENABLE_ECHO_INPUT` without changing unrelated mode bits;
5. perform the pre-read queue audit defined below; require a stable queue with
   zero pending character-producing input before `ReadConsoleW`;
6. read exactly one complete terminated line with one `ReadConsoleW` call into
   one mutable buffer bounded to `32767` UTF-16 code units excluding its line
   terminator and NUL;
7. perform the post-read queue audit while echo remains disabled; reject a
   second line or any other pending character-producing input;
8. require exactly one terminal carriage return, optionally followed by one
   line feed, with no earlier CR or LF; reject empty, unterminated, truncated,
   multi-line, NUL-containing, or unpaired-surrogate input without echo;
9. restore the exact original console mode in one attempt before child entry;
10. perform one final prelaunch queue audit after restoration and immediately
    before private target validation; reject any pending character-producing
    input or audit uncertainty;
11. perform no later console read, queue flush, input discard, or purge; and
12. clear every mutable input, queue-audit, and normalized-path buffer on every
    route with one best-effort overwrite, without claiming impossible total
    zeroization.

Each queue audit is the same closed non-consuming operation:

1. call `GetNumberOfConsoleInputEvents` and reject failure or a count greater
   than `4096`;
2. when the count is nonzero, call `PeekConsoleInputW` once into a bounded
   mutable `INPUT_RECORD` buffer and require exactly that count to be returned;
3. call `GetNumberOfConsoleInputEvents` again and require the same count; and
4. reject any `KEY_EVENT` record whose `bKeyDown` is true and whose
   `UnicodeChar` is not NUL.

An API failure, short peek, malformed record, over-limit count, or changed
count is queue-inspection uncertainty and selects `observation_binding_rejected`
before process entry. Prebuffered character input is never accepted as the
owner's contemporaneous line. A multi-line paste cannot be reduced to its
first line. Queue records are never dequeued by an audit. Input arriving after
the final successful audit cannot affect the child because the controller
performs no further console input operation.

The admitted path is one absolute local drive path. UNC, device, relative,
environment-expanded, wildcard, alternate-data-stream, trailing-dot,
trailing-space, dot-segment, and reparse paths are rejected. The immediate
file and every traversed component must be ordinary and non-reparse.

The controller opens the target before launch with read and execute-attribute
access while denying write and delete sharing. It binds stable volume/file
identity, byte length, SHA-256, version metadata, and basename `python.exe` to
the future owner decision. It rechecks stable identity immediately before the
sole process-entry call and after terminal readback while retaining the open
guard handle. Mismatch or uncertainty is `observation_binding_rejected` before
entry, or `observation_launch_unknown` after entry.

The private path may exist only in bounded controller memory and the necessary
Win32 application-image buffer. It must never enter stdout, stderr, a Python
exception string or chain, `repr`, logging, tracing, audit output, command
line, argument vector, environment block, cwd, title, file, registry, clipboard,
cache, receipt, comment, prompt, handoff, or durable artifact. Visibility to
the trusted Windows operating-system control plane remains an explicit
nonclaim; the controller does not claim to hide the target from that boundary.

## Fixed Child Construction

The controller performs exactly one `CreateProcessW` entry attempt. It uses:

```text
lpApplicationName = <private exact owner-bound python.exe>
argv = ["python.exe", "-B",
        "tools/check_role_pool_r0_offline_observation.py",
        <fresh_owner_bound_observation_id>]
cwd = <exact repository root>
timeout = 120 seconds
```

The mutable Windows command line is produced by one closed quoting function
from those four tokens only. The private path is not `argv[0]`. No caller text,
generic command parser, shell, interpolation, response file, alternate script,
flag, cwd, environment value, timeout, or second command can reach it.

The child environment contains only case-insensitively unique entries for
`PYTHONDONTWRITEBYTECODE=1` and the exact Windows directory as `SYSTEMROOT`.
It contains no PATH, Python path override, proxy, credential, token, secret,
arbitrary ambient variable, or caller value. Child stdin is a closed inherited
pipe. Stdout and stderr are separate bounded inherited pipes.

## Windows Process And Job Invariants

Before process entry, the controller creates one unnamed, non-inheritable Job
Object and one completion port. The job is configured with exactly:

- `JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 1`;
- `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; and
- no breakaway or silent-breakaway permission.

The completion port is associated before entry. The sole `CreateProcessW`
uses `STARTUPINFOEXW`, `PROC_THREAD_ATTRIBUTE_JOB_LIST`, and
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST` so the child enters the job before any
child code runs and inherits only its closed stdin read handle and stdout and
stderr write handles. `CREATE_SUSPENDED` plus later assignment is not a
fallback. If creation-time job assignment is unavailable, stop before entry.

The controller is outside receipt topology. The directly created validation
child is the one top-level process. Any job-member creation other than that
member, any active-process-limit message, any contradictory event, or any
nonzero final active-process count prevents acceptance. Zero descendants and
zero survivors are mandatory.

Completion-port creation events, exit events, cumulative job accounting, the
owned process handle, and final zero-active-process query must agree. Snapshot
polling, child claims, PID enumeration alone, and pre/post process lists are
not substitutes. Unknown parentage or terminal state fails closed.

## Streams, Timeout, Termination, And Cleanup

- The monotonic `120`-second deadline is established immediately before the
  sole `CreateProcessW` attempt.
- Stdout and stderr are drained concurrently from process entry through EOF.
- Stdout may retain at most `4096` bytes and stderr at most `128` bytes. The
  first overflow closes the acceptance route and requests termination.
- Success requires child exit `0`, complete stdout EOF containing exactly one
  accepted 37-field validation payload, complete stderr EOF with zero bytes,
  and no unconsumed bytes.
- Timeout, cancellation, overflow, unsafe topology, or uncertain terminal state
  causes at most one `TerminateJobObject` request followed by one bounded
  `5`-second reconciliation wait. There is no relaunch or replacement.
- Every proven-owned process, thread, job, completion-port, target-guard,
  stdin, stdout, stderr, and pipe handle receives exactly one close attempt.
  Close attempts continue in reverse acquisition order after failures and
  aggregate deterministically.
- `DeleteProcThreadAttributeList` is attempted exactly once only after
  successful attribute-list initialization. It is not a handle-close event.
- Console-mode restoration is attempted exactly once if and only if mode
  mutation succeeded. The console handle is borrowed and is never closed.
- Any required close, deletion, mode restoration, drain, terminal query,
  buffer clearing, or survivor check that fails or is unknown makes
  `cleanup_confirmed=false`.

No transcript, staging file, runtime-status file, log, cache, private evidence,
or durable controller artifact is created. The only successful local output is
the unchanged canonical receipt bytes. A fixed existing status plus final LF is
the only failure output; raw errors and exception chains are suppressed.

## Before And After Effect Evidence

The controller installs its Python audit observer before its first baseline and
keeps it active through sealing and cleanup. Before private input and again
after child termination, drain, and cleanup, it derives bounded stable
inventories for:

- the exact repository tree;
- the exact installed Role Pool tree;
- the fixed registry, release, authority-index, validator, harness, and
  contract bindings; and
- contract-defined generated residue under the repository and installed tree.

Each inventory requires an ordinary, non-reparse root, deterministic ordinal
path ordering, stable file identity during hashing, and exact current digest.
Any sampling, identity, read, or equality uncertainty fails closed. The
controller performs no repair, cleanup of pre-existing state, reset, revert,
or deletion.

The 15 `PostExitFacts` fields are derived as follows:

| Field | Parent-owned source |
| --- | --- |
| `top_level_process_count` | `1` only after the sole successful process-entry attempt; otherwise no receipt route. |
| `descendant_process_count` | Unique non-top-level job creation events cross-checked against cumulative job process count; acceptance requires `0`. |
| `process_relationships_known` | Creation-time job membership and complete, noncontradictory job accounting. |
| `process_terminal_states_known` | One top-level terminal state, complete job exits, and final active count `0`. |
| `surviving_process_count` | Final active job members; acceptance requires `0`. |
| `top_level_identity_exact` | Diagnostic comparison of the retained target identity with available process-image metadata; `true`, `false`, or `null` retains #826 semantics. |
| `timed_out` | Monotonic deadline expired before the complete terminal boundary. |
| `termination_uncertain` | Required termination or terminal reconciliation was unavailable, contradictory, or unsuccessful. |
| `cleanup_confirmed` | Every required drain, terminal, zero-survivor, close, deletion, mode-restoration, effect, and residue check completed exactly. |
| `output_complete` | Both bounded pipes reached EOF with no overflow and all retained bytes remained available. |
| `executor_network_operation_count` | Controller-owned Python network audit events; acceptance requires `0`. |
| `repository_write_count` | Controller-owned repository write events plus one mismatch event for unequal pre/post repository inventory; acceptance requires `0`. |
| `installed_write_count` | Controller-owned installed-tree write events plus one mismatch event for unequal pre/post installed inventory; acceptance requires `0`. |
| `external_effect_count` | Controller-owned environment mutation, extra process-entry, or write outside the two observed trees; the one fixed child entry is excluded; acceptance requires `0`. |
| `generated_residue_count` | Exact post-minus-pre generated-residue entries; acceptance requires `0`. |

Counts are derived and never inserted as fixed zero literals. Child output
never supplies a parent fact. The network field retains the accepted limited
meaning: zero means only zero controller-owned observed Python network events.
It does not prove child-network prevention, complete native observation,
firewall isolation, hostile-child containment, or network impossibility.

## Sealing And Output Custody

Only after the complete post-exit boundary may the controller call, in its own
process, exactly:

```text
seal_proportionate_observation_receipt(
    validation_payload,
    post_exit_facts,
    observation_id,
)
```

The function must come from the exact accepted #826 harness. The controller
does not copy or reimplement parsing, status precedence, receipt construction,
canonical JSON, digest logic, or known-answer vectors. The 32-, 36-, 37-, and
41-field schemas, 12-input selector, statuses, authority fields, and pure
sealer remain unchanged.

Canonical receipt bytes remain candidate evidence only. The controller writes
them once to local stdout after exact sealing and writes nothing to stderr.
It does not create or publish a GitHub receipt. The external lifecycle owner
retains any later publication and exact readback responsibility.

## Closed Failure Precedence And Nonretry

The first applicable row wins:

| Precedence | Condition | Existing public result |
| --- | --- | --- |
| 1 | Non-Windows host | `observation_host_rejected` |
| 2 | Invalid public identity | `observation_sequence_rejected` |
| 3 | Stale artifact, unsafe or uncertain console queue, unsafe private target, or pre-entry baseline mismatch | `observation_binding_rejected` |
| 4 | Process entry may have occurred but ownership, job membership, or top-level identity is unknown | `observation_launch_unknown` |
| 5 | Timeout, termination uncertainty, unknown terminal state, failed required close, mode-restoration failure, survivor ambiguity, or cleanup uncertainty | `observation_timeout_unknown` |
| 6 | Any descendant, survivor, write, controller-observed network operation, external effect, or residue | `observation_safety_boundary_failed` |
| 7 | Output overflow, incomplete EOF/drain, or unavailable complete output | `observation_result_unknown` |
| 8 | Nonzero child exit, nonempty stderr, or malformed validation payload | `observation_validation_failed` |
| 9 | Pure sealer rejects otherwise exact evidence | Exact existing sealer status |
| 10 | Every predicate exact | Existing canonical receipt bytes |

Known pre-entry rejection performs no child entry. Once the future owner
decision is consumed, every cancellation, failure, timeout, ambiguity, or
success is terminal and permanently nonreusable. There is no automatic retry,
manual retry under the same identity, fallback, relaunch, replacement identity,
second process-entry attempt, or evidence reconstruction.

## Operation-Free Tests

The focused test uses only fake console, filesystem, hashing, clock, audit,
Win32, job, completion, process, stream, and sealer adapters. It launches no
real process and accesses no private executable.

It must prove:

1. exact zero-extra-argument public parsing and every identity rejection;
2. non-Windows and redirected-console rejection before private input;
3. exact line-mode admission, echo disable, exactly one bounded `ReadConsoleW`,
   exact mode restoration, cancellation, unterminated or truncated input,
   malformed UTF-16, and best-effort buffer clearing;
4. stable bounded queue audits proving that prebuffered character input,
   multi-line paste with a queued second line, queue-inspection failure or
   instability, and any prelaunch character input reject before child entry,
   while one ordinary complete terminated line with empty character queues is
   admitted; the fakes must also prove no audit dequeues or flushes input;
5. private path absence from every public value, call record, exception,
   fixture representation, output, and serialized test artifact;
6. ordinary/non-reparse component validation, stable identity, exact owner
   binding, denied write/delete sharing, and every drift route;
7. exact four-token child construction, fixed cwd and environment, and
   rejection of shell, PATH, `py.exe`, alias, shim, wrapper, alternate script,
   caller argument, and fallback routes;
8. exactly one process-entry call under success, failure, exception,
   cancellation, timeout, and ambiguity;
9. creation-time Job Object membership, active-process limit `1`, kill-on-close,
   no breakaway, exact inherited handle list, and no post-create assignment;
10. complete and conflicting completion-event and cumulative-accounting cases;
11. zero descendants can pass and every descendant, survivor, unknown
    relationship, or unknown terminal state fails;
12. stdout and stderr boundaries at, below, and above their exact limits,
    concurrent drain, EOF, nonzero exit, nonempty stderr, and malformed payload;
13. timeout at the deadline, one termination request, five-second
    reconciliation, and no retry or replacement;
14. every owned-resource acquisition prefix and every close-failure
    permutation receives exactly one reverse-order close attempt without
    short-circuiting;
15. attribute-list deletion and console-mode restoration ownership rules;
16. deterministic pre/post equality, write, network, external-effect, residue,
    unstable-read, and sampling-unknown cases without hard-coded effect counts;
17. exact construction of all 15 immutable `PostExitFacts` fields from parent
    evidence only;
18. exactly one call to the accepted pure sealer after complete cleanup and
    zero calls on every earlier failure;
19. canonical receipt output and every existing fixed failure output are
    public-safe and no-echo;
20. the accepted #826 files and predecessor observer remain byte-identical and
    no predecessor-observer function is imported or called; and
21. no process, task, network, GitHub, repository, installed-tree, registry,
    release, identity, consumption, or publication operation occurs.

Required later implementation validation:

```powershell
py -3.13 -B -m pytest -q -p no:cacheprovider tests/test_run_role_pool_app_native_r0_observation_parent.py
py -3.13 -B -m pytest -q -p no:cacheprovider tests/test_check_role_pool_r0_offline_observation.py tests/test_run_role_pool_r0_trusted_launch_observer.py
py -3.13 -B -m ruff check tools/run_role_pool_app_native_r0_observation_parent.py tests/test_run_role_pool_app_native_r0_observation_parent.py
py -3.13 -B tools/check_agent_docs.py
py -3.13 -B tools/check_protected_surfaces.py --base origin/main
py -3.13 -B tools/check_secret_patterns.py --base origin/main
git diff --check
```

## Acceptance And Stop Conditions

Contract acceptance permits only a later owner decision about the exact
two-file inert implementation. Implementation acceptance and integration make
only a fresh current-binding eligibility review possible. They do not activate
the controller or observation.

Stop and return to Codex A or the owner if:

- either implementation path already exists or a third path is required;
- any accepted #826 file or predecessor observer must change;
- a private value must enter a model-visible, durable, redirected, or
  non-console surface;
- a conforming owner-operated interactive Windows console cannot be used;
- a generic runner, shell child, PATH lookup, `py.exe`, alias, shim, wrapper,
  helper, broker, service, task API, fallback, retry, or replacement is needed;
- creation-time Job Object assignment, exact handle inheritance, complete
  accounting, stream drain, close evidence, effect derivation, or cleanup
  cannot be operation-free tested and later directly observed;
- a new schema, selector input, status, receipt, digest family, lifecycle,
  authority field, or publication mechanism is required;
- current bindings drift; or
- issue #769 would require any read beyond state/comment-count validation or
  any mutation.

This contract does not authorize implementation, private-path access,
controller start, child creation, identity generation or consumption,
observation execution, candidate publication, Observation 2, task dispatch,
R1-R8, Stage 4, submission, merge, deployment, assurance, privacy guarantees,
security guarantees, or live readiness.

## Next Workflow Action

Next role: fresh independent Codex E contract reviewer.

Pasteable prompt:

```text
Use the current Mythic Edge repository authority.
Use $mythic-edge-workflow.

Act as Codex E: Independent App-Native R0 Successor Parent Controller Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/828
Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/826
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review exactly:
docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md

Bind the exact SHA-256 reported by Codex B. Refresh origin/main and GitHub
state. Confirm the exact two-path implementation envelope is complete and that
every accepted #826 path and the frozen predecessor observer remain unchanged.

Independently review the owner-operated attached-console ingress, private-value
custody, exact structured child construction, creation-time Job Object
membership, zero-descendant topology, bounded streams, timeout, termination,
exactly-once close evidence, pre/post effects, all 15 PostExitFacts derivations,
failure precedence, pure-sealer call, nonretry lifecycle, and operation-free
tests. Confirm `ME-RP-828-E-001` is closed by stable bounded queue audits before
the read, after the complete terminated single-line read, and immediately
before launch. Verify prebuffered character input, multi-line paste, queue
inspection uncertainty, and prelaunch character input fail before child entry;
verify an ordinary single line remains reachable; and verify no queue flush,
discard, retry, schema, lifecycle, helper, or third implementation path was
introduced. Confirm the current Codex shell remains a live-execution nonclaim.

Run contract-only structural and operation-free existing regression checks. Do
not implement, access a private path, start a controller or child, generate or
consume an identity, publish a receipt, touch issue #769, authorize Observation
1 or 2, advance R0-R8 or Stage 4, submit, merge, deploy, or claim readiness.

Lead with findings. Return the reviewed SHA-256, contract verdict, two-path and
private-ingress constructibility verdicts, validation, authority flags,
generated residue count, and workflow_handoff. If accepted, route to a separate
owner implementation decision and then Codex C.
```

```yaml
instruction_context:
  role: "B"
  risk_tier: "high"
  observed:
    - "The accepted #826 harness exposes immutable PostExitFacts and a pure sealer but no native parent operation."
    - "The current Codex shell exposes a command string, not the required structured native evidence surface."
    - "Issue #769 is open with zero comments."
    - "Independent review found the initial ingress did not reject prebuffered or queued second-line character input."
  derived:
    - "A two-file owner-operated controller can close the parent-evidence boundary without changing accepted #826 bytes."
    - "Attached-console ReadConsoleW ingress avoids command, environment, file, and durable private-path transfer."
    - "Three bounded non-consuming queue audits close E-001 without changing the process or receipt boundary."
  proposed:
    - "One successor-only controller plus one operation-free fake-native test."
  unknown:
    - "The future exact controller-runtime and target-executable bindings, which belong to a later owner decision."
    - "Whether independent review will prove every Win32 ownership route constructible within two files."
  authority_conflicts_found: false

workflow_handoff:
  role_performed: "Codex B: App-Native R0 Successor Parent Controller Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/828"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/826"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  base_commit: "f8e6fc186094182c68a98ebdf229123809e3d5cc"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md"
  implementation_paths:
    - "tools/run_role_pool_app_native_r0_observation_parent.py"
    - "tests/test_run_role_pool_app_native_r0_observation_parent.py"
  implementation_path_count: 2
  private_ingress: "bounded_attached_console_ReadConsoleW_no_echo_with_three_queue_audits"
  finding_status:
    ME-RP-828-E-001: "contract_corrected_pending_independent_confirmation"
  current_codex_shell_live_compatible: false
  implementation_authorized: false
  private_path_accessed: false
  controller_started: false
  child_created: false
  identity_created_or_consumed: false
  observation_authorized: false
  receipt_publication_authorized: false
  observation_2_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: Independent App-Native R0 Successor Parent Controller Contract Reviewer"
```
