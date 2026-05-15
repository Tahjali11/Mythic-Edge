# ADR-0005: External Integration And Collaboration Surfaces

Status: Accepted

Date: 2026-05-15

Decision owners / workflow role:

- Codex C: Module Implementer / comparison thread, with source contract `docs/contracts/external_integration_collaboration_surfaces.md`.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/79
- https://github.com/Tahjali11/Mythic-Edge/issues/76

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/80

Related contracts, handoffs, or review reports:

- `docs/contracts/external_integration_collaboration_surfaces.md`
- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0002: Local Deterministic Scorer Decides, LLM Explains`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`

## Context

Mythic Edge increasingly uses external systems and helper tools for research,
coordination, review, publishing, and explanation. Those surfaces include
GitHub, Google Drive, Google Docs, Google Sheets, MCP servers, plugins,
connectors, browser and shell automation helpers, local Codex skills, OpenAI
documentation tooling, future model-provider APIs, and external data sources.

The project already protects parser truth, AI boundaries, protected surfaces,
and Codex H advisory status. The remaining governance gap is that external
integration and collaboration surfaces need one durable decision that explains
what those surfaces are allowed to own.

## Decision

External integrations and collaboration spaces are access, collaboration,
research, evidence, transport, or explanation surfaces by default. They are not
project truth or repo authority unless a current issue, contract, accepted ADR,
or higher-priority authority explicitly grants that role.

Repo authority remains governed by active instructions, `AGENTS.md`,
`docs/agent_rules.yml`, `docs/agent_constitution.md`, current issues, current
contracts, accepted ADRs, reviewed handoffs, reviewed reports, and approved
PRs.

Parser/state remains the truth owner for MTGA event interpretation and
normalized match/game facts. Deterministic local code may own future scoring or
evaluation only when separately contracted. AI and LLM output may explain,
summarize, classify, compare, enrich, recommend, or hypothesize, but it must
not own parser-managed truth, deterministic scoring, workbook schema,
merge/deploy readiness, credential policy, or repo authority.

Google Sheets may support structured review, human annotations, testing queues,
experiment tracking, analytics snapshots, downstream storage, dashboards,
reports, helper tabs, and analysis views. Google Sheets must not own parser
truth, workbook schema truth, drift recovery truth, deterministic scoring
authority, or merge/deploy authority.

Google Docs may support drafted and reviewed memos, sideboard guides, matchup
notes, tournament prep, planning drafts, comments, feedback packets, and
research summaries. Google Docs content is not repo authority by default.

Local Codex skills are helper instructions. MCP servers, plugins, and
connectors are tool-access surfaces. They may help inspect, read, write,
comment, or automate external systems only when the current user request and
active workflow role authorize that action.

OpenAI documentation tooling is research/reference support. It is separate
from OpenAI API runtime integration. Runtime model-provider integration,
coaching evaluation, external data retention, credential contracts, and
sensitive data sharing each require separate scoped issue and contract
authority before implementation.

Human approval is required before live external writes, permission or sharing
changes, credential or secret changes, broader connector authorization,
sensitive external data sharing, production deployment changes, destructive
external operations, OpenAI API runtime integration, or coaching evaluation.

## Scope

This ADR governs governance boundaries for:

- GitHub issues, PRs, comments, checks, and Actions as workflow surfaces
- Google Drive, Google Docs, Google Sheets, and Google Slides
- live Mythic Edge and deck-testing workbooks
- local Codex skills
- MCP servers, plugins, and connectors
- browser, shell, and local automation helpers
- OpenAI documentation tooling
- future OpenAI API or model-provider runtime integrations
- external card, metagame, matchup, and strategy data sources
- email, chat, calendar, or collaboration connectors
- file export/import tools

It applies to future issues, contracts, implementation handoffs, reviews, PR
templates, and protected-surface reviews that involve external collaboration or
tool access.

## Non-Goals

This ADR does not:

- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change parser event classes or payload shapes
- change match/game identity or deduplication
- install or authorize connectors, plugins, MCP servers, or OAuth grants
- create, rotate, print, store, or change secrets, credentials, API keys,
  tokens, webhook URLs, or environment variable contracts
- edit live Google Docs, Google Sheets, Google Drive permissions, or sharing
- add OpenAI API runtime integration
- implement coaching evaluation
- send raw logs, failed posts, runtime status files, workbook exports, or
  generated local artifacts to external tools
- change CI gates, production deployment behavior, or merge-to-main policy

## Alternatives Considered

- Treat external tools as ordinary convenience helpers with no durable policy.
  Rejected because connector access, live documents, credentials, and retained
  external data create recurring authority and privacy risks.
- Let each connector or tool define its own authority. Rejected because repo
  authority must remain in repo-governed artifacts, not in tool behavior.
- Ban external tools entirely. Rejected because read-only research,
  collaboration, review, and publishing support are useful when scoped and
  labeled correctly.
- Bundle coaching evaluation into this policy. Rejected because coaching needs
  separate goals, scoring or rubric logic, prompts, privacy boundaries,
  validation evidence, and acceptance criteria.

## Consequences

Future threads have a durable citation for keeping tools, connectors, Docs,
Sheets, local skills, and AI output in the right role. Reviewers can reject
changes that treat external access as authority, parser truth, credential
permission, or merge/deploy readiness.

The cost is that live external writes, broader connector permissions, sensitive
data sharing, model-provider runtime integration, and coaching evaluation need
explicit issue and contract authority. That friction is intentional because
those actions can affect privacy, retention, credentials, production state, and
project truth boundaries.

## Truth Ownership Impact

This ADR preserves `ADR-0001` parser truth ownership and `ADR-0002` AI/LLM
boundaries. Parser/state owns parser-managed facts. Deterministic local code
may own future scoring or evaluation only when separately contracted. External
tools, collaboration spaces, local skills, connectors, Docs, Sheets, and AI
output remain downstream access, collaboration, storage, display, evidence, or
explanation layers by default.

## Protected Surfaces Touched

No protected runtime surfaces are touched by this ADR.

This ADR does not authorize:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- secrets, credential, token, API key, OAuth grant, service-account, or webhook
  URL changes
- environment variable contract changes
- live Google Docs or Google Sheets edits
- Google Drive permission or sharing changes
- connector/plugin/MCP installation or authorization changes
- committing raw logs
- generated card/tier data changes
- runtime status file changes
- failed-post changes
- workbook export changes
- OpenAI API runtime behavior
- coaching evaluation behavior
- production deployment behavior
- merge-to-main policy

## Validation Or Review Evidence

Runtime parser tests are not applicable for this docs-only ADR proposal because
no runtime code changed.

Implementation validation is recorded in
`docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md`.

This ADR cites issue #79, the external integration contract, the existing
constitution and rule index, Codex H tool-surface guidance, and the accepted
parser truth, AI boundary, and protected-surface ADRs.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Future OpenAI API runtime integration requires a separate issue, contract,
  privacy boundary, secret/environment contract, validation plan, and review.
- Future coaching evaluation requires a separate issue and contract.
- Future live Google Workspace workflows should define explicit write,
  sharing, retention, and redaction boundaries before implementation.
- Future external data-provider work may need a separate contract if it affects
  deterministic analytics or source-trust policy.

## Notes

Do not use this ADR as permission to touch live external systems, credentials,
runtime integrations, parser truth, workbook schema, deployment behavior, or
coaching evaluation. It records the default boundary: external surfaces help
the work; they do not own the work.
