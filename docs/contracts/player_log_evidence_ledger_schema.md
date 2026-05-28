# Player.log Evidence Ledger Schema Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- parent_issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- completed_support_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- branch_target: codex/parser-reliability-intelligence
- latest_verified_remote_commit: 066b55f441902913432250c05b1c920a79b3ae83
- target_artifact: docs/contracts/player_log_evidence_ledger_schema.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/problem_representations/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md

## Purpose

Issue #128 is the first implementation-sized slice of the broader
Player.log evidence ledger from issue #11.

The broad #11 contract defines the long-range evidence-ledger map: Tier 0
metadata, Tier 1-3 business-critical parser outputs, future Tier 4-7 coverage,
schema snapshots, drift reports, invariant checks, and degradation behavior.
That contract remains authoritative for the long-term goal.

This contract narrows the first buildable step to a machine-readable schema and
seed provenance registry. The first implementation should create stable
structures, vocabulary enforcement, deterministic serialization, and one
complete Tier 1 sample entry. It should not attempt to map every parser-owned
field yet.

Plain English: build the spine before the whole skeleton. The ledger should be
able to say, in a structured and testable way, "this parser-owned output is
supported by these evidence signals, with these allowed labels and review
rules." It must not become another parser, a workbook workaround, a runtime
status migration, or an AI truth layer.

## Reconciliation With The Broad #11 Contract

`docs/contracts/player_log_evidence_ledger.md` is intentionally broad. It names
future implementation modules:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/schema_snapshot.py`
- `src/mythic_edge_parser/app/drift_report.py`
- `src/mythic_edge_parser/app/invariants.py`

Issue #128 implements only the first of those surfaces:

- `src/mythic_edge_parser/app/evidence_ledger.py`

This contract does not supersede the broad #11 contract. It decomposes it.

If this contract and the broad #11 contract differ on scope, this contract
wins for issue #128 implementation scope only. The broader contract still owns
future schema snapshots, drift reports, invariants, and full Tier 1-7 coverage.

If this contract and ADR-0003 differ on value-source labels, confidence
labels, drift flags, invariant-status labels, or privacy posture, ADR-0003
wins unless a future ADR supersedes it.

Finality vocabulary has one intentional issue #128 clarification: this contract
preserves every ADR-0003 finality label and adds `final` as a schema-level
label. `final` is not a replacement for `reconciled`; it is the state after
final result evidence exists and before any later stronger evidence corrects
the value. `reconciled` remains the label for a final value updated by later
stronger evidence.

## Codex C Scope Decision

Codex C should implement:

- schema and vocabulary enforcement
- a small code-owned seed registry
- one complete Tier 1 field sample for `match_id` / `MTGA Match ID`

Codex C should not implement:

- schema snapshots
- drift reports
- invariant execution
- field evidence attachment to runtime rows
- workbook or webhook exposure
- full Tier 1-3 field mapping
- future Tier 4-7 implementation

Reasoning:

- Schema and vocabulary only would be too abstract to validate against real
  Mythic Edge parser-owned output surfaces.
- Full Tier 1-3 coverage would be too large and would risk hidden behavior
  decisions inside a schema bootstrap issue.
- One full Tier 1 sample proves the schema can express a real parser-owned
  output while keeping source-path disputes and degradation decisions small.

## Finality Vocabulary Clarification

Codex E identified an apparent vocabulary conflict between ADR-0003 and this
contract. The intended resolution is:

- ADR-0003 requires `live`, `provisional`, and `reconciled`.
- The broad #11 evidence-ledger contract also uses `final`.
- Issue #128 intentionally includes `final` in `FINALITY_LABELS`.
- `FINALITY_LABELS` must therefore be exactly:
  `("live", "provisional", "final", "reconciled")`.

Definitions:

- `live`: still updating during active parsing.
- `provisional`: likely or available but not reconciled against final result
  evidence.
- `final`: emitted after final result evidence exists and no later stronger
  correction has been applied.
- `reconciled`: a final value updated by later stronger evidence.

This is a scoped schema clarification for issue #128, not a parser behavior
change and not a runtime final-reconciliation change. It does not amend
ADR-0003 by itself. A future ADR cleanup may align ADR-0003 wording with the
broad #11 contract, but Codex C should implement `final` for issue #128.

## Owning Layer

Primary owning layer: parser resilience and parser provenance metadata.

Truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- Parser modules, `router.py`, `events.py`, `app/state.py`, and
  `app/models.py` remain the source of parser-owned interpretation and
  normalized facts.
- The evidence ledger describes support and provenance for parser-owned facts.
  It does not compute match facts, game facts, identity, winners, play/draw,
  mulligans, rank, cards, or final reconciliation.
- Diagnostics, golden replay, feature-equity corpus reports, runtime status,
  workbook formulas, Apps Script, webhook transport, dashboards, and AI output
  are consumers or reporting surfaces. They must not become parser truth.

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`066b55f441902913432250c05b1c920a79b3ae83`:

- Issue #47 is closed as completed.
- Issue #11 remains open as the evidence/provenance/drift owner.
- `docs/contracts/player_log_evidence_ledger.md` defines the broad ledger
  design and vocabulary.
- `docs/decisions/ADR-0003-player-log-drift-policy.md` accepts the Player.log
  drift vocabulary and privacy posture.
- `src/mythic_edge_parser/app/log_drift_sensor.py` reports routed and unknown
  Player.log entry families, unmatched API names, and baseline deltas. Its
  report is routing-drift oriented, not field-provenance oriented.
- `src/mythic_edge_parser/app/parser_diagnostics.py` produces local parser
  diagnostics reports using parser/router/drift evidence.
- `src/mythic_edge_parser/app/golden_replay.py` replays committed sanitized or
  synthetic fixtures through the normal parser path.
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` produces
  count-shaped corpus coverage reports from golden replay manifests.
- `src/mythic_edge_parser/app/models.py` and `app/state.py` own current match,
  game, rank, queue, play/draw, mulligan, opening-hand, and row construction
  behavior.
- No `src/mythic_edge_parser/app/evidence_ledger.py` module exists.
- No focused `tests/test_evidence_ledger.py` exists.
- No machine-readable registry currently maps parser-owned output fields to
  evidence signals, source labels, confidence labels, finality labels, drift
  flags, invariant names, or recommended review modules.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_schema.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_schema.md

Referenced but not silently owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/parsers/match_state.py
- tests/test_log_drift_sensor.py
- tests/test_parser_diagnostics_mode.py
- tests/test_golden_replay_harness.py
- tests/test_feature_equity_corpus_ratchet.py

Out of scope for issue #128:

- src/mythic_edge_parser/app/schema_snapshot.py
- src/mythic_edge_parser/app/drift_report.py
- src/mythic_edge_parser/app/invariants.py
- workbook schema files
- webhook payload builders
- Apps Script files
- parser state final reconciliation behavior
- parser event classes

## Public Interface

Recommended module:

```python
src/mythic_edge_parser/app/evidence_ledger.py
```

Required constants:

```python
LEDGER_OBJECT = "mythic_edge_player_log_evidence_ledger"
LEDGER_SCHEMA_VERSION = "player_log_evidence_ledger_schema.v1"
LEDGER_VERSION = "player_log_evidence_ledger.v1"
```

Required vocabulary constants:

```python
VALUE_SOURCES = (
    "observed",
    "derived",
    "inferred",
    "unknown",
    "conflict",
    "legacy_enriched",
)

CONFIDENCE_LEVELS = (
    "high",
    "medium",
    "low",
    "unknown",
)

FINALITY_LABELS = (
    "live",
    "provisional",
    "final",
    "reconciled",
)

INVARIANT_STATUSES = (
    "passed",
    "failed",
    "not_applicable",
    "not_checked",
    "degraded",
)
```

Required drift flags:

```python
DRIFT_FLAGS = (
    "missing_expected_event_family",
    "missing_expected_payload_path",
    "changed_signal_type",
    "new_unknown_event_family",
    "new_unknown_payload_path",
    "fallback_used",
    "weak_fallback_used",
    "conflicting_evidence",
    "invariant_failed",
    "schema_snapshot_missing",
    "fixture_gap",
    "parser_exception",
    "transport_failure",
    "workbook_drift",
    "deployment_drift",
    "sensitive_evidence_redacted",
)
```

Required public functions:

```python
from collections.abc import Mapping
from typing import Any


def build_player_log_evidence_ledger() -> dict[str, Any]:
    ...


def iter_ledger_entries() -> tuple[dict[str, Any], ...]:
    ...


def validate_player_log_evidence_ledger(
    payload: Mapping[str, Any] | None = None,
) -> list[str]:
    ...


def validate_ledger_entry(entry: Mapping[str, Any]) -> list[str]:
    ...
```

Allowed implementation form:

- Python constants plus pure functions
- frozen dataclasses with JSON export
- typed dictionaries with builder/validator helpers

Required behavior regardless of implementation form:

- Public builders return JSON-serializable dictionaries.
- Builders must be deterministic and must not include volatile timestamps.
- Validators return stable string error codes or error messages.
- Validators must not raise for malformed caller-provided payloads.
- Importing the module must have no filesystem, network, environment, GitHub,
  workbook, webhook, Apps Script, runtime-status, or local-log side effects.

No CLI entrypoint is required for issue #128.

## Ledger Object Schema

`build_player_log_evidence_ledger()` must return this logical shape:

```yaml
object: "mythic_edge_player_log_evidence_ledger"
schema_version: "player_log_evidence_ledger_schema.v1"
ledger_version: "player_log_evidence_ledger.v1"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
related_adrs:
  - "docs/decisions/ADR-0003-player-log-drift-policy.md"
branch_target: "codex/parser-reliability-intelligence"
privacy:
  raw_private_logs_included: false
  raw_payload_values_included: false
  source_paths_are_repo_relative_or_symbolic: true
vocabulary:
  value_sources: []
  confidence_levels: []
  finality_labels: []
  drift_flags: []
  invariant_statuses: []
output_families:
  - output_family_registration
entries:
  - ledger_entry
```

Required top-level fields:

- `object`
- `schema_version`
- `ledger_version`
- `source_issue`
- `parent_issue`
- `related_adrs`
- `branch_target`
- `privacy`
- `vocabulary`
- `output_families`
- `entries`

`generated_at`, absolute local file paths, local usernames, raw account names,
raw payload values, and raw Player.log lines are not allowed in the ledger
definition.

## Output Family Registration Schema

Output family registrations are lightweight registry rows. They make future
coverage visible without pretending every field is mapped in issue #128.

Required logical shape:

```yaml
output_family_registration:
  tier: 1
  output_family: "match_identity_and_lifecycle"
  status: "seeded_sample"
  description: "Match identity and lifecycle outputs owned by parser state."
  seed_fields:
    - "match_id"
  future_fields:
    - "match_started_at"
    - "match_finished_at"
  owner_modules:
    - "src/mythic_edge_parser/app/state.py"
  notes:
    - "Only match_id is fully mapped in issue #128."
```

Required family status values:

- `seeded_sample`: at least one complete ledger entry exists in this issue.
- `registered_future`: the family is acknowledged but not fully mapped.

Required issue #128 registrations:

| Tier | Output family | Required status |
| --- | --- | --- |
| 1 | `match_identity_and_lifecycle` | `seeded_sample` |
| 2 | `queue_format_rank_event_context` | `registered_future` |
| 3 | `game_level_facts` | `registered_future` |
| 4 | `sideboarding_and_deck_state` | `registered_future` |
| 5 | `card_identity_and_gameplay_actions` | `registered_future` |
| 6 | `runtime_health_and_drift_detection` | `registered_future` |
| 7 | `derived_analytics_outputs` | `registered_future` |

Only `match_identity_and_lifecycle.match_id` should be fully mapped by Codex C.

## Ledger Entry Schema

Required logical shape:

```yaml
ledger_entry:
  entry_id: "tier1.match_identity.match_id"
  tier: 1
  output_family: "match_identity_and_lifecycle"
  output_field: "match_id"
  display_name: "MTGA Match ID"
  parser_owner: "src/mythic_edge_parser/app/state.py"
  model_surface: "MatchSummary.to_match_log_row"
  downstream_surfaces:
    - "MatchLogRow"
  parser_managed_truth: true
  coverage_status: "seeded_sample"
  direct_evidence:
    - evidence_signal
  fallback_evidence:
    - evidence_signal
  value_source_policy:
    direct: "observed"
    fallback: "derived"
    missing: "unknown"
    contradiction: "conflict"
    historical: "legacy_enriched"
  confidence_policy:
    direct: "high"
    fallback: "medium"
    weak_fallback: "low"
    missing: "unknown"
    contradiction: "low"
  finality_policy:
    live: "live"
    provisional: "provisional"
    final: "final"
    corrected_by_later_evidence: "reconciled"
  invariant_checks:
    - "stable_match_id_required"
  degradation_behavior:
    - "block final match-level row identity when match_id is missing"
  drift_flags:
    - "missing_expected_payload_path"
  recommended_review_modules:
    - "src/mythic_edge_parser/app/state.py"
  tests:
    - "tests/test_evidence_ledger.py"
  fixture_refs:
    - "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json"
  notes:
    - "Seed entry only; broader Tier 1 coverage belongs to later issues."
```

Required entry fields:

- `entry_id`
- `tier`
- `output_family`
- `output_field`
- `display_name`
- `parser_owner`
- `model_surface`
- `downstream_surfaces`
- `parser_managed_truth`
- `coverage_status`
- `direct_evidence`
- `fallback_evidence`
- `value_source_policy`
- `confidence_policy`
- `finality_policy`
- `invariant_checks`
- `degradation_behavior`
- `drift_flags`
- `recommended_review_modules`
- `tests`
- `fixture_refs`
- `notes`

Required field rules:

- `entry_id` must be stable, lower-case, dot-separated, and unique.
- `tier` must be an integer from 0 through 7.
- `parser_managed_truth` must be `true` for parser-owned output entries.
- `coverage_status` must be either `seeded_sample` or `registered_future`.
- `direct_evidence` and `fallback_evidence` must be lists.
- Every value-source label in policies must belong to `VALUE_SOURCES`.
- Every confidence label in policies must belong to `CONFIDENCE_LEVELS`.
- Every finality label in policies must belong to `FINALITY_LABELS`.
- Every drift flag must belong to `DRIFT_FLAGS`.
- Path-like fields must be repository-relative paths or symbolic surfaces, not
  absolute local paths.

## Evidence Signal Schema

Required logical shape:

```yaml
evidence_signal:
  signal_id: "match_state.match_id"
  parser_event_kind: "MatchState"
  parser_event_type: "match_started"
  raw_event_family: "matchGameRoomStateChangedEvent"
  raw_message_type: ""
  normalized_payload_path: "payload.match_id"
  raw_payload_path: "matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.matchId"
  required_for_final: true
  value_source_when_used: "observed"
  confidence_when_used: "high"
  finality_when_used: "live"
  allowed_types:
    - "str"
  missing_behavior: "mark match_id unknown and block final match-level rows"
  privacy_class: "path_only_no_values"
```

Required evidence fields:

- `signal_id`
- `parser_event_kind`
- `parser_event_type`
- `raw_event_family`
- `raw_message_type`
- `normalized_payload_path`
- `raw_payload_path`
- `required_for_final`
- `value_source_when_used`
- `confidence_when_used`
- `finality_when_used`
- `allowed_types`
- `missing_behavior`
- `privacy_class`

Required field rules:

- `signal_id` must be stable, lower-case, dot-separated, and unique within a
  ledger entry.
- `parser_event_kind` should name an existing parser event kind or the symbolic
  value `parser_context`.
- `raw_event_family` should name the raw Player.log event family or the
  symbolic value `parser_context`.
- `raw_message_type` may be `""` when the signal has no GRE message type.
- `normalized_payload_path` and `raw_payload_path` must be path strings, not
  raw payload values.
- `value_source_when_used`, `confidence_when_used`, and
  `finality_when_used` must use the approved vocabularies.
- `allowed_types` must use symbolic type labels such as `str`, `int`,
  `bool`, `dict`, `list`, `str-int`, or `unknown`.
- `privacy_class` for issue #128 must be `path_only_no_values`.

## Seed Registry Requirement

Codex C must seed exactly one complete ledger entry:

```yaml
entry_id: "tier1.match_identity.match_id"
tier: 1
output_family: "match_identity_and_lifecycle"
output_field: "match_id"
display_name: "MTGA Match ID"
```

Required seed entry ownership:

- parser_owner: `src/mythic_edge_parser/app/state.py`
- model_surface: `MatchSummary.to_match_log_row`
- downstream_surfaces must include:
  - `MatchLogRow`
  - `GameLogRow`
  - `match_history`
- recommended_review_modules must include:
  - `src/mythic_edge_parser/app/state.py`
  - `src/mythic_edge_parser/parsers/match_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_result.py`

Required direct evidence signals:

1. `match_state.match_id`
   - parser_event_kind: `MatchState`
   - normalized_payload_path: `payload.match_id`
   - raw_event_family: `matchGameRoomStateChangedEvent`
   - raw_payload_path:
     `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.matchId`
   - value_source_when_used: `observed`
   - confidence_when_used: `high`

2. `game_state.identity.match_id`
   - parser_event_kind: `GameState`
   - normalized_payload_path: `payload.identity.match_id`
   - raw_event_family: `greToClientEvent`
   - raw_message_type: `GREMessageType_GameStateMessage`
   - raw_payload_path:
     `greToClientMessages[].gameStateMessage.gameInfo.matchID`
   - value_source_when_used: `observed`
   - confidence_when_used: `high`

3. `game_result.identity.match_id`
   - parser_event_kind: `GameResult`
   - normalized_payload_path: `payload.identity.match_id`
   - raw_event_family: `greToClientEvent`
   - raw_message_type: `GREMessageType_GameStateMessage`
   - raw_payload_path:
     `greToClientMessages[].gameStateMessage.gameInfo.matchID`
   - value_source_when_used: `observed`
   - confidence_when_used: `high`

Required fallback evidence signal:

1. `parser_context.current_match_id`
   - parser_event_kind: `parser_context`
   - raw_event_family: `parser_context`
   - normalized_payload_path: `state_context.current_match_id`
   - raw_payload_path: ``
   - value_source_when_used: `derived`
   - confidence_when_used: `medium`
   - missing_behavior:
     `mark match_id unknown and block final match-level rows`

Required seed invariants:

- `stable_match_id_required`
- `final_match_row_requires_match_id`
- `game_rows_must_not_attach_to_unknown_match_id`

Required seed degradation behavior:

- Missing direct and fallback match identity yields `value_source=unknown`.
- Missing match identity yields `confidence=unknown`.
- Missing match identity must mark review required in future field-evidence
  results.
- Missing match identity must block final match-level row identity. This
  describes expected provenance behavior only; issue #128 must not change
  current parser state behavior.

## Field Evidence Result Schema

Issue #128 should define this schema and may provide helper validation for it,
but it should not attach these records to runtime rows yet.

Required logical shape:

```yaml
field_evidence:
  object: "mythic_edge_player_log_field_evidence"
  schema_version: "player_log_field_evidence.v1"
  ledger_version: "player_log_evidence_ledger.v1"
  entry_id: "tier1.match_identity.match_id"
  output_family: "match_identity_and_lifecycle"
  output_field: "match_id"
  value_source: "observed"
  confidence: "high"
  finality: "live"
  source_event_kind: "MatchState"
  source_event_type: "match_started"
  source_payload_paths:
    - "payload.match_id"
  source_event_timestamp: ""
  drift_flags: []
  invariant_status: "not_checked"
  degraded_reason: ""
  review_required: false
```

Required behavior:

- The field evidence schema is a provenance metadata shape, not a workbook row.
- `review_required` must be true when:
  - `invariant_status == "failed"`
  - `value_source == "conflict"`
  - `confidence == "low"` and `finality in ("final", "reconciled")`
- `source_event_timestamp` may be empty for static examples.
- Future runtime use must redact or omit raw private log paths and values.

## Vocabulary Enforcement

Validators must reject or report:

- unknown top-level object values
- unknown schema versions
- missing required ledger fields
- missing required entry fields
- missing required evidence signal fields
- duplicate `entry_id` values
- duplicate `signal_id` values within one entry
- unknown `value_source` labels
- unknown `confidence` labels
- unknown `finality` labels
- unknown `drift_flags`
- unknown `invariant_status` values in field-evidence records
- absolute local paths in path-like fields
- raw Player.log-like line samples in registry fields

Validators may return human-readable strings, but focused tests should assert
stable substrings or stable error codes so wording can evolve.

Approved value-source precedence when multiple labels could apply:

1. `conflict`
2. `unknown`
3. `legacy_enriched`
4. `inferred`
5. `derived`
6. `observed`

This precedence is carried forward from the broad #11 contract.

## Serialization And Privacy Rules

The ledger registry must be deterministic:

- no generated timestamp
- no local absolute paths
- no local usernames
- no current machine hostname
- no raw Player.log lines
- no raw JSON payload examples from private logs
- no account names, display names, user IDs, auth tokens, webhook URLs, or
  credentials

If Codex C adds JSON serialization helpers, they must produce stable,
JSON-serializable data. Recommended JSON formatting:

```python
json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
```

Committed examples must use symbolic paths or repo-relative fixture paths only.

Private local logs may inform future local drift reports, but issue #128 must
not read, copy, summarize, or commit private `Player.log` excerpts.

## Relationship To Existing Tools

### `log_drift_sensor.py`

The existing drift sensor is a routing-drift helper. It may later consume the
ledger to map unknown or missing signals to affected outputs, but issue #128
must not change its report shape or behavior.

### `parser_diagnostics.py`

Diagnostics may later display ledger-backed field provenance or degraded
outputs. Issue #128 must not change diagnostics report shape or runtime status
files.

### `golden_replay.py`

Golden replay may later assert field-evidence records for selected fixtures.
Issue #128 must not change golden replay manifest shape or expected outputs.

### `feature_equity_corpus_ratchet.py`

The corpus ratchet may later count ledger coverage. Issue #128 must not change
ratchet baseline behavior, report status behavior, or fixture counts.

## Error Behavior

Required builder behavior:

- `build_player_log_evidence_ledger()` must produce a valid ledger without
  reading files, environment variables, Git state, logs, runtime status, or
  external services.
- `iter_ledger_entries()` must return immutable or copy-safe entry data so
  callers cannot mutate shared global state accidentally.

Required validator behavior:

- Passing no payload validates the built-in ledger.
- Passing malformed payloads returns validation errors instead of raising.
- Empty payloads must report missing required fields.
- Unknown vocabulary values must report errors.
- Duplicate IDs must report errors.

Contract ambiguity:

- If Codex C finds that the `match_id` seed entry requires parser behavior
  changes, it must stop and route back to Codex B.
- If Codex C finds that source paths in the seed entry are inaccurate, it may
  make a narrower path correction in implementation only if the handoff
  explains the evidence. If source ownership is unclear, route back to Codex B.

## Side Effects

Allowed in Codex C:

- add `src/mythic_edge_parser/app/evidence_ledger.py`
- add `tests/test_evidence_ledger.py`
- write `docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md`
- write `docs/contract_test_reports/player_log_evidence_ledger_schema.md` if
  acting in a review/reporting loop later

Forbidden in Codex C unless a later contract explicitly authorizes it:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- match identity or game identity behavior changes
- deduplication changes
- workbook schema changes
- webhook payload shape changes
- Apps Script changes
- runtime status file schema changes
- failed-post changes
- workbook export changes
- generated data changes
- secrets, credentials, tokens, API keys, webhook URLs, or environment
  variable contract changes
- reading or committing raw private Player.log excerpts
- live workbook, webhook, or Apps Script calls
- OpenAI/model-provider calls
- automatic GitHub issue creation from validation output

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch target is `codex/parser-reliability-intelligence` and inspect
   `git status --short --branch`.
2. Read issue #128, issue #11, ADR-0003, the broad #11 contract, and this
   contract.
3. Compare current branch state to this contract and confirm
   `evidence_ledger.py` is absent.
4. Add focused tests for vocabulary constants, ledger object shape, seed entry
   shape, validation behavior, JSON serializability, determinism, and privacy
   rules.
5. Add `src/mythic_edge_parser/app/evidence_ledger.py`.
6. Run focused validation.
7. Produce
   `docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md`.
8. Route to Codex E for review.

Do not edit diagnostics, golden replay, feature-equity corpus ratchet, state,
models, sheet schema, router, parser modules, workbook, webhook, or Apps Script
in issue #128.

## Tests Required

Focused tests in `tests/test_evidence_ledger.py` must cover:

- vocabulary constants exactly match this contract, preserve ADR-0003 labels,
  and intentionally include `final` in `FINALITY_LABELS`
- `build_player_log_evidence_ledger()` returns required top-level fields
- top-level `object`, `schema_version`, and `ledger_version` values are stable
- the registry includes the seven required output family registrations
- only `match_identity_and_lifecycle` has `seeded_sample` status in issue #128
- exactly one complete ledger entry exists:
  `tier1.match_identity.match_id`
- the seed entry includes the required direct evidence signals
- the seed entry includes the required parser context fallback signal
- every entry and evidence signal validates cleanly
- validator reports errors for missing required fields
- validator reports errors for unknown value-source labels
- validator reports errors for unknown confidence labels
- validator reports errors for unknown finality labels
- validator reports errors for unknown drift flags
- validator reports duplicate `entry_id` and duplicate per-entry `signal_id`
  values
- validator reports absolute local paths in path-like fields
- built ledger is JSON-serializable
- repeated builder calls are deterministic
- module import has no filesystem writes or external calls
- ledger data does not contain raw private-log examples, webhook URLs, tokens,
  local usernames, failed-post paths, runtime status paths, or workbook export
  paths

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m ruff check src tests tools
git diff --check
```

If changed-path protected-surface tooling is available on the branch, Codex C
should run the relevant protected-surface check and report forbidden/warning
counts.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_schema.md` exists.
- The contract reconciles issue #128 with issue #11, the broad #11 contract,
  completed #47 support, and ADR-0003.
- The contract defines machine-readable ledger object, output family,
  ledger-entry, evidence-signal, and field-evidence schemas.
- The contract defines vocabulary enforcement and privacy rules.
- The contract chooses the smallest safe seed registry scope:
  schema plus vocabulary plus one complete Tier 1 `match_id` sample.
- The contract lists focused tests and validation commands for Codex C.
- No code or behavior changes are made in Codex B.

## Open Questions And Contract Risks

- The seed `match_id` raw payload paths may need small corrections during
  implementation if focused inspection finds a more accurate path. Codex C may
  correct path strings only when the handoff documents the evidence and no
  behavior changes are needed.
- The broad #11 contract still requires full Tier 1-3 mapping. This issue only
  proves the schema and first sample.
- Future field-evidence runtime attachment may require a separate contract
  because it could touch diagnostics, runtime JSON, or downstream surfaces.
- Future schema snapshots, drift reports, and invariant execution remain
  separate modules and should not be smuggled into this issue.

## Contract Clarification Loopback

This contract has been clarified after Codex E found the finality-vocabulary
authority conflict. The clarified contract intentionally keeps `final` in the
issue #128 vocabulary.

If the implementation already uses
`("live", "provisional", "final", "reconciled")`, no Codex D code fix is
expected solely for this finding. The next workflow step after this
clarification is a narrow Codex E re-review of the contract clarification
against the existing implementation and tests.

## Recommended Next Role

Current loopback route: Codex E: Module Reviewer / Contract Tester.

Codex E should re-review the finality-vocabulary clarification against the
existing implementation and tests. If the implementation still matches the
clarified contract and no new blocker appears, the package can route to Codex F
for submission.

For a fresh branch without implementation, the normal route remains Codex C:
Module Implementer.

Codex C should implement only the schema/vocabulary/seed-registry module and
focused tests described here, then route to Codex E for contract review.

## Pasteable Prompt For Codex E Loopback

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #128 after Codex B contract clarification.

Context:
- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- Branch/base: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-schema
- Contract: docs/contracts/player_log_evidence_ledger_schema.md
- Prior review report: docs/contract_test_reports/player_log_evidence_ledger_schema.md
- Implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md

Goal:
Re-review only the Codex B finality-vocabulary clarification and confirm whether the existing implementation and tests now satisfy the clarified contract. The clarified contract intentionally includes `final` in `FINALITY_LABELS` as a schema-level label while preserving ADR-0003 labels.

Do not implement code.
Do not target main directly.
Do not close issue #11.
Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.

Expected output:
- Findings first.
- Verdict on whether the finality-vocabulary blocker is resolved.
- Validation inspected or run.
- Next recommended role: Codex F if clean, otherwise Codex D or Codex B with a concrete blocker.
- workflow_handoff block.
```

## Pasteable Prompt For Codex C

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #128: Player.log evidence ledger schema.

Context:
- Parent evidence/provenance issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Completed support tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- Branch/base: codex/parser-reliability-intelligence
- Latest verified remote commit: 066b55f441902913432250c05b1c920a79b3ae83
- Contract: docs/contracts/player_log_evidence_ledger_schema.md

Goal:
Implement the smallest coherent schema/provenance-registry slice required by the contract. Add a parser-local evidence ledger module with stable vocabulary constants, deterministic ledger builders, validators, seven output-family registrations, and one complete Tier 1 `match_id` seed entry. Add focused tests and produce the implementation handoff.

Read first:
1. AGENTS.md
2. docs/agent_rules.yml
3. docs/agent_constitution.md
4. docs/codex_module_workflow.md
5. docs/agent_threads/implementation.md
6. docs/contracts/player_log_evidence_ledger_schema.md
7. docs/contracts/player_log_evidence_ledger.md
8. docs/decisions/ADR-0003-player-log-drift-policy.md
9. src/mythic_edge_parser/app/models.py
10. src/mythic_edge_parser/app/state.py
11. src/mythic_edge_parser/parsers/match_state.py
12. src/mythic_edge_parser/app/log_drift_sensor.py
13. src/mythic_edge_parser/app/parser_diagnostics.py
14. src/mythic_edge_parser/app/golden_replay.py
15. src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py

Implement:
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md

Do not:
- Do not target main directly.
- Do not close issue #11.
- Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
- Do not change diagnostics, golden replay, feature-equity corpus ratchet, state, models, sheet schema, router, parser modules, workbook, webhook, or Apps Script behavior.
- Do not implement schema snapshots, drift reports, invariant execution, runtime row field-evidence attachment, or automatic GitHub issue creation.
- Do not read, copy, summarize, or commit raw private Player.log excerpts or local diagnostics artifacts.
- Do not stage or commit unless explicitly asked.

Required validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m ruff check src tests tools
- git diff --check
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_schema.md"
  target_artifact: "docs/contract_test_reports/player_log_evidence_ledger_schema.md"
  verdict: "contract_clarified_return_to_reviewer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema"
  validation:
    - "git diff --check"
    - "git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not change diagnostics, golden replay, feature-equity corpus ratchet, state, models, sheet schema, router, parser modules, workbook, webhook, or Apps Script behavior."
    - "Do not implement schema snapshots, drift reports, invariant execution, runtime row field-evidence attachment, or automatic GitHub issue creation."
    - "Do not read, copy, summarize, or commit raw private Player.log excerpts or local diagnostics artifacts."
```
