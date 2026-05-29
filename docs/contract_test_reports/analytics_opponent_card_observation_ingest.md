# Analytics Opponent-Card-Observation Ingest Contract-Test Report

report_lifecycle: initial_contract_test
role_performed: Codex E: Module Reviewer / contract-test thread
branch: codex/analytics-foundation
risk_tier: Medium

followup_lifecycle: followup_after_fixer
followup_role_performed: Codex E: Module Reviewer / confirmation thread
followup_fixer_handoff: `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md`

## Source Artifacts

- Contract: `docs/contracts/analytics_opponent_card_observation_ingest.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md`

## Files Reviewed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`

## Findings

### Follow-up Confirmation: Prior P1 fixed

finding_id: analytics_opponent_observation_ingest_001
finding_status: fixed_state_followup
blocking_status: resolved
next_route: Codex F
verification_evidence:

- `src/mythic_edge_parser/app/analytics_ingest.py:1284` now strips and validates each `degradation_flags` value before persistence.
- `src/mythic_edge_parser/app/analytics_ingest.py:1299` rejects path-like, URL-like, raw-log/private artifact, payload, and secret-marker labels.
- `tests/test_analytics_opponent_card_observation_ingest.py:376` covers unsafe degradation flags and confirms no partial observation or provenance rows are written.
- Direct reproduction check rejected `C:\private\Player.log`, `https://example.com/webhook`, raw payload marker, API-key marker, and failed-post payload marker with zero observation/provenance rows.

No remaining blocking findings were found in the Codex D confirmation pass.

### P1: `degradation_flags` can persist local paths or URLs into durable provenance

finding_id: analytics_opponent_observation_ingest_001
finding_status: original_finding
blocking_status: superseded_by_fixed_state_followup
next_route: Codex F after confirmation

`src/mythic_edge_parser/app/analytics_ingest.py:1271` accepts any string in `degradation_flags` without the safe-label validation already used for `source_artifact_label`. Those raw strings are serialized into `opponent_card_observations.degradation_flags` at `src/mythic_edge_parser/app/analytics_ingest.py:1082` and are also copied into durable `fact_provenance.drift_flags` and `fact_provenance.degraded_reason` at `src/mythic_edge_parser/app/analytics_ingest.py:1225` and `src/mythic_edge_parser/app/analytics_ingest.py:1226`.

That violates the contract prohibition in `docs/contracts/analytics_opponent_card_observation_ingest.md:524`, which says fact provenance must not store raw Player.log payloads, absolute local paths, webhook URLs, workbook IDs, API keys, secrets, or private runtime artifact paths.

Reproduction evidence from the public ingest API:

```text
degradation_flags input: ["C:\\private\\Player.log", "https://example.com/webhook"]
opponent_card_observations.degradation_flags:
["C:\\private\\Player.log","https://example.com/webhook"]
fact_provenance.drift_flags:
["C:\\private\\Player.log","https://example.com/webhook"]
fact_provenance.degraded_reason:
C:\private\Player.log;https://example.com/webhook
```

The focused safe-provenance test checks only `source_payload_paths` at `tests/test_analytics_opponent_card_observation_ingest.py:283`, so this path is currently unprotected by tests. The fix should keep parser-normalized labels accepted, but reject or sanitize path-like, URL-like, raw-log, secret-like, and private artifact marker values before writing observation drift/degradation text to durable rows or provenance.

## Contract Matches

- The implementation stores parser-normalized `opponent_card_observations` into the existing SQLite schema without adding a migration or schema file.
- The ingest path uses `opponent_card_observations.py` constants for object marker and schema version validation.
- The analytics layer does not call `build_opponent_card_observation()` or rebuild observations from raw gameplay actions.
- Opponent observations are no longer deferred/skipped when present.
- The implementation writes the expected parent observation row and optional child card row.
- Gameplay-action links are resolved from an explicit existing `gameplay_action_id`, or from the deterministic gameplay-action ID when the matching action was ingested in the same replay.
- Missing explicit gameplay-action links become warnings and `NULL` links, not failed ingest.
- Unknown parent games and malformed required fields fail the ingest transaction without partial fact rows.
- Idempotent re-ingest preserves deterministic row counts.
- Focused tests cover row counts, linking, null-link behavior, warning behavior, degraded observations, malformed input rollback, unknown parent rollback, and field-evidence remaining deferred.
- No parser, gameplay-action, opponent-observation classifier, workbook, webhook, Apps Script, production, or AI/model-provider behavior change was found in the reviewed diff.

## Contract Mismatches

- Resolved in follow-up: durable observation/provenance text now rejects unsafe `degradation_flags` values before persistence.

## Missing Tests Or Safeguards

- Resolved in follow-up: regression coverage now checks path-like, URL-like, raw payload marker, secret-like, and private artifact marker degradation flags.
- Remaining non-blocking risk: full repository tests were not run in this confirmation pass.

## Validation Run

- `git status --short --branch` -> branch confirmed as `codex/analytics-foundation`; expected modified/untracked implementation, contract, handoff, and focused test files observed.
- `py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py` -> 98 passed.
- `py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py` -> 26 passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped secret/private-marker scan over contract, handoff, `analytics_ingest.py`, and focused tests -> forbidden 0, warnings 1 on contract protected-surface wording.
- Path-scoped protected-surface check over contract, handoff, `analytics_ingest.py`, and focused tests -> forbidden 0, warnings 0.

Follow-up confirmation validation:

- `py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py` -> 29 passed.
- `py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py` -> 99 passed.
- `py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py` -> 26 passed.
- Direct unsafe-flag reproduction check -> all unsafe examples rejected with 0 observation rows and 0 provenance rows.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped secret/private-marker scan including fixer handoff and report -> forbidden 0, warnings 1 on contract protected-surface wording.
- Path-scoped protected-surface check including fixer handoff and report -> forbidden 0, warnings 0.

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/Apps Script/protected production surfaces were touched in the reviewed implementation scope.

## Secret / Private-Marker Status

Static path-scoped scan found no forbidden private or secret markers. The one warning is expected contract wording that mentions protected artifact categories.

Follow-up runtime review confirmed the unsafe-input path is fixed for path-like, URL-like, raw payload marker, secret-like, and private artifact marker values in `degradation_flags`.

## Generated SQLite Artifact Status

No changed or untracked SQLite database, WAL, SHM, journal, or `data/analytics` artifacts were found.

## Forbidden Scope

Forbidden scope was not otherwise touched. The blocker is an ingest validation/sanitization gap inside the authorized analytics ingest scope.

## Recommendation

Route to Codex F: Module Submitter. The prior P1 is resolved, and no new blocking findings were found in the confirmation pass.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for [analytics] Opponent-card-observation ingest into SQLite.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_opponent_card_observation_ingest.md

Review artifact:
docs/contract_test_reports/analytics_opponent_card_observation_ingest.md

Implementation handoff:
docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md

Fixer handoff:
docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md

Submit only the reviewed analytics opponent-card-observation ingest package.

Before staging, inspect `git status --short --branch` and stage only the intended package files:
- docs/contracts/analytics_opponent_card_observation_ingest.md
- docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md
- docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md
- docs/contract_test_reports/analytics_opponent_card_observation_ingest.md
- src/mythic_edge_parser/app/analytics_ingest.py
- tests/test_analytics_opponent_card_observation_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_analytics_parser_normalized_replay_ingest.py

Run:
py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py
py -m pytest -q tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
py -m pytest -q tests\test_opponent_card_observations.py tests\test_gameplay_actions.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over the intended package files if available.

Do not change parser behavior, opponent-card-observation classification behavior, gameplay-action classification behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, retry-queue payloads, workbook exports, generated SQLite files, or local runtime artifacts.

Do not target main. Open or update the draft PR only toward the approved analytics integration branch target if that is the established branch policy for this package.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_opponent_card_observation_ingest.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_opponent_card_observation_ingest_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_opponent_card_observation_ingest_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_opponent_card_observation_ingest.md"
  findings:
    - "Prior P1 fixed: unsafe degradation_flags no longer persist local paths, URLs, raw/private markers, or secret-like text into durable observation rows or fact_provenance drift/degraded fields."
  validation:
    - "py -m pytest -q tests\\test_analytics_opponent_card_observation_ingest.py -> 29 passed"
    - "py -m pytest -q tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> 98 passed"
    - "confirmation rerun of same analytics ingest/schema/loader slice after fixer -> 99 passed"
    - "py -m pytest -q tests\\test_opponent_card_observations.py tests\\test_gameplay_actions.py -> 26 passed"
    - "direct unsafe-flag reproduction check -> all unsafe examples rejected with 0 observation rows and 0 provenance rows"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 1 on contract protected-surface wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found"
  forbidden_scope_touched: false
  remaining_risks:
    - "Full repository test suite was not run in the confirmation pass."
    - "GitHub Actions not run locally."
  route: "Codex F"
```
