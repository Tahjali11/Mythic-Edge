# Analytics App First-Screen Competitive Cockpit Contract

## Module

`analytics_app_first_screen_competitive_cockpit`

Plain English: this contract defines a frontend-first redesign of the local app
first screen. The first screen should feel like a competitive MTGA review
cockpit, not a setup/status console. It should show the player what is useful
now, whether the data is trustworthy enough, and where to inspect diagnostics
when something looks wrong.

This is a contract-writing artifact only. It does not implement UI code,
change backend routes, change analytics queries, change parser behavior, or
alter runtime/live capture behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/278
- Analytics/local app tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/204
- Local app umbrella:
  https://github.com/Tahjali11/Mythic-Edge/issues/207
- Release readiness tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`
- Risk tier: Medium-High

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue `#278`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.test.tsx`

Reference inspiration, not compliance claims:

- Carbon dashboard guidance: hierarchy, focus, and limiting non-essential
  metrics.
- Carbon filtering guidance: task-based filters.
- USWDS alert/status guidance: concise human-readable messages and next steps.
- WCAG 2.2 Use of Color: color must not be the only conveyed meaning.

## Tracker

- Analytics/local app tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/204
- Local app umbrella:
  https://github.com/Tahjali11/Mythic-Edge/issues/207
- Release readiness tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/136

Trackers remain open. This contract does not close them.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting layers:

- Analytics / SQLite local storage.
- Live Player.log status and diagnostics.
- Match Journal.
- Operator documentation.

The frontend owns information architecture, layout, display vocabulary, visual
hierarchy, accessibility, redaction display, and user-facing status
translation. It does not own parser facts, analytics facts, live capture truth,
database truth, Match Journal truth, or release readiness truth.

## Internal Project Area

Local App / UI.

Adjacent areas:

- Analytics.
- Live Player.log Mode.
- Match Journal.
- Quality / Governance release readiness.

## Truth Owner

Truth ownership remains unchanged:

- Parser/state owns match/game facts, event interpretation, final
  reconciliation, parser event classes, match/game identity, and deduplication.
- Analytics/SQLite owns deterministic local storage and query results from
  parser-normalized facts.
- Live Player.log status surfaces own readiness/diagnostic status only.
- Match Journal owns human notes and labels, not parser or analytics truth.
- Frontend owns presentation and status translation only.

The cockpit may summarize, prioritize, group, translate, and display existing
facts. It must not infer hidden cards, classify archetypes as truth, label
player mistakes, provide best-line advice, or convert uncertain evidence into
certainty.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
backend setup/live/analytics/journal payloads
  -> frontend validation/redaction
  -> user-facing cockpit status translation
  -> competitive review modules
  -> diagnostics/details on demand
```

Forbidden reverse flow:

- cockpit display must not rewrite backend payloads;
- cockpit labels must not become parser truth;
- cockpit summaries must not become analytics truth;
- diagnostics details must not leak into committed artifacts;
- UI must not trigger destructive database, file, watcher, Git, Sheets, AI, or
  production operations.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`

Future Codex C may touch, if implementation is authorized:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `frontend/src/api.ts`, only if existing frontend validation/typing needs a
  narrow presentation helper
- `frontend/src/App.test.tsx`
- optional frontend-only helper modules under `frontend/src/` if they reduce
  repeated status translation or cockpit summary logic
- `docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md`

Future Codex C must not touch backend, parser, analytics schema/migrations,
SQLite ingest, live watcher behavior, Match Journal backend behavior, setup
scripts, launcher behavior, workbook/webhook/App Script/Sheets behavior, or
production/AI behavior unless a later contract explicitly authorizes that
scope.

## Observed Current Behavior

Current `frontend/src/App.tsx` first-screen behavior:

- the primary heading is `Setup Status`;
- the first section is a setup/status summary band;
- setup panels appear before competitive analytics value;
- live diagnostics appear before most analytics sections;
- operational panels include App Data, Local Config, Player Log, Live
  Player.log, Live Watcher, Live Watcher Process, Analytics Database, Match
  Journal, Migrations, and Runtime;
- first-screen panel details include internal labels such as `readiness_only`,
  `safeguards_only`, `not_capturing`, `not_running`, `start route`, `stop
  route`, `ui controls`, `state path`, `metadata`, `contents`, and `tailing`;
- analytics and review sections already exist lower in the page: Analytics
  History, Match Journal Cockpit, Early Game History, Action Review, and
  Play/Draw / Game 1/Postboard split review;
- frontend redaction helpers already reject raw paths, URLs, secret-like
  markers, JSON-like strings, and unsafe Player.log strings;
- tests currently assert the setup-console ordering and presence of raw-ish
  operational labels.

Observed gap:

- the local app has useful analytics surfaces, but the first screen asks the
  user to parse implementation state before seeing competitive value.
- internal backend/status vocabulary is visible too early.
- diagnostics are available, but they dominate the first impression rather than
  supporting trust on demand.

## Contract Decision

Issue #278 should authorize a frontend-first information architecture redesign.

Approved first slice:

- make the first screen a competitive decision-support cockpit;
- add a frontend status translation boundary for first-screen labels;
- keep backend payload contracts unchanged unless Codex C finds a narrow
  presentation gap that must route back to Codex B;
- make analytics/review modules the default first-screen emphasis;
- demote setup grids, raw status details, schema/process details, and live
  diagnostics tables behind a details/diagnostics affordance;
- preserve all safe redaction behavior;
- preserve all live Player.log support boundaries from #275;
- preserve all parser and analytics truth boundaries.

Not approved:

- backend route changes;
- analytics schema or query semantics changes;
- parser behavior changes;
- live watcher process-control changes;
- new capture/write behavior;
- destructive controls;
- AI/coaching/Line Tracer/hidden-card/best-line behavior;
- marketing landing-page work.

## First-Screen Goal

Within about 10 seconds, a competitive MTGA player should understand:

1. Mythic Edge is connected, blocked, or needs setup.
2. Player.log and live capture are ready, waiting, degraded, or blocked.
3. Local analytics storage is ready, empty, limited, degraded, or blocked.
4. The most useful review signals are visible without scrolling through
   implementation details.
5. Data trust/freshness is clear enough to decide whether to use the displayed
   signals.
6. Diagnostics and raw setup details are available when requested.

The first screen should optimize for:

1. non-technical competitive MTGA player;
2. owner / power user;
3. developer / debugger.

Developer traceability remains required, but it should use progressive
disclosure instead of default first-screen noise.

## First-Screen Information Architecture

Required first-screen order:

1. Competitive cockpit header.
2. Compact health/status rail.
3. Main competitive insight/review modules.
4. Quiet trust/freshness/privacy layer.
5. Manual import and Match Journal affordances.
6. Diagnostics/details surface after the player-facing cockpit.

The first screen must not begin with `Setup Status` as the primary product
headline after implementation. A diagnostics/details section may still contain
the phrase `Setup Status`.

Recommended heading direction:

- `Mythic Edge Cockpit`
- `Match Review Cockpit`
- `Competitive Review`

The heading must not imply public release, production service, cloud sync, AI
coaching, hidden-card inference, archetype certainty, player-mistake truth, or
best-line advice.

## Compact Health/Status Rail

The top rail should contain a small number of scan-friendly status items:

- App connection.
- Player.log monitor.
- Live capture.
- Analytics database.
- Data trust/freshness.

Optional if space allows:

- Match Journal readiness.
- Import readiness.

Each item must include:

- icon or short visual cue;
- text label;
- user-facing status label;
- tone/color;
- accessible name;
- details affordance or link into diagnostics.

Color must never be the only meaning. If a badge is amber or red, the text must
also say what is wrong or what needs review.

Allowed main rail labels:

- `Connected`
- `Ready`
- `Capturing`
- `Waiting for Arena activity`
- `Setup needed`
- `Needs review`
- `Blocked`
- `Limited data`
- `Empty history`
- `Degraded`
- `Stopped`
- `Unavailable`

Raw backend labels such as `schema_current`, `not_checked`, `deferred`,
`readiness_only`, `safeguards_only`, `not_started`, `not_running`, `state_only`,
`metadata`, `start route`, `stop route`, `ui controls`, and `state path` must
not appear in the default first-screen rail.

## User-Facing Status Translation Boundary

Codex C should add or use a frontend-only translation boundary that maps raw
backend/status labels into player-facing cockpit labels.

Example translations:

- `ok`, `enabled`, `completed`, `present`, `schema_current` -> `Ready` when
  the source contract supports readiness.
- `empty` -> `Empty history` or `Limited data`.
- `not_configured`, `missing`, `*_missing` -> `Setup needed`.
- `stopped`, `not_running`, `not_started` -> `Stopped` or `Waiting`, depending
  on source context.
- `deferred`, `disabled`, `state_only`, `readiness_only`,
  `safeguards_only` -> `Limited` or `Details available`, not `Ready`.
- `stale`, `degraded` -> `Needs review`.
- `blocked`, `failed`, `unreadable`, `crashed`, `rejected` -> `Blocked`.
- unknown or unrecognized values -> `Needs review` or `Unknown`, never
  `Ready`.

Translation rules:

- Raw labels may remain visible in diagnostics/details views.
- Unknown or unsupported states must fail closed.
- Translation must preserve the source tone/severity.
- Translation must not upgrade `deferred`, `unknown`, or `not_checked` into
  confidence.
- Translation must be testable separately from layout.

## Competitive Cockpit Modules

The default first-screen content should use existing approved analytics and
journal surfaces. Codex C should not invent new backend facts.

Required first-screen module families, using current data where available:

- Recent match/game review summary.
- Play/draw split summary.
- Game 1 vs postboard split summary.
- Opening-hand and mulligan signal summary.
- Gameplay action / opponent observation review summary.
- Match Journal needs-review or notes summary.
- Import/live data freshness and data quality summary.

Allowed module headings:

- `Recent Review`
- `Play/Draw Split`
- `Game 1 / Postboard`
- `Opening Hands`
- `Mulligans`
- `Gameplay Review`
- `Opponent Observations`
- `Needs Review`
- `Data Quality`

Allowed decision-support language:

- `observed pattern`
- `high-performing lines`
- `review signal`
- `limited data`
- `needs review`
- `confidence`
- `freshness`

Forbidden first-screen language:

- `best line`
- `correct play`
- `mistake`
- `punt`
- `guaranteed`
- `hidden card`
- `opponent decklist`
- `archetype truth`
- `AI coach`
- `Line Tracer` unless a later contract authorizes that product surface.

## Filters

Filters may be included if they use existing frontend/backend capabilities or
can be represented as a first-slice UI shell without changing backend query
semantics.

Recommended filter vocabulary:

- date range;
- format/queue;
- deck label;
- opponent label;
- play/draw;
- game 1/postboard;
- result;
- confidence/data quality.

First slice rule:

- If backend APIs do not already support a filter, Codex C may show a disabled
  or future placeholder only if it is clearly labeled and does not imply active
  filtering.
- Codex C must route back to Codex B before adding backend filter query
  parameters, SQLite view changes, analytics query changes, or new
  aggregation semantics.

## Trust, Freshness, And Privacy Layer

The first screen should show trust without turning the page back into a
diagnostics console.

Required trust signals:

- data freshness label such as `Updated recently`, `Stale`, or `No recent
  activity`;
- data quality label such as `Good`, `Limited`, `Needs review`, or `Blocked`;
- privacy label or affordance such as `Local only` and `Private values hidden`;
- link or button to diagnostics/details.

Trust rules:

- Freshness must not imply live capture success unless supported by current
  live status evidence.
- Data quality must not imply parser correctness beyond available parser and
  analytics evidence.
- Privacy label must not imply absolute security; it should describe current
  local/redaction behavior.
- Redaction warnings must remain visible when unsafe values were replaced.

## Diagnostics And Setup Details Boundary

Diagnostics/details must remain available for developer and owner workflows.

Demoted from default first-screen content:

- setup grid;
- schema versions;
- migration internals;
- process-control internals;
- raw backend status tables;
- raw status labels;
- state path values;
- UI control flags;
- tailing/content-read flags;
- redaction counts unless redaction occurred;
- UUID-heavy identifiers;
- raw route/object/schema names.

Allowed diagnostics/details affordances:

- `View setup details`
- `View live diagnostics`
- `View debug summary`
- `Show technical details`

Diagnostics/details must not expose raw Player.log content, raw JSONL payloads,
raw private paths, raw hashes, secrets, environment values, arbitrary SQL,
generated SQLite contents, stack traces, transport-failure payloads, workbook
exports, or local-only artifact contents.

## Accessibility Requirements

Codex C must preserve or add:

- semantic headings in a logical order;
- accessible names for status badges and details controls;
- text or icon+text labels for every color-coded state;
- keyboard-accessible details/diagnostics controls;
- no color-only status communication;
- focus states for interactive controls;
- reduced-motion support if any live/capture animation is added;
- responsive layout that works at narrow desktop/mobile widths;
- no text overlap or clipped labels in badges/cards/tables;
- no viewport-width font scaling;
- no negative letter spacing.

Icon use should prefer the project/frontend's existing icon approach if one is
already present. If a new icon library is required, Codex C must route back to
Codex B before adding the dependency.

## Visual Design Requirements

The redesign should feel like a quiet operational cockpit for repeated use,
not a marketing landing page.

Required design direction:

- dense but readable information hierarchy;
- fewer first-screen cards than the current setup grid;
- compact badges for status;
- analytics summaries before diagnostic grids;
- restrained color palette with text labels;
- page sections as unframed layouts or full-width bands;
- individual repeated items may use cards with border radius no larger than
  the existing 8px pattern unless the current design system changes.

Do not:

- create a hero/landing page;
- use decorative gradient/orb backgrounds;
- put cards inside cards;
- let diagnostics dominate the first viewport;
- rely on color alone;
- create marketing copy instead of the usable app screen.

## Backend Contract

No backend changes are authorized by this contract.

Codex C may consume existing backend payloads through existing frontend API
helpers. If Codex C finds that a cockpit module cannot be built safely without
new backend fields, query parameters, endpoints, aggregation semantics, or
status vocabulary, it must stop and route back to Codex B with the gap.

## Frontend Contract

Codex C may:

- reorder existing sections;
- add frontend-only presentation helpers;
- add a cockpit summary layer derived from already validated frontend payloads;
- add accessible status rail components;
- add first-screen data-quality/freshness summaries;
- move setup and diagnostics details behind progressive disclosure;
- update CSS for the new layout;
- update frontend tests to reflect the new first-screen hierarchy.

Codex C must:

- keep current redaction helpers active;
- preserve current route validators;
- preserve current error handling;
- keep manual import, Match Journal, analytics, live status, and diagnostics
  surfaces reachable;
- avoid changing backend contracts;
- avoid changing persistence or runtime behavior.

## Inputs

Allowed inputs:

- validated setup status payloads;
- validated live Player.log status payloads;
- validated live watcher status/process/diagnostics payloads;
- validated live ingest status payloads;
- validated analytics history responses;
- validated early-game history responses;
- validated gameplay action and opponent observation review responses;
- validated play/draw and postboard split responses;
- validated Match Journal responses;
- frontend redaction/safe-display results.

Forbidden inputs:

- raw Player.log content;
- raw log lines;
- raw JSONL payloads;
- raw private paths;
- raw hashes from private artifacts;
- secrets, credentials, tokens, endpoint values, spreadsheet IDs, environment
  values;
- generated SQLite contents outside approved API responses;
- arbitrary SQL results;
- local-only artifact contents.

## Outputs

Allowed outputs:

- frontend cockpit layout;
- user-facing status labels;
- frontend-only summary cards/sections;
- diagnostics/details controls;
- frontend tests;
- implementation handoff.

Forbidden outputs:

- new parser facts;
- new analytics facts;
- raw/private data displays;
- generated database files;
- runtime files;
- frontend build output committed to Git;
- screenshots containing private local data;
- public/production/AI/coaching/Line Tracer claims.

## Invariants

- Parser truth stays upstream.
- Analytics/SQLite truth stays downstream from parser-normalized facts.
- Live Player.log support boundaries from #275 stay visible.
- Privacy redaction stays active.
- Diagnostics stay reachable.
- First-screen labels must be user-facing.
- Raw/internal backend labels must move behind diagnostics/details unless they
  are already safe and player-facing.
- Unknown/deferred/not-checked states must not become `Ready`.
- No destructive controls are introduced.

## Error Behavior

Malformed setup/live/analytics/journal payload:

- keep current fail-closed behavior;
- show a concise user-facing error;
- keep raw details out of the first screen;
- route raw shape diagnostics to details only if safe.

Unsafe display value:

- preserve `<redacted_path>` or equivalent safe fallback behavior;
- show a visible privacy/degraded warning;
- never render the unsafe value.

Unknown status:

- translate to `Needs review`, `Unknown`, or `Limited data`;
- do not translate to `Ready`, `Capturing`, or `Good`.

Unavailable backend:

- show local app unavailable or backend unavailable in the health rail;
- keep analytics modules in a safe unavailable/empty state;
- do not offer destructive recovery controls.

## Side Effects

Codex B may write only:

- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`

Future Codex C may edit frontend source/tests and create an implementation
handoff. It must not create or commit generated frontend build output,
generated SQLite files, local app data, raw logs, private inputs,
transport-failure artifacts, workbook exports, secrets, credentials, tokens,
environment values, or local-only artifacts.

## Dependency Order

Recommended Codex C order:

1. Confirm branch and working tree.
2. Compare current first-screen JSX/tests against this contract.
3. Add or update frontend status translation helpers.
4. Reorder first-screen layout around the cockpit/health rail.
5. Move setup and diagnostics details behind progressive disclosure.
6. Update CSS for responsive cockpit layout.
7. Update frontend tests for first-screen labels, diagnostics demotion,
   translation, redaction, and no destructive controls.
8. Run validation.
9. Produce implementation handoff.

## Compatibility

Must remain compatible:

- existing backend route inventory;
- existing frontend API validators;
- existing safe display/redaction helpers;
- existing analytics history sections;
- existing Match Journal cockpit functionality;
- existing manual import UI behavior;
- existing Live Diagnostics behavior, moved or hidden by default but still
  accessible;
- existing setup/status details, moved or hidden by default but still
  accessible.

Tests that currently assert `Setup Status` as the first primary heading should
be updated because the contract intentionally changes the first-screen
hierarchy. Tests that assert privacy redaction, safe API validation, and absence
of destructive controls must remain or be strengthened.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema, migrations, or ingest semantics;
- backend route shapes;
- live watcher capture semantics;
- live watcher process-control semantics;
- Match Journal backend behavior or truth ownership;
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
- archetype inference as truth;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, tokens, endpoint values, spreadsheet IDs, or
  environment values;
- raw logs, private JSONL artifacts, generated SQLite databases, SQLite sidecar
  files, runtime files, transport-failure artifacts, workbook exports,
  frontend build output, app-data files, generated data, or local-only
  artifacts.

## Tests Required

Codex C must add or update frontend tests proving:

- first primary heading is cockpit/competitive-review oriented, not `Setup
  Status`;
- compact health/status rail appears before setup/diagnostic details;
- analytics/review modules appear before setup grid and live diagnostics table;
- raw backend/internal labels do not appear in the default first-screen view;
- raw backend/internal labels remain available only in diagnostics/details when
  safe;
- unknown/deferred/not-checked statuses are not translated to `Ready`;
- color-coded statuses include text/icon labels;
- unsafe values remain redacted;
- destructive controls remain absent;
- manual import, Match Journal, analytics history, live diagnostics, and setup
  details remain reachable.

Recommended validation:

```powershell
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, Codex C must
remove generated build output before final handoff unless a later contract
explicitly authorizes committing it.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`.
- Contract defines first-screen information architecture.
- Contract defines user-facing status vocabulary and translation rules.
- Contract defines raw-status diagnostics boundary.
- Contract defines compact health/status rail requirements.
- Contract defines competitive analytics cockpit requirements.
- Contract defines trust/freshness/privacy requirements.
- Contract defines accessibility requirements.
- Contract preserves parser truth ownership, analytics truth ownership, live
  Player.log boundaries, privacy redaction, and diagnostic traceability.
- Contract routes next to Codex C with frontend-only implementation scope.

## Open Questions

- Whether the cockpit should use one route's aggregate setup payload as its
  only status source or continue loading separate live/analytics/journal
  payloads in parallel.
- Whether a tab, disclosure, route, or in-page anchor is the best details
  pattern for diagnostics.
- Whether existing CSS should be reorganized during implementation or kept as a
  minimal additive change.
- Whether future backend summaries would be useful after this frontend-first
  slice proves the desired shape.

Codex C may choose conservative answers within frontend-only scope. Backend or
analytics gaps must route back to Codex B.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #278.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/278

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/204
- https://github.com/Tahjali11/Mythic-Edge/issues/207
- https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_first_screen_competitive_cockpit.md

Goal:
Compare the current React local app first screen against the contract and implement the smallest frontend-only redesign that turns the first screen into a competitive decision-support cockpit. Produce docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md.

Before editing:
- Confirm branch and git status.
- Inspect frontend/src/App.tsx, frontend/src/App.css, frontend/src/status.ts, frontend/src/types.ts, frontend/src/api.ts, frontend/src/App.test.tsx, issue #278, and the contract.
- State what the first screen is supposed to communicate, what the current screen does, why the current hierarchy is wrong for private-local-v1 usage, and the minimal frontend-only plan.

Do:
- Make the first primary heading cockpit/competitive-review oriented.
- Add or update frontend-only user-facing status translation.
- Add a compact health/status rail.
- Put competitive analytics/review modules before setup grids and diagnostics tables.
- Keep setup/status and diagnostics reachable through progressive disclosure or a clearly demoted details area.
- Preserve safe display/redaction behavior.
- Preserve route validators and existing backend contracts.
- Update frontend tests for hierarchy, translation, diagnostics demotion, redaction, accessibility, and absence of destructive controls.

Do not:
- Change backend route shapes.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, live watcher capture semantics, live watcher process-control semantics, Match Journal backend behavior/truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference as truth, player-mistake labels, or gameplay advice.
- Expose raw Player.log content, raw JSONL payloads, raw private paths, raw hashes, secrets, credentials, endpoint values, spreadsheet IDs, environment values, arbitrary SQL, generated SQLite contents, runtime files, transport-failure artifacts, workbook exports, frontend build output, app-data files, or local-only artifacts.
- Add destructive controls or arbitrary SQL/database browsing.
- Claim public release or production readiness.
- Target main.

Validation:
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

If npm build creates frontend/dist, remove generated build output before final handoff unless a later contract explicitly authorizes committing it.

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- first-screen hierarchy changed
- status translation changes
- diagnostics/details boundary
- validation run
- generated/private artifact status
- protected-surface status
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/278"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  release_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #278 problem representation"
  contract_artifact: "docs/contracts/analytics_app_first_screen_competitive_cockpit.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/analytics_app_first_screen_competitive_cockpit.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_app_first_screen_competitive_cockpit.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not change backend/parser/analytics schema/live watcher/Match Journal backend/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw Player.log content, raw private paths, raw hashes, secrets, generated SQLite contents, runtime artifacts, workbook exports, frontend build output, or local-only artifacts."
    - "Do not add destructive controls or arbitrary SQL/database browsing."
```
