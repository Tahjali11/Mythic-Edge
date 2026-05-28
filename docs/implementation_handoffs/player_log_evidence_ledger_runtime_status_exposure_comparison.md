# Player.log Evidence Ledger Runtime Status Exposure Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/183

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`

## Role Performed

- Codex C: Module Implementer / comparison thread.
- Codex D: Module Fixer follow-up for the blocking privacy redaction finding.

## Branch And Status

- Base branch: `codex/parser-reliability-intelligence`
- Implementation branch: `codex/player-log-evidence-ledger-runtime-status-exposure`
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/182
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/185
- Previous merge commit: `ee80e4b08ff12f904e745535877de72e856cc85b`
- Starting status: branch matched `origin/codex/parser-reliability-intelligence`
  at `ee80e4b`; the #183 contract existed as an untracked source artifact.
- Ending status: implemented optional summary-only
  `evidence_ledger_health` runtime status helper behavior, focused tests, this
  handoff, and a local validation report.
- Codex D fixer status: fixed complete local path redaction in
  `evidence_runtime_status._safe_text(...)`, added focused regression coverage,
  and updated the handoff/report to route back to Codex E.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`
- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `docs/contracts/player_log_evidence_ledger_invariant_execution.md`
- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
- `docs/contracts/player_log_evidence_ledger_schema_drift_report.md`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py`
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
- `tests/test_diagnostics.py`
- `tests/test_status_api.py`
- `tests/test_evidence_validation_report_wiring.py`
- `tests/test_runtime_field_evidence.py`
- `tests/test_evidence_invariant_execution.py`
- `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md`

## Current Behavior Compared To Contract

Before this pass, runtime status had no `evidence_ledger_health` field and no
helper for summarizing evidence-ledger review health. `diagnostics.py` already
provided the single local runtime status writer, `/status` already returned the
current status artifact unchanged, and `/health` already returned a narrow
operational liveness object.

The contract authorized exactly one optional additive runtime status field and
a pure in-memory summary builder plus a writer helper that reuses
`diagnostics.update_runtime_status(...)`.

## Implementation Option Chosen

Implemented the smallest local helper layer:

- Added `src/mythic_edge_parser/app/evidence_runtime_status.py`.
- Added focused tests in `tests/test_evidence_runtime_status.py`.
- Added a diagnostics test proving `update_runtime_status(...)` can write
  `evidence_ledger_health` without changing top-level runtime status.
- Added a status API test proving `/status` exposes the field when present and
  `/health` remains unchanged.
- Added `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md`.
- Produced this implementation handoff.
- Codex D tightened the sanitizer to collapse complete POSIX, Windows, UNC,
  and stale `[redacted-path]/...` path tails to `[redacted-path]` in copied
  runtime health strings.

No status API routes, CLI flags, environment variables, implicit file
discovery, background watchers, parser behavior, diagnostics report semantics,
or downstream surfaces were changed.

## Files Changed

- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `tests/test_evidence_runtime_status.py`
- `tests/test_diagnostics.py`
- `tests/test_status_api.py`
- `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md`

Source artifact present but not edited by this thread:

- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`

## Confirmed Matches

- The new module defines the contracted object, schema version, statuses, and
  source keys.
- Public functions match the contract:
  `build_evidence_ledger_health_status()` and
  `update_evidence_ledger_health_status()`.
- No-source input returns `status=unavailable`, `review_required=false`, and
  `unavailable_count=5`.
- Existing `evidence_ledger_review` input is preferred over individual source
  summaries.
- `not_supplied` review status maps to runtime health `unavailable`.
- Runtime field-evidence `review` maps to health `review`.
- Schema snapshot comparison `diff` maps to health `diff`.
- Schema drift or invariant execution `fail` maps to health `fail`.
- Unknown source object, schema version, or status fails health.
- Non-mapping supplied source input fails health without raising.
- Full runtime attachments, field-evidence records, schema snapshot diffs, and
  source detail bodies are not copied into `evidence_ledger_health`.
- Privacy findings fail health and remain path-only.
- Complete local path tokens copied through status reasons, affected entries,
  review notes, and drift flags are redacted without retaining local usernames
  or path tails.
- Protected-surface assertions fail health.
- Every `status_affects_*` flag is false.
- The writer helper calls `diagnostics.update_runtime_status(...)` with only
  `evidence_ledger_health`.
- Existing `diagnostics.update_runtime_status(...)` can write the summary while
  preserving top-level runtime `status` and counters.
- `/status` exposes the field only because it returns the status artifact.
- `/health` shape remains unchanged and does not include
  `evidence_ledger_health`.

## Contract Mismatches

None found.

## Missing Safeguards

None blocking. The helper accepts explicit in-memory mappings only. It does not
read raw logs, runtime status files, failed posts, workbook exports, generated
data, secrets, webhook URLs, OpenAI/model-provider output, or AI summaries.

## Missing Or Weak Tests

None blocking. Focused tests cover all contract-required behavior listed
above plus diagnostics writer, status API boundary checks, and complete local
path redaction for POSIX and Windows profile paths.

## Validation Run

```bash
python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py
python3 -m ruff check src tests tools
git diff --check
```

Results at handoff creation:

- Runtime status exposure suite: `22 passed`
- Evidence-adjacent suite: `108 passed`
- Parser diagnostics/runtime/runner suite: `35 passed`
- Ruff: `All checks passed!`
- `git diff --check`: passed with no output

Codex D focused rerun after the sanitizer fix:

- Runtime status exposure/status API/diagnostics suite: `23 passed`
- Evidence-adjacent suite: `108 passed`
- Parser diagnostics/runtime/runner suite: `35 passed`
- Ruff: `All checks passed!`
- `git diff --check`: passed with no output
- Path-scoped protected-surface check: passed with `changed_paths: 7`,
  `forbidden: 0`, `warnings: 0`
- Full test suite: `1084 passed`

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
router semantics, diagnostics report semantics, top-level runtime status
semantics, `/health` shape, status API routes, golden replay behavior,
feature-equity behavior, runtime field-evidence behavior, schema snapshot
behavior, schema drift behavior, invariant execution behavior, workbook schema,
webhook payload shape, Apps Script behavior, output transport, ActionLogRow
shape, active match snapshot shape, match timeline shape, match history shape,
active deck profile shape, collection profile shape, Match Journal behavior,
overlay behavior, SQLite behavior, Google Sheets sync behavior, production
behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates,
merge policy, deploy policy, or tracker lifecycle was changed.

## What Remains Unverified

- GitHub Actions were not run.
- Live workbook state was not checked.
- Deployed Apps Script state was not checked.
- Production behavior was not checked.
- No private local evidence-ledger reports or runtime artifacts were consumed.

## Open Risks

- Future launcher or overlay display remains intentionally deferred.
- Future `/health` inclusion remains intentionally deferred.
- Future implicit report discovery or configured paths remain intentionally
  deferred.
- The health object is advisory review metadata only; consumer documentation
  may be needed if a future UI begins displaying it.

## Next Recommended Role

Codex E: Module Reviewer / contract-test mode.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #183, runtime
status exposure for evidence-ledger health, under tracker #11.

Review:
- docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md
- docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md
- src/mythic_edge_parser/app/evidence_runtime_status.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/evidence_validation_report_wiring.py
- tests/test_evidence_runtime_status.py
- tests/test_diagnostics.py
- tests/test_status_api.py
- tests/test_evidence_validation_report_wiring.py
- tests/test_runtime_field_evidence.py
- tests/test_evidence_invariant_execution.py
- tests/test_evidence_schema_snapshot.py
- tests/test_evidence_schema_drift_report.py

Confirm:
- exactly one optional runtime status field is introduced: evidence_ledger_health
- health is built from explicit in-memory source summaries only
- evidence_ledger_review is preferred when supplied
- missing sources are unavailable, not failures
- statuses normalize to unavailable/pass/degraded/review/diff/fail
- malformed sources, unknown object/schema/status, privacy findings, and protected-surface assertions fail health
- health is summary-only and does not inline attachments, field_evidence records, invariant results, snapshots, drift diffs, raw logs, raw payload values, runtime status contents, failed posts, workbook exports, secrets, webhook URLs, or AI/model-provider output
- update_evidence_ledger_health_status writes only evidence_ledger_health through diagnostics.update_runtime_status
- top-level runtime status, parser status, transport status, diagnostics report status, /health shape, and CI/merge/deploy meaning are unchanged
- /status exposes the field only because it returns the existing status artifact
- no new CLI, environment variables, implicit discovery, background watcher, status API route, or status promotion was added
- complete POSIX and Windows local paths in copied runtime health strings are redacted without retaining usernames, `Player.log`, `AppData`, or path tails

Validation:
- python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
- python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py
- python3 -m ruff check src tests tools
- git diff --check

Output findings first, then contract-test verdict, validation results,
remaining non-blocking gaps, next recommended role, and workflow_handoff block.

Do not change parser behavior, parser state final reconciliation, parser event
classes, router semantics, diagnostics report semantics, top-level runtime
status semantics, /health shape, status API routes, workbook/webhook/App
Script/output surfaces, production behavior, analytics truth, AI truth, CI
gates, merge policy, deploy policy, or tracker lifecycle. Do not stage, commit,
target main, or close tracker #11.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/183"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/182"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/185"
  previous_merge_commit: "ee80e4b08ff12f904e745535877de72e856cc85b"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_runtime_status.py; tests/test_evidence_runtime_status.py; docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md; docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md"
  verdict: "privacy_redaction_gap_fixed_ready_for_module_review"
  risk_tier: "High"
  branch: "codex/player-log-evidence-ledger-runtime-status-exposure"
  base_branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py -> 23 passed"
    - "python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py -> 108 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py -> 35 passed"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed"
    - "python3 -m pytest -q -> 1084 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics, top-level runtime status semantics, /health shape, status API routes, golden replay behavior, feature-equity behavior, runtime field-evidence behavior, schema snapshot behavior, schema drift behavior, invariant execution behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, active match snapshot shape, match timeline shape, match history shape, active deck profile shape, collection profile shape, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, or tracker lifecycle."
    - "Do not add evidence-ledger health to /health or add new status API routes in V1."
    - "Do not read raw private Player.log excerpts, raw local logs, generated data, runtime status files as input evidence, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, OpenAI/model-provider output, or AI summaries."
```
