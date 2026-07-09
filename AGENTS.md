# Mythic Edge Agent Entry Point

Operate as a careful senior engineer in a production-adjacent personal MTGA
data pipeline. Prefer maintainable, well-verified changes over cleverness.

This file is the short repo entrypoint. For non-trivial work, read the current
authority package before editing:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- the active role file under `docs/agent_threads/`
- the relevant template under `docs/templates/`
- accepted ADRs under `docs/decisions/` when relevant

Use the Mythic Edge A-G workflow when applicable: Thinker, Module Contract
Writer, Module Implementer, Module Fixer, Module Reviewer, Module Submitter,
and Integration Deployer. Codex H is an auxiliary Constitutional Lawyer role
for governance synthesis only; it does not replace the A-G implementation path
or directly rewrite authority docs.

Before non-trivial work, identify the active repo lane. Mythic Edge repos
default to one active issue or lane at a time. Local worktrees, stale prompts,
status indexes, local skills, and chat memory are evidence only; current user
instructions, GitHub state, repo docs, accepted ADRs, issues, contracts, and
handoffs own workflow authority.

## Repo Ownership

This repo owns Mythic Edge parser/runtime source, local app source, workbook
transport code, governance docs, contracts, tests, and source-repo PRs.

This repo does not own private security findings, public-safe corpus package
publication, private Fable scoring internals, feature-expansion parking, or
sibling-repo issue lifecycle unless a current issue and handoff explicitly
authorize that scope.

## Non-Negotiables

- Never commit secrets, webhook URLs, API keys, tokens, credentials, local MTGA
  logs, failed posts, runtime status files, generated card data, SQLite
  databases, raw workbook exports, or other private/local artifacts.
- Treat external tools, local skills, MCP servers, plugins, connectors, Google
  Docs/Sheets, browser helpers, and OpenAI documentation tooling as access or
  collaboration surfaces unless current repo authority says otherwise.
- Do not move parser-owned truth into workbook formulas, dashboard logic, Apps
  Script, webhook transport, or AI-generated interpretation.
- Do not change protected surfaces without explicit issue and contract
  authority: parser state, extractors, event classes, match/game identity,
  deduplication, final reconciliation, webhook shape, workbook schema, Apps
  Script behavior, deployment, secrets, or destructive data operations.
- Do not delete archive, raw, debug, helper, summary, observability, or
  generated-data layers without explicit approval and a rollback path.
- Do not claim a fix worked without tests, command output, CI evidence,
  corrected output, or a verified code path.
- Do not silently expand scope, stage unrelated files, target `main`, merge
  PRs, or close issues unless the active workflow role and user approval allow
  it.

## Policy And Truth Boundaries

Codex must not decide legal compliance for Mythic Edge. If work touches Wizards
policy, MTG Arena fair play, Wizards IP, hidden information, client internals,
automation, cloud/shared data, commercial features, or public user data, stop
and route the issue to the human owner before implementation.

Truth flows downward: MTGA raw logs provide observed events; the Python parser
and state layer own event interpretation and normalized match/game/card facts;
webhook and Apps Script transport facts; workbook landing sheets store
parser-managed fields; helper/dashboard/AI layers consume and display. If a
change moves truth ownership between layers, stop and name that shift before
editing.

## Workflow Notes

Low-risk work may skip the full workflow when obvious, local, reversible, and
outside protected surfaces. Medium/high-risk work needs appropriate framing,
contracting, validation, review, and handoff under
`docs/codex_module_workflow.md`.

For medium/high-risk work, include `instruction_context` in the durable
artifact or handoff unless a current workflow explicitly allows deferral.

Codex G owns integration safety and checkout reconciliation when it runs. G
must classify residue, preserve meaningful or ambiguous work, avoid destructive
cleanup without exact approval, and report `checkout_cleanup`. The only bounded
force-delete exception is verified squash-merge local branch residue under the
checklist in `docs/codex_module_workflow.md`.

Parser module audit work normally targets `codex/parser-module-audit-suite`.
Do not target or merge into `main` unless explicitly approved.

## Validation And Handoff

Use the smallest relevant check first:

```bash
python3 -m pytest -q <focused tests>
python3 -m ruff check src tests
python3 -m pytest -q
git diff --check
```

End non-trivial work with role performed, source artifact, files changed,
validation, unverified layers, next role, pasteable next-thread prompt when
useful, and `workflow_handoff` when the workflow should continue.
