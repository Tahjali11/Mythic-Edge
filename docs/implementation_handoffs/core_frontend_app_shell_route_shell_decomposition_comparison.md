# Frontend App Shell Route-Shell Decomposition Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/700>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

Source decision packet:
<https://github.com/Tahjali11/Mythic-Edge/issues/697>

Fresh scoped evidence:
<https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/149>

## Contract

`docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

## Internal Project Area

Local App / UI.

## Truth Owner

The React app shell remains a display and explicit-control composition surface.
Parser facts, backend route payloads, API payload shape, live-capture runtime
semantics, workbook/webhook behavior, and Apps Script behavior remain upstream
of this change.

## Bridge-Code Status

`bridge_code`

## Role Performed

Codex C: Module Implementer.

## Current Behavior Before This Slice

`frontend/src/App.tsx` remained the public app-shell facade and also owned the
route/hash vocabulary, static rail item labels, static rail aria copy, hash
reader, route membership guard, and route link `href` construction inline.

The broader app shell also owns many unrelated concerns, including dashboard
composition, analytics and review panels, live-capture controls, diagnostics,
manual import, feedback, and Match Journal UI state. Those areas are
intentionally untouched by this route-shell slice.

## Implementation Comparison

What stayed the same:

- `frontend/src/App.tsx` remains the public facade.
- The named `SetupStatusApp` export is preserved.
- The default `SetupStatusApp` export is preserved.
- `SetupStatusAppProps` dependency-injection behavior is preserved.
- Route/hash values are preserved:
  `dashboard`, `coach`, `analytics`, `review`, `privacy`, `feedback`,
  `import`, and `diagnostics`.
- Unknown hashes still fall back to `dashboard`.
- Static rail labels, rail aria labels, active-route semantics, and route-card
  href values are preserved.
- No visible control, label, aria behavior, storage key, API payload,
  live-capture behavior, backend route, parser behavior, workbook/webhook
  behavior, Apps Script behavior, or CI behavior was intentionally changed.

What changed:

- Added private helper module `frontend/src/app_navigation.ts`.
- Moved route/hash vocabulary, static rail copy, rail items, route membership,
  hash reading, and `#route` href generation into that helper.
- Updated `frontend/src/App.tsx` to consume the helper while keeping rendering
  and route visibility decisions in the facade.
- Added `frontend/src/app_navigation.test.ts` to lock exact vocabulary,
  labels, fallback behavior, and href generation.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/app_navigation.ts`
- `frontend/src/app_navigation.test.ts`
- `docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md`

## Code Changed

Runtime frontend code changed only to extract private route-shell helpers behind
the existing `frontend/src/App.tsx` facade.

No public frontend interface changed. The new module is private same-repo
support for the first approved route/hash and static rail metadata slice.

## Tests Added Or Updated

- Added `frontend/src/app_navigation.test.ts` to verify:
  - exact route vocabulary and order;
  - exact rail labels and order;
  - static left-rail copy and aria labels;
  - supported hash normalization;
  - unknown-route fallback to `dashboard`;
  - route membership and symbolic `#route` href generation.

Existing `frontend/src/App.test.tsx` and `frontend/src/api.test.ts` were
rerun unchanged for facade and API-boundary behavior preservation.

## Interface Changes

No public interface changes.

Private same-repo module added:

- `frontend/src/app_navigation.ts`

Preserved public interfaces:

- `frontend/src/App.tsx`
- named `SetupStatusApp` export
- default `SetupStatusApp` export
- `SetupStatusAppProps` dependency-injection behavior
- route/hash vocabulary and fallback behavior

## Contracted Area Status

Stayed inside the contracted Local App / UI area and issue #700 scope.

The worktree was fast-forwarded to current `origin/main` at
`c152edbdf96b3ff77b9395b6a3d47a4757f19f81`. No frontend target drift was
present between the evidence target commit
`aff54bf0143cd57ca116ae4ed1822326410df29c` and current `origin/main`.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: Preserved; no raw logs, private paths, secrets,
  hashes, credentials, or runtime artifacts added.
- Vocabulary and example coherence: Route and rail vocabulary locked by focused
  tests.
- Authority/readiness semantics: No readiness, reliability readiness, parser
  truth, analytics truth, AI truth, coaching truth, security assurance, or
  privacy assurance claim made.
- Fail-closed schema or validator checks: Not applicable; this slice extracts
  pure frontend route/navigation helpers.
- Protected-surface rollout phase: Same-repo behavior-preserving
  decomposition only.

## Validation Run

```bash
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts
npm --prefix frontend test -- --run src/app_navigation.test.ts
npm --prefix frontend run typecheck
printf '%s\n' frontend/src/App.tsx frontend/src/app_navigation.ts frontend/src/app_navigation.test.ts | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/app_navigation.ts frontend/src/app_navigation.test.ts | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
printf '%s\n' frontend/src/App.tsx frontend/src/app_navigation.ts frontend/src/app_navigation.test.ts docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/app_navigation.ts frontend/src/app_navigation.test.ts docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
printf '%s\n' frontend/src/App.tsx frontend/src/app_navigation.ts frontend/src/app_navigation.test.ts docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Results:

- Required App/API tests passed: 2 files, 96 tests.
- New route-shell helper tests passed: 1 file, 4 tests.
- TypeScript typecheck passed.
- Required path-scoped frontend secret/private marker scan passed: 3 scanned
  paths, 0 findings.
- Required path-scoped frontend protected-surface scan passed: 3 changed paths,
  0 findings.
- Required `python3 tools/check_secret_patterns.py --all` failed on pre-existing
  repo-wide legacy findings outside this slice: 1,303 scanned paths, 479
  forbidden findings, 912 warnings. Changed-file scans for this implementation
  passed cleanly.
- Required `python3 tools/check_protected_surfaces.py --base origin/main`
  passed with 0 findings. It reported 0 changed paths because these changes are
  still in the working tree rather than committed `HEAD`; the path-scoped
  changed-file protected-surface scan above did scan the actual changed files.
- `git diff --check` passed.
- Path-scoped secret/private marker scan over frontend plus this handoff passed:
  4 scanned paths, 0 findings.
- Path-scoped protected-surface scan over frontend plus this handoff passed:
  4 changed paths, 0 findings.
- Agent docs consistency check passed: 36 checked files, 0 errors, 0 warnings.
- Validation selector passed and required frontend tests, build, typecheck,
  diff check, protected-surface gate, and secret/private marker scan.
- Full frontend test suite passed: 4 files, 104 tests.
- Production frontend build passed.

## Still Unverified

- Independent Codex E review.
- Browser visual/manual inspection.
- GitHub CI behavior.
- Any later frontend app-shell slices beyond route/hash and static rail
  metadata.

## Reviewer Focus

Please verify:

- route/hash fallback behavior stayed identical;
- rail labels and aria labels stayed identical;
- `frontend/src/App.tsx` remains the public facade;
- `SetupStatusApp`, the default export, and `SetupStatusAppProps` remained
  intact;
- no API, live-capture, parser, backend, storage, CI, workbook, webhook, or
  Apps Script behavior changed;
- the new helper module does not broaden beyond private same-repo route-shell
  support.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #700, frontend app shell route-shell behavior-preserving decomposition.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/700

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md

Review goal:
Review the behavior-preserving same-repo extraction of route/hash vocabulary and static rail metadata from frontend/src/App.tsx into frontend/src/app_navigation.ts.

Protected boundaries:
Do not change frontend behavior, route/hash behavior, visible controls, labels, aria labels, storage keys, API payloads, live-capture behavior, backend routes, parser behavior, workbook/webhook/Apps Script behavior, CI, readiness claims, reliability readiness claims, parser truth claims, security assurance, or privacy assurance.

Expected output:
Findings first, validation assessment, remaining risk, recommended next role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/700"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  fresh_scoped_evidence: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/149"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_app_shell_route_shell_decomposition_ready_for_review"
  target_artifact: "docs/implementation_handoffs/core_frontend_app_shell_route_shell_decomposition_comparison.md"
  branch: "codex/frontend-app-shell-route-shell-700"
  base_branch: "origin/main"
  current_origin_main: "c152edbdf96b3ff77b9395b6a3d47a4757f19f81"
  evidence_target_commit: "aff54bf0143cd57ca116ae4ed1822326410df29c"
  implementation_scope: "behavior_preserving_same_repo_route_hash_static_rail_metadata_slice"
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  visible_control_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  backend_route_change_authorized: false
  parser_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
