# Analytics Field Evidence Ingest Contract

## Module

Analytics field-evidence ingest for parser-normalized replay input.

This contract covers the first implementation slice that turns
`replay["field_evidence_entries"]` into local SQLite `fact_provenance` rows.
It does not define a new parser, a new evidence ledger schema, a new analytics
schema migration, or a runtime evidence generator.

## Source Artifact

- Codex A handoff for `docs/contracts/analytics_field_evidence_ingest.md`
- Parent analytics contracts on `codex/analytics-foundation`

## Tracker

N/A in the supplied handoff.

## Branch

`codex/analytics-foundation`

Current inspected commit:

```text
8cdfcaeae5e561d73056eeeda6ca0e3597564701
```

## Owning Layer

Parser/state modules and the Player.log evidence ledger own interpreted facts
and field-evidence labels.

The analytics ingest layer owns only local SQLite storage of those
parser-normalized facts and provenance records. It must not reinterpret raw
Player.log evidence, change parser truth, infer facts, or promote analytics
rows into parser truth.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- focused updates to existing analytics ingest tests when deferred
  `field_evidence_entries` assertions become stale

Reference-only source surfaces:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`

## Public Interface

The public interface remains:

```python
ingest_parser_normalized_replay(
    connection: sqlite3.Connection,
    replay: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult
```

The replay input already accepts:

```python
field_evidence_entries: list[dict[str, object]]
```

Codex C may add private helpers inside `analytics_ingest.py`, but must not add
a public CLI, live ingest path, Google Sheets sync, schema migration, or raw log
reader in this slice.

## Observed Current Behavior

- `ParserNormalizedReplayInput` already includes `field_evidence_entries`.
- `normalize_parser_normalized_replay()` already accepts
  `replay["field_evidence_entries"]` as a list of mappings.
- `deterministic_ingest_run_id()` already includes `field_evidence_entries` in
  the canonical replay hash.
- `_TOUCHED_TABLES` already includes `fact_provenance`.
- `fact_provenance` already supports multiple rows for the same
  `fact_table`, `fact_id`, and `fact_field`.
- `_upsert_fact_provenance()` writes most required storage columns, but its
  current deterministic id is one row per fact field and it sets
  `invariant_status` to `None`.
- Current ingest still treats `field_evidence_entries` as deferred:
  successful ingest reports them in `result.skipped` and emits the warning
  `field_evidence_entries are accepted but deferred by the first ingest pass`.
- `evidence_ledger.validate_field_evidence()` already validates the canonical
  field-evidence schema, vocabulary labels, review-required rule, and privacy
  markers.

## Required Input Shape

Each item in `replay["field_evidence_entries"]` must be a mapping containing:

1. A canonical field-evidence record compatible with
   `evidence_ledger.validate_field_evidence()`.
2. Analytics attachment fields that identify the SQLite fact row and field the
   evidence describes.

Required canonical field-evidence fields:

- `object`
- `schema_version`
- `ledger_version`
- `entry_id`
- `output_family`
- `output_field`
- `value_source`
- `confidence`
- `finality`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`
- `source_event_timestamp`
- `drift_flags`
- `invariant_status`
- `degraded_reason`
- `review_required`

Required canonical values:

- `object = "mythic_edge_player_log_field_evidence"`
- `schema_version = "player_log_field_evidence.v1"`
- `ledger_version = "player_log_evidence_ledger.v1"`

Required analytics attachment fields:

- `fact_table`: SQLite fact table name, such as `matches`, `games`,
  `game_results`, `gameplay_actions`, or `opponent_card_observations`
- `fact_id`: deterministic primary key of an existing fact row
- `fact_field`: SQLite column or field label being evidenced
- `source_parser_surface`: safe parser-owned surface label, such as
  `MatchSummary.to_match_log_row`, `GameSummary.to_game_log_row`,
  `gameplay_actions.py`, or `opponent_card_observations.py`
- `source_fact_key`: parser-normalized fact key that produced the fact field

The analytics attachment fields are not part of the canonical evidence-ledger
schema. They are required here only so local SQLite can attach a validated
field-evidence record to the correct `fact_provenance` target.

Input entries may include additional non-authoritative labels only when they
are safe, deterministic, and not raw/private evidence. Extra fields must not be
needed to pass required tests.

## Outputs

Successful ingest of valid field-evidence entries must write
`fact_provenance` rows.

Required mapping:

- `ledger_entry_id`: input `entry_id`
- `fact_table`: input `fact_table`
- `fact_id`: input `fact_id`
- `fact_field`: input `fact_field`
- `source_parser_surface`: input `source_parser_surface`
- `source_fact_key`: input `source_fact_key`
- `source_event_kind`: input `source_event_kind`, or null when empty
- `source_event_type`: input `source_event_type`, or null when empty
- `source_payload_paths`: stable JSON text array copied from input
- `source_event_timestamp`: input `source_event_timestamp`, or null when empty
- `value_source`: input `value_source`
- `confidence`: input `confidence`
- `finality`: input `finality`
- `drift_flags`: stable JSON text array copied from input
- `invariant_status`: input `invariant_status`
- `degraded_reason`: input `degraded_reason`, or null when empty
- `review_required`: 1 when input is true, otherwise 0
- `ingest_run_id`: current ingest run id
- `created_at`: current ingest timestamp

Field-evidence ingest must not update the parser fact row itself in this first
slice. Core provenance columns on fact tables may remain as written by the
existing match/game/gameplay-action/opponent-observation ingest paths.

## Deterministic Row Identity

Field-evidence provenance rows must use deterministic IDs that allow multiple
provenance rows for the same fact field.

The implementation must not reuse the existing default helper id pattern:

```text
{fact_table}:{fact_id}:{fact_field}:provenance
```

That id is one row per fact field and would collapse multiple field-evidence
records. Codex C should add an optional id override or a dedicated
field-evidence provenance helper.

Recommended id material:

- `fact_table`
- `fact_id`
- `fact_field`
- `entry_id`
- `source_parser_surface`
- `source_fact_key`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`

Recommended shape:

```text
field_evidence:{sha256(canonical_id_material)}
```

Repeated ingest of the same replay must upsert the same field-evidence
provenance rows without duplicating them.

## Required Guarantees

### Validation

Each field-evidence entry must be validated before any row is written.

Required validation:

- call `evidence_ledger.validate_field_evidence()` on the canonical
  field-evidence fields, or enforce exactly equivalent rules;
- require all analytics attachment fields listed above;
- require `fact_table`, `fact_id`, `fact_field`, `source_parser_surface`, and
  `source_fact_key` to be non-empty strings;
- require `fact_table` to be an existing analytics fact table, not a metadata
  table, `fact_provenance`, or an arbitrary SQL identifier;
- require the target fact row to already exist in the current database before
  writing field provenance;
- require `source_payload_paths` and `drift_flags` to be lists of strings;
- reject unknown `value_source`, `confidence`, `finality`, `drift_flags`, or
  `invariant_status` values;
- reject mismatched `review_required` values when the evidence-ledger policy
  requires review;
- reject raw Player.log lines, raw JSON payload copies, webhook URLs, workbook
  IDs, API keys, local absolute paths, and private runtime artifact paths.

Malformed field evidence must fail clearly and roll back the transaction. It
must not be reported as skipped, and it must not produce partial fact rows.

### Review-Required Rule

`review_required` must match the existing evidence-ledger rule:

- true when `invariant_status == "failed"`
- true when `value_source == "conflict"`
- true when `confidence == "low"` and `finality` is `final` or `reconciled`
- false otherwise

### Privacy

`source_payload_paths` must contain labels or JSON-pointer-like paths only.

Allowed examples:

- `/match_log_rows/0/match_id`
- `/game_log_rows/0/game_number`
- `/gameplay_action_entries/0/action_type`
- `/opponent_card_observations/0/visibility`
- `payload.match_id`

Forbidden examples:

- raw Player.log lines
- raw saved-event JSON
- absolute local paths
- webhook URLs
- workbook IDs
- API keys, tokens, secrets, or credentials
- runtime status file paths
- failed-post artifact paths

### Idempotency

Repeated ingest of the same parser-normalized replay must:

- preserve one deterministic `ingest_runs` row for that replay hash;
- preserve fact row counts after the first successful ingest;
- preserve field-evidence provenance row counts after the first successful
  ingest;
- update mutable storage metadata for the same deterministic provenance id
  without creating duplicates;
- avoid deleting existing automatically generated provenance rows.

### Row Counts, Skips, And Warnings

After implementation:

- valid `field_evidence_entries` must not appear in `result.skipped`;
- valid `field_evidence_entries` must not emit the current deferred warning;
- `result.row_counts["fact_provenance"]` and `ingest_runs.row_counts_json`
  must include field-evidence provenance rows;
- malformed field evidence must raise `AnalyticsReplayIngestError` or another
  explicit ingest validation error and roll back;
- no new database tables are required.

## Error Behavior

Required failure cases:

- `field_evidence_entries` is not a list of mappings;
- a field-evidence entry is missing canonical fields;
- a field-evidence entry has the wrong object, schema version, or ledger
  version;
- vocabulary labels are unknown;
- `review_required` does not match the evidence-ledger policy;
- `source_payload_paths` or `drift_flags` are not lists of strings;
- analytics attachment fields are missing or empty;
- `fact_table` is unknown, metadata-only, or unsafe;
- the referenced target fact row does not exist;
- privacy checks detect raw/private content.

All failures must be all-or-nothing for the ingest transaction.

## Side Effects

Allowed side effects:

- write or update `ingest_runs`;
- write or update existing parser-normalized analytics fact rows already owned
  by prior contracts;
- write or update `fact_provenance` rows for valid field-evidence entries.

Forbidden side effects:

- parser behavior changes;
- parser state final reconciliation changes;
- parser event class or payload shape changes;
- match/game identity or deduplication changes;
- SQLite schema migration changes;
- committed SQLite database files;
- raw Player.log storage;
- raw saved-event storage;
- workbook schema changes;
- webhook payload changes;
- Apps Script changes;
- Google Sheets sync;
- Line Tracer or AI/OpenAI runtime behavior;
- secrets, credentials, environment variables, generated data, runtime status
  files, failed posts, workbook exports, or production behavior.

## Compatibility

Existing replay inputs without `field_evidence_entries` must continue to ingest
successfully.

Existing deferred-field-evidence assertions in analytics tests must be updated
only where they specifically expect `field_evidence_entries` to remain skipped.
Gameplay-action and opponent-observation behavior must remain unchanged except
for any result warning/skipped changes caused by valid field evidence now being
handled.

## Unknowns

- The durable producer of replay-ready field-evidence entries is not yet fixed
  by this contract.
- Runtime field-evidence reports currently use attachment shapes; Codex C must
  decide whether the replay fixture supplies direct field-evidence dictionaries
  or flattens those attachments before ingest.
- There is no SQLite foreign key from `fact_provenance` to each possible
  `fact_table`; target-row existence must be checked in application code.
- The first implementation may not cover every evidence-ledger output family.
  It should prove representative match/game/action/observation targets without
  fabricating unsupported facts.

## Suspected Gaps

- `analytics_ingest.py` currently skips all `field_evidence_entries`.
- `_upsert_fact_provenance()` currently hardcodes one provenance id per fact
  field, which is too coarse for field-evidence ingest.
- `_upsert_fact_provenance()` currently sets `invariant_status` to `None`.
- Existing tests still assert that field evidence remains deferred after
  gameplay-action and opponent-observation ingest.
- No focused analytics test currently proves that canonical field-evidence
  validation is enforced before storage.

## Tests Required

Codex C should add:

```text
tests/test_analytics_field_evidence_ingest.py
```

Required focused coverage:

- valid field-evidence entries write `fact_provenance` rows;
- stored rows preserve `ledger_entry_id`, `source_parser_surface`,
  `source_fact_key`, `source_event_kind`, `source_event_type`,
  `source_payload_paths`, `source_event_timestamp`, `value_source`,
  `confidence`, `finality`, `drift_flags`, `invariant_status`,
  `degraded_reason`, and `review_required`;
- valid field-evidence entries are not reported as skipped or deferred;
- `row_counts` and `ingest_runs.row_counts_json` include the added
  `fact_provenance` rows;
- repeated ingest is idempotent for field-evidence provenance rows;
- multiple field-evidence rows may attach to the same `fact_table`,
  `fact_id`, and `fact_field` without collapsing;
- existing automatically generated provenance rows are not deleted;
- malformed canonical evidence fails and rolls back;
- malformed analytics attachment fields fail and roll back;
- a missing target fact row fails and rolls back;
- privacy violations in path-like fields fail and roll back;
- fact rows are not mutated by field-evidence ingest.

Regression coverage:

```powershell
py -m pytest -q tests/test_analytics_field_evidence_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py
py -m ruff check src tests
git diff --check
```

Protected-surface validation:

```powershell
@'
docs/contracts/analytics_field_evidence_ingest.md
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_field_evidence_ingest.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/analytics_field_evidence_ingest.md` exists and is tracked.
- Valid replay field-evidence entries are stored as `fact_provenance` rows.
- Invalid field-evidence entries fail before partial storage.
- Field-evidence ingest uses canonical evidence-ledger validation or equivalent
  checks.
- Field-evidence rows use deterministic ids that allow multiple provenance
  records for the same fact field.
- `invariant_status` is preserved in SQLite.
- `review_required` follows the evidence-ledger rule.
- Valid field evidence is no longer reported as deferred or skipped.
- No schema migration, parser behavior change, raw log storage, workbook
  schema change, webhook change, Apps Script change, AI runtime behavior, or
  production behavior is introduced.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the analytics-foundation slice:

[analytics] Field-evidence ingest into SQLite

Current branch/base branch:
codex/analytics-foundation

Source contract:
docs/contracts/analytics_field_evidence_ingest.md

Context:
- SQLite schema v1, migration loader, parser-normalized replay ingest, gameplay-action ingest, and opponent-card-observation ingest are complete.
- Current inspected commit for the contract pass was 8cdfcaeae5e561d73056eeeda6ca0e3597564701.
- `field_evidence_entries` are currently accepted by analytics replay input but still deferred/skipped.
- Do not target main or open a PR.

Task:
Compare the current implementation to docs/contracts/analytics_field_evidence_ingest.md. Implement only the narrow field-evidence ingest slice if the contract is clear.

Before editing, state:
- what field-evidence ingest is supposed to do;
- what the current code actually does;
- why it is failing or incomplete;
- the exact minimal implementation plan.

Required implementation focus:
- validate canonical field-evidence records using `evidence_ledger.validate_field_evidence()` or equivalent rules;
- require analytics attachment fields for `fact_table`, `fact_id`, `fact_field`, `source_parser_surface`, and `source_fact_key`;
- write deterministic `fact_provenance` rows that preserve ledger entry id, source labels, payload path labels, value source, confidence, finality, drift flags, invariant status, degraded reason, and review-required flag;
- allow multiple provenance rows for the same fact field without collapsing them;
- remove the deferred warning/skipped behavior for valid `field_evidence_entries`;
- fail malformed/private/missing-target evidence without partial writes;
- keep parser facts, parser behavior, schema, workbook/webhook/App Script behavior, raw logs, generated data, runtime artifacts, and production behavior untouched.

Expected tests:
- add focused tests in `tests/test_analytics_field_evidence_ingest.py`;
- update stale deferred-field-evidence assertions only where this contract changes behavior.

Validation:
py -m pytest -q tests/test_analytics_field_evidence_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py
py -m ruff check src tests
git diff --check
@'
docs/contracts/analytics_field_evidence_ingest.md
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_field_evidence_ingest.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed;
- source contract used;
- files changed;
- exact functions/tests changed;
- validation run;
- protected-surface status;
- remaining risks;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  completed_thread: "B"
  next_thread: "C"
  branch: "codex/analytics-foundation"
  source_artifact: "Codex A handoff for analytics_field_evidence_ingest"
  target_artifact: "docs/contracts/analytics_field_evidence_ingest.md"
  risk_tier: "Medium"
  validation:
    - "git status / branch / commit inspected before contract edit"
    - "source analytics ingest, evidence ledger, schema, and focused tests inspected"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser behavior."
    - "Do not change parser state final reconciliation."
    - "Do not change parser event classes."
    - "Do not change match/game identity or deduplication."
    - "Do not alter SQLite schema or create database files in this slice."
    - "Do not store raw Player.log data."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, Line Tracer, AI/OpenAI runtime behavior, secrets, generated data, runtime artifacts, workbook exports, CI gates, or production behavior."
```
