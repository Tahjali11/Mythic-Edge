# Player.log Evidence Ledger Validation Report Wiring Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/182
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/181
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/184
- previous_merge_commit: 466f0f3c6013e5579af808db76773ca3c8206ff7
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-validation-report-wiring
- target_artifact: docs/contracts/player_log_evidence_ledger_validation_report_wiring.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_validation_report_wiring_comparison.md
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

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_invariant_execution.md
- docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #182 defines a report-only bridge from Player.log evidence-ledger review
surfaces into three existing validation reports:

- parser diagnostics
- golden replay
- feature-equity corpus ratchet

The evidence ledger can now describe Tier 1-7 provenance, schema snapshots,
schema drift reports, invariant execution, and runtime field-evidence sidecar
reports. Diagnostics, golden replay, and feature-equity reports are useful
review surfaces, but they do not yet have an explicit contract for consuming
those evidence-ledger reports.

This contract should answer:

> What evidence-ledger review context was available when this validation report
> was produced, and what should a reviewer inspect next?

It must not answer:

- whether parser behavior is semantically correct
- whether a golden fixture expected value should change
- whether a feature-equity baseline should update
- whether the report is merge readiness, deploy readiness, CI truth, workbook
  truth, analytics truth, AI truth, or tracker-completion authority
- whether evidence-ledger review metadata may change parser facts

Plain English: this wiring may add a clearly labeled evidence-review section
to validation reports. It must not make those reports stronger than review
evidence.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger vocabulary, field-evidence records, drift flags, and validation rules.

`docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md` remains
authoritative for the runtime field-evidence sidecar. Issue #182 may consume a
runtime field-evidence report summary, but it must not inline full attachments
by default, create field references from parser values, or attach field
evidence to existing parser/runtime/output surfaces.

`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md` remains
authoritative for deterministic schema snapshots and update policy. Issue #182
must not update committed snapshots.

`docs/contracts/player_log_evidence_ledger_schema_drift_report.md` remains
authoritative for schema drift report behavior. Issue #182 may consume schema
drift status and summary fields, but it must not reimplement drift comparison.

`docs/contracts/player_log_evidence_ledger_invariant_execution.md` remains
authoritative for invariant execution behavior. Issue #182 may consume
invariant execution status and summary fields, but it must not execute new
semantic parser invariants.

`docs/contracts/parser_diagnostics_mode.md`,
`docs/contracts/parser_golden_replay_harness.md`, and
`docs/contracts/parser_feature_equity_corpus_ratchet.md` remain authoritative
for their report purposes, input policies, status vocabularies, privacy
posture, and CLI behavior.

## Owning Layer

Owning layer: parser resilience / validation report integration metadata.

Truth boundary:

- Parser modules, `router.py`, `events.py`, `app/state.py`, and
  `app/models.py` remain parser truth producers.
- `app/evidence_ledger.py`, `app/evidence_schema_snapshot.py`,
  `app/evidence_schema_drift_report.py`,
  `app/evidence_invariant_execution.py`, and
  `app/runtime_field_evidence.py` remain owners of their own review artifacts.
- Diagnostics, golden replay, and feature-equity reports are validation and
  review consumers.
- The new validation report wiring owns a standardized
  `evidence_ledger_review` section and optional helper code for summarizing
  evidence-ledger review artifacts.
- The wiring must not mutate parser facts, recompute parser facts, infer
  missing facts, update expected golden outputs, update feature-equity
  baselines, or approve schema snapshots.

The validation report wiring must not become:

- a parser
- parser state
- final reconciliation
- golden replay fixture truth
- feature-equity baseline update policy
- diagnostics parser-health truth beyond the contracted review section
- runtime status schema
- workbook schema
- webhook payload
- Apps Script behavior
- output transport
- Match Journal, overlay, SQLite, or Google Sheets sync behavior
- analytics truth, AI truth, or model-provider truth
- CI, merge, deploy, or tracker-completion authority

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`466f0f3c6013e5579af808db76773ca3c8206ff7`:

- Issue #11 is open as the Player.log evidence-ledger and parser-resilience
  tracker.
- Issue #182 is open.
- `src/mythic_edge_parser/app/evidence_ledger.py` exposes the current
  evidence-ledger schema, vocabulary, entries, validators, and field-evidence
  validator.
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py` builds and compares
  deterministic evidence-ledger schema snapshots.
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py` builds
  review-only schema drift reports with statuses `pass`, `review`, and `fail`.
- `src/mythic_edge_parser/app/evidence_invariant_execution.py` builds
  review-only invariant execution reports with statuses `pass`, `review`, and
  `fail`.
- `src/mythic_edge_parser/app/runtime_field_evidence.py` builds local
  review-only runtime field-evidence sidecar reports with statuses `pass`,
  `review`, and `fail`.
- `src/mythic_edge_parser/app/parser_diagnostics.py` builds diagnostics
  reports:
  - object: `mythic_edge_parser_diagnostics_report`
  - schema version: `parser_diagnostics.v1`
  - top-level status key: `overall_status`
  - status labels: `pass`, `review`, `fail`, `unknown`
  - no `evidence_ledger_review` section exists yet.
- `src/mythic_edge_parser/app/golden_replay.py` builds golden replay reports:
  - object: `mythic_edge_golden_replay_report`
  - schema version: `parser_golden_replay_report.v1`
  - top-level status key: `suite_status`
  - status labels: `pass`, `degraded`, `review`, `diff`, `fail`
  - no `evidence_ledger_review` section exists yet.
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` builds
  feature-equity corpus reports:
  - object: `mythic_edge_feature_equity_corpus_ratchet_report`
  - schema version: `parser_feature_equity_corpus_ratchet_report.v1`
  - top-level status key: `status`
  - status labels: `ok`, `review`, `diff`, `fail`
  - no `evidence_ledger_review` section exists yet.
- Focused tests currently assert stable report shapes and privacy behavior for
  diagnostics, golden replay, feature-equity, schema snapshots, schema drift,
  invariant execution, and runtime field evidence.

## Scope Decision

Codex C should implement a shared report-section builder plus narrow optional
wiring into the three validation reports.

V1 should add a standardized `evidence_ledger_review` section to diagnostics,
golden replay, and feature-equity reports. The section may summarize supplied
or locally built evidence-ledger review artifacts. It must not inline raw
parser values, raw logs, full runtime field-evidence attachments, full schema
snapshots, full drift diffs, or full invariant result lists by default.

V1 should not alter parent report statuses by default. Instead, the section
must include a `status_affects_parent: false` marker and a clear local review
status. A later contract may authorize strict mode or parent-status promotion.

Reasoning:

- These reports are trusted review surfaces. Changing their top-level status
  semantics could accidentally create CI, merge, or deploy gates.
- Summary-only evidence keeps the report useful without copying large or
  sensitive review artifacts.
- A shared helper prevents three subtly different evidence-review shapes.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_validation_report_wiring.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- tests/test_evidence_validation_report_wiring.py
- docs/implementation_handoffs/player_log_evidence_ledger_validation_report_wiring_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_validation_report_wiring.md

Existing report files authorized for narrow report-only wiring:

- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_parser_diagnostics_mode.py
- tests/test_golden_replay_harness.py
- tests/test_feature_equity_corpus_ratchet.py

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/runtime_field_evidence.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- tests/test_evidence_ledger.py
- tests/test_runtime_field_evidence.py
- tests/test_evidence_invariant_execution.py
- tests/test_evidence_schema_snapshot.py
- tests/test_evidence_schema_drift_report.py

## Public Interface

Recommended shared module:

```python
src/mythic_edge_parser/app/evidence_validation_report_wiring.py
```

Required constants:

```python
EVIDENCE_LEDGER_REVIEW_OBJECT = "mythic_edge_player_log_evidence_ledger_validation_review"
EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION = "player_log_evidence_ledger_validation_review.v1"
EVIDENCE_LEDGER_REVIEW_STATUSES = (
    "not_supplied",
    "pass",
    "degraded",
    "review",
    "diff",
    "fail",
)
EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS = (
    "runtime_field_evidence_report",
    "schema_drift_report",
    "invariant_execution_report",
    "schema_snapshot_comparison",
)
```

Required public functions:

```python
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def build_evidence_ledger_review_section(
    *,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
    report_context: str,
) -> dict[str, Any]:
    ...


def load_evidence_review_json(path: Path) -> dict[str, Any]:
    ...


def evidence_review_cli_arguments(parser: Any) -> None:
    ...


def evidence_review_inputs_from_args(args: Any) -> dict[str, Any]:
    ...
```

`report_context` must be one of:

- `parser_diagnostics`
- `golden_replay`
- `feature_equity_corpus_ratchet`
- `synthetic_test_reference`

Allowed implementation form:

- pure functions returning JSON-serializable dictionaries
- standard-library-only helper code
- no environment variable contract
- no network calls
- no default writes
- no reads of raw Player.log or runtime artifacts

The helper may load explicit JSON report paths passed by CLI arguments. It must
not discover files implicitly.

## Report Builder Wiring

Diagnostics may add optional keyword arguments:

```python
def build_parser_diagnostics_report(
    source_log: Path,
    *,
    profile: str = DEFAULT_PROFILE,
    runtime_status: dict[str, Any] | None = None,
    drift_baseline: dict[str, Any] | None = None,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...
```

Golden replay may add optional keyword arguments:

```python
def build_golden_replay_report(
    manifest_paths: Sequence[Path],
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...
```

Feature equity may add optional keyword arguments:

```python
def build_feature_equity_corpus_report(
    manifest_paths: Sequence[Path],
    *,
    baseline_path: Path | None = None,
    evidence_ledger_review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...
```

CLI wrappers may accept explicit evidence review inputs:

- `--evidence-runtime-field-report PATH`
- `--evidence-schema-drift-report PATH`
- `--evidence-invariant-report PATH`
- `--evidence-schema-snapshot-comparison PATH`

CLI wrappers must not add an update flag, strict status flag, environment
variable, or default filesystem discovery in V1.

## Output Shape

Each integrated report must include a top-level `evidence_ledger_review`
section. Add it at the end of the report object to minimize disruption to
existing report readers.

Required section shape:

```yaml
evidence_ledger_review:
  object: "mythic_edge_player_log_evidence_ledger_validation_review"
  schema_version: "player_log_evidence_ledger_validation_review.v1"
  report_context: "parser_diagnostics"
  status: "not_supplied"
  review_required: false
  status_affects_parent: false
  status_reasons: []
  summary:
    source_report_count: 0
    supplied_source_report_count: 0
    pass_count: 0
    degraded_count: 0
    review_count: 0
    diff_count: 0
    fail_count: 0
    runtime_field_evidence_attachment_count: 0
    runtime_field_evidence_review_required_count: 0
    runtime_field_evidence_missing_mapping_count: 0
    schema_drift_changed_entry_count: 0
    schema_drift_changed_signal_count: 0
    invariant_failed_count: 0
    invariant_degraded_count: 0
    invariant_not_checked_count: 0
    drift_flag_count: 0
    protected_surface_violation_count: 0
  sources:
    runtime_field_evidence_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "not_supplied"
      review_required: false
      status_reasons: []
      summary: {}
    schema_drift_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "not_supplied"
      review_required: false
      status_reasons: []
      summary: {}
    invariant_execution_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "not_supplied"
      review_required: false
      status_reasons: []
      summary: {}
    schema_snapshot_comparison:
      supplied: false
      object: ""
      schema_version: ""
      status: "not_supplied"
      review_required: false
      status_reasons: []
      summary: {}
  drift_flags: []
  affected:
    output_families: []
    entries: []
    evidence_signals: []
  review_guidance:
    recommended_review_modules: []
    recommended_tests: []
    review_notes: []
  privacy:
    forbidden_content_findings: []
    local_absolute_paths_found: []
    raw_private_logs_included: false
    raw_payload_values_included: false
    runtime_artifacts_included: false
    generated_data_included: false
    full_field_evidence_attachments_included: false
    full_schema_snapshots_included: false
  protected_surface_assertions:
    parser_behavior_changed: false
    parser_state_final_reconciliation_changed: false
    parser_event_classes_changed: false
    router_semantics_changed: false
    diagnostics_report_semantics_changed: false
    golden_replay_expected_fixture_truth_changed: false
    feature_equity_baseline_update_policy_changed: false
    workbook_schema_changed: false
    webhook_payload_shape_changed: false
    apps_script_behavior_changed: false
    output_transport_changed: false
    runtime_status_schema_changed: false
    match_journal_behavior_changed: false
    overlay_behavior_changed: false
    sqlite_behavior_changed: false
    google_sheets_sync_behavior_changed: false
    analytics_or_ai_truth_changed: false
    ci_merge_deploy_policy_changed: false
  limitations: []
```

The section must be summary-only. It must not include:

- `attachments` from runtime field-evidence reports
- full `field_evidence` records
- full `invariant_results`
- full schema snapshots
- full schema drift diffs
- raw parser output values
- raw payload values
- raw log lines
- runtime status contents
- failed post contents
- workbook exports

## Allowed Source Reports

Allowed source report inputs:

1. Runtime field evidence report
   - object: `mythic_edge_player_log_runtime_field_evidence_report`
   - schema version: `player_log_runtime_field_evidence_report.v1`
   - statuses: `pass`, `review`, `fail`
   - allowed summary fields:
     - `attachment_count`
     - `valid_field_evidence_count`
     - `missing_mapping_count`
     - `ambiguous_mapping_count`
     - `review_required_count`
     - `conflict_count`
     - `degraded_count`
     - `not_checked_count`
     - `drift_flag_count`
   - full attachments are forbidden in integrated reports.

2. Evidence schema drift report
   - object: `mythic_edge_player_log_evidence_schema_drift_report`
   - schema version: `player_log_evidence_schema_drift_report.v1`
   - statuses: `pass`, `review`, `fail`
   - allowed summary fields:
     - `output_family_changes`
     - `entry_changes`
     - `evidence_signal_changes`
     - `vocabulary_changes`
     - `policy_changes`
     - `privacy_findings`
   - full drift details are forbidden in integrated reports unless a future
     contract authorizes them.

3. Evidence invariant execution report
   - object: `mythic_edge_player_log_evidence_invariant_execution_report`
   - schema version: `player_log_evidence_invariant_execution.v1`
   - statuses: `pass`, `review`, `fail`
   - allowed summary fields:
     - `executable_invariant_count`
     - `declared_invariant_total_count`
     - `declared_invariant_unique_count`
     - `passed_count`
     - `failed_count`
     - `degraded_count`
     - `not_applicable_count`
     - `not_checked_count`
     - `affected_entry_count`
     - `affected_output_family_count`
     - `drift_flag_count`
   - full invariant result lists are forbidden in integrated reports.

4. Evidence schema snapshot comparison
   - object: `mythic_edge_player_log_evidence_schema_snapshot_comparison`
   - schema version: `player_log_evidence_schema_snapshot_comparison.v1`
   - statuses: `pass`, `diff`, `fail`
   - allowed summary fields:
     - `output_family_changes`
     - `entry_changes`
     - `evidence_signal_changes`
     - `vocabulary_changes`
     - `policy_changes`
     - `privacy_findings`
   - full snapshots and full diffs are forbidden in integrated reports.

Unknown object names, schema versions, or statuses must make the
`evidence_ledger_review` section status `fail`.

## Status Normalization

The `evidence_ledger_review.status` value must be derived from supplied source
reports using this precedence:

1. `fail`
2. `diff`
3. `review`
4. `degraded`
5. `pass`
6. `not_supplied`

Source status mapping:

- `pass` maps to `pass`.
- `ok` maps to `pass` only for feature-equity source contexts.
- `degraded` maps to `degraded`.
- `review` maps to `review`.
- `diff` maps to `diff`.
- `fail` maps to `fail`.
- `unknown` maps to `review` when the source was supplied.
- missing optional source reports map to `not_supplied`.
- malformed supplied source reports map to `fail`.

Parent report status policy:

- V1 must set `status_affects_parent: false`.
- V1 must not alter diagnostics `overall_status` based only on
  `evidence_ledger_review.status`.
- V1 must not alter golden replay `suite_status` based only on
  `evidence_ledger_review.status`.
- V1 must not alter feature-equity `status` based only on
  `evidence_ledger_review.status`.
- Privacy or protected-surface violations introduced by the integrated report
  itself must still fail the relevant report or raise before writing.

This policy intentionally separates "the parser/replay/corpus report says X"
from "evidence-ledger review context says Y."

## Report-Specific Boundaries

### Parser Diagnostics

Diagnostics may include `evidence_ledger_review` as local review context.

Allowed additions:

- top-level `evidence_ledger_review` section
- optional CLI arguments for explicit evidence review report JSON paths
- validation evidence notes naming evidence review inputs supplied

Forbidden changes:

- changing parser-health semantics
- treating evidence-ledger pass as parser-health pass
- treating evidence-ledger fail as proof of parser failure
- querying workbook or Apps Script
- changing runtime status schema
- reading runtime field-evidence reports implicitly
- reading raw logs beyond existing diagnostics input behavior

### Golden Replay

Golden replay may include `evidence_ledger_review` as suite-level review
context.

Allowed additions:

- top-level `evidence_ledger_review` section
- optional CLI arguments for explicit evidence review report JSON paths
- report metadata noting that evidence review is report-only

Forbidden changes:

- changing golden manifest schema
- changing `REQUIRED_EXPECTED_SECTIONS`
- changing expected fixture truth to satisfy evidence metadata
- changing fixture sanitization policy
- treating evidence-ledger pass as semantic parser correctness
- treating schema drift diff as permission to update expected outputs
- changing default CLI exit behavior for pass/degraded/review/diff/fail

### Feature-Equity Corpus Ratchet

Feature equity may include `evidence_ledger_review` as corpus-level review
context.

Allowed additions:

- top-level `evidence_ledger_review` section
- optional CLI arguments for explicit evidence review report JSON paths
- limitations noting that evidence review is not parity truth

Forbidden changes:

- changing count collection behavior
- changing count-only baseline shape
- changing baseline update policy
- treating evidence-ledger pass as feature parity
- treating evidence-ledger diff as baseline approval
- changing default CLI exit behavior

## Privacy And Protected-Surface Assertions

Integrated evidence review sections must preserve the strictest privacy
posture from the source reports:

- no raw private Player.log excerpts
- no raw payload values
- no local absolute paths
- no local usernames
- no runtime status file contents
- no failed post contents
- no workbook exports
- no generated card data
- no webhook URLs
- no secrets, credentials, API keys, or tokens
- no OpenAI/model-provider output
- no AI summaries

Privacy findings must be path-only. The integrated report may say
`schema_drift_report.privacy.local_absolute_paths_found` was non-empty; it must
not echo the sensitive value.

Protected-surface assertions must all be false for a clean V1 implementation.
If any protected-surface assertion is true, the evidence review section status
must be `fail`, and Codex C must route back for contract review unless the
change is explicitly authorized by a newer contract.

## Error Behavior

- Missing optional evidence review source reports produce `not_supplied`.
- No supplied source reports produce a section with status `not_supplied`,
  `review_required=false`, and a limitation that no evidence-ledger review
  inputs were supplied.
- Malformed supplied JSON produces section status `fail`.
- Unknown source report object or schema version produces section status
  `fail`.
- Unknown source report status produces section status `fail`.
- Privacy findings in supplied reports produce section status `fail`.
- Protected-surface assertions in supplied reports produce section status
  `fail`.
- Source reports with status `review` produce section status at least
  `review`.
- Source reports with status `diff` produce section status at least `diff`.
- Source reports with status `fail` produce section status `fail`.
- The integrated report must not throw uncaught exceptions for malformed
  optional evidence review inputs.

## Side Effects

Allowed side effects:

- Existing diagnostics report writes to explicit or existing local diagnostics
  paths as already authorized.
- Existing golden replay report writes to explicit output path as already
  authorized.
- Existing feature-equity report writes to explicit output path as already
  authorized.
- New helper reads only explicit source report paths passed by the caller.

Forbidden side effects:

- parser behavior changes
- parser state mutation
- parser event class changes
- router semantics changes
- runtime status writes or schema changes
- diagnostics report semantic changes outside `evidence_ledger_review`
- golden replay expected fixture truth changes
- feature-equity baseline writes or update policy changes
- schema snapshot updates
- schema drift behavior changes
- invariant execution behavior changes
- runtime field-evidence behavior changes
- workbook writes
- webhook posts
- Apps Script changes
- output transport changes
- Match Journal, overlay, SQLite, or Google Sheets sync changes
- GitHub issue or tracker updates from the module
- network calls
- OpenAI/model-provider calls
- environment variable contract changes

## Compatibility

Compatibility requirements:

- Existing report object names and schema versions remain unchanged:
  - `parser_diagnostics.v1`
  - `parser_golden_replay_report.v1`
  - `parser_feature_equity_corpus_ratchet_report.v1`
- Existing report status labels remain unchanged.
- Existing CLI exit policies remain unchanged.
- Existing golden replay manifest schema and expected sections remain
  unchanged.
- Existing feature-equity baseline schema and update policy remain unchanged.
- Existing diagnostics report semantics remain unchanged except for the
  additive top-level `evidence_ledger_review` section.
- Existing evidence-ledger, schema snapshot, schema drift, invariant execution,
  and runtime field-evidence tests must continue to pass.

## Tests Required

Focused Codex C tests should cover:

- Shared helper builds `not_supplied` section when no source reports are
  provided.
- Shared helper summarizes pass source reports as section status `pass`.
- Shared helper maps supplied runtime field-evidence `review` to section
  status `review`.
- Shared helper maps schema snapshot comparison `diff` to section status
  `diff`.
- Shared helper maps invariant execution or schema drift `fail` to section
  status `fail`.
- Unknown source object, schema version, or status fails the section.
- Privacy findings are path-only and do not echo raw values.
- Protected-surface assertion true fails the section.
- Diagnostics report includes `evidence_ledger_review` without changing
  parser-health section semantics.
- Golden replay report includes `evidence_ledger_review` without changing
  fixture expected sections or manifest schema.
- Feature-equity report includes `evidence_ledger_review` without changing
  count baseline comparison behavior.
- CLI options for explicit evidence report paths are optional and do not
  discover files implicitly.
- Existing CLI exit behavior remains unchanged.

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m ruff check src tests tools
git diff --check
```

Codex E should rerun at least:

```bash
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
python3 -m ruff check src tests tools
git diff --check
```

Codex F/G must use normal workflow gates. The `evidence_ledger_review` section
is not merge readiness by itself.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`
  exists and routes implementation to Codex C.
- The contract authorizes only report-only additions.
- The contract defines a shared `evidence_ledger_review` section.
- The contract forbids parent status changes by default.
- The contract forbids full attachment, snapshot, drift, invariant, raw log,
  raw payload, runtime status, failed post, workbook export, and secret data
  inclusion.
- The contract preserves parser behavior, golden fixture truth,
  feature-equity baseline policy, runtime status schema, workbook/webhook/App
  Script surfaces, analytics truth, AI truth, and deploy/merge policy.
- The contract lists focused validation and workflow handoff requirements.

## Unknowns And Suspected Gaps

- It is unknown whether future local review flows should promote
  `evidence_ledger_review.status` into parent report status. V1 forbids that
  default and leaves strict status projection for a later contract.
- It is unknown whether runtime status should expose evidence review counts.
  V1 forbids runtime status schema changes.
- It is unknown whether golden replay manifests should eventually declare
  expected evidence-ledger review summaries. V1 forbids manifest schema
  changes.
- It is unknown whether feature-equity baselines should eventually include
  evidence-ledger review count baselines. V1 forbids baseline policy changes.
- It is unknown whether Match Journal or overlay views should consume the
  evidence review section. V1 forbids those integrations.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #182, evidence-ledger validation report wiring, under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/182
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/181
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/184
- Previous merge commit: 466f0f3c6013e5579af808db76773ca3c8206ff7
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_validation_report_wiring.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_validation_report_wiring_comparison.md

Goal:
Implement the smallest report-only wiring that adds a standardized evidence_ledger_review section to diagnostics, golden replay, and feature-equity reports without changing parser behavior, report truth semantics, golden fixture truth, feature-equity baseline policy, runtime status schema, workbook/webhook/App Script surfaces, or AI/analytics truth.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_validation_report_wiring.md
- docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- docs/contracts/player_log_evidence_ledger_invariant_execution.md
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/runtime_field_evidence.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_runtime_field_evidence.py
- tests/test_evidence_invariant_execution.py
- tests/test_evidence_schema_snapshot.py
- tests/test_evidence_schema_drift_report.py
- tests/test_parser_diagnostics_mode.py
- tests/test_golden_replay_harness.py
- tests/test_feature_equity_corpus_ratchet.py

Implement:
- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- tests/test_evidence_validation_report_wiring.py
- narrow report-only additions in parser_diagnostics.py, golden_replay.py, and feature_equity_corpus_ratchet.py
- focused updates to existing report tests for the additive evidence_ledger_review section
- docs/implementation_handoffs/player_log_evidence_ledger_validation_report_wiring_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_validation_report_wiring.md if the workflow expects a test report

Required behavior:
- Add a top-level evidence_ledger_review section to diagnostics, golden replay, and feature-equity reports.
- Keep evidence_ledger_review summary-only.
- Consume only explicit evidence review report inputs.
- Preserve parent report statuses by default with status_affects_parent=false.
- Preserve existing CLI exit policies.
- Do not inline full runtime field-evidence attachments, full field_evidence records, full invariant results, full schema snapshots, full schema drift diffs, raw logs, raw payload values, runtime status contents, failed posts, workbook exports, secrets, webhook URLs, or AI/model-provider output.
- Fail the evidence_ledger_review section for malformed source reports, unknown object/schema/status values, privacy findings, or protected-surface assertions.

Do not:
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics outside the contracted report-only additions, golden replay expected fixture truth, feature-equity baseline update policy, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status schema, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, or deploy policy.
- Read raw private Player.log excerpts, raw local logs, generated data, runtime status files, failed posts, workbook exports, secrets, credentials, tokens, API keys, or webhook URLs.
- Target main directly.
- Close tracker #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m ruff check src tests tools
- git diff --check

End with:
- files changed
- comparison summary
- validation run
- remaining risks
- recommended next role
- workflow_handoff block to Codex E
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/182"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_validation_report_wiring.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_validation_report_wiring_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-validation-report-wiring"
  validation:
    - "git diff --check"
    - "Documentation-only contract pass; focused tests deferred to Codex C."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics outside contracted report-only additions, golden replay expected fixture truth, feature-equity baseline update policy, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status schema, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, or deploy policy."
    - "Do not inline full runtime field-evidence attachments, full field_evidence records, full invariant results, full schema snapshots, full schema drift diffs, raw logs, raw payload values, runtime status contents, failed posts, workbook exports, secrets, webhook URLs, or AI/model-provider output."
    - "Do not commit raw private Player.log excerpts, raw local logs, generated data, runtime status files, failed posts, workbook exports, secrets, credentials, tokens, API keys, or webhook URLs."
```
