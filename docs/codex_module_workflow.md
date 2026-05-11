# Codex Module Workflow

This workflow adapts the Manasight issue-to-PR pattern for Mythic Edge and Codex threads.

The goal is to keep each thread focused. A thread is a separate Codex conversation with a narrow job and a written handoff artifact. The artifacts become the stable shared memory between threads.

## Source Of Truth

The parser remains the source of truth for MTGA event interpretation. GitHub issues, contracts, pull requests, test reports, Google Sheets formulas, and AI review notes are downstream coordination tools.

For changes that cross parser, webhook, workbook, and dashboard layers, name the truth owner before implementation starts.

## Thread Roles

1. Problem Representation Thread
   - Starts from a user idea, bug, or confusing behavior.
   - Produces a GitHub issue using `docs/templates/problem_representation.md`.
   - Should not implement code.
   - Must identify the likely project layer, first bad value, expected output, and validation evidence needed.

2. Module Contract Thread
   - Starts from the approved problem issue.
   - Produces or updates a contract using `docs/templates/module_contract.md`.
   - Defines inputs, outputs, invariants, public functions, file ownership, error behavior, and test obligations.
   - Should not implement the feature beyond tiny discovery spikes.

3. Implementation Thread
   - Starts from the issue and module contract.
   - Implements the smallest coherent wiring pass against the contract.
   - Updates tests and docs that are directly affected.
   - Opens a pull request using `.github/pull_request_template.md`.

4. Contract Test Thread
   - Starts from the pull request and module contract.
   - Tests whether implementation behavior matches the contract.
   - Produces a contract verification report using `docs/templates/contract_test_report.md`.
   - Should prefer filing review feedback over silently changing the contract.

## Recommended GitHub Flow

Use one GitHub issue per coherent module change. Link every contract and pull request back to that issue.

Suggested labels:

- `workflow:problem`
- `workflow:contract`
- `workflow:implementation`
- `workflow:contract-test`
- `layer:parser`
- `layer:webhook`
- `layer:workbook`
- `layer:dashboard`

Suggested branches:

- `codex/problem-<short-name>` for issue-shaping docs only
- `codex/contract-<short-name>` for contract docs only
- `codex/impl-<short-name>` for code and tests
- `codex/test-<short-name>` only when the test thread needs a follow-up patch

## Checkpoints

Stable checkpoint 1: the problem issue is clear enough that a new thread can explain the bug or feature without rereading the whole conversation.

Stable checkpoint 2: the module contract names every changed interface between layers.

Stable checkpoint 3: implementation passes the smallest focused tests before the full repo checks.

Stable checkpoint 4: contract testing confirms the implemented behavior, or records exact mismatches as review feedback.

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

Before merging implementation work, start a fresh Codex thread with only:

- the GitHub issue link
- the module contract link
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

