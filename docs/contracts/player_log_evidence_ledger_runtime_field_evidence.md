# Player.log Evidence Ledger Runtime Field Evidence Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/181
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/179
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/180
- previous_merge_commit: 251a17cef4d508a8494aa876f9111016a6402593
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-runtime-field-evidence
- target_artifact: docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_runtime_field_evidence_comparison.md
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
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #181 defines the next narrow Player.log evidence-ledger resilience
layer: a controlled runtime field-evidence attachment boundary.

The evidence ledger can now describe parser-owned and parser-adjacent
provenance through Tier 7, deterministic schema snapshots, schema drift
reports, and invariant execution. The remaining gap is that local review
artifacts do not yet have a safe way to attach ledger-shaped field evidence to
the parser-owned output fields they are inspecting.

This contract should answer:

> Which ledger entry explains this local parser output field, what metadata is
> safe to show beside it, and what needs review?

It must not answer:

- whether the parser should change a value
- whether a value should be corrected, inferred, or overwritten
- whether workbook rows, webhook payloads, Apps Script, or output transport
  should carry field evidence
- whether diagnostics, golden replay, feature-equity reports, runtime status,
  Match Journal, overlay, SQLite, Google Sheets sync, analytics, AI, or a model
  provider become truth owners
- whether a PR is ready to merge, deploy, or close tracker #11

Plain English: this is a sidecar label maker for local review. It may point to
the ledger and say "this field has this evidence story." It must not touch the
field itself.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
the evidence-ledger object, vocabulary constants, validators, and the
`mythic_edge_player_log_field_evidence` record shape. Issue #181 must reuse
that shape instead of defining a competing schema.

`src/mythic_edge_parser/app/evidence_ledger.py` already exposes
`validate_field_evidence()`. Issue #181 may build and validate field-evidence
records, but it must not change the field-evidence validator vocabulary or
review-required policy unless a future schema contract authorizes it.

`docs/contracts/player_log_evidence_ledger_invariant_execution.md` and
`src/mythic_edge_parser/app/evidence_invariant_execution.py` remain
authoritative for local invariant execution. Issue #181 may consume an
invariant execution report as optional review evidence, but it must not
reimplement invariant execution or make invariant execution a CI, merge, or
deploy gate.

`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md` and
`docs/contracts/player_log_evidence_ledger_schema_drift_report.md` remain
authoritative for ledger schema snapshots and schema drift reports. Issue #181
may report that those dependencies were supplied or missing, but it must not
update snapshots or change drift-report behavior.

`src/mythic_edge_parser/app/models.py`, `app/state.py`,
`app/sheet_exports.py`, and `app/runtime_surfaces.py` remain parser/runtime
fact and transport surfaces. Issue #181 must observe their existing field names
for mapping only.

## Owning Layer

Owning layer: parser resilience / runtime provenance metadata.

Truth boundary:

- Parser modules, `app/state.py`, and `app/models.py` remain the producers of
  parser-owned facts.
- `app/evidence_ledger.py` remains the owner of ledger vocabulary,
  provenance schema, ledger entries, drift flags, validators, and
  field-evidence record validation.
- The runtime field-evidence layer owns a local sidecar/report that maps
  parser-owned output fields to ledger entries and validated field-evidence
  records.
- The sidecar/report describes provenance metadata only. It must not create,
  correct, overwrite, suppress, enrich, infer, or reconcile parser facts.
- Workbook rows, webhook payloads, Apps Script, output transport,
  `ActionLogRow`, runtime status JSON, diagnostics reports, golden replay
  reports, feature-equity reports, Match Journal, overlay, SQLite, Google
  Sheets sync, analytics, AI, and model-provider output remain downstream or
  out of scope unless a later contract explicitly changes ownership.

The runtime field-evidence layer must not become:

- a parser
- parser state
- parser final reconciliation
- a workbook schema migration
- a webhook payload migration
- an Apps Script migration
- runtime status schema
- diagnostics report schema
- golden replay or feature-equity schema
- Match Journal, overlay, SQLite, or Google Sheets sync schema
- analytics truth, AI truth, or model-provider truth
- CI, merge, deploy, or tracker-completion authority

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`251a17cef4d508a8494aa876f9111016a6402593`:

- Issue #11 is open as the Player.log evidence-ledger and parser-resilience
  tracker.
- Issue #181 is open.
- `src/mythic_edge_parser/app/evidence_ledger.py` exposes:
  - `build_player_log_evidence_ledger()`
  - `iter_ledger_entries()`
  - `validate_player_log_evidence_ledger()`
  - `validate_ledger_entry()`
  - `validate_field_evidence()`
- The field-evidence object is
  `mythic_edge_player_log_field_evidence`.
- The field-evidence schema version is `player_log_field_evidence.v1`.
- The current ledger has 7 output families and 71 seeded entries.
- Ledger vocabulary currently includes:
  - value sources: `observed`, `derived`, `inferred`, `unknown`, `conflict`,
    `legacy_enriched`
  - confidence labels: `high`, `medium`, `low`, `unknown`
  - finality labels: `live`, `provisional`, `final`, `reconciled`
  - invariant statuses: `passed`, `failed`, `not_applicable`,
    `not_checked`, `degraded`
- `validate_field_evidence()` requires `review_required` to be true when:
  - `invariant_status == "failed"`
  - `value_source == "conflict"`
  - `confidence == "low"` and `finality in ("final", "reconciled")`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py` exists and can
  produce a local invariant execution report.
- `src/mythic_edge_parser/app/models.py` produces parser-owned dictionaries
  for debug payloads, history items, match log rows, and game log rows.
- `src/mythic_edge_parser/app/state.py` builds live/final match log rows and
  game log row updates from `MatchSummary`.
- `src/mythic_edge_parser/app/runtime_surfaces.py` writes local runtime
  artifacts such as active match snapshots, match history, timelines, active
  deck profiles, and collection profiles.
- `src/mythic_edge_parser/app/sheet_exports.py` converts local runtime
  artifacts into runtime sheet rows.
- No `src/mythic_edge_parser/app/runtime_field_evidence.py` module exists.
- No `tools/build_runtime_field_evidence_report.py` wrapper exists.
- No focused `tests/test_runtime_field_evidence.py` exists.
- No local sidecar report currently attaches field evidence to parser-owned
  output field references.

## Scope Decision

Codex C should implement a local sidecar/report builder, not embedded runtime
field-evidence in existing artifacts.

V1 should create a new review-only report object that references parser-owned
output fields and attaches validated field-evidence records copied from the
ledger/vocabulary boundary. It should not mutate `MatchSummary`, `GameSummary`,
parser events, row dictionaries, local runtime status, diagnostics reports,
golden replay reports, feature-equity reports, sheet export rows, or transport
payloads.

Reasoning:

- Issue #181 is the first bridge from static ledger metadata into local
  runtime/review artifacts.
- Embedding field evidence into existing runtime artifacts would change those
  artifact shapes and could silently become transport or workbook schema.
- A sidecar report proves the mapping policy and privacy posture without
  changing production behavior.
- Future contracts can decide whether diagnostics, replay, feature-equity,
  runtime status, Match Journal, or overlay surfaces should consume this
  sidecar. Issue #181 should not wire those consumers.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/runtime_field_evidence.py
- tools/build_runtime_field_evidence_report.py
- tests/test_runtime_field_evidence.py
- docs/implementation_handoffs/player_log_evidence_ledger_runtime_field_evidence_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_runtime_field_evidence.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_exports.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_evidence_ledger.py
- tests/test_evidence_invariant_execution.py
- tests/test_app_models.py
- tests/test_state.py
- tests/test_runtime_surfaces.py
- tests/test_sheet_exports.py

## Public Interface

Recommended module:

```python
src/mythic_edge_parser/app/runtime_field_evidence.py
```

Required constants:

```python
RUNTIME_FIELD_EVIDENCE_REPORT_OBJECT = (
    "mythic_edge_player_log_runtime_field_evidence_report"
)
RUNTIME_FIELD_EVIDENCE_REPORT_VERSION = "player_log_runtime_field_evidence_report.v1"
RUNTIME_FIELD_EVIDENCE_ATTACHMENT_OBJECT = (
    "mythic_edge_player_log_runtime_field_evidence_attachment"
)
RUNTIME_FIELD_EVIDENCE_REPORT_STATUSES = ("pass", "review", "fail")
RUNTIME_FIELD_EVIDENCE_ATTACHMENT_SURFACES = (
    "local_review_sidecar",
    "synthetic_test_reference",
)
```

Required public functions:

```python
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def build_runtime_field_evidence_report(
    field_refs: Sequence[Mapping[str, Any]],
    *,
    ledger: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    require_invariant_execution_report: bool = False,
) -> dict[str, Any]:
    ...


def build_current_runtime_field_evidence_report(
    field_refs: Sequence[Mapping[str, Any]],
    *,
    require_invariant_execution_report: bool = False,
) -> dict[str, Any]:
    ...


def write_runtime_field_evidence_report(
    path: Path,
    report: Mapping[str, Any],
) -> None:
    ...


def main(argv: Sequence[str] | None = None) -> int:
    ...
```

Allowed implementation form:

- pure functions returning JSON-serializable dictionaries
- standard-library-only CLI wrapper
- optional internal helpers for entry lookup, field reference normalization,
  privacy scanning, status calculation, and deterministic summary building

Required behavior regardless of implementation form:

- Importing the module must have no filesystem, network, environment, GitHub,
  workbook, webhook, Apps Script, runtime-status, local-log, OpenAI, or model
  provider side effects.
- Builders must be deterministic and must not include volatile timestamps, git
  commit SHAs, branch names, working-tree status, hostnames, local usernames,
  current absolute paths, environment variable values, or raw runtime file
  paths.
- Builders must not include raw Player.log excerpts, raw payload values,
  runtime artifacts, failed posts, workbook exports, secrets, webhook URLs,
  generated data, OpenAI/model-provider output, or AI summaries.
- Malformed caller-provided payloads must produce report status `fail` rather
  than uncaught exceptions.

Recommended CLI/tool wrapper:

```text
tools/build_runtime_field_evidence_report.py
```

Recommended CLI modes:

- `--check`: build a report from an explicit field reference JSON payload and
  print JSON.
- `--field-refs PATH`: consume an explicit local JSON payload containing
  sanitized field references.
- `--ledger PATH`: run against an explicit synthetic JSON ledger payload, for
  local tests only.
- `--invariant-report PATH`: consume an explicit invariant execution report
  JSON.
- `--require-invariant-report`: mark missing or failed invariant report
  dependency as report `fail`.
- `--out PATH`: write JSON report to an explicit local path.
- `--markdown-out PATH`: optionally write a sanitized Markdown summary to an
  explicit local path.

Required CLI exit behavior:

- Return `0` for report status `pass`.
- Return `0` for report status `review`, because this tool is review evidence
  and must not become a CI, merge, or deploy gate by default.
- Return nonzero for report status `fail`.
- Never update committed schema snapshots.
- Never open GitHub issues, update trackers, write runtime status files, or
  post workbook/webhook/App Script updates.

## Allowed Attachment Surfaces

V1 authorizes only these attachment surfaces:

1. `local_review_sidecar`
   - A new local JSON/Markdown review artifact written only to an explicit
     caller-provided path.
   - The artifact contains field references and field-evidence metadata.
   - It does not change an existing runtime artifact shape.

2. `synthetic_test_reference`
   - In-memory or temporary test payloads used by focused unit tests.
   - These references may model match-level, game-level, action-level, and
     report-level fields without reading live logs or private artifacts.

3. `implementation_handoff_summary`
   - Markdown summaries in the implementation handoff or contract-test report.
   - These summaries may list entry IDs, output families, output fields,
     report status, and review guidance.

Allowed field reference categories inside those surfaces:

- match-level parser-owned fields already present in ledger entries
- game-level parser-owned fields already present in ledger entries
- sideboarding/submitted-deck evidence fields already present in ledger entries
- card identity, gameplay-action, and opponent-card-observation seed fields
  already present in ledger entries
- runtime-health/drift fields already present in ledger entries
- Tier 7 report-owned fields already present in ledger entries

Allowed attachment is by reference only. The sidecar may identify a field by
`entry_id`, `output_family`, `output_field`, `display_name`, `surface`, and a
sanitized caller-provided `entity_ref`. It must not include the field's raw
runtime value unless a later contract explicitly authorizes values.

## Forbidden Attachment Surfaces

V1 must not attach field evidence to:

- parser event classes
- parser event payloads
- `MatchSummary`
- `GameSummary`
- `ActionLogRow`
- `MatchLogRow`
- `GameLogRow`
- sheet row dictionaries from `app/sheet_exports.py`
- workbook schema constants
- webhook payloads
- Apps Script payload mappings
- output transport
- local runtime status files
- active match snapshot JSON
- match timeline JSON
- match history JSON
- active deck profile JSON
- collection profile JSON
- diagnostics reports
- golden replay reports
- feature-equity reports
- schema snapshot fixtures
- schema drift reports
- invariant execution reports
- failed posts
- generated card data
- raw local logs
- workbook exports
- Match Journal artifacts
- overlay payloads
- SQLite tables
- Google Sheets sync artifacts
- analytics or AI/model-provider output

Future work may consume runtime field-evidence reports, but it needs a new
contract when that consumption changes any existing artifact shape or user
visible surface.

## Inputs

Allowed inputs:

- The in-memory result of `evidence_ledger.build_player_log_evidence_ledger()`.
- Explicit synthetic caller-provided ledger mappings used by focused tests.
- Optional invariant execution report mappings produced by
  `evidence_invariant_execution.build_current_evidence_invariant_execution_report()`.
- Explicit sanitized field-reference mappings created by tests or local review
  tooling.
- Optional explicit output paths for local JSON or Markdown report artifacts.

Forbidden inputs:

- raw private Player.log files
- sanitized or synthetic fixture log contents
- live local MTGA logs
- runtime status files
- failed posts
- workbook exports
- generated card/tier/cache data
- local runtime artifacts
- live workbook state
- deployed Apps Script state
- webhook URLs
- environment variable values
- secrets, credentials, tokens, API keys
- OpenAI/model-provider output
- AI summaries
- external metagame data

V1 must not read `app/runtime_surfaces.py` output files directly. It may accept
sanitized field references that name fields those surfaces already expose.

## Field Reference Shape

Required caller-provided field reference shape:

```yaml
field_ref:
  surface: "local_review_sidecar"
  output_family: "match_identity_and_lifecycle"
  output_field: "match_id"
  entry_id: "tier1.match_identity.match_id"
  entity_ref:
    entity_type: "match"
    stable_ref: "synthetic-match-1"
    game_number: ""
    action_index: ""
  source_event_kind: "MatchState"
  source_event_type: "match_started"
  source_payload_paths:
    - "payload.match_id"
  source_event_timestamp: ""
  value_source: "observed"
  confidence: "high"
  finality: "live"
  drift_flags: []
  invariant_status: "not_checked"
  degraded_reason: ""
```

Rules:

- `surface` must be one of `RUNTIME_FIELD_EVIDENCE_ATTACHMENT_SURFACES`.
- `entry_id` may be empty only when the caller is intentionally testing
  missing mapping behavior. Missing mappings must not produce a valid
  field-evidence record.
- `entity_ref` must be sanitized. It may contain synthetic IDs, match/game/action
  categories, small integers, or stable symbolic labels. It must not contain
  raw match IDs from private logs, local absolute paths, secrets, raw payload
  values, decklists, card names from private payloads, local usernames, or
  workbook/export paths.
- `source_payload_paths` must use normalized or symbolic paths only.
- The field reference must not include a `value` key. V1 field evidence is
  about provenance metadata, not field-value serialization.

## Output Shape

Required report object:

```yaml
object: "mythic_edge_player_log_runtime_field_evidence_report"
schema_version: "player_log_runtime_field_evidence_report.v1"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/181"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
status: "pass"
review_required: false
status_reasons: []
input_refs:
  ledger:
    object: "mythic_edge_player_log_evidence_ledger"
    schema_version: "player_log_evidence_ledger_schema.v1"
    ledger_version: "player_log_evidence_ledger.v1"
  invariant_execution_report:
    supplied: true
    required: false
    status: "pass"
    schema_version: "player_log_evidence_invariant_execution.v1"
summary:
  field_ref_count: 0
  attachment_count: 0
  valid_field_evidence_count: 0
  missing_mapping_count: 0
  ambiguous_mapping_count: 0
  failed_validation_count: 0
  review_required_count: 0
  conflict_count: 0
  degraded_count: 0
  not_checked_count: 0
  drift_flag_count: 0
  protected_surface_violation_count: 0
attachments:
  - object: "mythic_edge_player_log_runtime_field_evidence_attachment"
    attachment_id: "match_identity_and_lifecycle.match_id.synthetic-match-1"
    surface: "local_review_sidecar"
    entity_ref:
      entity_type: "match"
      stable_ref: "synthetic-match-1"
      game_number: ""
      action_index: ""
    entry_id: "tier1.match_identity.match_id"
    output_family: "match_identity_and_lifecycle"
    output_field: "match_id"
    display_name: "MTGA Match ID"
    parser_owner: "src/mythic_edge_parser/app/state.py"
    model_surface: "MatchSummary.to_match_log_row"
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
    validation_errors: []
    review_notes: []
missing_mappings: []
ambiguous_mappings: []
validation_errors: []
affected:
  output_families: []
  entries: []
review_guidance:
  recommended_review_modules: []
  recommended_tests: []
  review_notes: []
drift_flags: []
privacy:
  forbidden_content_findings: []
  local_absolute_paths_found: []
  raw_private_logs_included: false
  raw_payload_values_included: false
  runtime_artifacts_included: false
  generated_data_included: false
  field_values_included: false
protected_surface_assertions:
  parser_behavior_changed: false
  parser_state_final_reconciliation_changed: false
  parser_event_classes_changed: false
  workbook_schema_changed: false
  webhook_payload_shape_changed: false
  apps_script_behavior_changed: false
  output_transport_changed: false
  action_log_row_shape_changed: false
  runtime_status_schema_changed: false
  diagnostics_report_shape_changed: false
  golden_replay_behavior_changed: false
  feature_equity_behavior_changed: false
  match_journal_behavior_changed: false
  overlay_behavior_changed: false
  sqlite_behavior_changed: false
  google_sheets_sync_behavior_changed: false
  analytics_or_ai_truth_changed: false
limitations: []
```

Field evidence records inside `attachments[].field_evidence` must validate
with `evidence_ledger.validate_field_evidence()`.

## Mapping Policy

Mapping from parser-owned output fields to ledger entries must follow this
order:

1. Exact `entry_id` match.
2. Exact `output_family` plus exact `output_field` match.
3. Exact `output_family` plus exact `display_name` match, only when it resolves
   to one entry.

Forbidden mapping behavior:

- no fuzzy matching
- no workbook header matching as truth
- no dashboard label matching as truth
- no AI/model-provider matching
- no raw payload value inspection
- no runtime artifact file reads
- no mutation of the field reference to make it match
- no automatic creation of missing ledger entries

Missing mapping behavior:

- Do not emit a `field_evidence` record for the missing field.
- Add an item to `missing_mappings`.
- Add `schema_snapshot_missing` or `missing_expected_payload_path` only when
  justified by the field reference context.
- Mark the report `review` for missing optional mappings.
- Mark the report `fail` if the caller explicitly required all supplied field
  references to map.

Ambiguous mapping behavior:

- Do not choose between candidate entries.
- Add an item to `ambiguous_mappings`.
- Mark report `review` or `fail` depending on caller strictness.

## Field Evidence Population Policy

For mapped fields, the builder should populate the required
`mythic_edge_player_log_field_evidence` shape as follows:

- `entry_id`, `output_family`, and `output_field` come from the resolved ledger
  entry.
- `value_source`, `confidence`, `finality`, `drift_flags`,
  `invariant_status`, and `degraded_reason` come from the sanitized field
  reference when supplied and valid.
- Missing `value_source` defaults to `unknown`.
- Missing `confidence` defaults to `unknown`.
- Missing `finality` defaults to `provisional`.
- Missing `drift_flags` defaults to `[]`.
- Missing `invariant_status` defaults to `not_checked`.
- Missing `degraded_reason` defaults to an empty string unless status or drift
  signals require review.
- `source_event_kind`, `source_event_type`, `source_payload_paths`, and
  `source_event_timestamp` come from the sanitized field reference when
  supplied. Missing values default to empty strings or empty lists.
- `review_required` must be computed by the same policy enforced by
  `evidence_ledger.validate_field_evidence()`.

The builder may use ledger evidence-signal defaults only as metadata defaults,
not as proof that the runtime value came from that signal. When no source
evidence is supplied by the caller, `value_source=unknown`,
`confidence=unknown`, and `invariant_status=not_checked` are safer than
pretending direct evidence was observed.

## Confidence, Finality, Degradation, Drift, And Invariants

Value-source policy:

- `observed`: use only when the sanitized field reference identifies a direct
  parser event or source signal that supports the field.
- `derived`: use when the field reference identifies parser-owned model/state
  derivation, aggregate math, classifier output, or report-owned derivation.
- `inferred`: use only for ledger-authorized inference boundaries such as
  later-game play/draw inference, never for hidden information or missing
  Player.log facts.
- `unknown`: use for missing, blank, unmapped, malformed, or unavailable
  support.
- `conflict`: use for contradictory supplied evidence. It must require review.
- `legacy_enriched`: preserve only where the ledger already authorizes legacy
  enriched provenance. Do not create new legacy enrichment semantics.

Confidence policy:

- `high` requires direct observed evidence or ledger-authorized high-confidence
  support supplied by the caller.
- `medium` covers parser-owned fallback, carried-forward, or derived support
  already authorized by the ledger.
- `low` covers weak fallback, lossy inference, degraded dependencies, or
  conflicting support that still maps to a known entry.
- `unknown` covers missing or unmapped support.

Finality policy:

- `live` means the field is still updating during active parsing.
- `provisional` means support exists but is not final or not reconciled.
- `final` means final result/report evidence exists and no later stronger
  correction has been applied.
- `reconciled` means a final value was updated by later stronger evidence.

Invariant-status policy:

- `passed`: use only when the caller supplies invariant evidence for that
  field or report context.
- `failed`: must make `review_required=true` and report status `fail`.
- `not_applicable`: use for fields where the supplied reference has no
  relevant invariant dependency.
- `not_checked`: default when no invariant evidence was supplied.
- `degraded`: use when invariant evidence is incomplete, schema drift report
  review is present, optional dependency evidence is missing under strict
  review, or the report can be produced but should not be trusted as clean.

Drift flags:

- Must use `evidence_ledger.DRIFT_FLAGS` exactly.
- Unknown drift flags must fail validation.
- Drift flags must describe provenance/review state only. They must not drive
  parser value changes.

Review-required policy:

- Must include the existing `validate_field_evidence()` review rules.
- The report must also mark review required when there are missing mappings,
  ambiguous mappings, degraded invariant dependencies, privacy findings,
  protected-surface assertions, failed validation, or caller-required evidence
  that is not supplied.

## Report Status Rules

Report statuses:

- `pass`: all field references map cleanly, all emitted field evidence records
  validate, no attachment requires review, no privacy findings exist, no
  protected-surface assertions are true, and required dependencies are present.
- `review`: no hard failure exists, but one or more attachments or dependencies
  need human review.
- `fail`: input is malformed, privacy findings exist, protected-surface
  assertions are true, required dependencies are missing or failed, field
  evidence validation fails, or report generation cannot be trusted.

Required status mapping:

- Any privacy finding -> report `fail`.
- Any protected-surface assertion true -> report `fail`.
- Any malformed required input -> report `fail`.
- Any invalid field-evidence record -> report `fail`.
- Any field evidence with `invariant_status == "failed"` -> report `fail`.
- Required invariant execution report missing -> report `fail`.
- Supplied invariant execution report status `fail` -> report `fail`.
- Supplied invariant execution report status `review` -> report `review`.
- Missing optional invariant execution report -> report may still be `pass`;
  field evidence should use `invariant_status=not_checked`.
- Missing or ambiguous optional mappings -> report `review`.

## Privacy And Protected-Surface Assertions

The report must preserve the evidence-ledger privacy posture:

- no raw private Player.log excerpts
- no raw payload values
- no local absolute paths
- no local usernames
- no generated card data
- no runtime status files
- no failed posts
- no workbook exports
- no webhook URLs
- no credentials, API keys, tokens, or secrets
- no OpenAI/model-provider output
- no AI summaries

Privacy findings must be path-only. The report may say
`field_refs[0].entity_ref.stable_ref` contained forbidden content; it must not
echo the forbidden value.

Protected-surface assertions in the report must all be false for a clean
implementation. If an implementation touches any protected surface listed in
this contract, the report must fail and Codex C must stop for contract
loopback.

## Error Behavior

- Non-mapping ledger input must produce report `fail`.
- Ledger validation errors must produce report `fail`.
- Non-list or non-sequence field references must produce report `fail`.
- Non-mapping field reference items must produce report `fail`.
- Unknown attachment surface values must produce report `fail`.
- Unknown vocabulary labels must produce report `fail`.
- Unknown drift flags must produce report `fail`.
- Malformed invariant execution report input must produce report `fail` when
  required, or `review` when optional and still usable.
- Missing optional field-reference values should degrade to unknown/not-checked
  metadata, not exceptions.

## Side Effects

Allowed side effects:

- Write a JSON report only to an explicit caller-provided output path.
- Write an optional sanitized Markdown summary only to an explicit
  caller-provided output path.
- Create implementation handoff and contract-test report docs during future
  workflow roles.

Forbidden side effects:

- parser behavior changes
- parser state mutation
- parser event class changes
- parser final reconciliation changes
- row shape changes
- workbook schema changes
- webhook payload changes
- Apps Script changes
- output transport changes
- runtime status writes
- runtime artifact writes
- diagnostics/golden/feature-equity writes
- schema snapshot updates
- schema drift report changes
- invariant execution report changes
- GitHub issue or tracker updates from the module
- network calls
- OpenAI/model-provider calls
- environment variable reads for secrets or provider configuration

## Compatibility

Compatibility requirements:

- Existing evidence-ledger constants and validators must continue to pass.
- Existing invariant execution reports must continue to pass.
- Existing model/state/runtime/sheet tests must not require fixture or
  expectation changes unless Codex C documents a contract-level reason and
  routes back for review.
- Existing local runtime artifacts must preserve their object names and field
  shapes.
- Existing workbook/webhook/App Script surfaces must not see field-evidence
  metadata.
- Existing field evidence schema version remains `player_log_field_evidence.v1`.
- The new report schema version is additive:
  `player_log_runtime_field_evidence_report.v1`.

## Tests Required

Focused Codex C tests should cover:

- Current ledger and a small sanitized field-reference set produce report
  `pass`.
- Report top-level shape and constants match this contract.
- `attachments[].field_evidence` records validate with
  `evidence_ledger.validate_field_evidence()`.
- Exact `entry_id` mapping wins.
- Exact `output_family` + `output_field` mapping works.
- Exact `display_name` mapping works only when unambiguous.
- Missing mapping produces `missing_mappings` and no field-evidence record.
- Ambiguous mapping does not choose a candidate.
- Unknown vocabulary labels fail.
- Unknown drift flags fail.
- `conflict` and low-confidence final/reconciled field evidence require
  review.
- Failed invariant status fails the report.
- Optional missing invariant report does not fail by default.
- Required missing invariant report fails.
- Supplied invariant execution report status `review` degrades report.
- Supplied invariant execution report status `fail` fails report.
- Privacy scanner reports private findings by path only and never echoes raw
  values.
- Writer rejects forbidden private snippets and local absolute paths.
- CLI returns zero for `pass` and `review`, nonzero for `fail`.
- CLI writes only to explicit output paths.
- Tests assert no changes to existing row/runtime/status/diagnostics shapes.

Recommended validation commands for Codex C:

```bash
py -m pytest -q tests/test_runtime_field_evidence.py tests/test_evidence_ledger.py tests/test_evidence_invariant_execution.py
py -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
py -m ruff check src tests tools
git diff --check
```

Codex E should rerun at least:

```bash
py -m pytest -q tests/test_runtime_field_evidence.py tests/test_evidence_ledger.py tests/test_evidence_invariant_execution.py
py -m pytest -q tests/test_runtime_surfaces.py tests/test_sheet_exports.py
py -m ruff check src tests tools
git diff --check
```

Codex F/G should use the workflow's normal changed-file, protected-surface,
tests, PR, merge, close, and tracker-update gates. Passing this report is not
merge readiness by itself.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
  exists and routes implementation to Codex C.
- The contract authorizes a local sidecar/report only.
- The contract forbids embedding field evidence into parser events, models,
  rows, runtime status, diagnostics, replay, feature-equity, workbook,
  webhook, Apps Script, Match Journal, overlay, SQLite, Sheets sync,
  analytics, AI, and model-provider surfaces.
- The contract reuses `mythic_edge_player_log_field_evidence` records and
  `evidence_ledger.validate_field_evidence()`.
- The contract defines deterministic mapping, missing/ambiguous mapping,
  privacy, degradation, invariant, and protected-surface behavior.
- The contract lists focused validation and workflow handoff requirements.

## Unknowns And Suspected Gaps

- It is unknown whether future diagnostics, golden replay, or feature-equity
  reports should consume runtime field-evidence reports directly. V1 defers
  that wiring.
- It is unknown whether runtime status should ever expose field-evidence
  counts. V1 forbids runtime status schema changes.
- It is unknown whether Match Journal or overlay review views should read the
  sidecar. V1 forbids those integrations.
- Some ledger entries represent broad seed fields with many facets, especially
  Tier 5 and Tier 7. V1 should attach only to the seeded ledger entry, not
  create facet-level entries.
- Existing ledger evidence can describe expected provenance, but runtime field
  references must not pretend a direct signal was observed unless the caller
  supplies that sanitized context.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #181, runtime field-evidence attachment boundary, under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/181
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/179
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/180
- Previous merge commit: 251a17cef4d508a8494aa876f9111016a6402593
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_runtime_field_evidence_comparison.md

Goal:
Implement the smallest local sidecar/report module that attaches validated Player.log evidence-ledger field evidence to sanitized parser-owned output field references without changing parser behavior or downstream workbook/webhook/App Script/runtime surfaces.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_invariant_execution.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/evidence_invariant_execution.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_evidence_ledger.py
- tests/test_evidence_invariant_execution.py

Implement:
- src/mythic_edge_parser/app/runtime_field_evidence.py
- tools/build_runtime_field_evidence_report.py
- tests/test_runtime_field_evidence.py
- docs/implementation_handoffs/player_log_evidence_ledger_runtime_field_evidence_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_runtime_field_evidence.md if the workflow expects a test report

Required behavior:
- Build a local review-only runtime field-evidence report.
- Reuse evidence_ledger.FIELD_EVIDENCE_OBJECT, FIELD_EVIDENCE_SCHEMA_VERSION, LEDGER_VERSION, vocabulary constants, and validate_field_evidence().
- Map field references by exact entry_id, then exact output_family/output_field, then unambiguous output_family/display_name.
- Emit field_evidence records only for mapped fields.
- Report missing and ambiguous mappings without guessing.
- Preserve privacy by omitting raw values, raw private logs, runtime artifacts, local absolute paths, secrets, generated data, workbook exports, webhook URLs, and model-provider/AI output.
- Keep imports/builders deterministic and side-effect free except explicit report writes.
- CLI returns 0 for pass/review and nonzero for fail.

Do not:
- Change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, runtime status schema, diagnostics report shape, golden replay behavior, feature-equity behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, or deploy policy.
- Attach field evidence to MatchSummary, GameSummary, ActionLogRow, MatchLogRow, GameLogRow, sheet export rows, runtime status files, active match snapshots, match timelines, match history, diagnostics reports, golden replay reports, feature-equity reports, workbook exports, webhooks, Apps Script, Match Journal, overlay, SQLite, Google Sheets sync, analytics, AI, or model-provider output.
- Read raw private Player.log excerpts, raw local logs, generated data, runtime status files, failed posts, workbook exports, secrets, credentials, tokens, API keys, or webhook URLs.
- Target main directly.
- Close tracker #11.
- Stage or commit unless explicitly asked.

Validation:
- py -m pytest -q tests/test_runtime_field_evidence.py tests/test_evidence_ledger.py tests/test_evidence_invariant_execution.py
- py -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
- py -m ruff check src tests tools
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/181"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_runtime_field_evidence_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-runtime-field-evidence"
  validation:
    - "git diff --check"
    - "Documentation-only contract pass; focused tests deferred to Codex C."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, runtime status schema, diagnostics report shape, golden replay behavior, feature-equity behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, or deploy policy."
    - "Do not attach field evidence to existing parser, row, runtime, diagnostics, replay, feature-equity, workbook, webhook, Apps Script, Match Journal, overlay, SQLite, Google Sheets sync, analytics, AI, or model-provider surfaces without a new explicit contract."
    - "Do not commit raw private Player.log excerpts, raw local logs, generated data, runtime status files, failed posts, workbook exports, secrets, credentials, tokens, API keys, or webhook URLs."
```
