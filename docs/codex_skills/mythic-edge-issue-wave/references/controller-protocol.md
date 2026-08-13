# Controller Protocol

## Contents

- Root authority boundary
- Invocation and allowlist
- Inspect protocol
- Candidate manifest protocol
- Dispatch role waves
- Stop and recovery rules
- Governance feedback
- Required output

## Root Authority Boundary

Keep the active root Codex responsible for:

- current repository and GitHub inspection;
- authority, dependency, WIP, eligibility, ranking, and overlap judgment;
- native subagent creation and self-contained role packets;
- branch, worktree, commit, push, draft-PR, and check operations;
- artifact, test, and role-outcome acceptance;
- every state transition and all A/B/D/E/F/G routing decisions.

Use the helper only after the root has supplied the facts it validates. Helper
acceptance proves schema and transition consistency, not the truth of supplied
facts.

## Invocation And Allowlist

The only entry role is `A`. Ignore outer whitespace and whitespace around
semicolons. Treat modes, roles, option names, and punctuation as exact.

Allowed options:

- `repos=owner/repo[,owner/repo...]`: one to three unique allowlisted repos;
- `anchor=owner/repo#number`: one allowlisted repo and positive issue;
- `run=YYYYMMDDTHHMMSSZ-8hex`: inspect or resume one existing run;
- `allow-main-draft`: Dispatch only;
- `allow-wip-exception`: Dispatch only.

Do not combine `run=` with `repos=` or `anchor=`. Inspect accepts no permission
flag. A resume may omit saved flags or repeat only a flag already saved as
true; it cannot add or reduce permission.

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

## Inspect Protocol

Keep a read ledger in the response, not on disk. For each selected repository:

1. Verify the GitHub repository identity.
2. Match exactly one local checkout by normalized fetch/push remote identity.
3. Read current `AGENTS.md`, workflow rules, role conventions, accepted ADRs,
   active issues/contracts/handoffs, and current branch/worktree/PR state.
4. Query only current public issue, PR, review, and check metadata needed for
   candidate judgment.
5. Record every issue actually considered and one exclusion or admission
   reason.

Admit a candidate only when current evidence proves:

- open and not deferred, parked, duplicate, superseded, or represented by
  active conflicting work;
- every declared prerequisite is durably complete and the relationship is
  unambiguous;
- compatible repository-local A through F authority and durable artifact
  conventions exist;
- exactly one checkout matches the repository;
- WIP-1 passes, or both the invocation and current issue-scoped authority
  permit the saved exception;
- all material scope dimensions are known and do not conflict with another
  selected lane.

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
unresolved. One state-root admission lock must serialize duplicate-active-lane
inspection through atomic publication of the complete run directory. Treat an
existing or stale lock as `state_locked`; do not delete, recover, or retry it.
Every new worktree must be outside and non-overlapping with the state root, all
target checkouts, and every recorded worktree.

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

Resume only a mechanically complete boundary after revalidating current heads,
artifacts, worktrees, role outcomes, every reviewed/submitted package binding,
live GitHub state, and immutable permissions. A missing or ambiguous checkout uses
`checkout_unavailable_or_ambiguous`; incompatible authority uses
`incompatible_repository_authority`; scope uncertainty uses
`unsafe_or_conflicting_scope`.

## Governance Feedback

Ask the affected role for one redacted packet only for:

- A ambiguity;
- authority conflict;
- unsafe governance-rule gap;
- repeated inefficiency with one mechanically identifiable cause;
- systemic failure across lanes or roles.

Ordinary exclusion is not material friction. Validate packet identifiers and
public-safe text before recording it. At completion, aggregate all packets and
ask for exactly one read-only Codex H task. If task creation is unavailable,
return one pasteable fallback prompt. Never let the helper or a background
process create the task.

## Required Output

For Inspect, return repositories/issues examined, every exclusion, selected
candidates in deterministic order, current evidence for every admission
predicate, and one pasteable A prompt per lane. Explicitly state that no local
or GitHub write occurred.

For Dispatch, return per lane:

- canonical repository and issue;
- last completed role and durable artifacts;
- review base, reviewed-package binding, F-created commit,
  submitted-package binding, branch, draft PR, and checks when available;
- exact state or stop reason;
- validation and remaining unknowns;
- one public-safe pasteable next-role prompt only when mechanically allowed.

Do not publish local absolute paths. End a successful lane at
`g_consideration_ready` with a G consideration prompt, not a readiness or
merge claim.
