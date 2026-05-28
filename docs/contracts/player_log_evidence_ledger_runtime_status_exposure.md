# Player.log Evidence Ledger Runtime Status Exposure Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/183
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/182
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/185
- previous_merge_commit: ee80e4b08ff12f904e745535877de72e856cc85b
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-runtime-status-exposure
- target_artifact: docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md
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
- docs/contracts/player_log_evidence_ledger_validation_report_wiring.md
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
- docs/contracts/parser_diagnostics_mode.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #183 defines the final narrow runtime-facing #11 slice: optional local
runtime status exposure of Player.log evidence-ledger health.

The evidence ledger now has Tier 1-7 provenance, schema snapshots, schema
drift reports, invariant execution, runtime field-evidence sidecar output, and
validation report wiring for diagnostics, golden replay, and feature-equity
reports. Those surfaces are useful for review, but normal runtime status does
not yet have a stable summary field for evidence-ledger health.

Runtime status is operationally visible. It may be read by launchers, local
status APIs, overlays, dashboards, or future automation. This contract permits
only a local, summary-only, review-oriented status summary. It must not become
parser truth, live Arena drift proof, CI truth, merge readiness, deploy
readiness, workbook truth, webhook truth, Apps Script truth, analytics truth,
AI truth, or gameplay advice.

Plain English: runtime status may say "evidence-ledger review health is
currently pass/review/fail/unavailable according to these supplied local
review summaries." It must not say "the parser is correct," "this branch is
ready to merge," "the workbook should change," or "Arena behavior has drifted
globally."

## Scope Decision

Runtime status exposure is approved in this slice, with these limits:

- V1 may add one additive runtime status field named `evidence_ledger_health`.
- V1 may add a pure helper module that builds the summary object.
- V1 may add an explicit helper for writing that summary through the existing
  `diagnostics.update_runtime_status(...)` mechanism.
- V1 may allow `/status` to expose the field because `/status` already returns
  the current local status artifact unchanged.
- V1 must not add new status API routes.
- V1 must not change `/health` output, top-level runtime `status`, parser
  health, transport health, diagnostics report shape, workbook/webhook/App
  Script surfaces, overlay behavior, or launcher behavior.

Reasoning:

- A summary-only local field closes the #11 runtime visibility gap without
  embedding field evidence into parser or transport surfaces.
- Reusing `update_runtime_status(...)` avoids a second runtime-status writer.
- Keeping `/health` unchanged prevents launchers and automation from treating
  evidence-ledger health as operational liveness.
- Keeping status projection optional prevents evidence review metadata from
  becoming a hidden runtime dependency.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger vocabulary, field-evidence records, drift flags, finality labels,
confidence labels, value-source labels, invariant-status labels, validators,
and privacy posture.

`docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md` remains
authoritative for the local runtime field-evidence sidecar. Issue #183 may
consume a sidecar report summary, but it must not inline full attachments or
field-evidence records into runtime status.

`docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`
remains authoritative for `evidence_ledger_review` sections in diagnostics,
golden replay, and feature-equity reports. Issue #183 may consume an
`evidence_ledger_review` section as a preferred source summary, but it must
not change validation report behavior or parent report statuses.

`docs/contracts/player_log_evidence_ledger_invariant_execution.md`,
`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`, and
`docs/contracts/player_log_evidence_ledger_schema_drift_report.md` remain
authoritative for their report shapes and status semantics. Issue #183 may
summarize their report statuses and counts only.

`docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
remains authoritative for Tier 6 ledger provenance fields
`diagnostics_status`, `unknown_entry_count`, and `truncation_count`. Issue
#183 is different: it exposes evidence-ledger review health in runtime status.
It must not add ledger seed fields, reinterpret Tier 6 fields, or change
diagnostics/drift/truncation behavior.

## Owning Layer

Owning layer: parser resilience / local runtime status review metadata.

Truth boundary:

- Parser modules, router dispatch, parser events, `app/state.py`, and
  `app/models.py` remain truth producers for parser-owned facts.
- Evidence-ledger modules own provenance metadata and review reports.
- `app/diagnostics.py` owns local runtime status writing.
- `app/status_api.py` owns local read-only HTTP exposure of already written
  runtime artifacts.
- The new runtime status exposure layer owns only the
  `evidence_ledger_health` summary object and helper behavior for placing that
  object in local runtime status.
- Launchers, overlays, dashboards, workbook sheets, webhooks, Apps Script,
  analytics, AI, OpenAI/model-provider output, CI, merge, and deploy policy
  remain downstream or out of scope.

The runtime status exposure layer must not become:

- a parser
- parser state
- parser final reconciliation
- live Arena drift truth
- diagnostics parser-health truth
- diagnostics transport-health truth
- validation report truth
- runtime liveness truth
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- ActionLogRow shape
- Match Journal, overlay, SQLite, or Google Sheets sync behavior
- analytics truth, AI truth, or model-provider truth
- CI, merge, deploy, or tracker-completion authority

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`ee80e4b08ff12f904e745535877de72e856cc85b`:

- Issue #11 is open.
- Issue #182 is closed and merged through PR #185.
- Issue #183 is open.
- `src/mythic_edge_parser/app/diagnostics.py` writes local runtime status via
  `update_runtime_status(**fields)`.
- Runtime status is stored in a local status artifact named
  `manasight_status_latest.json` under `STATUS_ROOT`.
- `update_runtime_status(...)` normalizes JSON-safe values, updates the
  in-memory `_STATUS_STATE`, refreshes `updated_at`, and writes the status
  artifact.
- `setup_runtime_logging()` initializes runtime status with:
  - `started_at`
  - `runtime_log_path`
  - `status`
  - `webhook_successes`
  - `webhook_failures`
  - `event_failures`
  - `router_failures`
- `runner.py` writes startup, running, status API, and stopped status fields
  through `update_runtime_status(...)`.
- `runtime_surfaces.py` writes some runtime artifact path/count fields through
  `update_runtime_status(...)`.
- `status_api.py` exposes:
  - `/status`: the full local runtime status artifact
  - `/health`: a narrow operational health summary from selected runtime
    status fields
  - other existing local runtime artifact routes
- `/health` currently does not expose evidence-ledger health.
- `/status` returns the current status artifact unchanged when present.
- `parser_diagnostics.py` can consume optional runtime status for transport
  health, but missing runtime status is not a parser failure.
- `evidence_validation_report_wiring.py` builds
  `evidence_ledger_review` sections with statuses:
  `not_supplied`, `pass`, `degraded`, `review`, `diff`, `fail`.
- `runtime_field_evidence.py` builds review-only sidecar reports with statuses
  `pass`, `review`, and `fail`.
- `evidence_invariant_execution.py` builds review-only invariant reports with
  statuses `pass`, `review`, and `fail`.
- `evidence_schema_drift_report.py` and schema snapshot comparison surfaces
  are review evidence, not parser truth.
- No `evidence_ledger_health` runtime status field exists.
- No runtime-status helper currently summarizes evidence-ledger review health.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_runtime_status.py
- tests/test_evidence_runtime_status.py
- docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md

Existing files authorized for narrow additive integration:

- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- tests/test_diagnostics.py
- tests/test_status_api.py

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- src/mythic_edge_parser/app/runtime_field_evidence.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/runner.py
- tests/test_evidence_validation_report_wiring.py
- tests/test_runtime_field_evidence.py
- tests/test_evidence_invariant_execution.py
- tests/test_evidence_schema_snapshot.py
- tests/test_evidence_schema_drift_report.py
- tests/test_parser_diagnostics_mode.py
- tests/test_runtime_surfaces.py
- tests/test_runner.py

## Public Interface

Recommended module:

```python
src/mythic_edge_parser/app/evidence_runtime_status.py
```

Required constants:

```python
EVIDENCE_LEDGER_HEALTH_OBJECT = "mythic_edge_player_log_evidence_ledger_runtime_health"
EVIDENCE_LEDGER_HEALTH_SCHEMA_VERSION = "player_log_evidence_ledger_runtime_health.v1"
EVIDENCE_LEDGER_HEALTH_STATUSES = (
    "unavailable",
    "pass",
    "degraded",
    "review",
    "diff",
    "fail",
)
EVIDENCE_LEDGER_HEALTH_SOURCE_KEYS = (
    "evidence_ledger_review",
    "runtime_field_evidence_report",
    "schema_drift_report",
    "invariant_execution_report",
    "schema_snapshot_comparison",
)
```

Required public functions:

```python
from collections.abc import Mapping
from typing import Any


def build_evidence_ledger_health_status(
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...


def update_evidence_ledger_health_status(
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...
```

Allowed implementation form:

- pure summary builder returning JSON-serializable dictionaries
- explicit writer helper that calls `diagnostics.update_runtime_status(...)`
  with only `evidence_ledger_health=<summary>`
- standard-library-only implementation
- no environment variable contract
- no CLI required in V1
- no network calls
- no implicit filesystem discovery
- no reads of raw Player.log, runtime status files, failed posts, workbook
  exports, generated card data, local logs, or secrets

`update_evidence_ledger_health_status(...)` may write the existing local
runtime status artifact through `diagnostics.update_runtime_status(...)`.
That is the only runtime file side effect authorized by this contract.

## Runtime Status Field

The only approved new runtime status field is:

```yaml
evidence_ledger_health:
  object: "mythic_edge_player_log_evidence_ledger_runtime_health"
  schema_version: "player_log_evidence_ledger_runtime_health.v1"
  status: "unavailable"
  review_required: false
  status_affects_runtime_status: false
  status_affects_parser: false
  status_affects_transport: false
  status_affects_workbook: false
  status_affects_overlay: false
  status_affects_ci_merge_deploy: false
  status_reasons: []
  source_refs:
    evidence_ledger_review:
      supplied: false
      object: ""
      schema_version: ""
      status: "unavailable"
      review_required: false
      status_reasons: []
      summary: {}
    runtime_field_evidence_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "unavailable"
      review_required: false
      status_reasons: []
      summary: {}
    schema_drift_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "unavailable"
      review_required: false
      status_reasons: []
      summary: {}
    invariant_execution_report:
      supplied: false
      object: ""
      schema_version: ""
      status: "unavailable"
      review_required: false
      status_reasons: []
      summary: {}
    schema_snapshot_comparison:
      supplied: false
      object: ""
      schema_version: ""
      status: "unavailable"
      review_required: false
      status_reasons: []
      summary: {}
  summary:
    supplied_source_count: 0
    pass_count: 0
    degraded_count: 0
    review_count: 0
    diff_count: 0
    fail_count: 0
    unavailable_count: 5
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
    privacy_finding_count: 0
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
    runtime_status_contents_included: false
    failed_posts_included: false
    workbook_exports_included: false
    secrets_or_credentials_included: false
    full_field_evidence_attachments_included: false
    full_schema_snapshots_included: false
    ai_or_model_provider_output_included: false
  protected_surface_assertions:
    parser_behavior_changed: false
    parser_state_final_reconciliation_changed: false
    parser_event_classes_changed: false
    router_semantics_changed: false
    diagnostics_report_shape_changed: false
    validation_report_status_semantics_changed: false
    runtime_status_top_level_status_changed: false
    status_api_routes_changed: false
    health_endpoint_changed: false
    workbook_schema_changed: false
    webhook_payload_shape_changed: false
    apps_script_behavior_changed: false
    output_transport_changed: false
    action_log_row_shape_changed: false
    match_journal_behavior_changed: false
    overlay_behavior_changed: false
    sqlite_behavior_changed: false
    google_sheets_sync_behavior_changed: false
    analytics_or_ai_truth_changed: false
    ci_merge_deploy_policy_changed: false
  limitations: []
```

Shape rules:

- The field must be absent unless a caller explicitly builds and writes it.
- If present, the field must be a dictionary with the shape above.
- The field must be summary-only.
- The field must not include raw report attachments, raw field evidence,
  invariant result lists, full schema snapshots, full drift diffs, raw parser
  output values, raw payload values, local absolute paths, runtime status
  contents, failed post contents, workbook exports, secrets, webhook URLs, or
  AI/model-provider output.
- `status_affects_runtime_status` and every `status_affects_*` flag must be
  `false` in V1.
- V1 must not add any other new runtime status field for evidence-ledger
  health.

## Allowed Inputs

Allowed in-memory inputs:

1. `evidence_ledger_review`
   - object:
     `mythic_edge_player_log_evidence_ledger_validation_review`
   - schema version:
     `player_log_evidence_ledger_validation_review.v1`
   - statuses:
     `not_supplied`, `pass`, `degraded`, `review`, `diff`, `fail`
   - preferred source when present because it is already summary-only and
     already wired into validation reports.

2. `runtime_field_evidence_report`
   - object:
     `mythic_edge_player_log_runtime_field_evidence_report`
   - schema version:
     `player_log_runtime_field_evidence_report.v1`
   - statuses: `pass`, `review`, `fail`
   - allowed summary fields are the same summary fields allowed by
     `docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`.
   - full `attachments` and `field_evidence` records are forbidden.

3. `schema_drift_report`
   - object:
     `mythic_edge_player_log_evidence_schema_drift_report`
   - schema version:
     `player_log_evidence_schema_drift_report.v1`
   - statuses: `pass`, `review`, `fail`
   - summary-only.

4. `invariant_execution_report`
   - object:
     `mythic_edge_player_log_evidence_invariant_execution_report`
   - schema version:
     `player_log_evidence_invariant_execution.v1`
   - statuses: `pass`, `review`, `fail`
   - summary-only.

5. `schema_snapshot_comparison`
   - object:
     `mythic_edge_player_log_evidence_schema_snapshot_comparison`
   - schema version:
     `player_log_evidence_schema_snapshot_comparison.v1`
   - statuses: `pass`, `diff`, `fail`
   - summary-only.

Allowed source material is explicit in-memory mappings only. V1 must not add a
CLI, environment variable, default path, background watcher, implicit report
discovery, or automatic report generation.

## Forbidden Inputs

V1 must not read or consume:

- raw private Player.log excerpts
- live local MTGA logs
- raw local logs
- runtime status files as evidence input
- failed posts
- workbook exports
- generated card data
- active deck profile artifacts
- active match snapshot artifacts
- match timelines
- match history
- collection profile artifacts
- local absolute paths
- local usernames
- webhook URLs
- environment variable values
- secrets, credentials, tokens, API keys
- OpenAI/model-provider output
- AI summaries
- external metagame data
- live workbook state
- deployed Apps Script state
- GitHub issue, PR, CI, or branch state

Runtime status exposure must be fed by explicit review summaries. It must not
become a report collector, file scanner, live diagnostics runner, schema drift
builder, invariant executor, or runtime field-evidence builder.

## Status Normalization

Allowed `evidence_ledger_health.status` values:

- `unavailable`
- `pass`
- `degraded`
- `review`
- `diff`
- `fail`

Precedence from strongest to weakest:

1. `fail`
2. `diff`
3. `review`
4. `degraded`
5. `pass`
6. `unavailable`

Source status mapping:

- `not_supplied` maps to `unavailable`.
- `unavailable` maps to `unavailable`.
- `pass` maps to `pass`.
- `ok` maps to `pass` only when supplied by an already sanitized validation
  review section.
- `degraded` maps to `degraded`.
- `review` maps to `review`.
- `diff` maps to `diff`.
- `fail` maps to `fail`.
- `unknown` maps to `review` when the source was explicitly supplied.
- malformed supplied source reports map to `fail`.
- unknown object, schema version, or status maps to `fail`.

Overall status behavior:

- No supplied source reports -> `unavailable`, `review_required=false`.
- Supplied source reports all pass -> `pass`, `review_required=false`.
- Any degraded source and no stronger status -> `degraded`,
  `review_required=true`.
- Any review source and no stronger status -> `review`,
  `review_required=true`.
- Any diff source and no fail -> `diff`, `review_required=true`.
- Any fail source -> `fail`, `review_required=true`.
- Privacy findings -> `fail`, `review_required=true`.
- Any protected-surface assertion true -> `fail`, `review_required=true`.

Runtime status projection policy:

- `evidence_ledger_health.status` must not alter top-level runtime
  `status`.
- It must not increment `event_failures`, `router_failures`, or
  `webhook_failures`.
- It must not alter `parser_diagnostics.overall_status`,
  `parser_health.status`, `transport_health.status`, or validation report
  parent status semantics.
- It must not alter `/health` status or fields in V1.
- It must not block startup, streaming, webhook dispatch, local status API
  startup, or shutdown.

## Relationship To Status API And Local Consumers

`status_api.py` behavior:

- `/status` may expose `evidence_ledger_health` because it returns the local
  status artifact unchanged.
- `/health` must remain unchanged in V1.
- No new route may be added for evidence-ledger health.
- No route may compute evidence-ledger health on request.
- No route may read raw logs, failed posts, workbook exports, generated data,
  schema snapshots, or report files to synthesize evidence-ledger health.

Launcher, overlay, dashboard, and future automation behavior:

- They may display `evidence_ledger_health.status`,
  `review_required`, `status_reasons`, counts, and review guidance if present.
- They must treat missing `evidence_ledger_health` as `unavailable`, not as a
  failure.
- They must not treat `pass` as parser correctness or live Arena drift proof.
- They must not treat `review`, `diff`, or `fail` as parser failure, transport
  failure, merge block, deploy block, tracker-completion block, or gameplay
  advice.
- This contract does not authorize overlay UI changes, Match Journal storage,
  SQLite schema changes, Google Sheets sync changes, dashboard changes, or
  launcher behavior changes.

## Privacy And Protected-Surface Assertions

The runtime health summary must preserve the strictest privacy posture from
source reports:

- no raw private Player.log excerpts
- no raw payload values
- no raw parser output values
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

Privacy findings must be path-only. The summary may say
`runtime_field_evidence_report.privacy.forbidden_content_findings` was
non-empty; it must not echo the forbidden value.

Protected-surface assertions must all be false for a clean V1 implementation.
If any protected-surface assertion is true, the summary status must be `fail`.
Codex C must route back to Codex B or A before implementing any protected
surface change not explicitly authorized by this contract.

## Error Behavior

- Missing optional sources produce `unavailable`.
- No supplied sources produce `status=unavailable`, `review_required=false`,
  and a limitation that no evidence-ledger health inputs were supplied.
- Non-mapping supplied sources produce `status=fail`.
- Unknown source object, schema version, or status produces `status=fail`.
- Malformed summary fields are ignored or counted as zero unless they indicate
  a protected-surface/privacy problem.
- Privacy findings in a supplied source produce `status=fail`.
- Protected-surface assertions in a supplied source produce `status=fail`.
- Full forbidden details in a supplied source must not be copied into runtime
  status. The health summary may record only sanitized path-style findings.
- Builder functions must not raise uncaught exceptions for malformed optional
  source mappings.
- The writer helper may propagate filesystem exceptions from the existing
  `diagnostics.update_runtime_status(...)` path; it must not swallow write
  failures as a successful runtime status update.

## Side Effects

Allowed side effects:

- `update_evidence_ledger_health_status(...)` may call
  `diagnostics.update_runtime_status(evidence_ledger_health=summary)`.
- Existing `diagnostics.update_runtime_status(...)` behavior may write the
  current local runtime status artifact.
- `/status` may expose the new field when it is already present in the status
  artifact.

Forbidden side effects:

- parser behavior changes
- parser state mutation
- parser event class changes
- router semantics changes
- diagnostics report shape or status semantic changes
- golden replay behavior changes
- feature-equity behavior changes
- runtime field-evidence behavior changes
- schema snapshot updates
- schema drift report behavior changes
- invariant execution behavior changes
- top-level runtime status semantic changes
- `/health` response changes
- status API route changes
- workbook writes or schema changes
- webhook posts or payload changes
- Apps Script changes
- output transport changes
- ActionLogRow shape changes
- active match snapshot shape changes
- match timeline shape changes
- match history shape changes
- active deck profile shape changes
- collection profile shape changes
- Match Journal, overlay, SQLite, or Google Sheets sync changes
- GitHub issue or tracker updates from runtime code
- network calls
- OpenAI/model-provider calls
- environment variable contract changes
- CI, merge, deploy, or tracker-completion policy changes

## Compatibility

Compatibility requirements:

- Existing runtime status fields remain unchanged.
- Existing top-level runtime `status` labels remain unchanged.
- Existing `diagnostics.update_runtime_status(...)` call sites continue to
  work.
- Existing `diagnostics._safe_json_value(...)` behavior remains compatible.
- Existing `/status` behavior remains "return status artifact unchanged."
- Existing `/health` shape remains unchanged.
- Existing `status_api._ROUTES` remains unchanged.
- Existing parser diagnostics, golden replay, feature-equity, runtime
  field-evidence, invariant execution, schema snapshot, and schema drift report
  shapes remain unchanged.
- Missing `evidence_ledger_health` is valid and means unavailable/not written.
- Existing runtime status tests must continue to pass without requiring
  evidence-ledger health input.

## Invariants

Required invariants:

- `evidence_ledger_health` is optional.
- If `evidence_ledger_health` is present, it is summary-only.
- `evidence_ledger_health.status_affects_runtime_status is False`.
- Every `status_affects_*` flag in `evidence_ledger_health` is false.
- All protected-surface assertions are false for clean reports.
- Any true protected-surface assertion fails the health summary.
- Privacy findings fail the health summary and are path-only.
- Full field-evidence attachments are not copied into runtime status.
- Full schema snapshots are not copied into runtime status.
- Full invariant results are not copied into runtime status.
- Full drift diffs are not copied into runtime status.
- Runtime status contents are not read as source evidence.
- `evidence_ledger_health.status` never changes top-level runtime `status`.
- `/health` never includes evidence-ledger health in V1.
- `/status` may expose the field only because it returns the status artifact.
- Missing evidence-ledger health is not an error.
- `pass` is advisory review metadata, not parser correctness.
- `fail` is advisory review metadata, not parser failure.

## Tests Required

Focused Codex C tests should cover:

- Builder returns `unavailable` when no sources are supplied.
- Builder summarizes a sanitized `evidence_ledger_review` section with status
  `pass`.
- Builder maps source `not_supplied` to `unavailable`.
- Builder maps runtime field-evidence `review` to health `review`.
- Builder maps schema snapshot comparison `diff` to health `diff`.
- Builder maps invariant execution or schema drift `fail` to health `fail`.
- Builder fails unknown source object, schema version, or status.
- Builder treats malformed non-mapping source input as `fail`.
- Builder strips or refuses full attachments, field-evidence records, invariant
  results, schema snapshots, and drift diffs.
- Privacy findings are path-only and do not echo raw values.
- Protected-surface assertion true fails the health summary.
- `update_evidence_ledger_health_status(...)` calls
  `diagnostics.update_runtime_status(...)` with only the
  `evidence_ledger_health` field.
- Existing `diagnostics.update_runtime_status(...)` can safely write a
  summary object.
- `/status` returns `evidence_ledger_health` when present in the status
  artifact.
- `/health` response remains unchanged and does not include
  `evidence_ledger_health`.
- Existing diagnostics, status API, runtime surfaces, runner, and evidence
  review tests continue to pass.

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py
python3 -m ruff check src tests tools
git diff --check
```

Codex E should rerun at least:

```bash
python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py
python3 -m ruff check src tests tools
git diff --check
```

Codex F/G must use normal workflow gates. `evidence_ledger_health` is not merge
readiness or deploy readiness by itself.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`
  exists and routes implementation to Codex C.
- The contract approves only optional, local, summary-only runtime status
  exposure.
- The contract defines exactly one new runtime status field:
  `evidence_ledger_health`.
- The contract forbids `/health` changes, new status API routes, parser
  behavior changes, runtime status top-level status changes, diagnostics report
  semantic changes, workbook/webhook/App Script/output changes, overlay/Match
  Journal/SQLite/Google Sheets sync changes, analytics truth, AI truth, and
  CI/merge/deploy policy changes.
- The contract defines allowed source summaries, forbidden inputs, status
  normalization, privacy behavior, protected-surface behavior, side effects,
  tests, validation, and handoff.
- The contract separates observed current behavior from required future
  guarantees.

## Unknowns And Suspected Gaps

- It is unknown whether a future overlay or launcher should display
  `evidence_ledger_health`. V1 permits consumers to display it if present but
  does not authorize UI behavior changes.
- It is unknown whether `/health` should eventually include a condensed
  evidence-ledger health status. V1 explicitly forbids `/health` changes.
- It is unknown whether runtime status should eventually discover or load
  evidence-ledger review reports from configured paths. V1 forbids implicit
  discovery and environment variable contracts.
- It is unknown whether evidence-ledger health should ever affect diagnostics,
  golden replay, feature-equity, CI, merge, deploy, or tracker decisions. V1
  forbids status promotion.
- It is unknown whether runtime status should retain historical
  evidence-ledger health changes. V1 exposes only the current status artifact.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #183, runtime status exposure for evidence-ledger health, under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/183
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/182
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/185
- Previous merge commit: ee80e4b08ff12f904e745535877de72e856cc85b
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md

Goal:
Implement the smallest optional local runtime status exposure for evidence-ledger health. Add a summary-only evidence_ledger_health runtime status object and helper behavior without changing parser behavior, top-level runtime status semantics, /health shape, status API routes, diagnostics report semantics, workbook/webhook/App Script/output surfaces, overlay/Match Journal/SQLite/Google Sheets sync behavior, analytics truth, AI truth, or CI/merge/deploy policy.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md
- docs/contracts/player_log_evidence_ledger_validation_report_wiring.md
- docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- docs/contracts/player_log_evidence_ledger_invariant_execution.md
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- src/mythic_edge_parser/app/runtime_field_evidence.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- tests/test_diagnostics.py
- tests/test_status_api.py
- tests/test_evidence_validation_report_wiring.py
- tests/test_runtime_field_evidence.py
- tests/test_evidence_invariant_execution.py
- focused runtime/status tests as needed

Implement:
- src/mythic_edge_parser/app/evidence_runtime_status.py
- tests/test_evidence_runtime_status.py
- narrow tests proving diagnostics.update_runtime_status can write evidence_ledger_health safely
- narrow status_api tests proving /status exposes the field when present and /health remains unchanged
- docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md if the workflow expects a test report

Required behavior:
- Add exactly one optional runtime status field: evidence_ledger_health.
- Build evidence_ledger_health from explicit in-memory source summaries only.
- Prefer an existing evidence_ledger_review section when supplied.
- Keep the object summary-only.
- Use statuses unavailable, pass, degraded, review, diff, fail.
- Treat missing sources as unavailable, not failure.
- Fail the health summary for malformed supplied sources, unknown object/schema/status values, privacy findings, or protected-surface assertions.
- Ensure evidence_ledger_health never changes top-level runtime status, parser status, transport status, diagnostics report status, /health shape, or CI/merge/deploy meaning.
- Ensure /status exposes the field only because it returns the existing status artifact.
- Do not add CLI, environment variable, implicit file discovery, background watchers, new routes, or status promotion.

Do not:
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics, top-level runtime status semantics, /health shape, status API routes, golden replay behavior, feature-equity behavior, runtime field-evidence behavior, schema snapshot behavior, schema drift behavior, invariant execution behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, active match snapshot shape, match timeline shape, match history shape, active deck profile shape, collection profile shape, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, or tracker lifecycle.
- Read raw private Player.log excerpts, raw local logs, generated data, runtime status files as input evidence, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, OpenAI/model-provider output, or AI summaries.
- Inline full runtime field-evidence attachments, full field_evidence records, full invariant results, full schema snapshots, full schema drift diffs, raw parser output values, raw payload values, runtime status contents, failed post contents, workbook exports, secrets, webhook URLs, or AI/model-provider output.
- Target main directly.
- Close tracker #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
- python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/183"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-runtime-status-exposure"
  validation:
    - "git diff --check"
    - "Documentation-only contract pass; focused tests deferred to Codex C."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics, top-level runtime status semantics, /health shape, status API routes, golden replay behavior, feature-equity behavior, runtime field-evidence behavior, schema snapshot behavior, schema drift behavior, invariant execution behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, active match snapshot shape, match timeline shape, match history shape, active deck profile shape, collection profile shape, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, or tracker lifecycle."
    - "Do not add evidence-ledger health to /health or add new status API routes in V1."
    - "Do not read raw private Player.log excerpts, raw local logs, generated data, runtime status files as input evidence, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, OpenAI/model-provider output, or AI summaries."
    - "Do not inline full runtime field-evidence attachments, full field_evidence records, full invariant results, full schema snapshots, full schema drift diffs, raw parser output values, raw payload values, runtime status contents, failed post contents, workbook exports, secrets, webhook URLs, or AI/model-provider output."
```
