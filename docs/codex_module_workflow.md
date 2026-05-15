# Codex Module Workflow

This workflow adapts the Manasight issue-to-PR pattern for Mythic Edge and
Codex threads. It is the operating guide for moving one coherent unit of work
from problem framing to reviewed integration.

Start every non-trivial thread from:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- the active role file in `docs/agent_threads/`
- the relevant artifact template in `docs/templates/`

The artifact is the source of truth. Pasteable prompts are only convenience
wrappers for the next thread.

Architecture Decision Records (ADRs) under `docs/decisions/` record durable cross-project decisions that future issues, contracts, reviews, and PRs should cite when relevant. ADRs do not replace issue-scoped contracts and do not authorize protected-surface changes by implication.

## Source Of Truth

The parser and state layer own MTGA event interpretation and normalized
match/game facts. GitHub issues, contracts, pull requests, workbook formulas,
dashboard logic, Apps Script, webhook transport, and AI notes are downstream
coordination or display surfaces.

For work that crosses parser, webhook, workbook, dashboard, deployment, or AI
analysis layers, name the truth owner before implementation starts.

External tools and collaboration spaces, including Google Docs, Google Sheets,
local skills, MCP servers, plugins, connectors, browser or shell helpers,
OpenAI documentation tooling, and external data sources, are access or
collaboration surfaces unless current repo authority says otherwise. Live
external writes, permission changes, credential work, sensitive external data
sharing, OpenAI API runtime integration, and coaching evaluation require
separate scoped authorization.

## Thread Roles

1. Codex A: Thinker
   - turns a vague request, bug, or audit target into a problem representation
   - owns scope, risk tier, first inspection order, and expected output
   - must not implement code

2. Codex B: Module Contract Writer
   - turns the approved problem representation into a contract
   - owns public interfaces, invariants, truth boundaries, side effects, tests,
     and acceptance criteria
   - must not implement behavior changes

3. Codex C: Module Implementer
   - compares current repo state to the contract
   - implements the smallest coherent change needed to satisfy the contract
   - updates focused tests and writes an implementation handoff
   - must not commit unless explicitly asked

4. Codex D: Module Fixer
   - starts from a concrete reviewer finding, contract-test mismatch, failing
     check, or explicit user request
   - makes the smallest coherent fix
   - routes back to B if the contract is ambiguous or wrong
   - routes back to A if the requested change changes scope

5. Codex E: Module Reviewer / Contract Tester
   - reviews with fresh context
   - verifies implementation against the issue, contract, handoff, and diff
   - produces findings or a contract-test report
   - does not silently fix code in review-only mode

6. Codex F: Module Submitter
   - stages only reviewed files, commits, pushes, and opens or updates a draft
     PR to the approved base branch
   - does not merge PRs, close issues, or update trackers as completed
   - routes merge/close/tracker-update work to Codex G

7. Codex G: Integration Deployer
   - starts only when the user explicitly asks for deployer or merge work
   - verifies merge gates, marks PRs ready when appropriate, merges into the
     approved base, closes completed issues, updates trackers, and records
     completion evidence
   - must not bypass review, CI, branch, issue, tracker, or scope gates

Auxiliary governance role:

- Codex H: Constitutional Lawyer
  - synthesizes constitution feedback packets into amendment proposals,
    consolidations, unresolved conflicts, and watch-list items
  - produces source coverage before synthesis when multiple packets are
    supplied
  - does not directly edit authority docs or replace the normal A-G module
    workflow

## Normal Path

```text
A Thinker -> B Module Contract Writer -> C Module Implementer -> E Module Reviewer -> F Module Submitter -> G Integration Deployer
```

Use D only as a loopback role for concrete fix targets.

Use H only for constitution feedback synthesis. H output routes back to A or B
for new framing or contracts, or to C only when an existing issue and contract
already authorize implementation.

Before proposing amendments, H should classify packet recommendations against
current repo state so satisfied, stale, superseded, conflicting, active, and
watch-list items are not flattened together.

Before routing amendments forward, H should also apply the amendment quality
test, classify each proposal by rule type, assess whether added ceremony is
justified by risk, and treat tools, plugins, connectors, MCP servers, and local
skills as access or collaboration surfaces unless current repo authority says
otherwise.

## Loopbacks

Route to A when scope is outside the issue, the problem framing is wrong, a
different module/layer is involved, or a new issue is needed.

Route to B when contract behavior is ambiguous or inaccurate, expected output
vocabulary is unclear, precedence rules are disputed, or downstream truth
ownership would change.

Route to D when implementation has a concrete bug, required tests are missing,
validation fails in reviewed scope, or reviewer findings are specific enough to
fix directly.

Route to E when implementation or fixer work is ready for contract
verification.

Route to F when review has no blocking findings and validation is complete or
explicitly explained.

Route to G only when a draft PR is ready for merge consideration and the user
asks for deployer or merge work.

## Handoff Rule

Every thread that expects the workflow to continue must produce:

- its durable artifact
- a pasteable next-thread prompt
- a machine-readable `workflow_handoff` block

Use `docs/templates/workflow_handoff.md` for the handoff shape.

Use `docs/templates/constitution_feedback_packet.md` for raw constitution
feedback packets. Raw packets default to pasteable output or GitHub issue
comments; repo storage requires an explicit feedback-round issue and contract.

## Issue Lifecycle

When the work relies on or changes durable project policy, the handoff should include `Related ADRs` or state `Related ADRs: N/A`. If a scoped issue or contract conflicts with an accepted ADR, route back to Thinker or Module Contract Writer before implementation unless the issue and contract explicitly authorize an ADR amendment or supersession path.

Use one GitHub issue per coherent module or workflow change. Link contracts,
handoffs, reports, and PRs back to the issue and to the tracker when one exists.

Trackers stay open until the entire tracked queue or phase is complete. A
single child issue or module finishing is not enough to close a tracker.

Module audit issues close only after required artifacts exist, review is clean
or accepted, PR work is merged into the approved base, validation or CI is
recorded, and the tracker is updated when applicable.

Bug issues close after the fix PR is merged, validation is recorded, and no
follow-up implementation is implied.

Planning or docs issues close when requested artifacts are complete, or when a
follow-up implementation issue is linked.

Constitution issues close when rule changes are merged, affected role docs and
templates are updated if needed, validation is recorded, and no amendment work
remains.

Completion comments should include PR number, merge commit, base branch,
durable artifacts produced, validation or CI result, and tracker status or next
queue item when applicable.

## PR Lifecycle

PRs default to draft unless the user explicitly asks otherwise.

Module audit PRs target the non-production integration branch first:

```text
codex/parser-module-audit-suite
```

Do not target `main` unless explicitly approved.

Use `Closes #...` only when the PR fully satisfies the issue. Use `Refs #...`
for partial, planning-only, contract-only, tracker, or follow-up work.

Codex F may submit a PR only after review has no blocking findings and
validation is present or explicitly explained.

Codex G may merge only after the user asks for deployer or merge work and all
merge gates pass.

Merge gates:

- PR is not draft
- base branch is approved
- target is not `main` unless explicitly approved
- CI/checks pass or the user explicitly waives named failures
- review has no blocking findings
- diff remains within reviewed scope
- no forbidden files, secrets, local artifacts, generated data, raw logs,
  runtime status files, failed posts, or workbook exports are included
- issue closing behavior is correct
- tracker update behavior is correct

After merge, Codex G confirms merge method and commit, confirms source branch
deletion or preservation, syncs the local integration branch when working
locally, closes fully satisfied issues with completion comments, updates
trackers, and names the next workflow step.

## Tracker Hygiene

Update trackers when a child issue is created, child PR is opened, child PR is
merged, child issue is closed, child issue is blocked, or the next queue item
changes.

Tracker updates should name issue number and title, PR number and base branch,
merge commit if merged, durable artifacts produced, validation or CI status,
blocker or residual risk, next queue item, and related open issues.

Trackers summarize workflow progress. They never own parser truth.

## Validation Policy

Run the smallest relevant command first.

Common Python checks:

```bash
python3 -m pytest -q <focused tests>
python3 -m ruff check src tests
python3 -m pytest -q
```

Documentation checks:

```bash
git diff --check
```

On Windows:

```powershell
py -m pytest -q tests
py -m ruff check src tests
.\tools\run_repo_checks.ps1
```

For narrow Python-only edits:

```powershell
.\tools\run_touched_file_checks.ps1 <changed-python-file> <changed-test-file>
```

## Fresh-Context Review Gate

Before submitter work, start a fresh Codex E thread with only:

- the GitHub issue link
- the module contract link
- the implementation handoff link
- the pull request link or changed-file list
- this workflow document

Ask it to review for contract mismatches, missing tests, stale imports or
renamed symbols, shared state ownership mistakes, workbook or deployment drift,
and parser truth leaking into downstream formulas.

Treat findings as blocking only when they include concrete evidence.
