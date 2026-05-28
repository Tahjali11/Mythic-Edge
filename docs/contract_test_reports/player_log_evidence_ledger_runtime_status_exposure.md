# Player.log Evidence Ledger Runtime Status Exposure Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/183

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Role Performed

- Codex E: Module Reviewer / contract-test thread.
- Codex D: Module Fixer follow-up for the blocking privacy redaction finding.
- Codex E: Module Reviewer / contract-test re-review of the Codex D fixer pass.

## Contract Under Test

- `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `tests/test_evidence_runtime_status.py`
- `tests/test_diagnostics.py`
- `tests/test_status_api.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md`

## Findings

### Blocking

None remaining from the Codex D fixer pass.

### Resolved By Codex D

1. `evidence_ledger_health` could expose local path and username fragments after sanitization.

   Contract reference: `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md:634` requires no local absolute paths and no local usernames in the runtime health summary, and `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md:651` says privacy findings must be path-only and must not echo forbidden values.

   Original review evidence showed `_safe_text(...)` redacting only path roots such as `/Users` or `C:\`, leaving path tails such as `example/private/Player.log` and Windows profile names such as `Jane Doe`.

   Codex D fixed `src/mythic_edge_parser/app/evidence_runtime_status.py` so complete POSIX paths, Windows local paths, UNC paths, and stale `[redacted-path]/...` tails are collapsed to `[redacted-path]`. Focused coverage in `tests/test_evidence_runtime_status.py` now proves copied `status_reasons`, `affected.entries`, `review_guidance.review_notes`, and `drift_flags` do not retain `/Users`, `example/private`, `Player.log`, `C:\Users`, `Jane Doe`, or `AppData` fragments.

## Contract-Test Verdict

No blocking findings remain. Issue #183 is ready for Codex F.

Most of the contracted runtime-status behavior matches: the implementation adds one optional `evidence_ledger_health` field, builds it from explicit in-memory mappings, keeps `/health` unchanged, writes through `diagnostics.update_runtime_status(...)`, avoids new routes/CLI/env vars/discovery, and preserves parser/runtime/workbook/webhook/App Script behavior outside the authorized local status field.

The Codex D fix is limited to privacy redaction in the new helper and focused tests. No parser behavior drift or downstream protected-surface change is introduced by the patch.

## Confirmed Contract Matches

- `src/mythic_edge_parser/app/evidence_runtime_status.py` defines the contracted health object, schema version, status vocabulary, and source keys.
- `build_evidence_ledger_health_status(...)` returns `unavailable` with `review_required=false` when no source summaries are supplied.
- Existing `evidence_ledger_review` input is preferred over individual source summaries.
- Source status normalization covers `not_supplied`, `pass`, `degraded`, `review`, `diff`, and `fail`.
- Malformed non-mapping sources, unknown object/schema/status values, privacy findings, and true protected-surface assertions fail the health summary.
- Full attachments, field-evidence records, schema snapshot diffs, and invariant result bodies are not copied as full detail structures.
- All `status_affects_*` flags are false.
- `update_evidence_ledger_health_status(...)` writes only `evidence_ledger_health` through `diagnostics.update_runtime_status(...)`.
- Existing runtime status top-level `status` and failure counters are preserved.
- `/status` exposes `evidence_ledger_health` only because it returns the existing status artifact.
- `/health` remains unchanged and does not include `evidence_ledger_health`.
- No new status API route, CLI, environment variable, implicit discovery, background watcher, or status promotion was added.
- Complete local POSIX and Windows path strings copied into runtime health summary strings are redacted without retaining usernames or path tails.

## Contract Mismatches

- None.

## Missing Tests Or Safeguards

- Added focused regression coverage for complete POSIX path-tail redaction after `/Users/<username>/...`.
- Added focused regression coverage for complete Windows profile path redaction, including usernames containing spaces.
- Added assertions that copied string fields do not contain username fragments, path tails, `Player.log`, `AppData`, or other local path components after redaction.

## Drift Classification

- Parser behavior: no drift found.
- Parser state final reconciliation: no drift found.
- Parser event classes/router semantics: no drift found.
- Workbook schema/webhook payload/Apps Script/output transport: no drift found.
- Status API route shape: no drift found.
- `/health` shape: no drift found.
- Runtime status schema: authorized additive `evidence_ledger_health` field only.
- Privacy boundary: original sanitizer drift fixed by Codex D and verified by Codex E re-review.
- Generated data, raw logs, runtime status files, failed posts, workbook exports, secrets, CI/deploy policy: no drift found in the reviewed diff.

## Validation Results

```bash
python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py
```

Codex E result: `22 passed in 0.61s`

Codex D result after sanitizer fix: `23 passed in 0.65s`

Codex E re-review result after sanitizer fix: `23 passed in 0.62s`

```bash
python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py
```

Result: `108 passed in 7.66s`

Codex D rerun after sanitizer fix: `108 passed in 7.97s`

Codex E re-review result after sanitizer fix: `108 passed in 7.88s`

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py
```

Result: `35 passed in 0.13s`

Codex D rerun after sanitizer fix: `35 passed in 0.25s`

Codex E re-review result after sanitizer fix: `35 passed in 0.21s`

```bash
python3 -m ruff check src tests tools
```

Result: `All checks passed!`

Codex D rerun after sanitizer fix: `All checks passed!`

Codex E re-review result after sanitizer fix: `All checks passed!`

```bash
git diff --check
```

Result: passed with no output.

Codex D rerun after sanitizer fix: passed with no output.

Codex E re-review result after sanitizer fix: passed with no output.

```bash
printf '%s\n' docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md src/mythic_edge_parser/app/evidence_runtime_status.py tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Result: passed; `changed_paths: 7`, `forbidden: 0`, `warnings: 0`.

Codex D rerun after sanitizer fix: passed; `changed_paths: 7`, `forbidden: 0`, `warnings: 0`.

Codex E re-review result after sanitizer fix: passed; `changed_paths: 7`, `forbidden: 0`, `warnings: 0`.

```bash
python3 -m pytest -q
```

Result: `1083 passed in 10.02s`

Codex D rerun after sanitizer fix: `1084 passed in 9.43s`

Codex E re-review result after sanitizer fix: `1084 passed in 9.36s`

The original review-only sanitizer probe finding is fixed by the Codex D path-token redaction and focused regression coverage. Codex E re-review also directly probed copied runtime health strings containing POSIX and Windows profile paths and confirmed no `/Users`, `example/private`, `Player.log`, `C:\Users`, `Jane Doe`, or `AppData` fragments remained in the encoded health object.

## Remaining Non-Blocking Gaps

- GitHub Actions were not run in this local review.
- Live workbook state, deployed Apps Script state, production behavior, private runtime artifacts, launcher behavior, and overlay display behavior were not checked.
- Future `/health` inclusion, launcher/overlay display, implicit report discovery, and configured report paths remain deferred by contract.

## Next Recommended Role

Codex F: Module Submitter.

Submit only the reviewed #183 scope. Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics, top-level runtime status semantics, `/health` shape, status API routes, workbook/webhook/App Script/output surfaces, production behavior, analytics truth, AI truth, CI gates, merge policy, deploy policy, or tracker lifecycle.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/183"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_runtime_status.py; tests/test_evidence_runtime_status.py; docs/implementation_handoffs/player_log_evidence_ledger_runtime_status_exposure_comparison.md; docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/player-log-evidence-ledger-runtime-status-exposure"
  base_branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_evidence_runtime_status.py tests/test_diagnostics.py tests/test_status_api.py -> 23 passed in 0.62s"
    - "python3 -m pytest -q tests/test_evidence_validation_report_wiring.py tests/test_runtime_field_evidence.py tests/test_evidence_invariant_execution.py tests/test_evidence_schema_snapshot.py tests/test_evidence_schema_drift_report.py -> 108 passed in 7.88s"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_runtime_surfaces.py tests/test_runner.py -> 35 passed in 0.21s"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed with changed_paths: 7, forbidden: 0, warnings: 0"
    - "python3 -m pytest -q -> 1084 passed in 9.36s"
  resolved_findings:
    - "evidence_runtime_status._safe_text now redacts complete POSIX and Windows local path tokens instead of leaving usernames/path tails in evidence_ledger_health copied strings."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #183 or tracker #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report semantics, top-level runtime status semantics, /health shape, status API routes, workbook/webhook/App Script/output surfaces, production behavior, analytics truth, AI truth, CI gates, merge policy, deploy policy, or tracker lifecycle."
    - "Do not read or commit raw private Player.log excerpts, local logs, generated data, runtime status files, failed posts, workbook exports, secrets, webhook URLs, OpenAI/model-provider output, or AI summaries."
```
