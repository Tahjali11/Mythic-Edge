# Player.log Evidence Ledger Tier 7 Derived Analytics Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/173
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/171
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/172
- previous_merge_commit: d084512bab464bf5566a84e5dd807a2c6c07b861
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier7-derived-analytics
- target_artifact: docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_sheet_exports.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #173 maps Tier 7 derived analytics output provenance in the Player.log
evidence ledger.

The fields in scope are exactly:

- `card_performance`
- `feature_equity_counts`

These are parser-adjacent derived analytics and reporting outputs. They are not
match facts, game facts, card identity truth, gameplay-action truth, opponent
deck truth, merge readiness, deploy readiness, CI truth, workbook truth, Apps
Script truth, coaching truth, model-provider truth, or AI truth.

Plain English: Mythic Edge can say "this card-performance report was derived
from these local match-history/action/card-identity ingredients" and "this
feature-equity count report was derived from these committed sanitized or
synthetic corpus manifests." It must not say that a win-rate metric is a parser
fact, that feature-equity status proves semantic correctness, that an analytics
report authorizes a protected-surface change, or that AI advice owns the
underlying truth.

This contract documents provenance metadata only. It must not change card
performance calculations, feature-equity behavior, golden replay behavior,
diagnostics behavior, drift behavior, parser behavior, workbook schema, webhook
payload shape, Apps Script behavior, output transport, runtime artifacts, Match
Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync
behavior, analytics truth, AI truth, or model-provider behavior.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
allowed `value_source`, `confidence`, `finality`, invariant, drift, and
privacy labels.

Tier 7 entries use the existing ledger field `parser_managed_truth` because the
current schema requires every ledger entry to validate that flag as true. For
Tier 7, that flag means "the local Mythic Edge codebase owns this report's
metadata provenance boundary." It does not mean card-performance metrics or
feature-equity counts are parser-owned match/game facts. Codex C must add
explicit notes and invariants to prevent this schema term from being read as
analytics truth.

`docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`,
`docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`, and
`docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
remain authoritative for card identity, gameplay-action, and visible
opponent-card observation provenance. Tier 7 consumes those facts as
ingredients and must not redefine them.

`docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md`
remains authoritative for diagnostics status, unknown-entry count, and
truncation count. Tier 7 consumes Tier 6 health and degradation context only as
qualification evidence.

`docs/contracts/parser_feature_equity_corpus_ratchet.md` remains authoritative
for the report-only corpus ratchet, count sections, baseline comparison,
privacy posture, limitations, and the rule that feature-equity counts are not
semantic correctness or merge readiness.

`docs/contracts/parser_golden_replay_harness.md` remains authoritative for
golden replay fixture acceptance, manifest safety, report statuses, and
parser-owned observed output comparison. Tier 7 consumes golden replay reports
as fixture/corpus evidence only.

`docs/contracts/parser_sheet_exports.md` remains authoritative for how current
card-performance payload fields are shaped for sheet export. Issue #173 must
not change those fields, workbook schema, Apps Script mappings, or output
transport.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #173 provenance should be
recorded through this contract, implementation handoff, family notes, entry
notes, and focused tests rather than by changing the top-level ledger object
shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata for derived
analytics outputs.

Truth boundary:

- `src/mythic_edge_parser/app/card_performance.py` owns local derived
  card-performance report generation from match history, local action
  artifacts, and card identity lookup.
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py` owns
  count-only feature-equity corpus reporting from committed sanitized or
  synthetic golden replay manifests and reviewed baselines.
- `src/mythic_edge_parser/app/golden_replay.py` owns fixture replay reports
  used by feature-equity counts.
- Tier 1 through Tier 6 evidence-ledger entries describe ingredient facts and
  health/degradation context consumed by Tier 7.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence, finality, degradation behavior, drift flags, invariants, and
  protected boundary notes.
- Parser state remains the owner of parser facts.
- Workbook formulas, dashboards, webhook transport, Apps Script, Match Journal,
  overlays, SQLite, Google Sheets sync, external metagame data, archetype
  classification, OpenAI/model-provider output, and AI output are downstream
  consumers, enrichment, or explanation surfaces only.

The evidence ledger must not become a second analytics engine, a second card
performance calculator, a feature-equity baseline updater, a semantic
correctness oracle, a schema snapshot generator, an invariant executor, a CI
gate, a merge/deploy gate, a workbook truth layer, a coaching layer, or an AI
truth layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier7_derived_analytics.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/card_performance.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_card_performance.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/test_golden_replay_harness.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_parser_diagnostics_mode.py
- tests/fixtures/golden_replay/
- tests/fixtures/feature_equity_corpus/

## Public Interface

This contract covers evidence-ledger metadata for existing derived analytics
and corpus-reporting surfaces. It does not create a new runtime API, parser
event, status file field, workbook column, webhook field, Apps Script field, or
CLI.

Required Tier 7 family transition:

- `derived_analytics_outputs.status` changes from `registered_future` to
  `seeded_sample`.
- `derived_analytics_outputs.seed_fields` becomes exactly:
  - `card_performance`
  - `feature_equity_counts`
- `derived_analytics_outputs.future_fields` becomes empty.
- No Tier 8 family is introduced.

Required Tier 7 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier7.derived_analytics_outputs.card_performance` | `card_performance` | `Card Performance` | `derived` |
| `tier7.derived_analytics_outputs.feature_equity_counts` | `feature_equity_counts` | `Feature-Equity Counts` | `derived` |

Existing report surfaces referenced by the entries:

| Existing surface | Relevant paths or fields |
| --- | --- |
| Card performance report | `object`, `generated_at`, `total_cards`, `total_games`, `baseline_game_win_rate`, `cards[]` |
| Card performance card rows | `card_key`, `grp_id`, `card_name`, `display_name`, `resolution_status`, `layout`, `card_faces`, `games_seen`, `seen_in_game_games`, `seen_in_game_win_rate`, `opening_hand_games`, `opening_hand_win_rate`, `cast_games`, `cast_win_rate`, `postboard_cast_games`, `postboard_cast_win_rate`, `mulliganed_away_games`, `mulliganed_away_win_rate`, `mulligan_tax`, `top_matchups`, `top_packages` |
| Match history artifact | `matches[]`, `match_id`, `games[]`, `game_number`, `result`, `opening_hand`, `mulliganed_away`, `opponent_archetype`, `opponent_variant` |
| Gameplay-action artifacts | `object`, `match_id`, `entries[]`, `game_number`, `action_type`, `grp_id`, `card_name`, `display_name`, `resolution_status`, `actor_relation` |
| Card identity lookup | `grp_id`, `resolved_name`, `display_name`, `resolution_status`, `resolved_layout`, `resolved_card_faces` |
| Feature-equity report | `object`, `schema_version`, `status`, `status_reasons`, `inputs`, `baseline`, `observed`, `comparison`, `privacy`, `protected_surfaces`, `limitations` |
| Feature-equity observed count sections | `input_counts`, `router_stats`, `event_family_counts`, `event_kind_counts`, `payload_type_counts`, `parser_claim_counts`, `game_state_evidence_counts`, `truncation_and_data_loss`, `unknowns_and_degradation` |
| Golden replay reports | fixture status, router stats, event-family counts, diagnostics summary, truncation/data-loss, unknowns/degradation, parser-owned observed outputs |
| Tier 6 runtime health | `diagnostics_status`, `unknown_entry_count`, `truncation_count` |

Fields and facets not authorized as separate Tier 7 seed fields in issue #173:

- `seen_win_rate`
- `opening_hand_win_rate`
- `cast_win_rate`
- `postboard_cast_win_rate`
- `mulligan_tax`
- `top_matchups`
- `top_packages`
- `baseline_game_win_rate`
- `total_cards`
- `total_games`
- `feature_equity_status`
- `feature_equity_status_reasons`
- `feature_equity_baseline_status`
- `fixture_pass_rate`
- `event_family_counts`
- `parser_claim_counts`
- `semantic_correctness`
- `merge_readiness`
- `deploy_readiness`
- `ci_status`
- `workbook_status`
- `ai_confidence`
- `sideboarding_recommendations`
- `matchup_notes`
- `gameplay_advice`
- `player_mistake_labels`

Those values may appear as facets, source evidence, degradation reasons,
downstream display fields, or future analytics contracts only.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`d084512bab464bf5566a84e5dd807a2c6c07b861`:

- Issue #171 / PR #172 is deployed.
- Tracker #11 remains open.
- Tier 7 `derived_analytics_outputs` is `registered_future`.
- Tier 7 future fields are:
  - `card_performance`
  - `feature_equity_counts`
- Tier 7 seed fields are empty.
- Tier 6 `runtime_health_and_drift_detection` is `seeded_sample`.
- `card_performance.refresh_card_performance_artifacts(...)` reads local match
  history and local action artifacts, aggregates card-level metrics, writes a
  JSON payload and Markdown summary, and returns the payload.
- `card_performance.load_card_performance_payload(...)` returns a blank
  `manasight_card_performance` payload when no JSON payload exists.
- Card-performance output currently uses object string
  `manasight_card_performance`.
- Card-performance card rows include rates and counts for seen-in-game,
  opening hand, casting, postboard casting, mulliganed-away games, matchup
  buckets, and package co-occurrence.
- Card-performance aggregation filters gameplay actions to local actor
  relation only.
- Card-performance card identity can come from direct `grp_id`, catalog
  name lookup, or display/name fallback.
- Feature-equity corpus ratchet output currently uses object
  `mythic_edge_feature_equity_corpus_ratchet_report` and schema version
  `parser_feature_equity_corpus_ratchet_report.v1`.
- Feature-equity corpus ratchet status values are `ok`, `review`, `diff`, and
  `fail`.
- Feature-equity count sections are count-shaped and report-only.
- Missing feature-equity baseline is `review`, not `ok`.
- Baseline count mismatch is `diff` and report-only.
- Private/unapproved fixture metadata is `fail` without copying raw fixture
  content.
- Feature-equity reports include protected-surface booleans and limitations
  stating the report does not decide semantic correctness, baseline updates,
  merge readiness, coaching quality, or AI analytics.

Observed risks:

- Card-performance rates can look like parser facts even though they are
  derived metrics over a local input set.
- `top_matchups` can look like archetype truth even though it comes from local
  match-history labels such as `opponent_archetype` or `opponent_variant`.
- `top_packages` can look like deck-synergy truth even though it is local
  co-occurrence over observed/opening/seen cards.
- Unresolved, name-only, degraded, or truncation-affected ingredients can be
  hidden if the ledger does not require confidence/degradation notes.
- `feature_equity_counts.status == ok` can look like semantic correctness,
  CI readiness, merge readiness, deploy readiness, or proof of no drift.
- Zero counts in feature-equity or card-performance reports can look global
  rather than scoped to the analyzed corpus or local report input set.
- AI/model-provider summaries could repackage analytics as advice unless the
  boundary is explicit.

## Scope Decision

Codex C should implement issue #173 as a Tier 7 `derived_analytics_outputs`
metadata slice in the existing evidence ledger.

Required family metadata:

- Change Tier 7 `derived_analytics_outputs.status` from `registered_future` to
  `seeded_sample`.
- Add exactly these Tier 7 seed fields, in this order:
  - `card_performance`
  - `feature_equity_counts`
- Remove those fields from Tier 7 `future_fields`.
- Keep Tier 7 `future_fields` empty after issue #173.
- Preserve all prior Tier 1, Tier 2, Tier 3, Tier 4, Tier 5, and Tier 6 seed
  fields and entries.
- Add notes stating that issue #173 maps derived analytics provenance only and
  does not change card-performance calculations, feature-equity behavior,
  golden replay behavior, diagnostics behavior, drift behavior, parser
  behavior, runtime artifacts, workbook sync, analytics truth, AI, CI gates,
  merge/deploy policy, or field-evidence attachment behavior.

Do not implement:

- card-performance calculation changes
- feature-equity report behavior changes
- golden replay behavior changes
- diagnostics or drift report behavior changes
- runtime artifact shape changes
- schema snapshot or invariant execution changes
- runtime field-evidence attachment
- workbook, webhook, Apps Script, Match Journal, overlay, SQLite, or Google
  Sheets sync changes
- analytics recommendation logic
- archetype classification logic
- coaching, advice, player-mistake, AI, or model-provider behavior

## Required Entry Semantics

### `card_performance`

Meaning:

- A broad local derived analytics report describing card-level metrics from
  local match history, local gameplay-action artifacts, and card identity
  lookup.

Facets covered by the broad entry:

- report metadata: `object`, `generated_at`, `total_cards`, `total_games`,
  `baseline_game_win_rate`
- card identity/display facets: `card_key`, `grp_id`, `card_name`,
  `display_name`, `resolution_status`, `layout`, `card_faces`
- local count/rate facets: `games_seen`, `seen_in_game_games`,
  `seen_in_game_win_rate`, `opening_hand_games`, `opening_hand_win_rate`,
  `cast_games`, `cast_win_rate`, `postboard_cast_games`,
  `postboard_cast_win_rate`, `mulliganed_away_games`,
  `mulliganed_away_win_rate`, `mulligan_tax`
- local co-occurrence/display facets: `top_matchups`, `top_packages`

Primary source evidence:

- `card_performance.refresh_card_performance_artifacts(...)`
- `card_performance.load_card_performance_payload(...)`
- local match history payload at the configured match-history path
- local gameplay-action payloads under the configured action-artifact root
- Tier 3 game result, opening-hand, mulligan, pre/postboard, and game-number
  provenance
- Tier 5 card identity and gameplay-action provenance
- Tier 6 diagnostics, unknown-entry, and truncation/data-loss context

Fallback / review evidence:

- catalog name lookup from `grp_id_catalog`
- name-only card identity fallback
- display-name fallback for unresolved gameplay-action entries
- missing or invalid match-history/action artifacts
- degraded gameplay-action actor relation, resolution status, or card identity
- local runtime artifact absence

Required policy:

- `value_source` should be `derived`.
- The broad entry may reference direct evidence from `card_performance.py` and
  fallback evidence from match history, gameplay-action artifacts, and card
  identity lookup.
- High confidence applies only to metrics whose required ingredients are
  present, locally scoped, and not degraded.
- Medium or low confidence applies when the report uses name-only identity,
  unresolved display fallback, incomplete match history, missing action
  artifacts, degraded actor relation, truncation/data-loss context, or
  unknown-entry context.
- A zero count or empty rate is valid only for the local report input set. It
  is not a global claim about the deck, format, metagame, or MTGA logs.
- `top_matchups` and `top_packages` are local derived facets. They must not
  become archetype truth, deck-construction truth, sideboarding advice, matchup
  plans, or AI truth.
- Card-performance output must not overwrite parser-owned card identity,
  gameplay-action, match, game, or result facts.

### `feature_equity_counts`

Meaning:

- A broad report-only corpus-count surface that summarizes explicit committed
  sanitized or synthetic golden replay manifests and compares count-shaped
  observations to a reviewed baseline.

Facets covered by the broad entry:

- report metadata: `object`, `schema_version`, `status`, `status_reasons`
- inputs: manifest paths, manifest count, source file count, source file paths,
  input kind, directory expansion, ordering
- baseline metadata and validation errors
- observed count sections: `input_counts`, `router_stats`,
  `event_family_counts`, `event_kind_counts`, `payload_type_counts`,
  `parser_claim_counts`, `game_state_evidence_counts`,
  `truncation_and_data_loss`, `unknowns_and_degradation`
- comparison metadata: matching sections, diff sections, review sections,
  missing expected sections, unexpected observed sections, count diffs
- privacy, protected-surface, and limitations sections

Primary source evidence:

- `feature_equity_corpus_ratchet.build_feature_equity_corpus_report(...)`
- explicit golden replay manifest paths
- committed sanitized or synthetic fixture metadata
- `golden_replay.run_golden_replay(...)` fixture reports
- router stats collected by replaying committed fixture slices
- parser event family/kind counts
- payload type counts
- parser claim counts
- GameState evidence counts
- truncation/data-loss counts
- unknown/degradation counts
- manually reviewed baseline payloads

Fallback / review evidence:

- missing baseline (`review`)
- malformed or unreadable baseline (`fail`)
- baseline count diffs (`diff`)
- golden replay `review`, `degraded`, `diff`, or `fail`
- unknown entries, timestamp anomalies, truncation/data-loss markers, degraded
  parser outputs, missing expected sections, unexpected observed sections, and
  privacy validation findings

Required policy:

- `value_source` should be `derived`.
- Feature-equity counts are count-shaped corpus evidence only.
- High confidence applies only to an explicit committed sanitized/synthetic
  corpus with a loaded reviewed baseline and no unexpected diffs.
- Medium confidence applies to `review` status, missing baseline, expected
  degraded fixtures, or incomplete but safe count sections.
- Low confidence applies to `diff` or `fail` status, malformed baseline,
  unapproved fixture privacy metadata, unknown-heavy input, or golden replay
  failures.
- A zero count is scoped to the analyzed corpus and baseline. It does not prove
  that a parser family never appears in live MTGA logs or that no drift exists.
- `status == ok` does not prove semantic parser correctness, merge readiness,
  deploy readiness, CI truth, workbook truth, or AI truth.
- Baseline updates must remain manual/reviewed and are not authorized by this
  evidence-ledger slice.

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| Card-performance payload | Local derived card metric report for the loaded match/action input set. | Parser-owned match/game truth, global deck performance, advice, AI truth. | `derived` |
| Match history artifact | Local report ingredient for games, results, opening hands, mulligans, and labels. | Raw Player.log proof by itself, workbook truth, external metagame truth. | ingredient |
| Gameplay-action artifact | Local action ingredient for seen/cast/postboard metrics. | Hidden-card truth, advice, independent action parser truth. | ingredient |
| GRP/catalog lookup | Card display/name enrichment and identity qualification. | Parser-owned card identity truth when upstream evidence is missing or contradicted. | fallback/enrichment |
| Tier 5 provenance | Card identity/action/observation confidence and degradation context. | Derived analytics correctness by itself. | dependency |
| Tier 6 provenance | Diagnostics, unknown, and truncation context for the analyzed run/corpus. | Global parser health, merge readiness, deploy readiness, CI truth. | dependency |
| Feature-equity report | Count-shaped coverage evidence over explicit committed manifests. | Semantic correctness, no global drift, baseline blessing, merge/deploy readiness. | `derived` |
| Golden replay report | Fixture-level observed parser output and replay status. | Runtime truth, global coverage, workbook/App Script truth. | validation consumer |
| Feature-equity baseline | Reviewed expected count shape for a corpus snapshot. | Authorization to change parser behavior or auto-bless diffs. | review baseline |
| Workbook, Apps Script, webhook, dashboards, Match Journal, overlays, SQLite, Google Sheets, analytics, AI | Downstream display, transport, storage, analysis, or explanation. | Parser evidence truth, analytics source truth, merge/deploy readiness. | not source evidence |

## Value-Source, Confidence, Finality, Drift, And Degradation Rules

Value-source policy:

- `card_performance`: `derived` from local report ingredients.
- `feature_equity_counts`: `derived` from explicit committed corpus and
  baseline/report evidence.
- Missing source artifacts produce `unknown` or degraded provenance, not clean
  zeros.
- Contradictory ingredient evidence, baseline diffs, malformed baselines, or
  incompatible section counts produce `conflict` or degraded review-required
  evidence.

Confidence policy:

- High confidence applies only to a successfully generated local report whose
  required ingredients are present and not degraded for the analyzed input set.
- Medium confidence applies when optional fallback sources are used or when
  the report is valid but contains review context such as missing baseline,
  name-only identity, expected degradation, or incomplete local artifacts.
- Low confidence applies when inputs are partial, malformed, unknown-heavy,
  baseline-diffed, truncation-affected, privacy-failed, or affected by replay,
  parser, router, or artifact failures.
- Unknown confidence applies when no trustworthy report, artifact, corpus, or
  baseline source exists.

Finality policy:

- Tier 7 finality describes a generated analytics/report snapshot.
- `live` may describe local runtime artifacts that are still changing.
- `provisional` may describe reports generated from incomplete or actively
  changing local runtime inputs.
- `final` may describe a completed report over an explicit input set at a
  given commit or local snapshot.
- `reconciled` is reserved for future field-evidence records corrected by
  stronger later evidence. Issue #173 does not implement runtime
  field-evidence attachment.

Drift policy:

- Feature-equity count diffs, missing expected sections, unexpected observed
  sections, new unknown entries, payload-path changes, and baseline validation
  failures should be represented through existing drift flags such as
  `missing_expected_event_family`, `missing_expected_payload_path`,
  `changed_signal_type`, `new_unknown_event_family`,
  `new_unknown_payload_path`, `fixture_gap`, `schema_snapshot_missing`,
  `parser_exception`, `invariant_failed`, and
  `sensitive_evidence_redacted` where applicable.
- Card-performance degradation caused by missing local artifacts, unresolved
  card identity, weak actor filtering, or truncation/unknown context should use
  existing fallback/degradation vocabulary rather than adding analytics-only
  truth labels.

Degradation behavior:

- Missing match history, missing action artifacts, invalid JSON, non-dict
  payloads, unresolved card identity, name-only identity, missing local actor
  relation, unknown/degraded parser inputs, and truncation/data-loss context
  must qualify card-performance provenance.
- Missing feature-equity baseline must remain `review`.
- Baseline count mismatch must remain `diff` and report-only.
- Malformed baseline, unapproved private fixture metadata, golden replay
  failure, privacy validation failure, and unreadable committed fixture inputs
  must degrade or fail feature-equity provenance.
- Missing optional runtime card-performance artifacts must not become parser
  failure.
- Workbook, webhook, Apps Script, and AI failures must remain downstream or
  external-surface evidence, not parser or Tier 7 source truth.
- Raw private logs, raw payload values, local absolute paths, runtime status
  files, failed posts, workbook exports, generated data, secrets, tokens,
  credentials, webhook URLs, and raw local analytics artifacts must not be
  serialized into ledger metadata.

## Required Invariants

Codex C should preserve or add tests for these invariants:

- Tier 7 status becomes `seeded_sample`.
- Tier 7 seed fields are exactly `card_performance` and
  `feature_equity_counts`.
- Tier 7 future fields are empty after issue #173.
- Required Tier 7 entries exist with the contracted entry IDs.
- No separate Tier 7 seed fields exist for card-performance submetrics,
  feature-equity subcounts, sideboarding recommendations, matchup notes,
  gameplay advice, player-mistake labels, merge readiness, deploy readiness,
  CI truth, workbook truth, analytics confidence, or AI confidence.
- `parser_managed_truth` on Tier 7 entries means local code/report provenance
  ownership only; it must not be read as parser-owned match/game/card/action
  fact truth.
- `card_performance` uses card-performance report surfaces and upstream
  ingredient provenance, and remains local derived analytics only.
- Card-performance metric zeros, empty rates, top matchups, and top packages
  are scoped to the local analyzed input set and are not global or strategic
  claims.
- `feature_equity_counts` uses feature-equity report, golden replay, count
  sections, and reviewed baseline evidence, and remains report-only.
- `feature_equity_counts.status == ok` is not semantic correctness, CI,
  merge, deploy, workbook, Apps Script, analytics, model-provider, or AI truth.
- Golden replay, diagnostics, and Tier 1-6 entries remain ingredient,
  validation, or qualification sources, not Tier 7 truth owners.
- Built-in ledger and entries validate cleanly.
- Privacy validation remains path-only/no-values and rejects raw-log-like text,
  absolute local paths, secrets, webhook URLs, and token-shaped text.

Recommended invariant names:

- `tier7_derived_analytics_status_is_seeded_sample`
- `tier7_seed_fields_are_broad_analytics_entries`
- `tier7_no_metric_subfields_seeded`
- `tier7_parser_managed_truth_means_report_metadata_not_parser_fact_truth`
- `tier7_card_performance_is_local_derived_analytics`
- `tier7_card_performance_metrics_are_input_scoped`
- `tier7_card_performance_top_matchups_are_not_archetype_truth`
- `tier7_card_performance_top_packages_are_not_deckbuilding_advice`
- `tier7_feature_equity_counts_are_report_only`
- `tier7_feature_equity_ok_is_not_semantic_correctness_or_merge_readiness`
- `tier7_feature_equity_counts_are_corpus_scoped`
- `tier7_ai_and_model_provider_output_are_downstream_only`
- `tier7_privacy_path_only_no_values`

## Protected Surfaces

Do not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- diagnostics report shape
- runtime status schema
- drift report implementation
- schema snapshots
- invariant execution
- golden replay behavior
- feature-equity behavior
- card-performance calculations
- card-performance artifact shape
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

Do not infer hidden cards, complete decklists, classify archetypes, provide
gameplay advice, create sideboarding recommendations, label player mistakes,
or move analytics/AI truth into parser truth.

## Side Effects

Allowed for Codex C:

- Update `src/mythic_edge_parser/app/evidence_ledger.py` metadata entries and
  family notes for Tier 7.
- Update `tests/test_evidence_ledger.py` focused metadata tests.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md`.

Forbidden for Codex C:

- Changing card-performance calculations, report object names, generated
  artifact shape, or sheet export behavior.
- Changing feature-equity report behavior, baseline behavior, count sections,
  CLI exit behavior, privacy policy, or protected-surface section.
- Changing golden replay, diagnostics, drift, router, parser, runtime,
  workbook, webhook, Apps Script, Match Journal, overlay, SQLite, Google
  Sheets sync, analytics, or AI behavior.
- Adding new runtime artifacts.
- Adding schema snapshots or invariant execution.
- Reading, copying, summarizing, or committing raw private logs.
- Adding raw local card-performance artifacts, raw logs, payload values, local
  paths, runtime status files, failed posts, workbook exports, tokens,
  credentials, webhook URLs, or generated data to the ledger.
- Adding workbook/webhook/App Script fields.
- Adding CI, merge, deploy, analytics, coaching, or AI gates.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 7 family status is `seeded_sample`.
- Tier 7 seed fields are exactly the two contracted fields.
- Tier 7 future fields are empty.
- The two required entry IDs are present.
- Each Tier 7 entry has `output_family == "derived_analytics_outputs"`.
- `card_performance` references card-performance report fields, match history
  artifacts, gameplay-action artifacts, card identity lookup, Tier 5
  provenance, and Tier 6 degradation context.
- `card_performance` invariant/degradation notes reject parser fact truth,
  global performance truth, archetype truth, deckbuilding truth, gameplay
  advice, player-mistake labels, workbook truth, analytics truth, and AI truth.
- `card_performance` notes that zeros, empty rates, top matchups, and top
  packages are scoped to the local analyzed input set.
- `feature_equity_counts` references feature-equity report fields, count
  sections, golden replay reports, manifest privacy, baseline comparison, and
  Tier 6 degradation context.
- `feature_equity_counts` notes that `ok` status is not semantic correctness,
  no-drift proof, CI truth, merge readiness, deploy readiness, workbook truth,
  analytics truth, or AI truth.
- No forbidden Tier 7 fields are seeded.
- Built-in ledger and entries validate cleanly.
- Privacy validation remains path-only/no-values.

Recommended focused validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py
python3 -m ruff check src tests tools
git diff --check
```

Protected-surface validation when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md
EOF
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
EOF
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md`
  exists.
- The contract explicitly authorizes seeding the two Tier 7 fields and no
  others.
- The contract defines exact entry IDs, source evidence, fallback evidence,
  value-source policy, confidence policy, finality policy, drift policy,
  degradation behavior, invariants, protected surfaces, and validation
  expectations.
- The contract keeps card performance as local derived analytics, not parser
  fact truth, global deck truth, archetype truth, advice, or AI truth.
- The contract keeps feature-equity counts as report-only corpus evidence, not
  semantic correctness, no-drift proof, merge readiness, deploy readiness, CI
  truth, workbook truth, analytics truth, or AI truth.
- The contract explains the current `parser_managed_truth` schema tension and
  preserves the boundary through explicit notes and invariants.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- The current ledger schema requires `parser_managed_truth` to be true for all
  entries. This contract keeps implementation narrow by documenting Tier 7
  local report/provenance ownership, but a future schema v2 may want a clearer
  field name for downstream analytics entries.
- Card-performance payloads currently use object string
  `manasight_card_performance`. This contract documents observed behavior and
  does not rename the object.
- Card-performance does not yet expose per-metric ingredient confidence inside
  the report payload. Issue #173 maps ledger metadata only and does not add
  runtime field-evidence attachment.
- Feature-equity count diffs remain report-only. A future governance issue
  could decide whether any subset becomes a CI gate, but issue #173 does not
  authorize that.
- Future AI/analytics contracts must decide how to consume Tier 7 without
  turning it into advice or model-provider truth.

## Suspected Gaps

- Tier 7 family notes currently only say the family is registered as future
  consumer metadata.
- Existing evidence-ledger tests currently expect Tier 7 to remain
  `registered_future`.
- The evidence ledger does not yet have entries for `card_performance` or
  `feature_equity_counts`.
- Existing card-performance tests validate aggregation behavior, but
  evidence-ledger tests do not yet assert derived-analytics boundaries.
- Existing feature-equity tests validate report behavior, privacy posture, and
  baseline handling, but evidence-ledger tests do not yet assert its
  provenance boundaries.
- Runtime field-evidence attachment remains deferred, so Tier 7 degradation
  does not yet automatically annotate individual analytics facets.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #173, Tier 7 derived analytics provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/173
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/171
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/172
- Previous merge commit: d084512bab464bf5566a84e5dd807a2c6c07b861
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 7 derived analytics contract. Implement only the smallest coherent metadata/test changes needed to seed card_performance and feature_equity_counts provenance.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Change Tier 7 derived_analytics_outputs from registered_future to seeded_sample.
- Add exactly these Tier 7 seed fields: card_performance, feature_equity_counts.
- Keep Tier 7 future_fields empty after seeding.
- Add exactly these entry IDs:
  - tier7.derived_analytics_outputs.card_performance
  - tier7.derived_analytics_outputs.feature_equity_counts
- Preserve existing Tier 1, Tier 2, Tier 3, Tier 4, Tier 5, and Tier 6 metadata and entries.
- Keep Tier 7 entries broad; do not add separate seed fields for card-performance submetrics, feature-equity subcounts, sideboarding recommendations, matchup notes, gameplay advice, player-mistake labels, merge readiness, deploy readiness, CI truth, workbook truth, analytics confidence, or AI confidence.
- Add focused tests in tests/test_evidence_ledger.py proving the Tier 7 fields, source paths, invariants, degradation behavior, privacy posture, and protected downstream boundaries.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, schema snapshots, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, card-performance artifact shape, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, archetype classification behavior, CI gates, merge/deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth.
- Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_card_performance.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_gsm_truncation_parser.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, evidence_ledger.py, tests/test_evidence_ledger.py, and the implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/173"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/171"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/172"
  previous_merge_commit: "d084512bab464bf5566a84e5dd807a2c6c07b861"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier7_derived_analytics_comparison.md"
  verdict: "tier7_derived_analytics_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier7-derived-analytics"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, schema snapshots, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, card-performance artifact shape, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, archetype classification behavior, CI gates, merge/deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not add Tier 7 seed fields beyond card_performance and feature_equity_counts."
    - "Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth."
    - "Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
```
