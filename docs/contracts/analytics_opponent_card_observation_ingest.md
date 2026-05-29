# Analytics Opponent Card Observation Ingest Contract

## Metadata

- role: Codex B / Module Contract Writer
- source_artifact: Codex A workflow handoff for `[analytics] Opponent-card-observation ingest into SQLite`
- current_branch: codex/analytics-foundation
- base_branch: codex/analytics-foundation
- verified_context_commit: 39948ed0f8b5f876371548357672dabdcb07debc
- target_artifact: docs/contracts/analytics_opponent_card_observation_ingest.md
- expected_next_artifact: docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md
- risk_tier: Medium
- status: contract only

## Source Artifacts

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/contracts/analytics_gameplay_action_ingest.md
- docs/contracts/parser_opponent_card_observations.md
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_opponent_card_observations.py

## Purpose

This contract defines the first opponent-card-observation ingest slice for the
Local Analytics Foundation.

Plain English: Mythic Edge already has parser-normalized visible/degraded
opponent-card observation payloads, and the SQLite schema already has
observation tables. This slice should store those parser-produced observations
locally, preserve their source/confidence/degradation labels, and link them to
stored gameplay actions when a deterministic match exists. It must not rebuild
observations from raw gameplay actions, infer hidden cards, alter parser
classification, or make analytics a new truth owner.

## Owning Truth Layer

`src/mythic_edge_parser/app/opponent_card_observations.py` owns the
parser-normalized opponent-card observation fact.

Analytics ingest owns only durable local storage of those facts in SQLite.

Analytics ingest may:

- validate primitive storage types;
- compute deterministic SQLite row IDs;
- link to a stored `gameplay_actions` row when the deterministic source action
  can be found;
- copy parser-owned observation labels into analytics fact rows;
- write fact-provenance rows that point to replay input paths.

Analytics ingest must not:

- call `build_opponent_card_observation()` to reinterpret gameplay actions in
  this slice;
- change `opponent_card_observations.py` behavior;
- change gameplay-action extraction or classification;
- infer hidden cards, complete decklists, sideboard deltas, archetypes,
  strategy, coaching verdicts, or player mistakes;
- move truth into SQLite, workbook formulas, webhook transport, Apps Script,
  Line Tracer, AI output, OpenAI runtime, or model-provider output.

## Observed Repo Behavior

Observed on `codex/analytics-foundation` at
39948ed0f8b5f876371548357672dabdcb07debc:

- SQLite schema v1 exists and includes `opponent_card_observations` and
  `opponent_card_observation_cards`.
- Parser-normalized replay ingest exists in `analytics_ingest.py`.
- Gameplay-action ingest is complete:
  - `_TOUCHED_TABLES` includes `gameplay_actions` and
    `gameplay_action_cards`;
  - `_ingest_gameplay_action_entries(...)` writes parent and child rows;
  - gameplay-action provenance uses
    `tier5.gameplay_action.gameplay_action`.
- `ParserNormalizedReplayInput` already accepts
  `opponent_card_observations`.
- Current ingest still reports `opponent_card_observations` as deferred
  optional input via warnings and `skipped["opponent_card_observations"]`.
- `tests/test_analytics_parser_normalized_replay_ingest.py` and
  `tests/test_analytics_gameplay_action_ingest.py` currently assert that
  opponent observations remain deferred.
- `opponent_card_observations.py` emits observation payloads with object marker
  `mythic_edge_opponent_card_observation` and schema version
  `parser_opponent_card_observations.v1`.
- Existing opponent-observation tests cover clean visible observations,
  observed-vs-canonical identity differences, hidden draw suppression,
  degraded missing identity, candidate/contradicted names, seat conflicts,
  unresolved known IDs, and collection payload counts.

## Public Interface

The implementation should extend the existing module:

```text
mythic_edge_parser.app.analytics_ingest
```

Required public function remains:

```text
ingest_parser_normalized_replay(
    connection: sqlite3.Connection,
    replay: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult
```

Required input location:

```text
replay["opponent_card_observations"]
```

No new CLI, live parser sidecar, raw Player.log reader, saved-event replay
runner, default database opener, Google Sheets sync, webhook sender, Apps
Script interaction, Line Tracer, AI coaching, or OpenAI runtime integration is
authorized.

Allowed private helpers:

- opponent-observation normalizer
- opponent-observation deterministic ID builder
- gameplay-action link resolver
- observation-card child-row builder
- observation provenance writer

Those helpers should remain private unless a future contract promotes them to a
stable public API.

## Input Shape

`replay["opponent_card_observations"]` is a list of individual observation
mappings. The collection payload shape from
`build_opponent_card_observations_payload(...)` is not required as input for
this slice.

Required fields per observation:

- `object`: must be `mythic_edge_opponent_card_observation`
- `schema_version`: must be `parser_opponent_card_observations.v1`
- `match_id`
- `game_number`
- `actor_relation`: must be `opponent`
- `action_type`
- `source_evidence`
- `evidence_status`
- `value_source`
- `confidence`
- `visibility`
- `degradation_flags`
- `review_required`

Required fields may be present with empty string values when the parser helper
uses an empty string to represent unavailable evidence, but storage validation
must still enforce the required type where the database column or downstream
contract needs one.

Optional or nullable fields:

- `timestamp`
- `game_state_id`
- `turn_number`
- `actor_seat_id`
- `local_seat_id`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `name_resolution_source`
- `layout`
- `card_faces`
- `cast_mode`
- `from_zone_type`
- `to_zone_type`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `finality`
- `drift_status`
- `gameplay_action_id`

`layout`, `card_faces`, `raw_action_types`, `annotation_types`, and
`annotation_categories` are allowed input context but do not currently have
dedicated columns in the v1 observation tables. They may be represented through
fact-provenance source payload paths and labels only. This contract does not
authorize schema changes to store them.

## Allowed Values

Allowed `value_source` values:

- `observed`
- `derived`
- `inferred`
- `unknown`
- `conflict`
- `legacy_enriched`

Allowed `confidence` values:

- `high`
- `medium`
- `low`
- `unknown`

Allowed `evidence_status` values:

- `observed`
- `derived`
- `inferred`
- `unknown`
- `conflict`
- `degraded`

Allowed `visibility` values:

- `action_visible`
- `public_zone`
- `revealed`
- `derived_zone_transition`
- `ambiguous`
- `hidden_not_recorded`

`hidden_not_recorded` must not be upgraded into a clean observed fact by
analytics ingest. If a parser-normalized observation payload already contains
that value, ingest may store it with degraded/unknown/conflict labels supplied
by the parser, but it must not infer a card identity from hidden information.

Allowed `finality` values for this slice:

- `reconciled`
- `final`
- `provisional`
- `live`

If `finality` is missing, use `reconciled` for replayed parser-normalized
observations.

Allowed `drift_status` values:

- `none`
- `not_checked`
- `degraded`
- `conflict`
- `missing_expected_evidence`
- `redacted`

If `drift_status` is missing:

- use `conflict` when `evidence_status` is `conflict`;
- use `degraded` when `evidence_status` is `degraded`,
  `degradation_flags` is non-empty, or `review_required` is true;
- otherwise use `not_checked`.

## Table Mapping

### `opponent_card_observations`

Each accepted input mapping must create or update one
`opponent_card_observations` row.

Required mapping:

- `opponent_card_observation_id`: deterministic text ID
- `game_id`: existing deterministic game ID for `match_id` and `game_number`
- `match_id`: input `match_id`
- `game_number`: input `game_number`
- `gameplay_action_id`: linked gameplay action ID when found, otherwise null
- `timestamp`: input `timestamp`, or null
- `game_state_id`: input `game_state_id`, or null
- `turn_number`: input `turn_number`, or null
- `actor_relation`: `opponent`
- `actor_seat_id`: input `actor_seat_id`, or null
- `local_seat_id`: input `local_seat_id`, or null
- `instance_id`: input `instance_id`, or null
- `grp_id`: input `grp_id`, or null
- `observed_grp_id`: input `observed_grp_id`, or null
- `overlay_grp_id`: input `overlay_grp_id`, or null
- `object_source_grp_id`: input `object_source_grp_id`, or null
- `parent_id`: input `parent_id`, or null
- `identity_hint_source`: input `identity_hint_source`, or null
- `card_name`: input `card_name`, or null
- `display_name`: input `display_name`, or null
- `resolution_status`: input `resolution_status`, or null
- `name_resolution_source`: input `name_resolution_source`, or null
- `action_type`: input `action_type`, or null only if contract ambiguity is
  routed back to Codex B
- `cast_mode`: input `cast_mode`, or null
- `source_evidence`: input `source_evidence`
- `evidence_status`: input `evidence_status`
- `visibility`: input `visibility`
- `from_zone_type`: input `from_zone_type`, or null
- `to_zone_type`: input `to_zone_type`, or null
- `degradation_flags`: stable JSON text array copied from input
- `review_required`: 1 when input is true, otherwise 0
- `value_source`: input `value_source`
- `confidence`: input `confidence`
- `finality`: input `finality`, or default described above
- `drift_status`: input `drift_status`, or derived default described above
- `source_parser_surface`: `opponent_card_observations.py`
- `source_fact_key`: deterministic observation ID or source key
- `availability_status`: `available`

### `opponent_card_observation_cards`

Current parser observations describe one primary observed card. Ingest should
write one child row when at least one card identity or card-display field is
present:

- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `identity_hint_source`
- `card_name`

Required child mapping:

- `opponent_card_observation_card_id`: deterministic text ID derived from
  observation ID and `card_ordinal`
- `opponent_card_observation_id`: parent observation ID
- `game_id`: parent game ID
- `card_ordinal`: 1 for the current single-card shape
- `grp_id`: input `grp_id`, or null
- `observed_grp_id`: input `observed_grp_id`, or null
- `overlay_grp_id`: input `overlay_grp_id`, or null
- `object_source_grp_id`: input `object_source_grp_id`, or null
- `identity_hint_source`: input `identity_hint_source`, or null
- `card_name`: input `card_name`, or null
- `resolution_status`: input `resolution_status`, or null
- `visibility`: input `visibility`
- `value_source`: input `value_source`
- `confidence`: input `confidence`
- `finality`: parent finality
- `drift_status`: parent drift status
- `source_parser_surface`: `opponent_card_observations.py`
- `source_fact_key`: parent source fact key
- `availability_status`: `available`

When `degradation_flags` includes `missing_card_identity` and no card identity
or name is present, the parent row must still be inserted. A child row may be
omitted rather than fabricating an unknown card row. The missing identity must
remain visible through the parent `degradation_flags`, `review_required`, and
fact-provenance rows.

Future multi-card observation input is out of scope unless the parser already
supplies an explicit list of card identities. Do not invent multi-card
semantics from a single observation row.

## Gameplay-Action Linking

`opponent_card_observations.gameplay_action_id` is nullable.

Required linking order:

1. If the input observation includes `gameplay_action_id` and that row exists
   in `gameplay_actions`, store it.
2. Otherwise, compute the deterministic gameplay-action candidate from the
   observation fields that overlap the gameplay-action ingest ID contract:
   `match_id`, `game_number`, `game_state_id`, `turn_number`, `action_type`,
   `cast_mode`, `actor_relation`, `instance_id`, `grp_id`,
   `observed_grp_id`, `overlay_grp_id`, `object_source_grp_id`, `parent_id`,
   `from_zone_type`, `to_zone_type`, `raw_action_types`, and
   `annotation_types`.
3. If that candidate row exists in `gameplay_actions`, store the candidate ID.
4. If no deterministic match exists, store null.

When no matching gameplay action exists:

- still insert the opponent observation if its parent game exists;
- still insert eligible child card rows;
- do not create a synthetic gameplay action;
- do not fail solely because the action link is unavailable;
- do not mutate parser-supplied `degradation_flags`, `value_source`,
  `confidence`, `visibility`, or `review_required`;
- do not count the observation as skipped.

If the input explicitly provides a `gameplay_action_id` that does not exist,
Codex C may add a warning, but it must still use null rather than creating an
orphan foreign key.

## Deterministic ID And Upsert Policy

`opponent_card_observation_id` must be deterministic across repeated ingest of
the same normalized replay.

Required ID inputs:

- `match_id`
- `game_number`
- `game_state_id`
- `turn_number`
- `actor_relation`
- `actor_seat_id`
- `local_seat_id`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `action_type`
- `cast_mode`
- `source_evidence`
- `visibility`
- `from_zone_type`
- `to_zone_type`

The ID may use a stable tuple or SHA-256 hash of canonical JSON. It must not
use Python's process-local `hash()`, ingest wall-clock time, local file paths,
display summary text, unordered dictionary stringification, raw Player.log
payload text, or generated artifact paths.

Repeated ingest of the same replay into the same database must:

- keep one parent row per deterministic observation ID;
- keep one child row per deterministic observation/card ordinal;
- avoid duplicate `fact_provenance` rows for the same fact and field;
- preserve row counts after the first successful ingest;
- update mutable display/enrichment fields for the same deterministic fact
  without creating duplicate rows.

## Validation And Error Behavior

Must reject and roll back the whole ingest transaction for:

- non-mapping observation entries;
- missing or blank `match_id`;
- missing, blank, non-integral, boolean, fractional, zero, or negative
  `game_number`;
- missing, wrong, or unsupported `object` or `schema_version`;
- `actor_relation` other than `opponent`;
- missing or unsupported `value_source`, `confidence`, `evidence_status`, or
  `visibility`;
- malformed `degradation_flags` values that are not lists of strings;
- malformed `review_required` values that are not booleans or safe boolean-like
  values;
- boolean, fractional, negative, or non-integral values for numeric identity,
  seat, turn, and game-state fields.

Must fail, not skip, when an observation references an unknown parent game. The
database schema requires a non-null `game_id`, and analytics ingest must not
guess or create parent games outside the parser-normalized match/game rows.

May tolerate as unavailable:

- missing timestamp;
- missing game-state ID;
- missing turn number;
- missing seat IDs, when the parser observation already marks the row degraded;
- missing card identity, when parser observation labels preserve the
  degradation;
- missing gameplay-action link.

## Provenance Requirements

All parent and child provenance rows for this slice must use:

```text
ledger_entry_id = "tier5.opponent_card_observation.opponent_card_observation"
source_parser_surface = "opponent_card_observations.py"
```

Minimum parent `fact_provenance` rows:

- `visibility`
- `evidence_status`
- `value_source`
- `confidence`
- `review_required`
- `degradation_flags`
- `action_type`

Minimum child `fact_provenance` rows when child rows are created:

- `grp_id` when present
- `observed_grp_id` when present and different from `grp_id`
- `card_name` when no numeric card identity is present but a parser display
  name exists

Fact provenance must preserve the observation labels:

- `value_source`: from the observation row
- `confidence`: from the observation row
- `finality`: from the observation row or default
- `drift_flags`: JSON array derived from `degradation_flags` without raw
  payload text
- `degraded_reason`: compact label when degraded or conflict status exists
- `review_required`: copied from the observation row

Suggested source metadata:

- `source_event_kind`: `GameState` when `game_state_id` is present, otherwise
  null
- `source_event_type`: null unless the replay input supplies a safe parser event
  type label
- `source_payload_paths`: JSON pointer-like labels such as
  `/opponent_card_observations/0/visibility`
- `source_event_timestamp`: observation `timestamp`, or null

Do not store raw Player.log payloads, raw saved-event lines, absolute local
paths, webhook URLs, workbook IDs, API keys, secrets, or private runtime
artifact paths in `fact_provenance`.

## Row Counts, Skips, And Warnings

After implementation:

- `_TOUCHED_TABLES` must include `opponent_card_observations` and
  `opponent_card_observation_cards`.
- Successful ingest of valid `opponent_card_observations` must not add
  `opponent_card_observations` to `result.skipped`.
- Successful ingest of valid observations must remove the current deferred
  warning: `opponent_card_observations are accepted but deferred by the first
  ingest pass`.
- `field_evidence_entries` may remain deferred/skipped unless a later contract
  implements them.
- Malformed observations must fail clearly and roll back instead of being
  reported as skipped.
- Missing deterministic gameplay-action links must not be counted as skipped.

`AnalyticsReplayIngestResult.row_counts` and `ingest_runs.row_counts_json` must
include both opponent observation tables after implementation.

## Tests Required

Codex C should add focused tests, preferably:

```text
tests/test_analytics_opponent_card_observation_ingest.py
```

Required test coverage:

- in-memory SQLite ingest writes `opponent_card_observations` from
  `replay["opponent_card_observations"]`;
- eligible observations write `opponent_card_observation_cards`;
- row counts and `ingest_runs.row_counts_json` include opponent observation
  tables;
- valid observations are no longer reported as deferred/skipped;
- field evidence may still remain deferred/skipped;
- repeated ingest of the same replay is idempotent for parent, child, and
  provenance rows;
- deterministic link to an existing `gameplay_actions` row is stored when
  replay input includes matching `gameplay_action_entries`;
- observations with no matching gameplay action are still stored with
  `gameplay_action_id` null and no synthetic gameplay action;
- parser-supplied `value_source`, `confidence`, `evidence_status`,
  `visibility`, `degradation_flags`, `review_required`, `finality`, and
  `drift_status` are preserved or defaulted according to this contract;
- degraded missing-card observations write a parent row without fabricating card
  identity;
- malformed numeric, enum, object/schema marker, actor relation, and flag inputs
  fail without partial fact rows;
- fact provenance uses the Tier 5 opponent-observation ledger entry and safe
  source payload paths.

Regression tests should keep parser helper behavior unchanged:

```powershell
py -m pytest -q tests/test_opponent_card_observations.py tests/test_gameplay_actions.py
```

Existing deferred-observation assertions in
`tests/test_analytics_parser_normalized_replay_ingest.py` and
`tests/test_analytics_gameplay_action_ingest.py` must be updated to match the
new accepted/written behavior.

## Validation Expectations

Codex C implementation/comparison validation should run:

```powershell
py -m pytest -q tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_opponent_card_observations.py tests/test_gameplay_actions.py
py -m ruff check src tests tools
git diff --check
```

Protected-surface validation should include a path-scoped protected-surface
check for the contract, implementation handoff, `analytics_ingest.py`, and
focused tests.

Contract-writer validation is docs-only:

```powershell
git diff --check
@'
docs/contracts/analytics_opponent_card_observation_ingest.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/analytics_opponent_card_observation_ingest.md` exists.
- The contract names `opponent_card_observations.py` as the parser-normalized
  truth owner.
- The contract defines the required
  `replay["opponent_card_observations"]` input shape.
- The contract maps inputs into `opponent_card_observations` and
  `opponent_card_observation_cards`.
- The contract defines deterministic gameplay-action linking when a matching
  stored action exists.
- The contract defines null-link behavior when no matching gameplay action
  exists.
- The contract defines deterministic IDs and idempotent upsert behavior.
- The contract requires provenance rows using
  `tier5.opponent_card_observation.opponent_card_observation`.
- The contract preserves value source, confidence, evidence status, visibility,
  degradation flags, review-required, finality, and drift labels.
- The contract defines row count, skipped, and warning behavior.
- The contract preserves parser truth ownership and protected surfaces.
- No implementation, parser, schema, migration, fixture, generated database,
  workbook, webhook, Apps Script, runtime, AI, OpenAI runtime, or production
  behavior changes are made in the contract-writing pass.

## Unknowns

- Whether future replay inputs will include an explicit `gameplay_action_id` or
  source action key, avoiding candidate recomputation.
- Whether `layout`, `card_faces`, `raw_action_types`, `annotation_types`, and
  `annotation_categories` will need dedicated analytics columns in a future
  schema migration.
- Whether future observations can include multiple card identities per
  observation.
- Whether future field-evidence ingest will provide stronger finality or drift
  labels than the current observation payload.
- Whether source event type can be safely populated from replay input without
  reading raw saved-event payloads.

## Suspected Implementation Gaps

- `_TOUCHED_TABLES` omits `opponent_card_observations` and
  `opponent_card_observation_cards`.
- `_deferred_optional_warnings(...)` and `_deferred_optional_skips(...)` still
  treat opponent observations as deferred.
- No `_ingest_opponent_card_observations(...)` helper exists.
- No deterministic opponent-observation ID helper exists.
- No gameplay-action link resolver exists for observations.
- No opponent-observation child-card row builder exists.
- Existing fact-provenance helper may need to accept row-specific
  value-source, confidence, drift flags, degraded reason, and review-required
  labels.
- Current focused analytics tests still assert deferred opponent observations.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- opponent-card-observation classification behavior
- gameplay-action extraction/classification behavior
- parser state final reconciliation
- parser event classes
- match/game identity and deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- raw Player.log files or raw private Player.log excerpts
- secrets, credentials, environment variables, webhook URLs, or API keys
- generated SQLite database files
- generated card data
- runtime status files
- failed posts
- workbook exports
- Google Sheets sync
- Line Tracer
- AI coaching
- OpenAI runtime integration
- model-provider behavior
- production behavior
- main branch targeting without explicit approval

## Out Of Scope

- Creating migration files or changing schema columns.
- Creating a SQLite database file.
- Implementing live parser sidecar ingest.
- Reading raw Player.log or saved-event JSONL files directly.
- Rebuilding opponent observations from gameplay actions.
- Changing `opponent_card_observations.py`.
- Changing `gameplay_actions.py`.
- Ingesting card movements, public zone observations, life totals, turns, or
  field evidence.
- Creating analytics summary tables.
- Refreshing fixtures, snapshots, or baselines.
- Adding hidden-card inference, complete-decklist inference, sideboard deltas,
  archetype labels, coaching verdicts, or player-mistake labels.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the analytics opponent-card-observation ingest contract.

Branch:
codex/analytics-foundation

Source artifact:
docs/contracts/analytics_opponent_card_observation_ingest.md

Current verified context:
- SQLite schema v1, migration loader, parser-normalized replay ingest, and gameplay-action ingest are complete.
- Verified commit: 39948ed0f8b5f876371548357672dabdcb07debc.
- opponent_card_observations are currently accepted by analytics replay input but still deferred/skipped.

Goal:
Compare current analytics replay ingest against the contract and implement the narrow opponent-card-observation ingest slice. Produce docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what opponent-card-observation ingest is supposed to do, what current code actually does, why the gap exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_opponent_card_observation_ingest.md
- docs/contracts/analytics_gameplay_action_ingest.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/parser_opponent_card_observations.md
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_opponent_card_observations.py

Implement only:
- replay["opponent_card_observations"] ingestion into opponent_card_observations and opponent_card_observation_cards
- deterministic opponent-observation and child-card IDs
- deterministic link to existing gameplay_actions when a matching action exists
- null-link storage when no matching gameplay action exists
- row-count/skipped/warning updates for opponent observation tables
- provenance rows using tier5.opponent_card_observation.opponent_card_observation
- focused tests for observation ingest, idempotency, action linking, null-link behavior, malformed inputs, label preservation, and safe provenance paths
- docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md

Do not:
- change parser behavior
- change opponent-card-observation classification behavior
- change gameplay-action extraction/classification behavior
- change parser state final reconciliation
- change parser event classes
- change match/game identity or deduplication
- change workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, generated SQLite files, or local runtime artifacts
- create migration files or alter schema
- rebuild observations from raw gameplay actions
- implement live ingest, Google Sheets sync, Line Tracer, AI coaching, or OpenAI runtime behavior
- target main or open a PR

Validation:
py -m pytest -q tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_opponent_card_observations.py tests/test_gameplay_actions.py
py -m ruff check src tests tools
git diff --check

Final handoff must include:
- role performed
- source artifact used
- files changed
- exact function/test sections changed
- what was verified
- what remains unverified
- whether any forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Codex A workflow handoff for [analytics] Opponent-card-observation ingest into SQLite"
  target_artifact: "docs/contracts/analytics_opponent_card_observation_ingest.md"
  branch: "codex/analytics-foundation"
  base_branch: "codex/analytics-foundation"
  verified_context_commit: "39948ed0f8b5f876371548357672dabdcb07debc"
  risk_tier: "Medium"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_opponent_card_observation_ingest.md"
  stop_conditions:
    - "Do not implement code in the contract writer pass."
    - "Do not change parser behavior or opponent-card-observation classification behavior."
    - "Do not change gameplay-action behavior."
    - "Do not alter schema, migrations, workbook schema, webhook payload shape, or Apps Script behavior."
    - "Do not create SQLite files or store raw Player.log data."
    - "Do not add live ingest, Google Sheets sync, Line Tracer, AI/OpenAI behavior, or production behavior."
    - "Do not target main or open a PR."
```
