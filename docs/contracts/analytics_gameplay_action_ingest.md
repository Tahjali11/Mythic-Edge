# Analytics Gameplay Action Ingest Contract

## Metadata

- role: Codex B / Module Contract Writer
- source_artifact: Codex A workflow handoff for `[analytics] Define gameplay-action ingest into SQLite`
- current_branch: codex/analytics-foundation
- target_branch: codex/analytics-foundation
- target_artifact: docs/contracts/analytics_gameplay_action_ingest.md
- expected_next_artifact: docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md
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
- docs/contracts/analytics_migration_loader.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
- docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_fixer.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_schema.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py

## Purpose

This contract defines the first gameplay-action ingest slice for the Local
Analytics Foundation.

Plain English: the parser already produces gameplay-action entries, and the
analytics schema already has tables for those entries. The missing step is a
narrow, deterministic import path from parser-normalized replay input into
SQLite. That import may store parser-owned gameplay-action facts, but it must
not reclassify actions, guess hidden information, alter parser behavior, or
turn analytics into a new truth owner.

## Ownership Boundary

Parser/state and `src/mythic_edge_parser/app/gameplay_actions.py` own
gameplay-action interpretation. Analytics ingest owns only durable local
storage of parser-normalized gameplay-action rows.

The analytics layer may:

- validate and normalize primitive storage types;
- derive deterministic SQLite row IDs from already-normalized parser values;
- copy parser-owned labels into analytics fact tables;
- attach storage-level provenance labels and fact-provenance rows.

The analytics layer must not:

- reinterpret `action_type`;
- infer missing actions, hidden cards, sideboard state, archetypes, strategy, or
  player mistakes;
- modify `gameplay_actions.py` extraction or classification behavior;
- become workbook, webhook, Apps Script, AI, Line Tracer, or coaching truth.

## Observed Repo Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- `src/mythic_edge_parser/app/analytics_ingest.py` exists and exposes
  `ingest_parser_normalized_replay(...)`.
- `ParserNormalizedReplayInput` already accepts optional
  `gameplay_action_entries`, `opponent_card_observations`, and
  `field_evidence_entries`.
- Current ingest writes match, game, context, opening-hand, mulligan, and
  `fact_provenance` rows.
- Current ingest still treats `gameplay_action_entries` as deferred optional
  payloads: it reports warnings and `skipped["gameplay_action_entries"]`
  instead of writing `gameplay_actions` or `gameplay_action_cards`.
- `_TOUCHED_TABLES` does not yet include `gameplay_actions` or
  `gameplay_action_cards`.
- Existing ingest tests assert that deferred optional payloads are reported as
  skipped.
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
  already creates `gameplay_actions`, `gameplay_action_cards`, supporting
  indexes, and `v_opening_lines`.
- `src/mythic_edge_parser/app/gameplay_actions.py` emits action entries with
  match/game identity, timestamp, game state id, turn number, action type, cast
  mode, instance/card identity hints, actor relation, zone movement, raw action
  labels, annotation labels, rendered names, visibility, and summaries.
- `gameplay_actions.py` deduplicates runtime action entries with a stable JSON
  key over game number, game state id, turn number, action type, instance id,
  `grp_id`, and zone movement.
- `src/mythic_edge_parser/app/opponent_card_observations.py` consumes
  gameplay-action entries to build downstream opponent-card observations, but
  opponent-card-observation ingest remains outside this slice.

## Public Interface

The implementation should extend the existing module:

```text
mythic_edge_parser.app.analytics_ingest
```

Required public constant remains:

```text
ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION = "analytics_parser_normalized_replay_ingest.v1"
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

This contract does not require a new CLI, default database opener, live sidecar,
saved-event replay runner, or raw Player.log reader.

Allowed private helpers:

- gameplay-action row normalizer
- gameplay-action deterministic ID builder
- gameplay-action card child-row builder
- gameplay-action provenance writer
- list-to-storage-text helper if existing helpers are insufficient

Those helpers should stay private unless a later contract needs them as stable
public API.

## Input Contract

`gameplay_action_entries` is an optional list of parser-normalized mappings
inside the existing `ParserNormalizedReplayInput`.

Required per action entry:

- `match_id`
- `game_number`
- `action_type`

Recommended per action entry when available:

- `timestamp`
- `game_state_id`
- `turn_number`
- `cast_mode`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `actor_relation`
- `from_zone_type`
- `to_zone_type`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `visible_in_log`
- `card_name`
- `display_name`
- `resolution_status`

Accepted source values must come from parser-normalized replay artifacts or
sanitized/synthetic fixtures. Ingest must not read raw Player.log files, runtime
status files, local action JSON/Markdown artifacts, workbook exports, or failed
posts directly.

## Storage Contract

Gameplay-action ingest may write only these new table families in this slice:

- `gameplay_actions`
- `gameplay_action_cards`
- additional `fact_provenance` rows for gameplay actions and associated card
  identity facets

Existing match/game parent writes from the parser-normalized replay ingest remain
in scope because `gameplay_actions.game_id` and `gameplay_actions.match_id`
reference those parent facts.

`_TOUCHED_TABLES` must include `gameplay_actions` and
`gameplay_action_cards` after implementation so `AnalyticsReplayIngestResult`
and `ingest_runs.row_counts_json` report the new writes.

No stored summary table is authorized. Existing SQL views may remain unchanged
unless a focused test reveals they already fail against correctly ingested
gameplay-action rows.

## Gameplay Actions Table Mapping

Each accepted action entry must create or update one `gameplay_actions` row.

Required column mapping:

- `gameplay_action_id`: deterministic text ID
- `game_id`: deterministic game ID used by existing ingest for the same
  `match_id` and `game_number`
- `match_id`: entry `match_id`
- `game_number`: entry `game_number`
- `timestamp`: entry `timestamp`, or null when unavailable
- `game_state_id`: entry `game_state_id`, or null when unavailable
- `turn_number`: entry `turn_number`, or null when unavailable
- `action_type`: entry `action_type`
- `actor_relation`: one of `local`, `opponent`, `unknown`, or ``
- `from_zone_type`: entry `from_zone_type`, or null when unavailable
- `to_zone_type`: entry `to_zone_type`, or null when unavailable
- `source_status`: storage-level status such as `parser_normalized`
- `annotation_context_label`: compact non-raw label derived from annotation
  categories when available, otherwise null
- `raw_action_type_labels`: stable text representation of `raw_action_types`
- `annotation_type_labels`: stable text representation of `annotation_types`
- `visible_in_log`: 1, 0, or null

Core provenance columns must use the existing analytics vocabulary:

- `value_source`: `derived` unless later field-evidence input justifies a more
  precise label
- `confidence`: `unknown` unless later field-evidence input justifies stronger
  confidence
- `finality`: `reconciled` for replayed final parser rows unless source input
  explicitly represents live/provisional facts
- `drift_status`: `not_checked`
- `parser_schema_version`: current analytics schema version
- `ingest_run_id`: current ingest run ID
- `source_parser_surface`: `gameplay_actions.py`
- `source_fact_key`: deterministic gameplay-action fact key
- `availability_status`: `available`

`cast_mode` is currently parser-normalized input but no dedicated
`gameplay_actions` column exists. It may contribute to deterministic ID,
`source_fact_key`, `fact_provenance`, or a future migration, but this contract
does not authorize schema changes solely to add `cast_mode`.

## Gameplay Action Cards Table Mapping

When an action entry includes any card identity evidence, ingest must create or
update child rows in `gameplay_action_cards`.

Card identity evidence includes at least one of:

- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `card_name`
- `display_name`

For current parser-normalized action entries, at most one child card row is
expected. Store it with `card_ordinal = 1`. If future parser-normalized entries
contain a list of associated cards, store one child row per card with stable
1-based ordinals and do not collapse multiple cards into delimited text.

Required child mapping:

- `gameplay_action_card_id`: deterministic text ID derived from
  `gameplay_action_id` and `card_ordinal`
- `gameplay_action_id`: parent action ID
- `game_id`: parent game ID
- `card_ordinal`: 1-based ordinal
- `instance_id`: entry `instance_id`, or null
- `grp_id`: entry canonical `grp_id`, or null
- `observed_grp_id`: entry `observed_grp_id`, or null
- `overlay_grp_id`: entry `overlay_grp_id`, or null
- `object_source_grp_id`: entry `object_source_grp_id`, or null
- `identity_hint_source`: entry `identity_hint_source`, or null
- `card_name`: entry `card_name`, or null
- `display_name`: entry `display_name`, or null
- `name_resolution_status`: entry `resolution_status`, or null
- `enrichment_status`: compact label such as `parser_rendered`,
  `name_only`, `unresolved_id`, or null

Child rows inherit the same conservative core provenance labels as the parent
unless the entry has field-specific labels.

An action without card identity evidence must still write the parent action row
and must not fabricate a card child row.

## Deterministic ID And Idempotency

`gameplay_action_id` must be deterministic across repeated ingest of the same
normalized replay.

Required ID inputs:

- `match_id`
- `game_number`
- `game_state_id`
- `turn_number`
- `action_type`
- `actor_relation`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `object_source_grp_id`
- `from_zone_type`
- `to_zone_type`
- stable representations of `raw_action_types` and `annotation_types`

Implementation may use a stable tuple or a SHA-256 hash of canonical JSON. It
must not use Python's process-local `hash()`.

The ID policy should be at least as specific as the current
`gameplay_actions._action_key(...)` runtime dedupe key. Codex C may include more
fields when needed to avoid collapsing distinct parser-emitted actions, but it
must not include volatile fields such as local file paths, generated summary
text, unordered dictionary stringification, or wall-clock ingest time.

Repeated ingest of the same replay into the same database must:

- keep one parent row per deterministic action ID;
- keep one child card row per deterministic action/card ordinal;
- avoid duplicate `fact_provenance` rows for the same fact/field;
- produce stable row counts after the first successful ingest.

## Validation And Degradation Rules

Malformed `gameplay_action_entries` must fail clearly and roll back the whole
ingest transaction when they would corrupt parser-owned numeric or identity
state.

Must reject:

- non-mapping action entries;
- missing or blank `match_id`;
- missing, blank, non-integral, boolean, fractional, zero, or negative
  `game_number`;
- missing or blank `action_type`;
- boolean, fractional, negative, or non-integral values for `game_state_id`,
  `turn_number`, `instance_id`, `grp_id`, `observed_grp_id`, `overlay_grp_id`,
  `object_source_grp_id`, and `card_ordinal`;
- `actor_relation` values outside `local`, `opponent`, `unknown`, or ``.

May tolerate as unavailable:

- missing timestamp;
- missing turn number;
- missing game state id;
- missing actor relation, normalized to `` or `unknown`;
- missing zone labels;
- missing card identity for parent action rows;
- missing card names when numeric identity is present.

Required parent integrity:

- A gameplay action must reference a known game parent from the same ingest
  input or an already-existing database row with the same deterministic game ID.
- If parent game identity cannot be established, ingest must fail rather than
  create an orphan or guessed parent.

## Provenance Requirements

Gameplay-action ingest must write `fact_provenance` rows for at least:

- parent `gameplay_actions.action_type`
- parent `gameplay_actions.actor_relation`
- parent `gameplay_actions.from_zone_type` and `to_zone_type` when either is
  present
- child `gameplay_action_cards.grp_id` when present
- child `gameplay_action_cards.instance_id` when present and `grp_id` is absent

Fact provenance must use labels and payload-path references, not raw payload
copies. Examples:

- `source_parser_surface`: `gameplay_actions.py`
- `source_fact_key`: the deterministic gameplay-action source key
- `source_event_kind`: `GameState` when known, otherwise null
- `source_event_type`: `GREMessageType_GameStateMessage` when known, otherwise
  null
- `source_payload_paths`: JSON list of label paths such as
  `/gameplay_action_entries/0/action_type`

`ledger_entry_id` may remain null until the analytics ingest layer is explicitly
connected to the evidence-ledger schema. If Codex C can safely reference the
existing broad Tier 5 gameplay-action ledger entry without importing ledger
runtime behavior, it may use:

```text
tier5.gameplay_action.gameplay_action
```

Do not store raw Player.log payloads, raw saved-event lines, absolute local
paths, webhook URLs, workbook IDs, API keys, or private runtime artifact paths in
`fact_provenance`.

## Opponent-Card-Observation Boundary

Opponent-card-observation ingest is not part of this contract.

After this slice:

- `gameplay_action_entries` should no longer be reported as deferred/skipped
  when accepted and written.
- `opponent_card_observations` may remain deferred/skipped.
- `field_evidence_entries` may remain deferred/skipped unless Codex C needs a
  narrow parser-label mapping to satisfy gameplay-action provenance without raw
  evidence.

Do not implement opponent-card-observation table writes in this slice. Do not
change `opponent_card_observations.py` behavior.

## Tests Required

Codex C should add focused tests, preferably in a new file:

```text
tests/test_analytics_gameplay_action_ingest.py
```

Focused required coverage:

- in-memory SQLite ingest writes `gameplay_actions` and
  `gameplay_action_cards` from `gameplay_action_entries`;
- `_TOUCHED_TABLES`, result `row_counts`, and `ingest_runs.row_counts_json`
  include gameplay tables;
- replaying the same normalized input is idempotent for parent rows, child rows,
  and gameplay provenance rows;
- action entries without card identity write parent rows and no child card rows;
- actor relation accepts `local`, `opponent`, `unknown`, and `` only;
- fractional, boolean, negative, and non-integral numeric action fields fail
  without partial fact rows;
- missing parent game identity fails clearly without orphan rows;
- `fact_provenance` uses source labels and payload paths, not raw payload copies;
- `opponent_card_observations` still remain deferred/skipped unless separately
  contracted.

Focused regression coverage should keep existing parser action tests green:

```powershell
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
```

## Validation Expectations

Codex C implementation/comparison validation should run:

```powershell
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
```

Protected-surface validation should include a path-scoped protected-surface
check for the contract, handoff, implementation module, and focused tests.

Contract-writer validation is docs-only:

```powershell
git diff --check
@'
docs/contracts/analytics_gameplay_action_ingest.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/analytics_gameplay_action_ingest.md` exists.
- The contract identifies current deferred/skipped gameplay-action ingest
  behavior.
- The contract extends the existing `analytics_ingest` replay interface instead
  of inventing a new runner.
- The contract defines `gameplay_actions` and `gameplay_action_cards` storage
  expectations.
- The contract defines deterministic ID and replay idempotency requirements.
- The contract defines malformed numeric, actor relation, parent-game, and
  missing-card degradation behavior.
- The contract requires fact provenance without raw payload storage.
- The contract keeps opponent-card-observation ingest deferred.
- The contract preserves parser truth ownership and protected surfaces.
- No implementation, migration, fixture, schema, parser, workbook, webhook, Apps
  Script, runtime, generated-data, or production behavior changes are made in
  the contract-writing pass.

## Unknowns

- Whether future parser-normalized replay artifacts will carry raw action-entry
  array indexes that should be included in deterministic IDs.
- Whether `cast_mode` should eventually receive a dedicated SQLite column or
  remain provenance/context until a future migration contract.
- Whether future gameplay action entries will contain multiple card identities
  per action.
- Whether field-evidence entries should later provide stronger confidence and
  finality labels for gameplay-action facts.
- Whether `source_event_kind` and `source_event_type` can be reliably populated
  from current replay inputs without reading raw saved events.

## Suspected Implementation Gaps

- `_TOUCHED_TABLES` omits `gameplay_actions` and `gameplay_action_cards`.
- `ingest_parser_normalized_replay(...)` currently computes skip/warning counts
  for gameplay action entries before any gameplay ingestion.
- No `_ingest_gameplay_action_entries(...)` helper exists.
- No deterministic gameplay-action SQLite ID helper exists.
- No gameplay-action-card child-row builder exists.
- Existing analytics ingest tests expect gameplay actions to remain skipped, so
  they will need a focused update.
- Existing fact-provenance helper may be too coarse for multiple gameplay action
  fields unless Codex C expands it carefully.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- gameplay-action extraction/classification behavior
- `src/mythic_edge_parser/app/gameplay_actions.py` runtime output behavior
- opponent-card-observation behavior
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
- Ingesting opponent-card observations.
- Ingesting card movements, public zone observations, life totals, or turns.
- Creating analytics summary tables.
- Refreshing fixtures, snapshots, or baselines.
- Changing existing parser action classification.
- Adding hidden-card inference, complete-decklist inference, sideboard deltas,
  archetype labels, coaching verdicts, or player-mistake labels.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the analytics gameplay-action ingest contract.

Branch:
codex/analytics-foundation

Source artifact:
docs/contracts/analytics_gameplay_action_ingest.md

Goal:
Compare the current analytics replay ingest implementation against the contract and implement the narrow gameplay-action ingest slice. Produce docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what gameplay-action ingest is supposed to do, what the current implementation actually does, why the gap exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_gameplay_action_ingest.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_schema.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py

Implement only:
- gameplay_action_entries ingestion into gameplay_actions and gameplay_action_cards
- deterministic gameplay-action and child-card IDs
- row-count/skipped/warning updates for gameplay tables
- focused tests for gameplay-action ingest, idempotency, malformed inputs, parent integrity, and provenance labels
- docs/implementation_handoffs/analytics_gameplay_action_ingest_comparison.md

Do not:
- change parser behavior
- change gameplay-action extraction/classification behavior
- change opponent-card-observation behavior
- change parser state final reconciliation
- change parser event classes
- change match/game identity or deduplication
- change workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, generated SQLite files, or local runtime artifacts
- create migration files unless a concrete schema bug blocks the contract
- ingest opponent_card_observations
- target main without explicit approval

Validation:
py -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
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

workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  source_artifact: "Codex A workflow handoff for [analytics] Define gameplay-action ingest into SQLite"
  target_artifact: "docs/contracts/analytics_gameplay_action_ingest.md"
  branch: "codex/analytics-foundation"
  target_branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  next_recommended_role: "Codex C: Module Implementer / comparison thread"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change gameplay-action extraction/classification behavior."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, workbook schema, webhook payload shape, or Apps Script behavior."
    - "Do not read or store raw Player.log payloads, secrets, generated DBs, runtime artifacts, failed posts, or workbook exports."
    - "Do not implement opponent-card-observation ingest in this slice."
    - "Do not target main without explicit approval."
