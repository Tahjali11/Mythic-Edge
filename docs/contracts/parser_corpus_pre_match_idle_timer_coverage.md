# Parser Corpus Pre-Match Idle Timer Coverage Contract

## Module

Pre-match idle timer corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`timer.pre_match_idle` with repo-owned synthetic metadata and existing
parser-owned GRE timer normalization evidence. It proves only that Mythic Edge
can normalize a bounded pre-match idle-style timer record that has no direct
seat ownership, has explicit seconds/milliseconds timer values, and stays
inside corpus metadata. It does not prove actual live Arena pre-match idle
behavior, inactivity timeouts, rope behavior, clock pressure, player mistakes,
private smoke readiness, release readiness, analytics truth, AI truth,
coaching truth, or production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/379
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/380
- Previous merge commit:
  `8359148957fd9f37399dff6e12a834cf78373e5c`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-pre-match-idle-timer-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `8359148957fd9f37399dff6e12a834cf78373e5c`
- target_artifact:
  `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`
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
- `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`
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

## Scope Decision

Implementation may proceed as safe synthetic coverage.

Codex B considered the three paths named by issue #389:

1. Safe synthetic coverage.
2. Report-only coverage.
3. Evidence-prerequisite or approval-gated private smoke planning before
   coverage.

Selected path: safe synthetic coverage.

Reasoning:

- Existing GRE timer normalization accepts arbitrary timer type/name/state
  strings and deterministic time-value fields without changing parser source.
- A synthetic pre-match idle-style timer can be represented with explicit
  `timerType`, `timerName`, `timerState`, seconds, and milliseconds values.
- The synthetic shape can deliberately omit direct seat fields, proving the
  "no direct player ownership" boundary that separates pre-match idle evidence
  from active-player timer evidence.
- No private live log, external corpus record, generated report, or parser
  behavior change is required for the narrow coverage row.

This decision is intentionally narrow. It does not claim live MTGA pre-match
idle behavior has been observed, that this synthetic shape matches every Arena
payload variant, or that Mythic Edge understands inactivity timeout or rope
semantics.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the `timer.pre_match_idle`
scenario family. GRE parser modules own the underlying timer normalization
behavior and GameState payload construction. Corpus parity artifacts own only
the coverage status claim that Mythic Edge has safe repo-owned synthetic
evidence for this narrow family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence, but it is not a Parser behavior module and is not a
runtime, diagnostics, analytics, workbook, local app, AI, coaching, release,
or production module.

## Truth Owner

Truth owner for `timer.pre_match_idle` coverage status:

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
- `docs/contracts/parser_corpus_active_player_timer_coverage.md`
- `docs/implementation_handoffs/parser_corpus_active_player_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_active_player_timer_coverage.md`

Truth boundary:

- `normalize_timer_record(...)` owns normalized evidence for one raw GRE timer
  record.
- `normalize_timer_array(...)` owns the normalized timer collection emitted as
  `GameStateEvent.payload["normalized_timers"]`.
- `timer_records_by_direct_seat(...)` owns grouping normalized timer records by
  direct timer-seat evidence only.
- `build_game_state_payload(...)` owns adding `normalized_timers` while
  preserving raw `timers`.
- A synthetic pre-match idle timer record may prove timer-label preservation,
  seconds/milliseconds normalization, and no direct-seat evidence.
- A synthetic pre-match idle timer record must not assign player ownership
  from contextual turn information or from the phrase "pre-match".
- Corpus parity artifacts own only the coverage row for `timer.pre_match_idle`.
- Corpus coverage status is review metadata. It is not parser truth, runtime
  health truth, clock-pressure truth, inactivity-timeout truth, rope truth,
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
  -> corpus parity coverage row for timer.pre_match_idle
```

Forbidden reverse flow:

- Corpus coverage status must not change timer parser behavior.
- Corpus metadata must not change `normalized_timers` shape, raw `timers`
  preservation, GameState payload construction, schema snapshots, parser event
  classes, router semantics, parser state, diagnostics behavior, golden replay
  behavior, feature-equity behavior, local runtime health behavior, workbook
  output, analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn synthetic pre-match idle timer evidence into a
  claim about Arena rope behavior, inactivity timeout, player waiting behavior,
  clock pressure, player mistakes, live private Player.log timer drift, private
  smoke readiness, or broad timer parity.

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
- local runtime health artifacts or schema
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

- `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_gre_timers_parser.py`, only for focused synthetic test evidence
  that does not change behavior
- `tests/test_gre_game_state_parser.py`, only for focused test evidence that
  does not change behavior
- `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`

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
- active-player timer coverage changes
- live private smoke execution
- committed raw log fixtures
- private Player.log fixture work
- Manasight corpus import
- diagnostics report changes
- golden replay behavior changes
- feature-equity behavior changes
- local runtime health changes
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public corpus interface remains the existing corpus parity report API:

```text
build_corpus_parity_report(
    manifest_path,
    *,
    session_ledger_path=None,
    feature_equity_report=None,
    external_reference=None,
) -> dict

write_corpus_parity_report(...) -> dict

validate_corpus_manifest(payload) -> list[str]
validate_session_ledger(payload) -> list[str]
```

The command-line interface remains:

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

The parser behavior interface referenced by this contract is existing evidence
only:

```text
TIMER_RECORD_OBJECT = "mythic_edge_gre_timer"
TIMER_COLLECTION_OBJECT = "mythic_edge_gre_timers"
SCHEMA_VERSION = "parser_gre_timers.v1"

normalize_timer_record(raw_timer, *, source_index) -> dict
normalize_timer_array(timers, *, turn_info=None) -> dict
timer_records_by_direct_seat(normalized_timers) -> dict
build_game_state_payload(message, gsm) -> dict
```

No new public parser, runtime, workbook, webhook, Apps Script, analytics, AI, or
production interface is authorized by this contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`8359148957fd9f37399dff6e12a834cf78373e5c`:

- Issue #389 is open under tracker #158.
- Tracker #158 remains open.
- Issue #379 is closed and PR #380 is merged into `codex/parser-parity`.
- The current corpus parity report is still partial:
  `partial_coverage_map_ready` with 45 scenario families, 6 committed
  families, 11 synthetic families, 2 report-only families, and 17 missing
  families.
- `timer.active_player_timer` is `covered_synthetic` through
  `active_player_timer_synthetic_v1`.
- `timer.inactivity_timeout` remains `blocked_external_boundary`.
- `timer.pre_match_idle` remains `missing`.
- `src/mythic_edge_parser/parsers/gre/timers.py` exposes timer normalization
  helpers.
- A synthetic pre-match idle-style timer shape with `timerType`,
  `timerName`, `timerState`, seconds, and milliseconds values normalizes as a
  clean `mythic_edge_gre_timers` collection with:
  - 1 total record;
  - 0 degraded records;
  - no review-required flag;
  - no direct seat IDs;
  - 1 seconds value;
  - 1 milliseconds value.
- `tests/test_gre_timers_parser.py` already covers active-player timer
  evidence but does not yet pin a pre-match idle no-direct-seat shape.
- `tests/test_corpus_parity_report.py` currently asserts
  `timer.pre_match_idle` remains `missing`.

## Required Guarantees

### Scenario Family Boundary

Codex C may close only this corpus coverage gap:

- `timer.pre_match_idle`

The implementation must not mark any of these families as covered or changed:

- `timer.inactivity_timeout`
- `timer.active_player_timer`
- `connection.firewall_or_network_drop`
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

Rationale:

- The coverage uses synthetic timer metadata, not private or external log
  material.
- The current timer normalizer can represent the synthetic pre-match idle shape
  through existing parser behavior.
- A focused test can verify that no direct-seat ownership is inferred.

Codex C must not use `covered_committed`, `covered_report_only`,
`partial`, `blocked_private_evidence`, or `blocked_external_boundary` for this
family in issue #389 unless it routes back to Codex B with evidence that the
selected synthetic path is unsafe.

### Synthetic Timer Shape

The synthetic test evidence should use a minimal timer record shaped like:

```yaml
timerId: 21
timerType: "TimerType_PreMatchIdle"
timerName: "PreMatchIdleTimer"
timerState: "waiting"
idleSeconds: 90
durationMs: 90000
running: false
```

Expected normalized behavior:

- Collection object: `mythic_edge_gre_timers`
- Schema version: `parser_gre_timers.v1`
- `total_records == 1`
- `degraded_records == 0`
- `review_required is false`
- `timer_ids == [21]`
- `timer_types == ["TimerType_PreMatchIdle"]`
- `direct_seat_ids == []`
- `contextual_turn_info` values are empty when no turn info is supplied.
- Record object: `mythic_edge_gre_timer`
- Record `timer_type == "TimerType_PreMatchIdle"`
- Record `timer_name == "PreMatchIdleTimer"`
- Record `timer_state == "waiting"`
- Record seat fields are all empty.
- Record `direct_seat_ids == []`
- Record `idleSeconds` normalizes as seconds.
- Record `durationMs` normalizes as milliseconds.
- Record `evidence_status == "observed"`
- Record `value_source == "derived"`
- Record `confidence == "high"`
- Record `degradation_flags == []`
- `timer_records_by_direct_seat(...) == {}`

Codex C may adjust the synthetic timer id if needed, but must preserve the
no-direct-seat, seconds/milliseconds, and non-degraded boundaries.

### Manifest Entry

Codex C should add exactly one corpus manifest entry for this family.

Recommended entry id:

```text
pre_match_idle_timer_synthetic_v1
```

Recommended logical shape:

```yaml
entry_id: "pre_match_idle_timer_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
authorized_by_contract: "docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  timer_normalization_test: "tests/test_gre_timers_parser.py"
  game_state_test: "tests/test_gre_game_state_parser.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "timer.pre_match_idle"
parser_event_families:
  - "GameState"
parser_claim_families:
  - "gre_timer_normalization"
  - "pre_match_idle_timer_record"
  - "pre_match_idle_no_direct_seat_boundary"
  - "pre_match_idle_time_unit_boundary"
  - "timer_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

Required known gap:

```text
Synthetic pre-match idle timer metadata does not prove live Arena pre-match
idle behavior, inactivity timeout, rope behavior, clock pressure, player
waiting behavior, player mistakes, private Player.log timer drift, diagnostics
readiness, release readiness, analytics truth, AI truth, coaching truth, or
production behavior.
```

Required review note:

```text
Synthetic pre-match idle timer coverage proves parser-owned normalized_timers
GameState metadata for a no-direct-seat timer shape only; it does not infer
player ownership, inactivity timeout, rope behavior, clock pressure, gameplay
advice, analytics, AI, coaching, release, or production truth.
```

### Session Ledger Entry

Codex C should add a matching session ledger row.

Recommended logical shape:

```yaml
session_id: "pre_match_idle_timer_synthetic_v1"
title: "Synthetic pre-match idle timer evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
authorized_by_contract: "docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md"
scenario_families:
  - "timer.pre_match_idle"
format_family: "timer_runtime"
match_shape: "pre_match_idle_timer_signal_only"
record_summary: "synthetic_timer_normalization_summary_only"
parser_coverage:
  event_families:
    GameState: 1
  unknown_entries: 0
  truncation_count: 0
  normalized_timer_records: 1
  pre_match_idle_timer_records: 1
  timer_records_with_direct_seat_evidence: 0
  timer_records_without_direct_seat_evidence: 1
  timer_records_with_contextual_active_player: 0
  timer_records_with_seconds_values: 1
  timer_records_with_milliseconds_values: 1
  timer_degraded_records: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Synthetic pre-match idle timer metadata does not prove live Arena pre-match idle behavior, inactivity timeout, rope behavior, clock pressure, private Player.log timer drift, release readiness, analytics truth, AI truth, coaching truth, or production behavior."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

Codex C may adjust summary count field names to match existing session-ledger
style, but must preserve the meaning and privacy boundary.

### Non-Claims

The pre-match idle coverage row must explicitly not claim:

- full Mythic Edge corpus parity;
- parser support from corpus metadata alone;
- live Arena pre-match idle behavior;
- private Player.log timer drift health;
- inactivity timeout coverage;
- rope behavior;
- clock pressure;
- player waiting behavior;
- player mistakes;
- gameplay advice;
- hidden-card inference;
- archetype classification;
- diagnostics readiness;
- release readiness;
- analytics truth;
- AI truth;
- coaching truth;
- merge readiness;
- deploy readiness;
- production behavior;
- tracker #158 completion.

### Deferred Timer Families

`timer.inactivity_timeout` remains blocked by external boundary. It needs a
separate problem representation and contract.

`timer.active_player_timer` remains covered by
`active_player_timer_synthetic_v1`; Codex C must not alter that row except for
adjacent test assertions needed to preserve the boundary.

## Inputs

Allowed inputs:

- Current repo docs and contracts named by this contract.
- Existing corpus parity manifest and session ledger.
- Existing GRE timer normalization code and focused tests.
- Current report output from the corpus parity CLI.
- Local synthetic values written in tests or metadata under this contract.
- Public Manasight metadata only through category-level taxonomy context
  already represented by prior corpus parity artifacts.

Forbidden inputs:

- Manasight raw logs, compressed corpus files, raw session payloads, hash lists,
  byte-size lists, capture-date row lists, parser source, timer examples, or
  external corpus contents.
- Private Player.log excerpts, private local logs, private smoke outputs,
  generated data, SQLite files, runtime artifacts, workbook exports,
  credentials, tokens, API keys, webhook endpoints, IP/network traces,
  decklists, deck names, card choices, strategy notes, private reports, or
  local MTGA settings dumps.
- Newly generated local reports committed as source artifacts, unless a later
  contract authorizes exact report artifact storage.

## Outputs

Authorized output changes for Codex C:

- One new corpus manifest entry for `timer.pre_match_idle`.
- One new session ledger entry for `timer.pre_match_idle`.
- Focused timer test proving the synthetic no-direct-seat pre-match idle shape.
- Focused corpus parity tests proving:
  - the new manifest entry validates;
  - the new session entry validates;
  - `timer.pre_match_idle` is `covered_synthetic`;
  - `timer.active_player_timer` remains `covered_synthetic`;
  - `timer.inactivity_timeout` remains `blocked_external_boundary`;
  - required non-claims are present in known gaps or review notes.
- Implementation handoff and contract-test report documents.

Expected report summary after implementation, assuming no other branch changes:

```text
partial_coverage_map_ready (45 families, 6 committed, 16 missing)
```

Expected summary count changes:

- `covered_synthetic`: 11 -> 12
- `missing`: 17 -> 16
- `covered_committed`: unchanged
- `covered_report_only`: unchanged
- `partial`: unchanged
- `blocked_external_boundary`: unchanged

## Invariants

- `timer.pre_match_idle` coverage must be `covered_synthetic`.
- `timer.pre_match_idle` coverage basis must be exactly:
  `fixture_metadata_only`, `parser_behavior_verified`.
- The new entry must use `parser_event_families: ["GameState"]`.
- The new entry must not use `diagnostics_only`, `evidence_ledger_only`,
  `count_ratchet_only`, or `external_reference_only`.
- The synthetic timer evidence must have no direct seat IDs.
- The synthetic timer evidence must not infer player ownership from turn-info
  context.
- The synthetic timer evidence must include both seconds and milliseconds
  values.
- The synthetic timer evidence must not be degraded.
- The synthetic timer evidence must not claim actual live Arena behavior.
- `timer.inactivity_timeout` must remain `blocked_external_boundary`.
- `timer.active_player_timer` must remain covered only by
  `active_player_timer_synthetic_v1`.
- The corpus parity report may remain `partial_coverage_map_ready`.
- No parser source, timer normalizer source, GameState payload shape, schema
  snapshot, runtime, diagnostics, golden replay, feature-equity, workbook,
  webhook, Apps Script, analytics, AI, coaching, CI, merge, deploy, release, or
  production behavior change is authorized.

## Error Behavior

Contract ambiguity:

- If Codex C cannot represent this slice using the existing manifest/session
  schema and allowed status/basis vocabulary, it must route back to Codex B.

Synthetic shape mismatch:

- If the focused synthetic timer shape produces degraded output, direct seat
  IDs, unknown time units, or review-required flags without changing source
  code, Codex C must route back to Codex B rather than changing the timer
  normalizer in this issue.

Existing test failure:

- If focused timer or corpus tests fail before Codex C edits metadata, Codex C
  must report the base failure and not patch parser behavior inside this issue.

Privacy or protected-surface warnings:

- If secret/private-marker or protected-surface checks warn on the new docs or
  metadata, Codex C must reword or narrow the metadata. It must not suppress
  checks or add broad allowlists.

Generated artifact temptation:

- If implementation would require committing generated reports, private smoke
  output, or runtime artifacts, stop and route back. Issue #389 authorizes
  synthetic metadata and tests only.

## Side Effects

Codex B side effects:

- Create only this contract.

Codex C authorized side effects:

- Edit corpus manifest JSON.
- Edit session ledger JSON.
- Edit focused corpus parity tests.
- Edit focused GRE timer tests.
- Optionally edit focused GameState tests only if needed to prove the existing
  additive payload boundary without changing behavior.
- Write implementation handoff.
- Write contract-test report.

No runtime side effects, local external writes, GitHub issue closure, PR
creation, tracker completion, generated artifact commits, workbook changes,
webhook changes, Apps Script changes, analytics changes, AI/model-provider
calls, or production behavior changes are authorized.

## Dependency Order

Codex C should proceed in this order:

1. Verify branch state against `origin/codex/parser-parity`.
2. Run the current corpus parity report and capture the three timer rows.
3. Run the focused synthetic timer shape through existing timer normalization.
4. Add a focused no-direct-seat pre-match idle timer test.
5. Add the manifest entry.
6. Add the session ledger entry.
7. Add focused corpus parity assertions.
8. Run validation.
9. Write the implementation handoff and contract-test report.

## Compatibility

This contract preserves:

- corpus manifest schema version `parser_corpus_manifest.v1`;
- session ledger schema version `parser_corpus_session_ledger.v1`;
- scenario family id `timer.pre_match_idle`;
- coverage status vocabulary;
- coverage basis vocabulary;
- timer normalization schema version `parser_gre_timers.v1`;
- GameState raw `timers` preservation;
- additive `normalized_timers` payload behavior;
- existing active-player timer coverage;
- existing inactivity-timeout boundary.

No migration is authorized.

## Tests Required

Focused validation for Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_gre_timers_parser.py docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Recommended broader validation if the environment is ready:

```bash
PYTHONPATH=src python3 -m ruff check src tests
```

Codex C must record any skipped validation and why.

## Acceptance Criteria

- `docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md` exists.
- Codex C updates only the corpus metadata/test/report surfaces authorized by
  this contract, unless it routes back.
- The corpus manifest validates cleanly.
- The session ledger validates cleanly.
- The corpus parity report still returns `partial_coverage_map_ready`.
- `timer.pre_match_idle` reports:
  - `coverage_status: covered_synthetic`
  - `coverage_basis: ["fixture_metadata_only", "parser_behavior_verified"]`
  - one Mythic Edge entry, `pre_match_idle_timer_synthetic_v1`
- `timer.active_player_timer` remains `covered_synthetic`.
- `timer.inactivity_timeout` remains `blocked_external_boundary`.
- The focused timer test proves a no-direct-seat, seconds/milliseconds,
  non-degraded pre-match idle timer shape.
- Tests assert non-claims and adjacent timer boundaries.
- No raw/private/external/generated artifacts are committed.
- No protected parser/runtime/workbook/webhook/App Script/diagnostics/golden
  replay/feature-equity/evidence-ledger/analytics/AI/production behavior
  changes are made.
- The implementation handoff and contract-test report name remaining gaps.

## Open Questions And Suspected Gaps

- The selected synthetic shape proves a bounded parser-normalization path, not
  actual live Arena pre-match idle payload diversity.
- If future private smoke evidence shows different payload fields, that should
  become a new scoped issue and contract.
- `timer.inactivity_timeout` remains blocked by external boundary and should
  not be collapsed into this issue.
- Clock-pressure analytics, rope interpretation, and player-mistake labels
  remain future analytics/coaching concerns, not parser corpus truth.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #389.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/389

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md

Goal:
Implement the smallest metadata/test/report-only change needed to satisfy the
pre-match idle timer corpus coverage contract. Move only
`timer.pre_match_idle` from missing to `covered_synthetic` using synthetic
timer metadata and existing GRE timer normalization behavior. Do not change
parser behavior or timer normalization behavior.

Before editing:
1. Fetch and verify `origin/codex/parser-parity`.
2. Create or use a clean implementation branch from `codex/parser-parity`.
3. Confirm PR #380 merged at
   `8359148957fd9f37399dff6e12a834cf78373e5c` or record the newer base.
4. Inspect `git status --short --branch`.
5. Leave unrelated or untracked local artifacts alone.

Read:
- docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md
- docs/contracts/parser_corpus_active_player_timer_coverage.md
- docs/contracts/parser_timer_normalization.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- src/mythic_edge_parser/parsers/gre/timers.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_parser.py

Do:
- Compare the current corpus parity report against the contract before editing.
- Add a focused synthetic pre-match idle timer normalization test proving no
  direct seat, seconds/milliseconds values, no degradation, and no seat
  grouping.
- Add exactly one manifest entry for `pre_match_idle_timer_synthetic_v1`.
- Add the matching session ledger entry.
- Add focused tests proving `timer.pre_match_idle` is `covered_synthetic` and
  adjacent timer rows remain bounded.
- Produce
  `docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md`.

Do not:
- Change parser behavior.
- Change GRE timer normalization behavior, GameState payload shape, parser
  state final reconciliation, parser event classes, router semantics,
  diagnostics, golden replay, feature-equity, evidence-ledger behavior,
  match/game identity, workbook/webhook or Apps Script behavior, analytics
  truth, AI truth, production behavior, CI gates, merge readiness, deploy
  readiness, or tracker lifecycle behavior.
- Cover `timer.inactivity_timeout` or any other scenario family in issue #389.
- Alter `timer.active_player_timer` beyond adjacent boundary assertions.
- Claim live Arena pre-match idle behavior, private smoke success,
  inactivity-timeout support, rope behavior, clock pressure, gameplay advice,
  player-mistake labels, release readiness, analytics truth, AI truth,
  coaching truth, production behavior, full corpus parity, or parser support
  from corpus metadata alone.
- Import, copy, mirror, or commit external corpus contents or forbidden
  private/generated/local artifacts named by the contract.
- Target main directly.
- Close issue #389 or tracker #158.
- Stage or commit unless explicitly asked.

Validation:
- Run the focused validation commands from the contract.
- Run changed-file secret/private and protected-surface checks.
- Record skipped validation with reasons.

Expected output:
- Updated corpus manifest/session ledger/tests.
- Implementation handoff.
- Contract-test report.
- Validation summary.
- workflow_handoff block to Codex E.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/379"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/380"
  previous_merge_commit: "8359148957fd9f37399dff6e12a834cf78373e5c"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_pre_match_idle_timer_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_pre_match_idle_timer_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_pre_match_idle_timer_coverage.md"
  verdict: "contract_ready_for_synthetic_pre_match_idle_timer_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-pre-match-idle-timer-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/private marker scan"
    - "changed-file protected-surface gate"
    - "changed-file validation selector"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not close issue #389."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from corpus metadata alone."
    - "Do not cover timer.inactivity_timeout or any other scenario family in issue #389."
    - "Do not claim live Arena pre-match idle behavior, private smoke success, inactivity-timeout support, rope behavior, clock pressure, gameplay advice, player-mistake labels, release readiness, analytics truth, AI truth, coaching truth, production behavior, or tracker completion."
    - "Do not import, copy, mirror, or commit external corpus contents or forbidden private/generated/local artifacts named by the contract."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
