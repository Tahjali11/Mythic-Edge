# Controller Protocol

## Contents

- Root authority boundary
- Invocation and allowlist
- Checkout-family inventory
- Inspect protocol
- Candidate manifest protocol
- Dispatch role waves
- Stop and recovery rules
- Governance feedback
- Required output

## Root Authority Boundary

Keep the active root Codex responsible for:

- current GitHub inspection and interpretation of local Git evidence;
- authoritative issue/worktree binding;
- authority, dependency, WIP, eligibility, ranking, and overlap judgment;
- native subagent creation and self-contained role packets;
- branch, worktree, commit, push, draft-PR, and check operations;
- artifact, test, and role-outcome acceptance;
- every state transition and all A/B/D/E/F/G routing decisions.

Use the helper's `inventory-checkouts` operation only for the closed local Git
facts it reads. For every other operation, use the helper only after the root
has supplied the facts it validates. Helper acceptance proves mechanical Git,
schema, or transition consistency, not issue identity, active-work status,
eligibility, authority, or the truth of root-supplied facts.

## Invocation And Allowlist

The preferred public grammar is:

```text
mythicedgeissuewave <Inspect|Dispatch> (<role-or-segment>;[ option ...])
```

Continue to accept `$mythic-edge-issue-wave` as the backward-compatible
command token. A lone no-option terminator such as `(A;)` or `(A-B;)` is
valid. A doubled semicolon, empty option, or trailing semicolon after an option
is invalid. Skill discovery from the exact preferred token loads instructions
only; it performs no action and grants no authority.

Inspect accepts only `A`. Bare Dispatch `A` is autonomous through F. New-run
segments are exactly `A-A`, `A-B`, `A-C`, `A-E`, and `A-F`. Saved-run
segments begin at the exact next role and end at that role or a later
normal-path role; aligned `B-B`, `C-C`, `E-E`, and `F-F` are valid. D is not a
selectable role. Ignore outer whitespace and whitespace around semicolons;
treat command tokens, modes, roles, option names, and punctuation as exact.

Allowed options:

- `repos=repo-ref[,repo-ref...]`: one to three unique allowlisted repos;
- `anchor=repo-ref#number`: one allowlisted repo and positive issue;
- `run=YYYYMMDDTHHMMSSZ-8hex`: inspect or resume one existing run;
- `allow-main-draft`: Dispatch only and only when the segment contains F;
- `allow-wip-exception`: new Dispatch run only.

Do not combine `run=` with `repos=` or `anchor=`. Inspect accepts no permission
flag. A resume may omit saved flags or repeat only `allow-main-draft` when it
was already saved as true; it cannot add or reduce permission.

The fixed allowlist is:

1. `Tahjali11/Mythic-Edge`
2. `Tahjali11/Mythic-Edge-Analytics`
3. `Tahjali11/Mythic-Edge-Fable-Engine`
4. `Tahjali11/Mythic-Edge-Corpus`
5. `Tahjali11/Mythic-Edge-Automation-Artifacts`
6. `Tahjali11/Mythic-Edge-Security`
7. `Tahjali11/Mythic-Edge-Feature-Expansions`
8. `Tahjali11/Mythic-Edge-Research-and-Development`
9. `Tahjali11/Mythic-Edge-Application-Function`
10. `Tahjali11/Mythic-Edge-Governance`

Match case-insensitively and emit the spelling above. With `repos=`, inspect
only that normalized set and never fill from an excluded repository.

A public `repo-ref` may be the canonical `owner/repo`, the full repository
name, or the exact suffix after `Mythic-Edge-`. The root repository has no
suffix alias and accepts only `Tahjali11/Mythic-Edge` or `Mythic-Edge`.
Short aliases are `Analytics`, `Fable-Engine`, `Corpus`,
`Automation-Artifacts`, `Security`, `Feature-Expansions`,
`Research-and-Development`, `Application-Function`, and `Governance`.
Normalize before uniqueness checks, so two aliases for one repository are a
duplicate. Internal manifests and saved state retain canonical identities and
do not accept aliases.

## Checkout-Family Inventory

Run exactly:

```text
py -B scripts/issue_wave_state.py inventory-checkouts \
  --workspace-root <coordinator-resolved-root> \
  --repository <canonical> [--repository <canonical> ...]
```

This is an internal operation. Add no invocation option for a checkout path
and keep no persistent local checkout map. The helper examines only Git
folders directly beneath the supplied workspace root. For a matched Git common
directory, it includes Git's registered primary worktree and every registered
linked worktree, even when a linked worktree is outside the workspace. It does
not search outside the workspace for independent clones.

Exactly one common directory is one usable checkout family. Two common
directories are independent clones and remain
`checkout_unavailable_or_ambiguous`, even if their remotes match and both are
clean. A fetch/push mismatch, missing checkout, bounded Git failure, or
internally inconsistent family also fails closed.

The operation uses only its contracted read-only Git allowlist with an exact
command-local `safe.directory` value for the inspected path, optional locks
disabled, terminal prompts disabled, ambient Git state removed, and global and
system configuration ignored. Origin evidence comes only from the inspected
checkout's local configuration. It never changes global Git config, fetches,
prunes, repairs, checks out, cleans, writes, or contacts a remote. Do not expose
raw remote URLs, command output, or credentials.

Consume `mythic_edge_issue_wave_checkout_inventory.v1` in memory. Never add it
to a saved-run schema, ledger, public packet, or handoff. Missing or prunable
registrations are warnings and are never cleaned up. Block on one only when
current run authority still depends on that registration.

## Inspect Protocol

Keep a read ledger in the response, not on disk. For each selected repository:

1. Verify the GitHub repository identity.
2. Require exactly one checkout family from the ephemeral inventory.
3. Read current `AGENTS.md`, workflow rules, role conventions, accepted ADRs,
   active issues/contracts/handoffs, and current branch/worktree/PR state.
4. Query only current public issue, PR, review, and check metadata needed for
   candidate judgment.
5. Bind active worktrees only through current open PR/issue linkage, a
   non-final issue-wave ledger, or a current contract/handoff tied to an open
   issue. Branch and folder issue numbers are query hints only.
6. When exactly one issue is bound, exclude only that exact issue from the
   duplicate-work gate. A clean historical worktree with no current
   active-work evidence is ignored. Dirty, ahead, in-progress, or open-PR
   work without exactly one authoritative issue binding blocks the repository.
7. Record every issue actually considered and one exclusion or admission
   reason.

Admit a candidate only when current evidence proves:

- open and not deferred, parked, duplicate, superseded, or represented by
  active conflicting work after exact-issue exclusion;
- every declared prerequisite is durably complete and the relationship is
  unambiguous;
- compatible repository-local A through F authority and durable artifact
  conventions exist;
- exactly one checkout family matches the repository;
- WIP-1 passes, or both the invocation and current issue-scoped authority
  permit the saved exception;
- all material scope dimensions are known and do not conflict with another
  selected lane.

Issue binding changes only duplicate-work detection. Every unrelated issue
still faces its independent prerequisite, WIP-1, authority, dependency, and
scope gates. An active worktree for issue X excludes X only; issue Y is
evaluated normally. If binding remains ambiguous, block the repository before
selecting either issue. A branch name or folder name never supplies the
missing authority.

Compare exact files and path families, public interfaces, truth ownership,
dependencies, shared artifacts, schema/protected surfaces, and submission
lanes. Absence or ambiguity excludes or stops; it is not permission to infer.

Treat `anchor=` as a strict filter. Require a durable dependency, child issue,
tracker, roadmap, or explicit next-role edge. Similar wording is insufficient.

Rank tracker-, roadmap-, and next-role-backed candidates together before other
candidates. Within a rank, order oldest issue creation time first, then
canonical repository name, then numeric issue. Select at most three and at
most one per repo.

## Candidate Manifest Protocol

Create the manifest only for a new Dispatch after read-only admission. Use the
schema in `state-schema.md`. Supply public-safe summaries, globally qualified
scope tokens, exact checkout roots, and candidates already in deterministic
order. The helper rejects unknown fields, eligibility falsehoods, scope token
collisions, unsafe state placement, pairwise duplicate or nested target roots,
and multiple lanes from one repo.

Keep the workspace state root outside and non-overlapping with every target
checkout and worktree:

```text
<workspace>/.codex/role-pool-runs/<run-id>/
```

Do not initialize a run when selection is empty or when any precondition is
unresolved. One state-root admission lock waits at most five seconds and
serializes inspection through atomic reservation and run publication. Permit
at most two active waves, six lanes, and disjoint active repository sets.
Reject cross-run scope, submission-surface, checkout, target, state-root, or
worktree overlap. A race loser stops before repository effects and is not
backfilled. Never delete a persistent lock. Every new worktree remains outside
and non-overlapping with the state root and active-run paths.

## Dispatch Role Waves

Immediately before writes, refresh every selected issue, checkout, head,
active lane, permission, dependency, and scope. Create no partial wave when
shared selection evidence is invalid.

For each accepted lane, create an isolated issue branch and worktree without
cleaning or altering existing state. Then follow:

```text
A wave -> root scope comparison -> B wave -> C wave -> independent E wave
       -> F wave -> bounded required-check polling -> stop before G
```

Use at most three concurrent child agents. Give each agent only its lane's
public-safe current packet:

- repository identity and operating checkout/worktree;
- issue, role, risk, current authority, and source/target artifacts;
- exact allowed and forbidden files/effects;
- verified facts, material unknowns, validation, and stop conditions;
- requirement to invoke `$mythic-edge-workflow` and write only its authorized
  durable artifact.

Use a fresh agent for every A, B, C, E, and F turn. The root verifies the
durable artifact and current bytes before accepting completion. Chat output
alone is not a completed role.

For explicit segments, stop at the inclusive endpoint. Wait until every
unaffected lane reaches that endpoint or a defined stop, append the checkpoint
release, preserve all work/history, and do not launch the next role. Renew the
five-minute reservation lease no later than 60 seconds after issue or renewal,
including during role and CI waits. No lane transition is accepted after that
renewal deadline or lease expiry.

After A, compare all exact scopes again. Stop the affected conflicting lanes;
do not replace them. Continue another lane only when the conflict did not
invalidate its dependency or shared evidence.

Before B, C, E, F, and each external write, revalidate current authority and
the completed boundary. Route framing or contract errors backward. Route a
concrete C/E/F/test/CI defect to `d_required`; never launch D automatically.

E reviews an exact uncommitted package. The root requires `HEAD` to equal the
review base, the real index to be empty, and the manifest to cover every
non-ignored changed path. The root passes that strict
`mythic_edge_issue_wave_reviewed_package.v1` manifest to `bind-package`; E
approval records only `review_base_commit` and `reviewed_package_sha256` plus
E evidence. `draft_pr` and `checks` remain null. E never stages, commits,
pushes, or creates a PR.

Before F, the root reconstructs the complete worktree package and binding.
Any base, path, set, order, status, mode, type, byte-length, byte-hash, index,
or package drift routes to `d_required` without launching or repairing F. F
receives the exact reviewed paths and binding. F alone stages only those paths,
rebinds the staged package, creates one commit with the review base as its sole
parent, rebinds the committed package, and only then pushes and opens one draft
PR. `f_complete` records `created_commit` and a
`submitted_package_sha256` equal to E's binding, explicitly reasserts the exact
issue branch bound at A, and newly records one positive draft-PR reference.
The branch and draft PR are immutable afterward. F makes no implementation
edit, broad restage, amend, reset, or replacement commit. Poll required checks
for at most 30 minutes. The event starting polling must newly record `running`;
each terminal check transition must newly record exactly `passed`, `failed`, or
`pending` for its destination. No earlier transition may claim check evidence.
Never rerun checks.

## Stop And Recovery Rules

Use only the states in `state-schema.md`. Never append a transition before the
durable outcome exists. A helper-valid transition is not evidence that the
role actually completed.

When agent outcome is uncertain, inspect durable artifacts and external state
read-only. If the exact result cannot be proven, use
`unknown_agent_outcome`. Do not retry or resume that lane.

When an external write is uncertain, reconcile the branch, commit, comment,
task, or PR read-only before any repeat. If still unknown, stop.

Resume only a mechanically complete released checkpoint. Reacquire capacity
and record the exact aligned segment authorization before agent launch, after
revalidating current heads, artifacts, worktrees, role outcomes, every
reviewed/submitted package binding, live GitHub state, immutable permissions,
and cross-run reservations. Supply a closed per-lane proof of exact expected
and observed repository heads and durable artifact SHA-256 identities; the
helper binds its canonical digest into the event and segment history. Manual
or external advancement is drift, not an
adoptable role outcome. A missing or ambiguous checkout uses
`checkout_unavailable_or_ambiguous`; incompatible authority uses
`incompatible_repository_authority`; scope uncertainty uses
`unsafe_or_conflicting_scope`.

Lease expiry performs no mutation and grants recovery-inspection eligibility
only. Prove the former parent task and every agent stopped through task state,
or require explicit user confirmation; repository inactivity alone is not
proof. Then prove preserved branches, worktrees, artifacts, heads, event chain,
and operation markers are stable and inactive. An in-flight role becomes
`unknown_agent_outcome`, is never retried/resumed, and releases capacity only
after this inspection. A durably complete checkpoint may be released and
later reacquired; no expired run is automatically resumed.

## Governance Feedback

Ask the affected role for one redacted packet only for:

- A ambiguity;
- authority conflict;
- unsafe governance-rule gap;
- repeated inefficiency with one mechanically identifiable cause;
- systemic failure across lanes or roles.

Ordinary exclusion is not material friction. Validate packet identifiers and
public-safe text before recording it. At a checkpoint, surface packets without
creating a task. At terminal completion, aggregate all packets and
ask for exactly one read-only Codex H task. If task creation is unavailable,
return one pasteable fallback prompt. Never let the helper or a background
process create the task.

## Required Output

For Inspect, return repositories/issues examined, every exclusion, selected
candidates in deterministic order, current evidence for every admission
predicate, and one pasteable A prompt per lane. Distinguish checkout identity,
the exact active issue excluded as duplicate work, WIP-1 incompatibility,
prerequisites and dependencies, authority, and scope conflicts. Zero selected
lanes is valid when those gates genuinely exclude everything. Explicitly state
that no local or GitHub write occurred.

For Dispatch, return per lane:

- canonical repository and issue;
- last completed role and durable artifacts;
- review base, reviewed-package binding, F-created commit,
  submitted-package binding, branch, draft PR, and checks when available;
- exact state or stop reason;
- validation and remaining unknowns;
- one public-safe pasteable next-role prompt and aligned saved-run command only
  for a released safe checkpoint with an exact next role.

Do not publish local absolute paths. End a successful lane at
`g_consideration_ready` with a G consideration prompt, not a readiness or
merge claim.
