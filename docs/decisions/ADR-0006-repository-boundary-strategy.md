# ADR-0006: Repository Boundary Strategy

Status: Proposed

Date: 2026-05-21

Decision owners / workflow role:

- Codex A: Thinker / architecture framing role.
- Codex D: Module Fixer / ADR-0006 governance blocker cleanup.

Related issues:

- N/A. This ADR records future repository-boundary policy before any split is
  attempted.

Related PRs:

- TBD

Related contracts, handoffs, or review reports:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/decisions/README.md`
- `README.md`
- `docs/problem_representations/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger.md`

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0002: Local Deterministic Scorer Decides, LLM Explains`
- `ADR-0003: Player.log Drift Policy`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`

## Context

Mythic Edge began as a personal MTG Arena parser/data pipeline, but its product
direction has expanded. The durable project identity is now a
competitively-oriented decision support tool. That tool requires multiple
capabilities:

- a parser that turns `Player.log` evidence into structured observations
- validation and provenance that explain whether parser-produced facts are
  trustworthy
- deterministic analytics that measure repeatable patterns
- future recommendation or explanation layers that help the player decide what
  to review

Manasight provides a useful reference for separating a parser library from a
sanitized corpus. Mythic Edge may eventually benefit from a similar multi-repo
shape, especially if the corpus, parser, analytics, and Codex workflow assets
become independently reusable.

The current Mythic Edge codebase is still changing rapidly. Parser event
contracts, evidence-ledger tiers, corpus reports, workbook-facing rows,
diagnostics, golden replay planning, and future analytics boundaries are still
being refined. Splitting repositories too early would increase dependency,
versioning, CI, branch, and Codex context risk.

The project needs a durable policy that allows future repository extraction
without making a split the current plan.

## Decision

Mythic Edge remains a single primary repository until a future issue, contract,
review, and user-approved migration plan explicitly authorize extracting a
component.

The current repo should still be organized as if future boundaries may exist.
Future work should keep parser, corpus, evidence/provenance, analytics,
recommendation, workflow, and app orchestration responsibilities separable even
while they live in one repository.

The preferred future extraction order is:

1. Corpus first.
   A future `mythic-edge-corpus` repository may own sanitized or synthetic
   `Player.log` fixture slices, golden replay manifests, count-only baselines,
   release tags, and corpus metadata. It must not contain raw private logs,
   secrets, failed posts, runtime status files, generated private data, or
   workbook exports.

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
   and provenance metadata. It must not reach backward into raw logs or parser
   internals as a truth shortcut.

4. Recommendation/advisor last.
   A future advisor or recommender repository may own user-facing
   recommendations, explanations, review prompts, and optional LLM advisory
   scaffolds. It must consume deterministic analytics and provenance labels. It
   must not own parser truth, validation truth, merge readiness, deployment
   readiness, or hidden game facts.

5. Agent workflow assets only if they become reusable outside Mythic Edge.
   A future workflow repository may own Codex skills, prompts, templates, or
   governance helpers. It must not supersede the active repo constitution,
   current issues, contracts, accepted ADRs, or reviewed PRs by implication.

The primary `mythic-edge` repository should remain the integration and app
orchestration home unless a later ADR supersedes this decision. It may own the
local runner, workbook/webhook integration, Apps Script assets, user-facing
configuration, launcher behavior, docs, and cross-component integration tests.

Future repository dependency direction should be one-way:

```text
corpus -> no production code dependency
parser -> may consume pinned corpus releases for tests
app/evidence -> consumes parser event and row contracts
analytics -> consumes validated parser/evidence outputs
advisor -> consumes deterministic analytics and provenance summaries
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
extracting parser, corpus, analytics, advisor, workflow, or app-orchestration
surfaces out of the current repository.

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
- change parser event classes or payload shapes
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change match/game identity or deduplication
- authorize raw private logs or local artifacts in any repository
- implement analytics or recommendation behavior
- authorize OpenAI API or model-provider runtime integration
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
  is not only a parser library. It is a competitively-oriented decision support
  tool with parser, validation, analytics, and recommendation layers.
- Split by implementation language or Codex role. Rejected for now because
  repository boundaries should follow product and truth-ownership boundaries,
  not just tooling convenience.
- Use a monorepo with internal package boundaries first. Accepted as the
  current operating strategy.

## Consequences

Future contributors and Codex threads have a clear answer when multi-repo
structure comes up: design for separation, but do not split until interfaces
are stable and migration is explicitly authorized.

The likely first useful extraction is a sanitized corpus repository, because
corpus artifacts can be versioned and consumed by CI without moving parser
truth. Parser extraction should wait for stable public event and payload
contracts. Analytics and advisor extraction should wait until evidence-ledger
and provenance semantics are strong enough for downstream consumption.

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
scores only when separately contracted. Recommendation and LLM layers may
explain, summarize, or propose hypotheses, but they must not own parser truth,
validation truth, schema truth, merge readiness, deploy readiness, or hidden
game facts.

A repository boundary is an ownership and packaging boundary, not a truth
shortcut.

## Protected Surfaces Touched

No protected runtime surfaces are touched by this ADR.

This ADR does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- parser event class or event `kind` changes
- parser payload shape changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- match/game identity changes
- deduplication changes
- environment variable contract changes
- secrets, credential, token, API key, or webhook URL changes
- raw local log commits
- generated card data commits
- runtime status file commits
- failed post commits
- workbook export commits
- production deployment changes
- OpenAI API or model-provider runtime behavior

Any future repository extraction that touches a protected surface still requires
an explicit issue, contract, review, validation, and deployer path.

## Validation Or Review Evidence

Runtime validation is not applicable because this ADR is documentation-only and
does not change code, imports, CI, parser behavior, workbook schema, webhook
payloads, Apps Script behavior, runtime artifacts, or generated data.

Codex D fixer validation for this ADR draft:

- `git diff --check`: no output.
- `git diff --check --no-index /dev/null docs/decisions/ADR-0006-repository-boundary-strategy.md`:
  no whitespace-error output; nonzero exit is expected for a new-file
  comparison.
- Trailing-whitespace scan for the ADR and ADR index: no matches.
- `python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`:
  passed with `forbidden: 0` and `warnings: 0`.

Future extraction plans must define their own validation, including consumer
compatibility tests across the source repository and the app repository.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Create a future repository-boundary problem representation before any actual
  extraction.
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

The preferred project framing is: Mythic Edge is a competitively-oriented MTGA
decision support tool. The parser is an evidence intake layer, not the whole
product.

This ADR cites only artifacts that exist on `origin/main` or accepted ADRs in
the standalone governance PR base. Parser-reliability branch artifacts can be
cited by a later update after they are merged into the target base.
