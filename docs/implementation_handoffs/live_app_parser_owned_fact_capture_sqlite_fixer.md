# Live App Parser-Owned Fact Capture SQLite Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/244

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella Issue

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`

## Review Artifact

`docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md`

## Internal Project Area

Local analytics SQLite ingest and local app live-status surfaces.

## Truth Owner

Parser/state remains the truth owner for parser-managed match and game facts.
The live analytics adapter is local bridge storage only and does not own parser,
workbook, webhook, or AI truth.

## Bridge-Code Status

`bridge_code`: parser-owned final/reconciled match and game rows into existing
local analytics SQLite fact tables.

## Role Performed

Codex D: Module Fixer.

## Finding Fixed

CT-244-001 P1: live sanitizer accepted raw/private markers in row payloads and
source labels instead of failing closed.

## What Changed

- Added focused live-ingest regression tests that first reproduced the accepted
  raw/private source label and nested row payload cases.
- Tightened live `source_artifact_label` validation to use the same safe live
  label policy as `session_id`.
- Added live-only row payload screening for `match_log_rows` and
  `game_log_rows` before migrations or writes begin.
- Rejected forbidden raw/private nested field names and unsafe private marker
  values in live row payloads.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md`

Existing issue #244 package files remain present from prior threads:

- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md`
- `docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md`

## Code Changed

Yes. Runtime code changed only in the live analytics ingest sanitizer path in
`src/mythic_edge_parser/app/analytics_ingest.py`.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations, manual import
semantics, workbook schema, webhook payload shape, Apps Script behavior, Sheets,
output transport, production behavior, OpenAI/AI/coaching behavior, or frontend
UI behavior was changed.

## Tests Added Or Updated

Added focused tests proving:

- `source_artifact_label = "Player.log"` is rejected by live ingest.
- `match_log_rows[0].player_log_path` is rejected when nested in a row.
- unsafe private marker values such as a row `debug_note` containing
  `Player.log` are rejected.
- each failure leaves no partial `ingest_runs`, `matches`, or `games` rows.

The new tests failed before the fix with 3 failures, then passed after the
sanitizer update.

## Interface Changes

No public interface, payload shape, route shape, workbook column, environment
variable, Apps Script entrypoint, schema, or migration change.

The live adapter now enforces the existing contract more strictly before
accepting payloads.

## Contracted Area Status

The fix stayed inside the contracted local analytics ingest bridge. It did not
start a parser runner, tail or inspect Player.log, write app-data files, enable
watcher process controls, or change downstream external behavior.

## Validation Run

```powershell
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
<generated SQLite artifact check>
```

Results:

- Focused live test before fix: failed, 3 failures reproducing CT-244-001.
- Focused live test after fix: passed, 11 passed.
- Replay ingest test: passed, 24 passed.
- Combined focused live/replay slice: passed, 35 passed.
- Local app backend/config slice: passed, 34 passed, 1 existing
  FastAPI/Starlette deprecation warning.
- Adjacent gameplay/opponent/field-evidence ingest slice: passed, 77 passed.
- Ruff: passed.
- Agent docs: passed, 46 checked files, 0 errors, 0 warnings.
- `git diff --check`: passed.
- Path-scoped protected-surface scan over 11 issue #244 paths: passed,
  forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 11 issue #244 paths: passed,
  forbidden 0, warnings 0.
- Generated SQLite artifact check: `data/analytics` is absent, so no generated
  SQLite artifacts were reported.

## Still Unverified

- No live parser runner, watcher tailing, actual app-data SQLite file, workbook,
  webhook, Apps Script, Sheets, production, OpenAI/AI, or browser UI behavior was
  exercised.
- Final confirmation by Codex E remains needed.

## Reviewer Focus

Codex E should confirm:

- raw/private source labels are rejected before any durable write;
- forbidden raw/private nested row fields are rejected before any durable write;
- unsafe private marker values in nested live row payloads are rejected before
  any durable write;
- replay/manual import behavior remains unchanged;
- no forbidden parser/runtime/workbook/webhook/App Script/Sheets/AI/production
  scope was touched.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #244.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/244

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_parser_owned_fact_capture_sqlite.md

Implementation handoff:
docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md

Review artifact:
docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md

Confirm only CT-244-001: live sanitizer now rejects raw/private markers in
source labels and nested match/game row payloads before any write begins.
Verify replay/manual import behavior and protected scope remain unchanged.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/244"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md"
  target_artifact: "docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md"
  branch: "codex/analytics-foundation"
  finding_fixed:
    - "CT-244-001 P1: live sanitizer now rejects raw/private markers in source labels and nested row payloads before writes."
  validation:
    - "focused live tests passed: 11 passed"
    - "focused live/replay tests passed: 35 passed"
    - "local app backend/config tests passed: 34 passed, 1 existing deprecation warning"
    - "adjacent analytics ingest tests passed: 77 passed"
    - "ruff passed"
    - "agent docs passed"
    - "git diff --check passed"
    - "path-scoped protected-surface scan passed: forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan passed: forbidden 0, warnings 0"
    - "generated SQLite artifact check passed: no data/analytics directory"
  forbidden_scope_touched: false
  next_step: "Codex E should confirm CT-244-001 and route onward if clean."
```
