# Live-Capture Control Runtime Decomposition Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/719>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

## Contract

`docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md`

## Internal Project Area

Local App / live-capture runtime support, with parser-state and local analytics contacts.

## Truth Owner

`live_capture_control.py` continues to own only local app runtime control mechanics. Parser/state code remains the parser truth owner.

## Bridge-Code Status

`bridge_code`

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented only the owner-approved first slice:

`extract_pure_status_state_payload_helpers`

The implementation keeps `src/mythic_edge_parser/local_app/live_capture_control.py` as the public facade and extracts deterministic status/state/payload helper logic into `src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py`.

The public facade still exposes:

- `build_live_capture_status()`
- `start_live_capture()`
- `stop_live_capture()`
- `LocalAppLiveCaptureSupervisor`
- existing public constants used by tests and callers

The first slice intentionally did not move supervisor lifecycle code, registry state, `_run_async()`, `_tick_mtga_lifecycle()`, parser calls, SQLite live-write behavior, configured Player.log path reads, app-data state-file reads/writes, backend route binding, or frontend payload validators.

## Files Changed

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py`
- `docs/implementation_handoffs/core_live_capture_control_runtime_decomposition_decision_packet_comparison.md`

## Code Changed

Runtime code changed only as a behavior-preserving same-repo extraction.

Moved helper implementations include heartbeat/progress defaulting, public-safe state/result/code sanitization, timestamp helpers, precondition row helpers, warning/error derivation, stale-state calculation, and parser status blurb construction.

## Tests Added Or Updated

No tests were changed. Existing focused tests already covered the moved helper behavior through the stable facade and backend routes.

## Interface Changes

No public interface changes.

No route behavior, frontend/API payload shape, parser behavior, parser truth ownership, EventBus behavior, SQLite live writes, MTGA lifecycle behavior, workbook/webhook/Apps Script behavior, or CI behavior changed.

## Contracted Area Status

The implementation stayed inside the owner-approved first slice. It preserved the current `live_capture_control.py` public facade and did not move protected lifecycle, parser, state-file I/O, or SQLite write behavior.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: preserved by existing focused no-echo tests.
- Vocabulary and example coherence: preserved; no status strings, schema versions, warning/error codes, or payload field names changed.
- Authority/readiness semantics: no readiness, reliability readiness, parser truth, security assurance, privacy assurance, release, deploy, or production claims made.
- Fail-closed schema or validator checks: not applicable to this helper extraction; existing fail-closed sanitizers were moved unchanged.
- Protected-surface rollout phase: Phase 5 same-repo behavior-preserving decomposition slice.

## Validation Run

```bash
python3 -m py_compile src/mythic_edge_parser/local_app/live_capture_control.py src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py
# passed

python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py
# 12 passed

python3 -m pytest -q tests/test_live_app_mtga_process_lifecycle.py
# 7 passed

python3 -m pytest -q tests/test_analytics_local_app_backend.py
# 32 passed

python3 -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py
# 11 passed

python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_live_app_mtga_process_lifecycle.py tests/test_analytics_local_app_backend.py tests/test_live_app_parser_owned_fact_capture_sqlite.py
# 62 passed

python3 -m pytest -q tests/test_analytics_local_app_config.py tests/test_analytics_local_app_backend.py
# 54 passed

python3 -m ruff check src/mythic_edge_parser/local_app tests/test_live_app_explicit_start_capture_control.py tests/test_live_app_mtga_process_lifecycle.py
# passed

python3 -m ruff check src tests tools
# passed

git diff --check
# passed

printf '%s\n' src/mythic_edge_parser/local_app/live_capture_control.py src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed; scanned_paths: 2, forbidden: 0, warnings: 0

printf '%s\n' src/mythic_edge_parser/local_app/live_capture_control.py src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed; changed_paths: 2, forbidden: 0, warnings: 0

printf '%s\n' src/mythic_edge_parser/local_app/live_capture_control.py src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
# selection_status: ok
```

Note: the full non-path-scoped secret/protected-surface tools compare committed `HEAD` to `origin/main`; because this Codex C work is uncommitted, those full commands reported zero changed paths. The path-scoped checks above inspected the changed files directly and passed.

## Still Unverified

- Independent Codex E review.
- Full repository test suite.
- Live MTGA runtime behavior, private Player.log behavior, deployed app behavior, workbook/webhook/Apps Script behavior, and production behavior were not exercised and are not claimed.

## Reviewer Focus

Codex E should check that:

- `live_capture_control.py` still exposes the same public functions, class, and constants.
- The new helper module contains only deterministic status/state/payload helper logic.
- No lifecycle, registry, parser call, SQLite live-write, state-file I/O, backend route, or frontend payload validator behavior moved.
- Existing private helper names reached through the facade remain available for focused tests.
- No payload shape, status vocabulary, warning/error code, no-echo behavior, or readiness/truth/assurance semantics changed.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #719.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/719

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_live_capture_control_runtime_decomposition_decision_packet_comparison.md

Review the Codex C implementation of the owner-approved first slice `extract_pure_status_state_payload_helpers` for `src/mythic_edge_parser/local_app/live_capture_control.py`.

Verify behavior preservation, public facade preservation, no payload/status/no-echo changes, no lifecycle/registry/parser/SQLite/state-file/backend/frontend movement, validation evidence, and preserved false-authority/non-claim boundaries.

Protected boundaries:
Do not implement fixes unless explicitly rerouted as Codex D. Do not run ARS or Refactor Scout, read private logs/raw Player.log/private evidence/raw diffs, change live-capture/frontend/API/parser/EventBus/SQLite/workbook/webhook/Apps Script/CI behavior, or claim readiness, reliability readiness, parser truth, security assurance, privacy assurance, release readiness, deploy readiness, or production readiness.

Expected output:
Findings first. If clean, route to Codex F. If blocked, route to Codex D with exact finding IDs, affected files/functions, expected vs actual behavior, and validation to rerun.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/719"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_live_capture_control_runtime_decomposition_decision_packet_comparison.md"
  risk_tier: "High"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/live-capture-control-runtime-impl-719"
  candidate_id: "live-capture-control-runtime"
  candidate_surface: "src/mythic_edge_parser/local_app/live_capture_control.py"
  implemented_slice: "extract_pure_status_state_payload_helpers"
  public_facade_preserved: true
  live_capture_behavior_change_authorized: false
  live_capture_behavior_changed: false
  live_capture_payload_shape_change_authorized: false
  live_capture_payload_shape_changed: false
  supervisor_lifecycle_change_authorized: false
  supervisor_lifecycle_changed: false
  parser_behavior_change_authorized: false
  parser_behavior_changed: false
  parser_truth_ownership_change_authorized: false
  eventbus_behavior_change_authorized: false
  sqlite_live_write_behavior_change_authorized: false
  mtga_process_lifecycle_behavior_change_authorized: false
  frontend_behavior_change_authorized: false
  api_payload_change_authorized: false
  backend_route_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_log_read_authorized: false
  raw_player_log_read_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  analytics_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
  validation:
    - "python3 -m py_compile src/mythic_edge_parser/local_app/live_capture_control.py src/mythic_edge_parser/local_app/live_capture_control_payload_helpers.py passed"
    - "python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py passed: 12 passed"
    - "python3 -m pytest -q tests/test_live_app_mtga_process_lifecycle.py passed: 7 passed"
    - "python3 -m pytest -q tests/test_analytics_local_app_backend.py passed: 32 passed"
    - "python3 -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py passed: 11 passed"
    - "combined contract-focused pytest passed: 62 passed"
    - "python3 -m pytest -q tests/test_analytics_local_app_config.py tests/test_analytics_local_app_backend.py passed: 54 passed"
    - "python3 -m ruff check src tests tools passed"
    - "git diff --check passed"
    - "path-scoped secret/private marker scan passed for changed files"
    - "path-scoped protected-surface gate passed for changed files"
    - "path-scoped validation selector returned selection_status: ok"
  stop_conditions:
    - "Do not move public live-capture status/start/stop entrypoints or LocalAppLiveCaptureSupervisor."
    - "Do not move registry, supervisor lifecycle, parser calls, SQLite live writes, MTGA lifecycle behavior, configured Player.log reads, state-file reads/writes, backend route binding, or frontend payload validators in this slice."
    - "Do not run ARS or Refactor Scout."
    - "Do not claim readiness, reliability readiness, parser truth, security assurance, privacy assurance, release readiness, deploy readiness, or production readiness."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "C"
  risk_tier: "High"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md"
  protected_surfaces:
    - "live-capture runtime control bridge"
    - "parser truth ownership"
    - "frontend/API payload shape"
    - "SQLite live writes"
    - "MTGA lifecycle behavior"
    - "state-file read/write behavior"
    - "backend route binding"
  authority_conflicts_found: true
  authority_conflict_notes: "The merged contract records implementation_authorized=false. The current owner approval authorizes only the first Codex C slice extract_pure_status_state_payload_helpers; all broader false-authority flags remain false."
  stop_conditions:
    - "Stop if implementation requires changing public entrypoints, payload shape, live-capture behavior, parser behavior, or lifecycle/state-file/SQLite behavior."
    - "Stop if private logs/raw Player.log/private evidence/raw diffs are needed."
```
