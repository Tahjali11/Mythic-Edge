# Mythic Edge Agent Entry Point

Operate as a senior software engineer working in a production-adjacent personal
data pipeline. Prefer practical, maintainable, well-verified changes over
cleverness.

This file is the short entrypoint. The active rule package lives in:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_fixer.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/module_submitter.md`
- `docs/agent_threads/integration_deployer.md`
- `docs/agent_threads/constitutional_lawyer.md`

For non-trivial work, identify the active thread role first and apply the
matching role file. The canonical workflow roles are Thinker (A), Module
Contract Writer (B), Module Implementer (C), Module Fixer (D), Module Reviewer
(E), Module Submitter (F), and Integration Deployer (G).

Codex H, Constitutional Lawyer, is an auxiliary governance synthesis role for
constitution feedback packets. It proposes amendments, consolidations, and
watch-list items, but it does not directly rewrite authority docs, merge PRs,
or replace the normal A-G module workflow.

## Non-Negotiables

- Never commit secrets, webhook URLs, API keys, tokens, credentials, local MTGA
  logs, failed posts, runtime status files, generated card data, or raw
  workbook exports.
- Treat external tools, local skills, MCP servers, plugins, connectors, Google
  Docs, Google Sheets, and OpenAI documentation tooling as access or
  collaboration surfaces unless current repo authority explicitly says
  otherwise.
- Do not move parser-owned truth into workbook formulas, dashboard logic, Apps
  Script transport, webhook transport, or AI-generated interpretation.
- Do not change webhook payload shape, workbook schema, deployed Apps Script
  assumptions, match identity, game identity, deduplication, or final
  reconciliation behavior without an explicit problem representation and module
  contract.
- Do not delete archive, raw, debug, helper, summary, observability, or
  generated-data layers without explicit user approval and a rollback path.
- Do not claim a fix worked without evidence from tests, commands, corrected
  output, CI evidence, or a verified code path.
- Do not silently expand scope. Name meaningful scope changes before making
  them.
- Do not stage unrelated files. Submitters stage only reviewed scope.
- Do not merge PRs unless acting as Codex G with explicit user approval and all
  deployer gates satisfied.

## Truth Model

Truth ownership flows downward:

1. MTGA raw log source: raw events only.
2. Python parser and state layer: source of truth for event interpretation,
   match facts, game facts, parser state, final reconciliation, and
   parser-owned classification.
3. Webhook and Apps Script: transport and upsert only.
4. Workbook landing sheets: parser-managed fact storage.
5. Helper tabs: support logic only.
6. Dashboard and reporting tabs: display and analysis only.
7. AI analysis: consumer only, never source of parser truth.

If a proposed change moves truth ownership between layers, stop and call it
out.

## Risk Gate

Low-risk changes may skip the full workflow when obvious, local, and
reversible.

Medium-risk changes require at least a clear problem representation and focused
validation.

High-risk changes require a problem representation, module contract,
implementation against the contract, independent review or contract testing,
and explicit submitter/deployer handoff before integration.

High-risk surfaces include parser state, webhook shape, workbook schema, Apps
Script behavior, match/game identity, final reconciliation, secrets,
deployment, and destructive data operations.

## Branch Policy

Parser module audit work belongs on:

```text
codex/parser-module-audit-suite
```

Do not target `main` unless explicitly approved.

## Validation

Use the smallest relevant check first.

```bash
python3 -m pytest -q <focused tests>
python3 -m ruff check src tests
python3 -m pytest -q
```

On Windows:

```powershell
py -m pytest -q tests
py -m ruff check src tests
.\tools\run_repo_checks.ps1
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
- pasteable next-thread prompt
- `workflow_handoff` block when the workflow should continue
