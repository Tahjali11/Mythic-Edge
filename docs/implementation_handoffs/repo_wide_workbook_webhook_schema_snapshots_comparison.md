# Repo-Wide Workbook/Webhook Schema Snapshot Tests Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/92

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/82

## Contract

`docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Worktree

- Branch confirmed: `codex/repo-wide-hardening-run`
- Branch tracks: `origin/codex/repo-wide-hardening-run`
- Initial dirty state: only
  `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md` was
  untracked
- Unrelated changes: none observed

The untracked source contract is in scope for issue #92 and was not treated as
unrelated work.

## What #92 Is Supposed To Protect

Issue #92 protects repo-side workbook/webhook schema contracts from accidental
drift. It is a coverage-confirmation and gap-closing issue, not a behavior
change issue and not a duplicate of the issue #60 parser event schema snapshot
suite.

The protected surfaces include:

- workbook landing row keys for `MatchLogRow` and `GameLogRow`
- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS`
- runtime workbook export row families and row keys
- repo-side Apps Script field maps, landing headers, dispatch families, and
  runtime row-builder consumed keys
- webhook-facing row dictionaries passed to `post_row_to_google_sheets()` and
  `submit_row_to_google_sheets()`
- stable identity fields such as `event_family`, `event_type`, `scope`,
  `match_id`, and `timestamp`

## Existing #60 Coverage Confirmed

`tests/test_event_schema_snapshots.py` and
`tests/fixtures/schema_snapshots/*.json` already cover most of issue #92:

- `workbook_row_keys.json` snapshots ordered `MatchLogRow` and `GameLogRow`
  keys, row metadata, `MATCH_LOG_SYNC_FIELDS`, and `GAME_LOG_SYNC_FIELDS`.
- The snapshot test asserts `"MGTA Start Time"` remains present in
  `MatchLogRow`.
- The snapshot test asserts `MATCH_LOG_SYNC_FIELDS` is a subset of
  `MatchLogRow` keys and `GAME_LOG_SYNC_FIELDS` is a subset of `GameLogRow`
  keys.
- `sheet_schema_surfaces.json` snapshots runtime sheet specs, runtime
  `event_type` values, runtime `scope` values, sync fields, and
  `SYNC_FIELDS_BY_ROW_KIND`.
- `runtime_export_row_keys.json` snapshots row keys and metadata for
  `ActionLogRow`, `DeckSnapshotRow`, `CollectionSnapshotRow`,
  `ParserStatusRow`, and `CardPerformanceRow`.
- `apps_script_repo_parity.json` snapshots repo-side Apps Script dispatch
  families under test, Match/Game field-map keys, runtime landing headers,
  runtime build-object headers, and runtime build-object consumed data keys.
- Snapshot fixtures are stable schema metadata only and are guarded by the
  existing explicit update policy.

No new #60-style snapshot fixture was needed.

## Output Coverage Before This Pass

`tests/test_app_outputs.py` already covered:

- failed webhook post persistence
- retry success and terminal retry failure
- missing webhook URL behavior
- successful status updates
- webhook target redaction
- async dispatch dedupe
- async job top-level shallow copy behavior
- callback/result drain behavior
- dispatcher lifecycle
- local JSONL append behavior

The contract gap was that no test explicitly asserted synchronous webhook
posting sends the row dictionary directly as the top-level JSON body with no
wrapper or envelope.

## What Changed

Added two focused tests:

- `tests/test_webhook_payload_schema.py::test_webhook_post_sends_row_dict_as_top_level_json_payload`
  - proves `post_row_to_google_sheets(row)` calls `requests.post(...,
    json=row, timeout=10)`
  - makes the no-wrapper/no-envelope webhook payload contract explicit
  - preserves `outputs.py` as schema-agnostic transport

- `tests/test_tier_sync.py::test_tier_source_snapshot_payload_top_level_schema_is_stable`
  - proves `TierSourceSnapshot` payloads use stable top-level webhook keys:
    `event_family`, `event_type`, `scope`, `timestamp`, `records`, `raw_json`
  - stubs all scrapers and uses no network access
  - does not snapshot actual tier records, generated tier data, public source
    payloads, raw JSON values, URLs beyond already-public constants, live
    workbook state, or deployed Apps Script state

## Files Changed

- `tests/test_webhook_payload_schema.py`
- `tests/test_tier_sync.py`
- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`

Also present as the source artifact:

- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`

## Code Changed

No production/runtime code changed.

## Tests Added Or Updated

Tests changed:

- Added a focused direct webhook JSON payload/envelope assertion.
- Added a focused `TierSourceSnapshot` top-level schema assertion.

No snapshot fixtures were added or updated.

## Interface Changes

No runtime interface changed.

The tests now explicitly lock existing behavior:

- synchronous webhook transport sends the caller's row dictionary as the
  top-level JSON body
- `TierSourceSnapshot` top-level payload keys remain stable for repo-side
  webhook/App Script dispatch

## Contract Matches

- Existing #60 snapshots already protect workbook landing row keys, sync
  fields, runtime schema surfaces, runtime export row keys, and repo-side Apps
  Script parity.
- Existing app output tests already protected retry/failure/redaction/dispatch
  behavior and async top-level shallow-copy semantics.
- The new output test closes the explicit synchronous no-wrapper/no-envelope
  webhook payload gap.
- The new tier-sync test closes the stable top-level `TierSourceSnapshot`
  payload-key gap without pulling generated tier data into snapshots.
- Apps Script parity remains repo-side only.
- Live workbook state and deployed Apps Script state remain out of scope.

## Contract Mismatches Or Gaps

No contract mismatch requiring production code changes was found.

Remaining accepted gap:

- Deeper `TierSourceSnapshot` record-level Apps Script helper parity is not
  snapshotted here. It depends on generated/external tier-source data and helper
  workbook behavior, so a future tier-source/workbook contract should own that
  if more coverage is desired.

## Snapshot Fixture Status

No snapshot fixtures changed.

Existing snapshot update policy remains unchanged:

- no auto-update
- schema mismatches are review signals
- snapshot updates require explicit issue, contract, implementation handoff,
  review, and approval

## Protected Surface Status

No workbook schema, webhook payload shape, Apps Script behavior, parser
behavior, parser state final reconciliation, parser event classes, match/game
identity, deduplication, secrets, environment variables, raw logs, generated
data, runtime status files, failed posts, workbook exports, live workbook
state, deployed Apps Script state, or production behavior changed.

The diff is test-only plus this handoff and the in-scope untracked contract.

## Validation Run

```powershell
git status --short --branch
```

Result: branch is `codex/repo-wide-hardening-run`; intended worktree changes
are `tests/test_tier_sync.py`, `tests/test_webhook_payload_schema.py`, this
handoff, and the in-scope untracked source contract.

```powershell
py -m pytest -q tests\test_webhook_payload_schema.py
```

Result: `1 passed`.

```powershell
py -m pytest -q tests\test_tier_sync.py
```

Result: `7 passed`.

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
```

Result: `6 passed`.

```powershell
py -m pytest -q tests\test_webhook_payload_schema.py tests\test_app_outputs.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_tier_sync.py
```

Result: `70 passed`.

```powershell
py -m pytest -q tests\test_select_validation.py tests\test_check_surface_authorization.py
```

Result: `48 passed`.

```powershell
py -m ruff check src tests tools
```

Result: `All checks passed!`

```powershell
py -m pyright
```

Result: failed in this shell with resolver/environment findings, including
missing imports for `pytest`, `bs4`, and `requests`, followed by a Windows
`Python was not found` app-execution-alias message. This appears to be the raw
Pyright environment path, not a regression from this test-only diff.

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
```

Result: passed. The repo-approved advisory wrapper resolved the active Python
interpreter and reported `0 errors, 0 warnings, 0 informations`.

```powershell
py tools\check_agent_docs.py
```

Result: passed. `checked_files: 45`, `errors: 0`, `warnings: 0`.

```powershell
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `scanned_paths: 0`, `forbidden: 0`, `warnings: 0`. This is
a HEAD-based check; unstaged and untracked local changes are covered by the
path-scoped check below.

```powershell
@('tests/test_webhook_payload_schema.py','tests/test_tier_sync.py','docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md','docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md') | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: warning, not failure. `scanned_paths: 4`, `forbidden: 0`,
`warnings: 4`. Warnings are policy/reference mentions of failed-post/runtime
artifact wording in the contract and handoff, not committed secrets or private
payloads.

```powershell
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `changed_paths: 0`, `forbidden: 0`, `warnings: 0`.

```powershell
@('tests/test_webhook_payload_schema.py','tests/test_tier_sync.py','docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md','docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md') | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: passed with `changed_paths: 4`, `forbidden: 0`, `warnings: 0`.

```powershell
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_workbook_webhook_schema_snapshots_comparison.md
```

Result: passed with `changed_paths: 0`, `authorization_status: ok`.

```powershell
@('tests/test_webhook_payload_schema.py','tests/test_tier_sync.py','docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md','docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md') | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_workbook_webhook_schema_snapshots_comparison.md
```

Result: passed with `changed_paths: 4`, `protected: 0`, `forbidden: 0`,
`authorization_status: ok`.

```powershell
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
```

Result: passed with `changed_paths: 0`, `selection_status: ok`.

```powershell
@('tests/test_webhook_payload_schema.py','tests/test_tier_sync.py','docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md','docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md') | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Result: passed with `changed_paths: 4`, `selection_status: ok`. Required
recommendations included focused tests for `tests/test_webhook_payload_schema.py`
and `tests/test_tier_sync.py`, Ruff, secret scan, protected-surface gate, and
`git diff --check`; recommended `tools/check_agent_docs.py`, which passed.

```powershell
git diff --check
```

Result: passed.

## Still Unverified

- Codex E review / contract-test verdict.
- Live workbook state and deployed Apps Script state, intentionally out of
  scope.
- Whether future tier-source work should add record-level schema parity under a
  separate issue/contract.
- PR submission, CI, merge, tracker updates, and issue closure.

## Reviewer Focus

Codex E should verify:

- The new tests are test-only and do not change production behavior.
- The direct webhook JSON payload assertion correctly captures the
  no-wrapper/no-envelope contract without changing webhook shape.
- The `TierSourceSnapshot` test is schema-level, deterministic, network-free,
  and does not commit generated/external tier data.
- Existing #60 snapshot coverage is correctly mapped and not duplicated.
- No snapshot fixtures changed.
- Apps Script parity remains repo-side only.
- Tracker #82 remains open and this work does not target `main`.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #92.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/92

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md

Implementation handoff:
docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md

Review the diff against the issue, tracker, contract, handoff, and current tests.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md
- docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/*.json
- tests/test_app_outputs.py
- tests/test_webhook_payload_schema.py
- tests/test_tier_sync.py
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/app/tier_sync.py
- tools/google_apps_script/Code.gs

Lead with findings. Verify:
- existing #60 snapshot coverage already protects workbook row keys, sync fields, runtime schema surfaces, runtime export row keys, and repo-side Apps Script parity
- the new direct webhook payload test proves no wrapper/envelope without changing webhook shape
- the new TierSourceSnapshot top-level schema test is deterministic, schema-level, network-free, and does not commit generated tier data
- no snapshot fixtures changed or were auto-updated
- Apps Script parity remains repo-side only
- no workbook schema, webhook payload shape, Apps Script behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, or production behavior changed
- tracker #82 remains open and the work does not target main

Validation to check or rerun:
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_webhook_payload_schema.py tests\test_app_outputs.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_tier_sync.py
py -m pytest -q tests\test_select_validation.py tests\test_check_surface_authorization.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_workbook_webhook_schema_snapshots_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

Do not edit files in review-only mode. Do not stage, commit, open a PR, merge, close issue #92, or mark tracker #82 complete.

Produce docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md or a review verdict with findings, validation evidence, protected-surface status, remaining risks, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/92"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md"
  target_artifact: "docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "py -m pytest -q tests\\test_webhook_payload_schema.py -> 1 passed"
    - "py -m pytest -q tests\\test_tier_sync.py -> 7 passed"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed"
    - "py -m pytest -q tests\\test_webhook_payload_schema.py tests\\test_app_outputs.py tests\\test_sheet_schema.py tests\\test_sheet_exports.py tests\\test_tier_sync.py -> 70 passed"
    - "py -m pytest -q tests\\test_select_validation.py tests\\test_check_surface_authorization.py -> 48 passed"
    - "py -m ruff check src tests tools -> All checks passed"
    - "py -m pyright -> failed from raw resolver/environment noise; advisory wrapper passed"
    - "powershell -ExecutionPolicy Bypass -File tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings, 0 informations"
    - "py tools\\check_agent_docs.py -> passed"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed with changed paths 0"
    - "path-scoped secret scan -> warning only, forbidden 0, policy/reference artifact mentions only"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed with changed paths 0"
    - "path-scoped protected-surface gate -> passed with changed paths 4, forbidden 0, warnings 0"
    - "path-scoped surface authorization check -> authorization_status ok"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> passed with zero-diff advisory"
    - "path-scoped validation selector -> selection_status ok"
    - "git diff --check -> passed"
  stop_conditions:
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, or production behavior."
    - "Do not auto-update snapshots without explicit issue/contract/review approval."
    - "Do not target main."
    - "Do not mark tracker #82 complete."
    - "Do not stage, commit, open a PR, merge, or close issues unless explicitly asked."
```
