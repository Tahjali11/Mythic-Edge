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
- Split-integration correction base commit:
  `68e3eff41ef1c531ced5e1df0b0b136562ee7e30`.
- Split-integration correction base tree:
  `27c4874937a915894f63d9ef6204f3177e7828e9`.

The owner's current instruction is a task-scoped `explicit_user_override` for
this one successor-parent-controller correction under open lifecycle issue
#826. It expires with this handoff. It creates no private-input,
controller-start, process-launch, observation, consumption, publication, or
rung authority.

Issue #828 is closed and historical. PR #829 integrated the exact controller
and controller test; PR #830 integrated the accepted predecessor version of
this contract. Issue #769 remains open with zero comments and is not a
coordination surface for this correction. The pre-existing
`frontend/.wrangler/` residue in the main checkout is preserved without
inspection or mutation and must not be represented as fresh-review cleanliness.

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
4. **Observed:** PR #829 already integrated one successor-only Windows parent
   controller and one operation-free focused test. The bounded repair remains
   exactly those two implementation paths; it does not reopen the completed
   capability issue or authorize another implementation surface.
5. **Decision:** private target selection uses bounded attached-console input
   through `ReadConsoleW` with echo disabled. The private target path is never
   a command argument, environment value, file, registry value, clipboard
   value, prompt, log, exception, result, receipt, comment, or handoff value.
6. **Decision:** this is an owner-operated boundary. The current noninteractive
   Codex shell is not a conforming live caller. That nonclaim does not block
   inert implementation or operation-free review, but it does block live use
   until a fresh owner decision selects a conforming interactive Windows host.
7. **Observed:** six post-merge review threads remain unresolved: PR #829 found
   that authority and checkout eligibility were assigned to the controller and
   that continuously productive drains could postpone the deadline; PR #830
   found an unguarded child-checker byte window, a prospective sequence that
   contradicted the integrated implementation, and an overclaim about console
   queue stability.
8. **Decision:** the external owner-operated preflight exclusively owns
   current-main, clean-worktree, GitHub decision, and exact consumption
   verification. The controller receives no new authority input, performs no
   Git or GitHub operation, and makes no authority-authentication claim.
9. **Decision:** controller-owned pre/post repository-effect comparison and
   critical-artifact guards remain mandatory. The exact child checker gains a
   write/delete-denying guard held from prelaunch through terminal cleanup.
10. **Decision:** every stdout, stderr, and completion-port servicing step is
    deadline-aware and work-bounded so continuous production cannot postpone
    timeout, termination, or cleanup.
11. **Decision:** the attached console is a trusted owner-controlled ingress
    boundary. Bounded audits reject observed prebuffered character input and
    multiline paste, but do not claim protection against an adversarial process
    concurrently mutating the same console queue.
12. **Decision:** this correction is retrospective. The implementation and
    predecessor contract are already integrated; this successor correction
    governs only the exact bounded contract, controller, and controller-test
    repair package.
13. **Observed:** PR #831 integrated this correction contract alone at
    `68e3eff41ef1c531ced5e1df0b0b136562ee7e30`. Fresh independent review then
    accepted the exact two-file correction at controller SHA-256
    `2f7daaca6b9643dd39182e208501e50062164c99cd177638d72e13743abd572e`
    and test SHA-256
    `32a2e01667613ec5aed404bf639f575995e32b2b8bb005674dd0194940a5daa3`.
    Requiring that already integrated contract path to appear unchanged in the
    later implementation PR is no longer constructible.
14. **Decision:** correct only that sequencing error. This exact amendment is
    one contract-only integration package. After its independent acceptance
    and integration, the exact accepted controller and test form a separate
    two-file implementation package. Neither package may contain another path,
    and no implementation behavior or reviewed byte is reopened.

Finding `ME-RP-826-PARENT-A-001` is
`contracted_successor_boundary_pending_independent_review`.

Finding `ME-RP-828-E-001` is
`superseded_by_trusted_console_boundary_pending_independent_confirmation`.

Finding `ME-RP-826-E-004` is
`six_post_merge_review_threads_contracted_pending_independent_confirmation`.

Finding `ME-RP-826-E-005` is
`fresh_clean_review_worktree_required_after_integration`; the existing main
checkout is not cleaned or mutated to satisfy that later gate.

Finding `ME-RP-826-SPLIT-B-001` is
`split_integration_sequence_contracted_pending_independent_confirmation`.

### Split-integration sequencing correction

This subsection supersedes only the same-PR and three-path-integration wording
in the future authority sequence, submission-envelope paragraph, acceptance
paragraph, review prompt, and workflow handoff. Every technical requirement,
implementation boundary, validation requirement, nonclaim, and authority
ceiling elsewhere in this contract remains unchanged.

The immutable sequencing predecessor is the `48527`-byte contract integrated
by PR #831 at SHA-256
`0d46c5f5466d542e56fbe8ee138b4710acb7d8e5878a7be3ecb20dbb629b2581`.
PR #831 remains historical accepted contract-only integration evidence. The
accepted implementation candidate remains exactly:

1. `tools/run_role_pool_app_native_r0_observation_parent.py`: `82771` bytes;
   SHA-256
   `2f7daaca6b9643dd39182e208501e50062164c99cd177638d72e13743abd572e`;
2. `tests/test_run_role_pool_app_native_r0_observation_parent.py`: `56400`
   bytes; SHA-256
   `32a2e01667613ec5aed404bf639f575995e32b2b8bb005674dd0194940a5daa3`.

The implementation candidate's independent technical acceptance remains
evidence, not submission authority. This amendment neither changes those bytes
nor permits a new Codex D repair unless later review identifies a concrete
technical defect.

### Historical predecessor and review evidence

- Accepted predecessor contract: `35296` bytes; SHA-256
  `a54caf3f16abb3f01becb0e8addcb8923c65714b4ed889ef67e38a4f013154d0`.
- Integrated controller: SHA-256
  `b0fd13c96b264230562113abfc90d880c7fbbc51a50ef6abec9ddfeeab923e64`.
- Integrated controller test: SHA-256
  `e4f2dce0341be0ad0d710de3142a2fa4bde7dc1895ea536aa135074788307410`.
- PR #829 reviewed head: `a7eab2e41615da49d8212535fddfe06d084c0aee`;
  unresolved threads `PRRT_kwDOSaCjf86Xq998`,
  `PRRT_kwDOSaCjf86Xq999`, and `PRRT_kwDOSaCjf86Xq9-A`.
- PR #830 reviewed head: `a73c42474f7bd9e0869757d3200e66e87ef635a0`;
  exact-head contract-only review `PRR_kwDOSaCjf88AAAABI5yAMg`; unresolved
  threads `PRRT_kwDOSaCjf86XrITJ`, `PRRT_kwDOSaCjf86XrITM`, and
  `PRRT_kwDOSaCjf86XrITN`.

These hashes and references are immutable historical evidence. This correction
supersedes the affected requirements prospectively; it does not rewrite or
erase the accepted predecessor review record.

| Review thread | Finding | Contract disposition |
| --- | --- | --- |
| `PRRT_kwDOSaCjf86Xq998` | Controller claimed decision/consumption authority | Current-main, clean-worktree, GitHub decision, and exact consumption verification belong exclusively to external owner-operated preflight; controller authentication claim forbidden. |
| `PRRT_kwDOSaCjf86Xq999` | Continuous drains can postpone timeout | Every stdout, stderr, and completion-port service cycle is monotonic-deadline-aware and work-bounded. |
| `PRRT_kwDOSaCjf86Xq9-A` | Controller did not prove exact checkout | Exact checkout eligibility belongs to external preflight; controller retains only frozen-critical-artifact checks and pre/post repository-effect comparison. |
| `PRRT_kwDOSaCjf86XrITJ` | Child-checker bytes unguarded across launch | Exact checker is opened with write/delete sharing denied and held through terminal cleanup with exactly-once close evidence. |
| `PRRT_kwDOSaCjf86XrITM` | Prospective sequence contradicted integrated paths | Sequence is retrospective; only the exact bounded repair is prospective, and the stale absent-path stop condition is superseded. |
| `PRRT_kwDOSaCjf86XrITN` | Queue audit overclaimed same-count stability | Console is explicitly trusted and owner-controlled; observed buffered/multiline input rejects, while adversarial concurrent mutation protection is a nonclaim. |

Every row is `contracted_pending_fresh_contract_only_E_confirmation`. Thread
resolution is a later GitHub lifecycle effect and is not performed by Codex B.

## Exact Frozen Bindings

| Artifact or fact | Exact binding |
| --- | --- |
| Repository ID | `1235264383` |
| Repository name | `tahjali11/mythic-edge` |
| Accepted predecessor parent-controller contract | `35296` bytes; `a54caf3f16abb3f01becb0e8addcb8923c65714b4ed889ef67e38a4f013154d0` |
| Integrated parent controller | `b0fd13c96b264230562113abfc90d880c7fbbc51a50ef6abec9ddfeeab923e64` |
| Integrated parent-controller test | `e4f2dce0341be0ad0d710de3142a2fa4bde7dc1895ea536aa135074788307410` |
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

## Retrospective Correction And Future Authority Sequence

PR #829 already integrated the controller and controller test, and PR #830
already integrated the accepted predecessor contract. Their integration is
historical evidence, not proof that the six later review findings are closed.
The exact two-file repair is complete and independently accepted. No further
Codex D work is authorized absent a new concrete implementation finding.

The conditional correction sequence is:

1. fresh Codex E reviews this split-integration correction only;
2. after acceptance and a separate owner submission decision, Codex F submits
   exactly this one contract path in one draft PR targeting `main`;
3. only if that submitted head remains exact, required checks pass, and fresh
   exact-head E review is clean may Codex G integrate the contract-only package;
4. from the resulting exact current `main`, fresh Codex E confirms the merged
   contract and the exact two-file implementation candidate together and
   reproduces the required operation-free checks;
5. after that acceptance and a separate owner submission decision, Codex F
   submits exactly the two implementation paths in one draft PR targeting
   `main`;
6. only if the implementation head remains exact, all required checks pass,
   every applicable review thread is resolved, and fresh exact-head E review is
   clean may Codex G squash-merge that exact two-file package; and
7. after both integrations, a fresh current-main eligibility review runs from
   a newly created clean review worktree. The existing main checkout is not
   cleaned or mutated to satisfy this gate. One public-safe #826 comment is
   permitted only if every exact eligibility gate passes.

The conditional chain stops on head drift, scope expansion, unknown GitHub
state, failed validation, unresolved review finding, private-value requirement,
operational process, or generated residue in the fresh review worktree. Codex G
must not close #826 or mutate #769, #746, or #813.

Any later controller execution is outside this correction authority. Before a
controller process may start, an external owner-operated preflight must prove
the exact current `main` commit and tree, synchronization with `origin/main`, a
clean dedicated operation worktree, exact integrated artifact bytes, required
GitHub issue states, one fresh 12-hour single-use owner decision, and a
byte-identical canonical consumption record and readback. The preflight keeps
that evidence outside controller inputs and starts the controller at most once
only after every predicate passes.

The controller does not authenticate or claim GitHub authority. It does not
create, post, fetch, repair, or infer a decision or consumption record; inspect
`.git`; determine branch, HEAD, remote synchronization, or worktree
cleanliness; invoke Git; access the network; or accept an authority token,
decision reference, consumption reference, commit, tree, or cleanliness claim
as a new input. External preflight success is a necessary precondition, not a
controller-produced fact and not sufficient execution authority by itself.

After exact external consumption, the controller start is the sole execution
attempt. Every startup, ingress, binding, launch, cancellation, timeout,
cleanup, output, sealing, or publication outcome permanently retires that
decision and identity. Unknown decision, consumption, readback, current-main,
or clean-worktree state stops in the external preflight before controller start
and permits no replacement or retry.

## Owning Layer And Files

The successor parent owns only private executable custody; critical-artifact
guards; parent-observed process, stream, timeout, termination, cleanup, and
effect evidence; and `PostExitFacts`. The accepted #826 harness remains sole
owner of child validation, schema parsing, status selection, canonical receipt
construction, and sealing. GitHub remains the durable owner of later decision,
consumption, and candidate-publication evidence. The external owner-operated
preflight owns current-main, clean-worktree, GitHub decision, and consumption
verification. The human owner alone grants execution authority.

This Codex B correction changes only:

- `docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md`

The exact accepted implementation envelope is the two integrated paths:

1. `tools/run_role_pool_app_native_r0_observation_parent.py`
2. `tests/test_run_role_pool_app_native_r0_observation_parent.py`

No third implementation, test, fixture, bootstrap, configuration, schema,
status, receipt, lifecycle contract, predecessor observer, service, broker,
GitHub client, launcher, helper, fallback, private ingress, or evidence path is
permitted. Every accepted #826 path and the predecessor observer remain
byte-identical. The complete future submission envelope is exactly two ordered,
nonoverlapping packages: first this one contract path, then the two
implementation paths. No package may add another path, and the implementation
package cannot precede exact contract integration and current-main E review.

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

After the external owner-operated preflight passes, the owner starts the
controller once from an already-running trusted owner-controlled interactive
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

External exact decision and consumption verification are preconditions, not
controller steps or claims. After that external preflight is complete, `main`
obtains the target executable through the trusted owner-controlled attached
console:

1. require Windows `os.name == "nt"` and `sys.platform == "win32"`;
2. require `GetStdHandle(STD_INPUT_HANDLE)` to identify an attached console
   accepted by `GetConsoleMode`, not a pipe, file, pseudo-input, or redirect;
3. snapshot the exact console input mode and require `ENABLE_LINE_INPUT`;
4. disable `ENABLE_ECHO_INPUT` without changing unrelated mode bits;
5. perform the pre-read queue audit defined below; require that the bounded
   snapshots expose zero pending character-producing input before
   `ReadConsoleW`;
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

Each queue audit is the same closed non-consuming operation within the trusted
owner-controlled console boundary:

1. call `GetNumberOfConsoleInputEvents` and reject failure or a count greater
   than `4096`;
2. when the count is nonzero, call `PeekConsoleInputW` once into a bounded
   mutable `INPUT_RECORD` buffer and require exactly that count to be returned;
3. call `GetNumberOfConsoleInputEvents` again and require the same count; and
4. reject any `KEY_EVENT` record whose `bKeyDown` is true and whose
   `UnicodeChar` is not NUL.

An API failure, short peek, malformed record, over-limit count, or observed
changed count is queue-inspection uncertainty and selects
`observation_binding_rejected` before process entry. Within the trusted
owner-controlled boundary, observed prebuffered character input is never
accepted as the owner's contemporaneous line, and an observed multi-line paste
cannot be reduced to its first line. Queue records are never dequeued by an
audit. Input arriving after the final successful audit cannot affect the child
because the controller performs no further console input operation.

The audits do not establish atomic queue snapshots, exclusivity, or protection
against an adversarial process concurrently consuming, replacing, reordering,
or appending console input records. The owner must ensure no untrusted or
competing process can mutate the attached console queue for the duration of
ingress. Loss of that trusted boundary stops before controller start; the
controller neither detects every same-count replacement nor claims hostile
same-console containment.

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

Before the sole process-entry call, the controller independently opens the
exact child checker
`tools/check_role_pool_r0_offline_observation.py` as an ordinary non-reparse
file while denying write and delete sharing. It verifies stable volume/file
identity, exact byte length, and SHA-256 against the frozen R0-checker binding,
then retains that guard continuously across process entry, child lifetime,
terminal readback, post-exit inventory, and cleanup. A replacement, write, or
delete attempt must be denied while the guard is held. Any pre-entry checker
identity or byte mismatch is `observation_binding_rejected`; any post-entry
identity uncertainty is fail-closed. The checker guard receives exactly one
close attempt during terminal cleanup, and a failed or unknown close makes
`cleanup_confirmed=false` and selects the cleanup-failure route. The guard does
not change the fixed relative child command or disclose a new child path.

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
- Stdout, stderr, and completion-port work are serviced concurrently from
  process entry through the complete terminal boundary by a closed scheduler.
  Every service cycle performs at most one bounded nonblocking stdout read, at
  most one bounded nonblocking stderr read, at most `32` completion-port packet
  reads, and one terminal-state query. The cycle checks the monotonic clock
  before and after every native operation and returns to the deadline decision
  after that finite work; no drain helper may loop until a producer becomes
  empty.
- Every pipe read is capped to the remaining retained ceiling plus one overflow
  sentinel byte. Every completion-port call is nonblocking or bounded by the
  lesser of the remaining monotonic time and the current reconciliation
  deadline. An empty, busy, or continuously replenished source yields control
  after its per-cycle budget.
- When the `120`-second deadline is reached, ordinary servicing stops, timeout
  becomes terminal for the acceptance route, and the controller makes at most
  one termination request. The `5`-second reconciliation grace uses the same
  bounded service-cycle rules and its own monotonic deadline. Continuous
  stdout, stderr, or completion-port production therefore cannot postpone
  timeout, termination, zero-survivor reconciliation, or cleanup.
- Stdout may retain at most `4096` bytes and stderr at most `128` bytes. The
  first overflow closes the acceptance route and requests termination.
- Success requires child exit `0`, complete stdout EOF containing exactly one
  accepted 37-field validation payload, complete stderr EOF with zero bytes,
  and no unconsumed bytes.
- Timeout, cancellation, overflow, unsafe topology, or uncertain terminal state
  causes at most one `TerminateJobObject` request followed by one bounded
  `5`-second reconciliation wait. There is no relaunch or replacement.
- Every proven-owned process, thread, job, completion-port, target-guard,
  checker-guard, stdin, stdout, stderr, and pipe handle receives exactly one
  close attempt.
  Close attempts continue in reverse acquisition order after failures and
  aggregate deterministically.
- `DeleteProcThreadAttributeList` is attempted exactly once only after
  successful attribute-list initialization. It is not a handle-close event.
- Console-mode restoration is attempted exactly once if and only if mode
  mutation succeeded. The console handle is borrowed and is never closed.
- Any required close, deletion, mode restoration, bounded drain, terminal query,
  buffer clearing, or survivor check that fails or is unknown makes
  `cleanup_confirmed=false`.

No transcript, staging file, runtime-status file, log, cache, private evidence,
or durable controller artifact is created. The only successful local output is
the unchanged canonical receipt bytes. A fixed existing status plus final LF is
the only failure output; raw errors and exception chains are suppressed.

## Before And After Effect Evidence

The controller installs its Python audit observer before its first baseline and
keeps it active through sealing and cleanup. Before private input and again
after child termination, bounded drain, and cleanup, it derives bounded stable
inventories for:

- the exact repository tree;
- the exact installed Role Pool tree;
- the fixed registry, release, authority-index, validator, harness, and
  contract bindings; and
- contract-defined generated residue under the repository and installed tree.

Each inventory requires an ordinary, non-reparse root, deterministic ordinal
path ordering, and stable file identity during hashing. The pre-entry and
post-exit inventories must be exactly equal, and every separately frozen
critical artifact must match its accepted byte binding. Any sampling,
identity, read, guard, or equality uncertainty fails closed. This comparison
detects controller-lifetime repository effects; it does not authenticate Git
HEAD, branch, remote synchronization, or pre-existing worktree cleanliness.
Those eligibility predicates belong only to the external owner-operated
preflight. The controller performs no Git subprocess, network operation,
repair, cleanup of pre-existing state, reset, revert, or deletion.

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
| `cleanup_confirmed` | Every required bounded drain, terminal, zero-survivor, target/checker-guard close, other close, deletion, mode-restoration, effect, and residue check completed exactly. |
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
4. bounded queue audits proving that observed prebuffered character input,
   multi-line paste with a queued second line, queue-inspection failure or
   observed instability, and any observed prelaunch character input reject
   before child entry, while one ordinary trusted complete terminated line with
   empty character queues remains reachable; the fakes must also prove no audit
   dequeues or flushes input and must preserve the explicit nonclaim for an
   adversarial process concurrently mutating the same console queue;
5. private path absence from every public value, call record, exception,
   fixture representation, output, and serialized test artifact;
6. ordinary/non-reparse component validation, stable identity, exact owner
   binding, denied write/delete sharing for both the target and exact child
   checker, checker replacement blocked while its guard is held, and every
   pre/post identity or byte-drift route;
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
    bounded concurrent servicing, EOF, nonzero exit, nonempty stderr, and
    malformed payload; synthetic endless stdout, endless stderr, and endless
    completion-port production must each yield to the monotonic deadline;
13. timeout at the exact deadline despite continuous production, one
    termination request, bounded five-second reconciliation, and no retry or
    replacement;
14. every owned-resource acquisition prefix and every close-failure
    permutation receives exactly one reverse-order close attempt without
    short-circuiting; checker-guard close failure remains fail-closed with
    `cleanup_confirmed=false`;
15. attribute-list deletion and console-mode restoration ownership rules;
16. deterministic pre/post equality, repository-effect drift, write, network,
    external-effect, residue, unstable-read, and sampling-unknown cases without
    hard-coded effect counts;
17. exact construction of all 15 immutable `PostExitFacts` fields from parent
    evidence only;
18. exactly one call to the accepted pure sealer after complete cleanup and
    zero calls on every earlier failure;
19. canonical receipt output and every existing fixed failure output are
    public-safe and no-echo;
20. the accepted #826 files and predecessor observer remain byte-identical and
    no predecessor-observer function is imported or called; and
21. current-main, clean-worktree, GitHub decision, and consumption verification
    remain external preconditions rather than controller inputs or claims; the
    controller performs no Git subprocess or network access; and
22. one launch attempt, no retry, full cleanup, and no real process, task,
    network, GitHub, repository write, installed-tree write, registry, release,
    identity, consumption, or publication operation occurs.

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

Contract acceptance permits only the ordered split-integration route defined
above. The exact two-file repair is complete and independently accepted; this
amendment does not authorize further implementation. Exact ordered integration
of this contract-only amendment and the separately reviewed two-file
implementation package makes only a fresh current-main eligibility review from
a new clean review worktree possible. It does not activate the controller or
Observation 1.

Stop and return to Codex A or the owner if:

- either integrated implementation path is missing, either ordered package
  requires an extra path, the implementation candidate bytes drift, or the
  implementation package would precede exact contract integration;
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
- external preflight would need the controller to authenticate GitHub, inspect
  `.git`, accept a new authority input, invoke Git, or access the network;
- the trusted owner-controlled console boundary cannot be maintained without
  claiming adversarial same-console containment; or
- issue #769 would require any read beyond state/comment-count validation or
  any mutation.

This contract does not authorize implementation. Fresh contract-only E
acceptance creates eligibility only for a separate owner decision about Codex F
submission of this exact contract-only amendment. The accepted two-file
implementation package remains ineligible for submission until the amendment
is integrated and fresh current-main E review accepts the combined binding. No
current authority permits private-path access, controller start, child
creation, identity generation or consumption, observation execution,
candidate publication, Observation 2, task dispatch, R1-R8, Stage 4,
deployment, assurance, privacy guarantees, security guarantees, or live
readiness.

## Next Workflow Action

Next role: fresh independent Codex E contract reviewer.

Pasteable prompt:

```text
Use the current Mythic Edge repository authority.
Use $mythic-edge-workflow.

Act as Codex E: Fresh Parent-Controller Split-Integration Sequencing Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Lifecycle issue: https://github.com/Tahjali11/Mythic-Edge/issues/826
Completed capability issue: https://github.com/Tahjali11/Mythic-Edge/issues/828
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769
Implementation PR: https://github.com/Tahjali11/Mythic-Edge/pull/829
Contract PR: https://github.com/Tahjali11/Mythic-Edge/pull/830
Correction contract PR: https://github.com/Tahjali11/Mythic-Edge/pull/831

Review exactly:
docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md

Bind the exact byte count and SHA-256 reported by Codex B. Refresh origin/main
and use the GitHub connector for current issue, PR, review-thread, and check
evidence. Treat #828 and the PR integrations as historical. Confirm issue #826
is open, issue #769 is open with zero comments, all six PR #829/#830 review
threads remain the correction source, and the accepted predecessor contract
hash and review references remain preserved as historical evidence.

Independently verify that the contract closes all six findings within exactly
the existing contract plus two implementation paths: deadline-aware
work-bounded stdout/stderr/completion-port servicing; a write/delete-denying
exact child-checker guard through terminal cleanup with exactly-once close;
external owner-operated current-main, clean-worktree, GitHub-decision, and
consumption preflight; controller-owned pre/post repository-effect comparison;
trusted owner-controlled console ingress that rejects observed prebuffered and
multiline input without claiming adversarial concurrent-queue protection; and
truthful retrospective correction wording.

Verify the fixed child command, creation-time Job Object membership, zero
descendants and survivors, bounded output, cleanup inventory, all 15
PostExitFacts, pure sealer, nonretry lifecycle, and false-authority boundaries
remain unchanged. Confirm no Git subprocess, network access, authority input,
fourth path, harness change, lifecycle-contract change, predecessor-observer
change, schema, status, receipt, broker, launcher, helper, fallback, or new
private ingress was introduced.

Review `ME-RP-826-SPLIT-B-001` specifically. Confirm PR #831 integrated the
immutable predecessor contract alone at merge commit
`68e3eff41ef1c531ced5e1df0b0b136562ee7e30`, making its former single-PR
three-path instruction impossible. Confirm the amendment changes only
sequencing: first one contract-only package, then after integration and fresh
current-main E confirmation one exact two-file implementation package. Verify
the accepted controller and test remain exactly `82771`/`56400` bytes at
SHA-256 `2f7daaca6b9643dd39182e208501e50062164c99cd177638d72e13743abd572e`
and `32a2e01667613ec5aed404bf639f575995e32b2b8bb005674dd0194940a5daa3`.
No Codex D repair is authorized unless review finds a new concrete technical
defect.

Run contract-only structural and operation-free existing regression checks. Do
not implement, access a private path, start a controller or child, generate or
consume an identity, publish a receipt, touch issue #769, authorize Observation
1 or 2, advance R0-R8 or Stage 4, submit, merge, deploy, or claim readiness.

Lead with findings. Return the reviewed SHA-256 and byte count, one disposition
for each of the six threads, the exact future two-file repair scope, validation,
authority flags, generated residue evidence, and workflow_handoff. If accepted,
route to a separate owner decision for Codex F submission of the exact
contract-only package. Do not submit or merge during review. If any finding
requires wider scope, changed implementation bytes, or weaker containment,
stop and route to Codex A/owner.
```

```yaml
instruction_context:
  role: "B"
  risk_tier: "high"
  observed:
    - "PR #829 integrated the controller and test; PR #830 integrated the accepted predecessor contract."
    - "PR #831 integrated the correction contract separately before the exact two-file correction could be submitted."
    - "Fresh E review accepted the exact two-file correction and found only the now-impossible single-PR sequencing clause."
    - "Six post-merge PR #829/#830 review threads remain unresolved."
    - "Issue #769 is open with zero comments."
    - "The main checkout contains preserved pre-existing frontend/.wrangler/ residue and is not a clean-review-worktree proof."
  derived:
    - "All six findings fit the existing contract plus exact two-file repair envelope."
    - "The contract digest is not embedded by either implementation file, so split integration requires no byte change."
    - "External preflight ownership avoids a GitHub client, Git subprocess, or new controller authority input."
    - "A trusted-console nonclaim closes the overstatement without weakening buffered or multiline rejection."
  proposed:
    - "One contract-only sequencing amendment followed, after integration and E confirmation, by the exact accepted two-file package."
  unknown:
    - "The future exact controller-runtime and target-executable bindings, which belong to a later owner decision."
    - "Whether independent review will prove every Win32 ownership route constructible within two files."
  authority_conflicts_found: false

workflow_handoff:
  role_performed: "Codex B: App-Native R0 Successor Parent Controller Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/826"
  historical_capability_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/828"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  base_commit: "68e3eff41ef1c531ced5e1df0b0b136562ee7e30"
  base_tree: "27c4874937a915894f63d9ef6204f3177e7828e9"
  target_artifact: "docs/contracts/role_pool_codex_app_native_r0_successor_parent_controller.md"
  implementation_paths:
    - "tools/run_role_pool_app_native_r0_observation_parent.py"
    - "tests/test_run_role_pool_app_native_r0_observation_parent.py"
  implementation_path_count: 2
  private_ingress: "trusted_owner_controlled_attached_console_ReadConsoleW_no_echo_with_bounded_queue_audits"
  finding_status:
    ME-RP-828-E-001: "superseded_by_trusted_console_boundary_pending_independent_confirmation"
    ME-RP-826-E-004: "six_post_merge_review_threads_contracted_pending_independent_confirmation"
    ME-RP-826-E-005: "fresh_clean_review_worktree_required_after_integration"
    ME-RP-826-SPLIT-B-001: "split_integration_sequence_contracted_pending_independent_confirmation"
  current_codex_shell_live_compatible: false
  implementation_authorized: false
  further_codex_d_repair_authorized: false
  submission_authorized_now: false
  contract_submission_eligible_only_after_fresh_contract_e_acceptance_and_owner_decision: true
  implementation_submission_eligible_only_after_contract_integration_fresh_e_acceptance_and_owner_decision: true
  merge_authorized_now: false
  conditional_g_authorized_only_for_unchanged_clean_exact_head: true
  private_path_accessed: false
  controller_started: false
  child_created: false
  identity_created_or_consumed: false
  observation_authorized: false
  observation_1_decision_authorized: false
  receipt_publication_authorized: false
  observation_2_authorized: false
  r0_r8_advancement_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  deployment_authorized: false
  issue_769_mutation_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: Fresh Parent-Controller Split-Integration Sequencing Contract Reviewer"
```
