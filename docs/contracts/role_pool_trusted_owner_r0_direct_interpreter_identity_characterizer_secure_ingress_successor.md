# R0 Identity Characterizer Secure-Ingress Successor Contract

## Findings And Decision

1. **Observed:** `origin/main` is
   `4a126a9f0ccb9234f08f5d706dbba49f31a3c176`, with tree
   `8cabe0458d8d1d7e0e1e792cd3dc8f6c8c9b775e`. Pull request #797 merged the
   independently reviewed terminal-observability implementation at those
   exact bytes.
2. **Observed:** the accepted production wrapper
   `run_consumed_characterization` is inert until called and accepts exactly
   the keyword-only inputs `characterization_id`, `stdin`, and `stdout`. It can
   therefore be invoked once in the controller process without changing the
   characterizer algorithm or adding a process.
3. **Observed:** the current Codex shell does not provide the interactive
   no-echo stdin channel required to supply the accepted private path. No
   private input was read and no fresh authority or characterization ID was
   consumed while establishing this gap.
4. **Finding:** `ME-RP-795-INGRESS-A-001` is an environment-capability gap plus
   a missing parent-executor contract. It is not an identity-algorithm defect
   and does not justify changing the accepted wrapper, result, target command,
   or process rules.
5. **Decision:** add one owner-operated, repository-owned parent boundary made
   of an in-process terminal bootstrap and one direct CPython controller. The
   bootstrap proves its no-echo launch capability before consumption, and the
   controller reads the target path without echo and invokes the accepted
   wrapper once in-process.
6. **Decision:** the bootstrap and controller introduce no authority schema,
   consumption schema, result schema, terminal category, receipt path, helper
   process, or parallel execution lane. Their only durable result is the
   unchanged 33-field characterizer result when that result already exists.
7. **Decision:** ADR-0010 remains `Proposed` and non-precedential. This contract
   derives authority from the current owner instruction, issue #795, accepted
   ADR-0008, and the exact merged repository evidence below.
8. **Review finding:** `ME-RP-795-INGRESS-E-001` correctly identified that the
   first version did not define how the pre-existing terminal host obtained the
   private controller image before the controller existed. The narrow closure
   adds one repository-owned PowerShell launch bootstrap that executes inside
   the already-running terminal host. It consumes no process slot, reads the
   private launch image only after durable authority consumption, and starts
   exactly the one bound controller process with no shell or helper fallback.
9. **Review finding:** `ME-RP-795-INGRESS-E-002` confirmed that the only current
   host is Windows PowerShell 5.1 and does not expose
   `ProcessStartInfo.ArgumentList`. The narrow correction uses only its
   documented `Arguments` string with fixed public tokens and two closed,
   whitespace-free public identifiers. The private image remains exclusively
   in `ProcessStartInfo.FileName`.

`ME-RP-795-INGRESS-A-001` is
`contract_correction_authored_independent_review_pending`.
`ME-RP-795-INGRESS-E-001` is
`fixed_confirmed_contract_only`.
`ME-RP-795-INGRESS-E-002` is
`contract_correction_authored_independent_re_review_pending`.

## Authority And Sources

- Repository: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/795>
- Parent: <https://github.com/Tahjali11/Mythic-Edge/issues/780>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>
- Protected coordination surface:
  <https://github.com/Tahjali11/Mythic-Edge/issues/769>
- Accepted WIP-1 authority:
  [`ADR-0008`](../decisions/ADR-0008-repo-wip-1-lane-activation-policy.md)
- Proposed, non-precedential reference:
  [`ADR-0010`](../decisions/ADR-0010-bounded-scope-and-informed-approval.md)
- Constitution: [`docs/agent_constitution.md`](../agent_constitution.md)
- Codex B role: [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md)
- Contract template: [`docs/templates/module_contract.md`](../templates/module_contract.md)
- Source finding: owner-supplied Codex A secure-ingress framing for
  `ME-RP-795-INGRESS-A-001` in the current task.

Issue #795 is the active capability lane. Issues #780 and #746 remain open;
issue #769 remains open with zero comments. Open pull requests #374 and #391
are unrelated. The current owner invocation continues #795 for this one
docs-only Codex B artifact and expires at handoff.

## Frozen Public Bindings

| Binding | Exact value |
| --- | --- |
| Repository ID | `1235264383` |
| Base commit | `4a126a9f0ccb9234f08f5d706dbba49f31a3c176` |
| Base tree | `8cabe0458d8d1d7e0e1e792cd3dc8f6c8c9b775e` |
| Characterizer contract | `42661d3f445c7d93e6253105c09d27454a96607b9acb2f7b2499290abcfda904`; `42604` bytes |
| Characterizer contract review | `89ee9144a2dee459a819259f05db7b659c6dc589fc8ef635234333f0e03a2127`; `8893` bytes |
| Characterizer implementation review | `e7194ec6dad4ed1a678c18f7d80fa9155d257b290c2bf53142ee9d1f1de71dff`; `10969` bytes |
| Terminal-observability successor | `f1e9ab7642ba191edf5568638c83fe4df01babae5b379733d6172a2e426e33a1`; `26875` bytes |
| Terminal-observability contract review | `78a46dfafbfb5fc61cb0b22937cb96873873acf8173d2af89bbbd7132e2572c6`; `15971` bytes |
| Accepted current characterizer | `46404b68c7005ff1df06c24426514ceedc8478956b95fbb1c753e247550bd1d0`; `78153` bytes |
| Accepted current focused test | `64e6ba5bae8bf75908212f521658853e100ca53686005495255b767653a47493`; `37153` bytes |
| PR #797 reviewed head | `61b1ea8b247e19cdb05a1a84f59edf79a143d368` |
| PR #797 review | <https://github.com/Tahjali11/Mythic-Edge/pull/797#pullrequestreview-4839350984>; `1980` UTF-8 body bytes; `9a6e90eb8b4ef7f01a05f5d1057f5d277a316004dd2aca1c4745a66a52fb1e36` |
| PR #797 merge commit | `4a126a9f0ccb9234f08f5d706dbba49f31a3c176` |
| Direct-interpreter binding | `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333` |
| Historical consumed record | <https://github.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-5156641209>; `1436` UTF-8 body bytes; `9b0597d83d9f71e0918a248c7d03cda487c25eab0010bdb282c50540bfb4b0b0` |
| Historical characterization ID | `r0_direct_interpreter_identity_characterization_v1_b318c12adae04f5a80c55e46bc695d1d` |
| Historical disposition | `consumed_nonreusable`; controller execution `1`; exit `2`; canonical result absent |
| Reviewed predecessor | `246f50d84245e4c7512bcabeee3108941a1f3e4d3c391e40d1e9c8930cc115d9`; `35181` bytes |
| Blocking review | `1759abe1563a8bab26c398e9c6148a08a901055c377516be58fb88cc092dc973`; `12039` bytes; `ME-RP-795-INGRESS-E-001` |
| Public-argument predecessor | `436811c649bc57d74c995dd3e9a1398d01d37e880b45a3a8624c0bc9ca41162d`; `44416` bytes |
| Public-argument re-review | `f6d81ea9af445802c1132488f04ce54aaceb503e80bee826d222471b9e0dd760`; `16533` bytes; `ME-RP-795-INGRESS-E-002` |

Every named repository artifact must be an ordinary, non-reparse file at the
exact byte count and digest before later implementation or execution is
eligible. The historical decision, comment, ID, and attempt are immutable and
permanently nonreusable.

## Owning Layer And Scope

The trusted-owner R0 workflow owns authority sequencing. The launch bootstrap
owns only pre-consumption launch readiness, one post-consumption private launch-
image read, one controller start/wait, and its bounded cleanup. The new
controller owns only its local console readiness, the target private-line
transfer, one in-process wrapper call, bounded wrapper-output capture,
controller cleanup, and public-safe exit projection.

The existing characterizer remains sole owner of:

- the five identity observations and 11 identity categories;
- the fixed target command and native process adapter;
- target timeout, containment, descendant, output, identity, and cleanup
  evidence;
- the 33-field canonical result and its self-digest; and
- the 18-field all-false authority object.

The exact later Codex C implementation scope is three new paths:

1. `tools/start_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.ps1`
2. `tools/run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py`
3. `tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py`

All three paths must be absent before implementation. No existing source, test,
contract, report, registry, release record, installed skill, or canonical Role
Pool source may change. The launch bootstrap executes in the pre-existing
terminal host and creates no process of its own. Together, that bootstrap and
the new controller close the one missing parent boundary; neither is a second
characterizer, fallback path, helper process, or parallel lane.

## Exact Pre-Controller Launch Ingress

The owner starts the public repository-owned launch bootstrap from one already-
running, owner-controlled Windows-hosted PowerShell console process. The bootstrap is
invoked in the current PowerShell process from its exact repository path; it
must not start another PowerShell, shell, launcher, helper, broker, service, or
scheduled task. Its invocation contains only the public script path, fresh
public characterization ID, and public owner-decision reference. No private
value appears in the invocation, command history, arguments, environment,
working directory, title, or durable output.

Before durable authority consumption, the bootstrap must prove, without
reading a private character, that:

1. it is executing in one already-running Windows PowerShell process with an
   attached interactive console and no redirected or synthetic stdin;
2. its source and the public repository, issue, contract, review, controller,
   characterization-ID, and owner-decision bindings are exact;
3. the repository root and fixed controller path are ordinary, non-reparse,
   and exact, while the fixed controller is invoked only as public source;
4. `[Console]::KeyAvailable` plus `[Console]::ReadKey($true)` is the selected
   documented no-echo launch-image reader and has not yet read a character;
5. `System.Diagnostics.ProcessStartInfo` and `System.Diagnostics.Process.Start`
   are available with `UseShellExecute=false`, fixed `WorkingDirectory`, and
   the Windows PowerShell 5.1-compatible `Arguments` string property;
6. no PATH lookup, executable association, shell execute, `py.exe`, alias,
   shim, wrapper, alternate runtime, child process, private read, or durable
   mutation has occurred; and
7. one monotonic timeout, cancellation handling, fixed categorical failure
   output, and final cleanup path are installed.

Controlling API references:

- <https://learn.microsoft.com/en-us/dotnet/api/system.console.readkey>
- <https://learn.microsoft.com/en-us/dotnet/api/system.console.keyavailable>
- <https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.useshellexecute>
- <https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.arguments>

Only then may it display this fixed public-safe console line:

`R0 secure launch ingress ready; consume authority, then press Enter.`

The trusted owner performs and exactly reads back the single-use issue #795
consumption transition before pressing Enter. That Enter confirms an already
durable transition; it is not authority. The bootstrap then uses only
`[Console]::KeyAvailable` plus `[Console]::ReadKey($true)` and accepts one
private absolute value whose basename is exactly `python.exe`. The `true`
intercept argument prohibits console echo. One 120-second monotonic deadline,
at most 12001 availability polls, at most 8192 key reads, and a 4095 UTF-8-byte
payload ceiling bound the read without a thread or helper. It converts
that bounded value only long enough to set `ProcessStartInfo.FileName`, requires
`UseShellExecute=false`, uses the exact fixed public `Arguments` string and
exact public repository working directory, starts exactly one controller, and
immediately attempts best-effort clearing of every mutable buffer and unmanaged
temporary it owns. It does not claim complete clearing of immutable PowerShell
or .NET objects. The dedicated terminal host must exit after the one attempt so
its process lifetime bounds those otherwise unzeroizable objects.

The bootstrap must never display, serialize, interpolate into a command line,
log, compare textually in public output, or retain the private launch image.
It may emit only fixed categorical setup, consumption, launch, wait, exit, and
cleanup outcomes. `ProcessStartInfo.FileName` is the one private native launch
field; it is not part of the public controller argument list. Any inability to
prove no-echo input, exact consumption, `UseShellExecute=false`, one-controller
creation, or bounded cleanup permanently retires the attempt. There is no
retry, relaunch, alternate reader, shell fallback, or second launch path.

The bootstrap waits for the one controller to exit, propagates only its public
exit code, and performs no canonical-result parsing or rewriting. Controller
stdout and stderr remain attached to their original console handles. The
bootstrap creates no receipt, schema, file, pipe, thread, or durable artifact.

## Exact Controller Runtime And Direct Launch

The controller runtime reuses the accepted
`trusted_owner_r0_direct_cpython_binding.v1` object. No second runtime binding
is created. The running controller must privately reproduce all of these
accepted values before it announces readiness:

| Field | Exact value |
| --- | --- |
| OS/runtime | `nt`; `win32`; `CPython` |
| Executable basename | `python.exe` |
| File/product version | `3.13.14` / `3.13.14` |
| Byte length | `105696` |
| File SHA-256 | `ef8f51028ac5329641985112f8efb1c2d4c47c86b8011ddf7e6fae21e2b4e5a1` |
| Stable identity schema | `trusted_owner_direct_cpython_file_identity.v1` |
| Stable identity SHA-256 | `570754cbc03fb52f4e846c3611e48e18334f08e621babfa2e8eb76f4a0e5c953` |
| Ordinary/reparse state | `true` / `false` |
| Binding SHA-256 | `2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333` |

The pre-existing terminal host, through the exact in-process bootstrap above,
starts the controller once. The only admissible launch uses
`ProcessStartInfo` with `UseShellExecute=false` and:

- `lpApplicationName` equal to the privately held exact bound `python.exe`;
- no PATH lookup, file association, shell execution, `py.exe`, WindowsApps
  alias, shim, wrapper, launcher, broker, service, scheduled task, or fallback;
- `Arguments` containing one ASCII string assembled from exactly seven public
  tokens separated by one U+0020 space and containing no leading or trailing
  space:
  `-I -B tools\\run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py --characterization-id <characterization_id> --owner-decision-ref <owner_decision_ref>`;
- `<characterization_id>` matching exactly
  `\Ar0_direct_interpreter_identity_characterization_v1_[0-9a-f]{32}\z`;
- `<owner_decision_ref>` matching exactly
  `\Ahttps://github\.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-[1-9][0-9]{0,19}\z`;
- ordinal ASCII validation of both variable tokens before string assembly,
  explicit rejection of whitespace, quotation marks, backticks, NUL, control
  characters, leading option markers, alternate URL forms, and any value not
  identical to the predeclared public owner decision; and
- a complete `Arguments` UTF-8 byte count no greater than `512`; the private
  application image is `FileName`, never an argument or part of `Arguments`;
- `lpCurrentDirectory` equal to the exact repository root;
- no private target path in the controller argument vector, environment,
  working-directory selection, or process-title customization; and
- inherited standard handles from the same interactive console, with no
  redirected or synthetic stdin.

No generic quoting, escaping, interpolation, or caller-selected argument
builder is permitted. Because every admitted token is ASCII and contains no
space or quotation mark, the exact one-space join is the only construction.
After launch, the controller must require `sys.argv` to contain exactly the
fixed script entry followed by the four option/value tokens above and reject
duplicates, reordering, missing tokens, extras, option-like values, or any
normalization. The bootstrap never logs `Arguments`, even though every token is
public.

The application image is the runtime binding, not a caller-selected target
argument. The private target line is a distinct later ingress value and may
not be inferred from `sys.executable`; equality is validated only after exact
consumption. The controller keeps its runtime path and all file identity facts
in bounded private memory and emits none of them.

The argument prohibition in this successor governs owner input and the
controller launch. It does not reinterpret or change the accepted wrapper's
internal fixed-target construction: after consumption, that wrapper privately
derives both `CreateProcessW.lpApplicationName` and target `argv[0]` from the
validated path. That bounded internal native use is not a caller-selected
controller argument and remains governed by the accepted characterizer
contract's no-echo and memory-lifetime rules.

If the terminal bootstrap cannot prove its pre-consumption readiness, it stops
before authority consumption. If consumption, private launch-image ingress,
controller creation, or runtime reproduction later fails, the attempt is
permanently consumed and nonreusable. Another process between terminal host and
controller is forbidden. There is no ambient-shell or alternate-runtime
fallback.

## Process Topology

The process roles are disjoint:

1. `terminal_host`: one pre-existing owner-controlled Windows-hosted PowerShell
   console process. It executes the repository-owned launch bootstrap
   in-process, performs only launch readiness, durable-consumption confirmation,
   one no-echo launch-image read, one controller start/wait, and bounded cleanup;
   it is not created by this operation and performs no characterizer work.
2. `controller`: exactly one directly launched process running the new
   repository-owned controller under the exact runtime above.
3. `in_process_wrapper`: the existing
   `run_consumed_characterization` function imported from the exact accepted
   characterizer bytes; it is not a process or thread.
4. `fixed_target`: zero or one direct child created only by the unchanged
   wrapper/native adapter with the accepted fixed command.

The launch bootstrap is code in `terminal_host`, not a process or thread. There
is no process between terminal host and controller and none between
controller and fixed target. `bootstrap_invocation_limit=1`,
`controller_execution_limit=1`,
`wrapper_invocation_limit=1`, `target_process_limit=1`, and
`target_descendant_process_limit=0`. The fixed target is not counted as its own
descendant. No thread may be created for input, timeout, output, authority, or
cleanup handling.

The existing result fields `process_launch_count`, `top_level_process_count`,
and `descendant_process_count` continue to describe only the fixed target and
its descendants. This successor does not reinterpret them to count the
controller or pre-existing terminal host.

## Controller Console Readiness

The controller uses only the Windows CPython 3.13 `msvcrt` console interface
and read-only Win32 handle/mode inspection. The controlling semantics are:

- Python 3.13 `msvcrt.getwch()` reads one wide console character without
  echo;
- `msvcrt.kbhit()` reports whether a keypress is waiting without blocking;
- `msvcrt.putwch()` writes only the fixed public readiness text directly to
  the console rather than the result streams;
- `GetConsoleMode` identifies a real console input handle and captures its
  current mode; and
- command-line programs capture the initial console mode and verify or restore
  it before exit.

References:

- <https://docs.python.org/3.13/library/msvcrt.html>
- <https://learn.microsoft.com/cpp/c-runtime-library/reference/getch-getwch>
- <https://learn.microsoft.com/windows/console/getconsolemode>
- <https://learn.microsoft.com/windows/console/console-modes>

Before controller target ingress or wrapper entry, the controller must prove
all of the following in order:

1. the host is Windows and the exact runtime/public bindings are valid;
2. stdin is the inherited standard-input handle, is a character device, is a
   console input buffer, and passes `GetConsoleMode`;
3. `msvcrt.kbhit`, `msvcrt.getwch`, and the monotonic clock are present and
   callable;
4. no keypress is pending, so stale input cannot be mistaken for owner
   confirmation or private input;
5. the original console input mode is retained in bounded memory;
6. controller stdout is writable and controller stderr has emitted no bytes;
7. the accepted characterizer module and exact
   `run_consumed_characterization` signature load without executing a process;
8. no target process has started and no private line has been requested or
   read; and
9. cancellation and a `finally` path are installed before readiness is
   announced.

The controller must not call `SetConsoleMode` on the ordinary path.
`getwch()` supplies the no-echo primitive directly. Before every exit, it must
re-read the console mode and require exact equality with the startup snapshot.
If code ever changes an owned mode after a partial failure, it must attempt one
restoration to the exact snapshot and verify readback. An unverified mode state
is terminal `unknown`; it cannot produce a result or a cleanup-success claim.

After launch and self-binding validation, controller readiness is announced
only through one fixed public-safe console-device line:

`R0 identity characterizer target ingress ready; enter the bound path.`

It is written directly to the attached console, not to the result stdout or
stderr streams, and contains no dynamic value. No console title, custom process
title, path, ID, digest, timestamp, or machine value may be displayed.

## Authority Consumption And Two-Stage Ingress

This controller has no GitHub, credential, network, browser, or issue-write
capability. Authority consumption remains the existing trusted-owner manual
transition on issue #795, not a controller side effect and not a new schema.

The exact sequence is:

1. a fresh owner execution decision predeclares one new characterization ID,
   one decision reference, the accepted controller/contract/review bindings,
   and limits from this contract;
2. the in-process terminal bootstrap reaches its exact launch-ingress readiness
   boundary without reading private input or creating a process;
3. while the bootstrap waits, the trusted owner creates exactly one durable
   consumption comment on issue #795 using the existing consumption shape;
4. the trusted owner re-reads that comment and confirms its exact issue,
   actor, fresh ID, contract/review/implementation bindings, limits,
   `consumed_nonreusable` state, and all false authorities;
5. only after that exact readback does the owner press Enter once in the
   terminal bootstrap;
6. the bootstrap reads the private launch image once without echo and starts
   the exact controller once;
7. the controller reproduces the accepted runtime binding, proves its inherited
   console, and announces the fixed target-ingress readiness line; and
8. the owner enters the same bound private path once without echo for the
   unchanged wrapper input.

The bootstrap launch image and the controller target line are not compared by
echoing, serializing, or transferring either raw value. They independently
must reproduce the same accepted direct-interpreter binding, so a different
file, alias, or identity fails closed without a raw-path comparison artifact.

The first Enter key is an owner confirmation of an already completed durable
transition; it is not itself authority and cannot repair a missing or invalid
comment. Fresh Codex E result review must independently re-read the comment.
If the comment is absent, mismatched, duplicated, edited, ambiguous, or cannot
be re-read, any controller output is rejected and the attempt is permanently
nonreusable.

The bootstrap waits at most `600` seconds for the exact confirmation Enter.
Any other key, buffered input, timeout, cancellation, loss of console, or
unknown state stops before private input. If durable consumption might already
have occurred, the decision is conservatively treated as consumed and
nonreusable; a fresh task reconciles the comment before any successor is
considered. No controller relaunch is permitted under the same decision.

The terminal bootstrap owns its one `600`-second confirmation deadline and one
no-echo launch-image read. The controller private phase uses one separate
120-second monotonic deadline, at most `12001` polls, and at most `8192`
`getwch()` calls including surrogate, backspace, special-key rejection, and
the terminating Enter. Deadline checks dominate further input calls. No
bootstrap or controller timeout starts a replacement process.

## Private One-Line Ingress

After confirmation, the controller reads the private path only through
`msvcrt.kbhit()` plus `msvcrt.getwch()` on the already-proved console. It must:

- wait at most `120` seconds for the terminating Enter;
- accept one absolute path whose basename is exactly `python.exe`;
- accept at most `4095` UTF-8 bytes before adding the required final LF;
- normalize a terminating carriage return to exactly one LF for the wrapper;
- reject NUL, CR inside the value, embedded LF, control characters, function
  or navigation keys, invalid UTF-16 surrogate structure, invalid UTF-8,
  overflow, EOF, interruption, or more than one line;
- treat backspace only as deletion of the previous complete Unicode scalar;
- display no character, replacement character, length marker, cursor marker,
  asterisk, or other echo; and
- never place the value in chat, arguments, environment variables, files,
  clipboard, registry, history, logs, exceptions, comments, handoffs, custom
  process titles, stdout, stderr, or console prompts.

The controller creates one bounded one-shot binary reader over the exact
UTF-8 line and passes that reader as `stdin` to the wrapper. The reader permits
the wrapper's one bounded read, then returns EOF. It cannot be rewound, reused,
logged, inspected through `repr`, or exposed through an exception. The public
characterization ID is passed separately.

Mutable UTF-16, UTF-8, and wrapper-input buffers receive one best-effort
overwrite in every ordinary and exceptional terminal path and become
unreachable immediately afterward. CPython can create immutable temporary
objects while decoding and validating text; this contract makes no impossible
claim that those objects are deterministically zeroized. The controller
process exit is the outer bounded-memory lifetime. Any implementation that
claims complete Python-object or operating-system memory zeroization is
nonconforming.

## In-Process Wrapper And Result Routing

The controller imports the exact accepted characterizer by its fixed
repository path and invokes `run_consumed_characterization` at most once in the
same process. It supplies:

- the fresh public characterization ID;
- the one-shot private-line reader above; and
- one bounded in-memory stdout sink limited to `4096` bytes.

No private value is passed through a controller command argument, environment,
file, named pipe, registry value, clipboard, or second process. The unchanged
wrapper remains responsible for private-path validation and clearing its own
owned mutable buffer.

On wrapper return `0`, the controller must validate the captured bytes using
the unchanged 33-field parser, require zero wrapper stderr bytes, and write the
exact captured canonical bytes once to controller stdout followed by one
flush. It adds no field, envelope, prefix, suffix, prompt, or alternate
artifact. On any nonzero wrapper return, invalid/partial output, controller
stdout failure, console-state uncertainty, or controller cleanup uncertainty,
it emits no canonical result.

The existing nine-value `controller_wrapper_terminal_phase` vocabulary and
return-code mapping remain unchanged. A controller failure before wrapper entry
or an unclassifiable controller terminal state maps only to existing
`unknown`; it does not create a tenth value. The controller exit code is the
unchanged wrapper code when a wrapper code is known, `0` only after exact
result routing, and `2` for controller-owned unknown failure.

The fixed readiness line is console-device UI, not result stdout, stderr, a
receipt, or a terminal category. No second result schema or durable private
artifact exists. Any external capture of the canonical stdout packet is
public-safe transport owned by the separately authorized execution role and
must preserve the exact original bytes.

## Closed Lifecycle And Precedence

Apply first match:

1. frozen artifact, issue, bootstrap-source, or public launch binding rejection ->
   stop before readiness, consumption, private input, wrapper entry, or target;
2. terminal-host or controller console, no-echo primitive, or launch bootstrap
   not exact -> stop before readiness or consumption;
3. cancellation or timeout before durable consumption -> no private input,
   controller, wrapper, or target; the one bootstrap invocation is spent and a
   fresh task reconciles whether a new owner decision is required;
4. durable consumption absent, mismatched, collided, edited, unreadable, or
   ambiguous -> no private input, wrapper, or target; conservatively retire any
   possibly consumed decision;
5. post-consumption confirmation, launch-image ingress, controller creation,
   controller runtime/self-binding, target-path ingress, console stability, or
   mutable-buffer cleanup failure -> existing terminal phase `unknown`, no
   wrapper result, permanent nonreuse;
6. wrapper returns one exact nonzero code -> map through the accepted terminal
   table, discard bounded output, restore/verify console state, permanent
   nonreuse;
7. wrapper returns `0` but result validation, controller stdout write/flush,
   console verification, or cleanup is not exact -> `unknown`, no accepted
   result, permanent nonreuse; and
8. wrapper returns `0`, unchanged result is canonical and complete, controller
   stdout is exact, console mode is unchanged, mutable owned buffers received
   their best-effort clear attempt, and all process/cleanup facts are exact ->
   unchanged canonical result plus existing `wrapper_complete` handoff.

Every post-consumption path is terminal and nonreusable. No retry, relaunch,
replacement ID, fallback runtime, alternate ingress, result repair, evidence
reconstruction, or automatic continuation is authorized. An unknown or
missing terminal handoff still retires the attempt.

## Operation-Free Test Contract

The focused test imports the controller with fake console, clock, binding,
wrapper, output, and cleanup adapters and inspects the fixed bootstrap source
without executing it. It must not access a real console, private path, GitHub,
network, registry, private file metadata, or native process API and must not
start any process or thread.

Required tests prove:

1. exact bootstrap, runtime, and public binding admission and each first-failure
   rejection;
2. exact Windows PowerShell 5.1 `Arguments` construction from the seven admitted
   ASCII tokens, including both closed identifier regexes, the `512`-byte
   ceiling, one-space joining, and rejection of private-path, quotation,
   whitespace, option-injection, command, timeout, cwd, environment, adapter,
   fallback, duplicate, reordered, missing, and extra arguments;
3. launch readiness requires one existing PowerShell console, documented
   `[Console]::KeyAvailable` and `[Console]::ReadKey($true)`,
   `UseShellExecute=false`, the exact public `Arguments` string, zero private
   reads, and zero child processes before consumption;
4. controller readiness requires a real-console projection, empty pending
   input, callable `kbhit/getwch`, mode snapshot, wrapper signature, exact
   self-runtime binding, and one consumed launch-image read owned by the
   bootstrap but zero prior controller private reads;
5. no controller code calls PATH discovery, `py.exe`, `subprocess`, shell,
   `os.system`, `os.startfile`, broker, service, task scheduler, network,
   clipboard, registry, file-write, or process-title APIs;
6. bootstrap source permits only one no-echo launch-image read and one
   `ProcessStartInfo` start with `UseShellExecute=false`; source inspection
   rejects command interpolation, shell execute, PATH lookup, a second start,
   output rewriting, a helper process/thread, and any durable private sink;
7. pre-consumption cancel, timeout, non-Enter, and stale-input routes never call
   either private reader, create the controller, or invoke the wrapper;
8. post-consumption cancel, timeout, malformed UTF-16, invalid UTF-8, control,
   function-key, overflow, multi-line, nonabsolute, wrong-basename, and console
   drift routes call no wrapper and select only `unknown`;
9. bootstrap `ReadKey($true)` and controller `getwch` input are never echoed and fake
   output never receives private data
   or a private-length projection;
10. exact Unicode scalar and backspace handling, one LF projection, one
   one-shot wrapper read, and EOF thereafter;
11. every mutable owned buffer receives one best-effort clear attempt without a
   complete-zeroization assertion;
12. the wrapper is invoked zero or one time, always in the controller process,
     and never retried;
13. wrapper returns `2`, `10` through `16`, and `0` retain the accepted phase
     mapping, including cleanup override and pairwise conflicts;
14. return `0` routes byte-identical 33-field canonical output with one stdout
     write and flush, while all failure routes produce no canonical result;
15. the 18 authority fields remain present, ordered, boolean, and all false;
16. console mode is unchanged on success and every injected ordinary failure;
     any unconfirmed restoration maps to `unknown`;
17. topology remains one pre-existing terminal host with one in-process
     bootstrap, one controller, zero or one fixed target, and zero target
     descendants, with no helper process or input thread; and
18. issue #769 receives no comment and no test creates durable residue.

The accepted current characterizer focused suite must remain unchanged and
pass. Static inspection must prove the controller contains no process-creation
API; the sole target `CreateProcessW` remains in the accepted characterizer.

## Acceptance And Validation

Independent Codex E accepts this contract only if it confirms:

- every frozen byte and GitHub binding is exact;
- the in-process PowerShell bootstrap is the sole pre-controller launch-ingress
  mechanism, creates no process slot of its own, and requires no PATH, extra
  launcher, helper process, shell fallback, alternate runtime, or undocumented
  Codex capability;
- the current Windows PowerShell 5.1 host needs only `Arguments`, not the absent
  `ArgumentList`; its two variable tokens match the closed regexes, the exact
  one-space string is no more than `512` bytes, and the private image remains
  only in `FileName`;
- launch-ingress readiness precedes durable consumption, and durable
  consumption precedes both the private launch-image read and controller target
  path read;
- trusted-owner confirmation does not replace the durable issue #795 comment
  or fresh E readback;
- the private line reaches only the in-process wrapper one-shot reader;
- console input is documented no-echo input and console state is unchanged or
  exactly restored;
- the bootstrap, controller, and one operation-free focused test add exactly
  three future implementation paths and no execution lane beyond the missing
  parent boundary;
- the existing wrapper, algorithm, target process, schemas, result categories,
  terminal vocabulary, and all-false authority object remain unchanged;
- every post-consumption outcome is terminal and nonreusable;
- tests are operation-free and cover every state above; and
- no prerequisite is misrepresented as preflight, Observation 1, R0/R1-R8,
  Stage 4, deployment, assurance, or readiness authority.

Contract validation requires:

```powershell
git diff --check
py -B tools/check_agent_docs.py
Write-Output 'docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md' | py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
Write-Output 'docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md' | py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py -q -p no:cacheprovider
```

Also require exact SHA-256 recomputation for every frozen artifact; issue
#795/#780/#746 and PR #797 revalidation; issue #769 open with zero comments;
open-PR/WIP reconciliation; matching characterizer/controller/preflight task
process count `0`; the pre-existing E review report preserved byte-for-byte;
only this contract changed by Codex B; and generated residue count `0`.

## Authority And Nonclaims

This contract creates no current implementation, controller, private-path,
authority-consumption, characterizer, process, result-publication, preflight,
observation, release, registry, installation, package, network, claim,
command, task, dispatch, canary, R1-R8, Stage-4, submission, merge, deployment,
assurance, or readiness authority.

Independent contract acceptance may make only a separate owner implementation
decision eligible for the exact three new files. Accepted implementation and
integration may make a separate fresh execution decision eligible. Neither
decision is created here.

Even an accepted characterization result is diagnostic evidence only. It is
not the R0 direct-interpreter preflight, Observation 1 or 2, a release receipt,
R0 acceptance, R1 eligibility, rung evidence, Stage-4 evidence, security or
privacy assurance, or live readiness. Only a later Codex A strategy
reconciliation may use independently accepted result evidence.

## Next Independent Review Prompt

Use the Mythic Edge agent constitution and `$mythic-edge-workflow`.

Act as Codex E: Independent R0 Identity Characterizer Secure-Ingress Successor
Contract Reviewer.

Repository: `Tahjali11/Mythic-Edge`

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/795>

Review only
`docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md`
at the exact SHA-256 reported by the Codex B handoff. Recompute every frozen
binding and review `ME-RP-795-INGRESS-A-001` and
`ME-RP-795-INGRESS-E-001` and `ME-RP-795-INGRESS-E-002` from first principles.

Confirm the exact repository-owned PowerShell bootstrap executes in the
pre-existing terminal process, proves its documented no-echo input and direct
`ProcessStartInfo` capability before consumption, and creates no process of its
own. Confirm the owner completes and reads back the existing issue #795 durable
transition before pressing Enter or supplying any private character. Confirm
the bootstrap then reads one private launch image through bounded
`[Console]::KeyAvailable` and `[Console]::ReadKey($true)`, uses only
`UseShellExecute=false`, starts the exact accepted CPython controller once with
public fixed arguments, and has no PATH,
extra launcher, helper, shell fallback, alternate runtime, or undocumented
Codex capability.

Confirm Windows PowerShell 5.1 uses only the exact `Arguments` string, with the
seven one-space-separated ASCII tokens, closed characterization-ID and issue
#795 owner-comment URL regexes, `512`-byte ceiling, and no general quoting or
escaping path. Confirm the private launch image remains exclusively in
`FileName`, and the controller rejects any `sys.argv` mismatch.

Confirm the controller calls the accepted wrapper once in-process, permits at
most one unchanged fixed target and zero target descendants, preserves the
unchanged 33-field result, 18 false authorities, nine terminal phases, target
algorithm, process behavior, and all historical evidence, and creates no
second schema, durable private artifact, helper, retry, fallback, or parallel
lane. Confirm console-state verification/restoration, bounded memory lifetime,
honest best-effort clearing without a complete-zeroization claim, operation-
free test closure, issue #769 protection, and all false authority fields.

Reject any hidden or second launch helper, private path in bootstrap or
controller arguments or durable output, bootstrap/controller network or GitHub
access, independent-consumption claim based only on Enter, wrapper or result
change, relaxed identity, process/thread/file beyond the exact three-path and
one-controller topology, or preflight/Observation/R1-R8/Stage-4/readiness
claim.

Do not implement, execute, access a private path, consume authority, generate a
fresh ID, mutate GitHub or release state, or route to Codex D. If exact, create
one contract-test report, set
`ME-RP-795-INGRESS-A-001=fixed_confirmed_contract_only` and
`ME-RP-795-INGRESS-E-001=fixed_confirmed_contract_only` and
`ME-RP-795-INGRESS-E-002=fixed_confirmed_contract_only`, and report whether a
separate owner three-file Codex C implementation decision is eligible.

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
  proposed_nonprecedential_adrs_read:
    - "docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md"
  protected_surfaces:
    - "private direct-interpreter path and runtime identity"
    - "single-use authority consumption and historical nonreuse"
    - "controller, target-process, console, output, and cleanup topology"
    - "issue #769 zero-comment boundary"
    - "R0, Observation 1, R1-R8, Stage 4, deployment, and readiness authority"
  authority_conflicts_found: true
  authority_conflict_notes: "The accepted contracts presumed but prohibited adding their missing parent executor. The owner-selected successor supersedes only that prohibition. E then proved that a controller cannot launch itself from a private image; this revision adds one in-process terminal bootstrap, one controller, and one operation-free test while preserving every other boundary."
  stop_conditions:
    - "Any frozen repository, review, issue, PR, runtime, or historical-attempt drift."
    - "Any need for PATH, py.exe, a shell fallback, alternate runtime, a launch mechanism beyond the exact in-process bootstrap, helper process, input thread, or undocumented Codex input capability."
    - "Any private path in controller arguments, environment, files, clipboard, history, logs, comments, handoffs, or durable output."
    - "Any implementation path beyond the exact launch bootstrap, controller, and focused test."
    - "Any wrapper, identity algorithm, result schema, terminal vocabulary, target-process, or authority change."
    - "Any implementation, execution, authority consumption, fresh ID, GitHub mutation, issue #769 touch, preflight, observation, or stage advancement in this B thread."
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Narrow Windows PowerShell 5.1 Public-Argument Transport Corrector"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/795"
  parent: "https://github.com/Tahjali11/Mythic-Edge/issues/780"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_coordination_surface: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md"
  contract_artifact: "docs/contracts/role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md"
  source_findings:
    ME-RP-795-INGRESS-A-001: "contract_correction_preserved_independent_re_review_pending"
    ME-RP-795-INGRESS-E-001: "fixed_confirmed_contract_only"
    ME-RP-795-INGRESS-E-002: "contract_correction_authored_independent_re_review_pending"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/r0-identity-characterizer-secure-ingress-contract-795"
  base_commit: "4a126a9f0ccb9234f08f5d706dbba49f31a3c176"
  predecessor_contract_sha256: "436811c649bc57d74c995dd3e9a1398d01d37e880b45a3a8624c0bc9ca41162d"
  blocking_review_sha256: "f6d81ea9af445802c1132488f04ce54aaceb503e80bee826d222471b9e0dd760"
  controller_runtime_binding_sha256: "2315511a22881182565b4e8f0dd3764c79982c0287e573c562b1bd1f6f902333"
  bootstrap_invocation_limit: 1
  controller_execution_limit: 1
  wrapper_invocation_limit: 1
  target_process_limit: 1
  target_descendant_process_limit: 0
  result_schema_changed: false
  terminal_vocabulary_changed: false
  new_execution_lane_created: false
  future_implementation_scope:
    - "tools/start_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.ps1"
    - "tools/run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py"
    - "tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py"
  owner_implementation_decision_eligible: false
  implementation_authorized: false
  private_path_accessed: false
  authority_consumed: false
  fresh_id_created: false
  characterizer_authorized: false
  preflight_authorized: false
  observation_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  validation:
    - "git diff checks passed"
    - "agent-doc validation passed with 0 errors and 0 warnings"
    - "path-scoped protected-surface and secret/private-marker scans passed with forbidden 0 and warnings 0"
    - "unchanged identity-characterizer focused suite passed: 187 tests"
    - "frozen bindings and issue states revalidated; matching task processes 0; generated residue 0"
  stop_conditions:
    - "Any requirement for a launch mechanism beyond the exact in-process bootstrap, helper process, PATH, py.exe, shell fallback, alternate runtime, input thread, or undocumented Codex capability."
    - "Any private path exposure or durable private artifact."
    - "Any change to accepted wrapper, algorithm, result, target process, or authority."
    - "Any implementation or execution before independent Codex E acceptance and separate owner decisions."
  next_recommended_role: "Codex E: independent secure-ingress successor contract reviewer"
```
