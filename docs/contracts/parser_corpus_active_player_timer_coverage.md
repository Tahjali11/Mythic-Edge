# Parser Corpus Active Player Timer Coverage Contract

## Module

Active player timer corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`timer.active_player_timer` with repo-owned synthetic metadata and existing
parser-owned GRE timer normalization evidence. It proves only that Mythic Edge
has safe corpus metadata for an active-player timer-style GameState timer
record and the normalized timer view that already exists. It does not prove
inactivity timeouts, pre-match idle timers, clock pressure, rope behavior,
player mistakes, live private Player.log timer drift, diagnostics readiness,
release readiness, full timer parity, or full Mythic Edge corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/373
- Previous merge commit:
  `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-active-player-timer-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`
- target_artifact:
  `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_timer_normalization.md`
- `docs/implementation_handoffs/parser_timer_normalization_comparison.md`
- `docs/contract_test_reports/parser_timer_normalization.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_game_state_diff_mechanics.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, timer examples,
  or external corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`timer.active_player_timer` scenario family. GRE parser modules own the
underlying timer normalization behavior and GameState payload construction.
Corpus parity artifacts own only the coverage status claim that Mythic Edge has
safe repo-owned evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `timer.active_player_timer` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for timer behavior referenced by this coverage:

- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`

Truth owner for broader timer semantics:

- `docs/contracts/parser_timer_normalization.md`
- `docs/implementation_handoffs/parser_timer_normalization_comparison.md`
- `docs/contract_test_reports/parser_timer_normalization.md`

Truth boundary:

- `normalize_timer_record(...)` owns normalized evidence for one raw GRE timer
  record.
- `normalize_timer_array(...)` owns the normalized timer collection emitted as
  `GameStateEvent.payload["normalized_timers"]`.
- `timer_records_by_direct_seat(...)` owns grouping normalized timer records by
  direct timer-seat evidence only.
- `build_game_state_payload(...)` owns adding `normalized_timers` while
  preserving raw `timers`.
- `turn_info` context may be carried in `normalized_timers`, but it must not
  assign timer ownership or populate `direct_seat_ids`.
- Corpus parity artifacts own the report-only coverage row for
  `timer.active_player_timer`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, clock-pressure truth, inactivity timeout truth, rope truth,
  diagnostics truth, workbook truth, analytics truth, AI truth, coaching
  truth, merge readiness, deploy readiness, public/private release readiness,
  or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing GRE normalized_timers / GameState timer evidence
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for timer.active_player_timer
```

Forbidden reverse flow:

- Corpus coverage status must not change timer parser behavior.
- Corpus metadata must not change `normalized_timers` shape, raw `timers`
  preservation, GameState payload construction, schema snapshots, parser event
  classes, router semantics, parser state, diagnostics behavior, golden replay
  behavior, feature-equity behavior, runtime status behavior, workbook output,
  analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn synthetic active-player timer evidence into a
  claim about Arena rope behavior, inactivity timeout, pre-match idle, clock
  pressure, player mistakes, live private Player.log timer drift, private smoke
  readiness, or broad timer parity.

Protected surfaces explicitly not touched:

- parser behavior
- GRE timer normalization behavior
- GameState payload semantics
- raw `timers` preservation
- parser payload schema snapshots
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- golden replay behavior
- feature-equity behavior
- runtime status artifacts or schema
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_active_player_timer_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_gre_timers_parser.py`, only for focused test evidence that does
  not change behavior
- `tests/test_gre_game_state_parser.py`, only for focused test evidence that
  does not change behavior
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that must be routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- relevant diagnostics, golden replay, feature-equity, and schema snapshot
  tests

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- GRE timer normalization changes
- GameState payload shape changes
- parser event class changes
- schema snapshot changes
- timer unit inference changes
- clock-pressure analytics
- rope analytics
- inactivity timeout coverage
- pre-match idle coverage
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- Manasight corpus import
- diagnostics report changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime status changes
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public corpus interface remains the existing corpus parity report API:

```python
build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]

write_corpus_parity_report(...) -> dict[str, Any]

validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]
validate_session_ledger(payload: Mapping[str, Any]) -> list[str]
```

The command-line interface remains:

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

The parser behavior interface referenced by this contract is existing evidence
only:

```python
TIMER_RECORD_OBJECT = "mythic_edge_gre_timer"
TIMER_COLLECTION_OBJECT = "mythic_edge_gre_timers"
SCHEMA_VERSION = "parser_gre_timers.v1"

normalize_timer_record(raw_timer: object, *, source_index: int) -> dict[str, object]
normalize_timer_array(
    timers: object,
    *,
    turn_info: Mapping[str, object] | None = None,
) -> dict[str, object]
timer_records_by_direct_seat(
    normalized_timers: Mapping[str, object],
) -> dict[int, list[dict[str, object]]]
build_game_state_payload(message: dict[str, Any], gsm: dict[str, Any]) -> dict[str, Any]
```

No new public parser, runtime, workbook, webhook, Apps Script, analytics, AI, or
production interface is authorized by this contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`:

- Issue #375 is open under tracker #158.
- Tracker #158 remains open.
- Issue #372 is closed and PR #373 is merged into `codex/parser-parity`.
- The current corpus parity report is still partial:
  `partial_coverage_map_ready` with 45 scenario families, 6 committed
  families, and 20 missing families.
- `timer.active_player_timer` exists in the corpus taxonomy.
- `timer.active_player_timer` has no dedicated manifest entry or session
  ledger entry yet.
- `timer.inactivity_timeout` and `timer.pre_match_idle` remain uncovered
  families and are not owned by this issue.
- `src/mythic_edge_parser/parsers/gre/timers.py` already exists and exposes
  parser-owned timer normalization helpers.
- `src/mythic_edge_parser/parsers/gre/game_state.py` already adds
  `payload["normalized_timers"]` while preserving raw `payload["timers"]`.
- `tests/test_gre_timers_parser.py` covers timer IDs, direct seat evidence,
  time units, malformed input, non-mutation, contextual turn-info separation,
  and direct-seat grouping.
- `tests/test_gre_game_state_parser.py` covers additive `normalized_timers`
  GameState payload behavior and malformed timer-section fallback.

## Required Guarantees

### Scenario Family Boundary

Codex C may close only this corpus coverage gap:

- `timer.active_player_timer`

The implementation must not mark any of these families as covered:

- `timer.inactivity_timeout`
- `timer.pre_match_idle`
- `gameplay_stress.event_ordering`
- any connection, log-runtime, deck API, gameplay-stress, drift-debug, local
  diagnostics, analytics, workbook, AI, coaching, or release-readiness family
  not explicitly named above

### Coverage Status

The authorized V1 coverage status is:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

The coverage status must stay `covered_synthetic`, not `covered_committed`,
because this slice should use bounded synthetic metadata and focused tests, not
a committed raw or sanitized Player.log timer fixture.

### Manifest Entry

Codex C should add exactly one manifest entry for this scenario family:

```yaml
entry_id: "active_player_timer_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
authorized_by_contract: "docs/contracts/parser_corpus_active_player_timer_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  timer_normalization_test: "tests/test_gre_timers_parser.py"
  game_state_test: "tests/test_gre_game_state_parser.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "timer.active_player_timer"
parser_event_families:
  - "GameState"
parser_claim_families:
  - "gre_timer_normalization"
  - "active_player_timer_record"
  - "active_player_timer_direct_seat_evidence"
  - "timer_turn_info_context_boundary"
  - "timer_time_unit_boundary"
  - "timer_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
known_gaps:
  - "Synthetic active player timer metadata does not prove inactivity timeout, pre-match idle timers, rope behavior, clock pressure, live private Player.log timer drift, diagnostics readiness, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
review_notes:
  - "Synthetic active player timer coverage proves parser-owned normalized_timers GameState metadata only; it does not infer timer ownership from turn_info context or claim clock-pressure, rope, inactivity-timeout, gameplay-advice, analytics, AI, coaching, release, or production truth."
```

Codex C may adjust wording only if the final wording preserves all non-claims,
privacy boundaries, and scenario-family limits above.

### Session Ledger Entry

Codex C should add exactly one session ledger entry with this logical shape:

```yaml
session_id: "active_player_timer_synthetic_v1"
title: "Synthetic active player timer evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
authorized_by_contract: "docs/contracts/parser_corpus_active_player_timer_coverage.md"
scenario_families:
  - "timer.active_player_timer"
format_family: "timer_runtime"
match_shape: "active_player_timer_signal_only"
record_summary: "synthetic_timer_normalization_summary_only"
parser_coverage:
  event_families:
    GameState: 1
  unknown_entries: 0
  truncation_count: 0
  normalized_timer_records: 1
  active_player_timer_records: 1
  timer_records_with_direct_seat_evidence: 1
  timer_records_with_contextual_active_player: 1
  timer_records_with_seconds_values: 1
  timer_records_with_milliseconds_values: 1
  timer_degraded_records: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Synthetic active player timer metadata does not prove inactivity timeout, pre-match idle timers, rope behavior, clock pressure, private Player.log timer drift, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

The session ledger may describe counts and coverage evidence, but it must not
include raw log lines, raw GameState payloads, private paths, actual timer
capture excerpts, external corpus filenames, local diagnostics outputs, SQLite
files, runtime artifacts, decklists, or workbook exports.

### Active Player Timer Evidence Model

The synthetic evidence model may claim active-player timer coverage only when
focused tests demonstrate all of the following:

- `normalize_timer_array(...)` can normalize at least one timer record.
- The normalized collection has `object:
  "mythic_edge_gre_timers"` and `schema_version:
  "parser_gre_timers.v1"`.
- The record includes a stable `timer_id` and at least one timer type, name,
  state, or boolean timer field.
- The record includes direct timer-seat evidence such as `playerSeatId`.
- `timer_records_by_direct_seat(...)` groups by direct timer-seat evidence.
- Contextual `turn_info.active_player_seat_id` may be present, but it remains
  collection context and does not assign timer ownership.
- Explicit seconds and milliseconds timer fields are normalized by field-name
  unit policy.
- Raw `timers` remain preserved by `build_game_state_payload(...)`.
- The GameState payload contains additive `normalized_timers`.
- Malformed or degraded timer values remain reviewable evidence and do not
  become clean active-player timer facts.

If existing focused tests already prove the evidence model, Codex C may cite
them and keep timer tests unchanged. If any one of the above is not explicitly
covered, Codex C may add a focused synthetic timer test without touching parser
implementation.

### Non-Claims

The active-player timer corpus row must not claim:

- inactivity timeout coverage;
- pre-match idle timer coverage;
- real Arena rope behavior;
- clock-pressure analytics;
- gameplay advice;
- player-mistake labels;
- live private Player.log timer drift;
- diagnostics readiness;
- golden replay readiness;
- feature-equity readiness;
- release readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- hidden-card, decklist, or archetype truth.

## Inputs

Allowed inputs:

- the current issue #375 problem representation and tracker #158 context;
- existing Mythic Edge corpus manifest and session ledger JSON;
- existing synthetic timer normalization tests;
- existing GameState parser tests;
- existing timer normalization contract, implementation handoff, and
  contract-test report;
- current `codex/parser-parity` source and tests;
- public Manasight category names only through already merged taxonomy
  artifacts, if needed for wording.

Forbidden inputs:

- raw private Player.log excerpts;
- actual local GameState timer payloads;
- private local app-data contents;
- Manasight raw logs, compressed logs, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or raw corpus
  files;
- generated SQLite databases;
- runtime status files;
- failed posts;
- workbook exports;
- credentials, tokens, API keys, webhook URLs, or secrets;
- OpenAI/model-provider output.

## Outputs

Future Codex C should produce:

- an updated corpus manifest entry for
  `active_player_timer_synthetic_v1`;
- an updated session ledger entry for
  `active_player_timer_synthetic_v1`;
- focused corpus parity tests proving the row, session ledger, coverage matrix,
  summary count, and non-claims;
- focused timer/GameState tests only if existing tests do not already prove the
  evidence model;
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`;
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`.

Expected report behavior after implementation:

- `timer.active_player_timer` should become `covered_synthetic`.
- `covered_synthetic` should increase by one.
- `missing` should decrease by one.
- The overall corpus parity report should remain
  `partial_coverage_map_ready` while other gaps remain.
- `timer.inactivity_timeout` and `timer.pre_match_idle` should remain
  uncovered according to their pre-existing status.

## Invariants

- Corpus parity metadata must remain report-only.
- No raw/private/external timer payload may be committed.
- `source_privacy.raw_private_log_committed`,
  `source_privacy.external_logs_committed`, and
  `source_privacy.local_private_artifacts_committed` must remain `false`.
- `timer.active_player_timer` must have exactly one new Mythic Edge entry in
  this slice.
- The new manifest entry and session ledger entry must use the same stable id:
  `active_player_timer_synthetic_v1`.
- The coverage basis must include `parser_behavior_verified` and
  `fixture_metadata_only`.
- `parser_event_families` must name `GameState`, because timer evidence is
  exposed through `GameStateEvent.payload["normalized_timers"]`.
- `turn_info` context must remain context only; it must not assign timer
  ownership.
- Active-player timer coverage must not imply clock-pressure, rope,
  inactivity-timeout, or coaching conclusions.
- The implementation must not change parser behavior or protected surfaces.

## Error Behavior

- If `timer.active_player_timer` is already covered by another entry, Codex C
  must stop and route back to Codex B rather than adding a duplicate.
- If current timer tests no longer match `parser_timer_normalization.md`, Codex
  C must stop and route back to Codex B or D depending on whether the contract
  or implementation is wrong.
- If adding the corpus row requires changing parser source, parser event
  classes, GameState payload shape, schema snapshots, diagnostics reports,
  golden replay behavior, feature-equity behavior, runtime status, workbook
  schema, webhook payloads, Apps Script, output transport, analytics, AI, or
  production behavior, Codex C must stop and route back to Codex A or B.
- If validation finds raw/private/external content in the manifest, session
  ledger, tests, handoff, or report, Codex C must remove it from scope and
  rerun privacy checks before review.

## Side Effects

Codex B side effects:

- writes this contract only.

Future Codex C side effects authorized by this contract:

- edit committed corpus metadata and focused tests;
- write implementation handoff and contract-test report docs.

No runtime state, local private artifacts, generated databases, workbook tabs,
webhooks, Apps Script deployments, GitHub Actions gates, issues, PRs, trackers,
or production surfaces are changed by this contract.

## Dependency Order

1. Confirm branch base is `codex/parser-parity` at or after
   `41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83`.
2. Re-read this contract and the timer normalization contract/report.
3. Verify existing timer and GameState tests still prove the evidence model.
4. Add the manifest entry and session ledger entry.
5. Update `tests/test_corpus_parity_report.py` for the new entry, session
   ledger shape, coverage matrix row, summary counts, and non-claims.
6. Add focused timer/GameState tests only if required by the evidence model.
7. Run validation.
8. Write the implementation handoff and contract-test report.

## Compatibility

- Existing corpus manifest and session ledger schema versions remain
  unchanged.
- Existing corpus CLI and report JSON shape remain unchanged.
- Existing timer normalizer public constants and helper names remain
  unchanged.
- Existing GameState payload keys remain unchanged.
- Existing parser payload schema snapshot remains unchanged in this slice.
- Existing coverage statuses and coverage basis vocabulary remain unchanged.

## Tests Required

Minimum Codex C validation:

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m ruff check src tests
git diff --check
python3 tools/check_agent_docs.py
```

Recommended privacy/protected-surface validation:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_active_player_timer_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_gre_timers_parser.py \
  tests/test_gre_game_state_parser.py \
  docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_active_player_timer_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_gre_timers_parser.py \
  tests/test_gre_game_state_parser.py \
  docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_active_player_timer_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  tests/test_gre_timers_parser.py \
  tests/test_gre_game_state_parser.py \
  docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md \
  | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If `tools/check_secret_patterns.py` is unavailable on this branch, Codex C must
record that explicitly and rely on corpus report forbidden-content validation,
`git diff --check`, and manual changed-file inspection.

Optional adjacency checks if timer evidence is touched:

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
```

## Acceptance Criteria

- `docs/contracts/parser_corpus_active_player_timer_coverage.md` exists and is
  the contract source for issue #375.
- The corpus manifest contains exactly one
  `active_player_timer_synthetic_v1` entry.
- The session ledger contains exactly one
  `active_player_timer_synthetic_v1` session.
- `timer.active_player_timer` reports `covered_synthetic`.
- `timer.inactivity_timeout` and `timer.pre_match_idle` do not become covered.
- Corpus report validation passes with no forbidden private or external
  content findings.
- Focused tests prove the manifest row, session row, report matrix row, summary
  count changes, and non-claim wording.
- Existing timer normalization and GameState tests pass.
- No parser behavior, protected surface, raw/private artifact, external corpus
  import, analytics truth, AI truth, coaching behavior, release policy, or
  production behavior changes.
- Codex C produces an implementation handoff and a contract-test report.

## Open Questions And Suspected Gaps

- Existing timer tests may already prove most active-player timer evidence, but
  Codex C should verify whether they prove a clean non-degraded active-player
  timer record with direct seat evidence and explicit second/millisecond units.
  If not, Codex C may add a focused synthetic test without changing parser
  implementation.
- The scenario family name says "active player timer", but the parser does not
  infer timer ownership from `turn_info`. This contract intentionally treats
  active-player context as evidence context only.
- Broader timer drift and live Arena timer behavior remain future work.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #375, active player timer corpus coverage.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/375
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/372
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/373
- Previous merge commit: 41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83
- Base branch: codex/parser-parity
- Implementation branch: codex/parser-corpus-active-player-timer-coverage
- Contract: docs/contracts/parser_corpus_active_player_timer_coverage.md
- Expected handoff: docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md
- Expected report: docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md

Goal:
Implement the smallest metadata/test-only package needed to mark exactly timer.active_player_timer as covered_synthetic in the parser corpus parity report, using existing GRE timer normalization and GameState timer evidence.

Do:
- Compare current corpus manifest, session ledger, timer tests, GameState tests, and corpus report behavior against the contract before editing.
- Add the active_player_timer_synthetic_v1 manifest entry and session ledger entry.
- Update tests/test_corpus_parity_report.py for the new entry, session entry, matrix row, summary counts, and non-claims.
- Add focused synthetic timer or GameState tests only if existing tests do not prove the contracted active-player timer evidence model.
- Produce docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md.
- Produce docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md.

Do not:
- Change parser behavior, GRE timer normalization behavior, GameState payload semantics, raw timers preservation, parser event classes, router semantics, parser state final reconciliation, match/game identity, deduplication, diagnostics behavior, golden replay behavior, feature-equity behavior, runtime status artifacts, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, or production behavior.
- Mark timer.inactivity_timeout or timer.pre_match_idle as covered.
- Add any forbidden private, external, generated, delivery, workbook, or
  credential artifact named in this contract.
- Claim clock pressure, rope behavior, inactivity timeout, player mistakes, gameplay advice, diagnostics readiness, release readiness, private smoke success, analytics truth, AI truth, coaching truth, or full corpus parity.
- Target main directly.
- Close tracker #158.
- Stage or commit unless explicitly asked.

Validation:
Run at minimum:
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m ruff check src tests
git diff --check
python3 tools/check_agent_docs.py

Also run changed-file secret/protected-surface/selector checks if the tools are available on this branch.

End with:
- role performed
- files changed
- validation run
- remaining risks
- next recommended role
- workflow_handoff block to Codex E
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/375"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/372"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/373"
  previous_merge_commit: "41e0c4a152ceb695cffd47cf3d3fb7fc3c005d83"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_active_player_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md"
  verdict: "contract_ready_for_synthetic_active_player_timer_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-active-player-timer-coverage"
  base_branch: "codex/parser-parity"
  validation:
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py"
    - "python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m ruff check src tests"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not change parser behavior, GRE timer normalization behavior, GameState payload semantics, raw timers preservation, parser event classes, router semantics, parser state final reconciliation, match/game identity, deduplication, diagnostics behavior, golden replay behavior, feature-equity behavior, runtime status artifacts, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics truth, AI truth, coaching behavior, CI gates, merge policy, deploy policy, or production behavior."
    - "Do not mark timer.inactivity_timeout or timer.pre_match_idle as covered."
    - "Do not commit any forbidden private, external, generated, delivery, workbook, or credential artifact named in this contract."
    - "Do not claim clock pressure, rope behavior, inactivity timeout, player mistakes, gameplay advice, diagnostics readiness, release readiness, private smoke success, analytics truth, AI truth, coaching truth, or full corpus parity."
```
