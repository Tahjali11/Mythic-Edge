# Core Sanitized Parser-Fact Producer Boundary Contract

## Contract Status

```yaml
schema_version: core_sanitized_parser_fact_producer_boundary.v1
decision_status: contract_review_required
implementation_authorized: false
sqlite_access_authorized: false
private_dataset_access_authorized: false
package_generation_authorized: false
package_transfer_authorized: false
r_and_d_dataset_access_authorized: false
ready_for_codex_c: false
```

This is a Core Codex B contract-only artifact for issue
[Tahjali11/Mythic-Edge#731](https://github.com/Tahjali11/Mythic-Edge/issues/731).
It defines a possible future producer boundary. It does not authorize a source
database read, implementation, package generation, transfer, consumer access,
or downstream activation.

## Module

Future Core producer for an owner-controlled, sanitized, local-only
parser-fact research package.

## Source Issue And Cross-Repository Predecessor

- Core issue: <https://github.com/Tahjali11/Mythic-Edge/issues/731>
- R&D issue: <https://github.com/Tahjali11/Mythic-Edge-Research-and-Development/issues/21>
- R&D tracker: <https://github.com/Tahjali11/Mythic-Edge-Research-and-Development/issues/4>
- R&D merge commit: `951a9c11422758e76ac553a5ad466dafa40f0b05`
- R&D consumer contract:
  `docs/contracts/sanitized_parser_fact_access_current_evidence_gap_report.md`
- R&D consumer-contract blob:
  `c9469042fe5998f145804d65f5dc13fd74777a58`
- R&D review-report blob:
  `26ae6d0bf0adc4836595ebf1ea5bacdd2663dad2`
- Issue-preflight Core source commit:
  `ea7bda2466bd78fa35a0529fa46a65cc7fb3a569`
- Contract-base Core source commit:
  `d235bcfdc2e913e2305d81a6a86414ba6781918a`

The one-commit advance between those Core refs added only the reviewed #732
frontend API decision packet and report. It did not change the SQLite schema,
migration loader, analytics ingest, producer-boundary contracts, or governing
ADRs named here.

The R&D consumer contract controls its schemas and consumer restrictions. This
Core contract controls only producer-side source selection, transformation,
validation, and local lifecycle requirements. Neither repository grants the
other repository implementation or access authority by implication.

## Governing Authority

This contract follows:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`

## Owning Layer And Truth Boundary

Core parser/state remains the truth owner for normalized match, game, result,
context, and evidence-status facts. Core analytics SQLite is a local persistence
surface. It does not become a new truth owner.

The future producer may own only:

- the source allowlist in this contract;
- the total sanitization mapping in this contract;
- dataset-local pseudonym assignment;
- package construction and local validation;
- producer-side lifecycle enforcement; and
- public-safe symbolic diagnostics.

The producer must not repair, infer, relabel, or improve parser facts. A
sanitization category is a disclosure-reducing representation, not replacement
parser truth. R&D may later profile an exactly approved package, but it does not
receive parser, producer, implementation, or downstream authority.

```text
Player.log evidence
  -> Core parser/state interpretation
  -> Core analytics SQLite parser-normalized facts
  -> future contract-bound Core producer
  -> owner-controlled sanitized local dataset
  -> separately approved R&D consumer
```

## Internal Project Area

- Primary area: `core_parser_and_runtime`
- Bridge classification: `cross_repository_evidence_bridge`
- Risk tier: `high`
- Data classification: `private_sensitive_local_only`

This bridge is not a shared truth layer and is not a public export API.

## Files Owned By This Contract

This Codex B pass owns only:

- `docs/contracts/core_sanitized_parser_fact_producer_boundary.md`

A later implementation contract would have to name producer code, schema,
tests, and local artifact paths. This contract does not reserve or create those
files.

## V1 Artifact Boundary

### Producer output

The only real-evidence output shape this contract recognizes is the R&D-owned
logical schema:

```yaml
object: sanitized_parser_fact_local_dataset
schema_version: sanitized_parser_fact_local_dataset.v1
evidence_mode: local_only
sanitization_profile:
  profile_id: core_parser_fact_research_profile
  profile_version: 1
```

The complete package and record field sets are reproduced below to close the
producer interface. Unknown, extra, missing, null where prohibited, or
differently versioned fields fail closed.

Core does not produce the commit-safe aggregate evidence profile or R&D
synthetic fixtures under this contract. No row-level package is commit-safe.

### Three-layer separation

| Artifact class | Owner | Real rows allowed | Commit-safe | Authority now |
| --- | --- | --- | --- | --- |
| Sanitized local dataset | Future Core producer | Yes, after separate approval | No | Not authorized |
| Aggregate evidence profile | Future R&D profiler | Aggregates only | Eligible for later review, not authorized here | Not authorized |
| Purely synthetic fixtures | Future R&D test implementation | No real or transformed records | Potentially, after review | Not authorized |

R&D must never receive raw or unsanitized data in order to sanitize it.

## Exact Source Schema Binding

### Accepted schema envelope

The v1 producer design is valid only while all of these statements are true:

```yaml
analytics_schema_version: analytics_local_sqlite_schema.v1
required_migration_id: 0001_initial_analytics_schema
required_migration_filename: 0001_initial_analytics_schema.sql
required_parser_schema_version_id: analytics_local_sqlite_schema.v1
required_ledger_versions:
  - player_log_evidence_ledger.v1
  - player_log_evidence_ledger_schema.v1
  - player_log_field_evidence.v1
```

The future producer must use the migration loader and read-only SQLite schema
introspection to verify the exact table names, columns, affinities, foreign
keys, and CHECK constraints against the reviewed migration. It may compare the
public source-controlled migration checksum with `schema_migrations`, but it
must not emit that checksum. Any migration beyond `0001`, missing migration,
checksum mismatch, table/column drift, trigger, view substitution, unknown
parser schema version, or incompatible constraint blocks generation with
`blocked_source_schema_drift`.

Dynamic table discovery, `SELECT *`, arbitrary SQL, caller-supplied table or
column names, attached databases, extensions, and schema fallback are
forbidden.

### Column-use classes

- `join_only`: may be held transiently to join or pseudonymize; never emitted.
- `mapping_input`: may be transformed only through the total mapping below.
- `provenance_input`: may contribute only to the closed provenance object.
- `preflight_only`: may validate source state; never enters a record.

### Closed table and column allowlist

Every source column not listed below is prohibited, including columns on an
otherwise allowed table.

| Table | Allowed columns | Use |
| --- | --- | --- |
| `schema_migrations` | `migration_id`, `migration_filename`, `checksum_sha256`, `schema_version_after` | preflight only |
| `parser_schema_versions` | `parser_schema_version_id`, `source_surfaces`, `field_evidence_schema_version` | preflight and package lineage |
| `ingest_runs` | `ingest_run_id`, `source_kind`, `status`, `schema_version` | join/preflight only |
| `matches` | `match_id`, `match_started_at`, `match_completed_at`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | join, time coarsening, provenance |
| `games` | `game_id`, `match_id`, `game_number`, `game_started_at`, `game_completed_at`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | join, mapping, time coarsening, provenance |
| `match_results` | `match_result_id`, `match_id`, `match_result`, `games_won`, `games_lost`, `total_games`, `match_win`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | mapping and provenance |
| `game_results` | `game_result_id`, `game_id`, `match_id`, `game_number`, `local_result`, `pre_postboard_label`, `play_draw`, `turn_count`, `game_started_at`, `game_completed_at`, `game_duration_seconds`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | mapping and provenance |
| `match_context` | `match_context_id`, `match_id`, `queue_name`, `format_name`, `match_win_condition`, `event_type`, `event_scope`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | mapping and provenance |
| `rank_snapshots` | `rank_snapshot_id`, `match_id`, `game_id`, `rank_context`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | availability/category and provenance |
| `opening_hands` | `opening_hand_id`, `game_id`, `match_id`, `game_number`, `hand_size`, `exact_card_count`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | mapping, card-identity availability only, provenance |
| `mulligan_events` | `mulligan_event_id`, `game_id`, `match_id`, `game_number`, `mulligan_count`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | mapping and provenance |
| `sideboarding_states` | `sideboarding_state_id`, `game_id`, `match_id`, `game_number`, `sideboarding_entered`, `submit_deck_seen`, `exact_sideboard_delta_available`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | availability only and provenance |
| `submitted_deck_snapshots` | `submitted_deck_snapshot_id`, `game_id`, `match_id`, `game_number`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | presence only and provenance |
| `gameplay_actions` | `gameplay_action_id`, `game_id`, `match_id`, `game_number`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | count only and provenance |
| `opponent_card_observations` | `opponent_card_observation_id`, `game_id`, `match_id`, `game_number`, `evidence_status`, `degradation_flags`, `review_required`, `value_source`, `confidence`, `finality`, `drift_status`, `parser_schema_version`, `ingest_run_id`, `source_parser_surface`, `availability_status` | count, closed evidence mapping, provenance |
| `fact_provenance` | `fact_provenance_id`, `fact_table`, `fact_id`, `fact_field`, `ledger_entry_id`, `source_parser_surface`, `value_source`, `confidence`, `finality`, `drift_flags`, `invariant_status`, `review_required`, `ingest_run_id` | allowlisted fact join and provenance only |

An implementation must encode this matrix as static structured data. It must
not infer permission from SQLite metadata.

### Prohibited source tables

The complete v1 prohibited-table set is:

- `sessions`
- `game_players`
- `deck_labels`
- `opening_hand_cards`
- `mulligan_bottomed_or_discarded_cards`
- `submitted_deck_cards`
- `turns`
- `gameplay_action_cards`
- `card_movements`
- `life_totals`
- `public_zone_observations`
- `opponent_card_observation_cards`
- `matchup_labels`
- `archetype_labels`
- `game_notes`

All unknown tables are prohibited. Human annotation tables are never parser
facts. Card-containing tables remain prohibited even for row counts because
the approved v1 availability signals already exist in non-card tables.

### Specifically prohibited columns

The producer must never select, inspect, or echo non-allowlisted columns. High
risk examples include:

- `source_artifact_label`, `row_counts_json`, and ingest timestamps;
- `session_id`, `session_label`, and parser/raw identity keys;
- `source_fact_key`, `source_payload_paths`, `source_event_timestamp`,
  `degraded_reason`, exception or diagnostic text;
- `event_id`, exact rank/tier values, deck labels, decision detail;
- card names, `grp_id`, object/instance IDs, card keys, quantities, sections,
  positions, sequences, identity hints, and resolution labels tied to cards;
- action type, raw/annotation labels, zones, actor/seat IDs, game-state IDs, and
  action timestamps; and
- `created_at` and `updated_at` values.

## Source Eligibility And Finality

### Eligible source rows

A match record is eligible only when:

1. its `matches` row is `final` or `reconciled`;
2. its `match_results` row, when present, is `final` or `reconciled`;
3. every emitted game has both `games` and `game_results` rows whose finality is
   `final` or `reconciled`;
4. every contributing child row is `final` or `reconciled`;
5. every contributing row references
   `analytics_local_sqlite_schema.v1`;
6. its ingest run has `status = completed`, uses the same schema version, and
   has `source_kind` in `live_parser`, `saved_event_replay`, or
   `sanitized_golden_replay`; and
7. all joins and uniqueness constraints are internally consistent.

All rows contributing to one emitted record must have one uniform finality.
An all-`final` record emits `final`; an all-`reconciled` record emits
`reconciled`. A mixture of `final` and `reconciled` blocks the full linked
match family as `blocked_mixed_source_finality`. The producer must not select a
weaker label, select a stronger label, or drop a contributor to hide the mix.

`live`, `provisional`, annotation finality, missing finality, mixed identity,
or contradictory joins block that record. A blocked record contributes to no
package total. If exclusion would create an unreported partial package, the
whole package is `review_required` and cannot be transferred.

Source kind is lineage context only. It is never represented as evidence that
one source is more truthful than another, and ingest IDs or artifact labels are
never exported.

## Closed Package Schema

The future producer must emit exactly:

```yaml
object: sanitized_parser_fact_local_dataset
schema_version: sanitized_parser_fact_local_dataset.v1
dataset_release_id: ds_<random_uuidv4>
dataset_version: 1
evidence_mode: local_only
sanitization_profile:
  profile_id: core_parser_fact_research_profile
  profile_version: 1
  status: active
producer:
  repository: Tahjali11/Mythic-Edge
  commit: <exact_40_character_lowercase_commit_sha>
  producer_contract_ref: <public_contract_reference>
  parser_schema_versions: <sorted_unique_nonempty_version_labels>
  ledger_versions: <sorted_unique_nonempty_version_labels>
  analytics_schema_version: analytics_local_sqlite_schema.v1
lifecycle:
  status: active_local
  approved_purpose_id: <purpose_id>
  approved_roles: <sorted_unique_approved_roles>
  approved_at_utc: <rfc3339_whole_second_utc>
  expires_at_utc: <rfc3339_whole_second_utc>
  revocation_ref: <approval_event_ref_or_none>
  supersedes_release_id: none
  superseded_by_release_id: none
records: <closed_sorted_record_list>
non_claims: <exact_non_claim_list>
```

The contract reference must bind this file at its eventual reviewed merge
commit. The producer commit must be the exact commit containing the reviewed
implementation. Neither value may be a branch name, mutable ref, placeholder,
or private-content digest.

Every record contains exactly:

```yaml
record_id: rec_<random_uuidv4>
record_kind: match|game
dataset_match_key: match_<random_uuidv4>
dataset_game_key: game_<random_uuidv4>|not_applicable
collection_period_bucket: YYYY-Q1|YYYY-Q2|YYYY-Q3|YYYY-Q4|unknown
context: <all_closed_context_keys>
metrics: <all_closed_metric_keys>
availability: <all_closed_availability_keys>
provenance: <all_closed_provenance_keys>
```

Match records require `dataset_game_key: not_applicable` and
`context.game_number: not_applicable`. Game records require a package-local
game key and game number. Every context, metric, availability, and provenance
key from the R&D v1 contract is required exactly once; omission is not a valid
way to hide a value. Withheld or unsupported facts use their closed status.

### Closed scalar and identifier syntax

- `positive_integer` is a JSON integer greater than or equal to one.
- UUIDv4 values use lowercase canonical `8-4-4-4-12` hexadecimal syntax, a
  version nibble of `4`, and a variant nibble of `8`, `9`, `a`, or `b`.
- Dataset, record, match, and game IDs are respectively `ds_`, `rec_`,
  `match_`, and `game_` plus a canonical UUIDv4.
- `purpose_id` is `purpose_` plus 3 to 48 lowercase ASCII letters, digits, or
  underscores, beginning with a letter.
- `approval_event_ref` is `approval_` plus a canonical UUIDv4.
- An exact commit is 40 lowercase hexadecimal characters.
- A version label is 1 to 64 lowercase ASCII letters, digits, underscores,
  periods, or hyphens and begins with a letter or digit.
- Package approval and expiry use RFC 3339 UTC whole-second timestamps. These
  are lifecycle metadata, never source/gameplay timestamps.
- Approved roles are exactly `owner`, `approved_local_research_operator`, and
  `deterministic_profiler`, deduplicated in that order.
- The public contract reference is
  `Tahjali11/Mythic-Edge@<exact_commit_sha>:docs/contracts/core_sanitized_parser_fact_producer_boundary.md`.
- `parser_schema_versions` is exactly
  `[analytics_local_sqlite_schema.v1]` for profile v1.
- `ledger_versions` is exactly the lexically sorted list
  `[player_log_evidence_ledger.v1,
  player_log_evidence_ledger_schema.v1,
  player_log_field_evidence.v1]`.

Unknown, path-shaped, private-derived, noncanonical, or coercible values are
invalid. Strings such as `true`, `1`, or `yes` never satisfy a boolean field.

### Closed output vocabularies

The producer may emit only these values:

- `format_family`: `standard`, `alchemy`, `historic`, `explorer`, `timeless`,
  `brawl`, `limited_draft`, `limited_sealed`, `other`, `unknown`.
- `queue_family`: `ranked`, `play`, `traditional`, `premier_draft`,
  `quick_draft`, `traditional_draft`, `sealed`, `event`,
  `direct_challenge`, `other`, `unknown`.
- `event_family`: `constructed`, `limited_draft`, `limited_sealed`, `brawl`,
  `direct_challenge`, `other`, `unknown`.
- `ranked_status`: `ranked`, `unranked`, `not_applicable`, `unknown`.
- `match_structure`: `bo1`, `bo3`, `other`, `unknown`.
- `game_number`: `1`, `2`, `3`, `other`, `not_applicable`, `unknown`.
- `play_draw`: `play`, `draw`, `not_applicable`, `unknown`, `conflict`.
- `board_stage`: `preboard`, `postboard`, `not_applicable`, `unknown`,
  `conflict`.
- `match_result` and `game_result`: `win`, `loss`, `draw`, `other`,
  `not_applicable`, `unknown`, `conflict`.
- `games_in_match_bucket`: `one`, `two`, `three`, `four_or_more`,
  `not_applicable`, `unknown`.
- `mulligan_count_bucket`: `zero`, `one`, `two`, `three_or_more`,
  `not_applicable`, `unknown`.
- `opening_hand_size_bucket`: `zero_to_four`, `five`, `six`, `seven`,
  `eight_or_more`, `not_applicable`, `unknown`.
- `turn_count_bucket`: `zero_to_four`, `five_to_nine`, `ten_to_fourteen`,
  `fifteen_or_more`, `not_applicable`, `unknown`.
- `duration_bucket`: `under_five_minutes`, `five_to_nine_minutes`,
  `ten_to_nineteen_minutes`, `twenty_to_thirty_nine_minutes`,
  `forty_minutes_or_more`, `not_applicable`, `unknown`.
- `gameplay_action_count_bucket`: `zero`, `one_to_nine`,
  `ten_to_twenty_nine`, `thirty_or_more`, `not_applicable`, `unknown`.
- `opponent_observation_count_bucket`: `zero`, `one_to_four`, `five_to_nine`,
  `ten_or_more`, `not_applicable`, `unknown`.
- Every availability key: `available`, `expected_unavailable`,
  `not_applicable`, `not_observed`, `withheld_private`, `not_yet_supported`,
  `unknown`.
- `value_source`: `observed`, `derived`, `inferred`, `unknown`, `conflict`,
  `legacy_enriched`.
- `confidence`: `high`, `medium`, `low`, `unknown`.
- `finality`: `final`, `reconciled` for producer-emitted profile-v1 records.
- `drift_status`: `none`, `not_checked`, `degraded`, `conflict`,
  `missing_expected_evidence`, `redacted`.
- `evidence_status`: `complete`, `partial`, `degraded`, `missing`, `conflict`,
  `not_applicable`, `unknown`.
- `degradation_flags`: `none`, `fallback_used`, `weak_fallback_used`,
  `conflicting_evidence`, `missing_expected_evidence`,
  `schema_or_fixture_gap`, `parser_exception`, `sensitive_evidence_redacted`,
  `other_review_required`, `unknown`.
- `source_parser_surfaces`: `match_summary`, `game_summary`,
  `gameplay_action`, `opponent_card_observation`, `field_evidence`,
  `runtime_health`, `other_approved`, `unknown`; profile v1 emits only the first
  five according to the mapping below.

All record objects contain every closed key. `degradation_flags` is
`[none]` only when no other flag applies; `none` cannot coexist with another
flag. `ledger_entry_ids`, degradation flags, and source surfaces are
deduplicated lists. A transformed ledger ID must match
`ledger_[a-z][a-z0-9_]{2,63}` or package creation is blocked.

## Dataset-Local Pseudonymization

- `dataset_release_id`, `record_id`, match keys, and game keys are
  cryptographically random UUIDv4 labels with the required prefixes.
- They must not encode, hash, encrypt deterministically, or otherwise derive
  from a source identifier, source content, path, timestamp, or private value.
- A producer-local raw-to-pseudonym map may exist only in memory during one
  separately authorized generation attempt.
- The map must not be written to the package, logs, snapshots, exceptions,
  reports, caches, temp files, or durable state.
- The map is destroyed when the attempt succeeds, fails, or is cancelled.
- Only game-to-match linkage survives within one release. Session, action,
  observation, card, deck, cross-release, and cross-repository linkage is
  prohibited.
- Profile v1 permits one issued release only. Any future profile version that
  permits another release must create all-new pseudonyms under a separately
  reviewed cross-release policy.

Random pseudonyms intentionally make separately generated releases differ.
Determinism means stable mapping, ordering, bucketing, and validation within
one attempt and byte-stable validation of the resulting immutable package. It
does not require reuse of private identities or pseudonyms across attempts.

## Total Source-To-Sanitized Mapping

Before mapping, text is Unicode-normalized to NFC for comparison only, leading
and trailing whitespace is removed, internal ASCII whitespace is collapsed,
and comparison is case-insensitive. Source text is never emitted. Null or empty
becomes `unknown`; nonempty unrecognized values follow the explicit fallback
below. No fuzzy match, model, network lookup, card database, or caller override
is allowed.

### Context mapping

| Output | Exact source and rule |
| --- | --- |
| `format_family` | `match_context.format_name`: exact normalized `standard`, `alchemy`, `historic`, `explorer`, `timeless`, `brawl` map identically; values containing exact token `draft` map `limited_draft`; values containing exact token `sealed` map `limited_sealed`; other nonempty values map `other`; null/empty maps `unknown`. |
| `queue_family` | `match_context.queue_name`: exact `ranked` maps `ranked`; exact `play` maps `play`; exact `traditional` or `traditional ranked` maps `traditional`; exact `premier draft`, `quick draft`, `traditional draft`, `sealed`, and `direct challenge` map to their underscore literals; any other value containing exact token `event` maps `event`; other nonempty maps `other`; null/empty maps `unknown`. |
| `event_family` | Evaluate `event_type`, then `event_scope`: exact normalized values containing `constructed`, `draft`, `sealed`, `brawl`, or `direct challenge` map to the corresponding closed literal; first recognized value wins; other nonempty input maps `other`; both null/empty map `unknown`. Exact `event_id` is never read. |
| `ranked_status` | `ranked` only when an allowlisted `rank_snapshots` row for the same record is `available`; `unranked` only when queue family is a known unranked family (`play` or `direct_challenge`) and no available rank row exists; otherwise `unknown`. Absence alone never means unranked. |
| `match_structure` | `match_win_condition`: exact normalized `matchwincondition_best2of3`, `best2of3`, `best of 3`, or `bo3` maps `bo3`; exact `matchwincondition_best1of1`, `best1of1`, `best of 1`, or `bo1` maps `bo1`; other nonempty maps `other`; null/empty maps `unknown`. |
| `game_number` | Match record: `not_applicable`. Game row integer `1`, `2`, or `3` maps to the corresponding string; any other positive integer maps `other`; missing/nonpositive blocks the game row. |
| `play_draw` | Exact source `play`, `draw`, or `unknown` maps identically; null maps `unknown`; any other source value blocks as schema drift. A conflicting provenance label maps the record value to `conflict`. |
| `board_stage` | `game1` and `preboard` map `preboard`; `postboard` maps `postboard`; `unknown` or null maps `unknown`; any other value blocks. Match record uses `not_applicable`. A conflicting provenance label maps to `conflict`. |
| `match_result` | Prefer `match_win`: `1` maps `win`, `0` maps `loss`. If absent, normalized `match_result` values `w`/`win` and `l`/`loss` map accordingly; `d`/`draw`/`tie` maps `draw`; other nonempty maps `other`; null maps `unknown`. Disagreement between recognized fields or conflicting provenance maps `conflict`. Game record repeats its parent match category. |
| `game_result` | Normalized `local_result`: `w`/`win` maps `win`; `l`/`loss` maps `loss`; `d`/`draw`/`tie` maps `draw`; other nonempty maps `other`; null maps `unknown`. Conflicting provenance maps `conflict`. Match record uses `not_applicable`. |

These rules are disclosure mappings, not corrections. The profile version must
change before any recognized literal or precedence changes.

### Metric mapping

| Output | Rule |
| --- | --- |
| `games_in_match_bucket` | Use a nonnegative `match_results.total_games` when present; otherwise count eligible `games` rows. Disagreement blocks the match. `1`, `2`, `3`, and `>=4` map to `one`, `two`, `three`, `four_or_more`; null maps `unknown`; game records use their parent match bucket. |
| `mulligan_count_bucket` | For a game, all nonnull `mulligan_events.mulligan_count` values must agree; `0`, `1`, `2`, and `>=3` map to the closed buckets. No row/null maps `unknown`. Match record uses `not_applicable`. |
| `opening_hand_size_bucket` | `opening_hands.hand_size`: `0..4`, `5`, `6`, `7`, and `>=8` map to the closed buckets. Negative blocks; null/no row maps `unknown`; match uses `not_applicable`. |
| `turn_count_bucket` | `game_results.turn_count`: `0..4`, `5..9`, `10..14`, and `>=15` map to the closed buckets. Negative blocks; null maps `unknown`; match uses `not_applicable`. |
| `duration_bucket` | Finite `game_duration_seconds`: `[0,300)`, `[300,600)`, `[600,1200)`, `[1200,2400)`, and `>=2400` map respectively to the five closed buckets. Negative/nonfinite blocks; null maps `unknown`; match uses `not_applicable`. |
| `gameplay_action_count_bucket` | Count only eligible `gameplay_actions` rows for the game. `0`, `1..9`, `10..29`, `>=30` map to the closed buckets. Match uses `not_applicable`. No action fields are read. |
| `opponent_observation_count_bucket` | Count only eligible `opponent_card_observations` rows for the game. `0`, `1..4`, `5..9`, `>=10` map to the closed buckets. Match uses `not_applicable`. No card or action fields are read. |

### Time mapping

Exact source and gameplay timestamps are transient mapping inputs only. For a
match use the first valid value in this order: `match_started_at`,
`match_completed_at`, earliest eligible game `game_started_at`, earliest
eligible game `game_completed_at`. For a game use `game_started_at`, then
`game_completed_at`. A valid RFC 3339 timestamp maps only to UTC calendar
quarter `YYYY-Q1` through `YYYY-Q4`; absent or unparsable input maps `unknown`
and sets `review_required: true`. The exact timestamp must be discarded before
record construction and must never appear in output or diagnostics.

### Availability mapping

Availability uses the following closed reducers before the per-key table:

**`single_row_availability(table, required_value)`**

1. No physical row -> `not_observed`.
2. One or more physical rows exist but none is eligible -> `unknown` and
   `review_required: true`.
3. More than one eligible row exists where the schema requires at most one ->
   `unknown` and review.
4. One eligible row with a missing, null, unknown, or non-closed
   `availability_status` -> `unknown` and review.
5. One eligible row with `expected_unavailable`, `not_applicable`,
   `not_observed`, `withheld_private`, or `not_yet_supported` -> that exact
   literal. Its scalar value is not inspected to upgrade the status.
6. One eligible row with `available` and a required scalar that is null,
   malformed, or contradictory -> `unknown` and review.
7. One eligible row with `available` and a valid required scalar, or with no
   required scalar -> `available`.

**`row_set_availability(table)`**

1. No physical rows -> `not_observed`.
2. Physical rows but no eligible rows -> `unknown` and review.
3. Eligible rows with a missing/unknown status or more than one distinct closed
   status -> `unknown` and review.
4. Eligible rows with exactly one shared closed status -> that status.

These reducers preserve `withheld_private`; they never infer it from missing
data. `not_yet_supported` is emitted only where the source says so or where
this profile explicitly fixes it. `not_applicable` is emitted only for a
record-kind exclusion named below.

| Output key | Match record | Game record | Exact present/absent/null/false rule |
| --- | --- | --- | --- |
| `match_identity` | `single_row_availability(matches, match_id)` | Same parent-match result | Construction requires one eligible row; absent/ineligible blocks record construction rather than inventing identity. A non-`available` source status is preserved and requires review. |
| `game_identity` | `not_applicable` | `single_row_availability(games, game_id)` | Missing/ineligible identity blocks the linked game and therefore the full match family. |
| `match_result` | `single_row_availability(match_results, match_result or match_win)` | Same parent-match result | No row -> `not_observed`; `available` plus both result fields null -> `unknown` and review; recognized or nonempty mapped result -> `available`; field disagreement -> `unknown` and review. |
| `game_result` | `not_applicable` | `single_row_availability(game_results, local_result)` | No row -> `not_observed`; `available` plus null result -> `unknown` and review; valid mapped result -> `available`. |
| `queue_format_context` | One `match_context` row reduced across `queue_name` and `format_name` | Same parent-match result | No row -> `not_observed`; source status other than `available` is preserved; `available` with both values null/empty -> `unknown` and review; at least one mappable nonempty value -> `available`. |
| `rank_context` | `row_set_availability(rank_snapshots)` | Rows scoped to the game, falling back to parent-match rows only when `game_id` is null | No rows -> `not_observed`; null `rank_context` on an otherwise `available` row -> `unknown` and review; one shared closed status follows the reducer. Absence never means unranked. |
| `play_draw` | `not_applicable` | `single_row_availability(game_results, play_draw)` | No result row -> `not_observed`; `available` plus null -> `unknown` and review; exact `play`, `draw`, or `unknown` value -> `available`; invalid value blocks schema mapping. |
| `pre_postboard` | `not_applicable` | `single_row_availability(game_results, pre_postboard_label)` | No row -> `not_observed`; `available` plus null -> `unknown` and review; exact allowed label -> `available`. |
| `opening_hand_size` | `not_applicable` | `single_row_availability(opening_hands, hand_size)` | No row -> `not_observed`; `available` plus null/negative size -> `unknown` and review; nonnegative size -> `available`. |
| `opening_hand_card_identity` | `not_applicable` | Specialized rule over the same `opening_hands` row | No row -> `not_observed`; non-`available` source status is preserved; null count -> `unknown` and review; count `< 0` blocks; count `0` -> `expected_unavailable`; count `> 0` -> `available`. Card rows and identities remain unread. |
| `mulligan_count` | `not_applicable` | Specialized row-set rule over `mulligan_events` | No rows -> `not_observed`; physical but ineligible rows -> `unknown` and review; any null count or disagreement -> `unknown` and review; all eligible counts equal and statuses equal -> shared status; a valid count with shared `available` -> `available`. |
| `submitted_deck_evidence` | `not_applicable` | `single_row_availability(submitted_deck_snapshots, none)` | No row -> `not_observed`; an eligible row uses its exact closed source status. Deck label/time/content columns remain unread. |
| `sideboarding_evidence` | `not_applicable` | Specialized rule over one `sideboarding_states` row | No row -> `not_observed`; non-`available` source status is preserved; any boolean outside `0|1|null` blocks; any true boolean -> `available`; all three false -> `not_observed`; no true value plus any null -> `unknown` and review. Exact delta contents remain unread. |
| `gameplay_actions` | `not_applicable` | `row_set_availability(gameplay_actions)` | No rows -> `not_observed`; eligible rows use the exact row-set reducer. Count zero is `not_observed`, not `expected_unavailable`. |
| `opponent_card_observations` | `not_applicable` | `row_set_availability(opponent_card_observations)` | No rows -> `not_observed`; eligible rows use the exact row-set reducer. Observation/card details remain unread. |
| `field_evidence` | Eligible `fact_provenance` rows joined to the match record | Eligible rows joined to the game and included fact rows | No rows -> `not_observed`; physical but ineligible/unjoinable rows -> `unknown` and review; eligible rows use the exact row-set reducer after their parent fact's availability status is projected. |
| `runtime_health_evidence` | `not_yet_supported` | `not_yet_supported` | Fixed profile-v1 value. No runtime file, table, status payload, or diagnostic is read. |

An available prohibited fact means only that its family was observed. It never
permits the underlying value to enter the package.

## Provenance Preservation

Every record must contain all R&D v1 provenance keys. Values are computed only
from eligible contributing rows and allowlisted provenance columns.

### Closed aggregation rules

- `value_source` uses the first present value in severity order:
  `conflict`, `unknown`, `inferred`, `legacy_enriched`, `derived`, `observed`.
- `confidence` uses `unknown`, `low`, `medium`, `high` severity order.
- `finality` is `final` only when every contributing row is `final`, and is
  `reconciled` only when every contributing row is `reconciled`. Mixed
  `final`/`reconciled` input blocks the full linked match family before record
  construction. No other finality is eligible.
- `drift_status` uses `conflict`, `missing_expected_evidence`, `degraded`,
  `redacted`, `not_checked`, `none` severity order.
- `review_required` is true if any contributing source says true, any result is
  conflict/unknown, confidence is low/unknown, drift is not `none` or
  `not_checked`, a timestamp is unparsable, a source value is generalized to
  `other`, or an availability/provenance value is unavailable to map exactly.
- Lists are deduplicated and sorted by the closed order in this contract.

### Evidence-status mapping

For opponent-observation source evidence:

- `observed` -> `complete`
- `derived` or `inferred` -> `partial`
- `degraded` -> `degraded`
- `conflict` -> `conflict`
- `unknown` -> `unknown`

For other families, source availability `expected_unavailable` or
`not_observed` maps `missing`, `not_applicable` maps `not_applicable`, and a
usable allowlisted provenance row maps `complete`. Otherwise use `unknown`.
The aggregate severity is `conflict`, `missing`, `degraded`, `partial`,
`unknown`, `not_applicable`, `complete`.

### Degradation mapping

The exact v1 mappings are:

| Source label | Output degradation flag |
| --- | --- |
| `fallback_used` | `fallback_used` |
| `weak_fallback_used` | `weak_fallback_used` |
| `conflicting_evidence`, `invariant_failed`, `actor_relation_conflict`, `action_seat_conflict`, `name_resolution_contradicted` | `conflicting_evidence` |
| `missing_expected_event_family`, `missing_expected_payload_path`, `missing_card_identity`, `missing_seat_mapping`, `data_loss_evidence` | `missing_expected_evidence` |
| `changed_signal_type`, `new_unknown_event_family`, `new_unknown_payload_path`, `schema_snapshot_missing`, `fixture_gap` | `schema_or_fixture_gap` |
| `parser_exception` | `parser_exception` |
| `sensitive_evidence_redacted` | `sensitive_evidence_redacted` |
| `name_resolution_candidate`, `name_resolution_ambiguous`, `name_resolution_name_only`, `name_resolution_unresolved`, `ambiguous_visibility` | `weak_fallback_used` |
| `transport_failure`, `workbook_drift`, `deployment_drift` | `other_review_required` |

No degradation label may be emitted verbatim. An unknown source label blocks
the package as `blocked_unknown_provenance_label`; it does not silently become
`unknown`.

`fact_provenance.drift_flags` and observation degradation flags must be valid
JSON arrays of unique strings. Malformed JSON, a scalar, duplicate labels, or
an unknown label blocks generation. `invariant_status` maps as follows:

- `passed` and `not_applicable` add no degradation flag;
- `not_checked` or null sets `review_required: true`;
- `degraded` adds `other_review_required` and requires review;
- `failed` adds `conflicting_evidence` and requires review; and
- any unknown nonnull literal blocks the contributing provenance row and the
  package.

A `fact_provenance` row may contribute only when `fact_table` names an allowed
fact table, `fact_id` exactly joins that table's listed primary ID, and
`fact_field` names one of that table's listed mapping or provenance input
columns. The query must name those table/field pairs statically. Provenance for
an annotation table, prohibited field, unmatched ID, `human_annotation` value
source, `human` confidence, or annotation finality blocks the package; it is
not ignored or recast as parser provenance.

### Ledger and surface mapping

- A nonnull ledger entry ID is eligible only when it is present in the bound
  `player_log_evidence_ledger.v1` source-controlled vocabulary.
- Its public-safe output is `ledger_` plus the lowercase entry ID with each dot
  replaced by an underscore. This transform is allowed because the input is a
  public schema label, not a private identifier.
- Unknown ledger IDs block generation.
- Exact source surface mappings are:
  `MatchSummary.to_match_log_row` -> `match_summary`,
  `GameSummary.to_game_log_row` -> `game_summary`,
  `gameplay_actions.py` -> `gameplay_action`, and
  `opponent_card_observations.py` -> `opponent_card_observation`.
- Presence of an allowlisted `fact_provenance` row also adds `field_evidence`.
- Unknown or path-shaped source surfaces block generation.

No payload path, source event timestamp, source fact key, event body,
invariant detail, degraded reason, or source artifact label may enter output.

## Card, Deck, Action, And Linkage Suppression

Profile v1 is availability-only for cards and decks. It must not read or emit:

- card names or IDs;
- opening-hand cards or sequences;
- mulligan bottom/discard cards;
- submitted-deck cards, quantities, sections, names, signatures, or deltas;
- action-associated cards, action sequences, zones, or actor details;
- opponent card identities or resolution details; or
- reconstructable deck, hand, sideboard, or gameplay fingerprints.

Only dataset-local match-to-game linkage is allowed. An implementation must
prove that no source session, action, observation, card, deck, ingest, or
provenance row identity survives package construction.

## Small-Cell And Combination Controls

The local dataset remains private and is not anonymous. Before an exact package
can become transfer-eligible, a producer-side validator must perform a local,
no-echo disclosure screen over sanitized values only:

### Exact released-value vector

Equivalence classes are computed separately by `record_kind` over the canonical
tuple below. Every tuple field is the exact post-mapping value that would be
released:

1. `record_kind`;
2. `collection_period_bucket`;
3. all context values in contract order;
4. all metric values in contract order;
5. all availability values in contract order;
6. provenance scalars in order: `value_source`, `confidence`, `finality`,
   `drift_status`, `evidence_status`, `review_required`;
7. the complete canonical degradation-flag tuple;
8. the complete canonical ledger-entry-ID tuple; and
9. the complete canonical source-parser-surface tuple.

Random `record_id`, `dataset_match_key`, and `dataset_game_key` are excluded
because they are release-local random labels. Linkage is screened separately
as a full match family. No other released field is excluded. Empty lists and
`[none]` remain distinct canonical values.

### Deterministic generalization and omission

1. A tuple class of one through four is `small_cell`; zero means no class.
2. Apply these global transformations one at a time in this exact order to all
   records, never only to selected rows: collection quarter -> `unknown`, event
   family -> `other`, queue family -> `other`, format family -> `other`, ranked
   status -> `unknown`, match structure -> `other`, then each metric in contract
   order -> `unknown`.
3. Recompute every complete tuple after each global step. The first state in
   which every nonzero class is at least five is the only eligible generalized
   state.
4. Availability and provenance values are never generalized. Replacing them
   would alter evidence meaning rather than coarsen context.
5. If any class remains one through four after all allowed generalizations,
   mark every linked match family containing one of its records for omission.
   Omit the whole family, including its match row and every game row.
6. Recompute from the original mapped records minus all marked families. Repeat
   steps 1 through 5 until no new family is marked.
7. If the remaining package is empty, if iteration does not reach a fixed point
   after at most the original number of match families, or if any remaining
   complete tuple has count one through four, block transfer as
   `blocked_rare_combination_risk`.

The set of marked families is determined simultaneously per iteration from
the lexically sorted canonical tuples, so traversal order cannot change the
result. Omitted records affect no released total, denominator, or linkage.

### Closed projection and complementary-disclosure check

After the complete-vector fixed point, construct every one-way and every
unordered two-way projection over this exact dimension list:

- `record_kind` and `collection_period_bucket`;
- every context key;
- every metric key;
- every availability key;
- every provenance scalar;
- canonical `degradation_flags` tuple;
- canonical `ledger_entry_ids` tuple; and
- canonical `source_parser_surfaces` tuple.

Dimensions use contract order; unordered pairs use ascending contract index.
Three-way and higher projections are not generated or requested. Each nonzero
projected cell must be at least five. A projected cell of one through four
blocks transfer as `blocked_complementary_disclosure`; the producer must not
choose an additional cell subjectively.

For every projection, mechanically test each cell against its dimension total:
`hidden = total - sum(other released cells)`. If `hidden` is in `1..4`, or if a
linked-family omission count in `1..4` can be derived from package-visible
totals, block the entire package as `blocked_complementary_disclosure`. No
secondary discretionary suppression is allowed in profile v1.

### Closed rare-combination rule

`rare_combination_risk` means exactly one of:

- a complete released-value tuple has count `1..4` after the fixed process;
- an allowed one-way or two-way projected cell has count `1..4`;
- complementary subtraction yields a hidden count `1..4`;
- an availability or provenance tuple requiring generalization remains
  distinguishing and therefore forces linked-family omission.

No cross-release source-ID comparison exists in profile v1. The producer does
not retain source IDs, source-to-pseudonym maps, source-derived membership
digests, Bloom filters, hashes, or any other private membership index. Instead,
the single-release seal below prevents a second profile-v1 package from being
issued at all. No prose notion of an "unusual" combination exists.

The minimum of five is inherited from the merged R&D v1 suppression policy.
It is a project disclosure control, not proof of anonymity or privacy. The
local validator may report only a closed status and an error count of zero or
at least five; it must not report hidden values or counts from one through four.

### Permanent profile-v1 single-release seal

`core_parser_fact_research_profile.v1` may issue exactly one package across all
purposes, operators, source database instances, attempts, and time. Expiry,
revocation, deletion, or an abandoned research purpose does not restore the
right to issue another profile-v1 package. A later package requires a new
producer profile and contract version with independently reviewed cross-release
controls.

A future implementation must maintain one owner-controlled, local-only seal
slot with this exact logical schema:

```yaml
object: core_sanitized_parser_fact_profile_release_seal
schema_version: core_sanitized_parser_fact_profile_release_seal.v1
profile_id: core_parser_fact_research_profile
profile_version: 1
record_version: <positive_integer>
seal_status: unused|issued_permanent
dataset_release_id: none|<dataset_release_id>
dataset_version: none|1
issuance_event_ref: none|<approval_event_ref>
issued_at_utc: none|<rfc3339_utc>
false_authority:
  sqlite_access_authorized_by_seal: false
  package_generation_authorized_by_seal: false
  package_transfer_authorized_by_seal: false
  r_and_d_access_authorized_by_seal: false
  implementation_authorized_by_seal: false
```

Cross-field rules are exact:

- `unused` requires `record_version = 1` and all release, event, and timestamp
  fields to be `none`;
- `issued_permanent` requires a canonical release ID, `dataset_version = 1`, a
  nonnull event reference, a valid issuance timestamp, and
  `record_version = 2`;
- in `issued_permanent`, the seal release ID/version equal the immutable
  package, `issuance_event_ref` equals the sequence-1 lifecycle `event_ref`,
  and `issued_at_utc` equals that record's `effective_at_utc` and is not later
  than its `recorded_at_utc`;
- no third status or record version exists;
- `issued_permanent` never returns to `unused` and cannot change release ID;
- a missing, deleted, unreadable, duplicated, extra, differently versioned,
  contradictory, or unknown seal is not equivalent to `unused`; it blocks as
  `blocked_profile_release_seal_invalid`; and
- the seal contains no purpose, source database identifier, source row ID,
  pseudonym, mapping, private hash, content digest, path, or package content.

The package and its sequence-1 `active_local` lifecycle record remain staged
and invisible to readers until one atomic local transaction compares the seal
as exact `unused`, changes it to `issued_permanent`, and publishes those two
immutable objects together. Exactly one concurrent transaction may succeed.

Failure behavior is closed:

- failure before commit leaves the seal `unused`; staged objects are
  inaccessible and must be removed without retaining a source mapping;
- successful commit makes the seal, package, and sequence-1 lifecycle record
  visible together;
- failure or ambiguity during commit is `review_required`; no object is
  readable or transferable until an independently authorized recovery proves
  either the complete pre-commit or complete post-commit state;
- failure after commit never rolls the seal back, even if package validation,
  transfer, research, or deletion later fails; and
- any later generation attempt reads only the seal metadata before SQLite or
  private source access and returns `blocked_profile_release_already_issued`
  when it is `issued_permanent`.

The transactional state mechanism, storage path, locking, crash recovery, and
artifact creation still require a later implementation contract. If that
mechanism cannot provide the atomic visibility above, profile-v1 generation is
not implementable and remains blocked. This contract does not create the seal
or authorize a package.

## Ordering, Repeatability, And Canonicalization

- Validate source rows before pseudonym assignment.
- Establish transient source order by record kind, source match ID, game
  number, and source game ID. Those values never leave producer memory.
- Assign random keys once per generation attempt.
- Emit match records before their game records.
- Sort output by `dataset_match_key`, record kind order `match`, `game`, then
  game number and `dataset_game_key`.
- Serialize UTF-8 without BOM, JSON objects with lexically sorted keys, compact
  separators, LF newlines, and one terminal newline.
- Arrays governed by closed vocabularies use contract order; symbolic IDs use
  lexical order.
- No generation time, path, random seed, host value, database filename, or
  locale-dependent formatting may affect category mapping.

Synthetic tests may inject a deterministic pseudonym source. Production/local
generation must use fresh randomness. Byte stability is required for repeated
validation of one immutable package, not for separate releases.

## Lifecycle, Retention, And Access

The package is an immutable issuance snapshot. Its embedded
`lifecycle.status` is always `active_local` and is never edited. Later state is
represented by a separate owner-controlled, local-only, append-only producer
lifecycle chain with logical schema
`core_sanitized_parser_fact_package_lifecycle.v1`. The chain is not part of the
row-level package, is not commit-safe, and has no repo-visible storage path.

### Immutable package lifecycle tuple

At issuance, the package lifecycle object is valid only when all these rules
hold:

```yaml
status: active_local
approved_purpose_id: <non_placeholder_purpose_id>
approved_roles: <nonempty_closed_role_list>
approved_at_utc: <rfc3339_utc>
expires_at_utc: <later_rfc3339_utc>
revocation_ref: none
supersedes_release_id: none
superseded_by_release_id: none
```

- `approved_at_utc < expires_at_utc` is strict.
- The package is issued at or after approval and strictly before expiry.
- Roles are nonempty, unique, and in contract order.
- An active package cannot carry a revocation reference or either supersession
  reference.
- Supersession is reserved and unsupported in profile v1. Any non-`none`
  supersession field invalidates issuance as `blocked_lifecycle_invalid`.
- `dataset_version` is exactly `1` and must match the permanent profile seal.
- Missing, unknown, extra, null, placeholder, contradictory, expired, or
  differently versioned values invalidate issuance.

These reproduce the merged R&D package constraints. The immutable package does
not pretend to update itself after issuance.

### Append-only lifecycle record schema

Every producer lifecycle record contains exactly:

```yaml
object: core_sanitized_parser_fact_package_lifecycle_record
schema_version: core_sanitized_parser_fact_package_lifecycle.v1
dataset_release_id: <dataset_release_id>
dataset_version: 1
sequence: <positive_integer>
record_ref: lifecycle:<dataset_release_id>:s<sequence>
previous_record_ref: lifecycle:<dataset_release_id>:s<previous_sequence>|none
status: active_local|expired|revoked|review_required|deletion_required|deletion_confirmed
recorded_at_utc: <rfc3339_utc>
effective_at_utc: <rfc3339_utc>
event_ref: <approval_event_ref>
reason: issued|expiry_reached|owner_revoked|prohibited_data_incident|deletion_after_expiry|deletion_after_revocation|deletion_after_incident|deletion_completed
approved_at_utc: <package_approved_at_utc>
expires_at_utc: <package_expires_at_utc>
revocation_ref: <approval_event_ref>|none
supersedes_release_id: none
superseded_by_release_id: none
deletion_confirmation_ref: <approval_event_ref>|none
false_authority:
  package_access_authorized_by_record: false
  package_transfer_authorized_by_record: false
  r_and_d_access_authorized_by_record: false
  implementation_authorized_by_record: false
```

The record contains no package path, filename, source ID, pseudonym, private
hash, content digest, package row, reason prose, operator identity, or deleted
value. `event_ref` and lifecycle references are random public-safe symbolic
labels, not hashes of private content.

### Chain identity, order, and replay

- Sequence begins at `1` and is contiguous without duplicates or gaps.
- Sequence 1 has `previous_record_ref: none`; every later record points to the
  immediately previous sequence.
- `record_ref`, sequence, release ID, and previous reference must agree
  mechanically.
- `recorded_at_utc` values strictly increase. `effective_at_utc` cannot be later
  than `recorded_at_utc`, cannot precede package approval, and must be greater
  than or equal to the immediately prior record's `effective_at_utc`.
- Package approval/expiry fields are repeated unchanged. Both supersession
  fields remain exactly `none` in every record.
- A duplicate sequence, reused event reference, branch, gap, rewrite, deleted
  predecessor, unknown record, or contradictory chain is
  `blocked_lifecycle_replay_or_fork`.
- Records are immutable after append. Correction requires a new release; it
  does not rewrite lifecycle history.

### Closed transition matrix

| Prior state | Next state | Required reason and fields | Forbidden fields |
| --- | --- | --- | --- |
| none | `active_local` | sequence 1; `issued`; package tuple copied exactly; effective time before expiry | revocation, superseded-by, deletion confirmation |
| `active_local` | `expired` | `expiry_reached`; `effective_at_utc >= expires_at_utc` | revocation, superseded-by, deletion confirmation |
| `active_local` | `revoked` | `owner_revoked`; `revocation_ref = event_ref != none`; effective time before or at recording | superseded-by, deletion confirmation |
| `active_local` | `review_required` | `prohibited_data_incident`; event reference names the symbolic incident decision | revocation, superseded-by, deletion confirmation |
| `expired` | `deletion_required` | `deletion_after_expiry` | revocation, superseded-by, deletion confirmation |
| `revoked` | `deletion_required` | `deletion_after_revocation`; preserve revocation reference | superseded-by, deletion confirmation |
| `review_required` | `deletion_required` | `deletion_after_incident` | new revocation/supersession fields, deletion confirmation |
| `deletion_required` | `deletion_confirmed` | `deletion_completed`; nonnull `deletion_confirmation_ref = event_ref` | any new revocation or supersession field |

No other transition exists. In particular, no nonactive state returns to
`active_local`; `deletion_confirmed` is terminal; expiry cannot be postponed by
editing a timestamp; a later record cannot backdate its effective transition;
supersession literals or references are invalid; and deletion cannot be
confirmed directly from `active_local`.

### Current-state derivation

The current producer lifecycle state is the status on the highest contiguous,
fully valid sequence after validating the entire chain from sequence 1. If the
chain is absent, incomplete, forked, stale, replayed, future-dated,
contradictory, or contains an invalid transition, current state is
`review_required` and access/transfer fail closed.

At or after `expires_at_utc`, an `active_local` latest record is treated as
`expired_pending_record` and blocks access immediately even if the append-only
expiry record has not yet been written. It never extends validity.

Only a latest state of `active_local`, observed strictly before expiry, is
eligible for a separately approved access or transfer decision.

### Two distinct owner approvals

1. **Generation approval** must name the source schema/commit, profile version,
   purpose, permitted local operator, exact time window, retention/expiry, and
   forbid transfer. It authorizes at most one generation attempt when a later
   implementation contract exists.
2. **Transfer/access approval** may occur only after local validation and must
   name the exact `dataset_release_id`, dataset version, producer commit,
   contract reference, profile version, purpose, R&D role, access window, and
   expiry. It authorizes only that package and does not authorize another
   release, raw access, consumer implementation, or downstream use.

Neither approval exists in this contract. Issue state, Codex role, clean tests,
contract review, or package validation is not an approval substitute.

### Transfer/access decision recheck

One access/transfer decision must atomically and read-only observe:

1. the permanent profile-v1 seal and its exact package binding;
2. the immutable package and exact package lifecycle tuple;
3. the complete append-only lifecycle chain;
4. the highest valid sequence and current derived state;
5. the exact transfer approval's release, version, profile, purpose, role, and
   expiry binding; and
6. the decision instant in UTC.

The decision is `authorized_local_only_for_exact_decision` only when the latest
state is `active_local`, the seal is `issued_permanent` and names this exact
release/version, decision time is at or after approval and strictly before both
package and transfer-approval expiry, no later lifecycle record exists in the
same locked snapshot, and all bindings match exactly. Otherwise it is
`blocked_lifecycle_invalid`. The decision grants no reusable token and must be
repeated for each read. A stale cached state, caller-supplied state,
package-embedded active status alone, seal alone, or previously valid decision
is never current authority.

### Retention and invalidation

- The owner supplies an exact expiry; no default or indefinite retention is
  allowed.
- Revocation, incident review, or expiry immediately blocks new reads,
  profiling, and transfer through current-state derivation.
- Expiry, revocation, incident review, and deletion never clear or replace the
  permanent profile-v1 release seal.
- Every nonactive state routes through `deletion_required` before
  `deletion_confirmed`.
- Deletion is manual or performed by a separately authorized producer tool.
- A prohibited-data incident appends `review_required`, blocks all use, and
  routes to the owner and Core security workflow. Repository-history
  remediation requires separate authority.

The ephemeral raw-to-pseudonym map is destroyed at attempt completion and is
never retained. Package lifecycle is tracked by public-safe release ID, not by
source identity.

## Exact Non-Claim Set

Every package contains each value exactly once in this order:

```yaml
non_claims:
  - no_anonymity_claim
  - no_privacy_assurance_claim
  - no_security_assurance_claim
  - no_parser_correctness_claim
  - no_representative_coverage_claim
  - no_causality_claim
  - no_exact_ev_or_win_probability_claim
  - no_optimal_play_or_player_mistake_claim
  - no_model_validity_claim
  - no_downstream_readiness_claim
  - no_raw_or_private_access_authority
  - no_implementation_authority
  - no_cross_repository_authority
```

Missing, extra, duplicated, reordered, unknown, or positively phrased values
invalidate the package.

## No-Echo And Diagnostic Contract

Errors, logs, exceptions, CLI output, tests, snapshots, reports, and validation
artifacts may contain only:

- artifact kind and schema version;
- closed validation step;
- closed status/reason code;
- literal booleans; and
- validation error count when zero or at least five.

They must not contain a database path/name, SQL, source table row, source or
dataset ID, pseudonym, timestamp, private hash, source value, card/deck value,
payload, exception message, stack trace, or unknown field. Unsafe input is
replaced before formatting by one of these closed statuses:

- `blocked_authority_missing`
- `blocked_source_schema_drift`
- `blocked_unknown_table`
- `blocked_unknown_column`
- `blocked_unknown_enum`
- `blocked_unknown_provenance_label`
- `blocked_prohibited_field`
- `blocked_unsafe_value_shape`
- `blocked_source_finality`
- `blocked_mixed_source_finality`
- `blocked_identity_or_join_conflict`
- `blocked_no_echo_violation`
- `blocked_small_cell`
- `blocked_complementary_disclosure`
- `blocked_rare_combination_risk`
- `blocked_lineage_incomplete`
- `blocked_profile_release_seal_invalid`
- `blocked_profile_release_already_issued`
- `blocked_lifecycle_invalid`
- `blocked_lifecycle_replay_or_fork`
- `expired_pending_record`
- `blocked_package_validation`
- `review_required`

No raw exception string may cross the producer boundary.

## Package Validation Before Transfer

A later implementation must validate, in this order:

1. generation authority and expiry;
2. exact profile-v1 seal schema and atomic `unused` state before any SQLite or
   private-source read;
3. source schema/migration identity;
4. exact table/column allowlist and query plan;
5. parser schema and ledger versions;
6. ingest completion and source finality;
7. identity/join consistency;
8. total context, metric, availability, and provenance mapping;
9. card/deck/action/raw-field absence;
10. pseudonym syntax, randomness class, and linkage scope;
11. package and record schema closure;
12. non-claim completeness;
13. timestamp coarsening and exact-time absence;
14. small-cell, complementary, and rare-combination controls;
15. no-echo canary scan;
16. immutable package-lifecycle tuple closure, complete append-only lifecycle
    chain continuity, transition-matrix validity, reference/timestamp
    consistency, derived current-state validity, expiry handling, and an atomic
    transfer-decision recheck against the highest valid record;
17. canonical serialization and immutable readback; and
18. a final prohibited-field scan over the package bytes.

Any failure prevents transfer. Passing all checks makes the package only
`locally_validated_awaiting_exact_transfer_approval`; it does not authorize
transfer or R&D access.

## Side Effects

This Codex B contract creates no runtime side effects. A later implementation
must still be separately approved and must not:

- mutate SQLite;
- change parser/state, reconciliation, identities, deduplication, or schemas;
- start live capture or transport;
- write workbook, webhook, Apps Script, Sheets, Analytics, Fable, AI, coaching,
  deployment, or production surfaces;
- upload or automatically transfer a package; or
- commit a local package or private artifact.

## Compatibility And Change Policy

Any change to the source allowlist, mapping, bucket boundary, pseudonym rules,
suppression policy, output field, non-claim set, lifecycle state, source schema,
or R&D consumer schema requires:

1. a new issue or explicit amendment scope;
2. a new producer contract/profile version;
3. independent Core review;
4. corresponding R&D consumer review when its interface changes; and
5. new exact owner approvals for generation and transfer.

Unknown future fields never inherit permission from a parent table.

## Tests Required Before Any Later Implementation Approval

Only purely synthetic, temporary SQLite fixtures may be used. Required tests:

- exact allowlist success and one rejection test per prohibited table/column;
- migration, schema-version, CHECK-constraint, and extra-object drift failures;
- all-`final` and all-`reconciled` acceptance, mixed `final`/`reconciled`
  linked-family rejection as `blocked_mixed_source_finality`, and every
  non-final finality rejection;
- exhaustive availability mapping for every output key and every contracted
  row state: absent table row, present eligible row, present ineligible row,
  required value present, required value null, false-only boolean set,
  true-containing boolean set, contradictory values, each source
  availability literal, and every unsupported or withheld output family;
- total context, metric, and provenance mapping tables for every input literal,
  null, fallback, conflict, and numeric boundary;
- source/result disagreement and join-conflict failures;
- provenance severity, evidence-status, degradation, ledger, and source-surface
  mapping tests;
- unknown provenance and path-shaped surface failures;
- random package-local pseudonym syntax, no private derivation, and only
  match-game linkage;
- exact timestamp disappearance and quarter/duration boundary tests;
- card/deck/action/private canary rejection and no-echo checks;
- full released-value-vector equivalence tests including availability and
  provenance, deterministic fixed-order generalization, linked-family
  omission to a fixed point, one-way and two-way projections, complementary
  disclosure arithmetic, and every closed `rare_combination_risk` predicate;
- profile-v1 seal schema/cross-field validation, atomic compare-and-publish,
  concurrent single-winner issuance, pre-commit rollback, ambiguous-commit
  fail-closed behavior, permanent post-commit sealing, and rejection of every
  second generation attempt without reading SQLite or private source data;
- deterministic canonical serialization with injected synthetic pseudonyms;
- immutable package-lifecycle cross-field tests and every permitted and
  prohibited append-only lifecycle transition, including sequence gaps,
  forks, duplicate or replayed records, invalid references, recorded-time or
  effective-time regression, every supersession literal/reference rejection,
  reactivation, `expired_pending_record`, deletion confirmation, stale transfer
  evidence, exact seal binding, and atomic current-state recheck;
- exact non-claim list tests;
- aborted-attempt cleanup and no durable mapping tests; and
- proof that no network, external write, raw artifact, or repository commit is
  needed.

Tests must not open a real database, Player.log, JSONL file, workbook export,
local app data, private path, or other arbitrary user file.

## Validation Expectations For This Contract

Codex B validation is docs-only:

```powershell
py tools/check_agent_docs.py
py tools/check_protected_surfaces.py --base origin/main
py tools/check_secret_patterns.py --base origin/main
git diff --check
```

Validation confirms document structure and scans only. It does not prove
sanitization, anonymity, privacy, parser correctness, implementation readiness,
or access safety.

## Protected Surfaces And Stop Conditions

Stop and route to the owner or owning repository if:

- SQLite, private dataset, raw artifact, or arbitrary file access is requested;
- the source schema or R&D schema differs from the bound versions;
- a table, column, enum, provenance label, card/deck field, identifier,
  timestamp, path, free text, or output field is outside this contract;
- R&D is asked to sanitize unsanitized input;
- exact generation or transfer approval is missing, stale, expired, revoked,
  contradictory, or for another release;
- the profile-v1 seal is missing, invalid, ambiguous, already issued, or cannot
  be updated atomically with package and initial-lifecycle visibility;
- a package has a small-cell, complementary, or rare-combination risk;
- a local package, profile seal, lifecycle chain, or pseudonym map would be
  committed or retained improperly;
- parser truth, identity, deduplication, final reconciliation, analytics schema,
  workbook/webhook/Apps Script, external integration, AI, deployment, or
  production behavior would change; or
- anyone treats contract review or validation as Codex C, access, transfer,
  truth, readiness, security, or privacy authority.

## Codex E Finding Reconciliation

This revision preserves the two confirmed fixes and responds only to the two
remaining blocking findings in
`docs/contract_test_reports/core_sanitized_parser_fact_producer_boundary.md`.
The existing review report remains independent review evidence and is not
rewritten by Codex B.

| finding | revision | Codex B status |
| --- | --- | --- |
| `CT-731-E-001` | Exhaustive availability reducers and per-key mappings were confirmed by Codex E. This revision does not alter them. | `fixed_state_confirmed` |
| `CT-731-E-002` | Uniform contributor finality and fail-closed mixed-finality handling were confirmed by Codex E. This revision does not alter them. | `fixed_state_confirmed` |
| `CT-731-E-003` | Preserves the accepted append-only lifecycle model, requires nondecreasing effective times, fixes both supersession references to `none`, and rejects all supersession statuses/reasons in profile v1. The permanent seal issuance transaction atomically publishes one package plus its initial lifecycle record, so no reciprocal supersession first-write dependency remains. | `revised_ready_for_codex_e_confirmation` |
| `CT-731-E-004` | Removes the impossible prior-source-ID overlap check and replaces it with one permanent source-ID-free release seal for the entire profile version. A second profile-v1 release is impossible even after expiry, revocation, or deletion. | `revised_ready_for_codex_e_confirmation` |

These are proposed contract corrections pending independent confirmation. They
do not close any finding, authorize implementation, or change any false
authority flag.

## Acceptance Criteria

- [x] Core is the only v1 producer and R&D never receives raw input to sanitize.
- [x] The source schema, table allowlist, column allowlist, and finality rules are closed.
- [x] The R&D local-dataset schema is reproduced as the only output interface.
- [x] Source-to-category mappings are total and versioned.
- [x] Pseudonyms are random, release-local, non-derived, and not recoverable outside ephemeral producer memory.
- [x] Exact timestamps become quarter/duration buckets only.
- [x] Card/deck/action content and non-match/game linkage are prohibited.
- [x] Provenance, uncertainty, finality, drift, and review status have deterministic mappings.
- [x] Small-cell, complementary, and rare-combination controls are exact.
- [x] Lifecycle, retention, revocation, expiry, deletion, incident routing, and
      effective-time ordering are closed; supersession is explicitly unsupported.
- [x] Profile v1 can issue only one package and retains no cross-release source membership.
- [x] No-echo and package validation rules fail closed.
- [x] Generation and transfer require separate future owner approvals.
- [x] This contract does not authorize SQLite access, implementation, package generation, transfer, R&D access, Codex C, or downstream activation.

## Unresolved Questions

No contract ambiguity is intentionally left for implementation. Operational
values still requiring future owner decisions are:

- the exact approved purpose ID;
- generation and access operators;
- approval and expiry timestamps;
- retention period;
- one exact source database instance;
- one exact package release; and
- the local storage mechanism and path, which must remain private and must be
  named only in owner-controlled execution authority, never in repo artifacts.

These are gated instance values, not permission to fill them now.

## Next Workflow Action

Next role: **Codex E, independent contract reviewer**.

Codex E should preserve the confirmed state of `CT-731-E-001` and
`CT-731-E-002`, then re-review only `CT-731-E-003` and `CT-731-E-004`. It must
verify the permanent single-release seal, fail-closed supersession boundary,
nondecreasing effective times, false-authority flags, and alignment with the
merged R&D contract. Passing review must not route directly to Codex C. The
owner must separately authorize any implementation-contract or execution work.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Independent Module Contract Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/731

Contract:
docs/contracts/core_sanitized_parser_fact_producer_boundary.md

Cross-repository predecessor:
Tahjali11/Mythic-Edge-Research-and-Development PR #22, merge commit
951a9c11422758e76ac553a5ad466dafa40f0b05

Review the Core producer contract against issue #731, the merged R&D consumer
contract, current analytics schema/migration, accepted ADRs, and repo workflow.
Lead with findings ordered by severity.

Verify:
- that the confirmed fixes for `CT-731-E-001` and `CT-731-E-002` remain intact;
- whether `CT-731-E-003` is fixed by nondecreasing lifecycle effective times,
  exact `none` supersession fields, rejection of all supersession transitions,
  and atomic publication of the seal/package/initial lifecycle record;
- whether `CT-731-E-004` is fixed by the permanent profile-v1 single-release
  seal without source IDs, membership hashes, or retained mapping state;
- exact schema/table/column/finality closure;
- exhaustive per-key availability mappings for absent, present, null, false,
  contradictory, ineligible, withheld, and unsupported states;
- uniform contributor finality and fail-closed mixed-finality handling;
- parser truth and provenance preservation;
- random package-local pseudonyms and no recovery-map transfer;
- timestamp, card/deck, linkage, complete released-vector disclosure, and
  no-echo controls;
- immutable issuance plus append-only lifecycle schema, transition, replay,
  effective-time, current-state, retention, revocation, expiry, and deletion
  rules, with supersession explicitly unsupported;
- separate generation and transfer approvals;
- exact non-claim and false-authority completeness; and
- that no SQLite/private access, implementation, generation, transfer, R&D
  access, Codex C, or downstream activation is authorized.

Run docs-only validation and create:
docs/contract_test_reports/core_sanitized_parser_fact_producer_boundary.md

Do not access SQLite or private evidence. Do not implement code or tests. Do
not create or transfer a package. Passing review must not authorize Codex C.
```

## instruction_context

```yaml
role: Codex B
risk_tier: high
repo_agents_read: true
issue_or_tracker_read: true
contract_or_handoff_read: true
protected_surfaces:
  - parser truth and final reconciliation
  - local analytics SQLite schema and private facts
  - match and game identity
  - provenance, confidence, finality, and drift
  - card, deck, and strategy privacy
  - cross-repository evidence transfer
  - retention, revocation, and deletion lifecycle
authority_conflicts_found: false
stop_conditions:
  - no SQLite or private dataset access
  - no raw artifact inspection
  - no exporter or sanitizer implementation
  - no package generation or transfer
  - no R&D dataset access
  - no Codex C authority
  - no downstream activation
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: Tahjali11/Mythic-Edge
  issue: https://github.com/Tahjali11/Mythic-Edge/issues/731
  completed_thread: B_contract_revision
  next_thread: E_contract_re_review
  branch: codex/sanitized-parser-fact-producer-boundary-731
  source_artifact: https://github.com/Tahjali11/Mythic-Edge/issues/731
  predecessor_commit: 951a9c11422758e76ac553a5ad466dafa40f0b05
  contract_artifact: docs/contracts/core_sanitized_parser_fact_producer_boundary.md
  risk_tier: high
  selected_producer: Tahjali11/Mythic-Edge
  source_boundary: core_local_analytics_sqlite_parser_normalized_facts
  output_schema: sanitized_parser_fact_local_dataset.v1
  sanitization_profile: core_parser_fact_research_profile.v1
  source_review_artifact: docs/contract_test_reports/core_sanitized_parser_fact_producer_boundary.md
  finding_reconciliation:
    CT-731-E-001: fixed_state_confirmed
    CT-731-E-002: fixed_state_confirmed
    CT-731-E-003: revised_ready_for_codex_e_confirmation
    CT-731-E-004: revised_ready_for_codex_e_confirmation
  decision: contract_revision_ready_for_independent_re_review
  sqlite_access_authorized: false
  private_dataset_access_authorized: false
  implementation_authorized: false
  package_generation_authorized: false
  package_transfer_authorized: false
  r_and_d_dataset_access_authorized: false
  ready_for_codex_c: false
  downstream_activation_authorized: false
  parser_truth_claimed: false
  anonymity_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  next_recommended_role: Codex E independent contract re-reviewer
```
