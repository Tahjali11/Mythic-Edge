# Codex Module Workflow

This workflow adapts the Manasight issue-to-PR pattern for Mythic Edge and Codex threads.

The goal is to keep each thread focused. A thread is a separate Codex conversation with a narrow job and a durable handoff artifact. The artifacts become the stable shared memory between threads.

All threads should start from `docs/agent_constitution.md`, then apply the role-specific file in `docs/agent_threads/`.

## Source Of Truth

The parser remains the source of truth for MTGA event interpretation. GitHub issues, contracts, pull requests, test reports, Google Sheets formulas, and AI review notes are downstream coordination tools.

For changes that cross parser, webhook, workbook, and dashboard layers, name the truth owner before implementation starts.

## Thread Roles

1. Thinker (A)
   - Starts from a user idea, bug, confusing behavior, or module audit request.
   - Produces a GitHub issue or problem representation using `docs/templates/problem_representation.md`.
   - Should not implement code.
   - Must identify likely project layer, risk tier, first bad value or inspection order, expected output, scope, and validation evidence needed.

2. Module Contract Writer (B)
   - Starts from the approved issue or problem representation.
   - Produces or updates a contract using `docs/templates/module_contract.md`.
   - Defines inputs, outputs, invariants, public interfaces, file ownership, error behavior, side effects, compatibility, and test obligations.
   - Should not implement behavior changes.

3. Module Implementer (C)
   - Starts from the issue and module contract.
   - Compares current code to the contract.
   - Implements the smallest coherent change needed to satisfy the contract.
   - Updates focused tests and writes an implementation handoff.

4. Module Fixer (D)
   - Starts from a concrete reviewer finding, contract-test mismatch, failing check, or explicit user request.
   - Makes the smallest coherent fix.
   - Routes back to Module Contract Writer if the contract is ambiguous or wrong.
   - Routes back to Thinker if the requested fix changes scope.

5. Module Reviewer (E)
   - Starts from the issue, contract, implementation handoff, and diff or pull request.
   - Reviews for contract mismatches, bugs, missing tests, unsafe behavior, and drift.
   - Produces a review or contract test report using `docs/templates/contract_test_report.md` when contract verification is the focus.
   - Routes to Module Fixer, Module Contract Writer, Thinker, Module Submitter, or none.

6. Module Submitter (F)
   - Starts only after review has no blocking findings.
   - Stages intended files, commits, pushes, and opens a draft pull request.
   - Targets a non-production branch unless the user explicitly approves a production target.
   - Does not merge.

## Handoff Rule

Every thread that expects the workflow to continue must produce:

- its durable artifact
- a pasteable next-thread prompt
- a machine-readable `workflow_handoff` block

Use `docs/templates/workflow_handoff.md` for the handoff shape.

The artifact is the source of truth. The prompt is only a convenience wrapper for the next thread.

## Normal Path

The normal path is:

```text
A Thinker -> B Module Contract Writer -> C Module Implementer -> E Module Reviewer -> F Module Submitter
```

Use D Module Fixer only after C or E when there is a concrete fix target.

## Loopbacks

Module Reviewer may route to:

- D Module Fixer when implementation is wrong or tests are missing
- B Module Contract Writer when the contract is ambiguous or incorrect
- A Thinker when the problem framing or scope is wrong
- F Module Submitter when ready for draft PR

Module Fixer may route to:

- E Module Reviewer after a code or test fix
- B Module Contract Writer when a fix requires contract clarification
- A Thinker when the requested behavior is outside the original problem scope

Module Submitter must stop if the working tree is mixed, validation is missing, review has blocking findings, secrets or local artifacts are staged, or the requested PR target is production without explicit approval.

## Recommended GitHub Flow

Use one GitHub issue per coherent module change. Link every contract, handoff, report, and pull request back to that issue.

Suggested labels:

- `workflow:problem`
- `workflow:contract`
- `workflow:implementation`
- `workflow:fix`
- `workflow:review`
- `workflow:submit`
- `workflow:contract-test`
- `layer:parser`
- `layer:webhook`
- `layer:workbook`
- `layer:dashboard`

Suggested branches:

- `codex/problem-<short-name>` for issue-shaping docs only
- `codex/contract-<short-name>` for contract docs only
- `codex/impl-<short-name>` for code and tests
- `codex/fix-<short-name>` for targeted fixes after review
- `codex/submit-<short-name>` only when submitter needs a separate publishing branch

For repeated parser module audits, use a non-production integration branch:

```text
codex/parser-module-audit-suite
```

Module-specific PRs should target that integration branch first. Open a later PR from the integration branch to `main` only after the audited module set is complete.

## Checkpoints

Stable checkpoint 1: the problem issue is clear enough that a new thread can explain the bug, feature, or audit without rereading the whole conversation.

Stable checkpoint 2: the module contract names every changed interface between layers.

Stable checkpoint 3: implementation passes the smallest focused tests before the full repo checks.

Stable checkpoint 4: review confirms the implemented behavior, or records exact mismatches as findings.

Stable checkpoint 5: submitter opens a draft PR to the approved target branch and stops before merge.

## Validation Policy

Run the smallest relevant command first.

For most Mythic Edge code changes:

```powershell
py -m pytest -q tests
py -m ruff check src tests
```

For repo-level validation:

```powershell
.\tools\run_repo_checks.ps1
```

For coverage-sensitive changes:

```powershell
.\tools\run_repo_checks.ps1 -Coverage
```

For narrow Python-only edits:

```powershell
.\tools\run_touched_file_checks.ps1 <changed-python-file> <changed-test-file>
```

## Fresh-Context Review Gate

Before submitting implementation work, start a fresh Codex thread with only:

- the GitHub issue link
- the module contract link
- the implementation handoff link
- the pull request link or changed-file list
- this workflow document

Ask it to review for:

- contract mismatches
- missing tests
- stale imports or renamed symbols
- shared state ownership mistakes
- workbook or deployment drift
- parser truth leaking into downstream formulas

Treat findings as blocking only when they include concrete evidence.
