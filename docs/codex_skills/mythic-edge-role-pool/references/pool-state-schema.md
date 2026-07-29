# Pool State And Result Contract

This reference describes the strict v3 documents enforced by
`scripts/check_pool_plan.py`. The validator rejects every missing or unknown
field. It performs no network access and no mutation.

## Contents

- [Evidence classes](#evidence-classes)
- [Plan contract](#plan-contract)
- [Inventory and repository identity](#inventory-and-repository-identity)
- [Lane, WIP, and role evidence](#lane-wip-and-role-evidence)
- [Claims, leases, and runtime](#claims-leases-and-runtime)
- [Candidates and compatibility](#candidates-and-compatibility)
- [Result and handoff contract](#result-and-handoff-contract)
- [Recovery journal](#recovery-journal)
- [Executable fixtures and validation](#executable-fixtures-and-validation)

## Evidence Classes

- **Deterministic:** strict keys, types, bounds, canonical IDs, state names,
  timestamps, digests, role bindings, capacity, WIP assignments, pair coverage,
  result bindings, and fallback fields.
- **Runtime-observable:** whether an inventory is actually complete, a GitHub
  receipt is authoritative, a server-ordered claim really won, a worktree is
  physically registered as recorded, or a launch receipt really identifies the
  stated isolated agent and packet.
- **Behavioral:** whether a fresh agent obeys the untrusted-evidence boundary.
  Unit tests prepare that boundary but do not replace the canary.

Never treat a structurally valid document as proof that its runtime receipts
are true. Refresh and verify those receipts on the named authority surface.

The isolated `MRP-RC-003` Stage-4 experiment uses the separate
`mythic_edge_role_pool_stage4_canary_exception.v1` contract documented in
`references/stage4-canary-exception.md`. It is never a plan or result under this
schema and cannot authorize normal dispatch, claims, reservations, or writes.
Its execution component must use the separately documented
`mythic_edge_role_pool_external_isolation_broker.v1` boundary in
`references/external-isolation-broker.md`. The current v3 validators implement
the broker launcher projection, but the preparation package remains unreviewed,
uninstalled, and unprovisioned, so the path remains non-live.

Stage 3 likewise uses the separate
`mythic_edge_role_pool_stage3_behavioral_planning.v1` contract documented in
`references/stage3-behavioral-planning.md`. It validates a fixed synthetic
three-repository/three-lane same-role compatibility projection and fail-closed
exclusions with zero Role Pool effects. It never emits an inspect, preclaim, or
prelaunch v3 document, creates no authority, and leaves agent behavior to
Stage 4. `scripts/check_pool_plan.py` intentionally remains unchanged and must
reject a Stage-3 observation as a v3 plan.

## Plan Contract

Use `schema_version: mythic_edge_role_pool_plan.v3`. The top-level fields are:

| Field | Requirement |
| --- | --- |
| `phase` | `inspect`, `preclaim`, or `prelaunch` |
| `action` | Exact mode, pooled role, operation, provenance, and action allowlist |
| `inventory` | Complete fresh repository discovery and active-state snapshot |
| `runtime_preflight` | `null` for inspect; model preference plus exact context/packet preflight for dispatch |
| `active_waves` | At most two total waves after adding the proposal |
| `proposed_wave` | `null` for inspect; one non-empty wave for dispatch |
| `queued_lanes` | Complete unselected target-role lane state |
| `candidate_inventory` | Every selected and queued target-role candidate |
| `compatibility` | Exactly one row for every required lane pair |
| `fallback` | Enforced old-workflow behavior |

Phase rules:

- `inspect` carries no claim, reservation, launch preflight, or proposed wave.
- `preclaim` requires a complete dispatch plan and launch preflight but carries
  no claim or reservation.
- `prelaunch` requires a winning refreshed claim, matching reservations, at
  least 15 minutes of launch lease, and no launched runtime yet.

The leading named selectors `Mythic-Edge-Role-Pool: Inspect` and
`Mythic-Edge-Role-Pool: Dispatch` (or the `$mythic-edge-role-pool` aliases)
deterministically select the plan mode. A dispatch selector is not standalone
authority: the same exact current request must still name exactly one pooled
role and every required authority clause. A bare or incomplete dispatch
selector cannot produce a valid `preclaim` document and permits no side effect.
Quoted examples, questions, conditions, negations, mixed inspect/dispatch text,
and selectors appearing after other prose normalize to inspect.

The compact personal grammar is:

```text
Mythic Edge Role Pool: <Inspect|Dispatch>: <A|B|C|D|E|F|G> <repository>[; <repository>][; <repository>]
```

The leading mode supplies explicit mode intent. The role letter expands to
`Codex <letter>`, and one-to-three repository tokens canonicalize into the exact
authorized repository set. `C` is recognized for fail-closed dedicated-task
routing but remains invalid in a pooled plan. Zero repositories is incomplete;
one or two are the entire scope and are never backfilled from unlisted
repositories. Candidate selection operates only inside the canonical set.
Ownerless short aliases receive owner `tahjali11` and prefix `mythic-edge-`;
`fable-engine` therefore becomes `tahjali11/mythic-edge-fable-engine`.
Each exact named repository receives the same request-bounded full read grant
whether its visibility is public or private. No separate private-read clause is
required. A legacy private-read clause is redundant and cannot add an unlisted
repository.

The complete non-compact form must contain one standalone semicolon-delimited
`authorize repository=owner/repository` binding for every and only inventory
repository; the compact list supplies the equivalent exact set. Quoted,
negated, conditional, example, or question-form repository text grants no read
authority. Current-user WIP exceptions, runtime overrides, a `main` draft-PR
target, and exceptional or mutating actions still use separate strict
affirmative clauses.

The personal defaults are owner `tahjali11` and repository prefix
`mythic-edge-`. In the repository binding and compact repository list,
ownerless `security`, `fable-engine`, and `corpus` canonicalize to their
`tahjali11/mythic-edge-*` identities. Root slug `mythic-edge`, already-prefixed
slugs, and explicit `other-owner/repository` identities remain unchanged.
Canonicalization occurs before the exact request-to-inventory set comparison.
All persisted identities and every lane, WIP, claim, evidence, result, and
receipt binding still require the full canonical `owner/repository` value.
Spaced names, URLs, filesystem paths, `.git` suffixes, and `auto` are invalid.

Only A, B, D, E, F, and G may be pooled. F may commit, push, and create or
update a draft PR only when those exact actions are authorized. Pooled G uses
`g_readiness_only`; merge and closeout actions do not exist in this schema.

Exact action maxima are: inspect = `read_authorized_metadata`; A adds scheduling,
routing, local-artifact, and `issue_write`; B/D/E/G add only scheduling,
routing, and local-artifact; F adds scheduling, routing, local-artifact,
`git_commit`, `git_push`, and `draft_pr_write`. A has no repository write path;
B writes only its contract; D writes only exact fix files; E/F/G have no
implementation write path and observe exactly the reviewed files.

## Inventory And Repository Identity

Canonical repository IDs are lowercase `owner/repository`. URLs, `.git`
suffixes, ownerless names, case aliases, and path aliases are invalid. Each
repository records its exact HTTPS remote, visibility, authority, read scope,
allowed references, no-echo rule, fresh status time, active slot, and active
lane IDs.

The union of repositories reported by all discovery sources must exactly equal
the repository inventory. Every active, proposed, and queued lane must appear
in that inventory. Dispatch-safe inventory is complete, no more than 15 minutes
old, and has no unresolved source.

Naming a repository establishes an `authorized_full` permission ceiling for
its public or private Git/GitHub content. A plan may narrow actual consumption
to `metadata_only`, which cannot support issue, PR, handoff, contract, comment,
or artifact content. `authorized_full` requires
`read_authority_ref: user:current-task/repository/<owner/repository>` and exact
`allowed_read_only_references`; the latter is an auditable lane-consumption
manifest, not another user grant. `private_content_authorized` is true exactly
when a private repository is consumed as `authorized_full` and is otherwise
false. Every repository requires `no_echo_required: true`.

## Lane, WIP, And Role Evidence

Every lane binds its canonical lane ID, repository, issue, role, base and target
branches, physical worktree evidence, WIP assignment, scope, evidence sources,
role evidence, reservation, and runtime.

One lane is the repository `slot_owner`. Every additional active or proposed
lane requires a complete, canonical ADR-0008 exception with its repository,
active lane, blocked item, reason, allowed scope, expiration condition and
time, authorizer, and durable record. A queued lane uses only `kind: queued`.

Pooled scope fails closed for credentials or secrets, machine-local or external
private evidence outside the exact named repository, production, destructive
behavior, every protected surface, or an external write not allowed by the
current invocation. Merely reading a named private repository is not a
protected effect. Protected work is routed to the old one-issue workflow even
when a contract reference is present.

External evidence records only metadata: kind, exact reference, author,
observation time, SHA-256, bound head, trust annotation,
`handling: untrusted_data_only`, and `grants_authority: false`. Raw content is
not a plan field.

Role evidence is tagged and strict:

| Role | Required binding |
| --- | --- |
| A | Planning need, scope, risk, inspection order, bounded issue-write flag |
| B | Issue, valid A handoff, contract path |
| D | Exact issue, concrete finding IDs and source, exact fix boundary |
| E | Issue, contract, implementation handoff, diff, head, files, scope digest |
| F | Exact issue, typed accepted E review, exact head/files, zero blockers, all-passed head/digest-bound validation rows, base, approval |
| G | Exact issue and PR, review/head/base, fresh checks, findings, readiness-only authority |

## Claims, Leases, And Runtime

A wave claim uses UUID claim and coordinator IDs, one globally unique live wave
slot, exact lane IDs, the plan digest, globally unique server receipt/comment,
server timestamp, verification time, expiry, and refreshed competing claims.
Only unexpired `reserved` rows compete; `released`, `lost`, `failed`, and expired
rows cannot win. The deterministic winner is the lowest tuple of
`server_created_at`, `server_comment_id`, and `claim_id` for both the slot and
every lane.

Every lane reservation matches the winning claim and uses scheduling authority
only. Implementation, execution, publication, and merge authorization remain
false. Claims and reservations last no more than 24 hours and need at least 15
minutes remaining before launch.

The direct launcher identity `codex:exec-single-start/v2` is retained only for
offline deterministic tests and preflight/argument preparation.
`scripts/codex_launcher_contract.py` still resolves the newest contained
compatible `codex.exe`, binds its path/hash/length/version and exact flags, and
builds the minimal environment. Its private deterministic seam re-hashes exact
inputs, uses `shell=False`, and exercises a process-local one-start guard, while
the public direct entry point refuses process creation. Those are useful
regression controls, but a direct `subprocess.Popen` process is not created by the external
isolation provider. Every direct-Popen receipt is therefore non-live and must
record `production_eligible=false`.

Use pooled/Stage-4 launcher identity `codex:broker-single-start/v1` and backend
`windows_isolation_broker` only after the implementation candidate for the
strict contract in `references/external-isolation-broker.md` is independently
reviewed, installed under separate authority, and proven on the current service
boundary. The
coordinator prepares the exact preflight, argument array, packet, child script,
schema, environment, workspace, and writable-scope bindings, then submits one
canonical request. It must not call `Popen`, own a kill-capable process handle,
or perform child wait, timeout termination, stream drain, or cleanup. The broker
atomically consumes machine-exclusive start authority, creates the child inside
the final boundary, and owns the complete process lifecycle.

The broker path requires the exact chain:

- `mythic_edge_role_pool_broker_launch_request.v1`;
- `mythic_edge_role_pool_broker_start_reservation.v1`;
- `mythic_edge_role_pool_broker_boundary_ready_receipt.v1`;
- `mythic_edge_role_pool_broker_start_receipt.v1`; and
- `mythic_edge_role_pool_broker_terminal_receipt.v1`, or the fixed abort receipt
  for a failed partial start.

Each live readback projects the broker backend and launcher, exact preflight and
executable, packet hash/length, and start/terminal receipt digests. Start proves
one process was created and resumed inside the independently observed boundary,
not that it remains running. A running state needs a fresh broker/verifier
status observation. Terminal proves the same process ended and cannot
substitute for start evidence.

The existing `mythic_edge_role_pool_launcher_receipt_sidecars.v1`,
`mythic_edge_role_pool_single_start_receipt.v2`,
`mythic_edge_role_pool_external_isolation.v3`, and
`mythic_edge_role_pool_external_os_isolation.v2` remain migration/offline
contracts. V3 isolation evidence is observed before an unrelated direct
process creation and cannot prove placement of that later process. Synthetic
sidecars continue to use `none`/null attestation markers and the exact
`internal_test_backend` / `false` pair. Offline fixtures must use the explicitly
named `offline_synthetic_fixture` mode; their success is non-live and grants no
claim or launch authority.

The current validators reject `subprocess_popen` / `true`, and the public direct
launcher refuses process creation after legacy validation. They also reject a
broker claim represented by the old single-start receipt. The implementation
candidate adds strict broker reservation/boundary-ready/start/terminal/abort
validation and updates plan, result, launcher-sidecar, runtime, and recovery
validation together. Until that implementation passes independent review and
the successor services are separately authorized, installed, and observed,
all preclaim, prelaunch, active runtime, result, Stage-4, and live validation
remains fail-closed.

Lease expiry removes launch authority. It does not erase a fresh observed
running runtime. Every launched lane separately records agent identity, runtime
state, fresh observation, unique launch receipt and digest, preferred
model/effort, the nullable values actually passed on the CLI, launcher argument
mode, complete launcher-preflight digest, selected executable binding, isolated
context, `fork_turns: none`, launcher, and exact
isolated-packet digest. Effective model/effort values and their readback receipt
are optional telemetry. The result binds the required non-model launch record to
the preflight, launch journal, and planned lane packet; independent active-wave
discovery binds it again.

Preferred values are `gpt-5.6-sol` and `max`. Request both only when the bundled
model catalog advertises `gpt-5.6-sol`; otherwise omit both preference arguments
and record both requested fields as null with mode `platform_default`. The full
validated launcher preflight and its selected executable are frozen from
preclaim through prelaunch. A non-default preferred value requires the exact
standalone clause `authorize runtime override model=<model>
reasoning_effort=<effort>`, current-user reference, request digest, grant time,
and nonempty reason. Every override field is frozen through prelaunch. Missing
control/readback or a reported effective-value difference does not fail the
plan.

Worktree evidence includes entered path, canonical resolved path, registered
Git top-level, common directory, canonical repository, branch, head, and fresh
verification time. Device prefixes, relative paths, duplicate branches, and
physical aliases fail closed.

## Candidates And Compatibility

Candidate selection is deterministic:

1. twice-deferred eligible lanes, oldest first;
2. returned eligible lanes with concrete findings, oldest first;
3. remaining eligible lanes, oldest first;
4. canonical lane ID as the tie-breaker.

Every unselected returned or twice-deferred lane requires a substantive
exclusion. Selected candidates must exactly equal proposed lanes.
For every phase, including inspect, the complete candidate inventory must
exactly equal the independently collected discovery sidecar. Inspect candidates
remain unselected because inspect has no proposed launch wave.

Compatibility covers every proposed/proposed and proposed/active pair exactly
once. `safe_to_run_concurrently` requires no dependency, shared write path,
contract, protected surface, external state, or invalidation risk.
Repository-relative write paths and unnamespaced contract-file surfaces bound
to those paths are keyed by repository, so identical local paths in different
repositories do not collide. Namespaced schema/contract identifiers, ambiguous
surfaces, protected surfaces, and external state remain global conflicts.
`concurrent_until_integration_then_serialize` requires exact order,
invalidation triggers, refresh barrier, and refresh bindings.

## Result And Handoff Contract

Use `schema_version: mythic_edge_role_pool_result.v3`. A result binds the exact
plan digest, wave, coordinator, role, expected lanes, one typed lane result per
lane, complete event journal, and fallback record.

Every lane result includes claim identity, launch and result status, next role,
immutable result reference and digest, role-tagged result, complete handoff,
release receipt, findings, and exact external-action receipts.

One central wave claim legitimately has one receipt shared by every lane's
`claim` journal event. That receipt may repeat only across `claim` events in the
same result wave and must equal the winning prelaunch claim. Reservation,
launch, role-artifact, result, route, release, and every other receipt remain
lane-unique and cannot evidence two logical side effects.

Role-tagged results require:

| Role | Result-specific proof |
| --- | --- |
| A | Problem representation and issue receipt |
| B | Contract reference and digest |
| D | Addressed finding IDs and validation references |
| E | Exact reviewed head/files, verdict, blocker count, review digest |
| F | Typed accepted review, carried prepublication validation rows, reviewed/staged files, commit, pushed head, draft PR, base |
| G | Exact PR/head/base/check/review/scope readiness with `no_integration_mutation: true` |

F staged files equal reviewed files; pushed head equals the created commit; the
accepted reviewed head, files, and base bind back to prelaunch evidence. A
separate outcome readback binds F commit/PR head, parent, base, state, and exact
changed files; a new draft may still have pending checks and review. Pooled G
contains no integration action. Accepted E with zero findings routes to F;
changes-required E with complete concrete findings routes to D. Incomplete E
never routes to F or G. A G `not_ready` verdict triggers exact fallback condition
18 and old-workflow reconciliation instead of a clean completed result.

Validate a result against the exact accepted prelaunch plan, not by itself:

```powershell
py -B scripts\check_pool_plan.py <result.json> --plan <prelaunch-plan.json> --preclaim <preclaim-plan.json> --discovery <discovery.json> --worktrees <worktrees.json>
```

F and G also require `--outcome <outcome-observation.json>`.

## Recovery Journal

Each logical side effect records an `intent` followed by exactly one
`succeeded`, `failed`, or `unknown` outcome using the same idempotency key and
attempt. Outcomes cannot precede intent. A successful key cannot be repeated.
Unknown outcome requires reconciliation and is never automatically retried.

Completed lanes require successful claim, reserve, launch, result, route, and
release entries plus exactly the role-specific external action set. Every
operation is role-scoped, uses unique typed receipt provenance, and must match
the typed result. G permits no integration journal operation. Partial G is
always manual reconciliation.

## Offline Fallback Sidecars

Fallback pickup is not a result summary field. It is a separately produced and
verified three-document bundle with exact, unknown-field-rejecting schemas:

| Schema | Exact required fields |
| --- | --- |
| `mythic_edge_old_workflow_prompt.v1` | `schema_version`, `route_id`, `prompt_ref`, `created_at`, `lane_id`, `repository_id`, `issue`, `role`, `mode`, `fallback_condition`, `source_artifact_ref`, `source_artifact_sha256`, `dispatch_authorized`, `mutation_authorized`, `raw_content_included`, `digest` |
| `mythic_edge_role_pool_fallback_injection.v1` | `schema_version`, `injection_id`, `receipt_ref`, `injected_at`, `status`, `fallback_condition`, `route_id`, `route_receipt_ref`, `lane_id`, `repository_id`, `issue`, `role`, `mode`, `prompt_ref`, `prompt_sha256`, `consumer_id`, `consumer_contract_ref`, `consumer_contract_sha256`, `consumer_ingress_ref`, `consumer_ingress_sha256`, `task_created`, `agent_launched`, `mutation_performed`, `digest` |
| `mythic_edge_old_workflow_pickup.v1` | `schema_version`, `pickup_id`, `receipt_ref`, `picked_up_at`, `pickup_kind`, `pickup_status`, `consumer_id`, `consumer_contract_ref`, `consumer_contract_sha256`, `consumer_ingress_ref`, `consumer_ingress_sha256`, `injection_ref`, `injection_sha256`, `fallback_condition`, `route_id`, `route_receipt_ref`, `lane_id`, `repository_id`, `issue`, `role`, `mode`, `prompt_ref`, `prompt_sha256`, `task_created`, `agent_launched`, `mutation_performed`, `digest` |

Use `one_issue_one_role_old_workflow` as the exact mode. The prompt has no raw
content and grants no dispatch or mutation authority. Injection status is
`succeeded` but creates no task, launches no agent, and performs no mutation.
Pickup is `ingress_acknowledgement` / `accepted_no_launch` and repeats those
false side-effect facts.

The prompt digest binds injection; injection receipt and digest bind pickup.
Route ID, route receipt where present, lane, canonical repository, issue, role,
mode, fallback condition, prompt reference, prompt digest, consumer identity,
consumer contract, and consumer ingress must match exactly across their
applicable documents. Consumer SHA-256 values must match the current
`mythic-edge-workflow/SKILL.md` and
`mythic-edge-workflow/scripts/accept_fallback_prompt.py`. The old-workflow
ingress deterministically derives pickup ID from injection digest plus pickup
timestamp and must emit pickup within five minutes of injection.

Reject duplicate JSON keys before schema validation. All timestamps use exact
UTC whole-second `Z` form. All references use bounded typed ASCII syntax with no
whitespace, control characters, empty path segments, or traversal segments;
the prompt and route receipt references end in the exact bound issue number.
Both producer and verifier receive `--source-artifact` and reproduce its raw
file SHA-256 before accepting the prompt. The source must resolve within the
canonical installed Role Pool skill, and the expected
`skill:mythic-edge-role-pool/...` reference is derived from that path rather
than accepted from the prompt alone.

Validate with the consumer-produced receipt:

```powershell
py -B scripts\check_fallback_pickup.py <fallback-injection.json> --prompt <old-workflow-prompt.json> --pickup <old-workflow-pickup.json> --workflow-skill ..\mythic-edge-workflow\SKILL.md --pickup-producer ..\mythic-edge-workflow\scripts\accept_fallback_prompt.py --source-artifact <exact-source-artifact>
```

Exit `0` means the complete bundle is valid, exit `1` means a strict schema,
digest, provenance, timestamp, or cross-document binding failed, and exit `2`
means an input could not be read or the command line was invalid. Omitting
`--pickup` after a successful injection is semantic exit `1` with
`pickup: required after successful fallback injection`.

## Executable Fixtures And Validation

The canonical executable fixtures are factory functions in
`scripts/pool_test_fixtures.py`; they cover inspect, preclaim, prelaunch,
active runtime, all role results, the old-workflow prompt, and fallback
injection. They also include a positive, explicitly synthetic three-repository,
three-lane Codex B sequence covering inspect, preclaim, prelaunch, all three
pairwise compatibility rows, one wave claim, unique lane reservations, complete
typed results, and exact observation/result bindings. Its repositories grant no
live Analytics, Corpus, or third-repository authority, and its role action set
contains no commit, push, PR, or integration operation.

The deterministic launcher fixtures use only fake executable files, command
runners, and process factories. They cover unavailable or malformed model
catalogs, flag lookalikes, nested-schema and argument tampering, executable
drift, forged child environments, credential-variable stripping, exact receipt
causality, success, process-start failure, post-start cleanup, timeout, output
separation, and a blocked second launch attempt. The independent pickup is intentionally produced by
`mythic-edge-workflow/scripts/accept_fallback_prompt.py`, not by a Role Pool
fixture. The resulting canonical typed-only prompt, injection, and pickup
observation is preserved in `references/fallback-pickup-fixture/` and is
revalidated without reconstruction by the release gate. Tests validate these
objects unchanged, so prose does not maintain a second drifting JSON example.
Synthetic plan and result fixtures are accepted only through the explicit
offline synthetic-fixture validation mode; ordinary validator calls retain
production semantics.
When the canonical fixture producer changes, regenerate all three frozen files
only through `py -B scripts\regenerate_fallback_pickup_fixture.py --replace`;
that command requires the independently hash-bound old-workflow ingress to
create the pickup and strictly validates the bundle before replacement.

Run the complete offline gate:

```powershell
py -B scripts\run_release_tests.py
```

The runner installs `scripts/offline_gate_guard/` in the parent interpreter,
both structural-validation children, and every allowed Python subprocess. This
is a trusted-code regression guard, not a security or isolation boundary. Its
tests prove propagation and exercise common accidental socket, subprocess, and
Python filesystem-mutation paths; they do not prove containment against code
that retains originals, invokes native OS APIs, or uses an uncovered mutation
path. The existing before/after digest snapshot independently requires both
installed skill trees to remain unchanged during the gate.

Step 1 may execute only reviewed, trusted Python validation code. Before any
untrusted executable or script, repository-supplied program, or live behavioral
proof, require a separately provisioned and independently verified external
OS-enforced read-only/no-network isolation boundary. Content-addressed inputs
must be pre-provisioned. Tool subprocesses receive no network; only the
separately identified Codex service channel may carry control-plane transport.
No process-local hook, launcher guard, conversation isolation setting, or
application-level read-only flag satisfies this requirement.

For inspect with no active waves, `--discovery` is sufficient. Inspect with an
active wave also requires `--worktrees`; preclaim and prelaunch always require
both sidecars, and prelaunch additionally requires `--preclaim`.

## Trusted-Owner Native V1 Schemas

`scripts/check_pool_plan.py` also owns inert, offline validators for the closed
`trusted_owner_native` interfaces. They cover:

- repository registry entries, approved command templates, and registry
  transitions;
- one-to-three-lane Safe or Automatic requests, results, handoffs, and
  false-authority flags;
- immutable claim events, GitHub readback observations, complete snapshots,
  resolution events, deterministic replay, and non-reusable unknown states;
- public-safe worktree observations and one-use native task
  request/receipt packets;
- typed process-local host and exact `codex:native-task-create/v1` capability
  observations that never enter a serialized packet or self-digest;
- Safe and Automatic state routing, ordered terminal selection, external
  isolation escalation, and the Codex F draft-PR-only boundary; and
- the `R0` through `R8` append-only release record chain.

All objects are strict ordered JSON objects with typed scalars and exact
self-digests. Duplicate or unknown fields, ambiguous identities, stale
bindings, wildcard scope, unsupported transitions, and authority widening
fail closed. Command resolution returns a typed, nonexecuting projection and
never searches `PATH`, invokes a shell, or creates a process.

The 34 managed migration rows and 16 generated-cache rows are disjoint.
Generated rows are evidence about the observed installation only and are never
canonical source. The managed-tree walker rejects missing, extra, nonordinary,
symlink, junction, and reparse-point representations before accepting a
manifest.

The initial execution profile is Windows-first. A mutating or advancing path
passes preflight only when the runtime observation is exactly
`os.name == "nt"` and `sys.platform == "win32"` and the exact native task
primitive satisfies every closed capability guarantee. A Mac remote-controls
a process running on Windows as Windows-hosted execution; native Mac dispatch
is deferred. Missing, conflicting, unsupported, or incompatible observations
select priority-1 `blocked_request_or_packet_invalid` before claim, worktree,
task, command, installer staging, or release mutation, with no weaker fallback.
Offline parsing, schema checks, source/install `--check`, and pure-function
tests remain platform-neutral, read-only, and non-authorizing.

The production registry and release-state files are intentionally absent.
Without those reviewed artifacts and a live first-party task capability,
validation remains synthetic-only and `trusted_owner_native_profile_ready`
remains false.
