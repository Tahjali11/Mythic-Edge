# Architecture Decision Records

Architecture Decision Records, or ADRs, are short durable documents that record important Mythic Edge design or process decisions. They explain the context, decision, scope, consequences, and follow-up path for choices that future issues, contracts, reviews, and PRs are expected to respect.

ADRs preserve why a cross-project rule exists. They do not replace current user instructions, GitHub issues, problem representations, module contracts, review reports, protected-surface checks, or PR drift budgets.

## Authority

Accepted ADRs are durable precedent, but they are not the highest authority.

Authority order for ADR use:

1. Active system, developer, and current user instructions.
2. Root `AGENTS.md`, `docs/agent_rules.yml`, and `docs/agent_constitution.md`.
3. Current GitHub issue, problem representation, and module contract for the scoped work.
4. Accepted ADRs in `docs/decisions/`.
5. Implementation handoffs, review reports, PR descriptions, and tracker comments as evidence and routing artifacts.
6. Older docs, examples, uncited assumptions, stale memory, and chat history.

If an accepted ADR appears to conflict with a higher-priority instruction or governing document, follow the higher-priority source and record the conflict. If a current issue or contract appears to conflict with an accepted ADR, name the conflict and route back to Codex A or Codex B unless the issue and contract explicitly authorize an ADR amendment or supersession path.

Handoffs, review reports, PR descriptions, and tracker comments can cite ADRs, but they do not supersede accepted ADRs by themselves.

ADRs cannot authorize protected-surface changes by implication. Parser behavior, parser state final reconciliation, workbook schema, webhook request/response contracts, Apps Script behavior, event classes, event kinds, parser message shapes, match/game identity, deduplication, secrets, generated data, raw logs, runtime health files, transport failure artifacts, workbook exports, production deployment behavior, and merge-to-main policy still require explicit issue, contract, review, and validation authority.

## When An ADR Is Required

Write or cite an ADR for durable decisions that outlive one issue, module, or PR, especially:

- truth ownership changes or clarifications between parser/state, webhook, Apps Script, workbook, dashboards, and AI layers
- protected-surface policy changes
- schema-change, snapshot-update, fixture/evidence, or drift-budget policy changes
- parser resilience and Player.log drift policy that affects future modules
- AI analytics or coaching boundaries
- persistent external integration boundaries, privacy boundaries, secrets policy, or data-retention policy
- branch, merge, deployment, or production-safety policy
- durable dependency, tooling, code-generation, or validation-gate strategy
- future escalation of advisory tools into required CI gates
- retirement, migration, or compatibility decisions for legacy workbook, parser, event, or runtime surfaces
- decisions that supersede, reject, or materially amend a prior ADR

Plain English test: if future reviewers will ask why the project is allowed or required to do this across multiple modules, write or cite an ADR.

## When An ADR Is Not Required

An ADR is not required for ordinary scoped work already covered by an issue, contract, and review path, such as:

- typos or formatting fixes
- local wording improvements that do not change rules
- focused tests that preserve an existing contract
- implementation details fully scoped to one module contract
- one-off bug fixes that do not establish cross-project precedent
- small reversible tooling conveniences that do not change validation policy
- PR-specific drift disclosures that do not set future policy
- implementation handoffs, contract-test reports, or review reports that only verify a scoped issue

If a small change moves truth ownership, loosens a protected surface, changes branch or deployment policy, or creates precedent for future work, route it through an ADR or back to Codex A/B.

## Status Values

Use exactly one of these status values:

- `Proposed`: written for review but not yet accepted as durable precedent.
- `Accepted`: reviewed and merged into the approved branch; future issues, contracts, and PRs should treat it as durable precedent.
- `Superseded`: replaced by a newer accepted ADR; the file remains and links to the superseding ADR.
- `Deprecated`: historically true but no longer recommended for new work, usually during migration.
- `Rejected`: intentionally not adopted; keep the record when the option is likely to recur or the rationale matters.

New ADRs start as `Proposed`. An ADR becomes `Accepted` only through reviewed repo changes on the approved branch or another explicit user-approved workflow.

## File Naming

Use this naming pattern:

```text
docs/decisions/ADR-0001-short-kebab-title.md
```

Rules:

- Use `ADR-` plus a four-digit, zero-padded, monotonic number.
- Use a short lowercase kebab-case slug after the number.
- Never reuse numbers, even if an ADR is rejected or superseded.
- Do not renumber existing ADRs.
- Do not use dates as the primary identifier.
- Do not create seed ADRs without an issue and contract that explicitly authorize them.

`ADR_TEMPLATE.md` is not a decision record and does not consume a number.

## Required ADR Fields

Every ADR must include:

- Title
- Status
- Date
- Decision owners / workflow role
- Related issues
- Related PRs
- Related contracts, handoffs, or review reports
- Context
- Decision
- Scope
- Non-goals
- Alternatives considered
- Consequences
- Truth ownership impact
- Protected surfaces touched or explicitly not touched
- Validation or review evidence
- Supersedes
- Superseded by
- Follow-ups
- Notes

Use `docs/decisions/ADR_TEMPLATE.md` as the starting point.

## Updates And Supersession

Material changes to an accepted ADR require a new ADR or explicit supersession path. Do not silently rewrite accepted rationale.

Tiny typo, formatting, broken-link, or metadata fixes may be made in place when they do not alter the decision.

Superseding ADRs must name older ADRs in `Supersedes`. Superseded ADRs must name the newer ADR in `Superseded by`. Rejected ADRs should remain in the directory when the rejected option or rationale is likely to recur.

## Citations

Issues, problem representations, module contracts, implementation handoffs, contract-test reports, review reports, and PRs should cite relevant accepted ADRs when they operate in an area covered by those ADRs.

Use `Related ADRs: N/A` when no ADR applies.

## ADR Index

| ADR | Status | Decision |
| --- | --- | --- |
| [ADR-0001: Parser Owns Truth](ADR-0001-parser-owns-truth.md) | Accepted | Parser/state owns event interpretation and normalized match/game facts. |
| [ADR-0002: Local Deterministic Scorer Decides, LLM Explains](ADR-0002-local-deterministic-scorer-decides-llm-explains.md) | Accepted | Deterministic local code owns scoring and LLMs explain or propose hypotheses. |
| [ADR-0003: Player.log Drift Policy](ADR-0003-player-log-drift-policy.md) | Accepted | Player.log is observable evidence that can drift; parser resilience must expose uncertainty. |
| [ADR-0004: Protected Surfaces And Schema-Change Policy](ADR-0004-protected-surfaces-and-schema-change-policy.md) | Accepted | Protected surfaces and schema changes require explicit issue, contract, review, and validation authority. |
| [ADR-0005: External Integration And Collaboration Surfaces](ADR-0005-external-integration-collaboration-surfaces.md) | Accepted | External tools and collaboration spaces are access, evidence, transport, or explanation surfaces by default. |
| [ADR-0006: Repository Boundary Strategy](ADR-0006-repository-boundary-strategy.md) | Accepted | Keep Mythic Edge monorepo-first while defining safe future boundaries for Parser, Corpus / Provenance, Analytics, Local App / UI, Workbook / Transport, Quality / Governance, and future AI Integration. |
| [ADR-0007: Parser Runtime State Decomposition Strategy](ADR-0007-parser-runtime-state-decomposition-strategy.md) | Accepted | Parser runtime state decomposition proceeds through one behavior-preserving state-cluster extraction at a time, with PostingState as the first pilot pattern. |
