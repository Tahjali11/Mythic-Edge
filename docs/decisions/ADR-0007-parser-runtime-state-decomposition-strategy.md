# ADR-0007: Parser Runtime State Decomposition Strategy

Status: Proposed

Date: 2026-06-09

Decision owners / workflow role:

- Codex A: problem representation for issue #307.
- Codex B: ADR adoption contract.
- Codex C: ADR adoption implementation pass.
- Codex E: pending ADR contract-test review.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/307

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/308

Related contracts, handoffs, or review reports:

- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`
- `src/mythic_edge_parser/app/posting_state.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- PR #308 merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0003: Player.log Drift Policy`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0006: Repository Boundary Strategy`

## Context

`src/mythic_edge_parser/app/state.py` is a protected parser runtime surface. It
owns live parser state, compatibility aliases, reset behavior, and helper APIs
used by parser, runner, outputs, transforms, tests, and local app support
surfaces.

Before issue #307, parser runtime state held multiple conceptual clusters in
one broad module. Those clusters include parser context, match and game summary
state, mulligan and opening-hand state, rank carry-forward state, card lookup
runtime state, local output path bookkeeping, transform emission guards, and
downstream posting or delivery bookkeeping.

That broad state shape is functional, but it creates review risk. Parser-truth
state and downstream delivery bookkeeping can appear equally authoritative when
they live beside each other. Compatibility aliases also make casual cleanup
risky because reset behavior and alias identity are part of the existing
runtime-state contract.

The issue #307 pilot extracted only `PostingState`, the downstream posting and
delivery bookkeeping cluster. PR #308 merged that behavior-preserving pilot
into `codex/analytics-foundation` at merge commit
`19192f718f8b50e1d7fe962d02455b0c933985ad`. The pilot introduced
`src/mythic_edge_parser/app/posting_state.py`, nested `PostingState` under
`ParserRuntimeState.posting`, and preserved existing `state.py` compatibility
aliases and helper behavior.

The original parser runtime state decomposition contract intentionally deferred
ADR-0007 until after a successful pilot. That condition has now been satisfied,
so this ADR records the durable strategy without authorizing another extraction
or any parser behavior change.

## Decision

Parser runtime state may be decomposed into smaller, named state clusters only
through incremental, behavior-preserving extraction contracts.

Each future extraction must operate on one coherent state cluster per issue and
contract. The extraction must preserve parser truth ownership, public helper
behavior, reset semantics, compatibility aliases, and validation expectations
unless a later contract explicitly authorizes a breaking cleanup.

`PostingState` is the accepted pilot pattern for this strategy. It is safe as a
precedent because it owns downstream posting and delivery bookkeeping, not
parser truth. It tracks which rows or payloads have already been emitted,
posted, or snapshotted. It does not decide match results, game results,
play/draw, mulligan counts, opening hands, card identity, match identity, game
identity, deduplication, or final reconciliation.

Compatibility aliases in `state.py` are intentional bridge code. They are not
accidental leftovers. Alias removal, deprecation warnings, broad caller
migration, constructor compatibility changes, or another state-cluster
extraction require a later issue, contract, review, and validation path.

## Scope

This ADR governs future parser runtime state decomposition work in Mythic Edge.

It applies to future issues, contracts, implementation handoffs, contract-test
reports, PR descriptions, and reviews that propose extracting or reorganizing
state currently owned by `src/mythic_edge_parser/app/state.py`.

Likely future state clusters include:

- posting and downstream delivery bookkeeping
- match lifecycle state
- game lifecycle state
- player, seat, team, and identity state
- mulligan and opening-hand state
- draft, deck, and sideboard state
- runtime diagnostics and drift status
- analytics or local-app bridge state, only where it does not own parser truth

Parser-truth clusters affect normalized match facts, game facts, event
interpretation, player identity, match identity, game identity, or final
reconciliation. Downstream bookkeeping clusters track delivery, posting, local
status, diagnostics, or transport progress and must not reinterpret parser
facts.

## Non-Goals

This ADR does not:

- accept broad parser-state rewrites
- implement another extraction
- remove compatibility aliases
- rewrite `state.py`
- change parser behavior
- change parser state final reconciliation
- change parser event classes or event kind values
- change parser payload shapes
- change match identity, game identity, or deduplication
- change workbook schema
- change webhook payload shape
- change Apps Script or Google Sheets behavior
- change analytics schema, migrations, or ingest behavior
- change local app behavior
- change output transport or production behavior
- change OpenAI/model-provider, AI/coaching, or Line Tracer behavior
- add CI gates
- move files, rename packages, or broadly change imports

## Alternatives Considered

- Rewrite `state.py` broadly. Rejected because parser runtime state is a
  protected surface and broad rewrites risk hidden changes to parser truth,
  final reconciliation, identity, reset behavior, and compatibility aliases.
- Extract multiple state clusters in one pass. Rejected because mixed clusters
  have different truth ownership and risk profiles. One cluster per contract is
  easier to review and validate.
- Remove legacy aliases during extraction. Rejected for the default path
  because existing tests and callers rely on alias identity and reset behavior.
  Alias removal needs a separate contract and caller inventory.
- Keep decomposition as only a one-off implementation detail. Rejected because
  the successful `PostingState` pilot establishes a reusable pattern that
  future parser-state work should follow.

## Consequences

Future parser runtime state work has a safer path: name one cluster, classify
truth ownership, preserve behavior, keep compatibility bridges, and validate
the affected surfaces before review.

The benefit is clearer architecture without a high-risk big-bang refactor. The
cost is that decomposition will be slower and more ceremonial. That cost is
intentional because parser runtime state is high risk.

Future contracts can cite this ADR to reject opportunistic parser-state cleanup
inside unrelated feature work. They can also cite the `PostingState` pilot as
evidence that behavior-preserving extraction is possible when the cluster is
small and well tested.

## Truth Ownership Impact

This ADR preserves `ADR-0001: Parser Owns Truth`.

Parser/state remains the owner of MTGA event interpretation, normalized match
facts, normalized game facts, parser-managed identity, deduplication, and final
reconciliation.

State decomposition does not move truth to workbook formulas, webhook
transport, Apps Script, analytics, local app UI, tests, compatibility aliases,
or AI-generated interpretation.

`PostingState` and similar downstream bookkeeping clusters may describe what
has already been emitted, posted, snapshotted, or delivered. They must not
reinterpret parser-owned facts.

## Protected Surfaces Touched

No runtime protected surfaces are touched by this ADR adoption document.

This ADR does not authorize protected-surface changes by implication. Future
state-cluster extractions that touch parser behavior, final reconciliation,
parser event classes, match/game identity, deduplication, workbook schema,
webhook payload shape, Apps Script behavior, analytics schema, local app
behavior, production behavior, AI/model-provider behavior, or generated/private
artifacts require explicit issue, contract, review, and validation authority.

The `PostingState` pilot touched parser runtime state under an explicit issue,
contract, implementation handoff, contract-test report, and PR review path.
That pilot is evidence for this strategy, not blanket authorization for future
runtime changes.

## Validation Or Review Evidence

This ADR adoption slice is docs-only. Runtime parser tests are not required for
the ADR creation because no runtime code changed.

The underlying pilot evidence is recorded in:

- `docs/contracts/parser_runtime_state_decomposition.md`
- `docs/implementation_handoffs/parser_runtime_state_decomposition_comparison.md`
- `docs/contract_test_reports/parser_runtime_state_decomposition.md`
- PR #308
- merge commit `19192f718f8b50e1d7fe962d02455b0c933985ad`

The contract-test report for the pilot recorded no blocking findings and
approved submitter routing after focused parser/runtime tests, parser
regression tests, app output tests, full tests, Ruff, whitespace validation,
agent docs validation, protected-surface scan, and secret/private-marker scan.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Route this Proposed ADR through Codex E contract testing before treating it
  as durable precedent.
- Future parser runtime state cluster extractions should cite this ADR and
  create a focused contract before editing code.
- Future alias removal or broad caller migration should be handled as a
  separate compatibility-cleanup issue and contract.

## Notes

This ADR records the strategy proven by the `PostingState` pilot. It does not
change parser behavior and does not close issue #307 by itself.
