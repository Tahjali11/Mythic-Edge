# Parser Recovery Field Evidence Comparison Report - Implementation Handoff

## Context

- Repository: `Tahjali11/Mythic-Edge`
- Issue: `https://github.com/Tahjali11/Mythic-Edge/issues/453`
- Tracker: `https://github.com/Tahjali11/Mythic-Edge/issues/388`
- Parent private-evidence issue: `https://github.com/Tahjali11/Mythic-Edge/issues/434`
- Previous issue: `https://github.com/Tahjali11/Mythic-Edge/issues/452`
- Previous PR: `https://github.com/Tahjali11/Mythic-Edge/pull/539`
- Previous merge commit: `b34c535a87c3640302b262fe45c28f1832a91346`
- Branch used: `codex/parser-recovery-field-evidence-comparison-453`
- Contract: `docs/contracts/parser_recovery_field_evidence_comparison_report.md`

## Comparison Summary

The contract called for a report-only field-evidence comparison helper that
compares Field Recovery Matrix rows against reduced current field-evidence
summaries, optionally using sanitized local watcher / offset-window metadata.

Implemented:

- Added `src/mythic_edge_parser/app/field_evidence_comparison_report.py`.
- Added the required comparison report, row, expected-evidence, and
  current-evidence schema constants.
- Added `build_field_evidence_comparison_report(...)`.
- Added `compare_field_evidence(...)`.
- Added validators for reports, rows, expected evidence, and current evidence
  summaries.
- Reused existing vocabulary from:
  - `src/mythic_edge_parser/app/field_recovery_matrix.py`
  - `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
  - `src/mythic_edge_parser/app/evidence_ledger.py`
- Kept the helper pure, deterministic, in-memory, JSON-serializable, and
  side-effect free.
- Preserved all readiness and authorization flags as `False`.
- Preserved parser and analytics output policies from the matrix rows.
- Added fail-closed privacy validation that records symbolic error locations
  without returning submitted private/path-like values in report rows.
- Codex D follow-up fixed `FECOMP-E-001` and `FECOMP-E-002` by making
  context-supplied readiness/authorization claims and protected-surface
  claims fail closed without preserving those claims in the emitted report.
- Added watcher-context routing for stale, degraded, unavailable,
  blocked-missing-approval, and manual-review window statuses.

Not implemented, by contract:

- No parser behavior changes.
- No parser runtime imports.
- No CLI or report writer.
- No diagnostics, drift, runtime status, golden replay, feature-equity, corpus,
  fixture, workbook, webhook, Apps Script, analytics, AI, or coaching
  integration.
- No private harvest, watcher startup, tailer startup, source discovery, or
  source content reads.
- No corpus status changes, fixture promotion, #388 activation, or #381
  activation.

## Files Changed

- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`
- `src/mythic_edge_parser/app/field_evidence_comparison_report.py`
- `tests/test_field_evidence_comparison_report.py`
- `docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md`

## Tests Added

`tests/test_field_evidence_comparison_report.py` covers:

- report shape and false readiness/authorization flags;
- deterministic JSON serialization;
- direct comparison success;
- equivalent and derived-bounded confidence caps and review routing;
- approximate analytics-only non-restoration policy;
- unavailable, blocked-private, and blocked-external rows;
- stale watcher-context routing;
- degraded and conflict routing;
- unknown field IDs and unknown ledger IDs requiring review;
- fail-closed privacy handling without value echo;
- fail-closed handling for context-supplied readiness/authorization claims;
- fail-closed handling for context-supplied protected-surface claims;
- copy safety;
- no parser runtime imports from the new helper.

## Validation Run

Passed:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
PYTHONPATH=src python3 -m pytest -q tests/test_runtime_field_evidence.py
PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_field_evidence_comparison_report.md \
  src/mythic_edge_parser/app/field_evidence_comparison_report.py \
  tests/test_field_evidence_comparison_report.py \
  docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 -m ruff check src tests tools
PYTHONPATH=src python3 -m pytest -q tests
```

Full pytest result: `1885 passed in 31.39s`.

## Codex D Fixer Addendum

Codex E routed `FECOMP-E-001` and `FECOMP-E-002` back to Module Fixer with
`blocking_fail_closed_gaps_need_codex_d_fixer`.

Fix applied:

- Added a narrow context-claim scanner in
  `src/mythic_edge_parser/app/field_evidence_comparison_report.py`.
- Context-supplied readiness and authorization flags now force report status
  `fail_closed`.
- Context-supplied protected-surface assertions now force report status
  `fail_closed`.
- Unknown future keys under `protected_surface_assertions` also fail closed
  when their values are not `False`.
- The emitted report still keeps all readiness/authorization flags and all
  protected-surface assertions `False`.
- Error/status output remains symbolic and does not echo submitted values.

Focused tests added:

- `test_context_readiness_and_authorization_claims_fail_closed`
- `test_context_protected_surface_claims_fail_closed`

Post-fix validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
# 13 passed in 0.59s

PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py tests/test_runtime_field_evidence.py
# 48 passed in 1.65s

python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_agent_docs.py
# passed: errors 0, warnings 0

path-scoped secret/private-marker scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped protected-surface scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped validation selector over the four #453 files
# selection_status: ok

python3 -m ruff check src tests tools
# All checks passed!

PYTHONPATH=src python3 -m pytest -q tests
# 1887 passed in 21.33s
```

## Codex D Rebound Addendum

Codex E returned the package with
`fixer_pass_not_verified_blocking_fail_closed_gaps_remain`.

The previous D pass only applied the fail-closed claim scanner to the optional
`context` input. That left equivalent readiness/authorization and
protected-surface claims in other caller-supplied inputs to be normalized away
or downgraded to non-fail-closed statuses.

Fix applied:

- Applied the input claim scanner to:
  - `context`
  - caller-supplied field recovery matrix reports
  - `current_field_evidence`
  - `watcher_context`
- Added camelCase normalization for the same contracted readiness,
  authorization, and protected-surface flag names.
- Treated scalar/non-mapping `protected_surface_assertions` claims as
  fail-closed rather than a soft shape error.

Focused tests added:

- `test_current_evidence_claims_fail_closed_before_normalization`
- `test_matrix_and_watcher_claims_fail_closed`

Direct rebound reproduction now returns `fail_closed` for:

- current evidence `parser_behavior_ready=true`
- current evidence `private_harvest_authorized=true`
- current evidence camelCase `parserBehaviorReady=true`
- current evidence `protected_surface_assertions` claims
- current evidence camelCase `protectedSurfaceAssertions` claims
- watcher-context readiness/protected-surface claims
- caller-supplied matrix readiness claims

Post-rebound validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
# 15 passed in 0.97s

PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py tests/test_runtime_field_evidence.py
# 48 passed in 1.61s

python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
# All checks passed!

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_agent_docs.py
# passed: errors 0, warnings 0

path-scoped secret/private-marker scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped protected-surface scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped validation selector over the four #453 files
# selection_status: ok

PYTHONPATH=src python3 -m pytest -q tests
# 1889 passed in 23.12s
```

## Codex D Second Rebound Addendum

Codex E returned the package with
`rebound_fix_incomplete_direct_comparator_bypass_needs_codex_d`.

The previous rebound fixed report-level input scanning but left the direct
`compare_field_evidence(...)` helper able to normalize away extra
readiness/authorization and protected-surface claim fields before comparison.
That meant direct comparator calls could still produce `comparison_status:
direct` for otherwise-valid current evidence or matrix rows carrying forbidden
claims.

Fix applied:

- Routed `_input_claim_errors(...)` through the direct comparator for:
  - matrix rows passed to `compare_field_evidence(...)`;
  - raw current evidence passed to `compare_field_evidence(...)`;
  - watcher context passed to `compare_field_evidence(...)`.
- Preserved report-level `fail_closed` behavior in
  `build_field_evidence_comparison_report(...)`.
- Preserved row-level vocabulary by routing direct-comparator claim bypasses to
  `comparison_status: invalid_input`, `review_required: true`, and
  `blocked_by_policy` recovery hints.

Focused test added:

- `test_direct_comparator_claim_bypass_inputs_are_invalid`

Direct second-rebound reproduction now returns `invalid_input` for:

- direct current evidence carrying camelCase `parserBehaviorReady=true`;
- direct current evidence carrying camelCase protected-surface assertions;
- direct matrix rows carrying `private_harvest_authorized=true`;
- direct watcher context carrying protected-surface assertions.

Post-second-rebound validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
# 16 passed in 1.00s

PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py tests/test_runtime_field_evidence.py tests/test_evidence_ledger.py
# 149 passed in 2.51s

python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
# All checks passed!

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed with no output

git diff --no-index --check /dev/null <new-file>
# passed for all four #453 artifacts

python3 tools/check_agent_docs.py
# passed: errors 0, warnings 0

path-scoped secret/private-marker scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped protected-surface scan over the four #453 files
# passed: forbidden 0, warnings 0

path-scoped validation selector over the four #453 files
# selection_status: ok

PYTHONPATH=src python3 -m pytest -q tests
# 1890 passed in 22.53s

python3 tools/run_pyright_advisory_report.py
# advisory_findings, advisory_non_blocking: 396 existing type findings
```

## Remaining Risks / Non-Claims

- The helper consumes synthetic/in-memory current field-evidence summaries only;
  no producer for those summaries is introduced in this issue.
- Summary counts are not readiness metrics.
- `direct` comparison rows do not authorize parser changes, fixture promotion,
  corpus status promotion, private harvest, or tracker activation.
- Equivalent, derived, stale, degraded, approximate, unavailable, blocked, and
  review-required rows remain review metadata only.
- Private-evidence and external-boundary rows remain blocked.
- #388, #381, and #434 remain inactive/open as applicable.

## Recommended Next Role

Codex E: Adversarial Reviewer.

Focus review on:

- whether the helper imports only allowed support modules;
- whether any parser runtime path imports the helper;
- whether privacy validation avoids echoing submitted private/path-like values;
- whether all false readiness and authorization flags are preserved;
- whether context, current-evidence, watcher-context, and caller-supplied
  matrix readiness/authorization and protected-surface claims fail closed;
- whether direct `compare_field_evidence(...)` calls with current-evidence,
  watcher-context, or matrix readiness/authorization and protected-surface
  claims return `invalid_input` rather than `direct`;
- whether comparison statuses, confidence caps, and recovery hints can promote
  parser truth, fixture promotion, corpus status, private harvest, #388/#381
  activation, or readiness by accident.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Adversarial Reviewer for issue #453.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/453

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/452

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/539

Previous merge commit:
b34c535a87c3640302b262fe45c28f1832a91346

Branch:
codex/parser-recovery-field-evidence-comparison-453

Contract:
docs/contracts/parser_recovery_field_evidence_comparison_report.md

Implementation handoff:
docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md

Goal:
Adversarially review the report-only field-evidence comparison helper against
the contract. Confirm the implementation is pure, deterministic, in-memory,
public-safe, and cannot promote parser truth, fixture promotion, corpus status,
private harvest, #388/#381 activation, or readiness.

Review:
- src/mythic_edge_parser/app/field_evidence_comparison_report.py
- tests/test_field_evidence_comparison_report.py
- docs/contracts/parser_recovery_field_evidence_comparison_report.md
- docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md
- read-only references:
  - src/mythic_edge_parser/app/field_recovery_matrix.py
  - src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py
  - src/mythic_edge_parser/app/evidence_ledger.py
  - src/mythic_edge_parser/app/runtime_field_evidence.py

Check especially:
- imports stay limited to allowed support modules;
- no parser runtime path imports the helper;
- report and row validators preserve false readiness/authorization flags;
- context, current-evidence, watcher-context, and caller-supplied matrix
  readiness/authorization and protected-surface claims fail closed without
  preserving the claims;
- direct `compare_field_evidence(...)` calls cannot normalize away
  readiness/authorization or protected-surface claims into `direct` rows;
- privacy errors do not echo submitted private/path-like values;
- current evidence summaries cannot carry parser output values, raw payload
  values, raw hashes, exact private offsets/sizes/timestamps, raw private lines,
  decklists, private paths, local artifacts, or secrets;
- direct/equivalent/derived/approximate/unavailable/blocked/stale/degraded/
  conflict/review/invalid statuses follow the contract;
- confidence caps never raise current evidence confidence;
- parser output policies are copied from the Field Recovery Matrix and not
  loosened;
- watcher context is optional sanitized metadata and never proof of watcher
  correctness or private smoke success.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py
- PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
- PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
- PYTHONPATH=src python3 -m pytest -q tests/test_runtime_field_evidence.py
- PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src/mythic_edge_parser/app/field_evidence_comparison_report.py tests/test_field_evidence_comparison_report.py
- git diff --check
- python3 tools/check_agent_docs.py
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
- path-scoped validation selector

Do not:
- Change parser behavior.
- Run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics,
  drift, watcher, tailer, network, firewall/drop, packet, OS/router, or private
  smoke checks.
- Create fixtures, manifests, expected outputs, recovery packets, metadata
  diffs, local watcher outputs, offset state, local/generated artifacts,
  private reports, or corpus metadata edits.
- Promote blocked, report-only, private-evidence, external-boundary,
  approximate, fallback, watcher, offset-window, degraded, stale, unavailable,
  or review-required signals to parser truth.
- Claim parser_behavior_ready, pipeline activation readiness,
  fixture-promotion readiness, field recovery readiness, private smoke success,
  watcher correctness, release readiness, production readiness, analytics
  truth, AI truth, coaching truth, or full parser regression parity.
- Close #453, #388, or #434.
- Activate #388 or #381.
- Stage or commit unless explicitly asked.

End with:
- findings first, ordered by severity;
- validation run;
- residual risks;
- recommendation for next role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/453"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/452"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/539"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_recovery_field_evidence_comparison_report.md"
  target_artifact: "docs/implementation_handoffs/parser_recovery_field_evidence_comparison_report_comparison.md"
  verdict: "FECOMP-E-001_and_FECOMP-E-002_second_rebound_fix_ready_for_adversarial_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "b34c535a87c3640302b262fe45c28f1832a91346"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
```
