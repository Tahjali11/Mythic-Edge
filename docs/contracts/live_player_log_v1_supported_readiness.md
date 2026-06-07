# Live Player.log V1 Supported Readiness Contract

## Module

`live_player_log_v1_supported_readiness`

Plain English: this contract defines what Mythic Edge may claim when it says
Live Player.log Mode is supported for the private-local-v1 release profile. It
does not add live capture behavior. It binds the already-completed live status,
watcher safeguard, SQLite capture, diagnostics, and operator-documentation
surfaces into a release-readiness decision.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/275
- Engineering maturity / release readiness tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/136
- Analytics/local app tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/204
- Local app umbrella issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/207
- Operator guide issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/274
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue `#275`
- GitHub issues `#136`, `#204`, `#207`, `#240`, `#242`, `#244`,
  `#246`, and `#274`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/contract_test_reports/live_app_player_log_path_watcher_status.md`
- `docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contract_test_reports/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contract_test_reports/live_app_watcher_diagnostics.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- Related backend, frontend, live status, live ingest, tailer, parser
  diagnostics, and evidence-runtime tests.

## Owning Layer

Primary owning layer: Local App / Live Player.log Mode release readiness.

Supporting layers:

- Parser and state interpretation.
- Analytics / SQLite local storage.
- Player.log evidence and diagnostics.
- Quality / Governance release readiness.
- Operator documentation.

## Internal Project Area

Local App / Live Player.log Mode.

This is bridge-code governance across:

- Local App / UI
- Parser
- Analytics
- Corpus / Provenance / evidence diagnostics
- Quality / Governance
- Operator documentation

## Truth Owner

Truth ownership remains unchanged:

- MTGA `Player.log` is the raw observable evidence source.
- Parser/state owns event interpretation and parser-managed match/game facts.
- SQLite stores approved parser-normalized facts and provenance as downstream
  local storage.
- Local app backend owns status and diagnostics composition only.
- Frontend owns read-only display and redaction only.
- Operator docs explain support boundaries only.

This contract does not make UI state, watcher state, SQLite state, diagnostics,
operator docs, workbook formulas, Google Sheets, Apps Script, OpenAI output, or
AI analysis into parser truth.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
Player.log metadata/status, watcher safeguards, live ingest status,
and sanitized diagnostics
  -> local app backend status responses
  -> frontend read-only display
  -> operator readiness documentation and release report
```

Allowed fact flow:

```text
parser-owned final/reconciled match/game facts
  -> approved live ingest boundary
  -> local SQLite analytics database
```

Forbidden reverse flow:

- SQLite must not reinterpret or rewrite parser-owned facts.
- Frontend display must not change parser behavior.
- Diagnostics must not infer hidden game truth.
- Operator docs must not overclaim unsupported production, workbook, AI, or
  coaching behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/live_player_log_v1_supported_readiness.md`

A later readiness/report pass may own:

- `docs/contract_test_reports/live_player_log_v1_supported_readiness.md`

If a later comparison-only implementation handoff is needed, it may own:

- `docs/implementation_handoffs/live_player_log_v1_supported_readiness_comparison.md`

## Public Interface

The release-readiness decision depends on these existing public surfaces:

- `GET /api/live/player-log/status`
- `GET /api/live/watcher/status`
- `GET /api/live/watcher/process`
- `GET /api/live/watcher/diagnostics`
- `GET /api/live/ingest/status`
- `GET /api/app/setup-status`
- `ingest_live_parser_owned_facts(...)`
- frontend Live Player.log, Live Watcher, Live Watcher Process, Live
  Diagnostics, and setup/status panels
- private-local-v1 setup and operator documentation surfaces

This contract does not authorize new write routes, start/stop routes, arbitrary
SQL routes, destructive UI controls, new migrations, or production transport.

## V1.0 Support Definition

Live Player.log Mode is `supported` for `private_local_v1` only when all of the
following are true:

1. The local app can show Player.log readiness using metadata/status only.
2. The local app can show watcher readiness and process-safeguard state without
   starting, stopping, or controlling a watcher from unsupported routes.
3. Duplicate or misleading watcher state is blocked, degraded, or clearly
   labeled instead of silently trusted.
4. Live SQLite capture is limited to approved parser-owned final/reconciled
   match/game facts through the #244 boundary.
5. Live ingest rejects raw/private payload markers and reports skipped,
   deferred, malformed, or unsupported fact families without storing unsafe
   data.
6. Live diagnostics can report missing, unreadable, stale, stopped, blocked,
   crashed, degraded, rotation/truncation/duplication-related, skipped, and
   malformed states through safe labels and counters.
7. Frontend display keeps status, readiness, diagnostics, and support claims
   visible without exposing unsafe values.
8. Operator documentation explains what is supported, what is degraded, what is
   deferred, and what is not claimed.
9. Validation proves backend, frontend, SQLite capture, diagnostics, privacy,
   and generated-artifact boundaries.
10. A privacy-safe real/private Player.log readiness smoke has been completed
    before the final v1.0 support claim, or the readiness report explicitly
    blocks the final support claim until that smoke is completed.

This support claim is limited to the private local Windows release profile. It
is not a public release, production, cloud, Google Sheets, deployed Apps Script,
OpenAI/AI coaching, Line Tracer, hidden-card inference, archetype inference,
player-mistake labeling, or best-line advice claim.

## Completed Surfaces Recognized

### Issue #240: Player.log Path And Watcher Status Surface

Recognized completed support:

- metadata-only Player.log path/readiness status;
- read-only watcher readiness status;
- symbolic display values instead of private absolute paths;
- no raw Player.log content reads;
- no watcher start/stop/tail behavior.

### Issue #242: Watcher Process-Control Safeguards

Recognized completed support:

- `GET /api/live/watcher/process`;
- single-instance and process-control readiness vocabulary;
- fail-closed process preconditions;
- start/stop UI and backend controls remain unauthorized;
- stale or malformed watcher state is reported, not repaired.

### Issue #244: Live Parser-Owned Fact Capture Into SQLite

Recognized completed support:

- `ingest_live_parser_owned_facts(...)`;
- source kind `live_parser`;
- parser-owned final/reconciled match/game fact writes only;
- deterministic upsert/idempotency behavior;
- raw/private marker rejection;
- warnings/skipped counts for deferred fact families;
- read-only `GET /api/live/ingest/status`.

### Issue #246: Live Watcher Diagnostics

Recognized completed support:

- `GET /api/live/watcher/diagnostics`;
- safe composition of Player.log, watcher, process, and ingest status;
- privacy and capability booleans;
- read-only frontend diagnostics display;
- no raw-log generation from diagnostics GET routes.

### Private-Local-V1 Release-Polish Context

Recognized supporting release work:

- private-local-v1 install mechanics have been exercised by prior proof work;
- package-footprint and release-ref expectations are documented;
- operator README/launch guide work is the correct place to explain live-mode
  support boundaries to the user.

## Missing Or Blocking Evidence

The final support claim is not complete until a later readiness report proves:

- current branch includes the completed live slices intended for v1.0;
- backend live routes return compatible safe response shapes;
- frontend live panels render safe status and degraded states;
- live ingest still writes only parser-owned final/reconciled match/game facts;
- raw/private payload markers are rejected before SQLite writes;
- diagnostics remain read-only and do not generate raw-log reports;
- generated/local artifacts are absent from the final diff;
- operator guide language explains support boundaries and non-claims;
- a real/private Player.log readiness smoke was performed safely, or the final
  support claim is explicitly blocked until that proof exists.

The readiness report must not use passing implementation tests alone as proof
that a real private Player.log environment has been validated.

## Real/Private Player.log Smoke Requirement

A privacy-safe real/private Player.log readiness smoke is required before
Mythic Edge may make a final private-local-v1 support claim for Live Player.log
Mode.

The smoke must be performed only in a later explicitly approved thread. It must
not be performed by this contract-writing thread.

The smoke must:

- use existing supported local app status and diagnostics surfaces;
- avoid copying, printing, committing, uploading, hashing, or storing raw
  Player.log content;
- avoid storing raw private paths or raw hashes in reports;
- record only safe labels, booleans, counters, symbolic path classifications,
  route names, command names, pass/degraded/fail results, and redacted
  screenshots if screenshots are needed;
- verify that missing, stale, stopped, blocked, degraded, or ready states are
  reported honestly;
- verify that no generated/private artifacts are staged or committed;
- stop immediately if a route, UI panel, log, report, screenshot, or terminal
  output exposes unsafe private content.

The smoke does not need to prove Google Sheets, deployed Apps Script,
production transport, AI/coaching, Line Tracer, hidden-card inference,
archetype inference, player-mistake labeling, or best-line advice.

If actual live capture from a real private Arena session cannot be safely
proven before v1.0, the readiness report must say so directly and classify the
support claim as blocked or limited to implementation-readiness rather than
operator-proven support.

## Acceptable Degraded States

These states may be acceptable for private-local-v1 support when they are
clearly surfaced and do not hide uncertainty:

- Player.log path is `not_configured`.
- MTGA/Arena is not currently running.
- Player.log is missing until configured.
- Player.log metadata is stale before a new Arena session.
- Watcher is intentionally `stopped`.
- Watcher state is absent in a clean app-data root.
- SQLite analytics history is empty before imports or live captures.
- Diagnostics contain warnings while capture remains safe.
- Deferred fact families are reported as `deferred` or `unsupported`.
- Unknown evidence remains labeled `unknown`, not inferred.

Acceptable degradation must still preserve privacy and parser truth ownership.

## Blocking Conditions

The support claim is blocked if any of these are true:

- Player.log readiness cannot be detected or configured through supported
  local-app surfaces.
- Watcher/process safeguards cannot prevent duplicate or misleading watcher
  state.
- Live parser-owned final/reconciled match/game facts cannot be written
  idempotently through the approved live ingest boundary.
- Raw Player.log content, raw log lines, raw private paths, raw hashes, secrets,
  environment values, local-only artifacts, or generated database contents are
  stored in SQLite, exposed through APIs, rendered in UI, printed in reports,
  included in screenshots, or committed.
- Diagnostics cannot report blocked/degraded/stale/malformed/skipped states
  without unsafe data exposure.
- Frontend display hides degraded states or converts unknown/deferred states
  into certainty.
- Operator docs imply unsupported public, production, Google Sheets, deployed
  Apps Script, OpenAI/AI coaching, Line Tracer, hidden-card, archetype,
  player-mistake, or best-line support.
- Required backend, frontend, live ingest, diagnostics, protected-surface, or
  private-marker validation fails.
- The required real/private Player.log smoke is not completed before the final
  v1.0 support claim.

## Canonical Status Vocabulary

Release-level status labels:

- `supported`: all required proof exists for the private-local-v1 support claim.
- `ready`: configured and safe for the current local app state.
- `ok`: current status has no warning or blocker.
- `degraded`: usable and safe, but uncertainty or review warnings exist.
- `blocked`: cannot proceed safely.
- `unsupported`: not part of the v1.0 support claim.
- `deferred`: intentionally outside this v1.0 slice or a later issue.

Runtime/status labels:

- `running`: a supported status source reports watcher/capture activity.
- `stopped`: intentionally not running.
- `stale`: status metadata is older than the accepted freshness window.
- `crashed`: app-owned state reports a crash or terminated watcher state.
- `unknown`: the app cannot classify the state safely.
- `unavailable`: the dependency or status source is unavailable.
- `not_configured`: required configuration is absent.

Status rules:

- `blocked` outranks all other labels.
- `degraded` outranks `ok`.
- `unknown` must not be upgraded to `ready` without direct supported evidence.
- `running` must not imply parser truth, capture success, or game correctness.
- `supported` is a release-report verdict, not a live route status by itself.

## Canonical Diagnostic Vocabulary

Approved diagnostic labels:

- `player_log_missing`
- `player_log_unreadable`
- `watcher_not_configured`
- `watcher_running`
- `watcher_stopped`
- `duplicate_watcher_blocked`
- `capture_blocked`
- `sqlite_capture_ok`
- `raw_payload_rejected`
- `rotation_detected`
- `truncation_detected`
- `duplicate_event_suspected`
- `event_skipped`
- `malformed_entry`
- `degraded_evidence`
- `watcher_stale`
- `watcher_crashed`
- `drift_detected`

Diagnostic rules:

- Confirmed labels require supported evidence.
- Suspected labels must include `suspected`, `degraded`, `unknown`, or an
  equivalent uncertainty marker.
- Deferred labels must remain `deferred` or `unsupported`; they must not be
  converted into confirmed runtime observations.
- Diagnostic entries must remain labels, counters, booleans, and safe messages.

## Backend Contract

Backend readiness requires:

- all existing live GET routes remain read-only and loopback/local-app scoped;
- route response shapes remain compatible with current frontend validators;
- diagnostics fail closed on malformed or unsafe source payloads;
- process state is reported without repair, cleanup, or process control;
- live ingest status is visible without writing from GET routes;
- live capture writes only through `ingest_live_parser_owned_facts(...)`;
- raw/private payload markers are rejected before SQLite writes;
- no raw Player.log content, raw private paths, raw hashes, stack traces, SQL
  text, secrets, or environment values are returned.

Backend readiness does not authorize:

- watcher start/stop/restart routes;
- parser runner startup from the local app;
- tailer polling from status GET routes;
- analytics schema or migration changes;
- new persistence for diagnostics;
- external workbook/webhook/App Script transport.

## Frontend Contract

Frontend readiness requires:

- Live Player.log, Watcher, Watcher Process, and Diagnostics panels render safe
  status/degraded states;
- unsupported or malformed live payloads fail closed;
- unsafe values are redacted or rejected;
- status labels make `ready`, `stopped`, `blocked`, `degraded`, `unknown`, and
  `unsupported` visibly distinct;
- no destructive or process-control UI is exposed unless a later contract
  authorizes it.

Frontend readiness does not authorize:

- arbitrary SQL or database browsing;
- raw Player.log display;
- raw path/hash display;
- coaching, hidden-card inference, archetype inference, player-mistake labels,
  or best-line advice.

## SQLite And Analytics Contract

SQLite readiness requires:

- live writes use the #244 source kind and entrypoint;
- accepted live rows are parser-owned final/reconciled match/game facts;
- deterministic IDs and upserts remain idempotent;
- replay/manual import semantics remain unchanged;
- skipped/deferred rows are reported as warnings or skipped counts;
- raw Player.log payloads, raw log lines, raw saved-event lines, raw private
  paths, raw private hashes, secrets, workbook exports, and local-only artifacts
  are not stored.

SQLite readiness does not authorize:

- new schema tables or migrations;
- provisional live fact writes;
- live gameplay-action writes;
- live opponent-observation writes;
- live field-evidence writes;
- raw evidence storage;
- analytics truth over parser truth.

## Operator Documentation Contract

Issue #274 or a follow-up operator-docs slice must explain:

- Mythic Edge private-local-v1 includes Live Player.log Mode as a private local
  feature when readiness proof passes;
- Live mode reads status and captures approved parser-owned facts locally;
- missing/stale/stopped/degraded states are normal and must be interpreted as
  readiness/status labels, not game truth;
- SQLite stores approved parser-normalized facts, not raw Player.log content;
- no public, production, Google Sheets, deployed Apps Script, OpenAI/AI
  coaching, Line Tracer, hidden-card, archetype, player-mistake, or best-line
  support is claimed;
- users should stop and report a bug if raw private content appears in the UI,
  logs, reports, screenshots, or Git diffs.

The operator guide must not instruct users to paste raw Player.log content into
GitHub issues, PRs, chat, reports, screenshots, or docs.

## Error Behavior

Malformed status payload:

- fail closed;
- report `unknown` or `blocked`;
- do not echo unsafe source payload values.

Missing Player.log:

- report `not_configured`, `unavailable`, or `player_log_missing`;
- do not infer watcher/capture success.

Stale watcher/process state:

- report `stale`, `watcher_stale`, or `degraded`;
- do not repair, delete, or overwrite state files.

Unsafe payload or marker:

- reject before persistence;
- report `raw_payload_rejected` or equivalent safe error;
- do not include the unsafe value.

Validation failure:

- classify support as blocked until the failure is fixed or explicitly
  accepted as a documented non-blocking risk.

## Side Effects

This contract-writing thread may write only:

- `docs/contracts/live_player_log_v1_supported_readiness.md`

A later readiness/report thread may write only:

- `docs/contract_test_reports/live_player_log_v1_supported_readiness.md`

This contract does not authorize runtime files, SQLite files, WAL/SHM/journal
files, frontend build output, local app state, raw logs, private inputs,
transport-failure artifacts, workbook exports, secrets, credentials, tokens, or
local-only artifacts as committed files.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema or migrations;
- manual JSONL import semantics;
- replay ingest semantics;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, environment variables, API keys, tokens, webhook URLs,
  spreadsheet IDs, deployment IDs, or credential policy.

## Validation Requirements

A later readiness/report thread should run:

```powershell
git status --short --branch --untracked-files=all
gh issue view 275
gh issue view 136
gh issue view 204
gh issue view 207
gh issue view 240
gh issue view 242
gh issue view 244
gh issue view 246
gh issue view 274
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
git diff --check
```

If `npm --prefix frontend run build` creates `frontend/dist`, the report thread
must remove generated build output before final handoff unless a later contract
explicitly authorizes committing it.

The real/private Player.log readiness smoke must be a separate explicitly
approved step in the report thread or a follow-up issue. It must use only safe
labels, booleans, counters, symbolic path classifications, command names,
route names, and pass/degraded/fail results.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/live_player_log_v1_supported_readiness.md`.
- Contract defines the private-local-v1 support claim and non-claims.
- Contract recognizes completed live surfaces from #240, #242, #244, and #246.
- Contract defines missing/blocking evidence and acceptable degraded states.
- Contract defines canonical status and diagnostic vocabulary.
- Contract defines backend, frontend, SQLite, and operator-doc boundaries.
- Contract requires a privacy-safe real/private Player.log readiness smoke
  before the final v1.0 support claim.
- Contract preserves parser truth ownership and protected surfaces.
- Contract routes next to a readiness/report pass unless a concrete
  implementation blocker is found.

## Next Workflow Action

Next role: Codex E: Module Reviewer / release readiness report.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / release readiness report for issue #275.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/275

Trackers / related issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/136
- https://github.com/Tahjali11/Mythic-Edge/issues/204
- https://github.com/Tahjali11/Mythic-Edge/issues/207
- https://github.com/Tahjali11/Mythic-Edge/issues/274
- completed live issues #240, #242, #244, and #246

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_player_log_v1_supported_readiness.md

Goal:
Produce docs/contract_test_reports/live_player_log_v1_supported_readiness.md. Evaluate whether Live Player.log Mode is ready to be claimed as a private-local-v1 supported feature, and identify any blockers, acceptable degraded states, or required follow-up.

Do:
- Confirm branch and git status.
- Review the issue, contract, completed live contracts/reports, backend live routes, live ingest helper, frontend live panels, operator-doc issue context, and validation results.
- Verify completed surfaces from #240/#242/#244/#246 are present.
- Verify status/diagnostic vocabulary is safe and coherent.
- Verify raw/private data is not exposed, stored, printed, or committed.
- Decide one of: supported, supported_with_acceptable_degradation, blocked_pending_real_private_smoke, blocked_pending_implementation, or blocked_pending_docs.
- Produce the readiness report artifact.

Real/private Player.log smoke:
- Do not perform it unless this thread has explicit user approval.
- If approved, use only existing supported status/diagnostics surfaces.
- Do not copy, print, hash, store, upload, screenshot, or commit raw Player.log content or private/local artifacts.
- Record only safe labels, booleans, counters, symbolic path classifications, route names, command names, and pass/degraded/fail results.
- Stop immediately if unsafe content appears.

Do not:
- Implement code.
- Target main.
- Start/stop watcher processes unless explicitly approved and already supported by prior contracts.
- Read, copy, print, store, hash, upload, or commit raw Player.log content, private JSONL artifacts, generated SQLite files, runtime logs, app-data files, transport-failure artifacts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, manual import semantics, replay ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.

Validation:
git status --short --branch --untracked-files=all
gh issue view 275
gh issue view 136
gh issue view 204
gh issue view 207
gh issue view 240
gh issue view 242
gh issue view 244
gh issue view 246
gh issue view 274
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
git diff --check

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- report artifact produced
- completed surfaces verified
- missing/blocking evidence
- acceptable degraded states
- readiness verdict
- whether real/private Player.log smoke was performed or remains required
- validation run
- generated/private artifact status
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/275"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  operator_guide_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/274"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue problem representation for Live Player.log v1 support readiness"
  contract_artifact: "docs/contracts/live_player_log_v1_supported_readiness.md"
  target_artifact: "docs/contract_test_reports/live_player_log_v1_supported_readiness.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/live_player_log_v1_supported_readiness.md"
    - "path-scoped secret/private-marker scan for docs/contracts/live_player_log_v1_supported_readiness.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not overclaim public release, production, Google Sheets, deployed Apps Script, OpenAI/AI coaching, Line Tracer, hidden-card/archetype/player-mistake/best-line support."
    - "Do not read, copy, print, store, hash, upload, or commit raw Player.log content or private/local artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
