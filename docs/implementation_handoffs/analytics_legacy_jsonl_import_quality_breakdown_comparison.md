# Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/212

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

Related manual import issue: https://github.com/Tahjali11/Mythic-Edge/issues/211

## Contract

`docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Status

Branch confirmed:

```text
codex/analytics-foundation
```

Starting status included unrelated pre-existing local launcher dirt that was not
absorbed into this module:

- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- untracked `Start Mythic Edge Dev App.cmd`

The source contract was present as an untracked artifact from Codex B:

- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`
- issue #212, tracker #204, umbrella #207, and related issue #211
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`

## Current Behavior Compared To Contract

The repo already had the manual JSONL import route, process-local job lookup,
safe path redaction, adapter stats, and frontend import summary from issue
#211.

Contract gaps were present:

- `LegacyJsonlAdapterResult` had no `quality` object.
- `events_skipped` combined blank lines, duplicate raw-hash skips, and
  unsupported event kinds.
- processed supported event kinds were not counted.
- adapter warning codes/counts were not structured.
- incomplete replay output gaps remained only top-level warning strings.
- manual import job responses did not include `adapter.quality`.
- frontend types/API validation did not know the quality schema.
- the Manual Import panel displayed only the coarse adapter skipped count.

## Implementation Option Chosen

Implemented the reporting-only additive quality object authorized by the
contract. Existing top-level adapter and job fields remain compatible.

## Implemented Quality Schema

Added public adapter constants:

- `ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT =
  "mythic_edge_legacy_jsonl_import_quality"`
- `ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION =
  "analytics_legacy_jsonl_import_quality_breakdown.v1"`

`LegacyJsonlAdapterResult.quality` now includes:

- `quality_status`
- `records_seen`
- `events_processed`
- `events_skipped`
- `processed_kind_counts`
- `unsupported_kind_counts`
- `skipped_reason_counts`
- `blank_line_count`
- `duplicate_raw_hash_count`
- `unsupported_kind_skip_count`
- `output_gap_counts`
- `adapter_warning_counts`
- `adapter_warning_codes`
- `ingest_warning_codes`
- `routing_hints`
- `privacy`

The first version uses `incomplete_summary_unclassified` for incomplete replay
output gaps and leaves `incomplete_match_summary` and
`incomplete_game_summary` at `0`, because the current adapter cannot safely
split that boundary without parser/state behavior changes.

## Files Changed

New file:

- `docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md`

Modified files:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

Pre-existing unrelated dirty files preserved:

- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- `Start Mythic Edge Dev App.cmd`

## Exact Sections Changed

Adapter:

- added import-quality constants;
- added `quality` to `LegacyJsonlAdapterResult`;
- counted blank lines, duplicate raw hashes, unsupported event skips, and
  processed supported event kinds;
- built sanitized quality objects with warning-code counts, output-gap counts,
  privacy flags, and conservative routing hints;
- added failed-quality helper for fail-fast adapter errors.

Manual import backend:

- propagated `result.quality` under `adapter.quality`;
- added failed adapter quality for adapter failures such as invalid JSONL;
- copied sanitized ingest warning codes into the quality object when ingest
  completed with warnings.

Frontend:

- added `LegacyJsonlImportQuality` and routing-hint types;
- added API validation for quality object/schema/version/required fields;
- displayed quality status, processed kinds, skipped reasons, unsupported
  kinds, output gaps, warning codes, ingest warning codes, and routing hints in
  the existing Manual Import result panel;
- added small CSS for the nested quality breakdown section.

Tests:

- adapter tests now cover quality schema constants, blank-line counts,
  duplicate raw-hash counts without hash exposure, unsupported-kind counts,
  processed-kind counts, warning-code counts, routing hints, and unclassified
  output-gap counts;
- manual import tests now assert `adapter.quality` on success, degraded import,
  and failed adapter import;
- frontend API tests now reject missing or incompatible quality responses for
  terminal adapter states;
- frontend UI tests now verify quality breakdown display and continued absence
  of destructive controls or raw path retention.

## Code/Test/Doc Status

Code changed: yes.

Tests changed: yes.

Docs changed: yes, implementation handoff only.

SQLite schema changed: no.

Backend route inventory changed: no.

Parser behavior changed: no.

Saved-event replay semantics changed: no.

## Validation Run

```powershell
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
# -> 9 passed

py -m pytest -q tests\test_analytics_manual_jsonl_import.py
# -> 12 passed, 1 Starlette/httpx deprecation warning

py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
# -> 35 passed, 1 Starlette/httpx deprecation warning

npm --prefix frontend run typecheck
# -> passed

npm --prefix frontend run test -- --run
# -> 3 files passed, 18 tests passed

npm --prefix frontend ci
# -> passed, 113 packages installed/audited, 0 vulnerabilities

npm --prefix frontend run build
# -> initial parallel run failed while npm ci was rebuilding node_modules and vite was unavailable
# -> rerun after npm ci completed passed

py -m ruff check src tests tools
# -> All checks passed

git diff --check
# -> passed

py tools\check_secret_patterns.py --all
# -> all-repo advisory result failed with pre-existing repository-wide findings outside this touched slice

@'
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
src/mythic_edge_parser/local_app/import_jobs.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# -> passed, forbidden 0, warnings 0

@'
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
src/mythic_edge_parser/local_app/import_jobs.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# -> passed, forbidden 0, warnings 0
```

## Protected-Surface Status

No parser behavior, saved-event replay semantics, dedupe scope, parser state
final reconciliation, parser event classes, event kind values, match/game
identity, analytics SQLite schema/migrations, workbook schema, webhook payload
shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior,
OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or
production behavior was changed.

## Secret/Private-Marker Status

This implementation uses synthetic test records only. It does not commit, copy,
sanitize, fixture, or raw-dump a private local JSONL artifact.

No raw Player.log payloads, raw saved-event lines, raw hashes, full submitted
paths, stack traces, secrets, webhook URLs, API keys, generated SQLite files,
runtime status files, failed-post payloads, workbook exports, or generated card
data were added.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed after
the build check.

Generated/local artifact check after cleanup:

- `frontend/dist`: absent
- `frontend/.vite`: absent
- `frontend/coverage`: absent
- `data/analytics`: absent

Expected ignored dependency folder:

- `frontend/node_modules/` exists and is ignored.

## Forbidden Scope

Forbidden scope touched: no.

No destructive import, database, job, launcher, or UI actions were exposed.

No live Player.log watcher, parser runner control, file upload, copied import
retention, persistent job history, database reset/delete/wipe/export, Google
Sheets sync, Match Journal behavior, OpenAI/model-provider runtime integration,
AI/coaching behavior, Line Tracer, or production behavior was added.

## Still Unverified

- Manual import against a real private local JSONL artifact was not run.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.
- Browser visual inspection was not run; frontend behavior was verified by
  Vitest, TypeScript, and production build.
- All-repo secret/private-marker scan still reports pre-existing findings
  outside this touched slice.

## Reviewer Focus

Codex E should focus on:

- whether failed adapter quality should include zero/default counters or try to
  report partial pre-failure counters;
- whether `adapter.quality` being optional for `not_started` adapter placeholders
  is acceptable under the contract;
- whether the frontend API validation is strict enough without becoming brittle
  for nonterminal placeholders;
- whether warning-code and routing-hint categories are conservative and
  sanitized;
- whether the unclassified output-gap approach is the correct contract match
  for current adapter behavior;
- whether the unrelated launcher dirty files should remain outside this PR
  scope.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #212.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/212

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Related manual import issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md

Implementation handoff:
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md

Risk tier:
Medium

Review the implementation against the issue, contract, handoff, and diff. Lead
with findings ordered by severity. Verify that this remains a reporting-only
quality breakdown for manual legacy JSONL imports.

Pay special attention to:
- `LegacyJsonlAdapterResult.quality`
- blank-line, duplicate raw-hash, unsupported-kind, processed-kind, warning-code,
  ingest-warning, and output-gap counters
- conservative routing hints
- failed adapter quality shape
- manual import response propagation under `adapter.quality`
- frontend type/API validation and Manual Import display
- privacy boundaries: no raw payloads, raw paths, raw hashes, stack traces,
  secrets, webhook URLs, API keys, private local JSONL, generated SQLite files,
  runtime artifacts, failed posts, workbook exports, or generated card data
- absence of parser/replay/ingest/schema/workbook/webhook/App Script/Sheets/
  Match Journal/OpenAI/AI/coaching/Line Tracer/production/destructive behavior
  changes
- unrelated pre-existing launcher dirt that should stay outside this module

Do not modify code in review mode. If findings are concrete, route to Codex D.
If the contract is ambiguous or wrong, route to Codex B. If clean, recommend
Codex F.

Suggested validation:
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run path-scoped protected-surface and secret/private-marker scans over:
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/import_jobs.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_manual_jsonl_import.py
- frontend/src/App.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/src/api.test.ts

Final report should include findings, contract matches, contract mismatches,
missing tests, validation run, protected-surface status, secret/private-marker
status, generated artifact status, and routing recommendation.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/212"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_manual_import_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md"
  target_artifact: "docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> 9 passed"
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py -> 12 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_local_app_backend.py -> 35 passed, 1 warning"
    - "npm --prefix frontend ci -> passed, 0 vulnerabilities"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 18 passed"
    - "npm --prefix frontend run build -> passed on rerun after npm ci completed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "py tools\\check_secret_patterns.py --all -> failed with pre-existing repository-wide findings outside touched slice"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/Line Tracer/production behavior."
    - "Do not change saved-event replay semantics or dedupe scope."
    - "Do not change analytics SQLite schema or migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose raw payloads, raw paths, raw hashes, stack traces, or destructive import/database/job actions."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
