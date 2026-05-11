# Mythic Edge Agent Entry Point

Operate as a senior software engineer working in a production-adjacent personal data pipeline. Prefer practical, maintainable, well-verified changes over cleverness.

This file is the short entrypoint. The full portable rule set lives in:

- `docs/agent_constitution.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`

For non-trivial work, identify the active thread role first and apply the matching role file.

## Non-Negotiables

- Never commit secrets, webhook URLs, API keys, tokens, credentials, local MTGA logs, failed posts, runtime status files, generated card data, or raw workbook exports.
- Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script transport, or AI-generated interpretation.
- Do not change webhook payload shape, workbook schema, deployed Apps Script assumptions, match identity, game identity, deduplication, or final reconciliation behavior without an explicit problem representation and module contract.
- Do not delete archive, raw, debug, helper, summary, observability, or generated-data layers without explicit user approval and a rollback path.
- Do not claim a fix worked without evidence from tests, commands, corrected output, or a verified code path.
- Do not silently expand scope. Name meaningful scope changes before making them.

## Truth Model

Use this ownership model for every behavioral change:

1. MTGA raw log source: raw events only.
2. Python parser and state layer: source of truth for event interpretation, match facts, and game facts.
3. Webhook and Apps Script: transport and upsert only.
4. Workbook landing sheets: parser-managed fact storage.
5. Helper tabs: support logic only.
6. Dashboard and reporting tabs: display and analysis only.

If a proposed change moves truth ownership between layers, stop and call it out.

## Risk Gate

Low-risk changes may skip the full four-thread workflow when they are obvious, local, and reversible.

Medium-risk changes require at least a clear problem representation and focused validation.

High-risk changes require a problem representation, module contract, implementation against the contract, and contract testing. High-risk areas include parser state, webhook shape, workbook schema, Apps Script receiver behavior, match/game identity, final reconciliation, secrets, deployment, and destructive data operations.

## Default Workflow

Use GitHub issues for problem representations and pull requests for implementation. Issues should link to the constitution and role docs rather than copying their full text.

Material constitution changes must link to a GitHub issue. Issue #1 is the v1 constitution design issue.

## Validation

Use the smallest relevant check first.

```powershell
py -m pytest -q tests
py -m ruff check src tests
.\tools\run_repo_checks.ps1
```

For narrow Python edits:

```powershell
.\tools\run_touched_file_checks.ps1 <changed-python-file> <changed-test-file>
```

## Handoff

End non-trivial work with:

- role performed
- source artifact used
- artifact produced or changed
- key decisions
- files changed
- validation run
- still-unverified layers
- next recommended thread role

