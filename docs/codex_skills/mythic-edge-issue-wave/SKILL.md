---
name: mythic-edge-issue-wave
description: Inspect up to three dependency-safe Mythic Edge issue lanes or, when explicitly asked to Dispatch, coordinate checkpointed fresh native Codex A through F role waves with isolated worktrees, two-wave reservations, renewable leases, recovery state, draft PRs, and a stop before G. Use for explicit $mythic-edge-issue-wave Inspect or Dispatch invocations; never use implicitly or as a replacement for the legacy mythic-edge-role-pool skill.
---

# Mythic Edge Issue Wave

Coordinate a bounded issue wave while keeping current GitHub and repository
authority above local state and model judgment. Keep the active root Codex in
charge. Never delegate GitHub or Git inspection, candidate selection, scope
judgment, agent creation, artifact acceptance, or consequential transitions to
the bundled helper.

## Load The Protocol

Read [references/controller-protocol.md](references/controller-protocol.md) in
full for every invocation. For Dispatch, resume, or ledger inspection, also
read [references/state-schema.md](references/state-schema.md) in full before
using the helper.

Invoke the helper only through these operations:

```text
py -B scripts/issue_wave_state.py parse <invocation>
py -B scripts/issue_wave_state.py bind-package --manifest <reviewed-package.json>
py -B scripts/issue_wave_state.py init ...
py -B scripts/issue_wave_state.py transition ...
py -B scripts/issue_wave_state.py renew-lease ...
py -B scripts/issue_wave_state.py release ...
py -B scripts/issue_wave_state.py authorize-segment ...
py -B scripts/issue_wave_state.py recover ...
py -B scripts/issue_wave_state.py inspect ...
```

The helper is deterministic, local, and network-free. It parses syntax,
validates root-supplied manifests, issues run identifiers, validates
transitions, and records or inspects local state. It does not inspect Git or
GitHub, rank or select issues, create branches or agents, invoke roles, retry
work, create PRs, poll CI, or decide authority.

## Accept Only The Public Grammar

Accept only:

```text
$mythic-edge-issue-wave <Inspect|Dispatch> (<role-or-segment>[; option ...])
```

Options are `repos=`, `anchor=`, `run=`, `allow-main-draft`, and
`allow-wip-exception` as defined in the controller protocol. Inspect accepts
only `A`; bare Dispatch `A` remains autonomous through F. New-run checkpoints
are exactly `A-A`, `A-B`, `A-C`, `A-E`, and `A-F`. Saved-run segments begin
at the exact next role. Fail closed on backward, skipped, D-inclusive,
misaligned, or malformed segments without echoing unsafe input.

## Inspect

Treat Inspect as mechanically zero-write.

1. Parse the invocation without writing.
2. Resolve the explicitly selected repositories, or the fixed allowlist, and
   refresh current read-only GitHub and Git evidence.
3. Read each repository's current authority before judging it compatible.
4. Record every issue actually considered with one explicit eligibility or
   exclusion reason.
5. Prove prerequisites, WIP compatibility, exact checkout identity, absence of
   active duplicate work, and pairwise lane separation.
6. Apply `anchor=` only to durable dependency, child, tracker, roadmap, or
   explicit next-role edges. Reject textual similarity as evidence.
7. Rank authority-backed candidates first; then sort equal ranks by oldest
   creation time, canonical repository name, and issue number.
8. Select zero to three lanes, never more than one issue per repository.
9. Return the evidence and one directly pasteable `$mythic-edge-workflow`
   Codex A prompt per selected candidate.

For `Inspect (A; run=...)`, validate the ledger and compare it with current
read-only evidence. Report drift and mechanically possible next states, but do
not lock, repair, append, reconcile, touch, or resume the run.

Before and after a source-loaded Inspect validation, compare repository status,
the external workspace path set, and current GitHub issue/PR metadata. Do not
install this skill for validation.

## Dispatch

Dispatch is allowed only by an explicit Dispatch invocation plus current
issue-scoped authority for every planned effect.

1. Complete the same read-only selection as Inspect.
2. Revalidate all selected issues, repositories, checkouts, heads, WIP state,
   dependencies, and scopes immediately before any write.
3. Build a redacted, deterministically ordered manifest. Prove that the state
   root and every target checkout are pairwise non-overlapping. Initialize its
   ledger outside every target repository only after all preconditions pass;
   one state-root admission lock must cover scanning through atomic run
   publication. Admit at most two active waves with disjoint repository sets;
   reject cross-run scope/path overlap before any repository effect.
4. Create one isolated branch and worktree per accepted lane. Never clone,
   clean, stash, reset, or delete.
5. Create up to three fresh native Codex A subagents in parallel. Give each a
   self-contained public-safe packet and require `$mythic-edge-workflow` plus
   that repository's current authority.
6. Verify each durable A artifact. Recompare exact files and path families,
   interfaces, truth owners, dependencies, shared artifacts, schemas, and
   submission lanes. Stop conflicting lanes without replacement or backfill;
   continue unaffected lanes only when their shared evidence remains valid.
7. For each continuing lane, create a fresh B, then fresh C, then independent
   fresh E, then fresh F agent. Never reuse an agent as the next role.
8. Verify every role artifact and append a transition only after the durable
   outcome is proven. Renew the five-minute lease no later than every 60
   seconds, including while waiting for agents or CI. Revalidate before each
   role and external write.
9. For E, require lane `HEAD` to remain the review base, require an empty real
   index, construct the complete canonical
   `mythic_edge_issue_wave_reviewed_package.v1` manifest from root-observed
    bytes and modes, and use `bind-package` to record only
   `review_base_commit` plus `reviewed_package_sha256`. E creates no commit,
   and neither `draft_pr` nor `checks` may be claimed before its owning
   transition.
10. Before F, reconstruct and rebind that complete package. On any base, path,
    status, mode, type, byte-length, byte-hash, set, order, index, or package
    drift, route to `d_required` without launching or repairing F. F alone
    stages the exact manifest paths, proves the staged package, creates one
    commit whose sole parent is the review base, proves the committed package,
    then pushes and creates one draft PR. At `f_complete`, require F's event to
    record `created_commit`, an equal `submitted_package_sha256`, the exact
    already-bound issue branch, and a newly supplied positive `draft_pr`.
    Those submission fields are immutable afterward. F makes no implementation
    edit, broad restage, amend, reset, or replacement commit.
11. Poll required checks for no more than 30 minutes. Record `checks` only on
    its owning transition: `running` when polling starts, `passed` for
    `g_consideration_ready`, `failed` for `d_required`, or `pending` for
    `checks_pending`. Reject pre-F and mismatched check claims.
12. Stop before D and G. Return a pasteable D or G prompt only when the saved
    state and current evidence permit it.

For an explicit segment, stop after every unaffected lane reaches its endpoint
or a defined stop. Release the reservation, preserve all work and history, and
do not launch the next role. Return concise summaries, exact public-safe
artifact references, validation, a manual prompt, and the aligned next-segment
command.

If an agent or external write has an uncertain outcome, reconcile read-only
first. If the exact outcome remains unknown, record
`unknown_agent_outcome`; never repeat the action or resume that lane.

## Resume

Resume only through an explicit `run=` invocation. Validate the saved hash
chain and projection, then refresh live issue, PR, check, head, worktree,
artifact, reviewed/submitted package binding, role-outcome, and permission evidence. Omitted permission flags keep
the saved immutable values; an explicitly repeated flag must already be true
in the run. Reacquire capacity and record a segment authorization before the
next agent starts. Detect manual advancement as drift and never adopt it.

Lease expiry authorizes recovery inspection only. Prove the former parent task
and all agents stopped, then prove preserved state is stable and inactive;
repository inactivity alone is insufficient. An in-flight role becomes
`unknown_agent_outcome` and is never automatically retried or resumed.

## Governance Feedback

Treat only A ambiguity, incompatible or conflicting authority, an unsafe rule
gap, repeated mechanically identical inefficiency, or a systemic multi-lane
failure as material friction. Store only validated redacted packets.

At run completion, aggregate all material packets once. The root creates one
separate read-only Mythic Edge task using
`$mythic-edge-constitutional-lawyer`. If task creation is unavailable, return
the helper's equivalent pasteable prompt. Create no task when packet count is
zero. Codex H remains advisory and edits no authority.

## Non-Negotiable Stops

Never:

- modify or invoke the legacy `mythic-edge-role-pool` package or any R0-bound
  controller, validator, profile, registry, release, receipt, or test;
- treat the helper, local ledger, prompt, model output, or subagent output as
  repository, issue, parser, schema, review, merge, or deployment truth;
- perform a real Dispatch without a fresh explicit invocation and current
  authority;
- clone a missing checkout, backfill a stopped lane, retry an unknown outcome,
  rerun CI, or run unattended;
- include local absolute paths, secrets, complete issue bodies, private
  transcripts, raw logs, runtime data, generated datasets, workbook exports,
  webhook URLs, or command output in public artifacts;
- install the skill, merge, deploy, mark a PR ready, close an issue, alter
  credentials, invoke webhooks, or start runtime or production work.

Passing tests, E approval, a draft PR, passing checks, and
`g_consideration_ready` are prerequisite evidence only. They create no G,
merge, deployment, installation, release, production, or later-Dispatch
authority.
