# Analytics App Frontend IA Layout Polish Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

Issue #299 is closed for the broader reviewed frontend information-architecture package. This handoff covers later focused layout-polish follow-ups on #299: compact left rail, stable active nav state, aligned dashboard status badges, and dashboard density.

## Tracker

N/A.

## Contract

`docs/contracts/analytics_app_frontend_information_architecture.md`

Additional source authority: the latest #299 focused frontend layout polish comment.

## Internal Project Area

Local App / UI.

## Truth Owner

The frontend owns route display state, layout hierarchy, and visual badge placement. Parser, analytics, live capture, Match Journal, workbook/webhook, Apps Script, Sheets, OpenAI/AI, and production surfaces remain unchanged.

## Bridge-Code Status

`bridge_code`

This slice only changes the frontend display bridge over existing backend/API data. It does not change backend payloads, parser truth, analytics truth, or local app runtime behavior.

## Role Performed

Codex C: Module Implementer / focused frontend-only layout polish.

## Current Behavior Compared To Source

Current repo behavior before this pass:

- `RAIL_ITEMS` contained Dashboard, Coach, Analytics, Review, Feedback, Import, and Diagnostics.
- Privacy was rendered separately in `.leftRailFooter`.
- `.leftRail` used a grid with `auto 1fr auto`, visually splitting the nav cluster and footer.
- Active rail links rendered a visible `Current` pill through `.navCurrentMarker`, changing the active item shape.
- Dashboard status badges in cockpit, insight, and trust cards did not share one stable alignment model.
- The dashboard header rendered a top-right status badge.
- The default dashboard status row rendered five cards: App connection, Player.log monitor, Live capture, Analytics database, and Data trust.
- The five-card row made the first screen feel crowded and increased the risk of title/badge overlap or awkward text wrapping.

Focused source expectation:

- Group Dashboard, Coach, Analytics, Review, Feedback, Import, Diagnostics, and Privacy near the top under `Local App`.
- Remove the `Current` pill.
- Preserve hash route behavior and `aria-current`.
- Use a compact green active indicator without changing item size or structure.
- Keep rail dimensions stable across active and inactive states.
- Align dashboard status badges consistently across cards.
- Remove the dashboard header status badge.
- Reduce the dashboard status row from five cards to three.
- Keep only App connection, Live capture, and Analytics database as the default dashboard status tiles.
- Move Player.log monitor detail out of the permanent dashboard status row; existing Diagnostics access remains.
- Move Data trust out of the permanent dashboard status row; existing Privacy/trust access remains.
- Use compact short tile copy and pin each tile badge bottom-left without title overlap.

## Implementation Option Chosen

Frontend-only layout polish:

- Move Privacy into the primary rail item list.
- Keep Settings metadata in the footer, but no longer use the footer to split the navigation group.
- Remove the active `Current` marker DOM.
- Use a CSS pseudo-element for the active green dot.
- Change the rail layout from a three-row grid to a compact flex column.
- Align cockpit rail, decision-support, and trust card status pills with CSS grid placement.
- Add focused frontend assertions for primary-nav Privacy and absence of `Current`.
- Remove the dashboard header status badge.
- Reduce `buildCockpitStatusItems` to App connection, Live capture, and Analytics database.
- Replace long dashboard tile explanations with short truthful sentences.
- Restyle the cockpit status row as compact, stable tiles with bottom-left status badges.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md`

## Code Changed

Yes, frontend-only.

### `frontend/src/App.tsx`

- Added `{ route: "privacy", label: "Privacy" }` to `RAIL_ITEMS`.
- Removed the separate footer Privacy `RailLink`.
- Removed the active `Current` marker from `RailLink`.
- Removed the dashboard header `StatusPill`.
- Reduced the default dashboard status row to App connection, Live capture, and Analytics database.
- Removed Player.log monitor and Data trust from the permanent dashboard status-card row.
- Added compact live-capture status sentence selection for dashboard tiles.

### `frontend/src/App.css`

- Changed `.leftRail` from grid rows to a compact flex column.
- Reduced rail spacing and kept footer metadata close to the nav group.
- Gave rail links stable min-height, padding, and alignment.
- Replaced `.navCurrentMarker` with an active `::before` green dot.
- Aligned `.cockpitRailItem` status pills in a third grid column.
- Set `.panelHeader` to a two-column grid so badge position is stable.
- Set `.cockpitInsight` and `.trustItem` to grid content flow for consistent card alignment.
- Tightened `.statusPill` alignment with centered inline-flex layout.
- Compacted the dashboard header.
- Changed `.cockpitRail` to responsive compact tiles.
- Reworked `.cockpitRailItem` so the icon/title sit at the top, the short sentence follows, and the badge anchors bottom-left.

### `frontend/src/App.test.tsx`

- Scoped the rail-link assertions to the `Primary sections` nav.
- Asserted Privacy is part of the primary nav.
- Asserted the `Current` pill text is absent.
- Asserted the dashboard header no longer renders a `Needs review` status badge.
- Asserted the dashboard status row renders exactly three cards.
- Asserted Player.log monitor and Data trust are not default dashboard status cards.
- Updated live-capture dashboard tile assertions for the new compact copy.

## Tests Changed

Yes, focused frontend test coverage changed in `frontend/src/App.test.tsx`.

## Interface Changes

None.

No backend routes, API response schemas, parser behavior, analytics schema, SQLite ingest, GitHub submission, AI/coaching behavior, workbook/webhook shape, Apps Script, Sheets, or production behavior changed.

## Validation Run

```powershell
npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run
# 3 test files passed; 86 tests passed

npm --prefix frontend run typecheck
# passed after dashboard density updates

npm --prefix frontend run test -- --run
# 3 test files passed; 86 tests passed after dashboard density updates

npm --prefix frontend run build
# passed; Vite built frontend/dist

Remove generated build output
# frontend/dist removed

git diff --check
# passed

py tools/check_agent_docs.py
# passed; errors 0, warnings 0

@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; forbidden 0, warnings 0

@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; forbidden 0, warnings 0

Browser smoke against temporary Vite server on http://127.0.0.1:5174/#dashboard
# rail smoke passed: all 8 primary links visible, equal 38px height, active aria-current=page, active dot 7px by 7px, no Current text
# full dashboard badge visual smoke not completed because backend was unavailable in the temporary frontend-only smoke
```

## Protected-Surface Status

Clean. The path-scoped protected-surface scan over changed files passed with forbidden 0 and warnings 0. The changed implementation files are frontend display/test files plus this handoff. No protected parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/production surfaces were edited.

## Secret/Private-Marker Status

Clean. The path-scoped secret/private-marker scan over changed files passed with forbidden 0 and warnings 0. No raw Player.log content, raw JSONL payloads, private paths, raw hashes, secrets, endpoint values, generated SQLite files, runtime artifacts, workbook exports, or local-only artifacts were added.

## Generated Artifact Status

`npm --prefix frontend run build` generated `frontend/dist`; it was removed before handoff.

## Still Unverified

- Full-data live rendered dashboard badge alignment, because the temporary frontend-only browser smoke showed backend unavailable.
- Exact no-scroll fit on the user's monitor, because no live screenshot with backend data was available in this pass.
- CSS visual alignment is covered by source review, tests, build, and partial browser smoke; a live rendered screenshot with backend mock or backend data remains the best final confirmation.

## Reviewer Focus

Codex E should check:

- Privacy is in the compact primary rail group.
- The `Current` pill is gone.
- Active rail state remains visible, compact, and retains `aria-current`.
- Rail item dimensions do not change between active and inactive routes.
- The dashboard header status badge is gone.
- The dashboard status row has only App connection, Live capture, and Analytics database.
- Player.log monitor and Data trust are no longer permanent dashboard status cards.
- Dashboard status tile badges are pinned bottom-left and do not overlap titles.
- No backend/API/parser/analytics/AI/workbook/production behavior changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #299 focused layout polish.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/299

Contract:
docs/contracts/analytics_app_frontend_information_architecture.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md

Branch:
codex/analytics-foundation

Review focus:
- Compare the diff against the latest #299 focused frontend layout polish comment.
- Verify Dashboard, Coach, Analytics, Review, Feedback, Import, Diagnostics, and Privacy are grouped compactly near the top under Local App.
- Verify the active Current pill was removed.
- Verify active route state remains stable, compact, visible, and preserves aria-current.
- Verify rail dimensions do not change between active and inactive items.
- Verify dashboard status badges align consistently across cockpit, decision-support, and trust cards.
- Verify the Dashboard header no longer renders a top-right status badge.
- Verify the default Dashboard status row contains exactly App connection, Live capture, and Analytics database.
- Verify Player.log monitor and Data trust are not permanent Dashboard status cards.
- Verify the remaining Dashboard status tiles use short copy and badge placement that avoids clipping, title overlap, and vertical word-column wrapping.
- Verify Settings/footer metadata does not split the primary navigation group.
- Verify no backend routes, API payloads, parser behavior, analytics schema/ingest, GitHub submission, AI/coaching behavior, workbook/webhook/App Script/Sheets behavior, or production behavior changed.

Validation to run:
- git status --short --branch --untracked-files=all
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files
- browser/screenshot smoke if feasible

If npm build creates frontend/dist, remove generated build output before final handoff unless explicitly authorized.

Final output:
- findings first, ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- browser/manual smoke status
- verdict
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "latest #299 focused frontend layout polish comment"
  contract_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md"
  focused_slice: "compact left rail, stable active nav state, aligned dashboard status badges"
  follow_up_slice: "dashboard density: three top status tiles, no header badge, compact tile copy"
  risk_tier: "Low-to-medium frontend-only"
  branch: "codex/analytics-foundation"
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 3 files passed, 86 tests passed"
    - "npm --prefix frontend run typecheck after density updates -> passed"
    - "npm --prefix frontend run test -- --run after density updates -> 3 files passed, 86 tests passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over changed files -> passed"
    - "path-scoped secret/private-marker scan over changed files -> passed"
    - "browser smoke on temporary http://127.0.0.1:5174/#dashboard -> rail passed; full-data badge visual smoke unverified because backend unavailable"
  stop_conditions:
    - "Do not target main."
    - "Do not change backend routes or API payloads."
    - "Do not change parser/runtime/analytics schema/SQLite ingest/GitHub submission/OpenAI/AI/coaching/workbook/webhook/App Script/Sheets/production behavior."
```
