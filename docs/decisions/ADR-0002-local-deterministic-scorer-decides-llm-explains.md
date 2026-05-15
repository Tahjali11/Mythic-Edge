# ADR-0002: Local Deterministic Scorer Decides, LLM Explains

Status: Accepted

Date: 2026-05-15

Decision owners / workflow role:

- Codex C: Module Implementer / comparison thread, with source contract `docs/contracts/code_hardening_seed_adrs.md`.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/decisions/README.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `tests/test_analytics_sidecar.py`
- `docs/Mythic_Edge_Deep_Dive_Guide.md`

Related ADRs:

- `ADR-0001: Parser Owns Truth`

## Context

Mythic Edge may eventually support richer coaching, analytics, scoring, ranking, filtering, and AI-assisted explanations. The project already distinguishes parser-owned facts from downstream analytics and AI interpretation.

Current analytics-sidecar code and tests are useful context, but they are not an implementation contract for future LLM or coaching work. This ADR records the durable boundary: deterministic local code decides, and LLMs explain or propose hypotheses.

The `Accepted` status is intended to become effective after this ADR is reviewed and merged into the approved hardening branch.

## Decision

For future coaching, analytics, scoring, ranking, filtering, and confidence-aware calculations, deterministic local code owns decisions.

Deterministic local code means repo-owned logic that can be inspected, tested, reviewed, rerun, and validated without relying on an LLM response.

LLMs may summarize, classify, explain, compare alternatives, and propose hypotheses from parser-produced facts, deterministic analytics, confidence labels, and curated strategy context.

LLM output must be labeled as inference, enrichment, recommendation, explanation, or hypothesis.

LLM output must not become the truth owner for match result, game result, play/draw, mulligan count, opening hand, card actions, deck submission, row identity, workbook schema, or parser-managed fields.

Strategy/coaching layers should carry deterministic evidence and uncertainty when available, including sample size, confidence warnings, and source labels.

Any OpenAI, LLM, coaching, or model-backed analytics implementation requires its own issue, module contract, validation plan, and privacy boundary review.

## Scope

This ADR governs future model-backed analytics, coaching, summarization, hypothesis generation, and strategic explanation layers.

It also governs how those layers should treat parser-produced facts, deterministic analytics, confidence labels, curated strategy context, and LLM output labels.

## Non-Goals

This ADR does not:

- implement OpenAI API integration
- send raw logs to any LLM
- add coaching modules
- change analytics sidecar behavior
- change parser-managed fields
- treat LLM guesses as professional-level strategic truth
- bypass future analytics or coaching module contracts
- define prompt text, model choice, token policy, API keys, or deployment behavior
- authorize workbook formulas or dashboards to own analytics truth

## Alternatives Considered

- Let LLMs directly decide scores, rankings, or parser-managed facts. Rejected because responses are not deterministic enough to own project truth.
- Keep all AI out of analytics. Rejected because explanation, comparison, and hypothesis support can be useful when grounded in parser-produced facts.
- Let workbook formulas own scoring. Rejected because durable analytics policy should stay in repo-owned, reviewable logic when it affects decisions.
- Treat the current analytics sidecar as the future coaching contract. Rejected because it is context, not a full LLM/coaching design.

## Consequences

Future coaching work must separate deterministic calculations from language-model explanation. This makes analytics easier to test, review, and reproduce.

LLM features can still be helpful, but they must carry labels and uncertainty. They cannot silently become parser truth, schema truth, or authoritative strategic verdicts.

The cost is that future AI work needs a clear module contract and privacy review before implementation.

## Truth Ownership Impact

This ADR preserves `ADR-0001` parser truth ownership. Parser/state owns parser-managed facts. Deterministic local analytics may own scoring or ranking decisions for analytics features. LLMs own explanation, inference, enrichment, recommendation, and hypothesis text only.

## Protected Surfaces Touched

No protected runtime surfaces are touched by this ADR.

This ADR does not authorize:

- parser behavior
- parser state final reconciliation
- parser-managed fields
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event class changes
- event `kind` value changes
- parser payload shape changes
- match identity changes
- game identity changes
- deduplication changes
- secrets, credential, token, API key, or webhook URL changes
- environment variable contract changes
- committing raw logs
- generated card/tier data changes
- runtime status file changes
- failed-post changes
- workbook export changes
- production deployment behavior
- merge-to-main policy

## Validation Or Review Evidence

Runtime parser tests are not applicable for this docs-only ADR creation because no runtime code changed.

Implementation validation is recorded in `docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md`.

This ADR cites the existing AI boundary in `docs/agent_constitution.md`, ADR policy in `docs/decisions/README.md`, the code hardening tracker, issue #47, and current analytics-sidecar context.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Create a dedicated issue and module contract before implementing OpenAI, LLM, coaching, or model-backed analytics features.
- Future analytics/coaching work should define privacy boundaries, prompt/data policy, deterministic scoring inputs, validation, and user-facing uncertainty labels.

## Notes

Do not use this ADR as permission to add API keys, send raw logs, change runtime behavior, or treat AI output as project truth.
