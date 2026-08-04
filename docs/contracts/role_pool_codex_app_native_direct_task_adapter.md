# Role Pool Codex App-Native Direct-Task Adapter Contract

Status: `review_pending`

Risk tier: `high`

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/813

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Predecessor profile issue:
https://github.com/Tahjali11/Mythic-Edge/issues/744

Owner activation:
https://github.com/Tahjali11/Mythic-Edge/issues/813#issuecomment-5175504058

## Findings And Decision

1. PR #812 is merged at
   `c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`, and issue #810 is closed as
   completed. Their direct-interpreter and prelaunch evidence remains accepted
   history and is not rewritten by this contract.
2. The initiating Codex Desktop runtime exposes first-party operations to
   create a user-owned project task, list user-owned tasks, and read one task
   independently by returned identity. The contracted operation identities are
   `codex_app__create_thread`, `codex_app__list_threads`, and
   `codex_app__read_thread`.
3. Presence of those operations supersedes issue #813's earlier
   no-callable-surface finding only for contract authoring. It does not prove
   successful live creation, a stable task identity, exact project or
   worktree readback, terminal behavior, typed output, or reconciliation.
4. The existing `trusted_owner_native_task_request.v1`,
   `trusted_owner_native_task_receipt.v1`, result, handoff, claim, registry,
   worktree, ordinary release-record, Safe/Automatic, F, and 20-outcome
   terminal structures can bind the direct realization without versioning.
5. One companion platform receipt is necessary because the existing task
   receipt intentionally delegates first-party response evidence through
   `platform_receipt_ref` and `platform_receipt_sha256`. One same-file R0
   rebaseline line type is also mechanically necessary because the immutable
   release record cannot change its current profile tuple or remain at R0.
   No other public schema, claim family, release path, lifecycle matrix,
   terminal status, or digest family is added.
6. Exact field-level project and worktree confirmation from real task readback
   remains unproven. The contract is sufficient for an inert fake-client
   implementation. Real R2 eligibility remains false unless the then-current
   callable descriptors and one separately authorized observation provide the
   exact facts required below.
7. The current R0 checker reports `blocked_contract_binding_invalid` because
   this candidate changes the profile hash. The old release chain remains
   valid historical evidence but cannot become current successor authority
   until the profile's exact R0 rebaseline event is separately reviewed and
   appended. Registry validation remains exact. Its read-only installed-tree
   observation is also `unsafe_or_unreadable` because the current installed
   skill target is a reparse point. The profile/checker binding requires a
   mechanical two-file update after contract acceptance; the installed-target
   condition remains a separate pre-R2 stop and is not repaired here.
8. `ME-RP-813-E-001` is corrected contract-only by the exact 19-field
   no-rung-advance rebaseline record, closed validator transition, KAT, and
   separately authorized append route in the profile. No release-state bytes
   are changed here.
9. `ME-RP-813-E-002` is corrected contract-only by the exact six-field
   terminal-readback object and KAT below. Codex C owns no unspecified
   serialization choice.

Decision:

`app_native_direct_contract_corrected_re_review_pending`

This decision is prerequisite evidence only. It creates no implementation,
task, observation, installation, dispatch, rung, Stage 4, or readiness
authority.

## Authority And WIP Reconciliation

The exact contract base is Core `origin/main` commit
`c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`, tree
`8c92dce411afa81600e522de0619bae43f73f68f`. PR #812 remains merged at that
commit. Issue #810 is closed as completed. Issue #813 is open, tracker #746 is
open, and protected issue #769 remains open with zero comments.

The owner activation was created at `2026-08-04T06:40:47Z`, was not edited,
and was authored by immutable GitHub actor ID `229644849`. Its exact UTF-8 body
is `1061` bytes with SHA-256
`7d0f97e6606242f6a9dba099ccae70b0d3a1728a26c8b23579b6f632cc1106dc`.
It authorizes only this two-file Codex B contract lane and expires with this
handoff or one proven contractibility blocker.

Open PRs #374 and #391 do not own either changed path. The exact scoped
ADR-0008 `explicit_user_override` is:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #813 direct app-native task contract"
  blocked_active_issue_or_pr:
    - "PR #374"
    - "PR #391"
  allowed_scope:
    - "docs/contracts/trusted_owner_native_role_pool_profile.md"
    - "docs/contracts/role_pool_codex_app_native_direct_task_adapter.md"
  expiration_condition: "Codex B two-file handoff or one proven contractibility blocker"
  authorized_by: "Tahjali11"
  recorded_in: "https://github.com/Tahjali11/Mythic-Edge/issues/813#issuecomment-5175504058"
```

The exception does not transfer to Codex C, E, F, G, task creation, or any
operational lane.

## Module And Truth Ownership

Module: Core-owned direct app-native trusted-owner task adapter.

Internal project area: `Quality / Governance`.

Bridge-code status: `shared_support`.

Truth owners:

- the accepted trusted-owner profile owns public requests, receipts, results,
  handoffs, claims, scheduling, worktrees, registry policy, terminal outcomes,
  release state, and R0-R8 advancement;
- this companion owns only the direct app-operation mapping, private response
  normalization, observation deadline, platform receipt, and fake-client
  contract;
- the current first-party Codex app operation descriptors own their callable
  argument and response shapes;
- the active registry and lane packet own repository, issue, role, operation,
  scope, and effect authority; and
- a later independent Codex E observation owns whether the live app surface
  actually satisfies this contract.

The adapter owns no repository truth, task authority, task transcript,
credential truth, release promotion, security assurance, or readiness claim.

## Public Interface Preservation

The public launcher identity remains:

`codex:native-task-create/v1`

The selected private realization identity is:

`codex:app-native-task-direct/v1`

The following profile interfaces remain unchanged:

- `trusted_owner_native_task_request.v1`;
- `trusted_owner_native_task_receipt.v1`;
- `trusted_owner_native_request.v1`;
- `trusted_owner_native_result.v1` and its existing handoff object;
- every lane, worktree, claim, registry, ordinary release, and authority
  schema, with only the profile-defined same-file R0 rebaseline line type added;
- the 20 profile terminal outcomes; and
- the R0-R8 ladder.

Unknown or duplicate fields remain invalid. The direct realization adds no
caller-controlled host, project, path, model, thinking, timeout, status,
reconciliation, or fallback field to the public task request.

## R0 Current-Profile Binding Prerequisite

The current historical R0 record remains valid only for predecessor profile
`944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`.
It cannot authorize this successor profile. Before any successor-profile R0
observation, R1 comparison, claim, worktree, or app task, the exact
`trusted_owner_native_release_rebaseline_record.v1` defined by the profile
must be the independently accepted release-state tip.

The adapter preclaim must validate the complete mixed release chain, require
`trusted_native_current_rung=R0`, require the rebaseline tip's
`contract_sha256` to equal the independently accepted current profile, and
require its skill-tree, registry, and validator-bundle values to equal the
current independently observed values. Missing, stale, malformed, forked,
duplicate, post-observation, or mismatched rebaseline evidence selects
`blocked_release_state_invalid` before claim or task creation.

The rebaseline is a prerequisite integration event, not part of this adapter
operation. This contract neither creates nor authorizes it. The historical
record remains the immutable first line; the event keeps the rung at R0; and
only observations made after exact rebaseline readback may support R0 to R1.

## Admitted R2 Request

The direct adapter may accept only a request that has already passed every
profile preclaim and prelaunch validator and has one winning claim and one
exact fresh worktree observation.

The adapter contract supports only roles `B` and `E`, with all of these lane
arrays empty:

- `command_ids`;
- `validation_command_ids`;
- `mutation_scope`; and
- `expected_artifact_paths`.

The registry entry must have
`repository_code_execution_policy=forbidden`, an empty
`maximum_mutation_scope`, and exact read authority for the requested scope.
The first future R2 observation is further restricted to one Safe-mode E lane
in one fresh worktree. B support is inert contract coverage and is not part of
that first observation.

The current Core registry's A-only, offline-validation entry does not satisfy
these R2 conditions. This contract does not amend or activate the registry.

## Fixed Direct Create Mapping

After exact validation, the adapter permits one call equivalent to:

```text
create_thread(
  target={
    type: "project",
    projectId: <exact privately observed saved Mythic Edge project identity>,
    environment={
      type: "worktree",
      startingState={
        type: "branch",
        branchName: <exact reviewed base_ref>
      }
    }
  },
  prompt=<exact canonical initial prompt>
)
```

The first R2 call omits `model` and `thinking`. No accepted owner preference is
bound for either field, and neither field is authority. Adding either field
requires a reviewed contract revision or exact pre-dispatch owner binding.

The project identity comes from one reviewed private project observation. Its
raw value remains transient. The environment is always `worktree`; a
projectless target, shared local checkout, existing worktree, alternate
environment, caller-selected target, or target omission is invalid before the
create call.

The starting branch equals lane `base_ref`. The created worktree must resolve
to lane `base_sha`; a moving branch, stale base, or alternate commit rejects
the observation.

Exactly one direct `codex_app__create_thread` call is permitted. These are
forbidden:

- a second create call for any outcome;
- `send_message_to_thread` or another follow-up prompt;
- steering, resume, fork, replacement, pin, archive, title mutation,
  interruption, or cancellation;
- App Server, subagent, shell, `codex exec`, direct-interpreter, broker, SDK,
  service, or alternate task fallback; and
- ambient conversation, inherited coordinator turns, or prompt changes after
  creation.

## Canonical Initial Prompt

Before prompt construction, the adapter derives one fresh public-safe
`app_task_operation_id`. The in-memory canonical binding contains, in order,
`schema_version=trusted_owner_app_native_operation_binding.v1`,
`task_request_sha256`, `request_sha256`, `claim_observation_sha256`,
`lane_packet_sha256`, `repository_id`, `issue_url`, `role`,
`lane_operation_id`, `base_sha`, `project_identity_sha256`, and
`pre_worktree_observation_sha256`, followed by one final LF. Its SHA-256 is
computed before creation. The public ID is literal `app_native_` followed by
the first 32 lowercase hexadecimal characters of that digest.

This ID is unique to the exact direct task attempt without adding a request
field. `lane_operation_id` remains the existing registry operation and keeps
its existing meaning. The derived `app_task_operation_id` is only an
idempotency and reconciliation marker; it is never authority.

The initial prompt is self-contained. It contains no coordinator conversation
or private value. Its exact UTF-8 form is the following fixed line sequence,
with each angle-bracket token replaced by the canonical public value or
one-line canonical JSON object it names, and one final LF:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.
mythic_edge_operation_id: <app_task_operation_id>
mythic_edge_task_request_sha256: <task_request_sha256>
mythic_edge_lane_packet_sha256: <lane_packet_sha256>
Act as Codex <role> for <issue_url>.
Use only the exact lane packet and predecessor packet below. Do not inherit or infer authority from ambient conversation.
lane_packet: <canonical_lane_packet_json>
predecessor_packet: <canonical_predecessor_packet_json_or_null>
This is a read-only task. Make no repository, GitHub, registry, release, installation, dispatch, or external mutation.
Return exactly one canonical object matching the existing trusted-owner native handoff object and no other prose.
```

The canonical prompt digest is derived before task creation and binds the
app-task operation ID, task request, lane packet, role, issue, repository,
claim, base, project-identity digest, and requested worktree observation
digest.

Any missing, duplicate, changed, reordered, extra, noncanonical, private, or
ambient prompt content is `blocked_request_or_packet_invalid` before
submission. The task receives no second prompt.

## Single-Use Boundary

The winning claim is the durable attempt reservation. Immediately before the
first create invocation, the adapter marks its process-local call guard used.
The call guard permits transition only from `not_entered` to `entered_once`.
It has no reset method.

If the process stops after call entry, the GitHub claim remains active. A
later process observes that claim and may perform read-only reconciliation,
but cannot re-enter task creation. No new local consumption schema is needed:
the existing unique request, operation, claim, and active-capacity rules make
the request permanently nonreusable after possible submission.

A known validation rejection before call entry leaves task creation known not
entered and projects the applicable existing prelaunch failure. Once call
entry occurs, every success, failure, timeout, exception, missing response,
or process loss consumes the create authority permanently.

## Closed Creation Response Normalizer

The private normalizer accepts only these returned-identity classifications:

| Classification | Exact meaning |
| --- | --- |
| `thread_id` | The create response directly supplies exactly one stable `threadId`. |
| `client_thread_id_resolved` | The create response supplies only one `clientThreadId`; later read-only list/read evidence resolves it to exactly one stable `threadId`. |
| `ambiguous_submission_reconciled` | Submission may have occurred and exact project plus operation-marker reconciliation proves exactly one stable `threadId`. |
| `identity_pending` | Only a client identity exists and no unique stable task identity is yet proven. |
| `identity_unknown` | No accepted identity exists, identifiers conflict, or the response is unavailable. |

The first three values are the only receipt-eligible
`returned_identifier_kind` values. `identity_pending` and `identity_unknown`
are private transient classifications and cannot appear in an accepted task
receipt.

Exactly one stable task identity is required. The adapter rejects or retains
unknown when neither identifier exists, both identifiers conflict, more than
one task matches the operation marker, the queued identity cannot be resolved,
project or worktree identity conflicts, the stable task identity changes, or
a required response fact is unavailable.

No accepted platform or task receipt is issued until one stable `threadId`
and exact project/worktree association are confirmed. Raw client identities
and machine-local project values never enter public evidence.

## Project And Worktree Readback

After creation and before receipt eligibility, independent
`codex_app__read_thread` evidence must confirm:

- stable task identity;
- exact saved project identity;
- immutable repository identity;
- fresh worktree identity equal to the accepted worktree observation;
- requested starting branch;
- observed base commit equal to `base_sha`; and
- exact operation marker.

The adapter hashes private project identity as SHA-256 over UTF-8
`app_native_project`, NUL, raw project identity. It never serializes the raw
value. Worktree equality uses the accepted profile worktree observation; no
raw local path is serialized.

The canonical target-readback preimage contains, in order,
`schema_version=trusted_owner_app_native_target_readback.v1`,
`task_identity_sha256`, `project_identity_sha256`, `repository_id`,
`worktree_observation_sha256`, `base_sha`, and `app_task_operation_id`,
followed by one final LF. Its SHA-256 is
`task_target_readback_sha256`. The object remains
in memory; only its digest enters the platform receipt.

If the then-current app read operation cannot directly establish every fact,
real R2 stops with `app_native_target_readback_insufficient`. It does not add
an observer, infer equality, relax the requirement, or select a fallback.

## Read-Only Observation And Deadline

`default_observation_deadline_seconds` is exactly `5400`.

After one task identity is known, `codex_app__list_threads` and
`codex_app__read_thread` may repeat only as read-only observations of the same
operation and task. They do not create, steer, resume, interrupt, cancel,
replace, archive, rename, pin, or message a task.

The deadline is measured from create-call entry by a monotonic clock. A
different positive deadline is valid only when an exact owner decision binds
it before claim and task-request construction. The selected integer must then
appear in exactly one lane `stop_conditions` member formatted
`app_native_observation_deadline_seconds:<positive integer>`. That member is
bound through `lane_packet_sha256` and `task_request_sha256`; its absence means
exactly `5400`. A duplicate, malformed, unreviewed, or contradictory member is
invalid before submission. The deadline cannot be shortened, extended, or
reset after create-call entry.

At the deadline the adapter performs one final read-only task and worktree
reconciliation. If the task is terminal, normal validation continues. If it
is running, absent, conflicting, identity-pending, or otherwise nonterminal or
unavailable, the existing profile outcome is
`unknown_outcome_reconciliation_required`. The claim remains active, the task
is untouched, no success or release receipt is published, no replacement is
created, and no follow-up prompt is sent.

A later separately admitted observer may continue readback against the same
operation and stable task identity. It cannot reuse create authority. Capacity
remains retained until one owner-authorized or independently reviewed existing
profile reconciliation closes the exact claim.

A dedicated wait, interrupt, or cancellation primitive is not required.
Their absence is a nonclaim. Timeout never authorizes cancellation,
replacement, or a second task.

## Closed Task-Status Projection

The private response normalizer emits exactly one value:

- `running`;
- `completed`;
- `failed`;
- `interrupted`;
- `unavailable`;
- `conflicting`; or
- `unknown`.

Precedence is deterministic: conflicting recognized observations select
`conflicting`; one exact directly observed terminal value selects its matching
terminal status; one exact nonterminal value selects `running`; a missing or
unreadable response selects `unavailable`; and an unrecognized value selects
`unknown`. No status is inferred from elapsed time, transcript prose, UI
appearance, or lack of output.

The adapter does not project process-start, PID, executable, descendant,
handle, Job Object, stream-drain, broker, or process cleanup states.

## Terminal Result And Existing Handoff

A completed app task is not an accepted lane result until:

1. terminal completion is directly read;
2. the stable task identity and target binding remain exact;
3. exactly one handoff object is available;
4. the existing handoff validator accepts its field order, values, and
   self-digest;
5. role, issue, repository, base, claim, operation, and worktree bindings all
   match;
6. its next role is permitted by the existing Safe or Automatic transition;
   and
7. no forbidden authority claim or ambient prose exists.

The child returns only the existing handoff object. The coordinator derives
the existing result packet from direct readback, worktree observations, the
task receipt, the validated handoff, and the lane packet. It does not repair,
summarize, or infer missing child fields.

Malformed, missing, duplicate, ambiguous, or prose-wrapped output is a known
invalid result only when its exact bytes and terminal task state are directly
known; otherwise the outcome is unknown. Neither case is success or retry
authority.

## Assigned-Worktree Reconciliation

The coordinator captures one exact accepted worktree observation before task
creation and another after terminal readback or the final deadline read.

The first E observation requires:

- unchanged HEAD;
- zero tracked modifications;
- zero staged modifications;
- zero untracked repository files;
- zero new commits;
- zero pushes;
- zero issue, PR, registry, release, installation, or external mutation; and
- no change outside the assigned worktree attributable to the lane.

The task's read-only status is a Mythic Edge authority ceiling and a verified
postcondition. This contract does not claim the app primitive technically
enforces a read-only sandbox.

An unexpected or unobservable change rejects the observation and enters the
existing reconciliation route. The coordinator never deletes, reverts,
cleans, stages, commits, pushes, or repairs unexpected state automatically.

The accepted limited network semantics remain unchanged: no network authority
is granted; executor-owned observed network operations must be zero; and this
contract makes no claim that child networking was prevented or completely
observed. Network isolation is not an R2 eligibility requirement here.

## Ambiguous Creation Reconciliation

If create fails, times out, throws, or loses its response after submission may
have occurred:

1. the create authority remains consumed and nonreusable;
2. the winning claim remains active;
3. read-only task listing/readback may match exact project context and the
   operation marker;
4. exactly one proven match may be adopted without another create call;
5. zero or multiple proven matches select
   `unknown_outcome_reconciliation_required`;
6. the adapter never sends a follow-up prompt or creates a replacement; and
7. later reconciliation remains read-only unless a separate owner decision
   and accepted profile route authorize claim closure.

A known rejection before submission is distinguishable from possible
submission. Only the former may project a known pre-task failure. Any
uncertainty about call entry or provider acceptance is unknown and preserves
the claim.

## App-Native Platform Receipt

After stable task and exact target confirmation, the adapter may construct one
canonical public-safe receipt with these fields in exact order:

| Ordinal | Field | Type and rule |
| ---: | --- | --- |
| 1 | `schema_version` | Exactly `trusted_owner_app_native_direct_platform_receipt.v1`. |
| 2 | `app_task_operation_id` | Exact derived public-safe attempt `id`. |
| 3 | `task_request_sha256` | Exact accepted task request. |
| 4 | `claim_observation_sha256` | Exact winning claim observation. |
| 5 | `lane_packet_sha256` | Exact lane packet. |
| 6 | `canonical_prompt_sha256` | Exact initial prompt digest. |
| 7 | `create_call_count` | Integer exactly `1`. |
| 8 | `returned_identifier_kind` | `thread_id`, `client_thread_id_resolved`, or `ambiguous_submission_reconciled`. |
| 9 | `task_identity_sha256` | Domain-separated stable `threadId` digest. |
| 10 | `project_identity_sha256` | Domain-separated saved-project digest. |
| 11 | `repository_id` | Exact positive integer repository ID. |
| 12 | `pre_worktree_observation_sha256` | Exact accepted pre-create observation. |
| 13 | `task_target_readback_sha256` | Exact private-to-public target projection digest. |
| 14 | `accepted_at_utc` | Whole-second task acceptance time. |
| 15 | `terminal_status` | Closed task-status projection. |
| 16 | `terminal_readback_sha256` | Public-safe readback digest or null when no terminal readback exists. |
| 17 | `typed_handoff_sha256` | Exact accepted handoff digest or null. |
| 18 | `post_worktree_observation_sha256` | Exact post observation or null when unavailable. |
| 19 | `automatic_retry_count` | Integer exactly `0`. |
| 20 | `replacement_task_count` | Integer exactly `0`. |
| 21 | `follow_up_message_count` | Integer exactly `0`. |
| 22 | `observation_deadline_seconds` | Positive integer; exactly `5400` unless pre-authorized otherwise. |
| 23 | `reconciliation_status` | `not_required`, `required_same_task`, or `resolved_same_task_terminal`. |
| 24 | `platform_receipt_sha256` | Self-digest. |

`task_identity_sha256` hashes UTF-8 `app_native_thread`, NUL, raw stable
`threadId`. The raw ID remains transient in this receipt but is the existing
public `task_id` in `trusted_owner_native_task_receipt.v1`.

`terminal_readback_sha256` is SHA-256 of one private in-memory canonical object
with exactly these six fields in this order:

| Ordinal | Field | Type and rule |
| ---: | --- | --- |
| 1 | `schema_version` | Exactly `trusted_owner_app_native_terminal_readback.v1`. |
| 2 | `app_task_operation_id` | Exact app-native operation identity from the platform receipt. |
| 3 | `task_identity_sha256` | Exact stable task-identity digest from the platform receipt. |
| 4 | `terminal_status` | Exactly `completed`, `failed`, or `interrupted`. |
| 5 | `task_target_readback_sha256` | Exact accepted target-readback digest from the platform receipt. |
| 6 | `read_at_utc` | Whole-second UTC time of the terminal read. |

The object uses the profile's NFC, ordinal key order, UTF-8 without BOM,
no-whitespace, and exactly-one-final-LF rules. It has no self-digest member;
`terminal_readback_sha256` is the SHA-256 of the complete object bytes. The
object is discarded after the enclosing platform receipt validates. It
contains no raw task ID, project identity, transcript, provider diagnostics,
path, machine value, or authority.

The canonical terminal-readback KAT is exactly 391 bytes with SHA-256
`09a3d716d4f14baf67ebc5b4914b7e4daea24d8fd4c5376924859b5885a76e45`:

```json
{"schema_version":"trusted_owner_app_native_terminal_readback.v1","app_task_operation_id":"app_native_0123456789abcdef0123456789abcdef","task_identity_sha256":"5555555555555555555555555555555555555555555555555555555555555555","terminal_status":"completed","task_target_readback_sha256":"8888888888888888888888888888888888888888888888888888888888888888","read_at_utc":"2026-08-04T12:05:00Z"}
```

Validation rejects missing, duplicate, unknown, reordered, wrongly typed, or
cross-binding fields; a nonterminal status; noncanonical UTC; missing or extra
final bytes; or a digest mismatch. Codex C may not accept an arbitrary 64-hex
value as terminal evidence.

For `completed`, a successful observation requires non-null terminal,
handoff, and post-worktree digests plus `reconciliation_status=not_required`
or `resolved_same_task_terminal`. A receipt with another status is never
success or release evidence. A task whose stable identity or target remains
unknown is not receipt-eligible.

Cross-field rules are closed:

- `completed`, `failed`, and `interrupted` require a non-null
  `terminal_readback_sha256`;
- `running`, `unavailable`, `conflicting`, and `unknown` require
  `terminal_readback_sha256=null` and
  `reconciliation_status=required_same_task`;
- `typed_handoff_sha256` is non-null only when the exact existing handoff
  validates; successful `completed` requires it, while every other value may
  carry only null;
- `post_worktree_observation_sha256` is non-null when the final observation
  succeeded and null only when that observation was unavailable;
- `not_required` applies only to a terminal status classified during the
  initial observation window;
- `resolved_same_task_terminal` applies only to a terminal status established
  by later read-only reconciliation of the same identity; and
- any other combination is noncanonical and cannot bind the outer task
  receipt.

The existing `trusted_owner_native_task_receipt.v1` uses:

- `task_id` equal to the exact stable `threadId`;
- `accepted_at_utc` equal to the companion receipt value;
- `platform_receipt_ref=role_pool:app_native_direct:` plus the first 32
  characters of `platform_receipt_sha256`; and
- `platform_receipt_sha256` equal to the companion self-digest.

The companion receipt is one necessary private platform schema. It does not
widen the public task receipt or authorize a task.

## Canonicalization And Privacy

The receipt rejects duplicate or unknown fields, wrong field order, wrong
scalar type, noncanonical enum, inconsistent nullability, or cross-binding
failure. It uses the profile's NFC, UTF-8, no-whitespace, one-final-LF, and
self-digest rules. The self-digest preimage removes only
`platform_receipt_sha256` and preserves every other byte and the final LF.

Durable evidence contains no raw transcript, prompt response, local path,
project ID, client task ID, machine ID, credential, token, environment value,
exception, stack trace, provider error, command output, PID, handle, process
identity, or private value.

The receipt may be published only through an existing separately authorized
Role Pool evidence owner. This contract creates no path, write, publication,
or mutation authority.

The canonical success known-answer vector below has one final LF. Its
self-digest preimage is `1489` bytes and yields
`c0af9c0be3cd43c4a1db80e1b525749d6c91cb2c8dc057e193c3badf17327918`.
The complete `1582`-byte artifact has SHA-256
`5df194e378dad42d515879fff05c671da3c4852394c2cbb87a3564ef9c33b0e4`:

```json
{"schema_version":"trusted_owner_app_native_direct_platform_receipt.v1","app_task_operation_id":"app_native_0123456789abcdef0123456789abcdef","task_request_sha256":"1111111111111111111111111111111111111111111111111111111111111111","claim_observation_sha256":"2222222222222222222222222222222222222222222222222222222222222222","lane_packet_sha256":"3333333333333333333333333333333333333333333333333333333333333333","canonical_prompt_sha256":"4444444444444444444444444444444444444444444444444444444444444444","create_call_count":1,"returned_identifier_kind":"thread_id","task_identity_sha256":"5555555555555555555555555555555555555555555555555555555555555555","project_identity_sha256":"6666666666666666666666666666666666666666666666666666666666666666","repository_id":1235264383,"pre_worktree_observation_sha256":"7777777777777777777777777777777777777777777777777777777777777777","task_target_readback_sha256":"8888888888888888888888888888888888888888888888888888888888888888","accepted_at_utc":"2026-08-04T12:00:00Z","terminal_status":"completed","terminal_readback_sha256":"09a3d716d4f14baf67ebc5b4914b7e4daea24d8fd4c5376924859b5885a76e45","typed_handoff_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","post_worktree_observation_sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","automatic_retry_count":0,"replacement_task_count":0,"follow_up_message_count":0,"observation_deadline_seconds":5400,"reconciliation_status":"not_required","platform_receipt_sha256":"c0af9c0be3cd43c4a1db80e1b525749d6c91cb2c8dc057e193c3badf17327918"}
```

Codex E and later tests must reconstruct this vector byte-for-byte, then
reject changed order, count, enum, nullability, digest, extra field, duplicate
field, missing final LF, or extra final byte.

## Existing Terminal Projection

The companion adds no lifecycle matrix or profile terminal outcome:

- known pre-submission validation rejection uses the first applicable existing
  prelaunch outcome;
- known post-submission task, target, terminal, handoff, or worktree failure
  uses `failed_lane_known` only when all required failure facts are directly
  known and the existing failure binding is constructible;
- unavailable, conflicting, ambiguous, or unbound creation, identity, target,
  terminal, handoff, worktree, receipt, or claim facts use
  `unknown_outcome_reconciliation_required`; and
- only a completed exact task, valid handoff, exact worktree equality, valid
  receipt, and existing claim release can eventually contribute to
  `accepted_wave_complete`.

Unknown never becomes known failure or success. Known failure never becomes
unknown merely to permit replacement. No outcome authorizes retry.

## Deferred Engineering And Non-Claims

The App Server, direct-interpreter, secure-ingress, identity-characterizer,
broker, hostile-content, and OS-isolation work remains preserved as historical
or deferred hardened-profile engineering. None is a direct realization
fallback or R2 eligibility requirement.

This contract makes no claim of:

- dedicated wait, interrupt, or cancellation support;
- task cancellation after timeout;
- exact executable, process, PID, descendant, handle, Job Object, or stream
  identity;
- complete child-network prevention or observation;
- hostile repository or malicious contributor containment;
- OS-enforced filesystem, credential, process, or network isolation;
- technical enforcement of the read-only authority ceiling;
- app-native compatibility before real independent evidence; or
- security, privacy, assurance, deployment, Stage 4, or live readiness.

## Future Inert Implementation Envelope

After independent contract acceptance and one separate owner implementation
decision, Codex C may change exactly:

1. `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py`
2. `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_direct_task_adapter.py`
3. `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py`
4. `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py`
5. `tools/check_role_pool_r0_bootstrap.py`
6. `tests/test_check_role_pool_r0_bootstrap.py`

The first file owns only the pure state machine, private response normalizer,
prompt construction, receipt validation/sealing, and injected fake-client
interface. The second owns operation-free fake-client tests. The two existing
files may receive only direct adapter selection plus existing request,
receipt, result, handoff, terminal cross-binding, and the profile-defined
rebaseline-record parser, validator, chain-tip, and current-binding rules.

The fifth and sixth files may change only the frozen accepted-profile and
new-companion bindings required to recognize this successor plus read-only
selection of the same validated rebaseline tip. The R0 evidence schema,
terminal precedence, ordinary release-record semantics, source/install
equality requirement, and all effect and authority fields remain unchanged.

The implementation must expose no real connector, generic task API, arbitrary
prompt API, task-management CLI, shell, subprocess, App Server, broker,
network client, package, registry mutation, release writer, installation, or
seventh path. It must not append the rebaseline event or invoke a real app
task. If another path or public schema is required, Codex C stops and routes
the exact mismatch to Codex B.

Adding the two source files changes the managed Role Pool manifest and
therefore requires the existing reviewed manifest-transition route before
integration. That later mechanical binding is not implementation or R2
authority and must not be hidden as an unrelated numeric replacement.

## Required Operation-Free Tests

The future fake-client suite must prove:

1. valid B and E request construction and every other role rejected;
2. the first R2 policy admits E only;
3. exact project target, fresh-worktree target, base branch, and base commit;
4. projectless, shared-local, alternate-environment, and caller-selected target
   rejection;
5. exact operation marker and canonical prompt binding with no ambient turns;
6. exactly one create call and zero follow-up messages or replacements;
7. known creation rejection before submission;
8. one direct stable task ID;
9. client identity resolving to exactly one stable task ID;
10. unresolved client identity;
11. ambiguous submission reconciled to exactly one existing matching task;
12. ambiguous submission with zero or multiple matches;
13. wrong project, repository, worktree, branch, base, operation, or changing
    task identity;
14. running before deadline and one final read at the deadline;
15. still running, absent, conflicting, or unavailable at 5400 seconds;
16. later readback of the same retained task without create authority;
17. completed terminal state with exactly one valid existing handoff;
18. completion with missing, malformed, duplicate, or prose-wrapped handoff;
19. failed and directly observed interrupted terminal states;
20. unexpected tracked, staged, untracked, commit, push, issue, PR, registry,
    release, installation, or external mutation;
21. no automatic cleanup, revert, or repair of unexpected state;
22. no retry after every known or unknown creation outcome;
23. exact receipt field order, nullability, self-digest, outer task-receipt
    binding, and private-value rejection;
24. exact six-field terminal-readback bytes and KAT plus rejection of every
    field, order, type, status, UTC, final-byte, and cross-binding mismatch;
25. historical-only R0 state before rebaseline; exact rebaseline KAT and
    current R0 tip after it; and rejection of stale, duplicate, forked,
    non-R0, post-observation, or wrongly bound rebaseline events;
26. source/install, registry, release, claim, request, lane, and worktree drift;
27. no App Server, direct-interpreter, broker, shell, subagent, or alternate
    task fallback; and
28. zero real task-management operation calls in the complete R0 suite.

Fake observations must be deterministic and operation-free. They create no
task, process, worktree, claim, receipt file, GitHub object, registry, release
record, installation, network operation, or external effect.

## Ladder Boundary

The existing ladder remains authoritative:

- R0 is fake-adapter and deterministic control validation only;
- R1 is manual-equivalence comparison only;
- R2 first observes one real read-only E task in one fresh worktree;
- R3 adds contention and up to three Safe lanes;
- R4 separately gates F draft-PR-only behavior; and
- R5-R8 govern later wave and Automatic-mode growth.

Nothing from R3-R8 moves into R2. Each later increase still requires two
accepted observations, fresh independent E review, a separate owner decision,
and one exact release append/readback.

## Stop Conditions And Remaining Unknowns

Stop inert implementation or real characterization at the first applicable
condition:

- current direct app operation descriptors drift or cannot be bound without
  invented behavior;
- exactly one stable task identity cannot be produced;
- exact project/worktree/base confirmation is unavailable;
- task status cannot be read independently;
- ambiguous creation would require another create call;
- the existing task receipt, result, or handoff cannot bind the evidence;
- the current registry or release rung does not admit the exact lane;
- a second prompt, task, fallback, mutation, or wider implementation path is
  required; or
- any of the eight owner-selected R2 requirements would require App Server,
  direct-interpreter, broker, hostile-content, or OS-isolation machinery.

The first unresolved live capability fact is exact field-level project,
worktree, base, and operation-marker confirmation from independent task
readback. It does not block contract acceptance or inert fake-client
implementation. It blocks real R2 execution until exact current evidence
establishes it.

## Validation And Acceptance

Codex B must:

- recompute the base, tree, predecessor profile, activation-comment, issue,
  merge, and protected-issue bindings;
- confirm issue #810 remains closed and PR #812 remains merged at the bound
  commit;
- strictly inspect the existing request, receipt, result, handoff, claim,
  worktree, registry, release, and terminal interfaces;
- verify the companion adds only one private platform receipt and the profile
  adds only the mechanically necessary same-file R0 rebaseline line type;
- recompute the rebaseline, terminal-readback, and enclosing platform-receipt
  KATs byte-for-byte;
- verify the final changed-path set is exactly the two contract files;
- run `git diff --check`;
- run `py -B tools/check_agent_docs.py`;
- run path-fed `tools/check_protected_surfaces.py` against `origin/main`;
- run path-fed `tools/check_secret_patterns.py` against `origin/main`;
- run path-fed `tools/select_validation.py` against `origin/main`; and
- confirm no generated residue or live task operation.

Independent Codex E must lead with findings and verify:

- exact source authority, owner activation, current base, #810 closure, and
  PR #812 merge;
- unchanged public request, task receipt, result, handoff, claim, ordinary
  release-record, authority, and 20-outcome interfaces;
- exact historical R0 preservation, 19-field no-rung-advance rebaseline KAT,
  current-profile tip selection, R1 predecessor rule, and fail-closed absence,
  drift, duplicate, fork, and post-observation behavior;
- exact one-create mapping and no second create or follow-up path;
- deterministic stable/client/ambiguous identity normalization;
- exact saved-project, repository, fresh-worktree, branch, base, task, and
  operation readback requirements without private-value emission;
- 5400-second deadline, same-task read-only observation, claim retention,
  and no replacement, cancellation, interrupt, retry, or fallback;
- exact terminal projection, existing handoff validation, and no ambient prose
  repair;
- exact six-field terminal-readback schema and KAT plus its binding into the
  revised 24-field platform-receipt KAT;
- exact pre/post worktree and external-effect reconciliation;
- the 24-field platform receipt, canonical rules, privacy, nullability, and
  unchanged outer task receipt;
- operation-free fake-client coverage and exact six-path later C envelope;
- first R2 observation restricted to one read-only E task;
- App Server and direct-interpreter evidence preserved but deferred; and
- every implementation, task, observation, release, rung, Stage 4, and
  readiness authority remains false.

Contract acceptance makes only a separate owner Codex C inert implementation
decision eligible. It does not make real task creation, R0/R1 advancement, R2
observation, publication, or dispatch eligible.

## Protected Boundaries

This contract does not authorize:

- implementation or test edits;
- task creation, list, read, wait, follow-up, steering, interruption,
  cancellation, replacement, pinning, archiving, or title mutation;
- a claim, worktree, platform receipt, result, or GitHub write;
- registry, release-state, canonical skill, installed skill, issue #769,
  issue #776, issue #810, or PR #812 mutation;
- installation, synchronization, dispatch, canary, R0-R8 advancement,
  submission, merge, deployment, or Stage 4;
- credential, private evidence, App Server, interpreter, broker, package,
  hostile-content, or OS-isolation access; or
- correctness, compatibility, security, privacy, assurance,
  `trusted_owner_native_profile_ready`, or live-readiness claims.

Current, future-without-separate-owner, and terminal operational authority
counts are `0/0/0`.

## Current Review Handoff

Next role: fresh independent Codex E contract reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Direct App-Native Release-Binding And
Terminal-Digest Contract Re-reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Owner activation: https://github.com/Tahjali11/Mythic-Edge/issues/813#issuecomment-5175504058
Base: origin/main@c24f1edf0a09a98439bdbd92ccf4e13155a3dd87
Source review report:
docs/contract_test_reports/role_pool_codex_app_native_direct_task_adapter.md
Required report SHA-256:
39dcf91bc82eb34e0802ee87473e1ceab2b6e81159d7807d89a1b625ff09d9cc
Source findings:
- ME-RP-813-E-001
- ME-RP-813-E-002

Review exactly:
- docs/contracts/trusted_owner_native_role_pool_profile.md
- docs/contracts/role_pool_codex_app_native_direct_task_adapter.md

Use the exact SHA-256 values from the Codex B handoff. Refresh origin/main,
issue #813, issue #810, PR #812, tracker #746, issue #769, ADR-0008, open PRs,
the profile, the App Server companion, canonical Role Pool source, registry,
release state, and current callable task metadata before review.

Confirm the app-native realization keeps the existing public task request,
task receipt, result, handoff, claim, registry, worktree, ordinary release
record, authority, 20-outcome, Safe/Automatic, F, and R0-R8 structures
unchanged. Verify one
create call, stable task identity resolution, exact saved-project and fresh
worktree readback, canonical operation marker and prompt, independent terminal
readback, typed handoff validation, assigned-worktree equality, 5400-second
deadline, retained claim, same-task read-only reconciliation, and zero retry,
replacement, follow-up, cancellation, interrupt, or fallback.

Verify ME-RP-813-E-001 is closed by exactly one 19-field same-file R0
rebaseline line type. Recompute its 1,352-byte preimage, self-digest,
1,435-byte artifact, and complete-artifact digest. Confirm the historical R0
line remains immutable; the event preserves R0, changes only the current
four-value binding tuple, admits no observations, and must precede every
successor-profile R0 observation. Audit absence, stale predecessor, wrong
rung, duplicate, fork, post-observation, current-tip, and R1-successor rules.
Confirm no release-state mutation authority exists.

Verify ME-RP-813-E-002 is closed by the exact six-field terminal-readback
object and 391-byte KAT. Recompute its digest and the mechanically revised
24-field platform receipt KAT. Confirm the platform receipt remains the only
new task-platform receipt, binds through the unchanged
trusted_owner_native_task_receipt.v1, and retains no transcript, local path,
project ID, credential, private value, or machine identity.

Confirm first R2 is one read-only E task and that B support is inert only.
Confirm App Server, direct-interpreter, broker, hostile-content,
network-isolation, and OS-isolation work is preserved but is neither a direct
path prerequisite nor a fallback.

Verify the exact six-path future inert implementation envelope and all
operation-free fake-client tests. Treat exact real project/worktree readback as
the first remaining live fact, not as established evidence. Contract
acceptance may make only a separate owner inert Codex C decision eligible.

Run git diff --check, check_agent_docs.py, path-fed protected-surface,
secret-pattern, and select-validation checks, exact changed-path checks, and
generated-residue checks. Do not implement, invoke task operations, mutate
GitHub/registry/release/installed state, advance a rung or Stage 4, submit,
merge, deploy, or claim readiness.

Return findings first, both reviewed hashes, both source-finding dispositions,
release-rebaseline verdict, terminal-readback and platform-receipt verdicts,
remaining live unknowns, validation, authority flags, and a workflow_handoff.
Route ambiguity to Codex B and concrete future implementation only after
acceptance plus a fresh owner decision.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
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
    - "native task launch authority"
    - "GitHub claim and release capacity"
    - "repository worktree mutation"
    - "Role Pool release ladder"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #810 is closed; the immutable #813 owner comment supplies the exact two-path ADR-0008 override."
  stop_conditions:
    - "task operation descriptor or source binding drift"
    - "need for any schema beyond the one platform receipt and one R0 rebaseline line type"
    - "need to invoke a live task operation"
    - "need to widen beyond the exact two contract paths"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/trusted_owner_native_role_pool_profile.md"
  target_artifact: "docs/contracts/role_pool_codex_app_native_direct_task_adapter.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "origin/main"
  branch: "codex/role-pool-app-native-direct-task-contract-813"
  internal_project_area: "Quality / Governance"
  truth_owner: "Core Role Pool profile and direct app-native companion"
  bridge_code_status: "shared_support"
  validation:
    - "git diff --check passed"
    - "agent docs: 55 files, 0 errors, 0 warnings"
    - "path-fed protected-surface gate: 2 paths, forbidden 0, warnings 0"
    - "path-fed secret/private-marker gate: 2 paths, forbidden 0, warnings 0"
    - "validation selector: 3 required and 1 recommended checks selected"
    - "19-field R0 rebaseline KAT: 1352-byte preimage and 1435-byte artifact exact"
    - "6-field terminal-readback KAT: 391-byte artifact exact"
    - "24-field platform-receipt KAT: 1489-byte preimage and 1582-byte artifact exact"
    - "ASCII, final-LF, trailing-whitespace, JSON, and changed-path checks passed"
  finding_status:
    ME-RP-813-E-001: "corrected_contract_only_re_review_pending"
    ME-RP-813-E-002: "corrected_contract_only_re_review_pending"
  stop_conditions:
    - "public binding drift"
    - "live task operation required"
    - "scope wider than two contracts"
```
