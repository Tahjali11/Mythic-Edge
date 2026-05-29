# Analytics Replay/View Validation Harness Contract

## Module

Local Analytics Foundation replay-to-view validation harness.

This contract defines a narrow validation harness that proves a
parser-normalized replay bundle can be ingested into local in-memory SQLite and
then queried through deterministic derived SQL views without duplicate facts,
hidden inference, raw Player.log storage, generated database artifacts, or loss
of provenance/degradation labels.

It does not define live ingest, a CLI, a generated database, a dashboard, Match
Journal behavior, overlay behavior, Google Sheets sync, workbook/webhook/App
Script behavior, AI/OpenAI behavior, gameplay advice, or parser truth.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/193>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/190>

Required repo authorities:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Branch

`codex/analytics-foundation`

Inspected local and remote head:

```text
81f058a26229f4535e25c44126d1bea43a40a115
```

## Risk Tier

Medium.

Reason: this is validation/review infrastructure over the local analytics
layer, not production behavior. The risk is still meaningful because the
harness can shape what future analytics consumers trust. It must stay
evidence-only and must not become parser truth, analytics truth, merge
readiness, deploy readiness, AI truth, coaching truth, or gameplay advice.

## Owning Layer

Primary owner: local analytics validation / review evidence.

Truth boundaries:

- Parser/state owns parser-managed match facts, game facts, event
  interpretation, identity, deduplication, and final reconciliation.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  degradation, invariant, and review vocabulary.
- Analytics ingest owns copying parser-normalized facts into local SQLite
  tables with deterministic IDs.
- Derived SQL views own deterministic query projections over already-stored
  local facts.
- The replay/view validation harness owns test evidence that analytics ingest
  and derived views compose correctly for a representative sanitized/synthetic
  replay bundle.

The harness must not become a parser, a second evidence ledger, a raw-log
reader, a generated database writer, a dashboard, a runtime status source, a
Match Journal/overlay/Google Sheets integration, merge/deploy authority,
analytics truth, AI truth, or coaching truth.

Plain English: the harness may prove "the current analytics path returns these
rows for this replay." It may not decide what happened in a match or recommend
how to play.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_replay_view_validation_harness.md`

Future implementation files authorized for Codex C:

- `tests/test_analytics_replay_view_harness.py`
- optional test-local helper functions inside
  `tests/test_analytics_replay_view_harness.py`
- `docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md`

Reference-only source surfaces:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `tests/test_analytics_derived_views.py`

Not owned by this contract:

- parser modules
- parser state final reconciliation
- parser event classes
- match/game identity or deduplication
- workbook schema, webhook payload shape, Apps Script behavior, or output
  transport
- runtime status schema or runtime artifacts
- saved-event replay behavior
- golden replay behavior
- generated SQLite database files
- Match Journal, overlay, Google Sheets sync, CI gates, merge policy, deploy
  policy, OpenAI/model-provider behavior, AI coaching, or gameplay advice

## Public Interface

No new production public interface is authorized.

The harness must use the existing public analytics ingest interface:

```python
ingest_parser_normalized_replay(
    connection: sqlite3.Connection,
    replay: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult
```

Allowed test interface:

- a focused pytest module named `tests/test_analytics_replay_view_harness.py`
- test-local helpers such as `_connect()`, `_representative_replay()`,
  `_view_rows()`, or `_count()` if they keep the replay shape inspectable

Forbidden interface expansion:

- no production module
- no CLI
- no default database opener
- no environment-variable contract
- no live parser runtime ingest
- no saved-event replay runner change
- no golden replay runner change
- no raw Player.log reader
- no Google Sheets sync
- no webhook sender
- no Apps Script interaction
- no Match Journal, overlay, AI coaching, OpenAI runtime, or model-provider
  interface

## Observed Current Behavior

- Issue #191 is closed and PR #192 is merged into
  `codex/analytics-foundation` at
  `81f058a26229f4535e25c44126d1bea43a40a115`.
- Issue #193 and tracker #190 are open.
- `docs/contracts/analytics_replay_view_validation_harness.md` did not exist
  before this contract.
- `ingest_parser_normalized_replay(...)` already applies analytics migrations,
  ingests match/game rows, opening hand rows, mulligan rows, gameplay actions,
  opponent-card observations, and field-evidence entries, then returns
  `AnalyticsReplayIngestResult`.
- `tests/test_analytics_parser_normalized_replay_ingest.py` proves core replay
  ingest, in-memory migration, idempotency, safe provenance labels, optional
  empty decision fields, and generated SQLite artifact safety.
- `tests/test_analytics_gameplay_action_ingest.py` proves gameplay-action and
  gameplay-action-card ingest behavior.
- `tests/test_analytics_opponent_card_observation_ingest.py` proves opponent
  observation ingest, action linking, degradation/review labels, and child card
  storage.
- `tests/test_analytics_field_evidence_ingest.py` proves canonical
  field-evidence ingest into `fact_provenance`.
- `tests/test_analytics_derived_views.py` proves view semantics over focused
  rows inserted directly into SQLite tables.
- No single focused test currently proves the combined path:

```text
parser-normalized replay input
  -> analytics ingest
  -> SQLite fact tables
  -> derived SQL views
```

## Required Decision

Implementation should proceed as a test-only validation harness unless Codex C
finds a concrete contradiction between current analytics behavior and an
existing analytics contract.

Preferred implementation shape:

- add `tests/test_analytics_replay_view_harness.py`
- keep helper functions local to that test module
- use inline sanitized/synthetic replay data rather than a new committed
  fixture
- use `sqlite3.connect(":memory:")`
- call `ingest_parser_normalized_replay(...)`
- query derived views directly
- repeat the same ingest and prove table counts and view rows remain stable
- write the implementation handoff

Codex C must not add production code just to create the harness. If the harness
exposes a real mismatch in existing analytics ingest or view behavior, Codex C
may document the mismatch in the handoff and either:

- make the smallest local analytics fix only if it is already authorized by the
  existing analytics contracts and does not touch protected surfaces, or
- route back to Codex B/D if the fix would change scope, schema ownership,
  runtime behavior, or protected surfaces.

## Inputs

### Harness Replay Bundle

Input type: parser-normalized replay mapping accepted by
`ingest_parser_normalized_replay(...)`.

Required top-level fields:

- `source_kind`
- `source_artifact_label`
- `parser_commit`
- `parser_version`
- `generated_at`
- `match_log_rows`
- `game_log_rows`
- `gameplay_action_entries`
- `opponent_card_observations`
- `field_evidence_entries`

Required `source_kind`:

```text
sanitized_golden_replay
```

Required source label style:

```text
analytics_replay_view_harness_v1
```

The label must be a safe label, not a local path or URL.

### Minimum Replay Contents

The representative replay must include enough data to exercise the combined
path without becoming broad or brittle.

Required match/game rows:

- one match with a stable synthetic match id
- at least two games in the same match so preboard/postboard and play/draw
  differences can be observed
- at least one preboard game and one postboard game
- at least one `Play` game and one `Draw` game
- at least one known win and one known loss if feasible with current row shape
- opening hand size and opening hand card names for at least one game
- mulligan count `1` or greater for one game
- mulligan count `0` for another game, or an explicit assertion that the
  current ingest surface stores only observed mulligan rows for the chosen
  replay shape
- turn count and duration values where the existing row shape supports them
- queue, format, event id, sync status, and timestamps as safe synthetic labels

Required gameplay-action entries:

- at least one action with `turn_number <= 3` so it appears in
  `v_opening_lines`
- at least one action with `turn_number > 3` or unknown turn so the harness can
  prove `v_gameplay_action_review` is broader than `v_opening_lines`
- at least one action with card identity fields sufficient to create a
  `gameplay_action_cards` row
- actor relation and zone fields sourced from parser-normalized labels only

Required opponent-card observations:

- at least one observation linked to an ingested gameplay action when current
  deterministic matching allows it
- `object = "mythic_edge_opponent_card_observation"`
- `schema_version = "parser_opponent_card_observations.v1"`
- `actor_relation = "opponent"`
- card identity fields sufficient to create an
  `opponent_card_observation_cards` row
- at least one degradation or review signal, such as
  `evidence_status = "degraded"`, `confidence = "low"`,
  `degradation_flags = ["ambiguous_zone_transition"]`, or
  `review_required = true`

Required field-evidence entries:

- at least one canonical field-evidence entry targeting a deterministic fact
  row whose id is stable from the replay shape, such as `matches.match_id` or
  `game_results.local_result`
- at least one review/degradation label in field evidence, such as
  `drift_flags = ["conflicting_evidence"]`,
  `invariant_status = "failed"`, `degraded_reason`, or
  `review_required = true`, if accepted by existing field-evidence validation
- safe `source_payload_paths` labels only

### Human Annotation Inputs

Human annotation rows are not required for the initial replay harness because
they are not part of parser-normalized replay input.

`v_matchup_label_performance` is already covered by derived-view tests. Codex C
may add a second small harness assertion that inserts a synthetic current
`matchup_labels` row after replay ingest and queries
`v_matchup_label_performance`, but this is optional and must remain clearly
human-annotation-owned.

### Forbidden Inputs

- raw Player.log payloads
- local raw logs or local log paths
- saved private Player.log excerpts
- generated SQLite database files
- runtime status files
- failed-post artifacts
- workbook exports
- webhook payloads
- Apps Script state
- Google Sheets live data
- Match Journal or overlay runtime state
- OpenAI/model-provider output
- hidden-card inference, decklist completion, archetype classification, player
  mistake labels, gameplay advice, or coaching text

## Outputs

Allowed outputs:

- pytest assertions from `tests/test_analytics_replay_view_harness.py`
- in-memory SQLite rows during test execution
- implementation handoff documentation

Forbidden outputs:

- generated SQLite database files
- SQLite WAL, SHM, journal, temporary, or private database artifacts
- committed raw Player.log excerpts or private local logs
- committed runtime artifacts, failed posts, generated data, workbook exports,
  credentials, tokens, API keys, secrets, or webhook URLs
- workbook schema changes
- webhook payload changes
- Apps Script changes
- runtime status changes
- Match Journal, overlay, Google Sheets, AI/OpenAI, CI, merge-policy, or
  deploy-policy behavior changes
- coaching, strategy, archetype, hidden-card, decklist, or player-mistake
  outputs

## Required Harness Guarantees

### In-Memory Execution

The harness must use in-memory SQLite by default:

```python
sqlite3.connect(":memory:")
```

It must not create, write, or depend on `data/analytics/mythic_edge.sqlite3` or
any committed/generated SQLite artifact.

### Composition Path

The harness must call the actual ingest API and then query views:

```text
ingest_parser_normalized_replay(...)
SELECT ... FROM v_opening_hand_cards
SELECT ... FROM v_opening_lines
SELECT ... FROM v_gameplay_action_review
SELECT ... FROM v_mulligan_outcomes
SELECT ... FROM v_game1_vs_postboard
SELECT ... FROM v_play_draw_splits
SELECT ... FROM v_sample_size_warnings
SELECT ... FROM v_opponent_card_observation_review
```

It must not insert parser fact rows directly into source tables for the primary
composition test. Direct inserts remain appropriate in
`tests/test_analytics_derived_views.py`, not in this harness.

### Idempotency

The harness must ingest the same replay twice into the same in-memory database
and prove:

- `ingest_run_id` is the same for both runs
- `row_counts` are stable after the second run
- fact table counts are stable after the second run
- selected view row counts are stable after the second run
- selected view row identity values are stable after the second run
- field-evidence rows are not duplicated after the second run

Required table count coverage:

- `ingest_runs`
- `matches`
- `games`
- `match_results`
- `game_results`
- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `gameplay_actions`
- `gameplay_action_cards`
- `opponent_card_observations`
- `opponent_card_observation_cards`
- `fact_provenance`

### Opening Hand And Mulligan Views

The harness must prove replay-ingested rows appear through:

- `v_opening_hand_cards`
- `v_mulligan_outcomes`

Required assertions:

- opening hand card rows preserve match/game identity, `opening_hand_id`,
  `opening_hand_card_id`, card position, card name, hand size, source surface,
  finality, drift status, ingest run id, and availability status
- mulligan rows distinguish observed mulligan count from unknown/unavailable
  values
- `0` mulligans must not be coerced into unknown, and unknown/unavailable must
  not be coerced into `0`

### Gameplay Action Views

The harness must prove replay-ingested gameplay actions appear through:

- `v_opening_lines`
- `v_gameplay_action_review`

Required assertions:

- first-three-turn action appears in both views
- later-turn or unknown-turn action appears in `v_gameplay_action_review` but
  not `v_opening_lines`
- card identity child-row count or `grp_ids` appears where current view shape
  supports it
- action source/provenance labels remain visible
- the harness does not reinterpret action type, zones, annotations, card
  identity, or visibility

### Opponent Observation View

The harness must prove replay-ingested opponent observations appear through:

- `v_opponent_card_observation_review`

Required assertions:

- observation identity and match/game identity are stable
- linked gameplay action id is present when current deterministic linking
  supports it
- child-card identity context is visible
- `actor_relation = "opponent"` remains unchanged
- degradation flags, evidence status, confidence, drift status, and
  review-required status remain visible where current storage/view shape
  supports them
- hidden-card, decklist, archetype, matchup-plan, strategy, coaching, and
  player-mistake inference remain absent

### Game Result And Play/Draw Views

The harness must prove replay-ingested game rows appear through:

- `v_game1_vs_postboard`
- `v_play_draw_splits`
- `v_sample_size_warnings`

Required assertions:

- preboard and postboard labels remain visible
- play/draw grouping works over ingested game-result rows
- known wins and losses are counted separately
- unknown/degraded/unavailable rows, if included in the replay, are visible as
  review counts and not treated as clean losses
- win rate is calculated only over known win/loss rows
- sample-size warning labels are deterministic and review-oriented only

### Field Evidence And Provenance

The harness must prove field-evidence entries survive the replay ingest path.

Required assertions:

- target fact rows exist before field-evidence rows are attached
- canonical field-evidence rows appear in `fact_provenance`
- `ledger_entry_id`, `fact_table`, `fact_id`, `fact_field`,
  `source_parser_surface`, `source_fact_key`, `value_source`, `confidence`,
  `finality`, `drift_flags`, `invariant_status`, `degraded_reason`, and
  `review_required` are preserved
- field-evidence rows are not duplicated after repeated ingest
- source payload paths remain safe labels, not raw log content or local paths

### Privacy And Artifact Safety

The harness must prove or document that it does not create local/generated
SQLite artifacts.

At minimum:

- tests use in-memory SQLite
- no new fixture file contains raw Player.log excerpts
- no file under `data/analytics/` is created or committed
- path-scoped secret/private marker and protected-surface checks are run for
  touched files if tools exist

## Error Behavior

Malformed replay input:

- Existing ingest tests already cover malformed input. The harness does not
  need to duplicate all malformed-input coverage.
- If Codex C adds a negative harness test, it must remain focused on
  replay-to-view composition and prove no partial facts are left behind.

Missing optional analytics rows:

- If a view returns no rows because the representative replay intentionally
  omitted a source family, the omission must be explicit in the test name or
  handoff. The preferred harness includes all required families.

Failed harness assertion:

- Treat as validation evidence, not proof that the parser is wrong.
- If failure indicates a local analytics ingest/view mismatch, document the
  failing path and route according to the Required Decision section.

Contract ambiguity:

- Route back to Codex B before adding production helpers, new migrations,
  generated database files, runtime behavior, saved/golden replay behavior,
  workbook/webhook/App Script behavior, Match Journal/overlay behavior,
  Google Sheets sync, OpenAI/model-provider behavior, AI coaching, or gameplay
  advice.

## Side Effects

Allowed side effects:

- add focused pytest file
- create in-memory SQLite databases during tests
- add test-local helpers
- produce implementation handoff

Forbidden side effects:

- add production code unless an already-contracted local analytics bug is
  discovered and explicitly justified
- create or commit generated SQLite databases or SQLite sidecar files
- create or commit raw/private/local artifacts
- change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, workbook schema, webhook payload
  shape, Apps Script behavior, output transport, runtime status schema, saved
  replay behavior, golden replay behavior, Match Journal behavior, overlay
  behavior, Google Sheets behavior, AI/OpenAI behavior, CI gates, merge policy,
  or deploy policy

## Dependency Order

Recommended Codex C implementation order:

1. Confirm branch is `codex/analytics-foundation` and starts clean.
2. Inspect issue #193, this contract, and #191 derived-view implementation
   artifacts.
3. Build the representative synthetic replay in
   `tests/test_analytics_replay_view_harness.py`.
4. Add the primary composition/idempotency test.
5. Add optional narrow helper assertions only if they keep the replay shape
   readable.
6. Run the focused harness test.
7. Run adjacent analytics ingest/view/schema tests.
8. Run ruff, whitespace, secret/private marker, and protected-surface checks.
9. Write
   `docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md`.

## Compatibility

- Existing analytics ingest public API remains unchanged.
- Existing analytics schema/view names remain unchanged.
- Existing analytics derived-view tests remain authoritative for direct view
  semantics.
- Existing ingest tests remain authoritative for per-family ingest behavior.
- Existing parser row shapes remain unchanged.
- Existing workbook/webhook/App Script/runtime/Match Journal/overlay/Google
  Sheets/OpenAI behavior remains unchanged.
- This harness must be additive and must not require generated artifacts.

## Tests Required

Required focused validation:

```bash
python3 -m pytest -q tests/test_analytics_replay_view_harness.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py
python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m ruff check src tests tools
git diff --check
```

Required safety checks if tools exist:

```bash
git diff --name-only origin/codex/analytics-foundation...HEAD | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only origin/codex/analytics-foundation...HEAD | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Recommended artifact scan:

```bash
find data -type f \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*-wal' -o -name '*-shm' -o -name '*-journal' \) -print
```

If `data/` does not exist, record that as expected. If the check tools are
absent, Codex C must say so and run the best available fallback scan.

## Acceptance Criteria

- `docs/contracts/analytics_replay_view_validation_harness.md` exists.
- Codex C adds a focused replay/view harness test module.
- The harness uses in-memory SQLite and `ingest_parser_normalized_replay(...)`.
- The harness uses sanitized/synthetic parser-normalized replay data only.
- The harness proves repeated ingest of the same replay does not duplicate
  facts or view rows.
- The harness queries the required derived views and proves representative
  rows preserve identity, provenance, availability, degradation, and review
  labels.
- The harness proves field-evidence rows survive ingest and remain safe
  labels.
- The harness does not create or commit generated SQLite/private/runtime
  artifacts.
- No parser/runtime/workbook/webhook/App Script/Match Journal/overlay/Google
  Sheets/AI/OpenAI behavior changes are introduced.
- Codex C produces
  `docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md`.

## Unknowns

- Whether the first replay bundle should be one match with two games or a small
  set of separate replay inputs. The preferred first pass is one compact
  two-game match.
- Whether a human matchup label should be added to the harness. It is optional
  because human labels are not parser-normalized replay input.
- Whether deterministic gameplay-action IDs should ever become a public helper.
  The harness should avoid depending on private ID helpers when querying by
  stable replay-visible fields is enough.
- Whether future historical replay artifacts should use committed sanitized
  JSON fixtures. This contract prefers inline synthetic data for the first
  harness.

## Suspected Gaps

- The combined replay-to-view path is not currently covered by one focused
  test.
- Existing tests may not prove that field-evidence review labels remain stable
  when the same replay also includes gameplay actions and opponent
  observations.
- Existing view tests use direct table inserts, which is right for view
  semantics but does not prove the ingest path populates the views as expected.
- Future consumers may overread harness success as broader analytics readiness;
  the harness must state exactly what it proves.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #193, analytics replay-to-view validation harness, under tracker #190.

Repo/worktree:
Use the existing local Mythic Edge analytics foundation worktree.

Branch:
codex/analytics-foundation

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/190
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/193
- Previous completed issue: #191
- Previous PR: #192
- Previous merge commit: 81f058a26229f4535e25c44126d1bea43a40a115
- Source contract: docs/contracts/analytics_replay_view_validation_harness.md
- Expected implementation handoff: docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md
- Risk tier: Medium

Goal:
Implement the smallest test-only replay-to-view validation harness that proves parser-normalized replay input can be ingested into in-memory SQLite and queried through deterministic derived SQL views without duplicate facts, hidden inference, raw Player.log storage, generated database artifacts, or loss of provenance/degradation labels.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/analytics_replay_view_validation_harness.md
- docs/contracts/analytics_derived_sql_views.md
- docs/implementation_handoffs/analytics_derived_sql_views_comparison.md
- docs/contract_test_reports/analytics_derived_sql_views.md
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_analytics_opponent_card_observation_ingest.py
- tests/test_analytics_field_evidence_ingest.py
- tests/test_analytics_derived_views.py

Do:
- Confirm branch state and compare current tests/code against the contract before editing.
- Add tests/test_analytics_replay_view_harness.py.
- Use inline sanitized/synthetic parser-normalized replay data and sqlite3.connect(":memory:").
- Call ingest_parser_normalized_replay(...) and then query derived SQL views.
- Prove replay idempotency by ingesting the same replay twice and checking stable row counts and view rows.
- Cover opening hand, mulligan, play/draw, game1/postboard, gameplay-action, opponent-observation, sample-size, and field-evidence/provenance expectations.
- Keep helpers test-local unless there is a clear contract-level reason to share them.
- Produce docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Add production code unless a concrete already-contracted local analytics bug is exposed and the handoff explicitly justifies the minimal fix.
- Open a PR or commit unless separately asked.
- Target main directly.
- Close tracker #190.
- Create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
- Store raw Player.log payloads in SQLite.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, Google Sheets sync, Match Journal behavior, overlay behavior, or OpenAI runtime behavior.
- Let analytics views or analytics harnesses become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching.

Validation:
- python3 -m pytest -q tests/test_analytics_replay_view_harness.py
- python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py
- python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
- python3 -m ruff check src tests tools
- git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/193"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/analytics_replay_view_validation_harness.md"
  target_artifact: "docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md"
  verdict: "contract_complete_implementation_ready"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "Documentation-only contract writer pass; no code tests run."
    - "Verified local branch codex/analytics-foundation matches origin at 81f058a26229f4535e25c44126d1bea43a40a115."
    - "Inspected issue #193 and tracker #190 with gh."
    - "Inspected existing analytics contracts, #191 implementation handoff/report, analytics ingest code, migration SQL, and focused analytics tests."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #190."
    - "Do not create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not change parser/runtime/workbook/webhook/App Script/AI/OpenAI/Match Journal/overlay/Google Sheets behavior."
    - "Do not let analytics views or analytics harnesses become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching."
```
