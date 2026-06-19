# Parser Corpus Timer Inactivity Timeout External Boundary Contract

## Module

Parser corpus parity coverage boundary for `timer.inactivity_timeout`.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/448
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/446
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/447
- Previous merge commit: `bad79df689a36b9bcdd5c486aba2b75e98e723dc`
- Base branch inspected: `main`
- Contract branch: `codex/parser-corpus-timer-inactivity-timeout-boundary-448`
- Risk tier: High
- Status: contract only

## Purpose

Define the safest corpus/provenance boundary for
`timer.inactivity_timeout`, which remains blocked by external-reference
evidence. This contract prevents adjacent timer coverage from being overread
as inactivity-timeout support.

This is corpus parity boundary work, not parser behavior work. The contract
does not authorize parser changes, timer normalization changes, manifest
promotion, session-ledger changes, private evidence collection, live MTGA
checks, or release/readiness claims.

## Observed Current Behavior

Observed on `main` at
`bad79df689a36b9bcdd5c486aba2b75e98e723dc`:

- Issue #448 is open.
- Tracker #158 remains open.
- Parent issue #434 remains open.
- PR #447 is merged into `main`.
- The corpus parity CLI is expected to report:
  `partial_coverage_map_ready`.
- `timer.inactivity_timeout` is represented only by
  `external_reference_category_boundary`.
- `timer.inactivity_timeout` currently has:
  - `coverage_status`: `blocked_external_boundary`
  - `coverage_basis`: `["external_reference_only"]`
  - `mythic_edge_entries`: `["external_reference_category_boundary"]`
  - `parser_event_families`: `[]`
- `external_reference_category_boundary` also covers:
  - `gameplay_stress.conjure`
  - `gameplay_stress.spellbook`
  - `drift_debug.recycle_or_rollback`
- `timer.active_player_timer` is `covered_synthetic` through
  `active_player_timer_synthetic_v1`.
- `timer.pre_match_idle` is `covered_synthetic` through
  `pre_match_idle_timer_synthetic_v1`.
- `src/mythic_edge_parser/parsers/gre/timers.py` preserves and normalizes
  generic timer fields. It recognizes time-like field names containing words
  such as `timeout`, `deadline`, `rope`, and `clock`, but generic preservation
  does not prove Arena inactivity-timeout semantics.
- `tests/test_gre_timers_parser.py` covers a clean active-player timer shape
  and a clean pre-match idle-style shape. Those tests do not prove inactivity
  timeout behavior, rope behavior, clock pressure, player waiting semantics, or
  live Arena timeout handling.
- `tests/test_corpus_parity_report.py` currently asserts that
  `timer.inactivity_timeout` remains `blocked_external_boundary`.

## Scope Decision

Selected path: remain `blocked_external_boundary`.

Codex B considered these paths:

1. Move `timer.inactivity_timeout` to `covered_report_only`.
2. Add synthetic or committed fixture coverage.
3. Define a future evidence-generation prerequisite and keep the row blocked.
4. Leave the broad external-reference row without a sharper contract.

This contract selects path 3.

Reasoning:

- Existing active-player timer coverage proves only a bounded synthetic timer
  record with direct seat evidence.
- Existing pre-match idle timer coverage proves only a bounded synthetic timer
  record with no direct seat evidence.
- Neither adjacent row proves an inactivity timeout, rope timeout, timeout
  expiry, player waiting timeout, clock pressure, timeout cause, or local/live
  MTGA behavior.
- Current timer normalization can preserve labels and time-like values, but
  it does not classify a timer as an Arena inactivity timeout.
- Public external taxonomy can name an inactivity-timeout family, but it is
  not Mythic Edge evidence.
- A future move out of `blocked_external_boundary` needs a separate evidence
  model. That model may be a reduced safe synthetic inactivity-timeout shape,
  an approval-gated private evidence packet, or a parser-evidence pipeline
  output after later evidence issues. This contract does not choose that later
  implementation path.

This decision does not authorize source-code changes, manifest status changes,
session-ledger changes, focused test changes, private/live execution, or
status promotion for this row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns the corpus coverage boundary for
`timer.inactivity_timeout`. GRE timer parser modules own timer normalization
behavior. GameState parser modules own GameState event emission. Corpus parity
may describe why current timer surfaces are insufficient, but it must not
reinterpret them as inactivity-timeout support.

## Internal Project Area

Corpus / Provenance, with Quality / Governance support for contract,
validation, review, and protected-surface checks.

This slice is not a parser behavior module, timer-normalization module,
GameState module, diagnostics implementation, drift-report implementation,
local app watcher implementation, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, readiness gate, or production
module.

## Truth Owner

Truth owner for current corpus coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent timer behavior:

- `docs/contracts/parser_timer_normalization.md`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`

Truth owners for adjacent corpus timer coverage:

- `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`
- `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`

## Bridge-Code Status

Bridge-code status: deferred future boundary.

No bridge code is authorized in this contract. Codex C is not required for a
metadata implementation because the selected row stays blocked. If the team
wants a no-change verification package, Codex C must produce docs-only
comparison/report artifacts and leave corpus metadata, parser code, and tests
untouched.

## Files Owned By This Contract

This contract directly owns:

- `docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md`

Expected optional no-change verification artifacts:

- `docs/implementation_handoffs/parser_corpus_timer_inactivity_timeout_external_boundary_comparison.md`
- `docs/contract_test_reports/parser_corpus_timer_inactivity_timeout_external_boundary.md`

This contract does not authorize edits to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`
- parser behavior, parser events, router behavior, diagnostics, drift reports,
  golden replay, feature-equity, evidence ledger, workbook/webhook/App Script,
  analytics, AI, coaching, CI, readiness, deploy, or production surfaces

## Public Interface

This contract defines no new runtime public API.

The current report-facing interface remains the corpus parity matrix row for
`timer.inactivity_timeout`:

```yaml
scenario_family: "timer.inactivity_timeout"
coverage_status: "blocked_external_boundary"
coverage_basis:
  - "external_reference_only"
mythic_edge_entries:
  - "external_reference_category_boundary"
external_reference_status: "reference_category_not_checked"
```

No new manifest entry, session-ledger entry, parser event, timer event,
diagnostics field, drift field, runtime status field, workbook row, webhook
payload field, Apps Script mapping, analytics view, or AI/coaching field is
authorized by this contract.

## Required Guarantees

### Status Boundary

`timer.inactivity_timeout` must remain:

```yaml
coverage_status: "blocked_external_boundary"
coverage_basis:
  - "external_reference_only"
```

No implementation may promote this row to `covered_report_only`,
`covered_synthetic`, `covered_committed`, `partial`, or
`blocked_private_evidence` without a later explicit contract.

### Adjacent Timer Boundaries

Current adjacent timer rows must not be reinterpreted:

- `timer.active_player_timer` stays limited to active-player timer synthetic
  metadata.
- `timer.pre_match_idle` stays limited to pre-match idle synthetic metadata.
- Neither row proves `timer.inactivity_timeout`.
- Neither row may be used as a fallback or substitute coverage source for
  inactivity-timeout behavior.

### External Reference Boundary

The external-reference row may name `timer.inactivity_timeout`, but naming the
family does not prove:

- parser support;
- live Arena inactivity-timeout behavior;
- rope behavior;
- clock-pressure truth;
- timeout expiry;
- player waiting behavior;
- player mistake labels;
- gameplay advice;
- timer drift health;
- private smoke success;
- release readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- full corpus parity.

### Future Evidence Prerequisites

A future status-change contract must define at least one of these evidence
paths before promotion:

- a Mythic Edge-owned synthetic inactivity-timeout evidence model that proves
  a dedicated inactivity-timeout shape without claiming live Arena behavior;
- an approval-gated private-evidence execution packet that uses local-only
  collection, redaction, retention, and public-summary controls;
- a parser-evidence pipeline output from later evidence issues that defines
  an allowed, non-private, reviewable evidence artifact.

Any future path must state exactly what is proved and what remains a non-claim.

### Protected Surface Guarantees

This contract must not change:

- parser behavior;
- timer normalization behavior;
- GameState payload semantics;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics report shape;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status files;
- failed posts;
- workbook exports;
- analytics truth;
- AI truth;
- coaching behavior;
- OpenAI/model-provider behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

## Inputs

Allowed Codex B inputs:

- GitHub issue #448, tracker #158, parent issue #434, previous issue #446,
  and PR #447 metadata.
- Existing repo contracts, implementation handoffs, and contract-test reports.
- Existing corpus manifest and session ledger metadata.
- Existing corpus parity report code and focused tests.
- Existing GRE timer normalization and GameState timer code/tests as reference
  context only.
- Existing public external taxonomy references already represented in Mythic
  Edge corpus parity artifacts.

Forbidden Codex B inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- timer drift checks;
- firewall/drop/network/packet/OS/router checks;
- screenshots;
- exact private paths;
- raw hashes;
- runtime logs;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- decklists, card choices, private strategy notes, or private reports;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source,
  or external corpus contents.

## Outputs

Allowed output for this contract:

- A Markdown contract file describing the blocked external-boundary decision.
- Optional future docs-only no-change comparison/report artifacts.
- A workflow handoff to Codex E by default, or an optional no-change Codex C
  route if the team explicitly requests verification artifacts.

Forbidden output:

- changed parser code;
- changed corpus manifest or session ledger;
- changed tests;
- raw or private evidence;
- generated data;
- runtime artifacts;
- private reports;
- readiness claims;
- status promotion for `timer.inactivity_timeout` or any blocked row.

## Unknowns

- Whether Arena exposes a stable, explicit inactivity-timeout payload shape in
  public or sanitized Mythic Edge-owned evidence.
- Whether any local private evidence window can be safely summarized without
  revealing raw log content, local paths, app-data contents, or gameplay
  context.
- Whether an eventual synthetic inactivity-timeout shape would be useful enough
  to justify a status change, or whether the family should stay blocked until
  approved private evidence exists.
- Whether later parser-evidence pipeline issues #381 through #387 will create
  a safe, non-private evidence source for this row.

## Suspected Gaps

- Current timer normalization preserves generic time-like fields but does not
  classify an inactivity-timeout event.
- Current corpus metadata groups `timer.inactivity_timeout` under a broad
  external-reference row with other unrelated external-boundary families.
- Adjacent synthetic timer coverage may tempt over-claiming unless
  inactivity-timeout remains explicitly blocked.
- There is no committed Mythic Edge-owned fixture, session-ledger entry,
  diagnostics report, drift report, or evidence-ledger artifact dedicated to
  inactivity timeout.

## Invariants

- `timer.inactivity_timeout` remains `blocked_external_boundary`.
- `timer.active_player_timer` remains `covered_synthetic`.
- `timer.pre_match_idle` remains `covered_synthetic`.
- `gameplay_stress.conjure` and `gameplay_stress.spellbook` remain later
  external-boundary candidates and must not be promoted by this issue.
- `drift_debug.recycle_or_rollback` remains governed by
  `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`.
- External-reference metadata is not parser truth.
- Corpus parity reports are review metadata, not readiness, production,
  analytics, AI, or coaching authority.

## Error Behavior

If validation observes `timer.inactivity_timeout` as anything other than
`blocked_external_boundary`, stop and route back to Codex B unless the status
change is explained by a later merged contract.

If validation requires private/live data, stop and record the blocked
condition. Do not run private/live checks.

If any proposed implementation needs parser behavior, timer normalization,
GameState, diagnostics, drift-report, runtime status, workbook, webhook, Apps
Script, analytics, AI, coaching, CI, merge, deploy, production, or final
integration changes, stop and create or request a new scoped contract.

If any proposed implementation would import, copy, mirror, summarize, hash, or
commit private logs or external corpus contents, reject it and keep the row
blocked.

## Side Effects

This contract has no runtime side effects.

The only intended repository side effect is adding this contract file.

## Dependency Order

Current dependencies:

1. `docs/contracts/parser_corpus_parity_expansion.md`
2. `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
3. `docs/contracts/parser_timer_normalization.md`
4. `docs/contracts/parser_corpus_active_player_timer_coverage.md`
5. `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`
6. `docs/contracts/parser_corpus_drift_recycle_rollback_external_boundary.md`

Potential future dependencies before promotion:

- parser-evidence pipeline issues #381 through #387;
- an approval-gated private evidence packet;
- a dedicated synthetic inactivity-timeout evidence contract;
- a later contract defining an allowed sanitized fixture or report-only
  summary.

## Compatibility

This contract is compatible with the current corpus parity vocabulary because
it preserves the existing `blocked_external_boundary` status and existing
external-reference entry.

The contract deliberately avoids requiring new status vocabulary, new coverage
basis vocabulary, new parser events, new runtime fields, new diagnostics
fields, new workbook fields, or new downstream consumer behavior.

## Tests Required

For this contract-only pass:

- Documentation-only checks are sufficient.
- No parser tests are required to pass before the contract exists.
- No private/live/timer-drift checks are allowed.

For optional no-change Codex C verification:

- Run the corpus parity CLI and confirm `timer.inactivity_timeout` remains
  `blocked_external_boundary`.
- Run focused corpus parity tests that assert the matrix row.
- Run existing timer tests only as reference evidence that adjacent timer rows
  remain bounded.
- Run protected-surface and secret/private-marker checks scoped to changed
  files.
- Produce a no-change implementation handoff and contract-test report.

Expected commands for optional verification:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

## Acceptance Criteria

- `docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md`
  exists.
- The contract selects `remain blocked_external_boundary`.
- The contract does not authorize manifest, session-ledger, parser, or test
  changes.
- The contract states that adjacent `timer.active_player_timer` and
  `timer.pre_match_idle` coverage does not prove inactivity-timeout support.
- The contract defines future evidence prerequisites before any status change.
- The contract preserves protected surfaces and non-claims.
- The workflow handoff routes to Codex E by default, with optional no-change
  Codex C verification only if explicitly requested.

## Next Workflow Action

Recommended next role: Codex E: Module Reviewer, if the team wants an
independent contract-only review before submitter work.

Codex C is not required for a metadata implementation because this contract
does not authorize corpus status promotion, manifest edits, session-ledger
edits, parser edits, or focused test changes. If the team wants a no-change
verification package anyway, Codex C must produce docs-only comparison/report
artifacts and leave corpus metadata untouched.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #448.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/448

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/446

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/447

Previous merge commit:
bad79df689a36b9bcdd5c486aba2b75e98e723dc

Base branch:
main

Contract:
docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md

Goal:
Review the contract-only boundary for timer.inactivity_timeout. Verify that the selected status remains blocked_external_boundary, no Codex C metadata promotion is authorized by default, and adjacent active-player/pre-match timer coverage is not overread as inactivity-timeout support.

Review:
- docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md
- docs/contracts/parser_corpus_active_player_timer_coverage.md
- docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md
- docs/contracts/parser_timer_normalization.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/parsers/gre/timers.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_corpus_parity_report.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_parser.py

Lead with findings. If no issues are found, say so and record residual risks.

Do not implement code. Do not target main directly. Do not close #158, #434, or #448. Do not run private Player.log, UTC_Log, app-data, live MTGA, timer drift, firewall/drop, network, packet, OS/router, diagnostics, or private smoke checks. Do not read private logs. Do not promote timer.inactivity_timeout or any blocked row. Do not claim parser support, inactivity-timeout behavior, rope behavior, clock-pressure truth, player-mistake labels, gameplay advice, timer drift health, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity.
```

Optional Codex C prompt, only if the team explicitly wants a no-change
verification package:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #448.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/448

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Parent/private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Contract:
docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md

Goal:
Produce a no-change docs verification package for the timer.inactivity_timeout external-boundary contract. Do not promote the row or edit corpus metadata.

Expected artifacts:
- docs/implementation_handoffs/parser_corpus_timer_inactivity_timeout_external_boundary_comparison.md
- docs/contract_test_reports/parser_corpus_timer_inactivity_timeout_external_boundary.md

Do:
- Verify main includes bad79df689a36b9bcdd5c486aba2b75e98e723dc.
- Confirm timer.inactivity_timeout remains blocked_external_boundary.
- Confirm timer.active_player_timer remains covered_synthetic.
- Confirm timer.pre_match_idle remains covered_synthetic.
- Confirm gameplay_stress.conjure and gameplay_stress.spellbook remain blocked_external_boundary.
- Confirm no private/live/timer-drift checks are needed.
- Record validation and residual risks.

Do not:
- Implement code.
- Edit tests.
- Edit corpus manifest or session ledger.
- Promote timer.inactivity_timeout or any blocked row.
- Run private Player.log, app-data, live MTGA, timer drift, firewall/drop, network, packet, OS/router, diagnostics, or private smoke checks.
- Read private logs.
- Claim parser support, inactivity-timeout behavior, rope behavior, clock-pressure truth, player-mistake labels, gameplay advice, timer drift health, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/448"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/446"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/447"
  previous_merge_commit: "bad79df689a36b9bcdd5c486aba2b75e98e723dc"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #448"
  target_artifact: "docs/contracts/parser_corpus_timer_inactivity_timeout_external_boundary.md"
  optional_no_change_c_artifacts:
    - "docs/implementation_handoffs/parser_corpus_timer_inactivity_timeout_external_boundary_comparison.md"
    - "docs/contract_test_reports/parser_corpus_timer_inactivity_timeout_external_boundary.md"
  verdict: "timer_inactivity_timeout_contract_preserves_blocked_external_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-timer-inactivity-timeout-boundary-448"
  base_branch: "main"
  selected_family: "timer.inactivity_timeout"
  status_decision: "remain_blocked_external_boundary"
  implementation_authorized: "no_metadata_promotion_by_default"
  tracker_status: "open"
  parent_issue_status: "open"
  later_external_candidates:
    - "gameplay_stress.conjure"
    - "gameplay_stress.spellbook"
  staged_later_sequence:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/381"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/382"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/383"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/384"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/386"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/385"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/387"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close parent issue #434 without explicit authorization."
    - "Do not run private Player.log, app-data, live MTGA, timer drift, firewall/drop, network, packet, OS/router, diagnostics, or private smoke checks."
    - "Do not read private logs in Codex B/C/E."
    - "Do not promote timer.inactivity_timeout or any blocked row by default."
    - "Do not claim parser support, inactivity-timeout behavior, rope behavior, clock-pressure truth, player-mistake labels, gameplay advice, timer drift health, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
