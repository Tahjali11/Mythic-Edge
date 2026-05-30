# ADR-0006: Repository Boundary Strategy

Status: Proposed

Date: 2026-05-21

Decision owners / workflow role:

- Codex A: architecture framing / readiness assessment.
- Codex B: ADR adoption contract.
- Codex C: adoption comparison / revision.
- Codex E: adoption review / contract test.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/217
- https://github.com/Tahjali11/Mythic-Edge/issues/215

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/216

Related contracts, handoffs, or review reports:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/decisions/README.md`
- `README.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- `docs/contracts/adr_0006_repository_boundary_adoption.md`
- `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`
- `docs/problem_representations/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger.md`

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0002: Local Deterministic Scorer Decides, LLM Explains`
- `ADR-0003: Player.log Drift Policy`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`

## Context

Mythic Edge began as a personal MTG Arena parser/data pipeline, but its project
direction has expanded into a local MTGA decision-support system. That system
requires multiple capabilities:

- a parser that turns `Player.log` evidence into structured observations
- validation and provenance that explain whether parser-produced facts are
  trustworthy
- deterministic analytics that measure repeatable patterns
- local app and UI surfaces that expose setup, import, and analytics workflows
- workbook and transport surfaces that receive parser-normalized rows
- quality and governance surfaces that keep boundaries reviewable
- future AI Integration layers that may explain, summarize, or propose
  hypotheses without owning truth

Manasight provides a useful reference for separating a parser library from a
sanitized corpus. Mythic Edge may eventually benefit from a similar multi-repo
shape, especially if Corpus / Provenance, Parser, Analytics, or future AI
Integration assets become independently reusable.

The current Mythic Edge codebase is still changing rapidly. Parser event
contracts, evidence-ledger tiers, corpus reports, workbook-facing rows,
diagnostics, golden replay planning, and future analytics boundaries are still
being refined. Splitting repositories too early would increase dependency,
versioning, CI, branch, and Codex context risk.

The project needs a durable policy that allows future repository extraction
without making a split the current plan.

The internal project boundary package from issue #215 names the current
monorepo-internal project areas and confirms that ADR-0006 should be treated as
proposed context until reviewed and accepted through the normal workflow.

## Decision

Mythic Edge remains a single primary repository until a future issue, contract,
review, and user-approved migration plan explicitly authorize extracting a
component.

The current repo should still be organized as if future boundaries may exist.
Future work should keep Parser, Corpus / Provenance, Analytics, Local App / UI,
Workbook / Transport, Quality / Governance, and future AI Integration
responsibilities separable even while they live in one repository.

The preferred future extraction order is:

1. Corpus / Provenance first.
   A future `mythic-edge-corpus` repository may own sanitized or synthetic
   `Player.log` fixture slices, golden replay manifests, count-only baselines,
   evidence-ledger metadata, drift baselines, release tags, and corpus
   metadata. It must not contain raw private logs, secrets, failed posts,
   runtime status files, generated private data, generated SQLite databases,
   local JSONL artifacts, or workbook exports.

2. Parser second.
   A future `mythic-edge-parser` repository may own `Player.log` discovery,
   tailing, line buffering, routing, parser event classes, parser modules,
   parser metadata, sanitization, and parser-library tests. Extraction should
   wait until event families, payload contracts, truncation/data-loss handling,
   GameState diff mechanics, draft events, and corpus parity are stable enough
   to version.

3. Analytics after parser and provenance stabilize.
   A future `mythic-edge-analytics` repository may own deterministic feature
   extraction, player-improvement metrics, matchup/card/performance analysis,
   and model-ready derived features. It should consume validated parser facts
   and provenance metadata. It must not reach backward into raw logs, parser
   internals, or legacy derived artifacts as a truth shortcut.

4. AI Integration / advisor last.
   A future AI Integration, advisor, or recommender repository may own
   user-facing explanations, review prompts, coaching hypotheses, and optional
   LLM advisory scaffolds. It must consume deterministic analytics and
   provenance labels. It must not own parser truth, analytics truth, validation
   truth, workbook truth, merge readiness, deployment readiness, model-provider
   truth, or hidden game facts.

5. Quality / Governance workflow assets only if they become reusable outside
   Mythic Edge.
   A future workflow repository may own reusable Codex skills, prompts,
   templates, or governance helpers. It must not supersede the active repo
   constitution, current issues, current contracts, accepted ADRs, reviewed
   PRs, or repo authority by implication.

This extraction order is planning guidance only. It is not authorization to
extract a repository, move files, rename packages, change imports, or add
validation gates.

The primary `mythic-edge` repository should remain the integration and app
orchestration home unless a later issue, contract, review, accepted ADR, and
explicit user-approved migration plan supersede this decision. It may own the
local runner, Local App / UI, Workbook / Transport integration, Apps Script
assets, user-facing configuration, launcher behavior, docs, and
cross-component integration tests.

Workbook / Transport and Local App / UI should remain in the primary repo by
default unless a future issue, contract, review, and accepted ADR explicitly
authorize a split.

Future repository dependency direction should be one-way:

```text
Corpus / Provenance -> no production code dependency by default
Parser -> may consume pinned sanitized corpus releases for tests
Workbook / Transport -> consumes parser-normalized row contracts
Analytics -> consumes validated parser facts and provenance metadata
Local App / UI -> consumes backend, analytics, setup/status, and display APIs
AI Integration -> consumes deterministic analytics and provenance summaries
Quality / Governance -> may inspect all layers without becoming runtime behavior
```

Repository boundaries do not change truth ownership. Moving code or data to a
new repository does not make that repository the owner of parser truth,
workbook truth, validation truth, merge readiness, deployment readiness, or AI
truth unless a future issue, contract, accepted ADR, and review path explicitly
say so.

Before any extraction, the project must define:

- the owning repository and non-owning consumers
- public API or artifact contracts
- versioning and dependency-pin strategy
- migration and rollback plan
- CI and validation gates for both source and consumer repositories
- protected-surface and secret/private-artifact policy for the new repository
- cross-repo issue, PR, release, and tracker workflow
- compatibility tests proving the existing app still works with the extracted
  component

## Scope

This ADR governs future repository-boundary planning for Mythic Edge.

It applies to future issues, contracts, implementation handoffs, reviews, PR
descriptions, release plans, CI plans, and migration plans that propose
extracting Parser, Corpus / Provenance, Analytics, Local App / UI, Workbook /
Transport, Quality / Governance, or future AI Integration surfaces out of the
current repository.

## Non-Goals

This ADR does not:

- split the repository
- move files
- create a new GitHub repository
- publish a package
- change imports
- change CI
- change parser behavior
- change parser state final reconciliation
- change parser event classes, event `kind` values, or payload shapes
- change analytics behavior
- change SQLite schema or migrations
- change local app/UI behavior
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change Google Sheets behavior
- change match/game identity or deduplication
- authorize raw private logs or local artifacts in any repository
- implement analytics, Local App / UI, or AI Integration behavior
- authorize OpenAI API or model-provider runtime integration
- add CI gates
- change branch, merge, deploy, or tracker policy by itself

## Alternatives Considered

- Split into multiple repositories immediately. Rejected for now because the
  parser, evidence ledger, workbook surfaces, diagnostics, and analytics
  boundaries are still evolving together. Early extraction would increase
  coordination overhead and Codex context risk.
- Keep one repository forever. Rejected as a durable policy because a future
  sanitized corpus or parser package may become easier to test, release, and
  consume as its own repository.
- Mirror Manasight's repository structure exactly. Rejected because Mythic Edge
  is not only a parser library. It is a local MTGA decision-support system with
  Parser, Corpus / Provenance, Analytics, Local App / UI, Workbook / Transport,
  Quality / Governance, and future AI Integration layers.
- Split by implementation language or Codex role. Rejected for now because
  repository boundaries should follow product and truth-ownership boundaries,
  not just tooling convenience.
- Use a monorepo with internal package boundaries first. Accepted as the
  current operating strategy.

## Consequences

Future contributors and Codex threads have a clear answer when multi-repo
structure comes up: design for separation, but do not split until interfaces
are stable and migration is explicitly authorized.

The likely first useful extraction is a sanitized Corpus / Provenance
repository, because corpus artifacts can be versioned and consumed by tests
without moving parser truth. Parser extraction should wait for stable public
event and payload contracts. Analytics and future AI Integration extraction
should wait until evidence-ledger and provenance semantics are strong enough
for downstream consumption.

The cost is that the current repository remains broad for longer. That is
acceptable while the project is still finding the right boundaries. The benefit
is fewer cross-repo dependency failures, fewer stale contracts, and less risk
that Codex treats an extracted component as owning truth it should only
consume.

## Truth Ownership Impact

This ADR preserves `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, and
`ADR-0005`.

Parser and state interpretation remain the source of truth for parser-managed
facts. The evidence ledger describes support, confidence, finality, drift, and
degradation for those facts. Deterministic analytics may own derived analytic
scores only when separately contracted. Local App / UI may display and
orchestrate local workflows, but it must not own parser or analytics truth.
Workbook / Transport may receive and move parser-normalized rows, but it must
not feed transport or sheet state back into parser truth. Future AI Integration
and LLM layers may explain, summarize, or propose hypotheses, but they must not
own parser truth, analytics truth, validation truth, schema truth, merge
readiness, deploy readiness, model-provider truth, or hidden game facts.

A repository boundary is an ownership and packaging boundary, not a truth
shortcut.

## Protected Surfaces Touched

No protected runtime surfaces are touched by this ADR.

This ADR does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- parser event class or event `kind` changes
- parser payload shape changes
- analytics behavior changes
- SQLite schema or migration changes
- local app/UI behavior changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- Google Sheets behavior changes
- match/game identity changes
- deduplication changes
- environment variable contract changes
- secrets, credential, token, API key, or webhook URL changes
- raw local log commits
- generated card data commits
- runtime status file commits
- failed post commits
- workbook export commits
- generated SQLite database commits
- local JSONL artifact commits
- production deployment changes
- OpenAI API or model-provider runtime behavior

Any future repository extraction that touches a protected surface still requires
an explicit issue, contract, review, validation, and deployer path.

## Validation Or Review Evidence

Runtime validation is not applicable because this ADR is documentation-only and
does not change code, imports, CI, parser behavior, analytics behavior, local
app/UI behavior, workbook schema, webhook payloads, Apps Script behavior,
runtime artifacts, or generated data.

Current adoption evidence:

- issue #217 ADR-0006 adoption governance issue:
  - https://github.com/Tahjali11/Mythic-Edge/issues/217
- PR #216 draft ADR-0006 adoption PR:
  - https://github.com/Tahjali11/Mythic-Edge/pull/216
- issue #215 internal project boundary package:
  - `docs/contracts/internal_project_boundaries.md`
  - `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
  - `docs/contract_test_reports/internal_project_boundaries.md`
- ADR-0006 adoption contract:
  - `docs/contracts/adr_0006_repository_boundary_adoption.md`
- Codex C adoption comparison:
  - `docs/implementation_handoffs/adr_0006_repository_boundary_adoption_comparison.md`
- Codex E adoption review:
  - `docs/contract_test_reports/adr_0006_repository_boundary_adoption.md`

Acceptance still requires explicit user authorization and the approved
submitter/deployer path. The Codex C handoff records `git diff --check`,
path-scoped protected-surface scan, and path-scoped secret/private-marker scan
results for this revision.

Future extraction plans must define their own validation, including consumer
compatibility tests across the source repository and the app repository.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Create a future repository-boundary problem representation before any actual
  extraction.
- Use issue #217 as the dedicated ADR-0006 adoption governance issue for this
  adoption package.
- Consider a future `mythic-edge-corpus` extraction plan after evidence-ledger
  Tier 7 and corpus parity goals are stable.
- Define public event, payload, fixture, and release compatibility contracts
  before any parser extraction.
- If extraction becomes near-term, create migration checklists for local
  worktrees, GitHub issues, PR routing, CI, secrets scanning, package versions,
  and rollback.

## Notes

This ADR intentionally keeps repository splitting as a future option, not a
current requirement.

The preferred project framing is: Mythic Edge is a local MTGA decision-support
system. The parser is an evidence intake and interpretation layer, not the
whole project.

This revision keeps `Status: Proposed`. Acceptance should occur only through
reviewed repo changes on an approved branch, or through another explicit
user-approved workflow.

Issue #217 is the direct ADR-0006 adoption governance issue for this pass.
Issue #215 is related evidence, not a closing target for this adoption pass.
Do not use `Closes #215` for the ADR-0006 adoption PR unless a future issue or
user instruction explicitly changes that routing.
