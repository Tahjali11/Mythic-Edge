# Analytics App Frontend IA Layout Polish Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

## Tracker

N/A.

## Contract

`docs/contracts/analytics_app_frontend_information_architecture.md`

## Review Artifact

`docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

## Source Finding

- CT-299-REFINE-001 P1: Dashboard exposes a live capture Start capture process-control button from a #299 display-polish slice.
- CT-299-REFINE-002 P2: Default Dashboard no longer shows the contract-required compact trust/privacy signal.

## Fault Category

Implementation drift inside a frontend-only display-polish slice.

The prior implementation moved a live-capture process-control action into the default Dashboard tile and hid the compact trust/privacy signal behind Privacy or technical details. The contract keeps #299 as frontend information architecture only: Dashboard may display compact live capture state, but live capture start/stop controls belong to the owning control surface from the separate #297 contract.

## Fix Produced

- Removed the Dashboard Live capture tile Start capture button and its `onStartCapture` wiring from `CockpitStatusRail`.
- Kept the explicit Start/Stop capture controls on the Diagnostics-owned `LiveCaptureControlPanel`.
- Restored a compact default Dashboard `Trust and Freshness` signal with Freshness, Data Quality, and Privacy status pills.
- Kept full trust/privacy details under the Privacy route and the expandable technical details view.
- Removed now-unused Dashboard tile action CSS.
- Updated focused frontend tests so Dashboard is display-only for live capture and shows the compact trust/privacy signal by default.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_fixer.md`

Unrelated dirty or untracked files observed and left untouched:

- `docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `frontend/src/api.test.ts`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_stream_unit.py`

## Code Changed

Yes, frontend-only.

No backend route shapes, parser behavior, analytics schema/ingest, live watcher backend behavior, Match Journal backend behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, production behavior, secrets, raw logs, runtime artifacts, generated data, or local app data were changed.

## Tests Changed

- `frontend/src/App.test.tsx` now asserts the default Dashboard Live capture tile has no Start/Stop controls.
- `frontend/src/App.test.tsx` now asserts the default Dashboard renders the compact `Trust and Freshness` signal.
- The live capture start test now routes to Diagnostics before asserting the authorized explicit backend control.

## Validation Evidence

```powershell
npm --prefix frontend test -- --run src/App.test.tsx
# 1 file passed; 50 tests passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend test -- --run
# 3 files passed; 86 tests passed

npm --prefix frontend run build
# passed; frontend/dist removed after build

git diff --check
# passed

py tools\check_agent_docs.py
# passed; errors 0, warnings 0

Browser DOM smoke against temporary Vite frontends on 5174 and 5175
# attempted; rail loaded and showed no Start capture button, but Dashboard content stayed behind Backend unavailable
# not counted as a Dashboard-content pass
```

## Protected-Surface Status

Path-scoped protected-surface scan over the changed #299 files and this handoff passed with `forbidden: 0` and `warnings: 0`.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over the changed #299 files and this handoff passed with `forbidden: 0` and `warnings: 0`.

## Generated Artifact Status

`npm --prefix frontend run build` generated `frontend/dist`; it was removed. No generated build output was intentionally retained.

## Browser Smoke Status

Browser smoke was attempted but is not counted as a content-level pass. The temporary Vite frontend rendered the shell and primary rail, but Dashboard content stayed behind `Backend unavailable`, so it did not verify the compact Dashboard trust/privacy region in-browser. The 5174/5175 temporary frontend processes were stopped, temp logs were removed, and the disposable app-data root was absent after cleanup.

## Still Unverified

- Browser DOM/visual smoke of the full Dashboard content remains unverified.
- No live backend or real Player.log/capture workflow was exercised, by contract.
- Codex E should confirm layout in browser if visual confidence is required before submission.

## Remaining Review Focus

Codex E should confirm:

- the default Dashboard no longer exposes a Start capture process-control button;
- actual Start/Stop controls remain limited to the explicit Diagnostics live-capture control surface;
- the default Dashboard shows the compact `Trust and Freshness` signal;
- detailed privacy/trust content remains behind Privacy or technical details;
- no backend/API/parser/analytics/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for the latest #299 frontend Dashboard refinement fixes.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/299

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_frontend_information_architecture.md

Review artifact:
docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md

Fixer handoff:
docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_fixer.md

Confirm only:
- CT-299-REFINE-001 P1: Dashboard no longer exposes a live capture Start capture process-control button from the #299 display-polish slice.
- CT-299-REFINE-002 P2: Default Dashboard again shows a compact trust/privacy signal.

Do not stage, commit, push, open a PR, merge, close issue #299, target main, start or stop a real watcher, read raw Player.log contents, or broaden scope beyond #299 confirmation.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md"
  findings_fixed:
    - "CT-299-REFINE-001 P1: Dashboard live capture tile is display-only again; Start capture remains on the explicit Diagnostics control surface."
    - "CT-299-REFINE-002 P2: Default Dashboard shows a compact Trust and Freshness signal again."
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
