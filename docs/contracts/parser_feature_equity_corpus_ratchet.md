# Parser Feature-Equity Corpus Ratchet Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/119
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_context:
  - https://github.com/Tahjali11/Mythic-Edge/issues/11
  - docs/problem_representations/parser_feature_equity_with_manasight.md
  - docs/contracts/parser_golden_replay_harness.md
  - docs/contracts/parser_diagnostics_mode.md
  - docs/contracts/parser_saved_event_replay.md
  - docs/contracts/parser_gsm_truncation.md
  - docs/contracts/parser_game_state_diff_mechanics.md
  - docs/contracts/parser_annotation_normalization.md
  - docs/contracts/parser_timer_normalization.md
  - docs/contracts/parser_opponent_card_observations.md
- current_integration_branch: codex/parser-reliability-intelligence
- target_artifact: docs/contracts/parser_feature_equity_corpus_ratchet.md
- module_status: contract only
- risk_tier: Medium
- protected_surface_posture: report-only, no parser behavior changes, no CI gate, no baseline auto-bless

## Purpose

Mythic Edge now has several parser reliability modules that produce fixture-level
evidence: golden replay, diagnostics, GSM truncation detection, opponent
observation parsing, annotation normalization, timer normalization, and GameState
diff mechanics. Those modules answer local questions, but there is no durable
corpus-level report that answers whether the parser reliability corpus still
exercises the feature families the project expects.

The parser feature-equity corpus ratchet is a report-only utility. It summarizes
explicit sanitized or synthetic corpus inputs, counts parser-observed feature
families, compares those count-shaped observations to a manually reviewed
baseline, and highlights drift for human review.

The ratchet must not become parser truth. It observes parser outputs and
diagnostic summaries that the parser already owns. It must not reinterpret raw
Player.log lines, reconstruct missing evidence, infer hidden game facts, decide
semantic correctness, authorize protected-surface changes, or decide merge
readiness.

## Source Artifacts Inspected

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_saved_event_replay.md
- docs/contracts/parser_gsm_truncation.md
- docs/contracts/parser_opponent_card_observations.md
- docs/contracts/parser_annotation_normalization.md
- docs/contracts/parser_timer_normalization.md
- docs/contracts/parser_game_state_diff_mechanics.md
- docs/contracts/parser_event_schema_snapshots.md
- docs/contracts/player_log_evidence_ledger.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/log/entry.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/saved_event_replay.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/annotations.py
- src/mythic_edge_parser/parsers/gre/timers.py
- src/mythic_edge_parser/parsers/gre/game_state_diff.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_golden_replay_harness.py
- tests/test_parser_diagnostics_mode.py
- tests/test_saved_event_replay.py
- tests/test_event_schema_snapshots.py
- tests/test_gsm_truncation_parser.py
- tests/test_gre_game_state_parser.py
- tests/test_gre_annotations_parser.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_diff_parser.py
- tests/test_opponent_card_observations.py
- tests/fixtures/golden_replay/*.manifest.json
- tests/fixtures/parser_regression_*_slice.log

## Observed Current Behavior

### Existing Golden Replay Behavior

- `src/mythic_edge_parser/app/golden_replay.py` defines an explicit committed
  manifest format:
  - `object`: `mythic_edge_golden_replay_manifest`
  - `schema_version`: `parser_golden_replay_manifest.v1`
- Golden replay currently builds fixture-level reports:
  - `object`: `mythic_edge_golden_replay_report`
  - `schema_version`: `parser_golden_replay_report.v1`
- Golden replay requires explicit manifest inputs.
- Golden replay rejects unsafe absolute fixture paths, private raw fixture
  declarations, and forbidden content patterns.
- Golden replay already counts:
  - manifest count
  - source file count
  - routed entries
  - unknown entries
  - timestamp missing entries
  - timestamp parse failures
  - event family counts
  - truncation and data-loss indicators
- Golden replay validates fixture-local expected sections:
  - `router_stats`
  - `event_family_counts`
  - `event_kind_sequence`
  - `diagnostics_summary`
  - `truncation_and_data_loss`
  - `unknowns_and_degradation`
  - `parser_state`
  - `final_reconciliation`
  - `parser_owned_rows`
- Golden replay status values are fixture-oriented:
  - `pass`
  - `degraded`
  - `review`
  - `diff`
  - `fail`
- Current committed golden replay manifests cover two sanitized fixtures:
  - a basic BO1 match win slice
  - a BO3 sideboard match loss slice
- Current committed golden replay manifests declare event-family coverage for:
  - `Rank`
  - `MatchState`
  - `ClientAction`
  - `GameState`
  - `GameResult`

### Existing Diagnostics Behavior

- `src/mythic_edge_parser/app/parser_diagnostics.py` produces diagnostics
  reports:
  - `object`: `mythic_edge_parser_diagnostics_report`
  - `schema_version`: `parser_diagnostics.v1`
- Diagnostics supports profile labels such as:
  - `fixture`
  - `local_log`
  - `live_game`
- Diagnostics already uses report-oriented status values:
  - `pass`
  - `review`
  - `fail`
  - `unknown`
- Diagnostics separates parser health from transport, workbook, and Apps Script
  health.
- Diagnostics already has vocabulary for:
  - router stats
  - event-family coverage
  - truncation and data loss
  - unknowns and degradation
  - final reconciliation

### Existing Parser Event Surfaces

- Parser events are modeled in `src/mythic_edge_parser/events.py`.
- Current event classes include, among others:
  - `GameState`
  - `ClientAction`
  - `MatchState`
  - `Truncation`
  - `DraftBot`
  - `DraftHuman`
  - `DraftComplete`
  - `EventLifecycle`
  - `Session`
  - `Rank`
  - `Collection`
  - `DeckCollection`
  - `Inventory`
  - `GameResult`
  - `LogFileRotated`
  - `DetailedLoggingStatus`
  - `MatchConnectionState`
  - `TcpConnectionClose`
  - `WebSocketClosed`
  - `ConnectionError`
- The router recognizes truncation markers through `EntryHeader.TRUNCATION_MARKER`.
- Saved-event replay can map stored event records back into current event
  classes, including `Truncation`.

### Existing GRE Feature Behavior

- GRE GameState parsing can attach:
  - raw annotation arrays
  - normalized annotation summaries
  - raw timer arrays
  - normalized timer summaries
  - GameState diff mechanics evidence
- Annotation normalization produces:
  - `object`: `mythic_edge_gre_annotations`
  - `schema_version`: `parser_gre_annotations.v1`
  - total/degraded/review counts
  - annotation type counts
  - marker type counts
  - deletion and replacement evidence
  - zone transfer evidence
  - degradation flags
- Timer normalization produces:
  - `object`: `mythic_edge_gre_timers`
  - `schema_version`: `parser_gre_timers.v1`
  - total/degraded/review counts
  - timer id/type counts
  - direct seat id evidence
  - time unit evidence
  - contextual turn info evidence
  - degradation flags
- GameState diff mechanics produces:
  - `object`: `mythic_edge_gre_game_state_diff_mechanics`
  - `schema_version`: `parser_gre_game_state_diff_mechanics.v1`
  - message/update kind evidence
  - complete vs diff state evidence
  - queued message evidence
  - previous GameState linkage evidence
  - deletion evidence
  - section counts
  - source fields used
  - evidence status
  - value source
  - confidence
  - degradation flags
  - review flags

### Existing Gap

The repo has fixture-level replay assertions and module-level parser tests, but
it does not yet have one durable corpus-level report that says:

- which parser event families the committed reliability corpus exercises
- which parser-owned claim families the corpus exercises
- which unknowns, timestamp anomalies, truncation markers, and data-loss markers
  appear across the corpus
- which selected GameState evidence categories appear across the corpus
- whether those count-shaped observations drifted from a manually reviewed
  baseline

## Required V1 Behavior

### Contract Summary

V1 must implement a deterministic report-only feature-equity corpus ratchet over
explicit committed golden replay manifests.

The implementation must:

- consume explicit manifest inputs only
- reject unsafe/private corpus inputs
- summarize parser-owned observations already produced by existing parser,
  replay, diagnostics, and GRE feature code
- compare observed count-shaped data to a manually reviewed baseline
- emit a stable JSON report
- remain report-only and non-authoritative
- avoid parser behavior changes
- avoid CI gate changes
- avoid automatic baseline update behavior

### Public Interfaces

The approved implementation location is:

- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`

The approved focused test file is:

- `tests/test_feature_equity_corpus_ratchet.py`

The approved baseline fixture directory is:

- `tests/fixtures/feature_equity_corpus/`

The approved initial baseline filename is:

- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

The public module constants must be:

```python
FEATURE_EQUITY_CORPUS_REPORT_OBJECT = "mythic_edge_feature_equity_corpus_ratchet_report"
FEATURE_EQUITY_CORPUS_REPORT_SCHEMA_VERSION = "parser_feature_equity_corpus_ratchet_report.v1"
FEATURE_EQUITY_CORPUS_BASELINE_OBJECT = "mythic_edge_feature_equity_corpus_ratchet_baseline"
FEATURE_EQUITY_CORPUS_BASELINE_SCHEMA_VERSION = "parser_feature_equity_corpus_ratchet_baseline.v1"
```

The public Python interface must provide:

```python
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def build_feature_equity_corpus_report(
    manifest_paths: Sequence[Path],
    *,
    baseline_path: Path | None = None,
) -> dict[str, Any]:
    ...


def write_feature_equity_corpus_report(
    manifest_paths: Sequence[Path],
    *,
    baseline_path: Path | None = None,
    report_path: Path | None = None,
) -> dict[str, Any]:
    ...


def main(argv: Sequence[str] | None = None) -> int:
    ...
```

`build_feature_equity_corpus_report()` must return the report object without
writing files.

`write_feature_equity_corpus_report()` must return the same report object and
write JSON only when `report_path` is provided.

`main()` must support the command:

```powershell
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json --out <local-report-path>
```

The CLI may also accept explicit manifest file paths. A directory argument must
expand only to golden replay manifest files matching `*.manifest.json`.

### V1 Input Scope

V1 approved input sources:

- committed golden replay manifest files under `tests/fixtures/golden_replay/`
- future committed sanitized/synthetic golden replay manifest files that satisfy
  the golden replay harness privacy rules

V1 deferred input sources:

- direct raw Player.log file inputs that are not wrapped by a golden replay
  manifest
- local private Player.log paths
- saved-event replay JSONL files
- runtime status files
- failed-post files
- workbook exports
- live workbook state
- deployed Apps Script state

The ratchet may later gain local private-log support, but not in V1. If future
work adds that mode, it must keep all private paths and raw content local-only
and must require a separate contract or contract amendment.

### Input Safety Requirements

The ratchet must rely on the golden replay manifest privacy model and must also
enforce the following at the corpus-report layer:

- Every V1 manifest input must be explicit.
- Directory expansion must be deterministic and sorted by normalized relative
  path.
- Absolute input paths are allowed only for locating a user-provided file on
  disk; the report must store repo-relative paths for committed repo fixtures.
- Any manifest declaring `raw_private_log_committed: true` must make the ratchet
  report status `fail`.
- Any manifest with source privacy outside approved committed fixture classes
  must make the ratchet report status `fail`.
- Forbidden-content findings from golden replay input validation must make the
  ratchet report status `fail`.
- The ratchet must not copy raw log lines into the report.
- The ratchet must not emit secret-like values, webhook URLs, tokens, workbook
  IDs, local usernames from absolute paths, or raw Player.log snippets.
- The ratchet must not write reports into committed fixture directories by
  default.

Approved V1 source privacy classes:

- `sanitized_committable`
- `synthetic_committable`

Approved V1 ratchet privacy label:

- `committed_count_only`

### Baseline Requirements

V1 must support a manually maintained count-only baseline file:

- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

The baseline must contain no raw log lines and no full parser payloads. It may
contain only:

- object and schema version
- baseline id
- linked issue URL
- source manifest path list
- source privacy summary
- expected count sections
- tolerance policy
- review notes

The baseline must never be updated automatically. V1 must not add:

- `--update-baseline`
- `--bless`
- `--accept`
- an environment variable that silently refreshes the baseline
- a CI action that refreshes the baseline

Baseline changes require human review in the PR diff. The PR body or review
handoff must explain:

- which manifest inputs changed
- which count sections changed
- whether the count change reflects broader corpus coverage, parser behavior
  drift, a fixture update, or a suspected bug
- why the new baseline is safe to accept

When no baseline is provided, the report may still be generated, but its status
must be `review` with reason `baseline_missing`. A missing baseline must not be
reported as `ok`.

### Baseline Schema

The V1 baseline must use this top-level shape:

```json
{
  "object": "mythic_edge_feature_equity_corpus_ratchet_baseline",
  "schema_version": "parser_feature_equity_corpus_ratchet_baseline.v1",
  "baseline_id": "parser_reliability_feature_equity_corpus_v1",
  "linked_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/119",
  "source_manifest_paths": [
    "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
    "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json"
  ],
  "source_privacy": {
    "privacy_class": "committed_count_only",
    "raw_private_log_committed": false
  },
  "expected": {
    "input_counts": {},
    "router_stats": {},
    "event_family_counts": {},
    "event_kind_counts": {},
    "payload_type_counts": {},
    "parser_claim_counts": {},
    "game_state_evidence_counts": {},
    "truncation_and_data_loss": {},
    "unknowns_and_degradation": {}
  },
  "tolerance_policy": {
    "exact_match_sections": [
      "input_counts",
      "router_stats",
      "event_family_counts",
      "event_kind_counts",
      "payload_type_counts",
      "parser_claim_counts",
      "game_state_evidence_counts",
      "truncation_and_data_loss",
      "unknowns_and_degradation"
    ],
    "minimum_sections": [],
    "review_on_new_unknowns": true,
    "review_on_new_timestamp_anomalies": true,
    "review_on_new_degradation": true,
    "review_on_new_data_loss": true
  },
  "review_notes": []
}
```

V1 may keep all count sections under exact-match policy. If Codex C decides that
a small number of count categories should be monotonic minimums instead of exact
matches, that choice must be documented in `tolerance_policy.minimum_sections`
and covered by focused tests.

### Report Schema

The V1 report must use this top-level shape:

```json
{
  "object": "mythic_edge_feature_equity_corpus_ratchet_report",
  "schema_version": "parser_feature_equity_corpus_ratchet_report.v1",
  "status": "ok",
  "status_reasons": [],
  "generated_at_utc": "2026-05-18T00:00:00Z",
  "inputs": {},
  "baseline": {},
  "observed": {},
  "comparison": {},
  "privacy": {},
  "protected_surfaces": {},
  "limitations": []
}
```

`generated_at_utc` is allowed to be volatile. Snapshot-style tests must either
normalize it or assert only that it is an ISO-like UTC timestamp.

Required report status values:

- `ok`
- `review`
- `diff`
- `fail`

Status precedence:

1. `fail`
2. `diff`
3. `review`
4. `ok`

The report must set `status` to:

- `ok` when a valid baseline is supplied, all compared sections match policy,
  and no review signals are present.
- `review` when the report builds but human attention is required without a
  count-policy mismatch. Examples: missing baseline, positive unknown count,
  positive timestamp anomaly count, positive degradation count, positive data
  loss count, or explicit manifest review flags.
- `diff` when a valid baseline is supplied and one or more count sections differ
  from the baseline policy.
- `fail` when inputs are unsafe or malformed, baseline schema is invalid, replay
  cannot run, or the report cannot be built reliably.

The CLI exit-code policy must remain report-oriented:

- return `0` for `ok`, `review`, and `diff`
- return non-zero for `fail` or unhandled command errors

This preserves the non-gate contract. A future CI or merge gate may not treat
`diff` as failing without a separate issue, contract, and explicit approval.

### Required Report Sections

#### inputs

`inputs` must include:

```json
{
  "manifest_paths": [],
  "manifest_count": 0,
  "source_file_count": 0,
  "source_file_paths": [],
  "input_kind": "golden_replay_manifest",
  "expanded_from_directories": [],
  "ordering": "sorted_repo_relative_path"
}
```

Path values must be repo-relative when the file is inside the repo.

#### baseline

`baseline` must include:

```json
{
  "path": "tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json",
  "present": true,
  "object": "mythic_edge_feature_equity_corpus_ratchet_baseline",
  "schema_version": "parser_feature_equity_corpus_ratchet_baseline.v1",
  "baseline_id": "parser_reliability_feature_equity_corpus_v1",
  "loaded": true,
  "validation_errors": []
}
```

When no baseline is supplied, `present` and `loaded` must be false and the report
must include `baseline_missing` in `status_reasons`.

#### observed

`observed` must include these required count sections:

```json
{
  "input_counts": {},
  "router_stats": {},
  "event_family_counts": {},
  "event_kind_counts": {},
  "payload_type_counts": {},
  "parser_claim_counts": {},
  "game_state_evidence_counts": {},
  "truncation_and_data_loss": {},
  "unknowns_and_degradation": {}
}
```

##### input_counts

`input_counts` must include:

- `manifests_total`
- `source_files_total`
- `fixtures_total`
- `fixtures_sanitized_committable`
- `fixtures_synthetic_committable`
- `fixtures_private_rejected`

##### router_stats

`router_stats` must include corpus-level sums:

- `routed`
- `unknown`
- `timestamp_missing`
- `timestamp_parse_failure`

These values must be counted from parser/replay-observed data, not from baseline
expectations alone.

##### event_family_counts

`event_family_counts` must count emitted parser event families by `event.kind`.

V1 must include zero-count keys for all current event families listed in
`src/mythic_edge_parser/events.py` so a missing family is explicit rather than
silently absent.

##### event_kind_counts

`event_kind_counts` must count concrete emitted event kinds. If event family and
event kind are identical in the current event model, this section may match
`event_family_counts` in V1, but it must remain present because future event
families may contain multiple concrete kinds.

##### payload_type_counts

`payload_type_counts` must count stable parser payload type labels when they are
present. The count key should be:

```text
<event.kind>:<payload.type>
```

If a payload has no `type`, use:

```text
<event.kind>:<missing>
```

The ratchet must not store the full payload.

##### parser_claim_counts

`parser_claim_counts` must count parser-owned claim families, not downstream
workbook formulas or AI interpretations. V1 categories must include:

- `match_lifecycle_claims`
- `game_result_claims`
- `client_action_claims`
- `rank_context_claims`
- `opponent_observation_claims`
- `game_state_claims`
- `final_reconciliation_claims`

These counts are coverage counts only. They do not assert that a claim is
semantically correct beyond the underlying parser tests and golden replay
fixtures.

##### game_state_evidence_counts

`game_state_evidence_counts` must summarize selected GRE evidence without
copying full payloads. V1 categories must include:

- `game_state_events`
- `connect_resp_events`
- `game_state_message_events`
- `queued_game_state_messages`
- `annotations_total_records`
- `annotations_degraded_records`
- `annotations_review_required`
- `annotation_type_counts`
- `annotation_marker_type_counts`
- `timers_total_records`
- `timers_degraded_records`
- `timers_review_required`
- `timer_type_counts`
- `timer_time_unit_counts`
- `diff_complete_snapshots`
- `diff_incremental_updates`
- `diff_queued_messages`
- `diff_previous_state_linked`
- `diff_previous_state_missing`
- `diff_deletion_evidence_present`
- `diff_deleted_instance_ids`
- `diff_deleted_annotation_ids`
- `diff_degraded_records`
- `diff_review_required`
- `diff_evidence_status_counts`
- `diff_value_source_counts`
- `diff_confidence_counts`
- `diff_source_field_counts`

If a category is not exercised by the current committed corpus, it must appear
with zero or an empty count object. Absence must not be used to mean zero.

##### truncation_and_data_loss

`truncation_and_data_loss` must include:

- `truncation_events`
- `fixtures_with_truncation`
- `data_loss_markers`
- `fixtures_with_data_loss`
- `data_loss_field_counts`

This section records evidence loss. It must not attempt to recover, reconstruct,
or infer missing GameState content.

##### unknowns_and_degradation

`unknowns_and_degradation` must include:

- `unknown_entries`
- `timestamp_missing`
- `timestamp_parse_failure`
- `degraded_parser_outputs`
- `review_required_outputs`
- `malformed_records`
- `unsupported_records`

Positive counts in this section should generally produce `review` unless a
baseline explicitly expects them and the count is unchanged. A future contract
may choose stricter handling for specific categories.

#### comparison

`comparison` must include:

```json
{
  "baseline_present": true,
  "sections_compared": [],
  "matching_sections": [],
  "diff_sections": [],
  "review_sections": [],
  "missing_expected_sections": [],
  "unexpected_observed_sections": [],
  "count_diffs": []
}
```

Each `count_diffs` entry must include:

```json
{
  "section": "event_family_counts",
  "key": "GameState",
  "expected": 6,
  "observed": 7,
  "delta": 1,
  "policy": "exact"
}
```

The report must compare counts deterministically. Object keys in emitted JSON
must be sorted where practical.

#### privacy

`privacy` must include:

```json
{
  "privacy_class": "committed_count_only",
  "raw_private_log_committed": false,
  "raw_log_lines_in_report": false,
  "forbidden_content_findings": [],
  "local_absolute_paths_redacted": true
}
```

#### protected_surfaces

`protected_surfaces` must include:

```json
{
  "parser_behavior_changed": false,
  "parser_state_final_reconciliation_changed": false,
  "parser_event_classes_changed": false,
  "match_or_game_identity_changed": false,
  "deduplication_changed": false,
  "workbook_schema_changed": false,
  "webhook_payload_shape_changed": false,
  "apps_script_behavior_changed": false,
  "ci_gate_changed": false,
  "production_behavior_changed": false
}
```

This section is a self-declaration for the report and tests. It is not a
substitute for protected-surface review.

#### limitations

`limitations` must state that:

- the ratchet measures corpus coverage shape, not semantic parser correctness
- the ratchet does not inspect live workbook state
- the ratchet does not inspect deployed Apps Script state
- the ratchet does not authorize baseline updates
- the ratchet does not decide merge readiness
- the ratchet does not implement the full Player.log evidence ledger
- the ratchet does not evaluate coaching quality or AI analytics

## Required Counting Rules

### General Counting Rules

- Count only data from explicit V1 manifest inputs.
- Do not count hidden local files.
- Do not count generated runtime artifacts.
- Do not count workbook exports.
- Do not use workbook formulas or Apps Script state as parser evidence.
- Do not parse raw log lines separately when the golden replay harness already
  owns routing for those manifest inputs.
- Prefer existing parser/replay/diagnostic data structures over ad hoc string
  parsing.
- Use zero or empty objects for known categories that are not observed.
- Sort paths and keys to keep reports deterministic.

### Event Family and Payload Rules

- Event family counts must use emitted parser event `kind`.
- Payload type counts must use payload metadata already emitted by parser
  modules.
- Missing payload type must be counted as `<missing>`, not ignored.
- Unknown router entries must be counted under router/unknowns sections, not
  invented as parser events.

### Parser Claim Rules

Parser claim counts are coverage counters for parser-owned output families.
They must not be used as proof that a claim is correct in isolation.

Allowed V1 claim sources:

- golden replay observed event summaries
- golden replay fixture-level expected section names
- parser diagnostics summaries
- normalized GRE summaries already attached by parser modules
- opponent observation summaries already produced by parser modules

Forbidden V1 claim sources:

- workbook helper formulas
- dashboard classifications
- user annotations
- AI-generated summaries
- hidden-card inference
- deck archetype inference
- coaching evaluations

### GameState Evidence Rules

GameState evidence counts must summarize normalized evidence objects that already
exist in parser-owned payloads. The ratchet may count the presence and labels of
these objects. It must not:

- derive new GameState mechanics
- reconstruct truncated GameState content
- infer hidden cards
- infer decklists
- decide whether a gameplay action was strategically correct
- promote GameState diagnostics into workbook truth

### Baseline Comparison Rules

- Missing baseline means `review`, not `ok`.
- Invalid baseline means `fail`.
- Baseline object/schema mismatch means `fail`.
- Input manifest list mismatch means `diff` unless the baseline policy explicitly
  allows a broader manifest set.
- Exact-match count mismatch means `diff`.
- Minimum-policy count below expected minimum means `diff`.
- Minimum-policy count above expected minimum remains `ok` unless another review
  signal applies.
- Positive unknown/timestamp/degradation/data-loss counts must produce `review`
  unless the baseline explicitly expects the exact same positive counts.

## Relationship To Existing Artifacts

### Golden Replay Harness

Golden replay remains the fixture-level oracle for replayed parser behavior.
The corpus ratchet may call golden replay or consume its in-memory report data,
but it must not replace golden replay manifest validation or fixture-local
expected checks.

If golden replay reports `fail` for an input manifest, the corpus ratchet must
report `fail`.

If golden replay reports `diff`, `review`, or `degraded`, the corpus ratchet must
include that fact in `status_reasons` and must not hide it behind aggregate
counts.

### Parser Diagnostics Mode

Parser diagnostics remains the module that summarizes parser health for a
single source/profile. The corpus ratchet may reuse diagnostics vocabulary, but
it should not duplicate transport, workbook, or Apps Script health checks.

### Saved Event Replay

Saved event replay remains a utility for replaying stored event records. It is
not a V1 corpus ratchet input source. A future contract may allow saved-event
replay summaries as an input class if privacy and schema rules are defined.

### Schema Snapshots

Event/schema snapshots guard shape. The corpus ratchet guards coverage shape.
The ratchet must not update schema snapshots and must not treat a count report
as a schema approval mechanism.

### Player.log Evidence Ledger

The evidence ledger remains the future source of field-level provenance,
confidence, finality, and drift labeling. The corpus ratchet may use compatible
labels and count categories, but it does not implement the ledger.

### Protected-Surface Gate

The ratchet report may note whether protected surfaces were touched by the
implementation pass, but it does not authorize such changes. Existing
protected-surface checks and human review remain authoritative.

## Unknowns And Open Questions

- The exact first V1 baseline counts should be generated by Codex C from the
  current committed golden replay manifests and reviewed in the implementation
  PR.
- It is unknown whether the first corpus should include only the two current
  golden replay manifests or add a tiny synthetic manifest specifically for
  GameState annotation/timer/diff coverage. If new fixture data is needed, that
  requires explicit implementation-scope review and must remain sanitized or
  synthetic.
- It is unknown whether parser claim counts should be derived entirely from
  golden replay observed sections or whether Codex C should call parser
  diagnostics per fixture. Either is acceptable if deterministic and tested.
- It is unknown whether future private local logs should feed the ratchet in a
  local-only mode. V1 must defer this.
- It is unknown whether a future CI report should run the ratchet. V1 must not
  add a failing gate.
- It is unknown whether a future human-readable Markdown summary is useful. V1
  may remain JSON-only.

## Suspected Implementation Gaps

- No `feature_equity_corpus_ratchet.py` module exists.
- No feature-equity corpus baseline directory exists.
- No focused tests exist for corpus-level feature-equity counts.
- Existing golden replay fixture coverage likely exercises only a subset of the
  GRE annotation, timer, and diff mechanics categories added by recent modules.
- Current diagnostics and replay reports may expose enough counts for a first
  implementation, but some GameState evidence counts may require a small
  summarizer over existing payload summaries.
- There is no approved baseline update workflow beyond ordinary PR review.
- No branch-local secret scanner script was observed during this contract pass.

## Protected Surfaces

V1 implementation must not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- parser event kind values
- parser payload shapes
- match identity
- game identity
- deduplication behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- live workbook state
- deployed Apps Script state
- generated card data
- runtime status files
- failed posts
- workbook exports
- production behavior
- CI required/failing gate behavior
- Pyright gate behavior
- secret or credential handling

V1 implementation must not commit:

- raw private Player.log files
- local runtime logs
- local generated reports unless explicitly approved as fixtures
- failed posts
- workbook exports
- secrets
- credentials
- tokens
- webhook URLs
- local-only machine artifacts

## Validation Requirements

### Contract Writer Validation

For this contract-only pass, run:

```powershell
git diff --check
@'
docs/contracts/parser_feature_equity_corpus_ratchet.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If branch-local secret scanning tooling is unavailable, report that it was not
run and leave it for Codex C/E if the tool exists on a later branch.

### Codex C Implementation Validation

Codex C should run the narrowest relevant validation first:

```powershell
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py
```

Then run related parser reliability validation:

```powershell
py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py
py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
```

Run the report commands:

```powershell
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
```

Run style and protected-surface validation:

```powershell
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/main
```

If a repo-approved secret scanner exists on the implementation branch, run it
against the new baseline, tests, and fixture paths.

### Codex E Review Validation

Codex E should independently review:

- report schema stability
- baseline schema stability
- path sorting and deterministic JSON output
- no raw log lines in baseline or report fixtures
- no automatic baseline update path
- `diff` remains report-only and exits zero
- invalid/private input fails
- missing baseline yields `review`
- baseline count mismatch yields `diff`
- golden replay failures propagate to the ratchet report
- protected surfaces remain untouched

## Acceptance Criteria

The implementation for issue #119 is acceptable when:

- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` exists.
- `tests/test_feature_equity_corpus_ratchet.py` covers the public API and CLI.
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  exists and contains count-only baseline data.
- The report object and schema version match this contract.
- The baseline object and schema version match this contract.
- Explicit manifest files and manifest directories are accepted.
- Manifest discovery order is deterministic.
- Unsafe/private inputs are rejected.
- Missing baseline returns a `review` report.
- Baseline mismatch returns a `diff` report.
- Malformed baseline returns a `fail` report.
- The CLI exits zero for `ok`, `review`, and `diff`.
- The CLI exits non-zero for `fail`.
- No automatic baseline update command exists.
- Reports contain counts, paths, and metadata only, not raw log lines.
- Protected surfaces are not changed.
- Focused tests and related parser reliability tests pass or failures are
  clearly identified as pre-existing.

## Out Of Scope

This contract does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- match/game identity changes
- workbook schema changes
- webhook payload changes
- Apps Script changes
- live workbook checks
- deployed Apps Script checks
- saved-event replay schema changes
- raw private Player.log fixture commits
- local private-log ratchet mode
- generated report commits outside explicit fixture/baseline files
- automatic baseline refresh
- CI/merge gate changes
- issue/tracker closure authority
- production deployment
- coaching evaluation
- AI analytics scoring
- OpenAI API runtime integration

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #119:
https://github.com/Tahjali11/Mythic-Edge/issues/119

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Current integration branch:
codex/parser-reliability-intelligence

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_saved_event_replay.md
- docs/contracts/parser_gsm_truncation.md
- docs/contracts/parser_annotation_normalization.md
- docs/contracts/parser_timer_normalization.md
- docs/contracts/parser_game_state_diff_mechanics.md
- docs/contracts/parser_opponent_card_observations.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_golden_replay_harness.py
- tests/test_parser_diagnostics_mode.py
- tests/test_gre_game_state_parser.py
- tests/test_gre_annotations_parser.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_diff_parser.py
- tests/test_opponent_card_observations.py
- tests/fixtures/golden_replay/

Goal:
Compare the current code and fixtures against docs/contracts/parser_feature_equity_corpus_ratchet.md, then implement the narrow report-only V1 parser feature-equity corpus ratchet if the contract is implementable as written.

Before editing:
- Confirm the branch is codex/parser-reliability-intelligence and even with origin.
- Inspect git status and exclude unrelated changes.
- State what the ratchet is supposed to do, what the repo already does, what gap remains, why the gap exists, and the exact minimal implementation plan.

Implement:
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json

Required behavior:
- Consume explicit golden replay manifest files or directories.
- Produce a deterministic JSON report with object/schema:
  - mythic_edge_feature_equity_corpus_ratchet_report
  - parser_feature_equity_corpus_ratchet_report.v1
- Support a count-only baseline with object/schema:
  - mythic_edge_feature_equity_corpus_ratchet_baseline
  - parser_feature_equity_corpus_ratchet_baseline.v1
- Return status ok/review/diff/fail according to the contract.
- Keep diff/review report-only and non-gating.
- Reject unsafe/private inputs.
- Do not add automatic baseline refresh/bless behavior.
- Do not store raw log lines in reports or baselines.

Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, live workbook state, deployed Apps Script state, generated card data, runtime status files, failed posts, workbook exports, production behavior, CI gate behavior, Pyright gate behavior, secrets, credentials, raw private logs, or local-only artifacts.

Validation:
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py
py -m pytest -q tests\test_golden_replay_harness.py tests\test_parser_diagnostics_mode.py tests\test_saved_event_replay.py
py -m pytest -q tests\test_gre_game_state_parser.py tests\test_gre_annotations_parser.py tests\test_gre_timers_parser.py tests\test_gre_game_state_diff_parser.py tests\test_opponent_card_observations.py tests\test_gsm_truncation_parser.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/main

Final handoff must include:
- role performed
- issue and tracker used
- contract used
- files changed
- exact module/test/baseline sections changed
- observed behavior
- implementation summary
- validation run
- remaining unverified surfaces
- whether forbidden scope was touched
- next recommended role: Codex E / Module Reviewer
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/119"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/problem_representations/parser_feature_equity_with_manasight.md and issue #119"
  target_artifact: "src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py plus focused tests and count-only baseline"
  contract_artifact: "docs/contracts/parser_feature_equity_corpus_ratchet.md"
  risk_tier: "Medium"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/parser_feature_equity_corpus_ratchet.md"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not add automatic baseline refresh or bless behavior."
    - "Do not add CI or merge gates."
    - "Do not commit raw private logs or local reports."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, runtime status files, failed posts, workbook exports, or production behavior."
    - "Do not close tracker #47."
```
