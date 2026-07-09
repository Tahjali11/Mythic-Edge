# Codex Module Workflow

This document is the operating guide for moving one coherent Mythic Edge unit
of work from problem framing to reviewed integration. It does not replace
`AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, accepted
ADRs, active issues, contracts, reviews, PRs, or tests. It explains how those
sources should be sequenced by the Codex A-G workflow.

Start every non-trivial thread by reading the current repo guidance:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- this workflow file
- the active role file under `docs/agent_threads/`
- the relevant template under `docs/templates/`
- accepted ADRs under `docs/decisions/` when they apply

The durable artifact is the source of workflow truth. Chat summaries and
pasteable prompts help the next thread start quickly, but they do not outrank
the issue, contract, handoff, review, PR, GitHub state, branch state, or repo
docs.

## Intake And Authority

Before activating non-trivial work, identify the repository, branch, active
issue or lane, intended base branch, risk tier, and protected surfaces. Mythic
Edge repositories default to one active issue or lane at a time. A second lane
requires a named, scoped, expiring exception such as `security_hotfix`,
`privacy_or_raw_log_leak`, `data_loss_or_corruption`, `ci_blocking_all_work`,
`dependency_security_update`, `blocked_lane_unblocker`,
`repo_bootstrap_or_split`, or `explicit_user_override`.

The active slot is owned by the repository, not by a local worktree name. Live
GitHub issues, PRs, branch heads, merge commits, current contracts, accepted
ADRs, and governance docs outrank stale prompts, local status indexes, parked
notes, local skills, chat memory, and ambiguous handoffs. If repo identity,
remote URL, active lane, or authorization is unclear, stop before mutating
files, staging, committing, pushing, cleaning, resetting, stashing, or deleting.

## Truth And Protected Surfaces

The parser and state layer own MTGA event interpretation and normalized
match/game facts. Webhook transport, Apps Script, workbook landing sheets,
helper formulas, dashboards, public reports, and AI or analytics notes are
downstream unless an issue and contract explicitly move responsibility.

External tools, MCP servers, plugins, connectors, browser helpers, shell
helpers, GitHub connectors, Google Docs, Google Sheets, OpenAI documentation
tooling, and local skills are access or collaboration surfaces. They do not own
project truth or repo authority by default.

Protected surfaces require explicit issue and contract authority before
behavior changes: parser event classes, extractors, parser state, final
reconciliation, match identity, game identity, deduplication, result fields,
play/draw, mulligans, opening-hand facts, deck submission facts, webhook
payload shape, workbook schema, Apps Script behavior, deployed workbook
assumptions, secrets, credentials, environment contracts, raw logs, runtime
status files, failed posts, generated data, workbook exports, and private
evidence.

## Thread Roles

Every non-trivial thread declares one active role.

Codex A: Thinker frames the problem, scope, risk tier, first inspection order,
expected artifact, and whether a GitHub issue or problem representation is
needed. A does not implement code.

Codex B: Module Contract Writer turns approved framing into a contract. B owns
interfaces, invariants, truth boundaries, side effects, tests, acceptance
criteria, and unknowns. B does not implement behavior changes.

Codex C: Module Implementer compares current code to the contract, makes the
smallest coherent implementation, updates focused tests, and writes an
implementation handoff. C does not commit unless explicitly asked.

Codex D: Module Fixer is only a loopback role for concrete reviewer, test, CI,
or user findings. D fixes the named defect, routes to B if the contract is
wrong, and routes to A if the finding changes scope.

Codex E: Module Reviewer or Contract Tester reviews with fresh context against
the issue, contract, handoff, diff, and tests. Findings lead, ordered by
severity. E does not silently fix code in review-only mode.

Codex F: Module Submitter stages reviewed files only, commits, pushes, and
opens or updates a draft PR to the approved base branch. F does not merge PRs,
close issues, or mark trackers complete.

Codex G: Integration Deployer runs only when the user asks for deployer, merge,
closeout, or integration work. G verifies merge gates, marks PRs ready when
appropriate, merges into an approved base, closes completed issues, updates
trackers, records completion evidence, and performs checkout reconciliation.

Codex H: Constitutional Lawyer is an auxiliary governance role. H synthesizes
constitution feedback packets into amendment proposals, consolidations,
unresolved conflicts, and watch-list items. H does not directly rewrite
authority docs or replace the normal A-G workflow.

## Normal Path And Loopbacks

```text
A Thinker -> B Module Contract Writer -> C Module Implementer -> E Module Reviewer -> F Module Submitter -> G Integration Deployer
```

Route to A when scope is wrong, a new issue is needed, a different layer owns
the problem, or current framing would cause drift.

Route to B when expected behavior, vocabulary, public interface, acceptance
criteria, downstream truth ownership, or contract authority is ambiguous or
wrong.

Route to D when E, CI, tests, or the user identifies a concrete fixable defect
inside reviewed scope.

Route to E when implementation or fixer work is ready for independent
contract verification.

Route to F only when review has no blocking findings and validation is present
or explicitly explained.

Route to G only when a draft PR is ready for merge consideration and the user
asks for deployer or merge work.

Use H only for governance synthesis. H output usually routes back to A or B.
It may route to C only when an existing issue and contract already authorize
implementation.

## Handoffs

Every continuing thread must produce a durable artifact, a pasteable
next-thread prompt, and a machine-readable `workflow_handoff` block. Use
`docs/templates/workflow_handoff.md` for the block shape.

The exact phrase `pasteable next-thread prompt` is intentional: the next role
should be able to continue from the artifact without reconstructing context
from chat history. Keep the prompt concise, but include enough repo, issue,
role, artifact, branch, validation, stop-condition, and routing detail that a
fresh Codex thread can verify its footing before it reads or edits anything.

Medium-risk and high-risk work must also include an `instruction_context`
block in the durable artifact or continuation handoff. It records the authority
sources read, active role, risk tier, protected surfaces, authority conflicts,
and stop conditions. It is orientation evidence, not a new authority source.
Low-risk work may defer it when the change is obvious, local, reversible, and
outside protected surfaces.

Public handoffs should include `repository` and `repository_url`; `base_branch`
for the branch work starts from or compares against; `target_branch` for the
future PR or deployer target; and `branch` for the working branch when useful.
Local absolute paths belong only in private/local prompts as an
`Operating repo/worktree:` hint, not in public `workflow_handoff` blocks.
If a checkout remote cannot be verified against `repository_url`, or a sibling
repository lacks `allowed_read_only_references`, hard stop before reading
outside approved scope or mutating content.

When Codex E routes work back to D, E must leave a durable blocker packet. Use
a GitHub issue or PR comment when that lane already uses comments; otherwise
use a contract-test report, review artifact, or handoff. Include finding ID,
severity, blocking status, affected file/function or section, expected
behavior, actual behavior, evidence or failing check, why the route is D
instead of A or B, exact fix boundary, validation D should run, pasteable D
prompt, and `workflow_handoff`.

## Issue And PR Lifecycle

Use one GitHub issue per coherent module or workflow change. Link contracts,
handoffs, reports, PRs, trackers, and related ADRs when relevant. Trackers
stay open until the tracked queue or phase is complete; one child issue
finishing is not enough to close a tracker.

Module audit issues close only after required artifacts exist, review is clean
or accepted, PR work is merged into the approved base, validation or CI is
recorded, and tracker state is updated when applicable. Bug issues close after
the fix PR is merged, validation is recorded, and no follow-up implementation
is implied. Planning or docs issues close when requested artifacts are
complete or linked follow-up implementation exists. Constitution issues close
when rule changes are merged, affected role docs/templates/skills are updated
if needed, validation is recorded, and no amendment work remains.

PRs default to draft. Parser audit PRs target `codex/parser-module-audit-suite`
unless the issue or tracker names another non-production base. Do not target
`main` unless explicitly approved. Use `Closes #...` only when the PR fully
satisfies the issue; use `Refs #...` for partial, planning-only, contract-only,
tracker, or follow-up work.

Codex F may submit a PR only after review has no blocking findings and
validation is present or explained. Codex G may merge only after the user asks
for deployer or merge work and the gates pass: PR not draft, base approved, CI
passed or named failures waived, review clean, diff within reviewed scope, no
forbidden files or secrets, and issue/tracker behavior correct.

After merge, G records PR number, merge commit, base branch, artifacts,
validation or CI result, tracker status, source branch disposition, preserved
changes, unresolved residue, and next workflow step.

## Codex G Checkout Reconciliation

Whenever Codex G runs, it must reconcile checkout state before final handoff.
The goal is to leave the checkout understandable and safe, not merely clean.

G must fetch/prune, inspect `git status --short --branch`, identify the active
repo/branch/worktree/PR/base/merge commit when relevant, classify residue, and
report `checkout_cleanup`. Classify residue as reviewed workflow files,
unrelated user changes, generated cache/build artifacts, stale branch state,
stale stash state, temporary validation worktree, or unsafe/unclear residue.

G may remove or normalize only clearly safe residue within deployer scope, such
as temporary validation worktrees created by the same pass when clean or
generated caches clearly produced by the current run. Preserve and report
meaningful, unrelated, ambiguous, or user-authored changes.

G must not run destructive cleanup commands such as `git reset --hard`,
`git clean -fd`, force branch deletion, or stash dropping unless the user
explicitly approves the exact cleanup. Raw logs, private artifacts, generated
evidence, workbook exports, local runtime files, and other private/local-only
data require exact approval before deletion.

The only standing exception is verified squash-merge local branch residue. G
may use `git branch -D` without asking again only when the branch is the head
branch of a PR G just merged or live-verified as merged; the PR is `MERGED`;
the local branch tip exactly equals the PR head SHA; the merge commit is
recorded; the branch is not current, `main`, an integration branch, or a
protected long-lived branch; no dirty worktree is attached; and the deletion is
recorded in `checkout_cleanup`. This exception does not cover reset, clean,
stash drops, private artifact deletion, remote branch deletion, or ambiguous
residue.

## Validation And Review

Run the smallest relevant validation first and record exact command-result
pairs. Common checks include focused `pytest`, related `pytest`, full `pytest`,
`ruff`, `python3 tools/check_agent_docs.py`, `git diff --check`, protected
surface scans, and secret-pattern scans.

Before submitter work, Codex E should review from fresh context with only the
issue, contract, implementation handoff, PR or changed-file list, and this
workflow file. Ask E to check contract mismatches, missing tests, stale
imports, renamed symbols, shared-state ownership mistakes, workbook or
deployment drift, protected-surface leaks, and parser truth leaking downstream.
Treat findings as blocking only when they include concrete evidence.

For no-known-bug module audits, compare implementation and focused tests
against the contract first. Do not change behavior unless a clear contract
mismatch appears; add tests only when the contract requires them, produce a
comparison handoff, and route to E.
