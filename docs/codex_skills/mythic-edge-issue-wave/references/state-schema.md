# State Schema And Helper Use

## Contents

- Command surface
- Manifest shape
- Reviewed package binding
- Run and event projections
- Transition vocabulary
- Recovery and locking
- Redaction and errors

## Command Surface

Run commands from the source-loaded skill directory. In PowerShell, quote an
invocation with single quotes so `$mythic-edge-issue-wave` remains literal.

Parse without writing:

```text
py -B scripts/issue_wave_state.py parse '<invocation>'
```

Validate and bind one root-supplied reviewed-package manifest without writing
or inspecting Git:

```text
py -B scripts/issue_wave_state.py bind-package \
  --manifest <reviewed-package.json>
```

Initialize a new Dispatch ledger from a strict JSON manifest:

```text
py -B scripts/issue_wave_state.py init '<Dispatch invocation>' \
  --manifest <manifest.json> \
  --workspace-root <absolute-workspace-root> \
  --target-root <canonical-owner/repo=absolute-checkout-root>
```

Repeat `--target-root` once per candidate. The helper creates the run ID unless
tests supply `--run-id`. Never call `init` during Inspect.

Append one transition from a strict JSON event request:

```text
py -B scripts/issue_wave_state.py transition \
  --workspace-root <absolute-workspace-root> \
  --run <run-id> \
  --expected-revision <integer> \
  --event <event-request.json>
```

Renew or release the active reservation, authorize an aligned saved-run
segment after root revalidation, or recover an expired run after termination
proof:

```text
py -B scripts/issue_wave_state.py renew-lease --workspace-root <root> --run <id> --expected-revision <n>
py -B scripts/issue_wave_state.py release --workspace-root <root> --run <id> --expected-revision <n> [--terminal]
py -B scripts/issue_wave_state.py authorize-segment '<Dispatch run invocation>' --workspace-root <root> --run <id> --expected-revision <n> --proof <proof.json>
py -B scripts/issue_wave_state.py recover --workspace-root <root> --run <id> --expected-revision <n> --proof <proof.json>
```

Inspect without writing or repairing:

```text
py -B scripts/issue_wave_state.py inspect \
  --workspace-root <absolute-workspace-root> \
  --run <run-id> \
  --invocation '$mythic-edge-issue-wave Inspect (A; run=<run-id>)'
```

CLI output is canonical JSON. Every error has a stable `error.code`, concise
message, and nonzero exit. Errors do not echo supplied values.

## Manifest Shape

Use exactly:

```json
{
  "schema_version": "mythic_edge_issue_wave_manifest.v1",
  "candidates": [
    {
      "lane_id": "repo-issue-123",
      "repository": "Tahjali11/Mythic-Edge",
      "issue": 123,
      "issue_created_at": "20260813T120000Z",
      "priority_source": "next_role",
      "target_root": "<private absolute checkout root>",
      "evidence": {
        "issue_open": true,
        "not_deferred": true,
        "prerequisites_complete": true,
        "prerequisite_relationship_unambiguous": true,
        "repository_authority_compatible": true,
        "checkout_identity_exact": true,
        "active_work_clear": true,
        "wip_compatible": true,
        "wip_exception_authorized": false,
        "scope_known": true,
        "anchor_relationship": null,
        "summary": "Public-safe current evidence summary."
      },
      "scope": {
        "paths": ["Tahjali11/Mythic-Edge:path-family"],
        "interfaces": [],
        "truth_owners": [],
        "dependencies": [],
        "shared_artifacts": [],
        "submission_lanes": ["Tahjali11/Mythic-Edge:issue-123"]
      }
    }
  ]
}
```

Use `tracker`, `roadmap`, `next_role`, or `other` as `priority_source`. Use
`dependency`, `child_issue`, `tracker`, `roadmap`, or `next_role` as a
non-null `anchor_relationship` only when `anchor=` is present.

Sort every scope token list case-insensitively and use globally qualified
tokens. Supply candidates in the deterministic order defined by the
controller protocol. The helper compares exact normalized tokens; the root
must decide semantic or path-family overlap before creating the manifest.

Resolve every target root canonically. Reject equality or any
ancestor/descendant relationship among the state root and all target roots.

## Reviewed Package Binding

Use exactly:

```json
{
  "schema_version": "mythic_edge_issue_wave_reviewed_package.v1",
  "base_commit": "0123456789abcdef0123456789abcdef01234567",
  "entries": [
    {
      "path": "docs/example.md",
      "status": "modified",
      "object": {
        "type": "blob",
        "mode": "100644",
        "byte_length": 123,
        "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      }
    }
  ]
}
```

The manifest is closed and nonempty. `base_commit` is 40 lowercase hex.
Entries use exact UTF-8 repository-relative `/` paths, sorted by path bytes,
with no duplicate, empty, `.`, or `..` segment, leading/trailing slash,
backslash, or NUL. Status is `added`, `modified`, or `deleted`; moves are one
deletion plus one addition. Every object is a `blob` with mode `100644` or
`100755`, a nonnegative raw-byte length, and a lowercase SHA-256. A deletion
describes the deleted base blob, not an empty placeholder. Symlinks, gitlinks,
trees, unmerged or intent-to-add entries, unknown keys, unsupported values,
and noncanonical entry order fail closed.

Canonical package JSON sorts object keys, uses `,` and `:` without added
whitespace, emits UTF-8 without BOM or trailing newline, and preserves entry
order. `bind-package` returns only the schema, base, ordered path list, and the
SHA-256 of those canonical bytes. The root constructs and verifies the
manifest from current repository evidence; the helper performs no discovery.

## Run And Event Projections

The private ledger contains only:

```text
<workspace>/.codex/role-pool-runs/<YYYYMMDDTHHMMSSZ-8hex>/
  run.json
  events.jsonl
```

`run.json` uses `mythic_edge_issue_wave_state.v2`. It holds schema and run
identifiers, timestamps, revision, last event digest, immutable selectors and
permissions, current segment, exact next role, immutable segment history,
execution status, accepted candidates, lane projections, reservation/lease/
recovery state, and derived run completion. Execution status is exactly
`active`, `checkpointed`, `stopped`, or `terminal`.

Each lane projection holds canonical repo/issue identity, redacted eligibility
summary and scope, private checkout/worktree locations, state, active role,
durable artifact references, `review_base_commit`,
`reviewed_package_sha256`, `created_commit`,
`submitted_package_sha256`, branch, draft PR, check summary, validation
summary, stop reason, and validated governance packets. All four package
identity fields start null. E alone sets the first pair at `e_approved`; F
alone sets the second pair at `f_complete`; each is immutable afterward.
`draft_pr` and `checks` also start null. A binds `branch` once; F must reassert
that exact branch and newly supply the positive `draft_pr` at `f_complete`.
Neither submission field may change afterward.

`events.jsonl` starts empty. Every V2 event appends one canonical UTF-8 LF line
containing schema version, sequence, timestamp, event type, segment, optional
lane transition, role, public-safe reason/evidence, closed updates, previous
digest, and its own SHA-256 digest. Types are transition, lease renewal,
checkpoint/terminal release, interruption stop, segment authorization, and
recovery admission.

An event request uses exactly:

```json
{
  "schema_version": "mythic_edge_issue_wave_event_request.v2",
  "lane_id": "repo-issue-123",
  "from_state": "selected",
  "to_state": "a_running",
  "role": "A",
  "reason": "Current pre-role evidence passed.",
  "evidence_summary": "The isolated branch and worktree now exist.",
  "updates": {
    "branch": "issue/123",
    "worktree_location": "<private absolute worktree path>"
  }
}
```

Allowlisted updates are `scope`, `worktree_location`, `artifacts`,
`review_base_commit`, `reviewed_package_sha256`, `created_commit`,
`submitted_package_sha256`, `branch`, `draft_pr`, `checks`,
`validation_summary`, and `governance_packets`. Supply a complete new value for
an updated field. This is a schema allowlist, not permission to write a field
on any transition: branch, draft-PR, package-identity, and check updates are
accepted only at their owning transitions. `reviewed_commit` is unknown and
rejected.

## Transition Vocabulary

Forward transitions are exactly:

```text
selected -> a_running -> a_complete -> a_scope_verified
a_scope_verified -> b_running -> b_complete
b_complete -> c_running -> c_complete
c_complete -> e_running -> e_approved
e_approved -> f_running -> f_complete -> checks_running
checks_running -> g_consideration_ready
```

Stop or pause states are exactly:

```text
a_ambiguous
backward_route_to_a_or_b
d_required
unknown_agent_outcome
incompatible_repository_authority
checkout_unavailable_or_ambiguous
unsafe_or_conflicting_scope
checks_pending
```

Apply these stop edges only:

- `a_running -> a_ambiguous`;
- `a_complete -> unsafe_or_conflicting_scope` after the root's A comparison;
- a pre-role boundary to incompatible authority, unavailable/ambiguous
  checkout, or unsafe/conflicting scope;
- B/C/E active or completed boundary to `backward_route_to_a_or_b`;
- C/E/F/checks boundary to `d_required`;
- any running state to `unknown_agent_outcome`;
- `checks_running -> checks_pending` at the 30-minute deadline.

The helper enforces required mechanical evidence: A starts with a branch and
existing isolated worktree; completed roles have durable artifact/validation
references; E approval atomically binds a 40-hex review base and 64-hex package
digest while branch remains unchanged and draft PR/checks remain null; F
completion atomically binds a 40-hex created commit and equal submitted-package
digest, requires the event to reassert the already-bound branch, and newly
records a positive draft PR. Check evidence is transition-scoped: exactly
`running` on `f_complete -> checks_running`, `passed` on
`checks_running -> g_consideration_ready`, `failed` on
`checks_running -> d_required`, and `pending` on
`checks_running -> checks_pending`. These checks do not prove the underlying
repository evidence is true.

## Recovery And Locking

Every initialization acquires one exclusive state-root admission lock, waits
at most five seconds, and holds it through atomic reservation and publication.
It admits at most two active waves and six lanes, requires disjoint active
repository sets, and rejects cross-run scope and path overlap. Expired but
unreleased capacity returns `recovery_proof_required`. Never remove a stale or
persistent lock. Initialization cleanup removes only owned staging state.

Every transition requires the exact current revision, an unexpired lease, and
a renewal age no greater than 60 seconds. The first immutable worktree binding
also holds the shared admission lock while checking every unreleased run, then
the per-run lock while recording the event. Every new worktree must be
non-overlapping with the state root, every target checkout, and every recorded
worktree after canonical resolution. Load and replay repeat the within-run
isolation check so a collision is a state-integrity failure. A worktree
location is set once on `selected -> a_running` and cannot later be cleared or
reassigned to bypass that check.

The helper flushes one hash-chained event before atomically replacing
`run.json`. On read:

- matching ledger and projection pass;
- a projection exactly one event behind is reconstructed in memory;
- projection ahead, more than one event behind, invalid UTF-8, duplicate or
  unknown keys, noncanonical JSON, invalid tail, broken digest, or illegal
  transition fails closed.

Read-only `inspect` never writes the reconstructed projection. A later valid
transition may continue from the in-memory recovered revision without
relaunching a role. This is state recovery only, not retry authority.

Missing recorded worktrees or artifacts do not rewrite history. Load the
ledger, report current absence during root revalidation, and stop through the
appropriate contracted state.

Each active lease lasts five minutes and renewal is accepted no later than 60
seconds after issue or renewal. Checkpoint and terminal release clear capacity
immediately but preserve branches, worktrees, artifacts, and history. Expiry
does nothing by itself. Recovery requires mechanically verified termination or
explicit owner confirmation plus stable preserved state and no active
operation. An in-flight role becomes `unknown_agent_outcome` and cannot be
resumed. A completed checkpoint must reacquire admission and record its exact
next segment before any agent launch. Its closed revalidation proof contains
every lane's exact repository head plus every durable artifact reference and
expected/observed SHA-256 identity. The canonical proof digest is bound into
both the authorization event and immutable segment history. Missing lanes,
changed identities, or false revalidation record no authorization.

## Redaction And Errors

Public summaries, artifact references, scope tokens, check summaries, and
governance packets reject drive-rooted Windows paths, backslash or
forward-slash UNC paths, every lexical POSIX absolute path, and common
secret/private markers while retaining HTTPS and repository-relative text.
`inspect` omits checkout and worktree locations and marks them redacted. It
emits saved-run continuation prompts and commands only for a released,
checkpointed run with one exact next role.

The private ledger may store only the local checkout/worktree paths needed for
recovery. Never supply credentials, tokens, environment values, complete issue
bodies, private transcripts, raw logs, runtime data, generated datasets,
workbook exports, webhook URLs, or secret-bearing output to any helper field.

Treat `state_locked`, `state_integrity_error`, `stale_revision`,
`permission_drift`, and `unknown_agent_outcome` as stops. Do not repair by
deleting files, editing JSON, weakening validation, or repeating an external
action.
