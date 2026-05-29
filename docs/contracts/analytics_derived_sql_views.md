# Analytics Derived SQL Views Contract

## Module

Local Analytics Foundation derived SQL views.

This contract defines the narrow read-only SQLite view layer for deterministic
analytics summaries over already-ingested local Mythic Edge facts. It does not
authorize new parser behavior, runtime behavior, workbook/webhook/App Script
behavior, Match Journal behavior, overlay behavior, AI output, coaching, or
raw Player.log storage.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/191>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/190>

## Branch

`codex/analytics-foundation`

Inspected local/remote head:

```text
77a4cd3045d3326f4583c6c9579afb758c987020
```

## Risk Tier

Medium-High.

Reason: SQL views are read-only, but they shape the first stable analytics
query surface for future dashboards, reports, and review workflows. The views
must not quietly convert missing, degraded, human-entered, or parser-derived
values into parser truth, gameplay advice, or model-ready claims.

## Owning Layer

Primary owner: local analytics foundation.

Truth boundaries:

- Parser/state owns parser-managed match, game, card, gameplay, and final
  reconciliation truth.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  degradation, and review vocabulary.
- SQLite analytics tables own local durable storage of parser-normalized facts,
  human annotations, and field evidence.
- Derived SQL views own deterministic, read-only query projections and
  aggregations over local SQLite tables.
- Derived SQL views do not own parser truth, evidence-ledger truth, runtime
  status truth, workbook truth, webhook truth, Apps Script truth, Match Journal
  truth, overlay truth, AI truth, coaching truth, merge readiness, or deploy
  readiness.

Plain English: these views may summarize what the local analytics database
already says. They may not decide what happened in Arena, guess hidden facts,
or tell the player what they should have done.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_derived_sql_views.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_derived_views.py`
- focused updates to `tests/test_analytics_schema.py`
- focused updates to `tests/test_analytics_migration_loader.py` only if view
  existence expectations change
- `docs/implementation_handoffs/analytics_derived_sql_views_comparison.md`

Not owned by this contract:

- parser modules
- parser state final reconciliation
- parser event classes
- runtime status schemas
- output transport
- workbook schema, webhook payloads, or Apps Script mappings
- Match Journal, overlay, SQLite sync services, Google Sheets sync, CI gates,
  merge policy, deploy policy, OpenAI/model-provider behavior, and AI
  coaching surfaces

## Public Interface

The public interface is the set of SQLite views created by the analytics schema
migration.

Current view names already present on the branch and approved to remain:

- `v_opening_hand_cards`
- `v_opening_lines`
- `v_mulligan_outcomes`
- `v_game1_vs_postboard`
- `v_play_draw_splits`
- `v_sample_size_warnings`
- `v_matchup_label_performance`

Additional view names approved for Codex C if current views do not provide the
required review surfaces:

- `v_gameplay_action_review`
- `v_opponent_card_observation_review`

Codex C may satisfy the contract by strengthening existing views and adding the
two approved review views. It must not add broad new analytics families, stored
summary tables, materialized tables, triggers, functions, or runtime APIs in
this slice.

## Observed Current Behavior

- Issue #191 and tracker #190 are open.
- The local branch is clean at `codex/analytics-foundation`, matching
  `origin/codex/analytics-foundation` at `77a4cd3`.
- `docs/contracts/analytics_derived_sql_views.md` did not exist before this
  contract.
- The branch already has a migration loader and
  `0001_initial_analytics_schema.sql`.
- The initial migration already creates the seven current views listed above.
- `tests/test_analytics_schema.py` requires those seven views to exist.
- `tests/test_analytics_migration_loader.py` smoke-checks that at least
  `v_opening_hand_cards` and `v_play_draw_splits` exist after migration.
- Current focused tests do not prove view-level behavior for opening-hand
  rows, opening lines, mulligan outcomes, game1/postboard splits, play/draw
  win-rate math, sample-size labels, matchup-label summaries, gameplay-action
  review, opponent-observation review, provenance visibility, degraded values,
  unknown values, or privacy boundaries.
- Current `v_play_draw_splits` groups by play/draw and computes win rate from
  `game_results.local_result`, but it appears to treat every non-win value as
  a loss and does not surface unknown-result counts.
- Current row-level views expose some provenance fields, but not consistently
  the full core review context available on parser fact tables.
- There is no dedicated view for all gameplay action review rows.
- There is no dedicated view for opponent-card-observation review rows.

## Required Decision

Derived SQL views are approved in this slice.

Implementation should proceed as a read-only, deterministic view/test update on
the unmerged analytics foundation branch. Because `0001_initial_analytics_schema.sql`
is still part of the active analytics foundation branch and has not been
integrated to the project baseline, Codex C should update the initial
migration's view definitions rather than create a follow-up migration, unless
the current branch policy has changed before implementation starts.

If Codex C finds the initial migration has already been treated as immutable by
a later merged branch, it must stop and route back to Codex B for a migration
versioning contract before adding a new migration.

## Inputs

Allowed source tables and local artifacts:

- `matches`
- `games`
- `match_results`
- `game_results`
- `match_context`
- `rank_snapshots`
- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `mulligan_bottomed_or_discarded_cards`
- `gameplay_actions`
- `gameplay_action_cards`
- `opponent_card_observations`
- `opponent_card_observation_cards`
- `fact_provenance`
- human annotation tables:
  - `matchup_labels`
  - `archetype_labels`
  - `game_notes`

Allowed source views:

- Existing analytics views may read from other analytics views only when the
  dependency is deterministic, read-only, and tested.

Forbidden inputs:

- raw Player.log payloads
- local raw logs or log paths
- saved private Player.log excerpts
- generated SQLite database files
- generated card data files
- runtime status files
- failed-post artifacts
- workbook exports
- webhook payloads
- Apps Script state
- Google Sheets live data
- overlay or Match Journal runtime state
- OpenAI/model-provider output
- hidden-card inference, decklist completion, archetype classification, player
  mistake labels, gameplay advice, or coaching text

## Outputs

Allowed outputs:

- SQLite `CREATE VIEW` definitions in the source-controlled analytics schema
  migration.
- Read-only query result rows returned by SQLite.
- Focused tests that create in-memory SQLite databases, insert deterministic
  test rows, and assert exact view behavior.
- Implementation handoff documentation.

Forbidden outputs:

- committed `data/analytics/mythic_edge.sqlite3`
- committed SQLite `-wal`, `-shm`, journal, temporary, or private database
  artifacts
- committed raw Player.log excerpts or private local logs
- workbook schema changes
- webhook payload changes
- Apps Script changes
- runtime status schema changes
- Match Journal or overlay behavior changes
- AI/model-provider calls or generated advice
- CI, merge-policy, or deploy-policy gates

## Required View Guarantees

### General View Rules

Every derived SQL view must be:

- deterministic for a fixed SQLite database state
- read-only
- side-effect free
- free of non-deterministic SQLite functions such as current time
- free of triggers, writes, materialized summary tables, temp-table
  requirements, external files, Python callbacks, network calls, or model calls
- named with lowercase `v_` snake_case
- documented by focused tests when its behavior affects analytics meaning

Views must preserve row identity and provenance enough for local review. A view
that projects parser fact rows should include the relevant row id plus the
available core review columns from its base table when applicable:

- `value_source`
- `confidence`
- `finality`
- `drift_status`
- `availability_status`
- `parser_schema_version`
- `ingest_run_id`
- `source_parser_surface`
- `source_fact_key`

Summary views may aggregate these labels, but they must not erase degraded,
unknown, unavailable, human-entered, or inferred values as though they were
clean observed parser facts.

### Opening Hand Views

`v_opening_hand_cards` must remain a row-level review surface for opening-hand
card rows.

Required behavior:

- One row per stored `opening_hand_cards` row.
- Preserve `match_id`, `game_id`, `game_number`, `opening_hand_id`, card row
  id or position, `grp_id`, `card_name`, identity hint/status fields, and
  opening hand size/count fields where available.
- Preserve provenance and availability labels from the opening-hand card row,
  and include opening-hand parent context when useful.
- Do not infer missing cards, hand contents, deck contents, mulligan decisions,
  card quality, or keep/mulligan advice.

### Opening Line / Gameplay Action Views

`v_opening_lines` must remain a deterministic first-three-turn action view.

Required behavior:

- Include only gameplay actions where `turn_number` is known and less than or
  equal to `3`.
- Preserve row identity, match/game identity, turn number, action type, actor
  relation, zone movement fields, card identity hints, source/confidence/finality
  labels, degradation status, and availability status where available.
- Do not reinterpret action arrays, GameState diffs, annotations, hidden cards,
  card names, action quality, or gameplay strategy.

If added, `v_gameplay_action_review` must be a broader row-level review surface
over all `gameplay_actions` rows, with optional child-card counts or joined
card identifiers. It must not replace or widen `v_opening_lines`.

### Mulligan Views

`v_mulligan_outcomes` must remain a game/mulligan review surface.

Required behavior:

- Preserve `mulligan_event_id`, match/game identity, `game_number`,
  `mulligan_count`, decision/detail fields when available, and related game
  result/play-draw context.
- Preserve provenance, finality, drift, and availability labels from
  `mulligan_events`.
- Distinguish `0` mulligans from unknown or unavailable mulligan detail.
- Do not infer unobserved mulligans, hidden hand contents, keep quality, player
  mistakes, or gameplay advice.

### Game 1 vs Postboard Views

`v_game1_vs_postboard` must remain a game-level review surface for comparing
preboard and postboard game rows.

Required behavior:

- Preserve match/game identity, game number, pre/postboard label, local result,
  play/draw, turn count, duration when available, and the base game-result
  provenance labels.
- Treat pre/postboard labels as parser/local analytics fields, not proof of
  deck-state contents or sideboard plan correctness.
- Do not infer deck-state contents, sideboard deltas, matchup plans, archetype
  labels, or coaching claims.

### Play/Draw Split Views

`v_play_draw_splits` must be a summary view over game results.

Required behavior:

- Group missing or blank play/draw as `unknown`, without rewriting base rows.
- Count total games in each play/draw group.
- Count known wins and known losses separately.
- Count unknown, unavailable, degraded, or non-win/loss results separately.
- Compute win rate only over known win/loss outcomes.
- Return `NULL` for win rate when there are no known win/loss outcomes.
- Include enough degraded/review counts to prevent unknown or degraded rows
  from being silently treated as losses.

`v_play_draw_splits` must not claim statistical significance, matchup truth,
pilot skill, or matchup advice.

### Sample-Size Warning Views

`v_sample_size_warnings` must be deterministic review guidance, not statistical
truth.

Required behavior:

- Use only counts from deterministic analytics views/tables.
- Produce stable labels.
- At minimum support:
  - `empty_sample` for `game_count = 0`, if such rows can appear
  - `small_sample` for `1 <= game_count < 10`
  - `ok` for `game_count >= 10`
- If Codex C adds an intermediate label, it must be explicitly tested and
  documented in the implementation handoff.
- Do not become merge readiness, deploy readiness, AI readiness, or gameplay
  advice.

### Matchup Label Performance Views

`v_matchup_label_performance` must remain a human-label analytics view.

Required behavior:

- Use only current human matchup labels when `is_current = 1`.
- Preserve that matchup labels are human annotations, not parser truth and not
  archetype classification.
- Count known match wins/losses separately when possible.
- Do not treat unknown match results as losses.
- Do not generate, infer, normalize, or classify archetypes.

### Opponent Observation Review Views

If added, `v_opponent_card_observation_review` must expose row-level review
context for `opponent_card_observations` and related child card rows.

Required behavior:

- Preserve observation identity, linked action identity when present, match/game
  identity, turn number, actor relation, observation/evidence status,
  confidence, degradation flags, review-required status, card identifiers, and
  availability labels where available.
- Do not infer hidden cards, decklists, opponent archetypes, matchup plans,
  gameplay advice, or card-performance claims.

## Null, Unknown, And Degraded Behavior

Views must keep these meanings distinct:

- `NULL`: not applicable, not stored, or unavailable in the base table.
- `unknown`: a stable label for an unknown category when grouping would
  otherwise collapse null/blank values.
- `expected_unavailable`: source evidence is not expected to exist for this
  field.
- `not_observed`: the parser did not observe the fact.
- `not_yet_supported`: the local analytics layer is not ready to represent the
  fact.
- `degraded` or drift labels: evidence exists but should be reviewed.

Views must not collapse missing/degraded/unknown values into clean losses,
clean wins, observed facts, or confident labels. Summary views must expose
counts or labels that allow a reviewer to see when unknown/degraded rows
affected the denominator.

## Evidence Ledger Relationship

Views may use `fact_provenance` to expose review-oriented counts, labels, or
joinable row context.

Allowed:

- `provenance_count`
- `review_required_count`
- `failed_invariant_count`
- `degraded_provenance_count`
- deterministic joins on `fact_table`, `fact_id`, and `fact_field`

Forbidden:

- treating a provenance row as a parser fact override
- deriving new match/game/card facts from provenance metadata
- exposing raw/private source payloads in broad summary views
- requiring raw Player.log excerpts to understand a view row

If Codex C exposes source payload path labels in a row-level review view, tests
must prove they are safe labels from existing local schema fields, not raw log
content or local private file paths.

## Migration And Versioning Policy

The current analytics branch is still the foundation branch for the v1 schema.
Codex C may update `0001_initial_analytics_schema.sql` view definitions in
place for this issue.

Codex C must not:

- add a new migration unless it first verifies that `0001` is already immutable
  for the active branch
- change the default database path
- add an environment variable contract
- create runtime database bootstrap behavior
- add materialized summary tables
- bump schema version solely because view definitions were corrected on the
  unmerged foundation branch

Any future migration-after-adoption policy belongs in a separate contract.

## Privacy And Local Artifact Rules

Derived views are local-only and must not require committing generated data.

Required privacy behavior:

- Tests must use in-memory SQLite databases or test-managed temporary files.
- Tests must not write or commit `data/analytics/`.
- Views must not store raw Player.log excerpts, raw local logs, raw decklists,
  runtime status files, failed posts, workbook exports, API keys, tokens,
  credentials, webhook URLs, or model-provider output.
- Views may reference deterministic ids, parser-normalized labels, and safe
  provenance labels already stored in the analytics schema.

## Compatibility Expectations

- Existing seven view names must remain available unless a future contract
  explicitly authorizes removal or rename.
- Existing table names, primary keys, and core provenance columns must remain
  compatible with current analytics ingest tests.
- View changes must not require parser row-shape changes.
- View changes must not require gameplay-action, opponent-observation, or
  field-evidence ingest behavior changes unless those tests reveal an existing
  bug and Codex C routes back for scope confirmation.
- Adding columns to views is allowed when it improves reviewability; removing
  or renaming existing view columns requires focused compatibility notes in the
  implementation handoff.
- Human annotation views must remain clearly annotation-owned and must not
  become parser-owned matchup or archetype truth.

## Error Behavior

Malformed SQL:

- Migration application must fail through the existing migration loader.
- Tests must catch malformed or missing view definitions through migration
  application and exact query assertions.

Missing source data:

- Views should return no rows or explicit `unknown`/review counts as
  appropriate.
- Views must not synthesize match/game rows that do not exist in source tables.

Conflicting or degraded evidence:

- Views must expose review labels or counts and must not resolve the conflict.

Contract ambiguity:

- Route back to Codex B before adding tables, triggers, generated artifacts,
  runtime behavior, workbook/webhook/App Script behavior, Match Journal
  behavior, overlay behavior, AI behavior, or gameplay advice.

## Side Effects

Allowed side effects for Codex C:

- update source-controlled SQL view definitions
- add focused derived-view tests
- update required-view existence tests if approved view names are added
- create in-memory SQLite databases during tests
- produce an implementation handoff

Forbidden side effects:

- creating or committing generated SQLite/local/private artifacts
- modifying parser behavior or parser state final reconciliation
- modifying parser event classes
- modifying runtime status schemas
- modifying workbook schema, webhook payloads, Apps Script behavior, or output
  transport
- modifying Match Journal, overlay, Google Sheets sync, CI gates, merge policy,
  or deploy policy
- calling OpenAI or any model provider

## Dependency Order

Recommended Codex C implementation order:

1. Confirm branch is `codex/analytics-foundation` and clean or only contains
   intentional local work.
2. Compare current view SQL against this contract.
3. Add `tests/test_analytics_derived_views.py` with representative in-memory
   SQLite setup and exact assertions for current and approved views.
4. Update existing view definitions in `0001_initial_analytics_schema.sql` only
   where tests prove current SQL does not meet the contract.
5. Update `tests/test_analytics_schema.py` required-view list only for approved
   new views.
6. Run focused analytics validation.
7. Write
   `docs/implementation_handoffs/analytics_derived_sql_views_comparison.md`.

## Tests Required

Codex C must add or update focused tests proving:

- all approved views exist after applying migrations
- `v_opening_hand_cards` returns one row per opening-hand card and preserves
  card identity/provenance labels
- `v_opening_lines` includes only turn `<= 3` known-turn gameplay actions
- `v_gameplay_action_review`, if added, includes all relevant action rows
  without widening `v_opening_lines`
- `v_mulligan_outcomes` distinguishes `0` from unknown/unavailable mulligans
- `v_game1_vs_postboard` preserves pre/postboard labels without inventing deck
  state
- `v_play_draw_splits` computes win rate only over known win/loss rows and
  exposes unknown/degraded counts
- `v_sample_size_warnings` produces deterministic labels at threshold edges
- `v_matchup_label_performance` uses current human labels and does not treat
  unknown match results as losses
- `v_opponent_card_observation_review`, if added, preserves observation review
  and degradation context
- views do not require raw Player.log payloads, runtime status files, workbook
  exports, generated DB files, network calls, or model calls

Required validation:

```bash
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m pytest -q tests/test_analytics_derived_views.py
python3 -m ruff check src tests tools
git diff --check
```

Recommended protected-surface checks, if the tools exist on the branch:

```bash
git diff --name-only origin/codex/analytics-foundation...HEAD | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only origin/codex/analytics-foundation...HEAD | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If those tools are absent, Codex C must say so and run the best available
fallback secret/protected-surface scan.

## Acceptance Criteria

- `docs/contracts/analytics_derived_sql_views.md` exists.
- Derived SQL views are explicitly approved as read-only local analytics query
  surfaces.
- Existing seven view names remain available.
- Any added view names are limited to the approved gameplay-action and
  opponent-observation review views.
- Focused tests prove behavior, not only view existence.
- Unknown/degraded/unavailable values are not silently counted as clean wins,
  losses, observations, or confident labels.
- Human matchup labels remain human annotations, not parser or archetype truth.
- SQL view changes stay within the analytics schema migration and tests.
- No generated SQLite artifacts, private logs, raw Player.log excerpts,
  workbook exports, credentials, webhook URLs, or model output are committed.
- No parser/runtime/workbook/webhook/App Script/Match Journal/overlay/AI/CI
  behavior changes are introduced.
- Codex C produces
  `docs/implementation_handoffs/analytics_derived_sql_views_comparison.md`.

## Unknowns

- Whether future analytics consumers will prefer row-level review views,
  aggregate summary views, or both.
- Whether view definitions should later move into a separate migration once
  `0001_initial_analytics_schema.sql` is merged into a stable base.
- Whether richer sample-size labels beyond `small_sample` and `ok` are worth
  standardizing now.
- Whether future Match Journal or overlay surfaces will read these views
  directly or through a separate report adapter.
- Whether future analytics should materialize expensive summaries. This
  contract does not approve materialization.

## Suspected Gaps

- Current view tests are existence-oriented and do not prove analytics
  semantics.
- Current play/draw win-rate math likely treats unknown or non-win/loss results
  as losses.
- Current views do not consistently expose finality, drift, availability, and
  parser source labels.
- Current schema has no dedicated opponent-observation review view.
- Current schema has no all-actions review view separate from opening lines.
- Current sample-size warning semantics are too lightly specified for durable
  downstream use.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #191, analytics derived SQL views, under tracker #190.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/190
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/191
- Branch: codex/analytics-foundation
- Source contract: docs/contracts/analytics_derived_sql_views.md
- Expected implementation handoff: docs/implementation_handoffs/analytics_derived_sql_views_comparison.md
- Risk tier: Medium-High

Goal:
Compare the current analytics SQLite view definitions and focused tests against the derived SQL views contract. Implement only the smallest coherent SQL view and test changes needed to satisfy the contract.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/analytics_derived_sql_views.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/analytics_migration_loader.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/contracts/analytics_gameplay_action_ingest.md
- docs/contracts/analytics_opponent_card_observation_ingest.md
- docs/contracts/analytics_field_evidence_ingest.md
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/analytics_ingest.py
- tests/test_analytics_schema.py
- tests/test_analytics_migration_loader.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_analytics_opponent_card_observation_ingest.py
- tests/test_analytics_field_evidence_ingest.py

Do:
- Confirm branch state and compare current view SQL against the contract before editing.
- Add focused derived-view tests, preferably in tests/test_analytics_derived_views.py.
- Keep existing seven view names available.
- Add only approved review views if needed: v_gameplay_action_review and v_opponent_card_observation_review.
- Update 0001_initial_analytics_schema.sql view definitions in place only because this is still the active unmerged analytics foundation branch.
- Preserve read-only deterministic SQL behavior and local-only privacy boundaries.
- Produce docs/implementation_handoffs/analytics_derived_sql_views_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Implement code outside the narrow SQL view/test slice unless a failing focused test proves a local analytics bug and the contract authorizes the fix.
- Target main directly.
- Store raw Player.log payloads or commit SQLite/local/generated/private artifacts.
- Change parser behavior, parser state final reconciliation, parser event classes, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, AI/OpenAI behavior, Match Journal behavior, overlay behavior, Google Sheets behavior, CI gates, merge policy, or deploy policy.
- Let analytics views become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching.

Validation:
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
- python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
- python3 -m pytest -q tests/test_analytics_derived_views.py
- python3 -m ruff check src tests tools
- git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/191"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/analytics_derived_sql_views.md"
  target_artifact: "docs/implementation_handoffs/analytics_derived_sql_views_comparison.md"
  verdict: "contract_complete_implementation_ready"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "Documentation-only contract writer pass; no code tests run."
    - "Inspected issue #191 and tracker #190 with gh."
    - "Inspected analytics contracts, migration SQL, migration loader, ingest modules, and focused analytics tests."
  stop_conditions:
    - "Do not target main directly."
    - "Do not store raw Player.log payloads or commit SQLite/local/generated/private artifacts."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, AI/OpenAI behavior, Match Journal behavior, overlay behavior, Google Sheets behavior, CI gates, merge policy, or deploy policy."
    - "Do not let analytics views become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching."
```
