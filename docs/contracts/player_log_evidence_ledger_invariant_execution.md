# Player.log Evidence Ledger Invariant Execution Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/179
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/177
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/178
- previous_merge_commit: 452a857e654ec63cdbff5472c6994ba3c8c8942f
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-invariant-execution
- target_artifact: docs/contracts/player_log_evidence_ledger_invariant_execution.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md
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
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- docs/contract_test_reports/player_log_evidence_ledger_schema_drift_report.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #179 defines the next narrow Player.log evidence-ledger resilience layer:
a deterministic local invariant execution surface.

The evidence ledger now has seeded Tier 1-7 provenance, a deterministic schema
snapshot builder, and a schema drift report. The next useful layer is a local
report that checks whether the ledger's invariant metadata is structurally
healthy and whether adjacent schema-drift evidence makes invariant review
degraded or untrustworthy.

This report should answer:

> Are the evidence-ledger invariant declarations and metadata review surfaces
> structurally healthy enough for local review, and what should a reviewer
> inspect when they are not?

It must not answer:

- whether parser behavior is semantically correct
- whether every declared gameplay/domain invariant is proven true
- whether a PR is ready to merge
- whether a deployment is ready
- whether a tracker can close
- whether a snapshot update is approved
- whether live Arena logs have or have not drifted
- whether workbook, webhook, Apps Script, runtime, analytics, AI, or model
  provider behavior is correct

Plain English: this executor can check the scaffolding and produce review
evidence. It cannot prove the match facts are right.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger.md` sketched future invariant
checks. Issue #179 implements only the first local invariant execution surface.

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative
for the evidence-ledger object, vocabulary, validators, field-evidence shape,
and privacy posture.

`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
remains authoritative for deterministic snapshot projection and comparison.
Issue #179 must not update the expected snapshot.

`docs/contracts/player_log_evidence_ledger_schema_drift_report.md` remains
authoritative for schema drift review guidance. The invariant executor may
consume its report as input evidence, but must not reimplement schema drift
comparison or change schema drift report behavior.

`src/mythic_edge_parser/app/parser_diagnostics.py`,
`src/mythic_edge_parser/app/log_drift_sensor.py`,
`src/mythic_edge_parser/app/golden_replay.py`, and
`src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` remain separate
runtime or validation reporting surfaces. Issue #179 must not wire invariant
results into them.

## Owning Layer

Owning layer: parser resilience / evidence-ledger invariant review metadata.

Truth boundary:

- `src/mythic_edge_parser/app/evidence_ledger.py` owns ledger entries,
  invariant names, drift flags, vocabulary, validators, and copy-safe ledger
  serialization.
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py` owns deterministic
  evidence-ledger schema snapshots and snapshot comparison.
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py` owns schema
  drift review guidance.
- The new invariant execution layer owns deterministic local invariant results
  over ledger/snapshot/report metadata.
- Parser modules and parser state remain truth producers for match facts, game
  facts, event interpretation, identity, final reconciliation, and
  parser-owned classifications.
- Runtime diagnostics, golden replay, feature-equity reports, workbook
  exports, webhooks, Apps Script, Match Journal, overlay, SQLite, analytics,
  AI, and model-provider output remain downstream or out of scope unless a
  later contract explicitly changes ownership.

The invariant executor must not become:

- a parser
- a semantic gameplay correctness proof
- a ledger authoring surface
- a schema snapshot updater
- a schema drift report replacement
- a live Player.log scanner
- a diagnostics or runtime status writer
- a workbook/App Script validator
- a CI, merge, or deploy gate
- an automatic GitHub issue or tracker updater
- an AI or analytics truth source

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`452a857e654ec63cdbff5472c6994ba3c8c8942f`:

- Issue #11 is open as the Player.log evidence-ledger and parser-resilience
  tracker.
- Issue #179 is open.
- `src/mythic_edge_parser/app/evidence_ledger.py` exposes:
  - `build_player_log_evidence_ledger()`
  - `iter_ledger_entries()`
  - `validate_player_log_evidence_ledger()`
  - `validate_ledger_entry()`
  - `validate_field_evidence()`
- The ledger vocabulary includes invariant statuses exactly:
  `passed`, `failed`, `not_applicable`, `not_checked`, `degraded`.
- The ledger has 7 output families, 71 entries, 448 evidence signals, 425
  declared invariant references, and 394 unique invariant names.
- Every current ledger entry declares at least one invariant.
- No current ledger entry has duplicate invariant names within the same entry.
- Some invariant names are intentionally shared across entries; global reuse is
  not an error.
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py` exists and the
  committed expected snapshot currently matches the generated current snapshot.
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py` exists and
  `tools/build_evidence_schema_drift_report.py --check` currently returns a
  `pass` report with no drift flags.
- No `src/mythic_edge_parser/app/evidence_invariant_execution.py` module
  exists.
- No `tools/run_evidence_invariants.py` wrapper exists.
- No focused `tests/test_evidence_invariant_execution.py` exists.
- No invariant execution report artifact is currently committed or generated
  by default.

## Scope Decision

Codex C should implement a metadata invariant executor, not a semantic
gameplay invariant engine.

V1 must execute a small registry of deterministic invariants over the ledger,
schema snapshot/drift report metadata, and optional synthetic caller-provided
ledger payloads used by tests. It must inventory the domain invariant names
declared in ledger entries, but it must not attempt to prove every declared
domain invariant such as winner precedence, play/draw correctness, mulligan
truth, deck-state boundaries, gameplay-action extraction, card identity, or
derived analytics correctness.

Reasoning:

- The current ledger's `invariant_checks` values are durable declarations and
  review anchors.
- Most declared names describe parser behavior boundaries that require parser
  event fixtures or runtime facts to prove.
- Executing those semantic checks in this issue would silently expand scope
  into parser behavior, runtime field evidence, fixture replay, diagnostics,
  or CI policy.
- A metadata executor is still useful because it can catch broken invariant
  declarations, missing review targets, malformed ledger structure, privacy
  leaks, schema-drift dependencies, and report-shape regressions.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_invariant_execution.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_invariant_execution.py
- tools/run_evidence_invariants.py
- tests/test_evidence_invariant_execution.py
- docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_invariant_execution.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- tools/build_evidence_schema_snapshot.py
- tools/build_evidence_schema_drift_report.py
- tests/test_evidence_ledger.py
- tests/test_evidence_schema_snapshot.py
- tests/test_evidence_schema_drift_report.py
- tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py

## Public Interface

Recommended module:

```python
src/mythic_edge_parser/app/evidence_invariant_execution.py
```

Required constants:

```python
EVIDENCE_INVARIANT_EXECUTION_REPORT_OBJECT = (
    "mythic_edge_player_log_evidence_invariant_execution_report"
)
EVIDENCE_INVARIANT_EXECUTION_REPORT_VERSION = "player_log_evidence_invariant_execution.v1"
EVIDENCE_INVARIANT_EXECUTION_REPORT_STATUSES = ("pass", "review", "fail")
EXECUTABLE_INVARIANT_IDS = (
    "ledger_validates_cleanly",
    "ledger_privacy_contract_holds",
    "invariant_status_vocabulary_matches_ledger",
    "entries_declare_invariant_checks",
    "entry_invariant_names_are_stable",
    "entry_invariant_names_are_unique_within_entry",
    "entries_with_invariants_have_review_modules",
    "entries_with_invariants_have_tests",
    "declared_invariant_inventory_is_deterministic",
    "schema_drift_report_is_usable_review_evidence",
    "schema_drift_report_protected_surface_assertions_hold",
)
```

Required public functions:

```python
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def build_evidence_invariant_execution_report(
    ledger: Mapping[str, Any] | None = None,
    *,
    schema_drift_report: Mapping[str, Any] | None = None,
    require_schema_drift_report: bool = False,
) -> dict[str, Any]:
    ...


def build_current_evidence_invariant_execution_report(
    *,
    expected_snapshot_path: Path | None = None,
    require_schema_drift_report: bool = True,
) -> dict[str, Any]:
    ...


def write_evidence_invariant_execution_report(
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
- optional internal helpers for invariant execution, inventory building,
  privacy scanning, and review guidance

Required behavior regardless of implementation form:

- Importing the module must have no filesystem, network, environment, GitHub,
  workbook, webhook, Apps Script, runtime-status, local-log, OpenAI, or model
  provider side effects.
- Builders must be deterministic and must not include volatile timestamps, git
  commit SHAs, branch names, working-tree status, hostnames, local usernames,
  current absolute paths, or environment variable values.
- Builders must not include raw Player.log excerpts, raw payload values,
  runtime artifacts, failed posts, workbook exports, secrets, webhook URLs,
  generated data, OpenAI/model-provider output, or AI summaries.
- Malformed caller-provided payloads must produce report status `fail` rather
  than uncaught exceptions.

Recommended CLI/tool wrapper:

```text
tools/run_evidence_invariants.py
```

Recommended CLI modes:

- `--check`: build the current ledger, build the current schema drift report,
  run invariant metadata checks, and print JSON.
- `--ledger PATH`: run against an explicit JSON ledger payload, for local
  synthetic testing only.
- `--schema-drift-report PATH`: consume an explicit schema drift report JSON.
- `--expected PATH`: expected schema snapshot path to pass through when
  building the current schema drift report.
- `--no-schema-drift-report`: run ledger-only checks and mark the schema-drift
  dependency invariant as `not_checked`.
- `--out PATH`: write the JSON report to an explicit local path.
- `--markdown-out PATH`: optionally write a sanitized Markdown summary to an
  explicit local path.

Required CLI exit behavior:

- Return `0` for report status `pass`.
- Return `0` for report status `review`, because this tool is review evidence
  and must not become a CI, merge, or deploy gate by default.
- Return nonzero for report status `fail`.
- Never update the committed expected snapshot.
- Never set or require `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT`.
- Never open GitHub issues, update trackers, or write runtime status files.

## Inputs

Allowed inputs:

- The in-memory result of `evidence_ledger.build_player_log_evidence_ledger()`.
- Explicit synthetic caller-provided ledger mappings used by focused tests.
- The in-memory result of
  `evidence_schema_drift_report.build_current_evidence_schema_drift_report()`.
- Explicit schema drift report JSON produced by
  `tools/build_evidence_schema_drift_report.py`.
- Optional explicit expected snapshot JSON path under
  `tests/fixtures/evidence_schema_snapshots/`, passed through only to the
  schema drift report builder.
- Optional explicit local report output paths.

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

V1 must not read golden replay manifests, feature-equity reports, parser
diagnostics reports, log drift reports, runtime status files, workbook exports,
or Player.log files directly.

## Output Shape

Required report object:

```yaml
object: "mythic_edge_player_log_evidence_invariant_execution_report"
schema_version: "player_log_evidence_invariant_execution.v1"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/179"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
status: "pass"
review_required: false
status_reasons: []
input_refs:
  ledger:
    object: "mythic_edge_player_log_evidence_ledger"
    schema_version: "player_log_evidence_ledger_schema.v1"
    ledger_version: "player_log_evidence_ledger.v1"
    source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
    parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  schema_drift_report:
    supplied: true
    status: "pass"
    schema_version: "player_log_evidence_schema_drift_report.v1"
    expected_snapshot_id: "sha256:..."
    current_snapshot_id: "sha256:..."
summary:
  executable_invariant_count: 0
  declared_invariant_total_count: 0
  declared_invariant_unique_count: 0
  passed_count: 0
  failed_count: 0
  degraded_count: 0
  not_applicable_count: 0
  not_checked_count: 0
  affected_entry_count: 0
  affected_output_family_count: 0
  drift_flag_count: 0
declared_invariants:
  total_count: 0
  unique_count: 0
  shared_name_count: 0
  entries_without_invariants: []
  duplicate_names_within_entries: []
  invalid_names: []
  by_output_family: {}
invariant_results:
  - invariant_id: "ledger_validates_cleanly"
    status: "passed"
    scope: "ledger"
    entry_id: ""
    output_family: ""
    review_required: false
    drift_flags: []
    reason: ""
    evidence_refs:
      - "evidence_ledger.validate_player_log_evidence_ledger"
    recommended_review_modules:
      - "src/mythic_edge_parser/app/evidence_ledger.py"
    recommended_tests:
      - "tests/test_evidence_ledger.py"
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
  local_absolute_paths_included: false
  runtime_artifacts_included: false
  generated_data_included: false
protected_surface_assertions:
  parser_behavior_changed: false
  parser_state_final_reconciliation_changed: false
  parser_event_classes_changed: false
  router_semantics_changed: false
  diagnostics_report_shape_changed: false
  runtime_status_schema_changed: false
  log_drift_report_behavior_changed: false
  schema_snapshot_update_policy_changed: false
  schema_drift_report_behavior_changed: false
  golden_replay_behavior_changed: false
  feature_equity_behavior_changed: false
  workbook_schema_changed: false
  webhook_payload_shape_changed: false
  apps_script_behavior_changed: false
  output_transport_changed: false
  analytics_or_ai_truth_changed: false
limitations: []
```

## Report Status Rules

Report status values:

- `pass`: all required executable invariant results are `passed` or
  `not_applicable`, no privacy findings exist, no required dependency is
  missing, and no malformed input was found.
- `review`: no invariant result is `failed`, but one or more results are
  `degraded` or optional results are `not_checked` under a mode that requests
  review for missing optional evidence.
- `fail`: one or more executable invariant results are `failed`, input is
  malformed, privacy/forbidden content is detected, a required dependency is
  missing or untrustworthy, or the report cannot be produced trustworthily.

Invariant result status values must use
`evidence_ledger.INVARIANT_STATUSES` exactly:

- `passed`
- `failed`
- `not_applicable`
- `not_checked`
- `degraded`

Required mapping:

- Any `failed` invariant result -> report `fail`.
- Any privacy finding -> report `fail`.
- Any malformed required input -> report `fail`.
- Required schema drift report missing -> report `fail`.
- Supplied schema drift report status `fail` -> invariant result `failed`,
  report `fail`.
- Supplied schema drift report status `review` -> invariant result
  `degraded`, report `review`.
- Supplied schema drift report status `pass` -> invariant result `passed`.
- Schema drift report not supplied and not required -> invariant result
  `not_checked`, report may still be `pass` if all required metadata
  invariants pass.

`review_required` must be true when report status is `review` or `fail`.
Individual invariant results should set `review_required` true for `failed` and
`degraded` statuses. `not_checked` should set `review_required` true only when
the caller required that check.

## Executable Invariants

V1 must execute only the metadata invariants below.

### `ledger_validates_cleanly`

Run `evidence_ledger.validate_player_log_evidence_ledger()` against the input
ledger.

- `passed`: validator returns no errors.
- `failed`: validator returns errors or input is not a mapping.
- Drift flags on failure: `invariant_failed`.
- Review targets:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`

### `ledger_privacy_contract_holds`

Scan ledger/report inputs for forbidden/private snippets and local absolute
paths.

- `passed`: no privacy findings.
- `failed`: privacy findings exist.
- Drift flags on failure: `sensitive_evidence_redacted`, `invariant_failed`.
- Findings must list paths only, not values.

### `invariant_status_vocabulary_matches_ledger`

Check that the ledger vocabulary's `invariant_statuses` exactly matches
`evidence_ledger.INVARIANT_STATUSES`.

- `passed`: exact match.
- `failed`: missing, reordered, unknown, or extra status labels.
- Drift flags on failure: `changed_signal_type`, `invariant_failed`.

### `entries_declare_invariant_checks`

Every seeded ledger entry must have a non-empty `invariant_checks` list.

- `passed`: all entries have non-empty lists.
- `failed`: any seeded entry is missing invariant checks.
- Drift flags on failure: `invariant_failed`.

### `entry_invariant_names_are_stable`

Every declared invariant name must be a non-empty string matching
`^[a-z0-9_]+$`.

- `passed`: all declared names are stable snake-case identifiers.
- `failed`: any name is blank, non-string, path-like, or contains other
  characters.
- Drift flags on failure: `invariant_failed`.

### `entry_invariant_names_are_unique_within_entry`

Each ledger entry must not repeat the same invariant name in its own
`invariant_checks` list.

- `passed`: no within-entry duplicates.
- `failed`: one or more entries repeat an invariant name.
- Drift flags on failure: `invariant_failed`.
- Global reuse across different entries is allowed and should be summarized in
  `declared_invariants.shared_name_count`.

### `entries_with_invariants_have_review_modules`

Every entry with declared invariants should provide at least one
`recommended_review_modules` value.

- `passed`: all entries with invariants have review modules.
- `degraded`: one or more entries lack review modules but the ledger otherwise
  validates.
- `failed`: malformed values prevent review guidance from being built.
- Drift flags on degraded/failed: `invariant_failed` only when failed.

### `entries_with_invariants_have_tests`

Every entry with declared invariants should provide at least one `tests` value.

- `passed`: all entries with invariants have tests.
- `degraded`: one or more entries lack tests but the ledger otherwise
  validates.
- `failed`: malformed values prevent review guidance from being built.
- Drift flags on degraded/failed: `invariant_failed` only when failed.

### `declared_invariant_inventory_is_deterministic`

Build a deterministic inventory of declared invariant names by output family,
entry, duplicate-within-entry status, and shared-name status.

- `passed`: inventory can be built deterministically.
- `failed`: inventory cannot be built due to malformed entries.
- Drift flags on failure: `invariant_failed`.

The inventory is a review aid. It is not proof that each declared domain
invariant is semantically true.

### `schema_drift_report_is_usable_review_evidence`

If a schema drift report is supplied or required, inspect its status and
summary.

- `passed`: schema drift report status is `pass`.
- `degraded`: schema drift report status is `review`.
- `failed`: schema drift report status is `fail`, unknown, malformed, or
  missing when required.
- `not_checked`: schema drift report is not supplied and not required.

This invariant may copy schema-drift report drift flags into the invariant
execution report, but it must not update snapshots or re-run snapshot
comparison itself.

### `schema_drift_report_protected_surface_assertions_hold`

If a schema drift report is supplied, inspect its
`protected_surface_assertions`.

- `passed`: all known protected-surface assertion values are `false`.
- `failed`: any protected-surface assertion is `true` or malformed.
- `not_checked`: schema drift report is not supplied and not required.
- Drift flags on failure: `invariant_failed`.

## Declared Invariant Name Policy

V1 must not require a global whitelist for the hundreds of domain invariant
names declared in ledger entries. A syntactically valid name in a ledger entry
is a declared invariant name.

Invalid declared names:

- non-string values
- blank strings
- path-like values
- values containing spaces, punctuation other than `_`, or uppercase letters
- values containing forbidden/private snippets

Duplicate policy:

- Duplicate names within the same ledger entry are failures.
- Duplicate names shared across different entries are allowed and should be
  counted as shared names in the inventory.

Unsupported semantic invariant policy:

- V1 does not execute semantic domain invariant names.
- The report should not create one `not_checked` result per declared semantic
  invariant because that would make every healthy ledger look degraded.
- Future issues may add executable semantic invariant registries, but each
  registry must name its evidence sources and protected-surface boundaries in
  a new contract.

## Review Guidance

The executor must produce deterministic review guidance:

- For ledger validation failures, recommend:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`
- For schema drift report degraded or failed input, include review modules and
  tests from the schema drift report's `review_guidance` when present.
- For affected entries, include each entry's `recommended_review_modules` and
  `tests`.
- If affected entries cannot be resolved, fall back to:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
  - `tests/test_evidence_ledger.py`
  - `tests/test_evidence_schema_drift_report.py`
- Do not generate GitHub issue titles, update trackers, create PRs, or suggest
  snapshot updates as automatic actions.

## Drift Flags

Allowed drift-flag behavior:

- Failed invariant results must add `invariant_failed`.
- Privacy findings must add `sensitive_evidence_redacted`.
- Malformed or missing required schema drift report evidence may add
  `schema_snapshot_missing`.
- Schema drift report input flags may be copied through when they already use
  approved `evidence_ledger.DRIFT_FLAGS`.
- Unknown drift flags from caller-provided inputs must be dropped or reported
  as malformed without echoing private values.

Issue #179 must not add new drift flag vocabulary.

## Privacy And Sanitization

Required privacy posture:

- The report must never include raw private Player.log excerpts.
- The report must never include raw payload values.
- The report must never include webhook URLs, API keys, tokens, credentials,
  secrets, local absolute paths, runtime status contents, failed post contents,
  workbook exports, generated card data, OpenAI/model-provider output, or AI
  summaries.
- Privacy findings may identify paths such as
  `ledger.entries[0].parser_owner` but must not reproduce the offending value.
- Markdown output, if implemented, must follow the same redaction and path-only
  rules as JSON output.
- Writing a report to an explicit local path must scan the report for
  forbidden/private snippets before writing.

Forbidden snippets and patterns should stay aligned with the snapshot and
schema drift report builders, including:

- `[UnityCrossThreadLogger]`
- `[Client GRE]`
- `DETAILED LOGS:`
- `script.google.com/macros/`
- webhook URLs
- bearer tokens
- `api_key`
- `secret`
- `token`
- `/Users/`
- `C:\Users\`
- `data/runtime_logs/`
- `data/failed_posts/`
- `data/status/`
- `data/generated/`

## Error Behavior

Malformed ledger input:

- Report status must be `fail`.
- `ledger_validates_cleanly` must be `failed`.
- Validation errors should be listed as stable strings or sanitized reason
  codes.
- The executor must not raise uncaught exceptions for caller-provided mappings.

Malformed schema drift report input:

- If schema drift report is required, report status must be `fail`.
- If schema drift report is optional, the dependency result may be
  `not_checked` or `failed` depending on whether malformed input was supplied.
- The executor must not re-run or repair schema drift report behavior.

Schema drift report status `review`:

- Invariant execution report status should be `review`, not `fail`, unless
  additional invariant failures exist.
- The result reason should state that schema drift review is required before
  approving any snapshot update.

Unknown or malformed invariant names:

- Report status must be `fail`.
- Affected entries should be listed.
- The report must not echo private values.

Missing review modules or tests:

- The relevant invariant result should be `degraded` when the ledger otherwise
  validates.
- Report status should be `review`.

Contract ambiguity:

- If Codex C cannot decide whether a check is metadata-only or semantic, it
  should leave that check out, document the omission in the implementation
  handoff, and route back to Codex B if the omission blocks useful review.

## Side Effects

Allowed for Codex C:

- Add `src/mythic_edge_parser/app/evidence_invariant_execution.py`.
- Add `tools/run_evidence_invariants.py`.
- Add `tests/test_evidence_invariant_execution.py`.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md`.
- Optionally produce a local uncommitted report by explicit `--out` or
  `--markdown-out` path while validating manually.

Forbidden for Codex C:

- Changing evidence-ledger entries, vocabulary, invariant names, or the
  committed expected snapshot unless a separate contract/review loop explicitly
  authorizes it.
- Updating
  `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`.
- Changing parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics report shape, runtime status schema,
  log drift report behavior, schema snapshot update policy, schema drift
  report behavior, golden replay behavior, feature-equity behavior,
  card-performance calculations, workbook schema, webhook payload shape, Apps
  Script behavior, output transport, ActionLogRow shape, match/game identity,
  deduplication, Match Journal behavior, overlay behavior, SQLite behavior,
  Google Sheets sync behavior, production behavior, analytics truth, AI truth,
  OpenAI/model-provider behavior, CI gates, merge policy, deploy policy,
  secrets, environment variables, raw logs, generated data, runtime status
  files, failed posts, workbook exports, or local runtime artifacts.
- Adding runtime field-evidence attachment.
- Adding semantic gameplay invariant execution.
- Wiring invariant reports into diagnostics, golden replay, feature-equity,
  log drift sensor, runtime status, workbook export, webhook delivery, or CI.
- Adding automatic GitHub issue or tracker updates.
- Reading, copying, summarizing, or committing raw private logs or local
  artifacts.

## Dependency Order

Implementation should proceed in this order:

1. Add a pure invariant execution report builder over a supplied ledger and
   optional schema drift report.
2. Add deterministic declared-invariant inventory helpers.
3. Add the V1 executable metadata invariant registry.
4. Add privacy scanning for inputs and output.
5. Add a CLI wrapper that builds the current ledger and current schema drift
   report without writing by default.
6. Add focused tests for pass, review, fail, malformed input, privacy,
   duplicate names, invalid names, schema-drift dependency handling, CLI exit
   behavior, explicit output writes, and no snapshot update behavior.
7. Produce the implementation handoff.

Do not edit the evidence ledger, snapshot builder, or schema drift report
unless a focused implementation issue proves that a tiny compatibility helper
is required. If such a helper changes public behavior, route back to Codex B
first.

## Compatibility

The invariant executor must remain compatible with:

- `evidence_ledger.build_player_log_evidence_ledger()`
- `evidence_ledger.validate_player_log_evidence_ledger()`
- `evidence_ledger.validate_ledger_entry()`
- `evidence_ledger.validate_field_evidence()`
- `evidence_schema_drift_report.build_current_evidence_schema_drift_report()`
- `tools/build_evidence_schema_drift_report.py --check`

The executor must not rename existing invariant status vocabulary or drift
flags. It may summarize them into its report shape.

The executor must not require a committed report fixture. Focused tests should
use synthetic in-memory ledgers and temporary output paths.

The executor must not require global uniqueness of invariant names across all
ledger entries.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_invariant_execution.py` should prove:

- Current ledger plus current schema drift report produces report status
  `pass`.
- Report shape includes required top-level sections and protected-surface
  assertions.
- The report uses `evidence_ledger.INVARIANT_STATUSES` exactly.
- The report inventories declared invariant total count, unique count, shared
  name count, entries without invariants, duplicate names within entries, and
  invalid names.
- Non-mapping ledger input produces report status `fail` without uncaught
  exceptions.
- Ledger validation errors produce `ledger_validates_cleanly` status `failed`
  and add `invariant_failed`.
- Missing invariant lists or empty invariant lists on seeded entries fail.
- Non-string, blank, uppercase, path-like, or punctuation-containing invariant
  names fail without echoing private values.
- Duplicate invariant names within one entry fail.
- Duplicate invariant names shared across different entries are allowed and
  counted as shared names.
- Missing recommended review modules degrades the relevant invariant and
  produces report status `review`.
- Missing tests degrades the relevant invariant and produces report status
  `review`.
- Schema drift report status `review` degrades invariant execution and
  produces report status `review`.
- Schema drift report status `fail` fails invariant execution.
- Schema drift report protected-surface assertion values set to `true` fail.
- Optional missing schema drift report is `not_checked` when not required.
- Required missing schema drift report fails.
- Privacy findings are path-only and never echo private values.
- Writing a report rejects forbidden/private/volatile snippets.
- CLI `--check` returns `0` for `pass` and `review`, nonzero for `fail`.
- CLI `--out` writes only to an explicit path.
- CLI does not update the expected snapshot and does not require or set
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT`.

Focused existing tests should continue to pass:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 -m pytest -q tests/test_evidence_schema_drift_report.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
```

Recommended validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_invariant_execution.py
python3 tools/run_evidence_invariants.py --check
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 -m pytest -q tests/test_evidence_schema_drift_report.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
```

Protected-surface validation when available:

```bash
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_invariant_execution.md \
  src/mythic_edge_parser/app/evidence_invariant_execution.py \
  tools/run_evidence_invariants.py \
  tests/test_evidence_invariant_execution.py \
  docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_invariant_execution.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_invariant_execution.md` exists.
- The contract defines a local metadata invariant executor over the
  evidence-ledger registry and optional schema drift report metadata.
- The contract distinguishes executable metadata invariants from declared
  semantic/domain invariant names.
- The contract defines report shape, status mapping, privacy rules, protected
  surfaces, validation expectations, and Codex C handoff.
- The contract authorizes only report-builder code, optional CLI wrapper,
  focused tests, and implementation handoff docs.
- The contract forbids committed report artifacts by default.
- The contract forbids snapshot baseline updates.
- The contract keeps invariant execution as review evidence only, not parser
  truth, CI truth, merge readiness, deploy readiness, tracker completion, or
  automatic drift approval.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- A future issue may add executable semantic invariant registries for specific
  parser surfaces. Each registry must name its fixtures, evidence sources,
  expected result fields, and protected-surface boundaries.
- A future issue may wire invariant reports into diagnostics, golden replay,
  feature-equity, runtime status, or CI. Issue #179 does not authorize that
  integration.
- A future issue may define field-evidence runtime attachment and use invariant
  results per parser output. Issue #179 keeps field-evidence attachment out of
  scope.
- A future issue may decide whether Markdown reports are worth standardizing.
  JSON is the required durable shape for issue #179.

## Suspected Gaps

- No `src/mythic_edge_parser/app/evidence_invariant_execution.py` module
  exists.
- No `tools/run_evidence_invariants.py` wrapper exists.
- No `tests/test_evidence_invariant_execution.py` exists.
- The existing ledger validates invariant names as lists only; it does not yet
  run invariant metadata checks or build a declared invariant inventory report.
- Current schema drift reports are review guidance only and do not include
  invariant execution results.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #179, the Player.log evidence-ledger invariant execution report under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/179
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/177
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/178
- Previous merge commit: 452a857e654ec63cdbff5472c6994ba3c8c8942f
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_invariant_execution.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md

Goal:
Compare the current evidence-ledger, schema snapshot, schema drift report, and focused tests against the invariant execution contract. Implement only the smallest coherent local metadata invariant report builder, optional CLI wrapper, focused tests, and implementation handoff needed to satisfy the contract.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Add a pure invariant execution report builder, preferably at src/mythic_edge_parser/app/evidence_invariant_execution.py.
- Execute only the V1 metadata invariants defined in the contract.
- Inventory declared ledger invariant names, but do not attempt to prove every semantic/domain invariant.
- Consume evidence_ledger validators and, when required, the existing schema drift report builder.
- Add a local tool wrapper, preferably tools/run_evidence_invariants.py.
- Add focused tests, preferably tests/test_evidence_invariant_execution.py.
- Keep CLI review status advisory: --check should return 0 for pass and review, and nonzero only for fail.
- Preserve privacy: report finding paths and counts only, never raw private values, raw payload values, logs, local absolute paths, secrets, webhook URLs, runtime artifacts, workbook exports, generated data, or AI/model-provider output.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not implement parser behavior changes.
- Do not implement semantic gameplay invariant execution.
- Do not change parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, log drift report behavior, schema snapshot update policy, schema drift report behavior, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not update tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json.
- Do not change evidence-ledger entries, invariant names, drift flags, or vocabulary unless a separate contract/review loop explicitly authorizes it.
- Do not wire invariant reports into diagnostics, golden replay, feature-equity, log drift sensor, runtime status, workbook export, webhook delivery, or CI.
- Do not add runtime field-evidence attachment, merge/deploy gates, automatic tracker updates, or automatic GitHub issue creation.
- Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth.
- Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_invariant_execution.py
- python3 tools/run_evidence_invariants.py --check
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_evidence_schema_snapshot.py
- python3 -m pytest -q tests/test_evidence_schema_drift_report.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, invariant execution module, tool wrapper, focused tests, and implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/179"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/177"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/178"
  previous_merge_commit: "452a857e654ec63cdbff5472c6994ba3c8c8942f"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_invariant_execution.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_invariant_execution_comparison.md"
  verdict: "invariant_execution_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-invariant-execution"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_invariant_execution.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not implement parser behavior changes."
    - "Do not implement semantic gameplay invariant execution."
    - "Do not change parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, log drift report behavior, schema snapshot update policy, schema drift report behavior, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not update tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json."
    - "Do not change evidence-ledger entries, invariant names, drift flags, or vocabulary unless a separate contract/review loop explicitly authorizes it."
    - "Do not wire invariant reports into diagnostics, golden replay, feature-equity, log drift sensor, runtime status, workbook export, webhook delivery, or CI."
    - "Do not add runtime field-evidence attachment, merge/deploy gates, automatic tracker updates, or automatic GitHub issue creation."
    - "Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
```
