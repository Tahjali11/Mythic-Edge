# Player.log Evidence Ledger Tier 6 Runtime Health And Drift Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/171
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/169
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/170
- previous_merge_commit: 5f242c07b2418c6d27d1e4670f19a81785546c27
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier6-runtime-health-drift
- target_artifact: docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md
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
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_gsm_truncation.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #171 maps Tier 6 runtime health and drift detection provenance in the
Player.log evidence ledger.

The fields in scope are exactly:

- `diagnostics_status`
- `unknown_entry_count`
- `truncation_count`

These are parser-resilience report outputs. They are not match facts, game
facts, merge readiness, deploy readiness, CI truth, workbook truth, transport
truth, analytics truth, or AI truth.

Plain English: Mythic Edge can say "this diagnostics run looked pass/review/
fail/unknown," "this analyzed log had N unknown routed entries," and "this run
observed N GameState truncation/data-loss markers." It must not say that a
healthy diagnostics report proves all parser facts are correct, that unknown
entries are safe to ignore, or that truncation markers recover missing
GameState data.

This contract documents provenance metadata only. It must not change
diagnostics behavior, drift behavior, truncation parsing, router semantics,
runtime status schema, golden replay behavior, feature-equity behavior, parser
behavior, workbook schema, webhook payload shape, Apps Script behavior, output
transport, runtime artifacts, Match Journal behavior, overlay behavior, SQLite
behavior, Google Sheets sync behavior, analytics truth, AI truth, or
model-provider behavior.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
allowed `value_source`, `confidence`, `finality`, invariant, drift, and
privacy labels.

`docs/contracts/parser_diagnostics_mode.md` remains authoritative for parser
diagnostics report purpose, public API, run modes, report schema, local-only
privacy posture, parser-health versus transport-health separation, and
pass/review/fail/unknown labels. Issue #171 may document diagnostics outputs
as Tier 6 provenance fields, but it must not change diagnostics report shape
or CLI behavior.

`docs/contracts/parser_gsm_truncation.md` remains authoritative for
`TruncationEvent`, parser-owned truncation/data-loss evidence, count semantics,
and the rule that truncation markers do not reconstruct missing GameState
payloads.

`docs/contracts/parser_golden_replay_harness.md` and
`docs/contracts/parser_feature_equity_corpus_ratchet.md` remain authoritative
for fixture and corpus report behavior. They may validate Tier 6 evidence, but
they do not become parser truth or runtime-health truth.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #171 provenance should be
recorded through this contract, implementation handoff, family notes, entry
notes, and focused tests rather than by changing the top-level ledger object
shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/app/parser_diagnostics.py` owns local diagnostics
  report aggregation and advisory status labels such as `pass`, `review`,
  `fail`, and `unknown`.
- `src/mythic_edge_parser/app/log_drift_sensor.py` owns local routing and drift
  evidence such as routed counts, unknown counts, unknown signatures, unmatched
  API names, and baseline deltas.
- `src/mythic_edge_parser/router.py` owns `RouterStats`, including routed,
  unknown, timestamp-missing, and timestamp-parse-failure counts for an
  analyzed input.
- `src/mythic_edge_parser/parsers/truncation.py`,
  `src/mythic_edge_parser/events.py`, and router dispatch own parser-observed
  GSM truncation/data-loss evidence.
- `src/mythic_edge_parser/app/diagnostics.py` owns runtime logging/status/error
  surfaces. Runtime status is local operational evidence, not parser truth.
- `src/mythic_edge_parser/app/golden_replay.py` and
  `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` are
  validation/report consumers of runtime-health evidence, not truth owners.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence, finality, degradation behavior, drift flags, invariants, and
  protected boundary notes.
- Workbook formulas, dashboards, webhook transport, Apps Script, Match Journal,
  overlays, SQLite, Google Sheets sync, analytics, archetype classification,
  OpenAI/model-provider output, and AI output are downstream consumers only.

The evidence ledger must not become a second diagnostics runner, a drift
detector implementation, an invariant executor, a schema snapshot generator, a
CI gate, a merge/deploy gate, a runtime status schema migration, or an AI truth
layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier6_runtime_health_drift.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/parsers/truncation.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- tests/test_parser_diagnostics_mode.py
- tests/test_log_drift_sensor.py
- tests/test_gsm_truncation_parser.py
- tests/test_golden_replay_harness.py
- tests/test_feature_equity_corpus_ratchet.py

## Public Interface

This contract covers evidence-ledger metadata for existing diagnostics, drift,
router, and truncation surfaces. It does not create a new runtime API, parser
event, status file field, workbook column, webhook field, Apps Script field, or
CLI.

Required Tier 6 family transition:

- `runtime_health_and_drift_detection.status` changes from
  `registered_future` to `seeded_sample`.
- `runtime_health_and_drift_detection.seed_fields` becomes exactly:
  - `diagnostics_status`
  - `unknown_entry_count`
  - `truncation_count`
- `runtime_health_and_drift_detection.future_fields` becomes empty.
- Tier 7 `derived_analytics_outputs` remains registered future work.

Required Tier 6 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier6.runtime_health_and_drift_detection.diagnostics_status` | `diagnostics_status` | `Diagnostics Status` | `derived` |
| `tier6.runtime_health_and_drift_detection.unknown_entry_count` | `unknown_entry_count` | `Unknown Entry Count` | `derived` |
| `tier6.runtime_health_and_drift_detection.truncation_count` | `truncation_count` | `Truncation Count` | `derived` from observed truncation evidence |

Existing report surfaces referenced by the entries:

| Existing surface | Relevant paths |
| --- | --- |
| Diagnostics report | `overall_status`, `summary.parser_status`, `parser_health.status`, `summary.unknown_entries`, `summary.truncation_events`, `parser_health.entry_counts.unknown`, `truncation_and_data_loss.truncation_count`, `unknowns_and_degradation.drift_flags` |
| Drift report | `status`, `entry_counts.routed`, `entry_counts.unknown`, `entry_counts.unknown_rate_pct`, `top_unknown_signatures`, `top_unmatched_api_names`, `top_unmatched_request_api_names`, `baseline_delta.*` |
| Router stats | `RouterStats.routed`, `RouterStats.unknown`, `RouterStats.timestamp_missing`, `RouterStats.timestamp_parse_failure` |
| Truncation event | `TruncationEvent.kind`, `payload.type`, `payload.data_loss`, `payload.recoverable`, `payload.drift_flag`, `payload.game_object_count`, `payload.annotation_count` |
| Golden replay | `diagnostics_summary`, `unknowns_and_degradation.unknown_entry_count`, `truncation_and_data_loss.truncation_count` |
| Feature-equity corpus | `unknowns_and_degradation.unknown_entries`, `truncation_and_data_loss.truncation_events`, `fixtures_with_truncation`, `data_loss_markers` |

Fields not authorized as separate seed fields in issue #171:

- `parser_status`
- `transport_status`
- `event_families_seen`
- `routed_entry_count`
- `unknown_rate_pct`
- `unknown_signatures`
- `unmatched_api_names`
- `unmatched_request_api_names`
- `timestamp_missing_count`
- `timestamp_parse_failure_count`
- `parser_failure_count`
- `transport_failure_count`
- `webhook_failure_count`
- `runtime_status`
- `workbook_status`
- `appscript_status`
- `merge_readiness`
- `deploy_readiness`
- `ci_status`
- `fixture_pass_rate`
- `analytics_confidence`
- `ai_confidence`

Those values may appear as facets, fallback evidence, degradation reasons, or
downstream report context only.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`5f242c07b2418c6d27d1e4670f19a81785546c27`:

- Issue #169 / PR #170 is deployed.
- Tracker #11 remains open.
- Tier 6 `runtime_health_and_drift_detection` is `registered_future`.
- Tier 6 future fields are:
  - `diagnostics_status`
  - `unknown_entry_count`
  - `truncation_count`
- Tier 6 seed fields are empty.
- Tier 7 remains `registered_future` for derived analytics outputs.
- `parser_diagnostics.build_parser_diagnostics_report(...)` produces a local
  JSON report with object `mythic_edge_parser_diagnostics_report` and schema
  `parser_diagnostics.v1`.
- Diagnostics report statuses use `pass`, `review`, `fail`, and `unknown`.
- Diagnostics report top-level `overall_status` is derived from section
  statuses. It is not CI, merge, deploy, parser-truth, or workbook authority.
- Diagnostics report `summary.unknown_entries` is derived from
  `parser_health.entry_counts.unknown`.
- Diagnostics report `summary.truncation_events` is derived from
  `truncation_and_data_loss.truncation_count`.
- Diagnostics report `parser_health.entry_counts` is populated from
  `log_drift_sensor.build_player_log_drift_report(...)`.
- Diagnostics report `truncation_and_data_loss.data_loss_events` is collected
  by routing entries and summarizing `Truncation` events or payloads with
  `data_loss is True`.
- Diagnostics report separates parser health from transport health and notes
  that workbook and Apps Script are not queried by diagnostics v1.
- `log_drift_sensor.build_player_log_drift_report(...)` replays a source log
  through `LineBuffer` and `Router`, counts routed and unknown entries, records
  unknown signatures and unmatched API names, and reports baseline deltas.
- `RouterStats` tracks routed, unknown, timestamp-missing, and
  timestamp-parse-failure counts for the analyzed input.
- `parsers/truncation.py` emits `TruncationEvent` for explicit GSM truncation
  markers with `data_loss=True`, `recoverable=False`, `value_source=observed`,
  `confidence=high`, `finality=live`, and
  `drift_flag=missing_expected_payload_path`.
- `TruncationEvent` is part of the public `GameEvent` union.
- `router.py` dispatches `EntryHeader.TRUNCATION_MARKER` to
  `parsers.truncation`.
- `golden_replay.py` includes diagnostics summary, truncation/data-loss, and
  unknown/degradation sections in observed fixture reports.
- `feature_equity_corpus_ratchet.py` counts unknown entries and truncation/data
  loss across explicit committed fixture manifests.

Observed risks:

- `diagnostics_status` can look like full parser correctness, but it is only a
  local report snapshot.
- `diagnostics_status=pass` can hide untested parser families, missing
  workbook verification, missing deployed Apps Script verification, or
  unverified production behavior.
- `unknown_entry_count=0` can look like no drift exists globally, but it only
  describes the analyzed input.
- `truncation_count=0` can look like proof no GameState data was lost, but it
  only means no truncation marker was observed in the analyzed input.
- `truncation_count>0` can look recoverable, but truncation markers are
  data-loss evidence and do not reconstruct omitted GameState payloads.
- Runtime status, webhook failures, workbook drift, and deployment drift can
  be confused with parser evidence drift if the ledger does not keep the
  surfaces separate.

## Scope Decision

Codex C should implement issue #171 as a Tier 6
`runtime_health_and_drift_detection` metadata slice in the existing evidence
ledger.

Required family metadata:

- Change Tier 6 `runtime_health_and_drift_detection.status` from
  `registered_future` to `seeded_sample`.
- Add exactly these Tier 6 seed fields, in this order:
  - `diagnostics_status`
  - `unknown_entry_count`
  - `truncation_count`
- Remove those fields from Tier 6 `future_fields`.
- Keep Tier 6 `future_fields` empty after issue #171.
- Preserve all prior Tier 1, Tier 2, Tier 3, Tier 4, and Tier 5 seed fields and
  entries.
- Preserve Tier 7 `derived_analytics_outputs` as registered future work.
- Add notes stating that issue #171 maps runtime-health and drift provenance
  only and does not change diagnostics behavior, drift behavior, router
  semantics, truncation parsing, runtime status schema, replay behavior,
  feature-equity behavior, CI gates, merge/deploy policy, workbook sync,
  analytics, AI, or field-evidence attachment behavior.

Do not implement:

- diagnostics report shape changes
- log drift report behavior changes
- router behavior changes
- truncation parsing changes
- runtime status schema changes
- schema snapshot or invariant execution changes
- runtime field-evidence attachment
- golden replay behavior changes
- feature-equity behavior changes
- workbook, webhook, Apps Script, Match Journal, overlay, SQLite, or Google
  Sheets sync changes
- analytics, archetype, advice, AI, or model-provider behavior

## Required Entry Semantics

### `diagnostics_status`

Meaning:

- The advisory top-level parser diagnostics status for one generated
  diagnostics report snapshot.

Allowed values:

- `pass`
- `review`
- `fail`
- `unknown`

Primary source evidence:

- `parser_diagnostics.build_parser_diagnostics_report(...).overall_status`
- `summary.parser_status`
- `parser_health.status`
- section statuses that contribute to `_overall_status(...)`

Required policy:

- `value_source` should be `derived`.
- Confidence is high for a successfully generated diagnostics report from an
  explicit analyzed input, medium if optional runtime status or baseline inputs
  are malformed or unavailable, low/review if parser/router failures or
  unknown-heavy evidence are present, and unknown for unreadable source or
  invalid profile failures.
- Finality describes the diagnostics report generation snapshot. It is not
  match/game final reconciliation.
- `diagnostics_status` must not become CI, merge, deploy, tracker completion,
  workbook, Apps Script, transport, production, analytics, or AI truth.

### `unknown_entry_count`

Meaning:

- The count of log entries that did not route to a parser event for one
  analyzed source log, fixture, or diagnostics run.

Primary source evidence:

- `parser_health.entry_counts.unknown`
- `summary.unknown_entries`
- `log_drift_sensor.build_player_log_drift_report(...).entry_counts.unknown`
- `RouterStats.unknown`

Fallback / review evidence:

- `unknowns_and_degradation.unknown_signatures`
- `top_unknown_signatures`
- `top_unmatched_api_names`
- `top_unmatched_request_api_names`
- `baseline_delta.new_unknown_signatures`
- golden replay `unknowns_and_degradation.unknown_entry_count`
- feature-equity `unknowns_and_degradation.unknown_entries`

Required policy:

- `value_source` should be `derived`.
- A numeric zero is valid only for the analyzed input. It is not a global
  no-drift claim.
- Missing, unreadable, malformed, or incomplete input must produce unknown or
  degraded provenance rather than silently becoming zero.
- Unknown signatures and unmatched API names are review samples. They are not
  trusted parser inputs and must not become parser truth.

### `truncation_count`

Meaning:

- The count of parser-observed GameState truncation/data-loss markers for one
  analyzed source log, fixture, or diagnostics run.

Primary source evidence:

- `truncation_and_data_loss.truncation_count`
- `summary.truncation_events`
- count of routed `TruncationEvent` instances
- `TruncationEvent.payload.type == "game_state_message_truncation"`
- `TruncationEvent.payload.data_loss is True`
- `TruncationEvent.payload.recoverable is False`
- `TruncationEvent.payload.drift_flag == "missing_expected_payload_path"`

Fallback / review evidence:

- golden replay `truncation_and_data_loss.truncation_count`
- feature-equity `truncation_and_data_loss.truncation_events`
- feature-equity `data_loss_markers` and `fixtures_with_truncation`

Required policy:

- The event marker is observed evidence; the count is derived from observed
  events or diagnostics summaries.
- A numeric zero is valid only for the analyzed input. It does not prove Arena
  never omitted GameState data outside that input.
- A positive count proves data-loss markers were observed. It does not recover
  omitted GameState payloads, objects, annotations, zones, actions, timers, or
  hidden facts.
- Truncation/data-loss evidence can lower confidence for dependent parser facts
  where later field-evidence attachment exists, but issue #171 must not
  implement field-evidence attachment.

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| Diagnostics `overall_status` | Advisory status for one local diagnostics report. | Merge readiness, deploy readiness, full parser correctness, workbook truth, AI truth. | `derived` |
| Diagnostics `summary.parser_status` / `parser_health.status` | Parser-health section status for one run. | Transport/workbook/App Script health or gameplay fact correctness. | `derived` |
| Diagnostics `summary.unknown_entries` | Unknown count summarized from report entry counts. | Global no-drift state or safe parser coverage. | `derived` |
| Drift report `entry_counts.unknown` | Unknown routed-entry count for analyzed input. | Trusted parser input or semantic interpretation of unknown entries. | `derived` |
| Router `RouterStats.unknown` | Count of entries that routed to no event in one router pass. | Permanent Arena schema behavior or parser correctness. | `derived` |
| Unknown signatures / unmatched API names | Review samples for unknown/unmatched families. | New parser truth, gameplay facts, automatic issue creation. | review only |
| Diagnostics `truncation_and_data_loss.truncation_count` | Count of data-loss markers summarized in one diagnostics report. | Recovered GameState content. | `derived` |
| `TruncationEvent` | Observed data-loss marker and marker metadata. | Omitted objects, annotations, zones, actions, timers, winners, hidden cards. | `observed` event evidence |
| Runtime status parser/router failure counters | Optional local operational evidence. | Parser truth, runtime status schema migration, workbook truth. | operational fallback |
| Golden replay reports | Fixture validation of unknown/truncation evidence. | Runtime truth, global coverage, parser semantics. | validation consumer |
| Feature-equity reports | Corpus count-shaped coverage evidence. | Parser truth, analytics truth, CI gate by itself. | validation consumer |
| Workbook, Apps Script, webhook, dashboards, Match Journal, overlays, SQLite, Google Sheets, analytics, AI | Downstream transport, storage, display, analysis, or explanation. | Parser evidence truth, diagnostics truth, merge/deploy readiness. | not source evidence |

## Value-Source, Confidence, Finality, And Degradation Rules

Value-source policy:

- `diagnostics_status`: `derived` from diagnostics report section statuses.
- `unknown_entry_count`: `derived` from router/drift counts.
- `truncation_count`: `derived` from observed `Truncation` events or
  diagnostics summaries.
- Missing or invalid inputs produce `unknown`.
- Contradictory report sections, malformed baselines, or inconsistent counts
  produce `conflict` or degraded review-required evidence.

Confidence policy:

- High confidence applies only to a successfully generated report over an
  explicit analyzed input with valid parser/drift surfaces.
- Medium confidence applies when optional fallback sources are used or when the
  report is valid but review context is incomplete.
- Low confidence applies when input was partial, malformed, unknown-heavy,
  baseline-malformed, timestamp-anomalous, or affected by parser/router
  failures.
- Unknown confidence applies when the source log is unreadable, the profile is
  invalid, the diagnostics report is malformed, or no trustworthy source exists.

Finality policy:

- Tier 6 finality describes a generated report snapshot.
- `live` may describe a currently running diagnostics or runtime status source.
- `provisional` may describe local runtime status or baseline fallback context.
- `final` may describe a completed diagnostics/drift report for the analyzed
  input.
- `reconciled` is reserved for future field-evidence records corrected by
  stronger later evidence. Issue #171 does not implement runtime
  field-evidence attachment.

Degradation behavior:

- Unreadable source log, non-file source, invalid profile, diagnostics replay
  failure, router exception, parser exception, malformed baseline, missing
  expected event families, new unknown signatures, new unmatched API names,
  timestamp parse failures, and truncation/data-loss markers must be visible
  as degraded or review-required evidence.
- Missing optional runtime status must not become a parser failure.
- Transport/webhook failure must remain transport evidence, not parser
  evidence drift.
- Workbook and Apps Script are not queried by diagnostics v1 and must not be
  inferred.
- Raw unknown entries, raw log excerpts, raw payloads, local paths, runtime
  artifacts, failed posts, workbook exports, secrets, tokens, and webhook URLs
  must not be serialized into ledger metadata.

## Required Invariants

Codex C should preserve or add tests for these invariants:

- Tier 6 status becomes `seeded_sample`.
- Tier 6 seed fields are exactly `diagnostics_status`,
  `unknown_entry_count`, and `truncation_count`.
- Tier 6 future fields are empty after issue #171.
- Required Tier 6 entries exist with the contracted entry IDs.
- No separate Tier 6 seed fields exist for diagnostics facets, transport
  status, workbook status, CI status, merge readiness, deploy readiness,
  analytics confidence, or AI confidence.
- `diagnostics_status` uses diagnostics report status fields and is advisory
  local evidence only.
- `unknown_entry_count` uses router/drift unknown counts and treats unknown
  signatures/API names as review samples only.
- `truncation_count` uses observed `Truncation` events or diagnostics
  truncation summaries and states that missing GameState data is not
  reconstructed.
- Golden replay and feature-equity reports remain validation/report consumers,
  not truth owners.
- Built-in ledger and entries validate cleanly.
- Privacy validation remains path-only/no-values and rejects raw-log-like text,
  absolute local paths, secrets, webhook URLs, and token-shaped text.

Recommended invariant names:

- `tier6_diagnostics_status_is_advisory_report_status`
- `tier6_diagnostics_status_not_merge_deploy_ci_or_ai_truth`
- `tier6_unknown_entry_count_is_run_scoped`
- `tier6_unknown_entries_are_review_samples_not_parser_truth`
- `tier6_truncation_count_is_data_loss_marker_count`
- `tier6_truncation_count_does_not_reconstruct_game_state`
- `tier6_transport_workbook_deployment_ai_are_downstream_only`
- `tier6_golden_replay_and_feature_equity_are_validation_consumers`
- `tier6_privacy_path_only_no_values`

## Protected Surfaces

Do not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- truncation parser behavior
- diagnostics report shape
- runtime status file schema
- drift report implementation
- schema snapshots
- invariant execution
- golden replay behavior
- feature-equity behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- ActionLogRow shape
- match identity
- game identity
- deduplication
- Match Journal behavior
- overlay behavior
- SQLite behavior
- Google Sheets sync behavior
- production behavior
- analytics truth
- AI truth
- OpenAI or model-provider behavior
- archetype classification behavior
- CI gates
- merge/deploy policy
- secrets, environment variables, API keys, tokens, credentials, or webhook URLs
- raw private Player.log excerpts
- generated card data
- local runtime artifacts
- runtime status files
- failed posts
- workbook exports

Do not reconstruct missing GameState data, infer hidden cards, complete
decklists, classify archetypes, provide gameplay advice, label player mistakes,
or move analytics/AI truth into parser truth.

## Side Effects

Allowed for Codex C:

- Update `src/mythic_edge_parser/app/evidence_ledger.py` metadata entries and
  family notes for Tier 6.
- Update `tests/test_evidence_ledger.py` focused metadata tests.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md`.

Forbidden for Codex C:

- Changing diagnostics, drift, router, truncation, runtime, replay, or
  feature-equity behavior.
- Adding new runtime artifacts.
- Adding schema snapshots or invariant execution.
- Reading, copying, summarizing, or committing raw private logs.
- Adding raw unknown signatures, raw log excerpts, payload values, local paths,
  runtime status files, failed posts, workbook exports, tokens, credentials,
  webhook URLs, or generated data to the ledger.
- Adding workbook/webhook/App Script fields.
- Adding CI, merge, deploy, analytics, or AI gates.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 6 family status is `seeded_sample`.
- Tier 6 seed fields are exactly the three contracted fields.
- Tier 6 future fields are empty.
- The three required entry IDs are present.
- Each Tier 6 entry has `output_family == "runtime_health_and_drift_detection"`.
- `diagnostics_status` references `parser_diagnostics.overall_status`,
  `summary.parser_status`, and `parser_health.status`.
- `diagnostics_status` invariant/degradation notes reject merge readiness,
  deploy readiness, CI truth, workbook truth, transport truth, analytics truth,
  and AI truth.
- `unknown_entry_count` references diagnostics summary, drift report
  `entry_counts.unknown`, and `RouterStats.unknown`.
- `unknown_entry_count` notes that zero is scoped to the analyzed input and
  unknown signatures/API names are review samples only.
- `truncation_count` references diagnostics truncation summary and
  `TruncationEvent` payload evidence.
- `truncation_count` notes that truncation markers do not reconstruct missing
  GameState data.
- Golden replay and feature-equity report paths are documented as
  validation/report consumers only.
- No forbidden Tier 6 fields are seeded.
- Built-in ledger and entries validate cleanly.
- Privacy validation remains path-only/no-values.

Recommended focused validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m ruff check src tests tools
git diff --check
```

Protected-surface validation when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md
EOF
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
EOF
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
  exists.
- The contract explicitly authorizes seeding the three Tier 6 fields and no
  others.
- The contract defines exact entry IDs, source evidence, fallback evidence,
  value-source policy, confidence policy, finality policy, degradation
  behavior, invariants, protected surfaces, and validation expectations.
- The contract keeps diagnostics status advisory/local and not merge, deploy,
  CI, workbook, parser-truth, analytics, or AI authority.
- The contract keeps unknown entries as drift/review signals, not trusted
  parser inputs.
- The contract keeps truncation markers as observed data-loss evidence, not
  recovered GameState data.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- Future runtime field-evidence attachment may need to connect Tier 6
  degradation labels to specific match/game/card fields. Issue #171 does not
  implement that link.
- Future drift-report work may add a dedicated `drift_report.py` logical
  module from the broad #11 contract. Issue #171 only maps existing
  diagnostics/drift surfaces.
- Future schema snapshot and invariant execution work may depend on Tier 6
  evidence, but this contract does not implement snapshots or invariants.
- Future Tier 7 analytics contracts must decide how to consume Tier 6 health
  without turning it into analytics truth.
- Diagnostics currently treats some report statuses as advisory local labels.
  This contract preserves that behavior rather than escalating diagnostics to
  a CI or deploy gate.

## Suspected Gaps

- Tier 6 family notes currently only say the family is registered for later
  mapping.
- Existing evidence-ledger tests currently expect Tier 6 to remain
  `registered_future`.
- The evidence ledger does not yet have entries for diagnostics status,
  unknown-entry count, or truncation count.
- Existing diagnostics, drift, truncation, replay, and feature-equity tests
  validate behavior, but evidence-ledger tests do not yet assert their
  provenance boundaries.
- Runtime field-evidence attachment remains deferred, so Tier 6 degradation
  does not yet automatically annotate individual parser-owned fields.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #171, Tier 6 runtime health and drift provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/171
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/169
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/170
- Previous merge commit: 5f242c07b2418c6d27d1e4670f19a81785546c27
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 6 runtime health and drift contract. Implement only the smallest coherent metadata/test changes needed to seed diagnostics_status, unknown_entry_count, and truncation_count provenance.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Change Tier 6 runtime_health_and_drift_detection from registered_future to seeded_sample.
- Add exactly these Tier 6 seed fields: diagnostics_status, unknown_entry_count, truncation_count.
- Keep Tier 6 future_fields empty after seeding.
- Add exactly these entry IDs:
  - tier6.runtime_health_and_drift_detection.diagnostics_status
  - tier6.runtime_health_and_drift_detection.unknown_entry_count
  - tier6.runtime_health_and_drift_detection.truncation_count
- Preserve existing Tier 1, Tier 2, Tier 3, Tier 4, Tier 5, and Tier 7 metadata and entries.
- Add focused tests in tests/test_evidence_ledger.py proving the Tier 6 fields, source paths, invariants, degradation behavior, privacy posture, and protected downstream boundaries.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, truncation parser behavior, diagnostics report shape, runtime status file schema, drift report implementation, schema snapshots, invariant execution, golden replay behavior, feature-equity behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, archetype classification behavior, CI gates, merge/deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not reconstruct missing GameState data, infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move analytics/AI truth into parser truth.
- Do not commit raw private Player.log excerpts, raw unknown signatures from private logs, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, evidence_ledger.py, tests/test_evidence_ledger.py, and the implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/171"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/169"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/170"
  previous_merge_commit: "5f242c07b2418c6d27d1e4670f19a81785546c27"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier6_runtime_health_drift_comparison.md"
  verdict: "tier6_runtime_health_drift_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier6-runtime-health-drift"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, truncation parser behavior, diagnostics report shape, runtime status file schema, drift report implementation, schema snapshots, invariant execution, golden replay behavior, feature-equity behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, archetype classification behavior, CI gates, merge/deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not add Tier 6 seed fields beyond diagnostics_status, unknown_entry_count, and truncation_count."
    - "Do not reconstruct missing GameState data, infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move analytics/AI truth into parser truth."
    - "Do not commit raw private Player.log excerpts, raw unknown signatures from private logs, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
```
