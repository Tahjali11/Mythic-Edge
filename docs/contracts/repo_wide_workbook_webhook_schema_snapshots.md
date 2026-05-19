# Repo-Wide Workbook/Webhook Schema Snapshot Tests Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/92

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Primary prior snapshot artifact:

- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/*.json`

Adjacent contracts and hardening artifacts:

- `docs/contracts/parser_models.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`

Relevant source and test surfaces:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/tier_sync.py`
- `tools/google_apps_script/Code.gs`
- `tests/test_event_schema_snapshots.py`
- `tests/test_sheet_schema.py`
- `tests/test_sheet_exports.py`
- `tests/test_app_outputs.py`
- `tests/test_tier_sync.py`

This is a contract-writing artifact only. It does not implement tests, add or
update snapshots, refresh expected outputs, change workbook schema, change
webhook payload shape, change Apps Script behavior, change parser behavior,
touch secrets or local artifacts, target `main`, or mark tracker #82 complete.

## Module

Repo-wide workbook/webhook schema snapshot tests.

Plain English: this issue should confirm that the repo already has deterministic
guards for workbook-facing row shapes and Apps Script repo parity, then close
only the real gaps. It must not duplicate the parser event schema snapshot
suite from issue #60 just to create more snapshot files.

Expected future implementation artifact:

- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`

Expected future review or contract-test report:

- `docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md`

Possible test surfaces, subject to Codex C comparison:

- `tests/test_event_schema_snapshots.py`
- `tests/test_app_outputs.py`
- `tests/test_sheet_schema.py`
- `tests/test_sheet_exports.py`
- `tests/test_tier_sync.py`
- `tests/fixtures/schema_snapshots/*.json`

## Owning Layer

Repository hardening test infrastructure for workbook-facing and
webhook-facing schema boundaries.

Truth boundary:

- Parser/state and model serializers own parser-managed match and game facts.
- `sheet_schema.py` owns Python-side workbook schema vocabulary.
- `sheet_exports.py` owns runtime workbook export row construction.
- `outputs.py` owns webhook transport mechanics and must remain schema
  agnostic.
- `tools/google_apps_script/Code.gs` is repo-side Apps Script source and a
  downstream upsert/transport consumer. It is not proof of deployed Apps Script
  or live workbook state.
- Snapshot tests are drift guards and review signals. They do not authorize
  schema changes or make fixtures a source of parser truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`

Expected future files owned by implementation if needed:

- `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`
- `docs/contract_test_reports/repo_wide_workbook_webhook_schema_snapshots.md`
- narrow additions to `tests/test_event_schema_snapshots.py`
- narrow additions to `tests/test_app_outputs.py`
- optional stable schema snapshot fixture under
  `tests/fixtures/schema_snapshots/`

This contract does not own production parser/runtime/App Script source files.
Codex C may read them and test their current contracts, but must not change
their behavior under issue #92.

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- Current branch is `codex/repo-wide-hardening-run`.
- Local branch is even with `origin/codex/repo-wide-hardening-run`.
- Tracker #82 is open and names workbook/webhook schema snapshots as the next
  queue item after the protected-surface authorization checker.
- Issue #92 is open and frames this work as coverage confirmation and
  gap-closing, not duplicate snapshot implementation.
- Issue #60 is closed, and PR #61 merged the parser event schema snapshot
  package into the hardening lineage.
- `tests/test_event_schema_snapshots.py` and
  `tests/fixtures/schema_snapshots/*.json` already exist.
- `tests/test_app_outputs.py` already covers webhook retries, failed-post
  capture, missing webhook URL behavior, status updates, redaction,
  async-dispatch dedupe, callbacks, and dispatcher lifecycle.
- `tests/test_app_outputs.py` does not appear to explicitly assert that
  `post_row_to_google_sheets(row)` calls `requests.post(..., json=row, ...)`
  with the row dictionary as the complete webhook payload and no wrapper.
- `outputs.submit_row_to_google_sheets(row)` currently enqueues a shallow
  `dict(row)` copy in `WebhookDispatchJob.row`.
- `tools/google_apps_script/Code.gs` parses the POST body directly into
  `data`, dispatches on `data.event_family`, and expects row fields at the
  top level of that parsed object.

## Existing Issue #60 Snapshot Coverage

Issue #60 already covers the following workbook/webhook-adjacent surfaces.
Codex C must account for this coverage before adding anything.

### Workbook Landing Row Keys

`tests/fixtures/schema_snapshots/workbook_row_keys.json` already snapshots:

- current `MatchLogRow` ordered keys
- current `GameLogRow` ordered keys
- stable row metadata for those rows
- `MATCH_LOG_SYNC_FIELDS`
- `GAME_LOG_SYNC_FIELDS`

Existing assertions already require:

- `"MGTA Start Time"` to remain present in `MatchLogRow`
- `MATCH_LOG_SYNC_FIELDS` to remain a subset of `MatchLogRow` keys
- `GAME_LOG_SYNC_FIELDS` to remain a subset of `GameLogRow` keys

### Sheet Schema Surfaces

`tests/fixtures/schema_snapshots/sheet_schema_surfaces.json` already snapshots:

- runtime sheet family specs
- runtime `event_type` values
- runtime `scope` values
- ordered runtime landing headers
- ordered match/game sync fields
- `SYNC_FIELDS_BY_ROW_KIND`

### Runtime Export Row Keys

`tests/fixtures/schema_snapshots/runtime_export_row_keys.json` already
snapshots row keys and metadata for:

- `ActionLogRow`
- `DeckSnapshotRow`
- `CollectionSnapshotRow`
- `ParserStatusRow`
- `CardPerformanceRow`

### Apps Script Repo Parity

`tests/fixtures/schema_snapshots/apps_script_repo_parity.json` already
snapshots or asserts:

- Apps Script dispatch families under test
- Match Log field-map keys matching `MATCH_LOG_SYNC_FIELDS`
- Game Log field-map keys matching `GAME_LOG_SYNC_FIELDS`
- runtime landing headers matching Python runtime header tuples
- runtime build-object headers matching Python runtime header tuples
- Apps Script runtime build-object data keys as subsets of Python runtime
  export row keys

This is repo-side parity only. It does not inspect live workbook tabs or
deployed Apps Script.

## Public Interface Protected By This Contract

### Workbook-Facing Row Key Surfaces

Workbook-facing row key surfaces are the stable row dictionaries produced by:

- `MatchSummary.to_match_log_row()`
- `GameSummary.to_game_log_row()` through `MatchSummary.to_game_sheet_rows()`
- `sheet_exports.collect_runtime_sheet_rows()`

Required guarantee:

- Issue #92 must not add duplicate snapshots for row keys already covered by
  `workbook_row_keys.json` and `runtime_export_row_keys.json` unless Codex C
  finds a precise missing workbook/webhook-facing row family or identity field.

### Python Schema Vocabulary

Schema vocabulary includes:

- `MATCH_LOG_SYNC_FIELDS`
- `GAME_LOG_SYNC_FIELDS`
- runtime row family names
- runtime `event_type` values
- runtime `scope` values
- runtime landing headers
- `SYNC_FIELDS_BY_ROW_KIND`

Required guarantee:

- Existing `sheet_schema_surfaces.json` remains the primary snapshot for this
  vocabulary.
- Any proposed schema vocabulary change is out of scope for issue #92 and must
  route through protected-surface authorization.

### Webhook Payload Shape

The webhook-facing payload shape is the row dictionary supplied to:

- `post_row_to_google_sheets(row)`
- `submit_row_to_google_sheets(row)`

Observed transport contract:

- Synchronous posting calls `requests.post(WEBHOOK_URL, json=row, timeout=10)`.
- Async submission enqueues a shallow copy of the row, then the dispatcher
  passes that copied row to `post_row_to_google_sheets()`.
- There is no wrapper object such as `{ "row": row }`, `{ "payload": row }`, or
  `{ "data": row }`.
- There are no transport-added schema fields before posting.

Required guarantee:

- The webhook payload must remain exactly the caller-provided row dictionary at
  the top level unless a future webhook payload migration contract authorizes a
  change.
- `outputs.py` must remain schema agnostic. It may log, retry, enqueue, and
  report delivery status, but it must not add, remove, rename, validate, or
  reinterpret row fields.
- Tests should make the no-wrapper/no-envelope contract explicit if current
  output tests do not already do so.

### Apps Script POST Contract

The repo-side Apps Script receiver currently:

- parses `e.postData.contents` into a top-level `data` object
- reads `data.event_family`
- dispatches by top-level `data.event_family`
- reads top-level row fields for Match Log, Game Log, runtime rows, tier source
  snapshots, legacy match summary rows, archive/debug rows, and helper logic

Required guarantee:

- Repo-side parity tests may assert static expectations from
  `tools/google_apps_script/Code.gs`.
- They must not call live Apps Script, inspect deployment state, or claim live
  workbook parity.
- They should not overfit to unrelated internal helper structure when a public
  field-map/header/dispatch assertion is sufficient.

## Confirmed Gaps Or Clarifications For Codex C To Verify

Codex B identified these as likely gaps or clarifications. Codex C must verify
them against the current code/tests before editing.

1. Webhook envelope assertion is likely missing.
   - Existing snapshots cover row key inventories.
   - Existing output tests cover webhook behavior and lifecycle.
   - A focused test may still be needed to assert that synchronous webhook
     transport sends `json=row` directly, with no wrapper or extra keys.

2. Async dispatch payload copy behavior is behavioral coverage, not a schema
   snapshot.
   - If not already asserted clearly enough, a focused output test may assert
     that the enqueued job row has the same top-level key/value pairs as the
     submitted row and is a distinct top-level dict.
   - This must not become a deep-copy guarantee unless a future outputs
     contract authorizes it.

3. Apps Script dispatch coverage is intentionally filtered.
   - Existing #60 snapshots include the parser/workbook/runtime families under
     test.
   - `Code.gs` also dispatches `TierSourceSnapshot`, which comes from
     `tier_sync.py` and generated/external tier-source data.
   - Codex C must decide whether #92 should document this as an accepted
     adjacent gap, add a stable schema-only assertion for the
     `TierSourceSnapshot` top-level payload keys, or route it to a separate
     tier-source/workbook contract.
   - Any TierSourceSnapshot check must not scrape network sources, write
     generated tier data, snapshot live URLs beyond already-public source
     constants, or include actual tier records/raw JSON values.

4. No-op implementation remains acceptable.
   - If Codex C verifies that existing #60 snapshots plus current output tests
     already satisfy this contract, it may produce the comparison handoff with
     no test or fixture changes.
   - The handoff must explain exactly which tests/fixtures cover each required
     surface and why no duplicate snapshots were added.

## Allowed Snapshot Content

Allowed schema snapshot content:

- schema snapshot version
- row family names
- `event_family`, `event_type`, and `scope` stable literal values
- ordered row key lists
- ordered sync-field lists
- ordered header lists
- Apps Script static dispatch family names
- Apps Script static field-map keys
- Apps Script static runtime build-object data keys
- stable source/function names when useful for review
- an explicit marker that webhook transport posts the row dictionary directly,
  if Codex C chooses a snapshot rather than an ordinary output test

Forbidden or volatile snapshot content:

- raw MTGA logs
- raw parser payload values
- raw bytes or raw byte hashes
- real webhook URLs or Apps Script deployment IDs
- API keys, tokens, credentials, or environment variable values
- workbook IDs or private spreadsheet URLs
- local absolute paths
- generated card/tier/oracle data dumps
- runtime status files
- failed-post artifacts
- raw workbook exports
- live workbook state
- deployed Apps Script state
- timestamps as evidence values
- full tier-source records or scraped website payloads
- private transcript dumps

## Snapshot Update Policy

Snapshot updates must remain explicit and reviewed.

Rules:

- Codex B must not update snapshots.
- Codex C must not auto-update snapshots as a first response to failure.
- Snapshot mismatches are review signals. They do not authorize schema drift.
- Legitimate snapshot updates require issue #92 or a follow-up issue, this
  contract or an amended contract, implementation handoff, Codex E review, and
  explicit approval in the normal workflow.
- Existing `MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS=1` behavior in
  `tests/test_event_schema_snapshots.py` remains the approved update seam for
  #60-style schema snapshots unless Codex C justifies a narrower alternative.

## Required Guarantees

- Treat #92 as a coverage-confirmation and gap-closing issue.
- Do not duplicate #60 snapshot coverage without a precise missing surface.
- Keep workbook schema, webhook payload shape, Apps Script behavior, parser
  behavior, and parser truth ownership unchanged.
- Preserve direct webhook row-dictionary payload semantics.
- Preserve repo-side-only Apps Script parity boundaries.
- Keep tests deterministic from a clean clone.
- Do not require network access, live workbook access, deployed Apps Script, raw
  local logs, generated data, runtime artifacts, failed posts, workbook exports,
  or secrets.
- Keep any new snapshot content schema-level and stable.
- If existing coverage is sufficient, prefer a no-op comparison handoff over
  unnecessary new fixtures.

## Error Behavior

If a future test fails because a workbook/webhook-facing key changed:

- report the changed key, family, or fixture path
- do not auto-update snapshots
- do not silently "fix" Apps Script, workbook schema, parser serializers, or
  webhook payload shape
- route through protected-surface authorization when the diff implies schema,
  webhook, Apps Script, parser event, match/game identity, or deduplication
  drift

If Codex C finds that required coverage would require behavior changes:

- stop and route back to Codex B or Codex A
- do not implement behavior changes under issue #92

## Side Effects

Allowed side effects for future implementation:

- add or update focused tests
- add or update stable schema snapshot fixtures only if needed and authorized
  by this contract
- write the implementation handoff
- write the Codex E contract-test report in the review thread

Forbidden side effects:

- no workbook schema changes
- no webhook payload shape changes
- no Apps Script behavior changes
- no parser behavior changes
- no parser state final reconciliation changes
- no parser event class changes
- no match/game identity or deduplication changes
- no secrets, credentials, webhook URLs, or environment variable changes
- no raw logs, generated data, runtime status files, failed posts, workbook
  exports, or local-only artifacts
- no live Google Sheets or deployed Apps Script inspection
- no PR, merge, tracker closure, or `main` targeting from Codex B

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/repo-wide-hardening-run`.
2. Inspect git status and exclude unrelated changes.
3. Read issue #92, tracker #82, and this contract.
4. Read the #60 snapshot contract, implementation report, test file, and
   fixtures.
5. Map each #92 required surface to existing #60 coverage.
6. Inspect `outputs.py` and `tests/test_app_outputs.py` for direct webhook
   payload/envelope coverage.
7. Inspect `Code.gs` dispatch families and decide whether any untracked
   workbook/webhook family, especially `TierSourceSnapshot`, is in scope or
   should be documented as a follow-up.
8. Choose the narrowest implementation:
   - no-op comparison handoff if coverage is already sufficient
   - focused `tests/test_app_outputs.py` assertion for direct `json=row`
   - focused async job row-copy assertion if needed
   - narrow #60 snapshot extension only if a real schema inventory gap remains
9. Run focused validation.
10. Write
    `docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md`.
11. Route to Codex E for review or contract testing.

## Compatibility

- `MGTA Start Time` remains the current protected workbook compatibility
  spelling.
- `MatchLogRow`, `GameLogRow`, runtime row family names, runtime event types,
  scopes, sync fields, and Apps Script field maps remain unchanged.
- `outputs.py` remains transport-only and schema agnostic.
- Existing #60 snapshot fixtures remain the canonical schema inventory unless
  Codex C identifies a precise missing workbook/webhook surface.
- `TierSourceSnapshot` is recognized as an adjacent webhook/App Script family,
  but its generated/external tier-source data must not be pulled into schema
  snapshots as values.

## Tests Required

Contract-writer validation:

```powershell
git diff --check
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md
```

Focused implementation validation:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_app_outputs.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_tier_sync.py
py -m pytest -q tests\test_select_validation.py tests\test_check_surface_authorization.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-92.md --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_workbook_webhook_schema_snapshots_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

If implementation makes no test or fixture changes, Codex C should still run:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py tests\test_app_outputs.py
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Codex E may request broader validation if the diff touches snapshot fixtures,
Apps Script static parsing, output transport tests, or adjacent hardening tools.

## Acceptance Criteria

- This contract exists at
  `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`.
- The contract explicitly accounts for existing #60 snapshot coverage.
- The contract names the likely missing explicit webhook no-wrapper/envelope
  assertion.
- The contract permits a no-op/coverage-confirmation implementation handoff if
  existing tests are sufficient.
- Any new tests are test-only and preserve runtime behavior.
- Any new snapshot fixture contains only stable schema metadata.
- Snapshot update policy remains explicit and reviewed.
- Apps Script parity remains repo-side only.
- Live workbook and deployed Apps Script state remain out of scope.
- Protected surfaces are not changed.
- Tracker #82 remains open.
- Work stays on `codex/repo-wide-hardening-run`, not `main`.

## Open Questions And Contract Risks

- Whether `TierSourceSnapshot` should be included in this issue as a
  webhook/App Script schema surface or routed to a separate tier-source
  hardening issue.
- Whether the direct webhook payload contract should live as a simple focused
  assertion in `tests/test_app_outputs.py` instead of a new snapshot fixture.
- Whether future schema snapshots should include all Apps Script dispatch
  families exactly, or keep the current filtered-family approach to avoid
  overreaching into adjacent generated-data workflows.
- Whether selector output for issue #92 should be updated later to recommend
  any new snapshot or output-focused tests added by Codex C.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for repo-wide hardening issue #92: Workbook/webhook schema snapshot tests.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/92

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md

Goal:
Compare existing workbook/webhook schema snapshot coverage against the contract. Account for existing #60 snapshot coverage first. Implement only the smallest test-only gap closure needed, or produce a no-op coverage-confirmation handoff if existing tests already satisfy the contract.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/parser_models.md
- docs/contracts/parser_outputs.md
- docs/contracts/parser_sheet_schema.md
- docs/contracts/parser_sheet_exports.md
- docs/contracts/repo_wide_validation_selector.md
- docs/contracts/repo_wide_protected_surface_authorization_checker.md
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/*.json
- tests/test_app_outputs.py
- tests/test_sheet_schema.py
- tests/test_sheet_exports.py
- tests/test_tier_sync.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/sheet_exports.py
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/app/tier_sync.py
- tools/google_apps_script/Code.gs

Before editing:
- Confirm branch is codex/repo-wide-hardening-run.
- Inspect git status and exclude unrelated changes.
- State what #92 is supposed to protect, what #60 already covers, what remains missing or unclear, and the exact minimal implementation plan.

Do:
- Prefer coverage confirmation over duplicate snapshots.
- If needed, add a focused test proving post_row_to_google_sheets(row) sends the row dict directly as the JSON payload with no wrapper/envelope.
- If needed, add a focused test proving submit_row_to_google_sheets(row) enqueues a top-level shallow copy without changing payload keys.
- If a real schema inventory gap remains, extend the existing #60 snapshot file/fixture only with stable schema metadata.
- Decide whether TierSourceSnapshot is in scope, and either add a stable schema-only assertion or document a follow-up gap without scraping network data or committing generated tier data.
- Produce docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md.

Do not:
- change workbook schema, webhook payload shape, Apps Script behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, fixtures outside stable schema snapshots, or baselines
- auto-update snapshots without explicit contract/review approval
- duplicate existing #60 snapshot coverage without a precise missing surface
- target main
- mark tracker #82 complete
- stage, commit, open a PR, merge, or close issues unless explicitly asked

Validation:
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_app_outputs.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_tier_sync.py
py -m pytest -q tests\test_select_validation.py tests\test_check_surface_authorization.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-92.md --authorization-file contract=docs\contracts\repo_wide_workbook_webhook_schema_snapshots.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_workbook_webhook_schema_snapshots_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/92"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_workbook_webhook_schema_snapshots_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-92.md --authorization-file contract=docs\\contracts\\repo_wide_workbook_webhook_schema_snapshots.md"
  stop_conditions:
    - "Do not implement tests in Codex B."
    - "Do not add or update snapshots in Codex B."
    - "Do not refresh expected outputs."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, or production behavior."
    - "Do not target main."
    - "Do not mark tracker #82 complete."
```
