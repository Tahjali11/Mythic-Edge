# ADR-0004: Protected Surfaces And Schema-Change Policy

Status: Accepted

Date: 2026-05-15

Decision owners / workflow role:

- Codex C: Module Implementer / comparison thread, with source contract `docs/contracts/code_hardening_seed_adrs.md`.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/34
- https://github.com/Tahjali11/Mythic-Edge/issues/39
- https://github.com/Tahjali11/Mythic-Edge/issues/60
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/37
- https://github.com/Tahjali11/Mythic-Edge/pull/42
- https://github.com/Tahjali11/Mythic-Edge/pull/61
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/agent_rules.yml`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `tools/check_protected_surfaces.py`
- `.github/pull_request_template.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/`

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0003: Player.log Drift Policy`

## Context

The code hardening suite added path-based protected-surface warnings, a PR drift budget, parser event schema snapshot tests, and ADR policy. These guardrails make sensitive changes visible without pretending that a tool alone can authorize a semantic change.

This ADR records the durable policy for protected surfaces and schema changes. It combines the protected-surface gate, PR drift budget, parser event schema snapshots, and ADR governance into one seed decision record.

The `Accepted` status is intended to become effective after this ADR is reviewed and merged into the approved hardening branch.

## Decision

Protected surfaces require explicit issue, contract, review, and validation authority before semantic change.

Protected-surface gate warnings are review signals, not automatic authorization and not automatic rejection.

Clearly forbidden local, generated, private, credential, raw log, failed post, runtime status, and workbook export artifacts must not be committed.

Schema shape changes require explicit scoped authorization.

Event class changes, event `kind` changes, parser payload changes, workbook-facing row-key changes, sync-field changes, runtime family changes, webhook payload changes, Apps Script behavior changes, match/game identity changes, deduplication changes, and production deployment changes require explicit scoped authorization.

Snapshot updates are contract-visible changes and must not be auto-updated by Codex without issue, contract, and review approval.

PR drift budgets should disclose whether a change creates `No drift`, `Authorized drift`, `Residual drift`, or `N/A` for each protected category.

Passing tests are necessary but not sufficient for protected-surface readiness. The issue, contract, review, and drift budget must agree.

## Scope

This ADR governs protected-surface policy, schema-change policy, snapshot-update policy, PR drift-budget interpretation, and forbidden local/generated/private artifact policy.

It applies to parser/runtime/workbook/webhook/Apps Script surfaces, workflow authority docs, schema snapshots, branch/merge/deploy policy, and Codex review/submitter handoffs.

## Non-Goals

This ADR does not:

- change any protected surface by itself
- bypass the protected-surface gate
- bypass issue/contract/review workflow
- weaken secret or local artifact rules
- merge to `main` or production branches without explicit approval
- auto-update snapshots without approval
- make protected warnings fail CI without a future issue and contract
- replace module contracts for schema or runtime changes
- authorize live workbook or deployed Apps Script changes

## Alternatives Considered

- Fail every protected-surface warning automatically. Rejected for the first policy because protected changes may be legitimate when explicitly authorized.
- Treat warnings as permission to proceed. Rejected because only issues, contracts, reviews, and validation can authorize semantic protected-surface changes.
- Auto-update snapshots when tests fail. Rejected because snapshot changes are contract-visible and may hide schema drift.
- Let passing tests alone decide readiness. Rejected because tests do not prove issue scope, contract authority, drift disclosure, or deployment safety.

## Consequences

Future PRs touching protected paths must carry clear issue/contract authority and drift-budget disclosure. Reviewers should treat protected-surface warnings as prompts to verify authorization and semantic scope.

Forbidden local/private/generated artifacts remain blocked by policy. Snapshot updates require explicit approval rather than automatic regeneration.

The cost is more ceremony around sensitive files. The benefit is that parser truth, schema, payloads, identity, dedupe, secrets, deployment behavior, and local artifacts are less likely to drift silently.

## Truth Ownership Impact

This ADR preserves parser truth ownership from `ADR-0001` and evidence drift boundaries from `ADR-0003`. Protected-surface and schema tools expose risk; they do not decide parser truth, workbook truth, webhook truth, Apps Script truth, or deployment readiness by themselves.

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
- runtime family names
- runtime `event_type` values
- runtime `scope` values
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

This ADR cites the protected-surface diff gate contract, PR drift-budget contract, parser event schema snapshot contract, ADR policy contract, protected-surface tool, PR template, and schema snapshot test surfaces.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Future contracts may decide whether protected-surface warnings should ever become failing CI checks.
- Future golden fixture, drift detector, or schema migration policies may add narrower ADRs or supersede this ADR in part.

## Notes

Do not use this ADR as permission to touch a protected surface. It records the authorization path required before such changes are safe.
