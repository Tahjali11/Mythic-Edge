# ADR-0001: Parser Owns Truth

Status: Accepted

Date: 2026-05-15

Decision owners / workflow role:

- Codex C: Module Implementer / comparison thread, with source contract `docs/contracts/code_hardening_seed_adrs.md`.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/1
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/56
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/decisions/README.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `origin/main:docs/contracts/parser_models.md`
- `origin/main:docs/contracts/parser_state.md`
- `origin/main:docs/contracts/parser_outputs.md`
- `origin/main:docs/contracts/parser_sheet_schema.md`
- `origin/main:docs/contracts/parser_sheet_exports.md`

Related ADRs:

- None.

## Context

Mythic Edge is a layered MTGA data pipeline. Raw MTGA logs provide observable evidence, but the parser and state layer turns that evidence into normalized match and game facts. Downstream systems store, transport, display, or analyze those facts.

The project has repeatedly protected this boundary in `AGENTS.md`, the agent constitution, the rule index, parser audit contracts, hardening contracts, and issue workflow. This ADR records that durable decision as the first seed architecture decision.

The parser-audit contracts cited from `origin/main` are remote source citations for this hardening branch. They are not copied into `codex/code-hardening-suite` by this ADR.

The `Accepted` status is intended to become effective after this ADR is reviewed and merged into the approved hardening branch.

## Decision

Parser and state interpretation own MTGA event interpretation and normalized match/game facts.

`state.py` owns live parser state, final reconciliation, changed-field detection, and in-memory match/game truth.

`models.py` owns normalized match/game row shapes and serializer behavior.

`sheet_schema.py` owns Python-side sync-field and workbook-facing schema vocabulary.

`outputs.py`, webhook transport, Apps Script, workbook landing sheets, helper tabs, dashboards, and AI interpretation consume parser-produced facts; they do not reconstruct or override parser truth.

Workbook formulas, helper tabs, dashboards, Apps Script, webhook transport, and AI-generated interpretation must not become truth owners for match result, game result, play/draw, mulligan count, opening hand, card actions, deck submission, row identity, workbook schema, or parser-managed fields.

Any proposed move of truth ownership requires a new issue, module contract, review, and validation. If it would supersede this ADR, it also requires an ADR amendment or supersession path.

## Scope

This ADR governs durable truth ownership boundaries across parser/state, models, sheet schema, output transport, Apps Script, workbook layers, dashboards, and AI/analytics consumers.

It applies to future issues, contracts, implementation handoffs, reviews, PR drift budgets, and protected-surface reviews that touch parser-managed facts.

## Non-Goals

This ADR does not:

- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change parser event classes or payload shapes
- change match/game identity or deduplication
- use dashboards, formulas, Apps Script, webhooks, or AI as parser truth
- define every module-level contract for parser code
- replace issue-specific problem representations or module contracts

## Alternatives Considered

- Let workbook formulas or dashboards reconstruct missing parser facts. Rejected because it moves truth downstream and hides parser/evidence drift.
- Let Apps Script or webhook transport reinterpret parser rows. Rejected because transport layers should move parser-produced facts, not decide them.
- Let AI or analytics classify parser-managed facts as truth. Rejected because AI may explain or enrich, but must not own parser-managed facts.
- Keep this rule only in scattered issues and contracts. Rejected because future threads need a stable ADR citation.

## Consequences

Future work has a clear owner for parser-managed facts. Reviewers can reject downstream fixes that should be parser/state fixes. Workbook, webhook, Apps Script, dashboard, and AI work must cite parser-produced facts rather than silently inventing their own truth.

The cost is that some convenient downstream patches require a proper parser issue, contract, and validation path. That friction is intentional when truth ownership is involved.

## Truth Ownership Impact

This ADR preserves existing Mythic Edge truth ownership. Parser/state remains the truth-producing layer for event interpretation and normalized match/game facts. Models and sheet schema define parser-owned row and schema vocabulary. Downstream layers consume, transport, store, display, summarize, or enrich those facts without becoming truth owners.

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

This ADR relies on reviewed governance and parser-audit source artifacts cited above, including the parser models, state, outputs, sheet schema, and sheet exports contracts.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Future work that intentionally changes parser truth ownership must create a new issue, module contract, and ADR amendment or supersession path.

## Notes

Do not use this ADR as blanket authorization for parser, workbook, webhook, Apps Script, AI, or deployment changes. It records the current ownership boundary; it does not implement behavior.
