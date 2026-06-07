# Private Local V1 High-Risk Scanner Findings Triage Comparison

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/260
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/252

## Contract

`docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`

## Internal Project Area

Quality / Governance, with Generated / Local Artifacts as the supporting area.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification. This handoff owns only the selected #260
high-risk triage classification and follow-up routing.

It does not own parser truth, analytics truth, workbook truth, webhook truth,
Apps Script deployment truth, credential policy, merge readiness, deploy
readiness, or tracker completion.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Branch: `codex/analytics-foundation`
- Starting status: one untracked #260 contract artifact,
  `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- No unrelated dirty tracked files were observed before editing.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/implementation_handoffs/private_local_v1_private_artifact_scanner_env_ignore_posture_comparison.md`
- `docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tools/check_local_environment.py`
- `tools/select_validation.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`
- `tests/test_check_protected_surfaces.py`
- selected high-risk finding paths reported by the scanner, inspected without
  copying raw matched values into this report
- GitHub issue #260, tracker #136, source issue #252, and PR #259 metadata

## Current Behavior Compared To Contract

The contract asks #260 to handle only the first selected high-risk tranche:

- `credential_value`
- `live_webhook_url`
- `workbook_export_marker`

Current scanner behavior matches the contract baseline:

| Scanner mode | Result |
| --- | --- |
| all-repo advisory | non-clean, exit code 0 |
| changed-path scanner against `origin/codex/analytics-foundation` | clean |
| path-scoped strictness | preserved |

The selected all-repo tranche remains present:

| Category | Forbidden | Warnings |
| --- | ---: | ---: |
| `credential_value` | 10 | 0 |
| `live_webhook_url` | 3 | 0 |
| `workbook_export_marker` | 3 | 0 |

All selected findings were triaged by category, path family, and safe context.
No raw matched values, endpoints, workbook identifiers, credential-looking
strings, private paths, or payload excerpts are included here.

## Implementation Option Chosen

Report-only triage and routing.

Reason: the selected tranche includes source files, tests, examples, tooling,
and an Apps Script-adjacent file. The lowest-risk safe action in this Codex C
pass is to classify and route each finding family without weakening scanner
coverage, changing scanner semantics, or editing protected behavior-adjacent
surfaces. This satisfies the comparison/report portion and creates a concrete
Codex E review target. Remediation remains intentionally scoped to follow-up
where a file edit would require additional review.

## Files Changed

- Added
  `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`

The untracked Codex B contract artifact was preserved and not edited:

- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`

## Exact Sections Changed

This report adds:

- issue, tracker, source issue, contract, and role metadata
- files inspected
- current scanner behavior compared to contract
- implementation option chosen
- selected high-risk all-repo scanner summary
- per-path classification table
- follow-up routing
- validation results
- protected-surface, secret/private-marker, and generated artifact status
- Codex E prompt and workflow handoff block

## Code/Test/Doc Status

- Code changed: no
- Tests changed: no
- Docs changed: yes
- Report-only: yes
- Scanner-policy-only: no

## All-Repo Scanner Summary

Refreshed summary during this pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 750
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected high-risk path families:

| Category | Path families |
| --- | --- |
| `credential_value` | root script, `examples/`, `src/`, `tests/`, `tools/` |
| `live_webhook_url` | `tests/` |
| `workbook_export_marker` | `tests/`, `tools/`, Apps Script-adjacent tooling |

## High-Risk Finding Classification

| Category | Path | Classification | Resolution |
| --- | --- | --- | --- |
| `credential_value` | `backfill_game_log_from_match_logs.py` | `scanner_false_positive` | Safe expression shape; no raw default recorded here. No edit in #260. |
| `credential_value` | `examples/live_print_filtered_v10_fixed.py` | `scanner_false_positive` | Environment-derived expression shape. No edit in #260. |
| `credential_value` | `examples/live_print_filtered_v8.py` | `scanner_false_positive` | Environment-derived expression shape. No edit in #260. |
| `credential_value` | `examples/live_print_filtered_v9.py` | `scanner_false_positive` | Environment-derived expression shape. No edit in #260. |
| `credential_value` | `src/mythic_edge_parser/app/card_catalog.py` | `scanner_false_positive` | Local parser/token variable expression, not a committed credential value. No edit in #260. |
| `credential_value` | `src/mythic_edge_parser/app/config.py` | `scanner_false_positive` | Environment helper expression. No credential-policy or env-contract edit in #260. |
| `credential_value` | `src/mythic_edge_parser/app/grp_id_candidates.py` | `scanner_false_positive` | Local parser/token variable expression, not a committed credential value. No edit in #260. |
| `credential_value` | `src/mythic_edge_parser/parsers/connection_error.py` | `scanner_false_positive` | Local parser/token variable expression, not a committed credential value. No edit in #260. |
| `credential_value` | `tests/test_sanitize.py` | `expected_synthetic_or_sanitized_test` | Sanitizer test fixture. Keep under Codex E review; optional follow-up can convert to fragment-built fixture. |
| `credential_value` | `tools/auto_launcher/manasight_launcher_auto.py` | `scanner_false_positive` | Function/method-call expression shape. No edit in #260. |
| `live_webhook_url` | `tests/test_evidence_runtime_status.py` | `defer_with_reason` | Test exercises privacy summary behavior, but current all-repo scanner still sees a full live-looking fixture. Follow-up should convert to fragment-built synthetic data or otherwise justify it. |
| `live_webhook_url` | `tests/test_evidence_validation_report_wiring.py` | `defer_with_reason` | Test exercises privacy summary behavior, but current all-repo scanner still sees a full live-looking fixture. Follow-up should convert to fragment-built synthetic data or otherwise justify it. |
| `live_webhook_url` | `tests/test_parser_diagnostics_mode.py` | `defer_with_reason` | Test exercises diagnostic redaction behavior, but current all-repo scanner still sees a full live-looking fixture. Follow-up should convert to fragment-built synthetic data or otherwise justify it. |
| `workbook_export_marker` | `tests/test_check_protected_surfaces.py` | `expected_synthetic_or_sanitized_test` | Protected-surface scanner test fixture. Keep detection strict; optional follow-up can fragment-build the fixture if reviewers require count reduction. |
| `workbook_export_marker` | `tools/check_protected_surfaces.py` | `expected_policy_or_contract_text` | Tooling rule text for protected workbook/export detection. No suppression or rule weakening in #260. |
| `workbook_export_marker` | `tools/google_apps_script/Code.gs` | `defer_with_reason` | Apps Script-adjacent workbook marker requires a separate protected-surface review before any edit. |

## Follow-Up Routing

Recommended follow-up routes before claiming full private-local-v1 private
artifact readiness:

1. Convert live-looking test fixtures in evidence-runtime, evidence-review, and
   parser-diagnostics tests to fragment-built synthetic data, then rerun the
   scanner tests and all-repo advisory scan.
2. Review the Apps Script-adjacent workbook marker under a protected-surface
   contract. If it is a real workbook identifier or deployment-sensitive value,
   replace it with an approved placeholder through the proper Apps Script /
   workbook authority path.
3. Consider a separate scanner-policy contract for expression-shape false
   positives if the project wants all-repo advisory counts to distinguish
   source expressions from committed literal values.

## Path-Scoped Scanner Strictness Status

Preserved. No scanner rules, scanner exit semantics, or path-scoped strictness
behavior changed.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch codex/analytics-foundation with two untracked #260 docs artifacts

py tools\check_secret_patterns.py --all
# advisory result remained non-clean as expected: forbidden 540, warnings 901, exit code 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
# passed; scanned_paths 0, forbidden 0, warnings 0

py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
# passed; 97 passed, 1 skipped

git diff --check
# passed

direct whitespace/ascii/final-newline check over the #260 docs
# passed

py tools\check_agent_docs.py
# passed; errors 0, warnings 0

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
# passed; changed_paths 0, forbidden 0, warnings 0

@'
docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md
docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; scanned_paths 2, forbidden 0, warnings 0

@'
docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md
docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; changed_paths 2, forbidden 0, warnings 0
```

## Protected-Surface Status

Passed for the #260 docs paths and base-diff scan. No protected runtime,
parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI, or
production behavior changed.

## Secret/Private-Marker Status

Passed for the #260 docs paths. No raw secret values, live endpoints, workbook
IDs, raw logs, private JSONL payloads, SQLite files, runtime files, retry
payload artifacts, workbook exports, app-data files, local env files, or
local-only artifacts were added to this report.

## Generated/Private Artifact Status

No generated or private artifacts were intentionally created, copied,
sanitized, imported, moved, deleted, or committed by this report-only pass.

## What Remains Unverified

- Codex E independent contract-test review.
- Whether the Apps Script-adjacent workbook marker is placeholder text,
  protected policy text, or a real value requiring replacement.
- Whether reviewers want immediate test-fixture rewrites for the live-looking
  webhook fixtures and sanitizer fixture.
- Whether a future scanner semantic refinement should distinguish safe source
  expressions from committed literal credential values.
- Full all-repo scanner cleanup; this pass does not claim all-repo cleanliness.
- #252 private-local-v1 private artifact readiness.
- Tracker #136 completion.

## Forbidden Scope

Forbidden scope was not intentionally touched:

- no parser behavior changed
- no parser state final reconciliation changed
- no analytics schema or migrations changed
- no workbook schema changed
- no webhook payload shape changed
- no Apps Script behavior changed
- no Google Sheets behavior changed
- no production behavior changed
- no OpenAI/model-provider or AI/coaching behavior changed
- no credential policy or environment-variable contract changed
- no CI gate added

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #260.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/260

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/252

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md

Expected review artifact:
docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md

Goal:
Review the Codex C #260 high-risk scanner findings triage against the contract. Verify that selected high-risk findings were classified without raw values, that path-scoped scanner strictness remains intact, that all-repo scanner remains advisory, and that any deferrals are explicit and safely routed.

Review focus:
- Check the classification of all 16 selected findings in `credential_value`, `live_webhook_url`, and `workbook_export_marker`.
- Confirm no raw matched values, endpoints, workbook IDs, secrets, private paths, or payload excerpts were copied into docs or reports.
- Decide whether report-only classification is sufficient for this #260 pass or whether Codex D should rewrite selected synthetic tests.
- Pay special attention to the Apps Script-adjacent workbook marker and route it to a protected-surface follow-up if needed.
- Confirm no scanner coverage was weakened and no path-scoped scanner strictness was relaxed.
- Confirm #252 private-local-v1 readiness and tracker #136 completion are not claimed.

Validation:
- git status --short --branch --untracked-files=all
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- path-scoped protected-surface and secret/private-marker scans over the #260 contract and handoff files

Do not:
- print or copy raw matched values, endpoints, workbook IDs, secrets, raw logs, private JSONL payloads, SQLite files, runtime files, retry payload artifacts, workbook exports, app-data files, local env files, or local-only artifacts;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior;
- change credential policy or environment-variable contracts;
- target main;
- stage, commit, push, open a PR, merge, close #260, close #252, or mark tracker #136 complete unless explicitly asked.

Final review output must include:
- role performed;
- issue/tracker/source issue;
- contract and handoff reviewed;
- findings first, ordered by severity;
- classification accuracy status;
- raw-value redaction status;
- path-scoped scanner strictness status;
- all-repo advisory/no-gate status;
- protected-surface status;
- secret/private-marker status;
- validation run and result;
- what remains unverified;
- whether forbidden scope was touched;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/260"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/252"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> two untracked #260 docs artifacts"
    - "py tools/check_secret_patterns.py --all -> advisory non-clean, forbidden 540, warnings 901, exit code 0"
    - "py tools/check_secret_patterns.py --base origin/codex/analytics-foundation -> passed"
    - "py -m pytest -q tests/test_check_secret_patterns.py tests/test_check_local_environment.py tests/test_check_protected_surfaces.py -> 97 passed, 1 skipped"
    - "git diff --check -> passed"
    - "direct whitespace/ascii/final-newline check over #260 docs -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation -> passed"
    - "path-scoped secret/private-marker scan over #260 docs -> passed"
    - "path-scoped protected-surface scan over #260 docs -> passed"
  stop_conditions:
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment-variable contracts."
    - "Do not target main, close #252, or close tracker #136."
```
