# ADR-0003: Player.log Drift Policy

Status: Accepted

Date: 2026-05-15

Decision owners / workflow role:

- Codex C: Module Implementer / comparison thread, with source contract `docs/contracts/code_hardening_seed_adrs.md`.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/11
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/60
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/12
- https://github.com/Tahjali11/Mythic-Edge/pull/61
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

Related ADRs:

- `ADR-0001: Parser Owns Truth`

## Context

Mythic Edge depends on MTGA `Player.log` data. `Player.log` is the local evidence source the project can inspect, but Arena may change or remove emitted fields without notice.

The Player.log evidence-ledger problem representation and contract exist on `origin/main` and `origin/codex/parser-module-audit-suite`, not locally on the current hardening branch. This ADR cites those remote source artifacts without copying them into this branch.

The `Accepted` status is intended to become effective after this ADR is reviewed and merged into the approved hardening branch.

## Decision

MTGA `Player.log` is the project's ultimate local observable evidence source, but it is not absolute game truth.

The real game state lives inside Arena. Mythic Edge can only parse what Arena emits.

Arena may remove, rename, reorder, redact, or reshape log fields without notice.

The parser should prioritize accuracy, explicit uncertainty, and safe degradation over filling missing facts with confident guesses.

Current observed log behavior can be used as a golden baseline for tests, schema snapshots, and drift detection, but not as a guarantee from Wizards.

Drift detection should distinguish parser evidence drift from webhook transport failure, workbook drift, deployed Apps Script drift, local artifact drift, and AI/analytics interpretation.

Future ledger and drift work should use the evidence-ledger vocabulary for value-source labels, confidence labels, finality labels, drift flags, invariant checks, and degradation behavior unless a later issue, contract, or ADR supersedes it.

Local private Player.log files may inform local drift reports, but committed fixtures must be sanitized.

Required value-source labels:

- `observed`: directly read from current Player.log evidence
- `derived`: computed from multiple observed facts without guessing
- `inferred`: best-effort fallback from indirect evidence
- `unknown`: unavailable or not safely recoverable
- `conflict`: multiple evidence paths disagree
- `legacy_enriched`: enriched from older retained metadata that is not currently emitted by current Player.log evidence

Required confidence labels:

- `high`: directly observed or derived from stable observed facts
- `medium`: inferred or derived from a known fallback with strong support
- `low`: inferred from weak, incomplete, or conflicting support
- `unknown`: no trustworthy evidence

Required finality labels:

- `live`: still updating during active parsing
- `provisional`: likely but not reconciled against final result evidence
- `reconciled`: a final value updated by later stronger evidence

Required drift flags include:

- `missing_expected_event_family`
- `missing_expected_payload_path`
- `changed_signal_type`
- `new_unknown_event_family`
- `new_unknown_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `invariant_failed`
- `schema_snapshot_missing`
- `fixture_gap`
- `parser_exception`
- `transport_failure`
- `workbook_drift`
- `deployment_drift`
- `sensitive_evidence_redacted`

## Scope

This ADR governs how Mythic Edge should talk about Player.log evidence, drift, uncertainty, confidence, finality, degradation, and sanitized fixtures.

It applies to future evidence-ledger, schema-snapshot, drift-report, invariant, golden-fixture, parser-resilience, and analytics-confidence work.

## Non-Goals

This ADR does not:

- implement the evidence ledger
- implement drift reports
- commit raw local logs
- change parser behavior
- change workbook or webhook schema
- automatically create GitHub issues from drift reports
- hide uncertainty from downstream analytics
- treat inferred or legacy-enriched values as observed truth
- define every raw log signal or parser field mapping
- replace the Player.log evidence-ledger contract

## Alternatives Considered

- Treat Player.log as absolute truth. Rejected because Arena is the real game state and logs are only observable evidence.
- Treat current log shape as a permanent external contract. Rejected because Arena log fields can drift without notice.
- Fill missing facts with confident guesses. Rejected because uncertainty must be visible to downstream analytics and review.
- Commit raw local logs as fixtures. Rejected because raw logs may contain private or local-only data; committed fixtures must be sanitized.

## Consequences

Future resilience work must expose uncertainty instead of hiding it. Drift reports should identify affected parser-managed outputs and separate parser evidence drift from transport, workbook, deployment, and AI interpretation problems.

This increases documentation and validation burden, but it prevents fragile assumptions from silently becoming workbook or analytics truth.

## Truth Ownership Impact

This ADR preserves parser/state truth ownership from `ADR-0001`. Player.log is evidence, not absolute game truth. The parser/state layer owns interpretation of that evidence. Evidence-ledger and drift tooling support parser quality assurance; they do not replace parser truth.

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

This ADR cites issue #11, PR #12, the Player.log evidence-ledger problem representation and contract from `origin/main`, and parser event schema snapshot hardening from issue #60 / PR #61.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Future evidence-ledger implementation should define machine-readable ledger entries and drift reports without changing workbook/webhook schemas unless a separate migration contract authorizes that.
- Future golden fixtures must use sanitized committed evidence only.

## Notes

Do not use this ADR as permission to commit raw logs, create automated issues, change parser behavior, or expose new workbook/webhook metadata.
