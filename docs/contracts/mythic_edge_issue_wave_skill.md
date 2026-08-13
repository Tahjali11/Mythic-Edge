# Mythic Edge Issue Wave Skill Contract

## Module

`mythic_edge_issue_wave_skill`

This contract defines a repo-owned Codex skill whose internal invocation name is
`$mythic-edge-issue-wave` and whose display name is **Mythic Edge Role Pool**.
The skill coordinates up to three dependency-safe, non-overlapping Mythic Edge
issue lanes. It is intentionally separate from the existing
`mythic-edge-role-pool` package and all R0-bound files.

The implementation is a lean hybrid:

- the root Codex coordinator owns repository and GitHub inspection, candidate
  judgment, native subagent creation, role packets, Git and GitHub actions, and
  every consequential workflow decision;
- a small deterministic Python helper owns only invocation parsing, manifest
  validation, run identifiers, transition validation, and crash-aware atomic
  local state recording;
- the helper must not inspect GitHub, select issues, spawn agents, invoke Git,
  retry work, open pull requests, or make governance judgments.

New runs start only at Codex A. Saved runs may continue only from their exact
mechanically proven next role under the segment rules in this contract. The
helper remains a local deterministic state boundary; this design adds no
daemon, service, scheduler, database, custom agent controller, or cross-machine
coordinator.

## Source Issue

https://github.com/Tahjali11/Mythic-Edge/issues/855

Issue #855 is the durable Codex A problem representation and contains the
issue-scoped user override for the bounded multi-lane implementation and draft
PR. That override does not extend to issue #826, the legacy Role Pool, merge,
installation, deployment, or a real write-enabled Mythic Edge dispatch.

## Tracker

N/A. Issue #855 is the direct source issue.

## Risk Tier

High workflow risk; no product-runtime change.

The package is workflow automation that can coordinate repository writes when
the user explicitly invokes Dispatch. Its mutation surface is bounded to
isolated issue branches/worktrees and draft pull requests; merge, deployment,
installation, credentials, private runtime data, and production state remain
forbidden. The root coordinator must keep every write behind current
repository authority and the recorded run permissions.

## Owning Layer

Quality / Governance, with GitHub and Codex native subagents treated as
External / Collaboration Surface consumers.

The skill owns coordination evidence and run-state vocabulary only. It does not
own issue truth, repository authority, implementation correctness, merge
readiness, deploy readiness, parser truth, analytics truth, workbook truth, or
AI-generated interpretation.

## Internal Project Area

Quality / Governance.

Adjacent classification:

- External / Collaboration Surface for GitHub, Git, connectors, and native
  Codex subagents;
- Generated / Local Artifacts for the ignored local run ledger;
- Shared Support for the deterministic state helper and its tests.

## Truth Owner

- Current GitHub issue, pull-request, review, and check state owns the
  corresponding collaboration facts.
- Each repository's current authority documents, accepted ADRs, issue,
  contract, handoff, diff, and tests own that lane's workflow facts.
- Git remotes, heads, worktrees, and status own local checkout facts.
- The root Codex coordinator owns reasoned candidate and overlap decisions,
  with its evidence recorded in the run manifest.
- `events.jsonl` owns the ordered local transition history; `run.json` is its
  atomically replaceable current-state projection.
- The helper owns only mechanical validation of supplied values. It must not
  turn an AI classification into project truth.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
current repo and GitHub evidence
  -> root Codex eligibility and overlap judgment
  -> self-contained lane packets
  -> fresh A, B, C, E, and F native subagents
  -> deterministic transition events and redacted coordinator output
```

Forbidden reverse flow:

- local state must not override current GitHub or repository authority;
- a generated prompt must not authorize a role or effect;
- a helper-accepted transition must not imply review, merge, deploy, release,
  or production readiness;
- subagent interpretation must not silently become a dependency, scope, or
  truth-ownership fact without evidence accepted by the root coordinator.

## Files Owned By This Contract

Codex C may create or edit only these implementation paths:

- `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
- `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
- `docs/codex_skills/mythic-edge-issue-wave/references/state-schema.md`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- `tests/test_install_codex_skills.py`
- `docs/codex_skills.md`
- `docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md`

Codex E may additionally create:

- `docs/contract_test_reports/mythic_edge_issue_wave_skill.md`

This contract file is owned by Codex B and may not be changed by C to make an
implementation easier. A contract defect routes backward to B.

No installer implementation change is authorized. The existing installer
already discovers a repo-owned directory containing `SKILL.md`; only its
expected-skill tests and documentation may change.

The entire tracked subtree
`docs/codex_skills/mythic-edge-role-pool/` and every legacy R0-bound contract,
controller, validator, profile, registry, release, and test file are forbidden.
Their current Git tree and tracked-file count must be compared before and after
implementation.

## Public Interface

### Invocation Grammar

The accepted command family is:

```text
$mythic-edge-issue-wave <Mode> (<role-or-segment>[; <option>[; <option> ...]])
```

`<Mode>` is exactly `Inspect` or `Dispatch`. Inspect accepts only role `A`.
New Dispatch accepts bare `A` or an explicit segment starting at `A`.
Saved-run Dispatch accepts bare `A` as the autonomous-resume form or an
explicit segment beginning at the run's exact next resumable role. Leading and
trailing whitespace and whitespace around semicolons may be ignored. Unknown
modes, roles, segments, options, repeated singleton options, empty values, or
malformed punctuation fail closed with concise usage guidance.

Allowed options:

- `repos=owner/repo[,owner/repo...]`: one to three unique repositories from
  the allowlist;
- `anchor=owner/repo#number`: an allowlisted repository and positive issue
  number;
- `run=<YYYYMMDDTHHMMSSZ-8hex>`: inspect or explicitly resume one existing run;
- `allow-main-draft`: Dispatch-only permission to target a draft PR to the
  repository's governed default branch when current repo authority also allows
  it;
- `allow-wip-exception`: Dispatch-only permission to exceed a repository's
  default WIP limit when current issue-scoped authority also allows it.

`run=` cannot be combined with `repos=` or `anchor=`. `allow-wip-exception` is
new-run-only. `allow-main-draft` is accepted only when the requested execution
contains F; on resume it must exactly equal the immutable permission already
recorded for the run. No resume may escalate or reduce a saved permission.
Inspect accepts no Dispatch permission flags.

Bare `Dispatch (A)` is the compatibility form for autonomous A through F.
Bare `Dispatch (A; run=<run-id>)` starts at the run's exact mechanically proven
next role and continues through F. Explicit new-run checkpoint segments are
exactly `A-A`, `A-B`, `A-C`, `A-E`, and `A-F`. Explicit saved-run segments must
start at the exact next resumable role and may end only at that role or a later
normal-path role through F. Consequently, aligned single-role segments
`B-B`, `C-C`, `E-E`, and `F-F` are valid on resume. D is a corrective route,
not a selectable segment role. Backward, repeated, skipped-start, D-inclusive,
misaligned, or post-F segments fail closed before authorization or effect.

Canonical forms:

```text
$mythic-edge-issue-wave Inspect (A)
$mythic-edge-issue-wave Inspect (A; repos=owner/repo,owner/repo)
$mythic-edge-issue-wave Inspect (A; repos=owner/repo; anchor=owner/repo#123)
$mythic-edge-issue-wave Inspect (A; run=20260813T120000Z-1a2b3c4d)
$mythic-edge-issue-wave Dispatch (A)
$mythic-edge-issue-wave Dispatch (A; repos=owner/repo; allow-main-draft)
$mythic-edge-issue-wave Dispatch (A; anchor=owner/repo#123; allow-wip-exception)
$mythic-edge-issue-wave Dispatch (A-B; repos=owner/repo)
$mythic-edge-issue-wave Dispatch (A; run=20260813T120000Z-1a2b3c4d)
$mythic-edge-issue-wave Dispatch (C-E; run=20260813T120000Z-1a2b3c4d)
```

The parser returns a typed, JSON-serializable invocation object. Parsing is
syntactic only; it does not prove eligibility or authority.

### Default Repository Allowlist

The default allowlist is exactly:

- `Tahjali11/Mythic-Edge`
- `Tahjali11/Mythic-Edge-Analytics`
- `Tahjali11/Mythic-Edge-Fable-Engine`
- `Tahjali11/Mythic-Edge-Corpus`
- `Tahjali11/Mythic-Edge-Automation-Artifacts`
- `Tahjali11/Mythic-Edge-Security`
- `Tahjali11/Mythic-Edge-Feature-Expansions`
- `Tahjali11/Mythic-Edge-Research-and-Development`
- `Tahjali11/Mythic-Edge-Application-Function`
- `Tahjali11/Mythic-Edge-Governance`

Matching may be case-insensitive, but the canonical spelling above must be
emitted and stored. With `repos=`, only that exact normalized set is searched;
an excluded repository is not replaced from the wider allowlist. Without
`repos=`, all allowlisted repositories may be inspected and at most three lanes
selected. No run may select more than one issue from one repository.

### Inspect Mode

New-candidate Inspect is read-only and produces:

- repositories and issues examined;
- one explicit eligibility or exclusion reason for every issue considered;
- zero to three deterministically ordered, non-conflicting candidates;
- current evidence for prerequisites, WIP compatibility, checkout identity,
  active-work exclusion, and lane separation;
- one directly pasteable `$mythic-edge-workflow` Codex A prompt per selected
  candidate.

`Inspect (A; run=...)` audits an existing ledger and current read-only evidence.
It may report staleness and the next mechanically possible action, but it must
not repair, reconcile, append to, touch, or resume the run.

Inspect must create no local state, files, directories, worktrees, branches,
commits, tasks, issues, comments, labels, pull requests, check reruns, or other
GitHub writes. It must not install a skill. A source-loaded Inspect validation
must operate directly from the repo-owned skill directory.

### Candidate Evidence Model

The root coordinator must prove all of the following before selection:

1. The issue is open, is not deferred, and is not already represented by an
   active issue branch, worktree, pull request, or conflicting current lane.
2. Every declared prerequisite is complete according to durable current
   authority. An absent or ambiguous prerequisite relationship fails closed.
3. The repository provides current A-G authority and durable conventions for
   its A, B, C, E, and F artifacts. Incompatible or missing authority excludes
   the candidate.
4. Exactly one local checkout can be matched to the expected GitHub repository
   by normalized fetch/push remote identity. Missing and conflicting matches
   are reported and excluded. Cloning is never automatic.
5. Known file paths or path families, public interfaces, truth owners,
   dependencies, shared artifacts, schema surfaces, and submission lanes do not
   overlap any other selected candidate.
6. Repository WIP-1 policy is satisfied, unless both the invocation records
   `allow-wip-exception` and current issue-scoped repo authority permits that
   exception.

An `anchor=` is a filter, not a similarity hint. A candidate must have a
durable dependency edge, child-issue edge, tracker/roadmap membership, or
explicit next-role relationship to the anchor. Textual similarity alone is
insufficient.

Authority-backed tracker, roadmap, and next-role candidates rank first.
Equally ranked candidates order oldest issue creation time first, then
canonical repository name, then numeric issue number. Fewer than three eligible
issues returns fewer than three lanes.

The helper may validate the shape and deterministic ordering of a candidate
manifest supplied by the root coordinator. It must not fetch, infer, rank, or
select candidates.

### Dispatch Mode

One parent Codex task owns one wave. Dispatch uses these root-owned steps:

1. Revalidate each selected issue and matched checkout immediately before any
   write. Create one isolated issue branch and worktree per lane only after all
   preconditions pass.
2. Spawn up to three fresh Codex A native subagents in parallel. Each receives
   a self-contained public-safe packet, invokes `$mythic-edge-workflow`, reads
   that repository's current authority, and writes only its repository-
   authorized problem-representation artifact.
3. The root coordinator compares the exact A scopes again across files,
   interfaces, truth ownership, dependencies, shared artifacts, and submission
   lanes. Conflicting lanes stop; unaffected lanes continue; replacements are
   never backfilled into the current run.
4. For every continuing lane, spawn a fresh B agent, then a fresh C agent, then
   an independent fresh E agent, then a fresh F agent. Each agent receives only
   the self-contained lane packet and durable artifacts needed for its role and
   must invoke `$mythic-edge-workflow`.
5. B defines the contract and required tests. C implements and validates only
   that contract and may correct its own in-scope mistakes during its turn. E
   independently reviews the issue, contract, exact pre-commit package,
   handoff, and evidence. E approval records the package binding defined below,
   not a commit. F makes no implementation edits: it reconstructs and stages
   only that reviewed package, creates the commit, proves the commit contains
   that exact package, pushes, and opens a draft pull request.
6. After a draft PR exists, poll its checks for at most 30 minutes. Passing
   required checks yields `g_consideration_ready`; any failing required check
   yields `d_required`; checks still nonterminal at the deadline yield
   `checks_pending`.
7. Stop before Codex G and return a directly pasteable G prompt. Never merge,
   deploy, mark a draft ready, close an issue, install the skill, or start a
   runtime/production action.

Bare `Dispatch (A)` performs the complete route above. An explicit segment
performs only the roles within its inclusive endpoints. At the segment endpoint
the coordinator waits until every unaffected lane has either reached that
endpoint or reached a defined stop state, records the checkpoint, releases the
wave's active reservation, and stops without creating an agent for the next
role. A stopped lane is not replaced or backfilled. A lane stopped earlier does
not prevent unaffected lanes from reaching the requested endpoint unless its
finding invalidates shared evidence or dependencies.

Every resumed segment requires a new immutable segment-authorization event
before any role agent starts. That event binds the requested segment, exact
next role, current run revision, revalidated repository heads and artifacts,
immutable permissions, and reacquired reservations. Segment authorization is
prerequisite evidence only; it does not establish role success or authorize
any effect outside the segment.

Agent creation and orchestration remain native root Codex responsibilities. No
Python program, background service, scheduled task, external controller, or
unattended retry loop may spawn or impersonate the agents.

### Reviewed Package Identity And E/F Handshake

E approves an exact pre-commit change package. The package is the canonical
UTF-8 JSON encoding of this schema:

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

The schema is closed and deterministic:

- `schema_version` is exactly
  `mythic_edge_issue_wave_reviewed_package.v1`;
- `base_commit` is the exact 40-lowercase-hex commit against which E reviewed
  the package, and lane `HEAD` must equal it until F creates the commit;
- `entries` is nonempty and sorted by the exact UTF-8 bytes of `path`, with no
  duplicate path;
- `path` is a valid UTF-8, repository-relative Git path using `/`, with no
  leading or trailing slash, backslash, NUL, empty segment, `.` segment, or
  `..` segment; Unicode text is not case-folded or normalized;
- `status` is exactly `added`, `modified`, or `deleted`; rename detection is
  disabled, so a move is one explicit `deleted` entry plus one `added` entry;
- `added` means absent from the base and present in the compared result,
  `modified` means present in both with different bytes or mode, and `deleted`
  means present in the base and absent from the compared result; identical
  entries are omitted, non-ignored untracked regular files are `added`, and
  ignored files are outside the package;
- `object.type` is exactly `blob`, `object.mode` is exactly `100644` or
  `100755`, `byte_length` is the nonnegative length of the raw blob bytes, and
  `sha256` is the lowercase SHA-256 of those exact bytes;
- for `added` and `modified`, `object` describes the proposed result bytes and
  mode; for `deleted`, it describes the exact base-commit blob being deleted,
  so a deletion is never represented by an absent or empty placeholder; and
- symlinks, gitlinks/submodules, trees, unmerged entries, intent-to-add
  entries, unsupported modes or types, invalid paths, unknown keys, and any
  status outside the closed vocabulary are unsupported and fail closed to
  `d_required`.

Canonical encoding sorts every object key lexicographically, uses the JSON
separators `,` and `:` with no added whitespace, emits UTF-8 without a BOM or
trailing newline, and emits JSON integers for byte lengths. The entries array
keeps the required path order. `reviewed_package_sha256` is the lowercase
SHA-256 of those canonical manifest bytes; the digest is stored outside the
manifest and therefore does not self-reference. File bytes are hashed without
newline conversion. If Git clean filters or line-ending conversion make the
staged blob differ from the bytes E reviewed, that is byte drift and fails
closed; V1 does not silently normalize or waive the mismatch.

The helper exposes one read-only `bind-package` operation for this schema. It
accepts strict manifest JSON supplied by the root, rejects duplicate or unknown
keys and every noncanonical/unsupported value above, and returns only the
canonical schema version, base commit, ordered path list, and
`reviewed_package_sha256`. It performs no Git or filesystem discovery and
writes no ledger or repository state. The root derives the manifest entries
from current Git/worktree evidence and verifies their truth; helper output is
only mechanical schema/encoding evidence. E and F use this same operation so
the binding algorithm cannot drift between roles.

E may approve only when `HEAD` is the manifest `base_commit`, the real index
has no staged change, the manifest represents every non-ignored changed path
relative to that base, E reviewed every entry, and E has no blocking finding.
The `e_running -> e_approved` transition atomically records exactly:

- `review_base_commit`: the manifest `base_commit`;
- `reviewed_package_sha256`: the manifest binding; and
- E's validation/artifact references.

It must not record `reviewed_commit`, `created_commit`,
`submitted_package_sha256`, a push, or a pull request. Review approval does not
grant F authority; it only binds the exact package that F is allowed to
submit.

Every lane initializes `review_base_commit`, `reviewed_package_sha256`,
`created_commit`, and `submitted_package_sha256` to null. The first two may
change from null only on `e_running -> e_approved`; the last two may change
from null only on `f_running -> f_complete`; all four are immutable afterward.
Both commit fields require 40 lowercase hexadecimal characters and both
package fields require 64 lowercase hexadecimal characters. `reviewed_commit`
is not a compatibility alias: it is an unknown lane/update key and fails
closed. Because no installation or real Dispatch is authorized for this
unsubmitted package, the implementation keeps this corrected field set rather
than adding a compatibility alias or accepting an ambiguous old run shape.

Before F starts, the root reconstructs the manifest from the current worktree
and the recorded `review_base_commit`. `HEAD`, the complete changed-path set,
each status, mode, type, byte length, byte SHA-256, order, and the resulting
manifest binding must still match E's values, and the real index must still
contain no staged change. Any mismatch routes the lane to `d_required` before
F is launched.

F receives only the reviewed manifest identity and its exact paths. F must:

1. revalidate the same base, empty-index, worktree-package, and binding facts;
2. stage only the exact manifest paths, including each explicit deletion,
   without `git add -A`, an unrestricted pathspec, implementation edits, or
   any additional path;
3. reconstruct the canonical package from the index against
   `review_base_commit` and prove its binding equals
   `reviewed_package_sha256` before committing;
4. create one commit whose sole parent is `review_base_commit`;
5. reconstruct the package from that commit against `review_base_commit` and
   prove its binding again equals `reviewed_package_sha256`; and
6. only after that post-commit proof, push the created commit and create the
   draft PR.

The `f_running -> f_complete` transition records `created_commit`,
`submitted_package_sha256`, branch, and positive draft-PR reference.
`submitted_package_sha256` must exactly equal `reviewed_package_sha256`, the
created commit must be 40 lowercase hexadecimal characters with the recorded
review base as its sole parent, and the root must have proved the commit change
package produces that digest. Helper validation is mechanical evidence only;
the root remains responsible for proving the Git facts.

Any base, byte, path, set, order, status, mode, type, length, digest, index,
parent, or commit-package drift fails closed to `d_required`. F must preserve
the worktree and any created local commit, must not edit, broaden the staged
set, stage a replacement path, amend, reset, create a replacement commit,
push a mismatched commit, or open a draft PR after such a mismatch. A fresh D
fix and fresh independent E review are required before another F attempt.

### Versioned Coordination Schemas

The checkpoint/concurrency revision uses these exact schema versions:

- normalized invocation: `mythic_edge_issue_wave_invocation.v2`;
- run projection: `mythic_edge_issue_wave_run_state.v2`;
- ledger event: `mythic_edge_issue_wave_event.v2`;
- transition/event request: `mythic_edge_issue_wave_event_request.v2`; and
- redacted Inspect projection: `mythic_edge_issue_wave_inspect.v2`.

The candidate manifest and reviewed-package manifest remain at their existing
V1 schema versions because their fields and meanings do not change. All V2
schemas are closed: duplicate keys, unknown keys, missing required keys, wrong
types, noncanonical identifiers, or invalid cross-field combinations fail
closed. No V1 run migration or dual-read compatibility is required because no
installed or real Dispatch state exists.

### Lane States And Stop Reasons

Progress states are exactly:

```text
selected
a_running
a_complete
a_scope_verified
b_running
b_complete
c_running
c_complete
e_running
e_approved
f_running
f_complete
checks_running
g_consideration_ready
```

Terminal or paused stop states are exactly:

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

Run execution status is separate from lane state and is exactly `active`,
`checkpointed`, `stopped`, or `terminal`. `active` means a current segment owns
an unexpired lease and reservations. `checkpointed` means all unaffected lanes
reached the requested segment endpoint or a defined lane stop and the lease was
released. `stopped` means safe automatic continuation is unavailable.
`terminal` means no forward role before G remains. Checkpointed and terminal
runs consume neither an active-wave slot nor a repository reservation.

The normal role order is `A, B, C, E, F`. The mechanically derived next role is
`A` before any A work, `B` after `a_scope_verified`, `C` after `b_complete`, `E`
after `c_complete`, and `F` after `e_approved`. A lane with a stop state,
`f_complete`, `checks_running`, `checks_pending`, or
`g_consideration_ready` has no resumable forward role unless this contract
explicitly names a safe check-status continuation. `unknown_agent_outcome`
never has a next resumable role.

Allowed forward transitions are:

```text
selected -> a_running -> a_complete -> a_scope_verified
a_scope_verified -> b_running -> b_complete
b_complete -> c_running -> c_complete
c_complete -> e_running -> e_approved
e_approved -> f_running -> f_complete -> checks_running
checks_running -> g_consideration_ready
```

`e_approved` means E approved the exact canonical pre-commit package and the
lane projection contains `review_base_commit` plus
`reviewed_package_sha256`; it never means a commit already exists.
`f_complete` means F alone created and submitted `created_commit`, and the
lane projection contains a `submitted_package_sha256` equal to E's binding
after both pre-commit index proof and post-commit package proof. Neither state
may be inferred from a role summary or validation text alone.

Stop transitions are allowed only when their reason is supported by the
current role or revalidation evidence:

- `a_running -> a_ambiguous`;
- `a_complete -> unsafe_or_conflicting_scope` after the cross-lane A comparison;
- any pre-role revalidation boundary ->
  `incompatible_repository_authority`,
  `checkout_unavailable_or_ambiguous`, or
  `unsafe_or_conflicting_scope`;
- B, C, or E active/completed boundaries -> `backward_route_to_a_or_b` when
  framing or contract authority is wrong or ambiguous;
- C, E, F, or checks boundaries -> `d_required` for a concrete implementation,
  review, reviewed-package drift, submission, test, or CI defect;
- any `*_running` state -> `unknown_agent_outcome` when the agent is interrupted
  or its durable outcome cannot be proven;
- `checks_running -> checks_pending` at the 30-minute deadline.

No terminal or paused state automatically retries. `unknown_agent_outcome` is
not resumable. Unaffected lanes continue unless the finding invalidates shared
dependency or selection evidence, in which case the newly unsafe lanes stop.
No stopped lane is replaced or backfilled.

Stable coordination error codes additionally include:

- `active_wave_limit`: two other active waves retain unreleased capacity;
- `repository_reserved`: an active wave already reserves any requested repo;
- `unsafe_or_conflicting_scope`: a cross-run scope, target-root, worktree,
  state-root, issue, or known submission-surface conflict exists;
- `state_locked`: admission or per-run state cannot be locked within its
  bounded wait; and
- `recovery_proof_required`: an expired lease exists but prior task/agent
  termination or a safe preserved boundary is not proven.

These are refusals, not retry instructions. They cause no candidate
replacement, lane backfill, worktree creation, agent launch, or GitHub effect.

### Pasteable Next-Role Output

Every lane result contains:

- run and lane identifiers;
- canonical repository and issue identifier;
- requested segment, roles completed, lane status, and last completed role;
- durable artifact references, review base, reviewed-package binding, created
  commit, and submitted-package binding where available;
- validation summary;
- branch and draft PR reference when applicable;
- exact state or stop reason;
- remaining unknowns;
- concise role summaries, including A framing and B contract summaries when
  those roles completed;
- one public-safe, directly pasteable manual next-role prompt when a next role
  is mechanically allowed; and
- the optional exact next-segment command when skill continuation is
  mechanically possible.

Checkpoint output references exact public-safe artifacts and links but does
not reproduce complete issue, contract, review, handoff, or transcript bodies.
It does not create the next-role agent. Material governance packets are listed
with their trigger reasons, but a checkpoint does not create a Codex H task.

Local absolute paths may be used inside the private local ledger and local
agent instructions when required, but must never appear in GitHub bodies,
comments, committed artifacts, governance packets, or public
`workflow_handoff` blocks.

## State And Recovery Interface

Dispatch state lives outside every target repository:

```text
<workspace>/.codex/role-pool-runs/<YYYYMMDDTHHMMSSZ-8hex>/
  run.json
  events.jsonl
```

The common state root also owns one OS-enforced admission lock used only while
validating and atomically recording admission, reservation, lease, release, or
recovery changes. Acquiring that lock waits no longer than five seconds.
Persistent contention returns `state_locked`. The helper never deletes or
breaks a lock merely because its file or metadata appears old.

The caller supplies an explicit workspace root and target repository roots.
The helper resolves them and refuses a state root that is inside, equal to, or
ambiguous relative to any target repository. Run IDs use UTC plus eight
lowercase hexadecimal characters. A cryptographically random suffix is the
default; tests may inject time and entropy.

`run.json` contains only versioned structured fields needed to recover:

- schema version, run ID, created/updated UTC times, revision, and last event
  digest;
- parsed selectors, immutable Dispatch permissions, requested current segment,
  exact next resumable role, run execution status, and immutable segment
  history;
- canonical repository/issue identifiers and redacted eligibility evidence;
- lane state, active role, durable artifact references,
  `review_base_commit`, `reviewed_package_sha256`, `created_commit`,
  `submitted_package_sha256`, branch/PR/check references, local worktree
  location, validation summary, and stop reason;
- canonical target roots and known cross-run scope/submission surfaces;
- reservation owner, reserved canonical repository set, lease issue/renewal/
  expiry/release timestamps, and recovery-proof state; and
- governance packet references and run completion state.

`events.jsonl` contains canonical one-line JSON transition records with schema
version, sequence number, UTC timestamp, event type, lane ID when applicable,
from/to state, role, segment, public-safe reason/evidence summary, and a SHA-256
link to the previous event. Event types include segment authorization,
transition, lease creation, lease renewal, checkpoint release, terminal
release, interruption stop, and recovery admission. Unknown keys, duplicate
JSON keys, invalid UTF-8, invalid types, malformed timestamps, unexpected
revisions, broken hash chains, path escapes, and illegal transitions fail
closed.

The ledger must not store credentials, tokens, environment values, complete
issue bodies, private transcripts, raw logs, private runtime data, generated
datasets, workbook exports, webhook URLs, or secret-bearing command output.
Issue excerpts are reduced to identifiers and public-safe evidence summaries.

State mutation requires the shared admission lock when cross-run ownership can
change, an exclusive per-run lock, and an expected revision. The helper
appends and flushes the next hash-chained event, then atomically replaces
`run.json` with a projection at the same revision. On load:

- a matching event ledger and projection are accepted;
- a projection exactly one revision behind a valid fully flushed final event
  may be deterministically reconstructed without rerunning an agent;
- a projection ahead of the ledger, more than one revision behind, an invalid
  tail, a broken chain, or a conflicting lock fails with
  `state_integrity_error` or `state_locked` and performs no mutation.

### Cross-Run Admission And Isolation

Under the shared admission lock, the helper validates a public-safe inventory
of all non-released V2 runs in the same canonical workspace. Admission permits
at most two active waves, three repositories per wave, and six active lanes in
total. An expired but unrecovered wave remains non-released and blocks capacity
or repository reuse with `recovery_proof_required`; expiry is not an implicit
release. The active waves' canonical repository sets must be disjoint. It also
rejects duplicate or nested target/worktree locations and supplied cross-run
issue-scope, target-root, worktree, state-root, or known submission-surface
overlap. Semantic overlap that cannot be mechanically encoded remains a root
coordinator judgment and must fail closed when material uncertainty remains.

Admission and reservation recording are one atomic critical section and occur
before branch/worktree creation, agent launch, or GitHub mutation. If two
invocations race, only a still-valid winner records capacity and repository
reservations. A loser returns the applicable stable error and performs no
repository effect, retry, replacement selection, or backfill. Historical,
checkpointed, stopped runs whose lease was released, and terminal runs remain inspectable but
do not consume active capacity or hard reservations. Coordination across
different canonical workspaces or machines is outside this version.

### Renewable Reservation Lease

Every active wave receives a five-minute lease, represented by canonical UTC
issue, last-renewed, and expiry timestamps. The owning coordinator renews it at
least once every 60 seconds, including while waiting for role agents or bounded
CI checks. Each renewal requires the expected run revision, holds the required
locks, extends expiry to five minutes after the recorded renewal time, and
appends an atomic hash-chained lease-renewal event. Renewal does not authorize
a role or prove progress.

A fully recorded checkpoint or normal terminal stop immediately appends its
release event, clears the active slot and hard repository reservations, and
sets the appropriate execution status. Branches, worktrees, artifacts, partial
results, and event history remain preserved. Lease expiration alone performs
no write: it never deletes, cleans, retries, resumes, releases preserved work,
backfills, or authorizes a role. It means only that a later invocation may ask
for recovery inspection.

### Resume And Fail-Closed Recovery

Resume is explicit only. Before continuing, the root coordinator revalidates
live GitHub state, repository heads, artifacts, worktrees, prior role outcomes,
immutable permissions, every recorded reviewed/submitted package binding, and
all active cross-run reservations. A lane resumes only from a fully completed,
mechanically proven boundary. A stale head, missing artifact, changed review
base, changed package binding, mismatched scope, uncertain agent outcome,
changed permission, or conflicting live state remains stopped. Resume never
means automatic retry.

An expired lease permits recovery inspection only after the former parent task
and all of its agents are proven finished or stopped through available Codex
task state. If that cannot be mechanically verified, recovery requires an
explicit user confirmation that the former task and all its agents were
stopped. Repository inactivity alone is never proof. The recovery inspection
then validates the entire event chain, preserved worktrees and branches,
repository heads, exact artifacts and package bindings, operation markers,
reservations, and absence of any conflicting agent or repository operation.
Only a complete checkpoint already durably recorded before interruption may
reacquire capacity and authorize its exact next segment after full live-state
revalidation.

If any role was in flight or its durable outcome is uncertain, the lane and run
stop as `unknown_agent_outcome`. The role is never automatically retried or
resumed. Expired capacity may be released only after the termination and
preserved-state inspection above; replacement work requires a fresh invocation
that independently passes conflict and preserved-worktree checks. No recovery
path adopts or certifies unproven work.

Manual continuation from a checkpoint prompt is supported, but the saved run
never imports, adopts, infers, or retrospectively certifies a manually or
externally completed role. If external work advances a repository, artifact,
branch, commit, or PR beyond the saved boundary, resume detects drift before
new segment authorization and stops. The original run remains available for
read-only Inspect; continued work remains manual or begins as a distinct fresh
run after conflicts are resolved.

The helper's command-line surface may expose only these operations:

- `parse`: parse and print a normalized invocation without writing;
- `bind-package`: validate and bind a root-supplied canonical reviewed-package
  manifest without writing or inspecting Git;
- `init`: validate a root-supplied manifest and create a new Dispatch ledger;
- `transition`: append one expected, allowed transition;
- `renew-lease`: atomically renew an active wave lease;
- `release`: atomically checkpoint or terminal-release reservations;
- `authorize-segment`: record a new or resumed segment before agent launch;
- `recover`: validate root-supplied task-termination and preserved-state proof,
  then reacquire capacity only at a proven checkpoint boundary;
- `inspect`: validate and print a redacted state projection without writing.

All machine errors use a stable code and concise message and return nonzero.
Machine output must not echo forbidden input values.

## Governance Feedback Interface

Material friction means one of:

- Codex A ambiguity;
- incompatible or conflicting current authority;
- an unsafe governance-rule gap;
- repeated inefficiency with the same mechanically identifiable cause; or
- a systemic failure affecting multiple lanes or roles.

The affected agent returns a redacted feedback packet to the root coordinator.
The packet records only schema version, run/lane/repository/issue identifiers,
role, trigger category, observed public-safe evidence summary, impact, repeated
pattern count when known, unresolved governance question, and suggested review
route. It contains no local paths, secrets, private content, complete issue
bodies, transcripts, raw logs, or proposed authority edits.

At a checkpoint, the result preserves and surfaces each packet and its trigger
reason but creates no Codex H task. At terminal run completion, when at least
one material packet exists, the root coordinator opens one separate read-only
Codex task in the saved **Mythic Edge** project and asks
`$mythic-edge-constitutional-lawyer` to inventory and analyze the packets. That
task may propose amendments or watch-list items but must not edit governance
authority or target repositories. If task creation is unavailable, the result
contains one equivalent directly pasteable prompt. No governance task is
created when there is no material packet.

## Inputs

- The exact invocation string.
- Current allowlist and optional explicitly supplied repository selector.
- Current live GitHub issue, PR, review, and check metadata acquired by the
  root coordinator through read-only operations until Dispatch mutation is
  authorized.
- Current local checkout, remote, branch, worktree, and dirty-state evidence.
- Current repository authority, accepted ADRs, issue artifacts, contracts,
  handoffs, diffs, and tests.
- Root-authored candidate manifests, canonical reviewed-package manifests,
  role packets, transition events, and redacted governance packets.
- For resume, an explicit run ID and current valid local ledger.

Inputs from local skills, memory, previous chat, tracker prose, issue labels,
or generated prompts are leads only until verified against current authority.

## Outputs

Inspect output is a read-only human-readable report with structured candidate
evidence and pasteable Codex A prompts.

Dispatch output is a per-lane report plus a local run ledger. A checkpointed
lane ends at its requested role with exact artifact references, concise role
summaries, a manual next-role prompt, and an optional aligned next-segment
command. A successful full lane ends at `g_consideration_ready` with matching
reviewed/submitted package bindings, the F-created commit, a draft PR, and
pasteable Codex G prompt. Other lanes end at one exact stop state with
evidence and, when safe, a pasteable recovery prompt. Neither output is a
readiness or authority claim beyond its defined state.

## Invariants

- The legacy `mythic-edge-role-pool` subtree and all R0-bound bytes remain
  unchanged.
- Inspect is zero-write, including no run directory.
- Dispatch never selects more than three lanes or more than one issue per repo.
- One canonical workspace never has more than two active or expired-unreleased
  waves, six associated lanes, or overlapping unreleased repository sets.
- Explicit `repos=` never falls back to another repository.
- Selection and post-A overlap checks fail closed on unknown material scope.
- Each A, B, C, E, and F turn uses a fresh native subagent and current durable
  artifacts; agent chat history is not authority.
- E is independent from C and approves the exact canonical pre-commit package,
  not a pre-existing commit. F alone stages, commits, pushes, and creates the
  draft PR; F makes no implementation edit.
- The package E approves and the package F stages and commits have the same
  base commit, exact ordered paths, statuses, modes/types, byte lengths,
  byte SHA-256s, and canonical manifest SHA-256.
- F stages no path outside the E-approved package and never repairs package
  drift by editing, expanding the staged set, amending, or replacement commit.
- A conflict does not cancel an unaffected lane unless shared evidence or a
  dependency becomes invalid.
- Stopped lanes are never backfilled or automatically retried.
- Every active lease lasts five minutes and is renewed no later than 60 seconds
  after its previous issue or renewal while the coordinator remains active.
- Checkpoint and normal terminal release preserve all branches, worktrees,
  artifacts, partial results, and event history.
- Expiry grants recovery-inspection eligibility only; uncertain task or role
  outcome remains `unknown_agent_outcome` with no automatic retry.
- Manual work is never adopted into a saved run.
- The helper has no network, Git, GitHub, subagent, task-creation, merge,
  deployment, installation, or issue-selection capability.
- State is local, explicit, versioned, redacted on output, integrity checked,
  and outside all target repositories.
- Validation, draft PR checks, E approval, and
  `g_consideration_ready` are prerequisite evidence only. They do not authorize
  G, merge, deployment, installation, release, production effects, or a later
  real Dispatch.

## Error Behavior

Malformed invocation, unsupported or misaligned segment, out-of-allowlist
repository, excessive repository count, invalid option combination, invalid
manifest, invalid transition, duplicate or stale revision, corrupt state,
unsafe state-root placement, permission drift, active-wave limit, repository
reservation, cross-run path or scope overlap, lease/recovery proof failure,
unsupported reviewed-package entry, or reviewed-package binding drift fail
closed with no unauthorized continuation.

Eligibility ambiguity excludes the candidate. Post-selection ambiguity stops
only affected lanes unless the ambiguity invalidates shared evidence. A missing
checkout is reported; it is never cloned. Dirty or conflicting worktrees are
preserved. Interrupted agents yield `unknown_agent_outcome`; no automatic retry
is allowed. Failed required PR checks yield `d_required`; nonterminal checks at
30 minutes yield `checks_pending`.

If an external write reports an uncertain outcome, the root coordinator first
performs a read-only reconciliation. It must not blindly repeat branch, push,
comment, task, or PR creation. If exact outcome still cannot be proven, the lane
stops with `unknown_agent_outcome`.

If package drift is found before commit, F performs no commit, push, or PR
creation. If post-commit reconstruction differs, the mismatched commit remains
local and preserved, no push or PR creation occurs, and the lane transitions to
`d_required`. Neither case permits F to edit or silently restage a replacement
package.

## Side Effects

Inspect side effects: none.

Authorized Dispatch side effects are limited to:

- one local run directory outside target repositories;
- shared admission locking plus atomic local reservation/lease/release records;
- up to three isolated worktrees and issue branches;
- repository-authorized A, B, C, E, and implementation handoff artifacts;
- contracted implementation and test edits on each lane;
- one F-created commit per successful lane only after exact reviewed-package
  staging proof, followed by its branch push only after exact post-commit
  package proof;
- one draft PR per successful lane;
- check-status reads for at most 30 minutes;
- one separate read-only Codex H task only at terminal completion when material
  governance packets exist, or a pasteable fallback prompt if task creation is
  unavailable.

Dispatch must not clone, clean, stash, reset, delete, merge, deploy, install,
mark a PR ready, close an issue, rerun checks, access private runtime paths,
read secrets, modify credentials, invoke webhooks, alter workbooks, or start
runtime controllers.

## Dependency Order

1. Revise this Codex B contract before implementation.
2. Update the deterministic helper, V2 schema/protocol references, skill
   instructions, UI metadata when needed, focused tests, installer expectations,
   concise documentation, and implementation handoff within the owned paths.
3. Run focused parsing, transition, concurrency, lease, recovery, package,
   redaction, and installer tests.
4. Run source-loaded live Inspect and prove zero writes.
5. Run synthetic two-wave Dispatch across six disposable repositories using
   local remotes and mocked PR/CI boundaries.
6. Run broader repo validation and prove the legacy Role Pool tree identity.
7. Run fresh independent Codex E review and replace the stale review report
   with exact-current-package evidence.
8. Route concrete findings through D and repeat fresh E after any changed byte.
9. Only after E reports no blocking findings may Codex F stage the exact
   reviewed package, create one new commit without amending the existing PR
   commit, push the current branch, and update draft PR #856.

## Compatibility

- The existing `mythic-edge-role-pool` package, invocation, installer behavior,
  R0 artifacts, and installed bytes remain unchanged.
- Existing `session-checkout` and `new-workcycle` skills remain installable and
  behavior-compatible.
- The new internal invocation name is distinct even though the display name is
  **Mythic Edge Role Pool**. UI metadata must disable implicit invocation so
  the display-name overlap cannot silently route work.
- Existing installer refusal, dry-run, and non-destructive copy semantics
  remain unchanged.
- Existing bare `Dispatch (A)` remains autonomous through F. New saved-run
  continuation is limited to exact-next-role segments under V2; no manual-work
  adoption, arbitrary-role entry, or V1 ledger migration is supported.

## Tests Required

Focused automated tests must cover:

- bare autonomous Dispatch, every new-run checkpoint `A-A`, `A-B`, `A-C`,
  `A-E`, and `A-F`, every aligned resume and single-role segment, and malformed
  syntax;
- unsupported roles/modes/options, repeated options, invalid combinations,
  out-of-allowlist repositories, normalization, one-to-three limits, immutable
  resume permissions, backward/repeated/skipped/D-inclusive/misaligned/post-F
  segments, and F-only permission compatibility;
- exact checkpoint stops, mixed completed/stopped lanes, summaries, artifact
  references, manual prompts, optional next-segment commands, and proof that no
  next-role agent launches;
- deterministic candidate ordering and manifest validation for dependency,
  anchor, WIP, authority compatibility, checkout identity, active work, and
  non-overlap evidence;
- post-A conflict stopping without backfill and unaffected-lane continuation;
- every allowed forward and stop transition plus every forbidden shortcut;
- exact `mythic_edge_issue_wave_reviewed_package.v1` canonicalization,
  including key encoding, UTF-8 path-byte order, add/modify/delete entries,
  explicit deletion object identity, executable and non-executable blob modes,
  raw byte lengths, and SHA-256 vectors;
- fail-closed rejection of duplicate/invalid paths, unknown keys, empty
  packages, unsupported statuses/modes/types, symlinks, gitlinks, unmerged or
  intent-to-add entries, malformed base/digests, and noncanonical entry order;
- `e_approved` succeeds with an uncommitted, empty-index C package and requires
  `review_base_commit` plus `reviewed_package_sha256`, while rejecting any
  pre-E `reviewed_commit`, `created_commit`, or submitted-package claim;
- F-only success in which F stages exactly the reviewed paths, the staged
  package binding matches before commit, F alone creates the single-parent
  commit, the commit package binding matches after commit, and `f_complete`
  stores `created_commit` plus equal `submitted_package_sha256` before push/PR
  completion is accepted;
- separate rejection cases for base, byte, added/deleted path, path order,
  status, executable mode, type, byte-length, SHA-256, extra/missing staged
  path, parent, and post-commit package drift, proving the lane reaches
  `d_required` without broad restaging, mismatch push, or PR creation;
- V2 schema versions, immutable segment history, segment authorization before
  role launch, exact next-role derivation, run-ID shape, target/state-root
  containment, expected revisions, duplicate JSON keys, unknown keys,
  hash-chain integrity, atomic snapshot projection, one-event crash recovery,
  stale state, permission drift, and unknown-outcome non-resumability;
- two genuinely simultaneous disjoint waves succeeding through serialized
  admission; same-repository, third-wave, target/worktree/state-root,
  issue-scope, and known submission-surface conflicts failing closed;
- a five-second bounded admission wait and race losers creating no worktree,
  branch, agent, GitHub effect, replacement, or backfilled lane;
- five-minute lease creation; renewal intervals no longer than 60 seconds while
  roles or CI are awaited; atomic renewal history; immediate checkpoint and
  terminal release; and preservation of all saved work and history;
- lease expiry producing zero deletion, retry, resume, authorization, release
  side effect, or repository mutation;
- recovery after mechanically verified task termination, explicit-user-
  confirmation fallback, refusal when termination remains uncertain, stable
  preserved-state revalidation, and safe checkpoint reacquisition;
- interrupted in-flight roles becoming `unknown_agent_outcome` without retry,
  plus manual advancement detection without adoption;
- field allowlisting, no-echo errors, public output path redaction, governance
  triggers, packet redaction, one-task aggregation, and task fallback;
- installer discovery, list/dry-run/install behavior for the new skill without
  changing existing skill behavior;
- legacy Role Pool tracked tree identity before and after implementation.

Source-loaded live Inspect must inspect current allowed repositories and record
the examined/excluded/selected evidence while proving zero local and GitHub
writes.

Synthetic Dispatch must use two simultaneous waves across six disposable local
Git repositories and local remotes, with PR and CI boundaries mocked. It must
cover:

- successful A through E with no commit, E approval of a canonical package,
  then F-only exact staging/commit/push/draft-PR progression and passing checks;
- A ambiguity;
- post-A overlap without backfill;
- an E finding routed to `d_required`;
- post-E package/base/mode/status/path drift and staged/commit binding mismatch
  routed to `d_required` without a mismatched push or PR;
- CI pass, failure, and 30-minute timeout;
- interrupted-run recovery and `unknown_agent_outcome` refusal;
- checkpoint release and exact-next-role continuation;
- concurrent disjoint success, overlap refusal, third-wave refusal, admission
  race loss, lease renewal/expiry, and manual drift without adoption;
- governance packet aggregation and task-creation fallback.

Required validation commands are selected from current repo tooling and must
include at least:

```text
py -m pytest tests/test_mythic_edge_issue_wave_skill.py -q
py -m pytest tests/test_install_codex_skills.py -q
py tools/install_codex_skills.py --list
py <skill-creator>/scripts/quick_validate.py docs/codex_skills/mythic-edge-issue-wave
py -m ruff check <changed Python files>
py tools/check_agent_docs.py
git diff --check
```

Broader adjacent tests and repo-required protected-surface/secret checks must
run according to the final changed-file set. Temporary test outputs must be
isolated and removed or left outside the repository; unrelated worktree
residue must be preserved.

## Acceptance Criteria

- Issue #855 remains the current Codex A authority and this file is the durable
  Codex B contract.
- `$mythic-edge-issue-wave` source validates and exposes exact Inspect and
  Dispatch behavior without implicit invocation.
- Bare Dispatch remains autonomous through F; explicit segments stop exactly
  at their requested checkpoint and exact-next-role resume records a new
  authorization before agent launch.
- Inspect produces useful candidate evidence and pasteable A prompts with zero
  writes.
- Dispatch instructions create fresh A/B/C/E/F native-agent waves and stop at
  every contracted ambiguity, D, unknown-outcome, and G boundary.
- Selection proves current dependencies, authority, checkout identity, WIP,
  active-work exclusion, and non-overlap, with deterministic ordering and no
  backfill.
- The helper is small, deterministic, network-free, agent-free, fail-closed,
  crash-aware, and limited to parsing/validation/local state transitions.
- Explicit resume cannot retry uncertain work or silently change permissions.
- At most two disjoint active or expired-unreleased waves and six associated
  lanes retain capacity in one canonical workspace; shared repositories, a
  third wave, or cross-run path/scope conflicts fail closed before repository
  effects.
- Every active reservation has a five-minute lease renewed no later than every
  60 seconds; checkpoint and terminal release are immediate and preserve all
  work and history.
- Lease expiry authorizes only recovery inspection. Recovery proves former
  task/agent termination and stable preserved state; uncertainty remains
  `unknown_agent_outcome` without automatic retry.
- Manual or external work is detected as drift and is never adopted or
  retrospectively certified into saved state.
- E can approve the exact uncommitted C package by canonical manifest SHA-256
  while F remains the sole staging, commit, push, and draft-PR owner.
- F proves the staged and committed packages both equal E's binding, records
  the F-created commit plus matching submitted binding at `f_complete`, and
  routes every base/byte/path/status/mode/type/package drift to `d_required`
  without broad restaging or mismatched submission.
- Governance feedback is material-triggered and redacted; checkpoints surface
  packets without creating H, while terminal completion aggregates once and
  routes to advisory Codex H without governance edits.
- Live read-only Inspect and all synthetic Dispatch scenarios pass.
- Focused, adjacent, lint, skill, docs, protected-surface, and secret checks
  pass or are explicitly classified with evidence.
- The legacy Role Pool tracked tree and R0-bound bytes match the pre-change
  baseline exactly.
- An independent Codex E report has no blocking findings.
- Codex F opens an independently reviewed draft PR for issue #855 and stops.
  No merge, installation, real Mythic Edge Dispatch, issue closure, deployment,
  or readiness claim occurs.

## Next Workflow Action

Next role: Codex C: Module Implementer.

```text
Act as fresh Mythic Edge Codex C for issue #855 on branch
agent/mythic-edge-issue-wave-855 and invoke $mythic-edge-workflow. Refresh
current repo authority, live issue #855, draft PR #856, accepted ADR-0008 and
ADR-0012, and docs/contracts/mythic_edge_issue_wave_skill.md. Implement only
the newly contracted checkpoint and two-wave revision: explicit A-A/A-B/A-C/
A-E/A-F checkpoints; exact-next-role saved-run segments; V2 invocation, run,
event, event-request, and Inspect schemas; two active disjoint waves; bounded
admission and cross-run isolation; five-minute leases renewed no later than 60
seconds; immediate checkpoint/terminal release with preserved work; fail-closed
expired-lease recovery requiring task/agent termination proof and stable-state
revalidation; unknown_agent_outcome with no automatic retry; no adoption of
manual work; and checkpoint/governance outputs. Preserve candidate-manifest
and reviewed-package V1 semantics, the E/F reviewed-package handshake, and
every legacy Role Pool/R0 byte.

Edit only the paths owned by this contract, update the implementation handoff,
and run the exact focused, simultaneous two-wave, lease/recovery, synthetic,
Inspect-zero-write, installer, Ruff, docs, protected-surface, secret, legacy-
identity, and diff checks required here. If safe behavior would require a
daemon, service, scheduler, database, custom agent controller, or cross-machine
coordinator, stop and route to A. Stop for fresh independent E without staging,
committing, pushing, updating PR #856, installing, performing a real Dispatch,
merging, deploying, or closing issue #855.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/mythic_edge_issue_wave_skill.md"
  target_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  validation:
    - "Contract reconciled to the refreshed issue #855 checkpoint, concurrency, lease, and recovery authority"
    - "Candidate-manifest and reviewed-package V1 semantics preserved"
    - "docs consistency checks"
    - "git diff --check"
  stop_conditions:
    - "contract or authority ambiguity"
    - "safe implementation requires a daemon, service, scheduler, database, custom controller, or cross-machine coordinator"
    - "legacy Role Pool or R0-bound byte change"
    - "staging, commit, push, PR update, real Dispatch, installation, G work, merge, deployment, or issue closure"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high workflow risk"
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
    - "workflow coordination and native subagent dispatch"
    - "Git branches, worktrees, commits, pushes, and draft pull requests"
    - "local resumable run state"
    - "legacy Role Pool and R0-bound files (explicitly forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #855 records the explicit ADR-0008 override and fixes the checkpoint grammar, two-wave limit, disjoint-repository rule, renewable lease, recovery proof, and manual-continuation boundary. No daemon or cross-machine enforcement is authorized or required."
  stop_conditions:
    - "the V2 transition, lease, or recovery contract remains ambiguous"
    - "implementation requires scope outside the contract-owned paths"
    - "legacy or R0 boundary cannot be proven unchanged"
```
