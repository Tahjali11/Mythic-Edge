# Parser Recovery Field Evidence Comparison Report Contract

## Module

Automated field-evidence comparison report for parser recovery planning.

Plain English: this contract defines a report-only layer that compares the
Field Recovery Matrix's expected evidence for parser-owned fields against a
reduced, public-safe summary of current field evidence. The report may classify
fields as direct, equivalent, derived/bounded, approximate/analytics-only,
unavailable, blocked-private, blocked-external, degraded, stale, conflicting,
or review-required. It must not restore parser fields, promote fixtures,
change corpus statuses, authorize private harvest, activate #388 or #381, or
claim readiness.

This Codex B pass does not implement code, open a PR, read private logs, run
watchers or diagnostics, create local artifacts, change parser behavior, or
claim parser recovery.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/453
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/452
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/539
- Previous merge commit: `b34c535a87c3640302b262fe45c28f1832a91346`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- Local `main` was behind `origin/main` and had unrelated untracked recovery
  contract artifacts from earlier steps. To avoid overwriting local state, this
  pass inspected `origin/main` directly instead of pulling.
- `origin/main` was
  `b34c535a87c3640302b262fe45c28f1832a91346`.
- Issue #453 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issue #452 was closed and PR #539 was merged into `main`.
- Issue #451 was closed and PR #538 was merged into `main`.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #453 and its Codex A reconciliation comment
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #452 and PR #539
- Issue #451 and PR #538
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`
- `docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_field_recovery_matrix.py`
- `tests/test_local_watcher_offset_window_monitor.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- adjacent diagnostics, drift, corpus parity, and parser-evidence pipeline
  surfaces as committed public-safe references only

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke check
was run, tailed, hashed, copied, summarized, or read.

## Observed Current Behavior

Issue #451 added a report-only Field Recovery Matrix helper:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

The matrix owns expected recovery metadata:

- field IDs and field families;
- evidence-ledger entry IDs;
- required direct evidence;
- allowed fallback evidence;
- forbidden fallback evidence;
- recovery categories;
- parser output policies;
- analytics/display output policies;
- minimum confidence;
- allowed finality;
- degradation flags;
- stale-source behavior;
- review requirements;
- non-claims and false readiness flags.

Issue #452 added a synthetic-only local watcher / offset-window metadata helper:

- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_local_watcher_offset_window_monitor.py`

The monitor owns symbolic source/window metadata for synthetic or explicitly
approved future local windows. It does not read private sources, write local
state, run a watcher, call `FileTailer`, or prove watcher correctness.

Existing evidence-ledger and runtime field-evidence modules define reusable
vocabularies:

- value sources: `observed`, `derived`, `inferred`, `unknown`, `conflict`,
  and `legacy_enriched`;
- confidence labels: `high`, `medium`, `low`, and `unknown`;
- finality labels: `live`, `provisional`, `final`, and `reconciled`;
- invariant statuses: `passed`, `failed`, `not_applicable`, `not_checked`,
  and `degraded`;
- review behavior for conflicts, failed invariants, and low-confidence final
  or reconciled values.

No dedicated field-evidence comparison report contract, helper module, tests,
or report artifact existed before this contract.

## Problem

After the Field Recovery Matrix and offset-window monitor, Mythic Edge needs a
safe way to compare "what evidence should support this parser-owned field" with
"what reduced evidence summary is currently available." That comparison is
useful for human recovery review and later staged recovery candidate packets.

Without a narrow contract, a future comparison report could accidentally:

- treat approximate evidence as parser truth;
- treat fallback evidence as high-confidence direct evidence;
- treat stale or degraded evidence as recovered parser behavior;
- treat private-evidence or external-boundary blockers as parser support;
- use local watcher offsets as proof of source completeness;
- promote corpus rows or fixtures from report wording;
- authorize private harvest or #388/#381 activation;
- let analytics, AI, coaching, workbook formulas, Apps Script, or reports own
  facts that remain parser-owned.

The first bad value is any comparison row whose status, confidence, output
policy, or recovery hint causes a parser field, fixture, corpus row, private
harvest, or readiness flag to move forward without a separate scoped contract,
implementation, fixture/review evidence, and approved workflow step.

## Scope Decision

This contract approves a future report-only metadata implementation.

Codex C may implement a pure Python helper and focused tests that compare:

1. expected field evidence from the Field Recovery Matrix; and
2. reduced current field-evidence summaries, optionally with sanitized
   offset-window metadata.

The implementation must be deterministic, side-effect-free, and public-safe.
It may produce in-memory comparison reports for tests and future review
consumers. It must not read private logs, write report artifacts, create
fixtures, create manifests, change parser outputs, change corpus metadata,
change runtime status, or integrate into diagnostics/drift/golden replay unless
a later contract explicitly authorizes that integration.

This contract does not authorize:

- private source discovery;
- private source content reads;
- watcher startup;
- tailer startup;
- diagnostics or drift execution;
- local offset-state writing;
- local report writing;
- recovery packet generation;
- issue or fixture draft generation;
- fixture creation or promotion;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`;
- `private_harvest_authorized=true`;
- `fixture_promotion_authorized=true`;
- `corpus_status_change_authorized=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns the comparison report vocabulary, expected-versus-
current evidence comparison policy, degraded/stale/review routing, and
candidate recovery hints.

Quality / Governance owns workflow routing, protected-surface assertions,
secret/private-marker validation, and non-claim enforcement.

Parser remains the owner of parser facts, parser behavior, parser events,
router semantics, parser state final reconciliation, match/game identity,
deduplication, and normalized output values.

Generated / Local Artifacts owns any future local-only private evidence,
offset state, private review report, or local watcher output if separately
approved.

Analytics, workbook/transport, Apps Script, local app, AI, and coaching
surfaces are consumers only. They must not own comparison truth or parser
recovery truth.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Quality / Governance, for report validation and workflow safety.
- Parser, for parser-owned field identity and output-policy boundaries.
- Generated / Local Artifacts, for future local-only private evidence or
  offset-window inputs if separately approved.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a diagnostics or
drift contract, not a local app contract, not a workbook or transport
contract, not an analytics contract, not an AI/coaching contract, not a CI
gate, and not a release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser values remains the existing parser, router, event,
state, model, extractor, match/game identity, deduplication, and final
reconciliation layers.

Truth owner for expected field recovery categories and output policies remains:

- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

Truth owner for local watcher / offset-window metadata remains:

- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_local_watcher_offset_window_monitor.py`

Truth owner for evidence-ledger vocabulary remains:

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

Truth owner for runtime field-evidence sidecar behavior remains:

- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `tests/test_runtime_field_evidence.py`

This contract owns only the comparison report schema, comparison status
vocabulary, fail-closed comparison rules, and candidate recovery hint
vocabulary. It does not own parser facts, private evidence, fixture expected
output, corpus status, analytics truth, AI truth, coaching truth, readiness, or
tracker completion.

## Bridge-Code Status

`deferred_future_boundary`

This Codex B pass authorizes no bridge code.

If later implemented, the helper may become shared support from Corpus /
Provenance to Quality / Governance and future parser recovery review workflows.

Allowed future data flow:

```text
Field Recovery Matrix rows
  + reduced current field-evidence summaries
  + optional sanitized local watcher / offset-window metadata
  -> field-evidence comparison report rows
  -> human/Codex recovery review
  -> later candidate packet issue, if separately authorized
```

Forbidden reverse flow:

```text
field-evidence comparison report
  -/-> parser value overwrite
  -/-> parser event or router behavior change
  -/-> parser state final reconciliation change
  -/-> workbook formula reconstruction
  -/-> webhook or Apps Script payload change
  -/-> analytics / AI / coaching truth
  -/-> fixture promotion
  -/-> corpus status promotion
  -/-> private harvest authorization
  -/-> #388 or #381 activation
```

## Files Owned By This Contract

This contract owns:

- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`

If implementation proceeds, Codex C may add or update only:

- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_evidence_comparison_report.py`
- `docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md`

If Codex E later reviews the implementation, it may add:

- `docs/contract_test_reports/parser_recovery_field_evidence_comparison_report.md`

Read-only references for Codex C:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- focused tests for those modules

Explicitly not owned:

- parser modules and parser runtime imports;
- `FileTailer`, stream, router, event classes, state, models, extractors;
- diagnostics report shape or drift report behavior;
- golden replay behavior or expected outputs;
- corpus manifest and session ledger files;
- fixture files or fixture-promotion packets;
- local watcher outputs, offset state, local report files, and private reports;
- runtime status schema;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport;
- analytics schema or AI/model-provider behavior.

## Public Interface

Future implementation should expose a narrow helper interface:

```python
FIELD_EVIDENCE_COMPARISON_REPORT_OBJECT = (
    "mythic_edge_parser_field_evidence_comparison_report"
)
FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION = (
    "parser_recovery_field_evidence_comparison_report.v1"
)
FIELD_EVIDENCE_COMPARISON_ROW_OBJECT = (
    "mythic_edge_parser_field_evidence_comparison_row"
)
FIELD_EVIDENCE_EXPECTED_OBJECT = (
    "mythic_edge_parser_expected_field_evidence"
)
FIELD_EVIDENCE_CURRENT_OBJECT = (
    "mythic_edge_parser_current_field_evidence_summary"
)

build_field_evidence_comparison_report(...)
compare_field_evidence(...)
validate_field_evidence_comparison_report(...)
validate_field_evidence_comparison_row(...)
validate_expected_field_evidence(...)
validate_current_field_evidence_summary(...)
```

The helper must not expose a CLI in this issue. A CLI, diagnostics integration,
drift integration, report writer, corpus integration, or recovery-packet
writer requires a later contract.

## Inputs

### Field Recovery Matrix

Type: mapping returned by `field_recovery_matrix.build_field_recovery_matrix()`
or a public-safe mapping with the same schema.

Required fields:

- `object`
- `schema_version`
- `status`
- false readiness and authorization flags
- `rows`
- `non_claims`

Row fields consumed:

- `field_id`
- `display_name`
- `field_family`
- `parser_owner`
- `output_surfaces`
- `evidence_ledger_entry_ids`
- `required_direct_evidence`
- `allowed_fallback_evidence`
- `forbidden_fallback_evidence`
- `recovery_category`
- `parser_output_policy`
- `analytics_output_policy`
- `minimum_confidence`
- `allowed_finality`
- `degradation_flags`
- `stale_source_behavior`
- `review_required`
- `restoration_requirements`
- `non_claims`

The comparison report must copy parser and analytics output policies from the
matrix. It must not invent more permissive policies.

### Current Field-Evidence Summaries

Type: sequence of public-safe mappings.

Each current summary must use reduced metadata only:

- `object`: `mythic_edge_parser_current_field_evidence_summary`
- `schema_version`: `parser_recovery_field_evidence_comparison_report.v1`
- `field_id`
- `evidence_ledger_entry_ids`
- `observed_signal_ids`
- `source_event_families`
- `source_event_kinds`
- `value_source`
- `confidence`
- `finality`
- `degradation_flags`
- `invariant_status`
- `stale_source_status`
- `review_required`
- `source_window_refs`
- `contents_read`: must be `False`
- `raw_path_included`: must be `False`
- `raw_hash_included`: must be `False`
- `raw_payload_values_included`: must be `False`
- `private_excerpt_included`: must be `False`

Allowed values must reuse evidence-ledger vocabulary where applicable.
`source_window_refs` may contain symbolic IDs only. It must not contain exact
private paths, exact private offsets, exact private file sizes, exact private
timestamps, raw hashes, raw lines, source snippets, or private report paths.

### Optional Watcher / Offset-Window Context

Type: public-safe report or summary generated from the local watcher /
offset-window monitor helper.

Allowed fields:

- report object and schema version;
- symbolic source label;
- source class;
- privacy class;
- selection status;
- window ID;
- source generation status;
- window status;
- offset range status;
- source transition status;
- stale-window status;
- buffer/backpressure/error statuses;
- false content/path/hash/local-state flags;
- non-claims.

Private/local watcher context may only appear as sanitized status labels and
symbolic IDs from a separately approved future workflow. This issue does not
authorize collecting or committing real private offsets or local source
metadata.

### Report Context

Type: optional mapping.

Allowed fields:

- `source_issue`
- `pipeline_tracker`
- `parent_private_evidence_issue`
- `base_branch`
- `target_branch`
- `comparison_run_label`
- `input_generation_label`
- `validation_context`

The context must not contain local absolute paths, raw evidence values,
private report paths, secrets, private hashes, or generated artifacts.

## Outputs

### Report Object

The report object is an in-memory mapping.

Required fields:

- `object`: `mythic_edge_parser_field_evidence_comparison_report`
- `schema_version`: `parser_recovery_field_evidence_comparison_report.v1`
- `source_issue`
- `pipeline_tracker`
- `parent_private_evidence_issue`
- `status`
- `status_reasons`
- `field_recovery_matrix_schema_version`
- `current_evidence_schema_version`
- `watcher_context_schema_version`
- `parser_behavior_ready`: `False`
- `pipeline_activation_ready_for_issue_388`: `False`
- `private_harvest_authorized`: `False`
- `fixture_promotion_authorized`: `False`
- `corpus_status_change_authorized`: `False`
- `field_recovery_ready`: `False`
- `summary`
- `rows`
- `privacy`
- `protected_surface_assertions`
- `limitations`
- `non_claims`

Allowed report statuses:

- `comparison_ready`
- `review_required`
- `invalid_input`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `fail_closed`

The report is provisional review metadata, never final parser truth.

### Row Object

Each row must include:

- `object`: `mythic_edge_parser_field_evidence_comparison_row`
- `field_id`
- `display_name`
- `field_family`
- `expected_evidence`
- `current_evidence`
- `recovery_category`
- `parser_output_policy`
- `analytics_output_policy`
- `comparison_status`
- `confidence`
- `finality`
- `degradation_flags`
- `stale_source_status`
- `watcher_window_status`
- `candidate_recovery_hints`
- `review_required`
- `stop_reasons`
- `non_claims`

Rows are report-only and provisional. They must not update parser fields,
runtime state, workbook rows, webhooks, corpus metadata, fixtures, diagnostics,
or local artifacts.

### Expected Evidence Object

Each expected evidence object must include:

- `object`: `mythic_edge_parser_expected_field_evidence`
- `field_id`
- `evidence_ledger_entry_ids`
- `required_direct_evidence`
- `allowed_fallback_evidence`
- `forbidden_fallback_evidence`
- `expected_recovery_category`
- `minimum_confidence`
- `allowed_finality`
- `expected_degradation_flags`
- `stale_source_behavior`
- `review_required_by_matrix`

### Current Evidence Object

Each current evidence object must include:

- `object`: `mythic_edge_parser_current_field_evidence_summary`
- `field_id`
- `evidence_ledger_entry_ids`
- `observed_signal_ids`
- `value_source`
- `confidence`
- `finality`
- `degradation_flags`
- `invariant_status`
- `stale_source_status`
- `source_window_refs`
- `review_required`
- false raw/private/local content flags

The current object is a summary of evidence metadata, not a field value carrier.
It must not include parser output values, raw payload values, raw private lines,
decklists, private paths, local artifacts, or exact private file metadata.

## Comparison Vocabulary

### Comparison Statuses

Allowed comparison statuses:

- `direct`
- `equivalent`
- `derived_bounded`
- `approximate_analytics_only`
- `unavailable`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `degraded`
- `stale`
- `conflict`
- `review_required`
- `invalid_input`

Status meaning:

- `direct`: current evidence satisfies the matrix's required direct evidence,
  confidence, and finality requirements without conflict.
- `equivalent`: current evidence appears semantically equivalent to the
  expected direct signal, but still requires parser contract and fixture review
  before parser restoration.
- `derived_bounded`: current evidence supports a bounded derivation permitted
  by the matrix, with confidence capped by matrix policy.
- `approximate_analytics_only`: current evidence may support analytics/display
  context only and must never restore parser truth.
- `unavailable`: expected evidence is absent and no approved fallback is
  available.
- `blocked_private_evidence`: evidence may exist only behind parent #434 or
  another explicitly approved private-evidence gate.
- `blocked_external_boundary`: evidence requires an external source or
  scenario boundary not available in committed Mythic Edge artifacts.
- `degraded`: evidence exists but has degradation flags, missing dependencies,
  invariant degradation, or weak fallback.
- `stale`: evidence or source-window context is stale relative to the expected
  recovery policy.
- `conflict`: evidence is contradictory, invariant status failed, or value
  source is `conflict`.
- `review_required`: manual/Codex review is required before any next workflow
  step.
- `invalid_input`: the report input is malformed, contains forbidden content,
  violates vocabulary, or tries to set an authorization/readiness flag true.

### Candidate Recovery Hints

Allowed recovery hints:

- `no_recovery_authorized`
- `existing_parser_behavior_sufficient`
- `needs_parser_contract`
- `needs_fixture_review`
- `needs_private_evidence_gate`
- `needs_external_boundary_issue`
- `needs_stale_source_refresh`
- `needs_field_matrix_update`
- `needs_manual_review`
- `needs_runtime_field_evidence_mapping`
- `needs_watcher_context_review`
- `analytics_display_only`
- `blocked_by_policy`

Hints are routing suggestions only. They do not authorize parser changes,
fixture promotion, private harvest, corpus status changes, readiness claims, or
issue closure.

## Confidence, Finality, Degradation, And Review Rules

The report must reuse evidence-ledger vocabulary for value source, confidence,
finality, drift/degradation flags, and invariant status.

Rules:

- A comparison row must never raise confidence above the current evidence
  summary's confidence.
- A comparison row must never raise confidence above the matrix's allowed
  category policy.
- `direct` may be high-confidence only when direct expected evidence is present,
  finality is allowed by the matrix, invariant status is not failed, and no
  privacy/stale/degraded/conflict flags are present.
- `equivalent` is capped at medium confidence and must set
  `review_required=true`.
- `derived_bounded` is capped at medium confidence and must set
  `review_required=true` unless a later parser contract says otherwise.
- `approximate_analytics_only` is capped at low confidence and must use a
  parser output policy that prevents parser restoration.
- `blocked_private_evidence`, `blocked_external_boundary`, `unavailable`,
  `conflict`, and `invalid_input` must use `unknown` or `low` confidence and
  must set `review_required=true`.
- `stale` must apply the matrix row's `stale_source_behavior` and must not
  claim recovery.
- Any failed invariant, `value_source=conflict`, unknown vocabulary, unknown
  ledger entry, forbidden fallback evidence, or forbidden local/private marker
  must route to `review_required`, `conflict`, or `invalid_input`.
- Low-confidence final or reconciled evidence must require review, matching
  runtime field-evidence behavior.

## Relationship To Field Recovery Matrix

The Field Recovery Matrix is the authority for expected recovery category,
parser output policy, analytics/display output policy, minimum confidence,
allowed finality, stale-source behavior, restoration requirements, and
non-claims.

The comparison report must:

- consume matrix rows without mutating them;
- copy output policies from the matrix row;
- preserve matrix anti-promotion rules;
- preserve matrix false readiness and authorization flags;
- treat non-direct matrix rows as review-required unless a later scoped parser
  contract explicitly changes that row;
- fail closed if matrix validation fails;
- fail closed if current evidence tries to override a matrix parser output
  policy.

The comparison report may summarize category counts, but summary counts are
not readiness metrics and must not be used as #388 activation evidence.

## Relationship To Local Watcher / Offset-Window Metadata

Offset-window metadata is optional context. It may help explain whether current
evidence is stale, unavailable, degraded, or review-required.

Allowed watcher-derived status effects:

- `window_ready` may support normal comparison when paired with valid current
  evidence.
- `window_in_progress` should keep finality provisional or review-required.
- `window_closed` may support stable review context, but not parser truth.
- `window_unavailable` should route affected fields to `unavailable` or
  `review_required`.
- `window_stale` should route affected fields to `stale`.
- `window_degraded` should route affected fields to `degraded`.
- `window_blocked_missing_approval` should route affected fields to
  `blocked_private_evidence`.
- `window_manual_review_required` should route affected fields to
  `review_required`.

The report must not:

- call the watcher;
- call `FileTailer`;
- read source contents;
- read private offsets from disk;
- write offset state;
- include exact private offsets, sizes, timestamps, hashes, paths, raw lines,
  or private report paths;
- treat watcher or offset-window metadata as parser source completeness,
  watcher correctness, private smoke success, or recovery proof.

## Parser Output Policy Versus Analytics / Display Policy

Parser output policy and analytics/display output policy must stay separate.

The comparison report may say:

- parser output must preserve existing behavior;
- parser output requires a new parser contract and fixture review;
- parser output must remain blank or unknown;
- parser output must remain blocked;
- analytics/display may show degraded, approximate, unavailable, or review
  context.

The comparison report must not:

- fill parser fields from analytics display context;
- tell workbook formulas or Apps Script to reconstruct parser truth;
- let `approximate_analytics_only` become parser output;
- let analytics, AI, coaching, dashboards, or reports override parser fields.

## Privacy And Forbidden Committed Artifact Rules

The report and any future tests must reject or fail closed on:

- raw Player.log or UTC_Log lines;
- exact private local paths;
- exact private offsets, file sizes, timestamps, raw hashes, or content hashes;
- private report paths;
- app-data contents;
- diagnostics, drift, watcher, tailer, live MTGA, network, firewall/drop,
  packet, OS/router, or private smoke outputs;
- screenshots;
- workbook exports;
- SQLite files;
- failed posts;
- runtime status files;
- secrets, credentials, tokens, API keys, webhook URLs, bearer tokens;
- decklists, card choices, private strategy notes, hidden-card evidence, or
  generated private artifacts.

Synthetic IDs, symbolic source labels, booleans, allowed vocabulary labels,
schema versions, repo-relative source file paths, issue URLs, PR URLs, and
public-safe validation command names are allowed.

Validation errors must not echo private or path-like submitted values. They
should report symbolic error locations such as
`privacy:absolute_path:current_evidence[0].source_window_refs[1]`.

## Invariants

- The report object and row objects are deterministic and JSON-serializable.
- The report is review metadata only.
- All readiness and authorization flags remain false.
- `non_claims` must include at least:
  - `not_parser_truth`
  - `not_field_recovery_readiness`
  - `not_private_harvest_authorization`
  - `not_fixture_promotion`
  - `not_corpus_status_change`
  - `not_parser_behavior_readiness`
  - `not_pipeline_activation_readiness`
  - `not_watcher_correctness`
  - `not_private_smoke_success`
  - `not_merge_readiness`
  - `not_deploy_readiness`
  - `not_release_readiness`
  - `not_production_behavior`
  - `not_analytics_truth`
  - `not_ai_truth`
  - `not_coaching_truth`
- Current evidence summaries must not carry parser field values.
- Current evidence summaries must not carry raw/private evidence.
- Unknown fields require review.
- Unknown evidence-ledger entry IDs require review.
- Unknown comparison statuses are invalid input.
- Unknown recovery hints are invalid input.
- Conflicts and failed invariants require review.
- Blocked private evidence remains blocked until a separate private-evidence
  contract and approval authorize a future local-only execution packet.
- External-boundary evidence remains blocked until a separate issue resolves
  the source boundary.
- Approximate analytics-only evidence must never restore parser output.
- Stale source context must never imply fresh parser evidence.

## Error Behavior

Malformed input must fail closed:

- missing or invalid matrix object: report status `invalid_input`;
- matrix validation errors: report status `invalid_input`;
- current evidence not a sequence: report status `invalid_input`;
- current evidence row not a mapping: row status `invalid_input`;
- unknown field ID: row status `review_required`;
- duplicate current evidence for a field: row status `conflict` or
  `review_required`;
- unknown evidence-ledger entry ID: row status `review_required`;
- forbidden current evidence source: row status `invalid_input`;
- current evidence includes field values or raw payload values: report status
  `fail_closed`;
- privacy marker found: report status `fail_closed`;
- protected-surface assertion not false: report status `fail_closed`;
- any readiness or authorization flag true: report status `fail_closed`;
- stale watcher context: affected rows status `stale`;
- blocked watcher/private context: affected rows status
  `blocked_private_evidence`;
- unavailable source context: affected rows status `unavailable` or
  `review_required`.

The helper must return symbolic errors and review statuses. It must not raise
uncaught exceptions for normal malformed report inputs unless the caller passes
an unsupported Python type that cannot be inspected safely.

## Side Effects

Codex B side effects:

- Writes only this contract file.

Authorized future Codex C side effects:

- Add a pure helper module.
- Add focused tests.
- Add an implementation handoff.

Not authorized:

- reading source logs;
- running watchers, tailers, diagnostics, drift, live MTGA, network, firewall,
  packet, OS/router, or private smoke checks;
- writing report artifacts;
- writing local offset state;
- writing fixtures, manifests, expected outputs, proof files, metadata diffs,
  or recovery packets;
- editing corpus metadata;
- changing parser runtime imports or behavior;
- changing workbook/webhook/Apps Script/Google Sheets/output transport;
- changing analytics, AI, coaching, CI, merge, deploy, release, production, or
  final integration policy;
- creating, closing, or updating issues/PRs unless a later workflow role
  explicitly authorizes it.

## Dependency Order

If implementation proceeds:

1. Add constants and validators in
   `src/mythic_edge_parser/app/field_evidence_comparison_report.py`.
2. Reuse public vocabularies from `field_recovery_matrix`,
   `local_watcher_offset_window_monitor`, and `evidence_ledger`.
3. Add comparison functions that fail closed on invalid input.
4. Add focused synthetic/in-memory tests.
5. Validate no runtime parser path imports the helper.
6. Write the implementation handoff.
7. Route to Codex E for adversarial review.

## Compatibility

The report must remain compatible with:

- Field Recovery Matrix object version `parser_field_recovery_matrix.v1`;
- local watcher offset-window monitor object version
  `parser_recovery_local_watcher_offset_window_monitor.v1`;
- evidence-ledger field-evidence version `player_log_field_evidence.v1`;
- existing runtime field-evidence report version
  `player_log_runtime_field_evidence_report.v1`.

If a future change requires new vocabulary, it must route back to Codex B
instead of silently accepting new statuses, flags, or policies.

## Tests Required

Codex C should add focused tests for:

- report object shape and required false readiness/authorization flags;
- row object shape;
- direct comparison success for a synthetic direct field;
- equivalent comparison requiring review and medium confidence cap;
- derived bounded comparison requiring review and confidence cap;
- approximate analytics-only comparison never restoring parser output;
- unavailable and blocked rows remaining blocked;
- stale watcher/window status routing to `stale`;
- degraded current evidence routing to `degraded`;
- conflict and failed invariant routing to `conflict` or `review_required`;
- unknown field IDs and unknown ledger IDs requiring review;
- invalid input failing closed;
- privacy markers, local absolute paths, raw log markers, exact private offset
  fields, and raw hash/content fields being rejected without value echo;
- deterministic JSON serialization;
- copy-safe input handling;
- no parser runtime import/use.

Recommended validation commands for Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
PYTHONPATH=src python3 -m pytest -q tests/test_runtime_field_evidence.py
PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Codex E should additionally inspect whether:

- the helper imports only allowed support modules;
- no parser runtime path imports the helper;
- no private values are echoed by validation errors;
- all non-claims and false flags are preserved;
- comparison statuses cannot promote parser output, fixture promotion, corpus
  status, private harvest, or #388/#381 activation.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_recovery_field_evidence_comparison_report.md`.
- The report object and row object schemas are explicit.
- Expected evidence and current evidence vocabularies are explicit.
- Comparison statuses and candidate recovery hints are explicit.
- Confidence, finality, degradation, stale-source, conflict, and review rules
  are explicit.
- Field Recovery Matrix output policies remain authoritative.
- Local watcher / offset-window metadata remains optional sanitized context.
- Parser output policy remains separate from analytics/display policy.
- Privacy and local-artifact rules reject raw/private evidence.
- Error behavior fails closed.
- Later Codex C/E validation expectations are testable.
- #388, #381, and #434 remain open/inactive as applicable.
- All readiness and authorization flags remain false.

## Open Questions / Contract Risks

- The future current-field-evidence summary input may need a separate producer
  contract if Codex C cannot safely model it with reduced in-memory test data.
- A future report writer, CLI, diagnostics integration, drift integration, or
  recovery packet generator needs a separate issue and contract.
- Some matrix seed rows may need expansion before a real comparison report is
  useful for every parser-owned output field. That expansion must not happen
  silently inside this issue.
- Private evidence and external-boundary rows remain blocked. The comparison
  report may identify blockers but must not resolve them.

## Next Workflow Action

Next role: Codex C: Module Implementer, if implementation is desired.

Codex C should implement only the pure, report-only helper and focused tests.
It should not write report artifacts, run private checks, create fixtures,
change parser behavior, or integrate into runtime/diagnostics/drift/corpus
systems.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #453.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/453

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/452

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/539

Previous merge commit:
b34c535a87c3640302b262fe45c28f1832a91346

Base branch:
main

Contract:
docs/contracts/parser_recovery_field_evidence_comparison_report.md

Goal:
Implement the report-only field-evidence comparison helper and focused tests
defined by the contract.

Expected implementation artifacts:
- src/mythic_edge_parser/app/field_evidence_comparison_report.py
- tests/test_field_evidence_comparison_report.py
- docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md

Implementation scope:
- Build a pure, deterministic helper that compares Field Recovery Matrix rows
  against reduced current field-evidence summaries.
- Reuse existing vocabularies from field_recovery_matrix,
  local_watcher_offset_window_monitor, and evidence_ledger.
- Keep all readiness and authorization flags false.
- Fail closed on malformed, private, stale, degraded, conflicting, unknown, or
  policy-changing inputs.
- Add focused synthetic/in-memory tests only.

Protected boundaries:
- Do not open a PR.
- Do not close #453, #388, or #434.
- Do not activate #388 or #381.
- Do not run or read private Player.log, UTC_Log, app-data, live MTGA,
  network, firewall/drop, packet, OS/router, diagnostics, drift, watcher,
  tailer, or private smoke checks.
- Do not create fixtures, manifests, expected outputs, recovery packets,
  metadata diffs, local watcher outputs, offset state, local/generated
  artifacts, private reports, or corpus metadata edits.
- Do not promote blocked, report-only, private-evidence, external-boundary,
  approximate, fallback, watcher, offset-window, degraded, stale, unavailable,
  or review-required signals to parser truth.
- Do not change parser behavior, parser event classes, parser state final
  reconciliation, router semantics, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics behavior, AI/model-provider behavior,
  coaching behavior, CI gates, merge readiness, deploy readiness, release
  readiness, production behavior, or final integration policy.
- Do not claim parser_behavior_ready, pipeline activation readiness,
  fixture-promotion readiness, field recovery readiness, private smoke success,
  watcher correctness, release readiness, production readiness, analytics
  truth, AI truth, coaching truth, or full parser regression parity.

Validation:
- Run the focused tests required by the contract.
- Run ruff on the new module and tests.
- Run git diff --check.
- Run agent-doc, secret-pattern, protected-surface, and validation-selector
  checks on the touched paths if available.

Expected output:
- Implementation summary.
- Validation run.
- Remaining risks.
- Recommended next role.
- workflow_handoff block with repository and repository_url.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/453"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/452"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/539"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #453 problem representation"
  target_artifact: "docs/contracts/parser_recovery_field_evidence_comparison_report.md"
  verdict: "field_evidence_comparison_report_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "b34c535a87c3640302b262fe45c28f1832a91346"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_scope: "report_only_field_evidence_comparison_helper"
  validation:
    - "git fetch --prune origin"
    - "verified origin/main at b34c535a87c3640302b262fe45c28f1832a91346"
    - "inspected #453, #388, #434, #452/PR #539, and #451/PR #538"
    - "inspected #451/#452 contracts, handoffs, modules, and focused tests from origin/main"
  stop_conditions:
    - "Do not close #453, #388, or #434."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, watcher, tailer, network, firewall/drop, packet, OS/router, or private smoke checks."
    - "Do not create fixtures, manifests, expected outputs, recovery packets, metadata diffs, local watcher outputs, offset state, local/generated artifacts, private reports, or corpus metadata edits."
    - "Do not promote blocked, report-only, private-evidence, external-boundary, approximate, fallback, watcher, offset-window, degraded, stale, unavailable, or review-required signals to parser truth."
    - "Do not change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics behavior, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, production behavior, or final integration policy."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, field recovery readiness, private smoke success, watcher correctness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
