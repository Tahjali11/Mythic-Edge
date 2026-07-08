# Codex C Implementation Handoff: Frontend API Client Boundary Decomposition

## Role Performed

Codex C: Module Implementer for issue #695.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/695>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Source decision packet: `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`
- Source decision PR: <https://github.com/Tahjali11/Mythic-Edge/pull/694>
- Source decision merge commit: `db722d865e8bf64f07a3c693acc654960867cf0f`

## Current Behavior Compared To Contract

`frontend/src/api.ts` was the stable browser-side API facade and also contained
endpoint path constants, public API error classes, loopback base URL validation,
local request-guard caching/fetching, guarded mutating fetch behavior, fetch
helpers, and payload validators.

The #693 decision packet and #695 issue authorize only behavior-preserving
same-repo decomposition for `frontend/src/api.ts`. They require preserving:

- the public `frontend/src/api.ts` import path;
- named public exports for current API helpers and error classes;
- endpoint paths;
- request-guard behavior;
- validator semantics;
- safe error mapping;
- frontend behavior;
- API payload shape;
- live-capture behavior;
- parser behavior and parser truth ownership.

## Implementation Summary

Implemented a narrow same-repo decomposition while preserving
`frontend/src/api.ts` as the public facade.

Private implementation details moved into:

- `frontend/src/api/errors.ts` for public API error class definitions;
- `frontend/src/api/paths.ts` for endpoint path constants;
- `frontend/src/api/request.ts` for loopback base URL validation,
  local request-guard caching/fetching, reset-for-tests, and guarded fetch.

`frontend/src/api.ts` now imports those private helpers and re-exports the same
public error classes and request helpers. Fetch helpers and payload validators
remain on the facade path, so callers continue to import from `./api`.

No endpoint paths, schema constants, request-guard header names, fetch helper
semantics, validators, backend route bindings, live-capture behavior, parser
behavior, CI configuration, or production behavior were changed.

## Files Changed

- `frontend/src/api.ts`
- `frontend/src/api/errors.ts`
- `frontend/src/api/paths.ts`
- `frontend/src/api/request.ts`
- `docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md`

## Behavior-Preservation Evidence

Frontend dependencies were missing at first: `vitest` and `tsc` were not
available until `npm --prefix frontend ci` restored local `node_modules`.
`npm ci` reported two high-severity dependency audit findings. This lane did
not authorize dependency updates or audit remediation.

The focused API test suite passed after the decomposition:

```bash
npm --prefix frontend test -- --run src/api.test.ts
```

Result:

- 1 test file passed.
- 39 tests passed.

The exact issue-listed command:

```bash
npm --prefix frontend test -- --run frontend/src/api.test.ts
```

was attempted first after dependencies were installed, but Vitest reported
`No test files found` because `npm --prefix frontend` runs with `frontend/` as
the working directory. The frontend-relative filter `src/api.test.ts` is the
equivalent focused test command for this package layout.

TypeScript validation passed:

```bash
npm --prefix frontend run typecheck
```

Safety and hygiene checks:

```
python3 tools/check_secret_patterns.py --all
printf '%s\n' frontend/src/api.ts frontend/src/api/errors.ts frontend/src/api/paths.ts frontend/src/api/request.ts docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' frontend/src/api.ts frontend/src/api/errors.ts frontend/src/api/paths.ts frontend/src/api/request.ts docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
python3 direct changed-file trailing-whitespace/final-newline/ASCII check
```

Results:

- Repo-wide secret/private marker scan failed on pre-existing findings outside
  this change: 479 forbidden and 912 warnings across 1,297 scanned paths.
- Path-scoped secret/private marker scan over the five changed files passed
  with 0 forbidden and 0 warnings.
- Broad protected-surface check passed but reported `changed_paths: 0` for the
  default protected-surface diff selection; the path-scoped rerun covered the
  exact changed files.
- Path-scoped protected-surface check over the five changed files passed with
  0 forbidden and 0 warnings.
- `git diff --check` passed for tracked diff content.
- Direct changed-file trailing-whitespace, final-newline, and ASCII check
  passed for tracked and untracked changed files.

## Preserved Boundaries

- `frontend_behavior_change_authorized: false`
- `api_payload_change_authorized: false`
- `api_endpoint_change_authorized: false`
- `request_guard_change_authorized: false`
- `validator_behavior_change_authorized: false`
- `live_capture_behavior_change_authorized: false`
- `backend_route_change_authorized: false`
- `parser_behavior_change_authorized: false`
- `ci_change_authorized: false`
- `readiness_claimed: false`
- `security_assurance_claimed: false`
- `privacy_assurance_claimed: false`
- `parser_truth_claimed: false`

## Remaining Risks / Unverified Layers

- Codex E has not yet independently reviewed that the decomposition is
  behavior-preserving against #695 and the #693 decision packet.
- The #148 scoped evidence issue remains open on GitHub. Issue #695 records
  owner-scoped implementation authorization and an active workflow handoff, so
  this Codex C pass proceeded under #695 authority rather than treating #148 as
  a merged evidence artifact.
- Dependency audit remediation was not performed and is out of scope.
- No browser/manual UI smoke was run.
- No backend, parser, live-capture, workbook, webhook, Apps Script, CI, release,
  deploy, or production behavior was exercised or changed.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #695.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/695

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Source decision packet:
docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md

Review goal:
Review the behavior-preserving same-repo decomposition of
`frontend/src/api.ts`. Lead with findings. Verify that `frontend/src/api.ts`
remains the public facade, that public imports and named exports are preserved,
and that moving API errors, endpoint paths, and request-guard/base-URL transport
into `frontend/src/api/*` did not change endpoint paths, payload shapes, schema
constants, request-guard behavior, validator semantics, fetch helper semantics,
safe error mapping, live-capture behavior, parser behavior, CI behavior, or any
readiness/security/privacy/parser-truth claims.

Validation to inspect or rerun:
- npm --prefix frontend test -- --run src/api.test.ts
- npm --prefix frontend run typecheck
- python3 tools/check_secret_patterns.py --all
- python3 tools/check_protected_surfaces.py --base origin/main
- git diff --check

Do not fix implementation while reviewing unless explicitly asked. Route to
Codex D for concrete findings, Codex B if the contract is ambiguous, Codex F
only if review has no blocking findings, or stop if the lane should not
proceed.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/695"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/693"
  source_decision_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/694"
  source_decision_merge_commit: "db722d865e8bf64f07a3c693acc654960867cf0f"
  related_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/148"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_api_client_boundary_behavior_preserving_decomposition_ready_for_review"
  candidate_id: "frontend_api_client_boundary"
  candidate_surface: "frontend/src/api.ts"
  implementation_authorized: true
  same_repo_decomposition_authorized: true
  file_move_authorized: true
  frontend_behavior_change_authorized: false
  api_payload_change_authorized: false
  api_endpoint_change_authorized: false
  request_guard_change_authorized: false
  validator_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  parser_truth_claimed: false
```
