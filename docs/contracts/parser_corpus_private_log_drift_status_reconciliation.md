# Parser Corpus Private Log Drift Status Reconciliation Contract

## Module

`mythic_edge.private_log_report_only_drift` corpus status reconciliation.

Plain English: this contract records that the existing private-log drift
boundary and private-evidence execution scaffold are sufficient for the current
tracker #158 state. The corpus family remains `blocked_private_evidence`. This
slice does not authorize private log reads, private drift execution, status
promotion, parser behavior changes, readiness claims, or #388 / #381
activation.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/510
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/508
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/509
- Previous merge commit:
  `d9be4b704a3e7b6039794d805a5039c5e411963f`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed issue state during this Codex B pass:

- Issue #510 is open.
- Tracker #158 is open.
- Related pipeline tracker #388 is open.
- Parent private-evidence issue #434 is open.
- The operating checkout was on `main` at
  `d9be4b704a3e7b6039794d805a5039c5e411963f`.
- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge`.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/contracts/repo_scoped_workflow_handoffs.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #510, tracker #158, issue #388, and issue #434
- Issue #422 / PR #423
- Issue #439 / PR #441
- Issue #442 / PR #443
- Issue #508 / PR #509
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `docs/templates/private_evidence_window_offset_capture.md`
- `docs/templates/private_log_drift_private_evidence_execution.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_private_evidence_execution_comparison.md`
- `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_log_drift_sensor.py`

## Observed Current Behavior

Current corpus parity CLI output:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current `mythic_edge.private_log_report_only_drift` row:

```yaml
scenario_family: "mythic_edge.private_log_report_only_drift"
coverage_status: "blocked_private_evidence"
coverage_basis:
  - "local_report_only"
entry_id: "private_log_report_only_drift_private_evidence_boundary_v1"
privacy_class: "local_private_not_committed"
sanitization_status: "requires_review"
parser_event_families: []
session_ledger_entry: intentionally_absent
committed_private_report_artifact: intentionally_absent
```

Existing boundary artifacts already establish:

- #422 / PR #423 selected `blocked_private_evidence` for this row.
- #439 / PR #441 established a private evidence window offset-capture process
  as process safety only.
- #442 / PR #443 established a private-log drift execution scaffold and
  template, but did not authorize private execution, private artifact commits,
  or status promotion.
- #508 / PR #509 did not change this row; it preserved report-only readiness
  semantics for an adjacent rename/rotation collision row.
- #158, #388, and #434 remain open.

Current non-evidence:

- No private `Player.log` or `UTC_Log` source has been read in this contract
  pass.
- No private diagnostics, drift, network, firewall/drop, live MTGA, packet,
  OS/router, or private smoke check has been run.
- No committed private drift report, private report hash, private offset
  state, private lifecycle summary, or private redacted drift summary exists
  for this row.
- No parser event family is attached to this row.
- No session-ledger entry exists for this row.

## Scope Decision

Selected path: preserve `blocked_private_evidence` with no new execution work.

This status-reconciliation contract is the only new artifact authorized by
issue #510. It records the decision; it does not create a new execution path.

Reasoning:

- #422 already defines the status boundary for the row.
- #442 already defines the approval-gated private execution scaffold.
- #439 already defines the offset-window safety primitive that future private
  execution may reference.
- The current issue provides no exact approved source class, symbolic source
  label, approved window, artifact class, offset policy, baseline policy,
  operator-note policy, redacted-summary policy, or status-transition approval.
- Without those inputs, any private execution, summary, or promotion would
  widen the lane and risk converting process scaffolding into false evidence.

Rejected paths in this slice:

- Do not move the row to `covered_report_only`.
- Do not move the row to `covered_synthetic`.
- Do not create or commit a private drift report.
- Do not run a local private execution packet.
- Do not split the row during this pass.
- Do not activate #388 / #381.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

This contract owns only the issue #510 status reconciliation decision for
`mythic_edge.private_log_report_only_drift`.

This contract does not own parser behavior, parser state final reconciliation,
parser event classes, router semantics, diagnostics behavior, drift report
behavior, runtime status behavior, workbook schema, webhook payload shape, Apps
Script behavior, Google Sheets sync, output transport, analytics truth, AI
truth, coaching truth, CI gates, merge readiness, deploy readiness, production
behavior, or tracker completion.

## Truth Boundary

Corpus parity owns scenario-family status and non-claim metadata.

`log_drift_sensor.py`, diagnostics code, live diagnostics reports,
unknown-entry reports, evidence-ledger health metadata, golden replay,
feature-equity reports, private-local readiness docs, and browser smoke plans
are adjacent review machinery or governance context. They do not prove private
log drift health.

Offset-window templates are process safety. They are not authorization to
inspect private data.

Future local private evidence, if explicitly approved later, remains
Generated / Local Artifacts until separately reviewed. It must not be treated
as parser truth, live Player.log health truth, drift health truth, readiness
truth, analytics truth, AI truth, coaching truth, tracker completion, or full
corpus parity truth.

## Public Interface

This contract adds no runtime public API, CLI, environment variable contract,
parser event class, parser payload shape, diagnostics report shape, drift
report shape, workbook schema, webhook payload shape, Apps Script behavior,
analytics schema, or local app behavior.

The only public artifact created by this Codex B pass is:

- `docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md`

## Allowed Inputs

Allowed in this contract pass:

- committed repo docs, contracts, templates, handoffs, reports, manifest,
  session ledger, source code, and focused tests;
- GitHub issue and PR metadata for #158, #388, #434, #422, #439, #442, #508,
  #509, and #510;
- already committed public-safe corpus parity metadata.

## Forbidden Inputs

Forbidden in this contract pass and in any committed artifact:

- raw private `Player.log` or `UTC_Log` contents;
- private app-data contents;
- private smoke outputs;
- private drift reports;
- local-only offset state;
- exact private paths;
- exact offsets, exact file sizes, exact private timestamps, raw hashes, raw
  payloads, raw log lines, screenshots, SQLite files, workbook exports,
  runtime artifacts, failed posts, credentials, tokens, API keys, webhook
  URLs, decklists, card choices, private strategy notes, IP/network traces,
  packet captures, OS/router diagnostics, firewall logs, Wi-Fi logs, or
  external corpus contents.

## Status-Transition Rules

This contract does not authorize status transitions.

`mythic_edge.private_log_report_only_drift` must remain
`blocked_private_evidence` unless a later explicit status-transition contract
and privacy review authorize a change.

The following values remain unchanged by this slice:

- `coverage_status: blocked_private_evidence`
- `coverage_basis: ["local_report_only"]`
- `parser_event_families: []`
- no session-ledger entry
- no committed private report artifact
- `parser_behavior_ready: false`
- `pipeline_activation_ready_for_issue_388: false`

Private drift execution, even if later approved and successful, does not by
itself prove parser support, private smoke success, live Player.log health,
drift health, release readiness, deploy readiness, production behavior,
analytics truth, AI truth, coaching truth, tracker completion, or full corpus
parity.

## Future Follow-Up Options

Future work may proceed only through a new scoped issue/contract if one of
these is explicitly chosen:

1. Local drift report execution packet for an approved symbolic source/window.
2. Redacted lifecycle summary candidate review.
3. Redacted drift summary candidate review.
4. Status-transition review for this row.
5. Row split into smaller sub-claims.
6. #388 / #381 parser-evidence-pipeline dependency activation.

None of those options is authorized by this contract.

## Invariants

- Codex B must not read private logs.
- Codex B must not run private checks.
- No private/local artifacts may be committed.
- No blocked row may be promoted by default.
- #158 remains open unless separately approved for lifecycle closure.
- #388 remains open and inactive.
- #434 remains open.
- #381 remains inactive.
- Zero missing corpus rows must not be treated as full corpus parity, tracker
  completion, parser support, private smoke success, live Player.log health,
  drift health, release readiness, production readiness, analytics truth, AI
  truth, or coaching truth.
- No parser/runtime/downstream behavior is authorized to change.

## Validation Expectations

Minimum validation for this Codex B pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
! rg -n '[ \t]$' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md
printf '%s\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin
! LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md
```

Expected results:

- Corpus parity remains `partial_coverage_map_ready`.
- `mythic_edge.private_log_report_only_drift` remains
  `blocked_private_evidence`.
- No private values, raw paths, exact offsets, exact file sizes, exact private
  timestamps, raw hashes, raw report data, or local-only artifact paths appear
  in the contract.

## Recommended Next Role

Recommended next role: Codex E / Module Reviewer.

Codex C implementation is not recommended for this issue because no code,
template, manifest, session-ledger, or tooling change is authorized. Codex E
should review the contract decision and confirm that #422 and #442 remain the
active boundaries for any future private-log drift execution.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #510.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/510

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Source artifact:
docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md

Target report:
docs/contract_test_reports/parser_corpus_private_log_drift_status_reconciliation.md

Goal:
Review the private-log drift status reconciliation contract. Confirm that it
preserves `mythic_edge.private_log_report_only_drift` as
`blocked_private_evidence`, does not authorize private log reads or private
drift execution, does not promote blocked rows, does not activate #388 / #381,
and does not weaken #422 or #442.

Do not implement code. Do not open a PR. Do not close #158, #388, #434, or
#510. Do not read private logs or run private checks. Do not claim parser
support, private smoke success, live Player.log health, drift health, release
readiness, production behavior, analytics truth, AI truth, coaching truth,
tracker completion, or full corpus parity.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/510"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/508"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/509"
  previous_merge_commit: "d9be4b704a3e7b6039794d805a5039c5e411963f"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_private_log_drift_status_reconciliation.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  selected_family: "mythic_edge.private_log_report_only_drift"
  status_decision: "preserve_blocked_private_evidence"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "! rg -n '[ \\t]$' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md"
    - "printf '%s\\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close #388 or #434 without separate authorization."
    - "Do not activate #388 / #381."
    - "Do not read private logs in Codex B/E."
    - "Do not run private Player.log, UTC_Log, app-data, live MTGA, diagnostics, network, firewall/drop, packet, OS/router, or private smoke checks."
    - "Do not create, commit, summarize, hash, bucket, or inspect private drift reports or local-only artifacts."
    - "Do not promote mythic_edge.private_log_report_only_drift or any blocked row by default."
    - "Do not claim parser support, private smoke success, live Player.log health, drift health, release readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity."
```
