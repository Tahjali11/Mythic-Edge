# Contract Test Report: Live App Parser-Owned Fact Capture Into SQLite

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/244

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella Issue

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md`

Fixer handoff:
`docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md`

Reviewed files:

- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md`
- `docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

Issue #244 authorizes the first live local-app SQLite capture boundary for
parser-owned final/reconciled match and game facts. The implementation may add a
narrow live ingest adapter and read-only live ingest status route. It must not
start the parser runner, tail Player.log, inspect private Player.log contents,
write actual app-data root during review, store raw Player.log or raw
saved-event data, alter parser truth, change analytics schema, or enable
workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Internal Project Area Reviewed

Local analytics SQLite ingest and local app live-status surfaces.

## Bridge-Code Status Reviewed

`bridge_code`: parser-owned final match/game rows -> live-only analytics ingest
adapter -> existing SQLite fact tables -> read-only local app status. This
bridge remains local support storage and status reporting, not parser truth,
analytics truth, workbook truth, or AI truth.

## Findings

No blocking findings remain.

### CT-244-001 fixed_state_followup: Live sanitizer now rejects raw/private markers in source labels and nested row payloads before writes

Original finding: the live adapter rejected forbidden raw/private fields only at
the top payload level and used a weaker sanitizer for `source_artifact_label`.
That allowed raw/private markers in `match_log_rows[*]`, `game_log_rows[*]`,
and live source labels to be accepted despite the contract's fail-closed
privacy boundary.

Confirmed fixed after Codex D:

- `normalize_live_parser_owned_facts(...)` now validates live
  `source_artifact_label` through `_required_live_safe_label(...)`, the same
  stricter safe-label helper used for `session_id`
  (`src/mythic_edge_parser/app/analytics_ingest.py`, lines 252-253).
- `normalize_live_parser_owned_facts(...)` now screens both `match_log_rows` and
  `game_log_rows` through `_reject_live_unsafe_row_payloads(...)` before
  finality validation and before the ingest path can apply migrations or write
  rows (`src/mythic_edge_parser/app/analytics_ingest.py`, lines 256-260).
- `_reject_live_unsafe_row_payloads(...)` recursively rejects forbidden nested
  field names and unsafe private marker values in live row payloads
  (`src/mythic_edge_parser/app/analytics_ingest.py`, lines 2106-2167).
- New regression tests cover raw artifact source labels, forbidden nested row
  field names, unsafe private marker row values, and no partial durable writes
  (`tests/test_live_app_parser_owned_fact_capture_sqlite.py`, lines 117-124 and
  226-248).
- Codex E reproduction probes confirmed `source_artifact_label = "Player.log"`,
  nested `match_log_rows[0].player_log_path`, and unsafe
  `game_log_rows[0].debug_note` values are rejected before any SQLite tables are
  created.

## Checks Run

```bash
git status --short --branch --untracked-files=all
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
<manual sanitizer reproduction probe>
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_analytics_parser_normalized_replay_ingest.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
<generated SQLite/database artifact check>
```

## Results

Validation passed and CT-244-001 is confirmed fixed.

- Issue #244 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- Branch sync: `0 0`.
- Manual sanitizer reproduction probe: the three original accepted cases are
  now rejected before migrations/tables are created.
- `tests\test_live_app_parser_owned_fact_capture_sqlite.py`: `11 passed`.
- Combined live/replay tests:
  `py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_analytics_parser_normalized_replay_ingest.py`
  -> `35 passed`.
- Local app backend/config tests:
  `py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py`
  -> `34 passed, 1 existing FastAPI/Starlette deprecation warning`.
- Adjacent analytics ingest tests:
  `py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py`
  -> `77 passed`.
- Ruff: passed.
- Agent docs check: passed, `errors: 0`, `warnings: 0`.
- `git diff --check`: passed.
- Repo-level protected-surface scan: passed but reported `changed_paths: 0`
  because untracked files are not included by that mode.
- Repo-level secret/private-marker scan: passed but scanned `0` paths for the
  same untracked-file reason.
- Path-scoped protected-surface scan over the full #244 package: passed,
  `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the full #244 package: passed,
  `forbidden: 0`, `warnings: 0`.
- Generated SQLite/database artifact check: `data/analytics` is absent; no
  SQLite DB/WAL/SHM/journal artifacts were reported.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-244-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Contract forbids raw/private fields and raw log artifact labels in live input rows/source labels. Original implementation checked only top-level forbidden fields and used a weaker source label sanitizer. | Live source labels now use the stricter safe-label helper; match/game row payloads are recursively screened before writes; focused regression tests pass; Codex E probes confirm the previously accepted cases are rejected before tables are created. | F |

## Confirmed Contract Matches

- Direct parser-normalized replay still rejects `source_kind = live_parser`.
- The live adapter requires the live-specific entrypoint
  `ingest_live_parser_owned_facts(...)`.
- The live adapter requires `source_kind = live_parser`, safe
  `source_artifact_label`, safe `session_id`, and final/reconciled match/game
  rows.
- Live source labels and nested live row payloads now reject raw/private markers
  before any durable writes.
- Final/reconciled match and game rows are written into existing match/game fact
  families without changing analytics schema or migrations.
- Repeated live ingest is idempotent for fact rows.
- Replay import followed by live ingest for the same logical facts does not
  duplicate match/game fact rows.
- Live/provisional match rows are rejected and do not overwrite final facts.
- Gameplay action, opponent-card-observation, and field-evidence live payloads
  are skipped with warnings and not written in this slice.
- `GET /api/live/ingest/status` is read-only, disabled/status-only, symbolic, and
  covered by no-app-data-creation tests.
- Watcher process controls remain disabled; no runner/tailer calls were
  introduced.
- No parser behavior, final reconciliation, parser event classes, match/game
  identity, deduplication semantics, workbook schema, webhook payload shape, Apps
  Script, Sheets, OpenAI/AI/coaching, or production behavior changed.

## Contract Mismatches

None remaining.

## Missing Tests

No blocking missing tests remain for CT-244-001.

## Drift Notes

- No branch drift detected against `origin/codex/analytics-foundation`.
- Issue lifecycle is normal: #244 remains open; tracker #204 and umbrella #207
  remain open.
- Repo-level scans reported zero changed/scanned paths because this package
  currently includes untracked files; path-scoped scans were used for the actual
  touched package.
- No workbook, deployed Apps Script, production, actual private Player.log,
  actual app-data root, or live watcher process state was inspected or changed.

## Protected-Surface Status

Path-scoped protected-surface scan passed with `forbidden: 0`, `warnings: 0`.
The implementation did not intentionally touch parser/runtime/workbook/webhook/
Apps Script/Sheets/OpenAI/AI/coaching/production behavior.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with `forbidden: 0`,
`warnings: 0`. The runtime sanitizer hole from CT-244-001 is now covered by
focused tests and Codex E reproduction probes.

## Generated Artifact Status

No generated SQLite/database artifacts were reported. `data/analytics` is
absent. The reviewed tests use in-memory or temporary roots and did not create
tracked or untracked SQLite DB, WAL, SHM, journal, raw log, runtime,
failed-post, workbook-export, or local-only artifacts.

## Forbidden Scope

Forbidden scope was not touched during review or confirmation. I did not start
the parser runner, tail/read/hash/copy Player.log, inspect private Player.log
contents, write to the actual app-data root, stage, commit, push, open a PR,
merge, close issues, or mark tracker #204 complete.

## Verdict

Approved after Codex D fix. CT-244-001 is confirmed fixed and no blocking
contract-test findings remain.

## Recommendation

Route to Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #244.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/244

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Reviewed artifact:
docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md

Contract:
docs/contracts/live_app_parser_owned_fact_capture_sqlite.md

Implementation handoff:
docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md

Fixer handoff:
docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md

Submit the reviewed #244 package only. Inspect git status, confirm unrelated work is not staged, stage only the intended #244 files, commit, push, and open or update the draft PR targeting the approved integration branch. Do not target main, close issue #244, mark tracker #204 complete, start parser runner, tail Player.log, inspect private Player.log contents, write actual app-data root without explicit approval, or change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/244"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/live_app_parser_owned_fact_capture_sqlite.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/live_app_parser_owned_fact_capture_sqlite_fixer.md"
  target_artifact: "docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md"
  finding_confirmed_fixed:
    - "CT-244-001 P1: live sanitizer now rejects raw/private markers in source labels and nested row payloads before writes."
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "manual sanitizer reproduction probe -> original accepted cases now rejected before migrations/tables are created"
    - "py -m pytest -q tests\\test_live_app_parser_owned_fact_capture_sqlite.py -> 11 passed"
    - "py -m pytest -q tests\\test_live_app_parser_owned_fact_capture_sqlite.py tests\\test_analytics_parser_normalized_replay_ingest.py -> 35 passed"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 34 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_field_evidence_ingest.py -> 77 passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact check -> data/analytics absent; no SQLite/database artifacts reported"
  stop_conditions:
    - "Do not target main."
    - "Do not start parser runner or tail Player.log."
    - "Do not inspect private Player.log contents or write actual app-data root without explicit approval."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
```
